# Herramientas de gestión y orquestación de agentes de código: qué hacen por el lado humano (a 2026-10-26)

Notas de investigación. Fuentes consultadas entre las disponibles el 2026-10-26. Muchas páginas de documentación no muestran fecha; se indica «sin fecha» cuando es así. Cuando una función no aparece en lo consultado se escribe «no se encontró función documentada», que no equivale a afirmar que no exista.

Ámbito de cada herramienta (multiproyecto / por repo; local / nube), resumen previo:

| Herramienta | Ámbito | Ejecución |
|---|---|---|
| Vibe Kanban (BloopAI) | Multiproyecto (selector de proyectos; workspaces multi-repo) | Local, con proyectos en la nube opcionales |
| Conductor (Melty Labs) | Workspace por tarea; el soporte multi-repo no aparece en lo consultado | App de Mac local; anuncia «Conductor Cloud» |
| Claude Squad | Una terminal TUI; multi-repo no mencionado | Local (tmux + worktrees) |
| GitHub Copilot coding agent / Agent HQ | Panel de agentes «across your repositories»; cada tarea limitada a un repo | Nube (GitHub Actions) |
| OpenAI Codex (app, cloud) | Proyectos y chats en paralelo | Local + nube |
| Cursor Agents Window | «across all your projects from one place» | Local, worktrees, VMs en la nube, SSH |
| Devin | Sesiones en la nube; Knowledge a nivel organización | Nube |
| Google Jules | Tareas por repo (hay página «Managing tasks and repos») | Nube |
| Factory (Droids) | Sesiones; Missions de varios agentes | Local/remoto |
| Linear (agentes) | Espacio de trabajo de Linear (issues, proyectos) | Plataforma de gestión; los agentes son de terceros |

## 1. Recuperar el contexto tras una pausa o entre proyectos

### Takeaway
Las herramientas guardan historial técnico (logs de sesión, chats, diffs) y algunas ofrecen memoria del repositorio o consultas en lenguaje natural sobre sesiones pasadas. No se encontró ninguna que genere un resumen orientado a la persona del estilo «dónde lo dejaste y qué decisiones te esperan» a través de varios proyectos; la unidad de recuperación es la sesión o el repositorio.

