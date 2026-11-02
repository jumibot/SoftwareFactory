---
antetitulo: Software Factory · Informe de análisis · Noviembre 2026
lema: El plugin se adapta al proyecto; // el proyecto no se adapta al plugin.
subtitulo: Qué impone hoy la SF a un proyecto que se incorpora, qué puede detectar y respetar, qué es lo mínimo que tiene que escribir y dónde, y cómo quedan las decisiones pendientes de la incorporación.
version: Versión 1.1 · 02/11/2026
estado: Decidido · Tarea 222
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
tipo: Informe de análisis
pie: Propuesta de la tarea «Incorporar un proyecto sin cambiarlo: el plugin se adapta al proyecto» (222). Sale de leer plugins/sf en develop (skill de incorporación, cola.py, el mod), las decisiones 138, 140, 156, 167, 171 y 187, los informes «Configuración inicial» y «Plugin en otros proyectos», y los proyectos JKanban, SmartColdBox, Sprites, sprite_animation, OncoCore y PoseTracker en solo lectura. Decidido por el propietario el 02/11/2026 (decisiones 201 a 209); la sección «Decidir» recoge lo elegido y «Tareas», cómo se reparte.
---
# Incorporar sin cambiar el proyecto

## Resumen | Detectar, guardar y respetar | Resumen {#resumen}

Un colega del propietario: «el plugin se tiene que adaptar al proyecto y no el proyecto al plugin». Hoy la incorporación hace lo contrario: crea ramas, carpetas y archivos con los nombres de la SF, reorganiza `docs/` y toca `.gitignore` y `.gitattributes`.

La propuesta separa dos cosas. El **mecanismo** de la SF sigue fijo: la cola y sus estados, una rama por tarea, el número de la tarea en cada commit, el registro de decisiones. Las **convenciones** se detectan y se respetan: cómo se llaman las ramas, dónde están los documentos y las decisiones, en qué idioma se escribe, cómo son los commits.

Las convenciones se detectan al incorporar, se confirman en un solo menú y se guardan en `.sf/proyecto.json`. El panel, `cola.py` y las skills las leen de ahí en lugar de suponer `develop`, `main`, `origin` y `docs/decisiones/`.

Lo único que la SF escribe en el repositorio es `.sf/proyecto.json`. La cola, el estado y el historial pueden vivir en `.git/sf/`, que ya comparten todos los worktrees y que git nunca versiona. Así no hace falta tocar `.gitignore`.

> [!aviso]
> Lo decidido corrige la propuesta en tres puntos: el modelo de ramas no se adapta, siempre `develop` («El manejo del repositorio no se negocia: siempre develop», 205); las decisiones van siempre en `sf/decisiones/`, con el formato de la SF («Las decisiones son material de la SF: siempre en sf/decisiones/», 208); y la cola se queda en `.sf/`, con `.gitignore`, mientras los documentos de la SF pasan a `sf/` («Los documentos de la SF van en la carpeta sf/», 203). El resto del análisis se conserva como antecedente; lo que manda está en «Decidir».

## Inventario | Qué impone hoy la SF y qué se puede hacer con cada cosa | Inventario {#inventario}

Tres respuestas posibles: **fijo** (sin ello no hay SF), **adaptar** (la SF lo detecta y usa lo del proyecto) y **opcional** (solo si el propietario lo elige).

### Repositorio

