# Probar antes de cerrar

- **Origen:** SoftwareFactory, 2026-10-28. Claude proponía cerrar tareas (commit y publicación) que aún no se habían probado, y Testing se llenaba.
- **Decisión:** al terminar una petición, Claude propone primero probarla, con una sugerencia de cómo hacer la prueba. Solo propone cerrarla sin probar si el cierre es necesario para poder probar. Objetivo: menos tareas en Testing.
- **Aplicada en:** metodología, 2; plantilla `claude-sf.md`; `CLAUDE.md`.
