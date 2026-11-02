# SoftwareFactory: el taller del hombre orquesta

<div class="caso">
<p class="caso-etiqueta">El caso · prólogo · un lunes por la mañana</p>
<p>Es lunes por la mañana. La sesión empieza con una frase: «dime qué tenemos pendiente». Claude no lo sabe de memoria: lee unas notas y un registro para reconstruirlo. Salen siete preguntas sin responder, cambios fuera de git en cuatro proyectos y una aplicación educativa esperando una decisión desde ayer. En media hora llegan seis commits, cinco propuestas de mejora y la idea de esta visión. Ninguno de los pendientes del principio se ha cerrado. <strong>¿Cómo se llevan seis trabajos y muchos proyectos sin que el día te lleve a ti?</strong></p>
</div>

## Resumen operativo

Esta visión cuenta SoftwareFactory desde otro lado. La primera explica cómo se construye un proyecto, de la visión al código. Esta explica para quién: para el **hombre orquesta del software**. Es una sola persona que cada día desarrolla, investiga, crea proyectos y visiones, enseña, aprende y se mantiene al día.

Su propósito es que lleves a término tus proyectos, no que abras más. La IA ha acelerado los seis trabajos a la vez, y tu atención sigue siendo la misma. Por eso la SF no busca que produzcas más: busca **pedirte menos atención**.

No parte de cero. Integra todo lo que ya existe y te sirve, entero o en parte: tus skills, las técnicas de otros y la mecánica de Claude Code. Tiene un solo centro, Claude Code, conectado a tu tablero. Una daily ordena el día por tipo de trabajo, y la visión hace de brújula. Un tope limita los frentes abiertos, y un catálogo reúne los instrumentos.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 46 560 454" width="100%" role="img" aria-label="Un día ordenado por tipo de trabajo con la SF" style="font-family:var(--fuente-texto);display:block">
<line x1="34" y1="66" x2="34" y2="456" stroke="#b2deda" stroke-width="2"/>
<circle cx="34" cy="66" r="7" fill="#00726b"/><text x="56" y="64" font-size="14.5" font-weight="700" fill="#004d47">Al empezar · la daily</text><text x="56" y="82" font-size="12.5" fill="#555">cómo va cada proyecto y qué espera de ti</text>
<circle cx="34" cy="131" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="129" font-size="14.5" font-weight="700" fill="#004d47">Lo fijo · lo que tiene fecha</text><text x="56" y="147" font-size="12.5" fill="#555">lo que marcan otros va primero; lo demás se coloca alrededor</text>
<circle cx="34" cy="196" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="194" font-size="14.5" font-weight="700" fill="#004d47">Un rato protegido · crear y aprender</text><text x="56" y="212" font-size="12.5" fill="#555">visiones, ideas y lo que quieres entender tú, sin avisos</text>
<circle cx="34" cy="261" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="259" font-size="14.5" font-weight="700" fill="#004d47">En segundo plano · desarrollar e investigar</text><text x="56" y="277" font-size="12.5" fill="#555">los agentes avanzan lo que ya está preparado</text>
<circle cx="34" cy="326" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="324" font-size="14.5" font-weight="700" fill="#004d47">Uno o dos momentos · decidir</text><text x="56" y="342" font-size="12.5" fill="#555">la bandeja, por lotes, cuando tú eliges</text>
<circle cx="34" cy="391" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="389" font-size="14.5" font-weight="700" fill="#004d47">Una vez por semana · estar al día</text><text x="56" y="407" font-size="12.5" fill="#555">lo nuevo de tu contexto tecnológico, en un resumen</text>
<circle cx="34" cy="456" r="7" fill="#00726b"/><text x="56" y="454" font-size="14.5" font-weight="700" fill="#004d47">Al cerrar · lo abierto</text><text x="56" y="472" font-size="12.5" fill="#555">los frentes del día, contados frente a tu tope</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Ilustrativo. Los agentes trabajan cuando tú no puedes atenderlos, y no al revés.</figcaption>
</figure>

El resto del documento sigue esa mañana, sección a sección, y termina en la del día siguiente. Es una visión para ti: una guía a vista de pájaro para no perder el rumbo de la propia fábrica.

---

