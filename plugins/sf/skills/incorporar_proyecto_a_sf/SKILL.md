---
name: incorporar_proyecto_a_sf
description: Prepara un proyecto para trabajar con la Software Factory (SF) sin cambiarlo — operación sin tarea, guiada por menús en la línea de prompts — identidad y configuración en .sf/proyecto.json (nombre, color de sesión, descripción breve, metodología, kanban si se elige, idioma, formato de commit, línea de coautoría, remoto de GitHub, rama de publicación y manifiesto con versión, detectados y confirmados), remoto en GitHub obligatorio (si no hay ninguno, se crea con gh; fuera de GitHub no hay SF), ramas develop y main, estado inicial, cola de peticiones, .gitignore, CLAUDE.md sin líneas de la SF (las reglas y la orquestación las entrega el mod; al actualizar, se quitan la copia .sf/claude-sf.md y su importación) y los documentos de la SF en sf/ (sf/propuestas.md, sf/decisiones/ una decisión por archivo, sf/informes/). No mueve ni renombra nada del proyecto; al poner al día, pasa a sf/ los documentos de la SF y las decisiones antiguas. Cubre cuatro casos — proyecto nuevo, proyecto existente anterior a la SF, actualizar uno ya incorporado a la versión actual de la SF y diagnosticar qué le falta sin cambiar nada. Úsala cuando pidan incorporar, adaptar o preparar un proyecto para la SF, ponerlo al día con la SF, o revisar si cumple lo que la SF necesita. Cambiar después la configuración de un proyecto ya incorporado es de `sf:configurar_proyecto` (/sf_config).
---

# Incorporar un proyecto a la SF

La skill prepara el proyecto de la sesión para la SF: le da identidad, ramas, estado y cola, y el sitio de los documentos de la SF. Las reglas de la SF y `sf:orquestacion` no se escriben en el proyecto: las entrega el mod del plugin al empezar la sesión, tras `/clear` y tras compactar, siempre en la versión instalada. El método está en la skill `sf:metodologia`.

**Una operación, sin tarea.** Incorporar, poner al día y pasar a `sf/` no se anotan en la cola, no crean tarea ni rama y no pasan por el panel («Incorporar un proyecto es una operación sin tarea, guiada por menús», 209). Claude la lleva desde la línea de prompts, con menús (la herramienta de preguntas con opciones) y mensajes cortos: dice qué va a crear, mover o cambiar, pide el OK del propietario y lo aplica en `develop`, con su commit. Lo que salga mal se deshace con git.

**Un proyecto por sesión.** La skill trabaja siempre sobre el proyecto de la carpeta de la sesión. Si esa carpeta es el repositorio de la propia SF, o el proyecto que se quiere incorporar es otro, no se hace nada: se dice en una línea y se propone abrir una sesión en ese proyecto.

**Nada del proyecto se mueve.** La SF no renombra carpetas ni archivos, ni cambia de sitio documentos, assets ni ningún otro contenido del proyecto («Incorporar un proyecto no mueve ni renombra nada», 201). Lo que necesita lo usa donde ya está o lo añade con lo mínimo; lo que el proyecto ya tiene, sobre todo su `CLAUDE.md`, se conserva. Reorganizar algo del proyecto es una petición aparte del propietario, nunca parte de la incorporación. La única excepción es pasar a `sf/` los documentos de la SF y las decisiones (paso 7), siempre con el OK del propietario.

**Lo fijo, lo que se detecta y lo que se elige** («La SF fija el mecanismo y se adapta a las convenciones del proyecto», 202; el diseño, en el informe «Configuración inicial» de la tarea 263):

- **Fijo, sin campo ni pregunta:** la cola, el modelo de ramas (`develop`, una rama `feature/NN-nombre` por tarea, squash al cerrar y publicación de `develop` a la rama que hace de `main`, «El manejo del repositorio no se negocia: siempre develop», 205), un remoto en GitHub («Sin remoto en GitHub no hay SF: se valida al incorporar y, si falta, se crea», 230), los commits, que los hace siempre Claude («Los commits los lleva siempre Claude», 225), la versión con su tag `vX.Y.Z` («La versión forma parte del manejo del repositorio», 226), las decisiones en `sf/decisiones/` («Las decisiones son material de la SF: siempre en sf/decisiones/», 208) y las reglas comunes, que entrega el mod. Negarse a `develop`, al remoto o a que Claude lleve los commits es no usar la SF: se explica y se pide reconfirmar (paso 2).
- **Se detecta y se confirma:** el idioma, el formato del commit (y con él la marca del número de la tarea), la línea de coautoría de los commits, el remoto de GitHub, la rama que hace de `main` y el manifiesto con versión (pasos 2 y 8).
- **Se elige:** la metodología y el kanban (pasos 1 y 8).

