---
antetitulo: Software Factory · Informe de diagnóstico · Noviembre 2026
lema: Lo que solo vale aquí, a la vista; // lo que bloquea, antes de la prueba.
subtitulo: Dónde se atasca un usuario nuevo al instalar el plugin sf, incorporar un proyecto y hacer su primera tarea, qué supone de esta máquina o del propietario y qué conviene arreglar antes de la prueba del colega.
version: Versión 1.0 · 02/11/2026
estado: Diagnóstico · Tarea 289
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
tipo: Informe de diagnóstico
pie: Primera tanda de la tarea «Primeros cinco minutos de un usuario nuevo con la SF» (289). Sale de leer plugins/sf en develop (sf 1.4.2), los README, el informe «Plugin en otros proyectos» (171) y el de «Incorporar sin cambiar el proyecto» (222, en su rama), y de un recorrido en una configuración desechable de Claude Code. Espera la decisión del propietario.
---
# Primeros cinco minutos

## Resumen | Tres cosas bloquean; el resto confunde | Resumen {#resumen}

Un colega que siga hoy las instrucciones no llega a su primera tarea. Se para en tres sitios:

- **No puede instalar.** El repositorio `jumibot/SoftwareFactory` es **privado**: `claude plugin marketplace add` falla sin acceso, y la página da 404 sin sesión.
- **No puede abrir su primera tarea.** Sin rama `develop`, `cola.py rama` responde «No hay rama develop.», y la incorporación no crea ni git ni `develop`. Pasa en una carpeta vacía y en cualquier proyecto que solo tenga `main`.
- **En macOS o Linux, Claude no puede usar la cola.** La orden fija es `python …`. Si en esa máquina solo existe `python3`, falla cada orden de la cola. El panel prueba `python` y `python3`, pero Claude no.

Lo demás no impide avanzar, pero hace dudar. No hay guía para quien empieza, y el README raíz está escrito para el propietario. JKanban sale en la incorporación. Cerrar sin remoto da un aviso que no se entiende. La metodología sigue hablando del registro común y del kanban de la SF, ya retirados («Sin registro ni mejoras de la SF desde otros proyectos», 194).

Casi todo lo que solo vale en esta máquina ya lo inventarió «Plugin en otros proyectos» (171) con la 1.2.0. En la 1.4.2 sigue igual, salvo el registro de uso, que lo retiró la decisión 194.

## Recorrido | Qué se ha podido hacer y qué no | Recorrido {#recorrido}

Se ha recorrido el camino en una configuración desechable (`CLAUDE_CONFIG_DIR` en el scratchpad), sin tocar `~/.claude` ni los plugins instalados:

1. **Leer el README raíz** como quien no sabe nada. No dice cómo instalar: remite al «propietario» y a «Claude Code». Las órdenes de instalación están en el README del plugin, entre el mod y «Publicar un cambio».
2. **`claude plugin marketplace add jumibot/SoftwareFactory`.** Funciona solo con las credenciales del propietario. La primera vez falló con «Filename too long»: el catálogo clona el repositorio entero, y los nombres de `docs/decisiones/` llegan a 130 caracteres. Con `core.longpaths` (puesto solo en el entorno de la orden) clona bien.
3. **`claude plugin install sf@softwarefactory --scope user`.** Instala la 1.4.2 y sus tres dependencias, sin errores.
4. **Abrir una carpeta vacía.** El mod carga: copia `cola.py` y su lanzador a `$CLAUDE_CONFIG_DIR/sf`. La sesión no sigue: «Not logged in». **No se ha recorrido la conversación** (pantalla completa, petición de incorporar, menús, orquestación) porque iniciar sesión en la configuración desechable necesita al propietario.
5. **Primera tarea sin Claude**, con `cola.py` sobre dos carpetas: una sin git y otra con git y solo `main`. En las dos, `crear --en-curso` funciona y `rama` se para en «No hay rama develop.». Con `develop` creada a mano, el ciclo llega a cerrar. El cierre avisa así: «Aviso: falta el push de develop (and the repository exists.)». Es la última línea del error de git, que sin remoto no se entiende. El commit lleva `Co-Authored-By: Claude Opus 5.5`, sea cual sea el modelo del colega.

## Atascos | Por gravedad, con el arreglo propuesto | Atascos {#atascos}

