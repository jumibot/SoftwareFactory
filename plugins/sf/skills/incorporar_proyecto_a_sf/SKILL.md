---
name: incorporar_proyecto_a_sf
user-invocable: false
description: Prepara un proyecto para trabajar con la Software Factory (SF) sin cambiarlo — operación sin tarea, guiada por menús en la línea de prompts — identidad y configuración en .sf/proyecto.json (nombre, color de sesión, descripción breve, metodología, kanban si se elige, idioma, formato de commit, línea de coautoría, remoto de GitHub, rama de publicación y manifiesto con versión, detectados y confirmados), remoto en GitHub obligatorio (si no hay ninguno, se crea con gh; fuera de GitHub no hay SF), ramas develop y main, estado inicial, cola de peticiones, .gitignore, CLAUDE.md sin líneas de la SF (las reglas y la orquestación las entrega el mod; al actualizar, se quitan la copia .sf/claude-sf.md y su importación) y los documentos de la SF en sf/ (sf/propuestas.md, sf/decisiones/ una decisión por archivo, sf/informes/). No mueve ni renombra nada del proyecto; al poner al día, pasa a sf/ los documentos de la SF y las decisiones antiguas. Cubre cuatro casos — proyecto nuevo, proyecto existente anterior a la SF, actualizar uno ya incorporado a la versión actual de la SF y diagnosticar qué le falta sin cambiar nada. Úsala cuando pidan incorporar, adaptar o preparar un proyecto para la SF, ponerlo al día con la SF, o revisar si cumple lo que la SF necesita. Cambiar después la configuración de un proyecto ya incorporado es de `sf:configurar_proyecto` (/sf_config).
---

# Incorporar un proyecto a la SF

La skill prepara el proyecto de la sesión para la SF: le da identidad, ramas, estado y cola, y el sitio de los documentos de la SF. Las reglas de la SF y `sf:orquestacion` no se escriben en el proyecto: las entrega el mod del plugin al empezar la sesión, tras `/clear` y tras compactar, siempre en la versión instalada. El método está en la skill `sf:metodologia`.

**Una operación, sin tarea.** Incorporar, poner al día y pasar a `sf/` no se anotan en la cola, no crean tarea ni rama y no pasan por el panel («Incorporar un proyecto es una operación sin tarea, guiada por menús», 209). Claude la lleva desde la línea de prompts, con menús (la herramienta de preguntas con opciones) y mensajes cortos: dice qué va a crear, mover o cambiar, pide el OK del propietario y lo aplica en `develop`, con su commit. Lo que salga mal se deshace con git.

**Un proyecto por sesión.** La skill trabaja siempre sobre el proyecto de la carpeta de la sesión. Si esa carpeta es el repositorio de la propia SF, o el proyecto que se quiere incorporar es otro, no se hace nada: se dice en una línea y se propone abrir una sesión en ese proyecto.

**Nada del proyecto se mueve.** La SF no renombra carpetas ni archivos, ni cambia de sitio documentos, assets ni ningún otro contenido del proyecto («Incorporar un proyecto no mueve ni renombra nada», 201). Lo que necesita lo usa donde ya está o lo añade con lo mínimo; lo que el proyecto ya tiene, sobre todo su `CLAUDE.md`, se conserva. Reorganizar algo del proyecto es una petición aparte del propietario, nunca parte de la incorporación. La única excepción es pasar a `sf/` los documentos de la SF y las decisiones (paso 7), siempre con el OK del propietario.

**Lo fijo, lo que se detecta y lo que se elige** («La SF fija el mecanismo y se adapta a las convenciones del proyecto», 202; el diseño, en el informe «Configuración inicial» de la tarea 263):

- **Fijo, sin campo ni pregunta:** la cola, el modelo de ramas (`develop`, una rama `feature/NN-nombre` por tarea, squash al cerrar y publicación de `develop` a la rama que hace de `main`, «El manejo del repositorio no se negocia: siempre develop», 205), un remoto en GitHub («Sin remoto en GitHub no hay SF: se valida al incorporar y, si falta, se crea», 230), los commits, que los hace siempre Claude («Los commits los lleva siempre Claude», 225), la versión con su tag `vX.Y.Z` («La versión forma parte del manejo del repositorio», 226), las decisiones en `sf/decisiones/` («Las decisiones son material de la SF: siempre en sf/decisiones/», 208) y las reglas comunes, que entrega el mod. **La gestión del repositorio no se deja a elección** («La SF gestiona el repositorio a su manera: la incorporación no lo deja a elección», 285): se explica una sola vez, en palabras llanas, antes de pedir nada más, y se pide aceptarla (paso 2). No hay opciones que dejen la SF a medias (que los commits los haga el propietario, no crear `develop`, no tener remoto): si no se acepta, la incorporación se para sin cambiar nada y lo dice. Lo aceptado no se vuelve a preguntar: las reglas del proyecto que choquen se adaptan como consecuencia, avisando de qué cambia («Reglas del proyecto»).
- **Se detecta y se confirma:** el idioma, el formato del commit (y con él la marca del número de la tarea), la línea de coautoría de los commits, el remoto de GitHub, la rama que hace de `main` y el manifiesto con versión (pasos 2 y 8).
- **Se elige:** la metodología y el kanban (pasos 1 y 8).

No hay mapa de documentos: si el proyecto sigue la estructura documental de la SF, sus documentos están donde la SF los busca; si no la sigue, no se mapean, y la incorporación no pregunta rutas («Sin mapa de documentos: o se sigue la estructura de la SF, o no se mapea», 229).

**Detectar con comandos.** Lo que se detecta lo da `python -I -X utf8 <plugin>/tools/configuracion.py detectar` (remotos y si son de GitHub, a cuál siguen `develop` y la rama de publicación, las ramas `main`, `master` y `develop`, los manifiestos con versión, la forma de los últimos 50 commits y su línea de coautoría más usada, y los colores de los proyectos vecinos), y lo que vale y falla de `.sf/proyecto.json`, `configuracion.py ver`; los dos solo leen y los usa también `sf:configurar_proyecto`. Si el mod dice al empezar la sesión que en esta máquina Python se lanza con otro nombre (en macOS, `python3`), estas órdenes van con ese («La orden de Python sale del intérprete que se detecta», 236). El idioma lo dice Claude leyendo el README, el `CLAUDE.md` y los commits.

**Menús de hasta cuatro preguntas.** Se pregunta con la herramienta de menús, la opción recomendada primero y con lo que la delata, en su descripción (por ejemplo, «Como los de ahora, con un tipo delante: `feat: …`» y «41 de los últimos 50 commits son así»). Lo que se detecta sin duda no se pregunta: se enseña en el resumen antes del OK. Cada menú lleva solo las preguntas que hacen falta; si se quedan en cero, no se muestra. Son tres, por este orden: repositorio (paso 2), identidad (paso 1) y convenciones (paso 8); si a uno le salen más de cuatro, la última va en un menú aparte justo después. El del repositorio va primero porque empieza por aceptar cómo lo lleva la SF: sin eso no tiene sentido preguntar lo demás.

