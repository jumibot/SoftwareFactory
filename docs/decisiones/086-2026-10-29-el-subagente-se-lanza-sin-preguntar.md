# El subagente se lanza sin preguntar

- **Origen:** SoftwareFactory, 2026-10-29, tarea 109. El propietario: «que el orquestador no pregunte siempre si lanzar el subagente, solo cuando sean triviales».
- **Decisión:** cuando una tarea ya no necesita interacción, el principal lanza el subagente sin pedir permiso, avisando. Solo pregunta en las triviales, para hacerlas en el principal. Precisa «El principal orquesta; los subagentes ejecutan».
- **Aplicada en:** metodología, 2 («Orquestación con subagentes»); plantilla `claude-sf.md`; `CLAUDE.md`.
