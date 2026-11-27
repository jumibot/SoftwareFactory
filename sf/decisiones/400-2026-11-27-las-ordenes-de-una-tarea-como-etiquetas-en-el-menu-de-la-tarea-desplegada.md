# Las órdenes de una tarea, como etiquetas en el menú de la tarea desplegada

Las órdenes de cada tarea van como etiquetas con su nombre, con mayúscula inicial y sin negrita, sobre fondo negro, en el menú de la tarea desplegada. La línea plegada no lleva ninguna, solo el ● del subagente. Toda tarea se puede desplegar y lleva la etiqueta «?», que pide a Claude que la explique.

Primero van las de la tarea, en verde, y al final la que destruye (Eliminar, Descartar o Revertir), en rojo. Después, las de sus pasos (Separar pasos, Paso +), con la letra atenuada. Las de dos clics confirman en la misma etiqueta: «¿Cerrar? sí». Cada paso pendiente lleva su «×», que confirma con «¿Quitar? sí», y su «?».

Qué órdenes hay y dónde sale cada una lo dice «Cómo funciona el panel», «Las órdenes de una tarea».

Recoge lo que sigue valiendo de «Las órdenes de cada tarea, en un menú de etiquetas» (168), «Toda tarea se despliega y lleva su etiqueta «?»» (173) y «Etiquetas «A Testing» en las tareas en curso y «Cerrar» en las de Testing» (182), que quedan deprecadas.

Porqué: el propietario de la Software Factory: «Cada vez hay más letras que memorizar lo que hacen. Lo convertimos en un menú (de etiquetas)» (168). Las letras reservaban ancho en todas las líneas.

Aplicada en: `plugins/sf/hooks/panel.tsx` (`etiquetaOrden` y el menú) y `estilo.ts` (`FONDO_ORDEN`, `COLOR_ORDEN_DESTRUCTIVA`), y sus pruebas.
