"""
=============================================================
  COWORKING SPACE — API REST de Autenticación
  Módulo: api.py
  Framework: Flask
  + SMTP Notifications + QR Access Passes + BI Export
=============================================================
"""

import os
import uuid
import time
import io
import csv
import base64
from flask import Flask, Response, request, jsonify, send_from_directory, send_file
from flask_cors import CORS


try:
    from auth import (
        AuthEventBus,
        ConsoleLogger,
        DatabaseObserver,
        EmailNotifier,
        SupabaseUserRepository,
        AuthService,
        BookingRepository,
        SpaceRepository,
        QRCodeGenerator,
        AuthEvent,
    )
except (ImportError, ValueError):
    from auth import (
        AuthEventBus,
        ConsoleLogger,
        DatabaseObserver,
        EmailNotifier,
        SupabaseUserRepository,
        AuthService,
        BookingRepository,
        SpaceRepository,
        QRCodeGenerator,
        AuthEvent,
    )

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=SRC_DIR, static_url_path="")
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]}})

@app.get("/")
def index():
    return send_from_directory(SRC_DIR, "login.html")

# Composición del sistema con Supabase
event_bus = AuthEventBus()
event_bus.subscribe(ConsoleLogger())
event_bus.subscribe(DatabaseObserver())
event_bus.subscribe(EmailNotifier())

repository = SupabaseUserRepository()  # ← 2. Conectamos el repositorio de la nube
auth_service = AuthService(repository=repository, event_bus=event_bus)
booking_repo = BookingRepository()
space_repo = SpaceRepository()

def _require_json_fields(data: dict, *fields: str):
    missing = [f for f in fields if not data.get(f)]
    if missing:
        return False, f"Campos requeridos: {', '.join(missing)}"
    return True, None


def _json_payload():
    return request.get_json(silent=True) or {}


@app.post("/api/auth/signup")
def signup():
    data = request.get_json(silent=True) or {}
    ok, err = _require_json_fields(data, "username", "email", "password", "confirm_password")
    if not ok:
        return jsonify({"success": False, "message": err, "errors": [err]}), 400

    result = auth_service.sign_up(
        username=data["username"].strip(),
        email=data["email"].strip().lower(),
        password=data["password"],
        confirm_password=data["confirm_password"],
        role=data.get("role", "member"),
    )
    status_code = 201 if result.success else 400
    return jsonify(result.to_dict()), status_code


