# Por qué de cada regla

El porqué de cada regla de la skill, en el orden de sus secciones y tarjetas (primero `SKILL.md`, después `references/estados.md`). Cada entrada cita la decisión de la SF que la fijó, con su título y su número entre paréntesis. Algunos números de `estados.md` son de tareas, no de decisiones: se dice en su entrada.

## Cómo se cambia la cola

- **Toda escritura, por el CLI, con historial y copias** («Flujo de tareas: un CLI común, historial por tarea y copias de la cola», 113): las reglas de los cambios de estado estaban repartidas entre varios documentos y el código del panel, y el panel deducía lo ocurrido comparando lecturas de la cola, con errores (una H en lugar de una A, reabiertas falsas). Un solo CLI aplica cada regla una vez, para Claude y para el panel; el historial de cada tarea dice qué pasó sin deducirlo, y las copias permiten volver atrás.
- **Los detalles del CLI** («Flujo de tareas: respuestas a la revisión de la tabla de estados», 115): la tabla de estados dejó 23 huecos e incoherencias entre las reglas escritas y el código del panel. Esta decisión los responde uno a uno; `estados.md` cita su punto entre paréntesis, como «115 (9)».
- **La orden de Python, la que diga el mod** («La orden de Python sale del intérprete que se detecta, no de `python` fijo», 236): en macOS y Linux `python` no suele existir y es `python3`. Con el intérprete detectado (3.9 o posterior), la SF funciona igual en Windows, macOS y Linux sin preparar nada.
- **El panel lanza una copia de cola.py hecha al cargar** («El panel ejecuta una copia de cola.py hecha al cargar», 136): el panel queda en memoria tal como se cargó, pero lanzaba `cola.py` desde el disco, y cerrar o activar una rama cambia la carpeta de rama (en la SF, el plugin es la propia copia de trabajo). Con la copia, panel y CLI van siempre a juego.

## Reglas que no hace el CLI

