---
antetitulo: Software Factory · Informe de análisis · Noviembre 2026
lema: Once preguntas; // el resto, en bloque.
subtitulo: Qué decisiones se deprecan, con qué vigente nueva, y las once preguntas que necesitan el criterio del propietario.
version: Versión 2.0 · 27/11/2026
estado: Propuesta · Tarea 439
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de análisis
pie: Informe de la tarea «Poner al día las decisiones: un solo formato y las antiguas, deprecadas» (439). Parte de las decisiones de sf/decisiones/ en develop, de las decisiones 360, 388, 389 y 390, y de cola.py, los hooks del panel y las skills en el worktree de la tarea. Espera la decisión del propietario.
---
# Poner al día las decisiones

## Resumen | Once preguntas y un bloque | Resumen {#resumen}

**11 preguntas** necesitan el criterio del propietario: las tres de la 115 y ocho sueltas.

**26 decisiones** se deprecan en bloque: 20 con 15 vigentes nuevas y 6 sin vigente nueva, porque ya lo dicen otras.

**Cómo contestar:** las preguntas por número («1 A, 2 A…» o «todas A») y OK al bloque.
{: .texto}

[Ver las preguntas](#por-decidir){: .salto}

## Por decidir | Lo que necesita su criterio | Preguntas {#por-decidir}

Once preguntas, una por ficha. La recomendada es siempre la A.

::: preguntas 2

### 1 · La 115: ¿una vigente nueva o dos? {recomendada=A} {: #p1}

Lo que sigue valiendo de la 115 se cita por punto en unos 40 sitios («115 (n)»).

Opción A
:   Una, en lista ([su texto](#t-115)).

Opción B
:   Dos: la cola por dentro, y cerrar, reabrir y subagentes.

Recomendación
:   **A.** Cada cita pasa a un solo número.

### 2 · La 115: ¿qué pasa con deshacer una fusión? {recomendada=A} {: #p2}

Lo dejaba para la tarea 135, que nunca se hizo, y `reabrir` aún la cita.

Opción A
:   Fuera: lo absorbido se saca con `/sf_split`, y `reabrir` deja de citar la 135.

Opción B
:   A una propuesta en `sf/propuestas.md`.

Opción C
:   En la vigente, como pendiente.

Recomendación
:   **A.** `/sf_split` ya cubre el caso.

### 3 · La 115: ¿se quitan los restos de «propuesta que toca un activo»? {recomendada=A} {: #p3}

Las propuestas ya no son tareas, y quedan restos en `sf:flujo_tareas`.

Opción A
:   Sí, en esta tarea.

Opción B
:   No, en otra tarea.

Recomendación
:   **A.** Es una skill del plugin y nada los sostiene.

### 4 · ¿Vale el porqué de la vigente nueva de la 007? {recomendada=A} {: #p4}

La 007 no lo escribió; el propuesto sale de la 004 y la 005: una skill con cosas de un proyecto deja de servir a los demás.

Opción A
:   Vale ([su texto](#t-007)).

Opción B
:   Otro: dilo en el chat.

Recomendación
:   **A.** Es lo que se ve en la 004 y la 005, del mismo día.

### 5 · La 019: ¿vigente nueva o solo deprecarla? {recomendada=A} {: #p5}

Sin vigente nueva, lo que sigue valiendo quedaría en la 032, que también se depreca.

Opción A
:   Vigente nueva ([su texto](#t-019)).

Opción B
:   Solo deprecarla: ya lo dicen la 027, la 037 y la 032.

Recomendación
:   **A.** No se apoya en otra deprecada.

### 6 · La 117: ¿vigente nueva o solo deprecarla? {recomendada=A} {: #p6}

Sin vigente nueva se pierde que un paso solo se quita si sigue en su sitio y sin empezar, que hace el código.

Opción A
:   Vigente nueva ([su texto](#t-117)).

Opción B
:   Solo deprecarla: ya lo dicen la 168 y la 174.

Recomendación
:   **A.** No se pierde lo que hace el código.

### 7 · ¿El fondo negro y el verde de las etiquetas se quedan? {recomendada=A} {: #p7}

Se pidieron «a prueba» el 2026-11-01, sin decisión; la vigente nueva de la 168 los recoge.

Opción A
:   Sí: quedan en la vigente.

Opción B
:   No: se quitan de la vigente y siguen a prueba.

Recomendación
:   **A.** Están en el código desde entonces.

### 8 · La 053 y la 054: ¿dos vigentes nuevas o una? {recomendada=A} {: #p8}

Las dos hablan de la A y la H: una, del bloque de tareas; la otra, de la letra de estado.

Opción A
:   Dos, tal cual.

Opción B
:   Una sola: el bloque y la letra.

Recomendación
:   **A.** Son dos temas, y lo repetido es una línea.

### 9 · La 071: ¿se depreca con vigente nueva? {recomendada=A} {: #p9}

Dice dentro del texto que la 084 la deja sin efecto en parte; lo de las horas no lo dice ninguna otra, y el amarillo cambió con la 355.

Opción A
:   Sí: su vigente, en la próxima vuelta, tras comprobar el dorado de la 355.

Opción B
:   Solo deprecarla: ya lo dicen la 084 y la 355.

Opción C
:   Dejarla como está.

Recomendación
:   **A.** Lo de las horas no está en otra decisión.

### 10 · La 194: ¿se depreca con vigente nueva? {recomendada=A} {: #p10}

Dice dentro del texto que la 210 la corrige en su punto 2; hoy sale como vigente entera.

Opción A
:   Sí: su vigente, en la próxima vuelta de esta tarea.

Opción B
:   Dejarla como está.

Recomendación
:   **A.** El mismo trato que las demás.

### 11 · ¿Se recoge que una tarea en observación ya superada por otra se cierra? {recomendada=A} {: #p11}

Lo decía la 042; no está en el código ni en las skills.

Opción A
:   No: el propietario lo decide con «¿Cómo va la N?».

Opción B
:   Sí, en una vigente nueva.

Recomendación
:   **A.** La 372 ya pide su OK tarea a tarea.

:::

## En bloque | Las que se deprecan sin pregunta | En bloque {#en-bloque}

Una fila por decisión que se depreca. Se aprueban todas con un OK. Las filas de la 019 y la 117 dependen de las preguntas [5](#p5) y [6](#p6).

| Nº | Qué decía | Cómo queda |
| --- | --- | --- |
| 007 | Las skills, con su fuente en la SF; lo propio de cada proyecto, en su `docs/identidad/`. | [Vigente nueva](#t-007): las skills tienen su fuente en el repositorio de la SF y viajan en el plugin; lo de cada proyecto, en su `docs/identidad/`. |
| 019 | El estado, en `docs/sf.json`, y un mod lo enseña en la línea de estado y el panel. | [Vigente nueva](#t-019): un mod dice si el proyecto está bajo la SF y su fase, leyendo `.sf/`, en la caja sobre el prompt. |
| 023 | Propuestas, decisiones, plantillas y ejemplos, cada uno en su sitio. | [Vigente nueva](#t-023): un ejemplo va junto a su regla, una plantilla al plugin y una propuesta a `sf/propuestas.md`. |
| 032 | El mod, centro de control de la SF, con las propuestas de todos los proyectos. | [Vigente nueva](#t-032): el mod lleva el método, la cola, un proyecto por sesión y las propuestas por revisar del proyecto. |
| 053 | Bloque TAREAS, con la A o la H según la sesión. | [Vigente nueva](#t-053): las tareas, en un bloque por el orden de su ciclo; la A o la H da el color del número. |
| 054 | La letra es el estado: A, H, T y C. | [Vigente nueva](#t-054): la letra es el estado, A, H, O, C o D, y solo da el color del número. |
| 091, 103 y 122 | Botón P, luego T, para probar una tarea en su rama, sin recargar el plugin. | [Vigente nueva](#t-091): «Activar rama» la pone en prueba con un clic, sin Claude y sin darla por buena. |
| 097 | `/split` separa pasos de una tarea en una nueva. | [Vigente nueva](#t-097): `/sf_split` y «Separar pasos» lo hacen con `cola.py`, sin Claude y sin los pasos de cierre. |
| 108 | Una decisión por archivo, en `docs/decisiones/`. | [Vigente nueva](#t-108): una por archivo en `sf/decisiones/`, numerada, y el índice lo genera un comando. |
| 117 | Pasos de cierre fijos, y la E con confirmación para quitar pasos. | [Vigente nueva](#t-117): un paso pendiente se quita con dos clics en su «×»; los de cierre, nunca. |
| 138 y 140 | Tareas y repositorio siempre; después, el registro de decisiones, obligatorio. | [Vigente nueva](#t-138-140): lo mínimo son las tareas, el repositorio y el registro de decisiones; la metodología se elige. |
| 161 | Un solo aviso de proyecto atrasado en el panel. | [Vigente nueva](#t-161): el aviso, solo en la cabecera del panel; la caja sobre el prompt da las dos versiones. |
| 168, 173 y 182 | Las órdenes, en un menú de etiquetas; «?» en todas; etiquetas de Testing. | [Vigente nueva](#t-168): las órdenes, como etiquetas en el menú de la tarea desplegada, y la destructiva al final, en rojo. |
| 202 | La SF fija el mecanismo y se adapta al proyecto en lo demás. | [Vigente nueva](#t-202): se adapta solo en el remoto, la rama de publicación, el idioma, los commits y el manifiesto. |
| 203 | Los documentos de la SF, en `sf/`. | [Vigente nueva](#t-203): los documentos de la SF, en `sf/`, y su máquina, en `.sf/`, con rutas fijas. |
| 035 | Marcador del día: terminadas, dejadas y propuestas. | Nada nuevo: ya lo dice la 038 (fuera el marcador). |
| 042 | Lo probado, también lo que comprueba Claude, sale de Sin probar. | Nada nuevo: ya lo dicen la 372 (sale con el OK del propietario) y la 288. |
| 058 | El código de tarea, «57-A». | Nada nuevo: ya lo dicen la 066 y la 373 (el número, sin letra). |
| 121 | Cerrar exige el paso de cerrar; quitar el de probar es cerrar sin probar. | Nada nuevo: ya lo dicen la 172 y la 174. |
| 192 | La mejora desde otro proyecto se escribe con Edit o Write. | Nada nuevo: ya lo dice la 194 (ningún proyecto escribe en la SF). |
| 253 | Botones del panel en la app de escritorio, con contorno de color. | Nada nuevo: ya lo dice la 290 (con el fondo de su color). |

Al aprobar, el principal registra cada vigente nueva con `cola.py decision` y pone a cada antigua su línea de estado, con la fecha del registro (390). La antigua pasa al catálogo de deprecadas (389).
{: .nota}

## Textos | El texto entero de cada vigente nueva | Textos {#textos}

Solo para quien quiera mirarlo: cada vigente nueva, tal como se registraría, con la línea de estado de la antigua debajo. Al final, las líneas de estado de las que se deprecan sin vigente nueva.

::: tarjetas 1 plegables

### 007 · Las skills de la SF tienen su fuente en el repositorio de la SF, y lo propio de cada proyecto va en su docs/identidad/ {: #t-007}

Las skills de la SF, las propias y las externas que adaptamos, tienen su fuente versionada en el repositorio de la SF, en `plugins/sf/skills/`, y viajan en el plugin `sf`. Una skill externa que se usa tal cual no se copia: es una dependencia del plugin, fijada a su commit (175, 176).

Lo propio de cada proyecto (estilo, tema, logo, producto y reglas del dominio) va en su `docs/identidad/`, nunca en la skill.

Recoge lo que sigue valiendo de «Fuente de las skills en la SF y lo propio de cada proyecto en `docs/identidad/`» (007), que queda deprecada.

**Porqué:** una skill con cosas de un proyecto o de un dominio deja de servir a los demás; por eso la visión y la infografía se hicieron independientes del dominio el mismo día (004, 005). Con la fuente en un solo sitio, una mejora llega a todos los proyectos al publicar el plugin.

**Aplicada en:** `plugins/sf/skills/`; `docs/identidad/` de cada proyecto (`sf:crear_documentos`, `sf:fijar_estilo`, `sf:infografia_tecnica`, `sf:documento_vision`); especificación, 2; metodología, 6.

**Línea de estado de la 007:** Estado: deprecada el AAAA-MM-DD por «Las skills de la SF tienen su fuente en el repositorio de la SF, y lo propio de cada proyecto va en su docs/identidad/» (nueva); lo demás, por «Un solo plugin, `sf`, con las skills y activado para el usuario» (021), «Skills externas: tal cual, como dependencias; adaptadas, como propias» (175) y «Todas las skills externas actuales, como dependencias» (176).
{: .nota}

### 019 · Un mod de la SF dice si el proyecto está bajo la SF y en qué punto del método está {: #t-019}

El plugin `sf` lleva un mod que dice si el proyecto está bajo la SF y, con metodología, su fase y su devslice. Lo lee de `.sf/` (027). Lo enseña en la caja sobre el prompt; no en la línea de estado (037) ni, de momento, en el panel lateral (166).

Recoge lo que sigue valiendo de «Estado del proyecto en `docs/sf.json` y mod de estado» (019), que queda deprecada.

**Porqué:** el propietario de la Software Factory: «Me gustaría un mod de UI que me diga si el proyecto está bajo sf, en qué fase…»; «creo que el mod me aportará más en este momento fundacional y experimental de sf» (019).

**Aplicada en:** `plugins/sf/hooks/lectura.ts` y `panel.tsx` (`lineaEstado`, la caja sobre el prompt).

**Línea de estado de la 019:** Estado: deprecada el AAAA-MM-DD por «Un mod de la SF dice si el proyecto está bajo la SF y en qué punto del método está» (nueva); lo demás, por «La carpeta `.sf/` identifica el proyecto y guarda su estado» (027), «Sin línea de estado» (037) y «La línea gris del proyecto sale del panel» (166).
{: .nota}

### 023 · Ejemplos, plantillas y propuestas, cada uno en su sitio {: #t-023}

La metodología, la especificación y los demás documentos de reglas solo llevan acuerdos, preferencias y pendientes. Lo demás va a su sitio:

- Un ejemplo que ilustra una regla se queda junto a ella y empieza por «Ejemplo:». No manda nada.
- Una plantilla (por ejemplo, una estructura de código) va al plugin, en `plugins/sf/templates/`, y el documento conserva la regla y un enlace.
- Una propuesta con forma de ejemplo va a `sf/propuestas.md`.

Lo no decidido va a `sf/propuestas.md` y lo decidido, con su porqué, a `sf/decisiones/`, una decisión por archivo (108, 203, 208).

Recoge lo que sigue valiendo de «Propuestas, decisiones, plantillas y ejemplos, cada uno en su sitio» (023), que queda deprecada.

**Porqué:** `docs/mejora-continua.md` mezclaba propuestas, decisiones e historia (más de 440 líneas), y la metodología y la especificación mezclaban acuerdos con «ejemplos» de tres tipos: ilustraciones, plantillas y propuestas. El propietario de la Software Factory: «sí, adelante con la separación y unifica criterios» (023).

**Aplicada en:** metodología y especificación («Cómo interpretar este documento»); `plugins/sf/templates/`; `sf/propuestas.md`.

**Línea de estado de la 023:** Estado: deprecada el AAAA-MM-DD por «Ejemplos, plantillas y propuestas, cada uno en su sitio» (nueva); lo demás, por «Una decisión por archivo, en `docs/decisiones/`» (108), «Los documentos de la SF van en la carpeta sf/» (203) y «Las decisiones son material de la SF: siempre en sf/decisiones/» (208).
{: .nota}

### 032 · El mod es el centro de control de la SF: el método, la cola, un proyecto por sesión y las propuestas por revisar {: #t-032}

El mod de la SF lleva el control del proyecto: enseña el estado del método y la cola de tareas, controla «Un proyecto por sesión» y sigue las propuestas del proyecto. Las de su `sf/propuestas.md` que esperan revisión («pendiente de aprobación» o «pendiente de decisión» en su «Estado») se cuentan en la caja sobre el prompt y se listan en la sección Propuestas del panel (197). Una responsabilidad nueva de control de la SF se plantea primero en el mod.

Cada proyecto sigue solo sus propuestas: desde otro proyecto no se registra nada en la SF (194).

Recoge lo que sigue valiendo de «El mod, centro de control de la SF: realimentación» (032), que queda deprecada.

**Porqué:** las propuestas se acumulaban sin una vista de cuántas esperaban revisión. El propietario de la Software Factory: «sí, aprueba e implementa la realimentación en el mod. El mod va tomando responsabilidades como centro de control de la sf» (032).

**Aplicada en:** `plugins/sf/hooks/control.ts`, `lectura.ts` (`leerRealimentacion`) y `panel.tsx` (caja sobre el prompt y sección Propuestas), y sus pruebas.

**Línea de estado de la 032:** Estado: deprecada el AAAA-MM-DD por «El mod es el centro de control de la SF: el método, la cola, un proyecto por sesión y las propuestas por revisar» (nueva); lo demás, por «Sin registro ni mejoras de la SF desde otros proyectos» (194).
{: .nota}

### 053 · Las tareas del panel, en un bloque por el orden de su ciclo, y la A o la H según la sesión {: #t-053}

Bajo las tareas en curso, el panel lleva un solo bloque con sus secciones en el orden del ciclo de una tarea: Pendientes, En observación, Cerradas y, al final, Propuestas (144, 197). Cerradas lista lo cerrado en la sesión.

Una tarea en cola o en curso lleva la letra A si entró en la cola en esta sesión y H si ya estaba al abrirla. Una H nunca pasa a A, y una reabierta cuenta como H. La letra no se escribe: da el color del número (373).

Recoge lo que sigue valiendo de «Bloque TAREAS con A y H» (053), que queda deprecada.

**Porqué:** la cola vive en `.sf/peticiones.json` y pasa de una sesión a otra; el rótulo SESIÓN daba a entender lo contrario, y la lista de lo que esperaba prueba quedaba fuera de las tareas. El propietario de la Software Factory: «H es de histórico, entonces en lugar de S mejor A de actual y si una H nunca cambiará a A» (053).

**Aplicada en:** `plugins/sf/hooks/panel.tsx` (grupos y letra) y sus pruebas.

**Línea de estado de la 053:** Estado: deprecada el AAAA-MM-DD por «Las tareas del panel, en un bloque por el orden de su ciclo, y la A o la H según la sesión» (nueva); lo demás, por «La letra es el estado: A, H, T y C; Sin probar pasa a Testing» (054), «Cada tarea, en una sola sección del panel» (144), «Las propuestas, en el bloque TAREAS; sin bloque PROYECTO» (197) y «El número de una tarea lleva el color de su estado, y una reabierta cuenta como H» (373).
{: .nota}

### 054 · La letra de una tarea es su estado: A, H, O, C o D, la misma en todos los sitios {: #t-054}

Cada tarea del panel tiene un número y una letra de estado, los mismos en todos los sitios donde sale:

- A: en cola o en curso, entró en la cola en esta sesión;
- H: en cola o en curso, ya estaba al abrirla, o reabierta (373);
- O: en observación (212);
- C: cerrada, ya fuera de la cola;
- D: descartada, también si ya salió de la cola.

La letra no se escribe: da el color del número (373).

Recoge lo que sigue valiendo de «La letra es el estado: A, H, T y C; Sin probar pasa a Testing» (054), que queda deprecada.

**Porqué:** la A y la H solo decían de dónde venía la tarea, y en las demás secciones no se veía en qué estado estaba. El propietario de la Software Factory: «Una tarea en todos los sitios en los que aparezca tendrá la misma letra (estado) y número (código de procesamiento)» (054).

**Aplicada en:** `plugins/sf/hooks/panel.tsx` (`letra`, `colorNumero`) y `estilo.ts` (`colorLetra`), y sus pruebas.

**Línea de estado de la 054:** Estado: deprecada el AAAA-MM-DD por «La letra de una tarea es su estado: A, H, O, C o D, la misma en todos los sitios» (nueva); lo demás, por «Testing pasa a llamarse «En observación»» (212) y «El número de una tarea lleva el color de su estado, y una reabierta cuenta como H» (373).
{: .nota}

### 091 · La orden Activar rama pone una tarea en prueba con un clic, sin Claude y sin darla por buena {: #t-091}

La orden «Activar rama» del menú de una tarea, en cola, en curso o en observación, activa su rama para probarla. Sale si la rama existe y no es la activa; si ya lo es, la cabecera la enseña en dorado. Con un clic y sin confirmar, el panel lo hace con `cola.py probar`, sin pasar por Claude (092):

- antes integra `develop` en la rama; si choca, o si el subagente tiene trabajo sin traer, no la activa y se lo pasa a Claude (191);
- no cambia de rama si la activa tiene cambios sin commit o si la rama está en otro worktree: lo dice y no hace nada;
- una tarea en cola pasa a en curso, y el paso «Activar rama para poder probar» queda hecho (172);
- abre en el navegador los `.html` que la rama cambia respecto a `develop`.

Activar la rama no da la tarea por buena: el OK del propietario es cerrarla. Tampoco recarga el plugin: eso queda a cargo del propietario.

Recoge lo que sigue valiendo de «Botón P para probar una tarea en su rama» (091), «La P no recarga el plugin» (103) y «La P de probar pasa a T, de Test Mode» (122), que quedan deprecadas.

**Porqué:** probar una tarea en su rama se pedía a Claude, cuando basta un comando (091, 092). El propietario de la Software Factory: «no hagas el reload, queda bajo mi responsabilidad» (103), y sobre el nombre: la P «sugería que pulsarlo daba la tarea por probada, cuando solo la pone en prueba» (122).

**Aplicada en:** `plugins/sf/hooks/panel.tsx` (`botonProbar`) y `cola.ts` (`probarTarea`, `probable`, `abrirDocumentos`); `plugins/sf/tools/cola.py` (`probar`); sus pruebas.

**Línea de estado de la 091:** Estado: deprecada el AAAA-MM-DD por «La orden Activar rama pone una tarea en prueba con un clic, sin Claude y sin darla por buena» (nueva); lo demás, por «Las órdenes de cada tarea, en un menú de etiquetas» (168), «El paso de prueba es «Activar rama para poder probar»» (172) y «Activar rama integra develop, avisa a Claude si choca y adelanta la rama del subagente» (191).
{: .nota}

**Línea de estado de la 103:** Estado: deprecada el AAAA-MM-DD por «La orden Activar rama pone una tarea en prueba con un clic, sin Claude y sin darla por buena» (nueva).
{: .nota}

**Línea de estado de la 122:** Estado: deprecada el AAAA-MM-DD por «La orden Activar rama pone una tarea en prueba con un clic, sin Claude y sin darla por buena» (nueva); lo demás, por «Las órdenes de cada tarea, en un menú de etiquetas» (168).
{: .nota}

### 097 · Separar pasos de una tarea en una tarea nueva lo hace cola.py, sin Claude {: #t-097}

`/sf_split` y «Separar pasos» del panel separan pasos de una tarea en curso o en cola en una tarea nueva, también a mitad de turno. `/sf_split 89 2,3` separa los pasos 2 y 3 de la 89, numerados como salen al desplegarla; `/sf_split 89` pregunta cuáles; `/sf_split` a secas pregunta antes la tarea, entre las cuatro más recientes con dos pasos o más (otra, por su número).

Lo hace `cola.py split`, sin Claude. Antes, el mod relee la cola: si la tarea o sus pasos han cambiado, avisa y no cambia nada.

La nueva va en cola, sin rama, con el número siguiente al último dado, los pasos separados con su estado y el tipo de la original. Se llama como su primer paso y no lleva descripción (098). Si un paso separado ya estaba hecho, cola.py avisa de que su trabajo sigue en la rama de la original. Renombrar queda para el propietario o para Claude.

No se separan los pasos de cierre ni las ayudas de prueba; hacen falta dos pasos de trabajo o más, y no se pueden separar todos: eso es renombrarla.

Recoge lo que sigue valiendo de «/split separa pasos en una tarea nueva» (097), que queda deprecada.

**Porqué:** separar la eliminación de la 89 en la 96 hubo que pedírselo a Claude a mano (097). Separar es mover datos de la cola; el propietario de la Software Factory: «/split 106 2 se podría hacer sin inferencia? solo es tocar datos» («Comandos antes que inferencia»).

**Aplicada en:** `plugins/sf/hooks/register.tsx`, `cola.ts` y `panel.tsx` («Separar pasos»), y sus pruebas; `plugins/sf/tools/cola.py` (`split`); `sf:flujo_tareas`.

**Línea de estado de la 097:** Estado: deprecada el AAAA-MM-DD por «Separar pasos de una tarea en una tarea nueva lo hace cola.py, sin Claude» (nueva); lo demás, por «Las descripciones, sin origen» (098).
{: .nota}

### 108 · Una decisión por archivo, con su número de orden total, y el índice lo genera un comando {: #t-108}

Cada decisión es un archivo de `sf/decisiones/` (208), `NNN-AAAA-MM-DD-titulo.md`: el número de orden total, la fecha del registro (390) y el título sin tildes ni signos. La registra `cola.py decision`, que da el número y hace el commit en `develop`. El índice no se escribe a mano: lo genera `indice_decisiones.py`, sin Claude, con la más alta arriba (389). Sus archivos se juntan con `merge=union` y se regeneran, así que dos ramas que añaden decisiones no chocan.

Un proyecto con su registro en un solo archivo lo parte con `indice_decisiones.py --migrar` al ponerse al día.

Recoge lo que sigue valiendo de «Una decisión por archivo, en `docs/decisiones/`» (108), que queda deprecada.

**Porqué:** todas las decisiones iban en un solo `docs/decisiones.md`, y dos ramas que añadían decisiones chocaban siempre en él al cerrar con squash. El propietario de la Software Factory: «prefiero que cada decisión se convierta en un md distinto y crear una carpeta de decisiones»; «añade el número de orden total como primera columna» (108).

**Aplicada en:** `plugins/sf/tools/indice_decisiones.py` y `cola.py` (`decision`); `.gitattributes`; `sf:incorporar_proyecto_a_sf`; metodología, «Decisiones».

**Línea de estado de la 108:** Estado: deprecada el AAAA-MM-DD por «Una decisión por archivo, con su número de orden total, y el índice lo genera un comando» (nueva); lo demás, por «Las decisiones son material de la SF: siempre en sf/decisiones/» (208), «Las decisiones, en un solo formato: regla y porqué» (388), «Vigentes y deprecadas, en dos catálogos distintos con un punto de entrada común» (389) y «La fecha del nombre de archivo de una decisión es la de su registro» (390).
{: .nota}

### 117 · Un paso pendiente se quita con dos clics en su «×»; los de cierre, nunca {: #t-117}

En el panel, cada paso pendiente lleva al final una «×» roja que lo quita con dos clics: el primero la cambia por «¿Quitar? sí» (168). Solo se quita si en ese sitio sigue el mismo paso y sin empezar, porque Claude puede haber cambiado la cola entretanto. El «?» de cada paso se queda.

Los pasos de cierre, «Activar rama para poder probar» y «Cerrar la tarea», no se quitan: no llevan «×» y `cola.py paso quitar` los rechaza (174). Un paso hecho o en curso tampoco se quita.

Recoge lo que sigue valiendo de «Pasos de cierre fijos y E con confirmación para quitar pasos» (117), que queda deprecada.

**Porqué:** cada paso pendiente llevaba un «−» que lo quitaba con un clic, también los de cierre, que el panel necesita para saber que a la tarea solo le falta cerrarse; un clic suelto bastaba para perder un paso (117).

**Aplicada en:** `plugins/sf/hooks/panel.tsx` y `cola.ts` (quitar un paso) y sus pruebas; `plugins/sf/tools/cola.py` (`paso quitar`).

**Línea de estado de la 117:** Estado: deprecada el AAAA-MM-DD por «Un paso pendiente se quita con dos clics en su «×»; los de cierre, nunca» (nueva); lo demás, por «Las órdenes de cada tarea, en un menú de etiquetas» (168), «El paso de prueba es «Activar rama para poder probar»» (172) y «Los pasos de cierre, desde que la tarea entra en curso» (174).
{: .nota}

### 138 y 140 · Lo mínimo de todo proyecto SF son las tareas, el repositorio y el registro de decisiones; la metodología se elige {: #t-138-140}

Al incorporar un proyecto, la SF gestiona siempre sus tareas (la cola y su flujo), su repositorio (una rama por tarea desde `develop`, squash al cerrar y publicación a `main` con su tag; 205) y su registro de decisiones, en `sf/decisiones/` (208). Esto no se elige. Lo que se elige es la metodología (fases y documentos): `.sf/proyecto.json` dice si el proyecto la sigue, y el panel enseña la fase solo si la sigue. La configuración se cambia después con `/sf_config`.

Recoge lo que sigue valiendo de «Configuración inicial: tareas y repo siempre, el resto opcional» (138) y «El registro de decisiones es obligatorio» (140), que quedan deprecadas.

**Porqué:** un proyecto puede querer la cola y el manejo del repositorio sin seguir el método. El propietario de la Software Factory: «Lo mínimo es que sf gestione las tareas y el repo. Esto siempre» (138); «Todos los proyectos sf registrarán las decisiones. No es opcional» (140).

**Aplicada en:** `sf:incorporar_proyecto_a_sf` y `sf:configurar_proyecto`; `plugins/sf/tools/configuracion.py` (`metodologia`); el panel (`plugins/sf/hooks/panel.tsx`, la fase).

**Línea de estado de la 138:** Estado: deprecada el AAAA-MM-DD por «Lo mínimo de todo proyecto SF son las tareas, el repositorio y el registro de decisiones; la metodología se elige» (nueva); lo demás, por «El registro de decisiones es obligatorio» (140) y «El mod entrega las reglas y sf:orquestacion al empezar la sesión, tras /clear y tras compactar» (379).
{: .nota}

**Línea de estado de la 140:** Estado: deprecada el AAAA-MM-DD por «Lo mínimo de todo proyecto SF son las tareas, el repositorio y el registro de decisiones; la metodología se elige» (nueva); lo demás, por «Las decisiones son material de la SF: siempre en sf/decisiones/» (208) y «El mod entrega las reglas y sf:orquestacion al empezar la sesión, tras /clear y tras compactar» (379).
{: .nota}

### 161 · Que el proyecto va por detrás de la SF lo dice un solo aviso en el panel lateral, y la caja sobre el prompt da las dos versiones {: #t-161}

En el panel lateral, que el proyecto va por detrás de la SF lo dice solo su aviso, en la cabecera con los demás (164): «incorporado con la SF 1.1.0; va por la 1.2.2: pide a Claude «pon el proyecto al día con la SF»». El panel lateral no lo repite en otra línea (166).

La caja pequeña sobre el prompt, que sale cuando no está el panel lateral, no lleva ese aviso: da las dos versiones en su primera línea, «SF 1.1.0 → 1.2.2 · Proyecto · …».

Recoge lo que sigue valiendo de «Un solo aviso de proyecto atrasado en el panel» (161), que queda deprecada.

**Porqué:** en SmartColdBox y sprite_animation, el panel lateral decía lo mismo dos veces, en la línea gris «SF 1.1.0 → 1.2.2 · 1/7 Visión» y en el aviso; el propietario de la Software Factory, al ver el arreglo: «mantenla» (161).

**Aplicada en:** `plugins/sf/hooks/panel.tsx` (`lineaEstado` y los avisos) y sus pruebas.

**Línea de estado de la 161:** Estado: deprecada el AAAA-MM-DD por «Que el proyecto va por detrás de la SF lo dice un solo aviso en el panel lateral, y la caja sobre el prompt da las dos versiones» (nueva); lo demás, por «La línea gris del proyecto sale del panel» (166).
{: .nota}

### 168 · Las órdenes de una tarea, como etiquetas en el menú de la tarea desplegada {: #t-168}

Las órdenes de cada tarea van como etiquetas con su nombre, con mayúscula inicial y sin negrita, sobre fondo negro, en el menú de la tarea desplegada. La línea plegada no lleva ninguna, solo el ● del subagente. Toda tarea se puede desplegar y lleva la etiqueta «?», que pide a Claude que la explique (173).

Primero van las de la tarea, en verde, y al final la que destruye (Eliminar, Descartar o Revertir), en rojo. Después, las de sus pasos (Separar pasos, Paso +), con la letra atenuada. Las de dos clics confirman en la misma etiqueta: «¿Cerrar? sí». Cada paso pendiente lleva su «×», que confirma con «¿Quitar? sí», y su «?».

Qué órdenes hay y dónde sale cada una lo dice «Cómo funciona el panel», «Las órdenes de una tarea».

Recoge lo que sigue valiendo de «Las órdenes de cada tarea, en un menú de etiquetas» (168), «Toda tarea se despliega y lleva su etiqueta «?»» (173) y «Etiquetas «A Testing» en las tareas en curso y «Cerrar» en las de Testing» (182), que quedan deprecadas.

**Porqué:** el propietario de la Software Factory: «Cada vez hay más letras que memorizar lo que hacen. Lo convertimos en un menú (de etiquetas)» (168). Las letras reservaban ancho en todas las líneas.

**Aplicada en:** `plugins/sf/hooks/panel.tsx` (`etiquetaOrden` y el menú) y `estilo.ts` (`FONDO_ORDEN`, `COLOR_ORDEN_DESTRUCTIVA`), y sus pruebas.

**Línea de estado de la 168:** Estado: deprecada el AAAA-MM-DD por «Las órdenes de una tarea, como etiquetas en el menú de la tarea desplegada» (nueva).
{: .nota}

**Línea de estado de la 173:** Estado: deprecada el AAAA-MM-DD por «Las órdenes de una tarea, como etiquetas en el menú de la tarea desplegada» (nueva).
{: .nota}

**Línea de estado de la 182:** Estado: deprecada el AAAA-MM-DD por «Las órdenes de una tarea, como etiquetas en el menú de la tarea desplegada» (nueva); lo demás, por «Testing pasa a llamarse «En observación»» (212).
{: .nota}

### 202 · La SF fija su mecanismo y se adapta al proyecto en el remoto, la rama de publicación, el idioma, los commits y el manifiesto {: #t-202}

La SF fija su mecanismo, que es igual en todos los proyectos: la cola de tareas, una rama `feature/NN-nombre` por tarea desde `develop` (205), el número de la tarea en el commit, el registro de decisiones en `sf/decisiones/` (208) y sus documentos en `sf/` (203).

En lo demás se adapta a lo que el proyecto ya tiene, y lo guarda en `.sf/proyecto.json`: el remoto, la rama de publicación (`rama_main`), el idioma, el formato del commit y el manifiesto con la versión. Los documentos del proyecto no se mapean: si siguen la estructura de la SF, están donde los busca; si no, no los busca (229).

Recoge lo que sigue valiendo de «La SF fija el mecanismo y se adapta a las convenciones del proyecto» (202), que queda deprecada.

**Porqué:** incorporar un proyecto no debe reorganizarlo (201), y dejarlo todo con interruptores no lo cumplía. El propietario de la Software Factory eligió «fija el mecanismo, se adapta en todo lo demás» (202), y después sacó del «todo lo demás» las ramas (205), las decisiones (208) y el mapa de documentos (229).

**Aplicada en:** `plugins/sf/tools/configuracion.py` y `cola.py` (`convenciones`), `plugins/sf/hooks/configuracion.ts` y `contexto.ts` (la línea de convenciones), y sus pruebas; `sf:incorporar_proyecto_a_sf` («Lo fijo, lo que se detecta y lo que se elige») y `sf:configurar_proyecto`.

**Línea de estado de la 202:** Estado: deprecada el AAAA-MM-DD por «La SF fija su mecanismo y se adapta al proyecto en el remoto, la rama de publicación, el idioma, los commits y el manifiesto» (nueva); lo demás, por «El manejo del repositorio no se negocia: siempre develop» (205), «Las decisiones son material de la SF: siempre en sf/decisiones/» (208) y «Sin mapa de documentos: o se sigue la estructura de la SF, o no se mapea» (229).
{: .nota}

### 203 · Los documentos de la SF van en la carpeta sf/ y su máquina en .sf/ {: #t-203}

En todo proyecto SF, `.sf/` es la máquina: `proyecto.json`, versionado, y la cola, el estado y el historial, fuera de git. `sf/`, en la raíz y visible, guarda los documentos de la SF: `sf/propuestas.md`, `sf/informes/` y `sf/decisiones/` (208). Sus rutas son fijas (229).

Un proyecto incorporado antes los pasa a `sf/` al ponerse al día, con el OK del propietario; mientras tanto, la SF los sigue leyendo en `docs/`. Es la excepción acordada a «Incorporar un proyecto no mueve ni renombra nada» (201).

Recoge lo que sigue valiendo de «Los documentos de la SF van en la carpeta sf/» (203), que queda deprecada.

**Porqué:** en el `docs/` del proyecto chocaban con los suyos (JKanban lo tiene en inglés, OncoCore usa `_docs/`), y dentro de `.sf/` se esconden: ripgrep se salta las carpetas con punto, Obsidian no las ve y en macOS y Linux no salen en el explorador. El propietario de la Software Factory: «una carpeta sf en la raíz para las cosas de la SF, en todos los proyectos SF, así nos evitamos choques de partida» (203).

**Aplicada en:** `plugins/sf/tools/cola.py` (`PROPUESTAS`, `DECISIONES`), `indice_decisiones.py` y `plugins/sf/hooks/lectura.ts` (`RUTAS_PROPUESTAS`), y sus pruebas; `sf:incorporar_proyecto_a_sf`; `sf:informe_deliberativa` («Dónde va»).

**Línea de estado de la 203:** Estado: deprecada el AAAA-MM-DD por «Los documentos de la SF van en la carpeta sf/ y su máquina en .sf/» (nueva); lo demás, por «Las decisiones son material de la SF: siempre en sf/decisiones/» (208) y «Sin mapa de documentos: o se sigue la estructura de la SF, o no se mapea» (229).
{: .nota}

### 115 (pregunta 1) · La cola por dentro: historial, copias, bloqueo, quién y por dónde, reabrir y subagentes {: #t-115}

`cola.py`, en Python, es la única forma de cambiar la cola. Por dentro funciona así:

- **Historial.** Cada tarea lleva su historial: cada cambio, con su fecha, quién lo decide (`propietario` o `principal`) y por dónde llega (`panel` o `cli`). También entran los pasos que se añaden, se marcan o se quitan.
- **Lo que sale de la cola** pasa, con su historial, a `.sf/historial.jsonl`: una línea por salida, con el estado con que sale. Una tarea eliminada desaparece de la vista, pero no se pierde: `restaurar` la devuelve desde ahí.
- **Copias y bloqueo.** Antes de cada escritura, cola.py guarda una copia de la cola (las últimas 50) y la bloquea con `.sf/peticiones.lock`, para que dos escrituras a la vez no la rompan.
- **El commit del cierre.** El hash del squash en `develop` queda en el historial, y Revertir lo lee de ahí. Si falla el push, también se anota, y el panel lo recuerda hasta que `develop` está subida.
- **Cerrar y observar.** Cerrar una tarea con rama hace el squash en `develop`, pase o no por observación. Una tarea en observación ya está en `develop`: no se descarta, se revierte.
- **Reabrir.** Una tarea reabierta, también una descartada, sale con una rama nueva desde `develop`; nunca se reutiliza el worktree viejo.
- **Subagentes.** El subagente trabaja en su rama auxiliar, no en la de la tarea, y el principal trae su trabajo con `git merge --ff-only`. El principal anota el worktree y la rama del subagente con `cola.py subagente` antes de lanzarlo. El subagente no escribe la cola; cola.py no lo comprueba.

Recoge lo que sigue valiendo de «Flujo de tareas: respuestas a la revisión de la tabla de estados» (115), que queda deprecada.

**Porqué:** la tabla de estados de la tarea 92 dejó 23 huecos e incoherencias entre las reglas escritas y el código del panel, y el propietario de la Software Factory aprobó en bloque estas respuestas para construir `cola.py` y `sf:flujo_tareas`. El historial y las copias permiten recuperar lo que sale o se rompe; saber quién y por dónde distingue el Cerrar del propietario en el panel de un cierre del principal; el hash permite revertir; la rama auxiliar deja libre la de la tarea mientras trabaja el subagente.

**Aplicada en:** `plugins/sf/tools/cola.py`; `sf:flujo_tareas` (SKILL.md, `references/estados.md` y `references/porque.md`); el panel (`plugins/sf/hooks/lectura.ts`, `cola.ts`, `panel.tsx`).

**Línea de estado de la 115:** Estado: deprecada el 2026-11-27 por «La cola por dentro: historial, copias, bloqueo, quién y por dónde, reabrir y subagentes» (nueva); lo demás, por «Cerrar exige siempre el paso de cerrar; quitar el de probar es cerrar sin probar» (121), «El paso de prueba es «Activar rama para poder probar»» (172), «Los pasos de cierre, desde que la tarea entra en curso» (174), «Una tarea en curso con rama no vuelve a la cola» (170), «La marca del subagente, verde trabajando y roja en espera» (162), «El tipo de tarea decide cómo se maneja el repositorio» (219), «Los commits los lleva siempre Claude» (225) y «Revertir elimina la tarea o la deja pendiente» (134).
{: .nota}

### Las que se deprecan sin vigente nueva {: #t-sin}

**035:** Estado: deprecada el 2026-10-27 por «Fuera el marcador de la última fila» (038).
{: .nota}

**042:** Estado: deprecada el AAAA-MM-DD por «Una tarea en observación sale solo con el OK del propietario, que se pide tarea a tarea» (372); lo demás, por «Las comprobaciones y pruebas hechas se anotan como pasos de su tarea» (288).
{: .nota}

**058:** Estado: deprecada el 2026-11-25 por «El número de una tarea lleva el color de su estado, y una reabierta cuenta como H» (373); lo demás, por «Código de tarea más ligero: 74C» (066).
{: .nota}

**121:** Estado: deprecada el 2026-11-01 por «Los pasos de cierre, desde que la tarea entra en curso» (174); lo demás, por «El paso de prueba es «Activar rama para poder probar»» (172).
{: .nota}

**192:** Estado: deprecada el 2026-11-01 por «Sin registro ni mejoras de la SF desde otros proyectos» (194).
{: .nota}

**253:** Estado: deprecada el 2026-11-05 por «Botones del panel en la app de escritorio con el fondo de su color» (290).
{: .nota}

:::

## Decidido | Lo que ya está decidido | Decidido {#decidido}

| Nº | Decisión | Qué fija aquí |
| --- | --- | --- |
| 388 | Las decisiones, en un solo formato: regla y porqué | El formato de cada vigente nueva y de la línea de estado. |
| 389 | Vigentes y deprecadas, en dos catálogos distintos con un punto de entrada común | Adónde va cada antigua al deprecarla. |
| 390 | La fecha del nombre de archivo de una decisión es la de su registro | La fecha de la vigente nueva y de la línea de estado. |

Después del OK, sin otra decisión: las citas «115 (n)» de `sf:flujo_tareas` y los hooks pasan a la vigente nueva; la ayuda de `cola.py paso quitar` nombra los dos pasos de cierre; el comentario de `exigir_cierre` cita la 172 y la 174 en vez de la 121.
{: .nota}
