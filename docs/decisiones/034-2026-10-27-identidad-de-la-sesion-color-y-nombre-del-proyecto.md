# Identidad de la sesión: color y nombre del proyecto

- **Origen:** SoftwareFactory, 2026-10-27. El propietario: «quiero el el mod al arrancar ponga cc con el color del proyecto y use el rename para poner el nombre del proyecto y eventualmente la tarea principal en la que se está trabajando», y «al cambiar de tarea que vaya renombrando la sesión».
- **Decisión:** al arrancar, el mod lanza `/color` con el color del proyecto (campo `color` de `.sf/proyecto.json`; la SF, `purple`) y `/rename` con el nombre del proyecto y la tarea principal (la primera petición en curso o, si no hay, la devslice). Al acabar cada turno, si la tarea cambió, renombra la sesión. Solo lanza los comandos cuando algo cambia.
- **Consecuencias:** cada proyecto elige su color en `.sf/proyecto.json`; un nombre puesto a mano se sustituye en el siguiente cambio de tarea. Con «Un proyecto por sesión», el color y el nombre dicen de un vistazo en qué proyecto y tarea está cada sesión.
- **Aplicada en:** metodología (6); mod de estado; `docs/como-funciona-la-software-factory.md`; plugin `sf` 0.12.0.
