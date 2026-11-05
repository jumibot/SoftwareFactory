# Si main solo está en el remoto, se crea la local sin preguntar

- **Origen:** SoftwareFactory, 2026-11-02. En «Implementar la configuración inicial» (193), al simular la incorporación de PoseTracker, se vio que su `main` solo existe en el remoto. Se preguntó si se crea la rama local sin preguntar o se pregunta en el menú del repositorio. El propietario aceptó la recomendación: crearla sin preguntar.
- **Contexto:** la SF necesita `develop` y la rama que hace de `main` («El manejo del repositorio no se negocia: siempre develop», 205; «Si el proyecto tiene master, se pregunta si hace de main», 213).
- **Decisión:** si la rama que hace de `main` existe solo en el remoto, la incorporación crea la local siguiéndola, sin preguntar, y lo dice en el resumen.
- **Precisada el mismo día:** lo mismo vale para `develop`: si solo existe en el remoto, se crea la local siguiéndola, sin preguntar.
- **Consecuencias:** el menú del repositorio no gana una pregunta; crear la rama solo copia lo que ya hay en el remoto.
- **Aplicada en:** `sf:incorporar_proyecto_a_sf` («Rama de publicación»: `git branch --track`, sin preguntar); `sf:configurar_proyecto` (`rama_main`); `plugins/sf/tools/configuracion.py` (`detectar`) y sus pruebas; «Cómo funciona la Software Factory», «Incorporación de un proyecto a la SF».
