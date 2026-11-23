# Cómo funciona el panel

El panel de la SF, parte por parte: qué enseña, cómo se lee y qué se puede hacer desde él. El resumen está en [Cómo funciona la Software Factory](como-funciona-la-software-factory.html#el-panel-de-la-sf). Qué hace cada cambio de estado de una tarea, en [Cómo funcionan los estados](como-funcionan-los-estados.html). Las reglas que hay detrás están en la metodología y en las [decisiones](decisiones/README.md).

**Estado:** 5 de noviembre de 2026, plugin `sf` 1.8.2 y lo que hay en `develop` sin publicar (ver «Historial»).

## Qué es

El panel es el **mod de estado** del plugin `sf`. Un mod es la parte de un plugin que cambia la interfaz o el comportamiento de Claude Code: responde a eventos de la sesión y dibuja en un panel o sobre el prompt. Este mod es el centro de control de la SF dentro de Claude Code, y las nuevas responsabilidades de control se plantean primero en él.

Su objetivo es el **control y el foco**: ver de un vistazo qué se está haciendo, qué espera y qué te pide a ti, y actuar sobre ello sin escribir en el chat ni sacar a Claude de lo suyo.

Se ve de dos formas. En la pantalla completa de Claude Code, el panel se abre solo al empezar la sesión, a la derecha de la conversación. Si lo cierras a mano, no se vuelve a abrir solo: `/sf` lo reabre. Cuando el panel no está a la vista, el mod se enseña en una caja pequeña sobre el prompt (ver «La caja sobre el prompt»). Funciona igual en el terminal y en las superficies gráficas: la app de escritorio, VS Code y el móvil (ver «En la app de escritorio»).

Es el mismo en todos los proyectos, la SF incluida, sin adaptaciones. En una carpeta sin SF, en lugar de las tareas, da la bienvenida y ofrece incorporarla (ver «Una carpeta sin SF»).

Se lee de arriba abajo: la cabecera dice dónde estás; lo amarillo, qué se está haciendo; el bloque de tareas, todo lo demás.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 312" width="100%" role="img" aria-label="Esquema del panel: la cabecera con sus tres filas, dos tareas en curso en amarillo con el punto del subagente, y el bloque con Pendientes, En observación, Cerradas y Propuestas" style="font-family:var(--fuente-texto);display:block">
<rect x="8" y="4" width="334" height="304" rx="6" fill="none" stroke="#999" stroke-width="1.2"/>
<rect x="16" y="12" width="60" height="18" rx="3" fill="none" stroke="#9333ea" stroke-width="1.2"/>
<text x="46" y="25" text-anchor="middle" font-size="11" font-weight="700" fill="#7e22ce">RELEASE</text>
<rect x="80" y="12" width="60" height="18" rx="3" fill="none" stroke="#0e7490" stroke-width="1.2"/>
<text x="110" y="25" text-anchor="middle" font-size="11" font-weight="700" fill="#0e7490">TURBO</text>
<rect x="266" y="12" width="68" height="18" rx="3" fill="#827dbd"/>
<text x="300" y="25" text-anchor="middle" font-size="11" fill="#000">SF 1.8.2</text>
<rect x="16" y="36" width="60" height="18" rx="3" fill="none" stroke="#999" stroke-width="1"/>
<text x="46" y="49" text-anchor="middle" font-size="11" fill="#555">2h 05m</text>
<rect x="80" y="36" width="60" height="18" rx="3" fill="none" stroke="#999" stroke-width="1"/>
<text x="110" y="49" text-anchor="middle" font-size="11" fill="#555">12 prompts</text>
<rect x="16" y="60" width="200" height="18" rx="3" fill="none" stroke="#999" stroke-width="1"/>
<text x="22" y="73" font-size="11" fill="#a16207">feature/198-actualizar-como-funciona…</text>
<text x="16" y="104" font-size="11.5" fill="#a16207"><tspan text-decoration="underline">198</tspan> Actualizar Cómo funciona el panel (documentar)</text>
<text x="330" y="104" text-anchor="end" font-size="12" fill="#15803d">●</text>
<text x="16" y="124" font-size="11.5" fill="#a16207"><tspan text-decoration="underline">201</tspan> Que la caja diga la fase (corregir)</text>
<text x="330" y="124" text-anchor="end" font-size="12" fill="#b91c1c">●</text>
<rect x="12" y="140" width="326" height="164" rx="4" fill="none" stroke="#bbb" stroke-width="1"/>
<text x="20" y="162" font-size="11.5" font-weight="700" fill="#333">PENDIENTES ▾ <tspan font-weight="400" fill="#888">2</tspan></text>
<text x="20" y="182" font-size="11.5" fill="#666"><tspan text-decoration="underline"> 12</tspan> Ordenar la cola por sprint (diseñar)</text>
<text x="20" y="200" font-size="11.5" fill="#666"><tspan text-decoration="underline" fill="#fff" style="paint-order:stroke" stroke="#dc2626" stroke-width="7">205</tspan> Avisar del push que falta (corregir)</text>
<text x="20" y="226" font-size="11.5" font-weight="700" fill="#333">EN OBSERVACIÓN ▸ <tspan font-weight="400" fill="#888">1</tspan></text>
<text x="20" y="252" font-size="11.5" font-weight="700" fill="#333">CERRADAS ▸ <tspan font-weight="400" fill="#888">4</tspan></text>
<text x="20" y="278" font-size="11.5" font-weight="700" fill="#333">PROPUESTAS ▸ <tspan font-weight="400" fill="#888">3</tspan></text>
<line x1="342" y1="45" x2="350" y2="45" stroke="#f97316" stroke-width="1.5"/>
<circle cx="360" cy="45" r="10" fill="#f97316"/>
<text x="360" y="50" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
<text x="376" y="42" font-size="14" font-weight="700" fill="#004d47">Cabecera</text>
<text x="376" y="59" font-size="12.5" fill="#555">botones, sesión y rama; fija</text>
<line x1="342" y1="114" x2="350" y2="114" stroke="#f97316" stroke-width="1.5"/>
<circle cx="360" cy="114" r="10" fill="#f97316"/>
<text x="360" y="119" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">2</text>
<text x="376" y="111" font-size="14" font-weight="700" fill="#004d47">Tareas en curso</text>
<text x="376" y="128" font-size="12.5" fill="#555">en amarillo, con su subagente</text>
<line x1="342" y1="182" x2="350" y2="182" stroke="#f97316" stroke-width="1.5"/>
<circle cx="360" cy="182" r="10" fill="#f97316"/>
<text x="360" y="187" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">3</text>
<text x="376" y="179" font-size="14" font-weight="700" fill="#004d47">Pendientes</text>
<text x="376" y="196" font-size="12.5" fill="#555">en cola; la 205, reabierta</text>
<line x1="342" y1="222" x2="350" y2="222" stroke="#f97316" stroke-width="1.5"/>
<circle cx="360" cy="222" r="10" fill="#f97316"/>
<text x="360" y="227" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">4</text>
<text x="376" y="227" font-size="14" font-weight="700" fill="#004d47">En observación</text>
<line x1="342" y1="248" x2="350" y2="248" stroke="#f97316" stroke-width="1.5"/>
<circle cx="360" cy="248" r="10" fill="#f97316"/>
<text x="360" y="253" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">5</text>
<text x="376" y="253" font-size="14" font-weight="700" fill="#004d47">Cerradas en la sesión</text>
<line x1="342" y1="274" x2="350" y2="274" stroke="#f97316" stroke-width="1.5"/>
<circle cx="360" cy="274" r="10" fill="#f97316"/>
<text x="360" y="279" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">6</text>
<text x="376" y="279" font-size="14" font-weight="700" fill="#004d47">Propuestas por decidir</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">El panel en la SF, con dos tareas en curso y Pendientes desplegada. Es un esquema, no una captura.</figcaption>
</figure>

## La cabecera

La cabecera queda fija al hacer scroll: lo demás sube bajo ella con la rueda o las teclas, también las tareas en curso. Si cambia la lista de tareas, se cierra el panel o cabe entero, el cuerpo vuelve arriba. Lo que queda fuera de la vista se marca: arriba, «▲ N filas más · arriba», que vuelve arriba al pulsarlo; abajo, en el terminal, «▼ N filas más».

Tiene tres filas: los botones y la versión, la sesión y la rama.

<figure class="vertical" style="margin:1.6rem 0 1.4rem;">
<svg viewBox="0 0 560 520" width="100%" role="img" aria-label="Las tres filas de la cabecera, dibujadas, con sus partes numeradas: ACTUALIZAR, RELEASE, TURBO, prueba y versión; duración y prompts; rama" style="font-family:var(--fuente-texto);display:block">
<rect x="40" y="28" width="76" height="22" rx="3" fill="none" stroke="#b91c1c" stroke-width="1.2"/>
<text x="78" y="43" text-anchor="middle" font-size="12" font-weight="700" fill="#b91c1c">ACTUALIZAR</text>
<rect x="120" y="28" width="76" height="22" rx="3" fill="none" stroke="#7e22ce" stroke-width="1.2"/>
<text x="158" y="43" text-anchor="middle" font-size="12" font-weight="700" fill="#7e22ce">RELEASE</text>
<rect x="200" y="28" width="76" height="22" rx="3" fill="none" stroke="#0e7490" stroke-width="1.2"/>
<text x="238" y="43" text-anchor="middle" font-size="12" font-weight="700" fill="#0e7490">TURBO</text>
<rect x="280" y="28" width="76" height="22" rx="3" fill="none" stroke="#c2410c" stroke-width="1.2"/>
<text x="318" y="43" text-anchor="middle" font-size="12" fill="#c2410c">PRUEBA</text>
<rect x="458" y="28" width="76" height="22" rx="3" fill="#827dbd"/>
<text x="496" y="43" text-anchor="middle" font-size="12" fill="#000">SF 1.8.2</text>
<rect x="40" y="56" width="76" height="22" rx="3" fill="none" stroke="#999" stroke-width="1.2"/>
<text x="78" y="71" text-anchor="middle" font-size="12" fill="#555">2h 05m</text>
<rect x="120" y="56" width="76" height="22" rx="3" fill="none" stroke="#999" stroke-width="1.2"/>
<text x="158" y="71" text-anchor="middle" font-size="12" fill="#555">12 prompts</text>
<rect x="40" y="84" width="200" height="22" rx="3" fill="none" stroke="#999" stroke-width="1.2"/>
<text x="140" y="99" text-anchor="middle" font-size="12" fill="#a16207">feature/198-actualizar-…</text>
<line x1="78" y1="22" x2="78" y2="28" stroke="#f97316" stroke-width="1.5"/>
<circle cx="78" cy="12" r="10" fill="#f97316"/>
<text x="78" y="17" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
<line x1="158" y1="22" x2="158" y2="28" stroke="#f97316" stroke-width="1.5"/>
<circle cx="158" cy="12" r="10" fill="#f97316"/>
<text x="158" y="17" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">2</text>
<line x1="238" y1="22" x2="238" y2="28" stroke="#f97316" stroke-width="1.5"/>
<circle cx="238" cy="12" r="10" fill="#f97316"/>
<text x="238" y="17" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">3</text>
<line x1="318" y1="22" x2="318" y2="28" stroke="#f97316" stroke-width="1.5"/>
<circle cx="318" cy="12" r="10" fill="#f97316"/>
<text x="318" y="17" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">4</text>
<line x1="496" y1="22" x2="496" y2="28" stroke="#f97316" stroke-width="1.5"/>
<circle cx="496" cy="12" r="10" fill="#f97316"/>
<text x="496" y="17" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">5</text>
<line x1="30" y1="67" x2="40" y2="67" stroke="#f97316" stroke-width="1.5"/>
<circle cx="18" cy="67" r="10" fill="#f97316"/>
<text x="18" y="72" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">6</text>
<line x1="196" y1="67" x2="210" y2="67" stroke="#f97316" stroke-width="1.5"/>
<circle cx="220" cy="67" r="10" fill="#f97316"/>
<text x="220" y="72" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">7</text>
<line x1="240" y1="95" x2="254" y2="95" stroke="#f97316" stroke-width="1.5"/>
<circle cx="264" cy="95" r="10" fill="#f97316"/>
<text x="264" y="100" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">8</text>
<circle cx="14" cy="136" r="11" fill="#f97316"/>
<text x="14" y="141" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>
<text x="34" y="141" font-size="16" font-weight="700" fill="#004d47">ACTUALIZAR o REFRESCAR, en rojo</text>
<text x="34" y="161" font-size="15" fill="#555">con una versión nueva, o la sesión por detrás</text>
<circle cx="14" cy="184" r="11" fill="#f97316"/>
<text x="14" y="189" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">2</text>
<text x="34" y="189" font-size="16" font-weight="700" fill="#004d47">RELEASE, en violeta</text>
<text x="34" y="209" font-size="15" fill="#555">publica develop en main con su tag</text>
<circle cx="14" cy="232" r="11" fill="#f97316"/>
<text x="14" y="237" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">3</text>
<text x="34" y="237" font-size="16" font-weight="700" fill="#004d47">TURBO, en cian</text>
<text x="34" y="257" font-size="15" fill="#555">pide a Claude lanzar lo que no te necesita</text>
<circle cx="14" cy="280" r="11" fill="#f97316"/>
<text x="14" y="285" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">4</text>
<text x="34" y="285" font-size="16" font-weight="700" fill="#004d47">Etiqueta de prueba, solo en la SF</text>
<text x="34" y="305" font-size="15" fill="#555">«PRUEBA» en naranja: la copia de trabajo</text>
<circle cx="14" cy="328" r="11" fill="#f97316"/>
<text x="14" y="333" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">5</text>
<text x="34" y="333" font-size="16" font-weight="700" fill="#004d47">SF y la versión que corre</text>
<text x="34" y="353" font-size="15" fill="#555">con el color de la sesión; un clic, la próxima comprobación</text>
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
<text x="34" y="477" font-size="16" font-weight="700" fill="#004d47">Rama activa, sola en su fila</text>
<text x="34" y="497" font-size="15" fill="#555">en amarillo si es la de una tarea; «develop ↑2» si hay que subir</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">La cabecera en la SF, con una versión nueva por instalar, en modo prueba y en la rama de una tarea. Es un esquema, no una captura.</figcaption>
</figure>

La primera fila tiene los botones a la izquierda y la versión a la derecha. Los botones son ACTUALIZAR o REFRESCAR, RELEASE, TURBO y, solo en la SF, la etiqueta de prueba. En una carpeta sin SF no sale ninguno.

- **ACTUALIZAR**, en rojo, solo sale con una versión publicada del plugin más nueva que la instalada; **REFRESCAR**, en su sitio, cuando lo instalado está al día pero la sesión corre una versión más vieja (ver «ACTUALIZAR y REFRESCAR»).
- **RELEASE**, en violeta, publica: pasa `develop` a `main` con su tag (ver «RELEASE»).
- **TURBO**, en cian, pide a Claude que ponga en curso con subagentes las tareas que no te necesitan (ver «TURBO»).
- **La etiqueta de prueba** sale en la SF si el catálogo local está registrado. «PRUEBA», en naranja, dice que se usa la copia de trabajo; «prueba», subrayada y atenuada, que se usa el plugin publicado. Un clic cambia de uno a otro (ver «Modo prueba»).

A la derecha va **«SF» y la versión del plugin que corre**, por ejemplo «SF 1.8.2», con el color de la sesión de fondo y letra negra, como la etiqueta que pone Claude Code. Sin versión legible, dice «SF» a secas. Sale en todos los proyectos, también sin SF, porque el panel es del plugin. El color es el de la sesión, uno de los ocho de `/color` (ver «Identidad de la sesión»); sin color, la etiqueta va atenuada. Un clic avisa de cuánto falta para la próxima comprobación de versión y de la hora de la última. El nombre del proyecto no sale en el panel: lo lleva la sesión, con `/rename`.

En el terminal, las etiquetas de las dos primeras filas tienen **el mismo ancho**, el de « ACTUALIZAR », con el texto centrado. En un panel estrecho el ancho común se reduce, comiéndose el relleno; si ni así caben, cada una vuelve a su ancho. Las que piden confirmar, como «¿Publicar v1.9.0? sí», crecen lo que necesitan.

### La duración, los prompts y la rama

La segunda fila lleva la **duración** de la sesión, en horas y minutos («2h 05m», o «45m» si no llega a una hora), y los **prompts**: los mensajes que has enviado, sin los que añade Claude Code sin que se vean, con «1 prompt» en singular y la cifra atenuada con 0. Las dos cuentan desde que se abre la conversación, también tras un `/clear` o al reanudarla; `/reload-plugins` no las reinicia. La duración se redibuja cada minuto.

La tercera fila, solo en proyectos con SF y si hay `.git`, lleva la **rama activa** de la carpeta del proyecto, sola y a la izquierda. La letra va atenuada; en el amarillo de la tarea si es la rama de una tarea en curso o en observación. Con la cabeza separada, sale el commit corto entre paréntesis. Si no cabe, se recorta por el final con «…».

Con `develop` activa y commits sin subir a su remoto, la etiqueta dice **«develop ↑2»**, con la cifra en verde, y es un botón (ver «Subir develop»). El remoto es el de la configuración del proyecto, y la cuenta sale de la referencia remota que ya tiene git, sin ir a la red.

La rama se lee de `.git/HEAD`, sin ejecutar git; en un worktree, del `HEAD` al que apunta su `.git`. Se relee con la cola (ver «Cuándo se actualiza»).

### Los avisos

Los avisos van **en la cabecera**, en un bloque blanco de dos filas con la letra oscura, y se turnan con ella: la cabecera, 5 segundos; los avisos, 10. Así se ven siempre, sin scroll y sin quitar filas al cuerpo. Con varios, cada turno enseña uno, y el fondo alterna entre blanco y gris claro para que se note el cambio. Un clic en el aviso lo quita hasta su siguiente turno. Mientras un botón de la cabecera espera su segundo clic, la cabecera se queda.

Los avisos son estos:

- **No se puede leer** `.sf/proyecto.json` o `.sf/estado.json`, o la fase no es ninguna de las siete.
- **Ubicación antigua**: el proyecto aún tiene `docs/sf.json` y no `.sf/`.
- **Cola ilegible**: `.sf/peticiones.json` no se lee, o tiene tareas sin texto o con un estado desconocido, que no se enseñan.
- **Configuración**: un valor de `.sf/proyecto.json` que no se entiende, o el remoto que falta o no es de GitHub. Avisa sin bloquear.
- **REFRESCAR**: «Esta sesión usa la SF 1.8.1 y está instalada la 1.8.2: pulsa REFRESCAR».
- **Proyecto atrasado**: se incorporó con una SF anterior, comparando los dos primeros números, o su `CLAUDE.md` aún importa la copia vieja de las reglas, `.sf/claude-sf.md`. En los dos casos, pide a Claude «pon el proyecto al día con la SF».

Con una versión de RELEASE por confirmar, la fila de relleno de la cabecera avisa de las tareas que siguen en observación, sin bloquear: «2 en observación: 4, 47».

### Bajo la cabecera

Bajo la cabecera, y ya subiendo con el scroll, van el aviso de la pantalla completa (ver «Sin pantalla completa»), la línea del modo prueba y las tareas en curso.

La **línea del modo prueba** sale en la SF cuando lo pedido y lo cargado no coinciden. Es naranja y dice «/reload-plugins para entrar en el modo prueba» o «para salir del modo prueba».

La versión de la SF del proyecto, su fase y su devslice no salen en el panel lateral: solo en la primera línea de la caja sobre el prompt (decisión [La línea gris del proyecto sale del panel](decisiones/166-2026-11-01-la-linea-gris-del-proyecto-sale-del-panel.md)).

## Las tareas en curso

Lo amarillo es lo que se está haciendo: arriba, bajo la cabecera, van todas las tareas **en curso** y la de observación que estás mirando, la del campo `observando`, que se trabaja como si estuviera en curso. La que ha cambiado la última, la de fecha más reciente en su historial, va arriba: es la **tarea principal**. Las que no tienen historial van detrás, de número más alto a más bajo.

Cada tarea sale **en una sola sección**: las de arriba no se repiten en Pendientes ni en En observación.

Plegada, cada una es solo su línea: el número y el título, enteros y en amarillo, sin negrita, con el tipo detrás. A la derecha, el **●** de su subagente, si lo tiene (ver «El ● del subagente»). Desplegada, enseña su detalle, como en las secciones (ver «Cómo se lee una tarea»); arriba, además, la Prueba y la orden Paso +.

Sin tareas en curso, la parte amarilla enseña la devslice del proyecto, «devslice 2», o, sin ella, una línea atenuada: «▷ ninguna tarea en curso».

<figure class="vertical" style="margin:1.6rem 0 1.4rem;">
<svg viewBox="0 0 560 670" width="100%" role="img" aria-label="Una tarea en curso desplegada, con sus partes numeradas: título, menú de órdenes de la tarea y de sus pasos, rama, Prueba, Descripción, pasos numerados y el punto del subagente" style="font-family:var(--fuente-texto);display:block">
<text x="40" y="20" font-size="12.5" fill="#a16207"><tspan text-decoration="underline">198</tspan> Actualizar Cómo funciona el panel (documentar)</text>
<text x="516" y="20" font-size="14" fill="#15803d">●</text>
<rect x="40" y="30" width="80" height="20" rx="3" fill="none" stroke="#15803d" stroke-width="1.2"/>
<text x="80" y="44" text-anchor="middle" font-size="11.5" fill="#15803d">Activar rama</text>
<rect x="124" y="30" width="50" height="20" rx="3" fill="none" stroke="#15803d" stroke-width="1.2"/>
<text x="149" y="44" text-anchor="middle" font-size="11.5" fill="#15803d">Cerrar</text>
<rect x="178" y="30" width="92" height="20" rx="3" fill="none" stroke="#15803d" stroke-width="1.2"/>
<text x="224" y="44" text-anchor="middle" font-size="11.5" fill="#15803d">A observación</text>
<rect x="274" y="30" width="78" height="20" rx="3" fill="none" stroke="#15803d" stroke-width="1.2"/>
<text x="313" y="44" text-anchor="middle" font-size="11.5" fill="#15803d">Redescribir</text>
<rect x="356" y="30" width="22" height="20" rx="3" fill="none" stroke="#15803d" stroke-width="1.2"/>
<text x="367" y="44" text-anchor="middle" font-size="11.5" fill="#15803d">?</text>
<rect x="382" y="30" width="70" height="20" rx="3" fill="none" stroke="#b91c1c" stroke-width="1.2"/>
<text x="417" y="44" text-anchor="middle" font-size="11.5" fill="#b91c1c">Descartar</text>
<rect x="40" y="56" width="90" height="20" rx="3" fill="none" stroke="#999" stroke-width="1.2"/>
<text x="85" y="70" text-anchor="middle" font-size="11.5" fill="#777">Separar pasos</text>
<rect x="134" y="56" width="56" height="20" rx="3" fill="none" stroke="#999" stroke-width="1.2"/>
<text x="162" y="70" text-anchor="middle" font-size="11.5" fill="#777">Paso +</text>
<text x="40" y="98" font-size="12" fill="#888">Rama: feature/198-actualizar-como-funciona-panel</text>
<text x="40" y="120" font-size="12" fill="#888" text-decoration="underline">Prueba</text>
<text x="40" y="142" font-size="12" fill="#888" text-decoration="underline">Descripción</text>
<text x="68" y="160" font-size="12" fill="#666">Llevar al documento los cambios del panel.</text>
<text x="40" y="184" font-size="12" fill="#888"><tspan text-decoration="underline">Pasos</tspan> 1/4</text>
<text x="40" y="204" font-size="12" fill="#555"><tspan>  1</tspan> Leer la tarea <tspan fill="#15803d">?</tspan></text>
<text x="40" y="222" font-size="12" font-weight="700" fill="#777">  2<tspan font-weight="400"> Comprobarlo contra el código </tspan><tspan font-weight="400" fill="#15803d">?</tspan></text>
<text x="40" y="240" font-size="12" fill="#777">  3 Escribir el documento <tspan fill="#15803d">?</tspan> <tspan fill="#b91c1c">×</tspan></text>
<text x="40" y="258" font-size="12" fill="#777">  4 Cerrar la tarea <tspan fill="#15803d">?</tspan></text>
<line x1="21" y1="16" x2="38" y2="16" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="16" r="10" fill="#f97316"/>
<text x="11" y="21" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
<line x1="21" y1="40" x2="38" y2="40" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="40" r="10" fill="#f97316"/>
<text x="11" y="45" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">2</text>
<line x1="21" y1="66" x2="38" y2="66" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="66" r="10" fill="#f97316"/>
<text x="11" y="71" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">3</text>
<line x1="21" y1="94" x2="38" y2="94" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="94" r="10" fill="#f97316"/>
<text x="11" y="99" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">4</text>
<line x1="21" y1="116" x2="38" y2="116" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="116" r="10" fill="#f97316"/>
<text x="11" y="121" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">5</text>
<line x1="21" y1="146" x2="38" y2="146" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="146" r="10" fill="#f97316"/>
<text x="11" y="151" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">6</text>
<line x1="21" y1="222" x2="38" y2="222" stroke="#f97316" stroke-width="1.5"/>
<circle cx="11" cy="222" r="10" fill="#f97316"/>
<text x="11" y="227" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">7</text>
<line x1="530" y1="16" x2="539" y2="16" stroke="#f97316" stroke-width="1.5"/>
<circle cx="549" cy="16" r="10" fill="#f97316"/>
<text x="549" y="21" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">8</text>
<circle cx="14" cy="294" r="11" fill="#f97316"/>
<text x="14" y="299" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>
<text x="34" y="299" font-size="16" font-weight="700" fill="#004d47">Número, título y tipo</text>
<text x="34" y="319" font-size="15" fill="#555">en amarillo; el número subrayado la pliega</text>
<circle cx="14" cy="342" r="11" fill="#f97316"/>
<text x="14" y="347" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">2</text>
<text x="34" y="347" font-size="16" font-weight="700" fill="#004d47">Órdenes de la tarea</text>
<text x="34" y="367" font-size="15" fill="#555">en verde; la que destruye, en rojo y al final</text>
<circle cx="14" cy="390" r="11" fill="#f97316"/>
<text x="14" y="395" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">3</text>
<text x="34" y="395" font-size="16" font-weight="700" fill="#004d47">Órdenes de sus pasos</text>
<text x="34" y="415" font-size="15" fill="#555">en su fila, con la letra atenuada</text>
<circle cx="14" cy="438" r="11" fill="#f97316"/>
<text x="14" y="443" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">4</text>
<text x="34" y="443" font-size="16" font-weight="700" fill="#004d47">Rama y commit</text>
<text x="34" y="463" font-size="15" fill="#555">atenuados, en la columna del número</text>
<circle cx="14" cy="486" r="11" fill="#f97316"/>
<text x="14" y="491" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">5</text>
<text x="34" y="491" font-size="16" font-weight="700" fill="#004d47">Prueba</text>
<text x="34" y="511" font-size="15" fill="#555">qué mirar al probarla</text>
<circle cx="14" cy="534" r="11" fill="#f97316"/>
<text x="14" y="539" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">6</text>
<text x="34" y="539" font-size="16" font-weight="700" fill="#004d47">Descripción</text>
<text x="34" y="559" font-size="15" fill="#555">abierta de inicio, en la columna del título</text>
<circle cx="14" cy="582" r="11" fill="#f97316"/>
<text x="14" y="587" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">7</text>
<text x="34" y="587" font-size="16" font-weight="700" fill="#004d47">Pasos numerados</text>
<text x="34" y="607" font-size="15" fill="#555">el hecho, oscuro; el actual, en negrita; «?» y «×»</text>
<circle cx="14" cy="630" r="11" fill="#f97316"/>
<text x="14" y="635" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">8</text>
<text x="34" y="635" font-size="16" font-weight="700" fill="#004d47">● del subagente</text>
<text x="34" y="655" font-size="15" fill="#555">verde mientras trabaja, rojo mientras espera</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Una tarea en curso desplegada, con su menú, su rama, la prueba, la descripción y los pasos. Es un esquema, no una captura.</figcaption>
</figure>

## Cómo se lee una tarea

Todas las tareas tienen el mismo diseño en todas las secciones: arriba, en Pendientes, en En observación y en Cerradas.

### Número, título y tipo

El número va **sin letra detrás**, alineado a la derecha en tres columnas («  4», « 41», «236»), para que los títulos empiecen en la misma columna. Su color dice el estado: amarillo, en curso; verde, cerrada; gris, lo demás. Una tarea **reabierta** lleva el número con fondo rojo, en todas las secciones; es el único rojo de los números.

El título va entero, sin negrita y en un gris más apagado que el texto normal; si no cabe, sigue en la línea siguiente en su misma columna, con sangría colgante. Detrás va su **tipo**, entre paréntesis y en minúsculas: «(deliberar)». Sin tipo, nada.

### Desplegar una tarea

Toda tarea se despliega, porque toda tarea tiene al menos una orden, el «?». En el terminal, su número va subrayado y un clic en la línea la despliega o la pliega; en una superficie gráfica, lo hace el «▸» o «▾» del final de la fila. Plegada, solo su línea. Desplegada, debajo y por este orden:

1. el menú de órdenes: una fila con las de la tarea y, debajo, otra con las de sus pasos (ver «Actuar desde el panel»);
2. la rama, atenuada: «Rama: feature/95-rama-en-panel», con « (no existe)» si ya no está en el repositorio, y en la misma línea, tras « · », «Commit: …»;
3. **Prueba**, arriba y en En observación (ver «La prueba»);
4. **Descripción**, con el texto en la columna del título y cada párrafo aparte;
5. **Pasos**, con la cuenta (ver «Los pasos»).

Lo que la tarea no tiene, no sale. Prueba, Descripción y Pasos se pliegan cada uno por su cuenta y empiezan plegados, salvo la Descripción, que sale abierta mientras no toques ninguno de los tres. Lo plegado se recuerda entre sesiones, sección a sección y tarea a tarea.

### Los pasos

«Pasos 3/5», subrayado y atenuado, despliega la lista: la cuenta es hechos de todos, sin las ayudas de prueba. Los pasos van sin sangría, cada uno con su número sin punto, en tres columnas alineado a la derecha, y su texto con sangría colgante:

- **hecho**, en gris oscuro: ya no pide nada;
- **en curso**, con el número en negrita: es en lo que está Claude;
- **pendiente**, en un gris más claro que el de las tareas.

Cada paso lleva tras su última palabra un **«?»** verde, que pide a Claude que lo explique: qué es, qué se ha hecho y qué falta, sin hacerlo ni cambiar nada. El mensaje entra en el chat como si lo hubieras escrito tú. El «?» de los pasos de cierre explica además el flujo de una tarea a quien no conoce la SF: la rama, `develop`, En observación y qué conviene hacer ahora.

Los pendientes llevan además una **«×»** roja, que quita el paso de la tarea con dos clics: el primero la cambia por «¿Quitar? sí». Solo lo quita si en ese sitio sigue el mismo paso y sin empezar, porque Claude puede haber cambiado la cola entretanto. Los pasos de cierre, «Activar rama para poder probar» y «Cerrar la tarea», no la llevan: la tarea los tiene desde que entra en curso (decisión [Los pasos de cierre, desde que la tarea entra en curso](decisiones/174-2026-11-01-los-pasos-de-cierre-desde-que-la-tarea-entra-en-curso.md)).

Lo que Claude ha comprobado va como **paso hecho**, «Comprobado: 300 pruebas de Python, sin fallos», antes de los pasos de cierre; lo no comprobado, como tal: «No comprobado: …». No hay «✓» ni apartado aparte para ello (decisión [Las comprobaciones y pruebas hechas se anotan como pasos de su tarea](decisiones/288-2026-11-05-las-comprobaciones-y-pruebas-hechas-se-anotan-como-pasos-de-su-tarea.md)). Una cola antigua con el campo `comprobado` se lee igual: su texto sale como un paso hecho más.

Las **ayudas de prueba** van tras «Activar rama para poder probar», con «(opcional)» detrás: no se exigen para cerrar ni cuentan en la cuenta.

Los pasos los escribe Claude en `.sf/peticiones.json`, en el campo `pasos` de la tarea, con `cola.py`. Un paso sin texto o con un estado desconocido no se enseña.

### La prueba

**Prueba**, subrayada, dice cómo probar la tarea. Sale arriba, en las en curso y en la que miras, y en En observación, si la tarea tiene prueba. Desplegada, lleva un apartado, **Qué mirar**, con su rótulo atenuado: un punto por línea, con guion y sangría colgante. El texto separa los puntos con «;», y un contexto corto al principio («Tras publicar:») va antes, atenuado.

Lo que Claude ya ha comprobado no va en la Prueba, sino en los pasos (ver «Los pasos»). Ninguna comprobación de Claude saca la tarea de observación: solo tu OK la cierra.

### El ● del subagente

Mientras un subagente trabaja en una tarea, su línea lleva a la derecha un **●** verde; cuando ha entregado su informe y espera instrucciones, rojo, solo si la tarea sigue en curso. Parado, no lleva nada. Un clic avisa de cuál es: «⚙: un subagente trabaja en la 148 (Tarea 148: …)» o «el subagente de la 148 espera instrucciones». La marca es un ● y no una ⚙ porque algunos terminales pintan la ⚙ como emoji gris, sin el color.

El panel lo lee de los subagentes del motor, con `$.agent.list()`. Trabaja uno en `pending`, `running` o `waiting` cuya descripción empiece por «Tarea NN»; «Tarea 1480» no es la 148. Por eso el principal lanza cada subagente con la descripción «Tarea NN: …». Espera uno en `idle` o `completed`, o uno que se veía trabajando y ya no sale en la lista. Uno parado con `TaskStop` deja de contar al momento. Lo visto se apunta en la sesión y en `.sf/subagentes.json`, para no perderlo al cambiar de plugin. Los worktrees no cuentan.

Los subagentes se releen al lanzar uno, tras cada herramienta y cada minuto. El ● de uno que acaba cambia al momento o, como mucho, en un minuto.

## El bloque de tareas

Bajo las tareas en curso va **un solo bloque**, con un fondo gris algo más claro que el del panel y sin rótulo, con sus secciones en el orden del ciclo de una tarea: **Pendientes**, **En observación**, **Cerradas** y **Propuestas** (decisión [Las propuestas, en el bloque TAREAS; sin bloque PROYECTO](decisiones/197-2026-11-01-las-propuestas-en-el-bloque-tareas-sin-bloque-proyecto.md)).

Cada sección tiene una cabecera, sin sangría, con su nombre en mayúsculas y en negrita, «▾» si está abierta o «▸» si está plegada, y su cuenta, atenuada: «PENDIENTES ▾ 3». Un clic la pliega o la despliega; con el panel enfocado, también Tab y Enter. De inicio, En observación y Propuestas están plegadas. Pendientes, En observación y Cerradas se ven siempre, también con 0; Propuestas, solo si el proyecto tiene propuestas.

### Pendientes

Las tareas que esperan en cola, la que ha cambiado la última arriba. Las en curso no salen aquí: van arriba. La cuenta es su número, sin reparto.

### En observación

Las tareas que ya están en `develop` y se vigilan con el uso, para cerrarlas si van bien o revertirlas si van mal. La que estás mirando va arriba, no aquí. Su detalle lleva la Prueba.

### Cerradas

Las tareas con un cierre desde que se abrió o se reanudó la conversación, o desde el último `/clear`, lo último arriba. Salen del historial de cada tarea, que escribe `cola.py`: entra la que tiene en la sesión un evento de cierre (cerrada, a observación, descartada, revertida o reabierta) y ya ha salido de la cola, o sigue en ella descartada. Una que vuelve a observación, a Pendientes o se reabre sale en su sección, no aquí. Las eliminadas y las absorbidas por `/sf_fusionar` no entran, porque salen sin cerrarse. El texto y el commit de las que ya han salido de la cola se leen en `.sf/historial.jsonl`.

La cuenta es su número, atenuado con 0. El número de cada cerrada va en verde. Desplegada, una cerrada enseña sus órdenes, A observación y Revertir (ver «En Cerradas»), y «Commit: …». Si falló el push de `develop` al cerrarla, la línea dice «falta el push», y al final de la sección sale «falta el push de develop (N…)» hasta que el remoto tiene su commit.

Desplegada la sección, encima de la lista va **«Limpiar (N)»** (ver «En Cerradas»).

### Propuestas

Las propuestas del proyecto que esperan tu sí o no, de su `sf/propuestas.md` (o de `docs/propuestas.md` mientras el proyecto no se ha puesto al día): las del apartado «Propuestas pendientes» cuyo «Estado» dice «pendiente de aprobación» o «pendiente de decisión». Con otra rama activa, se leen de `develop`, donde se escriben. Cada proyecto ve las suyas; las de la SF, solo en la SF (decisión [Sin registro ni mejoras de la SF desde otros proyectos](decisiones/194-2026-11-01-sin-registro-ni-mejoras-de-la-sf-desde-otros-proyectos.md)).

Cada propuesta se lee como una tarea: su número fijo, P01, P02…, alineado a la derecha en una columna común y subrayado, y el título entero con sangría colgante. Desplegada, su resumen en la columna del título y la orden **A Pendientes** (ver «En Propuestas»). El resumen es la primera frase de su «Cambio propuesto» o, si no tiene, de su «Propuesta original» o del primer apartado con texto, cortada con «…» a los 220 caracteres.

## Actuar desde el panel

Desde el panel se cambian las tareas sin escribir en el chat: con su menú de órdenes, con el «?» y la «×» de los pasos, con los comandos y con los botones de la cabecera. Lo que se puede hacer con un comando lo hace el panel, sin Claude, según la decisión [Comandos antes que inferencia](decisiones/092-2026-10-29-comandos-antes-que-inferencia.md). Pasan por Claude el «?», Redescribir, Paso +, TURBO, `/sf_redescribir` y `/sf_config`, porque piden criterio, y los cierres que fallan, para que los resuelva.

Las órdenes escriben la cola con `cola.py --json --quien propietario --via panel`. No usan el `cola.py` del disco, sino una copia que el panel hace al cargarse, también con `/reload-plugins`, en `~/.claude/sf/cola-<sesión>.py` (o en la carpeta de `CLAUDE_CONFIG_DIR`, si está puesta). La copia lleva en su primera línea la raíz del plugin, donde busca sus módulos. Así el panel y el CLI son de la misma versión aunque una orden cambie la rama activa y, con ella, el `cola.py` del disco. Si la copia falla, usa el del disco y avisa una vez. Antes de pedir el cambio, el panel relee la cola y comprueba que la tarea sigue como la viste; si no, avisa y no toca nada.

Las órdenes que cierran, mueven o destruyen piden **dos clics**: el primero cambia la etiqueta por «¿Cerrar? sí», en su mismo color, y el segundo actúa. A los 5 segundos, o con un clic en otro botón del panel, vuelve a ser la etiqueta. Después, cada orden avisa en un aviso emergente de lo que ha hecho o de por qué no ha podido.

### Las órdenes de una tarea

Van en el menú de la tarea desplegada, como etiquetas con su nombre, con mayúscula inicial y sin negrita, sobre fondo negro (decisión [Las órdenes de cada tarea, en un menú de etiquetas](decisiones/168-2026-11-01-las-ordenes-de-cada-tarea-en-un-menu-de-etiquetas.md)). Las de la tarea, en verde, y la que destruye, en rojo y al final; las de los pasos, en su fila, con la letra atenuada. Si no caben en una fila, siguen en la siguiente. La línea plegada no lleva ninguna.

| Orden | Dónde sale | Clics | Qué hace |
| --- | --- | --- | --- |
| Activar rama | con rama que existe y no es la activa | uno | integra `develop` en la rama, la activa y abre los `.html` que cambia |
| Cerrar | en curso, con solo los pasos de cierre por hacer | dos | squash en `develop` y fuera de la cola |
| A observación | como Cerrar, salvo en las deliberativas | dos | el mismo squash, y queda en observación |
| Cerrar | en observación | dos | la saca de la cola: va bien |
| Redescribir | con descripción | uno | Claude propone una redacción más clara |
| ? | en todas | uno | Claude explica la tarea |
| A propuesta | en Pendientes, en cola y sin rama, con propuestas | dos | la devuelve a las propuestas |
| Eliminar | en cola o en curso, sin rama | dos | la quita de la cola sin rastro |
| Descartar | en cola o en curso, con rama | dos | borra la rama y la pasa a descartada |
| Revertir | en observación, con commits en `develop` | dos | revierte, y la elimina o la deja en Pendientes |
| Separar pasos | en cola o en curso, con dos pendientes o más | uno | abre el menú de `/sf_split` |
| Paso + | arriba | uno | deja `/sf_paso N ` en el prompt |

Eliminar y Descartar nunca van juntas, porque una tarea con rama no se elimina. Una tarea que ya entró en `develop` se revierte, no se descarta.

#### Activar rama

Pone la tarea en prueba activando su rama, sin darla por buena. Con un clic, `cola.py probar` integra antes `develop` en la rama (decisión [Activar rama integra develop y avisa a Claude si choca](decisiones/191-2026-11-01-activar-rama-integra-develop-y-avisa-a-claude-si-choca.md)) y la activa; si la tarea estaba en cola, la pasa a en curso. Después abre en el navegador los `.html` que la rama cambia respecto a `develop` y lo dice en el aviso. No recarga el plugin: si la rama lo necesita, `/reload-plugins` lo lanzas tú.

No cambia de rama si hay cambios sin commit o si la rama está en otro worktree; lo dice. Si la integración choca, o la rama auxiliar del subagente tiene commits sin traer, no la activa y le pasa a Claude el encargo de resolverlo, con la orden para repetirlo.

#### Cerrar y A observación

Salen en las tareas en curso que tienen «Cerrar la tarea» y ningún otro paso por hacer, salvo el de prueba y las ayudas. Con rama, la rama debe existir; sin rama también se cierran, sin squash ni commit (decisión [Cerrar desde el panel también sin rama](decisiones/188-2026-11-01-cerrar-desde-el-panel-tambien-sin-rama.md)). Pulsarlas es tu OK.

**Cerrar**, con `cola.py cerrar`, pasa a `develop` y hace el squash de la rama con su commit, «`<tarea> (N)`», con los pasos hechos en el cuerpo. Hace push de `develop`, borra la rama, recoge al subagente (su worktree y su rama auxiliar) y saca la tarea de la cola: entra en Cerradas. **A observación**, con `cola.py a-observacion`, hace lo mismo pero deja la tarea en observación. Las tareas deliberativas (investigar, deliberar y diseñar) no llevan A observación: no se prueban.

No hace nada si la rama está en otro worktree o hay cambios sin commit. Si el squash choca o falla el commit, `cola.py` lo deshace y vuelve a la rama de antes, sin tocar la cola, y el panel pasa a Claude el encargo de resolverlo. Si falla el push o no puede borrar la rama, cierra igual y avisa de lo que falta.

En observación, **Cerrar** saca la tarea de la cola, sin git: ya está en `develop`.

#### Redescribir, «?» y Paso +

**Redescribir** hace lo mismo que `/sf_redescribir N`. El **«?»** pide a Claude que explique la tarea, breve y sencilla: qué es, en qué punto está y qué espera de ti, sin cambiar nada. **Paso +** deja escrito en el prompt `/sf_paso N `, para que escribas el paso.

#### Separar pasos

Abre el menú de `/sf_split` con los pasos pendientes, cada uno con su número en la tarea, y separa sin Claude. Los pasos de cierre y las ayudas no cuentan. El menú admite cuatro opciones: con más pasos, en lugar de abrirlo, el aviso da la forma corta, `/sf_split N 2,3`, y la lista.

#### A propuesta

Devuelve a `sf/propuestas.md` una tarea en cola y sin rama, con `cola.py a-propuesta`: si salió de una propuesta, la vuelve a dejar «pendiente de aprobación»; si no, crea una con su título, su descripción y su tipo. La tarea sale de la cola. El cambio se hace con su propio commit en `develop`, aunque la rama activa sea otra. Solo en los proyectos que tienen propuestas.

#### Eliminar, Descartar y Revertir

**Eliminar**, con `cola.py eliminar`, quita de la cola una tarea en cola o en curso sin rama, que aún no ha cambiado nada: no entra en Cerradas, su número no se reutiliza y su historial queda en `.sf/historial.jsonl`. Si vuelve en la misma sesión, es la eliminación deshecha: vuelve a Pendientes con su número, no como reabierta.

**Descartar**, con `cola.py descartar`, sale en las tareas con rama, en cola o en curso. Si la rama es la activa, pasa antes a `develop`. Borra la rama y la del subagente, recoge su worktree y pasa la tarea a `descartada`, sin sacarla de la cola: sale al limpiar Cerradas. No hace nada si la rama está en otro worktree o es la activa con cambios sin commit; si git falla, no toca la cola.

**Revertir** sale en observación, en las tareas con commits en `develop`, y en Cerradas. Los commits salen del historial de la tarea o, sin él, de la historia de `develop`: los de primer padre con « (N)» al final del título o el trailer `SF-Tarea: N`; un «Revert …» posterior deja fuera los anteriores. Con el primer clic, Revertir pasa a «¿Revertir?» con dos etiquetas, **eliminar** y **a Pendientes**; a los 5 segundos, o con un clic en otro sitio, vuelve a ser Revertir. El segundo clic elige el destino: lanza `cola.py revertir N --eliminar` o `--pendiente`. Pasa a `develop`, hace `git revert` de sus commits, del más reciente al más antiguo, y se queda allí, sin push. Con «eliminar», la tarea sale sin rastro; con «a Pendientes», vuelve a la cola reabierta y sin rama. No hace nada si `develop` ha cambiado desde que se pintó, si hay cambios sin commit o si `develop` está en otro worktree. Si choca, lo deshace y se lo pasa a Claude.

#### Tras cerrar o descartar una tarea con subagente

El panel no puede parar a un subagente. Con tu siguiente mensaje, el aviso de lo cambiado desde el panel pide a Claude que lo detenga, y dice si `cola.py` ya quitó su worktree y su rama auxiliar o qué quedó por quitar (ver «Lo que el panel dice a Claude»).

### En Cerradas

Una cerrada desplegada lleva dos órdenes, con dos clics:

- **A observación**, en todas las cerradas: la devuelve a la cola, en observación, con su commit de `develop`, con `cola.py reobservar`. Es para la cerrada por error.
- **Revertir**, en las que tienen commits en `develop`, como en observación.

**«Limpiar (N)»**, con dos clics, saca de la lista las cerradas, las descartadas y las revertidas de antes, que ya no piden nada; las descartadas salen además de la cola, con `cola.py limpiar`. El panel recuerda cada limpiada con la fecha de su último cierre, así que vuelve si se reabre o se vuelve a cerrar. Sin ninguna que limpiar, no sale. Las descartadas que quedaron de otra sesión salen de la cola al empezar una sesión nueva, no con `/reload-plugins`.

### En Propuestas

**A Pendientes**, con dos clics, «¿A Pendientes? sí», pasa la propuesta a tarea en cola del proyecto, sin Claude, con `cola.py de-propuesta`: su título como texto, su resumen como descripción y su «Tipo», si es uno de los de la cola, como tipo. Su «Estado» pasa a «pasada a la tarea N de la cola el `<fecha>`», así que sale de la lista y no se pasa dos veces. El cambio de la propuesta va con su propio commit en `develop`, aunque la rama activa sea otra. Si en `develop` ya no está por decidir, o no puede hacer el commit, no crea la tarea y lo dice. El aviso dice «Tarea N en cola: …».

### Los comandos

Todos los comandos de la SF empiezan por `sf` (decisión [Los comandos de la SF empiezan por sf_](decisiones/198-2026-11-01-los-comandos-de-la-sf-empiezan-por-sf.md)). Los que no pasan por Claude funcionan también a mitad de turno.

- **`/sf`** abre el panel. Si ya está abierto, lo cierra y lo vuelve a abrir: así repara uno que se ha quedado en blanco. Además relee el estado y vuelve a comprobar si hay versión nueva. **`/sf:panel`** es la orden fija del plugin: la app la lista antes del primer mensaje, cuando el mod aún no corre; con el mod en marcha hace lo mismo que `/sf` y no sale en la lista. Si su texto le llega a Claude, el mod no está cargado: Claude lo dice y ofrece comprobar la instalación.
- **`/sf_paso texto`** añade un paso pendiente a la tarea en curso, antes de los pasos de cierre, y se lo pide a Claude, que lo hace sin esperar un «continúa». Con varias en curso, pregunta a cuál; `/sf_paso 64 texto` elige la 64. Sin ninguna, dice que se lo digas a Claude en el chat.
- **`/sf_split 89 2,3`** separa de la 89 sus pasos 2 y 3 en una tarea nueva, en cola y sin rama, con el número siguiente al último dado, que se llama como su primer paso. Solo de tareas en cola o en curso con dos pasos o más, y nunca todos. `/sf_split 89` pregunta los pasos y `/sf_split` a secas, antes, la tarea.
- **`/sf_fusionar 104 105`** junta tareas en cola o en curso en la de número más alto, con los pasos de todas por orden de tarea y las descripciones en párrafos. Si alguna estaba en curso, la que queda pasa a en curso. Las demás salen sin cerrarse. Con varias ramas, fusiona si las que sobran ya no existen o están integradas en la de destino, y las borra. Sin números, pregunta cuáles.
- **`/sf_redescribir 162`** pide a Claude que vuelva a redactar la descripción de la 162 para que se lea fácilmente, sin quitar ni añadir nada. Claude te enseña la propuesta y la guarda solo con tu OK.
- **`/sf_config [qué]`** pide a Claude cambiar la configuración del proyecto con menús y tu OK, con la skill `sf:configurar_proyecto`. En la SF o sin incorporar, lo dice y no pide nada.
- **`/sf_prueba`**, solo en la SF con el catálogo local, cambia el modo prueba sin el panel.
- **`/sf_forzar_activa`** trae la SF a esta sesión, y **`/sf_forzar_inactiva`** la apaga en ella (ver «Una sola sesión con la SF por proyecto»). Con la SF apagada en la sesión, son las únicas que se atienden.

Los menús de los comandos admiten cuatro opciones: con más tareas, salen las cuatro más recientes, y otra se escribe por su número en «Other».

### Modo prueba

En el repositorio de la SF, la etiqueta de prueba, o `/sf_prueba`, cambia entre el plugin publicado y la copia de trabajo, para ver un cambio sin commit ni publicación. Cambia `.claude/settings.local.json` y lanza `/reload-plugins`. Claude Code guarda la recarga hasta que la sesión queda libre: con Claude trabajando, el aviso dice que recarga al acabar su turno y que mientras sigue el panel de antes.

El modo prueba se apaga solo al empezar cada sesión, una vez por sesión: la marca queda en `.sf/prueba.json`, y un `/reload-plugins` posterior no lo vuelve a apagar. Si la sesión arrancó desde la copia de trabajo, lanza `/reload-plugins` para volver al publicado. Al cerrar la sesión, también se apaga. Cada arranque y cada cambio quedan en `.sf/prueba.log`, fuera de git.

Todo esto solo en el repositorio fuente de la SF. En otra carpeta con el catálogo local, como una carpeta de prueba, el mod no apaga el modo prueba ni escribe en `.sf/`: manda lo que diga su `.claude/settings.local.json`.

Cómo se prepara el catálogo local está en [Cómo funciona la Software Factory](como-funciona-la-software-factory.html#publicacion-del-plugin).

### TURBO

TURBO lanza de una vez el trabajo que no te necesita. Al pulsarlo, el panel avisa, «TURBO: se lo paso a Claude.», y le pasa este prompt como si lo escribieras tú:

> TURBO: pon en curso, cada una con su subagente, las tareas de la cola que se pueden hacer sin interactuar con el propietario; lanza también el subagente de las tareas en curso que aún no lo tienen, y avísame de cuáles.

Pasa por Claude porque decidir qué tareas no te necesitan es criterio, no un comando. Cada subagente que lance pone su ● en su tarea.

### RELEASE

RELEASE publica el proyecto: pasa `develop` a `main` y lo marca con el tag `vX.Y.Z`, con comandos y sin Claude. Sale en la SF y en todos los proyectos con SF.

El primer clic lee la versión actual, la del último tag `vX.Y.Z`, también en la SF (decisión [La versión forma parte del manejo del repositorio](decisiones/226-2026-11-02-la-version-forma-parte-del-manejo-del-repositorio.md)). En su lugar salen las tres siguientes: patch, minor y major. Sin ningún tag, pregunta «¿Primera versión?», con `v0.1.0` y `v1.0.0`. Al elegir una, pide confirmarla: «¿Publicar vX.Y.Z? sí». Si hay tareas en observación, lo avisa sin bloquear.

Antes de publicar comprueba que existen la rama de publicación (la `rama_main` de la configuración) y `develop`, que estás en `develop` sin cambios sin commit, que `main` es antecesor de `develop`, que el tag no existe y que la versión no ha cambiado. Si algo falla, no hace nada y dice cómo arreglarlo.

Después **revisa lo que sale**, con `revision_publica.py`, sin Claude: secretos, datos personales y archivos internos en los commits nuevos (decisión [Revisión antes de publicar](decisiones/259-2026-11-04-revision-antes-de-publicar-bloquear-en-publico-preguntar-en-privado-y-revisar-tambien-al-subir-develop.md)). Lo ya publicado en el último tag no cuenta, ni lo que el proyecto da por publicable en `.sf/publicable.txt`, una entrada por línea. Con el remoto público, algo nuevo para la publicación; lo ya subido, o cualquier cosa con el remoto privado, se enseña y se pide permiso: volver a pulsar RELEASE y elegir la misma versión en 10 minutos.

Confirmada, sube la versión de los manifiestos de la configuración (en la SF, `plugin.json`) en un commit en `develop`, «sf X.Y.Z» en la SF y «vX.Y.Z» en los demás, con la línea de coautoría si la hay. Un manifiesto sin versión o con otra se avisa sin bloquear. Pasa `develop` a `main` por fast-forward, crea el tag y hace push de `develop`, `main` y el tag al remoto de la configuración. Si el push falla, lo local queda hecho y lo dice. Al acabar, vuelve a mirar si hay que ACTUALIZAR.

### ACTUALIZAR y REFRESCAR

Son dos botones para dos casos, en el mismo sitio (decisión [ACTUALIZAR y REFRESCAR: dos botones para dos casos](decisiones/177-2026-11-01-actualizar-y-refrescar-dos-botones-para-dos-casos.md)).

**ACTUALIZAR** sale cuando hay una versión publicada más nueva que la instalada. La publicada es el tag `vX.Y.Z` más alto del repositorio del catálogo, en GitHub, leído con `git ls-remote`. La instalada es la de `sf@softwarefactory` en `installed_plugins.json`, en el scope de usuario o en el local o de proyecto de esta carpeta, si el plugin está activo en el proyecto. La publicada se mira al empezar la sesión, cada 5 minutos, con `/sf` y tras publicar con RELEASE; lo instalado frente a lo que corre, cada minuto, sin red.

Confirmado, «¿Actualizar a vX.Y.Z? sí», refresca el catálogo con `claude plugin marketplace update softwarefactory` y lanza `claude plugin update sf@softwarefactory` en cada scope desactualizado. Si el refresco falla, no actualiza. Después **instala las dependencias** que pide la versión nueva y faltan, con una orden `claude plugin install` por dependencia; sin ellas, `sf` no carga. Con `automatizaciones.dependencias_al_actualizar` apagado en `.sf/proyecto.json`, no las instala y avisa de cuáles faltan, con una orden por línea para instalarlas a mano.

Al acabar: con alguna dependencia nueva, «reinicia Claude Code»; sin ninguna, el botón pasa a REFRESCAR, que carga la versión sin reiniciar (decisión [La SF recarga sola los plugins en la incorporación; ACTUALIZAR recarga si basta](decisiones/286-2026-11-04-la-sf-recarga-sola-los-plugins-en-la-incorporacion-actualizar-recarga-si-basta-y-abandonar-lo-borra-todo.md)). Si Claude Code ya tenía esa versión, el panel la anota en `installed_plugins.json`.

**REFRESCAR** sale cuando lo instalado está al día pero la sesión corre una versión más vieja, por ejemplo porque otra sesión actualizó el plugin. Confirmado, instala las dependencias que falten y lanza `/reload-plugins`.

### Subir develop

Con `develop` activa y commits sin subir, la etiqueta de la rama, «develop ↑2», sube `develop` a su remoto. El primer clic avisa de que, si el repositorio es público, lo subido se ve al momento, y la etiqueta pasa a «¿Subir 2 a origin? sí»; el segundo lo sube sin Claude, con `cola.py subir`, que con el remoto público revisa antes lo que sale, como RELEASE. Si la revisión pide permiso, se da volviendo a pulsar la etiqueta.

### Los avisos emergentes

Todo lo que el panel dice en un aviso emergente se lee a primera vista: los avisos empiezan por un cuadrado azul, 🟦, y los errores por uno rojo, 🟥, porque el aviso emergente no admite fondo. Las rutas absolutas se abrevian a su último tramo, y la carpeta del worktree de un subagente, a «wt-256». Duran de 4 a 15 segundos según su largo, y los errores, al menos 8; un clic los quita. Cuando una orden falla, el aviso empieza por su nombre: «Activar rama: …».

## La caja sobre el prompt

Cuando el panel no está a la vista, el mod se enseña sobre el prompt, en una caja pequeña con borde redondeado, alineada a la derecha.

<figure class="vertical" style="margin:1.6rem 0 1.4rem;">
<svg viewBox="0 0 560 312" width="100%" role="img" aria-label="Caja sobre el prompt con sus partes numeradas: la línea del proyecto, las tareas en curso, las cuentas y cómo abrir el panel" style="font-family:var(--fuente-texto);display:block">
<rect x="150" y="4" width="404" height="96" rx="8" fill="none" stroke="#999" stroke-width="1.2"/>
<text x="162" y="26" font-size="12" font-weight="700" fill="#333">SF 1.7 → 1.8.2 · LecturaFàcil · 2/7 Especificación…</text>
<text x="162" y="46" font-size="12" fill="#333">▶ Exportar en UTF-8 con BOM</text>
<text x="162" y="66" font-size="12" fill="#888">en cola 3 · observación 1 · propuestas 2</text>
<text x="162" y="86" font-size="12" fill="#888">/sf abre el panel</text>
<line x1="140" y1="22" x2="150" y2="22" stroke="#f97316" stroke-width="1.5"/>
<circle cx="130" cy="22" r="10" fill="#f97316"/>
<text x="130" y="27" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
<line x1="112" y1="42" x2="150" y2="42" stroke="#f97316" stroke-width="1.5"/>
<circle cx="102" cy="42" r="10" fill="#f97316"/>
<text x="102" y="47" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">2</text>
<line x1="140" y1="62" x2="150" y2="62" stroke="#f97316" stroke-width="1.5"/>
<circle cx="130" cy="62" r="10" fill="#f97316"/>
<text x="130" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">3</text>
<line x1="112" y1="82" x2="150" y2="82" stroke="#f97316" stroke-width="1.5"/>
<circle cx="102" cy="82" r="10" fill="#f97316"/>
<text x="102" y="87" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">4</text>
<circle cx="14" cy="132" r="11" fill="#f97316"/>
<text x="14" y="137" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>
<text x="34" y="137" font-size="16" font-weight="700" fill="#004d47">Dónde estás, en negrita</text>
<text x="34" y="157" font-size="15" fill="#555">versión de la SF, proyecto, fase y devslice</text>
<circle cx="14" cy="180" r="11" fill="#f97316"/>
<text x="14" y="185" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">2</text>
<text x="34" y="185" font-size="16" font-weight="700" fill="#004d47">Tareas en curso</text>
<text x="34" y="205" font-size="15" fill="#555">con «▶», recortadas</text>
<circle cx="14" cy="228" r="11" fill="#f97316"/>
<text x="14" y="233" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">3</text>
<text x="34" y="233" font-size="16" font-weight="700" fill="#004d47">Cuentas</text>
<text x="34" y="253" font-size="15" fill="#555">solo las que no son cero, atenuadas</text>
<circle cx="14" cy="276" r="11" fill="#f97316"/>
<text x="14" y="281" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">4</text>
<text x="34" y="281" font-size="16" font-weight="700" fill="#004d47">Cómo abrir el panel</text>
<text x="34" y="301" font-size="15" fill="#555">«/sf abre el panel»</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">La caja de un proyecto atrasado, con una tarea en curso y el panel cerrado. Es un esquema, no una captura.</figcaption>
</figure>

La caja sale siempre, salvo con el panel a la vista: colocado y al frente. Así sale en la pantalla normal de Claude Code, en un terminal demasiado estrecho para el panel, con el panel cerrado a mano hasta que lo reabres con `/sf` y con el panel detrás de otra pestaña. Al cerrar el panel, la caja se vuelve a pintar en el momento. No sale mientras Claude Code enseña una encuesta, ni antes de la primera lectura del estado.

Su primera línea, en negrita, tiene una de estas formas:

| Situación | Primera línea |
| --- | --- |
| Proyecto bajo la SF | `SF 1.8 · LecturaFàcil · 2/7 Especificación e interfaz · devslice 2` |
| Proyecto atrasado | `SF 1.7 → 1.8.2 · LecturaFàcil · …` |
| Sin metodología | `SF 1.8 · LecturaFàcil` |
| Fase sin declarar | `SF 1.8 · LecturaFàcil · fase sin declarar` |
| Repositorio de la propia SF | `SF · repositorio de la SF` |
| Carpeta sin SF | `Sin SF` |
| Estado ilegible o fase desconocida | `SF 1.8 · LecturaFàcil · ⚠ revisar .sf/` |
| Estado aún en `docs/sf.json` | `… · ⚠ mover a .sf/` |

La versión es el campo `sf` de `.sf/proyecto.json`, la de la SF con que se incorporó el proyecto; «→» y la versión que corre salen solo si va por detrás en los dos primeros números. La «→» solo sale aquí: el panel lo dice en su aviso de proyecto atrasado.

Debajo, cada tarea en curso con «▶», recortada a 56 caracteres. Después, en una línea atenuada y solo lo que no es cero, «en cola N», «observación N» y «propuestas N». Los avisos van como en el panel, en blanco con la letra oscura: el de la pantalla completa, «revisar .sf/» o «revisar .sf/peticiones.json». Al final, «/sf abre el panel».

En una carpeta sin SF, la caja lleva a su izquierda el logo «/SF» pequeño y, en lugar de las cuentas, lo mismo que la bienvenida: qué es la SF, la orden para empezar como botón y que Claude no cambia nada sin tu OK.

## Una carpeta sin SF

En una carpeta sin `.sf/proyecto.json`, el panel no enseña tareas ni secciones: da la bienvenida y ofrece incorporar el proyecto. La cabecera solo lleva la versión, la duración y los prompts.

<figure class="vertical" style="margin:1.6rem 0 1.4rem;">
<svg viewBox="0 0 560 590" width="100%" role="img" aria-label="La bienvenida del panel en una carpeta sin SF y, debajo, la lista de la incorporación en curso, con sus partes numeradas" style="font-family:var(--fuente-texto);display:block">
<text x="250" y="52" text-anchor="middle" font-size="44" font-weight="900"><tspan fill="#b3aee6">/</tspan><tspan fill="#827dbd">SF</tspan></text>
<text x="250" y="80" text-anchor="middle" font-size="13" font-weight="700" fill="#827dbd" letter-spacing="3">SOFTWARE FACTORY</text>
<text x="250" y="102" text-anchor="middle" font-size="12" fill="#333">Tu fábrica de software sobre Claude Code:</text>
<text x="250" y="118" text-anchor="middle" font-size="12" fill="#333">de la idea al código, tarea a tarea.</text>
<text x="250" y="144" text-anchor="middle" font-size="12" font-weight="700" fill="#333">Para empezar, pulsa o escríbelo en el chat:</text>
<rect x="150" y="154" width="200" height="22" rx="3" fill="#827dbd"/>
<text x="250" y="169" text-anchor="middle" font-size="12" font-weight="700" fill="#000">incorpora este proyecto a la SF</text>
<text x="250" y="196" text-anchor="middle" font-size="11.5" fill="#888">Claude te hará unas pocas preguntas y no cambia nada sin tu OK.</text>
<rect x="60" y="214" width="380" height="146" rx="6" fill="none" stroke="#bbb" stroke-width="1"/>
<text x="72" y="236" font-size="12" font-weight="700" fill="#827dbd">INCORPORACIÓN</text>
<rect x="176" y="224" width="64" height="17" rx="2" fill="#827dbd"/>
<text x="208" y="236" text-anchor="middle" font-size="11" font-weight="700" fill="#000">En curso</text>
<text x="248" y="236" font-size="11.5" fill="#888">paso 3 de 12</text>
<text x="72" y="262" font-size="12" fill="#15803d">1.<tspan fill="#333"> Plugin</tspan> ✓</text>
<text x="90" y="278" font-size="11.5" fill="#666">Al día, 1.8.2</text>
<text x="72" y="298" font-size="12" fill="#15803d">2.<tspan fill="#333"> Caso</tspan> ✓</text>
<text x="90" y="314" font-size="11.5" fill="#666">Existente</text>
<text x="72" y="334" font-size="12" font-weight="700" fill="#827dbd">3. Diagnóstico ◂</text>
<text x="72" y="352" font-size="11.5" fill="#888">▼ 9 pasos más</text>
<line x1="360" y1="40" x2="452" y2="40" stroke="#f97316" stroke-width="1.5"/>
<circle cx="462" cy="40" r="10" fill="#f97316"/>
<text x="462" y="45" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">1</text>
<line x1="350" y1="165" x2="452" y2="165" stroke="#f97316" stroke-width="1.5"/>
<circle cx="462" cy="165" r="10" fill="#f97316"/>
<text x="462" y="170" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">2</text>
<line x1="440" y1="232" x2="452" y2="232" stroke="#f97316" stroke-width="1.5"/>
<circle cx="462" cy="232" r="10" fill="#f97316"/>
<text x="462" y="237" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">3</text>
<line x1="440" y1="330" x2="452" y2="330" stroke="#f97316" stroke-width="1.5"/>
<circle cx="462" cy="330" r="10" fill="#f97316"/>
<text x="462" y="335" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">4</text>
<circle cx="14" cy="394" r="11" fill="#f97316"/>
<text x="14" y="399" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>
<text x="34" y="399" font-size="16" font-weight="700" fill="#004d47">El logo «/SF»</text>
<text x="34" y="419" font-size="15" fill="#555">la barra en morado claro recuerda la orden /sf</text>
<circle cx="14" cy="442" r="11" fill="#f97316"/>
<text x="14" y="447" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">2</text>
<text x="34" y="447" font-size="16" font-weight="700" fill="#004d47">La orden, un botón</text>
<text x="34" y="467" font-size="15" fill="#555">se la pasa a Claude como si la escribieras tú</text>
<circle cx="14" cy="490" r="11" fill="#f97316"/>
<text x="14" y="495" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">3</text>
<text x="34" y="495" font-size="16" font-weight="700" fill="#004d47">Cabecera de la lista</text>
<text x="34" y="515" font-size="15" fill="#555">su estado como etiqueta y el paso en que va</text>
<circle cx="14" cy="538" r="11" fill="#f97316"/>
<text x="14" y="543" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">4</text>
<text x="34" y="543" font-size="16" font-weight="700" fill="#004d47">El paso actual</text>
<text x="34" y="563" font-size="15" fill="#555">en morado y negrita; los hechos, con «✓» y su respuesta</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">La bienvenida con una incorporación ya empezada: sin ella, la lista no sale. Durante la incorporación, la invitación a empezar se quita; aquí se ve para enseñar las dos partes juntas. Es un esquema, no una captura.</figcaption>
</figure>

### La bienvenida

La bienvenida dice lo único que hace falta para empezar, sin JSON, rutas ni contadores: la marca, qué es la SF en una frase y la orden. Arriba va el logo **«/SF»**: una barra pixelada en morado claro (`#b3aee6`) delante de «SF» en el morado de la SF (`#827dbd`), que recuerda la orden `/sf` (decisión [Logo /SF: barra estrecha y empinada en morado claro](decisiones/255-2026-11-04-logo-sf-barra-estrecha-y-empinada-en-morado-claro.md)). Si no caben sus 18 columnas, va sin la barra; con menos de 13, sin logo. Debajo, «SOFTWARE FACTORY», el lema, «Para empezar, pulsa o escríbelo en el chat:» y la orden **«incorpora este proyecto a la SF»**, en una pastilla morada que es un botón: se la pasa a Claude como si la escribieras tú. Cierra «Claude te hará unas pocas preguntas y no cambia nada sin tu OK.».

La marca va siempre en el morado de la SF, sin depender del color de la sesión.

### Ofrecer la incorporación

Sin SF, la línea del prompt sugiere la orden, en gris, para tomarla con Tab: al empezar la sesión, tras `/clear` y tras las órdenes locales del mod. Con tu primer mensaje de la conversación, Claude pregunta con un menú si quieres incorporar el proyecto, con tres opciones: «Sí, incorporarlo», «Ahora no» y «No, y no vuelvas a preguntar en esta carpeta». El mod guarda la tercera por carpeta y deja de sugerirlo y de preguntarlo allí (decisión [Si se dice que no a incorporar, se puede no volver a preguntar](decisiones/246-2026-11-02-si-se-dice-que-no-a-incorporar-se-puede-no-volver-a-preguntar.md)).

Tras incorporar la carpeta en la conversación, tu siguiente mensaje lleva a Claude las reglas de la SF y la orquestación, sin reiniciar, y, si falta, la oferta de activar la pantalla completa.

### La lista de la incorporación

Mientras Claude incorpora un proyecto, el panel enseña sus **pasos**, en una caja con el fondo de los bloques: debajo de la bienvenida, sin SF, o arriba del cuerpo en un proyecto que se pone al día. En un proyecto con SF, mientras la incorporación no ha terminado, la caja sale **en lugar del bloque de tareas**: el proyecto ya tiene `.sf/proyecto.json` desde Aplicar, pero aún le faltan pasos. Durante la incorporación, la bienvenida no lleva la invitación a empezar.

La lee de `~/.claude/sf/incorporacion-<carpeta>.json`, que escribe Claude con `incorporacion.py`: uno por proyecto, no por sesión, así que sobrevive a `/reload-plugins`, a `/clear`, al modo prueba y a una sesión nueva.

La cabecera de la caja dice «INCORPORACIÓN», en el morado de la marca, su estado como etiqueta y en qué paso va: «paso 3 de 12». Los estados son **En curso**, **En pausa**, **Recargando la SF** y **Terminada**. Cada paso lleva su número; el actual, en morado y negrita con «◂»; los hechos, con «✓» verde y su respuesta debajo; los que faltan, atenuados. Si no caben todos en el alto del panel, se pliegan los que sobran, con «▲ 2 pasos antes» y «▼ 5 pasos más» para moverse; la lista vuelve a seguir al paso actual en cuanto Claude avanza.

La incorporación queda **en pausa** cuando el turno de Claude acaba o se interrumpe con Esc, y al cargarse el mod; mientras corre un turno, también con un menú esperando tu respuesta, sigue en curso. En pausa, la lista se atenúa y salen dos botones: **«Continuar incorporación a la SF»**, que pasa a Claude «continúa la incorporación a la SF», y **«Abandonar incorporación a la SF»**, que lo borra todo, también lo guardado (decisión [Esc pone en pausa la incorporación, con Continuar y Abandonar en el panel](decisiones/258-2026-11-04-esc-pone-en-pausa-la-incorporacion-con-continuar-y-abandonar-en-el-panel.md)). Si respondes «Ahora no» o «No…» al menú de incorporar, el progreso se borra.

Cuando la incorporación necesita la versión instalada de la SF, más nueva que la que corre, Claude lo pide y, al acabar su turno, el mod recarga los plugins solo: la etiqueta dice **Recargando la SF** y, tras recargar, el mod le pasa a Claude «continúa la incorporación a la SF», sin que escribas nada.

Terminada, la lista se queda junto al panel nuevo hasta el siguiente turno, para que veas Aplicar y Comprobación marcados. Si no hay panel operativo, como en un diagnóstico sin SF, se queda con un botón, **«Hecho: cerrar la lista»**, que devuelve la bienvenida.

## Una sola sesión con la SF por proyecto

Solo una sesión de cada proyecto lleva la SF: el panel, la caja sobre el prompt, la cola, los subagentes y sus avisos, y las órdenes `/sf_*` (decisión [Una sola sesión con la SF por proyecto](decisiones/193-2026-11-01-una-sola-sesion-con-la-sf-por-proyecto.md)). Las demás sesiones del mismo proyecto arrancan con la SF **apagada**.

**El latido.** La sesión que tiene la SF deja un latido cada minuto en `~/.claude/sf/latido-<carpeta>.json`, con su id y la hora; está fuera del proyecto, así que no hay que ignorarlo en git. Al arrancar, y tras un `/clear`, una sesión toma la SF si no hay latido, si es suyo o si tiene 3 minutos o más: una sesión colgada o cerrada sin soltarlo no la retiene. Al cerrarse, la que la tiene suelta el latido, y la siguiente la toma al arrancar sin esperar.

**La sesión apagada** es Claude Code sin más: sin panel ni caja, sin control de un proyecto por sesión, sin la regla en el prompt de sistema, sin las reglas ni el contexto de la SF, y sin `/color` ni `/rename` (decisiones [Sin la SF activa no hay panel](decisiones/296-2026-11-05-sin-la-sf-activa-no-hay-panel-se-avisa-al-apagarla-porque-ya-hay-latido-en-el-proyecto.md) y [Una sesión con la SF apagada y /sf_forzar_inactiva dejan Claude Code sin más](decisiones/297-2026-11-05-una-sesion-con-la-sf-apagada-y-sf-forzar-inactiva-dejan-claude-code-sin-mas.md)). Al apagarse lo avisa una vez, en un aviso emergente y en una línea del historial que queda: «SF apagada en esta sesión: otra sesión de este proyecto la tiene activa, y aquí se trabaja sin la SF. Para traerla aquí, /sf_forzar_activa.» Las órdenes de la SF, también `/sf`, contestan en una línea que la SF está apagada aquí y cómo traerla. Ni ACTUALIZAR ni REFRESCAR se comprueban en ella, y no toca el modo prueba.

La apagada **no toma la SF sola**, ni aunque la otra deje de latir, ni tras un `/clear` o un `/reload-plugins`: si la otra deja de latir, lo avisa una vez, también a Claude, y propone `/sf_forzar_activa` (decisión [La sesión apagada avisa y propone /sf_forzar_activa](decisiones/295-2026-11-05-la-sesion-apagada-avisa-y-propone-sf-forzar-activa-cuando-la-activa-deja-de-latir-y-avisa-de-que-se-trabaja-sin-la-sf.md)).

**Las dos órdenes**, que no pasan por Claude:

- **`/sf_forzar_activa`** trae la SF a esta sesión aunque otra la tenga: escribe su latido, abre el panel, relee el estado, comprueba ACTUALIZAR y REFRESCAR, lanza `/color` y `/rename` y da a Claude las reglas y la orquestación si aún no las tiene. La otra se apaga en su siguiente latido, en un minuto como mucho, avisa «otra sesión de este proyecto la ha tomado con /sf_forzar_activa» y pide a Claude que deje las reglas de la SF.
- **`/sf_forzar_inactiva`** apaga la SF en esta sesión, que deja de dar latido y sigue como Claude Code sin más; otra la toma al arrancar. Queda apagada también tras un cambio de plugin, hasta `/sf_forzar_activa`.

En una carpeta sin SF nada de esto aplica.

## En la app de escritorio

En las superficies gráficas, la app de escritorio, VS Code y el móvil, el panel se ve y funciona como en el terminal, con lo que cambia su forma de dibujar. Allí el texto va en letra proporcional y cada botón es un botón nativo, que solo pinta su texto con la letra clara de la app:

- Cada botón va **lleno de su color**, como la etiqueta de la versión: un tono más oscuro que el de su letra en el terminal, para que la letra clara se lea. Los discretos, como Separar pasos y Paso +, en un gris apagado.
- El número y el título de una tarea van fuera del botón, como texto con su color; despliega un «▸» o «▾» al final de la fila. Plegado, el título se corta con «…».
- Las etiquetas de la cabecera toman el ancho de su texto y se parten en filas si no caben; la de la versión queda siempre a la derecha.
- El logo va en SVG, porque los caracteres de bloque se descuadran en su letra; el nombre, en grande.
- Los apartados y las secciones van más separados, y los bloques con fondo llevan un contorno tenue.
- El aviso de la cabecera va como texto, con una «×» que lo quita hasta su siguiente turno.

En la app, `/sf:panel` sale en la lista de órdenes desde antes del primer mensaje (decisión [En la app, /sf disponible antes del primer mensaje](decisiones/254-2026-11-04-en-la-app-sf-disponible-antes-del-primer-mensaje-y-solo-ordenes-al-escribir-sf.md)).

## Sin pantalla completa

Fuera de la pantalla completa del terminal, el panel y la caja se pintan en la conversación y **no reciben clics**. El motor lo dice en cada dibujo. Entonces el panel y la caja avisan arriba, en blanco: «Los botones necesitan la pantalla completa: pide a Claude que la active.» En el móvil, que tampoco está en pantalla completa, los toques sí llegan y no se avisa.

Con tu primer mensaje de la conversación, Claude recibe el encargo de ofrecerte activarla, una vez por conversación, con la causa que el mod puede leer: una variable de entorno que la quita, el ajuste `tui` ya puesto tras un arranque fallido, o nada. Con tu OK, la activa en `.claude/settings.local.json` del proyecto, nunca en `~/.claude` sin tu OK expreso. En una carpeta sin SF no se ofrece hasta incorporarla.

## Lo que el panel dice a Claude

El mod añade contexto a la conversación para que Claude no dependa de acordarse:

- **Las reglas y la orquestación**, en los proyectos incorporados y también en la SF (decisión [En la SF, las reglas y sf:orquestacion las entrega el mod, como en los demás proyectos](decisiones/298-2026-11-05-en-la-sf-las-reglas-y-sf-orquestacion-las-entrega-el-mod-como-en-los-demas-proyectos.md)), al empezar la sesión, tras `/clear` y tras compactar: las reglas comunes, las del método si el proyecto lo sigue, sus convenciones y la skill `sf:orquestacion` entera (decisión [El panel entrega las reglas y la orquestación en los proyectos](decisiones/187-2026-11-01-el-panel-entrega-las-reglas-y-la-orquestacion-en-los-proyectos.md)). Si el `CLAUDE.md` aún importa la copia vieja, `.sf/claude-sf.md`, no repite las reglas y el panel avisa. Con `automatizaciones.orquestacion` apagado, no entrega la orquestación.
- **Lo que es de la SF**, en cada petición, al final del prompt de sistema de los proyectos incorporados: lo que pinta el plugin y `~/.claude` no son del proyecto.
- **El intérprete de Python**, si no es `python`: la orden con que se lanza la cola en esta máquina.
- **Lo cambiado desde el panel.** Con cada mensaje tuyo, «Desde el panel: …», con lo que has cambiado en la cola desde el panel desde el mensaje anterior: «cerrada la 12; la 15, paso añadido: «…»». Sale de los eventos del historial con `via` panel. Va también tras cada encargo del panel a Claude. Sobrevive a `/reload-plugins`, también si cambia de plugin, sin repetirse ni perder nada; tras `/clear` o al reanudar una conversación, cuenta desde ahí, y nunca llega más atrás de 12 horas. Tras cerrar o descartar una tarea con subagente, pide detenerlo.
- **Los subagentes.** Con cada mensaje tuyo y al volver un subagente, «ANTES DE NADA…» pide lanzar el de cada tarea en curso que no tiene ninguno vivo, mientras falte; y avisa una vez de cada subagente que ha terminado sin recoger. Tras `/clear` o una compactación, lo pendiente se vuelve a avisar. Con `automatizaciones.avisos_subagentes` apagado, no avisa.
- **La incorporación**, en una carpeta sin SF, y **la pantalla completa**, como se dice arriba.
- **La sesión con la SF**: que se ha apagado aquí, porque otra la tomó o con `/sf_forzar_inactiva`, y que deje las reglas de la SF; que se ha activado con `/sf_forzar_activa`; o que la que la tenía ya no da latido. Con la SF apagada, nada más (ver «Una sola sesión con la SF por proyecto»).

Los encargos del panel a Claude («?», Paso +, TURBO, los cierres que fallan…) entran como si los escribieras tú. Tras interrumpir a Claude con Esc, Claude Code no los admite hasta que escribas algo: entonces el panel deja el encargo escrito en el prompt, si está vacío, para enviarlo con Intro, y lo dice.

## Por dentro

Lo que el mod hace sin que se vea: cuándo relee, qué pone en la sesión, qué controla, qué escribe y dónde está su código.

### Cuándo se actualiza

El mod relee `.sf/`, las propuestas, la rama activa y los subagentes en estos momentos:

- al empezar la sesión y, si no encuentra ni la SF ni un proyecto, otra vez a los 2 segundos;
- después de cada herramienta que puede escribir, Bash, PowerShell, Write y Edit, y del Agent, sin esperar al final del turno;
- al lanzar un subagente y al pararlo con TaskStop;
- al acabar cada turno;
- con `/sf`;
- tras cada orden desde el panel y cada comando.

Además, un latido cada minuto deja el de la sesión con la SF (ver «Una sola sesión con la SF por proyecto»), redibuja la duración, relee los subagentes, compara lo instalado con lo que corre y, cada 5 minutos, mira la versión publicada. Si el estado sigue sin leer, por ejemplo tras un `/clear`, lo lee: el panel no se queda en «Leyendo el estado…». Las tareas que han entrado en `develop` salen de `git log`, que solo se lanza cuando cambia `develop`.

Reconoce el repositorio de la SF por `plugins/sf/.claude-plugin/plugin.json`.

### Sesión, /clear y reanudar

Un `/clear` empieza una sesión nueva en el panel (decisión [Un /clear empieza una sesión nueva en el panel](decisiones/165-2026-11-01-un-clear-empieza-una-sesion-nueva-en-el-panel.md)): la duración, los prompts, Cerradas y los avisos cuentan desde ahí, salen las descartadas de antes y el mod vuelve a cargar el estado. Al reanudar una conversación, con `--continue`, `--resume` o `/resume`, la duración, los prompts, Cerradas y los avisos del panel cuentan desde que se reanuda. `/reload-plugins` no reinicia nada de esto.

### Identidad de la sesión

Al arrancar, el mod pone a la sesión el color del proyecto, con `/color`, y su nombre, con `/rename`. Lo hace una vez y lo apunta, así que `/reload-plugins` no repite los comandos; solo los vuelve a lanzar si cambian, al acabar el turno. Si Claude Code no le deja lanzarlos, avisa una vez.

El color sale del **primario del estilo del proyecto**, `colores.primario` de `docs/identidad/estilo.json`: el de los ocho de `/color` de tono más cercano, también el morado de la SF, que no se reserva (decisiones [El color de sesión se deriva del color primario del estilo del proyecto](decisiones/310-2026-11-05-el-color-de-sesion-se-deriva-del-color-primario-del-estilo-del-proyecto.md) y [El color de sesión de la SF no se reserva](decisiones/311-2026-11-05-el-color-de-sesion-de-la-sf-no-se-reserva-un-proyecto-puede-salir-del-mismo-color.md)). Sin estilo, con un primario gris o con uno que no se lee, es el campo `color` de `.sf/proyecto.json`; en la SF, el morado. Ni la incorporación ni `/sf_config` lo preguntan: se cambia con el estilo.

### Qué controla

Un proyecto por sesión. Antes de que Claude escriba un archivo con Write, Edit o NotebookEdit, el mod comprueba a qué proyecto pertenece: la carpeta con `.sf/proyecto.json`, o la fuente de la SF. Si es otro, también la SF desde otro proyecto, bloquea la escritura y dice por qué. Lo que está fuera de cualquier proyecto, como los borradores o la memoria, pasa.

Un worktree de git es el proyecto de su repositorio. Los de los subagentes, en `<proyecto>/.claude/worktrees/<nombre>/`, se reconocen por su ruta, sin leer nada; los demás, por su `.git`, un archivo que apunta a `<repo>/.git/worktrees/<n>`.

Un clon del mismo repositorio también es el mismo proyecto, se llame como se llame su carpeta: el mod compara el remoto `origin` de `.git/config` de los dos, sin protocolo, usuario ni `.git` final. Sin `origin`, o con otro, es otro proyecto.

Solo el principal escribe la cola. Si un subagente intenta escribir `.sf/peticiones.json`, el mod lo bloquea y le pide que pase al principal lo que haya que anotar.

Si el control falla, la escritura sigue: el control ayuda, la regla manda. Las órdenes de terminal no se controlan: para ellas vale la regla de la metodología.

### Qué escribe

Llevar la cola y el estado es tarea de Claude. El panel escribe cuando se lo pides, y en la cola siempre con `cola.py`, que deja copia y lo apunta en el historial:

- las órdenes de las tareas, los pasos y las propuestas, y los comandos `/sf_paso`, `/sf_split` y `/sf_fusionar`, como se dice en «Actuar desde el panel»; A propuesta y A Pendientes, con su commit en `develop`;
- RELEASE sube la versión, pasa `develop` a `main`, crea el tag y hace push; ACTUALIZAR refresca el catálogo, actualiza el plugin, instala dependencias y, si ya estaba en esa versión, la anota en `installed_plugins.json`; la etiqueta de `develop` hace su push;
- la etiqueta de prueba cambia `.claude/settings.local.json`;
- Abandonar y Hecho borran el progreso de la incorporación.

Y escribe solo, sin que se lo pidas:

- al abrir una sesión nueva, no con `/reload-plugins`, saca de la cola con `cola.py limpiar` las descartadas que quedaron de otra;
- en la SF, al empezar y al cerrar la sesión, apaga el modo prueba, apunta en `.sf/prueba.json` la sesión que ya lo apagó y anota en `.sf/prueba.log` cada arranque y cada cambio;
- al cargarse, copia su `cola.py` en `~/.claude/sf/cola-<sesión>.py` y borra las copias de más de 7 días, y copia el lanzador de Claude a `~/.claude/sf/cola.py` si ha cambiado; con `CLAUDE_CONFIG_DIR`, en su carpeta, para no tocar el `~/.claude` real;
- en `~/.claude/sf/latido-<carpeta>.json`, el latido de la sesión con la SF, cada minuto;
- en `.sf/subagentes.json`, lo que sabe de los subagentes de cada sesión: los de la última semana, hasta diez;
- en el progreso de la incorporación, la pausa y la recarga;
- guarda las secciones y tareas plegadas, para recordarlas entre sesiones, y las carpetas donde dijiste que no volviera a ofrecer incorporar.

### Dónde está el código

En `plugins/sf/hooks/`, repartido por módulos:

- `register.tsx` conecta los eventos y los comandos.
- `panel.tsx` dibuja el panel y la caja sobre el prompt.
- `lectura.ts` lee el proyecto, la cola con sus pasos, el historial, las propuestas, la incorporación, la rama activa de `.git/HEAD` y los subagentes. Las tareas que han entrado en `develop` y lo que falta por subir salen de git.
- `cola.ts` lanza `cola.py` y atiende las órdenes, RELEASE y ACTUALIZAR.
- `avisos.ts`, el aviso de lo cambiado desde el panel y los encargos a Claude; `subagentes.ts` y `memoria.ts`, los avisos de subagentes y lo que se guarda de ellos.
- `contexto.ts`, las reglas y la orquestación, la regla de lo que es de la SF, la oferta de incorporar y la pausa de la incorporación.
- `bienvenida.ts` y `logo.ts`, la bienvenida y el logo.
- `pantalla.ts`, el aviso y la oferta de la pantalla completa; `emergentes.ts`, los avisos emergentes.
- `latido.tsx`, una sola sesión con la SF por proyecto: el latido, la sesión apagada y `/sf_forzar_activa` e inactiva.
- `control.ts`, un proyecto por sesión; `identidad.ts`, el color y el nombre de la sesión; `prueba.ts`, el modo prueba; `revision.ts`, la revisión de RELEASE; `python.ts`, el intérprete; `configuracion.ts`, la configuración del proyecto.
- `estilo.ts`, los colores y anchos; `constantes.ts`, las rutas y los valores fijos.

Su registro es `plugins/sf/hooks/hooks.json`, y el tipo del estado que comparte con el panel, `plugins/sf/types/index.d.ts`.

El motor de mods exige dos cosas. Cada archivo declara los valores de estado que usa; con el mismo plugin y clave, son el mismo valor. Y una función que recibe `$` desde otro archivo es una declaración `function`, no una flecha.

Antes de publicar se comprueba con `claude plugin validate plugins/sf`, con la comprobación de tipos y con `claude plugin test plugins/sf`, que pasa las pruebas de `plugins/sf/tests/`.

## Con JKanban

JKanban será el kanban de la SF, con un MCP a medida, y aún no está incorporado: lo dice la decisión [JKanban, con un MCP a medida e instalado dentro de la SF](decisiones/010-2026-10-26-jkanban-con-un-mcp-a-medida-e-instalado-dentro-de-la-sf.md). El kanban se elige al incorporar y, por defecto, no hay ninguno. Cuando esté, el tablero será la fuente del trabajo planificado y el panel, la ventana de la sesión. Esto cambia en el panel:

- **El estado viene del kanban.** El mod leerá la fase, la devslice y las tareas a través del MCP de JKanban. `.sf/estado.json` quedará como copia, para trabajar sin conexión.
- **La cola, al backlog.** Una petición pasa al backlog del proyecto solo si queda pendiente; las menores que se resuelven en el momento, no. `.sf/peticiones.json` quedará como copia de la cola.
- **Sección Planificado,** con las tareas del plan.

Están decididos: [El panel, en dos bloques; con JKanban, Planificado](decisiones/041-2026-10-27-el-panel-en-dos-bloques-con-jkanban-planificado.md). Lo que sigue son propuestas pendientes de decisión:

- **De planificada a la cola** (propuesta P23). Una planificada sin empezar lleva «P», sin número. Al empezar, entra en la cola en curso con su número; el número de su tarjeta queda en el campo `kanban` de la petición. Si se aparca, vuelve a «P». Al cerrarse pasa a observación y, con el OK del propietario, su tarjeta pasa a hecha y deja Planificado. Claude mueve la tarjeta con el MCP; mientras no esté conectado, no da ningún movimiento por hecho.
- **Estados del kanban** (propuesta P15): Planificada, En preparación, Preparada, En desarrollo, En verificación y Terminada. JKanban ya tiene flujos configurables; falta decidir los estados de la SF y sus transiciones.

## Historial

Lo más reciente, arriba. «próxima» es lo que ya está en `develop`, o en camino, y aún no se ha publicado. La 1.7.0 es la primera versión pública, sin la historia de antes: lo que entró entre la 1.0.0 y la 1.7.0 va con ella.

| Versión del plugin | Cambio |
| --- | --- |
| próxima | Al cambiar la lista, cerrar el panel o caber entero, el cuerpo vuelve arriba; lo que queda fuera de la vista se marca con «▲ N filas más · arriba» y, en el terminal, «▼ N filas más». |
| próxima | El color de la sesión sale del primario del estilo del proyecto; sin estilo, el de `.sf/proyecto.json`. |
| 1.9.0 | Una sola sesión con la SF por proyecto: latido cada minuto, las demás arrancan con la SF apagada, sin panel ni caja, y `/sf_forzar_activa` y `/sf_forzar_inactiva`; en la SF, el mod entrega las reglas como en los demás proyectos. |
| 1.8.3 | Sin «✓» ni «Comprobado por Claude» en la Prueba: lo comprobado, como pasos hechos «Comprobado: …». |
| 1.8.3 | Reconoce como el mismo proyecto un clon con el mismo remoto origin, y el encargo de los subagentes pide no sortear un bloqueo. |
| 1.8.2 | En la app, los botones van llenos de su color, como la etiqueta de la versión. |
| 1.8.2 | Incorporación de corrido: la SF recarga sola los plugins («Recargando la SF») y sigue; con un menú abierto, «En curso»; en un proyecto con SF, la caja de la incorporación en lugar de las tareas hasta terminar; Abandonar lo borra todo. |
| 1.8.2 | ACTUALIZAR sin dependencias nuevas no pide reiniciar: pasa a REFRESCAR. |
| 1.8.1 | La etiqueta «develop ↑N» de la rama sube `develop` a su remoto, con dos clics y la revisión de lo que sale. |
| 1.8.1 | En la app: la caja de la incorporación legible, los apartados separados y «1 prompt» en singular. |
| 1.8.0 | La SF se ve y funciona en la app de escritorio como en el terminal: botones con contorno, número y título fuera del botón, ▸/▾ al final de la fila; `/sf:panel`, la orden fija. |
| 1.8.0 | La etiqueta de la versión dice la versión que corre; RELEASE publica en el repositorio público y revisa antes lo que sale, con `.sf/publicable.txt`. |
| 1.8.0 | La lista de la incorporación en el panel: pasos con su respuesta, plegados según el alto, el actual en morado, pausa con Continuar y Abandonar, Hecho y progreso por proyecto. |
| 1.8.0 | El logo de la bienvenida es «/SF», con la barra en morado claro. |
| 1.8.0 | Fuera del repositorio fuente de la SF, el mod no apaga el modo prueba ni escribe `.sf/prueba.json`. |
| 1.8.0 | Cerradas, la duración y lo cambiado desde el panel cuentan desde que se abre o se reanuda la conversación. |
| 1.7.6 | Bienvenida en el morado de la SF, con la caja sobre el prompt informativa, la orden sugerida en el prompt y el botón de incorporar. |
| 1.7.5 | Panel legible en la app de escritorio: logo en SVG, botones y textos adaptados; la copia de `cola.py` lleva la raíz del plugin en su primera línea. |
| 1.7.4 | En una carpeta sin SF, Claude ofrece incorporarla con un menú; tras incorporar, las reglas llegan sin reiniciar y se ofrece la pantalla completa. |
| 1.7.3 | Bienvenida en el panel de una carpeta sin SF, sin JSON, en lugar de «Incorporarlo a la SF». |
| 1.7.0 | Sin pantalla completa, el panel y la caja avisan de que los botones no responden, y Claude ofrece activarla. |
| 1.7.0 | Avisos emergentes legibles: 🟦 avisos, 🟥 errores, rutas abreviadas. |
| 1.7.0 | Avisos de subagentes en el contexto de Claude: los que faltan por lanzar y los terminados sin recoger, también tras cambiar de plugin. |
| 1.7.0 | «Desde el panel: …»: Claude recibe con cada mensaje lo cambiado desde el panel; sobrevive a `/reload-plugins`. |
| 1.7.0 | Testing pasa a «En observación»; la O del menú: A observación y Cerrar en observación; A observación en las cerradas. |
| 1.7.0 | «Prueba», desplegable, con «Comprobado por Claude» y «Qué mirar»; «Rama: … · Commit: …» en una línea. |
| 1.7.0 | Las órdenes de cada tarea, en un menú de etiquetas al desplegarla; la E de los pasos pasa a «×»; «?» en cada tarea; A propuesta. |
| 1.7.0 | Activar rama, antes la T: integra `develop` y abre en el navegador los `.html` que cambia la tarea. |
| 1.7.0 | Cerrar también sin rama; cierre y descarte recogen el worktree y la rama auxiliar del subagente. |
| 1.7.0 | ACTUALIZAR cada 5 minutos y con `/sf`, instala las dependencias, una orden por plugin; REFRESCAR cuando la sesión corre una versión más vieja que la instalada. |
| 1.7.0 | Los avisos, en la cabecera con fondo blanco, turnándose con ella; la línea gris del proyecto sale del panel. |
| 1.7.0 | Cabecera en tres filas, con las etiquetas del mismo ancho y la rama sola en la tercera; un clic en la versión dice cuándo es la próxima comprobación. |
| 1.7.0 | El ● del subagente, verde mientras trabaja y rojo mientras espera, en lugar de la ⚙. |
| 1.7.0 | Un solo bloque de tareas, con Propuestas, que leen el `sf/propuestas.md` del proyecto y pasan a tarea con A Pendientes; fuera SF ENHANCE, el Registro y Documentos. |
| 1.7.0 | Los comandos empiezan por `sf_`: `/sf_paso`, `/sf_split`, `/sf_fusionar`, `/sf_redescribir`, `/sf_config` y `/sf_prueba`; `/sf` reabre un panel en blanco. |
| 1.7.0 | Tras un `/clear`, sesión nueva en el panel, que ya no se queda en «Leyendo el estado…». |
| 1.7.0 | El panel entrega las reglas y la orquestación en los proyectos, y avisa de la copia vieja de las reglas. |
| 1.7.0 | Respeta `CLAUDE_CONFIG_DIR` para las copias de `cola.py` y el lanzador. |
| 1.7.0 | Las tareas, sin letras: el número, en tres columnas, da el estado con su color; las reabiertas, con fondo rojo; cada tarea en una sola sección; Pendientes y En observación, también con 0. |
| 1.7.0 | Tareas: plegadas, solo el título, con sangría colgante y su tipo; desplegadas, menú, rama, Prueba, Descripción y Pasos; secciones en mayúsculas con ▸/▾. |
| 1.7.0 | Pasos numerados en tres columnas, en lugar de marcas; ayudas de prueba opcionales; los pasos de cierre, desde que la tarea entra en curso; una columna libre a la derecha. |
| 1.7.0 | `/sf_fusionar` admite ramas ya integradas en la de destino o inexistentes. |
| 1.7.0 | La etiqueta de la cabecera dice «SF» y la versión del plugin, en lugar del nombre del proyecto. |
| 1.7.0 | Los botones usan una copia de `cola.py` hecha al cargar el panel. |
| 1.7.0 | Registro del modo prueba en `.sf/prueba.log`, solo en la SF. |
| 1.7.0 | La R se parte en «R eliminar» y «R pendiente»: la revertida sale sin rastro o vuelve a Pendientes, reabierta. |
| 1.7.0 | El panel escribe la cola con `cola.py` y lee el historial: letras A y H, Cerradas y «falta el push»; en Testing, la R en lugar de la D. |
| 1.7.0 | En cada lista, la tarea que ha cambiado la última va arriba; la tarea principal es la en curso tocada la última. |
| 1.7.0 | Botón ACTUALIZAR, en rojo, en la cabecera: con una versión publicada más nueva, refresca el catálogo y actualiza el plugin. |
| 1.7.0 | `/redescribir N`: Claude propone una redacción más clara de la descripción y la guarda con tu OK. |
| 1.7.0 | Al fusionar, cada descripción en su párrafo; el panel pinta los párrafos aparte. |
| 1.7.0 | Control: los worktrees de los subagentes, en `.claude/worktrees/`, cuentan como el proyecto por su ruta. |
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
