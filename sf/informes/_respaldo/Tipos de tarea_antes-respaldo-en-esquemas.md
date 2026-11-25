---
antetitulo: Software Factory · Informe de análisis · Noviembre 2026
lema: Tres familias de tareas; // cada una, con su manejo y su agente.
subtitulo: Qué es cada familia de tareas y cómo usa el repositorio, el ciclo de una tarea deliberativa y de una documental de principio a fin, lo decidido, lo que queda por decidir, las separaciones propuestas y las tareas que salen.
version: Versión 2.1 · 02/11/2026
estado: Propuesta · Tarea 274
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de análisis
pie: Informe de la tarea «Tipos de tarea: tres familias, cómo usa el repositorio cada una y cómo se cierran» (274). Parte de las decisiones 212 y 215-223, de sf:flujo_tareas, sf:orquestacion, cola.py y el panel en develop, y de las tareas 190, 222 y 263 como casos. Las versiones anteriores, con el título «Tareas deliberativas», están en _respaldo/.
---
# Tipos de tarea

## Resumen | Tres familias, dos maneras de usar el repositorio | Resumen {#resumen}

Los siete tipos de tarea forman tres familias: código, deliberativas y documentales. Cada familia tendrá en el plugin su propio agente especializado.

El tipo decide cómo se usa el repositorio. Una tarea de código usa rama, worktree, squash y observación. Una deliberativa o una documental solo cambia documentos y se cierra con la aprobación del propietario, sin prueba.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 330" width="100%" role="img" aria-label="Las tres familias y su camino en el repositorio: código va por rama y worktree; las deliberativas, por documento nuevo; las documentales, por documento nuevo o por documento existente" style="font-family:var(--fuente-texto);display:block">
<defs>
<marker id="fl-cod" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1f7a7a"/></marker>
<marker id="fl-del" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#a6501a"/></marker>
<marker id="fl-doc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1f812d"/></marker>
</defs>
<rect x="10" y="10" width="230" height="90" rx="10" fill="none" stroke="#1f7a7a" stroke-width="1.5"/>
<rect x="10" y="10" width="230" height="5" rx="2" fill="#1f7a7a"/>
<text x="26" y="44" font-size="18" font-weight="700" fill="#1f7a7a">Código</text>
<text x="26" y="70" font-size="15" style="fill:var(--texto-suave)">implementar y corregir</text>
<rect x="10" y="120" width="230" height="90" rx="10" fill="none" stroke="#a6501a" stroke-width="1.5"/>
<rect x="10" y="120" width="230" height="5" rx="2" fill="#a6501a"/>
<text x="26" y="154" font-size="18" font-weight="700" fill="#a6501a">Deliberativas</text>
<text x="26" y="180" font-size="15" style="fill:var(--texto-suave)">investigar, deliberar</text>
<text x="26" y="199" font-size="15" style="fill:var(--texto-suave)">y diseñar</text>
<rect x="10" y="230" width="230" height="90" rx="10" fill="none" stroke="#1f812d" stroke-width="1.5"/>
<rect x="10" y="230" width="230" height="5" rx="2" fill="#1f812d"/>
<text x="26" y="264" font-size="18" font-weight="700" fill="#1f812d">Documentales</text>
<text x="26" y="290" font-size="15" style="fill:var(--texto-suave)">especificar y documentar</text>
<line x1="242" y1="55" x2="316" y2="55" stroke="#1f7a7a" stroke-width="2" marker-end="url(#fl-cod)"/>
<line x1="242" y1="165" x2="316" y2="165" stroke="#a6501a" stroke-width="2" marker-end="url(#fl-del)"/>
<line x1="242" y1="262" x2="316" y2="185" stroke="#1f812d" stroke-width="2" marker-end="url(#fl-doc)"/>
<line x1="242" y1="285" x2="316" y2="285" stroke="#1f812d" stroke-width="2" marker-end="url(#fl-doc)"/>
<rect x="320" y="10" width="230" height="90" rx="10" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/>
<text x="336" y="44" font-size="18" font-weight="700" style="fill:var(--oscuro)">Rama y worktree</text>
<text x="336" y="70" font-size="15" style="fill:var(--texto-suave)">squash en develop</text>
<text x="336" y="89" font-size="15" style="fill:var(--texto-suave)">prueba y observación</text>
<rect x="320" y="120" width="230" height="90" rx="10" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/>
<text x="336" y="154" font-size="18" font-weight="700" style="fill:var(--oscuro)">Documento nuevo</text>
<text x="336" y="180" font-size="15" style="fill:var(--texto-suave)">sin rama; a develop</text>
<text x="336" y="199" font-size="15" style="fill:var(--texto-suave)">aprobación del propietario</text>
<rect x="320" y="230" width="230" height="90" rx="10" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/>
<text x="336" y="264" font-size="18" font-weight="700" style="fill:var(--oscuro)">Documento existente</text>
<text x="336" y="290" font-size="15" style="fill:var(--texto-suave)">rama de la tarea y squash</text>
<text x="336" y="309" font-size="15" style="fill:var(--texto-suave)">aprobación del propietario</text>
</svg>
<figcaption style="font-size:.82rem;text-align:center;font-style:italic;margin-top:.3rem;">A la izquierda, las familias y sus tipos; a la derecha, el camino que siguen en el repositorio y cómo se cierran.</figcaption>
</figure>

