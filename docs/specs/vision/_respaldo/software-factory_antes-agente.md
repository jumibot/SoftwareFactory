# SoftwareFactory: tu forma de construir, convertida en fábrica

<div class="caso">
<p class="caso-etiqueta">El caso · prólogo · LecturaFàcil</p>
<p>LecturaFàcil ya tiene un sueño escrito: un documento de visión en el que una profesora de Filosofía da el mismo Kant a toda su clase. Yasmin lo recibe en Lectura Fácil, con glosario en árabe, y Pau, que tiene dislexia, con fondo crema y lectura en voz alta. No hay ni una línea de código. Será el <strong>proyecto piloto</strong> de la fábrica: el primero que se construye entero con el método. Hasta hoy, cada proyecto empezaba de cero, con sus propias reglas. Esta vez quieres otra cosa: <strong>¿cómo paso de este documento a una herramienta que funcione, sin perder nada por el camino, y que lo aprendido sirva al proyecto siguiente?</strong></p>
</div>

## Resumen operativo

Para eso existe **SoftwareFactory**: tu forma de construir aplicaciones con Claude Code, convertida en método y herramientas que se reutilizan. LecturaFàcil no pasará de la visión al código de golpe. Primero tendrá una especificación del conjunto y una definición técnica. Después, sus funcionalidades se construirán por devslices: incrementos pequeños y completos, que se preparan uno a uno.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 520" width="100%" role="img" aria-label="Recorrido de LecturaFàcil por el método, de la visión al cierre" style="font-family:'DM Sans',Arial,sans-serif;display:block">
<text x="14" y="24" font-size="15.5" font-weight="700" fill="#004d47">El recorrido de LecturaFàcil por la fábrica</text>
<line x1="14" y1="38" x2="546" y2="38" stroke="#e0f4f3" stroke-width="2"/>
<line x1="34" y1="64" x2="34" y2="482" stroke="#b2deda" stroke-width="2"/>
<circle cx="34" cy="64" r="7" fill="#00726b"/><text x="56" y="62" font-size="14.5" font-weight="700" fill="#004d47">Visión<tspan font-size="12.5" font-weight="700" fill="#00726b">   ✓ escrita</tspan></text><text x="56" y="80" font-size="12.5" fill="#555">el mismo Kant para Yasmin, Pau y su clase</text>
<rect x="290" y="98" width="120" height="22" rx="11" fill="#00726b"/><text x="350" y="113" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">estás aquí</text>
<circle cx="34" cy="134" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="132" font-size="14.5" font-weight="700" fill="#004d47">Especificación funcional global</text><text x="56" y="150" font-size="12.5" fill="#555">funcionalidades, recorridos, pantallas, estados, criterios</text>
<circle cx="34" cy="194" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="192" font-size="14.5" font-weight="700" fill="#004d47">Definición técnica</text><text x="56" y="210" font-size="12.5" fill="#555">tecnologías, arquitectura, datos, integraciones, pruebas</text>
<circle cx="34" cy="254" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="252" font-size="14.5" font-weight="700" fill="#004d47">Devslices</text><text x="56" y="270" font-size="12.5" fill="#555">incrementos verticales para construirlas</text>
<circle cx="34" cy="314" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="312" font-size="14.5" font-weight="700" fill="#004d47">Preparación</text><text x="56" y="330" font-size="12.5" fill="#555">criterios, pruebas previstas y tareas</text>
<circle cx="34" cy="374" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="372" font-size="14.5" font-weight="700" fill="#004d47">Desarrollo</text><text x="56" y="390" font-size="12.5" fill="#555">pruebas, después lógica y datos, después interfaz</text>
<circle cx="34" cy="434" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="432" font-size="14.5" font-weight="700" fill="#004d47">Cierre</text><text x="56" y="450" font-size="12.5" fill="#555">evidencias, informe y tarjeta terminada</text>
<path d="M436,246 H448 V456 H436" fill="none" stroke="#00726b" stroke-width="2"/>
<text x="458" y="340" font-size="12.5" font-weight="700" fill="#00726b">el tablero</text>
<text x="458" y="357" font-size="12.5" fill="#555">registra</text>
<text x="458" y="374" font-size="12.5" fill="#555">cada paso</text>
<text x="34" y="508" font-size="12.5" font-style="italic" fill="#888">y si surge una mejora general, va a la fábrica, no a LecturaFàcil</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">El mismo recorrido sirve para cualquier proyecto. LecturaFàcil acaba de cerrar el primer paso.</figcaption>
</figure>

