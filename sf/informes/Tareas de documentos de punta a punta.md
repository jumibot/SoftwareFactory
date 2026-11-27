---
antetitulo: Software Factory · Informe de análisis · Noviembre 2026
lema: Una orden por vuelta; // el documento, su respaldo y su HTML, juntos en develop.
subtitulo: Cómo se lleva una tarea de documentos de punta a punta — qué toca, cómo llega cada vuelta a develop con su respaldo y su HTML, cuándo se abre — y qué pasa con las «Actualizar…», la revisión y el diálogo.
version: Versión 2.0 · 27/11/2026
estado: Decidido · Tarea 303
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de análisis
pie: Informe de la tarea «Llevar las tareas de documentos de punta a punta: qué tocan, respaldo y HTML al día y abierto en cada vuelta» (303), que absorbió la 297. Parte de las preguntas del informe «Tipos de tarea» (274) y de las decisiones 147, 216, 217, 219, 220, 278, 344, 346, 369 y 377. Decidido por el propietario de la Software Factory: decisiones 393, 394 y 395.
---
# Tareas de documentos de punta a punta

## Resumen | Una sola orden para cada vuelta | Resumen {#resumen}

La orden que se propuso y se ha decidido es que cada vuelta de un documento la lleve a `develop` una sola orden, `cola.py documento N RUTA`. La orden respalda en `_respaldo/` la versión que hay en `develop`, regenera el HTML, hace el commit en `develop` sin cambiar de rama y abre el HTML si la tarea es el foco. Al usarla, la tarea declara su documento, y solo ese documento entra en `develop`. La implementa la tarea «Llevar cada vuelta de un documento a develop con una orden: respaldo, HTML, commit y apertura» (469).

Las piezas ya existen y se usan a mano: `respaldar.py`, el generador único y `commit_en_develop`, con la que `cola.py decision` ya escribe en `develop` sin cambiar de rama. Faltaba juntarlas, y se nota. 11 de los 25 HTML de `sf/informes/` y `docs/` no corresponden a su `.md`, y seis informes no tienen HTML. Una documental que crea un documento nuevo sigue teniendo rama. La «Actualizar» del CLAUDE.md lleva tres pasos «Reflejar» de una tarea que aún está en observación.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 436" width="100%" role="img" aria-label="La vuelta de un documento: el subagente escribe el .md; después, respaldar, regenerar el HTML, el commit en develop y abrir el HTML, que hoy van a mano o no existen y que la orden propuesta haría juntos" style="font-family:var(--fuente-texto);display:block">
<rect x="10" y="10" width="430" height="70" rx="10" fill="none" style="stroke:var(--primario-linea)" stroke-width="1.5"/>
<text x="26" y="40" font-size="18" font-weight="700" style="fill:var(--oscuro)">Escribe el subagente</text>
<text x="26" y="64" font-size="15" style="fill:var(--texto-suave)">el .md, en la carpeta del documento</text>
<rect x="10" y="100" width="430" height="70" rx="10" fill="none" style="stroke:var(--primario-linea)" stroke-width="1.5"/>
<text x="26" y="130" font-size="18" font-weight="700" style="fill:var(--oscuro)">Respaldar la versión anterior</text>
<text x="26" y="154" font-size="15" style="fill:var(--texto-suave)">respaldar.py, a mano; se para si el nombre existe</text>
<rect x="10" y="190" width="430" height="70" rx="10" fill="none" style="stroke:var(--primario-linea)" stroke-width="1.5"/>
<text x="26" y="220" font-size="18" font-weight="700" style="fill:var(--oscuro)">Regenerar el HTML</text>
<text x="26" y="244" font-size="15" style="fill:var(--texto-suave)">un generador por tipo, a mano; 11 de 25 desfasados</text>
<rect x="10" y="280" width="430" height="70" rx="10" fill="none" style="stroke:var(--primario-linea)" stroke-width="1.5"/>
<text x="26" y="310" font-size="18" font-weight="700" style="fill:var(--oscuro)">Commit en develop</text>
<text x="26" y="334" font-size="15" style="fill:var(--texto-suave)">solo con develop activa; la documental, con rama</text>
<rect x="10" y="370" width="430" height="56" rx="10" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.5" stroke-dasharray="6 4"/>
<text x="26" y="396" font-size="18" font-weight="700" style="fill:var(--oscuro)">Abrir el HTML</text>
<text x="26" y="416" font-size="15" style="fill:var(--texto-suave)">sin rama, nada lo abre</text>
<line x1="225" y1="80" x2="225" y2="100" style="stroke:var(--primario-linea)" stroke-width="2"/>
<line x1="225" y1="170" x2="225" y2="190" style="stroke:var(--primario-linea)" stroke-width="2"/>
<line x1="225" y1="260" x2="225" y2="280" style="stroke:var(--primario-linea)" stroke-width="2"/>
<line x1="225" y1="350" x2="225" y2="370" style="stroke:var(--primario-linea)" stroke-width="2"/>
<path d="M456 100 H472 V426 H456" fill="none" style="stroke:var(--texto-suave)" stroke-width="2" stroke-dasharray="6 4"/>
<text x="508" y="263" font-size="15" text-anchor="middle" transform="rotate(-90 508 263)" style="fill:var(--texto-suave)">cola.py documento (propuesta)</text>
</svg>
<figcaption style="font-size:.82rem;text-align:center;font-style:italic;margin-top:.3rem;">Tras escribir, cuatro pasos que hoy van a mano o faltan; la llave discontinua es la orden propuesta, que los haría juntos.</figcaption>
</figure>

