# SoftwareFactory: tu forma de construir, convertida en fábrica

<div class="caso">
<p class="caso-etiqueta">El caso · prólogo · JKanban</p>
<p>JKanban ya funciona. Va por la versión 7.0.0, suma 28 commits y organiza el trabajo en <strong>proyectos, columnas y tareas</strong>. Tiene arquitectura limpia, SQL escrito a mano y diez archivos de pruebas. En su base de datos hay un único proyecto, <strong>Prueba_1</strong>. Ahora le toca su funcionalidad más ambiciosa: que Claude Code consulte el tablero, cree tareas y mueva tarjetas. Hasta hoy, cada proyecto empezaba de cero, con sus propias reglas y lo aprendido guardado en su rincón. Esta vez quieres otra cosa: <strong>¿cómo consigo que esta funcionalidad nazca preparada, probada y visible en el propio tablero, y que lo que aprenda sirva al proyecto siguiente?</strong></p>
</div>

## Resumen operativo

Para eso existe **SoftwareFactory**: tu forma de construir aplicaciones con Claude Code, convertida en método y herramientas que se reutilizan. «Conectar JKanban con Claude Code» no empieza con código. Empieza con una devslice preparada: qué debe hacer, cómo se comprobará y qué tareas lleva, todo anotado en el tablero.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 520" width="100%" role="img" aria-label="Recorrido de JKanban por el método, de la visión al cierre" style="font-family:'DM Sans',Arial,sans-serif;display:block">
<text x="14" y="24" font-size="15.5" font-weight="700" fill="#004d47">El recorrido de JKanban por la fábrica</text>
<line x1="14" y1="38" x2="546" y2="38" stroke="#e0f4f3" stroke-width="2"/>
<line x1="34" y1="64" x2="34" y2="482" stroke="#b2deda" stroke-width="2"/>
<circle cx="34" cy="64" r="7" fill="#00726b"/><text x="56" y="62" font-size="14.5" font-weight="700" fill="#004d47">Visión</text><text x="56" y="80" font-size="12.5" fill="#555">para qué existe JKanban y para quién</text>
<circle cx="34" cy="124" r="7" fill="#00726b"/><text x="56" y="122" font-size="14.5" font-weight="700" fill="#004d47">Especificación funcional global</text><text x="56" y="140" font-size="12.5" fill="#555">proyectos, columnas, tareas… y lo que pide la fábrica</text>
<circle cx="34" cy="184" r="7" fill="#00726b"/><text x="56" y="182" font-size="14.5" font-weight="700" fill="#004d47">Definición técnica</text><text x="56" y="200" font-size="12.5" fill="#555">FastAPI, SQLite y SQL a mano: ya elegidos</text>
<circle cx="34" cy="244" r="7" fill="#00726b"/><text x="56" y="242" font-size="14.5" font-weight="700" fill="#004d47">Devslices</text><text x="56" y="260" font-size="12.5" fill="#555">«Conectar JKanban con Claude Code», entre otras</text>
<circle cx="34" cy="304" r="7" fill="#00726b"/><text x="56" y="302" font-size="14.5" font-weight="700" fill="#004d47">Preparación</text><text x="56" y="320" font-size="12.5" fill="#555">criterios, pruebas previstas y tareas</text>
<circle cx="34" cy="364" r="7" fill="#00726b"/><text x="56" y="362" font-size="14.5" font-weight="700" fill="#004d47">Desarrollo</text><text x="56" y="380" font-size="12.5" fill="#555">pruebas, después lógica y datos, después interfaz</text>
<circle cx="34" cy="424" r="7" fill="#00726b"/><text x="56" y="422" font-size="14.5" font-weight="700" fill="#004d47">Cierre</text><text x="56" y="440" font-size="12.5" fill="#555">evidencias, informe y tarjeta terminada</text>
<path d="M436,236 H448 V446 H436" fill="none" stroke="#00726b" stroke-width="2"/>
<text x="458" y="330" font-size="12.5" font-weight="700" fill="#00726b">el tablero</text>
<text x="458" y="347" font-size="12.5" fill="#555">registra</text>
<text x="458" y="364" font-size="12.5" fill="#555">cada paso</text>
<text x="34" y="508" font-size="12.5" font-style="italic" fill="#888">y si surge una mejora general, va a la fábrica, no a JKanban</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">El mismo recorrido para cualquier proyecto. Desde que existen las devslices, el tablero sigue cada paso.</figcaption>
</figure>

