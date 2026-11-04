<!-- destino: proyecto -->
<!-- herramientas: recomendadas -->
# Sprints con objetivo: saber qué toca cada vez que abres Claude Code

**Estado:** 4 de noviembre de 2026, versión 0.7. Basado en las decisiones 260 a 262, 264 a 266, 269, 271 y 272 y en el informe «Sprints con objetivo» 1.10 (tarea 347).

<div class="lector" data-titulo="El verano de Marc · prólogo">
<div class="libro">
<p class="libro-capitulo">Prólogo</p>
<p class="libro-titulo">Tres días para el jueves</p>
<p>El lunes, a las nueve y diez, Àlex abrió Claude Code con el café todavía caliente. Hacía meses que construía solo SmartColdBox, la caja que algún día llevaría los viales de Marc desde la farmacia del hospital hasta la nevera de su casa, en un pueblo a hora y media de autobús. Marc tenía hemofilia y un verano por delante; Àlex tenía un gemelo digital que aún no sabía contarlo entero.</p>
<p>En la bandeja esperaba un correo de Laura, la farmacéutica: <em>«¿El jueves nos enseñas el gemelo? Y dime si la caja cabe en nuestro rack»</em>. El jueves. Laura querría ver el verano de Marc de principio a fin: el autobús de las 13:15 con 34 °C en la calle y sesenta días de nevera. Y la última campaña del gemelo se había parado a los 420 minutos, sin avisar, como quien se cansa a mitad de cuesta.</p>
<p class="libro-ornamento"></p>
<p>Lo demás se había ido amontonando durante la semana, sin pedir permiso. Otro bug, el de la humedad, que salía negativa al abrir la tapa. Una petición que él mismo había escrito un domingo por la noche, «que la app avise antes», sin decir antes de qué. Dos ideas sueltas: pesar los viales, llevar la caja en ambulancias. La recarga en la farmacia, a medias desde el jueves anterior. Y una oferta del fabricante de la Peltier, con un modelo nuevo y una pregunta por el volumen.</p>
<p>Nada se había perdido: todo estaba anotado. El panel lo decía con su calma de siempre, <strong>4 en curso, 19 en cola, 9 en observación</strong>, y en ningún sitio ponía qué tocaba ahora. No había sprint. Àlex miró la lista, miró el correo de Laura y pensó lo que piensa cualquiera con tres días por delante: <strong>¿por dónde se empieza?</strong></p>
</div>
</div>

## Resumen operativo

La respuesta es un **sprint con objetivo**: una frase con lo que quieres conseguir ahora, siempre a la vista en el panel. El objetivo decide qué se pone en curso. Lo demás se anota igual, pero espera en cola hasta que tú digas otra cosa.

Cada vez que abres Claude Code, Claude hace la **daily** sin que se la pidas, haya sprint o no: un resumen de pie, de tres o cuatro líneas, y después conversas. Sin sprint, es el momento de fijar uno: Claude propone objetivos con su recomendación, y tú decides. Cuando no queda nada del objetivo, Claude propone la **revisión y planificación**: qué se consiguió y qué entra en el siguiente.

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

Todo sale de la cola y de las decisiones, sin trabajo a mano. El resto del documento sigue la semana de Àlex, del lunes al jueves de la farmacia y al lunes siguiente.

---

## Por qué hace falta un rumbo corto

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 1 · Cuarenta minutos en la humedad</p>
<p>A las nueve y doce, la daily empieza a hablar, pero Àlex ya tiene abierto el bug de la humedad: parece fácil, cosa de un rato. Cuarenta minutos después sigue en él, y el de los 420 minutos, el que decide el jueves, no lo ha tocado nadie. No ha perdido el tiempo; lo ha gastado en lo que tenía más a mano.</p>
</div>

Con Claude, anotar cuesta un segundo, y abrir una tarea, poco más. Lo que no se acelera es tu atención: decidir, probar y cerrar. Una cola sin rumbo no ordena ese trabajo; solo lo guarda, y lo más cercano gana a lo más importante.

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
<p>A las diez menos cinco, Àlex aparta la humedad y escribe <code>/sf_daily</code>. Esta vez escucha antes de elegir.</p>
</div>
<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · la primera daily, sin sprint</p>
<p class="escena-contexto">Lunes, 9:55. Claude habla primero.</p>
<div class="turno"><p class="ponente">Claude<small>daily</small></p><p>Tenemos pendiente bastante: dos bugs, el de los 420 minutos y el de la humedad; la recarga en la farmacia, a medias; «que la app avise antes», sin concretar; el pesaje y las ambulancias, como ideas; y Laura y el fabricante esperan respuesta. No tenemos sprint. Habría que decidir qué hacemos primero. Veo tres caminos: que el gemelo simule entero el verano de Marc, fijar la batería o contestar fuera. Iría a por el primero: es lo que Laura quiere ver el jueves.</p></div>
<div class="turno"><p class="ponente">Àlex<small>developer</small></p><p>Vale. ¿Y la humedad? Ya le he dedicado un rato.</p></div>
<div class="turno"><p class="ponente">Claude<small>planificación</small></p><p>A la cola, con lo que ya sabes anotado: no frena el jueves. Entran el bug de los 420 minutos, la recarga y sacar los acumuladores en la nevera. A Laura le contesto lo del rack en una línea.</p></div>
<p class="escena-pie">Diálogo imaginado: no es una transcripción ni un resultado validado.</p>
</div>

