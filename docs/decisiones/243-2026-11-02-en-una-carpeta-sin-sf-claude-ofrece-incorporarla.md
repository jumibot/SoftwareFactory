# En una carpeta sin SF, Claude ofrece incorporarla

- **Origen:** SoftwareFactory, 2026-11-02. En «Primeros cinco minutos de un usuario nuevo con la SF» (289) se preguntó qué sabe Claude en una carpeta sin SF (se proponía una línea de contexto y una orden `/sf_incorporar`). El propietario: «le preguntamos si quiere incorporar el proyecto a la sf y si es que sí lanzamos la incorporación».
- **Contexto:** con la SF instalada, en una carpeta sin `.sf/proyecto.json` el mod solo da a Claude la línea de Python; el colega tuvo que preguntar dónde estaba el panel.
- **Decisión:** en una carpeta sin SF, Claude pregunta al usuario, con un menú, si quiere incorporar el proyecto a la SF. Si dice que sí, lanza la incorporación (`sf:incorporar_proyecto_a_sf`).
- **Consecuencias:** el mod da a Claude ese encargo al empezar en una carpeta sin SF. Queda por concretar cuándo no se vuelve a preguntar si el usuario dice que no.
- **Aplicada en:** pendiente; en la 289.
