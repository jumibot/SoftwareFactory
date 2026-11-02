# Cómo funciona la Software Factory

Este documento describe el funcionamiento de la Software Factory: sus componentes, dónde está cada uno y cómo se relacionan. No contiene reglas. Las reglas están en la metodología, en la especificación y en las decisiones, y aquí solo se dice dónde buscarlas.

**Estado:** 2 de noviembre de 2026, plugin `sf` 1.5.0.

## La SF es un plugin

Un **plugin de Claude Code** es un paquete que amplía Claude Code con piezas que se instalan juntas: skills, comandos con barra, agentes, hooks, servidores MCP y mods de la interfaz. Se publica por versiones y se instala entero, para un proyecto o para el usuario.

La SF se escribe en un solo sitio, este repositorio. Llega a los proyectos de una sola forma: el plugin `sf` de Claude Code. Lleva la metodología, las skills, las plantillas de reglas y de estructuras, el kit de documentos y el mod con el panel. Se publica y se instala una vez, para el usuario. Desde ese momento está en todas las sesiones, en cualquier proyecto, con el prefijo `sf:`.

Cada proyecto pone solo lo suyo. La carpeta `.sf/` lo identifica, guarda su configuración y lleva su estado y su cola. La carpeta `sf/` guarda los documentos de la SF en el proyecto: sus propuestas, sus decisiones y sus informes. El kanban es opcional.

El circuito se cierra al revés. Lo que falla o falta en la SF se lleva a una sesión de la SF y allí se convierte en propuesta. Solo cuando el propietario la aprueba se aplica en la fuente y se publica una versión nueva.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 44 560 556" width="100%" role="img" aria-label="Mapa de la SF: de la fuente a los proyectos, pasando por la versión publicada y la copia instalada, y la vuelta de las mejoras" style="font-family:var(--fuente-texto);display:block">
<defs><marker id="flecha-cf-fra" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#be185d"/></marker><marker id="flecha-cf" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#00726b"/></marker></defs>
<rect x="14" y="54" width="500" height="178" rx="10" fill="none" stroke="#b2deda" stroke-width="1.5"/>
<path d="M30,66 v18 a10,4 0 0 0 20,0 v-18" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/><ellipse cx="40" cy="66" rx="10" ry="4" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<text x="62" y="74" font-size="14.5" font-weight="700" fill="#004d47">1 · Fuente: el repositorio de la SF</text>
<text x="62" y="92" font-size="12.5" fill="#555">D:\Projectes\SoftwareFactory · aquí se edita todo</text>
<text x="34" y="124" font-size="12.5" font-weight="700" fill="#00726b">Contenido del plugin sf</text>
<text x="34" y="144" font-size="12.5" fill="#555">metodología (sf:metodologia)</text>
<text x="34" y="162" font-size="12.5" fill="#555">skills del método y de orquestación</text>
<text x="34" y="180" font-size="12.5" fill="#555">plantillas de reglas y estructuras</text>
<text x="34" y="198" font-size="12.5" fill="#555">kit de documentos y CLI de la cola</text>
<text x="34" y="216" font-size="12.5" fill="#555">mod: panel /sf y reglas</text>
<text x="290" y="124" font-size="12.5" font-weight="700" fill="#004d47">Se queda en el repositorio</text>
<text x="290" y="144" font-size="12.5" fill="#555">especificación</text>
<text x="290" y="162" font-size="12.5" fill="#555">visiones</text>
<text x="290" y="180" font-size="12.5" fill="#555">decisiones</text>
<text x="290" y="198" font-size="12.5" font-weight="700" fill="#be185d">propuestas</text>
<text x="290" y="216" font-size="12.5" fill="#555">investigación e informes</text>
<line x1="264" y1="232" x2="264" y2="262" stroke="#00726b" stroke-width="2" marker-end="url(#flecha-cf)"/>
<text x="276" y="252" font-size="12" fill="#00726b">RELEASE: a main, con tag</text>
<rect x="14" y="266" width="500" height="54" rx="10" fill="none" stroke="#b2deda" stroke-width="1.5"/>
<path d="M30,278 v18 a10,4 0 0 0 20,0 v-18" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/><ellipse cx="40" cy="278" rx="10" ry="4" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<text x="62" y="288" font-size="14.5" font-weight="700" fill="#004d47">2 · Versión publicada</text>
<text x="62" y="306" font-size="12.5" fill="#555">cada versión del plugin, con su tag vX.Y.Z</text>
<line x1="264" y1="320" x2="264" y2="350" stroke="#00726b" stroke-width="2" marker-end="url(#flecha-cf)"/>
<text x="276" y="340" font-size="12" fill="#00726b">ACTUALIZAR, desde el panel</text>
<rect x="14" y="354" width="500" height="54" rx="10" fill="none" stroke="#b2deda" stroke-width="1.5"/>
<path d="M30,366 v18 a10,4 0 0 0 20,0 v-18" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/><ellipse cx="40" cy="366" rx="10" ry="4" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<text x="62" y="376" font-size="14.5" font-weight="700" fill="#004d47">3 · Copia instalada, activa para el usuario</text>
<text x="62" y="394" font-size="12.5" fill="#555">~/.claude/plugins/cache/…/sf/1.5.0 · no se edita</text>
<line x1="264" y1="408" x2="264" y2="438" stroke="#00726b" stroke-width="2" marker-end="url(#flecha-cf)"/>
<text x="276" y="428" font-size="12" fill="#00726b">en cada sesión, en cualquier proyecto</text>
<rect x="14" y="442" width="500" height="126" rx="10" fill="none" stroke="#c0dcc4" stroke-width="1.5"/>
<text x="34" y="464" font-size="14.5" font-weight="700" fill="#1f812d">4 · Proyectos</text>
<text x="34" y="482" font-size="12.5" fill="#555">JKanban · LecturaFàcil · SmartColdBox…</text>
<text x="34" y="510" font-size="12.5" font-weight="700" fill="#1f812d">.sf/</text><text x="80" y="510" font-size="12.5" fill="#555">identidad, configuración, estado y cola</text>
<text x="34" y="530" font-size="12.5" font-weight="700" fill="#1f812d">sf/</text><text x="80" y="530" font-size="12.5" fill="#555">propuestas, decisiones e informes</text>
<text x="34" y="550" font-size="12.5" font-weight="700" fill="#1f812d">kanban</text><text x="96" y="550" font-size="12.5" fill="#555">opcional; por defecto, ninguno</text>
<path d="M514,520 H536 V194 H520" fill="none" stroke="#be185d" stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#flecha-cf-fra)"/>
<text transform="rotate(-90 550 357)" x="550" y="357" text-anchor="middle" font-size="12" fill="#be185d">mejoras: el propietario las trae a la SF</text>
<text x="14" y="592" font-size="12.5" font-style="italic" fill="#888">hasta que no se publica, un cambio en 1 no llega a 4</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Lo que se edita está arriba; lo que se usa, abajo. La línea discontinua es el único camino de vuelta.</figcaption>
</figure>

## Instalación del plugin

El repositorio de la SF es la **fuente**: aquí se crea y se modifica todo, pero ningún proyecto lo usa directamente. Los proyectos usan la **copia instalada**: la versión publicada, que Claude Code descarga en su caché.

Por eso un cambio en la fuente no llega a ningún proyecto hasta que se publica y se actualiza la copia instalada. Esa copia no se edita nunca, porque la siguiente actualización la sobrescribe. Para ver un cambio antes de publicarlo está el **modo prueba**, solo en la SF (en «Publicación del plugin»).

