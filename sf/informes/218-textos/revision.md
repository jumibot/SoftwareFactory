---
antetitulo: SoftwareFactory · Tarea 218 · Noviembre 2026
lema: Cada regla de la orquestación, // con su decisión al día.
subtitulo: Los textos de las decisiones nuevas, las vigentes que recogen lo que sigue valiendo y las deprecadas, para revisarlos antes de registrarlos.
version: Versión 1.0 · 25/11/2026
estado: Para revisar · Tarea 218
destino: proyecto
herramientas: buscador lectura cabecera
menu: secciones
tipo: Revisión de decisiones
pie: Textos de la tarea «Registrar las decisiones de orquestación sin archivo» (218), según «Las decisiones superadas se deprecan enteras y lo vigente va a una decisión nueva» (360). Los archivos están en sf/informes/218-textos/; los registra el orquestador con cola.py decision tras el OK del propietario de la Software Factory.
---
# Decisiones de orquestación

## Resumen | Qué hay que revisar | Resumen {#resumen}

Salen 21 decisiones nuevas: las diez órdenes que no tenían archivo y once vigentes, cada una con lo que sigue valiendo de las que se deprecan. Se deprecan 24 decisiones, enteras, con su línea de estado y su «Aplicada en» al día; otras 6, que siguen vigentes, solo ponen al día su «Aplicada en». Nada está registrado todavía.

::: columnas
**21** decisiones nuevas
{: .metrica}
|||
**24** deprecadas
{: .metrica}
|||
**6** «Aplicada en» al día
{: .metrica}
:::

Donde un texto cita una decisión que aún no tiene número, lleva un marcador, como `{N6}` o `{V-083}`: al registrar cada una, se cambia por el número que le dé `cola.py decision`. Quedan tres dudas para el propietario, al final, con su recomendación.

> **Comprobado en el panel y el mod**
> La V-066 que se entregó decía «74C», pero el panel ya no escribe la letra tras el número: solo da su color. Está corregida aquí. La V-070 coincide con el código. El mod no trae la cola entera con cada mensaje, solo los cambios hechos desde el panel; la V-149 lo dice así.

## Las diez nuevas | Órdenes sin decisión | Nuevas {#nuevas}

Son órdenes del propietario que la skill de orquestación ya aplica y que su porqué citaba solo con una fecha o una tarea. Ninguna sustituye a otra: las que tocan una decisión vigente dicen que la amplían o la completan.

::: tarjetas 2 plegables

### N1 · Un cambio pequeño es un paso, y las tareas afines se fusionan {color=turquesa icono=documento}

Un cambio pequeño es un paso de la tarea en la que encaja, no una tarea nueva. Al anotar una petición, si hay una tarea en curso afín, se recomienda fusionarla con ella; y el principal sugiere las fusiones sin esperar a que se acumulen.

Una tarea con muchos pasos sigue siendo una mientras trate una sola cosa. Si su título queda desfasado, se renombra y se redescribe; si pierde el foco, se propone separarla.

Amplía «El orquestador sugiere fusiones y splits» (100).

Porqué: los cambios pequeños anotados como tareas sueltas llenaban la cola. Orden del propietario de la Software Factory del 2026-10-31, en «Skill de orquestación» (205).

Aplicada en: `sf:orquestacion` («Menú al anotar» y «Fusionar, separar y redescribir») y `references/porque.md`.

### N2 · Lo que permite probar una tarea va en la misma tarea {color=turquesa icono=documento}

Lo que hace falta para probar lo que hace una tarea (un botón, una orden, un dato de prueba) es parte de ella, no de otra tarea.

Porqué: la tarea de descartar y revertir se cerró sin su botón y no se pudo probar. Orden del propietario de la Software Factory del 2026-10-29.

Aplicada en: `sf:orquestacion` («Menú al anotar») y `references/porque.md`.

### N3 · Las tareas de definición proponen con pros y contras y dejan madurar la decisión {color=turquesa icono=documento}

En una tarea de definición, su subagente analiza y propone opciones con sus pros y contras. El principal las lleva al propietario, deja madurar la decisión sin correr a implementarla y registra cada decisión en cuanto se toma.

Porqué: una tarea de definición no ejecuta una idea, la define; correr a implementar se salta el diálogo con el propietario. Orden del propietario de la Software Factory del 2026-10-30, en «Diseñar la configuración inicial» (190).

Aplicada en: `sf:orquestacion` («Pasos») y `references/porque.md`.

### N4 · Un fallo propio de Claude es un bug y va a la cola {color=turquesa icono=documento}

Si el propietario no puede hacer algo por un olvido de Claude (un paso sin anotar, una orden que falta), es un bug: va a la cola en cuanto se detecta, como cualquier otro. No basta con arreglarlo y explicarlo.

Amplía «Los bugs son tareas nuevas» (096).

Porqué: en «Auditar que la skill de orquestación recoge todo lo ordenado» (216), el propietario no pudo cerrar desde el panel porque faltaba `cola.py listo`; se explicó el olvido y se cerró a mano sin anotar nada. «¿No consideras un bug lo que ha pasado?» (propietario de la Software Factory, 2026-11-01). Un olvido que se repite pide una regla o código.

Aplicada en: `sf:orquestacion` («Con cada mensaje», punto 2) y `references/porque.md`.

### N5 · Al proponer descartar una tarea, decir qué pedía, dónde quedó hecha y qué supone {color=turquesa icono=documento}

Al proponer descartar o eliminar una tarea, Claude dice qué pedía, dónde quedó hecha (tarea y versión) y qué supone descartarla.

Porqué: se proponía descartar una tarea duplicada citándola solo por su número, y el propietario no recuerda cada tarea por su número; así decide sin buscarla. Propietario de la Software Factory, 2026-11-03, tarea 324.

Aplicada en: `sf:orquestacion` («Probar y cerrar») y `references/porque.md`.

