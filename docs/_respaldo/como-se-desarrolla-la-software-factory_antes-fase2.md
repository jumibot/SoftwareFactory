---
tipo: Documento explicativo
destino: proyecto
herramientas: recomendadas
---
# Cómo se desarrolla la Software Factory

Este documento es para quien desarrolla la propia Software Factory (SF): dónde se escribe, qué hay en el repositorio y dónde vive cada pieza, cómo se mejora, se prueba y se publica. Quien solo usa la SF en sus proyectos tiene [Cómo funciona la Software Factory](como-funciona-la-software-factory.html). No contiene reglas: están en la metodología, en la especificación y en las decisiones, y aquí solo se dice dónde buscarlas. Para empezar a trabajar en el repositorio, [el arranque](arranque-claude.md).

**Estado:** 27 de noviembre de 2026, plugin sf 1.9.11.

## Dónde se escribe la SF

La SF se escribe en un solo sitio, este repositorio. Llega a los proyectos de una sola forma: el plugin `sf` de Claude Code. La propia SF se lleva como los demás proyectos, con su `.sf/proyecto.json` y su `sf/` («La SF se lleva como los demás proyectos», 299); en ella las reglas y `sf:orquestacion` las entrega el mod igual que en cualquier otro («En la SF, las reglas y sf:orquestacion las entrega el mod, como en los demás proyectos»), y lo del plugin sí es del proyecto, así que la regla de «lo que es de la SF» no va.

El repositorio es la **fuente**: aquí se crea y se modifica todo, pero ningún proyecto lo usa directamente. Los proyectos usan la **copia instalada**: la versión publicada, que Claude Code descarga en su caché y que no se edita nunca. Para ver un cambio antes de publicarlo está el **modo prueba** (en «Publicación del plugin»).

El circuito se cierra al revés. Lo que falla o falta en la SF se lleva a una sesión de la SF y allí se convierte en propuesta. Solo cuando el propietario la aprueba se aplica en la fuente y se publica una versión nueva. Hasta que no se publica, un cambio en la fuente no llega a los proyectos.

![](diagramas/sf-mapa.diagrama)

## Componentes del plugin

La fuente del plugin `sf` está en la carpeta `plugins/sf/` de este repositorio. Al publicar una versión, todo su contenido queda disponible en los proyectos. Las rutas son relativas a esa carpeta. Qué hace cada pieza, para quien la usa, está en «Qué lleva el plugin» de [Cómo funciona la Software Factory](como-funciona-la-software-factory.html).

### Skills y dónde están

::: tarjetas 2 plegables
#### Metodología {color=turquesa icono=documento}

La skill del método y su guía común de esquemas SVG.

Dónde
:   `skills/metodologia/`, con `references/desarrollo-de-proyectos.md` y `references/diagramas-svg.md`

#### Orquestación {color=turquesa icono=dialogo}

Las reglas del agente principal, que entrega el mod.

Dónde
:   `skills/orquestacion/`

#### Flujo, incorporación y configuración {color=turquesa icono=rama}

`sf:flujo_tareas`, `sf:incorporar_proyecto_a_sf`, `sf:configurar_proyecto` y `sf:comprobar_instalacion`.

Dónde
:   `skills/flujo_tareas/`, `skills/incorporar_proyecto_a_sf/`, `skills/configurar_proyecto/`, `skills/comprobar_instalacion/`

#### Documentos {color=naranja icono=documento}

`sf:crear_documentos` y, encima, una skill por tipo, cada una con su `perfil.json` y un envoltorio de pocas líneas: `documento_vision` (también los explicativos), `documento_fundacional` e `informe_deliberativa`.

Dónde
:   `skills/crear_documentos/` y la carpeta de cada tipo

#### Estilo y diagramas {color=naranja icono=lupa}

`sf:fijar_estilo` (con `scripts/estilo.py`) y `sf:diagramas`.

Dónde
:   `skills/fijar_estilo/`, `skills/diagramas/`

#### Fases del método {color=turquesa icono=codigo}

`sf:diseno_interfaz`, `sf:definicion_tecnica` e `sf:infografia_tecnica`.

Dónde
:   `skills/`, una carpeta por skill
:::

**Las plantillas.** Las comunes, en `templates/claude-sf.md`, y las del método, en `templates/claude-sf-metodologia.md`. Además, las estructuras de carpetas por perfil técnico (`templates/estructuras/`) y el `propuestas.md` vacío que crea la incorporación.

**El generador de documentos.** `crear_documentos/scripts/documento_a_html.py`, único y determinista, con el estilo del proyecto. La maqueta antigua de la visión se retiró: regenerar un documento hecho con ella ya lo migra, con los mismos enlaces («Cada documento se migra al generador único cuando se vuelve a tocar»). También el índice de las decisiones y `DESARROLLO.md` salen de él.

