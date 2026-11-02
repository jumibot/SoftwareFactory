# Agentes de IA en productos y desarrollo hardware+software con gemelo digital (a 2026-10-26)

Notas de investigación. Prioridad a la documentación oficial. «Verificado» = leído en la página primaria citada; «opinión/secundario» = prensa, blogs o resúmenes de terceros. Todo lo que se cita es candidato, no recomendación aprobada.

## A1. Estado del Claude Agent SDK, Managed Agents, MCP y otros frameworks

### Takeaway
El Claude Agent SDK es la forma oficial de incrustar el bucle de Claude Code en una aplicación propia (Python/TypeScript), con salida estructurada por JSON Schema y control explícito de qué configuración del sistema de archivos carga. Managed Agents (beta pública desde el 8-abr-2026) es la variante alojada por Anthropic. MCP está bajo gobierno neutral (Linux Foundation) desde dic-2025. Entre los frameworks de terceros, LangGraph y Pydantic AI tienen versiones estables con compromiso de compatibilidad; OpenAI Agents SDK, Google ADK y CrewAI no se verificaron en fuente primaria.

### Cited Findings
**Claude Agent SDK (verificado, documentación oficial de Anthropic)**
- El Agent SDK «gives you the same tools, agent loop, and context management that power Claude Code, programmable in Python and TypeScript»; es «a library that runs the Claude Code binary», con herramientas integradas, permisos, sesiones, hooks, subagentes, MCP, skills y plugins. Para otros lenguajes: ejecutar la CLI como subproceso con `-p` y `--output-format json`. El antiguo «Claude Code SDK» pasó a llamarse Claude Agent SDK. — [Agent SDK overview, code.claude.com](https://code.claude.com/docs/en/agent-sdk/overview)
- Tabla oficial de elección: Agent SDK (agente en un proceso que operas tú), CLI (uso interactivo), Client SDK (API directa, bucle de herramientas propio o el *tool runner* beta), Managed Agents (Anthropic aloja el agente; sandbox gestionado o [self-hosted sandbox](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes)). — [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- Uso gobernado por los Commercial Terms of Service, también cuando se usa para productos ofrecidos a clientes finales. Branding: permitido «Claude Agent» o «{TuAgente} Powered by Claude»; no permitido «Claude Code» ni «Claude Code Agent». — [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- **Aislamiento de la configuración del desarrollador** (relevante para LecturaFàcil): si se omite `settingSources`/`setting_sources`, el SDK carga lo mismo que la CLI (`["user","project","local"]`: `~/.claude/`, CLAUDE.md, skills, hooks…). Con `setting_sources=[]` se limita a lo configurado por programa. Aun así se leen siempre: políticas gestionadas, `~/.claude.json` (reubicable con `CLAUDE_CONFIG_DIR` en `env`), la memoria automática en `~/.claude/projects/<project>/memory/` (desactivable con `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`) y los conectores MCP de claude.ai si se autentica con login de claude.ai (desactivables con `strictMcpConfig: true` o `ENABLE_CLAUDEAI_MCP_SERVERS=false`). Aviso oficial: «Do not rely on default `query()` options for multi-tenant isolation». Las skills solo se registran como archivos `.claude/skills/<name>/SKILL.md`; no hay API para registrarlas por programa; la opción `skills` acepta `"all"`, lista o `[]`. — [Use Claude Code features in the SDK](https://code.claude.com/docs/en/agent-sdk/claude-code-features.md)
- **Salida contractual con esquema**: opción `output_format={"type":"json_schema","schema":...}` (Python) / `outputFormat` (TS); el resultado trae `structured_output` validado; el SDK reintenta ante discrepancias y, si no lo logra, devuelve subtipo `error_max_structured_output_retries`. Valida con JSON Schema **draft-07** (rechaza esquemas que declaran versiones más nuevas); `format` es solo anotación. Admite Pydantic (`model_json_schema()`) y Zod (`target: "draft-7"`). Desde v2.1.205 un esquema inválido falla al arrancar (antes se ignoraba en silencio). También puede acabar en `success` sin `structured_output`: tratarlo como fallo. — [Structured outputs, Agent SDK](https://code.claude.com/docs/en/agent-sdk/structured-outputs.md)

**Claude Managed Agents (verificado, blog oficial; precio y estado según el mismo post)**
- Lanzado el 8-abr-2026 en beta pública: «a suite of composable APIs for building and deploying cloud-hosted agents at scale». Sandbox, autenticación, ejecución de herramientas, sesiones largas con persistencia, permisos acotados, trazas. Coordinación multiagente y autoevaluación por resultados en *research preview* (requiere solicitar acceso). Añadidos posteriores: memoria integrada, despliegues programados con credenciales en *vault*, sandboxes autoalojados con túneles MCP. Precio: tarifas de tokens + 0,08 USD por hora de sesión activa. Clientes citados: Notion, Rakuten, Asana, Sentry, Atlassian, Vibecode, General Legal, Blockit. — [Claude Managed Agents, claude.com/blog, 2026-04-08](https://claude.com/blog/claude-managed-agents); cobertura secundaria: [InfoWorld](https://infoworld.com/article/4156852/anthropic-rolls-out-claude-managed-agents.html)
- Afirmación de marketing (no verificada independientemente): mejora de hasta 10 puntos en éxito de tareas de generación de archivos estructurados frente a un bucle de prompting estándar, según pruebas internas. — [mismo post](https://claude.com/blog/claude-managed-agents)

**MCP como estándar de integración**
- El 9-dic-2025 Anthropic donó MCP a la Agentic AI Foundation, fondo dirigido de la Linux Foundation, cofundada con Block y OpenAI y apoyada por Google, Microsoft, AWS, Cloudflare y Bloomberg; proyectos iniciales: MCP, goose (Block) y AGENTS.md (OpenAI). Anthropic declara >10.000 servidores MCP públicos activos y adopción en ChatGPT, Cursor, Gemini, Microsoft Copilot y VS Code (cifras de Anthropic, no verificadas por terceros). — [Anthropic news](https://anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation); [The New Stack](https://thenewstack.io/anthropic-donates-the-mcp-protocol-to-the-agentic-ai-foundation/)

**Otros frameworks**
- LangGraph 1.0 y LangChain 1.0 anunciados el 22-oct-2025, con compromiso de no romper compatibilidad hasta 2.0; LangGraph se presenta como framework y runtime de bajo nivel para agentes muy controlables. — [LangChain blog](https://blog.langchain.com/langchain-langgraph-1dot0)
- Pydantic AI v1.0.0 el 2025-09-04 (changelog oficial) con política de no romper código al menos 6 meses; V1 incluyó aprobación humana de herramientas y ejecución durable con Temporal. Según búsqueda, existe v2.0.0 estable con fecha 2026-06-23 (dato de la guía de actualización vista en snippet; no leído en detalle). — [Pydantic AI V1](https://pydantic.dev/articles/pydantic-ai-v1); [changelog](https://ai.pydantic.dev/changelog)
- Opinión/secundario: LangGraph descrito como el más endurecido para producción (checkpointing, ejecución durable) con la curva más empinada; OpenAI Agents SDK como opción ligera (agentes, handoffs, guardrails, tracing) que funciona mejor con modelos de OpenAI; Google ADK 2.0 con la mayor cobertura de lenguajes (Python, TS, Go, Java, Kotlin) y >100 proveedores vía LiteLLM; AutoGen en modo mantenimiento; ACP fusionado en A2A bajo la Linux Foundation. — [morphllm.com](https://www.morphllm.com/ai-agent-framework); [gamut.so](https://www.gamut.so/blog/best-ai-agent-frameworks-2026); [requesty.ai](https://requesty.ai/blog/best-ai-agent-sdks-compared-2026-langchain-crewai-openai-anthropic-google). Fuentes de calidad media, con rankings discrepantes.

### Inferences
- Para mantener el agente de producto intercambiable, las piezas más estables documentadas son: (1) contrato de salida en JSON Schema draft-07, que el Agent SDK valida y que Pydantic AI y otros también consumen; (2) herramientas de dominio expuestas como servidores MCP, estándar ya bajo gobierno neutral y soportado por todos los frameworks citados; (3) una interfaz propia del producto (p. ej. `Agente.ejecutar(entrada) -> salida validada`) con una implementación simulada para pruebas y otra real con Agent SDK. Esto encaja con la espera del propietario a «una solución más asentada»: el cambio de runtime (Agent SDK → Managed Agents → otro framework) quedaría detrás de esa interfaz.
- Para LecturaFàcil: `setting_sources=[]` + `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` + `CLAUDE_CONFIG_DIR` propio + `strictMcpConfig`, y skills del producto en un `cwd` dedicado, es la receta documentada más cercana a «aislado de la configuración del desarrollador». Queda por probar en la práctica.
- Managed Agents suprime la operación de infraestructura pero ata a Anthropic y está en beta; para una app de escritorio local no parece el encaje natural.

### Gaps
- No se verificaron en fuente primaria el estado/versión de OpenAI Agents SDK, Google ADK 2.0 ni CrewAI en 2026.
- No se leyó la página oficial de Managed Agents (`platform.claude.com/docs/en/managed-agents/overview`) ni sus límites de beta.
- Fecha y detalle de Pydantic AI v2 solo vistos en snippets.

## A2. Política de credenciales y facturación al incrustar Claude en productos

### Takeaway
Oficialmente: los productos (incluidos los hechos con Agent SDK) deben usar **clave de API** (Claude Console o proveedor cloud), no login de claude.ai ni credenciales Free/Pro/Max. Excepción documentada: si el producto ejecuta el binario de Claude Code sin modificar, cada usuario final puede autenticarse con su propia clave o su propia suscripción, pero el fabricante no puede pagar, revender ni intermediar ese uso.

### Cited Findings
- Nota oficial: «Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Use the API key authentication methods…» — [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- «Developers building products or services that interact with Claude's capabilities, including those using the Agent SDK, should use API key authentication through Claude Console or a supported cloud provider. Anthropic does not permit third-party developers to offer Claude.ai login into their own applications, or to route requests through Free, Pro, or Max plan credentials on behalf of their users. Moreover, developers may not collect, store, or intermediate Claude.ai credentials or session tokens.» Los límites anunciados de Pro/Max «assume ordinary, individual usage of Claude Code and the Agent SDK». Anthropic puede aplicar medidas «without prior notice». — [Legal and compliance, code.claude.com](https://code.claude.com/docs/en/legal-and-compliance)
- Preinstalar o ejecutar Claude Code dentro de productos requiere Commercial Terms y: binario sin modificar (sin quitar métodos de autenticación) y «Customers may not pay for, resell, or intermediate Claude usage on their end users' behalf. Each end user must authenticate with their own Anthropic API key, Claude subscription plan credentials, or 3P inference provider credential». Se permite gestionar claves propias (secret manager, imagen de máquina) para usuarios autorizados propios si se factura al titular. — [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance)
- Secundario: la aplicación efectiva de la restricción a OAuth de suscripción en herramientas de terceros se reportó en 2026 con fechas discrepantes (bloqueos desde 9-ene-2026; actualización de documentación 19-feb-2026; facturación como *overage* desde 4-abr-2026). — [AlternativeTo, feb-2026](https://alternativeto.net/news/2026/2/anthropic-officially-bans-using-subscription-authentication-for-third-party-claude-use); [WinBuzzer, 2026-02-19](https://winbuzzer.com/2026/02/19/anthropic-bans-claude-subscription-oauth-in-third-party-apps-xcxwbn/); [falcao.org](https://falcao.org/posts/anthropic-claude-access-crackdown-ecosystem-fallout/)

### Inferences
- LecturaFàcil vía Agent SDK: necesita clave de API (del propietario para uso propio, o de cada usuario si se distribuye). Usar la suscripción Max del desarrollador para el agente del producto no está permitido según la documentación.
- Prototipar con Claude Code como orquestador (OncoCore) con la propia suscripción entra en «uso individual ordinario» mientras sea el propio desarrollador; deja de serlo al ofrecerlo a terceros. Conviene confirmarlo con Anthropic si hay duda (la doc remite a ventas).

### Gaps
- No se leyó el texto actual de los Consumer Terms (anthropic.com/legal/consumer-terms) ni la fecha de la última revisión de la página de cumplimiento.

## A3. Pruebas y evaluación de agentes de producto para equipos pequeños

### Takeaway
La guía oficial de Anthropic (9-ene-2026) recomienda empezar con 20–50 tareas sacadas de fallos reales, graders deterministas cuando sea posible, leer transcripciones, y separar evals de capacidad y de regresión; medir pass^k para agentes de cara al cliente.

### Cited Findings
- «20-50 simple tasks drawn from real failures is a great start»; convertir comprobaciones manuales previas a la publicación y bugs reportados en casos; tareas inequívocas (dos expertos llegarían al mismo veredicto) con solución de referencia; si muchos intentos dan 0 %, sospechar de la tarea; casos equilibrados (cuando el comportamiento debe y no debe ocurrir). — [Demystifying evals for AI agents, Anthropic Engineering, 2026-01-09](https://anthropic.com/engineering/demystifying-evals-for-ai-agents)
- Graders: deterministas (código, tests, estado) preferentes; LLM cuando haga falta; humanos para calibrar. Evaluar el resultado, no el camino exacto; crédito parcial. — [misma fuente](https://anthropic.com/engineering/demystifying-evals-for-ai-agents)
- pass@k (al menos un éxito en k) frente a pass^k (todos los k); ejemplo: 75 % por intento → ~42 % en pass^3. Evals de capacidad empiezan bajas; las de regresión deben rondar el 100 %; promover las saturadas a regresión. Entorno limpio en cada intento; mantener las evals como tests unitarios, con dueño. — [misma fuente](https://anthropic.com/engineering/demystifying-evals-for-ai-agents)

### Inferences
- Para la SF: un *golden set* de 20–50 casos por agente de producto, graders deterministas sobre el JSON contractual (validación de esquema + comprobaciones de campos), un agente simulado/determinista para los tests unitarios del resto del sistema, y una batería de evals reales ejecutada a demanda (coste de API) separada de la suite normal.

### Gaps
- No se investigaron herramientas concretas de evals (Promptfoo, Inspect, Langfuse, Braintrust…) ni su encaje con el Agent SDK.

## B1. Gemelo digital, progresión a hardware-in-the-loop y uso de agentes de IA en firmware

### Takeaway
Las herramientas de simulación embebida tienen integración CI madura (Renode + Robot Framework + GitHub Action; Wokwi CLI/CI) y Wokwi ofrece un servidor MCP experimental que lista Claude Code como cliente. Los testimonios de Claude Code en firmware son positivos con revisión humana y prueba en hardware real. No se encontraron fuentes sólidas sobre prácticas de gemelo digital específicas para startups pequeñas.

### Cited Findings
**Simulación y CI**
- Renode (Antmicro, open source): GitHub Action `renode-test-action` que ejecuta tests Robot en CI y guarda logs/informes; entorno determinista con modelos de cientos de bloques, SoCs y placas. — [Antmicro blog, 2024-10](https://antmicro.com/blog/2024/10/renode-github-action-for-automated-testing-in-simulation)
- Caso Google ChromeOS: simulación del módulo de huella FPMCU en Renode para probar firmware del EC en CI de forma determinista, evitando reflashear microcontroladores físicos para decenas de binarios. — [Google Open Source Blog, 2023-08](https://opensource.googleblog.com/2023/08/chromeos-ec-testing-suite-renode-for-consumer-products.html?m=0)
- Memfault usa Renode como emulador para tests de firmware en GitHub Actions (UART, SPI, I2C, GPIO…). — [Interrupt (Memfault)](https://interrupt.memfault.com/blog/test-automation-renode)
- Wokwi CLI incluye un **servidor MCP experimental** para que agentes ejecuten simulaciones, tests automáticos, lean la consola serie e interactúen con el hardware virtual; configuración con `wokwi-cli mcp` y `WOKWI_CLI_TOKEN`; lista Claude Code, Copilot, Cursor, Gemini y ChatGPT como clientes; «the API may change». — [Wokwi docs, MCP support](https://docs.wokwi.com/wokwi-ci/mcp-support); [wokwi-cli GitHub](https://github.com/wokwi/wokwi-cli)
- Wokwi para VS Code funciona con PlatformIO; requiere compilar el firmware antes de simular. — [Wokwi docs](https://docs.wokwi.com/vscode/getting-started)
- Secundario (calidad baja): Wokwi orientado a Arduino/ESP32/RP2040 con periféricos básicos y poca precisión temporal; Renode a Cortex-M/RISC-V con periféricos avanzados. — [industrialmonitordirect.com](https://industrialmonitordirect.com/blogs/knowledgebase/wokwi-vs-renode-vs-qemu-embedded-system-simulators-comparison)
- Comunidad (no oficial, sin validar): skills de PlatformIO para Claude Code; paquete `nff` que compila, flashea y devuelve la salida serie de ESP32/ESP8266/AVR por USB. — [mcpmarket PlatformIO skill](https://mcpmarket.com/tools/skills/platformio-embedded-development); [PyPI nff](https://pypi.org/project/nff/)

**Testimonios de Claude Code en hardware (opinión)**
- Jacob Beningo inicia la serie «Faster, Smarter Firmware with AI» defendiendo Claude Code para firmware. — [beningo.com](https://www.beningo.com/why-claude-code-for-firmware-development-matters/)
- Ingeniero construye un módulo de pulsador universal con Claude Code usando skills, agentes y un servidor MCP (incluido un comprobador MISRA C); «matched how I would have designed it—just significantly faster». — [Design News](https://www.designnews.com/embedded-systems/how-i-built-a-universal-push-button-module-using-claude-code)
- Snyk resume que en r/embedded el sentimiento pasó del escepticismo a una adopción medida: Claude para HAL y patrones de interrupciones, revisando cada línea. — [Snyk](https://snyk.io/fr/articles/claude-skills-embedded-systems-engineers/)
- Hilo de EEVblog (abr-2026) «Using Claude Code for embedded work» con experiencias de usuarios. — [EEVblog](https://www.eevblog.com/forum/microcontrollers/using-claude-code-for-embedded-work/msg6241157/)

### Inferences
- Progresión plausible para SmartColdBox: gemelo v4.0 en Python (planta + MPC, contratos JSON Schema) → firmware del controlador real ejecutado en simulador (Renode o Wokwi según MCU) contra la planta simulada → HIL con placa real y planta simulada → banco con hardware real. Los contratos JSON Schema ya existentes son la frontera natural para sustituir cada proceso simulado por el real.
- El servidor MCP de Wokwi y los scripts de CI de Renode permiten a Claude Code cerrar el bucle «editar firmware → simular → leer serie → corregir» sin hardware; es candidato a validar, no práctica asentada.

### Gaps
- No se encontraron fuentes fiables sobre prácticas de gemelo digital para startups pequeñas de hardware ni guías de progresión SIL→HIL específicas; tampoco sobre Claude Code con Renode en concreto.
- No se buscaron frameworks de simulación de planta (p. ej. FMI/FMU, Simulink, Modelica) ni su relación con un gemelo en Python.
- No se verificó el MCU previsto para SmartColdBox, del que depende la elección Wokwi/Renode.
