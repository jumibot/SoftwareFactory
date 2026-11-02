# Las tareas sin historial, con H y fuera de Cerradas

- **Origen:** SoftwareFactory, 2026-10-30, tarea 145. Lo propuso el subagente; el propietario lo aceptó.
- **Contexto:** el panel saca las letras, Cerradas y los commits del historial de cada tarea. Las tareas anteriores al CLI no lo tienen, o les falta la creación o el cierre.
- **Decisión:** una tarea sin el evento «creada» en la sesión lleva H. Una tarea sin evento de cierre en la sesión no entra en Cerradas. Una en Testing sin commits en su historial ni «… (N)» en `develop` no lleva D ni R. No se deduce lo que falta comparando colas.
- **Consecuencias:** el panel no necesita el código que comparaba colas. Afecta solo a tareas antiguas, como la 4 y la 47, y deja de afectarlas en cuanto el CLI apunta su cierre.
- **Aplicada en:** plugins/sf/hooks/panel.tsx, plugins/sf/hooks/lectura.ts y docs/como-funciona-el-panel.md.