### Herramientas

Todas en `tools/`, en Python y sin Claude.


| Herramienta | Qué hace |
| --- | --- |
| `cola.py` | Única vía para escribir `.sf/peticiones.json`, con `sf:flujo_tareas`. Bloquea la cola (`peticiones.lock`), guarda una copia antes (`copias/`) y pasa lo que sale a `historial.jsonl`. Si Windows tiene la cola abierta, reintenta unos dos segundos antes de fallar. Desde el worktree de un subagente sin cola, encuentra la del proyecto. También registra las decisiones (`decision`), escribe la parte fija del encargo de un subagente (`encargo`), dice si una tarea comparte archivos con otra (`choques`) y sube `develop` con la revisión (`subir`). |
| `cola_sesion.py` | El lanzador: el panel lo copia a `~/.claude/sf/cola.py`, y Claude lanza siempre esa ruta, que pasa la orden a la copia de `cola.py` de su sesión, la misma que usa el panel. Así Claude nunca usa el `cola.py` de la rama activa. |
| `configuracion.py` | Enseña y comprueba `.sf/proyecto.json` (`ver`) y detecta las convenciones del repositorio (`detectar`). Solo lee. |
| `incorporacion.py` | Anota el progreso de una incorporación, paso a paso, en `~/.claude/sf/incorporacion-<carpeta>.json`, fuera del proyecto, para que el panel lo enseñe. |
| `plugin_sf.py` | La versión del plugin: compara la que corre, la instalada y la publicada (`ver`) y la pone al día (`actualizar`). La usan la incorporación, antes de nada, y `sf:comprobar_instalacion`. |
| `revision_publica.py` | Revisa lo que sale al publicar: secretos, datos personales y archivos internos en los commits nuevos. La lanzan RELEASE y el push de `develop`. |
| `indice_decisiones.py` | Regenera el índice de las decisiones; con `--html`, también su `README.html`, que no se versiona. |
| `kit_documentos/` | La barra y las herramientas de los documentos HTML: buscador, notas, lectura, edición y «Diagramas». |

### Mods

Hay un solo mod, el **mod de estado**, en `hooks/`. Qué hace, desde el lado de quien lo usa, está en «El mod de estado» y «El panel de la SF» de [Cómo funciona la Software Factory](como-funciona-la-software-factory.html), y se detalla en [Cómo funciona el panel](como-funciona-el-panel.html). Aquí, sus módulos:

| Módulo | Qué hace |
| --- | --- |
| `register.tsx` | Engancha el mod a los eventos de la sesión y registra `/sf` y las órdenes `/sf_…`. |
| `panel.tsx` | Pinta el panel y la caja sobre el prompt, y atiende sus clics. |
| `pulsable.tsx` | Módulo de superficie para la app de escritorio: la línea de una tarea, sus órdenes y la marca del subagente, que se pulsan como en el terminal. |
| `cola.ts` y `lectura.ts` | Lanzan `cola.py` y hacen RELEASE, ACTUALIZAR y REFRESCAR; leen la cola, el historial, las propuestas, la incorporación y la rama activa. |
| `configuracion.ts` | Lee `.sf/proyecto.json` con sus valores por defecto. |
| `contexto.ts` | Entrega las reglas y la orquestación, otra vez si cambian al recargar el plugin, y añade la regla de lo que es de la SF al prompt de sistema. |
| `avisos.ts`, `subagentes.ts` y `memoria.ts` | Avisan de lo cambiado desde el panel y de los subagentes que faltan o están sin recoger, arrancan la sesión y guardan lo avisado en `.sf/subagentes.json`. |
| `foco.ts` | La sugerencia tras 10 minutos sin escribir y el freno a los menús con texto a medio escribir. |
| `latido.tsx` | Una sola sesión con la SF por proyecto: el latido en `~/.claude/sf/latido-<carpeta>.json`, la sesión apagada, `/sf_forzar_activa` y `/sf_forzar_inactiva`. |
| `control.ts` | Bloquea la escritura en otro proyecto, también en un clon del mismo repositorio, que cuenta como él, y en la cola desde un subagente. |
| `identidad.ts` | Pone a la sesión el color del primario del estilo del proyecto y su nombre. |
| `bienvenida.ts`, `logo.ts` y `tema.ts` | La bienvenida en una carpeta sin SF, el logo y el tema claro u oscuro de Claude Code. |
| `revision.ts` y `python.ts` | La revisión antes de RELEASE y el intérprete de Python de la máquina. |
| `prueba.ts` | Lleva el modo prueba, solo en la SF. |
| `emergentes.ts` y `pantalla.ts` | Los avisos emergentes y el aviso de que, sin pantalla completa, los clics no llegan. |
| `estilo.ts` y `constantes.ts` | Colores, anchos, rutas y nombres comunes. |