**Para quien llega por primera vez** (tarea 357). Quien incorpora un proyecto puede no conocer la SF ni git a fondo: todo lo que se le enseña y se le pregunta se entiende sin saber cómo funciona por dentro.

- **La pregunta, corta; el detalle, en el chat.** Lo que hay que saber para responder (qué se va a hacer, qué se ha detectado, por qué hace falta) va antes del menú, en el chat, en una lista corta con una cosa por línea. La pregunta del menú cabe en una línea («¿Aplico estos cambios?», «¿Creo la rama develop?»), sin listas ni paréntesis dentro.
- **Opciones que dicen qué pasa.** El texto de cada opción es lo que hará Claude («Sí, aplícalos», «Sí, privado»), y su descripción, la consecuencia en palabras llanas («Crea y cambia lo de la lista y lo sube a GitHub»). Nada de «Aplicar» o «Sí» a secas cuando la pregunta no lo deja claro.
- **Palabras llanas.** Cada archivo o rama, con para qué sirve («`.gitignore`: para que git no guarde los archivos de trabajo de la SF»). Fuera la jerga interna: nombres de campos (`rama_main`, `coautor`), mecanismos de git (`merge=union`, «siguiendo `<remoto>/main`») y recuentos sin sentido para el lector («+8 líneas»). Los valores de configuración, con nombres legibles: «color verde», «idioma español», «commits sin formato fijo», «sin seguir la metodología», «sin firma de Claude en los commits». Los términos de la SF que no se pueden evitar (`develop`, la metodología), la primera vez con media frase que los explique.

**El progreso, en el panel** (tarea 333). Mientras dura la incorporación, el panel de la SF enseña sus pasos («1. Plugin», «2. Caso»…) con la respuesta de cada uno, el actual resaltado y los que faltan atenuados: así el propietario sabe dónde está y lo repasa todo antes del OK. Claude lo anota con `python -I -X utf8 <plugin>/tools/incorporacion.py <orden>`, desde la carpeta del proyecto. La herramienta lo guarda fuera del proyecto, en `~/.claude/sf/`, un archivo por proyecto que no depende de la sesión (sobrevive a `/reload-plugins`, `/clear`, el modo prueba y una sesión nueva o reanudada en la carpeta), y no toca nada del proyecto:

- `empezar <caso>` (`nuevo`, `existente`, `actualizar` o `diagnosticar`), lo primero, con el caso que se deduce mirando el proyecto, sin preguntar nada: fija los pasos del caso, el primero «Plugin». Si el propietario elige otro caso en el menú, se vuelve a lanzar con el elegido; lo ya anotado se conserva.
- `anotar <paso> "<respuesta>"`, con el número o el nombre del paso, en cuanto se responde cada menú: una línea corta con lo elegido (por ejemplo, `anotar Identidad "Contador · verde · sin metodología"`). Lo que se detecta sin preguntar también se anota, para que se vea antes del OK; un menú que no sale se anota con lo detectado. Anotar el paso actual pasa al siguiente.
- `paso <paso>`, si se vuelve a uno anterior (el propietario cambia algo antes del OK). Volver a anotar un paso ya respondido (el Plugin, tras actualizarlo) solo cambia su respuesta: lo demás se conserva y el paso actual no se mueve.
- `recargar`, cuando hace falta cargar la versión de la SF ya instalada («Antes de nada: el plugin al día»): al acabar el turno, el mod recarga los plugins y le pasa a Claude «continúa la incorporación a la SF». El panel dice «Recargando la SF» mientras tanto.
- `recuperar`, para traer lo respondido en una incorporación que se borró a medias («Lo primero, el progreso guardado»).
- `borrar --sin-guardar`, solo al empezar de nuevo. Borrar una incorporación a medias sin esa opción (o desde el mod, con un no a incorporar en un menú) guarda antes lo respondido aparte, para recuperarlo. Abandonar, en el panel, lo borra todo, también lo guardado: es una decisión expresa del propietario (decisión 286). Al terminar no se borra: se anotan todos los pasos, también Aplicar y Comprobación (o Informe), para que se vean marcados, y la lista sigue en el panel hasta que el proyecto tiene su panel operativo; entonces la quita el mod, al empezar el turno siguiente. Si se para sin cambiar nada (el propietario no acepta cómo lleva la SF el repositorio, o los remotos están fuera de GitHub), tampoco: la lista queda en pausa hasta que el propietario la abandona (tarea 333, norma del propietario).

**En pausa** (decisión 258). Si un turno acaba, o se interrumpe con Esc (en un menú o mientras Claude trabaja), con la incorporación a medias, el mod la pone en pausa: no borra nada de lo respondido. Mientras corre un turno, también con un menú esperando respuesta, no está en pausa: el panel dice «En curso», y el mod quita la pausa al empezar cada turno (tarea 366). Tras una recarga pedida con `recargar`, tampoco: sigue sola. El panel atenúa la lista, con «En pausa», y ofrece dos botones: «Continuar incorporación a la SF», que pasa a Claude «continúa la incorporación a la SF», y «Abandonar incorporación a la SF», que borra el progreso sin Claude. Cualquier orden que escribe (`anotar`, `paso`, `empezar`) quita la pausa. Al cargarse el mod (sesión nueva o reanudada, `/reload-plugins`, el modo prueba, `/clear`), una incorporación a medias queda igual, en pausa: no se pierde nada. El mod borra el progreso solo con «Abandonar incorporación a la SF», con «Hecho: cerrar la lista» en la lista terminada, al salir el panel operativo y con «Ahora no» o «No, y no vuelvas a preguntar en esta carpeta» en un menú. Mientras está a medias, aunque ya exista `.sf/proyecto.json` (desde Aplicar), el panel enseña la caja de la incorporación en lugar de las tareas: el panel normal sale al terminar la Comprobación (tarea 366). Terminada (todos los pasos anotados), la lista se queda con «Terminada» hasta que el proyecto tiene su panel operativo (`.sf/proyecto.json` válido) y, entonces, el mod la quita al empezar el turno siguiente; sin panel operativo (un diagnóstico sin SF, una prueba simulada), sigue con un solo botón, «Hecho: cerrar la lista», que la quita y devuelve la bienvenida. «Abandonar incorporación a la SF» sale solo con una incorporación a medias, en pausa. Mientras hay una incorporación, la bienvenida del panel no enseña la invitación a empezar.

**Lo primero, el progreso guardado.** Antes que nada, `incorporacion.py ver` (sale con 2 si no hay progreso):
- Con «continúa la incorporación a la SF» (el botón Continuar, o el mod tras recargar), se sigue desde el paso guardado sin preguntar: `paso <actual>`, que quita la pausa, y se repite su menú. Si el paso guardado era el Plugin tras recargar, se repite su comprobación, se anota y se sigue con el primero sin respuesta.
- Con «incorpora…» y progreso guardado, se pregunta en un menú, «¿Sigo donde lo dejamos?»: «Sí, seguir desde <paso>» (lo respondido se conserva) o «Empezar de nuevo» (`borrar --sin-guardar` y se empieza). Antes de seguir, el plugin se comprueba otra vez («Antes de nada: el plugin al día»): se anota el Plugin con lo nuevo, sin perder lo demás, y se sigue con `paso <actual>`.
- Sin progreso, pero con respuestas guardadas de una incorporación borrada a medias por otra causa que Abandonar (`ver` lo dice: «Hay respuestas guardadas…»), el mismo menú: «Sí, seguir con lo que respondiste» (`recuperar`) o «Empezar de nuevo» (`borrar --sin-guardar`).
- Sin progreso ni nada guardado, se empieza: el plugin («Antes de nada: el plugin al día») y después el caso.

