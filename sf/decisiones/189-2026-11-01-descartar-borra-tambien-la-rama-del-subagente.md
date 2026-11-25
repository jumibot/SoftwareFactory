# Descartar borra también la rama del subagente

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Al cerrar, cola.py borra la rama del subagente aunque tenga trabajo sin traer» (271). El propietario: «el descarte descarta todo».
- **Contexto:** la decisión 169 conserva, con aviso, la rama auxiliar `sub-NN` que tiene commits que no entraron en `develop`. Al descartar una tarea, eso dejaba su rama y su worktree.
- **Decisión:** descartar una tarea borra también su rama auxiliar y su worktree, aunque tengan commits que no entraron o cambios sin commit. Descartar ya es decidir tirar ese trabajo. Precisa la decisión 169 para el descarte; cerrar, pasar a Testing, dar por probada y revertir siguen conservándola con aviso.
- **Consecuencias:** un descarte no deja restos. Los commits descartados solo se recuperan por el reflog de git; los cambios sin commit, no.
- **Aplicada en:** `plugins/sf/tools/cola.py` (`descartar`, `limpiar`) y sus pruebas; `sf:flujo_tareas` («Recogida del subagente», `references/estados.md`); pendiente: «Cómo funcionan los estados».