- **Solo el principal y el panel escriben la cola** («El principal orquesta; los subagentes ejecutan», 083; «El mod impide que un subagente escriba la cola», 110): el principal lleva la cola y habla con el propietario; si cada subagente la escribiera, chocarían. El mod bloquea las herramientas de archivos de un subagente sobre la cola; las órdenes de terminal no se controlan, por eso la norma sigue escrita.
- **Sin tarea en curso no se trabaja; reorganizar la cola, sí** («Orquestación con un subagente vivo por tarea», 149): todo trabajo queda en una tarea que el panel enseña. Fusionar, separar, redescribir, añadir pasos o cambiar tipos no es trabajo de una tarea, sino ordenar la cola.
- **El OK del propietario para cerrar, pasar a observación y descartar** («Preguntar antes de cerrar una petición; lo nuevo, a la cola», 048): Claude terminó una skill, hizo su commit, la publicó y la cerró sin preguntar. Cerrar o tirar trabajo lo decide el propietario.
- **Una tarea en curso con trabajo no vuelve a la cola** («Una tarea en curso con rama no vuelve a la cola», 170): `en-cola` dejaba una rama viva sin subagente ni trabajo en marcha. Para dejarla, se cierra, se pasa a observación o se descarta. Con la rama vacía no hay nada que perder: se borra y vuelve a la cola (lo cita como 275, que es la tarea que lo hizo, no una decisión).
- **Pasos según el tipo** («Las tareas de código no llevan pasos de documentación», 240): una documental solo toca su documento y una de código, solo el código y lo que va con él. En un proyecto, una tarea de código acabó con un paso para explicar algo en el material del curso; mezclarlos hace chocar las tareas en los mismos documentos.
- **Choques antes de poner en curso** («Prever choques al poner una tarea en curso», 130): dos tareas que tocan los mismos archivos chocaban al cerrarse con squash, cuando ya estaba todo el trabajo hecho. Mirarlo al empezar deja esperar o fusionar a tiempo.
- **Las deliberativas, sin rama ni prueba** («Las tareas de investigar no tienen rama», 256; «Una tarea deliberativa da un informe y las tareas que salgan», 218; «Una deliberativa solo escribe su documento, sin rama; lo demás va a tareas propias con rama», 278): una investigación no cambia el repositorio, devuelve un análisis; una rama vacía no aporta nada y estorba al cerrar (al cerrar una, el squash de una rama sin cambios falló). La deliberación se cierra limpia con su documento, y los cambios en otras piezas se prueban y se cierran como cualquier tarea, en la suya. En una deliberativa no se prueba nada y solo cambia documentos: se cierra con la aprobación del propietario, sin observación, y por eso su único paso de cierre es «Cerrar la tarea».
- **Rama antes del primer activo; el subagente, en una auxiliar** («Orquestación con un subagente vivo por tarea», 149): con el subagente en su rama `sub-NN`, la rama de la tarea queda libre y Activar rama y Cerrar funcionan con el worktree puesto. Cerrar falló en una tarea porque su worktree tenía activa la propia rama de la tarea.
- **cola.py recoge el subagente** («cola.py recoge el subagente al dejar la tarea sin él», 169): el principal quitaba a mano worktrees y ramas auxiliares, y se quedaban. El CLI lo hace en toda orden que deja la tarea sin subagente, sin forzar nunca, para no perder trabajo.
- **Descartar quita todo** («Descartar borra también la rama del subagente», 189): la recogida sin forzar dejaba, al descartar, la auxiliar y su worktree. Descartar ya es decidir tirar ese trabajo.
- **La firma de los commits, configurable** («La firma del commit de cierre es configurable; sin configurar, sin línea», 238): el squash firmaba siempre con una línea fija de Claude. Cada proyecto decide su línea de coautoría; sin configurarla, no se pone ninguna.
- **Subir develop con revisión** («Revisión antes de publicar: bloquear en público, preguntar en privado, y revisar también al subir develop», 259): en un repositorio público, lo que se sube a `develop` ya es visible. Antes de subir se buscan secretos, datos personales, rutas de la máquina y documentos internos; si hay algo nuevo, no sube.
- **Las comprobaciones, como pasos hechos** («Las comprobaciones y pruebas hechas se anotan como pasos de su tarea», 288): el propietario quiere ver en el panel, mirando la tarea, qué se ha comprobado de verdad, sin buscarlo en informes ni fiarse de un resumen. Anotarlo no devuelve la tarea a la prueba, y el campo `comprobado` se retiró para tenerlo en un solo sitio.
- **Fusionar y separar los escribe el propietario; dos de un mismo documento, el principal** («Una tarea por documento que actualizar», 142): cada cambio abría su tarea de documentación y después había que fusionarlas a mano. Las de un mismo documento son una sola, así que juntarlas no necesita decidir nada.

## Todo cierre y revertir

- **Los pasos de cierre, desde que la tarea entra en curso** («Los pasos de cierre, desde que la tarea entra en curso», 174): los añadía `listo` al acabar; si el principal lo olvidaba, el panel no ofrecía Cerrar, y al relanzarlo el paso de prueba se repetía. Así toda tarea en curso muestra su camino completo desde el principio.
- **`listo` se niega con pasos de trabajo sin hacer** (447): una tarea salió en verde con un paso sin marcar y Cerrar se negó por él. Negarse en `listo` lo dice antes, no al cerrar; «Esperar al propietario:» no cuenta porque puede ir a la vez que lista para probar.
- **El paso de prueba es activar la rama; el OK es cerrar** («El paso de prueba es «Activar rama para poder probar»», 172; «Cerrar exige siempre el paso de cerrar; quitar el de probar es cerrar sin probar», 121): la C del panel ya es el OK del propietario («probada, ciérrala»); lo que pone la tarea en prueba es activar su rama. Todo cierre pide «Cerrar la tarea», con rama o sin ella: antes, sin rama, se cerraba con pasos de trabajo pendientes.
- **Las ayudas de prueba no bloquean** («Ayudas de prueba: tras activar la rama y no obligatorias para cerrar», 184): un paso de prueba añadido antes de los de cierre impedía que el panel ofreciera Cerrar, y el propietario no sabía cómo cerrar la tarea.
- **Revertir elimina o deja pendiente** («Revertir elimina la tarea o la deja pendiente», 134): una tarea revertida no está hecha, así que no debe quedar en Cerradas: o se abandona, o hay que rehacerla.

