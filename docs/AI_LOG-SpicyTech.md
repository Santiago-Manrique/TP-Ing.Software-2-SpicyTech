## Entrada 001 — Semana 1

**Fecha:** 19/03/2026
**Herramienta:** Gemini
**Responsable:** Scrum Master — Octavio García
**Eje temático:** Eje 1

**¿Para qué se usó?**
Definir la estructura inicial de gestión del proyecto (Sprint 0), incluyendo la configuración del tablero Kanban, la redacción del Contrato de Proyecto y la elaboración de la Matriz de Riesgos.

**¿Qué generó la IA?**
1. Una lista de 9 tarjetas para el backlog inicial con descripción y responsables.
2. Un borrador del Contrato de Proyecto con 4 secciones (Escenario, Metodología, Roles y Acuerdos).
3. Una tabla de Matriz de Riesgos con 6 ítems específicos para un sistema de coworking.

**¿Qué aceptamos tal cual?**
La justificación técnica de la metodología Scrum y la estructura de la Matriz de Riesgos (columnas de Impacto, Probabilidad y Mitigación).

**¿Qué modificamos y por qué?**
- **Nombre de la empresa:** Cambiamos el nombre sugerido por "SpicyTech" para alinearlo con la identidad definida por el grupo.
- **Roles y Acuerdos:** Completamos los nombres reales de los integrantes y definimos horarios de reunión específicos (Discord/WhatsApp) según la disponibilidad real del equipo.
- **Mitigación de riesgos:** Ajustamos el plan de mitigación del riesgo de "Concurrencia" para enfocarnos específicamente en bloqueos de base de datos, que es el enfoque técnico que discutió el equipo.

**¿Qué descartamos y por qué?**
Decidimos enfocarnos solo en el núcleo de reservas para no exceder el alcance del cuatrimestre y asegurar la calidad de las funcionalidades básicas.

## Entrada 002 — Semana 3

**Fecha:** 02/04/2026
**Herramienta:** Claude
**Responsable:** Dev Lead — Matías Polcowñuk
**Eje temático:** Eje 1

**¿Para qué se usó?**
Para crear el Back End del sistema en general.

**¿Qué generó la IA?**
1. La carpeta api.py, para combinar back end con front end.
2. La carpeta auth.py para autentificar al usuario en el login.
3. La carpeta tests.py pruebas del código.

**¿Qué aceptamos tal cual?**
El código base del Back End.
**¿Qué modificamos y por qué?**
- **Front End:** Vamos a agregarlo para su correcto funcionamiento.
- **Base de Datos:** Fusionarlo con el código.

**¿Qué descartamos y por qué?**
Por el momento el código funciona correctamente, así que no es necesario el descarte de nada.

## Entrada 003 — Semana 3

**Fecha:** 03/04/2026
**Herramienta:** Gemini
**Responsable:** QA Lead — Jesus Emanuel De Olivera
**Eje temático:** Eje 2 / Integración y Pruebas

**¿Para qué se usó?**
Integrar el Front y Back, aplicar seguridad (Bcrypt/JWT) y asegurar que las pruebas (`tests.py`) pasen sin errores.

**¿Qué generó la IA?**
Un backend seguro (`auth.py`, `api.py`), el JS necesario para consumir la API y un entorno 100% compatible con nuestros tests.

**¿Qué aceptamos tal cual?**
La lógica de encriptación (Bcrypt), el manejo de sesiones (JWT) y el formato de respuesta JSON.

**¿Qué modificamos y por qué?**
Bloqueamos los cambios de diseño. Forzamos a la IA a mantener nuestro código HTML/CSS original, inyectando únicamente el JS necesario para conectar ambas partes y no perder nuestro trabajo.

**¿Qué descartamos y por qué?**
Descartamos la interfaz visual que propuso la IA y su idea de validar contraseñas solo en el backend (decidimos mantener nuestra validación visual en tiempo real en el frontend para mejorar la UX).

## Entrada 004 — Semana 3

**Fecha:** 05/04/2026
**Herramienta:** Claude
**Responsable:** Dev Lead — Matías Polcowñuk
**Eje temático:** Eje 1

**¿Para qué se usó?**
Para agregar una base de datos al proyecto.

**¿Qué generó la IA?**
Una base de datos en SQlite que puede usarse desde manera remota al iniciarse.

**¿Qué aceptamos tal cual?**
El cambio en el modulo de BD.

