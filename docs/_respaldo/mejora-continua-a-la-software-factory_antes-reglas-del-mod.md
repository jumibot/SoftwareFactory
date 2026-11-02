<!-- destino: proyecto -->
<!-- herramientas: -notas -nota-texto -nota-seccion -nota-global -->
# Mejora continua a la Software Factory

Este documento describe el ciclo de mejora continua de la SF. Cuenta cómo se usa, qué se observa y dónde se anota, y cómo lo decide el propietario de la Software Factory. Después sigue a la decisión hasta los proyectos: dónde se registra, con qué formato, en qué componentes se aplica y cuándo los lee Claude. No contiene reglas: están en la metodología (secciones 2, 6 y 11), en la plantilla `claude-sf.md` y en el `CLAUDE.md` de la SF. Aquí solo se dice dónde buscarlas.

Las decisiones son la forma en que la SF evoluciona y se corrige. Cada una nace de usarla, en la propia SF o al desarrollar una aplicación. Puede responder a una necesidad nueva (evolutiva) o a algo que falla, sobra o estorba (correctiva). No son un trámite aparte, sino parte de su mejora continua (metodología, 11). Lo observado va al registro de uso y a las propuestas. Lo que decide el propietario de la Software Factory se registra aquí con su porqué. Después se aplica a sus componentes y llega a los proyectos con la siguiente versión.

**Estado:** 29 de octubre de 2026, plugin `sf` 0.34.3.

## El ciclo de mejora

La SF mejora usándola. Cada vuelta del ciclo empieza en el uso y termina en una versión publicada, que se vuelve a usar:

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 474" width="100%" role="img" aria-label="Ciclo de mejora continua de la SF: usar, observar y anotar, decidir, aplicar en una tarea, probar y cerrar, publicar una versión y volver a usar" style="font-family:var(--fuente-texto);display:block">
<defs><marker id="flecha-ciclo" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#00726b"/></marker></defs>
<circle cx="40" cy="38" r="15" fill="none" stroke="#1f812d" stroke-width="2"/><text x="40" y="43" text-anchor="middle" font-size="14" font-weight="700" fill="#1f812d">1</text>
<text x="72" y="36" font-size="15" font-weight="700" fill="#1f812d">Usar la SF</text><text x="72" y="56" font-size="12.5" fill="#555">en la propia SF y al desarrollar cada proyecto</text>
<line x1="40" y1="55" x2="40" y2="95" stroke="#00726b" stroke-width="2" marker-end="url(#flecha-ciclo)"/>
<circle cx="40" cy="112" r="15" fill="none" stroke="#00726b" stroke-width="2"/><text x="40" y="117" text-anchor="middle" font-size="14" font-weight="700" fill="#00726b">2</text>
<text x="72" y="110" font-size="15" font-weight="700" fill="#00726b">Observar y anotar</text><text x="72" y="130" font-size="12.5" fill="#555">registro de uso, errores en Pendientes, propuestas</text>
<line x1="40" y1="129" x2="40" y2="169" stroke="#00726b" stroke-width="2" marker-end="url(#flecha-ciclo)"/>
<circle cx="40" cy="186" r="15" fill="none" stroke="#be185d" stroke-width="2"/><text x="40" y="191" text-anchor="middle" font-size="14" font-weight="700" fill="#be185d">3</text>
<text x="72" y="184" font-size="15" font-weight="700" fill="#be185d">Decidir</text><text x="72" y="204" font-size="12.5" fill="#555">el propietario de la SF: evolutivo o correctivo</text>
<line x1="40" y1="203" x2="40" y2="243" stroke="#00726b" stroke-width="2" marker-end="url(#flecha-ciclo)"/>
<circle cx="40" cy="260" r="15" fill="none" stroke="#00726b" stroke-width="2"/><text x="40" y="265" text-anchor="middle" font-size="14" font-weight="700" fill="#00726b">4</text>
<text x="72" y="258" font-size="15" font-weight="700" fill="#00726b">Aplicar en una tarea</text><text x="72" y="278" font-size="12.5" fill="#555">rama feature/NN: decisiones, metodología, plugin</text>
<line x1="40" y1="277" x2="40" y2="317" stroke="#00726b" stroke-width="2" marker-end="url(#flecha-ciclo)"/>
<circle cx="40" cy="334" r="15" fill="none" stroke="#00726b" stroke-width="2"/><text x="40" y="339" text-anchor="middle" font-size="14" font-weight="700" fill="#00726b">5</text>
<text x="72" y="332" font-size="15" font-weight="700" fill="#00726b">Probar y cerrar</text><text x="72" y="352" font-size="12.5" fill="#555">con su OK, squash en develop</text>
<line x1="40" y1="351" x2="40" y2="391" stroke="#00726b" stroke-width="2" marker-end="url(#flecha-ciclo)"/>
<circle cx="40" cy="408" r="15" fill="none" stroke="#1f7a7a" stroke-width="2"/><text x="40" y="413" text-anchor="middle" font-size="14" font-weight="700" fill="#1f7a7a">6</text>
<text x="72" y="406" font-size="15" font-weight="700" fill="#1f7a7a">Publicar una versión</text><text x="72" y="426" font-size="12.5" fill="#555">develop a main con tag vX.Y.Z; llega a los proyectos</text>
<path d="M 470 408 H 530 V 38 H 478" fill="none" stroke="#00726b" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#flecha-ciclo)"/>
<text x="522" y="223" font-size="12.5" fill="#555" text-anchor="middle" transform="rotate(-90 522 223)">otra vuelta: el uso de la versión nueva</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Cada versión publicada se vuelve a usar, y lo que se observa al usarla empieza otra vuelta.</figcaption>
</figure>