El plugin se instala una sola vez por equipo, para el usuario, desde el catálogo de la SF en GitHub:

```
claude plugin marketplace add jumibot/SoftwareFactory
claude plugin install sf@softwarefactory --scope user
```

**Dependencias.** Las skills externas que la SF usa tal cual no viajan copiadas en el plugin: son dependencias de `sf` («Skills externas: tal cual, como dependencias; adaptadas, como propias»). Hoy son tres plugins: `gsap-skills`, `threejs-skills` y `oklch-skill`. Están en el catálogo de la SF, fijados a un commit de sus repositorios, así que instalar `sf` las trae sin añadir otro catálogo («Todas las skills externas actuales, como dependencias»). Solo viaja en el plugin una skill externa adaptada, que entonces es nuestra, con su `ORIGIN.md`. `dataviz` no es dependencia: es un requisito del entorno, anotado en `sf:documento_vision`.

Sin una de sus dependencias, `sf` no carga, ni su panel. `claude plugin update` no instala las nuevas, y `claude plugin install` solo instala el primer plugin que se le da. Por eso, a mano, va una orden por plugin. Quien actualiza desde la 1.2.10 o antes, con el ACTUALIZAR de entonces, tiene que instalarlas así una vez. Las órdenes están en `plugins/sf/README.md`.

## Componentes del plugin

La fuente del plugin `sf` está en la carpeta `plugins/sf/` de este repositorio. Al publicar una versión, todo su contenido queda disponible en los proyectos: Claude Code descarga esa versión y la usa en cualquier proyecto que se abra. Las rutas son relativas a esa carpeta. Sus componentes son de dos tipos, con finalidades distintas.

### Skills y sus recursos

**Finalidad común: que Claude trabaje según el método.** Son conocimiento e instrucciones que Claude carga cuando la tarea lo pide: qué hacer en cada fase, cómo hacerlo y con qué plantillas y herramientas. No hacen nada por sí solas; actúan a través del trabajo de Claude. La metodología y la guía de diagramas están dentro de la carpeta de la skill `sf:metodologia`; el kit de documentos y los generadores, en la carpeta de las skills que los usan.

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,19rem),1fr));gap:.9rem;margin:1.2rem 0 1.6rem;"><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Metodología</p><p style="margin:0 0 .45rem;">Cómo se desarrolla un proyecto: fases, devslices, kanban, estructura y pruebas.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>skills/metodologia/references/desarrollo-de-proyectos.md</code></p><p style="margin:.45rem 0 0;font-size:.82rem;color:var(--primario);font-weight:600;">skill sf:metodologia</p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Guía de diagramas</p><p style="margin:0 0 .45rem;">Norma y recomendaciones para los diagramas SVG de cualquier documento.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>skills/metodologia/references/diagramas-svg.md</code></p><p style="margin:.45rem 0 0;font-size:.82rem;color:var(--primario);font-weight:600;">con sf:metodologia</p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Orquestación</p><p style="margin:0 0 .45rem;">Las reglas del agente principal: qué hacer con cada mensaje del propietario, la cola, los subagentes, la prueba y el cierre, y cómo preguntar y escribir. En los proyectos la entrega el mod entera; en la SF la carga el principal.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>skills/orquestacion/</code></p><p style="margin:.45rem 0 0;font-size:.82rem;color:var(--primario);font-weight:600;">skill sf:orquestacion</p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Skills del método</p><p style="margin:0 0 .45rem;">Herramientas de Claude para cada fase y para el trabajo diario: incorporación de un proyecto, configuración del proyecto, flujo de tareas, visión, fundacional, interfaz, técnica e infografía.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>skills/</code></p><p style="margin:.45rem 0 0;font-size:.82rem;color:var(--primario);font-weight:600;">prefijo sf:</p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Plantillas de reglas</p><p style="margin:0 0 .45rem;">Las reglas que reciben los proyectos, partidas en dos: las comunes, en <code>claude-sf.md</code>, y las del método, en <code>claude-sf-metodologia.md</code>, solo si el proyecto lo sigue. No se copian al proyecto: las entrega el mod.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>templates/claude-sf.md</code>, <code>templates/claude-sf-metodologia.md</code></p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Otras plantillas</p><p style="margin:0 0 .45rem;">Estructuras de carpetas por perfil técnico y el <code>propuestas.md</code> vacío que crea la incorporación.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>templates/estructuras/</code>, <code>templates/propuestas.md</code></p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">CLI de la cola</p><p style="margin:0 0 .45rem;">Única vía para escribir <code>.sf/peticiones.json</code>: bloquea la cola (<code>peticiones.lock</code>), guarda una copia antes (<code>copias/</code>) y pasa lo que sale a <code>historial.jsonl</code>. Lo usan Claude y el panel. También registra las decisiones (<code>decision</code>), escribe la parte fija del encargo de un subagente (<code>encargo</code>) y dice si una tarea comparte archivos con otra en curso o en observación (<code>choques</code>, que sale con 3 si los hay).</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>tools/cola.py</code></p><p style="margin:.45rem 0 0;font-size:.82rem;color:var(--primario);font-weight:600;">con sf:flujo_tareas</p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Lanzador de la cola</p><p style="margin:0 0 .45rem;">El panel lo copia al cargar a <code>~/.claude/sf/cola.py</code>. Claude lanza siempre <code>python -I -X utf8 "$HOME/.claude/sf/cola.py" &lt;orden&gt;</code>, y el lanzador pasa la orden a la copia de <code>cola.py</code> de su sesión, la misma que usa el panel. Así Claude nunca usa el <code>cola.py</code> de la rama activa.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>tools/cola_sesion.py</code></p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Kit de documentos</p><p style="margin:0 0 .45rem;">Barra y herramientas de los documentos HTML: buscador, notas, lectura y edición.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>tools/kit_documentos/</code></p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Configuración del proyecto</p><p style="margin:0 0 .45rem;">Enseña y comprueba <code>.sf/proyecto.json</code> (<code>ver</code>) y detecta las convenciones del repositorio (<code>detectar</code>): remotos, ramas, manifiestos, forma de los commits y colores de los proyectos vecinos. Solo lee. La usan la incorporación y <code>sf:configurar_proyecto</code>.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>tools/configuracion.py</code></p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Índice de decisiones</p><p style="margin:0 0 .45rem;">Regenera el índice <code>README.md</code> de las decisiones, sin Claude. Con <code>--html</code> genera también su <code>README.html</code>, que no se versiona. Con <code>--nombre</code> da el nombre de una decisión nueva, y con <code>--migrar</code> parte un <code>decisiones.md</code> antiguo en un archivo por decisión.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>tools/indice_decisiones.py</code></p></div></div>

### Mods

**Finalidad común: que el propietario vea y controle el proyecto desde Claude Code.** Cambian la interfaz o el comportamiento de Claude Code y actúan solos, en respuesta a eventos de la sesión, sin que Claude tenga que acordarse. Hoy hay uno, el mod de estado, con el panel; se resume en «El panel de la SF» y se detalla en [Cómo funciona el panel](como-funciona-el-panel.html).

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,19rem),1fr));gap:.9rem;margin:1.2rem 0 1.6rem;"><div class="ficha" style="margin:0;--oscuro:#673210;--borde:#e6cebf;border-top:4px solid #a6501a;"><p class="ficha-titulo">Mod de estado</p><p style="margin:0 0 .45rem;">Panel lateral de la SF (<code>/sf</code>) y caja de reserva sobre el prompt, que leen <code>.sf/</code>. Entrega a Claude las reglas, la orquestación y los avisos.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>hooks/</code></p></div></div>

