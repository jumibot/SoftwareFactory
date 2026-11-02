# Plantilla: escritorio con clean

Estructura de partida de la [metodología de la SF, 7.2](../../skills/metodologia/references/desarrollo-de-proyectos.md). Es una plantilla adaptable: se crea solo lo necesario, y las reglas que la acompañan están en la metodología.

Mantener estructura exterior, documentación y pruebas; organizar el paquete así:

```text
src/nombre_app/
├── main.py
├── bootstrap.py
├── domain/
├── application/
│   ├── use_cases/
│   └── ports/
├── presentation/
│   ├── views/
│   └── presenters/
├── infrastructure/
│   ├── persistence/
│   │   ├── repositories/
│   │   ├── queries/
│   │   └── migrations/
│   └── integrations/
└── resources/
```
