"""Convierte un documento de visión .md a HTML.

Carcasa con bloques y subsecciones plegables, cabecera y pie, con un tema visual de la skill
crear_documentos (assets/temas/: colores, tipografías y aspecto). Ancho completo de pantalla, adaptación a móvil (gráficos
desplazables, diagramas verticales, tablas en fichas) y el primer bloque abierto.

Uso:
    python <carpeta de la skill>/scripts/doc_to_html.py <documento>.md [--tema <nombre>|<ruta .json>]
        [--identidad <carpeta>|ninguna] [--logo <ruta>|ninguno] [--producto "..."] [--tipo "..."]

Genera el .html junto al .md.

Todo lo propio de cada proyecto está en su identidad.json (doc/identidad/ o docs/identidad/, que se
busca subiendo carpetas desde el .md): tema, logo, producto, tipo de documento, CSS de sus
componentes y reglas de redacción. Las opciones de la línea de órdenes mandan sobre él.
La skill no contiene nada de ningún proyecto. Origen: docs/referencias/procedencia/ del repositorio de la SF.
Paquetes de Python necesarios: markdown, Pillow.
"""
import base64, io, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
# Lo común a todos los documentos (temas, identidad, herramientas, coloreado de código) está en la skill crear_documentos.
COMUN = Path(__file__).resolve().parent.parent.parent / "crear_documentos" / "scripts"
if not (COMUN / "tema_identidad.py").is_file():
    sys.exit(f"Falta la skill crear_documentos junto a esta: no encuentro {COMUN / 'tema_identidad.py'}")
sys.path.insert(0, str(COMUN))
import markdown
import carcasa as m
from resaltar_codigo import resaltar  # coloreado de sintaxis de los bloques de código

from tema_identidad import *  # temas, colores, tipografías e identidad del proyecto
from tema_identidad import _rgb