Los pasos de cada caso son: nuevo, Plugin, Caso, Repositorio, Identidad, Convenciones, Cambios y OK, Aplicar y Comprobación; existente, Plugin, Caso, Diagnóstico, Reglas del proyecto, Repositorio, Identidad, Convenciones, Cambios y OK, Aplicar, CLAUDE.md, Pasar a sf/ y Comprobación; actualizar, Plugin, Caso, Diagnóstico, Reglas del proyecto, Configuración, Cambios y OK, Aplicar, CLAUDE.md, Pasar a sf/ y Comprobación; diagnosticar, Plugin, Caso, Diagnóstico, Reglas del proyecto e Informe. «Reglas del proyecto» se anota con lo encontrado, en palabras llanas: «2 choques: commits y ramas», «sin choques». Lo que no aplica (sin choques en el `CLAUDE.md`, nada que pasar a `sf/`) se anota así, «sin choques», «nada que pasar». Si la herramienta falla, se sigue sin ella: el progreso es una ayuda, no un requisito.

**La lista de pasos del chat, igual que la del panel** (tarea 357). Si Claude lleva la incorporación con su lista de tareas (la que la app y la terminal enseñan en el chat), la lista tiene exactamente los pasos del caso, con los mismos nombres y en el mismo orden que el progreso («Plugin», «Caso», «Diagnóstico»…), no otros resumidos. Cada paso se marca en la lista a la vez que se anota con `incorporacion.py`: en curso al empezarlo, hecho al anotarlo. Al volver a uno anterior (`paso`), se marca así también. Al retomar (Continuar tras una pausa, «Seguir desde…» o una sesión nueva), lo primero es poner la lista al día con el progreso guardado: hechos los pasos ya anotados y en curso el actual. Si cambia el caso (`empezar` con otro), la lista se rehace con los pasos del nuevo. Una lista que se queda atrás confunde más que no tenerla.

## Antes de nada: el plugin al día

Incorporar con un `sf` viejo deja el proyecto con reglas y herramientas viejas. Por eso, en los cuatro casos, lo primero tras mirar el progreso guardado, antes de cualquier otra pregunta (también la del caso), es `python -I -X utf8 <plugin>/tools/plugin_sf.py ver`, que solo lee y se lanza sin preguntar (tarea 333). Compara la versión de `sf` que corre en la sesión, la instalada (en el scope de usuario y en los de esta carpeta) y la publicada (el tag `vX.Y.Z` más alto del catálogo `softwarefactory`), y da el estado:

- **`al_dia`**, o **`desconocido`** (sin red o sin catálogo): se anota (`anotar Plugin "Al día, 1.7.6"`, o «Sin comprobar: sin red») y se sigue.
- **`actualizar`**: la publicada es más nueva. Actualizar cambia la instalación de todos los proyectos del equipo, así que va con OK. Antes del menú, en una línea: «Hay una versión nueva de la SF (la X); tienes la Y. Conviene incorporar con la nueva». El menú, «¿Actualizo la SF a la X?», con «Sí, actualizar a la X (recomendado)» (la deja instalada para todos tus proyectos y la cargo enseguida; lo respondido se conserva) o «No, seguir con la Y». Con el OK, `plugin_sf.py actualizar` refresca el catálogo, actualiza `sf` en cada scope atrasado e instala las dependencias nuevas que falten, una orden por dependencia; si una orden falla, lo dice con su orden y no se sigue: sin una dependencia, `sf` no carga. Hecho, su estado dice cómo cargarla (decisión 286): `recargar` (solo ha cambiado `sf`), como `refrescar`, abajo; `reiniciar` (ha instalado dependencias nuevas), se anota (`anotar Plugin "Actualizado a la X: reiniciar"`), se pide al propietario en un mensaje corto, con la orden en su línea, «Sal con `/exit`, vuelve a abrir Claude Code en esta carpeta y pide otra vez «incorpora este proyecto a la SF»: seguiré donde lo dejamos», y se termina el turno. No se sigue con la versión vieja cargada. Con «No, seguir con la Y», se anota así y se sigue.
- **`refrescar`**: la instalada ya es más nueva que la que corre. La recarga la lanza el mod, sin que el propietario escriba nada (decisión 286, una excepción a la 103 acotada a la incorporación): se anota (`anotar Plugin "Recargando la X"`), se pide con `incorporacion.py recargar` y se termina el turno con una línea: «Recargo la SF para usar la X; en unos segundos sigo yo solo, donde lo dejamos». Al acabar el turno, el mod lanza `/reload-plugins` y, recargado, le pasa a Claude «continúa la incorporación a la SF»: se sigue sin volver a pedir la incorporación. Si `recargar` falla (sin progreso), la orden la escribe el propietario: «Escribe `/reload-plugins`; luego pulsa Continuar en el panel o pídeme «continúa la incorporación a la SF»». Si tras recargar `sf` no carga («failed to load» en `/plugin`) o sus skills salen como desconocidas, o `plugin_sf.py ver` sigue diciendo `refrescar`, se pide reiniciar Claude Code, con la misma frase que en `reiniciar`.
- **`sin_instalar`**: `sf@softwarefactory` no está instalado para esta carpeta (ni en el scope de usuario ni en uno de la carpeta): corre otra copia; se dice en una línea y se sigue.

Desde la copia de trabajo de la SF (el modo prueba), la versión que corre no se compara: el estado es el de la instalada frente a la publicada (`al_dia`, `actualizar` o `desconocido`), y el mensaje dice que corre la copia de trabajo. Se anota así (`anotar Plugin "Al día, 1.7.6 · corre la copia de trabajo"`) y se sigue.

Al volver, se repite la comprobación, que ya no tiene nada que hacer, se anota el Plugin (`anotar Plugin "Al día, X"`: lo demás se conserva) y se sigue con la skill nueva desde el primer paso sin respuesta. Si la herramienta falla, se dice y se sigue. Es la misma comprobación que hace `sf:comprobar_instalacion`.

## Los cuatro casos

Antes de tocar nada (y con el plugin al día), se deduce el caso mirando el proyecto y se presenta al propietario en un menú, «¿Qué hago con este proyecto?», en el que la primera opción es el caso detectado, marcado como recomendado, con lo que hará y, en su descripción, lo que lo delata en palabras llanas (por ejemplo, «Prepararlo para la SF (recomendado)», con «Ya tiene código y aún no usa la SF; no muevo nada de lo tuyo»; no «sin `.sf/`, con un `CLAUDE.md` de 553 líneas»). La otra opción es «Solo revisar qué le falta, sin cambiar nada». Si el propietario ya ha nombrado el caso en su petición («diagnostica», «actualiza a la SF»), no se pregunta. Los casos son estos:

- **Nuevo:** carpeta vacía o casi vacía, sin `.sf/`. Se crea todo.
- **Existente:** proyecto con código o documentos, pero sin `.sf/`. Se incorpora sin rehacer lo que ya funciona (metodología, 2, «Proyectos anteriores a la SF»).
- **Actualizar:** el proyecto ya tiene `.sf/proyecto.json` (o el antiguo `docs/sf.json`). Se pone al día con la versión actual de la SF (abajo, «Actualizar»).
- **Diagnosticar:** el propietario lo elige en el menú o pide revisar sin cambiar nada. Se hace la comprobación final y se da el informe. No se escribe nada.

En el caso existente, en el de actualizar y al diagnosticar, el diagnóstico va primero, y justo después, las reglas del proyecto: así se ve qué falta y qué choca antes de preguntar nada.

## Nuevo y existente

1. **Diagnóstico y reglas del proyecto.** En el caso existente, la comprobación final (abajo) dice qué falta, y después se leen las reglas del proyecto en busca de lo que choca con la SF («Reglas del proyecto», paso propio). En el nuevo, falta todo y no hay reglas que leer.
2. **Lo que solo da el propietario, en tres menús.** Repositorio (paso 2 del procedimiento: aceptar cómo lo lleva la SF, rama de publicación y remoto en GitHub), identidad (paso 1) y convenciones (paso 8: idioma, formato de commit, manifiestos, kanban y coautoría), con lo detectado como opción recomendada. Si el propietario no acepta cómo lleva la SF el repositorio, se para sin cambiar nada. Si los remotos están todos fuera de GitHub, se para antes de preguntar nada más (paso 2).
3. **Lo que va a cambiar, y el OK.** Antes del menú, en el chat, una lista corta en palabras llanas («Para quien llega por primera vez»), agrupada en cuatro apartados, cada cosa en su línea y con para qué sirve:

   - **Crea:** los archivos, carpetas y ramas nuevos, empezando por la ficha del proyecto (`.sf/proyecto.json`) con la configuración confirmada y lo detectado sin preguntar, en valores legibles.
   - **Cambia:** los archivos del proyecto que se editan, con qué se añade o se quita y para qué. Aquí van también las reglas del proyecto que chocan con lo aceptado del repositorio, con la frase de ahora y cómo queda («Reglas del proyecto»): son consecuencia del «Sí, trabajemos así», no una pregunta nueva.
   - **Sube a GitHub:** el commit, con su título, y las ramas que se suben, con el nombre del repositorio; y el repositorio, si se crea.
   - **No toca:** lo del proyecto que se queda como está, sobre todo su código y su `CLAUDE.md`, nombrando lo que el propietario pueda temer que se toque (archivos sin commit, carpetas de su editor).

   Un apartado sin nada no sale. Después, el menú, con la pregunta «¿Aplico estos cambios?» y tres opciones: «Sí, aplícalos» (crea y cambia lo de la lista, hace el commit y lo sube a GitHub), «Cambiar algo antes» (vuelve a la pregunta que se quiera cambiar, con `paso <paso>`) y «No, déjalo como está» (no cambia nada; la incorporación se puede seguir más tarde). Por ejemplo, para un proyecto existente sin metodología:

   > Esto es lo que voy a hacer en PoseTracker:
   >
   > **Crea**
   > - `.sf/proyecto.json`: la ficha del proyecto para la SF — nombre PoseTracker, color verde, idioma español, commits sin formato fijo, sin seguir la metodología, sin firma de Claude en los commits.
   > - `sf/decisiones/`: la carpeta donde se apuntan las decisiones del proyecto, con su índice.
   > - `sf/propuestas.md`: la lista de ideas pendientes de decidir; empieza vacía.
   > - `.gitattributes`: para que el índice de decisiones no dé conflictos al juntar ramas.
   > - La rama `main` en tu equipo, igual que la de GitHub: ahí se publica cada versión.
   >
   > **Cambia**
   > - `.gitignore`: añade unas líneas para que git no guarde los archivos de trabajo de la SF (la cola de tareas y su historial).
   > - `CLAUDE.md`, como aceptaste para el repositorio: quito «Los commits y los pull los hago yo», porque los commits los hago yo, Claude, con tu OK. El resto no cambia.
   >
   > **Sube a GitHub** (repositorio PoseTracker)
   > - Un commit, «Incorporado a la SF 1.8.0», con todo lo anterior, en la rama `develop`.
   > - Las ramas `develop` y `main`.
   >
   > **No toca**
   > - Tu código (`model.py` y lo demás), los `.pyc`, la carpeta `.vscode` ni el resto de tu `CLAUDE.md`.

   Lo que necesita una decisión aparte (los choques del `CLAUDE.md` que no son del repositorio ni de lo fijo, paso 5, y pasar a `sf/` las decisiones que ya tuviera el proyecto, paso 7) no entra en ese OK: se propone después, cada cosa con su menú.
4. **Aplicar en `develop`.** Con el OK, se aplican los pasos del procedimiento en `develop`, sin rama de tarea, y se hace su commit (paso 9). Si hay cambios sin commit en los archivos que se van a tocar, se dice y no se aplica hasta que estén resueltos. Desde aquí el proyecto ya tiene `.sf/proyecto.json` y el mod puede entregar las reglas de la SF con el siguiente mensaje: la incorporación sigue igual hasta la Comprobación, sin tarea ni cola, y el panel enseña su caja en lugar de las tareas hasta entonces.
5. **Comprobar e informar.** Se repite la comprobación final y se dice, en pocas líneas, qué ha cambiado, el commit y qué mirar («Al terminar»). No queda nada en la cola. Se anota el último paso (`incorporacion.py anotar Comprobación "…"`, o `Informe` al diagnosticar), sin borrar el progreso: lo quita el mod.

## Actualizar

Poner un proyecto al día no se anota en la cola ni crea tarea ni rama: el proceso ya está probado en la SF (decisiones «Poner un proyecto al día con la SF, sin tarea», 199, y 209). No se manda al propietario al panel.

1. **El plugin, al día.** Como en todos los casos, antes de nada («Antes de nada: el plugin al día»), con `plugin_sf.py`. Al pedir que se vuelva a lanzar, la petición es «pon el proyecto al día con la SF».

2. **Diagnóstico y reglas del proyecto.** La comprobación final (abajo) dice qué falta, y después se leen las reglas del proyecto en busca de lo que choca con la SF («Reglas del proyecto»). El proyecto ya trabaja con la SF: su manera de llevar el repositorio no se vuelve a preguntar; lo que choque se adapta y se enseña en la lista del OK, en «Cambia».

   - **Remoto en GitHub** (230): se comprueba como al incorporar (paso 2 del procedimiento). Si el `remoto` de `.sf/proyecto.json` no existe o no apunta a GitHub (el panel lo avisa), se corrige con el que haya de GitHub; si no hay ninguno, se ofrece crearlo; si solo los hay fuera de GitHub, se explica que la SF solo trabaja con GitHub y no se sigue.
   - **Configuración:** se escriben los campos que falten con lo detectado (paso 8), en un solo menú con lo que tenga duda; lo detectado sin duda se enseña en el informe. La cadena antigua de `kanban` (`"kanban": "JKanban"`) pasa a bloque (`{ "proveedor": "jkanban", "proyecto": "JKanban" }`). Un valor que no se entiende (el panel lo avisa) se vuelve a detectar y se confirma.