No hay mapa de documentos: si el proyecto sigue la estructura documental de la SF, sus documentos están donde la SF los busca; si no la sigue, no se mapean, y la incorporación no pregunta rutas («Sin mapa de documentos: o se sigue la estructura de la SF, o no se mapea», 229).

**Detectar con comandos.** Lo que se detecta lo da `python -I -X utf8 <plugin>/tools/configuracion.py detectar` (remotos y si son de GitHub, a cuál siguen `develop` y la rama de publicación, las ramas `main`, `master` y `develop`, los manifiestos con versión, la forma de los últimos 50 commits y su línea de coautoría más usada, y los colores de los proyectos vecinos), y lo que vale y falla de `.sf/proyecto.json`, `configuracion.py ver`; los dos solo leen y los usa también `sf:configurar_proyecto`. Si el mod dice al empezar la sesión que en esta máquina Python se lanza con otro nombre (en macOS, `python3`), estas órdenes van con ese («La orden de Python sale del intérprete que se detecta», 236). El idioma lo dice Claude leyendo el README, el `CLAUDE.md` y los commits.

**Menús de hasta cuatro preguntas.** Se pregunta con la herramienta de menús, la opción recomendada primero y con lo que la delata (por ejemplo, «Conventional (41 de los últimos 50 commits)»). Lo que se detecta sin duda no se pregunta: se enseña en el resumen antes del OK. Cada menú lleva solo las preguntas que hacen falta; si se quedan en cero, no se muestra. Son tres, por este orden: identidad (paso 1), repositorio (paso 2) y convenciones (paso 8); si a uno le salen más de cuatro, la última va en un menú aparte justo después.

## Los cuatro casos

Antes de tocar nada, se deduce el caso mirando el proyecto y se presenta al propietario en un menú, en el que la primera opción es el caso detectado, marcado como recomendado y con lo que lo delata (por ejemplo: «sin `.sf/`, con un `CLAUDE.md` de 553 líneas»). La otra opción es «Solo diagnosticar, sin cambiar nada». Si el propietario ya ha nombrado el caso en su petición («diagnostica», «actualiza a la SF»), no se pregunta. Los casos son estos:

- **Nuevo:** carpeta vacía o casi vacía, sin `.sf/`. Se crea todo.
- **Existente:** proyecto con código o documentos, pero sin `.sf/`. Se incorpora sin rehacer lo que ya funciona (metodología, 2, «Proyectos anteriores a la SF»).
- **Actualizar:** el proyecto ya tiene `.sf/proyecto.json` (o el antiguo `docs/sf.json`). Se pone al día con la versión actual de la SF (abajo, «Actualizar»).
- **Diagnosticar:** el propietario lo elige en el menú o pide revisar sin cambiar nada. Se hace la comprobación final y se da el informe. No se escribe nada.

En el caso existente y en el de actualizar, el diagnóstico va primero: así se ve qué falta antes de proponer cambios.

## Nuevo y existente

1. **Diagnóstico.** En el caso existente, la comprobación final (abajo) dice qué falta. En el nuevo, falta todo.
2. **Lo que solo da el propietario, en tres menús.** Identidad (paso 1 del procedimiento), repositorio (paso 2: rama de publicación, `develop`, remoto en GitHub y commits de Claude) y convenciones (paso 8: idioma, formato de commit, manifiestos, kanban y coautoría), con lo detectado como opción recomendada. Si el propietario se niega a `develop`, al remoto o a que Claude lleve los commits y lo reconfirma, se para sin cambiar nada. Si los remotos están todos fuera de GitHub, se para antes de preguntar nada más (paso 2).
3. **Lo que va a cambiar, y el OK.** Una lista corta: cada archivo o carpeta que se crea o se edita, con el cambio (por ejemplo, «`.gitignore`: se añaden 8 líneas» o «`sf/propuestas.md`: nuevo, vacío»), las ramas y el remoto que se crean, y la configuración confirmada, con lo detectado sin preguntar. Se pide la autorización en un menú: «Aplicar» o «No aplicar». Lo que necesita una decisión aparte (los choques del `CLAUDE.md`, paso 5, y pasar a `sf/` las decisiones que ya tuviera el proyecto, paso 7) no entra en ese OK: se propone después, cada cosa con su menú.
4. **Aplicar en `develop`.** Con el OK, se aplican los pasos del procedimiento en `develop`, sin rama de tarea, y se hace su commit (paso 9). Si hay cambios sin commit en los archivos que se van a tocar, se dice y no se aplica hasta que estén resueltos.
5. **Comprobar e informar.** Se repite la comprobación final y se dice, en pocas líneas, qué ha cambiado, el commit y qué mirar («Al terminar»). No queda nada en la cola.

## Actualizar

Poner un proyecto al día no se anota en la cola ni crea tarea ni rama: el proceso ya está probado en la SF (decisiones «Poner un proyecto al día con la SF, sin tarea», 199, y 209). No se manda al propietario al panel.

