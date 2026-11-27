<!-- destino: proyecto -->
<!-- herramientas: -notas -nota-texto -nota-seccion -nota-global -->
# Mejora continua a la Software Factory

Este documento describe el ciclo de mejora continua de la SF. Cuenta cómo se usa, qué se observa y dónde se anota, y cómo lo decide el propietario de la Software Factory. Después sigue a la decisión hasta los proyectos: dónde se registra, con qué formato, en qué componentes se aplica y cuándo los lee Claude. No contiene reglas: están en la metodología (secciones 2, 6 y 11), en la plantilla de reglas `claude-sf.md`, que entrega el mod, y, lo propio de trabajar en el repositorio de la SF, en su `CLAUDE.md`. Aquí solo se dice dónde buscarlas.

Las decisiones son la forma en que la SF evoluciona y se corrige. Cada una nace de usarla, en la propia SF o al desarrollar una aplicación. Puede responder a una necesidad nueva (evolutiva) o a algo que falla, sobra o estorba (correctiva). No son un trámite aparte, sino parte de su mejora continua (metodología, 11). Lo observado va a la cola, como tarea o como bug, o a las propuestas. Lo que decide el propietario de la Software Factory se registra en `sf/decisiones/`, con su porqué. Después se aplica a sus componentes y llega a los proyectos con la siguiente versión.

**Estado:** 27 de noviembre de 2026, plugin `sf` 1.9.14.

## El ciclo de mejora

La SF mejora usándola. Cada vuelta del ciclo empieza en el uso y termina en una versión publicada, que se vuelve a usar:

![](diagramas/ciclo-de-mejora.diagrama)

Todo empieza al **usar la SF**, al construir la propia SF o al desarrollar un proyecto con ella. Al usarla aparece lo que falta, lo que falla y lo que estorba. Eso **se anota** en cuanto aparece, sin parar el trabajo: un error, como bug en la cola de tareas; lo que hay que pensar antes de decidir, en las propuestas, `sf/propuestas.md`. Si es de la SF y aparece en otro proyecto, ese proyecto no lo anota: Claude lo dice en una línea, y llevarlo a la SF es cosa del propietario, en una sesión de la SF («Un proyecto solo anota propuestas suyas», 210).

Lo anotado no cambia nada hasta que **el propietario de la Software Factory lo decide**. La decisión puede ser evolutiva, si añade algo que la SF no tenía (el botón para descartar una tarea). O correctiva, si arregla algo que ya hay (las tablas que partían las palabras). En los dos casos se convierte en una tarea, con su propia rama.

La decisión **se registra** en cuanto se toma, en su archivo de `sf/decisiones/`, directamente en `develop`. En la rama de la tarea **se aplica**: se lleva a los componentes que la recogen, como la metodología, las plantillas de reglas o el código del plugin. Después **se prueba**. Lo que salga al probar se corrige en la misma rama, como un paso más de la tarea. Con el OK del propietario de la Software Factory, la tarea entra en `develop`.

Lo que está en `develop` llega a los proyectos al **publicar una versión** del plugin. Desde entonces se usa en todos ellos. Lo que se observe al usarlo empieza la vuelta siguiente.

Los apartados que siguen recorren el ciclo con detalle. Cuentan cómo se distingue lo decidido de lo propuesto, cuándo y cómo se registra una decisión, dónde se aplica, cómo se prueba y cómo llega a los proyectos.

## Decisión, propuesta, preferencia y pendiente

La SF separa lo decidido de lo que aún no lo está. Cada tipo tiene su sitio y no se mezcla con los demás.

