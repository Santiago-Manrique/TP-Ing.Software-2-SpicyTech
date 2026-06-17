# Sistema de Reservas para Espacios de Coworking
**Grupo:** SpicyTech 
**Proyecto:** Sistema de Reservas UCP 
**Materia:** Ingeniería de Software II · UCP · 2026

---

## Descripción del Proyecto
Este sistema permite a los miembros de un espacio de coworking reservar salas y escritorios de forma eficiente a través de una interfaz web, eliminando conflictos de doble reserva. El software gestiona la disponibilidad en tiempo real, permite bloqueos por mantenimiento y mantiene un historial detallado de las reservas por miembro. 

---

## Integrantes y Roles
| Nombre | Rol | GitHub |
| :--- | :--- | :--- |
| **Octavio García** | **Scrum Master** | @octavioleogarcia-png |
| **Calamari Santino** | Dev Leader + QA Lead | @Barriletecosmicok |
| **Polcowñuk Matias** | Dev Leader | @ZeroKava |
| **De Olivera Jesus** | QA Lead | @Jesucristo23 |
| **Manrique Santiago** | UX Lead | @Santiago-Manrique |



---

## Enlaces de Gestión
**Tablero Kanban:** https://github.com/users/ZeroKava/projects/2/views/1

**Reporte Semanal (S1):** [Enlace al campus/Moodle](PEGAR_ACA_LINK_A_MOODLE)

---

## Estructura del Repositorio
Organización de archivos según los lineamientos de la cátedra: 

**docs/**: Documentación oficial (Contrato, Matriz de Riesgos y AI_LOG).

**design/**: Prototipos y mockups del sistema. 

**src/**: Código fuente del proyecto. 

**tests/**: Casos de prueba y validaciones.


**Patrones de Diseño Seleccionados:**
Factory Method y Observer  

---

## Despliegue en Vercel

El proyecto ya quedó preparado para Vercel con:

- `vercel.json` en la raíz.
- Función Python en `api/[...path].py` para exponer el backend Flask.
- `index.html` raíz como entrada pública.
- `src/` con el frontend estático original.

Variables de entorno requeridas:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SMTP_USER`
- `SMTP_PASS` o `GMAIL_APP_PASSWORD`
- `EMAIL_FROM`
- `CONTACT_EMAIL`
- `CONTACT_PHONE`
- `CONTACT_WEB`

### Correo

Para Gmail, no uses la contraseña normal de la cuenta. Debés configurar una cuenta corporativa o de trabajo con verificación en dos pasos y generar una App Password. Sin eso, Gmail va a devolver `535 5.7.8 Username and Password not accepted`.

### Checklist exacta

#### Paso 1: base funcional

- [ ] Confirmar que `src/auth.py` compila sin errores.
- [ ] Verificar que el flujo de reservas confirma, rechaza y genera QR.
- [ ] Ejecutar `python analytics.py` y confirmar que imprime `Paso 1`.

#### Paso 2: Vercel

- [ ] Crear las variables de entorno en Vercel: `SUPABASE_URL`, `SUPABASE_KEY`, `SMTP_USER`, `SMTP_PASS` o `GMAIL_APP_PASSWORD`, `EMAIL_FROM`, `CONTACT_EMAIL`, `CONTACT_PHONE`, `CONTACT_WEB`.
- [ ] Confirmar que `vercel.json` apunta a `api/[...path].py`.
- [ ] Verificar que la raíz pública use `index.html`.
- [ ] Ejecutar deploy en Vercel y validar que el backend responda con la URL publicada.

#### Paso 3: Gmail App Password

- [ ] Activar verificación en dos pasos en la cuenta de Google.
- [ ] Entrar en Google Account > Security > App passwords.
- [ ] Crear una nueva App Password para la app de correo.
- [ ] Copiar esa clave en `SMTP_PASS` o `GMAIL_APP_PASSWORD`.
- [ ] Probar `python tests/manual_email_smoke.py` y confirmar que no aparece `535 5.7.8`.

#### Paso 4: validación del upgrade

- [ ] Crear una reserva con `10` días o más de anticipación.
- [ ] Confirmar que la correlación histórica sea positiva.
- [ ] Verificar que el sistema dispare `BOOKING_UPGRADE_AVAILABLE` y envíe el email de “Upgrade a jornada completa”.

### Ejecución local

```bash
python analytics.py
python tests/manual_email_smoke.py
```
