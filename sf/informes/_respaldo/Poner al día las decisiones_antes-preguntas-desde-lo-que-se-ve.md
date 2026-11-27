---
antetitulo: Software Factory · Informe de análisis · Noviembre 2026
lema: Once preguntas; // el resto, en bloque.
subtitulo: Qué reglas antiguas de la SF se deprecan, con qué regla vigente nueva, y las once preguntas que necesitan el criterio del propietario.
version: Versión 2.1 · 27/11/2026
estado: Propuesta · Tarea 439
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de análisis
pie: Informe de la tarea «Poner al día las decisiones: un solo formato y las antiguas, deprecadas» (439). Parte de las decisiones de sf/decisiones/ en develop, de las decisiones 360, 388, 389 y 390, y de cola.py, los hooks del panel y las skills en el worktree de la tarea. Espera la decisión del propietario.
---
# Poner al día las decisiones

## Resumen | Once preguntas y un bloque | Resumen {#resumen}

**11 preguntas** necesitan el criterio del propietario: tres sobre cómo funciona la cola de tareas por dentro y ocho sueltas, sobre el panel, las skills y otras reglas. Cada una se entiende sola.

**26 reglas antiguas** se deprecan en bloque, sin pregunta: lo que sigue valiendo de 20 pasa a 15 reglas vigentes nuevas, y lo de las otras 6 ya lo dicen reglas vigentes.

**Cómo contestar:** las preguntas por número («1 A, 2 A…» o «todas A») y OK al bloque.
{: .texto}

