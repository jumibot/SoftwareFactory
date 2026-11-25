# Lanzar sin esperar lo que no necesita al propietario

Estado: deprecada el 2026-11-25 por «El principal orquesta y lanza cada subagente sin preguntar» ({V-083}); lo demás, por «Todo el trabajo de la tarea, a su subagente» (151) y «TURBO pone en curso las tareas que no necesitan al propietario» (160).

- **Origen:** SoftwareFactory, 2026-10-29. El propietario: «No entiendo porque has esperado tanto a lanzar los subagentes si las tareas estaban en curso y no dependian de mi. Esto ha paso varias veces»; y: «compartir archivos no es motivo para esperar a no ser que haya alto riesgo de perdidas por la colisión».
- **Contexto:** el principal esperaba a cerrar la tarea en prueba antes de lanzar otras que tocaban los mismos archivos, y preguntaba o anunciaba los lanzamientos. Ocupaba tiempo y atención del propietario sin necesitarle.
- **Decisión:** al final de cada turno, el principal repasa las tareas en curso que no necesitan al propietario y las lanza, sin esperar a la conversación en marcha. Compartir archivos no es motivo para esperar, salvo alto riesgo de pérdidas por la colisión: el solape se resuelve al juntar. Sí lo es que una tarea necesite el resultado de otra. Solo las en curso: las de la cola esperan a que el propietario las ponga en curso. Lanza y avisa en una línea, sin preguntar.
- **Aplicada en:** lo vigente, en `sf:orquestacion` («Subagentes») y la metodología, «Orquestación con subagentes».
