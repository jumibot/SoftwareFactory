---
antetitulo: Software Factory · Informe de diseño · Noviembre 2026
lema: El mecanismo, fijo; // las convenciones, detectadas.
subtitulo: El diseño final de la configuración de un proyecto: qué es fijo, cada campo de .sf/proyecto.json con su valor por defecto, las preguntas de la incorporación y lo que debe implementar «Implementar la configuración inicial».
version: Versión 3.2 · 02/11/2026
estado: Diseño final · Tarea 263
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
tipo: Informe de diseño
pie: Diseño de la tarea «Configuración inicial: decidir el mínimo, los commits y la versión, y diseñar .sf/proyecto.json y las preguntas» (263), que cierra la de «Diseñar la configuración inicial» (190). Aplica las decisiones 138, 140, 171, 187, 199, 201 a 209, 213, 214 y 224 a 230, sobre el código del mod, cola.py y la skill de incorporación, y sobre PoseTracker, JKanban, SmartColdBox y sprite_animation (solo lectura).
---
# Configuración inicial

## Resumen | Todo decidido | Resumen {#resumen}

La SF fija el **mecanismo** y se adapta a las **convenciones** del proyecto («La SF fija el mecanismo y se adapta a las convenciones del proyecto», 202).

- **Fijo:** la cola, el modelo de ramas, un remoto en GitHub, los commits (siempre de Claude), la versión con tag y las decisiones en `sf/decisiones/`.
- **Se detecta y se confirma:** idioma, formato de commit, remoto, rama que hace de `main` y manifiesto con versión.
- **Se elige:** metodología y kanban.

Todo va en `.sf/proyecto.json`, en campos sueltos, al nivel de `proyecto` y `color`. Solo se agrupa lo afín cuando hay muchos campos, como `automatizaciones` («Todo proyecto.json es configuración: plana, y bloques solo para lo afín», 227). Lo que falta vale lo de hoy, así los proyectos ya incorporados no cambian hasta ponerlos al día.

Incorporar es una operación sin tarea, guiada por menús en la línea de prompts (209). Cambiar la configuración después tiene su propia skill y su orden de barra («La configuración se cambia pidiéndoselo a Claude, con menús», 228, corregida el mismo día), en la tarea «Skill y orden de barra para cambiar la configuración del proyecto» (299).

No hay mapa de documentos: si el proyecto sigue la estructura documental de la SF, sus documentos están donde la SF los busca; si no la sigue, no se mapean («Sin mapa de documentos: o se sigue la estructura de la SF, o no se mapea», 229). Por eso `.sf/proyecto.json` no lleva un bloque `documentos` y la incorporación no pregunta rutas.

## Mínimo | Qué es fijo, qué se detecta y qué se elige | Mínimo {#minimo}

### Fijo: el mecanismo, sin campo

- **Tareas:** la cola con `cola.py`, sus estados, los pasos, el panel y la orquestación con un subagente por tarea en curso.
- **Ramas:** `develop`, una rama `feature/NN-nombre` por tarea, squash al cerrar y publicación de `develop` a `main` («El manejo del repositorio no se negocia: siempre develop», 205). Sin `develop` no hay SF: si el desarrollador no quiere crearla, se le pide que lo reconfirme y se para («Sin develop no hay SF, y las decisiones mezcladas se sacan con enlace», 214).
- **Commits:** los hace siempre Claude, en la rama de la tarea, en el squash y al publicar, cada uno con el OK del propietario como hasta ahora («Los commits los lleva siempre Claude», 225). No hay modo de commits a mano. Si el desarrollador no lo acepta, se trata como negarse a `develop`.
- **Remoto en GitHub:** todo proyecto con la SF lo tiene. Al incorporar y al poner al día se comprueba; si falta, se ofrece crearlo con `gh`, y si el desarrollador no quiere, se le pide que lo reconfirme y no hay SF («Sin remoto en GitHub no hay SF: se valida al incorporar y, si falta, se crea», 230). Solo cuenta un remoto que apunte a `github.com`: uno en otro servicio no basta, y se ofrece crear el de GitHub a su lado.
- **Versión:** al publicar, siempre un tag `vX.Y.Z`, que es la fuente de la versión («La versión forma parte del manejo del repositorio», 226).
- **Documentos de la SF**, en `sf/`: `sf/decisiones/` (una por archivo, con su índice), `sf/propuestas.md` y `sf/informes/` (203, 208).
- **Reglas comunes**, que entrega el mod siempre (187).

