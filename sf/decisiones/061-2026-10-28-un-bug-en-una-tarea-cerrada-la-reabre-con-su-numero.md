# Un bug en una tarea cerrada la reabre con su número

- **Origen:** SoftwareFactory, 2026-10-28. Al corregir en pruebas la 66, el propietario pidió que la tarea reabierta mantuviera su número, en Cerradas y en rojo; la norma se extiende a los bugs de tareas cerradas.
- **Decisión:** si al probar una tarea hay que corregirla, o aparece un bug en una tarea ya cerrada (en Testing o probada), se reabre esa tarea con su número: vuelve a `en-curso`, o a la cola con su número si había salido. No se crea una tarea nueva, para que el fallo quede unido a su origen y la cuenta de cerradas no engañe. Solo es tarea nueva lo que cambia el alcance.
- **Aplicada en:** metodología (2) y skill `sf:metodologia`; plantilla `templates/claude-sf.md`.
