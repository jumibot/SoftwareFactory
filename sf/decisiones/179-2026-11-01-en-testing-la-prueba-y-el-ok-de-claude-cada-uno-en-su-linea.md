# En Testing, la prueba y el OK de Claude, cada uno en su línea

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Las tareas de Testing no están bien alineadas ni sangradas en el panel» (237). El propietario confirma el cambio: «Sí, cada uno en su línea».
- **Contexto:** desde el 2026-10-31, en la tarea desplegada de Testing, «probar: …» y «✓ Claude: …» iban en la misma línea que la rama y el commit; al ser largos, se partían en la columna 0, sin sangría, y la tarea no quedaba alineada como en las demás secciones.
- **Decisión:** la línea de la rama lleva solo la rama y el commit, como en las demás secciones. Debajo, «✓ Claude: …» y «probar: …» van cada uno en su línea, en la columna del título, y al partirse siguen bajo él. Vale en Testing y en la tarea que se prueba arriba.
- **Consecuencias:** sustituye lo decidido el 2026-10-31 sobre poner la prueba y el OK de Claude en la línea de la rama.
- **Aplicada en:** `plugins/sf/hooks/panel.tsx` y sus pruebas (237).
