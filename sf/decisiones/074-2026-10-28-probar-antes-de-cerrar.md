# Probar antes de cerrar

Estado: deprecada el 2026-11-25 por «Al terminar una tarea, Claude propone probarla o cerrarla, y cerrar espera el OK del propietario» (371).

- **Origen:** SoftwareFactory, 2026-10-28. Claude proponía cerrar tareas (commit y publicación) que aún no se habían probado, y Testing se llenaba.
- **Decisión:** al terminar una petición, Claude propone primero probarla, con una sugerencia de cómo hacer la prueba. Solo propone cerrarla sin probar si el cierre es necesario para poder probar. Objetivo: menos tareas en Testing.
- **Aplicada en:** lo vigente, en `sf:orquestacion` («Probar y cerrar») y la metodología, «Tareas y cola» («Probar y cerrar»).
