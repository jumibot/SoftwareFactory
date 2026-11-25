# El mod entrega las reglas y sf:orquestacion al empezar la sesión, tras /clear y tras compactar

En los proyectos con `.sf/proyecto.json`, también en la propia SF («En la SF, las reglas y sf:orquestacion las entrega el mod, como en los demás proyectos», 298), el mod entrega como contexto, al empezar la sesión, tras `/clear` y tras compactar, las reglas de la plantilla y el texto entero de `sf:orquestacion`, leídos del plugin instalado. Nunca a un subagente. En cada mensaje se aplican sin volver a cargarlas.

La orquestación tiene su interruptor, `orquestacion` en `.sf/proyecto.json`, encendido por defecto («Las automatizaciones del plugin, configurables y avisando antes que bloquear», 171). Apagado, la carga el principal en esos mismos momentos.

El `CLAUDE.md` de un proyecto no lleva ninguna línea de la SF. Un proyecto que aún importa `@.sf/claude-sf.md` va atrasado: el mod no le entrega las reglas, pero sí la orquestación, y el panel avisa. Ponerlo al día quita la línea y la copia. La regla de «Lo que pinta la SF y lo global no son del proyecto» (167) sigue en el prompt de sistema, por corta.

Recoge lo que sigue valiendo de «El panel entrega las reglas y la orquestación en los proyectos» (187), que queda deprecada.

Porqué: la copia `.sf/claude-sf.md` de cada proyecto se quedaba atrás con cada versión, y cargar `sf:orquestacion` dependía de que Claude se acordara. Al empezar y tras compactar, no en cada mensaje: cada entrega añade unos 3.000 o 4.000 tokens.

Aplicada en: el mod (`hooks/contexto.ts`, `register.tsx`; el aviso de proyecto atrasado en `panel.tsx` y `lectura.ts`); `sf:incorporar_proyecto_a_sf`; `sf:orquestacion`; metodología, «Las reglas las entrega el mod».
