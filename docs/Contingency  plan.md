# Plan de Gestión de Riesgos del Proyecto

Este documento detalla la Matriz de Riesgos identificada para el desarrollo del proyecto, alineada con los hallazgos visuales. Incluye las estrategias de mitigación (preventivas) y los planes de contingencia (reactivos).

## Resumen de Clasificación

Para la evaluación y visualización de los riesgos, se utiliza la siguiente escala de severidad, tal como se muestra en la matriz gráfica del proyecto:

* **Bajo (Verde):** Puntuaciones 1-3.
* **Medio (Amarillo/Naranja claro):** Puntuaciones 4-6.
* **Alto (Naranja oscuro):** Puntuaciones 8-12.
* **Extremo (Rojo):** Puntuaciones 15-25.

---

## 1. Matriz de Riesgos y Mitigación

Esta matriz identifica los eventos potenciales y establece acciones preventivas para reducir su probabilidad o impacto *antes* de que ocurran.

| # | Nombre del Riesgo | Categoría | Probabilidad | Impacto (Severidad Visual) | Plan de Mitigación (Preventivo) |
| :-: | :--- | :---: | :---: | :---: | :--- |
| **1** | **Falta de experiencia en React de Dev Leaders**: Retraso en calendario de reservas dinámico. | Técnicos | **Alta** | **Medio** (4-6) | Realizar una semana de investigación y prototipado rápido (PoC) enfocado en gestión de estados de React. |
| **2** | **Indisponibilidad por exámenes parciales**: Coincidencia de fechas de exámenes, reduciendo capacidad en Sprint 1. | Equipo | **Alta** | **Alto** (8-10) | Actualizar el tablero Kanban semanalmente y adelantar entregas críticas antes de las semanas de exámenes. |
| **3** | **Ambigüedad en reglas de negocio**: Retrabajo en backend por definición difusa de cancelaciones y reembolsos. | Requisitos | Media | **Alto** (12) | Mantener reuniones constantes con el docente para validar que las reglas de negocio sean claras y precisas. |
| **4** | **Dependencia de hosting gratuito**: Suspensión por inactividad (Render/Railway), dificultando pruebas y demo. | Externo | Media | **Medio** (12) | Configurar un sistema de logs de errores y realizar backups periódicos para asegurar disponibilidad. |
| **5** | **Conflictos de Concurrencia (Doble Reserva)**: Falta de conocimiento técnico para implementar bloqueos (locks) de BD. | Técnicos | Baja | **Alto/Extremo** (10-25) | Implementar validaciones estrictas en el backend antes de confirmar una reserva y capacitar al equipo en locks de BD. |

---

## 2. Plan de Contingencia

Este plan define las acciones inmediatas a tomar *una vez que el riesgo ha ocurrido* para minimizar los daños y recuperar el control del proyecto.

### 🚨 R1. Falta de experiencia en React
* **Disparador:** Tareas de gestión de estado bloqueadas o retrasos críticos detectados tras la primera semana de PoC.
* **Acción Inmediata:**
    1.  **Simplificar MVP:** Reúnase con stakeholders/docente para acordar una reducción drástica del alcance técnico de la gestión de estados. Sustituir lógicas complejas por soluciones simples o "hardcodeadas".
    2.  **Asignar Dueños:** Dividir el desarrollo por módulos y nombrar al miembro con más conocimiento como "dueño" técnico para centralizar y resolver bloqueos de React del equipo.
    3.  **Adaptar Código Verificado:** Priorizar el uso de repositorios de ejemplo o *boilerplates* verificados para React en lugar de programar arquitecturas base desde cero.

### 🚨 R2. Indisponibilidad por exámenes parciales
* **Disparador:** Miembros clave del equipo reportan incapacidad total de trabajo o baja drástica de productividad durante la semana crítica de entrega.
* **Acción Inmediata:**
    1.  **Congelar No Críticos:** Detener inmediatamente el pulido visual y las *features* secundarias. Cero recursos dedicados a ellas.
    2.  **Foco en *Happy Path*:** Redistribuir el esfuerzo limitado *exclusivamente* en asegurar que los flujos principales de usuario funcionen para la entrega (MVP).
    3.  **Consumir Reserva:** Utilizar la reserva de tiempo final (buffer) planificada para pruebas como tiempo de desarrollo ahora.
    4.  **Notificar:** Avisar preventivamente al docente sobre la entrega parcial debido a la baja disponibilidad del equipo.

### 🚨 R3. Ambigüedad en reglas de negocio
* **Disparador:** Identificación de retrabajo significativo en el backend o lógica de negocio que no cumple con las expectativas a mitad del desarrollo.
* **Acción Inmediata:**
    1.  **Detener Desarrollo:** Parar inmediatamente el desarrollo en la lógica afectada hasta tener claridad. Mover tareas a una lista de "Por Validar".
    2.  **Validación con Docente:** Programar una reunión de emergencia con el docente para re-definir y aclarar las reglas de negocio ambiguas. Obtener aprobación por escrito si es posible.
    3.  **Actualizar Documentación:** Reflejar inmediatamente los cambios en la documentación de requisitos y comunicarlos a todo el equipo para evitar futuros retrabajos.

### 🚨 R4. Dependencia de hosting gratuito
* **Disparador:** Detección de tiempos de inactividad o fallos en las pruebas integrales y demo debido a suspensión del hosting Render/Railway.
* **Acción Inmediata:**
    1.  **Diagnosticar:** Analizar logs de errores y alertas para hallar la causa raíz de la inactividad.
    2.  **Ejecutar Plan de Backups:** Iniciar inmediatamente el proceso de restore de la base de datos y/o archivos de aplicación desde el backup periódico más reciente.
    3.  **Prevenir Daño Circular:** Asegurar que el código de la aplicación o configuración no causará un nuevo fallo antes de reactivar el servicio. Si es necesario, configurar alertas adicionales.

### 🚨 R5. Conflictos de Concurrencia (Doble Reserva)
* **Disparador:** Reportes de usuarios de reservas duplicadas o detección visual de la severidad del riesgo alcanzando el nivel Alto/Extremo.
* **Acción Inmediata:**
    1.  **Congelar Confirmaciones:** Bloquear temporalmente nuevas confirmaciones en el backend (mantener el sistema en modo solo lectura).
    2.  **Identificar y Mediar:** Consultar la base de datos para hallar duplicados. Aplicar regla "primero en llegar": mantener la primera reserva, cancelar la segunda.
    3.  **Notificar y Compensar:** Informar inmediatamente a ambos usuarios. Ofrecer disculpas y una alternativa inmediata (otra fecha/recurso) al usuario cancelado.
    4.  **Parche Técnico:** Implementar un *fix* de emergencia (e.g., cola de mensajes, caché distribuida) o acelerar la capacitación y aplicación de locks de BD antes de reabrir el sistema.
