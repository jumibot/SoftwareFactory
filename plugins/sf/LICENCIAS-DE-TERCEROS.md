# Licencias de terceros

El plugin `sf` es obra propia de la Software Factory, con licencia MIT (`LICENSE`, en la raíz del repositorio). Algunas skills adaptan técnicas y estructuras de proyectos de terceros, y otras piezas usan software ajeno que no viaja en el plugin. Aquí está la atribución y la licencia de cada uno. La historia completa de cada pieza (qué se tomó, de qué versión, qué se cambió y por qué) está en el repositorio de la SF, en `docs/referencias/procedencia/`.

## Adaptado dentro del plugin

No se copia ningún archivo de estos proyectos: se toman estructuras, secciones y reglas, traducidas al español y adaptadas al método de la SF.

| Proyecto | Licencia | Copyright | Lo usa | Qué se toma |
| --- | --- | --- | --- | --- |
| [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD), commit `61e01f8` | MIT | Copyright (c) 2025 BMad Code, LLC | `definicion_tecnica`, `diseno_interfaz` | De `bmad-architecture`: el documento corto de arquitectura, la forma de las decisiones, convenciones, stack y estructura semilla, y la lista del revisor. De `bmad-ux`: las secciones del documento de experiencia, los bocetos de pantallas clave y la lista de cobertura. |
| [Spec Kit](https://github.com/github/spec-kit), commit `67e0f72` | MIT | Copyright GitHub, Inc. | `definicion_tecnica`, `diseno_interfaz` | Los campos del contexto técnico, la marca «NECESITA ACLARACIÓN», la tabla de complejidad y los escenarios «Dado / Cuando / Entonces». |
| [MADR](https://github.com/adr/madr) 4.0.0 | MIT o CC0-1.0, a elección; se usa bajo MIT | Copyright (c) 2017-2022 Oliver Kopp, Olaf Zimmermann | `definicion_tecnica` | Las secciones del registro de una decisión. |
| [Superpowers](https://github.com/obra/superpowers) | MIT | Copyright (c) 2025 Jesse Vincent | `diseno_interfaz` | Una pregunta cada vez, con propuesta. |

BMad™, BMad Method™ y BMad Core™ son marcas de BMad Code, LLC. Su mención aquí solo indica la procedencia y no implica respaldo.

`diseno_interfaz` toma además de Scott Hurff, «[Why your user interface is awkward: you're ignoring the UI stack](https://www.scotthurff.com/posts/why-your-user-interface-is-awkward-youre-ignoring-the-ui-stack/)», la idea de los estados de cada pantalla (ideal, vacío, cargando, parcial y error). Es una idea citada, no un texto copiado.

Texto de la licencia MIT, que se aplica a las partes adaptadas de esos proyectos, con el copyright de cada uno indicado en la tabla:

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Dependencias que no viajan en el plugin

Se instalan desde su propio repositorio, fijadas a un commit en el catálogo de la SF, y traen su propia licencia.

| Plugin | Repositorio | Licencia |
| --- | --- | --- |
| `gsap-skills` | [greensock/gsap-skills](https://github.com/greensock/gsap-skills), commit `aed9cfd` | MIT, Copyright (c) 2026 GreenSock |
| `threejs-skills` | [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills), commit `0e18186` | MIT, Copyright (c) 2026 CloudAI-X |
| `oklch-skill` | [jakubkrehel/oklch-skill](https://github.com/jakubkrehel/oklch-skill), commit `0e81f04` | MIT, Copyright (c) 2026 Jakub Krehel |

## Lo que se carga al usar los documentos

Los documentos e infografías que generan las skills cargan desde una CDN, al abrirse en el navegador:

- [three.js](https://github.com/mrdoob/three.js) (MIT, Copyright 2010-2025 three.js authors) y [es-module-shims](https://github.com/guybedford/es-module-shims) (MIT), en las infografías. `infografia_tecnica/scripts/empaquetar_autonomo.py` incrusta three.js en la versión sin red con su cabecera de licencia.
- Tipografías de Google Fonts, con su propia licencia (SIL Open Font License en las que usan los temas).

Los scripts de Python usan los paquetes `markdown` (BSD-3-Clause) y `Pillow` (MIT-CMU), que se instalan aparte.
