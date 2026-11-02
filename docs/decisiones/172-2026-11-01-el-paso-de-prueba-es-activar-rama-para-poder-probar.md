# El paso de prueba es «Activar rama para poder probar»

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Las órdenes de cada tarea, en un menú de etiquetas al desplegarla» (247). Tras renombrar la orden T a «Activar rama», el propietario: «el paso debe ser Activar rama para poder probar».
- **Contexto:** el paso de cierre «Probar la tarea» se marcaba con el OK del propietario, y la C del panel ya es ese OK («probada, ciérrala»). La orden que pone la tarea en prueba es activar su rama.
- **Decisión:** el paso de cierre «Probar la tarea» pasa a llamarse «Activar rama para poder probar» y se marca hecho al activar la rama de la tarea (la orden «Activar rama» del panel o `cola.py probar`). El OK del propietario es cerrar. Quitar el paso sigue siendo cerrar sin probar.
- **Consecuencias:** las colas existentes renombran el paso pendiente. `cola.py`, el panel, `sf:flujo_tareas` y `sf:orquestacion` lo buscan por el nombre nuevo.
- **Aplicada en:** `plugins/sf/tools/cola.py`, `plugins/sf/hooks/` y sus pruebas; `sf:flujo_tareas` y `sf:orquestacion` (247).