### N6 · Los commits de trabajo en la rama de la tarea no esperan el OK {color=turquesa icono=documento}

Claude hace los commits de trabajo en la rama de la tarea sin preguntar. Esperan el OK del propietario el cierre, el paso a observación, el descarte y la publicación.

Porqué: con una rama por tarea («Una rama de feature por tarea», 082), lo hecho en ella no toca `develop` y se descarta con la rama; lo que entra en `develop` o se publica es lo que espera su OK. Orden del propietario de la Software Factory del 2026-10-29.

Aplicada en: `sf:orquestacion` («Probar y cerrar») y `references/porque.md`; metodología, «Tareas y cola» («El OK»).

### N7 · Sin menú para lo que el propietario ya tiene en el panel {color=turquesa icono=documento}

Para probar, cerrar, pasar a observación, descartar, separar pasos o publicar, el principal no abre un menú: dice en una línea qué botón del panel usar. La excepción es «¿Cómo va la N?» de las tareas en observación, que sigue siendo un menú («¿Cómo va la N?» de las tareas en observación sigue siendo un menú», 327).

Porqué: el menú en la línea del prompt corta lo que el propietario escribe, y el panel ya tiene el botón. Tarea «Que Claude siga el foco del propietario y no le interrumpa» (372).

Aplicada en: `sf:orquestacion` («Preguntar») y `references/porque.md`; la excepción, pendiente en la skill.

### N8 · Una tarea que espera al propietario lleva el paso «Esperar al propietario: …» {color=turquesa icono=documento}

Si una tarea en curso espera al propietario (una respuesta, una decisión, una prueba), el principal le añade el paso «Esperar al propietario: …» y lo marca hecho al recibir la respuesta. Mientras está pendiente, el panel pinta la tarea en rojo en la lista y, si además está lista para probar, en verde.

Completa «Una tarea que espera y no puede volver a la cola lleva un paso «Esperar a …»» (178).

Porqué: el propietario ve de un vistazo qué le toca. Tareas «Que las tareas listas para probar salgan en verde en la lista del panel» (383) y «Afinar las reglas del foco con el uso» (417).

Aplicada en: `sf:orquestacion` («Pasos») y `references/porque.md`; el panel.

### N9 · Una tarea de código tampoco crea documentos {color=turquesa icono=documento}

Un documento nuevo que salga de una tarea de código (un catálogo, un informe generado) va a una tarea documental, igual que cambiar uno que ya existe.

Amplía «Las tareas de código no llevan pasos de documentación» (240).

Porqué: una documental solo toca su documento, y una de código solo el código y lo que va con él; crear un documento cuenta igual que cambiarlo. Tarea «Afinar las reglas del foco con el uso» (417).

Aplicada en: `sf:orquestacion` («Pasos» y «Documentos compartidos») y `references/porque.md`; `sf:flujo_tareas` («Pasos según el tipo»); metodología, «Documentos compartidos».

### N10 · Las respuestas del principal, legibles en el terminal {color=turquesa icono=documento}

En el chat:

- Los números de tarea van con dígitos en círculo negro (❶ … ❾, el cero ⓿), pegados a la T y con un espacio detrás de cada uno: «T❸ ❾ ❷ ». Solo en el chat: no en commits, en la cola ni en los documentos.
- La descripción de la línea del foco va como código en línea, para que salga en color. La etiqueta del off-topic, «ᴏꜰꜰ-ᴛᴏᴘɪᴄ», va en versalitas, para que pese menos que el foco, y también como código en línea.
- Las preguntas al propietario van en verde, en un bloque `diff` de una línea «+ ¿…?», con ❓ al final si esperan su decisión sobre una tarea. La de un off-topic, no: va en su paréntesis.
- Ninguna línea ni viñeta empieza con un emoji, y nunca van dos seguidos. ✅ va detrás de la palabra que dice el estado.

Porqué: el terminal pinta más anchos los dígitos en círculo y, sin espacio, se montan; el código en línea y el verde del bloque `diff` dan color donde no lo hay; un emoji al principio queda pegado a la viñeta. Tareas «Construir la skill que fija los parámetros del estilo con muestras y afinado» (392) y «Afinar las reglas del foco con el uso» (417).

Aplicada en: `sf:orquestacion` («Con cada mensaje» y «Cómo escribir») y `references/porque.md`; el mod, en la sugerencia de la caja del prompt.

:::

## Las once vigentes | Lo que sigue valiendo | Vigentes {#vigentes}

Cada una reúne lo que sigue valiendo de una o varias decisiones que se deprecan, sin repetir lo que ya dice otra vigente: para eso, la cita. Debajo de cada texto, lo que se ha dejado fuera de las antiguas y por qué.

::: tarjetas 2 plegables

### V-048 · Al terminar una tarea, Claude propone probarla o cerrarla, y cerrar espera el OK del propietario {color=verde icono=check}

Recoge
:   «Preguntar antes de cerrar una petición; lo nuevo, a la cola» (048), «Probar antes de cerrar» (074), «Pasos de cierre: probar y cerrar la tarea» (090), «La tarea que se prueba es la de la rama activa» (095) y «Cerrar directamente lo que no tiene prueba» (154)

Al terminar una tarea, Claude enseña lo hecho y propone probarla, con cómo. Si no tiene nada que probar (deliberar, investigar, documentar, especificar…), propone cerrarla directamente, enseñando el resultado: el OK del propietario es la aprobación.

El cierre, el paso a observación y la publicación esperan el OK del propietario. Los commits de trabajo en la rama, no («Los commits de trabajo en la rama de la tarea no esperan el OK», `{N6}`).

Toda tarea lleva dos pasos de cierre: «Activar rama para poder probar» y «Cerrar la tarea». Van separados porque la prueba depende del propietario, y el cierre, de su OK. Un cambio pedido al probar es un paso nuevo antes de ellos. Cómo se llaman y cuándo se ponen, en «El paso de prueba es «Activar rama para poder probar»» (172) y «Los pasos de cierre, desde que la tarea entra en curso» (174).

