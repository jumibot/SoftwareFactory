# Cerrar exige siempre el paso de cerrar; quitar el de probar es cerrar sin probar

- **Origen:** SoftwareFactory, 2026-10-29, prueba del CLI `cola.py` de la tarea 92. Al cerrar la 157 sin rama y sin pasos de cierre, el CLI la dejó cerrar. El propietario: «exige siempre probar y cerrar, como antes. Si quiero cerrar sin probar elimino el paso de probar y ya está».
- **Contexto:** `cerrar` pedía «Probar la tarea» y «Cerrar la tarea» solo a una tarea con rama; sin rama, cerraba sin pasos y con pasos de trabajo pendientes. `a-testing` no pedía ninguno. Y para cerrar sin probar no había otro camino que saltarse los pasos.
- **Decisión:**
  - Todo cierre (`cerrar`, `a-testing`), con rama o sin ella y también en una propuesta, exige el paso «Cerrar la tarea» y que no quede pendiente ningún otro salvo «Probar la tarea». Una tarea sin pasos de cierre no se cierra: antes se añaden con `listo`.
  - «Cerrar la tarea» nunca se quita: la orden que quita pasos lo rechaza.
  - «Probar la tarea» sí se quita, si está pendiente, y quitarlo es la forma de cerrar sin probar. Si está, `cerrar` lo da por hecho, porque la C es el OK del propietario.
  - `probar` (la P) solo activa la rama: entrar en prueba no es estar probada, y no marca «Probar la tarea».
- **Consecuencias:** precisa la decisión 115, respuesta 5 (la C exige los pasos de cierre), que ahora vale para todo cierre y admite cerrar sin «Probar la tarea»; y la 117 (los pasos de cierre no se eliminan): «Probar la tarea» vuelve a poder quitarse, y en el panel vuelve a tener E, lo que hace la tarea 138, reabierta.
- **Aplicada en:** `plugins/sf/tools/cola.py` y sus pruebas; `plugins/sf/skills/flujo_tareas/SKILL.md` y `references/estados.md` (tarjetas 08, 13, 15, 18, 20 y 21, y sección 5).