EXTRA_HEAD = """
  <link href="{{fuentes_url}}" rel="stylesheet">
  <style>
    /* Tres niveles de lectura:
       1. narración y explicación: tipografía de texto del tema;
       2. escenas dialogadas: tipografía de escena, con etiqueta, margen lateral y fondo suave;
       3. datos del caso, fuentes y evidencias: tipografía de texto compacta, cifras tabulares, etiqueta en versalitas. */
    .escena { font-family: var(--fuente-escena); background: var(--fondo-suave); border-left: 3px solid var(--tenue);
              border-radius: 0 12px 12px 0; padding: 1rem 1.4rem .9rem; margin: 1.8rem 0; max-width: none; }
    .escena p { margin: 0; }
    .escena-etiqueta { font-family: var(--fuente-texto); font-size: .7rem; font-weight: 700; letter-spacing: .09em;
                       text-transform: uppercase; color: var(--primario); margin-bottom: .35rem !important; }
    .escena-contexto { font-size: .95rem; color: var(--texto-suave); line-height: 1.5; margin-bottom: .6rem !important; }
    .turno { display: grid; grid-template-columns: 9.5rem 1fr; gap: .15rem 1.1rem; padding: .6rem 0; border-top: 1px solid var(--linea); }
    .ponente { font-family: var(--fuente-texto); font-size: .8rem; font-weight: 700; color: var(--oscuro); line-height: 1.35; padding-top: .2rem; }
    .ponente small { display: block; font-weight: 400; color: var(--texto-tenue); font-size: .74rem; }
    .turno > p:last-child { font-size: 1.04rem; line-height: 1.6; color: var(--texto); }
    .turno.sistema .ponente { color: var(--texto-suave); }
    .turno.sistema > p:last-child { font-family: var(--fuente-texto); font-size: .9rem; color: #4b5563; font-variant-numeric: tabular-nums; }
    .escena-pie { font-family: var(--fuente-texto); font-size: .74rem; color: var(--texto-tenue); border-top: 1px solid var(--linea); padding-top: .5rem; margin-top: .1rem !important; }
    /* Hilo conductor: la narración del caso va en cursiva dentro de un recuadro gris claro, con la etiqueta
       «El caso», al abrir, en cada capítulo, cada vez que se revela un dato y al cerrar. */
    .caso, .expediente { background: #f7f7f8; border: 1px solid #e5e7eb; border-radius: 10px;
                         padding: .9rem 1.3rem 1rem; margin: 1.4rem 0 1.6rem; max-width: none; }
    .caso-etiqueta, .expediente b:first-child { display: block; font-size: .7rem; font-weight: 700; letter-spacing: .09em;
                                                text-transform: uppercase; color: var(--oscuro); margin: 0 0 .35rem; font-style: normal; }
    /* Aviso de ficción: al principio del documento, antes del prólogo. */
    .aviso-ficcion { border-left: 4px solid #b91c1c; background: #fef2f2; border-radius: 0 8px 8px 0;
                     padding: .7rem 1.1rem; margin: .4rem 0 1.4rem; font-size: .92rem; line-height: 1.55; color: #3b0d0d; max-width: none; }
    .aviso-ficcion p { margin: 0; }
    .aviso-ficcion p + p { margin-top: .4rem; }
    .caso p { margin: 0; }
    .caso p + p { margin-top: .6rem; }
    .caso > p:not(.caso-etiqueta) { font-size: 1.08rem; line-height: 1.65; color: var(--texto); font-style: italic; }
    .expediente { font-size: .92rem; font-variant-numeric: tabular-nums; color: var(--texto); padding: .6rem 1.3rem .7rem; }
    .ficha { border: 1px solid var(--borde); border-radius: 12px; padding: .9rem 1.2rem; margin: 1.6rem 0; max-width: none; font-size: .92rem; }
    .ficha-titulo { font-family: var(--fuente-titulos); font-weight: 600; color: var(--oscuro); font-size: 1.02rem; margin: 0 0 .5rem; }
    .ficha dl { display: grid; grid-template-columns: 11rem 1fr; margin: 0; }
    .ficha dt, .ficha dd { margin: 0; padding: .42rem 0; border-top: 1px solid #f1ebfa; }
    .ficha dt { font-size: .7rem; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; color: var(--texto-suave); padding-top: .55rem; }
    .ficha dt.acordado, .ficha dd.acordado { border-top: 2px solid var(--primario); }
    .ficha dt.acordado { color: var(--primario); }
    .ficha dt.evidencia { color: var(--acento); }
    @media (max-width: 720px) {
      .escena { padding: .9rem 1rem .8rem; }
      .turno { grid-template-columns: 1fr; }
      .ficha dl { grid-template-columns: 1fr; }
      .ficha dd { border-top: none; padding-top: 0; }
    }
    h1, h2, h3, .institution-name, .bloque-title, .subseccion-summary { font-family: var(--fuente-titulos); }
    .site-header { background: #fff; border-bottom: 1px solid rgba(var(--primario-rgb),.15); justify-content: flex-start; gap: 1rem; align-items: center; }
    .site-header .brand-logo { height: 52px; width: auto; }
    .institution-name { color: var(--texto); font-weight: 600; }
    .institution-sub { color: var(--primario); }

    /* Ancho completo de pantalla, con márgenes que escalan */
    .page { max-width: none; box-shadow: none; }
    .site-header, .report-header { padding-left: clamp(1rem, 4vw, 3.5rem); padding-right: clamp(1rem, 4vw, 3.5rem); }
    .report-body { padding: 1.8rem clamp(1rem, 4vw, 3.5rem) 3rem; }
    @media (min-width: 1400px) { body { font-size: 1.06rem; } }

    /* Gráficos: no crecen sin límite en pantallas anchas */
    figure svg { max-width: 1100px; margin: 0 auto; }
    /* Diagramas verticales: estrechos en escritorio y a todo el ancho en móvil, sin desplazamiento */
    figure.vertical svg { max-width: 560px; }
    @media (max-width: 720px) {
      figure.vertical { overflow-x: visible; }
      figure.vertical svg { min-width: 0 !important; }
      figure.vertical::before { content: none !important; display: none !important; }
    }

    /* Móvil y tableta estrecha */
    /* Aviso de desplazamiento solo cuando el gráfico (mín. 680px) no cabe */
    @media (max-width: 700px) {
      figure::before { content: 'Desliza para ver el gráfico completo →'; display: block; font-size: .72rem; color: var(--texto-tenue); text-align: right; margin-bottom: .3rem; }
    }
    @media (max-width: 720px) {
      body { line-height: 1.6; }
      .site-header .brand-logo { height: 38px; }
      .institution-name { font-size: .98rem; }
      .institution-sub { font-size: .66rem; }
      .report-header { padding-top: .7rem; padding-bottom: .7rem; }
      :root { --marca: 1.15rem; --chip-izq: .75rem; }
      .bloque-summary::before { width: .7rem; height: .7rem; margin-right: .45rem; }
      .bloque-chip { padding: .3rem .75rem; }
      .bloque-title { font-size: .98rem; line-height: 1.3; }
      .bloque-btn { display: none; }
      blockquote { padding: .5rem .9rem; }
      /* Los gráficos conservan un tamaño legible y se desplazan en horizontal */
      figure { overflow-x: auto; -webkit-overflow-scrolling: touch; margin-left: 0 !important; margin-right: 0 !important; }
      figure svg { min-width: 680px; }
      figcaption { position: sticky; left: 0; max-width: calc(100vw - 2rem); text-align: left !important; }
      /* Tablas en fichas apiladas: cada fila es una tarjeta con sus etiquetas */
      table, tbody, tr, td { display: block; width: 100%; }
      thead { display: none; }
      tr { border: 1px solid rgba(var(--primario-rgb),.15); border-radius: 10px; margin: 0 0 .8rem; padding: .55rem .85rem; background: #fff; }
      tr:hover td { background: transparent; }
      td { border: none; padding: .18rem 0; word-break: normal; overflow-wrap: anywhere; hyphens: auto; }
      td:first-child { font-family: var(--fuente-titulos); font-weight: 600; color: var(--oscuro); font-size: 1rem; padding-bottom: .3rem; }
      td[data-label]:not(:first-child)::before { content: attr(data-label); display: block; font-size: .7rem; letter-spacing: .05em; text-transform: uppercase; color: var(--texto-tenue); }
    }

    /* Comparativa de versiones en tarjetas: una tarjeta por idea y, dentro, una subtarjeta por versión
       con su nombre (data-version), el texto y el comentario de lo que ha cambiado y por qué.
       Las subtarjetas van en 4 columnas (o --cols) en escritorio, 2 en tableta y 1 en móvil. */
    .comparativa { margin: 1.6rem 0 1.4rem; font-size: .9rem; }
    .cmp-cab { display: none; }
    .cmp-fila { display: grid; grid-template-columns: repeat(var(--cols, 4), minmax(0, 1fr)); gap: .7rem;
      background: #fff; border: 1px solid var(--linea); border-radius: 12px; padding: 1rem 1.05rem 1.05rem;
      margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(var(--primario-rgb),.06); }
    .cmp-idea { grid-column: 1 / -1; margin: 0 0 .1rem; font-family: var(--fuente-titulos);
      font-size: .8rem; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; color: var(--primario); }
    .cmp-celda { background: var(--fondo); border-radius: 8px; padding: .7rem .8rem .75rem; min-width: 0; }
    .cmp-celda[data-version^="Original"] { background: #fff; border: 1px dashed var(--tenue); }
    .cmp-celda::before { content: attr(data-version); display: block; font-size: .7rem; font-weight: 700;
      color: var(--oscuro); margin-bottom: .35rem; letter-spacing: .02em; }
    .cmp-celda p { margin: 0; }
    .cmp-texto { font-size: .9rem; line-height: 1.5; color: var(--texto); }
    .cmp-texto + .cmp-texto { margin-top: .2rem !important; }
    .cmp-nota { margin-top: .6rem !important; padding-top: .5rem; border-top: 1px solid var(--linea);
      font-size: .78rem; line-height: 1.45; color: var(--texto-suave); }
    .cmp-vacia .cmp-texto { color: var(--texto-tenue); font-style: italic; }
    .cmp-pie { background: var(--fondo); }
    .cmp-pie .cmp-celda { background: #fff; }
    .cmp-pie .cmp-texto { font-variant-numeric: tabular-nums; font-weight: 700; font-size: .95rem; }
    .report-body li, .report-body p { overflow-wrap: anywhere; }
    @media (max-width: 1000px) { .cmp-fila { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
    @media (max-width: 560px) { .cmp-fila { grid-template-columns: 1fr; } }
  </style>"""



