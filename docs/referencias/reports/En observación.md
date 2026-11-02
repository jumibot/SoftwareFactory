# En observación: inventario de lo que habla de Testing

**Tarea 291**, paso 1. 2 de noviembre de 2026. Inventario en `develop` (5490f86), sin cambios de código: las tareas 222 y 296 cambian `cola.py` y el panel, y el cambio se hará cuando cierren. Las líneas pueden moverse; el texto citado sirve para encontrarlas.

Aplica las decisiones 204 («Los estados de las tareas se nombran con el lenguaje de la SF»), 212 («Testing pasa a llamarse «En observación»») y 215 («En observación», sin alias ni rastros).

## 0. Decidido (215, 2026-11-02)

- **Sin alias.** `a-testing` → `a-observacion`; `cerrar` vale para las en observación y `probada` desaparece; `probando` → `observando`; `pendiente` → `seguir`. Las viejas dejan de existir. Donde abajo pone «alias», no aplica.
- **Lo interno, también.** `sin-probar` → `en-observacion`; campo `probando` → `observando`; eventos con el nombre nuevo (`a-observacion`, `observando`, `seguir`; cerrar una en observación anota `cerrada`). Opción 2 de la sección 3, sin lectores que acepten los viejos salvo la migración.
- **Migración, no alias.** Las colas (y las copias de `.sf/copias/` al recuperarlas) con el estado, el campo o los eventos viejos se convierten una vez al cargarlas; también las líneas de `.sf/historial.jsonl` que se lean (reabrir, restaurar, revertir, Cerradas). Lo cubre una prueba.
- **Historia, intacta.** El historial de versiones de los documentos y las decisiones antiguas no se tocan.
- **Pregunta:** «¿Cómo va la N?» con Cerrar / Sigue en observación / La miro ahora / Revertir.
- **Pruebas a fondo**, entre ellas una que falla si reaparece el nombre viejo en el alcance (sección 8).
- **Pendiente de decidir aún:** las claves internas de botón (`a-testing-tarea`, `probada-tarea`, `quitar-probadas`) y la sección `probar` de `PLEGADAS_DE_INICIO`. Con «sin rastros», se renombran (`a-observacion-tarea`, `cerrar-observada-tarea`, `limpiar-cerradas`, `observacion`); el plegado guardado de la sección se migra al cargar el estado del panel o se pierde una vez.

## 0b. Lo que añadió la 296 (en develop, af6125c)

- `cola.py reobservar N`: una cerrada vuelve a observación con su commit de develop; botón «A observación» en Cerradas (`reobservar-tarea`), `reobservarTarea` en cola.ts, aviso en avisos.ts y pruebas en los dos tests. Ya usa el nombre nuevo en lo visible, pero escribe el estado `sin-probar` y convive con «Testing»: entra en el renombrado (estado `en-observacion`, comentarios «Testing en la cola»).
- El botón de la en curso pasará a llamarse también «A observación» (`a-observacion`): mismo rótulo para «llevar a observación» desde en curso o desde Cerradas. Las dos órdenes siguen separadas (`a-observacion` cierra con squash; `reobservar` no toca git).

## 1. Dos sentidos de «probar»

- **Sentido del estado (se cambia).** Testing, «sin probar», «probada», «dar por probada», «Probar ahora», «pendiente de prueba», «¿está probada?», «cerrar sin probar (a Testing)», «lo cerrado queda por probar». Una tarea en observación ya está en `develop`: se **cierra** (va bien) o se **revierte** (va mal).
- **Sentido real (se queda).** Probar una tarea en curso en su rama antes de cerrarla: «Activar rama», el paso «Activar rama para poder probar», `cola.py probar` (activa la rama), `listo --prueba "qué mirar"`, las ayudas de prueba, el desplegable «Prueba» («Comprobado por Claude», «Qué mirar»), «proponer probar, con cómo», «lista para probar». También el aviso «Probando la N: rama … activa».
- **Caso frontera.** «cerrar sin probar» como frase de A Testing: cambia. «se cierra sin probar» de lo que no tiene nada que probar (154): es sentido real, se queda.

## 2. Nombres propuestos (para decidir)

