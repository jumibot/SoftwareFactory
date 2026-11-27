"""Temas e identidad de proyecto, compartidos por los generadores HTML de la SF (skill crear_documentos).

Lo usa documento_a_html.py, el generador único de crear_documentos, con el que generan todos los tipos de documento
(el fundacional, los informes, la visión y los explicativos). Carga un tema de assets/temas/ o del proyecto, deriva sus
tonos, produce las variables CSS y busca el identidad.json del proyecto.
"""

from __future__ import annotations

import base64, io, json, re, sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
TEMAS = ASSETS / "temas"

# Roles de color de los temas. Cada rol es una variable CSS (--<rol>) que usan las hojas de estilos de los documentos.
# En el .md, los gráficos pueden escribir el color de un rol en el tema teal o en el morado: el
# generador lo pasa a la variable del rol. Orden: rol, valor en el tema teal, valor en el tema morado.
ROLES = [
    ("primario", "#00726b", "#7b2cbf"), ("oscuro", "#004d47", "#4c1d80"), ("primario-vivo", "#009690", "#9d5ce0"),
    ("fondo", "#e0f4f3", "#f8f5ff"), ("borde", "#b2deda", "#e4d7f5"), ("linea", "#e0eceb", "#ece4f7"),
    ("fondo-medio", "#d4ecea", "#e6dcf4"), ("fondo-suave", "#f0faf9", "#fbf9fe"), ("tenue", "#7dffd9", "#c4b5d9"),
    ("pagina", "#f2f4f4", "#faf8fd"), ("texto", "#1a1a1a", "#2b2b2f"), ("texto-suave", "#555", "#6b7280"),
    ("texto-tenue", "#888", "#9ca3af"), ("acento", "#6d28d9", "#b45309"), ("acento-fondo", "#ede9fe", "#fff7ed"),
    ("acento-borde", "#c4b5fd", "#fcd9b6"),
    ("segundo", "#2f5597", "#2f5598"),   # segundo color: lo que no es el foco ni el acento (el recorrido de un diagrama)
]

# Roles que no traducen colores del .md (no están en ROLES): se derivan si faltan. «sobre-primario» y
# «primario-texto», los del primario claro (decisión 319); «tinta-oscura», la tinta fuerte sobre fondo claro, que en
# oscuro pasa a clara, mientras «oscuro» queda como superficie oscura (349); «superficie», el fondo de tarjetas,
# tablas, menús y paneles (blanco en claro); «cabecera» y «sobre-cabecera», el fondo de la portada destacada con el
# color del proyecto y su texto: un tono del primario menos brillante (351).
ROLES_PROPIOS = ("sobre-primario", "primario-texto", "tinta-oscura", "superficie", "cabecera", "sobre-cabecera",
                 "primario-linea", "borde-campo")
ROLES_VALIDOS = {r for r, _, _ in ROLES} | set(ROLES_PROPIOS)

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
COLORES_MINIMOS = {"texto": "#2b2b2f", "acento": "#b45309", "segundo": "#2f5597"}  # el tema solo tiene que dar «primario»
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

def ruta_tema(nombre_o_ruta: str) -> Path:
    ruta = Path(nombre_o_ruta)
    if ruta.suffix != ".json":
        ruta = TEMAS / f"{nombre_o_ruta}.json"
    if not ruta.is_file():
        disponibles = ", ".join(sorted(p.stem for p in TEMAS.glob("*.json")))
        sys.exit(f"Tema no encontrado: {nombre_o_ruta}. Temas disponibles: {disponibles}")
    return ruta

def cargar_tema(nombre_o_ruta: str) -> dict:
    ruta = ruta_tema(nombre_o_ruta)
    return normalizar_tema(json.loads(ruta.read_text(encoding="utf-8")), ruta.name)

def luminancia(color: str) -> float:
    canales = []
    for c in _rgb(color):
        c /= 255
        canales.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * canales[0] + 0.7152 * canales[1] + 0.0722 * canales[2]

