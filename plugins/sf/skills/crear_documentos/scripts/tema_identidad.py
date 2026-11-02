"""Temas e identidad de proyecto, compartidos por los generadores HTML de la SF (skill crear_documentos).

Lo usan documento_a_html.py (el generador común de crear_documentos, con el que generan el fundacional y los
informes) y doc_to_html.py (la maqueta de la visión). Carga un tema de assets/temas/ o del proyecto, deriva sus
tonos, produce las variables CSS y busca el identidad.json del proyecto.
"""

from __future__ import annotations

import base64, io, json, re, sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
TEMAS = ASSETS / "temas"

# Roles de color de los temas. Cada rol es una variable CSS (--<rol>) en estilo_base.css y EXTRA_HEAD.
# En el .md, los gráficos pueden escribir el color de un rol en el tema teal o en el morado: el
# generador lo pasa a la variable del rol. Orden: rol, valor en el tema teal, valor en el tema morado.
ROLES = [
    ("primario", "#00726b", "#7b2cbf"), ("oscuro", "#004d47", "#4c1d80"), ("primario-vivo", "#009690", "#9d5ce0"),
    ("fondo", "#e0f4f3", "#f8f5ff"), ("borde", "#b2deda", "#e4d7f5"), ("linea", "#e0eceb", "#ece4f7"),
    ("fondo-medio", "#d4ecea", "#e6dcf4"), ("fondo-suave", "#f0faf9", "#fbf9fe"), ("tenue", "#7dffd9", "#c4b5d9"),
    ("pagina", "#f2f4f4", "#faf8fd"), ("texto", "#1a1a1a", "#2b2b2f"), ("texto-suave", "#555", "#6b7280"),
    ("texto-tenue", "#888", "#9ca3af"), ("acento", "#6d28d9", "#b45309"), ("acento-fondo", "#ede9fe", "#fff7ed"),
    ("acento-borde", "#c4b5fd", "#fcd9b6"),
]

# Tonos derivados: si el tema no da un rol, se calcula mezclando otro rol con blanco o negro.
# (rol, rol de partida, color de mezcla, proporción de mezcla). Proporciones tomadas del tema morado.
DERIVADOS = [
    ("oscuro", "primario", "#000000", .38), ("primario-vivo", "primario", "#ffffff", .25),
    ("fondo", "primario", "#ffffff", .95), ("borde", "primario", "#ffffff", .81),
    ("linea", "primario", "#ffffff", .88), ("fondo-medio", "primario", "#ffffff", .84),
    ("fondo-suave", "primario", "#ffffff", .97), ("tenue", "primario", "#ffffff", .55),
    ("pagina", "primario", "#ffffff", .97),
    ("texto-suave", "texto", "#ffffff", .40), ("texto-tenue", "texto", "#ffffff", .60),
    ("acento-fondo", "acento", "#ffffff", .94), ("acento-borde", "acento", "#ffffff", .72),
]
COLORES_MINIMOS = {"texto": "#2b2b2f", "acento": "#b45309"}  # el tema solo tiene que dar «primario»
TIPOGRAFIAS = {  # valores por defecto si el tema no define tipografías
    "texto": "'DM Sans', Arial, sans-serif",
    "titulos": "'Space Grotesk', 'DM Sans', sans-serif",
    "escena": "'Source Serif 4', Georgia, serif",
    "url": "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap",
}

def _rgb(h: str) -> tuple:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[k:k + 2], 16) for k in (0, 2, 4))

def mezclar(color: str, con: str, prop: float) -> str:
    a, b = _rgb(color), _rgb(con)
    return "#" + "".join(f"{round(x + (y - x) * prop):02x}" for x, y in zip(a, b))

