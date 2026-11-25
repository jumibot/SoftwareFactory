# Cada tarea, en una sola sección del panel

- **Origen:** SoftwareFactory, 2026-10-31, tarea 196. El propietario, ante las tareas en curso repetidas en Pendientes: «las tareas solo aparecen en una cola… he visto que esto no aporta»; y después: «algo parecido pasa con las cerradas reabiertas… revisa todos los cambios de estado para ver aquellos en los que la tarea queda en dos secciones».
- **Contexto:** una tarea salía en dos secciones a la vez: en curso, arriba y en Pendientes; en Testing, también en Cerradas; reabierta o revertida a Pendientes, también en Cerradas; en prueba, arriba y en Testing.
- **Decisión:** cada tarea sale en una sola sección del panel, la de su estado. La cabecera de tareas en curso, arriba, es el foco y no cuenta como sección. Cerradas muestra solo las que han salido de la cola y las descartadas; Testing, las que esperan prueba y no se están probando; Pendientes, solo las en cola.
- **Consecuencias:** una tarea reabierta deja Cerradas y vuelve solo a Pendientes o arriba, con su número sobre fondo rojo. Pasar a Testing la quita de Cerradas.
- **Aplicada en:** plugins/sf/hooks/panel.tsx y sus pruebas. Cómo funciona el panel se ajusta en su tarea de actualizar.
