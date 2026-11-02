# Métodos y flujos de trabajo con agentes para una persona con muchos proyectos de riesgo (a 2026-10-26)

Notas de investigación. Leyenda de fiabilidad:
- **[V]**: verificado en esta sesión leyendo la fuente primaria (WebFetch).
- **[S]**: secundaria (prensa o resúmenes de búsqueda), sin leer la fuente primaria.
- **[N]**: URL y contenido tomados de conocimiento previo, **no comprobados en esta sesión**; verificar antes de citar.

No se repiten Spec Kit, BMAD, Superpowers, Kiro, Agent OS ni la crítica de Böckeler. Las citas literales solo aparecen cuando la herramienta las devolvió entre comillas; el resto son paráfrasis.

## 1. Flujos personales publicados por ingenieros con experiencia

### Takeaway
Los flujos maduros coinciden en cinco cosas que la SF ya tiene: idea afinada por entrevista → spec escrita → plan en pasos pequeños con tests → ejecución con una comprobación ejecutable → revisión humana. Lo nuevo y aprovechable es: (a) un archivo de plan o checklist que el agente marca como memoria entre sesiones (Harper Reed `todo.md`, Beck `plan.md`, Huntley `fix_plan.md`); (b) señales explícitas de que el agente se desvía (Beck); (c) separar commits estructurales y de comportamiento (Beck, Tidy First); (d) diseñar el entorno para que el agente se observe solo (logs en archivo, Makefile, herramientas rápidas; Ronacher); (e) revisión adversarial en contexto limpio (Anthropic).

### Cited Findings
**Harper Reed, «My LLM codegen workflow atm», 16-02-2025** [V] — [harper.blog](https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/)
- Tres fases. (1) Spec: un LLM conversacional hace **una pregunta cada vez** para afinar la idea y compila `spec.md`. (2) Plan: un modelo de razonamiento redacta un blueprint, lo trocea en pasos pequeños y testeables y genera prompts de codegen (variante TDD y no TDD) en `prompt_plan.md`, más un checklist `todo.md` que la herramienta va marcando **para conservar el estado entre sesiones**. (3) Ejecución con Claude o Aider.
- Brownfield: planifica **por tarea**, no el proyecto entero; empaqueta el código con Repomix y genera README, revisión de código, issues y tests que faltan.
- Advertencias del autor: el flujo «probablemente no funcione dentro de 2 semanas»; es fácil ir «over my skis» (demasiado rápido), y los documentos de plan y los tests lo frenan; Claude tiende a React por defecto, así que fija antes la base y el tooling; el flujo es básicamente **de un solo jugador** y colaborar varias personas con agentes es difícil; los tiempos de espera los llena con otras tareas.
- *Qué tomar:* la entrevista de una pregunta cada vez (ya está en la visión de la SF), `todo.md` como checklist que marca el agente, fijar el stack antes de generar y el trato distinto de greenfield y brownfield. *Conflicto con la SF:* planifica el proyecto entero de una vez en greenfield, mientras la SF detalla solo cuando está claro; no tiene kanban ni aprobación humana formal de la integración.

**Kent Beck, «Augmented Coding: Beyond the Vibes», 25-06-2025** [V] — [newsletter.kentbeck.com](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes) (antes tidyfirst.substack.com)
- Distinción: en *vibe coding* solo importa el comportamiento y los errores se devuelven a la IA; en *augmented coding* importan el código, la complejidad, los tests y la cobertura. Valores como en la programación a mano («tidy code that works»), pero escribiendo poco código él mismo.
- System prompt (apéndice): el agente sigue `plan.md`; con «go» busca el siguiente test sin marcar, lo implementa y escribe solo lo justo para pasarlo. Red → Green → Refactor. *Tidy First*: separar los cambios estructurales de los de comportamiento, también en los commits. Commit solo con todos los tests en verde y sin warnings; commits pequeños etiquetados como estructurales o de comportamiento.
- **Tres señales de que la IA se desvía:** bucles; funcionalidad no pedida, aunque sea un paso siguiente razonable; indicios de trampa, como desactivar o borrar tests.
- *Qué tomar:* las tres señales como checklist de supervisión y de informe de cierre; la etiqueta estructural/de comportamiento en los commits de cada devslice; «go» al siguiente test sin marcar como ritmo de TDD. *Conflicto:* ninguno grave; el artículo no describe el formato de `plan.md`.

