# Informe de Ingeniería de Software II: Estándares, Usabilidad y V&V

##  Cuestionario de Verificación y Validación (V&V) Aplicado a Spicy Tech

### 1. Verificación vs Validación
* **Verificación (*Verificamos si estamos construyendo el producto con el plano y las herramientas correctas*):** Comprobación técnica de que el software responde fielmente a las especificaciones de diseño y requerimientos lógicos sin introducir fallas en el código.
    * *Ejemplo en nuestro proyecto Spicy Tech:* Implementar una prueba unitaria para verificar que la función constructora de tarifas calcule correctamente el valor neto sumando las horas reservadas por el valor base de la sala de coworking, sin bugs de redondeo o desbordamiento de tipos.
* **Validación (*Estamos haciendo el producto correcto para nuestro cliente?*):** Evaluación de si el software en funcionamiento satisface las necesidades reales del negocio y del usuario final dentro de su entorno operativo.
    * *Ejemplo en nuestro proyecto Spicy Tech:* Someter la interfaz del flujo de reservas a un test con un administrador real de un coworking para certificar que la planilla horaria visual le permite organizar el espacio físico de forma fluida y sin confusiones operacionales.

### 2. Planificación de V&V en un Sprint de 1 Semana
Este tipo de planificaciones son una sección estratégica donde se define cómo, cuándo y con qué herramientas el equipo va a asegurar que el sistema se está construyendo bien (Verificación) y que cumple con las necesidades del cliente (Validación) a lo largo del ciclo de vida del proyecto, si tuviéramos que planificar las actividades de V&V para el próximo sprint de desarrollo de **Spicy Tech**, considerando la alta restricción de tiempo (1 semana), nos enfocaríamos concretamente en el **módulo de reservas y asignación de roles**:

1.  **Actividad de Verificación Concreta:** Desarrollar e integrar una suite de pruebas unitarias automatizadas sobre el controlador de la base de datos que maneja la disponibilidad de salas. El objetivo técnico es verificar que cuando un usuario con rol "Cliente" reserve un espacio, el sistema bloquee el registro de manera atómica para impedir colisiones (*race conditions*) si otro usuario intenta clickear el mismo asiento simultáneamente.
2.  **Actividad de Validación Concreta:** Preparar un escenario de prueba interactivo (User Acceptance Testing ágil) del "camino feliz" de una reserva desde la interfaz móvil. Al final de la semana, ejecutaremos una sesión de pruebas con un usuario externo simulando un entorno con conexión inestable para validar si el flujo de selección de escritorio y confirmación de franja horaria resulta intuitivo, veloz y libre de fricciones cognitivas.

### 3. Inspecciones de Software vs Pruebas Automáticas
* **Diferencia Clave:** La **Inspección de código** es un proceso estático y humano (ej. *Code Reviews* a través de *Pull Requests*) enfocado en evaluar la calidad del diseño arquitectónico, legibilidad y mantenibilidad. La **Prueba automática** es un proceso dinámico y computacional donde se ejecuta un fragmento de código aislado con entradas y salidas predefinidas de forma repetitiva.
* **Aplicación en Spicy Tech:**
    * *Cuándo nos conviene una Inspección?:* Al diseñar la estructura de los middlewares de autenticación y los decoradores de **gestión de roles** en la API. Una revisión por pares humana es superior para detectar vulnerabilidades lógicas de seguridad (como saltos de permisos o IDOR) que las pruebas automáticas suelen pasar por alto.
    * *Cuándo nos convienen Pruebas Automáticas?:* Al realizar cambios en los modelos de datos o agregar nuevos tipos de membresías (ej. pase corporativo). Ejecutar tests automáticos nos permite hacer **pruebas de regresión** instantáneas para asegurar que el nuevo código no rompió la lógica de reservas básicas que ya funcionaba bien.

### 4. Análisis Estático Automatizado
* **Herramienta de referencia:** `ESLint` (para el frontend en React) o `Pylint` (si se utiliza Python en el backend).
* **Errores específicos en nuestro proyecto Spicy Tech:** Analiza el código fuente como texto plano sin ejecutar el programa. En nuestro sistema de coworking, esta herramienta detectaría tempranamente si un desarrollador importó un hook de conexión a la pasarela de pagos pero olvidó invocarlo (código muerto), si se dejaron bloques `try/catch` vacíos al intentar conectar con la base de datos (lo que silenciaría errores críticos de servidor), o si se instanció una variable de sesión de usuario que nunca se lee, optimizando la memoria antes del despliegue.

### 5. Métodos Formales de Verificación
* **Imprescindibles en:** Sistemas de misión crítica o vida crítica donde un fallo de software causa catástrofes físicas o financieras humanas (sistemas aeroespaciales, dispositivos médicos autónomos, algoritmos core de compensación bancaria masiva).
* **Por qué no los usamos en Spicy Tech:** Los métodos formales se basan en demostraciones matemáticas lógicas extremadamente complejas para asegurar matemáticamente que un programa está 100% libre de fallas. Para una aplicación comercial de gestión de coworking como Spicy Tech, el costo financiero, la especialización requerida del equipo y el tiempo de desarrollo que demandaría aplicar estos métodos harían inviable el proyecto, superando drásticamente los beneficios comerciales de la plataforma.

