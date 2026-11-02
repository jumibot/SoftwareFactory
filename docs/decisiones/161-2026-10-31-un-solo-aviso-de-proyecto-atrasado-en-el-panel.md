# Un solo aviso de proyecto atrasado en el panel

- **Origen:** SoftwareFactory, 2026-10-31, tarea «El panel avisa dos veces de que el proyecto no está al día con la SF» (189), vista en SmartColdBox y sprite_animation. El propietario, al ver el arreglo propuesto: «mantenla».
- **Contexto:** en un proyecto incorporado con una SF anterior, el panel lateral decía lo mismo dos veces: la línea gris «SF 1.1.0 → 1.2.2 · 1/7 Visión» y el aviso amarillo «incorporado con la SF 1.1.0; va por la 1.2.2: pide a Claude «pon el proyecto al día con la SF»».
- **Decisión:** en el panel lateral, la línea gris da solo la versión con que se incorporó el proyecto, «SF 1.1.0 · 1/7 Visión», sin «→»; el aviso amarillo, que dice qué hacer, es el único aviso. La caja pequeña sobre el prompt, que no tiene aviso amarillo, conserva «SF 1.1.0 → 1.2.2».
- **Consecuencias:** precisa «El panel avisa si el proyecto va por detrás de la SF» (070), que mostraba las dos cosas.
- **Aplicada en:** `plugins/sf/hooks/panel.tsx` y sus pruebas (189).
