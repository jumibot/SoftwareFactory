"""El estilo del proyecto (docs/identidad/estilo.json) para el generador de documentos.

Lo usa documento_a_html.py. El estilo es del proyecto y vale para todos sus documentos (decisiones 305, 316 y 317):
diez grupos de parámetros con sus valores resueltos, la referencia a los archivos del logo, una versión y un historial.
Cada parámetro que falta toma su valor por defecto, que es lo que el generador hacía antes de tenerlo: sin el parámetro,
la salida no cambia. Un grupo, un parámetro o un valor desconocidos detienen el generador y enseñan los posibles.

Sin estilo.json, el generador sale del paso con los valores por defecto de un tema, elegido por el del identidad.json o
por el color de sesión del proyecto (.sf/proyecto.json), y avisa una vez (decisión 323).

Aquí están también la comprobación del contraste (decisión 320) y el CSS de los parámetros que no tienen su valor por
defecto.
"""

from __future__ import annotations

import colorsys, json, re, sys
from pathlib import Path

from tema_identidad import (ROLES_VALIDOS, TEMAS, TIPOGRAFIAS, cargar_tema, contraste, mezclar, normalizar_tema, oscuro_de,
                            ruta_tema, sobre, tonos_serie_oscuro)

HEX = re.compile(r"#[0-9a-fA-F]{6}")

# Colores con significado de las tarjetas («{color=correcto}»): por defecto, los de las tarjetas de hoy.
SIGNIFICADO = {"correcto": "#1f812d", "aviso": "#a6501a", "error": "#be185d", "info": "#1f7a7a"}


def _opciones(*valores):
    def validar(v):
        return v in valores
    validar.posibles = " | ".join(str(v) for v in valores)
    return validar


def _numero(minimo, maximo, entero=False):
    def validar(v):
        tipo = int if entero else (int, float)
        return isinstance(v, tipo) and not isinstance(v, bool) and minimo <= v <= maximo
    validar.posibles = f"{'entero' if entero else 'número'} de {minimo} a {maximo}"
    return validar


def _texto(v):
    return isinstance(v, str) and v.strip() != ""
_texto.posibles = "texto"


def _texto_o_vacio(v):
    return isinstance(v, str)
_texto_o_vacio.posibles = "texto (vacío: fuentes del sistema)"


def _hex(v):
    return isinstance(v, str) and bool(HEX.fullmatch(v))
_hex.posibles = "#rrggbb"


def _ruta_o_lista(v):
    return _texto(v) or (isinstance(v, list) and v and all(_texto(x) for x in v))
_ruta_o_lista.posibles = "ruta o lista de rutas, relativas a docs/identidad/"


def _url(v):
    return isinstance(v, str) and bool(re.match(r"https?://\S+$", v))
_url.posibles = "url (https://…)"


