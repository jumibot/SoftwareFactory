# La cola por dentro: historial, copias, bloqueo, quién y por dónde, reabrir y subagentes

`cola.py`, en Python, es la única forma de cambiar la cola. Por dentro funciona así:

- **Historial.** Cada tarea lleva su historial: cada cambio, con su fecha, quién lo decide (`propietario` o `principal`) y por dónde llega (`panel` o `cli`). También entran los pasos que se añaden, se marcan o se quitan.
- **Lo que sale de la cola** pasa, con su historial, a `.sf/historial.jsonl`: una línea por salida, con el estado con que sale. Una tarea eliminada desaparece de la vista, pero no se pierde: `restaurar` la devuelve desde ahí.
- **Copias y bloqueo.** Antes de cada escritura, cola.py guarda una copia de la cola (las últimas 50) y la bloquea con `.sf/peticiones.lock`, para que dos escrituras a la vez no la rompan.
- **El commit del cierre.** El hash del squash en `develop` queda en el historial, y Revertir lo lee de ahí. Si falla el push, también se anota, y el panel lo recuerda hasta que `develop` está subida.
- **Cerrar y observar.** Cerrar una tarea con rama hace el squash en `develop`, pase o no por observación. Una tarea en observación ya está en `develop`: no se descarta, se revierte.
- **Reabrir.** Una tarea reabierta, también una descartada, sale con una rama nueva desde `develop`; nunca se reutiliza el worktree viejo.
- **Subagentes.** El subagente trabaja en su rama auxiliar, no en la de la tarea, y el principal trae su trabajo con `git merge --ff-only`. El principal anota el worktree y la rama del subagente con `cola.py subagente` antes de lanzarlo. El subagente no escribe la cola; cola.py no lo comprueba.

Recoge lo que sigue valiendo de «Flujo de tareas: respuestas a la revisión de la tabla de estados» (115), que queda deprecada.

Porqué: la tabla de estados de la tarea 92 dejó 23 huecos e incoherencias entre las reglas escritas y el código del panel, y el propietario de la Software Factory aprobó en bloque estas respuestas para construir `cola.py` y `sf:flujo_tareas`. El historial y las copias permiten recuperar lo que sale o se rompe; saber quién y por dónde distingue el Cerrar del propietario en el panel de un cierre del principal; el hash permite revertir; la rama auxiliar deja libre la de la tarea mientras trabaja el subagente.

Aplicada en: `plugins/sf/tools/cola.py`; `sf:flujo_tareas` (SKILL.md, `references/estados.md` y `references/porque.md`); el panel (`plugins/sf/hooks/lectura.ts`, `cola.ts`, `panel.tsx`).
