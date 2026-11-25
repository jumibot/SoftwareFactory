# La metodología viaja en el plugin `sf`

- **Origen:** SoftwareFactory, 2026-10-27: «mete la metodología dentro del plugin sf».
- **Contexto:** los proyectos enlazaban la metodología en la carpeta de trabajo de la SF (`../SoftwareFactory/docs/metodologia/`), en contra de «La SF es fuente, no instalación operativa».
- **Opciones:** copiar el documento al plugin al publicar (dos copias, una generada) o moverlo al plugin (una sola fuente).
- **Decisión:** la fuente de la metodología pasa a `plugins/sf/skills/metodologia/references/desarrollo-de-proyectos.md`, y la skill `sf:metodologia` dice qué sección leer en cada momento. Los enlaces a decisiones, propuestas y especificación apuntan a su versión publicada en GitHub.
- **Consecuencias:** cada proyecto lee la versión instalada del método; un cambio en el método se publica como una versión del plugin. El mod reconoce el repositorio de la SF por `plugins/sf/.claude-plugin/plugin.json`.
- **Aplicada en:** plugin `sf` 0.5.0; `CLAUDE.md`, README, especificación, metodología (2), JKanban (`CLAUDE.md`).
