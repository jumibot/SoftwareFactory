---
antetitulo: Software Factory · Informe de análisis · Octubre 2026
lema: Lo de esta máquina, fuera; // cada caso, probado en su sesión.
subtitulo: Qué tiene el plugin sf que solo vale en esta máquina o para el propietario, qué cambia en la incorporación con las tareas en marcha y el guion para probar cada caso en su proyecto.
version: Versión 1.0 · 31/10/2026
estado: Propuesta · Tarea 171
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
tipo: Informe de análisis
pie: Propuesta de la tarea «Repensar instalación y uso del plugin» (171). Sale de leer plugins/sf en develop (sf 1.2.0), los proyectos de prueba en solo lectura y el registro de uso de la SF. Espera la decisión del propietario.
---
# Plugin en otros proyectos

## Resumen | Tres bloques que no son del plugin | Resumen {#resumen}

El plugin funciona en los proyectos del propietario porque esta máquina tiene a la vez la fuente de la SF, JKanban y los proyectos en `D:\Projectes`. Para otro usuario, o en otra máquina, fallan tres cosas.

**La realimentación a la SF.** El registro de uso y las mejoras se escriben en la copia local del repositorio de la SF, que apunta `~/.claude/sf/fuente.json`; y la mejora continua va al proyecto **SoftwareFactory** de JKanban. Quien no desarrolla la SF no tiene ni lo uno ni lo otro.

**Supuestos del repositorio.** El remoto se llama `origin` (PoseTracker usa `PoseTracker`), la firma del commit nombra un modelo fijo y el modo prueba reconoce la SF por el nombre de su carpeta.

**Historia y ejemplos del propietario.** Los `ORIGIN.md` de las skills, con rutas `D:/` y nombres de proyectos; los ejemplos con LecturaFàcil; los comentarios del kit que remiten a OncoCore.

Lo que cambia en la incorporación lo cubren casi entero «Normas y CLAUDE.md en los proyectos» (211), «Diseñar la configuración inicial» (190) e «Incorporar: cierre y ramas según el flujo de tareas» (222). A esta tarea le quedan cinco ajustes propios.

Las pruebas tienen orden: se prueban con el plugin publicado después de esas tareas, no con la 1.2.0.

## Inventario | Qué solo vale aquí o para el propietario | Inventario {#inventario}

Se ha buscado en `plugins/sf/` (skills, tools, hooks, templates, tests, README y manifiesto) cada ruta de Windows, la carpeta del usuario, el nombre del propietario, sus proyectos, JKanban y lo que supone el repositorio de la SF a mano. Las skills de terceros (gsap, three.js, oklch) no tienen nada.

Las propuestas son de cuatro clases: **quitar**, **parametrizar** en `.sf/proyecto.json`, **configuración del usuario** (un `~/.claude/sf/config.json`, que hoy no existe) y **dejar**, cuando es la identidad de la distribución.

### Realimentación a la SF | Lo que más pesa {#realimentacion}

| Dónde | Qué dice | Propuesta |
| --- | --- | --- |
| `templates/claude-sf.md`, 16 | Claude anota en el registro común, `.sf/registro.json` de la SF. | Configuración del usuario: con la fuente de la SF, como hoy; sin ella, en el registro del propio proyecto, o se omite la regla. Lo cambia la tarea de la plantilla. |
| `templates/claude-sf.md`, 17; `skills/metodologia/SKILL.md`, 40 | Las mejoras van al proyecto **SoftwareFactory** del kanban, tarea «Mejorar la Software Factory». | Configuración del usuario: el canal de mejoras (JKanban, issues de GitHub del repositorio de la SF o ninguno). Para otros usuarios, por defecto, issues. |
| `skills/metodologia/references/desarrollo-de-proyectos.md`, 62, 380, 504-506 | Registro de uso común y mejoras en **SoftwareFactory**. | Lo mismo, en la tarea «Actualizar la metodología». |
| `hooks/lectura.ts`, 73-104; `hooks/constantes.ts`, 28-31; `hooks/register.tsx`, 103 | El panel lee el registro y las mejoras de la SF que apunta `~/.claude/sf/fuente.json`, escrito al abrir la SF. | Dejar: sin la SF en la máquina, el bloque SF ENHANCE queda vacío y no falla. Con la configuración del usuario, el registro del proyecto ocuparía su sitio. |
| `hooks/control.ts`, 14-16, 85-87 | Única escritura permitida fuera del proyecto: el registro y las propuestas de la SF. | Dejar, y seguir la ruta configurada si el registro pasa al proyecto. |

