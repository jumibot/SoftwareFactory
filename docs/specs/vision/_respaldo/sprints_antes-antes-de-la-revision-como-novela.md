<!-- destino: proyecto -->
<!-- herramientas: recomendadas -->
# Sprints con objetivo: saber qué toca cada vez que abres Claude Code

**Estado:** 4 de noviembre de 2026, versión 0.6. Basado en las decisiones 260 a 262, 264 a 266, 269, 271 y 272 y en el informe «Sprints con objetivo» 1.10 (tarea 347).

<div class="caso">
<p class="caso-etiqueta">El caso · prólogo · una mañana en SmartColdBox</p>
<p>Abres Claude Code en SmartColdBox, la caja que lleva los viales de Marc de la farmacia a su nevera. En la cola se ha ido juntando de todo. Dos bugs que viste ayer: la campaña del gemelo se para a los 420 minutos de los 60 días, y la humedad interior sale negativa al abrir la tapa. Una petición sin concretar, «que la app avise antes». Ideas sueltas: el pesaje en el prototipo, la caja en ambulancias. La recarga en la farmacia, a medias. Y dos mensajes de fuera: el fabricante ofrece otra Peltier, y la farmacia pregunta si la caja cabe en su rack. El panel enseña <strong>4 tareas en curso, 19 en cola y 9 en observación</strong>, y todavía no hay sprint. <strong>¿Qué persigues esta mañana, y qué puede esperar?</strong></p>
</div>

## Resumen operativo

La respuesta es un **sprint con objetivo**: una frase con lo que quieres conseguir ahora, siempre a la vista en el panel. El objetivo decide qué se pone en curso. Lo demás se anota igual, pero espera en cola hasta que tú digas otra cosa.

Cada vez que abres Claude Code, Claude hace la **daily** sin que se lo pidas, haya sprint o no. Es un resumen de pie, de tres o cuatro líneas, tras el que preguntas o aportas lo que quieras. Sin sprint, la daily resume lo que hay y es el momento de fijar uno: Claude propone objetivos con su recomendación, y tú decides. Cuando ya no queda nada del objetivo, Claude te propone cambiar de sprint con una **revisión y planificación** breve: qué se consiguió y qué entra en el siguiente.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 440" width="100%" role="img" aria-label="El ciclo del sprint: abrir Claude Code, daily, seguir mientras queden tareas del objetivo; si no, revisión y objetivo nuevo" style="font-family:var(--fuente-texto);display:block">
<line x1="34" y1="40" x2="34" y2="400" stroke="#b2deda" stroke-width="2"/>
<circle cx="34" cy="40" r="7" fill="#00726b"/>
<text x="56" y="38" font-size="14.5" font-weight="700" fill="#004d47">Abres Claude Code · o escribes /sf_daily</text>
<text x="56" y="56" font-size="12.5" fill="#555">no hace falta pedir nada</text>
<circle cx="34" cy="110" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/>
<text x="56" y="108" font-size="14.5" font-weight="700" fill="#004d47">La daily · tres o cuatro líneas</text>
<text x="56" y="126" font-size="12.5" fill="#555">objetivo, en curso, qué espera de ti, qué hay en cola</text>
<circle cx="34" cy="180" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/>
<text x="56" y="178" font-size="14.5" font-weight="700" fill="#004d47">¿Quedan tareas del objetivo?</text>
<text x="56" y="196" font-size="12.5" fill="#555">sí: sigues el sprint, cerrando antes que abriendo</text>
<circle cx="34" cy="250" r="7" fill="#fff" stroke="#a6501a" stroke-width="2"/>
<text x="56" y="248" font-size="14.5" font-weight="700" fill="#a6501a">No quedan · revisión y planificación</text>
<text x="56" y="266" font-size="12.5" fill="#555">qué se consiguió, en una línea de números y lo importante</text>
<circle cx="34" cy="320" r="7" fill="#fff" stroke="#a6501a" stroke-width="2"/>
<text x="56" y="318" font-size="14.5" font-weight="700" fill="#a6501a">Objetivo nuevo · lo eliges tú</text>
<text x="56" y="336" font-size="12.5" fill="#555">si dudas, Claude propone dos o tres con su recomendación</text>
<circle cx="34" cy="400" r="7" fill="#00726b"/>
<text x="56" y="398" font-size="14.5" font-weight="700" fill="#004d47">Empieza el sprint siguiente</text>
<text x="56" y="416" font-size="12.5" fill="#555">entran sus tareas; lo de fuera espera en cola</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Sin fechas: un sprint dura lo que tarda su objetivo.</figcaption>
</figure>

