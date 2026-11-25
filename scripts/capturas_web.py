"""Genera los pantallazos simulados de la página web y del README (site/img/*.svg), en inglés y en castellano.

Imitan el panel de la SF en Claude Code con datos ficticios (el proyecto «Pantry», inventado). Cada SVG lleva su
propio fondo oscuro de terminal, así se lee igual en el tema claro y en el oscuro de GitHub. Los textos de cada
idioma están en TEXTOS; el dibujo es el mismo.

Uso: python -I -X utf8 scripts/capturas_web.py
"""
import json
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "site" / "img"
# El estilo de la SF (docs/identidad/estilo.json): su amarillo y su paleta oscura, la del logo oscuro (decisión 335).
ESTILO = json.loads((RAIZ / "docs" / "identidad" / "estilo.json").read_text(encoding="utf-8"))["colores"]

# Colores del panel (los del mod: hooks/constantes.ts, logo.ts) y del terminal.
FONDO = "#191512"
PANEL = "#22201d"
BLOQUE = "#383532"
TEXTO = "#ece8e2"
TENUE = "#a6a19c"
OSCURO = "#77726d"
AMARILLO = ESTILO["primario"]
VERDE = "#6ed889"
ROJO = "#f87171"
AZUL = "#93c5fd"
VIOLETA = "#c084fc"
AMARILLO_CLARO = "#f8dc8c"
# Paleta de taller (tarea 368): grafito cálido, el amarillo de la SF (decisión 304) en su marca, la versión y el foco, y
# verde para lo hecho. Como en el panel, la tarea en curso va en azul claro (decisión 334) y RELEASE en violeta. El
# logo, como el oscuro del estilo: la barra en su texto claro y las letras en el amarillo.
LOGO_BARRA = ESTILO["colores-oscuro"]["texto"]
LOGO_LETRAS = ESTILO["colores-oscuro"]["primario"]
ROTULO = "#c8c3bc"
BORDE = "#4a4540"
CAJA = "#1f1c19"
CAJA_BORDE = "#3d3934"
CIAN = "#22d3ee"
NARANJA = "#fb923c"
MONO = "ui-monospace, 'Cascadia Mono', 'SF Mono', Menlo, Consolas, 'DejaVu Sans Mono', monospace"
CH = 8.4  # ancho de un carácter a 14 px (0,6 em)

# El logo «/SF» del panel (hooks/logo.ts): cinco filas, celdas de 1×2.
LETRAS = ['▄█████ ██████', '██     ██    ', '▀████▄ █████ ', '    ██ ██    ', '█████▀ ██    ']
BARRA = ['  ██ ', ' ▄█▀ ', ' ██  ', '▄█▀  ', '██   ']


class Svg:
    def __init__(self, ancho, alto, etiqueta):
        self.ancho, self.alto, self.etiqueta, self.partes = ancho, alto, etiqueta, []

    def add(self, s):
        self.partes.append(s)

    def rect(self, x, y, w, h, fill, rx=4, stroke=None, extra=""):
        st = f' stroke="{stroke}" stroke-width="1.2"' if stroke else ""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{st}{extra}/>')

    def text(self, x, y, t, fill=TEXTO, size=14, weight=None, anchor=None, mono=True, deco=None):
        a = f' text-anchor="{anchor}"' if anchor else ""
        w = f' font-weight="{weight}"' if weight else ""
        d = f' text-decoration="{deco}"' if deco else ""
        f = "" if mono else " font-family=\"system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif\""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}"{a}{w}{d}{f} xml:space="preserve">{escape(t)}</text>')

    def spans(self, x, y, trozos, size=14):
        """Una línea de varios colores: [(texto, color, negrita?)]."""
        s = "".join(f'<tspan fill="{c}"{" font-weight=\"700\"" if (len(t) > 2 and t[2]) else ""}>{escape(t[0])}</tspan>'
                    for t in trozos for c in [t[1]])
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" xml:space="preserve">{s}</text>')

    def etiqueta_boton(self, x, y, t, fondo, letra="#000", size=13, derecha=False, weight="700"):
        """Una etiqueta con fondo, como los botones de la cabecera. Devuelve su ancho."""
        w = len(t) * size * 0.6 + 12
        if derecha:
            x -= w
        self.rect(x, y - size - 1, w, size + 8, fondo, rx=3)
        self.text(x + w / 2, y + 1, t, fill=letra, size=size, weight=weight, anchor="middle")
        return w

    def guardar(self, ruta):
        cuerpo = "\n".join(self.partes)
        ruta.write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.ancho} {self.alto}" width="{self.ancho}" '
            f'height="{self.alto}" role="img" aria-label="{escape(self.etiqueta)}" font-family="{MONO}">\n'
            f'<title>{escape(self.etiqueta)}</title>\n'
            f'<rect width="{self.ancho}" height="{self.alto}" rx="14" fill="{FONDO}"/>\n{cuerpo}\n</svg>\n',
            encoding="utf-8")