**¿Qué modificamos y por qué?**
Anteriormente era todo local y no se guardaban los nuevos usuarios, si se quiere completar el caso de uso de Login es un paso necesario. Además de agregar el iniciador de la BD.

**¿Qué descartamos y por qué?**
Descartamos "InMemoryUserRepository", porque no funcionaba de manera correcta.

## Entrada 005 — Semana 3

**Fecha:** 06/04/2026
**Herramienta:** Gemini
**Responsable:** UX Dev — Santiago Manrique
**Eje temático:** Eje 1 / Desarrollo Front End

**¿Para qué se usó?**

Maquetar la interfaz principal y armar el index.html pasándole todo el contexto del proyecto a la IA para que no tire fruta.

**¿Qué generó la IA?**

## Entrada 006 — Semana 4

**Fecha:** 18/04/2026

**Herramienta:** Gemini/ISO - International Organization for Standardization

**Responsable:** QA Lead — Santino Calamari

**Eje temático:** Eje 2 / Diseño Orientado a Objetos
**¿Para qué se usó?**

Analizamos nuestro sistema en base a los estándares históricos centrados en la interacción persona‑ordenador(ISO 9241‑11 e ISO 13407) y los tres estándares actuales para sistemas críticos (ISO/IEC 27001, ISA/IEC 62443, ISO 9001)

**¿Qué generó la IA?**

Luego de investigar personalmente usamos la ia para que analice nuestro sistema en conjunto con el fin de obtener una conclusión acerca de que normas se ven reflejadas en nuestro sistema y cuales pulir más.

## Entrada 007 — Semana 4

**Fecha:** 18/04/2026
**Herramienta:** Gemini
**Responsable:** QA Lead — Jesus Emanuel De Olivera
**Eje temático:** Eje 1

**¿Para qué se usó?**
Estructurar el entregable `ANALISIS_ESTANDARES.md` requerido por la cátedra, integrando el análisis propio del equipo sobre normas ISO y completando los requisitos faltantes de la consigna.

**¿Qué generó la IA?**
1. Una tabla comparativa en formato Markdown.
2. La redacción técnica y justificación de dos estándares adicionales (ISO/IEC 25010 de Calidad e ISO/IEC/IEEE 29119 de Testing) para cumplir con el mínimo de 5 normas exigidas por el profesor.
3. Un párrafo de conclusión técnica que vincula el cumplimiento de la norma de seguridad (ISO 27001) con los patrones de diseño implementados en el TP1 (Observer y Factory Method).

**¿Qué aceptamos tal cual?**
El formato de la tabla, la justificación de las dos normas agregadas (25010 y 29119) y la conclusión que enlaza los patrones de diseño con la arquitectura segura, ya que aporta mucho valor técnico para el coloquio.

**¿Qué modificamos y por qué?**
Restringimos la autonomía de la IA proporcionándole un archivo PDF con nuestro propio análisis previo de 3 normas (ISO 9241-11, ISO 13407, ISO 27001). Forzamos a la IA a usar nuestras justificaciones y no inventar contenido nuevo para esos puntos, manteniendo la autoría intelectual del equipo.

**¿Qué descartamos y por qué?**
No fue necesario descartar nada, ya que la salida se configuró para cumplir estrictamente con los puntos solicitados en la rúbrica de la entrega.

## Entrada 008 — Semana 5 

**Fecha:** 25/04/2026  
**Herramienta:** Gemini  
**Responsable:** QA Lead — Jesus Emanuel De Olivera  
**Eje temático:** Gestión de Proyecto / Calidad y Testing  

**¿Para qué se usó?** Definir la estrategia integral de pruebas del sistema Nexo Coworking y redactar el contrato formal de desarrollo para el equipo SpicyTech, asegurando que todos los requisitos técnicos y administrativos de la cátedra se cumplan bajo estándares profesionales.

**¿Qué generó la IA?** 
1. **Estrategia de Testing:** Una planificación completa dividida en niveles (Unitarias, Integración, E2E y Estrés). Se definieron casos de prueba específicos para el motor de reservas, clases de equivalencia para horarios laborales (08:00 a 20:00) y el plan de mocks para aislar la base de datos.  
2. **Stack de Automatización:** Selección justificada de herramientas gratuitas: **pytest** (unitarias), **Cypress** (E2E) y **Locust** (estrés), alineadas con el stack tecnológico del proyecto (Python/Flask/Vanilla JS).  
3. **Contrato de Software:** Un documento formal en Markdown que consolida los roles del equipo (Scrum Master, Dev Leaders, QA, UX), los acuerdos de trabajo (SLA), las reglas de negocio críticas y los admins predefinidos.  