3. **Informe y OK.** Como al incorporar («Nuevo y existente», paso 3): antes del menú, la lista en palabras llanas con «Crea», «Cambia» (aquí también lo que se borra), «Sube a GitHub» y «No toca», cada cosa con para qué (por ejemplo, «`CLAUDE.md`: quito la línea que cargaba la copia antigua de las reglas de la SF; ahora las da el plugin» o «`.sf/proyecto.json`: apunta que el proyecto ya va con la SF 1.4.2, antes la 1.3.0»). Después, el menú «¿Aplico estos cambios?», con «Sí, aplícalos», «Cambiar algo antes» y «No, déjalo como está». Lo que necesita una decisión aparte (los choques del `CLAUDE.md` que no son del repositorio ni de lo fijo, paso 5 del procedimiento, y pasar a `sf/` los documentos de la SF y las decisiones, paso 7) no entra en ese OK: se propone después, cada cosa con su menú.

4. **Aplicar en `develop`.** Con el OK, se aplican los pasos del procedimiento que hagan falta en `develop` del proyecto, sin rama, y se hace su commit (paso 9). Si la sesión está en otra rama, se pasa a `develop`; si hay cambios sin commit en los archivos que se van a tocar, se dice y no se aplica hasta que estén resueltos.

5. **Comprobar que ya no va atrasado.** Se repite la comprobación final y se mira lo mismo que mira el aviso de atraso: `sf` de `.sf/proyecto.json` tiene el mismo mayor.menor que la versión que corre, y ni `CLAUDE.md` ni `.claude/CLAUDE.md` tienen la línea `@.sf/claude-sf.md`. Si algo falla, se dice y se arregla antes de terminar.

6. **Las reglas nuevas, con `/clear`.** El mod entrega las reglas y la orquestación al empezar la sesión, tras `/clear` y tras compactar; la conversación en curso sigue con las de antes (o con la copia `.sf/claude-sf.md`, si se acaba de quitar). Si el plugin se ha actualizado o se ha quitado la importación, se pide en el mismo mensaje del informe: «Escribe `/clear` para que entren las reglas nuevas.»

7. **Informe.** En pocas líneas: qué ha cambiado, los commits, la versión con la que queda y que el aviso de atraso desaparece. No queda nada en la cola. Se anota el último paso (`incorporacion.py anotar Comprobación "…"`, o `Informe` al diagnosticar), sin borrar el progreso: lo quita el mod.

8. **Cambiar la configuración.** Tras el informe, se enseña la configuración con que queda (`configuracion.py ver`), contada en palabras llanas como en la lista del OK («color verde», «commits sin formato fijo»), y se ofrece cambiarla en un menú, «¿Cambio algo de la configuración?»: «No, así está bien» o «Sí, cambiar algo». Con «Sí, cambiar algo», se sigue con `sf:configurar_proyecto` desde su paso 2, sin volver a enseñarla (228). Lo mismo se puede pedir después con `/sf_config`.

## Reglas del proyecto: qué choca con la SF

Paso propio, justo después del diagnóstico y antes de cualquier pregunta (casos existente, actualizar y diagnosticar; tarea 366). Solo lee: no cambia nada ni pregunta nada.

1. **Qué se lee.** El `CLAUDE.md` entero (y `.claude/CLAUDE.md` y `CLAUDE.local.md`, si los hay), y las demás reglas que el proyecto se da: `AGENTS.md`, `CONTRIBUTING.md`, las reglas de `.claude/` (`rules/`, `settings.json` con sus hooks y permisos, comandos y skills propios), los ganchos de git (`.husky/`, `.pre-commit-config.yaml`, `.git/hooks/` que no sean los de ejemplo) y lo que el README diga sobre cómo se trabaja (ramas, commits, pull requests).
2. **Qué es un choque.** Lo que contradice cómo trabaja la SF:
   - **El repositorio** (lo fijo, 285): quién hace los commits o los push; con qué ramas se trabaja (todo en `main`, otro nombre para `develop`, ramas por persona); cómo se junta el trabajo (merge sin squash, pull requests obligatorias, prohibido reescribir); quién publica y cómo se versiona; ganchos o permisos que impidan a Claude hacer commit, push o crear ramas.
   - **Otras piezas fijas:** otra forma de registrar las decisiones o las tareas; un apartado «Software Factory» escrito dentro que repita sus reglas, o la línea `@.sf/claude-sf.md`.
   - **Convenciones que la SF detecta** (idioma, formato de los commits, firma de coautoría): no son choques que haya que quitar, sino lo que el proyecto ya decide; se usan como lo detectado en el paso 8.
   - **El resto** (dónde va cada cosa: memoria, `CLAUDE.md`, skills): se cruza con la SF pero las dos formas pueden convivir.

   Que el proyecto tenga sus documentos en otra carpeta (`_docs/`, `doc/`) no es un choque: la SF no los mapea (229).
3. **Qué se dice.** Antes del menú del repositorio, en el chat, la lista de choques en palabras llanas, uno por línea, con dónde está y qué dice («`CLAUDE.md`: los commits y los pull los llevas tú»). Se anota el paso con el resumen («2 choques: commits y ramas», «sin choques»).
4. **Qué se hace con ellos.** Ninguno se pregunta aquí:
   - Los del repositorio y de las otras piezas fijas se adaptan como consecuencia de aceptar cómo trabaja la SF (paso 2): se quita la frase o se reescribe lo justo para que no contradiga, sin añadir reglas de la SF (las entrega el mod), y va en la lista del OK, en «Cambia», con la frase de ahora y cómo queda. Un gancho o un permiso que impida trabajar a la SF, igual: se dice qué se cambia.
   - Los de convenciones dan el valor detectado (paso 8).
   - Los del resto se proponen después de aplicar, cada uno con su menú (paso 5).

## Procedimiento

Los menús van en este orden: repositorio (paso 2), identidad (paso 1) y convenciones (paso 8).

1. **Identidad.** Se pregunta lo que falte de `.sf/proyecto.json`, con un valor propuesto sacado del proyecto (su README, el nombre de la carpeta o del repositorio). Lo que ya está no se pregunta.
   - `proyecto`: el nombre, tal como se escribe (con acentos y mayúsculas).
   - `descripcion`: una línea de 120 caracteres como mucho que diga qué es el proyecto, por defecto la primera frase del README. La lee el panel (y el kanban, si se elige).
   - `color`: el color de sus sesiones, uno de `red`, `blue`, `green`, `yellow`, `orange`, `pink` o `cyan`, con dos o tres libres como opciones, nombrados en el idioma del proyecto («verde», no `green`): «¿De qué color quieres las sesiones de este proyecto?», con la descripción «Para distinguirlo de tus otros proyectos». `purple` es de la SF. Se recomienda uno que no usen los otros proyectos, mirando los `.sf/proyecto.json` de las carpetas vecinas (solo lectura).
   - `metodologia`: «¿Sigo la metodología de la SF?», con «Sí, con sus fases y documentos» (antes de programar se escriben la visión y la especificación, y el trabajo va por fases) y «No, solo tareas y ramas» (la SF lleva las tareas, las ramas y las decisiones; el proyecto sigue como lo llevas). Por defecto, «Sí» en un proyecto nuevo y «No» en uno existente, salvo que tenga visión o especificación. Sin metodología, el mod no entrega las reglas del método y el panel no pinta la fase ni pide `estado.json`.
   - `sf`: no se pregunta: la versión del plugin `sf` instalado, tomada de su `plugin.json`, no de memoria.

   El mod de estado aplica el color y el nombre a la sesión (`/color` y `/rename`) en cuanto lee el archivo.

