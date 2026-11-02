# Una tarea en curso con rama no vuelve a la cola

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Al cerrar una tarea, cola.py quita el worktree y la rama auxiliar de su subagente» (246). Al decidir qué pasaba con el subagente al devolver una tarea a la cola, el propietario lo repensó: «queda prohibido pasar una tarea en curso que tiene rama a pendiente».
- **Contexto:** `cola.py en-cola` pasaba una tarea de en curso a en cola conservando su rama, y dejaba una rama viva sin subagente ni trabajo en marcha.
- **Decisión:** una tarea en curso con rama no puede volver a la cola. `cola.py en-cola` lo rechaza; para dejarla, se cierra, se pasa a Testing o se descarta. Una tarea en curso sin rama sí puede volver. Revertir, con «eliminar» o con «a Pendientes», borra también la rama de la tarea si aún existe y lo que quede de su subagente: la tarea queda sin rama y limpia, y al ponerla en curso sale una rama nueva desde develop. Solo se conserva, con aviso, una rama con commits que nunca entraron en develop.
- **Consecuencias:** no quedan ramas de tareas en cola, ni subagentes que recoger al devolverlas.
- **Aplicada en:** `plugins/sf/tools/cola.py`, el panel si ofrece esa orden, y `sf:flujo_tareas` y `sf:orquestacion` (246).