**¿Qué aceptamos tal cual?** El stack tecnológico de pruebas y la justificación técnica de las herramientas, ya que se adaptan perfectamente a nuestra arquitectura actual. También se aceptó la estructura del contrato y la redacción de las cláusulas de seguridad y cumplimiento de estándares ISO.

**¿Qué modificamos y por qué?** Se ajustaron manualmente los parámetros de los casos de prueba unitaria para que reflejen exactamente las reglas de negocio de nuestro coworking (como el margen de error en horarios y la imposibilidad de auto-confirmación de reservas). Se verificó que las contraseñas de los administradores en el contrato coincidieran con los requerimientos de complejidad definidos previamente.

**¿Qué descartamos y por qué?** Se descartaron sugerencias iniciales de usar herramientas de testing pagas o de alta complejidad (como Selenium o JMeter) en favor de opciones más ágiles y modernas como Cypress y Locust, priorizando la facilidad de mantenimiento y la curva de aprendizaje del equipo.

## Entrada 009 — Semana 6

**Fecha:** 01/05/2026
**Herramienta:** Claude
**Responsable:** Dev Lead — Matías Polcowñuk
**Eje temático:** Pruebas Unitarias


¿Para qué se usó? Crear las seis pruebas unitarias en pytest

¿Qué generó la IA? Generó el archivo test_validaciones.py con 6 pruebas unitarias organizadas en dos clases (TestValidarHorarioOperativo y TestValidarLogicaTiempo), cubriendo los 6 casos de prueba especificados. Incluyó además la implementación de las dos funciones validadas (validar_horario_operativo y validar_logica_tiempo) usando el módulo datetime de Python estándar.

¿Qué aceptamos tal cual? Los 6 casos de prueba con sus assertions, el uso de pytest.raises con match= para validar los mensajes de excepción, la estructura en clases por función, y los docstrings con técnica, entrada y resultado esperado.

¿Qué modificamos y por qué? Nada.

## Entrada 010 — Semana 7

**Fecha:** 05/05/2026
**Herramienta:** Figma (AI Design / HTML to Design)
**Responsable:** UX Dev — Santiago Manrique
**Eje temático:** Eje 1 / Desarrollo Front End y UI/UX

**¿Para qué se usó?**
Adaptar los archivos HTML maquetados a un entorno de Figma para asegurar que el sitio sea responsivo y generar un enlace de prototipo interactivo para el archivo `docs/tp2-ui-ux.md`.

**¿Qué generó la IA?**
1. Conversión de código HTML/CSS a capas de diseño en Figma con *Auto Layout*.
2. Adaptaciones del layout para resoluciones Mobile, Tablet y Desktop.
3. Creación de un enlace de visualización e interacción para el prototipo.

**¿Qué aceptamos tal cual?**
La estructura de los componentes en los diferentes marcos responsivos y la fidelidad visual respecto al código original.

**¿Qué modificamos y por qué?**
- **Interacciones:** Ajustamos manualmente el flujo de navegación entre pantallas para que coincida con la lógica de negocio del coworking.
- **Breakpoints:** Refinamos márgenes en la versión mobile para evitar superposición de elementos en el menú.

**¿Qué descartamos y por qué?**
Descartamos la iconografía sugerida por la IA, manteniendo nuestros SVG originales para asegurar la consistencia con el desarrollo previo.

## Entrada 011 — Semana 7
Fecha: 06/05/2026

Herramienta: Gemini

Responsable: Scrum Master — Octavio García

Eje temático: Gestión de Proyecto / Documentación Final TP2

¿Para qué se usó?
Consolidar toda la información técnica producida por los diferentes roles del equipo (Jesus, Matías y Manrique) en un informe final coherente. Se utilizó específicamente para estructurar el archivo docs/tp2-ui-ux.md y para definir el esqueleto del informe PDF que se sube al aula virtual, asegurando que ningún punto de la consigna (ISO, TDD, CI/CD) quedara fuera.

¿Qué generó la IA?

Estructura del Informe: Un índice detallado alineado con las consignas del TP2, organizando la Parte A (UI/UX) y la Parte B (Testing) de forma profesional.

