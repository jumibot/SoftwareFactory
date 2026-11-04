---
antetitulo: Software Factory · Informe de análisis · Noviembre 2026
lema: Cada sprint, un objetivo; // cada sesión, su daily.
subtitulo: Cómo se organiza el trabajo en sprints con objetivo, qué es la daily al abrir Claude Code, cómo se cierra un sprint y empieza el siguiente, lo decidido, lo que queda por decidir y las tareas que salen.
version: Versión 1.6 · 04/11/2026
estado: Propuesta · Tarea 347
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de análisis
pie: Informe de la tarea «Que cada sprint tenga un objetivo y empiece con el resumen del anterior» (347). Parte de las decisiones 260 a 269, de la metodología, de sf:orquestacion, de cola.py y de lo que el mod entrega al empezar la sesión (contexto.ts, subagentes.ts). Espera la decisión del propietario. Las versiones anteriores, en _respaldo/.
---
# Sprints con objetivo

## Resumen | Un objetivo que orienta la cola | Resumen {#resumen}

El trabajo se organiza en **sprints**, cada uno con un **objetivo** de una frase, visible en el panel. El objetivo decide qué se pone en curso y qué espera en cola. Un devslice puede tener muchos sprints (260).

Cada vez que se abre Claude Code, Claude hace la **daily** (261): un resumen introductorio de tres o cuatro líneas con el objetivo, lo que está en curso, lo que espera prueba o decisión y lo que hay en cola, y después el developer pregunta o aporta lo que crea conveniente. Es el arranque de una conversación, no un informe cerrado. También se pide en cualquier momento, con `/sf_daily` (262, 264). Si no quedan tareas del objetivo, Claude propone cerrar el sprint: hace la **revisión y planificación** (qué se consiguió y qué entra en el siguiente) y pregunta el objetivo nuevo, con candidatos y su recomendación.

