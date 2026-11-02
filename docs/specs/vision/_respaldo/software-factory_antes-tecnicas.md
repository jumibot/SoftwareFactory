# SoftwareFactory: tu forma de construir, convertida en fábrica

<div class="caso">
<p class="caso-etiqueta">El caso · prólogo · LecturaFàcil</p>
<p>LecturaFàcil ya tiene un sueño escrito: un documento de visión en el que una profesora de Filosofía da el mismo Kant a toda su clase. Yasmin lo recibe en Lectura Fácil, con glosario en árabe, y Pau, que tiene dislexia, con fondo crema y lectura en voz alta. No hay ni una línea de código. Será el <strong>proyecto piloto</strong> de la fábrica: el primero que se construye entero con el método. Hasta hoy, cada proyecto empezaba de cero, con sus propias reglas. Esta vez quieres otra cosa: <strong>¿cómo paso de este documento a una herramienta que funcione, sin perder nada por el camino, y que lo aprendido sirva al proyecto siguiente?</strong></p>
</div>

## Resumen operativo

Para eso existe **SoftwareFactory**: tu forma de construir aplicaciones con Claude Code, convertida en método y herramientas que se reutilizan. LecturaFàcil no pasará de la visión al código de golpe. Primero tendrá una especificación del conjunto, con su interfaz, y una definición técnica. Después se construirá por devslices: incrementos pequeños y completos, que se preparan uno a uno.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 520" width="100%" role="img" aria-label="Recorrido de LecturaFàcil por el método, de la visión al cierre" style="font-family:'DM Sans',Arial,sans-serif;display:block">
<text x="14" y="24" font-size="15.5" font-weight="700" fill="#004d47">El recorrido de LecturaFàcil por la fábrica</text>
<line x1="14" y1="38" x2="546" y2="38" stroke="#e0f4f3" stroke-width="2"/>
<line x1="34" y1="64" x2="34" y2="482" stroke="#b2deda" stroke-width="2"/>
<circle cx="34" cy="64" r="7" fill="#00726b"/><text x="56" y="62" font-size="14.5" font-weight="700" fill="#004d47">Visión<tspan font-size="12.5" font-weight="700" fill="#00726b">   ✓ escrita</tspan></text><text x="56" y="80" font-size="12.5" fill="#555">el mismo Kant para Yasmin, Pau y su clase</text>
<rect x="290" y="98" width="120" height="22" rx="11" fill="#00726b"/><text x="350" y="113" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">estás aquí</text>
<circle cx="34" cy="134" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="132" font-size="14.5" font-weight="700" fill="#004d47">Especificación funcional global</text><text x="56" y="150" font-size="12.5" fill="#555">funcionalidades, interfaz, recorridos, estados, criterios</text>
<circle cx="34" cy="194" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="192" font-size="14.5" font-weight="700" fill="#004d47">Definición técnica</text><text x="56" y="210" font-size="12.5" fill="#555">escritorio: Python, Tkinter, SQLite y un agente</text>
<circle cx="34" cy="254" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="252" font-size="14.5" font-weight="700" fill="#004d47">Devslices</text><text x="56" y="270" font-size="12.5" fill="#555">pequeñas: una o dos sesiones cada una</text>
<circle cx="34" cy="314" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="312" font-size="14.5" font-weight="700" fill="#004d47">Preparación</text><text x="56" y="330" font-size="12.5" fill="#555">criterios, pruebas previstas y tareas</text>
<circle cx="34" cy="374" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="372" font-size="14.5" font-weight="700" fill="#004d47">Desarrollo</text><text x="56" y="390" font-size="12.5" fill="#555">pruebas, después lógica y datos, después interfaz</text>
<circle cx="34" cy="434" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="432" font-size="14.5" font-weight="700" fill="#004d47">Cierre</text><text x="56" y="450" font-size="12.5" fill="#555">criterios comprobados, informe y tarjeta terminada</text>
<path d="M436,246 H448 V456 H436" fill="none" stroke="#00726b" stroke-width="2"/>
<text x="458" y="340" font-size="12.5" font-weight="700" fill="#00726b">el tablero</text>
<text x="458" y="357" font-size="12.5" fill="#555">registra</text>
<text x="458" y="374" font-size="12.5" fill="#555">cada paso</text>
<text x="34" y="508" font-size="12.5" font-style="italic" fill="#888">y si surge una mejora general, va a la fábrica, no a LecturaFàcil</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">El mismo recorrido sirve para cualquier proyecto. LecturaFàcil acaba de cerrar el primer paso.</figcaption>
</figure>

Mientras se construye, el estado vive en tu tablero, JKanban. Claude lo consulta y no da nada por anotado hasta que el tablero lo confirma. Cuando falta información, pregunta en lugar de inventar. Las skills que usa salen de un único sitio, con su versión y su procedencia. Y como LecturaFàcil llevará un agente de IA dentro, la fábrica cuida que el Claude que desarrolla y el Claude que adapta textos nunca se mezclen.

Cuando algo se puede hacer mejor, la fábrica lo propone, pero no cambia nada sin tu aprobación. El resto del documento sigue a LecturaFàcil capítulo a capítulo, desde la visión hasta sus primeras devslices cerradas. Es más largo de lo habitual a propósito: LecturaFàcil es el caso que ayuda a definir la propia fábrica.

---

## Por qué una fábrica

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 1 · Antes de empezar</p>
<p>Antes de dar el siguiente paso, miras <code>D:\Projectes</code>. PoseTracker tiene su «doctrina», OncoCore sus propias instrucciones y JKanban guarda en su <code>CLAUDE.md</code> la lección de la función <code>jsq()</code> contra el XSS. Cada proyecto ha aprendido algo, y nada de eso ha llegado a los demás. ¿Con qué reglas empezará LecturaFàcil?</p>
</div>

Hoy trabajas como un buen artesano: cada pieza sale bien, pero cada taller tiene sus herramientas y sus notas. Una fábrica no es menos cuidadosa; es un taller con **recetario común**. Los pasos son los mismos en cada proyecto, las herramientas están en un sitio conocido y lo que se aprende en uno pasa al siguiente.

También el orden es común. Todos los proyectos guardan su documentación igual: la visión, la especificación funcional, la técnica y las devslices en `docs/specs/`, las referencias en `docs/referencias/` y las decisiones en `docs/decisiones/`. Quien abre un proyecto sabe dónde buscar, y Claude también.

LecturaFàcil es el primero que nace así desde el principio. Por eso es el piloto: lo que funcione con él se queda en la fábrica, y lo que no, se corrige antes de publicar una versión estable.

---

