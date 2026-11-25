# Las propuestas, en el bloque TAREAS; sin bloque PROYECTO

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Simplificar la SF: sin registro ni mejoras desde otros proyectos» (282). El propietario, al probarla: «pon las propuestas en la sección de tareas y quita la sección de PROYECTO. Seguimos KISS».
- **Contexto:** tras quitar SF ENHANCE (194) y Documentos (195), el bloque PROYECTO del panel solo tenía la sección Propuestas.
- **Decisión:** la sección Propuestas pasa al bloque TAREAS, y desaparece el bloque PROYECTO. Pasar una propuesta a Pendientes se hace con una etiqueta «A Pendientes», como las demás órdenes del panel, en lugar de la «→»; «A propuesta» se queda. El panel queda con un solo bloque.
- **Consecuencias:** menos piezas en el panel; las propuestas se ven junto a las tareas en que se convierten.
- **Aplicada en:** el panel (`plugins/sf/hooks/panel.tsx`: Propuestas al final del bloque, con «A Pendientes») y sus pruebas; `sf:flujo_tareas` (`references/estados.md`); especificación; «Cómo funciona la Software Factory» («El panel de la SF»); pendiente: «Cómo funciona el panel».
