---
antetitulo: Software Factory · Informe de investigación · Noviembre 2026
lema: Las 25 cajas caben y pasan el comprobador; // leerlas con fluidez pide las reglas del original.
subtitulo: Cómo queda con la skill de diagramas el flujo de audio de LupDub hecho a mano, qué reglas de lectura salen del original, cómo se afinó en rondas y qué le falta a la skill.
version: Versión 1.3 · 06/11/2026
estado: Decidido · Tarea 398
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas diagramas
menu: secciones
tipo: Informe de investigación
pie: Informe de la tarea «Probar la skill de diagramas con el flujo de audio de LupDub en un informe» (398). Parte del diagrama a mano «Flujo de audio LupDub v2», leído sin cambiarlo, y de la skill diagramas de develop. Decidido por el propietario de la Software Factory (decisiones 325 y 326).
---
# Prueba de diagramas: el flujo de audio de LupDub

## Resumen | Las 25 cajas, en cinco zonas | Resumen {#resumen}

El flujo de audio de LupDub, rehecho con el generador de la skill con todas las cajas del original: 25, en arquitectura vertical, con las zonas Acciones, Control, Motor (voces, y mezcla y cadena) y Escucha, dos cajas por fila, plegadas por defecto y con la cadena en serpentina. Cada caja abre su ficha con el texto y el código del original; el foco está en Captación, donde entran las dos voces nuevas.

![](diagramas/flujo-audio-lupdub.diagrama)

Pasa el comprobador, pero no se lee con la fluidez del original: la cadena va en serpentina, las flechas comparten la calle central y la vuelta del reloj cruza el dibujo entero. Del original salen dieciocho reglas de lectura, desde la primera: qué concepto fluye (aquí, el audio) y que su recorrido se cuente de principio a fin; aplicadas a mano en cinco rondas, la mejor disposición (el eje en una columna con las entradas al lado) choca con dos fallos del generador. La orientación horizontal no existe para esta figura y la herramienta no lo dice.

El propietario de la Software Factory ha decidido las dos preguntas: las nueve propuestas salen en una sola tarea con rama (401), y los flujos con entradas laterales se dibujan con el eje en una columna y cada entrada frente a su destino. No queda ninguna abierta.