Durante el trabajo, Claude no adivina el estado: lo consulta en JKanban y no da nada por anotado hasta que el tablero lo confirma. Las skills que usa salen de un único sitio, con su versión y su procedencia. Y cuando algo se puede hacer mejor, la fábrica lo propone, pero no cambia nada sin tu aprobación.

El resto del documento sigue a JKanban capítulo a capítulo, desde que entra en la fábrica hasta que su primera devslice queda cerrada.

---

## Por qué una fábrica

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 1 · Antes de entrar</p>
<p>Antes de tocar nada, miras <code>D:\Projectes</code>. PoseTracker tiene su «doctrina», OncoCore sus propias instrucciones y JKanban guarda en su <code>CLAUDE.md</code> la lección de la función <code>jsq()</code> contra el XSS. Cada proyecto ha aprendido algo, y nada de eso ha llegado a los demás. ¿Cuánto se pierde así?</p>
</div>

Hoy trabajas como un buen artesano: cada pieza sale bien, pero cada taller tiene sus herramientas y sus notas. Una fábrica no es menos cuidadosa; es un taller con **recetario común**. Los pasos son los mismos en cada proyecto, las herramientas están en un sitio conocido y lo que se aprende en uno pasa al siguiente.

Un detalle lo muestra bien. Este documento se ha generado con tu skill de visión, y su script importa código de OncoCore. Si OncoCore no estuviera en este ordenador, la skill no funcionaría. Las herramientas buenas merecen un sitio propio, con su versión y sus dependencias a la vista.

---

## Cómo empieza un proyecto

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 2 · Un documento para empezar</p>
<p>JKanban entra en la fábrica, y lo primero no es abrir el código. Es escribir su documento de visión: para qué existe y qué podría llegar a ser. Tiene siete documentos técnicos, pero ninguno cuenta por qué merece la pena. ¿Por dónde se empieza?</p>
</div>

Todo proyecto empieza igual: con un **documento de visión** pensado para personas, no para programadores. Lo prepara tu skill `documento_vision` en una conversación de cuatro fases. Primero se valora la idea. Después se acuerdan la visión y las secciones. Luego se escribe y, al final, se afina sobre lo escrito. La visión es tuya: Claude propone, tú corriges.

<figure style="margin:1.6rem 0 1.2rem;">
<div style="border:1px solid #b2deda;border-radius:8px;padding:1rem 1.2rem;background:#fff;">
<p style="font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:#00726b;margin:0 0 .5rem;font-weight:700;">Documento de visión de JKanban · primera página</p>
<p style="font-size:1.15rem;font-weight:700;color:#004d47;margin:0 0 .6rem;">JKanban: el trabajo de cada proyecto, a la vista</p>
<p style="margin:0 0 .5rem;font-style:italic;">Tres proyectos abiertos a la vez. Las tareas de cada uno están repartidas entre notas, correos y la memoria. Cuando alguien pregunta «¿cómo va?», la respuesta tarda.</p>
<p style="margin:0;">JKanban reúne ese trabajo en un tablero por proyecto, con columnas, tareas, subtareas y responsables. Cualquiera del equipo ve de un vistazo qué falta, quién lo lleva y qué está bloqueado.</p>
</div>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Así podría abrir su documento de visión: un caso que se reconoce, y en dos frases, lo que ofrece. Ilustrativo.</figcaption>
</figure>

Con la visión acordada llegan la especificación funcional global y la definición técnica. En JKanban, buena parte ya existe: su API, su modelo de datos y sus reglas están documentados. La fábrica no rehace ese trabajo: **lo adopta y lo completa** con lo que pide el método.

---

## Cómo nace una funcionalidad

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 3 · Antes de la primera línea</p>
<p>«Conectar JKanban con Claude Code» ya está planificada como devslice. Pero planificada no es preparada: falta decidir qué cuenta como hecho. ¿Qué tiene que pasar exactamente cuando Claude mueve una tarjeta?</p>
</div>

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · preparando la devslice</p>
<p class="escena-contexto">Martes. Tú y Claude afináis los criterios de aceptación.</p>
<div class="turno"><p class="ponente">Claude<small>propone</small></p><p>Criterio: Claude puede mover una tarea de columna. Prueba prevista: mover una tarea de Prueba_1 y leer su columna nueva.</p></div>
<div class="turno"><p class="ponente">Tú<small>matiza</small></p><p>Falta el caso malo. Si la tarea no existe, quiero verlo, no que me digas que está movida.</p></div>
<div class="turno"><p class="ponente">Claude<small>acepta</small></p><p>Segundo criterio, entonces: si JKanban devuelve <code>TaskNotFound</code>, el error se muestra tal cual y el movimiento no se da por hecho. Lo pruebo antes de escribir el código.</p></div>
<p class="escena-pie">Diálogo imaginado: muestra cómo se prepara una devslice, no una conversación real.</p>
</div>

