# Nombre de la sesión: el del proyecto, solo al entrar

- **Origen:** SoftwareFactory, 2026-10-28. El propietario: «He visto que nos es útil teniendo el panel renombrar esto continuamente. Deja siempre el nombre del proyecto sin modificar». Y, viendo `/rename SoftwareFactory` tras recargar el plugin: «No renombres la sesión más que al entrar».
- **Decisión:** `/rename` pone solo el nombre del proyecto, sin la tarea, y `/color` y `/rename` se lanzan una vez, al entrar. El mod guarda lo puesto en su estado de la sesión, que sobrevive a `/reload-plugins`, y solo los repite si cambian el color o el nombre de `.sf/proyecto.json`. Sustituye en parte a «Identidad de la sesión: color y nombre del proyecto» (el nombre ya no lleva la tarea).
- **Aplicada en:** mod de estado; especificación; `docs/como-funciona-la-software-factory.md`; plugin `sf` 0.30.1.
