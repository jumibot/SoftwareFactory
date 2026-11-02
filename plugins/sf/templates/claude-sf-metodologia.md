<!-- sf {{version}} · Reglas del método. Las entrega el mod de la SF junto a las comunes en los proyectos con "metodologia": true en .sf/proyecto.json; no se copian al proyecto. -->

# Software Factory: metodología

Este proyecto sigue la metodología de la SF (`"metodologia": true` en `.sf/proyecto.json`).

- **Método:** la skill `sf:metodologia`, que dice qué parte del método leer en cada momento.
- **Estado:** `.sf/estado.json` se actualiza al cambiar de fase o de devslice.
- **Documentos:** se generan con la skill `crear_documentos` y la de su tipo; los diagramas, en SVG inline, nunca en ASCII ni en mermaid.
