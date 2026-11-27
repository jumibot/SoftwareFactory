# Un front envía todo junto al pulsar Enviar y se pone al día en su sitio sin cambiar solo de versión

Regla: en una página interactiva de la SF (un front), lo contestado se envía todo junto al pulsar Enviar, con un borrador guardado en el navegador mientras tanto. La página pregunta a sf_proxy cada pocos segundos y pone al día en su sitio el estado de lo contestado y los avisos de Claude; si hay una versión nueva del documento, la ofrece, pero no la aplica sola. El HTML del repositorio sigue siendo el documento estático.

Opciones: enviar cada respuesta al elegirla, por bloques o con un borrador guardado en el servidor; y, para recibir, solo enviar o que el servidor empuje y la página se reescriba entera. Se descartan: más ruido en el chat, mensajes mientras Claude trabaja, o cambiar el texto bajo quien lee.

Porqué: el propietario acepta las dos recomendaciones del informe «Responder a un informe desde la página» (preguntas 7 y 8). Un informe largo puede pasar luego a bloques sin tocar sf_proxy (tarea 475).

Aplicada en: pendiente, en la tarea 475.
