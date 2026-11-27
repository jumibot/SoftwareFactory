---
tipo: Documento explicativo
destino: proyecto
herramientas: recomendadas
---
# Cómo funciona la Software Factory

Este documento es para quien usa la Software Factory (SF) en sus proyectos: qué es, qué hace, cómo se instala y cómo se trabaja con ella. No contiene reglas: están en la metodología y en las decisiones, y aquí solo se dice dónde buscarlas. Cómo se escribe, se publica y se mejora la propia SF está en [Cómo se desarrolla la Software Factory](como-se-desarrolla-la-software-factory.html).

**Estado:** 27 de noviembre de 2026, plugin sf 1.9.11.

## La SF es un plugin

Un **plugin de Claude Code** es un paquete que amplía Claude Code con piezas que se instalan juntas: skills, órdenes con barra, hooks y mods de la interfaz. Se publica por versiones y se instala entero.

La SF llega a los proyectos de una sola forma: el plugin `sf`. Lleva el método de trabajo, las skills, las plantillas, el generador de documentos, las herramientas de la cola y el panel. Se instala una vez, para el usuario, y desde ese momento está en todas las sesiones, en cualquier proyecto, con el prefijo `sf:`.

La SF no vive dentro de tus proyectos: el plugin está instalado en tu equipo. Al incorporar un proyecto, la SF le añade dos carpetas suyas, `.sf/` (su configuración, su estado y su cola de tareas) y `sf/` (sus propuestas, sus decisiones y sus informes), y deja lo demás como está: «Incorporación de un proyecto a la SF» dice exactamente qué añade, qué cambia y qué no toca. El kanban es opcional.

Las mejoras de la SF llegan en versiones nuevas del plugin: el panel avisa cuando hay una más nueva que la instalada, y ACTUALIZAR la instala (en «Actualizar la SF»).

## La SF, el CLAUDE.md y las memorias

La SF no interfiere en tu proyecto. Esto es lo que no toca, lo que solo añade y cómo se las apaña para no estorbar.

### Lo que no hace

::: tarjetas 2
#### No añade nada de la SF a tu CLAUDE.md {color=turquesa icono=check}

Sus reglas no se copian ni se importan en él. Si el proyecto no tiene `CLAUDE.md`, se crea solo con el título y la descripción.

#### No toca el CLAUDE.md global ni lo demás de ~/.claude {color=turquesa icono=check}

No sin tu OK. Lo único que guarda ahí, en `~/.claude/sf/`, es su propio estado.

#### No escribe en las memorias de Claude {color=turquesa icono=check}

Lo que la SF recuerda entre sesiones está dentro del proyecto, en `.sf/` y `sf/`, no en las memorias.

#### Solo añade lo suyo, en sitios propios {color=turquesa icono=check}

Dos carpetas propias, `.sf/` y `sf/`, que viajan con el proyecto. Tu código y tus documentos se quedan donde están. La lista completa, en «Incorporación de un proyecto a la SF».
:::

En resumen, hay dos sitios. En tu proyecto, lo que ya tenías sigue intacto y lo que añade la SF es del propio proyecto y viaja con él en el repositorio. En tu equipo, fuera del proyecto, viven el plugin y su estado, y tu CLAUDE.md global y tus memorias quedan intactos.

![](diagramas/sf-dos-sitios.diagrama)

En el esquema, «tu proyecto» abarca las dos primeras zonas: su repositorio y lo que se queda solo en tu máquina, dentro de su carpeta. **Lo que aporta la SF va resaltado en color** (sus carpetas y ramas, lo local, el plugin, su estado en `~/.claude/sf/` y la flecha de las reglas); lo tuyo, en neutro.

### Cómo se las apaña

**Sus reglas llegan por el mod, no por tu CLAUDE.md.** Al empezar cada sesión, el mod entrega a Claude las reglas de la SF desde el plugin. Si actualizas el plugin, llegan las nuevas sin tocar el proyecto.

**Lo suyo tiene sitios propios.** Dentro del proyecto, en `.sf/` y `sf/`, con lo local (la cola y los worktrees) marcado como solo de tu máquina; fuera, en `~/.claude/sf/`. Qué va en cada sitio y quién lo pone está en la tabla de «Estructura de un proyecto bajo la SF».

**Ante un choque con tus reglas, pregunta, y manda la tuya.** Antes de preguntar nada, Claude lee tus reglas y te dice qué choca con la SF, una por línea.

- Lo que choca con cómo la SF lleva el repositorio (quién hace los commits y los push, las ramas, cómo se junta el trabajo, quién publica) no se puede dejar como está: sin ello la SF no podría trabajar. Lo aceptas antes de empezar, y con un no no se cambia nada. Si aceptas, Claude adapta esas frases y las ves antes de aplicar nada.
- Lo demás puede convivir con la SF. Se te propone una regla cada vez, con dos opciones válidas, y lo que decidas se anota en `sf/decisiones/`. Mientras no decidas, manda la regla del proyecto.
- Un `CLAUDE.md` largo o con muchas reglas propias no se revisa en la incorporación: se propone una tarea aparte, con un cambio cada vez, cada uno con tu OK y en su commit.
- Mover secciones del `CLAUDE.md` a otro documento tampoco entra: es una petición tuya aparte.