Todo empieza al **usar la SF**, al construir la propia SF o al desarrollar un proyecto con ella. Al usarla aparece lo que falta, lo que falla y lo que estorba. Eso **se anota** en cuanto aparece, sin parar el trabajo. Lo observado va al registro de uso; un error, como tarea a Pendientes; lo que hay que pensar antes de decidir, a propuestas. Si se observa en otro proyecto, se anota igual en la SF, con ese proyecto como origen. El cambio se hace después, en una sesión de la SF.

Lo anotado no cambia nada hasta que **el propietario de la Software Factory lo decide**. La decisión puede ser evolutiva, si añade algo que la SF no tenía (el botón para descartar una tarea). O correctiva, si arregla algo que ya hay (las tablas que partían las palabras). En los dos casos se convierte en una tarea, con su propia rama.

En esa rama **se aplica** la decisión. Se registra en un archivo nuevo de `docs/decisiones/` y se lleva a los componentes que la recogen: la metodología, la plantilla o el código del plugin. Después **se prueba**. Lo que salga al probar se corrige en la misma rama, como un paso más de la tarea. Cuando el propietario de la Software Factory la da por probada, la tarea entra en `develop`.

Lo que está en `develop` llega a los proyectos al **publicar una versión** del plugin. Desde entonces se usa en todos ellos. Lo que se observe al usarlo empieza la vuelta siguiente.

Los apartados que siguen recorren el ciclo con detalle. Cuentan cómo se distingue lo decidido de lo propuesto, cuándo y cómo se registra una decisión, dónde se aplica, cómo se prueba y cómo llega a los proyectos.

## Decisión, propuesta, preferencia y pendiente

La SF separa lo decidido de lo que aún no lo está. Cada tipo tiene su sitio y no se mezcla con los demás.

| Tipo | Qué es | Dónde va |
| --- | --- | --- |
| Decisión | Lo que el propietario de la Software Factory ha decidido, con su porqué. | Un archivo en `docs/decisiones/`. La regla que sale de ella va a la metodología o a la especificación, marcada como acuerdo o norma del propietario, con fecha. |
| Propuesta | Un cambio que alguien plantea y el propietario de la Software Factory aún no ha decidido. | `docs/propuestas.md`, con número fijo (P01, P02…). Una mejora de la SF va además al proyecto SoftwareFactory del kanban. |
| Preferencia | Una opción favorita que se confirma en cada proyecto. | Metodología y especificación, marcada como preferencia (por ejemplo, metodología, 5). |
| Pendiente | Una decisión o un dato que falta. | Al final de la metodología (sección 10) y de la especificación (sección 4). En un proyecto, en `pendientes` de `.sf/estado.json`. |