import argparse
ap = argparse.ArgumentParser()
ap.add_argument("md")
ap.add_argument("--producto", default=None, help="nombre del producto (cabecera y pie); por defecto, el de la identidad del proyecto")
ap.add_argument("--tipo", default=None, help="tipo de documento, para el pie; por defecto, el de la identidad o «Documento de visión»")
ap.add_argument("--tema", "--paleta", dest="tema", default=None,
                help="tema visual: nombre de un tema de crear_documentos (assets/temas/, sin .json) o ruta a un .json; por defecto, el de la identidad del proyecto o «morado»")
ap.add_argument("--logo", default=None,
                help="ruta del logo; por defecto, el de la identidad del proyecto. 'ninguno' deja la cabecera solo con texto")
ap.add_argument("--identidad", default=None,
                help="carpeta con identidad.json (o el propio archivo); por defecto se busca doc/identidad/ o docs/identidad/ "
                     "subiendo desde el .md. 'ninguna' para no usarla")
ap.add_argument("--destino", default=None, help="proyecto o usuario; manda sobre el .md y la identidad. Sin destino, error")
ap.add_argument("--herramientas", default=None,
                help="recomendadas, todas, ninguna, una lista o cambios («+leyenda -tablas»); manda sobre el .md y la identidad. "
                     "Sin herramientas, error")