**Lo útil para otros va al plugin, no a las memorias.** Una regla, preferencia o mejora que sirva a otros usuarios de la SF no se guarda en la memoria de Claude ni en tu `CLAUDE.md`, que solo se ven en esa carpeta y en esa máquina: va a una pieza del plugin o, desde otro proyecto, Claude dice en una línea que es de la SF. La memoria queda para lo propio del usuario o de la sesión.

::: tarjetas 2 plegables
#### Qué lee Claude antes de incorporar {color=turquesa icono=lupa}

El `CLAUDE.md` entero, `.claude/CLAUDE.md` y `CLAUDE.local.md` si los hay; `AGENTS.md`, `CONTRIBUTING.md`, las reglas, los ganchos y los permisos de `.claude/` y de git; y lo que el README diga de cómo se trabaja. Solo lee: no cambia nada. El `CLAUDE.md` global no está en esa lista.

#### Al poner al día un proyecto antiguo {color=turquesa icono=rama}

Se borra la copia `.sf/claude-sf.md` y se quita del `CLAUDE.md` su línea de importación `@.sf/claude-sf.md`, sin tocar lo demás. Mientras la línea siga, el mod entrega solo las reglas del agente principal, para no dar las reglas dos veces, y el panel avisa de que el proyecto va atrasado.
:::

## Instalación del plugin

Los proyectos usan la **copia instalada**: la versión publicada, que Claude Code descarga en su caché y que no se edita nunca, porque la siguiente actualización la sobrescribe.

El plugin se instala una sola vez por equipo, para el usuario, desde el catálogo de la SF en GitHub:

```bash
claude plugin marketplace add jumibot/SoftwareFactory
claude plugin install sf@softwarefactory --scope user
```

**Dependencias.** `sf` necesita tres plugins más, `gsap-skills`, `threejs-skills` y `oklch-skill`, del mismo catálogo: instalar `sf` los trae sin añadir otro catálogo. `dataviz` no es dependencia: es un requisito del entorno para crear series de color. Sin una de ellas, `sf` no carga, ni su panel; `claude plugin update` no instala las nuevas, y por eso, a mano, va una orden por plugin.

**Comprobar la instalación.** La skill `sf:comprobar_instalacion`, la única de la SF que sale en el menú `/`, revisa el catálogo, el plugin y sus dependencias (instalados, activos y en la versión publicada) y los requisitos: git con nombre y correo, `gh` con la sesión iniciada y Python 3.9 o posterior. Dice en pocas líneas qué está bien y qué falta, y propone el arreglo con un menú. La orden `/sf:panel` la ofrece también si el mod no está cargado.

**Python.** La SF necesita Python 3.9 o posterior. El mod prueba `python`, `python3` y `py`, por este orden, y usa el primero que responde, así que arranca igual en un Mac, donde solo hay `python3`.

## Qué lleva el plugin

Sus piezas son de dos tipos, con finalidades distintas: skills y mod.

### Skills

**Finalidad común: que Claude trabaje según el método.** Son conocimiento e instrucciones que Claude carga cuando la tarea lo pide: qué hacer en cada fase, cómo hacerlo y con qué plantillas y herramientas. No hacen nada por sí solas; actúan a través del trabajo de Claude. Salvo `sf:comprobar_instalacion`, son internas: no salen en el menú `/`, para no llenarlo, y Claude las carga cuando tocan.

::: tarjetas 2 plegables
#### Metodología {color=turquesa icono=documento}

Cómo se desarrolla un proyecto: fases, devslices, kanban, estructura, tipos de tarea y pruebas. Con ella viaja la guía común de los esquemas SVG.

#### Orquestación {color=turquesa icono=dialogo}

Las reglas del agente principal: qué hacer con cada mensaje del propietario, el foco, la cola, los subagentes, la prueba y el cierre, y cómo preguntar y escribir. La entrega el mod entera.

#### Flujo, incorporación y configuración {color=turquesa icono=rama}

`sf:flujo_tareas` lleva el ciclo de las tareas con `cola.py`; `sf:incorporar_proyecto_a_sf` prepara un proyecto; `sf:configurar_proyecto` cambia su configuración (`/sf_config`); `sf:comprobar_instalacion` revisa el equipo.

#### Documentos {color=naranja icono=documento}

`sf:crear_documentos` es lo común: el generador único `.md` → HTML, el catálogo de recursos, el estilo del proyecto, el respaldo y la comprobación. Encima, una skill por tipo: `documento_vision` (también los explicativos), `documento_fundacional` e `informe_deliberativa`.

#### Estilo y diagramas {color=naranja icono=lupa}

`sf:fijar_estilo` fija y afina el estilo de los documentos del proyecto, con muestras. `sf:diagramas` dibuja los diagramas desde datos (`.diagrama`), con la estética de diagram-design y su comprobación.

#### Fases del método {color=turquesa icono=codigo}