Mientras se construye, el estado vive en tu tablero, JKanban. Claude lo consulta y no da nada por anotado hasta que el tablero lo confirma. Las skills que usa salen de un único sitio, con su versión y su procedencia. Y cuando algo se puede hacer mejor, la fábrica lo propone, pero no cambia nada sin tu aprobación.

El resto del documento sigue a LecturaFàcil capítulo a capítulo, desde la visión hasta su primera devslice cerrada.

---

## Por qué una fábrica

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 1 · Antes de empezar</p>
<p>Antes de dar el siguiente paso, miras <code>D:\Projectes</code>. PoseTracker tiene su «doctrina», OncoCore sus propias instrucciones y JKanban guarda en su <code>CLAUDE.md</code> la lección de la función <code>jsq()</code> contra el XSS. Cada proyecto ha aprendido algo, y nada de eso ha llegado a los demás. ¿Con qué reglas empezará LecturaFàcil?</p>
</div>

Hoy trabajas como un buen artesano: cada pieza sale bien, pero cada taller tiene sus herramientas y sus notas. Una fábrica no es menos cuidadosa; es un taller con **recetario común**. Los pasos son los mismos en cada proyecto, las herramientas están en un sitio conocido y lo que se aprende en uno pasa al siguiente.

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
<p>La visión de LecturaFàcil emociona, pero deja muchas preguntas sin respuesta. ¿Qué ve el docente si la IA no consigue adaptar un texto? ¿Dónde se guarda cómo lee cada alumno, y quién puede verlo? ¿La adaptación la hace un agente dentro del producto? Nadie debería responderlas a mitad de una devslice.</p>
</div>

Primero viene la **especificación funcional global**: el comportamiento del producto entero. Sus funcionalidades no salen solo de la visión. Salen también de las referencias, como la presentación de la Coordinadora Balear y los enunciados de Jaume Serra, y del estudio de mercado de la propia visión, con productos como Diffit o SUMM AI. Y de cualquier otra fuente de requisitos.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 604" width="100%" role="img" aria-label="Lo que se define en la especificación funcional y en la definición técnica de LecturaFàcil" style="font-family:'DM Sans',Arial,sans-serif;display:block">
<text x="14" y="24" font-size="15" font-weight="700" fill="#004d47">Especificación funcional global</text>
<text x="34" y="60" font-size="13.5" font-weight="700" fill="#004d47">Funcionalidades y reglas</text><text x="34" y="77" font-size="12" fill="#555">perfiles de lector, dial, línea roja, ayudas</text>
<text x="34" y="102" font-size="13.5" font-weight="700" fill="#004d47">Recorridos de usuario</text><text x="34" y="119" font-size="12" fill="#555">pegar un texto, elegir el grupo, revisar, aprobar</text>
<text x="34" y="144" font-size="13.5" font-weight="700" fill="#004d47">Pantallas e interacción</text><text x="34" y="161" font-size="12" fill="#555">diseñadas antes de elegir la técnica</text>
<text x="34" y="186" font-size="13.5" font-weight="700" fill="#004d47">Estados</text><text x="34" y="203" font-size="12" fill="#555">texto vacío, la IA falla, quién ve cada perfil</text>
<text x="34" y="228" font-size="13.5" font-weight="700" fill="#004d47">Criterios comprobables</text><text x="34" y="245" font-size="12" fill="#555">«los conceptos de la materia no cambian»</text>
<text x="34" y="270" font-size="13.5" font-weight="700" fill="#004d47">Contratos de API</text><text x="34" y="287" font-size="12" fill="#555">si hay servidor: entradas, salidas y errores</text>
<path d="M22,38 H16 V286 H22" fill="none" stroke="#00726b" stroke-width="2"/>
<text x="14" y="326" font-size="15" font-weight="700" fill="#004d47">Definición técnica y arquitectura</text>
<text x="34" y="362" font-size="13.5" font-weight="700" fill="#004d47">Tecnologías y plataforma</text><text x="34" y="379" font-size="12" fill="#555">web o escritorio, partiendo de tus favoritas</text>
<text x="34" y="404" font-size="13.5" font-weight="700" fill="#004d47">Arquitectura y datos</text><text x="34" y="421" font-size="12" fill="#555">capas, SQL nativo y migraciones versionadas</text>
<text x="34" y="446" font-size="13.5" font-weight="700" fill="#004d47">Integraciones</text><text x="34" y="463" font-size="12" fill="#555">la IA que adapta, pictogramas, la voz de TextAid</text>
<text x="34" y="488" font-size="13.5" font-weight="700" fill="#004d47">¿Un agente dentro del producto?</text><text x="34" y="505" font-size="12" fill="#555">Claude adaptando textos, con sus límites</text>
<text x="34" y="530" font-size="13.5" font-weight="700" fill="#004d47">Pruebas y distribución</text><text x="34" y="547" font-size="12" fill="#555">cómo se comprueba y cómo llega al centro</text>
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
<text x="30" y="402" font-size="12" fill="#888">Si la IA no puede adaptar: aviso, y el original queda intacto</text>
<rect x="290" y="418" width="110" height="32" rx="16" fill="#fff" stroke="#00726b" stroke-width="1.5"/><text x="345" y="439" text-anchor="middle" font-size="12.5" font-weight="700" fill="#00726b">Ajustar regla</text>
<rect x="410" y="418" width="120" height="32" rx="16" fill="#00726b"/><text x="470" y="439" text-anchor="middle" font-size="12.5" font-weight="700" fill="#fff">Aprobar</text>
<text x="30" y="474" font-size="11.5" font-style="italic" fill="#888">nada llega a la clase sin el visto bueno del docente</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Boceto ilustrativo de la pantalla de revisión, con la hoja de Yasmin y los cambios que recoge su documento de visión.</figcaption>
</figure>

