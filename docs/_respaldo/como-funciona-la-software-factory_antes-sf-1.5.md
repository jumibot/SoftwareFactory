# Cómo funciona la Software Factory

Este documento describe el funcionamiento de la Software Factory: sus componentes, dónde está cada uno y cómo se relacionan. No contiene reglas. Las reglas están en la metodología, en la especificación y en las decisiones, y aquí solo se dice dónde buscarlas.

**Estado:** 28 de octubre de 2026, plugin `sf` 0.34.3.

## La SF es un plugin

Un **plugin de Claude Code** es un paquete que amplía Claude Code con piezas que se instalan juntas: skills, comandos con barra, agentes, hooks, servidores MCP y mods de la interfaz, como la línea de estado. Se publica por versiones y se instala entero, para un proyecto o para el usuario.

La SF se escribe en un solo sitio, este repositorio, y llega a los proyectos de una sola forma: el plugin `sf` de Claude Code. Lo que contiene el plugin (la metodología, las skills, las plantillas, el kit de documentos y el mod de estado) se publica y se instala una vez, para el usuario. Desde ese momento está en todas las sesiones, en cualquier proyecto, con el prefijo `sf:`.

Cada proyecto pone solo lo suyo: la carpeta `.sf/`, que lo identifica y guarda su estado (fase y devslice en curso, que el panel lateral de la SF muestra al momento), y `docs/decisiones/`, con lo que el propietario ha decidido, una decisión por archivo. Las tareas viven en JKanban.

El circuito se cierra al revés: lo que falla o falta en un proyecto vuelve a la SF como propuesta. Solo cuando el propietario la aprueba se aplica en la fuente y se publica una versión nueva.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 44 560 556" width="100%" role="img" aria-label="Mapa de la SF: de la fuente a los proyectos, pasando por la versión publicada y la copia instalada, y la vuelta de las mejoras" style="font-family:var(--fuente-texto);display:block">
<defs><marker id="flecha-cf-fra" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#be185d"/></marker><marker id="flecha-cf" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#00726b"/></marker></defs>
<rect x="14" y="54" width="500" height="178" rx="10" fill="none" stroke="#b2deda" stroke-width="1.5"/>
<path d="M30,66 v18 a10,4 0 0 0 20,0 v-18" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/><ellipse cx="40" cy="66" rx="10" ry="4" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<text x="62" y="74" font-size="14.5" font-weight="700" fill="#004d47">1 · Fuente: el repositorio de la SF</text>
<text x="62" y="92" font-size="12.5" fill="#555">D:\Projectes\SoftwareFactory · aquí se edita todo</text>
<text x="34" y="124" font-size="12.5" font-weight="700" fill="#00726b">Contenido del plugin sf</text>
<text x="34" y="144" font-size="12.5" fill="#555">metodología (sf:metodologia)</text>
<text x="34" y="162" font-size="12.5" fill="#555">skills de cada fase y de apoyo</text>
<text x="34" y="180" font-size="12.5" fill="#555">plantillas de estructuras</text>
<text x="34" y="198" font-size="12.5" fill="#555">kit de documentos HTML</text>
<text x="34" y="216" font-size="12.5" fill="#555">mod de estado: línea y /sf</text>
<text x="290" y="124" font-size="12.5" font-weight="700" fill="#004d47">Se queda en el repositorio</text>
<text x="290" y="144" font-size="12.5" fill="#555">especificación</text>
<text x="290" y="162" font-size="12.5" fill="#555">visiones</text>
<text x="290" y="180" font-size="12.5" fill="#555">decisiones</text>
<text x="290" y="198" font-size="12.5" font-weight="700" fill="#be185d">propuestas</text>
<text x="290" y="216" font-size="12.5" fill="#555">investigación</text>
<line x1="264" y1="232" x2="264" y2="262" stroke="#00726b" stroke-width="2" marker-end="url(#flecha-cf)"/>
<text x="276" y="252" font-size="12" fill="#00726b">publicar: a main, con tag</text>
<rect x="14" y="266" width="500" height="54" rx="10" fill="none" stroke="#b2deda" stroke-width="1.5"/>
<path d="M30,278 v18 a10,4 0 0 0 20,0 v-18" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/><ellipse cx="40" cy="278" rx="10" ry="4" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<text x="62" y="288" font-size="14.5" font-weight="700" fill="#004d47">2 · Versión publicada</text>
<text x="62" y="306" font-size="12.5" fill="#555">cada versión del plugin, numerada</text>
<line x1="264" y1="320" x2="264" y2="350" stroke="#00726b" stroke-width="2" marker-end="url(#flecha-cf)"/>
<text x="276" y="340" font-size="12" fill="#00726b">actualización del plugin</text>
<rect x="14" y="354" width="500" height="54" rx="10" fill="none" stroke="#b2deda" stroke-width="1.5"/>
<path d="M30,366 v18 a10,4 0 0 0 20,0 v-18" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/><ellipse cx="40" cy="366" rx="10" ry="4" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<text x="62" y="376" font-size="14.5" font-weight="700" fill="#004d47">3 · Copia instalada, activa para el usuario</text>
<text x="62" y="394" font-size="12.5" fill="#555">~/.claude/plugins/cache/…/sf/0.13.1 · no se edita</text>
<line x1="264" y1="408" x2="264" y2="438" stroke="#00726b" stroke-width="2" marker-end="url(#flecha-cf)"/>
<text x="276" y="428" font-size="12" fill="#00726b">en cada sesión, en cualquier proyecto</text>
<rect x="14" y="442" width="500" height="126" rx="10" fill="none" stroke="#c0dcc4" stroke-width="1.5"/>
<text x="34" y="464" font-size="14.5" font-weight="700" fill="#1f812d">4 · Proyectos</text>
<text x="34" y="482" font-size="12.5" fill="#555">JKanban · LecturaFàcil · SmartColdBox…</text>
<text x="34" y="510" font-size="12.5" font-weight="700" fill="#1f812d">.sf/</text><text x="80" y="510" font-size="12.5" fill="#555">identidad y estado; los muestran la línea y /sf</text>
<text x="34" y="530" font-size="12.5" font-weight="700" fill="#1f812d">docs/decisiones/</text><text x="168" y="530" font-size="12.5" fill="#555">lo decidido en el proyecto</text>
<text x="34" y="550" font-size="12.5" font-weight="700" fill="#1f812d">JKanban</text><text x="96" y="550" font-size="12.5" fill="#555">las tareas y el estado vivo</text>
<path d="M514,520 H536 V194 H520" fill="none" stroke="#be185d" stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#flecha-cf-fra)"/>
<text transform="rotate(-90 550 357)" x="550" y="357" text-anchor="middle" font-size="12" fill="#be185d">mejoras: vuelven como propuesta</text>
<text x="14" y="592" font-size="12.5" font-style="italic" fill="#888">hasta que no se publica, un cambio en 1 no llega a 4</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Lo que se edita está arriba; lo que se usa, abajo. La línea discontinua es el único camino de vuelta.</figcaption>
</figure>