def ventana(s, titulo):
    """La barra de la ventana del terminal."""
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        s.add(f'<circle cx="{22 + i * 18}" cy="20" r="5.5" fill="{c}"/>')
    s.text(s.ancho / 2, 25, titulo, fill=TENUE, size=12, anchor="middle")
    s.add(f'<line x1="0" y1="38" x2="{s.ancho}" y2="38" stroke="#312d2a"/>')


def cabecera(s, x, y, w, T, rama="develop", subir=2, release=None):
    """Las dos filas de la cabecera del panel."""
    cx = x
    if release is None:
        cx += s.etiqueta_boton(cx, y, "RELEASE", VIOLETA) + 6
    else:
        for t, f in release:
            cx += s.etiqueta_boton(cx, y, t, f) + 6
    if release is None:
        s.etiqueta_boton(cx, y, "TURBO", "#334155", letra=CIAN)
    s.etiqueta_boton(x + w, y, "SF 1.8.2", AMARILLO, derecha=True)
    y2 = y + 28
    s.rect(x, y2 - 15, 72, 22, BLOQUE, rx=3)
    s.text(x + 36, y2 + 1, "4h 12m", fill=TENUE, size=13, anchor="middle")
    s.rect(x + 78, y2 - 15, 104, 22, BLOQUE, rx=3)
    s.spans(x + 86, y2 + 1, [("86", TEXTO, True), (" " + T["prompts"], TENUE)], size=13)
    rt = rama + (f" ↑{subir}" if subir else "")
    rw = len(rt) * 7.8 + 14
    s.rect(x + w - rw, y2 - 15, rw, 22, BLOQUE, rx=3)
    if subir:
        s.spans(x + w - rw + 7, y2 + 1, [(rama + " ", TENUE), (f"↑{subir}", VERDE, True)], size=13)
    else:
        s.text(x + w - rw + 7, y2 + 1, rama, fill=AZUL if rama != "develop" else TENUE, size=13)
    return y2 + 30


def menu(s, x, y, ordenes):
    """Una fila del menú de etiquetas de una tarea desplegada (como en el panel desde la 1.8): cada orden, con su nombre
    sobre fondo negro y sin negrita; en verde las de la tarea, en rojo las que destruyen y atenuadas las de los pasos."""
    for nombre, color in ordenes:
        x += s.etiqueta_boton(x, y, nombre, "#000000", letra=color, size=12, weight=None) + 6
    return y + 23


def numero(s, x, y, num, color, subrayado, titulo, color_titulo):
    """«número título», sin letra tras el número; el número, subrayado si la tarea se despliega."""
    s.text(x, y, str(num), fill=color, deco="underline" if subrayado else None)
    s.text(x + (len(str(num)) + 1) * CH, y, titulo, fill=color_titulo)


def tarea(s, x, y, w, num, titulo, T, marca=None, ordenes=(), rama=None, pasos=None, desplegada=None):
    """Una tarea en curso, arriba, en azul: «número título» y, a la derecha, el ● de su subagente. Desplegada, como
    en el panel: el menú de etiquetas (una fila por lista de órdenes), la rama y «Pasos N/M», con los pasos debajo si
    van desplegados."""
    abierta = bool(ordenes or rama or pasos)
    numero(s, x, y, num, AZUL, abierta, titulo, AZUL)
    if marca:
        s.text(x + w, y, marca[0], fill=marca[1], weight="700", anchor="end")
    y += 23
    if not abierta:
        return y
    for fila in ordenes:
        y = menu(s, x + 16, y + 1, fila)
    if rama:
        s.text(x + 16, y, f'{T["rama"]}: {rama}', fill=TENUE, size=13)
        y += 21
    if pasos:
        s.spans(x + 16, y, [(T["pasos"], TENUE), (" " + pasos, TENUE)], size=13)
        s.add(f'<line x1="{x + 16:.1f}" y1="{y + 3:.1f}" x2="{x + 16 + len(T["pasos"]) * 7.8:.1f}" y2="{y + 3:.1f}" '
              f'stroke="{TENUE}" stroke-width="1"/>')
        y += 21
    for marca_paso, texto in desplegada or ():
        color = OSCURO if marca_paso == "✓" else TEXTO if marca_paso == "▸" else TENUE
        s.spans(x + 16, y, [(marca_paso + " ", VERDE if marca_paso == "✓" else color), (texto, color)])
        y += 20
    return y + 6


