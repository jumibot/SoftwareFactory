# Problemas manifiestos y testimonios (2025-2026) relevantes para la SF

Notas de investigación, 2026-10-26. Complementan, sin repetirlo, [Fricciones humanas del desarrollo con IA](../../reports/Fricciones%20humanas%20del%20desarrollo%20con%20IA.md) (atención, agentes en paralelo, delegación, fatiga). Las citas entre comillas son literales tal como las devolvió la página consultada; «[paráfrasis]» marca lo que no es literal. **[solo/indie]** marca autores individuales. Se distingue **dato** (medido) de **opinión** (testimonio). Cobertura limitada (unas 20 consultas): falta revisar Reddit (r/indiehackers, r/SideProject, r/Teachers, r/learnprogramming), que no se consultó directamente.

## 1. Terminar proyectos: muchos se empiezan, pocos se acaban

### Takeaway
La IA abarata empezar y abre ideas aparcadas, pero los testimonios coinciden en que el cuello de botella se ha desplazado al último tramo (auth, pagos, despliegue, robustez) y, sobre todo, a la distribución y al interés sostenido. No encontré datos cuantitativos sobre tasas de abandono; solo anécdotas.

### Cited Findings
- Opinión, HN, ~feb 2026 [solo/indie]: sarbajitsaha pregunta «Is AI the final nail in the coffin for solo developers?»: «with agentic coding, I feel it has now become almost impossible» (ganarse la vida con apps o juegos) — [HN 47059223](https://news.ycombinator.com/item?id=47059223)
- En el mismo hilo, a favor de terminar: tracker1: «AI coding has gotten me more involved with personal project ideas I've let just sit for years.»; delaminator: «I've made things with Claude I wouldn't begin to do on my own.» — [HN 47059223](https://news.ycombinator.com/item?id=47059223)
- En el mismo hilo, en contra: marginalia_nu: «There's certainly more weekend projects being built, but the vast majority of it is unabashed shovelware.»; dudewhocodes: «You can be the greatest marketer but you will fail when all channels are flooded.»; midnitewarrior: «Is it simply the one that sticks around the longest and doesn't become abandonware?» — [HN 47059223](https://news.ycombinator.com/item?id=47059223)
- Opinión, hilo «I hate AI side projects» (artículo en dylancastillo.co, ~feb 2026; autoría no confirmada en la página): simonw: «If your side project took a couple of hours it's not worthy of a Show HN.»; socketcluster: «AI slop alternatives which were assembled in a few months with no long term vision»; rspoerri: «Until then i am going to work on my AI side project every evening until i deem it ready and bug free.» — [HN 47094637](https://news.ycombinator.com/item?id=47094637); artículo: [dylancastillo.co](https://dylancastillo.co/posts/ai-side-projects.html)
- Consejos previos a la IA que siguen citándose: proyectos terminados eran los que cabían en menos de una semana; trocear y aceptar el «progreso asintótico» del último 30 % [paráfrasis] — [HN 41010229 «How to finish last 30% of a side project?»](https://news.ycombinator.com/item?id=41010229); [HN 23672686](https://news.ycombinator.com/item?id=23672686)
- Opinión [solo/indie, fuente con ángulo comercial]: un constructor que lleva un año con vibe coding relata decenas de apps «casi terminadas» sin publicar y su remedio: una regla de un único proyecto principal, el resto en reposo hasta que salga [paráfrasis del resultado de búsqueda; no verificado en la página] — [blog.vibecoder.me](https://blog.vibecoder.me/indie-hacker-intermediate-path-building-and-shipping-solo)
- Dato relacionado (Stack Overflow 2025, 33.662 respuestas sobre uso de IA): el 66 % señala como frustración principal «AI solutions that are almost right, but not quite» y el 45,2 % dice que depurar código generado lleva más tiempo — [Stack Overflow Developer Survey 2025, IA](https://survey.stackoverflow.co/2025/ai)

### Inferences
- Para el hombre orquesta, el riesgo no es la falta de prototipos sino la dispersión: lo que ayuda según los testimonios es limitar el trabajo en curso (un proyecto principal), alcance pequeño y fijar de antemano qué significa «terminado» (incluyendo auth, pagos, despliegue y la distribución). Encaja con la preparación de devslices y criterios de aceptación de la SF.
- El «casi bien» del 66 % es la versión de cada tarea del «90 % hecho» del proyecto.

### Gaps
- No encontré estudios que cuantifiquen cuántos proyectos de indies con IA llegan a publicarse o a facturar. La expresión «90 % done» no apareció en fuentes verificables.
- No revisé Indie Hackers ni r/SideProject directamente.

## 2. Proliferación de herramientas, FOMO y coste de estar al día

### Takeaway
El testimonio más citado (Khare, feb 2026, nº 1 en HN) describe fines de semana perdidos evaluando herramientas con mejoras de ~5 % y recomienda un asistente principal y adoptar herramientas solo tras meses. Incluso Karpathy (dic 2025) declaró sentirse «más atrás que nunca». Las cifras de gasto y «demasiadas herramientas» que circulan en blogs no son verificables.

### Cited Findings
- Opinión, Siddhant Khare (ingeniero de infraestructura de agentes, mantenedor de OpenFGA), 8 feb 2026: «I was spending weekends evaluating new tools.»; «Reading every changelog. Watching every demo. Trying to stay at the frontier because I was terrified of falling behind.»; «Each migration cost me a weekend and gave me maybe a 5% improvement that I couldn't even measure properly.»; «I watched teams go from LangChain to CrewAI to AutoGen to custom orchestration in the span of a year.» — [siddhantkhare.com](https://siddhantkhare.com/writing/ai-fatigue-is-real)
- Sus recomendaciones: «I use one primary coding assistant and know it deeply.»; «I evaluate new tools when they've proven themselves over months, not days.»; «There's a difference between being informed and being reactive.»; «If a feed is making you feel behind instead of informed, it's not serving you.»; «Tools come and go. The problems they solve don't.» — [siddhantkhare.com](https://siddhantkhare.com/writing/ai-fatigue-is-real). Alcance: 470+ puntos en HN según su propia web [dato autodeclarado] — [siddhantkhare.com](https://www.siddhantkhare.com/)
- Opinión, Andrej Karpathy, X, 26 dic 2025: «I've never felt this much behind as a programmer.»; «I have a sense that I could be 10X more powerful if I just properly string together» [fragmento]; «A failure to claim the boost feels decidedly like skill issue.» — [x.com/karpathy](https://x.com/karpathy/status/2004607146781278521), citado por [AOL/Business Insider](https://www.aol.com/news/guy-coined-vibe-coding-now-172146964.html)
- Cifras no verificadas (no usar sin fuente primaria): gasto de 150-500 $/mes atribuido a JetBrains 2025; «73 % de trabajadores con demasiadas herramientas de IA» atribuido a Microsoft 2024; retención anual de apps de IA del 21,1 % — [buildmvpfast](https://www.buildmvpfast.com/blog/ai-fatigue-tool-overwhelm-developer-counter-trend-2026); [mylastai](https://mylastai.com/stats/ai-tool-fatigue-statistics-2026/); [favtray](https://favtray.com/blog/developer-subscription-fatigue-2026)

### Inferences
- Para la SF: una función de «vigilancia tecnológica» que filtre y resuma lanzamientos por lotes (no reactiva) y un contexto único del proyecto (brain en `docs/`) que no dependa de la herramienta del momento atacan directamente esta fricción.

### Gaps
- No encontré encuestas primarias fiables sobre número de suscripciones o gasto mensual de desarrolladores individuales en IA, ni sobre contexto disperso entre ChatGPT/Claude/Cursor.

## 3. Enseñar programación en la era de la IA

### Takeaway
La evidencia es mixta: con instrucción formal los estudiantes se perciben mejor, pero hay pérdidas medibles en evaluaciones sin IA y uso masivo no detectable. Los docentes están desplazando la nota hacia exámenes presenciales o defensas orales y diseñando tareas que obliguen a aprender.

### Cited Findings
- Testimonio docente, Ozan Erat (Yale, CPSC 223), The New Journal, 28 oct 2025: «one third of submissions have shown clear evidence of AI usage»; sobre una pregunta de examen acerca de una técnica no enseñada que aparecía en las entregas: «95 percent or 99 percent were not able to answer that question»; estima el uso real en «70 percent or more»; «If you let AI do the job for you, AI will take your job». En otoño de 2025 dejó de prohibir la IA: los deberes valen 0 % y tres exámenes escritos de tres horas, el 90 % — [The New Journal at Yale](https://thenewjournalatyale.com/2025/10/inside-yales-quiet-reckoning-with-ai/)
- Lin Zhong (Yale): «If your student[s] don't learn how to use [AI], they lose their job»; «You have to design the curriculum so that students are forced to learn, right?»; endureció su curso y da crédito extra por uso creativo de IA — [The New Journal at Yale](https://thenewjournalatyale.com/2025/10/inside-yales-quiet-reckoning-with-ai/)
- Dato, SIGCSE TS 2025 (curso de bases de datos): quienes usaron GenAI rindieron mejor en la parte donde estaba permitida, pero peor en el resto de la tarea y en el curso global [paráfrasis del resumen] — [SIGCSE TS 2025](https://sigcse2025.sigcse.org/details/sigcse-ts-2025-Papers/3/Understanding-the-Impact-of-Using-Generative-AI-Tools-in-a-Database-Course)
- Dato autodeclarado, SIGCSE TS 2025 (16 instituciones MSI): el 89 % ya usaba GenAI antes del curso sin instrucción; con instrucción formal la usaron sobre todo para explicar conceptos y valoraron positivamente su aprendizaje [paráfrasis] — [SIGCSE TS 2025](https://sigcse2025.sigcse.org/details/sigcse-ts-2025-Papers/35/Unlocking-Potential-with-Generative-AI-Instruction-Investigating-Mid-level-Software-)
- Dato, Northeastern/Wellesley/Oberlin: 120 estudiantes con poca experiencia tuvieron dificultades para que la IA escribiera código desde lenguaje natural porque les faltaba vocabulario y sintaxis para describir el problema [paráfrasis; fecha no confirmada] — [Khoury College](https://www.khoury.northeastern.edu/can-newbie-coders-use-chatgpt-instead-of-learning-to-write-code/)
- Dato contrario (experimento con 182 estudiantes de primer curso, 2024): el rendimiento global no se vio afectado por ChatGPT cuando el curso incluía evaluación tipo defensa [paráfrasis] — [MDPI Mathematics 12(5):629](https://www.mdpi.com/2227-7390/12/5/629)
- Dato, Anthropic (ver §4): el aprendizaje de una librería nueva con IA dio un 17 % menos en un cuestionario posterior; los patrones de pregunta conceptual preservaron el aprendizaje — [Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills)
- Línea de investigación activa sobre políticas docentes («vigilar o guiar») — [arXiv 2607.16475](https://arxiv.org/pdf/2607.16475) (no revisado en detalle)

### Inferences
- Para la actividad docente del propietario: evaluar con defensa oral o en vivo, hacer que el alumno pregunte conceptos en lugar de pedir código, y enseñar explícitamente a usar la IA (los alumnos ya la usan, el 89 %). La SF podría ofrecer plantillas de ejercicios con «modo tutor» (explica, no resuelve).

### Gaps
- No consulté r/Teachers ni r/learnprogramming; faltan testimonios de docentes de formación profesional o bootcamps (más cercanos al perfil del propietario) y estudios de ITiCSE 2025-2026.

## 4. Aprendizaje y atrofia de habilidades en desarrolladores experimentados

### Takeaway
El mejor dato disponible (ECA de Anthropic, ene 2026, n=52, mayoritariamente juniors) muestra 17 puntos menos de comprensión sin mejora de velocidad significativa, y que la forma de uso decide: pedir explicaciones conserva el aprendizaje; delegar lo destruye. Hay testimonios de seniors (Karpathy) que reconocen atrofia del código a mano.

### Cited Findings
- Dato, Shen y Tamkin (Anthropic), 29 ene 2026, ECA con 52 ingenieros aprendiendo Trio: grupo con IA 50 % vs 67 % en el cuestionario (d=0,738, p=0,01), mayor diferencia en depuración; ~23 vs 25 min, no significativo (p=0,391). Patrones con buena puntuación: generar y luego preguntar (86 %, n=2), código con explicación (68 %, n=3), solo preguntas conceptuales (65 %, n=7); delegación, dependencia progresiva y depuración iterativa con IA <40 %. Citas: «Cognitive effort—and even getting painfully stuck—is likely important for fostering mastery.»; «AI assistance should enable humans to work more efficiently _and_ develop new skills at the same time.» — [Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills); paper [arXiv 2601.20245](https://arxiv.org/abs/2601.20245). Limitaciones: muestra pequeña, retención a corto plazo, subgrupos de 2-7 personas.
- Opinión, Karpathy: reconoce que pierde poco a poco la capacidad de escribir código a mano y que ahora programa sobre todo «en inglés» con agentes [paráfrasis de la cobertura] — [AOL](https://www.aol.com/articles/ex-tesla-ai-head-seen-093701714.html)
- Opinión, Addy Osmani: compara la delegación en IA con el GPS que erosiona la orientación y aconseja no saltarse el depurador ni recurrir a la IA en cada excepción [paráfrasis] — [Elevate (Substack)](https://addyo.substack.com/p/avoiding-skill-atrophy-in-the-age)
- Opinión, Thoughtworks/Martin Fowler: el trabajo supervisado con agentes depende del criterio del desarrollador, que hay que preservar y entrenar [paráfrasis] — [martinfowler.com](https://www.martinfowler.com/articles/exploring-gen-ai/13-role-of-developer-skills.html)
- Testimonios [solo/indie]: un desarrollador se quedó en blanco con un bucle básico de Lua en una máquina sin Copilot [paráfrasis] — [DEV](https://dev.to/dev_tips/ai-killed-my-coding-brain-but-im-rebuilding-it-4i35); un junior se bloqueó en una tarea simple de React y concluye que nunca aprendió bien los fundamentos [paráfrasis] — [DEV](https://dev.to/mahou_anisphia/when-ai-makes-you-forget-how-to-code-5cii)
- Contrapunto: puede atrofiarse el tecleo mientras crecen la revisión, la arquitectura y la delegación [paráfrasis de un comentario] — [Substack](https://iamcharliegraham.substack.com/p/is-ai-making-me-lazy/comments)
- Regla práctica de Khare: «If the AI doesn't get me to 70% usable in three prompts, I write it myself.» — [siddhantkhare.com](https://siddhantkhare.com/writing/ai-fatigue-is-real)

### Inferences
- Para el aprendizaje del propietario: cuando el objetivo sea aprender una tecnología nueva, la SF debería usar un modo «explicar y comprobar comprensión» en lugar de «generar»; reservar práctica deliberada sin agente (p. ej., depuración manual) como tarea explícita.

### Gaps
- No hay estudios longitudinales sobre seniors; el ECA es de juniors y de una sesión.

## 5. Prototipos de vibe coding que llegan a producción

### Takeaway
Hay datos sólidos de fallos de seguridad masivos en apps generadas con plataformas de vibe coding, concentrados en control de acceso y datos expuestos sin autenticación, no en inyecciones clásicas. El uso de vibe coding en el trabajo profesional sigue siendo minoritario.

### Cited Findings
- Dato, Escape.tech, 29 oct 2025: escaneo pasivo de 5.600+ apps públicas (≈4.000 de Lovable, 449 Create.xyz, 159 Base44, además de Vibe Studio y Bolt.new): más de 2.000 vulnerabilidades, más de 400 secretos expuestos y 175 casos de datos personales (historias médicas, IBAN, teléfonos, correos); la mayoría de problemas críticos accesibles sin autenticación. Son mínimos (modo pasivo, verificación conservadora, sesgo hacia Lovable) — [Escape.tech](https://escape.tech/blog/methodology-how-we-discovered-vulnerabilities-apps-built-with-vibe-coding/)
- Dato, CVE-2025-48757 (marzo 2025): 170 de 1.645 apps de Lovable compartían un fallo crítico por falta de permisos en la base de datos [según cobertura secundaria] — [mothasa.substack](https://mothasa.substack.com/p/vibe-coding-has-a-security-problem); un fallo BOLA posterior quedó abierto 48 días tras cerrarse el informe del bug bounty sin escalarlo — [The Next Web](https://thenextweb.com/news/lovable-vibe-coding-security-crisis-exposed)
- Dato, Veracode 2025 (código generado en general, no apps de vibe coding): ~45 % del código de más de 100 modelos en 80 tareas contenía una vulnerabilidad OWASP Top 10; 72 % en Java [según cobertura secundaria; no verifiqué el informe primario] — [vibecodedirectory](https://vibecodedirectory.beehiiv.com/p/the-hidden-cost-of-speed-why-45-of-vibe-coded-apps-have-security-vulnerabilities-and-how-to-fix-it)
- Dato, Tenzai: 15 apps (3 por cada una de 5 herramientas) con 69 vulnerabilidades, 6 críticas; ninguna inyección SQL ni XSS explotable; fallos en lógica de negocio y autorización [según cobertura secundaria] — [The Next Web](https://thenextweb.com/news/lovable-vibe-coding-security-crisis-exposed)
- Dato, Stack Overflow 2025: el 72,2 % responde «No» y el 5,3 % «No, emphatically» a si hace vibe coding en el trabajo; ~15 % sí en algún grado. Confían en la precisión de la IA el 32,7 % y desconfían el 45,7 % — [Stack Overflow 2025](https://survey.stackoverflow.co/2025/ai)
- Opinión: el vibe coding sirve para prototipos, pero un sistema robusto con auth, seguridad y buenas prácticas es «way harder» [paráfrasis con fragmento] — [Transitions (Substack)](https://transitions.substack.com/p/vibe-coding-is-overrated)

### Inferences
- Para la SF: el paso de prototipo a producción necesita una puerta explícita (revisión de autorización/RLS, secretos, datos personales) antes de exponer nada. Lo crítico es la lógica de acceso, que los modelos no resuelven solos.

### Gaps
- No encontré estudios rigurosos sobre mantenibilidad a largo plazo ni de la «resaca del vibe coding» más allá de opiniones.

## 6. Agentes dentro de productos (Claude Code / Agent SDK) e incertidumbre de arquitectura

### Takeaway
Abunda material de tutorial y cursos, pero hay pocos testimonios primarios de paso de prototipo a producción. Lo que aparece apunta a que la configuración de Claude Code (CLAUDE.md, skills, MCP, hooks) se traslada al producto, y a lecciones de diseño genéricas (estado por eventos, permisos con denegación por defecto).

### Cited Findings
- Opinión de practicante [solo]: CLAUDE.md, skills, configuración MCP y hooks pasan de Claude Code a una app en producción; trazas por OpenTelemetry a Langfuse [paráfrasis] — [ProductCompass](https://www.productcompass.pm/p/claude-agent-sdk-production-agent)
- Guía: lista explícita de herramientas con denegación por defecto en agentes sin interfaz; los subagentes no pueden lanzar subagentes [paráfrasis] — [inference.net](https://inference.net/content/claude-agent-sdk-production-guide/)
- Resumen de una charla de Anthropic (AI Engineer Summit): «bash is all you need», descubrimiento de contexto por sistema de archivos, el arnés importa tanto como el modelo [paráfrasis de terceros] — [ML6](https://www.ml6.eu/en/blog/inside-the-claude-agents-sdk-lessons-from-the-ai-engineer-summit)
- Referencia académica no Claude: OpenHands Agent SDK resume cuatro lecciones de pasar de prototipo de investigación a producción: separar núcleo y aplicaciones, estado por eventos para recuperación, componentes inmutables y un único modelo de ejecución local/sandbox — [arXiv 2511.03690](https://arxiv.org/pdf/2511.03690)
- Dato: el 31 % aprox. usa agentes en el trabajo al menos ocasionalmente (14,1 % a diario) y el 37,9 % no tiene planes — [Stack Overflow 2025](https://survey.stackoverflow.co/2025/ai)

### Inferences
- La incertidumbre arquitectónica parece real, pero no está documentada en testimonios. Para la SF conviene aislar el agente operativo tras una interfaz propia (encaja con la regla de separar Claude Code de desarrollo y Claude Code como componente).

### Gaps
- No encontré testimonios verificables de desarrolladores que relaten dudas sobre la arquitectura final de un agente de producto tras prototiparlo con Claude Code. Sería útil buscar en r/ClaudeAI y en el GitHub de claude-agent-sdk (issues).

## 7. Creadores de hardware + software con IA (embebido, firmware, gemelos digitales)

### Takeaway
La fricción específica más documentada es la alucinación de APIs y de configuraciones de registros en microcontroladores, por la escasez de datos de entrenamiento por MCU. Las mitigaciones pasan por extraer el mapa de registros de la hoja de datos y validar con compilación cruzada y hardware en bucle (HIL).

### Cited Findings
- Dato/paper IEEE: la programación directa con LLM sufre «hallucinated library functions, incorrect register configurations, and low compilation success rates»; su canal con compilación cruzada y HIL declara 89,2 % de corrección funcional y 77,2 % menos de llamadas alucinadas (resultados de los propios autores) — [IEEE Xplore 11694922](https://ieeexplore.ieee.org/abstract/document/11694922/)
- Opinión de proveedor: el asistente «pattern-matching against whatever scraps made it into the training set» cuando se pide código para un periférico concreto — [ulogger.ai](https://ulogger.ai/blog/ai-coding-assistants-fall-flat-in-embedded.html)
- Prensa sectorial: la hoja de datos es central porque describe el orden correcto de uso de los registros [paráfrasis] — [Fierce Sensors](https://www.fiercesensors.com/ai/ai-hallucinations-embedded-are-yes-thing)
- Investigación: validación de seguridad y parcheo automáticos del firmware generado por LLM — [arXiv 2509.09970](https://arxiv.org/pdf/2509.09970)
- Mitigación práctica: extraer primero mapa de registros, campos de bits, límites de tiempo y secuencia de inicialización; generar a partir de esos datos estructurados y no del PDF en bruto [paráfrasis] — [Hubble](https://hubble.com/community/guides/how-firmware-engineers-get-the-most-out-of-claude/)

### Inferences
- Para proyectos con hardware, la SF debería tratar las hojas de datos como fuentes estructuradas del brain y exigir verificación en el dispositivo (o simulador/gemelo) como criterio de aceptación.

### Gaps
- No encontré testimonios de makers individuales ni datos sobre gemelos digitales con IA; tampoco encuestas de ingenieros de embebido. Un arXiv (2608.25217) sobre verificación de compatibilidad basada en hojas de datos apareció pero no lo revisé.

## Estimación de extensión (juicio propio, no medido salvo donde se indica)

| Problema | Extensión estimada | Base |
|---|---|---|
| 1. Terminar proyectos | Alta entre indies; sin datos | Muchos testimonios, cero estudios; 66 % «casi bien» (SO 2025) |
| 2. Proliferación de herramientas / FOMO | Alta y muy visible | Khare nº 1 en HN, Karpathy; cifras de gasto no verificadas |
| 3. Enseñar programación | Muy alta en docencia | 89 % usaba IA antes del curso; Yale estima ≥70 % |
| 4. Atrofia de habilidades | Media-alta, evidencia inicial | ECA n=52; testimonios de seniors |
| 5. Vibe coding a producción | Alta en plataformas no-code; minoritaria en el trabajo | Escape (2.000+ vulnerabilidades en 5.600 apps); SO: ~77 % no hace vibe coding en el trabajo |
| 6. Agentes en productos | Creciente; poco documentada | ~31 % usa agentes en el trabajo (SO 2025) |
| 7. Hardware + software | Nicho, fricción alta | Papers sobre alucinación de registros |
