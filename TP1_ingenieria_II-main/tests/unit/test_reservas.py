"""
Pruebas unitarias — Validaciones de horario
Coworking Auth System
=====================
Cubre 6 casos de prueba sobre dos funciones de negocio:
  - validar_horario_operativo(hora_solicitada)
  - validar_logica_tiempo(hora_inicio, hora_fin)
"""

import pytest
from datetime import time


# ══════════════════════════════════════════════════════════════
# IMPLEMENTACIÓN DE LAS FUNCIONES
# (Si ya las tenés en tu código, importalas desde tu módulo
#  y borrá esta sección)
# ══════════════════════════════════════════════════════════════

HORA_APERTURA = time(8, 0)   # 08:00
HORA_CIERRE   = time(20, 0)  # 20:00


def validar_horario_operativo(hora_solicitada: str) -> bool:
    """
    Valida que la hora esté dentro de la franja operativa (08:00–20:00).
    Retorna True si es válida, lanza ValueError si está fuera de rango.
    """
    hora = time.fromisoformat(hora_solicitada)
    if hora < HORA_APERTURA or hora > HORA_CIERRE:
        raise ValueError("Horario fuera del rango operativo")
    return True


def validar_logica_tiempo(hora_inicio: str, hora_fin: str) -> bool:
    """
    Valida que hora_fin sea estrictamente posterior a hora_inicio.
    Retorna True si es válida, lanza ValueError si no lo es.
    """
    inicio = time.fromisoformat(hora_inicio)
    fin    = time.fromisoformat(hora_fin)

    if fin == inicio:
        raise ValueError("La hora de fin no puede ser igual a la hora de inicio")
    if fin < inicio:
        raise ValueError("La hora de fin debe ser posterior a la hora de inicio")
    return True


# ══════════════════════════════════════════════════════════════
# PRUEBAS UNITARIAS
# ══════════════════════════════════════════════════════════════

class TestValidarHorarioOperativo:
    """Función 1: validar_horario_operativo(hora_solicitada)"""

    def test_CP01_particion_equivalencia_clase_valida(self):
        """
        CP01 — Partición de Equivalencia (Clase Válida)
        Entrada:  hora_solicitada = "14:00"
        Esperado: True
        """
        resultado = validar_horario_operativo("14:00")
        assert resultado is True

    def test_CP02_valor_limite_frontera_inferior_invalida(self):
        """
        CP02 — Valores Límite (Frontera Inferior Inválida)
        Entrada:  hora_solicitada = "07:59"
        Esperado: ValueError — "Horario fuera del rango operativo"
        """
        with pytest.raises(ValueError, match="Horario fuera del rango operativo"):
            validar_horario_operativo("07:59")

    def test_CP03_valor_limite_frontera_superior_valida(self):
        """
        CP03 — Valores Límite (Frontera Superior Válida)
        Entrada:  hora_solicitada = "20:00"
        Esperado: True (último minuto válido)
        """
        resultado = validar_horario_operativo("20:00")
        assert resultado is True


class TestValidarLogicaTiempo:
    """Función 2: validar_logica_tiempo(hora_inicio, hora_fin)"""

    def test_CP04_particion_equivalencia_clase_valida(self):
        """
        CP04 — Partición de Equivalencia (Clase Válida)
        Entrada:  hora_inicio = "10:00", hora_fin = "13:00"
        Esperado: True
        """
        resultado = validar_logica_tiempo("10:00", "13:00")
        assert resultado is True

    def test_CP05_valor_limite_colision_exacta(self):
        """
        CP05 — Valores Límite (Límite exacto de colisión)
        Entrada:  hora_inicio = "15:00", hora_fin = "15:00"
        Esperado: ValueError — "La hora de fin no puede ser igual a la hora de inicio"
        """
        with pytest.raises(ValueError, match="La hora de fin no puede ser igual a la hora de inicio"):
            validar_logica_tiempo("15:00", "15:00")

    def test_CP06_particion_equivalencia_logica_inversa(self):
        """
        CP06 — Partición de Equivalencia (Clase Inválida - Lógica inversa)
        Entrada:  hora_inicio = "18:00", hora_fin = "16:00"
        Esperado: ValueError — "La hora de fin debe ser posterior a la hora de inicio"
        """
        with pytest.raises(ValueError, match="La hora de fin debe ser posterior a la hora de inicio"):
            validar_logica_tiempo("18:00", "16:00")