## Instalación del plugin

El repositorio de la SF es la **fuente**: aquí se crea y se modifica todo, pero ningún proyecto lo usa directamente. Los proyectos usan la **copia instalada**: la versión publicada, que Claude Code descarga en su caché.

Por eso un cambio en la fuente no llega a ningún proyecto hasta que se publica y se actualiza la copia instalada, y esa copia no se edita nunca, porque la siguiente actualización la sobrescribe. Para probar un cambio antes de publicarlo hay una vía aparte: abrir una sesión de prueba con `claude --plugin-dir D:/Projectes/SoftwareFactory/plugins/sf`.

El plugin se instala una sola vez por equipo, para el usuario. El procedimiento de instalación se describirá aparte.

## Componentes del plugin

La fuente del plugin `sf` está en la carpeta `plugins/sf/` de este repositorio. Al publicar una versión, todo su contenido queda disponible en los proyectos: Claude Code descarga esa versión y la usa en cualquier proyecto que se abra. Las rutas son relativas a esa carpeta. Sus componentes son de dos tipos, con finalidades distintas.

### Skills y sus recursos

**Finalidad común: que Claude trabaje según el método.** Son conocimiento e instrucciones que Claude carga cuando la tarea lo pide: qué hacer en cada fase, cómo hacerlo y con qué plantillas y herramientas. No hacen nada por sí solas; actúan a través del trabajo de Claude. La metodología y la guía de diagramas están dentro de la carpeta de la skill `sf:metodologia`; las plantillas y el kit de documentos, en la carpeta de las skills que los usan.

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,19rem),1fr));gap:.9rem;margin:1.2rem 0 1.6rem;"><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Metodología</p><p style="margin:0 0 .45rem;">Cómo se desarrolla un proyecto: fases, devslices, kanban, estructura y pruebas.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>skills/metodologia/references/desarrollo-de-proyectos.md</code></p><p style="margin:.45rem 0 0;font-size:.82rem;color:var(--primario);font-weight:600;">skill sf:metodologia</p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Guía de diagramas</p><p style="margin:0 0 .45rem;">Norma y recomendaciones para los diagramas SVG de cualquier documento.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>skills/metodologia/references/diagramas-svg.md</code></p><p style="margin:.45rem 0 0;font-size:.82rem;color:var(--primario);font-weight:600;">con sf:metodologia</p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Skills</p><p style="margin:0 0 .45rem;">Herramientas de Claude para cada fase: incorporación de un proyecto, flujo de tareas, visión, fundacional, interfaz, técnica e infografía, y de apoyo (color, GSAP, three.js).</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>skills/</code></p><p style="margin:.45rem 0 0;font-size:.82rem;color:var(--primario);font-weight:600;">prefijo sf:</p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Plantillas</p><p style="margin:0 0 .45rem;">Estructuras de carpetas por perfil técnico y reglas de la SF que importa el <code>CLAUDE.md</code> de cada proyecto.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>templates/</code></p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">CLI de la cola</p><p style="margin:0 0 .45rem;">Única vía para escribir <code>.sf/peticiones.json</code>: bloquea la cola (<code>peticiones.lock</code>), guarda una copia antes (<code>copias/</code>) y pasa lo que sale a <code>historial.jsonl</code>. Lo usan Claude y el panel. La consulta <code>choques</code> dice si una tarea comparte archivos con otra en curso o en Testing; con choques, sale con 3.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>tools/cola.py</code></p><p style="margin:.45rem 0 0;font-size:.82rem;color:var(--primario);font-weight:600;">con sf:flujo_tareas</p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Kit de documentos</p><p style="margin:0 0 .45rem;">Barra y herramientas de los documentos HTML: buscador, notas, lectura y edición.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>tools/kit_documentos/</code></p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Índice de decisiones</p><p style="margin:0 0 .45rem;">Genera el índice de <code>docs/decisiones/</code> y migra un <code>docs/decisiones.md</code> antiguo, sin Claude.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>tools/indice_decisiones.py</code></p></div></div>