Un OK sin número («ciérrala», «ok») es para la tarea de la rama activa. Si hay duda (la rama activa no es de ninguna tarea, o el contexto apunta a otra), Claude pregunta antes de cerrar.

Recoge lo que sigue valiendo de «Preguntar antes de cerrar una petición; lo nuevo, a la cola» (048), «Probar antes de cerrar» (074), «Pasos de cierre: probar y cerrar la tarea» (090), «La tarea que se prueba es la de la rama activa» (095) y «Cerrar directamente lo que no tiene prueba» (154), que quedan deprecadas.

Porqué: Claude cerró y publicó una skill sin permiso (048). Proponía cerrar tareas sin probarlas y la observación se llenaba (074). Deliberar, investigar, documentar o especificar no se prueban como el código (154). Con dos pasos, el panel muestra que a una tarea solo le falta cerrarse (090). Un «probada» sin número se aplicó a otra tarea tras un cambio de rama (095).

Aplicada en: `sf:orquestacion` («Probar y cerrar») y `references/porque.md`; `sf:flujo_tareas` y `cola.py` (pasos de cierre); metodología, «Tareas y cola» («Probar y cerrar» y «El OK»).

Dejado fuera
:   De la 048, que una pendiente pasa a en curso al preguntar por ella y que lo nuevo entra en cola salvo el primer paso (los sustituyen el menú al anotar y que solo el propietario pone en curso), y que el commit espere el OK (N6). De la 074, cerrar sin probar solo si hace falta para probar (lo sustituye cerrar directamente). De la 090, el nombre «Probar la tarea» y que los pasos se añadieran al acabar (172 y 174), y qué hace Cerrar, que es mecánica de `sf:flujo_tareas`. De la 095, la palabra «probada» (204). De la 154, que quitar el paso de prueba es cerrar sin probar (174: los pasos de cierre ya no se quitan).

### V-050 · Una tarea en observación sale solo con el OK del propietario, que se pide tarea a tarea {color=verde icono=check}

Recoge
:   «Sin probar hasta el OK del propietario; preguntar antes de cambiar de tarea» (050) y «La pregunta de «¿está probada?»: una por petición, con tres respuestas» (051)

Una tarea en observación sigue ahí hasta que el propietario la cierra o la revierte. Lo que solo ha comprobado Claude no la saca.

Antes de pasar a otra tarea, el principal pregunta por las que están en observación. Es una pregunta por tarea, cuatro como mucho, con su número, su título y qué mirar, y las respuestas Cerrar, Sigue en observación, La miro ahora y Revertir, sin descripción («¿Cómo va la N?» de las tareas en observación sigue siendo un menú», 327).

Con La miro ahora, Claude dice qué mirar y espera el resultado, sin abrir otra tarea ni preguntar por la siguiente.

Recoge lo que sigue valiendo de «Sin probar hasta el OK del propietario; preguntar antes de cambiar de tarea» (050) y «La pregunta de «¿está probada?»: una por petición, con tres respuestas» (051), que quedan deprecadas.

Porqué: Claude sacaba de la cola lo que él mismo comprobaba, sin que el propietario viera ni aprobara su funcionamiento; muchas tareas pequeñas las prueba en el momento del cierre (050). El menú anterior mezclaba tareas y daba números sin decir qué era cada una. «Si te digo a una probar ahora, no me intentes abrir otra tarea» (051).

Aplicada en: `sf:orquestacion` («Probar y cerrar») y `references/porque.md`; metodología, «Tareas y cola» («En observación»).

Dejado fuera
:   El estado «sin probar» y el campo `comprobado` con su marca verde (212 y 288); las respuestas Probada, Pendiente y Probar ahora (204 y 327).

### V-066 · El número de una tarea lleva el color de su estado, y una reabierta cuenta como H {color=verde icono=check}

Recoge
:   «Código de tarea más ligero: 74C» (066) y «Una tarea reabierta lleva H» (069)

En el panel, el número de una tarea va sin letra detrás: la letra de su estado (A, H, O, C o D) solo le da el color. El número va subrayado cuando la tarea se despliega.

Una tarea reabierta no es nueva: cuenta como H, aunque haya entrado en la sesión.

El ancho de los números y el rojo de las reabiertas, en «Números de tarea en tres columnas, apartados con 0 y rojo solo para las reabiertas» (159).

Recoge lo que sigue valiendo de «Código de tarea más ligero: 74C» (066) y «Una tarea reabierta lleva H» (069), que quedan deprecadas.

Porqué: los códigos de tarea pesaban a la vista; primero se quitó el guion y después la letra, que quedó solo como color (propietario de la Software Factory, 2026-10-28 y 2026-10-31). Una reabierta volvía con A, como si fuera nueva (069).

Aplicada en: el panel (`plugins/sf/hooks/panel.tsx`) y sus pruebas.

Dejado fuera
:   La letra pegada al número («74C»), en mayúscula y más apagada, los colores por letra y el reparto «3 (1A + 2H)» de las cabeceras: el panel ya no escribe la letra (orden del propietario del 2026-10-31, sin decisión propia) y los colores los cambiaron la 159, la 334 y la 355. «Los textos de las tareas, sin negrita», no comprobado. De la 069, la H en rojo (159).

### V-070 · El panel avisa cuando el proyecto va por detrás de la SF {color=verde icono=check}

Recoge
:   «El panel avisa si el proyecto va por detrás de la SF» (070)

Si la versión de `.sf/proyecto.json` es anterior (mayor.menor) a la del plugin, el panel avisa de que el proyecto va por detrás y dice cómo ponerlo al día: pedir a Claude «pon el proyecto al día con la SF» (skill `sf:incorporar_proyecto_a_sf`). Los arreglos (tercer número) no avisan.

