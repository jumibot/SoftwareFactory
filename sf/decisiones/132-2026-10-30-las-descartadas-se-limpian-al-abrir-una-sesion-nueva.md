# Las descartadas se limpian al abrir una sesión nueva

- **Origen:** SoftwareFactory, 2026-10-30, tarea 145. Lo propuso el subagente; el propietario lo aceptó.
- **Contexto:** el panel saca de la cola las descartadas que quedaron de otra sesión. Con `/reload-plugins` el mod arranca de nuevo, y limpiarlas entonces haría desaparecer las descartadas de la sesión en curso, que aún se ven en Cerradas.
- **Decisión:** el panel llama a `cola.py limpiar` solo al abrir una sesión nueva, no con `/reload-plugins`.
- **Consecuencias:** las descartadas de la sesión siguen en Cerradas hasta pulsar «limpiar» o abrir otra sesión.
- **Aplicada en:** plugins/sf/hooks/register.tsx, docs/como-funciona-el-panel.md y plugins/sf/skills/flujo_tareas/references/estados.md (25).