[Ver las rondas](#rondas){: .salto} [Ver las reglas](#reglas){: .salto} [Ver las propuestas](#propuestas){: .salto} [Ver lo decidido](#decidido){: .salto} [Ver la tarea](#tareas){: .salto}

## Comparación | El original frente al nuevo, con las mismas cajas | Comparación {#comparacion}

El original es un diagrama de bloques de 778 × 1446, al 80 % y con zoom: dentro del recuadro Motor, el control arriba en violeta discontinuo, la cadena en una columna con cuatro mezcladores y las voces a su derecha, cada una frente a su mezclador; debajo, la escucha web, y tres acciones del usuario en círculos rosas con flechas punteadas a lo que cambian. Su ficha sale en una hoja abajo, con tipo, ruta del código y texto.

| Aspecto | Original a mano | Con la skill |
| --- | --- | --- |
| Tamaño | 778 × 1446; zoom con botones o pellizco | 400 × 1873 plegado (1999 desplegado); a 375, sin zoom |
| Flechas | 36 trazos, 9 codos; la señal, 13 tramos rectos de 24 | 28 flechas, 35 codos, 5565 de tramo compartido |
| Cadena | Una columna; cada voz frente a su mezclador | Dos por fila, en serpentina; las voces, en su zona encima |
| Zonas | Motor, que contiene control, cadena y voces; escucha | Cinco hermanas, sin anidar |
| Acciones | Círculos con flecha punteada a lo que cambian | Cajas en su zona, con flecha morada discontinua |
| Vacío o previsto | Discontinuo y atenuado | Discontinuo, con la clase `externo` |
| Horizontal | No tiene | No la hay (1396 > 960); elegirla en la herramienta no hace nada |
| Comprobación | Ninguna | Solapes, contraste, letra y accesibilidad a 375 y 1440 |

Se gana lectura en el móvil sin zoom, las fichas junto al nodo, el recorrido resaltado, los ajustes comunes y la comprobación automática. Se pierde la columna vertebral, cada entrada frente a su destino y el bus del control: lo que hace fluida la lectura del original.

## Rondas | El afinado a mano, en cinco rondas | Rondas {#rondas}

Cada ronda: generar, medir (longitud, codos y tramo compartido de las flechas, con el comprobador), mirar la captura y contestar cómo lo lee un lector nuevo y dónde se atasca; el atasco decide el cambio siguiente.

| Ronda | Cambio | Medidas | Cómo se lee y dónde se atasca |
| --- | --- | --- | --- |
| 0 · v1.1 | Arquitectura, cinco zonas | 7892 de largo, 42 codos, 5522 compartido; 0 errores | Fluye el audio, pero su recorrido se pierde en el zigzag y entre las líneas de la calle central |
| 1 | Tres zonas (Control, Motor, Escucha), para que quepa la horizontal | Sin figura: el generador dice que no hay sitio para «PIDE 128» | No llega a dibujarse |
| 2 | Tipo proceso: el eje en una columna y las voces y acciones al lado, como el original | 3594 de largo, 2 codos, 0 compartido; 4 errores | Se lee de arriba abajo de un tirón; se atasca en las entradas, cuyas flechas llegan 14 por debajo de su caja, y «Grabar» se sale de su zona |
| 3 | Arquitectura con la cadena en serpentina (orden de la zona) | Igual que la ronda 0: el orden de la zona no cuenta | Sin cambio |
| 4 · v1.2 | La serpentina, en el orden de los nodos | 7794 de largo, 35 codos, 5565 compartido; 0 errores | El audio baja por la cadena sin saltos en Z; se atasca aún en la calle central y en la vuelta del reloj |

La ronda 2 es la que mejor se lee y la que más se parece al original, pero no se puede entregar: sus flechas laterales no tocan su destino (el comprobador no lo ve) y una caja lateral se sale de su zona. La ronda 1 habría dado la horizontal (unos 840 de ancho). En la ronda 3, el orden de una zona no cambió nada: manda el orden en que se declaran los nodos. La ronda 4 es la figura de esta versión.

## Reglas | Reglas que salen del original | Reglas {#reglas}

> **Criterio rector**
> ¿Lo entenderá de forma fluida un lector nuevo, organizado así? Lo que fluye no es una flecha sino un concepto (aquí, el audio; en otros, un estado, una petición, un dato); seguir el flujo es contar su vida de principio a fin sin perderse. Las medidas sirven a esa pregunta, no la sustituyen.

Preguntas de cada ronda, en este orden, contestadas por Claude en una o dos frases cada una; el atasco decide el cambio siguiente:

1. ¿Qué concepto fluye?
2. ¿Se entiende su recorrido con fluidez, de principio a fin? ¿Dónde se atasca un lector nuevo?
3. ¿Van las áreas funcionales una tras otra, con sus conexiones claras?
4. ¿Qué hay que destacar?
5. ¿Qué información no aporta?
6. ¿Queda oculto algo clave?
7. ¿Es un enredo o se sigue con facilidad?
8. ¿Qué dinamismo ayuda a la idea clave?
9. ¿Quedan cruces que evitar?

Las reglas siguen el mismo orden.

::: tarjetas 2 plegables

### El concepto que fluye y su recorrido {color=turquesa icono=rama}

Qué fluye
:   Antes de colocar nada, se nombra el concepto que fluye; aquí, la señal de audio, de las voces al altavoz. Las flechas que lo llevan se marcan en los datos (una clase `flujo`) y son las principales; las de control y las acciones, secundarias, con otro trazo. Medida: cada figura declara su concepto y sus flechas de flujo; ninguna secundaria con el estilo de flujo.

Columna vertebral
:   El recorrido del concepto, en una columna y en el orden de la historia, de arriba abajo. El ojo baja sin buscar. Medida: saltos de columna, codos y flechas que suben en las flechas de flujo, cero (original: 13 tramos rectos de 24).

Áreas, las etapas del concepto
:   Las zonas son las etapas por las que pasa (control que lo prepara, motor que lo produce, escucha que lo entrega) y se apilan en ese orden; el lector entiende una entera antes de la siguiente. Medida: el orden de las zonas es el del primer nodo del camino que contienen; todas las flechas internas, dentro de su zona.

Pocos puentes, en la frontera
:   Entre dos áreas, pocas conexiones, juntas en la frontera y con etiqueta. Medida: flechas entre zonas por frontera (dos como mucho, salvo un bus); ningún tramo dentro de una zona ajena (original: «1 × 128 · 4 kHz · fin del motor»).

### Vista y desplazamiento {color=turquesa icono=lupa}

La historia avanza con el scroll
:   Nada obliga a volver hacia arriba salvo las vueltas, que se ven como vueltas. Medida: flechas que suben sin ser vuelta, cero.

Origen y destino a la vista
:   Una flecha se sigue sin perder su origen. Medida: largo de cada flecha en pantallas a 375 y a 1440; una o menos, salvo vueltas.

Vueltas por fuera
:   La vuelta va por el carril más exterior, discontinua, una por carril: se lee como excepción sin cortar la columna. Medida: ningún trazo entre su carril y el borde.

### Destacar y quitar {color=verde icono=check}

Un foco, lo que el lector debe llevarse
:   Lo nuevo o lo que cambia, con borde de acento; la cadena principal, con el color del camino. Medida: un foco, dos como mucho; ningún otro recurso de realce.

Nada que no aporte
:   Cada etiqueta dice algo que la flecha no dice ya; lo que no ayuda a seguir el flujo va a la ficha. Medida: etiquetas que repiten el nombre del destino, cero; detalle de una caja plegada, en una línea.

Lo clave, sin pulsar
:   Lo que hay que entender se ve sin abrir fichas: no al final del scroll, ni en una caja pequeña, ni tapado por flechas. Medida: el foco y los nombres del camino, visibles con todo plegado.

### Flechas sin enredo {color=frambuesa icono=aviso}

Cada entrada frente a su destino
:   Lo que alimenta un paso va en la columna de al lado, a su altura: flecha recta y corta (original: voces a mezcladores, 44). Medida: diferencia de altura de cuatro o menos, sin codos.

Columnas por papel
:   Control, entradas, camino y acciones, cada uno en su columna; las flechas, solo entre vecinas. Medida: flechas que cruzan una columna, cero.

Reparto en bus
:   Un origen con tres destinos o más, un tronco y ramas cortas (original: la cola a las voces). Medida: tramos paralelos a menos de 12 de orígenes distintos, cero; el bus cuenta como uno.

¿Enredo o se sigue?
:   Si para seguir una flecha hay que buscarla entre otras, es un enredo. Medida: tramo compartido, flechas con más de dos codos y líneas por franja de 100.

### Forma, ritmo y dinamismo {color=naranja icono=documento}

Acciones y previsto con su forma
:   Las acciones, fuera del camino, con forma propia y flecha a lo que cambian (un nodo o el corchete de un tramo); lo previsto, discontinuo y atenuado. Medida: clase propia y estilo comprobado.

Ritmo compacto
:   Cajas del camino de un alto y un paso constantes (original: 42 y 70), nombre en una línea; el blanco, entre áreas. Medida: desviación del paso, cero.

Un dinamismo, al servicio de la idea
:   Uno principal, nunca decorativo, con teclado y sin movimiento si se pide menos. Aquí ayuda recorrer la señal paso a paso por la cadena y el resaltado del recorrido, que la skill ya tiene; el pulso animado por las flechas distrae.

Y, al final, evitar cruces
:   Con lo anterior resuelto, se quitan los cruces que queden; si uno no se puede evitar, un puente. Medida: cruces entre flechas y flechas que pasan por una caja ajena, cero.

:::

## Propuestas | Lo que faltó, no cuadró o hubo que forzar | Propuestas {#propuestas}

Cada propuesta es un paso posible de una tarea con rama sobre la skill. Las seis primeras salen de dibujar el diagrama completo y de las rondas; las demás, de recursos que el original tenía y la skill no.

::: tarjetas 3 plegables

### Bucle de afinado con Claude {color=frambuesa icono=dialogo}

Los datos marcan las flechas que llevan el concepto (clase `flujo`, distinta de `principal`, que solo colorea) y el generador coloca su recorrido como columna. El generador, determinista, mide (cruces, calles compartidas, codos, largo, flechas que suben, largo en pantallas, puentes entre áreas, etiquetas lejos) y Claude mira la captura y las medidas, contesta las preguntas de revisión y decide el cambio en los datos; se repite hasta que no mejora o tras tres rondas. Sustituye a probar todas las permutaciones: con una zona de seis nodos, 4,5 minutos por figura; con siete, más de diez sin terminar.

### Orientación horizontal {color=frambuesa icono=aviso}

Si la horizontal no cabe en 960, el generador no la emite y «Horizontal» en la herramienta no hace nada, sin aviso. Paso: emitirla siempre (con desplazamiento o escalada), o que la herramienta desactive la opción y diga «no cabe en horizontal a este ancho».

### Eje con entradas laterales {color=frambuesa icono=aviso}

En el proceso, una caja lateral va 52 por debajo de su origen y su flecha al eje llega por debajo de la caja de destino; la que va al último paso se sale de su zona. Paso: entradas a la altura de su destino, la zona que las contiene y que el comprobador vea una flecha que no toca su caja.

### El presupuesto, una recomendación {color=frambuesa icono=aviso}

Con 25 nodos y 28 flechas, el generador avisa «¿Dos diagramas?». Cuando el diagrama tiene que ser completo, el límite debe ser una recomendación, no una regla. Paso: decirlo así en la skill y en `tipos.md`, y una opción `completo` que deja el aviso en informativo.

### Orden y compacidad {color=frambuesa icono=aviso}

El orden de una zona no manda: manda el de los nodos. Plegado, el dibujo baja un 6 %. Paso: respetar el orden de la zona, serpentina para las cadenas y plegadas de 32 a 40 de alto, tres por fila.

### Etiquetas, calles y puentes {color=frambuesa icono=aviso}

«PIDE 128» queda lejos de su tramo, varias flechas bajan juntas por la calle central y otras atraviesan zonas ajenas, y una etiqueta larga impide dibujar la figura. Paso: la etiqueta junto a su origen, una calle por flecha, reparto en bus y los puentes en la frontera, medidos por el comprobador.

### Zonas anidadas, corchetes y formas {color=turquesa icono=carpeta}

Paso: una zona dentro de otra (el Motor del original); un corchete lateral para un tramo; una clase `accion` con su forma; una clase `previsto`, discontinua y atenuada, en lugar de forzar `externo`.

### Dinamismo para la idea clave {color=turquesa icono=rama}

Paso: un modo «recorrer» que avanza el foco por el camino principal con ← y →, con su ficha, sin animación con movimiento reducido; un modo «solo lo nuevo»; áreas que se pliegan a su nombre.

### Ficha, sintaxis y kit {color=naranja icono=codigo}

Paso: el chip como tipo en la ficha y una línea `codigo:` en mono; aceptar `a > b | marca` y marcas separadas por espacio; en el kit, «Vale para las figura del documento» en singular.

:::

## Decidido | Lo que ya está decidido | Decidido {#decidido}

| Nº | Decisión | Qué fija aquí |
| --- | --- | --- |
| 325 | Las nueve propuestas de la prueba de diagramas, en una sola tarea | Una tarea con rama (401) con las nueve [propuestas](#propuestas), en el orden de la [pregunta 1](#p1) |
| 326 | Flujos con entradas laterales: eje en columna y cada entrada frente a su destino | La disposición base de la [pregunta 2](#p2); chip para las entradas menores |

## Por decidir | Qué hacer con las reglas y las propuestas | Por decidir {#por-decidir}

Las dos preguntas, ya decididas: qué tarea sale, y qué disposición se toma como base para un flujo como este.

::: preguntas 2

### 1 · Qué tarea sale {estado=decidida recomendada=A elegida=A} {: #p1}

Opción A
:   Una tarea con rama con las reglas de lectura y los nueve pasos; primero el bucle de afinado, la horizontal y el eje con entradas.

Opción B
:   Solo las reglas y el bucle; los recursos nuevos, como propuesta.

Opción C
:   Ninguna por ahora.

Recomendación
:   **A.** Las reglas sin el generador que las cumpla se quedan en el papel.

Decisión
:   A, decisión 325. Las nueve propuestas, en una sola tarea con rama (401), por este orden: reglas de lectura y bucle de afinado; entradas laterales; horizontal o aviso; presupuesto como recomendación; y después orden y compacidad, etiquetas y calles, zonas anidadas y formas, dinamismo, y ficha, sintaxis y kit.

### 2 · Disposición base para un flujo con entradas {estado=decidida recomendada=A elegida=A} {: #p2}

Opción A
:   El eje en una columna con las entradas al lado, como el original y la ronda 2, arreglando el generador.

Opción B
:   La arquitectura por zonas de hoy, con orden por zona y bus.

Recomendación
:   **A.** Es la que se lee de un tirón; la arquitectura sirve para piezas, no para una cadena.

Decisión
:   A, decisión 326. El eje en una columna y cada entrada al lado, a la altura de su destino y dentro de su zona; las entradas menores que no merecen caja, como chip dentro de su nodo.

:::

## Tareas | Lo que sale de este informe | Tareas {#tareas}

| Tarea | Tipo | Qué hace |
| --- | --- | --- |
| Que la skill de diagramas dibuje flujos que se leen de un tirón, con las entradas frente a su destino (401) | Implementar, con rama | Las [reglas](#reglas) y las nueve [propuestas](#propuestas) (decisión 325), con la disposición de la [pregunta 2](#p2) (decisión 326) y este flujo como prueba. |

Pasos de la 401:

1. Añadir a la skill las reglas de lectura y el bucle de afinado con Claude, en tres rondas como mucho.
2. Colocar las entradas laterales a la altura de su destino en el eje, en su zona, y detectar flechas que no tocan su caja.
3. Emitir la horizontal o avisar de que no cabe.
4. Hacer del presupuesto de nodos una recomendación, con la opción `completo`.
5. Respetar el orden de la zona y compactar las cajas plegadas.
6. Poner cada etiqueta junto a su tramo, una calle por flecha, reparto en bus y puentes en la frontera.
7. Añadir zonas anidadas, corchetes y las clases `accion` y `previsto`.
8. Añadir el modo «recorrer» con ← y →, «solo lo nuevo» y áreas plegables.
9. Arreglar la ficha, la sintaxis y el kit: chip como tipo, línea `codigo:`, `a > b | marca` y la errata «las figura».
10. Rehacer con la skill el flujo de audio de LupDub y comprobarlo a 375 y 1440, en claro y oscuro.
