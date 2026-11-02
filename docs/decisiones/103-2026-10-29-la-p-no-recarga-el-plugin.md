# La P no recarga el plugin

- **Origen:** SoftwareFactory, 2026-10-29, tarea 118, al probar la P. El propietario: «no hagas el reload, queda bajo mi responsabilidad. el modo prueba cambia de rama y si es necesario pone la tarea en curso».
- **Contexto:** en modo prueba, la P lanzaba `/reload-plugins` tras el `git switch`. La recarga solo hace falta si la rama trae otro `plugins/sf`, y solo en la SF.
- **Decisión:** la P cambia de rama y, si la tarea está en cola, la pasa a en curso. No recarga el plugin: recargar queda a cargo del propietario.
- **Consecuencias:** sustituye en parte a «Botón P para probar una tarea en su rama» y a la precisión de la 118. El aviso pasa a ser «Rama … activa: probar la N».
- **Aplicada en:** `plugins/sf/hooks/cola.ts` y sus pruebas; `docs/como-funciona-el-panel.md`; metodología, 2 («Ramas por tarea»).