El mod está repartido en módulos, todos en `hooks/`:

| Módulo | Qué hace |
| --- | --- |
| `register.tsx` | Engancha el mod a los eventos de la sesión y registra los comandos `/sf` y `/sf_…`, también `/sf_config`. |
| `panel.tsx` | Pinta el panel y la caja sobre el prompt, y atiende sus clics. |
| `cola.ts` | Lee el estado, lanza `cola.py` y hace RELEASE, ACTUALIZAR y REFRESCAR. |
| `lectura.ts` | Lee la cola, el historial y el estado del proyecto. |
| `configuracion.ts` | Lee `.sf/proyecto.json` con sus valores por defecto. |
| `contexto.ts` | Entrega las reglas y la orquestación, y añade la regla de lo que es de la SF al prompt de sistema. |
| `avisos.ts` | Avisa a Claude de lo que el propietario ha cambiado desde el panel. |
| `subagentes.ts` y `memoria.ts` | Avisan de las tareas en curso sin subagente y de los subagentes sin recoger, y guardan lo avisado en `.sf/subagentes.json`. |
| `control.ts` | Bloquea la escritura en otro proyecto, y en la cola desde un subagente. |
| `emergentes.ts` | Da forma a los avisos emergentes: lo importante primero, sin rutas largas. |
| `pantalla.ts` | Sin pantalla completa, avisa de que los clics no llegan. |
| `prueba.ts` | Lleva el modo prueba, solo en la SF. |
| `identidad.ts` | Pone a la sesión el color y el nombre del proyecto. |
| `estilo.ts` y `constantes.ts` | Colores, anchos, rutas y nombres comunes. |

## Componentes de la SF fuera del plugin

No se instala con el plugin: se queda en el repositorio de la SF.

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,19rem),1fr));gap:.9rem;margin:1.2rem 0 1.6rem;"><div class="ficha" style="margin:0;"><p class="ficha-titulo">Especificación</p><p style="margin:0 0 .45rem;">Qué hay que construir en la SF.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/specs/funcional/software-factory.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Visiones</p><p style="margin:0 0 .45rem;">La SF contada desde cada perspectiva.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/specs/vision/</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Decisiones</p><p style="margin:0 0 .45rem;">Lo que el propietario ha decidido sobre la SF, con su porqué. La SF aún las tiene en <code>docs/</code>; los proyectos, en <code>sf/</code>.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/decisiones/</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Mejora continua a la Software Factory</p><p style="margin:0 0 .45rem;">Dónde se registra una decisión, con qué formato, en qué componentes se aplica y cómo llega a los proyectos.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/mejora-continua-a-la-software-factory.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Propuestas</p><p style="margin:0 0 .45rem;">Ideas de mejora aún sin decidir.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/propuestas.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Cómo funciona el panel</p><p style="margin:0 0 .45rem;">Cada parte del panel, qué controla, su código y su historial.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/como-funciona-el-panel.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Cómo funcionan los estados</p><p style="margin:0 0 .45rem;">Cada cambio de estado de una tarea: cuándo, quién, qué pide y qué hace en git.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/como-funcionan-los-estados.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Uso del panel</p><p style="margin:0 0 .45rem;">Cómo se vive el panel: fricciones y aciertos.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/uso-del-panel.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Investigación e informes</p><p style="margin:0 0 .45rem;">Informes y notas con fuentes, como «Configuración inicial» o «Tipos de tarea».</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/referencias/</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">JKanban</p><p style="margin:0 0 .45rem;">El tablero de tareas, con un MCP para la SF. Es opcional y aún no está conectado.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>D:\Projectes\JKanban</code></p></div></div>

## Estructura de un proyecto bajo la SF

Un proyecto está bajo la SF cuando tiene `.sf/proyecto.json`. Hay dos carpetas de la SF, con una regla sencilla: `.sf/` es la máquina y `sf/` son los documentos («Los documentos de la SF van en la carpeta sf/»).

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 390" width="100%" role="img" aria-label="Qué pone cada cual en un proyecto bajo la SF: lo versionado del proyecto, lo local fuera de git y lo que viene de fuera" style="font-family:var(--fuente-texto);display:block">
<defs><marker id="flecha-est" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#00726b"/></marker></defs>
<text x="14" y="20" font-size="12.5" font-weight="700" fill="#1f812d">En el repositorio del proyecto, versionado</text>
<rect x="14" y="30" width="500" height="114" rx="10" fill="none" stroke="#c0dcc4" stroke-width="1.5"/>
<text x="34" y="56" font-size="12.5" font-weight="700" fill="#1f812d">.sf/proyecto.json</text><text x="200" y="56" font-size="12.5" fill="#555">identidad y configuración</text>
<text x="34" y="80" font-size="12.5" font-weight="700" fill="#1f812d">sf/</text><text x="200" y="80" font-size="12.5" fill="#555">propuestas, decisiones e informes</text>
<text x="34" y="104" font-size="12.5" font-weight="700" fill="#1f812d">CLAUDE.md</text><text x="200" y="104" font-size="12.5" fill="#555">solo lo del proyecto, sin líneas de la SF</text>
<text x="34" y="128" font-size="12.5" font-weight="700" fill="#1f812d">docs/</text><text x="200" y="128" font-size="12.5" fill="#555">documentos del proyecto, donde ya estén</text>
<text x="14" y="172" font-size="12.5" font-weight="700" fill="#a6501a">Local, fuera de git</text>
<rect x="14" y="182" width="500" height="86" rx="10" fill="none" stroke="#e6cebf" stroke-width="1.5"/>
<text x="34" y="206" font-size="12.5" font-weight="700" fill="#a6501a">.sf/estado.json</text><text x="200" y="206" font-size="12.5" fill="#555">fase y devslice, con metodología</text>
<text x="34" y="230" font-size="12.5" font-weight="700" fill="#a6501a">.sf/peticiones.json</text><text x="200" y="230" font-size="12.5" fill="#555">la cola, su historial y sus copias</text>
<text x="34" y="254" font-size="12.5" font-weight="700" fill="#a6501a">.claude/worktrees/</text><text x="200" y="254" font-size="12.5" fill="#555">los worktrees de los subagentes</text>
<text x="14" y="296" font-size="12.5" font-weight="700" fill="#004d47">Fuera del proyecto</text>
<rect x="14" y="306" width="500" height="70" rx="10" fill="none" stroke="#b2deda" stroke-width="1.5"/>
<text x="34" y="330" font-size="12.5" font-weight="700" fill="#00726b">plugin sf</text><text x="200" y="330" font-size="12.5" fill="#555">instalado para el usuario: método, reglas y mod</text>
<rect x="20" y="342" width="488" height="24" rx="6" fill="none" stroke="#bbb" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="34" y="358" font-size="12.5" font-weight="700" fill="#888">kanban</text><text x="200" y="358" font-size="12.5" fill="#888">opcional: JKanban, aún sin conectar</text>
<path d="M514,330 H538 V56 H520" fill="none" stroke="#00726b" stroke-width="1.6" marker-end="url(#flecha-est)"/>
<path d="M538,206 H520" fill="none" stroke="#00726b" stroke-width="1.6" marker-end="url(#flecha-est)"/>
<path d="M538,230 H520" fill="none" stroke="#00726b" stroke-width="1.6" marker-end="url(#flecha-est)"/>
<text transform="rotate(-90 551 190)" x="551" y="190" text-anchor="middle" font-size="12" fill="#00726b">el mod lee .sf/</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">El proyecto versiona su configuración y los documentos; la máquina de la cola y el estado se quedan en el equipo.</figcaption>
</figure>