`sf:diseno_interfaz`, `sf:definicion_tecnica` e `sf:infografia_tecnica`, para la interfaz, la técnica y las infografías 3D de un producto.
:::

**Las plantillas.** Las reglas que reciben los proyectos van partidas en dos: las comunes y las del método, solo si el proyecto lo sigue. No se copian al proyecto: las entrega el mod. Además, el plugin trae las estructuras de carpetas por perfil técnico y el `propuestas.md` vacío que crea la incorporación.

**Las herramientas.** Son órdenes en Python que lanzan Claude o el panel, no tú. La principal es `cola.py`, la única vía para escribir la cola de tareas (`.sf/peticiones.json`): la bloquea mientras escribe y guarda antes una copia y después lo que cambia en su historial.

### El mod de estado

**Finalidad común: que el propietario vea y controle el proyecto desde Claude Code.** Un mod cambia la interfaz o el comportamiento de Claude Code y actúa solo, en respuesta a eventos de la sesión, sin que Claude tenga que acordarse. El de la SF reúne el panel lateral (`/sf`), la caja sobre el prompt, el control de la sesión y lo que entrega a Claude. Se resume en «El panel de la SF» y se detalla en [Cómo funciona el panel](como-funciona-el-panel.html).

## Incorporación de un proyecto a la SF

La vía es pedírselo a Claude en una sesión abierta en el proyecto. En una carpeta sin SF, el panel da la bienvenida con la orden para empezar y, con el primer mensaje, Claude ofrece incorporarla («En una carpeta sin SF, Claude ofrece incorporarla»). Lo hace la skill `sf:incorporar_proyecto_a_sf`, en cuatro casos: proyecto nuevo, existente, actualizar uno ya incorporado y diagnosticar sin cambiar nada.

**Una operación, sin tarea.** Incorporar y poner al día no pasan por la cola y no crean tarea ni rama («Incorporar un proyecto es una operación sin tarea, guiada por menús»). Claude la guía con menús en la línea de prompts: dice qué va a crear o cambiar, en palabras llanas, pide el OK y lo aplica en `develop`, con su commit. Lo que salga mal se deshace con git.


**El repositorio no se elige** («La SF gestiona el repositorio a su manera: la incorporación no lo deja a elección»). Las ramas `develop` y `main`, una rama por tarea, el remoto en GitHub, los commits de Claude y la versión con su tag son fijos. Claude lo explica una sola vez, en palabras llanas, y pregunta si se trabaja así; con un no, para sin cambiar nada. Lo demás se detecta y se confirma (idioma, formato y firma de los commits, remoto, rama de publicación y manifiestos) o se elige (metodología y kanban). El color no se pregunta.

**Los pasos, en el panel.** Mientras dura, el panel enseña bajo la bienvenida cada paso con su respuesta, el actual resaltado y los que faltan atenuados, desde «Plugin» hasta «Comprobación». Claude lo anota fuera del proyecto. Lo respondido no se pierde: si el turno acaba, queda en pausa con «Continuar» y «Abandonar»; si se borra a medias, se guarda aparte para recuperarlo.

::: tarjetas 3
#### Plugin {color=turquesa icono=check}

Antes de cualquier pregunta, Claude comprueba la versión del plugin: si hay una más nueva, la instala con el OK del propietario y, si basta recargar, el mod recarga los plugins solo y Claude sigue la incorporación sin que nadie escriba nada.

#### Reglas del proyecto {color=turquesa icono=lupa}

Antes de los menús, Claude lee el `CLAUDE.md` y las demás reglas que el proyecto se da, y dice qué choca con cómo trabaja la SF. Lo del repositorio se adapta al aceptar; lo demás se propone después, una cosa cada vez.

#### Los menús {color=turquesa icono=dialogo}

Repositorio, identidad y convenciones, por este orden y de hasta cuatro preguntas. Lo que se detecta sin duda no se pregunta: se enseña en el resumen antes del OK.
:::

**La SF interfiere lo mínimo en un proyecto ya empezado.** Añade lo suyo en carpetas propias, cambia solo lo que no puede dejar como está, con tu OK, y no toca el resto. Antes de aplicar nada, Claude te enseña la lista, con para qué sirve cada cosa, y espera tu OK.

::: tarjetas 3
#### Lo que añade la SF {color=turquesa icono=carpeta}

- En `.sf/`: `proyecto.json` (la ficha y la configuración) y, si sigues la metodología, `estado.json` (la fase).
- En `sf/`: `decisiones/` con su índice, `propuestas.md` vacío, y `informes/` cuando Claude escriba el primero.
- `.gitattributes`: una línea para que el índice de decisiones no dé conflictos al juntar ramas.
- Las ramas `develop` y la que hace de `main`, si no existen (las que ya tengas se respetan, también si se llaman `master`), y después una `feature/NN-nombre` por tarea.
- El repositorio en GitHub, si no tiene remoto (sin él no hay SF).
- Un `CLAUDE.md` solo con el título y la descripción, si no tienes ninguno.

#### Lo que cambia, con tu OK {color=turquesa icono=documento}

