# Por qué de cada regla

El porqué, los datos y la decisión de cada regla de la skill, en el orden de sus secciones. Las decisiones están en `docs/decisiones/` de la SF, con el número entre paréntesis.

## Carga

- **Al empezar la sesión y tras cada compactación, no en cada mensaje**: cada carga añade unos 4.000 tokens. Solo el principal: el subagente sigue su encargo (propietario, 2026-10-31).

## Papel del orquestador

- **El principal orquesta; los subagentes ejecutan** (083): el principal define, decide y lleva la cola; ejecutar le ocupa y deja al propietario esperando.
- **Todo pasa por la cola**: así el panel da el control y el foco («El objetivo del panel es el control y el foco», 143). Toda tarea en curso tiene su subagente, así que el principal queda libre para el propietario («Todo el trabajo de la tarea, a su subagente», 151).

## Al llegar un mensaje

- **Consultar la cola antes de actuar**: el propietario la cambia desde el panel. Pasó con un aviso de choque de la 210 con la 195, que él ya había cerrado (propietario, 2026-10-31; «Orquestación con un subagente vivo por tarea», 149).
- **Clasificar la petición antes de anotarla** («Lo que pinta la SF y lo global no son del proyecto», 167): en otro proyecto, ante «esto fuera» sobre la línea gris del panel, la sesión la tomó por suya y propuso cambiar el script global de la línea de estado. Lo de la SF se hace en una sesión de la SF; `~/.claude` afecta a todos los proyectos. El mod pone la misma regla en el prompt de sistema fuera de la SF, para que llegue también a los proyectos atrasados. Lo de la SF tampoco se anota en el proyecto: en otro proyecto, una corrección de cómo habla la SF acabó en su `docs/propuestas.md` («Un proyecto solo anota propuestas suyas», 210).
- **Bugs, a la cola antes de investigarlos**: uno se investigó en el chat y no se veía en el panel. «Intento que todas las tareas pasen por el panel» («Los bugs son tareas nuevas», 096). Errores ajenos a la tarea: «Errores detectados, a Pendientes» (077).
- **Un fallo propio también es bug**: con la 216, el propietario no pudo cerrar desde el panel porque faltaba `cola.py listo`; se explicó el olvido y se cerró a mano sin anotar nada. «¿No consideras un bug lo que ha pasado?». Un olvido que se repite pide una regla, o código (propietario, 2026-11-01).
- **Sin tarea en curso no se trabaja**, salvo para reorganizar la cola (149).
- **Anotar al llegar, aunque esté sin concretar** («Lo que falta por concretar va como pasos de la tarea», 211): en otro proyecto, Claude dejó una petición en la conversación: «Cuando me digas qué quieres cambiar, lo anoto como tarea en curso». «Si el enunciado no basta, preguntar» se leía como preguntar antes de anotar, y lo que queda en la conversación se pierde. Lo que falta (concretar, deliberar, decidir o diseñar cómo) son pasos de la tarea.
- **Menú al anotar**: el propietario quiere elegir en el momento si empieza una tarea o la deja pendiente; sin pasos, cada subtarea acababa como tarea suelta («Menú al anotar: paso, en curso o en cola», 139).
- **Agresivo con los pasos y las fusiones**: los cambios pequeños como tareas sueltas llenaban la cola (propietario, 2026-10-31, tarea «Skill de orquestación», 205).
- **La tarea incluye lo que permite probarla**: la de descartar y revertir se cerró sin su botón y no se pudo probar (propietario, 2026-10-29).
- **Guiar, no solo ejecutar** («La SF guía el desarrollo: observa y sugiere cómo avanzar», 235): las sugerencias llegaban a petición o tarde. El propietario: «la SF es la guía que organiza el desarrollo, observando las tareas, el proyecto y al desarrollador». Solo sugerir: decide él.
- **Lo útil para terceros, en el plugin** («Lo útil para terceros viaja en el plugin, no en la memoria ni en CLAUDE.md», 247): al pedir el propietario que los descartes llevaran contexto, Claude lo guardó en su memoria, que solo ve quien trabaja en esa carpeta y esa máquina. «Todas tus propuestas para la sf que sean de utilidad para terceros no las guardes en memoria ni en claude.md sino en alguna parte en la que viajen con el plugin».

## Poner en curso

- **Especificar y planificar**: una tarea con solo «Probar» y «Cerrar»: «Me hace pensar que no has hecho nada». Sin pasos, el panel no muestra el trabajo (149).
- **Planificar sin pedir aprobación** («El principal planifica los pasos sin pedir aprobación», 181, que sustituye a la 180): esperar el OK de los pasos era un paso más del propietario. «No pidas confirmación, confío en ti». Enseñarlos al avisar le deja corregirlos.
- **Choques**: dos tareas sobre los mismos archivos chocaban al cerrarse con squash, cuando ya estaba todo hecho («Prever choques al poner una tarea en curso», 130).

