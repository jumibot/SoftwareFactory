---
antetitulo: Software Factory · Informe de análisis · Noviembre 2026
lema: Que la cola no haga esperar al propietario; // menos idas y vueltas, no un agente más.
subtitulo: El principal hace esperar al propietario mientras lleva la cola. Cuánto espera de verdad, qué ganaría un subagente de la cola en segundo plano, qué ganan las órdenes compuestas y lo que decidió el propietario.
version: Versión 3.1 · 04/11/2026
estado: Decidido · Tarea 358
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de análisis
pie: Informe de la tarea «Liberar antes al agente principal: deliberar qué delegar en agentes del plugin y qué en órdenes de cola.py» (358). Parte de sf:orquestacion, sf:flujo_tareas, cola.py y los avisos del mod en develop, de las cinco últimas sesiones largas del principal en la SF y de la documentación oficial de Claude Code. Decidido por el propietario de la Software Factory (decisiones 283 y 284). Las versiones anteriores, más amplias, están en _respaldo/.
---
# Que la cola no frene al principal: subagente de la cola u órdenes compuestas

## Resumen | El freno, la pregunta y la respuesta | Resumen {#resumen}

El principal hace esperar al propietario mientras lleva la cola. Antes de contestar, consulta la cola, anota la petición, añade pasos, marca los hechos, registra informes y deja tareas listas, cada cosa con su llamada. Mientras tanto, el propietario espera su respuesta, o la conversación se corta para que el principal acabe esas operaciones. Es el freno que hoy se nota.

> **La pregunta que se delibera**
> ¿Conviene un subagente de la cola, vivo toda la sesión y en segundo plano, al que el principal encargue las operaciones de la cola para contestar al propietario sin esperar? ¿O bastan las órdenes compuestas ya decididas, o las dos cosas?

La respuesta del análisis es que no conviene el subagente. Cada operación le cuesta al principal unos 5 s, pero solo 1,4 son de `cola.py`: el resto es su propio turno de modelo, y encargar la operación a otro agente también es un turno, el de escribirle. Delegar ahorra, como mucho, esos 1,4 s por operación, y a cambio trae fallos que nadie ve, operaciones fuera de orden y un contexto más que pagar. Lo que sí quita espera es hacer menos llamadas: las órdenes compuestas ya decididas, varios pasos en una orden, la cola ya en el contexto del principal y contestar antes de anotar.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 420" width="100%" role="img" aria-label="Un turno de ejemplo, a unos 5 segundos por llamada. Hoy: lista, crear y tres pasos, y contesta a los 25 segundos. Con un subagente de la cola: lista, crear y el mensaje al subagente, y contesta a los 15 segundos; después el subagente anota los tres pasos y su aviso vuelve al principal. Con una orden con sus pasos y la cola ya en el contexto: una llamada y contesta a los 5 segundos." style="font-family:var(--fuente-texto);display:block">
<g font-size="15">
<text x="10" y="24" font-size="18" font-weight="700" style="fill:var(--oscuro)">Hoy</text>
<rect x="10" y="36" width="86" height="36" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="53" y="59" text-anchor="middle" style="fill:var(--texto)">lista</text>
<rect x="100" y="36" width="86" height="36" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="143" y="59" text-anchor="middle" style="fill:var(--texto)">crear</text>
<rect x="190" y="36" width="86" height="36" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="233" y="59" text-anchor="middle" style="fill:var(--texto)">paso</text>
<rect x="280" y="36" width="86" height="36" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="323" y="59" text-anchor="middle" style="fill:var(--texto)">paso</text>
<rect x="370" y="36" width="86" height="36" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="413" y="59" text-anchor="middle" style="fill:var(--texto)">paso</text>
<line x1="462" y1="30" x2="462" y2="80" style="stroke:var(--oscuro)" stroke-width="3"/>
<text x="462" y="100" text-anchor="end" font-weight="700" style="fill:var(--oscuro)">contesta a los ≈ 25 s</text>
<text x="10" y="136" font-size="18" font-weight="700" style="fill:var(--texto-suave)">Con un subagente de la cola</text>
<rect x="10" y="148" width="86" height="36" rx="6" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.5" stroke-dasharray="6 4"/><text x="53" y="171" text-anchor="middle" style="fill:var(--texto)">lista</text>
<rect x="100" y="148" width="86" height="36" rx="6" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.5" stroke-dasharray="6 4"/><text x="143" y="171" text-anchor="middle" style="fill:var(--texto)">crear</text>
<rect x="190" y="148" width="86" height="36" rx="6" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.5" stroke-dasharray="6 4"/><text x="233" y="171" text-anchor="middle" style="fill:var(--texto)">mensaje</text>
<line x1="282" y1="142" x2="282" y2="192" style="stroke:var(--oscuro)" stroke-width="3"/>
<text x="282" y="212" text-anchor="end" font-weight="700" style="fill:var(--oscuro)">contesta a los ≈ 15 s</text>
<rect x="190" y="226" width="360" height="36" rx="6" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.5" stroke-dasharray="2 4"/><text x="202" y="249" style="fill:var(--texto-suave)">después: el subagente anota los 3 pasos</text>
<text x="202" y="284" style="fill:var(--texto-suave)">y su aviso vuelve al principal, otro turno</text>
<text x="10" y="330" font-size="18" font-weight="700" style="fill:var(--texto-suave)">Una orden con sus pasos, cola en el contexto</text>
<rect x="10" y="342" width="86" height="36" rx="6" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.5" stroke-dasharray="6 4"/><text x="53" y="365" text-anchor="middle" style="fill:var(--texto)">crear</text>
<line x1="102" y1="336" x2="102" y2="386" style="stroke:var(--oscuro)" stroke-width="3"/>
<text x="10" y="406" font-weight="700" style="fill:var(--oscuro)">contesta a los ≈ 5 s</text>
</g>
</svg>
<figcaption>Un turno de ejemplo (anotar una petición con tres pasos), a unos 5 s por llamada. Lo que gana el subagente es juntar los tres pasos en un mensaje, que una orden con sus pasos junta igual sin él; y deja trabajo y un aviso para después.</figcaption>
</figure>

