# El subagente se lanza sin preguntar

Estado: deprecada el 2026-11-25 por «El principal orquesta y lanza cada subagente sin preguntar» ({V-083}); lo demás, por «Todo el trabajo de la tarea, a su subagente» (151).

- **Origen:** SoftwareFactory, 2026-10-29, tarea 109. El propietario: «que el orquestador no pregunte siempre si lanzar el subagente, solo cuando sean triviales».
- **Decisión:** cuando una tarea ya no necesita interacción, el principal lanza el subagente sin pedir permiso, avisando. Solo pregunta en las triviales, para hacerlas en el principal. Precisa «El principal orquesta; los subagentes ejecutan».
- **Aplicada en:** lo vigente, en `sf:orquestacion` («Subagentes»).
