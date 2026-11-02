# Activar rama integra develop, avisa a Claude si choca y adelanta la rama del subagente

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Las ramas se prueban siempre al día con develop, sin pedírselo a Claude» (270). El propietario acepta las dos opciones recomendadas.
- **Contexto:** `cola.py probar` integra `develop` en la rama de la tarea antes de activarla; con choque lo deshace y avisa, y con trabajo del subagente sin traer no activa. El panel solo enseñaba el mensaje. Además, el merge deja `sub-NN` por detrás de la rama de la tarea y el siguiente `git merge --ff-only` del principal fallaría.
- **Decisión:**
  1. Si «Activar rama» choca o encuentra trabajo sin traer, el panel pasa el fallo a Claude, como ya hace «Cerrar», para que lo resuelva el subagente de la tarea.
  2. Tras integrar, `probar` adelanta la rama auxiliar: fast-forward en el worktree del subagente, o `branch -f` si no tiene, sin pisar cambios sin commit. Si no puede, avisa.
- **Consecuencias:** el principal sigue trayendo el trabajo con `git merge --ff-only` y probar no depende de pedírselo a Claude. `probar` toca el worktree del subagente, solo con fast-forward.
- **Aplicada en:** `cola.py probar` (270); el aviso del panel, pendiente (270); metodología y «Cómo funciona el panel», pendientes (208, 198).