Dónde se ve el aviso y la versión, en «Un solo aviso de proyecto atrasado en el panel» (161) y «La línea gris del proyecto sale del panel» (166).

Recoge lo que sigue valiendo de «El panel avisa si el proyecto va por detrás de la SF» (070), que queda deprecada.

Porqué: en SmartColdBox, el panel parecía antiguo: el plugin era el 0.32.1, pero el proyecto se había incorporado con la SF 0.13 y su `.sf/` era de entonces.

Aplicada en: `plugins/sf/hooks/lectura.ts` y `panel.tsx`.

Dejado fuera
:   La versión «SF 0.13 → 0.32.3» en el panel lateral: con la 161 y la 166, solo sale en la línea de la caja sobre el prompt.

### V-083 · El principal orquesta y lanza cada subagente sin preguntar {color=verde icono=check}

Recoge
:   «El principal orquesta; los subagentes ejecutan» (083), «El subagente se lanza sin preguntar» (086) y «Lanzar sin esperar lo que no necesita al propietario» (105)

El agente principal es el orquestador del desarrollo: habla con el propietario, define y decide con él, lleva la cola y lanza y sigue los subagentes. Qué trabajo hace cada subagente, en «Un subagente vivo por tarea en curso, en su rama auxiliar» (`{V-149}`) y «Todo el trabajo de la tarea, a su subagente» (151).

Solo el principal escribe la cola. Antes de anotar lo que trae un subagente, revisa sus cambios en la rama (el diff y, si se puede, la comprobación). El encargo prohíbe al subagente escribir la cola.

El subagente informa con un formato fijo, que da su encargo: si ha terminado o se ha interrumpido y qué necesita, lo hecho, lo comprobado y lo pendiente. Antes de parar, hace commit de lo hecho en su rama. Una tarea interrumpida se retoma con el mismo subagente, que conserva su contexto; si no se puede, con uno nuevo en la misma rama, a partir del informe.

El subagente se lanza sin pedir permiso, avisando en una línea. Compartir archivos con otra tarea no es motivo para esperar, salvo alto riesgo de pérdidas: el solape se resuelve al juntar. Sí lo es necesitar el resultado de otra. Al final de cada turno, el principal lanza el de las tareas en curso que aún no lo tienen. Las de la cola, solo cuando se ponen en curso; quién las pone, en «TURBO pone en curso las tareas que no necesitan al propietario» (160).

Recoge lo que sigue valiendo de «El principal orquesta; los subagentes ejecutan» (083), «El subagente se lanza sin preguntar» (086) y «Lanzar sin esperar lo que no necesita al propietario» (105), que quedan deprecadas.

Porqué: «el principal, que pasa a orquestador del desarrollo, que lo gestione» (083). «Que el orquestador no pregunte siempre si lanzar el subagente» (086). «No entiendo por qué has esperado tanto a lanzar los subagentes si las tareas estaban en curso y no dependían de mí»; «compartir archivos no es motivo para esperar, a no ser que haya alto riesgo de pérdidas por la colisión» (105).

Aplicada en: `sf:orquestacion` («Subagentes») y `references/porque.md`; metodología, «Orquestación con subagentes»; el mod, `control.ts` («El mod impide que un subagente escriba la cola», 110).

Dejado fuera
:   Las tareas triviales y los cambios durante la prueba en el principal (149 y 151); el subagente que pasaba las decisiones a `docs/decisiones.md` (155); la tarea del principal en la carpeta principal (la rama auxiliar, 149); los pendientes de entonces, ya hechos. De la 105, «solo las en curso», que con TURBO cambió la 160.

### V-112 · Cada documento compartido se actualiza en su propia tarea, «Actualizar &lt;documento&gt;» {color=verde icono=check}

Recoge
:   «Los documentos compartidos se actualizan en una tarea aparte» (112) y «Una tarea por documento que actualizar» (142)

Son documentos compartidos los «Cómo funciona…», la metodología, la plantilla `claude-sf.md` y el `CLAUDE.md` de la SF. Una tarea que necesita cambiar uno no lo cambia: su cambio va a la tarea de ese documento. Cómo se anota, en «El paso de documentar es crear la tarea de documentos» (116) y «Documentación, una vez por tarea» (147). La decisión de la tarea y sus pruebas siguen dentro de ella.

Cada documento tiene una sola tarea, «Actualizar &lt;documento&gt;». Un cambio nuevo en un documento con su tarea abierta se añade a ella. Si aun así hay dos tareas del mismo documento, el principal las fusiona directamente, sin pedírselo al propietario. La metodología, la plantilla y el `CLAUDE.md` de la SF comparten una («Las reglas del método se actualizan en una sola tarea», 148). Quién las hace, en «Documentos compartidos, también por subagente» (152).

Un documento compartido queda desfasado hasta que se hace su tarea.

Recoge lo que sigue valiendo de «Los documentos compartidos se actualizan en una tarea aparte» (112) y «Una tarea por documento que actualizar» (142), que quedan deprecadas.

Porqué: cada tarea cambiaba en su rama los documentos que todas tocan, y al cerrarlas con squash chocaban en ellos y en sus HTML (112). Cada cambio abría su propia tarea de documentación y había que fusionarlas a mano (142).

Aplicada en: `sf:orquestacion` («Documentos compartidos») y `references/porque.md`; `sf:flujo_tareas` («Fusionar y separar» y `references/estados.md`); metodología, «Documentos compartidos»; `CLAUDE.md` de la SF.

Dejado fuera
:   El paso «Documentar: tarea NN» (116), «de una en una, en el principal» (152), sugerir `/fusionar` (142: se fusionan directamente) y, de la 142, un paso por cambio (147).

### V-139 · Al anotar sin foco, un menú breve: paso de una tarea, en curso o en cola {color=verde icono=check}

Recoge
:   «Menú al anotar: paso, en curso o en cola» (139)

