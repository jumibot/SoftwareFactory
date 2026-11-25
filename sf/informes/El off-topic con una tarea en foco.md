---
antetitulo: SoftwareFactory · Informe de investigación · Noviembre 2026
lema: El foco falla donde la regla calla // y donde otras reglas y el mod piden hablar.
subtitulo: Por qué Claude incumple el off-topic con una tarea en foco, y cómo corregirlo.
version: Versión 1.0 · 25/11/2026
estado: Propuesta · Tarea 431
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de investigación
pie: Informe de la tarea «Que Claude respete siempre el off-topic cuando hay una tarea en foco» (431). Parte de sf:orquestacion y su porque.md, claude-sf.md, flujo_tareas, los avisos del mod en plugins/sf/hooks/, las decisiones del foco y la conversación del 25/11/2026. Espera la decisión del propietario de la Software Factory.
---
# El off-topic con una tarea en foco

## Resumen | Tres causas, y ninguna es un olvido suelto | Resumen {#resumen}

Los dos fallos del 25/11 no salen de una sola regla mal escrita. Salen de tres cosas a la vez. La primera es que la sesión no tenía las reglas del foco vigentes: trabajaba con las de la 1.9.7, y el mod no vuelve a entregar la orquestación al recargar el plugin. La segunda es que la regla del foco no dice qué hacer con lo que el propietario pide y no es del foco: una petición nueva, una pregunta sin tarea o un botón del panel. Y cuando el foco solo espera, se contradice: no deja decir nada del foco, pero exige una respuesta del foco para colgar el off-topic. La tercera es que otras reglas de la skill y los avisos del mod piden contar cosas («avisando en una línea», «decir qué cambió», «antes de contestar») como si no hubiera foco. Los avisos llegan frescos en cada turno; la regla del foco se entregó una vez, al principio.

La propuesta es una regla de precedencia («con foco, todo lo que no es de su tarea va como off-topic, lo pida quien lo pida»), qué cuenta como «otra tarea» caso por caso y seis ejemplos cortos en la skill. Además, que el mod deje de empujar hacia el cuerpo de la respuesta: avisos que lo dicen, un recordatorio breve cuando trae cosas de otras tareas y volver a entregar la orquestación cuando cambia.

<figure class="vertical">
<svg viewBox="0 0 560 420" width="100%" role="img" aria-label="Lo que pesa en cada respuesta: la regla del foco llega una vez al empezar la sesión, y en cada turno llegan el mensaje del propietario, los avisos del mod, los informes de subagentes y los recordatorios de Claude Code; la respuesta con foco tiene tres partes: la línea del foco, lo del foco y los off-topic" style="font-family:var(--fuente-texto);display:block">
<rect x="10" y="10" width="540" height="66" rx="8" fill="none" stroke="var(--texto-suave)" stroke-dasharray="6 5" stroke-width="1.5"/>
<text x="26" y="38" font-size="18" font-weight="600" fill="var(--texto-suave)">Regla del foco, una vez</text>
<text x="26" y="62" font-size="15" fill="var(--texto-suave)">al empezar la sesión: la de la 1.9.7</text>
<path d="M425 76 V 112" stroke="var(--texto-suave)" stroke-dasharray="5 4" stroke-width="1.5" fill="none"/>
<path d="M419 104 L425 114 L431 104" stroke="var(--texto-suave)" stroke-width="1.5" fill="none"/>
<text x="10" y="104" font-size="15" fill="var(--texto-suave)">Cada turno, fresco:</text>
<rect x="10" y="118" width="250" height="58" rx="8" fill="var(--fondo)" stroke="var(--primario)" stroke-width="1.5"/>
<text x="24" y="143" font-size="15" font-weight="600" fill="var(--texto)">Mensaje del propietario</text>
<text x="24" y="165" font-size="15" fill="var(--texto-suave)">petición, pregunta, botón</text>
<rect x="10" y="186" width="250" height="58" rx="8" fill="var(--fondo)" stroke="var(--primario)" stroke-width="1.5"/>
<text x="24" y="211" font-size="15" font-weight="600" fill="var(--texto)">Avisos del mod</text>
<text x="24" y="233" font-size="15" fill="var(--texto-suave)">«ANTES DE NADA…»</text>
<rect x="10" y="254" width="250" height="58" rx="8" fill="var(--fondo)" stroke="var(--primario)" stroke-width="1.5"/>
<text x="24" y="279" font-size="15" font-weight="600" fill="var(--texto)">Informes de subagentes</text>
<text x="24" y="301" font-size="15" fill="var(--texto-suave)">y sus notificaciones</text>
<rect x="10" y="322" width="250" height="58" rx="8" fill="var(--fondo)" stroke="var(--primario)" stroke-width="1.5"/>
<text x="24" y="347" font-size="15" font-weight="600" fill="var(--texto)">Claude Code</text>
<text x="24" y="369" font-size="15" fill="var(--texto-suave)">«di qué estás haciendo»</text>
<path d="M260 147 H 280 M260 215 H 280 M260 283 H 280 M260 351 H 280 M280 147 V 351 M280 249 H 298" stroke="var(--primario)" stroke-width="1.5" fill="none"/>
<path d="M290 243 L300 249 L290 255" stroke="var(--primario)" stroke-width="1.5" fill="none"/>
<rect x="300" y="118" width="250" height="262" rx="8" fill="none" stroke="var(--oscuro)" stroke-width="2"/>
<text x="316" y="146" font-size="18" font-weight="600" fill="var(--oscuro)">Respuesta con foco</text>
<rect x="314" y="160" width="222" height="56" rx="6" fill="var(--fondo)" stroke="var(--linea)"/>
<text x="326" y="184" font-size="15" font-weight="600" fill="var(--texto)">1 · Línea del foco</text>
<text x="326" y="205" font-size="15" fill="var(--texto-suave)">una sola tarea</text>
<rect x="314" y="226" width="222" height="56" rx="6" fill="var(--fondo)" stroke="var(--linea)"/>
<text x="326" y="250" font-size="15" font-weight="600" fill="var(--texto)">2 · Lo del foco</text>
<text x="326" y="271" font-size="15" fill="var(--texto-suave)">¿y si no hay nada?</text>
<rect x="314" y="292" width="222" height="72" rx="6" fill="var(--fondo)" stroke="var(--linea)"/>
<text x="326" y="316" font-size="15" font-weight="600" fill="var(--texto)">3 · Off-topic al final</text>
<text x="326" y="337" font-size="15" fill="var(--texto-suave)">una por tarea, breve;</text>
<text x="326" y="356" font-size="15" fill="var(--texto-suave)">nunca en el cuerpo</text>
<text x="10" y="408" font-size="15" fill="var(--texto-suave)">Lo fresco empuja a contar en el cuerpo; la regla queda lejos.</text>
</svg>
<figcaption>La regla del foco llega una vez; lo que empuja a contar otras tareas en el cuerpo llega en cada turno.</figcaption>
</figure>

