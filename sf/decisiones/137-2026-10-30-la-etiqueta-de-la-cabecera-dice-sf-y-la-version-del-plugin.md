# La etiqueta de la cabecera dice SF y la versión del plugin

- **Origen:** SoftwareFactory, 2026-10-30, tarea 181. El propietario pide «"SF" y la versión del plugin en la etiqueta de la cabecera» y, entre añadirla delante del nombre, ponerla debajo o sustituirlo, elige sustituir.
- **Contexto:** arriba a la derecha de la cabecera del panel iba el nombre del proyecto en mayúsculas, con el fondo del color de la sesión y letra negra. El nombre ya lo dicen la sesión y su color; qué versión de la SF está cargada no se veía en la cabecera fija.
- **Decisión:** la etiqueta dice «SF» y la versión del plugin que corre, la de su `plugin.json` (p. ej. «SF 1.0.0»), en lugar del nombre del proyecto; si no se puede leer, «SF» a secas. Mismo estilo: fondo del color de la sesión y letra negra; sin color, atenuada. Vale en todos los proyectos, la SF incluida, y también en uno sin SF: el panel es del plugin, que sí está cargado; que el proyecto no tiene SF ya lo dice «sin SF» bajo la cabecera.
- **Consecuencias:** el nombre del proyecto deja de estar en el panel. La línea bajo la cabecera de un proyecto con SF sigue diciendo con qué versión se incorporó y si va por detrás.
- **Aplicada en:** plugins/sf/hooks/panel.tsx y sus pruebas.