### Mods

**Finalidad común: que el propietario vea y controle el proyecto desde Claude Code.** Cambian la interfaz o el comportamiento de Claude Code y actúan solos, en respuesta a eventos de la sesión, sin que Claude tenga que acordarse. Hoy hay uno, el panel; se resume en «El panel de la SF» y se detalla en [Cómo funciona el panel](como-funciona-el-panel.html).

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,19rem),1fr));gap:.9rem;margin:1.2rem 0 1.6rem;"><div class="ficha" style="margin:0;--oscuro:#673210;--borde:#e6cebf;border-top:4px solid #a6501a;"><p class="ficha-titulo">Mod de estado</p><p style="margin:0 0 .45rem;">Panel lateral de la SF (<code>/sf</code>) y caja de reserva sobre el prompt, que leen la carpeta <code>.sf/</code> del proyecto.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>hooks/</code></p></div></div>

## Componentes de la SF fuera del plugin

No se instala con el plugin: se queda en el repositorio de la SF.

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,19rem),1fr));gap:.9rem;margin:1.2rem 0 1.6rem;"><div class="ficha" style="margin:0;"><p class="ficha-titulo">Especificación</p><p style="margin:0 0 .45rem;">Qué hay que construir en la SF.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/specs/funcional/software-factory.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Visiones</p><p style="margin:0 0 .45rem;">La SF contada desde cada perspectiva.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/specs/vision/</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Decisiones</p><p style="margin:0 0 .45rem;">Lo que el propietario ha decidido sobre la SF, con su porqué.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/decisiones/</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Mejora continua a la Software Factory</p><p style="margin:0 0 .45rem;">Dónde se registra una decisión, con qué formato, en qué componentes se aplica y cómo llega a los proyectos.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/mejora-continua-a-la-software-factory.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Propuestas</p><p style="margin:0 0 .45rem;">Ideas de mejora aún sin decidir.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/propuestas.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Cómo funciona el panel</p><p style="margin:0 0 .45rem;">Cada parte del panel, qué controla, su código y su historial.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/como-funciona-el-panel.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Cómo funcionan los estados</p><p style="margin:0 0 .45rem;">Cada cambio de estado de una tarea: cuándo, quién, qué pide y qué hace en git.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/como-funcionan-los-estados.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Uso del panel</p><p style="margin:0 0 .45rem;">Cómo se vive el panel: fricciones y aciertos.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/uso-del-panel.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Investigación</p><p style="margin:0 0 .45rem;">Informes y notas con fuentes.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/referencias/</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">JKanban</p><p style="margin:0 0 .45rem;">El tablero de tareas, con un MCP para la SF. Su instalación en la SF está pendiente.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>D:\Projectes\JKanban</code></p></div></div>

