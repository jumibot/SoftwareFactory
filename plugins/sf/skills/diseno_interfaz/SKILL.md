---
name: diseno_interfaz
user-invocable: false
description: Define en detalle la interfaz de un proyecto antes de implementarla y antes de elegir tecnología — recorridos con protagonista, inventario de pantallas, matriz pantalla × estado (ideal, vacío, cargando, parcial, error, sin permiso), comportamiento de componentes, interacción, textos, accesibilidad mínima, bocetos estáticos de las pantallas clave y criterios de aceptación «Dado / Cuando / Entonces». Úsala cuando pidan diseñar o especificar la interfaz, las pantallas, la experiencia de usuario o los estados de una aplicación de escritorio, web o móvil, como parte de la especificación funcional de la Software Factory.
---

# Diseño de interfaz

Esta skill es una **capa fina de la Software Factory (SF)**: el método es de la SF y la técnica se reutiliza de otros (atribución y licencias en `LICENCIAS-DE-TERCEROS.md`, en la raíz del plugin; la historia, en la [procedencia de las piezas](https://github.com/jumibot/SoftwareFactory/blob/main/docs/referencias/procedencia/README.md)). Produce la especificación de la interfaz de un proyecto **antes de elegir la tecnología** y antes de implementar nada, como parte de la especificación funcional global (metodología, 3.2).

No contiene nada de ningún proyecto. Lo propio de cada uno está en sus documentos (`docs/`) y en su identidad (`docs/identidad/`).

## Qué produce

- `docs/specs/funcional/interfaz.md`, con la forma de `assets/plantilla-interfaz.md`.
- `docs/specs/funcional/bocetos/`, con 2-4 bocetos estáticos de las pantallas clave.
- Las decisiones duraderas que surjan, en `sf/decisiones/`, una por archivo (formato de la skill `definicion_tecnica`).

La especificación es el contrato; los bocetos ilustran. Si chocan, manda la especificación.

## Reglas de la SF

- **Antes de la técnica.** No se eligen tecnologías ni librerías. Sí se fija la **forma** (escritorio, web, móvil o varias), porque condiciona la interfaz.
- **Sale de la especificación funcional.** Cada pantalla responde a funcionalidades y recorridos ya acordados, o a una pregunta nueva para el propietario.
- **Preguntar, no inventar.** Una pregunta cada vez, con una propuesta concreta cuando ayude. Lo que no está decidido se marca `[SUPUESTO]` y se convierte en pregunta; nunca pasa al documento como decisión.
- **Complejidad proporcionada.** Tantas pantallas, estados y bocetos como el proyecto necesite; ni uno más. Sin medidas en píxeles ni detalle visual que no decida nada.
- **Nombres descriptivos** para pantallas, componentes y criterios. Nunca códigos como `P01` o `CA-3`.
- **Idioma del usuario final** en textos, tono y ejemplos.
- **Diagramas en SVG** (metodología, 6): el mapa de pantallas, los recorridos y cualquier otro esquema van como SVG inline en el `.md`, con las recomendaciones de `../metodologia/references/diagramas-svg.md` (vertical, 560 de ancho). Nunca en ASCII ni en mermaid.
- **Aprobación del propietario** antes de dar la interfaz por cerrada.

## Modos

- **Guiado** (por defecto): se recorre cada paso con el propietario y se decide con él.
- **Rápido:** se redacta todo de una vez con `[SUPUESTO]` en lo no confirmado y se repasa al final. Solo si el propietario lo pide.

## Procedimiento

1. **Leer** la visión, la especificación funcional, las referencias, la identidad del proyecto y lo que ya exista de interfaz (bocetos, capturas, notas). No preguntar lo que ya está escrito.
2. **Forma y fundamento.** Confirmar la forma (escritorio, web, móvil) y, si existe, el sistema de componentes que se hereda. En escritorio, si la plataforma aún no está elegida, describir en términos neutros (ventana, panel, diálogo, lista).
3. **Recorridos clave.** Para cada funcionalidad importante, un recorrido real con **protagonista con nombre** (preferentemente el caso conductor de la visión), pasos numerados, el **momento clave** (cuando el usuario obtiene lo que buscaba) y el **camino de fallo** cuando proceda. Los nombres de recorridos y funcionalidades se copian literalmente de la especificación funcional.
4. **Inventario de pantallas.** Tabla *Pantalla · Se llega desde · Para qué*. Comprobar el **cierre**: cada necesidad tiene una pantalla que la cumple y cada pantalla tiene un recorrido que llega a ella. Si falla, preguntar; no inventar la pieza que falta. Anotar las reglas de navegación (por ejemplo, un solo nivel de diálogos modales).
5. **Matriz pantalla × estado.** Para cada pantalla, los estados que procedan: **ideal, vacío, cargando, parcial, error y sin permiso**, más los propios del producto (por ejemplo, «agente trabajando»). Para cada celda, el tratamiento: qué ve y qué puede hacer el usuario. Las celdas que no aplican se marcan «no aplica» con su motivo.
6. **Comportamiento.**
   - **Componentes:** tabla *Componente · Dónde · Reglas de comportamiento* (qué hace al pulsar, al editar, al fallar). El aspecto visual no va aquí.
   - **Interacción:** teclado y atajos, foco y orden de tabulación, ratón o toque, lo que está prohibido.
   - **Textos y tono:** pares *Sí · No* con frases reales en el idioma del usuario.
   - **Accesibilidad mínima:** el nivel exigido y cómo se cumple en el comportamiento (lectores de pantalla, teclado, tamaños de texto, tiempos).
7. **Bocetos.** De 2 a 4 pantallas clave: la de entrada, la que más decide del recorrido principal y algún diálogo o estado alternativo importante. Cada boceto es un **HTML autocontenido** (CSS en línea, fuentes del sistema, sin JavaScript ni red) o un **SVG**, con contenido real del caso (nunca *lorem ipsum*), un estado canónico y, si importa, un estado alternativo al lado. Al principio de cada boceto, un comentario con las secciones de la especificación que ilustra. No introducir componentes ni textos que no estén en la especificación.
8. **Traducción a la plataforma.** Una nota breve por boceto sobre cómo se construiría en la forma elegida: en escritorio, ventanas, paneles, diálogos, atajos y foco; en web, rutas y componentes. Sin elegir librerías: eso es de la definición técnica.
9. **Criterios de aceptación.** Para cada recorrido y para cada celda de la matriz que lo merezca, un criterio con **nombre descriptivo** y uno o varios escenarios **Dado / Cuando / Entonces**. Estos criterios alimentan la preparación de cada devslice (metodología, 3.5) y sus pruebas (metodología, 8).
10. **Revisión.** Antes de entregar, recorrer la lista de comprobación. Para una interfaz grande o crítica, ofrecer una revisión independiente con un subagente que solo lea el documento y busque huecos.
11. **Entrega.** Resumir qué se ha definido, qué queda como `[SUPUESTO]` o pregunta y qué conviene que valide un usuario real. Pedir la aprobación del propietario.

## Lista de comprobación

- [ ] Cada recorrido de la especificación funcional tiene su recorrido aquí, con protagonista, pasos, momento clave y camino de fallo si procede.
- [ ] Cierre: cada necesidad tiene pantalla y cada pantalla tiene recorrido.
- [ ] Cada pantalla tiene sus estados; las celdas vacías están justificadas.
- [ ] Cada componente nombrado en cualquier sección tiene su fila de comportamiento, con reglas reales, no una palabra.
- [ ] Cada boceto está enlazado desde la sección que ilustra y dice qué ilustra; se indica una vez que manda la especificación.
- [ ] Los nombres (pantallas, componentes, recorridos) son idénticos en todas las secciones y coinciden con la especificación funcional.
- [ ] Cada recorrido tiene al menos un criterio «Dado / Cuando / Entonces».
- [ ] No hay tecnologías ni librerías elegidas, ni detalle visual que no decida nada, ni copia de la especificación funcional.
- [ ] Los `[SUPUESTO]` están listados como preguntas para el propietario.

## Aspecto visual

Esta skill define cómo **funciona** la interfaz. El aspecto (colores, tipografía, espaciado) se decide después, con la identidad del proyecto y la tecnología elegida. En proyectos web, la skill `frontend-design` es candidata para esa fase y `webapp-testing` para verificar la interfaz; ninguna de las dos está validada aún en la SF.
