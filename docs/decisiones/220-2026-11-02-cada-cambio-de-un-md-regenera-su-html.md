# Cada cambio de un .md regenera su HTML

- **Origen:** SoftwareFactory, 2026-11-02. Al repasar las tareas de documentos en «Tareas deliberativas: registrar decisiones y dilemas abiertos» (274), el propietario: «siempre que se modifique un documento (md) se regenera su html».
- **Contexto:** los documentos de la SF tienen su `.md` como fuente y un HTML para leerlos en el navegador, generado con uno de tres scripts (`doc_to_html.py`, `fundacional_to_html.py` y el de los «Cómo funciona…»). Nada obligaba a regenerarlo, y algunos informes no tenían HTML. «Los documentos nuevos van a develop en cada vuelta y se ofrecen en el navegador» (216) da por hecho que el HTML está al día.
- **Decisión:** siempre que se modifica un `.md` que tiene HTML, o que debe tenerlo (documentos, informes), se regenera su HTML en el mismo cambio. Un `.md` y su HTML nunca quedan desfasados.
- **Consecuencias:** hace falta una forma única de regenerar (una orden que elija el generador según el documento) que usen la copia a `develop` de la 216, los subagentes y el cierre; y conviene una comprobación que detecte un HTML más viejo que su `.md`. Responde a la pregunta de la 274 sobre regenerar el HTML.
- **Aplicada en:** pendiente; en «Documentos nuevos a develop en cada vuelta, y abrirlos en el navegador» (297).
