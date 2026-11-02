# Plantilla: Perfil: escritorio Python con MVP y agente Claude Code

Estructura de partida de la [metodología de la SF, 7.7](../../skills/metodologia/references/desarrollo-de-proyectos.md). Es una plantilla adaptable: se crea solo lo necesario, y las reglas que la acompañan están en la metodología.

**Estructura:** la de 7.1, con dos añadidos:

```text
proyecto/
├── agent-runtime/          # instrucciones, skills, hooks y validadores del agente del producto
└── src/nombre_app/
    └── agent/
        ├── port.py         # interfaz que usan los presentadores y el modelo
        ├── claude_adapter.py
        └── fake_agent.py   # agente simulado para pruebas y desarrollo
```
