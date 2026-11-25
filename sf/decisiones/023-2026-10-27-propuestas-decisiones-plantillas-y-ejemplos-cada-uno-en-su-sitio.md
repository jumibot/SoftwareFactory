# Propuestas, decisiones, plantillas y ejemplos, cada uno en su sitio

**Sustituida en parte** el 2026-10-29 por «Una decisión por archivo, en `docs/decisiones/`»: las decisiones van en la carpeta `docs/decisiones/`, un archivo por decisión, y no en un solo `docs/decisiones.md`.

- **Origen:** SoftwareFactory, 2026-10-27. El propietario preguntó cómo y dónde documentar los cambios y decisiones de la SF y dónde están las reglas vigentes. Respuestas: «ok a separar propuestas de decisiones en dos docs distintos» y «sí, adelante con la separación y unifica criterios».
- **Contexto:** `docs/mejora-continua.md` mezclaba propuestas, decisiones e historia (más de 440 líneas). La metodología y la especificación mezclaban acuerdos con «ejemplos» que en realidad eran de tres tipos: ilustraciones, plantillas y propuestas con forma de ejemplo.
- **Opciones:** un archivo por decisión en `docs/decisiones/` (lo que la metodología pedía a los proyectos) o un solo documento de decisiones.
- **Decisión:**
  - Dos documentos: `docs/propuestas.md` (lo pendiente y lo descartado) y `docs/decisiones.md` (lo decidido, con su porqué). `mejora-continua.md` desaparece.
  - Mismo criterio en todos los proyectos: un `docs/decisiones.md` en lugar de la carpeta `docs/decisiones/`.
  - Las **ilustraciones** se quedan junto a su regla, empezando por «Ejemplo:».
  - Las **plantillas** (estructuras de código) pasan al plugin, `plugins/sf/templates/`, y el documento conserva la regla y un enlace.
  - Las **propuestas con forma de ejemplo** pasan a `propuestas.md`.
- **Consecuencias:** en la metodología y la especificación quedan acuerdos, preferencias y pendientes. Cambian la skill `definicion_tecnica`, su plantilla de decisión y `diseno_interfaz`. Los proyectos que ya tienen otro registro (SmartColdBox, `docs/decisiones-y-pendientes.md`) se adaptan cuando se trabaje en ellos.
- **Aplicada en:** este documento, `propuestas.md`, metodología («Cómo interpretar», 4, 6 y 7), especificación («Cómo interpretar», 1, 2 y 4), `CLAUDE.md`, plugin `sf` 0.4.0.