### Bloquean {#bloquean}

| Atasco | Dónde | Arreglo propuesto |
| --- | --- | --- |
| **1. Repositorio privado.** Sin acceso, el catálogo no se añade. | GitHub `jumibot/SoftwareFactory` | Decide el propietario: hacerlo público, invitar al colega (con `gh auth login` para que git clone por HTTPS) o crear un repositorio público solo de distribución. |
| **2. Sin `develop` no hay primera tarea.** La incorporación no hace `git init` ni crea `develop`. | `tools/cola.py` (`rama`); `skills/incorporar_proyecto_a_sf/SKILL.md` | Para la prueba basta lo mínimo. En el caso nuevo, `git init`, `main` con un primer commit y `develop` desde ella. En un proyecto existente sin `develop`, crearla desde `main`. Choca con la pregunta de ramas de «Incorporar sin cambiar el proyecto» (222), que propone no crear `develop`: lo decide la 222, o se acepta como arreglo provisional. |
| **3. `python` fijo en la orden de la cola.** En macOS y Linux suele haber solo `python3`. En Windows, `python` puede ser el atajo de la Microsoft Store. | `hooks/constantes.ts`, 32 (`ORDEN_COLA`); `skills/flujo_tareas/SKILL.md` | El panel ya sabe qué intérprete responde (`hooks/cola.ts`, 103). La orden que se da a Claude podría usar ese mismo, o ir a un lanzador `sf-cola` que lo elija. Si el colega usa Windows con Python instalado, no bloquea: basta decirlo en la guía. |

### Confunden {#confunden}

| Atasco | Dónde | Arreglo propuesto |
| --- | --- | --- |
| **4. No hay guía de arranque.** El README raíz da un estado viejo («sf 0.13.1»; va por la 1.4.2) y lo primero que enseña es el aviso de actualizar desde la 1.2.10. Las órdenes de instalación están junto a lo que solo sirve a quien desarrolla la SF. | `README.md`; `plugins/sf/README.md` | El paso 7: la guía de arranque. En el README raíz, un apartado «Probar la SF» que la enlace, y el aviso de la 1.2.10 más abajo. Al publicar, poner al día el estado. |
| **5. Requisitos sin decir.** Una versión reciente de Claude Code con mods (probada la 2.1.316), git con `user.name` y `user.email`, Python 3.10 o posterior (por los tipos `str \| None` de `cola.py`), la pantalla completa (`/tui fullscreen`) para que el panel reciba clics y reiniciar tras instalar. | — | En la guía, como lista de comprobación previa. |
| **6. JKanban en la incorporación.** Se pregunta `kanban` y la comprobación final lo exige. La descripción «la leen el panel, Claude Code Commander y JKanban». La `description` de la skill nombra «proyecto en JKanban». | `skills/incorporar_proyecto_a_sf/SKILL.md`, 3, 29, 31, 71, 83 | Dejar `kanban` como opcional y no preguntarlo, como propone «Configuración inicial» (190). Para la prueba basta quitarlo de la pregunta y de la comprobación final, y decir «la lee el panel». Esta tanda no toca la skill: se hace con la 222 o la 193, o en el paso 2 de esta. |
| **7. Push sin remoto.** El cierre avisa «falta el push de develop (and the repository exists.)». El panel cuenta un push pendiente que nunca se hará. | `tools/cola.py`, 435; `hooks/lectura.ts`, 170-180 | Sin remoto, no hacer push ni avisar de él. Ya está como paso de «Implementar la configuración inicial» (193): «Hacer push al remoto del proyecto…». Además, que el motivo cite la primera línea del error de git, no la última. |
| **8. Enlaces de la metodología a un repositorio privado.** Unos diez enlaces a decisiones, propuestas y la especificación dan 404. | `skills/metodologia/references/*.md`; `skills/orquestacion/references/porque.md` | Se resuelve con el atasco 1. Si el repositorio sigue privado, que el texto se entienda sin abrir el enlace. |
| **9. La metodología contradice la decisión 194.** Siguen el «Registro de uso» en el registro común de la SF y su bloque SF ENHANCE (sección 2), las mejoras «en SoftwareFactory» (7.6) y la automejora con el kanban de la SF (11). El Claude del colega podría intentar escribir en la SF. | `skills/metodologia/references/desarrollo-de-proyectos.md`, 62, 380, 504-508 | En la tarea «Actualizar las reglas del método» (208); texto propuesto en el informe de la tanda. La plantilla y `metodologia/SKILL.md` ya siguen la 194. |
| **10. Ejemplos con LecturaFàcil y `kanban`.** El panel de una carpeta sin SF propone un `proyecto.json` de ejemplo con `"kanban": "LecturaFàcil"`. Lo mismo pasa en el README del plugin y en la skill, con `"sf": "0.29.0"`. | `hooks/constantes.ts`, 61-65; `plugins/sf/README.md`, 17-24; skill de incorporación, 35-42 | Un ejemplo neutro («MiProyecto»), sin `kanban` y con la versión actual o `<versión>`. Va al paso 1. |
| **11. Todo en español.** Panel, mensajes de `cola.py`, skills y reglas. | Todo el plugin | Decide el propietario según quién sea el colega. Para esta prueba, se supone que lee español. |

