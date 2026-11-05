# Arranque de Claude en la SF

Para Claude: lo único que se lee al empezar una sesión en la SF. Se mantiene al día con lo que haga falta para continuar el desarrollo de la SF: lo que se aprende o cambia en una sesión (piezas nuevas, dónde vive cada cosa, cómo se trabaja aquí) entra aquí. Añadir o cambiar algo pide la autorización del propietario: se propone el texto y se espera su OK (decisión 293). No repite reglas del plugin: las enlaza.

## Qué es este repositorio

- Es la fuente de la SF, no una instalación. Ningún proyecto usa esta carpeta: usan el plugin `sf` publicado e instalado desde el catálogo `softwarefactory` (jumibot/SoftwareFactory, público).
- Un cambio en la fuente no llega a ningún proyecto hasta que se publica y se actualiza la copia instalada. La copia instalada no se edita nunca.
- Se desarrolla en `develop`; cada tarea, en `feature/NN-nombre`, con squash a `develop` al cerrar (`sf:flujo_tareas`).
- Publicar: RELEASE del panel. Revisa lo que sale (datos privados, `.sf/publicable.txt`), sube la `version` de `plugins/sf/.claude-plugin/plugin.json`, pasa `develop` a `main` con el tag `vX.Y.Z` y hace push. ACTUALIZAR instala la versión publicada en el equipo.
- Ver un cambio sin publicar: modo prueba (etiqueta PRUEBA del panel o `/sf_prueba`), que activa `sf@softwarefactory-dev` (la copia de trabajo) y `/reload-plugins`. Solo en la SF.
- Comprobar el plugin: `python -I -X utf8 -m pytest plugins/sf/tests`, `claude plugin test plugins/sf` y `claude plugin validate plugins/sf`.
- En la SF el mod no entrega las reglas ni la orquestación: el principal carga `sf:orquestacion` (CLAUDE.md). No hay `.sf/proyecto.json`.

## Piezas del plugin (`plugins/sf/`)

| Pieza | Qué es |
| --- | --- |
| `skills/orquestacion/` | Reglas del agente principal: cada mensaje, cola, subagentes, prueba, cierre, preguntar, escribir. |
| `skills/flujo_tareas/` | Mecánica de la cola y de `cola.py`: estados, pasos, ramas, cierre, observación. `references/estados.md`, cada transición. |
| `skills/metodologia/` | El método. `references/desarrollo-de-proyectos.md` y la guía `references/diagramas-svg.md`. |
| `skills/incorporar_proyecto_a_sf/` | Incorporar, poner al día o diagnosticar un proyecto. Sin tarea. |
| `skills/configurar_proyecto/` | Cambiar `.sf/proyecto.json` de un proyecto (`/sf_config`). |
| `skills/comprobar_instalacion/` | Comprobar y arreglar la instalación del plugin y sus requisitos. |
| `skills/crear_documentos/` | Lo común de los documentos: generador .md → HTML, recursos, temas, respaldo. |
| `skills/documento_vision/`, `documento_fundacional/`, `informe_deliberativa/` | Un tipo de documento cada una, encima de `crear_documentos`. |
| `skills/diseno_interfaz/`, `definicion_tecnica/` | Fases de interfaz y de técnica del método. |
| `skills/infografia_tecnica/` | Infografías 3D con three.js. |
| `tools/cola.py` | Único escritor de la cola. Claude lo lanza siempre por `~/.claude/sf/cola.py` (lanzador `tools/cola_sesion.py`). |
| `tools/configuracion.py` | Ver, comprobar y detectar la configuración de un proyecto. Solo lee. |
| `tools/indice_decisiones.py` | Regenera el índice de decisiones. |
| `tools/revision_publica.py` | Revisión de datos privados antes de RELEASE y de subir `develop`. |
| `tools/plugin_sf.py`, `tools/incorporacion.py` | Versión del plugin al día; progreso de una incorporación para el panel. |
| `tools/kit_documentos/` | Barra y herramientas de los documentos HTML. |
| `hooks/` | El mod: panel `/sf` (`panel.tsx`), comandos `/sf_…` (`register.tsx`), cola y RELEASE (`cola.ts`), reglas entregadas (`contexto.ts`), avisos, subagentes, bloqueo de otros proyectos (`control.ts`), modo prueba (`prueba.ts`), Python detectado (`python.ts`), revisión (`revision.ts`). |
| `templates/claude-sf.md`, `claude-sf-metodologia.md` | Reglas que el mod entrega a los proyectos. |
| `templates/estructuras/`, `templates/propuestas.md` | Estructuras de código por perfil; propuestas vacías para la incorporación. |
| `tests/` | Pruebas de Python (`test_*.py`) y del panel (`panel.test.tsx`). |
| `.claude-plugin/plugin.json` | Versión y dependencias (gsap-skills, threejs-skills, oklch-skill). |

El catálogo es `.claude-plugin/marketplace.json`, en la raíz.

## Dónde vive cada cosa

| Qué | Dónde |
| --- | --- |
| Cola de la SF | `.sf/peticiones.json`, fuera de git; solo con `cola.py`. |
| Decisiones | `docs/decisiones/`, una por archivo; con `cola.py decision`. Aquí no van a `sf/`. |
| Propuestas | `docs/propuestas.md`. |
| Informes de deliberativas e investigación | `docs/referencias/reports/`. |
| Especificación de la SF | `docs/specs/funcional/software-factory.md`. |
| Visiones | `docs/specs/vision/`. |
| Índice para quien desarrolla la SF | `DESARROLLO.md`. |
| Presentación pública | `README.md` (inglés), `README.es.md` y la web de `site/` (GitHub Pages desde `main`). |
| Pantallazos de la web | `scripts/capturas_web.py` → `site/img/`. |
| Permitidos de la revisión | `.sf/publicable.txt`. |

## Cuándo abrir cada documento

| Documento | Léelo si… |
| --- | --- |
| [Cómo funciona la Software Factory](como-funciona-la-software-factory.md) | cambias una pieza, la publicación o lo que recibe la sesión de un proyecto. |
| [Cómo funciona el panel](como-funciona-el-panel.md) | tocas el panel o el mod. |
| [Cómo funcionan los estados](como-funcionan-los-estados.md) | tocas un cambio de estado de una tarea. |
| [Metodología](../plugins/sf/skills/metodologia/references/desarrollo-de-proyectos.md) | cambias el método o necesitas un acuerdo. |
| [Especificación de la SF](specs/funcional/software-factory.md) | decides qué construir en la SF. |
| [Mejora continua](mejora-continua-a-la-software-factory.md) | registras o aplicas una mejora o una decisión. |
| [Propuestas](propuestas.md) | el propietario pregunta por una idea sin decidir. |
| [Índice de decisiones](decisiones/README.md) | buscas el porqué de algo. |
| [Uso del panel](uso-del-panel.md) | revisas fricciones del panel. |
| [DESARROLLO.md](../DESARROLLO.md) | quieres el índice completo de la SF. |
