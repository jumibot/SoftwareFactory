# Pasos de cierre: probar y cerrar la tarea

- **Origen:** SoftwareFactory, 2026-10-29, tarea 101, pedida al cerrar la 94: que el panel muestre que a una tarea solo le falta cerrarse. El propietario aprobó la propuesta de Claude («sí a todo»).
- **Opciones:** un solo paso «Probar y cerrar», o dos separados.
- **Decisión:** dos pasos pendientes al final, en cuanto acaba el último paso de trabajo: «Probar la tarea», con lo que hay que mirar en el campo `prueba`, y «Cerrar la tarea». Separados, porque la prueba depende del propietario y el cierre de su OK. Un cambio pedido al probar es un paso nuevo antes de los dos. Cerrar es: con rama, squash en `develop`, push, borrar la rama y sacarla de la cola; sin rama, sacarla de la cola; donde el commit lo hace el propietario, dejarla lista para su commit. Como la cerrada sale de la cola, «Cerrar la tarea» no llega a verse hecho.
- **Consecuencias:** hasta la skill `sf:flujo_tareas` (tarea 92), Claude añade y marca estos pasos a mano; después, sus scripts.
- **Aplicada en:** metodología, 2 («Pasos de una tarea»); plantilla `claude-sf.md`.