**`.sf/proyecto.json`** identifica el proyecto y guarda su configuración, en campos sueltos. Lo que falta vale lo de por defecto, y lo que no se entiende sale en los avisos del panel, sin bloquear. Por ejemplo:

```json
{
  "sf": "1.5.0",
  "proyecto": "LecturaFàcil",
  "descripcion": "Adapta textos a lectura fácil con revisión humana",
  "color": "pink",
  "metodologia": true,
  "kanban": { "proveedor": "jkanban", "proyecto": "LecturaFàcil" },
  "idioma": "ca",
  "commits": "libre",
  "remoto": "origin",
  "rama_main": "master",
  "manifiesto": ["frontend/package.json", "backend/pyproject.toml"]
}
```

- `sf` es la versión de la SF con la que se incorporó o se puso al día. Si sus dos primeros números van por detrás del plugin, el panel avisa de que el proyecto va atrasado.
- `metodologia` dice si el proyecto sigue el método, con fases y documentos. Sin metodología, el panel no da fase ni lee `.sf/estado.json`, y el proyecto solo recibe las reglas comunes.
- `kanban` es opcional y por defecto no está («El kanban se elige, y por defecto ninguno»).
- `idioma` es el de los commits, las tareas y los documentos que escribe Claude.
- `commits` es `libre`, `conventional` o `propio`. Con `libre`, el commit de una tarea lleva «(N)» al final del título; con los otros dos, el trailer `SF-Tarea: N` al pie, y el squash, el prefijo del tipo de tarea.
- `remoto` es el remoto de GitHub al que se sube. Sin remoto en GitHub no hay SF. Si no existe o no apunta a GitHub, el panel lo avisa.
- `rama_main` es la rama en la que se publica: `main` u otra que haga de `main`, como `master`.
- `manifiesto` son los archivos cuya versión sube al publicar (`package.json`, `pyproject.toml` o `plugin.json`), o `null` si solo se marca el tag.
- `automatizaciones` solo aparece si se apaga algo. Cada regla que el mod o `cola.py` aplican solos tiene su interruptor, encendido por defecto: `orquestacion`, `avisos_subagentes`, `dependencias_al_actualizar` y `encargo_subagente`.

El detalle de cada campo está en `plugins/sf/README.md` y en el informe «Configuración inicial».

**Cambiar la configuración.** Se cambia con `/sf_config`, o pidiéndoselo a Claude («La configuración se cambia pidiéndoselo a Claude, con menús»). La skill `sf:configurar_proyecto` la enseña, pregunta qué cambiar con menús, pide el OK y lo aplica en `develop` con su commit, sin tarea. Lo que se ve y se detecta lo da `tools/configuracion.py`, que solo lee. La propia SF no tiene `.sf/proyecto.json`: su configuración sale de su marca, con el manifiesto del plugin y lo demás por defecto.

**`sf/`** guarda los documentos de la SF: `sf/propuestas.md`, `sf/decisiones/` (una decisión por archivo, con su índice) y `sf/informes/`. Los documentos del proyecto se quedan donde ya están: la SF no los mueve ni los mapea. Si siguen su estructura documental, están donde la SF los busca; si no, no se mapean («Sin mapa de documentos: o se sigue la estructura de la SF, o no se mapea»).

**Lo local.** `.sf/estado.json` guarda la fase y la devslice, solo con metodología, y se actualiza al cambiar de una a otra. La cola, `.sf/peticiones.json`, va con su bloqueo, `.sf/peticiones.lock`, su historial, `.sf/historial.jsonl`, y sus copias, `.sf/copias/`. `.sf/subagentes.json` es lo que el mod sabe de los subagentes de cada sesión, para no perderlo al recargar el plugin. Los worktrees de los subagentes van en `.claude/worktrees/`. Todo eso, y el `sf/decisiones/README.html`, va al `.gitignore` del proyecto.

**El `CLAUDE.md`** es solo del proyecto. No lleva ninguna línea de la SF: las reglas las entrega el mod (abajo, «Lo que recibe la sesión»). El proyecto no instala nada: el plugin `sf` ya está activo, porque se instaló para el usuario.

## Incorporación de un proyecto a la SF

La vía es pedírselo a Claude en una sesión abierta en el proyecto («incorpora este proyecto a la SF»). Lo hace la skill `sf:incorporar_proyecto_a_sf`. Cubre cuatro casos: proyecto nuevo, existente, actualizar uno ya incorporado y diagnosticar sin cambiar nada.

**Una operación, sin tarea.** Incorporar y poner al día no pasan por la cola ni por el panel, y no crean tarea ni rama («Incorporar un proyecto es una operación sin tarea, guiada por menús»). Claude la guía con menús en la línea de prompts. Dice qué va a crear, mover o cambiar, pide el OK y lo aplica en `develop`, con su commit: «Incorporado a la SF <versión>» o «Actualizado a la SF <versión>».

**Sin cambiar el proyecto.** La SF no renombra ni mueve nada del proyecto («Incorporar un proyecto no mueve ni renombra nada»). Lo que necesita lo usa donde ya está o lo añade con lo mínimo. La única excepción es pasar a `sf/` los documentos de la SF y las decisiones que el proyecto ya tuviera, con su propio OK y en su propio commit.

**Lo fijo, lo detectado y lo elegido.** Lo fijo no se pregunta: la cola, el modelo de ramas con `develop`, un remoto en GitHub, los commits de Claude, la versión con su tag y las decisiones en `sf/decisiones/`. Negarse a `develop`, al remoto o a que Claude lleve los commits es no usar la SF: se explica, se pide reconfirmar y, si se reconfirma, se para sin cambiar nada. Lo demás se detecta y se confirma (idioma, formato de commit, remoto, rama de publicación y manifiestos) o se elige (metodología y kanban).

Las preguntas van en tres menús, por este orden:

1. **Identidad:** nombre, descripción, color de las sesiones y si sigue la metodología.
2. **Repositorio:** si `master` hace de `main`, crear `develop`, el remoto de GitHub (y crearlo con `gh` si no hay ninguno) y que los commits los haga Claude.
3. **Convenciones:** idioma, formato de los commits, manifiestos y kanban.

Lo que se detecta sin duda no se pregunta: se enseña en el resumen antes del OK. Si una rama solo está en el remoto, se crea la local siguiéndola, sin preguntar.

Después se crean `.sf/proyecto.json`, `.sf/estado.json` (con metodología), las líneas del `.gitignore`, `sf/decisiones/` con su índice y su línea `merge=union` en `.gitattributes`, y `sf/propuestas.md` con su «## Propuestas pendientes». Si no hay `CLAUDE.md`, se crea solo con el título y la descripción. Los choques de un `CLAUDE.md` existente con la SF se proponen uno por uno; si es complejo, como el de OncoCore, revisarlo es una tarea aparte, de una sesión entera.

**Actualizar.** Primero se pone al día el plugin si hay una versión publicada más nueva, y se pide `/reload-plugins`. Después se diagnostica y se aplica lo que falta: los campos nuevos de la configuración, el paso a `sf/` y quitar la copia antigua de las reglas, `.sf/claude-sf.md`, con su línea `@.sf/claude-sf.md` del `CLAUDE.md`. Al final se enseña la configuración con que queda y se ofrece cambiarla, con `sf:configurar_proyecto`, y se pide `/clear`, para que entren las reglas nuevas.

