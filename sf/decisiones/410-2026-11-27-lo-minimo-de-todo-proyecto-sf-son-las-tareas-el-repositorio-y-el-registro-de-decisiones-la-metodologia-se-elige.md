# Lo mínimo de todo proyecto SF son las tareas, el repositorio y el registro de decisiones; la metodología se elige

Al incorporar un proyecto, la SF gestiona siempre sus tareas (la cola y su flujo), su repositorio (una rama por tarea desde `develop`, squash al cerrar y publicación a `main` con su tag; 205) y su registro de decisiones, en `sf/decisiones/` (208). Esto no se elige. Lo que se elige es la metodología (fases y documentos): `.sf/proyecto.json` dice si el proyecto la sigue, y el panel enseña la fase solo si la sigue. La configuración se cambia después con `/sf_config`.

Recoge lo que sigue valiendo de «Configuración inicial: tareas y repo siempre, el resto opcional» (138) y «El registro de decisiones es obligatorio» (140), que quedan deprecadas.

Porqué: un proyecto puede querer la cola y el manejo del repositorio sin seguir el método. El propietario de la Software Factory: «Lo mínimo es que sf gestione las tareas y el repo. Esto siempre» (138); «Todos los proyectos sf registrarán las decisiones. No es opcional» (140).

Aplicada en: `sf:incorporar_proyecto_a_sf` y `sf:configurar_proyecto`; `plugins/sf/tools/configuracion.py` (`metodologia`); el panel (`plugins/sf/hooks/panel.tsx`, la fase).
