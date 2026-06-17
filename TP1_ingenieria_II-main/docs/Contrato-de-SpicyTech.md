# Contrato de Desarrollo de Software: Proyecto SpicyTech Coworking

**Entre:** La Cátedra de Ingeniería de Software II (UCP)  
**Y:** El Equipo de Desarrollo "SpicyTech"  
**Fecha de vigencia:** Ciclo Lectivo 2026

---

## 1. Declaración del Proyecto y Objetivos
El presente contrato rige el desarrollo del sistema **SpicyTech Coworking**, una solución integral para la gestión de reservas de espacios físicos. El objetivo primordial es resolver la problemática actual de conflictos de disponibilidad y falta de visibilidad en tiempo real mediante una plataforma centralizada que gestione escritorios, salas de reuniones y oficinas de manera automatizada.

## 2. Marco Metodológico (Scrum)
El equipo se compromete a la implementación rigurosa del marco de trabajo **Scrum** bajo un enfoque iterativo e incremental:
* **Ciclos de trabajo:** El sistema se dividirá en Sprints para asegurar la validación temprana de funcionalidades críticas.
* **Trazabilidad:** Se mantendrá un tablero Kanban actualizado y control de versiones mediante un repositorio en GitHub.
* **Inspección y Adaptación:** Se realizarán ceremonias para ajustar el alcance del Producto Mínimo Viable (MVP) según el progreso del equipo.

## 3. Estructura Organizacional y Roles
Se establecen las siguientes responsabilidades de liderazgo dentro del equipo **SpicyTech**:

* **Scrum Master:** Octavio García. Responsable de eliminar impedimentos y asegurar el cumplimiento de la metodología.
* **Dev Leaders:** Matias Polcowñuk y Santino Calamari. Responsables de la arquitectura técnica y la integridad del código fuente.
* **QA Leads:** Jesus Emanuel De Olivera y Santino Calamari. Responsables de asegurar la calidad del producto y la ejecución de planes de prueba.
* **UX Lead:** Santiago Manrique. Responsable del diseño centrado en el usuario y la usabilidad de la interfaz.

## 4. Acuerdos de Trabajo (Service Level Agreements)
Para garantizar la excelencia operativa, el equipo suscribe los siguientes acuerdos:
* **Sincronización:** Reuniones presenciales o virtuales todos los días hábiles a las 09:00 hs vía Discord.
* **Integración Continua:** Frecuencia mínima de tres (3) aportes de código (commits) por semana.
* **Definición de Terminado (DoD):** Ninguna tarea se considerará finalizada hasta que el código haya sido testeado y revisado por un miembro del equipo de QA.
* **Comunicación Oficial:** Canal exclusivo vía WhatsApp con un tiempo de respuesta esperado inferior a dos (2) horas durante el horario laboral.

## 5. Especificaciones Técnicas y Reglas de Negocio
El sistema deberá cumplir estrictamente con las siguientes lógicas operativas definidas:
* **Seguridad de Acceso:** La autenticación se basará en estándares industriales (JWT y Bcrypt). Se eliminan los roles de "Invitado", permitiendo únicamente perfiles de "Miembro" y "Administrador".
* **Administración Predefinida:** El sistema contará con cinco (5) cuentas de administrador de origen, asignadas a los creadores del proyecto: 
    1. **JesusDO** 
    2. **MatiasP** 
    3. **SantinoC** 
    4. **OctavioG** 
    5. **SantiagoM** 
* **Modelo de Reserva:** El catálogo de espacios será de acceso público (sin login previo). Sin embargo, el inicio de la reserva requerirá autenticación obligatoria.
* **Flujo de Confirmación:** Toda reserva solicitada por un miembro nacerá en estado "Pendiente" y requerirá la validación explícita de un Administrador para ser confirmada. El usuario podrá visualizar sus reservas y el administrador dispondrá de un panel para gestionarlas.
* **Integración de Datos:** No se permitirá el uso de datos sintéticos o falsos; la disponibilidad se calculará en base a la concurrencia real y el horario laboral establecido (08:00 a 20:00 hs).

## 6. Estándares de Calidad y Cumplimiento
El diseño del software se alineará con los siguientes estándares internacionales:
* **ISO/IEC 27001:** Para la protección de datos personales y la integridad de la información financiera.
* **ISO 9241-11 / ISO 13407:** Para garantizar la eficiencia y eficacia del sistema desde una perspectiva centrada en el usuario humano.

## 7. Conformidad
Al aceptar los términos de este contrato, los integrantes de **SpicyTech** asumen la responsabilidad compartida sobre la calidad, el diseño y la ética en el uso de herramientas de inteligencia artificial documentadas en el `AI_LOG` oficial del proyecto.

---

**Firmas:**

| Integrante | Rol |
| :--- | :--- |
| **Octavio García** | Scrum Master |
| **Matias Polcowñuk** | Dev Leader |
| **Jesus E. De Olivera** | QA Lead |
| **Santino Calamari** | Dev Leader / QA |
| **Santiago Manrique** | UX Lead |
