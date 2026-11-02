---
name: informe_deliberativa
description: Crea o pone al día el informe de una tarea deliberativa de la Software Factory (investigar, deliberar, diseñar) — con la estructura fija de resumen, el análisis, lo decidido, lo que queda por decidir partido en bloques, las separaciones propuestas y las tareas que salen — y con las preguntas como fichas con opciones, recomendación destacada y estado (abierta, decidida, separada), al día con cada respuesta del propietario. Cada vuelta sube la versión, respalda la anterior en _respaldo/ y regenera el HTML. Úsala cuando una tarea deliberativa escriba o actualice su informe, cuando haya que registrar en él una respuesta, una decisión o una separación, o al pasar un informe antiguo a este formato. Usa el generador y los recursos comunes de crear_documentos.
---

# Informe de una deliberativa

Una tarea deliberativa (investigar, deliberar o diseñar; «Siete tipos de tarea en tres familias», 223) da **un informe y las tareas que salgan de él** («Una tarea deliberativa da un informe y las tareas que salgan», 218). Sus dilemas viven en el informe, al día con cada respuesta del propietario, y no en la cola ni en otro archivo. Lo que es de otra tarea se propone separar; al cerrar, lo que siga abierto sale a su tarea («En una deliberativa, lo que es de otra tarea se propone separar», 221). Una deliberativa no prueba nada y solo cambia su informe: lo que haya que aplicar lo hacen las tareas que crea.

Esta skill dice qué lleva el informe, cómo se escriben sus preguntas y cómo es cada vuelta. El generador, los recursos, los temas y la comprobación son los de `crear_documentos`, que se lee junto a esta. Es la skill del agente de la familia deliberativa, cuando exista («Agentes especializados, uno por familia de tarea», 304); mientras tanto, la carga el subagente de la tarea.

**El lector es el propietario, que tiene que decidir.** El informe le ahorra trabajo: lo que tiene que decidir se ve primero, cada pregunta se responde con una letra y la recomendación se distingue de un vistazo. Comunicar bien es un objetivo de la SF (decisión 231).

## Dónde va

- En un proyecto incorporado a la SF, en `sf/informes/` («Los documentos de la SF van en la carpeta sf/», 203).
- En la propia SF, en `docs/referencias/reports/`, hasta que se decida su paso a `sf/` (pregunta 13 del informe «Tipos de tarea», en la tarea 303).

El nombre del archivo es el tema, no el número de la tarea: `Tipos de tarea.md` y su `.html`. Las versiones sustituidas van a `_respaldo/`, en la misma carpeta.

**Modelo:** el informe `docs/referencias/reports/Tipos de tarea.md` de la SF (tarea 274). Si está en el equipo, se lee como ejemplo; su contenido no se copia. La plantilla vacía está en `assets/plantilla-informe.md`.

## Estructura

Las secciones van siempre en este orden, con estos `{#id}`, para que el propietario sepa dónde mirar y las tareas puedan enlazarlas:

1. **Resumen** `{#resumen}`. La conclusión en dos o tres párrafos cortos: qué se propone, en qué se apoya y cuántas preguntas quedan y dónde. Si un esquema aclara el conjunto, va aquí. Termina con saltos a lo que hay que decidir (`[Ver las N preguntas](#por-decidir){: .salto}`).
2. **El análisis**, en una o varias secciones propias: lo que se estudió y lo que se propone, con su porqué. Primero lo que se propone o se concluye, aunque se derive del resto; después, la valoración que lo sostiene y sus límites. Aquí van las tarjetas, los esquemas y las tablas del tema.
3. **Decidido** `{#decidido}`. Una tabla con las decisiones del propietario que fija esta tarea: `Nº | Decisión | Qué fija aquí`. Cada decisión está registrada en su archivo de decisiones antes de aparecer aquí.
4. **Por decidir** `{#por-decidir}`. Las preguntas abiertas, en un bloque `::: preguntas`. Si son muchas, se parten en bloques, cada uno en su sección (`{#por-decidir-<destino>}`), por importancia o por el sitio adonde irían si se separan; cada bloque abre con una frase que dice qué reúne y un salto a su separación.
5. **Separar** `{#separar}`. Las separaciones propuestas: una tarjeta por separación (`{: #a-<destino>}`), con qué se lleva (las preguntas, con enlace a cada una) y adónde (una tarea nueva, un paso de una tarea existente o `/sf_split`). Si hay que elegir cómo separar, también es una pregunta.
6. **Tareas** `{#tareas}`. Las tareas que salen: `Tarea | Tipo | Qué hace`. Las que ya existen, con su número.

