# La SF es fuente, no instalación operativa

- **Origen:** SoftwareFactory, 2026-10-27. Corrección del propietario: «sf es fuente y donde se crea y modifica pero no es un operativo…».
- **Contexto:** la primera instalación del mod en JKanban leía la carpeta de trabajo de la SF, así que cualquier cambio a medias le llegaba.
- **Decisión:** ningún proyecto usa la copia de trabajo de la SF. Usan lo publicado en GitHub, que Claude Code copia a `~/.claude/plugins/cache/`, y que solo cambia al actualizar a propósito. Los cambios se prueban antes con `claude --plugin-dir`.
- **Consecuencias:** el método viaja en el plugin desde el mismo día (decisión «La metodología viaja en el plugin `sf`»).
- **Aplicada en:** especificación, 1; `CLAUDE.md`; `plugins/sf/README.md`.