| Qué impone hoy | Dónde | Casos reales | Propuesta |
| --- | --- | --- | --- |
| Rama `develop` de integración | `cola.py` (unas 15 veces), `cola.ts`, `lectura.ts` | SmartColdBox solo tiene `main`; PoseTracker solo `develop` | Adaptar: la rama de integración es la que haya (`develop` si existe; si no, la principal). |
| Rama `main` de publicación | `cola.ts` (RELEASE) | PoseTracker no tiene; JKanban publica con `release/vX.Y.Z` y PR | Adaptar: la de publicación, o ninguna (se publica con tag en la de integración). |
| Ramas `feature/NN-nombre` | `cola.py` `rama` | JKanban usa `feature/*` sin número | Fijo que haya una por tarea; adaptar el patrón del nombre. |
| Squash al cerrar | `cola.py cerrar` | JKanban integra por PR en GitHub | Fijo de momento: squash o merge local. PR, más adelante (riesgos). |
| Push a `origin` | `cola.py`, `cola.ts` | PoseTracker: remoto `PoseTracker` | Adaptar (ya propuesto en «Configuración inicial»). |
| Título del commit `Texto (N)` | `cola.py` cierre; el panel busca `(N)` en `develop` | JKanban: `feat(web): …`; OncoCore: inglés | Fijo el número de tarea; adaptar dónde va (ver «Convenciones»). |
| `Co-Authored-By` con el modelo fijo | `cola.py` `COAUTOR` | — | Quitar el modelo fijo (ya en «Plugin en otros proyectos»). |
| Versión en `plugin.json` o solo tag | RELEASE | — | Adaptar (ya en «Configuración inicial»). |

### Archivos y carpetas

| Qué impone hoy | Propuesta |
| --- | --- |
| `.sf/proyecto.json`, versionado | Fijo: es la marca de que el proyecto está bajo la SF y guarda sus convenciones. |
| `.sf/estado.json`, `peticiones.json`, `.lock`, `historial.jsonl`, `copias/` | Fijo que existan; pueden salir del árbol de trabajo a `.git/sf/` («Huella»). |
| Líneas en `.gitignore` | Sobran si lo anterior va a `.git/sf/`; `.claude/worktrees/` va a `.git/info/exclude`, que es local. |
| `merge=union` en `.gitattributes` | A `.git/info/attributes`, también local. Solo hace falta si el índice de decisiones lo genera la SF. |
| `docs/decisiones/README.html`, generado por el panel | Fuera del repositorio: a una caché del plugin. |
| `docs/decisiones/` creada vacía al incorporar | Adaptar: se usa la carpeta o el archivo que ya tenga el proyecto; si no tiene, se crea al registrar la primera decisión. |
| `docs/propuestas.md` | Opcional: `cola.py` ya funciona sin él. |

### Documentos

| Qué impone hoy | Casos reales | Propuesta |
| --- | --- | --- |
| Estructura común de `docs/` (`specs/vision`, `specs/funcional`, `specs/tecnica`, `guias/`…), leída por el panel con rutas fijas | OncoCore: `_docs/` y `doc/`; JKanban: `docs/architecture.md` en inglés | Adaptar: un mapa de papel a ruta. El panel enseña lo que el mapa dice. |
| Reorganizar `docs/` con `git mv` | — | Opcional: solo si el propietario lo pide, como tarea normal. Nunca en la incorporación. |
| Decisiones una por archivo `NNN-AAAA-MM-DD-titulo.md` | SmartColdBox: un solo `decisiones-y-pendientes.md` | Adaptar dentro de lo soportado (ver «Convenciones»). |
| Visión, especificación, devslices, `estado.json` | — | Opcional: es la metodología, elegible desde la decisión 138. |

### Instrucciones

| Qué impone hoy | Propuesta |
| --- | --- |
| Línea `@.sf/claude-sf.md` y copia de la plantilla | Ya decidido que no («El panel entrega las reglas y la orquestación en los proyectos», 187). |
| Choques con el `CLAUDE.md` resueltos por el propietario uno a uno | Se mantiene: manda la regla del proyecto mientras no se decida otra cosa. Muchos choques desaparecen si la SF lee las convenciones en lugar de imponerlas. |
| Textos que escribe Claude en español | Adaptar: el idioma del proyecto para lo que queda en él (commits, decisiones, documentos). La interfaz de la SF sigue en español. |
| Kanban obligatorio | Opcional (ya en «Configuración inicial»). |

## Convenciones | Cómo se detectan, dónde se guardan y quién las lee | Convenciones {#convenciones}

### Qué se detecta y cómo

