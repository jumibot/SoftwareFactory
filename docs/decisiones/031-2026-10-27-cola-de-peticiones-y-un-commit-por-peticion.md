# Cola de peticiones y un commit por petición

- **Origen:** SoftwareFactory, 2026-10-27. A la pregunta del propietario «que más podemos hacer para mejorar mi forma de trabajo con la sf?», Claude propuso cinco mejoras; el propietario: «sí, regístralas e implementa 1 y 2». Y después: «la cola de peticiones encaja en el jkanban como tareas de una lista de backlog».
- **Contexto:** las peticiones llegan a mitad de otra tarea; se acumulaban sin registro, varios cambios acababan en un mismo commit y lo que Claude no podía comprobar quedaba enterrado en los resúmenes.
- **Opciones:** seguir con el registro informal en la conversación; una cola en un archivo que lee el mod; la cola directamente en JKanban (aún no incorporado).
- **Decisión:** cada petición se anota en `.sf/peticiones.json` (fuera de git) en cuanto llega, con el estado `en-cola`, `en-curso` o `sin-probar`; cada petición se cierra con su propio commit; lo que solo el propietario puede comprobar queda `sin-probar` con qué probar, y sale de la cola cuando lo confirma. El mod de estado la muestra en una franja sobre el prompt y en `/sf`. Cuando JKanban esté incorporado, cada petición será una tarea de la lista de backlog del proyecto y el archivo, su copia sin conexión.
- **Consecuencias:** Claude mantiene la cola como parte de su trabajo; los proyectos añaden `.sf/peticiones.json` a su `.gitignore`.
- **Aplicada en:** metodología (2 y 6) y skill `sf:metodologia`; `CLAUDE.md` de la SF; mod de estado; `docs/como-funciona-la-software-factory.md`; plugin `sf` 0.9.0.
