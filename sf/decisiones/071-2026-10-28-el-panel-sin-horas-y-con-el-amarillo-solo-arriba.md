# El panel, sin horas y con el amarillo solo arriba

- **Origen:** SoftwareFactory, 2026-10-28, al ver «· ahora» en la cabecera de Cerradas.
- **Decisión:** el panel no muestra horas ni antigüedades («ahora», «5 min», «3 h»): ni en la cabecera de Cerradas ni en sus filas. Y la tarea en curso va en amarillo solo arriba del panel; dentro de las secciones (Pendientes, Testing), su código, texto y paso en curso van como los demás. *Sustituida en parte el 2026-10-29: el código va en amarillo también en las secciones (ver «El código de la tarea en curso, en amarillo también en las secciones»).* El paso en curso no va en amarillo en ningún sitio, tampoco arriba.
- **Aplicada en:** `plugins/sf/hooks/panel.tsx` y `lectura.ts`; `docs/como-funciona-la-software-factory.md`.
