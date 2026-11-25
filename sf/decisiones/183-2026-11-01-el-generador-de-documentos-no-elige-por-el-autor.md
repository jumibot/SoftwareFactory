# El generador de documentos no elige por el autor

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Las skills de documentos HTML preguntan qué herramientas incluir» (204). Ante los documentos de la SF que no dicen su destino ni sus herramientas, el propietario elige «indicarlo al generarlos»; y sobre el modo oscuro forzado por el autor, «retirarla».
- **Contexto:** con la 204, toda skill que genera un documento HTML pregunta el destino y las herramientas, y el generador se detiene si faltan. Los documentos existentes de la SF (Cómo funciona…, visiones) no los anotan.
- **Decisión:** los documentos de la SF que no anotan destino ni herramientas se generan indicándolos cada vez (`--destino` y `--herramientas` del generador), sin anotarlos en la identidad ni en cada documento. El autor ya no puede forzar el modo oscuro: los documentos abren en claro y el oscuro lo elige quien lee en «Lectura»; un documento antiguo con `oscuro` lo ignora con un aviso.
- **Consecuencias:** quien regenera un documento de la SF decide en ese momento para quién es y qué lleva. Los scripts que generan sin preguntar (índice de decisiones, README) pasan `--destino proyecto --herramientas recomendadas`.
- **Aplicada en:** skills de visión, fundacional e infografía y el kit de documentos (204).
