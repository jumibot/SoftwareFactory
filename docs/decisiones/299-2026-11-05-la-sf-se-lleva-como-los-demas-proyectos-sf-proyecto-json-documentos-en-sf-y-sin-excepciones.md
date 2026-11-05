# La SF se lleva como los demás proyectos: .sf/proyecto.json, documentos en sf/ y sin excepciones

Fecha: 2026-11-05. Decidida por el propietario de la Software Factory.

## Qué se decide

- La SF se lleva como los demás proyectos, sin excepciones: tiene su `.sf/proyecto.json` (con metodología), sus documentos de la SF en `sf/` (`sf/decisiones/`, `sf/propuestas.md`, `sf/informes/`) y, si la metodología lo pide, su `.sf/estado.json`.
- `cola.py` y el mod dejan de tratarla como caso especial donde no haga falta: la configuración sale de su `.sf/proyecto.json`.
- El `CLAUDE.md` de la SF no lleva excepciones a las reglas que entrega el mod.

## Por qué

Así la SF se prueba exactamente como la reciben los demás proyectos, y no hay reglas que digan una cosa en los proyectos y otra en la SF.

## Opciones descartadas

- Una línea en el `CLAUDE.md` con las diferencias de la SF.

## Aplicada en

Pendiente: tarea de normalizar la SF.
