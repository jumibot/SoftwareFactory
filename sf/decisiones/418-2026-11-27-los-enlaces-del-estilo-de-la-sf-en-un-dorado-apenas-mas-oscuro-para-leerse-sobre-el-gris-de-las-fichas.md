# Los enlaces del estilo de la SF, en un dorado apenas más oscuro para leerse sobre el gris de las fichas

Regla: en el estilo Áureo de la SF, el color de texto del primario pasa de #876c00 a #806700, para que un enlace llegue a 4,5:1 también sobre el fondo gris de las fichas (4,52:1; sobre la página, 5,26:1). En oscuro no cambia.

Opciones: quitar el color fijado para que lo calcule el generador. No sirve: el generador solo lo oscurece si el primario ya se lee, y el dorado #f5c400 es demasiado claro; los enlaces saldrían en amarillo (1,37:1).

Porqué: con la tarea 479, el generador comprueba ese contraste y se niega a sacar un documento que no llegue; con #876c00 (4,18:1) dejaría de generar los documentos de la SF.

Aplicada en: pendiente, en la tarea 479 (docs/identidad/estilo.json, con fijar_estilo).