Sección de Auditoría ISO 9241-11: Redacción técnica de las métricas de eficacia y eficiencia basadas en las simulaciones realizadas sobre el prototipo de Figma.

Justificación ISO 13407: Un párrafo argumentativo que vincula nuestro proceso de diseño iterativo con el estándar internacional de diseño centrado en el usuario.

Guía de Solución de Entorno: Un borrador de los pasos de instalación de dependencias, adaptado a los problemas de compatibilidad detectados durante la semana.

¿Qué aceptamos tal cual?

La tabla de auditoría de usabilidad, ya que los criterios de "Tasa de éxito" (Eficacia) y "Tiempo en tarea" (Eficiencia) son los estándares que mejor se adaptan a nuestro sistema de reservas.

La estructura jerárquica para el archivo tp2-ui-ux.md.

¿Qué modificamos y por qué?

Configuración del Entorno: Forzamos la redacción para especificar el uso de Python 3.13 y el comando py -3.13. La IA sugería inicialmente versiones genéricas, pero debido a los errores de "Build Tools" detectados en la práctica, ajustamos la documentación para que sea una guía de instalación infalible para el equipo y los evaluadores.

Contexto de Usuario: Refinamos la descripción de los usuarios objetivo (Sección A2) para que coincida exactamente con el alcance de SpicyTech, eliminando generalidades sobre otros tipos de sistemas.

¿Qué descartamos y por qué?

Descartamos una propuesta de la IA para incluir métricas de "Satisfacción" mediante encuestas de escala Likert, ya que en esta fase de prototipo no contamos con usuarios reales suficientes para que el dato sea estadísticamente válido; decidimos priorizar Eficacia y Eficiencia que son medibles mediante observación técnica.

## Entrada 012 — Semana 7

**Fecha:** 06/05/2026
**Herramienta:** Claude
**Responsable:** Dev Lead / QA — Calamari Santino
**Eje temático:** Eje 2 / Pruebas Unitarias y CI/CD

**¿Para qué se usó?**
Redactar la justificación técnica de los frameworks de testing en `docs/tp2-pruebas-unitarias.md`, configurar el pipeline de CI/CD en `.github/workflows/test.yml` para automatizar la ejecución de los tests unitarios en cada push y pull request a main, y preparar el guión y estructura del video de evidencia.

**¿Qué generó la IA?**
1. **Justificación de frameworks:** Redacción de la elección de pytest (backend), Cypress (frontend E2E) y unittest.mock + SQLite en memoria (integración), con argumentos técnicos concretos aplicados al stack real del proyecto (Python/Flask/Vanilla JS).
2. **Archivo `test.yml`:** Configuración completa del workflow de GitHub Actions con los pasos de checkout, setup de Python 3.11, instalación de dependencias (pytest, bcrypt, PyJWT, flask, flask-sqlalchemy, supabase) y ejecución de `pytest tests/unit/tests.py -v`.
3. **Documentación técnica:** Contenido del archivo `tests/unit/test.md` explicando cada clase de prueba, sus dependencias y las decisiones de diseño del módulo de tests.
4. **Guión del video:** Estructura y texto para el video de evidencia de 2-3 minutos mostrando los tests corriendo en verde en la terminal y el pipeline exitoso en GitHub Actions.

**¿Qué aceptamos tal cual?**
La justificación de los tres frameworks y su relación con el stack tecnológico del proyecto. El archivo `test.yml` final (luego de resolver los errores de dependencias). La documentación técnica de `test.md`.

**¿Qué modificamos y por qué?**
- **Dependencias del workflow:** El `test.yml` requirió múltiples iteraciones para identificar todos los módulos necesarios (`bcrypt`, `PyJWT`, `supabase`), ya que el proyecto no tiene `requirements.txt`. Cada error del runner de GitHub Actions fue analizado y corregido manualmente hasta lograr el workflow verde.
- **Guión del video:** Adaptamos el guión sugerido agregando las indicaciones exactas de qué mostrar en pantalla y qué comandos ejecutar en cada momento, para que la evidencia cubra todos los requisitos de la consigna.

**¿Qué descartamos y por qué?**
Descartamos la sugerencia de usar `supabase-py` como nombre del paquete pip, ya que no existe en el índice de PyPI. El nombre correcto es `supabase` y fue verificado empíricamente en el runner de GitHub Actions.