- `.gitignore`: unas líneas para que git no guarde los archivos de trabajo de la SF (la cola, su historial y sus copias, `.sf/estado.json`, `.sf/subagentes.json`, `.claude/worktrees/` y `sf/decisiones/README.html`).
- Las frases de tu `CLAUDE.md` que chocan con cómo la SF lleva el repositorio, y nada más de él.
- Al poner al día un proyecto ya incorporado: se quitan `.sf/claude-sf.md` y su línea en el `CLAUDE.md`, y, si lo aceptas, las decisiones, propuestas e informes de la SF que estuvieran en otro sitio pasan a `sf/`.
- Un commit propio en `develop`, «Incorporado a la SF» (o «Actualizado»), que se sube a GitHub con las ramas.

#### Lo que no toca {color=turquesa icono=check}

- Tu código, tus documentos y las carpetas de tu editor: no los renombra ni los mueve.
- El resto de tu `CLAUDE.md`, ni el `CLAUDE.md` global ni `~/.claude`.
- Tus ramas y tu forma de nombrarlas: si tu rama principal es `master`, puede publicar en ella.
- Reorganizar algo del proyecto es una petición tuya aparte, nunca parte de la incorporación.
:::

Si no aceptas cómo la SF lleva el repositorio, no se cambia nada. Si el proyecto no tiene estilo para sus documentos, se ofrece fijarlo con `sf:fijar_estilo`; solo se crea `docs/identidad/estilo.json` si aceptas.

**Sin reiniciar.** Con el siguiente mensaje, el mod entrega las reglas y la orquestación («Tras incorporar, el mod entrega las reglas sin reiniciar»), y el panel pasa de la bienvenida al panel del proyecto, con su nombre, su color, la fase si sigue la metodología y sus tareas, sin avisos de la configuración. Sin panel, la caja sobre el prompt muestra `SF <versión> · <proyecto>`.

## Estructura de un proyecto bajo la SF

Un proyecto está bajo la SF cuando tiene `.sf/proyecto.json`. La SF pone dos carpetas en él, con una regla sencilla: `.sf/` es la máquina y `sf/` son los documentos («Los documentos de la SF van en la carpeta sf/»). Qué va al repositorio y qué se queda en tu equipo está en la tabla de abajo; el plugin y el kanban quedan fuera del proyecto.

![](diagramas/sf-proyecto.diagrama)

**`.sf/proyecto.json`** identifica el proyecto y guarda su configuración, en campos sueltos. Lo que falta vale lo de por defecto, y lo que no se entiende sale en los avisos del panel, sin bloquear. Por ejemplo:

```json
{
  "sf": "1.9.11",
  "proyecto": "MiProyecto",
  "descripcion": "Aplicación de ejemplo",
  "color": "blue",
  "metodologia": true,
  "idioma": "es",
  "commits": "libre",
  "remoto": "origin",
  "rama_main": "main",
  "manifiesto": ["package.json"],
  "coautor": "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
}
```

`sf`
:   La versión de la SF con que se incorporó o se puso al día. Si sus dos primeros números van por detrás del plugin, el panel avisa de que el proyecto va atrasado.

`color`
:   El color de las sesiones solo mientras el proyecto no tiene estilo: con `docs/identidad/estilo.json`, sale de su primario (en «El panel de la SF»). No se pregunta.

`metodologia`
:   Si el proyecto sigue el método. Sin él, el panel no da fase ni lee `.sf/estado.json`, y el proyecto solo recibe las reglas comunes.

`kanban`
:   Opcional y, por defecto, no está («El kanban se elige, y por defecto ninguno»).

`idioma`
:   El de los commits, las tareas y los documentos que escribe Claude.

`commits`
:   `libre`, `conventional` o `propio`. Con `libre`, el commit de una tarea lleva «(N)» al final del título; con los otros dos, el trailer `SF-Tarea: N` y el prefijo del tipo de tarea.

`coautor`
:   La línea `Co-Authored-By` que cierra los commits de Claude, o `null`, sin firma.

`remoto` y `rama_main`
:   El remoto de GitHub al que se sube (sin él no hay SF) y la rama en la que se publica: `main` u otra que haga de `main`.

`manifiesto`
:   Los archivos cuya versión sube al publicar, o `null` si solo se marca el tag.

`automatizaciones`
:   Solo aparece si se apaga algo: `orquestacion`, `avisos_subagentes`, `encargo_subagente` y `dependencias_al_actualizar`, encendidos por defecto.

El detalle de cada campo está en el informe «Configuración inicial». Se cambia con `/sf_config`, o pidiéndoselo a Claude: la skill `sf:configurar_proyecto` la enseña, pregunta qué cambiar con menús, pide el OK y lo aplica en `develop` con su commit, sin tarea.

**Quién pone qué y dónde.** Lo que la SF añade a un proyecto, en un vistazo:

