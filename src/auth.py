"""
=============================================================
  COWORKING SPACE — Authentication Backend
  Módulo: auth.py
  Patrones: Observer, Factory Method
  + JWT + bcrypt + Supabase + SMTP + QR
=============================================================
"""

from __future__ import annotations
from abc import abstractmethod

import bcrypt
import jwt
import re
import time
import uuid
import json
import os
import io
import base64
import threading
import resend
import qrcode
from datetime import datetime, timedelta
from typing import Any
from supabase import create_client, Client

# ---------- JWT Secret (cambiar en producción) ----------
JWT_SECRET = "nexo_coworking_super_secret_key_2025"
JWT_EXPIRATION_HOURS = 2

# ---------- Supabase ----------
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://kyjszgpgyykktbhsqqjg.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_7XJYNkkzzbg7HZC7bEqv3w_zxFFxd8U")

# Inicializamos el cliente UNA sola vez para todo el módulo (Mejora drástica de rendimiento)
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "info@spicytech.com")
CONTACT_PHONE = os.environ.get("CONTACT_PHONE", "+54 11 0000-0000")
CONTACT_WEB = os.environ.get("CONTACT_WEB", "http://127.0.0.1:5000")


class SupabaseTableRepository:
    """Base para repositorios que persisten en una tabla de Supabase."""

    def __init__(self, client: Client | None = None):
        self._client = client or supabase_client

    def _table(self, table_name: str):
        return self._client.table(table_name)

    @staticmethod
    def _first_row(response: Any) -> dict | None:
        data = getattr(response, "data", None) or []
        return data[0] if data else None

    @staticmethod
    def _coerce_id(record_id: Any) -> Any:
        try:
            return int(record_id)
        except (TypeError, ValueError):
            return str(record_id)

    @staticmethod
    def _generate_numeric_id() -> int:
        return int(time.time() * 1000) + int(uuid.uuid4().int % 10000)

# ---------- Resend Configuración (Email API) ----------
# RESEND_API_KEY: se obtiene en https://resend.com/api-keys (Sending access).
# EMAIL_FROM: mientras no verifiques un dominio propio en Resend, usá el sandbox
#             "onboarding@resend.dev". En ese modo, Resend SOLO entrega a la casilla
#             con la que te registraste en Resend (ej. santi481manrique@gmail.com).
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
EMAIL_FROM = os.environ.get("EMAIL_FROM", "SpicyTech Coworking <onboarding@resend.dev>")
resend.api_key = RESEND_API_KEY


# ═══════════════════════════════════════════════════════════════
# SECCIÓN 1 ─ OBSERVER PATTERN
# ═══════════════════════════════════════════════════════════════

class AuthEvent:
    USER_REGISTERED  = "USER_REGISTERED"
    LOGIN_SUCCESS    = "LOGIN_SUCCESS"
    LOGIN_FAILED     = "LOGIN_FAILED"
    ACCOUNT_LOCKED   = "ACCOUNT_LOCKED"
    PASSWORD_CHANGED = "PASSWORD_CHANGED"
    # Nuevos eventos de reserva
    BOOKING_CONFIRMED = "BOOKING_CONFIRMED"
    BOOKING_REJECTED  = "BOOKING_REJECTED"
    BOOKING_UPGRADE_AVAILABLE = "BOOKING_UPGRADE_AVAILABLE"

    def __init__(self, event_type: str, payload: dict[str, Any]):
        self.event_type = event_type
        self.payload    = payload
        self.timestamp  = datetime.utcnow().isoformat()

    def __repr__(self) -> str:
        return f"AuthEvent(type={self.event_type}, at={self.timestamp})"


class AuthObserver:
    def update(self, event: AuthEvent) -> None:
        ...


class AuthEventBus:
    def __init__(self):
        self._observers: list[AuthObserver] = []

    def subscribe(self, observer: AuthObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: AuthObserver) -> None:
        self._observers = [o for o in self._observers if o is not observer]

    def publish(self, event: AuthEvent) -> None:
        for observer in self._observers:
            observer.update(event)


class ConsoleLogger(AuthObserver):
    def update(self, event: AuthEvent) -> None:
        print(f"[LOG] {event.timestamp} | {event.event_type} | {event.payload}")


