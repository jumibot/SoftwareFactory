# Claude Code, centro del trabajo de desarrollo

- **Origen:** SoftwareFactory, 2026-10-26.
- **Decisión:** Claude Code es el centro del desarrollo. Las piezas de la SF para la persona (tablero, daily, bandeja de decisiones, informes) se conectan a Claude Code con hooks, MCP o lo que haga falta, en lugar de usar una herramienta de orquestación aparte.
- **Consecuencias:** encaja con el plugin `sf` como vía para llevarlas a cada proyecto. La arquitectura de los agentes dentro de los productos no está cerrada; de momento se prototipa con Claude Code como orquestador.
