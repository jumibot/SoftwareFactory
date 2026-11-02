# Especificación para construir la Software Factory

Estado del documento: **borrador de trabajo**, pendiente de revisión y aprobación como especificación completa.

Los acuerdos recogidos conservan su validez; el estado de borrador no los convierte en propuestas. No constituye una implementación ni una selección de skills aprobada.

## Cómo interpretar este documento

- **Acuerdo:** requisito decidido por el propietario; debe respetarse. Su porqué está en las [decisiones de la SF](../../decisiones/README.md).
- **Preferencia:** opción favorita, cuya adecuación se confirma en cada contexto.
- **Pendiente:** información o decisión todavía necesaria, reunida al final.
- **Ejemplo:** empieza por «Ejemplo:» o «por ejemplo» e ilustra; no manda nada.

Lo que aún no está decidido (organización del repositorio, skills candidatas, orden de construcción, estados del kanban…) vive en las [propuestas](../../propuestas.md). Las plantillas están en el plugin `sf` (`plugins/sf/templates/`).

## Propósito y alcance

Construir un proyecto central para documentar, desarrollar, evaluar, versionar y distribuir una Software Factory personal para Claude Code.

La SF debe permitir aplicar la [metodología de desarrollo de proyectos](../../../plugins/sf/skills/metodologia/references/desarrollo-de-proyectos.md). Ese documento es la referencia sobre el ciclo de trabajo, los perfiles técnicos, las estructuras de aplicación, las pruebas y los informes. Aquí se define qué construir para soportarlo, sin duplicar esas reglas.