### Se detecta y se confirma: las convenciones

| Convención | Decisión | Campo |
| --- | --- | --- |
| Idioma de lo que escribe Claude | 206 | `idioma` |
| Formato del commit y marca del número de tarea | 206, 207 | `commits` |
| Nombre del remoto de GitHub al que se hace push | 202, 205, 230 | `remoto` |
| Rama que hace de `main` | 213 | `rama_main` |
| Manifiesto con versión | 226 | `manifiesto` |

### Se elige

| Elección | Decisión | Campo |
| --- | --- | --- |
| Metodología | 138 | `metodologia` |
| Kanban | 224 | `kanban` |

Las automatizaciones (171) no se preguntan: están encendidas salvo `false` y se cambian con la skill de configuración (299).

## Esquema | .sf/proyecto.json, campo a campo | Esquema {#esquema}

### Los campos

| Campo | Tipo y valores | Si falta | Cómo se fija | Lo leen |
| --- | --- | --- | --- | --- |
| `sf` | versión `X.Y.Z` | — (obligatorio) | Detectado: el `plugin.json` del plugin instalado, al incorporar y al poner al día | Panel (aviso de atraso) |
| `proyecto` | texto | — (obligatorio) | Elegido; se propone el del README o la carpeta | Panel, sesión, `cola.py` |
| `descripcion` | texto, ≤ 120 caracteres | — (obligatorio) | Elegido; se propone del README | Panel, Commander, kanban |
| `color` | `red`, `blue`, `green`, `yellow`, `orange`, `pink`, `cyan` | — (obligatorio) | Elegido; se propone uno que no usen los proyectos vecinos | Sesión (`/color`) |
| `metodologia` | `true` \| `false` | `true` | Elegido | Mod (reglas del método, fase), skills |
| `kanban` | `{ "proveedor": "jkanban", "proyecto": "…" }`, o cadena (forma antigua: proyecto de JKanban) | ninguno | Elegido; por defecto, ninguno | Mod, skills |
| `idioma` | código corto (`es`, `en`, `ca`…) | `es` | Detectado y confirmado | Mod (línea de convenciones), `cola.py` (encargo) |
| `commits` | `libre` \| `conventional` \| `propio` | `libre` | Detectado y confirmado | `cola.py` (squash, encargo), mod |
| `remoto` | nombre de un remoto que apunta a GitHub | `origin` | Detectado; se pregunta solo si hay varios de GitHub; si no hay ninguno, se crea (230) | `cola.py` (cierre), RELEASE, panel (push pendiente) |
| `rama_main` | nombre de rama | `main` | Detectado; se pregunta si hay `master` u otra principal (213) | RELEASE, `cola.py` |
| `manifiesto` | ruta, lista de rutas, o `null` | ninguno (solo tag) | Detectado; se pregunta solo si hay varios | RELEASE |
| `automatizaciones` | bloque de interruptores `true` \| `false` | todos `true` | No se pregunta | Mod, `cola.py` |

### Reglas

