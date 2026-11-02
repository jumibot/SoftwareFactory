# Origen de la skill `definicion_tecnica`

- **Tipo:** skill propia de la SF, escrita el 2026-10-25 como capa fina sobre técnicas de terceros.
- **Motivo:** criterio del propietario del 2026-10-25: la SF define el método y reutiliza las técnicas; en la definición técnica, «ver qué aprovechamos y qué customizamos». Propuesta «Método propio, técnicas reutilizadas» de `docs/mejora-continua.md`, aprobada ese día.
- **Validación:** ninguna todavía. Está previsto probarla con LecturaFàcil, después de su interfaz.

## Qué es de la SF y qué se reutiliza

- **De la SF (sin equivalente en las fuentes):** partir del perfil favorito y justificar excepciones; capacidades opcionales; estructuras MVP y Clean; SQL nativo con migraciones; Claude Code como componente; brain de desarrollo y KB operativa; instalación en un paso; nombres descriptivos sin códigos; aprobación del propietario.
- **Reutilizado y adaptado:** ver la tabla.

| Fuente | Qué se toma | Qué se deja |
| --- | --- | --- |
| BMAD Method, skill `bmad-architecture` (`SKILL.md`, `assets/spine-template.md`, `references/reviewer-gate.md`), commit `61e01f82644c4bb533750cfa0d6d61ab61d2cc9b` de https://github.com/bmad-code-org/BMAD-METHOD | El documento corto que fija solo lo que evita que las partes diverjan, con su criterio de inclusión. Decisiones con *a qué obliga / qué evita / regla* y diagrama de dependencias. Convenciones, stack con versión verificada, estructura semilla (manda el código cuando existe), mapa capacidad → arquitectura y «Aplazado». Ratificar lo existente en un proyecto con código. Modos guiado y rápido. La lista de comprobación del revisor. | Su infraestructura (scripts `uv`, `_bmad/`, memlog, tickets, la PO «Sofia», `lint_spine.py`), los identificadores `AD-n`, la jerarquía iniciativa / epic y los revisores obligatorios. El porqué no va a un memlog sino a `docs/decisiones.md` (hasta el 2026-10-27, una carpeta `docs/decisiones/` con un archivo por decisión). |
| BMAD Method, «Theory of project context», https://docs.bmad-method.org/existing-codebases/theory-of-project-context/ | La disciplina para el `CLAUDE.md`: mínimo, sin arquitectura, igual o más corto en cada revisión. | — |
| Spec Kit, `templates/plan-template.md`, commit `67e0f7294e6e728ab60bf7b4590deb470448bc2d` de https://github.com/github/spec-kit | Los campos del contexto técnico y la marca `NEEDS CLARIFICATION` («NECESITA ACLARACIÓN»). La tabla de complejidad para justificar excepciones. | El plan por funcionalidad y rama, la constitución como documento aparte y los comandos. La SF hace la definición técnica una vez por proyecto; el plan por funcionalidad de Spec Kit se parece más a la preparación de cada devslice. |
| MADR 4.0.0, `template/adr-template-minimal.md`, https://github.com/adr/madr | Las secciones de la decisión: contexto y problema, opciones, decisión con porqué, consecuencias. | La numeración `NNNN-` de los archivos (la SF usa nombres descriptivos). |

Fuentes consultadas el 2026-10-25. Las copias leídas no se guardan en el repositorio.

## Licencias y avisos

BMAD Method — MIT License. Copyright (c) 2025 BMad Code, LLC. BMad™, BMad Method™ y BMad Core™ son marcas de BMad Code, LLC; su mención aquí solo indica la procedencia.

Spec Kit — MIT License. Copyright GitHub, Inc.

MADR — doble licencia MIT o CC0-1.0, a elección; la SF la usa bajo MIT.

Texto de la licencia MIT, que se aplica a las partes adaptadas de esos proyectos:

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Pendiente

- Probarla en LecturaFàcil y ajustar con lo aprendido.
- Revisar las fuentes cuando cambien (BMAD v7 está en alfa).

## Un solo documento de decisiones (2026-10-27)

Por decisión del propietario («separar propuestas de decisiones en dos docs distintos… unifica criterios»), las decisiones de cada proyecto van en un solo `docs/decisiones.md`, una sección por decisión y la más reciente arriba, igual que las de la propia SF. Cambiados `SKILL.md` (salida, paso 6 y lista de comprobación), `assets/plantilla-decision.md` (pasa a ser una sección) y el enlace «Porqué» de `assets/plantilla-definicion-tecnica.md`. El formato MADR mínimo no cambia.

## Una decisión por archivo (2026-10-29)

Por decisión del propietario («prefiero que cada decisión se convierta en un md distinto y crear una carpeta de decisiones»), las decisiones vuelven a una carpeta, `docs/decisiones/`, un archivo por decisión, con un índice generado por `tools/indice_decisiones.py`. Motivo: el archivo único chocaba en cada squash. Cambiados `SKILL.md` (salida, paso 6 y lista de comprobación), `assets/plantilla-decision.md` (vuelve a ser un archivo, con `#` y `##`) y el enlace «Porqué» de `assets/plantilla-definicion-tecnica.md`.