## Estructura de un proyecto bajo la SF

Un proyecto está bajo la SF cuando tiene `.sf/proyecto.json`.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 330" width="100%" role="img" aria-label="Qué pone cada cual en un proyecto bajo la SF: lo versionado del proyecto, el estado local fuera de git y lo que viene de fuera" style="font-family:var(--fuente-texto);display:block">
<text x="14" y="20" font-size="12.5" font-weight="700" fill="#1f812d">En el repositorio del proyecto, versionado</text>
<rect x="14" y="30" width="500" height="114" rx="10" fill="none" stroke="#c0dcc4" stroke-width="1.5"/>
<text x="34" y="56" font-size="12.5" font-weight="700" fill="#1f812d">.sf/proyecto.json</text><text x="200" y="56" font-size="12.5" fill="#555">nombre, descripción, color, versión y kanban</text>
<text x="34" y="80" font-size="12.5" font-weight="700" fill="#1f812d">docs/decisiones/</text><text x="200" y="80" font-size="12.5" fill="#555">lo decidido, con su porqué</text>
<text x="34" y="104" font-size="12.5" font-weight="700" fill="#1f812d">CLAUDE.md</text><text x="200" y="104" font-size="12.5" fill="#555">importa las reglas de .sf/claude-sf.md</text>
<text x="34" y="128" font-size="12.5" font-weight="700" fill="#1f812d">docs/specs/</text><text x="200" y="128" font-size="12.5" fill="#555">visión, especificación, técnica y devslices</text>
<text x="14" y="172" font-size="12.5" font-weight="700" fill="#a6501a">Local, fuera de git</text>
<rect x="14" y="182" width="500" height="38" rx="10" fill="none" stroke="#e6cebf" stroke-width="1.5"/>
<text x="34" y="206" font-size="12.5" font-weight="700" fill="#a6501a">.sf/estado.json</text><text x="200" y="206" font-size="12.5" fill="#555">fase, devslice, fases hechas y pendientes</text>
<text x="14" y="248" font-size="12.5" font-weight="700" fill="#004d47">Fuera del proyecto</text>
<rect x="14" y="258" width="500" height="62" rx="10" fill="none" stroke="#b2deda" stroke-width="1.5"/>
<text x="34" y="282" font-size="12.5" font-weight="700" fill="#00726b">plugin sf</text><text x="200" y="282" font-size="12.5" fill="#555">instalado para el usuario: método, skills y mod</text>
<rect x="20" y="294" width="488" height="20" rx="6" fill="none" stroke="#bbb" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="34" y="308" font-size="12.5" font-weight="700" fill="#888">JKanban</text><text x="200" y="308" font-size="12.5" fill="#888">previsto: fuente del estado; estado.json, su copia</text>
<path d="M514,282 H538 V56 H520" fill="none" stroke="#00726b" stroke-width="1.6" marker-end="url(#flecha-est)"/>
<path d="M538,206 H520" fill="none" stroke="#00726b" stroke-width="1.6" marker-end="url(#flecha-est)"/>
<defs><marker id="flecha-est" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#00726b"/></marker></defs>
<text transform="rotate(-90 551 170)" x="551" y="170" text-anchor="middle" font-size="12" fill="#00726b">el mod lee .sf/</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">El proyecto solo versiona su identidad y sus documentos; el estado es local y, más adelante, vendrá de JKanban.</figcaption>
</figure>


El estado de `.sf/estado.json` se actualiza al cambiar de fase o de devslice, y la carpeta `.sf/` admite más archivos de la SF si hacen falta. Además de sus decisiones, el proyecto lleva en `docs/guias/` una guía de instalación desde cero y otra de actualización; junto a la visión puede tener, si le sirven, visiones desde otras perspectivas, infografías técnicas y su propio «Cómo funciona» (metodología, 3.1). Su `CLAUDE.md` importa con `@.sf/claude-sf.md` las reglas de la SF, que remiten a `sf:metodologia`, a las decisiones, al estado, a la cola y a la regla de mejora continua; el resto del `CLAUDE.md` es del proyecto. El proyecto no instala nada: el plugin `sf` ya está activo, porque se instaló para el usuario.