Diseñada antes, la interfaz marca lo que la técnica tiene que servir, y no al revés. Lo que se dibuja aquí se convierte después en criterios comprobables.

### El contexto tecnológico

La definición técnica empieza por el **contexto**: dónde vivirá el producto y con qué convive. LecturaFàcil se usará en un instituto donde el alumnado ya trabaja con Google Classroom y escucha textos con TextAid. Ese contexto decide si conviene una aplicación web, qué integraciones hacen falta y qué datos de los alumnos pueden salir del centro.

Con el contexto claro se eligen las tecnologías. Tus favoritas son el punto de partida: React y FastAPI para la web, Python para el escritorio pequeño, SQLite cuando encaje y SQL nativo sin ORM. Cada una se confirma para este proyecto, y cada excepción queda escrita con su razón.

### La arquitectura

Falta decidir qué piezas tiene el producto y cómo se hablan. Una buena **arquitectura** separa lo que no debe mezclarse. Las reglas de la Lectura Fácil no dependen de la pantalla ni de la base de datos. Y la IA que adapta los textos se conecta por un adaptador, sin contaminar esas reglas.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 506" width="100%" role="img" aria-label="Arquitectura posible de LecturaFàcil por capas" style="font-family:'DM Sans',Arial,sans-serif;display:block">
<defs><marker id="vc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#004d47"/></marker></defs>
<text x="280" y="22" text-anchor="middle" font-size="13" fill="#555">el docente, en el navegador</text>
<line x1="280" y1="30" x2="280" y2="50" stroke="#004d47" stroke-width="2" marker-end="url(#vc)"/>
<rect x="80" y="54" width="400" height="56" rx="8" fill="#fff" stroke="#00726b" stroke-width="1.5"/>
<text x="280" y="78" text-anchor="middle" font-size="14.5" font-weight="700" fill="#004d47">Interfaz</text>
<text x="280" y="98" text-anchor="middle" font-size="12" fill="#555">revisión, grupos y hojas · React, la favorita</text>
<line x1="280" y1="112" x2="280" y2="132" stroke="#004d47" stroke-width="2" marker-end="url(#vc)"/>
<rect x="80" y="136" width="400" height="56" rx="8" fill="#fff" stroke="#00726b" stroke-width="1.5"/>
<text x="280" y="160" text-anchor="middle" font-size="14.5" font-weight="700" fill="#004d47">Casos de uso</text>
<text x="280" y="180" text-anchor="middle" font-size="12" fill="#555">adaptar, revisar, aprobar, afinar · API con FastAPI</text>
<line x1="280" y1="194" x2="280" y2="214" stroke="#004d47" stroke-width="2" marker-end="url(#vc)"/>
<rect x="80" y="218" width="400" height="62" rx="8" fill="#00726b"/>
<text x="280" y="244" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">Dominio</text>
<text x="280" y="266" text-anchor="middle" font-size="12" fill="#e0f4f3">perfiles, dial, reglas y línea roja · sin pantallas ni SQL</text>
<text x="280" y="306" text-anchor="middle" font-size="12" font-style="italic" fill="#888">lo externo, en el borde, detrás de un adaptador</text>
<ellipse cx="62" cy="336" rx="22" ry="6" fill="#e0f4f3" stroke="#00726b"/><path d="M40,336 V364 A22,6 0 0 0 84,364 V336" fill="#e0f4f3" stroke="#00726b"/><ellipse cx="62" cy="336" rx="22" ry="6" fill="#e0f4f3" stroke="#00726b"/>
<text x="104" y="346" font-size="14" font-weight="700" fill="#004d47">Datos</text><text x="104" y="364" font-size="12" fill="#555">grupos y perfiles · SQL nativo, migraciones versionadas</text>
<circle cx="62" cy="414" r="18" fill="#fff" stroke="#00726b" stroke-width="1.5"/><text x="62" y="419" text-anchor="middle" font-size="13" font-weight="700" fill="#00726b">IA</text>
<text x="104" y="410" font-size="14" font-weight="700" fill="#004d47">Agente que adapta</text><text x="104" y="428" font-size="12" fill="#555">Claude Code con sus propias skills, versionadas aparte</text>
<rect x="44" y="460" width="36" height="28" rx="5" fill="#fff" stroke="#00726b" stroke-width="1.5"/><text x="62" y="479" text-anchor="middle" font-size="11" font-weight="700" fill="#00726b">ext</text>
<text x="104" y="472" font-size="14" font-weight="700" fill="#004d47">Servicios externos</text><text x="104" y="490" font-size="12" fill="#555">pictogramas de ARASAAC, la voz de TextAid</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Una arquitectura posible para LecturaFàcil: las reglas en el centro y lo externo en los bordes. Ilustrativa: se decide en la definición técnica.</figcaption>
</figure>

