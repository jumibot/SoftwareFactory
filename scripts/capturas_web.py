"""Genera los pantallazos simulados de la página web y del README (site/img/*.svg), en inglés y en castellano.

Imitan el panel de la SF en Claude Code con datos ficticios (el proyecto «Pantry», inventado). Cada SVG lleva su
propio fondo oscuro de terminal, así se lee igual en el tema claro y en el oscuro de GitHub. Los textos de cada
idioma están en TEXTOS; el dibujo es el mismo.

Uso: python -I -X utf8 scripts/capturas_web.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "site" / "img"

# Colores del panel (los del mod: hooks/constantes.ts, logo.ts) y del terminal.
FONDO = "#191512"
PANEL = "#22201d"
BLOQUE = "#383532"
TEXTO = "#ece8e2"
TENUE = "#a6a19c"
OSCURO = "#77726d"
AMARILLO = "#f4bf36"
AMARILLO_APAGADO = "#b8963a"
VERDE = "#6ed889"
ROJO = "#f87171"
MORADO = "#827dbd"
MORADO_CLARO = "#b3aee6"
# Paleta de taller (tarea 368): grafito cálido, ámbar para «lo de ahora» y verde para lo hecho. El morado de la SF
# queda en el logo y en las etiquetas propias del panel (RELEASE, la versión, la orden de la bienvenida).
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

    def etiqueta_boton(self, x, y, t, fondo, letra="#000", size=13, derecha=False):
        """Una etiqueta con fondo, como los botones de la cabecera. Devuelve su ancho."""
        w = len(t) * size * 0.6 + 12
        if derecha:
            x -= w
        self.rect(x, y - size - 1, w, size + 8, fondo, rx=3)
        self.text(x + w / 2, y + 1, t, fill=letra, size=size, weight="700", anchor="middle")
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
        cx += s.etiqueta_boton(cx, y, "RELEASE", MORADO) + 6
    else:
        for t, f in release:
            cx += s.etiqueta_boton(cx, y, t, f) + 6
    if release is None:
        s.etiqueta_boton(cx, y, "TURBO", "#334155", letra=CIAN)
    s.etiqueta_boton(x + w, y, "SF 1.8.1", MORADO, derecha=True)
    y2 = y + 28
    s.rect(x, y2 - 15, 72, 22, BLOQUE, rx=3)
    s.text(x + 36, y2 + 1, "2h 05m", fill=TENUE, size=13, anchor="middle")
    s.rect(x + 78, y2 - 15, 104, 22, BLOQUE, rx=3)
    s.spans(x + 86, y2 + 1, [("31", TEXTO, True), (" " + T["prompts"], TENUE)], size=13)
    rt = rama + (f" ↑{subir}" if subir else "")
    rw = len(rt) * 7.8 + 14
    s.rect(x + w - rw, y2 - 15, rw, 22, BLOQUE, rx=3)
    if subir:
        s.spans(x + w - rw + 7, y2 + 1, [(rama + " ", TENUE), (f"↑{subir}", VERDE, True)], size=13)
    else:
        s.text(x + w - rw + 7, y2 + 1, rama, fill=AMARILLO if rama != "develop" else TENUE, size=13)
    return y2 + 30


def tarea(s, x, y, w, num, letra, titulo, pasos, actual, botones=("⚙",), desplegada=None):
    """Una tarea en curso, en amarillo, con su cuenta de pasos y el paso actual."""
    s.spans(x, y, [(str(num), AMARILLO), (letra, AMARILLO_APAGADO), (" " + titulo, AMARILLO)])
    bx = x + w
    for b, c in reversed([(b, {"⚙": TENUE, "T": CIAN, "C": VERDE, "D": AMARILLO, "E": ROJO}.get(b, TENUE)) for b in botones]):
        s.text(bx, y, b, fill=c, weight="700", anchor="end")
        bx -= len(b) * CH + 10
    y += 21
    if desplegada:
        s.text(x + 16, y, pasos, fill=TENUE, deco="underline")
        y += 21
        for marca, texto in desplegada:
            color = OSCURO if marca == "✓" else TEXTO if marca == "▸" else TENUE
            s.spans(x + 16, y, [(marca + " ", VERDE if marca == "✓" else color), (texto, color)])
            y += 20
        return y + 6
    s.spans(x + 16, y, [(pasos, TENUE), (" " + actual, TENUE)])
    return y + 28


def bloque(s, x, y, w, nombre, cuenta, derecha="", color_cuenta=TENUE):
    s.rect(x, y, w, 30, BLOQUE, rx=0)
    s.spans(x + 10, y + 20, [("▸ ", TENUE), (nombre, TEXTO, True), ("  " + cuenta, color_cuenta)])
    if derecha:
        s.text(x + w - 10, y + 20, derecha, fill=TENUE, size=12, anchor="end")
    return y + 38


def foco(s, x, y, w, h):
    """El punto de color que guía la vista: un marco ámbar, el amarillo de las tareas, alrededor de lo importante."""
    s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="8" fill="{AMARILLO}" fill-opacity=".07" '
          f'stroke="{AMARILLO}" stroke-width="1.6"/>')


# ── Los pantallazos ──

def panel(T):
    s = Svg(560, 470, T["panel_alt"])
    ventana(s, T["ventana"])
    x, w = 22, 516
    y = cabecera(s, x, 66, w, T)
    foco(s, x - 8, y - 10, w + 16, 50)
    y = tarea(s, x, y + 8, w, 47, "A", T["t47"], "3/5", T["t47_paso"], ("⚙", "T", "C"))
    y = tarea(s, x, y, w, 48, "A", T["t48"], "1/4", T["t48_paso"], ("⚙",))
    y = tarea(s, x, y, w, 51, "H", T["t51"], "0/3", T["t51_paso"], ())
    y += 6
    s.text(x + w, y - 4, T["tareas"], fill=TENUE, size=12, anchor="end")
    y = bloque(s, x, y + 4, w, T["pendientes"], "6 (5A + 1H)")
    y = bloque(s, x, y, w, T["observacion"], "2")
    y = bloque(s, x, y, w, T["cerradas"], "4 (4C)", color_cuenta=VERDE)
    y = bloque(s, x, y, w, T["propuestas"], "3")
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
    y = tarea(s, x + 6, y + 26, 504, 47, "A", T["t47"], "3/5", "", ("⚙", "T", "C"),
              desplegada=[("✓", T["s1"]), ("✓", T["s2"]), ("▸", T["s3"]), ("·", T["s4"]), ("·", T["s5"])])
    y = tarea(s, x + 6, y + 6, 504, 48, "A", T["t48"], "1/4", T["t48_paso"], ("⚙",))
    s.partes.insert(i, f'<rect x="{x - 6}" y="{y0}" width="528" height="{y - y0 - 4}" rx="6" fill="{PANEL}"/>')
    s.alto = y + 14
    s.guardar(SALIDA / f"request-{T['id']}.svg")


def logo(s, cx, y, celda=6):
    w = (len(BARRA[0]) + len(LETRAS[0])) * celda
    x0 = cx - w / 2
    for filas, color, dx in ((BARRA, MORADO_CLARO, 0), (LETRAS, MORADO, len(BARRA[0]))):
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
    s.text(280, y + 30, "S O F T W A R E   F A C T O R Y", fill=MORADO_CLARO, weight="700", anchor="middle")
    s.text(280, y + 58, T["lema1"], fill=TENUE, size=13, anchor="middle")
    s.text(280, y + 76, T["lema2"], fill=TENUE, size=13, anchor="middle")
    pw = len(T["orden"]) * CH + 24
    s.rect(280 - pw / 2, y + 96, pw, 28, MORADO, rx=4)
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
    lineas = [(T["caja_l1"], TEXTO, True), ("▶ 47 " + T["t47"], AMARILLO, False), ("▶ 48 " + T["t48"], AMARILLO, False),
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
    y = tarea(s, x, y + 8, w, 47, "T", T["t47"], "5/6", "", ("C", "D"),
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
    y = cabecera(s, x, 66, w, T, release=[(T["publicar_v"], MORADO)], subir=0)
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
    s.etiqueta_boton(x, 76, "RELEASE", MORADO, size=11)
    s.etiqueta_boton(x0 + w - 12, 76, "SF 1.8.1", MORADO, size=11, derecha=True)
    s.text(x, 100, "develop", fill=TENUE, size=12, **sans)
    s.text(x0 + w - 12, 100, "↑2", fill=VERDE, size=12, weight="700", anchor="end", **sans)
    foco(s, x - 6, 112, w - 12, 44)
    s.spans(x, 130, [("47", AMARILLO, True), (" " + T["app_t47"], AMARILLO)], size=12)
    s.text(x + 12, 148, T["app_p47"], fill=TENUE, size=11, **sans)
    s.spans(x, 178, [("48", AMARILLO, True), (" " + T["app_t48"], AMARILLO)], size=12)
    s.text(x + 12, 196, T["app_p48"], fill=TENUE, size=11, **sans)
    y = 222
    for nombre, n, c in ((T["pendientes"], "6", TENUE), (T["observacion"], "2", TENUE), (T["cerradas"], "4", VERDE)):
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
         panel_alt="The SF panel in Claude Code: header with RELEASE, TURBO and the version, two tasks in progress with their steps and a subagent, and the task blocks",
         prompts="prompts", tareas="TASKS", pendientes="Queued", observacion="In review", cerradas="Closed",
         propuestas="Proposals",
         t47="Fix accents in the CSV export", t47_paso="Export as UTF-8 with BOM",
         t48="Dark mode in Settings", t48_paso="Pick the colour tokens",
         t51="Login fails after an hour", t51_paso="Reproduce the expired token",
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
         caja_l1="SF 1.8 · Pantry · 6/7 Build and verify · devslice 2", caja_cuentas="3 queued · 1 in review", caja_abre="opens the panel",
         caja_prompt="Try it now…",
         publicado1="v1.3.0 published", publicado2="develop → main, tag pushed. Projects can update."),
    dict(COMUNES, id="es",
         panel_alt="El panel de la SF en Claude Code: cabecera con RELEASE, TURBO y la versión, dos tareas en curso con sus pasos y un subagente, y los bloques de tareas",
         prompts="prompts", tareas="TAREAS", pendientes="Pendientes", observacion="En observación", cerradas="Cerradas",
         propuestas="Propuestas",
         t47="Arreglar los acentos del CSV", t47_paso="Exportar en UTF-8 con BOM",
         t48="Modo oscuro en Ajustes", t48_paso="Elegir los colores",
         t51="El login falla a la hora", t51_paso="Reproducir el token caducado",
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
         caja_l1="SF 1.8 · Pantry · 6/7 Desarrollo y verificación · devslice 2", caja_cuentas="3 en cola · 1 en observación", caja_abre="abre el panel",
         caja_prompt="Pruébala ahora…",
         publicado1="v1.3.0 publicada", publicado2="develop → main y el tag, subidos. Ya se puede actualizar."),
]


def logo_suelto():
    """El logo «/SF» solo, sin fondo, para la página y el favicon."""
    s = Svg(108, 60, "/SF")
    s.partes = []
    logo(s, 54, 0, celda=6)
    (SALIDA / "logo.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 60" width="108" height="60" role="img" '
        'aria-label="SoftwareFactory" shape-rendering="crispEdges">\n' + "\n".join(s.partes) + "\n</svg>\n",
        encoding="utf-8")


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    logo_suelto()
    for T in TEXTOS:
        for f in (panel, app, metodo, caja, peticion, incorporacion, probar, publicar):
            f(T)
    print(f"Pantallazos generados en {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
