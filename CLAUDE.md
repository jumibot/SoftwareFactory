# Guía para trabajar en la Software Factory

Este proyecto construye y evoluciona la propia SF para Claude Code. Las aplicaciones consumidoras tendrán sus propias instrucciones; este archivo no es todavía su plantilla.

## Lectura de entrada

1. Leer [README.md](README.md).
2. Leer [Cómo funciona la Software Factory](docs/como-funciona-la-software-factory.md): el mapa de piezas, fuente frente a copia instalada y publicación. El detalle del panel, en [Cómo funciona el panel](docs/como-funciona-el-panel.md).
3. Leer la [metodología](plugins/sf/skills/metodologia/references/desarrollo-de-proyectos.md): referencia de cómo desarrollar aplicaciones. Viaja en el plugin `sf` como skill `sf:metodologia`.
4. Leer la [especificación de la SF](docs/specs/funcional/software-factory.md): referencia de qué construir para aplicar y distribuir el método.
5. Consultar las [propuestas](docs/propuestas.md) y las [decisiones](docs/decisiones/README.md) (cómo se gestionan, en [Mejora continua a la Software Factory](docs/mejora-continua-a-la-software-factory.md)) y, cuando esté disponible, la tarea correspondiente en el kanban.

## Reglas de trabajo

