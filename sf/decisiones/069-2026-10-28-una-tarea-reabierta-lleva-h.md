# Una tarea reabierta lleva H

Estado: deprecada el 2026-11-25 por «El número de una tarea lleva el color de su estado, y una reabierta cuenta como H» (373); lo demás, por «Números de tarea en tres columnas, apartados con 0 y rojo solo para las reabiertas» (159).

- **Origen:** SoftwareFactory, 2026-10-28. Al partir la prueba del panel (76), una tarea reabierta volvía a Cerradas con la letra A, como si fuera nueva.
- **Decisión:** una tarea reabierta no es nueva: lleva H, en rojo, aunque haya entrado en la sesión.
- **Aplicada en:** lo vigente, en el panel (`plugins/sf/hooks/panel.tsx`).