**Un ejemplo de cada tipo:**

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,26rem),1fr));gap:.9rem;margin:1rem 0 1.4rem;"><div class="ficha" style="margin:0;"><p class="ficha-titulo">Decisión · Una rama de feature por tarea</p><p style="margin:0 0 .45rem;">Cada tarea tiene su rama <code>feature/NN-nombre</code> desde <code>develop</code>; entra en <code>develop</code> por squash cuando está probada. Su regla está en la metodología, 2, «Ramas por tarea».</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/decisiones/082-2026-10-29-una-rama-de-feature-por-tarea.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Propuesta · P03 Perfil para productos de software y hardware</p><p style="margin:0 0 .45rem;">Añadir a la metodología un perfil «gemelo digital primero», a partir de SmartColdBox. Nació en otro proyecto y se anotó en la SF con su origen.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/propuestas.md</code>, P03</p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Preferencia · Frontend web: React</p><p style="margin:0 0 .45rem;">React es la favorita para el frontend web. Un proyecto puede elegir otra si lo justifica, y lo anota en sus decisiones.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);">Metodología, 5</p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Pendiente · Ejecutor de migraciones</p><p style="margin:0 0 .45rem;">Elegir el ejecutor de migraciones y las versiones de esquema soportadas.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);">Metodología, 10</p></div></div>

En la metodología y en la especificación solo hay acuerdos, preferencias y pendientes. Los dos documentos explican al principio cómo distinguirlos. Lo que empieza por «Ejemplo:» ilustra una regla y no manda nada. Una propuesta aprobada pasa a `docs/decisiones/` y sale de las pendientes. Una descartada queda en «Descartadas», con el motivo. Registrar una propuesta no autoriza aplicarla. Una instrucción directa del propietario de la Software Factory sí, dentro de su alcance (`CLAUDE.md` de la SF, reglas de trabajo).

## Cuándo se registra

Una decisión se registra en cuanto se toma. Suele ser en el chat, mientras se define una tarea. El agente principal es quien habla con el propietario de la Software Factory. Él la anota en la tarea de la cola (`.sf/peticiones.json`), con sus palabras.

El archivo de la decisión se escribe en la rama de la tarea, `feature/NN-nombre`, junto con los cambios que la aplican. La escribe quien hace la tarea: el principal o el subagente, a partir de lo anotado en la cola. La decisión entra en `develop` con el squash de la tarea, cuando el propietario de la Software Factory la da por probada. Hasta entonces solo está en la rama. Si la tarea se descarta, la decisión se va con ella. Una decisión escrita en el repositorio es un activo: su tarea ya no se puede eliminar, solo descartar o revertir (metodología, 2).

<div class="ejemplo"><p>Mientras se escribía este documento (tarea 91), el propietario de la Software Factory dijo en el chat: «en las tareas de creación y/o mejora de docs en las que se usen skill se podrán mejorar estos como pasos propios de la tarea».</p><p>El principal lo anotó en la tarea 91 de la cola, con esas palabras. En la rama <code>feature/91-gestion-decisiones</code> escribió la entrada «Mejorar la skill que se usa es un paso» en las decisiones. En la misma rama la aplicó a la metodología, a la plantilla y al <code>CLAUDE.md</code>.</p><p>La decisión entró en <code>develop</code> con el squash de la 91, cuando el propietario de la Software Factory la dio por probada.</p></div>

Las reglas están en la metodología, sección 2 («Orquestación con subagentes» y «Ramas por tarea»). También en las decisiones «Llevar cada decisión a los documentos en cuanto se toma» y «El principal orquesta; los subagentes ejecutan».

## Formato

Cada decisión es un archivo de `docs/decisiones/`, `NNN-AAAA-MM-DD-titulo.md`: el número de orden total (el siguiente al más alto), la fecha del origen y el título sin tildes ni signos. Empieza por `# Título` y lleva estos campos, solo los que hacen falta:

- **Origen:** proyecto, fecha, tarea y palabras del propietario de la Software Factory, entre comillas latinas.
- **Contexto:** el problema que llevó a decidir.
- **Opciones:** las que se valoraron, si las hubo.
- **Decisión:** lo decidido y por qué.
- **Consecuencias:** lo que cambia, lo que queda pendiente y lo que se resuelve más adelante.
- **Aplicada en:** los componentes que la recogen: secciones de la metodología, plantilla, `CLAUDE.md`, especificación, archivos del plugin y documentos.

El **índice** es `docs/decisiones/README.md`: un párrafo que dice qué recoge y dónde están las reglas, la forma de registrar una decisión y una tabla de dos columnas, fecha y decisión con enlace a su archivo, la más reciente arriba. La tabla no se escribe a mano: `python -I -X utf8 plugins/sf/tools/indice_decisiones.py docs/decisiones` la regenera, sin Claude, y conserva lo que va antes de «Índice». Así, dos tareas que añaden decisiones no chocan al juntarse: cada una trae su archivo, y el índice se junta con `merge=union` (`.gitattributes`) y se regenera.