- El agente principal carga la skill `sf:orquestacion` al empezar la sesión y tras cada compactación del contexto, y la aplica en cada mensaje del propietario sin volver a cargarla: qué hacer con la petición, la cola, los subagentes, la prueba y el cierre, y cómo preguntar y escribir. Un subagente no la carga: sigue su encargo.
- Distinguir acuerdos, preferencias, propuestas y pendientes. La metodología y la especificación recogen acuerdos, preferencias y pendientes; las propuestas están aparte. No tratar los ejemplos como obligaciones aprobadas.
- Si falta información, consultar lo disponible y pedir toda la información adicional necesaria. No inventar requisitos ni asumir decisiones importantes. Continuar solo las partes independientes ya autorizadas.
- Mejora continua: en la SF, las mejoras son tareas y propuestas suyas, bajo la tarea permanente **Mejorar la Software Factory** del proyecto **SoftwareFactory** del kanban, cuando esté conectado. Desde otros proyectos no se registra nada en la SF: allí, lo que es de la SF se dice en una línea, y traerlo es cosa del propietario, en una sesión de la SF («Sin registro ni mejoras de la SF desde otros proyectos» y «Un proyecto solo anota propuestas suyas»; esta regla se distribuye con la SF). Registrar oportunidades y preparar propuestas concretas; pedir aprobación explícita antes de aplicar o distribuir cambios de automejora. Las instrucciones directas del propietario autorizan el cambio solicitado dentro de su alcance.
- Un proyecto por sesión: esta sesión modifica solo la SF. Leer otros proyectos para realimentar la SF, sí; cambiarlos, en una sesión abierta en ellos (metodología, «Qué pertenece a cada proyecto consumidor»). Esta regla se distribuye con la SF. La configuración global (`~/.claude`) no se toca sin que el propietario lo pida y lo confirme.
- Cola de peticiones: toda petición del propietario, y todo bug o error detectado, a `.sf/peticiones.json` en cuanto llega, aunque esté sin concretar: lo que falte va como pasos de su tarea. Se trabaja bajo una tarea en curso. La cola solo se escribe con el CLI `cola.py`, con su orden fija (`python -I -X utf8 "$HOME/.claude/sf/cola.py" <orden>`). Cómo se lleva en la conversación, en la skill `sf:orquestacion`; estados y órdenes, en `sf:flujo_tareas`.
- Tipos de tarea: siete en tres familias (código, deliberativas y documentales); el tipo decide cómo se maneja el repositorio (metodología, «Tareas y cola»).
- Ramas por tarea: se desarrolla en `develop`; cada tarea, en su rama `feature/NN-nombre`, que entra en `develop` por squash al cerrarla; publicar es pasar `develop` a `main` con el tag `vX.Y.Z` y la `version` subida solo entonces (metodología, «Ramas y subagentes»; detalle en `sf:flujo_tareas`).
- Orquestación con subagentes: el principal habla con el propietario y lleva la cola; toda tarea en curso tiene su subagente, que hace todo su trabajo (decisiones «Orquestación con un subagente vivo por tarea» y «Todo el trabajo de la tarea, a su subagente»). Las reglas, en `sf:orquestacion`.
- Reglas en los proyectos: allí, las reglas comunes (`plugins/sf/templates/claude-sf.md` y, con metodología, `claude-sf-metodologia.md`) y `sf:orquestacion` las entrega el mod al empezar la sesión, tras `/clear` y tras compactar, y su `CLAUDE.md` no lleva líneas de la SF. En la SF no: este archivo las dice desde la fuente.
- Si cambia una pieza de la SF o la forma de publicarla, actualizar [Cómo funciona la Software Factory](docs/como-funciona-la-software-factory.md); si es del panel, también [Cómo funciona el panel](docs/como-funciona-el-panel.md). Estos documentos, la metodología, la plantilla y este archivo se actualizan en su tarea «Actualizar <documento>» (los tres últimos, en una sola), de una en una y cada una con su subagente, como dice `sf:orquestacion` («Documentos compartidos»).
- Diagramas de los documentos: SVG inline, nunca ASCII ni mermaid, con la [guía de diagramas](plugins/sf/skills/metodologia/references/diagramas-svg.md) (metodología, «Estructura documental común»). Norma del propietario.
- Mantener coherentes ambos documentos: si cambia el método, actualizar su referencia y las partes de la SF afectadas. Evitar duplicar reglas extensas aquí.
- Registrar cada decisión del propietario en cuanto se tome: en su propio archivo de [decisiones](docs/decisiones/README.md), con su porqué, con `cola.py decision`, que da el número, rehace el índice y hace el commit en `develop` sin cambiar la rama activa; aplicarla a la metodología o a la especificación, como acuerdo con fecha, es trabajo de su tarea. Lo que no está decidido va a [propuestas](docs/propuestas.md); las plantillas, al plugin (`plugins/sf/templates/`); los ejemplos solo ilustran.
- Este repositorio es la fuente de la SF, no una instalación operativa: ningún proyecto usa su copia de trabajo, sino lo publicado e instalado (especificación, «El proyecto central de la SF»).
- Respetar visión global, preparación de devslices y tareas antes del desarrollo, preferencia por backend primero, pruebas anticipadas cuando sea viable, SQL nativo y nombres descriptivos.
- Distinguir Claude Code para desarrollar de Claude Code como componente operativo del backend. Mantener separados sus instrucciones, skills, hooks y configuración; las carpetas propuestas no implican carga automática.
- Separar brain de desarrollo (`docs/`) y KB operativa del agente. Configurar explícitamente el acceso y conservar los datos operativos con sus políticas propias.
- Guardar scripts de creación y modificación SQL en las migraciones de persistencia, versionados junto al código.
- Usar complejidad proporcionada y crear carpetas cuando tengan contenido.
- Comandos antes que inferencia: lo que se pueda hacer con un comando, sin pasar por Claude (metodología, «Principios acordados»). Las herramientas que sirvan a otros proyectos van al plugin, versionadas y sin nada de ningún proyecto.
- La skill de visión y el kanban ya existen: pedir su ubicación si no está disponible. No sustituir la skill sin estudiarla ni afirmar que el MCP está conectado.
- Skills externas: las que la SF usa tal cual son dependencias del plugin, fijadas a su commit; una adaptada viaja en el plugin como propia, con su origen y lo que cambia («Skills externas: tal cual, como dependencias; adaptadas, como propias» y «Todas las skills externas actuales, como dependencias»). Las de la propuesta «Skills externas candidatas» (P18) no tienen validación práctica: no instalarlas ni adoptar una metodología completa como consecuencia de leer su listado.
- En los documentos de la SF, el propietario se nombra «propietario de la Software Factory»; las marcas «(norma del propietario, fecha)» no cambian.
- Al cerrar trabajo, indicar cambios, comprobaciones y pendientes reales. No afirmar operaciones de kanban o verificaciones sin confirmación.

El siguiente entregable se concreta con las instrucciones del propietario y el contexto disponible. Leer estos archivos no autoriza implementar todas las propuestas ni programar actividad en segundo plano.