def contraste(a: str, b: str) -> float:
    """Contraste WCAG entre dos colores #rrggbb (de 1 a 21)."""
    la, lb = luminancia(a), luminancia(b)
    return (max(la, lb) + .05) / (min(la, lb) + .05)

def sobre(fondo: str, tinta: str = "#2b2b2f") -> str:
    """El color de texto con más contraste sobre «fondo»: blanco o la tinta del texto. En empate, blanco."""
    return "#ffffff" if contraste("#ffffff", fondo) >= contraste(tinta, fondo) else tinta

def legible(color: str, fondos: list, hacia: str, minimo: float = 4.5) -> str:
    """El color, mezclado con «hacia» (negro o blanco) lo justo para leerse a «minimo»:1 sobre todos los fondos."""
    for paso in range(41):
        c = mezclar(color, hacia, paso / 40)
        if all(contraste(c, f) >= minimo for f in fondos):
            return c
    return mezclar(color, hacia, 1)

NEGRO, BLANCO = "#000000", "#ffffff"

def legible_sobre_su_fondo(color: str, fondos: list, pagina: str, mezcla: float = .16, hacia: str = BLANCO) -> str:
    """Como legible, contando también su propio fondo tintado (la página con un «mezcla» del color), que cambia con él:
    los rótulos de los recuadros sobre su fondo."""
    for paso in range(41):
        c = mezclar(color, hacia, paso / 40)
        if all(contraste(c, f) >= 4.5 for f in fondos + [mezclar(pagina, c, mezcla)]):
            return c
    return hacia

LUMINANCIA_CABECERA = .3  # tope de la cabecera clara: un primario más luminoso, como un amarillo, deslumbra a lo ancho
MEZCLA_CABECERA_OSCURA = .35  # la cabecera oscura: la página oscura con un 35 % del primario

def _con_texto(fondo: str, tintas: tuple, hacia: str) -> tuple:
    """(fondo, texto): el texto, la tinta de más contraste; si ninguna llega a 4,5:1, el fondo se mueve hacia «hacia»."""
    for _ in range(40):
        texto = max(tintas, key=lambda t: contraste(t, fondo))
        if contraste(texto, fondo) >= 4.5:
            return fondo, texto
        fondo = mezclar(fondo, hacia, .05)
    return fondo, max(tintas, key=lambda t: contraste(t, fondo))

def cabecera_clara(primario: str, texto: str) -> dict:
    """La cabecera destacada en claro (decisión 351): el primario con un 10 % de la tinta del texto, que le quita brillo
    y croma, y oscurecido con ella hasta una luminancia de 0,3 como mucho; su texto, blanco o la tinta, a 4,5:1."""
    c = mezclar(primario, texto, .1)
    while luminancia(c) > LUMINANCIA_CABECERA:
        c = mezclar(c, texto, .05)
    c, t = _con_texto(c, (BLANCO, texto), texto)
    return {"cabecera": c, "sobre-cabecera": t}

def cabecera_oscura(po: str, pagina: str, texto: str) -> dict:
    """La cabecera destacada en oscuro (351): un tono profundo del primario, la página oscura con un 35 % de él, que no
    deslumbra; su texto, el claro de la página o la tinta oscura, a 4,5:1."""
    c, t = _con_texto(mezclar(pagina, po, MEZCLA_CABECERA_OSCURA), (texto, pagina), pagina)
    return {"cabecera": c, "sobre-cabecera": t}

def primario_linea(primario: str, fondos: list, hacia: str) -> str:
    """Las líneas y bordes en el color del proyecto (decisión 335, 8): el primario, oscurecido (o aclarado, en oscuro)
    lo justo para 3:1 sobre los fondos. Con un primario claro, como un amarillo, las flechas de los diagramas se ven."""
    return legible(primario, fondos, hacia, 3)

