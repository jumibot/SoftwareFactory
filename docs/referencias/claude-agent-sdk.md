# Claude Agent SDK para Python

Datos de la documentación oficial que pesan en las aplicaciones con un agente de Claude Code dentro. Verificados el 2026-10-25; sin reverificar desde entonces.

## Paquete y opciones

- Paquete `claude-agent-sdk`, Python 3.10 o superior, con `query()` y `ClaudeSDKClient`. Incluye el binario de Claude Code, salvo en Windows ARM64, donde va aparte. No lee `.env`.
- `ClaudeAgentOptions`: `system_prompt`, `allowed_tools`, `disallowed_tools`, `permission_mode`, `cwd`, `max_turns`, `model`, `setting_sources` (por omisión carga `user`, `project` y `local`), `hooks`, `mcp_servers` y `output_format` (con `json_schema`, el resultado llega en `structured_output`).
- También `env`, un diccionario que se mezcla sobre el entorno heredado (no sirve para quitar variables), `cli_path` y `extra_args`.

## Skills

Las skills se buscan en `<cwd>/.claude/skills/`, subiendo hasta la raíz del repositorio, y solo si `setting_sources` incluye `"project"`. Por eso el agente de un producto se ejecuta fuera del repositorio de desarrollo: si no, cargaría las skills de desarrollo.

## Credenciales

- Un producto de terceros no puede usar el inicio de sesión de claude.ai sin aprobación previa: necesita clave de API, o Bedrock, Vertex o Foundry.
- Orden en que Claude Code toma la credencial: proveedor en la nube, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_API_KEY`, `apiKeyHelper`, `CLAUDE_CODE_OAUTH_TOKEN` (la suscripción, con el token que genera `claude setup-token`, válido un año), perfiles y `/login`.
- El modo `--bare` no lee `CLAUDE_CODE_OAUTH_TOKEN`.

## Fuentes

- [Agent SDK: visión general](https://code.claude.com/docs/en/agent-sdk/overview.md)
- [Agent SDK para Python](https://code.claude.com/docs/en/agent-sdk/python.md)
- [Skills en el Agent SDK](https://code.claude.com/docs/en/agent-sdk/skills.md)
- [Hooks en el Agent SDK](https://code.claude.com/docs/en/agent-sdk/hooks.md)
- [Herramientas propias en el Agent SDK](https://code.claude.com/docs/en/agent-sdk/custom-tools.md)
- [Uso sin interfaz](https://code.claude.com/docs/en/headless.md)
- [Autenticación](https://code.claude.com/docs/en/authentication.md)