El propietario lo decidió así: sin subagente de la cola; órdenes compuestas, varios pasos en una orden, la cola en el contexto del principal y contestar primero («Sin subagente de la cola: órdenes compuestas, la cola en el contexto y contestar primero», decisión 284). No queda ninguna pregunta abierta.

[Ver lo decidido](#decidido){: .salto} [Ver la medición](#medicion){: .salto}

## Medición | Cuánto espera el propietario por la cola | Medición {#medicion}

La cola se lleva la mitad de las llamadas del principal, pero solo una cuarta parte de ese tiempo es de operaciones cuyo resultado no necesita para contestar. Se midieron las cinco últimas sesiones largas del principal en la SF, sin las de los subagentes, y se clasificó cada llamada a `cola.py` según si el principal necesita su resultado al momento.

::: columnas

**51 %**  de las llamadas
{: .metrica}

Son a `cola.py`: 1.126 de 2.209. Llevan unos 65 min en esas sesiones, contando el turno del modelo de cada una.

|||

**1,4 de 5 s**  por llamada
{: .metrica}

Es lo que tarda `cola.py`. El resto, 3,7 s de mediana, es el turno del modelo entre una llamada y la siguiente.

|||

**16 min**  sin necesidad de esperar
{: .metrica}

Es lo que llevan las operaciones cuyo resultado no hace falta para contestar (173 llamadas), un 25 % del tiempo de la cola.

:::

### Qué necesita el principal al momento

Para contestar, el principal necesita el resultado de casi todo lo que no sea anotar: el número de la tarea nueva, un choque, un rechazo, la cola que consulta o el encargo que va a pasar. Lo demás lo apunta para que conste, y no cambia lo que dice al propietario.

| Clase | Órdenes | Llamadas | Tiempo |
| --- | --- | --- | --- |
| Necesita el resultado al momento | `lista` y `ver` (121, 9 min); `crear` (48, 5 min); `choques`, `en-curso`, `rama`, `subagente`, `encargo`; `probar`, `cerrar`, `decision`, `fusionar`, `descartar`… | 347 | 46 min |
| No lo necesita | `paso añadir` (120, 11 min); `paso marcar` (44, 3 min); `informe`, `listo`, `comprobado`, `renombrar` | 173 | 16 min |
| Las dos en una llamada | cadenas que mezclan ambas | 23 | 3 min |

Las que no necesitan el resultado aparecen en 165 turnos, con una mediana de una llamada y 5 s por turno. Es decir: en el turno típico donde se podrían delegar, se delegaría una sola llamada.

> **Método**
> El tiempo de cada llamada va desde el evento anterior hasta su resultado: incluye el turno del modelo y la orden. Son cifras para comparar opciones, no un presupuesto.

## Subagente | Qué ganaría un subagente de la cola | Subagente {#subagente}

Un subagente de la cola, lanzado al empezar la sesión y vivo hasta el final, recibiría por `SendMessage` las operaciones que no necesitan respuesta; el principal las encargaría y contestaría sin esperar a que se hicieran. Lo que ahorra es menos de lo que parece, porque encargar también cuesta un turno.

### Lo que ahorra

Hoy, cada operación que no necesita respuesta cuesta un turno del principal (≈ 3,7 s) más `cola.py` (1,4 s). Con el subagente, cuesta un turno del principal para escribir el mensaje, que puede ser algo más largo que la orden. El ahorro por operación es la ejecución de `cola.py`, 1,4 s, y solo si el mensaje junta varias operaciones gana algo más; pero juntarlas en una sola llamada a `cola.py` da lo mismo sin subagente. En las cinco sesiones, el ahorro máximo serían unos 4 min (173 × 1,4 s), repartidos en 165 turnos: alrededor de un segundo por turno.

::: tarjetas 2 plegables

### No lee el mensaje mientras trabaja {icono=dialogo}

Un subagente que ya está trabajando no recibe el mensaje hasta su siguiente ronda; la documentación solo describe `SendMessage` para reanudar a uno parado. Con varias operaciones seguidas, se acumulan y llegan juntas.

### Fallos que nadie ve {icono=aviso}

Si una orden falla (2,7 % de las de la cola en las sesiones medidas), el subagente lo devuelve en su aviso, que llega como un turno nuevo del principal. Si el principal no lo atiende, la cola queda distinta de lo que cree, y el panel lo enseña al propietario antes que a él.

### Orden de las operaciones {icono=rama}

El principal sigue haciendo las que necesitan respuesta. Si cierra una tarea mientras el subagente aún no ha marcado sus pasos, `cerrar` se niega por pasos pendientes. El bloqueo de la cola evita que se rompa, no que las órdenes lleguen en mal orden.

### Coste en tokens {icono=documento}

Su contexto crece con cada salida de `cola.py` y se compacta. Su caché es suya y dura 5 min: tras una pausa, vuelve a pagar su contexto entero. Cada aviso de vuelta es, además, un turno más del principal.

### La regla de quién escribe la cola {icono=check}

«El mod impide que un subagente escriba la cola» (decisión 110) bloquea la escritura directa de `.sf/peticiones.json`, no `cola.py`, pero la regla escrita (`sf:flujo_tareas`) dice que solo el principal la escribe. Habría que hacer una excepción para el agente de la cola y anotarlo como autor en el historial (`--quien`), para que se sepa quién hizo cada cambio.

### Si muere {icono=lupa}

No está documentado qué pasa con un subagente tras `/clear` o al cerrar la sesión. Habría que relanzarlo y que el mod avisara de su falta, como ya hace con los de las tareas.

:::

### Lo descartado: un orquestador completo

Un orquestador completo, que llevara también los subagentes de las tareas, no quita espera: el que habla con el propietario sigue siendo el principal, y un subagente no puede preguntarle (`AskUserQuestion` se quita a todo subagente). Todo lo que decidiera pasaría dos veces.

## Órdenes | Lo que sí quita espera: menos llamadas | Órdenes {#ordenes}

Quitar llamadas quita espera entera: el turno del modelo y la orden. Las órdenes compuestas ya decididas atacan el principio y el final de cada tarea; quedan tres huecos que se cubren sin ningún agente.

::: tarjetas 2 plegables

### Poner en curso y recoger, una orden cada uno {icono=codigo} {: #o-283}

Decidido («Poner en curso y recoger una tarea con una sola orden», decisión 283; tarea 360). `en-curso N` deja hechos rama, worktree, rama auxiliar y la anotación del subagente; `recoger N` trae el trabajo, anota el informe, marca los pasos y deja la tarea lista, con la orden escrita por el subagente.

Quita
:   De 4-7 llamadas a 1 al abrir, y de 3-6 a 1 al recoger: los informes, pasos marcados y listos de la recogida, unos 6 min de los 16 que no necesitan respuesta.

### Varios pasos en una orden {icono=check} {: #o-pasos}

`paso añadir N "a" "b" "c"` y `crear … --paso "a" --paso "b"`: los pasos de una tarea nueva, de una vez.

Quita
:   `paso añadir` es la operación más repetida (120 llamadas, 11 min): casi todo lo que queda sin necesidad de respuesta.

### La cola, ya en el contexto {icono=lupa} {: #o-contexto}

El mod añade en cada mensaje del propietario un resumen de las tareas en curso y de lo que cambió desde el mensaje anterior (también desde el panel), como ya añade sus avisos.

Quita
:   Buena parte de `lista` y `ver` (121 llamadas, 9 min), que son de las que necesitan respuesta y ningún subagente puede quitar.

### Contestar primero, anotar después {icono=dialogo} {: #o-orden}

Una regla de la orquestación: en un turno, lo que no necesita respuesta va después de contestar al propietario.

Quita
:   La espera de esas operaciones, sin cambiar ninguna pieza: el propietario lee la respuesta mientras el principal termina de anotar.

:::

Juntas, estas piezas quitan casi todo el tiempo de la cola que el subagente podría quitar, y además parte del que no puede quitar. Por eso el subagente no se complementa con ellas: llega tarde a un hueco que ya está cubierto.

## Decidido | Lo que ya fija esta tarea | Decidido {#decidido}

| Nº | Decisión | Qué fija aquí |
| --- | --- | --- |
| 283 | Poner en curso y recoger una tarea con una sola orden | `en-curso N` lo hace todo, sin orden nueva; `recoger N` trae el trabajo, anota el informe, marca los pasos y deja la tarea lista, y el subagente deja la orden escrita al final de su informe. Se aplica en la tarea 360. |
| 284 | Sin subagente de la cola: órdenes compuestas, la cola en el contexto y contestar primero | Sin subagente de la cola ([pregunta 1](#p1)). Varios pasos en una orden, como paso de la 360 ([pregunta 2](#p2)). La cola en el contexto del principal, y lo demás que mejore su contexto de entrada, que es barato, en la tarea 361 ([pregunta 3](#p3)). Contestar primero y anotar después, en `sf:orquestacion` ([pregunta 4](#p4)). |

## Preguntas | Las preguntas y lo que se eligió | Preguntas {#por-decidir}

Las cuatro, decididas con la opción recomendada (decisión 284).

::: preguntas 2 plegables

### 1 · Un subagente de la cola en segundo plano {estado=decidida elegida=B recomendada=B icono=dialogo} {: #p1}

Las órdenes compuestas (283) ya están decididas; falta saber si además conviene el subagente.

Opción A
:   Un subagente de la cola, vivo toda la sesión, para las operaciones que no necesitan respuesta; el principal contesta sin esperarlas.

Opción B
:   Solo órdenes: las compuestas (283) y las tres piezas que las completan (preguntas 2, 3 y 4).

Opción C
:   Las dos: las órdenes, y probar el subagente en una tarea aparte para medir si quita espera.

Recomendación
:   **B.** Encargar una operación cuesta el mismo turno que hacerla; el subagente ahorraría alrededor de un segundo por turno y traería fallos que nadie ve y operaciones fuera de orden.

Decisión
:   **B.** Solo órdenes, sin subagente de la cola. Decisión 284.

### 2 · Varios pasos en una orden {estado=decidida elegida=A recomendada=A icono=check} {: #p2}

`paso añadir` es la operación más repetida del principal.

Opción A
:   `paso añadir N "a" "b" …` y `crear … --paso "a" --paso "b"`.

Opción B
:   Como hoy, un paso por orden.

Recomendación
:   **A.** Es poco código y quita la mayor parte de lo que no necesita respuesta.

Decisión
:   **A.** Como paso de la tarea 360. Decisión 284.

### 3 · La cola en el contexto del principal {estado=decidida elegida=A recomendada=A icono=lupa} {: #p3}

El principal consulta la cola antes de actuar porque el propietario la cambia desde el panel.

Opción A
:   El mod añade a cada mensaje las tareas en curso y lo que cambió desde el mensaje anterior.

Opción B
:   Como hoy: `lista` y `ver` cuando hace falta.

Recomendación
:   **A.** Quita consultas que ningún agente puede quitar; con solo lo que cambia, el texto añadido es corto.

Decisión
:   **A,** y más: el contexto de entrada es barato, así que la tarea 361 valora también qué otras cosas conviene poner en él. Decisión 284.

### 4 · Contestar primero, anotar después {estado=decidida elegida=A recomendada=A icono=dialogo} {: #p4}

Hoy el principal anota cuando le viene en el turno, a veces antes de contestar.

Opción A
:   Regla en `sf:orquestacion`: lo que no necesita respuesta, después de contestar.

Opción B
:   Como hoy.

Recomendación
:   **A.** No cuesta nada y quita la espera de lo que queda por anotar.

Decisión
:   **A.** Como paso de la tarea que actualiza las reglas del método (`sf:orquestacion`). Decisión 284.

:::

## Tareas | Las tareas que salen | Tareas {#tareas}

No sale ningún agente: salen órdenes, la cola en el contexto y una regla.

| Tarea | Tipo | Qué hace |
| --- | --- | --- |
| Poner en curso y recoger una tarea con una sola orden (360) | implementar | `en-curso N` completo y `recoger N` (decisión 283), con un paso nuevo: varios pasos en una orden ([pregunta 2](#p2)). |
| Que el principal tenga la cola en su contexto (361) | implementar | El mod añade a cada mensaje las tareas en curso y los cambios, y se valora qué más conviene poner en el contexto de entrada ([pregunta 3](#p3)); `sf:orquestacion` deja de pedir `lista` antes de actuar. |
| Actualizar la metodología, la plantilla y el CLAUDE.md | documentar | Con el paso de contestar primero y anotar después en `sf:orquestacion` ([pregunta 4](#p4)). |

Los agentes del plugin por familia de tarea quedan fuera de esta tarea: en «Agentes especializados, uno por familia de tarea» (304), con la decisión 282.

## Anexo | Texto propuesto para los documentos compartidos | Anexo {#anexo}

Para la tarea «Actualizar la metodología, la plantilla y el CLAUDE.md», una vez hecha la 360.

#### Metodología («Ramas y subagentes»)

> `cola.py en-curso N` pone la tarea en curso con su rama, su worktree y su rama auxiliar, y la deja lista para lanzar su subagente; `cola.py recoger N`, con la orden que deja el subagente al final de su informe, trae su trabajo, anota el informe y marca los pasos.

#### `sf:orquestacion` (pregunta 4)

> En un turno, lo que no necesita respuesta (añadir o marcar pasos, informes, listos) va después de contestar al propietario.

::: fuentes

**Sub-agents.** Claude Code Docs, consultado el 04/11/2026. code.claude.com/docs/en/sub-agents
{: #src-E1}

**Prompt caching.** Claude Code Docs, consultado el 04/11/2026. code.claude.com/docs/en/prompt-caching
{: #src-E2}

:::