def familia_primario_oscuro(po: str, pagina: str, fondo_medio: str | None = None) -> dict:
    """Los tonos del primario en oscuro (decisión 338), con el primario ya legible sobre la página oscura. Como texto
    (enlaces), también sobre «fondo_medio», el de las decisiones de las preguntas."""
    # Solo si ya se lee sobre la página: uno que no, lo avisa el contraste.
    texto = legible(po, [pagina, fondo_medio], BLANCO) if fondo_medio and contraste(po, pagina) >= 4.5 else po
    return {"primario": po, "primario-vivo": mezclar(po, BLANCO, .25), "primario-texto": texto,
            "primario-linea": primario_linea(po, [pagina, mezclar(pagina, po, .16)], BLANCO),
            "sobre-primario": sobre(po, tinta=pagina), "fondo": mezclar(pagina, po, .16),
            "tenue": mezclar(pagina, po, .42)}

def derivar_oscuro(claro: dict, dado: dict | None = None) -> dict:
    """La paleta oscura completa (decisión 348): la que se da, rol por rol, y lo que falta derivado de la clara con
    reglas fijas. Página y fondos, de la tinta del texto mezclada con negro; textos claros; primario, acento y segundo
    aclarados lo justo para 4,5:1 sobre la página oscura y las superficies, como en la 338. «oscuro» sigue siendo una
    superficie oscura y «tinta-oscura» pasa a clara (349).

    Una paleta oscura anterior a la 349, con «oscuro» claro (la tinta fuerte), se lee como «tinta-oscura»."""
    o = dict(dado or {})
    if "oscuro" in o and "tinta-oscura" not in o and luminancia(o["oscuro"]) > .3:
        o["tinta-oscura"] = o.pop("oscuro")
    pagina = o.get("pagina")
    if not pagina:
        pagina = mezclar(claro["texto"], NEGRO, .3)
        while luminancia(pagina) > .018:
            pagina = mezclar(pagina, NEGRO, .15)
    d = {"pagina": pagina}
    d["fondo-suave"] = o.get("fondo-suave") or mezclar(pagina, BLANCO, .035)
    d["superficie"] = o.get("superficie") or d["fondo-suave"]
    d["fondo-medio"] = o.get("fondo-medio") or mezclar(pagina, BLANCO, .09)
    d["linea"] = o.get("linea") or mezclar(pagina, BLANCO, .14)
    superficies = [pagina, d["superficie"]]
    d["borde"] = o.get("borde") or legible(mezclar(pagina, BLANCO, .25), superficies, BLANCO, 3)
    d["borde-campo"] = o.get("borde-campo") or legible(d["borde"], superficies, BLANCO, 3)
    fondos_texto = superficies + [d["fondo-medio"]]
    d["texto"] = o.get("texto") or legible(mezclar(claro["pagina"], NEGRO, .04), fondos_texto, BLANCO, 7)
    d["texto-suave"] = o.get("texto-suave") or legible(mezclar(d["texto"], pagina, .3), fondos_texto, BLANCO)
    d["texto-tenue"] = o.get("texto-tenue") or legible(mezclar(d["texto"], pagina, .45), superficies, BLANCO, 3)
    d["tinta-oscura"] = o.get("tinta-oscura") or d["texto"]
    # «oscuro» es una superficie oscura con texto blanco (portada, decisiones, cabeceras de tabla): sigue oscura.
    # Se aclara lo justo para distinguirse de la página oscura (1,4:1), sin bajar de 4,5:1 con el blanco.
    po = o.get("primario") or legible_sobre_su_fondo(claro["primario"], superficies, pagina)
    # Se aclara lo justo para distinguirse de la página oscura (1,4:1), sin bajar de 4,5:1 con el blanco; y se oscurece
    # si hace falta para que el primario se lea encima (rótulos de las decisiones y de la portada oscura).
    oscuro = legible(claro["oscuro"], [BLANCO, po], NEGRO)
    for paso in range(1, 21):
        if contraste(oscuro, pagina) >= 1.4:
            break
        siguiente = mezclar(oscuro, BLANCO, .03)
        if contraste(BLANCO, siguiente) < 4.5 or contraste(po, siguiente) < 4.5:
            break
        oscuro = siguiente
    d["oscuro"] = o.get("oscuro") or oscuro
    for rol, valor in {**familia_primario_oscuro(po, pagina, d["fondo-medio"]), **cabecera_oscura(po, pagina, d["texto"])}.items():
        d[rol] = o.get(rol) or valor
    if claro["acento"] in (claro["primario"], claro.get("primario-texto")):
        acento = o.get("acento") or d["primario-texto"]
    else:
        acento = o.get("acento") or legible_sobre_su_fondo(claro["acento"], superficies, pagina)
    d["acento"] = acento
    d["acento-fondo"] = o.get("acento-fondo") or mezclar(pagina, acento, .16)
    d["acento-borde"] = o.get("acento-borde") or mezclar(pagina, acento, .55)
    d["segundo"] = o.get("segundo") or legible(claro["segundo"], superficies, BLANCO)
    return d