## Incorporación de un proyecto a la SF

La vía habitual es pedírselo a Claude en una sesión abierta en el proyecto («incorpora este proyecto a la SF»). Lo hace la skill `sf:incorporar_proyecto_a_sf`, que cubre cuatro casos: proyecto nuevo, existente, actualizar uno ya incorporado y diagnosticar sin cambiar nada (metodología, sección 2). Estos son sus pasos, que sirven también para hacerlo a mano.

**1. Plugin instalado.** Una vez por equipo, como se indica en «Instalación del plugin». El proyecto no instala nada.

**2. Identidad del proyecto,** en `.sf/proyecto.json`, versionado:

```json
{
  "sf": "0.7",
  "proyecto": "<nombre del proyecto>",
  "descripcion": "<qué es, en una línea de 120 caracteres como mucho>",
  "kanban": "<su proyecto en JKanban>",
  "color": "<color de sus sesiones: red, blue, green, yellow, orange, pink o cyan>"
}
```

**3. Estado inicial,** en `.sf/estado.json`, y esta ruta y las de la cola, `.sf/peticiones.json`, `.sf/peticiones.lock`, `.sf/historial.jsonl` y `.sf/copias/`, añadidas al `.gitignore` del proyecto. En un proyecto nuevo, la fase es `vision`:

```json
{
  "fase": "vision",
  "hechas": [],
  "actualizado": "<fecha>",
  "pendientes": []
}
```

**4. Reglas de la SF importadas en el `CLAUDE.md`.** Se copia la plantilla `plugins/sf/templates/claude-sf.md` a `.sf/claude-sf.md`, versionado, con la versión de la SF. Sus puntos: el método es la skill `sf:metodologia`; las decisiones van a `docs/decisiones/`, una por archivo, con su porqué; el estado está en `.sf/` y se actualiza al cambiar de fase o de devslice; la sesión solo modifica este proyecto; cada petición va a la cola, con un commit por petición; las mejoras de la SF que se detecten se registran en el proyecto SoftwareFactory del kanban, con el origen, y no se aplican sin aprobación del propietario; y, si una regla del proyecto choca con la SF, manda la del proyecto y se anota. En el `CLAUDE.md` solo se añade la línea `@.sf/claude-sf.md`, debajo del título: lo que ya tenía no se toca. Al pasar a otra versión de la SF, se regenera solo `.sf/claude-sf.md`. Los proyectos que llevan un apartado «Software Factory» escrito dentro del `CLAUDE.md` (las primeras incorporaciones, como JKanban) lo cambian por la importación al actualizarse. Si el `CLAUDE.md` es complejo, como el de OncoCore, revisar lo que choca con la SF es una tarea aparte, de una sesión entera.

**5. `docs/decisiones/`,** con su índice, `README.md`, aunque empiece sin decisiones. Un proyecto con el antiguo `docs/decisiones.md` lo migra con `tools/indice_decisiones.py docs/decisiones --migrar docs/decisiones.md`.

**6. Proyecto en el kanban,** cuando JKanban esté incorporado a la SF.

**Comprobación.** Al abrir Claude Code en el proyecto, el panel lateral de la SF se abre solo (en pantalla completa) con el proyecto, la fase, las peticiones y los documentos; sin panel, la caja sobre el prompt muestra `SF 0.7 · <proyecto> · <n>/7 <fase>`.

**Proyectos anteriores a la SF.** Se incorporan sin rehacer lo que ya funciona (metodología, sección 2). En `estado.json` se declara la fase real y, en `hechas`, solo las fases cubiertas de verdad; los documentos que faltan (por ejemplo, la visión o la especificación funcional) se anotan como pendientes; y `docs/` se reorganiza según la estructura común cuando no haya trabajo en curso que pueda chocar. JKanban es el primer caso.

## El panel de la SF

El **panel** es el mod de estado del plugin `sf`: una columna a la derecha de la conversación que enseña en qué se trabaja, qué espera y qué se ha cerrado. Un mod es la parte de un plugin que cambia la interfaz o el comportamiento de Claude Code, en respuesta a eventos de la sesión. Es el centro de control de la SF dentro de Claude Code, y el mismo en todos los proyectos.