## Pasos

- **Definir y decidir son pasos** (080), también concretar y deliberar (211); **en participio al hacerse** (081). Se notó al proponer un criterio sin anotar ningún paso.
- **Tareas de definición**: no ejecutan una idea, la definen; correr a implementar se salta el diálogo (propietario, 2026-10-30).
- **Mejorar la skill que se usa es un paso** (094): lo aprendido llega a la skill mientras está fresco.
- **Paso «Esperar a …»** («Una tarea que espera y no puede volver a la cola lleva un paso «Esperar a …»», 178): con commits en su rama, una tarea no vuelve a la cola (170; con la rama vacía, sí, 275); el paso dice en el panel por qué está parada. Pasó con la 229, que esperaba el cierre de la 255.
- **/sf_paso, a su subagente** («/sf_paso pone a Claude con el paso», 072; 151): el panel lo escribe y lo pasa a Claude como mensaje; hacerlo en el principal era trabajo de la tarea fuera de su subagente (auditoría de la orquestación («Auditar que la skill de orquestación recoge todo lo ordenado», 216)).

## Subagentes

- **Lanzar sin preguntar y sin esperar** («El subagente se lanza sin preguntar», 086; 105): esperar por compartir archivos o preguntar ocupaba al propietario «cuando no se me necesita». Nunca las de la cola: se lanzaron cuatro y hubo que pararlas. TURBO lo pide desde el panel («Cabecera en dos filas y botón TURBO», 120): pone en curso, con su subagente, las de la cola que no necesitan al propietario y lanza el de las en curso que no lo tienen; su objetivo es mover tareas pendientes a en curso («TURBO pone en curso las tareas que no necesitan al propietario», 160, que sustituye a la 153).
- **Un subagente vivo por tarea, también en la prueba** (149, que corrige la 083): los ajustes de la prueba ocupaban al principal. La 196 llevó 12 ajustes en unas 2,5 h y unos 360.000 tokens; la 210, 9 ajustes en unos 25 minutos. El propietario: «tener subagentes esperando instrucciones y dejando libre el agente principal lo veo una gran ventaja».
- **Todo el trabajo de la tarea, también el análisis, al subagente** («Todo el trabajo de la tarea, a su subagente», 151): «lanzar las que no necesitan al propietario» dejó al principal clasificar memorias y analizar la incorporación en una tarea de diseño («Las normas guardadas en la memoria de la SF, también en los demás proyectos», 211) porque esperaba decisiones. Esperar al propietario no quita el subagente: analiza, propone y queda vivo; el principal solo lleva las preguntas y registra.
- **El encargo y el informe con formato fijo** (083). Lleva las reglas de «Cómo escribir», porque el subagente no carga esta skill, y el informe dice qué documentos compartidos actualizar, porque el subagente no los toca (auditoría de la orquestación («Auditar que la skill de orquestación recoge todo lo ordenado», 216)). Solo el principal escribe la cola; el mod lo impone a las herramientas de archivos («El mod impide que un subagente escriba la cola», 110).
- **Recoger en cuanto vuelve** (149): si no, el panel queda desfasado.
- **Ramas del subagente, borradas al cerrar** («Borrar las ramas del subagente al volver», 135): se acumulaban ramas sueltas.
- **El worktree se quita al cerrar, no para probar** (149): con el subagente en su rama auxiliar, la rama de la tarea queda libre; la C falló en la 194 porque su worktree tenía activa la propia rama de la tarea.
- **Cerrar con la C también para el subagente**: el panel cierra sin poder pararlo ni quitar su worktree; quedaba vivo (auditoría de la orquestación («Auditar que la skill de orquestación recoge todo lo ordenado», 216)).

## Probar y cerrar