1. **El plugin, al día.** Se miran tres versiones de `sf`, con comandos:
   - la que corre: la `version` del `plugin.json` de la carpeta de esta skill (`<plugin>/.claude-plugin/plugin.json`);
   - la instalada: la de `sf@softwarefactory` en `~/.claude/plugins/installed_plugins.json` (con `CLAUDE_CONFIG_DIR`, en su `plugins/`), en cada scope que usa el proyecto (`user`, y `project` o `local` con su `projectPath`);
   - la publicada: el tag `vX.Y.Z` más alto de `git ls-remote --tags` del repositorio del catálogo `softwarefactory` (su `source` en `known_marketplaces.json`).

   Si la publicada es más nueva que la instalada, se ofrece en un menú: «Actualizar el plugin a la X (recomendado)» o «Seguir con la Y». Con el OK, se ejecutan, desde la carpeta del proyecto, `claude plugin marketplace update softwarefactory`, `claude plugin update sf@softwarefactory --scope <scope>` en cada scope atrasado y `claude plugin install <dependencia> --scope <scope>` por cada una de las `dependencies` del `plugin.json` nuevo que no esté instalada, una orden por dependencia (la orden instala solo la primera que se le da). Si una falla, se dice con su orden y no se sigue: sin una dependencia, `sf` no carga.

2. **Refrescar la sesión.** Si la instalada es ahora más nueva que la que corre, la sesión sigue con el mod y las skills viejos. Claude no puede lanzar una orden de barra: se lo pide al propietario en un mensaje corto, con la orden en su línea, y termina el turno. «Escribe `/reload-plugins` y después pídeme otra vez «pon el proyecto al día con la SF».» `/reload-plugins` carga la versión instalada, con su mod y sus skills, sin reiniciar. Si tras recargar el plugin no carga (`/plugin` lo da como «failed to load») o sus skills salen como desconocidas, se pide reiniciar Claude Code. Al volver, se repite el paso 1, que ya no tiene nada que hacer, y se sigue con la skill nueva.

3. **Diagnóstico.** La comprobación final (abajo) dice qué falta.

   - **Remoto en GitHub** (230): se comprueba como al incorporar (paso 2 del procedimiento). Si el `remoto` de `.sf/proyecto.json` no existe o no apunta a GitHub (el panel lo avisa), se corrige con el que haya de GitHub; si no hay ninguno, se ofrece crearlo; si solo los hay fuera de GitHub, se explica que la SF solo trabaja con GitHub y no se sigue.
   - **Configuración:** se escriben los campos que falten con lo detectado (paso 8), en un solo menú con lo que tenga duda; lo detectado sin duda se enseña en el informe. La cadena antigua de `kanban` (`"kanban": "JKanban"`) pasa a bloque (`{ "proveedor": "jkanban", "proyecto": "JKanban" }`). Un valor que no se entiende (el panel lo avisa) se vuelve a detectar y se confirma.

4. **Informe y OK.** Se dice al propietario qué va a cambiar, en una lista corta: cada archivo que se crea, se borra o se edita, con el cambio (por ejemplo, «`CLAUDE.md`: se quita la línea `@.sf/claude-sf.md`» o «`.sf/proyecto.json`: `sf` de 1.3.0 a 1.4.2»). Se pide la autorización en un menú: «Aplicar» o «No aplicar». Lo que necesita una decisión aparte (los choques del `CLAUDE.md`, paso 5 del procedimiento, y pasar a `sf/` los documentos de la SF y las decisiones, paso 7) no entra en ese OK: se propone después, cada cosa con su menú.

5. **Aplicar en `develop`.** Con el OK, se aplican los pasos del procedimiento que hagan falta en `develop` del proyecto, sin rama, y se hace su commit (paso 9). Si la sesión está en otra rama, se pasa a `develop`; si hay cambios sin commit en los archivos que se van a tocar, se dice y no se aplica hasta que estén resueltos.

6. **Comprobar que ya no va atrasado.** Se repite la comprobación final y se mira lo mismo que mira el aviso de atraso: `sf` de `.sf/proyecto.json` tiene el mismo mayor.menor que la versión que corre, y ni `CLAUDE.md` ni `.claude/CLAUDE.md` tienen la línea `@.sf/claude-sf.md`. Si algo falla, se dice y se arregla antes de terminar.

7. **Las reglas nuevas, con `/clear`.** El mod entrega las reglas y la orquestación al empezar la sesión, tras `/clear` y tras compactar; la conversación en curso sigue con las de antes (o con la copia `.sf/claude-sf.md`, si se acaba de quitar). Si el plugin se ha actualizado o se ha quitado la importación, se pide en el mismo mensaje del informe: «Escribe `/clear` para que entren las reglas nuevas.»