- **La marca del número sale de `commits`** y no se guarda aparte: con `libre`, «(N)» al final del título; con `conventional` o `propio`, el trailer `SF-Tarea: N` al pie (207). Guardarla aparte permitiría combinaciones sin uso.
- **`propio`** es un formato estricto sin nombre: Claude imita los títulos de los últimos commits del proyecto.
- **`kanban` es un bloque** porque proveedor y proyecto solo valen juntos, y así añadir GitHub Projects es un valor más de `proveedor` (224). La cadena antigua (`"kanban": "JKanban"`) se lee como `{ "proveedor": "jkanban", "proyecto": "JKanban" }`; al poner al día se reescribe.
- **`manifiesto`:** formatos soportados, `.json` (clave `version`: `package.json`, `plugin.json`) y `pyproject.toml` (`version = "…"`). Otros (`pom.xml`, `Cargo.toml`, Gradle), cuando un proyecto los traiga. Con una lista, se suben todos en el mismo commit. Un archivo con la versión en el código, como `backend/main.py` en JKanban, no es manifiesto: JKanban se queda con el tag.
- **La propia SF** no tiene `.sf/proyecto.json` en su repositorio. Sus valores salen de la marca de la SF: manifiesto `plugins/sf/.claude-plugin/plugin.json`, lo demás por defecto.
- **`remoto` no admite `null`** (230): siempre hay push en el cierre y en RELEASE. Si el remoto configurado no existe o no apunta a GitHub, el panel avisa y la puesta al día lo arregla.
- **Valores desconocidos:** el mod y `cola.py` los tratan como si faltaran y el panel avisa, sin bloquear (171).
- **La incorporación escribe siempre lo confirmado**, aunque coincida con el valor por defecto, salvo `automatizaciones`, que solo aparece si se apaga algo.

### Ejemplos

PoseTracker: sin metodología, con su remoto, sin `main` hasta crearla.

```json
{
  "sf": "1.5.0",
  "proyecto": "PoseTracker",
  "descripcion": "Seguimiento de manos y cuerpo con cámara para un gimnasio digital",
  "color": "green",
  "metodologia": false,
  "idioma": "es",
  "commits": "libre",
  "remoto": "PoseTracker",
  "rama_main": "main",
  "manifiesto": null
}
```

JKanban: en inglés, conventional commits, con kanban.

```json
{
  "sf": "1.5.0",
  "proyecto": "JKanban",
  "descripcion": "Kanban propio con API y MCP",
  "color": "blue",
  "metodologia": true,
  "kanban": { "proveedor": "jkanban", "proyecto": "JKanban" },
  "idioma": "en",
  "commits": "conventional",
  "remoto": "origin",
  "rama_main": "main",
  "manifiesto": null
}
```

Un proyecto web con `master` como rama principal y dos manifiestos:

```json
{
  "sf": "1.5.0",
  "proyecto": "LecturaFàcil",
  "descripcion": "Adapta textos a lectura fácil con revisión humana",
  "color": "pink",
  "metodologia": true,
  "idioma": "ca",
  "commits": "libre",
  "remoto": "origin",
  "rama_main": "master",
  "manifiesto": ["frontend/package.json", "backend/pyproject.toml"],
  "automatizaciones": { "avisos_subagentes": false }
}
```

## Preguntas | La incorporación, en menús de hasta cuatro | Preguntas {#preguntas}

Se pregunta con la herramienta de menús, la opción recomendada primero y con lo que la delata. Lo que se detecta sin duda no se pregunta: se enseña en el resumen final. Cada menú lleva solo las preguntas que hacen falta; si se quedan en cero, no se muestra.

### Menú 0: caso

«Nuevo», «Existente» o «Poner al día», el detectado primero, o «Solo diagnosticar». Se salta si el propietario ya lo ha dicho.

### Menú 1: identidad

| # | Pregunta | Opciones | Por defecto | Se salta si |
| --- | --- | --- | --- | --- |
| 1 | ¿Nombre del proyecto? | El propuesto / otro | El del README o la carpeta | Ya está en `proyecto.json` |
| 2 | ¿Descripción? | La propuesta / otra | Primera frase del README, ≤ 120 caracteres | Ya está |
| 3 | ¿Color de las sesiones? | Dos o tres libres / otro | Uno que no usen los vecinos | Ya está |
| 4 | ¿Seguir la metodología: fases y documentos del método? | «Sí» / «No: solo tareas, repositorio y decisiones» | Nuevo: «Sí». Existente: «No», salvo que tenga visión o especificación | Ya está (poner al día) |