@app.post("/api/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    ok, err = _require_json_fields(data, "username", "password")
    if not ok:
        return jsonify({"success": False, "message": err, "errors": [err]}), 400

    result = auth_service.log_in(
        username=data["username"].strip(),
        password=data["password"],
    )
    status_code = 200 if result.success else 401
    return jsonify(result.to_dict()), status_code

@app.get("/api/users")
def get_all_users():
    """Endpoint para que el Dashboard obtenga la lista real de usuarios."""
    users = repository.get_all()
    # Convertimos los objetos a diccionarios, pero ocultamos el password_hash por seguridad
    users_data = []
    for u in users:
        u_dict = u.to_dict()
        users_data.append(u_dict)

    return jsonify({
        "success": True,
        "data": users_data
    }), 200


@app.patch("/api/users/<username>")
def update_user(username):
    """Actualiza campos administrativos de un usuario."""
    data = _json_payload()
    user = repository.find_by_username(username)
    if not user:
        return jsonify({"success": False, "message": "No se encontro el usuario"}), 404

    if "is_active" in data:
        user.is_active = bool(data["is_active"])

    try:
        repository.update(user)
        return jsonify({"success": True, "data": user.to_dict()}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# --- ENDPOINTS DE RESERVAS ---

@app.get("/api/bookings")
def get_bookings():
    """Devuelve todas las reservas o las de un usuario puntual."""
    try:
        username = (request.args.get("username") or "").strip()
        bookings = booking_repo.get_by_username(username) if username else booking_repo.get_all()
        return jsonify({"success": True, "data": bookings}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": []}), 500


@app.post("/api/bookings")
def create_booking():
    """Crea una nueva reserva con un ID auto-generado (timestamp-based)."""
    data = request.json
    
    # Validamos que estén los datos necesarios
    if not all([data.get("username"), data.get("space_name"), data.get("booking_date"), data.get("booking_time")]):
        return jsonify({"success": False, "message": "Faltan datos para la reserva"}), 400

    # Generamos un ID numérico usando timestamp en milisegundos + aleatorio
    # Esto garantiza unicidad sin depender de secuencias de BD
    booking_id = int(time.time() * 1000) + int(uuid.uuid4().int % 10000)

    # Armamos el diccionario CON el campo 'id' generado
    new_booking = {
        "id": booking_id,
        "username": data["username"],
        "space_name": data["space_name"],
        "booking_date": data["booking_date"],
        "booking_time": data["booking_time"],
        "status": "pendiente"
    }

    # Información adicional del cliente (nombre, apellido, email, tel, notas)
    # Se guarda como JSON string en la columna 'additional_info' (opcional)
    import json as _json
    if data.get("additional_info"):
        try:
            ai = data["additional_info"]
            new_booking["additional_info"] = _json.dumps(ai) if isinstance(ai, dict) else str(ai)
        except Exception:
            pass  # si falla, seguimos sin el campo adicional

    try:
        # Usamos el método limpio del repositorio
        result = booking_repo.create(new_booking)
        return jsonify({"success": True, "message": "Reserva guardada", "data": result}), 201
    except Exception as e:
        print(f"Error al crear reserva: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

# Usamos @app.route para evitar el bloqueo 405 de CORS
@app.route("/api/bookings/<booking_id>", methods=["PATCH", "OPTIONS"])
def update_booking_status(booking_id):
    """Permite al administrador aprobar o rechazar una reserva.
    Al confirmar: genera QR + envía email de aprobación.
    Al rechazar: envía email de rechazo."""
    # Responder al preflight CORS manualmente por si flask-cors no lo captura
    if request.method == "OPTIONS":
        from flask import make_response
        resp = make_response("", 204)
        resp.headers["Access-Control-Allow-Origin"]  = "*"
        resp.headers["Access-Control-Allow-Methods"] = "PATCH, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return resp

    try:
        new_status = _json_payload().get("status")
        if not new_status:
            return jsonify({"success": False, "message": "Falta el campo 'status'"}), 400

        # Intentamos convertir a entero si es posible (tabla con PK entera)
        try:
            booking_id_typed = int(booking_id)
        except (ValueError, TypeError):
            booking_id_typed = booking_id  # UUID o string

        # 1) Obtenemos la reserva actual para tener datos del usuario
        booking = booking_repo.get_by_id(booking_id_typed)
        if not booking:
            return jsonify({"success": False, "message": f"No se encontró la reserva con id={booking_id}"}), 404

        # 2) Actualizamos el estado
        result = booking_repo.update_status(booking_id_typed, new_status)

        # 3) SI la actualización fue exitosa, disparamos email + QR
        if result:
            username = booking.get("username")
            user = repository.find_by_username(username) if username else None
            user_email = user.email if user else None

            status_lower = new_status.lower()

            if status_lower in ("confirmada", "confirmed"):
                # ── GENERAR QR ──
                qr_token = QRCodeGenerator.generate_token(booking_id_typed, username or "")
                # Guardamos el token en la BD (silencioso si la columna aun no existe en Supabase)
                booking_repo.update_qr_token(booking_id_typed, qr_token)
                qr_bytes = QRCodeGenerator.generate_image(booking_id_typed, username or "")

                # ── DISPARAR EMAIL DE CONFIRMACIÓN (async) ──
                event_bus.publish(AuthEvent(AuthEvent.BOOKING_CONFIRMED, {
                    "booking_id":     str(booking_id_typed),
                    "username":       username,
                    "email":          user_email,
                    "space_name":     booking.get("space_name"),
                    "booking_date":   booking.get("booking_date"),
                    "booking_time":   booking.get("booking_time"),
                    "qr_token":       qr_token,
                    "qr_image_bytes": qr_bytes,  # EmailNotifier lo adjuntará
                }))

                # Devolvemos la reserva actualizada con datos del QR
                result["qr_token"] = qr_token
                result["qr_data_uri"] = QRCodeGenerator.generate_data_uri(booking_id_typed, username or "")

                return jsonify({
                    "success": True,
                    "message": f"Reserva confirmada. Se envió email de notificación al cliente.",
                    "data": result
                }), 200

            elif status_lower in ("rechazada", "rechazado", "cancelada", "cancelled"):
                # ── DISPARAR EMAIL DE RECHAZO (async) ──
                event_bus.publish(AuthEvent(AuthEvent.BOOKING_REJECTED, {
                    "booking_id":   str(booking_id_typed),
                    "username":     username,
                    "email":        user_email,
                    "space_name":   booking.get("space_name"),
                    "booking_date": booking.get("booking_date"),
                    "booking_time": booking.get("booking_time"),
                }))

                return jsonify({
                    "success": True,
                    "message": f"Reserva rechazada. Se notificó al cliente vía email.",
                    "data": result
                }), 200

            else:
                return jsonify({
                    "success": True,
                    "message": f"Reserva actualizada a '{new_status}'",
                    "data": result
                }), 200

        # Si Supabase no devuelve data, igual puede haber actualizado (0 rows afectadas = 404)
        return jsonify({"success": False, "message": f"No se encontró la reserva con id={booking_id}"}), 404

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500


@app.get("/api/bookings/<booking_id>/qr")
def get_booking_qr(booking_id):
    """Devuelve la imagen PNG del QR de acceso para una reserva confirmada."""
    try:
        try:
            booking_id_typed = int(booking_id)
        except (ValueError, TypeError):
            booking_id_typed = booking_id

        booking = booking_repo.get_by_id(booking_id_typed)
        if not booking:
            return jsonify({"success": False, "message": "Reserva no encontrada"}), 404

        status = (booking.get("status") or "").lower()
        if status not in ("confirmada", "confirmed"):
            return jsonify({"success": False, "message": "La reserva no está confirmada"}), 400

        username = booking.get("username", "")
        qr_bytes = QRCodeGenerator.generate_image(booking_id_typed, username)
        
        return send_file(
            io.BytesIO(qr_bytes),
            mimetype="image/png",
            as_filename=f"pase_acceso_{booking_id}.png"
        )
       
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500


@app.get("/api/bookings/<booking_id>/qr-datauri")
def get_booking_qr_datauri(booking_id):
    """Devuelve el QR como Data URI (base64) para embeber en HTML."""
    try:
        try:
            booking_id_typed = int(booking_id)
        except (ValueError, TypeError):
            booking_id_typed = booking_id

        booking = booking_repo.get_by_id(booking_id_typed)
        if not booking:
            return jsonify({"success": False, "message": "Reserva no encontrada"}), 404

        status = (booking.get("status") or "").lower()
        if status not in ("confirmada", "confirmed"):
            return jsonify({"success": False, "message": "La reserva no está confirmada"}), 400

        username = booking.get("username", "")
        data_uri = QRCodeGenerator.generate_data_uri(booking_id_typed, username)

        return jsonify({"success": True, "data": {"qr_data_uri": data_uri, "qr_token": booking.get("qr_token", "")}}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500


# --- ENDPOINTS PARA ESPACIOS (ABM) ---
@app.get("/api/spaces")
def get_spaces():
    """Devuelve el catalogo de espacios."""
    try:
        return jsonify({"success": True, "data": space_repo.get_all()}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "data": []}), 500


@app.post("/api/spaces")
def create_space():
    """Crea un nuevo espacio con un ID auto-generado"""
    data = _json_payload()
    ok, err = _require_json_fields(data, "name", "type", "capacity", "price")
    if not ok:
        return jsonify({"success": False, "message": err, "errors": [err]}), 400

    try:
        # Generamos un ID numérico para el espacio si no lo proporciona
        if not data.get("id"):
            data["id"] = int(time.time() * 1000) + int(uuid.uuid4().int % 10000)
        
        # ¡Usamos el método limpio del repositorio!
        result = space_repo.create(data)
        return jsonify({"success": True, "data": result}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.put("/api/spaces/<space_id>")
def edit_space(space_id):
    """Edita un espacio existente"""
    data = _json_payload()
    if not data:
        return jsonify({"success": False, "message": "No se recibieron datos para actualizar"}), 400

    try:
        # ¡Usamos el método limpio del repositorio!
        result = space_repo.update(space_id, data)
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ═══════════════════════════════════════════════════════════════
# MÓDULO DE INTELIGENCIA DE NEGOCIOS — EXPORTACIÓN CSV
# ═══════════════════════════════════════════════════════════════

@app.get("/api/export/estadistica")
def export_estadistica():
    """
    Exporta un reporte CSV estructurado con todas las reservas activas,
    calculando horas reservadas e ingresos estimados por espacio.
    Filtros opcionales: ?month=MM&year=YYYY
    """
    try:
        # a) Obtén todas las reservas activas.
        all_bookings = booking_repo.get_all()
        # Se consideran activas aquellas que no están canceladas o rechazadas
        active_bookings = [
            b for b in all_bookings 
            if b.get("status", "").lower() not in ["cancelada", "rechazada", "cancelled"]
        ]

        # Filtros opcionales por mes y año
        month_filter = request.args.get("month", "")
        year_filter  = request.args.get("year", "")
        if month_filter and year_filter:
            try:
                m, y = int(month_filter), int(year_filter)
                active_bookings = [
                    b for b in active_bookings
                    if _extract_month_year(b.get("booking_date", ""), y, m)
                ]
            except ValueError:
                pass  # ignorar filtros inválidos

        # Necesitamos los costos de los espacios
        spaces = space_repo.get_all()
        space_prices = {}
        for sp in spaces:
            try:
                space_prices[sp["name"]] = float(sp.get("price", 0))
            except (ValueError, TypeError):
                space_prices[sp["name"]] = 0.0

        si = io.StringIO()
        cw = csv.writer(si)
        
        # Columnas: ID_Reserva, Usuario, Espacio, Fecha, Horas_Reservadas, Ingreso_Estimado_ARS, Estado
        cw.writerow(["ID_Reserva", "Usuario", "Espacio", "Fecha", "Horas_Reservadas", "Ingreso_Estimado_ARS", "Estado"])

        for b in active_bookings:
            # b) Calcula "Horas_Reservadas" contando la cantidad de slots horarios
            time_str = b.get("booking_time", "")
            horas = len(time_str.split(",")) if time_str else 0
            
            # c) Calcula "Ingreso_Estimado_ARS" multiplicando las horas por el costo del espacio
            costo_espacio = space_prices.get(b.get("space_name"), 0.0)
            ingreso = horas * costo_espacio

            cw.writerow([
                b.get("id", ""),
                b.get("username", ""),
                b.get("space_name", ""),
                b.get("booking_date", ""),
                horas,
                ingreso,
                b.get("status", "")
            ])

        output = si.getvalue()
        si.close()

        # Nombre de archivo dinámico según filtros
        filename = "SpicyTech_Estadistica_2026.csv"
        if month_filter and year_filter:
            filename = f"SpicyTech_Estadistica_{year_filter}{int(month_filter):02d}.csv"

        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


def _extract_month_year(date_str: str, year: int, month: int) -> bool:
    """Helper: verifica si una fecha ISO (yyyy-mm-dd) coincide con año/mes dados."""
    if not date_str or len(date_str) < 7:
        return False
    try:
        parts = date_str.split("-")
        return int(parts[0]) == year and int(parts[1]) == month
    except (ValueError, IndexError):
        return False


if __name__ == "__main__":
    app.run(debug=True, port=5000)
