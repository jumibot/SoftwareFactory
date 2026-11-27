---
antetitulo: Software Factory · Informe de investigación · Noviembre 2026
lema: Lo caro no es lo que dicen los tests, // sino cuántas veces se lanzan.
subtitulo: Dónde se van los tokens cuando un subagente testea su trabajo, en la SF y en otros proyectos, y cómo sería una orden del plugin que detecte los tests de cualquier proyecto, los lance y resuma.
version: Versión 2.0 · 27/11/2026
estado: Propuesta · Tarea 474
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de investigación
pie: Informe de la tarea «Gastar menos tokens al probar, con una herramienta de Python que lo resuma» (474). Parte de 418 transcripciones de subagentes de la SF y 93 de otros siete proyectos del propietario (del 25/10 al 27/11/2026), de ejecuciones reales de cada comprobación en develop y de las skills crear_documentos, diagramas y orquestación. De los otros proyectos solo se usan cifras y el nombre de su stack. Espera la decisión del propietario de la Software Factory.
---
# Testear con una sola orden

## Resumen | Una orden para cualquier proyecto | Resumen {#resumen}

Testear el trabajo se lleva cerca de un tercio de lo que gastan los subagentes de la SF (el 29 % del contexto que releen, en 418 subagentes de este mes) y entre el 1 % y el 9 % en los otros proyectos del propietario (4,7 % en conjunto, en 93 subagentes). Casi nada de ese gasto está en lo que dicen los tests: los subagentes ya recortan las salidas, y lo que leen de todas las comprobaciones juntas no llega al 6 % del texto que reciben. Lo caro es **cuántas llamadas hacen**: cada orden es un turno, y en cada turno el subagente relee todo lo que lleva, unos 137.000 tokens de media en la SF. La mediana es parecida en todos los proyectos: 6 llamadas de test por subagente en la SF y 7 en los demás (16 o más el 10 % que más, 26 como mucho fuera de la SF). Lo que cambia es qué se lanza: en la SF, tests de Python y del plugin; en los otros proyectos, sobre todo comprobaciones de documentos y capturas con Playwright (el 90 % de sus llamadas), y casi ningún test de código (17 llamadas de 271).

Se propone una orden del plugin, `comprobar.py`, que sirve a cualquier proyecto bajo la SF y que el subagente lanza **una vez por vuelta**. Sabe qué tests tiene el proyecto porque detecta su stack (pytest, npm o pnpm test con vitest o jest, cargo test, go test, dotnet test, Playwright, tsc, eslint…) y, cuando eso no basta, lee una declaración del proyecto en `.sf/`. Además aprende: cada comprobación que lanza queda registrada en el proyecto (comando, duración, qué cubre, si se puede partir), y con ese registro sabe qué tests hay, también los que nadie declaró, y puede lanzarlos todos o solo los que tocan lo cambiado. Después hace lo mismo en todos, en dos rondas dentro de la misma orden. Primera ronda, seleccionar, de forma determinista: están registrados todos los tests y cada uno dice qué archivos cubre; se salta solo el que ninguno de los archivos cambiados toca (o cuya caché por hash coincide), y el que no declara qué cubre corre siempre, así que ninguno se queda olvidado. Segunda ronda, ejecutar a la vez lo seleccionado y devolver unas pocas líneas, con el detalle de lo que falla y la salida entera en un log. Lo que depende del stack (cómo se lanza en paralelo, cómo se filtra por lo cambiado, cómo se resume) vive en un detector por stack. La SF es un caso más: sus reglas son su declaración. Quitaría alrededor de dos tercios de ese gasto, según cuántas llamadas sueltas queden; en la SF, la suite entera baja de unos 7 minutos a unos 2½.

Los dos esquemas siguientes tienen la misma forma y escala para compararlos de un vistazo: primero cómo se testea hoy, después cómo sería con la orden.

![](diagramas/comprobar-ahora.diagrama)

![](diagramas/comprobar-una-orden.diagrama)

Quedan seis preguntas: qué hace la orden, cómo conoce los tests de cada proyecto (detectándolos, declarándolos o aprendiéndolos al lanzarlos), cuándo se fía de lo ya comprobado, qué pasa con las capturas, cómo se pide usarla y qué hacer con los tests lentos.