Sin foco, al anotar una petición, Claude abre un menú. Si, a su juicio, encaja como paso de una tarea, de cualquier estado, pregunta primero si se añade a ella. Si no encaja, o el propietario lo descarta, pregunta si va en curso o se queda en cola. Con «En curso», sigue lo de poner una tarea en curso: los choques, su rama y su subagente.

El menú es breve y no pregunta lo que el propietario ya ha dicho: «tarea» salta la pregunta del paso; «paso de la NN», «en curso» o «en cola», el menú entero.

Con foco, se anota sin menú («El principal no abre menús con texto a medio escribir ni fuera del foco», 333; «Reglas del foco y del off-topic: las once recomendaciones del informe de la 431», 357).

Recoge lo que sigue valiendo de «Menú al anotar: paso, en curso o en cola» (139), que queda deprecada.

Porqué: el propietario quiere elegir en el momento si empieza una tarea o la deja pendiente: «al añadir una tarea, abrir un menú para saber si en curso o en la cola de pendientes».

Aplicada en: `sf:orquestacion` («Menú al anotar») y `references/porque.md`; `sf:flujo_tareas` (`references/estados.md`); metodología, «Tareas y cola».

Dejado fuera
:   La «→» del panel que creaba en cola sin menú: el panel ya no la tiene («¿A Pendientes?»). Con foco, el menú (333 y 357).

### V-149 · Un subagente vivo por tarea en curso, en su rama auxiliar {color=verde icono=check}

Recoge
:   «Orquestación con un subagente vivo por tarea» (149)

Cada tarea en curso tiene un subagente vivo, al que se le pasa cada encargo del propietario sobre ella, también durante la prueba. Todo cambio de la tarea lo hace él («Todo el trabajo de la tarea, a su subagente», 151).

El subagente trabaja siempre en su rama auxiliar, `sub-NN`. La rama de la tarea queda libre, y Activar rama y Cerrar funcionan sin quitar su worktree. Al cerrar, Claude detiene el subagente; su worktree y su rama auxiliar los recoge `cola.py` («cola.py recoge el subagente al dejar la tarea sin él», 169).

Para que el panel refleje el trabajo:

- Antes de informar o actuar sobre una tarea, el principal mira la cola al día: el propietario la cambia desde el panel, y el mod le trae esos cambios con cada mensaje.
- Recoge el trabajo del subagente y marca sus pasos en cuanto vuelve.
- Con el último paso hecho, `listo --prueba`, sin esperar.
- Al poner una tarea en curso, planifica sus pasos en la cola; lo que falte por concretar va como pasos («Lo que falta por concretar va como pasos de la tarea», 211).
- Sin tarea en curso no se trabaja, salvo para reorganizar la cola (fusionar, separar, redescribir, añadir pasos, cambiar tipos).

Recoge lo que sigue valiendo de «Orquestación con un subagente vivo por tarea» (149), que queda deprecada.

Porqué: los ajustes que pedía el propietario durante la prueba ocupaban al principal: la 196 llevó 12 ajustes en unas 2,5 horas y unos 360.000 tokens. El panel no reflejaba el trabajo: tareas sin pasos, informes sin recoger y la cola desfasada. «Tener subagentes esperando instrucciones y dejando libre el agente principal lo veo una gran ventaja». La C falló en la 194 porque su worktree tenía activa la rama de la tarea.

Aplicada en: `sf:orquestacion` («Con cada mensaje», «Poner en curso», «Subagentes» y «Probar y cerrar») y `references/porque.md`; `sf:flujo_tareas`.

Dejado fuera
:   «Si su enunciado no basta, preguntar» (211: lo que falta va como pasos) y «al cerrar, parar el subagente y quitar su worktree» (169: lo recoge `cola.py`).

### V-187 · El mod entrega las reglas y sf:orquestacion al empezar la sesión, tras /clear y tras compactar {color=verde icono=check}

Recoge
:   «El panel entrega las reglas y la orquestación en los proyectos» (187)

En los proyectos con `.sf/proyecto.json`, también en la propia SF («En la SF, las reglas y sf:orquestacion las entrega el mod, como en los demás proyectos», 298), el mod entrega como contexto, al empezar la sesión, tras `/clear` y tras compactar, las reglas de la plantilla y el texto entero de `sf:orquestacion`, leídos del plugin instalado. Nunca a un subagente. En cada mensaje se aplican sin volver a cargarlas.

La orquestación tiene su interruptor, `orquestacion` en `.sf/proyecto.json`, encendido por defecto («Las automatizaciones del plugin, configurables y avisando antes que bloquear», 171). Apagado, la carga el principal en esos mismos momentos.

El `CLAUDE.md` de un proyecto no lleva ninguna línea de la SF. Un proyecto que aún importa `@.sf/claude-sf.md` va atrasado: el mod no le entrega las reglas, pero sí la orquestación, y el panel avisa. Ponerlo al día quita la línea y la copia. La regla de «Lo que pinta la SF y lo global no son del proyecto» (167) sigue en el prompt de sistema, por corta.

Recoge lo que sigue valiendo de «El panel entrega las reglas y la orquestación en los proyectos» (187), que queda deprecada.

Porqué: la copia `.sf/claude-sf.md` de cada proyecto se quedaba atrás con cada versión, y cargar `sf:orquestacion` dependía de que Claude se acordara. Al empezar y tras compactar, no en cada mensaje: cada entrega añade unos 3.000 o 4.000 tokens.

Aplicada en: el mod (`hooks/contexto.ts`, `register.tsx`; el aviso de proyecto atrasado en `panel.tsx` y `lectura.ts`); `sf:incorporar_proyecto_a_sf`; `sf:orquestacion`; metodología, «Las reglas las entrega el mod».

Dejado fuera
:   «La propia SF no recibe la inyección» (298).

