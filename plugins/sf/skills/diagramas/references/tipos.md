# Tipos de diagrama

Los 45 tipos de diagram-design (commit `f24d98b`), con sus convenciones y límites, y su forma vertical en la SF. Se elige por lo que se quiere enseñar; si dos encajan, el del eje dominante; si una tabla de tres columnas dice lo mismo, la tabla. El detalle fino de cada tipo, en `references/type-<tipo>.md` del repositorio de origen, en ese commit.

**Primero el comportamiento.** Si lo que importa es cómo se comporta (un cuello de botella, un ciclo de vida con esperas y salidas, controles por dónde se aplican), se elige antes el patrón y luego el tipo:

| Si lo importante es… | Patrón → tipo |
|---|---|
| Un sujeto que pasa por 4–5 fases, con esperas, reintentos, cancelación y finales | Mapa de fases de un ciclo de vida → Estados: fases en la columna, esperas a un lado, finales en otra banda; ≤ 9 estados, ≤ 10 transiciones |
| Entradas que convergen, cola, capacidad finita | Cuello de botella → Flujo de datos |
| Las mismas casillas (pregunta, entrada, control, salida) en cada etapa | Etapas con casillas → Proceso |
| Una conversación que se vuelve un artefacto estructurado | De lo suelto a lo estructurado → Flujo de datos |
| Dos recorridos de reglas que divergen | Trazas de evaluación → Flujo |
| Fronteras de confianza y caminos permitidos o prohibidos | Camino seguro → Arquitectura |
| Controles agrupados por dónde se aplican, o capas que compensan huecos | Catálogo de controles → Capas |
| Bloques con id, entradas, salidas y enlace al código | Descomposición trazable → Árbol |

El patrón pone sus piezas y un presupuesto más estricto; el tipo pone la maquetación.

## Los más usados en la SF

| Tipo | Para | Convenciones | Límite | En vertical |
|---|---|---|---|---|
| **Estados** | Estados, transiciones y condiciones | Cajas `rx=8`; inicio, punto lleno `r=6`; fin, punto con anillo; cada transición con su `evento [condición] / acción`; foco en el estado del que se habla o en el error | transiciones ≤ 2 × estados | Camino principal en la columna; vueltas y salidas a los lados, con carril con nombre; «desde cualquier estado», una nota |
| **Flujo** | Decisiones con ramas | La forma dice el tipo, no el color: óvalo inicio y fin, caja paso, rombo decisión (≤ 3 salidas), punto donde se juntan ramas; toda salida etiquetada | 9 nodos | Baja; Sí a la derecha, No abajo; un puente si dos flechas se cruzan |
| **Secuencia** | Mensajes en el tiempo entre actores | Líneas de vida, mensajes horizontales, la respuesta principal en el foco; `alt` y `opt` como marcos | 5 actores, 1 marco (2 si son simples), 2 regiones `alt` | Con 2–3 actores cabe a 400; con más, horizontal a 960 y en vertical una lista de pasos «actor → actor: mensaje» |
| **Arquitectura** | Piezas y conexiones en un momento | Agrupar por capa o frontera de confianza; un sentido de lectura; fronteras con rectángulo discontinuo y su nombre sobre máscara; foco en la integración o el almacén clave | 9 nodos | Capas de arriba abajo, una banda por zona; en cada banda, hasta tres cajas por fila (dos a 400 con nombres cortos; un nombre largo, en dos líneas) |
| **Capas** | Niveles de abstracción apilados | Bandas del mismo ancho, 4–6; índice a la izquierda, nombre, nota a la derecha; separadores finos; flecha de sentido fuera, a la izquierda | 6 capas | Ya es vertical; la nota debajo del nombre |
| **Árbol** | Padre → hijos | Bus ortogonal: bajada del padre, horizontal, bajadas a los hijos; 2 anchos de caja como mucho | profundidad 4, 5 por nivel | Sangrado: cada nivel 24 a la derecha, una fila por nodo |
| **Línea de tiempo** | Hechos en el tiempo | Un eje, marcas con fecha, foco en el hito | — | Eje vertical a la izquierda, un hecho por fila |
| **Carriles** | Proceso entre equipos con traspasos | Un carril por actor, el traspaso cruza carriles | 5 carriles | Carriles como columnas estrechas (2–3) o bandas apiladas por etapa |
| **Proceso** | Pasos con actor, datos que entran y salen, herramientas | Etiquetas ≤ 9 caracteres; ≤ 3 colores además del foco; las flechas no toman el color de la pieza | 9 pasos | Un paso por fila; actor y datos en la línea de detalle |
| **Flujo de datos** | Quién inicia, procesa, publica y consume | Roles por columnas o bandas; ≤ 3 colores de pieza | 9 nodos | Roles apilados; los datos bajan |
| **Fases** (mapa de fases) | Etapas de un método o un ciclo | Una línea de fases; lo que deja cada una debajo | 8 | Una fase por fila |
| **Bucle** | Ciclo que se refuerza, con un núcleo que acumula | 5–8 estaciones y un solo núcleo; el trabajo gira en sentido horario | 8 estaciones | Cuadrado de 400 con el núcleo en el centro, o columna que vuelve arriba |
| **Anidado** | Jerarquía por contención o alcance | 3–5 rectángulos `rx=8` con margen constante; nombre de cada nivel arriba a la izquierda, sobre máscara; trazos de fuera más tenues; foco en el de dentro | 6 niveles | Ya cabe: margen de 16 por nivel |
| **Organigrama** | Quién es dueño, a quién se escala | Raíz arriba; nombre, cómo se le invoca y alcance en 2–4 palabras; los que aún no existen, discontinuos | 12 nodos, profundidad 4 | Sangrado, como el árbol |
| **ER** | Entidades, campos y relaciones | Caja con cabecera y lista de campos; `#` clave, `→` ajena; cardinalidad junto a cada extremo | 8 entidades | Entidades apiladas, relaciones por el lateral |
| **Esquema de base de datos** | Tablas físicas, tipos SQL, índices | Filas de 24; tipo SQL a la derecha; la clave ajena va de fila a fila; `+ N columnas más` si se corta | 5 tablas, 8 columnas, 6 claves | Tablas apiladas |
| **Dependencias** | Qué depende de qué, con ciclos | Filas por profundidad; insignia «N entran» en cada nodo; un solo ciclo, en el foco, rodeando por fuera | 9 nodos, 14 aristas, 1 ciclo | Las filas ya son verticales |
| **Despliegue** | Dónde corre el software | Zona, nodo y artefacto con versión; réplicas como insignia `x3`; protocolo y puerto en cada camino | 3 zonas, 6 nodos, 8 caminos | Zonas apiladas |
| **Cuadrante** | Dos ejes para priorizar | Cruz fina; una palabra en cada extremo; puntos `r=4` con etiqueta; foco en «primero» | 12 elementos | Cuadrado de 400 |
| **Kanban** | Trabajo por estado, con límites | Columnas con límite `n/límite` en etiqueta rectangular; tarjetas de 56; sin flechas | 5 columnas, 4 tarjetas por columna | Columnas apiladas como bandas |