8. **Informe.** En pocas líneas: qué ha cambiado, los commits, la versión con la que queda y que el aviso de atraso desaparece. No queda nada en la cola.

9. **Cambiar la configuración.** Tras el informe, se enseña la configuración con que queda (`configuracion.py ver`) y se ofrece cambiarla en un menú: «Así está bien» o «Cambiar algo de la configuración». Con la segunda, se sigue con `sf:configurar_proyecto` desde su paso 2, sin volver a enseñarla (228). Lo mismo se puede pedir después con `/sf_config`.

## Procedimiento

1. **Identidad (menú 1).** Se pregunta lo que falte de `.sf/proyecto.json`, con un valor propuesto sacado del proyecto (su README, el nombre de la carpeta o del repositorio). Lo que ya está no se pregunta.
   - `proyecto`: el nombre, tal como se escribe (con acentos y mayúsculas).
   - `descripcion`: una línea de 120 caracteres como mucho que diga qué es el proyecto, por defecto la primera frase del README. La lee el panel (y el kanban, si se elige).
   - `color`: el color de sus sesiones, uno de `red`, `blue`, `green`, `yellow`, `orange`, `pink` o `cyan`, con dos o tres libres como opciones. `purple` es de la SF. Se recomienda uno que no usen los otros proyectos, mirando los `.sf/proyecto.json` de las carpetas vecinas (solo lectura).
   - `metodologia`: «¿Seguir la metodología: fases y documentos del método?», con «Sí» y «No: solo tareas, repositorio y decisiones». Por defecto, «Sí» en un proyecto nuevo y «No» en uno existente, salvo que tenga visión o especificación. Sin metodología, el mod no entrega las reglas del método y el panel no pinta la fase ni pide `estado.json`.
   - `sf`: no se pregunta: la versión del plugin `sf` instalado, tomada de su `plugin.json`, no de memoria.

   El mod de estado aplica el color y el nombre a la sesión (`/color` y `/rename`) en cuanto lee el archivo.

2. **Repositorio (menú 2): rama de publicación, `develop`, remoto en GitHub y commits.** La SF trabaja siempre con su modelo de ramas (205), un remoto en GitHub (230) y sus commits (225). Antes del menú:
   - **Sin repositorio git:** se propone crearlo (`git init -b main`) con un primer commit de lo que ya hay. En una carpeta vacía no hay nada que poner en él: es un commit vacío (`git commit --allow-empty`), con un título como «Inicio del repositorio» en el idioma del proyecto, para que exista `main` y de ella salga `develop`.
   - **git sin identidad:** si `git config user.name` o `git config user.email` no dan nada (pasa en un equipo recién estrenado), ningún commit sale. Se dice antes del menú y se piden el nombre y el correo al desarrollador, con dónde guardarlos: «Solo en este proyecto» (`git config`, recomendado) o «Para todos tus proyectos» (`git config --global`). Se ponen con su OK.
   - **Remotos fuera de GitHub:** con `git remote -v`, solo cuenta un remoto cuya url apunte a `github.com` (`https://github.com/…`, `git@github.com:…`). Si el proyecto tiene remotos y ninguno es de GitHub (GitLab u otro), no hay menú: se explica que, por ahora, la SF solo trabaja con GitHub y que hay que pasar el proyecto allí, y se para sin cambiar nada. No se crea uno de GitHub a su lado (230, precisada el mismo día).

   El menú, con solo las preguntas que hagan falta:

   | # | Pregunta | Opciones (la recomendada, primero) | Se salta si |
   | --- | --- | --- | --- |
   | 1 | ¿`master` hace de `main`? | «`master` hace de `main`» / «Crear `main` desde `master`» | Hay `main`, o no hay rama principal |
   | 2 | ¿Crear `develop` desde `<rama_main>`? | «Crear `develop`» / «No crear» | Ya existe `develop`, en local o en el remoto |
   | 3 | Con varios remotos de GitHub: ¿a cuál se hace push? Sin ninguno: ¿crear `<cuenta>/<proyecto>` en GitHub? | Varios: cada uno, primero el que siguen `develop` o la rama de publicación (`git config branch.<rama>.remote`). Ninguno: «Crear privado» / «Crear público» / «No crear» | Hay uno de GitHub: se usa |
   | 4 | Los commits los hace Claude, con tu OK en cada cierre y publicación | «De acuerdo» / «No usar la SF aquí» | El `CLAUDE.md` no dice que los lleve el desarrollador: entonces solo se cuenta en el resumen |

   - **Rama de publicación** («Si el proyecto tiene master, se pregunta si hace de main», 213): si el proyecto tiene `main`, es la suya. Si su rama principal se llama de otra forma (`master`, por ejemplo), con la primera opción la SF publica en ella y no se crea `main`; con la segunda, se crea `main` desde ella, y la suya queda como estaba, sin borrarla ni renombrarla (201). Se guarda en `rama_main`. Si esa rama solo existe en el remoto (por ejemplo, `github/main` sin `main` local), se crea la local siguiéndola (`git branch --track <rama> <remoto>/<rama>`), sin preguntar, y se dice en el resumen («Si main solo está en el remoto, se crea la local sin preguntar», 234). Igual con `develop`: si solo está en el remoto, se crea la local siguiéndola, sin preguntar, y la pregunta de crearla no sale.
   - **Remoto:** el nombre del remoto de GitHub elegido se guarda en `remoto`. Para crearlo hace falta `gh` instalado y con la sesión iniciada (`gh auth status`); si no, se dice cómo (instalarlo: en macOS, `brew install gh`; en Windows, `winget install GitHub.cli`; y `gh auth login`, aceptando que configure git) y se espera: sin remoto no se sigue. Se crea, tras el OK, con `gh repo create <cuenta>/<proyecto> --private --source . --remote origin` (o `--public`), y `remoto` vale `origin`. Solo se ofrece crearlo si el proyecto no tiene ningún remoto.
   - **Reconfirmar** («Sin develop no hay SF, y las decisiones mezcladas se sacan con enlace», 214; 225; 230). Con «No crear» `develop`, «No crear» el remoto o «No usar la SF aquí», un menú propio explica por qué la SF no funciona sin ello (de `develop` salen y a ella vuelven todas las tareas; el cierre y la publicación hacen push al remoto; el squash, el revert y la publicación son commits de Claude) y ofrece «Crear `develop`», «Crear el remoto» o «De acuerdo», frente a «No usar la SF en este proyecto». Con la segunda, se para sin haber cambiado nada: ni `.sf/` ni ningún otro archivo.

   Las ramas se crean en local y se suben al remoto con el commit final (paso 9). Si el push pide usuario y contraseña, git no tiene las credenciales de `gh`: `gh auth setup-git` las configura.

