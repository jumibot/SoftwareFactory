---
name: definicion_tecnica
description: Elabora la definición técnica y la arquitectura global de un proyecto de la Software Factory — contexto tecnológico, perfil técnico favorito con sus excepciones justificadas, paradigma, decisiones de arquitectura que evitan que las partes diverjan, convenciones, stack con versiones verificadas, estructura semilla, persistencia, capacidades opcionales (agente de IA, brain, KB, API), lo que se aplaza y registro de decisiones en formato MADR. Úsala cuando pidan definir la técnica, la arquitectura, el stack o la solución de un proyecto, o registrar una decisión técnica, después de la especificación funcional y la interfaz.
---

# Definición técnica

Esta skill es una **capa fina de la Software Factory (SF)**: el método es de la SF y la técnica se reutiliza de otros (atribución y licencias en `LICENCIAS-DE-TERCEROS.md`, en la raíz del plugin; la historia, en la [procedencia de las piezas](https://github.com/jumibot/SoftwareFactory/blob/main/docs/referencias/procedencia/README.md)). Produce la definición técnica global del proyecto (metodología, 3.3), una sola vez por proyecto y no por funcionalidad, después de la especificación funcional y del diseño de interfaz.

No contiene nada de ningún proyecto. Las preferencias y los perfiles técnicos están en la metodología de la SF (secciones 5 y 7); lo propio de cada proyecto, en sus documentos.

## Qué produce

- `docs/specs/tecnica/definicion-tecnica.md`, con la forma de `assets/plantilla-definicion-tecnica.md`.
- Un archivo por decisión no obvia en `sf/decisiones/`, `NNN-AAAA-MM-DD-titulo.md`, con la forma de `assets/plantilla-decision.md`. La carpeta reúne todas las decisiones del proyecto; se crea si no existe. Se registra con `cola.py decision "Título" --archivo RUTA` (`tools/` del plugin), que da el número y el nombre, rehace el índice, `README.md`, y hace el commit en `develop` sin cambiar la rama activa; `--numero NNN` reescribe una. Al juntar ramas, el índice se regenera con `tools/indice_decisiones.py docs/decisiones`.
- Si hace falta, una actualización mínima del `CLAUDE.md` del proyecto.

El documento técnico dice **la regla**; cada decisión en `sf/decisiones/` guarda **el porqué**. Cuando ya exista código, la estructura y el stack los manda el código; las reglas siguen en el documento.

## Reglas de la SF

- **Partir del perfil.** Las preferencias y el perfil favorito que encaje (metodología, 5 y 7) son el punto de partida. Se confirma su adecuación y cada excepción se justifica.
- **Solo lo que el proyecto necesita.** Agente de IA como componente, brain de desarrollo, KB operativa, API separada, interfaz web: todo es **opcional**. Se pregunta si el proyecto lo necesita; si no, no aparece.
- **Complejidad proporcionada.** Pocas decisiones para un proyecto pequeño; más para uno grande. Sin carpetas ni capas que no tengan contenido.
- **SQL nativo** con migraciones versionadas (metodología, 7.5), sin ORM salvo excepción justificada.
- **Versiones verificadas.** Toda tecnología que se nombre se comprueba en su fuente oficial en la fecha de trabajo; nunca de memoria.
- **Preguntar, no inventar.** Lo que falta se marca `NECESITA ACLARACIÓN` o `[SUPUESTO]` y pasa a pregunta para el propietario.
- **Nombres descriptivos** para decisiones y componentes. Nunca códigos como `AD-1` o `0007`.
- **Diagramas en SVG** (metodología, 6): el diagrama de dependencias y cualquier esquema de arquitectura, de flujo o de datos van como SVG inline en el `.md`, con las recomendaciones de `../metodologia/references/diagramas-svg.md` (vertical, 560 de ancho). Nunca en ASCII ni en mermaid. La estructura semilla de carpetas sí va como árbol de texto.
- **Aprobación del propietario** antes de dar la definición por cerrada.

## Modos

- **Guiado** (por defecto): ante cada decisión con alternativas reales, se presentan las opciones con sus consecuencias y elige el propietario.
- **Rápido:** se redacta todo con `[SUPUESTO]` en lo no confirmado y se repasa al final. Solo si el propietario lo pide.

## Qué entra en el documento

Una decisión entra como **decisión de arquitectura** solo si cumple las tres condiciones:

1. Dos partes construidas por separado (dos devslices, dos personas, dos agentes) podrían elegir de forma incompatible.
2. La elección no es obvia.
3. Hay una alternativa real con otro coste.

Si no las cumple, va a convenciones, al stack o a **Aplazado**, con el motivo por el que puede esperar.

## Procedimiento

1. **Leer** la visión, la especificación funcional, la interfaz, las referencias, las decisiones ya registradas y, en un proyecto con código, el código existente. En un proyecto con código, se ratifican las convenciones que ya hay en lugar de inventar otras.
2. **Contexto técnico.** Rellenar los campos de la plantilla: lenguaje y versión, dependencias principales, persistencia, pruebas, plataforma, tipo de proyecto, rendimiento, restricciones, escala, integraciones, instalación y distribución, y capacidades opcionales. Lo que no se sepa: `NECESITA ACLARACIÓN`.
3. **Investigar lo abierto.** Para cada `NECESITA ACLARACIÓN`, buscar en fuentes oficiales y proponer opciones. Verificar las versiones vigentes.
4. **Perfil y excepciones.** Proponer el perfil favorito que encaje. Cada excepción va a la tabla *Excepción · Por qué hace falta · Alternativa más simple descartada porque*.
5. **Arquitectura.**
   - **Paradigma** con nombre (por ejemplo, MVP o Clean), con sus capas asignadas a carpetas.
   - **Decisiones de arquitectura**, cada una con *A qué obliga*, *Qué evita* y *Regla*, y un diagrama de dependencias en SVG (quién puede depender de quién).
   - **Convenciones**: nombres; datos y formatos (identificadores, fechas, errores); estado y aspectos transversales (errores, registro, configuración, permisos).
   - **Stack** con versión fijada.
   - **Estructura semilla**: la del perfil, ajustada; solo lo que no es obvio.
   - **Persistencia**: entidades principales y relaciones, motor y migraciones.
   - **Capacidades opcionales** que el proyecto use: agente de IA (metodología, 7.4 y 7.7: contrato, credencial, agente simulado), brain de desarrollo y KB operativa (7.6), API.
   - **Instalación y operación**: el paso único de instalación, entornos y despliegue.
   - **Mapa funcionalidad → componente**: dónde vive cada funcionalidad y qué la gobierna.
   - **Aplazado**, con el motivo de cada punto.
6. **Decisiones.** Por cada decisión no obvia, un archivo en `sf/decisiones/` con nombre descriptivo, fecha, contexto y problema, opciones consideradas, decisión con su porqué y consecuencias. Si cambia una decisión anterior, lo dice y marca la antigua como sustituida. Después se regenera el índice. El documento técnico enlaza el archivo.
7. **`CLAUDE.md` del proyecto.** Si hace falta, un bloque mínimo con comandos, políticas que el código no expresa, divergencias respecto a lo habitual y versiones. Sin resumen de arquitectura (está en el documento técnico). Cada revisión lo deja igual o más corto.
8. **Revisión.** Recorrer la lista de comprobación. Para un proyecto grande o crítico, ofrecer una revisión independiente con un subagente que solo lea el documento y busque dos partes que puedan chocar.
9. **Entrega.** Resumir decisiones, excepciones, lo aplazado y las preguntas abiertas. Pedir la aprobación del propietario.

## Lista de comprobación

- [ ] Cubre cada funcionalidad de la especificación (mapa funcionalidad → componente).
- [ ] Cada decisión de arquitectura cumple las tres condiciones y su regla es comprobable y evita de verdad la divergencia que nombra.
- [ ] Nada de lo aplazado permite que dos partes diverjan.
- [ ] Cada dimensión está decidida, aplazada o como pregunta abierta. Ninguna queda en silencio, incluidas la instalación, los entornos y la operación.
- [ ] Las versiones del stack están verificadas en su fuente y con fecha.
- [ ] Las excepciones al perfil están justificadas.
- [ ] Las capacidades opcionales que aparecen son las que el proyecto necesita; las demás no aparecen.
- [ ] En un proyecto con código, ratifica lo existente en lugar de contradecirlo.
- [ ] Cada decisión no obvia tiene su archivo en `sf/decisiones/`, enlazado, y el índice está regenerado.
