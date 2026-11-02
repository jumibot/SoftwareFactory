# «En observación», sin alias ni rastros

- **Origen:** SoftwareFactory, 2026-11-02. Al aplicar «Testing pasa a llamarse «En observación»» (212) en «Testing pasa a «En observación»: se cierra o se revierte, sin rastros del nombre viejo» (291), se propuso mantener alias de las órdenes viejas y dudar si cambiar el valor interno de la cola. El propietario: «prefiero una limpieza y no dejar flecos ya en el inicio del proyecto. Aquí tú puedes hacer una gran labor para mí con testings automáticos. Lo mismo aplica a 3, prefiero el refactor ahora, y para la 4 ok».
- **Contexto:** el inventario de la 291 separó lo visible (panel, avisos, preguntas), las órdenes de `cola.py` (`a-testing`, `probada`, `probando`, `pendiente`) y lo interno (el estado `sin-probar`, el campo `probando`, los eventos). Mantener alias o valores viejos deja dos nombres para lo mismo.
- **Decisión:**
  - Las órdenes se renombran sin alias: `a-testing` pasa a `a-observacion`, una tarea en observación se cierra con `cerrar` (desaparece `probada`), y las demás toman su nombre nuevo. Los nombres viejos dejan de existir.
  - Lo interno también se renombra: el estado `sin-probar` pasa a `en-observacion` y el campo `probando` a `observando`, con sus eventos.
  - El historial de versiones de los documentos y las decisiones antiguas no se tocan: son historia.
  - Lo garantizan pruebas automáticas, entre ellas una que falla si reaparece el nombre viejo en lo que está en el alcance.
- **Consecuencias:** las colas ya guardadas en otros proyectos se convierten una vez al cargarlas, porque sin eso dejarían de abrirse; es una migración, no un alias, y la prueba lo cubre. Lo que llame a las órdenes viejas (skills, panel, documentos) se cambia en la misma tarea. Preferencia general: al principio del proyecto, limpieza completa antes que compatibilidad con nombres viejos.
- **Aplicada en:** pendiente; en la 291.