### Supuestos del repositorio | Fallan sin avisar {#repositorio}

| Dónde | Qué dice | Propuesta |
| --- | --- | --- |
| `tools/cola.py`, 357; `hooks/cola.ts`, 332, 335; `hooks/lectura.ts`, 263 | Push y «push pendiente» contra `origin`. PoseTracker tiene el remoto `PoseTracker`; un proyecto nuevo, ninguno. | Parametrizar: `remoto` en `.sf/proyecto.json`, por defecto el único remoto que haya o el que siga `develop`; sin remoto, no hay push ni aviso de push pendiente. |
| `tools/cola.py`, 55 | `COAUTOR = 'Co-Authored-By: Claude Opus 5.5 …'` en el commit del cierre. | Quitar el modelo fijo: la firma, de la configuración del usuario o ninguna. Claude Code ya da sus líneas de atribución a Claude, pero el cierre lo hace el CLI. |
| `hooks/prueba.ts`, 89 | El modo prueba se reconoce porque la ruta acaba en `SoftwareFactory/plugins/sf`. | Parametrizar: comparar con la ruta del catálogo `softwarefactory-dev`, no con el nombre de la carpeta. Solo afecta a quien desarrolla la SF. |
| `hooks/prueba.ts`, 12 | El catálogo local está en `D:/Projectes/.claude-plugin/marketplace.json`. | Quitar la ruta del comentario; documentar en la guía de desarrollo de la SF cómo crear el catálogo local. |
| `README.md`, 53 | `claude --plugin-dir D:/Projectes/SoftwareFactory/plugins/sf`. | Quitar la ruta: `<repositorio de la SF>/plugins/sf`. |
| `hooks/cola.ts`, 343-344, 380; `hooks/prueba.ts`, 18; `README.md`, 47 | `sf@softwarefactory` y `jumibot/SoftwareFactory`. | Dejar: es la identidad de la distribución. Si algún día hay forks, leer el catálogo del plugin instalado en vez de fijarlo. |
| `.claude-plugin/plugin.json`, 6 | Autor `jumibot`. | Dejar. |

### Identidad y kanban | Lo que es del propietario {#identidad}

| Dónde | Qué dice | Propuesta |
| --- | --- | --- |
| `skills/incorporar_proyecto_a_sf/SKILL.md`, 3, 29, 31, 73, 84; `types/index.d.ts`, 63 | `kanban` es el proyecto en **JKanban**, obligatorio en el diagnóstico. | Parametrizar: `kanban` opcional; se pregunta solo si la configuración del usuario dice que hay kanban. JKanban se nombra como ejemplo. |
| `skills/incorporar_proyecto_a_sf/SKILL.md`, 30 | El color se elige mirando los `.sf/proyecto.json` de las carpetas vecinas. | Dejar como recomendación, sin dar por hecho que los proyectos son carpetas hermanas. |
| `skills/incorporar_proyecto_a_sf/SKILL.md`, 29; `skills/metodologia/references/desarrollo-de-proyectos.md`, 268 | La descripción la leen el panel, Claude Code Commander y JKanban. | Quitar Commander y JKanban, que no existen para otros; basta «la lee el panel». |
| `hooks/constantes.ts`, 61-63; `README.md`, 19-21; `skills/incorporar_proyecto_a_sf/SKILL.md`, 37-39 | Ejemplos con «LecturaFàcil». | Dejar como ejemplo; si se publica para otros, uno neutro («MiProyecto»). |
| `hooks/lectura.ts`, 453; `hooks/constantes.ts`, 40 | La SF se pinta como «SoftwareFactory», en morado reservado. | Dejar: es la propia SF. |