| Qué | Dónde | Quién lo pone | En el repositorio |
| --- | --- | --- | --- |
| La ficha y la configuración | `.sf/proyecto.json` | La SF al incorporar; se cambia con `/sf_config` | Sí |
| La fase y la devslice (con metodología) | `.sf/estado.json` | La SF al incorporar | No |
| La cola de tareas, su historial y sus copias | `.sf/peticiones.json`, `historial.jsonl`, `copias/` | `cola.py`, cuando Claude o el panel cambian una tarea | No |
| Lo que el mod sabe de los subagentes | `.sf/subagentes.json` | El mod | No |
| Los worktrees de los subagentes | `.claude/worktrees/`, dentro de la carpeta del proyecto | El subagente de cada tarea; `cola.py` los quita al cerrarla | No |
| Las decisiones | `sf/decisiones/`, con su índice | Claude, en cuanto decides algo; la carpeta, la SF al incorporar | Sí |
| Las propuestas | `sf/propuestas.md` | La SF crea el archivo vacío al incorporar; las propuestas, Claude | Sí |
| Los informes | `sf/informes/` | Claude, al escribir el primero | Sí |
| Las ramas | `develop`, la rama de publicación y `feature/NN-nombre` | La SF al incorporar; `cola.py` crea la de cada tarea | En GitHub |
| El estilo de los documentos | `docs/identidad/estilo.json` | `sf:fijar_estilo`, solo si aceptas | Sí |
| Las reglas de la SF | No están en el proyecto | El mod, desde el plugin, en cada sesión | No aplica |
| El latido de la sesión, el progreso de una incorporación y las copias de `cola.py` | `~/.claude/sf/`, fuera del proyecto | El mod y las herramientas | No aplica |
| Tu `CLAUDE.md`, tu código y tus documentos | Donde ya están | Tú; la SF solo crea el `CLAUDE.md` si no existe | Sí |

Los documentos del proyecto se quedan donde ya están: la SF no los mueve ni los mapea («Sin mapa de documentos: o se sigue la estructura de la SF, o no se mapea»). Lo que no es del repositorio, además de en esa tabla, va al `.gitignore`.


## Lo que recibe la sesión

En un proyecto incorporado, el mod da a Claude lo que necesita para trabajar según la SF, siempre de la versión instalada del plugin, sin depender de que Claude se acuerde de cargarlo ni de una copia en el proyecto («El panel entrega las reglas y la orquestación en los proyectos»).

![](diagramas/sf-sesion.diagrama)

**Las reglas y la orquestación.** Al empezar la sesión, tras `/clear` y tras compactar, Claude recibe las reglas comunes, las del método si el proyecto lo sigue, las convenciones del proyecto (idioma, commits, remoto y rama de publicación) y las reglas del agente principal (`sf:orquestacion`). Se apaga esto último con `"automatizaciones": {"orquestacion": false}`; entonces las carga el propio Claude. Los subagentes no las reciben. Si actualizas o recargas el plugin y han cambiado, tu siguiente mensaje las lleva otra vez, con una línea que dice a qué versión se ha actualizado la SF.

**El arranque.** Al abrir o reanudar la sesión, tras `/clear` y tras compactar, si hay tareas en curso sin subagente o subagentes terminados sin recoger, Claude no espera a tu primer mensaje: toma un turno propio para lanzarlos o recogerlos. Solo con alguien delante y con los avisos de subagentes encendidos.

**Tus tareas en curso.** Con cada mensaje tuyo, Claude recibe la lista de tareas en curso, una línea por tarea: su número, su título corto, si está lista para probar o espera por ti y cómo está su subagente. Así no tiene que consultar la cola antes de contestar. Si nada ha cambiado desde el último mensaje, recibe solo «sin cambios».

**Los avisos.** Con cada mensaje tuyo, Claude se entera de lo que has cambiado desde el panel desde el mensaje anterior, hasta 12 horas atrás, y de lo que le falta hacer: las tareas en curso sin subagente vivo, en cada mensaje mientras falten (salvo las que esperan a otra), y los subagentes que han terminado sin recoger, una vez cada uno. Los avisos de subagentes se apagan con `"automatizaciones": {"avisos_subagentes": false}`.

**Las esperas.** Si una tarea no puede seguir hasta que otra se cierre, la cola lo guarda como dato (`cola.py espera M N`), no como un paso de texto. Mientras la otra siga abierta, Claude no lanza el subagente de la que espera y el panel pone tras su título, atenuado, « · espera a la N». Cuando la otra se cierra o pasa a observación, la espera se libera sola, y Claude lanza el subagente. Al fusionar tareas, quien esperaba a una absorbida espera a la que queda.

**El foco.** El foco es la tarea en la que estás: lo fijas con tus palabras o con Activar rama, lo guarda la cola (`cola.py foco N`; sin número lo dice, con `--quitar` lo quita) y se va solo cuando esa tarea se cierra, se elimina o se descarta; en observación sigue. Con foco, cada respuesta de Claude empieza con la línea 🅵🅾🅲🆄🆂 y el título corto de la tarea, y lo de otras tareas va al final, como off-topic («Reglas del foco y del off-topic»). Para respetarlo, el mod da a Claude el foco guardado al empezar la sesión, tras `/clear` y tras compactar; cuando sus avisos traen algo de otras tareas, le recuerda que eso va como off-topic y sin menús de otras tareas; y mientras pruebas, no le pide lanzar subagentes de otras. Sin foco guardado no recuerda nada. Y pone dos ayudas para no interrumpirte: tras 10 minutos sin escribir, deja en la caja del prompt, sin enviarla, la pregunta «¿Seguimos con …?»; y con texto a medio escribir, no deja que Claude abra un menú.