- **`listo --prueba` al acabar el último paso** (090, 149): sin los pasos de cierre el panel no muestra la C.
- **Probar antes de cerrar** (074): la observación se llenaba de tareas cerradas sin probar en su rama.
- **Cerrar directamente lo que no tiene nada que probar**: deliberar, investigar, documentar o especificar no se prueban como el código; el propietario aprueba el resultado («Cerrar directamente lo que no tiene prueba», 154).
- **El cierre espera el OK** («Preguntar antes de cerrar una petición; lo nuevo, a la cola», 048): Claude cerró y publicó una skill sin permiso. Los commits en la rama, sin preguntar.
- **Descartes con contexto** (propietario, 2026-11-03, tarea 324): se proponía descartar una tarea duplicada citándola por su número, y el propietario no recuerda cada tarea por su número; con qué pedía, dónde quedó hecha y qué supone, decide sin buscarla.
- **«Ciérrala» sin número, la rama activa** (095): se cerró otra tarea tras un cambio de rama.
- **La pregunta de «¿Cómo va?»** por las en observación (050, 051, 204): el menú anterior mezclaba tareas y no decía qué era cada una; se cierra o se revierte, en el lenguaje de la SF.
- **Cambios, comprobaciones y pendientes reales al acabar** (regla del `CLAUDE.md` de la SF y del informe de los subagentes): no viajaba al principal de los proyectos, que daba por hechas operaciones y verificaciones sin confirmarlas.
- **Cada comprobación, paso hecho de su tarea** («Las comprobaciones y pruebas hechas se anotan como pasos de su tarea», 288): el propietario quiere ver en el panel, mirando la tarea, qué se ha comprobado de verdad, sin buscarlo en los informes ni fiarse de un resumen. Por eso el encargo pide «Lo comprobado» en lista, una línea por comprobación, lista para pasar a pasos. Una sola orden, `comprobado`, añade el paso ya hecho y no devuelve a pendiente «Activar rama para poder probar»: anotarlo tras la prueba del propietario no le obliga a probar otra vez. El campo `comprobado` de la tarea se retiró: un solo sitio, sin dos versiones.
- **Un cierre que falla pasa a Claude** (111).

## Fusionar, separar y redescribir

- **Sugerir fusiones y splits** («El orquestador sugiere fusiones y splits», 100).
- **Redescribir tras fusionar** (141): la descripción resultante se leía como dos textos pegados.
- **Título desfasado: renombrar, redescribir o separar** (149): `/sf_redescribir` solo cambia la descripción («Redescribir: Claude vuelve a redactar una descripción», 126), así que el título se propone aparte; si la tarea pierde el foco, se separa (auditoría de la orquestación («Auditar que la skill de orquestación recoge todo lo ordenado», 216)).
- **Sugerir partir o cerrar la tarea que crece** (235): «Tipos de tarea» (274) acumuló dieciséis pasos y diecisiete preguntas antes de partirse. «Si una tarea crece mucho en pasos, sugerir splits y cierres si tu valoración es positiva». Sin umbral fijo: `cola.py lista` da la cuenta y el criterio lo pone el principal; un aviso mecánico se propone aparte.

## Documentos compartidos

- **Tarea aparte** (112, 116): cada cierre chocaba en esos documentos; el paso de documentar bloqueaba la C, y ahora es «Creada la tarea NN…», hecho.
- **También por subagente, de una en una** («Documentos compartidos, también por subagente», 152, que precisa la 112): de una en una para no tener dos en paralelo sobre el mismo documento, no para que las hiciera el principal.
- **Una tarea por documento, con un paso por tarea** (142, 147): la de «Cómo funciona el panel» llegó a 19 pasos casi iguales. **Las reglas del método, en una sola** (148): los tres documentos repetían lo mismo.

## Libre

- **Desbloquear las tareas en curso** («Libre, el orquestador desbloquea las tareas en curso», 102): se quedaban paradas esperando respuestas que nadie pedía.

## Preguntar

- **Opciones con `description` vacía** (240): la herramienta exige el campo y, sin él, la llamada falla; por eso cada opción repetía su etiqueta debajo («Tarea nueva en cola: tarea propia de corregir, en cola»). El esquema lo acepta vacío (`string` sin longitud mínima, Claude Code 2.1.316).

- **Las decisiones, a develop en cuanto se toman** («Las decisiones, a develop en cuanto se toman», 155): escritas en la rama de una tarea chocaban con su subagente, y escritas por el subagente esperaban al cierre. Aplicarlas sigue siendo trabajo de la tarea. Escritas a mano con la rama de una tarea activa, se quedaban en esa rama: por eso las registra `cola.py decision`, que hace el commit en `develop` sin cambiar de rama (tarea 283).

## Escribir

- **Textos compactos** (040): el panel es estrecho; «de la SF» no aporta.
- **Título con el resultado buscado** (251): «El panel de la SF muestra la versión publicada, no una antigua» se leía como lo que ya pasaba.
- **Sin referencias por número que no se vean en pantalla** (150): «los humanos no tenemos un json fácil de consultar».
- **Descripciones sin origen** (098): «me enredan la descripción». **Cada idea en su párrafo** (125).
- **Tareas internas legibles** (186): las que mejoran el trabajo de Claude se titulaban con su mecánica y el propietario no sabía para qué servían («¿qué hace en realidad esta tarea?»).
