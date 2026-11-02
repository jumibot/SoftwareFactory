# Comandos antes que inferencia

- **Origen:** SoftwareFactory, 2026-10-29, tarea 100, al probar la P. El propietario: «para activar una rama preferiría que lo hagas con un comando en lugar de con inferencia…»; y después: «Lo que se pueda hacer con comando que se haga sin inferencia».
- **Contexto:** la P enviaba a Claude un prompt para cambiar de rama. Era lento, gastaba inferencia y el resultado podía variar, para algo que hace una orden de git.
- **Decisión:** lo que se pueda hacer con un comando (git, escribir la cola, generar un documento) se hace con el comando, sin pasar por Claude. Claude solo entra donde hace falta criterio: decidir, redactar, resolver un caso dudoso. En el panel, un botón ejecuta él mismo la orden y, si no puede (un caso que pide criterio), dice por qué y no hace nada.
- **Consecuencias:** la P activa la rama con `git switch` (ver «Botón P para probar una tarea en su rama»). Revisar el resto del panel con este criterio es la tarea 118. *Aplicado en la 118: la D descarta con git, la P pasa a en curso la tarea en cola (sin recargar, ver «La P no recarga el plugin»), la «→» del registro crea la tarea, y la C nueva cierra la tarea sin Claude.*
- **Aplicada en:** metodología, 1; plantilla `claude-sf.md`; `CLAUDE.md`; `plugins/sf/hooks/cola.ts` y `panel.tsx`.