De las once preguntas que llegaron del informe «Tipos de tarea», la 13 ya estaba resuelta y las otras diez las ha decidido el propietario, todas con la opción recomendada (A). **No queda ninguna pregunta abierta.** Las decisiones están registradas como 393 (la vuelta de un documento), 394 (las «Actualizar…») y 395 (el diálogo de las skills de documentos).

Salen cinco tareas, ya en la cola, y un paso en la tarea 305. Se separaron dos cosas: el paso del botón «Finalizar deliberación», que ya era de la 305, y el umbral de pasos, que pasa a la 309.

[Ver lo decidido](#decidido){: .salto} · [Ver las tareas](#tareas){: .salto}

## Hoy | Cómo funciona hoy cada pieza | Hoy {#hoy}

Lo decidido el 2 de noviembre (216, 217, 219, 220) está escrito en las skills, pero casi todo se hace a mano. Solo las deliberativas tienen ya su camino en `cola.py`: sin rama, worktree ni rama auxiliar (278). Las documentales siguen el camino de una tarea de código aunque su documento sea nuevo. El color de cada tarjeta dice si la pieza existe (verde), existe a medias (naranja) o falta (frambuesa).

::: tarjetas 3 plegables

### Solo su documento {color=aviso icono=documento}

Hoy
:   Es una regla, en el encargo de las deliberativas (278), en `sf:orquestacion` (369) y en `sf:flujo_tareas`. El CLI no lo comprueba (240).

Falta
:   Que la tarea declare su documento y que solo ese documento entre en `develop`.

### Respaldo {color=aviso icono=carpeta}

Hoy
:   `respaldar.py` copia el `.md` y su HTML a `_respaldo/` (217). Lo llama a mano el subagente. Si el nombre ya existe, se para. Los registros (decisiones y propuestas) no se respaldan.

Falta
:   Que lo haga la orden de cada vuelta, y la regla de los nombres repetidos.

### HTML al día {color=error icono=documento}

Hoy
:   Un generador único y un envoltorio por tipo, que se lanza a mano (220). 11 de los 25 HTML no corresponden a su `.md`: la mudanza de la 379 reescribió sus enlaces sin regenerarlos. Seis informes no tienen HTML.

Falta
:   Una orden que elija el generador, y el aviso de los desfasados. El pie dice «commit X (con cambios sin commit)» y cita el commit anterior.

### A develop {color=aviso icono=rama}

Hoy
:   La deliberativa escribe en la carpeta del proyecto. Hace el commit en `develop` solo si `develop` es la rama activa (278). La documental tiene rama aunque su documento sea nuevo: `cola.py rama` solo se niega en las deliberativas.

Ya existe
:   `commit_en_develop` hace un commit en `develop` sin cambiar de rama. Lo usan `decision` y las propuestas.

### Abrir el HTML {color=error icono=lupa}

Hoy
:   Solo Activar rama abre los HTML que cambia la rama de la tarea. Un documento sin rama no lo abre nada: lo ofrece el principal, si se acuerda.

En marcha
:   El botón Abrir de cada tarea, en «Abrir los documentos desde el panel» (452).

### Las «Actualizar…» {color=aviso icono=dialogo}

Hoy
:   Cada documento tiene una tarea (377), y se hacen de una en una, con su subagente (152). Las tres atascadas del informe 274 se cerraron: 198, 308 y 316.

Pero
:   La del CLAUDE.md y el arranque (422) lleva 12 pasos pendientes desde el 24/11 y nunca se ha puesto en curso. Tres de esos pasos son de la 379, que sigue en observación.

:::

Algunas cosas ya están resueltas. La pregunta 13 la resolvieron las decisiones 344 y 346. El aviso del informe «Tipos de tarea» sobre el CLAUDE.md, que decía «en el principal», ya no vale: el CLAUDE.md dice ahora «cada una con su subagente». El paso del botón «Finalizar deliberación» ya es de «Decidir y aplicar cómo se lleva y se cierra cada familia de tareas, con su agente» (305) y se quitó de esta tarea.

## La orden | Una orden para cada vuelta | La orden {#orden}

La orden junta las cuatro piezas en una llamada que el subagente hace al terminar cada vuelta. Así no depende de que Claude se acuerde, que es lo que hoy deja HTML desfasados y documentos sin commit. El nombre, `cola.py documento`, es provisional.

1. **Declara el documento.** La primera vez, anota en la tarea la ruta de su `.md`; después, solo admite esa ruta. Entran el `.md`, su HTML, su carpeta de imágenes o diagramas y sus respaldos (pregunta 1: [cómo se cumple «solo su documento»](#p1)).
2. **Respalda.** Si `develop` ya tiene el documento, copia esa versión y su HTML a `_respaldo/<nombre>_antes-<motivo>`, con «-2», «-3»… si el nombre existe. El respaldo sale de `develop`, no de la copia del subagente, y va en el mismo commit ([respaldos con el mismo nombre](#p10), [qué se respalda](#p12)).
3. **Regenera el HTML** con el generador de su tipo, en el mismo cambio.
4. **Hace el commit en `develop`** solo de esos archivos, con `commit_en_develop`: un commit normal si `develop` está activa y, si no, sin tocar la copia de trabajo ([subagente de un documento nuevo](#p3)).
5. **Abre el HTML** si la tarea es el foco. Si no lo es, lo dice en su salida ([cuándo se abre](#p6)).

A favor: una vuelta pasa a ser una sola orden, y el documento de cada tarea queda anotado en la cola, que es lo que necesita el botón Abrir de «Abrir los documentos desde el panel» (452). En contra: `cola.py` crece y tiene que conocer los generadores. Un documento que ya existe sigue con su rama y su squash: para él, la orden solo regenera y respalda. Se hace en la tarea 469.

### Los pasos de implementación de la tarea

Estos pasos de la tarea 303 han ido a otras tareas o se han quitado:

| Paso | Dónde queda |
| --- | --- |
| Respaldar antes de sustituir | En «Llevar cada vuelta de un documento a develop con una orden: respaldo, HTML, commit y apertura» (469) |
| Regenerar con una orden única y comprobar que ninguno queda desfasado | En «Avisar de los HTML desfasados de su .md, con una orden única para regenerar» (470) |
| Botón «Finalizar deliberación» | Quitado: ya es un paso de «Decidir y aplicar cómo se lleva y se cierra cada familia de tareas, con su agente» (305) |
| Sin rama para una tarea que solo hace un documento nuevo | En la tarea 469: `rama` se niega si el documento declarado aún no está en `develop` |
| Que el pie no diga «con cambios sin commit» | En la tarea 470: si el `.md` no tiene commit, el pie da la huella y «sin commit todavía» |

## Decidido | Lo que ya está decidido | Decidido {#decidido}

Esta tarea ha fijado tres decisiones, que recogen las diez preguntas. Debajo, las decisiones anteriores en las que se apoya.

| Nº | Decisión | Qué fija aquí |
| --- | --- | --- |
| 393 | Cada vuelta de un documento la lleva a develop una sola orden, solo con ese documento | La orden, el documento declarado, el worktree desprendido, cuándo se abre el HTML, los respaldos con «-2», qué se respalda, el `.ignore` y la copia anotada fuera de git (preguntas 1, 3, 6, 10, 11, 12 y 14) |
| 394 | Las «Actualizar…» no se quedan atrás: Reflejar nace al entrar la tarea en develop y RELEASE avisa de las pendientes | El momento del paso «Reflejar» y el aviso de RELEASE (preguntas 2 y 4) |
| 395 | En las skills de documentos, el subagente prepara en tanda las preguntas de cada fase y el principal las lleva al propietario | El reparto del diálogo (pregunta 15) |
| 344, 346 | La mudanza a `sf/`, justo antes de cerrar; todos los informes en `sf/informes/` | Resolvieron la pregunta 13 |

Siguen vigentes, como base: 147 (documentación una vez por tarea), 216 (los documentos nuevos van a `develop` y se ofrecen en el navegador), 217 (respaldar antes de sustituir), 219 (el tipo de tarea decide cómo se maneja el repositorio), 220 (cada cambio de un `.md` regenera su HTML), 278 (una deliberativa solo escribe su documento), 369 (una tarea de código tampoco crea documentos) y 377 (cada documento compartido se actualiza en su tarea).

## Por decidir | Todo decidido | Por decidir {#por-decidir}

No queda ninguna pregunta abierta: las diez están decididas, todas con la opción recomendada (A). Las preguntas conservan el número del informe «Tipos de tarea» (274), que es el que citan los pasos de las tareas. Van en tres bloques: la vuelta de un documento, las «Actualizar…», y la revisión y el diálogo.

## La vuelta de un documento | Seis preguntas que dan forma a la orden | Decidido · vuelta {#por-decidir-vuelta}

Las seis dan forma a la orden de cada vuelta. Las recoge la decisión 393 y las lleva la tarea 469 (salvo la 11 y la 14, que van a la 472).

::: preguntas 2 plegables

### 1 · Cómo se cumple «solo su documento» {estado=decidida recomendada=A elegida=A} {: #p1}

Hoy es una regla, escrita en el encargo de las deliberativas y en la orquestación, y nada la comprueba. Una deliberativa hace su commit en `develop` sin que nada mire qué lleva.

Opción A
:   La tarea declara su documento con la orden de cada vuelta, y la orden solo lleva a `develop` ese documento con lo suyo. En una documental con rama, `cerrar` se niega si la rama toca otros archivos.

Opción B
:   Solo la regla, como hoy, en la orquestación y en el encargo.

Opción C
:   Solo una comprobación por familia al cerrar: que la rama no toque más que `.md`, HTML, imágenes y `_respaldo/`.

Recomendación
:   **A.** Se cumple con la orden, sin depender de la memoria, y da al panel el documento de cada tarea, que necesita «Abrir los documentos desde el panel» (452).

Decisión
:   A. La tarea declara su documento y solo ese documento, con lo suyo, entra en `develop`. Decisión 393; la aplica la tarea 469.

### 3 · El subagente de un documento nuevo {estado=decidida recomendada=A elegida=A} {: #p3}

Una deliberativa ya trabaja sin worktree y solo hace commit con `develop` activa. Si el propietario está probando otra tarea, el informe queda sin commit en la copia de trabajo de esa rama, y al volver a `develop` git puede negarse a cambiar.

Opción A
:   Un worktree desprendido desde `develop`, sin rama propia, solo para escribir. La orden lleva el documento a `develop` con `commit_en_develop` y pone el worktree al día.

Opción B
:   Sin worktree, como hoy, y la orden hace el commit con `commit_en_develop` aunque haya otra rama activa. El archivo sigue en la copia de trabajo de esa rama.

Opción C
:   Como hoy.

Recomendación
:   **A.** Nunca toca la copia de trabajo del propietario y funciona con cualquier rama activa. B deja el choque para cuando se vuelve a `develop`.

Decisión
:   A. El subagente de un documento nuevo escribe en un worktree desprendido desde `develop`, sin rama propia. Decisión 393; la aplica la tarea 469.

### 6 · Cuándo se abre el HTML en cada vuelta {estado=decidida recomendada=A elegida=A} {: #p6}

Se decidió ofrecerlo en cada versión nueva. Abrir una ventana mientras el propietario está en otra tarea le interrumpe.

Opción A
:   Lo abre la orden de cada vuelta si la tarea es el foco, que ya se guarda en la cola. Si no lo es, la orden lo dice en su salida y el principal lo deja como off-topic. Para abrirlo otra vez, el botón Abrir de «Abrir los documentos desde el panel» (452).

Opción B
:   Lo abre siempre la orden.

Opción C
:   Lo ofrece el principal en cada vuelta, con una pregunta, como hoy.

Recomendación
:   **A.** Se cumple sin depender de Claude y no salta encima de otra tarea.

Decisión
:   A. Lo abre la orden si la tarea es el foco; si no, lo dice y el principal lo da como off-topic. Decisión 393; la aplica la tarea 469.

### 10 · Respaldos con el mismo nombre {estado=decidida recomendada=A elegida=A} {: #p10}

Hoy `respaldar.py` se para y pide otro motivo. Dentro de la orden, la vuelta se quedaría a medias.

Opción A
:   Añadir `-2`, `-3`… solo si el nombre ya existe.

Opción B
:   Poner siempre la fecha y la hora en el nombre.

Opción C
:   Como hoy: se para y se elige otro motivo.

Recomendación
:   **A.** El nombre sigue siendo el de siempre, y la vuelta no se para.

Decisión
:   A. Se añade «-2», «-3»… solo si el nombre ya existe. Decisión 393; la aplica la tarea 469.

### 11 · Búsquedas y respaldos {estado=decidida recomendada=A elegida=A} {: #p11}

La búsqueda de Claude entra en `_respaldo/`. Buscar «punta a punta» en los `.md` de `sf/informes/` da siete archivos, y los siete son respaldos. En una carpeta de prueba se comprobó que un `.ignore` con `_respaldo/` los quita de las búsquedas a cualquier profundidad, y que si se nombra la carpeta se sigue buscando en ella.

Opción A
:   Un `.ignore` con `_respaldo/` en la raíz de la SF y en la de cada proyecto, que lo pone la incorporación. ripgrep lo respeta; git, no.

Opción B
:   Nada.

Recomendación
:   **A.** Claude deja de citar como vigente una versión sustituida, y los respaldos se siguen encontrando cuando se buscan a propósito.

Decisión
:   A. Un `.ignore` con `_respaldo/` en la SF y en cada proyecto. Decisión 393; la aplica la tarea 472.

### 12 · Qué se respalda {estado=decidida recomendada=A elegida=A} {: #p12}

En la práctica ya es A. Los informes, las visiones y los «Cómo funciona…» se respaldan. `cola.py` escribe las decisiones y las propuestas por partes, sin respaldo. Faltaba registrarlo.

Opción A
:   Solo los documentos que se reescriben enteros. Los registros (propuestas, decisiones y su índice), no.

Opción B
:   Todo documento que cambie una tarea de documentos.

Recomendación
:   **A.** Los registros se editan por partes, y git ya guarda su historia.

Decisión
:   A. Solo se respaldan los documentos que se reescriben enteros; los registros, no. Decisión 393; la aplica la tarea 469.

### 14 · Revisión con notas {estado=decidida recomendada=A elegida=A} {: #p14}

«Guardar» crea la copia anotada `<nombre>.notas-<autor>.html`, y `extraer_notas.py` la lee. Nada decía dónde va esa copia ni si entra en git, y el `.gitignore` no la nombra.

Opción A
:   La copia anotada se guarda junto al documento y fuera de git (`*.notas-*.html` en el `.gitignore`, también en los proyectos). El subagente le pasa `extraer_notas.py` en la vuelta siguiente.

Opción B
:   Las notas llegan por el chat.

Opción C
:   La copia anotada entra en git, como registro de la revisión.

Recomendación
:   **A.** Lo que vale de la copia pasa al `.md`. Versionarla llenaría el historial de HTML enteros.

Decisión
:   A. La copia anotada, junto al documento y fuera de git. Decisión 393; la aplica la tarea 472.

:::

## Las «Actualizar…» | Que los documentos compartidos no se queden atrás | Decidido · Actualizar {#por-decidir-compartidos}

Dos preguntas sobre cuándo llega el trabajo a las «Actualizar…» y cómo no se quedan paradas. Las recoge la decisión 394 y las lleva la tarea 473. El umbral del panel de la pregunta 2 se llevó a «Decidir si el panel avisa por umbral de pasos» (309).

[Ver la separación](#a-309){: .salto}

::: preguntas 2 plegables

### 2 · Las tareas «Actualizar…» atascadas {estado=decidida recomendada=A elegida=A} {: #p2}

Las tres atascadas del informe «Tipos de tarea» se cerraron, pero la «Actualizar» del CLAUDE.md y el arranque (422) lleva 12 pasos sin ponerse en curso. La opción «cada tarea en su rama» de entonces ya no cabe, porque se descartó.

Opción A
:   RELEASE avisa de las «Actualizar…» con pasos pendientes, porque la versión saldría con esos documentos desfasados. Y, cuando está libre, el principal propone primero las que pasan de diez pasos o de una semana.

Opción B
:   Solo un aviso por umbral en el panel, que se decide en «Decidir si el panel avisa por umbral de pasos» (309).

Opción C
:   Como hoy.

Recomendación
:   **A.** Publicar es cuando un documento desfasado hace daño. Si la 309 fija un umbral para el panel, se usa el mismo.

Decisión
:   A. RELEASE avisa de las «Actualizar…» pendientes y el principal propone primero las de más de diez pasos o una semana. Decisión 394; la aplica la tarea 473.

### 4 · Cuándo se añade «Reflejar» {estado=decidida recomendada=A elegida=A} {: #p4}

Hoy se añade al poner en curso la tarea de origen. La regla pide un solo paso por tarea, y que quien actualiza mire su squash, que en ese momento aún no existe. La «Actualizar» del CLAUDE.md (422) tiene tres pasos de una tarea que sigue en observación y uno de otra en curso.

Opción A
:   Al poner en curso se anota en la propia tarea qué documento compartido toca. `cola.py` añade el paso «Reflejar» a la «Actualizar…» cuando la tarea entra en `develop` (cerrar o a observación), uno solo, y descartar o revertir lo quita.

Opción B
:   Como hoy, pero el subagente de la «Actualizar…» solo refleja las tareas que ya están en `develop`, y deja pendientes los demás pasos.

Opción C
:   Como hoy.

Recomendación
:   **A.** El paso nace cuando ya hay un squash que mirar, y no se repite.

Decisión
:   A. «Reflejar» nace al entrar la tarea en `develop`, uno solo. Decisión 394; la aplica la tarea 473.

:::

## La revisión y el diálogo | Revisión, diálogo y sitio de los informes | Decidido · revisión {#por-decidir-revision}

Cómo vuelven las notas del propietario al `.md` y quién lleva el diálogo de las skills de documentos. La pregunta 14 (revisión con notas) quedó en el primer bloque; aquí quedan la 13, resuelta antes, y la 15 (decisión 395).

::: preguntas 2 plegables

### 13 · Migración a sf/ {estado=decidida recomendada=A elegida=A} {: #p13}

Opción A
:   Migrar cuando no haya en curso tareas con informes o documentos de la SF.

Opción B
:   Migrar ya. Cada subagente mueve su informe al integrar `develop`.

Recomendación
:   **A.**

Decisión
:   A, por decisiones anteriores (344 y 346). La mudanza se hizo justo antes de cerrar la tarea que la lleva, sin otras ramas tocando esos archivos, con todos los informes en `sf/informes/`. `informe_deliberativa` ya los pone ahí.

### 15 · Diálogo de las skills de documentos {estado=decidida recomendada=A elegida=A} {: #p15}

En la práctica ya es A. El subagente propone y devuelve lo que hay que decidir, y el principal lo lleva al propietario. Las skills de visión y fundacional no lo decían: su fase 1 es «valorar en conversación».

Opción A
:   El subagente prepara en tanda las preguntas de cada fase y el principal las lleva al propietario. Se escribe así en las dos skills.

Opción B
:   El principal hace la fase de diálogo, con la instrucción expresa del propietario.

Recomendación
:   **A**, y B cuando el propietario lo pida. Es lo que ya se hace; faltaba escribirlo donde se lee al crear un documento.

Decisión
:   A. El subagente prepara en tanda las preguntas de cada fase y el principal las lleva; el diálogo directo, solo cuando el propietario lo pida. Decisión 395; lo aplica un paso de la tarea 305.

:::


## Separar | Lo que se llevó a otras tareas | Separar {#separar}

Todo está hecho. Se separaron dos cosas: un paso repetido y un umbral que ya se delibera en otra tarea.

::: tarjetas 2

### 1 · Quitar el paso del botón «Finalizar deliberación» de esta tarea {: #a-305}

El paso «Botón Finalizar deliberación» ya es un paso de la tarea «Decidir y aplicar cómo se lleva y se cierra cada familia de tareas, con su agente» (305).

Hecho
:   Quitado de esta tarea (303). No se llevó ninguna pregunta.

### 2 · El umbral de pasos, a «Decidir si el panel avisa por umbral de pasos» (309) {: #a-309}

Esa tarea ya delibera si el panel avisa por número de pasos.

Hecho
:   Se le llevó la parte de umbral de la [pregunta 2](#p2): diez pasos o una semana, y si el panel lo pinta. El aviso de RELEASE se queda en la tarea 473.

:::

## Tareas | Las tareas que salen | Tareas {#tareas}

Salen cinco tareas y un paso en la 305. Todas están ya en la cola.

| Tarea | Tipo | Qué hace |
| --- | --- | --- |
| «Llevar cada vuelta de un documento a develop con una orden: respaldo, HTML, commit y apertura» (469) | implementar | `cola.py documento N RUTA`: declara el documento, respalda la versión de `develop`, regenera, hace el commit con `commit_en_develop` y abre el HTML si la tarea es el foco. Lleva el worktree desprendido, la negativa de `rama` para un documento nuevo, los respaldos con «-2», «-3» y las preguntas 1, 3, 6, 10 y 12. |
| «Avisar de los HTML desfasados de su .md, con una orden única para regenerar» (470) | implementar | Una orden que elige el generador por el tipo del documento. Con `--comprobar`, lista los HTML cuya huella no es la del `.md` y los `.md` sin HTML. El pie deja de citar el commit anterior. |
| «Regenerar los HTML desfasados y crear los que faltan» (471) | documentar | Los 11 desfasados y los 6 informes sin HTML, después de la anterior (470). Los «Cómo funciona…», como paso «Reflejar» de su «Actualizar…». |
| «Que las búsquedas no entren en _respaldo/ y las copias anotadas no entren en git» (472) | implementar | `.ignore` y `.gitignore` en la SF y en la incorporación de proyectos. Preguntas 11 y 14. |
| «Que «Reflejar» nazca al entrar la tarea en develop, y RELEASE avise de las «Actualizar…» pendientes» (473) | implementar | En `cola.py`, el panel y `sf:orquestacion`. Preguntas 2 y 4. |
| Un paso en «Decidir y aplicar cómo se lleva y se cierra cada familia de tareas, con su agente» (305) | decidir y aplicar | «Decir en documento_vision y documento_fundacional cómo se reparten el diálogo el principal y el subagente» (pregunta 15). |

## Anexo | Texto propuesto para los documentos compartidos | Anexo {#anexo}

Se aplica cuando estén hechas las tareas que salen, con su paso «Reflejar» en la «Actualizar…» de cada documento. El propietario ha elegido las opciones recomendadas.

**Metodología, «Tareas y cola», y «Cómo funciona la Software Factory»:**

> Una tarea de documentos declara su documento. Cada vuelta la lleva a `develop` la orden `cola.py documento N RUTA`: respalda la versión anterior en `_respaldo/`, regenera el HTML, hace el commit en `develop` sin cambiar de rama y abre el HTML si la tarea es el foco. Un documento nuevo no tiene rama, y su subagente escribe en un worktree desprendido desde `develop`; uno que ya existe se cambia en la rama de su tarea y entra por squash.

**Metodología, «Documentos compartidos»:**

> Al poner en curso una tarea, se anota qué documento compartido toca. Cuando la tarea entra en `develop`, `cola.py` añade a la «Actualizar &lt;documento&gt;» un solo paso, «Reflejar «&lt;título&gt;» (NN)». RELEASE avisa de las «Actualizar…» con pasos pendientes.