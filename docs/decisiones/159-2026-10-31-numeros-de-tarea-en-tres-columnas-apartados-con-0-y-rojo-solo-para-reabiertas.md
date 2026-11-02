# Números de tarea en tres columnas, apartados con 0 y rojo solo para las reabiertas

- **Origen:** SoftwareFactory, 2026-10-31, tarea «Panel: números de tarea a tres columnas y apartados Pendientes y Testing visibles» (236). Mirando el panel de un proyecto con pocas tareas, el propietario: «me parece raro que los números de las tareas parezcan de dos columnas en lugar de tres y que no aparecen los apartados de pendientes ni testing»; «si es el mismo panel, ¿por qué formatea distintos los códigos de tareas?»; y «sigues usando el rojo para tareas de sesiones anteriores, pero ya te dije que solo deben marcar tareas reabiertas».
- **Contexto:** «Código de tarea más ligero: 74C» (066) hacía que los números de una cifra ocuparan dos y reservaba el rojo para lo que venía de sesiones anteriores. En la SF, con números de tres cifras, no se notaba. En un proyecto nuevo, los números quedaban en dos columnas y se desalineaban al pasar de 99. Pendientes y Testing desaparecían vacíos, igual que antes Cerradas, que ya se dejó visible con 0 porque parecía un fallo.
- **Decisión:**
  - Los números de tarea ocupan siempre tres columnas, alineados a la derecha, en todos los apartados: «  4», « 41», «236».
  - Pendientes y Testing se ven siempre, también con 0, como Cerradas.
  - El rojo marca solo las tareas reabiertas, no las que vienen de sesiones anteriores.
- **Consecuencias:** precisa «Código de tarea más ligero: 74C» (066) en el ancho de los números y en el significado del rojo, y amplía a Pendientes y Testing lo que ya valía para Cerradas.
- **Aplicada en:** pendiente en el panel (tarea 236) y en «Cómo funciona el panel».