### V-287 · La línea del foco abre cada respuesta y lo de otras tareas va al final {color=verde icono=check}

Recoge
:   «No interrumpir mientras se prueba o se está en otra tarea» (250) y «El principal dice en qué tarea está concentrado el propietario, con «FOCUS: &lt;título corto&gt; (T NN)»» (287)

El principal le dice al propietario en qué tarea está concentrado con una línea al principio de su respuesta: la etiqueta «🅵🅾🅲🆄🆂», en letras de fondo negro y sin dos puntos, y el título corto de la tarea con su número. Su forma, en «Las respuestas del principal, legibles en el terminal» (`{N10}`). Sin foco, la línea no va.

El foco es una sola tarea. Termina al cerrarse la tarea o cuando el propietario la deja. Qué lo fija y qué lo mueve, en «Con un foco fijado y sin resolver no se cambia de tarea sin instrucción expresa del propietario» (337) y «Reglas del foco y del off-topic: las once recomendaciones del informe de la 431» (357).

Con foco, el principal no interrumpe al propietario con lo de otras tareas: ni actualizaciones, ni preguntas, ni menús. Va al final de la respuesta, como off-topic, uno por tarea y lo más breve posible: lo hecho, y el detalle solo si él lo pide.

Si la tarea del foco espera (a un subagente, a otra cosa) y al propietario no le toca nada en ella, el principal le propone una sola cosa entre las tareas en curso, la mejor de lo que le espera para probar, decidir o contestar; no una lista.

Es la primera regla de la SF que propuso Claude por iniciativa propia y que el propietario hizo suya.

Recoge lo que sigue valiendo de «No interrumpir mientras se prueba o se está en otra tarea» (250) y «El principal dice en qué tarea está concentrado el propietario, con «FOCUS: &lt;título corto&gt; (T NN)»» (287), que quedan deprecadas.

Porqué: mientras el propietario probaba una tarea, Claude le abrió un menú de otra: «Cuando estamos probando o centrados en otra tarea no me interrumpas» (250). Estuvo escribiendo en la vista de un subagente sin darse cuenta; que el principal le dijera en qué tarea estaba le devolvió el foco. Le llegaban actualizaciones de otras tareas incluso mientras escribía, y eligió que fueran al final, breves (287).

Aplicada en: `sf:orquestacion` («Con cada mensaje» y «Cómo escribir») y `references/porque.md`; el mod, `hooks/foco.ts` (la sugerencia tras un rato sin escribir, 332, y el freno a los menús, 333).

Dejado fuera
:   El formato «FOCUS: …» y «(off-topic T NN: …)» (N10); «el foco es la tarea sobre la que más escribe» y «el foco pasa a la propuesta» (337 y 357); el off-topic suelto solo con el foco terminado (357). De la 250, la llamada a la acción tras un rato sin actividad (332: el mod deja una sugerencia en la caja del prompt).

### V-289 · Un juego fijo de emojis de estado en las respuestas del principal, coherente con el panel {color=verde icono=check}

Recoge
:   «Emojis de estado fijos en las respuestas del principal, coherentes con el panel» (289)

El principal marca los estados con este juego fijo de emojis, el mismo en todos los proyectos y sin añadir otros:

🟡 tarea puesta en curso · 🟢 subagente trabajando · 🔴 subagente terminado · ⚪ en cola · ▶️ lista para probar (te toca ponerla en marcha) · 👀 en observación · 🔒 cerrada · ✅ comprobado · ❔ no comprobado · ❓ decisión del propietario sobre una tarea · ⭐ la opción recomendada · ⚠️ aviso o riesgo · ❌ algo falla

🟡 solo al poner una tarea en curso, no al mencionar una que ya lo está. ❓ solo en la pregunta que espera una decisión del propietario sobre una tarea, al final y en lugar del signo de cierre. El rojo es «terminado», como el punto de los subagentes en el panel; por eso un fallo va con ❌. ✅ solo marca lo comprobado; lo hecho no lleva emoji.

Para el antes y el después de un texto, y para los pasos y tareas que se añaden o se quitan, un bloque `diff`: las líneas con «+» salen en verde y las de «-» en rojo. Sus líneas, sin emojis: el color ya marca el estado.

Dónde va cada emoji en la línea y sus excepciones, en «La línea del foco es una excepción al juego fijo de emojis» (336), «Reglas del foco y del off-topic: las once recomendaciones del informe de la 431» (357) y «Las respuestas del principal, legibles en el terminal» (`{N10}`).

Recoge lo que sigue valiendo de «Emojis de estado fijos en las respuestas del principal, coherentes con el panel» (289), que queda deprecada.

Porqué: en el chat no hay colores, y el propietario quiere ver de un vistazo el estado de lo que se le cuenta, con los mismos significados que el panel. Juego corto: muchos emojis restan.

Aplicada en: `sf:orquestacion` («Cómo escribir») y `references/porque.md`.

Dejado fuera
:   «✅ y ⭐ van al final de su línea» (N10 y 357).

:::

## Dudas | Lo que decide el propietario | Dudas {#dudas}

Tres puntos que no cambian ningún texto si se acepta la recomendación. Las dos últimas se han contrastado con el código de `plugins/sf/hooks/`.

::: preguntas 1 plegables

### 1 · Fecha de la deprecación {recomendada=A} {: #p1}

La línea de estado lleva una fecha. Tres decisiones (la 135, la 153 y la 180) quedaron sustituidas del todo mucho antes, por otra que ya existía; las demás se deprecan hoy, al registrar su vigente.

Opción A
:   La fecha de hoy, 2026-11-25, salvo las tres sustituidas del todo antes, que llevan la fecha de la decisión que las sustituyó (2026-11-01, 2026-10-31 y 2026-11-01). Es como están los textos.

Opción B
:   La fecha de hoy en todas.

Opción C
:   En todas, la fecha de la última decisión que cambió algo de ella, aunque la vigente se registre hoy.