**Comprobación.** Al abrir Claude Code en el proyecto, el panel lateral de la SF se abre solo, en pantalla completa, con el color de las sesiones del proyecto, la fase si sigue la metodología y sus tareas, sin avisos de la configuración. Sin panel, la caja sobre el prompt muestra `SF <versión> · <proyecto>` y, con metodología, la fase.

## Lo que recibe la sesión

En un proyecto incorporado, el mod da a Claude lo que necesita para trabajar según la SF, siempre de la versión instalada del plugin. No depende de que Claude se acuerde de cargarlo ni de una copia en el proyecto («El panel entrega las reglas y la orquestación en los proyectos»).

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 270" width="100%" role="img" aria-label="Qué entrega el mod a la sesión y cuándo: las reglas y la orquestación al empezar, la regla de lo que es de la SF en cada petición y los avisos con cada mensaje" style="font-family:var(--fuente-texto);display:block">
<line x1="34" y1="22" x2="34" y2="192" stroke="#e6cebf" stroke-width="2"/>
<circle cx="34" cy="22" r="7" fill="#fff" stroke="#a6501a" stroke-width="2"/>
<text x="56" y="20" font-size="14.5" font-weight="700" fill="#004d47">Al empezar, tras /clear y tras compactar</text>
<text x="56" y="40" font-size="12.5" fill="#555">las reglas comunes, de claude-sf.md</text>
<text x="56" y="58" font-size="12.5" fill="#555">las del método, si el proyecto lo sigue</text>
<text x="56" y="76" font-size="12.5" fill="#555">una línea con sus convenciones</text>
<text x="56" y="94" font-size="12.5" fill="#555">sf:orquestacion entera, salvo que se apague</text>
<circle cx="34" cy="134" r="7" fill="#fff" stroke="#a6501a" stroke-width="2"/>
<text x="56" y="132" font-size="14.5" font-weight="700" fill="#004d47">En cada petición, en el prompt de sistema</text>
<text x="56" y="152" font-size="12.5" fill="#555">lo que pinta la SF y lo global no son del proyecto</text>
<circle cx="34" cy="192" r="7" fill="#a6501a"/>
<text x="56" y="190" font-size="14.5" font-weight="700" fill="#004d47">Con cada mensaje del propietario</text>
<text x="56" y="210" font-size="12.5" fill="#555">lo que ha cambiado desde el panel</text>
<text x="56" y="228" font-size="12.5" fill="#555">tareas en curso sin subagente y subagentes sin recoger</text>
<text x="14" y="260" font-size="12.5" font-style="italic" fill="#888">las dos primeras, solo en proyectos: a la SF se las da su CLAUDE.md</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Tres momentos y tres entregas: nada de esto vive en el proyecto.</figcaption>
</figure>

**Las reglas y la orquestación.** Al empezar la sesión, tras `/clear` y tras compactar, el mod añade al contexto las reglas comunes de `templates/claude-sf.md`, las del método de `templates/claude-sf-metodologia.md` si el proyecto lo sigue y una línea con sus convenciones: idioma, commits, remoto y rama de publicación. Añade también el texto entero de `sf:orquestacion`, que se apaga con `"automatizaciones": {"orquestacion": false}`; entonces la carga el principal. Los subagentes no la reciben.

Si el `CLAUDE.md` aún importa la copia antigua, `@.sf/claude-sf.md`, el mod entrega solo la orquestación, para no dar las reglas dos veces, y el panel avisa de que el proyecto va atrasado. Ponerlo al día quita la copia y la línea.

**Lo que es de la SF.** En cada petición, el mod añade al final del prompt de sistema una regla corta: lo que el plugin pinta en el proyecto (el panel, la caja, los avisos) y sus skills son de la SF, y `~/.claude` es de todos los proyectos («Lo que pinta la SF y lo global no son del proyecto»). Una petición sobre ello no se cambia en el proyecto ni se anota en él: Claude dice en una línea que es de la SF. Va en el prompt de sistema para que llegue siempre, también a los proyectos atrasados.

**Los avisos.** Con cada mensaje del propietario, el mod dice a Claude lo que el propietario ha cambiado en la cola desde el panel desde el mensaje anterior. Y le avisa de las tareas en curso sin subagente vivo y de los subagentes que han terminado sin recoger, una vez cada situación. Estos avisos se apagan con `"automatizaciones": {"avisos_subagentes": false}`. Llegan también en la SF.

## El panel de la SF

El **panel** es el mod de estado del plugin `sf`: una columna a la derecha de la conversación que enseña en qué se trabaja, qué espera y qué se ha cerrado. Un mod es la parte de un plugin que cambia la interfaz o el comportamiento de Claude Code, en respuesta a eventos de la sesión. Es el centro de control de la SF dentro de Claude Code, y el mismo en todos los proyectos.

En la pantalla completa se abre solo al empezar la sesión; `/sf` lo vuelve a abrir. Sin sitio para el panel, el mod se enseña en una caja pequeña sobre el prompt. Fuera de la pantalla completa los clics no llegan: el panel lo dice y Claude ofrece activarla.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 312" width="100%" role="img" aria-label="Esquema del panel de la SF: la cabecera con sus etiquetas, la tarea en curso con sus pasos y el bloque de tareas con Pendientes, En observación, Cerradas y Propuestas" style="font-family:var(--fuente-texto);display:block">
<rect x="14" y="6" width="290" height="300" rx="6" fill="none" stroke="#bbb" stroke-width="1.2"/>
<rect x="22" y="14" width="62" height="18" rx="3" fill="none" stroke="#a6501a" stroke-width="1"/><text x="53" y="27" text-anchor="middle" font-size="10.5" font-weight="700" fill="#a6501a">RELEASE</text>
<rect x="90" y="14" width="52" height="18" rx="3" fill="none" stroke="#a6501a" stroke-width="1"/><text x="116" y="27" text-anchor="middle" font-size="10.5" font-weight="700" fill="#a6501a">TURBO</text>
<rect x="148" y="14" width="56" height="18" rx="3" fill="none" stroke="#a6501a" stroke-width="1"/><text x="176" y="27" text-anchor="middle" font-size="10.5" font-weight="700" fill="#a6501a">PRUEBA</text>
<rect x="236" y="14" width="60" height="18" rx="3" fill="none" stroke="#555" stroke-width="1"/><text x="266" y="27" text-anchor="middle" font-size="10.5" fill="#555">SF 1.5.0</text>
<rect x="22" y="38" width="52" height="18" rx="3" fill="none" stroke="#bbb" stroke-width="1"/><text x="48" y="51" text-anchor="middle" font-size="10.5" fill="#555">1h 05m</text>
<rect x="80" y="38" width="72" height="18" rx="3" fill="none" stroke="#bbb" stroke-width="1"/><text x="116" y="51" text-anchor="middle" font-size="10.5" fill="#555">12 prompts</text>
<rect x="22" y="62" width="150" height="18" rx="3" fill="none" stroke="#bbb" stroke-width="1"/><text x="30" y="75" font-size="10.5" fill="#555">feature/219-actualizar…</text>
<text x="24" y="106" font-size="11.5" font-weight="700" fill="#a16207">▶ 219 Actualizar Cómo funciona…</text>
<text x="38" y="124" font-size="10.5" fill="#888">✓ Reflejar la orquestación</text>
<text x="38" y="140" font-size="10.5" fill="#555">· Activar rama para poder probar</text>
<text x="38" y="156" font-size="10.5" fill="#555">· Cerrar la tarea</text>
<text x="24" y="196" font-size="11.5" fill="#555">▸ Pendientes · 4</text>
<text x="24" y="222" font-size="11.5" fill="#555">▸ En observación · 1</text>
<text x="24" y="248" font-size="11.5" fill="#555">▸ Cerradas · 3</text>
<text x="24" y="274" font-size="11.5" fill="#555">▸ Propuestas · 25</text>
<rect x="17" y="9" width="284" height="76" rx="4" fill="none" stroke="#a6501a" stroke-width="2"/>
<line x1="304" y1="46" x2="336" y2="46" stroke="#a6501a" stroke-width="2"/>
<text x="344" y="44" font-size="15" font-weight="700" fill="#004d47">Cabecera</text>
<text x="344" y="62" font-size="12.5" fill="#555">publicar, actualizar, TURBO,</text>
<text x="344" y="78" font-size="12.5" fill="#555">versión, duración y rama</text>
<rect x="17" y="92" width="284" height="72" rx="4" fill="none" stroke="#a6501a" stroke-width="2"/>
<line x1="304" y1="128" x2="336" y2="128" stroke="#a6501a" stroke-width="2"/>
<text x="344" y="126" font-size="15" font-weight="700" fill="#004d47">En curso</text>
<text x="344" y="144" font-size="12.5" fill="#555">la tarea en amarillo y sus pasos</text>
<rect x="17" y="178" width="284" height="124" rx="4" fill="none" stroke="#a6501a" stroke-width="2"/>
<line x1="304" y1="240" x2="336" y2="240" stroke="#a6501a" stroke-width="2"/>
<text x="344" y="238" font-size="15" font-weight="700" fill="#004d47">Tareas</text>
<text x="344" y="256" font-size="12.5" fill="#555">un solo bloque, en el orden</text>
<text x="344" y="272" font-size="12.5" fill="#555">del ciclo de las tareas</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Esquema del panel en la SF, con una tarea en curso y las secciones plegadas.</figcaption>
</figure>