3. **Estado y cola.** Con metodología, se crea `.sf/estado.json` con la fase real del proyecto. En uno nuevo, la fase es `vision` y `hechas` queda vacío. En uno existente, `hechas` lleva solo las fases cubiertas de verdad, y los documentos que faltan (la visión, la especificación funcional, las guías) van a `pendientes`. Sin metodología, no se crea. `.sf/estado.json`, `.sf/peticiones.json`, `.sf/peticiones.lock`, `.sf/historial.jsonl`, `.sf/copias/` (lo que escribe el CLI `cola.py`), `.sf/subagentes.json` (lo que el panel sabe de los subagentes de cada sesión), `.claude/worktrees/` (los worktrees de los subagentes) y `sf/decisiones/README.html` (el índice de las decisiones en html, que se genera a mano con `indice_decisiones.py --html`) se añaden al `.gitignore`; `proyecto.json` sí se versiona. Si existía `docs/sf.json`, sus datos pasan a `.sf/` y el archivo antiguo se borra con `git rm`.

4. **Reglas de la SF, sin tocar el `CLAUDE.md`.** Las reglas que la SF distribuye (las comunes de `templates/claude-sf.md` del plugin y, si el proyecto sigue la metodología, las de `templates/claude-sf-metodologia.md`), una línea con sus convenciones (las de `.sf/proyecto.json`, paso 8) y el texto de `sf:orquestacion` los entrega el mod de la SF como contexto al empezar la sesión, tras `/clear` y tras compactar, en los proyectos con `.sf/proyecto.json`. El proyecto no lleva copia ni línea de la SF en su `CLAUDE.md`. Si no hay `CLAUDE.md`, se crea solo con el título del proyecto y su descripción, para lo propio del proyecto.

   La orquestación se apaga con `"automatizaciones": { "orquestacion": false }` en `.sf/proyecto.json`; entonces la carga el principal. Las reglas no se apagan.

   **Al actualizar** un proyecto incorporado con una SF anterior: se borra la copia `.sf/claude-sf.md` con `git rm` y se quita del `CLAUDE.md` (o de `.claude/CLAUDE.md`) la línea `@.sf/claude-sf.md`, sin tocar lo demás. Mientras la línea siga, el mod entrega solo la orquestación, para no dar las reglas dos veces, y el panel avisa de que el proyecto va atrasado. Un apartado «Software Factory» escrito a mano dentro del `CLAUDE.md`, como el de las primeras incorporaciones, repite las reglas: se propone quitarlo (paso 5). Se enseña el cambio antes de escribirlo.

