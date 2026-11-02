# Ayudas de prueba: tras activar la rama y no obligatorias para cerrar

- **Origen:** SoftwareFactory, 2026-11-01, tras probar la 240 con una pregunta que Claude preparó como paso. El propietario: «Es genial que me ayudes en las pruebas. Planifícame siempre que puedas ayudas o un plan de pasos, pero ponlos después de la activación de la rama y que no sean obligatorios para cerrar la tarea».
- **Contexto:** el paso de prueba que Claude añadió a la 240 quedó antes de los pasos de cierre y, pendiente, impedía que el panel ofreciera Cerrar; el propietario no sabía cómo cerrarla.
- **Decisión:** al dejar una tarea lista para probar, Claude planifica, siempre que pueda, ayudas o un plan de pasos para la prueba. Van detrás de «Activar rama para poder probar» y no son obligatorios para cerrar: Cerrar no los exige, y añadirlos no devuelve «Activar rama» a pendiente. Si son pasos que hace Claude, los hace cuando el propietario activa la rama.
- **Consecuencias:** la orquestación no bloquea el cierre: el propietario puede cerrar la tarea en cualquier momento. Precisa la decisión 174 (pasos de cierre y paso que devuelve «Activar rama» a pendiente).
- **Aplicada en:** `cola.py` (`paso añadir --prueba`), el panel (con «(opcional)», fuera de la cuenta y sin exigirlas para la C), `sf:flujo_tareas` y `sf:orquestacion` (tarea 266).
