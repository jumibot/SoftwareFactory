# SoftwareFactory

Una fábrica de software personal sobre Claude Code. Reúne el método y las herramientas con los que una sola persona, el «hombre orquesta», lleva a término muchos proyectos a la vez. Esa persona cada día desarrolla, investiga, crea proyectos y visiones, enseña, aprende y se mantiene al día.

La SF no parte de cero: integra todo lo que ya existe y sirve, entero o en parte. Claude Code es su sistema nervioso central. Su objetivo no es producir más, sino pedir menos atención.

**Estado (2 de noviembre de 2026):** en desarrollo. La SF se distribuye como el plugin `sf`, cuya versión publicada es la del último tag `vX.Y.Z` (y la `version` de [`plugin.json`](plugins/sf/.claude-plugin/plugin.json) en `main`); JKanban tiene MCP, pero aún no está instalado en la SF; varias propuestas esperan aprobación.

Los documentos distinguen acuerdos, propuestas y pendientes.

Para leer este índice en local con el estilo de la SF, abre [README.html](README.html): sus enlaces llevan a las versiones html.

## Instalar

Requisitos: Claude Code, git, `gh` con la sesión iniciada (`gh auth login`) y Python 3.9 o posterior. Funciona en Windows, macOS y Linux.

Una sola vez por equipo:

```bash
claude plugin marketplace add jumibot/SoftwareFactory
claude plugin install sf@softwarefactory --scope user
```

Instalar `sf` trae solas sus tres dependencias (`gsap-skills`, `threejs-skills` y `oklch-skill`): no las instales a mano. Después:

1. **Comprueba la instalación.** Abre Claude Code y pídele: «Comprueba la instalación de la SF: el catálogo softwarefactory, el plugin sf@softwarefactory y sus dependencias, con `claude plugin list`, y arregla lo que falte con mi OK». Claude lo mira todo, te dice qué falta y lo arregla si le das el OK.
2. **Empieza.** Abre Claude Code en una carpeta vacía o en tu proyecto. Claude te preguntará si quieres incorporarlo a la SF; dile que sí. Pon la pantalla completa (`/tui fullscreen`) para ver el panel de la SF a la derecha.

