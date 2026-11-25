---
antetitulo: Software Factory · Informe de diseño · Noviembre 2026
lema: El mecanismo, fijo; // las convenciones, en config.
subtitulo: Qué fija y qué elige la configuración inicial de un proyecto, quién hace los commits, dónde guarda su versión, cómo se escribe en .sf/proyecto.json y qué se pregunta al incorporar y al cambiarla.
version: Versión 2.1 · 02/11/2026
estado: Propuesta · Tarea 263
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
tipo: Informe de diseño
pie: Propuesta de la tarea «Configuración inicial: decidir el mínimo, los commits y la versión, y diseñar .sf/proyecto.json y las preguntas» (263), que revisa la de «Diseñar la configuración inicial» (190). Sale de las decisiones 138, 140, 171, 187, 194, 196, 199 y 201 a 209, del código del mod y de cola.py, de la skill de incorporación, del informe «Incorporar sin cambiar el proyecto» (222) y de los proyectos PoseTracker, JKanban, SmartColdBox y sprite_animation (solo lectura). Espera la decisión del propietario en lo que queda abierto.
---
# Configuración inicial

## Resumen | Lo decidido y lo que queda | Resumen {#resumen}

Las decisiones de la 222 (201 a 209) han cerrado buena parte del diseño. La SF fija el **mecanismo**: la cola, el modelo de ramas (`develop`, `feature/NN-nombre`, squash, `main` con tag), el número de la tarea en el commit y las decisiones en `sf/decisiones/` con su formato. Se **adapta** a las convenciones del proyecto: remoto, documentos, idioma y formato del commit («La SF fija el mecanismo y se adapta a las convenciones del proyecto», 202, corregida por «El manejo del repositorio no se negocia: siempre develop», 205, y «Las decisiones son material de la SF: siempre en sf/decisiones/», 208).

Esas convenciones, y lo que se elige, van en el bloque `config` de `.sf/proyecto.json`, al lado del bloque `automatizaciones` que ya existe. Lo que falta vale lo de hoy, para que los proyectos ya incorporados no cambien hasta ponerlos al día.

Incorporar, poner al día y cambiar la configuración son una operación sin tarea, guiada por menús en la línea de prompts («Incorporar un proyecto es una operación sin tarea, guiada por menús», 209).

Quedan abiertas cinco preguntas: el kanban, quién hace los commits, dónde se guarda la versión, si `automatizaciones` va dentro de `config` y cómo se cambia la configuración más tarde.

### Qué queda resuelto por las decisiones 201 a 209

| Lo que proponía la versión anterior | Ahora |
| --- | --- |
| Remoto configurable | Resuelto: es una convención adaptable (202, 205). |
| Huecos `ramas` y `decisiones` en `config` | Fuera: son mecanismo fijo (205, 208). |
| Huecos `idioma` y `commits.formato` | Dentro: Claude escribe en el idioma del proyecto y sigue su formato de commit (206). |
| Número de tarea en el commit | Resuelto: «(N)» al final del título sin formato propio; trailer `SF-Tarea: N` con formato estricto (207). Va en `config.commits.marca`. |
| Proponer `develop` en el resumen | Resuelto: se propone siempre crear `develop`, y `main` si falta (205). |
| Incorporación guiada por menús, sin tarea | Resuelto (209). |
| `docs/propuestas.md` y `docs/decisiones/` | Pasan a `sf/propuestas.md`, `sf/informes/` y `sf/decisiones/` (203, 208). |
| Reorganizar `docs/` | Fuera: la incorporación no mueve ni renombra nada (201), salvo los documentos de la SF a `sf/`. |

## Mínimo y elegible | Qué es fijo, qué se elige y qué se adapta | Mínimo {#minimo}

### Lo fijo (mecanismo)

- **Identidad:** `proyecto`, `descripcion`, `color` y `sf`.
- **Tareas:** la cola con `cola.py`, sus estados y su lenguaje («Los estados de las tareas se nombran con el lenguaje de la SF», 204), los pasos, el panel y la orquestación con un subagente por tarea en curso.
- **Repositorio:** `develop`, una rama `feature/NN-nombre` por tarea, squash al cerrar, publicación de `develop` a `main` con RELEASE y tag `vX.Y.Z` (205). El número de la tarea en cada commit (207).
- **Documentos de la SF**, en `sf/`: `sf/decisiones/`, una por archivo con su índice (140, 208); `sf/propuestas.md`; `sf/informes/` (203).
- **Reglas comunes**, que entrega el mod siempre (187): un proyecto por sesión, comandos antes que inferencia, lo que pinta la SF no es del proyecto (167).

