# En una prueba piloto de una skill gráfica, cada gráfico se crea en un subagente limpio

Regla: en una prueba piloto de una skill gráfica, cada gráfico (cada esquema y cada variante: con o sin glosario, hoy o propuesta) se crea en su propio subagente nuevo, sin el contexto de la conversación ni el de otros gráficos, con un encargo fijo que solo lleva la skill, la semántica y la entrada que se prueba; la lectura en frío, también en subagentes limpios, uno por versión. Así la prueba es reproducible y no se falsea con lo que sabe quien dibuja.

Porqué: la primera vez que se probó la cabecera semántica, el esquema de la tarea 474 salió bien porque lo rehízo el agente principal partiendo del esquema anterior, con todo el contexto de la conversación y mirando el dibujo; desde cero, en el piloto, la estructura se perdió. Para medir la skill y no a quien dibuja, cada gráfico parte de cero (tarea 401).

Aplicada en: pendiente, en la prueba piloto de la tarea 401.
