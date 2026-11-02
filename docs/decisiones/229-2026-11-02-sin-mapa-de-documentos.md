# Sin mapa de documentos: o se sigue la estructura de la SF, o no se mapea

- **Origen:** SoftwareFactory, 2026-11-02. En «Configuración inicial: decidir el mínimo, los commits y la versión, y diseñar .sf/proyecto.json y las preguntas» (263) se preguntó dónde se guarda el mapa de los documentos del proyecto que menciona «Incorporar un proyecto no mueve ni renombra nada» (201). El propietario: «en caso de que el nuevo proyecto no se adapte a la estructura de sf no hay mapeo. Si se adapta ya sabemos dónde buscarlos».
- **Contexto:** la 201 dice que la SF mapea los documentos de un proyecto que no se reorganiza. La 263 proponía no guardar nada (Claude los busca y, si no, pregunta) o un bloque `documentos` en `.sf/proyecto.json` con sus rutas.
- **Decisión:** no hay mapa de documentos. Si el proyecto sigue la estructura documental de la SF, sus documentos están donde la SF los busca. Si no la sigue, la SF no los mapea.
- **Consecuencias:** `.sf/proyecto.json` no lleva un bloque `documentos`, y la incorporación no pregunta rutas de documentos. Corrige lo que la 201 decía sobre mapear.
- **Aplicada en:** pendiente; en la 263 (el informe) y en `sf:incorporar_proyecto_a_sf` («Implementar la configuración inicial», 193).