## Cómo empieza un proyecto

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 2 · Un documento para empezar</p>
<p>LecturaFàcil empezó como empiezan todos: con dos documentos de referencia y una idea. Antes de hablar de pantallas o de bases de datos, había que contar por qué merece la pena. ¿Cómo se cuenta una idea para que otros la entiendan y la quieran?</p>
</div>

Todo proyecto empieza con un **documento de visión**, pensado para personas y no para programadores. Lo prepara tu skill `documento_vision` en una conversación de cuatro fases. Primero se valora la idea. Después se acuerdan la visión y las secciones. Luego se escribe y, al final, se afina sobre lo escrito. La visión es tuya: Claude propone y tú corriges.

<figure style="margin:1.6rem 0 1.2rem;">
<div style="border:1px solid #b2deda;border-radius:8px;padding:1rem 1.2rem;background:#fff;">
<p style="font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:#00726b;margin:0 0 .5rem;font-weight:700;">Documento de visión de LecturaFàcil · prólogo</p>
<p style="font-size:1.15rem;font-weight:700;color:#004d47;margin:0 0 .6rem;">LecturaFàcil: documento de visión</p>
<p style="margin:0;font-style:italic;">«Mañana empieza "¿Qué es la Ilustración?", de Kant: […]. En su grupo está Yasmin, que llegó de Marruecos hace cuatro meses y se pierde en "minoria d'edat" y "enteniment". También está Pau, que tiene dislexia y llega cansado al "Sapere aude!". […] ¿Cómo puede dar el mismo Kant a toda la clase sin bajar la exigencia?»</p>
</div>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Un fragmento real de su documento de visión: un caso que se reconoce y una pregunta que hay que responder. La historia que cuenta es ficticia.</figcaption>
</figure>

Esa pregunta es la brújula de todo lo que viene. Pero una brújula no es un plano: entre la visión y la primera línea de código hay mucho que definir.

---

## Qué se define antes de construir

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 3 · Lo que la visión no dice</p>
<p>La visión de LecturaFàcil emociona, pero deja muchas preguntas sin respuesta. ¿Qué ve el docente si la IA no consigue adaptar un texto? ¿Dónde se guarda cómo lee cada alumno, y quién puede verlo? ¿Qué datos salen del ordenador del docente? Nadie debería responderlas a mitad de una devslice.</p>
</div>

Primero viene la **especificación funcional global**: el comportamiento del producto entero. Sus funcionalidades no salen solo de la visión. Salen también de las referencias, como la presentación de la Coordinadora Balear y los enunciados de Jaume Serra, y del estudio de mercado de la propia visión, con productos como Diffit o SUMM AI. Y de cualquier otra fuente de requisitos.

Después llega la **definición técnica**: con qué y cómo se construye. El detalle no tiene que ser total: basta con entender el producto completo y las decisiones que lo sostienen.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 604" width="100%" role="img" aria-label="Lo que se define en la especificación funcional y en la definición técnica de LecturaFàcil" style="font-family:'DM Sans',Arial,sans-serif;display:block">
<text x="14" y="24" font-size="15" font-weight="700" fill="#004d47">Especificación funcional global</text>
<text x="34" y="60" font-size="13.5" font-weight="700" fill="#004d47">Funcionalidades y reglas</text><text x="34" y="77" font-size="12" fill="#555">perfiles de lector, dial, línea roja, ayudas</text>
<text x="34" y="102" font-size="13.5" font-weight="700" fill="#004d47">Interfaz</text><text x="34" y="119" font-size="12" fill="#555">pantallas y navegación, diseñadas antes de elegir la técnica</text>
<text x="34" y="144" font-size="13.5" font-weight="700" fill="#004d47">Recorridos de usuario</text><text x="34" y="161" font-size="12" fill="#555">pegar un texto, elegir el grupo, revisar, aprobar</text>
<text x="34" y="186" font-size="13.5" font-weight="700" fill="#004d47">Estados</text><text x="34" y="203" font-size="12" fill="#555">texto vacío, el agente falla, quién ve cada perfil</text>
<text x="34" y="228" font-size="13.5" font-weight="700" fill="#004d47">Criterios comprobables</text><text x="34" y="245" font-size="12" fill="#555">«los conceptos de la materia no cambian»</text>
<text x="34" y="270" font-size="13.5" font-weight="700" fill="#004d47">Contratos</text><text x="34" y="287" font-size="12" fill="#555">entre la aplicación y el agente: entradas, salidas, errores</text>
<path d="M22,38 H16 V286 H22" fill="none" stroke="#00726b" stroke-width="2"/>
<text x="14" y="326" font-size="15" font-weight="700" fill="#004d47">Definición técnica y arquitectura</text>
<text x="34" y="362" font-size="13.5" font-weight="700" fill="#004d47">Tecnologías y plataforma</text><text x="34" y="379" font-size="12" fill="#555">escritorio, por ahora: Python, Tkinter y SQLite</text>
<text x="34" y="404" font-size="13.5" font-weight="700" fill="#004d47">Arquitectura y datos</text><text x="34" y="421" font-size="12" fill="#555">MVP, SQL nativo y migraciones versionadas</text>
<text x="34" y="446" font-size="13.5" font-weight="700" fill="#004d47">El agente</text><text x="34" y="463" font-size="12" fill="#555">Claude Code: contrato, permisos, límites y coste</text>
<text x="34" y="488" font-size="13.5" font-weight="700" fill="#004d47">Integraciones y datos que salen</text><text x="34" y="505" font-size="12" fill="#555">pictogramas; nada de nombres de alumnos</text>
<text x="34" y="530" font-size="13.5" font-weight="700" fill="#004d47">Pruebas y distribución</text><text x="34" y="547" font-size="12" fill="#555">cómo se comprueba y cómo llega al docente</text>
<text x="34" y="572" font-size="13.5" font-weight="700" fill="#004d47">Decisiones</text><text x="34" y="589" font-size="12" fill="#555">cada elección, con su razón por escrito</text>
<path d="M22,340 H16 V588 H22" fill="none" stroke="#00726b" stroke-width="2"/>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">El mapa de lo que se define antes de repartir el trabajo, con ejemplos de LecturaFàcil.</figcaption>
</figure>

### La interfaz, antes que la técnica