[Ver las preguntas](#por-decidir){: .salto}

## Por decidir | Lo que necesita su criterio | Preguntas {#por-decidir}

Once preguntas, una por ficha. Cada una dice de qué va, qué cambia y qué pasa con cada opción. La recomendada es siempre la A.

::: preguntas 2

### 1 · Cómo funciona la cola de tareas por dentro: ¿una regla vigente nueva o dos? (115) {recomendada=A} {: #p1}

La cola de tareas (lo que el panel enseña en Pendientes, En curso y En observación) solo la cambia `cola.py`. Cómo guarda el historial de cada tarea, sus copias de seguridad, el cierre, reabrir y los subagentes lo dice una regla antigua de 23 puntos sueltos («Flujo de tareas: respuestas a la revisión de la tabla de estados», 115). Lo que sigue valiendo pasa a una regla vigente nueva, y la skill de tareas y el panel citan la antigua por punto en unos 40 sitios.

Opción A
:   Una sola regla, en lista ([su texto](#t-115)): cada cita pasa a un solo número.

Opción B
:   Dos reglas, «la cola por dentro» y «cerrar, reabrir y subagentes»: se leen mejor por tema, pero cada cita hay que repartirla entre las dos.

Recomendación
:   **A.** Menos trabajo y ninguna cita dudosa.

### 2 · Deshacer la fusión de dos tareas: ¿qué se hace con lo que se prometió? (115) {recomendada=A} {: #p2}

En el panel se pueden fusionar dos tareas: una absorbe a la otra. La regla antigua de la cola prometía una orden para deshacerlo, `/desfusionar`, que nunca se hizo; y `cola.py`, al intentar reabrir una tarea absorbida, aún remite a ella.

Opción A
:   Fuera: una fusión no se deshace; lo absorbido se saca a una tarea nueva con «Separar pasos» (`/sf_split`), y `cola.py` lo dice así.

Opción B
:   A una propuesta de `sf/propuestas.md`, por si un día se hace la orden.

Opción C
:   En la regla vigente nueva, como pendiente.

Recomendación
:   **A.** «Separar pasos» ya cubre el caso.

### 3 · Restos de una regla vieja en la skill de tareas: ¿se quitan? (115) {recomendada=A} {: #p3}

Antes, una propuesta de mejora podía ser una tarea con su rama. Hoy las propuestas viven en `sf/propuestas.md` y, al aceptarlas, pasan a la cola como una tarea más. La skill que lleva la cola (`sf:flujo_tareas`) aún habla en tres sitios de «una propuesta que toca un activo».

Opción A
:   Se quitan en esta tarea: la skill deja de describir algo que ya no pasa.

Opción B
:   Se quedan hasta otra tarea.

Recomendación
:   **A.** Son tres frases en una skill del plugin.

### 4 · Dónde viven las skills y lo propio de cada proyecto: ¿vale este porqué? (007) {recomendada=A} {: #p4}

Una regla antigua dice que las skills de la SF tienen su fuente en el repositorio de la SF, y que lo propio de cada proyecto (su estilo, su logo, las reglas de su dominio) va en su `docs/identidad/`, nunca en la skill. No dejó escrito por qué, y su regla vigente nueva lo necesita. El propuesto: una skill con cosas de un proyecto deja de servir a los demás, y con la fuente en un solo sitio una mejora llega a todos los proyectos al publicar el plugin.

Opción A
:   Vale ([su texto](#t-007)). Sale de cuando las skills de visión y de infografía se hicieron independientes de su proyecto, el mismo día (004, 005).

Opción B
:   Otro porqué: dilo en el chat.

Recomendación
:   **A.** Es el que se ve en lo que se hizo ese día.

### 5 · La caja del estado del proyecto, sobre el prompt: ¿regla nueva o bastan las que hay? (019) {recomendada=A} {: #p5}

Sobre el prompt, una caja pequeña dice si el proyecto está bajo la SF y, si sigue el método, su fase y su devslice. La regla antigua guardaba ese estado en `docs/sf.json` y lo enseñaba en la línea de estado; las dos cosas cambiaron.

Opción A
:   Una regla vigente nueva que dice cómo es hoy ([su texto](#t-019)): el mod lo lee de `.sf/` y lo enseña en la caja sobre el prompt.

Opción B
:   Ninguna regla nueva: lo dejan dicho otras tres, y una de ellas, la del mod como centro de control de la SF (032), también se depreca en este informe.

Recomendación
:   **A.** No se apoya en otra regla que también se depreca.

### 6 · Quitar un paso de una tarea en el panel: ¿regla nueva o bastan las que hay? (117) {recomendada=A} {: #p6}

En el panel, cada paso pendiente de una tarea lleva una «×» roja: el primer clic pide «¿Quitar? sí» y el segundo lo quita. Los dos pasos de cierre no se pueden quitar. Y solo se quita si el paso sigue en su sitio y sin empezar, por si Claude ha cambiado la cola entretanto; esto último no lo dice ninguna regla.

Opción A
:   Una regla vigente nueva con las tres cosas ([su texto](#t-117)).

Opción B
:   Ninguna regla nueva: el menú de etiquetas (168) y los pasos de cierre (174) ya dicen las dos primeras; la tercera queda solo en el código.

Recomendación
:   **A.** No se pierde lo que hace el código.

### 7 · Las etiquetas de las órdenes de una tarea: ¿se quedan con fondo negro y texto verde? (168) {recomendada=A} {: #p7}

Al desplegar una tarea en el panel salen sus órdenes como etiquetas: Activar rama, Cerrar, Paso +… Desde el 2026-11-01 llevan fondo negro, y las de la tarea van en verde. Se pidió «a prueba», sin regla escrita; la regla vigente nueva del menú de etiquetas lo recoge.

Opción A
:   Se quedan: la regla lo dice ([su texto](#t-168)).

Opción B
:   Siguen a prueba: la regla no habla del color.

Recomendación
:   **A.** Están así desde entonces.

### 8 · Las letras A y H de las tareas del panel: ¿en una regla o en dos? (053, 054) {recomendada=A} {: #p8}

En el panel, el número de cada tarea va del color de su letra: A si entró en la cola en esta sesión, H si ya estaba, O en observación, C cerrada, D descartada. Hay dos reglas antiguas, una sobre el bloque de tareas y su orden, que también habla de la A y la H, y otra sobre la letra como estado. Cada una tiene su regla vigente nueva, y las dos repiten la A y la H.

Opción A
:   Dos reglas, tal cual ([el bloque](#t-053), [la letra](#t-054)): el orden del bloque y la letra son dos temas, y lo repetido es una línea.

Opción B
:   Una sola regla: el bloque de tareas y la letra de cada una.

Opción C
:   Dos, y la A y la H solo en la de la letra.

Recomendación
:   **A.** Cada regla, de un tema.

### 9 · El panel sin horas, y el color de la tarea en curso: ¿regla nueva? (071) {recomendada=A} {: #p9}

Una regla antigua dice que el panel no enseña horas ni antigüedades («ahora», «5 min») y que la tarea en curso solo va en color arriba. Lo del color cambió dos veces: su código va en color también en las secciones (084), y el amarillo pasó a dorado (355). Ese cambio está escrito dentro del texto de la regla, así que el índice la cuenta como vigente entera.

Opción A
:   Se depreca con una regla vigente nueva, que se escribe en la próxima vuelta tras comprobar el dorado en el panel.

Opción B
:   Se depreca sin regla nueva: se pierde lo de las horas, que no dice otra regla.

Opción C
:   Se queda como está.

Recomendación
:   **A.** Lo de las horas no está en otra regla.

### 10 · Mejoras de la SF vistas en otro proyecto: ¿regla nueva? (194) {recomendada=A} {: #p10}

Una regla dice que ningún proyecto escribe en la SF, y que una mejora de la SF vista en un proyecto se anota como propuesta de ese proyecto. Después se corrigió: no se anota; Claude la dice en una línea, y el propietario la lleva a la SF (210). La corrección está escrita dentro del texto, así que el índice la cuenta como vigente entera.

Opción A
:   Se depreca con una regla vigente nueva, que se escribe en la próxima vuelta de esta tarea.

Opción B
:   Se queda como está.

Recomendación
:   **A.** El mismo trato que las demás.

### 11 · Una tarea en observación que otra posterior ya ha dejado atrás: ¿sale sola? (042) {recomendada=A} {: #p11}

Una tarea en observación ya está en `develop` y espera a que el propietario la dé por buena: sale solo con su OK, que Claude pide tarea a tarea («¿Cómo va la N?»). Una regla antigua decía que también sale si un cambio posterior la deja atrás. Hoy no lo hace nada.

Opción A
:   No se recoge: sigue saliendo solo con el OK del propietario.

Opción B
:   Se recoge en una regla vigente nueva: Claude la saca si un cambio posterior la deja atrás.

Recomendación
:   **A.** Así lo decide siempre el propietario.

:::

## En bloque | Las que se deprecan sin pregunta | En bloque {#en-bloque}

Una fila por regla antigua que se depreca. Se aprueban todas con un OK. Dos filas, la caja del estado del proyecto (019) y quitar un paso (117), dependen de las preguntas [5](#p5) y [6](#p6).

| Nº | Qué decía | Cómo queda |
| --- | --- | --- |
| 007 | Dónde viven las skills: su fuente, en la SF; lo de cada proyecto, en su `docs/identidad/`. | [Vigente nueva](#t-007): las skills tienen su fuente en el repositorio de la SF y viajan en el plugin; lo de cada proyecto, en su `docs/identidad/`. |
| 019 | La caja del estado del proyecto: el estado, en `docs/sf.json`, en la línea de estado y en el panel. | [Vigente nueva](#t-019): un mod dice si el proyecto está bajo la SF y su fase, leyendo `.sf/`, en la caja sobre el prompt. |
| 023 | Dónde va cada cosa en los documentos: propuestas, decisiones, plantillas y ejemplos. | [Vigente nueva](#t-023): un ejemplo va junto a su regla, una plantilla al plugin y una propuesta a `sf/propuestas.md`. |
| 032 | El mod como centro de control de la SF, con las propuestas de todos los proyectos. | [Vigente nueva](#t-032): el mod lleva el método, la cola, un proyecto por sesión y las propuestas por revisar del proyecto. |
| 053 | El bloque de tareas del panel, con la A o la H según la sesión. | [Vigente nueva](#t-053): las tareas, en un bloque por el orden de su ciclo; la A o la H da el color del número. |
| 054 | La letra de cada tarea en el panel: A, H, T o C, según su estado. | [Vigente nueva](#t-054): la letra es el estado, A, H, O, C o D, y solo da el color del número. |
| 091, 103 y 122 | El botón para probar una tarea en su rama: P, luego T, sin recargar el plugin. | [Vigente nueva](#t-091): «Activar rama» la pone en prueba con un clic, sin Claude y sin darla por buena. |
| 097 | Separar pasos de una tarea en otra nueva: la orden `/split`. | [Vigente nueva](#t-097): `/sf_split` y «Separar pasos» lo hacen con `cola.py`, sin Claude y sin los pasos de cierre. |
| 108 | Dónde se guardan las decisiones: una por archivo, en `docs/decisiones/`. | [Vigente nueva](#t-108): una por archivo en `sf/decisiones/`, numerada, y el índice lo genera un comando. |
| 117 | Quitar un paso de una tarea en el panel: la E, con confirmación; los de cierre, fijos. | [Vigente nueva](#t-117): un paso pendiente se quita con dos clics en su «×»; los de cierre, nunca. |
| 138 y 140 | Qué gestiona siempre la SF en un proyecto: tareas y repositorio; después, también las decisiones. | [Vigente nueva](#t-138-140): lo mínimo son las tareas, el repositorio y el registro de decisiones; la metodología se elige. |
| 161 | El aviso de proyecto atrasado respecto a la SF: uno solo en el panel. | [Vigente nueva](#t-161): el aviso, solo en la cabecera del panel; la caja sobre el prompt da las dos versiones. |
| 168, 173 y 182 | Las órdenes de una tarea en el panel: un menú de etiquetas, «?» en todas, etiquetas de Testing. | [Vigente nueva](#t-168): las órdenes, como etiquetas en el menú de la tarea desplegada, y la destructiva al final, en rojo. |
| 202 | Qué fija la SF y qué adapta a cada proyecto: fija el mecanismo, adapta lo demás. | [Vigente nueva](#t-202): se adapta solo en el remoto, la rama de publicación, el idioma, los commits y el manifiesto. |
| 203 | Dónde van los documentos de la SF en un proyecto: en `sf/`. | [Vigente nueva](#t-203): los documentos de la SF, en `sf/`, y su máquina, en `.sf/`, con rutas fijas. |
| 035 | Un marcador del día en el panel: terminadas, dejadas y propuestas. | Nada nuevo: el marcador ya se quitó (038). |
| 042 | Cuándo sale una tarea de Sin probar: también si Claude la comprueba. | Nada nuevo: sale solo con el OK del propietario (372), y lo que comprueba Claude se anota como paso (288). |
| 058 | Cómo se escribe el código de una tarea: «57-A». | Nada nuevo: el número va sin letra, y la letra da su color (066, 373). |
| 121 | Qué exige cerrar una tarea: el paso de cerrar; quitar el de probar es cerrar sin probar. | Nada nuevo: los pasos de cierre se ponen al entrar en curso y no se quitan (172, 174). |
| 192 | Cómo se escribe en la SF una mejora vista en otro proyecto: con Edit o Write. | Nada nuevo: ningún proyecto escribe en la SF (194). |
| 253 | Los botones del panel en la app de escritorio: con contorno de color. | Nada nuevo: los botones llevan el fondo de su color (290). |

Al aprobar, el principal registra cada regla vigente nueva con `cola.py decision` y pone a cada antigua su línea de estado, con la fecha del registro (390). La antigua pasa al catálogo de deprecadas (389).
{: .nota}

## Textos | El texto entero de cada vigente nueva | Textos {#textos}

Solo para quien quiera mirarlo: cada regla vigente nueva, tal como se registraría, con la línea de estado de la antigua debajo. Al final, las líneas de estado de las que se deprecan sin regla nueva.

::: tarjetas 1 plegables

### Las skills de la SF tienen su fuente en el repositorio de la SF, y lo propio de cada proyecto va en su docs/identidad/ (007) {: #t-007}

Las skills de la SF, las propias y las externas que adaptamos, tienen su fuente versionada en el repositorio de la SF, en `plugins/sf/skills/`, y viajan en el plugin `sf`. Una skill externa que se usa tal cual no se copia: es una dependencia del plugin, fijada a su commit (175, 176).

Lo propio de cada proyecto (estilo, tema, logo, producto y reglas del dominio) va en su `docs/identidad/`, nunca en la skill.

Recoge lo que sigue valiendo de «Fuente de las skills en la SF y lo propio de cada proyecto en `docs/identidad/`» (007), que queda deprecada.

**Porqué:** una skill con cosas de un proyecto o de un dominio deja de servir a los demás; por eso la visión y la infografía se hicieron independientes del dominio el mismo día (004, 005). Con la fuente en un solo sitio, una mejora llega a todos los proyectos al publicar el plugin.

**Aplicada en:** `plugins/sf/skills/`; `docs/identidad/` de cada proyecto (`sf:crear_documentos`, `sf:fijar_estilo`, `sf:infografia_tecnica`, `sf:documento_vision`); especificación, 2; metodología, 6.

**Línea de estado de la antigua (007):** Estado: deprecada el AAAA-MM-DD por «Las skills de la SF tienen su fuente en el repositorio de la SF, y lo propio de cada proyecto va en su docs/identidad/» (nueva); lo demás, por «Un solo plugin, `sf`, con las skills y activado para el usuario» (021), «Skills externas: tal cual, como dependencias; adaptadas, como propias» (175) y «Todas las skills externas actuales, como dependencias» (176).
{: .nota}

### Un mod de la SF dice si el proyecto está bajo la SF y en qué punto del método está (019) {: #t-019}

El plugin `sf` lleva un mod que dice si el proyecto está bajo la SF y, con metodología, su fase y su devslice. Lo lee de `.sf/` (027). Lo enseña en la caja sobre el prompt; no en la línea de estado (037) ni, de momento, en el panel lateral (166).

Recoge lo que sigue valiendo de «Estado del proyecto en `docs/sf.json` y mod de estado» (019), que queda deprecada.

**Porqué:** el propietario de la Software Factory: «Me gustaría un mod de UI que me diga si el proyecto está bajo sf, en qué fase…»; «creo que el mod me aportará más en este momento fundacional y experimental de sf» (019).

**Aplicada en:** `plugins/sf/hooks/lectura.ts` y `panel.tsx` (`lineaEstado`, la caja sobre el prompt).

**Línea de estado de la antigua (019):** Estado: deprecada el AAAA-MM-DD por «Un mod de la SF dice si el proyecto está bajo la SF y en qué punto del método está» (nueva); lo demás, por «La carpeta `.sf/` identifica el proyecto y guarda su estado» (027), «Sin línea de estado» (037) y «La línea gris del proyecto sale del panel» (166).
{: .nota}

### Ejemplos, plantillas y propuestas, cada uno en su sitio (023) {: #t-023}

La metodología, la especificación y los demás documentos de reglas solo llevan acuerdos, preferencias y pendientes. Lo demás va a su sitio:

- Un ejemplo que ilustra una regla se queda junto a ella y empieza por «Ejemplo:». No manda nada.
- Una plantilla (por ejemplo, una estructura de código) va al plugin, en `plugins/sf/templates/`, y el documento conserva la regla y un enlace.
- Una propuesta con forma de ejemplo va a `sf/propuestas.md`.

Lo no decidido va a `sf/propuestas.md` y lo decidido, con su porqué, a `sf/decisiones/`, una decisión por archivo (108, 203, 208).

Recoge lo que sigue valiendo de «Propuestas, decisiones, plantillas y ejemplos, cada uno en su sitio» (023), que queda deprecada.

**Porqué:** `docs/mejora-continua.md` mezclaba propuestas, decisiones e historia (más de 440 líneas), y la metodología y la especificación mezclaban acuerdos con «ejemplos» de tres tipos: ilustraciones, plantillas y propuestas. El propietario de la Software Factory: «sí, adelante con la separación y unifica criterios» (023).

**Aplicada en:** metodología y especificación («Cómo interpretar este documento»); `plugins/sf/templates/`; `sf/propuestas.md`.

**Línea de estado de la antigua (023):** Estado: deprecada el AAAA-MM-DD por «Ejemplos, plantillas y propuestas, cada uno en su sitio» (nueva); lo demás, por «Una decisión por archivo, en `docs/decisiones/`» (108), «Los documentos de la SF van en la carpeta sf/» (203) y «Las decisiones son material de la SF: siempre en sf/decisiones/» (208).
{: .nota}

### El mod es el centro de control de la SF: el método, la cola, un proyecto por sesión y las propuestas por revisar (032) {: #t-032}

El mod de la SF lleva el control del proyecto: enseña el estado del método y la cola de tareas, controla «Un proyecto por sesión» y sigue las propuestas del proyecto. Las de su `sf/propuestas.md` que esperan revisión («pendiente de aprobación» o «pendiente de decisión» en su «Estado») se cuentan en la caja sobre el prompt y se listan en la sección Propuestas del panel (197). Una responsabilidad nueva de control de la SF se plantea primero en el mod.

Cada proyecto sigue solo sus propuestas: desde otro proyecto no se registra nada en la SF (194).

Recoge lo que sigue valiendo de «El mod, centro de control de la SF: realimentación» (032), que queda deprecada.

**Porqué:** las propuestas se acumulaban sin una vista de cuántas esperaban revisión. El propietario de la Software Factory: «sí, aprueba e implementa la realimentación en el mod. El mod va tomando responsabilidades como centro de control de la sf» (032).

**Aplicada en:** `plugins/sf/hooks/control.ts`, `lectura.ts` (`leerRealimentacion`) y `panel.tsx` (caja sobre el prompt y sección Propuestas), y sus pruebas.

**Línea de estado de la antigua (032):** Estado: deprecada el AAAA-MM-DD por «El mod es el centro de control de la SF: el método, la cola, un proyecto por sesión y las propuestas por revisar» (nueva); lo demás, por «Sin registro ni mejoras de la SF desde otros proyectos» (194).
{: .nota}

### Las tareas del panel, en un bloque por el orden de su ciclo, y la A o la H según la sesión (053) {: #t-053}

Bajo las tareas en curso, el panel lleva un solo bloque con sus secciones en el orden del ciclo de una tarea: Pendientes, En observación, Cerradas y, al final, Propuestas (144, 197). Cerradas lista lo cerrado en la sesión.

Una tarea en cola o en curso lleva la letra A si entró en la cola en esta sesión y H si ya estaba al abrirla. Una H nunca pasa a A, y una reabierta cuenta como H. La letra no se escribe: da el color del número (373).

Recoge lo que sigue valiendo de «Bloque TAREAS con A y H» (053), que queda deprecada.

**Porqué:** la cola vive en `.sf/peticiones.json` y pasa de una sesión a otra; el rótulo SESIÓN daba a entender lo contrario, y la lista de lo que esperaba prueba quedaba fuera de las tareas. El propietario de la Software Factory: «H es de histórico, entonces en lugar de S mejor A de actual y si una H nunca cambiará a A» (053).

**Aplicada en:** `plugins/sf/hooks/panel.tsx` (grupos y letra) y sus pruebas.

**Línea de estado de la antigua (053):** Estado: deprecada el AAAA-MM-DD por «Las tareas del panel, en un bloque por el orden de su ciclo, y la A o la H según la sesión» (nueva); lo demás, por «La letra es el estado: A, H, T y C; Sin probar pasa a Testing» (054), «Cada tarea, en una sola sección del panel» (144), «Las propuestas, en el bloque TAREAS; sin bloque PROYECTO» (197) y «El número de una tarea lleva el color de su estado, y una reabierta cuenta como H» (373).
{: .nota}

### La letra de una tarea es su estado: A, H, O, C o D, la misma en todos los sitios (054) {: #t-054}

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

**Línea de estado de la antigua (054):** Estado: deprecada el AAAA-MM-DD por «La letra de una tarea es su estado: A, H, O, C o D, la misma en todos los sitios» (nueva); lo demás, por «Testing pasa a llamarse «En observación»» (212) y «El número de una tarea lleva el color de su estado, y una reabierta cuenta como H» (373).
{: .nota}

### La orden Activar rama pone una tarea en prueba con un clic, sin Claude y sin darla por buena (091) {: #t-091}

La orden «Activar rama» del menú de una tarea, en cola, en curso o en observación, activa su rama para probarla. Sale si la rama existe y no es la activa; si ya lo es, la cabecera la enseña en dorado. Con un clic y sin confirmar, el panel lo hace con `cola.py probar`, sin pasar por Claude (092):

- antes integra `develop` en la rama; si choca, o si el subagente tiene trabajo sin traer, no la activa y se lo pasa a Claude (191);
- no cambia de rama si la activa tiene cambios sin commit o si la rama está en otro worktree: lo dice y no hace nada;
- una tarea en cola pasa a en curso, y el paso «Activar rama para poder probar» queda hecho (172);
- abre en el navegador los `.html` que la rama cambia respecto a `develop`.

Activar la rama no da la tarea por buena: el OK del propietario es cerrarla. Tampoco recarga el plugin: eso queda a cargo del propietario.

Recoge lo que sigue valiendo de «Botón P para probar una tarea en su rama» (091), «La P no recarga el plugin» (103) y «La P de probar pasa a T, de Test Mode» (122), que quedan deprecadas.

**Porqué:** probar una tarea en su rama se pedía a Claude, cuando basta un comando (091, 092). El propietario de la Software Factory: «no hagas el reload, queda bajo mi responsabilidad» (103), y sobre el nombre: la P «sugería que pulsarlo daba la tarea por probada, cuando solo la pone en prueba» (122).

**Aplicada en:** `plugins/sf/hooks/panel.tsx` (`botonProbar`) y `cola.ts` (`probarTarea`, `probable`, `abrirDocumentos`); `plugins/sf/tools/cola.py` (`probar`); sus pruebas.

**Línea de estado de la antigua (091):** Estado: deprecada el AAAA-MM-DD por «La orden Activar rama pone una tarea en prueba con un clic, sin Claude y sin darla por buena» (nueva); lo demás, por «Las órdenes de cada tarea, en un menú de etiquetas» (168), «El paso de prueba es «Activar rama para poder probar»» (172) y «Activar rama integra develop, avisa a Claude si choca y adelanta la rama del subagente» (191).
{: .nota}

**Línea de estado de la antigua (103):** Estado: deprecada el AAAA-MM-DD por «La orden Activar rama pone una tarea en prueba con un clic, sin Claude y sin darla por buena» (nueva).
{: .nota}

**Línea de estado de la antigua (122):** Estado: deprecada el AAAA-MM-DD por «La orden Activar rama pone una tarea en prueba con un clic, sin Claude y sin darla por buena» (nueva); lo demás, por «Las órdenes de cada tarea, en un menú de etiquetas» (168).
{: .nota}

### Separar pasos de una tarea en una tarea nueva lo hace cola.py, sin Claude (097) {: #t-097}

`/sf_split` y «Separar pasos» del panel separan pasos de una tarea en curso o en cola en una tarea nueva, también a mitad de turno. `/sf_split 89 2,3` separa los pasos 2 y 3 de la 89, numerados como salen al desplegarla; `/sf_split 89` pregunta cuáles; `/sf_split` a secas pregunta antes la tarea, entre las cuatro más recientes con dos pasos o más (otra, por su número).

Lo hace `cola.py split`, sin Claude. Antes, el mod relee la cola: si la tarea o sus pasos han cambiado, avisa y no cambia nada.

La nueva va en cola, sin rama, con el número siguiente al último dado, los pasos separados con su estado y el tipo de la original. Se llama como su primer paso y no lleva descripción (098). Si un paso separado ya estaba hecho, cola.py avisa de que su trabajo sigue en la rama de la original. Renombrar queda para el propietario o para Claude.

No se separan los pasos de cierre ni las ayudas de prueba; hacen falta dos pasos de trabajo o más, y no se pueden separar todos: eso es renombrarla.

Recoge lo que sigue valiendo de «/split separa pasos en una tarea nueva» (097), que queda deprecada.

**Porqué:** separar la eliminación de la 89 en la 96 hubo que pedírselo a Claude a mano (097). Separar es mover datos de la cola; el propietario de la Software Factory: «/split 106 2 se podría hacer sin inferencia? solo es tocar datos» («Comandos antes que inferencia»).

**Aplicada en:** `plugins/sf/hooks/register.tsx`, `cola.ts` y `panel.tsx` («Separar pasos»), y sus pruebas; `plugins/sf/tools/cola.py` (`split`); `sf:flujo_tareas`.

**Línea de estado de la antigua (097):** Estado: deprecada el AAAA-MM-DD por «Separar pasos de una tarea en una tarea nueva lo hace cola.py, sin Claude» (nueva); lo demás, por «Las descripciones, sin origen» (098).
{: .nota}

### Una decisión por archivo, con su número de orden total, y el índice lo genera un comando (108) {: #t-108}

Cada decisión es un archivo de `sf/decisiones/` (208), `NNN-AAAA-MM-DD-titulo.md`: el número de orden total, la fecha del registro (390) y el título sin tildes ni signos. La registra `cola.py decision`, que da el número y hace el commit en `develop`. El índice no se escribe a mano: lo genera `indice_decisiones.py`, sin Claude, con la más alta arriba (389). Sus archivos se juntan con `merge=union` y se regeneran, así que dos ramas que añaden decisiones no chocan.

Un proyecto con su registro en un solo archivo lo parte con `indice_decisiones.py --migrar` al ponerse al día.

Recoge lo que sigue valiendo de «Una decisión por archivo, en `docs/decisiones/`» (108), que queda deprecada.

**Porqué:** todas las decisiones iban en un solo `docs/decisiones.md`, y dos ramas que añadían decisiones chocaban siempre en él al cerrar con squash. El propietario de la Software Factory: «prefiero que cada decisión se convierta en un md distinto y crear una carpeta de decisiones»; «añade el número de orden total como primera columna» (108).

**Aplicada en:** `plugins/sf/tools/indice_decisiones.py` y `cola.py` (`decision`); `.gitattributes`; `sf:incorporar_proyecto_a_sf`; metodología, «Decisiones».

**Línea de estado de la antigua (108):** Estado: deprecada el AAAA-MM-DD por «Una decisión por archivo, con su número de orden total, y el índice lo genera un comando» (nueva); lo demás, por «Las decisiones son material de la SF: siempre en sf/decisiones/» (208), «Las decisiones, en un solo formato: regla y porqué» (388), «Vigentes y deprecadas, en dos catálogos distintos con un punto de entrada común» (389) y «La fecha del nombre de archivo de una decisión es la de su registro» (390).
{: .nota}

### Un paso pendiente se quita con dos clics en su «×»; los de cierre, nunca (117) {: #t-117}

En el panel, cada paso pendiente lleva al final una «×» roja que lo quita con dos clics: el primero la cambia por «¿Quitar? sí» (168). Solo se quita si en ese sitio sigue el mismo paso y sin empezar, porque Claude puede haber cambiado la cola entretanto. El «?» de cada paso se queda.

Los pasos de cierre, «Activar rama para poder probar» y «Cerrar la tarea», no se quitan: no llevan «×» y `cola.py paso quitar` los rechaza (174). Un paso hecho o en curso tampoco se quita.

Recoge lo que sigue valiendo de «Pasos de cierre fijos y E con confirmación para quitar pasos» (117), que queda deprecada.

**Porqué:** cada paso pendiente llevaba un «−» que lo quitaba con un clic, también los de cierre, que el panel necesita para saber que a la tarea solo le falta cerrarse; un clic suelto bastaba para perder un paso (117).

**Aplicada en:** `plugins/sf/hooks/panel.tsx` y `cola.ts` (quitar un paso) y sus pruebas; `plugins/sf/tools/cola.py` (`paso quitar`).

**Línea de estado de la antigua (117):** Estado: deprecada el AAAA-MM-DD por «Un paso pendiente se quita con dos clics en su «×»; los de cierre, nunca» (nueva); lo demás, por «Las órdenes de cada tarea, en un menú de etiquetas» (168), «El paso de prueba es «Activar rama para poder probar»» (172) y «Los pasos de cierre, desde que la tarea entra en curso» (174).
{: .nota}

### Lo mínimo de todo proyecto SF son las tareas, el repositorio y el registro de decisiones; la metodología se elige (138, 140) {: #t-138-140}

Al incorporar un proyecto, la SF gestiona siempre sus tareas (la cola y su flujo), su repositorio (una rama por tarea desde `develop`, squash al cerrar y publicación a `main` con su tag; 205) y su registro de decisiones, en `sf/decisiones/` (208). Esto no se elige. Lo que se elige es la metodología (fases y documentos): `.sf/proyecto.json` dice si el proyecto la sigue, y el panel enseña la fase solo si la sigue. La configuración se cambia después con `/sf_config`.

Recoge lo que sigue valiendo de «Configuración inicial: tareas y repo siempre, el resto opcional» (138) y «El registro de decisiones es obligatorio» (140), que quedan deprecadas.

**Porqué:** un proyecto puede querer la cola y el manejo del repositorio sin seguir el método. El propietario de la Software Factory: «Lo mínimo es que sf gestione las tareas y el repo. Esto siempre» (138); «Todos los proyectos sf registrarán las decisiones. No es opcional» (140).

**Aplicada en:** `sf:incorporar_proyecto_a_sf` y `sf:configurar_proyecto`; `plugins/sf/tools/configuracion.py` (`metodologia`); el panel (`plugins/sf/hooks/panel.tsx`, la fase).

**Línea de estado de la antigua (138):** Estado: deprecada el AAAA-MM-DD por «Lo mínimo de todo proyecto SF son las tareas, el repositorio y el registro de decisiones; la metodología se elige» (nueva); lo demás, por «El registro de decisiones es obligatorio» (140) y «El mod entrega las reglas y sf:orquestacion al empezar la sesión, tras /clear y tras compactar» (379).
{: .nota}

**Línea de estado de la antigua (140):** Estado: deprecada el AAAA-MM-DD por «Lo mínimo de todo proyecto SF son las tareas, el repositorio y el registro de decisiones; la metodología se elige» (nueva); lo demás, por «Las decisiones son material de la SF: siempre en sf/decisiones/» (208) y «El mod entrega las reglas y sf:orquestacion al empezar la sesión, tras /clear y tras compactar» (379).
{: .nota}

### Que el proyecto va por detrás de la SF lo dice un solo aviso en el panel lateral, y la caja sobre el prompt da las dos versiones (161) {: #t-161}

En el panel lateral, que el proyecto va por detrás de la SF lo dice solo su aviso, en la cabecera con los demás (164): «incorporado con la SF 1.1.0; va por la 1.2.2: pide a Claude «pon el proyecto al día con la SF»». El panel lateral no lo repite en otra línea (166).

La caja pequeña sobre el prompt, que sale cuando no está el panel lateral, no lleva ese aviso: da las dos versiones en su primera línea, «SF 1.1.0 → 1.2.2 · Proyecto · …».

Recoge lo que sigue valiendo de «Un solo aviso de proyecto atrasado en el panel» (161), que queda deprecada.

**Porqué:** en SmartColdBox y sprite_animation, el panel lateral decía lo mismo dos veces, en la línea gris «SF 1.1.0 → 1.2.2 · 1/7 Visión» y en el aviso; el propietario de la Software Factory, al ver el arreglo: «mantenla» (161).

**Aplicada en:** `plugins/sf/hooks/panel.tsx` (`lineaEstado` y los avisos) y sus pruebas.

**Línea de estado de la antigua (161):** Estado: deprecada el AAAA-MM-DD por «Que el proyecto va por detrás de la SF lo dice un solo aviso en el panel lateral, y la caja sobre el prompt da las dos versiones» (nueva); lo demás, por «La línea gris del proyecto sale del panel» (166).
{: .nota}

### Las órdenes de una tarea, como etiquetas en el menú de la tarea desplegada (168) {: #t-168}

Las órdenes de cada tarea van como etiquetas con su nombre, con mayúscula inicial y sin negrita, sobre fondo negro, en el menú de la tarea desplegada. La línea plegada no lleva ninguna, solo el ● del subagente. Toda tarea se puede desplegar y lleva la etiqueta «?», que pide a Claude que la explique (173).

Primero van las de la tarea, en verde, y al final la que destruye (Eliminar, Descartar o Revertir), en rojo. Después, las de sus pasos (Separar pasos, Paso +), con la letra atenuada. Las de dos clics confirman en la misma etiqueta: «¿Cerrar? sí». Cada paso pendiente lleva su «×», que confirma con «¿Quitar? sí», y su «?».

Qué órdenes hay y dónde sale cada una lo dice «Cómo funciona el panel», «Las órdenes de una tarea».

Recoge lo que sigue valiendo de «Las órdenes de cada tarea, en un menú de etiquetas» (168), «Toda tarea se despliega y lleva su etiqueta «?»» (173) y «Etiquetas «A Testing» en las tareas en curso y «Cerrar» en las de Testing» (182), que quedan deprecadas.

**Porqué:** el propietario de la Software Factory: «Cada vez hay más letras que memorizar lo que hacen. Lo convertimos en un menú (de etiquetas)» (168). Las letras reservaban ancho en todas las líneas.

**Aplicada en:** `plugins/sf/hooks/panel.tsx` (`etiquetaOrden` y el menú) y `estilo.ts` (`FONDO_ORDEN`, `COLOR_ORDEN_DESTRUCTIVA`), y sus pruebas.

**Línea de estado de la antigua (168):** Estado: deprecada el AAAA-MM-DD por «Las órdenes de una tarea, como etiquetas en el menú de la tarea desplegada» (nueva).
{: .nota}

**Línea de estado de la antigua (173):** Estado: deprecada el AAAA-MM-DD por «Las órdenes de una tarea, como etiquetas en el menú de la tarea desplegada» (nueva).
{: .nota}

**Línea de estado de la antigua (182):** Estado: deprecada el AAAA-MM-DD por «Las órdenes de una tarea, como etiquetas en el menú de la tarea desplegada» (nueva); lo demás, por «Testing pasa a llamarse «En observación»» (212).
{: .nota}

### La SF fija su mecanismo y se adapta al proyecto en el remoto, la rama de publicación, el idioma, los commits y el manifiesto (202) {: #t-202}

La SF fija su mecanismo, que es igual en todos los proyectos: la cola de tareas, una rama `feature/NN-nombre` por tarea desde `develop` (205), el número de la tarea en el commit, el registro de decisiones en `sf/decisiones/` (208) y sus documentos en `sf/` (203).

En lo demás se adapta a lo que el proyecto ya tiene, y lo guarda en `.sf/proyecto.json`: el remoto, la rama de publicación (`rama_main`), el idioma, el formato del commit y el manifiesto con la versión. Los documentos del proyecto no se mapean: si siguen la estructura de la SF, están donde los busca; si no, no los busca (229).

Recoge lo que sigue valiendo de «La SF fija el mecanismo y se adapta a las convenciones del proyecto» (202), que queda deprecada.

**Porqué:** incorporar un proyecto no debe reorganizarlo (201), y dejarlo todo con interruptores no lo cumplía. El propietario de la Software Factory eligió «fija el mecanismo, se adapta en todo lo demás» (202), y después sacó del «todo lo demás» las ramas (205), las decisiones (208) y el mapa de documentos (229).

**Aplicada en:** `plugins/sf/tools/configuracion.py` y `cola.py` (`convenciones`), `plugins/sf/hooks/configuracion.ts` y `contexto.ts` (la línea de convenciones), y sus pruebas; `sf:incorporar_proyecto_a_sf` («Lo fijo, lo que se detecta y lo que se elige») y `sf:configurar_proyecto`.

**Línea de estado de la antigua (202):** Estado: deprecada el AAAA-MM-DD por «La SF fija su mecanismo y se adapta al proyecto en el remoto, la rama de publicación, el idioma, los commits y el manifiesto» (nueva); lo demás, por «El manejo del repositorio no se negocia: siempre develop» (205), «Las decisiones son material de la SF: siempre en sf/decisiones/» (208) y «Sin mapa de documentos: o se sigue la estructura de la SF, o no se mapea» (229).
{: .nota}

### Los documentos de la SF van en la carpeta sf/ y su máquina en .sf/ (203) {: #t-203}

En todo proyecto SF, `.sf/` es la máquina: `proyecto.json`, versionado, y la cola, el estado y el historial, fuera de git. `sf/`, en la raíz y visible, guarda los documentos de la SF: `sf/propuestas.md`, `sf/informes/` y `sf/decisiones/` (208). Sus rutas son fijas (229).

Un proyecto incorporado antes los pasa a `sf/` al ponerse al día, con el OK del propietario; mientras tanto, la SF los sigue leyendo en `docs/`. Es la excepción acordada a «Incorporar un proyecto no mueve ni renombra nada» (201).

Recoge lo que sigue valiendo de «Los documentos de la SF van en la carpeta sf/» (203), que queda deprecada.

**Porqué:** en el `docs/` del proyecto chocaban con los suyos (JKanban lo tiene en inglés, OncoCore usa `_docs/`), y dentro de `.sf/` se esconden: ripgrep se salta las carpetas con punto, Obsidian no las ve y en macOS y Linux no salen en el explorador. El propietario de la Software Factory: «una carpeta sf en la raíz para las cosas de la SF, en todos los proyectos SF, así nos evitamos choques de partida» (203).

**Aplicada en:** `plugins/sf/tools/cola.py` (`PROPUESTAS`, `DECISIONES`), `indice_decisiones.py` y `plugins/sf/hooks/lectura.ts` (`RUTAS_PROPUESTAS`), y sus pruebas; `sf:incorporar_proyecto_a_sf`; `sf:informe_deliberativa` («Dónde va»).

**Línea de estado de la antigua (203):** Estado: deprecada el AAAA-MM-DD por «Los documentos de la SF van en la carpeta sf/ y su máquina en .sf/» (nueva); lo demás, por «Las decisiones son material de la SF: siempre en sf/decisiones/» (208) y «Sin mapa de documentos: o se sigue la estructura de la SF, o no se mapea» (229).
{: .nota}

### La cola por dentro: historial, copias, bloqueo, quién y por dónde, reabrir y subagentes (115; pregunta 1) {: #t-115}

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

**Línea de estado de la antigua (115):** Estado: deprecada el 2026-11-27 por «La cola por dentro: historial, copias, bloqueo, quién y por dónde, reabrir y subagentes» (nueva); lo demás, por «Cerrar exige siempre el paso de cerrar; quitar el de probar es cerrar sin probar» (121), «El paso de prueba es «Activar rama para poder probar»» (172), «Los pasos de cierre, desde que la tarea entra en curso» (174), «Una tarea en curso con rama no vuelve a la cola» (170), «La marca del subagente, verde trabajando y roja en espera» (162), «El tipo de tarea decide cómo se maneja el repositorio» (219), «Los commits los lleva siempre Claude» (225) y «Revertir elimina la tarea o la deja pendiente» (134).
{: .nota}

### Las que se deprecan sin regla vigente nueva {: #t-sin}

**«Marcador del día: terminadas, dejadas y propuestas» (035):** Estado: deprecada el 2026-10-27 por «Fuera el marcador de la última fila» (038).
{: .nota}

**«Lo probado sale de Sin probar» (042):** Estado: deprecada el AAAA-MM-DD por «Una tarea en observación sale solo con el OK del propietario, que se pide tarea a tarea» (372); lo demás, por «Las comprobaciones y pruebas hechas se anotan como pasos de su tarea» (288).
{: .nota}

**«Código de tarea: número y estado, «57-A»» (058):** Estado: deprecada el 2026-11-25 por «El número de una tarea lleva el color de su estado, y una reabierta cuenta como H» (373); lo demás, por «Código de tarea más ligero: 74C» (066).
{: .nota}

**«Cerrar exige siempre el paso de cerrar; quitar el de probar es cerrar sin probar» (121):** Estado: deprecada el 2026-11-01 por «Los pasos de cierre, desde que la tarea entra en curso» (174); lo demás, por «El paso de prueba es «Activar rama para poder probar»» (172).
{: .nota}

**«La mejora desde otro proyecto se escribe con Edit o Write» (192):** Estado: deprecada el 2026-11-01 por «Sin registro ni mejoras de la SF desde otros proyectos» (194).
{: .nota}

**«Botones del panel en la app de escritorio, con contorno de color» (253):** Estado: deprecada el 2026-11-05 por «Botones del panel en la app de escritorio con el fondo de su color» (290).
{: .nota}

:::

## Decidido | Lo que ya está decidido | Decidido {#decidido}

| Nº | Decisión | Qué fija aquí |
| --- | --- | --- |
| 388 | Las decisiones, en un solo formato: regla y porqué | El formato de cada regla vigente nueva y de la línea de estado. |
| 389 | Vigentes y deprecadas, en dos catálogos distintos con un punto de entrada común | Adónde va cada antigua al deprecarla. |
| 390 | La fecha del nombre de archivo de una decisión es la de su registro | La fecha de la regla vigente nueva y de la línea de estado. |

Después del OK, sin otra decisión: las citas por punto de la regla antigua de la cola (115) pasan a su regla vigente nueva; la ayuda de `cola.py paso quitar` nombra los dos pasos de cierre; y un comentario de `cola.py` deja de citar una regla deprecada (121).
{: .nota}