### Menores {#menores}

| Atasco | Dónde | Arreglo propuesto |
| --- | --- | --- |
| **12. Rutas de esta máquina.** `claude --plugin-dir D:/Projectes/SoftwareFactory/plugins/sf`; el catálogo local en `D:/Projectes/.claude-plugin/`. El modo prueba reconoce la SF por el nombre de su carpeta. | `plugins/sf/README.md`, 68; `hooks/prueba.ts`, 13 y 103 | `<repositorio de la SF>/plugins/sf` en el README y el comentario sin ruta (paso 1). El modo prueba solo afecta a quien desarrolla la SF. |
| **13. Firma fija del cierre.** `COAUTOR = 'Co-Authored-By: Claude Opus 5.5 …'`. | `tools/cola.py`, 74 | Quitar el modelo fijo: firma configurable o ninguna (171, pregunta 4, sin decidir). |
| **14. Historia del propietario en el plugin.** Ocho `ORIGIN.md` con rutas `D:/` y proyectos suyos. El kit de documentos menciona OncoCore en sus comentarios. `documento_fundacional` toma como modelo un archivo de SmartColdBox que el colega no tiene. | `skills/*/ORIGIN.md`; `tools/kit_documentos/*`; `skills/documento_fundacional/SKILL.md`, 27; `skills/documento_vision/SKILL.md`, 313 | Paso 1: los `ORIGIN.md` de las skills propias, a `docs/referencias/` de la SF, y en el plugin solo la licencia de lo de terceros. Sacar OncoCore de los comentarios. En el fundacional, el modelo solo «si está disponible», con las reglas escritas en la skill. |
| **15. Rutas largas en Windows.** El catálogo clona el repositorio entero, con `docs/`, `_respaldo/` y los html. Con un perfil de usuario de nombre largo, o una carpeta de configuración profunda, falla con «Filename too long». | `docs/decisiones/` (nombres de hasta 130 caracteres) | En la guía: `git config --global core.longpaths true` si falla. Más adelante, un catálogo más ligero o nombres de decisión más cortos. |
| **16. La orden de la cola usa `$HOME/.claude`** aunque haya `CLAUDE_CONFIG_DIR`. Sin `~/.claude/sf/cola.py`, falla. En esta máquina no se nota porque existe el del propietario. | `hooks/constantes.ts`, 32 | Solo afecta a configuraciones aparte, como la del ensayo del paso 8. Para que el ensayo sea fiel, hacerlo con un `HOME` (o `USERPROFILE`) desechable, no solo con `CLAUDE_CONFIG_DIR`. |
| **17. El plugin publicado lleva `tests/`**, con rutas y nombres de prueba (`D:/sf`, JKanban). | `plugins/sf/tests/` | Dejar: Claude no los carga. |
| **18. `dataviz`** no es un plugin: la trae el entorno de claude.ai. En Claude Code a secas puede faltar. | README raíz; `skills/documento_vision/SKILL.md` | La skill ya dice qué hacer si falta. Basta mencionarlo en la guía. |

## Inventario | Lo que solo vale aquí o para el propietario | Inventario {#inventario}

Búsqueda en `plugins/sf/` (sin `tests/`) de rutas `D:`/`C:`, `Projectes`, el usuario y el correo, los proyectos del propietario, JKanban, Commander, Windows, PowerShell y Python. No aparecen ni el usuario de Windows ni el correo. Lo que sale:

- **Para la prueba** (pasos 1 y 2): los atascos 2, 3, 6, 7, 10 y 12.
- **Ruido, no bloquea:** los atascos 13, 14 y 17.
- **Identidad de la distribución, se deja:** `jumibot` como autor y dueño del catálogo, `sf@softwarefactory`, «SoftwareFactory» en morado para la propia SF.
- **Windows:** el mod ya distingue Windows de los demás sistemas (`hooks/cola.ts`, 115) y prueba `python` y `python3`. Lo que solo funciona en Windows es la orden de Claude (atasco 3).
- **MCP propios:** el plugin no declara ninguno. JKanban aparece solo como texto (atascos 6 y 10, y la metodología).

## Otras tareas | Qué ya está en marcha | Otras {#otras}

- **«Incorporar un proyecto sin cambiarlo» (222)**: decide si se crea `develop` (atasco 2), dónde viven la cola y el estado, y los nombres de ramas y remoto. Si su respuesta llega tarde para la prueba, el atasco 2 necesita un arreglo provisional.
- **«Implementar la configuración inicial» (193)**: `kanban` opcional (atasco 6) y push al remoto del proyecto (atasco 7).
- **«Poner un proyecto al día con la SF sin tarea» (288)**: el caso «actualizar». No afecta a un usuario nuevo.
- **«Actualizar las reglas del método» (208)**: la metodología y la decisión 194 (atasco 9).

## Decidir | Lo que decide el propietario | Decidir {#decidir}

1. **Acceso al repositorio (atasco 1).** A: hacerlo público. B: invitar al colega como colaborador (necesita `gh auth login`). C: un repositorio público solo para distribuir el plugin. Recomendación: A si no hay nada que ocultar; si no, B para esta prueba. Antes de A, conviene repasar `docs/` y `_respaldo/`, que pasarían a ser públicos.
2. **Sistema del colega.** ¿Windows, macOS o Linux? Si no es Windows, el atasco 3 bloquea y hay que arreglarlo antes de la prueba.
3. **`develop` en la prueba (atasco 2).** A: esperar a la 222. B: arreglo provisional en el paso 2 de esta tarea (crear git y `develop` en el caso nuevo, y `develop` desde `main` en el existente), que la 222 rehará si decide otra cosa. Recomendación: B si la prueba va antes que la 222.
4. **Qué se arregla antes de la prueba.** Recomendación: los atascos 1 a 7, 10 y 12, y la guía (atasco 4, en el paso 7). Los atascos 8, 9 y 11, según la respuesta 1 y la tarea 208. Los menores, después.
5. **Recorrido con sesión real (paso 5).** Para recorrer la conversación (incorporar y primera tarea con Claude) hace falta iniciar sesión en una configuración desechable. A: el propietario inicia sesión una vez en `CLAUDE_CONFIG_DIR` y `HOME` desechables, y el recorrido se repite ahí. B: dejar la conversación para el ensayo del paso 8. Recomendación: A, para encontrar ahora los atascos de la conversación.
6. **Idioma (atasco 11).** ¿El colega lee español? Si no, la prueba tiene otro alcance.

## Prueba | Qué mirar cuando se recorra con sesión | Prueba {#prueba}

En una configuración desechable (`CLAUDE_CONFIG_DIR` y `HOME` en una carpeta temporal), con el plugin instalado desde el catálogo publicado:

1. **Arranque en una carpeta vacía.** El panel dice «Sin SF» y propone «incorpora este proyecto a la SF». Mirar si se abre solo o hay que activar la pantalla completa, y qué entiende de eso alguien nuevo.
2. **«Incorpora este proyecto a la SF».** Mirar el menú del caso, que pregunte el nombre, la descripción y el color, y si pregunta por JKanban. Mirar si crea git y `develop` y si el color y el nombre se aplican sin `/color` ni `/rename`.
3. **Primera tarea («añade un README»).** Mirar si va a la cola, si se crea su rama, si lanza un subagente con su worktree y si cierra sin el aviso de push.
4. **Cuánto tarda y cuántas preguntas hace** antes de que el colega vea su primera tarea hecha: es la medida de los cinco minutos.
