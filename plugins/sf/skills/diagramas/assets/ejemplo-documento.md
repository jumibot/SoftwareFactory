---
antetitulo: Software Factory · Ejemplo de la skill diagramas
lema: Seis diagramas generados // con todas las herramientas del documento.
subtitulo: Comprueba que los diagramas y las herramientas conviven: buscador, notas, lectura, fuentes, tablas, edición y la herramienta «diagramas».
version: 1
estado: Ejemplo
destino: usuario
herramientas: todas
pie: Cada diagrama se nombra en el .md (![](ejemplos/x.diagrama)) y documento_a_html.py lo dibuja con generar_diagrama.py.
---
# Diagramas de la SF

> **Cómo se hizo**
> Cada figura sale de un archivo de datos de assets/ejemplos con generar_diagrama.py --fragmento, pegada tal cual en el .md. La herramienta «Diagramas» cambia cómo se ven todas a la vez.

## Estados | El ciclo de una tarea {#estados-sec}

Una tarea pasa por cuatro fases: Pendientes, En curso, En observación y Cerradas. Claude la devuelve a Pendientes si su rama no tiene trabajo; Descartar y Eliminar la sacan del camino [[E1]](#src-E1 "Metodología de la SF"){: .ref}.

![](ejemplos/estados.diagrama)

## Proceso | Publicar con RELEASE {#proceso-sec}

RELEASE comprueba que todo está en orden, sube la versión, pasa develop a main con su tag y hace push. Si algo falla, no publica y dice qué falta.

![](ejemplos/proceso.diagrama)

## Arquitectura | De la fuente al proyecto {#arquitectura-sec}

El repositorio publica, el equipo instala el plugin y cola.py, y el proyecto guarda la cola que el panel lee.

![](ejemplos/arquitectura.diagrama)

## Piezas | Lo que lleva el plugin {#piezas-sec}

Comandos, mod de estado, herramientas, pruebas, plantillas y skills, y de qué dependen.

![](ejemplos/piezas.diagrama)

## Secuencia | De la petición al cierre {#secuencia-sec}

El propietario pide; el principal lleva la cola con cola.py y encarga el trabajo al subagente; el propietario da el OK y el principal cierra.

![](ejemplos/secuencia.diagrama)

## Fases | Las fases de la metodología {#fases-sec}

De la visión al cierre, con lo que deja cada fase: visión, especificación, definición técnica, devslices, preparación, desarrollo y cierre.

![](ejemplos/fases.diagrama)

## Fuentes | Fuentes {#fuentes}

::: fuentes
**Metodología de la Software Factory.** Tareas y cola, en la skill sf:metodologia.
{: #src-E1}
:::
