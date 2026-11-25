# Un cierre que falla pasa a Claude

- **Origen:** SoftwareFactory, 2026-10-29, tras tres C que chocaron en docs/decisiones.md. El propietario: «si falla un cierre pasa al agente principal el prompt para resolverlo».
- **Decisión:** si el squash de la C choca o falla su commit, el panel lo deshace, vuelve a la rama de antes y envía a Claude un prompt con la tarea, la rama y los archivos en conflicto para que cierre él. El propietario ya no tiene que contarlo.
- **Consecuencias:** precisa «Botón C para cerrar una tarea».
- **Aplicada en:** plugins/sf/hooks/cola.ts y sus pruebas; docs/como-funciona-el-panel.md.
