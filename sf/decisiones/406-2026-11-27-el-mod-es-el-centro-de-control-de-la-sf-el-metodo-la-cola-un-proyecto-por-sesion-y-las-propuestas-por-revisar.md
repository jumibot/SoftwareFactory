# El mod es el centro de control de la SF: el método, la cola, un proyecto por sesión y las propuestas por revisar

El mod de la SF lleva el control del proyecto: enseña el estado del método y la cola de tareas, controla «Un proyecto por sesión» y sigue las propuestas del proyecto. Las de su `sf/propuestas.md` que esperan revisión («pendiente de aprobación» o «pendiente de decisión» en su «Estado») se cuentan en la caja sobre el prompt y se listan en la sección Propuestas del panel (197). Una responsabilidad nueva de control de la SF se plantea primero en el mod.

Cada proyecto sigue solo sus propuestas: desde otro proyecto no se registra nada en la SF (401).

Recoge lo que sigue valiendo de «El mod, centro de control de la SF: realimentación» (032), que queda deprecada.

Porqué: las propuestas se acumulaban sin una vista de cuántas esperaban revisión. El propietario de la Software Factory: «sí, aprueba e implementa la realimentación en el mod. El mod va tomando responsabilidades como centro de control de la sf» (032).

Aplicada en: `plugins/sf/hooks/control.ts`, `lectura.ts` (`leerRealimentacion`) y `panel.tsx` (caja sobre el prompt y sección Propuestas), y sus pruebas.