Antes de elegir ninguna tecnología se **crea la interfaz**: pantallas, navegación y lo que ocurre en cada estado, como cargando, vacío, error o sin permiso. En LecturaFàcil, el corazón es la pantalla de revisión, donde el docente ve cada hoja, entiende cada cambio y decide.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 492" width="100%" role="img" aria-label="Boceto de la pantalla de revisión de LecturaFàcil" style="font-family:'DM Sans',Arial,sans-serif;display:block">
<rect x="14" y="8" width="532" height="474" rx="10" fill="#fff" stroke="#b2deda" stroke-width="1.5"/>
<line x1="14" y1="40" x2="546" y2="40" stroke="#b2deda" stroke-width="1.5"/>
<text x="30" y="30" font-size="13" font-weight="700" fill="#004d47">LecturaFàcil · Revisar versiones · 2.º B · Kant</text>
<text x="30" y="68" font-size="12.5" fill="#888">Original</text>
<text x="110" y="68" font-size="12.5" fill="#888">Pau · nivel 1</text>
<text x="222" y="68" font-size="12.5" font-weight="700" fill="#00726b">Yasmin · nivel 3</text>
<line x1="222" y1="76" x2="330" y2="76" stroke="#00726b" stroke-width="2.5"/>
<rect x="30" y="92" width="500" height="148" rx="6" fill="#f7f7f7"/>
<text x="46" y="116" font-size="13" font-weight="700" fill="#1a1a1a">Qui és Kant</text>
<text x="46" y="138" font-size="12.5" fill="#1a1a1a">Kant és un filòsof.</text>
<text x="46" y="158" font-size="12.5" fill="#1a1a1a">Kant va viure a Prússia fa més de 200 anys.</text>
<rect x="46" y="172" width="250" height="8" rx="4" fill="#ddd"/><rect x="46" y="190" width="200" height="8" rx="4" fill="#ddd"/><rect x="46" y="208" width="230" height="8" rx="4" fill="#ddd"/>
<rect x="340" y="104" width="176" height="122" rx="6" fill="#fff" stroke="#b2deda"/>
<text x="352" y="124" font-size="11.5" font-weight="700" fill="#00726b">Glosario</text>
<text x="352" y="144" font-size="11.5" fill="#1a1a1a">enteniment · العقل</text>
<text x="352" y="162" font-size="11.5" fill="#1a1a1a">menor d'edat · قاصر</text>
<rect x="352" y="174" width="120" height="7" rx="3.5" fill="#ddd"/><rect x="352" y="190" width="100" height="7" rx="3.5" fill="#ddd"/>
<text x="30" y="270" font-size="13.5" font-weight="700" fill="#004d47">Qué ha cambiado, y por qué</text>
<text x="30" y="294" font-size="12.5" fill="#1a1a1a">La frase larga se parte</text><text x="530" y="294" text-anchor="end" font-size="12" fill="#888">frases cortas</text>
<text x="30" y="316" font-size="12.5" fill="#1a1a1a">Primero el ejemplo, después el concepto</text><text x="530" y="316" text-anchor="end" font-size="12" fill="#888">concreto antes que abstracto</text>
<text x="30" y="338" font-size="12.5" fill="#1a1a1a">Los conceptos se quedan</text><text x="530" y="338" text-anchor="end" font-size="12" font-weight="700" fill="#00726b">línea roja ✓</text>
<text x="30" y="360" font-size="12" fill="#888">+ 3 cambios más</text>
<line x1="30" y1="378" x2="530" y2="378" stroke="#e0f4f3" stroke-width="2"/>
<text x="30" y="402" font-size="12" fill="#888">Si el agente no puede adaptar: aviso, y el original queda intacto</text>
<rect x="290" y="418" width="110" height="32" rx="16" fill="#fff" stroke="#00726b" stroke-width="1.5"/><text x="345" y="439" text-anchor="middle" font-size="12.5" font-weight="700" fill="#00726b">Ajustar regla</text>
<rect x="410" y="418" width="120" height="32" rx="16" fill="#00726b"/><text x="470" y="439" text-anchor="middle" font-size="12.5" font-weight="700" fill="#fff">Aprobar</text>
<text x="30" y="474" font-size="11.5" font-style="italic" fill="#888">nada llega a la clase sin el visto bueno del docente</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Boceto ilustrativo de la pantalla de revisión, con la hoja de Yasmin y los cambios que recoge su documento de visión.</figcaption>
</figure>

Diseñada antes, la interfaz marca lo que la técnica tiene que servir, y no al revés. Lo que se dibuja aquí se convierte después en criterios comprobables.

### El contexto tecnológico

La definición técnica empieza por el **contexto**: dónde vivirá el producto y con qué convive. LecturaFàcil será, de momento, una aplicación de escritorio: Python, Tkinter y SQLite, con Claude Code como agente que adapta los textos. Encaja con tus favoritas para el escritorio pequeño, así que no hay excepciones que justificar.

El centro de su visión ya trabaja con Google Classroom y escucha textos con TextAid. Ese contexto no cambia la plataforma, pero pesa al decidir cómo llega cada hoja al alumno. Cada elección queda escrita con su razón, para que nadie tenga que volver a discutirla.

### La arquitectura

