# Una tarea reabierta lleva H

- **Origen:** SoftwareFactory, 2026-10-28. Al partir la prueba del panel (76), una tarea reabierta volvía a Cerradas con la letra A, como si fuera nueva.
- **Decisión:** una tarea reabierta no es nueva: lleva H, en rojo, aunque haya entrado en la sesión.
- **Precisada por:** «Números de tarea en tres columnas, apartados con 0 y rojo solo para las reabiertas» (159): la H ya no va en rojo; el rojo marca la reabierta como fondo del número.
- **Aplicada en:** `plugins/sf/hooks/cola.ts`; `docs/como-funciona-la-software-factory.md`.