def ordenes_arriba(T, activar=True, cerrar=False):
    """Las órdenes de una tarea en curso, arriba: las de la tarea y, en otra fila, Paso +."""
    deTarea = ([(T["o_activar"], VERDE)] if activar else []) +         ([(T["o_cerrar"], VERDE), (T["o_observacion"], VERDE)] if cerrar else []) +         [(T["o_redescribir"], VERDE), ("?", VERDE)] + ([(T["o_descartar"], ROJO)] if cerrar else [])
    return [deTarea, [(T["o_paso"], TENUE)]]


def bloque(s, x, y, w, nombre, cuenta, derecha="", color_cuenta=TENUE):
    s.rect(x, y, w, 30, BLOQUE, rx=0)
    s.spans(x + 10, y + 20, [("▸ ", TENUE), (nombre, TEXTO, True), ("  " + cuenta, color_cuenta)])
    if derecha:
        s.text(x + w - 10, y + 20, derecha, fill=TENUE, size=12, anchor="end")
    return y + 38


def foco(s, x, y, w, h):
    """El punto de color que guía la vista: un marco en el amarillo de la SF alrededor de lo importante."""
    s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="8" fill="{AMARILLO}" fill-opacity=".07" '
          f'stroke="{AMARILLO}" stroke-width="1.6"/>')


# ── Los pantallazos ──

def plegada(s, x, y, w, num, titulo, marca, color):
    """Una tarea en curso plegada: su línea y, a la derecha, el ● de su subagente (verde trabaja, rojo espera) o ▶."""
    numero(s, x, y, num, AZUL, False, titulo, AZUL)
    s.text(x + w, y, marca, fill=color, weight="700", anchor="end")
    return y + 23


def panel(T):
    s = Svg(560, 640, T["panel_alt"])
    ventana(s, T["ventana"])
    x, w = 22, 516
    y = cabecera(s, x, 66, w, T, subir=3)
    i, y0 = len(s.partes), y + 8
    y = tarea(s, x, y0, w, 47, T["t47"], T, marca=("●", VERDE), ordenes=ordenes_arriba(T), rama="feature/47-csv",
              pasos="3/5")
    foco(s, x - 8, y0 - 18, w + 16, y - y0 + 12)
    s.partes.insert(i, s.partes.pop())  # el marco, detrás de la tarea
    y += 12
    for num, clave, marca, color in ((48, "t48", "●", VERDE), (51, "t51", "▶", VERDE), (55, "t55", "●", VERDE),
                                     (58, "t58", "●", ROJO), (60, "t60", "●", VERDE), (63, "t63", "●", VERDE)):
        y = plegada(s, x, y, w, num, T[clave], marca, color)
    y += 6
    s.text(x + w, y - 4, T["tareas"], fill=TENUE, size=12, anchor="end")
    s.rect(x, y + 4, w, 30, BLOQUE, rx=0)
    s.spans(x + 10, y + 24, [("▾ ", TENUE), (T["pendientes"], TEXTO, True), ("  38", TENUE)])
    y += 34
    s.rect(x, y, w, 133, PANEL, rx=0)
    y += 22
    for i, (num, clave) in enumerate(((52, "t52"), (53, "t53"), (64, "t64"), (66, "t66"))):
        s.spans(x + 24, y, [(str(num), TEXTO if i == 0 else TENUE), (f" {T[clave]}", TEXTO if i == 0 else TENUE)], size=13)
        if i == 0:
            s.add(f'<line x1="{x + 24:.1f}" y1="{y + 3:.1f}" x2="{x + 24 + 2 * 7.8:.1f}" y2="{y + 3:.1f}" stroke="{TEXTO}"/>')
            y = menu(s, x + 40, y + 23, [(T["poner"], VERDE), ("?", VERDE), (T["o_eliminar"], ROJO)]) - 23
        y += 20
    s.text(x + 24, y, T["mas"], fill=OSCURO, size=12)
    y += 18
    y = bloque(s, x, y, w, T["observacion"], "3")
    y = bloque(s, x, y, w, T["cerradas"], "124", color_cuenta=VERDE)
    y = bloque(s, x, y, w, T["propuestas"], "12")
    s.alto = y + 14
    s.guardar(SALIDA / f"panel-{T['id']}.svg")


def chat_linea(s, x, y, quien, texto, color, ancho=60):
    """Una intervención en el chat, partida en líneas."""
    palabras, lineas, l = texto.split(), [], ""
    for p in palabras:
        if len(l) + len(p) + 1 > ancho:
            lineas.append(l)
            l = p
        else:
            l = (l + " " + p).strip()
    lineas.append(l)
    for i, li in enumerate(lineas):
        if i == 0:
            s.spans(x, y, [(quien + " ", color, True), (li, TEXTO)])
        else:
            s.text(x + (len(quien) + 1) * CH, y, li)
        y += 20
    return y


