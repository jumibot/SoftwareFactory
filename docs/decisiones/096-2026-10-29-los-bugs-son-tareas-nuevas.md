# Los bugs son tareas nuevas

- **Origen:** SoftwareFactory, 2026-10-29, al informar de que el panel había perdido la duración de la sesión. El propietario: «regla orquestador: Los bugs son tareas nuevas. Si lo ves importante o muy trivial puedes preguntar y ponerlo en curso a la vez. Intento que todas las tareas pasen por el panel».
- **Contexto:** el bug se investigó en el chat sin pasar por la cola, así que no se veía en el panel.
- **Decisión:** todo bug, lo detecte Claude o lo diga el propietario, entra en la cola en cuanto aparece, con su descripción. Si se puede atribuir a una tarea ya cerrada, esa tarea se reabre con su número (sigue valiendo «Reabrir en lugar de crear»); si no, porque no se localiza la tarea que lo causó, es una tarea nueva. El propietario: «sigue valiendo reabrir pero un bug puede que no sea sobre una tarea concreta que podamos localizar». El principal no lo investiga ni lo arregla fuera de una tarea. Si es importante o muy trivial, puede preguntar si se pone en curso, a la vez que la anota. Así todo el trabajo pasa por el panel.
- **Consecuencias:** precisa «Errores detectados, a Pendientes», que solo hablaba de los que detecta Claude.
- **Aplicada en:** metodología, 2 («Orquestación con subagentes» y «Errores detectados, a Pendientes»); plantilla `claude-sf.md`; `CLAUDE.md`.