2. **Repositorio: cómo lo lleva la SF, rama de publicación y remoto en GitHub.** La SF trabaja siempre con su modelo de ramas (205), un remoto en GitHub (230) y sus commits (225), y eso no se deja a elección (285). Antes del menú, lo que lo impide o hay que preparar:
   - **Sin repositorio git:** se propone crearlo (`git init -b main`) con un primer commit de lo que ya hay. En una carpeta vacía no hay nada que poner en él: es un commit vacío (`git commit --allow-empty`), con un título como «Inicio del repositorio» en el idioma del proyecto, para que exista `main` y de ella salga `develop`.
   - **git sin identidad:** si `git config user.name` o `git config user.email` no dan nada (pasa en un equipo recién estrenado), ningún commit sale. Se dice antes del menú, en palabras llanas («git necesita tu nombre y tu correo para firmar los cambios, y en este equipo aún no los tiene»), se piden el nombre y el correo al desarrollador y se pregunta dónde guardarlos, «¿Dónde guardo tu nombre y correo?»: «Solo en este proyecto (recomendado)» (`git config`) o «Para todos tus proyectos» (`git config --global`). Se ponen con su OK.
   - **Remotos fuera de GitHub:** con `git remote -v`, solo cuenta un remoto cuya url apunte a `github.com` (`https://github.com/…`, `git@github.com:…`). Si el proyecto tiene remotos y ninguno es de GitHub (GitLab u otro), no hay menú: se explica que, por ahora, la SF solo trabaja con GitHub y que hay que pasar el proyecto allí, y se para sin cambiar nada. No se crea uno de GitHub a su lado (230, precisada el mismo día).

   **Cómo lleva la SF el repositorio, una sola vez y antes de pedir nada** (285). En el chat, en palabras llanas, una cosa por línea: lo que hace la SF, lo que hace el propietario y, si «Reglas del proyecto» encontró choques, qué reglas suyas se adaptarán. Sin jerga: «commit», la primera vez, con media frase («cada cambio guardado en git»). Por ejemplo:

   > Antes de seguir, así trabaja la SF con el repositorio de PoseTracker:
   > - Dos ramas fijas: `main`, con lo publicado, y `develop`, donde se junta lo terminado. Si aún no existen, las creo.
   > - Cada tarea se hace en su propia rama; cuando la pruebas y das el OK, entra en `develop` como un solo cambio.
   > - Los commits (cada cambio guardado en git) los hago siempre yo, Claude. Tú no tienes que hacer ninguno.
   > - Subo los cambios a GitHub y publico una versión (de `develop` a `main`) solo con tu OK.
   > - Lo tuyo: probar cada tarea y darme el OK. Nada se cierra ni se publica sin él.
   >
   > Tu `CLAUDE.md` dice otra cosa en un punto; si te parece bien trabajar así, lo adapto (lo verás antes de aplicarlo):
   > - «Los commits y los pull los hago yo»: lo quito, porque los commits los haré yo.

   El menú, con la pregunta de aceptar primero y, después, solo las que hagan falta:

   | # | Pregunta | Opciones (la recomendada, primero) | Se salta si |
   | --- | --- | --- | --- |
   | 1 | ¿Trabajamos así en `<proyecto>`? | «Sí, trabajemos así» (la SF lleva el repositorio como acabo de contar; con choques: «y adapto las N reglas tuyas que dicen otra cosa») / «No: dejar el proyecto sin la SF» (paro aquí sin cambiar nada; puedes incorporarlo más adelante) | Nunca (al actualizar no se pregunta: ya trabaja así) |
   | 2 | ¿Publico las versiones en `master`? | «Sí, publicar en `master`» (la SF la usa como su rama principal) / «Crear una rama `main` aparte» (desde `master`, que se queda como está) | Hay `main`, o no hay rama principal |
   | 3 | Con varios remotos de GitHub: «¿A qué repositorio de GitHub subo los cambios?». Sin ninguno: «¿Creo el repositorio en GitHub como privado?» | Varios: cada uno, con su dirección en la descripción, primero el que siguen `develop` o la rama de publicación (`git config branch.<rama>.remote`). Ninguno: «Sí, privado (recomendado)» (solo tú lo ves) / «No, público» (cualquiera puede verlo) | Hay uno de GitHub: se usa |

   `develop` no se pregunta: crearla es parte de lo aceptado; se dice en el resumen. Tampoco hay opción de no crear el remoto: sin él, la SF no puede subir ni publicar.

   - **Rama de publicación** («Si el proyecto tiene master, se pregunta si hace de main», 213): si el proyecto tiene `main`, es la suya. Si su rama principal se llama de otra forma (`master`, por ejemplo), con la primera opción la SF publica en ella y no se crea `main`; con la segunda, se crea `main` desde ella, y la suya queda como estaba, sin borrarla ni renombrarla (201). Se guarda en `rama_main`. Si esa rama solo existe en el remoto (por ejemplo, `github/main` sin `main` local), se crea la local siguiéndola (`git branch --track <rama> <remoto>/<rama>`), sin preguntar, y se dice en el resumen («Si main solo está en el remoto, se crea la local sin preguntar», 234). Igual con `develop`: si solo está en el remoto, se crea la local siguiéndola, sin preguntar, y la pregunta de crearla no sale.
   - **Remoto:** el nombre del remoto de GitHub elegido se guarda en `remoto`. Para crearlo hace falta `gh` instalado y con la sesión iniciada (`gh auth status`); si no, se dice cómo (instalarlo: en macOS, `brew install gh`; en Windows, `winget install GitHub.cli`; y `gh auth login`, aceptando que configure git) y se espera: sin remoto no se sigue. Se crea, tras el OK, con `gh repo create <cuenta>/<proyecto> --private --source . --remote origin` (o `--public`), y `remoto` vale `origin`. Solo se ofrece crearlo si el proyecto no tiene ningún remoto.
   - **Si no se acepta** (285; 214; 225; 230). Con «No: dejar el proyecto sin la SF», no hay segundo menú ni opciones intermedias: se dice en una línea por qué («La SF necesita llevar así el repositorio para poder cerrar y publicar tus tareas; sin eso no puede trabajar aquí»), que no se ha cambiado nada (ni `.sf/` ni ningún otro archivo) y que se puede incorporar más adelante, pidiéndolo otra vez. Se anota (`anotar Repositorio "No aceptado: sin la SF"`) y se para.
   - **Al aceptar**, se anota (`anotar Repositorio "De acuerdo · publicar en main · github"`) y las reglas del proyecto que chocan quedan para la lista del OK, en «Cambia» («Reglas del proyecto»). No se vuelven a preguntar en el paso CLAUDE.md.

   Las ramas se crean en local y se suben al remoto con el commit final (paso 9). Si el push pide usuario y contraseña, git no tiene las credenciales de `gh`: `gh auth setup-git` las configura.