def cargar_tema(nombre_o_ruta: str) -> dict:
    ruta = Path(nombre_o_ruta)
    if ruta.suffix != ".json":
        ruta = TEMAS / f"{nombre_o_ruta}.json"
    if not ruta.is_file():
        disponibles = ", ".join(sorted(p.stem for p in TEMAS.glob("*.json")))
        sys.exit(f"Tema no encontrado: {nombre_o_ruta}. Temas disponibles: {disponibles}")
    tema = json.loads(ruta.read_text(encoding="utf-8"))
    colores = {k: v.lower() for k, v in tema.get("colores", {}).items()}
    if "primario" not in colores:
        sys.exit(f"El tema {ruta.name} debe definir al menos el color «primario».")
    desconocidos = set(colores) - {r for r, _, _ in ROLES}
    if desconocidos:
        sys.exit(f"El tema {ruta.name} usa roles de color desconocidos: {', '.join(sorted(desconocidos))}")
    for rol, valor in COLORES_MINIMOS.items():
        colores.setdefault(rol, valor)
    for rol, base, con, prop in DERIVADOS:
        colores.setdefault(rol, mezclar(colores[base], con, prop))
    tema["colores"] = colores
    serie = [c.lower() for c in tema.get("serie", [])]
    for c in serie:
        if not re.fullmatch(r"#[0-9a-f]{6}", c):
            sys.exit(f"El tema {ruta.name} tiene un color de «serie» no válido: {c} (formato #rrggbb)")
    tema["serie"] = serie
    estilo = tema.get("estilo", {})
    for clave, valor in estilo.items():
        if clave == "esquinas":
            if not isinstance(valor, (int, float)) or valor < 0:
                sys.exit(f"El tema {ruta.name}: «esquinas» debe ser un número de píxeles")
        elif clave == "opacidad":
            # De 0,75 a 1, título blanco (grande y en negrita por debajo de 1: 3:1 o más).
            # De 0,2 a 0,5, título en el color oscuro del bloque (4,5:1 o más). En medio no se lee bien ninguno.
            if not isinstance(valor, (int, float)) or not (0.75 <= valor <= 1 or 0.2 <= valor <= 0.5):
                sys.exit(f"El tema {ruta.name}: «opacidad» (etiqueta sólida) debe estar entre 0.75 y 1 (título blanco) "
                         "o entre 0.2 y 0.5 (título oscuro)")
        elif clave not in ESTILO_OPCIONES or valor not in ESTILO_OPCIONES[clave]:
            opciones = "; ".join(f"{k}: {', '.join(v)}" for k, v in ESTILO_OPCIONES.items())
            sys.exit(f"El tema {ruta.name}: estilo «{clave}: {valor}» no válido. Opciones: {opciones}; esquinas: número")
    tema["estilo"] = estilo
    tema["tipografias"] = {**TIPOGRAFIAS, **tema.get("tipografias", {})}
    return tema

# Opciones de aspecto de un tema («estilo»). Sin ellas, el aspecto es el de siempre (tema «morado»).
ESTILO_OPCIONES = {
    "cabecera": ("blanca", "primario", "oscuro"),
    "etiqueta": ("tinte", "solida", "linea"),
    "marcador": ("circulo", "cuadrado", "ninguno"),
}

def css_estilo(estilo: dict) -> str:
    """CSS adicional según las opciones de «estilo» del tema."""
    css = []
    cab = estilo.get("cabecera", "blanca")
    if cab != "blanca":
        fondo = "var(--primario)" if cab == "primario" else "var(--oscuro)"
        css.append(f".site-header {{ background: {fondo}; border-bottom: none; }}"
                   " .institution-name { color: #fff; } .institution-sub { color: rgba(255,255,255,.8); }"
                   " .site-header .brand-logo { background: #fff; border-radius: 6px; padding: 4px; }")
    eti = estilo.get("etiqueta", "tinte")
    if eti == "solida":
        opacidad = float(estilo.get("opacidad", 1))
        fondo = "var(--primario)" if opacidad >= 1 else f"rgba(var(--primario-rgb), {opacidad:g})"
        texto = "#fff" if opacidad >= .75 else "var(--oscuro)"
        css.append(f".bloque-chip {{ background: {fondo}; }} .bloque-summary, .bloque-summary:hover {{ color: {texto}; }}")
        if opacidad >= 1:
            css.append(".bloque-btn { color: #fff; border-color: rgba(255,255,255,.6); }"
                       " .bloque-btn:hover { background: rgba(255,255,255,.18); color: #fff; }")
        else:
            # Con fondo traslúcido, el texto blanco pierde contraste: el título pasa a texto grande en negrita
            # (WCAG pide 3:1) y los botones van sobre blanco con el color oscuro del bloque.
            css.append(".bloque-summary { font-size: 1.17rem; font-weight: 700; }"
                       " .bloque-btn { color: var(--oscuro); background: rgba(255,255,255,.92); border-color: transparent; }"
                       " .bloque-btn:hover { background: #fff; color: var(--oscuro); }")
    elif eti == "linea":
        css.append(".bloque-chip { background: transparent; border-radius: 0; border-left: 4px solid var(--primario);"
                   " border-bottom: 1px solid var(--borde); padding-left: .8rem; }"
                   # El texto del título empieza tras el borde (4px) y el relleno (.8rem): ahí se alinea el contenido.
                   " :root { --chip-izq: calc(.8rem + 4px); }")
    mar = estilo.get("marcador", "circulo")
    if mar == "cuadrado":
        css.append(".bloque-summary::before { border-radius: 2px; }")
    elif mar == "ninguno":
        css.append(".bloque-summary::before { display: none; } :root { --marca: 0rem; }")
    if "esquinas" in estilo:
        r = f'{float(estilo["esquinas"]):g}px'
        # --esquinas queda disponible para el CSS de cada proyecto: border-radius: var(--esquinas, 4px).
        css.append(f":root {{ --esquinas: {r}; }} .caso, .expediente, .ficha, .cmp-fila, .aviso-ficcion {{ border-radius: {r}; }}"
                   f" .escena {{ border-radius: 0 {r} {r} 0; }}"
                   + (f" .bloque-chip, .bloque-btn {{ border-radius: {r}; }}" if eti != "linea" else ""))
    return " ".join(css)