args = ap.parse_args()

def archivo_identidad(nombre: str, clave: str) -> Path:
    ruta = ruta_identidad.parent / nombre
    if not ruta.is_file():
        sys.exit(f"«{clave}» de {ruta_identidad} indica un archivo que no existe: {ruta}")
    return ruta

ruta_identidad = buscar_identidad(Path(args.md), args.identidad)
identidad = json.loads(ruta_identidad.read_text(encoding="utf-8")) if ruta_identidad else {}
desconocidas = set(identidad) - CLAVES_IDENTIDAD
if desconocidas:
    sys.exit(f"{ruta_identidad} usa claves desconocidas: {', '.join(sorted(desconocidas))}. "
             f"Claves posibles: {', '.join(sorted(CLAVES_IDENTIDAD))}")
tema_id = identidad.get("tema")
if tema_id and tema_id.endswith(".json"):
    tema_id = str(archivo_identidad(tema_id, "tema"))
tema = cargar_tema(args.tema or tema_id or "morado")
producto = args.producto if args.producto is not None else identidad.get("producto", "")
tipo = args.tipo if args.tipo is not None else identidad.get("tipo", "Documento de visión")
css_proyecto = identidad.get("css", [])
css_proyecto = [css_proyecto] if isinstance(css_proyecto, str) else css_proyecto
css_proyecto = "".join("\n  <style>\n" + archivo_identidad(c, "css").read_text(encoding="utf-8").rstrip() + "\n  </style>"
                       for c in css_proyecto)
if args.logo == "ninguno":
    logo = None
elif args.logo:
    logo = Path(args.logo)
elif identidad.get("logo"):
    logo = archivo_identidad(identidad["logo"], "logo")
else:
    logo = None
src = Path(args.md)
raw = src.read_text(encoding="utf-8")
h1 = re.match(r"(?:\s*<!--.*?-->\s*\n)*#\s+(.+)\n", raw)  # antes del título, los comentarios de opciones
title = h1.group(1).strip()
body_md = m.ensure_blank_line_before_headings(raw[h1.end():])
# La barra bajo la cabecera lleva el estado del documento, no su nombre de archivo: si antes de la primera
# sección hay un párrafo de una línea que empieza por «**Estado…:**», sale del cuerpo y va a la barra.
# Sin él, no hay barra.
estado = re.search(r"^(\*\*Estado[^*\n]*:\*\*[^\n]+)\n(?:\n|$)", body_md.split("\n## ", 1)[0], re.M)
if estado:
    body_md = body_md.replace(estado.group(1), "", 1)
    barra_html = '<div class="report-title report-estado">' + re.sub(
        r"^<p>|</p>$", "", markdown.markdown(estado.group(1)).strip()) + "</div>"