## Los demás

| Tipo | Para | Lo esencial | Límite |
|---|---|---|---|
| Delta de arquitectura | Cambio de topología: antes, cambios, después | Mismas coordenadas en los dos; registro de cambios con verbo y objeto | 8 piezas, 10 relaciones, 8 cambios |
| Estado actual de TI | El «antes» de una modernización | Zonas por fase o departamento; ≤ 3 colores de pieza | 9 nodos |
| Alto nivel | Pila de datos completa sobre un orquestador | Franja de fases, frontera de despliegue, capas transversales | 9 nodos |
| Medallón | Niveles de calidad de los mismos datos | Bandas por nivel, flechas de promoción con verbo corto | 6 niveles |
| Integración de una plataforma de datos | Fuentes → núcleo → consumidores | Radial dentro de la capa de plataforma, protocolo en cada conexión | 9 nodos |
| Matriz de seguridad | Permisos por rol y pieza | Rejilla; ≤ 5 entidades con color | 1 foco |
| Radar | 3–5 criterios para varias entidades | Primer eje arriba, sentido horario; puntos solo en la serie foco | 5 ejes, 5 series |
| Polar | Una serie sobre categorías cíclicas | Escala desde 0, etiquetas horizontales fuera del anillo | 8 categorías, 1 serie |
| Despiece | Partes de un objeto separadas en un eje | 2–5 partes, de abajo arriba, mismo hueco; etiquetas en una columna | 5 partes, 1 foco |
| Plano axonométrico | Una planta vista desde arriba en ángulo | Muros cortados a la altura de la mesa; nada fuera de la placa | 8 salas, 40 cajas |
| Venn | Intersección de conjuntos | Círculos con relleno muy suave, nombre fuera | 3 círculos |
| Pirámide o embudo | Jerarquía o caída por etapas | 4–6 trapecios, anchos honestos con los datos; foco en uno | 6 capas |
| Barras | Comparar cantidades | Eje desde 0; foco en una barra; horizontales si las etiquetas son largas | 8 barras |
| Cascada | De un total a otro por aportaciones | Totales y puentes con signo; 1 subtotal | 8 barras |
| Mapa de árbol | Partes de un todo por tamaño | Áreas proporcionales; etiqueta o marca si no cabe | 8 celdas |
| Mapa de calor | Valor por celda cruzada | Una rampa de un solo tono; texto claro sobre las celdas oscuras | 7 filas, 8 columnas |
| Líneas | Tendencias, pendiente entre dos momentos, crestas, posiciones | Polilíneas sin suavizar; puntos solo en la serie foco | 5 series, 4–12 puntos |
| Gantt | Tareas y fases en el tiempo | Filas de 40; un foco (la entrega o el camino crítico) | 12 tareas |
| Dispersión (burbujas, enjambre, cajas) | Relación o distribución | Un radio; cinco números en las cajas | 30 puntos; 8 series en cajas |
| Sankey | Una cantidad que se reparte | El grosor es el dato | 3 etapas, 8 nodos, 12 flujos |
| Espina de pescado | Causas de un efecto | Espina horizontal, huesos a 60° (la única diagonal permitida); una causa raíz en el foco; el efecto es lo observado, no el remedio | 6 huesos, 3 subcausas |
| Mapa de Wardley | Cadena de valor frente a evolución | Qué construir, qué comprar, qué se mueve | 9 piezas, 12 enlaces, 2 movimientos |
| Recorrido de usuario | Qué hace y siente una persona por etapas | Curva de sentimiento con niveles con nombre; una persona por mapa | 6 etapas, 3 filas, 2 marcas de dolor |
| Plano de servicio | Lo que ve el cliente y lo que no | Línea de visibilidad; 1 celda foco | 6 etapas |
| Clases UML | Clases, operaciones, herencia y composición | Vocabulario de puntas de UML; `…` si se corta | 7 clases, 8 relaciones, 5 miembros |
| Mapa de historias | Relato por actividades y el corte de la primera entrega | El corte es el foco | 5 actividades, 3 cortes, 12 tarjetas |

Los gráficos de datos (barras, líneas, dispersión, mapas de calor, radar, polar, cascada, Sankey) se pueden hacer también con la skill `dataviz` si está en la sesión; aquí manda la forma vertical y la letra mínima.
