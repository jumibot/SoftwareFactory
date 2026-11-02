# Cómo funciona el panel

El panel de la SF, parte por parte: qué enseña, cómo se lee y qué se puede hacer desde él. El resumen está en [Cómo funciona la Software Factory](como-funciona-la-software-factory.html#el-panel-de-la-sf). Las reglas del método que hay detrás están en la metodología (sección 2) y en las [decisiones](decisiones/README.md).

**Estado:** 29 de octubre de 2026, plugin `sf` 0.34.3 y lo que hay en `develop` sin publicar (ver «Historial»).

## Qué es

El panel es el **mod de estado** del plugin `sf`. Un mod es la parte de un plugin que cambia la interfaz o el comportamiento de Claude Code: responde a eventos de la sesión y dibuja en un panel o sobre el prompt. Este mod es el centro de control de la SF dentro de Claude Code, y las nuevas responsabilidades de control se plantean primero en él.

Se ve de dos formas. En la pantalla completa de Claude Code, el panel se abre solo al empezar la sesión, a la derecha de la conversación. Si lo cierras a mano, no se vuelve a abrir solo: `/sf` lo reabre. Cuando el panel no está a la vista, el mod se enseña en una caja pequeña sobre el prompt (ver «La caja sobre el prompt»).

Es el mismo en todos los proyectos, la SF incluida, sin adaptaciones. En un proyecto sin SF, bajo la cabecera dice «sin SF» y enseña una sección más, «Incorporarlo a la SF». Dice qué pedir a Claude y trae un ejemplo de `.sf/proyecto.json` y otro de `.sf/estado.json`.

Se lee de arriba abajo: la cabecera dice dónde estás; la parte amarilla, qué se está haciendo; los bloques, todo lo demás.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 287.3" width="100%" role="img" aria-label="Captura del panel de la SF con sus partes marcadas: cabecera, tareas en curso con sus pasos, y los bloques Tareas, Proyecto y SF ENHANCE" style="font-family:var(--fuente-texto);display:block">
<image href="capturas/panel/panel.png" x="0" y="6" width="320" height="275.3"/>
<rect x="2" y="7.2" width="316" height="24.6" rx="4" fill="none" stroke="#a6501a" stroke-width="2"/>
<line x1="320" y1="19.5" x2="336" y2="19.5" stroke="#a6501a" stroke-width="2"/>
<text x="344" y="19.5" font-size="17" font-weight="700" fill="#004d47">Cabecera</text>
<text x="344" y="38.5" font-size="15" fill="#555">prompts, nombre y rama</text>
<rect x="2" y="52.7" width="316" height="58.8" rx="4" fill="none" stroke="#a6501a" stroke-width="2"/>
<line x1="320" y1="82.1" x2="336" y2="82.1" stroke="#a6501a" stroke-width="2"/>
<text x="344" y="82.1" font-size="17" font-weight="700" fill="#004d47">En curso</text>
<text x="344" y="101.1" font-size="15" fill="#555">la tarea en amarillo y sus pasos</text>
<rect x="2" y="121.1" width="316" height="68.4" rx="4" fill="none" stroke="#a6501a" stroke-width="2"/>
<line x1="320" y1="155.3" x2="336" y2="155.3" stroke="#a6501a" stroke-width="2"/>
<text x="344" y="155.3" font-size="17" font-weight="700" fill="#004d47">Tareas</text>
<text x="344" y="174.3" font-size="15" fill="#555">Pendientes, Testing y Cerradas</text>
<rect x="2" y="200" width="316" height="23.3" rx="4" fill="none" stroke="#a6501a" stroke-width="2"/>
<line x1="320" y1="211.7" x2="336" y2="211.7" stroke="#a6501a" stroke-width="2"/>
<text x="344" y="211.7" font-size="17" font-weight="700" fill="#004d47">Proyecto</text>
<text x="344" y="230.7" font-size="15" fill="#555">Documentos</text>
<rect x="2" y="233.8" width="316" height="46.7" rx="4" fill="none" stroke="#a6501a" stroke-width="2"/>
<line x1="320" y1="257.2" x2="336" y2="257.2" stroke="#a6501a" stroke-width="2"/>
<text x="344" y="257.2" font-size="17" font-weight="700" fill="#004d47">SF ENHANCE</text>
<text x="344" y="276.2" font-size="15" fill="#555">Registro y Mejoras</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">El panel en la SF, con dos tareas en curso y los bloques plegados. La cabecera de la captura es la de antes de TURBO.</figcaption>
</figure>

## La cabecera

La cabecera son dos filas que quedan fijas al hacer scroll. Lo demás sube con la rueda o las teclas, también la tarea en curso.

<figure class="vertical" style="margin:1.6rem 0 1.4rem;">
<svg viewBox="0 0 560 520" width="100%" role="img" aria-label="Las dos filas de la cabecera del panel, dibujadas, con sus partes numeradas: ACTUALIZAR, RELEASE, TURBO, prueba y nombre; duración, prompts y rama" style="font-family:var(--fuente-texto);display:block">
<rect x="26" y="28" width="96" height="22" rx="3" fill="none" stroke="#b91c1c" stroke-width="1.2"/>
<text x="74" y="43" text-anchor="middle" font-size="12" font-weight="700" fill="#b91c1c">ACTUALIZAR</text>
<rect x="126" y="28" width="74" height="22" rx="3" fill="none" stroke="#7e22ce" stroke-width="1.2"/>
<text x="163" y="43" text-anchor="middle" font-size="12" font-weight="700" fill="#7e22ce">RELEASE</text>
<rect x="204" y="28" width="62" height="22" rx="3" fill="none" stroke="#999" stroke-width="1.2"/>
<text x="235" y="43" text-anchor="middle" font-size="12" font-weight="700" fill="#0e7490">TURBO</text>
<rect x="270" y="28" width="64" height="22" rx="3" fill="none" stroke="#a6501a" stroke-width="1.2"/>
<text x="302" y="43" text-anchor="middle" font-size="12" fill="#a6501a">PRUEBA</text>
<rect x="404" y="28" width="130" height="22" rx="3" fill="none" stroke="#6d28d9" stroke-width="1.2"/>
<text x="469" y="43" text-anchor="middle" font-size="12" fill="#6d28d9">SF 1.0.0</text>
<rect x="26" y="56" width="64" height="22" rx="3" fill="none" stroke="#999" stroke-width="1.2"/>
<text x="58" y="71" text-anchor="middle" font-size="12" fill="#555">2h 05m</text>
<rect x="94" y="56" width="88" height="22" rx="3" fill="none" stroke="#999" stroke-width="1.2"/>
<text x="138" y="71" text-anchor="middle" font-size="12" fill="#555">12 prompts</text>
<rect x="354" y="56" width="180" height="22" rx="3" fill="none" stroke="#999" stroke-width="1.2"/>
<text x="444" y="71" text-anchor="middle" font-size="12" fill="#555">feature/155-doc-panel</text>
<line x1="74" y1="22" x2="74" y2="28" stroke="#f97316" stroke-width="1.5"/>
<circle cx="74" cy="12" r="10" fill="#f97316"/>
<text x="74" y="17" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
<line x1="163" y1="22" x2="163" y2="28" stroke="#f97316" stroke-width="1.5"/>
<circle cx="163" cy="12" r="10" fill="#f97316"/>
<text x="163" y="17" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">2</text>
<line x1="235" y1="22" x2="235" y2="28" stroke="#f97316" stroke-width="1.5"/>
<circle cx="235" cy="12" r="10" fill="#f97316"/>
<text x="235" y="17" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">3</text>
<line x1="302" y1="22" x2="302" y2="28" stroke="#f97316" stroke-width="1.5"/>
<circle cx="302" cy="12" r="10" fill="#f97316"/>
<text x="302" y="17" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">4</text>
<line x1="469" y1="22" x2="469" y2="28" stroke="#f97316" stroke-width="1.5"/>
<circle cx="469" cy="12" r="10" fill="#f97316"/>
<text x="469" y="17" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">5</text>
<line x1="58" y1="78" x2="58" y2="84" stroke="#f97316" stroke-width="1.5"/>
<circle cx="58" cy="94" r="10" fill="#f97316"/>
<text x="58" y="99" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">6</text>
<line x1="138" y1="78" x2="138" y2="84" stroke="#f97316" stroke-width="1.5"/>
<circle cx="138" cy="94" r="10" fill="#f97316"/>
<text x="138" y="99" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">7</text>
<line x1="444" y1="78" x2="444" y2="84" stroke="#f97316" stroke-width="1.5"/>
<circle cx="444" cy="94" r="10" fill="#f97316"/>
<text x="444" y="99" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">8</text>
<circle cx="14" cy="136" r="11" fill="#f97316"/>
<text x="14" y="141" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>
<text x="34" y="141" font-size="16" font-weight="700" fill="#004d47">ACTUALIZAR, en rojo</text>
<text x="34" y="161" font-size="15" fill="#555">solo con una versión publicada más nueva</text>
<circle cx="14" cy="184" r="11" fill="#f97316"/>
<text x="14" y="189" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">2</text>
<text x="34" y="189" font-size="16" font-weight="700" fill="#004d47">RELEASE, en violeta</text>
<text x="34" y="209" font-size="15" fill="#555">publica develop en main con su tag</text>
<circle cx="14" cy="232" r="11" fill="#f97316"/>
<text x="14" y="237" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">3</text>
<text x="34" y="237" font-size="16" font-weight="700" fill="#004d47">TURBO</text>
<text x="34" y="257" font-size="15" fill="#555">pide a Claude lanzar lo que no te necesita</text>
<circle cx="14" cy="280" r="11" fill="#f97316"/>
<text x="14" y="285" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">4</text>
<text x="34" y="285" font-size="16" font-weight="700" fill="#004d47">Etiqueta de prueba, solo en la SF</text>
<text x="34" y="305" font-size="15" fill="#555">«PRUEBA» en naranja: la copia de trabajo</text>
<circle cx="14" cy="328" r="11" fill="#f97316"/>
<text x="14" y="333" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">5</text>
<text x="34" y="333" font-size="16" font-weight="700" fill="#004d47">SF y la versión del plugin</text>
<text x="34" y="353" font-size="15" fill="#555">con el color de la sesión</text>
<circle cx="14" cy="376" r="11" fill="#f97316"/>
<text x="14" y="381" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">6</text>
<text x="34" y="381" font-size="16" font-weight="700" fill="#004d47">Duración de la sesión</text>
<text x="34" y="401" font-size="15" fill="#555">en horas y minutos, desde que se abrió</text>
<circle cx="14" cy="424" r="11" fill="#f97316"/>
<text x="14" y="429" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">7</text>
<text x="34" y="429" font-size="16" font-weight="700" fill="#004d47">Prompts de la sesión</text>
<text x="34" y="449" font-size="15" fill="#555">los que envías tú; con 0, atenuados</text>
<circle cx="14" cy="472" r="11" fill="#f97316"/>
<text x="14" y="477" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">8</text>
<text x="34" y="477" font-size="16" font-weight="700" fill="#004d47">Rama activa</text>
<text x="34" y="497" font-size="15" fill="#555">a la derecha; en amarillo si es la de una tarea</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Las dos filas fijas de la cabecera en la SF, con una versión nueva por instalar, en modo prueba y en la rama de una tarea. Es un esquema, no una captura.</figcaption>
</figure>

La primera fila tiene los botones de la sesión a la izquierda y el proyecto a la derecha. Los botones son ACTUALIZAR, RELEASE, TURBO y, solo en la SF, la etiqueta de prueba. Todos van en etiquetas, con la letra en negrita.

**ACTUALIZAR**, en rojo, solo sale cuando hay una versión publicada del plugin más nueva que la instalada. Al pulsarlo, actualiza el plugin (ver «ACTUALIZAR»). Va en rojo para no confundirlo con RELEASE.

**RELEASE**, en violeta, publica: pasa `develop` a `main` con su tag (ver «RELEASE»). Sale en la SF y en todos los proyectos con SF.

La etiqueta **TURBO**, con la letra cian, pide a Claude que lance con subagentes las tareas que no te necesitan (ver «TURBO»).

En la SF, tras TURBO, puede ir la etiqueta de prueba. Sale si el catálogo local está registrado. «PRUEBA», en naranja, dice que se usa la copia de trabajo; «prueba», subrayada, atenuada y sin fondo, que se usa el plugin publicado. Un clic cambia de uno a otro (ver «Modo prueba»).

A la derecha va **«SF» y la versión del plugin cargado**, por ejemplo «SF 1.0.0», con el color de la sesión de fondo y letra negra, como la etiqueta que pone Claude Code. Si no puede leer la versión, dice «SF» a secas. Sale igual en todos los proyectos, también en uno sin SF, porque el panel es del plugin. El color es el campo `color` de `.sf/proyecto.json`, uno de los ocho de `/color`: red, blue, green, yellow, purple, orange, pink o cyan. Sin color, la etiqueta va atenuada. La SF usa purple. El nombre del proyecto ya no sale en el panel: lo lleva la sesión, con `/rename`.

### La duración, los prompts y la rama activa

La segunda fila lleva la duración de la sesión y los prompts a la izquierda, y la rama activa a la derecha.

La duración va en horas y minutos: «2h 05m», o «45m» si no llega a una hora. Cuenta desde que se abrió la sesión, `/reload-plugins` no la reinicia y se redibuja cada minuto.

Los **prompts** son los mensajes que has enviado en la sesión. No cuentan los que añade Claude Code sin que se vean. La cifra va en color; con 0, atenuada. La cuenta dura toda la sesión, también tras `/reload-plugins`, y vuelve a 0 en la siguiente.

La **rama activa** es la de la carpeta del proyecto, por ejemplo `develop`. Va alineada a la derecha, en una etiqueta con el estilo de la de los prompts y la letra atenuada.

Si es la rama de una tarea en curso o en Testing, su campo `rama` en `.sf/peticiones.json`, la letra va en el amarillo de la tarea. Así se ve que estás en la rama de esa tarea, por ejemplo al probarla.

Con la cabeza separada, sin rama, sale el commit corto entre paréntesis: «(0123456)». Si el nombre no cabe en lo que deja la duración, se recorta por el final con «…».

El mod no ejecuta git para leerla: lee `.git/HEAD`. En un worktree, `.git` es un archivo que apunta a su carpeta, y lee el `HEAD` de allí. Sin `.git`, no sale nada. Solo sale en proyectos con SF, la propia SF incluida.

Se relee con la cola (ver «Cuándo se actualiza»). Si cambias de rama en otra terminal, el panel lo muestra tras la siguiente herramienta, al acabar el turno o con `/sf`.

### Bajo la cabecera

Bajo las dos filas fijas, y ya subiendo con el scroll, van por este orden la línea del proyecto, la línea del modo prueba, las tareas en curso y los avisos.

La **línea del proyecto** sale en los proyectos que no son la SF. Es atenuada y dice la versión de la SF, la fase y la devslice: «SF 0.34 · 3/7 Definición técnica · devslice 2». La versión es el campo `sf` de `.sf/proyecto.json`, la de la SF con la que se incorporó el proyecto. Sin versión, dice «SF (sin versión)»; sin fase declarada, «fase sin declarar». En un proyecto sin SF, la línea solo dice «sin SF».

Si esa versión va por detrás del plugin que se ejecuta, la línea sale como «SF 0.13 → 0.34.3». Se comparan solo los dos primeros números: un arreglo, el tercero, no obliga a poner el proyecto al día.

La línea del modo prueba sale en la SF cuando lo pedido y lo cargado no coinciden. Es naranja y dice «/reload-plugins para entrar en el modo prueba» o «para salir del modo prueba».

Los avisos van en amarillo, con «⚠», bajo las tareas en curso. Hay tres:

- **No se puede leer** `.sf/proyecto.json` o `.sf/estado.json`, o la fase no es ninguna de las siete. El aviso dice cuáles son las válidas.
- **Ubicación antigua**: el proyecto aún tiene `docs/sf.json` y no `.sf/`. Pide pasar la identidad a `.sf/proyecto.json` y el estado a `.sf/estado.json`.
- **Versión atrasada**: dice con qué SF se incorporó el proyecto, por cuál va y que hay que pedir a Claude «pon el proyecto al día con la SF».

El aviso de una cola ilegible va aparte, al principio del bloque TAREAS (ver «Pendientes»).

## La tarea en curso y sus pasos

Lo amarillo es lo que se está haciendo. La línea en amarillo solo va aquí. En el resto del panel, las mismas tareas llevan su código en amarillo y el texto en gris; fuera de ellas, solo la rama de la cabecera puede ir en amarillo.

<figure class="vertical" style="margin:1.6rem 0 1.4rem;">
<svg viewBox="0 0 560 523.5" width="100%" role="img" aria-label="Tareas en curso con la primera desplegada y sus partes numeradas" style="font-family:var(--fuente-texto);display:block">
<image href="capturas/panel/en-curso.png" x="26" y="0" width="508" height="218.5"/>
<rect x="29.8" y="2.6" width="296.5" height="19.2" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="12.1" x2="29.8" y2="12.1" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="12.1" r="10" fill="#f97316"/>
<text x="11" y="17.1" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
<rect x="49" y="21.7" width="485" height="53.7" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="48.6" x2="49" y2="48.6" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="48.6" r="10" fill="#f97316"/>
<text x="11" y="53.6" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">2</text>
<rect x="49" y="75.4" width="82.4" height="17.9" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="84.3" x2="49" y2="84.3" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="84.3" r="10" fill="#f97316"/>
<text x="11" y="89.3" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">3</text>
<rect x="45.2" y="93.3" width="153.4" height="70.3" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="128.4" x2="45.2" y2="128.4" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="128.4" r="10" fill="#f97316"/>
<text x="11" y="133.4" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">4</text>
<rect x="204.9" y="127.8" width="38.3" height="35.8" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="243.3" y1="145.7" x2="539" y2="145.7" stroke="#f97316" stroke-width="1.5"/>
<circle cx="549" cy="145.7" r="10" fill="#f97316"/>
<text x="549" y="150.7" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">5</text>
<rect x="29.8" y="163.6" width="504.2" height="55" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="191.1" x2="29.8" y2="191.1" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="191.1" r="10" fill="#f97316"/>
<text x="11" y="196.1" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">6</text>
<circle cx="14" cy="248.5" r="11" fill="#f97316"/>
<text x="14" y="253.5" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>
<text x="34" y="253.5" font-size="16" font-weight="700" fill="#004d47">Tarea en curso, desplegada</text>
<text x="34" y="273.5" font-size="15" fill="#555">en amarillo; el número subrayado la pliega</text>
<circle cx="14" cy="296.5" r="11" fill="#f97316"/>
<text x="14" y="301.5" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">2</text>
<text x="34" y="301.5" font-size="16" font-weight="700" fill="#004d47">Descripción y rama</text>
<text x="34" y="321.5" font-size="15" fill="#555">la rama, atenuada: «rama: feature/…»</text>
<circle cx="14" cy="344.5" r="11" fill="#f97316"/>
<text x="14" y="349.5" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">3</text>
<text x="34" y="349.5" font-size="16" font-weight="700" fill="#004d47">Cuenta de pasos</text>
<text x="34" y="369.5" font-size="15" fill="#555">hechos de todos; un clic pliega la lista</text>
<circle cx="14" cy="392.5" r="11" fill="#f97316"/>
<text x="14" y="397.5" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">4</text>
<text x="34" y="397.5" font-size="16" font-weight="700" fill="#004d47">Pasos con su marca</text>
<text x="34" y="417.5" font-size="15" fill="#555">✓ hecho, ▸ en curso, · pendiente</text>
<circle cx="14" cy="440.5" r="11" fill="#f97316"/>
<text x="14" y="445.5" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">5</text>
<text x="34" y="445.5" font-size="16" font-weight="700" fill="#004d47">«?» y E</text>
<text x="34" y="465.5" font-size="15" fill="#555">explicar el paso; quitar uno pendiente</text>
<circle cx="14" cy="488.5" r="11" fill="#f97316"/>
<text x="14" y="493.5" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">6</text>
<text x="34" y="493.5" font-size="16" font-weight="700" fill="#004d47">Otra tarea en curso, plegada</text>
<text x="34" y="513.5" font-size="15" fill="#555">con su paso actual debajo</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Dos tareas en curso: la de arriba, desplegada con su descripción, su rama y sus cuatro pasos. La captura es anterior: recorta con «…» la 102 y su paso, que ahora van enteros, y lleva «−» donde ahora va la E.</figcaption>
</figure>

### Qué tareas salen

Sale toda tarea **en curso** y la que estás probando, la del campo `probando`. Esta última se trabaja como si estuviera en curso, pero sigue en Testing y conserva su letra, T. Arriba va la que ha cambiado la última: la de fecha más reciente en su historial. Esa es la **tarea principal**, así que anotar un paso en otra en curso la sube. Las que no tienen historial van detrás, de número más alto a más bajo.

Todas van enteras, en varias líneas si hace falta. Todo va en amarillo, número incluido, y sin negrita; la letra, en un amarillo más apagado. A la derecha van sus botones (ver «Botones de las tareas»).

Si una tarea tiene descripción o rama, su número va subrayado. Un clic la despliega: debajo, la descripción y la línea «rama:». Otro clic la pliega. Los pasos se pliegan y despliegan aparte, con su cuenta.

Sin tareas en curso, la parte amarilla enseña la devslice del proyecto: «devslice 2». Sin devslice, una línea atenuada: «▷ ninguna tarea en curso».

### Cómo se leen los pasos

Bajo cada tarea en curso va la cuenta de sus pasos y el paso actual, también entero: «3/5 Aplicarlo». La cuenta es hechos de todos. El paso actual es el que está en curso o, si no hay ninguno, el primero pendiente. Con todos hechos, dice «6/6 pasos hechos».

La cuenta va subrayada: un clic despliega todos los pasos, con «2/4 pasos» encima, y otro los pliega. Cada paso lleva una marca:

- **✓** hecho, en gris oscuro: ya no pide nada.
- **▸** en curso, en gris claro: es en lo que está Claude.
- **·** pendiente, en gris claro.

Cada paso lleva al final un **«?»**. Un clic pide a Claude que explique el paso: qué es, qué se ha hecho y qué falta, sin hacerlo ni cambiar nada. El mensaje entra en el chat como si lo hubieras escrito tú.

Los pendientes llevan además, tras el «?», una **E** roja, que quita el paso de la tarea. Pide dos clics, como la E y la D de las tareas: el primero la cambia por «E eliminar» y el segundo quita el paso; a los 5 segundos vuelve a ser E. «Probar la tarea» la lleva: quitarlo es cerrar sin probar. «Cerrar la tarea» no la lleva nunca, porque toda tarea se cierra con él. Solo quita el paso si en ese sitio sigue el mismo y sin empezar, porque Claude puede haber cambiado la cola entretanto. Los pasos hechos o en curso no se pueden quitar.

Los pasos los escribe Claude en `.sf/peticiones.json`, en el campo `pasos` de la tarea, con su texto y su estado, y los actualiza en el momento. Un paso sin texto o con un estado desconocido no se enseña.

## Los bloques

Debajo van las secciones, agrupadas en **tres bloques**: TAREAS, PROYECTO y SF ENHANCE. Cada bloque tiene un fondo gris algo más claro que el del panel, pensado para el tema oscuro, y una fila con el fondo del panel separa un bloque del siguiente.

<figure class="vertical" style="margin:1.6rem 0 1.4rem;">
<svg viewBox="0 0 560 419.2" width="100%" role="img" aria-label="Los tres bloques del panel, plegados, con sus partes numeradas" style="font-family:var(--fuente-texto);display:block">
<image href="capturas/panel/bloques.png" x="26" y="0" width="508" height="258.2"/>
<rect x="28.6" y="4.5" width="245.4" height="17.9" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="13.4" x2="28.6" y2="13.4" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="13.4" r="10" fill="#f97316"/>
<text x="11" y="18.4" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
<rect x="473.3" y="4.5" width="60.1" height="17.9" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="533.4" y1="13.4" x2="539" y2="13.4" stroke="#f97316" stroke-width="1.5"/>
<circle cx="549" cy="13.4" r="10" fill="#f97316"/>
<text x="549" y="18.4" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">2</text>
<rect x="26" y="112.5" width="508" height="17.3" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="121.1" x2="26" y2="121.1" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="121.1" r="10" fill="#f97316"/>
<text x="11" y="126.1" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">3</text>
<circle cx="14" cy="288.2" r="11" fill="#f97316"/>
<text x="14" y="293.2" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>
<text x="34" y="293.2" font-size="16" font-weight="700" fill="#004d47">Sección plegada</text>
<text x="34" y="313.2" font-size="15" fill="#555">«▸», su título y su cuenta; un clic la abre</text>
<circle cx="14" cy="336.2" r="11" fill="#f97316"/>
<text x="14" y="341.2" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">2</text>
<text x="34" y="341.2" font-size="16" font-weight="700" fill="#004d47">Rótulo del bloque</text>
<text x="34" y="361.2" font-size="15" fill="#555">a la derecha, en la fila de su primera sección</text>
<circle cx="14" cy="384.2" r="11" fill="#f97316"/>
<text x="14" y="389.2" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">3</text>
<text x="34" y="389.2" font-size="16" font-weight="700" fill="#004d47">Separación</text>
<text x="34" y="409.2" font-size="15" fill="#555">una fila con el fondo del panel</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Los bloques Tareas, Proyecto y SF ENHANCE, con todas sus secciones plegadas.</figcaption>
</figure>

El rótulo del bloque va a la derecha, en la fila de su primera sección, sin gastar una propia. Cada sección tiene una cabecera con «▾» si está abierta y «▸» si está plegada, su título en negrita y su cuenta, atenuada. Un clic en la cabecera la pliega o la despliega; con el panel enfocado, también Tab y Enter.

De inicio, Testing, Documentos y Mejoras están plegadas, y las demás, abiertas. Las tareas, los pasos, las propuestas y las cerradas empiezan plegados. Lo que pliegues o despliegues se recuerda entre sesiones, sección a sección y tarea a tarea.

Pendientes y Testing no salen si no tienen ninguna tarea. Cerradas, Documentos y Registro salen siempre.

## Tareas

El bloque TAREAS sigue el ciclo de una tarea: Pendientes, Testing y Cerradas. Las tareas pasan de una sesión a otra, por eso no se llama «sesión». Antes de las secciones, cómo se lee cada tarea. Qué hace cada cambio de estado, quién lo pide y qué toca en git, en [Cómo funcionan los estados](como-funcionan-los-estados.html).

### Código y letras

Cada tarea ocupa una línea: su código, la cuenta de pasos si los tiene, «8/9», y el texto, recortado al ancho. El código es el número y una letra, que es su estado. Es la misma en todos los sitios, también arriba:

- **A**, actual: en cola o en curso, y entró en esta sesión.
- **H**, histórico: en cola o en curso, y ya estaba al abrir la sesión. Una H no pasa a A.
- **T**: en Testing.
- **C**: cerrada y probada, ya fuera de la cola.
- **D**: descartada. Sigue en la cola, en el estado `descartada`, hasta que se limpian las Cerradas.
- **R**: revertida con la R de antes, que la dejaba en Cerradas. Sale al limpiarlas. Hoy una revertida se elimina o vuelve a Pendientes.

Las letras salen del historial de cada tarea, que escribe `cola.py`. A, si se creó, o nació de un `/split`, después de abrir la sesión; H, si no. Una tarea **reabierta** lleva H, aunque vuelva en esta sesión: no es nueva. Una tarea sin historial, anterior al CLI, también lleva H. Fuera de la cola, la letra es el estado con que salió, apuntado en `.sf/historial.jsonl`: D, R o, si no, C.

La letra va pegada al número, sin guion, más apagada y nunca subrayada: «57A». Solo el número se subraya, cuando la tarea se despliega. Los números de una cifra ocupan dos, « 4T», para que los códigos queden alineados.

Cada letra tiene su color, igual en los códigos y en las cuentas de las cabeceras. La H, en rojo; la C, en verde; la A, la T, la D y la R, en el gris de las tareas. El código de una tarea en curso, en amarillo, en todas las secciones. Los textos de las tareas y de las mejoras van sin negrita, en un gris más apagado que el texto normal.

### Desplegar una tarea

Si una tarea tiene más que ver, su número va subrayado y un clic la despliega; otro clic la pliega. Hay más que ver si el texto está recortado o si tiene descripción, pasos, commit, rama o, en Testing, qué probar o lo que comprobó Claude.

Desplegada, la línea muestra el texto entero, sin repetirlo debajo. Si no cabe, sigue en la línea siguiente desde la izquierda, sin sangría, porque el panel es estrecho. Debajo, con sangría, van por este orden:

1. la descripción;
2. los pasos, con sus marcas, su «?» y su E;
3. el commit, atenuado;
4. la rama de la tarea, atenuada: «rama: feature/95-rama-en-panel», con « (no existe)» detrás si ya no está en el repositorio;
5. en Testing, «✓ Claude: …» en verde, si lo comprobó;
6. en Testing, «probar: …», atenuado.

Cada fila se despliega por separado. Una tarea en prueba sale en Pendientes y en Testing, y tú decides dónde verla.

### Pendientes

Arriba, las tareas en curso, también la que se está probando, con su código en amarillo y el texto en gris. Debajo, las que esperan en cola. En cada grupo, la que ha cambiado la última va arriba, como en «Qué tareas salen».

<figure class="vertical" style="margin:1.6rem 0 1.4rem;">
<svg viewBox="0 0 560 603.3" width="100%" role="img" aria-label="Sección Pendientes con sus partes numeradas" style="font-family:var(--fuente-texto);display:block">
<image href="capturas/panel/pendientes.png" x="26" y="0" width="508" height="346.3"/>
<rect x="28.6" y="2.6" width="245.4" height="19.2" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="12.1" x2="28.6" y2="12.1" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="12.1" r="10" fill="#f97316"/>
<text x="11" y="17.1" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
<rect x="45.2" y="21.7" width="338.7" height="35.8" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="39.6" x2="45.2" y2="39.6" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="39.6" r="10" fill="#f97316"/>
<text x="11" y="44.6" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">2</text>
<rect x="45.2" y="57.5" width="39.6" height="17.9" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="66.5" x2="45.2" y2="66.5" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="66.5" r="10" fill="#f97316"/>
<text x="11" y="71.5" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">3</text>
<rect x="45.2" y="200.6" width="488.8" height="107.4" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="254.3" x2="45.2" y2="254.3" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="254.3" r="10" fill="#f97316"/>
<text x="11" y="259.3" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">4</text>
<rect x="478.4" y="21.7" width="55.6" height="322.1" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="534" y1="182.8" x2="539" y2="182.8" stroke="#f97316" stroke-width="1.5"/>
<circle cx="549" cy="182.8" r="10" fill="#f97316"/>
<text x="549" y="187.8" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">5</text>
<circle cx="14" cy="376.3" r="11" fill="#f97316"/>
<text x="14" y="381.3" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>
<text x="34" y="381.3" font-size="16" font-weight="700" fill="#004d47">Cabecera de Pendientes</text>
<text x="34" y="401.3" font-size="15" fill="#555">total y reparto por letra; las H, en rojo</text>
<circle cx="14" cy="424.3" r="11" fill="#f97316"/>
<text x="14" y="429.3" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">2</text>
<text x="34" y="429.3" font-size="16" font-weight="700" fill="#004d47">Las tareas en curso, arriba</text>
<text x="34" y="449.3" font-size="15" fill="#555">código en amarillo y cuenta de pasos</text>
<circle cx="14" cy="472.3" r="11" fill="#f97316"/>
<text x="14" y="477.3" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">3</text>
<text x="34" y="477.3" font-size="16" font-weight="700" fill="#004d47">Una H</text>
<text x="34" y="497.3" font-size="15" fill="#555">en cola desde una sesión anterior</text>
<circle cx="14" cy="520.3" r="11" fill="#f97316"/>
<text x="14" y="525.3" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">4</text>
<text x="34" y="525.3" font-size="16" font-weight="700" fill="#004d47">Una tarea desplegada</text>
<text x="34" y="545.3" font-size="15" fill="#555">el texto entero, sin sangría</text>
<circle cx="14" cy="568.3" r="11" fill="#f97316"/>
<text x="14" y="573.3" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">5</text>
<text x="34" y="573.3" font-size="16" font-weight="700" fill="#004d47">Botones</text>
<text x="34" y="593.3" font-size="15" fill="#555">T y C en verde, D en amarillo, E en rojo</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Pendientes desplegada: dos tareas en curso arriba y, debajo, las que esperan en cola.</figcaption>
</figure>

La cabecera dice el total y su reparto por letra: «3 (1A + 2H)». Las H van en rojo y no se pone la letra que no tiene ninguna.

Si `.sf/peticiones.json` tiene tareas sin texto o con un estado desconocido, no se enseñan. Un aviso amarillo al principio del bloque TAREAS, antes de Pendientes, dice cuántas son. Si el archivo no se puede leer, el aviso lo dice. Sale aunque Pendientes no salga.

### Testing

Lo que espera tu prueba: las tareas en el estado `sin-probar`. La cabecera dice cuántas son. La que ha cambiado la última va arriba.

<figure class="vertical" style="margin:1.6rem 0 1.4rem;">
<svg viewBox="0 0 560 638.6" width="100%" role="img" aria-label="Secciones Testing y Cerradas con sus partes numeradas" style="font-family:var(--fuente-texto);display:block">
<image href="capturas/panel/testing-cerradas.png" x="26" y="0" width="508" height="333.6"/>
<rect x="45.2" y="23" width="466.5" height="37.1" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="41.5" x2="45.2" y2="41.5" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="41.5" r="10" fill="#f97316"/>
<text x="11" y="46.5" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
<rect x="28.6" y="76" width="273.5" height="19.2" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="85.6" x2="28.6" y2="85.6" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="85.6" r="10" fill="#f97316"/>
<text x="11" y="90.6" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">2</text>
<rect x="419.6" y="76" width="114.4" height="19.2" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="534" y1="85.6" x2="539" y2="85.6" stroke="#f97316" stroke-width="1.5"/>
<circle cx="549" cy="85.6" r="10" fill="#f97316"/>
<text x="549" y="90.6" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">3</text>
<rect x="437.5" y="113.7" width="96.5" height="17.3" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="534" y1="122.4" x2="539" y2="122.4" stroke="#f97316" stroke-width="1.5"/>
<circle cx="549" cy="122.4" r="10" fill="#f97316"/>
<text x="549" y="127.4" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">4</text>
<rect x="518" y="131" width="16" height="172.5" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="534" y1="217.3" x2="539" y2="217.3" stroke="#f97316" stroke-width="1.5"/>
<circle cx="549" cy="217.3" r="10" fill="#f97316"/>
<text x="549" y="222.3" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">5</text>
<rect x="45.2" y="311.2" width="39.6" height="17.9" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="320.1" x2="45.2" y2="320.1" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="320.1" r="10" fill="#f97316"/>
<text x="11" y="325.1" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">6</text>
<circle cx="14" cy="363.6" r="11" fill="#f97316"/>
<text x="14" y="368.6" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>
<text x="34" y="368.6" font-size="16" font-weight="700" fill="#004d47">Tareas en Testing</text>
<text x="34" y="388.6" font-size="15" fill="#555">con la T; esperan tu prueba</text>
<circle cx="14" cy="411.6" r="11" fill="#f97316"/>
<text x="14" y="416.6" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">2</text>
<text x="34" y="416.6" font-size="16" font-weight="700" fill="#004d47">Cabecera de Cerradas</text>
<text x="34" y="436.6" font-size="15" fill="#555">total y reparto; las C, en verde</text>
<circle cx="14" cy="459.6" r="11" fill="#f97316"/>
<text x="14" y="464.6" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">3</text>
<text x="34" y="464.6" font-size="16" font-weight="700" fill="#004d47">«limpiar (N)»</text>
<text x="34" y="484.6" font-size="15" fill="#555">saca de la lista las C, las D y las R</text>
<circle cx="14" cy="507.6" r="11" fill="#f97316"/>
<text x="14" y="512.6" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">4</text>
<text x="34" y="512.6" font-size="16" font-weight="700" fill="#004d47">R esperando el segundo clic</text>
<text x="34" y="532.6" font-size="15" fill="#555">hoy, «R eliminar» y «R pendiente»</text>
<circle cx="14" cy="555.6" r="11" fill="#f97316"/>
<text x="14" y="560.6" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">5</text>
<text x="34" y="560.6" font-size="16" font-weight="700" fill="#004d47">R de revertir</text>
<text x="34" y="580.6" font-size="15" fill="#555">en las C que tienen commit en develop</text>
<circle cx="14" cy="603.6" r="11" fill="#f97316"/>
<text x="14" y="608.6" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">6</text>
<text x="34" y="608.6" font-size="16" font-weight="700" fill="#004d47">Una H en Cerradas</text>
<text x="34" y="628.6" font-size="15" fill="#555">reabierta: vuelve a estar en la cola</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Testing y Cerradas desplegadas, con una R esperando el segundo clic. La captura es anterior: la R dice «R revertir», y ahora se parte en dos.</figcaption>
</figure>

Un **«✓» verde** tras el número dice que Claude ya ha comprobado la tarea en lo que puede, en el campo `comprobado`. No la saca de Testing: solo tu OK la saca. Desplegada, la tarea enseña «✓ Claude: …», con lo que comprobó, y «probar: …», con lo que tienes que probar tú.

### Cerradas

Las tareas con un cierre en esta sesión, en la cola o ya fuera, lo último arriba. Salen del historial: entra la que tiene en la sesión un evento de cierre (a Testing, cerrada, probada, descartada, revertida o reabierta), y la ordena la fecha del último. Las eliminadas y las absorbidas por `/fusionar` no entran, porque salen sin cerrarse. Tampoco las tareas sin historial, anteriores al CLI.

Una C revertida con «R pendiente» sigue en la lista como reabierta, en rojo con H; con «R eliminar», sale. Si una tarea quitada con «limpiar» se reabre o se vuelve a cerrar, vuelve a la lista, arriba.

Si falló el push de `develop` al cerrar una tarea, su línea lleva «· falta el push», y debajo de Cerradas sale «falta el push de develop (N…)», hasta que `origin/develop` tiene su commit.

La cabecera dice el total y su reparto: «3 (1T + 2C)», con las C en verde y las demás atenuadas. Se ve siempre, también con 0. Si una línea está recortada o tiene commit, un clic la despliega: el texto entero y el commit, o «sin commit».

El botón **«limpiar (N)»**, a la derecha del título, saca de la lista las cerradas y probadas, las C, las revertidas antiguas, las R, y las descartadas, las D, que además salen de la cola con `cola.py limpiar`. El panel recuerda cada limpiada con la fecha de su último cierre, así que vuelve si se reabre o se vuelve a cerrar. Una reabierta, con H, no se limpia: sigue pidiendo trabajo. Sin ninguna que limpiar, el botón no sale. Las descartadas que quedaron de otra sesión salen de la cola al abrir una sesión nueva, no con `/reload-plugins`.

El texto y el commit de las que ya han salido de la cola se leen en `.sf/historial.jsonl`.

## Proyecto

De momento, el bloque PROYECTO solo tiene **Documentos**. La fase y la devslice ya van bajo la cabecera.

<figure class="vertical" style="margin:1.6rem 0 1.4rem;">
<svg viewBox="0 0 560 438.8" width="100%" role="img" aria-label="Sección Documentos con sus partes numeradas" style="font-family:var(--fuente-texto);display:block">
<image href="capturas/panel/documentos.png" x="26" y="24" width="508" height="205.8"/>
<rect x="28.6" y="26.6" width="168.7" height="19.2" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<circle cx="112.9" cy="12" r="10" fill="#f97316"/>
<text x="112.9" y="17" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
<rect x="45.2" y="45.7" width="95.8" height="17.9" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="54.7" x2="45.2" y2="54.7" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="54.7" r="10" fill="#f97316"/>
<text x="11" y="59.7" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">2</text>
<rect x="45.2" y="98.1" width="185.3" height="17.9" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="107.1" x2="45.2" y2="107.1" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="107.1" r="10" fill="#f97316"/>
<text x="11" y="112.1" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">3</text>
<rect x="45.2" y="187.6" width="226.8" height="17.9" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="196.5" x2="45.2" y2="196.5" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="196.5" r="10" fill="#f97316"/>
<text x="11" y="201.5" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">4</text>
<circle cx="14" cy="259.8" r="11" fill="#f97316"/>
<text x="14" y="264.8" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>
<text x="34" y="264.8" font-size="16" font-weight="700" fill="#004d47">Cabecera</text>
<text x="34" y="284.8" font-size="15" fill="#555">tipos que existen, de los diez</text>
<circle cx="14" cy="307.8" r="11" fill="#f97316"/>
<text x="14" y="312.8" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">2</text>
<text x="34" y="312.8" font-size="16" font-weight="700" fill="#004d47">«✓», existe</text>
<text x="34" y="332.8" font-size="15" fill="#555">con su cantidad detrás, atenuada</text>
<circle cx="14" cy="355.8" r="11" fill="#f97316"/>
<text x="14" y="360.8" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">3</text>
<text x="34" y="360.8" font-size="16" font-weight="700" fill="#004d47">«·», falta</text>
<text x="34" y="380.8" font-size="15" fill="#555">atenuado</text>
<circle cx="14" cy="403.8" r="11" fill="#f97316"/>
<text x="14" y="408.8" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">4</text>
<text x="34" y="408.8" font-size="16" font-weight="700" fill="#004d47">«◦», falta y es opcional</text>
<text x="34" y="428.8" font-size="15" fill="#555">atenuado, con «(opcional)»</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Documentos en la SF: cinco de los diez tipos.</figcaption>
</figure>

La cabecera dice cuántos tipos de documento existen de los diez: «5/10». Cada línea es un tipo:

- **✓** existe, con su cantidad atenuada detrás: «✓ Visión 3».
- **·** falta, atenuado.
- **◦** falta y es opcional, atenuado y con «(opcional)».

Los tipos y dónde se buscan:

- Visión: los `.md` de `docs/specs/vision/` que no empiezan por «fundacional».
- Fundacional: los `.md` de esa carpeta que sí empiezan así.
- Especificación funcional: los `.md` de `docs/specs/funcional/`.
- Definición técnica: los `.md` de `docs/specs/tecnica/`.
- Devslices: cualquier archivo de `docs/specs/devslices/`.
- Decisiones: los `.md` de `docs/decisiones/`, una decisión por archivo, sin contar su índice, `README.md`.
- Guía de instalación: `docs/guias/instalacion.md`.
- Guía de actualización: `docs/guias/actualizacion.md`.
- Infografías, opcional: los `.html` de `docs/specs/vision/infografias/`.
- Cómo funciona la Software Factory, opcional: `docs/como-funciona-la-software-factory.md`.

No cuentan los archivos que empiezan por «.» o «_».

## SF ENHANCE

El bloque SF ENHANCE reúne lo de la propia SF y se ve igual desde cualquier proyecto. Desde otro proyecto, el panel encuentra la SF por `~/.claude/sf/fuente.json`, que el mod apunta cada vez que se abre en ella.

<figure class="vertical" style="margin:1.6rem 0 1.4rem;">
<svg viewBox="0 0 560 669.2" width="100%" role="img" aria-label="Secciones Registro y Mejoras con sus partes numeradas" style="font-family:var(--fuente-texto);display:block">
<image href="capturas/panel/registro-mejoras.png" x="26" y="0" width="508" height="412.2"/>
<rect x="45.2" y="20.4" width="156.6" height="17.9" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="29.4" x2="45.2" y2="29.4" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="29.4" r="10" fill="#f97316"/>
<text x="11" y="34.4" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
<rect x="500.1" y="20.4" width="33.9" height="17.9" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="534" y1="29.4" x2="539" y2="29.4" stroke="#f97316" stroke-width="1.5"/>
<circle cx="549" cy="29.4" r="10" fill="#f97316"/>
<text x="549" y="34.4" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">2</text>
<rect x="28.6" y="269.7" width="118.9" height="19.2" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="279.2" x2="28.6" y2="279.2" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="279.2" r="10" fill="#f97316"/>
<text x="11" y="284.2" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">3</text>
<rect x="43.9" y="323.3" width="397.5" height="19.2" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="332.9" x2="43.9" y2="332.9" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="332.9" r="10" fill="#f97316"/>
<text x="11" y="337.9" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">4</text>
<rect x="43.9" y="342.5" width="33.2" height="69.7" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="377.3" x2="43.9" y2="377.3" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="377.3" r="10" fill="#f97316"/>
<text x="11" y="382.3" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">5</text>
<circle cx="14" cy="442.2" r="11" fill="#f97316"/>
<text x="14" y="447.2" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>
<text x="34" y="447.2" font-size="16" font-weight="700" fill="#004d47">Marca y proyecto</text>
<text x="34" y="467.2" font-size="15" fill="#555">✓ acierto, « dicho, ✗ fricción, · nota</text>
<circle cx="14" cy="490.2" r="11" fill="#f97316"/>
<text x="14" y="495.2" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">2</text>
<text x="34" y="495.2" font-size="16" font-weight="700" fill="#004d47">«→» y «−»</text>
<text x="34" y="515.2" font-size="15" fill="#555">pasar la entrada a tarea; borrarla</text>
<circle cx="14" cy="538.2" r="11" fill="#f97316"/>
<text x="14" y="543.2" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">3</text>
<text x="34" y="543.2" font-size="16" font-weight="700" fill="#004d47">Cabecera de Mejoras</text>
<text x="34" y="563.2" font-size="15" fill="#555">propuestas por decidir</text>
<circle cx="14" cy="586.2" r="11" fill="#f97316"/>
<text x="14" y="591.2" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">4</text>
<text x="34" y="591.2" font-size="16" font-weight="700" fill="#004d47">Tres cuentas</text>
<text x="34" y="611.2" font-size="15" fill="#555">abiertas, por decidir y sin kanban</text>
<circle cx="14" cy="634.2" r="11" fill="#f97316"/>
<text x="14" y="639.2" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">5</text>
<text x="34" y="639.2" font-size="16" font-weight="700" fill="#004d47">Número fijo, subrayado</text>
<text x="34" y="659.2" font-size="15" fill="#555">un clic despliega su resumen</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">El bloque SF ENHANCE con Registro y Mejoras desplegadas.</figcaption>
</figure>

### Registro

Lo que Claude observa al trabajar con la SF, en `.sf/registro.json` de la SF. Es común a todos los proyectos. Claude anota en tiempo real, sin interrumpir y solo lo significativo. El registro es el feedback sobre la SF: no hay resumen aparte. El uso está en [Uso del panel](uso-del-panel.md).

Cada entrada empieza con una marca de su tipo:

- **✗** en rojo: una fricción, algo que estorba, falla o falta.
- **✓** en verde: un acierto, algo que ayudó.
- **«**: algo que has dicho, con tus palabras.
- **·**: una nota.

Detrás va el proyecto donde se observó, atenuado, y el texto. Al final, dos botones, que no pasan por Claude:

- **«→»** la pasa a tarea. El panel la añade a la cola del proyecto de la sesión, en cola, con el texto de la entrada, sin descripción y con el número siguiente al último dado. Después borra la entrada y avisa: «Tarea N en cola: …». Si no puede escribir el registro, deja la cola como estaba. Renombrar la tarea queda para ti o para Claude.
- **«−»**, en rojo, borra la entrada del todo.

Claude borra también lo resuelto: el registro solo guarda lo abierto. Vacío, la sección dice para qué sirve, y también si el panel no encuentra la SF. Una entrada sin texto no se enseña, y una de tipo desconocido se enseña como nota.

### Mejoras

Las propuestas de mejora de la SF que esperan tu sí o no, de `docs/propuestas.md` de la SF. La cabecera dice cuántas son.

La primera línea lo recuerda: «Mejoras de la SF que esperan tu sí o no (docs/propuestas.md)». La segunda da tres cuentas de las propuestas pendientes:

- **Abiertas**: todas las del apartado «Propuestas pendientes».
- **Por decidir**: las que dicen en su «Estado» «pendiente de aprobación» o «pendiente de decisión». Son las que se listan.
- **Sin kanban**: las que no tienen la línea «Kanban».

Cada propuesta lleva su número fijo, subrayado, que no cambia aunque se decidan otras: P01, P02… Un clic despliega su resumen: la primera frase de su «Cambio propuesto» o, si no tiene, de su «Propuesta original» o del primer apartado con texto. Si pasa de 220 caracteres, se corta con «…».

Si en la sesión Claude registra una mejora en la SF desde otro proyecto, la sección lo dice: «Esta sesión ha registrado 1 mejora(s) en la SF». Si el panel no encuentra la SF, la sección solo sale cuando hay alguna así, con el título «Realimentación» y la cuenta «1 registradas».

## La caja sobre el prompt

Cuando el panel no está a la vista, el mod se enseña sobre el prompt, en una caja pequeña con borde redondeado, alineada a la derecha.

<figure class="vertical" style="margin:1.6rem 0 1.4rem;">
<svg viewBox="0 0 560 308.3" width="100%" role="img" aria-label="Caja sobre el prompt con sus partes numeradas" style="font-family:var(--fuente-texto);display:block">
<image href="capturas/panel/caja.png" x="26" y="0" width="508" height="99.3"/>
<rect x="43.5" y="20.4" width="210.2" height="15.8" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="28.3" x2="43.5" y2="28.3" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="28.3" r="10" fill="#f97316"/>
<text x="11" y="33.3" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
<rect x="43.5" y="36.2" width="478.8" height="16.3" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="522.3" y1="44.4" x2="539" y2="44.4" stroke="#f97316" stroke-width="1.5"/>
<circle cx="549" cy="44.4" r="10" fill="#f97316"/>
<text x="549" y="49.4" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">2</text>
<rect x="43.5" y="52.6" width="400" height="16.3" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="21" y1="60.7" x2="43.5" y2="60.7" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="60.7" r="10" fill="#f97316"/>
<text x="11" y="65.7" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">3</text>
<rect x="43.5" y="68.9" width="157.7" height="16.3" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="201.2" y1="77.1" x2="539" y2="77.1" stroke="#f97316" stroke-width="1.5"/>
<circle cx="549" cy="77.1" r="10" fill="#f97316"/>
<text x="549" y="82.1" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">4</text>
<circle cx="14" cy="129.3" r="11" fill="#f97316"/>
<text x="14" y="134.3" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>
<text x="34" y="134.3" font-size="16" font-weight="700" fill="#004d47">Primera línea</text>
<text x="34" y="154.3" font-size="15" fill="#555">dónde estás, en negrita</text>
<circle cx="14" cy="177.3" r="11" fill="#f97316"/>
<text x="14" y="182.3" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">2</text>
<text x="34" y="182.3" font-size="16" font-weight="700" fill="#004d47">Tareas en curso</text>
<text x="34" y="202.3" font-size="15" fill="#555">con «▶», recortadas</text>
<circle cx="14" cy="225.3" r="11" fill="#f97316"/>
<text x="14" y="230.3" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">3</text>
<text x="34" y="230.3" font-size="16" font-weight="700" fill="#004d47">Cuentas</text>
<text x="34" y="250.3" font-size="15" fill="#555">solo las que no son cero, atenuadas</text>
<circle cx="14" cy="273.3" r="11" fill="#f97316"/>
<text x="14" y="278.3" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">4</text>
<text x="34" y="278.3" font-size="16" font-weight="700" fill="#004d47">Cómo abrir el panel</text>
<text x="34" y="298.3" font-size="15" fill="#555">«/sf abre el panel»</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">La caja sobre el prompt en la SF, con el panel cerrado. La captura aún dice «mejoras SF a valorar».</figcaption>
</figure>

La caja sale siempre, salvo con el panel a la vista: colocado y al frente. Así sale:

- en la pantalla normal de Claude Code;
- en un terminal demasiado estrecho para el panel;
- con el panel cerrado a mano, hasta que lo reabres con `/sf`;
- con el panel abierto pero detrás de otra pestaña.

Al cerrar el panel, la caja se vuelve a pintar en el momento. No sale mientras Claude Code enseña una encuesta, ni antes de la primera lectura del estado.

Su primera línea, en negrita, tiene una de estas formas:

| Situación | Primera línea |
| --- | --- |
| Proyecto bajo la SF | `SF 0.7 · LecturaFàcil · 2/7 Especificación e interfaz · devslice 2` |
| Proyecto atrasado | `SF 0.13 → 0.34.3 · LecturaFàcil · …` |
| Fase sin declarar | `SF 0.7 · LecturaFàcil · fase sin declarar` |
| Repositorio de la propia SF | `SF · repositorio de la SF` |
| Proyecto sin SF | `Sin SF` |
| Estado ilegible o fase desconocida | `SF 0.7 · LecturaFàcil · ⚠ revisar .sf/` |
| Estado aún en `docs/sf.json` | `… · ⚠ mover a .sf/` |

Debajo, cada tarea en curso con «▶», recortada a 56 caracteres. Después, en una línea atenuada y solo lo que no es cero, cuatro cuentas con su número:

- «en cola»: las que esperan en cola, sin las en curso;
- «testing»: las de Testing;
- «mejoras»: las propuestas por decidir, las de la sección Mejoras;
- «registradas en la SF»: las mejoras registradas en la SF desde esta sesión.

Al final van los avisos en amarillo, «⚠ revisar .sf/» o «⚠ revisar .sf/peticiones.json», y «/sf abre el panel».

## Actuar desde el panel

Desde el panel se cambian las tareas sin escribir en el chat: con los botones de cada tarea, con el «?» y la E de los pasos, con cuatro comandos, con la etiqueta de prueba y con TURBO, RELEASE y ACTUALIZAR. Salvo el «?», `/redescribir` y TURBO, nada de esto pasa por Claude: lo que se puede hacer con un comando lo hace el panel, según la decisión [Comandos antes que inferencia](decisiones/092-2026-10-29-comandos-antes-que-inferencia.md). Si el caso pide criterio, el panel dice por qué y no hace nada, o se lo pasa a Claude.

### Botones de las tareas

A la derecha de una tarea van sus botones: la T de Test Mode, la C de cerrar, la S de separar y, detrás, la E de eliminar, la D de descartar o, en Testing, la R de revertir. En Cerradas va también la R. Mientras un subagente trabaja en la tarea, en lugar de la T va una ⚙ (ver «⚙, un subagente en la tarea»).

<figure class="vertical" style="margin:1.6rem 0 1.4rem;">
<svg viewBox="0 0 560 260.4" width="100%" role="img" aria-label="Botones de dos tareas en curso con sus partes numeradas" style="font-family:var(--fuente-texto);display:block">
<image href="capturas/panel/botones.png" x="26" y="24" width="508" height="75.4"/>
<rect x="393.4" y="26.6" width="33.9" height="17.3" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<circle cx="410.4" cy="12" r="10" fill="#f97316"/>
<text x="410.4" y="17" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
<rect x="429.8" y="26.6" width="103.5" height="17.3" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="533.4" y1="35.2" x2="539" y2="35.2" stroke="#f97316" stroke-width="1.5"/>
<circle cx="549" cy="35.2" r="10" fill="#f97316"/>
<text x="549" y="40.2" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">2</text>
<rect x="518" y="61.1" width="16" height="17.9" rx="3" fill="none" stroke="#f97316" stroke-width="2"/>
<line x1="534" y1="70" x2="539" y2="70" stroke="#f97316" stroke-width="1.5"/>
<circle cx="549" cy="70" r="10" fill="#f97316"/>
<text x="549" y="75" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">3</text>
<circle cx="14" cy="129.4" r="11" fill="#f97316"/>
<text x="14" y="134.4" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>
<text x="34" y="134.4" font-size="16" font-weight="700" fill="#004d47">T y C</text>
<text x="34" y="154.4" font-size="15" fill="#555">Test Mode y cerrar, en verde y en negrita</text>
<circle cx="14" cy="177.4" r="11" fill="#f97316"/>
<text x="14" y="182.4" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">2</text>
<text x="34" y="182.4" font-size="16" font-weight="700" fill="#004d47">D esperando el segundo clic</text>
<text x="34" y="202.4" font-size="15" fill="#555">«D descartar», en negrita</text>
<circle cx="14" cy="225.4" r="11" fill="#f97316"/>
<text x="14" y="230.4" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">3</text>
<text x="34" y="230.4" font-size="16" font-weight="700" fill="#004d47">E de eliminar</text>
<text x="34" y="250.4" font-size="15" fill="#555">en rojo, en las tareas sin rama</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Arriba, la 141 con su P, su C y su D a punto de descartar; la 102, sin rama, con su E. La captura es anterior a la T: donde pone P, hoy va la T.</figcaption>
</figure>

La E y la D nunca van juntas, porque una tarea con rama no se puede eliminar. Una tarea ya en `develop`, también la de Testing, se revierte con la R, no se descarta.

Los botones escriben la cola con `cola.py --json --quien propietario --via panel`. No usan el `cola.py` del disco, sino una copia que el panel hace al cargarse, también con `/reload-plugins`, en `~/.claude/sf/cola-<sesión>.py`. Así el panel y el CLI son siempre de la misma versión, aunque la C, la R o la T cambien la rama activa y, con ella, el `cola.py` del disco. Un cambio en `cola.py` llega al panel al recargarlo. Si la copia falla, usa el del disco y avisa una vez. El CLI hace el cambio, con git cuando toca, y lo apunta en el historial de la tarea. Antes, el panel relee la cola y comprueba que la tarea sigue como la viste. Si el CLI no lo hace, el aviso lleva su motivo detrás de la letra del botón: «C: …».

La E, la D, la C y la R piden **dos clics**. El primero cambia el símbolo por «E eliminar», «D descartar» o «C cerrar», en negrita, y el segundo actúa. La R se parte en dos, «R eliminar» y «R pendiente», y el segundo clic elige el destino. A los 5 segundos, o con un clic en otro botón del panel, vuelve a ser el símbolo. La T y la S actúan con un clic.

Cada fila de las secciones reserva sitio para sus botones: con la T, la C, la S y la D, el título se recorta antes para que la línea no se parta. Después de actuar, cada botón avisa en una línea de lo que ha hecho.

#### T, Test Mode

Verde y en negrita. Sale en las tareas con rama, en cola, en curso o en Testing, si la rama existe y no es la activa. Si ya es la activa, no sale, porque la cabecera ya muestra la rama en amarillo. Va en Pendientes, arriba y en Testing.

La T pone la tarea en prueba, pero no la da por probada: no marca «Probar la tarea». Probada lo está cuando lo dices o pulsas la C.

Con un clic, el panel activa la rama con `git switch`. Si la tarea estaba en cola, la pasa a en curso. Después avisa con un mensaje que empieza por «T:», con lo que hay que probar. No recarga el plugin ni activa el modo prueba: si la rama lo necesita, `/reload-plugins` lo lanzas tú. Para volver a `develop`, pídeselo a Claude: no hay botón.

No cambia de rama si la activa tiene cambios sin commit o si la tarea ya no tiene esa rama.

Si la rama está en otro worktree, la T sale, pero al pulsarla no cambia de rama y avisa en qué carpeta está.

#### C, cerrar

Verde y en negrita, como la T. Sale en las tareas en curso con una rama que existe, que tienen el paso «Cerrar la tarea» y ningún otro pendiente, salvo «Probar la tarea». Sin pasos no hay C: Claude añade los dos de cierre al dejar la tarea lista para probar. Va en Pendientes y arriba. Pulsarla es tu OK: «probada, ciérrala».

Para cerrar sin probar, quita antes «Probar la tarea» con su E. «Cerrar la tarea» no se quita nunca.

Con `cola.py cerrar`, el panel pasa a `develop` y hace el squash de la rama con su commit, «<tarea> (N)», con los pasos hechos en el cuerpo. Después hace push de `develop`, borra la rama y saca la tarea de la cola. La tarea entra en Cerradas con la C, y el aviso da el commit: «Cerrada la N en develop (…)». Si falla el push o no puede borrar la rama, la cierra igual y avisa de lo que falta.

No hace nada si la rama está en otro worktree o si hay cambios sin commit. Si el squash choca o falla el commit, lo deshace y vuelve a la rama de antes, sin tocar la cola. Después pasa a Claude el prompt para resolverlo, con los archivos en conflicto, y para repetirlo con `cola.py cerrar N`.

#### S, separar

Azul y en negrita. Sale en las tareas en cola o en curso con dos pasos pendientes o más, sin contar «Probar la tarea» ni «Cerrar la tarea». Va en Pendientes y arriba, detrás de la T y la C.

Con un clic abre el menú de `/split` con los pasos pendientes, cada uno con su número en la tarea, y se pueden elegir varios. Separa sin Claude, igual que `/split`.

El menú admite cuatro opciones. Con más de cuatro pasos pendientes, no lo abre: recuerda la forma corta, `/split N 2,3`.

#### E, eliminar

Roja. Sale en las tareas en cola o en curso sin rama, que aún no han cambiado ningún activo. Va en Pendientes y arriba.

La quita de la cola sin rastro: no entra en Cerradas y su número no se reutiliza. Si vuelve a la cola en la misma sesión, es la eliminación deshecha: vuelve a Pendientes con su letra, no a Cerradas como reabierta.

#### D, descartar

Negra y en negrita sobre fondo amarillo, para distinguirla de la E. Sale en las tareas con rama, en cola o en curso, que aún no han entrado en `develop`. Va en Pendientes y arriba.

Lo hace con `cola.py descartar`. Si la rama es la activa, pasa antes a `develop`. Después la borra con `git branch -D` y pasa la tarea al estado `descartada`, sin sacarla de la cola: sale al limpiar Cerradas. Si la rama ya no existe, solo la pasa a descartada.

No hace nada si la rama está en otro worktree, con su ruta en el aviso, o si es la activa y tiene cambios sin commit. Si git falla, no toca la cola.

#### R, revertir

Negra y en negrita sobre fondo naranja. Sale en Cerradas, en las C que han entrado en `develop`, y en Testing, en las tareas con commits en `develop`. Los commits salen del historial de la tarea; en una sin historial, de la historia de `develop`: son de la tarea N los commits de primer padre cuyo título acaba en « (N)», como el squash de la C. Un «Revert "… (N)"» deja fuera los anteriores a él; si después vuelve a entrar algo de la tarea, la R vuelve a salir. Una tarea antigua en Testing sin commits en `develop` no lleva ni D ni R.

Con el primer clic, la R se parte en **«R eliminar»** y **«R pendiente»**; a los 5 segundos, o con un clic en otro sitio, vuelve a ser la R. El segundo clic lanza `cola.py revertir N --eliminar` o `--pendiente`: pasa a `develop` si no es la activa y hace `git revert --no-edit` de esos commits, del más reciente al más antiguo. Se queda en `develop` y no hace push: el push es del cierre.

- **«R eliminar»**: la tarea sale de la cola sin rastro, como con la E. No entra en Cerradas, su número no se reutiliza y `cola.py restaurar N` la devuelve.
- **«R pendiente»**: vuelve a Pendientes, en cola, reabierta, con H y sin rama. En Cerradas sale en rojo con su H, como cualquier reabierta.

Ninguna tarea queda ya en Cerradas con la R. Desde Claude, `cola.py revertir` pide siempre el destino: si no lo dices, Claude te pregunta cuál.

No hace nada si `develop` ha cambiado desde que se pintó el botón, si hay cambios sin commit o si `develop` está en otro worktree. Si el revert choca, lo deshace con `git revert --abort`, vuelve a la rama de antes y se lo pasa a Claude, con la tarea y los commits.

#### ⚙, un subagente en la tarea

Mientras un subagente trabaja en una tarea, la tarea lleva una **⚙** atenuada en el sitio de la T y no muestra la T, la C, la D ni la E. Así no se cierra ni se descarta una rama que otro está cambiando. Sale en Pendientes, arriba y en Testing.

Pulsarla solo avisa de qué subagente trabaja en ella: «⚙: un subagente trabaja en la 148 (Tarea 148: …)».

El panel lo lee de los subagentes en marcha del motor, con `$.agent.list()`. Cuenta uno en estado `pending`, `running` o `waiting` cuya descripción empiece por «Tarea NN», sin distinguir mayúsculas; «Tarea 1480» no es la 148. Por eso el principal lanza cada subagente con la descripción «Tarea NN: …». Si la lista falla, no sale ninguna ⚙.

Los subagentes se releen al lanzar uno, tras cada herramienta y en el latido de cada minuto. La ⚙ de uno que acaba se va al momento o, como mucho, en un minuto.

No mira los worktrees: uno que queda tras acabar el subagente no da ⚙. Con la rama en un worktree y sin subagente, la T, la C y la D salen, pero al pulsarlas no actúan y avisan de en qué carpeta está la rama.

### Añadir un paso: `/paso`

`/paso texto` añade un paso pendiente a la tarea en curso al momento, antes de «Probar la tarea» y «Cerrar la tarea» si los tiene, también a mitad de turno. Vale también para la tarea que se está probando. Además se lo pide a Claude, que lo hace sin esperar un «continúa»: al momento si está parado y, si está trabajando, al acabar el turno.

Con varias tareas en curso, `/paso` pregunta a cuál, con las cuatro más recientes como opciones. `/paso 64 texto` elige la 64 sin preguntar, si está en curso. Si no lo está y solo hay una en curso, todo el texto, «64 texto» incluido, va a esa. Sin ninguna en curso, avisa de que hay que decírselo a Claude en el chat.

### Separar pasos en una tarea nueva: `/split`

`/split 89 2,3` separa de la 89 sus pasos 2 y 3 en una tarea nueva, también a mitad de turno. Los pasos se numeran 1, 2, 3… en el orden en que salen al desplegar la tarea. La respuesta dice en una línea lo que ha hecho.

La tarea nueva lleva el número siguiente al último dado, el campo `ultimo` de la cola. Va en cola, con esos pasos y su estado, y se llama como su primer paso. No lleva descripción de origen y empieza sin rama. Si un paso separado ya está hecho, la respuesta avisa de que su trabajo sigue en la rama de la 89. Renombrar la nueva o la 89, si hace falta, queda para ti o para Claude.

Solo se separan pasos de tareas en curso o en cola con dos pasos o más, y nunca todos, porque eso es renombrarla. Antes de escribir, el mod relee la cola: si la tarea o sus pasos han cambiado, avisa y no toca nada.

Sin pasos, `/split 89` pregunta cuáles, con varios a la vez. `/split` a secas pregunta antes la tarea. El diálogo admite cuatro opciones: con más tareas salen las cuatro más recientes, y otra se escribe por su número en «Other». Una tarea con más de cuatro pasos los lista y pide la forma corta. «Probar la tarea» y «Cerrar la tarea» no salen en el menú: no se separan.

### Fusionar tareas: `/fusionar`

`/fusionar 104 105 107` junta esas tareas en una, también a mitad de turno. Queda la de número más alto, con su número y su nombre: así el hueco queda en el histórico. La respuesta dice en una línea lo que ha hecho.

La que queda reúne los pasos de todas por orden de número de tarea, cada uno con su estado. Una tarea sin pasos aporta uno con su nombre, pendiente si estaba en cola y en curso si estaba en curso. Si alguna estaba en curso, la que queda pasa a en curso.

Conserva su descripción y le añade detrás las de las otras, tal cual, sin origen, cada una en su párrafo. El panel pinta cada párrafo aparte, con una línea en blanco entre ellos. Si no tiene prueba, se lleva la de otra. Si una tenía rama, pasa a la que queda.

Las demás salen de la cola sin cerrarse: no entran en Cerradas ni cuentan como hechas, y sus números no se reutilizan. Si una vuelve a la cola en la misma sesión, es la fusión deshecha: vuelve a Pendientes con su letra, no a Cerradas como reabierta.

Solo se fusionan tareas en cola o en curso, y como mucho una con rama. Una en Testing, descartada o que no está en la cola no se fusiona: el mod dice por qué y no toca nada. Antes de escribir relee la cola: si alguna tarea ha cambiado, avisa y no toca nada.

`/fusionar` a secas pregunta cuáles, con varias a la vez, entre las cuatro más recientes en cola o en curso; otra se escribe por su número en «Other». Con menos de dos elegidas, no fusiona.

### Redactar de nuevo una descripción: `/redescribir`

`/redescribir 162` pide a Claude que vuelva a redactar la descripción de la 162 para que se lea fácilmente: frases claras y cortas, sin quitar ni añadir nada, cada idea en su párrafo. Claude te enseña la propuesta y espera tu OK; solo entonces la guarda con `cola.py redescribir`. Es el único comando que pasa por Claude, porque redactar es criterio.

Sin número, con una tarea que no está en la cola o sin descripción, lo dice y no pide nada.

### Modo prueba

En el repositorio de la SF, la etiqueta de prueba de la cabecera cambia entre el plugin publicado y la copia de trabajo, para ver un cambio sin commit ni publicación. Un clic cambia `.claude/settings.local.json` y lanza `/reload-plugins`, que aplica el cambio.

El modo prueba se apaga solo al empezar cada sesión. Lo hace una vez por sesión: la marca queda en `.sf/prueba.json`, y un `/reload-plugins` posterior no lo vuelve a apagar. Si la sesión arrancó desde la copia de trabajo, porque la anterior se cerró sin apagarlo, lanza `/reload-plugins` para volver al publicado. Al cerrar la sesión, también se apaga.

Cada arranque del panel y cada cambio del modo prueba quedan en `.sf/prueba.log`, fuera de git, con quién lo hizo: la etiqueta, el arranque de una sesión nueva o el cierre de la sesión. Solo se escribe en la SF, donde está registrado el catálogo local `softwarefactory-dev`; en los demás proyectos no se crea. Sirve para averiguar por qué se apaga a veces solo al cambiar de rama.

Cómo se prepara el catálogo local está en [Cómo funciona la Software Factory](como-funciona-la-software-factory.html#publicacion-del-plugin).

### TURBO

TURBO lanza de una vez el trabajo que no te necesita. Al pulsarlo, el panel avisa con un toast, «TURBO: se lo paso a Claude.», y le pasa este prompt como si lo escribieras tú:

> TURBO: revisa la cola y pon en curso las tareas que se pueden hacer sin interacción con el propietario; lánzalas con subagentes y avísame de cuáles.

Lo envía desde un temporizador, porque el motor no deja enviar un prompt desde el hook que atiende el panel. Pasa por Claude porque decidir qué tareas no te necesitan es criterio, no un comando. Cada subagente que lance pone su ⚙ en su tarea.

### RELEASE

RELEASE publica el proyecto: pasa `develop` a `main` y lo marca con el tag `vX.Y.Z`, con comandos y sin Claude. Sale en la SF y en todos los proyectos con SF, según la decisión [Botón RELEASE](decisiones/123-2026-10-29-boton-release-version-elegida-al-pulsar-fast-forward-y-aviso-de-lo-sin-probar.md).

El primer clic lee la versión actual. En la SF es la `version` de `plugins/sf/.claude-plugin/plugin.json`; en los demás proyectos, el último tag `vX.Y.Z`. En su lugar salen las tres siguientes: patch, minor y major. Sin ningún tag, pregunta «¿Primera versión?», con `v0.1.0` y `v1.0.0`.

Al elegir una, pide confirmarla con otro clic: «¿Publicar vX.Y.Z? sí». Si hay tareas en Testing, lo avisa al lado, sin bloquear: «2 sin probar: 4, 47». A los 5 segundos, o con un clic en otro botón, vuelve a ser RELEASE.

Antes de publicar comprueba que existen `main` y `develop`, que estás en `develop` sin cambios sin commit, que `main` es antecesor de `develop` y que el tag no existe. Si algo falla, no hace nada y dice cómo arreglarlo.

Confirmada, en la SF sube la `version` y hace su commit en `develop`; en los demás proyectos no toca ningún archivo. Después pasa `develop` a `main` por fast-forward, crea el tag y hace push de `develop`, `main` y el tag. Al acabar, vuelve a mirar si hay que ACTUALIZAR.

### ACTUALIZAR

ACTUALIZAR pone al día el plugin `sf` instalado, con comandos y sin Claude, según la decisión [Botón ACTUALIZAR](decisiones/124-2026-10-29-boton-actualizar-el-plugin-sf-solo-cuando-hay-version-publicada-nueva.md). Solo sale cuando hay una versión publicada más nueva que la instalada.

La versión publicada es el tag `vX.Y.Z` más alto del repositorio del catálogo, en GitHub, leído con `git ls-remote`. La instalada es la de `sf@softwarefactory` en `installed_plugins.json`, en el scope de usuario o en el local o de proyecto de esta carpeta. El panel lo mira al empezar la sesión, cada 30 minutos y después de publicar con RELEASE. La primera vez tarda unos segundos, lo que tarde GitHub en responder.

El primer clic pide confirmarla: «¿Actualizar a vX.Y.Z? sí». A los 5 segundos, o con un clic en otro botón, vuelve a ser ACTUALIZAR.

Confirmado, primero refresca el catálogo con `claude plugin marketplace update softwarefactory`. Hace falta porque el botón ve la versión en GitHub, pero `claude plugin update` la busca en el clon local del catálogo, que solo se refresca al arrancar y con la actualización automática activada. Si el refresco falla, no actualiza y dice por qué.

Después lanza `claude plugin update sf@softwarefactory` en cada scope desactualizado y avisa: «Actualizado a vX.Y.Z: reinicia Claude Code». Los scopes que fallan siguen en el botón, con el error en el aviso.

Si Claude Code responde que ya tenía esa versión, el panel la anota en `installed_plugins.json` y avisa: «sf ya estaba en vX.Y.Z: anotado en el registro», sin pedir reiniciar. Si no puede anotarla, dice por qué.

El botón llega con la versión que lo trae. Un proyecto con una versión anterior se actualiza esa vez a mano, desde `/plugin` o con los dos comandos, y reinicia Claude Code.

## Por dentro

Lo que el mod hace sin que se vea: cuándo relee, qué pone en la sesión, qué controla, qué escribe y dónde está su código.

### Cuándo se actualiza

El mod relee `.sf/`, el registro de la SF, la rama activa y los subagentes en marcha en estos momentos:

- al empezar la sesión y, si no encuentra ni la SF ni un proyecto, otra vez a los 2 segundos;
- después de cada herramienta que puede escribir, Bash, PowerShell, Write y Edit, y del Agent, sin esperar al final del turno: así una tarea o un paso nuevos se ven al momento;
- al lanzar un subagente, para que su ⚙ salga al momento;
- al acabar cada turno;
- con `/sf`;
- tras cada orden desde el panel: los botones de las tareas, la E de un paso, «limpiar», la «→» y el «−» del registro, y los comandos `/paso`, `/split` y `/fusionar`.

Además, un latido cada minuto redibuja la duración de la sesión y relee solo los subagentes: así se va la ⚙ de uno que ha acabado. Las tareas que han entrado en `develop`, las de la R, salen de `git log`, que solo se lanza cuando cambia `develop`.

Reconoce el repositorio de la SF por `plugins/sf/.claude-plugin/plugin.json`.

### Identidad de la sesión

Al arrancar, el mod pone a la sesión el color del proyecto, con `/color`. También le pone el nombre del proyecto, con `/rename`; la tarea ya se ve en el panel.

Lo hace una vez, al entrar, y lo apunta en el estado del mod, así que `/reload-plugins` no repite los comandos. Solo los vuelve a lanzar si cambian el color o el nombre en `.sf/proyecto.json`. Si Claude Code no le deja lanzarlos, avisa una vez.

### Qué controla

Un proyecto por sesión. Antes de que Claude escriba un archivo con Write, Edit o NotebookEdit, el mod comprueba a qué proyecto pertenece: la carpeta con `.sf/proyecto.json`, o la fuente de la SF. Si es otro, bloquea la escritura y dice por qué. Lo que está fuera de cualquier proyecto, como los borradores o la memoria, pasa.

Un worktree de git es el proyecto de su repositorio. Los de los subagentes, en `<proyecto>/.claude/worktrees/<nombre>/`, se reconocen por su ruta, sin leer nada. Los demás, por su `.git`, un archivo que apunta a `<repo>/.git/worktrees/<n>`. Así un subagente escribe en su worktree, y una sesión abierta dentro del worktree escribe también en el proyecto.

Solo el principal escribe la cola. Si un subagente intenta escribir `.sf/peticiones.json`, el mod lo bloquea y le pide que pase al principal lo que haya que anotar. Lo sabe por el `agentId` de la llamada, que el principal no lleva.

Hay dos excepciones, ambas en la SF desde otro proyecto: registrar una mejora en `docs/propuestas.md` y anotar en el registro de uso, `.sf/registro.json`. Cuando Claude registra una mejora así, el mod lo avisa y la cuenta en la sesión.

Si el control falla, la escritura sigue: el control ayuda, la regla manda. Las órdenes de terminal no se controlan: para ellas vale la regla de la metodología (sección 2).

### Qué escribe

Llevar la cola y el estado es tarea de Claude. El panel escribe cuando se lo pides, y en la cola siempre con `cola.py`, que deja copia y lo apunta en el historial:

- `/paso` añade un paso a `.sf/peticiones.json` y la E de un paso lo quita; `/split` mueve pasos a una tarea nueva; `/fusionar` junta tareas en una y saca las demás de la cola;
- la T cambia de rama con git y pasa a en curso la tarea que estaba en cola;
- RELEASE sube la versión, pasa `develop` a `main`, crea el tag y hace push; ACTUALIZAR refresca el catálogo, actualiza el plugin y, si ya estaba en esa versión, la anota en `installed_plugins.json`;
- la C hace el squash, el commit y el push en `develop`, borra la rama y saca la tarea de la cola;
- la E quita la tarea de la cola;
- la D borra la rama y pasa la tarea a `descartada`;
- la R hace el revert en `develop`, sin push, y elimina la tarea o la devuelve a la cola;
- «limpiar» saca de la cola las descartadas;
- el «−» del registro borra la entrada de `.sf/registro.json` de la SF; la «→» la borra y añade la tarea a `.sf/peticiones.json`;
- la etiqueta de prueba cambia `.claude/settings.local.json`.

Y escribe solo, sin que se lo pidas:

- al abrir una sesión nueva, no con `/reload-plugins`, saca de la cola con `cola.py limpiar` las descartadas que quedaron de otra;
- al empezar y al cerrar la sesión, apaga el modo prueba en `.claude/settings.local.json`, apunta en `.sf/prueba.json` la sesión que ya lo apagó y, en la SF, anota en `.sf/prueba.log` cada arranque y cada cambio;
- al cargarse, copia su `cola.py` en `~/.claude/sf/cola-<sesión>.py` y borra las copias de más de 7 días;
- en la SF, apunta dónde está, en `~/.claude/sf/fuente.json`;
- guarda las secciones y tareas plegadas, para recordarlas entre sesiones.

### Dónde está el código

En `plugins/sf/hooks/`, repartido por módulos:

- `register.tsx` conecta los eventos y los comandos `/sf`, `/paso`, `/split` y `/fusionar`.
- `panel.tsx` dibuja el panel y la caja sobre el prompt.
- `lectura.ts` lee el proyecto, la cola con sus pasos, los documentos, el registro, las propuestas y la rama activa, de `.git/HEAD`, sin ejecutar git, y los subagentes en marcha. Las tareas que han entrado en `develop` salen de `git log`.
- `cola.ts` sigue la cola, lleva las cuentas de la sesión y atiende los botones y los comandos `/split` y `/fusionar`, con las órdenes de git que necesitan.
- `control.ts`, un proyecto por sesión.
- `identidad.ts`, el color y el nombre de la sesión.
- `prueba.ts`, el modo prueba.
- `estilo.ts`, los colores de las tareas y de las letras.
- `constantes.ts`, las rutas y los valores fijos.

Su registro es `plugins/sf/hooks/hooks.json`, y el tipo del estado que comparte con el panel, `plugins/sf/types/index.d.ts`.

El motor de mods exige dos cosas. Cada archivo declara los valores de estado que usa; con el mismo plugin y clave, son el mismo valor. Y una función que recibe `$` desde otro archivo es una declaración `function`, no una flecha.

Antes de publicar se comprueba con `claude plugin validate plugins/sf`, con la comprobación de tipos y con `claude plugin test plugins/sf`, que pasa las pruebas de `plugins/sf/tests/`.

## Con JKanban

JKanban será el kanban de la SF, con un MCP a medida, y aún no está incorporado: lo dice la decisión [JKanban, con un MCP a medida e instalado dentro de la SF](decisiones/010-2026-10-26-jkanban-con-un-mcp-a-medida-e-instalado-dentro-de-la-sf.md). Cuando lo esté, el tablero será la fuente del trabajo planificado y el panel, la ventana de la sesión. Esto cambia en el panel:

- **El estado viene del kanban.** El mod leerá la fase, la devslice y las tareas a través del MCP de JKanban. `.sf/estado.json` quedará como copia, para trabajar sin conexión.
- **La cola, al backlog.** Una petición pasa al backlog del proyecto solo si queda pendiente; las menores que se resuelven en el momento, no. `.sf/peticiones.json` quedará como copia de la cola.
- **Sección Planificado,** en el bloque Proyecto, con las tareas del plan.
- **Las mejoras de la SF, tareas del kanban.** Las propuestas de Mejoras pasarán a ser tareas del proyecto SoftwareFactory, junto a la tarea «Mejorar la Software Factory».

Los tres primeros puntos están decididos: [El panel, en dos bloques; con JKanban, Planificado](decisiones/041-2026-10-27-el-panel-en-dos-bloques-con-jkanban-planificado.md). Lo que sigue son propuestas pendientes de decisión:

- **De planificada a la cola** (propuesta P23). Una planificada sin empezar lleva «P», sin número. Al empezar, entra en la cola en curso con su número y la A, y en Planificado pasa de «P» a «63A»; el número de su tarjeta queda en el campo `kanban` de la petición. Si se aparca, vuelve a «P». Al cerrarse va a Testing y, con el OK del propietario, su tarjeta pasa a hecha y deja Planificado. Claude mueve la tarjeta con el MCP; mientras no esté conectado, no da ningún movimiento por hecho.
- **Estados del kanban** (propuesta P15): Planificada, En preparación, Preparada, En desarrollo, En verificación y Terminada. JKanban ya tiene flujos configurables; falta decidir los estados de la SF y sus transiciones.

Más adelante, el Claude Code Commander lanzará sobre Claude Code las tareas de un proyecto en JKanban, y el mod de cada sesión será su enlace: decisión [Claude Code Commander](decisiones/036-2026-10-27-claude-code-commander.md). Las propuestas sobre el mod se registran como cualquier otra mejora de la SF.

## Historial

Lo más reciente, arriba. «próxima» es lo que ya está en `develop` y aún no se ha publicado.

| Versión del plugin | Cambio |
| --- | --- |
| próxima | La etiqueta de la cabecera dice «SF» y la versión del plugin, en lugar del nombre del proyecto. |
| próxima | Los botones usan una copia de `cola.py` hecha al cargar el panel. |
| próxima | Registro del modo prueba en `.sf/prueba.log`, solo en la SF. |
| próxima | La R se parte en «R eliminar» y «R pendiente»: la revertida sale sin rastro o vuelve a Pendientes, reabierta. |
| próxima | El panel escribe la cola con `cola.py` y lee el historial: letras A y H, Cerradas y «falta el push»; en Testing, la R en lugar de la D. |
| próxima | En cada lista, la tarea que ha cambiado la última va arriba; la tarea principal es la en curso tocada la última. |
| próxima | Botón ACTUALIZAR, en rojo, en la cabecera: con una versión publicada más nueva, refresca el catálogo y actualiza el plugin. |
| próxima | `/redescribir N`: Claude propone una redacción más clara de la descripción y la guarda con tu OK. |
| próxima | Al fusionar, cada descripción en su párrafo; el panel pinta los párrafos aparte. |
| próxima | Control: los worktrees de los subagentes, en `.claude/worktrees/`, cuentan como el proyecto por su ruta. |
| 1.0.0 | Botón RELEASE, en violeta, en la cabecera: publica `develop` en `main` con su tag; los prompts pasan a la segunda fila. |
| 1.0.0 | La P pasa a T, de Test Mode: pone la tarea en prueba, sin darla por probada. |
| 1.0.0 | La C exige «Cerrar la tarea» y ningún otro paso pendiente salvo «Probar la tarea»; «Probar la tarea» lleva E y quitarlo es cerrar sin probar. |
| 1.0.0 | Arriba, todas las tareas en curso enteras, en varias líneas si hace falta, y el paso actual de cada una, también entero. |
| 1.0.0 | ⚙ en lugar de la P mientras un subagente trabaja en la tarea, leído de los subagentes en marcha y no de los worktrees; sin P, C, D ni E. |
| 1.0.0 | Cabecera en dos filas: los prompts y, a la derecha, TURBO, prueba y nombre; la duración y, a la derecha, la rama. TURBO pide a Claude lanzar con subagentes las tareas que no necesitan al propietario. |
| 1.0.0 | Si la C no puede cerrar, su prompt llega a Claude: se envía desde un temporizador, como el de la R. |
| 1.0.0 | La caja sobre el prompt dice «mejoras N». |
| 1.0.0 | Los pasos se quitan con una E de dos clics; «Probar la tarea» y «Cerrar la tarea», no. |
| 1.0.0 | La S separa pasos pendientes de una tarea sin Claude, como `/split`; «Probar» y «Cerrar» no cuentan. |
| 1.0.0 | La caja sobre el prompt sale salvo con el panel a la vista, colocado y al frente, y se vuelve a pintar al cerrarlo. |
| 1.0.0 | Documentos cuenta las decisiones de `docs/decisiones/`, una por archivo, sin su índice. |
| 1.0.0 | Si la C no puede cerrar una tarea, pasa a Claude el prompt para resolverlo. |
| 1.0.0 | Control: un worktree es el proyecto de su repositorio, y un subagente no puede escribir la cola. |
| 1.0.0 | Una fusión o una eliminación deshecha no es una reabierta: conserva su letra. |
| 1.0.0 | Botón R: revierte en `develop` una tarea cerrada; la revertida, con R en Cerradas. |
| 1.0.0 | La cabecera, sus dos primeras filas, queda fija al hacer scroll. |
| 1.0.0 | Botón C para cerrar una tarea; la D y la «→» del registro, con comandos y sin Claude. |
| 1.0.0 | `/fusionar` junta tareas en una, la de número más alto. |
| 1.0.0 | `/split` separa pasos de una tarea en una tarea nueva. |
| 1.0.0 | Botón P: activa con git la rama de una tarea para probarla. |
| 1.0.0 | Botones E de eliminar y D de descartar; la descartada, con D en Cerradas. |
| 1.0.0 | El botón de Cerradas pasa a llamarse «limpiar». |
| 1.0.0 | La cabecera, en etiquetas: la duración de la sesión tras los prompts y, en una segunda fila, la rama activa, en amarillo si es la de una tarea en curso o en Testing; al desplegar una tarea, «rama: …», con « (no existe)» si no está. |
| 1.0.0 | El código de una tarea en curso, en amarillo también dentro de las secciones. |
| 1.0.0 | Documentos: «Cómo funciona la Software Factory» en lugar de «Cómo funciona». |
| 1.0.0 | Eliminar una tarea sin rama desde el panel, con confirmación. |
| 0.34.3 | «Mejoras SF a valorar» pasa a «Mejoras». |
| 0.34.2 | Arriba, cada tarea con descripción se despliega para verla. |
| 0.34.1 | «?» en cada paso: pide a Claude que lo explique. |
| 0.34.0 | SF ENHANCE: el registro de uso, común a todos los proyectos; el mismo panel en todos los proyectos. |
| 0.33.2 | `/paso` avisa a Claude y pregunta la tarea; «−» quita un paso; cada tarea de arriba despliega los suyos. |
| 0.33.1 | Sin horas en Cerradas, y el amarillo solo en la tarea de arriba. |
| 0.33.0 | Avisa si el proyecto va por detrás de la SF. |
| 0.32.3 | Una tarea reabierta vuelve a Cerradas con H, en rojo. |
| 0.32.1 | El mod, repartido en módulos. |
| 0.32.0 | Pasos de una tarea: verlos y añadirlos con `/paso`. |
| 0.31.5 | Códigos de tarea más ligeros y un color por letra. |
| 0.31.4 | «Propuestas por decidir» pasa a «Mejoras SF a valorar». |
| 0.31.3 | Cerradas muestra todo cambio en el cierre de una tarea. |
| 0.31.2 | Cada fila de tarea se despliega por separado. |
| 0.31.1 | Cerradas se ve también con 0. |
| 0.31.0 | Modo prueba: etiqueta en el panel para cargar la copia de trabajo. |
| 0.30.9 | La tarea que se está probando, en curso. |
| 0.30.8 | Las probadas quitadas ya no vuelven al releer la cola. |
| 0.30.7 | La tarea en curso, con su código en todos los sitios. |
| 0.30.6 | Código de tarea: número y estado, «57-A». |
| 0.30.5 | Quitar las probadas, en la fila del título de Cerradas. |
| 0.30.4 | Cerradas: botón para quitar las probadas. |
| 0.30.3 | Subrayado en lugar de fondo negro en lo desplegable. |
| 0.30.2 | El código, en color y con fondo negro, en lugar del led y de ▸/▾. |
| 0.30.1 | Nombre de la sesión: el del proyecto, solo al entrar. |
| 0.30.0 | La letra es el estado: A, H, T y C; Sin probar pasa a Testing. |
| 0.29.10 | Letra y número con guion: «A-57». |
| 0.29.9 | Bloque TAREAS, con A y H. |
| 0.29.8 | Las tareas en curso, también en Pendientes. |
| 0.29.5 | En Sin probar, «✓» verde si Claude ya ha comprobado la tarea. |
| 0.29.4 | Propuestas numeradas: P01, P02… |
| 0.29.2 | Propuestas por decidir, desplegables con su resumen. |
| 0.29.0 | Sin SF, «Incorporarlo a la SF» propone pedírselo a Claude, con la skill de incorporación. |
| 0.28.7 | El nombre del proyecto, en la fila del marcador: no gasta una propia. |
| 0.28.6 | «En cola» pasa a «Pendientes», con el número en rojo. |
| 0.28.5 | Cerradas cuenta también las que no se vieron en curso; el marcador, solo con los prompts. |
| 0.28.4 | El nombre del proyecto, con los colores de la etiqueta de la sesión. |
| 0.28.3 | El nombre del proyecto, en mayúsculas. |
| 0.28.2 | El nombre del proyecto, a la derecha y atenuado, como los rótulos de los bloques. |
| 0.28.1 | Marcador con prompts, añadidas y propuestas; el número de Cerradas, en verde en su cabecera. |
| 0.28.0 | El marcador, fijo bajo el título del proyecto, fuera del bloque SESIÓN. |
| 0.27.9 | Tarea en curso en amarillo claro (#facc15), con grosor normal explícito. |
| 0.27.8 | El rótulo de cada bloque, en la fila de su primera sección. |
| 0.27.7 | Cerradas: las que no tienen texto guardado, juntas en una línea. |
| 0.27.6 | Cerradas: el led hace de viñeta, sin ▸ delante. |
| 0.27.5 | «Hecho en esta sesión» pasa a llamarse «Cerradas». |
| 0.27.4 | La tarea en curso más reciente, arriba; el nombre de la sesión también la usa. |
| 0.27.3 | La tarea en curso, toda en amarillo, número incluido, y sin negrita. |
| 0.27.2 | Hecho en esta sesión no pierde cierres con `/reload-plugins` y muestra también las hechas sin registro, con su número. |
| 0.27.1 | Todas las peticiones en curso arriba, una por línea; fuera «y N más en curso» y la sección También en curso. |
| 0.27.0 | Hecho en esta sesión: las peticiones cerradas, con led verde si tienen commit, en lugar de los commits de git. |
| 0.26.7 | Metodología: lo probado sale de Sin probar en el momento, sin pedir confirmación. |
| 0.26.6 | Hecho en esta sesión cuenta desde el inicio real de la sesión, no desde el último `/reload-plugins`. |
| 0.26.5 | En la SF, el título sin «fuente de la SF» debajo. |
| 0.26.4 | Fondo de los bloques algo más claro. |
| 0.26.3 | Rótulos SESIÓN y PROYECTO a la derecha; los dos bloques con el mismo fondo, separados por una fila con el del panel. |
| 0.26.2 | Cada bloque del panel con su fondo. |
| 0.26.1 | Fuera la sección En curso: la tarea ya está arriba; con varias, «También en curso» lista las demás. |
| 0.26.0 | Panel en dos bloques, Esta sesión y Proyecto; «Hecho en esta sesión» en lugar de los cinco últimos commits; Realimentación solo en la SF. |
| 0.25.2 | Documentos: también los de un solo archivo llevan su cantidad. |
| 0.25.1 | Lo último hecho: la antigüedad de cada commit, sin «hace». |
| 0.25.0 | Documentos: cada tipo con su cantidad. |
| 0.24.2 | La tarea en curso, sin `▶` delante: no hay nada que desplegar. |
| 0.24.1 | La tarea en curso, en amarillo en todos los proyectos. |
| 0.24.0 | Fuera el marcador de la última fila: las métricas quedan solo en la sección Sesión. |
| 0.23.1 | Marcador de la sesión compacto: dos líneas, la cifra delante de su etiqueta. |
| 0.23.0 | La sección Sesión, con estilo marcador: seis casillas en dos filas, cifra en color sobre su etiqueta. |
| 0.22.3 | El título de una petición o un commit desplegados, al partirse, vuelve a la izquierda. |
| 0.22.2 | Sangría del detalle de una petición, a 2. |
| 0.22.1 | El detalle de una petición desplegada, sin sangría colgante: «probar:» ocupa todo el ancho. |
| 0.22.0 | Sección Lo último hecho: los cinco últimos commits del proyecto, con su antigüedad. |
| 0.21.0 | El panel se relee a mitad de turno, tras cada herramienta que puede escribir: la tarea en curso se ve al momento. |
| 0.20.1 | La tarea en curso, en el color del proyecto. |
| 0.20.0 | Sección Sesión con las métricas de la sesión: prompts, tareas añadidas, terminadas, probadas, dejadas a medias y propuestas. |
| 0.19.1 | La tarea en curso, en el color de acento del tema y con una línea en blanco encima. |
| 0.19.0 | Arriba del panel, la tarea en la que se trabaja. |
| 0.18.0 | Al desplegar una petición, la cabecera muestra su texto entero sin repetirlo; el texto y «probar:» se parten alineados tras la marca. |
| 0.17.0 | Sangría en tres niveles; cada petición en una línea, con su detalle plegable. |
| 0.16.0 | Panel con secciones plegables y su cuenta en la cabecera; lo plegado se recuerda entre sesiones. |
| 0.15.0 | El mod pasa al panel lateral: en pantalla completa se abre solo y la caja sobre el prompt queda de reserva para cuando no hay panel. |
| 0.14.0 | Sin línea de estado: lo que mostraba ya está en la caja sobre el prompt. Si no puede poner el color o el nombre de la sesión, lo avisa. |
| 0.13.4 | Corrige el control de un proyecto por sesión, que bloqueaba las escrituras en el propio proyecto, y olvida lo visto al refrescar, para reconocer un proyecto incorporado en mitad de la sesión. |
| 0.13.3 | Al arrancar, el estado se lee cuando Claude Code ha terminado de arrancar, y se vuelve a mirar a los 2 s si no sale ni la SF ni un proyecto. |
| 0.13.2 | La ventana sobre el prompt se alinea a la derecha. |
| 0.13.0 | Marcador del día en la última fila: `+` por petición terminada, `−` por petición dejada a medias y `·` por propuesta añadida en la sesión; contador de prompts enviados en la sesión. |
| 0.12.0 | Identidad de la sesión: color del proyecto y nombre con la tarea principal, que se actualiza al cambiar de tarea. |
| 0.11.0 | Se presenta como una ventana pequeña sobre el prompt, siempre visible: estado, peticiones y realimentación. |
| 0.10.0 | Realimentación: cuenta las propuestas por revisar y sin pasar al kanban; avisa de las mejoras registradas desde otro proyecto. |
| 0.9.0 | Cola de peticiones: franja sobre el prompt y sección en el panel, a partir de `.sf/peticiones.json`. |
| 0.8.0 | Un proyecto por sesión: bloquea las escrituras de archivos en otro proyecto. |
| 0.7.6 | El panel muestra las guías de instalación y de actualización, y los documentos opcionales. |
| 0.7.0 | Lee la carpeta `.sf/` (`proyecto.json` y `estado.json`) y muestra el proyecto en el kanban; avisa si el estado sigue en `docs/sf.json`. |
| 0.5.0 | Reconoce el repositorio de la SF por la fuente del plugin. |
| 0.2.0 | Primera versión: línea de estado y panel `/sf`, a partir de `docs/sf.json`. |