Una decisión no se borra cuando otra la cambia. La nueva lo dice con «Sustituye a…» (la cambia) o «Precisa…» (la concreta sin anularla), y el título de la anterior. En la anterior se marca el cambio con una línea bajo el título: «**Sustituida** el …» o «**Sustituida en parte** por …». También puede ir, junto a la frase afectada, una nota en cursiva: «*Sustituido: …*» o «*Precisado: …*». En el índice, la sustituida en parte lleva detrás «(sustituida en parte)». Así se ve qué rige hoy sin perder el porqué de lo anterior.

Ejemplo: una decisión real, que precisa otra anterior.

```markdown
# El botón de Cerradas se llama «limpiar»

- **Origen:** SoftwareFactory, 2026-10-29, tarea 114. El propietario, con una captura de «quitar las probadas (1)»: «llámale a este botón limpiar».
- **Decisión:** el botón de la fila del título de Cerradas dice «limpiar (N)»; hace lo mismo que antes. Precisa «Cerradas: botón para quitar las probadas».
- **Aplicada en:** `plugins/sf/hooks/panel.tsx` y su prueba; `docs/como-funciona-el-panel.md`.
```

Es el formato MADR mínimo que pide la metodología (sección 6) para todos los proyectos. La skill `sf:definicion_tecnica` trae la plantilla de una decisión técnica.

## Dónde se aplica

Una decisión no se queda en `docs/decisiones/`. Se aplica en el mismo momento y en la misma rama, en los componentes que la recogen. El campo «Aplicada en» los enumera. Cada componente llega a un sitio distinto, y Claude lo lee en un momento distinto.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 600" width="100%" role="img" aria-label="Recorrido de una decisión: del propietario de la Software Factory a la cola, a docs/decisiones/ en la rama de la tarea y a los componentes que la aplican; solo los del plugin llegan a los proyectos al publicar" style="font-family:var(--fuente-texto);display:block">
<defs><marker id="flecha-gd" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#00726b"/></marker><marker id="flecha-gd-v" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1f812d"/></marker></defs>
<rect x="54" y="10" width="420" height="26" rx="13" fill="#be185d"/>
<text x="264" y="28" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">el propietario de la Software Factory decide, en el chat</text>
<line x1="264" y1="36" x2="264" y2="62" stroke="#00726b" stroke-width="2" marker-end="url(#flecha-gd)"/>
<text x="276" y="54" font-size="12" fill="#00726b">al momento</text>
<rect x="14" y="66" width="500" height="52" rx="10" fill="none" stroke="#b2deda" stroke-width="1.5"/>
<path d="M30,80 v16 a10,4 0 0 0 20,0 v-16" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/><ellipse cx="40" cy="80" rx="10" ry="4" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<text x="62" y="88" font-size="14.5" font-weight="700" fill="#004d47">Tarea de la cola: .sf/peticiones.json</text>
<text x="62" y="106" font-size="12.5" fill="#555">el principal anota lo decidido, con sus palabras</text>
<line x1="264" y1="118" x2="264" y2="148" stroke="#00726b" stroke-width="2" marker-end="url(#flecha-gd)"/>
<text x="276" y="138" font-size="12" fill="#00726b">en la rama feature/NN-nombre</text>
<rect x="14" y="152" width="500" height="52" rx="10" fill="none" stroke="#b2deda" stroke-width="1.5"/>
<path d="M30,166 v16 a10,4 0 0 0 20,0 v-16" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/><ellipse cx="40" cy="166" rx="10" ry="4" fill="#e0f4f3" stroke="#00726b" stroke-width="1.5"/>
<text x="62" y="174" font-size="14.5" font-weight="700" fill="#004d47">docs/decisiones/</text>
<text x="62" y="192" font-size="12.5" fill="#555">con su porqué; la escribe el principal o el subagente</text>
<line x1="264" y1="204" x2="264" y2="234" stroke="#00726b" stroke-width="2" marker-end="url(#flecha-gd)"/>
<text x="276" y="224" font-size="12" fill="#00726b">se aplica en la misma tarea</text>
<rect x="14" y="238" width="500" height="106" rx="10" fill="none" stroke="#c0dada" stroke-width="1.5"/>
<text x="34" y="262" font-size="14.5" font-weight="700" fill="#1f7a7a">En el plugin sf</text>
<text x="34" y="288" font-size="12.5" font-weight="700" fill="#1f7a7a">metodología</text><text x="200" y="288" font-size="12.5" fill="#555">skill sf:metodologia</text>
<text x="34" y="310" font-size="12.5" font-weight="700" fill="#1f7a7a">plantilla claude-sf.md</text><text x="200" y="310" font-size="12.5" fill="#555">se copia a .sf/claude-sf.md</text>
<text x="34" y="332" font-size="12.5" font-weight="700" fill="#1f7a7a">código del plugin</text><text x="200" y="332" font-size="12.5" fill="#555">panel, skills y plantillas</text>
<rect x="14" y="356" width="500" height="106" rx="10" fill="none" stroke="#b2deda" stroke-width="1.5"/>
<text x="34" y="380" font-size="14.5" font-weight="700" fill="#004d47">Solo en el repositorio de la SF</text>
<text x="34" y="406" font-size="12.5" font-weight="700" fill="#00726b">CLAUDE.md de la SF</text><text x="200" y="406" font-size="12.5" fill="#555">reglas de cada sesión de la SF</text>
<text x="34" y="428" font-size="12.5" font-weight="700" fill="#00726b">especificación</text><text x="200" y="428" font-size="12.5" fill="#555">qué construir en la SF</text>
<text x="34" y="450" font-size="12.5" font-weight="700" fill="#00726b">«Cómo funciona…»</text><text x="200" y="450" font-size="12.5" fill="#555">cómo es cada componente</text>
<rect x="14" y="474" width="500" height="38" rx="10" fill="none" stroke="#bbb" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="34" y="498" font-size="12.5" font-weight="700" fill="#888">memoria de Claude</text><text x="200" y="498" font-size="12.5" fill="#888">fuera de git, por usuario y proyecto</text>
<rect x="14" y="540" width="500" height="52" rx="10" fill="none" stroke="#c0dcc4" stroke-width="1.5"/>
<text x="34" y="562" font-size="14.5" font-weight="700" fill="#1f812d">Proyectos</text>
<text x="34" y="580" font-size="12.5" fill="#555">plugin actualizado y .sf/claude-sf.md regenerado</text>
<path d="M514,290 H538 V566 H520" fill="none" stroke="#1f812d" stroke-width="1.8" marker-end="url(#flecha-gd-v)"/>
<text transform="rotate(-90 551 428)" x="551" y="428" text-anchor="middle" font-size="12" fill="#1f812d">al publicar una versión</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">Solo lo que está en el plugin llega a los proyectos; el resto se queda en la SF, y la memoria, en el equipo.</figcaption>
</figure>

