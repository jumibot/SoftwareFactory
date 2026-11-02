# Productividad, confianza, carga de revisión y delegación con asistentes y agentes de IA (evidencia 2024-2026)

Notas de investigación del 2026-10-26. Las cifras marcadas como «verificado» se comprobaron en la fuente primaria con WebFetch. Las marcadas como «secundario» solo aparecen en resúmenes de terceros y deben confirmarse antes de citarlas en el documento de visión.

## 1. METR: ensayo controlado aleatorizado de 2025 y seguimiento de 2026

### Takeaway
En el ensayo de principios de 2025, desarrolladores expertos de código abierto tardaron un 19 % más con IA, aunque creían haber ido un 20 % más rápido. El seguimiento de febrero de 2026, con herramientas de finales de 2025, no permite medir bien el efecto real: muchos desarrolladores se negaron a trabajar sin IA, y los que ejecutaban varios agentes a la vez no podían registrar el tiempo con fiabilidad. La brecha entre percepción y realidad es el hallazgo más sólido.

### Cited Findings
- **Estudio original (publicado el 10-07-2025).**
  - Muestra: 16 desarrolladores expertos de código abierto y 246 issues reales de unas 2 horas de media cada una, en repositorios grandes con más de 22.000 estrellas y más de un millón de líneas de media.
  - Diseño: cada issue se asignó al azar a «IA permitida» o «IA no permitida».
  - Herramientas: sobre todo Cursor Pro con Claude 3.5/3.7 Sonnet. Pago de 150 USD/hora.
  - Resultados: las issues con IA tardaron un 19 % más. Antes, los desarrolladores esperaban una aceleración del 24 %; después seguían creyendo que la IA les había acelerado un 20 %.
  - Factores: se examinaron 20 posibles factores y 5 contribuyen probablemente a la ralentización (verificado). — [METR, blog 2025-07-10](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/); [arXiv 2507.09089](https://arxiv.org/abs/2507.09089)
- **Salvedades declaradas por los autores del estudio original.**
  - La muestra es pequeña y puede haber sesgo de selección.
  - La mayoría tenía solo unas decenas de horas de experiencia con Cursor, así que no se descartan efectos de aprendizaje por encima de unas 50 horas.
  - El estudio solo cubre repositorios que los desarrolladores ya conocían.
  - Los desarrolladores apenas pedían varias respuestas al modelo; mejores prompts o andamiaje podrían cambiar el resultado.
  - El estudio no demuestra que la IA no acelere en otros contextos (verificado). — [METR, blog 2025-07-10](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- **Seguimiento (blog del 24-02-2026, estudio iniciado en agosto de 2025).**
  - El post da para el estudio original un 19 % de ralentización con IC 95 % de +2 % a +39 %.
  - Muestra nueva: 57 desarrolladores (10 del estudio original y 47 nuevos), 143 repositorios y más de 800 tareas, con una mediana de 10 años de experiencia en código abierto. Pago reducido a 50 USD/hora.
  - Estimación de «speedup» en notación de METR, donde un valor negativo significa más rápido con IA: −18 % para los desarrolladores originales (IC −38 % a +9 %) y −4 % para los nuevos (IC −15 % a +9 %) (verificado). — [METR, uplift update 2026-02-24](https://metr.org/blog/2026-02-24-uplift-update/)
- **Por qué METR considera poco fiables sus propios datos de 2026 (verificado).** — [METR, uplift update 2026-02-24](https://metr.org/blog/2026-02-24-uplift-update/)
  - Cada vez más desarrolladores dicen que no querrían hacer el 50 % de su trabajo sin IA.
  - Entre el 30 % y el 50 % de los encuestados admitió no presentar algunas tareas porque no quería hacerlas sin IA.
  - Las mediciones de tiempo no son fiables cuando el desarrollador ejecuta varios agentes a la vez y trabaja en otras cosas mientras tanto.
  - Los desarrolladores desplazaron el tipo de tarea hacia lo que la IA hace bien.
  - Hubo diferencias de calidad, documentación y tests entre las dos condiciones.
  - Algunos dejaron sin terminar tareas de la condición sin IA; uno no completó ninguna.
  - Conclusión de los autores: la estimación es «likely a bad proxy for the real productivity impact» y «only very weak evidence» de que la aceleración haya aumentado desde principios de 2025.
- **Rediseño anunciado (verificado).** Experimentos más cortos y con mayor cumplimiento, datos observacionales (commits y transcripciones), estudios de uso del tiempo, tareas fijas y aleatorización por desarrollador. — [METR, uplift update 2026-02-24](https://metr.org/blog/2026-02-24-uplift-update/)
- **Encuesta posterior (secundario, no verificado).** Según fuentes secundarias, METR hizo una encuesta entre febrero y abril de 2026 a 349 trabajadores técnicos, que declararon grandes ganancias; METR advierte que esas respuestas no tienen por qué reflejar la realidad. No encontré la página primaria. — [i-programmer](https://www.i-programmer.info/news/99-professional/18910-perceived-value-of-ai-tools.html)
- **Discrepancia sobre la cobertura de prensa.** Algunos medios presentaron el seguimiento como una «reversión» del hallazgo de 2025. Es una lectura incorrecta: METR no afirma que haya aceleración, sino que no puede medirla de forma fiable. — [particula.tech](https://particula.tech/blog/metr-reversed-19-percent-slower-ai-coding-study)

### Inferences
- El sesgo de percepción es directamente relevante para un desarrollador solo: sentir que la IA acelera no es evidencia de que acelere. Hace falta medir el resultado entregado, no la sensación.
- Que METR no pueda medir el tiempo cuando hay varios agentes en paralelo es una señal en sí misma: con agentes concurrentes, el tiempo humano se fragmenta y deja de corresponder a una tarea concreta. Eso dificulta saber qué frentes avanzan de verdad.

### Gaps
- No verifiqué en fuente primaria la encuesta de METR de 2026 (n=349).
- La página de METR no da las previsiones numéricas de los expertos externos del estudio de 2025.

## 2. DORA 2025: «State of AI-assisted Software Development» (Google Cloud)

### Takeaway
La IA actúa como amplificador: potencia las fortalezas y las debilidades que ya existían. En 2025 la adopción de IA se asocia por primera vez a más throughput, pero sigue asociándose a menos estabilidad, porque más volumen de cambios desborda controles débiles como los tests, el control de versiones y los ciclos de feedback.

### Cited Findings
- **Datos generales del informe (verificado).** — [Google Cloud blog, 2025-09-23](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report)
  - Publicado el 23-09-2025, a partir de casi 5.000 profesionales y más de 100 horas de datos cualitativos.
  - El 90 % usa IA en el trabajo y más del 80 % cree que le ha aumentado la productividad.
  - El 30 % confía poco o nada en el código generado por IA, algo menos que el año anterior.
- **Throughput y estabilidad (verificado).** — [Google Cloud blog, 2025-09-23](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report)
  - A diferencia de 2024, la adopción de IA tiene relación positiva con el throughput de entrega y con el rendimiento del producto.
  - Sigue teniendo relación negativa con la estabilidad de entrega. Los autores lo atribuyen a que el mayor volumen de cambios desborda controles débiles (tests automatizados, prácticas de control de versiones, bucles de feedback).
  - El 90 % de las organizaciones ha adoptado al menos una plataforma interna, lo que se correlaciona con su capacidad de aprovechar la IA.
- **Datos citados en el resumen de Google (secundario respecto al informe completo).** — [Google blog](https://blog.google/technology/developers/dora-report-2025/)
  - La adopción subió 14 puntos respecto a 2024.
  - Uso típico de unas 2 horas al día.
  - El 65 % depende mucho de la IA y el 59 % percibe un efecto positivo en la calidad del código.
- **La IA como amplificador (verificado).** Cita del informe: «AI's primary role is as an amplifier, magnifying an organization's existing strengths and weaknesses.» — [dora.dev 2025 report](https://dora.dev/research/2025/dora-report/)
- **Perfiles de equipo y burnout (verificado, sin cifras).** El informe define siete perfiles de equipo. El blog solo nombra dos:
  - «Foundational challenges»: bajo rendimiento, alto burnout y alta fricción.
  - «Harmonious high achievers»: fuertes en bienestar, resultados de producto y entrega.
  - No se dan porcentajes de burnout. — [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report)
- **Modelo de capacidades de IA de DORA (verificado parcialmente).** Son siete capacidades que «amplifican los beneficios de la IA»; la página se actualizó el 25-11-2025. La página de Google Cloud menciona como ejemplos «healthy data ecosystems», «clear and communicated AI stance» y «strong user-centric focus», además de que el 76 % de las organizaciones tiene equipos de plataforma dedicados. — [dora.dev capabilities model](https://dora.dev/ai/capabilities-model/); [Google Cloud, informe del modelo](https://cloud.google.com/resources/content/2025-dora-ai-capabilities-model-report)
- **Cautela metodológica.** El informe se basa en una muestra autoseleccionada y en datos declarados; las relaciones que describe son correlaciones. — [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report)

### Inferences
- Para una fábrica de un solo desarrollador, el mensaje de DORA se traduce en esto: sin tests automáticos, lotes pequeños y feedback rápido, delegar más en IA aumenta el volumen de cambios y la inestabilidad, no el valor entregado.

### Gaps
- No pude extraer en fuente primaria la lista completa de las siete capacidades: el texto está en una imagen o en el PDF con registro. Según conocimiento previo no verificado aquí, incluyen trabajo en lotes pequeños, control de versiones fuerte, datos internos accesibles para la IA y plataforma interna de calidad. Hay que confirmarlo en el PDF.
- Tampoco obtuve los nombres de los siete perfiles de equipo ni porcentajes de burnout.

## 3. Stack Overflow Developer Survey 2025 y 2026

### Takeaway
En 2025 el uso de IA crece (84 %) mientras la confianza en su precisión baja: el 46 % desconfía y solo el 3 % confía mucho. La frustración principal son las soluciones «casi correctas» (66 %), y el 45 % dice que depurar código de IA lleva más tiempo. La encuesta de 2026 (publicada el 06-10-2026) muestra una confianza condicionada a poder verificar y a conocer la fuente, y una adopción masiva de agentes de código.

### Cited Findings
- **2025: adopción (verificado).** — [SO Survey 2025, sección IA](https://survey.stackoverflow.co/2025/ai)
  - El 84 % usa IA o piensa usarla (76 % en 2024): 47,1 % a diario y 50,6 % a diario entre profesionales.
  - Aproximadamente 33.662 respondieron a esta pregunta; el total de la encuesta ronda las 49.000 respuestas (cifra derivada, no declarada en la página).
- **2025: opinión y confianza (verificado).** — [SO Survey 2025, sección IA](https://survey.stackoverflow.co/2025/ai)
  - Opinión favorable del 59,7 %.
  - Confianza en la precisión de la IA:

    | Respuesta | Todos | Desarrolladores experimentados |
    |---|---|---|
    | Confía mucho | 3,1 % | 2,5 % |
    | Confía algo | 29,6 % | — |
    | Desconfía algo | 26,1 % | — |
    | Desconfía mucho | 19,6 % | 20,7 % |

- **2025: frustraciones (verificado).** El 66 % menciona «AI solutions that are almost right, but not quite» y el 45,2 % dice que depurar código generado por IA lleva más tiempo. — [SO Survey 2025, sección IA](https://survey.stackoverflow.co/2025/ai)
- **2025: agentes (verificado).** — [SO Survey 2025, sección IA](https://survey.stackoverflow.co/2025/ai)
  - Alrededor del 31 % usa agentes en el trabajo: 14,1 % a diario, 9 % semanalmente y 7,8 % mensualmente o menos. El 17,4 % piensa usarlos y el 37,9 % no tiene planes (n=31.877).
  - Entre quienes usan agentes, alrededor del 69 % dice que aumentaron su productividad y el 70 % que redujeron el tiempo en tareas concretas.
  - El 52 % de todos los encuestados percibe un efecto positivo en su productividad.
  - Alrededor del 77 % no hace «vibe coding» en el trabajo.
- **2026: datos verificados en el blog oficial (06-10-2026).** — [Stack Overflow blog, 2026-10-06](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/)
  - Más de 30.000 respuestas recogidas durante siete semanas.
  - El 73 % de quienes usan asistentes o agentes de código los usa a diario, y un tercio de los usuarios diarios de cualquier herramienta de IA la usa 4 horas o más al día.
  - El 66 % de los usuarios de IA trabaja con agentes de código y el 63 % con chatbots. Claude Code (66 %) y GitHub Copilot (59 %) son los agentes más usados.
  - El 62 % ve la IA al menos algo positivamente; entre los usuarios diarios, el 71 %.
  - El 93 % dice que la atribución de fuentes es necesaria para confiar en la salida.
  - El 38 % de las organizaciones pone límites de uso.
- **2026: datos de prensa (secundario).** — [IT Brief](https://itbrief.co.uk/story/stack-overflow-survey-shows-developers-trust-ai-with-caveats); [InfoWorld](https://www.infoworld.com/article/4233357/ai-distrust-is-githubs-opportunity.html)
  - Alrededor del 48 % confiaría si pudiera verificar fácilmente, y solo el 6,6–7 % confiaría para decisiones importantes.
  - El 76,5 % ejecuta las respuestas en local y el 63,9 % las compara con su base de código; solo el 9,6 % las usa tal cual.
  - El 26,2 % usa flujos de agentes automatizados.
  - InfoWorld señala que la pregunta de confianza cambió en 2026, así que no es comparable con 2025.
- **Discrepancia de cifras.** El blog de Stack Overflow da un 93 % para la atribución de fuentes y la prensa un 78,7 % («importante»). Probablemente miden ítems distintos. — [Stack Overflow blog](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/) vs. [IT Brief](https://itbrief.co.uk/story/stack-overflow-survey-shows-developers-trust-ai-with-caveats)

### Inferences
- Los datos de 2026 sustituyen a los de 2025 en cuanto a adopción de agentes: se pasa de alrededor del 31 % de usuarios de agentes al 66 % de los usuarios de IA. No sustituyen la medición de confianza, porque la pregunta cambió.
- El patrón que se repite es el uso intensivo con verificación: la confianza depende de poder comprobar el resultado de forma barata (ejecución local, tests, fuentes). Para la SF, esto significa que la verificabilidad es la condición para delegar.

### Gaps
- No obtuve de la fuente primaria de 2026 un porcentaje de confianza en la precisión ni el dato de frustración por soluciones «casi correctas».

## 4. Datos de telemetría y repositorios: Faros AI, GitClear, GitHub Octoverse, NBER, Google y Microsoft

### Takeaway
La telemetría coincide en que la IA aumenta mucho la producción de código y de PR, pero esa ganancia se diluye al pasar a entregas, releases y uso real. Al mismo tiempo crecen el tamaño de las PR, el tiempo de revisión, los bugs, los incidentes y la duplicación de código. El cuello de botella se desplaza a revisión, QA e integración.

### Cited Findings
- **Faros AI, «AI Productivity Paradox» (2025, verificado parcialmente).** Telemetría de más de 10.000 desarrolladores en 1.255 equipos: se completan aproximadamente el doble de cambios de código, pero las métricas a nivel de empresa siguen planas. — [Faros research](https://www.faros.ai/research/ai-productivity-paradox)
  - Las cifras muy citadas (+21 % tareas, +98 % PR fusionadas, +91 % tiempo de revisión, +154 % tamaño de PR, sin mejora en las métricas DORA) aparecen en fuentes secundarias; no las encontré en la página web actual de Faros. — [augmentcode](https://www.augmentcode.com/guides/ai-productivity-paradox-engineering-delivery); [getunblocked](https://getunblocked.com/blog/ai-productivity-paradox/)
- **Faros AI, «Acceleration Whiplash» (AI Engineering Report, 2.º trimestre de 2026, verificado).** — [Faros, Acceleration Whiplash](https://www.faros.ai/research/ai-acceleration-whiplash)
  - Muestra: 22.000 desarrolladores en 4.000 equipos, con dos años de telemetría.
  - Throughput:

    | Métrica | Variación |
    |---|---|
    | Épicas completadas | +66,2 % |
    | Tareas | +33,7 % |
    | Tasa de merge de PR | +16,2 % |
    | Despliegues por semana | −11,7 % |

  - Revisión y tamaño: el tiempo mediano de revisión se multiplica por 5 y el tamaño de las PR crece un 51 %.
  - Calidad e incidentes:

    | Métrica | Variación |
    |---|---|
    | Incidentes por PR | +242,7 % |
    | Incidentes mensuales | +57,9 % |
    | Bugs por PR | +28,7 % |
    | Bugs por desarrollador | +54 % |
    | Churn de código | +861 % |

  - El 25 % de las PR las revisa un agente de IA.
  - Discrepancia: un resumen secundario habla de «+441 % de tiempo mediano de revisión», lo que equivale aproximadamente a ×5.
- **Faros AI, «The Speed Trap» (3.er trimestre de 2026, publicado el 18-09-2026, verificado).** Doce meses de telemetría de 22.000 desarrolladores en 4.000 equipos. — [Faros, Speed Trap takeaways](https://www.faros.ai/blog/ai-speed-trap-takeaways)
  - Adopción: tasa de aceptación de código de IA del 65 %, uso semanal de IA del 79 %, revisión por IA en el 50–80 % de las PR en muchas empresas y entre un 13 % y un 14 % de PR escritas por agentes en las empresas más avanzadas.
  - Trabajo rehecho y tamaño: «restarts» +66,7 % y tamaño medio de PR +71,8 %.
  - PR fusionadas sin revisión: +76,3 %, frente a +31,3 % en el informe anterior. Es probable que sea un incremento y no la proporción de PR; hay que confirmarlo en el informe.
  - Calidad: tiempo en QA +300,6 %, incidentes por PR +14,5 % e incidentes mensuales +125,4 %.
  - El tiempo de revisión aparece como «heavily elevated», sin cifra.
  - La página menciona una tendencia de «paralelismo» del informe anterior, pero sin cifra.
  - Nota: son informes de un proveedor y los datos son correlacionales.
- **NBER Working Paper 35275, «Writing Code vs. Shipping Code» (mayo de 2026, revisado en septiembre de 2026, verificado).** — [NBER w35275](https://www.nber.org/papers/w35275)
  - Autores: Demirer, Musolff y Yang. Datos de más de 500.000 desarrolladores de GitHub.
  - Efecto acumulado sobre commits: +30 % con autocompletado, +180 % con agentes interactivos y +240 % con agentes autónomos.
  - El efecto se atenúa a lo largo de la cadena: el +240 % se queda en +80 % en proyectos y en +30 % en releases.
  - Elasticidad de sustitución IA–esfuerzo humano de 0,23, lo que indica fuertes complementariedades (hipótesis del eslabón débil).
  - En cuatro grandes marketplaces suben mucho las apps nuevas, pero el uso total no aumenta.
  - Discrepancia: un blog secundario da «100.000 desarrolladores» y «+180 % commits / +30 % releases»; la cifra primaria es la anterior. — [hyrax.dev](https://hyrax.dev/blog/mit-wharton-code-review-bottleneck-2026)
- **GitClear, «AI Copilot Code Quality 2025» (verificado parcialmente).** — [GitClear](https://www.gitclear.com/ai_assistant_code_quality_2025_research)
  - Analiza 211 millones de líneas cambiadas entre 2020 y 2024 en repositorios de Google, Microsoft, Meta y empresas.
  - El código clonado multiplica su presencia por 4: pasa del 8,3 % (2021) al 12,3 % (2024).
  - Las líneas movidas, que se usan como indicador de refactorización, caen del 25 % a menos del 10 %.
  - En 2024 el copia-pega supera por primera vez al código movido.
  - Discrepancia: la prensa habla de «8× bloques duplicados de 5 o más líneas»; es otra métrica. — [devclass](https://devclass.com/2025/02/20/ai-is-eroding-code-quality-states-new-in-depth-report/)
- **GitHub Octoverse 2025 (28-10-2025, actualizado el 28-02-2026, verificado).** — [GitHub blog, Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
  - Más de 180 millones de desarrolladores, más de 36 millones nuevos en el año (+23 %).
  - PR fusionadas: 43,2 millones al mes de media (+23 %) y 518,7 millones en el año (+29 %).
  - Unos 986 millones de commits (+25 %).
  - Más de un millón de PR creadas por el agente de código de Copilot entre mayo y septiembre de 2025.
  - Casi el 80 % de los desarrolladores nuevos usa Copilot en su primera semana.
- **Google, ensayo controlado aleatorizado interno (2024; ICSE SEIP 2025).** Con 96 ingenieros de Google, el efecto estimado es de alrededor de un 21 % más rápido, con un intervalo de confianza amplio y herramientas internas de verano de 2024. — [arXiv 2410.12944](https://arxiv.org/abs/2410.12944v3)
- **Microsoft, Accenture y una empresa Fortune 100: tres ensayos de campo (Cui, Demirer et al.; Management Science).**
  - Participaron 4.867 desarrolladores entre septiembre de 2022 y abril de 2024.
  - Resultado conjunto: +26 % de tareas completadas (PR), con error estándar de alrededor de ±10 %. Solo fue significativo en Microsoft.
  - La adopción fue incompleta: 44,2 % en Microsoft y 61,7 % en Accenture.
  - Verificado solo a través del apéndice de INFORMS y de resúmenes. — [INFORMS supplement](https://pubsonline.informs.org/doi/suppl/10.1287/mnsc.2025.00535/suppl_file/mnsc.2025.00535.sm1.pdf); [DX newsletter](https://newsletter.getdx.com/p/copilot-impact-on-productivity)
- **PR de agentes en repositorios abiertos (arXiv 2601.00753, secundario).** Sobre 33.707 PR escritas por agentes, el 28,3 % se fusiona de inmediato y muchas otras se abandonan tras comentarios de revisión; el artículo habla de un «attention tax» para los mantenedores. — [arXiv 2601.00753](https://arxiv.org/abs/2601.00753v1)
- **Por qué no se fusionan las PR de corrección de agentes (arXiv 2602.00164, secundario).** No atacan la causa raíz, introducen efectos secundarios o no validan con tests. — [arXiv 2602.00164](https://arxiv.org/html/2602.00164)
- **Revisión humana de PR de agentes: datos contradictorios (secundario).**
  - Un estudio longitudinal (arXiv 2607.07980) indica que la proporción de PR de agentes fusionadas sin revisión humana bajó desde su pico de mediados de 2025 hacia la tasa de las PR humanas a principios de 2026. — [alphaxiv 2607.07980](https://www.alphaxiv.org/abs/2607.07980.md)
  - Un blog cita que el 61 % de las PR de agentes no recibe revisión, sin fuente primaria clara. — [votazz](https://votazz.co/2026/07/07/ai-code-review-bottleneck/)

### Inferences
- La atenuación que mide el NBER (+240 % en commits frente a +30 % en releases) es la evidencia más directa de que más trabajo paralelo de IA no se traduce proporcionalmente en valor entregado. El eslabón débil es humano: revisión, integración y decisión.
- Para un desarrollador que dirige muchos proyectos, abrir más frentes con agentes aumenta el inventario de código sin revisar. Los datos de Faros (revisión ×5, QA +300 %, PR más grandes) indican que ese inventario tiene un coste creciente.

### Gaps
- No verifiqué en fuente primaria las cifras de Faros 2025 (+98 % PR, +91 % revisión, +154 % tamaño). Tampoco obtuve el dato de paralelismo o WIP de Faros.
- No encontré un estudio de Microsoft de 2025-2026 comparable con datos de revisión.

## 5. Calibración de la confianza, sesgo de automatización y dependencia excesiva

### Takeaway
La evidencia empírica directa sobre revisores humanos que pasan por alto defectos en código de IA es escasa. Lo más sólido es indirecto:
- la brecha de percepción de METR;
- el ensayo de Anthropic de 2026, según el cual delegar la generación de código reduce la comprensión;
- encuestas en las que la confianza depende de poder verificar.

### Cited Findings
- **Ensayo de Anthropic (29-01-2026, secundario y en web de Anthropic).** — [Anthropic research](https://www.anthropic.com/research/AI-assistance-coding-skills); [InfoQ](https://infoq.com/news/2026/02/ai-coding-skill-formation/)
  - 52 ingenieros, en su mayoría junior, aprendieron Trio, una biblioteca de Python que no conocían.
  - Quien usó IA obtuvo un 17 % menos en el test de comprensión, con la mayor diferencia en las preguntas de depuración, y solo fue unos 2 minutos más rápido, sin significación estadística.
  - Quien usó la IA para hacer preguntas conceptuales puntuó por encima del 65 %; quien delegó la generación de código, por debajo del 40% (secundario).
- **Brecha de percepción de METR (verificado).** Previsión de +24 %, percepción posterior de +20 % y resultado real de −19 %. — [METR 2025](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- **«More code, less validation» (arXiv 2512.19644, diciembre de 2025, secundario).** En programadores científicos, la productividad se juzga por el código generado y no por la validación, lo que favorece la dependencia excesiva. — [arXiv 2512.19644](https://arxiv.org/abs/2512.19644v1)
- **«Automated Code Review in Practice» (arXiv 2412.18531, secundario).** La dependencia excesiva de bots de revisión deja pasar bugs graves porque los revisores asumen que el bot ya los habría señalado. — [arXiv 2412.18531](https://arxiv.org/pdf/2412.18531)
- **Thoughtworks Technology Radar: «Complacency with AI-generated code» (opinión experta).** Alerta sobre la complacencia con el código generado por IA. — [Thoughtworks Radar](https://thoughtworks.com/radar/techniques/complacency-with-ai-generated-code)
- **DORA 2025 (verificado).** El 30 % confía poco o nada, aunque el 90 % usa IA: se usa sin confiar del todo. — [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report)
- **Faros, Speed Trap (verificado).** Fuertes aumentos de PR fusionadas sin revisión y revisión por IA en el 50–80 % de las PR: la revisión se delega a su vez en IA. — [Faros](https://www.faros.ai/blog/ai-speed-trap-takeaways)

### Inferences
- Una persona que no escribe el código y revisa cada vez menos se expone a dos riesgos acumulados: la degradación de la comprensión que mide Anthropic y la complacencia ante código pulido. Para la SF tiene sentido pasar de «revisar el código» a «verificar contra criterios», con tests de aceptación previos y evidencias de ejecución.

### Gaps
- No encontré un ensayo controlado de 2024-2026 que mida la tasa de defectos o vulnerabilidades que detectan revisores humanos en código de IA frente a código humano.

## 6. Trabajo en curso y trabajo en paralelo: ¿más trabajo paralelo de IA se traduce en valor entregado?

### Takeaway
No de forma proporcional. Las ganancias en producción de código se diluyen hacia proyectos, releases y uso. Además, la ejecución de agentes en paralelo aparece como un fenómeno que rompe la medición y desplaza el coste hacia la revisión y la QA.

### Cited Findings
- **NBER w35275 (verificado).** — [NBER w35275](https://www.nber.org/papers/w35275)
  - Con agentes autónomos, los commits crecen un 240 %, los proyectos un 80 % y las releases un 30 %.
  - Las apps nuevas aumentan mucho, pero el uso total no crece.
- **METR 2026 (verificado).** El uso de varios agentes concurrentes vuelve poco fiables los registros de tiempo, y algunas tareas quedaron sin terminar. — [METR 2026-02-24](https://metr.org/blog/2026-02-24-uplift-update/)
- **Faros 2.º trimestre de 2026 (verificado).** Las épicas completadas crecen un 66 %, pero los despliegues semanales bajan un 11,7 %, los incidentes mensuales suben un 57,9 % y el churn un 861 %. — [Faros](https://www.faros.ai/research/ai-acceleration-whiplash)
- **Faros 3.er trimestre de 2026 (verificado).** Los «restarts» suben un 66,7 % y el tiempo en QA un 300,6 %. — [Faros](https://www.faros.ai/blog/ai-speed-trap-takeaways)
- **DORA 2025 (verificado).** El mayor volumen de cambios desborda los controles y reduce la estabilidad. — [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report)

### Inferences
- La evidencia apoya limitar el trabajo en curso por proyecto y en total, y medir el progreso por entregas cerradas y validadas, no por PR o commits. La capacidad de revisión y decisión del único humano es la restricción del sistema.

### Gaps
- No encontré estudios específicos sobre desarrolladores individuales que gestionen varios proyectos en paralelo con agentes.
- No encontré cifras primarias de Faros sobre paralelismo o trabajo en curso.
