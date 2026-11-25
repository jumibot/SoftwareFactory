# TURBO pone en curso las tareas que no necesitan al propietario

- **Origen:** SoftwareFactory, 2026-10-31, tarea «El texto de TURBO pide poner en curso tareas de la cola» (226). El propietario: «la 153 está mal aceptada por mi parte. El objetivo de Turbo es mover tareas pendientes a en curso, siempre y cuando no requieran interactuar con el owner».
- **Contexto:** «TURBO solo lanza las tareas en curso» (153) se aceptó a partir de una recomendación de la auditoría de la orquestación y dejaba TURBO sin su propósito.
- **Decisión:** TURBO pone en curso, cada una con su subagente, las tareas de la cola que se pueden hacer sin interactuar con el propietario, y avisa de cuáles. Las tareas que necesitan al propietario se quedan en la cola.
- **Consecuencias:** sustituye a «TURBO solo lanza las tareas en curso» (153). La regla «las de la cola, nunca, tampoco con TURBO» de `sf:orquestacion` deja de valer para TURBO; sin TURBO, poner en curso sigue esperando al propietario.
- **Aplicada en:** `plugins/sf/skills/orquestacion/SKILL.md` y `references/porque.md`; `plugins/sf/skills/flujo_tareas/references/estados.md`; texto del botón en `plugins/sf/hooks/cola.ts` y sus pruebas (226).