### Historia y ejemplos | Ruido para otros {#historia}

| Dónde | Qué dice | Propuesta |
| --- | --- | --- |
| `skills/*/ORIGIN.md` (24 archivos) y `tools/kit_documentos/ORIGIN.md` | Procedencia con rutas `D:/Projectes/OncoCore/…`, `D:/SecondMind/…` y proyectos (SmartColdBox, LecturaFàcil, MedRol, SocratIX). Claude no los carga. | Mover las de las skills propias a `docs/referencias/origenes/` de la SF; en el plugin, solo licencia y autoría de las de terceros. |
| `tools/kit_documentos/*.js`, `*.css`, `actualizar_copia.py`; `skills/documento_vision/SKILL.md`, 312 | «Modelo: kit_documentos de OncoCore», «gene_associations». | Quitar las menciones de los comentarios, o pasarlas al origen. |
| `skills/incorporar_proyecto_a_sf/SKILL.md`, 60 | El `CLAUDE.md` de OncoCore como ejemplo de complejo. | Generalizar el ejemplo. |
| `skills/metodologia/references/desarrollo-de-proyectos.md`, 82, 149, 193, 213, 275 | «Primer caso: JKanban», «en LecturaFàcil…», el kanban local multiproyecto es JKanban. | En «Actualizar la metodología»: el kanban como pieza opcional; los casos, como ejemplos. |
| `skills/metodologia/references/*.md` y `skills/orquestacion/references/porque.md` | Enlaces a decisiones y propuestas de `github.com/jumibot/SoftwareFactory`, con número. | Dejar: el repositorio es público. Comprobar que se abre sin sesión de GitHub. |
| `tests/panel.test.tsx`, 493, 1577, 2656 | Rutas y nombres de prueba (`D:/sf`, JKanban). | Dejar: son datos de prueba. Si el paquete publicado no debe llevar `tests/`, excluirlos. |

### Portabilidad | Si se publica para otros {#portabilidad}

**Python.** Las skills y la plantilla dicen `python -I -X utf8 …`; en macOS y Linux suele ser `python3`. El mod ya prueba los dos (`hooks/cola.ts`, 84 y 95); las skills, no.

**Idioma.** Todo el plugin está en español, incluidos los mensajes del panel y de `cola.py`. Para otros usuarios es una decisión aparte, no de esta tarea.

## La incorporación | Qué cambia con las tareas en marcha | Incorporación {#incorporacion}

### Lo que ya cubren otras tareas {#otras}

**«Normas y CLAUDE.md en los proyectos» (211).** Si se elige que el mod entregue las reglas en SessionStart, la incorporación deja de copiar `.sf/claude-sf.md` y de añadir `@.sf/claude-sf.md`, y el caso «actualizar» los quita. Eso elimina el paso 3 de la skill y la comprobación de versión de la copia. Lo hace la 211.

**«Diseñar la configuración inicial» (190).** Lo mínimo (tareas y repo) y lo elegible (metodología, decisiones), su formato en `.sf/proyecto.json` y las preguntas. Con la 211, las reglas entregadas dependen de esa configuración: la 190 debe dar el formato que lea el mod. Lo implementa la 193.

**«Incorporar: cierre y ramas según el flujo de tareas» (222).** Que lo no comprobado pase a Testing con `listo` antes de `a-testing` (fricción de Sprites), sin el OK; el commit de incorporación en `develop`, creando `develop` si no existe (SmartColdBox y Balls solo tienen `main`).

### Lo que queda a esta tarea {#queda}