Si Claude Code trabaja dentro del producto, sus instrucciones y skills se versionan aparte de las que usamos para desarrollarlo. Así, mejorar la fábrica nunca cambia sin querer cómo adapta un texto. Con la interfaz, el contexto y la arquitectura definidos, cada decisión queda escrita con su porqué, y ya nada importante se decide sobre la marcha.

---

## Cómo se construye, devslice a devslice

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 4 · Repartir el trabajo</p>
<p>La especificación ya reúne las funcionalidades de LecturaFàcil, y la definición técnica, con qué se construirán. Ahora toca decidir cómo construirlas. Lo fácil sería ir funcionalidad a funcionalidad, o hacer primero toda la base de datos y después todas las pantallas. Pero así no habría nada que enseñar a un docente durante semanas. ¿Cómo se trocea para que cada paso entregue algo que funcione?</p>
</div>

Las funcionalidades dicen **qué** hará LecturaFàcil. Las **devslices** dicen **cómo se construye**: incrementos verticales que atraviesan interfaz, lógica, datos y pruebas, y que al terminar dejan algo que un docente puede usar. Una devslice puede tocar varias funcionalidades, y una funcionalidad grande se completa a lo largo de varias devslices. El plan fija su orden y sus dependencias, y cada devslice queda registrada en el tablero.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 372" width="100%" role="img" aria-label="Funcionalidades de LecturaFàcil en columnas y devslices en filas que tocan varias" style="font-family:'DM Sans',Arial,sans-serif;display:block">
<text x="14" y="24" font-size="15.5" font-weight="700" fill="#004d47">Funcionalidades y devslices · LecturaFàcil</text>
<text x="14" y="62" font-size="12.5" font-weight="700" fill="#00726b">devslices, en orden</text>
<text x="428" y="40" text-anchor="middle" font-size="12" font-weight="700" fill="#00726b">funcionalidades</text>
<text x="318" y="62" text-anchor="middle" font-size="11" fill="#555">perfiles</text>
<text x="362" y="62" text-anchor="middle" font-size="11" fill="#555">dial</text>
<text x="406" y="62" text-anchor="middle" font-size="11" fill="#555">reglas</text>
<text x="452" y="62" text-anchor="middle" font-size="11" fill="#555">revisión</text>
<text x="498" y="62" text-anchor="middle" font-size="11" fill="#555">ayudas</text>
<text x="538" y="62" text-anchor="middle" font-size="11" fill="#555">grados</text>
<line x1="14" y1="72" x2="546" y2="72" stroke="#e0f4f3" stroke-width="2"/>
<line x1="318" y1="76" x2="318" y2="334" stroke="#b2deda" stroke-width="1" stroke-dasharray="2 4"/>
<line x1="362" y1="76" x2="362" y2="334" stroke="#b2deda" stroke-width="1" stroke-dasharray="2 4"/>
<line x1="406" y1="76" x2="406" y2="334" stroke="#b2deda" stroke-width="1" stroke-dasharray="2 4"/>
<line x1="452" y1="76" x2="452" y2="334" stroke="#b2deda" stroke-width="1" stroke-dasharray="2 4"/>
<line x1="498" y1="76" x2="498" y2="334" stroke="#b2deda" stroke-width="1" stroke-dasharray="2 4"/>
<line x1="538" y1="76" x2="538" y2="334" stroke="#b2deda" stroke-width="1" stroke-dasharray="2 4"/>
<text x="14" y="100" font-size="13.5" font-weight="700" fill="#004d47">Primera adaptación de punta a punta</text><text x="14" y="118" font-size="11.5" fill="#555">un perfil, Lectura Fácil, línea roja y visto bueno</text>
<circle cx="318" cy="104" r="6" fill="#00726b"/>
<circle cx="362" cy="104" r="6" fill="#00726b"/>
<circle cx="406" cy="104" r="6" fill="#00726b"/>
<circle cx="452" cy="104" r="6" fill="#00726b"/>
<text x="14" y="152" font-size="13.5" font-weight="700" fill="#004d47">Todos los perfiles y el dial</text><text x="14" y="170" font-size="11.5" fill="#555">dislexia, recién llegado… y los tres niveles</text>
<circle cx="318" cy="156" r="6" fill="#9d5ce0"/>
<circle cx="362" cy="156" r="6" fill="#9d5ce0"/>
<circle cx="406" cy="156" r="6" fill="#9d5ce0"/>
<text x="14" y="204" font-size="13.5" font-weight="700" fill="#004d47">Ajustar una regla y recordarla</text><text x="14" y="222" font-size="11.5" fill="#555">el cambio del docente se guarda en el perfil</text>
<circle cx="318" cy="208" r="6" fill="#9d5ce0"/>
<circle cx="406" cy="208" r="6" fill="#9d5ce0"/>
<circle cx="452" cy="208" r="6" fill="#9d5ce0"/>
<text x="14" y="256" font-size="13.5" font-weight="700" fill="#004d47">El glosario al lado del texto</text><text x="14" y="274" font-size="11.5" fill="#555">con pictograma y lengua materna</text>
<circle cx="452" cy="260" r="6" fill="#9d5ce0"/>
<circle cx="498" cy="260" r="6" fill="#9d5ce0"/>
<text x="14" y="308" font-size="13.5" font-weight="700" fill="#004d47">Retirar una ayuda por grados</text><text x="14" y="326" font-size="11.5" fill="#555">proponer menos apoyo cuando el alumno avanza</text>
<circle cx="318" cy="312" r="6" fill="#9d5ce0"/>
<circle cx="498" cy="312" r="6" fill="#9d5ce0"/>
<circle cx="538" cy="312" r="6" fill="#9d5ce0"/>
<text x="14" y="362" font-size="12.5" font-style="italic" fill="#888">cada fila, de punta a punta: interfaz, lógica, datos y pruebas</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Cada devslice toma un trozo de varias funcionalidades y lo construye entero. Plan ilustrativo.</figcaption>
</figure>

