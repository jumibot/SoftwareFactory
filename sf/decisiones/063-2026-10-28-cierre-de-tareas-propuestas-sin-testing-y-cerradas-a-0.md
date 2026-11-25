# Cierre de tareas: propuestas sin Testing y Cerradas a 0

- **Origen:** SoftwareFactory, 2026-10-28. El propietario: «Las propuestas se anotan, no pasan por Sin probar»; «Aun sin tareas cerradas que aparezca la sección con 0»; «quiero agrupar las tareas pendientes que tienen que ver con el cierre de tareas. Pon todos los detalles en la descripción»; «sí, añade la descripción a la 61».
- **Decisión:** una petición que solo anota una propuesta se cierra al anotarla, sin Testing: no hay nada que probar hasta decidirla. La sección Cerradas se ve siempre, también con 0 al empezar la sesión (antes desaparecía y parecía un fallo). Una petición puede llevar `descripcion` con sus detalles, que el panel muestra al desplegarla.
- **Aplicada en:** metodología (2) y skill `sf:metodologia`; plantilla `templates/claude-sf.md`; mod de estado; `docs/como-funciona-la-software-factory.md`; plugin `sf` 0.31.1.