Hoy nada de esto existe. El mod entrega al empezar las reglas y la orquestación, pero **ningún resumen**; la cola no sabe de sprints ni de prioridades. Se proponen el ciclo de abajo, guardar el sprint en la cola con `cola.py` y que el mod lance la daily solo. De **14 preguntas**, once están decididas (265, 266, 269) y quedan **3 abiertas**, en tres bloques. La tarea se cierra con este informe validado (263, 267); al cerrarla se ofrece crear lo que sale, **cuatro tareas** nuevas y tres pasos en tareas de documentos, y lo decide el developer.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 380" width="100%" role="img" aria-label="Ciclo del sprint: al abrir Claude Code, la daily; si quedan tareas del objetivo, se sigue; si no, revisión y planificación y objetivo nuevo" style="font-family:var(--fuente-texto);display:block">
<defs>
<marker id="sp-f" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1f7a7a"/></marker>
<marker id="sp-n" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#a6501a"/></marker>
</defs>
<rect x="20" y="20" width="200" height="60" rx="10" fill="none" stroke="#1f7a7a" stroke-width="1.5"/>
<text x="120" y="47" font-size="16" font-weight="700" fill="#1f7a7a" text-anchor="middle">Abrir Claude Code</text>
<text x="120" y="67" font-size="13" text-anchor="middle" style="fill:var(--texto-suave)">o pedir la daily</text>
<line x1="220" y1="50" x2="330" y2="50" stroke="#1f7a7a" stroke-width="1.5" marker-end="url(#sp-f)"/>
<rect x="340" y="20" width="200" height="60" rx="10" fill="none" stroke="#1f7a7a" stroke-width="1.5"/>
<text x="440" y="47" font-size="16" font-weight="700" fill="#1f7a7a" text-anchor="middle">Daily</text>
<text x="440" y="67" font-size="13" text-anchor="middle" style="fill:var(--texto-suave)">3–4 líneas</text>
<line x1="440" y1="80" x2="440" y2="128" stroke="#1f7a7a" stroke-width="1.5" marker-end="url(#sp-f)"/>
<polygon points="440,135 540,180 440,225 340,180" fill="none" stroke="#1f7a7a" stroke-width="1.5"/>
<text x="440" y="176" font-size="13" text-anchor="middle" style="fill:var(--texto)">¿Quedan tareas</text>
<text x="440" y="194" font-size="13" text-anchor="middle" style="fill:var(--texto)">del objetivo?</text>
<line x1="340" y1="180" x2="232" y2="180" stroke="#1f7a7a" stroke-width="1.5" marker-end="url(#sp-f)"/>
<text x="286" y="170" font-size="13" font-weight="700" fill="#1f7a7a" text-anchor="middle">sí</text>
<rect x="20" y="150" width="200" height="60" rx="10" fill="none" stroke="#1f7a7a" stroke-width="1.5"/>
<text x="120" y="177" font-size="16" font-weight="700" fill="#1f7a7a" text-anchor="middle">Seguir el sprint</text>
<text x="120" y="197" font-size="13" text-anchor="middle" style="fill:var(--texto-suave)">cerrar antes que abrir</text>
<line x1="440" y1="225" x2="440" y2="273" stroke="#a6501a" stroke-width="1.5" marker-end="url(#sp-n)"/>
<text x="452" y="254" font-size="13" font-weight="700" fill="#a6501a">no</text>
<rect x="340" y="280" width="200" height="70" rx="10" fill="none" stroke="#a6501a" stroke-width="1.5"/>
<text x="440" y="307" font-size="15" font-weight="700" fill="#a6501a" text-anchor="middle">Revisión y</text>
<text x="440" y="326" font-size="15" font-weight="700" fill="#a6501a" text-anchor="middle">planificación</text>
<text x="440" y="343" font-size="12" text-anchor="middle" style="fill:var(--texto-suave)">del sprint que acaba</text>
<line x1="340" y1="315" x2="232" y2="315" stroke="#a6501a" stroke-width="1.5" marker-end="url(#sp-n)"/>
<rect x="20" y="280" width="200" height="70" rx="10" fill="none" stroke="#a6501a" stroke-width="1.5"/>
<text x="120" y="307" font-size="15" font-weight="700" fill="#a6501a" text-anchor="middle">Objetivo nuevo</text>
<text x="120" y="327" font-size="12" text-anchor="middle" style="fill:var(--texto-suave)">2–3 candidatos</text>
<text x="120" y="342" font-size="12" text-anchor="middle" style="fill:var(--texto-suave)">con recomendación</text>
<line x1="120" y1="280" x2="120" y2="218" stroke="#a6501a" stroke-width="1.5" marker-end="url(#sp-n)"/>
</svg>
</figure>

