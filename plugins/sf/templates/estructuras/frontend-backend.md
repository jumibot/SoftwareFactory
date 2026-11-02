# Plantilla: frontend y backend separados

Estructura de partida de la [metodología de la SF, 7.3](../../skills/metodologia/references/desarrollo-de-proyectos.md). Es una plantilla adaptable: se crea solo lo necesario, y las reglas que la acompañan están en la metodología.

```text
proyecto/
├── CLAUDE.md
├── docs/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── features/
│   │   └── shared/
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   └── package.json
├── backend/
│   ├── src/
│   │   └── nombre_api/
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   └── pyproject.toml
├── tests/
│   └── acceptance/
└── reports/
    └── tests/
```

Variante sencilla del backend:

```text
nombre_api/
├── main.py
├── api/
│   ├── routers/
│   └── schemas/
├── services/
├── model/
└── persistence/
    ├── repositories/
    ├── queries/
    └── migrations/
```

MVP no prescribe la estructura del servidor. En React, componentes y hooks presentadores pueden separar vista y coordinación por funcionalidad:

```text
frontend/src/features/registros/
├── components/
├── useRegistrosPresenter.ts
├── registrosApi.ts
└── types.ts
```

Variante Clean del backend:

```text
nombre_api/
├── main.py
├── bootstrap.py
├── domain/
├── application/
│   ├── use_cases/
│   └── ports/
├── presentation/
│   └── api/
│       ├── routers/
│       └── schemas/
└── infrastructure/
    ├── persistence/
    │   ├── repositories/
    │   ├── queries/
    │   └── migrations/
    └── integrations/
```