- **Rama de integración:** `develop` si existe; si no, la rama por defecto del remoto (`origin/HEAD`), o la única.
- **Rama de publicación:** `main` o `master` si existe y no es la de integración; si no, ninguna.
- **Patrón de rama de tarea:** el de las ramas existentes (`feature/*`, `feat/*`); si no hay, `feature/{n}-{nombre}`.
- **Remoto:** el único, o el que sigue la rama de integración.
- **Idioma:** el del README, el `CLAUDE.md` y los últimos commits.
- **Formato de commit:** «conventional commits» si la mayoría de los últimos 50 títulos siguen `tipo(ámbito): `; si no, libre.
- **Documentos:** la carpeta (`docs/`, `doc/`, `_docs/`) y, dentro, los papeles por nombre (`vision`, `spec`, `architecture`, `guias`, `install`…).
- **Decisiones:** `docs/decisiones/`, una carpeta `adr/`, un archivo único con «decisiones» en el nombre, o nada.
- **Versión:** el manifiesto del stack (ya en «Configuración inicial»).

Nada se da por bueno sin confirmar. Se enseña en un menú, con lo detectado como recomendado y lo que lo delata.

### Dónde se guarda

En `.sf/proyecto.json`, en el bloque `config` que propone «Configuración inicial», ampliado. Lo que falta vale lo de hoy, así los proyectos ya incorporados no cambian. Tras lo decidido, el bloque no lleva ramas (205) ni decisiones (208), que son fijas, ni de momento el mapa de documentos («Lo que queda abierto»). La incorporación escribe siempre lo detectado, aunque coincida.

```json
{
  "sf": "1.4.0",
  "proyecto": "JKanban",
  "descripcion": "Kanban propio con API y MCP",
  "color": "blue",
  "config": {
    "metodologia": false,
    "remoto": "origin",
    "idioma": "en",
    "commits": { "quien": "claude", "formato": "conventional", "tarea": "trailer" },
    "version": null
  }
}
```

### El número de tarea, sin imponer el título

Hoy el panel reconoce una tarea cerrada por `(N)` al final del título en `develop`. Eso choca con conventional commits y con títulos en inglés.

Propuesta: un *trailer* de git al final del mensaje, `SF-Tarea: 222`. El título sigue la convención del proyecto; el panel y `cola.py` leen el trailer con `git log --format=%(trailers:key=SF-Tarea)`. En los proyectos ya incorporados se sigue aceptando `(N)`.

### Quién las lee

- **`cola.py` y el mod:** una sola función cada uno que lee `config` con sus valores por defecto. Cada `'develop'`, `'main'`, `'origin'` y `docs/…` fijo pasa por ella. Es trabajo mecánico pero amplio: unas 30 apariciones.
- **Las skills:** no leen el JSON una a una. El mod ya va a entregar las reglas al empezar la sesión (decisión 187); añade un bloque corto «Convenciones de este proyecto» generado de `config`: «la rama de integración es `main`; las decisiones van en `docs/adr/`; escribe en inglés». Las skills dicen «la rama de integración», no `develop`.
- **`indice_decisiones.py`:** recibe la ruta de `config` y no genera índice si la forma es de archivo único.

## Huella | Lo mínimo que se escribe y dónde | Huella {#huella}

### En el repositorio, versionado

- **`.sf/proyecto.json`.** Imprescindible: identidad y convenciones, compartidas con quien clone el repositorio. Es un archivo nuevo en una carpeta nueva; no cambia nada existente.
- **Las decisiones**, cuando se registra la primera, donde y como diga `config`.
- **El trabajo de cada tarea**, que es el del proyecto.

### En `.git/sf/`, sin versionar

La cola, su lock, el historial, las copias y `estado.json`. Ventajas:

- git no versiona nada dentro de `.git/`: no hace falta `.gitignore`.
- Es la carpeta común de todos los worktrees (`git rev-parse --git-common-dir`): los subagentes ven la misma cola sin pasar `--raiz`.
- Se pierde igual que hoy al clonar de nuevo: hoy también está fuera de git.

Contra: deja de verse en el explorador de archivos y hay que migrar las colas actuales (lo hace el caso «actualizar»).

### En `.git/info/`, local

`exclude` para `.claude/worktrees/` y `attributes` para `merge=union`, si hace falta. Son de cada clon, como hoy son de cada máquina los worktrees.

### Fuera del proyecto

En `~/.claude/sf/`: el registro de uso, la configuración del usuario («Plugin en otros proyectos») y la caché del índice html de decisiones.