**Una sola sesión con la SF por proyecto.** Solo una sesión de cada proyecto lleva la SF: el panel, la cola, los subagentes, sus avisos y las órdenes `/sf_*` («Una sola sesión con la SF por proyecto»). La que la tiene deja un latido cada minuto en `~/.claude/sf/latido-<carpeta>.json`; las demás arrancan con la SF apagada y lo dicen antes del primer mensaje, en un aviso y en una línea del historial: son Claude Code sin más, sin panel, sin reglas de la SF y sin `/color` ni `/rename`. `/sf_forzar_activa` trae la SF a una sesión aunque otra la tenga, y `/sf_forzar_inactiva` la apaga en la suya.

## El panel de la SF

El **panel** es el mod de estado del plugin `sf`: una columna a la derecha de la conversación que enseña en qué se trabaja, qué espera y qué se ha cerrado. Es el centro de control de la SF dentro de Claude Code, el mismo en todos los proyectos. En la pantalla completa se abre solo al empezar la sesión; `/sf` lo vuelve a abrir, y en la app de escritorio `/sf:panel` sale en el menú desde antes del primer mensaje. Sin sitio para el panel, el mod se enseña en una caja pequeña sobre el prompt. Fuera de la pantalla completa del terminal los clics no llegan: el panel lo dice y Claude ofrece activarla.

![](diagramas/sf-panel.diagrama)

**La cabecera.** Arriba van RELEASE, que publica una versión del proyecto; TURBO, que pide a Claude poner en curso las tareas que no necesitan al propietario y lanzar sus subagentes. A la derecha, `SF` con la versión que corre, en el color de las sesiones del proyecto. ACTUALIZAR o REFRESCAR salen a la izquierda cuando hacen falta. Debajo, la duración de la sesión, los prompts y la rama activa.

**En curso y Tareas.** En amarillo, las tareas en curso con sus pasos; un ● verde dice que su subagente trabaja. Debajo, un solo bloque de secciones plegables, en el orden del ciclo: **Pendientes**, **En observación**, **Cerradas** y **Propuestas**, que son las de `sf/propuestas.md`.

**Las órdenes, en etiquetas.** Al desplegar una tarea, su primera fila lleva sus órdenes con su nombre («Las órdenes de cada tarea, en un menú de etiquetas»). Primero las de la tarea: Poner en curso, en las de Pendientes, que la pasa a en curso con un clic y pide a Claude que lance su subagente; Activar rama, Cerrar, A observación, Redescribir, A propuesta y, en rojo, Eliminar, Descartar o Revertir. Después, las de sus pasos: Separar pasos y Paso +. Las que cierran o destruyen piden un segundo clic en la misma etiqueta: «¿Cerrar? sí». Una propuesta pasa a la cola con «A Pendientes». En un paso, «?» pide a Claude que lo explique y «×» lo quita. Lo que se puede hacer con una orden lo hace el panel, sin Claude, con git y `cola.py`; cada cambio de estado se explica en [Cómo funcionan los estados](como-funcionan-los-estados.html).

**Las órdenes con barra.** Todas las de la SF empiezan por `sf_`, salvo `/sf`, que abre el panel («Los comandos de la SF empiezan por sf_»): `/sf_paso`, `/sf_split`, `/sf_fusionar`, `/sf_redescribir`, `/sf_config`, `/sf_forzar_activa` y `/sf_forzar_inactiva`.

**En la app de escritorio**, VS Code y el móvil, el panel se ve y funciona como en el terminal: cada botón va en su caja de color, del tamaño mínimo, y en la app de escritorio la línea entera de una tarea, sus órdenes y la marca del subagente se pulsan como en el terminal,.

**El control.** El mod controla que cada sesión modifique un solo proyecto: bloquea, con el motivo, la escritura de archivos en otro («Sin registro ni mejoras de la SF desde otros proyectos»). Un worktree cuenta como su repositorio, y un clon con el mismo remoto `origin`, como el mismo proyecto. Y no deja que un subagente escriba la cola.

**El color de la sesión.** Al arrancar, el mod pone a la sesión el color y el nombre del proyecto, con `/color` y `/rename`. El color sale del primario del estilo del proyecto, el más cercano de los de `/color`, sin reservar el amarillo de la SF («El color de sesión se deriva del color primario del estilo del proyecto»); sin estilo, el `color` de `.sf/proyecto.json`.

El detalle de cada parte, el control, el código y el historial de versiones están en [Cómo funciona el panel](como-funciona-el-panel.html).

## Flujo de trabajo en un proyecto

Al abrir una sesión en el proyecto, el mod lee `.sf/`, abre el panel y entrega las reglas y la orquestación. Si el proyecto sigue la metodología, Claude usa la skill `sf:metodologia`, que le indica qué sección del método leer según el momento, y en cada fase trabaja con la skill que toca.