5. **Lo que choca con la SF en un `CLAUDE.md` existente.** Se lee el `CLAUDE.md` entero y se hace una lista de los puntos donde se cruza con la SF. Por ejemplo: otra forma de registrar decisiones, otra regla sobre dónde va cada cosa (memoria, `CLAUDE.md`, skills) o un apartado «Software Factory» escrito dentro del propio `CLAUDE.md`, como el de las primeras incorporaciones. Que el proyecto tenga sus documentos en otra carpeta (`_docs/`, `doc/`) no es un choque: la SF no los mapea (229). Los choques no se resuelven solos. Se presentan al propietario uno por uno, en un menú con una recomendación, y cada decisión se anota en `sf/decisiones/`. Mientras no se decide, manda la regla del proyecto, porque es la que conoce su dominio.

   Si alguna sección del `CLAUDE.md` tendría mejor sitio en un documento (decisiones de arquitectura, procedimientos de despliegue), se dice como sugerencia. Moverla es una petición aparte del propietario (201), que se anota en la cola si la quiere.

   **`CLAUDE.md` complejo** (acuerdo del propietario, 2026-10-28). Cuando el `CLAUDE.md` es largo o tiene muchas reglas propias (por ejemplo, uno con principios inviolables, reglas de arquitectura y de despliegue), la revisión de los choques no se hace dentro de la incorporación. Es una tarea aparte que ocupa una sesión entera y estudia en detalle cada cambio antes de hacerlo. La incorporación hace solo lo que no toca ese contenido y propone anotar esa tarea en la cola, con el número de reglas y de choques detectados. En esa sesión se trabaja así:
   - un cambio cada vez, con el texto actual, el propuesto y por qué;
   - se aplica solo con el OK del propietario, y cada cambio va en su propio commit;
   - antes de proponer cada cambio, se comprueba que no se pierde ninguna regla.

6. **Los documentos de la SF, en `sf/`.** Lo que la SF escribe en el proyecto va en la carpeta `sf/` de su raíz, visible y versionada, al lado del contenido del proyecto («Los documentos de la SF van en la carpeta sf/», 203). `.sf/` es la máquina; `sf/`, los documentos:
   - **`sf/decisiones/`**, con su índice: `python -I -X utf8 <plugin>/tools/indice_decisiones.py sf/decisiones` escribe `README.md` con la forma de registrar las decisiones, un archivo por decisión. Se añade al `.gitattributes` la línea `sf/decisiones/README.md merge=union`, para que dos ramas no choquen en el índice.
   - **`sf/propuestas.md`**, copiando `templates/propuestas.md` del plugin, con su «## Propuestas pendientes» vacía. Ahí van las propuestas del proyecto, y el panel las muestra en su sección Propuestas (decisión 196). Si ya existe, no se toca.
   - **`sf/informes/`**, para los informes que Claude escriba en el proyecto (análisis, auditorías, diagnósticos). Se crea con el primero, porque git no guarda carpetas vacías.

   Los documentos del proyecto (visión, especificación, guías) no se crean ni se mueven en la incorporación, y no se preguntan sus rutas: si siguen la estructura documental de la SF, están donde la SF los busca; si no, no se mapean (229). En un proyecto nuevo, se crean cuando toque escribirlos, según la metodología.