En la pantalla completa se abre solo al empezar la sesión; `/sf` lo vuelve a abrir. Sin sitio para el panel, el mod se enseña en una caja pequeña sobre el prompt.

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
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">El panel en la SF, con dos tareas en curso y los bloques plegados.</figcaption>
</figure>

Arriba van el proyecto, su versión y su fase, y en amarillo las tareas en curso con su paso, la tocada la última arriba. Debajo, tres bloques de secciones plegables: **Tareas** (Pendientes, Testing y Cerradas), **Proyecto** (Documentos) y **SF ENHANCE** (el registro de uso y las mejoras de la SF). Cada tarea lleva una letra con su estado: A, nueva en la sesión; H, de antes; T, en Testing; C, cerrada y probada; D, descartada. A la derecha de una tarea, la T activa su rama para probarla, la C la cierra en `develop`, la E la elimina y la D la descarta. En la cabecera, RELEASE publica y ACTUALIZAR pone al día el plugin instalado. Lo hacen sin Claude, con git, la cola y los comandos de Claude Code. Cada cambio de estado se explica en [Cómo funcionan los estados](como-funcionan-los-estados.html).

Desde el panel, el propietario añade un paso a la tarea en curso con `/paso`, separa pasos de una tarea en una tarea nueva con `/split`, pide a Claude que explique un paso con «?» o lo quita con «−», y convierte una entrada del registro en tarea con «→».

El mod también controla que cada sesión modifique un solo proyecto: bloquea, con el motivo, la escritura de archivos en otro. Un worktree cuenta como su repositorio. Y no deja que un subagente escriba la cola. Lee `.sf/` al abrir la sesión, al acabar cada turno y tras cada herramienta que puede escribir, y solo escribe cuando lo pide el propietario. Su código está en `plugins/sf/hooks/`.

El detalle de cada parte, el control, el código y el historial de versiones están en [Cómo funciona el panel](como-funciona-el-panel.html).

## Flujo de trabajo en un proyecto

Al abrir una sesión en el proyecto, el mod lee `.sf/` y abre el panel lateral con el proyecto, la fase, la devslice y el detalle (sin panel, una caja sobre el prompt; `/sf` lo abre). Claude usa la skill `sf:metodologia`, que le indica qué sección del método leer según el momento, y en cada fase trabaja con la skill que toca: `sf:documento_vision`, `sf:diseno_interfaz`, `sf:definicion_tecnica`…

Lo que decide el propietario se anota en un archivo nuevo de `docs/decisiones/` del proyecto, y al cambiar de fase o de devslice se actualiza `.sf/estado.json`. Si algo del método o de una skill falla, sobra o falta, Claude lo registra como mejora de la SF (ver «Flujo de mejora de la SF»); en el proyecto solo se corrige lo que es propio de la aplicación.

## Flujo de mejora de la SF

La SF mejora con el uso. La tarea permanente **Mejorar la Software Factory**, del proyecto **SoftwareFactory** en el kanban, está siempre activa y recoge las mejoras que se detectan en cualquier proyecto, no solo en el repositorio de la SF. Ninguna mejora salta de la idea al código: pasa por una propuesta y por una decisión del propietario.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 44 560 356" width="100%" role="img" aria-label="Flujo de mejora de la SF, de la detección en un proyecto a la versión publicada" style="font-family:var(--fuente-texto);display:block">
<line x1="34" y1="66" x2="34" y2="346" stroke="#b2deda" stroke-width="2"/>
<circle cx="34" cy="66" r="7" fill="#fff" stroke="#1f812d" stroke-width="2"/>
<text x="56" y="64" font-size="14.5" font-weight="700" fill="#004d47">Detección en cualquier proyecto</text>
<text x="56" y="82" font-size="12.5" fill="#555">tarea en el kanban, proyecto SoftwareFactory</text>
<path d="M50,128 v16 a10,4 0 0 0 20,0 v-16" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/><ellipse cx="60" cy="128" rx="10" ry="4" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<circle cx="34" cy="136" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/>
<text x="82" y="134" font-size="14.5" font-weight="700" fill="#004d47">docs/propuestas.md</text>
<text x="82" y="152" font-size="12.5" fill="#555">origen, evidencia y cambio; nada se aplica aún</text>
<rect x="56" y="172" width="196" height="24" rx="12" fill="#be185d"/>
<text x="154" y="188" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">el propietario decide</text>
<path d="M50,208 v16 a10,4 0 0 0 20,0 v-16" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/><ellipse cx="60" cy="208" rx="10" ry="4" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<circle cx="34" cy="216" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/>
<text x="82" y="214" font-size="14.5" font-weight="700" fill="#004d47">docs/decisiones/</text>
<text x="82" y="232" font-size="12.5" fill="#555">con su porqué y dónde se aplica</text>
<circle cx="34" cy="282" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/>
<text x="56" y="280" font-size="14.5" font-weight="700" fill="#004d47">Aplicada en la fuente, en el momento</text>
<text x="56" y="298" font-size="12.5" fill="#555">metodología, especificación, skills o plantillas</text>
<circle cx="34" cy="346" r="7" fill="#00726b"/>
<text x="56" y="344" font-size="14.5" font-weight="700" fill="#004d47">Versión nueva del plugin</text>
<text x="56" y="362" font-size="12.5" fill="#555">llega a cada proyecto al actualizar el plugin</text>
<text x="34" y="392" font-size="12.5" font-style="italic" fill="#888">si no toca el plugin, basta con el squash a develop</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">La decisión del propietario es la única puerta entre proponer y cambiar.</figcaption>
</figure>