1. **Proyecto sin git.** El caso nuevo (Sprites empezó así) necesita `git init`, rama `main` con un primer commit y `develop` desde ella. Hoy la skill no lo dice. Puede ir a la 222, que ya trata las ramas: decidir dónde.
2. **Remoto.** Detectar el remoto al incorporar y guardarlo en `.sf/proyecto.json` si no es `origin`; sin remoto, decirlo y no prometer push.
3. **Color y nombre.** La skill dice que el mod los aplica al leer `.sf/proyecto.json`; en SpriteAnimation el propietario tuvo que hacer `/color` y `/rename` a mano. Comprobar en la prueba si el mod no los aplica la primera vez (el archivo aparece con la sesión ya abierta) y, si es así, que la skill los lance o lo diga.
4. **Kanban y realimentación según la configuración del usuario.** La pregunta de `kanban` y la regla de mejoras, solo si hay kanban o canal de mejoras configurado.
5. **Proyecto anterior a la plantilla.** SmartColdBox (sf 0.13) tiene un apartado «Software Factory» escrito a mano que apunta a `D:\Projectes\SoftwareFactory\docs\propuestas.md`, sin `descripcion` en `proyecto.json` y con `.gitignore` incompleto. La skill ya prevé quitar el apartado; la 211 lo repite. Aquí solo se comprueba en la prueba.

**Fuera de la incorporación.** La numeración de `indice_decisiones.py --nombre`, que repite números entre ramas y entre dos peticiones seguidas (fricciones de Sprites y SpriteAnimation), es una tarea del script, no de esta.

## Guion de prueba | Una sesión por proyecto | Prueba {#prueba}

**Cuándo.** Con el plugin publicado tras la 211, la 193 y la 222, y con lo de esta tarea aplicado. Probar antes con la 1.2.0 prueba lo que va a cambiar.

**Cómo, en cada sesión.** Abrir Claude Code en la carpeta del proyecto con el plugin publicado, nunca con `--plugin-dir`. Comprobar la versión en la cabecera del panel. Pedir «incorpora este proyecto a la SF» (o «ponlo al día con la SF»). Lo que falle, al registro de uso (bloque SF ENHANCE), no a la SF desde esa sesión.

**Antes de empezar.** Árbol limpio (`git status` sin cambios) en el proyecto. SmartColdBox tiene ahora un borrado sin commit (`docs/specs/vision/SMB_VIAL_Justificacion.html`): resolverlo antes.

### Caso nuevo · carpeta vacía {#nuevo}

Sprites ya se incorporó así con la 1.1.0 (commit «Incorporado a la SF 1.1.0»). Para repetir el caso, una carpeta nueva y vacía, sin git (por ejemplo, `D:\Projectes\PruebaSF`).

1. Pedir la incorporación. **Mirar:** el menú propone «Nuevo» como recomendado y pregunta la configuración inicial (tareas y repo siempre; metodología y decisiones, elegibles).
2. Elegir la configuración completa. **Mirar:** crea git con `main` y `develop`, `.sf/proyecto.json` con lo elegido, `.gitignore` con lo de la SF, `docs/decisiones/` con su índice y `merge=union`.
3. **Mirar** el `CLAUDE.md`: según la 211, sin líneas de la SF (o con `@.sf/claude-sf.md`, si se decide la forma A).
4. **Mirar** el panel: nombre, color de la sesión sin tocar nada, fase 1/7 Visión, rama `develop`.
5. Pedir una tarea de prueba («añade un README»). **Mirar:** va a la cola, se pone en curso con su rama, se cierra por squash en `develop`; sin remoto, sin error de push.
6. `/compact` y preguntar «¿qué reglas sigues?». **Mirar:** sigue cargada la orquestación.

### Caso existente con metodología · Balls {#balls}

Java, en GitHub (`origin`), solo `main`, sin `CLAUDE.md` ni `docs/`.