## Componentes de la SF fuera del plugin

No se instala con el plugin: se queda en el repositorio de la SF, como en cualquier proyecto. Lo que sirve a los usuarios viaja en el plugin; lo propio de desarrollarla se queda aquí.

::: tarjetas 3 plegables
#### Especificación y visiones {icono=documento}

Qué hay que construir en la SF y la SF contada desde cada perspectiva.

Dónde
:   `docs/specs/funcional/software-factory.md` y `docs/specs/vision/`

#### Documentos de la SF {icono=carpeta}

Las decisiones del propietario, una por archivo con su índice; las propuestas aún sin decidir; y los informes, como «Configuración inicial» o «Tipos de tarea».

Dónde
:   `sf/decisiones/`, `sf/propuestas.md` y `sf/informes/`

#### Explicativos {icono=lupa}

Este documento, [Cómo funciona la Software Factory](como-funciona-la-software-factory.html), [Cómo funciona el panel](como-funciona-el-panel.html), [Cómo funcionan los estados](como-funcionan-los-estados.html), la mejora continua y el uso del panel.

Dónde
:   `docs/`

#### Identidad y estilo {icono=check}

El estilo de los documentos de la SF, «Áureo», y su logo; la web y los documentos toman de él sus colores y su letra.

Dónde
:   `docs/identidad/estilo.json` e `identidad.json`

#### La web {icono=codigo}

La página comercial, en inglés y castellano, que GitHub Pages publica con cada push a `main` que la toca. `DESARROLLO.md` es el índice interno, para quien trabaja en la SF.

Dónde
:   `site/`, `.github/workflows/pages.yml` y `DESARROLLO.md`

#### JKanban {icono=rama}

El tablero de tareas, con un MCP para la SF. Es opcional y aún no está conectado.

Dónde
:   `D:\Projectes\JKanban`
:::

## Flujo de mejora de la SF

Ninguna mejora de la SF salta de la idea al código: pasa por una propuesta y por una decisión del propietario.

![](diagramas/sf-mejora.diagrama)

**De dónde viene.** En la SF, una mejora es una petición más: va a la cola si ya está clara, o a `sf/propuestas.md` si hay que decidirla. Lo que se detecta en otro proyecto no se escribe allí en la SF: el propietario lo trae a una sesión de la SF («Lo que es de la SF», en [Cómo funciona la Software Factory](como-funciona-la-software-factory.html)). Con el kanban conectado, la tarea permanente **Mejorar la Software Factory**, del proyecto **SoftwareFactory**, las recogerá.

**La propuesta.** En `sf/propuestas.md` la mejora se convierte en una propuesta: el cambio concreto, su beneficio, su impacto y cómo se comprobará. Ahí se detiene hasta que el propietario la aprueba, la ajusta o la descarta. Registrar o preparar una propuesta no autoriza aplicarla; una instrucción directa del propietario sí, dentro de su alcance.

**La decisión.** Lo aprobado pasa a un archivo de `sf/decisiones/` con su porqué, registrado con `cola.py decision`. Lo descartado queda en «Descartadas», con el motivo.

**La aplicación.** Una decisión se aplica en su tarea, en la fuente: metodología, especificación, skills, plantillas o código. Si el cambio afecta al plugin, se publica una versión nueva (abajo). Si no lo toca, basta con el squash a `develop`, y llega a `main` con la siguiente publicación.


### Publicación del plugin

Se desarrolla en `develop`; `main` es lo que instalan los proyectos.

1. Cada cambio, en una tarea, con su rama `feature/NN-nombre` desde `develop` (el ciclo, en «Flujo de trabajo en un proyecto» de [Cómo funciona la Software Factory](como-funciona-la-software-factory.html)).
2. Probar en la rama con el plugin en **modo prueba** (abajo).
3. Comprobar con `claude plugin validate plugins/sf`, `claude plugin test plugins/sf` y las pruebas de Python de `plugins/sf/tests/`.
4. Con el OK del propietario, cerrar la tarea: un commit por tarea en `develop`, con sus pasos en el cuerpo y «(N)» al final del título. Cada decisión es un archivo propio, así que dos ramas no chocan al añadirlas; el índice se junta sin choques (`merge=union`).
5. Publicar con RELEASE, que funciona como en cualquier proyecto («Publicar una versión del proyecto», en «Flujo de trabajo en un proyecto» de [Cómo funciona la Software Factory](como-funciona-la-software-factory.html)). En la SF, la revisión de lo que sale la hace `revision_publica.py` («Revisión antes de publicar: bloquear en público, preguntar en privado, y revisar también al subir develop») y el manifiesto es `plugins/sf/.claude-plugin/plugin.json`.
6. Actualizar la copia instalada con ACTUALIZAR o REFRESCAR, como cualquier usuario («Actualizar la SF»).