Falta decidir qué piezas tiene el producto y cómo se hablan. Para un escritorio pequeño, el método propone **Modelo–Vista–Presentador**. La vista muestra y recoge acciones, el presentador coordina, y el modelo guarda las reglas de la Lectura Fácil sin saber nada de Tkinter ni de SQL. La arquitectura se ajusta a la complejidad real: capas más elaboradas, como Clean, solo cuando se justifican, y sin carpetas vacías.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 506" width="100%" role="img" aria-label="Arquitectura posible de LecturaFàcil: Modelo-Vista-Presentador con el agente detrás de un adaptador" style="font-family:'DM Sans',Arial,sans-serif;display:block">
<defs><marker id="vc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#004d47"/></marker></defs>
<text x="280" y="22" text-anchor="middle" font-size="13" fill="#555">el docente, en su ordenador</text>
<line x1="280" y1="30" x2="280" y2="50" stroke="#004d47" stroke-width="2" marker-end="url(#vc)"/>
<rect x="80" y="54" width="400" height="56" rx="8" fill="#fff" stroke="#00726b" stroke-width="1.5"/>
<text x="280" y="78" text-anchor="middle" font-size="14.5" font-weight="700" fill="#004d47">Vista · Tkinter</text>
<text x="280" y="98" text-anchor="middle" font-size="12" fill="#555">grupos, textos y la pantalla de revisión</text>
<line x1="280" y1="112" x2="280" y2="132" stroke="#004d47" stroke-width="2" marker-end="url(#vc)"/>
<rect x="80" y="136" width="400" height="56" rx="8" fill="#fff" stroke="#00726b" stroke-width="1.5"/>
<text x="280" y="160" text-anchor="middle" font-size="14.5" font-weight="700" fill="#004d47">Presentador</text>
<text x="280" y="180" text-anchor="middle" font-size="12" fill="#555">coordina cada acción y sus estados: cargando, error…</text>
<line x1="280" y1="194" x2="280" y2="214" stroke="#004d47" stroke-width="2" marker-end="url(#vc)"/>
<rect x="80" y="218" width="400" height="62" rx="8" fill="#00726b"/>
<text x="280" y="244" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">Modelo</text>
<text x="280" y="266" text-anchor="middle" font-size="12" fill="#e0f4f3">perfiles, dial, reglas y línea roja · sin Tkinter ni SQL</text>
<text x="280" y="306" text-anchor="middle" font-size="12" font-style="italic" fill="#888">lo externo, en el borde, detrás de un adaptador</text>
<ellipse cx="62" cy="336" rx="22" ry="6" fill="#e0f4f3" stroke="#00726b"/><path d="M40,336 V364 A22,6 0 0 0 84,364 V336" fill="#e0f4f3" stroke="#00726b"/><ellipse cx="62" cy="336" rx="22" ry="6" fill="#e0f4f3" stroke="#00726b"/>
<text x="104" y="346" font-size="14" font-weight="700" fill="#004d47">Persistencia · SQLite</text><text x="104" y="364" font-size="12" fill="#555">SQL nativo, sin ORM, y migraciones versionadas</text>
<circle cx="62" cy="414" r="18" fill="#fff" stroke="#00726b" stroke-width="1.5"/><text x="62" y="419" text-anchor="middle" font-size="13" font-weight="700" fill="#00726b">IA</text>
<text x="104" y="410" font-size="14" font-weight="700" fill="#004d47">El agente · Claude Code</text><text x="104" y="428" font-size="12" fill="#555">agent-runtime/: instrucciones, skill y validadores</text>
<rect x="44" y="460" width="36" height="28" rx="5" fill="#fff" stroke="#00726b" stroke-width="1.5"/><text x="62" y="479" text-anchor="middle" font-size="11" font-weight="700" fill="#00726b">ext</text>
<text x="104" y="472" font-size="14" font-weight="700" fill="#004d47">Servicios externos</text><text x="104" y="490" font-size="12" fill="#555">pictogramas de ARASAAC</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Una arquitectura posible para LecturaFàcil: las reglas en el centro y lo externo en los bordes. Ilustrativa: se decide en la definición técnica.</figcaption>
</figure>

Hay dos memorias más que considerar. La carpeta `docs/` de LecturaFàcil puede abrirse como vault de Obsidian: es su **brain de desarrollo**, sin copiar nada. Y lo que el producto aprende mientras funciona, como el pictograma que el docente pidió recordar para «Il·lustració» o las palabras que marca Yasmin, es **conocimiento operativo**. Hay que decidir si vive en tablas SQL o en una base de conocimiento del agente, y cuál manda si las dos describen lo mismo.

### Preguntar, no inventar

Definir tanto deja huecos, y la tentación es rellenarlos con suposiciones. La fábrica tiene un acuerdo para eso.

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · un hueco en la definición</p>
<p class="escena-contexto">Claude prepara el contrato entre la aplicación y el agente.</p>
<div class="turno"><p class="ponente">Claude<small>pregunta</small></p><p>La visión no dice qué datos de los alumnos pueden salir del ordenador. No quiero suponerlo. ¿Envío al agente solo el texto, la materia, los conceptos protegidos y el perfil de lectura, sin nombres?</p></div>
<div class="turno"><p class="ponente">Tú<small>decide</small></p><p>Sin nombres, nunca. Y apúntalo.</p></div>
<div class="turno"><p class="ponente">Claude<small>registra</small></p><p>Queda en <code>docs/decisiones/</code> con su razón. Mientras esperaba, he seguido con la interfaz, que no dependía de esto. Ahora continúo con el contrato.</p></div>
<p class="escena-pie">Diálogo imaginado: muestra cómo se resuelve un hueco, no una conversación real.</p>
</div>

Cuando falta información, Claude consulta lo que hay y después pregunta todo lo que necesita, de una vez. No inventa requisitos ni convierte supuestos en decisiones. Mientras espera, sigue con lo que no depende de la respuesta. Y cada decisión queda escrita con su porqué, para que nadie tenga que volver a preguntarla.

---

## Qué cambia con un agente dentro

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 4 · Dos Claude</p>
<p>LecturaFàcil tendrá dos Claude. Uno la construye contigo. El otro vivirá dentro, adaptando textos para Yasmin y Pau. Se llaman igual, pero no deben conocerse. ¿Qué pasa si se mezclan?</p>
</div>

