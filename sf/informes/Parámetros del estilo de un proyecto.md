---
antetitulo: Software Factory · Informe de diseño · Noviembre 2026
lema: Un archivo de estilo por proyecto; // lo que falta es lo de hoy, lo nuevo es un parámetro.
subtitulo: Qué parámetros forman el estilo de un proyecto, con sus valores, su valor por defecto y su efecto; dónde se guardan y cómo los lee el generador; cómo se registra cada afinado y cómo entra un parámetro nuevo.
version: Versión 1.1 · 06/11/2026
estado: Decidido · Tarea 387
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de diseño
pie: Informe de la tarea «Diseñar los parámetros del estilo de un proyecto y dónde se guardan» (387), que sale del informe «Un estilo de documentos por proyecto» (385, decisiones 305 a 315). Parte de tema_identidad.py, documento_a_html.py, los temas de crear_documentos, los identidad.json de la SF, SpriteAnimation, SmartColdBox, LecturaFàcil, MedRol y SocratIX, y la web de la SF, leídos sin cambiarlos. Lo decidió el propietario de la Software Factory (decisiones 316 a 324).
---
# Parámetros del estilo de un proyecto: qué lleva, dónde vive y cómo evoluciona

## Resumen | Un archivo, nueve grupos, lo de hoy por defecto | Resumen {#resumen}

El estilo de un proyecto va en **`docs/identidad/estilo.json`**: nueve grupos de parámetros con todos los valores resueltos, la referencia a los archivos del logo, una versión y un historial. Lo escribe solo la skill de estilo y lo leen el generador, la infografía, la web y la sesión. **El valor por defecto de cada parámetro es lo que el generador hace hoy**: sin el parámetro, nada cambia. Pulsa cada grupo para ver sus parámetros.

![](diagramas/estilo-parametros.diagrama)

Las **nueve preguntas están decididas** (decisiones 316 a 324) y no queda ninguna abierta: cinco como se recomendaba, dos con un matiz (el logo en `estilo.json`; el contraste, que se revisará con la práctica) y dos de otra forma. Sin `estilo.json`, el generador sale del paso con los valores por defecto de un tema elegido por el color del proyecto. Un parámetro pedido desde otro proyecto se dice en una línea y se ofrece una issue en GitHub de la SF, sin anotarlo en su estilo. Ninguna tarea nueva: lo diseñado se reparte en pasos de las tareas que ya salieron del informe de partida.

