# Documentación Técnica de Tests — SpicyTech Coworking

**Archivo:** `tests/unit/tests.py`  
**Framework:** pytest (corre tests de `unittest.TestCase`)  
**Módulo testeado:** `src/auth.py`

---

## Módulo bajo prueba

`auth.py` implementa el sistema de autenticación del backend Flask. Contiene dos patrones de diseño principales:

- **Factory Method** → `UserFactoryRegistry` crea usuarios según su rol (`member`, `admin`, `guest`).
- **Observer** → `AuthEventBus` publica eventos de autenticación a los observadores suscritos (`ConsoleLogger`, `DatabaseObserver`, `EmailNotifier`).

También incluye `AuthService` (lógica de registro y login), `PasswordHasher` (bcrypt), `PasswordPolicy` (reglas de contraseña segura) e `InMemoryUserRepository` (repositorio en memoria usado como stub en los tests).

---

## Clases de prueba

### `TestUserFactory`

Testea el patrón **Factory Method** implementado en `UserFactoryRegistry`.

| Test | Qué verifica |
|------|-------------|
| `test_member_creation` | Que `UserFactoryRegistry.get("member")` retorna una factory que construye un usuario con `role = "member"` y el email correcto. |
| `test_invalid_type_raises` | Que solicitar un rol inexistente (`"alien"`) lanza un `ValueError`. |

**Por qué son importantes:** Garantizan que el sistema de roles funciona correctamente. Si `UserFactoryRegistry` crea un usuario con el rol equivocado, un miembro podría tener permisos de admin.

---

### `TestAuthServiceSignUp`

Testea el flujo de **registro de usuarios** en `AuthService.sign_up()`.  
Usa `InMemoryUserRepository` como stub de la base de datos y `AuthEventBus` real.

| Test | Qué verifica |
|------|-------------|
| `test_duplicate_username_fails` | Que registrar dos usuarios con el mismo username retorna `success = False` con el error `"Usuario duplicado"`. |
| `test_passwords_do_not_match` | Que si `password` y `confirm_password` no coinciden, el registro falla con un mensaje de error de validación. |

**Por qué son importantes:** `sign_up()` tiene múltiples validaciones encadenadas (username, email, contraseñas, política de seguridad). Estos tests verifican que las validaciones de negocio bloquean correctamente los registros inválidos antes de tocar la base de datos.

---

### `TestObserverPattern`

Testea el patrón **Observer** implementado en `AuthEventBus`.

| Test | Qué verifica |
|------|-------------|
| `test_event_bus_publishes_events` | Que al publicar un evento `USER_REGISTERED`, el observador suscripto lo recibe exactamente una vez y con el tipo de evento correcto. |

**Por qué es importante:** El bus de eventos notifica al `DatabaseObserver` (que persiste en Supabase) y al `EmailNotifier` en producción. Si el bus no publica correctamente, los eventos de autenticación se pierden silenciosamente.

---

## Dependencias de los tests

| Dependencia | Uso |
|-------------|-----|
| `pytest` | Framework de ejecución de tests |
| `bcrypt` | Usado por `PasswordHasher` para hashear contraseñas |
| `PyJWT` | Usado por `AuthService._generate_token()` para generar tokens JWT |
| `flask` + `flask-sqlalchemy` | Importados por `auth.py` como dependencias del backend |
| `supabase` | Importado por `auth.py` para la conexión al repositorio en la nube |
| `InMemoryUserRepository` | Stub interno — reemplaza Supabase durante los tests para no tocar datos reales |

---

## Cómo correr los tests

Desde la raíz del proyecto:

    pytest tests/unit/tests.py -v

Resultado esperado:

    tests/unit/tests.py::TestUserFactory::test_invalid_type_raises            PASSED
    tests/unit/tests.py::TestUserFactory::test_member_creation                PASSED
    tests/unit/tests.py::TestAuthServiceSignUp::test_duplicate_username_fails PASSED
    tests/unit/tests.py::TestAuthServiceSignUp::test_passwords_do_not_match   PASSED
    tests/unit/tests.py::TestObserverPattern::test_event_bus_publishes_events PASSED

    5 passed in X.XXs

---

## Decisiones de diseño

**¿Por qué `InMemoryUserRepository` y no Supabase?**  
Usar la base de datos real en los tests unitarios los haría lentos, dependientes de conexión a internet y no reproducibles. El `InMemoryUserRepository` ya está implementado en `auth.py` exactamente para esto — es un stub oficial del proyecto.

**¿Por qué no se testea `log_in()`?**  
Testear `log_in()` de forma aislada es el siguiente paso planificado. Los tests de `sign_up()` cubren indirectamente el hashing y la lógica de validación.

**¿Por qué se usa `unittest.TestCase` con pytest?**  
Los tests están escritos con `unittest.TestCase` pero pytest los descubre y ejecuta sin problema. Esto permite usar `assertFalse`, `assertEqual`, `assertRaises` y demás métodos nativos de unittest mientras se aprovecha la salida visual y el reporte de pytest.

## Video evidencia de los test 

link yt: https://www.youtube.com/watch?v=ZY8X9JZbet4