### Menú 2: repositorio

| # | Pregunta | Opciones | Por defecto | Se salta si |
| --- | --- | --- | --- | --- |
| 1 | ¿`master` hace de `main`? | «`master` hace de `main`» / «Crear `main` desde `master`» | La primera (213) | Hay `main`, o no hay rama principal |
| 2 | ¿Crear `develop` desde `<rama_main>`? | «Crear `develop`» / «No crear» | «Crear» | Ya existe `develop` |
| 3 | Remoto en GitHub. Con varios: ¿a cuál se hace push? Sin ninguno: ¿crear `<cuenta>/<proyecto>` en GitHub? | Varios: cada remoto de GitHub. Ninguno: «Crear privado» / «Crear público» / «No crear» | Varios: el que sigue `develop` o `rama_main`. Ninguno: «Crear privado» | Hay uno de GitHub (se usa) |
| 4 | Los commits los hace Claude, con tu OK en cada cierre y publicación | «De acuerdo» / «No usar la SF aquí» | «De acuerdo» | El `CLAUDE.md` no dice que los lleve el desarrollador; entonces solo se cuenta en el resumen |

Sin repositorio git, antes de este menú se propone crearlo (`git init -b main`). Para crear el remoto hace falta `gh` instalado y con la sesión iniciada (`gh auth status`); si no, se dice cómo (`gh auth login`) y se espera: sin remoto no se sigue. Se crea con `gh repo create <cuenta>/<proyecto> --private --source . --remote origin` (o `github` si `origin` ya existe y apunta a otro servicio), y las ramas se suben en el commit final.

**Reconfirmar.** Con «No crear» `develop`, «No crear» el remoto o «No usar la SF aquí», un menú propio explica por qué la SF no funciona sin ello y ofrece «Crear `develop`», «Crear el remoto» o «De acuerdo», frente a «No usar la SF en este proyecto». Con la segunda, se para sin cambiar nada (214, 225, 230).

### Menú 3: convenciones

| # | Pregunta | Opciones | Por defecto | Se salta si |
| --- | --- | --- | --- | --- |
| 1 | ¿En qué idioma escribe Claude commits, tareas y documentos? | El detectado / español / inglés | El del README, el `CLAUDE.md` y los últimos commits | Proyecto nuevo: el de la conversación |
| 2 | ¿Cómo son los commits? | «Conventional, con `SF-Tarea: N` al pie» / «Como los de ahora (`<ejemplo>`), con `SF-Tarea: N`» / «Libres, con `(N)` al final» | Conventional si lo siguen la mayoría de los últimos 50 títulos; propio si comparten otra forma fija; si no, libres | Proyecto nuevo: libres |
| 3 | ¿Qué manifiestos suben de versión al publicar? | Cada uno (selección múltiple) / «Ninguno: solo el tag» | Todos los detectados | Hay uno (se usa) o ninguno |
| 4 | ¿Kanban? | «Ninguno» / «JKanban: `<proyecto>`» | «Ninguno» (224) | — |

### Resumen y OK

Lo que se va a crear (`.sf/`, `sf/`, `develop` y `main` si faltan, el remoto en GitHub si falta, las líneas del `.gitignore`) y lo que se va a mover (los documentos de la SF a `sf/`, 203 y 208), con la configuración confirmada y lo detectado sin preguntar. Con el OK se aplica en `develop`, con el commit «Incorporado a la SF X.Y.Z», en el idioma y el formato del proyecto, y se suben `develop` y `rama_main` al remoto.

### Poner al día

Se comprueba el remoto en GitHub como al incorporar (230). Se escriben los campos que falten con lo detectado, en un solo menú con lo que tenga duda. La cadena antigua de `kanban` pasa a bloque. El menú final ofrece además cambiar la configuración, con la skill de la 299.

## Implementar | Lo que hace «Implementar la configuración inicial» (193) | Implementar {#implementar}

