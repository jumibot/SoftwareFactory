# Plantilla: scripts sql de creación y modificación

Estructura de partida de la [metodología de la SF, 7.5](../../skills/metodologia/references/desarrollo-de-proyectos.md). Es una plantilla adaptable: se crea solo lo necesario, y las reglas que la acompañan están en la metodología.

```text
persistence/
├── connection.py
├── repositories/
├── queries/
└── migrations/
    ├── 20261025_153000_crear_esquema_inicial.sql
    └── 20261026_100000_anadir_estado_a_registros.sql
```