Así nace cada funcionalidad: **primero se prepara**, con alcance, criterios, pruebas previstas y tareas. Después se escriben las pruebas y se construye empezando por la lógica y los datos. La interfaz llega al final, y se comprueba el recorrido completo. Las pruebas siguen vivas cuando la devslice se cierra, porque pertenecen a JKanban.

---

## Qué muestra el tablero

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 4 · El tablero responde</p>
<p>Las tareas de la devslice ya están en JKanban. Claude empieza a trabajar y quiere mover la primera a «En desarrollo». Es la primera vez que el tablero habla con Claude. ¿Y si algo falla?</p>
</div>

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · una operación que no se confirma</p>
<p class="escena-contexto">Miércoles. Claude intenta actualizar el tablero.</p>
<div class="turno"><p class="ponente">Claude<small>pide</small></p><p>Mover «Escribir pruebas del movimiento» a En desarrollo.</p></div>
<div class="turno arnes"><p class="ponente">JKanban<small>responde</small></p><p>403 · UserNotInProject: el usuario no tiene acceso al proyecto.</p></div>
<div class="turno"><p class="ponente">Claude<small>informa</small></p><p>No he podido mover la tarea: mi usuario no es miembro del proyecto. Sigue en Preparada. ¿Me añades al equipo?</p></div>
<p class="escena-pie">Diálogo imaginado. El error y su código existen en JKanban; la situación es un ejemplo.</p>
</div>

El tablero es tu **ventana permanente** al trabajo. Cada devslice tiene sus tareas, y cada tarea su estado, sus dependencias y sus bloqueos, con el motivo a la vista. Claude lo consulta para retomar después de una pausa y lo actualiza mientras trabaja. Hay una regla que no se negocia: nada está anotado hasta que JKanban lo confirma. Un error se ve; no se esconde.

---

## De dónde salen las herramientas

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 5 · La caja de herramientas</p>
<p>Para construir la conexión, Claude necesita skills: preparar devslices, diseñar pruebas, operar el tablero. ¿Las de qué carpeta? ¿En qué versión?</p>
</div>

Todas las skills de la fábrica, propias o de otros autores, viven en un solo sitio: la carpeta `skills/` de SoftwareFactory. Cada una lleva su procedencia, su licencia y su versión. Las externas se guardan enteras, aunque no se toquen, para que ninguna actualización ajena cambie nada sin que lo decidas.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 345" width="100%" role="img" aria-label="De la carpeta skills a cada proyecto, con versión" style="font-family:'DM Sans',Arial,sans-serif;display:block">
<defs><marker id="vb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#004d47"/></marker></defs>
<ellipse cx="280" cy="26" rx="120" ry="14" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<path d="M160,26 V106 A120,14 0 0 0 400,106 V26" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<ellipse cx="280" cy="26" rx="120" ry="14" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<text x="280" y="58" text-anchor="middle" font-size="15" font-weight="700" fill="#004d47">skills/ de SoftwareFactory</text>
<text x="280" y="78" text-anchor="middle" font-size="12" fill="#555">propias y externas, con procedencia</text>
<text x="280" y="95" text-anchor="middle" font-size="12" fill="#555">plantillas y perfiles técnicos</text>
<line x1="280" y1="124" x2="280" y2="152" stroke="#004d47" stroke-width="2" marker-end="url(#vb)"/>
<rect x="150" y="156" width="260" height="44" rx="22" fill="#00726b"/>
<text x="280" y="176" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">una versión estable</text>
<text x="280" y="192" text-anchor="middle" font-size="11.5" fill="#e0f4f3">evaluada antes de publicarse</text>
<line x1="280" y1="202" x2="280" y2="230" stroke="#004d47" stroke-width="2" marker-end="url(#vb)"/>
<text x="60" y="258" font-size="14.5" font-weight="700" fill="#004d47">JKanban</text><text x="250" y="258" font-size="12.5" fill="#555">sabe qué versión usa</text>
<text x="60" y="290" font-size="14.5" font-weight="700" fill="#004d47">OncoCore</text><text x="250" y="290" font-size="12.5" fill="#555">la misma u otra, a su ritmo</text>
<text x="60" y="322" font-size="14.5" font-weight="700" fill="#004d47">El próximo proyecto</text><text x="250" y="322" font-size="12.5" fill="#555">arranca con lo aprendido</text>
<line x1="40" y1="242" x2="40" y2="330" stroke="#b2deda" stroke-width="2"/>
<path d="M440,318 C548,318 548,60 404,60" fill="none" stroke="#00726b" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#vb)"/>
<text x="498" y="232" text-anchor="end" font-size="12" font-weight="700" fill="#00726b">mejora aprobada</text>
<text x="498" y="248" text-anchor="end" font-size="12" fill="#555">vuelve a la fuente</text>
<text x="498" y="264" text-anchor="end" font-size="12" fill="#555">como nueva versión</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Una sola fuente, versiones con nombre y un camino de vuelta para lo que se aprende.</figcaption>
</figure>