def _opacidad(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and (0.2 <= v <= 0.5 or 0.75 <= v <= 1)
_opacidad.posibles = "de 0.2 a 0.5 (título oscuro) o de 0.75 a 1 (título sobre el primario)"


def _herramientas(v):
    return _texto(v) or (isinstance(v, list) and all(_texto(x) for x in v))
_herramientas.posibles = "recomendadas | todas | ninguna | una lista | cambios («+leyenda -tablas»)"


def _hud(v):
    return v in ("primario", "acento") or _hex(v)
_hud.posibles = "primario | acento | #rrggbb"


def _si_no(v):
    return v in ("si", "sí", "no", True, False)
_si_no.posibles = "si | no"


def _diagramas():
    """Los selectores de la herramienta «Diagramas» (los mismos de generar_diagrama.py, decisión 302) y el tema."""
    import importlib.util
    ruta = Path(__file__).resolve().parent.parent.parent / "diagramas" / "scripts" / "generar_diagrama.py"
    if not ruta.is_file():
        sys.exit(f"Falta la skill de diagramas junto a crear_documentos: no encuentro {ruta}")
    spec = importlib.util.spec_from_file_location("generar_diagrama", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    selectores = {clave: _opciones(*valores) for clave, valores in modulo.SELECTORES.items()}
    temas = sorted(p.stem for p in TEMAS.glob("*.json"))
    selectores["tema"] = _opciones("documento", *temas)
    return selectores


# Los diez grupos: parámetro → validación. El valor por defecto de cada uno es lo que el generador hacía sin él.
CATALOGO = {
    "identidad": {"producto": _texto, "logo": _ruta_o_lista, "logo-oscuro": _texto, "enlace": _url},
    "colores": {**{rol: _hex for rol in sorted(ROLES_VALIDOS)}, "colores-oscuro": None, "serie": None,
                "significado": None},
    "letra": {"texto": _texto, "titulos": _texto, "escena": _texto, "codigo": _texto, "url": _texto_o_vacio,
              "tamano": _opciones(16, 17, 18), "escala": _opciones("editorial", "compacta")},
    "portada": {"forma": _opciones("clara", "oscura", "compacta"), "fondo": _opciones("oscuro", "primario"),
                "linea": _si_no},
    "secciones": {"cabecera": _opciones("numero-etiqueta", "numero-titulo", "titulo"),
                  "etiqueta": _opciones("tinte", "solida", "linea", "ninguna"), "opacidad": _opacidad,
                  "marcador": _opciones("flecha", "circulo", "cuadrado", "ninguno"),
                  "plegado": _opciones("primera", "todas", "ninguna")},
    "pagina": {"ancho": _numero(980, 1400, entero=True), "esquinas": _numero(0, 16), "codigo": _opciones("bloque", "linea"),
               "pie": _opciones("claro", "oscuro"), "filetes": _si_no},
    "recuadros": {"filete": _si_no},
    "lectura": {"destino": _opciones("proyecto", "usuario"), "herramientas": _herramientas,
                "menu": _opciones("botones", "secciones", "no")},
    "diagramas": None,  # se rellena al validar, con los selectores de la skill de diagramas
    "aparte": {"escenario": _opciones("derivado", "claro"), "hud": _hud},
}
# Los valores por defecto, para la documentación y las pruebas (lo que el generador hace sin el parámetro).
POR_DEFECTO = {
    "identidad": {"producto": "el de identidad.json o el título", "logo": "el de identidad.json o ninguno",
                  "logo-oscuro": "el mismo logo", "enlace": "ninguno"},
    "letra": {"tamano": 17, "escala": "editorial"},
    "portada": {"forma": "la del .md o clara", "fondo": "oscuro", "linea": "si"},
    "secciones": {"cabecera": "numero-etiqueta", "etiqueta": "tinte", "opacidad": 1, "marcador": "flecha",
                  "plegado": "primera"},
    "pagina": {"ancho": 1240, "esquinas": "las de cada pieza", "codigo": "bloque", "pie": "claro", "filetes": "si"},
    "recuadros": {"filete": "si"},
    "lectura": {"menu": "botones"},
    "aparte": {"escenario": "derivado", "hud": "primario"},
}
CLAVES = {"version", "origen", "nombre", "historial", *CATALOGO}


def _parar(ruta, texto):
    sys.exit(f"{ruta}: {texto}")


def validar(estilo: dict, ruta) -> dict:
    """Comprueba las claves y los valores de estilo.json. Se detiene con lo desconocido y enseña los posibles."""
    if not isinstance(estilo, dict):
        _parar(ruta, "debe ser un objeto JSON.")
    raras = set(estilo) - CLAVES
    if raras:
        _parar(ruta, f"grupos desconocidos: {', '.join(sorted(raras))}. Posibles: version, origen, nombre, historial, "
                     + ", ".join(CATALOGO) + ".")
    version = estilo.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        _parar(ruta, "falta «version» (un entero desde 1; cada afinado la sube, decisión 322).")
    if "nombre" in estilo and not _texto(estilo["nombre"]):
        _parar(ruta, "«nombre» es el nombre del estilo, un texto («Áureo»).")
    historial = estilo.get("historial", [])
    if not isinstance(historial, list) or not all(isinstance(h, dict) for h in historial):
        _parar(ruta, "«historial» es una lista de {version, fecha, cambio, motivo}.")
    catalogo = dict(CATALOGO, diagramas=_diagramas())
    for grupo, params in catalogo.items():
        valores = estilo.get(grupo, {})
        if not isinstance(valores, dict):
            _parar(ruta, f"el grupo «{grupo}» es un objeto con sus parámetros.")
        raros = set(valores) - set(params)
        if raros:
            _parar(ruta, f"«{grupo}» no tiene {', '.join(sorted(raros))}. Parámetros: {', '.join(params)}.")
        for clave, valor in valores.items():
            comprobar = params[clave]
            if comprobar and not comprobar(valor):
                _parar(ruta, f"«{grupo}.{clave}: {json.dumps(valor, ensure_ascii=False)}» no vale. "
                             f"Posibles: {comprobar.posibles}.")
    colores = estilo.get("colores", {})
    if "primario" not in colores:
        _parar(ruta, "falta «colores.primario», el único color obligatorio.")
    oscuro = colores.get("colores-oscuro", {})
    if not isinstance(oscuro, dict) or set(oscuro) - ROLES_VALIDOS or not all(_hex(v) for v in oscuro.values()):
        _parar(ruta, "«colores.colores-oscuro» es un objeto rol → #rrggbb con los roles de «colores».")
    serie = colores.get("serie", [])
    if not isinstance(serie, list) or not all(_hex(c) for c in serie):
        _parar(ruta, "«colores.serie» es una lista de colores #rrggbb.")
    significado = colores.get("significado", {})
    if (not isinstance(significado, dict) or set(significado) - set(SIGNIFICADO)
            or not all(_hex(v) for v in significado.values())):
        _parar(ruta, f"«colores.significado» es un objeto con {', '.join(SIGNIFICADO)} → #rrggbb.")
    return estilo


# --- Dónde está ----------------------------------------------------------------------------------

def buscar_estilo(md: Path, identidad: str | None, indicado: str | None) -> Path | None:
    """estilo.json del proyecto: el indicado (--estilo), el de la carpeta de --identidad, o docs/identidad/estilo.json
    subiendo desde el .md. Con --identidad ninguna y sin --estilo, ninguno."""
    if indicado == "ninguno":
        return None
    if indicado:
        ruta = Path(indicado)
        ruta = ruta if ruta.suffix == ".json" else ruta / "estilo.json"
        if not ruta.is_file():
            sys.exit(f"No se encuentra el estilo del proyecto: {ruta}")
        return ruta
    if identidad == "ninguna":
        return None
    if identidad:
        ruta = Path(identidad)
        ruta = (ruta.parent if ruta.suffix == ".json" else ruta) / "estilo.json"
        return ruta if ruta.is_file() else None
    for carpeta in md.resolve().parents:
        for sub in ("doc/identidad", "docs/identidad"):
            ruta = carpeta / sub / "estilo.json"
            if ruta.is_file():
                return ruta
    return None


def cargar(ruta: Path) -> dict:
    try:
        estilo = json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"{ruta} no es JSON válido: {e}")
    return validar(estilo, ruta)


# --- Sin estilo.json: el tema por el color del proyecto (decisión 323) ------------------------------

COLORES_SESION = {"red": "#dc2626", "orange": "#ea580c", "yellow": "#ca8a04", "green": "#16a34a",
                  "cyan": "#0891b2", "blue": "#2563eb", "purple": "#7c3aed", "pink": "#db2777"}


def _tono(color: str) -> float:
    r, g, b = (int(color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return colorsys.rgb_to_hsv(r, g, b)[0]


def tema_por_color(color: str) -> str:
    """El tema del catálogo cuyo primario tiene el tono más cercano al color de sesión («blue») o a un #rrggbb."""
    ref = COLORES_SESION.get(color, color)
    if not _hex(ref):
        return "morado"
    t = _tono(ref)
    def distancia(p):
        d = abs(_tono(json.loads(p.read_text(encoding="utf-8"))["colores"]["primario"]) - t)
        return (min(d, 1 - d), p.stem)
    return min(TEMAS.glob("*.json"), key=distancia).stem


def color_del_proyecto(md: Path) -> str | None:
    """El color de sesión de .sf/proyecto.json, subiendo desde el .md."""
    for carpeta in md.resolve().parents:
        ruta = carpeta / ".sf" / "proyecto.json"
        if ruta.is_file():
            try:
                return json.loads(ruta.read_text(encoding="utf-8")).get("color")
            except (json.JSONDecodeError, AttributeError):
                return None
    return None


def tema_sin_estilo(src: Path, identidad: dict, ruta_id: Path | None, tema_indicado: str | None) -> tuple[dict, str]:
    """Sin estilo.json, los valores por defecto de un tema (decisión 323) y el aviso que lo dice: el indicado (--tema),
    el de identidad.json, el más cercano al color de sesión del proyecto o «morado». Lo usan el generador de documentos
    y el estilo de la infografía técnica."""
    tema_id = identidad.get("tema")
    if tema_id and tema_id.endswith(".json") and ruta_id:
        tema_id = str(ruta_id.parent / tema_id)
    color = None if tema_indicado or tema_id else color_del_proyecto(src)
    if tema_indicado:
        nombre, por = tema_indicado, "indicado con --tema"
    elif tema_id:
        nombre, por = tema_id, "el de identidad.json"
    elif color:
        nombre, por = tema_por_color(color), f"por el color de sesión del proyecto, {color}"
    else:
        nombre, por = "morado", "el de siempre"
    tema = cargar_tema(nombre)
    aviso = (f"Aviso: el proyecto no tiene estilo (docs/identidad/estilo.json): se genera con los valores por defecto "
             f"del tema «{tema.get('nombre', nombre)}» ({por}).")
    return tema, aviso


# --- Del estilo al tema ----------------------------------------------------------------------------

def tema_del_estilo(estilo: dict, ruta: Path) -> dict:
    """El tema que entiende el generador (colores, versión oscura, serie y tipografías) con los valores del estilo."""
    colores = dict(estilo.get("colores", {}))
    tema = {"nombre": f"estilo v{estilo['version']}",
            "colores": {k: v for k, v in colores.items() if k in ROLES_VALIDOS},
            "colores-oscuro": colores.get("colores-oscuro", {}), "serie": colores.get("serie", [])}
    letra = estilo.get("letra", {})
    tipos = {k: letra[k] for k in ("texto", "titulos", "escena", "url") if k in letra}
    if tipos:
        tema["tipografias"] = tipos
    return normalizar_tema(tema, ruta.name)


def significado(estilo: dict | None) -> dict:
    return {**SIGNIFICADO, **((estilo or {}).get("colores", {}).get("significado", {}))}


def param(estilo: dict | None, grupo: str, clave: str, defecto=None):
    return ((estilo or {}).get(grupo) or {}).get(clave, defecto)


# --- Contraste (decisión 320) --------------------------------------------------------------------------

def comprobar_contraste(tema: dict, estilo: dict | None) -> tuple[list[str], list[str]]:
    """(textos por debajo de 4,5:1 —3:1 el grande—, bordes y líneas por debajo de 3:1) con los colores del tema y lo que
    el estilo pide, en claro y en oscuro (decisión 347). Cada par es un uso real de la maqueta: color del texto, fondo,
    dónde se ve y si es grande. Lo del oscuro lo dice delante («en oscuro»)."""
    errores, avisos = _contraste_modo(tema["colores"], tema, estilo, oscuro=False)
    e2, a2 = _contraste_modo(tema["colores-oscuro"], tema, estilo, oscuro=True)
    return errores + [f"en oscuro, {x}" for x in e2], avisos + [f"en oscuro, {x}" for x in a2]


def _contraste_modo(colores: dict, tema: dict, estilo: dict | None, oscuro: bool) -> tuple[list[str], list[str]]:
    c = dict(colores, blanco="#ffffff")
    pares = [  # (texto, fondo, dónde, grande)
        ("texto", "pagina", "texto sobre la página", False),
        ("texto", "superficie", "texto de tarjetas y tablas", False),
        ("texto-suave", "pagina", "texto secundario", False),
        ("texto-suave", "superficie", "texto secundario en tarjetas y tablas", False),
        ("primario-texto", "pagina", "enlaces y rótulos sobre la página", False),
        ("primario-texto", "superficie", "enlaces y rótulos en la portada, tarjetas y menú", False),
        ("primario-texto", "fondo", "rótulos de los recuadros", False),
        ("sobre-primario", "primario", "texto de los botones y las marcas sobre el primario", False),
        ("primario-linea", "pagina", "líneas y bordes de los diagramas en el color del proyecto", True),
        ("primario-linea", "superficie", "líneas y bordes de los diagramas sobre las tarjetas", True),
        ("sobre-cabecera", "cabecera", "texto de la portada destacada con el color del proyecto", False),
        ("blanco", "oscuro", "texto de la portada oscura, de las cabeceras de tabla y de los botones al pasar", False),
        ("primario" if oscuro else "tenue", "oscuro",
         "marca de la portada oscura y rótulos de los recuadros de decisión", False),
        ("acento", "acento-fondo", "rótulo de los recuadros de aviso", False),
        ("acento", "superficie", "pregunta abierta", False),
        ("tinta-oscura", "fondo-medio", "insignias y decisiones", False),
        ("tinta-oscura", "superficie", "botones y rótulos de las herramientas", False),
    ]
    if param(estilo, "secciones", "etiqueta") == "solida":
        op = float(param(estilo, "secciones", "opacidad", 1))
        tras = mezclar(c["pagina"], c["primario"], op)
        c["cabecera-solida"] = tras
        rotulo = "sobre-primario" if op >= .75 else "tinta-oscura"
        pares.append((rotulo, "cabecera-solida", "número y etiqueta de la cabecera de sección sólida", False))
        pares.append((rotulo, "cabecera-solida", "título de la cabecera de sección sólida", True))
    for i, s in enumerate(tema.get("serie", []), 1):
        tonos = tonos_serie_oscuro(s, colores) if oscuro else {"primario": s, "sobre-primario": sobre(s, c["texto"])}
        c[f"serie-{i}"] = tonos["primario"]
        c[f"sobre-serie-{i}"] = tonos["sobre-primario"]
        pares.append((f"serie-{i}", "pagina", f"rótulos de las secciones en el color {i} de la serie", False))
        pares.append((f"sobre-serie-{i}", f"serie-{i}", f"texto sobre el color {i} de la serie", False))
        if oscuro:  # en oscuro, el color del bloque rotula también su fondo tintado y los recuadros de decisión
            c[f"fondo-serie-{i}"] = tonos["fondo"]
            pares.append((f"serie-{i}", f"fondo-serie-{i}", f"rótulos sobre el fondo del color {i} de la serie", False))
            pares.append((f"serie-{i}", "oscuro", f"rótulos de las decisiones en el color {i} de la serie", False))
    for nombre, valor in significado(estilo).items():
        c[f"significado-{nombre}"] = valor
        pares.append(("blanco", f"significado-{nombre}", f"cabecera de las tarjetas «{nombre}»", False))
        if oscuro:
            c[f"texto-{nombre}"] = oscuro_de(valor, colores)
            pares.append((f"texto-{nombre}", "superficie", f"campos de las tarjetas «{nombre}»", False))
    errores = []
    for texto, fondo, donde, grande in pares:
        minimo = 3 if grande else 4.5
        r = contraste(c[texto], c[fondo])
        if r < minimo - 1e-9:
            errores.append(f"{donde}: {_nombre(texto)} {c[texto]} sobre {_nombre(fondo)} {c[fondo]} da {r:.2f}:1 "
                           f"(mínimo {minimo:g}:1)")
    avisos = []
    # Los campos, a 3:1; las cajas, fuera del aviso: su borde es suave a propósito (decisión 335, 9).
    for linea, fondo, donde in (("borde-campo", "pagina", "bordes de los campos"),
                                ("borde-campo", "superficie", "bordes de los campos sobre las tarjetas"),
                                ("texto-tenue", "pagina", "líneas y zonas de los diagramas")):
        r = contraste(c[linea], c[fondo])
        if r < 3 - 1e-9:
            avisos.append(f"{donde}: {_nombre(linea)} {c[linea]} sobre {_nombre(fondo)} {c[fondo]} da {r:.2f}:1 "
                          "(mínimo 3:1)")
    return errores, avisos


def _nombre(rol: str) -> str:
    return "blanco" if rol == "blanco" else f"«{rol}»"


# --- CSS de los parámetros ------------------------------------------------------------------------------
# Solo lo que cambia respecto al valor por defecto: sin parámetros, nada (la salida, como antes de tenerlos).

def css_parametros(estilo: dict | None) -> str:
    if not estilo:
        return ""
    css = []
    letra = estilo.get("letra", {})
    if letra.get("tamano", 17) != 17:
        n = letra["tamano"]
        css.append(f"@media screen {{ body {{ font-size: {n / 16:g}rem; }} }}"
                   f" @media screen and (min-width: 1600px) {{ body {{ font-size: {(n + 1) / 16:g}rem; }} }}")
    if letra.get("escala") == "compacta":
        css.append(".titular { font-size: clamp(1.5rem, 3vw, 1.9rem); } .seccion h2 { font-size: 1.05rem; line-height: 1.3; }"
                   " .seccion h3 { font-size: 1rem; } .seccion { padding-top: 1.6rem; }")
    if letra.get("codigo"):
        css.append(f"code, pre, kbd, .formula {{ font-family: {letra['codigo']}; }}")
    portada = estilo.get("portada", {})
    if portada.get("forma") == "compacta":
        css.append(".portada.compacta { padding: .9rem 0 .7rem; } .portada.compacta .titular { font-size: clamp(1.35rem, 2.6vw, 1.75rem); }"
                   " .portada.compacta .subtitulo { font-size: 1rem; margin-bottom: .7rem; }"
                   " .portada.compacta .idea p { font-size: .95rem; }")
    if portada.get("fondo") == "primario":
        # El color de cabecera del estilo, un tono del primario menos brillante, y su texto (decisión 351)
        css.append(".portada.oscura { background: var(--cabecera); color: var(--sobre-cabecera); }"
                   " .portada.oscura .marca, .portada.oscura .tipo-doc, .portada.oscura .subtitulo, .portada.oscura .idea p, .portada.oscura a,"
                   " .portada.oscura .datos-version, .portada.oscura .datos-version span, .portada.oscura .cifras strong,"
                   " .portada.oscura .cifras span { color: var(--sobre-cabecera); }")
        css.append("@media print { .portada.oscura, .portada.oscura :is(.marca, .tipo-doc, .subtitulo, .idea p, a, .datos-version,"
                   " .datos-version span, .cifras strong, .cifras span) { color: var(--texto); } }")
    secc = estilo.get("secciones", {})
    etiqueta = secc.get("etiqueta", "tinte")
    if etiqueta == "solida":
        op = float(secc.get("opacidad", 1))
        fondo = "var(--primario)" if op >= 1 else f"rgba(var(--primario-rgb), {op:g})"
        rotulo = "var(--sobre-primario)" if op >= .75 else "var(--tinta-oscura)"
        # Con un hueco debajo: sin él, la entradilla queda pegada a la banda (informe de estilo, SF-2)
        css.append(f".seccion-titulo {{ background: {fondo}; padding: .8rem 1rem; }}"
                   " .seccion[open] > .seccion-titulo { margin-bottom: 1.1rem; }"
                   f" .seccion-titulo .etiqueta, .seccion-titulo h2, .seccion-titulo:hover h2,"
                   f" .seccion-titulo .seccion-numero {{ color: {rotulo}; }}"
                   f" .seccion-titulo::after {{ border-color: {rotulo}; }}")
    elif etiqueta == "linea":
        css.append(".seccion-titulo { border-left: 4px solid var(--primario); border-radius: 0; padding-left: .8rem; }")
    elif etiqueta == "ninguna":
        css.append(".seccion-titulo .etiqueta, .seccion-titulo .seccion-numero { color: var(--texto-suave); }")
    marcador = secc.get("marcador", "flecha")
    if marcador in ("circulo", "cuadrado"):
        radio = "50%" if marcador == "circulo" else "2px"
        css.append(f".seccion-titulo::after {{ width: .8rem; height: .8rem; border: 2px solid var(--primario); border-radius: {radio};"
                   " transform: none; margin: .65rem .4rem 0; }"
                   " .seccion[open] > .seccion-titulo::after { transform: none; background: var(--primario); }")
        if etiqueta == "solida":
            css.append(".seccion-titulo::after, .seccion[open] > .seccion-titulo::after { border-color: currentColor; }"
                       " .seccion[open] > .seccion-titulo::after { background: currentColor; }")
    elif marcador == "ninguno":
        css.append(".seccion-titulo::after { display: none; }")
    pagina = estilo.get("pagina", {})
    if pagina.get("ancho", 1240) != 1240:
        a = pagina["ancho"]
        css.append(f".hoja, .portada-dentro, .menu-dentro {{ width: min({a}px, 100% - 32px); }}"
                   f" @media (min-width: 1025px) {{ .hoja, .portada-dentro, .menu-dentro {{ width: min({a}px, 100% - 64px); }} }}")
    if "esquinas" in pagina:
        css.append(f":root {{ --esquinas: {float(pagina['esquinas']):g}px; }}")
    if pagina.get("codigo") == "linea":  # «bloque», el de por defecto, está en estilo_documento.css
        css.append("pre { background: none; border-left: 0; border-radius: 0; border-top: 1px solid var(--borde);"
                   " border-bottom: 1px solid var(--borde); padding: .8rem 0; }")
    if pagina.get("filetes") in ("no", False):  # sin los filetes que separan la portada clara, el menú y el pie
        css.append(".portada, .menu { border-bottom: 0; } .pie { border-top: 0; }")
    if estilo.get("recuadros", {}).get("filete") in ("no", False):  # recuadros sin la barra izquierda
        css.append(".recuadro:not(.decision) { border-left: 0; border-radius: var(--esquinas, 8px); }")
    if pagina.get("pie") == "oscuro":
        css.append(".pie { background: var(--oscuro); color: rgba(255,255,255,.86); border: 0; padding: 1.2rem 1.4rem 2rem;"
                   " border-radius: var(--esquinas, 6px) var(--esquinas, 6px) 0 0; } .pie a { color: #fff; }"
                   " .pie .procedencia { color: rgba(255,255,255,.72); }")
    return " ".join(css)


def aplicar_diagramas(html: str, estilo: dict | None) -> str:
    """Los valores de partida de los diagramas del proyecto en cada figura (data-d-…): el lector los sigue cambiando con
    la herramienta «Diagramas». «tema: documento» quita el tema propio de la figura, que toma el del documento (307)."""
    ajustes = (estilo or {}).get("diagramas", {})
    if not ajustes:
        return html

    def figura(m):
        tag = m.group(0)
        for clave, valor in ajustes.items():
            if clave == "tema" and valor == "documento":
                tag = re.sub(r'\sdata-d-tema="[^"]*"', "", tag)
                continue
            atributo = f'data-d-{clave}="{valor}"'
            if re.search(rf'\sdata-d-{re.escape(clave)}="', tag):
                tag = re.sub(rf'data-d-{re.escape(clave)}="[^"]*"', atributo, tag)
            else:
                tag = tag[:-1] + f" {atributo}>"
        return tag
    return re.sub(r'<figure\b[^>]*class="diagrama[^"]*"[^>]*>', figura, html)