Recomendación
:   **A.** La fecha dice cuándo dejó de valer: las tres antiguas dejaron de valer entonces, y las demás, hoy, cuando lo vigente pasa a una decisión nueva.

### 2 · V-066 y V-070, contrastadas con el panel {recomendada=A} {: #p2}

Comprobado en `panel.tsx` y `lectura.ts`. La V-070 coincide: el aviso compara mayor.menor, los arreglos no avisan, dice «pide a Claude «pon el proyecto al día con la SF»» y la flecha de versiones solo sale en la línea de la caja. La V-066 no coincidía: el panel no escribe la letra tras el número desde el 2026-10-31 («Sin letras tras los números», orden del propietario sin decisión propia); la letra solo da el color, y una reabierta cuenta como H. El texto ya está corregido.

Opción A
:   Registrar la V-066 corregida y la V-070 como están, con la 066, la 069 y la 070 deprecadas.

Opción B
:   Sacar las tres del panel de este lote y llevarlas a una tarea del panel que revise también la 159, la 161 y la 166.

Recomendación
:   **A.** Los textos ya coinciden con el código, y la orden de quitar la letra queda registrada dentro de la V-066.

### 3 · V-149 y la cola en el contexto {recomendada=A} {: #p3}

«Sin subagente de la cola…» (284) dice que el mod pone en cada mensaje las tareas en curso y lo que cambió en la cola. Comprobado en `register.tsx` y `avisos.ts`: con cada mensaje del propietario, el mod añade lo que él cambió desde el panel desde el mensaje anterior, y los avisos de subagentes por lanzar o por recoger; la lista de tareas en curso, no.

Opción A
:   La V-149 dice: mirar la cola al día, porque el propietario la cambia desde el panel y el mod trae esos cambios con cada mensaje. Es como está el texto.

Opción B
:   Decir que el mod trae la cola y quitar la consulta: hoy no es cierto.

Opción C
:   Dejar «consultar la cola con `cola.py lista` antes de informar o actuar», como decía la 149.

Recomendación
:   **A.** Dice lo que pasa hoy sin atarse a cómo; cuando el mod traiga las tareas en curso, sigue valiendo.
:::

## Deprecadas y «Aplicada en» | Lista de las 24 | Deprecadas {#deprecadas}

Cada deprecada se reescribe con `cola.py decision "Título" --numero NNN`: lleva su línea de estado bajo el título y su «Aplicada en» al día, y el resto del texto queda como estaba. Esta es la línea de estado de cada una.


### 048 · Preguntar antes de cerrar una petición; lo nuevo, a la cola

Estado: deprecada el 2026-11-25 por «Al terminar una tarea, Claude propone probarla o cerrarla, y cerrar espera el OK del propietario» (`{V-048}`); lo demás, por «El principal orquesta y lanza cada subagente sin preguntar» (`{V-083}`), «Al anotar sin foco, un menú breve: paso de una tarea, en curso o en cola» (`{V-139}`) y «Los commits de trabajo en la rama de la tarea no esperan el OK» (`{N6}`).
{: .nota}

### 050 · Sin probar hasta el OK del propietario; preguntar antes de cambiar de tarea

Estado: deprecada el 2026-11-25 por «Una tarea en observación sale solo con el OK del propietario, que se pide tarea a tarea» (`{V-050}`); lo demás, por «Testing pasa a llamarse «En observación»» (212) y «Las comprobaciones y pruebas hechas se anotan como pasos de su tarea» (288).
{: .nota}

### 051 · La pregunta de «¿está probada?»: una por petición, con tres respuestas

Estado: deprecada el 2026-11-25 por «Una tarea en observación sale solo con el OK del propietario, que se pide tarea a tarea» (`{V-050}`); lo demás, por «Los estados de las tareas se nombran con el lenguaje de la SF» (204) y «¿Cómo va la N?» de las tareas en observación sigue siendo un menú» (327).
{: .nota}

### 066 · Código de tarea más ligero: 74C

Estado: deprecada el 2026-11-25 por «El número de una tarea lleva el color de su estado, y una reabierta cuenta como H» (`{V-066}`); lo demás, por «Números de tarea en tres columnas, apartados con 0 y rojo solo para las reabiertas» (159).
{: .nota}

### 069 · Una tarea reabierta lleva H

Estado: deprecada el 2026-11-25 por «El número de una tarea lleva el color de su estado, y una reabierta cuenta como H» (`{V-066}`); lo demás, por «Números de tarea en tres columnas, apartados con 0 y rojo solo para las reabiertas» (159).
{: .nota}

### 070 · El panel avisa si el proyecto va por detrás de la SF

Estado: deprecada el 2026-11-25 por «El panel avisa cuando el proyecto va por detrás de la SF» (`{V-070}`); lo demás, por «Un solo aviso de proyecto atrasado en el panel» (161) y «La línea gris del proyecto sale del panel» (166).
{: .nota}

### 074 · Probar antes de cerrar

Estado: deprecada el 2026-11-25 por «Al terminar una tarea, Claude propone probarla o cerrarla, y cerrar espera el OK del propietario» (`{V-048}`).
{: .nota}

### 083 · El principal orquesta; los subagentes ejecutan

Estado: deprecada el 2026-11-25 por «El principal orquesta y lanza cada subagente sin preguntar» (`{V-083}`); lo demás, por «Un subagente vivo por tarea en curso, en su rama auxiliar» (`{V-149}`), «Todo el trabajo de la tarea, a su subagente» (151) y «Las decisiones, a develop en cuanto se toman» (155).
{: .nota}

### 086 · El subagente se lanza sin preguntar

Estado: deprecada el 2026-11-25 por «El principal orquesta y lanza cada subagente sin preguntar» (`{V-083}`); lo demás, por «Todo el trabajo de la tarea, a su subagente» (151).
{: .nota}

### 090 · Pasos de cierre: probar y cerrar la tarea

