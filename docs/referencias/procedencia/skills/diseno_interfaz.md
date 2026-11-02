# Origen de la skill `diseno_interfaz`

- **Tipo:** skill propia de la SF, escrita el 2026-10-25 como capa fina sobre técnicas de terceros.
- **Motivo:** criterio del propietario del 2026-10-25: la SF define el método y reutiliza las técnicas. El propietario no tenía skill de interfaz y quiere definirla en detalle antes de implementar. Propuesta «Método propio, técnicas reutilizadas» de `docs/mejora-continua.md`, aprobada ese día.
- **Validación:** ninguna todavía. Está previsto probarla con la pantalla de revisión de LecturaFàcil.

## Técnicas tomadas

No se copia ningún archivo. Se toman estructuras y reglas, traducidas y adaptadas al método de la SF.

| Fuente | Qué se toma | Qué se deja |
| --- | --- | --- |
| BMAD Method, skill `bmad-ux` (`SKILL.md`, `assets/key-screens.md`, `references/validate.md`, `assets/experience-example-shadcn.md`), commit `61e01f82644c4bb533750cfa0d6d61ab61d2cc9b` de https://github.com/bmad-code-org/BMAD-METHOD | Las secciones del documento de experiencia (fundamento, inventario de pantallas «se llega desde / para qué», textos y tono, componentes por comportamiento, estados, interacción, accesibilidad mínima, recorridos con protagonista y momento clave). El cierre de superficies. Los bocetos de 2-4 pantallas clave en HTML sin JS ni red, con contenido real, y «la especificación manda». La lista de comprobación de cobertura. Los modos guiado y rápido con supuestos marcados. | Su infraestructura (scripts `uv`, `_bmad/`, memlog, tickets, iniciativas, modo *party*), el documento visual `DESIGN.md` y los revisores en paralelo obligatorios. |
| Spec Kit, `templates/spec-template.md`, commit `67e0f7294e6e728ab60bf7b4590deb470448bc2d` de https://github.com/github/spec-kit | Los escenarios de aceptación *Given / When / Then* («Dado / Cuando / Entonces»). | Sus identificadores (`FR-001`, prioridades P1…), la rama por funcionalidad y el comando `/specify`. |
| Scott Hurff, «Why your user interface is awkward: you're ignoring the UI stack», https://www.scotthurff.com/posts/why-your-user-interface-is-awkward-youre-ignoring-the-ui-stack/ | Los estados por pantalla: ideal, vacío, cargando, parcial y error. La SF añade «sin permiso» (metodología, 3.2). | — |
| Superpowers, skill `brainstorming`, https://github.com/obra/superpowers | Una pregunta cada vez, con propuesta. | Su flujo obligatorio hacia `writing-plans`. |

Fuentes consultadas el 2026-10-25. Las copias leídas no se guardan en el repositorio.

## Licencias y avisos

BMAD Method — MIT License. Copyright (c) 2025 BMad Code, LLC. BMad™, BMad Method™ y BMad Core™ son marcas de BMad Code, LLC; su mención aquí solo indica la procedencia.

Spec Kit — MIT License. Copyright GitHub, Inc.

Superpowers — MIT License (Jesse Vincent).

Texto de la licencia MIT, que se aplica a las partes adaptadas de esos proyectos:

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Pendiente

- Probarla en LecturaFàcil y ajustar con lo aprendido.
- Revisar las fuentes cuando cambien (BMAD v7 está en alfa) y decidir si se incorpora algo nuevo.