## 1. Estados y marcas

- **En cola y en curso; lo nuevo, a la cola** («Cola de peticiones y un commit por petición», 031; 048; «Menú al anotar: paso, en curso o en cola», 139): las peticiones llegaban a mitad de otra tarea y se acumulaban sin registro, con varios cambios en un mismo commit. Anotarlas al llegar las hace visibles; el menú deja al propietario elegir en el momento si la empieza.
- **En observación** («Sin probar hasta el OK del propietario; preguntar antes de cambiar de tarea», 050; «La letra es el estado: A, H, T y C…», 054; «Flujo de tareas: respuestas a la revisión de la tabla de estados», 115; «Los estados de las tareas se nombran con el lenguaje de la SF», 204; y el nombre de hoy, de la decisión 212): Claude sacaba de la cola lo que solo él había comprobado, sin que el propietario viera su funcionamiento. La tarea ya está en `develop` y se vigila con el uso; el nombre de antes sugería que faltaba probarla, y la forma de cerrarla describía mal lo que pasa: se cierra si va bien o se revierte si va mal.
- **Descartada, hasta limpiar** («Descartar y revertir una tarea», 078; «Botón D para descartar una tarea», 088): cada acción según el rastro que deja la tarea: se elimina lo que no deja rastro, se descarta lo empezado que no ha entrado en `develop` y se revierte lo que ya entró. La descartada se ve en Cerradas hasta limpiarla, sin pedir motivo.
- **«La miro ahora»** («La tarea que se está … en curso», 060): mientras el propietario la mira, el panel la trata como en curso, para que se vea en qué está.
- **Lo que sale de la cola, a `historial.jsonl`** (115, puntos 2 y 3): una eliminada «sin rastro» sale de la vista, pero su historial queda para recuperarla.
- **Cerrada** (050; «Pasos de cierre: probar y cerrar la tarea», 090; «Botón C para cerrar una tarea», 101): la prueba depende del propietario y el cierre, de su OK: por eso son dos pasos. La C cierra sin pasar por Claude.
- **Eliminada** («Eliminar una tarea», 079; 115; 134): se elimina sin rastro solo lo que no ha cambiado ningún activo (lo escrito y versionado en el repositorio); lo que ya tiene trabajo se descarta o se revierte.
- **Absorbida** («/fusionar junta tareas en una», 099): el mod fusiona sin Claude, también a mitad de turno; queda una sola tarea.
- **Revertida, solo las antiguas** («Botón R para revertir una tarea», 107; 134): el revert deshace en `develop` el squash de la tarea. Desde la 134, una revertida ya no queda en Cerradas con R.
- **Nombres de antes, convertidos al cargar, sin alias** (««En observación», sin alias ni rastros», 215): mantener alias o valores viejos deja dos nombres para lo mismo.
- **La rama marca el trabajo efectivo** («Eliminar una tarea», 079; «Una rama de feature por tarea», 082): la rama se crea antes de tocar el primer activo, así que tener rama es tener trabajo: deja de poder eliminarse y pasa a descartarse.
- **Pasos con estado** («Pasos de una tarea», 067): un paso no es una tarea ni lleva número; solo es tarea nueva lo que cambia el alcance. El panel muestra la cuenta.
- **Reabierta** («Un bug en una tarea cerrada la reabre con su número», 061; «Cerradas: todo cambio en el cierre de una tarea», 064): el fallo queda unido a la tarea que lo causó, en lugar de abrir otra.
- **La letra es el estado** (054; «Código de tarea: número y estado, «57-A»», 058): la A y la H solo decían de dónde venía la tarea; con la letra del estado se ve en qué está en todos los sitios.
- **Una H no pasa a A** («Bloque TAREAS con A y H», 053; «Una tarea reabierta lleva H», 069): la cola pasa de una sesión a otra; una reabierta no es nueva aunque entre en la sesión.
- **D en Cerradas** («Letras E, D y R en los botones de las tareas», 089): la D es también la letra de la descartada.
- **La tarea en curso, en amarillo** («La tarea en curso, en amarillo», 039; «El código de la tarea en curso, en amarillo también en las secciones», 084): el color del proyecto se leía mal sobre el fondo oscuro del panel; el amarillo la distingue en todos los proyectos.
- **Verde con «●» si tiene commit** («Hecho en esta sesión: peticiones cerradas», 044): el panel guarda texto y commit al cerrarse cada tarea, porque después salen de la cola.
- **El panel lee el historial, no compara colas** (113): deducir lo ocurrido comparando lecturas daba letras falsas. La tarea 145 pasó el panel a leer el historial.