| Tipo | Qué es | Dónde va |
| --- | --- | --- |
| Decisión | Lo que el propietario de la Software Factory ha decidido, con su porqué. | Un archivo en `sf/decisiones/`. La regla que sale de ella va a la metodología o a la especificación, marcada como acuerdo o norma del propietario, con fecha. |
| Propuesta | Un cambio que alguien plantea y el propietario de la Software Factory aún no ha decidido. | `sf/propuestas.md`, con número fijo (P01, P02…). Una mejora de la SF va además a la tarea permanente «Mejorar la Software Factory» del proyecto SoftwareFactory del kanban, cuando esté conectado. |
| Preferencia | Una opción favorita que se confirma en cada proyecto. | Metodología y especificación, marcada como preferencia (por ejemplo, metodología, 5). |
| Pendiente | Una decisión o un dato que falta. | Al final de la metodología (sección 10) y de la especificación (sección 4). En un proyecto, en `pendientes` de `.sf/estado.json`. |

**Un ejemplo de cada tipo:**

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,26rem),1fr));gap:.9rem;margin:1rem 0 1.4rem;"><div class="ficha" style="margin:0;"><p class="ficha-titulo">Decisión · Una rama de feature por tarea</p><p style="margin:0 0 .45rem;">Cada tarea tiene su rama <code>feature/NN-nombre</code> desde <code>develop</code>; entra en <code>develop</code> por squash cuando está probada. Su regla está en la metodología, 2.2, «Ramas por tarea».</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>sf/decisiones/082-2026-10-29-una-rama-de-feature-por-tarea.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Propuesta · P03 Perfil para productos de software y hardware</p><p style="margin:0 0 .45rem;">Añadir a la metodología un perfil «gemelo digital primero», a partir de SmartColdBox. La planteó el propietario de la Software Factory al hablar de ese proyecto.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>sf/propuestas.md</code>, P03</p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Preferencia · Frontend web: React</p><p style="margin:0 0 .45rem;">React es la favorita para el frontend web. Un proyecto puede elegir otra si lo justifica, y lo anota en sus decisiones.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);">Metodología, 5</p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Pendiente · Ejecutor de migraciones</p><p style="margin:0 0 .45rem;">Elegir el ejecutor de migraciones y las versiones de esquema soportadas.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);">Metodología, 10</p></div></div>

En la metodología y en la especificación solo hay acuerdos, preferencias y pendientes. Los dos documentos explican al principio cómo distinguirlos. Lo que empieza por «Ejemplo:» ilustra una regla y no manda nada. Una propuesta aprobada pasa a `sf/decisiones/` y sale de las pendientes. Una descartada queda en «Descartadas», con el motivo. Registrar una propuesta no autoriza aplicarla. Una instrucción directa del propietario de la Software Factory sí, dentro de su alcance (`CLAUDE.md` de la SF, reglas de trabajo).

## Cuándo se registra

Una decisión se registra en cuanto se toma. Suele ser en el chat, mientras se define una tarea. El agente principal es quien habla con el propietario de la Software Factory, y quien la registra, con `cola.py decision`: le da número, escribe su archivo en `sf/decisiones/`, rehace el índice y hace el commit «Decisión NNN: Título» en `develop`, aunque la rama activa sea otra y sin cambiarla («Las decisiones, a develop en cuanto se toman», 155). Así está en `develop` desde el primer momento y no choca con las ramas de las tareas. Nunca se escribe a mano en la rama de una tarea.

Aplicarla es trabajo de una tarea. Su subagente la lleva a la metodología, las skills, el código o los documentos, en la rama `feature/NN-nombre`, y eso entra en `develop` con el cierre de la tarea, cuando el propietario de la Software Factory da su OK.

<div class="ejemplo"><p>Mientras se definía la tarea 439, el propietario de la Software Factory eligió el formato de las decisiones entre tres propuestas, y sobre el índice dijo: «Dos catálogos distintos accesibles desde un punto común si se quiere».</p><p>El principal lo registró al momento con <code>cola.py decision</code>, en <code>develop</code>: las decisiones 388 (el formato), 389 (los dos catálogos) y 390 (la fecha del registro).</p><p>El subagente de la 439 las aplicó después en su rama: la plantilla de <code>sf:definicion_tecnica</code>, <code>indice_decisiones.py</code>, <code>cola.py</code> y este documento. Eso entra en <code>develop</code> cuando el propietario cierre la tarea.</p></div>