**La cola y las tareas.** Toda petición del propietario, y todo bug que se detecte, va a la cola en cuanto llega, con `cola.py`. Se trabaja siempre bajo una tarea en curso. El principal habla con el propietario y lleva la cola; cada tarea en curso tiene su subagente, que hace todo su trabajo en su worktree, con una rama auxiliar `sub-NN`. Las reglas, en `sf:orquestacion`; los estados y las órdenes, en `sf:flujo_tareas`.

**La SF guía.** Además de hacer lo que se le pide, el principal observa las tareas, el proyecto y al propietario, y sugiere cómo avanzar mejor, en una línea y con la orden lista («La SF guía el desarrollo: observa y sugiere cómo avanzar»). Sugerir no es hacer: nada se parte, se cierra ni se reordena sin el OK del propietario.

**Tipos de tarea.** Cada tarea tiene un tipo, uno de siete, en tres familias: **código** (implementar y corregir), **deliberativas** (investigar, deliberar y diseñar) y **documentales** (especificar y documentar). El tipo da el prefijo del squash cuando los commits son conventional o propios: `feat`, `fix` o `docs`; sin tipo, `chore`. Las deliberativas no tienen rama, worktree ni rama auxiliar: su subagente solo escribe su documento, que va directo a `develop` en cada vuelta con su respaldo, y su único paso de cierre es «Cerrar la tarea», sin observación («Una deliberativa solo escribe su documento, sin rama; lo demás va a tareas propias con rama»).

**Los pasos de cierre.** Las demás llevan dos desde que entran en curso: «Activar rama para poder probar» y «Cerrar la tarea». No se quitan, y los pasos nuevos van antes de ellos. Si se añade trabajo con la rama ya activada, «Activar rama» vuelve a pendiente, para probar otra vez.

**La prueba.** «Activar rama» integra `develop` en la rama de la tarea y la activa, para probar con lo último. Si choca, no la activa y dice qué archivos chocan. Detrás puede haber ayudas de prueba, que salen como «(opcional)» y no cuentan para cerrar.

**El cierre.** Cerrar entra la rama en `develop` por squash, con su commit, y lo sube al remoto con la revisión de lo que sale. Una rama sin cambios respecto a `develop` se cierra sin commit: se borra y la tarea sale de la cola. «A observación» cierra igual, pero deja la tarea en observación, que después se cierra, si va bien, o se revierte. Cerrar se niega si el subagente tiene trabajo sin traer; al cerrar, `cola.py` quita su worktree y borra su rama auxiliar, sin forzar. Descartar, en cambio, lo borra todo.

**Las decisiones.** Lo que decide el propietario se registra en cuanto se toma: Claude le da número, lo guarda en un archivo de `sf/decisiones/`, rehace el índice y hace el commit «Decisión NNN: Título» en `develop`, aunque la rama activa sea otra, sin cambiarla. No toca la cola.

**Publicar una versión del proyecto.** Se desarrolla en `develop`; `main`, o la rama de publicación que diga la configuración, es lo que se publica. **RELEASE** ofrece con el primer clic las tres versiones siguientes y confirma la elegida con el segundo, avisando de las tareas que quedan en observación. Antes de tocar nada revisa lo que sale: con el remoto público, algo nuevo con un secreto, un dato personal o un archivo interno para la publicación; lo ya subido se enseña y se publica si se vuelve a pulsar en 10 minutos. Después sube la versión de los manifiestos en un commit «vX.Y.Z» en `develop`, pasa `develop` a `main` por fast-forward, la marca con el tag y hace push de las dos ramas y el tag. Si algo no está en orden, no publica y dice cómo arreglarlo.

**Lo que es de la SF.** En un proyecto solo se anotan propuestas de ese proyecto («Un proyecto solo anota propuestas suyas»). Si algo de la SF falla, sobra o falta, Claude lo dice en una línea y no lo anota en el proyecto: la mejora se lleva a la SF aparte, como se cuenta en [Cómo se desarrolla la Software Factory](como-se-desarrolla-la-software-factory.html).

## Documentos del proyecto

Todos los documentos de un proyecto bajo la SF salen de un **generador único** y determinista, con el **estilo del proyecto** («Un solo generador determinista con el estilo del proyecto»). Cada tipo de documento pone solo lo suyo en su skill: un `perfil.json` con los recursos que usa y un envoltorio de pocas líneas. También el índice de las decisiones sale de él.

::: tarjetas 2 plegables
#### El estilo del proyecto {color=naranja icono=lupa}

Todo el aspecto vive en `docs/identidad/estilo.json`, junto a `identidad.json`: identidad y logo, colores, letra, portada, secciones, página, recuadros, lectura, diagramas y la infografía aparte. El `.md` no fija el aspecto: solo cómo se lee («El aspecto lo fija solo el estilo; cada documento fija cómo se lee»). Sin estilo, el generador sale del paso con un tema elegido por el color del proyecto y lo avisa.

#### Fijar el estilo {color=naranja icono=check}