Una devslice planificada todavía no está preparada. Cuando le llega el turno a la primera, «Primera adaptación de punta a punta», hay que decidir qué cuenta como hecho.

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · preparando la devslice</p>
<p class="escena-contexto">Tú y Claude afináis los criterios de aceptación.</p>
<div class="turno"><p class="ponente">Claude<small>propone</small></p><p>Criterio: la versión de Lectura Fácil tiene frases de diez palabras o menos. Prueba prevista: adaptar el fragmento de Kant y medir cada frase.</p></div>
<div class="turno"><p class="ponente">Tú<small>matiza</small></p><p>Falta la línea roja. Puede ser muy fácil y haber perdido a Kant. Quiero que «enteniment», «minoria d'edat» y «Sapere aude» sigan ahí.</p></div>
<div class="turno"><p class="ponente">Claude<small>acepta</small></p><p>Segundo criterio, entonces: los conceptos marcados se conservan en todas las versiones. Escribo esa prueba antes que el código, y debe fallar hasta que la adaptación los respete.</p></div>
<p class="escena-pie">Diálogo imaginado: muestra cómo se prepara una devslice, no una conversación real.</p>
</div>

Así avanza cada devslice: **planificada en el plan y preparada antes de construirse**, con alcance, criterios, pruebas previstas y tareas. Después se escriben las pruebas y se construye empezando por la lógica y los datos: las reglas, los perfiles y lo que se guarda. La interfaz llega al final, y se comprueba el recorrido completo. Las pruebas siguen vivas cuando la devslice se cierra, porque pertenecen a LecturaFàcil.

