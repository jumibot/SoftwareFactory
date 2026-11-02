# Cerrar y pasar a Testing desde el panel también las tareas en curso sin rama

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Las tareas en curso sin rama no se pueden cerrar desde el panel» (278). Se vio al cerrar la 272, que se puso en curso sin rama porque solo escribía en la cola.
- **Contexto:** el panel solo ofrece «Cerrar» en las tareas en curso con rama; una sin rama había que cerrarla con `cola.py cerrar`. Había dos salidas: que poner en curso cree siempre la rama, o que el panel ofrezca «Cerrar» también sin rama.
- **Decisión:** el panel ofrece «Cerrar» y «A Testing» en las tareas en curso sin rama cuyos pasos de trabajo están hechos. Cierran sin squash ni commit, con `cola.py cerrar` y `cola.py a-testing`, que ya lo admiten. «A Testing» también, por pregunta aparte al propietario el mismo día.
- **Consecuencias:** una tarea que solo toca la cola o no cambia archivos se cierra desde el panel sin crear una rama vacía.
- **Aplicada en:** plugins/sf/hooks/cola.ts, plugins/sf/hooks/panel.tsx, plugins/sf/tests/panel.test.tsx y plugins/sf/skills/flujo_tareas/references/estados.md (278).