La inspiración inicial fue el [vídeo de Eric Risco sobre software factories](https://www.youtube.com/watch?v=p6nnqerea7w). La metodología es propia y no presupone adoptar su implementación.

## Resultados que debe proporcionar la SF

- Documentación central y plantillas alineadas con la metodología.
- Skills propias y especializadas seleccionadas o adaptadas.
- Perfiles técnicos reutilizables con opciones favoritas y excepciones explícitas.
- Distribución e instalación versionadas para múltiples proyectos.
- Integración del kanban existente mediante MCP.
- Evaluaciones y un piloto antes de publicar una versión estable.

## Integración del kanban

Revisar primero la aplicación local multiproyecto existente. Construir un MCP que permita consultar proyectos, devslices y tareas, crear y ordenar trabajo, actualizar estados y dependencias, registrar bloqueos y enlazar documentos e informes.

El modelo y las transiciones deben respetar la metodología. Las actualizaciones deben confirmarse y los errores deben ser visibles para que no se dé por actualizado un tablero que no lo está. El diseño concreto de operaciones, validaciones, historial y recuperación se decidirá al inspeccionar la aplicación.

La ubicación del MCP —en este repositorio o en uno propio— está pendiente de decidir.

## Piloto — acuerdo (propietario, 2026-10-25)

LecturaFàcil es el proyecto piloto de la SF y su caso conductor: recorre el circuito completo del método y sirve de ejemplo en los documentos de la SF. Su contexto técnico, «de momento», es una aplicación de escritorio en Python, Tkinter y SQLite, con Claude Code como agente dentro del producto, instalada en local en el centro y con credencial intercambiable: el caso del perfil de escritorio con agente de la metodología.

JKanban es una herramienta de la SF, no un caso: usarlo como ejemplo sería recursivo, porque forma parte de la propia SF.

## 1. El proyecto central de la SF

La propia SF tendrá un proyecto y repositorio desde el que se documentará, desarrollará, probará y evolucionará.

Contendrá:

- Metodología y decisiones sobre su evolución.
- Skills propias, skills externas seleccionadas y adaptaciones.
- Plantillas de documentos.
- Perfiles tecnológicos y opciones favoritas.
- Casos de evaluación de las skills y del proceso.
- Mecanismo de distribución, instalación y actualización.
- Historial de versiones y cambios.
- Registro de [decisiones](../../decisiones/README.md) y de [propuestas](../../propuestas.md), separados (acuerdo del propietario, 2026-10-27). Cada decisión, en su archivo de `docs/decisiones/`, con un índice generado por comando (acuerdo del propietario, 2026-10-29).

La organización del repositorio que no está fijada en la sección 2 sigue abierta (propuesta «Organización del repositorio de la SF»).

Las skills se editan en este repositorio, no en copias instaladas dispersas. Desde aquí se publican versiones identificables para utilizar en otros proyectos.

Se propone mantener una distribución estable para uso habitual y evaluar los cambios de la SF de forma aislada. Cada proyecto consumidor debe poder identificar la versión que utiliza.

**Fuente y uso operativo — acuerdo (propietario, 2026-10-27):** el repositorio de la SF es la fuente, donde se crea y se modifica todo; no es una instalación operativa. Ningún proyecto usa directamente la copia de trabajo de la SF: usa lo publicado (subido a GitHub) e instalado como copia propia, que solo cambia cuando se actualiza a propósito. Los cambios se prueban antes en una sesión aparte (`claude --plugin-dir <carpeta>`).

**Plugin de la SF — acuerdo (2026-10-27):** la SF llega a los proyectos como un plugin de Claude Code, `sf`, publicado desde este repositorio. La estrategia completa está en la sección 2, «Plugin y mods de la SF».

La integración MCP del kanban podrá vivir en este repositorio o en uno propio. Está pendiente decidirlo al revisar la aplicación existente.

## 2. Skills de la SF

### Organización general — acuerdos

Las fuentes de las skills propias de la SF, y de las versiones nuestras de skills externas, se guardan **dentro del plugin `sf`, en `plugins/sf/skills/`** (acuerdo del propietario, 2026-10-27; antes, `skills/` en la raíz), versionadas junto con su documentación y recursos. Una skill externa que la SF usa tal cual no se copia: es una dependencia del plugin (ver «Skills externas», acuerdo del propietario, 2026-11-01). Cada skill tiene una carpeta y su archivo principal `SKILL.md`. La biblioteca de los documentos HTML, que comparten varias skills, está en `plugins/sf/tools/kit_documentos/`.

```text
SoftwareFactory/
├── .claude-plugin/marketplace.json   # catálogo softwarefactory: sf y las dependencias fijadas a un commit
├── plugins/
│   └── sf/                          # el plugin de la SF
│       ├── .claude-plugin/plugin.json
│       ├── hooks/                   # mods
│       ├── skills/
│       │   └── nombre-descriptivo/
│       │       ├── SKILL.md
│       │       ├── ORIGIN.md
│       │       ├── references/      # Consulta y explicaciones opcionales
│       │       ├── templates/       # Modelos de salida opcionales
│       │       └── scripts/         # Automatización opcional
│       ├── templates/               # plantillas (estructuras de los perfiles)
│       └── tools/                   # kit_documentos/ e indice_decisiones.py
├── docs/
│   ├── decisiones/                  # una decisión por archivo; README.md, el índice
│   └── propuestas.md
└── _respaldo/
```

Crear únicamente los recursos necesarios. Este ejemplo describe organización, no una selección de skills iniciales ni un mecanismo de carga automática.

### Archivo principal y material auxiliar

`SKILL.md` define objetivo, condiciones de uso, información necesaria, procedimiento, resultado esperado, comprobaciones y condiciones de intervención humana. Las reglas esenciales deben permanecer en este archivo.

`references/` contiene material de consulta: explicaciones detalladas, ejemplos, criterios de calidad, decisiones técnicas o errores habituales. Permite ampliar instrucciones sin incluir todo el detalle en el archivo principal. Es opcional.

**Las referencias no son subskills.** No tienen un procedimiento independiente por el hecho de estar en esa carpeta. Si una capacidad requiere objetivo, entradas, pasos y resultado propios y puede utilizarse por separado, se puede definir como otra skill con su propio `SKILL.md`.

Cada referencia se enlaza desde `SKILL.md` mediante una ruta relativa y se indica **cuándo debe consultarse**, preferiblemente en el paso correspondiente o en un índice breve. No asumir que todos los archivos de `references/` se leerán automáticamente en cada ejecución.

Ejemplo ilustrativo dentro de un `SKILL.md`:

```markdown
## Referencias

- [Criterios de aceptación](references/criterios-aceptacion.md):
  consultar al redactar o revisar criterios de una devslice.
- [Diseño de interfaz](references/diseno-interfaz.md):
  consultar cuando la devslice incluya pantallas o interacción.
```

Distinguir los recursos y las salidas:

| Componente | Función |
| --- | --- |
| `SKILL.md` | Qué hacer, en qué orden y cómo comprobarlo. |
| `references/` de la skill | Cómo hacerlo bien: explicaciones, ejemplos y criterios de consulta. |
| `templates/` de la skill | Modelos que se rellenan para producir documentos. |
| `scripts/` de la skill | Automatizaciones auxiliares, cuando sean necesarias. |
| `docs/referencias/` del proyecto consumidor | Estudios y materiales específicos que considerar en esa aplicación. |
| Documentación producida en el proyecto consumidor | Resultados concretos, por ejemplo `docs/specs/devslices/crear-registro/especificacion.md`. |

No guardar los resultados de ejecutar una skill dentro de sus referencias ni modificar sus plantillas como sustituto de crear el documento del proyecto. Las plantillas comunes a varias skills pueden mantenerse en `templates/` de la raíz; definir su acceso sin duplicar copias editables.

### Fuentes, instalación y distribución

| Ubicación | Responsabilidad |
| --- | --- |
| `plugins/sf/` de la SF | Fuente del plugin `sf` (skills, kit de documentos y mods), listado en el catálogo `.claude-plugin/marketplace.json`. Fuente oficial editable, evaluada y versionada. |
| Skills procedentes de plugins ajenos | Copia en `plugins/sf/skills/`, con procedencia y versión; declarar aparte los componentes del plugin necesarios para ejecutarlas. |
| `~/.claude/plugins/cache/softwarefactory/` | Copia operativa del plugin `sf`, instalada por Claude Code desde GitHub. Nunca se edita ni se sustituye por la carpeta de trabajo de la SF. |
| `~/.claude/skills/` y `~/.claude/tools/` | Ya no reciben nada de la SF: las copias globales se retiraron el 2026-10-27 al pasar las skills al plugin. |
| `agent-runtime/skills/` de una aplicación | Fuentes de las skills operativas del agente de ese producto. |

No mantener copias editables independientes como fuentes equivalentes. Instalación y actualización parten de una versión publicada del plugin `sf` (siguiente apartado).

### Plugin y mods de la SF — acuerdos (propietario, 2026-10-27)

**Qué es cada cosa.**

- Un **plugin** de Claude Code es una carpeta con nombre y versión (`.claude-plugin/plugin.json`). Puede llevar skills, comandos, subagentes, hooks, servidores MCP y mods, y se instala y actualiza como una sola pieza.
- Un **mod** es la parte de un plugin que cambia la interfaz o el comportamiento de Claude Code: línea de estado, banda sobre el prompt, panel, avisos, comandos o reacciones a la sesión. Es un módulo de hooks (`hooks/hooks.json` y `hooks/register.tsx`) dentro del plugin.

**Estrategia.**

1. **Un solo plugin, `sf`.** Todo lo que la SF distribuya a los proyectos irá en él: los mods, los comandos, los hooks (por ejemplo, la daily) y el MCP de JKanban, cada pieza cuando exista y se apruebe. No se crea un plugin por pieza.
2. **Fuente en `plugins/sf/`**, listado en el catálogo `softwarefactory` (`.claude-plugin/marketplace.json`, en la raíz del repositorio). Ahí se crea y se modifica.
3. **Se usa lo publicado, activado para el usuario.** El catálogo se añade desde GitHub (`claude plugin marketplace add jumibot/SoftwareFactory`). El plugin se instala con ámbito de usuario (`claude plugin install sf@softwarefactory --scope user`): queda activo en todos los proyectos, como antes las skills globales (acuerdo del propietario, 2026-10-27). El mod distingue solo los proyectos bajo la SF (los que tienen `.sf/proyecto.json`) de los demás. Claude Code guarda la copia operativa en `~/.claude/plugins/cache/softwarefactory/sf/<versión>/`. Nunca se instala desde la carpeta de trabajo de la SF (sección 1).
4. **Desarrollo aislado.** Un cambio se prueba en una sesión aparte con `claude --plugin-dir D:/Projectes/SoftwareFactory/plugins/sf`, que sustituye al instalado solo en esa sesión y recarga al guardar. En las sesiones dedicadas a crear mods, Claude Code puede cargarlos además desde la carpeta de mods de la sesión. La fuente que vale es siempre la de `plugins/sf/`.
5. **Publicar.** Subir la `version` del `plugin.json` (la copia instalada se guarda por versión; solo al publicar, nunca en una feature), pasar `develop` a `main`, marcarlo con el tag `vX.Y.Z` y hacer push. Cada tarea llega antes a `develop` desde su rama, por squash, una vez probada (metodología, 2; acuerdo del propietario, 2026-10-29). Después: `claude plugin marketplace update softwarefactory` y `claude plugin update sf@softwarefactory`.
6. **Comprobar antes de publicar:** `claude plugin validate plugins/sf`, las pruebas del mod (`claude plugin test plugins/sf`), la comprobación de tipos del módulo (`tsc`) y, si cambian las skills de documentos, regenerar un documento y compararlo.

**Contenido actual (0.28.7).**

- **Metodología:** la skill `sf:metodologia`, con el documento del método como referencia (`plugins/sf/skills/metodologia/references/desarrollo-de-proyectos.md`; acuerdo del propietario, 2026-10-27). Es su única fuente.
- **Skills:** las propias de la SF y las versiones nuestras de externas (`plugins/sf/skills/`). Se invocan con el prefijo `sf:`, por ejemplo `sf:documento_vision`. Las externas que se usan tal cual llegan como dependencias del plugin y se invocan con el prefijo de su plugin (acuerdo del propietario, 2026-11-01). Las que producen documentos aplican la norma de diagramas en SVG, nunca en ASCII ni en mermaid (metodología, 6; norma del propietario, 2026-10-27).
- **Kit de documentos** (`plugins/sf/tools/kit_documentos/`): las skills de documentos lo buscan dos carpetas por encima de sus scripts, así que skills y kit viajan juntos. Distribuir siempre los recursos junto a `SKILL.md`, con rutas relativas válidas, y declarar las dependencias entre skills.
- **Mod de estado**, centro de control de la SF dentro de Claude Code (peticiones del propietario, 2026-10-27; detalle y versiones en [Cómo funciona](../../como-funciona-la-software-factory.md), «Mod de estado»):
  - **Panel lateral** (`/sf`): en pantalla completa se abre solo al empezar la sesión; `/sf` lo reabre. Arriba, el proyecto y, bajo la SF, versión, fase y devslice; tras una línea en blanco, en amarillo y sin marca delante, la tarea en la que se trabaja (las peticiones en curso, una línea cada una, o la devslice) y, bajo ella, su paso en curso con la cuenta de pasos, «1/3» (acuerdo del propietario, 2026-10-28).
  - **Secciones plegables**, con su cuenta en la cabecera, en un solo bloque, con su fondo y sin rótulo (2026-11-01), en el orden del ciclo de una tarea (norma del propietario, 2026-10-28): Pendientes, la cola, con su total; En observación (2026-11-02), con qué mirar y, con «✓» verde, lo que Claude ya ha comprobado; Cerradas, lo cerrado en esta sesión; y Propuestas, las de `propuestas.md` del proyecto (2026-11-01). Las en curso van arriba, en amarillo, una por línea (norma del propietario, 2026-10-28). El número de cada tarea lleva el color de su estado, sin letra detrás (2026-10-31): nueva en la sesión, de antes, en observación, cerrada, descartada o revertida. Con JKanban, un estado más marcaría una planificada sin empezar (propuesta P23). El bloque PROYECTO y SF ENHANCE desaparecieron (2026-11-01). Un clic (o Tab y Enter) las pliega; lo plegado se recuerda entre sesiones. En un proyecto sin SF, el panel enseña cómo incorporarlo.
  - **Legibilidad en un panel estrecho**: tres niveles de sangría (sección, elemento, detalle). Cada petición o commit ocupa una línea recortada al ancho; desplegado, el título sale entero una sola vez y, al partirse, vuelve a la izquierda; el detalle (commit, qué probar) va con sangría 2 y sin sangría colgante.
  - **Marcador de la sesión**, fijo arriba, en la fila del nombre del proyecto y fuera de las secciones: los prompts enviados. Las cerradas se cuentan, en verde, en la cabecera de Cerradas; las propuestas, en Mejoras SF a valorar.
  - **Cerradas**: siempre visible, también con 0 (acuerdo del propietario, 2026-10-28); las peticiones cuyo cierre cambia en la sesión (a observación, cerradas o reabiertas, aunque se cerraran en otra sesión; acuerdo del propietario, 2026-10-28), con su antigüedad y su cuenta en la cabecera, sin reparto (2026-10-31). Un color por letra, en las cuentas y en los códigos: rojo solo para las H, verde solo para las C; la tarea en curso, en amarillo; el resto, en un gris más apagado que el texto normal y sin negrita (acuerdo del propietario, 2026-10-28) (norma del propietario, 2026-10-28). En la fila del título, a la derecha, «limpiar (N)» las saca de la lista (2026-10-29); si una se reabre, vuelve (acuerdo del propietario, 2026-10-28).
  - **Tarea en observación que se está mirando** (acuerdo del propietario, 2026-10-28; nombres de 2026-11-02): Claude la marca `observando` y el panel la muestra arriba, en amarillo, como las en curso, hasta que llega el resultado.
  - **Filas de tareas** sin «▸/▾»: el código de las que se despliegan va subrayado (norma del propietario, 2026-10-28).
  - **Con JKanban** (decisión del propietario, 2026-10-27; pendiente de incorporarlo): el panel añade una sección Planificado y deja de mostrar Fases; Pendientes sale cuando sus elementos pasan al backlog. Solo van al backlog las peticiones que quedan pendientes; las menores que se resuelven en el momento, no.
  - **Cola de peticiones** en `.sf/peticiones.json` (metodología, 2): Claude anota cada petición al llegar y la cierra con su commit; con «A observación», lo cerrado queda en observación (`en-observacion`) con qué mirar, y después se cierra o se revierte (2026-11-02).
  - **Un proyecto por sesión**: bloquea las escrituras en otro proyecto, salvo registrar una propuesta en la SF.
  - **Mejoras** (antes Mejoras SF a valorar, Propuestas por decidir y, antes, Realimentación; acuerdo del propietario, 2026-10-28): en la SF, las propuestas de `docs/propuestas.md` que esperan su sí o no, con una línea que lo dice. Cada una ocupa una línea, con su número fijo (P01, P02…; acuerdo del propietario, 2026-10-28); un clic la despliega con su resumen (la primera frase de su «Cambio propuesto»). Cuenta también las abiertas y las que faltan por pasar al kanban. En otro proyecto, la sección se llama Realimentación y avisa de las mejoras registradas en la SF.
  - **Identidad de la sesión**: `/color` con el color del proyecto y `/rename` con el nombre del proyecto, solo al entrar en la sesión; recargar el plugin no los repite (norma del propietario, 2026-10-28).
  - **Nada en la última fila**: las métricas están solo en la sección Sesión (decisión del propietario, 2026-10-27).
  - **Caja sobre el prompt**, solo de reserva cuando no hay panel: `SF · <proyecto> · <n>/7 <fase> · devslice <nombre>`, `SF · repositorio de la SF` o `Sin SF`, las peticiones en curso y las cuentas. Sin línea de estado (decisión del propietario, 2026-10-27).
  - **Lectura**: `.sf/` (`proyecto.json`, `estado.json`, `peticiones.json`; metodología, 6), al abrir la sesión, al acabar cada turno y tras cada herramienta que puede escribir, para que la tarea en curso se vea al momento. No escribe nada. Si solo encuentra el antiguo `docs/sf.json`, lo lee y avisa de que hay que moverlo.
- **Plantillas** (`plugins/sf/templates/`): las estructuras de carpetas de los perfiles de la metodología (7), en `estructuras/`.
- Instrucciones en `plugins/sf/README.md`.

**Límites conocidos.**

- Claude Code no documenta que dos proyectos usen versiones distintas del mismo plugin: hay una versión instalada por plugin y usuario.
- Con ámbito de usuario, la activación no queda en el repositorio de cada proyecto; lo que dice si un proyecto está bajo la SF es su `.sf/proyecto.json`.

**Skills externas — acuerdo (propietario, 2026-11-01; decisiones 175 y 176; sustituye a lo acordado el 2026-10-25 en la decisión 007).**

- **Tal cual, como dependencia.** Una skill externa que la SF usa tal cual no se copia en el plugin: es una dependencia de `sf`, que se instala con él (`dependencies` del `plugin.json`). Se invoca con el prefijo de su plugin, no con `sf:`.
- **Cómo se declara.** El marketplace de la SF le da una entrada que apunta a su repositorio fijado a un commit (`source` `url` o `git-subdir`, con url https y `sha`; nunca `github`, que clona por SSH y falla en un equipo sin clave: comprobado el 2026-11-02), aunque el repositorio ya sea un plugin con su propio marketplace. Así, instalar `sf` la trae sin añadir antes ningún catálogo ajeno; sin ese catálogo, una dependencia de otro marketplace deja `sf` sin cargar (comprobado el 2026-11-01). La SF mueve la versión cambiando el commit, cuando le interesa. Si el repositorio tiene un `plugin.json` en su raíz, `git-subdir` de la carpeta de las skills lo evita. Si hay que elegir solo las skills que se usan, se usa `git-subdir` con `path` en la carpeta de las skills, `strict: false` y `skills`: con `url` o `github`, que clonan el repositorio entero, `skills` se suma a la carpeta `skills/` y se cargan todas (comprobado con `github` el 2026-11-01).
- **Instalación y actualización.** Al instalar `sf`, Claude Code instala sus dependencias. `claude plugin update` no instala las dependencias nuevas, y sin una de ellas `sf` no carga (comprobado el 2026-11-01). Por eso el botón ACTUALIZAR del panel, mientras aún corre la versión vieja, instala las dependencias de la versión nueva que falten antes de recargar o pedir reiniciar. ACTUALIZAR sale cuando hay una versión publicada sin instalar; cuando la instalada es más nueva que la que corre la sesión, sale REFRESCAR, que instala las dependencias que falten y recarga el plugin, con el aviso «Esta sesión usa la SF X y está instalada la Y: pulsa REFRESCAR» (acuerdo del 2026-11-01, decisión 177). Si una falla, avisa con la orden exacta y no recarga. Es configurable (`automatizaciones.dependencias_al_actualizar` en `.sf/proyecto.json`, encendido por defecto; decisión 171). Las instrucciones de publicación (`plugins/sf/README.md`) llevan las órdenes para actualizar a mano.
- **Personalizada, como versión nuestra.** Solo viaja en `plugins/sf/skills/` una skill externa que la SF ha cambiado. Entonces es una versión nuestra, con su origen y sus cambios en su `ORIGIN.md`, sin alterar los avisos del autor. Si la licencia impide copiarla o redistribuirla, informar al propietario y resolverlo antes.
- **Lo que no es un plugin no puede ser una dependencia** (por ejemplo, `dataviz`, que trae el entorno). Se anota como requisito del entorno en la skill que la usa, con qué hacer si no está.
- **Hoy:**
  - Del marketplace de la SF: `gsap-skills` ([greensock/gsap-skills](https://github.com/greensock/gsap-skills), commit `aed9cfd`, solo las cinco skills que se usan), `threejs-skills` ([CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills), commit `0e18186`, solo las diez que se usan) y `oklch-skill` ([jakubkrehel/oklch-skill](https://github.com/jakubkrehel/oklch-skill), commit `0e81f04`).
  - `dataviz`, requisito del entorno de `documento_vision`.

Por cada dependencia, el `ORIGIN.md` de la skill propia que la usa anota:

- Autor y repositorio o fuente original.
- Versión, etiqueta o commit, o que no está fijada.
- Licencia.
- Para qué se usa.
- Qué hacer si no está.

Una versión nuestra anota además los recursos que copia y sus modificaciones, con su justificación. Hoy todas las skills usan `ORIGIN.md`, y fijarlo como formato es una propuesta («Formato del archivo de procedencia de las skills»).

Las actualizaciones externas se revisan como cambios explícitos. En una dependencia fijada a un commit, cambiar el `sha` es un cambio de la SF, que se revisa y se publica como tal. En una versión nuestra, comparar con la versión de origen, preservar las adaptaciones, evaluar el resultado y publicar una nueva versión de la SF. No cargar a la vez una versión nuestra y la original sin una decisión explícita.

Guardar una skill no implica que baste para ejecutar todo su plugin: identificar y configurar las dependencias necesarias. Distinguir las capacidades ya disponibles en la instalación del usuario de las que realmente suministra la SF.

Las skills operativas pertenecen a cada aplicación. La SF puede proporcionar plantillas o piezas reutilizables, manteniendo explícita su versión y evitando que una actualización de skills de desarrollo altere inadvertidamente el producto.

### Claude Code Commander — acuerdo (propietario, 2026-10-27)

Aplicación aparte de la SF, pieza clave para trabajar con varias sesiones de Claude Code a la vez. Vive en el plugin `sf` y se usa desde el ordenador, la tableta y el móvil; la tecnología está por decidir. Su alcance, que se irá concretando:

1. Ver todas las sesiones abiertas, con su proyecto, fase, peticiones y avisos.
2. Dar órdenes a las sesiones.
3. Conducir Claude Code: abrir y cerrar sesiones, lanzar tareas y enviar prompts.
4. Lanzar sobre Claude Code las tareas del proyecto en JKanban.
5. Llevar métricas del trabajo, para poner control al desarrollador que lo hace todo a la vez.

El mod de cada sesión es su enlace: le envía el estado y ejecuta las órdenes de esa sesión, de modo que se respeta «Un proyecto por sesión». Lo que falta concretar está en la propuesta «Claude Code Commander: lo que falta concretar». Ver la decisión «Claude Code Commander».

### Mantenimiento y comprobación

Antes de publicar una skill, comprobar sus instrucciones, enlaces y recursos y evaluarla con casos representativos. Confirmar que las referencias indican cuándo leerlas y que las dependencias están disponibles en el destino. Las mejoras siguen el circuito de propuesta y aprobación de automejora de esta especificación.

Estas convenciones generales no aprueban ni amplían el catálogo inicial. La selección de skills concretas se decidirá por separado, aprovechando primero las disponibles y evitando duplicados.

### Propias de la metodología

- Incorporación de un proyecto: skill `incorporar_proyecto_a_sf` (2026-10-28, sin validar). Es una operación sin tarea, guiada por menús (2026-11-02). Prepara un proyecto nuevo o existente, lo pone al día con la versión actual de la SF o diagnostica qué le falta: identidad y configuración en `.sf/proyecto.json`, ramas `develop` y `main`, remoto en GitHub, estado, cola, `.gitignore` y los documentos de la SF en `sf/` (propuestas, decisiones e informes). No mueve ni renombra nada del proyecto (2026-11-02) ni escribe líneas de la SF en su `CLAUDE.md`: las reglas y la orquestación las entrega el mod (2026-11-01). Al poner al día un proyecto antiguo, quita la copia `.sf/claude-sf.md` y su importación. Si el `CLAUDE.md` es complejo, revisarlo es una tarea de una sesión entera.
- Visión: incorporar la skill existente del propietario.
- Documento fundacional: skill `documento_fundacional` (2026-10-26). Es la presentación formal del proyecto o de cada producto, sin historia conductora, junto a la visión en `docs/specs/vision/`. Tiene un núcleo de secciones, secciones opcionales y una maqueta editorial que se imprime en A4. Está pensada para todos los proyectos. Comprobada con dos documentos de SmartColdBox, pero sin validar todavía con el propietario.
- Especificación funcional global y diseño de interfaz: reúne las funcionalidades desde la visión, las referencias, el estudio de mercado y otras fuentes de requisitos. El diseño de interfaz ya tiene skill, `diseno_interfaz` (sin validar).
- Definición técnica y selección de perfil: skill `definicion_tecnica` (sin validar), con el registro de decisiones.
- Planificación por devslices: incrementos de construcción relacionados con las funcionalidades, sin copiar su lista. Propone el plan con las recomendaciones generales de la metodología (devslices de una o dos sesiones, ordenadas por lo que hace falta para comprobar lo siguiente, con las integraciones caras o inciertas al final y simuladas hasta entonces) y lo ajusta con el propietario.
- Preparación de devslice y creación de tareas en el kanban, comprobando que la devslice sigue cabiendo en una o dos sesiones.
- Diseño y revisión de pruebas respecto a requisitos.
- Coordinación del desarrollo, revisión y cierre.
- Operación del kanban por MCP y mantenimiento del contexto.

### Especializadas

Seleccionar según necesidad: Python, Tkinter o Qt, React, FastAPI, SQL nativo, arquitectura, UX/UI, contratos API, pruebas, revisión, seguridad, diagnóstico, graficación y distribución.

Las skills aportan técnicas; el perfil y las decisiones del proyecto seleccionan tecnologías. Evitar que cada skill imponga su propia metodología incompatible.

**Método propio, técnicas reutilizadas — acuerdo.** Cada skill de paso es una capa fina: las reglas del método de la SF (qué entra, qué sale, dónde se guarda, qué pasa al kanban y cuándo decide el propietario) sobre técnicas tomadas de terceros y adaptadas, sin su flujo ni su infraestructura. Antes de escribir una skill de paso, buscar la técnica equivalente y leerla entera. Solo se escribe técnica propia cuando no hay equivalente; la skill de visión es propia por decisión del propietario. El `ORIGIN.md` de cada skill indica qué se tomó, de qué versión y con qué licencia.

Cada skill propia debe definir entradas, procedimiento, resultados, comprobaciones y condiciones de intervención humana. Conservar procedencia, licencia, versión y modificaciones de las externas, en la versión nuestra o, si es una dependencia, en el `ORIGIN.md` de la skill propia que la usa.

### Skills candidatas

Las skills externas localizadas para evaluar, ninguna instalada ni validada, están en la propuesta «Skills externas candidatas». No considerarlas aprobadas.

## Capacidades que la SF debe soportar en los proyectos

Además de los perfiles de arquitectura y tecnología, contemplar estas capacidades combinables, definidas en la metodología:

- **Agente operativo en el backend:** Claude Code ejecuta funcionalidades del producto. Preparar plantillas para instrucciones, skills, hooks, herramientas y validadores de ejecución, separadas del entorno usado para desarrollar.
- **Persistencia SQL nativa:** incorporar en perfiles y skills la ubicación de migraciones, creación inicial, modificaciones, registro de aplicación y pruebas de evolución del esquema.
- **Brain de desarrollo:** documentación Markdown que puede abrirse como vault de Obsidian, sin duplicación de especificaciones.
- **KB operativa:** almacenamiento y recuperación de información para el agente del producto, con datos separados de las fuentes versionadas del proyecto y configuración por entorno.

La SF debe guiar la selección y documentar los límites; no imponer estas capacidades a todos los proyectos. Las estructuras concretas de carpetas son plantillas de la metodología, no motores ya implementados.

### Trabajo necesario

- Ampliar perfiles y plantillas de especificación con responsabilidades del agente, contratos, permisos, fallos y comprobaciones.
- Distinguir en distribución e instalación las skills de desarrollo de las skills operativas del producto y sus versiones; evitar que una actualización global cambie inadvertidamente el runtime.
- Definir cómo materializar y verificar la configuración efectiva de Claude Code: `agent-runtime/` solo organiza fuentes y no es un directorio de carga implícita.
- Evaluar skills especializadas para hooks, herramientas del agente, conocimiento/Obsidian y SQL/migraciones, sin dar por aprobada ninguna candidata.
- Preparar evaluación de recuperación y actualización de KB y comportamiento del agente, junto a pruebas deterministas de hooks y herramientas.
- Diseñar mantenimiento, permisos y conservación de la KB con la aplicación; no confundirlo con las tareas de automejora del método.

La SF mantiene su propio brain de desarrollo en su documentación si se adopta Obsidian. Esto no implica que la SF necesite una KB operativa para sí misma.

## 3. Reglas de colaboración y automejora

### Información suficiente antes de actuar — acuerdo

Cuando las instrucciones o el contexto sean insuficientes para definir o ejecutar correctamente un trabajo, Claude Code debe pedir toda la información adicional que necesite. Primero consultará la documentación y el contexto disponibles; después formulará preguntas concretas, agrupadas cuando ayude a responderlas.

No inventará requisitos ni convertirá supuestos importantes en decisiones. Si las respuestas son necesarias para avanzar en una parte, mantendrá esa parte pendiente hasta recibirlas. Puede continuar trabajo independiente ya autorizado. Esta regla no obliga a preguntar por detalles ya resueltos ni por elecciones rutinarias cubiertas por el método.

### Tarea permanente de automejora — acuerdo

La SF debe mantener siempre presente y activa una tarea denominada **Mejorar la Software Factory**. La tarea permanente y todas las tareas concretas de mejora continua se asociarán al proyecto **SoftwareFactory** del kanban. Es una línea continua de trabajo y no se marca como terminada al completar una mejora; cada propuesta concreta puede tener su propia tarea y cierre.

Esta regla es transversal: las skills e instrucciones distribuidas deben mantener la automejora presente también durante el desarrollo de proyectos consumidores. Aunque la observación surja en otra aplicación, su tarea de mejora de la SF pertenece a **SoftwareFactory**. Registrar proyecto de origen, devslice o tarea relacionada y evidencia; enlazar ambos contextos cuando corresponda. Las correcciones específicas de una aplicación conservan su tarea en esa aplicación; una mejora general derivada se registra como tarea vinculada en **SoftwareFactory**. Si no hay acceso al kanban, conservar la propuesta pendiente de traslado y confirmar su registro posteriormente.

Durante el trabajo y al revisar sus resultados, observar fricciones, instrucciones ambiguas, errores repetidos, pasos innecesarios y oportunidades de mejorar skills, plantillas, perfiles o herramientas. Basar las propuestas en evidencias y mantener este análisis proporcionado al trabajo principal.

Para cada mejora:

1. Registrar el problema observado y la evidencia.
2. Preparar una propuesta concreta con beneficio, alcance, impacto y forma de comprobarla.
3. Solicitar aprobación explícita del propietario antes de aplicar el cambio de automejora. La autorización general para trabajar en la SF no equivale a aprobar todas las mejoras futuras.
4. Una vez aprobada, implementar, verificar y registrar el resultado y su versión cuando corresponda.

Investigar y redactar propuestas no modifica el método vigente. No aplicar ni distribuir cambios de automejora sin aprobación. Los cambios expresamente solicitados por el propietario cuentan como autorizados dentro de su alcance.

Persistencia: mantener la tarea y sus propuestas concretas en el proyecto **SoftwareFactory** del kanban cuando esté accesible. Si el proyecto no existe, solicitar su creación o la información necesaria antes de registrar las tareas; no utilizar otro proyecto por defecto. Hasta disponer de acceso, usar [propuestas](../../propuestas.md) como soporte provisional. Al aprobarse, la decisión pasa a [decisiones](../../decisiones/README.md). Al iniciar o retomar trabajo en la SF, consultarlo y tener presente la tarea. No afirmar que se ha creado o actualizado una tarjeta si no se ha confirmado la operación.

La tarea es permanente durante el trabajo con la SF; no implica ejecución en segundo plano ni una automatización programada.

## 4. Próximos pasos y asuntos pendientes

El orden de construcción de la SF es una propuesta («Orden de construcción de la SF»). En la práctica lo marca el propietario sesión a sesión.

### Pendientes por resolver

- Aprobación de esta especificación completa.
- Mecanismo concreto para registrar y recuperar la tarea permanente de automejora en el kanban.

- Instalación de JKanban en la SF. JKanban está en su propio repositorio (`jumibot/JKanban`, FastAPI y SQLite sin ORM, rama de trabajo `develop`), en la carpeta de desarrollo `D:\Projectes\JKanban`. Ya tiene un MCP para la SF y flujos de estados (su `docs/mcp.md` y `docs/flows.md`). Desde el 2026-10-27 se desarrolla como proyecto bajo la SF (`.sf/`, plugin `sf`). Por decisión del propietario (2026-10-26), se instalará dentro de la carpeta de la SF; según el acuerdo de la sección 1, esa instalación será una copia operativa de una versión publicada, no la carpeta de desarrollo. La ubicación propuesta, sin confirmar, es `herramientas/jkanban/` para el código, como submódulo con una versión etiquetada, y `datos/jkanban/` para la base de datos, fuera de git.
- Tareas previas en el repositorio de JKanban, antes de instalarlo:
  1. Terminar el paso de la conexión antigua (`backend/infrastructure/database.py`, con la ruta de `tasks.db` fija en la raíz) a la nueva (`backend/infrastructure/persistence/sqlite/connection.py`, que lee `SQLITE_PATH`). Todos los repositorios deben usar la nueva, para que los datos puedan vivir fuera del código.
  2. Etiquetar una versión estable. Hoy solo existe `v0.0.0`.
- MCP de JKanban, construido a medida (decisión del propietario, 2026-10-26). De otros proyectos solo se toman ideas (Backlog.md, beads), según el [informe de recursos](../../referencias/reports/Recursos%20para%20la%20SoftwareFactory.md).
- Ubicación y contenido de la skill de visión existente.
- Control de versiones por proyecto, que Claude Code no documenta (sección 2, «Límites conocidos»).
- Reglas de aprobación, ejecución autónoma, integración y publicación.
- Límites de tiempo, rondas y consumo; tratamiento del estancamiento.
- Herramientas de pruebas, informes y conservación de evidencias.
- Selección definitiva de skills tras evaluación práctica.
- Mecanismo de ejecución y despliegue del agente operativo y separación de versiones respecto a la SF.
- Plantillas de brains, herramientas de acceso y gestión de KB operativa según proyecto.
- Ejecutor y estrategia de migraciones SQL para cada perfil.

## 5. Indicaciones para continuar en Claude Code

Leer primero la metodología enlazada y después esta especificación. Distinguir las preferencias confirmadas de las propuestas pendientes.

Mantener visión global, preparación antes de implementación, devslices verticales, SQL nativo, nombres descriptivos y complejidad proporcionada.

No sustituir la skill de visión existente sin estudiarla. No considerar las skills candidatas aprobadas ni instalar metodologías completas por defecto. No dar por construido o conectado el MCP del kanban.

Al comenzar, inspeccionar el proyecto disponible, consultar la tarea permanente de automejora y concretar el siguiente entregable. Pedir la información adicional necesaria conforme a las reglas de colaboración. Este documento transmite contexto; no constituye por sí mismo una orden de implementar todas sus propuestas.