3. **Estado y cola.** Con metodología, se crea `.sf/estado.json` con la fase real del proyecto. En uno nuevo, la fase es `vision` y `hechas` queda vacío. En uno existente, `hechas` lleva solo las fases cubiertas de verdad, y los documentos que faltan (la visión, la especificación funcional, las guías) van a `pendientes`. Sin metodología, no se crea. `.sf/estado.json`, `.sf/peticiones.json`, `.sf/peticiones.lock`, `.sf/historial.jsonl`, `.sf/copias/` (lo que escribe el CLI `cola.py`), `.sf/subagentes.json` (lo que el panel sabe de los subagentes de cada sesión), `.claude/worktrees/` (los worktrees de los subagentes) y `sf/decisiones/README.html` (el índice de las decisiones en html, que se genera a mano con `indice_decisiones.py --html`) se añaden al `.gitignore`; `proyecto.json` sí se versiona. Si existía `docs/sf.json`, sus datos pasan a `.sf/` y el archivo antiguo se borra con `git rm`.

4. **Reglas de la SF, sin tocar el `CLAUDE.md`.** Las reglas que la SF distribuye (las comunes de `templates/claude-sf.md` del plugin y, si el proyecto sigue la metodología, las de `templates/claude-sf-metodologia.md`), una línea con sus convenciones (las de `.sf/proyecto.json`, paso 8) y el texto de `sf:orquestacion` los entrega el mod de la SF como contexto al empezar la sesión, tras `/clear` y tras compactar, en los proyectos con `.sf/proyecto.json`. El proyecto no lleva copia ni línea de la SF en su `CLAUDE.md`. Si no hay `CLAUDE.md`, se crea solo con el título del proyecto y su descripción, para lo propio del proyecto.

   La orquestación se apaga con `"automatizaciones": { "orquestacion": false }` en `.sf/proyecto.json`; entonces la carga el principal. Las reglas no se apagan.

   **Al actualizar** un proyecto incorporado con una SF anterior: se borra la copia `.sf/claude-sf.md` con `git rm` y se quita del `CLAUDE.md` (o de `.claude/CLAUDE.md`) la línea `@.sf/claude-sf.md`, sin tocar lo demás. Mientras la línea siga, el mod entrega solo la orquestación, para no dar las reglas dos veces, y el panel avisa de que el proyecto va atrasado. Un apartado «Software Factory» escrito a mano dentro del `CLAUDE.md`, como el de las primeras incorporaciones, repite las reglas: se propone quitarlo (paso 5). Se enseña el cambio antes de escribirlo.

5. **Lo que choca con la SF en un `CLAUDE.md` existente** (el paso CLAUDE.md). Los choques ya están en la lista de «Reglas del proyecto», y cada clase tiene su camino (285):
   - **Los del repositorio y de las otras piezas fijas** ya se adaptaron al aplicar, como consecuencia de lo aceptado en el paso 2 y enseñados en la lista del OK. Aquí no se preguntan otra vez: se anota lo hecho («Adaptadas 2 frases: commits y ramas»). Nunca se ofrece dejarlos como están: con ellos, la SF no podría trabajar.
   - **Los demás** (dónde va cada cosa, un apartado «Software Factory» escrito a mano), que pueden convivir con la SF, se presentan uno por uno: antes del menú, en el chat, qué dice la regla del proyecto, qué hace la SF y qué se recomienda, en palabras llanas; el menú, corto («¿Qué hago con esta regla?»), con opciones que digan qué pasa con ella («Quitarla: la SF ya lo hace así», «Dejarla como está»), las dos válidas para la SF, y cada decisión se anota en `sf/decisiones/`. Mientras no se decide, manda la regla del proyecto, porque es la que conoce su dominio.
   - Sin choques, se anota «sin choques».

   Si alguna sección del `CLAUDE.md` tendría mejor sitio en un documento (decisiones de arquitectura, procedimientos de despliegue), se dice como sugerencia. Moverla es una petición aparte del propietario (201), que se anota en la cola si la quiere.

   **`CLAUDE.md` complejo** (acuerdo del propietario, 2026-10-28). Cuando el `CLAUDE.md` es largo o tiene muchas reglas propias (por ejemplo, uno con principios inviolables, reglas de arquitectura y de despliegue), la revisión de los choques no se hace dentro de la incorporación. Es una tarea aparte que ocupa una sesión entera y estudia en detalle cada cambio antes de hacerlo. La incorporación hace solo lo que no toca ese contenido, salvo las frases que chocan con cómo lleva la SF el repositorio, que se adaptan igual (sin ellas la SF no puede cerrar ni publicar), y propone anotar esa tarea en la cola, con el número de reglas y de choques detectados. En esa sesión se trabaja así:
   - un cambio cada vez, con el texto actual, el propuesto y por qué;
   - se aplica solo con el OK del propietario, y cada cambio va en su propio commit;
   - antes de proponer cada cambio, se comprueba que no se pierde ninguna regla.

6. **Los documentos de la SF, en `sf/`.** Lo que la SF escribe en el proyecto va en la carpeta `sf/` de su raíz, visible y versionada, al lado del contenido del proyecto («Los documentos de la SF van en la carpeta sf/», 203). `.sf/` es la máquina; `sf/`, los documentos:
   - **`sf/decisiones/`**, con su índice: `python -I -X utf8 <plugin>/tools/indice_decisiones.py sf/decisiones` escribe `README.md` con la forma de registrar las decisiones, un archivo por decisión. Se añade al `.gitattributes` la línea `sf/decisiones/README.md merge=union`, para que dos ramas no choquen en el índice.
   - **`sf/propuestas.md`**, copiando `templates/propuestas.md` del plugin, con su «## Propuestas pendientes» vacía. Ahí van las propuestas del proyecto, y el panel las muestra en su sección Propuestas (decisión 196). Si ya existe, no se toca.
   - **`sf/informes/`**, para los informes que Claude escriba en el proyecto (análisis, auditorías, diagnósticos). Se crea con el primero, porque git no guarda carpetas vacías.

   Los documentos del proyecto (visión, especificación, guías) no se crean ni se mueven en la incorporación, y no se preguntan sus rutas: si siguen la estructura documental de la SF, están donde la SF los busca; si no, no se mapean (229). En un proyecto nuevo, se crean cuando toque escribirlos, según la metodología.