Todo empieza en un proyecto cualquiera. Mientras trabaja, Claude observa lo que falla, sobra, falta o se repite en el método, en una skill o en una plantilla. Las correcciones propias de la aplicación se quedan en su proyecto; si además revelan algo general, se registran también como mejora de la SF. Cada mejora es una tarea del proyecto **SoftwareFactory** en el kanban, vinculada a la tarea permanente, con el proyecto de origen, la devslice o tarea relacionada, el contexto y la evidencia. Mientras el kanban no esté conectado, se anota en `docs/propuestas.md` como pendiente de traslado, sin afirmar que la tarjeta existe.

En `docs/propuestas.md` la mejora se convierte en una propuesta: el cambio concreto, su beneficio, su impacto y cómo se comprobará. Ahí se detiene hasta que el propietario la aprueba, la ajusta o la descarta. Registrar o preparar una propuesta no autoriza aplicarla; una instrucción directa del propietario sí, dentro de su alcance. Lo aprobado pasa a un archivo de `docs/decisiones/` con su porqué, y lo descartado queda en «Descartadas», con el motivo.

Una decisión se aplica en el mismo momento, en la fuente: metodología, especificación, skills o plantillas. Si el cambio afecta al plugin, se publica una versión nueva, y cada proyecto la recibe al actualizar el plugin. Mientras tanto, el mod de estado lleva la cuenta: en la SF muestra cuántas propuestas esperan revisión y cuántas faltan por pasar al kanban.

### Publicación del plugin

Se desarrolla en `develop`; `main` es lo que instalan los proyectos (metodología, 2).

1. Cada tarea, en su rama `feature/NN-nombre`, creada desde `develop` antes de tocar el primer activo.
2. Cambiar y probar en la rama, con el plugin en **modo prueba** (abajo).
3. Comprobar con `claude plugin validate plugins/sf`.
4. Con el OK del propietario, squash de la rama a `develop`: un commit por tarea, con sus pasos en el cuerpo. Push de `develop` y se borra la rama. Cada decisión es un archivo propio, así que dos ramas no chocan al añadirlas; el índice, `docs/decisiones/README.md`, se junta sin choques (`merge=union` en `.gitattributes`) y se regenera con `tools/indice_decisiones.py`.
5. Publicar con el botón **RELEASE** de la cabecera del panel: el primer clic ofrece las tres versiones siguientes (patch, minor y major) y el segundo confirma la elegida, avisando de las tareas que quedan en Testing. Sube `version` en `plugins/sf/.claude-plugin/plugin.json` (solo aquí, nunca en una feature) con su commit en `develop`, pasa `develop` a `main` por fast-forward, lo marca con el tag `vX.Y.Z` y hace push de `develop`, `main` y el tag. Si algo no está en orden, no publica y dice cómo arreglarlo. Sin rama de release, salvo que la versión necesite preparación.
6. Actualizar la copia instalada con el botón **ACTUALIZAR**, en rojo, que sale cuando hay una versión publicada más nueva. Refresca el catálogo (`claude plugin marketplace update softwarefactory`), actualiza el plugin en cada scope y pide reiniciar Claude Code. Un equipo con una versión sin el botón se actualiza esa vez a mano.

Los cambios que no tocan el plugin (especificación, visiones, decisiones, propuestas) solo necesitan el squash a `develop`; llegan a `main` con la siguiente publicación.