def variables_css(tema: dict) -> str:
    c, t = tema["colores"], tema["tipografias"]
    lineas = [f"--{rol}: {c[rol]};" for rol, _, _ in ROLES]
    lineas.append("--primario-rgb: " + ", ".join(str(x) for x in _rgb(c["primario"])) + ";")
    lineas += [f"--fuente-{k}: {t[k]};" for k in ("texto", "titulos", "escena")]
    css = ":root { " + " ".join(lineas) + " }"
    # Serie opcional: cada bloque (H2) toma un color de la lista, en ciclo, con sus tonos derivados.
    serie = tema.get("serie", [])
    for n in range(1, 41) if serie else ():
        c = serie[(n - 1) % len(serie)]
        tonos = {"primario": c, "oscuro": mezclar(c, "#000000", .38), "fondo": mezclar(c, "#ffffff", .95),
                 "borde": mezclar(c, "#ffffff", .81), "linea": mezclar(c, "#ffffff", .88),
                 "tenue": mezclar(c, "#ffffff", .55), "fondo-suave": mezclar(c, "#ffffff", .97),
                 "fondo-medio": mezclar(c, "#ffffff", .84), "primario-vivo": mezclar(c, "#ffffff", .25)}
        decl = " ".join(f"--{k}: {v};" for k, v in tonos.items())
        decl += " --primario-rgb: " + ", ".join(str(x) for x in _rgb(c)) + ";"
        css += f"\n    .bloque-{n} {{ {decl} }}"
    return css

def aplicar_tema(page: str, tema: dict) -> str:
    """Rellena los marcadores de la carcasa ({{fuentes_url}}, colores en URIs de datos)."""
    if tema["tipografias"]["url"]:
        page = page.replace("{{fuentes_url}}", tema["tipografias"]["url"])
    else:  # tema con fuentes del sistema: sin hoja de Google Fonts
        page = re.sub(r'[ \t]*<link href="\{\{fuentes_url\}\}" rel="stylesheet">\n?', "", page)
    for rol, _, _ in ROLES:
        page = page.replace("{{" + rol + "}}", "%23" + tema["colores"][rol].lstrip("#"))
    return page

_ATRIBUTOS_COLOR = ("fill", "stroke", "stop-color", "flood-color", "lighting-color")