def peticion(T):
    s = Svg(560, 600, T["peticion_alt"])
    ventana(s, T["ventana"])
    x = 22
    s.text(x, 64, T["paso1"], fill=ROTULO, size=12, weight="700")
    s.rect(x, 74, 516, 66, "#262320", rx=8, stroke=CAJA_BORDE)
    chat_linea(s, x + 12, 98, ">", T["pide"], AMARILLO, ancho=56)
    s.text(x, 170, T["paso2"], fill=ROTULO, size=12, weight="700")
    y = chat_linea(s, x, 196, "●", T["claude1"], TEXTO, ancho=58)
    yf = y
    y = chat_linea(s, x + 18, y + 2, "", T["claude2"], TEXTO, ancho=56)
    y = chat_linea(s, x + 18, y, "", T["claude3"], TEXTO, ancho=56)
    foco(s, x + 8, yf - 14, 506, y - yf + 6)
    s.text(x, y + 24, T["paso3"], fill=ROTULO, size=12, weight="700")
    y += 40
    i, y0 = len(s.partes), y
    y = tarea(s, x + 6, y + 26, 504, 47, T["t47"], T, marca=("●", VERDE), ordenes=ordenes_arriba(T),
              rama="feature/47-csv", pasos="2/5",
              desplegada=[("✓", T["s1"]), ("✓", T["s2"]), ("▸", T["s3"]), ("·", T["s4"]), ("·", T["s5"])])
    y = tarea(s, x + 6, y + 2, 504, 48, T["t48"], T, marca=("●", VERDE))
    s.partes.insert(i, f'<rect x="{x - 6}" y="{y0}" width="528" height="{y - y0 - 4}" rx="6" fill="{PANEL}"/>')
    s.alto = y + 14
    s.guardar(SALIDA / f"request-{T['id']}.svg")


def logo(s, cx, y, celda=6):
    w = (len(BARRA[0]) + len(LETRAS[0])) * celda
    x0 = cx - w / 2
    for filas, color, dx in ((BARRA, LOGO_BARRA, 0), (LETRAS, LOGO_LETRAS, len(BARRA[0]))):
        for fy, fila in enumerate(filas):
            for fx, c in enumerate(fila):
                dy, alto = {"█": (0, 2), "▄": (1, 1), "▀": (0, 1)}.get(c, (0, 0))
                if alto:
                    s.add(f'<rect x="{x0 + (fx + dx) * celda:.1f}" y="{y + (fy * 2 + dy) * celda:.1f}" '
                          f'width="{celda + 0.3:.1f}" height="{alto * celda + 0.3:.1f}" fill="{color}"/>')
    return y + 10 * celda


def incorporacion(T):
    s = Svg(560, 720, T["incorporacion_alt"])
    ventana(s, T["ventana"])
    s.rect(16, 52, 528, 262, PANEL, rx=6)
    y = logo(s, 280, 74)
    s.text(280, y + 30, "S O F T W A R E   F A C T O R Y", fill=AMARILLO_CLARO, weight="700", anchor="middle")
    s.text(280, y + 58, T["lema1"], fill=TENUE, size=13, anchor="middle")
    s.text(280, y + 76, T["lema2"], fill=TENUE, size=13, anchor="middle")
    pw = len(T["orden"]) * CH + 24
    s.rect(280 - pw / 2, y + 96, pw, 28, AMARILLO, rx=4)
    s.text(280, y + 115, T["orden"], fill="#000", weight="700", anchor="middle")
    y = 346
    s.text(22, y, T["inc_paso"], fill=ROTULO, size=12, weight="700")
    fondo, y0 = len(s.partes), y + 12
    yy = y + 40
    s.spans(32, yy, [("☐ ", TENUE), (T["preg_cab"], TEXTO, True)])
    yy += 28
    s.text(32, yy, T["preg"], fill=TEXTO, weight="700")
    yy += 30
    for i, (op, det, elegida) in enumerate(T["opciones"]):
        if elegida:
            foco(s, 30, yy - 20, 500, 46)
        col = AMARILLO if elegida else TEXTO
        s.spans(40, yy, [(("❯ " if elegida else "  ") + f"{i + 1}. ", col, elegida), (op, col, elegida)])
        s.text(76, yy + 19, det, fill=TENUE, size=12)
        yy += 48
    s.text(32, yy + 6, T["sin_ok"], fill=TENUE, size=12)
    s.partes.insert(fondo, f'<rect x="16" y="{y0}" width="528" height="{yy + 26 - y0}" rx="8" fill="{CAJA}" stroke="{BORDE}" stroke-width="1.2"/>')
    s.alto = yy + 46
    s.guardar(SALIDA / f"onboarding-{T['id']}.svg")


