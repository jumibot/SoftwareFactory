# Por qué de cada regla

El porqué de cada regla de la skill, en el orden de sus secciones. Cada entrada cita la decisión de la SF que la fijó, con su título y su número entre paréntesis.

## Cómo es la incorporación

- **Una operación, sin tarea** («Incorporar un proyecto es una operación sin tarea, guiada por menús», 209; «Poner un proyecto al día con la SF, sin tarea», 199): incorporar y poner al día pasaban por crear una tarea con su rama, probarla y cerrarla en `develop`. El proceso ya está probado en la SF, así que esa ceremonia sobra: Claude dice qué va a cambiar, pide el OK y lo aplica en `develop` con su commit.
- **Nada del proyecto se mueve** («Incorporar un proyecto no mueve ni renombra nada», 201): la incorporación reorganizaba `docs/` según la estructura de la SF, y en un proyecto existente eso choca con su forma de trabajar, con su historial y con quien lo mantiene. El plugin se adapta al proyecto, y no al revés. La única excepción es pasar a `sf/` los documentos de la SF.
- **Lo fijo, lo que se detecta y lo que se elige** («La SF fija el mecanismo y se adapta a las convenciones del proyecto», 202): la SF impone solo su mecanismo (la cola, una rama por tarea, el número de la tarea en el commit, el registro de decisiones) y en lo demás se adapta a lo que el proyecto ya tiene. La corrigieron después la 205 y la 208: las ramas y las decisiones también son fijas.
- **Siempre `develop`** («El manejo del repositorio no se negocia: siempre develop», 205): la SF trabaja con su modelo de ramas, que forma parte del mecanismo que fija: se desarrolla en `develop`, cada tarea en su rama, que entra por squash, y publicar es pasar `develop` a `main` con su tag.
- **Un remoto en GitHub** («Sin remoto en GitHub no hay SF: se valida al incorporar y, si falta, se crea», 230): un remoto en otro servicio no cuenta y no se crea uno de GitHub a su lado. Es una limitación inicial a propósito: «más adelante nos replanteamos abrir el abanico. Por ahora KISS» (propietario).
- **Los commits los hace Claude** («Los commits los lleva siempre Claude», 225): forman parte del manejo del repositorio. Si los hiciera el desarrollador a mano se perderían los subagentes, el squash y revertir; lo que se adapta es su idioma y su formato.
- **La versión con su tag** («La versión forma parte del manejo del repositorio», 226): publicar es igual en todos los proyectos, pasar `develop` a `main` con el tag `vX.Y.Z`; no es un valor que el proyecto configure.
- **Las decisiones, siempre en `sf/decisiones/`** («Las decisiones son material de la SF: siempre en sf/decisiones/», 208): el registro de decisiones es material de la SF, con su formato (un archivo por decisión y su índice), y la SF lo lee y lo escribe; no se adapta al sitio ni al formato que tuviera el proyecto.
- **La gestión del repositorio se acepta o no hay SF** («La SF gestiona el repositorio a su manera: la incorporación no lo deja a elección», 285): incorporando un proyecto, la incorporación preguntó si Claude hacía los commits y, tras el «De acuerdo», volvió a preguntarlo con otras palabras al revisar su `CLAUDE.md`, ofreciendo dejar una regla que impedía cerrar. La gestión del repositorio es crítica y no puede haber malentendidos: se explica una vez, se acepta, y lo que choque se adapta avisando.
- **Sin mapa de documentos** («Sin mapa de documentos: o se sigue la estructura de la SF, o no se mapea», 229): se valoró que Claude los buscara o guardar sus rutas en `.sf/proyecto.json`; se eligió lo más simple: si el proyecto sigue la estructura de la SF, sus documentos están donde la SF los busca, y si no, no se mapean ni se preguntan rutas.
- **La orden de Python, la que da el mod** («La orden de Python sale del intérprete que se detecta, no de `python` fijo», 236): en macOS y Linux `python` suele no existir (allí es `python3`). Con el intérprete que detecta el mod, la SF funciona igual en Windows, macOS y Linux sin preparar nada.

## El progreso, en el panel

- **Abandonar lo borra todo** («La SF recarga sola los plugins en la incorporación; ACTUALIZAR recarga si basta y Abandonar lo borra todo», 286): abandonar es una decisión expresa del usuario y no debe dejar nada atrás. Si el progreso se borra a medias por otra causa, se guarda lo respondido para ofrecer seguir.
- **Esc pone en pausa, no borra** («Esc pone en pausa la incorporación, con Continuar y Abandonar en el panel», 258): Esc se pulsa a menudo para corregir algo o sin querer, y perder lo respondido molesta. Con los botones del panel, la pausa se ve y se resuelve con un clic.

## Antes de nada: el plugin al día

- **El mod recarga solo** (286; «La P no recarga el plugin», 103): incorporando un proyecto, la incorporación se paró para pedir `/reload-plugins` y no siguió sola; el propietario pidió que la recarga y la continuación fueran automáticas. Es una excepción, acotada a la incorporación, a la regla de que el mod no recarga por su cuenta: recargar queda a cargo del propietario.

## Actualizar

- **Remoto en GitHub, comprobado otra vez** (230): un proyecto con la SF tiene siempre un remoto en GitHub; al ponerlo al día se comprueba como al incorporar, por si falta o apunta fuera de GitHub.

## Reglas del proyecto: qué choca con la SF

- **Lo fijo del repositorio** (285): es lo que se busca en las reglas del proyecto porque no se deja a elección.
- **Documentos en otra carpeta no chocan** (229): la SF no los mapea.