def colores_a_variables(html: str) -> str:
    """Pasa los colores con rol del .md a variables CSS, para que cada gráfico siga los colores de su bloque.

    - En los atributos style="…", el color se sustituye por var(--rol).
    - Los atributos SVG fill, stroke… no admiten var(): se pasan a la declaración style del elemento,
      delante de lo que ya tuviera (lo que ya estaba en style sigue mandando).
    """
    a_rol = {}
    for rol, teal, morado in ROLES:
        a_rol[teal] = a_rol[morado] = rol
    hex_re = re.compile(r"#[0-9a-fA-F]{6}(?![0-9a-fA-F])|#[0-9a-fA-F]{3}(?![0-9a-fA-F])")

    def en_css(texto: str) -> str:
        texto = hex_re.sub(lambda m: f"var(--{a_rol[m.group(0).lower()]})" if m.group(0).lower() in a_rol else m.group(0), texto)
        for pref in ("rgba(0, 114, 107, ", "rgba(123, 44, 191, ", "rgba(0,114,107,", "rgba(123,44,191,"):
            texto = texto.replace(pref, "rgba(var(--primario-rgb), ")
        return texto

    def etiqueta(m):
        tag = m.group(0)
        movidos = []
        def atributo(am):
            valor = am.group(2)
            if valor.lower() in a_rol or valor.startswith(("rgba(0, 114, 107", "rgba(123, 44, 191", "rgba(0,114,107", "rgba(123,44,191")):
                movidos.append(f"{am.group(1)}: {en_css(valor)}")
                return ""
            return am.group(0)
        tag = re.sub(r'\s(' + "|".join(_ATRIBUTOS_COLOR) + r')="([^"]*)"', atributo, tag)
        tag = re.sub(r'\sstyle="([^"]*)"', lambda sm: f' style="{en_css(sm.group(1))}"', tag)
        if movidos:
            previo = "; ".join(movidos)
            if re.search(r'\sstyle="', tag):
                tag = re.sub(r'\sstyle="', lambda _: f' style="{previo}; ', tag, count=1)
            else:
                tag = re.sub(r"\s*(/?>)$", lambda e: f' style="{previo}"{e.group(1)}', tag, count=1)
        return tag

    return re.sub(r"<[a-zA-Z][^<>]*>", etiqueta, html)

def traducir_colores(html: str, tema: dict) -> str:
    """Traduce los colores escritos en el .md (de los temas teal o morado) a los del tema elegido."""
    a_valor = {}
    for rol, teal, morado in ROLES:
        a_valor[teal] = a_valor[morado] = tema["colores"][rol]
    html = re.sub(r"#[0-9a-fA-F]{6}(?![0-9a-fA-F])|#[0-9a-fA-F]{3}(?![0-9a-fA-F])",
                  lambda x: a_valor.get(x.group(0).lower(), x.group(0)), html)
    for rol, teal, morado in ROLES:
        for origen in (teal, morado):
            if len(origen) == 7:
                html = html.replace("%23" + origen[1:], "%23" + tema["colores"][rol].lstrip("#"))
    r, g, b = _rgb(tema["colores"]["primario"])
    for pref in ("rgba(0, 114, 107, ", "rgba(123, 44, 191, "):
        html = html.replace(pref, f"rgba({r}, {g}, {b}, ")
    for pref in ("rgba(0,114,107,", "rgba(123,44,191,"):
        html = html.replace(pref, f"rgba({r},{g},{b},")
    return html

def logo_data_uri(ruta: Path, h: int = 128) -> str:
    from PIL import Image
    im = Image.open(ruta)
    im = im.resize((round(im.width * h / im.height), h))
    buf = io.BytesIO(); im.save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# Claves de identidad.json. Las rutas son relativas a la carpeta del propio identidad.json.
#   tema      nombre de un tema de la skill o ruta a un .json de tema del proyecto
#   logo      imagen de la cabecera
#   producto  nombre del producto (cabecera y pie)
#   tipo      tipo de documento (pie)
#   css       hoja (o lista de hojas) con los componentes propios del proyecto
#   reglas    reglas de redacción del dominio; no las usa el script, las lee quien redacta (ver SKILL.md)
#   js        scripts de componentes propios; solo los usa documento_a_html.py
#   herramientas  herramientas del documento para todo el proyecto (ver HERRAMIENTAS)
#   destino   para quién es el artefacto: «proyecto» (manda el .md) o «usuario» (el .html es el entregable)
#   iconos    iconos propios de las tarjetas: nombre → trazos SVG de 24 × 24 o ruta a un .svg (documento_a_html.py)
CLAVES_IDENTIDAD = {"tema", "logo", "producto", "tipo", "css", "reglas", "js", "herramientas", "destino", "iconos"}

