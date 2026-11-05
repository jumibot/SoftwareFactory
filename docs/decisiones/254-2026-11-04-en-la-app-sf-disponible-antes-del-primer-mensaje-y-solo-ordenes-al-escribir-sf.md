# En la app, /sf disponible antes del primer mensaje y solo órdenes al escribir /sf

- **Origen:** SoftwareFactory, 2026-11-04, en la tarea «Que la SF se vea y funcione en la app de escritorio como en la terminal» (337). La decidió el propietario de la Software Factory; sus palabras no constan.
- **Contexto:** en la app la SF no corre hasta el primer mensaje y /sf no aparece; y una lista con todas las skills tapa las órdenes que busca el usuario.
- **Opciones:** no constan.
- **Decisión:** se prueba una orden /sf fija en el plugin para que en la app salga en la lista desde el principio, antes de que arranque el mod; si sale duplicada en la terminal o con otro nombre, se quita. Además, al escribir /sf la lista debería enseñar solo las órdenes de la SF (/sf, /sf_paso, /sf_config…), no todas sus skills. La caja «Sin SF» sigue sin salir con el panel abierto, como dice la decisión 164: la bienvenida del panel ya cumple esa función. Por qué: lo que dice el contexto; no consta más porqué que ese.
- **Consecuencias:** el plugin lleva una orden fija y el mod la oculta cuando corre; las skills internas dejan de salir en la lista. Lo concretan «La orden fija del plugin se llama /sf:panel» y «Las skills internas de la SF no salen en el menú al escribir /sf».
- **Aplicada en:** `plugins/sf/commands/panel.md` (la orden fija, `/sf:panel`); el mod (`hooks/register.tsx`: `ORDEN_FIJA`, la atiende como /sf y la oculta de la lista); `user-invocable: false` en el frontmatter de las skills internas.
