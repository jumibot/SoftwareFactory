# En la SF, las reglas y sf:orquestacion las entrega el mod, como en los demás proyectos

Fecha: 2026-11-05. Decidida por el propietario de la Software Factory.

## Qué se decide

- En la propia SF, las reglas comunes y `sf:orquestacion` las entrega el mod, como en los demás proyectos: al empezar la sesión, tras `/clear` y tras compactar.
- El `CLAUDE.md` de la SF deja de mandar cargar `sf:orquestacion` y de repetir esas reglas.
- Con la SF apagada en la sesión, el mod no entrega nada y la sesión es Claude Code sin más (decisión 297).

## Por qué

Así la SF se prueba tal como la reciben los demás proyectos. Y una sesión apagada no sigue leyendo reglas de la SF en el `CLAUDE.md`, sin saber que está apagada.

## Opciones descartadas

- Un contexto mínimo al arrancar apagada, solo en la SF.

## Aplicada en

Pendiente: tarea 281 (mod) y la tarea de actualizar la metodología, la plantilla y el CLAUDE.md.