---

## Qué muestra el tablero

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 5 · El tablero responde</p>
<p>Las tareas de la devslice ya están en JKanban, dentro del proyecto LecturaFàcil. Claude empieza a trabajar y quiere mover la primera a «En desarrollo». ¿Y si algo falla?</p>
</div>

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · una operación que no se confirma</p>
<p class="escena-contexto">Claude intenta actualizar el tablero.</p>
<div class="turno"><p class="ponente">Claude<small>pide</small></p><p>Mover «Escribir la prueba de la línea roja» a En desarrollo.</p></div>
<div class="turno arnes"><p class="ponente">JKanban<small>responde</small></p><p>403 · UserNotInProject: el usuario no tiene acceso al proyecto.</p></div>
<div class="turno"><p class="ponente">Claude<small>informa</small></p><p>No he podido mover la tarea: mi usuario no es miembro de LecturaFàcil. Sigue en Preparada. ¿Me añades al equipo?</p></div>
<p class="escena-pie">Diálogo imaginado. El error y su código existen en JKanban; la situación es un ejemplo.</p>
</div>

El tablero es tu **ventana permanente** al trabajo. Cada devslice tiene sus tareas, y cada tarea su estado, sus dependencias y sus bloqueos, con el motivo a la vista. Claude lo consulta para retomar después de una pausa y lo actualiza mientras trabaja. Hay una regla que no se negocia: nada está anotado hasta que JKanban lo confirma. Un error se ve; no se esconde.

---

## De dónde salen las herramientas

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 6 · La caja de herramientas</p>
<p>Para construir la adaptación, Claude necesita skills: preparar devslices, diseñar pruebas, operar el tablero. ¿Las de qué carpeta? ¿En qué versión?</p>
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
<p class="caso-etiqueta">El caso · capítulo 7 · Una lección que viaja</p>
<p>El documento de visión de LecturaFàcil se generó con la paleta y el emblema de un instituto. Pero el script que lo convierte en página importa código de OncoCore y su hoja de estilos. Si OncoCore no estuviera en este ordenador, la skill no funcionaría. ¿Es un problema de LecturaFàcil o de la fábrica?</p>
</div>

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · una propuesta de mejora</p>
<div class="turno"><p class="ponente">Claude<small>propone</small></p><p>Mejora para SoftwareFactory: que la skill de visión funcione sin depender de OncoCore. Origen: LecturaFàcil, documento de visión. Evidencia: su script carga <code>md_to_html</code> desde la carpeta de OncoCore. La registro en el proyecto SoftwareFactory y espero tu aprobación.</p></div>
<div class="turno"><p class="ponente">Tú<small>decide</small></p><p>Regístrala. La miramos antes de publicar la primera versión.</p></div>
<p class="escena-pie">Diálogo imaginado. La dependencia es real; la propuesta todavía no está registrada.</p>
</div>

