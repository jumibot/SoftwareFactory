# La SF fija su mecanismo y se adapta al proyecto en el remoto, la rama de publicación, el idioma, los commits y el manifiesto

La SF fija su mecanismo, que es igual en todos los proyectos: la cola de tareas, una rama `feature/NN-nombre` por tarea desde `develop` (205), el número de la tarea en el commit, el registro de decisiones en `sf/decisiones/` (208) y sus documentos en `sf/` (399).

En lo demás se adapta a lo que el proyecto ya tiene, y lo guarda en `.sf/proyecto.json`: el remoto, la rama de publicación (`rama_main`), el idioma, el formato del commit y el manifiesto con la versión. Los documentos del proyecto no se mapean: si siguen la estructura de la SF, están donde los busca; si no, no los busca (229).

Recoge lo que sigue valiendo de «La SF fija el mecanismo y se adapta a las convenciones del proyecto» (202), que queda deprecada.

Porqué: incorporar un proyecto no debe reorganizarlo (201), y dejarlo todo con interruptores no lo cumplía. El propietario de la Software Factory eligió «fija el mecanismo, se adapta en todo lo demás» (202), y después sacó del «todo lo demás» las ramas (205), las decisiones (208) y el mapa de documentos (229).

Aplicada en: `plugins/sf/tools/configuracion.py` y `cola.py` (`convenciones`), `plugins/sf/hooks/configuracion.ts` y `contexto.ts` (la línea de convenciones), y sus pruebas; `sf:incorporar_proyecto_a_sf` («Lo fijo, lo que se detecta y lo que se elige») y `sf:configurar_proyecto`.
