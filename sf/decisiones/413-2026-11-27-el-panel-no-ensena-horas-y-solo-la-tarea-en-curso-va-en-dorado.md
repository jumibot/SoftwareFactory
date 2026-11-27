# El panel no enseña horas, y solo la tarea en curso va en dorado

El panel no enseña horas ni antigüedades («ahora», «5 min», «3 h»), ni en las cabeceras ni en las filas. El número de la tarea en curso va en dorado, arriba y también en las secciones (084, 355). Su paso en curso, no: el dorado es solo para la tarea.

Recoge lo que sigue valiendo de «El panel, sin horas y con el amarillo solo arriba» (071), que queda deprecada.

Porqué: «· ahora» en la cabecera de Cerradas no decía nada que sirviera para decidir y ocupaba sitio; el color marca la tarea en curso, no cada línea suya (071).

Aplicada en: `plugins/sf/hooks/panel.tsx` y `estilo.ts` (`COLOR_TAREA`, `colorTareaDe`), y sus pruebas.