Las reglas están en la metodología (sección 6, «Estructura documental común», y 2.2, «Orquestación con subagentes») y en `sf:orquestacion`. También en las decisiones «Las decisiones, a develop en cuanto se toman» (155) y «El principal orquesta y lanza cada subagente sin preguntar» (376).

## Formato

Cada decisión es un archivo de `sf/decisiones/`, `NNN-AAAA-MM-DD-titulo.md`: el número de orden total (el siguiente al más alto), la fecha del día en que se registra y el título sin tildes ni signos («La fecha del nombre de archivo de una decisión es la de su registro», 390). La registra `cola.py decision "Título" --archivo RUTA`, que da el número y el nombre, rehace el índice y hace el commit en `develop`, también con otra rama activa. Todas siguen un solo formato, «regla y porqué» («Las decisiones, en un solo formato: regla y porqué», 388), y la plantilla está en la skill `sf:definicion_tecnica`. Cada parte va en este orden, y solo las que hacen falta:

El título
:   La regla decidida, en una frase: lo que se decidió, no el tema.

Lo decidido
:   En párrafos cortos o en lista, con los nombres de las piezas que cambian.

Opciones
:   Solo si hubo alternativas reales: cuál se elige y por qué se descartan las demás. Los pros y contras completos se quedan en el informe de la tarea, que la decisión enlaza.

Sustituye a
:   Si cambia otra: «Sustituye a «Título» (NNN), que queda deprecada» o, si de la otra sigue valiendo algo, «Recoge lo que sigue valiendo de «Título» (NNN), que queda deprecada».

Porqué
:   El problema y la razón, con las palabras del propietario de la Software Factory entre comillas latinas y la tarea de origen.

Aplicada en
:   Las piezas que la recogen: secciones de la metodología, skills, archivos del plugin y documentos; y lo pendiente.

Mientras está vigente, una decisión no lleva estado, ni fecha ni quién decide: la fecha va en el nombre del archivo y decide siempre el propietario. Lo que aún no está decidido no es una decisión: va a las propuestas.

Una decisión no se borra cuando otra la cambia: se depreca entera, también si solo cambia una parte («Las decisiones superadas se deprecan enteras y lo vigente va a una decisión nueva», 360). Bajo su título lleva una línea de estado, con la decisión que la sustituye y las que cambiaron el resto: «Estado: deprecada el AAAA-MM-DD por «Título» (NNN); lo demás, por «Título» (NNN)». Lo que siga valiendo va a una decisión nueva, que lo dice. De la antigua solo cambian esa línea y su «Aplicada en»; el resto queda como historia.

Ejemplo: una decisión real que recoge lo vigente de dos anteriores, que quedan deprecadas.

```markdown
# El número de una tarea lleva el color de su estado, y una reabierta cuenta como H

En el panel, el número de una tarea va sin letra detrás: la letra de su estado (A, H, O, C o D) solo le da el color. El número va subrayado cuando la tarea se despliega.

Una tarea reabierta no es nueva: cuenta como H, aunque haya entrado en la sesión.

Recoge lo que sigue valiendo de «Código de tarea más ligero: 74C» (066) y «Una tarea reabierta lleva H» (069), que quedan deprecadas.

Porqué: los códigos de tarea pesaban a la vista; primero se quitó el guion y después la letra, que quedó solo como color (propietario de la Software Factory, 2026-10-28 y 2026-10-31). Una reabierta volvía con A, como si fuera nueva (069).

Aplicada en: el panel (`plugins/sf/hooks/panel.tsx`) y sus pruebas.
```

Y la primera línea de una de las que deprecó, bajo su título:

```markdown
Estado: deprecada el 2026-11-25 por «El número de una tarea lleva el color de su estado, y una reabierta cuenta como H» (373); lo demás, por «Números de tarea en tres columnas, apartados con 0 y rojo solo para las reabiertas» (159).
```

