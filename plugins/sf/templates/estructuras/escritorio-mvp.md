# Plantilla: escritorio con mvp

Estructura de partida de la [metodología de la SF, 7.1](../../skills/metodologia/references/desarrollo-de-proyectos.md). Es una plantilla adaptable: se crea solo lo necesario, y las reglas que la acompañan están en la metodología.

```text
proyecto/
├── CLAUDE.md
├── docs/
├── src/
│   └── nombre_app/
│       ├── main.py
│       ├── bootstrap.py
│       ├── presentation/
│       │   ├── views/
│       │   └── presenters/
│       ├── model/
│       ├── persistence/
│       │   ├── repositories/
│       │   ├── queries/
│       │   └── migrations/
│       └── resources/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── acceptance/
├── reports/
│   └── tests/
└── pyproject.toml
```
