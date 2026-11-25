# El número de una tarea lleva el color de su estado, y una reabierta cuenta como H

En el panel, el número de una tarea va sin letra detrás: la letra de su estado (A, H, O, C o D) solo le da el color. El número va subrayado cuando la tarea se despliega.

Una tarea reabierta no es nueva: cuenta como H, aunque haya entrado en la sesión.

El ancho de los números y el rojo de las reabiertas, en «Números de tarea en tres columnas, apartados con 0 y rojo solo para las reabiertas» (159).

Recoge lo que sigue valiendo de «Código de tarea más ligero: 74C» (066) y «Una tarea reabierta lleva H» (069), que quedan deprecadas.

Porqué: los códigos de tarea pesaban a la vista; primero se quitó el guion y después la letra, que quedó solo como color (propietario de la Software Factory, 2026-10-28 y 2026-10-31). Una reabierta volvía con A, como si fuera nueva (069).

Aplicada en: el panel (`plugins/sf/hooks/panel.tsx`) y sus pruebas.