**La cabecera.** Arriba van RELEASE, que publica; TURBO, que pide a Claude poner en curso las tareas que no necesitan al propietario y lanzar sus subagentes; y, solo en la SF, PRUEBA, el modo prueba. A la derecha, la etiqueta `SF` con la versión del plugin que corre, en el color de las sesiones del proyecto. ACTUALIZAR o REFRESCAR salen a la izquierda cuando hacen falta (en «Publicación del plugin»). Debajo van la duración de la sesión, los prompts enviados y la rama activa. Los avisos se turnan con la cabecera, en un bloque blanco.

**En curso.** En amarillo, las tareas en curso con sus pasos, la tocada la última arriba. Un ● verde dice que su subagente trabaja, y rojo, que espera.

**Tareas.** Un solo bloque de secciones plegables, en el orden del ciclo: **Pendientes**, **En observación**, **Cerradas** y **Propuestas**. Las propuestas son las de `sf/propuestas.md` del proyecto, o `docs/propuestas.md` en la SF.

**Las órdenes, en etiquetas.** Al desplegar una tarea, su primera fila lleva sus órdenes con su nombre («Las órdenes de cada tarea, en un menú de etiquetas»). Primero las de la tarea: Activar rama, Cerrar, A observación, Redescribir, A propuesta y, en rojo, Eliminar, Descartar o Revertir. Después, las de sus pasos: Separar pasos y Paso +. Las que piden confirmación lo hacen en la misma etiqueta: «¿Cerrar? sí». Una propuesta pasa a la cola con «A Pendientes». En un paso, «?» pide a Claude que lo explique y «×» lo quita.

Lo hacen sin Claude, con git, la cola y los comandos de Claude Code. Cada cambio de estado se explica en [Cómo funcionan los estados](como-funcionan-los-estados.html).

**Los comandos.** Todos los de la SF empiezan por `sf_`, salvo `/sf`, que abre el panel («Los comandos de la SF empiezan por sf_»). `/sf_paso` añade un paso a la tarea en curso; `/sf_split` separa pasos de una tarea en una nueva; `/sf_fusionar` junta tareas; `/sf_redescribir` pide a Claude que vuelva a redactar una descripción; `/sf_config` pide a Claude cambiar la configuración del proyecto; y `/sf_prueba`, solo en la SF, cambia el modo prueba sin el panel.

**El control.** El mod controla que cada sesión modifique un solo proyecto. Bloquea, con el motivo, la escritura de archivos en otro proyecto, también en la SF: ningún proyecto escribe en ella («Sin registro ni mejoras de la SF desde otros proyectos»). Un worktree cuenta como su repositorio. Y no deja que un subagente escriba la cola. El mod lee `.sf/` al abrir la sesión, al acabar cada turno y tras cada herramienta que puede escribir. Cada minuto relee los subagentes y comprueba la versión instalada. Solo escribe cuando lo pide el propietario.

El detalle de cada parte, el control, el código y el historial de versiones están en [Cómo funciona el panel](como-funciona-el-panel.html).

## Flujo de trabajo en un proyecto

Al abrir una sesión en el proyecto, el mod lee `.sf/`, abre el panel y entrega las reglas y la orquestación. Si el proyecto sigue la metodología, Claude usa la skill `sf:metodologia`, que le indica qué sección del método leer según el momento. En cada fase trabaja con la skill que toca: `sf:documento_vision`, `sf:diseno_interfaz`, `sf:definicion_tecnica`…

**La cola y las tareas.** Toda petición del propietario, y todo bug que se detecte, va a la cola en cuanto llega, con `cola.py`. Se trabaja siempre bajo una tarea en curso. El principal habla con el propietario y lleva la cola; cada tarea en curso tiene su subagente, que hace todo su trabajo en su worktree, con una rama auxiliar `sub-NN`. `cola.py encargo N` le escribe la parte fija del encargo. Las reglas, en `sf:orquestacion`; los estados y las órdenes, en `sf:flujo_tareas`.

**La SF guía.** Además de hacer lo que se le pide, el principal observa las tareas, el proyecto y al propietario, y sugiere cómo avanzar mejor, en una línea y con la orden lista («La SF guía el desarrollo: observa y sugiere cómo avanzar»). Por ejemplo, `cola.py lista` da de cada tarea `pasos hechos/total`, contando solo los de trabajo, sin los de cierre ni las ayudas de prueba. Si una tarea crece mucho, el principal valora sugerir partirla o cerrar lo hecho, con sus `/sf_split`. Sugerir no es hacer: nada se parte, se cierra ni se reordena sin el OK del propietario.

**Tipos de tarea.** Cada tarea tiene un tipo, uno de siete, en tres familias: **código** (implementar y corregir), **deliberativas** (investigar, deliberar y diseñar) y **documentales** (especificar y documentar). Hoy el tipo da el prefijo del squash cuando los commits son conventional o propios: `feat`, `fix` o `docs`; sin tipo, `chore`. Cómo usa el repositorio cada familia y cómo se cierra está decidido y aún sin aplicar (al final, «Decidido y aún sin aplicar»). El análisis, en el informe «Tipos de tarea».

**Los pasos de cierre.** Una tarea lleva dos pasos de cierre desde que entra en curso: «Activar rama para poder probar» y «Cerrar la tarea» («Los pasos de cierre, desde que la tarea entra en curso»). No se quitan, y los pasos nuevos van antes de ellos. Si se añade trabajo con la rama ya activada, «Activar rama» vuelve a pendiente, para probar otra vez.

