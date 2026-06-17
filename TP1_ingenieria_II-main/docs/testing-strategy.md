# Estrategia de Testing y Calidad

**Proyecto:** SpicyTech Coworking 


---

## 1. Tipos de pruebas seleccionadas
| Tipo de prueba | ¿Aplica en este proyecto? | Justificación |
| :--- | :---: | :--- |
| Unitarias | ✅ | Verificar lógica de validación de contraseñas, cálculo de rangos horarios permitidos (08:00 a 20:00) y que la hora de fin sea mayor a la de inicio. |
| Integración | ✅ | Comprobar que el `AuthService` guarda correctamente el usuario en la base de datos (SQLite) y dispara los eventos (`AuthEventBus`) sin enviar correos reales. |
| Componentes | ✅ (futuro) | Probar el Dashboard del Administrador de forma aislada para asegurar que solo lista reservas en estado `PENDIENTE`. |
| Sistema (E2E) | ✅ | Validar el flujo completo: el usuario inicia sesión, solicita una sala, y luego el Administrador entra y se la confirma. |
| Regresión | ✅ | Se automatizará con GitHub Actions (CI/CD) para evitar que un código nuevo rompa el sistema de login o las validaciones de turnos. |
| Estrés | 🔜 Planificado | Se simulará concurrencia extrema (condición de carrera) cuando tengamos el motor de reservas completo para probar los bloqueos de base de datos. |

---

## 2. Herramientas gratuitas elegidas (stack de automatización)

| Nivel de prueba | Herramienta | ¿Qué automatiza en este proyecto? | Justificación |
| :--- | :--- | :--- | :--- |
| Unitarias | **pytest** | Validaciones de negocio (`PasswordPolicy`, `InputValidator`, control de horarios). | Sintaxis limpia, uso de fixtures muy potentes y compatibilidad 100% nativa con nuestro backend en Python/Flask. |
| Integración | **unittest.mock + SQLite (en memoria)** | Simulación de la base de datos y aislamiento del `AuthEventBus` (notificaciones). | Viene incluida en la librería estándar de Python. Aisla el código a la perfección sin instalar dependencias extra. |
| Sistema / E2E | **Cypress** | Flujo de login, navegación del catálogo público y uso del Dashboard Admin. | Excelente interfaz visual "Time Travel" ideal para debuggear nuestro frontend en Vanilla JS y verificar el almacenamiento del JWT en LocalStorage. |
| Estrés | **Locust** | Pruebas de carga sobre el endpoint de reservas simulando colisiones de turnos. | Se escribe en Python (curva de aprendizaje nula para el equipo), tiene interfaz web amigable y bajo consumo de CPU. |

---

## 3. Ejemplos de casos de prueba unitaria (clases de equivalencia y valores límite)

> **Funcionalidad elegida:** Motor de Reservas (Validación de disponibilidad horaria).
> *Regla de negocio:* El coworking opera de 08:00 a 20:00 hs. Las reservas deben hacerse dentro de este rango y la hora de fin debe ser estrictamente posterior a la de inicio.

### Clases de equivalencia identificadas
- **Válidas:** Horarios entre las 08:00 y las 20:00, donde Inicio < Fin.
- **Inválidas (por debajo/fuera de rango):** Horarios antes de las 08:00 (ej. madrugada).
- **Inválidas (por encima/fuera de rango):** Horarios después de las 20:00 (ej. noche) o donde Inicio >= Fin.

### Tres casos de prueba representativos
1. **Caso 1 (válido - dentro del rango):** Entrada = `Inicio: 10:00, Fin: 12:00`, Resultado esperado = `True` (Reserva permitida).
2. **Caso 2 (inválido – límite inferior):** Entrada = `Inicio: 07:59, Fin: 09:00`, Resultado esperado = `False` (Excepción: "Horario fuera del rango operativo").
3. **Caso 3 (inválido – lógica temporal):** Entrada = `Inicio: 15:00, Fin: 15:00`, Resultado esperado = `False` (Excepción: "La hora de fin debe ser posterior a la hora de inicio").