Más detalle, en [el README del plugin](plugins/sf/README.md#instalación).

La SF tiene licencia MIT ([LICENSE](LICENSE)); lo que toma de terceros y sus licencias, en [`plugins/sf/LICENCIAS-DE-TERCEROS.md`](plugins/sf/LICENCIAS-DE-TERCEROS.md).

## Las visiones de la SF

Empieza por aquí. Cada visión cuenta la SF desde una perspectiva, a vista de pájaro, para no perder el rumbo.

- **[El método](docs/specs/vision/software-factory.md)**: cómo se pasa de la visión al código, devslice a devslice. ([html, en local](docs/specs/vision/software-factory.html)).
- **[El taller del hombre orquesta](docs/specs/vision/hombre-orquesta.md)**: para quién es la SF. Una persona, seis trabajos y muchos proyectos. Caso: una mañana con muchos frentes abiertos. ([html, en local](docs/specs/vision/hombre-orquesta.html)).

Previstas, sin escribir todavía: productos con un agente dentro; software y hardware, con el gemelo digital primero; y la fábrica que aprende.

Los enlaces abren el `.md`, que GitHub muestra formateado. Cada visión tiene también un `.html` con el estilo de la SF, para abrirlo en el navegador desde la copia local.

## Por dónde empezar

- **Si eres el propietario:** las [visiones](#las-visiones-de-la-sf) dan la imagen de conjunto. [Cómo funciona la Software Factory](docs/como-funciona-la-software-factory.md) describe los componentes de la SF, cómo se instala y cómo se mejora. Después, la metodología y la especificación.
- **Si eres Claude Code:** empieza por [CLAUDE.md](CLAUDE.md), que tiene las instrucciones de entrada y de colaboración.

## Documentos

Los enlaces abren los `.md`. Los `.html` se generan desde ellos con el estilo propio de la SF y se abren en el navegador desde la copia local, porque GitHub solo muestra su código.

### Visión

Las visiones están al principio de este README, en [Las visiones de la SF](#las-visiones-de-la-sf).

### Método y especificación

- [Cómo funciona la Software Factory](docs/como-funciona-la-software-factory.md): el mapa. Qué piezas tiene la SF, dónde está cada una, cómo llega a los proyectos y cómo se publica un cambio. ([html, en local](docs/como-funciona-la-software-factory.html)).
- [Metodología de desarrollo de proyectos](plugins/sf/skills/metodologia/references/desarrollo-de-proyectos.md): cómo se construyen las aplicaciones. Viaja en el plugin `sf` como skill `sf:metodologia`, así que cada proyecto lee la versión publicada. Cubre visión, especificaciones, interfaz, definición técnica, devslices, kanban, perfiles técnicos, estructura de código, pruebas e informes.
- [Especificación de la SF](docs/specs/funcional/software-factory.md): qué hay que construir para aplicar y distribuir el método. Cubre skills, plantillas, distribución, versiones, MCP, evaluación y próximos pasos.

La metodología es la referencia del proceso, y la especificación la usa. Si un cambio de la SF modifica el método, se actualizan los dos documentos.

### Decisiones y propuestas

- [Decisiones](docs/decisiones/README.md): lo que el propietario ha decidido sobre la SF, con su porqué y dónde se aplicó; una por archivo, con su índice generado.
- [Propuestas](docs/propuestas.md): las ideas de mejora aún sin decidir, con su origen y su evidencia. Es el registro de la tarea permanente «Mejorar la Software Factory». Ninguna propuesta se aplica sin aprobación explícita del propietario.

### Investigación

En `docs/referencias/`. Cada informe resume sus notas; las notas guardan el detalle y las fuentes.

**Fricciones humanas del desarrollo con IA** (26 de octubre de 2026): qué cuesta a una persona trabajar con agentes, qué dicen los estudios y los testimonios, y qué resuelven las herramientas actuales.
- [Informe](docs/referencias/reports/Fricciones%20humanas%20del%20desarrollo%20con%20IA.md) ([html, en local](docs/referencias/reports/Fricciones%20humanas%20del%20desarrollo%20con%20IA.html)). Lleva una fe de erratas: manda la verificación de citas.
- Notas:
  - [atención y estrés](docs/referencias/research_notes/Fricciones%20humanas%20del%20desarrollo%20con%20IA/atencion_y_estres.md)
  - [productividad y confianza](docs/referencias/research_notes/Fricciones%20humanas%20del%20desarrollo%20con%20IA/productividad_y_confianza.md)
  - [testimonios](docs/referencias/research_notes/Fricciones%20humanas%20del%20desarrollo%20con%20IA/testimonios.md)
  - [herramientas de orquestación](docs/referencias/research_notes/Fricciones%20humanas%20del%20desarrollo%20con%20IA/herramientas_orquestacion.md)
  - [Claude Code y métodos](docs/referencias/research_notes/Fricciones%20humanas%20del%20desarrollo%20con%20IA/claude_code_y_metodos.md)
  - [verificación de citas](docs/referencias/research_notes/Fricciones%20humanas%20del%20desarrollo%20con%20IA/verificacion_citas.md)

**Recursos para la SoftwareFactory** (26 de octubre de 2026): qué se puede integrar, entero o en parte, ordenado por necesidad de la SF.
- [Informe](docs/referencias/reports/Recursos%20para%20la%20SoftwareFactory.md) ([html, en local](docs/referencias/reports/Recursos%20para%20la%20SoftwareFactory.html))
- Notas:
  - [skills y plugins](docs/referencias/research_notes/Recursos%20para%20la%20SoftwareFactory/skills_y_plugins.md)
  - [métodos y flujos](docs/referencias/research_notes/Recursos%20para%20la%20SoftwareFactory/metodos_y_flujos.md)
  - [repositorios e integraciones](docs/referencias/research_notes/Recursos%20para%20la%20SoftwareFactory/repositorios_e_integraciones.md)
  - [problemas y testimonios](docs/referencias/research_notes/Recursos%20para%20la%20SoftwareFactory/problemas_y_testimonios.md)
  - [vibe design](docs/referencias/research_notes/Recursos%20para%20la%20SoftwareFactory/vibe_design.md)
  - [agentes y gemelos](docs/referencias/research_notes/Recursos%20para%20la%20SoftwareFactory/agentes_y_gemelos.md)

### Identidad visual

- [identidad.json](docs/identidad/identidad.json) y [tema-azul.json](docs/identidad/tema-azul.json): el tema y los datos de cabecera que usan las visiones y los informes en HTML.

## Skills

Todas las skills de la SF viven dentro del plugin `sf`, en [`plugins/sf/skills/`](plugins/sf/skills/). Su procedencia (qué se tomó, de dónde y qué se cambió) está en [`docs/referencias/procedencia/`](docs/referencias/procedencia/README.md); la atribución y las licencias de lo que es de terceros, en [`plugins/sf/LICENCIAS-DE-TERCEROS.md`](plugins/sf/LICENCIAS-DE-TERCEROS.md). El plugin se publica en GitHub y se instala para el usuario, así que las skills están en cualquier proyecto con el prefijo `sf:` (por ejemplo, `sf:documento_vision`). Ver [`plugins/sf/README.md`](plugins/sf/README.md).

**Propias**

| Skill | Para qué | Estado |
|---|---|---|
| [crear_documentos](plugins/sf/skills/crear_documentos/SKILL.md) | Lo común para crear cualquier documento: generador .md → HTML, catálogo de recursos, temas e identidad, herramientas de lectura, respaldo y comprobación | Nueva |
| [documento_vision](plugins/sf/skills/documento_vision/SKILL.md) | Documentos de visión, en conversación de cuatro fases, con HTML de estilo propio | Validada |
| [documento_fundacional](plugins/sf/skills/documento_fundacional/SKILL.md) | Documento fundacional: presentación formal del proyecto, sin historia, con evidencias, escenarios y fuentes; HTML editorial imprimible | Nueva, sin validar |
| [informe_deliberativa](plugins/sf/skills/informe_deliberativa/SKILL.md) | Informe de una tarea deliberativa: estructura fija, preguntas con opciones, recomendación y estado, y una versión con respaldo y HTML en cada vuelta | Nueva |
| [infografia_tecnica](plugins/sf/skills/infografia_tecnica/SKILL.md) | Infografías técnicas en 3D e interactivas de un producto o dispositivo | Validada |
| [diseno_interfaz](plugins/sf/skills/diseno_interfaz/SKILL.md) | Interfaz en detalle antes de la técnica: recorridos, pantallas, estados y criterios | Sin probar |
| [definicion_tecnica](plugins/sf/skills/definicion_tecnica/SKILL.md) | Definición técnica y arquitectura, con decisiones en formato MADR | Sin probar |

**Externas, de apoyo.** No viajan en el plugin: son dependencias de `sf` y se instalan con él (decisiones 175 y 176). Se invocan con el prefijo de su plugin.
- `oklch-skill`: color en OKLCH, paletas y contraste. Viene de [jakubkrehel/oklch-skill](https://github.com/jakubkrehel/oklch-skill), fijada al commit `0e81f04`. La usa `crear_documentos` para crear las series de colores de los temas; se invoca como `oklch-skill:oklch-skill`.
- `gsap-skills`: animación web, de las skills oficiales de GreenSock ([greensock/gsap-skills](https://github.com/greensock/gsap-skills)), fijada al commit `aed9cfd`. La usa `infografia_tecnica` con cinco de sus skills: core, timeline, plugins, utils y performance.
- `threejs-skills`: 3D en la web, de [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills), fijada al commit `0e18186`. La usa `infografia_tecnica` con diez de sus skills: fundamentals, geometry, materials, lighting, textures, animation, interaction, shaders, postprocessing y performance.

`crear_documentos` necesita además `dataviz` para validar las series de colores; no es un plugin y la trae el entorno. Si no está, la skill dice qué hacer.

## Estructura

```text
SoftwareFactory/
├── CLAUDE.md                 entrada para Claude Code
├── README.md                 este índice (y README.html, para leerlo en local)
├── docs/
│   ├── identidad/            tema visual de la SF
│   ├── specs/
│   │   ├── vision/           una visión por perspectiva (.md y .html)
│   │   └── funcional/        qué construir en la SF
│   ├── referencias/
│   │   ├── procedencia/      de dónde viene cada skill y herramienta del plugin
│   │   ├── reports/          informes de investigación
│   │   └── research_notes/   notas y fuentes de cada investigación
│   ├── como-funciona-la-software-factory.md  el mapa de la SF
│   ├── como-funciona-el-panel.md  el detalle del panel
│   ├── decisiones/           decisiones tomadas, una por archivo, con su índice
│   └── propuestas.md         propuestas de mejora sin decidir
├── plugins/sf/               el plugin de la SF: skills, kit de documentos, plantillas y mods, con las licencias de terceros
└── scripts/                  utilidades del repositorio
```

Las carpetas `_respaldo/` guardan versiones anteriores de documentos y skills antes de cambios grandes.

## Cómo se trabaja

- **Generar el HTML de una visión o de un informe:**

  ```bash
  python -I -X utf8 plugins/sf/skills/documento_vision/scripts/doc_to_html.py docs/specs/vision/hombre-orquesta.md
  python -I -X utf8 plugins/sf/skills/documento_vision/scripts/doc_to_html.py "docs/referencias/reports/<informe>.md" --tipo "Informe de investigación"
  ```

  El script encuentra solo la identidad de `docs/identidad/`. El `.html` no se edita a mano.
- **Regenerar README.html** cada vez que cambie el README:

  ```bash
  python -I -X utf8 scripts/readme_a_html.py
  ```
- **Cambios en la SF:** cada tarea, en su rama `feature/NN-nombre` desde `develop`; probada, entra en `develop` por squash y push. Publicar es pasar `develop` a `main` con el tag `vX.Y.Z` ([metodología, 2](plugins/sf/skills/metodologia/references/desarrollo-de-proyectos.md)).
- **Mejoras:** se registran en [propuestas](docs/propuestas.md) con su origen, aunque surjan en otro proyecto, y se aplican solo con aprobación del propietario. Al decidirse, pasan a [decisiones](docs/decisiones/README.md).
- **Información que falta:** se pide; no se inventan requisitos ni decisiones.

## Pendiente

Lo más inmediato:
- Aprobar o ajustar las propuestas de mejora del 26 de octubre.
- Decidir cómo se instala JKanban dentro de la SF y construir su MCP a medida.
- Migrar lo que dependa de claude.ai/design antes de que cierre, el 14 de diciembre de 2026.
- Probar `diseno_interfaz` y `definicion_tecnica` en un proyecto real.

El estado completo está en [propuestas](docs/propuestas.md), [decisiones](docs/decisiones/README.md) y la sección de próximos pasos de la [especificación](docs/specs/funcional/software-factory.md).