## 2. Cambios de estado

- **Quién escribe la cola** (083, 110, 115): ver «Reglas que no hace el CLI».

### Alta y arranque

- **Crear al llegar** (031; «Errores detectados, a Pendientes», 077; «Los bugs son tareas nuevas», 096): un error ajeno a la tarea no se arregla de paso ni se queda en el chat; un bug investigado en el chat no se veía en el panel.
- **Descripción sin origen** («Las descripciones, sin origen», 098): «Separada de la 89» o quién la creó no dicen qué es la tarea y enredan la descripción.
- **El panel ejecuta las órdenes él mismo** («Comandos antes que inferencia», 092): un prompt a Claude para cambiar de rama era lento, gastaba inferencia y el resultado podía variar. Lo que hace un comando, lo hace el comando; Claude solo entra donde hace falta criterio.
- **Crear en curso** (048, 139): el propietario elige en el menú si la empieza ya.
- **Poner en curso** (048; «La P no recarga el plugin», 103; 130): preguntar por una tarea pendiente es empezarla. Activar rama solo cambia de rama: recargar el plugin solo hace falta en la SF y lo decide el propietario.
- **Dejar para luego** (115, punto 9; 170): el principal la deja con el OK del propietario; con trabajo en su rama no vuelve a la cola (arriba). El «(275)» es la tarea que dejó volver a la cola una tarea con la rama vacía.
- **Crear la rama, avisando** (079, 082; 115, punto 16): una rama por tarea, creada antes de tocar el primer activo; al principio se pedía autorización y desde la definición completa solo se avisa. El principal la anota antes de lanzar al subagente. Las deliberativas no la tienen (256, 278).

### Durante el trabajo

- **Añadir un paso** (067; «/paso pone a Claude con el paso», 072; «Definir y decidir también son pasos», 080; 115, punto 11): `/paso` escribe el paso y se lo pide a Claude como un mensaje del propietario. Definir, diseñar y decidir también son trabajo y se ven en el panel.
- **Un paso nuevo devuelve la prueba a pendiente** (174): lo que se añade después hay que probarlo otra vez.
- **Ayudas de prueba** (184): arriba.
- **Los textos de cierre no se tocan** («Los pasos de cierre, desde que la tarea entra en curso», 174): los pasos de cierre los pone cola.py una vez y al final, así que su texto no cambia, otro paso no toma el suyo y un repetido se quita.
- **Marcar un paso, en participio** («Pasos hechos, en participio», 081): así el texto dice también si está hecho.
- **No quitar los pasos de cierre** («/paso pone a Claude con el paso», 072, ampliada; «Pasos de cierre fijos y E con confirmación para quitar pasos», 117; 121; 172; 174): un clic suelto bastaba para perder un paso, también los de cierre. La 117 está sustituida en parte por la 121 («Probar la tarea» se podía quitar para cerrar sin probar); desde la 174 no se quita ninguno, porque cerrar ya no exige el de prueba y lo marca al cerrar.
- **Renombrar y redescribir** (067; «Al fusionar, cada descripción en su párrafo», 125; «/redescribir: Claude vuelve a redactar una descripción», 126): al añadir pasos, el nombre dejaba de reflejar la tarea; al fusionar, las descripciones quedaban pegadas en un bloque difícil de leer. Claude la redacta de nuevo sin quitar ni añadir y espera el OK.
- **Lanzar el subagente** (083; «El subagente se lanza sin preguntar», 086; «Lanzar sin esperar lo que no necesita al propietario», 105; 149; «Todo el trabajo de la tarea, a su subagente», 151; «Documentos compartidos, también por subagente», 152; «TURBO pone en curso las tareas que no necesitan al propietario», 160): esperar o preguntar ocupaba al propietario sin necesitarle; un subagente vivo por tarea deja libre al principal para hablar con él. En una tarea de diseño, el principal hizo él mismo el análisis porque la tarea esperaba decisiones: todo el trabajo, también analizar, es del subagente. Las «Actualizar <documento>» también tienen el suyo, de una en una para no tener dos sobre el mismo documento. TURBO pone en curso lo que se puede hacer sin el propietario.
- **El subagente, en una auxiliar** (115, puntos 14, 15 y 17): la rama de la tarea puede estar ocupada; el subagente trabaja en una auxiliar y el principal la trae con `git merge --ff-only`.
- **La marca del subagente** («La marca del subagente, verde trabajando y roja en espera», 162): verde mientras trabaja, roja mientras espera instrucciones; parado, sin marca.
- **Volver de un subagente** (083; 115, punto 15; «Borrar las ramas del subagente al volver», 135; 149; 151; 169): al quitar el worktree, la auxiliar y la `worktree-agent-<id>` quedaban sueltas; se borran tras comprobar que no tienen commits fuera de la rama de la tarea. El subagente sigue vivo hasta el cierre: los ajustes de la prueba ocupaban al principal (una tarea llevó 12 ajustes en unas 2,5 horas).
- **Commit de guardado** (082): los pasos van en la rama de la tarea, que entra en `develop` por squash.

