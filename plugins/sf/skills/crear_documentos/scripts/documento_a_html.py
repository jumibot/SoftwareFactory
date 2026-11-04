"""Generador común de los documentos de la SF: convierte un .md a HTML con maqueta editorial.

Uso:
    python <skills>/crear_documentos/scripts/documento_a_html.py <documento>.md [--perfil <perfil.json>]
        [--tema <nombre>|<ruta .json>] [--identidad <carpeta>|ninguna] [--logo <ruta>|ninguno]
        [--producto "..."] [--tipo "..."] [--destino proyecto|usuario] [--herramientas "..."]

Genera el .html junto al .md. La sintaxis de los recursos está en la skill crear_documentos (SKILL.md,
«Catálogo de recursos»). Cada tipo de documento (fundacional, informe…) tiene su perfil (perfil.json en su skill):
su tipo por defecto, los recursos del catálogo que usa y sus propios CSS y JS. Sin perfil, todos los recursos.
Los temas y la identidad del proyecto están en scripts/tema_identidad.py, junto a este.
Paquetes de Python necesarios: markdown, Pillow (solo si hay logo).
"""

from __future__ import annotations

import argparse, html as html_mod, json, re, sys
from pathlib import Path

import collections
import markdown

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from tema_identidad import (BASE, CLAVES_IDENTIDAD, bloque_kit, buscar_identidad, cargar_tema,  # noqa: E402
                            destino_documento, enlaces_externos, herramientas_activas, kit_estilos, kit_scripts,
                            lector_estilos, lector_scripts,
                            logo_data_uri, procedencia, variables_css)

ASSETS = AQUI.parent / "assets"
RUTA_CSS = "skills/crear_documentos/assets/estilo_documento.css"
CSS = (BASE / RUTA_CSS).read_text(encoding="utf-8")
# Bloques «::: tipo» del catálogo. Un perfil elige cuáles usa su tipo de documento.
BLOQUES = ("tarjetas", "fichas", "columnas", "fuentes", "preguntas")
PERMITIDOS = set(BLOQUES)  # los que deja usar el perfil del tipo de documento (main)
NOMBRE_PERFIL = ""
EXTENSIONES = ["tables", "sane_lists", "attr_list", "md_in_html", "def_list"]
esc = html_mod.escape


# --- Cabecera de datos -------------------------------------------------------------------------

def leer_cabecera(raw: str) -> tuple[dict, str]:
    """Datos de portada entre dos líneas «---» al principio (clave: valor, una por línea)."""
    datos = {}
    m = re.match(r"---\s*\n(.*?)\n---\s*\n", raw, re.S)
    if not m:
        return datos, raw
    for linea in m.group(1).splitlines():
        if ":" in linea:
            k, v = linea.split(":", 1)
            datos[k.strip().lower()] = v.strip()
    return datos, raw[m.end():]


# --- Bloques «::: tipo» -----------------------------------------------------------------------

def arbol_bloques(lineas: list[str]) -> list:
    """Agrupa los bloques «::: tipo args» … «:::» (anidables) en nodos (tipo, args, hijos)."""
    raiz, pila = [], []
    actual = raiz
    for linea in lineas:
        m = re.match(r"^:::\s*(\w+)\s*(.*?)\s*$", linea)
        if m:
            nodo = (m.group(1).lower(), m.group(2), [])
            actual.append(nodo)
            pila.append(actual)
            actual = nodo[2]
        elif re.match(r"^:::\s*$", linea) and pila:
            actual = pila.pop()
        else:
            actual.append(linea)
    return raiz


def trocear(hijos: list, por_titulo: bool) -> tuple[list, list[list]]:
    """Separa los hijos de un bloque en piezas: en cada título (### o ####) o en cada línea «|||»."""
    intro, piezas, nivel = [], [], None
    for h in hijos:
        corta = False
        if isinstance(h, str):
            if por_titulo:
                t = re.match(r"^(#{3,4})\s", h)
                if t and (nivel is None or len(t.group(1)) == nivel):
                    nivel = len(t.group(1))
                    corta = True
            elif h.strip() == "|||":
                piezas.append([])
                continue
        if corta:
            piezas.append([h])
        elif piezas:
            piezas[-1].append(h)
        elif por_titulo:
            intro.append(h)
        else:
            piezas.append([h])
    return intro, piezas