def oscuro_de(color: str, oscuro: dict) -> str:
    """Un color con significado (tarjetas, resaltado de código), aclarado hasta 4,5:1 sobre la página y las superficies
    oscuras (decisión 350)."""
    return legible(color, [oscuro["pagina"], oscuro["superficie"], oscuro["fondo-suave"]], BLANCO)

def normalizar_tema(tema: dict, nombre: str) -> dict:
    """Completa un tema (o los colores de un estilo.json): roles mínimos, tonos derivados, versión oscura, serie,
    opciones de aspecto y tipografías. Se detiene con un rol, un color o una opción desconocidos."""
    colores = {k: v.lower() for k, v in tema.get("colores", {}).items()}
    if "primario" not in colores:
        sys.exit(f"El tema {nombre} debe definir al menos el color «primario».")
    desconocidos = set(colores) - ROLES_VALIDOS
    if desconocidos:
        sys.exit(f"El tema {nombre} usa roles de color desconocidos: {', '.join(sorted(desconocidos))}. "
                 f"Posibles: {', '.join(sorted(ROLES_VALIDOS))}")
    for rol, valor in colores.items():
        if not re.fullmatch(r"#[0-9a-f]{6}|#[0-9a-f]{3}", valor):
            sys.exit(f"El tema {nombre} tiene un color no válido: {rol} {valor} (formato #rrggbb)")
    for rol, valor in COLORES_MINIMOS.items():
        colores.setdefault(rol, valor)
    for rol, base, con, prop in DERIVADOS:
        colores.setdefault(rol, mezclar(colores[base], con, prop))
    # Roles de un primario claro (decisión 319): el texto sobre el primario y el primario usado como texto.
    # Si faltan, se derivan: blanco o la tinta del texto, el de más contraste, y el propio primario.
    colores.setdefault("sobre-primario", sobre(colores["primario"], tinta=colores["texto"]))
    # Como texto (enlaces) se lee sobre la página, las tarjetas, los recuadros y la decisión de las preguntas. Un
    # primario que ya se lee sobre los tres primeros se oscurece lo justo para el cuarto; uno claro de verdad se deja
    # como está, para que el contraste avise y lo fije el propietario (319).
    colores.setdefault("superficie", BLANCO)
    base = [colores["pagina"], colores["superficie"], colores["fondo"]]
    if all(contraste(colores["primario"], f) >= 4.5 for f in base):
        colores.setdefault("primario-texto", legible(colores["primario"], base + [colores["fondo-medio"]], NEGRO))
    colores.setdefault("primario-texto", colores["primario"])
    colores.setdefault("tinta-oscura", colores["oscuro"])
    colores.setdefault("superficie", BLANCO)
    for rol, valor in cabecera_clara(colores["primario"], colores["texto"]).items():
        colores.setdefault(rol, valor)
    # El borde de los campos (notas, buscador), a 3:1 para verse; el de las cajas sigue suave (decisión 335, 9).
    colores.setdefault("borde-campo", legible(colores["borde"], [colores["pagina"], colores["superficie"]],
                                              colores["texto"], 3))
    colores.setdefault("primario-linea", primario_linea(
        colores["primario"], [colores["pagina"], colores["superficie"], colores["fondo"]], NEGRO))
    tema["colores"] = colores
    # La versión oscura del tema, rol por rol: la que da el tema y lo que falta derivado de la clara (decisión 348).
    # La usan el modo oscuro de «Lectura» de los documentos (347) y las páginas con data-theme="dark" (diagramas,
    # artifacts).
    oscuro = {k: v.lower() for k, v in tema.get("colores-oscuro", {}).items()}
    raros = set(oscuro) - ROLES_VALIDOS
    if raros:
        sys.exit(f"El tema {nombre} usa roles de color desconocidos en «colores-oscuro»: {', '.join(sorted(raros))}")
    for rol, valor in oscuro.items():
        if not re.fullmatch(r"#[0-9a-f]{6}", valor):
            sys.exit(f"El tema {nombre} tiene un color no válido en «colores-oscuro»: {rol} {valor} (formato #rrggbb)")
    tema["colores-oscuro"] = derivar_oscuro(colores, oscuro)
    serie = [c.lower() for c in tema.get("serie", [])]
    for c in serie:
        if not re.fullmatch(r"#[0-9a-f]{6}", c):
            sys.exit(f"El tema {nombre} tiene un color de «serie» no válido: {c} (formato #rrggbb)")
    tema["serie"] = serie
    estilo = tema.get("estilo", {})
    for clave, valor in estilo.items():
        if clave == "esquinas":
            if not isinstance(valor, (int, float)) or valor < 0:
                sys.exit(f"El tema {nombre}: «esquinas» debe ser un número de píxeles")
        elif clave == "opacidad":
            # De 0,75 a 1, título blanco (grande y en negrita por debajo de 1: 3:1 o más).
            # De 0,2 a 0,5, título en el color oscuro del bloque (4,5:1 o más). En medio no se lee bien ninguno.
            if not isinstance(valor, (int, float)) or not (0.75 <= valor <= 1 or 0.2 <= valor <= 0.5):
                sys.exit(f"El tema {nombre}: «opacidad» (etiqueta sólida) debe estar entre 0.75 y 1 (título blanco) "
                         "o entre 0.2 y 0.5 (título oscuro)")
        elif clave not in ESTILO_OPCIONES or valor not in ESTILO_OPCIONES[clave]:
            opciones = "; ".join(f"{k}: {', '.join(v)}" for k, v in ESTILO_OPCIONES.items())
            sys.exit(f"El tema {nombre}: estilo «{clave}: {valor}» no válido. Opciones: {opciones}; esquinas: número")
    tema["estilo"] = estilo
    tema["tipografias"] = {**TIPOGRAFIAS, **tema.get("tipografias", {})}
    return tema