Las skills aportan técnica; tu método y el perfil de cada proyecto deciden la tecnología. Así ninguna pieza impone una metodología ajena. Y las skills con las que trabaja un agente dentro de un producto se guardan aparte, para que mejorar la fábrica no cambie sin querer cómo funciona una aplicación.

---

## Cómo aprende la fábrica

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 6 · Una lección que viaja</p>
<p>Al revisar la interfaz de la conexión, Claude vuelve a comprobar a mano los escapes <code>esc()</code> y <code>jsq()</code>, igual que en las correcciones de JKanban contra el XSS. Es la segunda vez que se repite el mismo cuidado. ¿Debería saberlo ya la fábrica?</p>
</div>

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · una propuesta de mejora</p>
<div class="turno"><p class="ponente">Claude<small>propone</small></p><p>Mejora para SoftwareFactory: que la revisión de interfaces web compruebe siempre el escape del contenido de usuario. Origen: JKanban, devslice «Conectar JKanban con Claude Code». La registro en el proyecto SoftwareFactory y espero tu aprobación.</p></div>
<div class="turno"><p class="ponente">Tú<small>decide</small></p><p>Regístrala. La miro el viernes.</p></div>
<p class="escena-pie">Diálogo imaginado: la mejora es un ejemplo, no una propuesta registrada.</p>
</div>

La fábrica tiene una tarea que nunca se cierra: **Mejorar la Software Factory**. Mientras trabaja en cualquier proyecto, Claude observa fricciones, errores repetidos y pasos de más. Cada mejora general va al proyecto SoftwareFactory del tablero, con su origen y su evidencia. Lo que es propio de JKanban se queda en JKanban.

Proponer no es cambiar. Ninguna mejora se aplica ni se distribuye sin tu aprobación expresa. La fábrica aprende rápido, pero el método sigue siendo tuyo.

---

## En qué se diferencia de lo que ya existe

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 7 · Mirar alrededor</p>
<p>Mientras la conexión avanza, te preguntas si no habría bastado con instalar algo ya hecho. Hay marcos de trabajo con cientos de miles de estrellas en GitHub. ¿Por qué construir la tuya?</p>
</div>

La idea de una fábrica de software personal se inspira en el vídeo de Eric Risco *Programar con agentes ya no basta: monta tu Software Factory*. Alrededor hay tres familias de propuestas, cada una con su propio método:

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 410" width="100%" role="img" aria-label="Familias de propuestas y SoftwareFactory" style="font-family:'DM Sans',Arial,sans-serif;display:block">
<text x="14" y="30" font-size="14.5" font-weight="700" fill="#004d47">Kits de especificación<tspan font-size="12.5" font-weight="400" fill="#888">   Spec Kit, de GitHub</tspan></text>
<text x="14" y="52" font-size="12.5" fill="#1a1a1a">especificar → planificar → tareas → implementar</text>
<text x="14" y="70" font-size="12.5" fill="#888">su medida es la especificación de cada funcionalidad</text>
<line x1="14" y1="88" x2="546" y2="88" stroke="#e0f4f3" stroke-width="2"/>
<text x="14" y="118" font-size="14.5" font-weight="700" fill="#004d47">Bibliotecas de skills con método<tspan font-size="12.5" font-weight="400" fill="#888">   Superpowers</tspan></text>
<text x="14" y="140" font-size="12.5" fill="#1a1a1a">planificar, pruebas primero, verificar antes de terminar</text>
<text x="14" y="158" font-size="12.5" fill="#888">disciplina de trabajo con el método de su autor</text>
<line x1="14" y1="176" x2="546" y2="176" stroke="#e0f4f3" stroke-width="2"/>
<text x="14" y="206" font-size="14.5" font-weight="700" fill="#004d47">Equipos de agentes simulados<tspan font-size="12.5" font-weight="400" fill="#888">   BMAD</tspan></text>
<text x="14" y="228" font-size="12.5" fill="#1a1a1a">analista, jefe de producto, arquitecto, desarrollador…</text>
<text x="14" y="246" font-size="12.5" fill="#888">reparte el trabajo en papeles de un equipo ágil</text>
<line x1="280" y1="266" x2="280" y2="290" stroke="#00726b" stroke-width="2"/>
<rect x="14" y="296" width="532" height="104" rx="8" fill="#00726b"/>
<text x="34" y="326" font-size="16" font-weight="700" fill="#fff">SoftwareFactory</text>
<text x="34" y="348" font-size="12.5" fill="#e0f4f3">tu método: visión, devslices preparadas, backend primero</text>
<text x="34" y="368" font-size="12.5" fill="#e0f4f3">tu tablero como ventana, tus preferencias como perfil</text>
<text x="34" y="388" font-size="12.5" fill="#e0f4f3">piezas de otros, elegidas y guardadas con su procedencia</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Tres maneras de ordenar el trabajo con agentes, y la tuya, que puede tomar piezas de todas.</figcaption>
</figure>