**Modo prueba** (solo en la SF). Ver un cambio del plugin sin commit ni publicación. En este repositorio, el panel muestra junto al nombre del proyecto la etiqueta «prueba», atenuada (se usa el plugin publicado), o **PRUEBA** en naranja (se usa la copia de trabajo de `plugins/sf`). Un clic cambia de uno a otro: el mod escribe en `.claude/settings.local.json` (fuera de git) qué plugin está activo en este proyecto, `sf@softwarefactory-dev` o `sf@softwarefactory`, y lanza `/reload-plugins`. En modo prueba, cada retoque se ve con `/reload-plugins`, sin subir la versión. Al entrar en una sesión y al cerrarla, siempre desactivado: el mod lo apaga una vez por sesión (la sesión que ya lo apagó queda en `.sf/prueba.json`, fuera de git, porque `/reload-plugins` vuelve a pasar por el arranque) y, si la sesión arrancó con la copia de trabajo, recarga el publicado.

Preparación, una vez por equipo: el catálogo local `softwarefactory-dev`, en `D:/Projectes/.claude-plugin/marketplace.json`, fuera del repositorio, con el plugin `sf` en `./SoftwareFactory/plugins/sf`. Claude Code carga en su sitio, sin copiarlo a la caché, el plugin de un catálogo de carpeta; no acepta la ruta absoluta, la que sube de carpeta ni un enlace, y dos catálogos no pueden llamarse igual, por eso está en la carpeta de arriba. Después, en el repositorio: `claude plugin marketplace add D:/Projectes --scope local` y `claude plugin install sf@softwarefactory-dev --scope local`. Sin el catálogo registrado, el panel no muestra la etiqueta. Probado y descartado: la variable `CLAUDE_CODE_PLUGIN_DIRS` en los ajustes del proyecto, que no carga la copia de trabajo, ni con `/reload-plugins` ni al reiniciar.

## Índice de consulta

<dl class="faq">
<dt>¿Cómo se hace algo en un proyecto?</dt><dd>Metodología (skill <code>sf:metodologia</code>)</dd>
<dt>¿Qué falta por construir en la SF?</dt><dd>Especificación, próximos pasos</dd>
<dt>¿Por qué se hizo así?</dt><dd><code>docs/decisiones/</code></dd>
<dt>¿Cómo se registra una decisión y dónde se aplica?</dt><dd><code>docs/mejora-continua-a-la-software-factory.md</code></dd>
<dt>¿Qué ideas esperan aprobación?</dt><dd><code>docs/propuestas.md</code> y el proyecto SoftwareFactory del kanban</dd>
<dt>¿Qué hace el panel y cómo evoluciona?</dt><dd>«El panel de la SF», en este documento, y <code>docs/como-funciona-el-panel.md</code></dd>
<dt>¿Cómo cambia de estado una tarea?</dt><dd><code>docs/como-funcionan-los-estados.md</code> y la skill <code>sf:flujo_tareas</code></dd>
<dt>¿Cómo se pone un proyecto bajo la SF?</dt><dd>«Incorporación de un proyecto a la SF», en este documento</dd>
<dt>¿En qué punto está un proyecto?</dt><dd>Su <code>.sf/estado.json</code>, o <code>/sf</code> dentro de Claude Code</dd>
<dt>¿Qué decidió el propietario en un proyecto?</dt><dd>La carpeta <code>docs/decisiones/</code> de ese proyecto</dd>
<dt>¿Qué carpetas lleva un proyecto?</dt><dd>Metodología, sección 6, y las plantillas del plugin</dd>
<dt>¿Cómo se dibuja un diagrama?</dt><dd>Guía de diagramas en SVG (<code>plugins/sf/skills/metodologia/references/diagramas-svg.md</code>); nunca ASCII ni mermaid</dd>
<dt>¿De dónde viene una skill?</dt><dd>El <code>ORIGIN.md</code> de la skill</dd>
<dt>¿Cómo se instala o se publica el plugin?</dt><dd><code>plugins/sf/README.md</code> y este documento</dd>
<dt>¿Cómo empieza Claude a trabajar en la SF?</dt><dd><code>CLAUDE.md</code> del repositorio</dd>
</dl>

## Cuestiones pendientes de decisión

Está en [propuestas](propuestas.md). Lo que más afecta a este mapa:

- **Procedimiento de instalación del plugin.**
- **Cómo se instala JKanban dentro de la SF.**
- **Historial de versiones del plugin** (CHANGELOG).
- **Organización del repositorio de la SF.**
