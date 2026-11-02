# Skills, plugins y marketplaces de Claude Code reutilizables por la SF (a 2026-10-26)

Convenciones de estas notas:

- **[V]**, verificado: metadatos leídos directamente de la API de GitHub o del fichero del repositorio el 2026-10-26 (estrellas, licencia SPDX, fecha del último *push* o del último commit en la ruta, descripción literal).
- **[S]**, secundario: procede de resultados de búsqueda, de agregadores o de la descripción de una lista curada, sin abrir el repositorio.
- «Última actividad» es `pushed_at` del repositorio salvo que se indique «commit en ruta», que es el último commit que toca esa carpeta.
- Todo es **candidato**. Nada se ha instalado ni probado. Las estrellas miden popularidad, no calidad.
- «Licencia: ninguna» significa que GitHub no detecta licencia; legalmente no concede derechos de reutilización.

## 1. Skills y marketplace oficiales de Anthropic

### Takeaway
Anthropic mantiene dos fuentes oficiales: `anthropics/skills` (19 skills, licencias mixtas) y `anthropics/claude-plugins-official` (315 entradas en el `marketplace.json`, de las que unas 40 son plugins internos de Anthropic y el resto de partners o comunidad). Para la SF lo más reutilizable es skill-creator, mcp-builder y mcp-server-dev (para el MCP de JKanban), frontend-design, playground, learning/explanatory-output-style (enseñar y aprender), session-report, receipts y project-artifact (informes y cierre), claude-md-management y hookify (automejora) y feature-dev, code-review y pr-review-toolkit (desarrollo).

### Cited Findings

