# Las skills de la SF tienen su fuente en el repositorio de la SF, y lo propio de cada proyecto va en su docs/identidad/

Las skills de la SF, las propias y las externas que adaptamos, tienen su fuente versionada en el repositorio de la SF, en `plugins/sf/skills/`, y viajan en el plugin `sf`. Una skill externa que se usa tal cual no se copia: es una dependencia del plugin, fijada a su commit (175, 176).

Lo propio de cada proyecto (estilo, tema, logo, producto y reglas del dominio) va en su `docs/identidad/`, nunca en la skill.

Recoge lo que sigue valiendo de «Fuente de las skills en la SF y lo propio de cada proyecto en `docs/identidad/`» (007), que queda deprecada.

Porqué: una skill con cosas de un proyecto o de un dominio deja de servir a los demás; por eso la visión y la infografía se hicieron independientes del dominio el mismo día (004, 005). Con la fuente en un solo sitio, una mejora llega a todos los proyectos al publicar el plugin.

Aplicada en: `plugins/sf/skills/`; `docs/identidad/` de cada proyecto (`sf:crear_documentos`, `sf:fijar_estilo`, `sf:infografia_tecnica`, `sf:documento_vision`); especificación, 2; metodología, 6.
