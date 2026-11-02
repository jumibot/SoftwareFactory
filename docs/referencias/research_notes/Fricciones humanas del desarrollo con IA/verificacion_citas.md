# Verificación de citas y datos del informe «Fricciones humanas del desarrollo con IA»

Comprobación hecha el 26-10-2026 contra las fuentes primarias. Cubre la tabla «Citas y datos que conviene volver a verificar antes de usarlos» del informe y los puntos que se pidió revisar con más cuidado. El informe no se ha modificado.

Estados:

- **VERIFICADO**: la cita o la cifra aparece en la fuente primaria abierta directamente. Las citas se copian en su idioma original.
- **CORREGIDO**: la fuente primaria dice algo distinto de lo que recoge el informe, o le añade un matiz que cambia el uso.
- **NO VERIFICABLE**: no se pudo abrir la fuente primaria (muro de pago, bloqueo 403, página inexistente) o no existe. Se indica si solo hay fuentes secundarias.

No se han saltado muros de pago ni bloqueos antibots. Los textos de Medium, Axios, Bloomberg y el cuerpo de HBR quedan sin verificar por ese motivo.

---

## 1. Atención e interrupciones (investigación clásica)

### 1.1. «23 minutos para recuperar la concentración» (Gloria Mark)
- **Estado:** VERIFICADO que **no figura** en los artículos. CORREGIDO a favor de la cifra de 2005.
- **Dato exacto:** en los textos completos de CHI 2005 y CHI 2008 no aparece ninguna cifra de 23 minutos. CHI 2005 dice: «When people did resume work on the same day, it took an average length of time of 25 min. 26 sec (sd=54 min. 48 sec.)» y «before resuming work, our informants worked in an average of 2.26 (sd=2.79) working spheres».
- **Fuente:** Mark, González y Harris, «No Task Left Behind? Examining the Nature of Fragmented Work», CHI 2005.
- **URL:** https://www.interruptions.net/literature/Mark-CHI05-p321-mark.pdf
- **Fecha:** 2005.
- **Nota:** el post de UC Irvine de 2017 que atribuiría los 23 minutos a Fast Company devuelve 404 (https://www.informatics.uci.edu/2017/01), así que esa atribución concreta es NO VERIFICABLE. Las páginas de UCI y de las editoriales sobre el libro *Attention Span* (2023) hablan de «up to 25 minutes». El resto de cifras de CHI 2005 también se verificaron: 24 informantes; «11 min. 4 sec., (sd=18 min. 9 sec.)» por esfera; «57.1% of all informants' working sphere segments were interrupted».

### 1.2. Mark, Gudith y Klocke (2008): interrupciones cada 2 minutos
- **Estado:** VERIFICADO, con un matiz.
- **Cita exacta:** «Interruption frequency was set to two minutes»; «After only 20 minutes of interrupted performance people reported significantly higher stress, frustration, workload, effort, and pressure»; «people completed interrupted tasks in less time with no difference in quality».
- **Fuente:** Mark, Gudith y Klocke, «The Cost of Interrupted Work: More Speed and Stress», CHI 2008.
- **URL:** https://www.interruptions.net/literature/Mark-CHI08.pdf
- **Fecha:** 2008.
- **Nota:** en la tabla 3, el estrés pasa de 6,92 (sin interrupción) a 9,46 y la frustración de 4,73 a 6,63 en la condición de **interrupción del mismo contexto**. Con interrupción de contexto distinto, los valores son 9,13 y 6,48. Conviene citar la condición.

### 1.3. Parnin y Rugaber (2010): reanudar la programación
- **Estado:** VERIFICADO.
- **Cita exacta:** «we perform exploratory analysis on 10,000 recorded programming sessions of 85 programmers»; «In 10% of the sessions, edit lag was less than a minute»; «In about 30% of sessions, the edit lag is over 30 minutes. In these sessions, we believe the developers may be engaged in debugging activities».
- **Fuente:** Parnin y Rugaber, ICPC 2010.
- **URL:** https://sites.cc.gatech.edu/reverse/repository/resumptionstrategies.pdf
- **Nota:** son 10.000 sesiones de **85 programadores**. Los propios autores reconocen que parte de la espera es depuración.

### 1.4. Bainbridge (1983), «Ironies of Automation»
- **Estado:** VERIFICADO.
- **Cita exacta:** «it is impossible for even a highly motivated human being to maintain effective visual attention towards a source of information on which very little happens, for more than about half an hour» y «Unfortunately people can write down numbers without noticing what they are.»
- **Fuente:** Lisanne Bainbridge, *Automatica*, 1983.
- **URL:** https://gwern.net/doc/sociology/technology/1983-bainbridge.pdf
- **Nota:** la primera frase se apoya en Mackworth (1950).

### 1.5. Leroy (2009), residuo atencional
- **Estado:** VERIFICADO (resumen completo).
- **Cita exacta (resumen):** «As revealed by two experiments, people need to stop thinking about one task in order to fully transition their attention and perform well on another. Yet, results indicate it is difficult for people to transition their attention away from an unfinished task and their subsequent task performance suffers. Being able to finish one task before switching to another is, however, not enough to enable effective task transitions. Time pressure while finishing a prior task is needed to disengage from the first task and thus move to the next task and it contributes to higher performance on the next task.»
- **Fuente:** Sophie Leroy, «Why is it so hard to do my work? The challenge of attention residue when switching between work tasks», *Organizational Behavior and Human Decision Processes* 109(2):168-181.
- **URL:** https://ideas.repec.org/a/eee/jobhdp/v109y2009i2p168-181.html (DOI: https://doi.org/10.1016/j.obhdp.2009.04.002)
- **Fecha:** julio de 2009.
- **Nota:** son dos experimentos. El resumen no da la N; la cifra de 162 personas solo aparece en fuentes secundarias. No hay que confundir este trabajo con Leroy y Glomb (2018), donde la presión temporal *anticipada* produce el efecto contrario.

### 1.6. Meyer et al., la agencia en un buen día de trabajo
- **Estado:** VERIFICADO (resumen).
- **Cita exacta:** «One key finding is the importance of agency, developers' control over their workday and whether it goes as planned or is disrupted by external factors.»
- **Fuente:** Meyer, Barr, Bird y Zimmermann, «Today was a Good Day: The Daily Life of Software Developers», IEEE TSE.
- **URL:** https://www.microsoft.com/en-us/research/?p=578803
- **Fecha:** abril de 2019.

---

## 2. Testimonios de figuras conocidas

### 2.1. Simon Willison en Lenny's Podcast
- **Estado:** VERIFICADO, con un matiz de contexto importante.
- **Citas exactas** (del post de Willison con los momentos destacados, transcritos por él mismo):
  - [26:25] «I'm finding that using coding agents well is taking every inch of my 25 years of experience as a software engineer, and it is mentally exhausting. I can fire up four agents in parallel and have them work on four different problems. And by like 11 AM, I am wiped out for the day.»
  - [26:25, tras una elipsis «[...]»] «I've talked to a lot of people who are losing sleep [...] That's obviously unsustainable. [...] There's an element of sort of gambling and addiction to how we're using some of these tools.»
  - [45:16] «My programming work, I need two minutes every now and then to prompt my agent about what to do next. And then I can do the other stuff and I can go back. I'm much more interruptible than I used to be.»
  - [36:56] «And they almost feel a sort of sense of loss at the end where they're like, well, okay, my backlog's gone. Now what am I going to build?»
  - [37:47] «I've got some very cool software that I built that I've never used.»
- **Fuente:** Simon Willison (cocreador de Django, blogger independiente), «Highlights from my conversation about agentic engineering on Lenny's Podcast».
- **URL:** https://simonwillison.net/2026/Apr/2/lennys-podcast/
- **Fecha:** 02-04-2026.
- **Nota:** «I'm much more interruptible» va bajo el epígrafe **«Interruptions cost a lot less now»** y tiene sentido **positivo**: ya no necesita bloques de dos a cuatro horas. No debe citarse como queja. Las citas de agotamiento sí están bajo «This stuff is exhausting». Hay además una corrección a las notas (`testimonios.md`): la frase «every evening I'm like, let's take that project and finish it» la pone Willison en boca de sus amigos, no habla de sí mismo.

### 2.2. Willison y Tim Dettmers en Axios («pop that stack»)
- **Estado:** NO VERIFICABLE.
- **Dato:** «There is a limit on human cognition, in how much you can hold in your head at one time» y «pop that stack» (Willison); Dettmers sostendría que la productividad máxima con agentes exige cambiar de contexto casi constantemente.
- **Fuente:** Axios, 04-04-2026.
- **URL:** https://www.axios.com/2026/04/04/ai-agents-burnout-addiction-claude-code-openclaw
- **Nota:** Axios devuelve 403 a las herramientas automáticas. El post de Dettmers «Use Agents or Be Left Behind?» (https://timdettmers.com/2026/01/13/use-agents-or-be-left-behind/, 13-01-2026) no contiene esa idea: dice que la paralelización es sobre todo propia de la ingeniería de software. No hay fuente primaria accesible para estas citas.

### 2.3. Mitchell Hashimoto: «If I'm coding, I want an agent planning»
- **Estado:** VERIFICADO.
- **Cita exacta:** «If I'm coding, I want an agent planning. If they're coding, I want to be reviewing.» y «the best engineers are the ones that context-switch the least.»
- **Fuente:** Gergely Orosz, «Mitchell Hashimoto's new way of writing code», The Pragmatic Engineer. Hashimoto es cofundador de HashiCorp y creador de Ghostty.
- **URL:** https://newsletter.pragmaticengineer.com/i/188952833/key-observation-from-mitchell
- **Fecha:** 25-02-2026.
- **Nota:** en esa página no se mencionan las notificaciones (véase 2.4).

### 2.4. Hashimoto apaga las notificaciones del agente
- **Estado:** CORREGIDO. Hay fuente primaria: su propio blog.
- **Cita exacta:** «Very important at this stage: turn off agent desktop notifications. Context switching is very expensive. In order to remain efficient, I found that it was my job as a human to be in control of when I interrupt the agent, not the other way around. Don't let the agent notify you. During natural breaks in your work, tab over and check on it, then carry on.»
- **Fuente:** Mitchell Hashimoto, «My AI Adoption Journey», paso «Outsource the Slam Dunks».
- **URL:** https://mitchellh.com/writing/my-ai-adoption-journey
- **Fecha:** 05-02-2026.
- **Nota:** en ese paso Hashimoto ejecuta los agentes «one at a time, not in parallel» mientras él trabaja en otra cosa. Es otro dato a favor de limitar los frentes.

### 2.5. Steve Yegge, «The AI Vampire», y las horas al día
- **Estado:** NO VERIFICABLE en el original. La cita de Yegge reproducida literalmente por Willison sí está verificada; la cifra de horas está CORREGIDA.
- **Cita exacta (de Yegge, reproducida por Willison):** «I find that I am only really comfortable working at that pace for short bursts of a few hours once or occasionally twice a day, even with lots of practice.» Y también «And you're exhausted. You're tired, Boss. You got nothing for it. Congrats, you were just drained by a company.»
- **Paráfrasis de Willison:** «Steve reports needing more sleep due to the cognitive burden involved in agentic engineering, and notes that four hours of agent work a day is a more realistic pace».
- **Fuente:** Simon Willison, post de enlace «The AI Vampire»; el original es de Steve Yegge en Medium.
- **URL:** https://simonwillison.net/2026/Feb/15/the-ai-vampire/ (original: https://steve-yegge.medium.com/the-ai-vampire-eda6e4f07163, que devuelve 403)
- **Fecha:** 15-02-2026 el post de Willison; el original es de febrero de 2026.
- **Nota:** la cifra de «cuatro horas» es de Willison, no una cita de Yegge. Lo único literal de Yegge es «short bursts of a few hours once or occasionally twice a day». Las tres horas de Business Insider (enlace AOL con 404; solo se ve en dev.ua) y las cuatro o cinco de O'Reilly son secundarias. Lo prudente es escribir «unas pocas horas, una o dos veces al día (Yegge)».

### 2.6. Armin Ronacher, «The Tower Keeps Rising»
- **Estado:** VERIFICADO.
- **Cita exacta:** «But with agents I can ask an agent to add OAuth, you can ask one to add caching, and somebody else can ask one to rebuild the database from first principles and make the UI pink. Each change can be reasonable in isolation but since it's frictionless, none of us necessarily has to talk to the others or familiarize ourselves with the code we are changing. The more we use agents, the less we feel the pain as agents feel none of it, and a useful signal is gone.» También: «large software projects have never been limited only by how quickly an individual can produce code but they are limited by how well people can coordinate their understanding of the system they are changing.»
- **Fuente:** Armin Ronacher (creador de Flask), blog personal.
- **URL:** https://lucumr.pocoo.org/2026/7/13/the-tower-keeps-rising/
- **Fecha:** 13-07-2026.
- **Nota:** el resumen secundario era fiel. El ensayo habla de equipos, no de una persona sola.

### 2.7. Bloomberg, «Claude Code and the Great Productivity Panic of 2026»
- **Estado:** NO VERIFICABLE el cuerpo (muro de pago). Título y fecha VERIFICADOS.
- **Dato:** el título exacto lo da el envío a HN, que enlaza a https://www.bloomberg.com/news/articles/2026-02-26/ai-coding-agents-like-claude-code-are-fueling-a-productivity-panic-in-tech.
- **Fecha:** 26-02-2026.
- **Nota:** Bloomberg Law lo publica como «Claude Code Is Causing the Great Productivity Panic of 2026». La autoría (probablemente Issie Lapowsky) no está confirmada. No hay que citar contenido del artículo.

### 2.8. Comentarios de Hacker News (hilo 47467922)
- **Estado:** VERIFICADO.
- **Citas exactas:**
  - scuff3d: «My brain feels like a fractured mess.»
  - bbangjo: «So true in my case, the speed of ai-assisted coding removeds the natrual pause where your brain used to process what it just wrote.» (sic)
  - npilk (21-03-2026): «Yes, spending time working with Claude Code leaves me feeling the same way I feel after a day scrolling Reddit and HN - a thin, jittery, frayed sort of weariness. It's almost like gambling, with inconsistent dopamine hits, but it adds an element of keeping track of an ever-increasing number of projects and to-dos.»
  - iainctduncan: «Alomst makes me want to just teach music lessons again for way less money.» (sic)
  - bayareapsycho: «I don't really feel this kind of friction.»
  - pbjhsu: «I work on a social platform and the frontier we're hitting isn't productivity, it's trust.»
- **URL:** https://news.ycombinator.com/item?id=47467922
- **Fecha:** el hilo es de marzo de 2026 (el comentario de npilk se fechó el 21-03-2026 a través de la API de Algolia). El artículo de Bloomberg es del 26-02-2026.
- **Nota:** son comentarios anónimos. Sirven como ilustración, no como evidencia.

---

## 3. Citas literales de blogs

### 3.1. Constantin Gonzalez
- **Estado:** VERIFICADO.
- **Citas exactas:** «I've started calling it agent hopping»; «peeking at a still-working agent is a paid interruption with zero yield, and agent notifications that interrupt you rebuild the bad kind of task switching with extra steps»; «Every dish that's still cooking with an agent somewhere keeps simmering in your head, too.»; «It felt great: three streams of steady progress, one me.»
- **URL:** https://constantin.glez.de/posts/2026-07-16-why-working-with-ai-agents-is-so-tiring-and-what-to-do-about-it/
- **Fecha:** 16-07-2026 (según la URL).
- **Nota:** propone un límite útil para la SF: «Cap your burners. One big dish, at most two small ones on the side. My personal Kanban board enforces this limit».

### 3.2. Wolfgang Wagner
- **Estado:** VERIFICADO; la fecha está CORREGIDA.
- **Citas exactas:** «Even when I'm writing an email, the question lingers in the background: Is it done yet? Did it work?»; «I was exhausted, and my head felt full. More tired than I used to be on days when I did everything by hand.»
- **URL:** https://wwagner.net/en/blog/a/more-time-thanks-to-ai-but-still-exhausted-a-personal-experiment
- **Fecha:** **08-10-2026** (`datePublished` de la página), no el 10-08-2026 que da el informe.

### 3.3. Eva Keiffenheim
- **Estado:** VERIFICADO.
- **Citas exactas:** «The greatest risk of automation is losing your mental model of the project (what researchers call situation awareness).»; «Every time you context-switch between agents, your brain leaves behind "attention residue," making the next task harder.»; «Every workday felt exhausting. I wasn't recovering overnight.»
- **URL:** https://evakeiffenheim.substack.com/p/the-cognitive-costs-of-multi-clauding
- **Fecha:** 13-05-2026.
- **Nota:** la cita de Boris Cherny («I feel like now is the age of multi-clauding.») está reproducida por Keiffenheim, que la oyó en un podcast; no se verificó en el original.

### 3.4. Siva (SivaLabs)
- **Estado:** VERIFICADO.
- **Citas exactas:** «I hadn't actually reviewed the AI-generated code. I had only checked whether it looked reasonable. Those are not the same thing.»; «I can deeply focus on maybe two things before my brain starts filing formal complaints.»
- **URL:** https://www.sivalabs.in/blog/ai-agents-are-doing-the-heavy-lifting/
- **Fecha:** 30-06-2026.

### 3.5. Addy Osmani, «Comprehension debt», y su afiliación
- **Estado:** VERIFICADO.
- **Citas exactas:** «comprehension debt breeds false confidence. The codebase looks clean. The tests are green.»; «Engineers approved code they didn't fully understand, which now carries implicit endorsement.»; «a junior engineer can now generate code faster than a senior engineer can critically audit it.»
- **Biografía en la página:** «Addy Osmani is an engineering and evangelism leader and a Member of Technical Staff at Anthropic, where he works on Claude Code. He spent over 14 years at Google…»
- **URL:** https://addyosmani.com/blog/comprehension-debt/
- **Fecha:** publicado el 14-03-2026 (`article:published_time`); la página tiene otra fecha del 14-09-2026, que puede ser una actualización.
- **Nota:** sigue sin saberse en qué empresa estaba al publicar el ensayo. Lo seguro es escribir «ex-Google, actualmente en Anthropic según su web».

### 3.6. Bunny Honey Club (fundador con cuatro negocios)
- **Estado:** VERIFICADO, con correcciones de atribución.
- **Cita exacta:** «Before Claude Code we ran each business in blocks — Monday was Shopify, Tuesday was agency work, and so on. It felt efficient and was not. The context tax of switching from a Shopify PDP bug to a cold-outreach sequence was enormous»; «Four businesses is a real ceiling for this pattern. The bottleneck is founder memory, not model capacity.»
- **Fuente:** Arthur Hof, «Founder, Bunny Honey Club AI», «Claude Code for solo founders running multiple businesses».
- **URL:** https://blog.bunnyhoneyclub.com/posts/claude-code-for-solo-founders-running-multiple-businesses
- **Fecha:** 02-12-2025.
- **Nota:** el «mayor de lo esperado» del informe no es literal; el texto dice «enormous» y se refiere al horario por bloques *anterior* a Claude Code. Es un post comercial de un estudio de IA que vende ese servicio. La frase «founder memory, not model capacity» es muy pertinente para la SF.

### 3.7. Indie Hackers («ended up not getting anywhere»)
- **Estado:** NO VERIFICABLE (403).
- **URL:** https://www.indiehackers.com/post/how-many-projects-are-you-currently-working-on-e7f67780cd

---

## 4. Productividad y delegación

### 4.1. METR 2025: 19 % más lentos
- **Estado:** VERIFICADO.
- **Cita exacta:** «When developers are allowed to use AI tools, they take 19% longer to complete issues» y «developers expected AI to speed them up by 24%, and even after experiencing the slowdown, they still believed AI had sped them up by 20%.» Participaron 16 desarrolladores y se resolvieron 246 issues.
- **Fuente:** METR, «Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity».
- **URL:** https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
- **Fecha:** 10-07-2025.

### 4.2. METR 2026: ¿revierte el 19 %?
- **Estado:** VERIFICADO que no lo revierte. Hay un matiz que el informe no recoge.
- **Cita exacta:** «we believe it is likely a bad proxy for the real productivity impact of AI tools on these developers»; «our measurements of time-spent on each task are unreliable for the fraction of developers who use multiple AI agents concurrently»; «30% to 50% of developers told us that they were choosing not to submit some tasks because they did not want to do them without AI»; «we now estimate a speedup of -18% with a confidence interval between -38% and +9%. Among newly-recruited developers the estimated speedup is -4%, with a confidence interval between -15% and +9%». Se recogieron datos de 57 desarrolladores, 143 repositorios y más de 800 tareas.
- **Fuente:** METR, actualización del estudio.
- **URL:** https://metr.org/blog/2026-02-24-uplift-update/
- **Fecha:** 24-02-2026.
- **Nota:** METR también escribe «we believe it is likely that developers are more sped up from AI tools now» y que su estimación es «likely [...] a lower-bound on the true productivity effects». Lo correcto es decir que METR cree probable que ahora haya aceleración, pero que sus datos son «only very weak evidence for the size of this increase». No hay que presentarlo ni como reversión ni como ausencia de aceleración.

### 4.3. Encuesta de METR de 2026 (n=349)
- **Estado:** VERIFICADO. Ahora hay página primaria.
- **Cita exacta:** «In February–April 2026, we ran a survey of 349 technical workers (including 87 software engineers, 71 researchers, 129 academics and PhD students, and 48 founders and managers)»; «A survey of 349 technical workers finds a median 1.4–2x self-reported change in value of work due to AI tools [...] though there are reasons to be skeptical of the magnitude»; «Importantly, survey results are not necessarily grounded in reality.»
- **Fuente:** Joel Becker (METR), «Measuring the Self-Reported Impact of Early-2026 AI on Technical Worker Productivity».
- **URL:** https://metr.org/blog/2026-05-11-ai-usage-survey/
- **Fecha:** 11-05-2026.
- **Nota:** METR recuerda que en 2025 la gente sobrestimó el efecto en 40 puntos porcentuales.

### 4.4. NBER w35275 (commits +240 %, proyectos +80 %, releases +30 %)
- **Estado:** VERIFICADO.
- **Cita exacta (resumen):** «using data on more than 500,000 GitHub developers combined with their AI usage telemetry. In a matched event study design, we find that autocomplete, interactive coding agents, and autonomous coding agents each significantly increase coding activity ("commits"), with respective cumulative effects of 30%, 180%, and 240%. These gains, however, attenuate sharply across the production hierarchy: the 240% cumulative effect falls to 80% for the number of projects, and to 30% for actual releases. This pattern is consistent with the weak-link hypothesis [...] with an estimated elasticity of substitution of 0.23 between AI and human effort [...] finding a sharp increase in the number of new apps but no increase in total usage. Large task-level AI productivity gains have therefore translated only partially into shipped and used software thus far.»
- **Fuente:** Mert Demirer, Leon Musolff y Liyuan Yang, «Writing Code vs. Shipping Code: Productivity Effects Across Generations of AI Coding Tools», NBER Working Paper 35275.
- **URL:** https://www.nber.org/papers/w35275
- **Fecha:** mayo de 2026, revisado en septiembre de 2026.
- **Nota:** según la propia página, Demirer y Musolff son consultores remunerados de Microsoft. Es un working paper sin revisión por pares formal.

### 4.5. Faros AI, «The Acceleration Whiplash» (segundo trimestre de 2026)
- **Estado:** VERIFICADO.
- **Dato exacto:** «Two years of telemetry from 22K developers across 4K teams»; «epics completed (+66.2%)»; «deployments per week (-11.7%)»; «5X Median Review Time»; «+242.7% incidents per PR»; «+57.9% monthly incidents»; «code churn (+861%)».
- **Fuente:** Faros AI, AI Engineering Report Q2 2026.
- **URL:** https://www.faros.ai/research/ai-acceleration-whiplash
- **Nota:** es un informe de proveedor y los datos son correlacionales. El «+441 %» de algunos resúmenes no aparece en la página.

### 4.6. Faros AI, «The Speed Trap» (tercer trimestre de 2026)
- **Estado:** VERIFICADO.
- **Dato exacto:** «time in QA is up 300.6%»; «restarts are up 66.7%, nearly five times the increase we saw previously»; PR fusionadas sin revisión: el aumento señalado seis meses antes era del 31,3 % y «That figure has increased to 76.3%»; muestra de «22,000 developers across 4,000 teams», últimos 12 meses.
- **Fuente:** Faros Research.
- **URL:** https://www.faros.ai/blog/ai-speed-trap-takeaways
- **Fecha:** 18-09-2026.
- **Nota:** el 76,3 % es un incremento, no la proporción de PR fusionadas sin revisión.

### 4.7. Faros 2025 (+98 % de PR, +91 % de revisión, +154 % de tamaño)
- **Estado:** NO VERIFICABLE.
- **URL:** https://www.faros.ai/research/ai-productivity-paradox
- **Nota:** la página actual no muestra esas cifras en el HTML accesible. Hay que usar los informes de 2026.

### 4.8. Ensayo de Anthropic sobre comprensión (17 %)
- **Estado:** VERIFICADO, con matices.
- **Cita exacta:** «participants in the AI group scored 17% lower than those who coded by hand, or the equivalent of nearly two letter grades»; «the AI group averaged 50% on the quiz, compared to 67% in the hand-coding group [...] (Cohen's d =0.738, p =0.01)»; «On average, participants in the AI group finished about two minutes faster, although the difference was not statistically significant»; «The largest gap in scores between the two groups was on debugging questions». Participaron «52 (mostly junior) software engineers».
- **Fuente:** Anthropic, «How AI assistance impacts the formation of coding skills». Dirigieron el estudio Judy Hanwen Shen y Alex Tamkin (Anthropic Safety Fellows Program); el artículo es arXiv 2601.20245.
- **URL:** https://www.anthropic.com/research/AI-assistance-coding-skills
- **Fecha:** 29-01-2026.
- **Nota:** se usó un asistente en una barra lateral de chat, no un agente. Anthropic avisa: «this setup is different from agentic coding products like Claude Code; we expect that the impacts of such programs on skill development are likely to be more pronounced». La pérdida es de 17 puntos sobre una nota de 67; el texto la llama «17% lower».

### 4.9. Estudio interno de Anthropic
- **Estado:** VERIFICADO; una cita está CORREGIDA.
- **Citas exactas:**
  - «in August 2025 we surveyed 132 Anthropic engineers and researchers, conducted 53 in-depth qualitative interviews»
  - «more than half said they can "fully delegate" only between 0-20% of their work to Claude»
  - «27% of Claude-assisted work consists of tasks that wouldn't have been done otherwise»
  - «the "paradox of supervision"—as mentioned above, effectively using Claude requires supervision, and supervising Claude requires the very coding skills that may atrophy from AI overuse»
  - «I am for sure atrophying in my skills as a software engineer...»
  - «When producing output is so easy and fast, it gets harder and harder to actually take the time to learn something.»
  - «70%+ to being a code reviewer/reviser rather than a net-new code writer»
  - «Spending your day prompting Claude is not very fun or fulfilling.»
  - «It's the end of an era for me - I've been programming for 25 years»
  - «The more excited I am to do the task, the more likely I am to not use Claude.»
  - «having a million horses… allows you to test a bunch of different ideas»
- **Fuente:** Saffron Huang, Bryan Seethor, Esin Durmus, Kunal Handa, Miles McCain, Michael Stern y Deep Ganguli (Anthropic, Societal Impacts), «How AI Is Transforming Work at Anthropic».
- **URL:** https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic
- **Fecha:** 02-12-2025.
- **Nota:** la cita «I thought that I really enjoyed writing code, and instead I actually just enjoy what I get out of writing code» aparece en dos versiones en la misma página. En la sección de resultados clave dice «…and I think instead I actually just enjoy…». Si se cita, hay que tomar la versión de la entrevista. Los datos son de agosto de 2025, con Claude Sonnet 4 y Opus 4.

### 4.10. Anthropic: el 93 % de los permisos se aceptan
- **Estado:** VERIFICADO el texto; el método no está publicado.
- **Cita exacta:** «Over time that leads to approval fatigue, where people stop paying close attention to what they're approving.» y «Manual prompts sit in the middle, and in practice users accept 93% of them anyway.»
- **Fuente:** Anthropic Engineering, «How we built Claude Code auto mode: a safer way to skip permissions».
- **URL:** https://www.anthropic.com/engineering/claude-code-auto-mode
- **Fecha:** 25-03-2026.
- **Nota:** el post no dice cómo se midió. El 97 % que circula no tiene fuente.

---

## 5. Encuestas

### 5.1. Stack Overflow 2025
- **Estado:** VERIFICADO; una cifra está CORREGIDA.
- **Dato exacto:** «84% of respondents are using or planning to use AI tools in their development process, an increase over last year (76%)»; confianza: «Highly trust 3.1%» (n=33.244; experimentados, 2,5 %); «AI solutions that are almost right, but not quite 66%»; «Debugging AI-generated code is more time-consuming 45.2%».
- **URL:** https://survey.stackoverflow.co/2025/ai
- **Fecha:** 2025.
- **Nota:** el 84 % incluye a quien **planea** usarla. No es correcto escribir «el 84 % usa IA».

### 5.2. Stack Overflow 2026
- **Estado:** VERIFICADO; el 93 % está CORREGIDO.
- **Dato exacto:**
  - Blog: «Over seven weeks, more than 30,000 people took the survey»; «73% of respondents who indicate using AI coding assistants/agents use them daily, and a third of daily users using any AI tools use AI four or more hours per day»; «Many of those AI users live in coding agents (66%) and chatbots (63%) [...] The agents of choice are Claude Code (66%) and GitHub Copilot (59%)».
  - Página de resultados: «4+ hours/day [...] 30.9%» (n=10.926).
- **Fuente:** Ryan Donovan (Stack Overflow, staff), «The results of the 2026 Developer Survey are here», y página oficial de resultados.
- **URL:** https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/ ; https://survey.stackoverflow.co/2026/ai ; https://survey.stackoverflow.co/2026/
- **Fecha:** 06-10-2026.
- **Nota sobre el 93 % frente al 78,7 %:** es **el mismo ítem**. En la página de resultados, la importancia de la atribución de fuentes se reparte así: «Very important 52.1%», «Important 26.5%» y «Somewhat important 14.0%» (n=13.945). El 78,7 % es «muy importante + importante» y el 93 % suma además «algo importante». Por eso, escribir que el 93 % la «considera necesaria para confiar» exagera. Lo exacto es: «el 93 % la considera al menos algo importante; el 79 %, importante o muy importante». También se verificó: «48% indicate they trust AI when they can easily validate the answers» y «I trust it for many tasks, including important work decisions 6.6%».

### 5.3. BCG/HBR, «AI brain fry»
- **Estado:** NO VERIFICABLE en la fuente primaria (cuerpo de HBR de pago; no hay informe público de BCG). VERIFICADOS la autoría, la fecha y la parte abierta.
- **Lo verificado en HBR:**
  - Título: «When Using AI Leads to "Brain Fry"».
  - Subtítulo: «A new study finds that certain patterns of AI use are driving cognitive fatigue, while others can help reduce burnout.»
  - Fecha: 05-03-2026.
  - Autores: Julie Bedard (Managing Director & Partner, BCG), Matthew Kropp (Managing Director y Senior Partner, Chief AI Officer de BCG X), Megan Hsu (Project Leader, BCG), Olivia T. Karaman y Jason Hawes (doctorandos de UC Riverside y ayudantes de investigación en BCG) y Gabriella Rosen Kellerman (Expert Partner y Director, BCG; psiquiatra).
  - Cita abierta de un usuario de Gas Town: «I had a palpable sense of stress watching it. Gas Town was moving too fast for me.»
- **Cifras, solo en fuente secundaria:** The Decoder (Maximilian Schreiner, 09-03-2026) recoge una encuesta a 1.488 trabajadores a tiempo completo de EE. UU.: «Workers with high oversight demands expended 14 percent more mental effort, reported 12 percent more mental fatigue, and experienced 19 percent greater information overload»; «Going from one to two simultaneous AI tools, perceived productivity rises significantly. At three tools, it peaks. Beyond four, it drops again»; «Fourteen percent of AI-using respondents reported experiencing "AI brain fry."» (26 % en marketing y 6 % en legal); «33 percent more decision fatigue and 39 percent more major errors. Intent to quit rose from 25 to 34 percent.»
- **URL:** https://hbr.org/2026/03/when-using-ai-leads-to-brain-fry ; https://the-decoder.com/study-warns-of-ai-brain-fry-as-workers-hit-cognitive-limits-overseeing-ai-agents/ ; Axios (403): https://www.axios.com/2026/03/06/ai-chatgpt-claude-jobs-brain-fry
- **Nota:** el informe dice «+12 % de fatiga mental y +19 % de sobrecarga» pero omite el «+14 % de esfuerzo mental», que también figura. Las cifras coinciden en The Decoder, Fortune y The Register, aunque todo es secundario. Además, hay dos «14 %» distintos (prevalencia y esfuerzo mental) que no deben confundirse. Si se usan, deben ir como «según la cobertura de prensa del estudio de BCG publicado en HBR». Un resumen sitúa el descenso a partir de la tercera herramienta, no de la cuarta.

---

## 6. Preprints y estudios citados dentro de otros

### 6.1. ParallelPilot (Microsoft Research)
- **Estado:** VERIFICADO; el «desencadenante principal» está CORREGIDO.
- **Cita exacta:** «our data point to a consistent trigger for when they did so: idle time in their workflow—periods when they were waiting for a single agent to complete»; «All 14 participants described a real coordination and monitoring tax.»; «Requests for clarification and errors or bugs required immediate intervention, yet were also the signals participants most reliably missed»; «ParallelPilot increased ticket throughput by 63% in short coding tasks»; esfuerzo de seguimiento de 4,63 frente a 2,75 (p < ,001); «These gains were not accompanied by significant improvements in perceived control or perceived success in redirecting the agents» (control p = ,414; redirección p = ,603; confianza al delegar p = ,108).
- **Fuente:** Tao Long (Microsoft Research AI Frontiers y Columbia), Weili Shi, Hussein Mozannar, Maya Murad y Rafah Hosn (Microsoft Research), «ParallelPilot: Supporting Coordination and Monitoring in Parallel AI Coding», arXiv 2609.33113v1.
- **URL:** https://arxiv.org/html/2609.33113v1
- **Fecha:** 27-09-2026.
- **Nota:** el texto dice «consistent trigger» (desencadenante constante), no «principal». El estudio formativo tiene N=14 y el de usuarios N=16. Es un preprint.

### 6.2. Park et al.
- **Estado:** VERIFICADO.
- **Dato exacto:** 19 participantes, 12.912 comentarios de Reddit y siete etapas (Plan, Monitor, Wait, Review, Teach, Manual Fix, Update Assets); el fragmento «mentally much less taxing to just code it up manually».
- **Fuente:** Yeon Su Park, Nadia Arvi, Hae Ri Lee, Sehoon Lim (KAIST), Qianou Ma (CMU) y Juho Kim (KAIST y SkillBench), «The Work Behind Delegation: A Framework for Supervising AI Coding Agents», arXiv 2609.24234v1.
- **URL:** https://arxiv.org/html/2609.24234v1
- **Fecha:** 21-09-2026.
- **Nota:** la frase completa que rodea el fragmento no se extrajo; conviene citar solo el fragmento.

### 6.3. Ye et al. (el 94 % no detecta el sabotaje)
- **Estado:** VERIFICADO en la fuente primaria.
- **Cita exacta (resumen):** «Over 100 participants collaborate with one of four frontier models [...] on a long-horizon coding task lasting around five hours [...] We find that 83/88 (94%) of developers in the no-monitor conditions fail to detect sabotage [...] while the monitor reduces sabotage success, sabotage still succeeds in 9/16 (56%) of sessions with a correct monitor alert.»
- **Fuente:** Jingheng Ye, Huiqi Zou, Simon Yu y Weiyan Shi, «Coding with "Enemy": Can Human Developers Detect AI Agent Sabotage?», arXiv 2606.05647.
- **URL:** https://arxiv.org/abs/2606.05647
- **Fecha:** v1 del 04-06-2026; v2 del 05-10-2026.
- **Nota:** el 94 % se refiere a las condiciones **sin monitor** (83 de 88).

### 6.4. Kitano et al.
- **Estado:** NO VERIFICABLE por separado. Solo se comprobó la referencia dentro de ParallelPilot: B. Kitano, E. Carlson, B. Russett y A. Kesling, «Managing Multi-Agent Research Systems: A Dashboard for Human Oversight of Coordinating AI Agents», HEAL@CHI'26.
- **Nota:** no se abrió el artículo.

### 6.5. BMAD v6 (pistas o niveles)
- **Estado:** NO VERIFICABLE.
- **Dato:** el README oficial (https://github.com/bmad-code-org/BMAD-METHOD) da como versión estable la **v6.12** (última etiqueta, v6.12.4, del 14-10-2026) y una V7 en alfa. Ni el README ni la lista de documentos de la rama V6.12 mencionan las pistas «Quick Flow / BMAD Method / Enterprise» ni los niveles 0-4.
- **Nota:** la «v6.8.0» de las notas está desactualizada. No conviene describir su taxonomía.

---

## Resumen: qué se puede citar con seguridad

**Seguro, con la fuente primaria y la formulación exacta indicada:**
- **Investigación clásica:** Mark 2005 (25 min 26 s, con su definición), Mark 2008 (indicando la condición), Parnin y Rugaber, Bainbridge, el resumen de Leroy 2009 y Meyer et al.
- **METR:** METR 2025 (19 % más lentos y la brecha 24 % / 20 %), METR 2026 con el matiz de que METR cree probable la aceleración pero con evidencia muy débil, y la encuesta METR 2026 (n=349).
- **Telemetría:** NBER w35275 (+240 % de commits, +80 % de proyectos, +30 % de releases, elasticidad de 0,23) y Faros Q2 y Q3 de 2026, como informes de proveedor.
- **Anthropic:** el ensayo del 17 %, aclarando que no usaba agentes, el estudio interno con sus citas y el 93 % de permisos aceptados, sin método publicado.
- **Encuestas:** Stack Overflow 2025 (con «usa o planea usar») y Stack Overflow 2026 (30,9 % de cuatro horas o más; atribución: el 79 % la considera importante o muy importante).
- **Testimonios:** Willison en Lenny's (con el «more interruptible» en sentido positivo), Hashimoto en Pragmatic Engineer y **en su blog, donde apaga las notificaciones**, Ronacher, Gonzalez, Wagner (08-10-2026), Keiffenheim, Siva, Osmani con su biografía, Bunny Honey Club (Arthur Hof, post comercial) y los comentarios de HN como ilustración.
- **Preprints:** ParallelPilot («consistent trigger»), Park et al. y Ye et al. (83/88 sin monitor).

**Solo como secundario y avisándolo:** las cifras de BCG/HBR (1.488; +14 %, +12 % y +19 %; máximo con tres herramientas) y la cifra de horas de Yegge. De Yegge lo seguro es «short bursts of a few hours once or occasionally twice a day», reproducido por Willison; las «cuatro horas» son paráfrasis de Willison.

**No usar:** los 23 minutos, las citas de Axios (Willison con «pop that stack» y Dettmers), el contenido del artículo de Bloomberg, Faros 2025, Indie Hackers, Kitano et al., la taxonomía de BMAD y el 97 % de permisos.