7. **Pasar a `sf/` lo que ya había.** En el caso existente y al actualizar, los documentos de la SF que estén en otro sitio y las decisiones que el proyecto ya tuviera se pasan a `sf/` (decisiones 203 y 208, la excepción de la 201). Se enseña al propietario, antes del menú, la lista con cada origen y su destino, y en una línea para qué: «La SF guarda sus documentos (decisiones, propuestas, informes) en la carpeta `sf/`; los tuyos no se tocan». El menú, «¿Paso estos documentos a `sf/`?», con «Sí, pasar todos (recomendado)», «Elegir uno por uno» o «Más adelante» (se quedan donde están y el panel los sigue leyendo allí). Ninguna opción de la incorporación empieza por «Ahora no»: el mod la toma como el no a incorporar y borra el progreso. Si se aplaza, queda en `pendientes` de `estado.json`, y el panel y `cola.py` siguen leyendo el sitio de antes. No se hace si hay trabajo en curso que pueda chocar (cambios sin commit, ramas de tareas abiertas que toquen esos archivos): se dice y queda en `pendientes`.
   - **`docs/propuestas.md`** → `git mv docs/propuestas.md sf/propuestas.md`.
   - **`docs/decisiones/`** → `git mv docs/decisiones sf/decisiones`. La línea de `.gitattributes` pasa a `sf/decisiones/README.md merge=union`, y la del `README.html` en `.gitignore`, a `sf/decisiones/README.html`. Se regenera el índice, que conserva lo que hay antes de «Índice».
   - **El antiguo `docs/decisiones.md`** (una sección «### Título» por decisión) → `python -I -X utf8 <plugin>/tools/indice_decisiones.py sf/decisiones --migrar docs/decisiones.md`: cada sección pasa a su archivo, con el mismo texto y sus enlaces rehechos desde la carpeta nueva, y el antiguo se borra. `git add sf/decisiones docs/decisiones.md` deja en el commit los archivos nuevos y el borrado.
   - **Decisiones en otra forma** (por ejemplo, un `decisiones-y-pendientes.md` con una lista por fecha, o una carpeta `adr/`) → Claude escribe cada decisión en su archivo de `sf/decisiones/`, con el nombre que da `indice_decisiones.py sf/decisiones --nombre "Título" --fecha <fecha>`, el texto literal en «Decisión», la fecha y el proyecto en «Origen» y, en «Contexto», de qué archivo viene. Se enseña la lista de títulos antes del OK. Si el archivo de origen solo tenía decisiones, se borra con `git rm`; si tiene más cosas (por ejemplo, los pendientes), se queda, y su sección de decisiones se cambia por un enlace a `sf/decisiones/`.
   - **Informes de la SF** que estén en `docs/` (por ejemplo, en `docs/referencias/reports/`) → `git mv` a `sf/informes/`, con los `.html` generados junto a su `.md`. Se proponen solo los que escribió la SF; los del proyecto no se tocan.

   Después de mover, se buscan con `git grep` los enlaces a las rutas antiguas (en el `CLAUDE.md`, los documentos y las propias decisiones) y se rehacen. El informe dice cuántos enlaces se han cambiado.

8. **Convenciones y configuración.** Se detectan con comandos y se confirman en un menú; lo que se detecta sin duda no se pregunta:

   Como en los otros menús, las preguntas, cortas, y lo detectado, en la descripción de cada opción («41 de los últimos 50 commits son así»):

   | # | Pregunta | Opciones (la recomendada, primero) | Por defecto | Se salta si |
   | --- | --- | --- | --- | --- |
   | 1 | ¿En qué idioma escribo commits, tareas y documentos? | El detectado / español / inglés | El del README, el `CLAUDE.md` y los últimos commits | Proyecto nuevo: el de la conversación |
   | 2 | ¿Cómo escribo los títulos de los commits? | «Con un tipo delante, como `feat: …`» (conventional; el número de la tarea va al pie, `SF-Tarea: N`) / «Como los de ahora, por ejemplo `<ejemplo>`» (el número, al pie) / «Sin formato fijo» (el número, al final del título, «(N)») | Con un tipo delante si lo sigue la mayoría de los últimos 50 títulos (`git log -50 --format=%s`); como los de ahora si comparten otra forma fija; si no, sin formato fijo | Proyecto nuevo: sin formato fijo |
   | 3 | ¿En qué archivos subo la versión al publicar? | Cada uno (selección múltiple), con para qué es («`package.json`, la versión de la aplicación web») / «En ninguno: solo la etiqueta de git» | Todos los detectados | Hay uno (se usa) o ninguno |
   | 4 | ¿Llevo las tareas también en un kanban? | «No, solo en la SF» / «Sí, en JKanban: `<proyecto>`» | «No» («El kanban se elige, y por defecto ninguno», 224) | — |
   | 5 | ¿Firmo mis commits como coautor? | «Sí, con mi nombre: `Claude <modelo>`» (añade al pie la línea `Co-Authored-By: Claude <modelo> <noreply@anthropic.com>`) / «No, sin firma» | La de esta sesión, con el modelo con que trabaja Claude ahora | Más de la mitad de los últimos 50 commits llevan la misma (`detectar`, «Coautoría»): se usa esa |

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
- Las reglas del proyecto (`CLAUDE.md`, `AGENTS.md`, ganchos y permisos de `.claude/` y de git) no dicen nada que impida a la SF llevar el repositorio a su manera: que los commits o los push los haga otro, trabajar sin `develop` o sin ramas por tarea («Reglas del proyecto»). Al diagnosticar, se dice cuáles chocan y qué se cambiaría al incorporar.
- Con metodología, lo que la metodología espera y el proyecto no tiene (guías de instalación y de actualización, visión, especificación funcional) se anota como pendiente, no como error, y sin proponer moverlo de donde esté.

El informe da, por este orden y en palabras llanas («Para quien llega por primera vez»: cada cosa con para qué sirve, sin nombres de campos): qué está bien, qué falta y qué propone hacer, separando lo que se puede hacer en la incorporación de lo que necesita una sesión aparte.

## Al terminar

Se dice qué se ha creado, movido o cambiado, qué queda pendiente y qué debe comprobar el propietario: abrir Claude Code en el proyecto y ver que el panel de la SF muestra el nombre, el color, la fase si sigue la metodología, y sus propuestas si las hay, sin avisos de la configuración. Claude comprueba lo que puede (la comprobación final) y lo dice en su informe; no queda nada en la cola. No se afirma que el proyecto exista en el kanban si no se ha creado.

En el caso nuevo y en el existente, el informe acaba con el paso siguiente, en una línea: la primera tarea, con un ejemplo que encaje con el proyecto («Pide tu primera tarea, por ejemplo: añade un README que explique el proyecto»). Claude la pondrá en la cola, la hará en su rama y pedirá probarla. No hace falta `/clear` ni reiniciar: con el siguiente mensaje, el mod entrega las reglas de la SF y la orquestación y, si Claude Code no está en pantalla completa, el encargo de ofrecerla («Tras incorporar, el mod entrega las reglas sin reiniciar», 242, y «Bienvenida del panel publicada y pantalla completa al incorporar», 245). Si ese mensaje no las trae, `/clear` las entrega.

Si durante la incorporación algo de la SF falla, sobra o falta, no se anota en el proyecto: se dice en una línea que es de la SF, y llevarlo a ella es cosa del propietario, en una sesión de la SF («Un proyecto solo anota propuestas suyas», 210).
