---
antetitulo: Software Factory · Informe de investigación · Noviembre 2026
lema: Lo caro no es lo que dicen las pruebas, // sino cuántas veces se lanzan.
subtitulo: Dónde se van los tokens cuando un subagente comprueba su trabajo, qué herramientas ya lo resumen y cómo sería una sola orden de Python que elija, lance y resuma las comprobaciones.
version: Versión 1.2 · 27/11/2026
estado: Propuesta · Tarea 474
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de investigación
pie: Informe de la tarea «Gastar menos tokens al probar, con una herramienta de Python que lo resuma» (474). Parte de 418 transcripciones de subagentes de la SF (del 25/10 al 27/11/2026), de ejecuciones reales de cada comprobación en develop y de las skills crear_documentos, diagramas y orquestación. Espera la decisión del propietario de la Software Factory.
---
# Probar con una sola orden

## Resumen | Menos órdenes, no textos más cortos | Resumen {#resumen}

Comprobar el trabajo se lleva cerca de un tercio de lo que gastan los subagentes: el 2 % del texto que tienen que releer, medido en 418 subagentes de este mes. Pero casi nada de ese gasto está en lo que dicen las pruebas. Los subagentes ya recortan lo que escriben las pruebas (con opciones de pytest y con `tail`, que deja solo las últimas líneas), y lo que leen de todas las comprobaciones juntas no llega al  % del texto que reciben. Lo caro es **cuántas órdenes lanzan**: cada orden es un paso de su conversación, y en cada paso el subagente vuelve a leer todo lo que lleva, unos 137.000 tokens de media. Un subagente que comprueba lanza 6 órdenes de prueba (la mediana; 22 o más el 1 % que más), y las pruebas de Python, que seguidas tardan 6 minutos, no caben en el plazo de una orden: se dejan corriendo aparte y el subagente gasta más pasos en vigilarlas.

Se propone una orden, `comprobar.py`, que el subagente lanza **una vez por vuelta**: mira qué cambió en la rama, elige qué comprobar, salta lo que ya pasó sin que nada cambiara, lo lanza todo a la vez y devuelve unas pocas líneas, con el detalle de lo que falla y todo el texto de las pruebas guardado en un archivo. Repartiendo las pruebas en partes que corren a la vez, el conjunto entero baja de unos 7 minutos (Python y `claude plugin test` seguidos) a unos 2½, y una vuelta normal, que solo toca una parte, a menos de un minuto. Quitaría alrededor de dos tercios de ese 2 %, según cuántas órdenes sueltas queden.

Los dos esquemas siguientes tienen la misma forma y escala para compararlos de un vistazo: primero cómo se comprueba hoy, después cómo sería con la orden.

![](diagramas/comprobar-ahora.diagrama)

![](diagramas/comprobar-una-orden.diagrama)

Quedan seis preguntas: qué hace la orden, dónde vive, cuándo se fía de lo ya comprobado, qué pasa con las capturas de pantalla, cómo se pide usarla y qué hacer con las pruebas lentas.

