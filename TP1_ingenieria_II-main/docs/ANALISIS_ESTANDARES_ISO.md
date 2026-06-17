# Análisis de Estándares ISO - SpicyTech 

Este documento analiza los estándares de ingeniería de software y su aplicabilidad al sistema de gestión de reservas del proyecto Spicy Coworking, evaluando su impacto en la arquitectura y el diseño.

## 1. Tabla Comparativa de Estándares

| Estándar | Año (aprox) | Enfoque principal | ¿Aplica a mi proyecto? | Justificación |
| :--- | :--- | :--- | :---: | :--- |
| **ISO 9241-11** | 1998 (2018) | Usabilidad (Eficacia, eficiencia y satisfacción)  | **Sí** | Es innegociable; si el cliente tiene que hacer muchos clics o lidiar con un calendario confuso, abandonará la plataforma. La usabilidad actúa como capa de seguridad, priorizando que el usuario logre el objetivo con precisión absoluta antes que la estética. |
| **ISO 13407** | 1999 (2010) | Proceso de diseño centrado en el humano  | **Sí** | El software se construye desde el usuario hacia abajo, resolviendo los problemas reales de cada perfil (administrador en PC, cliente en celular). Diseñar pensando en el entorno de uso evita saturar a un operador bajo estrés y previene errores. |
| **ISO/IEC 27001** | 2005 (2022) | Seguridad de la información  | **Sí** | Garantiza la confidencialidad, integridad y disponibilidad. Es vital porque el sistema maneja datos sensibles de clientes y pagos; una inyección SQL o caída del servicio implicaría demandas legales y pérdida de confianza. Exige arquitecturas de alta disponibilidad (99.99% uptime). |
| **ISO/IEC 25010** | 2011 (2023) | Calidad del Producto de Software | **Sí** | Evalúa características técnicas como la mantenibilidad, portabilidad y el rendimiento. Aplica directamente a nuestra necesidad de tener una API REST (Flask) que responda rápido a las reservas concurrentes y un código fácil de mantener para futuros Sprints. |
| **ISO/IEC/IEEE 29119** | 2013 | Pruebas de Software (Testing) | **Sí** | Estandariza los procesos de validación y verificación. Para asegurar la calidad (QA), aplicar esta norma nos obliga a mantener y ejecutar pruebas automatizadas rigurosas antes de desplegar código, previniendo regresiones en la lógica de turnos. |

## 2. Conclusión y Relación con la Arquitectura (TP1)

Si tuviéramos que certificar nuestro sistema hoy, elegiríamos **ISO/IEC 27001 (Seguridad de la Información)** por el nivel crítico de los datos personales y bancarios que gestionamos. Cumplir con esto nos obligaría a robustecer nuestra arquitectura actual añadiendo capas de encriptación en reposo y rotación automatizada de tokens JWT. Afortunadamente, nuestras decisiones de diseño del TP1 facilitan este camino: 

## 3. Estándares relevantes para SpicyTech: 

ISO 9241-11: Usabilidad
Para nuestro proyecto resulta muy relevante ya que para un sistema de coworking, nuestro producto compite directamente por la comodidad, si un cliente entra a nuestro sistema y tiene que hacer 10 clics para reservar una sala, lidiar con un calendario confuso (cosa que refleja una baja eficiencia) o el sistema le reserva un horario equivocado por un diseño poco intuitivo (otra vez baja eficacia), el usuario simplemente dejará ir nuestra propuesta, la usabilidad acá define el éxito comercial del sistema.

ISO 13407: Proceso de diseño centrado en el humano

Esta norma dicta que el software no debe construirse sólo desde la base de datos o el código hacia arriba, por ende es muy importante para la etapa en la que estamos ya que nuestro sistema tiene distintos actores: el administrador del lugar, el recepcionista y el cliente final, no podemos diseñar la misma interfaz ni los mismos flujos de datos para el administrador (que necesita ver reportes y facturación en la PC) que para el cliente (que necesita reservar rápido desde su celular mientras va en el colectivo). Aplicar este concepto asegura que el sistema resuelva los problemas reales de cada perfil.

 ISO/IEC 27001: Seguridad de la información
Es una norma de seguridad de la información. Especifica los requisitos para establecer, implementar, mantener y mejorar continuamente un sistema de gestión de la seguridad de la información (SGSI).
Esta norma establece que para proteger los datos se tiene que cumplir con: 
Confidencialidad: Que solo acceda quien debe acceder.
Integridad: Que los datos no se modifiquen de forma no autorizada.
Disponibilidad: Que el sistema esté arriba cuando se lo necesite.
Nuestro sistema va a manejar información muy sensible como son los datos personales de los clientes, contraseñas, correos, y fundamentalmente, datos de pagos, facturación o tarjetas de crédito para cobrar las horas del coworking, si tenemos una vulnerabilidad en nuestra arquitectura (ej. una inyección SQL o una API mal protegida) y se filtran esos datos, nuestro servicio se enfrenta a demandas legales gravísimas y la pérdida total de confianza de parte del cliente.

## 4.¿Qué estándares debería cumplir obligatoriamente y por qué?
Si nuestro sistema se declara crítico este debe cumplir si o si con estos estándares:

ISO/IEC 27001 (Seguridad de la Información): En sistemas críticos, un fallo de seguridad no solo genera pérdidas económicas, sino catástrofe en:
La Integridad: En la gestión de fondos bancarios o historiales clínicos, alterar un número por error tiene consecuencias devastadoras, los datos deben ser inmutables y estar cifrados.
La Disponibilidad: Si nuestro sistema el cual consiste en turnos y transito de clientes no puede "caerse por mantenimiento" ni sufrir ataques de denegación de servicio, requiere arquitecturas redundantes con una Alta Disponibilidad que garantice un uptime del 99.99%.
 ISO 9241-11 y ISO 13407 (Usabilidad y Diseño Centrado en el Humano) - 
Obligatorio como capa de seguridad,aunque parezca que es  "solo diseño visual", en sistemas críticos la usabilidad salva sistemas.
Si el sistema tiene una alta carga cognitiva (es confuso, los botones críticos están escondidos, las alertas visuales no son claras), se produce el error humano. Un diseño centrado en el usuario aquí no busca vender más, sino evitar que el operador presione el botón equivocado en el peor momento posible.
Para nuestro sistema coworking aunque estas normas ya sean algo viejas para sistemas de última generación, estos dos pilares son innegociables:
Contexto de Uso (ISO 13407): Diseñar pensando en el entorno del usuario, un operador bajo estrés necesita interfaces que no lo saturen para evitar errores fatales.
Eficacia antes que Estética (ISO 9241-11): En sistemas críticos, la prioridad no es que sea "lindo", sino que el usuario logre el objetivo con precisión absoluta, con esto la usabilidad es, en realidad, una capa más de seguridad.




## 5. Conclusión y Relación con la Arquitectura

El patrón **Observer** implementado en la autenticación nos permite agregar un `DatabaseObserver` para registrar logs de auditoría inmutables (vitales para la ISO 27001) cada vez que alguien inicia sesión, sin acoplar ni alterar el flujo principal de seguridad; mientras que el patrón **Factory Method** centraliza y blinda la creación de roles, mitigando riesgos de escalamiento de privilegios de manera estandarizada.


 
