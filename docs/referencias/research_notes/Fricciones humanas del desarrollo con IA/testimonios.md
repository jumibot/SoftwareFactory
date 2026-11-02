# Testimonios de desarrolladores sobre las fricciones humanas del trabajo con agentes de programación (2025-2026)

Notas de investigación del 2026-10-26. Las citas se dejan en inglés original, entre comillas, tal como las devolvió la lectura de cada página. **[paráfrasis]** marca resúmenes que no son literales. **[secundario]** marca lo que solo se vio a través de un tercero. **[perfil objetivo]** marca a personas que trabajan solas o como freelance en varios frentes a la vez. Limitación del método: las páginas se leyeron con una herramienta que extrae fragmentos, así que conviene volver a comprobar cada cita literal en su URL antes de publicarla.

## 1. Recuperar el contexto tras una pausa o al cambiar de proyecto («¿dónde estaba?»)

### Takeaway
Este problema se nombra a menudo, pero casi siempre aparece en guías técnicas sobre la memoria del agente (CLAUDE.md, ficheros de checkpoint, `--resume`) y casi nunca como testimonio en primera persona del coste humano. El testimonio más claro de alguien que lleva varios negocios a la vez habla del coste del cambio de contexto entre ellos.

### Cited Findings
- **[perfil objetivo]** Un fundador que lleva cuatro negocios a la vez usa Claude Code como capa organizadora. Su herramienta principal es un fichero de instrucciones por repositorio, que según él reduce las preguntas repetidas y acelera las sesiones nuevas. Cuenta que el coste del cambio de contexto con su antiguo horario por bloques era mayor de lo que esperaba **[paráfrasis, secundario: solo se vio en el resumen del buscador; la entrada tiene unos 328 días]**. — [Bunny Honey Club blog, «Claude Code for solo founders running multiple businesses»](https://blog.bunnyhoneyclub.com/posts/claude-code-for-solo-founders-running-multiple-businesses)
- Eva Keiffenheim (Lifelong Learning Club, escribe sobre aprendizaje e IA), 13-05-2026: «The greatest risk of automation is losing your mental model of the project.» y «If you don't know how the house is framed, you won't know when the AI installs a faulty beam.» Su consejo: «Step away, reset your attention, and return to review the output with fresh eyes.» — [Brain in the Clouds After Working With Claude Code](https://evakeiffenheim.substack.com/p/the-cognitive-costs-of-multi-clauding)
- Constantin Gonzalez (freelance, mentor, 27 años en TI), 16-07-2026, **[perfil objetivo]**: «Every dish that's still cooking with an agent somewhere keeps simmering in your head, too.» — [Why working with AI agents is so tiring](https://constantin.glez.de/posts/2026-07-16-why-working-with-ai-agents-is-so-tiring-and-what-to-do-about-it/)
- Las soluciones de la comunidad coinciden: guardar el estado en ficheros (CLAUDE.md, un fichero de checkpoint con el objetivo actual y el siguiente paso, los mensajes de commit) y no en el historial del chat. Aparece una herramienta, claunch, para mantener sesiones persistentes por proyecto **[secundario, contenido de herramientas, no testimonios]**. — [DEV: Claude Code Keeps Forgetting Your Project](https://dev.to/277479420qqcom_5c9aa4d3/claude-code-keeps-forgetting-your-project-heres-a-fix-2c4j); [DEV: lightweight session manager (claunch)](https://dev.to/kaz123/how-i-solved-claude-codes-context-loss-problem-with-a-lightweight-session-manager-265d); [AgentKit: context loss recovery](https://agentkit.best/blog/claude-code-guides/claude-code-context-loss-prevent-recover-session-issues)

### Inferences
- Casi todo lo publicado trata cómo recupera el contexto *el agente*, no la *persona*. Que el humano recupere el hilo de varios proyectos parece un hueco poco tratado, y por eso una oportunidad para la SF.
- La frase de Gonzalez sobre los platos que siguen «simmering in your head» describe el lado inverso: los proyectos abiertos no se olvidan, ocupan la cabeza.

### Gaps
- No encontré ningún testimonio en primera persona, verificable y de 2025-2026, de alguien que describa volver a uno de sus varios proyectos tras semanas y no saber dónde estaba. Puede existir en Reddit o X, pero las búsquedas no lo devolvieron.

## 2. Perder la dirección estratégica: deriva respecto a la visión cuando los agentes producen rápido

### Takeaway
Hay mucha literatura sobre la «architectural drift» provocada por los agentes, sobre todo en blogs de empresas, y poco testimonio personal sobre perder la visión de producto. La señal personal más fuerte viene de Willison: construye software que luego no usa, y la gente se queda sin backlog.

### Cited Findings
- Simon Willison (cocreador de Django, blogger independiente), Lenny's Podcast, publicado en su blog el 02-04-2026, [36:56–37:47]: sobre amigos que vacían su lista de proyectos personales, «they almost feel a sort of sense of loss at the end where they're like, well, okay, my backlog's gone. Now what am I going to build?». Sobre sí mismo: «every evening I'm like, let's take that project and finish it» y «I've got some very cool software that I built that I've never used.» — [simonwillison.net, Lenny's podcast](https://simonwillison.net/2026/Apr/2/lennys-podcast/)
- Sobre Armin Ronacher (creador de Flask, cofundador de Earendil), un resumen secundario de su ensayo «The Tower Keeps Rising» (13-07-2026) dice que los agentes permiten a cada ingeniero sacar funcionalidades en paralelo sin la coordinación que antes mantenía sincronizado el modelo mental compartido del código **[secundario; no pude abrir el original]**. — [ai-tldr resumen](https://ai-tldr.dev/releases/lucumr-tower-keeps-rising-jul13/); blog original: [lucumr.pocoo.org](https://lucumr.pocoo.org/)
- La deriva se define como la divergencia gradual entre la arquitectura prevista y el código fusionado. Ocurre porque los agentes optimizan la tarea inmediata y empiezan de cero en cada sesión. El remedio que se propone es dejar las decisiones por escrito donde los agentes puedan leerlas: ADR en el repositorio, CLAUDE.md o AGENTS.md **[contenido de empresas, no testimonios]**. — [AsDecided](https://asdecided.com/articles/how-to-prevent-architectural-drift-from-ai-coding-agents); [techdebt.guru](https://techdebt.guru/ai-architecture-drift/); [ogbuilds](https://ogbuilds.ai/qualityvibes/preventing-architectural-drift)
- El estudio interno de Anthropic (02-12-2025) concluye que el 27 % del trabajo asistido por Claude son tareas que no se habrían hecho de otra forma, como escalar proyectos o paneles de datos que estaría bien tener. Es un indicio de que crece el alcance. — [Anthropic, How AI is transforming work at Anthropic](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic)

### Inferences
- «Construir cosas que nunca uso» y «quedarse sin backlog» son formas concretas de perder el norte: la capacidad de producción supera la claridad sobre qué merece la pena construir. Esto respalda que la SF ancle cada proyecto a su visión.

### Gaps
- No encontré ningún testimonio individual que use la expresión «perder la visión» de un proyecto propio. El término de la comunidad es técnico («architectural drift»). No pude verificar el texto original de Ronacher.

## 3. Atención e interrupciones: pedir aprobaciones, vigilar a los agentes, cambios de tarea constantes

### Takeaway
Es una queja extendida y está bien documentada. Hay testimonios de figuras conocidas (Willison, Hashimoto), de freelances y de hilos de HN. Las peticiones de permiso cada pocos minutos generan muchas guías y herramientas de terceros. La respuesta más citada es la de Hashimoto: decidir uno mismo cuándo atender al agente.

### Cited Findings
- Simon Willison, 02-04-2026 [45:16]: «My programming work, I need two minutes every now and then to prompt my agent about what to do next.» y «I'm much more interruptible than I used to be.» — [simonwillison.net](https://simonwillison.net/2026/Apr/2/lennys-podcast/)
- Constantin Gonzalez, **[perfil objetivo]**, 16-07-2026: «I hopped between tasks all afternoon (I've started calling it agent hopping)»; «peeking at a still-working agent is a paid interruption with zero yield»; «agent notifications that interrupt you rebuild the bad kind of task switching with extra steps». — [constantin.glez.de](https://constantin.glez.de/posts/2026-07-16-why-working-with-ai-agents-is-so-tiring-and-what-to-do-about-it/)
- Wolfgang Wagner (formador y consultor TYPO3 con servicios propios), 10-08-2026, **[perfil objetivo probable]**: «So I filled in the gaps. I answered emails, sorted through tickets, and continued working on another project.»; «Even when I'm writing an email, the question lingers in the background: Is it done yet?»; «This unresolved loop weighs on me, even though I'm not consciously thinking about it.» Su contramedida experimental es tomar cada tarea en marcha del agente como señal para una pausa corta. La segunda parte, con los resultados, no estaba publicada. — [wwagner.net](https://wwagner.net/en/blog/a/more-time-thanks-to-ai-but-still-exhausted-a-personal-experiment)
- Mitchell Hashimoto (cofundador de HashiCorp, creador de Ghostty), The Pragmatic Engineer, 25-02-2026: «If I'm coding, I want an agent planning. If they're coding, I want to be reviewing.» y «the best engineers are the ones that context-switch the least.» Que apaga las notificaciones del agente y decide él cuándo interrumpirlo solo aparece en resúmenes de terceros **[secundario]**. — [Pragmatic Engineer, Mitchell Hashimoto's new way of writing code](https://newsletter.pragmaticengineer.com/i/188952833/key-observation-from-mitchell); [teamday.ai resumen](https://www.teamday.ai/ai/hashimoto-new-way-of-writing-code)
- Hilo de HN sobre el artículo de Bloomberg «Claude Code and the Great Productivity Panic of 2026» (26-02-2026). scuff3d escribe «My brain feels like a fractured mess.» y bbangjo «the speed of ai-assisted coding removeds the natrual pause» (sic). — [HN 47467922](https://news.ycombinator.com/item?id=47467922)
- Sobre los permisos: guías que describen peticiones que obligan a cambiar de contexto cada pocos minutos. Una sostiene que pedir permiso quince veces por hora acostumbra a la gente a aceptar sin leer. Un desarrollador creó un notificador porque volvía y encontraba la sesión parada en una petición de permiso **[secundario, guías]**. — [understandingdata, YOLO mode](https://understandingdata.com/posts/yolo-mode-configuration/); [DEV, why Claude Code keeps asking](https://dev.to/vincentchabran/why-claude-code-keeps-asking-for-permission-and-how-to-fix-your-setup-so-it-stops-3ho8); [GitHub issue 48225](https://github.com/anthropics/claude-code/issues/48225)
- Tim Dettmers (Allen Institute y CMU) sostiene que la productividad máxima con agentes exige cambiar de contexto casi constantemente, algo para lo que los humanos no estamos hechos **[secundario: según Axios; la página devolvió 403]**. — [Axios, 04-04-2026](https://www.axios.com/2026/04/04/ai-agents-burnout-addiction-claude-code-openclaw)

### Inferences
- Este es el punto con más testimonios independientes. El patrón es «relleno cada espera con otra tarea → acabo agotado». Las respuestas que se proponen son de tres tipos: horarios (Hashimoto), pausas (Wagner) y no mirar al agente mientras trabaja (Gonzalez).

### Gaps
- No encontré una cifra fiable de la frecuencia real de las peticiones de aprobación. Las guías hablan de «cada pocos minutos» sin medirlo.

## 4. Delegar con menos control: revisar código ajeno, confianza, deuda de comprensión

### Takeaway
La «comprehension debt», término acuñado por Addy Osmani (Anthropic), está consolidada y respaldada por un ensayo controlado. Los ingenieros de Anthropic describen cómo se pierden habilidades y la «paradoja de la supervisión». También hay testimonios de quien admite que solo echó un vistazo al código.

### Cited Findings
- Addy Osmani (Member of Technical Staff en Anthropic, trabaja en Claude Code), 14-03-2026: «comprehension debt breeds false confidence»; «The codebase looks clean. The tests are green.»; «Engineers approved code they didn't fully understand, which now carries implicit endorsement.»; «a junior engineer can now generate code faster than a senior engineer can critically audit it.» Cita un ensayo con 52 ingenieros: el grupo asistido por IA sacó un 17 % menos en comprensión (50 % frente a 67 %), arXiv 2601.20245. — [addyosmani.com, Comprehension debt](https://addyosmani.com/blog/comprehension-debt/)
- Ingenieros de Anthropic (encuesta a 132 personas y 53 entrevistas, agosto de 2025, publicada el 02-12-2025): «I am for sure atrophying in my skills as a software engineer.»; «When producing output is so easy and fast, it gets harder and harder to actually take the time to learn something.». Un ingeniero calcula que su trabajo pasó en «70%+ to being a code reviewer/reviser rather than a net-new code writer.» El informe lo llama «paradox of supervision». Más de la mitad dice que solo puede delegar del todo entre el 0 y el 20 % de su trabajo. — [Anthropic](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic)
- Siva (SivaLabs, desarrollador Java y Spring), 30-06-2026: «I hadn't actually reviewed the AI-generated code.» y «I had only checked whether it looked reasonable.» — [SivaLabs](https://www.sivalabs.in/blog/ai-agents-are-doing-the-heavy-lifting/)
- Margaret-Anne Storey escribió un ensayo sobre la «cognitive debt» que O'Reilly cita junto al de Yegge **[secundario; no se leyó el original]**. — [O'Reilly Radar](https://www.oreilly.com/radar/?p=18698)
- En HN, pbjhsu escribe: «the frontier we're hitting isn't productivity, it's trust.» — [HN 47467922](https://news.ycombinator.com/item?id=47467922)

### Inferences
- Para un desarrollador solo que no tiene revisores, la deuda de comprensión es acumulativa y no tiene red de seguridad. La métrica de Anthropic sobre lo que se puede delegar del todo (0-20 %) sirve para moderar las expectativas.

### Gaps
- La búsqueda de «vibe coding hangover» solo devolvió explicaciones genéricas y una guía en italiano que cita a Fast Company (septiembre de 2025), que no pude verificar.

## 5. Trabajo en paralelo: muchos agentes o proyectos a la vez, más frentes abiertos que cerrados

### Takeaway
El «multi-clauding» es una práctica habitual, avalada por los creadores de Claude Code, con un límite humano muy claro. Willison dice que con cuatro agentes está agotado a las 11 de la mañana. Osmani recomienda que cada uno encuentre su techo. Otros cuentan que el cuello de botella pasa a ser la persona que revisa.

### Cited Findings
- Simon Willison, 02-04-2026 [26:25]: «I can fire up four agents in parallel and have them work on four different problems.» y «And by like 11 AM, I am wiped out for the day.» — [simonwillison.net](https://simonwillison.net/2026/Apr/2/lennys-podcast/)
- Willison, según Axios: «There is a limit on human cognition, in how much you can hold in your head at one time» y que es muy fácil «pop that stack» **[secundario]**. — [Axios](https://www.axios.com/2026/04/04/ai-agents-burnout-addiction-claude-code-openclaw)
- Boris Cherny (Head of Claude Code, Anthropic): «I feel like now is the age of multi-clauding.» **[citado por Keiffenheim]**. Keiffenheim añade: «Every time you context-switch between agents, your brain leaves behind 'attention residue'». — [evakeiffenheim.substack.com](https://evakeiffenheim.substack.com/p/the-cognitive-costs-of-multi-clauding)
- Javatarz (DEV) llevaba tres o cuatro agentes de Claude Code en paralelo sobre tarjetas del backlog y acabó siendo él el cuello de botella, porque los agentes van más rápido de lo que una persona revisa y redirige **[paráfrasis]**. — [DEV, Multi-Agent Development Workflows](https://dev.to/javatarz/multi-agent-development-workflows-with-claude-code-n23)
- Gijs (Substack) usa entre una y tres instancias, siente que va por detrás con la IA y tiene ansiedad por los límites de uso **[paráfrasis]**. — [gijs.substack.com](https://gijs.substack.com/p/running-multiple-ai-agents-in-parallel)
- Siva (SivaLabs): «I can deeply focus on maybe two things before my brain starts filing formal complaints.» — [SivaLabs](https://www.sivalabs.in/blog/ai-agents-are-doing-the-heavy-lifting/)
- Constantin Gonzalez, **[perfil objetivo]**, sobre el lado bueno: «It felt great: three streams of steady progress, one me.» — [constantin.glez.de](https://constantin.glez.de/posts/2026-07-16-why-working-with-ai-agents-is-so-tiring-and-what-to-do-about-it/)
- Según un resumen, Addy Osmani propone que cada persona encuentre su techo personal de agentes en paralelo **[secundario: tuit citado en un hilo]**. — [Business Insider vía AOL](https://www.aol.com/articles/ai-pilled-engineers-working-harder-081601472.html)
- Hilos de Indie Hackers anteriores a la IA ya muestran el mismo patrón: «working on more than 2 projects... very challenging», y alguien que llevaba varios proyectos personales a la vez «ended up not getting anywhere» **[paráfrasis de los fragmentos; sin fecha verificada]**. — [Indie Hackers, How many projects are you currently working on?](https://www.indiehackers.com/post/how-many-projects-are-you-currently-working-on-e7f67780cd)

### Inferences
- El límite que se cita con más frecuencia está entre dos y cuatro frentes simultáneos para mantener la calidad. Encaja con la tradición indie anterior a la IA («2-3 proyectos con uno principal»). La IA abarata empezar proyectos, pero no cerrarlos ni revisarlos.

### Gaps
- No encontré ningún testimonio verificable de un indie hacker que lleve varias startups de riesgo con agentes y explique cómo reparte la atención entre ellas, aparte del post de Bunny Honey Club, que solo vi en un resumen.

## 6. Estrés, fatiga, burnout, pérdida del flow y de la alegría… y el entusiasmo

### Takeaway
La «AI fatigue» o «agent fatigue» es un tema principal en 2026. Los textos de referencia son «The AI Vampire» de Yegge (febrero), el podcast de Willison (abril), la cobertura de Axios, Bloomberg y Business Insider y varios blogs personales. A la vez, casi todos los que se quejan siguen siendo entusiastas. La pérdida de la alegría de programar tiene su propio grupo de ensayos desde 2025.

### Cited Findings
**Fatiga y burnout**
- Steve Yegge (veterano de Amazon y Google, autor de Beads y Gas Town), «The AI Vampire», febrero de 2026: «And you're _exhausted._ You're tired, Boss. You got nothing for it.» Dice que solo está cómodo a ese ritmo «for short bursts of a few hours once or occasionally twice a day». Willison lo resume como «four hours of agent work a day is a more realistic pace» y menciona que necesita dormir más por la carga cognitiva **[paráfrasis de Willison]**. Business Insider habla de tres horas productivas al día; O'Reilly, de cuatro o cinco **[las fuentes difieren en la cifra]**. — [Willison sobre Yegge, 15-02-2026](https://simonwillison.net/2026/Feb/15/the-ai-vampire/); original: [steve-yegge.medium.com](https://steve-yegge.medium.com/the-ai-vampire-eda6e4f07163) **[no leído directamente]**; [BI vía AOL](https://www.aol.com/articles/software-engineer-says-theres-vampiric-095101323.html)
- Simon Willison [26:25]: «using coding agents well is taking every inch of my 25 years of experience as a software engineer, and it is mentally exhausting.»; «There's an element of sort of gambling and addiction to how we're using some of these tools.»; sobre quedarse sin dormir para lanzar más agentes: «That's obviously unsustainable.» — [simonwillison.net](https://simonwillison.net/2026/Apr/2/lennys-podcast/)
- Eva Keiffenheim: «Every workday felt exhausting. I wasn't recovering overnight.» — [Substack](https://evakeiffenheim.substack.com/p/the-cognitive-costs-of-multi-clauding)
- Wolfgang Wagner: «I was exhausted, and my head felt full.» y «More tired than I used to be on days when I did everything by hand.» — [wwagner.net](https://wwagner.net/en/blog/a/more-time-thanks-to-ai-but-still-exhausted-a-personal-experiment)
- Siva: «I was exhausted.» y «Just mentally drained.» — [SivaLabs](https://www.sivalabs.in/blog/ai-agents-are-doing-the-heavy-lifting/)
- Gonzalez: «my head was buzzing» y «Expect the tiredness. It's arithmetic, not weakness.» — [constantin.glez.de](https://constantin.glez.de/posts/2026-07-16-why-working-with-ai-agents-is-so-tiring-and-what-to-do-about-it/)
- En HN, npilk: «spending time working with Claude Code leaves me feeling the same way I feel after a day scrolling Reddit and HN»; iainctduncan: «Alomst makes me want to just teach music lessons again» (sic). Como contrapunto, bayareapsycho: «I don't really feel this kind of friction.» — [HN 47467922](https://news.ycombinator.com/item?id=47467922)
- Según Business Insider, Willison dice que la fatiga ha aumentado desde noviembre de 2025 **[secundario]**. — [BI vía AOL](https://www.aol.com/articles/ai-pilled-engineers-working-harder-081601472.html)
- Dato contrastado: en el ensayo de METR de 2025, los desarrolladores experimentados con IA fueron un 19 % más lentos aunque creían ir un 20 % más rápido **[citado por Keiffenheim]**. — [Substack](https://evakeiffenheim.substack.com/p/the-cognitive-costs-of-multi-clauding)

**Pérdida de la alegría y del flow**
- Ingenieros de Anthropic: «Spending your day prompting Claude is not very fun or fulfilling.»; «It's the end of an era for me» (25 años programando); y, en sentido contrario, «I thought that I really enjoyed writing code, and instead I actually just enjoy what I get out of writing code.» y «The more excited I am to do the task, the more likely I am to not use Claude.» — [Anthropic](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic)
- Ensayos personales: Alexandru Nedelcu, «'AI' Sucks the Joy Out of Programming» (27-10-2025); Meysam Azad, «AI-Assisted Coding Killed My Joy of Programming» (01-12-2025); Alsado, «ai does not spark joy in programming» (el código ya no le parece una expresión creativa y dice que eso «deserves a bit of mourning» **[paráfrasis del fragmento]**); Elio Struyf se pregunta si la IA le quita la alegría o si es él quien la cede; Juntao dice ser más productivo pero no entrar en «the zone»; y el hilo «Tell HN: I Lost Joy of Programming» **[solo vistos los fragmentos del buscador]**. — [alexn.org](https://alexn.org/blog/2025/10/27/ai-sucks-the-joy-out-of-programming/); [meysam.io](https://meysam.io/blog/ai-assisted-coding-killed-programming-joy/); [alsado.ca](https://alsado.ca/posts/ai-does-not-spark-joy-in-programming/); [eliostruyf.com](https://www.eliostruyf.com/ai-taking-joy-out-of-coding-or-giving-it-away/); [juntao.substack.com](https://juntao.substack.com/p/ai-is-making-you-a-shallow-developer); [HN 44499063](https://news.ycombinator.com/item?id=44499063)

**Entusiasmo**
- Simon Willison: «I write so much of my code on my phone. It's wild.»; «I can get good work done walking the dog along the beach, which is delightful.»; «I've always loved prototyping things, and prototyping is even more valuable now.» Según BI, sigue siendo optimista y dice que trabaja más rápido. — [simonwillison.net](https://simonwillison.net/2026/Apr/2/lennys-podcast/)
- Constantin Gonzalez: «It felt great: three streams of steady progress, one me.» y cierra felicitando al lector por su «promotion to head chef». — [constantin.glez.de](https://constantin.glez.de/posts/2026-07-16-why-working-with-ai-agents-is-so-tiring-and-what-to-do-about-it/)
- Anthropic: los empleados dicen sentirse más productivos y más «full stack», y un investigador compara tener muchas instancias de Claude con «having a million horses… allows you to test a bunch of different ideas». — [Anthropic](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic)
- Armin Ronacher, «A Year of Vibes» (22-12-2025): usa a diario varios agentes de línea de comandos (Amp, Claude Code y Pi) **[paráfrasis del fragmento]**. — [lucumr.pocoo.org](https://lucumr.pocoo.org/2025/12/22/a-year-of-vibes/)

### Inferences
- **Grado de difusión (valoración cualitativa):** la fatiga y el cambio de contexto en paralelo (frentes 3, 5 y 6) son las quejas más extendidas. Las recogen medios generalistas (Axios, Bloomberg, Business Insider, O'Reilly), figuras de referencia y muchos blogs personales, con un pico entre febrero y julio de 2026. La deuda de comprensión (frente 4) es muy citada pero más conceptual. La deriva de la visión (2) y la recuperación de contexto de la persona (1) están poco tratadas como experiencia humana; se discuten sobre todo como problemas técnicos del agente.
- Mucha cobertura repite las mismas citas de Willison y Yegge, así que las voces independientes son menos de las que parece.
- El patrón emocional que se repite es la ambivalencia: «es fantástico» y «estoy agotado» en la misma persona (Willison, Gonzalez, Yegge). Es el mismo perfil que el del propietario.
- Los remedios propuestos convergen: limitar las horas (Yegge), limitar los agentes a la vez (Willison, Osmani), no rellenar las esperas (Wagner), no mirar al agente ni recibir notificaciones (Gonzalez, Hashimoto) y dejar el contexto por escrito en ficheros (comunidad).

### Gaps
- No pude abrir directamente el artículo de Axios (403), el de Bloomberg, el original de Yegge en Medium ni el ensayo de Ronacher. Lo que se cita de ellos es secundario.
- Las citas de HN son fragmentos cortos devueltos por la herramienta. Conviene confirmarlas con su contexto completo.
- Faltan testimonios de Reddit (r/ClaudeAI, r/ExperiencedDevs): las búsquedas no devolvieron hilos concretos. Tampoco encontré textos de Kent Beck, Thorsten Ball, Geoffrey Huntley ni Jesse Vincent sobre estas fricciones dentro del presupuesto de búsqueda.