Lo escribe solo `sf:fijar_estilo`: parte de una de las seis muestras con nombre (sereno, desenfadado, técnico, institucional, sobrio y editorial) o de una séptima, el estilo actual del proyecto (sin él, con su color), enseña muestras del mismo documento y afina en vueltas; cada vuelta aceptada respalda la anterior, sube la versión y anota el historial. También puede generar el catálogo de temas en miniatura, en claro y en oscuro.

#### Contraste y modo oscuro {color=naranja icono=aviso}

Antes de generar, el generador se detiene si un texto baja de 4,5:1 (3:1 el grande) y solo avisa de un borde o una línea por debajo de 3:1. Un color primario claro, como el amarillo, se sostiene con colores derivados. El modo oscuro de «Lectura» aplica la paleta oscura del estilo, derivada si el tema no la trae, sin invertir la página.

#### Diagramas {color=naranja icono=rama}

Un diagrama se escribe como datos en un `.diagrama` y el `.md` lo nombra en una línea; en cada generación, el motor de `sf:diagramas` lo dibuja con el estilo del documento, en vertical y, si cabe, en horizontal, con fichas que se abren al pulsar cada nodo.
:::

**Respaldar y comprobar.** Antes de sustituir un documento por una versión nueva, la anterior se copia a `_respaldo/`. Cada cambio del `.md` regenera su HTML. Antes de entregar, se abre el HTML en escritorio y en móvil, en claro y en oscuro, lo imprime en A4 y pasa la comprobación de los diagramas: desbordes, errores de JS, contraste, restos de sintaxis y enlaces internos rotos. Sale con error si encuentra alguno. Si el documento abre en la historia, la comprobación lo mide también después de salir de ella, no solo al abrirlo.

## Actualizar la SF

**Actualizar la SF.** La versión publicada del plugin se mira al empezar, cada 5 minutos, con `/sf` y tras publicar; la instalada, cada minuto. **ACTUALIZAR**, en rojo, sale cuando hay una versión publicada sin instalar: refresca el catálogo, actualiza el plugin en cada scope que usa el proyecto e instala las dependencias que falten, una orden por plugin. **REFRESCAR** sale cuando la instalada es más nueva que la que corre la sesión, porque la actualizó otra: recarga el plugin sin reiniciar, con un aviso que lo explica («ACTUALIZAR y REFRESCAR: dos botones para dos casos»). Si hay dependencias nuevas, pide reiniciar Claude Code. Se apaga con `"automatizaciones": {"dependencias_al_actualizar": false}`: entonces solo da las órdenes. Tras recargar, el siguiente mensaje lleva a Claude las reglas y la orquestación nuevas, si han cambiado (en «Lo que recibe la sesión»).

## Índice de consulta

<dl class="faq">
<dt>¿Cómo se hace algo en un proyecto?</dt><dd>Metodología (skill <code>sf:metodologia</code>)</dd>
<dt>¿Qué hace el principal con cada mensaje?</dt><dd>Skill <code>sf:orquestacion</code></dd>
<dt>¿Por qué se hizo así?</dt><dd><code>sf/decisiones/</code></dd>
<dt>¿Qué ideas esperan aprobación?</dt><dd><code>sf/propuestas.md</code>, y la sección Propuestas del panel</dd>
<dt>¿Qué hace el panel?</dt><dd>«El panel de la SF», en este documento, y <a href="como-funciona-el-panel.html">Cómo funciona el panel</a></dd>
<dt>¿Cómo cambia de estado una tarea?</dt><dd><a href="como-funcionan-los-estados.html">Cómo funcionan los estados</a> y la skill <code>sf:flujo_tareas</code></dd>
<dt>¿Cómo se pone un proyecto bajo la SF?</dt><dd>«Incorporación de un proyecto a la SF», en este documento, y la skill <code>sf:incorporar_proyecto_a_sf</code></dd>
<dt>¿Está bien instalada la SF en este equipo?</dt><dd>La skill <code>sf:comprobar_instalacion</code></dd>
<dt>¿Cómo se configura un proyecto?</dt><dd>Su <code>.sf/proyecto.json</code>, que se cambia con <code>/sf_config</code>; el detalle, en el informe «Configuración inicial»</dd>
<dt>¿En qué punto está un proyecto?</dt><dd>Su <code>.sf/estado.json</code>, si sigue la metodología, o <code>/sf</code> dentro de Claude Code</dd>
<dt>¿Qué decidió el propietario en un proyecto?</dt><dd>La carpeta <code>sf/decisiones/</code> de ese proyecto</dd>
<dt>¿Cómo se hace un documento?</dt><dd>La skill <code>sf:crear_documentos</code> y la de su tipo; su aspecto, en <code>docs/identidad/estilo.json</code>, con <code>sf:fijar_estilo</code></dd>
<dt>¿Cómo se dibuja un diagrama?</dt><dd>La skill <code>sf:diagramas</code>; nunca ASCII ni mermaid</dd>
<dt>¿Cómo se desarrolla la propia SF?</dt><dd><a href="como-se-desarrolla-la-software-factory.html">Cómo se desarrolla la Software Factory</a></dd>
</dl>