def caja(T):
    """Sin pantalla completa: la caja sobre el prompt, con lo esencial."""
    s = Svg(560, 400, T["caja_alt"])
    ventana(s, T["ventana"])
    y = chat_linea(s, 22, 66, "●", T["caja_chat"], TEXTO, ancho=58)
    s.text(40, y + 4, T["caja_chat2"], fill=TENUE, size=13)
    # La caja, alineada a la derecha, con borde redondeado.
    lineas = [(T["caja_l1"], TEXTO, True), ("▶ 47 " + T["t47"], AZUL, False), ("▶ 48 " + T["t48"], AZUL, False),
              (T["caja_cuentas"], TENUE, False), ("/sf " + T["caja_abre"], TENUE, False)]
    ancho = max(len(l[0]) for l in lineas) * 7.8 + 28
    bx, by = 538 - ancho, y + 32
    s.rect(bx, by, ancho, len(lineas) * 21 + 18, FONDO, rx=10, stroke=BORDE)
    for k, (texto, color, negrita) in enumerate(lineas):
        s.text(bx + 14, by + 26 + k * 21, texto, fill=color, size=13, weight="700" if negrita else None)
    y = by + len(lineas) * 21 + 34
    s.rect(16, y, 528, 40, CAJA, rx=8, stroke=CAJA_BORDE)
    s.spans(30, y + 25, [("> ", AMARILLO, True), (T["caja_prompt"], TENUE)])
    s.alto = y + 58
    s.guardar(SALIDA / f"box-{T['id']}.svg")


def probar(T):
    s = Svg(560, 470, T["probar_alt"])
    ventana(s, T["ventana"])
    x, w = 22, 516
    y = cabecera(s, x, 66, w, T, rama="feature/47-csv", subir=0)
    y = tarea(s, x, y + 8, w, 47, T["t47"], T, ordenes=ordenes_arriba(T, activar=False, cerrar=True),
              rama="feature/47-csv", pasos="5/6",
              desplegada=[("✓", T["s1"]), ("✓", T["s2"]), ("✓", T["s3"]), ("✓", T["s4"]), ("✓", T["s5"]),
                          ("▸", T["s6"])])
    s.text(x + w, y - 2, T["tareas"], fill=TENUE, size=12, anchor="end")
    y = bloque(s, x, y + 6, w, T["observacion"], "1")
    # El aviso del cierre.
    y += 18
    s.rect(x, y, w, 76, "#1a2a1e", rx=8, stroke="#3b6b49")
    foco(s, x - 4, y - 4, w + 8, 84)
    s.spans(x + 14, y + 28, [("✓ ", VERDE, True), (T["cerrada1"], TEXTO, True)])
    s.text(x + 34, y + 52, T["cerrada2"], fill=TENUE, size=13)
    s.alto = y + 96
    s.guardar(SALIDA / f"test-{T['id']}.svg")


def publicar(T):
    s = Svg(560, 480, T["publicar_alt"])
    ventana(s, T["ventana"])
    x, w = 22, 516
    y = cabecera(s, x, 66, w, T, release=[(T["publicar_v"], VIOLETA)], subir=0)
    s.text(x, y + 10, T["rev_titulo"], fill=ROTULO, size=12, weight="700")
    y += 22
    s.rect(x, y, w, 196, CAJA, rx=8, stroke=CAJA_BORDE)
    yy = y + 30
    for marca, texto, color in T["rev"]:
        if marca == "✕":
            foco(s, x + 6, yy - 18, w - 12, 27)
        s.spans(x + 14, yy, [(marca + " ", color, True), (texto, TEXTO)])
        yy += 26
    s.spans(x + 14, yy + 6, [("⛔ ", ROJO), (T["bloqueado"], ROJO, True)])
    s.text(x + 36, yy + 28, T["bloqueado2"], fill=TENUE, size=13)
    y += 216
    s.rect(x, y, w, 76, "#1a2a1e", rx=8, stroke="#3b6b49")
    s.spans(x + 14, y + 28, [("✓ ", VERDE, True), (T["publicado1"], TEXTO, True)])
    s.text(x + 34, y + 52, T["publicado2"], fill=TENUE, size=13)
    s.alto = y + 96
    s.guardar(SALIDA / f"publish-{T['id']}.svg")