Estado: deprecada el 2026-11-25 por «Al terminar una tarea, Claude propone probarla o cerrarla, y cerrar espera el OK del propietario» (`{V-048}`); lo demás, por «El paso de prueba es «Activar rama para poder probar»» (172) y «Los pasos de cierre, desde que la tarea entra en curso» (174).
{: .nota}

### 095 · La tarea que se prueba es la de la rama activa

Estado: deprecada el 2026-11-25 por «Al terminar una tarea, Claude propone probarla o cerrarla, y cerrar espera el OK del propietario» (`{V-048}`); lo demás, por «Los estados de las tareas se nombran con el lenguaje de la SF» (204).
{: .nota}

### 105 · Lanzar sin esperar lo que no necesita al propietario

Estado: deprecada el 2026-11-25 por «El principal orquesta y lanza cada subagente sin preguntar» (`{V-083}`); lo demás, por «Todo el trabajo de la tarea, a su subagente» (151) y «TURBO pone en curso las tareas que no necesitan al propietario» (160).
{: .nota}

### 112 · Los documentos compartidos se actualizan en una tarea aparte

Estado: deprecada el 2026-11-25 por «Cada documento compartido se actualiza en su propia tarea, «Actualizar &lt;documento&gt;»» (`{V-112}`); lo demás, por «El paso de documentar es crear la tarea de documentos» (116), «Documentación, una vez por tarea» (147) y «Documentos compartidos, también por subagente» (152).
{: .nota}

### 135 · Borrar las ramas del subagente al volver

Estado: deprecada el 2026-11-01 por «cola.py recoge el subagente al dejar la tarea sin él» (169).
{: .nota}

### 139 · Menú al anotar: paso, en curso o en cola

Estado: deprecada el 2026-11-25 por «Al anotar sin foco, un menú breve: paso de una tarea, en curso o en cola» (`{V-139}`); lo demás, por «El principal no abre menús con texto a medio escribir ni fuera del foco» (333) y «Reglas del foco y del off-topic: las once recomendaciones del informe de la 431» (357).
{: .nota}

### 142 · Una tarea por documento que actualizar

Estado: deprecada el 2026-11-25 por «Cada documento compartido se actualiza en su propia tarea, «Actualizar &lt;documento&gt;»» (`{V-112}`); lo demás, por «Documentación, una vez por tarea» (147) y «Las reglas del método se actualizan en una sola tarea» (148).
{: .nota}

### 149 · Orquestación con un subagente vivo por tarea

Estado: deprecada el 2026-11-25 por «Un subagente vivo por tarea en curso, en su rama auxiliar» (`{V-149}`); lo demás, por «cola.py recoge el subagente al dejar la tarea sin él» (169) y «Lo que falta por concretar va como pasos de la tarea» (211).
{: .nota}

### 153 · TURBO solo lanza las tareas en curso

Estado: deprecada el 2026-10-31 por «TURBO pone en curso las tareas que no necesitan al propietario» (160).
{: .nota}

### 154 · Cerrar directamente lo que no tiene prueba

Estado: deprecada el 2026-11-25 por «Al terminar una tarea, Claude propone probarla o cerrarla, y cerrar espera el OK del propietario» (`{V-048}`); lo demás, por «Los pasos de cierre, desde que la tarea entra en curso» (174).
{: .nota}

### 180 · Los pasos de una tarea se deciden en modo plan

Estado: deprecada el 2026-11-01 por «El principal planifica los pasos sin pedir aprobación» (181).
{: .nota}

### 187 · El panel entrega las reglas y la orquestación en los proyectos

Estado: deprecada el 2026-11-25 por «El mod entrega las reglas y sf:orquestacion al empezar la sesión, tras /clear y tras compactar» (`{V-187}`); lo demás, por «En la SF, las reglas y sf:orquestacion las entrega el mod, como en los demás proyectos» (298).
{: .nota}

### 250 · No interrumpir mientras se prueba o se está en otra tarea

Estado: deprecada el 2026-11-25 por «La línea del foco abre cada respuesta y lo de otras tareas va al final» (`{V-287}`); lo demás, por «Tras un rato sin escribir, la SF deja una sugerencia en la caja del prompt» (332) y «El principal no abre menús con texto a medio escribir ni fuera del foco» (333).
{: .nota}

### 287 · El principal dice en qué tarea está concentrado el propietario, con «FOCUS: &lt;título corto&gt; (T NN)»

Estado: deprecada el 2026-11-25 por «La línea del foco abre cada respuesta y lo de otras tareas va al final» (`{V-287}`); lo demás, por «Con un foco fijado y sin resolver no se cambia de tarea sin instrucción expresa del propietario» (337), «Reglas del foco y del off-topic: las once recomendaciones del informe de la 431» (357) y «Las respuestas del principal, legibles en el terminal» (`{N10}`).
{: .nota}

### 289 · Emojis de estado fijos en las respuestas del principal, coherentes con el panel

Estado: deprecada el 2026-11-25 por «Un juego fijo de emojis de estado en las respuestas del principal, coherente con el panel» (`{V-289}`); lo demás, por «La línea del foco es una excepción al juego fijo de emojis» (336), «Reglas del foco y del off-topic: las once recomendaciones del informe de la 431» (357) y «Las respuestas del principal, legibles en el terminal» (`{N10}`).
{: .nota}


Solo cambian su «Aplicada en», porque siguen vigentes y las citan la skill o las nuevas: «La sección 2 de la metodología resume el flujo de tareas y remite a sf:flujo_tareas» (114), «El paso de documentar es crear la tarea de documentos» (116), «Tras una fusión, redescribir la tarea resultante» (141), «Documentación, una vez por tarea» (147), «Las reglas del método se actualizan en una sola tarea» (148), «En la SF, las reglas y sf:orquestacion las entrega el mod, como en los demás proyectos» (298).