Todo sale de la cola y de las decisiones, sin trabajo a mano. El resto del documento sigue esta misma mañana hasta el sprint siguiente.

---

## Por qué hace falta un rumbo corto

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 1 · Todo anotado, nada elegido</p>
<p>La cola cumple su papel: nada se pierde. Pero los bugs, las ideas y los mensajes de fuera piden atención a la vez. Las 9 en observación esperan tu OK desde hace días. ¿Cuál de las 32 tareas acerca hoy la caja al prototipo?</p>
</div>

Con Claude, anotar cuesta un segundo, y abrir una tarea, poco más. Lo que no se acelera es tu atención: decidir, probar y cerrar. Una cola sin rumbo no ordena ese trabajo; solo lo guarda.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 50 560 170" width="100%" role="img" aria-label="Estado de la cola de SmartColdBox esta mañana: 4 en curso, 19 en cola, 9 en observación" style="font-family:var(--fuente-texto);display:block">
<text x="14" y="76" font-size="14" font-weight="700" fill="#004d47">En curso</text>
<rect x="170" y="60" width="63" height="24" rx="4" fill="#00726b"/><text x="241" y="77" font-size="14" font-weight="700" fill="#004d47">4</text>
<text x="14" y="122" font-size="14" font-weight="700" fill="#004d47">En observación</text>
<rect x="170" y="106" width="142" height="24" rx="4" fill="#00726b" opacity=".75"/><text x="320" y="123" font-size="14" font-weight="700" fill="#004d47">9</text>
<text x="14" y="168" font-size="14" font-weight="700" fill="#004d47">En cola</text>
<rect x="170" y="152" width="300" height="24" rx="4" fill="#00726b" opacity=".5"/><text x="478" y="169" font-size="14" font-weight="700" fill="#004d47">19</text>
<text x="14" y="206" font-size="12.5" fill="#555">32 tareas abiertas; ninguna dice cuál toca ahora</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Ilustrativo: la cola de una mañana imaginada en SmartColdBox.</figcaption>
</figure>

El sprint añade lo único que faltaba: una frase que dice qué persigues. Con ella, la regla de siempre, **cerrar antes que abrir**, sabe qué cerrar primero.

---

## Dónde encaja: fase, devslice, sprint y tarea

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 2 · El primer sprint sale del desorden</p>
<p>La daily se hace igual, aunque no haya sprint: resume lo que hay y, como no hay objetivo, es el momento de fijar uno. ¿Cuál, y qué pasa con todo lo demás?</p>
</div>
<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · la primera daily, sin sprint</p>
<p class="escena-contexto">Claude Code recién abierto. Nadie ha escrito todavía.</p>
<div class="turno"><p class="ponente">Claude<small>daily</small></p><p>Buenos días. Tenemos pendiente bastante: dos bugs de ayer, el de los 420 minutos y el de la humedad; la recarga en la farmacia, a medias; «que la app avise antes», sin concretar; el pesaje y las ambulancias, como ideas; y el fabricante y la farmacia esperan respuesta. Y no tenemos sprint. Habría que decidir qué hacemos primero. Yo veo tres caminos: que el gemelo simule entero el verano de Marc, fijar la batería o contestar fuera. Iría a por el primero: el bug de los 420 minutos lo frena todo.</p></div>
<div class="turno"><p class="ponente">Tú<small>developer</small></p><p>El primero. ¿Y el de la humedad?</p></div>
<div class="turno"><p class="ponente">Claude<small>planificación</small></p><p>A la cola: no frena nada. Entran en el sprint el bug de los 420 minutos, la recarga y sacar los acumuladores en la nevera. Lo demás espera; si un bug fuera urgente, entraría marcado fuera del objetivo.</p></div>
<p class="escena-pie">Diálogo imaginado: no es una transcripción ni un resultado validado.</p>
</div>

El objetivo ordena el desorden sin perder nada: lo que no entra sigue anotado en la cola, y la petición sin concretar espera a que la concretes.

