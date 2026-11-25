# La incorporación crea docs/propuestas.md; el índice de decisiones sale del panel

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Simplificar la SF: sin registro ni mejoras desde otros proyectos» (282). El propietario elige las dos opciones recomendadas.
- **Contexto:** con la decisión 194, cada proyecto guarda sus propuestas en su `docs/propuestas.md` y el panel las muestra en PROYECTO · Propuestas, pero solo si el archivo existe. Al quitar la sección Documentos (195), también se fue el clic que generaba y abría el índice de decisiones en HTML.
- **Decisión:**
  1. `sf:incorporar_proyecto_a_sf` crea `docs/propuestas.md` con su «## Propuestas pendientes» vacía, en proyectos nuevos y al actualizar uno que no lo tenga.
  2. El índice de decisiones en HTML no vuelve al panel: se genera a mano con `indice_decisiones.py` si hace falta (KISS).
- **Consecuencias:** todo proyecto incorporado tiene dónde anotar sus propuestas y su sección en el panel.
- **Aplicada en:** `sf:incorporar_proyecto_a_sf` (crea `sf/propuestas.md` desde `templates/propuestas.md`) y sus pruebas; «Cómo funciona la Software Factory», «Incorporación de un proyecto a la SF».