### Lo que se adapta (convenciones, detectadas y confirmadas)

- **Remoto:** a cuál se hace push, o a ninguno. Hoy `cola.py` (squash, hacia la línea 435) y RELEASE (`cola.ts`, hacia la 401) lo hacen fijo a `origin`: en PoseTracker (remoto `PoseTracker`) y en sprite_animation (sin remoto) falla en cada cierre.
- **Idioma:** el de los commits, tareas, pasos, informes y documentos que escribe Claude (206).
- **Formato del commit** y **marca del número** (206, 207).
- **Documentos del proyecto:** dónde tiene su visión, su especificación o sus guías, para que el panel los encuentre sin moverlos (201, 202). El mapa lo diseña la 222; aquí solo se le reserva sitio.

### Lo que se elige

- **Metodología:** fases y `estado.json`, los documentos del método y las guías (138). Con ella, el panel enseña la fase y el mod entrega también las reglas del método. Sin ella, ni `estado.json` ni fase.
- **Kanban:** el proyecto en JKanban, o ninguno. Abierta (pregunta 1).
- **Quién hace los commits** y **dónde se guarda la versión**: cómo se hace lo fijo. Abiertas (preguntas 2 y 3).

### Lo que no se pregunta

- **Automatizaciones** («Las automatizaciones del plugin, configurables y avisando antes que bloquear», 171): `orquestacion`, `avisos_subagentes`, `encargo_subagente` y `dependencias_al_actualizar`, encendidas salvo `false`. Son ayudas del plugin, no forma de trabajar del proyecto.

### Kanban: opciones

**A. Elegible, por defecto ninguno.** Pros: no obliga a un kanban que hoy no está conectado; PoseTracker no lo necesita. Contras: los proyectos dejan de ser uniformes en eso.

**B. Fijo.** Pros: todos los proyectos en JKanban. Contras: hoy la incorporación tendría que dejarlo siempre como pendiente, sin poder crearlo.

**Recomendación: la A.** Volver a mirarlo cuando JKanban esté conectado.

## Commits | Quién los hace cuando el propietario los hace a mano | Commits {#commits}

El caso es PoseTracker: su `CLAUDE.md` dice que el propietario «prueba en vivo […] y lleva commits/pulls él mismo». Sus commits los firma la misma identidad git que los de Claude (`jumibot`).

Hoy los commits tienen tres orígenes:

- **De trabajo,** en la rama de la tarea: los hace el subagente en su rama auxiliar y el principal los trae (decisiones 149 y 151).
- **El squash a `develop`:** la C del panel, o `cola.py cerrar` con el OK del propietario de palabra.
- **La publicación:** RELEASE, un botón.

Los dos últimos ya los decide el propietario; solo los de trabajo los decide Claude.

**A. Siempre Claude.** Pros: sin código nuevo. Contras: choca con una regla escrita del proyecto, que manda mientras no se decide lo contrario.

**B. Integra el propietario** (`propietario-integra`). Claude hace los commits de trabajo en la rama de la tarea; a `develop` y a `main` solo llega lo que el propietario lanza: la C, RELEASE o una orden suya explícita en ese mensaje. `cola.py cerrar` lo rechaza sin la marca de que lo pide el propietario, como ya hace el panel. Pros: conserva ramas, squash, subagentes y reversión, que la 205 hace innegociables. Contras: solo cambia una regla, puede que no sea lo que él entiende por «llevar los commits».

**C. Todo a mano** (`propietario`). Claude no hace ningún commit ni push y deja los cambios en el árbol, con el mensaje propuesto. Pros: control total. Contras: sin commits los subagentes en worktree no pueden devolver el trabajo, y sin ramas por tarea ni squash no se cumple el manejo del repositorio que la 205 declara no negociable. Pide otro flujo en `cola.py` y en las skills.

**Recomendación: la B.** La C choca ahora con la 205; solo tendría sentido si el propietario decide que «llevar los commits» en PoseTracker es escribir él cada uno, y entonces sería una excepción a la 205. En los tres casos el autor es la identidad git de la máquina, con la línea `Co-Authored-By` de Claude en los commits de Claude.

## Versión | Dónde la guarda un proyecto al publicar | Versión {#version}

Hoy RELEASE trata dos casos: en la SF sube `version` en `plugins/sf/.claude-plugin/plugin.json`, con un commit `sf X.Y.Z`; en los demás proyectos solo crea el tag, y la versión actual es el último tag `vX.Y.Z`. La escritura ya es un reemplazo de texto sobre `"version": "…"`, que conserva el resto del archivo.

