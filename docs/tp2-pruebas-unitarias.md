# Pruebas de Software - SpicyTech Coworking 

## B0. Investigación Previa y Técnicas de Diseño de Pruebas

### 1. Clases de Equivalencia
**¿Qué es y cómo se aplica?**
La partición en clases de equivalencia es una técnica de testing de caja negra que consiste en dividir el dominio de los datos de entrada en diferentes grupos (clases). La premisa es que si un valor de una clase funciona correctamente (o falla), todos los demás valores de esa misma clase se comportarán exactamente igual. Esto permite reducir drásticamente la cantidad de casos de prueba necesarios, eligiendo solo un valor representativo por cada clase válida o inválida.

### 2. Valores Límite
**¿Qué es y cómo se aplica?**
El análisis de valores límite es una técnica complementaria a las clases de equivalencia. Se basa en la observación de que la mayoría de los defectos de software ocurren en los "bordes" de las clases de equivalencia, más que en el centro. Consiste en diseñar casos de prueba que evalúen los extremos exactos (límites permitidos) y los valores inmediatamente fuera de esos límites (justo por encima o justo por debajo).

### 3. Ejemplo Concreto Aplicado a SpicyTech Coworking
**Función bajo prueba:** Validación del rango horario para reservar un espacio.
**Regla de negocio:** El coworking opera estrictamente de 08:00 a 20:00 hs.

*   **Clases de Equivalencia:**
    *   *Clase Válida:* Cualquier hora entre las 08:00 y las 20:00 (ej. valor representativo: 14:00).
    *   *Clase Inválida 1 (Inferior):* Cualquier hora antes de las 08:00 (ej. 03:00).
    *   *Clase Inválida 2 (Superior):* Cualquier hora después de las 20:00 (ej. 22:00).
*   **Valores Límite:**
    *   *Límite Inferior Válido:* 08:00.
    *   *Límite Inferior Inválido:* 07:59.
    *   *Límite Superior Válido:* 20:00.
    *   *Límite Superior Inválido:* 20:01.

## B1. Diseño de Casos de Prueba Unitaria (TDD)

A continuación se detallan los 6 casos de prueba diseñados utilizando partición de equivalencia y análisis de valores límite. Estos casos aseguran la integridad de las reglas de negocio fundamentales de **SpicyTech Coworking** y serán automatizados mediante código por el equipo de desarrollo.

### Función 1: `validar_horario_operativo(hora_solicitada)`
*Regla de negocio:* El coworking solo permite reservas dentro de la franja horaria de 08:00 a 20:00 hs.

*   **Caso de Prueba 1 (CP01)**
    *   **Técnica:** Partición de Equivalencia (Clase Válida).
    *   **Datos de entrada:** `hora_solicitada = "14:00"`
    *   **Resultado esperado:** `True` (El sistema permite continuar con la reserva).

*   **Caso de Prueba 2 (CP02)**
    *   **Técnica:** Valores Límite (Frontera Inferior Inválida).
    *   **Datos de entrada:** `hora_solicitada = "07:59"`
    *   **Resultado esperado:** `False` / Excepción: "Horario fuera del rango operativo".

*   **Caso de Prueba 3 (CP03)**
    *   **Técnica:** Valores Límite (Frontera Superior Válida).
    *   **Datos de entrada:** `hora_solicitada = "20:00"`
    *   **Resultado esperado:** `True` (Es el último minuto válido para estar en el espacio).

---

### Función 2: `validar_logica_tiempo(hora_inicio, hora_fin)`
*Regla de negocio:* Para que un bloque de reserva sea válido, la hora de finalización debe ser estrictamente posterior a la hora de inicio.

*   **Caso de Prueba 4 (CP04)**
    *   **Técnica:** Partición de Equivalencia (Clase Válida).
    *   **Datos de entrada:** `hora_inicio = "10:00"`, `hora_fin = "13:00"`
    *   **Resultado esperado:** `True` (El bloque es lógico y válido).

*   **Caso de Prueba 5 (CP05)**
    *   **Técnica:** Valores Límite (Límite exacto de colisión).
    *   **Datos de entrada:** `hora_inicio = "15:00"`, `hora_fin = "15:00"`
    *   **Resultado esperado:** `False` / Excepción: "La hora de fin no puede ser igual a la hora de inicio".

*   **Caso de Prueba 6 (CP06)**
    *   **Técnica:** Partición de Equivalencia (Clase Inválida - Lógica inversa).
    *   **Datos de entrada:** `hora_inicio = "18:00"`, `hora_fin = "16:00"`
    *   **Resultado esperado:** `False` / Excepción: "La hora de fin debe ser posterior a la hora de inicio".
---

## B2. Framework de pruebas y automatización CI/CD

### Evidencia Audiovisual
A continuación se adjunta el video con la ejecución de las pruebas unitarias en el entorno local:

**[Ver video de ejecución de pruebas - SpicyTech](https://youtu.be/ZY8X9JZbet4)**
---

## B3. Diseño Conceptual de Pruebas de Integración

### 1. Dependencias Externas Identificadas
Para el módulo de reservas y autenticación de nuestro backend (Flask), hemos identificado las siguientes dependencias externas críticas:
1.  **Base de Datos Relacional (SQLite/SQLAlchemy):** Encargada de persistir el estado de los usuarios y las reservas.
2.  **Servicio de Notificaciones (AuthEventBus):** El bus de eventos que enviaría correos electrónicos o alertas al Administrador cuando un miembro solicita una reserva y esta queda en estado "PENDIENTE".

### 2. Estrategia de Mocks y Stubs
Para realizar pruebas de integración rápidas, predecibles y que no afecten los datos de producción, aislaremos estas dependencias:
*   **Stub para la Base de Datos:** En lugar de conectarnos a la base de datos real, configuraremos SQLAlchemy para que utilice una base de datos en memoria (`sqlite:///:memory:`). Este Stub nace vacío al inicio de la prueba y se destruye al finalizar, garantizando un entorno limpio.
*   **Mock para Notificaciones:** Reemplazaremos el objeto real del notificador por un objeto *Mock* simulado. Esto evitará que se envíen correos reales durante las pruebas automatizadas, pero nos permitirá "espiar" si el sistema intentó enviar el mensaje correctamente.

# Pruebas de Software - SpicyTech Coworking

---
# Estrategia de Testing y Calidad — SpicyTech

---

## Stack tecnológico del proyecto

| Capa | Tecnología |
|------|------------|
| Backend | Python + Flask |
| Frontend | Vanilla JS |
| Base de datos | SQLite |

---

## Elección y Justificación de frameworks

### Backend → pytest

Elegimos **pytest** para testear el backend porque todo el proyecto está en Python y pytest es la herramienta más natural para ese ecosistema. Comparado con `unittest` (que también es Python nativo), pytest tiene una sintaxis mucho más limpia: los tests son funciones simples, no clases obligatorias, y los fixtures permiten reutilizar la configuración de objetos como `AuthService` o `InMemoryUserRepository` sin repetir código en cada `setUp()`.

Otra ventaja concreta: cuando un assert falla, pytest muestra exactamente qué valor se esperaba y qué se recibió, con un diff legible. Eso acelera bastante el debug. Y para el CI/CD con GitHub Actions, se integra solo — basta con correr `pytest src/tests.py` y el workflow interpreta el exit code correctamente.

No se consideró ninguna herramienta de otro lenguaje porque no tiene sentido agregar complejidad cuando el stack ya está definido en Python.

### Frontend → Cypress

El frontend de SpicyTech es Vanilla JS puro (sin React ni ningún framework de componentes), así que necesitábamos una herramienta E2E que no requiera adaptadores especiales. **Cypress** funciona directamente sobre el navegador, lo que lo hace ideal para este caso.

El motivo más concreto por el que lo elegimos es el **Time Travel Debugging**: Cypress guarda capturas de cada paso del test y permite reproducirlos visualmente, lo cual es muy útil para depurar flujos como el login con JWT. Además, permite hacer assertions sobre el `localStorage` del navegador, que es exactamente donde SpicyTech guarda el token de sesión. Eso no es algo que todas las herramientas E2E soporten fácilmente.

### Testing de integración → unittest.mock + SQLite en memoria

Para las pruebas de integración no instalamos nada extra: usamos `unittest.mock` (incluido en la librería estándar de Python) para simular el `AuthEventBus` y evitar que los tests manden correos reales, y una base de datos SQLite en memoria (`:memory:`) como stub de la base de datos de producción. Así cada test arranca con un estado limpio sin tocar datos reales.

---

## Tipos de pruebas

| Tipo | Estado | Qué cubre |
|------|--------|-----------|
| Unitarias | ✅ Implementadas | `PasswordPolicy`, `PasswordHasher`, `UserFactory`, `AuthService`, `AuthEventBus` |
| Integración | ✅ Implementadas | Registro y login contra `InMemoryUserRepository` con mocks del bus de eventos |
| Sistema (E2E) | ✅ Implementadas | Flujo completo de login, verificación de JWT en localStorage, rol admin |
| Regresión (CI/CD) | ✅ Activo | GitHub Actions corre `pytest` en cada push a `main` |
| Estrés | 🔜 Planificado | Locust — condición de carrera en reservas simultáneas (Fase 2) |

---

## Casos de prueba unitaria — Motor de Reservas

**Regla de negocio:** el coworking opera de 08:00 a 20:00. La hora de fin debe ser mayor a la de inicio.

| # | Entrada | Resultado esperado |
|---|---------|-------------------|
| 1 (válido) | Inicio: 10:00 / Fin: 12:00 | `True` — reserva permitida |
| 2 (límite inferior) | Inicio: 07:59 / Fin: 09:00 | `False` — fuera del rango operativo |
| 3 (lógica temporal) | Inicio: 15:00 / Fin: 15:00 | `False` — fin no es posterior al inicio |

Implementados en `src/tests.py`.

---

## CI/CD

El workflow `.github/workflows/test.yml` se activa en cada `push` y `pull request` a `main`. Corre `pytest src/tests.py` y bloquea el merge si algún test falla. Los resultados se ven en la pestaña **Actions** de GitHub.

> <img width="1529" height="649" alt="image" src="https://github.com/user-attachments/assets/13b88e39-9992-43cf-8edb-f56c4d514df7" />