> **El índice, en dos catálogos**
> Las vigentes y las deprecadas van en dos archivos distintos, con un punto de entrada común («Vigentes y deprecadas, en dos catálogos distintos con un punto de entrada común», 389). `sf/decisiones/README.md` es la entrada: dice qué recoge, cómo se registra una decisión y enlaza a los dos. `vigentes.md` lista las que se aplican y `deprecadas.md`, las superadas, cada una con las que la sustituyen. En los dos, la más reciente arriba.

Los tres archivos no se escriben a mano: `python -I -X utf8 plugins/sf/tools/indice_decisiones.py sf/decisiones` los regenera, sin Claude, y conserva lo que va antes de «Índice» en el `README.md`. El estado lo lee de la primera línea bajo el título; las marcas de antes se leen igual: «**Sustituida**» cuenta como deprecada, y «**Sustituida en parte**» sigue en vigentes con esa marca. Dos tareas que añaden decisiones no chocan al juntarse: cada una trae su archivo, y los del índice se juntan con `merge=union` (`.gitattributes`) y se regeneran. Sus versiones `.html` no se versionan.

Es el formato que pide la metodología (sección 6) para todos los proyectos, con la plantilla de `sf:definicion_tecnica`.

## Dónde se aplica

Una decisión no se queda en `sf/decisiones/`. Se aplica en su tarea, en los componentes que la recogen, y su «Aplicada en» los enumera. Cada componente llega a un sitio distinto, y Claude lo lee en un momento distinto.

![](diagramas/recorrido-de-una-decision.diagrama)