Cada componente guarda una parte distinta de lo decidido. Lo que se aplica en todas las sesiones está en la plantilla y en el `CLAUDE.md`. El detalle está en la metodología, que Claude lee cuando la tarea lo pide.

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,19rem),1fr));gap:.9rem;margin:1.2rem 0 1.6rem;"><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Metodología</p><p style="margin:0 0 .45rem;"><strong>Guarda</strong> la regla completa, como acuerdo o norma del propietario con fecha, además de preferencias y pendientes.</p><p style="margin:0 0 .45rem;"><strong>La lee</strong> Claude, en la SF y en cada proyecto.</p><p style="margin:0 0 .45rem;"><strong>Se carga</strong> como skill: Claude Code tiene su descripción en todas las sesiones y Claude la carga cuando la tarea lo pide (empezar o retomar un proyecto, cambiar de fase, saber cómo se hace algo). La skill le dice qué sección leer en cada momento. En la SF, la lectura de entrada del <code>CLAUDE.md</code> pide leerla.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>plugins/sf/skills/metodologia/references/desarrollo-de-proyectos.md</code></p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Plantilla <code>claude-sf.md</code></p><p style="margin:0 0 .45rem;"><strong>Guarda</strong> las reglas que se aplican siempre en un proyecto, en un punto cada una: método, decisiones, estado, un proyecto por sesión, cola, ramas, subagentes, registro de uso, mejora continua y reglas del proyecto.</p><p style="margin:0 0 .45rem;"><strong>La lee</strong> Claude, en cada proyecto.</p><p style="margin:0 0 .45rem;"><strong>Se carga</strong> en cada sesión del proyecto: se copia a <code>.sf/claude-sf.md</code> y el <code>CLAUDE.md</code> del proyecto la importa con <code>@.sf/claude-sf.md</code>, así que Claude Code la carga como si estuviera escrita en él. La SF no la importa.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>plugins/sf/templates/claude-sf.md</code></p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Código del plugin</p><p style="margin:0 0 .45rem;"><strong>Guarda</strong> el comportamiento: lo que hace el panel, lo que bloquea el mod y lo que hacen las skills y sus plantillas.</p><p style="margin:0 0 .45rem;"><strong>Lo ve</strong> el propietario de la Software Factory, en el panel; las skills, Claude.</p><p style="margin:0 0 .45rem;"><strong>Se carga</strong> desde la copia instalada: el mod responde solo a los eventos de cada sesión, sin que Claude tenga que acordarse; las skills, cuando la tarea lo pide.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>plugins/sf/hooks/</code>, <code>plugins/sf/skills/</code>, <code>plugins/sf/templates/</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo"><code>CLAUDE.md</code> de la SF</p><p style="margin:0 0 .45rem;"><strong>Guarda</strong> la lectura de entrada y las reglas de trabajo de la SF, en una línea cada una, con la sección de la metodología donde está el detalle. Las reglas que se distribuyen están también en la plantilla.</p><p style="margin:0 0 .45rem;"><strong>Lo lee</strong> Claude, en la SF.</p><p style="margin:0 0 .45rem;"><strong>Se carga</strong> al empezar cada sesión abierta en la SF. No llega a los proyectos.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>CLAUDE.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Especificación</p><p style="margin:0 0 .45rem;"><strong>Guarda</strong> qué hay que construir en la SF para aplicar y distribuir el método (plugin, mods, skills), con acuerdos fechados y pendientes.</p><p style="margin:0 0 .45rem;"><strong>La leen</strong> Claude y el propietario de la Software Factory, en la SF.</p><p style="margin:0 0 .45rem;"><strong>No se carga sola:</strong> la lectura de entrada del <code>CLAUDE.md</code> de la SF pide leerla. Se queda en el repositorio.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/specs/funcional/software-factory.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">«Cómo funciona…»</p><p style="margin:0 0 .45rem;"><strong>Guardan</strong> cómo es cada componente después de la decisión, sin reglas: dónde está, qué hace y cómo se relaciona.</p><p style="margin:0 0 .45rem;"><strong>Los leen</strong> el propietario de la Software Factory y Claude, en la SF.</p><p style="margin:0 0 .45rem;"><strong>No se cargan solos:</strong> la lectura de entrada del <code>CLAUDE.md</code> pide leer el de la SF, y una regla de trabajo pide actualizarlos cuando cambia un componente.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/como-funciona-la-software-factory.md</code>, <code>docs/como-funciona-el-panel.md</code> y este documento</p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Memoria de Claude</p><p style="margin:0 0 .45rem;"><strong>Guarda</strong> notas de Claude para un usuario y un proyecto: contexto, preferencias y recordatorios de normas.</p><p style="margin:0 0 .45rem;"><strong>La lee</strong> Claude, en ese proyecto y en ese equipo.</p><p style="margin:0 0 .45rem;"><strong>Se carga</strong> al empezar cada sesión del proyecto: el índice, <code>MEMORY.md</code>; cada nota, cuando hace falta. Está fuera del repositorio: no es un activo, no se versiona y no llega a otros proyectos.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>~/.claude/projects/&lt;carpeta del proyecto&gt;/memory/</code></p></div></div>

