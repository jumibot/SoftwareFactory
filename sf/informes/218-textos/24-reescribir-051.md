# La pregunta de «¿está probada?»: una por petición, con tres respuestas

Estado: deprecada el 2026-11-25 por «Una tarea en observación sale solo con el OK del propietario, que se pide tarea a tarea» ({V-050}); lo demás, por «Los estados de las tareas se nombran con el lenguaje de la SF» (204) y «¿Cómo va la N?» de las tareas en observación sigue siendo un menú» (327).

- **Origen:** SoftwareFactory, 2026-10-28. Ante un menú con «Las pruebo luego», «49, 50 y 52, probadas» y «Todas probadas», el propietario: «Este menu es confuso lo podemos tunear para la próxima?». A la propuesta de Claude: «No prefiero una lista con cada tarea y tres checks: probada, pendiente, probar ahora».
- **Contexto:** el menú daba números sin decir qué era cada petición, mezclaba varias peticiones en una misma respuesta y sus descripciones se cortaban.
- **Decisión:** la pregunta es una lista con una entrada por petición, con su número, su título y qué mirar, y tres respuestas en cada una: Probada (sale de Sin probar), Pendiente (queda en Sin probar) y Probar ahora (Claude dice qué mirar y espera el resultado, sin abrir otra petición ni preguntar por la siguiente; el propietario: «si te digo a una probar ahora, no me intentes abrir otra tarea...»). Con la herramienta de preguntas, es una pregunta por petición, cuatro como mucho en cada vez. Las respuestas van sin descripción, porque se explican solas (el propietario: «lo quiero compacto. Fuera explicaciones de cosas obvias...»).
- **Aplicada en:** lo vigente, en `sf:orquestacion` («Probar y cerrar» y «Preguntar»).
