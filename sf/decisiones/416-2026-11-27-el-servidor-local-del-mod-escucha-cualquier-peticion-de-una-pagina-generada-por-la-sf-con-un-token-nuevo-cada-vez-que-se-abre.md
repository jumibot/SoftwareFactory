# El servidor local sf_proxy escucha cualquier petición de una página generada por la SF, con un token por apertura y las peticiones numeradas

Regla: el mod levanta un servidor local genérico, `sf_proxy`, solo en 127.0.0.1, que acepta cualquier petición, no solo las respuestas de un informe, para poder montar interfaces externas. Cada `sf_proxy` vale solo para una sesión concreta de Claude: lo que le llega va a esa sesión y muere con ella.

Lo que lo protege:
- la página la ha generado Claude;
- cada vez que se abre una página interactiva lleva un token nuevo, que invalida el anterior de esa página;
- cada petición va numerada, y el servidor rechaza un número repetido o anterior, así que ninguna petición vale dos veces.

Sin token válido, el servidor no atiende.

Opciones: renovar el token en cada llamada, para que fuera de un solo uso. Se descarta porque en local aporta poco (quien roba el token ya lee la página) y lo hace frágil: la página consulta cada pocos segundos, y con dos pestañas o una respuesta perdida quedaría bloqueada. La numeración da lo mismo sin ese riesgo.

Porqué: el diseño del informe «Responder a un informe desde la página» proponía un servidor que solo recogiera respuestas muy concretas. El propietario prefiere uno genérico para reutilizarlo en otras interfaces, y de momento solo lo usará en su ordenador, así que el token por apertura, las peticiones numeradas y la página generada por la SF le bastan.

Aplicada en: pendiente, en la tarea 475 (su informe y las tareas que salen de él).