Nada se pierde al elegir: lo que no entra sigue anotado en la cola, y la petición sin concretar espera a que la concretes.

El objetivo de Àlex es pequeño a propósito. El método ya tenía la **fase** (visión, especificación, desarrollo…) y el **devslice**, una porción de producto completa que puede llevar semanas. El sprint es más corto: un devslice tiene **muchos sprints**, y el objetivo de cada uno es una parte de lo que el devslice persigue. Debajo, las **tareas** de la cola.

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

En un proyecto sin metodología no hay fases ni devslices, pero sí cola. Por eso el sprint puede vivir igual en él; está por decidir si siempre o con interruptor.

---

## Cómo empieza cada sesión: la daily

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 3 · Martes, después de comer</p>
<p>El lunes y la mañana del martes pasan sin desvíos: la campaña corre sola mientras Àlex prepara la recarga. La humedad espera en la cola. El martes cierra Claude Code para comer y, al volver, antes de escribir nada, Claude ya está hablando.</p>
</div>
<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · la daily de la tarde</p>
<p class="escena-contexto">Martes, 15:20.</p>
<div class="turno"><p class="ponente">Claude<small>daily</small></p><p>Seguimos con el verano de Marc. Tenemos pendiente: la campaña va por el día 12 y no se ha parado; sacar los acumuladores en la nevera está para que lo pruebes; la recarga, en marcha. Ha entrado la leyenda del corte de la caja: habría que decidir si la metemos.</p></div>
<div class="turno"><p class="ponente">Àlex<small>developer</small></p><p>La leyenda, no: el jueves nadie va a mirar el dibujo. ¿Qué miro en lo de los acumuladores?</p></div>
<div class="turno"><p class="ponente">Claude<small>orquestador</small></p><p>Que en la nevera ya no estén y la cámara siga entre 2 y 8 °C. Te abro la gráfica.</p></div>
<p class="escena-pie">Diálogo imaginado: no es una transcripción ni un resultado validado.</p>
</div>

La daily es una **reunión de pie**: breve, en la conversación y sin documento. Arranca con lo pendiente, «tenemos pendiente…», y con lo que hay que decidir, «habría que decidir…»; después hablas tú. Al repasar la cola, Claude propone qué añadir al sprint, y tú decides.

Sale sola al abrir Claude Code, porque el mod se la encarga a Claude. Y la pides cuando quieras con **/sf_daily** o con palabras.

---

## Qué entra en el sprint y qué espera

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 4 · Miércoles, 19:40</p>
<p>La víspera de la farmacia, Àlex lanza el panel del gemelo para ensayar. Pantalla en blanco. No tiene nada que ver con el verano de Marc, pero sin panel no hay demo, y arreglarlo le va a costar la noche y la recarga, que se queda para la semana siguiente.</p>
</div>
<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · lo urgente</p>
<p class="escena-contexto">Miércoles, 19:42.</p>
<div class="turno"><p class="ponente">Àlex<small>developer</small></p><p>El panel del gemelo no arranca. Ponlo en curso ya.</p></div>
<div class="turno"><p class="ponente">Claude<small>orquestador</small></p><p>Entra en el sprint marcado «fuera del objetivo». La campaña sigue sola; la humedad, en cola.</p></div>
<p class="escena-pie">Diálogo imaginado: no es una transcripción ni un resultado validado.</p>
</div>

Una tarea entra en el sprint **al ponerse en curso**: ponerla en curso ya es tu decisión. Lo que llega fuera del objetivo se anota, pero no se pone en curso sin que lo digas. Si lo dices, entra **marcado «fuera del objetivo»**, sin fricción, y la revisión cuenta aparte cuánto se desvió el sprint.

Dos piezas que ya conoces se ajustan al objetivo:

- **TURBO** solo pone en curso las tareas del sprint que no te necesitan, y avisa de cuántas de fuera podría hacer.
- **Las tareas en observación** no frenan el sprint, pero se intenta limpiarlas: la daily las cuenta y la revisión pregunta por las más antiguas.

---

