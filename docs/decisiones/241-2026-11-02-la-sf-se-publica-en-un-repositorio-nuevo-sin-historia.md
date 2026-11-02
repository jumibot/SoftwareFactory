# La SF se publica en un repositorio nuevo sin historia, con licencia MIT

- **Origen:** SoftwareFactory, 2026-11-02. El propietario pidió dejar público el repositorio de la SF («Prepara para dejar el repo público ya»). La revisión de «Dejar público el repositorio de la SF» (317) no encontró secretos, pero sí cuatro cosas graves en la historia de git: un dato de salud en una decisión, el correo personal en todos los commits, el emblema de un instituto en una copia vieja y el diseño completo de SmartColdBox en un archivo ya borrado.
- **Contexto:** se valoraron reescribir la historia con `git filter-repo`, publicar solo el plugin en un repositorio de distribución, publicar tal cual y empezar un repositorio público nuevo con la historia aplanada.
- **Decisión:**
  - El repositorio actual se renombra y queda privado como archivo de la historia. El público, `jumibot/SoftwareFactory`, arranca con un solo commit del árbol ya limpio.
  - Antes se limpia el árbol: fuera el dato de salud de la decisión 035, la copia vieja `_respaldo/skills/documento_vision_global_2026-10-25/`, los proyectos del propietario del README («Proyectos relacionados» y LecturaFàcil) y su perfil personal de la visión «hombre orquesta» (clases, sustento, horario).
  - Licencia MIT a nombre de jumibot. La procedencia de las piezas vive en `docs/referencias/procedencia/`; en el plugin solo queda `LICENCIAS-DE-TERCEROS.md`.
  - Los commits se firman con el correo jumiadistancia@gmail.com.
- **Consecuencias:** `git log` y `blame` empiezan de cero en el público; la historia sigue en el archivo privado. Los hashes citados en los documentos quedan sin destino público. Hay que repuntar `origin` y rehacer los worktrees. Crear el repositorio y cambiar la visibilidad necesitan el OK del propietario. Corrige el acceso de «Así se prepara la prueba del colega» (239).
- **Aplicada en:** «Dejar público el repositorio de la SF» (317) limpió el árbol y puso la licencia; el corte, en la 318.