[Ver las 9 decisiones](#decidido){: .salto} [Ver las preguntas respondidas](#por-decidir){: .salto} [Ver los pasos para las tareas](#tareas){: .salto}

## Dónde vive | Quién lo escribe y quién lo lee | Dónde vive {#donde}

![](diagramas/estilo-donde.diagrama)

> **Por qué no `sf/`**
> `sf/` es de los documentos de la SF (propuestas, decisiones, informes). El estilo es identidad del proyecto y lo leen piezas que no son documentos (la infografía, la web, la sesión), como ya decía la decisión «Fuente de las skills en la SF y lo propio de cada proyecto en `docs/identidad/`» (7).

Sin `estilo.json`, el generador sale del paso con los valores por defecto de un tema, que se puede elegir por el color del proyecto en su identidad, y avisa una vez ([pregunta 8](#p8)): fijar el estilo no bloquea tocar un documento (309).

### Lo que hoy fija cada uno por su cuenta {: #hoy}

| Hoy | Dónde | Pasa a |
| --- | --- | --- |
| `tema`, `logo`, `producto` | `identidad.json` | `estilo.json`: colores, letra, forma e identidad, con la referencia a los archivos del logo ([pregunta 1](#p1)) |
| `cabecera`, `etiqueta`, `marcador`, `esquinas`, `opacidad` | `estilo` del tema | `portada.fondo`, `secciones.*`, `pagina.esquinas` |
| `destino`, `herramientas` | `identidad.json` o cabecera del `.md` | `lectura.*` del estilo, y el documento puede cambiarlas ([pregunta 3](#p3)) |
| `portada: oscura`, `menu: secciones` | cabecera de cada `.md` | `portada.forma` en el estilo; `menu`, como `destino` |
| `tipo: Documento de visión` | `identidad.json` | Se retira: lo da el perfil del tipo o la cabecera |
| `codigo.css` (SpriteAnimation) | `css` de la identidad | `pagina.codigo`: bloque con filete por defecto, con el coloreado de «Completar el generador único…» (389) |
| `cabecera.css` (SpriteAnimation) | `css` de la identidad | Enlace ilegible en portada oscura: **arreglo** del generador; el enlace al repositorio, `identidad.enlace` |
| `modo-claro.js` (SpriteAnimation) | `js` de la identidad | Sobra: el kit ya abre siempre en claro; se quita en una sesión de ese proyecto |
| `paleta.md` (SmartColdBox): significado, oscuro, HUD | texto de la identidad | `significado`, `colores-oscuro` y `aparte.hud` |
| Calculadora, `componentes.css` | `css` y `js` de la identidad | **Se quedan** en `identidad.json`, con las variables del estilo (313) |

### Un primario claro, como el amarillo de la SF {: #amarillo}

El amarillo de la web (`oklch(0.83 0.155 86)`) no da 4,5:1 ni con texto blanco encima ni como texto sobre papel: la web ya lo separa en `--accent`, `--on-accent` y `--accent-ink`. Hoy el generador usa `primario` para las tres cosas. Por eso el grupo Colores añade **`sobre-primario`** y **`primario-texto`** ([pregunta 4](#p4)); el color de sesión sale del `primario`, el de marca.

## Afinado | Cómo cambia el estilo y cómo entra un parámetro | Afinado {#afinado}

![](diagramas/estilo-afinado.diagrama)

El historial va dentro de `estilo.json`, una línea por versión, y la versión anterior a `_respaldo/` ([pregunta 7](#p7)), y el pie de cada documento cita la versión del estilo con que se generó. Como el generador es determinista, las muestras no se guardan: se rehacen con la versión y el documento de muestra.

```json
{
  "version": 3,
  "origen": "colorido",
  "historial": [
    {"version": 1, "fecha": "2026-11-10", "cambio": "estilo de partida", "motivo": "muestra B"},
    {"version": 2, "fecha": "2026-11-12", "cambio": "secciones.etiqueta: solida, opacidad 0.4", "motivo": "títulos más visibles"},
    {"version": 3, "fecha": "2026-11-20", "cambio": "pagina.codigo: bloque", "motivo": "código más legible"}
  ],
  "identidad": {"producto": "SoftwareFactory", "logo": "logo.svg", "logo-oscuro": "logo-oscuro.svg"},
  "colores": {"primario": "#…", "sobre-primario": "#…", "primario-texto": "#…"},
  "letra": {"titulos": "'Outfit', 'DM Sans', sans-serif", "tamano": 17},
  "portada": {"forma": "oscura"},
  "secciones": {"cabecera": "numero-etiqueta", "etiqueta": "solida", "opacidad": 0.4, "marcador": "ninguno"},
  "pagina": {"esquinas": 16},
  "lectura": {"destino": "proyecto", "menu": "secciones"}
}
```

El ejemplo es la forma, no el estilo de la SF: sus valores los fija «Diseñar con el propietario las muestras de estilo…» (388).

Un parámetro que pide otro proyecto no se anota en su estilo: Claude dice en una línea que es de la SF y ofrece abrir una issue en el repositorio de GitHub de la SF con lo que se pide ([pregunta 9](#p9)). Los desarrolladores de otros proyectos solo tienen el plugin: una anotación en su historial no llegaría a nadie; la issue, sí.

## Decidido | Lo que ya fija el diseño | Decidido {#decidido}

| Nº | Decisión | Qué fija aquí |
| --- | --- | --- |
| 316 | El estilo del proyecto se guarda en `docs/identidad/estilo.json`, con la referencia a los archivos de su logo | El sitio del archivo y `identidad.logo` ([pregunta 1](#p1)) |
| 317 | `estilo.json` guarda los valores resueltos; el tema del catálogo es solo la muestra de partida | `origen`, solo informativo ([pregunta 2](#p2)) |
| 318 | El aspecto lo fija solo el estilo; cada documento fija cómo se lee | Grupo Lectura en el documento; aviso y conversor para el aspecto ([pregunta 3](#p3)) |
| 319 | Dos roles de color para un primario claro: `sobre-primario` y `primario-texto` | Grupo Colores ([pregunta 4](#p4)) |
| 320 | El generador se detiene con un texto por debajo de 4,5:1 y avisa con un borde o una línea | La validación del generador; se revisará con la práctica ([pregunta 5](#p5)) |
| 321 | La forma de la cabecera de sección es un parámetro del estilo | `secciones.cabecera` ([pregunta 6](#p6)) |
| 322 | Cada afinado del estilo sube su versión, se anota en su historial y respalda la anterior | `version`, `historial`, `_respaldo/` y el pie ([pregunta 7](#p7)) |
| 323 | Un proyecto sin `estilo.json` se genera con los valores por defecto de un tema elegido por su color | Sin estilo, sin bloqueo ([pregunta 8](#p8)) |
| 324 | Un parámetro de estilo que pide otro proyecto se dice en una línea y se ofrece abrir una issue en GitHub de la SF | Nada se anota en el estilo del proyecto ([pregunta 9](#p9)) |
| 305 | Un solo generador determinista con el estilo del proyecto; una skill ayuda a fijar sus parámetros con muestras y afinado | Lo escribe solo la skill; las muestras, el generador; parámetros nuevos, no excepciones |
| 306 | Las secciones sin etiqueta salen con número y título hasta que el estilo del proyecto diga otra cosa | La regla del valor por defecto sin etiqueta (321) |
| 307 | Los diagramas toman el estilo del documento; tinta, en el selector y en páginas sueltas | Grupo Diagramas |
| 309 | Cada documento se migra al generador único cuando se vuelve a tocar | Un estilo nuevo llega a cada documento al regenerarlo |
| 310 | El color de sesión se deriva del color primario del estilo del proyecto | Derivado de `colores.primario`, no se guarda |
| 312 | La web comercial comparte los colores y la letra del estilo de la SF, con su propia forma de página | Grupo Infografía y web |
| 313 | El logo y el producto forman parte del estilo; los componentes propios van al lado y usan sus variables | Grupo Identidad; `identidad.json` para los componentes |
| 315 | La infografía técnica se puede incrustar como cualquier recurso o ir como pieza aparte | Grupo Infografía y web |
| 7 | Fuente de las skills en la SF y lo propio de cada proyecto en `docs/identidad/` | El sitio del archivo |
| 183 | El generador de documentos no elige por el autor | `destino` y `herramientas` sin valor por defecto |
| 217 | Antes de sustituir un documento, se respalda en `_respaldo/` | También `estilo.json` |

## Preguntas | Nueve preguntas, decididas | Preguntas {#por-decidir}

::: preguntas 2 plegables

### 1 · Dónde se guarda el estilo {recomendada=A estado=decidida elegida=A} {: #p1}

Hoy el tema va en `identidad.json` (nombre o archivo) junto a los componentes y las reglas.

Opción A
:   `docs/identidad/estilo.json`, aparte; `identidad.json` queda para componentes, iconos y reglas.

Opción B
:   Un bloque `estilo` dentro de `identidad.json`.

Opción C
:   `sf/estilo.json`, con los documentos de la SF.

Recomendación
:   **A.** Separa lo que fija la skill de lo que no (313) y lo pueden leer la infografía y la web sin lo demás.

Decisión
:   **A**, y además `estilo.json` guarda la referencia al archivo o los archivos del logo (316).

### 2 · Valores resueltos o tema de referencia {recomendada=A estado=decidida elegida=A} {: #p2}

Hoy `"tema": "pool"` apunta al catálogo del plugin: si el plugin cambia el tema, cambian los documentos del proyecto.

Opción A
:   `estilo.json` guarda todos los valores resueltos; el tema del catálogo es solo la muestra de partida (`origen`).

Opción B
:   `base: pool` más los cambios del proyecto.

Recomendación
:   **A.** El estilo es del proyecto: una actualización del plugin no lo cambia sin una vuelta de afinado.

Decisión
:   **A** (317).

### 3 · Qué puede fijar un documento por su cuenta {recomendada=A estado=decidida elegida=A} {: #p3}

Hoy cada `.md` pone `portada`, `menu`, `destino` y `herramientas` en su cabecera.

Opción A
:   El aspecto, solo en el estilo (el generador avisa y el conversor quita la clave al migrar); la lectura (`destino`, `herramientas`, `menu`), en el documento, con el valor del estilo por defecto.

Opción B
:   Todo en el estilo; el documento no fija nada.

Opción C
:   El documento puede cambiar cualquier parámetro.

Recomendación
:   **A.** Un solo aspecto por proyecto, y cada documento sigue diciendo para quién es (183).

Decisión
:   **A** (318).

### 4 · Roles para un primario claro {recomendada=A estado=decidida elegida=A} {: #p4}

El amarillo de la SF no da 4,5:1 con texto encima ni como texto ([Un primario claro](#amarillo)).

Opción A
:   Dos roles nuevos, `sobre-primario` y `primario-texto`, derivados si faltan y fijables.

Opción B
:   Exigir que el primario dé 4,5:1; el amarillo iría como acento y el primario sería otro color.

Recomendación
:   **A.** Permite un primario de marca claro, como hace la web, sin cambiar ningún tema de hoy.

Decisión
:   **A** (319).

### 5 · Qué hace el generador con un contraste bajo {recomendada=A estado=decidida elegida=A} {: #p5}

Hoy el tema azul de la SF da 2,54:1 en `texto-tenue` y 2,43:1 en el borde de las cajas.

Opción A
:   Se detiene si un texto baja de 4,5:1 (3:1 el grande); avisa si es un borde o una línea.

Opción B
:   Solo avisa.

Recomendación
:   **A.** El contraste es calidad de la salida, y el generador la garantiza (305).

Decisión
:   **A**; se revisará con la práctica (320).

### 6 · La forma de sección que sustituye a la 306 {recomendada=A estado=decidida elegida=A} {: #p6}

Opción A
:   Un parámetro, `secciones.cabecera` (`numero-etiqueta`, `numero-titulo` o `titulo`), por defecto `numero-etiqueta`; la 306 es la regla de ese valor sin etiqueta, y cada proyecto elige con las muestras.

Opción B
:   `numero-titulo` en todos los proyectos, sin parámetro.

Recomendación
:   **A.** Es preferencia de aspecto, la de este informe en la SF, y no reescribe ningún documento.

Decisión
:   **A** (321).

### 7 · Cómo se registra cada afinado {recomendada=A estado=decidida elegida=A} {: #p7}

Opción A
:   `version` e `historial` dentro de `estilo.json`, una línea por vuelta, y la versión anterior en `_respaldo/`.

Opción B
:   Solo el historial de git.

Opción C
:   Un `estilo-historial.md` aparte.

Recomendación
:   **A.** Se lee junto al estilo, lo escribe la misma orden y el pie de cada documento cita su versión.

Decisión
:   **A** (322).

### 8 · Un proyecto sin `estilo.json` {recomendada=A estado=decidida elegida=C} {: #p8}

Hoy seis proyectos tienen `identidad.json` y ninguno tiene estilo.

Opción A
:   El generador compone un estilo implícito con `identidad.json` y su tema, genera como hoy y avisa una vez; sin nada, se detiene y propone la skill.

Opción B
:   Se detiene siempre hasta fijar el estilo con la skill.

Opción C
:   El generador sale del paso con los valores por defecto de un tema, que se puede elegir por el color del proyecto en su identidad, y avisa una vez.

Recomendación
:   **A.** Sin migración en bloque (309): fijar el estilo no bloquea tocar un documento.

Decisión
:   **C**, la del propietario: sin `estilo.json`, los valores por defecto de un tema, elegido si se quiere por el color del proyecto, y un aviso (323).

### 9 · Un parámetro pedido desde otro proyecto {recomendada=A estado=decidida elegida=B} {: #p9}

Ningún proyecto escribe en la SF («Automejora durante el uso de la SF»).

Opción A
:   Claude dice en una línea que es de la SF y el historial del estilo anota «pedido a la SF»; el propietario lo lleva a una sesión de la SF.

Opción B
:   Solo la línea, sin anotarlo.

Recomendación
:   **A.** El proyecto recuerda lo que pidió sin escribir en la SF, y el afinado se retoma cuando llegue el parámetro.

Decisión
:   **B, con issue**: Claude dice en una línea que es de la SF y ofrece abrir una issue en el repositorio de GitHub de la SF con lo que se pide; no se anota en el estilo del proyecto. Los desarrolladores de otros proyectos solo tienen el plugin, no el proyecto de la SF (324).

:::

## Tareas | Pasos para las tareas que ya existen | Tareas {#tareas}

No sale ninguna tarea nueva. Con las respuestas (decisiones 316 a 324), estos pasos van a las tareas que salieron del informe de partida; el de la issue en GitHub de la SF (324) ya está anotado en «Construir la skill…» (392):

| Tarea | Paso que se añade |
| --- | --- |
| Diseñar con el propietario las muestras de estilo y el estilo de partida de la SF (388) | Muestras de estilo como juegos completos de valores de `estilo.json`, con su tema de origen (317) |
| Diseñar con el propietario las muestras de estilo y el estilo de partida de la SF (388) | Estilo de partida de la SF con `primario`, `sobre-primario` y `primario-texto` del amarillo (319) |
| Diseñar con el propietario las muestras de estilo y el estilo de partida de la SF (388) | Archivos del logo de la SF citados en su `estilo.json` (316) |
| Diseñar con el propietario las muestras de estilo y el estilo de partida de la SF (388) | Forma de la cabecera de sección de la SF elegida con las muestras (321) |
| Completar el generador único con lo que solo tiene la visión (389) | Leer `docs/identidad/estilo.json` con los nueve grupos, cada parámetro con su valor por defecto de hoy (316, 317) |
| Completar el generador único con lo que solo tiene la visión (389) | Logo de la portada desde los archivos que cita `estilo.json` (316) |
| Completar el generador único con lo que solo tiene la visión (389) | Aviso si un `.md` fija el aspecto en su cabecera, y el conversor quita la clave al migrarlo (318) |
| Completar el generador único con lo que solo tiene la visión (389) | Roles `sobre-primario` y `primario-texto`, derivados si faltan (319) |
| Completar el generador único con lo que solo tiene la visión (389) | Parada con un texto por debajo de 4,5:1 (3:1 el grande) y aviso con un borde o una línea (320) |
| Completar el generador único con lo que solo tiene la visión (389) | Parámetro `secciones.cabecera`: `numero-etiqueta`, `numero-titulo` y `titulo` (321) |
| Completar el generador único con lo que solo tiene la visión (389) | Versión del estilo en el pie de cada documento (322) |
| Completar el generador único con lo que solo tiene la visión (389) | Sin `estilo.json`, los valores por defecto de un tema elegido por el color del proyecto, con un aviso (323) |
| Completar el generador único con lo que solo tiene la visión (389) | Enlace legible en la portada oscura, como arreglo del generador |
| Construir la skill que fija los parámetros del estilo con muestras y afinado (392) | `estilo.json` con todos los valores resueltos y el tema de partida solo como `origen` (317) |
| Construir la skill que fija los parámetros del estilo con muestras y afinado (392) | Versión, historial y respaldo en `_respaldo/` en cada afinado (322) |
| Construir la skill que fija los parámetros del estilo con muestras y afinado (392) | Valores en prueba fuera de `estilo.json` hasta aceptarlos |
| Construir la skill que fija los parámetros del estilo con muestras y afinado (392) | Arreglo del generador o parámetro nuevo, según la petición |
| Derivar el color de sesión del primario del estilo del proyecto (393) | Primario desde `colores.primario` de `estilo.json`, o desde el tema por defecto si falta (310, 323) |
| Que la infografía técnica tome el estilo del proyecto… (394) | Colores, Letra e Infografía y web (`escenario`, `hud`) desde `estilo.json`, o desde el tema por defecto si falta (315, 323) |
| Que la web comercial tome los colores y la letra del estilo de la SF (395) | Solo Colores y Letra desde el `estilo.json` de la SF (312) |
| Actualizar Cómo funciona la Software Factory (313) | `docs/identidad/estilo.json` junto a `identidad.json`, cuando estén hechos el generador y la skill de estilo (316 a 324) |

En los proyectos, en una sesión abierta en cada uno: SpriteAnimation quita `modo-claro.js`, y `codigo.css` y `cabecera.css` cuando su generador tenga `pagina.codigo` y el arreglo de la portada.
