# Manda el proyecto salvo en cómo se lleva el repositorio: ramas, commits, push, cola y publicación

Fecha: 2026-11-05. Decidida por el propietario de la Software Factory.

## Qué se decide

- Si una regla del `CLAUDE.md` de un proyecto choca con la SF, manda la del proyecto, salvo en cómo se lleva el repositorio.
- «Cómo se lleva el repositorio» incluye las ramas (`develop`, `main`, `feature/NN-…` con squash al cerrar, worktrees de los subagentes), los commits, los push, la cola y la publicación con tag.
- El formato de los commits sigue siendo el de la configuración del proyecto (`.sf/proyecto.json`), aceptado al incorporarlo.

## Por qué

El panel, `cola.py` y el cierre dan por hecho esa forma de llevar el repositorio. Si una regla del proyecto la cambiara (trabajar en `main`, commits o push a su manera), cerrar, revertir, activar una rama o publicar dejarían de funcionar o romperían cosas. Al incorporar el proyecto se aceptó.

## Aplicada en

Pendiente: plantilla `plugins/sf/templates/claude-sf.md` y metodología, «Reglas del proyecto» (tarea 316).
