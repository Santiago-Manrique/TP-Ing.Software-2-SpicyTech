
# Parte A: Diseño de Interfaz Centrado en el Usuario (Eje 3)

## A1. Prototipado en Figma
El prototipo de **SpicyTech** ha sido diseñado para reflejar el flujo crítico de reserva de recursos, asegurando una navegación intuitiva y una jerarquía visual clara.

*   **Enlace al prototipo navegable:** [https://mobile-excel-62702710.figma.site/]

### Vistas Principales del Sistema
*A continuación se presentan las capturas de pantalla de las tres pantallas que cubren el caso de uso principal.*

| Pantalla 1: Panel de Control / Inicio | Pantalla 2: Formulario de Reserva | Pantalla 3: Confirmación de Éxito |
| :---: | :---: | :---: |
| <img src="https://github.com/user-attachments/assets/638dd97c-01ee-4a6e-a44e-d4989e1d82a1" width="200" alt="PC inicio"><br><sub>PC</sub><br><br><img src="https://github.com/user-attachments/assets/9e6aef5b-366f-4aa6-bbe4-f081b586e6f7" width="200" alt="Tablet inicio"><br><sub>Tablet</sub><br><br><img src="https://github.com/user-attachments/assets/89510abf-fc2d-4296-80ef-0ef8dc6469e7" width="120" alt="iphone 16 inicio"><br><sub>Mobile</sub> | <img src="https://github.com/user-attachments/assets/8e58ac7d-bd53-4881-8c90-05a0068df664" width="200" alt="PC reserva"><br><sub>PC</sub><br><br><img src="https://github.com/user-attachments/assets/07ab8649-f9a1-4e77-83b1-8f403e2c6735" width="200" alt="Tablet reserva"><br><sub>Tablet</sub><br><br><img src="https://github.com/user-attachments/assets/9fefc6f3-ec28-4b44-90ef-0c8ff8168d2b" width="120" alt="iphone 16 reserva"><br><sub>Mobile</sub> | <img src="https://github.com/user-attachments/assets/313b1293-0662-4017-a9a5-3739b8e3171d" width="200" alt="PC reserva exito"><br><sub>PC</sub><br><br><img src="https://github.com/user-attachments/assets/164c68e6-c629-4aa8-b03d-bf7a970d8d85" width="200" alt="Tablet reserva exito"><br><sub>Tablet</sub><br><br><img src="https://github.com/user-attachments/assets/aa7ed903-a272-4fd2-b591-fbedbc84a658" width="120" alt="iphone 16 reserva confirmado"><br><sub>Mobile</sub> |

## A2. Análisis de Usuario, Tarea y Contexto

**Usuarios Objetivo:**  
El sistema está dirigido a personas de entre 18 y 60 años con un nivel de alfabetización digital medio. Los perfiles se dividen en:
1.  **Usuarios finales:** Clientes que buscan realizar una reserva de forma rápida y autónoma.
2.  **Personal administrativo:** Encargados de gestionar y validar las reservas recibidas.

**Tareas Principales:**  
La tarea crítica es la **creación de una reserva válida**. Esto implica que el usuario debe poder visualizar la disponibilidad en tiempo real, seleccionar los parámetros deseados (fecha, hora, recurso) y completar sus datos de contacto sin ambigüedades.

**Contexto de Uso:**  
El sistema se utiliza principalmente en **dispositivos móviles y computadoras de escritorio**. Los usuarios suelen interactuar con la aplicación en entornos con distracciones (vía pública o entornos de oficina), lo que exige una interfaz con carga cognitiva baja, tiempos de respuesta rápidos y una visualización adaptada a diferentes condiciones de iluminación.

---

## A3. Auditoría de Usabilidad según ISO 9241-11

Se han seleccionado dos criterios fundamentales de la norma para evaluar el estado actual del prototipo de SpicyTech.

| Criterio | Métrica Definida | Simulación de Evaluación | Mejora Propuesta |
| :--- | :--- | :--- | :--- |
| **Eficacia** | Tasa de éxito en la finalización de la tarea. | 8 de cada 10 usuarios logran completar la reserva en el primer intento sin ayuda externa. | Incorporar validación en tiempo real en los campos de entrada para prevenir errores de formato. |
| **Eficiencia** | Tiempo medio empleado para concretar la reserva. | Un usuario promedio tarda 45 segundos desde que ingresa al sistema hasta que recibe el comprobante. | Reducir la cantidad de clics mediante un selector de fecha y hora más visual (calendario integrado). |

### Alineación con el Ciclo de Diseño Centrado en el Usuario (ISO 13407)
El proceso de desarrollo de este TP se alinea con la norma **ISO 13407** mediante un enfoque iterativo:
1.  **Entender el contexto:** Análisis realizado en la sección A2.
2.  **Especificar requisitos:** Definición de la tarea de reserva.
3.  **Producir soluciones de diseño:** Creación del prototipo navegable en Figma.
4.  **Evaluar el diseño:** Aplicación de la auditoría de usabilidad para retroalimentar el desarrollo del backend.

---