### La alternativa radical

Ni siquiera `.sf/proyecto.json` en el repositorio: todo en `.git/sf/` o en `~/.claude/sf/proyectos/`. Huella cero. Pero las convenciones no viajan con el repositorio: otra máquina o un colaborador vuelve a incorporar, y el panel de otro clon no sabe que el proyecto es de la SF.

## Pendientes | Las tres decisiones paradas, bajo el principio | Pendientes {#pendientes}

### Crear `develop` si el proyecto no la tiene

Desaparece. La rama de integración es la que ya tenga el proyecto: `main` en SmartColdBox, `develop` en PoseTracker. Las ramas de tarea salen de ella y vuelven a ella. Crear `develop` se ofrece solo si el propietario quiere separar integración y publicación.

### Los movimientos de documentos, en otra tarea

Desaparece también como parte de la incorporación: la SF mapea en lugar de mover. Reorganizar `docs/` pasa a ser una petición más del propietario, si la quiere, con su tarea y su rama como cualquier otra.

### Escribir `.sf/proyecto.json` antes de anotar la tarea

Cambia de naturaleza. La incorporación ya no es una tarea con rama: escribe un archivo nuevo y, como mucho, la primera decisión. Es configurar la SF, no trabajar en el proyecto.

Propuesta: se escribe `.sf/proyecto.json`, la cola empieza a existir y la incorporación queda como su primera entrada, ya cerrada, con un solo commit en la rama de integración («Incorporado a la SF X.Y.Z»), o el archivo sin commit si los commits los hace el propietario. Así el orden deja de ser un problema.

Alternativa: mantenerla como tarea con rama, como hoy. Más coherente con el flujo, pero una rama y un squash para un solo archivo.

## Riesgos | Dónde adaptarse cuesta y dónde conviene imponer | Riesgos {#riesgos}

### Lo que cuesta

- **Combinaciones.** Cada convención multiplica los casos: integración igual a publicación, sin publicación, sin remoto. `cola.py` tiene pruebas para el caso SF; cada valor nuevo pide las suyas.
- **Formatos.** Soportar ADR, MADR, archivo único y la forma SF en `indice_decisiones.py` son cuatro lectores y escritores. Propuesta: dos formas al principio, «un archivo por decisión» (en cualquier carpeta, con la plantilla SF) y «archivo único» (se añade una sección al final). Lo demás, cuando un proyecto lo traiga.
- **Integración por PR.** JKanban integra por PR en GitHub. Pedirlo en `cola.py cerrar` es otro flujo (push de la rama, `gh pr create`, esperar el merge). Propuesta: no soportarlo todavía; el proyecto elige squash local o se queda con su flujo y la SF no cierra.
- **Detección equivocada.** Un repositorio con ramas viejas engaña. Por eso todo se confirma.
- **Migración.** Cola a `.git/sf/` y trailer en vez de `(N)` cambian los proyectos ya incorporados: hay que aceptar las dos formas un tiempo.

### Lo que pierde el propietario

El propietario lleva muchos proyectos a la vez. Que todos tengan `develop`, `feature/NN` y `docs/decisiones/` le ahorra pensar en cuál está. Adaptarse rompe esa uniformidad.

Mitigación: el panel habla con palabras de papel, no de nombre: «Integración: main», «Decisiones: docs/adr». Lo que cambia entre proyectos se ve, y el flujo es el mismo.

### Dónde conviene que la SF imponga

- **La cola, sus estados y `cola.py`** como única vía de escritura. Es el corazón de la SF.
- **Una rama por tarea** y el número de la tarea en el commit. Sin ellos no hay subagentes en worktree, ni prueba en la rama, ni revertir una tarea.
- **No trabajar en la rama de publicación.** Si integración y publicación son la misma, la SF lo dice y avisa antes de cada cierre.
- **Registrar las decisiones**, aunque el sitio y la forma sean del proyecto (decisión 140).
- **`.sf/proyecto.json`**, como marca.

## Decidir | Lo que ha decidido el propietario | Decidir {#decidir}

Todo decidido el 02/11/2026. Cada pregunta, con lo elegido y su decisión.

