# Las skills internas de la SF no salen en el menú al escribir /sf

Doce skills de la SF llevan user-invocable: false en su frontmatter: configurar_proyecto, crear_documentos, definicion_tecnica, diseno_interfaz, documento_fundacional, documento_vision, flujo_tareas, incorporar_proyecto_a_sf, infografia_tecnica, informe_deliberativa, metodologia y orquestacion. Al escribir /sf, el menú enseña solo /sf:panel, /sf:comprobar_instalacion y las órdenes del mod (/sf, /sf_config…).

Claude las sigue cargando igual; solo deja de poder lanzarlas el usuario escribiendo su nombre, y para eso basta pedírselo a Claude.

Porqué: el menú de /sf, sobre todo en la app de escritorio, se llenaba de skills internas y escondía las órdenes que el usuario necesita (decisión 254).