| Hoy | Propuesta | Alias |
|---|---|---|
| Estado «Testing», sección «Testing» | **En observación** | — |
| Cabecera «testing N» | «observación N» | — |
| `nombre_estado`: «en Testing» | «en observación» | — |
| Orden `a-testing` | **`a-observacion`** | `a-testing`, oculto en la ayuda |
| Botón «A Testing» («¿A Testing? sí») | **«A observación»** («¿A observación? sí») | — |
| Orden `probada` | **`cerrar`** también para una en observación (A); o `cerrar-observada` (B) | `probada`, oculto |
| Botón «Cerrar» en Testing | igual, «Cerrar» | — |
| Orden `probando` («Probar ahora») | **`observando`** | `probando` |
| Orden `pendiente` («sigue en Testing») | **`seguir`** («sigue en observación») | `pendiente` |
| Pregunta «¿está probada?»: Probada / Pendiente / Probar ahora | **«¿Cómo va la N?»: Cerrar / Sigue en observación / La miro ahora / Revertir** | — |
| Letra T (color de En observación) | **O** | — |
| `probar` (activa la rama), «Activar rama», paso «Activar rama para poder probar» | sin cambio (sentido real) | opcional: `activar-rama` como alias de `probar` |

Recomendación: opción A para `probada`: el botón ya se llama Cerrar y cerrar es lo que dice la 204; `o_cerrar` decide por el estado. Los alias, en argparse con `aliases=[…]` (ya se usa en `paso añadir`/`anadir`) y fuera del texto de uso, para no dejar rastro visible.

## 3. Lo interno: cambiar o dejar

| Interno | Dónde | Opción 1: se deja | Opción 2: se cambia |
|---|---|---|---|
| Estado `sin-probar` | cola, copias, `ESTADOS` (cola.py 66), `ESTADOS_PETICION` (constantes.ts 33), `Peticion.estado` (types 10), unas 25 comparaciones en cola.py, cola.ts y panel.tsx | Sin migración; pero `sin-probar` («sin probar») sigue en skills y documentos, que Claude lee y repite | **`en-observacion`**, renombrado al cargar la cola (precedente: el paso «Probar la tarea», 172); el panel acepta los dos hasta que `cola.py` escribe |
| Campo `probando` | cola, types 16, lectura.ts 71, cola.ts 43 | Se deja | `observando`, renombrado al cargar |
| Eventos `a-testing`, `probada`, `probando`, `pendiente` | historial de cada tarea y `.sf/historial.jsonl` | Se dejan; los nuevos órdenes escriben los nombres viejos | Los nuevos se escriben con el nombre nuevo (`a-observacion`, `cerrada` con detalle «en observación», `observando`, `seguir`); los lectores (`CIERRES` en lectura.ts 106, `commitsDe` 130/140, cola.py 254/449, avisos.ts) aceptan los dos. El historial no se reescribe |
| Claves de botón `a-testing-tarea`, `probada-tarea`, `quitar-probadas`; sección `probar` en `PLEGADAS_DE_INICIO` | panel.tsx 105-106, 946, 817; constantes.ts 55 | Se dejan (no se ven) | Renombrar; la sección `probar` perdería el plegado guardado del propietario |
| Funciones `probadaTarea`, `revertibleEnTesting`, `o_a_testing`, `o_probada`, `o_probando`, `aTesting`, `secSinProbar`, `sinProbar` | cola.ts, panel.tsx, cola.py | — | Renombrar sin coste (`cerrarObservada`, `revertibleEnObservacion`, `o_a_observacion`…) |

**Recomendación:** opción 2 para el estado y para el campo (migración al cargar, como en la 172, una línea por campo), porque deja limpio lo que leen Claude y los documentos; eventos con el nombre nuevo y lectores que aceptan los dos; claves de botón y de sección, se dejan; funciones, se renombran. Si se prefiere mínimo riesgo: opción 1 en todo lo interno y quitar `sin-probar` de los textos que lee Claude, salvo el esquema de datos de `estados.md`.

## 4. Inventario: código

V = visible (texto, botón, ayuda, mensaje); I = interno. Comentarios del código: se reescriben con el vocabulario nuevo al tocar cada sitio.

### plugins/sf/tools/cola.py