**Repositorio `anthropics/skills`** [V] — https://github.com/anthropics/skills · Anthropic (organización) · 183 842 estrellas · último push 2026-10-09 · licencia de repositorio no detectada por GitHub (mixta): la mayoría de las skills son Apache 2.0; las document skills (`docx`, `pdf`, `pptx`, `xlsx`) son *source-available*, no open source — [repo](https://github.com/anthropics/skills)
- Se instala como marketplace con `/plugin marketplace add anthropics/skills` y los plugins `document-skills` y `example-skills` — [repo](https://github.com/anthropics/skills)
- Skills actuales [V]: academy-guide, algorithmic-art, brand-guidelines, canvas-design, claude-api, discernment-nudge, doc-coauthoring, docx, frontend-design, internal-comms, mcp-builder, pdf, pptx, skill-creator, slack-gif-creator, theme-factory, web-artifacts-builder, webapp-testing, xlsx — [carpeta skills](https://github.com/anthropics/skills/tree/main/skills)
- `skill-creator` [V]: crear, modificar y mejorar skills, ejecutar evals, medir rendimiento con análisis de varianza y optimizar la descripción para que se active bien. Commit en ruta 2026-04-20 — [SKILL.md](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
- `mcp-builder` [V]: guía para crear servidores MCP de calidad en Python (FastMCP) o Node/TypeScript. Commit en ruta 2026-04-20 — [SKILL.md](https://github.com/anthropics/skills/tree/main/skills/mcp-builder)
- `frontend-design` [V]: dirección estética, tipografía y decisiones que no parezcan plantilla al construir o rehacer UI. Commit en ruta 2026-09-03 — [SKILL.md](https://github.com/anthropics/skills/tree/main/skills/frontend-design)
- `webapp-testing` [V]: probar aplicaciones web locales con Playwright (verificar frontend, capturas, logs del navegador). Commit en ruta 2026-04-20 — [SKILL.md](https://github.com/anthropics/skills/tree/main/skills/webapp-testing)
- `web-artifacts-builder` [V]: artifacts HTML complejos con React, Tailwind y shadcn/ui. Commit en ruta 2026-04-20 — [SKILL.md](https://github.com/anthropics/skills/tree/main/skills/web-artifacts-builder)
- `doc-coauthoring` [V]: flujo estructurado para coescribir documentación, propuestas, especificaciones técnicas y documentos de decisión. Commit en ruta 2025-12-04 — [SKILL.md](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring)
- `academy-guide` [V] (nueva, commit en ruta 2026-08-18): recomienda cursos y tutoriales de Claude Academy (academy.claude.com) cuando el usuario aprende a usar Claude; también se activa con peticiones de material de formación u *onboarding* para un equipo o una clase — [SKILL.md](https://github.com/anthropics/skills/tree/main/skills/academy-guide)
- `discernment-nudge` [V] (nueva, commit en ruta 2026-08-17): tras una respuesta sustantiva (planes, propuestas, estimaciones, análisis), añade 2-3 preguntas para que el usuario compruebe datos, cuestione supuestos y detecte contexto que falta; como mucho una vez por conversación — [SKILL.md](https://github.com/anthropics/skills/tree/main/skills/discernment-nudge)

**Marketplace `anthropics/claude-plugins-official`** [V] — https://github.com/anthropics/claude-plugins-official · Anthropic · 44 639 estrellas · último push 2026-10-26 · Apache-2.0 en el repositorio, pero cada plugin tiene su propia LICENSE — [repo](https://github.com/anthropics/claude-plugins-official)
- Estructura: `/plugins` (internos, desarrollados y mantenidos por Anthropic), `/external_plugins` (partners y comunidad) y `.claude-plugin/marketplace.json`, que tiene 315 entradas [V] — [repo](https://github.com/anthropics/claude-plugins-official)
- Advertencias del README: hay que confiar en un plugin antes de instalarlo; Anthropic no controla los servidores MCP ni el software incluido y no puede garantizar que funcionen como dicen o que no cambien; los externos pasan una revisión de calidad y seguridad que tampoco garantiza su contenido; los *skill bundles* con `strict: false` traen skills de otra fuente git fijada por `sha` — [repo](https://github.com/anthropics/claude-plugins-official)
- Plugins internos relevantes para la SF [V] (descripción del `marketplace.json`; fecha = commit en ruta):
  - `skill-creator`: el mismo skill-creator empaquetado como plugin — [plugins/skill-creator](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator)
  - `mcp-server-dev`: skills para diseñar y construir servidores MCP (modelos de despliegue: HTTP remoto, MCPB, local; diseño de herramientas) — [plugins/mcp-server-dev](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/mcp-server-dev)
  - `plugin-dev`: 7 skills sobre hooks, integración MCP, comandos, agentes y buenas prácticas para crear plugins — [plugins/plugin-dev](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/plugin-dev)
  - `feature-dev` (2026-02-20): flujo de 7 fases con agentes para explorar el código, diseñar la arquitectura y revisar la calidad — [plugins/feature-dev](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/feature-dev)
  - `code-review` (2026-02-20): revisión de PR con varios agentes en paralelo y puntuación de confianza para filtrar falsos positivos — [plugins/code-review](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-review)
  - `pr-review-toolkit`: agentes de revisión de comentarios, tests, manejo de errores, diseño de tipos, calidad y simplificación — [plugins/pr-review-toolkit](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pr-review-toolkit)
  - `code-simplifier`, `commit-commands`, `security-guidance` (avisos por patrones al editar, revisión del diff con LLM al parar y revisor de commits), `claude-security` (escaneo profundo de vulnerabilidades dentro de la sesión) — [plugins](https://github.com/anthropics/claude-plugins-official/tree/main/plugins)
  - `learning-output-style` (2026-03-28): modo de aprendizaje interactivo que pide al usuario contribuciones de código en los puntos de decisión; recrea el estilo «Learning» que no llegó a publicarse, mediante un hook SessionStart, e incluye lo de explanatory — [plugins/learning-output-style](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/learning-output-style)
  - `explanatory-output-style` (2026-03-28): añade explicaciones educativas sobre decisiones de implementación; el README advierte del coste en tokens — [plugins/explanatory-output-style](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/explanatory-output-style)
  - `session-report` (2026-04-10): informe HTML explorable del uso de sesiones (tokens, eficiencia de caché, subagentes, skills, prompts más caros) — [plugins/session-report](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/session-report)
  - `receipts` (2026-10-08): informe personal de impacto generado a partir de las transcripciones (qué se entregó y en qué proyectos) — [plugins/receipts](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/receipts)
  - `project-artifact` (2026-08-13): página de estado viva de un proyecto con varias líneas de trabajo (resumen y criterios de éxito, secuencia, franja de «siguientes pasos»), publicada como artifact de claude.ai — [plugins/project-artifact](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/project-artifact)
  - `claude-md-management` (2026-02-20): skill `claude-md-improver` y comando `/revise-claude-md` para auditar CLAUDE.md y guardar lo aprendido en la sesión — [plugins/claude-md-management](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-md-management)
  - `claude-code-setup`: analiza el código y recomienda hooks, skills, MCP y subagentes — [plugins/claude-code-setup](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-code-setup)
  - `hookify` (2026-05-20): crea hooks a partir de reglas en markdown, sin editar `hooks.json` — [plugins/hookify](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/hookify)
  - `playground` (2026-02-20): «playgrounds» HTML de un solo fichero con controles, vista previa y prompt copiable — [plugins/playground](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/playground)
  - `ralph-loop` (2026-03-28): bucles iterativos autorreferenciales (técnica Ralph Wiggum) — [plugins/ralph-loop](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-loop)
  - `frontend-design`, `pyright-lsp` (Python), `clangd-lsp` (C/C++, útil para firmware), `agent-sdk-dev` (Claude Agent SDK), `code-modernization` — [plugins](https://github.com/anthropics/claude-plugins-official/tree/main/plugins)
  - `cwc-makers`: prepara un Cardputer de Code-with-Claude Makers (clona el repo build-with-claude y flashea el firmware UIFlow). Es lo más cercano a hardware dentro del marketplace oficial — [plugins/cwc-makers](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/cwc-makers)
- Entradas externas relevantes del mismo marketplace [V] (descripción del `marketplace.json`; no se ha revisado cada repositorio):
  - `superpowers` → https://github.com/obra/superpowers (ver §2)
  - `mattpocock-skills` → https://github.com/mattpocock/skills (ver §2)
  - `remember` → https://github.com/Digital-Process-Tools/claude-remember: memoria continua que resume y comprime conversaciones en registros diarios por niveles («Claude recuerda lo que hiciste ayer»). 202 estrellas, licencia NOASSERTION, push 2026-10-25 [V]
  - `context7`, `serena`, `playwright`, `github`, `linear`, `asana`, `notion`, `atlassian`, `figma`, `canva`, `exa` y `tavily` (búsqueda e investigación), `learn-with-coursera`, `duckdb-skills` (incluye búsqueda en logs de sesiones anteriores), `prisma`, `supabase`, `neon` y `planetscale` (migraciones y SQL en servicios gestionados), `telegram` y `discord` (canales), `coderabbit`, `greptile` y `qodo` (revisión de código), `logfire` (observabilidad de FastAPI) — [marketplace.json](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json)

### Inferences
- Para el MCP de JKanban (FastAPI + SQLite), `mcp-builder` y `mcp-server-dev` son la referencia oficial más directa: cubren FastMCP en Python, que coincide con el stack del kanban.
- `learning-output-style` y `explanatory-output-style` son la base oficial más cercana a los trabajos de «enseñar» y «aprender»: el modo Learning, que pide al alumno escribir el código en los puntos de decisión, encaja con formar a programadores nuevos.
- `receipts`, `session-report` y `project-artifact` cubren parte de los informes de cierre, el resumen diario y el panel multiproyecto. Ninguno integra un kanban propio; habría que adaptarlos.
- `claude-md-management` y `hookify` encajan con la automejora continua (guardar lo aprendido en la sesión y convertir errores repetidos en reglas).
- `discernment-nudge` responde directamente al riesgo de aceptar sin crítica lo que produce la IA, tratado en el informe de fricciones. Conviene compararla con las salvaguardas propias de la SF.
- Las document skills no son open source: se pueden usar, pero redistribuirlas con la SF tiene restricciones.

### Gaps
- No he leído la LICENSE de cada plugin interno; el README dice que puede variar.
- La fecha de `skill-creator` en el marketplace de plugins no se comprobó por separado (es una copia empaquetada).
- No se encontró documentación oficial con el número de plugins aprobados ni con los criterios exactos de su revisión de seguridad.

## 2. Grandes colecciones comunitarias y su correspondencia con las necesidades de la SF

### Takeaway
Los ecosistemas comunitarios más activos en 2026 son obra/superpowers y mattpocock/skills (ambos MIT, más de 300 000 estrellas, presentes en el marketplace oficial), wshobson/agents (más de 80 plugins temáticos), ECC (antes everything-claude-code), alirezarezvani/claude-skills y las listas curadas hesreallyhim/awesome-claude-code y ComposioHQ/awesome-claude-skills. Cubren bien planificación, TDD, revisión, verificación e investigación; flojean en enseñanza de programación, hardware, Tkinter y migraciones con SQL nativo.

### Cited Findings

**Colecciones y listas** (todas [V] por la API de GitHub salvo que se indique)

| Repositorio | Autor | Estrellas | Licencia | Último push | Tipo |
|---|---|---|---|---|---|
| https://github.com/obra/superpowers | Jesse Vincent (obra) | 305 257 | MIT | 2026-10-23 | Skills y metodología |
| https://github.com/mattpocock/skills | Matt Pocock | 303 538 | MIT | 2026-10-22 (último commit 2026-10-19) | Skills |
| https://github.com/affaan-m/ECC (antes everything-claude-code) | affaan-m | 289 115 | MIT | 2026-10-26 | Arnés: skills, memoria, seguridad |
| https://github.com/github/spec-kit | GitHub | 142 936 | MIT | 2026-10-23 | SDD (ya es candidato de la SF) |
| https://github.com/ComposioHQ/awesome-claude-skills | Composio | 77 969 | ninguna | 2026-09-18 | Lista curada |
| https://github.com/hesreallyhim/awesome-claude-code | hesreallyhim | 56 564 | NOASSERTION | 2026-10-26 | Lista curada (263 recursos en CSV) |
| https://github.com/K-Dense-AI/scientific-agent-skills | K-Dense AI | 54 662 | MIT | 2026-10-19 | Skills científicas |
| https://github.com/bmad-code-org/BMAD-METHOD | BMAD | 54 566 | NOASSERTION | 2026-10-20 | Metodología (ya es candidato de la SF) |
| https://github.com/wshobson/agents | Seth Hobson | 41 733 | MIT | 2026-10-26 | Marketplace multiherramienta |
| https://github.com/davila7/claude-code-templates | davila7 | 32 908 | MIT | 2026-10-26 | CLI para configurar y monitorizar |
| https://github.com/alirezarezvani/claude-skills | Alireza Rezvani | 28 735 | MIT | 2026-10-23 | 380+ skills |
| https://github.com/VoltAgent/awesome-claude-code-subagents | VoltAgent | 26 068 | MIT | 2026-10-11 | 100+ subagentes |
| https://github.com/travisvn/awesome-claude-skills | travisvn | 15 569 | ninguna | 2026-04-28 | Lista curada |
| https://github.com/trailofbits/skills | Trail of Bits | 7 805 | CC-BY-SA-4.0 | 2026-10-24 | Skills de seguridad |
| https://github.com/jeremylongshore/tons-of-skills-marketplace | Jeremy Longshore | 2 873 | MIT | 2026-10-26 | Marketplace con gestor de paquetes |
| https://github.com/travisjneuman/.claude | Travis Neuman | 106 | MIT | 2026-10-25 | Kit: 180 skills, 7 hooks |

- Superpowers, skills actuales [V]: brainstorming, writing-plans, executing-plans, subagent-driven-development, dispatching-parallel-agents, test-driven-development, systematic-debugging, requesting-code-review, receiving-code-review, verification-before-completion, finishing-a-development-branch, using-git-worktrees, writing-skills, using-superpowers y diagnosing-superpowers — [skills/](https://github.com/obra/superpowers/tree/main/skills). Según el marketplace oficial: lluvia de ideas, desarrollo dirigido por subagentes con revisión de código integrada, depuración sistemática y TDD rojo/verde — [marketplace.json](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json)
- mattpocock/skills [V]: engineering (code-review, tdd, to-spec, to-tickets, implement-spec, implement, prototype, research, retro, triage, wayfinder, domain-modeling, diagnosing-bugs, improve-codebase-architecture, grill-with-docs, pr), productivity (grill-me, handoff, **teach**, to-questionnaire, writing-for-agents, wait-what), misc (**scaffold-exercises**, git-guardrails-claude-code, setup-pre-commit), in-progress (chief-of-staff, claude-handoff, loop-me…) — [árbol del repo](https://github.com/mattpocock/skills/tree/main/skills)
  - `to-tickets`: divide un plan o especificación en tickets *tracer-bullet* con dependencias de bloqueo y los publica en el tracker configurado (un fichero por ticket en local o enlaces nativos en un tracker real) [V] — [SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md)
  - `wayfinder`: planifica un trabajo mayor que una sesión como un mapa de tickets de decisión en el tracker, que se resuelven uno a uno [V] — [SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md)
  - `teach`: enseña al usuario una habilidad o un concepto dentro del espacio de trabajo [V] — [SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/teach/SKILL.md)
  - `scaffold-exercises`: crea estructuras de ejercicios con secciones, problemas, soluciones y explicaciones que pasan el linter [V] — [SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/misc/scaffold-exercises/SKILL.md)
  - `research`: investiga contra fuentes primarias en un agente de fondo y guarda el resultado en Markdown en el repo [V] — [SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/engineering/research/SKILL.md)
  - `retro` (retrospectiva de una sesión) y `handoff` (comprime la conversación en un documento de relevo) [V] — [repo](https://github.com/mattpocock/skills)
- wshobson/agents: carpetas de plugins relevantes [V] — `tdd-workflows` («TDD con ciclos rojo-verde-refactor y revisión»), `database-migrations` («automatización de migraciones, observabilidad y estrategias entre bases de datos»), `arm-cortex-microcontrollers` («firmware ARM Cortex-M para Teensy, STM32, nRF52 y SAMD con drivers de periféricos y patrones de seguridad de memoria»), `python-development` («Python 3.12+, Django, FastAPI, async»), `team-collaboration` («gestión de issues, automatización de standups»), `before-you-build` («revisión de riesgos de producto antes de implementar, para fundadores»), `conductor`, `c4-architecture`, `code-documentation`, `comprehensive-review`, `unit-testing`, `debugging-toolkit`, `startup-business-analyst`, `systems-programming` — [plugins/](https://github.com/wshobson/agents/tree/main/plugins)

**Correspondencia por necesidad de la SF** (repositorios no citados arriba, verificados con la API de GitHub salvo indicación)

| Necesidad | Candidatos | Datos [V] |
|---|---|---|
| Planificar y preparar devslices | Superpowers `writing-plans`/`executing-plans`; mattpocock `to-spec`, `to-tickets`, `wayfinder`; oficial `feature-dev`; **Plannotator** (UI para anotar planes interceptando ExitPlanMode con hooks) https://github.com/backnotprop/plannotator; AB Method https://github.com/ayoubben18/ab-method; RIPER-5 https://github.com/tony/claude-code-riper-5; Claude Code Harness (Plan→Work→Review) https://github.com/Chachamaru127/claude-code-harness; Charrette (diseño antes del código) https://github.com/Ovich/charrette | Plannotator 9 649★ Apache-2.0 2026-10-26 · AB Method 192★ MIT 2026-10-22 · RIPER-5 95★ MIT 2026-08-16 · Harness 3 186★ MIT 2026-10-26 · Charrette redirige a `Ovich/swarmstorm` 13★ MIT 2026-10-25 (renombrado; comprobar) |
| TDD | Superpowers `test-driven-development`; mattpocock `tdd`; wshobson `tdd-workflows`; **TDD Guard** (hooks que bloquean cambios que violan TDD) https://github.com/nizos/tdd-guard; Claude CodePro / qualitylayer (flujo con especificación y TDD obligatorio) https://github.com/maxritter/claude-codepro | TDD Guard 2 367★ MIT 2026-10-12 · claude-codepro redirige a `maxritter/qualitylayer` 2 101★ NOASSERTION 2026-10-26 |
| Revisión de código | Oficiales `code-review`, `pr-review-toolkit`, `code-simplifier`, `security-guidance`; Superpowers `requesting-/receiving-code-review`; mattpocock `code-review`; Claude Code Workflows (revisión de PR, seguridad y diseño) https://github.com/OneRedOak/claude-code-workflows; localpr (revisión local de cambios sin commit al estilo PR) https://github.com/gilles-g/localpr; Trail of Bits | Workflows 3 908★ MIT 2026-10-09 · localpr 4★ MIT 2026-10-21 |
| Verificación e informes de cierre | Superpowers `verification-before-completion` y `finishing-a-development-branch`; mattpocock `retro` y `handoff`; oficiales `receipts`, `session-report` y `project-artifact`; visual-explainer (salida de terminal → páginas HTML o diapositivas) https://github.com/nicobailon/visual-explainer; claude-replay (transcripciones → reproducciones incrustables) https://github.com/es617/claude-replay | visual-explainer 10 631★ MIT 2026-10-20 · claude-replay 850★ MIT 2026-10-16 |
| Kanban / integración MCP | Vibe Kanban (tablero para orquestar agentes) https://github.com/BloopAI/vibe-kanban; Backlog.md (tareas en markdown dentro de git, para humanos y agentes) https://github.com/MrLesk/Backlog.md; Task Master https://github.com/eyaltoledano/claude-task-master; kanban-mcp https://github.com/multidimensionalcats/kanban-mcp; kanban-mcp (memoria de tareas multisesión) https://github.com/eyalzh/kanban-mcp; oficiales `linear`, `asana`, `notion`, `github` | vibe-kanban 28 458★ Apache-2.0 2026-10-26 · Backlog.md 7 150★ MIT 2026-10-25 · task-master 28 276★ NOASSERTION 2026-04-28 · multidimensionalcats 84★ MIT 2026-03-17 · eyalzh 41★ MIT 2025-07-13 |
| Resúmenes diarios y memoria | Oficial-externo `remember` (registros diarios); claude-code-tools (continuidad de sesión) https://github.com/pchalasani/claude-code-tools; mattpocock `handoff`; ccusage `daily` | claude-code-tools 2 019★ MIT 2026-10-24 |
| Investigación | mattpocock `research`; oficiales-externos `exa`, `tavily`, `context7`; AI Research Skills (15 skills en 8 etapas: literatura, análisis de huecos, diseño…) https://github.com/WenyuChiou/ai-research-skills; K-Dense scientific-agent-skills | AI Research Skills 407★ MIT 2026-10-26 |
| Mantenerse al día (resúmenes de changelog) | claude-daily-digest (resumen diario del changelog de Claude Code por correo; launchd de macOS + `claude -p` sin interfaz + SMTP de Gmail) https://github.com/NicoSuave17/claude-daily-digest; claude-code-docs (espejo de la documentación con búsqueda de texto completo) https://github.com/costiash/claude-code-docs; daily.dev (noticias curadas; la lista lo incluye por sus skills y plugins) https://github.com/dailydotdev/daily | digest 5★ MIT 2026-04-21 (solo macOS) · claude-code-docs 55★ NOASSERTION 2026-10-26 · daily.dev 20 117★ AGPL-3.0 2026-10-23 (es la plataforma entera; habría que localizar dónde están las skills) |
| Enseñar (material de curso, ejercicios) | mattpocock `scaffold-exercises`; Codebase to Course (repositorio → curso HTML interactivo) https://github.com/zarazhangrui/codebase-to-course; oficial `learning-output-style`; oficial `academy-guide`; course-material-creator de travisjneuman/.claude [S] https://claudemarketplaces.com/skills/travisjneuman/.claude/course-material-creator; School Skills (K-12, fichas con solucionario y cuestionarios) [S] https://sharedcontext.ai/plugins/external/Jellypod-Inc/school-skills-for-claude-code | codebase-to-course 5 731★ **sin licencia** 2026-03-30 · Jellypod-Inc/school-skills-for-claude-code: el repo da 404 en la API de GitHub |
| Aprender (modos explicativo o tutor) | Oficiales `learning-output-style`, `explanatory-output-style`; mattpocock `teach`; Bloom (tutoría «2 sigma» de Bloom como skill) https://github.com/Li-Evan/Bloom; learn-faster-kit (método FASTER) https://github.com/hluaguo/learn-faster-kit; Universal Exam Cram Coach https://github.com/ZeKaiNie/universal-examprep-skill; RAG Learning Academy https://github.com/TakaGoto/rag-learning-academy | Bloom 292★ MIT 2026-10-20 · learn-faster-kit 394★ MIT 2026-08-04 · examprep 318★ MIT 2026-10-19 · RAG Academy 24★ MIT 2026-04-03 |
| Diseño y prototipos | Oficiales `frontend-design`, `playground`, `web-artifacts-builder`; externos `figma`, `canva`; Dev Browser (el agente prueba su propio trabajo en un navegador) https://github.com/SawyerHood/dev-browser; Snip (pizarra visual entre usuario y agente) https://github.com/rixinhahaha/snip; mattpocock `prototype` | Dev Browser 6 696★ MIT 2026-10-18 · Snip 348★ MIT 2026-05-07 |
| Hardware, embebidos, gemelos digitales | wshobson `arm-cortex-microcontrollers`; oficial `clangd-lsp`; oficial `cwc-makers` (Cardputer); platformio-mcp https://github.com/jl-codes/platformio-mcp; embedded-agent-skills https://github.com/claudius-ars/embedded-agent-skills; electronics-agent-kit (skill de PlatformIO para Arduino, ESP-IDF y STM32) https://github.com/o2scale/electronics-agent-kit; skill embedded-iot de travisjneuman/.claude [S] | platformio-mcp 54★ MIT 2026-10-13 · embedded-agent-skills 21★ MIT 2026-02-08 · electronics-agent-kit 14★ MIT 2026-02-03 |
| Migraciones SQL | wshobson `database-migrations`; oficiales-externos `prisma`, `supabase`, `neon` y `planetscale` (ligados a servicios gestionados u ORM) | — |
| Python de escritorio (Tkinter) | Nada específico; `pyright-lsp` y wshobson `python-development` como base general | — |

- Búsqueda web: no se encontraron skills oficiales de Espressif, Arduino ni PlatformIO; todo lo que aparece es comunitario [S] — [mcpmarket](https://mcpmarket.com/tools/skills/platformio-embedded-development), [skillsmp](https://skillsmp.com/creators/o2scale/electronics-agent-kit/agent-skills-platformio)
- Búsqueda web: para material de cursos de programación no hay una skill que encaje claramente; los resultados son generadores genéricos de práctica, cuestionarios K-12 y codebase-to-course [S] — [claudskills learning-practice-generator](https://claudskills.com/skills/learning-practice-generator/), [claudskills exercise-builder](https://claudskills.com/skills/exercise-builder/)

### Inferences
- Superpowers y mattpocock/skills son los candidatos de mayor señal: los dos están en el marketplace oficial, tienen licencia MIT y actividad en octubre de 2026, y cubren planificación, TDD, revisión, verificación, relevo y retrospectiva. mattpocock añade `to-tickets` y `wayfinder`, con un *tracker* configurable, que podría apuntar al kanban (habría que comprobar si admite un tracker propio vía MCP).
- Para la SF, Backlog.md es la alternativa al kanban más parecida en filosofía («tareas en git para humanos y agentes»), y vibe-kanban la más popular; las dos sirven para inspirarse en las herramientas MCP de JKanban, no para sustituirlo.
- Enseñar, Tkinter, gemelos digitales y migraciones con SQL nativo (sin ORM ni proveedor) son huecos: probablemente la SF tenga que crear skills propias con `skill-creator`, partiendo de `scaffold-exercises`, `learning-output-style` y codebase-to-course.
- codebase-to-course no tiene licencia: puede estudiarse, pero no copiarse ni redistribuirse.

### Gaps
- No se leyó el contenido de las skills comunitarias. Calidad, tamaño en tokens y posibles instrucciones ocultas no están evaluados.
- Las cifras de estrellas de superpowers, mattpocock y ECC (unas 290 000-305 000) proceden de la API, pero son excepcionalmente altas; no se ha verificado si hay inflación.
- No se encontró un candidato serio para gemelos digitales ni para Tkinter.
- Charrette y Claude CodePro redirigen a repositorios renombrados (`Ovich/swarmstorm`, `maxritter/qualitylayer`); no se confirmó que el contenido siga siendo el mismo.

## 3. Plugins con hooks para notificaciones, resúmenes de sesión, seguimiento de tiempo o atención y paneles multiproyecto

### Takeaway
Hay una categoría comunitaria amplia de observabilidad (uso y coste, monitores de sesión, barras de estado) y otra de notificaciones. Para el «hombre orquesta» que lleva muchos proyectos, los candidatos más sólidos son ccusage y Codeburn (coste y uso por proyecto), Claude HUD (barra de estado), Claude Code Agent Monitor y agents-observe (paneles basados en hooks) y anotifier (avisos al escritorio o al móvil cuando el agente necesita atención). Casi todos los monitores de menú son solo para macOS, y el usuario trabaja en Windows.

### Cited Findings
- **ccusage** https://github.com/ccusage/ccusage — ryoppippi · CLI sin instalación (`npx ccusage`) que analiza tokens y coste desde los JSONL locales, por día y otras agregaciones · 19 178★ · NOASSERTION · 2026-10-26 [V] — [awesome-claude-code CSV](https://github.com/hesreallyhim/awesome-claude-code)
- **Codeburn** https://github.com/getagentseal/codeburn — gasto local desglosado por proyecto, modelo, rama de git y tarea; seguimiento de cuotas del plan · 11 578★ · MIT · 2026-10-26 [V]
- **Claude HUD** https://github.com/jarrodwatts/claude-hud — Jarrod Watts · barra de estado con uso de contexto, herramientas, agentes… · 28 888★ · MIT · 2026-10-26 [V]
- **Claude Code Agent Monitor** https://github.com/hoangsonww/Claude-Code-Agent-Monitor — panel autoalojado en tiempo real basado en los hooks nativos (sesiones en vivo) · 1 118★ · MIT · 2026-10-23 [V]
- **agents-observe** https://github.com/simple10/agents-observe — panel de observabilidad instalado como plugin que registra hooks en todo el ciclo de la sesión · 708★ · MIT · 2026-09-04 [V]
- **Multi-Agent Observability** https://github.com/disler/claude-code-hooks-multi-agent-observability — disler · panel que captura eventos de hooks de agentes concurrentes · 1 554★ · **sin licencia** · 2026-02-08 [V]
- **Claude Code OTel stack** https://github.com/ColeMurray/claude-code-otel — OpenTelemetry → Grafana en Docker · 513★ · MIT · **2025-06-17** (sin actividad en 2026) [V]
- **anotifier** https://github.com/DevinoSolutions/anotifier-for-claude-codex-cursor — notificador multiplataforma sin dependencias: aviso en el escritorio y push gratuito al móvil (ntfy) cuando el agente necesita al usuario · 33★ · **AGPL-3.0** · 2026-10-22 [V]
- **cc-semaphore** https://github.com/patakuti/cc-semaphore — junta el estado (en marcha, esperando, inactivo) de sesiones paralelas · 2★ · MIT · 2026-10-11 [V]
- **bough** https://github.com/nickelsec/bough — dibuja la historia de un proyecto a partir de las transcripciones JSONL · 128★ · MIT · 2026-10-20 [V]
- **Awesome Claude Code Mods** https://github.com/karanb192/awesome-claude-code-mods — lista comunitaria de mods hechos con hooks; escanea GitHub · 762★ · CC0-1.0 · 2026-10-26 [V]
- **Review Inbox** https://github.com/SummerRiversound/review-inbox — mod que muestra sobre el prompt los PR pendientes de revisión · 2★ · MIT · 2026-10-26 [V]
- La lista awesome-claude-code tiene subcategorías «Usage & Cost» (Claumon, ccvitals, toktrack, CCDash, Pacer, goccc, better-ccflare, ccxray…), «Session Monitors» (c9watch, Claude Status, claude-control, cctop, so-agentbar… mayoritariamente de barra de menú de macOS) y «Remote Control, Notifications & Voice I/O» (Claude Threads hacia Slack o Mattermost, bot de Telegram, canal de WhatsApp) [V: descripciones del CSV; repositorios no verificados uno a uno] — [THE_RESOURCES_TABLE_NEW.csv](https://github.com/hesreallyhim/awesome-claude-code/blob/main/THE_RESOURCES_TABLE_NEW.csv)
- Oficiales: `session-report` (uso por sesión), `receipts` (impacto por proyecto), `project-artifact` (página de estado), `telegram`, `discord` y `fakechat` (flujo de notificaciones por canal) [V] — [marketplace.json](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json)

### Inferences
- No hay ningún plugin que mida tiempo o atención humana (interrupciones, cambios de contexto entre proyectos). Los existentes miden tokens, coste y estado del agente. Codeburn (por proyecto y tarea) y `receipts` (por proyecto) son lo más aprovechable como indicador indirecto.
- Un panel multiproyecto para la SF podría salir de combinar los hooks de Claude Code con el kanban (JKanban) en lugar de adoptar un monitor externo; Agent Monitor y agents-observe sirven de referencia de arquitectura.
- Licencias que condicionan la redistribución: anotifier es AGPL-3.0 y disler no tiene licencia.

### Gaps
- No se comprobó qué monitores funcionan en Windows.
- No se encontró ningún plugin específico de seguimiento de tiempo o de foco.

## Riesgos transversales (calidad, mantenimiento, licencia, cadena de suministro)

### Takeaway
El riesgo principal es la cadena de suministro: las skills y los hooks ejecutan instrucciones y código con los permisos del usuario. Las auditorías de 2026 encuentran tasas altas de problemas en los registros abiertos de skills, y el propio marketplace oficial avisa de que su revisión no garantiza el contenido.

### Cited Findings
- Snyk «ToxicSkills» (febrero de 2026): de 3 984 skills de ClawHub y skills.sh, el 13,4 % (534) tenía al menos un problema crítico (distribución de malware, inyección de prompts, secretos expuestos) y el 36,82 % (1 467) al menos un fallo de cualquier gravedad [S: resumen de búsqueda; el titular dice «prompt injection in 36%», pero esa cifra cubre cualquier fallo] — [Snyk](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub)
- MalSkillBench (arXiv 2606.07131, junio de 2026): banco de pruebas de 3 944 skills maliciosas verificadas en ejecución [S] — [emergentmind](https://www.emergentmind.com/papers/2606.07131)
- MITRE ATLAS añadió técnicas agénticas como el envenenamiento de skills y la exfiltración mediante llamadas a herramientas [S] — [Security Affairs](https://securityaffairs.com/199454/ai/the-target-is-no-longer-the-model-its-the-agent.html)
- El marketplace oficial avisa de que Anthropic no controla el contenido de los plugins y de que la revisión de los externos no lo garantiza [V] — [claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

### Inferences
- Si la SF adopta algo, debería ser copiando o adaptando el texto de las skills a `skills/` del repositorio con su ORIGIN.md (como ya hace la SF), fijando el commit y revisándolo, no instalando marketplaces que se actualizan solos. Los plugins con hooks o servidores MCP necesitan una revisión más estricta que las skills que solo contienen texto.
- Los mantenedores individuales con muchas estrellas (superpowers, mattpocock) cambian a menudo; fijar el commit evita que cambie el comportamiento sin que nadie lo note.

### Gaps
- No se encontró ninguna auditoría que cubra específicamente el marketplace oficial de Anthropic ni los repositorios comunitarios citados.