# Catálogo de herramientas y opciones de lectura del documento (tools/kit_documentos/).
# nombre: (qué hace, valor inicial si es para el proyecto, valor inicial si es para el usuario, el lector lo ajusta).
# Se eligen por documento («herramientas:» y «destino:» en la cabecera del .md, o en identidad.json). Las que el lector
# ajusta aparecen en «Lectura» (el modal del engranaje, a la izquierda de la barra) con el valor que ha elegido el autor como punto de partida.
HERRAMIENTAS = {
    "buscador": ("Buscar en el documento", True, True, False),
    "notas": ("Notas personales; barra con la versión y «Guardar»", True, True, False),
    "nota-texto": ("Con «notas»: anotar un texto seleccionado («Anotar»)", True, True, False),
    "nota-seccion": ("Con «notas»: una nota por sección, que aparece sola al leerla y se ve también en su sitio", True, True, False),
    "nota-global": ("Con «notas»: una nota general de todo el documento", True, True, False),
    "lectura": ("«Lectura» (engranaje a la izquierda de la barra): el lector ajusta las opciones marcadas como ajustables", True, True, False),
    "fuentes": ("Bocadillo con la fuente al pasar por una referencia, y la frase que respalda resaltada", True, True, True),
    "cabecera": ("Título de la sección abierta fijo arriba mientras se lee", True, True, True),
    "tablas": ("Ancho de las columnas de tabla ajustable arrastrando su borde", True, True, False),
    "aviso": ("Aviso al cerrar si hay cambios que solo están en la página (párrafos editados o añadidos)", True, True, False),
    "leyenda": ("«Cómo leer este documento», con muestras de lo que el documento usa", False, True, False),
    "edicion": ("Editar párrafos en su sitio, con su trazabilidad", False, True, False),
    "nota-a-parrafo": ("Con «notas»: convertir una nota en párrafo del documento, con «Añadido · fecha» y «Retirar»", False, True, False),
    "mismo-archivo": ("«Guardar» escribe sobre el mismo archivo, sin preguntar después de la primera vez", False, True, False),
    "acordeon": ("Un solo bloque abierto a la vez", False, False, True),
    "bocadillos": ("Los subapartados de detalle se abren en un bocadillo, sin desplazar el texto", False, False, True),
}
DESTINOS = ("proyecto", "usuario")
# Retiradas del catálogo: se aceptan en documentos antiguos y no hacen nada.
RETIRADAS = {"oscuro": "los documentos abren siempre en claro y el lector elige el oscuro en «Lectura»"}


def faltan_opciones(destino, herramientas) -> None:
    """Sin destino o sin herramientas, el generador no elige por el autor: se detiene y enseña las opciones."""
    faltan = [n for n, v in (("destino", destino), ("herramientas", herramientas)) if v is None or str(v).strip() == ""]
    if not faltan:
        return
    filas = "\n".join(f"    {n:<15}{'sí' if x[1] else 'no'} / {'sí' if x[2] else 'no'}  {x[0]}" for n, x in HERRAMIENTAS.items())
    sys.exit(
        f"Falta elegir {' y '.join(faltan)} del documento. Pregunta al autor y anótalo: en la visión, "
        "«<!-- destino: … -->» y «<!-- herramientas: … -->» al principio del .md; en el fundacional, «destino:» y "
        "«herramientas:» en su cabecera; para todo el proyecto, en identidad.json; o con --destino y --herramientas.\n"
        "  destino: proyecto (manda el .md) | usuario (el .html es el entregable)\n"
        "  herramientas: recomendadas (las del destino) | todas | ninguna | una lista | cambios («+leyenda -tablas»)\n"
        "  Catálogo (recomendada para proyecto / usuario):\n" + filas)


def destino_documento(valor) -> str:
    v = str(valor or "").strip().lower()
    if v not in DESTINOS:
        sys.exit(f"Destino desconocido: «{v}». Posibles: {', '.join(DESTINOS)}.")
    return v


def herramientas_activas(valor, destino) -> str:
    """Herramientas para <html data-herramientas>. «valor»: «recomendadas» (las del destino), «todas», «ninguna», una
    lista de nombres del catálogo o cambios sobre las recomendadas («+leyenda -tablas»). Sin destino o sin valor, error."""
    faltan_opciones(destino, valor)
    d = destino_documento(destino)
    base = [n for n, x in HERRAMIENTAS.items() if x[1 if d == "proyecto" else 2]]
    nombres = valor if isinstance(valor, list) else re.split(r"[\s,]+", str(valor).strip())
    nombres = [n for n in nombres if n]
    for n in [n for n in nombres if n.lstrip("+-") in RETIRADAS]:
        print(f"Aviso: «{n.lstrip('+-')}» ya no es una opción ({RETIRADAS[n.lstrip('+-')]}); se ignora.")
        nombres.remove(n)
    if nombres in (["recomendadas"], []):
        elegidas = base
    else:
        if nombres in (["ninguna"], ["no"]):
            return "ninguna"
        if "todas" in nombres:  # «todas -tablas»: todas menos las que se quitan
            base, nombres = list(HERRAMIENTAS), [n if n[0] in "+-" else "-" + n for n in nombres if n != "todas"]
        if True:
            relativo = any(n[0] in "+-" for n in nombres) or not nombres
            elegidas = list(base) if relativo else []
            malas = [n.lstrip("+-") for n in nombres if n.lstrip("+-") not in HERRAMIENTAS]
            if malas:
                sys.exit(f"Herramientas desconocidas: {', '.join(malas)}. Catálogo: {', '.join(HERRAMIENTAS)}.")
            for n in nombres:
                k = n.lstrip("+-")
                if n.startswith("-"):
                    elegidas = [x for x in elegidas if x != k]
                elif k not in elegidas:
                    elegidas.append(k)
    print(f"Herramientas ({d}): {' '.join(elegidas) or 'ninguna'}")
    return " ".join(elegidas) or "ninguna"


