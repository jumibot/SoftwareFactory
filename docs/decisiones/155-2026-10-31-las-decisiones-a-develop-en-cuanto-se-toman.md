# Las decisiones, a develop en cuanto se toman

- **Origen:** SoftwareFactory, 2026-10-31, tarea «Auditar que la skill de orquestación recoge todo lo ordenado» (216). El propietario aceptó la recomendación de la auditoría. Recoge la propuesta «Decisiones a develop al momento» del informe «Trabajo con la SF y sin ella».
- **Contexto:** si el principal escribe una decisión en la rama de una tarea mientras su subagente trabaja, chocan las ramas; si la escribe el subagente, la decisión espera al cierre de la tarea para llegar a develop.
- **Decisión:** el principal registra cada decisión en su archivo de docs/decisiones/ y la lleva a develop en cuanto se toma, con el índice regenerado. Aplicarla a la metodología, las skills o los documentos sigue siendo trabajo de la tarea, en su subagente.
- **Consecuencias:** las decisiones están en develop al momento y no chocan con las ramas de los subagentes.
- **Aplicada en:** `plugins/sf/tools/cola.py` (`decision`) y sus pruebas; `sf:orquestacion` («Preguntar») y su `references/porque.md`; plantilla `claude-sf.md`; metodología, «Estructura documental común»; `CLAUDE.md`; «Cómo funciona la Software Factory».