Los productos del gráfico: [Spec Kit](https://github.github.com/spec-kit/), [Superpowers](https://github.com/obra/superpowers) y [BMAD](https://github.com/bmad-code-org/BMAD-METHOD).

Son buenas propuestas, y por eso no son rivales. Spec Kit [cumplió un año en agosto de 2026 y publicó su versión 1.0.0](https://github.github.com/spec-kit/history.html), con 38 agentes compatibles. Pero cada una trae su método, y tú ya tienes el tuyo. SoftwareFactory no adopta un marco entero: **toma las piezas que sirven a tu método**, como dos skills de Superpowers que son candidatas, y las guarda con su procedencia.

---

## De vuelta al caso

<div class="caso">
<p class="caso-etiqueta">El caso · epílogo</p>
<p>JKanban sigue siendo el mismo tablero, pero ahora habla con Claude. Su devslice se ha preparado antes de escribir código, se ha probado empezando por los datos y se ha seguido paso a paso en el propio tablero. Cuando algo falló, el error se vio. En el tablero hay además un proyecto nuevo, <strong>SoftwareFactory</strong>, con su tarea permanente y una primera propuesta que salió de JKanban.</p>
<p>Lo que la fábrica no decide es lo que te corresponde: si esa mejora se aplica, cuándo se publica una versión nueva y qué proyecto entra después. <strong>La fábrica prepara, construye y propone; las decisiones son tuyas.</strong></p>
</div>

---

## Anexo: el caso JKanban

### Qué es real

JKanban existe en `D:\Projectes\ExampleClaudeCode`. Es una aplicación web multiusuario con backend en FastAPI y SQLite, sin ORM, y frontend en JavaScript sin frameworks. Va por la versión 7.0.0 y tiene 28 commits. Organiza el trabajo en proyectos, grupos (columnas) y tareas, con subtareas, etiquetas, prioridades y roles. Tiene diez archivos de pruebas y siete documentos técnicos en `docs/`. Su base de datos contiene un único proyecto, Prueba_1, consultado el 25 de octubre de 2026.

Los errores de las escenas, `TaskNotFound` y `UserNotInProject`, son excepciones reales de JKanban (`docs/business-rules.md`). Las funciones `esc()` y `jsq()` y las correcciones contra el XSS constan en su `CLAUDE.md` y en su historial. La dependencia de la skill de visión respecto a OncoCore consta en su script `doc_to_html.py`.

### Qué es ilustrativo

La conexión de JKanban con Claude Code todavía no existe: es la funcionalidad que se planea construir. Los capítulos, sus días, las escenas y la propuesta de mejora son imaginados. La primera página del documento de visión de JKanban es un ejemplo, no un documento escrito. El proyecto SoftwareFactory todavía no existe en el tablero.

### Fuentes

Consultadas el 25 de octubre de 2026:

- Eric Risco, [*Programar con agentes ya no basta: monta tu Software Factory*](https://www.youtube.com/watch?v=p6nnqerea7w), YouTube.
- [Spec Kit](https://github.github.com/spec-kit/), de GitHub, y [su historia](https://github.github.com/spec-kit/history.html). Licencia MIT.
- [Superpowers](https://github.com/obra/superpowers), de Jesse Vincent. Licencia MIT.
- [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD), de BMad Code.

---

*Documento de visión de SoftwareFactory — 2026-10-25.*
