# Leer de un tirón

Reglas de lectura para los diagramas de flujo, sacadas de un flujo hecho a mano que se lee con fluidez (el de audio de LupDub, informe de la tarea 398). Valen sobre todo para proceso, estados, flujo de datos y arquitectura con un camino.

**Criterio rector**: ¿lo entenderá de forma fluida un lector nuevo, organizado así? Lo que fluye no es una flecha sino un concepto (una señal, un estado, una petición, un dato); seguir el flujo es contar su vida de principio a fin sin perderse. Las medidas sirven a esa pregunta, no la sustituyen.

## Preguntas de cada ronda

Claude las contesta en una o dos frases cada una, mirando la captura; el atasco decide el cambio siguiente.

1. ¿Qué concepto fluye?
2. ¿Se entiende su recorrido con fluidez, de principio a fin? ¿Dónde se atasca un lector nuevo?
3. ¿Van las áreas funcionales una tras otra, con sus conexiones claras?
4. ¿Qué hay que destacar?
5. ¿Qué información no aporta?
6. ¿Queda oculto algo clave?
7. ¿Es un enredo o se sigue con facilidad?
8. ¿Qué dinamismo ayuda a la idea clave?
9. ¿Quedan cruces que evitar?

## Reglas, en el mismo orden

Cada una con su medida; las que mide el generador (`--medidas`), entre comillas angulares.