Casos reales: JKanban tiene la versión en `backend/main.py` (`FastAPI(..., version="1.0.0")`) y en `CHANGELOG.md`, sin manifiesto; sprite_animation y PoseTracker, en ningún sitio; SmartColdBox, solo un tag (`v4.0-rc1`, que no es `vX.Y.Z`).

**A. Solo el tag.** Pros: nada que escribir ni commit extra; vale para cualquier stack. Contras: la aplicación no puede enseñar su versión sin git, y una copia descargada no la lleva.

**B. El tag y un archivo del proyecto, configurado, con su patrón.** `config.version` dice el archivo y, si no es un formato conocido, el patrón que encuentra el valor. RELEASE reescribe solo el valor y hace el commit `vX.Y.Z` antes del tag. Formatos conocidos, con patrón por defecto: `.json` (`"version": "…"`: `package.json`, `plugin.json`) y `pyproject.toml` (`version = "…"`). Para el resto (`main.py`, `pom.xml`, `.properties`, Gradle), una expresión regular con un grupo para el valor. Pros: la versión está donde la buscan las herramientas y la propia aplicación; un solo mecanismo (el que ya usa RELEASE); la SF deja de ser un caso aparte. Respeta la 201: usa el archivo que el proyecto ya tiene. Contras: un patrón mal escrito publicaría sin cambiar el archivo, así que RELEASE comprueba antes que encuentra un solo valor y que es la versión actual.

**C. Un archivo `VERSION`** en la raíz. Pros: trivial y universal. Contras: añade un archivo al proyecto y duplica la versión si ya tiene manifiesto.

**D. En `.sf/proyecto.json`.** Pros: un solo sitio para el panel. Contras: la aplicación no lee `.sf/`, y se confunde con `sf`, la versión de la SF.

**Recomendación: la B si el proyecto tiene un archivo con versión; si no, la A.** La incorporación detecta el archivo y lo propone. Varios archivos (JKanban querría `main.py` y `CHANGELOG.md`) y pasar «Sin publicar» del CHANGELOG a la versión quedan como propuesta aparte, para cuando un proyecto lo pida.

## Formato | La configuración en .sf/proyecto.json | Formato {#formato}

Que haya un bloque `config` lo da por hecho la 202. Queda si `automatizaciones` va dentro o al lado.

**A. `config` al lado de `automatizaciones`.** Pros: separa tres cosas que cambian por motivos distintos: la identidad (casi nunca), la configuración (se pregunta al incorporar) y los interruptores del plugin (no se preguntan). El bloque `automatizaciones` ya lo leen cuatro sitios del código y no hay que migrarlo. Contras: dos bloques de ajustes.

**B. Todo en `config`, con `automatizaciones` dentro.** Pros: un solo bloque. Contras: hay que mover el código que ya lee `automatizaciones` y aceptar las dos formas un tiempo; mezcla lo que se pregunta con lo que no.

**Recomendación: la A.** `kanban` se queda en la raíz, con la identidad, y pasa a ser opcional.

### Esquema comentado

Comentarios al estilo JSONC solo para leerlo; el archivo real es JSON sin comentarios.

```jsonc
{
  // Identidad (fija). Casi nunca cambia.
  "sf": "1.4.2",                 // versión de la SF con la que se incorporó o se puso al día
  "proyecto": "JKanban",         // nombre tal como se escribe
  "descripcion": "Kanban propio con API y MCP",  // ≤ 120 caracteres
  "color": "blue",               // red, blue, green, yellow, orange, pink, cyan (purple es de la SF)
  "kanban": "JKanban",           // opcional: su proyecto en JKanban; sin él, no hay kanban

  // Configuración: se elige o se detecta y confirma al incorporar. Lo que falta, como hoy.
  "config": {
    "metodologia": true,         // true | false. Falta: true
    "idioma": "en",              // BCP 47 corto (es, en, ca…): commits, tareas, pasos, informes y documentos. Falta: "es"
    "commits": {
      "quien": "claude",         // "claude" | "propietario-integra" (abierta, pregunta 2). Falta: "claude"
      "formato": "conventional", // "libre" | "conventional": cómo escribe Claude el título. Falta: "libre"
      "marca": "trailer"         // "titulo": «(N)» al final | "trailer": «SF-Tarea: N» al pie (207).
                                 // Falta: "titulo" con formato libre, "trailer" con otro
    },
    "version": { "archivo": "backend/main.py", "patron": "version=\"(\\d+\\.\\d+\\.\\d+)\"" },
                                 // null (solo tag) | "ruta" (.json, pyproject.toml) | { archivo, patron } (abierta, pregunta 3)
                                 // Falta: solo el tag; en la SF, plugins/sf/.claude-plugin/plugin.json
    "remoto": "origin",          // nombre del remoto | null (sin push). Falta: "origin"
    "documentos": { }            // mapa de los documentos del proyecto (visión, especificación, guías…): lo diseña la 222
  },

  // Interruptores del plugin (decisión 171). No se preguntan; encendidos salvo false.
  "automatizaciones": {
    "orquestacion": true,
    "avisos_subagentes": true,
    "encargo_subagente": true,
    "dependencias_al_actualizar": true
  }
}
```

