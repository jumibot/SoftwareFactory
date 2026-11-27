# Los documentos de la SF van en la carpeta sf/ y su máquina en .sf/

En todo proyecto SF, `.sf/` es la máquina: `proyecto.json`, versionado, y la cola, el estado y el historial, fuera de git. `sf/`, en la raíz y visible, guarda los documentos de la SF: `sf/propuestas.md`, `sf/informes/` y `sf/decisiones/` (208). Sus rutas son fijas (229).

Un proyecto incorporado antes los pasa a `sf/` al ponerse al día, con el OK del propietario; mientras tanto, la SF los sigue leyendo en `docs/`. Es la excepción acordada a «Incorporar un proyecto no mueve ni renombra nada» (201).

Recoge lo que sigue valiendo de «Los documentos de la SF van en la carpeta sf/» (203), que queda deprecada.

Porqué: en el `docs/` del proyecto chocaban con los suyos (JKanban lo tiene en inglés, OncoCore usa `_docs/`), y dentro de `.sf/` se esconden: ripgrep se salta las carpetas con punto, Obsidian no las ve y en macOS y Linux no salen en el explorador. El propietario de la Software Factory: «una carpeta sf en la raíz para las cosas de la SF, en todos los proyectos SF, así nos evitamos choques de partida» (203).

Aplicada en: `plugins/sf/tools/cola.py` (`PROPUESTAS`, `DECISIONES`), `indice_decisiones.py` y `plugins/sf/hooks/lectura.ts` (`RUTAS_PROPUESTAS`), y sus pruebas; `sf:incorporar_proyecto_a_sf`; `sf:informe_deliberativa` («Dónde va»).