[Ver las 3 preguntas abiertas](#por-decidir){: .salto} [Ver las tareas](#tareas){: .salto}

## Punto de partida | De dónde sale y qué se pretende | Partida {#partida}

**El problema.** Con Claude Code se abren muchas tareas a la vez y la cola crece sin foco: en la SF, al empezar esta tarea, había 7 en curso, 36 en cola y 22 en observación. Al volver tras una pausa no hay un sitio que diga dónde se está ni qué toca, y nada distingue lo que se persigue ahora de lo que solo espera.

**Lo que se pretende.** Que el trabajo tenga un rumbo corto y visible (el objetivo del sprint), que situarse sea automático y barato (la daily), que cambiar de rumbo deje constancia de lo conseguido (la revisión y planificación) y que todo salga de la cola y las decisiones, sin trabajo a mano ni ceremonias que pesen.

**Cómo usar este informe.** Lo decidido está en [Decidido](#decidido), con su porqué; lo abierto, en [Por decidir](#por-decidir), con opciones y recomendación; y lo que hay que construir, en [Tareas](#tareas), listo para crear en la cola. Basta por sí solo para retomarlo sin la conversación (268).

## El sprint | Qué es, cuándo empieza y cuándo acaba | El sprint {#sprint}

Se propone:

::: tarjetas 3 plegables

#### Objetivo {color=turquesa icono=check}

Una frase con lo que se quiere conseguir, del tamaño de unas sesiones de trabajo. Es una parte de lo que persigue el devslice en curso (260), o, sin metodología, lo que el developer quiera conseguir ahora.

Orienta
:   Qué se pone en curso y qué espera en cola. Lo que llega fuera del objetivo se anota como siempre, pero no se pone en curso sin que el developer lo decida.

#### Daily {color=naranja icono=dialogo}

Al abrir Claude Code, sin pedirlo (261), y con `/sf_daily` (262, 264). Abre una conversación: tras el resumen, el developer pregunta o aporta.

Resume
:   - el objetivo;
    - las tareas en curso y qué espera cada una (probar, decidir, trabajo);
    - las en observación, en un número;
    - lo que hay en cola del sprint.

#### Revisión y planificación {color=verde icono=rama}

Al cerrar un sprint y abrir el siguiente.

Dice
:   - qué se consiguió: cerradas, decisiones, lo que queda;
    - el objetivo nuevo;
    - qué tareas entran en curso y cuáles esperan en cola.

:::

**Sin fechas.** Un sprint acaba cuando se cumple su objetivo o cuando el developer lo cambia (pregunta [1](#p1)). Así encaja con cómo se trabaja con Claude Code: por sesiones de duración irregular, no por semanas.

**Encaje con el método.** Fase → devslice → sprint → tarea. La fase y el devslice siguen en `.sf/estado.json`; el sprint es más corto que el devslice (260) y agrupa tareas de la cola. Sin metodología no hay fase ni devslice, pero sí cola, así que el sprint puede existir igual (pregunta [13](#p13)).

## Lo que hay hoy | Qué se puede aprovechar | Hoy {#hoy}

::: tarjetas 2

#### Lo que entrega el mod al empezar {color=turquesa icono=codigo}

En `SessionStart` (empezar, `/clear`, compactar), las reglas de la SF, la orquestación y la línea de Python (`contexto.ts`). Con el primer mensaje, los avisos de subagentes: las en curso sin subagente y los terminados sin recoger (`subagentes.ts`).

**No hay ningún resumen del estado.** La daily es nueva. El mod ya sabe encargar algo a Claude «como si lo escribiera el propietario» (`encargarAClaude`, el de TURBO): con eso puede lanzar la daily sola al abrir (pregunta [2](#p2)).

#### Lo que guarda la cola {color=naranja icono=carpeta}

Por tarea: número, texto, estado, tipo, descripción, pasos, rama, prueba, comprobado, commit e historial. No hay **sprint** ni **prioridad**: la posición en la cola es todo el orden que hay.

Hoy, en la SF: 7 en curso, 36 en cola y 22 en observación. Sin un objetivo, la cola no dice qué toca; con 22 en observación, la daily tiene que resumirlas en un número (pregunta [6](#p6)).

:::

Lo que ya dice la orquestación encaja sin cambiarla: **Cerrar antes que abrir** es seguir el sprint mientras queden tareas del objetivo; **Libre** es el momento de proponer cerrarlo; **Guiar, no solo ejecutar** es sugerir el cierre y los candidatos, sin hacerlo sin el OK.

## Decidido | Lo que ya está decidido | Decidido {#decidido}

| Nº | Decisión | Qué fija aquí | Por qué |
| --- | --- | --- | --- |
| 260 | Un devslice puede tener muchos sprints | El sprint es más corto que el devslice; su objetivo es una parte de lo que el devslice persigue. | El devslice puede llevar días o semanas; el sprint es el tramo que se organiza con un objetivo concreto y se revisa al cambiarlo. |
| 261 | El resumen al abrir Claude Code es la daily del sprint | Hay una daily cada vez que se abre Claude Code; se distingue de la revisión y planificación del cambio de sprint. | Da nombre conocido al momento de situarse y lo separa de la revisión. |
| 262 | La daily se puede pedir en cualquier momento | Además de la automática, cuando el developer quiera. | Tras una pausa o con muchas tareas a la vez, situarse no debe exigir cerrar y abrir Claude Code. |
| 263 | Una deliberación abre su tarea en curso al empezar y se cierra con su documento validado | Esta tarea se cierra con este informe validado; crear las tareas de [Tareas](#tareas) se ofrece al cerrar y lo decide el developer. | Ninguna decisión se queda en la conversación, y el informe basta para retomar las tareas más adelante (268). |
| 264 | La daily se pide con /sf_daily y es una conversación | La orden es `/sf_daily`; la daily es un resumen introductorio y después el developer pregunta o aporta. Si lleva además botón, en la pregunta [12](#p12). | Precisa la 262: la daily sitúa y abre el diálogo, no lo cierra. |
| 265 | Ciclo del sprint: cierre, daily, entrada de tareas y cambio de objetivo | Preguntas [1](#p1), [2](#p2), [4](#p4) y [7](#p7): sin fechas; la daily la encarga el mod al abrir; las tareas entran al ponerse en curso y cada daily revisa la cola; cambiar el objetivo abre otro sprint. | El ritmo con Claude es irregular y las fechas se incumplirían; revisar la cola en cada daily evita que el sprint se cierre a lo que llega; cambiar de objetivo sin revisión borraría lo conseguido. |
| 266 | Dónde vive el sprint, cómo se ve y qué hace con lo de fuera | Preguntas [3](#p3), [5](#p5), [6](#p6) y [8](#p8): en la cola, y el panel solo enseña el sprint actual; objetivo bajo la cabecera y marca en sus tareas; las en observación no frenan el cierre, pero se intenta limpiarlas; lo urgente de fuera entra marcado. | La cola ya es el estado del proyecto; ver solo el sprint actual mantiene el foco; las de observación no deben bloquear ni acumularse; lo urgente ocurre y debe verse. |
| 269 | TURBO, peso de la daily y orden sin botón | Preguntas [9](#p9), [10](#p10) y [12](#p12): TURBO solo con las del sprint; la daily, en la conversación, breve y sin documento; la revisión, también breve; solo `/sf_daily`, sin botón. | Respetar el objetivo y que la daily sea una reunión de pie, no un informe. |
| 267 | Una deliberativa no se cierra sin su documento validado | Esta tarea se cierra con este informe validado por el propietario. | El informe es el resultado de la deliberación. |
| 268 | El informe basta por sí solo para retomar lo decidido | Este informe lleva el punto de partida, lo decidido con su porqué, lo abierto con recomendación y las tareas listas para crear. | Se puede poner en práctica más adelante aunque la tarea se cierre sin crear las tareas ejecutivas. |

## Por decidir | Lo que queda por decidir | Por decidir {#por-decidir}

Catorce preguntas, numeradas por importancia; las 1 a 10 y la 12 están decididas (265, 266, 269) y quedan tres abiertas: 11, 13 y 14, en tres bloques: el sprint, la daily y la revisión, y dónde vive y cómo se ve. Las 1, 3 y 10 son las tres propuestas del principal.

### El sprint | Cuándo acaba, qué entra y qué pasa con lo de fuera | El sprint {#por-decidir-sprint}

Las reglas del sprint, que irían a la orquestación y a la metodología.

::: preguntas 2 plegables

### 1 · Qué cierra un sprint {estado=decidida recomendada=A elegida=A} {: #p1}

Opción A
:   El objetivo cumplido o el developer, que lo cambia. Sin fechas. Claude sugiere cerrarlo cuando no quedan tareas del sprint en curso ni en cola.

Opción B
:   Una fecha fija (una semana, por ejemplo), como un sprint de Scrum.

Opción C
:   Como A, y la daily avisa si el sprint pasa de un número de días sin cerrarse.

Recomendación
:   **A.** Se trabaja por sesiones irregulares; una fecha obligaría a cerrar sprints a medias. El aviso de C se puede añadir si se ven sprints eternos.

Decisión
:   A: sin fechas; Claude sugiere cerrarlo cuando no quedan tareas del sprint (265).

### 4 · Cómo entra una tarea en el sprint {estado=decidida recomendada=A elegida=A} {: #p4}

Opción A
:   Al ponerse en curso, entra sola en el sprint abierto. Las en cola entran en la planificación, con una orden de `cola.py`, cuando el developer las elige.

Opción B
:   Siempre de forma explícita, con una orden, también las que se ponen en curso.

Opción C
:   Claude decide cuáles son del objetivo, sin guardarlo.

Recomendación
:   **A.** Lo que se pone en curso ya es una decisión del developer; no hace falta otra orden.

Decisión
:   A, y además en cada daily se revisa si alguna tarea en cola o petición nueva conviene añadirla al sprint (265).

### 6 · Las tareas en observación {estado=decidida recomendada=A elegida=A} {: #p6}

Una en observación ya está integrada; solo espera el OK. Hoy hay 22 en la SF.

Opción A
:   No frenan el cierre del sprint. La daily las da en un número; la revisión las lista y pregunta por las dos o tres más antiguas («¿Cómo va la N?»).

Opción B
:   El sprint no se cierra mientras quede alguna suya en observación.

Opción C
:   Pasan solas al sprint siguiente, como pendientes.

Recomendación
:   **A.** Como en «Libre», no bloquean; preguntar por todas haría pesada cada revisión.

Decisión
:   A, con matiz: no frenan el cierre, pero se intenta limpiarlas; la daily las cuenta y la revisión pregunta por las más antiguas (266).

### 7 · Si el objetivo cambia a mitad {estado=decidida recomendada=A elegida=A} {: #p7}

Opción A
:   Cambiar el objetivo es cerrar el sprint: revisión corta y sprint nuevo. Las en curso pasan al nuevo si el developer las quiere; si no, a la cola.

Opción B
:   Se reescribe el objetivo en el mismo sprint, con el anterior en su historial.

Recomendación
:   **A.** Un sprint, un objetivo: la revisión queda limpia y el cambio se ve.

Decisión
:   A: cambiar el objetivo cierra el sprint con su revisión y abre otro (265).

### 8 · Lo de fuera del objetivo que el developer pone en curso {estado=decidida recomendada=A elegida=A} {: #p8}

Lo de fuera se anota y no se pone en curso sin el developer. Si él lo decide (un bug urgente, por ejemplo):

Opción A
:   Entra en el sprint marcada «fuera del objetivo», y la revisión la cuenta aparte.

Opción B
:   Entra en el sprint como cualquier otra.

Opción C
:   Queda fuera de todo sprint.

Recomendación
:   **A.** Se hace sin fricción, y la revisión enseña cuánto se desvió el sprint.

Decisión
:   A: entra marcada «fuera del objetivo»; puede ser algo urgente (266).

### 9 · TURBO dentro de un sprint {estado=decidida recomendada=A elegida=A} {: #p9}

Hoy TURBO pone en curso todas las de la cola que no necesitan al developer.

Opción A
:   Solo las del sprint. Avisa de cuántas de fuera podría hacer, sin ponerlas.

Opción B
:   Como hoy: todas.

Recomendación
:   **A.** Respeta el objetivo; pulsar TURBO no es decidir sobre lo de fuera.

Decisión
:   A: TURBO solo pone en curso las del sprint y avisa de cuántas de fuera podría hacer (269).

:::

### La daily y la revisión | Cuándo salen, qué dicen y cuánto pesan | Daily {#por-decidir-daily}

Cómo se produce cada resumen. Siguen «Comandos antes que inferencia»: los datos, de `cola.py`; Claude solo los cuenta.

::: preguntas 2 plegables

### 2 · Cómo sale la daily al abrir {estado=decidida recomendada=A elegida=A} {: #p2}

Claude Code no habla hasta que el developer escribe. Para que la daily salga «sin pedirlo» (261), alguien tiene que lanzarla.

Opción A
:   El mod la encarga a Claude al empezar la sesión (no tras `/clear`, compactar ni reanudar), como hace TURBO, con los datos de una orden de `cola.py`. Gasta un turno corto.

Opción B
:   Sale con el primer mensaje del developer, antes de atenderlo.

Opción C
:   La pinta el mod sin Claude, en el panel o un emergente.

Recomendación
:   **A.** Es la única que cumple «al abrir» con Claude hablando; B la retrasa y C no permite preguntar después.

Decisión
:   A: el mod la encarga al empezar la sesión, y además `/sf_daily` cuando el developer quiera (265).

### 10 · Que no pese {estado=decidida recomendada=A elegida=A} {: #p10}

Opción A
:   Resumen introductorio de la daily en 3–4 líneas, y después conversación; revisión con una línea de números (cerradas, decisiones, en observación, siguen) y lo importante en tres viñetas como mucho; menú de 2–3 candidatos con recomendación. La revisión se guarda como texto en el sprint.

Opción B
:   Como A, sin guardar la revisión.

Opción C
:   La revisión como informe HTML en `sf/informes/`.

Recomendación
:   **A.** Corto en pantalla y, guardado, la siguiente revisión y la historia del proyecto lo tienen sin rehacerlo.

Decisión
:   A, en la conversación y sin documento: la daily, breve, «de pie como toca»; la revisión al cambiar de sprint, también breve (269).

### 11 · De dónde salen los candidatos {recomendada=A} {: #p11}

Al abrir un sprint nuevo, Claude propone 2–3 objetivos candidatos «por prioridad». Lo que se prioriza son esos candidatos: qué conviene perseguir ahora. Para ordenarlos hace falta un criterio, y la cola no guarda prioridad.

Opción A
:   Del orden de la cola y del criterio de Claude: el devslice en curso, lo bloqueado, los bugs, lo que lleva más tiempo esperando. Cada candidato, con su porqué en una línea.

Opción B
:   Un campo de prioridad en cada tarea, que el developer pone.

Recomendación
:   **A.** Sin trabajo a mano; si los candidatos fallan a menudo, se añade B.

### 12 · Si `/sf_daily` lleva además un botón en el panel {estado=decidida recomendada=A elegida=A} {: #p12}

La orden es `/sf_daily` (264); también se puede pedir con palabras.

Opción A
:   Solo la orden y las palabras.

Opción B
:   También un botón DAILY en la cabecera del panel, junto a TURBO, que se la encarga a Claude.

Recomendación
:   **A.** La cabecera ya lleva ACTUALIZAR, RELEASE, TURBO y PRUEBA; el botón puede venir después si se usa mucho.

Decisión
:   A: solo `/sf_daily` y las palabras, sin botón (269).

:::

### Dónde vive y cómo se ve | Guardado, panel, proyectos sin metodología y kanban | Dónde {#por-decidir-donde}

Lo que necesita la implementación.

::: preguntas 2 plegables

### 3 · Dónde se guarda el sprint {estado=decidida recomendada=A elegida=A} {: #p3}

Opción A
:   En `.sf/peticiones.json`: una lista `sprints` (número, objetivo, inicio, fin, revisión) y, en cada tarea, el número de su sprint. Se escribe con `cola.py sprint …`, con las copias y el historial de la cola.

Opción B
:   En un archivo aparte, `.sf/sprint.json`.

Opción C
:   En `.sf/estado.json`, junto a la fase y el devslice.

Recomendación
:   **A.** Un solo archivo y un solo escritor; B duplica la mecánica de copias, y C solo existe con metodología.

Decisión
:   A: en `.sf/peticiones.json`, con `cola.py sprint`; además, el panel solo enseña el sprint actual (266).

### 5 · Cómo lo enseña el panel {estado=decidida recomendada=A elegida=A} {: #p5}

Opción A
:   El objetivo en una línea bajo la cabecera, y una marca en las tareas del sprint; las de fuera, sin marca.

Opción B
:   Solo el objetivo.

Opción C
:   Una sección «Sprint» que agrupa sus tareas, aparte de En curso y En cola.

Recomendación
:   **A.** Se ve qué es del objetivo sin cambiar las secciones que el developer ya conoce.

Decisión
:   A: el objetivo bajo la cabecera y una marca en las tareas del sprint (266).

### 13 · En un proyecto sin metodología {recomendada=A} {: #p13}

Opción A
:   Igual que con ella: el sprint es de la cola, no del método. Se puede apagar con `automatizaciones.sprints` en `.sf/proyecto.json`.

Opción B
:   Solo con metodología.

Recomendación
:   **A.** La cola existe en todos los proyectos y el desorden también; el interruptor cubre a quien no lo quiera.

### 14 · Relación con el kanban {recomendada=A} {: #p14}

La metodología ya dice que, con JKanban, la cola vivirá en el kanban y `.sf/` será su copia sin conexión.

Opción A
:   Lo mismo para el sprint: con kanban, vive allí (como sprint o etiqueta del tablero) y `.sf/` es su copia; hoy, sin kanban, `.sf/` es la fuente.

Opción B
:   El sprint siempre en `.sf/`; el kanban no sabe de sprints.

Recomendación
:   **A.** Una sola fuente, como la cola. Cómo se lleva a JKanban se decide al integrarlo.

:::

## Tareas | Las tareas que salen | Tareas {#tareas}

Esta tarea se cierra con el informe validado (263, 267). Al cerrarla se ofrece crear estas tareas y lo decide el developer; si no se crean, este informe basta para crearlas más adelante (268). Cada una se crea en cola con su título, su tipo y su descripción. Lo abierto que les afecta se dice en su descripción: mientras siga abierto, vale la recomendación.

Orden: primero «Guardar los sprints en la cola», del que dependen las demás; después la daily, el panel y la orquestación, en cualquier orden; los pasos de documentos, al cerrar cada una.

| Tarea | Tipo | Descripción |
| --- | --- | --- |
| Guardar los sprints en la cola | implementar | Que `.sf/peticiones.json` guarde los sprints (número, objetivo, inicio, fin y revisión) y en cada tarea su sprint, con `cola.py sprint abrir`, `cerrar`, `añadir` y `quitar`. Una tarea entra sola al ponerse en curso; las de fuera del objetivo, marcadas. Una orden da los datos de la daily y de la revisión, para que Claude no los cuente a mano. Abiertas: [13](#p13) (interruptor sin metodología) y [14](#p14) (kanban). |
| Que Claude haga la daily al abrir y con /sf_daily | implementar | Al empezar la sesión (no tras `/clear`, compactar ni reanudar), el mod encarga la daily a Claude con los datos de `cola.py`; la orden `/sf_daily` la pide en cualquier momento. Claude hace el resumen introductorio en 3–4 líneas, propone añadir al sprint las tareas en cola o peticiones nuevas que convenga, y deja que el developer pregunte o aporte. Sin botón en el panel. |
| Ver el objetivo del sprint en el panel | implementar | Solo el sprint actual: su objetivo, en una línea bajo la cabecera, y una marca en sus tareas. TURBO pone en curso solo las del sprint y avisa de cuántas de fuera podría hacer. Se apaga con `automatizaciones.sprints`. Abierta: [13](#p13). |
| Llevar el sprint a la orquestación | implementar | En `sf:orquestacion`: seguir el sprint mientras queden tareas del objetivo; en cada daily, mirar si algo de la cola conviene añadirlo; cambiar el objetivo cierra el sprint; sugerir cerrarlo cuando no queden; revisión y planificación con una línea de números y 2–3 candidatos con recomendación; lo de fuera del objetivo, anotado y sin poner en curso sin el developer; las en observación, en un número, intentando limpiarlas: la revisión pregunta por las más antiguas. Daily y revisión, breves y en la conversación. Abierta: [11](#p11) (candidatos). |
| Actualizar las reglas del método (316), paso | documentar | «Reflejar «Que cada sprint tenga un objetivo y empiece con el resumen del anterior» (347)»: el sprint en la metodología, con el texto del anexo. |
| Actualizar Cómo funciona la Software Factory (313), paso | documentar | «Reflejar … (347)»: el sprint en `.sf/peticiones.json` y la daily que encarga el mod. |
| Actualizar Cómo funciona el panel (198), paso | documentar | «Reflejar … (347)»: el objetivo bajo la cabecera, la marca del sprint y TURBO. |

## Anexo | Texto propuesto para la metodología | Anexo {#anexo}

Para «Tareas y cola», cuando se decida, en la tarea de las reglas del método:

> **Sprints**
> El trabajo se organiza en sprints, cada uno con un objetivo de una frase, visible en el panel, que orienta qué se pone en curso y qué espera en cola. Un devslice puede tener muchos sprints (260). Al abrir Claude Code, y con `/sf_daily`, Claude hace la daily: un resumen introductorio del objetivo, lo que está en curso, lo que espera prueba o decisión y lo que hay en cola, en pocas líneas, tras el que el developer pregunta o aporta (261, 262, 264). Un sprint acaba al cumplirse su objetivo o al cambiarlo el developer; el siguiente empieza con la revisión y planificación del anterior. Lo que llega fuera del objetivo se anota, pero no se pone en curso sin que el developer lo decida.