La aplicación lanza a Claude Code con su SDK de Python. Por defecto, ese SDK carga la configuración del usuario y la del proyecto, y [busca skills hasta la raíz del repositorio](https://code.claude.com/docs/en/agent-sdk/skills.md). Sin cuidado, el agente que adapta textos cargaría las skills con las que desarrollas. Por eso trabaja en su propio directorio, fuera del repositorio y solo con su skill. Una prueba comprueba qué skills carga al arrancar.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 400" width="100%" role="img" aria-label="El Claude que desarrolla y el agente dentro de LecturaFàcil, separados" style="font-family:'DM Sans',Arial,sans-serif;display:block">
<rect x="14" y="8" width="532" height="150" rx="8" fill="#fff" stroke="#00726b" stroke-width="1.5"/>
<text x="34" y="36" font-size="15" font-weight="700" fill="#004d47">El Claude que desarrolla</text>
<text x="34" y="62" font-size="12.5" fill="#1a1a1a">lo usas tú, con tu suscripción de Claude Code</text>
<text x="34" y="84" font-size="12.5" fill="#1a1a1a">las skills de la SF: especificar, preparar, probar, cerrar</text>
<text x="34" y="106" font-size="12.5" fill="#1a1a1a">trabaja en el repositorio de LecturaFàcil</text>
<text x="34" y="128" font-size="12.5" fill="#1a1a1a">puede leer y escribir código, con tu permiso</text>
<line x1="14" y1="182" x2="546" y2="182" stroke="#991b1b" stroke-width="1.6" stroke-dasharray="6 5"/>
<text x="280" y="204" text-anchor="middle" font-size="12.5" font-style="italic" fill="#991b1b">nada pasa de uno a otro sin una versión</text>
<rect x="14" y="222" width="532" height="170" rx="8" fill="#00726b"/>
<text x="34" y="250" font-size="15" font-weight="700" fill="#fff">El agente dentro de LecturaFàcil</text>
<text x="34" y="276" font-size="12.5" fill="#e0f4f3">pago por uso: cada llamada tiene un coste</text>
<text x="34" y="298" font-size="12.5" fill="#e0f4f3">solo la skill de Lectura Fácil, sin herramientas que no necesita</text>
<text x="34" y="320" font-size="12.5" fill="#e0f4f3">su propio directorio, fuera del repositorio</text>
<text x="34" y="342" font-size="12.5" fill="#e0f4f3">cada respuesta pasa por los validadores</text>
<text x="34" y="364" font-size="12.5" fill="#e0f4f3">lo usan los docentes, sin nombres de alumnos</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Dos Claude con papeles, permisos y versiones distintos. Mejorar uno no cambia al otro sin querer.</figcaption>
</figure>

Además, no se autentican igual. Tú desarrollas con tu suscripción. El producto no puede ofrecer el inicio de sesión de claude.ai, porque Anthropic [no lo permite a productos de terceros sin su aprobación](https://code.claude.com/docs/en/agent-sdk/overview.md). Por eso la credencial es una línea de configuración, no de código. El centro elige una clave de API, la consola de Claude o un proveedor en la nube, y paga por uso. Un cliente que ya programa con Claude Code podría usar su propia suscripción, pero conviene confirmarlo antes con Anthropic.

Cada adaptación cuesta dinero, también en las pruebas. Por eso casi todas usan un agente falso, y las evaluaciones con el real se lanzan a propósito, con su coste en el informe.

El agente tampoco responde dos veces igual. La garantía no está en comparar textos, sino en los **validadores**: la línea roja, la longitud de las frases y el formato de la respuesta, que el SDK puede exigir como JSON con un esquema. Cada informe anota el modelo y la versión de la skill.

El resto son buenas costumbres que se diseñan desde el principio. La ventana no se congela mientras el agente piensa. El agente no tiene herramientas que no necesita. Sus versiones se fijan para que nada cambie sin querer. Y ningún nombre de alumno sale del ordenador.

También se piensa desde el principio cómo se instala: en un solo paso. Ese paso deja las dependencias, la base de datos, las skills del agente y la configuración. LecturaFàcil se instalará en los equipos del centro. Los datos se quedan allí; solo salen las llamadas al modelo.

Todo esto se repetirá en cada aplicación con un agente dentro. Por eso LecturaFàcil no es solo un piloto: es el caso que enseñará a la fábrica cómo se construyen.

---

## Cómo se construye, devslice a devslice

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 5 · Repartir el trabajo</p>
<p>La especificación y la definición técnica de LecturaFàcil ya están acordadas. Toca decidir cómo se construye. Lo tentador sería empezar por lo más vistoso: que la IA adapte a Kant. Pero sería la pieza más crítica, sin nada debajo para comprobarla. ¿Por dónde se empieza?</p>
</div>

Las funcionalidades dicen **qué** hará LecturaFàcil. Las **devslices** dicen **cómo se construye**: incrementos pequeños y verticales, que atraviesan interfaz, lógica, datos y pruebas. Cada una cabe en **una o dos sesiones de trabajo**. Si al prepararla no cabe, se parte en dos.

El orden sigue una regla sencilla: **primero, lo que hace falta para comprobar que lo siguiente funciona**. Por eso LecturaFàcil empieza por lo básico: docentes, grupos, perfiles y materias. El agente llega al final. Hasta entonces, un agente simulado devuelve versiones de ejemplo, como las de Kant de su visión, detrás del mismo adaptador. Cuando llegue Claude Code, la pantalla, la línea roja y los validadores ya estarán probados.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 826" width="100%" role="img" aria-label="Plan de devslices de LecturaFàcil en cuatro fases, con el agente al final" style="font-family:'DM Sans',Arial,sans-serif;display:block">
<text x="14" y="24" font-size="15.5" font-weight="700" fill="#004d47">Plan de devslices · LecturaFàcil</text>
<text x="546" y="24" text-anchor="end" font-size="12" fill="#888">sesiones</text>
<line x1="14" y1="36" x2="546" y2="36" stroke="#e0f4f3" stroke-width="2"/>
<text x="14" y="64" font-size="14.5" font-weight="700" fill="#00726b">La base<tspan font-size="12" font-weight="400" fill="#888">   lo que necesita todo lo demás</tspan></text>
<text x="34" y="92" font-size="13.5" font-weight="700" fill="#004d47">Docentes</text><text x="34" y="109" font-size="12" fill="#555">el armazón: ventana, MVP y SQLite con su migración</text><text x="546" y="92" text-anchor="end" font-size="12" fill="#00726b">1–2</text>
<text x="34" y="132" font-size="13.5" font-weight="700" fill="#004d47">Grupos y alumnos</text><text x="34" y="149" font-size="12" fill="#555">datos mínimos: cómo lee cada uno, no su expediente</text><text x="546" y="132" text-anchor="end" font-size="12" fill="#00726b">1–2</text>
<text x="34" y="172" font-size="13.5" font-weight="700" fill="#004d47">Perfiles de lector y niveles</text><text x="34" y="189" font-size="12" fill="#555">perfil, nivel del dial y lengua materna</text><text x="546" y="172" text-anchor="end" font-size="12" fill="#00726b">1–2</text>
<text x="34" y="212" font-size="13.5" font-weight="700" fill="#004d47">Materias y conceptos protegidos</text><text x="34" y="229" font-size="12" fill="#555">lo que no se toca: «enteniment», «Sapere aude»…</text><text x="546" y="212" text-anchor="end" font-size="12" fill="#00726b">1</text>
<text x="14" y="262" font-size="14.5" font-weight="700" fill="#00726b">El texto y su revisión<tspan font-size="12" font-weight="400" fill="#888">   con un agente simulado</tspan></text>
<text x="34" y="290" font-size="13.5" font-weight="700" fill="#004d47">Guardar un texto</text><text x="34" y="307" font-size="12" fill="#555">un texto de una materia, que sigue ahí al reabrir</text><text x="546" y="290" text-anchor="end" font-size="12" fill="#00726b">1</text>
<text x="34" y="330" font-size="13.5" font-weight="700" fill="#004d47">Original y versión, lado a lado</text><text x="34" y="347" font-size="12" fill="#555">la pantalla de revisión y el contrato del agente</text><text x="546" y="330" text-anchor="end" font-size="12" fill="#00726b">1–2</text>
<rect x="26" y="354" width="524" height="42" rx="6" fill="none" stroke="#00726b" stroke-width="1.2"/>
<text x="34" y="370" font-size="13.5" font-weight="700" fill="#00726b">La línea roja</text><text x="34" y="387" font-size="12" fill="#555">el validador rechaza la versión sin un concepto protegido</text><text x="542" y="370" text-anchor="end" font-size="12" fill="#00726b">1</text>
<text x="34" y="420" font-size="13.5" font-weight="700" fill="#004d47">Comprobar las reglas</text><text x="34" y="437" font-size="12" fill="#555">validadores medibles: largo de frase, un término por concepto</text><text x="546" y="420" text-anchor="end" font-size="12" fill="#00726b">1–2</text>
<text x="34" y="460" font-size="13.5" font-weight="700" fill="#004d47">Revisar y aprobar</text><text x="34" y="477" font-size="12" fill="#555">cada cambio con su regla, y el visto bueno</text><text x="546" y="460" text-anchor="end" font-size="12" fill="#00726b">1–2</text>
<text x="14" y="510" font-size="14.5" font-weight="700" fill="#00726b">El aula</text>
<text x="34" y="538" font-size="13.5" font-weight="700" fill="#004d47">Una versión por lector</text><text x="34" y="555" font-size="12" fill="#555">todo el grupo, a la vez</text><text x="546" y="538" text-anchor="end" font-size="12" fill="#00726b">1–2</text>
<text x="34" y="578" font-size="13.5" font-weight="700" fill="#004d47">Ajustar una regla en un perfil</text><text x="34" y="595" font-size="12" fill="#555">el ajuste del docente se recuerda</text><text x="546" y="578" text-anchor="end" font-size="12" fill="#00726b">1</text>
<text x="34" y="618" font-size="13.5" font-weight="700" fill="#004d47">El glosario al lado del texto</text><text x="34" y="635" font-size="12" fill="#555">con pictograma y lengua materna</text><text x="546" y="618" text-anchor="end" font-size="12" fill="#00726b">1–2</text>
<text x="34" y="658" font-size="13.5" font-weight="700" fill="#004d47">Retirar ayudas por grados</text><text x="34" y="675" font-size="12" fill="#555">menos apoyo cuando el alumno avanza</text><text x="546" y="658" text-anchor="end" font-size="12" fill="#00726b">1–2</text>
<text x="14" y="708" font-size="14.5" font-weight="700" fill="#00726b">El agente<tspan font-size="12" font-weight="400" fill="#888">   cuando todo lo demás ya se puede comprobar</tspan></text>
<text x="34" y="736" font-size="13.5" font-weight="700" fill="#004d47">Conectar el agente</text><text x="34" y="753" font-size="12" fill="#555">Claude Code sustituye al simulado: llamadas, registro, errores</text><text x="546" y="736" text-anchor="end" font-size="12" fill="#00726b">2</text>
<text x="34" y="776" font-size="13.5" font-weight="700" fill="#004d47">La skill de Lectura Fácil</text><text x="34" y="793" font-size="12" fill="#555">las reglas, en tandas pequeñas y evaluadas</text><text x="546" y="776" text-anchor="end" font-size="12" fill="#00726b">1–2 c/u</text>
<text x="14" y="820" font-size="12" font-style="italic" fill="#888">primero, lo que permite comprobar lo siguiente</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Cada devslice, de una o dos sesiones y con algo que se ve funcionar. Plan ilustrativo: se fija con la especificación y la definición técnica.</figcaption>
</figure>

Cada devslice lleva un nombre que se entiende, como «La línea roja», nunca un código como `DS007`. Y una devslice planificada todavía no está preparada. Cuando le llega el turno a «La línea roja», hay que decidir qué cuenta como hecho.

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · preparando «La línea roja»</p>
<p class="escena-contexto">Tú y Claude afináis los criterios de aceptación.</p>
<div class="turno"><p class="ponente">Claude<small>propone</small></p><p>Criterio: el validador rechaza una versión a la que le falte un concepto protegido de la materia. Prueba prevista: las cuatro hojas de Kant de la visión deben pasar, y una copia sin «Sapere aude» debe fallar.</p></div>
<div class="turno"><p class="ponente">Tú<small>matiza</small></p><p>Mira la hoja de Yasmin: dice «menors d'edat», pero también «minoria d'edat». ¿Qué cuenta?</p></div>
<div class="turno"><p class="ponente">Claude<small>pregunta</small></p><p>No lo decido yo. Propongo que el concepto aparezca al menos una vez en su forma original, y que las variantes cuenten como explicación. ¿Te vale?</p></div>
<div class="turno"><p class="ponente">Tú<small>decide</small></p><p>Me vale. Que quede escrito en el criterio.</p></div>
<p class="escena-pie">Diálogo imaginado. Las palabras de la hoja de Yasmin son reales, de la visión de LecturaFàcil.</p>
</div>

Así avanza cada devslice: **planificada en el plan y preparada antes de construirse**, con alcance, criterios, pruebas previstas y tareas. Después se escriben las pruebas y se revisa que de verdad representan los criterios: una prueba que pasa no basta si no comprueba lo que se pidió. Luego se construyen la lógica y los datos, y la interfaz al final. Las pruebas siguen vivas cuando la devslice se cierra, porque pertenecen a LecturaFàcil.

---

## Qué muestra el tablero

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 6 · El tablero responde</p>
<p>Las tareas de «La línea roja» ya están en JKanban, dentro del proyecto LecturaFàcil. Claude empieza a trabajar y quiere mover la primera a «En desarrollo». ¿Y si algo falla?</p>
</div>

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · una operación que no se confirma</p>
<p class="escena-contexto">Claude intenta actualizar el tablero.</p>
<div class="turno"><p class="ponente">Claude<small>pide</small></p><p>Mover «Escribir la prueba de la línea roja» a En desarrollo.</p></div>
<div class="turno sistema"><p class="ponente">JKanban<small>responde</small></p><p>403 · UserNotInProject: el usuario no tiene acceso al proyecto.</p></div>
<div class="turno"><p class="ponente">Claude<small>informa</small></p><p>No he podido mover la tarea: mi usuario no es miembro de LecturaFàcil. Sigue en Preparada. ¿Me añades al equipo?</p></div>
<p class="escena-pie">Diálogo imaginado. El error y su código existen en JKanban; la situación es un ejemplo.</p>
</div>

El tablero es tu **ventana permanente** al trabajo. Cada devslice tiene sus tareas, y cada tarea su estado, sus dependencias y sus bloqueos, con el motivo a la vista. Claude lo consulta para retomar después de una pausa y lo actualiza mientras trabaja. Hay una regla que no se negocia: nada está anotado hasta que JKanban lo confirma. Un error se ve; no se esconde.

---

## Cómo se cierra una devslice

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 7 · Darla por terminada</p>
<p>«La línea roja» ya funciona en la pantalla de Claude: la copia sin «Sapere aude» falla y las cuatro hojas de Kant pasan. Pero que funcione allí no es lo mismo que darla por terminada. ¿Qué hace falta para cerrarla?</p>
</div>

Tres cosas que a menudo se confunden son distintas. El **criterio** es lo que se exige, y vive en la especificación de la devslice. Las **pruebas** son la forma de comprobarlo, y viven en el código. El **resultado** es lo que pasó al ejecutarlas sobre una versión concreta, y vive en un informe. Un criterio puede necesitar varias pruebas, y que pasen aporta evidencia, pero no cambia el criterio.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 402" width="100%" role="img" aria-label="Cierre de la devslice La línea roja: criterio, pruebas, resultado, tablero y aprobación" style="font-family:'DM Sans',Arial,sans-serif;display:block">
<line x1="34" y1="52" x2="34" y2="360" stroke="#b2deda" stroke-width="2"/>
<circle cx="34" cy="52" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/>
<text x="56" y="56" font-size="14.5" font-weight="700" fill="#004d47">Criterio<tspan font-size="12" font-weight="400" fill="#888">   en la especificación de la devslice</tspan></text>
<text x="56" y="76" font-size="12.5" fill="#1a1a1a">«Rechazar una versión a la que le falte</text>
<text x="56" y="93" font-size="12.5" fill="#1a1a1a">un concepto protegido de la materia»</text>
<circle cx="34" cy="128" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/>
<text x="56" y="132" font-size="14.5" font-weight="700" fill="#004d47">Pruebas<tspan font-size="12" font-weight="400" fill="#888">   en tests/</tspan></text>
<text x="56" y="152" font-size="12.5" fill="#1a1a1a">unitaria: el validador, con y sin el concepto</text>
<text x="56" y="170" font-size="12.5" fill="#1a1a1a">integración: los conceptos guardados en SQLite</text>
<text x="56" y="188" font-size="12.5" fill="#1a1a1a">aceptación: las cuatro hojas de Kant</text>
<circle cx="34" cy="222" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/>
<text x="56" y="226" font-size="14.5" font-weight="700" fill="#004d47">Resultado<tspan font-size="12" font-weight="400" fill="#888">   en reports/tests/, sin sobrescribir</tspan></text>
<text x="56" y="246" font-size="12.5" fill="#1a1a1a">qué pasó, con qué versión del código</text>
<text x="56" y="264" font-size="12.5" fill="#1a1a1a">y con qué evidencias, en un informe legible</text>
<circle cx="34" cy="298" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/>
<text x="56" y="302" font-size="14.5" font-weight="700" fill="#004d47">Tablero</text>
<text x="56" y="322" font-size="12.5" fill="#1a1a1a">la tarjeta pasa a Terminada y enlaza el informe</text>
<circle cx="34" cy="360" r="7" fill="#00726b"/>
<text x="56" y="364" font-size="14.5" font-weight="700" fill="#00726b">Tu aprobación</text>
<text x="56" y="384" font-size="12.5" fill="#1a1a1a">nada se integra ni se publica sin ella</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">El cierre de «La línea roja», paso a paso. Ilustrativo.</figcaption>
</figure>

Cada ejecución relevante deja un informe con fecha, alcance y versión del código, y no sobrescribe los anteriores. Se puede volver a ejecutar las pruebas, pero eso no reproduce la evidencia de entonces. Por eso el tablero enlaza el informe del cierre. Integrar o publicar sigue siendo tu decisión: el método no autoriza nada automático.

---

## De dónde salen las herramientas

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 8 · La caja de herramientas</p>
<p>Para preparar, construir y cerrar cada devslice, Claude necesita skills: preparar devslices, diseñar pruebas, operar el tablero. ¿Las de qué carpeta? ¿En qué versión?</p>
</div>

Todas las skills de la fábrica, propias o de otros autores, viven en un solo sitio: la carpeta `skills/` de SoftwareFactory. Cada una lleva su procedencia, su licencia y su versión. Las externas se guardan enteras, aunque no se toquen, para que ninguna actualización ajena cambie nada sin que lo decidas. Desde ahí se instalan todas en la carpeta global de Claude Code, para usarlas en cualquier proyecto. Ninguna lleva nada de un proyecto concreto: lo propio de cada uno, como su tema, su logo o sus reglas, vive en su carpeta `docs/identidad/`.

La fábrica tendrá **una skill para cada paso del método**. La de visión ya existe. La acompañan skills de apoyo, como la de infografías técnicas en 3D o las de GSAP y three.js. Las demás cubrirán la especificación y el diseño de interfaz, la definición técnica, la planificación de devslices, su preparación, el diseño y la revisión de pruebas, el cierre y el manejo del tablero. Las acompañan plantillas de documentos y perfiles técnicos. Uno de ellos servirá para aplicaciones de escritorio con un agente dentro, y LecturaFàcil ayudará a definirlo.

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
<text x="60" y="258" font-size="14.5" font-weight="700" fill="#004d47">LecturaFàcil</text><text x="250" y="258" font-size="12.5" fill="#555">el piloto, sabe qué versión usa</text>
<text x="60" y="290" font-size="14.5" font-weight="700" fill="#004d47">OncoCore</text><text x="250" y="290" font-size="12.5" fill="#555">la misma u otra, a su ritmo</text>
<text x="60" y="322" font-size="14.5" font-weight="700" fill="#004d47">El próximo proyecto</text><text x="250" y="322" font-size="12.5" fill="#555">arranca con lo aprendido</text>
<line x1="40" y1="242" x2="40" y2="330" stroke="#b2deda" stroke-width="2"/>
<path d="M440,318 C548,318 548,60 404,60" fill="none" stroke="#00726b" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#vb)"/>
<text x="414" y="140" font-size="11.5" font-weight="700" fill="#00726b">mejora</text>
<text x="414" y="156" font-size="11.5" font-weight="700" fill="#00726b">aprobada</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Una sola fuente, versiones con nombre y un camino de vuelta para lo que se aprende.</figcaption>
</figure>

Las skills aportan técnica; tu método y el perfil de cada proyecto deciden la tecnología. Así ninguna pieza impone una metodología ajena.

---

## Cómo aprende la fábrica

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 9 · Una lección que viaja</p>
<p>El documento de visión de LecturaFàcil se generó con la paleta y el emblema de un instituto. Pero el script que lo convertía en página importaba código de OncoCore y su hoja de estilos. Si OncoCore no hubiera estado en este ordenador, la skill no habría funcionado. ¿Era un problema de LecturaFàcil o de la fábrica?</p>
</div>

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · una propuesta de mejora</p>
<div class="turno"><p class="ponente">Claude<small>propone</small></p><p>Mejora para SoftwareFactory: que la skill de visión funcione sin depender de OncoCore. Origen: LecturaFàcil, documento de visión. Evidencia: su script carga <code>md_to_html</code> desde la carpeta de OncoCore. La registro en el proyecto SoftwareFactory y espero tu aprobación.</p></div>
<div class="turno"><p class="ponente">Tú<small>decide</small></p><p>Aprobada. Y que el tema y el emblema de cada proyecto vivan en el proyecto, no en la skill.</p></div>
<p class="escena-pie">Diálogo imaginado. La dependencia era real y la mejora ya está aplicada; consta en el registro local de la fábrica, todavía sin tarjeta en el tablero.</p>
</div>

La fábrica tiene una tarea que nunca se cierra: **Mejorar la Software Factory**. Mientras trabaja en cualquier proyecto, Claude observa fricciones, errores repetidos y pasos de más. Cada mejora general va al proyecto SoftwareFactory del tablero, con su origen y su evidencia. Lo que es propio de LecturaFàcil se queda en LecturaFàcil. Así nació la carpeta de identidad de cada proyecto. La skill ya no sabe nada de OncoCore ni de un instituto: cada proyecto guarda allí su tema y su emblema.

Proponer no es cambiar. Ninguna mejora se aplica ni se distribuye sin tu aprobación expresa. La fábrica aprende rápido, pero el método sigue siendo tuyo.

---

## En qué se diferencia de lo que ya existe

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 10 · Mirar alrededor</p>
<p>Con la visión de LecturaFàcil en la mano, te preguntas si no habría bastado con instalar algo ya hecho. Hay marcos de trabajo con cientos de miles de estrellas en GitHub. ¿Por qué construir el tuyo?</p>
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

Son alternativas reales, y en varias cosas van por delante. Spec Kit [cumplió un año en agosto de 2026 con su versión 1.0.0](https://github.github.com/spec-kit/history.html) y funciona con 38 agentes. SoftwareFactory solo funciona con Claude Code. [Superpowers](https://github.com/obra/superpowers) ya resuelve pasos que tu fábrica solo ha planificado: el diseño previo, los planes en tareas pequeñas, las pruebas primero, la revisión de código y la verificación antes de terminar. [BMAD](https://github.com/bmad-code-org/BMAD-METHOD) ajusta cuánto se planifica al tamaño de cada cambio. Y las tres tienen detrás comunidades que las usan y las corrigen.

Frente a eso, SoftwareFactory es hoy un método escrito con pocas herramientas. Tiene la skill de visión y las de apoyo; las de los demás pasos están por construir. Ningún proyecto ha llegado todavía de la visión al código con ella: LecturaFàcil aún no tiene especificación. La mantiene una sola persona, y cada hora que se dedica a la fábrica no se dedica a LecturaFàcil.

Lo que la distingue es más estrecho de lo que parece. Empieza con una visión escrita para personas, trabaja con tu tablero y separa el Claude que desarrolla del que vive dentro de tus productos. Para el resto, SoftwareFactory **toma las piezas que sirven a tu método**, como dos skills de Superpowers que son candidatas, y las guarda con su procedencia. El piloto tiene que demostrar que esa diferencia compensa el coste de mantenerla.

---

## De vuelta al caso

<div class="caso">
<p class="caso-etiqueta">El caso · epílogo</p>
<p>LecturaFàcil sigue teniendo la misma pregunta: cómo dar el mismo Kant a toda la clase sin bajar la exigencia. Lo que ha cambiado es el camino para responderla. Sabe qué hará, cómo se verá y con qué se construirá. Su trabajo está repartido en devslices pequeñas, que empiezan por lo básico. La línea roja protege a Kant antes de que el agente escriba una palabra, y cada cierre deja su informe enlazado en el tablero. Además, el piloto ya ha dejado su primera mejora aplicada en la fábrica, registrada para el proyecto <strong>SoftwareFactory</strong>.</p>
<p>Lo que la fábrica no decide es lo que te corresponde: quién paga cada adaptación, si una mejora se aplica, cuándo se integra una devslice y cuándo se publica una versión. <strong>La fábrica prepara, construye y propone; las decisiones son tuyas.</strong></p>
</div>

---

## Anexo: el caso LecturaFàcil

### Qué es real

LecturaFàcil está en `D:\Projectes\LecturaFacil`, en fase inicial de definición. Contiene su documento de visión (`doc/vision/documento-vision.md` y su `.html`) y dos referencias: la presentación de la Coordinadora Balear de Persones amb Discapacitat (21 de octubre de 2026) y los enunciados de Jaume Serra (2008). Todavía no tiene especificación funcional ni código. Es el proyecto piloto de SoftwareFactory por decisión del propietario.

El propietario ha decidido su contexto tecnológico, de momento: escritorio con Python, Tkinter y SQLite, y Claude Code como agente de IA dentro del producto. Se instalará en local, en el centro. Estas decisiones todavía no constan en los documentos de LecturaFàcil.

El fragmento citado sale de su documento de visión, cuya historia es ficticia; Yasmin y Pau son personajes inventados. Las palabras de la escena de la línea roja («minoria d'edat», «menors d'edat», «enteniment», «Sapere aude») están en las hojas de Kant de esa visión. El error `UserNotInProject` es una excepción real de JKanban (`docs/business-rules.md`). La dependencia de la skill de visión respecto a OncoCore constaba en su script `doc_to_html.py`; su retirada está en el `ORIGIN.md` de la skill.

Lo que se dice del SDK de Claude Code (carga de configuración y de skills, modos de credencial, salida JSON con esquema) sale de su documentación oficial.

### Qué es ilustrativo

El plan de devslices, su orden, sus criterios y sus tareas son ejemplos sacados de la visión. También lo son los bocetos de la interfaz y de la arquitectura. Las escenas son imaginadas, incluida la decisión de no enviar nombres de alumnos al agente. Los proyectos LecturaFàcil y SoftwareFactory todavía no existen en JKanban, y la integración de Claude con el tablero aún no está construida. El perfil técnico para escritorio con agente es una idea por definir.

### Fuentes

Consultadas el 25 de octubre de 2026:

- Eric Risco, [*Programar con agentes ya no basta: monta tu Software Factory*](https://www.youtube.com/watch?v=p6nnqerea7w), YouTube.
- [Spec Kit](https://github.github.com/spec-kit/), de GitHub, y [su historia](https://github.github.com/spec-kit/history.html). Licencia MIT.
- [Superpowers](https://github.com/obra/superpowers), de Jesse Vincent. Licencia MIT.
- [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD), de BMad Code.
- Claude Agent SDK: [visión general y autenticación](https://code.claude.com/docs/en/agent-sdk/overview.md), [SDK de Python](https://code.claude.com/docs/en/agent-sdk/python.md) y [skills](https://code.claude.com/docs/en/agent-sdk/skills.md).

---

*Documento de visión de SoftwareFactory — 2026-10-25.*