Cada componente guarda una parte distinta de lo decidido. Lo que se aplica en todas las sesiones está en la plantilla y en el `CLAUDE.md`. El detalle está en la metodología, que Claude lee cuando la tarea lo pide.

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,19rem),1fr));gap:.9rem;margin:1.2rem 0 1.6rem;"><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Metodología</p><p style="margin:0 0 .45rem;"><strong>Guarda</strong> la regla completa, como acuerdo o norma del propietario con fecha, además de preferencias y pendientes.</p><p style="margin:0 0 .45rem;"><strong>La lee</strong> Claude, en la SF y en cada proyecto.</p><p style="margin:0 0 .45rem;"><strong>Se carga</strong> como skill: Claude Code tiene su descripción en todas las sesiones y Claude la carga cuando la tarea lo pide (empezar o retomar un proyecto, cambiar de fase, saber cómo se hace algo). La skill le dice qué sección leer en cada momento. En la SF, el arranque (<code>docs/arranque-claude.md</code>) dice cuándo abrirla.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>plugins/sf/skills/metodologia/references/desarrollo-de-proyectos.md</code></p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Plantilla <code>claude-sf.md</code></p><p style="margin:0 0 .45rem;"><strong>Guarda</strong> las reglas que se aplican siempre en un proyecto, en un punto cada una: orquestación, comandos antes que inferencia, configuración, un proyecto por sesión, lo que es de la SF, cola, ramas, subagentes, decisiones, preguntas, documentos, propuestas y reglas del proyecto. Las del método (método y estado) van aparte, en <code>claude-sf-metodologia.md</code>.</p><p style="margin:0 0 .45rem;"><strong>La lee</strong> Claude, en cada proyecto y en la propia SF.</p><p style="margin:0 0 .45rem;"><strong>Se carga</strong> en cada sesión del proyecto: el mod la entrega, de la versión instalada, al empezar, tras <code>/clear</code> y tras compactar, junto con <code>claude-sf-metodologia.md</code> si el proyecto sigue el método y con <code>sf:orquestacion</code>. No se copia al proyecto, y la SF la recibe como los demás («En la SF, las reglas y sf:orquestacion las entrega el mod, como en los demás proyectos», 298).</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>plugins/sf/templates/claude-sf.md</code></p></div><div class="ficha" style="margin:0;--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;"><p class="ficha-titulo">Código del plugin</p><p style="margin:0 0 .45rem;"><strong>Guarda</strong> el comportamiento: lo que hace el panel, lo que bloquea el mod y lo que hacen las skills y sus plantillas.</p><p style="margin:0 0 .45rem;"><strong>Lo ve</strong> el propietario de la Software Factory, en el panel; las skills, Claude.</p><p style="margin:0 0 .45rem;"><strong>Se carga</strong> desde la copia instalada: el mod responde solo a los eventos de cada sesión, sin que Claude tenga que acordarse; las skills, cuando la tarea lo pide.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>plugins/sf/hooks/</code>, <code>plugins/sf/skills/</code>, <code>plugins/sf/templates/</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo"><code>CLAUDE.md</code> de la SF</p><p style="margin:0 0 .45rem;"><strong>Guarda</strong> la lectura de entrada, el arranque, y las reglas de trabajo propias del repositorio de la SF, con enlaces a lo demás. No lleva nada que viaje en el plugin, y cambiarlo pide la autorización del propietario (291).</p><p style="margin:0 0 .45rem;"><strong>Lo lee</strong> Claude, en la SF.</p><p style="margin:0 0 .45rem;"><strong>Se carga</strong> al empezar cada sesión abierta en la SF. No llega a los proyectos.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>CLAUDE.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Especificación</p><p style="margin:0 0 .45rem;"><strong>Guarda</strong> qué hay que construir en la SF para aplicar y distribuir el método (plugin, mods, skills), con acuerdos fechados y pendientes.</p><p style="margin:0 0 .45rem;"><strong>La leen</strong> Claude y el propietario de la Software Factory, en la SF.</p><p style="margin:0 0 .45rem;"><strong>No se carga sola:</strong> el arranque dice cuándo abrirla. Se queda en el repositorio.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/specs/funcional/software-factory.md</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">«Cómo funciona…»</p><p style="margin:0 0 .45rem;"><strong>Guardan</strong> cómo es cada componente después de la decisión, sin reglas: dónde está, qué hace y cómo se relaciona.</p><p style="margin:0 0 .45rem;"><strong>Los leen</strong> el propietario de la Software Factory y Claude, en la SF.</p><p style="margin:0 0 .45rem;"><strong>No se cargan solos:</strong> el arranque dice cuándo abrir cada uno, y una regla de trabajo del <code>CLAUDE.md</code> pide actualizarlos cuando cambia un componente.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/como-funciona-la-software-factory.md</code>, <code>docs/como-funciona-el-panel.md</code> y este documento</p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Memoria de Claude</p><p style="margin:0 0 .45rem;"><strong>Guarda</strong> notas de Claude para un usuario y un proyecto: contexto, preferencias y recordatorios de normas. En la SF no lleva nada que viaje en el plugin, y cambiarla pide la autorización del propietario (292).</p><p style="margin:0 0 .45rem;"><strong>La lee</strong> Claude, en ese proyecto y en ese equipo.</p><p style="margin:0 0 .45rem;"><strong>Se carga</strong> al empezar cada sesión del proyecto: el índice, <code>MEMORY.md</code>; cada nota, cuando hace falta. Está fuera del repositorio: no es un activo, no se versiona y no llega a otros proyectos.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>~/.claude/projects/&lt;carpeta del proyecto&gt;/memory/</code></p></div></div>

Una regla que se aplica siempre se escribe en dos sitios. Completa, en la metodología. En una línea, en la plantilla `claude-sf.md`, que remite a la sección y que el mod entrega en todas las sesiones, también en la SF. Por eso muchas decisiones dicen «Aplicada en: metodología, 2; plantilla `claude-sf.md`». El `CLAUDE.md` de la SF solo lleva lo propio de trabajar en su repositorio (291). La memoria no se versiona, así que el registro es `sf/decisiones/`. Qué va a memoria, al `CLAUDE.md` o a una skill en los proyectos sigue sin decidir (propuesta P01, bloque B).

## Cómo se prueban las mejoras

Ninguna mejora entra en `develop` sin el OK del propietario de la Software Factory. La prueba la hace él, en la rama de la tarea. Claude la prepara: al terminar una tarea, propone probarla, con cómo, o cerrarla si no tiene nada que probar; cerrar espera su OK («Al terminar una tarea, Claude propone probarla o cerrarla, y cerrar espera el OK del propietario», 371).