**La prueba.** «Activar rama» integra `develop` en la rama de la tarea y la activa, para probar con lo último. Si choca, no la activa y dice qué archivos chocan. Detrás puede haber ayudas de prueba, que Claude planifica cuando puede («Ayudas de prueba: tras activar la rama y no obligatorias para cerrar»): salen como «(opcional)», no cuentan para cerrar y no devuelven «Activar rama» a pendiente.

**El cierre.** Cerrar entra la rama en `develop` por squash, con su commit, y lo sube al remoto. «A observación» cierra igual, pero deja la tarea en observación: se vigila un tiempo y después se cierra, si va bien, o se revierte, si va mal («En observación, sin alias ni rastros»). Cerrar se niega si el subagente tiene trabajo sin traer a la rama. Al cerrar, `cola.py` quita el worktree del subagente y borra su rama auxiliar, sin forzar: lo que quede con cambios se avisa («cola.py recoge el subagente al dejar la tarea sin él»). Descartar, en cambio, lo borra todo.

**Las decisiones.** Lo que decide el propietario se registra en cuanto se toma, con `cola.py decision "Título" --archivo RUTA [--push]`. La orden da el número, escribe el archivo, rehace el índice y hace el commit «Decisión NNN: Título» en `develop`, aunque la rama activa sea otra, sin cambiarla («Las decisiones se guardan en develop aunque la rama activa sea otra»). No toca la cola.

**Lo que es de la SF.** En un proyecto solo se anotan propuestas de ese proyecto («Un proyecto solo anota propuestas suyas»). Si algo de la SF falla, sobra o falta, Claude lo dice en una línea y no lo anota ni en la cola ni en las propuestas del proyecto. Llevarlo a la SF es cosa del propietario, en una sesión de la SF.

## Flujo de mejora de la SF

La SF mejora con el uso. Ninguna mejora salta de la idea al código: pasa por una propuesta y por una decisión del propietario.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 44 560 356" width="100%" role="img" aria-label="Flujo de mejora de la SF, de la detección a la versión publicada" style="font-family:var(--fuente-texto);display:block">
<line x1="34" y1="66" x2="34" y2="346" stroke="#b2deda" stroke-width="2"/>
<circle cx="34" cy="66" r="7" fill="#fff" stroke="#1f812d" stroke-width="2"/>
<text x="56" y="64" font-size="14.5" font-weight="700" fill="#004d47">Se detecta, en la SF o en otro proyecto</text>
<text x="56" y="82" font-size="12.5" fill="#555">desde otro, el propietario lo trae a una sesión de la SF</text>
<path d="M50,128 v16 a10,4 0 0 0 20,0 v-16" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/><ellipse cx="60" cy="128" rx="10" ry="4" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<circle cx="34" cy="136" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/>
<text x="82" y="134" font-size="14.5" font-weight="700" fill="#004d47">docs/propuestas.md</text>
<text x="82" y="152" font-size="12.5" fill="#555">lo que aún no está decidido; nada se aplica</text>
<rect x="56" y="172" width="196" height="24" rx="12" fill="#be185d"/>
<text x="154" y="188" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">el propietario decide</text>
<path d="M50,208 v16 a10,4 0 0 0 20,0 v-16" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/><ellipse cx="60" cy="208" rx="10" ry="4" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<circle cx="34" cy="216" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/>
<text x="82" y="214" font-size="14.5" font-weight="700" fill="#004d47">docs/decisiones/</text>
<text x="82" y="232" font-size="12.5" fill="#555">con su porqué, a develop con cola.py decision</text>
<circle cx="34" cy="282" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/>
<text x="56" y="280" font-size="14.5" font-weight="700" fill="#004d47">Aplicada en una tarea</text>
<text x="56" y="298" font-size="12.5" fill="#555">en su rama, con su prueba y su squash a develop</text>
<circle cx="34" cy="346" r="7" fill="#00726b"/>
<text x="56" y="344" font-size="14.5" font-weight="700" fill="#004d47">Versión nueva del plugin</text>
<text x="56" y="362" font-size="12.5" fill="#555">RELEASE la publica; ACTUALIZAR la instala</text>
<text x="34" y="392" font-size="12.5" font-style="italic" fill="#888">si no toca el plugin, basta con el squash a develop</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">La decisión del propietario es la única puerta entre proponer y cambiar.</figcaption>
</figure>

**De dónde viene.** En la SF, una mejora es una petición más: va a la cola si ya está clara, o a `docs/propuestas.md` si hay que decidirla. Desde otro proyecto no se escribe nada en la SF: Claude dice en una línea que es de la SF, y el propietario la trae a una sesión de la SF («Sin registro ni mejoras de la SF desde otros proyectos», precisada por «Un proyecto solo anota propuestas suyas»). Con el kanban conectado, la tarea permanente **Mejorar la Software Factory**, del proyecto **SoftwareFactory**, las recogerá.

**La propuesta.** En `docs/propuestas.md` la mejora se convierte en una propuesta: el cambio concreto, su beneficio, su impacto y cómo se comprobará. Ahí se detiene hasta que el propietario la aprueba, la ajusta o la descarta. El panel la enseña en Propuestas, y «A Pendientes» la pasa a la cola como tarea. Registrar o preparar una propuesta no autoriza aplicarla; una instrucción directa del propietario sí, dentro de su alcance.

**La decisión.** Lo aprobado pasa a un archivo de `docs/decisiones/` con su porqué, registrado con `cola.py decision`. Lo descartado queda en «Descartadas», con el motivo.

**La aplicación.** Una decisión se aplica en su tarea, en la fuente: metodología, especificación, skills, plantillas o código. Si el cambio afecta al plugin, se publica una versión nueva, y cada equipo la recibe con ACTUALIZAR.

### Publicación del plugin

Se desarrolla en `develop`; `main` es lo que instalan los proyectos.

1. Cada tarea, en su rama `feature/NN-nombre`, creada desde `develop` con `cola.py rama` antes de tocar el primer activo. Su subagente trabaja en su worktree, con su rama auxiliar.
2. Probar en la rama con «Activar rama» y el plugin en **modo prueba** (abajo).
3. Comprobar con `claude plugin validate plugins/sf` y las pruebas de `plugins/sf/tests/`.
4. Con el OK del propietario, Cerrar: squash de la rama a `develop`, un commit por tarea con sus pasos en el cuerpo y «(N)» al final del título, y push de `develop`. Cada decisión es un archivo propio, así que dos ramas no chocan al añadirlas. El índice, `docs/decisiones/README.md`, se junta sin choques (`merge=union` en `.gitattributes`) y se regenera con `tools/indice_decisiones.py`.
5. Publicar con **RELEASE**. La versión actual es la del último tag `vX.Y.Z`. El primer clic ofrece las tres siguientes (patch, minor y major) y el segundo confirma la elegida, avisando de las tareas que quedan en observación. Sube la versión de los manifiestos de la configuración, en la SF el `plugins/sf/.claude-plugin/plugin.json`, en un commit «sf X.Y.Z» en `develop`. Pasa `develop` a la rama de publicación (`rama_main`) por fast-forward, la marca con el tag y hace push de las dos ramas y el tag al remoto configurado. Si algo no está en orden, no publica y dice cómo arreglarlo. En los proyectos es igual, con su commit «vX.Y.Z».
6. Actualizar la copia instalada con **ACTUALIZAR**, en rojo, que sale cuando hay una versión publicada más nueva. Refresca el catálogo (`claude plugin marketplace update softwarefactory`), actualiza el plugin en cada scope que usa el proyecto e instala las dependencias que falten, una orden por plugin, antes de pedir reiniciar. Si alguna no se instala, da sus órdenes y no sigue. Se apaga con `"automatizaciones": {"dependencias_al_actualizar": false}`: entonces solo da las órdenes.