Una regla que se aplica siempre se escribe en dos sitios. Completa, en la metodología. En una línea, en la plantilla y en el `CLAUDE.md` de la SF, que remiten a la sección. Por eso muchas decisiones dicen «Aplicada en: metodología, 2; plantilla `claude-sf.md`; `CLAUDE.md`». La memoria puede llevar un recordatorio de lo decidido. Pero no se versiona, así que el registro es `docs/decisiones/`. Qué va a memoria, al `CLAUDE.md` o a una skill está sin decidir (propuesta P01, bloque B).

## Cómo se prueban las mejoras

Ninguna mejora entra en `develop` sin probar. La prueba la hace el propietario de la Software Factory, en la rama de la tarea. Claude la prepara: al terminar una tarea, propone probarla y dice cómo (metodología, 2).

**Antes de la prueba, lo que comprueba Claude.** Claude ejecuta lo que puede comprobar solo. En el plugin, `claude plugin validate plugins/sf` y las pruebas automáticas, `claude plugin test plugins/sf`. En un documento, una captura del HTML, para ver que ningún texto se sale ni se solapa. Lo anota en el campo `comprobado` de la tarea, y el panel lo muestra con «✓». No sustituye la prueba del propietario de la Software Factory: la tarea sigue en Testing hasta su OK.

