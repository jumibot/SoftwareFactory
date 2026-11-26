<!-- destino: proyecto -->
# Claude Code Commander: quien dirige tu orquesta

**Estado:** 27 de octubre de 2026, borrador 0.1.0.

<div class="caso">
<p class="caso-etiqueta">El caso · prólogo · la noche del 27 de octubre</p>
<p>Es martes, 27 de octubre de 2026. A las 00:08 haces commit en SoftwareFactory y, en el mismo minuto, en SmartColdBox. Hasta las dos y cuarto trabajas en tres sesiones de Claude Code a la vez: la SF, SmartColdBox y JKanban. Por la mañana sigues, y a las tres de la tarde llevas 94 commits entre los tres proyectos. La sesión de la SF arranca diciendo «Sin SF» en su propio repositorio. Mientras lo investigas, pides alinear una ventana y preguntas si podría flotar fuera de la terminal. El 1 de diciembre abre Turboconvo, y la memoria de SmartColdBox está sin empezar. <strong>Tocas todos los instrumentos. ¿Quién dirige la orquesta?</strong></p>
</div>

## Resumen operativo

El **Claude Code Commander** (en corto, el CCC) es tu puesto de mando. Es una aplicación de la SF que ve a la vez todas tus sesiones de Claude Code y las conduce. La abres en el ordenador, en la tableta o en el móvil. Es una ventana que flota por encima de todo, también fuera de casa.

Desde el CCC ves cada sesión con su proyecto, su fase, lo que tiene en curso y lo que espera de ti. Le das órdenes, abres y cierras sesiones, y lanzas sobre ellas las tareas de JKanban. Mientras tanto, el CCC mide cuántos frentes tienes abiertos y cuánto dejas a medias, y te avisa cuando te dispersas.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 430" width="100%" role="img" aria-label="El CCC reúne las tres sesiones de la noche del 27 de octubre" style="font-family:var(--fuente-texto);display:block">
<text x="280" y="26" text-anchor="middle" font-size="14.5" font-weight="700" fill="#004d47">Tú</text>
<text x="280" y="46" text-anchor="middle" font-size="12.5" fill="#555">en el ordenador, la tableta o el móvil</text>
<line x1="280" y1="58" x2="280" y2="92" stroke="#00726b" stroke-width="2"/>
<polygon points="274,86 286,86 280,96" fill="#00726b"/>
<rect x="150" y="100" width="260" height="62" rx="10" fill="#e6f4f2" stroke="#00726b" stroke-width="2"/>
<text x="280" y="127" text-anchor="middle" font-size="15.5" font-weight="700" fill="#004d47">Claude Code Commander</text>
<text x="280" y="148" text-anchor="middle" font-size="12.5" fill="#555">ve, ordena, lanza y mide</text>
<line x1="280" y1="162" x2="280" y2="196" stroke="#00726b" stroke-width="2"/>
<text x="292" y="184" font-size="12" fill="#555">órdenes ↓ · estado ↑</text>
<line x1="90" y1="200" x2="470" y2="200" stroke="#00726b" stroke-width="2"/>
<line x1="90" y1="200" x2="90" y2="222" stroke="#00726b" stroke-width="2"/>
<line x1="280" y1="200" x2="280" y2="222" stroke="#00726b" stroke-width="2"/>
<line x1="470" y1="200" x2="470" y2="222" stroke="#00726b" stroke-width="2"/>
<rect x="14" y="226" width="152" height="54" rx="8" fill="none" stroke="#8e44ad" stroke-width="1.6"/>
<text x="90" y="250" text-anchor="middle" font-size="13.5" font-weight="700" fill="#6c3483">SoftwareFactory</text>
<text x="90" y="268" text-anchor="middle" font-size="12" fill="#555">su sesión, su mod</text>
<rect x="204" y="226" width="152" height="54" rx="8" fill="none" stroke="#0e7490" stroke-width="1.6"/>
<text x="280" y="250" text-anchor="middle" font-size="13.5" font-weight="700" fill="#0e7490">SmartColdBox</text>
<text x="280" y="268" text-anchor="middle" font-size="12" fill="#555">su sesión, su mod</text>
<rect x="394" y="226" width="152" height="54" rx="8" fill="none" stroke="#475569" stroke-width="1.6"/>
<text x="470" y="250" text-anchor="middle" font-size="13.5" font-weight="700" fill="#334155">JKanban</text>
<text x="470" y="268" text-anchor="middle" font-size="12" fill="#555">su sesión, su mod</text>
<text x="280" y="318" text-anchor="middle" font-size="13" fill="#1a1a1a">Cada mod cuenta al CCC cómo va su sesión</text>
<text x="280" y="338" text-anchor="middle" font-size="13" fill="#1a1a1a">y ejecuta solo las órdenes de su proyecto.</text>
<text x="280" y="378" text-anchor="middle" font-size="13" fill="#1a1a1a">El CCC nunca escribe en un proyecto:</text>
<text x="280" y="398" text-anchor="middle" font-size="13" fill="#1a1a1a">«un proyecto por sesión» se cumple siempre.</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Las tres sesiones reales de la noche, bajo un solo puesto de mando.</figcaption>
</figure>

