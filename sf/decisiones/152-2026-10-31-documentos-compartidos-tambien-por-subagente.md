# Documentos compartidos, también por subagente

- **Origen:** SoftwareFactory, 2026-10-31, tarea «Auditar que la skill de orquestación recoge todo lo ordenado» (216). El propietario aceptó la recomendación de la auditoría.
- **Contexto:** «Los documentos compartidos se actualizan en una tarea aparte» (112) decía que se hacen de una en una, en el principal. Choca con «Todo el trabajo de la tarea, a su subagente» (151). El motivo de hacerlas de una en una era no tener dos en paralelo sobre el mismo documento, no que las hiciera el principal.
- **Decisión:** las tareas «Actualizar <documento>» tienen su subagente como cualquier otra. Se siguen haciendo de una en una: no se lanza una mientras otra del mismo grupo de documentos está en marcha.
- **Consecuencias:** precisa la 112. El principal queda libre también mientras se actualiza la documentación.
- **Aplicada en:** `sf:orquestacion` («Documentos compartidos») y su `references/porque.md`; metodología, «Tareas y cola»; `CLAUDE.md`.