**ACTUALIZAR y REFRESCAR.** Son dos botones para dos casos («ACTUALIZAR y REFRESCAR: dos botones para dos casos»). ACTUALIZAR sale cuando hay una versión publicada sin instalar. REFRESCAR sale cuando la instalada es más nueva que la que corre la sesión, porque la actualizó otra sesión: instala las dependencias que falten y recarga el plugin. Con REFRESCAR sale también un aviso: «Esta sesión usa la SF X y está instalada la Y: pulsa REFRESCAR» («El panel avisa cuando la sesión usa un plugin más viejo que el instalado»). La versión publicada se mira al empezar, cada 5 minutos, con `/sf` y tras RELEASE; la instalada, cada minuto. Pulsar la etiqueta `SF` dice cuánto falta para la próxima comprobación.

Los cambios que no tocan el plugin (especificación, visiones, decisiones, propuestas) solo necesitan el squash a `develop`; llegan a `main` con la siguiente publicación.

**Modo prueba** (solo en la SF). Ver un cambio del plugin sin commit ni publicación. En este repositorio, la cabecera del panel lleva la etiqueta PRUEBA: atenuada, se usa el plugin publicado; en naranja, la copia de trabajo de `plugins/sf`. Un clic, o `/sf_prueba`, cambia de uno a otro: el mod escribe en `.claude/settings.local.json` (fuera de git) qué plugin está activo en este proyecto, `sf@softwarefactory-dev` o `sf@softwarefactory`, y lanza `/reload-plugins`. En modo prueba, cada retoque se ve con `/reload-plugins`, sin subir la versión. Al entrar en una sesión y al cerrarla, siempre desactivado: el mod lo apaga una vez por sesión y, si la sesión arrancó con la copia de trabajo, recarga el publicado. La sesión que ya lo apagó queda en `.sf/prueba.json`, fuera de git, porque `/reload-plugins` vuelve a pasar por el arranque.

Preparación, una vez por equipo: el catálogo local `softwarefactory-dev`, en `D:/Projectes/.claude-plugin/marketplace.json`, fuera del repositorio, con el plugin `sf` en `./SoftwareFactory/plugins/sf`. Claude Code carga en su sitio, sin copiarlo a la caché, el plugin de un catálogo de carpeta. No acepta la ruta absoluta, la que sube de carpeta ni un enlace, y dos catálogos no pueden llamarse igual: por eso está en la carpeta de arriba. Después, en el repositorio: `claude plugin marketplace add D:/Projectes --scope local` y `claude plugin install sf@softwarefactory-dev --scope local`. Sin el catálogo registrado, el panel no muestra la etiqueta. Probado y descartado: la variable `CLAUDE_CODE_PLUGIN_DIRS` en los ajustes del proyecto, que no carga la copia de trabajo, ni con `/reload-plugins` ni al reiniciar.

## Decidido y aún sin aplicar

Estas decisiones cambian piezas de este mapa, pero el código de la 1.5.0 aún no las lleva. Hasta que se apliquen, vale lo descrito arriba.

- **Una sola sesión con la SF por proyecto.** La segunda sesión en el mismo proyecto arrancará con la SF apagada, con un latido para saber cuál la tiene y `/sf_forzar_activa` y `/sf_forzar_inactiva` para pasarla. Hoy dos sesiones pueden tener la SF activa a la vez.
- **El repositorio según el tipo de tarea.** Las de código seguirán como hoy. Un documento nuevo, también el informe de una deliberativa, irá a `develop` en cada vuelta, sin rama, con su respaldo en `_respaldo/` y su HTML regenerado, y se cerrará con la aprobación del propietario, sin observación. Las deliberativas se cerrarán con «Finalizar deliberación», y cada familia tendrá su agente.
- **Los documentos de la SF, en `sf/`, también en la SF.** La propia SF pasará `docs/propuestas.md`, sus informes y `docs/decisiones/` a `sf/`, como los demás proyectos.
- **Cada cambio de un `.md` regenera su HTML,** con una orden única que elija el generador.

## Índice de consulta

<dl class="faq">
<dt>¿Cómo se hace algo en un proyecto?</dt><dd>Metodología (skill <code>sf:metodologia</code>)</dd>
<dt>¿Qué hace el principal con cada mensaje?</dt><dd>Skill <code>sf:orquestacion</code></dd>
<dt>¿Qué falta por construir en la SF?</dt><dd>Especificación, próximos pasos</dd>
<dt>¿Por qué se hizo así?</dt><dd><code>docs/decisiones/</code></dd>
<dt>¿Cómo se registra una decisión y dónde se aplica?</dt><dd><code>docs/mejora-continua-a-la-software-factory.md</code> y <code>cola.py decision</code></dd>
<dt>¿Qué ideas esperan aprobación?</dt><dd><code>docs/propuestas.md</code>, y la sección Propuestas del panel</dd>
<dt>¿Qué hace el panel y cómo evoluciona?</dt><dd>«El panel de la SF», en este documento, y <code>docs/como-funciona-el-panel.md</code></dd>
<dt>¿Cómo cambia de estado una tarea?</dt><dd><code>docs/como-funcionan-los-estados.md</code> y la skill <code>sf:flujo_tareas</code></dd>
<dt>¿Cómo se pone un proyecto bajo la SF?</dt><dd>«Incorporación de un proyecto a la SF», en este documento, y la skill <code>sf:incorporar_proyecto_a_sf</code></dd>
<dt>¿Cómo se configura un proyecto?</dt><dd>Su <code>.sf/proyecto.json</code>, que se cambia con <code>/sf_config</code>; el detalle, en <code>plugins/sf/README.md</code> y en el informe «Configuración inicial»</dd>
<dt>¿Qué reglas recibe un proyecto?</dt><dd><code>plugins/sf/templates/claude-sf.md</code> y <code>claude-sf-metodologia.md</code>, que entrega el mod</dd>
<dt>¿En qué punto está un proyecto?</dt><dd>Su <code>.sf/estado.json</code>, si sigue la metodología, o <code>/sf</code> dentro de Claude Code</dd>
<dt>¿Qué decidió el propietario en un proyecto?</dt><dd>La carpeta <code>sf/decisiones/</code> de ese proyecto</dd>
<dt>¿Qué carpetas lleva un proyecto?</dt><dd>Metodología, sección 6, y las plantillas del plugin</dd>
<dt>¿Cómo se dibuja un diagrama?</dt><dd>Guía de diagramas en SVG (<code>plugins/sf/skills/metodologia/references/diagramas-svg.md</code>); nunca ASCII ni mermaid</dd>
<dt>¿De dónde viene una skill?</dt><dd>El <code>ORIGIN.md</code> de la skill; las externas que se usan tal cual, en las <code>dependencies</code> del <code>plugin.json</code></dd>
<dt>¿Cómo se instala o se publica el plugin?</dt><dd><code>plugins/sf/README.md</code> y este documento</dd>
<dt>¿Cómo empieza Claude a trabajar en la SF?</dt><dd><code>CLAUDE.md</code> del repositorio</dd>
</dl>

## Cuestiones pendientes de decisión

Está en [propuestas](propuestas.md). Lo que más afecta a este mapa:

- **Procedimiento de instalación del plugin**, más allá de las órdenes de `plugins/sf/README.md`.
- **Cómo se instala JKanban dentro de la SF.**
- **Historial de versiones del plugin** (CHANGELOG).
- **Organización del repositorio de la SF.**