1. Pedir la incorporación. **Mirar:** propone «Existente» con lo que lo delata.
2. Configuración completa. **Mirar:** crea `develop` desde `main`; no mueve `src/`; propone el plan de `docs/` sin aplicarlo solo.
3. **Mirar:** `estado.json` con la fase real y en `pendientes` lo que falta (visión, especificación, guías).
4. Tarea de prueba hasta cerrarla. **Mirar:** push a `origin develop`.

### Caso existente solo tareas y repo · PoseTracker {#posetracker}

Python, `CLAUDE.md` propio de 92 líneas, en `develop`, remoto llamado `PoseTracker`.

1. Pedir la incorporación y elegir solo tareas y repo. **Mirar:** no crea `docs/decisiones/` ni fases; no toca su `CLAUDE.md` salvo lo que diga la 211.
2. **Mirar** el panel: sin fases ni Documentos; tareas y rama, sí.
3. Tarea de prueba hasta cerrarla. **Mirar:** el push va al remoto `PoseTracker`, no a `origin`, y el panel no da push pendiente falso.
4. Ampliar la configuración («añade la metodología»). **Mirar:** pregunta lo que falta sin rehacer lo hecho.

### Versión anterior · SmartColdBox {#smartcoldbox}

sf 0.13, sin `descripcion`, apartado «Software Factory» a mano en el `CLAUDE.md`, `docs/decisiones-y-pendientes.md`, solo `main`.

1. Pedir «ponlo al día con la SF». **Mirar:** propone «Actualizar» y diagnostica primero.
2. **Mirar:** pide la descripción; completa el `.gitignore` (lock, historial, copias, worktrees); crea `develop`.
3. **Mirar:** propone quitar el apartado «Software Factory» (con la ruta `D:\`) y no lo quita sin el OK.
4. **Mirar:** propone migrar `decisiones-y-pendientes.md`, que no es el `docs/decisiones.md` que la skill sabe migrar: anotar cómo lo resuelve.
5. **Mirar:** commit «Actualizado a la SF X.Y.Z» en `develop`.

### Versión anterior reciente · Sprites {#sprites}

sf 1.1.0, con la línea `@.sf/claude-sf.md`, ramas de tareas abiertas.

1. Con las ramas de tarea cerradas o sin cambios, pedir «ponlo al día con la SF». **Mirar:** con la forma B de la 211, quita la línea y `.sf/claude-sf.md`; sube `sf` en `proyecto.json`.
2. **Mirar:** si hay trabajo en curso, no reorganiza nada y lo dice.

### Diagnóstico · cualquiera {#diagnostico}

En PoseTracker antes de incorporarlo, pedir «diagnostica si cumple la SF». **Mirar:** no escribe nada (`git status` igual que antes) y el informe dice qué está bien, qué falta y qué propone.

## Lo que decide el propietario | Preguntas | Decidir {#decidir}

1. ¿Se crea una configuración del usuario (`~/.claude/sf/config.json`) con la ruta de la SF, el kanban, el canal de mejoras y la firma de los commits, o esos valores se preguntan por proyecto en `.sf/proyecto.json`?
2. Sin la SF en la máquina, ¿el registro de uso va al propio proyecto, a issues de GitHub del repositorio de la SF o no se lleva?
3. ¿`kanban` pasa a opcional, preguntado solo si hay kanban configurado?
4. ¿La firma del commit de cierre de `cola.py` sale de la configuración o se quita?
5. ¿Los `ORIGIN.md` de las skills propias salen del plugin a `docs/referencias/` de la SF?
6. ¿Crear git y `develop` en un proyecto sin git va a esta tarea o a la 222?
7. ¿Se da por hecha la prueba del caso nuevo en Sprites (incorporado con la 1.1.0, con sus fricciones en el registro) y se repite después en una carpeta vacía nueva?
8. ¿Se prueba solo después de publicar la 211, la 193 y la 222, como propone el guion?