## Por qué el límite eres tú

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 1 · Media hora muy productiva</p>
<p>Sale el primer commit del día: la visión de la SF explica ahora en qué se diferencia. Unos minutos después llegan tres propuestas de mejora, luego otra y luego la quinta. Cada idea es buena y cada una lleva a la siguiente. Media hora después hay seis commits nuevos. ¿Has avanzado, o solo has abierto?</p>
</div>

Lo que te pasa esta mañana ya tiene cifras. Un estudio del NBER con más de 500.000 desarrolladores mide qué cambia con los agentes autónomos. Los commits suben mucho más que lo que llega a publicarse ([NBER w35275, 2026](https://www.nber.org/papers/w35275)).

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 50 560 170" width="100%" role="img" aria-label="Con agentes autónomos, según el NBER: commits, proyectos y versiones publicadas" style="font-family:var(--fuente-texto);display:block">
<text x="14" y="76" font-size="14" font-weight="700" fill="#004d47">Commits</text>
<rect x="190" y="60" width="300" height="24" rx="4" fill="#00726b"/><text x="498" y="77" font-size="14" font-weight="700" fill="#004d47">+240 %</text>
<text x="14" y="122" font-size="14" font-weight="700" fill="#004d47">Proyectos</text>
<rect x="190" y="106" width="100" height="24" rx="4" fill="#00726b" opacity=".75"/><text x="298" y="123" font-size="14" font-weight="700" fill="#004d47">+80 %</text>
<text x="14" y="168" font-size="14" font-weight="700" fill="#004d47">Versiones publicadas</text>
<rect x="190" y="152" width="38" height="24" rx="4" fill="#00726b" opacity=".5"/><text x="236" y="169" font-size="14" font-weight="700" fill="#004d47">+30 %</text>
<text x="14" y="206" font-size="12.5" fill="#555">lo que se produce crece mucho más que lo que se termina</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Con agentes autónomos, según el NBER. Resultados de estudio, no una predicción para tus proyectos.</figcaption>
</figure>

El eslabón que no se acelera es humano: revisar, decidir y cerrar. Faros, que analiza la actividad de 22.000 desarrolladores, ve cómo el tiempo de revisión se multiplica por cinco ([Faros, 2026](https://www.faros.ai/research/ai-acceleration-whiplash)). Es un informe de un proveedor, pero apunta en la misma dirección.

Además, cuesta notarlo desde dentro. En el ensayo de METR, desarrolladores expertos tardaron un 19 % más con IA y creían haber ido un 20 % más rápido ([METR, 2025](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)). La sensación de avanzar no es una medida. Por eso la SF cuenta lo que se cierra, no lo que se abre.

---

## Seis trabajos, un solo taller

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 2 · Todos en la misma mañana</p>
<p>Nadie los ha nombrado así, pero esta mañana están los seis. La aplicación educativa espera para avanzar, y el gemelo digital de un dispositivo va por su versión 4.0. A media mañana se lanza una investigación en cinco frentes. Nace esta visión. Descubres fricciones que «recién estás intuyendo». Y una charla que dar la semana que viene sigue ahí. ¿Es lo mismo todo esto?</p>
</div>

No lo es. Todo es crear software, pero cada trabajo pide una atención distinta y termina de otra manera. Ordenados de más a menos delegable:

- **Desarrollar.** Convergente: el qué ya está decidido. Termina en una devslice cerrada. Lo tocan el tablero, las devslices y los agentes.
- **Investigar.** Parte de una pregunta acotada. Se delega bien, pero hay que verificar. Termina en un informe con sus fuentes, en `docs/referencias/`.
- **Estar al día.** Vigilancia de tu contexto tecnológico: Claude Code, BMAD, las herramientas nuevas. Termina en una decisión: adoptar, probar o ignorar.
- **Crear proyectos y visiones.** Divergente: necesita calma y ratos largos. La IA trabaja contigo, no por ti. Termina en una visión, con la skill de visión y el vibe design.
- **Aprender.** Tiene que pasar por ti. Termina en lo que sabes hacer sin ayuda.
- **Enseñar.** Formar a otros y contar tu trabajo. Cuando tiene fechas que marcan otros, no se delega.

Pasar de revisar una devslice a escribir una visión no es cambiar de pestaña: es cambiar de forma de pensar. Por eso la daily no reparte el día solo por proyectos, sino por tipos de trabajo. Lo que tiene fecha fija se coloca primero.

Los seis trabajos se alimentan entre sí, y la SF es donde se encuentran. Lo que investigas alimenta tus visiones, y las visiones abren proyectos. Lo que aprendes y lo que vigilas mejora la fábrica. Y lo que la fábrica produce te sirve para enseñar: quienes aprenden de ti se encontrarán mañana con las mismas fricciones que tú hoy.

---

## Cómo retomas cada proyecto

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 3 · Reconstruir de memoria</p>
<p>Para responder «qué tenemos pendiente», Claude junta tres notas de memoria y un registro de 226 líneas. Y aun así falta algo. La aplicación educativa empezó en ChatGPT Work, y en su repositorio no queda rastro de aquella conversación. Hay una visión, dos PDF de referencia y nada más. ¿Qué se decidió al principio, y por qué?</p>
</div>

Retomar cuesta, y no solo a ti. En 10.000 sesiones de 85 programadores, solo el 10 % empezó a editar en menos de un minuto. En el 30 %, la primera edición llegó después de media hora ([Parnin y Rugaber, 2010](https://sites.cc.gatech.edu/reverse/repository/resumptionstrategies.pdf)).

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · la daily con la SF</p>
<p class="escena-contexto">Lunes por la mañana. El resumen ya está escrito cuando abres la sesión.</p>
<div class="turno"><p class="ponente">Claude<small>resume</small></p><p>La aplicación educativa espera de ti una decisión: diseñar ya la pantalla de revisión o hacer antes la especificación. El dispositivo tiene el gemelo 4.0 verificado la semana pasada; su perfil técnico necesita los datos del hardware. SoftwareFactory tiene cinco propuestas nuevas por aprobar.</p></div>
<div class="turno"><p class="ponente">Tú<small>pregunta</small></p><p>¿Y lo de ChatGPT de la aplicación educativa?</p></div>
<div class="turno"><p class="ponente">Claude<small>responde</small></p><p>No está en el proyecto. Si me pegas lo que se decidió allí, lo guardo en sus referencias con la fecha y su porqué.</p></div>
<div class="turno sistema"><p class="ponente">Tablero<small>estado</small></p><p>Frentes abiertos: tres de un tope de cuatro.</p></div>
<p class="escena-pie">Diálogo imaginado; el tope de cuatro es un ejemplo.</p>
</div>

Lo que acabas de ver es un **resumen de retorno**. Tiene el mismo formato en todos los proyectos y sale del tablero, no de tu memoria. Claude lo escribe antes de que preguntes. Así, retomar deja de ser una arqueología.

La regla que lo hace posible es sencilla: lo que importa vive en el proyecto, no en un chat. Lo decidido en ChatGPT, en un lienzo de Claude Design o en una conversación se trae a `docs/referencias/` o a `docs/decisiones/`. Lo que no se trae, para la SF no existe.

---

## Cómo no pierdes el rumbo

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 4 · Una idea a mitad de la daily</p>
<p>A media mañana dices: «creo que este proyecto requiere más de un documento de visión». Es una buena idea, y es la que ha dado lugar a este documento. Pero también es un frente nuevo, abierto antes de cerrar ningún pendiente. ¿Sirve a la estrategia, o la desvía?</p>
</div>

Cuando producir es fácil, el riesgo ya no es quedarse corto, sino perderse. Simon Willison, uno de los programadores que más escribe sobre agentes, lo cuenta así: «I've got some very cool software that I built that I've never used». Y habla de amigos que vacían su lista de pendientes y sienten «a sort of sense of loss… Now what am I going to build?» ([Lenny's Podcast, abril de 2026](https://simonwillison.net/2026/Apr/2/lennys-podcast/)).

La brújula de cada proyecto es su visión, y cada visión termina en una pregunta. La de la aplicación educativa es cómo dar el mismo texto difícil a toda la clase sin bajar la exigencia. Cuando la SF planifica o cierra una devslice, la contrasta con esa pregunta. Si el trabajo se aleja, te avisa antes de seguir.

Las ideas nuevas no se pierden, pero tampoco abren un frente sin permiso. Van a un **banco de ideas**, con su fecha y su porqué. En la daily decides si alguna pasa a ser proyecto. Esta visión pasó, y por eso existe.

---

## Qué espera de ti

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 5 · Siete preguntas</p>
<p>Hoy hay siete preguntas. Qué paso sigue en la aplicación educativa. Dónde se registra su contexto técnico. Si se prueba pronto el agente, y quién paga su clave. Si se lleva un registro de cambios. De dónde salen dos familias de skills. Y qué pasa con los cambios fuera de git en cuatro proyectos. Algunas esperan desde ayer. ¿Cuál bloquea algo, y cuál puede esperar?</p>
</div>

Vigilar cansa más de lo que parece. En 1983, Lisanne Bainbridge escribió que nadie mantiene una atención eficaz sobre algo en lo que pasa poco «for more than about half an hour» ([Ironies of Automation](https://gwern.net/doc/sociology/technology/1983-bainbridge.pdf)). Hoy, según Anthropic, los usuarios de Claude Code aceptan el 93 % de las peticiones de permiso, y lo llama «approval fatigue» ([Anthropic, 2026](https://anthropic.com/engineering/claude-code-auto-mode)).

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · la bandeja de decisiones</p>
<p class="escena-contexto">Es el momento del día que has reservado para decidir.</p>
<div class="turno"><p class="ponente">Claude<small>propone</small></p><p>Tienes siete preguntas. Una bloquea trabajo: el siguiente paso de la aplicación educativa. Dos se responden en un minuto: el registro de cambios y el origen de las skills. Las otras cuatro no frenan nada esta semana.</p></div>
<div class="turno"><p class="ponente">Tú<small>decide</small></p><p>Primero la pantalla de revisión. Lo de la clave lo hablo con el cliente.</p></div>
<div class="turno"><p class="ponente">Claude<small>registra</small></p><p>Anotado en el tablero. La de la clave pasa a esperar al cliente, con la fecha de hoy.</p></div>
<p class="escena-pie">Diálogo imaginado.</p>
</div>

La bandeja junta en un solo sitio lo que todos tus proyectos esperan de ti. Claude separa lo que bloquea de lo que puede esperar y sigue con lo que no depende de ti. Tú eliges cuándo la abres. Un buen día es aquel en el que se cumple tu plan y no el de tus agentes ([Meyer y otros, Microsoft Research](https://www.microsoft.com/en-us/research/?p=578803)).

---

## Cómo delegas sin revisar cada línea

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 6 · El informe del gemelo</p>
<p>El gemelo digital del dispositivo tiene un informe de verificación de la semana pasada. Dice que pasan 200 de 200 pruebas en Python, 23 de ellas entre cinco procesos reales. La interfaz tiene 37 ficheros y pasa sus 34 pruebas. Nadie puede leer todo eso cada vez. ¿Cómo sabes qué funciona?</p>
</div>

Lo sabes por el informe, no por haberlo leído entero. Esa es la idea: **evidencias en lugar de control**. Cada devslice se cierra contra sus criterios de aceptación, con un informe que dice qué se comprobó y cómo. Si alguna prueba falla, la devslice no se da por cerrada.

Hace falta, porque la confianza a ojo engaña. En la encuesta de Stack Overflow de 2025, solo el 3,1 % confía mucho en la precisión de la IA. Dos de cada tres sufren soluciones «almost right, but not quite» ([Stack Overflow, 2025](https://survey.stackoverflow.co/2025/ai)).

Delegar también cambia lo que entiendes. En un ensayo de Anthropic, quien aprendió con IA sacó un 17 % menos en comprensión ([Anthropic, 2026](https://www.anthropic.com/research/AI-assistance-coding-skills)). Por eso la SF dice qué hace Claude solo y qué te pide a ti. Y deja para tu rato de aprender lo que quieres entender de verdad.

---

## Cuántos instrumentos a la vez

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 7 · Lo que suena hoy</p>
<p>Al acabar la mañana suenan muchas cosas a la vez. La aplicación educativa, que espera. El dispositivo, con su perfil pendiente. Cinco propuestas nuevas, una investigación en cinco frentes y esta visión. Y la charla, que tiene fecha. ¿Cuántas puede tocar bien una sola persona?</p>
</div>

Quien más lo ha probado lo cuenta igual. Willison: «I can fire up four agents in parallel… And by like 11 AM, I am wiped out for the day» ([Lenny's Podcast, 2026](https://simonwillison.net/2026/Apr/2/lennys-podcast/)). Constantin Gonzalez, que trabaja por su cuenta, describe la otra cara: «three streams of steady progress, one me». Y advierte de que cada tarea a medias «keeps simmering in your head, too» ([Gonzalez, julio de 2026](https://constantin.glez.de/posts/2026-07-16-why-working-with-ai-agents-is-so-tiring-and-what-to-do-about-it/)).

Los techos que se citan coinciden: de dos a cuatro frentes simultáneos. Mitchell Hashimoto, creador de varias herramientas muy usadas, va más lejos. Apaga los avisos del agente: «Don't let the agent notify you» ([Hashimoto, febrero de 2026](https://mitchellh.com/writing/my-ai-adoption-journey)). Y da una regla práctica: «If I'm coding, I want an agent planning. If they're coding, I want to be reviewing» ([The Pragmatic Engineer, 2026](https://newsletter.pragmaticengineer.com/i/188952833/key-observation-from-mitchell)).

La SF lleva la cuenta por ti. Un frente es una devslice en desarrollo, una visión abierta o una investigación en marcha, en cualquier proyecto. Tú fijas el tope. Antes de abrir uno nuevo, Claude te enseña cuántos hay y qué se cerraría antes. No es una prohibición: es la partitura que te recuerda qué estás tocando.

---

## Un solo centro

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 8 · Tres herramientas, tres memorias</p>
<p>La aplicación educativa empezó en ChatGPT Work. El formulario de una aplicación clínica tiene ocho pantallas en un lienzo de Claude Design. Y todo se desarrolla en Claude Code. Cada herramienta recuerda lo suyo, y ninguna sabe lo que saben las otras. Cada semana, además, sale una nueva. ¿Dónde vive tu trabajo?</p>
</div>

Vive en un solo sitio: **Claude Code es el sistema nervioso central**, y la SF, el arnés que lo une todo. El hombre orquesta puede tocar instrumentos de otras marcas, pero todos se atan al mismo cuerpo. Lo que se hace fuera se trae al proyecto. Lo nuevo entra primero como candidato y se prueba en un caso real antes de adoptarse.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 46 560 424" width="100%" role="img" aria-label="Claude Code conectado al backend de la SF" style="font-family:var(--fuente-texto);display:block">
<defs><marker id="hoA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#004d47"/></marker></defs>
<rect x="14" y="54" width="164" height="52" rx="8" fill="none" stroke="#00726b" stroke-width="1.5"/><text x="96" y="76" text-anchor="middle" font-size="14" font-weight="700" fill="#004d47">App educativa</text><text x="96" y="94" text-anchor="middle" font-size="11.5" fill="#555">su sesión de Claude Code</text>
<rect x="198" y="54" width="164" height="52" rx="8" fill="none" stroke="#00726b" stroke-width="1.5"/><text x="280" y="76" text-anchor="middle" font-size="14" font-weight="700" fill="#004d47">Dispositivo</text><text x="280" y="94" text-anchor="middle" font-size="11.5" fill="#555">su sesión de Claude Code</text>
<rect x="382" y="54" width="164" height="52" rx="8" fill="none" stroke="#00726b" stroke-width="1.5"/><text x="464" y="76" text-anchor="middle" font-size="14" font-weight="700" fill="#004d47">App clínica</text><text x="464" y="94" text-anchor="middle" font-size="11.5" fill="#555">su sesión de Claude Code</text>
<line x1="96" y1="106" x2="96" y2="122" stroke="#004d47" stroke-width="2"/><line x1="280" y1="106" x2="280" y2="122" stroke="#004d47" stroke-width="2"/><line x1="464" y1="106" x2="464" y2="122" stroke="#004d47" stroke-width="2"/><line x1="96" y1="122" x2="464" y2="122" stroke="#004d47" stroke-width="2"/>
<line x1="150" y1="122" x2="150" y2="200" stroke="#004d47" stroke-width="2" marker-end="url(#hoA)"/>
<text x="160" y="150" font-size="12" font-weight="700" fill="#00726b">eventos</text><text x="160" y="166" font-size="11.5" fill="#555">empieza, espera,</text><text x="160" y="181" font-size="11.5" fill="#555">termina</text>
<line x1="410" y1="204" x2="410" y2="126" stroke="#004d47" stroke-width="2" marker-end="url(#hoA)"/>
<text x="300" y="150" font-size="12" font-weight="700" fill="#00726b">contexto</text><text x="300" y="166" font-size="11.5" fill="#555">al abrir cada</text><text x="300" y="181" font-size="11.5" fill="#555">sesión</text>
<rect x="14" y="206" width="532" height="88" rx="8" fill="#00726b"/>
<text x="34" y="236" font-size="16" font-weight="700" fill="#fff">El backend de la SF</text>
<text x="34" y="258" font-size="12.5" fill="#e0f4f3">el tablero, la daily, la bandeja de decisiones</text>
<text x="34" y="278" font-size="12.5" fill="#e0f4f3">los informes de cierre y el tope de frentes</text>
<line x1="60" y1="358" x2="60" y2="300" stroke="#004d47" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#hoA)"/>
<text x="14" y="376" font-size="12" font-weight="700" fill="#00726b">de fuera, se trae</text>
<text x="14" y="392" font-size="11.5" fill="#555">ChatGPT, Claude Design…</text>
<line x1="280" y1="298" x2="280" y2="382" stroke="#004d47" stroke-width="2" marker-end="url(#hoA)"/>
<text x="292" y="336" font-size="12" font-weight="700" fill="#00726b">un resumen y una bandeja</text>
<text x="292" y="352" font-size="11.5" fill="#555">no veinte avisos sueltos</text>
<rect x="200" y="388" width="160" height="44" rx="22" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<text x="280" y="415" text-anchor="middle" font-size="15" font-weight="700" fill="#004d47">Tú</text>
<text x="280" y="458" text-anchor="middle" font-size="12" font-style="italic" fill="#888">organizado por proyecto, no por sesión</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Ilustrativo. Claude Code pone la mecánica; el backend de la SF pone el modelo y las reglas.</figcaption>
</figure>

Claude Code ya ofrece casi toda la mecánica. Sus hooks avisan cuando una sesión empieza, espera o termina, y pueden añadir contexto antes del primer mensaje. Un servidor MCP deja que cualquier sesión consulte y actualice el tablero. Y un plugin lo empaqueta todo para instalarlo una vez en todos los proyectos.

Lo que Claude Code no sabe es cómo va tu cartera. Su vista de agentes ordena sesiones; la SF ordena proyectos, con su visión, sus frentes y lo que esperan de ti. Ninguna herramienta registra tu atención ni tus cambios de proyecto, así que el backend los deduce del ir y venir de las sesiones.

#### Los puntos de conexión con Claude Code

Según su documentación, consultada el 26 de octubre de 2026 ([hooks](https://code.claude.com/docs/en/hooks.md), [MCP](https://code.claude.com/docs/en/mcp.md), [uso programático](https://code.claude.com/docs/en/headless.md), [tareas programadas](https://code.claude.com/docs/en/routines.md), [plugins](https://code.claude.com/docs/en/plugins.md), [vista de agentes](https://code.claude.com/docs/en/agent-view.md)):

- **Hooks de usuario.** En `~/.claude/settings.json` valen para todos los proyectos de la máquina. Cada evento lleva el identificador de sesión y la carpeta. Pueden ser un comando o una llamada HTTP al backend.
- **Al empezar una sesión.** El hook `SessionStart` añade contexto antes del primer mensaje: el estado del proyecto, la devslice activa y la pregunta de su visión.
- **Cuando una sesión espera.** El hook `Notification` dice si pide permiso, está inactiva o necesita una respuesta. Alimenta la bandeja.
- **Al terminar.** `Stop` y `TaskCompleted` dan el último mensaje y pueden impedir el cierre si fallan las pruebas. Sirven para los informes de cierre.
- **MCP de ámbito usuario.** El tablero, como herramienta disponible en todas las sesiones.
- **Uso programático.** `claude -p` con salida JSON y `--resume` permite preguntar a una sesión qué cambió. Sirve para escribir la daily.
- **Tareas programadas.** Lanzan la daily a una hora fija. Las de la nube no ven los hooks ni los MCP locales.
- **Plugins.** Empaquetan skills, hooks y MCP para instalar la SF de una vez.
- **Límites.** Las sesiones interactivas no aparecen en la vista de agentes hasta pasarlas a segundo plano. Ningún evento mide la atención de la persona.

---

## En qué se diferencia de lo que ya existe

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 9 · ¿Ya lo ha resuelto alguien?</p>
<p>Antes de construir nada, la investigación de hoy busca en cinco frentes: estudios, testimonios y herramientas. Algunas ya avisan cuando un agente te espera. Otras coordinan decenas de agentes en paralelo. ¿Alguna se ocupa de ti?</p>
</div>

Alrededor hay tres familias, y en varias cosas van por delante:

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 430" width="100%" role="img" aria-label="Familias de herramientas y SoftwareFactory" style="font-family:var(--fuente-texto);display:block">
<text x="14" y="30" font-size="14.5" font-weight="700" fill="#004d47">Coordinar agentes<tspan font-size="12.5" font-weight="400" fill="#888">   Vibe Kanban, Conductor, Agent HQ, Codex</tspan></text>
<text x="14" y="52" font-size="12.5" fill="#1a1a1a">muchos agentes en paralelo, cada uno en su rama</text>
<text x="14" y="70" font-size="12.5" fill="#888">ven sesiones y agentes, no proyectos con su visión</text>
<line x1="14" y1="88" x2="546" y2="88" stroke="#e0f4f3" stroke-width="2"/>
<text x="14" y="118" font-size="14.5" font-weight="700" fill="#004d47">Métodos de especificación<tspan font-size="12.5" font-weight="400" fill="#888">   Spec Kit, Kiro, BMAD, Superpowers</tspan></text>
<text x="14" y="140" font-size="12.5" fill="#1a1a1a">especificar, planificar y verificar con rigor</text>
<text x="14" y="158" font-size="12.5" fill="#888">cuidan el artefacto de un proyecto</text>
<line x1="14" y1="176" x2="546" y2="176" stroke="#e0f4f3" stroke-width="2"/>
<text x="14" y="206" font-size="14.5" font-weight="700" fill="#004d47">Claude Code<tspan font-size="12.5" font-weight="400" fill="#888">   de Anthropic</tspan></text>
<text x="14" y="228" font-size="12.5" fill="#1a1a1a">avisos, vista de sesiones, hooks, MCP y plugins</text>
<text x="14" y="246" font-size="12.5" fill="#888">pone la mecánica para todos tus proyectos</text>
<line x1="280" y1="266" x2="280" y2="290" stroke="#00726b" stroke-width="2"/>
<rect x="14" y="296" width="532" height="124" rx="8" fill="#00726b"/>
<text x="34" y="326" font-size="16" font-weight="700" fill="#fff">SoftwareFactory</text>
<text x="34" y="348" font-size="12.5" fill="#e0f4f3">tu cartera vista desde ti: cómo va cada proyecto</text>
<text x="34" y="368" font-size="12.5" fill="#e0f4f3">la visión como brújula y un tope de frentes abiertos</text>
<text x="34" y="388" font-size="12.5" fill="#e0f4f3">los seis trabajos ordenados en la daily</text>
<text x="34" y="408" font-size="12.5" fill="#e0f4f3">pedirte menos atención, sobre la mecánica de Claude Code</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Tres familias que optimizan la producción, y una que se ocupa de quien la dirige.</figcaption>
</figure>

Van por delante en lo que ya funciona. La app de Codex distingue los chats que están en marcha, sin leer o esperando tu respuesta ([Codex](https://learn.chatgpt.com/codex/notifications)). La vista de agentes de Claude Code agrupa lo que necesita una respuesta ([Claude Code](https://code.claude.com/docs/en/agent-view.md)). Superpowers exige evidencias antes de dar algo por hecho ([Superpowers](https://github.com/obra/superpowers)).

Y la SF, hoy, es una idea con piezas sueltas. El tablero existe, pero aún no tiene tus proyectos. La daily, la bandeja y el tope están por construir. Factory usa incluso el nombre «software factory», aunque para la ejecución autónoma en empresas ([Factory](https://factory.ai/news/software-factory)).

Lo que la distingue es el punto de vista. Casi todo está pensado para equipos y para uno o dos proyectos ([informe de la investigación](../../referencias/reports/Fricciones%20humanas%20del%20desarrollo%20con%20IA.md)). Nadie ofrece la cartera vista desde la persona, ni la comprobación contra una visión, ni un tope pensado para quien revisa. Tampoco hay estudios sobre tu perfil. Por eso la SF registrará sus propios datos desde el principio: frentes abiertos, decisiones pendientes y cierres.

---

## De vuelta al caso

<div class="caso">
<p class="caso-etiqueta">El caso · epílogo · la daily de mañana</p>
<p>Mañana la daily empezará igual, pero el resumen estará escrito antes de que preguntes. Cada proyecto dirá cómo va frente a su visión, y la bandeja, qué espera de ti. El tablero contará los frentes abiertos. La idea de esta mañana tendrá su sitio: el banco de ideas o, como esta visión, un proyecto aceptado.</p>
<p>Lo que la SF no decide es lo que te toca: qué proyecto suena hoy, qué idea se guarda, cuándo se cierra un frente y qué no puede esperar. <strong>La SF lleva la cuenta y propone; el director de la orquesta sigues siendo tú.</strong></p>
</div>

---

## Anexo: el caso y sus fuentes

### Qué es real

El caso se inspira en una mañana real de trabajo con la SF, en octubre de 2026: la frase «dime qué tenemos pendiente», las siete preguntas abiertas, los commits y las propuestas de esa mañana, la investigación en cinco frentes (en `docs/referencias/`) y la idea de escribir más de una visión. Los proyectos se nombran por su tipo y sin datos de su estado.

### Qué es ilustrativo

Las escenas son imaginadas: el resumen de retorno, la bandeja y sus respuestas. El tope de cuatro frentes es un ejemplo. El día por tipo de trabajo del resumen operativo es una propuesta, no un horario. La daily del epílogo describe lo que la SF hará, no algo que ya ocurra. La daily, la bandeja, el banco de ideas, el tope y el backend conectado a Claude Code están por construir.

### Fuentes

Consultadas el 26 de octubre de 2026. Cada cita se ha cotejado con su fuente original ([verificación](../../referencias/research_notes/Fricciones%20humanas%20del%20desarrollo%20con%20IA/verificacion_citas.md)). El detalle está en el [informe de la investigación](../../referencias/reports/Fricciones%20humanas%20del%20desarrollo%20con%20IA.md).

- Demirer, Musolff y Yang, [NBER w35275](https://www.nber.org/papers/w35275), 2026. Según la propia página, dos de los autores son consultores pagados por Microsoft.
- Faros AI, [AI Acceleration Whiplash](https://www.faros.ai/research/ai-acceleration-whiplash), 2026. Informe de un proveedor.
- METR, [estudio con desarrolladores expertos](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/), 10 de julio de 2025, y [actualización](https://metr.org/blog/2026-02-24-uplift-update/), 24 de febrero de 2026. La actualización no invierte el resultado: METR dice que no puede medirlo bien, aunque cree probable que ahora se vaya más rápido.
- Parnin y Rugaber, [Resumption strategies for interrupted programming tasks](https://sites.cc.gatech.edu/reverse/repository/resumptionstrategies.pdf), 2010.
- Bainbridge, [Ironies of Automation](https://gwern.net/doc/sociology/technology/1983-bainbridge.pdf), 1983.
- Anthropic, [Claude Code auto mode](https://anthropic.com/engineering/claude-code-auto-mode), 25 de marzo de 2026, y [AI assistance and coding skills](https://www.anthropic.com/research/AI-assistance-coding-skills), 29 de enero de 2026.
- Meyer y otros, [días buenos de los desarrolladores](https://www.microsoft.com/en-us/research/?p=578803), Microsoft Research.
- Stack Overflow, [Developer Survey 2025, IA](https://survey.stackoverflow.co/2025/ai).
- Simon Willison, [notas de Lenny's Podcast](https://simonwillison.net/2026/Apr/2/lennys-podcast/), 2 de abril de 2026.
- Constantin Gonzalez, [Why working with AI agents is so tiring](https://constantin.glez.de/posts/2026-07-16-why-working-with-ai-agents-is-so-tiring-and-what-to-do-about-it/), 16 de julio de 2026.
- Mitchell Hashimoto, [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey), 5 de febrero de 2026, y The Pragmatic Engineer, [entrevista](https://newsletter.pragmaticengineer.com/i/188952833/key-observation-from-mitchell), 25 de febrero de 2026.
- Herramientas: [Codex](https://learn.chatgpt.com/codex/notifications), [Claude Code](https://code.claude.com/docs/en/agent-view.md), [Superpowers](https://github.com/obra/superpowers), [Factory](https://factory.ai/news/software-factory), [Vibe Kanban](https://vibekanban.com/docs/getting-started), [Conductor](https://www.conductor.build/docs/), [GitHub Agent HQ](https://github.blog/news-insights/company-news/welcome-home-agents/), [Spec Kit](https://github.com/github/spec-kit), [Kiro](https://kiro.dev/docs/steering/), [BMAD](https://github.com/bmad-code-org/BMAD-METHOD).

---

*Documento de visión de SoftwareFactory: el hombre orquesta — 2026-10-26.*