El método ya tenía dos niveles: la **fase** (visión, especificación, desarrollo…) y el **devslice**, una porción de producto completa que puede llevar días o semanas. El sprint es más corto: un devslice puede tener **muchos sprints**, y el objetivo de cada uno es una parte de lo que el devslice persigue. Debajo, las **tareas** de la cola.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 330" width="100%" role="img" aria-label="Jerarquía: fase, devslice, sprints y tareas, con un ejemplo ilustrativo" style="font-family:var(--fuente-texto);display:block">
<rect x="10" y="10" width="540" height="310" rx="10" fill="none" stroke="#b2deda" stroke-width="1.5"/>
<text x="26" y="38" font-size="14.5" font-weight="700" fill="#004d47">Fase · desarrollo</text>
<text x="26" y="56" font-size="12.5" fill="#555">dónde está el proyecto en el método</text>
<rect x="30" y="72" width="500" height="236" rx="10" fill="none" stroke="#00726b" stroke-width="1.5"/>
<text x="46" y="98" font-size="14.5" font-weight="700" fill="#00726b">Devslice · el viaje de los viales</text>
<text x="46" y="116" font-size="12.5" fill="#555">días o semanas; algo completo que se ve funcionar</text>
<rect x="50" y="132" width="220" height="160" rx="10" fill="none" stroke="#a6501a" stroke-width="2"/>
<text x="64" y="156" font-size="13.5" font-weight="700" fill="#a6501a">Sprint actual</text>
<text x="64" y="174" font-size="12" fill="#555">«que el gemelo simule</text>
<text x="64" y="189" font-size="12" fill="#555">entero el verano de Marc»</text>
<text x="64" y="216" font-size="12.5" fill="#004d47">● campaña de 60 días</text>
<text x="64" y="238" font-size="12.5" fill="#004d47">● acumuladores fuera</text>
<text x="64" y="260" font-size="12.5" fill="#004d47">● recarga en la farmacia</text>
<rect x="290" y="132" width="220" height="70" rx="10" fill="none" stroke="#999" stroke-width="1" stroke-dasharray="4 3"/>
<text x="304" y="160" font-size="13.5" font-weight="700" fill="#777">Sprint anterior</text>
<text x="304" y="180" font-size="12" fill="#777">cerrado, con su revisión</text>
<rect x="290" y="222" width="220" height="70" rx="10" fill="none" stroke="#999" stroke-width="1" stroke-dasharray="4 3"/>
<text x="304" y="250" font-size="13.5" font-weight="700" fill="#777">Sprint siguiente</text>
<text x="304" y="270" font-size="12" fill="#777">su objetivo, cuando toque</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Ilustrativo: el devslice y las tareas son un ejemplo, no un plan.</figcaption>
</figure>

En un proyecto sin metodología no hay fases ni devslices, pero sí cola. Por eso el sprint puede vivir igual en él; está por decidir si es así siempre o se puede apagar.

---

## Cómo empieza cada sesión: la daily

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 3 · Vuelves después de comer</p>
<p>Cierras Claude Code para comer. Al volver, lo abres y, antes de escribir nada, Claude ya está hablando. ¿Qué te cuenta, y cuánto tarda?</p>
</div>

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · la daily de la tarde</p>
<p class="escena-contexto">Claude Code recién abierto. Nadie ha escrito todavía.</p>
<div class="turno"><p class="ponente">Claude<small>daily</small></p><p>Seguimos con el verano de Marc. Tenemos pendiente: la campaña de 60 días va por el día 12, sacar los acumuladores en la nevera está para que lo pruebes, y la recarga sigue en marcha. Hay 9 en observación. Y ha entrado la leyenda del corte de la caja: habría que decidir si la metemos en el sprint.</p></div>
<div class="turno"><p class="ponente">Tú<small>developer</small></p><p>La leyenda, no: que espere. ¿Qué tengo que mirar en la prueba de los acumuladores?</p></div>
<div class="turno"><p class="ponente">Claude<small>orquestador</small></p><p>Que en la nevera el ejemplo ya no los lleve y la cámara siga entre 2 y 8 °C. Te abro la gráfica.</p></div>
<p class="escena-pie">Diálogo imaginado: no es una transcripción ni un resultado validado.</p>
</div>

