# Hecho en esta sesión: peticiones cerradas

- **Origen:** SoftwareFactory, 2026-10-27. El propietario: «Hecho en esta sesión son commits?» y, tras la respuesta: «mejor peticiones cerradas en vez de commits y un led verde si tiene commit».
- **Decisión:** la sección lista las peticiones cerradas en la sesión, la última arriba, con «●» verde si tienen commit y «○» si no. El panel guarda el texto y el commit al cerrarse cada una, porque después, probadas, salen de la cola. Sustituye a la lista de commits del punto 1 de «El panel, en dos bloques».
- **Aplicada en:** mod de estado; especificación de la SF; `docs/como-funciona-la-software-factory.md`; plugin `sf` 0.27.0.