7. **Pasar a `sf/` lo que ya había.** En el caso existente y al actualizar, los documentos de la SF que estén en otro sitio y las decisiones que el proyecto ya tuviera se pasan a `sf/` (decisiones 203 y 208, la excepción de la 201). Se enseña al propietario la lista, con cada origen y su destino, en un menú: «Pasar todo a `sf/` (recomendado)», «Elegir uno por uno» o «Ahora no». Si se aplaza, queda en `pendientes` de `estado.json`, y el panel y `cola.py` siguen leyendo el sitio de antes. No se hace si hay trabajo en curso que pueda chocar (cambios sin commit, ramas de tareas abiertas que toquen esos archivos): se dice y queda en `pendientes`.
   - **`docs/propuestas.md`** → `git mv docs/propuestas.md sf/propuestas.md`.
   - **`docs/decisiones/`** → `git mv docs/decisiones sf/decisiones`. La línea de `.gitattributes` pasa a `sf/decisiones/README.md merge=union`, y la del `README.html` en `.gitignore`, a `sf/decisiones/README.html`. Se regenera el índice, que conserva lo que hay antes de «Índice».
   - **El antiguo `docs/decisiones.md`** (una sección «### Título» por decisión) → `python -I -X utf8 <plugin>/tools/indice_decisiones.py sf/decisiones --migrar docs/decisiones.md`: cada sección pasa a su archivo, con el mismo texto y sus enlaces rehechos desde la carpeta nueva, y el antiguo se borra. `git add sf/decisiones docs/decisiones.md` deja en el commit los archivos nuevos y el borrado.
   - **Decisiones en otra forma** (por ejemplo, un `decisiones-y-pendientes.md` con una lista por fecha, o una carpeta `adr/`) → Claude escribe cada decisión en su archivo de `sf/decisiones/`, con el nombre que da `indice_decisiones.py sf/decisiones --nombre "Título" --fecha <fecha>`, el texto literal en «Decisión», la fecha y el proyecto en «Origen» y, en «Contexto», de qué archivo viene. Se enseña la lista de títulos antes del OK. Si el archivo de origen solo tenía decisiones, se borra con `git rm`; si tiene más cosas (por ejemplo, los pendientes), se queda, y su sección de decisiones se cambia por un enlace a `sf/decisiones/`.
   - **Informes de la SF** que estén en `docs/` (por ejemplo, en `docs/referencias/reports/`) → `git mv` a `sf/informes/`, con los `.html` generados junto a su `.md`. Se proponen solo los que escribió la SF; los del proyecto no se tocan.

   Después de mover, se buscan con `git grep` los enlaces a las rutas antiguas (en el `CLAUDE.md`, los documentos y las propias decisiones) y se rehacen. El informe dice cuántos enlaces se han cambiado.

8. **Convenciones (menú 3) y configuración.** Se detectan con comandos y se confirman en un menú; lo que se detecta sin duda no se pregunta:

   | # | Pregunta | Opciones (la recomendada, primero) | Por defecto | Se salta si |
   | --- | --- | --- | --- | --- |
   | 1 | ¿En qué idioma escribe Claude commits, tareas y documentos? | El detectado / español / inglés | El del README, el `CLAUDE.md` y los últimos commits | Proyecto nuevo: el de la conversación |
   | 2 | ¿Cómo son los commits? | «Conventional, con `SF-Tarea: N` al pie» / «Como los de ahora (`<ejemplo>`), con `SF-Tarea: N`» / «Libres, con `(N)` al final» | Conventional si lo sigue la mayoría de los últimos 50 títulos (`git log -50 --format=%s`); propio si comparten otra forma fija; si no, libres | Proyecto nuevo: libres |
   | 3 | ¿Qué manifiestos suben de versión al publicar? | Cada uno (selección múltiple) / «Ninguno: solo el tag» | Todos los detectados | Hay uno (se usa) o ninguno |
   | 4 | ¿Kanban? | «Ninguno» / «JKanban: `<proyecto>`» | «Ninguno» («El kanban se elige, y por defecto ninguno», 224) | — |
   | 5 | ¿Con qué línea de coautoría firma Claude sus commits? | «La de esta sesión: `Co-Authored-By: Claude <modelo> <noreply@anthropic.com>`» / «Sin línea de coautoría» | La de esta sesión, con el modelo con que trabaja Claude ahora | Más de la mitad de los últimos 50 commits llevan la misma (`detectar`, «Coautoría»): se usa esa |

   - **Idioma** («Claude escribe en el idioma del proyecto y del desarrollador», 206): `idioma`, con su código corto (`es`, `en`, `ca`…).
   - **Commits** («El número de la tarea en el commit, según el formato del proyecto», 207): `commits` vale `libre`, `conventional` o `propio`, y de él sale la marca del número: con `libre`, «(N)» al final del título; con `conventional` o `propio`, el trailer `SF-Tarea: N` al pie. `propio` es un formato estricto sin nombre: Claude imita los títulos de los últimos commits del proyecto. En los dos, el squash de cierre lleva el prefijo del tipo de tarea (implementar, `feat`; corregir, `fix`; los que entregan documentos, `docs`; sin tipo, `chore`) seguido del título de la tarea («El título del commit en formato conventional sale del tipo de tarea», 233). Un título es conventional si empieza por `tipo(ámbito)?!?: ` con un tipo de los habituales (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`…).
   - **Manifiestos** («La versión forma parte del manejo del repositorio», 226): se buscan en la raíz y un nivel por debajo los `package.json`, `pyproject.toml` y `.claude-plugin/plugin.json` con versión. `manifiesto` es una ruta, una lista de rutas o `null` (solo el tag). Otros formatos (`pom.xml`, `Cargo.toml`, Gradle) aún no se soportan: se dice y no se guardan. Un archivo con la versión en el código (como `backend/main.py`) no es manifiesto. Al publicar, RELEASE pone la versión del tag en cada uno, en un commit `vX.Y.Z`.
   - **Coautoría** («La firma del commit de cierre es configurable; sin configurar, sin línea», 238): `coautor` es la línea que llevan al pie el squash de cada cierre, las decisiones, la versión de RELEASE y los commits de los subagentes, con `Co-Authored-By: ` delante (si se escribe sin él, se añade). Sin `coautor`, o con `null`, van sin línea de coautoría. Con «Other» se escribe otra.
   - **Kanban:** `kanban` es un bloque, `{ "proveedor": "jkanban", "proyecto": "<proyecto>" }`, o no está. Mientras JKanban no esté conectado, el proyecto **no se crea** en el kanban: crearlo queda en los pendientes del informe, y no se afirma que exista.
   - **`remoto` y `rama_main`** salen del paso 2.
   - **`automatizaciones`** no se pregunta: todo encendido salvo que se apague; solo aparece si se apaga algo.

   **Se escribe siempre lo confirmado**, aunque coincida con el valor por defecto, salvo `automatizaciones`. Por ejemplo, un proyecto sin metodología y con su propio remoto:

   ```json
   {
     "sf": "1.5.0",
     "proyecto": "Contador",
     "descripcion": "Cuenta las visitas de una tienda con un sensor en la puerta",
     "color": "green",
     "metodologia": false,
     "idioma": "es",
     "commits": "libre",
     "remoto": "github",
     "rama_main": "main",
     "manifiesto": null,
     "coautor": "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
   }
   ```

   Cambiar la configuración después es de la skill `sf:configurar_proyecto`, con la orden `/sf_config` o pidiéndoselo a Claude («La configuración se cambia pidiéndoselo a Claude, con menús», 228).

9. **Commit y push.** Todo lo de la incorporación va en un commit propio en `develop`: `Incorporado a la SF <versión>`, o `Actualizado a la SF <versión>`, en el idioma y el formato del proyecto (con conventional commits, por ejemplo, `chore: incorporado a la SF <versión>`). No es de ninguna tarea: no lleva número. El paso a `sf/` del paso 7 va en otro commit, `Documentos de la SF a sf/`, para que se pueda deshacer aparte. Los commits los hace Claude, siempre (225). Después se suben `develop` y la rama de publicación al `remoto` (`git push -u <remoto> develop <rama_main>`); si el push falla, se dice con su orden y lo local queda hecho.

## Comprobación final y diagnóstico

Se revisa lo siguiente, y es también el informe del caso «diagnosticar». La parte de `.sf/proyecto.json`, el remoto, las ramas y los manifiestos la da `configuracion.py ver`:

- `.sf/proyecto.json` existe, es válido y tiene `proyecto`, `descripcion`, `color` (no `purple`) y `sf`, y la configuración con valores válidos: `metodologia` (`true` o `false`), `idioma`, `commits` (`libre`, `conventional` o `propio`), `remoto`, `rama_main`, `manifiesto` (ruta `.json` o `pyproject.toml`, lista de rutas o `null`) y `coautor` (una línea o `null`). Lo que falta vale lo de por defecto, pero al incorporar y al poner al día se escribe. `kanban` es opcional: sin él no falla nada; si está, en bloque (`{ "proveedor": "jkanban", "proyecto": "…" }`); en cadena, es la forma antigua y se reescribe.
- El proyecto es un repositorio git con `develop` y su rama de publicación (`rama_main`: `main`, u otra que haga de `main`).
- El `remoto` existe y apunta a `github.com` (230), y `develop` y la rama de publicación están subidas a él.
- Con metodología, `.sf/estado.json` es válido y tiene una fase conocida. Está fuera de git, igual que `.sf/peticiones.json`, `.sf/peticiones.lock`, `.sf/historial.jsonl`, `.sf/copias/`, `.sf/subagentes.json`, `.claude/worktrees/` y `sf/decisiones/README.html`.
- No queda `.sf/claude-sf.md`, ni la línea `@.sf/claude-sf.md` en el `CLAUDE.md` o en `.claude/CLAUDE.md`, ni un apartado «Software Factory» escrito dentro que repita las reglas: las entrega el mod.
- `sf/decisiones/` existe, con su índice al día (regenerarlo no cambia nada) y la línea `merge=union` en `.gitattributes`.
- `sf/propuestas.md` existe y tiene «## Propuestas pendientes»: sin ella, el panel no muestra las propuestas ni `cola.py` puede pasar una tarea a propuesta.
- No quedan documentos de la SF ni decisiones fuera de `sf/`: `docs/propuestas.md`, `docs/decisiones/`, `docs/decisiones.md` u otro registro de decisiones del proyecto. Si quedan, es lo que propone el paso 7.
- No queda `docs/sf.json`.
- Con metodología, lo que la metodología espera y el proyecto no tiene (guías de instalación y de actualización, visión, especificación funcional) se anota como pendiente, no como error, y sin proponer moverlo de donde esté.

El informe da, por este orden: qué está bien, qué falta y qué propone hacer, separando lo que se puede hacer en la incorporación de lo que necesita una sesión aparte.

## Al terminar

Se dice qué se ha creado, movido o cambiado, qué queda pendiente y qué debe comprobar el propietario: abrir Claude Code en el proyecto y ver que el panel de la SF muestra el nombre, el color, la fase si sigue la metodología, y sus propuestas si las hay, sin avisos de la configuración. Claude comprueba lo que puede (la comprobación final) y lo dice en su informe; no queda nada en la cola. No se afirma que el proyecto exista en el kanban si no se ha creado.

Si durante la incorporación algo de la SF falla, sobra o falta, no se anota en el proyecto: se dice en una línea que es de la SF, y llevarlo a ella es cosa del propietario, en una sesión de la SF («Un proyecto solo anota propuestas suyas», 210).