**Antes de la prueba, lo que comprueba Claude.** Claude ejecuta lo que puede comprobar solo. En el plugin, `claude plugin validate plugins/sf` y las pruebas automáticas, `claude plugin test plugins/sf`. En un documento, `comprobar_documento.py` de `sf:crear_documentos`, en escritorio, móvil, claro, oscuro y A4. Lo anota como paso hecho de la tarea, «Comprobado: …», y lo que no pudo comprobar, como «No comprobado: …» («Las comprobaciones y pruebas hechas se anotan como pasos de su tarea», 288). No sustituye la prueba del propietario de la Software Factory: la tarea sigue en curso hasta su OK, o en observación si se cerró con «A observación».

**Dónde se prueba.** En la carpeta principal, con la rama de la tarea activa. Solo hay una rama activa por carpeta. La orden «Activar rama» del menú de la tarea, en el panel, la activa con un clic, sin pasar por Claude: antes integra `develop` en ella, y marca hecho el paso «Activar rama para poder probar». Si la rama activa tiene cambios sin commit, o la de la tarea está en otro worktree, no cambia de rama y avisa. El subagente trabaja en su rama auxiliar, `sub-NN`, en su worktree, y el principal trae ese trabajo a la rama de la tarea; si queda algo sin traer, «Activar rama» no la activa y se lo pasa a Claude («Activar rama integra develop, avisa a Claude si choca y adelanta la rama del subagente», 191). Qué se mira depende de lo que cambia:

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,19rem),1fr));gap:.9rem;margin:1rem 0 1.4rem;"><div class="ficha" style="margin:0;"><p class="ficha-titulo">Un documento</p><p style="margin:0 0 .45rem;">Se abre el HTML generado, con la rama activa. Si cambia el generador, se regenera antes.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);"><code>docs/*.html</code></p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">El plugin en la SF</p><p style="margin:0 0 .45rem;">El panel, los comandos y las skills se prueban con el modo prueba, que carga la copia de trabajo, y <code>/reload-plugins</code> tras cada cambio.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);">Etiqueta «prueba» de la cabecera del panel</p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">El plugin en otro proyecto</p><p style="margin:0 0 .45rem;">Si el efecto se ve en otro proyecto, se abre una sesión de ese proyecto con <code>claude --plugin-dir D:/Projectes/SoftwareFactory/plugins/sf</code>.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);">Sesión del otro proyecto</p></div><div class="ficha" style="margin:0;"><p class="ficha-titulo">Una aplicación</p><p style="margin:0 0 .45rem;">En un proyecto: su rama activa y la aplicación reiniciada; con migraciones, sobre una base de pruebas, y con dependencias nuevas, instaladas antes.</p><p style="margin:0;font-size:.82rem;color:var(--texto-suave);">Metodología, 2 y 8</p></div></div>

**Qué mirar.** Claude dice en el chat qué hacer y qué mirar. Lo deja también en el campo `prueba` de la tarea, que el panel muestra al desplegarla. Desde que entra en curso, la tarea lleva al final los pasos «Activar rama para poder probar» y «Cerrar la tarea» («Los pasos de cierre, desde que la tarea entra en curso», 174): así se ve lo que falta.

**Si al probar hace falta un cambio**, se hace en ese momento, en la misma rama. Es un paso nuevo de la tarea, y se vuelve a probar. Si es otra cosa, va a Pendientes como tarea nueva. Si es un fallo de una tarea ya cerrada, esa tarea se reabre con su número.

**Al terminar.** Con el OK del propietario de la Software Factory («va bien, ciérrala»), la tarea entra en `develop` por squash y sale de la cola. Si quiere vigilarla un tiempo, la cierra con «A observación»: entra en `develop` y queda en observación, con qué mirar, hasta que se cierra o se revierte. Lo que no ha pasado la prueba no se publica.

## Cómo llega a los proyectos

Lo decidido llega a los proyectos solo al publicar el plugin. Los proyectos usan la versión publicada e instalada, nunca la copia de trabajo de la SF (especificación, sección 1).

![](diagramas/como-llega.diagrama)

El recorrido tiene dos pasos. Primero, la tarea probada entra en `develop` por squash, con el OK del propietario de la Software Factory. Después, al publicar, se sube la `version` de `plugins/sf/.claude-plugin/plugin.json`. `develop` pasa a `main` y se marca con el tag `vX.Y.Z` (metodología, 2; «Publicación del plugin» en [Cómo se desarrolla la Software Factory](como-se-desarrolla-la-software-factory.html#flujo-de-mejora-de-la-sf)). Cuando el plugin se actualiza en el equipo, la metodología, las skills y el mod nuevos están en todas las sesiones de todos los proyectos.

Las reglas tampoco se copian al proyecto. Las plantillas `claude-sf.md` y, si el proyecto sigue el método, `claude-sf-metodologia.md` las entrega el mod de la versión instalada al empezar la sesión, tras `/clear` y tras compactar, junto con `sf:orquestacion` («El mod entrega las reglas y sf:orquestacion al empezar la sesión, tras /clear y tras compactar», 379), también en la propia SF (298). Llegan en cuanto se actualiza el plugin, con un `/clear`.

Un proyecto incorporado con una SF anterior aún tiene la copia `.sf/claude-sf.md` y su línea `@.sf/claude-sf.md` en el `CLAUDE.md`. Mientras tanto, el mod le entrega solo la orquestación y el panel avisa de que va atrasado. Ponerlo al día con la skill `sf:incorporar_proyecto_a_sf` (caso «actualizar») quita la copia y la línea, sin tocar lo demás del `CLAUDE.md`. El panel también avisa si el proyecto va por detrás del plugin en los dos primeros números de la versión («SF 1.3 → 1.5»).

Lo que no está en el plugin (especificación, decisiones, propuestas, «Cómo funciona…» y el `CLAUDE.md` de la SF) solo necesita el squash a `develop`. Llega a `main` con la siguiente publicación, pero no cambia nada en los proyectos. Para probar un cambio del plugin antes de publicarlo está el modo prueba, solo en la SF. Comprobar y arreglar la instalación lo hace la skill `sf:comprobar_instalacion`; las guías de instalación y de actualización están pendientes (propuesta P12).

## En los proyectos consumidores

Cada proyecto registra sus propias decisiones (de producto, de interfaz y técnicas) en su `sf/decisiones/`, una por archivo. Usa el mismo formato que la SF y el mismo script para el índice (metodología, 6). La skill `sf:incorporar_proyecto_a_sf` crea la carpeta al incorporar el proyecto, aunque empiece vacía, y al ponerlo al día pasa a ella, con el OK del propietario, las que tuviera en otro sitio (`docs/decisiones/`, un `docs/decisiones.md` u otro registro). El recorrido es el mismo: el principal registra la decisión en `develop` en cuanto se toma, y se aplica en la rama de la tarea, en los documentos y el código del proyecto, sin salir de él.

Si una regla del `CLAUDE.md` del proyecto choca con la SF, manda la del proyecto. El choque se anota en su `sf/decisiones/` (plantilla, «Reglas del proyecto»). Salvo en cómo se lleva el repositorio (ramas, commits, push, cola y publicación), aceptado al incorporarlo: ahí manda la SF. Al incorporar un proyecto existente, la skill hace la lista de esos choques. Los presenta al propietario de la Software Factory uno por uno, con una recomendación. Cada decisión se anota en el proyecto. Mientras no se decide, manda la regla del proyecto.

Lo que el proyecto decide no cambia la SF. Una mejora de la SF que aparece al trabajar en él no se anota en el proyecto: Claude lo dice en una línea, y llevarla a la SF es cosa del propietario de la Software Factory, en una sesión de la SF, donde sigue el ciclo de mejora («Un proyecto solo anota propuestas suyas», 210).