# Opciones de aspecto de un tema («estilo»), de la maqueta antigua de la visión: se validan, pero el generador único no
# las aplica; el aspecto lo fija el estilo del proyecto (docs/identidad/estilo.json, decisión 318).
ESTILO_OPCIONES = {
    "cabecera": ("blanca", "primario", "oscuro"),
    "etiqueta": ("tinte", "solida", "linea"),
    "marcador": ("circulo", "cuadrado", "ninguno"),
}

TODOS_LOS_ROLES = [r for r, _, _ in ROLES] + list(ROLES_PROPIOS)
# Colores fijos del resaltado de código (estilo_documento.css, --sx-…): en oscuro, aclarados (decisión 350).
ERROR = "#b3261e"  # el rojo de borrar y de «sin resultados» (herramientas.css, var(--error))
SX_FIJOS = {"cadena": "#1f812d", "numero": "#a6501a", "funcion": "#1f7a7a", "atributo": "#a6501a"}

def _decl(colores: dict, roles=None) -> str:
    out = " ".join(f"--{r}: {colores[r]};" for r in (roles or TODOS_LOS_ROLES) if r in colores)
    if "primario" in colores:
        out += " --primario-rgb: " + ", ".join(str(x) for x in _rgb(colores["primario"])) + ";"
    return out