| Regla | Qué pide | Medida |
|---|---|---|
| Qué fluye | Antes de colocar nada, nombrar el concepto que fluye; sus flechas, `flujo` en los datos, son las principales; control y acciones, secundarias, con otro trazo | Cada figura declara su flujo; ninguna secundaria con su estilo («flujo») |
| Columna vertebral | El recorrido del concepto en una columna, en el orden de la historia, de arriba abajo | Codos y subidas del flujo, cero («flujo») |
| Áreas, las etapas del concepto | Las zonas son las etapas por las que pasa y se apilan en ese orden; se entiende una entera antes de la siguiente. Solo las etapas reales: una carpeta no se inventa para encajar | El orden de las zonas, el del camino; las flechas internas, dentro de su zona; cada carpeta, un módulo clave (el generador) |
| Quién hace qué | Cada caja, verbo y objeto con las palabras del lector (el glosario inspira, no obliga: 426); el detalle, la consecuencia o la cifra; el actor, donde cambia. Un bucle dice cuándo acaba; una rama que no vuelve, en qué acaba; la etiqueta de una flecha, lo que pasa o lo que viaja (el porqué, a la ficha); la discontinua, un solo sentido (decisiones 422 y 423) | Avisos del generador; la lectura en frío coincide con el concepto |
| Del concepto a la estructura | Cada condición, una decisión con su pregunta; el bucle, desde ella; lo que cuelga de un paso, a su lado (si no cabe, rótulos más cortos) | Avisos del generador; error si lo de al lado no cabe |
| Rehacer conserva el concepto | Rehacer o convertir un diagrama deja los mismos pasos, decisiones, flechas, bucles y etiquetas, por ids (el rótulo puede mejorar); si el generador no puede dibujar algo, se arregla el generador, no el contenido | Con `--antes`, ninguna diferencia (el generador) |
| Ciclo o jerarquía entre bloques | Lo primero al colocar las zonas: con todas las flechas entre bloques, por partes. ¿Un par con ida y vuelta? Vecinos, cada flecha por su lado. ¿Un ciclo, de todos o de algunos? En anillo (el primero, una fila arriba; los demás, columnas que bajan y suben), la vuelta cierra en su sitio y lo demás cuelga de él. ¿Una cadena o una jerarquía? En columnas por orden, lo supeditado al lado de lo que depende. Cada zona, una sola carpeta. Se mide contra la forma apilada y se queda la que mejor se lee (decisión 415) | Ciclo o hermanos apilados pudiendo ir de otra forma, cero (el comprobador lo avisa) |
| Bloques cerrados al empezar | Con varios bloques, la figura empieza con todos cerrados, en todas las anchuras: se ve el ciclo o la jerarquía entre ellos. Cada bloque es una carpeta con su nombre en la pestaña y el fondo suave de su cauce, distinta de un paso; abierta, la misma carpeta en grande. Entre dos bloques cerrados, una flecha ancha y rellena; pulsar uno lo abre en su sitio, su nombre lo cierra, «Abrir todos» lo abre entero. Al imprimir, abiertos | El comprobador abre y cierra uno y prueba «Abrir todos» |
| Un flujo lineal, recto | Una cadena dentro de un bloque (cada paso, una entrada y una salida dentro de él) va en una fila o una columna si cabe; el codo, solo si no cabe | Requiebros con sitio para ir recta, cero («requiebros»; el comprobador lo avisa) |
| Pesos repartidos | Al abrir un bloque (o con todos cerrados o abiertos), los demás se reparten respecto a él: centrados, o cada uno bajo el paso con que se une, sin romper los ángulos rectos. Cada vista se ajusta a lo que dibuja, centrada a lo ancho y sin hueco arriba, a la misma escala; al cambiar de vista, lo pulsado se queda en su sitio de la pantalla | Filas con bloques cerrados que cargan a un lado con sitio para repartirse, cero («desequilibrio»; el comprobador lo avisa). Vistas descentradas o con hueco arriba, cero («descentrado», «hueco arriba»: errores del comprobador) |
| Pocos puentes, en la frontera | Entre dos áreas, pocas conexiones, juntas en la frontera y con etiqueta | Dos como mucho entre las mismas, salvo un bus («puentes de más») |
| La historia avanza con el scroll | Nada obliga a volver arriba salvo las vueltas, que se ven como vueltas | Flechas que suben sin ser vuelta, cero («suben») |
| Origen y destino a la vista | Una flecha se sigue sin perder su origen | Una pantalla o menos a 375 y a 1440, salvo vueltas («más larga») |
| Vueltas por fuera | La vuelta, por el carril más exterior, discontinua, una por carril | Ningún trazo entre su carril y el borde |
| Un foco | Lo nuevo o lo que cambia, con el acento; la cadena, con el color del camino | Un foco, dos como mucho |
| La idea, no todo el detalle | Primero, la versión más simple que transmite el objetivo: las cajas que pide el objetivo, no el concepto entero; una caja puede resumir varias cosas; códigos, cifras y detalles, a las fichas (387, criterio) | Aviso con más de ocho cajas y con un código o una cifra en un nombre o una etiqueta |
| Nada que no aporte | Cada etiqueta dice algo que la flecha no dice ya; el detalle, a la ficha | Etiquetas que repiten el destino, cero; detalle plegado en una línea |
| Lo clave, sin pulsar | El foco y los nombres del camino se ven con todo plegado | — |
| Cada entrada frente a su destino | Lo que alimenta un paso va en la columna de al lado, a su altura: flecha recta y corta | Sin codos («codos») |
| Una, dos o más columnas | Se elige la que mejor se lee; una rama que cuelga de un paso del medio, al lado de ese paso y no al fondo, donde parece el final | Cajas lejos de su única unión, cero («cajas lejos de su única unión»; el comprobador lo avisa) |
| Columnas por papel | Control, entradas, camino y acciones, cada uno en su columna; flechas solo entre vecinas | Tramos por una caja ajena, cero («por caja ajena») |
| Reparto en bus | Un origen con tres destinos o más: un tronco y ramas cortas | Tramo compartido sin contar el bus, cero («compartido») |
| ¿Enredo o se sigue? | Si para seguir una flecha hay que buscarla entre otras, es un enredo | Compartido, codos y largo |
| Acciones y previsto con su forma | Las acciones, fuera del camino, con su forma y flecha a lo que cambian (un nodo o, si son varios, la carpeta de su zona); lo previsto, discontinuo y atenuado | Clases `accion` y `previsto` |
| Ritmo compacto | Cajas del camino de un alto y un paso constantes; el blanco, entre áreas | — |
| Un dinamismo, al servicio de la idea | Uno principal, nunca decorativo, con teclado y quieto si se pide menos movimiento: recorrer el camino paso a paso y el resaltado | — |
| Y, al final, evitar cruces | Con lo anterior resuelto, quitar los cruces que queden; si uno no se puede evitar, un puente | Cruces y tramos por una caja ajena, cero («cruces») |
