# Las comprobaciones y pruebas hechas se anotan como pasos de su tarea

Fecha: 2026-11-05. Decidida por el propietario de la Software Factory.

- Cada comprobación y cada prueba que se hace en una tarea (las pruebas automáticas, la validación del plugin, una revisión en el navegador, una prueba a mano) se anota como paso hecho de esa tarea, con lo que se comprobó y su resultado, por ejemplo «Comprobado: 300 pruebas de Python y validación del plugin, sin fallos».
- Lo que no se ha podido comprobar se dice en la tarea como no comprobado, no se calla.
- Una sola orden añade el paso de comprobación ya hecho, sin devolver a pendiente «Activar rama para poder probar»: anotarlo después de la prueba del propietario no le obliga a probar otra vez.
- Se retira el campo «comprobado» de la tarea: lo comprobado vive solo en los pasos, que son lo que el propietario ve en el panel.

Porqué: el propietario quiere saber, mirando la tarea en el panel, qué se ha comprobado de verdad, sin tener que buscarlo en los informes ni fiarse de un resumen. Con una orden y un solo sitio, cuesta menos y no hay dos versiones.

Aplicada en: pendiente, tarea «Que Claude cierre con cambios, comprobaciones y pendientes reales…» (340).
