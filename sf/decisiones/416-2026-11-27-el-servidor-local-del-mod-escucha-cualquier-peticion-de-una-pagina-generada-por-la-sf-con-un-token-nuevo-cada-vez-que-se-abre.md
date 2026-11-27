# El servidor local del mod escucha cualquier petición de una página generada por la SF, con un token nuevo cada vez que se abre

Regla: el mod levanta un servidor local genérico, solo en 127.0.0.1, que acepta cualquier petición, no solo las respuestas de un informe, para poder montar interfaces externas. Lo que lo protege es que la página la ha generado Claude y que cada vez que se abre una página interactiva lleva un token nuevo; sin ese token, el servidor no atiende.

Porqué: el diseño del informe «Responder a un informe desde la página» proponía un servidor que solo recogiera respuestas muy concretas. El propietario prefiere uno genérico para reutilizarlo en otras interfaces, y de momento solo lo usará en su ordenador, así que el token por apertura y la página generada por la SF le bastan.

Aplicada en: pendiente, en la tarea 475 (su informe y las tareas que salen de él).
