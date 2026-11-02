# Atención, interrupciones, cambio de contexto y estrés en el desarrollo con agentes de IA

Notas de investigación, 2026-10-26. Las cifras marcadas como **[primaria]** se comprobaron leyendo el texto del artículo o la página original. Las marcadas como **[secundaria]** proceden de resúmenes o de prensa. Esas fuentes no se pudieron contrastar con el original y hay que tratarlas con cautela.

## 1. Investigación clásica: ¿cuánto cuesta una interrupción o un cambio de tarea?

### Takeaway
La evidencia sólida dice cuatro cosas. El trabajo del conocimiento está muy fragmentado: unos 11 minutos por "esfera de trabajo" y el 57 % de ellas interrumpidas. Lo interrumpido se retoma, de media, unos 25 minutos después y tras unas 2,3 actividades intermedias. La gente compensa las interrupciones trabajando más rápido, pero con más estrés, frustración, presión temporal y esfuerzo, y eso aparece ya a los 20 minutos. En programación, solo el 10 % de las sesiones empieza a editar código en menos de un minuto. La cifra popular de "23 minutos para recuperar la concentración" no figura en los artículos revisados: es una reformulación divulgativa de un dato distinto.

### Cited Findings

**Mark, González y Harris (2005), "No Task Left Behind? Examining the Nature of Fragmented Work", CHI 2005 [primaria]**
- Diseño: observación de campo detallada (shadowing con registro al segundo) de **24 trabajadores de la información** de una empresa de servicios TI. Se observó a cada uno unos 3 días, de media 25 h 42 min por persona — [PDF](https://www.interruptions.net/literature/Mark-CHI05-p321-mark.pdf)
- Cada informante trabajaba en una media de **11,7 esferas de trabajo** (sd 2,4) distintas — [PDF](https://www.interruptions.net/literature/Mark-CHI05-p321-mark.pdf)
- Tiempo medio en una esfera antes de cambiar o ser interrumpido: **11 min 4 s** (sd 18 min 9 s) — [PDF](https://www.interruptions.net/literature/Mark-CHI05-p321-mark.pdf)
- Se interrumpió el **57,1 %** de los segmentos de trabajo. La ironía que señalan los autores: cuanto más tiempo se lleva en una esfera, más probable es la interrupción y más larga resulta — [PDF](https://www.interruptions.net/literature/Mark-CHI05-p321-mark.pdf)
- El **77,2 %** del trabajo interrumpido se retomó el mismo día. Las esferas centrales se retomaron mucho más (82,0 %) que las periféricas (43,8 %) — [PDF](https://www.interruptions.net/literature/Mark-CHI05-p321-mark.pdf)
- Cuando se retomaba el mismo día, el trabajo se reanudaba tras una media de **25 min 26 s (sd 54 min 48 s)**, y antes se habían atendido de media **2,26 esferas de trabajo intermedias** (sd 2,79). Los informantes lo describieron como "muy perjudicial" — [PDF](https://www.interruptions.net/literature/Mark-CHI05-p321-mark.pdf)
- **Corrección de la cita popular.** El artículo mide cuánto tarda alguien en *volver* a la tarea interrumpida, durante el cual se hace otro trabajo. No mide cuánto tarda en *recuperar la concentración* tras volver. La cifra "23 min 15 s" circula atribuida a Mark a través de entrevistas en prensa. Un post de UC Irvine Informatics de 2017 la atribuye a Fast Company. Otra pieza de UCI de 2011 dice que el 82 % se retoma el mismo día "pero no hasta más de 23 minutos después". Ninguna de esas cifras de 23 minutos aparece en el CHI 2005 ni en el CHI 2008 revisados — [UCI Informatics, ene. 2017](https://www.informatics.uci.edu/2017/01); [Calit2/UCI 2011](https://www.calit2.uci.edu/2011/08/08/post-workingfastermanagingmore/)

**Mark, Gudith y Klocke (2008), "The Cost of Interrupted Work: More Speed and Stress", CHI 2008, pp. 107-110 [primaria]**
- Diseño: experimento de laboratorio 3×2. Factor intra-sujeto: sin interrupción, interrupción del mismo contexto o de contexto distinto. Factor entre sujetos: teléfono o mensajería instantánea. Participaron **48 sujetos** (81 % estudiantes alemanes, edad media 26). La tarea consistía en contestar 12 emails por bloque como responsable de RR. HH., con una interrupción **cada 2 minutos** — [PDF](https://www.interruptions.net/literature/Mark-CHI08.pdf)
- Con interrupciones, la tarea se completó **más rápido**: 22,77 min sin interrupción frente a 20,31 min (mismo contexto) y 20,60 min (contexto distinto). No hubo diferencias en errores ni en cortesía, pero los emails fueron más cortos (31,5 frente a 29,2 palabras) — [PDF](https://www.interruptions.net/literature/Mark-CHI08.pdf)
- NASA-TLX modificado (escala 1-20). El **estrés** pasó de 6,92 sin interrupción a 9,46 y 9,13 con ella (p<.001), y la **frustración** de 4,73 a 6,63 y 6,48. También subieron la presión temporal (11,02 a 12,69 y 12,17), el esfuerzo (9,50 a 11,04 y 11,52) y la carga mental, máxima con interrupciones de contexto distinto (11,50) — [PDF](https://www.interruptions.net/literature/Mark-CHI08.pdf)
- El contexto de la interrupción no cambió el coste: "any interruption introduces a change in work pattern and is not related to context per se" — [PDF](https://www.interruptions.net/literature/Mark-CHI08.pdf)
- Cita textual relevante: "After only 20 minutes of interrupted performance people reported significantly higher stress, frustration, workload, effort, and pressure." Los propios autores advierten que no saben si con el tiempo la gente se adapta o si esos niveles siguen aumentando — [PDF](https://www.interruptions.net/literature/Mark-CHI08.pdf)
- Diferencias individuales: la apertura a la experiencia y la necesidad de estructura personal predicen un menor coste de disrupción (R²=.14) — [PDF](https://www.interruptions.net/literature/Mark-CHI08.pdf)

**Mark: duración de la atención en pantalla [secundaria, palabras de la autora]**
- Desde aproximadamente 2016, la media es de **47 s** en una pantalla antes de cambiar, con una mediana de unos **40 s**. En 2004 la media era de unos 2,5 minutos. Mide comportamiento de cambio registrado con logging, no un "límite biológico" — [Steelcase, transcripción de la entrevista con Gloria Mark](https://www.steelcase.com/research/articles/our-47-second-attention-span-with-gloria-mark-s5-ep3-transcript/); [análisis crítico en Silicon Canals](https://siliconcanals.com/t-screen-attention-47-seconds-gloria-mark/)

**Parnin y Rugaber (2010), "Resumption Strategies for Interrupted Programming Tasks", ICPC / Software Quality Journal 2011 [primaria]**
- Diseño: análisis exploratorio de **10.000 sesiones de programación registradas de 85 programadores** con datos de interacción del IDE (Eclipse/Visual Studio, abril-diciembre de 2008). La versión de revista dice 86 programadores y añade una encuesta a 414 — [PDF](https://sites.cc.gatech.edu/reverse/repository/resumptionstrategies.pdf); [Microsoft Research](https://www.microsoft.com/en-us/research/publication/evaluating-cues-for-resuming-interrupted-programming-tasks/)
- Resultados: solo el **10 %** de las sesiones empieza a editar en menos de un minuto ("edit lag"). Solo el **7 %** no navega a otros sitios antes de editar. En un **30 %** de las sesiones la primera edición llega después de más de 30 minutos — [PDF](https://sites.cc.gatech.edu/reverse/repository/resumptionstrategies.pdf)
- Matiz metodológico: una "sesión" empieza tras una pausa de actividad de 15 minutos o más. El "edit lag" puede incluir depuración y lectura legítimas, así que no es tiempo perdido puro. La cifra divulgativa de "10-15 minutos para empezar a editar" simplifica esto — [PDF](https://sites.cc.gatech.edu/reverse/repository/resumptionstrategies.pdf); [InfoQ 2013](https://www.infoq.com/news/2013/01/Interruptions/)
- El mismo artículo resume trabajos previos. Van Solingen observó en empresas de software alrededor de **1 h al día gestionando interrupciones** y unos **15 min** para recuperarse de cada una. En una encuesta de Microsoft, el **62 %** de los desarrolladores consideraba un problema serio recuperarse de las interrupciones — [PDF](https://sites.cc.gatech.edu/reverse/repository/resumptionstrategies.pdf)

**Meyer, Barr, Bird y Zimmermann (2019/2021), "Today was a Good Day: The Daily Life of Software Developers", IEEE TSE 47(5) [primaria, resumen]**
- **5.971 respuestas** de desarrolladores profesionales de Microsoft. Se confirma que los desarrolladores dedican poco tiempo a desarrollar y que les desagradan las reuniones y las interrupciones. Las interrupciones solo son improductivas en fases de desarrollo; en planificación, especificación y release son "comunes y constructivas" — [Microsoft Research](https://www.microsoft.com/en-us/research/?p=578803)
- Hallazgo clave: la **agencia**, es decir, el control sobre la propia jornada y si el plan se cumple o lo rompen factores externos — [Microsoft Research](https://www.microsoft.com/en-us/research/?p=578803)

**Leroy (2009), "Why is it so hard to do my work? The challenge of attention residue when switching between work tasks", OBHDP 109(2):168-181, julio de 2009 [solo metadatos verificados]**
- Metadatos comprobados en Crossref — [Crossref](https://api.crossref.org/works/10.1016/j.obhdp.2009.04.002); [DOI](https://doi.org/10.1016/j.obhdp.2009.04.002)
- Según un resumen de la BPS, terminar la primera tarea bajo presión temporal reducía el "residuo atencional", lo que se atribuye a una sensación de cierre cognitivo — [BPS Research Digest](https://bps.org.uk/research-digest/surprising-benefits-time-pressure-work)

**Monsell (2003), "Task switching", Trends in Cognitive Sciences [metadatos verificados]**
- Revisión de referencia sobre el coste de cambiar entre tareas en laboratorio — [DOI](https://doi.org/10.1016/s1364-6613(03)00028-7)

**Microsoft Work Trend Index, "Breaking down the infinite workday", 17-06-2025 [primaria]**
- Telemetría agregada de Microsoft 365 hasta el 15-02-2025, más una encuesta a 31.000 trabajadores en 31 mercados (6-02 a 24-03-2025) — [Microsoft WorkLab](https://www.microsoft.com/en-us/worklab/work-trend-index/breaking-down-infinite-workday)
- Los empleados reciben una interrupción por reunión, email o chat **cada 2 minutos** de horario central, lo que equivale a **275 al día**. Las dos cifras usan bases temporales distintas — [Microsoft WorkLab](https://www.microsoft.com/en-us/worklab/work-trend-index/breaking-down-infinite-workday)
- Otras cifras: 153 mensajes de Teams y 117 emails al día, 58 mensajes fuera de horario (+15 % interanual), un 57 % de reuniones ad hoc y un 29 % que vuelve al correo hacia las 22 h — [Microsoft WorkLab](https://www.microsoft.com/en-us/worklab/work-trend-index/breaking-down-infinite-workday)

### Inferences
- El patrón descrito por el propietario, con cambios radicales de tarea cada ~10 minutos, se parece al ritmo base que Mark ya midió en 2005: unos 11 minutos por esfera. La diferencia es que aquí el disparador es el agente y cada cambio es radical, de un proyecto a otro, no dentro de un mismo proyecto.
- El experimento de 2008 encaja muy bien con la sensación de "día acelerado": cuando se espera una interrupción cada 2 minutos, se trabaja más rápido y peor dosificado (emails más cortos), con más estrés y frustración, y el efecto aparece en 20 minutos. Más velocidad no significa menos coste.
- El coste en programación es especialmente alto. Retomar exige reconstruir el estado mental: planes, intenciones y modelo del código. Solo el 7 % de las reanudaciones va directo a editar.
- La agencia (Meyer et al.) apunta a una palanca de diseño: el coste disminuye si es el desarrollador quien decide cuándo atender, no el agente.

### Gaps
- No se recuperó el resumen original de Leroy 2009: número de experimentos, N y efectos. La afirmación de que el residuo atencional empeora el rendimiento en la tarea siguiente se basa en conocimiento general y en resúmenes, no en lectura directa.
- No se verificó la fuente original del "23 min 15 s". Parece proceder de entrevistas (Fast Company / Gallup Business Journal, hacia 2006-2008), no de un artículo revisado por pares.
- No se verificó González y Mark 2004 ("Constant, constant, multi-tasking craziness", CHI 2004) ni Mark, Iqbal, Czerwinski y Johns (2016) sobre emails y estrés con biosensores.
- No se revisó la literatura de *flow* en desarrolladores, como Müller y Fritz (2015) sobre biometría y progreso.

## 2. Supervisar automatización: vigilancia e ironías de la automatización

### Takeaway
Bainbridge (1983) ya formuló la paradoja que vive quien supervisa agentes. A una persona se le pide vigilar un sistema que hace la tarea mejor y más rápido que ella. Nadie mantiene atención efectiva sobre algo en lo que pasa poco durante más de unos 30 minutos. Y la habilidad de tomar el control se deteriora precisamente por no ejercerla.

### Cited Findings
- Bainbridge, L. (1983), "Ironies of Automation", *Automatica* 19(6):775-779 [primaria]. Cita textual: "it is impossible for even a highly motivated human being to maintain effective visual attention towards a source of information on which very little happens, for more than about half an hour". Se apoya en los estudios de vigilancia de Mackworth (1950). La autora concluye que la monitorización de anomalías improbables debe delegarse en alarmas automáticas — [PDF (gwern)](https://gwern.net/doc/sociology/technology/1983-bainbridge.pdf)
- La misma autora sostiene que el operador "will not monitor the automatics effectively if they have been operating acceptably for a long period". También advierte de que obligarle a llevar un registro no garantiza atención: "people can write down numbers without noticing what they are" — [PDF](https://gwern.net/doc/sociology/technology/1983-bainbridge.pdf)
- Si el ordenador decide más rápido y con más criterios, el humano solo puede supervisar "at some meta-level": "The human monitor has been given an impossible task." — [PDF](https://gwern.net/doc/sociology/technology/1983-bainbridge.pdf)
- Las habilidades manuales y cognitivas se deterioran si no se usan, así que quien solo supervisa puede ser menos capaz de intervenir cuando hace falta — [PDF](https://gwern.net/doc/sociology/technology/1983-bainbridge.pdf)
- Equivalente actual en Claude Code: Anthropic afirma que "in practice users accept 93% of [permission prompts] anyway", y que eso "leads to approval fatigue, where people stop paying close attention to what they're approving". El post no explica cómo se midió el 93 %. Un medio secundario cita un 97 % sin fuente verificable — [Anthropic Engineering, 25-03-2026](https://anthropic.com/engineering/claude-code-auto-mode); [devops.com](https://devops.com/anthropic-makes-claude-codes-auto-mode-the-default-betting-automation-beats-manual-review/)

### Inferences
- Las aprobaciones manuales frecuentes reproducen la ironía del registro de Bainbridge: se aprueba sin leer. El diseño razonable es concentrar la atención humana en pocos puntos de alto valor, como el plan, la revisión final y las alarmas por anomalía, y automatizar lo rutinario.
- "Vigilar el terminal mientras el agente trabaja" es una tarea de vigilancia en el sentido de Mackworth: poca señal durante mucho tiempo. La literatura predice que falla sola, por lo que conviene sustituirla por notificaciones solo cuando haya un evento relevante.

### Gaps
- No se revisó la literatura moderna de "human-out-of-the-loop", conciencia situacional y complacencia (Endsley y Kiris 1995; Parasuraman y Manzey 2010).

## 3. Investigación específica (2025-2026) sobre desarrolladores que supervisan agentes de IA

### Takeaway
Sí existe investigación específica y muy reciente, casi toda preprints de arXiv de 2026 y con muestras pequeñas. Coinciden en tres puntos. Esperar al agente es el motivo principal para lanzar sesiones en paralelo. Coordinar y monitorizar varias sesiones tiene un coste real que mencionan todos los participantes. Las peticiones de aclaración y los errores de los agentes son las señales que más se pierden. Con herramientas de apoyo, el rendimiento sube y el esfuerzo de seguimiento baja, pero no aumentan ni el control percibido ni el éxito al redirigir a los agentes.

### Cited Findings

**Long, Shi, Mozannar, Murad y Hosn (Microsoft Research AI Frontiers / Columbia), "ParallelPilot: Supporting Coordination and Monitoring in Parallel AI Coding", arXiv:2609.33113, 27-09-2026 [primaria, preprint]**
- Estudio formativo con **14 desarrolladores** que usan habitualmente sesiones de IA en paralelo, mediante entrevistas de 60 minutos. Declaran que la IA paralela supone el **45,3 %** de su tiempo de programación, frente al 48,6 % de una sola sesión y el 6,1 % sin IA — [arXiv](https://arxiv.org/html/2609.33113v1)
- El **tiempo muerto esperando a un único agente** fue el desencadenante principal del paralelismo. Los **14 de 14** describieron una sobrecarga real de coordinación y monitorización — [arXiv](https://arxiv.org/html/2609.33113v1)
- Señales que exigen intervención: finalización, peticiones de aclaración, errores y retrasos inesperados. Las que **más se pierden** son las aclaraciones y los errores — [arXiv](https://arxiv.org/html/2609.33113v1)
- Estudio de usuario intra-sujetos con **16 desarrolladores**, bloques de 20 minutos y 6 tickets, comparando con GitHub Copilot CLI o Chat. Con la herramienta, los tickets por minuto pasaron de 0,272 a 0,445 (**+63 %**). El pico de agentes concurrentes subió de 2,31 a 3,25. El esfuerzo de seguimiento bajó de 4,63 a 2,75 (escala 1-7), la disrupción por cambio de 4,50 a 2,69 y el cambio de contexto de 3,81 a 2,25 — [arXiv](https://arxiv.org/html/2609.33113v1)
- **No mejoraron significativamente** el control percibido (3,94 frente a 4,31; q=.416), el éxito al intervenir ni la confianza al delegar. No se usó NASA-TLX — [arXiv](https://arxiv.org/html/2609.33113v1)
- Trabajos citados por el artículo, no verificados por separado. Vasilescu et al. (2016) identifican el cambio de contexto como "el coste clave de la paralelización". Ye et al. (2026) encuentran que el 94 % de más de 100 desarrolladores no detectó sabotaje insertado por un agente. Catalan et al. (2026) observan que los desarrolladores hojean o ignoran trazas de ejecución largas. Kitano et al. (2026) describen "overwhelming information" con 3 agentes concurrentes durante 6 semanas — [arXiv](https://arxiv.org/html/2609.33113v1)

**Park, Arvi, Lee, Lim, Ma y Kim, "The Work Behind Delegation: A Framework for Supervising AI Coding Agents", arXiv:2609.24234, 21-09-2026 [primaria, preprint]**
- Observación con think-aloud de **19 desarrolladores experimentados** en sus propias tareas de unos 40 minutos. Se completa con un análisis temático de **102 hilos y 12.912 comentarios** de r/ClaudeCode, r/codex y r/ExperiencedDevs (17-05 a 17-08-2026) — [arXiv](https://arxiv.org/html/2609.24234v1)
- Adapta el control supervisor de Sheridan a siete etapas: **Plan, Monitor, Wait, Review, Teach, Manual Fix y Update Assets**. *Wait* se distingue de *Monitor*: unos aprovechan la espera para supervisar otros agentes y otros hacen algo ajeno ("just watch YouTube") — [arXiv](https://arxiv.org/html/2609.24234v1)
- Monitor y Wait se alternan: se lee la salida a ráfagas, se hace otra cosa y se detiene al agente solo si algo "seems really off". Algunos delegan la supervisión en otros agentes (un "Advisor" que revisa a un "Implementer") o montan relés que congelan y avisan cuando "anything weird happens" — [arXiv](https://arxiv.org/html/2609.24234v1)
- Para algunos, corregir con prompts repetidos resulta más pesado que programar: "mentally much less taxing to just code it up manually". El artículo no da medidas cuantitativas de carga ni de fatiga — [arXiv](https://arxiv.org/html/2609.24234v1)

**Wang et al. (CMU, Stanford, Princeton, UIUC), "Position: Humans are Missing from AI Coding Agent Research", arXiv:2608.12355, 4-07-2026 [primaria, artículo de posición]**
- Sostiene que el cuello de botella ya no es la autonomía, sino cómo los humanos se comunican con los agentes, los supervisan y confían en ellos. Propone líneas de "efficient oversight" y métricas de interacción — [arXiv](https://arxiv.org/html/2608.12355v1)
- Cita "prompt fatigue" (Lessard 2025): hay que restablecer contexto en cada sesión — [arXiv](https://arxiv.org/html/2608.12355v1)

**METR: ensayos aleatorizados de productividad**
- Julio de 2025, ECA con **16 desarrolladores** experimentados de código abierto y **246 issues**. Con IA tardaron un **19 % más**, aunque esperaban ir un 24 % más rápido y después creían haber ido un 20 % más rápido — [METR, 10-07-2025](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- Actualización del 24-02-2026: **57 desarrolladores** y más de 800 tareas. Los desarrolladores originales obtienen −18 % de tiempo (IC −38 % a +9 %) y los nuevos −4 % (IC −15 % a +9 %). METR lo califica de evidencia débil por sesgos de selección — [METR, 24-02-2026](https://metr.org/blog/2026-02-24-uplift-update/)
- Relevante aquí: las mediciones de tiempo son "unreliable for the fraction of developers who use multiple AI agents concurrently", porque los desarrolladores hacían otra tarea mientras el agente trabajaba — [METR, 24-02-2026](https://metr.org/blog/2026-02-24-uplift-update/)

### Inferences
- La secuencia "el agente me hace esperar, abro otro proyecto, el agente me reclama" está documentada como el mecanismo típico (ParallelPilot). Lo que describe el propietario es el caso normal del paralelismo con agentes, solo que llevado a varios proyectos de riesgo a la vez.
- El paralelismo parece aumentar el rendimiento en tareas cortas cuando hay apoyo de coordinación, pero las propias medidas indican un coste de seguimiento y de cambio de contexto. Sin herramientas, ese coste es alto: unos 4,5 sobre 7.
- Que no mejoren el control percibido ni el éxito al redirigir sugiere un límite que la interfaz no resuelve: el humano sigue sin poder supervisar a fondo. Es la ironía de Bainbridge.
- Señales de diseño respaldadas por la evidencia: notificaciones solo para aclaraciones, errores, finalización y bloqueos; un estado visible de cada agente; registro y planificación previa; aislamiento entre tareas.

### Gaps
- No se encontraron estudios con medidas fisiológicas o estandarizadas (NASA-TLX, VFC) de carga en desarrolladores que supervisan varios agentes.
- No se encontraron estudios longitudinales de semanas o meses sobre estrés o burnout en flujos multiagente.
- Los estudios de 2026 son preprints sin revisión por pares, con N entre 14 y 19, y algunos los firma la empresa que fabrica la herramienta (Microsoft / Copilot).

## 4. Estrés, fatiga y burnout asociados al desarrollo y el trabajo asistidos por IA (encuestas 2025-2026)

### Takeaway
El dato más directo es el estudio de BCG publicado en HBR en marzo de 2026 sobre "AI brain fry". En él, una alta exigencia de supervisión de IA se asocia a más esfuerzo mental, fatiga y sobrecarga informativa, y la productividad percibida cae a partir de 3-4 herramientas simultáneas. Las encuestas sobre desarrolladores (DORA 2025, Atlassian 2025) no muestran que la IA reduzca el burnout ni la fricción: las ganancias de tiempo se compensan con ineficiencias organizativas.

### Cited Findings
- **BCG / HBR, "When Using AI Leads to 'Brain Fry'"**, de Bedard, Kropp, Hsu, Karaman, Hawes y Kellerman, publicado el 05-03-2026. El texto abierto arranca con Gas Town, una plataforma para ejecutar muchos agentes de Claude Code a la vez, y con un usuario que dice "I had a palpable sense of stress watching it" — [HBR](https://hbr.org/2026/03/when-using-ai-leads-to-brain-fry) (cuerpo de pago)
- Cifras del estudio [secundaria, The Decoder 09-03-2026 y Axios 06-03-2026]. Encuesta autodeclarada a **1.488 trabajadores a tiempo completo de EE. UU.**; un **14 %** de los usuarios de IA declara "brain fry" (26 % en marketing, 6 % en legal). Una alta exigencia de supervisión se asocia a **+14 % de esfuerzo mental, +12 % de fatiga mental y +19 % de sobrecarga informativa**. La productividad percibida sube de 1 a 2 herramientas, alcanza su máximo con **3** y cae a partir de **4**. También aparecen +33 % de fatiga de decisión, +39 % de errores graves y una intención de dejar el empleo que pasa del 25 % al 34 %. Usar IA para sustituir tareas repetitivas se asocia a un burnout un 15 % menor — [The Decoder](https://the-decoder.com/study-warns-of-ai-brain-fry-as-workers-hit-cognitive-limits-overseeing-ai-agents/); [Axios](https://www.axios.com/2026/03/06/ai-chatgpt-claude-jobs-brain-fry)
  - Cautelas: BCG asesora en transformación con IA, los datos son transversales y autodeclarados, y la muestra no se limita a desarrolladores.
- **DORA 2025 (Google Cloud)**, con unas 5.000 respuestas [secundaria]. A igualdad de rasgos y entorno, una mayor adopción de IA se asocia a más eficacia individual, pero a **niveles similares de burnout y fricción**, y a más inestabilidad en las entregas. La idea central: la IA amplifica lo que ya existe — [RedMonk, 18-12-2025](https://redmonk.com/rstephens/2025/12/18/dora2025/); [Google Cloud](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report)
- **Atlassian State of DevEx 2025**, con 3.500 desarrolladores y managers de 6 países [secundaria / página del fabricante]. El 99 % declara ahorrar tiempo con IA y el 68 % más de 10 h a la semana. Pero el 50 % pierde más de 10 h semanales y el 90 % más de 6 h por ineficiencias organizativas: información difícil de encontrar, flujos fragmentados y colaboración — [Atlassian](https://www.atlassian.com/teams/software-development/state-of-developer-experience-2025); [LeadDev](https://leaddev.com/velocity/ai-productivity-gains-are-being-offset-by-organizational-bottlenecks)

### Inferences
- El máximo de productividad percibida en unas 3 herramientas o agentes simultáneos, si se confirma, es un dato útil para fijar un límite de WIP de agentes concurrentes. Es una asociación autodeclarada, no un umbral causal.
- La IA no reduce por sí sola el estrés: DORA y Atlassian coinciden en que el sistema de trabajo determina el resultado. Para la SF, el diseño del flujo de atención importa tanto como la herramienta.

### Gaps
- No se verificó el informe de Harness (State of AI in Software Engineering) ni otras encuestas específicas de 2026 sobre burnout de desarrolladores con agentes.
- No se accedió al texto completo de HBR para comprobar las cifras de BCG. Proceden de prensa que coincide entre sí.
- No se encontró ningún estudio académico revisado por pares que mida "AI fatigue" en desarrolladores con instrumentos validados.
- No hay estudios sobre un único desarrollador que lleve muchos proyectos distintos en paralelo con agentes. Todo lo encontrado trata varios agentes sobre uno o dos proyectos.