def tonos_serie(c: str, texto: str) -> dict:
    return {"primario": c, "oscuro": mezclar(c, NEGRO, .38), "tinta-oscura": mezclar(c, NEGRO, .38),
            "fondo": mezclar(c, BLANCO, .95), "borde": mezclar(c, BLANCO, .81), "linea": mezclar(c, BLANCO, .88),
            "tenue": mezclar(c, BLANCO, .55), "fondo-suave": mezclar(c, BLANCO, .97),
            "fondo-medio": mezclar(c, BLANCO, .84), "primario-vivo": mezclar(c, BLANCO, .25),
            "primario-texto": c, "sobre-primario": sobre(c, texto),
            "primario-linea": primario_linea(c, [BLANCO, mezclar(c, BLANCO, .95)], NEGRO)}

def tonos_serie_oscuro(c: str, oscuro: dict) -> dict:
    """Los tonos oscuros de un color de la serie. Redefine todos los roles que da tonos_serie: los neutros (tinta,
    superficies de tabla, líneas) vuelven a los del oscuro, para que no se queden con los claros del bloque. El color se
    lee a 4,5:1 también sobre su fondo tintado (la recomendación de una pregunta) y sobre la superficie oscura (los
    rótulos de los recuadros de decisión), como el primario en derivar_oscuro."""
    po = legible_sobre_su_fondo(c, [oscuro["pagina"], oscuro["superficie"], oscuro["oscuro"]], oscuro["pagina"])
    neutros = {k: oscuro[k] for k in ("oscuro", "tinta-oscura", "fondo-suave", "fondo-medio", "linea")}
    return {**neutros, **familia_primario_oscuro(po, oscuro["pagina"]), "borde": mezclar(oscuro["pagina"], po, .55)}

def variables_css(tema: dict) -> str:
    """Las variables de los roles: las claras en :root y las oscuras con data-theme="dark" en <html>, que pone el modo
    oscuro de «Lectura» (decisión 347) y usan los diagramas y los artifacts. El oscuro es solo de pantalla: al imprimir,
    los colores claros. El lector electrónico (.lector) imita un aparato y sigue en claro."""
    c, t = tema["colores"], tema["tipografias"]
    lineas = [_decl(c)] + [f"--fuente-{k}: {t[k]};" for k in ("texto", "titulos", "escena")]
    css = ":root { " + " ".join(lineas) + " }"
    oscuro = tema.get("colores-oscuro") or derivar_oscuro(c, {})
    sx = " ".join(f"--sx-{k}: {oscuro_de(v, oscuro)};" for k, v in SX_FIJOS.items())
    sx += f" --error: {oscuro_de(ERROR, oscuro)};"
    reglas = [f':root[data-theme="dark"] {{ {_decl(oscuro)} {sx} color-scheme: dark; }}',
              f':root[data-theme="dark"] .lector {{ {_decl(c)} color-scheme: light; }}']
    # Serie opcional: cada bloque (H2) toma un color de la lista, en ciclo, con sus tonos derivados.
    serie = tema.get("serie", [])
    for n in range(1, 41) if serie else ():
        s = serie[(n - 1) % len(serie)]
        css += f"\n    .bloque-{n} {{ {_decl(tonos_serie(s, c['texto']))} }}"
        reglas.append(f':root[data-theme="dark"] .bloque-{n} {{ {_decl(tonos_serie_oscuro(s, oscuro))} }}')
    return css + "\n    @media screen {\n    " + "\n    ".join(reglas) + "\n    }"