La fábrica tiene una tarea que nunca se cierra: **Mejorar la Software Factory**. Mientras trabaja en cualquier proyecto, Claude observa fricciones, errores repetidos y pasos de más. Cada mejora general va al proyecto SoftwareFactory del tablero, con su origen y su evidencia. Lo que es propio de LecturaFàcil se queda en LecturaFàcil.

Proponer no es cambiar. Ninguna mejora se aplica ni se distribuye sin tu aprobación expresa. La fábrica aprende rápido, pero el método sigue siendo tuyo.

---

## En qué se diferencia de lo que ya existe

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 8 · Mirar alrededor</p>
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

Los productos del gráfico: [Spec Kit](https://github.github.com/spec-kit/), [Superpowers](https://github.com/obra/superpowers) y [BMAD](https://github.com/bmad-code-org/BMAD-METHOD).

Son buenas propuestas, y por eso no son rivales. Spec Kit [cumplió un año en agosto de 2026 y publicó su versión 1.0.0](https://github.github.com/spec-kit/history.html), con 38 agentes compatibles. Pero cada una trae su método, y tú ya tienes el tuyo, que empieza con un documento de visión para personas, como el de LecturaFàcil. SoftwareFactory **toma las piezas que sirven a tu método**, como dos skills de Superpowers que son candidatas, y las guarda con su procedencia.

---

## De vuelta al caso

<div class="caso">
<p class="caso-etiqueta">El caso · epílogo</p>
<p>LecturaFàcil sigue teniendo la misma pregunta: cómo dar el mismo Kant a toda la clase sin bajar la exigencia. Lo que ha cambiado es el camino para responderla. Su primera devslice se ha preparado antes de escribir código y tiene una prueba que protege la línea roja. El tablero ha seguido cada paso, y cuando algo falló, el error se vio. Además, el piloto ha dejado una primera propuesta en el proyecto <strong>SoftwareFactory</strong>.</p>
<p>Lo que la fábrica no decide es lo que te corresponde: con qué tecnología se construye LecturaFàcil, si una mejora se aplica y cuándo se publica una versión. <strong>La fábrica prepara, construye y propone; las decisiones son tuyas.</strong></p>
</div>

---

## Anexo: el caso LecturaFàcil

### Qué es real

LecturaFàcil está en `D:\Projectes\LecturaFacil`, en fase inicial de definición. Contiene su documento de visión (`doc/vision/documento-vision.md` y su `.html`) y dos referencias: la presentación de la Coordinadora Balear de Persones amb Discapacitat (21 de octubre de 2026) y los enunciados de Jaume Serra (2008). Todavía no tiene especificación funcional ni código. Es el proyecto piloto de SoftwareFactory por decisión del propietario.

El fragmento citado sale de su documento de visión. Su historia es ficticia; Yasmin y Pau son personajes inventados. El error `UserNotInProject` de la escena es una excepción real de JKanban (`docs/business-rules.md`). La dependencia de la skill de visión respecto a OncoCore consta en su script `doc_to_html.py`.

### Qué es ilustrativo

El plan de devslices, su orden, sus criterios y sus tareas son ejemplos sacados de la visión. Las escenas y la propuesta de mejora son imaginadas. Los proyectos LecturaFàcil y SoftwareFactory todavía no existen en JKanban, y la integración de Claude con el tablero aún no está construida.

### Fuentes

Consultadas el 25 de octubre de 2026:

- Eric Risco, [*Programar con agentes ya no basta: monta tu Software Factory*](https://www.youtube.com/watch?v=p6nnqerea7w), YouTube.
- [Spec Kit](https://github.github.com/spec-kit/), de GitHub, y [su historia](https://github.github.com/spec-kit/history.html). Licencia MIT.
- [Superpowers](https://github.com/obra/superpowers), de Jesse Vincent. Licencia MIT.
- [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD), de BMad Code.

---

*Documento de visión de SoftwareFactory — 2026-10-25.*