### Cited Findings
- GitHub Copilot: el panel de agentes, accesible desde cualquier página de GitHub, permite «monitor and manage agent sessions across your repositories»; cada sesión muestra log, progreso, uso de tokens y duración; se puede preguntar en lenguaje natural por sesiones pasadas en Copilot Chat (sin fecha) — [GitHub Docs: manage agents](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/manage-agents)
- GitHub Copilot Memory construye «a longer-term, persistent understanding of your repositories and preferences across sessions»; Copilot Chat puede responder sobre PR creadas por Copilot usando los logs de sesión (sin fecha) — [GitHub Docs: about coding agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- Mission control de Agent HQ (anunciado el 2025-10-28): «a single command center to assign, steer, and track the work of multiple agents from anywhere», en web, VS Code, móvil y CLI — [GitHub Blog, Introducing Agent HQ](https://github.blog/news-insights/company-news/welcome-home-agents/)
- OpenAI Codex app: «Move between projects and long-running work without losing context» y «Keep every chat in view»; tiene páginas de documentación de «Memories» y «Long-running work» (sin fecha; no se leyeron en detalle) — [Codex app docs](https://learn.chatgpt.com/docs/app)
- La app de Codex se lanzó el 2026-02-02 para macOS; agentes en hilos agrupados por proyecto (fuente secundaria) — [heise](https://heise.de/-11165126); [Interesting Engineering](https://interestingengineering.com/ai-robotics/openai-codex-app-multi-agent-software-development)
- Cursor Agents Window (GA con Cursor 3, 2026-04-02): «work with agents across all your projects from one place»; traspaso de un agente de la nube a local y vuelta — [Cursor Docs: Agents Window](https://cursor.com/docs/agent/agents-window)
- Devin: Knowledge es un almacén de consejos y documentación que Devin recuerda automáticamente en sesiones futuras (actualización de septiembre de 2024) — [Cognition, Sept '24 update](https://cognition.ai/blog/sept-24-product-update); Devin puede analizar sesiones pasadas a partir de su enlace y deduplicar o consolidar entradas de Knowledge — [Devin Docs: advanced capabilities](https://docs.devin.ai/work-with-devin/advanced-capabilities)
- Devin 2.0 incorporó Devin Search (preguntas sobre el código con citas) y Devin Wiki (documentación generada del repositorio) — [Cognition, Devin 2.0](https://cognition.ai/blog/devin-2)
- Factory Droid: las sesiones se reanudan con `droid --resume` o se duplican con `/fork`; hay una Sessions API (fuente secundaria, no verificada con docs.factory.ai) — [innFactory](https://innfactory.ai/en/ai-harness/droid/)
- Claude Squad: «c» hace commit y pausa una sesión; «r» la reanuda — [GitHub smtg-ai/claude-squad](https://github.com/smtg-ai/claude-squad)
- Vibe Kanban: el workspace muestra los logs del agente; la página de inicio no menciona resúmenes ni historial — [Vibe Kanban docs: getting started](https://vibekanban.com/docs/getting-started)
- AGENTS.md (Copilot, Jules) e instrucciones personalizadas evitan volver a dar las mismas indicaciones en cada sesión — [GitHub Blog, Agent HQ](https://github.blog/news-insights/company-news/welcome-home-agents/); [Jules docs](https://jules.google/docs/)

### Inferences
- La «memoria» documentada sirve al agente (conocimiento del repo y preferencias para trabajar mejor), no a que la persona recupere su propio hilo mental. El historial se puede consultar, pero no se encontró ninguna herramienta que lo prepare de forma proactiva para retomar el trabajo.
- Las vistas que cruzan repositorios (panel de agentes de GitHub, Agents Window de Cursor, la app de Codex) se organizan por sesión o por chat, no por proyecto con su estado, objetivos y pendientes.

### Gaps
- No se leyeron las páginas «Memories» y «Projects and chats» de Codex; pueden contener más detalle.
- No se encontró documentación sobre resúmenes automáticos para retomar el trabajo en ninguna herramienta; no se puede afirmar que no existan.

## 2. Mantener la dirección estratégica y la alineación con una visión

### Takeaway
Lo más alto que se encontró por encima de la tarea es: issues padre e hijo y prioridades (Vibe Kanban), proyectos e initiatives como contenedores de Linear, guidance por espacio de trabajo y por equipo (Linear), planes por tarea (plan mode de Copilot y Vibe Kanban, Interactive Planning de Devin, planes de Jules) y «Missions» que descomponen trabajo de horas o días (Factory). No se encontró ninguna función documentada que mantenga una visión de producto y compruebe con ella las tareas o resultados.

### Cited Findings
- Vibe Kanban: las issues tienen prioridades, etiquetas y relaciones padre/hijo; las sub-issues dividen funcionalidades grandes; la configuración del agente incluye un modo plan — [Vibe Kanban docs: getting started](https://vibekanban.com/docs/getting-started)
- Linear: «Workspace guidance» y «team guidance» son instrucciones que los agentes reciben automáticamente al trabajar en issues; «team guidance takes priority». La página no describe que se pase contexto de proyecto o initiative al agente — [Linear Docs: Agents in Linear](https://linear.app/docs/agents-in-linear)
- Plan Mode de Copilot en VS Code «asks you clarifying questions» para construir un plan paso a paso antes de escribir código (2025-10-28) — [GitHub Blog, Agent HQ](https://github.blog/news-insights/company-news/welcome-home-agents/)
- Devin Interactive Planning: una evaluación inicial rápida y después un plan detallado con citas de código, que se puede revisar antes de aprobarlo — [Devin Docs: interactive planning](https://docs.devin.ai/work-with-devin/interactive-planning)
- Jules genera un plan y «You can review and approve it before any code changes are made» — [Jules docs](https://jules.google/docs/)
- Factory 2.0 (junio de 2026): autonomía como espectro; «Missions» resuelven tareas complejas durante horas o días dividiéndolas en pistas paralelas — [Factory: software factory](https://factory.ai/news/software-factory)

### Inferences
- La planificación documentada se queda en la tarea o la funcionalidad (técnica). La alineación estratégica depende de la persona o del gestor de tareas que tenga encima.
- Es notable que Factory llame a su enfoque «software factory», el mismo nombre que este proyecto, aunque con orientación a la ejecución autónoma en empresa.

### Gaps
- No se consultaron las docs de proyectos e initiatives de Linear ni si los agentes reciben su contenido.

## 3. Gestión de la atención: notificaciones, agrupar aprobaciones, bandeja de decisiones pendientes

### Takeaway
Las notificaciones existen y se configuran sobre todo por evento (turno terminado, permiso pedido, pregunta). Codex tiene la vista de actividad más elaborada («unread, running, or waiting for your response»). Han surgido productos pequeños de «bandeja de atención» (attnbox, Agentbox, la Agent Inbox de Dailybot) que solo muestran lo que está bloqueado o terminado. No se encontró en las herramientas principales ninguna función documentada para agrupar aprobaciones ni un modo «no molestar».

### Cited Findings
- Codex: avisos de turno completado configurables («never, only while ChatGPT is in the background, or always»); controles separados para avisos de permiso y de pregunta; la campana de la barra lateral muestra chats «unread, running, or waiting for your response»; un «pet» flotante muestra «Running», «Needs input», «Ready» o «Blocked»; en la web, avisos por push, email o SMS; en la CLI, un programa externo al terminar el turno (`notify`). La página no menciona agrupación ni no molestar — [Codex docs: notifications](https://learn.chatgpt.com/codex/notifications)
- Jules: notificaciones del navegador «when the task completes or needs your input» — [Jules docs](https://jules.google/docs/); las notificaciones nativas en móvil estaban «en exploración» en octubre de 2025 — [TechCrunch, 2025-10-02](https://techcrunch.com/2025/10/02/googles-jules-enters-developers-toolchains-as-ai-coding-agent-competition-heats-up)
- Vibe Kanban: preferencias de notificación (incluido el sonido) al configurarlo y en ajustes — [Vibe Kanban docs: getting started](https://vibekanban.com/docs/getting-started)
- Linear: estados de sesión del agente pending, active, error, awaitingInput y complete, que se fijan automáticamente; las buenas prácticas piden emitir una elicitación o un error cuando hace falta que actúe una persona — [Linear Developers: agents](https://linear.app/developers/agents); en la vista «My issues» siguen las issues delegadas — [Linear Docs](https://linear.app/docs/agents-in-linear)
- GitHub: steering con mensajes de seguimiento que se aplican «after it finishes its current tool call»; las páginas consultadas no describen notificaciones — [GitHub Docs: manage agents](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/manage-agents)
- Conductor y Claude Squad: no se encontraron notificaciones documentadas en las páginas consultadas — [Conductor docs: parallel agents](https://www.conductor.build/docs/concepts/parallel-agents); [Claude Squad](https://github.com/smtg-ai/claude-squad)
- attnbox (código abierto): reúne sesiones de Claude Code, Codex CLI y agentes en la nube en una «Unified attention inbox», con estados esperando, trabajando, inactivo o terminado y avisos opcionales cuando un agente empieza a esperar — [GitHub wookat/attnbox](https://github.com/wookat/attnbox)
- Agentbox: una fila vuelve al usuario solo cuando su agente termina o se atasca — [EveryDev: Agentbox](https://www.everydev.ai/tools/agentbox)
- Dailybot Agent Inbox: llegan elementos solo cuando el agente necesita una decisión, un acceso, una aclaración o una aprobación, «not when everything is proceeding normally» — [Dailybot help: Agent Inbox](https://v3.dailybot.com/help/using-dailybot/agent-inbox/overview)

### Inferences
- El patrón dominante es el estado por sesión más aviso por evento. Filtrar para avisar solo cuando algo está bloqueado o terminado aparece como producto independiente, lo que sugiere un hueco en las herramientas principales. No se encontró ninguna que priorice las decisiones pendientes por importancia o por proyecto ni que las agrupe en franjas.

### Gaps
- No se verificó si Cursor, Devin o Conductor tienen configuración de notificaciones en otras páginas de su documentación.

## 4. Delegar con evidencias: revisión, diffs, pruebas, informes de verificación, niveles de autonomía

### Takeaway
Es el área mejor cubierta: visores de diff con comentarios en línea, previsualización en navegador, checks y CI, revisión automática previa, logs de sesión, niveles de autonomía y políticas de gobierno. Las evidencias se presentan como artefactos técnicos (diff, PR, log, checks), no como un informe de verificación contra criterios de aceptación.

### Cited Findings
- Vibe Kanban: panel de cambios con diffs resaltados y comentarios en línea para devolver feedback al agente; previsualización del sitio en el navegador; scripts de preparación y limpieza; merge por PR o en local — [Vibe Kanban docs: getting started](https://vibekanban.com/docs/getting-started)
- Conductor: visor de diff, checks, revisión de una rama por varios agentes antes de abrir la PR, archivo del workspace tras el merge — [Conductor docs](https://www.conductor.build/docs/); [parallel agents](https://www.conductor.build/docs/concepts/parallel-agents)
- GitHub Agent HQ: «branch controls» para decidir cuándo ejecutar CI y checks sobre código de agentes; revisión de primera línea antes de que mire una persona; un plano de control como «agent governance layer» con políticas, auditoría y acceso (2025-10-28) — [GitHub Blog](https://github.blog/news-insights/company-news/welcome-home-agents/)
- Copilot coding agent: un repositorio, una rama y una PR por tarea; límite fijo de 59 minutos por sesión; los logs «don't replace your own review and testing» — [GitHub Docs: about coding agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- Codex: páginas de Permissions, Sandboxing y «Agent approvals & security» (no leídas en detalle) — [Codex app docs](https://learn.chatgpt.com/docs/app)
- Cursor: «New diffs view» para revisar, hacer commit y gestionar PR; `/autopilot` para una PR — [Cursor Docs: Agents Window](https://cursor.com/docs/agent/agents-window)
- Jules: al terminar presenta plan, razonamiento y diff para revisar y aprobar antes del merge — [InfoQ, agosto de 2025](https://www.infoq.com/news/2025/08/google-jules)
- Devin: las citas del plan enlazan con su IDE para comprobar los hallazgos antes de aprobar — [Devin Docs: interactive planning](https://docs.devin.ai/work-with-devin/interactive-planning)
- Factory Droid: nivel de autonomía Off/Low/Medium/High según el riesgo, una lista de bloqueo de comandos destructivos y comprobaciones de sandbox independientes (fuente secundaria) — [innFactory](https://innfactory.ai/en/ai-harness/droid/)
- Claude Squad: modo experimental `-y` de aceptación automática («yolo»); revisión del diff y checkout antes de hacer push — [Claude Squad](https://github.com/smtg-ai/claude-squad)
- Linear: la delegación no sustituye al responsable; la issue conserva una persona asignada que responde del resultado y el agente queda como «delegate» — [Linear blog: Agent Interaction SDK](https://linear.app/now/our-approach-to-building-the-agent-interaction-sdk); [Linear Developers](https://linear.app/developers/agents)

### Inferences
- La revisión está pensada para leer código. No se encontró un formato estándar de «informe de evidencias» (qué criterio se comprobó, cómo y con qué resultado) dirigido a una persona que no quiere leer cada diff.
- El modelo de responsabilidad de Linear (la persona responde del resultado y el agente es su delegado) es el que más se acerca a una delegación con rendición de cuentas.

### Gaps
- No se consultaron las páginas de checks de Conductor ni de permisos de Codex.

## 5. Trabajo en paralelo: worktrees, muchos agentes, límites de WIP, vistas entre proyectos

### Takeaway
Todas las herramientas resuelven el aislamiento técnico (worktrees, VMs, contenedores) y el lanzamiento de muchos agentes a la vez. Los únicos límites que se encontraron son de cuota o de plan, no de WIP pensados para la persona; no se encontró ninguna función documentada que recomiende o imponga un límite de trabajo en curso para proteger su atención.

### Cited Findings
- Vibe Kanban: al crear un workspace se generan worktrees de los repositorios elegidos; se pueden asociar varios workspaces a una issue — [Vibe Kanban docs](https://vibekanban.com/docs/getting-started)
- Conductor: cada workspace tiene «a separate branch and working tree»; recomienda un workspace por issue de GitHub o Linear; la página no describe máximos ni límites de concurrencia — [Conductor docs: parallel agents](https://www.conductor.build/docs/concepts/parallel-agents)
- Claude Squad: tmux para cada sesión y worktrees para aislar el código — [Claude Squad](https://github.com/smtg-ai/claude-squad)
- Cursor: muchos agentes en la nube, que se pueden seguir desde el móvil, la web, Slack, GitHub o Linear; worktrees aislados — [Cursor Docs: Agents Window](https://cursor.com/docs/agent/agents-window)
- Codex: worktrees de Git y entornos en la nube en paralelo — [Codex app docs](https://learn.chatgpt.com/docs/app)
- Jules (plan gratuito): hasta 15 tareas diarias y 3 simultáneas, un límite de uso y no de bienestar — [Gigazine, 2025-08-07](https://gigazine.net/gsc_news/en/20250807-ai-coding-agent-jules-public)
- Linear: Insights y vistas segmentadas por «Delegate» muestran la implicación y la carga de los agentes — [Linear Docs](https://linear.app/docs/agents-in-linear)
- Claude Code «agent teams» (experimental, desactivado por defecto): una sesión hace de líder del equipo — [Claude Code docs: agent teams](https://code.claude.com/docs/en/agent-teams)

### Inferences
- Lo que miden las vistas de carga (Linear Insights, panel de GitHub, métricas de Copilot) es el trabajo de los agentes, no la capacidad de revisión de la persona, que es el cuello de botella real.

### Gaps
- No se pudo verificar el estado a octubre de 2026 de Sculptor (Imbue), Crystal/Nimbalyst (Stravu) ni Terragon: la búsqueda no dio resultados relevantes.

## 6. Bienestar: estrés, concentración, limitar la carga

### Takeaway
No se encontró en ninguna de las herramientas cubiertas una función documentada dirigida explícitamente al estrés, la concentración o el límite de carga de la persona. Lo más cercano son controles de notificación (Codex), bandejas que filtran por bloqueo (attnbox, Agentbox, Dailybot) y el discurso de «no perder el contexto» (Codex).

### Cited Findings
- Los controles de Codex permiten silenciar los avisos de turno completado o mostrarlos solo con la app en segundo plano; no se documenta un modo no molestar — [Codex docs: notifications](https://learn.chatgpt.com/codex/notifications)
- Las bandejas de atención se presentan como medio para que solo vuelva a la persona lo que la necesita — [attnbox](https://github.com/wookat/attnbox); [Dailybot Agent Inbox](https://v3.dailybot.com/help/using-dailybot/agent-inbox/overview)
- La búsqueda sobre «agent inbox» y carga cognitiva o burnout no encontró fuentes que evalúen si estas herramientas la reducen — búsqueda propia del 2026-10-26, sin resultado citable.
- Los paneles de métricas que se anuncian miden el impacto y el uso de Copilot en la organización, no la carga de la persona — [GitHub Blog, Agent HQ](https://github.blog/news-insights/company-news/welcome-home-agents/)

### Inferences
- La hipótesis del propietario («las herramientas actuales se centran en el producto, no en las fricciones de la persona») se sostiene en gran medida para la recuperación del contexto, la dirección estratégica y el bienestar. No se sostiene del todo para la atención y la delegación: Codex, Linear y las bandejas de atención sí atacan explícitamente las interrupciones y la responsabilidad humana. Conviene reconocerlo en el documento de visión para no ser benévolos con el propio proyecto.
- Casi todas las herramientas están pensadas para equipos o empresas (gobierno, auditoría, métricas de organización). El caso de una sola persona con muchos proyectos queda cubierto solo de forma indirecta.

### Gaps
- Falta evidencia empírica (estudios o encuestas) sobre la carga de supervisar agentes en paralelo; corresponde a otra línea de investigación.
- La fecha de muchas páginas de documentación no es visible; las funciones pueden haber cambiado.