| Pregunta | Lo decidido | Decisión |
| --- | --- | --- |
| Límite de la incorporación | No se renombra ni se mueve nada del proyecto: se mapea donde está o se añade lo mínimo. Reorganizar es una petición aparte. Excepción: el paso a `sf/` de los documentos de la SF. | «Incorporar un proyecto no mueve ni renombra nada» (201) |
| 1. Alcance | La SF fija el mecanismo (cola, una rama por tarea, número de la tarea en el commit, registro de decisiones) y se adapta en lo demás: remoto, documentos del proyecto, idioma y formato del commit. | «La SF fija el mecanismo y se adapta a las convenciones del proyecto» (202), corregida por la 205 y la 208 |
| 2. Huella | Como hoy: `.sf/` con `proyecto.json` versionado, y la cola, el estado y el historial en `.gitignore`. Los documentos de la SF, en `sf/` en la raíz, sin nivel `docs/`: `sf/propuestas.md`, `sf/informes/`, `sf/decisiones/`. Los proyectos ya incorporados, también la SF, se pasan a `sf/` al ponerlos al día, con el OK del propietario. | «Los documentos de la SF van en la carpeta sf/» (203) |
| 3. Ramas | No se adaptan: siempre `develop`, `feature/NN-nombre`, squash al cerrar y `main` con tag al publicar. Si el proyecto no tiene `develop` (o `main`), se propone crearla. | «El manejo del repositorio no se negocia: siempre develop» (205) |
| 4. Documentos y decisiones | Los documentos del proyecto, donde están (201). Las decisiones, siempre en `sf/decisiones/`, un archivo por decisión con su índice; las que ya tenga el proyecto se migran ahí con el OK. | 201 y «Las decisiones son material de la SF: siempre en sf/decisiones/» (208) |
| 5. Idioma y commits | Claude escribe en el idioma del proyecto y del desarrollador, y sigue su formato de commit. El número de la tarea va como «(N)» al final si el proyecto no tiene formato propio, o en el trailer `SF-Tarea: N` si lo tiene estricto. | «Claude escribe en el idioma del proyecto y del desarrollador» (206) y «El número de la tarea en el commit, según el formato del proyecto» (207) |
| 6. La incorporación | Operación sin tarea, fuera de la cola y del panel, guiada por menús en la línea de prompts: qué se crea, mueve o cambia, el OK y un commit en `develop`. Vale para incorporar, poner al día y migrar a `sf/`. | «Incorporar un proyecto es una operación sin tarea, guiada por menús» (209) |

De paso, «Los estados de las tareas se nombran con el lenguaje de la SF» (204): una tarea de Testing se cierra o se revierte, no se «da por probada».

### Lo que queda abierto

Nada que bloquee el reparto. Tres detalles, que conviene que decida la tarea que los aplica, con su recomendación:

- **Mientras un proyecto no se ha pasado a `sf/`.** El plugin lee `sf/propuestas.md` y `sf/decisiones/` y, si no existen, los de `docs/` como hasta ahora, con un aviso de atraso en el panel. Recomendado: aceptar las dos rutas hasta que todos los proyectos estén al día, igual que «(N)» y el trailer.
- **El mapa de los documentos del proyecto.** Desde «Fuera la sección Documentos del panel» (195), el panel ya no los enseña. El mapa (`config.documentos`) solo serviría a las skills. Recomendado: no crearlo hasta que una skill lo necesite (KISS); las skills buscan el documento al usarlo.
- **JKanban integra por PR.** Con la 205, al incorporarse tiene que pasar a `develop` y al squash de la SF. No es una decisión nueva, pero el propietario debe saberlo antes de la prueba en ese proyecto.

## Tareas | Cómo se reparte la aplicación | Tareas {#tareas}

En este orden. Las dos primeras pueden ir a la vez.

