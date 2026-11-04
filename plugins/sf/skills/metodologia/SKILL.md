---
name: metodologia
user-invocable: false
description: "Método de la Software Factory (SF) para desarrollar proyectos con Claude Code: fases (visión, especificación e interfaz, definición técnica, planificación por devslices, preparación, desarrollo y verificación, cierre), kanban, estructura documental, estado del proyecto en .sf/, documentos de la SF en sf/ (propuestas, decisiones una por archivo, informes), tipos de tarea, perfiles y estructuras de código, pruebas, informes y automejora. Úsala al empezar o retomar un proyecto bajo la SF (tiene .sf/proyecto.json), al cambiar de fase o de devslice, al planificar o preparar devslices, al incorporar un proyecto existente a la SF, o cuando haya que saber cómo se hace algo según la SF."
---

# Metodología de la Software Factory

El método completo está en [references/desarrollo-de-proyectos.md](references/desarrollo-de-proyectos.md). Esta skill dice cuándo leer cada parte; las reglas están en el documento, no aquí.

Un proyecto está **bajo la SF** cuando tiene `.sf/proyecto.json` («Qué pertenece a cada proyecto consumidor»). En un proyecto sin ese archivo, no aplicar el método salvo que el propietario lo pida; si lo pide, incorporarlo con la skill `incorporar_proyecto_a_sf`.

## Qué leer en cada momento

| Momento | Dónde |
| --- | --- |
| Primera vez en la sesión con un proyecto bajo la SF | «Cómo interpretar este documento», «Principios acordados» y «Qué pertenece a cada proyecto consumidor». Después, el apartado de la fase que marca `.sf/estado.json`. |
| Incorporar un proyecto, nuevo o que ya existía, o ponerlo al día con la SF | Skill `incorporar_proyecto_a_sf`, con «Incorporación» y «Estructura documental común». |
| Cambiar la configuración del proyecto | Skill `configurar_proyecto` (`/sf_config`). |
| Llevar la conversación, la cola y los subagentes | Skills `sf:orquestacion` (el agente principal) y `sf:flujo_tareas` (la mecánica de la cola), con «Tareas y cola» y «Ramas y subagentes». |
| Visión y documento fundacional | «Documento de visión», con las skills `documento_vision` y `documento_fundacional`. |
| Especificación funcional e interfaz | «Especificación funcional global y diseño de interfaz», con la skill `diseno_interfaz`. |
| Definición técnica y arquitectura | «Definición técnica y arquitectura global», «Preferencias técnicas» y «Estructuras de código», con la skill `definicion_tecnica`. Las estructuras de carpetas están en `../../templates/estructuras/`. |
| Planificar el catálogo de devslices | «Planificación por devslices» y «Seguimiento en el kanban». |
| Preparar una devslice | «Preparación de cada devslice», «Seguimiento en el kanban» y «Pruebas y criterios de aceptación». |
| Desarrollar y verificar | «Desarrollo y verificación», «Pruebas y criterios de aceptación» y «Resultados: carpeta reports». |
| Cerrar una devslice | «Cierre» y «Resultados: carpeta reports». |
| Dónde guardar un documento, una propuesta o una decisión | «Estructura documental común». |
| Escribir o generar un documento | «Estructura documental común», con la skill `crear_documentos` y la del tipo de documento (`documento_vision`, `documento_fundacional`, `informe_deliberativa`). |
| Informe de una tarea deliberativa | Skill `informe_deliberativa`, con «Tareas y cola». |
| Dibujar un diagrama en cualquier documento | «Estructura documental común» y [references/diagramas-svg.md](references/diagramas-svg.md). |
| Persistencia SQL, agente del producto, brain o KB | De «Claude Code como componente del backend» a «Perfil: escritorio Python con MVP y agente Claude Code». |
| Algo de la SF no encaja, falta o se repite | «Automejora durante el uso de la SF». |

## Reglas que se aplican siempre

- **Estado.** Con metodología, al cambiar de fase o de devslice, actualizar `.sf/estado.json` («Estructura documental común»).
- **Decisiones.** Cada decisión del propietario se registra en cuanto se toma, en su propio archivo de `sf/decisiones/`, con su porqué, con `cola.py decision`: da el número, rehace el índice y hace el commit en `develop` («Estructura documental común»).
- **Diagramas en SVG.** Todo diagrama de un documento va como SVG inline en el `.md`, nunca en ASCII ni en mermaid, con las recomendaciones de [references/diagramas-svg.md](references/diagramas-svg.md). Los árboles de carpetas siguen en texto.
- **Un proyecto por sesión.** La sesión modifica solo el proyecto de su carpeta; leer otros, sí. Ningún proyecto escribe en la SF. El mod bloquea las escrituras de archivos en otro proyecto.
- **Cola y tareas.** Cada petición del propietario va a la cola en cuanto llega, aunque esté sin concretar, y se trabaja bajo una tarea en curso. La cola solo se escribe con `cola.py`. Cómo se lleva, en `sf:orquestacion`; sus estados y órdenes, en `sf:flujo_tareas`; los acuerdos, en «Tareas y cola».
- **Guías de cada proyecto.** Con metodología, instalación desde cero (`docs/guias/instalacion.md`) y actualización (`docs/guias/actualizacion.md`), obligatorias. Opcionales junto a la visión: visiones desde otras perspectivas, infografías técnicas y «Cómo funciona».
- **Forma de los documentos** («Estructura documental común»): texto literal y «componentes», no «elementos»; tablas de tres columnas como máximo, si no, tarjetas; índices y preguntas frecuentes en estilo FAQ, sin rótulos obvios; ninguna sección empieza por un diagrama (introducción breve, diagrama y prosa); prosa para explicar y listas numeradas solo para procedimientos; color con significado fijo, sin fondos; cada bloque de código con su lenguaje; sin referencias por número que no se vean en pantalla.
- **Lo que no está decidido no se decide solo.** Si falta información, se pregunta; no se inventan requisitos.
- **Automejora.** Si el método o una skill de la SF fallan, sobran o faltan, no se anota en el proyecto, ni en su cola ni en sus propuestas: se dice en una línea que es de la SF, y llevarlo a la SF es cosa del propietario, en una sesión de la SF («Un proyecto solo anota propuestas suyas»). En la propia SF es del proyecto. No se cambia la SF sin su aprobación.
- **Versión.** Este documento es la versión publicada con el plugin. La fuente se edita solo en el repositorio de la SF, nunca en la copia instalada.
