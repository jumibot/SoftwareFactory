# Errores detectados, a Pendientes

- **Origen:** SoftwareFactory, 2026-10-28. Al documentar el panel, Claude vio que la caja sobre el prompt seguía diciendo «mejoras SF a valorar» y preguntó si lo arreglaba. El propietario: «norma: Cuando detectes errores déjalos en la lista de pendientes con su descripción correspondiente».
- **Decisión:** un error que Claude detecta y no es de la tarea en curso se anota en la cola, en cola, con una descripción de qué falla, dónde y cómo se ve. No se arregla de paso ni se queda solo en el chat. Si es de una tarea cerrada, se reabre esa tarea.
- **Aplicada en:** metodología, 2; plantilla `claude-sf.md`; `CLAUDE.md`.