Una deliberativa entrega un informe y las tareas que salgan de él. Sus dilemas viven en el informe. Lo que es de otra tarea se separa, y lo que queda abierto al cerrar, también.

Una documental escribe un documento acordado y solo toca ese documento. Si el documento es nuevo, va a `develop` en cada vuelta: con su respaldo, con su HTML regenerado y abierto en el navegador.

Quedan 17 preguntas abiertas, casi todas sobre cómo se implementa lo decidido. Se propone repartirlas en tres sitios: esta tarea, una deliberativa nueva sobre el ciclo de los documentos y la tarea que implementa la copia a `develop` (297).

[Ver las 17 preguntas](#por-decidir){: .salto} · [Ver las separaciones propuestas](#separar){: .salto}

## Familias | Qué es cada una y cómo usa el repositorio | Familias {#familias}

Deliberativas y documentales comparten el manejo del repositorio. Son familias distintas porque su trabajo es distinto y cada una tendrá su propio agente.

### Las tres familias

<div class="tarjetas cols-3" markdown="1">

<article class="tarjeta" style="--oscuro:#134c4c;--borde:#c0dada;border-top:4px solid #1f7a7a;" markdown="1">

#### Código

Tipos
:   implementar, corregir

Resultado
:   Código y pruebas

</article>

<article class="tarjeta" style="--oscuro:#673210;--borde:#e6cebf;border-top:4px solid #a6501a;" markdown="1">

#### Deliberativas

Dialogan, deciden y separan temas.

Tipos
:   investigar, deliberar, diseñar

Resultado
:   Un informe y las tareas que salgan

</article>

<article class="tarjeta" style="--oscuro:#134f1c;--borde:#c3e0c7;border-top:4px solid #1f812d;" markdown="1">

#### Documentales

Escriben lo que ya está acordado.

Tipos
:   especificar, documentar

Resultado
:   Un documento acordado

</article>

</div>

### Cómo usa el repositorio cada camino

| Camino | Repositorio | Cierre |
| --- | --- | --- |
| Código | Rama de la tarea, worktree del subagente, squash en `develop` | Se prueba, se cierra y pasa a observación |
| Documento nuevo | Sin rama para el documento; copia a `develop` en cada vuelta | Aprobación del propietario, sin observación |
| Documento existente | Rama de la tarea y squash al cerrar | Aprobación del propietario, sin observación |

Una deliberativa siempre va por «documento nuevo», porque su documento es su informe. Una documental va por «documento nuevo» o por «documento existente», según su documento.

El modelo de ramas no cambia: `develop` para integrar y `main` para publicar.

### Lo común a deliberativas y documentales

- Solo tocan su documento: el `.md`, su HTML, su carpeta de imágenes y sus respaldos. Ni código, ni skills, ni otros documentos.
- Antes de sustituir un documento, la versión anterior se copia a `_respaldo/`, en la misma carpeta, como `<nombre>_antes-<motivo>.<ext>`, junto con su HTML. Volver atrás es copiarla de vuelta.
- Cada cambio del `.md` regenera su HTML en el mismo cambio.
- En cada versión nueva, Claude ofrece abrir el HTML en el navegador.
- No se prueban y no pasan a observación.

## Deliberativa | El ciclo de principio a fin | Deliberativa {#deliberativa}

Del alta al cierre, en siete momentos. El informe, las preguntas y las separaciones van en vueltas, una por cada respuesta del propietario.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 445" width="100%" role="img" aria-label="Ciclo de una deliberativa: nace, se pone en curso, escribe su informe, pregunta y decide, separa lo ajeno, crea las tareas que salgan y se cierra con Finalizar deliberación; del informe a las tareas se repite con cada respuesta" style="font-family:var(--fuente-texto);display:block">
<defs>
<marker id="fl-vuelta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#a6501a"/></marker>
</defs>
<line x1="34" y1="30" x2="34" y2="414" style="stroke:var(--linea)" stroke-width="2"/>
<circle cx="34" cy="30" r="8" style="fill:var(--fondo);stroke:var(--primario)" stroke-width="2"/>
<text x="56" y="28" font-size="18" font-weight="700" style="fill:var(--oscuro)">Nace</text>
<text x="56" y="49" font-size="15" style="fill:var(--texto-suave)">por el menú de alta, con su tipo</text>
<circle cx="34" cy="94" r="8" style="fill:var(--fondo);stroke:var(--primario)" stroke-width="2"/>
<text x="56" y="92" font-size="18" font-weight="700" style="fill:var(--oscuro)">Se pone en curso</text>
<text x="56" y="113" font-size="15" style="fill:var(--texto-suave)">el subagente analiza y propone</text>
<circle cx="34" cy="158" r="8" style="fill:var(--fondo);stroke:var(--primario)" stroke-width="2"/>
<text x="56" y="156" font-size="18" font-weight="700" style="fill:var(--oscuro)">Escribe su informe</text>
<text x="56" y="177" font-size="15" style="fill:var(--texto-suave)">formato de fundacional; a develop en cada vuelta</text>
<circle cx="34" cy="222" r="8" style="fill:var(--fondo);stroke:var(--primario)" stroke-width="2"/>
<text x="56" y="220" font-size="18" font-weight="700" style="fill:var(--oscuro)">Pregunta y decide</text>
<text x="56" y="241" font-size="15" style="fill:var(--texto-suave)">de una en una; cada decisión, en su archivo</text>
<circle cx="34" cy="286" r="8" style="fill:var(--fondo);stroke:var(--primario)" stroke-width="2"/>
<text x="56" y="284" font-size="18" font-weight="700" style="fill:var(--oscuro)">Separa lo que es de otra tarea</text>
<text x="56" y="305" font-size="15" style="fill:var(--texto-suave)">con la orden lista y el OK del propietario</text>
<circle cx="34" cy="350" r="8" style="fill:var(--fondo);stroke:var(--primario)" stroke-width="2"/>
<text x="56" y="348" font-size="18" font-weight="700" style="fill:var(--oscuro)">Crea las tareas que salgan</text>
<text x="56" y="369" font-size="15" style="fill:var(--texto-suave)">lo que haya que aplicar, en tareas nuevas</text>
<circle cx="34" cy="414" r="8" style="fill:var(--primario);stroke:var(--primario)" stroke-width="2"/>
<text x="56" y="412" font-size="18" font-weight="700" style="fill:var(--oscuro)">Se cierra</text>
<text x="56" y="433" font-size="15" style="fill:var(--texto-suave)">«Finalizar deliberación»; sin prueba ni observación</text>
<path d="M470 350 C 528 350 528 158 470 158" fill="none" stroke="#a6501a" stroke-width="2" marker-end="url(#fl-vuelta)"/>
<text x="548" y="254" font-size="15" fill="#a6501a" text-anchor="middle" transform="rotate(-90 548 254)">con cada respuesta</text>
</svg>
<figcaption style="font-size:.82rem;text-align:center;font-style:italic;margin-top:.3rem;">La flecha marca la vuelta: del informe a las tareas que salen, se repite hasta finalizar.</figcaption>
</figure>

### Nace

Entra por el menú de alta, con su tipo: investigar, deliberar o diseñar.

El título dice lo que queda decidido, o la pregunta, con el verbo del oficio.

La descripción empieza por la pregunta y por qué hace falta decidirla.

### Se pone en curso

Como toda tarea en curso, tiene su subagente. El principal habla con el propietario; el subagente analiza y propone.

Los primeros pasos son «Analizar…» y «Proponer…». Detrás va «Decidir con el propietario lo que salga y registrarlo».

### Escribe su informe

El informe tiene el formato de los fundacionales y se genera con `fundacional_to_html.py`.

Su sección central reúne lo que queda por decidir. Cada pregunta lleva sus opciones, sus pros y contras, una recomendación y de qué depende.

El informe es un documento nuevo. En cada vuelta se respalda la versión anterior, se copia a `develop`, se regenera el HTML y se ofrece abrirlo. El propietario lo lee siempre en `develop`.

### Pregunta y decide

El principal lleva las preguntas al propietario de una en una.

Cada decisión se registra al tomarse, en su propio archivo, con `cola.py decision`.

Con cada respuesta, el subagente pone el informe al día: la pregunta queda decidida, pasa a otra tarea o se descarta.

Los dilemas abiertos viven **en el informe y en ningún otro sitio**.

### Separa lo que es de otra tarea

Cuando aparece un tema de otra tarea, Claude propone sacarlo, en una línea y con la orden lista: `/sf_split`, un paso de otra tarea o una tarea nueva. Lo hace con el OK del propietario.

### Crea las tareas que salgan

Una deliberativa no cambia código ni otros documentos. Lo que haya que aplicar lo hacen tareas nuevas: deliberativas, documentales o de código.

Cuáles, se decide con el propietario a medida que avanza la tarea. Cada una entra por el menú de alta y deja en la deliberativa el paso «Creada la tarea N para …».

### Se cierra

En el panel, el botón se llama «Finalizar deliberación» y hace lo mismo que cerrar.

Antes de finalizar, cada tema que siga abierto sale a su propia tarea. La deliberativa se cierra con lo decidido.

El OK del propietario es la aprobación. No hay prueba ni observación.

## Documental | El ciclo de principio a fin | Documental {#documental}

Del alta al cierre, en cuatro pasos. Escribir y revisar se repiten en cada vuelta de afinado.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 330" width="100%" role="img" aria-label="Ciclo de una documental: nace, escribe (un documento nuevo sin rama y a develop en cada vuelta; uno existente en la rama de la tarea), se revisa con notas y vuelve a escribir, y se aprueba y se cierra sin observación" style="font-family:var(--fuente-texto);display:block">
<defs>
<marker id="fl-afinado" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1f812d"/></marker>
</defs>
<line x1="34" y1="30" x2="34" y2="280" style="stroke:var(--linea)" stroke-width="2"/>
<circle cx="34" cy="30" r="8" style="fill:var(--fondo);stroke:var(--primario)" stroke-width="2"/>
<text x="56" y="28" font-size="18" font-weight="700" style="fill:var(--oscuro)">Nace</text>
<text x="56" y="49" font-size="15" style="fill:var(--texto-suave)">por el menú de alta; pasos con las fases del oficio</text>
<circle cx="34" cy="104" r="8" style="fill:var(--fondo);stroke:var(--primario)" stroke-width="2"/>
<text x="56" y="102" font-size="18" font-weight="700" style="fill:var(--oscuro)">Escribe</text>
<text x="56" y="123" font-size="15" style="fill:var(--texto-suave)">nuevo: sin rama, a develop en cada vuelta</text>
<text x="56" y="142" font-size="15" style="fill:var(--texto-suave)">existente: en la rama de la tarea</text>
<circle cx="34" cy="196" r="8" style="fill:var(--fondo);stroke:var(--primario)" stroke-width="2"/>
<text x="56" y="194" font-size="18" font-weight="700" style="fill:var(--oscuro)">Se revisa</text>
<text x="56" y="215" font-size="15" style="fill:var(--texto-suave)">copia anotada; sus notas, al .md</text>
<circle cx="34" cy="280" r="8" style="fill:var(--primario);stroke:var(--primario)" stroke-width="2"/>
<text x="56" y="278" font-size="18" font-weight="700" style="fill:var(--oscuro)">Se aprueba y se cierra</text>
<text x="56" y="299" font-size="15" style="fill:var(--texto-suave)">nuevo: ya en develop; existente: por squash</text>
<text x="56" y="318" font-size="15" style="fill:var(--texto-suave)">sin observación</text>
<path d="M440 196 C 510 196 510 104 440 104" fill="none" stroke="#1f812d" stroke-width="2" marker-end="url(#fl-afinado)"/>
<text x="530" y="150" font-size="15" fill="#1f812d" text-anchor="middle" transform="rotate(-90 530 150)">afinado</text>
</svg>
<figcaption style="font-size:.82rem;text-align:center;font-style:italic;margin-top:.3rem;">El camino del repositorio depende de si el documento es nuevo o ya existe; la vuelta de afinado, no.</figcaption>
</figure>

### Nace

Entra por el menú de alta, con su tipo: especificar o documentar. Lo que falte por concretar va como pasos de la tarea.

Sus pasos siguen las fases de la skill del oficio: acordar las secciones, escribir la primera versión y afinar sobre el HTML. Cada vuelta de afinado es una iteración.

### Escribe

Escribe el subagente.

Si el documento es nuevo, trabaja sin rama de tarea. En cada vuelta, el documento se respalda, se copia a `develop`, se regenera su HTML y se ofrece abrirlo.

Si el documento ya existe, trabaja en la rama de la tarea. Al activar la rama, el panel abre los HTML que esa rama cambia.

### Solo su documento

Una documental no lleva pasos de código ni cambios en otros activos.

Si una decisión dentro de ella pide cambiar código, se registra la decisión y su aplicación va a una tarea nueva. El documento describe lo que ya es, no lo que será.

### Se revisa

El propietario anota en el HTML y guarda una copia anotada, `<nombre>.notas-<autor>.html`.

`extraer_notas.py` saca sus notas por sección, y el subagente las lleva al `.md` en la vuelta siguiente.

### Se aprueba y se cierra

El OK del propietario al documento es cerrar.

Un documento nuevo ya está en `develop`. Uno que ya existía entra por squash.

No pasa a observación.

### Los documentos compartidos

> [!aviso]
> La tarea que afecta a la metodología, la plantilla, el CLAUDE.md o «Cómo funciona…» no los cambia. Añade el paso «Reflejar «…» (N)» a la tarea «Actualizar &lt;documento&gt;».

Las tareas «Actualizar…» son documentales de un documento que ya existe. Se hacen de una en una, cada una con su subagente.

## Decidido | Lo que ya está decidido | Decidido {#decidido}

| Nº | Decisión | Qué fija aquí |
| --- | --- | --- |
| 212, 215 | Testing pasa a llamarse «En observación», sin alias ni rastros | El nombre del estado en que se vigila una tarea ya cerrada |
| 216 | Los documentos nuevos van a `develop` en cada vuelta y se ofrecen en el navegador | Sin rama para un documento nuevo; solo su documento |
| 217 | Antes de sustituir un documento, se respalda en `_respaldo/` | El respaldo en cada vuelta |
| 218 | Una tarea deliberativa da un informe y las tareas que salgan | Informe con formato de fundacional, dilemas en él, sin prueba, manejo de documental |
| 219 | El tipo de tarea decide cómo se maneja el repositorio | Los tres caminos |
| 220 | Cada cambio de un `.md` regenera su HTML | Una orden única para el HTML |
| 221 | En una deliberativa, lo que es de otra tarea se propone separar | Separar lo ajeno, y lo abierto al cerrar |
| 222 | Las deliberativas se cierran con «Finalizar deliberación» | El botón de cierre |
| 223 | Siete tipos de tarea en tres familias, para agentes especializados | Las tres familias |

## Por decidir | Lo que queda abierto, por importancia | Por decidir {#por-decidir}

Diecisiete preguntas, numeradas por importancia. Cada una lleva sus opciones y una recomendación.

La insignia de cada pregunta dice a dónde iría con las separaciones propuestas. El filtro las agrupa por destino.

::: fichas 2

### 1 · Cómo se cumple «solo su documento» {: #p1}

[Nueva](#a-nueva){: .insignia}

Hoy nada lo vigila: cualquier paso entra en la tarea, y `cerrar` integra todo lo que haya en la rama.

Opción A
:   La tarea declara su documento con una orden. La copia a `develop` solo copia ese documento. `cerrar` se niega si la rama toca otros archivos. Al anotar, el menú ofrece una tarea nueva cuando lo pedido toca otro activo.

Opción B
:   Solo la regla, escrita en la orquestación y en el encargo.

Opción C
:   Solo una comprobación por tipo al cerrar: que la rama no toque más que `.md`, HTML e imágenes.

Recomendación
:   **A.** Se cumple con un comando, no con la memoria del principal.

### 2 · Las tareas «Actualizar…» atascadas {: #p2}

[Nueva](#a-nueva){: .insignia}

Las tres acumulan 66, 45 y 29 pasos pendientes desde el 30 y el 31 de octubre. Los documentos compartidos llevan días de retraso.

Opción A
:   RELEASE avisa de las que tienen pasos pendientes. Con el principal libre, se proponen primero cuando pasan de diez pasos o de una semana.

Opción B
:   Cada tarea actualiza el documento compartido en su propia rama.

Opción C
:   Como hoy.

Recomendación
:   **A.** B trae de vuelta los choques entre ramas que se quisieron evitar.

### 3 · El subagente de un documento nuevo {: #p3}

[297](#a-297){: .insignia}

Sin rama de tarea, la recogida del subagente no funciona: el documento llega a `develop` en commits distintos de los de su rama auxiliar.

Opción A
:   Worktree desde `develop` en `sub-NN`. La recogida compara el documento con el de `develop`, no los commits.

Opción B
:   Sin worktree: el subagente escribe en una carpeta temporal y la copia lleva el documento a `develop` desde allí.

Recomendación
:   **A.** Usa lo que ya existe y solo cambia una comprobación.

### 4 · Cuándo se añade «Reflejar» {: #p4}

[Nueva](#a-nueva){: .insignia}

Hoy se añade al poner en curso la tarea de origen. Así se reflejan cosas que aún no están en `develop`, y los pasos de las tareas descartadas se quedan.

Opción A
:   Al cerrar la tarea de origen. Lo añade `cola.py cerrar`.

Opción B
:   Al empezarla, con «Esperar a «…» (N)» hasta el cierre.

Opción C
:   Como hoy.

Recomendación
:   **A.**

### 5 · Pasos de cierre de deliberativas y documentales {: #p5}

[274](#a-274){: .insignia}

Se cierran con aprobación. Falta cómo se ve eso en la cola.

Opción A
:   «Aprobar el resultado» y «Cerrar la tarea» en las dos familias. Solo cambia el botón de las deliberativas.

Opción B
:   Lo mismo, pero en las deliberativas el último paso dice «Finalizar la deliberación».

Opción C
:   Solo «Cerrar la tarea», cuyo OK es la aprobación.

Recomendación
:   **A.** Los textos de los pasos de cierre siguen fijos en `cola.py`.

### 6 · Abrir el HTML en cada vuelta {: #p6}

[297](#a-297){: .insignia}

Hoy solo lo abre «Activar rama» en el panel. Un documento nuevo no tiene rama.

Opción A
:   Lo abre la orden de copia a `develop` al terminar, y lo dice en su salida.

Opción B
:   El principal lo ofrece en cada vuelta, con una pregunta.

Recomendación
:   **A.** Se cumple sin depender de Claude.

### 7 · Pasos de decisión {: #p7}

[274](#a-274){: .insignia}

Opción A
:   `cola.py` pone «Decidir con el propietario lo que salga y registrarlo» al poner en curso una deliberativa. Al llegar el informe, ese paso se sustituye por uno por pregunta, más «Creada la tarea N para …» por cada tarea que salga.

Opción B
:   Un paso por pregunta, puesto a mano.

Opción C
:   Un solo paso genérico.

Recomendación
:   **A.** La cuenta de pasos dice cuántas preguntas faltan.

### 8 · Preguntas que dependen de otra tarea {: #p8}

[274](#a-274){: .insignia}

Opción A
:   Su paso pasa a «Esperar a «…» (N)», y se preguntan juntas.

Opción B
:   Se fusionan las dos tareas.

Opción C
:   Se decide con un supuesto, marcado como revisable.

Recomendación
:   **A.**

### 9 · Deliberativas estancadas {: #p9}

[274](#a-274){: .insignia}

Opción A
:   Si una deliberativa pasa una sesión sin decidir nada, el principal propone finalizarla y separar lo que siga abierto.

Opción B
:   Nada: lo decide el propietario cuando quiera.

Recomendación
:   **A.** Cerrar antes que abrir.

### 10 · Respaldos con el mismo nombre {: #p10}

[297](#a-297){: .insignia}

Dos vueltas con el mismo motivo darían el mismo nombre.

Opción A
:   Añadir `-2`, `-3`… solo si el nombre ya existe.

Opción B
:   Poner siempre la fecha y la hora en el nombre.

Recomendación
:   **A.** El nombre sigue siendo el de la 217.

### 11 · Búsquedas y respaldos {: #p11}

[297](#a-297){: .insignia}

La búsqueda de Claude no se salta `_respaldo/` y puede citar como vigente una versión sustituida.

Opción A
:   Un archivo `.ignore` en la raíz con `_respaldo/`. ripgrep lo respeta; git, no.

Opción B
:   Nada.

Recomendación
:   **A.**

### 12 · Qué se respalda {: #p12}

[297](#a-297){: .insignia}

Opción A
:   Solo los documentos que se reescriben enteros. Los registros (propuestas, decisiones, índice), no.

Opción B
:   Todo documento que cambie una tarea de documentos.

Recomendación
:   **A.** Los registros se editan por partes; no se sustituyen.

### 13 · Migración a sf/ {: #p13}

[Nueva](#a-nueva){: .insignia}

Los informes, las propuestas y las decisiones pasan a `sf/`. Las tareas en curso tienen sus informes en el sitio viejo.

Opción A
:   Migrar cuando no haya en curso tareas con informes o documentos de la SF. La copia a `develop` escribe en la ruta configurada.

Opción B
:   Migrar ya. Cada subagente mueve su informe al integrar `develop`.

Recomendación
:   **A.**

### 14 · Revisión con notas {: #p14}

[Nueva](#a-nueva){: .insignia}

Opción A
:   La copia anotada se guarda junto al documento y fuera de git (`*.notas-*.html` en `.gitignore`). El subagente aplica `extraer_notas.py` en la vuelta siguiente.

Opción B
:   Las notas llegan por el chat.

Recomendación
:   **A.**

### 15 · Diálogo de las skills de documentos {: #p15}

[Nueva](#a-nueva){: .insignia}

Las skills de visión y de fundacional empiezan con una conversación. La conversación la lleva el principal; el trabajo, el subagente.

Opción A
:   El subagente prepara en tanda las preguntas de cada fase, y el principal las lleva al propietario.

Opción B
:   El principal hace la fase de diálogo, con la instrucción expresa del propietario.

Recomendación
:   **A**, y B cuando el propietario lo pida.

### 16 · El encargo hasta que existan los agentes {: #p16}

[274 o agentes](#a-274){: .insignia}

Cada familia tendrá su agente, que se definirá en su propia tarea.

Opción A
:   Mientras tanto, `cola.py encargo` cambia por familia. En una deliberativa, nombra `sf:documento_fundacional`, pide la sección de lo que queda por decidir y que señale los temas ajenos. Ese texto es el punto de partida del agente.

Opción B
:   El encargo sigue igual hasta que existan los agentes.

Recomendación
:   **A.** Hoy el encargo pide «qué mirar en la prueba» también a una tarea que no se prueba.

### 17 · El panel {: #p17}

[274](#a-274){: .insignia}

Opción A
:   El tipo tras el título, como hoy, y una cuenta de decisiones sacada del historial de la tarea.

Opción B
:   Como hoy.

Opción C
:   Una sección o un color propio para las deliberativas.

Recomendación
:   **A.** C choca con la letra y el color, que dicen el estado.

:::

## Separar | Las separaciones propuestas | Separar {#separar}

El ciclo de las tareas de documentos ya es otra deliberación.

Parte de él, además, solo da forma a la orden de la tarea 297. La propuesta, con el OK del propietario:

::: tarjetas 3

### 1 · Una deliberativa nueva, con `/sf_split 274 7` {: #a-nueva}

Nace la deliberativa «Ciclo de las tareas de documentos: solo su documento, Actualizar… y revisión», con el paso 7.

Se lleva a su propio informe
:   Las preguntas [1](#p1), [2](#p2), [4](#p4), [13](#p13), [14](#p14) y [15](#p15), y el ciclo de una documental.

### 2 · Pasos «Decidir…» en la 297 {: #a-297}

En «Documentos nuevos a develop en cada vuelta, y abrirlos en el navegador» (297).

Se lleva
:   Las preguntas [3](#p3), [6](#p6), [10](#p10), [11](#p11) y [12](#p12), porque solo dan forma a su orden.

### 3 · Lo que queda en la 274 {: #a-274}

La 16 puede ir a la tarea de los agentes especializados cuando exista.

Se queda
:   Las preguntas [5](#p5), [7](#p7), [8](#p8), [9](#p9), [16](#p16) y [17](#p17).

:::

Las fases del método ya están fuera, en «Qué tipos de tarea y skills usa cada fase del método» (298).

Opción A
:   Hacer a la vez las tres primeras separaciones.

Opción B
:   Hacer solo el split.

Opción C
:   No separar.

> [!decision]
> **Recomendación: A**
> Cada tarea conserva su foco y la 274 se finaliza antes.

## Tareas | Las tareas que salen | Tareas {#tareas}

Salen cinco tareas; una ya existe, la 297.

| Tarea | Tipo | Qué hace |
| --- | --- | --- |
| Agentes especializados, uno por familia | deliberar | La pide la 223: el encargo de cada agente, sus herramientas y sus skills. |
| Aplicar las familias en `cola.py` y el panel | implementar | Los pasos de cierre por familia, «Decidir…» al poner en curso una deliberativa, el encargo por familia, el botón «Finalizar deliberación» y, si se aprueba, la cuenta de decisiones. Con sus pruebas. |
| «Documentos nuevos a develop en cada vuelta, y abrirlos en el navegador» (297) | ya existe | La orden de copia, con el respaldo, el HTML regenerado y la apertura en el navegador, más lo que se decida en sus pasos. |
| `sf:flujo_tareas` y `sf:orquestacion` | documentar | `sf:flujo_tareas` gana el apartado «Por tipo» de abajo. En `sf:orquestacion`, «Tareas de definición» y «Probar y cerrar» remiten a él, y «Fusionar, separar y redescribir» recoge la separación de temas. |
| Las «Actualizar…» de la metodología, de «Cómo funciona la Software Factory» y del CLAUDE.md | documentar | Un paso «Reflejar» en cada una. |

> [!aviso]
> El CLAUDE.md dice que las «Actualizar…» se hacen «en el principal»; lo vigente es que cada una tiene su subagente.

### Texto propuesto para `sf:flujo_tareas` (apartado «Por tipo»)

> **Por tipo.** Los siete tipos forman tres familias. La familia decide cómo se maneja el repositorio, cómo se cierra la tarea y qué agente la trabaja.
>
> - **Código** (implementar, corregir): rama de la tarea, worktree del subagente, squash en `develop` y observación. Pasos de cierre «Activar rama para poder probar» y «Cerrar la tarea».
> - **Deliberativas** (investigar, deliberar, diseñar): dialogan, deciden y separan temas. Su único documento es un informe con el formato de los fundacionales. Su sección de lo que queda por decidir lleva una pregunta por decisión, con opciones, pros y contras, recomendación y de qué depende, al día con cada respuesta. Lo que haya que aplicar lo hacen las tareas que crean. Lo que es de otra tarea se propone separar en cuanto aparece; al cerrar, lo abierto sale a su tarea. En el panel se cierran con «Finalizar deliberación».
> - **Documentales** (especificar, documentar): escriben un documento acordado y solo tocan ese documento.
>
> Deliberativas y documentales comparten el manejo del repositorio. Un documento nuevo va sin rama: en cada vuelta se respalda la versión anterior en `_respaldo/`, se copia a `develop`, se regenera su HTML y se ofrece abrirlo. Uno que ya existe se cambia en su rama y entra por squash. Se cierran con la aprobación del propietario, sin observación: pasos de cierre «Aprobar el resultado» y «Cerrar la tarea».