class DatabaseObserver(AuthObserver):
    """Persiste cada evento de autenticación en la tabla auth_events de Supabase."""
    def __init__(self, db_path: str = None):
        pass # Acepta un arg opcional por compatibilidad con código viejo

    def _json_safe(self, value: Any):
        if isinstance(value, bytes):
            return {"__type": "bytes", "length": len(value)}
        if isinstance(value, dict):
            return {key: self._json_safe(item) for key, item in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [self._json_safe(item) for item in value]
        try:
            json.dumps(value)
            return value
        except TypeError:
            return str(value)

    def update(self, event: AuthEvent) -> None:
        try:
            supabase_client.table("auth_events").insert({
                "event_type": event.event_type,
                "payload":    json.dumps(self._json_safe(event.payload), ensure_ascii=False),
                "timestamp":  event.timestamp,
            }).execute()
        except Exception as exc:
            print(f"[DatabaseObserver] Error al guardar evento: {exc}")


# ═══════════════════════════════════════════════════════════════
# SECCIÓN 1.5 ─ EMAIL NOTIFIER (SMTP REAL)
# ═══════════════════════════════════════════════════════════════

class EmailNotifier(AuthObserver):
    """
    Envía notificaciones por email usando SMTP (Gmail).
    Se ejecuta de forma asíncrona en un thread separado para no bloquear la API.
    """

    def update(self, event: AuthEvent) -> None:
        """Reactúa a eventos del sistema disparando emails."""
        if event.event_type == AuthEvent.USER_REGISTERED:
            self._send_async(
                to=event.payload.get("email"),
                subject="¡Bienvenido a SpicyTech Coworking!",
                body=self._template_welcome(event.payload)
            )
        elif event.event_type == AuthEvent.BOOKING_CONFIRMED:
            self._send_async(
                to=event.payload.get("email"),
                subject="✅ Tu reserva fue confirmada · SpicyTech",
                body=self._template_confirmed(event.payload),
                attach_qr=event.payload.get("qr_image_bytes"),
                qr_filename=f"pase_acceso_{event.payload.get('booking_id', 'reserva')}.png"
            )
        elif event.event_type == AuthEvent.BOOKING_REJECTED:
            self._send_async(
                to=event.payload.get("email"),
                subject="❌ Tu reserva fue rechazada · SpicyTech",
                body=self._template_rejected(event.payload)
            )
        elif event.event_type == AuthEvent.BOOKING_UPGRADE_AVAILABLE:
            self._send_async(
                to=event.payload.get("email"),
                subject="🚀 Upgrade a jornada completa · SpicyTech",
                body=self._template_upgrade(event.payload)
            )

    def _send_async(self, to: str, subject: str, body: str, attach_qr: bytes = None, qr_filename: str = None):
        """Dispara el envío en un thread en segundo plano."""
        if not to:
            print("[EmailNotifier] No se envía email: destinatario vacío.")
            return
        thread = threading.Thread(
            target=self._send_email,
            args=(to, subject, body, attach_qr, qr_filename),
            daemon=True
        )
        thread.start()

    def _send_email(self, to: str, subject: str, html_body: str, attach_qr: bytes = None, qr_filename: str = None):
        """Envío real vía Resend (Email API)."""
        try:
            if not RESEND_API_KEY:
                raise RuntimeError(
                    "Configuración de Resend incompleta: definí RESEND_API_KEY en las variables de entorno. "
                    "Podés generarla en https://resend.com/api-keys"
                )

            params: resend.Emails.SendParams = {
                "from": EMAIL_FROM,
                "to": [to],
                "subject": subject,
                "html": html_body,
            }

            # Adjuntar QR si existe (como inline image vía Content-ID)
            if attach_qr and qr_filename:
                params["attachments"] = [{
                    "filename": qr_filename,
                    "content": base64.b64encode(attach_qr).decode("utf-8"),
                    "content_id": "qr_code",
                }]

            email = resend.Emails.send(params)
            print(f"[EmailNotifier] ✅ Email enviado a {to} · {subject} · id={email.get('id')}")
        except Exception as exc:
            print(f"[EmailNotifier] ❌ Error enviando email a {to}: {exc}")

    # ── Templates de email ──

    def _template_welcome(self, p: dict) -> str:
        return f"""\
<html><body style="font-family:'Segoe UI',Arial,sans-serif;color:#2C1A10;background:#FAF6F0;padding:20px;">
<div style="max-width:520px;margin:0 auto;background:#fff;border-radius:16px;padding:32px;border:1px solid #E8DDD0;">
  <h2 style="color:#C0392B;font-family:Georgia,serif;">🌶️ ¡Bienvenido a SpicyTech, {p.get('username')}!</h2>
  <p style="line-height:1.7;">Tu cuenta ha sido creada exitosamente. Ya podés iniciar sesión y empezar a reservar espacios de trabajo.</p>
  <ul style="line-height:1.8;">
    <li>📅 Reservá salas en tiempo real</li>
    <li>🏢 Accedé a oficinas privadas</li>
    <li>📊 Gestioná tu historial de uso</li>
  </ul>
  <p style="margin-top:20px;"><a href="#" style="background:#C0392B;color:#fff;padding:12px 24px;border-radius:10px;text-decoration:none;font-weight:600;">Iniciar sesión →</a></p>
    <p style="font-size:12px;color:#A08870;margin-top:24px;">SpicyTech Coworking · {CONTACT_EMAIL} · {CONTACT_PHONE}</p>
</div></body></html>"""

    def _template_confirmed(self, p: dict) -> str:
        qr_img_tag = '<img src="cid:qr_code" style="width:180px;height:180px;border-radius:12px;border:2px solid #E8DDD0;margin:16px 0;"><br><span style="font-size:12px;color:#7A5C44;">Mostrá este código en recepción para acceder</span>' if p.get("qr_image_bytes") else ""
        return f"""\
<html><body style="font-family:'Segoe UI',Arial,sans-serif;color:#2C1A10;background:#FAF6F0;padding:20px;">
<div style="max-width:520px;margin:0 auto;background:#fff;border-radius:16px;padding:32px;border:1px solid #E8DDD0;">
  <h2 style="color:#2E7D52;font-family:Georgia,serif;">✅ Reserva Confirmada</h2>
  <p style="line-height:1.7;">Hola <strong>{p.get('username')}</strong>, tu reserva fue <strong>aprobada</strong> por el equipo de SpicyTech.</p>
  <div style="background:#F0FBF4;border-radius:12px;padding:16px;margin:16px 0;border-left:4px solid #22C55E;">
    <p style="margin:4px 0;"><strong>Espacio:</strong> {p.get('space_name')}</p>
    <p style="margin:4px 0;"><strong>Fecha:</strong> {p.get('booking_date')}</p>
    <p style="margin:4px 0;"><strong>Horario:</strong> {p.get('booking_time')}</p>
    <p style="margin:4px 0;"><strong>Estado:</strong> <span style="color:#2E7D52;font-weight:700;">CONFIRMADA</span></p>
  </div>
  <div style="text-align:center;margin:20px 0;background:#FAF6F0;border-radius:12px;padding:20px;">
    <div style="font-size:13px;font-weight:600;color:#C0392B;margin-bottom:8px;">🎫 Tu Pase de Acceso Inteligente</div>
    {qr_img_tag}
  </div>
    <p style="font-size:13px;color:#7A5C44;line-height:1.6;">Presentá este código QR en la recepción del edificio al momento de tu llegada. No es necesario imprimirlo — podés mostrarlo desde tu celular.</p>
    <p style="font-size:12px;color:#A08870;margin-top:24px;">SpicyTech Coworking · {CONTACT_EMAIL} · {CONTACT_PHONE} · <a href="{CONTACT_WEB}/mis-reservas.html">Ver mis reservas</a></p>
</div></body></html>"""

    def _template_rejected(self, p: dict) -> str:
        return f"""\
<html><body style="font-family:'Segoe UI',Arial,sans-serif;color:#2C1A10;background:#FAF6F0;padding:20px;">
<div style="max-width:520px;margin:0 auto;background:#fff;border-radius:16px;padding:32px;border:1px solid #E8DDD0;">
  <h2 style="color:#C0392B;font-family:Georgia,serif;">❌ Reserva Rechazada</h2>
  <p style="line-height:1.7;">Hola <strong>{p.get('username')}</strong>, lamentamos informarte que tu solicitud de reserva no pudo ser confirmada.</p>
  <div style="background:#FEE9E7;border-radius:12px;padding:16px;margin:16px 0;border-left:4px solid #C0392B;">
    <p style="margin:4px 0;"><strong>Espacio:</strong> {p.get('space_name')}</p>
    <p style="margin:4px 0;"><strong>Fecha:</strong> {p.get('booking_date')}</p>
    <p style="margin:4px 0;"><strong>Horario:</strong> {p.get('booking_time')}</p>
    <p style="margin:4px 0;"><strong>Motivo:</strong> El espacio ya no está disponible para la fecha y horario solicitados.</p>
  </div>
    <p style="line-height:1.7;">Te invitamos a realizar una nueva reserva seleccionando otro espacio o horario alternativo.</p>
    <p style="margin-top:20px;"><a href="{CONTACT_WEB}/spaces.html" style="background:#C0392B;color:#fff;padding:12px 24px;border-radius:10px;text-decoration:none;font-weight:600;">Buscar otros espacios →</a></p>
    <p style="font-size:12px;color:#A08870;margin-top:24px;">SpicyTech Coworking · {CONTACT_EMAIL} · {CONTACT_PHONE}</p>
</div></body></html>"""

    def _template_upgrade(self, p: dict) -> str:
        return f"""\
<html><body style="font-family:'Segoe UI',Arial,sans-serif;color:#2C1A10;background:#FAF6F0;padding:20px;">
<div style="max-width:520px;margin:0 auto;background:#fff;border-radius:16px;padding:32px;border:1px solid #E8DDD0;">
  <h2 style="color:#C0392B;font-family:Georgia,serif;">🚀 Upgrade a jornada completa</h2>
  <p style="line-height:1.7;">Hola <strong>{p.get('username')}</strong>, detectamos que reservaste con bastante anticipación y tu patrón histórico sugiere una oportunidad de mayor uso del espacio.</p>
  <div style="background:#F0FBF4;border-radius:12px;padding:16px;margin:16px 0;border-left:4px solid #2E7D52;">
    <p style="margin:4px 0;"><strong>Espacio:</strong> {p.get('space_name')}</p>
    <p style="margin:4px 0;"><strong>Fecha:</strong> {p.get('booking_date')}</p>
    <p style="margin:4px 0;"><strong>Anticipación detectada:</strong> {p.get('days_ahead')} días</p>
    <p style="margin:4px 0;"><strong>Correlación observada:</strong> r={p.get('correlation_r')}</p>
  </div>
  <p style="line-height:1.7;">Te recomendamos considerar un <strong>upgrade a jornada completa</strong> para aprovechar mejor el espacio y consolidar tu agenda del día.</p>
  <p style="margin-top:20px;"><a href="{CONTACT_WEB}/spaces.html" style="background:#C0392B;color:#fff;padding:12px 24px;border-radius:10px;text-decoration:none;font-weight:600;">Ver opciones de upgrade →</a></p>
  <p style="font-size:12px;color:#A08870;margin-top:24px;">SpicyTech Coworking · {CONTACT_EMAIL} · {CONTACT_PHONE}</p>
</div></body></html>"""


# ═══════════════════════════════════════════════════════════════
# SECCIÓN 1.6 ─ QR CODE GENERATOR
# ═══════════════════════════════════════════════════════════════

class QRCodeGenerator:
    """Genera códigos QR únicos para pases de acceso."""

    QR_SECRET = "spicytech_qr_secret_2026"

    @classmethod
    def generate_token(cls, booking_id: str | int, username: str) -> str:
        """Genera un token único e inalterable para la reserva."""
        payload = f"{booking_id}:{username}:{cls.QR_SECRET}"
        import hashlib
        return hashlib.sha256(payload.encode()).hexdigest()[:32]

    @classmethod
    def generate_payload(cls, booking_id: str | int, username: str) -> str:
        """Genera el payload real que se codifica dentro del QR."""
        return json.dumps({
            "booking_id": str(booking_id),
            "username": username,
            "token": cls.generate_token(booking_id, username),
        }, ensure_ascii=False, separators=(",", ":"))

    @classmethod
    def generate_image(cls, booking_id: str | int, username: str, size: int = 10) -> bytes:
        """Genera la imagen PNG del QR como bytes."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=size,
            border=4,
        )
        # El QR contiene el identificador de la reserva y el usuario asociado.
        qr.add_data(cls.generate_payload(booking_id, username))
        qr.make(fit=True)

        img = qr.make_image(fill_color="#1C1209", back_color="#FAF6F0")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

    @classmethod
    def generate_data_uri(cls, booking_id: str | int, username: str) -> str:
        """Genera un Data URI para embeber el QR directamente en HTML."""
        png_bytes = cls.generate_image(booking_id, username)
        b64 = base64.b64encode(png_bytes).decode("ascii")
        return f"data:image/png;base64,{b64}"


# ═══════════════════════════════════════════════════════════════
# SECCIÓN 2 ─ MODELOS DE USUARIO
# ═══════════════════════════════════════════════════════════════

class User:
    def __init__(
        self,
        user_id:       str,
        username:      str,
        email:         str,
        password_hash: str,
        role:          str,
    ):
        self.user_id       = user_id
        self.username      = username
        self.email         = email
        self.password_hash = password_hash
        self.role          = role
        self.is_active     = True
        self.created_at    = datetime.utcnow().isoformat()
        self.failed_attempts: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id":    self.user_id,
            "username":   self.username,
            "email":      self.email,
            "role":       self.role,
            "is_active":  self.is_active,
            "created_at": self.created_at,
        }


class MemberUser(User):
    def __init__(self, user_id, username, email, password_hash):
        super().__init__(user_id, username, email, password_hash, role="member")


class AdminUser(User):
    def __init__(self, user_id, username, email, password_hash):
        super().__init__(user_id, username, email, password_hash, role="admin")


class GuestUser(User):
    def __init__(self, user_id, username, email, password_hash):
        super().__init__(user_id, username, email, password_hash, role="guest")


# ═══════════════════════════════════════════════════════════════
# SECCIÓN 3 ─ FACTORY METHOD
# ═══════════════════════════════════════════════════════════════

class UserFactory:
    @abstractmethod
    def create_user(self, user_id, username, email, password_hash) -> User:
        ...

    def build(self, username, email, password_hash) -> User:
        user_id = str(uuid.uuid4())
        return self.create_user(user_id, username, email, password_hash)


class MemberFactory(UserFactory):
    def create_user(self, user_id, username, email, password_hash) -> MemberUser:
        return MemberUser(user_id, username, email, password_hash)


class AdminFactory(UserFactory):
    def create_user(self, user_id, username, email, password_hash) -> AdminUser:
        return AdminUser(user_id, username, email, password_hash)


class GuestFactory(UserFactory):
    def create_user(self, user_id, username, email, password_hash) -> GuestUser:
        return GuestUser(user_id, username, email, password_hash)


class UserFactoryRegistry:
    _factories: dict[str, UserFactory] = {
        "member": MemberFactory(),
        "admin":  AdminFactory(),
        "guest":  GuestFactory(),
    }

    @classmethod
    def get(cls, role: str) -> UserFactory:
        factory = cls._factories.get(role.lower())
        if not factory:
            raise ValueError(f"Rol desconocido: '{role}'. Disponibles: {list(cls._factories)}")
        return factory

    @classmethod
    def register(cls, role: str, factory: UserFactory) -> None:
        cls._factories[role.lower()] = factory


# ═══════════════════════════════════════════════════════════════
# SECCIÓN 4 ─ REPOSITORIO
# ═══════════════════════════════════════════════════════════════

class UserRepository:
    def save(self, user: User) -> None: ...
    def find_by_username(self, username: str) -> User | None: ...
    def find_by_email(self, email: str) -> User | None: ...
    def update(self, user: User) -> None: ...


class InMemoryUserRepository(UserRepository):
    """Repositorio en memoria (útil para tests)."""

    def __init__(self):
        self._store: dict[str, User] = {}

    def save(self, user: User) -> None:
        self._store[user.username] = user

    def find_by_username(self, username: str) -> User | None:
        return self._store.get(username)

    def find_by_email(self, email: str) -> User | None:
        return next((u for u in self._store.values() if u.email == email), None)

    def update(self, user: User) -> None:
        if user.username in self._store:
            self._store[user.username] = user


class SupabaseUserRepository(SupabaseTableRepository, UserRepository):
    """Repositorio persistente usando Supabase."""
    def __init__(self, db_path: str = None, client: Client | None = None):
        super().__init__(client)
        pass # Acepta db_path para no romper compatibilidad con api.py

    def _row_to_user(self, row: dict) -> User:
        role = row.get("role", "member")
        constructors = {
            "member": MemberUser,
            "admin":  AdminUser,
            "guest":  GuestUser,
        }
        cls = constructors.get(role, MemberUser)
        user = cls(
            user_id       = row["user_id"],
            username      = row["username"],
            email         = row["email"],
            password_hash = row["password_hash"],
        )
        user.is_active       = bool(row.get("is_active", True))
        user.failed_attempts = row.get("failed_attempts", 0)
        user.created_at      = row.get("created_at", datetime.utcnow().isoformat())
        return user

    def save(self, user: User) -> None:
        self._table("users").insert({
            "user_id":         user.user_id,
            "username":        user.username,
            "email":           user.email,
            "password_hash":   user.password_hash,
            "role":            user.role,
            "is_active":       int(user.is_active), # ← ¡Acá está la magia! Forzamos 1 o 0
            "failed_attempts": user.failed_attempts,
            "created_at":      user.created_at,
        }).execute()

    def find_by_username(self, username: str) -> User | None:
        response = self._table("users").select("*").eq("username", username).execute()
        if response.data:
            return self._row_to_user(response.data[0])
        return None

    def find_by_email(self, email: str) -> User | None:
        response = self._table("users").select("*").eq("email", email).execute()
        if response.data:
            return self._row_to_user(response.data[0])
        return None

    def get_all(self) -> list[User]:
        """Obtiene todos los usuarios registrados en Supabase."""
        response = self._table("users").select("*").execute()
        if response.data:
            return [self._row_to_user(row) for row in response.data]
        return []

    def update(self, user: User) -> None:
        self._table("users").update({
            "email":           user.email,
            "password_hash":   user.password_hash,
            "is_active":       int(user.is_active), # ← Acá también
            "failed_attempts": user.failed_attempts,
        }).eq("username", user.username).execute()


# Alias clave para mantener compatibilidad con el servidor Flask actual
SQLiteUserRepository = SupabaseUserRepository


# ═══════════════════════════════════════════════════════════════
# SECCIÓN 5 ─ VALIDACIONES Y HASHING
# ═══════════════════════════════════════════════════════════════

class PasswordPolicy:
    MIN_LENGTH = 8

    @classmethod
    def validate(cls, password: str) -> tuple[bool, list[str]]:
        errors = []
        if len(password) < cls.MIN_LENGTH:
            errors.append(f"Debe tener al menos {cls.MIN_LENGTH} caracteres.")
        if not re.search(r"[A-Z]", password):
            errors.append("Debe contener al menos una letra mayúscula.")
        if not re.search(r"[a-z]", password):
            errors.append("Debe contener al menos una letra minúscula.")
        if not re.search(r"\d", password):
            errors.append("Debe contener al menos un número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            errors.append("Debe contener al menos un carácter especial.")
        return (len(errors) == 0, errors)


class InputValidator:
    @staticmethod
    def is_valid_username(username: str) -> tuple[bool, str]:
        if not username or len(username) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres."
        if len(username) > 30:
            return False, "El nombre de usuario no puede superar los 30 caracteres."
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            return False, "El nombre de usuario solo puede contener letras, números y guiones bajos."
        return True, ""

    @staticmethod
    def is_valid_email(email: str) -> tuple[bool, str]:
        pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            return False, "El correo electrónico no tiene un formato válido."
        return True, ""

    @staticmethod
    def passwords_match(password: str, confirm: str) -> tuple[bool, str]:
        if password != confirm:
            return False, "Las contraseñas no coinciden."
        return True, ""


class PasswordHasher:
    """Clase restaurada para aislar la lógica de encriptación y no romper los tests."""
    @staticmethod
    def hash(plain_password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verify(plain_password: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed.encode('utf-8'))


# ═══════════════════════════════════════════════════════════════
# SECCIÓN 6 ─ RESULTADO DE AUTENTICACIÓN
# ═══════════════════════════════════════════════════════════════

class AuthResult:
    def __init__(self, success: bool, message: str, data: dict | None = None, errors: list | None = None):
        self.success = success
        self.message = message
        self.data    = data or {}
        self.errors  = errors or []

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "message": self.message,
            "data":    self.data,
            "errors":  self.errors,
        }


# ═══════════════════════════════════════════════════════════════
# SECCIÓN 7 ─ SERVICIO DE AUTENTICACIÓN
# ═══════════════════════════════════════════════════════════════

MAX_FAILED_ATTEMPTS = 5

class AuthService:
    def __init__(self, repository: UserRepository, event_bus: AuthEventBus):
        self._repo      = repository
        self._event_bus = event_bus

    def _generate_token(self, user: User) -> str:
        payload = {
            "user_id":  user.user_id,
            "username": user.username,
            "role":     user.role,
            "exp":      datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    def sign_up(self, username: str, email: str, password: str, confirm_password: str, role: str = "member") -> AuthResult:
        errors = []

        ok, msg = InputValidator.is_valid_username(username)
        if not ok:
            errors.append(msg)

        ok, msg = InputValidator.is_valid_email(email)
        if not ok:
            errors.append(msg)

        ok, msg = InputValidator.passwords_match(password, confirm_password)
        if not ok:
            errors.append(msg)

        ok, pwd_errors = PasswordPolicy.validate(password)
        if not ok:
            errors.extend(pwd_errors)

        if errors:
            return AuthResult(False, "Error de validación.", errors=errors)

        if self._repo.find_by_username(username):
            return AuthResult(False, "El nombre de usuario ya está en uso.", errors=["Usuario duplicado."])

        if self._repo.find_by_email(email):
            return AuthResult(False, "El correo ya está registrado.", errors=["Email duplicado."])

        # Usamos nuestro PasswordHasher restaurado
        password_hash = PasswordHasher.hash(password)

        factory = UserFactoryRegistry.get(role)
        user    = factory.build(username, email, password_hash)

        self._repo.save(user)
        self._event_bus.publish(AuthEvent(AuthEvent.USER_REGISTERED, {
            "user_id":  user.user_id,
            "username": user.username,
            "email":    user.email,
            "role":     user.role,
        }))

        token = self._generate_token(user)
        return AuthResult(True, "Usuario registrado correctamente.", data={**user.to_dict(), "token": token})

    def log_in(self, username: str, password: str) -> AuthResult:
        user = self._repo.find_by_username(username)

        if not user:
            self._event_bus.publish(AuthEvent(AuthEvent.LOGIN_FAILED, {"username": username}))
            # FIJATE ACÁ: No hay coma al final, solo el AuthResult
            return AuthResult(False, "Credenciales incorrectas.", errors=["Usuario no encontrado."])

        if not user.is_active:
            return AuthResult(False, "Cuenta bloqueada. Contactá al administrador.", errors=["Cuenta bloqueada."])

        if not PasswordHasher.verify(password, user.password_hash):
            user.failed_attempts += 1
            if user.failed_attempts >= MAX_FAILED_ATTEMPTS:
                user.is_active = False
                self._event_bus.publish(AuthEvent(AuthEvent.ACCOUNT_LOCKED, {"username": username}))
            else:
                self._event_bus.publish(AuthEvent(AuthEvent.LOGIN_FAILED, {"username": username}))
            self._repo.update(user)
            return AuthResult(False, "Credenciales incorrectas.", errors=["Contraseña incorrecta."])

        user.failed_attempts = 0
        self._repo.update(user)

        self._event_bus.publish(AuthEvent(AuthEvent.LOGIN_SUCCESS, {
            "user_id":  user.user_id,
            "username": user.username,
            "role":     user.role,
        }))

        token = self._generate_token(user)
        return AuthResult(True, "Inicio de sesión exitoso.", data={**user.to_dict(), "token": token})


# ═══════════════════════════════════════════════════════════════
# SECCIÓN 8 ─ REPOSITORIO DE RESERVAS Y ESPACIOS
# ═══════════════════════════════════════════════════════════════

class BookingRepository(SupabaseTableRepository):
    """Repositorio para gestionar las reservas en Supabase."""

    TABLE_NAME = "bookings"

    def __init__(self, event_bus: AuthEventBus | None = None, user_repository: UserRepository | None = None, client: Client | None = None):
        super().__init__(client)
        self._event_bus = event_bus
        self._user_repository = user_repository

    @staticmethod
    def _normalize_status(status: str) -> str:
        return (status or "").strip().lower()

    def _resolve_user_email(self, username: str) -> str | None:
        if not username or not self._user_repository:
            return None

        user = self._user_repository.find_by_username(username)
        return user.email if user else None

    def _publish_booking_event(self, event_type: str, payload: dict[str, Any]) -> None:
        if self._event_bus:
            self._event_bus.publish(AuthEvent(event_type, payload))

    @staticmethod
    def _parse_hours_value(time_value: Any) -> float | None:
        text = str(time_value or "").strip().lower()
        if not text or "mensual" in text:
            return None

        try:
            if "," in text:
                parts = [part.strip() for part in text.split(",") if part.strip()]
                if len(parts) > 1:
                    return float(len(parts))

            hour_match = re.search(r"(\d+(?:[\.,]\d+)?)\s*h", text)
            if hour_match:
                return float(hour_match.group(1).replace(",", "."))

            range_match = re.search(r"^(\d{1,2}):(\d{2})\s*[-–]\s*(\d{1,2}):(\d{2})$", text)
            if range_match:
                start = int(range_match.group(1)) * 60 + int(range_match.group(2))
                end = int(range_match.group(3)) * 60 + int(range_match.group(4))
                diff = end - start
                if diff > 0:
                    return diff / 60.0

            numeric = float(text.replace(",", "."))
            return numeric if numeric > 0 else None
        except Exception:
            return 1.0

    @staticmethod
    def _days_ahead_value(date_value: Any) -> float | None:
        if not date_value:
            return None
        try:
            target = datetime.strptime(str(date_value)[:10], "%Y-%m-%d")
            today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            return max(0.0, float((target - today).days))
        except Exception:
            return None

    @staticmethod
    def _pearson_r_from_rows(rows: list[dict]) -> float:
        samples: list[tuple[float, float]] = []
        for row in rows:
            x = BookingRepository._days_ahead_value(row.get("booking_date"))
            y = BookingRepository._parse_hours_value(row.get("booking_time"))
            if x is None or y is None:
                continue
            samples.append((x, y))

        if len(samples) < 3:
            return 0.0

        xs = [item[0] for item in samples]
        ys = [item[1] for item in samples]
        x_mean = sum(xs) / len(xs)
        y_mean = sum(ys) / len(ys)
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in samples)
        denominator_x = sum((x - x_mean) ** 2 for x in xs)
        denominator_y = sum((y - y_mean) ** 2 for y in ys)
        denominator = (denominator_x * denominator_y) ** 0.5
        if denominator == 0:
            return 0.0
        return float(numerator / denominator)

    def _maybe_publish_upgrade(self, booking: dict, correlation_r: float) -> None:
        days_ahead = self._days_ahead_value(booking.get("booking_date"))
        if days_ahead is None or days_ahead < 10 or correlation_r <= 0:
            return

        username = booking.get("username", "")
        user_email = self._resolve_user_email(username)
        if not user_email:
            return

        self._publish_booking_event(AuthEvent.BOOKING_UPGRADE_AVAILABLE, {
            "booking_id": str(booking.get("id", "")),
            "username": username,
            "email": user_email,
            "space_name": booking.get("space_name"),
            "booking_date": booking.get("booking_date"),
            "booking_time": booking.get("booking_time"),
            "days_ahead": int(days_ahead),
            "correlation_r": round(correlation_r, 3),
        })

    def get_all(self) -> list[dict]:
        response = self._table(self.TABLE_NAME).select("*").execute()
        return response.data if response.data else []

    def get_by_id(self, booking_id):
        """Obtiene una reserva por su ID (int o string)."""
        normalized_id = self._coerce_id(booking_id)
        response = self._table(self.TABLE_NAME).select("*").eq("id", normalized_id).execute()
        return self._first_row(response)

    def get_by_username(self, username: str) -> list[dict]:
        response = self._table(self.TABLE_NAME).select("*").eq("username", username).execute()
        return response.data if response.data else []

    def create(self, booking_data: dict) -> dict | None:
        record = dict(booking_data)
        if not record.get("id"):
            record["id"] = self._generate_numeric_id()

        additional_info = record.get("additional_info")
        if isinstance(additional_info, (dict, list)):
            record["additional_info"] = json.dumps(additional_info)

        response = self._table(self.TABLE_NAME).insert(record).execute()
        created = self._first_row(response)
        if not created:
            return None

        correlation_r = self._pearson_r_from_rows(self.get_all())
        self._maybe_publish_upgrade(created, correlation_r)
        return created

    def update_status(self, booking_id: str, new_status: str) -> dict | None:
        """Actualiza el estado de una reserva (Aprobar/Rechazar)."""
        response = self._table(self.TABLE_NAME).update({"status": new_status}).eq("id", self._coerce_id(booking_id)).execute()
        updated = self._first_row(response)
        if not updated:
            return None

        normalized_status = self._normalize_status(new_status)
        username = updated.get("username", "")
        user_email = self._resolve_user_email(username)

        if normalized_status in {"confirmada", "confirmed"}:
            qr_token = QRCodeGenerator.generate_token(updated.get("id"), username)
            qr_bytes = QRCodeGenerator.generate_image(updated.get("id"), username)
            self.update_qr_token(updated.get("id"), qr_token)

            updated["qr_token"] = qr_token
            updated["qr_data_uri"] = QRCodeGenerator.generate_data_uri(updated.get("id"), username)

            self._publish_booking_event(AuthEvent.BOOKING_CONFIRMED, {
                "booking_id": str(updated.get("id", "")),
                "username": username,
                "email": user_email,
                "space_name": updated.get("space_name"),
                "booking_date": updated.get("booking_date"),
                "booking_time": updated.get("booking_time"),
                "qr_token": qr_token,
                "qr_image_bytes": qr_bytes,
            })
        elif normalized_status in {"rechazada", "rechazado", "cancelada", "cancelled"}:
            self._publish_booking_event(AuthEvent.BOOKING_REJECTED, {
                "booking_id": str(updated.get("id", "")),
                "username": username,
                "email": user_email,
                "space_name": updated.get("space_name"),
                "booking_date": updated.get("booking_date"),
                "booking_time": updated.get("booking_time"),
            })

        return updated

    def update_qr_token(self, booking_id: str, qr_token: str) -> dict | None:
        """Guarda el token QR en la reserva confirmada.
        Si la columna 'qr_token' no existe en Supabase, falla silenciosamente
        para no interrumpir el flujo de email y generacion de QR."""
        try:
            response = self._table(self.TABLE_NAME).update({"qr_token": qr_token}).eq("id", self._coerce_id(booking_id)).execute()
            return self._first_row(response)
        except Exception as exc:
            print(f"[BookingRepository] Aviso: no se pudo guardar qr_token (agregar columna en Supabase): {exc}")
            return None

    def update_additional_info(self, booking_id, additional_info: str) -> dict | None:
        """Guarda informacion adicional del cliente. Falla silenciosamente si la columna no existe."""
        try:
            value = json.dumps(additional_info) if isinstance(additional_info, (dict, list)) else additional_info
            response = self._table(self.TABLE_NAME).update({"additional_info": value}).eq("id", self._coerce_id(booking_id)).execute()
            return self._first_row(response)
        except Exception as exc:
            print(f"[BookingRepository] Aviso: no se pudo guardar additional_info: {exc}")
            return None


class SpaceRepository(SupabaseTableRepository):
    """Repositorio para leer y modificar el catálogo de espacios en Supabase."""

    TABLE_NAME = "spaces"

    def get_all(self) -> list[dict]:
        response = self._table(self.TABLE_NAME).select("*").execute()
        return response.data if response.data else []

    def create(self, space_data: dict) -> dict | None:
        """Crea un nuevo espacio en la base de datos."""
        record = dict(space_data)
        if not record.get("id"):
            record["id"] = self._generate_numeric_id()
        response = self._table(self.TABLE_NAME).insert(record).execute()
        return self._first_row(response)

    def update(self, space_id: str, space_data: dict) -> dict | None:
        """Edita un espacio existente."""
        response = self._table(self.TABLE_NAME).update(space_data).eq("id", self._coerce_id(space_id)).execute()
        return self._first_row(response)