**Modo prueba** (solo en la SF). Ver un cambio del plugin sin commit ni publicación. En este repositorio, la cabecera del panel lleva la etiqueta de prueba: atenuada, se usa el plugin publicado; en naranja, la copia de trabajo de `plugins/sf`. Un clic, o `/sf_prueba`, cambia de uno a otro: el mod escribe en `.claude/settings.local.json` (fuera de git) qué plugin está activo, `sf@softwarefactory-dev` o `sf@softwarefactory`, y lanza `/reload-plugins`. Al entrar en una sesión y al cerrarla, siempre desactivado: el mod lo apaga una vez por sesión y apunta en `.sf/prueba.json` la sesión que ya lo apagó. Fuera del repositorio de la SF, como en una carpeta de prueba con el catálogo local, no lo apaga: manda lo que diga su `.claude/settings.local.json`.

Preparación, una vez por equipo: el catálogo local `softwarefactory-dev`, en `D:/Projectes/.claude-plugin/marketplace.json`, fuera del repositorio, con el plugin `sf` en `./SoftwareFactory/plugins/sf`. Claude Code carga en su sitio, sin copiarlo a la caché, el plugin de un catálogo de carpeta; no acepta la ruta absoluta, la que sube de carpeta ni un enlace, y dos catálogos no pueden llamarse igual: por eso está en la carpeta de arriba. Después, en el repositorio: `claude plugin marketplace add D:/Projectes --scope local` y `claude plugin install sf@softwarefactory-dev --scope local`. Sin el catálogo registrado, el panel no muestra la etiqueta.

## Cómo se mantienen los documentos

Si cambia una pieza de la SF o la forma de publicarla, se actualizan este documento y, si es del panel, [Cómo funciona el panel](como-funciona-el-panel.html); si cambia lo que de ella ve quien la usa, también [Cómo funciona la Software Factory](como-funciona-la-software-factory.html). Lo que hace falta para seguir desarrollando la SF está en [el arranque](arranque-claude.md). Cada documento se regenera con el generador único de `sf:crear_documentos` y se comprueba con `comprobar_documento.py`.

## Decidido y aún sin aplicar

Estas decisiones cambian piezas de este mapa, pero el código de la 1.9.11 aún no las lleva. Hasta que se apliquen, vale lo descrito arriba.

- **«Finalizar deliberación».** Una deliberativa mostrará ese botón en lugar de Cerrar, con la misma orden («Las deliberativas se cierran con «Finalizar deliberación»»). Hoy se cierra con Cerrar.
- **Agentes por familia de tarea.** Un agente del plugin por familia, con las reglas del encargo dentro, solo si la especialización aporta («Agentes del plugin por familia de tarea, solo si la especialización aporta»). Está por valorar en su tarea.
- **Una orden única para regenerar.** Cada cambio de un `.md` regenera su HTML; falta una orden única que elija el generador de cada documento.

## Índice de consulta

<dl class="faq">
<dt>¿Qué falta por construir en la SF?</dt><dd>Especificación, próximos pasos</dd>
<dt>¿Cómo se registra una decisión y dónde se aplica?</dt><dd><code>docs/mejora-continua-a-la-software-factory.md</code> y <code>cola.py decision</code></dd>
<dt>¿Qué reglas recibe un proyecto?</dt><dd><code>plugins/sf/templates/claude-sf.md</code> y <code>claude-sf-metodologia.md</code>, que entrega el mod</dd>
<dt>¿Qué carpetas lleva un proyecto?</dt><dd>Metodología, sección 6, y las plantillas del plugin</dd>
<dt>¿De dónde viene una skill?</dt><dd>La sección «Origen» de una skill adaptada, como <code>sf:diagramas</code>; las externas que se usan tal cual, en las <code>dependencies</code> del <code>plugin.json</code></dd>
<dt>¿Cómo se instala o se publica el plugin?</dt><dd><code>plugins/sf/README.md</code> y este documento</dd>
<dt>¿Cómo empieza Claude a trabajar en la SF?</dt><dd>El <code>CLAUDE.md</code> del repositorio y el arranque, <code>docs/arranque-claude.md</code></dd>
<dt>¿Cómo funciona la SF para quien la usa?</dt><dd><a href="como-funciona-la-software-factory.html">Cómo funciona la Software Factory</a></dd>
</dl>


## Cuestiones pendientes de decisión

Están en [propuestas](../sf/propuestas.md). Lo que más afecta a este mapa:

- **Procedimiento de instalación del plugin**, más allá de las órdenes de `plugins/sf/README.md` (P12).
- **Historial de versiones del plugin**, un CHANGELOG (P13).
- **Organización del repositorio de la SF** (P14).