### Lectura

1. Una sola función de lectura en `cola.py` y otra en el mod, con los valores por defecto de la tabla. La cadena antigua de `kanban` se lee como bloque, y un valor desconocido se trata como si faltara, con aviso en el panel. En la SF, los valores salen de su marca.
2. Arreglar `nombre_proyecto` en `cola.py`: lee el campo `nombre`, pero el campo es `proyecto`, así que siempre cae al nombre de la carpeta.

### Repositorio

3. **`remoto`:** el push del squash en `cola.py` (hoy fijo a `origin`), el de RELEASE en `cola.ts` y la comprobación del push pendiente en `lectura.ts` (`origin/develop`). Sin valor `null`: un remoto que falta o no apunta a GitHub se avisa en el panel (230).
4. **`rama_main`:** RELEASE (existencia de la rama, `merge-base`, `fetch . develop:<rama_main>`, tag, push) y lo que en `cola.py` y en el mod nombra `main`.
5. **Versión (226):** la versión actual sale siempre del último tag `vX.Y.Z`, también en la SF. RELEASE sube la `version` de cada `manifiesto` (`.json` y `pyproject.toml`) en un commit `vX.Y.Z` (en la SF, `sf X.Y.Z`) antes del tag. Si un manifiesto no tiene versión o no coincide con el tag, avisa sin bloquear y la escribe.
6. **`commits`:** el mensaje del squash en `cola.py` pone «(N)» o el trailer `SF-Tarea: N`, según el formato. Lo que busca los commits de una tarea (el panel, en `lectura.ts`; `cola.py`) acepta las dos formas. Revertir no cambia, porque va por hash.
7. **La coautoría** (`COAUTOR`) sigue en todos los formatos, como trailer.

### Reglas y panel

8. **`metodologia`:** el mod entrega las reglas del método solo con `true`, así que hay que partir `templates/claude-sf.md` en comunes y del método (el paso que ya tiene la 193). Con `false`, el panel no pinta la fase ni pide `estado.json`.
9. **Línea de convenciones** en lo que entrega el mod: idioma, formato de commit y marca, remoto y `rama_main` si no es `main`. `cola.py encargo` la añade al encargo del subagente.
10. **`kanban` opcional:** el panel y el diagnóstico no fallan ni avisan sin él.

### Incorporación

11. **`sf:incorporar_proyecto_a_sf`:** los menús 1 a 3 con su detección, la comprobación del remoto en GitHub y su creación con `gh` (230), la reconfirmación de commits (225) y del remoto junto a la de `develop`, la escritura de los campos y la comprobación final (`kanban` deja de ser obligatorio; los campos, válidos). Así se cierran sus pasos 2 y 8, que hoy dicen «pendiente del diseño de la configuración inicial». Además, quitar lo que diga de mapear documentos: no se preguntan rutas (229).
12. **Poner al día:** comprobar el remoto en GitHub y crearlo si falta (230), escribir los campos que falten y pasar `kanban` a bloque.

### Pruebas y documentos

13. **Pruebas de `cola.py`:** remoto con otro nombre; trailer y «(N)»; `rama_main` `master`; manifiesto `.json`, `pyproject.toml` y lista; `kanban` en cadena. **Pruebas del panel:** metodología apagada, aviso de remoto que falta o no es de GitHub, push pendiente con otro remoto, RELEASE con `rama_main`.
14. **Documentos compartidos,** cada uno en su tarea «Actualizar <documento>»: «Cómo funciona la Software Factory» (identidad y configuración, RELEASE) y la metodología (sección 6, `proyecto.json`).

### Fuera de la 193

- La skill y la orden de barra para cambiar la configuración: «Skill y orden de barra para cambiar la configuración del proyecto» (299).
- El kanban de GitHub (224): tarea aparte, más adelante.
- Más formatos de manifiesto, y pasar «Sin publicar» del CHANGELOG a la versión: cuando un proyecto lo pida.
