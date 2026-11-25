# El panel entrega las reglas y la orquestación en los proyectos

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Las normas guardadas en la memoria de la SF, también en los demás proyectos» (211), informe «Normas y CLAUDE.md en los proyectos». El propietario elige las tres opciones recomendadas.
- **Contexto:** cada proyecto carga las reglas de la SF con la línea `@.sf/claude-sf.md` de su `CLAUDE.md`, una copia que se queda atrás con cada versión; cargar `sf:orquestacion` al empezar y tras compactar dependía de que Claude se acordara. Las normas ya llegan por el plugin, en sus skills (decisión 156).
- **Decisión:**
  1. El mod entrega las reglas de la plantilla al empezar la sesión, tras `/clear` y tras compactar (`classic.SessionStart`), solo en los proyectos con `.sf/proyecto.json`, leídas del plugin instalado. El `CLAUDE.md` de un proyecto no lleva ninguna línea de la SF. La regla de la decisión 167 sigue en el prompt de sistema, por corta.
  2. Entrega también el texto entero de `sf:orquestacion`, no solo la orden de cargarla, con el interruptor `orquestacion` en `.sf/proyecto.json`, encendido por defecto (decisión 171).
  3. En un proyecto que aún tiene la línea `@.sf/claude-sf.md`, el mod no entrega las reglas pero sí la orquestación, y el panel avisa de que el proyecto va atrasado. El caso «actualizar» de `sf:incorporar_proyecto_a_sf` quita la línea y la copia, en una sesión abierta en cada proyecto.
  La propia SF no recibe la inyección: su `CLAUDE.md` dice las reglas desde la fuente.
- **Consecuencias:** sin copias que regenerar y siempre la versión instalada; cargar la orquestación ya no depende de Claude. Unos 3.000 tokens más por arranque y por compactación. Los subagentes no deben recibirla.
- **Aplicada en:** el mod (`hooks/contexto.ts`, `register.tsx`; el aviso de proyecto atrasado en `panel.tsx` y `lectura.ts`); `sf:incorporar_proyecto_a_sf` («Reglas de la SF, sin tocar el CLAUDE.md»); `sf:orquestacion`; metodología, «Qué pertenece a cada proyecto consumidor»; `CLAUDE.md`; «Cómo funciona la Software Factory»; «Mejora continua a la Software Factory».