| Línea | Hoy | Propuesta | |
|---|---|---|---|
| 10 | «un cierre, una reversión o un «probar» que choca» | se queda (sentido real) | V |
| 20 | `probar N \| probando N \| pendiente N   cerrar N \| a-testing N [--prueba P] \| probada N` | `probar N \| observando N \| seguir N   cerrar N \| a-observacion N [--prueba P]` | V |
| 38-39 | «Cerrar, también a Testing, pide…» | «Cerrar, también a observación, pide…» | V |
| 41 | «(cerrar, a-testing, probada, descartar…» | «(cerrar, a-observacion, descartar…» | V |
| 53 | «con las en curso o en Testing» | «… o en observación» | V |
| 66 | `ESTADOS = (…, 'sin-probar', …)` | `'en-observacion'` + migración al cargar | I |
| 246 | `'sin-probar': 'en Testing'` | `'en-observacion': 'en observación'` | V |
| 254-255 | evento `probada` → «cerrada y probada» | «cerrada en observación» (y aceptar el evento nuevo) | V/I |
| 449 | `('cerrada', 'a-testing')` | añadir `'a-observacion'` | I |
| 604 | docstring «cerrar, a Testing, probada, …» | «cerrar, a observación, …» | I |
| 625 | `" · probando"` en `lista` | `" · observándola"` | V |
| 671 | «ciérrala, pásala a Testing o descártala» | «ciérrala, pásala a observación o descártala» | V |
| 695-696 | «También en Testing: la que el propietario está probando…» | «… en observación: la que el propietario está mirando…» | I |
| 923-928 | `o_probando`; «La N, en prueba.» | `o_observando`; «La N, en observación: la estás mirando.» | V/I |
| 931-936 | `o_pendiente`; «La N sigue en Testing.» | `o_seguir`; «La N sigue en observación.» | V/I |
| 940 | «(C o a Testing)» | «(C o a observación)» | I |
| 1023-1045 | `o_a_testing`; evento `a-testing`; «La N, en Testing{detalle}.» | `o_a_observacion`; «La N, en observación{detalle}.» | V/I |
| 1048-1058 | `o_probada`; evento `probada`; «Probada la N: sale de la cola.»; comentario «al pasarla a Testing» | dentro de `o_cerrar` para una en observación; «Cerrada la N: sale de la cola.» | V/I |
| 1063-1064 | «La N está en Testing: ya entró en develop; se revierte» | «… en observación: …» | V |
| 1111 | «solo se revierte una en Testing o cerrada» | «… en observación o cerrada» | V |
| 1148 | comentario «al pasarla a Testing» | «a observación» | I |
| 1641 | «La N está en Testing: no se fusiona.» | «… en observación: …» | V |
| 1890 | «ni en Testing» | «ni en observación» | V |
| 2018-2024 | ayudas: `probando` «el propietario la prueba ahora»; `pendiente` «sigue en Testing»; `a-testing` «cierra sin probar: squash en develop y a Testing»; `probada` «de Testing, fuera de la cola» | `observando` «el propietario la mira ahora»; `seguir` «sigue en observación»; `a-observacion` «cierra y la deja en observación: squash en develop»; `cerrar` «… o, en observación, la saca de la cola»; alias ocultos | V |
| 2049 | ayuda `choques` «o en Testing» | «o en observación» | V |
| 16, 19, 44-45, 71-73, 284, 313-314, 717, 814, 865-914, 976, 1015, 1996, 2013-2017 | «Activar rama para poder probar», `probar`, «lista para probar», `--prueba` | se quedan (sentido real) | V |

`cola_sesion.py`: nada (su «prueba» es una configuración de prueba).

### plugins/sf/hooks

| Archivo:línea | Hoy | Propuesta | |
|---|---|---|---|
| avisos.ts:50 | `probando: «la N, en prueba»` | `observando: «la N, la estás mirando»` (y `probando` igual, para el historial viejo) | V |
| avisos.ts:51 | `pendiente: «la N, sin probar aún»` | `seguir`/`pendiente`: «la N, sigue en observación» | V |
| avisos.ts:54 | `'a-testing': «la N, a Testing»` | `'a-observacion'` y `'a-testing'`: «la N, a observación» | V |
| avisos.ts:55 | `probada: «probada la N»` | «cerrada la N» (los dos eventos) | V |
| avisos.ts:47, 49 | «lista para probar», `probar`: «en prueba» | se quedan (sentido real) | V |
| cola.ts:40-43 | comentario «(«Probar ahora»)… los de Testing»; `'sin-probar' && p.probando` | «(«La miro ahora»)… en observación»; estado y campo nuevos | I |
| cola.ts:194-207 | comentarios «en Testing»; `revertibleEnTesting` | «en observación»; `revertibleEnObservacion` | I |
| cola.ts:279-297 | comentarios «probada, ciérrala», «A Testing»; `orden: 'a-testing'`; letra «A Testing»; «Pasa a Testing la N…»; «A Testing del panel no pudo» | `'a-observacion'`; «A observación»; «Pasa a observación la N…» | V |
| cola.ts:311-317 | `probadaTarea`; «dar por probada… es cerrarla»; `['probada', N]` | `cerrarObservada`; `['cerrar', N]` | I |
| cola.ts:716, 742, 754 | comentarios «o en Testing»; «La T… de Test Mode… sin darla por probada» | «o en observación»; «Activar rama… sin darla por buena» | I |
| cola.ts:784 | `conLetra('T', r)` (prefijo del mensaje de fallo de Activar rama) | `conLetra('Activar rama', r)` | V |
| cola.ts:803 | comentario «las probadas (C)» | «las cerradas (C)» | I |
| cola.ts:833 | «?» de paso: «Explica para qué sirve Testing (lo que se cierra quedando aún por probar) y qué pasa si no se prueba.» | «Explica para qué sirve En observación (ya está en develop y se vigila cómo funciona con el uso, para cerrarla o revertirla) y qué pasa si se cierra sin observarla.» | V (prompt a Claude) |
| cola.ts:989, 1003 | «Las de Testing…»; «La N está en Testing: no se fusiona.» | «en observación» | V |
| cola.ts:168-173 | «Activar rama para poder probar» / «Probar la tarea» | se quedan | I |
| constantes.ts:33 | `'sin-probar'` | `'en-observacion'` (+ `'sin-probar'` aceptado al leer) | I |
| constantes.ts:55 | `PLEGADAS_DE_INICIO = ['probar', …]` | se deja (clave de sección) | I |
| lectura.ts:71 | `probando: p.probando === true` | `observando`, aceptando el viejo | I |
| lectura.ts:104-106 | comentario «su paso a Testing, su prueba»; `CIERRES = ['a-testing', 'cerrada', 'probada', …]` | «su paso a observación»; añadir los eventos nuevos | I |
| lectura.ts:123-140 | comentario y `'a-testing'` | añadir `'a-observacion'` | I |
| panel.tsx:103-106 | comentarios; `aTesting: { nombre: 'A Testing', …, clave: 'a-testing-tarea' }`; `probada: { nombre: 'Cerrar', …, clave: 'probada-tarea' }` | `nombre: 'A observación'`; claves, se dejan (o se renombran) | V |
| panel.tsx:172 | `` `testing ${…}` `` (cabecera) | `` `observación ${…}` `` | V |
| panel.tsx:239, 254 | letra T «en Testing»; `'sin-probar' → 'T'`; «C: cerrada y probada» | letra O; «C: cerrada» | I (da el color) |
| panel.tsx:321, 505-509 | comentarios «Activar rama para poder probar»; «sin darla por probada» | «sin darla por buena» | I |
| panel.tsx:426-480 | comentarios «A Testing», «Cerrar en Testing la da por probada», «En Testing, Revertir…»; `accion === 'aTesting'`; mensaje «No se pudo pasar a Testing la N» | «A observación», «Cerrar en observación la saca»; «No se pudo pasar a observación la N» | V |
| panel.tsx:563-574 | comentario «Pendientes (cola) y Testing (probar)»; `'sin-probar'` | «En observación» | I |
| panel.tsx:600, 611, 697, 1269-1270 | comentarios «En Testing o la que se prueba» | «En observación o la que se mira» | I |
| panel.tsx:817 | `['sin-probar', 'probar', 'Testing', true]` | `['en-observacion', 'probar', 'En observación', true]` | V |
| panel.tsx:821-829, 907, 974-976, 1319, 1330 | comentarios «Testing», «probadas (C)» | «En observación», «cerradas (C)» | I |
| panel.tsx:926, 936 | comentarios «probadas (C)» | «cerradas (C)» | I |
| panel.tsx:832, 1100 | `secSinProbar`, `sinProbar` | `secObservacion`, `enObservacion` | I |
| panel.tsx:1195-1197 | RELEASE: «N sin probar: 4, 47» | «N en observación: 4, 47» | V |
| panel.tsx:1418 | comentario «las tareas que quedan en Testing» | «en observación» | I |
| panel.tsx:523-525, 643-653 | «Activar rama», «Prueba», «Comprobado por Claude», «Qué mirar» | se quedan | V |

### plugins/sf/types/index.d.ts

| Línea | Hoy | Propuesta | |
|---|---|---|---|
| 10 | `estado: … \| 'sin-probar' \| …` | `'en-observacion'` | I |
| 11 | «qué debe comprobar el propietario (sin-probar)» | «(en curso o en observación)» | I |
| 12 | «su OK, que no la saca de Testing» | «… de En observación» | I |
| 16 | `probando: boolean // en Testing y el propietario la está probando ahora` | `observando: boolean // en observación y el propietario la está mirando ahora` | I |

### plugins/sf/tests

- **test_cola.py** (74 líneas con el vocabulario): órdenes `a-testing` (30 usos), `probada` (11), `probando`, `pendiente`; mensajes esperados «La 18, en Testing.», «La 12, en Testing en develop (c0ffee1).», «La 2 está en Testing: no se fusiona.», «ciérrala, pásala a Testing o descártala», «Tarea 9: en Testing»; el estado `'sin-probar'`. Se cambian a los nombres y mensajes nuevos, y se añaden pruebas de los alias (`a-testing`, `probada`, `probando`, `pendiente` siguen funcionando) y de la migración al cargar (`sin-probar` → `en-observacion`, `probando` → `observando`).
- **panel.test.tsx** (159): textos esperados `'En Testing'`, `'Testing'`, «A Testing», «¿A Testing? sí», «Pasa a Testing la 12», «sin probar» del RELEASE, letra T; nombres de casos («Testing: plegadas y desplegadas…», «Cerrar en Testing: … cola.py probada…», «A Testing: junto a Cerrar…», «RELEASE: … avisa de lo sin probar», «Probar: T en las que tienen rama…»); claves `a-testing-tarea:…`, `probada-tarea:…`, `quitar-probadas`. Se cambian los textos y los nombres de caso; las claves, según lo que se decida en 3. Añadir: una cola vieja con `sin-probar` sale en «En observación».

## 5. Inventario: skills, plantillas y documentos

### plugins/sf/skills/flujo_tareas

| Archivo:línea | Hoy | Propuesta |
|---|---|---|
| SKILL.md:3 (description) | «estados (en cola, en curso, Testing, descartada)… dejarla lista para probar, cerrarla, pasarla a Testing, darla por probada…» | «estados (en cola, en curso, en observación, descartada)… dejarla lista para probar, cerrarla, pasarla a observación, cerrarla o revertirla en observación…» |
| SKILL.md:20 | «(su OK a cerrar, su «probada»)» | «(su OK a cerrar)» |
| SKILL.md:31 | «`cerrar`, `a-testing`, `probada` y `descartar` lo esperan…; se cierra, se pasa a Testing o se descarta» | «`cerrar`, `a-observacion` y `descartar`…; se cierra, se pasa a observación o se descarta» |
| SKILL.md:35 | lista de recogida «`cerrar`, `a-testing`, `probada`, …» | «`cerrar`, `a-observacion`, …» |
| SKILL.md:45-46 | tabla: Prueba `listo`, `comprobado`, `probar`, `probando`, `pendiente`; Cierre `cerrar`, `a-testing`, `probada` | Prueba `listo`, `comprobado`, `probar`; Observación `observando`, `seguir`; Cierre `cerrar`, `a-observacion` |
| SKILL.md:52 | «Todo cierre (`cerrar`, `a-testing`)» | «(`cerrar`, `a-observacion`)» |
| references/estados.md:15 | «`sin-probar`, que el panel y los documentos llaman Testing: cerrada sin el OK del propietario a su funcionamiento… Espera ese OK» | «`en-observacion` (En observación): ya en `develop` por squash (con rama); se vigila cómo funciona con el uso y se cierra o se revierte (204, 212).» |
| :20 | «`probando: true`: solo en `sin-probar`. El propietario la prueba ahora («Probar ahora»)… con su código de Testing, «66-T»» | «`observando: true`: solo en observación. El propietario la está mirando («La miro ahora»)… en amarillo» (el «66-T» ya no existe: sin letras tras el número) |
| :26 | «Cerrada y probada: salió por la C, por un OK de prueba…» | «Cerrada: salió por la C, cerrada en observación o por un cierre sin rama» |
| :29, 326, 332, 360, 361, 372 | «en Testing», «Pendientes y Testing», «desde Testing», «(cerrada, probada, revertida)» | «en observación», «(cerrada, revertida)» |
| :46-47 | «T: en Testing (`sin-probar`)»; «C: … cerrada y probada» | «O: en observación»; «C: … cerrada» |
| :59, 226, 228 | ««✓» verde en Testing»; «No saca la tarea de Testing» | «en observación» |
| :64, 503, 511, 513, 517 | eventos `a-testing`, `probada`, `probando`, `pendiente`; «al darla por probada» | eventos nuevos (y los viejos, «de antes de la 291»); «al cerrarla en observación» |
| :101, 113 | «en curso o en Testing»; «se pasa a Testing» | «en observación»; «se pasa a observación» |
| :215, 217 | «sin pasar por Testing»; panel «Cerrar» y «A Testing» | «sin pasar por observación»; «A observación» |
| :240 | «entrar en prueba no es estar probada; el OK del propietario es cerrar» | «activar la rama no es darla por buena; el OK del propietario es cerrar» |
| :243-251 | «16 · Probar ahora»; «a la pregunta «¿está probada?»… «Probar ahora»»; `cola.py probando 66`; «con su T» | «16 · Mirarla ahora»; «a «¿Cómo va la 66?», responde «La miro ahora»»; `cola.py observando 66` |
| :253-261 | «17 · Seguir pendiente de prueba»; «respuesta «Pendiente», o la prueba queda a medias»; «vuelve a Testing»; `cola.py pendiente 66` | «17 · Seguir en observación»; «respuesta «Sigue en observación»»; `cola.py seguir 66` |
| :270 | «Pulsar la C equivale a «probada, ciérrala»» | «Pulsar la C es el OK del propietario: «ciérrala»» |
| :292 | «(no pasa por Testing)» | «(no pasa por observación)» |
| :300-308 | «21 · Cerrar sin probar (a Testing)»; «Panel con «A Testing»»; «Testing, con T; Cerradas, con T»; `cola.py a-testing 92` | «21 · Cerrar y dejar en observación»; «A observación»; «En observación; Cerradas, con O»; `cola.py a-observacion 92` |
| :303 | «hay algo que probar y el cierre hace falta para poder probarlo (un commit o una publicación)» | «el resultado solo se puede ver funcionando tras el cierre (un commit o una publicación): se cierra y se observa» |
| :311-319 | «22 · Dar por probada»; ««Probada», o «probada» sin número…»; «ya entró en develop al pasar a Testing»; `cola.py probada 66` | «22 · Cerrar en observación»; «el propietario da el OK («ciérrala»; sin número, la de la rama activa)»; «al pasar a observación»; `cola.py cerrar 66` |
| :331 | «`a-testing`, `probada`, …» | «`a-observacion`, …» |
| :482-485 | campo `probando`; «`commit`: … lo pone `a-testing`» | campo `observando`; «lo pone `a-observacion`» |
| :87, 98, 133, 155 | paso «Activar rama para poder probar» | se queda |

### plugins/sf/skills/orquestacion

| Archivo:línea | Hoy | Propuesta |
|---|---|---|
| SKILL.md:55 | «El cierre, `a-testing`, `probada`, `descartar` y la publicación esperan el OK» | «El cierre, `a-observacion`, `descartar` y la publicación esperan el OK» |
| SKILL.md:56 | «El worktree sigue mientras se prueba: la T y la C funcionan con él puesto.» | «… Activar rama y la C funcionan con él puesto.» (la T ya no existe) |
| SKILL.md:57 | ««Probada» sin número es la tarea de la rama activa» | ««Ciérrala» sin número es la tarea de la rama activa» |
| SKILL.md:58 | «Antes de pasar a otra, preguntar por las de Testing: … con Probada, Pendiente y Probar ahora. Con Probar ahora, `probando` y esperar» | «Antes de pasar a otra, preguntar por las en observación: … «¿Cómo va?» con Cerrar, Sigue en observación, La miro ahora y Revertir. Con La miro ahora, `observando` y esperar» |
| SKILL.md:75 | «(no las de Testing)» | «(no las en observación)» |
| SKILL.md:53-54 | «Activar rama para poder probar», «proponer probar», «se cierra sin probar» | se quedan |
| references/porque.md:53 | «Testing se llenaba de tareas cerradas sin probar» | «En observación (antes Testing) se llenaba de tareas cerradas sin probar en su rama» |
| references/porque.md:56 | ««Probada» sin número, la rama activa (095)» | ««Ciérrala» sin número, la rama activa (095)» |
| references/porque.md:57 | «La pregunta de «¿está probada?» (050, 051)» | «La pregunta de «¿Cómo va?» por las en observación (050, 051)» |

### Otras skills y plantillas

| Archivo:línea | Hoy | Propuesta |
|---|---|---|
| metodologia/SKILL.md:36 | «`sin-probar` —Testing— con su `prueba`» | «en observación, con su `prueba`» |
| metodologia/references/desarrollo-de-proyectos.md:52 | «el cierre por squash, Testing, descartar…» | «… En observación, descartar…» |
| …desarrollo-de-proyectos.md:54 | «solo propone cerrar sin probar si la prueba necesita el cierre… y el paso a Testing esperan el OK… pregunta si la cerrada se da por probada o se prueba en ese momento» | «solo propone cerrar y dejarla en observación si verla funcionar necesita el cierre… y el paso a observación esperan el OK… pregunta por la que está en observación si se cierra, sigue en observación o se revierte» |
| …desarrollo-de-proyectos.md:59 | «se cierra al anotarla, sin Testing» | «sin pasar por observación» |
| incorporar_proyecto_a_sf/SKILL.md:108 | «Lo que no se ha podido comprobar queda en Testing (`sin-probar`) en la cola, con qué probar» | «queda en observación en la cola, con qué mirar» |
| templates/claude-sf.md | solo «prueba» en sentido real | nada |

Falsos positivos en skills (no se tocan): `webapp-testing` (diseno_interfaz:68), «aprobado», «comprobado», «probada» de una plantilla (infografia_tecnica:10), «está probado en la SF» (incorporar:27), «Sin probar» de la tabla de skills del README (99-100: estado de validación de una skill, no de una tarea).

### Documentos compartidos (los cambia su tarea «Actualizar <documento>»)

**docs/como-funcionan-los-estados.md** (27 sitios): 5 («la T, hoy Activar rama»: se queda); 9 «en cola, en curso, Testing y descartada» → «en observación»; diagrama SVG 12-60: aria-label, «A Testing: cerrar sin probar» → «A observación: cerrar y observar», nodo «Testing» → «En observación», «Cerrar: probada» → «Cerrar: va bien», «Cerrar: probada y cerrada» → «Cerrar», «desde Testing…» → «desde En observación…»; 66, 68, 92, 98, 104, 106, 108, 112, 124, 147 «Testing», «A Testing», «a-testing», «probada»; 72 marca «probando», «Probar ahora», «Pendiente» → «observando», «La miro ahora», «Sigue en observación»; 80 «dar por probada» → «cerrar en observación»; 102 «es decir «probada, ciérrala»» → «es tu OK: «ciérrala»»; 108 «(`cola.py probada`): darla por probada es cerrarla. También vale decir «probada»» → «(`cola.py cerrar`)… También vale decir «ciérrala»»; 114 «Entrar en prueba no es estar probada… no da la tarea por probada» → «Activar la rama no es darla por buena». Añadir que se revierte si funciona mal (204).

**docs/como-funciona-el-panel.md** (44 sitios): 31 (SVG) «Pendientes, Testing y Cerradas» → «Pendientes, En observación y Cerradas»; 148, 235, 296, 298, 302, 310-311, 323, 331-334, 338 «Testing», «T: en Testing», «C: cerrada y probada», «la que estás probando, la del campo `probando`», «en Testing, «probar: …»»; 391 título «### Testing» → «### En observación»; 396-447 SVG y pie («Tareas en Testing», «con la T; esperan tu prueba» → «se cierran o se revierten»); 450 «No la saca de Testing… «probar: …»» → «de En observación… «Qué mirar»»; 454, 462 «a Testing, cerrada, probada», «las cerradas y probadas»; 679 «testing»: las de Testing» → «observación»; 691-814 la sección de botones está desfasada entera (T de Test Mode, «Probar la tarea», C, S, E): se reescribe con las etiquetas de hoy (Activar rama, Cerrar, A observación, Revertir…), no solo el nombre; 826, 860 («2 sin probar: 4, 47» → «2 en observación: 4, 47»), 924, 988. Historial de versiones (995-1094): ver la decisión 4 de abajo.

**docs/como-funciona-la-software-factory.md**: 184 (SVG) y 197 «Pendientes, Testing y Cerradas»; 256 «las tareas que quedan en Testing» → «en observación».

**docs/specs/funcional/software-factory.md**: 173 «Testing con qué comprobar» y «T, en Testing; y C, cerrada y probada»; 176 «(a Testing, probadas o reabiertas…)» → «(a observación, cerradas o reabiertas…)»; 177 «Tarea que se está probando… con «Probar ahora»… su código de Testing, «66-T»» → «Tarea que se está mirando… con «La miro ahora»…»; 180 «lo cerrado queda en Testing (`sin-probar`) con qué probar» → «queda en observación con qué mirar»; 163 «una vez probada» (sentido real, en su rama): se queda.

**docs/mejora-continua-a-la-software-factory.md**: 169 «(«probada, ciérrala»)… queda en Testing con su `prueba`» → «(«ciérrala»)… queda en observación con su `prueba`»; 98-99 (registro de una decisión, «quitar las probadas»): histórico, se queda; 45, 157, 179, 183, 204 «probada» en su rama: sentido real, se queda.

**docs/uso-del-panel.md:8**: «qué queda en Testing» → «qué queda en observación».

**CLAUDE.md**: nada (el «aprobadas» de la línea 16 es un falso positivo). **README.md:148** «probada, entra en `develop`»: sentido real (probada en su rama), se queda.

Los `.html` de los documentos se regeneran desde el `.md`.

## 6. Fuera del alcance (no se tocan)

- `docs/decisiones/`: es registro histórico; la 212 ya dice el cambio.
- `docs/referencias/` (research notes, inventarios, informes), `docs/specs/vision/` y `_respaldo/`: «testing» en sentido general (pruebas de software) o histórico.
- `ORIGIN.md` de las skills: procedencia.

## 7. Decisiones del propietario

Resueltas en la 215 (sección 0): nombres (tabla 2, opción A, `seguir` para `pendiente`), sin alias, valor interno renombrado con migración, historial de versiones y decisiones intactos. Queda solo lo de las claves internas de botón y de sección (sección 0).

## 8. Pruebas previstas (pasos 6 y 7)

- **Migración (test_cola.py):** una cola con `sin-probar`, `probando: true` y eventos `a-testing`, `probada`, `probando`, `pendiente` se carga y queda con `en-observacion`, `observando` y los eventos nuevos, una sola vez (cargarla otra vez no cambia nada); lo mismo con una copia recuperada y con una línea de `historial.jsonl` reabierta o revertida.
- **Órdenes viejas, fuera:** `a-testing`, `probada`, `probando` y `pendiente` salen con 2 (orden mal escrita); las nuevas hacen lo de antes; `cerrar` de una en observación la saca sin git; `reobservar` deja `en-observacion`.
- **Panel (panel.test.tsx):** sección «En observación», cabecera «observación N», botón «A observación» con «¿A observación? sí», RELEASE «N en observación: …», avisos de los eventos nuevos; una cola vieja leída por el panel antes de que escriba `cola.py` sale en «En observación».
- **Sin rastros:** una prueba recorre `plugins/sf` (hooks, tools, skills con references, templates, types y los tests, salvo la lista de nombres prohibidos y los datos de migración) y los documentos del alcance (como-funciona*, como-funcionan-los-estados, especificación funcional, mejora-continua, uso-del-panel, CLAUDE.md, README), y falla si encuentra `Testing`, `sin-probar`, `probada`, `probando`, `a-testing`, «Probar ahora», «dar por probada» o «sin probar» referido al estado. Excluye, con lista explícita: `docs/decisiones/`, las tablas de historial de versiones, `docs/referencias/`, `docs/specs/vision/`, `_respaldo/`, `ORIGIN.md` y los falsos positivos conocidos (`webapp-testing`, la columna «Sin probar» de skills del README, «comprobado», «aprobado»). Va en test_cola.py (pytest), para que corra con las demás.

## 9. Hecho (pasos 5 a 7)

- **cola.py:** órdenes `a-observacion`, `observando`, `seguir`; `cerrar` saca una en observación sin git (evento `cerrada`, «en observación»); fuera `a-testing`, `probada`, `probando` y `pendiente`, sin alias. Estado `en-observacion`, campo `observando`. `migrar_tarea` convierte al cargar la cola, al leer el historial y las copias y al recuperar una; `guardar` reescribe una vez `.sf/historial.jsonl` si trae lo de antes. El aviso de Activar rama dice «La N, en prueba: rama … activa».
- **Panel:** sección «En observación» (clave `observacion`), cabecera «observación N», botón «A observación» (`a-observacion-tarea`), Cerrar en observación (`cerrar-observada-tarea`), «Limpiar» (`limpiar-cerradas`), letra O, RELEASE «N en observación: …», el «?» de los pasos de cierre, avisos de los eventos nuevos. Lee ya convertidos la cola, el historial y el plegado guardado, que reescribe una vez (`migrarPlegado`). Los restos de la T de antes, a Activar rama.
- **Skills:** flujo_tareas (SKILL.md y estados.md, con la tarjeta 22 bis de la 296), orquestacion (pregunta «¿Cómo va la N?» con Cerrar, Sigue en observación, La miro ahora y Revertir) y su porqué.
- **Pruebas:** test_cola.py, clase `Migracion215` (cola, lista y ver, órdenes nuevas sobre cola vieja, historial, copias, órdenes viejas con salida 2); panel.test.tsx, dos de migración (cola vieja y plegado e historial); test_sin_nombres_viejos.py, que recorre el alcance con la lista de exclusiones de su cabecera y deja fuera, hasta su tarea, los documentos compartidos (`EN_SU_TAREA`: cuando uno se ponga al día, la prueba pide sacarlo de la lista).
- **Pendiente en su tarea:** los documentos compartidos de la sección 5, y además `plugins/sf/skills/metodologia/SKILL.md:36` («`sin-probar` —Testing— con su `prueba`» → «`en-observacion` —En observación— con su `prueba`»).