### 6. Reuniones de Validación en Frameworks Ágiles (Scrum/XP)
* **Rol del Product Owner (PO) en la Sprint Review:** El PO actúa como el validador supremo del incremento de software. Su función en la demo de Spicy Tech no es evaluar el código, sino juzgar si las funcionalidades de reserva de salas construidas durante la semana cumplen con los criterios de aceptación y si realmente aportan el valor estratégico que el negocio del coworking necesita.
* **Relación con las Pruebas Automatizadas:** Las pruebas automáticas actúan como un filtro higiénico de verificación técnica previa. Al garantizar robóticamente que el servidor de Spicy Tech es estable y que no va a colapsar por bugs básicos en plena presentación, le permiten al PO y a los stakeholders clave enfocar la discusión de la Sprint Review al 100% en la **validación funcional y usabilidad de negocio**, maximizando el valor del feedback recibido.


# SEGUNDA PARTE 

## 7. Plan de Verificación y Validación (V&V) a Escala — Spicy Tech

---

### SECCIÓN 1: Verificación vs Validación

1.  **Verificación actual en el proyecto:** Ejecutamos de manera automatizada una suite de pruebas unitarias(contenedor de pruebas) sobre las funciones controladoras del backend para verificar que el cálculo del precio neto de una reserva de coworking (horas seleccionadas multiplicadas por la tarifa base del espacio) arroje el valor matemático exacto antes de impactar en la base de datos.
2.  **Validación planificada con el Product Owner:** Planificamos realizar una simulación interactiva junto al Product Owner utilizando un entorno de pruebas (*Staging*) recreando una situación de alta demanda simultánea, para validar si la interfaz de usuario de Spicy Tech responde de forma intuitiva, no genera confusión al mostrar los escritorios ocupados y cumple con las expectativas del negocio en tiempo real.

---

### SECCIÓN 2: Planificación de V&V (Cronograma de Sprints)

A continuación detallamos la planificación de actividades de aseguramiento de la calidad para el ciclo actual y el subsiguiente:

| Sprint | Actividad de V&V | Técnica | Responsable | Herramienta |
| :--- | :--- | :--- | :--- | :--- |
| **Actual** | Revisión de la lógica de los middlewares de control de acceso y validación de tokens de sesión. | Inspección estática por pares (*Code Review*) | Backend Developer | GitHub Pull Requests & Checklist OWASP |
| **Próximo** | Evaluación del comportamiento transaccional del módulo de reservas bajo concurrencia masiva simultánea. | Pruebas de estrés y carga automatizadas | QA / Tester Lead | Apache JMeter |

---

### SECCIÓN 3: Inspección y Análisis Estático

* **a) Módulo prioritario para inspección:** Inspeccionaríamos primero el módulo del **Controlador de Autenticación y Gestión de Roles** (`AuthController`). Al ser un sistema comercial basado en roles donde los clientes manejan datos de facturación y los administradores tienen control total de las salas, es el componente más crítico. Un error de lógica humana en los middlewares o decoradores de permisos podría provocar una escalada de privilegios (IDOR), exponiendo datos privados o permitiendo acciones destructivas no autorizadas.
* **b) Herramienta de análisis estático y regla prioritaria:** Utilizaremos **ESLint** (si el stack frontend es React) o **Pylint** (para backend en Python). La primera regla estricta que aplicaríamos es `no-unused-vars` (o `unused-import` en Python). Esta regla bloquea de manera automática cualquier despliegue si detecta que se importó una función, variable de sesión o hook (como el de conexión a la pasarela de pagos externos) pero nunca se invocó en el código ejecutable, evitando subir código "muerto" o incompleto.

---

### SECCIÓN 4: Método Formal Conceptual (Invariantes de Software)

* **a) Descripción del Invariante en Spicy Tech:**
    En la clase o entidad `Reserva`, se establece el siguiente invariante lógico fundamental: *“Para cualquier instancia válida de una reserva, la propiedad `fecha_fin` debe ser estrictamente posterior en el tiempo a la propiedad `fecha_inicio`, y la duración resultante (`fecha_fin - fecha_inicio`) debe ser mayor o igual a la fracción mínima parametrizada (ej. 1 hora).”*
* **b) Estrategia de prueba unitaria para verificar la propiedad:**
    Para probar este invariante de forma automática, escribiríamos un test unitario que intente forzar una violación de la regla. El test instanciará un objeto `Reserva` pasándole por parámetro una `fecha_inicio` fijada a las `10:00 AM` y una `fecha_fin` inválida fijada a las `09:00 AM` (pasado) o a las `10:00 AM` (duración cero). La prueba unitaria verificará (*assert*) que el constructor de la clase o el servicio de validación lance explícitamente una excepción de negocio (ej. `InvalidReservationIntervalException`) y deniegue la creación del objeto, demostrando que el código bloquea los estados inválidos de manera matemática y hermética.

---

### SECCIÓN 5: Reunión de Validación (Simulación Sprint Review)

Para garantizar en la próxima Sprint Review que el incremento del sistema realmente resuelve la problemática de optimización del coworking, le haríamos las siguientes dos preguntas clave al Product Owner:

1.  *“Considerando el flujo actual de reservas que te acabamos de mostrar, ¿consideras que un cliente promedio de nuestro coworking podrá agendar un escritorio común en menos de tres clics desde el celular, mitigando las colas de espera físicas en la recepción?”*
2.  *“Desde la perspectiva operativa del Administrador del lugar, ¿los indicadores visuales del mapa de salas ocupadas/libres que agregamos en este sprint le aportan la claridad necesaria para reorganizar los espacios físicos en el día a día sin requerir planillas de Excel externas?”*