def app(T):
    """El mismo panel en la app de escritorio de Claude Code: el chat a la izquierda y el panel, a la derecha."""
    s = Svg(560, 420, T["app_alt"])
    ventana(s, T["app_ventana"])
    sans = dict(mono=False)
    # El chat.
    s.rect(16, 54, 300, 52, "#262320", rx=12)
    s.text(30, 76, T["app_tu1"], size=13, **sans)
    s.text(30, 95, T["app_tu2"], size=13, **sans)
    s.text(16, 132, T["app_claude1"], size=13, **sans)
    s.text(16, 151, T["app_claude2"], size=13, **sans)
    s.text(16, 170, T["app_claude3"], fill=TENUE, size=13, **sans)
    s.rect(16, 360, 300, 40, CAJA, rx=12, stroke=CAJA_BORDE)
    s.text(30, 385, T["caja_prompt"], fill=TENUE, size=13, **sans)
    # El panel.
    x0, w = 332, 212
    s.rect(x0, 50, w, 356, PANEL, rx=10)
    x = x0 + 12
    s.etiqueta_boton(x, 76, "RELEASE", VIOLETA, size=11)
    s.etiqueta_boton(x0 + w - 12, 76, "SF 1.8.2", AMARILLO, size=11, derecha=True)
    s.text(x, 100, "develop", fill=TENUE, size=12, **sans)
    s.text(x0 + w - 12, 100, "↑2", fill=VERDE, size=12, weight="700", anchor="end", **sans)
    foco(s, x - 6, 112, w - 12, 44)
    s.spans(x, 130, [("47", AZUL, True), (" " + T["app_t47"], AZUL)], size=12)
    s.text(x + 12, 148, T["app_p47"], fill=TENUE, size=11, **sans)
    s.spans(x, 178, [("48", AZUL, True), (" " + T["app_t48"], AZUL)], size=12)
    s.text(x + 12, 196, T["app_p48"], fill=TENUE, size=11, **sans)
    y = 222
    for nombre, n, c in ((T["pendientes"], "38", TENUE), (T["observacion"], "3", TENUE), (T["cerradas"], "124", VERDE)):
        s.rect(x0 + 8, y, w - 16, 28, BLOQUE, rx=6)
        s.text(x0 + 18, y + 19, nombre, weight="700", size=12, **sans)
        s.text(x0 + w - 18, y + 19, n, fill=c, size=12, anchor="end", **sans)
        y += 36
    s.guardar(SALIDA / f"app-{T['id']}.svg")


def metodo(T):
    """Con la metodología: las siete fases, la actual, y los documentos que van saliendo."""
    s = Svg(560, 470, T["metodo_alt"])
    ventana(s, T["ventana"])
    x, w = 22, 516
    s.text(x, 66, T["metodo_linea"], fill=TENUE, size=13)
    y = 98
    for k, fase in enumerate(T["fases"]):
        marca, color = ("✓", OSCURO) if k < 2 else ("▸", TEXTO) if k == 2 else ("·", TENUE)
        if k == 2:
            foco(s, x - 6, y - 18, w + 12, 28)
        s.spans(x + 6, y, [(f"{k + 1}  ", ROTULO if k <= 2 else TENUE, True), (marca + " ", VERDE if k < 2 else color),
                           (fase, AMARILLO if k == 2 else color, k == 2)])
        y += 26
    y += 10
    s.rect(x, y, w, 30, BLOQUE, rx=0)
    s.spans(x + 10, y + 20, [("▾ ", TENUE), (T["documentos"], TEXTO, True), ("  3/4", TENUE)])
    s.text(x + w - 10, y + 20, T["proyecto"], fill=TENUE, size=12, anchor="end")
    y += 52
    for nombre, estado in T["docs"]:
        s.spans(x + 12, y, [("✓ " if estado else "▸ ", VERDE if estado else AMARILLO), (nombre, TEXTO if estado else AMARILLO)])
        y += 24
    s.alto = y + 10
    s.guardar(SALIDA / f"method-{T['id']}.svg")


COMUNES = dict(ventana="pantry — claude")

