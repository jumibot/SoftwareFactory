# En la app, /sf disponible antes del primer mensaje y solo órdenes al escribir /sf

Se prueba una orden /sf fija en el plugin para que en la app salga en la lista desde el principio, antes de que arranque el mod; si sale duplicada en la terminal o con otro nombre, se quita. Además, al escribir /sf la lista debería enseñar solo las órdenes de la SF (/sf, /sf_paso, /sf_config…), no todas sus skills.

La caja «Sin SF» sigue sin salir con el panel abierto, como dice la decisión 164: la bienvenida del panel ya cumple esa función.

Por qué: en la app la SF no corre hasta el primer mensaje y /sf no aparece; y una lista con todas las skills tapa las órdenes que busca el usuario (tarea 337).