La daily es una **reunión de pie**: breve, en la conversación y sin documento. No es un informe cerrado, sino el arranque de una conversación: tras el resumen, preguntas o aportas lo que quieras. Al revisar la cola, Claude te propone añadir al sprint lo que convenga, y tú decides.

Sale sola al abrir Claude Code: el mod se la encarga a Claude al empezar la sesión. Y la puedes pedir cuando quieras con **/sf_daily** o con palabras, sin cerrar ni abrir nada.

---

## Qué entra en el sprint y qué espera

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 4 · Algo urgente que no es del objetivo</p>
<p>A media tarde llega un aviso: mañana enseñas el gemelo en la farmacia del hospital, y su panel no arranca. No tiene nada que ver con el objetivo, pero no puede esperar. ¿Rompe el sprint?</p>
</div>

Una tarea entra en el sprint **al ponerse en curso**: ponerla en curso ya es tu decisión, y no hace falta otra orden. Lo que llega fuera del objetivo se anota como siempre, pero no se pone en curso sin que lo digas.

Si lo dices, porque es urgente, entra en el sprint **marcada «fuera del objetivo»**. Se hace sin fricción, y la revisión cuenta aparte cuánto se desvió el sprint.

Dos piezas que ya conoces cambian un poco:

- **TURBO** solo pone en curso las tareas del sprint que no te necesitan, y te avisa de cuántas de fuera podría hacer.
- **Las tareas en observación** no frenan el sprint, pero se intenta limpiarlas: la daily las cuenta y la revisión pregunta por las más antiguas.

---

## Cuándo se cambia de sprint

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 5 · No queda nada del objetivo</p>
<p>Días después, la campaña llega a los 60 días con la cámara en rango, y la prueba de los acumuladores está cerrada. En la daily, Claude lo nota antes que tú. ¿Y ahora qué?</p>
</div>

Un sprint **no tiene fecha**: acaba cuando se cumple su objetivo o cuando tú lo cambias. El ritmo con Claude es irregular, y una fecha obligaría a cerrar sprints a medias. Claude sugiere cerrarlo cuando no quedan tareas del objetivo; cambiar el objetivo a mitad también cierra el sprint, con su revisión.

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · revisión y planificación</p>
<p class="escena-contexto">La daily detecta que no quedan tareas del objetivo.</p>
<div class="turno"><p class="ponente">Claude<small>revisión</small></p><p>Sprint cumplido: 5 cerradas, 3 decisiones, 2 siguen en observación. Lo importante: el gemelo simula el verano entero, sin acumuladores en la nevera. ¿Cuál es el siguiente objetivo?</p></div>
<div class="turno"><p class="ponente">Tú<small>developer</small></p><p>No lo tengo claro.</p></div>
<div class="turno"><p class="ponente">Claude<small>planificación</small></p><p>Tres candidatos: fijar la batería, con su fracción útil y su presupuesto; cerrar las contradicciones que quedan del gemelo; empezar la especificación funcional. Recomiendo la batería: sin ella no hay presupuesto de la caja.</p></div>
<div class="turno"><p class="ponente">Tú<small>developer</small></p><p>De acuerdo, pero la leyenda del corte entra también.</p></div>
<p class="escena-pie">Diálogo imaginado: las cifras y los candidatos son ilustrativos.</p>
</div>

La revisión es tan breve como la daily: una línea de números, lo importante en pocas líneas y un menú con dos o tres candidatos y su recomendación. Termina con el objetivo nuevo y las tareas que entran en curso o esperan en cola.

---

## Qué cambia en el panel y en las órdenes

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 6 · Un vistazo basta</p>
<p>Al día siguiente, otra sesión. Antes de leer la daily, miras el panel. ¿Qué ves que antes no estaba?</p>
</div>