_ATRIBUTOS_COLOR = ("fill", "stroke", "stop-color", "flood-color", "lighting-color")
# El rol según el uso: un color de texto (color, o fill de un <text>) toma el rol legible del tema y un trazo, el de las
# líneas. Así un .md escrito con el primario oscuro de teal o morado se lee con un primario claro (un amarillo) y en
# oscuro, donde «oscuro» es una superficie y no una tinta (349); el tenue es para líneas, no para letra (3:1).
_ROL_TEXTO = {"primario": "primario-texto", "primario-vivo": "primario-texto", "oscuro": "tinta-oscura",
              "texto-tenue": "texto-suave"}
_ROL_TRAZO = {"primario": "primario-linea", "primario-vivo": "primario-linea"}
_ETIQUETAS_TEXTO = ("text", "tspan", "textpath")


def _rol_por_uso(css: str, es_texto: bool) -> str:
    """Cambia var(--rol) por el rol de su uso en cada declaración «propiedad: valor» de un style."""
    def declaracion(d: str) -> str:
        prop = d.split(":", 1)[0].strip().lower() if ":" in d else ""
        roles = (_ROL_TEXTO if prop == "color" or (prop == "fill" and es_texto)
                 else _ROL_TRAZO if prop == "stroke" else None)
        if not roles:
            return d
        return re.sub(r"var\(--([\w-]+)\)", lambda m: f"var(--{roles.get(m.group(1), m.group(1))})", d)
    return ";".join(declaracion(d) for d in css.split(";"))

def colores_a_variables(html: str) -> str:
    """Pasa los colores con rol del .md a variables CSS, para que cada gráfico siga los colores de su bloque.

    - En los atributos style="…", el color se sustituye por var(--rol).
    - Los atributos SVG fill, stroke… no admiten var(): se pasan a la declaración style del elemento,
      delante de lo que ya tuviera (lo que ya estaba en style sigue mandando).
    """
    a_rol = {}
    for rol, teal, morado in ROLES:
        a_rol[teal] = a_rol[morado] = rol
    a_rol["#ffffff"] = a_rol["#fff"] = a_rol["white"] = "superficie"  # el blanco de los esquemas pasa a oscuro con la página
    hex_re = re.compile(r"#[0-9a-fA-F]{6}(?![0-9a-fA-F])|#[0-9a-fA-F]{3}(?![0-9a-fA-F])")

    def en_css(texto: str) -> str:
        texto = hex_re.sub(lambda m: f"var(--{a_rol[m.group(0).lower()]})" if m.group(0).lower() in a_rol else m.group(0), texto)
        texto = re.sub(r"(?<![\w-])white(?![\w-])", "var(--superficie)", texto, flags=re.I)
        for pref in ("rgba(0, 114, 107, ", "rgba(123, 44, 191, ", "rgba(0,114,107,", "rgba(123,44,191,"):
            texto = texto.replace(pref, "rgba(var(--primario-rgb), ")
        return texto

    def etiqueta(m):
        tag = m.group(0)
        es_texto = re.match(r"<([\w:-]+)", tag).group(1).lower() in _ETIQUETAS_TEXTO
        movidos = []
        def atributo(am):
            valor = am.group(2)
            if valor.lower() in a_rol or valor.startswith(("rgba(0, 114, 107", "rgba(123, 44, 191", "rgba(0,114,107", "rgba(123,44,191")):
                movidos.append(f"{am.group(1)}: {en_css(valor)}")
                return ""
            return am.group(0)
        tag = re.sub(r'\s(' + "|".join(_ATRIBUTOS_COLOR) + r')="([^"]*)"', atributo, tag)
        tag = re.sub(r'\sstyle="([^"]*)"', lambda sm: f' style="{_rol_por_uso(en_css(sm.group(1)), es_texto)}"', tag)
        if movidos:
            previo = _rol_por_uso("; ".join(movidos), es_texto)
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
    "diagramas": ("Ajustes de los diagramas en la barra lateral (tema, forma, cabecera, dibujo, interacción y pie), para todas las figuras; solo si hay diagramas", True, True, False),
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