No hay campos de ramas ni de decisiones: son mecanismo fijo (205, 208). Tampoco de rutas de `sf/`: son fijas (203).

### Reglas del esquema

- **Lo que falta vale lo de hoy**, campo a campo; un `config` ausente es un proyecto como los de ahora.
- **`commits` admite una cadena** (`"commits": "claude"`), equivalente a `{ "quien": "claude" }` con formato y marca por defecto.
- **`marca` se guarda aparte de `formato`**, aunque por defecto se deduce de él: un proyecto con formato libre puede preferir el trailer, y lo que lee commits para encontrar los de una tarea acepta las dos formas (207).
- **`idioma` es del proyecto**, versionado, y vale para lo que queda en el repositorio y en la cola. La conversación sigue al desarrollador, sin campo: Claude ya contesta en el idioma en que le hablan (206).
- **`version` como cadena** solo para formatos conocidos; con otra extensión, objeto con `patron`.
- **`remoto: null`**: no hay push en el cierre ni en RELEASE, y el panel no avisa de «falta el push».
- **Valores desconocidos:** el mod y `cola.py` los tratan como si faltaran y el panel avisa, sin bloquear (171).
- **La incorporación escribe siempre lo confirmado**, aunque coincida con el valor por defecto, para que se vea qué se decidió.

### Ejemplos

PoseTracker, sin metodología y con el remoto propio:

```json
{
  "sf": "1.4.2",
  "proyecto": "PoseTracker",
  "descripcion": "Seguimiento de manos y cuerpo con cámara para un gimnasio digital",
  "color": "green",
  "config": {
    "metodologia": false,
    "idioma": "es",
    "commits": { "quien": "propietario-integra", "formato": "libre", "marca": "titulo" },
    "version": null,
    "remoto": "PoseTracker"
  }
}
```

sprite_animation, sin remoto:

```json
{
  "sf": "1.4.2",
  "proyecto": "SpriteAnimation",
  "descripcion": "Demostración de cómo usar sprites para crear animaciones en Java",
  "color": "orange",
  "config": { "metodologia": true, "idioma": "es", "commits": "claude", "version": null, "remoto": null }
}
```

### Quién lo lee

- **El mod:** enseña solo lo configurado (sin fase si no hay metodología); entrega las reglas comunes siempre y las del método solo con `metodologia: true`; añade a las reglas entregadas una línea con las convenciones («escribe en inglés; commits conventional con `SF-Tarea: N` al pie»); usa el remoto y la versión en RELEASE.
- **`cola.py`:** el remoto del push en el cierre; el idioma, el formato y la marca en el mensaje del squash y en el encargo del subagente (207); con `propietario-integra`, rechaza `cerrar` sin la marca del propietario.
- **La skill de incorporación:** lo detecta, lo pregunta, lo escribe y lo comprueba.

Una sola función de lectura en cada lado (mod y `cola.py`) con los valores por defecto. Es trabajo de «Implementar la configuración inicial» (193).

> [!aviso]
> De paso: `nombre_proyecto` en `cola.py` (hacia la línea 1268) lee el campo `nombre` de `.sf/proyecto.json`, pero el campo es `proyecto`. Siempre cae al nombre de la carpeta. Conviene anotarlo como bug.

## Preguntas | El guion de la incorporación | Preguntas {#preguntas}

Es una operación sin tarea, en la línea de prompts (209). Se pregunta con la herramienta de menús (hasta cuatro preguntas por llamada, de dos a cuatro opciones cada una), la opción recomendada primero y con lo que la delata. Lo que se detecta sin duda no se pregunta: se enseña en el resumen final.

### Incorporar (casos nuevo y existente)

1. **Caso:** el detectado, recomendado, o «Solo diagnosticar». Se salta si el propietario ya lo ha dicho.
2. **Identidad**, una pregunta con lo que falte: nombre, descripción y color, con valores sacados del proyecto.
3. **Elección**, una llamada:

| # | Pregunta | Opciones | Por defecto | Se salta si |
| --- | --- | --- | --- | --- |
| 1 | ¿Seguir la metodología: fases y documentos del método? | «Sí» / «No: solo tareas, repo y decisiones» | Nuevo: «Sí». Existente: «No», salvo que ya tenga visión o especificación | — |
| 2 | ¿Quién hace los commits? | «Claude» / «Claude en la rama; el propietario cierra y publica» | «Claude»; si el `CLAUDE.md` dice que los lleva el propietario, la segunda, citando la línea | — |
| 3 | ¿Dónde se guarda la versión al publicar? | «En `<archivo>` y en el tag» / «Solo en el tag» | La primera si se detecta un archivo con versión | No se detecta ninguno: solo el tag |
| 4 | ¿Proyecto en JKanban? | «Ninguno» / «<nombre del proyecto>» | «Ninguno» mientras JKanban no esté conectado | — |

4. **Convenciones**, otra llamada, con lo detectado:

| # | Pregunta | Opciones | Por defecto | Se salta si |
| --- | --- | --- | --- | --- |
| 1 | ¿En qué idioma escribe Claude commits, tareas y documentos? | El detectado / español / inglés | El del README, el `CLAUDE.md` y los últimos commits | Todo coincide con el idioma de la conversación |
| 2 | ¿Cómo son los commits? | «Como hasta ahora: `<ejemplo>`, con `SF-Tarea: N` al pie» / «Libres, con `(N)` al final» | Conventional si lo siguen la mayoría de los últimos 50 títulos; si no, libres | Proyecto nuevo: libres con `(N)` |
| 3 | ¿A qué remoto se hace push? | Cada remoto / «Ninguno» | El que sigue `develop` o `main` | Hay uno solo (se usa); ninguno (`null`, y el resumen avisa) |
| 4 | Documentos del proyecto | Lo que diseñe la 222 para el mapa | — | — |

5. **Resumen y OK**: lo que se va a crear (`.sf/`, `sf/`, `develop` y `main` si faltan, las líneas del `.gitignore`) y lo que se va a mover (en «poner al día», los documentos de la SF a `sf/`, 203 y 208), con la configuración elegida y lo detectado sin preguntar. Con el OK se aplica en `develop` con el commit «Incorporado a la SF X.Y.Z», en el idioma y el formato elegidos.

### Cambiar la configuración más tarde

Que sea una operación sin tarea ya lo dice la 209. Queda cómo se pide.

**A. Un caso «Configurar» en `sf:incorporar_proyecto_a_sf`.** Enseña la configuración actual y repite los pasos 3 y 4 con lo actual como opción por defecto; dice qué va a cambiar, pide el OK y lo aplica en `develop` con su commit. Activar la metodología crea `estado.json` con la fase real; quitarla lo borra y deja los documentos. También en el menú de «poner al día» («Poner al día y revisar la configuración»). Pros: un solo sitio que sabe incorporar. Contras: pasa por Claude también lo que es un simple valor.

**B. A más una orden del CLI** (`cola.py config remoto PoseTracker`) para lo que es solo un valor. Pros: comandos antes que inferencia. Contras: dos caminos; `cola.py` pasa a escribir un archivo versionado que no es la cola.

**C. Editar `proyecto.json` a mano.** Pros: nada nuevo. Contras: activar la metodología pide trabajo que a mano no se hace.

**Recomendación: la A ahora**, y la B si cambiar valores resulta frecuente.

## Decidir | Lo que decide el propietario | Decidir {#decidir}

1. **Kanban.** A, elegible y por defecto ninguno mientras JKanban no esté conectado (recomendada); B, fijo en todos los proyectos.
2. **Commits, cuando el propietario los lleva.** A, siempre Claude; B, Claude en la rama y el propietario cierra y publica, `propietario-integra` (recomendada); C, el propietario todos, como excepción a la 205. Y para PoseTracker: ¿qué busca, controlar lo que entra o escribirlo él?
3. **Versión.** A, solo el tag; B, el tag y un archivo configurado con su patrón, con la SF como un caso más (recomendada); C, un archivo `VERSION`; D, en `.sf/proyecto.json`.
4. **Automatizaciones.** A, `config` al lado de `automatizaciones`, sin migrar (recomendada); B, `automatizaciones` dentro de `config`.
5. **Cambiar la configuración.** A, caso «Configurar» en la skill de incorporación (recomendada); B, lo mismo y una orden de `cola.py` para los valores; C, a mano.