**Simon Willison, «Vibe engineering», 07-10-2025** [V] — [simonwillison.net](https://simonwillison.net/2025/Oct/7/vibe-engineering/)
- Propone *vibe engineering* como contrapunto disciplinado del vibe coding: ingenieros con experiencia usan agentes **sin dejar de responder del software**. Los agentes premian las buenas prácticas de siempre: tests automáticos (el test-first encaja con agentes que iteran en bucle), plan de alto nivel antes de delegar, documentación, control de versiones (los agentes manejan bien `git bisect`), CI/lint/formato, revisión de código rápida, **habilidades de gestión** (instrucciones claras, contexto, feedback accionable), QA manual, investigación previa para probar enfoques, entornos de previsualización, criterio para delegar y **reajustar estimaciones**.
- *Qué tomar:* la lista sirve como autoevaluación de la SF (casi todo está cubierto; faltan entornos de preview y un criterio explícito de qué no delegar). *Conflicto:* ninguno.
- Otras piezas suyas [N]: «Here's how I use LLMs to help me write code», 11-03-2025 — https://simonwillison.net/2025/Mar/11/using-llms-for-code/ (pedir opciones antes de elegir, «vibe-coding» para prototipos y aprendizaje, el humano es responsable de probar).

**Armin Ronacher, «Agentic Coding Recommendations», 12-06-2025** [V] — [lucumr.pocoo.org](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)
- Ejecuta Claude Code sin permisos (propone Docker para contener el riesgo). Recomienda Go en backends nuevos porque los agentes lo manejan mejor que Python: contexto explícito, tests incrementales rápidos y ecosistema estable.
- «Lo más tonto que funcione»: funciones mejor que clases, sin herencia, **SQL plano que coincide con los logs** y comprobaciones de permisos visibles y locales.
- Todo lo que el agente puede usar u observar es una herramienta: comandos en un Makefile (`make dev`), pidfile para no lanzar servicios duplicados, **logs en archivos que el agente lee** y emails impresos en stdout en modo debug para que encuentre solo los enlaces de login. Las herramientas deben ser rápidas, dar errores claros y resistir el mal uso.
- Refactorizar cuando el código supera lo que el agente abarca; ni antes ni después. Paralelizar con checkouts separados y aislar el estado compartido (BD, Redis). Actualizar dependencias con prudencia y preferir generar código a añadir dependencias.
- Posteriores [S, según el resultado de búsqueda]: «Agentic Coding Things That Didn't Work» (30-07-2025) y «A Year of Vibes» (22-12-2025, https://lucumr.pocoo.org/2025/12/22/a-year-of-vibes/), donde dice apostar por generación de código, sistemas de archivos y aprendizaje basado en skills.
- *Qué tomar:* encaja de lleno con SQL nativo y backend primero; añadir a la definición técnica de la SF un **«entorno observable por el agente»** (logs a archivo, comandos únicos, servicios idempotentes). *Conflicto:* saltarse los permisos choca con la aprobación humana y con el uso seguro; la elección de Go es una preferencia personal.

**Geoffrey Huntley, «Ralph Wiggum as a "software engineer"», 14-07-2025** [V] — [ghuntley.com/ralph](https://ghuntley.com/ralph/)
- Bucle bash que reinyecta un `PROMPT.md` al agente indefinidamente. Specs nacidas de una conversación larga, un archivo por requisito; `fix_plan.md` como lista priorizada que se regenera comparando specs y código; `AGENT.md` con cómo construir y ejecutar, que el agente mantiene breve.
- Reglas: **un elemento por vuelta**; el mismo contexto se carga en cada vuelta; el contexto principal hace de planificador y los subagentes buscan y resumen; «buscar antes de suponer» que algo no existe; sin placeholders. *Backpressure*: tests de la unidad cambiada tras cada cambio, análisis estático, que el agente documente por qué importa cada test, y commit/tag cuando todo pasa.
- Advertencias: duplicados por no determinismo; puedes despertar con el build roto; **no recomendado en código existente**, sí en greenfield (el autor espera ~90 % de compleción); sigue haciendo falta criterio senior.
- *Qué tomar:* «un elemento por vuelta» confirma el tamaño del devslice; «documentar por qué existe cada test»; «buscar antes de suponer». *Conflicto:* la autonomía nocturna sin revisión choca con la aprobación humana y con no programar actividad en segundo plano sin autorización; como mucho, un experimento acotado en un spike desechable.

**Anthropic, «Best practices for Claude Code» (documentación viva, consultada 26-10-2026)** [V] — [code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices) (antes anthropic.com/engineering/claude-code-best-practices)
- Restricción central: el contexto se llena rápido y el rendimiento cae al llenarse.
- **Dar al agente una comprobación ejecutable** (tests, build, captura comparada): «es la diferencia entre una sesión que vigilas y una de la que te puedes ir». Endurecer por niveles: en el prompt, `/goal`, Stop hook determinista y subagente verificador. Pedir **evidencias** (salida de tests, comando y resultado) en vez de afirmaciones.
- Explorar → planificar → implementar → commit con plan mode; saltarse el plan si el diff cabe en una frase.
- **Que Claude te entreviste** (AskUserQuestion) y escriba `SPEC.md`, y luego ejecutar en sesión nueva. Las mejores specs nombran archivos e interfaces, dicen qué queda fuera de alcance y acaban con una verificación de extremo a extremo.
- CLAUDE.md corto: por cada línea, preguntar si quitarla causaría errores; lo ocasional va a skills; lo obligatorio, a hooks. Tras dos correcciones fallidas, `/clear` y mejor prompt. Nombrar sesiones como ramas (`/rename`, `--resume`).
- **Revisión adversarial** en subagente con contexto limpio contra PLAN.md, pidiendo solo huecos que afecten a la corrección o a los requisitos, porque perseguir todos los hallazgos lleva a sobreingeniería. Patrón escritor/revisor en dos sesiones.
- *Qué tomar:* casi todo ya encaja; incorporar «evidencia en el informe de cierre», «spec con fuera de alcance y verificación e2e», «revisor que solo informa de huecos de corrección o de criterio» y «sesión nueva tras escribir la spec». *Conflicto:* el modo auto o desatendido debe pasar por la aprobación del propietario.

**Anthropic, «How Anthropic teams use Claude Code», 24-07-2025** [V] — [claude.com/blog](https://claude.com/blog/how-anthropic-teams-use-claude-code)
- Diseño de producto: Figma → bucles autónomos (escribe, ejecuta tests, itera) con revisión humana antes del refinado final; mapear los estados de error durante el diseño. Prototipos one-shot en sandbox de perfiles no programadores. Onboarding y explicación de código, con una reducción de ~80 % del tiempo de investigación declarada por el equipo de Inference.
- *Qué tomar:* refuerza el vibe design y la matriz de estados de la skill de interfaz. La cifra del 80 % es autodeclarada, sin método.

**Thorsten Ball** [N] — «How to Build an Agent», ampcode.com, abril 2025 — https://ampcode.com/how-to-build-an-agent : un agente es un LLM, un bucle y unas pocas herramientas. Útil para el Claude Code «componente operativo» de la SF, no como método de desarrollo. No verificado.

**Steve Yegge y Gene Kim, *Vibe Coding: Building Production-Grade Software With GenAI, Chat, Agents, and Beyond*, IT Revolution (2025)** [S] — [bookshop.org](https://bookshop.org/p/books/vibe-coding-building-production-grade-software-with-genai-chat-agents-and-beyond-gene-kim/b6e53e37eeba8cac); [Simon & Schuster](https://www.simonandschuster.com.au/books/Vibe-Coding/Gene-Kim/9781966280033)
- Solo se confirmaron título, autores, prólogo de Dario Amodei y la meta declarada de proyectos más ambiciosos sin perder calidad. No se confirmó el acrónimo FAAFO ni las prácticas concretas. El resumen de Blinkist no encaja con la descripción del editor y no es fiable.

### Inferences
- Un patrón común que la SF puede formalizar dentro de cada devslice: un **archivo-checklist marcado por el agente** (Reed/Beck/Huntley) enlazado a la tarea del kanban. El kanban guarda la memoria entre slices y el checklist, la memoria dentro de la slice.
- Las tres señales de Beck y la revisión adversarial de Anthropic se pueden juntar en un apartado fijo del informe de cierre: «¿hubo bucles, alcance extra o tests tocados?».
- Reed y Huntley insisten en que su método es de un solo jugador o solo greenfield; la SF, con varios proyectos en marcha, necesita además la capa de cartera (sección 3), que ninguno cubre.

### Gaps
- No se leyó el texto primario de Yegge (ni el libro ni el post «Revenge of the junior developer»); FAAFO sin confirmar.
- No se localizó el post primario de Karpathy sobre «agentic engineering» (ver la sección 2).
- Thorsten Ball y el post de Willison de marzo de 2025 están sin verificar en esta sesión.

## 2. Métodos para la incertidumbre y la exploración (spikes, Shape Up, Lean, vibe coding frente a agentic engineering)

### Takeaway
Para proyectos de riesgo, lo más reutilizable de Shape Up es el **appetite** (tiempo fijo con alcance flexible) y el **circuit breaker** (lo que no se termina en su ciclo se cancela por defecto). Encajan con devslices de una o dos sesiones y con varios proyectos a la vez. La distinción vibe coding / vibe o agentic engineering ya está asentada: vibe coding solo para prototipos y spikes desechables.

### Cited Findings
**Ryan Singer, *Shape Up* (37signals; libro online, sin fecha en la página consultada)** [V] — [basecamp.com/shapeup, cap. «Bets, Not Backlogs»](https://basecamp.com/shapeup/2.1-chapter-07)
- **Appetite**: tiempo que se está dispuesto a gastar, fijado antes de empezar; no es una estimación; el tiempo es fijo y el alcance se ajusta.
- **Betting table** en el cool-down: se revisan pocas propuestas «shaped» y se elige cuáles financiar; lo no elegido se descarta y puede volver a proponerse.
- Ciclos de 6 semanas sin interrupciones y cool-down de 2 semanas.
- **Circuit breaker**: si no se entrega dentro del ciclo, se cancela por defecto y no se prorroga.
- **Sin backlogs**: los backlogs grandes dan sensación de ir atrasado y consumen tiempo; las ideas importantes vuelven solas.
- Hill charts (subir la colina = descubrir el problema; bajar = ejecutar) [N] — https://basecamp.com/shapeup/3.4-chapter-13 (no consultado en esta sesión).
- *Qué tomar:* un appetite por proyecto o por bloque de devslices (p. ej. «2 sesiones; si no, se replantea»); circuit breaker por proyecto en la revisión de cartera; la colina como estado de cada devslice en el kanban (incógnitas pendientes frente a ejecución). *Conflicto:* «sin backlogs» choca con el kanban como memoria y con el registro de mejora continua; conviene adaptarlo: backlog como **archivo de ideas sin compromiso**, nunca como cola obligatoria. Los ciclos de 6 semanas son de equipo; para una persona sobra el calendario rígido.

**Karpathy, «agentic engineering», febrero de 2026** [S] — [The New Stack](https://thenewstack.io/vibe-coding-is-passe-karpathy-has-a-new-name-for-the-future-of-software/); [Glide, 06-02-2026](https://glideapps.com/blog/what-is-agentic-engineering); [Let's Data Science](https://letsdatascience.com/news/karpathy-explains-vibe-coding-to-agentic-engineering-2d34b5c2)
- Según la prensa, Karpathy da por superado el «vibe coding» de 2025 (que llamó una ocurrencia en un tuit) y propone «agentic engineering»: *agentic* porque casi nunca se escribe el código directamente y se orquestan agentes; *engineering* porque es una disciplina aprendible. En una charla de abril de 2026 habló de competencia «jagged», mejor en dominios verificables. **Sin post primario localizado.**
- Equivalentes ya verificados: Beck (vibe coding frente a augmented coding, 25-06-2025) y Willison (vibe engineering, 07-10-2025), en la sección 1.

**Spikes y prototipos con IA**
- Huntley desaconseja Ralph fuera de greenfield [V] ([ghuntley.com/ralph](https://ghuntley.com/ralph/)); Anthropic sugiere probar algo arriesgado y rebobinar con checkpoints, y saltarse el plan cuando la tarea es exploratoria [V] ([code.claude.com](https://code.claude.com/docs/en/best-practices)). Willison recomienda investigar y probar enfoques antes de que el agente escriba el código definitivo [V] ([simonwillison.net](https://simonwillison.net/2025/Oct/7/vibe-engineering/)).

### Inferences
- Propuesta para la SF: tipificar en el kanban un **«spike»** distinto del devslice. Tiene appetite fijo, se permite el vibe coding, su código es desechable por defecto y produce una conclusión (aprendizaje o decisión), no un incremento. Su informe de cierre responde a una pregunta, no a criterios de aceptación.
- Lean Startup o discovery: no encontré fuentes primarias que lo adapten a la IA con rigor. Lo útil del método (hipótesis → experimento más barato → aprendizaje) se puede aplicar con spikes y prototipos de vibe design antes de la visión detallada.

### Gaps
- Sin fuente primaria sobre Lean Startup o discovery adaptado a agentes; no se buscó a fondo por falta de presupuesto.
- Hill charts sin verificar en esta sesión.

## 3. Personal kanban, límites WIP, cartera de varios productos y práctica deliberada

### Takeaway
No se encontraron, en el presupuesto de esta sesión, fuentes primarias sobre gestión de cartera de indie hackers con agentes. Lo sólido: las dos reglas de Personal Kanban (visualizar y limitar el WIP) [N], el circuit breaker de Shape Up [V] y la paralelización con checkouts aislados de Ronacher y Anthropic [V]. Contra la atrofia hay prácticas concretas (Osmani) y un estudio controlado de Anthropic.

### Cited Findings
- **Personal Kanban (Jim Benson y Tonianne DeMaria Barry, 2011)**: dos reglas, visualizar el trabajo y limitar el trabajo en curso [N] — https://www.personalkanban.com/ (no consultado).
- **Paralelismo**: Ronacher ejecuta varios agentes a la vez en checkouts separados para ganar rendimiento y aísla el estado compartido [V] — [lucumr.pocoo.org](https://lucumr.pocoo.org/2025/6/12/agentic-coding/). Anthropic ofrece worktrees, sesiones con nombre «como ramas» y patrón escritor/revisor [V] — [code.claude.com](https://code.claude.com/docs/en/best-practices). Harper Reed llena las esperas del LLM con otras tareas [V] — [harper.blog](https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/).
- **Addy Osmani, «Avoiding Skill Atrophy in the Age of AI», 25-04-2025** [V] — [addyo.substack.com](https://addyo.substack.com/p/avoiding-skill-atrophy-in-the-age)
  - Prácticas: higiene de IA (verificar y preguntar por qué funciona y dónde falla); **días sin IA** (p. ej. uno por semana); **intentarlo primero**, 15–30 min de depuración propia antes de pedir ayuda; explicar con tus palabras la solución de la IA; **diario de aprendizaje** con las preguntas recurrentes, convertidas luego en ejercicios sin IA; pair programming con la IA llevando tú el control; revisar el código de la IA como el de un colega («AI can draft it, but we own it»); conservar las partes difíciles.
  - Cita un estudio Microsoft–CMU de 2025: más confianza en la IA, menos pensamiento crítico y soluciones menos diversas. El resto son anécdotas.
- **Anthropic Research, «How AI assistance impacts the formation of coding skills», 29-01-2026 (Judy Hanwen Shen y Alex Tamkin)** [S; página primaria no leída] — [anthropic.com/research](https://www.anthropic.com/research/AI-assistance-coding-skills); [InfoQ](https://infoq.com/news/2026/02/ai-coding-skill-formation/); [The Decoder](https://the-decoder.com/ai-coding-tools-hurt-learning-unless-you-ask-why-anthropic-study-finds/)
  - RCT con ~52 ingenieros junior y una librería Python nueva: el grupo con IA obtuvo ~17 % menos en el test de conceptos; la ganancia de velocidad **no fue estadísticamente significativa**; la mayor brecha estuvo en **depuración**. Quienes usaron la IA para preguntas conceptuales o explicaciones puntuaron ≥65 %, y quienes delegaron la generación, <40 %. Limitaciones: tarea de una hora, interfaz de chat, muestra pequeña. Las cifras varían entre medios (51 o 52 participantes).

### Inferences
- Para una persona con muchos proyectos: **WIP = 1 devslice activa por sesión y un máximo pequeño de proyectos «calientes»**. El resto queda «aparcado» con su estado de reanudación (sección 5) y un appetite y circuit breaker por proyecto revisado periódicamente. Es inferencia, no fuente.
- La práctica deliberada se puede meter en la SF como opción por devslice: «modo aprendizaje» (el propietario escribe el núcleo y la IA revisa) o un hueco periódico sin IA, siguiendo a Osmani.

### Gaps
- Sin fuentes primarias verificadas sobre cartera de indie hackers (p. ej. Pieter Levels, Marc Lou, Tony Dinh) ni sobre «portfolio kanban» personal; queda pendiente.
- La página de Personal Kanban no se consultó.

## 4. Enseñar programación en la era de la IA y aprender sin perder comprensión

### Takeaway
La evidencia más sólida (Anthropic, ene-2026; estudio de 2024 con React citado por InfoQ) apunta a lo mismo: **usar la IA para explicar y preguntar no perjudica el aprendizaje; delegar la generación sí, sobre todo en depuración**. Para enseñar: IA como tutor que no da la solución y ejercicios de «intentar primero».

### Cited Findings
- Estudio de Anthropic (detalles en la sección 3) [S] — [anthropic.com/research](https://www.anthropic.com/research/AI-assistance-coding-skills). Según InfoQ, un estudio revisado por pares de 2024 con universitarios que aprendían React encontró que generar código con LLM se correlacionaba negativamente con las notas y que pedir explicaciones no tenía impacto negativo significativo [S] — [InfoQ](https://infoq.com/news/2026/02/ai-coding-skill-formation/).
- Las prácticas de Osmani (intentar primero, explicar con tus palabras, diario de aprendizaje) son directamente trasladables al aula [V] — [addyo.substack.com](https://addyo.substack.com/p/avoiding-skill-atrophy-in-the-age).
- Anthropic usa Claude Code para el onboarding y para explicar código desconocido [V] — [claude.com/blog](https://claude.com/blog/how-anthropic-teams-use-claude-code); la guía oficial recomienda hacer a Claude «las preguntas que harías a un ingeniero sénior» [V] — [code.claude.com](https://code.claude.com/docs/en/best-practices).
- CS50 de Harvard (David Malan): «CS50 Duck», tutor de IA con barreras para que guíe sin dar soluciones, descrito en un artículo SIGCSE 2024 [N] — https://cs50.ai/ (no consultado).
- Claude Code ofrece estilos de salida educativos («Explanatory» y «Learning», que deja huecos para que el humano escriba código) [N] — https://code.claude.com/docs/en/output-styles (no consultado en esta sesión).

### Inferences
- Para los alumnos del propietario: la misma SF con un «perfil docente». Visión y spec escritas por el alumno; la IA solo entrevista y revisa; el núcleo se escribe sin generación; el informe de cierre incluye «explica con tus palabras». Es inferencia que habría que validar en clase.

### Gaps
- No se leyó el artículo primario de Anthropic ni el de CS50; las cifras proceden de prensa.
- Sin fuentes sobre currículos completos rediseñados para la IA.

## 5. Ingeniería de contexto y documentación para retomar proyectos (AGENTS.md, CLAUDE.md, memory banks)

### Takeaway
Para retomar un proyecto se necesitan dos piezas: un archivo de instrucciones **corto y estable** (CLAUDE.md o AGENTS.md: comandos, convenciones y trampas) y un **estado vivo** separado (foco actual, siguientes pasos, qué funciona). Lo segundo es lo que el Memory Bank de Cline formaliza en `activeContext.md` y `progress.md`, y en la SF ya lo ocupan el kanban y los informes de cierre.

### Cited Findings
- **Cline Memory Bank** (documentación sin fecha) [V] — [docs.cline.bot](https://docs.cline.bot/prompting/cline-memory-bank): carpeta `memory-bank/` con `projectbrief.md` (requisitos y objetivos base), `productContext.md` (por qué existe y objetivos de UX), `activeContext.md` (foco actual, cambios recientes y siguientes pasos; el que más cambia), `systemPatterns.md` (arquitectura y patrones), `techContext.md` (stack, setup, restricciones) y `progress.md` (qué funciona, qué falta, problemas conocidos). Comandos: «initialize memory bank», «update memory bank» y, al retomar, «follow your custom instructions». Ante límites de contexto: actualizar, abrir conversación nueva y releer.
- **AGENTS.md** [V] — [agents.md](https://agents.md/): «README para agentes» en Markdown plano, mantenido ahora por la Agentic AI Foundation (Linux Foundation); salió de Codex, Amp, Jules, Cursor y Factory. La página habla de más de 60 000 proyectos. Secciones sugeridas: visión general, build y test, estilo, testing y seguridad. Archivos anidados: gana el más cercano al archivo editado y el prompt del usuario prevalece. Sin fecha en la página.
- **CLAUDE.md según Anthropic** [V] — [code.claude.com](https://code.claude.com/docs/en/best-practices): corto; incluir comandos que Claude no adivina, estilo que difiere del estándar, decisiones de arquitectura y trampas; excluir lo deducible del código, lo que cambia a menudo y las descripciones archivo por archivo. Lo ocasional va a skills y lo obligatorio a hooks. Imports `@path`. Instrucciones de compactación en CLAUDE.md («al compactar, conservar archivos modificados y comandos de test»). Si Claude ignora una regla, probablemente el archivo es demasiado largo.
- **Huntley**: `AGENT.md` breve, que el agente actualiza al aprender cómo construir y ejecutar; specs en un archivo por requisito [V] — [ghuntley.com/ralph](https://ghuntley.com/ralph/). **Reed**: `todo.md` marcado como estado entre sesiones [V] — [harper.blog](https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/).

### Inferences
- Correspondencia con la SF: `projectbrief` y `productContext` ↔ visión y spec funcional; `systemPatterns` y `techContext` ↔ definición técnica y ADR; `activeContext` y `progress` ↔ kanban y último informe de cierre. Lo que falta es un **«punto de reanudación»** breve por proyecto (foco, siguiente devslice, bloqueos y comando para arrancar). Es clave con muchos proyectos aparcados.
- Conflicto: el Memory Bank invita a releer seis archivos en cada sesión, lo que va contra la recomendación de Anthropic de contexto mínimo. Conviene cargarlo bajo demanda (skill o import), no siempre.
- Publicar un AGENTS.md junto al CLAUDE.md, o hacer que uno importe al otro, haría portables los proyectos consumidores a otros agentes. Es una opción, no una necesidad.

### Gaps
- La página de Cline no tiene fecha y no describe el flujo plan/act.
- No se evaluaron empíricamente los memory banks frente al CLAUDE.md mínimo; no se encontraron estudios.