*Nota: estos casos están implementados (o se implementarán) en `src/tests.py`*

---

## 4. Plan de mocks / stubs para pruebas de integración

- **Dependencias externas a simular:**
  1. Base de datos real de producción (usaremos un Stub en memoria).
  2. Módulo de Notificaciones / `AuthEventBus` (usaremos un Mock para no mandar correos reales).
- **Estrategia de dobles:**
  - Usaremos `unittest.mock` (Mock) para el bus de eventos y `sqlite:///:memory:` (Stub) para la persistencia efímera.
  - Ejemplo de prueba de integración (Flujo de reserva):
    - *Flujo:* Usuario solicita reserva → se guarda en DB en memoria → se intercepta el evento de notificación → el sistema retorna estado "PENDIENTE".
    - *Pseudocódigo:* `db_stub = crear_bd_en_memoria()`. `mock_event_bus.subscribe()`. Al llamar a `reservar_espacio()`, verificamos que la BD temporal tiene 1 reserva nueva y llamamos a `mock_event_bus.assert_called_once()` para confirmar que se intentó avisar al administrador, aislando la prueba del servidor de correos.
- **Ubicación en el repo:** `src/tests.py` (Sección: Pruebas de Integración).

---

## 5. Pruebas de sistema (E2E) – flujo básico actual

**Flujo: “Login exitoso y visualización de contraseña”**
1. Abrir la URL de la aplicación (`index.html`).
2. Localizar el campo de usuario e ingresar `JesusDO` (Cuenta predefinida Admin).
3. Localizar el campo de contraseña e ingresar la clave correspondiente.
4. Hacer clic en el ícono "Ojo" (👁️) y **Validar** que la contraseña se vuelve visible (type="text").
5. Hacer clic en “Iniciar sesión”.
6. **Validar** que el sistema muestra la pantalla de éxito, se guarda el JWT en el LocalStorage y se reconoce el rol "admin".

*Script E2E implementado en: `tests/e2e/login.spec.js` (con Cypress)*

**Futuros flujos** (a medida que avance el desarrollo):
- **Visualización pública:** Un visitante sin sesión puede ver el catálogo de espacios (GET público).
- **Solicitud de turno:** Un miembro intenta reservar → su solicitud queda `PENDIENTE`.
- **Aprobación Admin:** El Administrador ingresa al Dashboard → confirma la reserva → las reservas superpuestas de otros usuarios pasan a `RECHAZADA`.

---

## 6. Estrategia de regresión automatizada (CI/CD)

- **Herramienta de CI/CD:** GitHub Actions (gratuito en repositorios públicos).
- **Workflow:** `.github/workflows/test.yml`
- **Activación:** Se ejecuta en cada `push` y `pull request` hacia la rama `main`.
- **Qué pruebas ejecuta actualmente:**
  - Pruebas unitarias de Python (`pytest src/tests.py`).
  - Linter básico para revisar sintaxis y calidad de código.
- **Reporting:** Los resultados se muestran en la pestaña Actions de GitHub. Bloquea el merge si alguna prueba falla (ej. si alguien rompe la validación JWT accidentalmente).

A medida que el proyecto crezca, se irán agregando las pruebas de integración con la base de datos SQL y las pruebas E2E con Cypress al pipeline.

---

## 7. Pruebas de estrés – planificación futura

- **Herramienta elegida:** **Locust**.
- **Escenario de carga extrema propuesto (Condición de Carrera):** Simularemos 100 usuarios (hilos) enviando una solicitud HTTP POST exactamente en el mismo milisegundo para reservar la "Sala de Reuniones A" el día "15/05/2026 a las 10:00 hs". Validaremos que el sistema maneje el cuello de botella guardando las solicitudes como `PENDIENTE` sin corromper la base de datos.
- **Estado actual:** Definido a nivel arquitectónico; a la espera de la construcción del endpoint de reservas (`/api/reservas`).
- **Hito de implementación:** Fase 2 (mes 6), cuando el backend y el Dashboard de Administrador estén conectados a la base de datos real.

---