1. **«Configuración inicial: decidir el mínimo, los commits y la versión, y diseñar .sf/proyecto.json y las preguntas» (263).** Cierra el bloque `config` con lo decidido: `remoto`, `idioma`, `commits.formato` y `commits.tarea` (título o trailer), `metodologia` y `version`; sin ramas (205) ni decisiones (208). Diseña también qué detecta la incorporación y cómo lo pregunta en un menú. Su paso «Decidir con el propietario las seis preguntas del informe y registrarlas» queda hecho con esta tarea.
2. **Nueva: «Los documentos de la SF en sf/: rutas del plugin».** `cola.py` (la constante `PROPUESTAS`, sus commits en `develop` y la orden `decision`), `lectura.ts` y el panel, `indice_decisiones.py` (por defecto `sf/decisiones`, y la línea `merge=union` de `.gitattributes`), las plantillas y sus pruebas, con la lectura de las rutas antiguas mientras dure la migración. No depende de la configuración, porque `sf/` es fijo.
3. **«Implementar la configuración inicial» (193).** Lee el bloque `config` en `cola.py` y en el mod: el remoto en el cierre y en la publicación (ya tiene el paso), el número de la tarea según `commits.tarea` en el squash y en el encargo de los subagentes (207), y el idioma en los textos que escribe Claude (206). Después de la 263.
4. **«Poner un proyecto al día con la SF sin tarea: informar, pedir OK y aplicar» (288).** Ya tiene hecho el caso «actualizar» sin tarea. Conviene cerrarla así y no hacerla crecer.
5. **Nueva: «Incorporar sin tarea, con menús y sin mover nada».** Reescribe `sf:incorporar_proyecto_a_sf` en sus cuatro casos:
   - operación sin tarea ni panel, con menús (209), y la excepción en `sf:orquestacion`;
   - fuera la reorganización de `docs/` (201);
   - crear `develop` y `main` con el OK (205);
   - `sf/propuestas.md`, `sf/informes/` y `sf/decisiones/` en lugar de `docs/` (203, 208);
   - migrar a `sf/` al poner al día, incluidas las decisiones, el antiguo `docs/decisiones.md` y las de otra forma, como el archivo único de SmartColdBox (208);
   - detectar y guardar las convenciones de la 263.

   Después de la 288, la 263 y la nueva de rutas, para que la skill nombre lo que ya existe.
6. **Pasar la propia SF a `sf/`.** Es la operación de poner al día (209), hecha en una sesión de la SF cuando el plugin ya lea `sf/`: `docs/propuestas.md`, `docs/decisiones/` y los informes de `docs/referencias/reports/` pasan a `sf/`, con sus enlaces rehechos. Los enlaces del CLAUDE.md y de los documentos compartidos van en sus tareas «Actualizar…». Después, sprite_animation, en su propia sesión.
7. **«Primeros cinco minutos de un usuario nuevo con la SF» (289).** Prueba la incorporación nueva en los proyectos que la retratan:
   - JKanban: inglés, conventional commits, PR que pasa a `develop`;
   - SmartColdBox: solo `main`, decisiones en un archivo;
   - PoseTracker: sin `main` ni `docs/`;
   - OncoCore: `_docs/` sin tocar;
   - Sprites: vacío y sin git.

   Su atasco de idioma recoge los textos fijos del plugin en español (206). Al final, cuando todo lo anterior esté hecho.
8. **Documentos compartidos, cada uno en su tarea y en el principal:**
   - «Metodología y especificación: configuración inicial» (191): el acuerdo, como mecanismo fijo más convenciones (202, 205 a 208).
   - «Actualizar las reglas del método: metodología, plantilla y CLAUDE.md» (208): estructura documental con `sf/` y `.sf/`, ramas fijas (205), idioma (206), número de la tarea (207), incorporación sin tarea (209) y lenguaje de los estados (204). En el CLAUDE.md, los enlaces a `docs/decisiones/` y `docs/propuestas.md` tras el paso 6.
   - «Actualizar Cómo funciona la Software Factory» (219): mapa de piezas del proyecto (`sf/` y `.sf/`) y la incorporación como operación.
   - «Actualizar Cómo funciona el panel» (198): las propuestas desde `sf/propuestas.md`.
9. **El lenguaje de los estados (204),** si no tiene tarea: la orden `probada` de `cola.py`, los botones y avisos del panel y `sf:flujo_tareas`. No depende de lo anterior.
