# Claude Code y los métodos «spec-driven»: qué hacen por el lado humano del trabajo (a 2026-10-26)

Notas de investigación. Consulta: 2026-10-26. Las páginas de code.claude.com/docs no muestran fecha de publicación; donde hay dato, se cita la versión mínima de Claude Code (v2.1.x) que indica la propia página. «No se ha encontrado función documentada» significa que no se ha encontrado en lo consultado, no que no exista.

Alcance: «por repo» = el ámbito es un directorio o repositorio; «multiproyecto» = abarca varios repositorios o proyectos de la misma máquina o cuenta.

## Claude Code como sistema nervioso central: puntos de integración

### Takeaway
Claude Code ofrece hoy suficientes puntos de enganche documentados para que un backend propio (kanban, resumen diario, bandeja de decisiones, informes de cierre) **reciba eventos** (hooks command/http/mcp_tool en ~33 eventos, también a nivel de usuario para todos los proyectos), **inyecte contexto** (SessionStart/UserPromptSubmit `additionalContext`), **empuje mensajes a una sesión abierta** (channels, en research preview), **lance o reanude sesiones** (`claude -p`, `--resume <id>`, Agent SDK, `/fire` de tareas programadas) y **se distribuya como una unidad** (plugins a nivel de usuario). Lo que no aporta es el modelo de datos del estado de varios proyectos ni el criterio de priorización: eso tendría que ponerlo el backend.

### Cited Findings