TEXTOS = [
    dict(COMUNES, id="en",
         rama="Branch", pasos="Steps", o_activar="Switch branch", o_cerrar="Close", o_observacion="To review", o_redescribir="Redescribe", o_paso="Step +", o_eliminar="Delete", o_descartar="Discard",
         panel_alt="The SF panel in Claude Code: seven tasks in progress, each with its subagent, one ready to test, 38 queued with a Start button, 3 in review and 124 closed",
         prompts="prompts", tareas="TASKS", pendientes="Queued", observacion="In review", cerradas="Closed",
         propuestas="Proposals",
         t47="Fix accents in the CSV export",
         t48="Dark mode in Settings",
         t51="Search by tag",
         t52="Export invoices to PDF", t53="Welcome e-mail for new users", t55="Weekly sales report",
         t58="Import contacts from Google", t60="Cache the product images", t63="Date formats per country",
         t64="Two-factor sign-in", t66="Print delivery notes", poner="Start", mas="…and 34 more",
         peticion_alt="From a request to a task: you write in the chat, Claude queues it as a task with steps and a branch, and a subagent works through the steps",
         paso1="1 · YOU ASK, IN YOUR OWN WORDS", pide="The CSV export breaks names with accents. And Settings needs a dark mode.",
         paso2="2 · CLAUDE TURNS IT INTO TASKS",
         claude1="Two requests, two tasks:",
         claude2="47 Fix accents in the CSV export — branch feature/47-csv, subagent on it.",
         claude3="48 Dark mode in Settings — queued, a subagent will start it.",
         paso3="3 · A SUBAGENT WORKS, STEP BY STEP",
         s1="Reproduce with a real file", s2="Write the test with “Muñoz”", s3="Export as UTF-8 with BOM",
         s4="Check it opens in Excel", s5="Test the task", s6="Close the task",
         incorporacion_alt="Onboarding a project: the welcome screen with the /SF logo and a one-click start, then Claude asking a few questions as menus",
         lema1="Your software factory on Claude Code:", lema2="from idea to code, task by task.",
         orden="onboard this project to the SF", inc_paso="CLAUDE ASKS A FEW QUESTIONS, AS MENUS",
         preg_cab="Method", preg="How do you want to work on Pantry?",
         opciones=[("Full method", "Vision, spec, design, then slices of code", True),
                   ("Just the queue and the panel", "Tasks, branches and subagents, no documents", False),
                   ("Decide later", "You can switch any time with /sf_config", False)],
         sin_ok="Nothing in your project changes without your OK.",
         probar_alt="Testing and closing a task: every step done, test it on its branch, then one click closes it into develop",
         cerrada1="47 closed: squashed into develop", cerrada2="One clean commit. Branch deleted. develop ↑1",
         publicar_alt="Publishing with a privacy check: RELEASE asks for the version, reviews every new commit for secrets and personal data, and blocks until it is clean",
         publicar_v="Publish v1.3.0? yes", rev_titulo="PUBLIC REVIEW · 9 NEW COMMITS",
         rev=[("✓", "No keys, tokens or passwords", VERDE), ("✓", "No local settings or task queue", VERDE),
              ("✓", "No e-mail addresses", VERDE), ("✕", "A personal folder path in docs/notes.md:14", ROJO),
              ("·", "Remote is public on GitHub", TENUE)],
         bloqueado="Blocked: nothing was published.", bloqueado2="Fix it and press RELEASE again.",
         app_alt="The same panel in the Claude Code desktop app: the chat on the left and the panel on the right, with tasks 47 and 48 in progress",
         app_ventana="Claude — Pantry", app_tu1="Export invoices to PDF too,", app_tu2="and add a download button.",
         app_claude1="Queued as task 52, with four steps.", app_claude2="A subagent will start it when 47 is done.",
         app_claude3="Task 47 is waiting for you to test it.",
         app_t47="CSV accents", app_p47="5/5 · ready to test", app_t48="Dark mode", app_p48="1/4 · Apply the colours",
         metodo_alt="With the method: the seven phases with the current one highlighted, and the project documents as they are written",
         metodo_linea="SF 1.8 · Pantry · 3/7 Technical definition",
         fases=["Vision", "Spec and interface", "Technical definition", "Devslice planning", "Devslice preparation",
                "Build and verify", "Wrap-up"],
         documentos="Documents", proyecto="PROJECT",
         docs=[("Vision of Pantry", True), ("Functional spec", True), ("Interface design", True),
               ("Technical definition", False)],
         caja_alt="Outside full screen, a small box above the prompt shows the project, the tasks in progress and the counts",
         caja_chat="Task 47 is ready for you to test on its branch.", caja_chat2="Steps 1 to 5 done.",
         caja_l1="SF 1.8 · Pantry · 6/7 Build and verify · devslice 2", caja_cuentas="38 queued · 3 in review", caja_abre="opens the panel",
         caja_prompt="Try it now…",
         publicado1="v1.3.0 published", publicado2="develop → main, tag pushed. Projects can update."),
    dict(COMUNES, id="es",
         rama="Rama", pasos="Pasos", o_activar="Activar rama", o_cerrar="Cerrar", o_observacion="A observación", o_redescribir="Redescribir", o_paso="Paso +", o_eliminar="Eliminar", o_descartar="Descartar",
         panel_alt="El panel de la SF en Claude Code: siete tareas en curso, cada una con su subagente, una lista para probar, 38 pendientes con el botón Poner en curso, 3 en observación y 124 cerradas",
         prompts="prompts", tareas="TAREAS", pendientes="Pendientes", observacion="En observación", cerradas="Cerradas",
         propuestas="Propuestas",
         t47="Arreglar los acentos del CSV",
         t48="Modo oscuro en Ajustes",
         t51="Buscar por etiqueta",
         t52="Exportar las facturas a PDF", t53="Correo de bienvenida", t55="Informe semanal de ventas",
         t58="Importar contactos de Google", t60="Caché de las fotos de producto", t63="Fechas según el país",
         t64="Acceso en dos pasos", t66="Imprimir albaranes", poner="Poner en curso", mas="…y 34 más",
         peticion_alt="De una petición a una tarea: escribes en el chat, Claude la pone en la cola como tarea con pasos y rama, y un subagente hace los pasos",
         paso1="1 · LO PIDES CON TUS PALABRAS", pide="El CSV exportado rompe los nombres con acentos. Y Ajustes necesita modo oscuro.",
         paso2="2 · CLAUDE LO CONVIERTE EN TAREAS",
         claude1="Dos peticiones, dos tareas:",
         claude2="47 Arreglar los acentos del CSV — rama feature/47-csv, con su subagente.",
         claude3="48 Modo oscuro en Ajustes — en la cola; la empezará otro subagente.",
         paso3="3 · UN SUBAGENTE TRABAJA, PASO A PASO",
         s1="Reproducirlo con un archivo real", s2="Escribir la prueba con «Muñoz»", s3="Exportar en UTF-8 con BOM",
         s4="Comprobar que abre en Excel", s5="Probar la tarea", s6="Cerrar la tarea",
         incorporacion_alt="La incorporación de un proyecto: la bienvenida con el logo /SF y la orden para empezar, y Claude haciendo unas pocas preguntas con menús",
         lema1="Tu fábrica de software sobre Claude Code:", lema2="de la idea al código, tarea a tarea.",
         orden="incorpora este proyecto a la SF", inc_paso="CLAUDE HACE UNAS POCAS PREGUNTAS, CON MENÚS",
         preg_cab="Metodología", preg="¿Cómo quieres trabajar en Pantry?",
         opciones=[("Con la metodología", "Visión, especificación, diseño y código por partes", True),
                   ("Solo la cola y el panel", "Tareas, ramas y subagentes, sin documentos", False),
                   ("Decidirlo después", "Se cambia cuando quieras con /sf_config", False)],
         sin_ok="Nada de tu proyecto cambia sin tu OK.",
         probar_alt="Probar y cerrar una tarea: todos los pasos hechos, se prueba en su rama y un clic la cierra en develop",
         cerrada1="47 cerrada: squash en develop", cerrada2="Un commit limpio. Rama borrada. develop ↑1",
         publicar_alt="Publicar con revisión de datos privados: RELEASE pide la versión, revisa cada commit nuevo en busca de secretos y datos personales, y bloquea hasta que esté limpio",
         publicar_v="¿Publicar v1.3.0? sí", rev_titulo="REVISIÓN PÚBLICA · 9 COMMITS NUEVOS",
         rev=[("✓", "Sin claves, tokens ni contraseñas", VERDE), ("✓", "Sin ajustes locales ni la cola", VERDE),
              ("✓", "Sin correos electrónicos", VERDE), ("✕", "Una ruta de carpeta personal en docs/notas.md:14", ROJO),
              ("·", "El remoto es público en GitHub", TENUE)],
         bloqueado="Bloqueado: no se ha publicado nada.", bloqueado2="Arréglalo y pulsa RELEASE otra vez.",
         app_alt="El mismo panel en la app de escritorio de Claude Code: el chat a la izquierda y el panel a la derecha, con las tareas 47 y 48 en curso",
         app_ventana="Claude — Pantry", app_tu1="Exporta también las facturas a PDF", app_tu2="y añade un botón de descarga.",
         app_claude1="En la cola como tarea 52, con cuatro pasos.", app_claude2="La empezará un subagente al acabar la 47.",
         app_claude3="La 47 te espera para que la pruebes.",
         app_t47="Acentos del CSV", app_p47="5/5 · lista para probar", app_t48="Modo oscuro", app_p48="1/4 · Aplicar los colores",
         metodo_alt="Con la metodología: las siete fases, con la actual destacada, y los documentos del proyecto según se escriben",
         metodo_linea="SF 1.8 · Pantry · 3/7 Definición técnica",
         fases=["Visión", "Especificación e interfaz", "Definición técnica", "Planificación de devslices",
                "Preparación de la devslice", "Desarrollo y verificación", "Cierre"],
         documentos="Documentos", proyecto="PROYECTO",
         docs=[("Visión de Pantry", True), ("Especificación funcional", True), ("Diseño de la interfaz", True),
               ("Definición técnica", False)],
         caja_alt="Sin pantalla completa, una caja pequeña sobre el prompt enseña el proyecto, las tareas en curso y las cuentas",
         caja_chat="La 47 está lista para que la pruebes en su rama.", caja_chat2="Pasos 1 a 5 hechos.",
         caja_l1="SF 1.8 · Pantry · 6/7 Desarrollo y verificación · devslice 2", caja_cuentas="38 en cola · 3 en observación", caja_abre="abre el panel",
         caja_prompt="Pruébala ahora…",
         publicado1="v1.3.0 publicada", publicado2="develop → main y el tag, subidos. Ya se puede actualizar."),
]


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    for T in TEXTOS:
        for f in (panel, app, metodo, caja, peticion, incorporacion, probar, publicar):
            f(T)
    print(f"Pantallazos generados en {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