else:
    barra_html = ""
html = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"]).convert(body_md)
html = resaltar(html)
html, _ = m.add_anchors(html)
# Solo el primer bloque queda abierto; el resto (anexos incluidos) empieza plegado. El detalle de
# segundo nivel va en H4, que la carcasa pliega como subsubsección cerrada.
html = re.sub(r'<details id="([^"]*)" class="(bloque bloque-1)">', r'<details id="\1" class="\2" open>', m.wrap_bloques(html), count=1)
html = traducir_colores(colores_a_variables(html), tema)
page = m.render_page(
    title=re.sub(r"^\W+\s*", "", title),
    header_main=title,
    header_sub=producto,
    resumen_html=barra_html,
    body_html=html,
    # Variables del tema al principio; reglas de «estilo» al final, para que manden sobre las de EXTRA_HEAD.
    # Después, el CSS del proyecto, que puede usar las variables del tema y ajustar lo que necesite.
    extra_head=EXTRA_HEAD.replace("<style>", "<style>\n    " + variables_css(tema), 1).replace(
        "</style>", ("    " + css_estilo(tema["estilo"]) + "\n  " if tema["estilo"] else "") + "</style>")
        + kit_estilos() + lector_estilos(html) + css_proyecto,
    # Columna de herramientas (buscador): anclada a la derecha en pantalla grande y despegable; ver tools/kit_documentos/herramientas.js.
    extra_body_end=kit_scripts() + lector_scripts(html),
    footer_text=" · ".join(x for x in (producto, tipo) if x),
)
page = page.replace('class="subseccion">', 'class="subseccion" open>')
if not barra_html:
    page = re.sub(r'\s*<div class="report-header">\s*</div>', "", page, count=1)
page = aplicar_tema(page, tema)

def etiquetar_tablas(html: str) -> str:
    """Añade data-label a cada celda con el texto de su cabecera (fichas apiladas en móvil)."""
    def una(tm):
        tabla = tm.group(0)
        heads = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", tabla, re.S)]
        def fila(rm):
            celdas = iter(heads)
            return re.sub(r"<td>", lambda _: f'<td data-label="{next(celdas, "")}">', rm.group(0))
        return re.sub(r"<tr>.*?</tr>", fila, tabla, flags=re.S)
    return re.sub(r"<table>.*?</table>", una, html, flags=re.S)

page = etiquetar_tablas(page)
page = enlaces_externos(page)
# Opciones del documento: --destino y --herramientas; si no, comentarios «<!-- clave: valor -->» al principio del .md;
# si no, identidad. Si falta alguna, herramientas_activas se detiene con las opciones: no se elige por el autor.
opciones = dict(re.findall(r"<!--\s*(herramientas|destino)\s*:\s*(.*?)\s*-->", raw[:3000]))
destino = args.destino or opciones.get("destino", identidad.get("destino"))
activas = herramientas_activas(args.herramientas or opciones.get("herramientas", identidad.get("herramientas")), destino)
page = page.replace('<html lang="es">', f'<html lang="es" data-destino="{destino_documento(destino)}" data-herramientas="{activas}">', 1)
page = page.replace("</footer>", f'<p class="procedencia">{procedencia(src)}</p></footer>', 1) if "</footer>" in page else page
if logo:
    page = page.replace('<div class="institution">', f'<img class="brand-logo" src="{logo_data_uri(logo)}" alt="{producto}"><div class="institution">', 1)
out = src.with_suffix(".html")
out.write_text(page, encoding="utf-8")
print(out, "· tema:", tema.get("nombre", args.tema), "· identidad:", ruta_identidad or "ninguna", "· logo:", logo or "ninguno")