## Cuándo se cambia de sprint

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 5 · Jueves, en la farmacia</p>
<p>A medianoche el panel vuelve a arrancar. A las once del jueves, en el despacho de Laura, el gemelo recorre el verano de Marc: el autobús de las 13:15 a 34 °C y sesenta días de nevera, con la cámara en rango de principio a fin. Laura sonríe y pregunta lo único que Àlex aún no sabe: cuánto aguanta la batería. Esa tarde, la daily lo nota antes que él: no queda nada del objetivo.</p>
</div>
<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · revisión y planificación</p>
<p class="escena-contexto">Jueves, 17:05.</p>
<div class="turno"><p class="ponente">Claude<small>revisión</small></p><p>Sprint cumplido: cinco cerradas, tres decisiones, dos en observación; una fuera del objetivo, el panel del gemelo. Lo importante: el verano de Marc, entero. Habría que decidir el siguiente.</p></div>
<div class="turno"><p class="ponente">Àlex<small>developer</small></p><p>Laura ya lo ha decidido por mí, creo.</p></div>
<div class="turno"><p class="ponente">Claude<small>planificación</small></p><p>Lo veo igual: fijar la batería, con su fracción útil y su presupuesto. Los otros dos caminos son cerrar las contradicciones del gemelo o empezar la especificación. Sin batería no hay presupuesto de la caja.</p></div>
<div class="turno"><p class="ponente">Àlex<small>developer</small></p><p>La batería. Y mete la leyenda del corte, que ya toca.</p></div>
<p class="escena-pie">Diálogo imaginado: las cifras y los candidatos son ilustrativos.</p>
</div>

Un sprint **no tiene fecha**: acaba cuando se cumple su objetivo o cuando lo cambias, y cambiarlo a mitad también lo cierra, con su revisión. El ritmo con Claude es irregular, y una fecha obligaría a cerrar sprints a medias. La revisión es tan breve como la daily: una línea de números, lo importante y dos o tres candidatos con su recomendación.

---

## Qué cambia en el panel y en las órdenes

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 6 · Un vistazo</p>
<p>El viernes, Àlex abre el panel antes que la daily. Arriba, en una línea, el objetivo nuevo: fijar la batería. Le basta para saber dónde está.</p>
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

Quedan cuatro puntos, cada uno con su recomendación en el informe «Sprints con objetivo»:

- **De dónde salen los candidatos a objetivo.** La cola no guarda prioridad. Se recomienda que Claude los ordene con su criterio (el devslice, lo bloqueado, los fallos, lo que más espera), cada uno con su porqué, como hizo el lunes con el jueves de Laura.
- **Proyectos sin metodología.** Se recomienda que tengan sprints igual, con un interruptor para apagarlos.
- **El kanban.** Se recomienda que, cuando haya kanban, el sprint viva allí y la carpeta `.sf/` sea su copia, como la cola.
- **Guardar la revisión.** Se recomienda guardarla como texto en el sprint, para que la siguiente revisión la tenga sin rehacerla.

---

## De vuelta al caso

<div class="lector" data-titulo="El verano de Marc · epílogo">
<div class="libro">
<p class="libro-capitulo">Epílogo</p>
<p class="libro-titulo">Otro lunes</p>
<p>El lunes siguiente, a las nueve y diez, Àlex abrió Claude Code con el café todavía caliente. Esta vez no abrió nada antes de escuchar. «Seguimos con la batería —dijo Claude—. Tenemos pendiente la curva del fabricante y el presupuesto; la humedad sigue en cola, y la recarga vuelve esta semana».</p>
<p>El bug de la humedad llevaba una semana esperando, y no había pasado nada. La leyenda del corte había esperado tres días; la recarga, una semana, el precio de una noche de urgencias. Laura tenía su respuesta sobre el rack, y Marc, por fin, su verano entero en el gemelo. Las 19 de la cola seguían ahí, pero ya no tiraban de él.</p>
<p class="libro-ornamento"></p>
<p>Aquella semana Àlex no había trabajado más que otras. Había elegido antes. Lo cercano y lo urgente siempre encuentran hueco solos; lo importante solo lo encuentra si alguien lo nombra cada mañana, en una frase, y se atreve a dejar esperando lo demás. <strong>Saber qué perseguía y qué podía esperar</strong> no le quitaba ninguna decisión: se las ponía todas delante.</p>
</div>
</div>

---

## Anexo: el caso y sus fuentes

El caso ocurre en SmartColdBox, un proyecto real que se desarrolla con la SF: una caja autónoma que mantiene en frío los viales de un paciente, con su gemelo digital. Son reales del proyecto Marc, Laura y el verano de su visión (el autobús de las 13:15, hora y media de transporte con 35 °C fuera y 60 días en la nevera), la campaña del gemelo que se quedó en 420 minutos, los acumuladores que el ejemplo de 60 días no retira, la recarga en la farmacia, la fracción útil de la batería y el presupuesto pendientes, la leyenda del corte de la caja y la duda del pesaje (`docs/decisiones-y-pendientes.md` de SmartColdBox).

Es ilustrativo todo lo demás. El proyecto está hoy en la fase de visión, sin devslices. Son imaginados Àlex, la semana y sus horas, la demostración en la farmacia, el correo de Laura, las cifras de la cola, las tareas tal como se nombran, el bug de la humedad, la petición de avisar antes, la idea de las ambulancias, la oferta del fabricante, la pregunta por el rack, el fallo del panel del gemelo, el devslice, los objetivos, las escenas y las cifras de la revisión.

Las fuentes de los sprints son las decisiones del propietario de la Software Factory 260 a 262, 264 a 266, 269, 271 y 272 (`docs/decisiones/`) y el informe «Sprints con objetivo» 1.10 (`docs/referencias/reports/`), que recoge lo decidido con su porqué, las preguntas abiertas y las tareas que salen.