**Hooks (eventos, datos, capacidades)**
- Hay 33 eventos de hook: SessionStart, Setup, UserPromptSubmit, UserPromptExpansion, PreToolUse, PermissionRequest, PermissionDenied, PostToolUse, PostToolUseFailure, PostToolBatch, Notification, MessageDisplay, SubagentStart, SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, TeammateIdle, InstructionsLoaded, ConfigChange, CwdChanged, DirectoryAdded, FileChanged, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact, PreModelSwitch, PostModelSwitch, Elicitation, ElicitationResult, SessionEnd — [Hooks reference](https://code.claude.com/docs/en/hooks.md)
- Pueden **inyectar contexto** (`hookSpecificOutput.additionalContext`): SessionStart, UserPromptSubmit, UserPromptExpansion, PreToolUse, PostToolUse, PostToolUseFailure, PostToolBatch, SubagentStart, SubagentStop, Stop, PostModelSwitch. Pueden **bloquear**: UserPromptSubmit, PreToolUse, PermissionRequest (vía JSON `decision`), PostToolBatch, SubagentStop, TaskCreated, TaskCompleted, Stop (fuerza a continuar), TeammateIdle, ConfigChange, WorktreeCreate/Remove, PreCompact, PreModelSwitch, Elicitation(Result) — [Hooks reference](https://code.claude.com/docs/en/hooks.md)
- Tipos de hook: `command` (stdin JSON), `http` (hace POST del JSON a una URL; la respuesta usa el mismo formato de salida), `mcp_tool` (llama a una herramienta de un servidor MCP configurado), `prompt` (decisión de un modelo en un turno) y `agent` (subagente verificador, experimental) — [Hooks reference](https://code.claude.com/docs/en/hooks.md)
- Campos comunes a todos los eventos: `session_id`, `transcript_path` (puede ir retrasado respecto a la conversación en memoria), `cwd`, `hook_event_name`; según el caso, `permission_mode`, `prompt_id`, `effort`, `agent_id`/`agent_type` — [Hooks reference](https://code.claude.com/docs/en/hooks.md)
- SessionStart recibe `source` = `startup` | `resume` | `clear` | `compact` | `fork`; su `additionalContext` se añade «al inicio de la conversación, antes del primer prompt», y el stdout en texto plano también entra en contexto; la primera respuesta de Claude espera a que acaben los hooks — [Hooks reference](https://code.claude.com/docs/en/hooks.md)
- UserPromptSubmit puede añadir contexto (stdout o `additionalContext`) sin entrada visible en la transcripción, bloquear el prompt (`decision: "block"`) o fijar `sessionTitle`; tiempo de espera por defecto 30 s para `command`, `http` y `mcp_tool`, y si vence se descarta el contexto — [Hooks reference](https://code.claude.com/docs/en/hooks.md)
- Stop recibe `stop_hook_active`, `last_assistant_message` (texto final de Claude; la doc recomienda usarlo en lugar de leer la transcripción), `background_tasks` y `session_crons`; puede devolver `decision: "block"` + `reason` o `additionalContext` para que Claude siga, con un tope de 8 continuaciones consecutivas — [Hooks reference](https://code.claude.com/docs/en/hooks.md)
- TaskCompleted puede impedir que una tarea se marque como completada (exit 2), con el ejemplo oficial de ejecutar los tests y bloquear si fallan — [Hooks reference](https://code.claude.com/docs/en/hooks.md)
- PreCompact recibe `trigger` (`manual`/`auto`) y `custom_instructions`; PostCompact recibe `trigger` y `compact_summary` (el resumen generado por la compactación). SessionEnd recibe `reason` (p. ej. `prompt_input_exit`, `other`) — [Hooks reference](https://code.claude.com/docs/en/hooks.md)
- Notification recibe `message`, `title`, `notification_type`; tipos: `permission_prompt` (aprobación esperando ~6 s), `idle_prompt` (Claude terminó hace ~60 s y no has escrito), `agent_needs_input` y `agent_completed` (sesiones en segundo plano, solo con agent view abierto), `elicitation_*`, `auth_success`, `quota_auto_resume_*` (v2.1.234+), `plugin_notification`. No puede bloquear ni modificar la notificación — [Hooks reference](https://code.claude.com/docs/en/hooks.md)
- Hooks asíncronos: `"async": true` corre en segundo plano sin bloquear; `"asyncRewake": true` despierta a Claude si sale con código 2 — [Hooks reference](https://code.claude.com/docs/en/hooks.md)
- Ámbitos de configuración: `~/.claude/settings.json` (todos tus proyectos), `.claude/settings.json` (un proyecto, versionable), `.claude/settings.local.json` (un proyecto, ignorado por git), políticas gestionadas, `hooks/hooks.json` de un plugin, frontmatter de skill o de subagente; los niveles **se combinan**, no se sustituyen — [Hooks reference](https://code.claude.com/docs/en/hooks.md)

**MCP y canales de entrada**
- MCP con ámbitos local (por defecto, solo el proyecto actual, en `~/.claude.json`), project (`.mcp.json` versionado) y user (todos tus proyectos); transportes HTTP (recomendado para remoto), stdio, WebSocket (para servidores que empujan eventos sin que se les pida) y SSE (obsoleto) — [MCP](https://code.claude.com/docs/en/mcp.md)
- MCP tasks (beta pública, v2.1.304+): trabajos largos que corre el propio servidor; las llamadas que pasan de dos minutos se mueven a segundo plano y una tarea en un servidor remoto sigue tras salir de Claude Code — [MCP](https://code.claude.com/docs/en/mcp.md)
- **Channels** (research preview): un servidor MCP que declara la capacidad `claude/channel` «empuja eventos a tu sesión de Claude Code en marcha»; pueden ser bidireccionales; solo llegan con la sesión abierta y si se activa con `--channels`; incluidos Telegram, Discord, iMessage y una demo local (fakechat); hay ejemplo oficial de receptor de webhooks; con lista blanca de remitentes; pueden reenviar peticiones de permiso («permission relay») para aprobar a distancia — [Channels](https://code.claude.com/docs/en/channels.md), [Channels reference](https://code.claude.com/docs/en/channels-reference.md)
- Durante la preview, `--channels` solo acepta plugins de una lista blanca de Anthropic; los propios se prueban con `--dangerously-load-development-channels` — [Channels](https://code.claude.com/docs/en/channels.md)
- Mensajería entre sesiones: Claude puede listar tus otras sesiones de Claude Code y enviarles mensajes, en esta máquina, en otra o en la nube — [Run agents in parallel](https://code.claude.com/docs/en/agents.md), [Cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging.md)

**Uso programático (lanzar y reanudar sesiones)**
- `claude -p` con `--output-format text|json|stream-json`; `json` incluye resultado, `session_id`, uso y `total_cost_usd`; `--json-schema` devuelve `structured_output` validado — [Headless](https://code.claude.com/docs/en/headless.md)
- Reanudación programática: capturar `session_id` y `claude -p "..." --resume "$session_id"`, desde cualquier directorio (búsqueda por ID en todos los proyectos de la máquina) — [Headless](https://code.claude.com/docs/en/headless.md), [Sessions](https://code.claude.com/docs/en/sessions.md)
- Ejemplo oficial de «preguntar a una sesión existente»: `claude -p --resume <id> --output-format json "summarize what we changed" | jq -r '.result'` — [Sessions](https://code.claude.com/docs/en/sessions.md)
- `--permission-prompts none` (v2.1.259+) para ejecuciones desatendidas: lo que pediría permiso se deniega y se informa en `permission_denials`; `--bare` omite hooks, skills, CLAUDE.md, auto memory y MCP para resultados reproducibles — [Headless](https://code.claude.com/docs/en/headless.md)
- Agent SDK (Python/TypeScript) con las mismas herramientas y bucle — [Headless](https://code.claude.com/docs/en/headless.md)
- Transcripciones en `~/.claude/projects/<proyecto>/<session-id>.jsonl`, retención por defecto 30 días (`cleanupPeriodDays`); el formato interno cambia entre versiones y la doc desaconseja analizarlo directamente — [Sessions](https://code.claude.com/docs/en/sessions.md)

**Programación y trabajo en segundo plano**
- Tareas programadas en la nube (antes «routines», research preview): prompt + repos + conectores; disparadores por calendario (mínimo cada hora), por API (POST a `/fire` con token, devuelve `claude_code_session_id` y URL) o por eventos de GitHub; planes Pro, Max, Team, Enterprise; corren aunque el portátil esté cerrado; la sesión arranca en auto mode — [Scheduled tasks](https://code.claude.com/docs/en/routines.md)
- El estado «Succeeded» de una ejecución dice cómo acabó la sesión, «no si Claude completó el trabajo»: hay que leer la transcripción — [Scheduled tasks](https://code.claude.com/docs/en/routines.md)
- Los conectores de una tarea en la nube son los de claude.ai; los MCP locales añadidos con `claude mcp add` no aparecen — [Scheduled tasks](https://code.claude.com/docs/en/routines.md)
- Además existen tareas programadas locales en Desktop y `/loop` dentro de una sesión — [Scheduled tasks](https://code.claude.com/docs/en/routines.md), [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks.md)

**Status line, plugins, memoria**
- Status line: script que recibe por stdin JSON con `session_id`, `session_name`, `cwd`, `workspace`, `transcript_path`, `cost` (incl. `total_duration_ms`), `context_window.used_percentage`, `rate_limits`, `worktree`; actualización por eventos con debounce de 300 ms y `refreshInterval` opcional — [Status line](https://code.claude.com/docs/en/statusline.md)
- Plugins: empaquetan skills, agentes, hooks, módulo de hooks («mod», que puede dibujar paneles y añadir comandos) y servidores MCP; ámbito user (todos los proyectos de la máquina), project o local; las sesiones en la nube no cargan los plugins locales — [Plugins](https://code.claude.com/docs/en/plugins.md)
- `~/.claude/rules/` aplica a todos los proyectos de la máquina; `.claude/rules/` admite enlaces simbólicos para compartir reglas entre proyectos — [Memory](https://code.claude.com/docs/en/memory.md)

**Ejemplos de terceros (no oficiales, no validados)**
- claude-code-kanban (NikiforovAll, MIT) instala hooks para seguimiento de subagentes e indicadores de actividad; claude-code-hub del mismo autor añade panel de costes y explorador de memoria, con hooks que añaden datos a ficheros JSONL — [claude-code-kanban](https://github.com/NikiforovAll/claude-code-kanban), [claude-code-hub](https://nikiforovall.blog/productivity/ai/2026/04/08/claude-code-hub.html)
- atc-claude-kanban (.NET) muestra una línea de tiempo con duración de tareas — [NuGet atc-claude-kanban](https://www.nuget.org/packages/atc-claude-kanban)

### Inferences
- Mapa integración → fricción (propuesta, no validada):
  - F1 recuperar contexto: SessionStart (`source=startup|resume|compact`) + `additionalContext` puede inyectar el estado del proyecto desde el kanban; PostCompact `compact_summary` y Stop `last_assistant_message` / SessionEnd pueden alimentar el informe de cierre y el kanban.
  - F2 dirección estratégica: SessionStart/UserPromptSubmit pueden recordar la visión o la devslice activa; un hook `prompt`/`agent` en Stop o TaskCompleted podría comparar el trabajo con la devslice (detección de deriva hecha por la SF, no por Claude Code).
  - F3 atención: Notification (`permission_prompt`, `idle_prompt`, `agent_needs_input`, `agent_completed`) con hook `http` → bandeja de decisiones única; channels/Remote Control para responder desde el móvil.
  - F4 delegación con evidencia: TaskCompleted/Stop bloqueantes con tests; `--json-schema` para informes de cierre estructurados; `/goal` para condiciones verificables.
  - F5 frentes abiertos: los hooks de usuario (`~/.claude/settings.json`) ven todas las sesiones de todos los proyectos de la máquina con `session_id` + `cwd`, lo que permite que el backend cuente frentes abiertos y aplique un límite propio (p. ej., PreToolUse/UserPromptSubmit que bloquee o avise).
  - F6 carga cognitiva: resumen diario multiproyecto vía tarea programada (nube) o tarea Desktop/`claude -p` local leyendo el kanban.
- Un hook de usuario o un plugin a nivel de usuario es la vía natural de «una SF, muchos proyectos», porque se aplica a todos los repos sin tocar cada uno.

### Gaps
- No se ha leído la sección de configuración del hook `http` (campos `url`, `headers`, `allowedEnvVars`, tiempo de espera, comportamiento ante error): la página es muy larga y la extracción no la cubrió.
- No se han verificado los recursos MCP (menciones @) ni los prompts MCP como comandos: la parte leída de la página MCP no los incluía.
- Límites de observación: las sesiones interactivas en otros terminales no aparecen en agent view hasta pasarlas a segundo plano ([Agent view](https://code.claude.com/docs/en/agent-view.md)); `transcript_path` puede ir retrasado; los hooks de Notification de agentes en segundo plano solo saltan con agent view abierto; las sesiones en la nube (tareas programadas, Projects) no cargan `.claude/settings.json`, skills ni `.mcp.json` del repo en los threads de Projects ([Projects](https://code.claude.com/docs/en/claude-projects.md)), así que los hooks locales no las observan. No se ha encontrado un evento que exponga el tiempo de atención humana o el cambio de proyecto del usuario.
- Fechas exactas de lanzamiento de hooks http, channels o agent view: las páginas no las dan; no se consultó el CHANGELOG.

## 1. Recuperar contexto tras una pausa o entre proyectos

### Takeaway
Claude Code recupera bien la **conversación** (resume/continue, nombres, selector con vista de todos los proyectos, resumen de una línea por sesión en agent view, memoria automática por repo). Lo que recupera es la sesión técnica, no «en qué punto está el proyecto y qué decidí»; para eso hay que escribir memoria o CLAUDE.md. Spec Kit, Kiro y Agent OS guardan el contexto en ficheros por repo.

### Cited Findings
- Una sesión es «una conversación guardada ligada a un directorio de proyecto»; `claude --continue` reabre la más reciente del directorio, `--resume` abre el selector, `--resume <nombre>`, `--from-pr <n>` — [Sessions](https://code.claude.com/docs/en/sessions.md)
- El selector muestra por defecto el worktree actual; `Ctrl+W` amplía a todos los worktrees y `Ctrl+A` a «todos los proyectos de esta máquina»; cada fila muestra nombre o título generado, resumen, tiempo desde la última actividad, rama y tamaño — [Sessions](https://code.claude.com/docs/en/sessions.md) (multiproyecto, local)
- Al seleccionar una sesión de otro proyecto, Claude Code copia al portapapeles un `cd` + comando de reanudación — [Sessions](https://code.claude.com/docs/en/sessions.md)
- Las sesiones sin nombre reciben un título generado por un modelo tipo Haiku a partir del primer prompt; aceptar un plan sustituye el título por uno basado en el plan — [Sessions](https://code.claude.com/docs/en/sessions.md)
- Diálogo «Resume this conversation?» tras una pausa larga: estima la parte del límite de 5 h que consumiría reanudar y ofrece empezar de nuevo — [Sessions](https://code.claude.com/docs/en/sessions.md)
- Lo que restaura un resume: historial (desde el último resumen de compactación), modelo, agente, modo de permisos (según la vía), objetivo `/goal` activo, tareas programadas de sesión no caducadas; el trabajo en segundo plano interrumpido aparece como nota — [Sessions](https://code.claude.com/docs/en/sessions.md)
- CLAUDE.md (lo escribe el usuario; ámbitos proyecto, usuario u organización) y auto memory (la escribe Claude; «por repositorio, compartida entre worktrees»; se cargan las primeras 200 líneas o 25 KB) — [Memory](https://code.claude.com/docs/en/memory.md) (auto memory: por repo)
- Ambos sistemas se tratan como contexto, no como configuración obligatoria: «para bloquear una acción… usa un hook PreToolUse» — [Memory](https://code.claude.com/docs/en/memory.md)
- Agent view (research preview, `claude agents`): una pantalla con todas las sesiones en segundo plano «de todos tus proyectos», con estado (working, needs input, idle, completed, failed) y resumen de una línea generado por un modelo tipo Haiku «sin abrir la transcripción»; `Ctrl+S` agrupa por directorio — [Agent view](https://code.claude.com/docs/en/agent-view.md) (multiproyecto, solo sesiones en segundo plano)
- Projects (beta pública, Pro y Max, despliegue gradual): una conversación continua donde Claude abre hilos en la nube; memoria de proyecto (`MEMORY.md` + ficheros) e instrucciones de hasta 16.000 caracteres; «no gestionas ventanas de contexto»; se le puede pedir «Give me a status update on every thread» — [Projects](https://code.claude.com/docs/en/claude-projects.md) (un project puede abarcar varios repos de **una** línea de trabajo)
- Kiro: steering `product.md`, `tech.md`, `structure.md` incluidos en cada interacción; ámbito de workspace (`.kiro/steering/`) y global (`~/.kiro/steering/`) — [Kiro Steering](https://kiro.dev/docs/steering/) (actualizada 2026-10-21)
- Spec Kit: la constitución se crea «una vez por proyecto»; el README no trata el alcance multiproyecto — [GitHub Spec Kit](https://github.com/github/spec-kit)

### Inferences
- Ninguna de las herramientas revisadas ofrece una vista documentada del tipo «estado de mis N productos y qué toca ahora en cada uno»; lo más cercano son agent view (sesiones, no proyectos) y Projects (una línea de trabajo, en la nube).
- La memoria automática de Claude Code guarda aprendizajes técnicos por repo; no hay un esquema documentado de «decisiones pendientes» o «siguiente paso».

### Gaps
- No se ha encontrado documentación de un resumen tipo «mientras estabas fuera» al volver a una sesión interactiva, más allá del título y resumen del selector y de agent view.

## 2. Mantener la dirección estratégica (visión por encima de la tarea; detectar deriva)

### Takeaway
Los marcos SDD ponen un documento por encima de la tarea (constitución, steering, misión), pero por repo y con poca detección de deriva documentada. Claude Code ofrece CLAUDE.md/reglas, plan mode y `/goal`, que dirigen la sesión, no la cartera de proyectos.

### Cited Findings
- Spec Kit: `/speckit-constitution` (principios del proyecto), `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement`, `/speckit-converge` (repetir implement/converge hasta «Converged»); menciona clarify, checklist y análisis de consistencia sin detallar cómo se detecta la deriva; discusión de Spec Kit 1.0 fechada el 16-10-2026 — [GitHub Spec Kit](https://github.com/github/spec-kit)
- Kiro: steering global gana ante conflicto el de workspace; modos de inclusión `always`, `fileMatch`, `manual`, `auto` — [Kiro Steering](https://kiro.dev/docs/steering/)
- Agent OS v3: estándares de código inyectados en contexto, planificación de producto y «shape spec» en plan mode alineado con la misión y los estándares — [Agent OS](https://buildermethods.com/agent-os)
- BMAD v6 (última versión etiquetada citada v6.8.0, hacia mayo de 2026): ecosistema de módulos, planificación «scale-adaptive» en tres pistas (Quick Flow, BMAD Method, Enterprise) — [rywalker.com](https://rywalker.com/research/bmad-method); otra fuente describe niveles 0–4 — [bmad-method README (fork)](https://github.com/macelik/bmad-method). Las taxonomías no coinciden y son fuentes secundarias.
- Claude Code: los límites que dices («no hagas push») cuentan para el clasificador de auto mode, pero «viven en la conversación… la compactación puede eliminarlos»; para garantía, regla de denegación — [Permission modes](https://code.claude.com/docs/en/permission-modes.md)
- `/goal`: condición de finalización evaluada por un modelo rápido tras cada turno; el evaluador «no ejecuta comandos ni lee ficheros», juzga solo lo que aparece en la conversación — [Goal](https://code.claude.com/docs/en/goal.md)
- Böckeler: los agentes a menudo ignoraban instrucciones de la spec o las aplicaban en exceso («falsa sensación de control») — [Martin Fowler, 15-10-2025](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)

### Inferences
- La «dirección» documentada es de producto único (constitución/steering por repo); ninguna herramienta revisada documenta priorizar entre varios productos ni detectar que el trabajo se desvía de una visión.

### Gaps
- Tessl: solo se dispone de la descripción de Böckeler (beta privada en 2025, spec-as-source); no se verificó su estado en 2026.

## 3. Gestión de la atención: notificaciones, menos aprobaciones, decisiones agrupadas

### Takeaway
Es la fricción mejor cubierta por Claude Code: modos de permiso con auto mode, notificaciones (terminal, desktop, push al móvil), agent view con «needs input», Projects con «Waiting on you». No se ha encontrado una bandeja única de decisiones entre proyectos con agrupación por lotes.

### Cited Findings
- Modos: Manual, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`; auto mode usa un clasificador que bloquea lo que «escala más allá de tu petición»; vuelve a preguntar tras 3 bloqueos seguidos o 20 en total; «reduce las peticiones de permiso pero no garantiza seguridad»; desde v2.1.283 auto es el modo inicial en terminal y VS Code — [Permission modes](https://code.claude.com/docs/en/permission-modes.md)
- Agent view: grupos Needs input / Ready for review arriba; contador en el título de la pestaña («2 awaiting input»); notificación por el canal de terminal cuando una sesión local en segundo plano necesita input, termina o falla (solo con agent view abierto) — [Agent view](https://code.claude.com/docs/en/agent-view.md)
- Push al móvil con Remote Control: «Claude decide cuándo»; típicamente al terminar una tarea larga o cuando necesita una decisión; dos interruptores (`Push when Claude decides`, `Push when actions required`) y «no hay configuración por evento»; se omiten mientras escribes en el terminal; `CLAUDE_CLIENT_PRESENCE_FILE` las suprime mientras estás en la máquina — [Remote Control](https://code.claude.com/docs/en/remote-control.md)
- Projects: notificación de escritorio cuando un hilo da error o necesita input; pestaña «Waiting on you» — [Projects](https://code.claude.com/docs/en/claude-projects.md)
- Skill `/fewer-permission-prompts` y reglas `permissions.ask` para mantener puntos de control humanos concretos en auto mode — [Permission modes](https://code.claude.com/docs/en/permission-modes.md)
- Superpowers: puntos de control humanos en aprobación del diseño, «go» para implementar y elección final de cómo cerrar la rama; luego el agente trabaja «un par de horas» sin desviarse — [obra/superpowers](https://github.com/obra/superpowers)

### Inferences
- Las notificaciones son por sesión; un backend puede agregarlas con el hook Notification para construir la bandeja de decisiones multiproyecto, pero eso no viene hecho.

### Gaps
- No se ha encontrado documentación de agrupar decisiones en lotes o de franjas horarias de interrupción, salvo la supresión de push por presencia.

## 4. Delegar con evidencia: verificación, tests, informes, niveles de autonomía

### Takeaway
Superpowers es el marco que más insiste en evidencia (TDD obligatorio, revisión en dos fases, «evidence over claims»). Claude Code aporta mecanismos (hooks bloqueantes, `/goal`, salida JSON con esquema, checkpoints), pero el informe de cierre y el criterio de «hecho» los define el usuario.

### Cited Findings
- Superpowers: `writing-plans` en tareas de 2–5 min con rutas exactas y pasos de verificación; `subagent-driven-development` con un subagente nuevo por tarea y revisión en dos fases (cumplimiento de la spec y calidad); TDD que borra el código escrito antes del test; `verification-before-completion`; filosofía «Evidence over claims», «Verify before declaring success» — [obra/superpowers](https://github.com/obra/superpowers) (sin fecha de versión visible)
- Claude Code: hook TaskCompleted que corre tests y bloquea la tarea si fallan (ejemplo oficial) — [Hooks reference](https://code.claude.com/docs/en/hooks.md)
- `/goal`: «la finalización la decide un modelo nuevo y no el que hace el trabajo»; muestra veredicto y motivo por turno; la doc pide escribir la condición como algo que la salida de Claude pueda demostrar — [Goal](https://code.claude.com/docs/en/goal.md)
- Tareas programadas: «Succeeded» no implica que el trabajo esté hecho; hay que leer la transcripción — [Scheduled tasks](https://code.claude.com/docs/en/routines.md)
- Projects sugiere instrucciones del tipo «antes de dar por hecho el trabajo, ejecuta `make test` y `make lint` y pega las líneas de resumen» — [Projects](https://code.claude.com/docs/en/claude-projects.md)
- Dynamic workflows: script que lanza muchos subagentes y contrasta sus resultados entre sí — [Run agents in parallel](https://code.claude.com/docs/en/agents.md)
- Böckeler, citando a GitHub: «tu papel no es solo dirigir. Es verificar»; y sobre Spec Kit: ficheros «muy verbosos y tediosos de revisar… prefiero revisar código» — [Martin Fowler, 15-10-2025](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)

### Inferences
- La verificación documentada va dirigida al código (tests, revisión); no se ha encontrado un formato estándar de «informe de cierre para la persona» en ninguna herramienta.

### Gaps
- Superpowers no describe el formato de la evidencia que entrega.

## 5. Trabajo en paralelo y límite de frentes abiertos

### Takeaway
Claude Code multiplica la capacidad de abrir frentes (agent view, worktrees, subagentes, agent teams, Projects, workflows, `/batch`). No se ha encontrado ninguna función documentada que **limite** los frentes abiertos por motivos humanos; los límites documentados son de cuota/coste.

### Cited Findings
- Cinco formas de trabajo paralelo: subagentes, agent view, agent teams (experimental, desactivado por defecto), Projects y dynamic workflows; más worktrees, mensajería entre sesiones y `/batch` (5–30 subagentes en worktrees) — [Run agents in parallel](https://code.claude.com/docs/en/agents.md)
- «Ejecutar varias sesiones o subagentes a la vez multiplica el uso de tokens» — [Run agents in parallel](https://code.claude.com/docs/en/agents.md); cada sesión de agent view «usa tu cuota de forma independiente» — [Agent view](https://code.claude.com/docs/en/agent-view.md)
- En Projects puedes decir a Claude un límite de hilos, pero se guarda como preferencia en memoria: «no es un tope estricto» — [Projects](https://code.claude.com/docs/en/claude-projects.md)
- Límites horarios de tareas programadas (100 ejecuciones/h por cuenta, etc.) — [Scheduled tasks](https://code.claude.com/docs/en/routines.md)
- Superpowers usa `using-git-worktrees` para aislar cada trabajo — [obra/superpowers](https://github.com/obra/superpowers); Spec Kit crea una rama por spec — [Martin Fowler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)

### Inferences
- La tendencia del producto es facilitar más paralelismo; el límite de frentes como regla de método (WIP) tendría que ponerlo la SF.

### Gaps
- No se leyó la sección «Limitations» de agent view (la extracción la cortó).

## 6. Bienestar, foco y carga cognitiva

### Takeaway
No se ha encontrado ninguna función documentada en Claude Code ni en los marcos SDD revisados orientada explícitamente al bienestar o a la carga cognitiva de la persona. Lo más cercano son efectos secundarios: menos peticiones de permiso, resúmenes de sesión, supresión de push por presencia, y la crítica de que SDD **aumenta** la carga de revisión.

### Cited Findings
- Auto mode se presenta para «reducir la fatiga de peticiones» (prompt fatigue) — [Permission modes](https://code.claude.com/docs/en/permission-modes.md)
- Supresión de push mientras estás en la máquina (`CLAUDE_CLIENT_PRESENCE_FILE`) y aviso de que Focus de iOS puede retrasarlas — [Remote Control](https://code.claude.com/docs/en/remote-control.md)
- Böckeler: Kiro convirtió un bug pequeño en varias historias con muchos criterios; Spec Kit «más pesado» que la programación asistida normal para una funcionalidad media; prefiere «pasos pequeños e iterativos» para mantener el control — [Martin Fowler, 15-10-2025](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- Críticas «SDD = waterfall»: specs por funcionalidad escritas antes de aprender algo son «big design upfront»; se defienden specs por porción («slice») escritas justo antes del código — [Maulik Kataria (LinkedIn)](https://no.linkedin.com/in/maulikk); riesgo de convertir analistas en revisores de Markdown — [feedbagel](https://feedbagel.com/post/critique-of-spec-driven-development-balancing-structure-and-agility-in-ai-progra); réplica: con agentes el ciclo de feedback baja a minutos — [Allstacks](https://www.allstacks.com/blog/spec-driven-development-isnt-waterfall-why-the-ai-coding-bottleneck-changed-everything). Son opiniones de blog/LinkedIn, no estudios.

### Inferences
- La hipótesis del propietario («las herramientas se centran en el producto final más que en las fricciones de la persona») se sostiene **parcialmente**: Claude Code sí trabaja activamente la atención (notificaciones, permisos, agent view, Projects «Waiting on you») y la recuperación de sesión; donde no se ha encontrado nada documentado es en cartera multiproyecto, límite de frentes, priorización estratégica entre productos y bienestar. Los marcos SDD se centran en calidad del artefacto y pueden añadir carga de revisión.
- Matiz honesto para la SF: varias piezas que la SF diseña (bandeja de decisiones, resumen) se pueden apoyar directamente en hooks, agent view y Projects; la diferencia de la SF tendría que estar en el modelo multiproyecto y las reglas de método, no en la mecánica.

### Gaps
- No se buscaron estudios empíricos (p. ej., de Anthropic o académicos) sobre carga cognitiva con agentes; quedan fuera de esta nota.