## Procedimiento

- **Color de las sesiones, del estilo** («El color de sesión se deriva del color primario del estilo del proyecto», 310; «El color de sesión de la SF no se reserva: un proyecto puede salir del mismo color», 311): una sola fuente para el color del proyecto. No se reserva el de la SF: que hoy haya menos temas que colores es circunstancial.
- **El estilo de los documentos, más adelante si se quiere** («Un proyecto sin estilo.json se genera con los valores por defecto de un tema elegido por su color», 323): fijar el estilo no bloquea nada; sin él, los documentos salen con los valores por defecto de un tema y un aviso.
- **`master` puede hacer de `main`** («Si el proyecto tiene master, se pregunta si hace de main», 213): la SF no renombra ramas del proyecto (201), y crear `main` al lado de `master` dejaba dos ramas principales.
- **Rama solo en el remoto: se crea la local sin preguntar** («Si main solo está en el remoto, se crea la local sin preguntar», 234): la SF necesita en local `develop` y la rama que hace de `main`; si ya existe en el remoto, basta con seguirla, y se dice en el resumen.
- **Si no se acepta, se para sin cambiar nada** (285; «Sin develop no hay SF, y las decisiones mezcladas se sacan con enlace», 214; 225; 230): no hay opciones intermedias que dejen la SF a medias, sin poder cerrar ni publicar. Sin `develop`, sin un remoto en GitHub o sin que Claude haga los commits, la SF no se puede usar, así que la incorporación se para sin cambiar nada.
- **Mover secciones del `CLAUDE.md`, aparte** (201): reorganizar algo del proyecto es una petición aparte del propietario, nunca parte de la incorporación.

- **Los documentos de la SF, en la carpeta `sf/`, visible** («Los documentos de la SF van en la carpeta sf/», 203): en `docs/` chocaban con los del proyecto (uno lo tiene en inglés, otro usa `_docs/`). En `.sf/` quedaban escondidos: las búsquedas de Claude se saltan las carpetas con punto, Obsidian no las ve y en macOS y Linux no se ven en el explorador. Un nivel `sf/docs/` sobraba, porque en `sf/` solo van documentos.
- **`sf/propuestas.md`, creado al incorporar** («La incorporación crea docs/propuestas.md; el índice de decisiones sale del panel», 196): el panel muestra las propuestas del proyecto solo si el archivo existe. Hoy va en `sf/` (203).
- **Pasar a `sf/` lo que ya había** (203; 208; 201): los proyectos ya incorporados se pasan al sitio nuevo al ponerlos al día, por uniformidad, con el OK del propietario; es la única excepción a no mover nada. Un archivo que mezcla decisiones con otras cosas deja en su sitio un enlace a ellas y conserva lo demás (214).

- **Convenciones: kanban opcional, por defecto ninguno** («El kanban se elige, y por defecto ninguno», 224): JKanban no está conectado y un usuario nuevo no lo tiene; el proyecto funciona solo con su cola.
- **El idioma del proyecto** («Claude escribe en el idioma del proyecto y del desarrollador», 206): hay proyectos con sus documentos en inglés, y quien prueba la SF puede no trabajar en español. El modelo de ramas es fijo, pero el idioma se adapta: commits, tareas, pasos, informes y documentos.
- **El número de la tarea, según el formato de los commits** («El número de la tarea en el commit, según el formato del proyecto», 207): el número sirve a las personas, para ver en `git log` a qué tarea es cada commit. Un «(N)» al final rompe formatos estrictos como conventional commits; allí va al pie, `SF-Tarea: N`.
- **El prefijo del squash, del tipo de la tarea** («El título del commit en formato conventional sale del tipo de tarea», 233): la C del panel cierra sin pedir nada, así que el título tiene que salir solo: implementar da `feat`, corregir `fix`, los que entregan documentos `docs`; sin tipo, `chore`.
- **Manifiestos con versión** (226): se elige solo en qué archivos se sube el número; el tag va siempre.
- **La firma, configurable; sin configurar, sin línea** («La firma del commit de cierre es configurable; sin configurar, sin línea», 238): la línea fija «Co-Authored-By: Claude Opus…» no servía a todos. Se recomienda la de Claude con el modelo de la sesión, porque los commits los hace Claude.
- **Cambiarla después, con su skill** («La configuración se cambia pidiéndoselo a Claude, con menús», 228): la configuración puede cambiar tras incorporar; el propietario prefirió una skill y una orden propias (`/sf_config`) a un caso más dentro de la incorporación.

## Comprobación final y al terminar

- **Remoto en GitHub** (230): sin él no hay SF, así que se comprueba al final que existe, apunta a GitHub y tiene subidas las ramas.
- **Lo que falla de la SF no se anota en el proyecto** («Un proyecto solo anota propuestas suyas», 210): las propuestas de cada proyecto se llenaban de cosas de la SF que nadie del proyecto iba a hacer. Llevarlo a la SF es cosa del propietario, en una sesión de la SF.
- **Las reglas llegan con el siguiente mensaje, sin reiniciar** («Tras incorporar, el mod entrega las reglas sin reiniciar», 242): el mod guardaba que la carpeta no era de la SF hasta recargar, y ni `/clear` entregaba las reglas. Ahora, al ver `.sf/proyecto.json`, las entrega con el siguiente mensaje; `/clear` queda de respaldo.
- **La pantalla completa, al terminar** («Bienvenida del panel publicada y pantalla completa al incorporar», 245): se ofrecía en el primer mensaje, también en una carpeta sin la SF; tiene sentido cuando el proyecto ya la usa.