Lo que sigue cuenta ese día con el CCC delante, capítulo a capítulo. Al final, cómo está hecho y en qué se diferencia de lo que ya existe.

## Por qué hace falta un director

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 1 · la sesión que no se reconoce</p>
<p>Abres la sesión de la SF y la línea de estado dice «Sin SF». Pones a mano el color y el nombre que el mod debía poner. Al rato, Claude intenta corregir el mod y el propio mod lo bloquea: «esta sesión es de .». Mientras tanto, a SmartColdBox le quedan tres mejoras para la SF que solo ves porque las escribió en un archivo. <strong>¿Cómo sabes qué pasa en una sesión que no estás mirando?</strong></p>
</div>

Cada sesión de Claude Code es una isla. Vive en su terminal, con su proyecto y su conversación, y no ve a las demás. El mod de la SF ya ordena mucho dentro de cada una. Lleva la fase, la cola de peticiones, el marcador del día y la regla de un proyecto por sesión. Pero solo ve su sesión.

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · las 00:40, en la sesión de la SF</p>
<p class="escena-contexto">Tres sesiones abiertas. Tú estás en la de la SF.</p>
<div class="turno"><p class="ponente">Tú<small>a Claude</small></p><p>¿Cómo va SmartColdBox? ¿Ha terminado el anexo de la patente?</p></div>
<div class="turno"><p class="ponente">Claude<small>sesión de la SF</small></p><p>No lo sé. No veo otras sesiones: tendrías que mirar su terminal o su historial.</p></div>
<div class="turno"><p class="ponente">Tú<small>a Claude</small></p><p>Entonces la orquesta la dirijo yo, de memoria.</p></div>
<p class="escena-pie">Diálogo imaginado: no es una transcripción ni un resultado validado.</p>
</div>

