# Borrar las ramas del subagente al volver

- **Origen:** SoftwareFactory, 2026-10-30, tarea 176. Decisión del propietario.
- **Contexto:** al lanzar un subagente con worktree, Claude Code crea una rama `worktree-agent-<id>` desde `main`; el subagente trabaja en una rama auxiliar desde la de la tarea y el principal la trae con `git merge --ff-only`. Al quitar el worktree, las dos ramas quedan sueltas: se acumularon cinco.
- **Decisión:** al volver un subagente, tras traer sus commits y quitar el worktree, el principal borra con `git branch -D` su rama auxiliar y la `worktree-agent-<id>`, después de comprobar que no tienen commits fuera de la rama de la tarea.
- **Consecuencias:** no se acumulan ramas sueltas. Si alguna tiene commits que no están en la rama de la tarea, no se borra: primero se traen o se decide qué hacer con ellos.
- **Aplicada en:** plugins/sf/skills/flujo_tareas/references/estados.md (transición 11) y plugins/sf/skills/flujo_tareas/SKILL.md.
