# Al terminar una tarea, Claude propone probarla o cerrarla, y cerrar espera el OK del propietario

Al terminar una tarea, Claude enseña lo hecho y propone probarla, con cómo. Si no tiene nada que probar (deliberar, investigar, documentar, especificar…), propone cerrarla directamente, enseñando el resultado: el OK del propietario es la aprobación.

El cierre, el paso a observación y la publicación esperan el OK del propietario. Los commits de trabajo en la rama, no («Los commits de trabajo en la rama de la tarea no esperan el OK», {N6}).

Toda tarea lleva dos pasos de cierre: «Activar rama para poder probar» y «Cerrar la tarea». Van separados porque la prueba depende del propietario, y el cierre, de su OK. Un cambio pedido al probar es un paso nuevo antes de ellos. Cómo se llaman y cuándo se ponen, en «El paso de prueba es «Activar rama para poder probar»» (172) y «Los pasos de cierre, desde que la tarea entra en curso» (174).

Un OK sin número («ciérrala», «ok») es para la tarea de la rama activa. Si hay duda (la rama activa no es de ninguna tarea, o el contexto apunta a otra), Claude pregunta antes de cerrar.

Recoge lo que sigue valiendo de «Preguntar antes de cerrar una petición; lo nuevo, a la cola» (048), «Probar antes de cerrar» (074), «Pasos de cierre: probar y cerrar la tarea» (090), «La tarea que se prueba es la de la rama activa» (095) y «Cerrar directamente lo que no tiene prueba» (154), que quedan deprecadas.

Porqué: Claude cerró y publicó una skill sin permiso (048). Proponía cerrar tareas sin probarlas y la observación se llenaba (074). Deliberar, investigar, documentar o especificar no se prueban como el código (154). Con dos pasos, el panel muestra que a una tarea solo le falta cerrarse (090). Un «probada» sin número se aplicó a otra tarea tras un cambio de rama (095).

Aplicada en: `sf:orquestacion` («Probar y cerrar») y `references/porque.md`; `sf:flujo_tareas` y `cola.py` (pasos de cierre); metodología, «Tareas y cola» («Probar y cerrar» y «El OK»).