**Dónde se prueba.** En la carpeta principal, con la rama de la tarea activa. Solo hay una rama activa por carpeta. La P verde del panel, junto a la tarea, la activa con un clic, sin pasar por Claude. Si la rama activa tiene cambios sin commit, la P no cambia de rama y avisa. La rama de un subagente se prueba ahí también, una vez quitado su worktree. Qué se mira depende de lo que cambia:

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,19rem),1fr));gap:.9rem;margin:1rem 0 1.4rem;"><div class="ficha" style="margin:0;"><p class="ficha-titulo">Un documento</p><p style="margin:0 0 .45rem;">Se abre el HTML generado, con la rama activa. Si cambia el generador, se regenera antes.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/*.html</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">El plugin en la SF</p><p style="margin:0 0 .45rem;">El panel, los comandos y las skills se prueban con el modo prueba, que carga la copia de trabajo, y <code>/reload-plugins</code> tras cada cambio.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);">Etiqueta «prueba» de la cabecera del panel</p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">El plugin en otro proyecto</p><p style="margin:0 0 .45rem;">Si el efecto se ve en otro proyecto, se abre una sesión de ese proyecto con <code>claude --plugin-dir D:/Projectes/SoftwareFactory/plugins/sf</code>.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);">Sesión del otro proyecto</p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Una aplicación</p><p style="margin:0 0 .45rem;">En un proyecto: su rama activa y la aplicación reiniciada; con migraciones, sobre una base de pruebas, y con dependencias nuevas, instaladas antes.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);">Metodología, 2 y 8</p></div></div>

**Qué mirar.** Claude dice en el chat qué hacer y qué mirar. Lo deja también en el campo `prueba` de la tarea, que el panel muestra al desplegarla. La tarea lleva al final los pasos «Probar la tarea» y «Cerrar la tarea»: así se ve que solo falta eso.

**Si al probar hace falta un cambio**, se hace en ese momento, en la misma rama. Es un paso nuevo de la tarea, y se vuelve a probar. Si es otra cosa, va a Pendientes como tarea nueva. Si es un fallo de una tarea ya cerrada, esa tarea se reabre con su número.

**Al terminar.** Con el OK del propietario de la Software Factory («probada, ciérrala»), la tarea entra en `develop` por squash y sale de la cola. Si la deja para más tarde, queda en Testing con su `prueba`. Lo que no ha pasado la prueba no se publica.

## Cómo llega a los proyectos

Lo decidido llega a los proyectos solo al publicar el plugin. Los proyectos usan la versión publicada e instalada, nunca la copia de trabajo de la SF (especificación, sección 1).

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 440" width="100%" role="img" aria-label="Cómo llega una mejora a los proyectos: de la rama de la tarea a develop por squash, de develop a main al publicar con su tag, y del plugin actualizado a cada sesión al momento y a .sf/claude-sf.md al poner el proyecto al día; especificación, decisiones, propuestas y Cómo funciona se quedan en la SF" style="font-family:var(--fuente-texto);display:block">
<defs><marker id="fl-llega" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#00726b"/></marker><marker id="fl-llega-t" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1f7a7a"/></marker></defs>
<text x="40" y="30" font-size="15" font-weight="700" fill="#00726b">feature/NN-nombre</text>
<text x="40" y="49" font-size="12.5" fill="#555">la tarea, en su rama, probada</text>
<line x1="52" y1="60" x2="52" y2="100" stroke="#00726b" stroke-width="2" marker-end="url(#fl-llega)"/>
<text x="70" y="85" font-size="12.5" fill="#555">squash, con el OK del propietario de la SF</text>
<text x="40" y="124" font-size="15" font-weight="700" fill="#00726b">develop</text>
<text x="40" y="143" font-size="12.5" fill="#555">lo probado, aún sin publicar</text>
<line x1="52" y1="154" x2="52" y2="194" stroke="#00726b" stroke-width="2" marker-end="url(#fl-llega)"/>
<text x="70" y="179" font-size="12.5" fill="#555">publicar: sube la version y pone el tag vX.Y.Z</text>
<text x="40" y="218" font-size="15" font-weight="700" fill="#1f7a7a">main</text>
<text x="40" y="237" font-size="12.5" fill="#555">lo que usan los proyectos; los tags, el histórico</text>
<line x1="52" y1="248" x2="52" y2="300" stroke="#1f7a7a" stroke-width="2" marker-end="url(#fl-llega-t)"/>
<text x="70" y="272" font-size="12.5" fill="#555">el plugin se actualiza en el equipo</text>
<path d="M 52 286 H 312 V 300" fill="none" stroke="#1f7a7a" stroke-width="2" marker-end="url(#fl-llega-t)"/>
<text x="40" y="324" font-size="14" font-weight="700" fill="#1f812d">En cada sesión, al momento</text>
<text x="40" y="343" font-size="12.5" fill="#555">metodología, skills y mod nuevos</text>
<text x="40" y="360" font-size="12.5" fill="#555">en todos los proyectos</text>
<text x="300" y="324" font-size="14" font-weight="700" fill="#1f812d">.sf/claude-sf.md</text>
<text x="300" y="343" font-size="12.5" fill="#555">al poner el proyecto al día;</text>
<text x="300" y="360" font-size="12.5" fill="#555">el panel avisa: SF 0.13 → 0.34</text>
<rect x="30" y="384" width="500" height="44" rx="8" fill="none" stroke="#999" stroke-width="1.2" stroke-dasharray="5 4"/>
<text x="280" y="402" font-size="12.5" text-anchor="middle" fill="#555">Se quedan en la SF, sin cambiar nada en los proyectos:</text>
<text x="280" y="419" font-size="12.5" text-anchor="middle" fill="#555">especificación, decisiones, propuestas, «Cómo funciona…»</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">La plantilla de cada proyecto es la única copia que no cambia sola con el plugin.</figcaption>
</figure>