[Ver las seis preguntas](#por-decidir){: .salto}

## Gasto | Dónde se van los tokens al testear | El gasto {#gasto}

La medida que importa es el contexto releído, no el tamaño de la salida. Con la caché, releer es barato por token, pero se paga entero en cada turno: un test que cuesta una llamada cuesta unos 137.000 tokens releídos en la SF, diga lo que diga. Por eso pytest es solo el 0,9 % del texto que reciben y el 4,4 % de los turnos. Lo mismo pasa con los generadores, las capturas y las esperas de los tests en segundo plano.

**29 %** del contexto releído en la SF
{: .metrica}

**6 y 7** llamadas de test por subagente, mediana, en la SF y fuera de ella
{: .metrica}

**188** suites de Python pasadas a segundo plano en el mes, en la SF
{: .metrica}

### En otros proyectos {#otros}

Se midieron las transcripciones de subagentes de más de 20 kB de los proyectos del propietario que tienen alguna, con el mismo método que en la SF. Solo se guardan cifras y el nombre del stack.

| Stack | Subagentes | Con tests | Llamadas | Mediana | Contexto |
| --- | --- | --- | --- | --- | --- |
| Web: Python y Vite | 42 | 24 | 227 | 7,5 | 9,4 % |
| Documentos y navegador | 25 | 5 | 28 | 5 | 0,9 % |
| Documentos | 3 | 2 | 12 | 6 | 2,3 % |
| Python (cámara) | 3 | 1 | 2 | 2 | 5,1 % |
| Python (análisis) | 11 | 1 | 1 | 1 | 0,5 % |
| Documentos (otros dos) | 9 | 1 | 1 | 1 | 0,4 % |
| Todos | 93 | 34 | 271 | 7 | 4,7 % |

Las 271 llamadas son: comprobar documentos o diagramas, 154; capturas o tests con Playwright, 89; pytest, 16; eslint o ruff, 6; tsc, 4; build, 1; npm test, 1. La salida más larga leída fue de 223 líneas, y de media 19 líneas por llamada. Dos cosas se ven. Primera: el patrón es el mismo (muchas llamadas sueltas, un turno cada una), y en el proyecto web ya es el 9,4 % del contexto con solo 24 subagentes. Segunda: fuera de la SF casi nadie lanza una suite de tests, así que la orden tiene que cubrir también lo que sí lanzan: documentos, Playwright, tipos y lint.

El reparto en la SF, por tipo de llamada, sumando en cada una el contexto que relee el turno que recibe su resultado:

| Llamada | Llamadas en el mes | Caracteres por llamada | Contexto releído |
| --- | --- | --- | --- |
| Generar un HTML o un diagrama | 849 | 1.663 | 6,0 % |
| `claude plugin test` | 988 | 1.102 | 4,9 % |
| Esperar una orden en segundo plano (Monitor, TaskStop, leer su salida) | 842 | 359 | 4,6 % |
| `pytest` | 774 | 722 | 4,4 % |
| Mirar una captura | 583 | una imagen | 2,9 % |
| Sacar una captura con Playwright | 328 | 1.294 | 2,4 % |
| `claude plugin validate` | 296 | 1.151 | 1,6 % |
| `comprobar_diagramas.py` | 150 | 1.565 | 1,2 % |
| `comprobar_documento.py` | 141 | 2.146 | 0,9 % |
| Todo lo de testear | | | 29,1 % |

El resto, el 71 %, es leer y buscar en el código (`Read`, `sed`, `grep`, `cat`), git, editar y escribir: no es de esta tarea. En cada subagente de la SF, lo de testear es el 18 % de la mediana, el 31 % del cuartil alto y el 46 % del 10 % que más testea.

> **Lo que dicen las ejecuciones en develop**
> La suite de Python seguida, 518 tests: 368 s, más que los 120 s de una orden, así que pasa a segundo plano. `claude plugin test`: 66 s y 536 líneas (56.465 caracteres) si no se recorta. `claude plugin validate`: 1 s y 83 líneas (9.461 caracteres), 57 de ellas informativas. `comprobar_documento.py` de un informe con tres diagramas: 6 s y 10 líneas. `comprobar_diagramas.py`: 1 s y 9 líneas. El generador de un informe: menos de 1 s y 3 líneas.

#### Repeticiones por subagente {#repeticiones}

Entre los subagentes de la SF que usan cada comprobación, la mediana y el percentil 90: pytest 2 y 9 (82 como mucho); `claude plugin test` 3 y 10; `claude plugin validate` 1 y 3; `comprobar_documento.py` 3,5 y 17; `comprobar_diagramas.py` 3 y 12; generar un documento 4 y 25; capturas 3 y 8. En 731 llamadas el subagente ya junta varias comprobaciones en una orden, a mano.

## Stacks | Qué tests tiene cada proyecto | Stacks {#stacks}

La orden no puede traer las reglas de todos los proyectos, pero casi todos los tests se lanzan con unas pocas órdenes conocidas, y esas órdenes ya saben repartirse y filtrar. Cada detector reconoce su stack por los archivos del proyecto y dice cómo lanzar, cómo filtrar por lo cambiado y qué dejar del resultado. Las opciones de cada runner están por verificar en la tarea de desarrollo (anexo de medida).

::: tarjetas 3 plegables

### Python con pytest {color=correcto icono=codigo}

Detecta
:   `pyproject.toml`, `pytest.ini` o `requirements.txt` con pytest, y una carpeta `tests/`.

Paralelo
:   Shards por archivo en procesos aparte; `pytest-xdist` solo si el proyecto ya lo tiene.

Filtra por lo cambiado
:   Los archivos de test cambiados y los de `test_<módulo>.py` de cada módulo cambiado; sin regla, todos.

Resumen
:   `-q`; el nombre del test y la primera línea de su error.

### Node con vitest o jest {color=correcto icono=codigo}

Detecta
:   `package.json` con un script `test` o con `vitest` o `jest`; `pnpm`, `yarn` o `npm` según su lockfile.

Paralelo
:   El del runner, que ya reparte en workers.

Filtra por lo cambiado
:   `vitest run --changed develop`; `jest --changedSince=develop`.

Resumen
:   Su última línea de totales y las líneas `FAIL`.

### TypeScript, eslint y ruff {color=correcto icono=check}

Detecta
:   `tsconfig.json`, scripts `typecheck` o `lint`; `ruff` o `flake8` en `pyproject.toml`.

Paralelo
:   Cada uno, en su proceso; son rápidos.

Filtra por lo cambiado
:   `tsc` mira el proyecto entero; eslint y ruff, solo los archivos cambiados.

Resumen
:   Número de errores y los cinco primeros.

### Rust con cargo {color=aviso icono=codigo}

Detecta
:   `Cargo.toml`; en un workspace, sus crates.

Paralelo
:   `cargo test` ya usa hilos; compilar es lo caro y lo guarda su `target/`.

Filtra por lo cambiado
:   `-p <crate>` de cada crate con archivos cambiados.

Resumen
:   Las líneas `test result:` y los `FAILED`.

### Go y .NET {color=aviso icono=codigo}

Detecta
:   `go.mod`, o `*.sln` o `*.csproj` con un proyecto de tests.

Paralelo
:   `go test ./...` reparte por paquete; `dotnet test`, por ensamblado.

Filtra por lo cambiado
:   Los paquetes (`go list`) o proyectos que contienen archivos cambiados.

Resumen
:   `FAIL` y `ok` por paquete; `Failed!` o `Passed!` con sus totales.

### Playwright {color=error icono=lupa}

Detecta
:   `playwright.config.*` o `@playwright/test` en `package.json`.

Paralelo
:   `--shard=1/N`; sus workers ya son varios.

Filtra por lo cambiado
:   `--only-changed=develop`.

Resumen
:   Reporter breve; las capturas y los vídeos, a una carpeta, nunca al contexto. Hoy cada captura son unos 1.500 tokens (pregunta [4](#p4)).

:::

### Cuando la detección no basta {#declaracion}

Un proyecto con varios stacks, tests que necesitan un servidor, o una orden propia (como las de documentos de la SF) lo declara en un archivo, `.sf/comprobar.json`. Lo declarado manda sobre lo detectado, y lo que no se declara se detecta. Se escribe una vez, por ejemplo al incorporar el proyecto a la SF o al ponerlo al día:

```json
{
  "comprobaciones": [
    { "nombre": "tests de Python", "orden": "python -m pytest -q",
      "cubre": ["backend/**/*.py", "backend/tests/**"], "reparto": "archivo", "plazo": 300 },
    { "nombre": "tipos del frontend", "orden": "npm --prefix frontend run typecheck",
      "cubre": ["frontend/src/**"] },
    { "nombre": "documentos", "orden": "sf:documentos", "cubre": ["**/*.md"] }
  ]
}
```

`cubre` son los archivos de los que depende la comprobación (los usa para seleccionar y para el hash; sin él, el test corre siempre), `reparto` dice cómo se parte (`archivo` o ninguno) y `plazo`, los segundos que se le dan. «sf:documentos» es una comprobación incluida: regenera el HTML y pasa `comprobar_documento.py`.

### Aprender de lo que se lanza {#aprender}

Idea del propietario: si la SF lanza los tests, sabe cuáles hay. Cada vez que un subagente (o la propia orden) lanza una comprobación por `comprobar.py`, queda anotada en el proyecto, en `.sf/comprobaciones-vistas.json`: el comando, cuánto tardó (la última y la media), qué archivos cubre (ver la sección siguiente), si se pudo partir en shards y cuándo pasó por última vez. Con ese registro la orden sabe qué tests hay sin que nadie los declare, puede lanzarlos todos a la vez (`--todo`), o solo los que tocan lo cambiado, y usa las duraciones para decidir el plazo, el orden (los lentos primero) y qué merece partirse. Lo que se registra es local: los tiempos son de cada equipo, así que el archivo va en `.gitignore`.

Como pieza central no basta, porque tiene tres huecos. **Arranque en frío:** en un proyecto nuevo, o en una máquina nueva, el registro está vacío y la primera vuelta no sabe qué lanzar. **Tests que nadie ha lanzado:** el registro solo conoce lo que ya se lanzó, justo lo que un test nuevo o un stack recién añadido todavía no ha hecho; y un `--todo` basado solo en él daría por completo algo que no lo es. **Comandos que cambian:** un script renombrado o un runner nuevo dejan entradas viejas que fallan o que lanzan algo que ya no es el test (hay que caducarlas cuando el comando falla por no existir o el archivo de configuración cambia). Como complemento sí encaja bien: la detección arranca en frío y encuentra lo que nadie lanzó, el registro añade lo que la detección no ve (las órdenes propias, como las de documentos) y las duraciones reales, y la declaración manda sobre los dos. El orden de prioridad es declarado, visto, detectado.

### Seleccionar y ejecutar, en dos rondas {#rondas}

Idea del propietario: que se lancen todos los tests registrados y que cada test decida si le toca ejecutarse, según las partes que cubre y los archivos modificados; así ninguno se olvida. La orden lo hace en dos rondas seguidas, sin que Claude elija nada:

- **Ronda 1, seleccionar.** Compara los archivos modificados (rama contra develop, más lo que no tiene commit) con lo que cubre cada test, y escribe una lista: qué corre y qué se salta, con su porqué («corre: toca `backend/cola.py`», «se salta: nada de `frontend/**` cambió», «se salta: ya pasó con el mismo hash a las 10:42», «corre: no declara qué cubre»). Es una función de los archivos y del registro: con los mismos datos da siempre la misma lista.
- **Ronda 2, ejecutar.** Lanza a la vez lo seleccionado, con el reparto de su stack, y resume.

**Cómo declara un test lo que cubre.** En `cubre`, patrones de rutas (`backend/**/*.py`), en este orden de prioridad: lo que escribe el propietario o Claude a mano en `.sf/comprobar.json`, lo que se aprendió y quedó en `.sf/comprobaciones-vistas.json`, y lo que da el propio stack (el grafo de importaciones de vitest con `--changed`, `jest --findRelatedTests`, los paquetes de go, los crates de cargo, la convención `test_<módulo>.py` de pytest). Lo aprendido se mide en la pasada completa: con la herramienta de cobertura del stack (coverage.py, c8, `go test -coverprofile`) la orden anota qué archivos toca cada test. Se puede corregir a mano, y lo escrito a mano no lo pisa el aprendizaje.

**Un test sin declaración corre siempre.** Es la regla que impide olvidos: lo desconocido se lanza. Del mismo modo, un archivo cambiado que ningún test dice cubrir se avisa («sin ningún test que lo cubra») y se lanzan los tests que no declaran qué cubren.

**Con la caché.** La selección responde «¿lo toca lo cambiado?» y la caché responde «¿ya pasó así?»: un test se salta si no lo toca nada, o si, tocándolo, el hash de sus archivos y de su orden es el mismo que la última vez que pasó. Los dos motivos salen en la lista.

**Con la pasada completa.** Antes de dejar la tarea lista para probar, `comprobar.py --todo --sin-cache` lanza todos los tests sin seleccionar ni fiarse de la caché, y es donde se aprende `cubre`. Además hace de red de seguridad: si un test que la selección se habría saltado falla en la pasada completa, la orden lo dice («`cubre` incompleto en este test») y propone ampliarlo.

**El problema serio y su salida.** El riesgo de este diseño es un `cubre` demasiado estrecho: un test que debería haberse ejecutado y se salta, justo lo que el propietario quiere evitar. Lo cubren tres cosas: lo desconocido corre, lo aprendido se mide en vez de suponerse y la pasada completa antes de cerrar lo atrapa. Lo que no cubre es el tiempo entre dos pasadas completas, en que un fallo puede esperar a la pasada final; por eso las rondas de cada vuelta sirven para avisar pronto y no sustituyen a la pasada final. Si el propietario prefiere cero riesgo, la alternativa es lanzar siempre todo y quedarse solo con la caché (opción B de la [pregunta 3](#p3)), que ahorra menos.

### Una orden de Python o una herramienta del mod {#tool}

Conviene que el núcleo sea la **orden de Python** del plugin. La lanza cualquier subagente con Bash, en cualquier proyecto, desde la terminal y desde un hook, y se prueba con tests sin tener Claude delante. Una herramienta del mod (`$.tool.register`, como la que propone la tarea 475) solo la vería, en principio, el agente principal que corre con el mod, y no se sabe si un subagente la recibe; a cambio, le daría un nombre y un esquema de parámetros más cómodos que una línea de órdenes. Lo razonable es hacer primero la orden y, si luego hace falta, una herramienta del mod que no haga más que llamarla. Esto último queda sin decidir hasta ver qué tools ven los subagentes.

## Propuesta | Cómo sería la orden | La orden {#propuesta}

Una orden de Python sin dependencias nuevas, en la biblioteca del plugin, que el subagente lanza al acabar cada vuelta con el plazo máximo de una orden (10 minutos), para que nunca pase a segundo plano. Hace seis cosas, en este orden, en dos rondas (ver «Seleccionar y ejecutar, en dos rondas»). Las cinco últimas son iguales en todos los proyectos; solo la primera cambia con el stack y con lo que el proyecto ya haya lanzado:

1. **Saber qué tests hay:** junta lo declarado en `.sf/comprobar.json`, lo ya visto en `.sf/comprobaciones-vistas.json` (lo aprendido al lanzar) y lo detectado por el stack; si dos dicen lo mismo, manda el declarado, luego el visto, luego el detectado. Cada test lleva lo que cubre.
2. **Ronda 1, seleccionar:** compara los archivos modificados (los que difieren de develop en la rama de la tarea, más los que aún no tienen commit; con `--todo`, todo; en una deliberativa, sin rama, los documentos que se le nombren) con lo que cubre cada test y lista qué corre y qué se salta, con su porqué. Un test sin declaración corre siempre.
3. **Caché por hash:** para cada test, un hash de sus archivos y de su orden. Si es el mismo que la última vez que pasó, se salta y lo dice («ya pasó, sin cambios desde las 10:42»). La caché va en la carpeta temporal, fuera del repositorio.
4. **Ronda 2, lanzar a la vez:** cada comprobación en su proceso; los tests, con el reparto de su stack; los del navegador, pocos a la vez, para no ahogar el equipo. Lee las salidas en UTF-8 sin romperse con otra codificación (al medir, Windows dio una salida que no era UTF-8).
5. **Resumen, log y registro:** una línea por comprobación y, de lo que falla, el nombre del test y su error, en pocas líneas. La salida entera de cada orden va a un archivo de log, que el resumen nombra, y la duración se anota en `.sf/comprobaciones-vistas.json`.
6. **Código de salida:** sale con 1 si algo falla, y con `--json` da lo mismo para otra herramienta.

::: columnas

#### Igual en todos los proyectos

La selección determinista por lo que cubre cada test, la caché por hash, lanzar a la vez, el resumen de pocas líneas, el log aparte, el código de salida, el `--json` y la línea «Comprobado: …» lista para los pasos hechos.

|||

#### Depende del stack

Cómo se reconoce el proyecto, cómo se reparte (shards, workers del runner), cómo se sabe lo que cubre un test (grafo de importaciones, paquetes, crates, convención de nombres) y qué se queda del resultado (sus líneas de totales y de fallos).

:::

### Lo que lee el subagente {#salida}

Cuando todo pasa, la lista de la ronda 1 (qué se salta y por qué) y cuatro o cinco líneas, ya listas para copiar a los pasos hechos de la tarea. Tres ejemplos de stacks distintos:

```text
Comprobado: 38 tests de Python (backend), sin fallos · 9 s
Comprobado: tsc del frontend, sin errores · 4 s
Sin lanzar: eslint (nada de frontend/src cambió; ya pasó a las 10:42)
Log: C:\Users\…\Temp\sf-comprobar\2026-11-27-1042.log
```

```text
Comprobado: cargo test en 2 crates (core, cli), 112 tests, sin fallos · 21 s
Sin lanzar: crate docs (nada cambió)
Log: /tmp/sf-comprobar/2026-11-27-1042.log
```

```text
Comprobado: 244 tests de Python de la cola, sin fallos · 28 s
Comprobado: claude plugin validate, sin errores (1 aviso del directorio de plugins)
Comprobado: «Gastar menos tokens al probar.html» en escritorio, móvil, claro, oscuro y A4, sin errores · 6 s
Sin lanzar: claude plugin test (nada del mod cambió)
Log: C:\Users\…\Temp\sf-comprobar\2026-11-27-1042.log
```

Cuando algo falla (aquí, un ejemplo inventado), solo eso tiene detalle:

```text
Falla: 1 de 244 tests de Python de la cola
  test_cola.py::ConGit::test_cerrar_firma_con_el_coautor_configurado
  AssertionError: 'Co-Authored-By: Claude' not found in '…' (test_cola.py:812)
Comprobado: claude plugin validate, sin errores
Log: C:\Users\…\Temp\sf-comprobar\2026-11-27-1047.log
```

### Cómo la usarían el encargo y las skills {#uso}

::: columnas

#### El encargo del subagente

Una línea en el encargo que escribe el principal, igual en todos los proyectos: «Al acabar cada vuelta, comprueba con una sola orden, `comprobar.py`, con el plazo de 10 minutos; las órdenes sueltas, solo para depurar un fallo, mirando antes el log. Copia a tu informe sus líneas «Comprobado: …»». Antes de dejar la tarea lista para probar (lo que hace el propietario), `comprobar.py --todo --sin-cache`.

|||

#### crear_documentos y diagramas

En la «Comprobación», la orden de partida pasa a ser `comprobar.py --doc <documento>.md`: regenera el HTML, avisa si no estaba al día y lanza `comprobar_documento.py`, que ya pasa los diagramas. En diagramas, igual con la página. Lo que se mira a mano sigue en la lista de la skill, sin capturas por costumbre (pregunta [4](#p4)).

:::

## En la SF | La SF, un caso más | En la SF {#en-la-sf}

La SF no lleva reglas aparte dentro de la orden: declara las suyas en su `.sf/comprobar.json`, como cualquier proyecto. Son las de hoy: `tools/cola.py` o su test dan los tests de la cola; un `.ts` o `.tsx` del mod, `claude plugin test`; el manifiesto, los hooks o el `SKILL.md` de una skill, `claude plugin validate`; un `.md` con su `.html` o un `.diagrama`, `sf:documentos`.

Lo propio de la SF es que tiene la suite más pesada de todos los proyectos medidos y que por eso gana más. Dos archivos de tests se llevan casi todo el tiempo: los de la cola (244 tests con repositorios git de prueba, unos 150 s) y los de diagramas (24 tests en el navegador, uno de ellos de 67 s, que pasa cada tema del catálogo). Lanzados todos los archivos a la vez, con `claude plugin test` al lado, la suite tarda 155 s en lugar de 434 s. Partiendo la cola en diez shards, sus 148 s bajan a 28 s; los diagramas, en ocho shards, a 83 s, porque el test de los temas no se parte. El techo queda en `claude plugin test` y en ese test: unos 2 minutos para todo (pregunta [6](#p6)).

## Alternativas | Lo que se valoró | Alternativas {#alternativas}

Las otras formas de gastar menos dejan sin tocar lo que más pesa, el número de llamadas, o lo tocan a cambio de algo peor. La orden propuesta es la única que baja a la vez las llamadas, las esperas en segundo plano y las salidas largas, sirve a todos los proyectos y se apoya en algo que la SF ya decidió para la cola: juntar en una orden lo que antes eran varias («Sin subagente de la cola: órdenes compuestas…», 284).

| Alternativa | A favor | En contra |
| --- | --- | --- |
| La orden `comprobar.py` con detección y declaración (propuesta) | Una llamada por vuelta en cualquier proyecto; elige, salta lo ya pasado y no pasa a segundo plano | Código que mantener; los detectores y las reglas de qué mira cada comprobación pueden quedarse cortos |
| Una orden que solo junta y resume lo que se le pide | Más sencilla, sin reglas ni caché | El subagente sigue eligiendo qué lanzar y repite lo que ya pasó |
| Solo reglas en el encargo («una orden compuesta, con `-q` y `tail`») | Sin código | Ya se hace en buena parte; depende de la memoria y no quita las esperas |
| Un hook que recorte las salidas largas | Automático, sin cambiar los encargos | Las salidas ya son cortas; no baja las llamadas, que es lo caro |
| Un subagente barato que testee y resuma | Su contexto es pequeño | Lanzarlo y esperarlo cuesta turnos del que lo llama; el fallo llega de segunda mano |
| `pytest-xdist` para la suite | Paraleliza sin escribir nada | Una dependencia más en cada equipo; solo acelera pytest, no los demás stacks |

## Por decidir | Lo que queda por decidir | Por decidir {#por-decidir}

Seis preguntas, de la más importante a la menos. La primera decide si se hace la orden; las demás, cómo. Cada una se entiende sola, partiendo de lo que ves hoy.

::: preguntas 2 plegables

### 1 · Qué hace la orden nueva de comprobar {recomendada=A} {: #p1}

Hoy, en cualquier proyecto, al acabar cada vuelta el subagente lanza a mano entre cuatro y veinte órdenes de test o de comprobación, una por turno, y en cada turno relee todo su contexto. Hay que elegir hasta dónde llega la herramienta nueva.

Opción A
:   Una orden del plugin que en una ronda selecciona los tests según lo que cambió y lo que cubre cada uno, y en otra ejecuta a la vez lo seleccionado y devuelve pocas líneas: una sola orden por vuelta, en cualquier proyecto.

Opción B
:   Una orden que solo lanza a la vez y resume lo que se le pide, sin elegir por lo cambiado ni recordar lo ya pasado.

Opción C
:   Sin herramienta: una regla en el encargo para juntar las órdenes y recortar su salida.

Recomendación
:   **A.** Es la única que quita llamadas y esperas, que es donde está el gasto; B y C dejan al subagente decidiendo y repitiendo.

### 2 · Cómo sabe la orden qué tests tiene cada proyecto {recomendada=A} {: #p2}

Cada proyecto testea a su manera: pytest, npm test, cargo test, Playwright, o las órdenes de documentos de la SF. Hoy el subagente lo averigua leyendo el proyecto y lo lanza como puede, y nadie anota lo que lanza. La orden tiene que conocerlo, y qué cubre cada test, sin que nadie lo reescriba cada vez; el propietario propone, además, que la SF aprenda los tests al lanzarlos.

Opción A
:   Tres fuentes, cada test con lo que cubre, en este orden de prioridad: lo que el proyecto declara en `.sf/comprobar.json`, lo que la SF ha visto lanzar (queda anotado en `.sf/comprobaciones-vistas.json`, con su duración) y lo que detecta por el stack (pytest, vitest o jest, cargo, go, dotnet, Playwright, tsc, eslint). La SF declara las suyas ahí.

Opción B
:   Detección y declaración, sin aprender de lo lanzado: más sencilla, pero las duraciones, las órdenes propias y lo que cubre cada test hay que escribirlos a mano.

Opción C
:   Solo lo que la SF ha visto lanzar, sin detectar ni declarar: no pide nada al proyecto, pero en un proyecto nuevo no sabe qué hay y un test que nadie ha lanzado no existe para ella.

Recomendación
:   **A.** Detectar arranca en frío y encuentra lo que nadie ha lanzado; lo visto añade lo que la detección no ve y los tiempos reales; y declarar manda cuando hace falta. Cada una por separado tiene un hueco que las otras dos tapan.

### 3 · Qué tests se saltan {recomendada=A} {: #p3}

Hoy el subagente decide a ojo qué lanzar y repite comprobaciones aunque no haya cambiado nada desde que pasaron (un documento se comprueba 3 o 4 veces por tarea en la SF); otras veces se deja un test sin lanzar. La orden puede decidirlo de forma determinista: se registran todos los tests, cada uno dice qué archivos cubre, y en la ronda de selección se salta el que ningún archivo cambiado toca o el que, tocándolo, tiene el mismo hash que la última vez que pasó. El riesgo es que lo que un test dice cubrir se quede corto y se salte uno que hacía falta.

Opción A
:   Selección determinista por lo que cubre cada test, más la caché por hash. Un test sin declaración corre siempre, y antes de dejar la tarea lista para probar hay una pasada completa, sin selección ni caché (unos 2 minutos en la SF), que además avisa si algún test saltado falla.

Opción B
:   Solo la caché por hash: se lanza todo salvo lo que ya pasó con los mismos archivos; nunca se salta un test por no estar tocado.

Opción C
:   Nunca se salta nada: cada vez lanza todo.

Recomendación
:   **A.** Es determinista (los mismos archivos dan siempre la misma lista), no deja olvidos porque lo desconocido corre, y la pasada completa final atrapa un `cubre` que se quedara corto; B ahorra menos y C no ahorra las repeticiones.

### 4 · Qué hace el subagente con las capturas de pantalla {recomendada=A} {: #p4}

Además de las comprobaciones automáticas, muchos subagentes sacan capturas con Playwright y las miran: cada imagen son unos 1.500 tokens que se quedan en el contexto (583 en la SF este mes, unas 8 por subagente que las usa; 89 llamadas de Playwright en los otros proyectos).

Opción A
:   Solo si el cambio es visual o la comprobación avisa de algo que no sabe medir, y una sola imagen, con escritorio y móvil en claro y oscuro juntos, que saca la orden si se le pide.

Opción B
:   Como hoy: cada subagente las saca y las mira cuando le parece.

Opción C
:   Nunca: se fía de la comprobación, y lo visual lo ve el propietario al probar.

Recomendación
:   **A.** Quita las capturas de costumbre sin dejar a ciegas un cambio de aspecto, que la comprobación no juzga.

### 5 · Cómo se pide al subagente que la use {recomendada=A} {: #p5}

La orden solo ahorra si se usa en lugar de las sueltas, y hoy cada subagente sigue su costumbre. Lo único que leen todos los subagentes, en cualquier proyecto, es el encargo que les escribe el agente principal.

Opción A
:   El encargo lo dice: una sola llamada al acabar cada vuelta, con el plazo de 10 minutos; las órdenes sueltas, solo para depurar un fallo; y su línea «Comprobado: …» pasa tal cual al informe.

Opción B
:   Se recomienda en las skills y en el arranque, sin tocar el encargo.

Recomendación
:   **A.** Sin decirlo en el encargo, cada subagente seguiría con su costumbre.

### 6 · Qué hacer con los tests lentos {recomendada=A} {: #p6}

Un proyecto con muchos tests tarda más que el plazo de una orden y el subagente los deja en segundo plano y los vigila con más turnos. En la SF, la suite de Python seguida tarda 6 minutos; casi todo es de los tests de la cola y de un test de diagramas que pasa cada tema (67 s solo). La mayoría de los runners de otros stacks (vitest, jest, cargo, go) ya reparten solos; pytest no.

Opción A
:   Que la orden use el reparto del runner cuando lo tenga y parta en shards por archivo cuando no (pytest): en la SF, la cola baja de 148 s a 28 s y todo queda en unos 2 minutos, el tiempo de `claude plugin test`.

Opción B
:   Lo mismo y, además, una tarea para acelerar el test de los temas de la SF.

Opción C
:   Instalar `pytest-xdist`, que lo hace por su cuenta: una dependencia más en cada equipo, y solo vale para Python.

Recomendación
:   **A.** Sirve a cualquier stack sin instalar nada; con los shards, el techo de la SF es `claude plugin test`, y acelerar el test de los temas no bajaría el total.

:::

## Tareas | Las tareas que salen | Tareas {#tareas}

Si el propietario elige lo recomendado, salen cuatro tareas, en este orden. La primera lleva las preguntas [1](#p1), [2](#p2), [3](#p3) y [6](#p6); la tercera, [4](#p4) y [5](#p5).

| Tarea | Tipo | Qué hace |
| --- | --- | --- |
| Comprobar con una sola orden: selecciona en una ronda, ejecuta a la vez en otra y resume | Desarrollo | Crea `comprobar.py` en el plugin, con la detección de stacks y su reparto, la selección por lo que cubre cada test (con la medición de cobertura en la pasada completa), el registro de lo lanzado, la caché por hash, los shards, el log y sus tests; verifica las opciones de cada runner en proyectos reales; al mes, vuelve a medir el gasto con el mismo método |
| Declarar y registrar las comprobaciones de cada proyecto | Desarrollo | `.sf/comprobar.json` (a mano, con `cubre` por test) y `.sf/comprobaciones-vistas.json` (lo aprendido al lanzar, en `.gitignore`); la incorporación y «poner al día» proponen la declaración a partir de lo detectado; la SF declara las suyas |
| El encargo y las skills de documentos comprueban con la orden nueva | Desarrollo | Cambia la línea de comprobar del encargo (orquestación) y la «Comprobación» de crear_documentos y diagramas |
| Actualizar el arranque y «Cómo se desarrolla la Software Factory» | Documental | Pone en ambos la orden nueva en lugar de las tres sueltas (texto propuesto en el anexo) |

## Anexo · Cómo se midió | Método y límites | Medida {#medicion}

Las 418 transcripciones de subagentes de la SF de más de 20 kB, y 93 de otros siete proyectos del propietario (los que tienen alguna), del 25/10 al 27/11/2026, leídas por un script que no guarda nada de su contenido: por cada llamada de comprobación, su tipo (por la orden o el archivo que lee), el tamaño de su resultado y el contexto que trae el turno siguiente, el que recibe ese resultado. «Contexto releído» suma, por turno, los tokens de entrada, de caché leída y de caché creada; es la base de lo que cuesta un turno, aunque cada clase de token tiene su precio. Las imágenes cuentan como unos 1.500 tokens.

Límites: una orden que junta varias comprobaciones cuenta en la primera que nombra; una llamada repetida en una transcripción reanudada puede contar dos veces en el tamaño de los resultados, no en los turnos. En los otros proyectos hay pocos subagentes (93), concentrados en uno (42), y el stack se deduce de sus archivos y de las órdenes que lanzan: son órdenes de magnitud, no una medida fina. Los tiempos se midieron en este equipo (24 núcleos), con otras sesiones abiertas: el de la suite en paralelo es con 8 procesos a la vez, y `claude plugin test` tardó 66 s solo y 116 s acompañado. El ahorro de dos tercios es una estimación: supone pasar de unas 6 llamadas de test por vuelta a una o dos. Las opciones de los runners de la tarjeta de cada stack (`--changed`, `--changedSince`, `--only-changed`, `-p`, `go list`) salen de su documentación y no se han probado todavía.

## Anexo · Documentos compartidos | Texto propuesto para otras tareas | Documentos {#documentos}

Cuando exista la orden, el arranque (`docs/arranque-claude.md`) cambiaría su línea de comprobar el plugin por esta, con el OK del propietario:

> «Comprobar: `python -I -X utf8 plugins/sf/tools/comprobar.py`, que detecta los tests del proyecto (o los lee de `.sf/comprobar.json`), selecciona los que toca lo cambiado frente a develop (los que no declaran qué cubren corren siempre), los lanza a la vez y resume; `--todo --sin-cache` antes de dejar una tarea lista para probar. Las órdenes sueltas (`pytest`, `claude plugin test`, `claude plugin validate`), solo para depurar un fallo.»

En «Cómo se desarrolla la Software Factory», el paso 3 de comprobar quedaría: «Comprobar con `comprobar.py --todo`, que pasa `claude plugin validate`, `claude plugin test`, los tests de Python de `plugins/sf/tests/` y los documentos cambiados». La referencia de desarrollo de la metodología nombra hoy `unittest discover` para los tests de Python, cuando el arranque dice `pytest`: la tarea que la ponga al día debería dejar una sola orden. La metodología y la plantilla de proyecto añadirían la línea del encargo y la existencia de `.sf/comprobar.json`.