El panel enseña **solo el sprint actual**: su objetivo, en una línea bajo la cabecera, y una marca en sus tareas. Las secciones de siempre no cambian; lo de fuera, sin marca, sigue en su sitio.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 260" width="100%" role="img" aria-label="El panel con el objetivo del sprint bajo la cabecera y la marca en las tareas del sprint" style="font-family:var(--fuente-texto);display:block">
<rect x="10" y="10" width="540" height="240" rx="10" fill="none" stroke="#999" stroke-width="1"/>
<text x="26" y="38" font-size="14" font-weight="700" fill="#004d47">SmartColdBox</text>
<text x="380" y="38" font-size="12.5" fill="#555">TURBO  RELEASE</text>
<rect x="26" y="52" width="508" height="30" rx="6" fill="none" stroke="#a6501a" stroke-width="1.5"/>
<text x="38" y="72" font-size="13" font-weight="700" fill="#a6501a">Objetivo · que el gemelo simule entero el verano de Marc</text>
<text x="26" y="110" font-size="13" font-weight="700" fill="#004d47">En curso</text>
<text x="34" y="134" font-size="12.5" fill="#a6501a">●</text><text x="52" y="134" font-size="12.5" fill="#333">Ejecutar completa la campaña de 60 días</text>
<text x="34" y="156" font-size="12.5" fill="#a6501a">●</text><text x="52" y="156" font-size="12.5" fill="#333">Recargar en la farmacia, no en casa</text>
<text x="34" y="178" font-size="12.5" fill="#a6501a">◐</text><text x="52" y="178" font-size="12.5" fill="#333">Que el panel del gemelo arranque</text><text x="372" y="178" font-size="11.5" fill="#a6501a">fuera del objetivo</text>
<text x="26" y="210" font-size="13" font-weight="700" fill="#004d47">En cola</text>
<text x="52" y="234" font-size="12.5" fill="#777">Decidir si el pesaje entra en el prototipo</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Boceto ilustrativo: la forma de la marca se decide al construirlo.</figcaption>
</figure>

En las órdenes, una sola novedad: **/sf_daily**, para pedir la daily cuando quieras. No lleva botón en el panel: la cabecera ya va llena, y escribirla o pedirla con palabras basta.

---

## Lo que queda por decidir

Casi todo está decidido. Quedan cuatro puntos, cada uno con su recomendación en el informe «Sprints con objetivo»:

- **De dónde salen los candidatos a objetivo.** La cola no guarda prioridad. Se recomienda que Claude los ordene con su criterio (el devslice, lo bloqueado, los fallos, lo que más espera), cada uno con su porqué.
- **Proyectos sin metodología.** Se recomienda que tengan sprints igual, con un interruptor para apagarlos.
- **El kanban.** Se recomienda que, cuando haya kanban, el sprint viva allí y la carpeta `.sf/` sea su copia, como la cola.
- **Guardar la revisión.** Se recomienda guardarla como texto en el sprint, para que la siguiente revisión la tenga sin rehacerla.

---

## De vuelta al caso

<div class="caso">
<p class="caso-etiqueta">El caso · epílogo · otra mañana</p>
<p>Abres Claude Code. Antes de escribir, la daily: el objetivo, tres tareas en curso, una que espera tu prueba y una petición nueva que podría entrar. Las 19 de la cola siguen ahí, pero ya no piden atención: <strong>sabes qué persigues y qué puede esperar</strong>. La decisión de qué hacer después sigue siendo tuya; ahora la tomas con todo delante.</p>
</div>

---

## Anexo: el caso y sus fuentes

El caso ocurre en SmartColdBox, un proyecto real que se desarrolla con la SF: una caja autónoma que mantiene en frío los viales de un paciente, con su gemelo digital. Son reales del proyecto el verano de Marc de su visión (hora y media de transporte con 35 °C fuera y 60 días en la nevera), la campaña del gemelo que se quedó en 420 minutos, los acumuladores que el ejemplo de 60 días no retira, la recarga en la farmacia, la fracción útil de la batería y el presupuesto pendientes, la leyenda del corte de la caja y la duda del pesaje (`docs/decisiones-y-pendientes.md` de SmartColdBox).

Es ilustrativo todo lo demás. El proyecto está hoy en la fase de visión, sin devslices: la mañana, las cifras de la cola, las tareas tal como se nombran, el bug de la humedad, la petición de avisar antes, la idea de las ambulancias, la oferta del fabricante, la pregunta de la farmacia por su rack, el devslice, los objetivos, la demostración en la farmacia, las escenas y las cifras de la revisión son imaginados.

Las fuentes de los sprints son las decisiones del propietario de la Software Factory 260 a 262, 264 a 266, 269, 271 y 272 (`docs/decisiones/`) y el informe «Sprints con objetivo» 1.10 (`docs/referencias/reports/`), que recoge lo decidido con su porqué, las preguntas abiertas y las tareas que salen.