[Ver las seis preguntas](#por-decidir){: .salto}

## Gasto | Dónde se van los tokens al probar | El gasto {#gasto}

La medida que importa es el texto que se vuelve a leer en cada paso, no lo largo de lo que escribe una prueba. Releer es barato por token, pero se paga entero en cada paso: una prueba que cuesta una orden cuesta unos 137.000 tokens releídos, diga lo que diga. Por eso, en el texto que reciben, pytest es solo el 0, % y en pasos es el 4, %. Lo mismo pasa con `claude plugin test`, los generadores de documentos y las esperas de las pruebas que se dejan corriendo aparte.

**2 %** del texto releído en cada paso
{: .metrica}

**6** órdenes de prueba por subagente (mediana)
{: .metrica}

**188** veces que las pruebas de Python se dejaron corriendo aparte en el mes
{: .metrica}

El reparto, por tipo de orden, sumando en cada una el texto que se relee en el paso que recibe su resultado:

| Orden | Veces en el mes | Caracteres que escribe | Texto releído |
| --- | --- | --- | --- |
| Generar un HTML o un diagrama | 849 | 1.663 | 6, % |
| `claude plugin test` | 988 | 1.102 | 4, % |
| Vigilar, parar o leer una orden que corre aparte | 842 | 359 | 4, % |
| `pytest` | 774 | 722 | 4, % |
| Mirar una captura | 583 | una imagen | 2, % |
| Sacar una captura con el navegador automático (Playwright) | 328 | 1.294 | 2, % |
| `claude plugin validate` | 296 | 1.151 | 1, % |
| `comprobar_diagramas.py` | 150 | 1.565 | 1, % |
| `comprobar_documento.py` | 141 | 2.146 | 0, % |
| Todo lo de probar | | | 29, % |

El resto, el 7 %, es leer y buscar en el código (`Read`, `sed`, `grep`, `cat`), git, editar y escribir: no es de esta tarea. En cada subagente, lo de probar es el 1 % de la mediana, el 3 % del cuartil alto y el 4 % del 1 % que más prueba.

> **Lo que dicen las ejecuciones en develop**
> Las pruebas de Python seguidas, 518: 368 s, más que los 120 s de plazo de una orden, así que se dejan corriendo aparte. `claude plugin test`: 66 s y 536 líneas (56.465 caracteres) si no se recorta. `claude plugin validate`: 1 s y 83 líneas (9.461 caracteres), 57 de ellas informativas. `comprobar_documento.py` de un informe con tres diagramas: 6 s y 10 líneas. `comprobar_diagramas.py`: 1 s y 9 líneas. El generador de un informe: menos de 1 s y 3 líneas.

### Qué tarda y por qué se deja corriendo aparte {#lentas}

Dos grupos de pruebas se llevan casi todo el tiempo: los de la cola de tareas (244 pruebas que crean repositorios de prueba, unos 150 s) y los de diagramas (24 pruebas que abren el navegador, una de ellas de 67 s, que prueba cada tema de colores del catálogo). Lanzados todos los archivos a la vez, con `claude plugin test` al lado, el conjunto tarda 155 s en lugar de 434 s. Repartiendo las de la cola en diez partes, sus 148 s bajan a 28 s; las de diagramas, en ocho partes, a 83 s, porque la prueba de los temas no se puede partir. El techo queda en `claude plugin test` y en esa prueba: unos 2 minutos para todo.

#### Repeticiones por subagente {#repeticiones}

Entre los subagentes que usan cada comprobación, la mediana y el valor que solo supera el 1 % que más la usa: pytest 2 y 9 (82 como mucho); `claude plugin test` 3 y 10; `claude plugin validate` 1 y 3; `comprobar_documento.py` 3,5 y 17; `comprobar_diagramas.py` 3 y 12; generar un documento 4 y 25; capturas 3 y 8. En 731 órdenes el subagente ya junta varias comprobaciones en una sola, a mano.

## Herramientas | Lo que ya se resume y lo que no | Herramientas {#herramientas}

Las comprobaciones de documentos de la SF ya resumen: dicen en pocas líneas qué pasa y qué falla, y avisan con un código de error si algo va mal. Lo que no resume son las órdenes de fuera (pytest a medias, `claude plugin test` nada) y las capturas, que cada subagente se hace a mano. Juntarlas en una orden no exige reescribir ninguna: basta con lanzarlas, ver si terminaron bien y quedarse con sus últimas líneas.

::: tarjetas 3 plegables

### comprobar_documento.py {color=correcto icono=check}

Resume
:   Sí: unas 10 líneas, con cada fallo en la suya.

Tarda
:   6 s, con escritorio, móvil, claro, oscuro, A4 y diagramas.

Para la orden
:   Se lanza tal cual por cada documento cambiado.

### comprobar_diagramas.py {color=correcto icono=check}

Resume
:   Sí: unas 9 líneas, por ancho y por figura.

Tarda
:   1 s.

Para la orden
:   Ya lo lanza `comprobar_documento.py`; suelto, solo para una página sin documento.

### Generadores de documentos {color=correcto icono=documento}

Resume
:   Sí: 3 líneas y sus avisos.

Tarda
:   Menos de 1 s.

Para la orden
:   Regenera el documento y avisa si el HTML no estaba al día con su `.md`.

### pytest {color=aviso icono=codigo}

Resume
:   A medias: en modo breve, una línea por archivo y el detalle de cada fallo, que puede ser largo.

Tarda
:   368 s seguida; 28 s las de la cola, repartidas en partes.

Para la orden
:   Se reparte en partes y se queda con el nombre y la primera línea de cada fallo.

### claude plugin validate {color=aviso icono=check}

Resume
:   A medias: 83 líneas, casi todas informativas; tiene un modo que las da ordenadas para otra herramienta (`--json`).

Tarda
:   1 s.

Para la orden
:   Se lee ese modo: errores y avisos, nada más.

### claude plugin test {color=error icono=codigo}

Resume
:   No: una línea por prueba, 536 líneas, sin modo breve.

Tarda
:   66 s; 116 s con otras pruebas a la vez.

Para la orden
:   Se queda con su última línea y con las que dicen `(fail)`.

### Capturas con el navegador automático {color=error icono=lupa}

Resume
:   No: un script distinto cada vez y una imagen que mirar, de unos 1.500 tokens, que se quedan en lo que el subagente relee.

Tarda
:   Segundos, más el paso de mirarla.

Para la orden
:   Una sola imagen de muestra, solo si se pide (pregunta [4](#p4)).

:::

## Propuesta | Cómo sería la orden | La orden {#propuesta}

Una orden de Python sin nada nuevo que instalar, en la biblioteca del plugin, que el subagente lanza al acabar cada vuelta con el plazo máximo de una orden (10 minutos), para que nunca tenga que dejarse corriendo aparte. Hace cinco cosas, en este orden:

1. **Qué cambió:** los archivos que difieren de develop en la rama de la tarea, más los que aún no tienen commit. Con `--todo`, todo; en una deliberativa, sin rama, los documentos que se le nombren.
2. **Elegir:** cada regla dice qué archivos mira y qué orden lanza. En la SF, `tools/cola.py` o su prueba dan las pruebas de la cola; un archivo de código del panel (`.ts` o `.tsx`), `claude plugin test`; el manifiesto, los avisos automáticos o el `SKILL.md` de una skill, `claude plugin validate`; un `.md` con su `.html` o un `.diagrama`, generar el documento y `comprobar_documento.py`. Un archivo del plugin que ninguna regla nombra lanza todas las pruebas: ante la duda, más.
3. **Marca de lo comprobado:** para cada comprobación, la orden hace una marca con sus archivos y su orden (un código corto que cambia si cambia cualquiera de ellos). Si la marca es igual que la de la última vez que pasó, no se repite y lo dice («ya pasó, sin cambios desde las 10:42»). Las marcas se guardan en la carpeta temporal, fuera del repositorio.
4. **Lanzar a la vez:** cada comprobación por su lado; las pruebas de Python, repartidas en partes; las del navegador, pocas a la vez, para no ahogar el equipo. Lee lo que escriben aunque lleve acentos o símbolos raros (al medir, Windows dio un texto con otra codificación).
5. **Resumen y archivo con el texto completo:** una línea por comprobación y, de lo que falla, el nombre de la prueba y su error, en pocas líneas. Todo lo que escribió cada orden va a un archivo, que el resumen nombra. Termina con error si algo falla, y con `--json` da lo mismo ordenado para otra herramienta.

### Lo que lee el subagente {#salida}

Cuando todo pasa, cuatro o cinco líneas, ya listas para copiar a los pasos hechos de la tarea:

```text
Comprobado: 244 pruebas de Python de la cola, sin fallos · 28 s
Comprobado: claude plugin validate, sin errores (1 aviso del directorio de plugins)
Comprobado: «Gastar menos tokens al probar.html» en escritorio, móvil, claro, oscuro y A4, sin errores · 6 s
Sin lanzar: claude plugin test (nada cambió en el mod)
Texto completo: C:\Users\…\Temp\sf-comprobar\2026-11-27-1042.log
```

Cuando algo falla (aquí, un ejemplo inventado), solo eso tiene detalle:

```text
Falla: 1 de 244 pruebas de Python de la cola
  test_cola.py::ConGit::test_cerrar_firma_con_el_coautor_configurado
  AssertionError: 'Co-Authored-By: Claude' not found in '…' (test_cola.py:812)
Comprobado: claude plugin validate, sin errores
Texto completo: C:\Users\…\Temp\sf-comprobar\2026-11-27-1047.log
```

### Cómo la usarían el encargo y las skills {#uso}

::: columnas

#### El encargo del subagente

Una línea en el encargo que escribe el principal: «Al acabar cada vuelta, comprueba con una sola orden, `comprobar.py`, con el plazo de 10 minutos; las órdenes sueltas, solo para buscar la causa de un fallo, mirando antes el archivo con el texto completo. Copia a tu informe sus líneas «Comprobado: …»». Antes de dejar la tarea lista para probar, `comprobar.py --todo --desde-cero` (todo otra vez, sin fiarse de lo ya comprobado).

|||

#### crear_documentos y diagramas

En el apartado «Comprobación», la orden de partida pasa a ser `comprobar.py --doc <documento>.md`: regenera el HTML, avisa si no estaba al día y lanza `comprobar_documento.py`, que ya revisa los diagramas. En diagramas, igual con la página. Lo que se mira a mano sigue en la lista de la skill, sin capturas de pantalla por costumbre (pregunta [4](#p4)).

:::

En los demás proyectos, la orden es la misma y sus reglas, las del proyecto: las de los documentos vienen incluidas y cada proyecto añade sus pruebas en un archivo suyo, si se elige así (pregunta [2](#p2)).

## Alternativas | Lo que se valoró | Alternativas {#alternativas}

Las otras formas de gastar menos dejan sin tocar lo que más pesa, el número de órdenes, o lo tocan a cambio de algo peor. La orden propuesta es la única que baja a la vez las órdenes, las esperas y los textos largos, y se apoya en algo que la SF ya decidió para la cola: juntar en una orden lo que antes eran varias («Sin subagente de la cola: órdenes compuestas…», 284).

| Alternativa | A favor | En contra |
| --- | --- | --- |
| La orden `comprobar.py` (propuesta) | Una orden por vuelta; elige, salta lo ya pasado y no hay que dejarla corriendo aparte | Código que mantener; las reglas de qué mira cada comprobación pueden quedarse cortas |
| Una orden que solo junta y resume lo que se le pide | Más sencilla, sin reglas ni marcas | El subagente sigue eligiendo qué lanzar y repite lo que ya pasó |
| Solo reglas en el encargo («junta las órdenes en una y recorta lo que escriben») | Sin código | Ya se hace en buena parte; depende de que el subagente se acuerde y no quita las esperas |
| Un aviso automático que recorte los textos largos | Automático, sin cambiar los encargos | Los textos ya son cortos; no baja el número de órdenes, que es lo caro |
| Un subagente barato que pruebe y resuma | Lee poco | Lanzarlo y esperarlo cuesta pasos del que lo llama; el fallo llega de segunda mano |
| `pytest-xdist`, una herramienta ajena que reparte las pruebas de Python entre los procesadores | No hay que escribir nada | Hay que instalarla en cada equipo; solo acelera pytest |

## Por decidir | Lo que queda por decidir | Por decidir {#por-decidir}

Seis preguntas, de la más importante a la menos. La primera decide si se hace la orden; las demás, cómo. Cada una se entiende sola, partiendo de lo que ves hoy.

::: preguntas 2 plegables

### 1 · Qué hace la orden nueva de comprobar {recomendada=A} {: #p1}

Hoy, al acabar cada vuelta, el subagente escribe a mano entre cuatro y veinte órdenes de prueba, una tras otra, y en cada paso vuelve a leer todo lo que lleva. Hay que elegir hasta dónde llega la herramienta nueva.

Opción A
:   Una orden que mira qué cambió, elige qué comprobar, salta lo que ya pasó, lo lanza todo a la vez y devuelve pocas líneas: una sola orden por vuelta.

Opción B
:   Una orden que solo lanza a la vez y resume lo que se le pide, sin elegir por lo que cambió ni recordar lo ya comprobado.

Opción C
:   Sin herramienta: una regla en el encargo para juntar las órdenes y recortar lo que escriben.

Recomendación
:   **A.** Es la única que quita órdenes y esperas, que es donde está el gasto; B y C dejan al subagente decidiendo y repitiendo.

### 2 · Dónde vive la orden de comprobar {recomendada=A} {: #p2}

Las pruebas del plugin son propias de la SF, pero comprobar documentos y diagramas sirve a cualquier proyecto que use la SF, y esos proyectos también tienen sus propias pruebas. Hoy cada uno las lanza como puede.

Opción A
:   En el plugin, para todos los proyectos: las comprobaciones de documentos y diagramas ya incluidas, y cada proyecto declara sus pruebas en un archivo suyo (la SF, las suyas).

Opción B
:   Solo en el repositorio de la SF, fuera del plugin: más sencilla, pero los demás proyectos no la tienen.

Opción C
:   En el plugin, solo para documentos y diagramas; las pruebas de la SF, en otra orden de su repositorio.

Recomendación
:   **A.** Lo que sirve a los usuarios viaja en el plugin, y un proyecto con pruebas propias ahorra lo mismo que la SF.

### 3 · Cuándo se fía de lo que ya pasó {recomendada=B} {: #p3}

Hoy el subagente repite las comprobaciones aunque no haya cambiado nada desde que pasaron (un documento se comprueba 3 o 4 veces por tarea). La orden nueva podría saltarse lo que no cambió: para saberlo hace una marca con los archivos de los que depende cada comprobación, y si la marca es la misma que la última vez que pasó, no repite. El riesgo es que una prueba dependa de un archivo que la regla no nombra, y se salte una comprobación que sí hacía falta.

Opción A
:   Siempre: si la marca no cambió, da el resultado anterior.

Opción B
:   Durante la vuelta, sí; antes de dejar la tarea lista para probar, todo otra vez, sin fiarse de lo anterior (unos 2 minutos).

Opción C
:   Nunca: cada vez lanza todo lo elegido.

Recomendación
:   **B.** Ahorra las repeticiones de cada vuelta, y la pasada entera del final recoge lo que una marca mal hecha dejaría pasar.

### 4 · Qué hace el subagente con las capturas de pantalla {recomendada=A} {: #p4}

Además de la comprobación automática de documentos, muchos subagentes sacan capturas de pantalla con un navegador automático y las miran: cada imagen son unos 1.500 tokens que se quedan en lo que releen (583 en el mes; unas 8 por subagente que las usa).

Opción A
:   Solo si el cambio es visual o la comprobación avisa de algo que no sabe medir, y una sola imagen, con escritorio y móvil en claro y oscuro juntos, que saca la orden si se le pide.

Opción B
:   Como hoy: cada subagente las saca y las mira cuando le parece.

Opción C
:   Nunca: se fía de la comprobación, y lo visual lo ve el propietario al probar.

Recomendación
:   **A.** Quita las capturas de costumbre sin dejar a ciegas un cambio de aspecto, que la comprobación no juzga.

### 5 · Cómo se pide al subagente que la use {recomendada=A} {: #p5}

La orden nueva solo ahorra si el subagente la usa en lugar de las órdenes sueltas, y hoy cada uno sigue su costumbre. Lo único que leen todos los subagentes es el encargo que les escribe el agente principal.

Opción A
:   El encargo lo dice: una sola orden al acabar cada vuelta, con el plazo de 10 minutos; las órdenes sueltas, solo para buscar la causa de un fallo; y su línea «Comprobado: …» pasa tal cual al informe.

Opción B
:   Se recomienda en las skills y en el documento de arranque, sin tocar el encargo.

Recomendación
:   **A.** Sin decirlo en el encargo, cada subagente seguiría con su costumbre.

### 6 · Qué hacer con las pruebas lentas {recomendada=A} {: #p6}

Hoy las pruebas de Python seguidas tardan 6 minutos, más que el plazo de una orden, y el subagente las deja corriendo aparte y las vigila con más pasos. Casi todo el tiempo es de las pruebas de la cola de tareas y de una prueba de diagramas que prueba cada tema de colores (67 s ella sola).

Opción A
:   Que la orden las reparta en partes y las lance a la vez: las de la cola bajan de 148 s a 28 s y todo queda en unos 2 minutos, el tiempo de `claude plugin test`.

Opción B
:   Lo mismo y, además, una tarea para acelerar la prueba de los temas.

Opción C
:   Instalar `pytest-xdist`, una herramienta ajena que reparte las pruebas por su cuenta: hay que instalarla en cada equipo.

Recomendación
:   **A.** Con las partes, el techo es `claude plugin test`; acelerar la prueba de los temas no bajaría el total.

:::

## Tareas | Las tareas que salen | Tareas {#tareas}

Si el propietario elige lo recomendado, salen tres tareas, en este orden. La primera lleva las preguntas [1](#p1), [2](#p2), [3](#p3) y [6](#p6); la segunda, [4](#p4) y [5](#p5).

| Tarea | Tipo | Qué hace |
| --- | --- | --- |
| Comprobar con una sola orden: elige por lo cambiado, lanza a la vez y resume | Desarrollo | Crea `comprobar.py` en el plugin, con sus reglas para la SF y los documentos, las marcas de lo comprobado, el reparto en partes, el archivo con el texto completo y sus pruebas; al mes, vuelve a medir el gasto con el mismo método |
| El encargo y las skills de documentos comprueban con la orden nueva | Desarrollo | Cambia la línea de comprobar del encargo (orquestación) y el apartado «Comprobación» de crear_documentos y diagramas |
| Actualizar el arranque y «Cómo se desarrolla la Software Factory» | Documental | Pone en ambos la orden nueva en lugar de las tres sueltas (texto propuesto en el anexo) |

## Anexo · Cómo se midió | Método y límites | Medida {#medicion}

Las 418 transcripciones de subagentes de la SF de más de 20 kB, del 25/10 al 27/11/2026, leídas por un script que no guarda nada de su contenido: por cada orden, su tipo (por la orden o el archivo que lee), el tamaño de su resultado y el texto que trae el paso siguiente, el que recibe ese resultado. «Texto releído» suma, por paso, los tokens de entrada, los leídos de la memoria rápida y los guardados en ella; es la base de lo que cuesta un paso, aunque cada clase de token tiene su precio. Las imágenes cuentan como unos 1.500 tokens.

Límites: una orden que junta varias comprobaciones cuenta en la primera que nombra; una orden repetida en una transcripción reanudada puede contar dos veces en el tamaño de los resultados, no en los pasos. Los tiempos se midieron en este equipo (24 núcleos), con otras sesiones abiertas: el del conjunto de pruebas en paralelo es con 8 procesos a la vez, y `claude plugin test` tardó 66 s solo y 116 s acompañado. El ahorro de dos tercios es una estimación: supone pasar de unas 6 órdenes de prueba por vuelta a una o dos.

## Anexo · Documentos compartidos | Texto propuesto para otras tareas | Documentos {#documentos}

Cuando exista la orden, el arranque (`docs/arranque-claude.md`) cambiaría su línea de comprobar el plugin por esta, con el OK del propietario:

> «Comprobar: `python -I -X utf8 plugins/sf/tools/comprobar.py`, que elige por lo cambiado frente a develop, lo lanza a la vez y resume; `--todo --desde-cero` antes de dejar una tarea lista para probar. Las órdenes sueltas (`pytest`, `claude plugin test`, `claude plugin validate`), solo para buscar la causa de un fallo.»

En «Cómo se desarrolla la Software Factory», el paso 3 de comprobar quedaría: «Comprobar con `comprobar.py --todo`, que pasa `claude plugin validate`, `claude plugin test`, las pruebas de Python de `plugins/sf/tests/` y los documentos cambiados». La referencia de desarrollo de la metodología nombra hoy `unittest discover` para las pruebas de Python, cuando el arranque dice `pytest`: la tarea que la ponga al día debería dejar una sola orden.