# --- Tarjetas con color, icono y plegado ----------------------------------------------------------
# «#### Título {color=turquesa icono=codigo}» en la primera línea de una tarjeta: cabecera con el color
# de fondo y el icono; «::: tarjetas 3 plegables»: cada tarjeta es un <details> con la cabecera siempre a la vista.

COLORES = {"turquesa": "#1f7a7a", "naranja": "#a6501a", "verde": "#1f812d", "frambuesa": "#be185d"}
ICONOS = {  # trazos de 24 × 24, sin relleno
    "codigo": '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
    "dialogo": '<path d="M4 5h11a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H9l-4 3v-3H4a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z"/><path d="M19 9h1a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-1v3l-3-3h-3"/>',
    "documento": '<path d="M6 2h8l5 5v13a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"/><path d="M14 2v5h5M8 13h8M8 17h6"/>',
    "rama": '<circle cx="6" cy="5" r="2.2"/><circle cx="6" cy="19" r="2.2"/><circle cx="18" cy="7" r="2.2"/><path d="M6 7.2v9.6M18 9.2c0 5-12 3-12 7.6"/>',
    "carpeta": '<path d="M3 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "lupa": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l3 3 5-6"/>',
    "aviso": '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.01"/>',
}


def mezclar(hex_color: str, con: str, t: float) -> str:
    a = [int(hex_color[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(con[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


OPCIONES_TARJETA = {"color", "icono"}
# «::: preguntas»: cada tarjeta es una pregunta con opciones («Opción A» / «:   …»), recomendación y estado.
ESTADOS = {"abierta": "Abierta", "decidida": "Decidida", "separada": "Separada"}
OPCIONES_PREGUNTA = {"icono", "estado", "recomendada", "elegida", "destino"}


def svg_icono(icono: str) -> str:
    return (f'<svg class="tarjeta-icono" viewBox="0 0 24 24" width="26" height="26" aria-hidden="true" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONOS[icono]}</svg>')


def opciones_pregunta(opciones: dict, titulo: str) -> tuple[str, str, str]:
    """Clases, atributos y marca de estado de una pregunta. Valida estado, recomendada, elegida y destino."""
    estado = opciones.get("estado", "abierta").lower()
    if estado not in ESTADOS:
        sys.exit(f"Estado de pregunta no válido: «{estado}» en «{titulo}». Posibles: {', '.join(ESTADOS)}.")
    if "elegida" in opciones and estado != "decidida":
        sys.exit(f"«elegida» solo vale con estado=decidida: «{titulo}».")
    if "destino" in opciones and estado != "separada":
        sys.exit(f"«destino» solo vale con estado=separada: «{titulo}».")
    if estado == "abierta" and "recomendada" not in opciones:
        print(f"Aviso: la pregunta «{titulo}» está abierta y no tiene opción recomendada (recomendada=…).", file=sys.stderr)
    marca = ESTADOS[estado]
    if estado == "decidida" and opciones.get("elegida"):
        marca += f" · {opciones['elegida']}"
    elif estado == "separada" and opciones.get("destino"):
        marca += f" · {opciones['destino'].replace('_', ' ')}"
    datos = "".join(f' data-{k}="{esc(opciones[k])}"' for k in ("recomendada", "elegida") if opciones.get(k))
    return f" pregunta {estado}", datos, f'<span class="estado-pregunta {estado}">{esc(marca)}</span>'


def tarjeta(clase: str, piezas: list, plegable: bool, pregunta: bool = False) -> list[str]:
    """Una tarjeta. Sin color ni plegado, como siempre: <article> con su Markdown. Una pregunta lleva siempre cabecera."""
    titulo = piezas[0] if piezas and isinstance(piezas[0], str) else ""
    m = re.match(r"^(#{3,4})\s+(.*?)\s*\{(?![:#.])([^}]*)\}\s*(\{:?\s*#[\w-]+\s*\})?\s*$", titulo)
    opciones = {}
    validas = OPCIONES_PREGUNTA if pregunta else OPCIONES_TARJETA
    if m:
        opciones = dict(re.findall(r"(\w+)=(\S+)", m.group(3)))
        desconocidas = set(opciones) - validas
        if desconocidas:
            sys.exit(f"Opción de {'pregunta' if pregunta else 'tarjeta'} desconocida: {', '.join(sorted(desconocidas))}. "
                     f"Posibles: {', '.join(sorted(validas))}.")
    if not opciones and not plegable and not pregunta:
        return ["", f'<article class="{clase}" markdown="1">', ""] + emitir(piezas) + ["", "</article>", ""]
    if m:
        nivel, texto, ident = m.group(1), m.group(2), m.group(4)
    else:
        t = re.match(r"^(#{3,4})\s+(.*?)\s*(\{:?\s*#[\w-]+\s*\})?\s*$", titulo)
        if not t:
            que = "pregunta" if pregunta else "tarjeta con color o plegable"
            sys.exit(f"Una {que} empieza por su título ### o ####: «{titulo}»")
        nivel, texto, ident = t.group(1), t.group(2), t.group(3)
    ident = re.search(r"#([\w-]+)", ident).group(1) if ident else ""
    estilo, clases, datos, marca = "", clase + " con-cabecera", "", ""
    color = opciones.get("color")
    if color:
        color = COLORES.get(color, color)
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
            sys.exit(f"Color de tarjeta no válido: «{opciones['color']}». Posibles: {', '.join(COLORES)} o #rrggbb.")
        estilo = (f' style="--c:{color};--c-oscuro:{mezclar(color, "#000000", .35)};'
                  f'--c-borde:{mezclar(color, "#ffffff", .7)};--c-suave:{mezclar(color, "#ffffff", .9)}"')
        clases += " con-color"
    if pregunta:
        extra, datos, marca = opciones_pregunta(opciones, texto)
        clases += extra
    icono = opciones.get("icono")
    if icono and icono not in ICONOS:
        sys.exit(f"Icono de tarjeta desconocido: «{icono}». Posibles: {', '.join(ICONOS)}.")
    svg = svg_icono(icono) if icono else ""
    h = f"h{len(nivel)}"
    texto_html = re.sub(r"^<p>|</p>$", "", markdown.markdown(texto).strip())
    cabecera = f'{svg}<{h} class="tarjeta-titulo">{texto_html}</{h}>{marca}'
    id_attr = f' id="{ident}"' if ident else ""
    if plegable:
        clases += " plegable"
        return (["", f'<details class="{clases}"{id_attr}{estilo}{datos} open markdown="1">',
                 f'<summary class="tarjeta-cabecera">{cabecera}</summary>', "", '<div class="tarjeta-cuerpo" markdown="1">', ""]
                + emitir(piezas[1:]) + ["", "</div>", "</details>", ""])
    return (["", f'<article class="{clases}"{id_attr}{estilo}{datos} markdown="1">',
             f'<div class="tarjeta-cabecera">{cabecera}</div>', "", '<div class="tarjeta-cuerpo" markdown="1">', ""]
            + emitir(piezas[1:]) + ["", "</div>", "</article>", ""])


def marcar_preguntas(h: str) -> str:
    """En cada pregunta, los campos «Opción X» se marcan como opciones; la recomendada y la elegida llevan su marca, y
    «Recomendación» y «Decisión» se destacan. Comprueba que la recomendada y la elegida existen."""
    def una(m):
        html = m.group(0)
        apertura = html[:html.index(">") + 1]
        rec = re.search(r'data-recomendada="([^"]+)"', apertura)
        ele = re.search(r'data-elegida="([^"]+)"', apertura)
        rec, ele = (rec.group(1) if rec else None), (ele.group(1) if ele else None)
        letras = []

        def opcion(om):
            letra = om.group(1)
            letras.append(letra)
            clases, marcas = ["opcion"], []
            if letra == rec:
                clases.append("recomendada")
                marcas.append('<span class="marca-opcion recomendada">Recomendada</span>')
            if letra == ele:
                clases.append("elegida")
                marcas.append('<span class="marca-opcion elegida">Elegida</span>')
            if ele and letra != ele:
                clases.append("descartada")
            c = " ".join(clases)
            return f'<dt class="{c}">Opción {letra}{"".join(marcas)}</dt>\n<dd class="{c}">'

        html = re.sub(r"<dt>Opción\s+([A-Za-z0-9]+)\s*</dt>\s*<dd>", opcion, html)

        def campo(cm):
            c = "recomendacion" if cm.group(1) == "Recomendación" else "decision"
            return f'<dt class="{c}">{cm.group(1)}</dt>\n<dd class="{c}">'

        html = re.sub(r"<dt>(Recomendación|Decisión)</dt>\s*<dd>", campo, html)
        titulo = re.search(r'class="tarjeta-titulo">(.*?)</h[34]>', html, re.S)
        titulo = re.sub(r"<[^>]+>", "", titulo.group(1)) if titulo else ""
        for nombre, letra in (("recomendada", rec), ("elegida", ele)):
            if letra and letra not in letras:
                sys.exit(f"La pregunta «{titulo}» da {nombre}={letra}, pero no tiene «Opción {letra}». "
                         f"Opciones: {', '.join(letras) or 'ninguna'}.")
        return html
    return re.sub(r'<(article|details) class="tarjeta[^"]*\bpregunta\b[^"]*"[^>]*>.*?</\1>', una, h, flags=re.S)


def emitir(nodos: list) -> list[str]:
    """Convierte el árbol a Markdown con <div markdown="1">, que entiende md_in_html."""
    out = []
    for n in nodos:
        if isinstance(n, str):
            out.append(n)
            continue
        tipo, args, hijos = n
        if tipo in BLOQUES and tipo not in PERMITIDOS:
            sys.exit(f"El {NOMBRE_PERFIL or 'perfil'} no usa el recurso «::: {tipo}». Recursos de este tipo de documento: "
                     f"{', '.join(b for b in BLOQUES if b in PERMITIDOS)}. Si le hace falta, se añade a su perfil.json.")
        abre = lambda cls, tag="div": ["", f'<{tag} class="{cls}" markdown="1">', ""]
        cierra = lambda tag="div": ["", f"</{tag}>", ""]
        if tipo in ("tarjetas", "fichas", "preguntas"):
            opciones = args.split()
            cols = next((a for a in opciones if a in ("1", "2", "3")), "3" if tipo == "tarjetas" else "2")
            plegables = "plegables" in opciones
            intro, piezas = trocear(hijos, por_titulo=True)
            out += emitir(intro)
            out += abre(f"{'tarjetas preguntas' if tipo == 'preguntas' else tipo} cols-{cols}")
            clase = "tarjeta ficha" if tipo == "fichas" else "tarjeta"
            for p in piezas:
                out += tarjeta(clase, p, plegables, pregunta=tipo == "preguntas")
            out += cierra()
        elif tipo == "columnas":
            _, piezas = trocear(hijos, por_titulo=False)
            out += abre(f"columnas cols-{len(piezas) or 1}")
            for p in piezas:
                out += abre("columna") + emitir(p) + cierra()
            out += cierra()
        elif tipo == "fuentes":
            out += abre("fuentes") + emitir(hijos) + cierra()
        else:
            sys.exit(f"Bloque desconocido «::: {tipo}». Posibles: {', '.join(BLOQUES)}.")
    return out


def a_html(md: str) -> str:
    md = "\n".join(emitir(arbol_bloques(md.splitlines())))
    return marcar_preguntas(markdown.Markdown(extensions=EXTENSIONES).convert(md))


# --- Retoques del HTML ---------------------------------------------------------------------------

def slug(texto: str) -> str:
    t = re.sub(r"<[^>]+>", "", texto).lower()
    t = re.sub(r"[^\w\s-]", "", t, flags=re.U)
    return re.sub(r"[\s_]+", "-", t).strip("-")


def recuadros(h: str) -> str:
    """Citas → recuadros. «[!aviso]» o «[!decision]» en la primera línea eligen la variante;
    una primera línea solo en negrita es la etiqueta; sin nada de eso, es una cita destacada."""
    def uno(m):
        cuerpo = m.group(1).strip()
        variante = ""
        v = re.match(r"<p>\[!(aviso|decision|decisión)\]\s*(?:<br\s*/?>)?\s*", cuerpo)
        if v:
            variante = " " + v.group(1).replace("decisión", "decision")
            cuerpo = "<p>" + cuerpo[v.end():]
            cuerpo = re.sub(r"^<p>\s*</p>\s*", "", cuerpo)
        e = re.match(r"<p><strong>([^<]*?)</strong>\s*(?:<br\s*/?>|\n)\s*(.*)", cuerpo, re.S)
        if e:
            resto = e.group(2).strip()
            resto = ("<p>" + resto) if resto and not resto.startswith("<") else resto
            return f'<aside class="recuadro{variante}"><p class="recuadro-etiqueta">{e.group(1)}</p>{resto}</aside>'
        if variante or cuerpo.startswith("<p><strong>") or "<h3" in cuerpo or "<h4" in cuerpo:
            return f'<aside class="recuadro{variante}">{cuerpo}</aside>'
        return f'<blockquote class="destacado">{cuerpo}</blockquote>'
    return re.sub(r"<blockquote>(.*?)</blockquote>", uno, h, flags=re.S)


def etiquetar_tablas(h: str) -> str:
    """data-label en cada celda con el texto de su cabecera, para las fichas apiladas en el móvil."""
    def una(tm):
        tabla = tm.group(0)
        heads = [re.sub(r"<[^>]+>", "", x).strip() for x in re.findall(r"<th[^>]*>(.*?)</th>", tabla, re.S)]
        def fila(rm):
            celdas = iter(heads)
            return re.sub(r"<td([^>]*)>", lambda c: f'<td{c.group(1)} data-label="{next(celdas, "")}">', rm.group(0))
        return re.sub(r"<tr>.*?</tr>", fila, tabla, flags=re.S)
    return re.sub(r"<table>.*?</table>", una, h, flags=re.S)


def cabecera_seccion(linea: str) -> tuple[str, str, str, str]:
    """«Etiqueta | Título | Menú {#id}» → (etiqueta, título, menú, id)."""
    ident = ""
    m = re.search(r"\s*\{:?\s*#([\w-]+)\s*\}\s*$", linea)
    if m:
        ident, linea = m.group(1), linea[:m.start()]
    partes = [p.strip() for p in linea.split("|")]
    etiqueta = partes[0]
    titulo = partes[1] if len(partes) > 1 and partes[1] else etiqueta
    menu = partes[2] if len(partes) > 2 else ""
    return etiqueta, titulo, menu, ident or slug(titulo)


def seccion(n: int, etiqueta: str, titulo: str, ident: str, cuerpo_md: str) -> str:
    cuerpo = recuadros(a_html(cuerpo_md))
    # El primer párrafo sin clase de la sección es la entradilla.
    cuerpo = re.sub(r"^\s*<p>", '<p class="entradilla">', cuerpo, count=1)
    # Sección plegable: solo la primera abierta al cargar; se abre o pliega tocando el título
    # (assets/plegado.js añade el resto; al imprimir se abre todo).
    abierta = " open" if n == 1 else ""
    return (f'<details class="seccion" id="{ident}"{abierta}><summary class="seccion-titulo">'
            f'<span class="etiqueta">{n:02d} / {etiqueta}</span><h2>{titulo}</h2></summary>'
            f'<div class="seccion-cuerpo">{cuerpo}</div></details>')


def lineas_lema(lema: str) -> list[str]:
    """« // » fuerza el salto; si no lo hay, cada frase va en su línea."""
    if "//" in lema:
        return [x.strip() for x in lema.split("//")]
    return re.split(r"(?<=[.!?])\s+", lema.strip())


# --- Avisos del generador ------------------------------------------------------------------------
# Markdown deja pasar el HTML en bruto: un «<documento>» escrito en el texto se toma por una etiqueta y no se ve.
ETIQUETAS_HTML = set("""a abbr article aside audio b bdi bdo blockquote br button canvas caption cite code col colgroup dd del
details dfn div dl dt em fieldset figcaption figure footer form h1 h2 h3 h4 h5 h6 header hr i iframe img input ins kbd label
legend li main mark meter nav ol optgroup option output p picture pre progress q s samp script section select small source
span strong style sub summary sup table tbody td template textarea tfoot th thead time tr u ul var video wbr
svg g defs symbol use marker path rect circle ellipse line polyline polygon text tspan textpath title desc image pattern
lineargradient radialgradient stop clippath mask filter foreignobject""".split())


def avisar_etiquetas_sueltas(raw: str, desplazamiento: int = 0) -> list[str]:
    """Los «<…>» del texto que no son HTML conocido se pierden al generar: se avisa con su línea, fuera del código."""
    avisos, en_codigo = [], False
    for n, linea in enumerate(raw.splitlines(), 1 + desplazamiento):
        if re.match(r"^\s*(```|~~~)", linea):
            en_codigo = not en_codigo
            continue
        if en_codigo or linea.startswith("    ") and not linea.lstrip().startswith((":", "-", "*")):
            continue
        sin_codigo = re.sub(r"`[^`]*`", "", linea)
        for m in re.finditer(r"<(/?)([^\s<>/!]+)[^<>]*>", sin_codigo):
            nombre = m.group(2)
            if re.match(r"(https?|mailto|ftp):", nombre) or nombre.lower() in ETIQUETAS_HTML:
                continue
            avisos.append(f"línea {n}: «{m.group(0)}»")
    return avisos


def iconos_propios(identidad: dict, carpeta: Path) -> None:
    """«iconos» de identidad.json: nombre → trazos SVG de 24 × 24 o ruta a un .svg. Se suman a ICONOS."""
    for nombre, valor in identidad.get("iconos", {}).items():
        if not re.fullmatch(r"[\w-]+", nombre):
            sys.exit(f"Nombre de icono no válido en identidad.json: «{nombre}» (letras, cifras, - o _).")
        if valor.strip().endswith(".svg"):
            ruta = carpeta / valor.strip()
            if not ruta.is_file():
                sys.exit(f"No encuentro el icono «{nombre}» de identidad.json: {ruta}")
            m = re.search(r"<svg\b[^>]*>(.*)</svg>", ruta.read_text(encoding="utf-8"), re.S)
            if not m:
                sys.exit(f"El icono «{nombre}» ({ruta}) no es un SVG.")
            valor = m.group(1).strip()
        ICONOS[nombre] = valor


# --- Página ---------------------------------------------------------------------------------------

def cargar_perfil(ruta: str | None) -> dict:
    """Perfil de un tipo de documento: {"tipo", "recursos", "css", "js"}. Las rutas, relativas al perfil."""
    if not ruta:
        return {}
    r = Path(ruta)
    if not r.is_file():
        sys.exit(f"No encuentro el perfil del tipo de documento: {r}")
    perfil = json.loads(r.read_text(encoding="utf-8"))
    malas = set(perfil) - {"tipo", "recursos", "css", "js", "descripcion"}
    if malas:
        sys.exit(f"{r} usa claves desconocidas: {', '.join(sorted(malas))}. Posibles: tipo, recursos, css, js, descripcion.")
    desconocidos = set(perfil.get("recursos", BLOQUES)) - set(BLOQUES)
    if desconocidos:
        sys.exit(f"{r}: recursos desconocidos: {', '.join(sorted(desconocidos))}. Catálogo: {', '.join(BLOQUES)}.")
    perfil["_carpeta"] = r.parent
    return perfil


def bloque_propio(ruta: Path) -> str:
    """CSS o JS propio de un tipo de documento. Con data-kit si vive en el plugin, para actualizar_copia.py."""
    try:
        return bloque_kit(ruta.resolve().relative_to(BASE.resolve()).as_posix())
    except ValueError:
        etiqueta = "style" if ruta.suffix == ".css" else "script"
        return f"<{etiqueta}>\n{ruta.read_text(encoding='utf-8').rstrip()}\n</{etiqueta}>"


def main():
    global PERMITIDOS, NOMBRE_PERFIL
    ap = argparse.ArgumentParser(description="Documento .md → HTML editorial (generador común de crear_documentos)")
    ap.add_argument("md")
    ap.add_argument("--perfil", default=None, help="perfil.json del tipo de documento (lo pasa el generador de cada skill de tipo)")
    ap.add_argument("--tema", default=None, help="tema de crear_documentos (assets/temas/) o ruta a un .json; por defecto, el de la identidad")
    ap.add_argument("--identidad", default=None, help="carpeta con identidad.json; por defecto se busca docs/identidad/ subiendo desde el .md")
    ap.add_argument("--logo", default=None, help="ruta del logo; 'ninguno' para no ponerlo")
    ap.add_argument("--producto", default=None, help="nombre del producto; por defecto, el de la identidad o el título")
    ap.add_argument("--tipo", default=None, help="tipo de documento; por defecto, el de la cabecera del .md, el del perfil o «Documento»")
    ap.add_argument("--destino", default=None, help="proyecto o usuario; manda sobre la cabecera y la identidad. Sin destino, error")
    ap.add_argument("--herramientas", default=None, help="recomendadas, todas, ninguna, una lista o cambios («+leyenda -tablas»); "
                    "manda sobre la cabecera y la identidad. Sin herramientas, error")
    args = ap.parse_args()
    perfil = cargar_perfil(args.perfil)
    PERMITIDOS = set(perfil.get("recursos", BLOQUES))
    NOMBRE_PERFIL = perfil.get("tipo", "").lower()

    src = Path(args.md)
    ruta_id = buscar_identidad(src, args.identidad)
    identidad = json.loads(ruta_id.read_text(encoding="utf-8")) if ruta_id else {}
    desconocidas = set(identidad) - CLAVES_IDENTIDAD
    if desconocidas:
        sys.exit(f"{ruta_id} usa claves desconocidas: {', '.join(sorted(desconocidas))}")
    def archivos(clave):
        v = identidad.get(clave, [])
        return [ruta_id.parent / x for x in ([v] if isinstance(v, str) else v)]
    tema_id = identidad.get("tema")
    if tema_id and tema_id.endswith(".json"):
        tema_id = str(ruta_id.parent / tema_id)
    tema = cargar_tema(args.tema or tema_id or "morado")
    css_proyecto = "".join(f"\n  <style>\n{p.read_text(encoding='utf-8')}\n  </style>" for p in archivos("css"))
    js_proyecto = "".join(f"\n<script>\n{p.read_text(encoding='utf-8')}\n</script>" for p in archivos("js"))
    logo = None
    if args.logo and args.logo != "ninguno":
        logo = Path(args.logo)
    elif args.logo != "ninguno" and identidad.get("logo"):
        logo = ruta_id.parent / identidad["logo"]

    if ruta_id:
        iconos_propios(identidad, ruta_id.parent)
    texto_md = src.read_text(encoding="utf-8")
    datos, raw = leer_cabecera(texto_md)
    sueltas = avisar_etiquetas_sueltas(raw, texto_md[:len(texto_md) - len(raw)].count("\n"))
    if sueltas:
        print("Aviso: estos «<…>» no son HTML y no se verán en el documento. Escríbelos entre comillas invertidas "
              "(`<nombre>`) o con &lt; y &gt;:\n  " + "\n  ".join(sueltas), file=sys.stderr)
    tipo = args.tipo or datos.get("tipo") or perfil.get("tipo") or "Documento"
    h1 = re.search(r"^#\s+(.+)$", raw, re.M)
    if not h1:
        sys.exit("El documento necesita un título «# Nombre del proyecto».")
    nombre = h1.group(1).strip()
    producto = args.producto if args.producto is not None else identidad.get("producto", nombre)
    partes = re.split(r"^##\s+(.+)$", raw[h1.end():], flags=re.M)
    portada_md, secciones = partes[0], [(cabecera_seccion(c), md) for c, md in zip(partes[1::2], partes[2::2])]
    # Las citas «>» antes de la primera sección son avisos de alcance global: van al principio, fuera de las secciones.
    bloques = re.split(r"\n\s*\n", portada_md.strip()) if portada_md.strip() else []
    avisos_md = "\n\n".join(b for b in bloques if b.lstrip().startswith(">"))
    portada_md = "\n\n".join(b for b in bloques if not b.lstrip().startswith(">"))
    avisos = f'<div class="avisos-globales">{recuadros(a_html(avisos_md))}</div>' if avisos_md else ""

    # Portada. Con «antetitulo», el nombre es el titular y el lema va debajo; sin él, el lema es el titular.
    oscura = datos.get("portada", "").lower() == "oscura"
    marca = esc(datos.get("antetitulo") or nombre)
    if logo:  # alto de 40 px, como en el CSS; ancho y alto explícitos para que la portada no salte al cargar
        from PIL import Image
        with Image.open(logo) as im:
            ancho = round(im.width * 40 / im.height)
        marca = f'<img src="{logo_data_uri(logo)}" alt="" width="{ancho}" height="40">' + marca
    lema = "<br>".join(esc(x) for x in lineas_lema(datos["lema"])) if datos.get("lema") else ""
    p = [f'<header class="portada{" oscura" if oscura else ""}"><div class="portada-dentro">', f'<p class="marca">{marca}</p>']
    if datos.get("antetitulo"):
        p.append(f'<h1 class="titular">{esc(nombre)}' + (f'<span class="lema">{lema}</span>' if lema else "") + "</h1>")
    else:
        p.append(f'<h1 class="titular">{lema or esc(nombre)}</h1>')
    if not datos.get("antetitulo"):
        p.append(f'<p class="tipo-doc">{esc(tipo)}</p>')
    if datos.get("subtitulo"):
        p.append(f'<p class="subtitulo">{esc(datos["subtitulo"])}</p>')
    if not oscura:
        p.append('<hr class="portada-linea">')
    if portada_md.strip():
        p.append(f'<div class="idea">{a_html(portada_md)}</div>')
    # Portada sobria: la versión y el estado van al pie; las cifras ya no se muestran.
    version = datos.get("version", "")
    if datos.get("cifras"):
        print("Aviso: la portada ya no muestra «cifras»; se ignoran. Si una cifra argumenta, va en el texto.", file=sys.stderr)
    p.append("</div></header>")

    # Menú fijo: por defecto solo los botones (las secciones ya se ven como títulos plegables).
    # Con «menu: secciones», también los enlaces de las secciones con tercera parte en su título; con «menu: no», sin menú.
    opcion_menu = datos.get("menu", "botones").lower()
    enlaces = [(ident, menu) for (_, _, menu, ident), _ in secciones if menu] if opcion_menu == "secciones" else []
    nav = ""
    if secciones and opcion_menu not in ("no", "false"):
        nav = ('<nav class="menu" aria-label="Secciones del documento"><div class="menu-dentro">'
               + "".join(f'<a href="#{i}">{esc(t)}</a>' for i, t in enlaces)
               + '<span class="menu-botones"><button type="button" class="plegar">Plegar todo</button>'
               + '<button type="button" class="imprimir" onclick="window.print()">Imprimir / PDF</button></span></div></nav>')

    cuerpo = "".join(seccion(n, e, t, i, md) for n, ((e, t, _, i), md) in enumerate(secciones, 1))
    cuerpo = etiquetar_tablas(cuerpo)
    js = "\n" + bloque_kit("skills/crear_documentos/assets/plegado.js") + kit_scripts() if secciones else ""
    js += "\n" + bloque_kit("skills/crear_documentos/assets/fichas.js") if 'class="fichas' in cuerpo else ""
    # Lo propio del tipo de documento (perfil.json): después de lo común, antes de lo del proyecto.
    css_tipo = "".join("\n  " + bloque_propio(perfil["_carpeta"] / x) for x in perfil.get("css", []))
    js += "".join("\n" + bloque_propio(perfil["_carpeta"] / x) for x in perfil.get("js", []))
    # Si falta el destino o las herramientas, herramientas_activas se detiene con las opciones: no se elige por el autor.
    destino = args.destino or datos.get("destino", identidad.get("destino"))
    activas = herramientas_activas(args.herramientas or datos.get("herramientas", identidad.get("herramientas")), destino)
    pie_texto = datos.get("pie", "")
    url_fuentes = tema["tipografias"]["url"]
    fuentes = ('  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
               '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
               f'  <link href="{url_fuentes}" rel="stylesheet">\n') if url_fuentes else ""

    page = f"""<!DOCTYPE html>
<html lang="es" data-destino="{destino_documento(destino)}" data-herramientas="{activas}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(nombre)} · {esc(tipo)}</title>
  <meta name="theme-color" content="{tema['colores']['oscuro'] if oscura else '#ffffff'}">
{fuentes}  <style>
    {variables_css(tema)}
  </style>
  <style data-kit="{RUTA_CSS}">
{CSS}
  </style>{kit_estilos()}{lector_estilos(cuerpo)}{css_tipo}{css_proyecto}
</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
{''.join(p)}
{nav}
<div class="hoja">
  <main id="contenido" tabindex="-1">{avisos}{cuerpo}</main>
  <footer class="pie"><p>{esc(" · ".join(x for x in (producto, tipo, version, datos.get("estado", "")) if x))}</p>{f"<p>{esc(pie_texto)}</p>" if pie_texto else ""}<p class="procedencia">{esc(procedencia(src))}</p></footer>
</div>{js}{lector_scripts(cuerpo)}{js_proyecto}
</body>
</html>
"""
    page = enlaces_externos(page)
    out = src.with_suffix(".html")
    # Un id repetido rompe los enlaces internos (p. ej. una sección {#contenido} choca con <main id="contenido">).
    vistos = collections.Counter(re.findall(r'\sid="([^"]+)"', page))
    repetidos = sorted(i for i, n in vistos.items() if n > 1)
    if repetidos:
        sys.exit("Ids repetidos en la página: " + ", ".join(repetidos) + ". Cambia el {#id} de la sección o del elemento.")
    out.write_text(page, encoding="utf-8")
    print(out, "· tema:", tema.get("nombre", args.tema), "· identidad:", ruta_id or "ninguna", "· secciones:", len(secciones))


if __name__ == "__main__":
    main()