# Bloques de código del kit. La biblioteca está en tools/kit_documentos/, junto a skills/ (en el repositorio de la SF
# y en ~/.claude). Cada bloque lleva data-kit con su ruta desde esa carpeta común, para que
# tools/kit_documentos/actualizar_copia.py pueda poner al día una copia ya repartida sin tocar su contenido.
BASE = Path(__file__).resolve().parent.parent.parent.parent
KIT = BASE / "tools" / "kit_documentos"
if not (KIT / "herramientas.js").is_file():
    sys.exit(f"Falta la biblioteca de herramientas de los documentos: no encuentro {KIT / 'herramientas.js'}")
KIT_ESTILOS = ("tools/kit_documentos/herramientas.css",)
KIT_SCRIPTS = ("tools/kit_documentos/herramientas.js", "tools/kit_documentos/lectura.js",
               "tools/kit_documentos/edicion.js")


def bloque_kit(ruta: str) -> str:
    cuerpo = (BASE / ruta).read_text(encoding="utf-8").rstrip()
    etiqueta = "style" if ruta.endswith(".css") else "script"
    return f'<{etiqueta} data-kit="{ruta}">\n{cuerpo}\n</{etiqueta}>'


def kit_estilos() -> str:
    return "".join("\n  " + bloque_kit(r) for r in KIT_ESTILOS)


def kit_scripts() -> str:
    return "".join("\n" + bloque_kit(r) for r in KIT_SCRIPTS)


def enlaces_externos(html: str) -> str:
    """Los enlaces a otras webs se abren aparte (target, rel) y lo dicen con ↗, salvo si el texto ya lo lleva."""
    def uno(m):
        a, texto = m.group(1), m.group(2)
        if "target=" in a:
            return m.group(0)
        clase = "" if "↗" in texto else " externo"
        if 'class="' in a:
            a = a.replace('class="', f'class="{clase.strip()} ', 1) if clase else a
        elif clase:
            a += ' class="externo"'
        return f'<a{a} target="_blank" rel="noopener noreferrer">{texto}</a>'
    return re.sub(r'<a(\s[^>]*href="https?://[^"]*"[^>]*)>(.*?)</a>', uno, html, flags=re.S)


def procedencia(md: Path) -> str:
    """Pie con la procedencia: fecha de generación, huella del .md, commit corto y aviso de cambios sin commit."""
    import datetime, hashlib, subprocess
    partes = ["Generado el " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
              f"fuente {md.name} · huella {hashlib.sha256(md.read_bytes()).hexdigest()[:12]}"]
    try:
        run = lambda *a: subprocess.run(["git", *a], cwd=md.parent, capture_output=True, text=True, timeout=10)
        c = run("log", "-1", "--format=%h", "--", md.name)
        if c.returncode == 0 and c.stdout.strip():
            sucio = run("status", "--porcelain", "--", md.name).stdout.strip()
            partes.append("commit " + c.stdout.strip() + (" (con cambios sin commit)" if sucio else ""))
        elif c.returncode == 0:
            partes.append("sin commit")
    except Exception:
        pass
    return " · ".join(partes)


def buscar_identidad(md: Path, indicada: str | None) -> Path | None:
    """identidad.json del proyecto: todo lo propio del proyecto (tema, logo, producto, CSS, reglas)."""
    if indicada == "ninguna":
        return None
    if indicada:
        ruta = Path(indicada)
        ruta = ruta if ruta.suffix == ".json" else ruta / "identidad.json"
        if not ruta.is_file():
            sys.exit(f"No se encuentra la identidad del proyecto: {ruta}")
        return ruta
    for carpeta in md.resolve().parents:
        for sub in ("doc/identidad", "docs/identidad"):
            ruta = carpeta / sub / "identidad.json"
            if ruta.is_file():
                return ruta
    return None

