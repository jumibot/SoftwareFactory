# Sin registro ni mejoras de la SF desde otros proyectos

- **Origen:** SoftwareFactory, 2026-11-01. El propietario simplifica la SF: «No se registran items ni mejoras en la sf desde otros proyectos. Las mejoras las convertimos en propuestas, pero del proyecto en curso. Así desaparece la sección de sf enhance. Me aplico KISS».
- **Contexto:** desde cualquier proyecto, Claude anotaba en el registro común de la SF (`.sf/registro.json`, con `registro.py`) y escribía mejoras en `docs/propuestas.md` de la SF. El mod lo permitía como excepción a «un proyecto por sesión», y el panel lo mostraba en el bloque SF ENHANCE (Registro y Mejoras). Eso traía excepciones, commits cruzados entre repositorios (276) y reglas extra.
- **Decisión:**
  1. Ningún proyecto escribe en la SF: ni registro ni mejoras.
  2. Una mejora detectada en un proyecto se convierte en propuesta de ese mismo proyecto, en su `docs/propuestas.md`.
  3. Desaparece el bloque SF ENHANCE del panel y el registro de uso de la SF.
- **Consecuencias:** sin excepciones en el control de escritura, sin `registro.py` ni `.sf/registro.json` y sin commits en la SF desde otros proyectos. Las mejoras de la SF que salgan en otro proyecto quedan como propuestas de ese proyecto; llevarlas a la SF es cosa del propietario, en una sesión de la SF. Sustituye a la decisión 192 y deja sin efecto, en lo que toca al registro y a las mejoras desde otros proyectos, las 032, 104 y 146 y la regla de asociar al proyecto SoftwareFactory las mejoras detectadas en otros proyectos.
- **Corregida por:** «Un proyecto solo anota propuestas suyas» (210): las mejoras de la SF no se anotan en el proyecto; se dicen en una línea.
- **Aplicada en:** pendiente: el mod, `cola.py`, `registro.py`, las skills, la metodología, la plantilla y el CLAUDE.md, y los «Cómo funciona…».