### Prueba

- **Lista para probar** (174; «Probar antes de cerrar», 074; 090; 121; «Cerrar directamente lo que no tiene prueba», 154): probar antes de cerrar deja menos tareas en observación. Lo que no tiene nada que probar (deliberar, documentar…) se cierra directamente: el OK del propietario es la aprobación. Que una tarea antigua reciba sus pasos de cierre al cargar y se quite un repetido lo cita como 253, que es una tarea.
- **Cerrar y A observación también sin rama** («Cerrar y pasar a … desde el panel también las tareas en curso sin rama», 188, con el nombre de antes de «En observación»): una tarea en curso sin rama había que cerrarla a mano con `cola.py`.
- **Anotar lo comprobado** (050; 288): lo comprobado se ve en la tarea y no se confunde con lo probado por el propietario.
- **Activar rama integra develop** («Botón P para probar una tarea en su rama», 091; 092; 103; 121; «Activar rama integra develop, avisa a Claude si choca y adelanta la rama del subagente», 191): se prueba con lo último y el cierre no choca; si choca o falta traer trabajo del subagente, el panel se lo pasa a Claude, como al cerrar. Adelantar la auxiliar evita que falle el siguiente `--ff-only` del principal. El «(270)» es la tarea que hizo la integración, de la que salió la 191; el «(253)» de «ya era la activa», otra tarea.
- **Mirarla ahora y seguir en observación** («La pregunta de «¿está probada?»: una por petición, con tres respuestas», 051; 060): el menú daba números sin decir qué era cada tarea y mezclaba varias; una pregunta por tarea, con su título y qué mirar.

### Cierre

- **Cerrar con squash** (082; 090; 101; 115, puntos 5, 18, 19 y 20; 121): el hash del squash entra en el historial para poder revertir; un push que falla no impide el cierre y queda anotado; una propuesta que toca un activo lleva rama y squash.
- **Se niega con trabajo del subagente sin traer** («Cerrar se niega si el subagente tiene trabajo sin traer», 200): el squash lo perdería. El propietario se lo pide a Claude, que lo trae, lo revisa y, si hace falta, lo prueba antes de cerrar.
- **El prefijo del commit sale del tipo** («El título del commit en formato conventional sale del tipo de tarea», 233; «El número de la tarea en el commit, según el formato del proyecto», 207): la C cierra sin pedir nada, así que el título tiene que salir solo. El número va como «(N)» o, si el proyecto tiene un formato estricto, en el trailer `SF-Tarea: N`, para no romper su formato.
- **Cierre que falla** («Un cierre que falla pasa a Claude», 111): el panel lo deshace y le pasa a Claude la tarea, la rama y los archivos en conflicto; el propietario ya no tiene que contarlo.
- **Cerrar sin rama** (048; «Cierre de tareas: propuestas sin … y Cerradas a 0», 063; 090; 115, punto 20; 121; 188; 278): una tarea que no tocó ningún activo no tiene nada que observar en `develop`; una deliberativa siempre se cierra así.
- **Cerrar y dejar en observación** (050; 054; 074; 115, punto 4; 121; 154; 188): lo que solo se ve funcionando tras el cierre se cierra y se observa. En observación ya no se descarta, se revierte: ya entró en `develop`.
- **Cerrar en observación** («Lo probado sale de Sin probar», 042; 050; 051; 064; «La tarea que se prueba es la de la rama activa», 095; 115, punto 4; 204; 215): un «ciérrala» sin número podía ser la tarea de la rama activa o la última de la que se habló; es la de la rama activa y, en duda, se pregunta. La 042 está sustituida en parte por la 050: lo que solo ha comprobado Claude ya no sale de la cola.