El recorrido tiene dos pasos. Primero, la tarea probada entra en `develop` por squash, con el OK del propietario de la Software Factory. Después, al publicar, se sube la `version` de `plugins/sf/.claude-plugin/plugin.json`. `develop` pasa a `main` y se marca con el tag `vX.Y.Z` (metodología, 2; «Publicación del plugin» en [Cómo funciona la Software Factory](como-funciona-la-software-factory.html#publicacion-del-plugin)). Cuando el plugin se actualiza en el equipo, la metodología, las skills y el mod nuevos están en todas las sesiones de todos los proyectos.

La plantilla es la excepción. Cada proyecto tiene su propia copia en `.sf/claude-sf.md`, que no cambia con el plugin. Se regenera al poner el proyecto al día con la SF, con la skill `sf:incorporar_proyecto_a_sf` (caso «actualizar»). La skill solo rehace ese archivo y no toca el `CLAUDE.md` del proyecto. Si el proyecto va por detrás del plugin en los dos primeros números de la versión, el panel lo avisa («SF 0.13 → 0.34») y dice cómo ponerlo al día.

Lo que no está en el plugin (especificación, decisiones, propuestas, «Cómo funciona…» y el `CLAUDE.md` de la SF) solo necesita el squash a `develop`. Llega a `main` con la siguiente publicación, pero no cambia nada en los proyectos. Para probar un cambio del plugin antes de publicarlo está el modo prueba, solo en la SF. El procedimiento de instalación del plugin está pendiente (propuesta P12).

## En los proyectos consumidores

Cada proyecto registra sus propias decisiones (de producto, de interfaz y técnicas) en su `docs/decisiones/`, una por archivo. Usa el mismo formato que la SF y el mismo script para el índice (metodología, 6). La skill `sf:incorporar_proyecto_a_sf` crea la carpeta al incorporar el proyecto, aunque empiece vacía, y migra el antiguo `docs/decisiones.md` al ponerlo al día. El recorrido es el mismo: el principal anota lo decidido en la cola y la entrada se escribe en la rama de la tarea. Se aplica en los documentos y el código del proyecto, y no sale de él.

Si una regla del `CLAUDE.md` del proyecto choca con la SF, manda la del proyecto. El choque se anota en su `docs/decisiones/` (plantilla, «Reglas del proyecto»). Al incorporar un proyecto existente, la skill hace la lista de esos choques. Los presenta al propietario de la Software Factory uno por uno, con una recomendación. Cada decisión se anota en el proyecto. Mientras no se decide, manda la regla del proyecto.

Lo que el proyecto decide no cambia la SF. Una mejora de la SF que aparece al trabajar en él sigue el ciclo de mejora (ver «El ciclo de mejora»). Se anota en la SF y solo pasa a su `docs/decisiones/` cuando el propietario de la Software Factory la aprueba, en una sesión de la SF.