Quedan once preguntas: ocho sobre la regla y tres sobre el mod. Salen dos tareas de implementar, un paso para una tarea en cola afín, una tarea de documentar y pasos para «Actualizar Cómo funciona la Software Factory» (313), con su texto propuesto.

[Ver las once preguntas](#por-decidir){: .salto} [Ver el texto propuesto para la skill](#anexo-texto){: .salto}

## Los fallos | Qué tenía Claude delante en cada uno | Los fallos {#fallos}

Los dos fallos son de la misma conversación de la SF. Entre uno y otro, `/reload-plugins` cargó el mod 1.9.8, pero los dos se dieron con la orquestación de la 1.9.7 en el contexto. Esa versión ya decía que anotar otra tarea no cambia el foco y que lo de otras tareas va al final. Le faltaba lo que añadió la tarea «Afinar las reglas del foco con el uso» (417): «Solo el propietario mueve el foco», «también cuando el propietario pregunta por otra tarea» y «nunca en el cuerpo». Esa tarea se cerró a las 11:09 y la 1.9.8 se publicó a las 11:16; la sesión había recibido la orquestación a las 11:07. Aun así, el primer fallo incumple una regla que ya tenía, y el segundo cae en un caso que ninguna versión cubre.

::: tarjetas 2

### 1 · El bug del panel, en el cuerpo {color=frambuesa icono=aviso}

Foco
:   «SF como un proyecto más» (379), esperando el OK del propietario a un texto del CLAUDE.md.

Llegó al turno
:   Un mensaje que era entero de otra cosa: «hay un bug en desktop con el scroll», con un clip. Antes, el aviso «Subagentes: el subagente de la 379 ha terminado: recógelo», el informe de ese subagente y su notificación. Durante el turno, el recordatorio de Claude Code «say in a few words what you're doing».

Respuesta
:   Línea del foco de la 379; dos párrafos con el bug anotado como la 429 y su causa probable; al final, la pregunta pendiente de la 379 cerrada con «⭐❓».

Incumple
:   Lo de otra tarea, al final y breve (ya en la 1.9.7); dos emojis seguidos (ya en la 1.9.7). Además, Claude extrajo fotogramas del clip y los analizó en el principal, con la 429 en cola y sin subagente.

### 2 · Una pregunta sin tarea, bajo el foco {color=naranja icono=dialogo}

Foco
:   «Botones del panel más pequeños» (397), esperando a que su subagente integre `develop`.

Llegó al turno
:   Una pregunta general: por qué unos subagentes no muestran su número de tarea en la lista de Claude Code. Con ella, por segunda vez, «ANTES DE NADA, en este turno y antes de contestar: lanza el subagente de […] la 429», aunque el propietario había dicho «si esperamos» un turno antes.

Respuesta
:   Línea del foco de la 397; la respuesta a la pregunta; y en el cuerpo, «La 429 sigue esperando a que se cierre la 397 […] Por eso no lanzo su subagente, aunque el mod lo pida».

Incumple
:   Lo de la 429 en el cuerpo. La línea del foco encabeza algo que no es de la 397: la regla dice «primera línea de cada respuesta» y no tiene caso para una pregunta sin tarea. Y le habla al propietario de un aviso que él no ve.

:::

No son casos sueltos. De las 47 respuestas con línea del foco de esa conversación, al menos siete llevan otra tarea en el cuerpo:

| Momento | Foco | En el cuerpo | Qué la empujó |
| --- | --- | --- | --- |
| Tras un informe | Listas para probar en verde (383) | La 397, lista para probar, con sus pasos de prueba | «Si el foco espera… el foco pasa a la propuesta» (1.9.7) |
| Bug del clip | SF como un proyecto más (379) | La 429 anotada y su causa | Mensaje entero sobre otra cosa |
| Tras «adelante» | SF como un proyecto más (379) | La 430 anotada | «Al acabar un trabajo, decir qué cambió» |
| Esperando | Botones del panel más pequeños (397) | «Luego la cierro y lanzo la 429» | Aviso «ANTES DE NADA… lanza» |
| Pregunta general | Botones del panel más pequeños (397) | La 429 y el aviso del mod | Aviso repetido y sin caso para la pregunta |
| Tras cerrar la 397 | Scroll del panel en la app (429) | La 397 cerrada y cómo probarla | Encargo del panel «dime en una línea» |
| Tras la queja | Scroll del panel en la app (429) | La 431 anotada | Mensaje entero sobre otra cosa |

La línea del foco también se movió sola: a la 429 cuando el propietario la puso en curso desde el panel, de vuelta a la 397 un turno después, y a la 431 con «ponla en curso». La 1.9.8 dice que poner en curso no mueve el foco, pero no dice si un botón del panel o una orden expresa sobre otra tarea cuentan como «instrucción expresa».

## Causas | Trece causas, cada una con su cita | Causas {#causas}

Las causas se agrupan en cuatro clases, con un color cada una en las tarjetas: entrega (verde), instrucción poco concreta (turquesa), inconsistencia entre partes (naranja) y contradicción (frambuesa). Las citas son de `plugins/sf/skills/orquestacion/SKILL.md` en `develop`, salvo que digan otra cosa. Las más graves son las contradicciones: obligan a incumplir una regla para cumplir otra, y Claude resuelve el choque contando las cosas en el cuerpo.

### Entrega: la regla no estaba, o estaba lejos {#causas-entrega}

::: tarjetas 2 plegables

#### C1 · La sesión no tenía las reglas vigentes {color=verde icono=documento} {: #c1}

Dónde
:   `plugins/sf/hooks/contexto.ts`, `FUENTES_REGLAS = new Set(['startup', 'clear', 'compact'])`.

Cómo pesó
:   La orquestación solo se entrega al empezar, tras `/clear` y tras compactar. `/reload-plugins` carga el mod nuevo, pero no la skill nueva: la sesión siguió con la 1.9.7 aunque la 1.9.8 ya estaba publicada e instalada.

Corrección
:   [Pregunta 11](#p11).

#### C2 · Una vez al principio frente a avisos en cada turno {color=verde icono=documento} {: #c2}

Dónde
:   La regla entra una vez en el contexto de SessionStart; los avisos del mod, en cada mensaje (`register.tsx`, `prompt.submit`), y el de lanzar va el primero.

Cómo pesó
:   En la conversación, el primer fallo llegó unas 1.250 entradas después de la entrega. En cambio, el aviso imperativo estaba justo encima del mensaje. Lo reciente y lo imperativo pesan más que una regla lejana.

Corrección
:   [Pregunta 10](#p10).

:::

### Instrucciones poco concretas {#causas-concretas}

::: tarjetas 2 plegables

#### C3 · Qué es «lo de otra tarea» {color=turquesa icono=lupa} {: #c3}

Cita
:   «Todo lo de otra tarea lleva la etiqueta […]: también propuestas y preguntas […]. También cuando el propietario pregunta por otra tarea» (línea 26).

Qué falta
:   No nombra la petición o el bug que llegan (no son tarea hasta anotarlos), lo que el propietario encarga de otra tarea («ponla en curso»), los encargos del panel ni los avisos del mod. Solo habla de «preguntas» del propietario.

Corrección
:   [Pregunta 2](#p2).

#### C4 · Una pregunta sin tarea {color=turquesa icono=lupa} {: #c4}

Cita
:   «FOCUS, primera línea de cada respuesta […]. Sin foco, la línea no va» (línea 109).

Qué falta
:   Con foco, toda respuesta lleva la línea, también la que contesta una duda general o de Claude Code. Ninguna regla dice si esa respuesta es del foco, off-topic o de nadie. Es el segundo fallo.

Corrección
:   [Pregunta 3](#p3).

#### C5 · Qué mueve el foco {color=turquesa icono=lupa} {: #c5}

Cita
:   «la que dice el propietario […] o, si no, sobre la que más escribe» (línea 23) y «sin su instrucción expresa» (línea 25).

Qué falta
:   «Sobre la que más escribe» invita a seguir al propietario cuando habla de otra tarea, y la 337 lo prohíbe. Tampoco dice si un botón del panel (en curso, Cerrar, Activar rama), que llega como mensaje suyo, es una instrucción expresa. En la sesión, el foco saltó tres veces sin que él lo pidiera.

Corrección
:   [Pregunta 5](#p5).

#### C6 · Qué es «libre» {color=turquesa icono=lupa} {: #c6}

Cita
:   «Al acabar el turno: lanzar lo que se pueda y, libre, desbloquear» (línea 21) y la sección «Libre»: «Preguntar al propietario lo que esperan de él las tareas en curso» (línea 98).

Qué falta
:   No dice si «libre» es «sin foco». Leído como «sin trabajo en este turno», manda preguntar por otras tareas al final de cada turno.

Corrección
:   [Pregunta 1](#p1).

:::

### Inconsistencias entre partes {#causas-inconsistencias}

::: tarjetas 2 plegables

#### C7 · Reglas que piden contar, sin la excepción del foco {color=naranja icono=rama} {: #c7}

Citas
:   «avisando en una línea» al lanzar (línea 61); «avisando con los pasos en pocas líneas» al poner en curso (línea 47); «llevar al propietario lo que pide» al volver un subagente (línea 66); «Al acabar un trabajo, decir qué cambió, qué se comprobó y qué queda pendiente» (línea 79); «Cerrar antes que abrir […] llevando al propietario lo que necesitan» (línea 41); «Guiar […] sugerir cómo avanzar mejor: en una línea» (línea 35).

Cómo pesó
:   Cada regla está escrita como si no hubiera foco, y solo la sección del foco dice que, con él, todo eso va al final. Al aplicar una de ellas, Claude cuenta lo hecho en el cuerpo y con detalle.

Corrección
:   [Pregunta 1](#p1).

#### C8 · Silencio u off-topic en el mismo párrafo {color=naranja icono=rama} {: #c8}

Cita
:   «Con foco, sobre todo mientras prueba, nada de otras tareas: ni preguntas, ni menús, ni informes de subagentes, listas o avisos» (línea 23), y justo debajo, lo de otras tareas «va al final de una respuesta del foco» (línea 26).

Cómo pesó
:   Son dos regímenes de dos decisiones: el silencio de «No interrumpir mientras se prueba o se está en otra tarea» (250) y el off-topic de la 287. Se leen como dos reglas distintas, y ninguna dice cuál vale.

Corrección
:   [Pregunta 1](#p1), con el texto del [anexo](#anexo-texto).

#### C9 · Decisiones y versiones que no dicen lo mismo {color=naranja icono=rama} {: #c9}

Citas
:   La decisión 287: «el foco pasa a la propuesta»; la 337: «Claude no cambia de tarea ni mueve el foco a otra, salvo instrucción expresa». La 1.9.7 de la skill aún decía «el foco pasa a la propuesta».

Cómo pesó
:   Con la 1.9.7, proponer probar otra tarea en el cuerpo era casi lo que mandaba la regla: es el caso de la 397 bajo el foco de la 383. La 1.9.8 lo arregló en la skill, pero la 287 no dice que la 337 la corrige.

Corrección
:   Una línea en el `porque.md` (tarea [«Que la regla del foco diga qué hacer en cada caso»](#a-reglas)).

:::

### Contradicciones {#causas-contradicciones}

::: tarjetas 2 plegables

#### C10 · El foco que espera no deja decir nada {color=frambuesa icono=aviso} {: #c10}

Citas
:   «si solo espera a su subagente, no se le cuenta que sigue trabajando» (línea 29); «Un off-topic sin respuesta del foco, solo si la tarea del foco ha terminado o lleva un rato sin actividad» (línea 26); «Tras ella, primero lo del foco» (línea 109).

El choque
:   Si el foco espera a su subagente y llega algo de otra tarea, no se puede decir nada del foco, y el off-topic necesita una respuesta del foco. Hay que incumplir una de las tres reglas. Claude llenó el hueco con lo de la otra tarea, o con «Sigo esperando a que el subagente de la 397 termine», que incumple la primera.

Corrección
:   [Pregunta 4](#p4).

#### C11 · El menú al anotar frente a los menús con foco {color=frambuesa icono=aviso} {: #c11}

Citas
:   «Del proyecto: a la cola, con el menú» (línea 18) y «Menú al anotar» (línea 33), frente a «Con foco, solo de la tarea del foco; lo demás, off-topic» (línea 27).

El choque
:   Ninguna dice cuál manda ni cómo se pregunta entonces si va en curso, en cola o como paso. Claude la dejó en cola sin preguntar y contó la anotación en el cuerpo.

Corrección
:   [Pregunta 6](#p6).

#### C12 · Los avisos del mod frente a lo decidido con el propietario {color=frambuesa icono=aviso} {: #c12}

Citas
:   «ANTES DE NADA, en este turno y antes de contestar: lanza el subagente de cada tarea en curso que no lo tiene» (`subagentes.ts`, línea 69); la skill lo repite: «lanzar los que faltan es lo primero del turno, antes de contestar» (línea 62). Frente a «Una tarea en curso que tiene que esperar […] su subagente no trabaja hasta que se cumpla» (línea 56) y los choques: «recomendar esperar o fusionar y seguir solo con el OK» (línea 44).

El choque
:   El propietario eligió esperar; el mod no mira el paso «Esperar a …» y repitió la orden en cada mensaje. Para incumplirla, Claude se justificó ante el propietario en el cuerpo («aunque el mod lo pida»). Además, el aviso, el arranque («Al acabar, di en una línea qué has lanzado o recogido», línea 144) y el encargo del panel al poner en curso («dime en una línea qué va a hacer», `cola.ts`, línea 321) piden contarlo sin decir dónde.

Corrección
:   [Pregunta 9](#p9).

#### C13 · ⭐ y ❓ quieren el mismo sitio {color=frambuesa icono=aviso} {: #c13}

Citas
:   «⭐, al final de la línea de la opción recomendada […] también cuando las opciones se explican en el chat»; «❓ […] en lugar del signo de cierre»; «Nunca dos emojis seguidos» (línea 117). Y las preguntas en el chat, en un bloque `diff` cuyas líneas van «sin emojis», salvo ❓ (línea 118).

El choque
:   Una pregunta que nombra la opción recomendada acaba con las dos: «el recomendado ⭐❓». Dentro del bloque `diff`, la ⭐ ni siquiera cabe.

Corrección
:   [Pregunta 7](#p7).

:::

Queda una presión que no es de la SF: Claude Code inserta en turnos largos «The user hasn't heard from you in a while — say in a few words what you're doing», y los informes y notificaciones de los subagentes llegan como mensajes. Todo empuja a narrar en el cuerpo. No se puede cambiar, pero la regla de precedencia lo cubre: lo que se cuenta de otra tarea mientras se trabaja también va como off-topic.

Fuera del foco, dos detalles sueltos. La línea 11 de la skill dice que en la propia SF el mod no la entrega («Si no ha llegado (en la propia SF, …)»), pero desde «Las reglas y la orquestación también en la SF» (298) sí la entrega. Y los ejemplos del README (`FOCUS … (T 47)`, `(off-topic T 48: …)`) siguen con el formato de antes de la 417. `claude-sf.md` y `flujo_tareas` no hablan del foco: no contradicen nada.

## Cómo corregirlo | Cuatro vías, juntas | Cómo corregirlo {#propuesta}

Se recomienda combinar las cuatro vías, porque cada una ataca una causa distinta. Reescribir la regla y quitar las contradicciones resuelve lo que hoy obliga a elegir qué regla incumplir. Los ejemplos fijan la forma, que es lo que el modelo imita. El mod corrige lo que empuja en cada turno y lo que no llega.

| Vía | Ataca | A favor | En contra |
| --- | --- | --- | --- |
| Reescribir la regla: precedencia, casos, qué mueve el foco | C3 a C8, C10, C11 | Una frase cubre las reglas de hoy y las que vengan; los casos dudosos quedan resueltos por escrito | Más texto en una skill que ya ocupa unos 4.000 tokens en cada sesión |
| Quitar contradicciones: foco que espera, menú al anotar, emojis, avisos | C10 a C13 | Sin ellas, cumplir una regla no obliga a romper otra | Toca la skill y el mod a la vez |
| Ejemplos concretos en la skill | Todas las de forma | El modelo imita la forma mejor que una descripción; seis casos ocupan unas 15 líneas | Si no cubren un caso, Claude puede tomar el ejemplo más parecido como regla |
| Que el mod lo refuerce | C1, C2, C12 | Llega en el turno en que hace falta, como los avisos que hoy empujan en contra | El mod no sabe el foco (328): solo puede recordar la regla, no aplicarla |

> **Propuesta**
> Una regla de precedencia al principio de «Con cada mensaje», la sección del foco reescrita con sus casos y seis ejemplos (texto en el [anexo](#anexo-texto)). Avisos del mod que dicen «cuéntalo como off-topic» y no piden lanzar el subagente de una tarea que espera, un recordatorio de una línea cuando traen cosas de otras tareas, y la orquestación entregada de nuevo cuando cambia en la sesión.

No se propone que el mod compruebe la respuesta después de escrita (leer la línea del foco y buscar otros números de tarea en el cuerpo): no se ha comprobado que el mod pueda leer la respuesta al acabar el turno, y solo avisaría en el turno siguiente. Queda como idea si lo demás no basta.

## Por decidir | Once preguntas, en dos bloques | Por decidir {#por-decidir}

Las preguntas van numeradas por importancia y partidas en dos bloques: ocho sobre la regla, que irían a una tarea sobre la skill, y tres sobre el mod, que irían a código. Cada bloque abre con un salto a su separación.

| Nº | Pregunta | Recomendada |
| --- | --- | --- |
| [1](#p1) | Precedencia del foco sobre las demás reglas | A: una frase al principio de «Con cada mensaje» |
| [2](#p2) | Qué cuenta como «lo de otra tarea» | A: todo lo que no avanza el foco, también lo que él pide |
| [3](#p3) | Una pregunta sin tarea | A: sin línea del foco |
| [4](#p4) | Qué dice lo del foco cuando no hay nada nuevo | C: lo pendiente del propietario, o la línea sola |
| [5](#p5) | Qué mueve el foco | A: solo sus palabras o Activar rama |
| [6](#p6) | El menú al anotar con foco | A: sin menú; la pregunta, en el off-topic |
| [7](#p7) | ⭐ y ❓ en la misma pregunta | A: ⭐ tras la opción, ❓ al final |
| [8](#p8) | Ejemplos en la skill | A: seis casos, junto a la regla |
| [9](#p9) | Avisos del mod que piden actuar | A: dicen dónde contarlo y respetan «Esperar a …» |
| [10](#p10) | Recordatorio del mod | B: solo cuando trae cosas de otras tareas |
| [11](#p11) | La orquestación nueva en la sesión | A: se entrega de nuevo con el siguiente mensaje |

## Por decidir: la regla | Ocho preguntas sobre sf:orquestacion | La regla {#por-decidir-regla}

Lo que se decida aquí va a la tarea que reescribe la regla del foco en la skill y su `porque.md`.

[Ver su separación](#a-reglas){: .salto}

::: preguntas 2 plegables

### 1 · Precedencia del foco sobre las demás reglas {recomendada=A} {: #p1}

Hoy, solo la sección del foco dice que lo de otras tareas va al final; las reglas que piden contar algo no lo recuerdan ([C6](#c6), [C7](#c7), [C8](#c8)).

Opción A
:   Una frase al principio de «Con cada mensaje»: con foco, todo lo que no es de su tarea va como off-topic, lo pida una regla de esta skill, el mod, un subagente o el propietario. La sección del foco pasa a ser la primera, y «nada de otras tareas» se cambia por «nada de otras tareas en el cuerpo». «Libre» queda definido como «sin foco».

Opción B
:   La misma frase, pero dentro de la sección del foco, donde está hoy.

Opción C
:   Una coletilla «(con foco, como off-topic)» en cada regla que pide contar algo.

Recomendación
:   **A.** Una sola frase, lo primero que se lee en cada mensaje, cubre las reglas de hoy y las que vengan; la C se olvida en la próxima regla nueva.

### 2 · Qué cuenta como «lo de otra tarea» {recomendada=A} {: #p2}

La regla de hoy solo nombra las propuestas, las preguntas y las preguntas del propietario sobre otra tarea ([C3](#c3)).

Opción A
:   Todo lo que no hace avanzar la tarea del foco: una petición o un bug nuevos (también al anotarlos), lo que el propietario pregunta o encarga de otra tarea, los encargos del panel y los avisos del mod sobre otra, y los informes de sus subagentes. Lo que él pidió va en su off-topic, con el detalle que haya pedido.

Opción B
:   Como la A, pero lo que el propietario pide directamente de otra tarea se contesta en el cuerpo, bajo la línea del foco.

Opción C
:   Como hoy.

Recomendación
:   **A.** Sigue lo que el propietario ya pidió para las preguntas sobre otra tarea, y no deja huecos que Claude rellene con el cuerpo.

### 3 · Una pregunta sin tarea {recomendada=A} {: #p3}

Una duda general, sobre Claude Code o sobre cómo funciona algo, no es de ninguna tarea ([C4](#c4)).

Opción A
:   Se responde sin línea del foco, y nada más. El foco vuelve en la respuesta siguiente. Si la pregunta destapa una petición o un bug, se anota y va como off-topic, con la línea del foco.

Opción B
:   Línea del foco, lo del foco si lo hay, y la respuesta al final con su propia etiqueta en versalitas, «ꜱɪɴ ᴛᴀʀᴇᴀ».

Opción C
:   Línea del foco y la respuesta en el cuerpo, como en el segundo fallo.

Recomendación
:   **A.** La falta de la línea dice, sin más, que esa respuesta no es del foco; es la que el propio Claude propuso al reconocer el fallo.

### 4 · Qué dice lo del foco cuando no hay nada nuevo {recomendada=C} {: #p4}

Si el foco solo espera a su subagente, hoy no se puede decir nada de él, y el off-topic necesita una respuesta del foco ([C10](#c10)).

Opción A
:   La línea del foco basta: puede ir sola, seguida de los off-topic.

Opción B
:   Una línea fija con su estado («Esperando a su subagente»), aunque hoy «no se le cuenta que sigue trabajando».

Opción C
:   Si el foco espera algo del propietario, esa pregunta en una línea, como en la corrección del primer fallo; si no, la A.

Recomendación
:   **C.** Recuerda lo único útil del foco y, cuando no hay nada, no obliga a inventar una frase.

### 5 · Qué mueve el foco {recomendada=A} {: #p5}

Hoy no se sabe si un botón del panel u «ponla en curso» son una instrucción expresa, y «sobre la que más escribe» choca con la 337 ([C5](#c5)).

Opción A
:   Solo lo que el propietario dice con palabras («vamos con la …», «cambia el foco») y pulsar Activar rama en otra tarea, que es ponerse a probarla. Poner en curso, Cerrar, Descartar, anotar, lanzar o preguntar por otra no lo mueven. «Sobre la que más escribe» solo sirve para fijarlo cuando no hay ninguno.

Opción B
:   También cualquier encargo suyo sobre otra tarea, desde el chat o el panel: el foco sigue lo último que pidió.

Opción C
:   Como hoy.

Recomendación
:   **A.** Deja una lista cerrada de lo que mueve el foco y acaba con los saltos sin pedirlos; Activar rama es su forma de decir «vamos a probar la …».

### 6 · El menú al anotar con foco {recomendada=A} {: #p6}

«Menú al anotar» y «con foco, solo menús de su tarea» no dicen cuál manda ([C11](#c11)).

Opción A
:   Con foco, sin menú: se anota en cola, o como paso si encaja claramente en una tarea, y la pregunta va en su off-topic, en una línea: «(`ᴏꜰꜰ-ᴛᴏᴘɪᴄ` T❹ ❷ ❾ : anotada en cola; ¿la pongo en curso❓)».

Opción B
:   El menú se abre igual: anotar es del momento.

Opción C
:   En cola sin preguntar; el menú, al terminar el foco.

Recomendación
:   **A.** Anota sin cortar y deja la elección a mano, sin otro menú encima del foco.

### 7 · ⭐ y ❓ en la misma pregunta {recomendada=A} {: #p7}

Una pregunta que nombra la opción recomendada acaba con «⭐❓», y en el bloque `diff` la ⭐ no cabe ([C13](#c13)).

Opción A
:   ⭐ detrás del nombre de la opción y ❓ al final: «¿Le doy el OK al texto recomendado ⭐ de la línea del CLAUDE.md❓». En el bloque `diff`, también la ⭐, como excepción igual que la ❓.

Opción B
:   Con ❓ al final y sin ⭐: la recomendación, con palabras.

Recomendación
:   **A.** Es la forma que el propio Claude usó al corregirse, y conserva las dos marcas que el propietario quiere ver.

### 8 · Ejemplos en la skill {recomendada=A} {: #p8}

La regla describe la forma, pero no la enseña.

Opción A
:   Seis casos cortos junto a la regla, cada uno con su respuesta en una a tres líneas: petición nueva, pregunta sin tarea, foco que espera e informe de otra, aviso «ANTES DE NADA», encargo de otra tarea y pregunta con opción recomendada. Unas 15 líneas.

Opción B
:   Los mismos casos en `references/`, para leer si hace falta.

Opción C
:   Sin ejemplos.

Recomendación
:   **A.** El modelo imita ejemplos mejor que reglas, y en `references/` no se leerían en el momento del fallo.

:::

## Por decidir: el mod | Tres preguntas sobre los avisos y la entrega | El mod {#por-decidir-mod}

Lo que se decida aquí va a código: una tarea nueva para los avisos y el recordatorio, y un paso de una tarea en cola para volver a entregar la orquestación.

[Ver sus separaciones](#a-mod){: .salto}

::: preguntas 2 plegables

### 9 · Avisos del mod que piden actuar {recomendada=A} {: #p9}

«ANTES DE NADA… antes de contestar», el arranque y el encargo de poner en curso piden actuar y contarlo sin decir dónde, y el de lanzar no ve el paso «Esperar a …» ([C12](#c12)).

Opción A
:   Los textos cambian: «hazlo antes de contestar; con foco, cuéntalo solo como off-topic al final». El aviso de lanzar se salta la tarea cuyo siguiente paso pendiente es «Esperar a …», y la skill dice que esa tarea puede quedar sin subagente hasta que se cumpla.

Opción B
:   Solo la regla de precedencia de la [pregunta 1](#p1); los avisos, como hoy.

Opción C
:   La A sin saltarse las tareas que esperan: se lanza el subagente y él espera.

Recomendación
:   **A.** Quita la orden que obligaba a desobedecer al mod y le dice a Claude dónde va lo que hace por él.

### 10 · Recordatorio del mod {recomendada=B} {: #p10}

El mod no sabe el foco (328), pero puede recordar la regla en el turno en que más falla ([C2](#c2)).

Opción A
:   Sin recordatorio, como hoy.

Opción B
:   Una línea solo en los mensajes en que el mod ya trae algo de otras tareas (avisos de subagentes, «Desde el panel», encargos del panel, la notificación de un subagente): «Con foco, lo de otras tareas va al final, como (`ᴏꜰꜰ-ᴛᴏᴘɪᴄ` T… : …)».

Opción C
:   La misma línea en cada mensaje del propietario.

Recomendación
:   **B.** Llega justo cuando el aviso empuja en contra y no añade ruido en los demás turnos.

### 11 · La orquestación nueva en la sesión {recomendada=A} {: #p11}

Hoy, una regla nueva no llega a una sesión abierta hasta `/clear` o una compactación ([C1](#c1)).

Opción A
:   Cuando `/reload-plugins` o REFRESCAR cargan una versión cuya orquestación es distinta de la entregada, el mod la entrega de nuevo con el siguiente mensaje del propietario, una vez.

Opción B
:   Solo un aviso: «La orquestación ha cambiado: haz /clear o compacta para tenerla».

Opción C
:   Como hoy.

Recomendación
:   **A.** Pasa pocas veces y cuesta unos 4.000 tokens cada vez; en la SF, que cambia sus reglas a diario, es justo cuando más falta hace.

:::

## Separar | Tres destinos para aplicar lo que se decida | Separar {#separar}

Esta tarea solo escribe su informe: lo que se decida lo aplican tareas con rama. Las preguntas se separan cuando el propietario las responda o, si lo prefiere, ya, para decidirlas dentro de cada tarea.

::: tarjetas 3

### Regla del foco {color=turquesa icono=codigo} {: #a-reglas}

Se lleva
:   Las preguntas [1](#p1) a [8](#p8).

Adónde
:   Una tarea nueva, «Que la regla del foco diga qué hacer en cada caso», sobre `sf:orquestacion` y su `porque.md`.

También
:   La línea 11 de la skill («en la propia SF»), de [C9](#c9) la nota de que la 337 corrige la 287, y el texto del [anexo](#anexo-texto).

### Avisos del mod {color=naranja icono=codigo} {: #a-mod}

Se lleva
:   Las preguntas [9](#p9) y [10](#p10).

Adónde
:   Una tarea nueva, «Que los avisos del mod respeten el foco», sobre `subagentes.ts`, `cola.ts` y `register.tsx`.

También
:   El paso «Reflejar …» en «Actualizar Cómo funciona la Software Factory» (313).

### Entrega de la orquestación {color=verde icono=codigo} {: #a-entrega}

Se lleva
:   La pregunta [11](#p11).

Adónde
:   Un paso de «Que al actualizar el plugin se refresque solo, sin tener que pedirlo» (378), en cola y afín: refrescar el plugin y que la sesión reciba sus reglas nuevas son lo mismo visto desde Claude. Sobre `contexto.ts` y `register.tsx`.

También
:   El paso «Reflejar …» en «Actualizar Cómo funciona la Software Factory» (313).

:::

## Tareas | Las que salen | Tareas {#tareas}

| Tarea | Tipo | Qué hace |
| --- | --- | --- |
| Que la regla del foco diga qué hacer en cada caso | implementar | Reescribe la sección del foco con su precedencia, sus casos y seis ejemplos, y quita los choques con el menú al anotar y los emojis. |
| Que los avisos del mod respeten el foco | implementar | Cambia los textos de los avisos y encargos, salta las tareas que esperan y añade el recordatorio cuando hace falta. |
| Que al actualizar el plugin se refresque solo, sin tener que pedirlo (378) | implementar | Ya en cola; recibe el paso de volver a entregar la orquestación cuando cambia en la sesión. |
| Poner al día el ejemplo del foco en los README y la web | documentar | Cambia `FOCUS … (T 47)` y `(off-topic T 48: …)` por el formato de hoy en `README.md`, `README.es.md` y `site/index.html`. |
| Actualizar Cómo funciona la Software Factory (313) | documentar | Ya en cola; recibe un paso «Reflejar …» por cada tarea del mod y el arreglo de la ficha de la orquestación (texto en el anexo). |

## Anexo: texto propuesto para la skill | La sección del foco, reescrita | Texto para la skill {#anexo-texto}

Es el texto con las respuestas recomendadas. Sustituiría a «El foco del propietario y no interrumpirle» y sus viñetas (líneas 23 a 29) y subiría al principio de «Con cada mensaje». Las demás viñetas («Tras un rato sin escribir», «Si el foco espera») se quedan como están.

```text
**El foco manda** (287, 250, 337): con foco, todo lo que no es de su tarea va al final como off-topic, nunca en el cuerpo, lo pida una regla de esta skill (avisar al lanzar, llevar lo que pide un subagente, decir qué cambió, cerrar antes que abrir, guiar), el mod, un subagente, Claude Code o el propietario. «Libre» es sin foco.

- **El foco** es una sola tarea, nunca un grupo. Lo fija el propietario: lo dice («vamos a probar la …») o pulsa Activar rama en ella; sin foco, es sobre la que más escribe. Acaba al cerrarse la tarea o cuando él la deja: lo dice, o lleva un rato sin hablar de ella. Nada más lo mueve: ni anotar, poner en curso, cerrar o lanzar otra, ni otro botón del panel, ni que pregunte por otra.
- **Lo de otra tarea:** una petición o un bug nuevos, también al anotarlos; lo que el propietario pregunta o encarga de otra tarea; lo que traen de otra el panel, el mod o un subagente; las propuestas y preguntas de otra.
- **La respuesta con foco**, en este orden: la línea 🅵🅾🅲🆄🆂; lo del foco (sin nada nuevo, lo que espera del propietario en una línea, o nada: la línea basta); un «(`ᴏꜰꜰ-ᴛᴏᴘɪᴄ` T❸ ❾ ❷ : …)» por tarea, con lo hecho y el detalle que él haya pedido.
- **Una pregunta sin tarea** (una duda general, de Claude Code): sin línea del foco; se responde y nada más. Si destapa una petición o un bug, se anota y va como off-topic.
- **Menús** (333): nunca con texto a medio escribir en la caja del prompt (el mod lo bloquea). Con foco, solo de su tarea. Al anotar con foco, sin menú: en cola, o como paso si encaja claramente, y la pregunta en su off-topic.
```

Y los ejemplos, a continuación. En el chat, la pregunta que espera su decisión va además en su bloque `diff` de una línea, como hoy:

```text
Petición nueva (foco en la 379):
  🅵🅾🅲🆄🆂 `SF como un proyecto más (T❸ ❼ ❾ )`
  ¿Le doy el OK al texto recomendado ⭐ de la línea del CLAUDE.md❓
  (`ᴏꜰꜰ-ᴛᴏᴘɪᴄ` T❹ ❷ ❾ : anotada en cola; el panel de la app vuelve solo arriba; ¿la pongo en curso❓)

Pregunta sin tarea (foco en la 397): sin línea del foco.
  Los subagentes no escriben esa línea: Claude Code cambia su nombre por un resumen en vivo.

El foco espera a su subagente y vuelve el de otra:
  🅵🅾🅲🆄🆂 `Botones del panel más pequeños (T❸ ❾ ❼ )`
  (`ᴏꜰꜰ-ᴛᴏᴘɪᴄ` T❸ ❼ ❾ : lista para probar ▶️)

Aviso «ANTES DE NADA: lanza el subagente de la 426» (foco en la 383): se lanza y
  🅵🅾🅲🆄🆂 `Listas para probar en verde (T❸ ❽ ❸ )`
  <lo del foco, si lo hay>
  (`ᴏꜰꜰ-ᴛᴏᴘɪᴄ` T❹ ❷ ❻ : subagente lanzado)

«Ponla en curso» (la 431, foco en la 429): el foco no cambia.
  🅵🅾🅲🆄🆂 `Scroll del panel en la app (T❹ ❷ ❾ )`
  (`ᴏꜰꜰ-ᴛᴏᴘɪᴄ` T❹ ❸ ❶ : en curso 🟡, su subagente investiga de dónde viene el fallo)
```

## Anexo: texto propuesto para «Cómo funciona la Software Factory» | Dos cambios | Cómo funciona {#anexo-como-funciona}

Lo cambia su tarea «Actualizar Cómo funciona la Software Factory», no esta. El primero vale ya; el segundo, solo si se deciden como se recomienda las preguntas [9](#p9), [10](#p10) y [11](#p11).

```diff
- Las reglas del agente principal: […] y cómo preguntar y escribir. En los proyectos la entrega el mod entera; en la SF la carga el principal.
+ Las reglas del agente principal: […] y cómo preguntar y escribir. La entrega el mod entera, en los proyectos y en la SF, al empezar la sesión, tras /clear, tras compactar y cuando cambia al recargar el plugin.
```

```diff
  **Los avisos.** Con cada mensaje del propietario, el mod dice a Claude lo que el propietario ha cambiado en la cola desde el panel desde el mensaje anterior. Y le avisa de las tareas en curso sin subagente vivo y de los subagentes que han terminado sin recoger, una vez cada situación.
+ No avisa de lanzar el subagente de una tarea cuyo siguiente paso es «Esperar a …». Los avisos que piden actuar dicen que, si hay foco, lo hecho se cuenta solo como off-topic, y cuando el mod trae algo de otras tareas añade una línea que lo recuerda.
  Estos avisos se apagan con `"automatizaciones": {"avisos_subagentes": false}`. Llegan también en la SF.
```
