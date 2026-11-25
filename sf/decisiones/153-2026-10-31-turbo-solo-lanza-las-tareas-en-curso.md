# TURBO solo lanza las tareas en curso

Estado: deprecada el 2026-10-31 por «TURBO pone en curso las tareas que no necesitan al propietario» (160).

- **Origen:** SoftwareFactory, 2026-10-31, tarea «Auditar que la skill de orquestación recoge todo lo ordenado» (216). El propietario aceptó la recomendación de la auditoría.
- **Contexto:** la auditoría vio ambiguo si el botón TURBO del panel autoriza poner en curso tareas de la cola.
- **Decisión:** TURBO lanza el subagente de las tareas en curso que no lo tienen. No pone en curso tareas de la cola: eso lo decide el propietario.
- **Consecuencias:** se mantiene «las de la cola, nunca».
- **Aplicada en:** ninguna pieza: `sf:orquestacion` recoge la 160.