# Lector de libros (recurso común: assets/lector.css y lector.js). Solo entra si el documento lo usa.
LECTOR_CSS = "skills/crear_documentos/assets/lector.css"
LECTOR_JS = "skills/crear_documentos/assets/lector.js"
# Con data-al-abrir="historia", la cabecera oculta el documento desde el principio, sin parpadeo; sin JS, la clase no
# se pone y el documento se ve entero.
HISTORIA_PRIMERO = "\n  <script>document.documentElement.classList.add('historia-primero')</script>"


def lector_estilos(html: str) -> str:
    if 'class="libro' not in html and 'class="lector' not in html:
        return ""
    return "\n  " + bloque_kit(LECTOR_CSS) + (HISTORIA_PRIMERO if 'data-al-abrir="historia"' in html else "")


def lector_scripts(html: str) -> str:
    return "\n" + bloque_kit(LECTOR_JS) if 'class="lector"' in html else ""


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



# Diagramas de la skill diagramas (generar_diagrama.py --fragmento pegado en el .md): su CSS y su JS, los colores de
# cada tema para .diagrama[data-d-tema] y la herramienta «diagramas» del kit. Solo entran si el documento los tiene.
DIAGRAMAS_CSS = "skills/diagramas/assets/diagramas.css"
DIAGRAMAS_JS = "skills/diagramas/assets/diagramas.js"
DIAGRAMAS_KIT = "tools/kit_documentos/diagramas.js"


def tiene_diagramas(html: str) -> bool:
    return 'class="diagrama' in html


def temas_diagramas() -> list:
    """[(nombre, título, tema)] de los temas de assets/temas, para que las figuras puedan tomar cualquiera."""
    out = []
    for p in sorted(TEMAS.glob("*.json")):
        t = cargar_tema(p.stem)
        out.append((p.stem, t.get("nombre", p.stem).split("·")[0].strip() or p.stem, t))
    return out


def diagramas_estilos(html: str) -> str:
    if not tiene_diagramas(html):
        return ""
    reglas, oscuras = [], []
    for nombre, _, t in temas_diagramas():
        v = " ".join(f"--{k}: {c};" for k, c in t["colores"].items())
        oscuras.append(f':root[data-theme="dark"] .diagrama[data-d-tema="{nombre}"] {{ {_decl(t["colores-oscuro"])} }}')
        f = t.get("tipografias", {})
        fuentes = "".join(f" --fuente-{k}: {f[k]};" for k in ("texto", "titulos", "escena") if f.get(k))
        reglas.append(f'.diagrama[data-d-tema="{nombre}"] {{ {v}{fuentes} --diagrama-papel: var(--pagina); '
                      'background: var(--pagina); color: var(--texto); padding: 14px clamp(0px, (100% - 400px) / 2, 16px); '
                      'border-radius: var(--esquinas, 8px); }')
    usados = sorted(set(re.findall(r'data-d-tema="([\w-]+)"', html)))
    urls = [t.get("tipografias", {}).get("url") for n, _, t in temas_diagramas() if n in usados]
    enlaces = "".join(f'\n  <link href="{u}" rel="stylesheet">' for u in dict.fromkeys(u for u in urls if u))
    return (enlaces + "\n  " + bloque_kit(DIAGRAMAS_CSS) + '\n  <style data-diagramas-temas>\n'
            + "\n".join(reglas) + "\n@media screen {\n" + "\n".join(oscuras) + "\n}\n  </style>")


def diagramas_scripts(html: str, activas: str, con_kit: bool) -> str:
    if not tiene_diagramas(html):
        return ""
    lista = json.dumps([[n, titulo] for n, titulo, _ in temas_diagramas()], ensure_ascii=False)
    out = f'\n<script type="application/json" id="diagramas-temas">{lista}</script>\n' + bloque_kit(DIAGRAMAS_JS)
    if con_kit and "diagramas" in activas.split():
        out += "\n" + bloque_kit(DIAGRAMAS_KIT)
    return out