La escena muestra el hueco. El estado de conjunto vive solo en tu cabeza, y retomar cuesta. En un estudio con 10.000 sesiones de programadores, solo el 10 % empezó a editar en menos de un minuto tras una interrupción ([Parnin y Rugaber, 2010](https://sites.cc.gatech.edu/reverse/repository/resumptionstrategies.pdf)).

La visión [«el hombre orquesta»](hombre-orquesta.html) ya pedía un solo centro para todos tus trabajos. El CCC es la pieza que lo hace visible y manejable: el director que mira todas las sesiones a la vez.

## Qué ves de un vistazo

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 2 · las tres de la tarde, lejos de la mesa</p>
<p>Has bajado a por un café con el móvil en la mano. Abres el CCC y aparecen tus sesiones, cada una con su color. La SF trabaja en la visión del CCC; SmartColdBox cierra su visión; JKanban publicó la versión 1.0.0 a las 10:27. <strong>¿Qué necesitas ver para decidir sin volver a la terminal?</strong></p>
</div>

La ventana del CCC es una lista de tarjetas, una por sesión. Cada tarjeta lleva el color del proyecto, el mismo que el mod pone a la sesión. Dentro va lo que hoy muestra la caja sobre el prompt: la fase, lo que está en curso, la cola y los avisos.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 470" width="100%" role="img" aria-label="Boceto de la ventana del CCC a las 15:03 del 27 de octubre" style="font-family:var(--fuente-texto);display:block">
<rect x="10" y="6" width="540" height="456" rx="16" fill="none" stroke="#9aa5b1" stroke-width="1.5"/>
<text x="34" y="38" font-size="15" font-weight="700" fill="#004d47">Claude Code Commander</text>
<text x="526" y="38" text-anchor="end" font-size="12.5" fill="#555">martes 27 · 15:03</text>
<line x1="34" y1="52" x2="526" y2="52" stroke="#d9dee3"/>
<rect x="34" y="66" width="6" height="96" rx="3" fill="#8e44ad"/>
<text x="54" y="84" font-size="14" font-weight="700" fill="#6c3483">SoftwareFactory</text>
<text x="54" y="104" font-size="12.5" fill="#1a1a1a">▶ Documento de visión del Claude Code Commander</text>
<text x="54" y="124" font-size="12.5" fill="#555">sin probar 7 · propuestas por revisar 17</text>
<text x="54" y="144" font-size="12.5" fill="#555">60 commits hoy · último a las 15:03</text>
<rect x="34" y="180" width="6" height="96" rx="3" fill="#0e7490"/>
<text x="54" y="198" font-size="14" font-weight="700" fill="#0e7490">SmartColdBox · 1/7 visión</text>
<text x="54" y="218" font-size="12.5" fill="#1a1a1a">cerrando la visión; después, la especificación</text>
<text x="54" y="238" font-size="12.5" fill="#555">22 commits hoy · último a las 14:41</text>
<text x="54" y="258" font-size="12.5" fill="#991b1b">Turboconvo abre el 1 de diciembre · memoria sin empezar</text>
<rect x="34" y="294" width="6" height="76" rx="3" fill="#475569"/>
<text x="54" y="312" font-size="14" font-weight="700" fill="#334155">JKanban</text>
<text x="54" y="332" font-size="12.5" fill="#1a1a1a">versión 1.0.0 publicada a las 10:27</text>
<text x="54" y="352" font-size="12.5" fill="#555">12 commits hoy · último a las 10:27</text>
<line x1="34" y1="390" x2="526" y2="390" stroke="#d9dee3"/>
<text x="34" y="416" font-size="12.5" fill="#1a1a1a">Hoy: 3 proyectos con commits · 94 commits · desde las 00:08</text>
<text x="34" y="440" font-size="12.5" fill="#555">Esta noche, tres frentes a la vez durante dos horas</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Boceto. Los datos son los reales de ese momento; la forma de la ventana, no.</figcaption>
</figure>

Las cifras del boceto no salen de ningún informe: las cuenta cada mod mientras trabajas. Por eso la ventana está al día sin que nadie la rellene.

Lo que pide tu atención va en rojo y arriba: un aviso del mod, una petición bloqueada o un plazo que se acerca. Lo demás espera a que lo mires. Así, el café dura un café.

## Cómo llegan las órdenes a cada sesión

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 3 · una orden desde el sofá</p>
<p>En la tarjeta de la SF ves la caja del mod alineada a la izquierda, y no te gusta. Escribes en el móvil: «alinea la ventana a la derecha». No abres ninguna terminal. <strong>¿Cómo llega esa frase a la sesión correcta sin saltarse ninguna regla?</strong></p>
</div>

El CCC no toca los proyectos. Deja la orden para una sesión concreta, y el mod de esa sesión la recoge. Es como un director que da la entrada: cada músico toca su propio instrumento.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 452" width="100%" role="img" aria-label="Recorrido de la orden «alinea la ventana a la derecha»" style="font-family:var(--fuente-texto);display:block">
<line x1="34" y1="26" x2="34" y2="416" stroke="#b2deda" stroke-width="2"/>
<circle cx="34" cy="26" r="7" fill="#00726b"/><text x="56" y="24" font-size="14.5" font-weight="700" fill="#004d47">Tú, en el móvil</text><text x="56" y="42" font-size="12.5" fill="#555">«alinea la ventana a la derecha», en la tarjeta de la SF</text>
<circle cx="34" cy="104" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="102" font-size="14.5" font-weight="700" fill="#004d47">El CCC</text><text x="56" y="120" font-size="12.5" fill="#555">guarda la orden para la sesión de SoftwareFactory</text>
<circle cx="34" cy="182" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="180" font-size="14.5" font-weight="700" fill="#004d47">El mod de esa sesión</text><text x="56" y="198" font-size="12.5" fill="#555">la recoge y la anota en su cola de peticiones</text>
<circle cx="34" cy="260" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="258" font-size="14.5" font-weight="700" fill="#004d47">Claude, en su sesión</text><text x="56" y="276" font-size="12.5" fill="#555">cambia una línea, sube la versión y hace commit</text>
<circle cx="34" cy="338" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="336" font-size="14.5" font-weight="700" fill="#004d47">El mod, al acabar el turno</text><text x="56" y="354" font-size="12.5" fill="#555">cuenta el nuevo estado al CCC: la petición, sin probar</text>
<circle cx="34" cy="416" r="7" fill="#00726b"/><text x="56" y="414" font-size="14.5" font-weight="700" fill="#004d47">Tu móvil</text><text x="56" y="432" font-size="12.5" fill="#555">la tarjeta cambia: una petición más por probar</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">La petición es real: hoy fue la número 8, sf 0.13.2. El recorrido por el CCC es ilustrativo.</figcaption>
</figure>

La regla de un proyecto por sesión vive en el mod, no en el CCC. Hoy mismo se vio su fuerza: el mod bloqueó una escritura, aunque por un error suyo. Con el CCC, esa guardia sigue en el mismo sitio, y ninguna orden la rodea.

Si el CCC se cae, cada sesión sigue como si nada. Pierdes el mando a distancia, no la orquesta.

## De la tarea del kanban a la sesión

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 4 · la memoria que no empieza</p>
<p>Turboconvo abre el 1 de diciembre. Decidiste terminar primero el documento fundacional de SmartColdBox y empezar después la memoria. Esa memoria tendría que ser una tarea en JKanban, y ese tablero ya trae un servidor MCP. <strong>¿Cómo pasa una tarea del tablero a la sesión que la hará?</strong></p>
</div>

En el CCC, cada tarjeta de sesión enseña también las tareas de su proyecto en JKanban. Eliges una y la lanzas: el CCC abre o despierta la sesión del proyecto y le entrega la tarea con su contexto.

<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · las 18:00, con la tableta</p>
<p class="escena-contexto">La tarea «Memoria de Turboconvo: índice del anexo 5» está en la columna de pendientes de SmartColdBox.</p>
<div class="turno"><p class="ponente">Tú<small>en el CCC</small></p><p>Lanza esta tarea en SmartColdBox, después del fundacional.</p></div>
<div class="turno sistema"><p class="ponente">CCC<small>registro</small></p><p>Sesión de SmartColdBox abierta. Tarea entregada y anotada en su cola, en espera.</p></div>
<div class="turno"><p class="ponente">Claude<small>sesión de SmartColdBox</small></p><p>La tengo en cola. El anexo 5 pide 40 páginas en Noto Sans 11; empiezo por el índice cuando cierres el fundacional.</p></div>
<div class="turno sistema"><p class="ponente">CCC<small>registro</small></p><p>Tarea en curso en JKanban. Te aviso cuando quede por revisar.</p></div>
<p class="escena-pie">Diálogo imaginado: no es una transcripción ni un resultado validado.</p>
</div>

La escena enseña el ciclo completo. La tarea sale del tablero y entra en la cola de peticiones de su sesión. Cuando Claude la termina, vuelve al tablero en su nueva columna. La cola de cada sesión y el kanban son la misma lista, vista desde dos lados.

Así, JKanban deja de ser un sitio que consultas aparte. Es el atril de cada proyecto, y el CCC pasa las páginas.

## Abrir, cerrar y conducir sesiones

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 5 · el piloto que espera</p>
<p>LecturaFàcil, el piloto de la SF, espera una decisión desde hace días: diseñar su pantalla de revisión. Hoy no tiene sesión abierta, ni carpeta <code>.sf/</code>, ni repositorio git. <strong>¿Puedes ponerla en marcha sin sentarte a abrir una terminal?</strong></p>
</div>

Desde el CCC abres una sesión nueva en cualquier proyecto y le das el primer prompt. Por ejemplo: «retoma LecturaFàcil: prepara su incorporación a la SF». La sesión arranca en su carpeta, el mod le pone color y nombre, y su tarjeta aparece en la ventana.

También cierras las sesiones que ya no tocan. Al cerrar, el mod cuenta como dejado a medias lo que seguía en curso. Ese «−» del marcador no es un castigo: es lo que tendrás que retomar mañana.

Conducir no es delegar a ciegas. El CCC manda prompts y lanza tareas, pero cada sesión sigue en su modo de permisos, y las decisiones importantes siguen llegando a ti. La diferencia es que te llegan donde estés.

## Qué mide y para qué

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 6 · la noche, en números</p>
<p>Entre las 00:08 y las 02:11 hiciste commits en tres proyectos a la vez. Por la mañana seguiste solo con la SF, a un ritmo de hasta 18 commits por hora. Nadie te dijo nada a las dos de la madrugada. <strong>¿Qué te habría dicho un director que lo mirara todo?</strong></p>
</div>

El CCC mide tu día con lo que ya cuentan los mods y con lo que dice Claude Code de cada sesión. No mide a Claude: te mide a ti dirigiendo, que es lo que nadie mide hoy.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 420" width="100%" role="img" aria-label="Commits por hora del 27 de octubre en SoftwareFactory, SmartColdBox y JKanban" style="font-family:var(--fuente-texto);display:block">
<text x="14" y="22" font-size="12.5" fill="#6c3483">■ SoftwareFactory</text>
<text x="160" y="22" font-size="12.5" fill="#0e7490">■ SmartColdBox</text>
<text x="292" y="22" font-size="12.5" fill="#334155">■ JKanban</text>
<text x="54" y="58" text-anchor="end" font-size="12.5" fill="#1a1a1a">00 h</text>
<rect x="62" y="46" width="96" height="16" fill="#8e44ad"/><rect x="158" y="46" width="120" height="16" fill="#0e7490"/><rect x="278" y="46" width="60" height="16" fill="#475569"/>
<text x="346" y="58" font-size="12.5" fill="#991b1b">23 · tres frentes</text>
<text x="54" y="98" text-anchor="end" font-size="12.5" fill="#1a1a1a">01 h</text>
<rect x="62" y="86" width="36" height="16" fill="#8e44ad"/><rect x="98" y="86" width="108" height="16" fill="#0e7490"/><rect x="206" y="86" width="48" height="16" fill="#475569"/>
<text x="262" y="98" font-size="12.5" fill="#991b1b">16 · tres frentes</text>
<text x="54" y="138" text-anchor="end" font-size="12.5" fill="#1a1a1a">02 h</text>
<rect x="62" y="126" width="24" height="16" fill="#0e7490"/><rect x="86" y="126" width="24" height="16" fill="#475569"/>
<text x="118" y="138" font-size="12.5" fill="#555">4 · dos frentes</text>
<text x="54" y="178" text-anchor="end" font-size="12.5" fill="#999">03–08 h</text>
<text x="62" y="178" font-size="12.5" fill="#999">sin commits</text>
<text x="54" y="218" text-anchor="end" font-size="12.5" fill="#1a1a1a">09 h</text>
<rect x="62" y="206" width="72" height="16" fill="#8e44ad"/>
<text x="142" y="218" font-size="12.5" fill="#555">6</text>
<text x="54" y="258" text-anchor="end" font-size="12.5" fill="#1a1a1a">10 h</text>
<rect x="62" y="246" width="156" height="16" fill="#8e44ad"/><rect x="218" y="246" width="12" height="16" fill="#475569"/>
<text x="238" y="258" font-size="12.5" fill="#555">14</text>
<text x="54" y="298" text-anchor="end" font-size="12.5" fill="#1a1a1a">11 h</text>
<rect x="62" y="286" width="216" height="16" fill="#8e44ad"/>
<text x="286" y="298" font-size="12.5" fill="#555">18</text>
<text x="54" y="338" text-anchor="end" font-size="12.5" fill="#1a1a1a">14 h</text>
<rect x="62" y="326" width="120" height="16" fill="#8e44ad"/><rect x="182" y="326" width="12" height="16" fill="#0e7490"/>
<text x="202" y="338" font-size="12.5" fill="#555">11</text>
<text x="54" y="378" text-anchor="end" font-size="12.5" fill="#1a1a1a">15 h</text>
<rect x="62" y="366" width="24" height="16" fill="#8e44ad"/>
<text x="94" y="378" font-size="12.5" fill="#555">2, hasta las 15:03</text>
<text x="14" y="410" font-size="12" fill="#555">Largo de cada tramo: los commits de ese proyecto. Fuente: el historial git.</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Datos reales. Las dos horas en rojo son las que un director habría señalado.</figcaption>
</figure>

Las medidas salen de lo que ya existe. Los commits de cada proyecto y los prompts de cada sesión. El marcador de peticiones terminadas y dejadas a medias. El coste y el contexto que Claude Code da de cada sesión. El CCC las junta en una sola vista por día y por proyecto.

Medir sirve para avisar, no para juzgar. Fijas un tope de frentes a la vez, y el CCC te avisa cuando lo pasas. A las dos de la madrugada, también te recuerda la hora. El cansancio de supervisar agentes es real y está descrito ([Gonzalez, 2026](https://constantin.glez.de/posts/2026-07-16-why-working-with-ai-agents-is-so-tiring-and-what-to-do-about-it/)). La vieja ironía de la automatización sigue en pie: cuanto más automático es el sistema, más exigente es supervisarlo ([Bainbridge, 1983](https://gwern.net/doc/sociology/technology/1983-bainbridge.pdf)).

## Cómo está hecho

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 7 · la ventana que flota del todo</p>
<p>Primero pensaste en una ventana de escritorio en Python. Una hora después la quisiste también en la tableta y el móvil: «así será una ventana flotante del todo». <strong>¿Qué tiene que cumplir el CCC, la tecnología que se elija?</strong></p>
</div>

El CCC viene dentro del plugin `sf`, como las skills y el mod: se instala y se actualiza con la SF. Se usa desde el ordenador, la tableta y el móvil. La tecnología está por decidir; lo que no cambia es cómo se reparte el trabajo.

- **El mod es el enlace.** Cuenta al CCC el estado de su sesión al arrancar, al acabar cada turno y al cerrarse, y recoge las órdenes de su sesión.
- **El CCC no escribe en los proyectos.** Guarda órdenes, abre sesiones y mide; los cambios los hace Claude en cada sesión.
- **Las sesiones no dependen del CCC.** Si se cae, todo sigue igual y la ventana avisa de que está desconectada.
- **Seguro por defecto.** Escucha en tu equipo, con una clave en un archivo tuyo; abrirlo a la tableta o al móvil se hace a propósito, nunca por accidente.

#### Lo que ya permite el mod

Según los tipos de la API de los mods, un mod puede llamar por HTTP a una dirección local. También puede lanzar un proceso y leer su salida, escribir archivos y usar temporizadores. Y conoce el uso y el coste de su sesión. No tiene un cliente de websockets propio: si hace falta empuje inmediato, el mod mantiene un pequeño proceso puente. Nada de esto se ha probado aún en la práctica.

#### Opciones para la ventana

Una aplicación web que sirve el propio CCC y que se abre en cualquier navegador. Una aplicación web instalable, que en el móvil se abre como una aplicación más. O apoyarse en las superficies que ya tiene Claude Code (escritorio, móvil y control remoto). La elección depende de cómo se llegue con seguridad desde fuera de casa.

#### Lo que Claude Code ya ofrece y el CCC puede usar

Los mensajes entre sesiones listan las sesiones de la máquina y les escriben: pueden ser el canal de las órdenes. El control remoto lleva una sesión al móvil con avisos. La vista de agentes lanza y para sesiones en segundo plano. La telemetría oficial da coste, tokens y tiempo. Construir encima de esto, y no en paralelo, es lo que mantiene al CCC al día cuando Claude Code cambia.

#### Orden de construcción

Primero ver todas las sesiones, con las métricas que ya cuentan los mods. Después, las órdenes a una sesión. Después, abrir y cerrar sesiones y lanzar tareas de JKanban, que necesita su servidor MCP. Cada paso se usa a diario antes de empezar el siguiente.

## En qué se diferencia de lo que ya existe

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 8 · ¿no existe ya?</p>
<p>Antes de construir nada, te preguntas si alguien lo ha hecho ya. Claude Code tiene su vista de agentes, su control remoto desde el móvil y mensajes entre sesiones. Hay gestores de sesiones con miles de usuarios. <strong>¿Qué queda por hacer que no esté hecho?</strong></p>
</div>

Mucho de lo que necesita el CCC ya existe, y en algunos puntos va por delante. Lo que falta es la capa de tu método: sesiones vistas por fase y peticiones, tu kanban como origen de las tareas y la medida de cómo diriges.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 46 560 384" width="100%" role="img" aria-label="Familias de herramientas para varias sesiones de Claude Code, y dónde queda el CCC" style="font-family:var(--fuente-texto);display:block">
<line x1="34" y1="66" x2="34" y2="386" stroke="#b2deda" stroke-width="2"/>
<circle cx="34" cy="66" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="64" font-size="14.5" font-weight="700" fill="#004d47">Lo de Anthropic</text><text x="56" y="82" font-size="12.5" fill="#555">vista de agentes, control remoto, móvil y mensajes entre sesiones</text><text x="56" y="100" font-size="12.5" fill="#991b1b">sin fases, sin tu kanban, sin medir cómo diriges</text>
<circle cx="34" cy="146" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="144" font-size="14.5" font-weight="700" fill="#004d47">Gestores de sesiones en paralelo</text><text x="56" y="162" font-size="12.5" fill="#555">aíslan cada agente en su copia del repositorio y revisan sus cambios</text><text x="56" y="180" font-size="12.5" fill="#991b1b">casi todos de escritorio; ninguno conoce un método</text>
<circle cx="34" cy="226" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="224" font-size="14.5" font-weight="700" fill="#004d47">Tableros kanban de agentes</text><text x="56" y="242" font-size="12.5" fill="#555">cada tarjeta lanza un agente</text><text x="56" y="260" font-size="12.5" fill="#991b1b">el tablero es el suyo, no el de tus proyectos</text>
<circle cx="34" cy="306" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/><text x="56" y="304" font-size="14.5" font-weight="700" fill="#004d47">Métricas de uso</text><text x="56" y="322" font-size="12.5" fill="#555">tokens, coste, commits y tiempo activo</text><text x="56" y="340" font-size="12.5" fill="#991b1b">miden el consumo, no los frentes ni lo que dejas a medias</text>
<circle cx="34" cy="386" r="7" fill="#00726b"/><text x="56" y="384" font-size="14.5" font-weight="700" fill="#004d47">Claude Code Commander</text><text x="56" y="402" font-size="12.5" fill="#555">se apoya en todo lo anterior y añade tu método,</text><text x="56" y="420" font-size="12.5" fill="#555">JKanban y la medida de cómo diriges, también en el móvil</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">En rojo, lo que le falta a cada familia para la noche del 27 de octubre.</figcaption>
</figure>

**Lo de Anthropic** es oficial y avanza deprisa. La [vista de agentes](https://code.claude.com/docs/en/agent-view.md) muestra las sesiones en segundo plano con su estado, aunque no las interactivas ni el coste de cada una. El [control remoto](https://code.claude.com/docs/en/remote-control.md) lleva una sesión al móvil con avisos. Los [mensajes entre sesiones](https://code.claude.com/docs/en/cross-session-messaging.md) dejan que una sesión escriba a otra. El CCC no compite con esto: lo usa.

**Los gestores de sesiones** como [Claude Squad](https://github.com/smtg-ai/claude-squad), [CCManager](https://github.com/kbwo/ccmanager), [Conductor](https://www.conductor.build) u [opcode](https://github.com/winfunc/opcode) tienen comunidad y meses de uso. [Happy](https://github.com/slopus/happy) y [Nimbalyst](https://github.com/Nimbalyst/nimbalyst) ya llegan al móvil. Ninguno sabe en qué fase está un proyecto ni respeta un proyecto por sesión.

**Los tableros de agentes** como [Vibe Kanban](https://github.com/BloopAI/vibe-kanban) lanzan un agente por tarjeta, pero con su propio tablero. Su empresa cerró la nube en abril de 2026 y el proyecto sigue en manos de la comunidad ([anuncio](https://vibekanban.com/blog/shutdown)).

**Las métricas** de la [telemetría oficial](https://code.claude.com/docs/en/monitoring-usage.md) y de [ccusage](https://github.com/ryoppippi/ccusage) cuentan tokens, coste y commits. El CCC las consumirá; lo que añade es medir la dirección.

Esa medida importa. Un estudio de BCG con casi 1.500 trabajadores lo midió. La productividad sube con los tres primeros agentes y cae con el cuarto ([Built In, 10 de junio de 2026](https://builtin.com/articles/ai-brain-fry-software-developers)). La noche del 27 llevabas tres frentes. Un director lo habría visto.

#### Los productos del gráfico, uno a uno

- [Vista de agentes](https://code.claude.com/docs/en/agent-view.md): todas las sesiones en segundo plano de todos los proyectos, en la terminal.
- [Control remoto](https://code.claude.com/docs/en/remote-control.md): una sesión local en la web o en la app de Claude, con avisos.
- [Mensajes entre sesiones](https://code.claude.com/docs/en/cross-session-messaging.md): listar sesiones y escribirles en la misma máquina o a través del control remoto.
- [Claude Squad](https://github.com/smtg-ai/claude-squad): varios agentes en la terminal, cada uno aislado.
- [CCManager](https://github.com/kbwo/ccmanager): estado de cada sesión y sus copias del repositorio, sin tmux.
- [Conductor](https://www.conductor.build): agentes en paralelo para revisar y fusionar, en Mac.
- [opcode](https://github.com/winfunc/opcode): interfaz gráfica de sesiones con coste y tokens.
- [Happy](https://github.com/slopus/happy): cliente cifrado para el móvil, la web y el escritorio.
- [Nimbalyst](https://github.com/Nimbalyst/nimbalyst): escritorio con app acompañante para el móvil y seguimiento de tareas.
- [Vibe Kanban](https://github.com/BloopAI/vibe-kanban): un agente por tarjeta, en local.
- [Telemetría oficial](https://code.claude.com/docs/en/monitoring-usage.md) y [ccusage](https://github.com/ryoppippi/ccusage): consumo, coste y producción de código.

## De vuelta al caso

<div class="caso">
<p class="caso-etiqueta">El caso · epílogo · el mismo martes, con el CCC</p>
<p>A las 00:30, el CCC te habría dicho que llevabas tres frentes y que pasaba la medianoche. El «Sin SF» habría salido en rojo en la tarjeta de la SF, sin abrir su terminal. La alineación de la ventana la habrías pedido desde el sofá. La memoria de Turboconvo estaría en JKanban, en la cola de SmartColdBox, esperando al fundacional. <strong>Qué proyecto va primero, cuándo paras y qué se presenta el 1 de diciembre lo sigues decidiendo tú.</strong></p>
</div>

El CCC no toca por ti. Te da la partitura entera, te avisa de la hora y te deja dar la entrada a cada sesión desde donde estés. La música, y las decisiones, siguen siendo tuyas.

## Anexo: el caso y sus fuentes

### Qué es real

El día es el martes 27 de octubre de 2026. Los commits y sus horas salen del historial git de SoftwareFactory, SmartColdBox y JKanban, contados a las 15:03: 60, 22 y 12. Hubo commits en los tres proyectos entre las 00:08 y las 02:11. La versión 1.0.0 de JKanban se preparó a las 10:27, y JKanban trae la carpeta `jkanban_mcp`.

El «Sin SF» al arrancar, el bloqueo «esta sesión es de .» y la petición de alinear la ventana a la derecha ocurrieron en la sesión de la SF. Las tres mejoras registradas desde SmartColdBox están en `docs/propuestas.md`. Las cifras «sin probar 7» y «propuestas por revisar 17» son las que mostraba la caja del mod esa tarde.

El estado de SmartColdBox («cerrando la visión; lo siguiente es la especificación funcional») sale de su `.sf/estado.json`. Turboconvo, la convocatoria de innovación de las Illes Balears, recibe solicitudes del 1 de diciembre de 2026 al 5 de enero de 2027 ([convocatoria](https://www.caib.es/sites/innovacio/es/n/subvencions_per_a_la_innovacia/)). Su memoria sigue el anexo 5: 40 páginas en Noto Sans 11. Que la memoria espera al fundacional es decisión tuya. LecturaFàcil no tiene `.sf/` ni repositorio git.

Las frases sobre la ventana flotante, el alcance del CCC y las métricas para los «hombres orquesta» son tuyas, y están en la decisión «Claude Code Commander» de `docs/decisiones/`.

### Qué es ilustrativo

El CCC no existe todavía: todo lo que hace en la historia es lo que hará. Las escenas son imaginadas, también la tarea «Memoria de Turboconvo: índice del anexo 5» y las horas del café y de la tableta. La forma de la ventana del boceto es un ejemplo; sus datos son los reales de ese momento. El tope de frentes es un ejemplo.

### Fuentes

Consultadas el 27 de octubre de 2026.

- Parnin y Rugaber, [Resumption strategies for interrupted programming tasks](https://sites.cc.gatech.edu/reverse/repository/resumptionstrategies.pdf), 2010.
- Constantin Gonzalez, [Why working with AI agents is so tiring](https://constantin.glez.de/posts/2026-07-16-why-working-with-ai-agents-is-so-tiring-and-what-to-do-about-it/), 16 de julio de 2026.
- Bainbridge, [Ironies of Automation](https://gwern.net/doc/sociology/technology/1983-bainbridge.pdf), 1983.
- Visión de SoftwareFactory [«el hombre orquesta»](hombre-orquesta.html), con su verificación de citas.
- Govern de les Illes Balears, [subvenciones para la innovación](https://www.caib.es/sites/innovacio/es/n/subvencions_per_a_la_innovacia/).
- Built In, [AI brain fry](https://builtin.com/articles/ai-brain-fry-software-developers), 10 de junio de 2026, sobre el estudio de BCG. La fecha del estudio no es clara: el artículo dice abril y la página de BCG, 5 de marzo.
- Documentación de Claude Code: [vista de agentes](https://code.claude.com/docs/en/agent-view.md), [control remoto](https://code.claude.com/docs/en/remote-control.md), [mensajes entre sesiones](https://code.claude.com/docs/en/cross-session-messaging.md), [telemetría](https://code.claude.com/docs/en/monitoring-usage.md).
- Productos de la comparación: los enlaces de «Los productos del gráfico, uno a uno». Comparación fechada el 27 de octubre de 2026; Terragon y Crystal, discontinuados, no se incluyen.

---

*Documento de visión de SoftwareFactory: Claude Code Commander — 2026-10-27.*