Anexos, al final y solo si hacen falta: fuentes (`::: fuentes`), datos completos, texto propuesto para un documento que cambiará otra tarea.

Si el análisis no deja nada por decidir, separar o crear, esas secciones se quitan; las demás no cambian de orden.

**Cabecera:** `antetitulo` con «Proyecto · Informe de <análisis, diseño o investigación> · <mes año>», `lema`, `subtitulo` con lo que el informe responde, `version`, `estado` («Propuesta · Tarea N», «Decidido · Tarea N»…), `portada: oscura`, `destino: proyecto`, `herramientas`, `menu: secciones` (el propietario salta entre secciones), `tipo` («Informe de análisis», «Informe de diseño», «Informe de investigación») y `pie` con la tarea, de qué parte el informe y quién decide.

## Las preguntas

Cada pregunta es una tarjeta de `::: preguntas`, el recurso «pregunta con opciones» de `crear_documentos`:

```markdown
::: preguntas 2 plegables

### 1 · Cómo se cumple «solo su documento» {recomendada=A} {: #p1}

Hoy nada lo vigila: cualquier paso entra en la tarea.

Opción A
:   La tarea declara su documento con una orden, y `cerrar` se niega si la rama toca otros archivos.

Opción B
:   Solo la regla, escrita en la orquestación.

Recomendación
:   **A.** Se cumple con un comando, no con la memoria del principal.

:::
```

- **Una decisión por pregunta**, con un título que la nombra y un número por importancia (1 la más importante). El número y el ancla `{: #pN}` no cambian aunque la pregunta se decida o se separe: los pasos de las tareas la citan por ellos («Decidir … (pregunta 5) (informe «Tipos de tarea», 274)»).
- **Contexto en una o dos frases**, solo si hace falta para elegir: qué pasa hoy o por qué hay que decidir.
- **Dos o tres opciones**, `Opción A`, `Opción B`…, cada una con lo que implica en una o dos frases. «Como hoy» es una opción cuando lo es de verdad.
- **Recomendación** con su porqué en una frase, y `recomendada=A` en el título para que se destaque. Toda pregunta abierta lleva recomendación; el generador avisa si falta.
- **Estado**, al día con cada respuesta:
  - `estado=abierta` (por defecto): se espera la respuesta;
  - `estado=decidida elegida=B`: con un campo `Decisión` que dice lo elegido, con sus matices, y el número de la decisión registrada; la opción elegida se marca y las demás pasan a gris;
  - `estado=separada destino=tarea_303`: se fue a otra tarea (el `_` se lee como espacio en la marca). Sigue en el informe para que la tarea de destino la enlace.
- Las preguntas que dependen de otra se dicen en su contexto, con enlace a la otra.

Cuando una pregunta se decide o se separa, su tarjeta se queda en su bloque con el estado nuevo, y la decisión pasa también a la tabla de «Decidido». El resumen dice cuántas siguen abiertas.

## Cada vuelta

Cada respuesta del propietario, o cada avance del análisis que cambie el informe, es una vuelta:

1. **Respaldar** la versión que se va a sustituir: `python -I -X utf8 <skills>/crear_documentos/scripts/respaldar.py <informe>.md <motivo>` («Antes de sustituir un documento, se respalda en _respaldo/», 217).
2. **Escribir** los cambios: el estado de las preguntas respondidas, «Decidido», las separaciones y las tareas, y el resumen. **Subir la versión** en la cabecera (2.5 → 2.6; el primer número cuando cambia la estructura del informe) y poner al día el `estado`.
3. **Regenerar el HTML** en el mismo cambio («Cada cambio de un .md regenera su HTML», 220):

   ```bash
   python -I -X utf8 <skills>/informe_deliberativa/scripts/informe_to_html.py <informe>.md
   ```

4. **Llevarlo a `develop`** sin rama, porque es un documento nuevo («Los documentos nuevos van a develop en cada vuelta y se ofrecen en el navegador», 216), con la orden que lo hace cuando exista («Documentos nuevos a develop en cada vuelta, y abrirlos en el navegador», 297).
5. **Ofrecer abrir el HTML** en el navegador, con la versión nueva.

## Comprobación

La de `crear_documentos` («Comprobación») y, además:

- cada pregunta abierta tiene al menos dos opciones y una recomendada; ninguna decidida sin `elegida` ni separada sin `destino`;
- las cuentas del resumen (preguntas abiertas, separaciones, tareas) coinciden con las secciones;
- cada enlace a una pregunta (`#pN`) o a una separación (`#a-…`) existe;
- la tabla de «Decidido» solo trae decisiones ya registradas.