### Deshacer

- **Descartar** (078; 088; 089; 092; 115, punto 4): la D descarta lo empezado que no ha entrado en `develop`, sin motivo.
- **Limpiar Cerradas** («Cerradas: botón para quitar …», 057; «El botón de Cerradas se llama «limpiar»», 087; 088): un botón en la fila del título, sin gastar una fila.
- **Limpiar al empezar sesión** (078, 088): las descartadas no se arrastran de una sesión a otra.
- **Revertir** (078; 107; 115, puntos 4 y 18; 134): lo que ya entró en `develop` no se descarta, se revierte; el commit sale del historial.
- **Reabrir** (061; 064; 069; 096; 083; 115, puntos 6 y 7; 149; 151; 169): el bug se une a su tarea, con una rama nueva desde `develop`. Un worktree viejo no se reutiliza.
- **Eliminar** (079; 089; 115, puntos 3 y 8): solo lo que no tocó ningún activo; su historial queda para restaurarla.

### Juntar y separar

- **Fusionar** (098; 099; «El orquestador sugiere fusiones y splits», 100; «Tras una fusión, redescribir la tarea resultante», 141; 142): la tarea resultante se leía como dos textos pegados; por eso, tras fusionar, se propone redescribirla. El «(227)» es una tarea.
- **Queda la que tiene el trabajo, y la resultante se retitula y se ordena** («Al fusionar queda la tarea que tiene el trabajo, y la resultante se retitula y se ordena», 358): quedarse siempre con la de número mayor podía dejar fuera la tarea con la rama, los commits y el subagente, y obligaba a mover el trabajo. Juntar dos con trabajo mezclaría ramas y subagentes, así que se niega. Sin retitular, la resultante conserva títulos y pasos que ya no dicen lo que es.
- **Separar** («/split separa pasos en una tarea nueva», 097; 098; 100): una tarea que junta partes separables se parte sin Claude, también a mitad de turno. La 097 está sustituida en parte por la 098: la nueva ya no lleva «Separada de la 89».
- **Deshacer una fusión o una eliminación** (115, punto 8; 134).

### Fuera de una tarea

- **Publicar** (082; «La versión forma parte del manejo del repositorio», 226): la versión la lleva la SF al publicar, como el resto del manejo del repositorio, que no se negocia: siempre `develop` a la rama principal, con su tag.
- **Recuperar una copia** (113; 115, punto 12): una escritura puede romper la cola; las últimas 50 copias permiten volver atrás.

## 3. Formato de `.sf/peticiones.json`

- **Nombres compactos** («Textos compactos: nada que no aporte», 040): el panel recorta cada línea al ancho; los prefijos repetidos se comen el espacio y lo importante se pierde.
- **Descripción sin origen** (063, 098): arriba.
- **`quien` y `via`** (115, punto 10): distinguen el Cerrar del propietario en el panel de un cierre del principal.
- **El subagente no escribe, aunque el CLI no lo compruebe** (110; 115, punto 14).

## 4. Copias rotativas

- **Copias, bloqueo y recuperación** (113; 115, puntos 12 y 13): cada escritura guarda antes una copia, y un archivo de bloqueo evita que dos escrituras a la vez rompan la cola. La tarea 145 pasó el panel a escribir con el CLI.
