"""Genera sintesis-sf.html: la síntesis de diagramas de la SF con la estética de diagram-design,
en seis tipos de diagrama con contenido real de la SF (tarea 308).

Cada figura lleva dos dibujos de los mismos datos, horizontal y vertical, y elige uno según su
propio ancho (consulta de contenedor). Al pulsar un nodo se abre su ficha, de una en una: como HUD
junto al nodo si la figura es ancha y como croqueta debajo si es estrecha; se resalta su recorrido
y Escape la cierra.

Uso: python -I -X utf8 docs/_pruebas/sintesis_sf.py
"""
import re
from html import escape
from pathlib import Path

# ───────────────────────── medidas de letra (unidades del SVG) ─────────────────────────
# Lo más pequeño mide 12: la vertical (420 de ancho) se ve a 375 a un 77 %, unos 9,2 px reales.
F_NOMBRE, F_SUB, F_ETQ, F_CARRIL = 15, 12, 12, 12
C_NOMBRE, C_MONO, C_SERIF = 8.3, 7.7, 7.0  # ancho medio por carácter


def a_mono(t):
    return len(t) * C_MONO


# ───────────────────────── piezas ─────────────────────────

class Lienzo:
    """Acumula un SVG en capas (carriles, flechas, etiquetas, nodos) y cuenta nodos y flechas."""

    def __init__(self, p, w, h, aria, y0=0):
        self.p, self.w, self.h, self.aria, self.y0 = p, w, h, aria, y0
        self.capas = {"fondo": [], "flechas": [], "etiquetas": [], "nodos": []}
        self.n_nodos = self.n_flechas = 0
        self.ultima = ""

    def svg(self, clase):
        defs = (f'<defs><marker id="{self.p}-m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
                f'<path d="M0,1 L10,5 L0,9 z" class="ah"/></marker>'
                f'<marker id="{self.p}-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
                f'<path d="M0,1 L10,5 L0,9 z" class="ah-a"/></marker></defs>')
        cuerpo = "".join("".join(self.capas[c]) for c in ("fondo", "flechas", "etiquetas", "nodos"))
        return (f'<svg class="{clase}" viewBox="0 {self.y0} {self.w} {self.h - self.y0}" role="img" aria-label="{escape(self.aria)}">{defs}'
                f'<rect class="papel" y="{self.y0}" width="{self.w}" height="{self.h - self.y0}"/>{cuerpo}</svg>')

    # carriles y notas
    def carril(self, x, y, w, nombre):
        self.capas["fondo"].append(f'<g class="carril-g"><text class="carril" x="{x}" y="{y}">{escape(nombre)}</text>'
                                   f'<line class="regla" x1="{x}" y1="{y + 6}" x2="{x + w}" y2="{y + 6}"/></g>')

    def zona(self, x, y, w, h, nombre, hx=None):
        self.capas["fondo"].append(f'<rect class="zona" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
                                   f'<text class="carril" x="{hx if hx else x + 14}" y="{y + 22}">{escape(nombre)}</text>')

    def nota(self, x, y, w, cabeza, texto):
        """La nota «desde cualquier estado»: una transición que vale para varios nodos va aquí, no en flechas."""
        self.capas["fondo"].append(f'<g class="nota"><rect x="{x}" y="{y}" width="{w}" height="46" rx="6"/>'
                                   f'<text class="nota-c" x="{x + 12}" y="{y + 18}">{escape(cabeza)}</text>'
                                   f'<text class="nota-t" x="{x + 12}" y="{y + 36}">{escape(texto)}</text></g>')

    def texto(self, x, y, t, clase="llamada", ancla="start"):
        self.capas["fondo"].append(f'<text class="{clase}" x="{x}" y="{y}" text-anchor="{ancla}">{escape(t)}</text>')

    # nodos
    def nodo(self, nid, x, y, w, h, nombre, sub=(), k="", tipo=None):
        self.n_nodos += 1
        sub = [sub] if isinstance(sub, str) else list(sub)
        base = y + h / 2 + 5 - 7.5 * len(sub)
        if k == "dec":
            cx, cy = x + w / 2, y + h / 2
            forma = f'<polygon class="caja" points="{x},{cy} {x + 18},{y} {x + w - 18},{y} {x + w},{cy} {x + w - 18},{y + h} {x + 18},{y + h}"/>'
        else:
            forma = f'<rect class="caja" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>'
        o = [f'<g class="n {k}{" contipo" if tipo else ""}" data-n="{nid}">{forma}']
        if tipo:
            o.append(f'<g class="tipo-g"><rect class="tipo-c" x="{x + 8}" y="{y + 7}" width="{len(tipo) * 8.4 + 10:.0f}" height="16" rx="2"/>'
                     f'<text class="tipo" x="{x + 13}" y="{y + 19.5}">{tipo}</text></g>')
        o.append(f'<g class="desplaza"><text class="nn" x="{x + w / 2}" y="{base:.1f}" text-anchor="middle">{escape(nombre)}</text>')
        for i, s in enumerate(sub):
            o.append(f'<text class="sb" x="{x + w / 2}" y="{base + 17 + 14 * i:.1f}" text-anchor="middle">{escape(s)}</text>')
        o.append('</g>')
        if k == "fin":
            o.append(f'<circle class="fin-a" cx="{x + w - 14}" cy="{y + 14}" r="6"/><circle class="fin" cx="{x + w - 14}" cy="{y + 14}" r="3"/>')
        o.append('</g>')
        self.capas["nodos"].append("".join(o))

    def inicio(self, x, y):
        self.capas["nodos"].append(f'<circle class="ini" cx="{x}" cy="{y}" r="5"/>')

    def salida(self, x, y, lineas, de, a, abajo=False):
        """Un final sin caja (fuera de la cola): anillo y una nota en cursiva."""
        o = [f'<g data-de="{de}" data-a="{a}" class="et"><circle class="fin-a" cx="{x}" cy="{y}" r="8"/><circle class="fin" cx="{x}" cy="{y}" r="4"/>']
        for i, t in enumerate(lineas):
            if abajo:
                o.append(f'<text class="cl" x="{x}" y="{y + 26 + 17 * i}" text-anchor="middle">{escape(t)}</text>')
            else:
                o.append(f'<text class="cl" x="{x + 16}" y="{y + 5 + 17 * i}">{escape(t)}</text>')
        o.append('</g>')
        self.capas["nodos"].append("".join(o))

    # flechas y etiquetas
    def flecha(self, de, a, d, k="", punta=True):
        self.n_flechas += 1
        m = f' marker-end="url(#{self.p}-{"a" if k == "acc" else "m"})"' if punta else ""
        k = {"cl": "claude"}.get(k, k)
        self.ultima = d
        self.capas["flechas"].append(f'<path class="fl {k}" d="{d}" data-de="{de}" data-a="{a}"{m}/>')

    def boton(self, x, y, t, de, a, k="", alt=None):
        """La etiqueta de un botón del panel (decisión 301): texto mono separado de su línea, como cualquier etiqueta,
        con el color del botón solo en el texto. (x, y) es un punto de su flecha: la etiqueta va encima si el tramo es
        horizontal y a la derecha si es vertical; alt = (x, y, ancla) la pone en otro sitio."""
        k = {"RELEASE": "rel", "ACTUALIZAR": "de"}.get(t, k or "ok")
        if alt is None:
            alt = (x + 10, y + 4, "start") if self.vertical_en(x, y) else (x, y - 10, "middle")
        self.verbo(alt[0], alt[1], t, de, a, alt[2], "bt-t " + k)

    def vertical_en(self, x, y):
        """Si el tramo de la última flecha que pasa por (x, y) es vertical."""
        pts, cur = [], (0, 0)
        for c, nums in re.findall(r"([MLHVQ])([^MLHVQ]*)", self.ultima):
            v = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", nums)]
            if c in "ML":
                cur = (v[0], v[1])
            elif c == "H":
                cur = (v[0], cur[1])
            elif c == "V":
                cur = (cur[0], v[0])
            elif c == "Q":
                cur = (v[2], v[3])
            pts.append((c, cur))
        mejor, d = False, 1e9
        for (_, a), (c, b) in zip(pts, pts[1:]):
            if c == "Q":
                continue
            if a[0] == b[0] and min(a[1], b[1]) - 1 <= y <= max(a[1], b[1]) + 1 and abs(x - a[0]) < d:
                mejor, d = True, abs(x - a[0])
            if a[1] == b[1] and min(a[0], b[0]) - 1 <= x <= max(a[0], b[0]) + 1 and abs(y - a[1]) < d:
                mejor, d = False, abs(y - a[1])
        return mejor

    def verbo(self, x, y, t, de, a, ancla="middle", extra=""):
        """Una etiqueta de flecha: mayúsculas, monoespaciada, sobre su máscara y separada de la línea."""
        w = a_mono(t) + 8
        rx = {"middle": x - w / 2, "start": x - 4, "end": x - w + 4}[ancla]
        self.capas["etiquetas"].append(f'<g class="et" data-de="{de}" data-a="{a}"><rect class="masc" x="{rx:.1f}" y="{y - 13}" width="{w:.1f}" height="17" rx="2"/>'
                                       f'<text class="lb {extra}" x="{x}" y="{y}" text-anchor="{ancla}">{escape(t)}</text></g>')

    def claude(self, x, y, lineas, de, a, ancla="middle"):
        """Lo que hace Claude, no un botón: cursiva, y su flecha, discontinua."""
        lineas = [lineas] if isinstance(lineas, str) else lineas
        w = max(len(t) for t in lineas) * C_SERIF + 8
        rx = {"middle": x - w / 2, "start": x - 4, "end": x - w + 4}[ancla]
        o = [f'<g class="et" data-de="{de}" data-a="{a}"><rect class="masc" x="{rx:.1f}" y="{y - 14}" width="{w:.1f}" height="{17 * len(lineas) + 2}" rx="2"/>']
        for i, t in enumerate(lineas):
            o.append(f'<text class="cl cl-claude" x="{x}" y="{y + 17 * i}" text-anchor="{ancla}">{escape(t)}</text>')
        o.append('</g>')
        self.capas["etiquetas"].append("".join(o))


def codo(*p, r=8):
    """Camino ortogonal con codos redondeados."""
    d = [f"M{p[0][0]},{p[0][1]}"]
    for i in range(1, len(p) - 1):
        (xa, ya), (xb, yb), (xc, yc) = p[i - 1], p[i], p[i + 1]
        s1x, s1y = (xb > xa) - (xb < xa), (yb > ya) - (yb < ya)
        s2x, s2y = (xc > xb) - (xc < xb), (yc > yb) - (yc < yb)
        d.append(f"L{xb - s1x * r},{yb - s1y * r} Q{xb},{yb} {xb + s2x * r},{yb + s2y * r}")
    d.append(f"L{p[-1][0]},{p[-1][1]}")
    return " ".join(d)


# ───────────────────────── 1. ciclo de vida de una tarea ─────────────────────────

def ciclo(p, vertical):
    if vertical:
        L = Lienzo(p, 420, 610, "Ciclo de vida de una tarea, en vertical: las fases bajan por el centro; a la izquierda, la vuelta que hace Claude; a la derecha, las salidas.")
        L.carril(8, 18, 92, "VUELTAS"), L.carril(110, 18, 140, "FASES"), L.carril(268, 18, 144, "SALIDAS")
        L.inicio(180, 32)
        L.flecha("ini", "pend", "M180 37 V50")
        L.flecha("pend", "curso", "M180 110 V170"), L.boton(180, 140, "ACTIVAR RAMA", "pend", "curso")
        L.flecha("curso", "pend", codo((110, 200), (56, 200), (56, 80), (110, 80)), "cl"), L.claude(62, 136, ["sin", "trabajo"], "curso", "pend", "start")
        L.flecha("curso", "obs", "M180 230 V290"), L.boton(180, 260, "A OBSERVACIÓN", "curso", "obs", alt=(172, 264, "end"))
        L.flecha("obs", "cerr", "M225 350 V410"), L.boton(225, 384, "CERRAR", "obs", "cerr")
        L.flecha("cerr", "obs", "M160 410 V350"), L.boton(160, 380, "A OBSERVACIÓN", "cerr", "obs", alt=(152, 384, "end"))
        L.flecha("curso", "cerr", codo((250, 215), (290, 215), (290, 440), (250, 440))), L.boton(290, 250, "CERRAR", "curso", "cerr")
        L.flecha("curso", "desc", codo((250, 185), (360, 185), (360, 290))), L.boton(360, 274, "DESCARTAR", "curso", "desc", "de", alt=(305, 176, "middle"))
        L.flecha("pend", "fuera", "M250 70 H342"), L.boton(296, 70, "ELIMINAR", "pend", "fuera", "de")
        L.salida(352, 70, ["fuera de", "la cola"], "pend", "fuera", abajo=True)
        L.nodo("pend", 110, 50, 140, 60, "Pendientes", "sin rama", tipo="FASE")
        L.nodo("curso", 110, 170, 140, 60, "En curso", "rama · subagente", "foco", tipo="FASE")
        L.nodo("obs", 110, 290, 140, 60, "En observación", "en develop", tipo="FASE")
        L.nodo("cerr", 110, 410, 140, 60, "Cerradas", "en develop", "fin", tipo="FASE")
        L.nodo("desc", 310, 290, 104, 60, "Descartada", "sin botones", "sal", tipo="SALIDA")
        L.nota(8, 500, 404, "DESDE EN OBSERVACIÓN O CERRADAS", "Revertir → Pendientes o fuera de la cola")
        L.nota(8, 554, 404, "DESDE OBSERVACIÓN, CERRADAS O DESCARTADA", "Claude la reabre → En curso")
    else:
        L = Lienzo(p, 960, 420, "Ciclo de vida de una tarea: las fases en un carril; arriba, la vuelta que hace Claude; abajo, las salidas; a la derecha, lo que vale desde varios estados.", y0=76)
        L.carril(24, 98, 912, "VUELTAS · LAS HACE CLAUDE"), L.carril(24, 160, 72, "FASES"), L.carril(112, 304, 324, "SALIDAS"), L.carril(456, 304, 480, "DESDE VARIOS ESTADOS")
        L.inicio(16, 200)
        L.flecha("ini", "pend", "M21 200 H44")
        L.flecha("pend", "curso", "M180 200 H300"), L.boton(240, 200, "ACTIVAR RAMA", "pend", "curso")
        L.flecha("curso", "pend", codo((368, 170), (368, 128), (112, 128), (112, 170)), "cl"), L.claude(240, 122, "sin trabajo", "curso", "pend")
        L.flecha("curso", "obs", "M436 200 H556"), L.boton(496, 200, "A OBSERVACIÓN", "curso", "obs")
        L.flecha("obs", "cerr", "M692 188 H812"), L.boton(752, 188, "CERRAR", "obs", "cerr")
        L.flecha("cerr", "obs", "M812 214 H692"), L.boton(752, 214, "A OBSERVACIÓN", "cerr", "obs", alt=(752, 231, "middle"))
        L.flecha("curso", "cerr", codo((404, 230), (404, 268), (846, 268), (846, 230))), L.boton(625, 268, "CERRAR", "curso", "cerr")
        L.flecha("curso", "desc", "M336 230 V330"), L.boton(336, 286, "DESCARTAR", "curso", "desc", "de")
        L.flecha("pend", "fuera", "M78 230 V330"), L.boton(78, 280, "ELIMINAR", "pend", "fuera", "de")
        L.salida(78, 342, ["fuera de la cola"], "pend", "fuera")
        L.nodo("pend", 44, 170, 136, 60, "Pendientes", "sin rama", tipo="FASE")
        L.nodo("curso", 300, 170, 136, 60, "En curso", "rama · subagente", "foco", tipo="FASE")
        L.nodo("obs", 556, 170, 136, 60, "En observación", "en develop", tipo="FASE")
        L.nodo("cerr", 812, 170, 136, 60, "Cerradas", "en develop", "fin", tipo="FASE")
        L.nodo("desc", 268, 330, 136, 56, "Descartada", "sin botones", "sal", tipo="SALIDA")
        L.nota(456, 318, 480, "DESDE EN OBSERVACIÓN O CERRADAS", "Revertir → Pendientes o fuera de la cola")
        L.nota(456, 368, 480, "DESDE OBSERVACIÓN, CERRADAS O DESCARTADA", "Claude la reabre → En curso")
    return L


CICLO_FICHAS = {
    "pend": ("Pendientes", "En la cola, sin rama.", "✕✕✕", [("ACTIVAR RAMA", "", "con rama, o al elegirla → En curso"), ("A PROPUESTA", "", "→ propuestas"), ("ELIMINAR", "de", "→ fuera de la cola")]),
    "curso": ("En curso", "Arriba en el panel, en amarillo.", "✓✓✕", [("A OBSERVACIÓN", "", "→ En observación"), ("CERRAR", "", "→ Cerradas"), ("DESCARTAR", "de", "→ Descartada"), ("ACTIVAR RAMA", "", "→ la prueba en su rama"), ("", "cl", "Claude, sin trabajo en su rama → Pendientes")]),
    "obs": ("En observación", "El squash ya está en develop.", "✕✕✓", [("CERRAR", "", "→ Cerradas"), ("REVERTIR", "de", "→ Pendientes o fuera de la cola"), ("", "cl", "Claude la reabre → En curso")]),
    "cerr": ("Cerradas", "En verde; el trabajo sigue en develop.", "✕✕✓", [("A OBSERVACIÓN", "", "→ En observación"), ("REVERTIR", "de", "→ Pendientes o fuera de la cola"), ("", "cl", "Claude la reabre → En curso")]),
    "desc": ("Descartada", "Entre las cerradas, con una D.", "✕✕✕", [("", "cl", "Claude la reabre → En curso")]),
}


# ───────────────────────── 2. arquitectura ─────────────────────────

def arquitectura(p, vertical):
    if vertical:
        L = Lienzo(p, 420, 600, "Arquitectura de la SF en vertical: el repositorio, el equipo y el proyecto, de arriba abajo.")
        L.zona(8, 16, 404, 196, "REPOSITORIO", 250), L.zona(8, 236, 404, 194, "EQUIPO · ~/.CLAUDE", 250), L.zona(8, 458, 404, 132, "PROYECTO · .SF/", 250)
        L.flecha("dev", "main", "M135 104 V140"), L.boton(135, 122, "RELEASE", "dev", "main")
        L.flecha("main", "plug", "M135 196 V264"), L.boton(135, 224, "ACTUALIZAR", "main", "plug")
        L.flecha("plug", "cola", "M135 320 V358"), L.verbo(143, 344, "COPIA", "plug", "cola", "start")
        L.flecha("cola", "pet", "M135 414 V490"), L.verbo(143, 450, "ESCRIBE", "cola", "pet", "start")
        L.flecha("plug", "panel", codo((230, 292), (330, 292), (330, 490))), L.verbo(338, 384, "PINTA", "plug", "panel", "start")
        L.flecha("panel", "pet", "M268 518 H230", "dash"), L.verbo(249, 540, "LEE", "panel", "pet")
        L.nodo("dev", 40, 48, 190, 56, "develop", "rama de trabajo", tipo="RAMA")
        L.nodo("main", 40, 140, 190, 56, "main · vX.Y.Z", "lo publicado", tipo="TAG")
        L.nodo("plug", 40, 264, 190, 56, "Plugin sf", "instalado", "foco", tipo="PLUGIN")
        L.nodo("cola", 40, 358, 190, 56, "cola.py", "~/.claude/sf/", tipo="CLI")
        L.nodo("pet", 40, 490, 190, 56, "peticiones.json", "la cola", tipo="ESTADO")
        L.nodo("panel", 268, 490, 132, 56, "Panel", "el mod, /sf", tipo="MOD")
    else:
        L = Lienzo(p, 960, 310, "Arquitectura de la SF: el repositorio publica, el equipo instala el plugin y cola.py, y el proyecto guarda la cola que el panel lee.")
        L.zona(12, 24, 276, 270, "REPOSITORIO · GITHUB"), L.zona(380, 24, 240, 270, "EQUIPO · ~/.CLAUDE"), L.zona(680, 24, 268, 270, "PROYECTO · .SF/")
        L.flecha("dev", "main", "M150 124 V190"), L.boton(150, 157, "RELEASE", "dev", "main")
        L.flecha("main", "plug", "M260 218 H400"), L.boton(330, 218, "ACTUALIZAR", "main", "plug")
        L.flecha("plug", "cola", "M500 190 V124"), L.verbo(508, 162, "COPIA", "plug", "cola", "start")
        L.flecha("cola", "pet", "M600 96 H700"), L.verbo(650, 88, "ESCRIBE", "cola", "pet")
        L.flecha("plug", "panel", "M600 218 H700"), L.verbo(650, 210, "PINTA", "plug", "panel")
        L.flecha("panel", "pet", "M814 190 V124", "dash"), L.verbo(822, 162, "LEE", "panel", "pet", "start")
        L.nodo("dev", 40, 68, 220, 56, "develop", "rama de trabajo", tipo="RAMA")
        L.nodo("main", 40, 190, 220, 56, "main · vX.Y.Z", "lo publicado", tipo="TAG")
        L.nodo("cola", 400, 68, 200, 56, "cola.py", "~/.claude/sf/", tipo="CLI")
        L.nodo("plug", 400, 190, 200, 56, "Plugin sf", "instalado", "foco", tipo="PLUGIN")
        L.nodo("pet", 700, 68, 228, 56, "peticiones.json", "la cola del proyecto", tipo="ESTADO")
        L.nodo("panel", 700, 190, 228, 56, "Panel de la SF", "lo pinta el mod, /sf", tipo="MOD")
    return L


ARQ_FICHAS = {
    "dev": ("develop", "La rama de trabajo del repositorio fuente.", None, [("", "", "Cada tarea entra por squash al cerrarla, con «(N)» al final del título.")]),
    "main": ("main · vX.Y.Z", "Lo que instalan los proyectos.", None, [("RELEASE", "", "sube la versión, pasa develop a main por fast-forward, pone el tag y hace push")]),
    "plug": ("Plugin sf", "Instalado desde el catálogo softwarefactory.", None, [("ACTUALIZAR", "", "instala la versión publicada y las dependencias que falten"), ("", "", "Lleva las skills, el mod de estado, las plantillas y las herramientas.")]),
    "cola": ("cola.py", "El lanzador, en ~/.claude/sf/cola.py.", None, [("", "", "El panel lo copia al cargar; pasa cada orden a la copia de cola.py de la sesión."), ("", "", "Es la única vía para escribir la cola.")]),
    "pet": ("peticiones.json", "La cola del proyecto, en .sf/.", None, [("", "", "Tareas, pasos y estados. Se bloquea al escribir y guarda una copia antes.")]),
    "panel": ("Panel de la SF", "Lo pinta el mod de estado (/sf).", None, [("", "", "Lee la cola y, con sus botones, lanza cola.py.")]),
}


# ───────────────────────── 3. secuencia ─────────────────────────

SEQ_ACTORES = [("prop", "Propietario"), ("prin", "Principal"), ("sub", "Subagente"), ("cola", "cola.py")]
SEQ_MSG = [("prop", "prin", "PIDE", ""), ("prin", "cola", "CREAR", "", "Pendientes"), ("prin", "cola", "EN-CURSO · RAMA", "", "En curso"),
           ("prin", "sub", "ENCARGA", ""), ("sub", "prin", "INFORME", "dash"), ("prin", "cola", "LISTO", ""),
           ("prin", "prop", "¿OK? · PRUEBA", ""), ("prop", "prin", "OK", "acc"), ("prin", "cola", "CERRAR", "", "Cerradas")]


def secuencia(p, vertical):
    w = 420 if vertical else 960
    xs = [52, 158, 264, 370] if vertical else [120, 360, 600, 840]
    pos = dict(zip([a for a, _ in SEQ_ACTORES], xs))
    y0, paso = 96, 50
    h = y0 + paso * len(SEQ_MSG) + 10
    L = Lienzo(p, w, h, "Secuencia de una tarea, de la petición al cierre: el propietario pide, el principal lleva la cola con cola.py y encarga el trabajo al subagente; el propietario da el OK y el principal cierra.")
    for aid, nombre in SEQ_ACTORES:
        x = pos[aid]
        L.capas["fondo"].append(f'<line class="vida" x1="{x}" y1="58" x2="{x}" y2="{h - 8}" data-de="{aid}" data-a="{aid}"/>')
        bw = 96 if vertical else 140
        L.nodo(aid, x - bw / 2, 16, bw, 40, nombre, (), "foco" if aid == "prin" else "")
    L.capas["fondo"].append(f'<rect class="act" x="{pos["prin"] - 5}" y="{y0 - 12}" width="10" height="{paso * (len(SEQ_MSG) - 1) + 24}" rx="2"/>'
                            f'<rect class="act" x="{pos["sub"] - 5}" y="{y0 + paso * 3 - 8}" width="10" height="{paso + 16}" rx="2"/>')
    for i, m in enumerate(SEQ_MSG):
        de, a, t, k = m[:4]
        y = y0 + paso * i
        x1, x2 = pos[de], pos[a]
        s = 1 if x2 > x1 else -1
        x1 += 5 * s
        x2 -= 5 * s if a in ("prin", "sub") else 0
        L.flecha(de, a, f"M{x1} {y} H{x2}", "dash" if k == "dash" else ("acc" if k == "acc" else ""))
        L.verbo((x1 + x2) / 2, y - 7, t, de, a)
        if k == "acc":
            L.capas["etiquetas"][-1] = L.capas["etiquetas"][-1].replace('class="lb"', 'class="lb acc-t"')
        if len(m) > 4:
            cw = a_mono(m[4]) * 0.92 + 14
            L.capas["nodos"].append(f'<g class="estado" data-de="{de}" data-a="{a}"><rect x="{pos[a] - cw / 2:.1f}" y="{y + 9}" width="{cw:.1f}" height="19" rx="9.5"/>'
                                    f'<text x="{pos[a]}" y="{y + 22.5}" text-anchor="middle">{escape(m[4])}</text></g>')
    return L


SEQ_FICHAS = {
    "prop": ("Propietario", "Pide, prueba y da el OK.", None, [("", "", "Nada se cierra sin su OK."), ("ACTIVAR RAMA", "", "prueba la tarea en su rama antes de decir OK")]),
    "prin": ("Principal", "Habla con el propietario y lleva la cola.", None, [("", "", "Anota toda petición en cuanto llega y no hace el trabajo de la tarea: lo encarga.")]),
    "sub": ("Subagente", "Hace todo el trabajo de su tarea.", None, [("", "", "En su worktree, con la rama auxiliar sub-NN; vuelve con su informe.")]),
    "cola": ("cola.py", "Cada orden, un cambio de estado.", None, [("", "", "crear → Pendientes; en-curso y rama → En curso; listo; cerrar → squash en develop.")]),
}


# ───────────────────────── 4. fases de la metodología ─────────────────────────

FASES = [("vis", "Visión", "documento de visión"), ("esp", "Especificación e interfaz", "spec y bocetos"),
         ("tec", "Definición técnica", "arquitectura y stack"), ("dvs", "Devslices", "plan en el kanban"),
         ("pre", "Preparación", "devslice preparada"), ("des", "Desarrollo y verificación", "código y pruebas"),
         ("cie", "Cierre", "evidencias e informe")]


def fases(p, vertical):
    if vertical:
        paso = 70
        L = Lienzo(p, 420, 40 + paso * 6 + 50, "Las siete fases de la metodología, de arriba abajo, con lo que deja cada una.")
        for i, (fid, n, s) in enumerate(FASES):
            y = 36 + i * paso
            if i:
                L.flecha(FASES[i - 1][0], fid, f"M36 {y - paso + 9} V{y - 9}", punta=False)
            foco = fid == "des"
            L.capas["nodos"].append(f'<g class="n hito{" foco" if foco else ""}" data-n="{fid}"><rect class="toque" x="16" y="{y - 22}" width="388" height="50" rx="6"/>'
                                    f'<circle class="punto" cx="36" cy="{y}" r="{7 if foco else 5}"/>'
                                    f'<text class="carril" x="60" y="{y - 6}">FASE {i + 1}</text>'
                                    f'<text class="nn" x="60" y="{y + 13}">{escape(n)}</text>'
                                    f'<text class="sb" x="396" y="{y + 13}" text-anchor="end">{escape(s)}</text></g>')
            L.n_nodos += 1
    else:
        L = Lienzo(p, 960, 230, "Las siete fases de la metodología en una línea de tiempo, con lo que deja cada una.")
        xs = [92 + i * 129.3 for i in range(7)]
        for i, (fid, n, s) in enumerate(FASES):
            x = xs[i]
            if i:
                L.flecha(FASES[i - 1][0], fid, f"M{xs[i - 1] + 9:.0f} 115 H{x - 9:.0f}", punta=False)
            foco = fid == "des"
            arriba = i % 2 == 0
            yt = 46 if arriba else 152
            L.capas["nodos"].append(f'<g class="n hito{" foco" if foco else ""}" data-n="{fid}"><rect class="toque" x="{x - 118:.0f}" y="{yt - 18 if arriba else 92}" width="236" height="{(115 - yt + 30) if arriba else (yt + 44 - 92)}" rx="6"/>'
                                    f'<circle class="punto" cx="{x:.0f}" cy="115" r="{7 if foco else 5}"/>'
                                    f'<line class="regla" x1="{x:.0f}" y1="{100 if arriba else 130}" x2="{x:.0f}" y2="{(yt + 34) if arriba else (yt - 22)}"/>'
                                    f'<text class="carril" x="{x:.0f}" y="{yt - 4 if arriba else yt}" text-anchor="middle">FASE {i + 1}</text>'
                                    f'<text class="nn" x="{x:.0f}" y="{yt + 14 if arriba else yt + 18}" text-anchor="middle">{escape(n)}</text>'
                                    f'<text class="sb" x="{x:.0f}" y="{yt + 30 if arriba else yt + 34}" text-anchor="middle">{escape(s)}</text></g>')
            L.n_nodos += 1
    return L


FASES_FICHAS = {
    "vis": ("Visión", "La idea contada para entenderla y decidir.", None, [("", "", "Visión y documento fundacional; opcionales, otras visiones e infografías."), ("", "", "Skills documento_vision y documento_fundacional.")]),
    "esp": ("Especificación e interfaz", "Qué hace el producto, antes de la técnica.", None, [("", "", "Funcionalidades, recorridos, pantallas y estados, y criterios «Dado / Cuando / Entonces»."), ("", "", "Skill diseno_interfaz.")]),
    "tec": ("Definición técnica", "Una vez por proyecto, y corta.", None, [("", "", "Fija lo que evita que dos partes elijan de forma incompatible: paradigma, arquitectura y convenciones."), ("", "", "Skill definicion_tecnica.")]),
    "dvs": ("Devslices", "Incrementos verticales comprobables.", None, [("", "", "Cada una cabe en una o dos sesiones y deja algo que se ve funcionar.")]),
    "pre": ("Preparación", "Una devslice planificada aún no está lista.", None, [("", "", "Afinar alcance y criterios, resolver dudas, diseñar contratos y crear sus tareas.")]),
    "des": ("Desarrollo y verificación", "Pruebas anticipadas, backend primero.", None, [("", "", "Pruebas, lógica y datos, interfaz, comportamiento completo y revisión.")]),
    "cie": ("Cierre", "Evidencias, no impresiones.", None, [("", "", "Verificar criterios, registrar lo comprobado y lo pendiente, y actualizar la documentación.")]),
}


# ───────────────────────── 5. flujo de proceso: publicar con RELEASE ─────────────────────────

def proceso(p, vertical):
    if vertical:
        L = Lienzo(p, 420, 660, "Publicar con RELEASE, de arriba abajo: el propietario elige y confirma; el mod comprueba, sube la versión, pasa develop a main con su tag y hace push; los equipos ven ACTUALIZAR.")
        L.carril(8, 18, 404, "PROPIETARIO"), L.carril(8, 150, 404, "MOD · COLA.TS"), L.carril(8, 566, 404, "EQUIPOS")
        L.inicio(160, 30)
        L.flecha("ini", "eleg", "M160 35 V64"), L.boton(160, 50, "RELEASE", "ini", "eleg")
        L.flecha("eleg", "dec", "M160 120 V186")
        L.flecha("dec", "no", "M250 210 H300"), L.verbo(275, 202, "NO", "dec", "no")
        L.flecha("dec", "ver", "M160 234 V270"), L.verbo(168, 256, "SÍ", "dec", "ver", "start")
        L.flecha("ver", "ff", "M160 326 V362")
        L.flecha("ff", "push", "M160 418 V454")
        L.flecha("push", "fin", "M160 510 V586")
        L.nodo("eleg", 70, 64, 180, 56, "Elegir versión", "patch, minor o major")
        L.nodo("dec", 70, 186, 180, 48, "¿En orden?", (), "dec")
        L.nodo("no", 300, 182, 112, 56, "No publica", "dice qué falta", "sal")
        L.nodo("ver", 70, 270, 180, 56, "Subir versión", "commit «sf X.Y.Z»")
        L.nodo("ff", 70, 362, 180, 56, "develop → main", "fast-forward y tag", "foco")
        L.nodo("push", 70, 454, 180, 56, "Push", "develop, main y tag")
        L.nodo("fin", 70, 586, 180, 56, "Publicada", "sale ACTUALIZAR")
        L.texto(268, 62, "El segundo clic", "llamada"), L.texto(268, 80, "confirma y avisa", "llamada"), L.texto(268, 98, "de lo que queda en", "llamada"), L.texto(268, 116, "observación.", "llamada")
    else:
        L = Lienzo(p, 960, 300, "Publicar con RELEASE, de izquierda a derecha: el propietario elige y confirma; el mod comprueba, sube la versión, pasa develop a main con su tag y hace push; los equipos ven ACTUALIZAR.")
        L.carril(16, 20, 150, "PROPIETARIO"), L.carril(190, 20, 618, "MOD · COLA.TS"), L.carril(826, 20, 120, "EQUIPOS")
        L.inicio(103, 40)
        L.flecha("ini", "eleg", "M103 45 V80"), L.boton(103, 61, "RELEASE", "ini", "eleg")
        L.flecha("eleg", "dec", "M166 108 H198")
        L.flecha("dec", "no", "M262 132 V202"), L.verbo(270, 172, "NO", "dec", "no", "start")
        L.flecha("dec", "ver", "M326 108 H356"), L.verbo(341, 98, "SÍ", "dec", "ver")
        L.flecha("ver", "ff", "M482 108 H508")
        L.flecha("ff", "push", "M634 108 H660")
        L.flecha("push", "fin", "M786 108 H826")
        L.nodo("eleg", 40, 80, 126, 56, "Elegir versión", ["patch, minor", "o major"])
        L.nodo("dec", 198, 84, 128, 48, "¿En orden?", (), "dec")
        L.nodo("no", 198, 202, 128, 56, "No publica", "dice qué falta", "sal")
        L.nodo("ver", 356, 80, 126, 56, "Subir versión", ["commit", "«sf X.Y.Z»"])
        L.nodo("ff", 508, 80, 126, 56, "develop → main", ["fast-forward", "y tag"], "foco")
        L.nodo("push", 660, 80, 126, 56, "Push", ["develop, main", "y tag"])
        L.nodo("fin", 826, 80, 120, 56, "Publicada", ["sale", "ACTUALIZAR"])
        L.texto(30, 172, "El segundo clic", "llamada"), L.texto(30, 190, "confirma y avisa de", "llamada"), L.texto(30, 208, "lo que queda en", "llamada"), L.texto(30, 226, "observación.", "llamada")
    return L


PROC_FICHAS = {
    "eleg": ("Elegir versión", "Dos clics en RELEASE.", None, [("RELEASE", "", "el primero ofrece patch, minor y major desde el último tag"), ("RELEASE", "", "el segundo confirma y avisa de las tareas en observación")]),
    "dec": ("¿En orden?", "Lo comprueba antes de tocar nada.", None, [("", "", "Si algo no está en orden, no publica y dice cómo arreglarlo.")]),
    "no": ("No publica", "Dice qué falta y cómo arreglarlo.", None, [("", "", "No sube la versión ni toca main.")]),
    "ver": ("Subir versión", "Los manifiestos de la configuración.", None, [("", "", "En la SF, plugins/sf/.claude-plugin/plugin.json, en un commit «sf X.Y.Z» en develop; en los proyectos, «vX.Y.Z».")]),
    "ff": ("develop → main", "Fast-forward y tag vX.Y.Z.", None, [("", "", "main pasa a ser develop, sin merge, y queda marcada con el tag.")]),
    "push": ("Push", "Al remoto configurado.", None, [("", "", "Las dos ramas y el tag.")]),
    "fin": ("Publicada", "Lo ven los equipos.", None, [("ACTUALIZAR", "", "en rojo en cada panel: instala la versión y sus dependencias")]),
}


# ───────────────────────── 6. mapa de piezas del plugin ─────────────────────────

def piezas(p, vertical):
    if vertical:
        L = Lienzo(p, 420, 466, "Piezas del plugin sf en vertical: comandos, mod, plantillas, skills, herramientas y pruebas, y sus dependencias.")
        L.zona(8, 16, 404, 358, "PLUGIN SF · PLUGINS/SF/")
        L.flecha("cmd", "hooks", "M96 110 V178"), L.verbo(104, 148, "ABRE", "cmd", "hooks", "start")
        L.flecha("hooks", "tpl", "M96 234 V302"), L.verbo(104, 272, "ENTREGA", "hooks", "tpl", "start")
        L.flecha("skills", "tools", "M324 110 V178"), L.verbo(316, 148, "USAN", "skills", "tools", "end")
        L.flecha("hooks", "tools", "M176 206 H244"), L.verbo(210, 198, "LANZA", "hooks", "tools")
        L.flecha("plug", "deps", "M210 374 V400"), L.verbo(218, 392, "DEPENDE DE", "plug", "deps", "start")
        L.nodo("cmd", 16, 54, 160, 56, "Comandos", "/sf y /sf_…", tipo="ENTRADA")
        L.nodo("hooks", 16, 178, 160, 56, "Mod de estado", "hooks/ · panel", "foco", tipo="MOD")
        L.nodo("tpl", 16, 302, 160, 56, "Plantillas", "reglas de proyecto", tipo="PLANTILLA")
        L.nodo("skills", 244, 54, 160, 56, "Skills", "13 · método y docs", tipo="SKILL")
        L.nodo("tools", 244, 178, 160, 56, "Herramientas", "cola.py · kit", tipo="CLI")
        L.nodo("tests", 244, 302, 160, 56, "Pruebas", "tests/ · unittest", tipo="PRUEBA")
        L.nodo("deps", 110, 400, 200, 56, "Dependencias", "threejs · oklch · gsap", "sal", tipo="EXTERNA")
    else:
        L = Lienzo(p, 960, 330, "Piezas del plugin sf: comandos, mod, herramientas, pruebas, plantillas y skills, y sus dependencias.")
        L.zona(12, 16, 936, 236, "PLUGIN SF · PLUGINS/SF/")
        L.flecha("cmd", "hooks", "M276 84 H360"), L.verbo(318, 76, "ABRE", "cmd", "hooks")
        L.flecha("hooks", "tools", "M596 84 H680"), L.verbo(638, 76, "LANZA", "hooks", "tools")
        L.flecha("hooks", "tpl", "M478 112 V170"), L.verbo(486, 146, "ENTREGA", "hooks", "tpl", "start")
        L.flecha("skills", "tools", "M798 170 V112"), L.verbo(806, 146, "USAN", "skills", "tools", "start")
        L.flecha("plug", "deps", "M480 252 V274"), L.verbo(488, 268, "DEPENDE DE", "plug", "deps", "start")
        L.nodo("cmd", 40, 56, 236, 56, "Comandos", "commands/ · /sf y /sf_…", tipo="ENTRADA")
        L.nodo("hooks", 360, 56, 236, 56, "Mod de estado", "hooks/ · panel y avisos", "foco", tipo="MOD")
        L.nodo("tools", 680, 56, 236, 56, "Herramientas", "tools/ · cola.py y kit", tipo="CLI")
        L.nodo("tests", 40, 170, 236, 56, "Pruebas", "tests/ · unittest", tipo="PRUEBA")
        L.nodo("tpl", 360, 170, 236, 56, "Plantillas", "templates/ · reglas", tipo="PLANTILLA")
        L.nodo("skills", 680, 170, 236, 56, "Skills", "skills/ · 13 del método", tipo="SKILL")
        L.nodo("deps", 360, 274, 240, 50, "Dependencias", "threejs · oklch · gsap", "sal", tipo="EXTERNA")
    return L


PIEZAS_FICHAS = {
    "cmd": ("Comandos", "commands/ y los que registra el mod.", None, [("", "", "/sf abre el panel; /sf_config, /sf_prueba, /sf_split y los demás, en register.tsx.")]),
    "hooks": ("Mod de estado", "hooks/: panel, avisos y reglas.", None, [("", "", "panel.tsx pinta el panel; cola.ts lanza cola.py y hace RELEASE, ACTUALIZAR y REFRESCAR; contexto.ts entrega las reglas y la orquestación.")]),
    "tools": ("Herramientas", "tools/: lo que se hace con un comando.", None, [("", "", "cola.py, el lanzador cola_sesion.py, configuracion.py, indice_decisiones.py y el kit de documentos.")]),
    "tests": ("Pruebas", "tests/, con unittest.", None, [("", "", "Se pasan antes de cerrar con «python -m unittest discover -s tests».")]),
    "tpl": ("Plantillas", "templates/.", None, [("", "", "claude-sf.md y claude-sf-metodologia.md, que el mod entrega; estructuras por perfil y propuestas.md.")]),
    "skills": ("Skills", "skills/: el método y los documentos.", None, [("", "", "metodologia, orquestacion, flujo_tareas, crear_documentos, documento_vision, definicion_tecnica…")]),
    "deps": ("Dependencias", "Skills externas, tal cual.", None, [("", "", "threejs-skills, oklch-skill y gsap-skills, fijadas en el catálogo softwarefactory.")]),
}


# ───────────────────────── figura ─────────────────────────

def croquetas(fichas):
    o = []
    for fid, (t, resumen, marcas, lineas) in fichas.items():
        cuerpo = [f'<p class="res">{escape(resumen)}</p>']
        if marcas:
            cuerpo.append('<ul class="marcas">' + "".join(f'<li>{"✓" if c == "✓" else "✕"} {n}</li>' for c, n in zip(marcas, ["rama", "subagente", "en develop"])) + '</ul>')
        cuerpo.append('<ul class="lineas">' + "".join(
            (f'<li><span class="bt-h {({"RELEASE": "rel", "ACTUALIZAR": "de"}.get(b, k or "ok"))}">{escape(b)}</span> {escape(x)}</li>' if b else f'<li class="{"cl-li" if k == "cl" else ""}">{escape(x)}</li>')
            for b, k, x in lineas) + '</ul>')
        o.append(f'<details class="croq" data-f="{fid}"><summary><span class="croq-t">{escape(t)}</span></summary><div class="cuerpo">{"".join(cuerpo)}</div></details>')
    return '<div class="croquetas">' + "".join(o) + '</div>'


def desc(t):
    """La descripción, con su primera frase aparte para la forma corta."""
    m = re.match(r"(.+?[.:])\s+(.+)$", t)
    if not m:
        return f'<span class="d-corta">{escape(t)}</span>'
    return f'<span class="d-corta">{escape(m.group(1))}</span><span class="d-resto"> {escape(m.group(2))}</span>'


def figura(fid, tipo, titulo, subt, fn, fichas):
    h, v = fn(fid + "h", False), fn(fid + "v", True)
    pie = f"{tipo.upper()} · {h.n_nodos} NODOS · {h.n_flechas} FLECHAS"
    return (f'<figure class="fig" id="{fid}"><div class="marco cq" data-fig>'
            f'<div class="cab"><p class="ceja">{escape(tipo)}</p><h3 class="tit">{escape(titulo)}</h3></div><p class="subt">{desc(subt)}</p>'
            f'<div class="lienzo"><div class="solo-h">{h.svg("h")}</div><div class="solo-v">{v.svg("v")}</div>'
            f'<div class="hud" hidden role="region" aria-label="Ficha" aria-live="polite"><button type="button" class="x" aria-label="Cerrar la ficha">✕</button><div class="hud-c"></div></div></div>'
            f'{croquetas(fichas)}'
            f'<p class="pista">Pulsa un elemento para abrir su ficha; pasa el ratón o llega con el tabulador para resaltar su recorrido. Escape la cierra.</p>'
            f'<div class="pie"><span class="firma">SÍNTESIS SF · ESTÉTICA DIAGRAM-DESIGN</span><span class="cuenta">{pie}</span></div></div></figure>'), (h, v)


REGLAS = [
    ("Un lienzo por orientación", "Cada diagrama se dibuja dos veces con los mismos datos e ids: vertical a 420 de ancho (la de partida) y horizontal a 960. La figura elige por su propio ancho con <code>@container</code>: horizontal desde 800 px."),
    ("Letra mínima", "Nada mide menos de 12 en el SVG: a 375 la vertical queda a unos 9 px reales, y la horizontal no baja de 10. Nombres a 15 en Geist; etiquetas y subtítulos en Geist Mono; lo que hace Claude y las llamadas, en cursiva Instrument Serif."),
    ("Paleta por funciones", "Tinta, apagado, papel y nodo, con un solo acento para el foco. Lo destructivo se distingue por el borde discontinuo, no por otro color. Sin sombras ni degradados."),
    ("Un foco por diagrama", "El acento marca una sola cosa: el estado del que se habla, la pieza clave o el paso esencial."),
    ("Flechas en ángulo recto", "Codos redondeados (r = 8), sin diagonales; entran y salen perpendiculares al borde y lejos de las esquinas."),
    ("Etiquetas sobre su máscara", "Los verbos van en mayúsculas monoespaciadas, sobre un fondo opaco y separados de la línea; al lado en los tramos verticales; sin solapes."),
    ("Etiquetas como diagram-design", "La orden del panel es texto mono separado de su flecha, sin cápsula ni fondo; solo el texto lleva el color de su botón (verde, rojo o morado). Lo que hace Claude, en cursiva y con la flecha discontinua."),
    ("Carriles con nombre", "Cada lado tiene un nombre (vueltas, fases, salidas; o el actor), que dice qué es cada flecha antes que su forma."),
    ("Presupuesto", "Como mucho 9 nodos y 12 flechas. Lo que vale desde varios estados va a una nota «desde cualquier estado», no a más flechas."),
    ("Fichas de una en una", "Cada nodo tiene su ficha: al pulsarlo se abre (y se cierra la anterior), como HUD junto al nodo en la horizontal y como croqueta debajo en la vertical. Se resaltan sus flechas al pasar el ratón o con el foco; Escape cierra. Sin script, las croquetas siguen ahí."),
    ("Accesible", "Cada SVG con su aria-label; los nodos con foco de teclado, Intro y Espacio; transiciones cortas que se apagan con movimiento reducido."),
    ("Comprobado", "A 1440 y a 375, en claro y en oscuro: sin desbordar la página y sin letra por debajo del mínimo."),
]


CSS = r"""
:root{--papel:#f5f5f4;--papel2:#ebeae7;--nodo:#ffffff;--tinta:#25283a;--apagado:#4f5871;--suave:#6a7388;--regla:rgba(37,40,58,.14);--regla-f:#b9bcc4;--acento:#b8431c;--tinte:rgba(184,67,28,.08);--fondo:#fbfbfa;--puntos:rgba(37,40,58,.08);--b-ok:#15803d;--b-de:#dc2626;--b-rel:#9333ea}
:root[data-theme=dark]{--papel:#23263a;--papel2:#2f3349;--nodo:#2b2f45;--tinta:#f2f2f0;--apagado:#b8bdc9;--suave:#9aa1b2;--regla:rgba(242,242,240,.12);--regla-f:#575d75;--acento:#f08a59;--tinte:rgba(240,138,89,.12);--fondo:#1b1d2c;--puntos:rgba(242,242,240,.06);--b-ok:#4ade80;--b-de:#f87171;--b-rel:#c084fc}
*{box-sizing:border-box}
html{background:var(--fondo)}
body{margin:0;background:var(--fondo);color:var(--tinta);font:16px/1.55 'Geist',system-ui,sans-serif}
a{color:var(--acento)}
main{max-width:1200px;margin:0 auto;padding:2rem 16px 4rem}
.cabecera{display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;flex-wrap:wrap}
h1{font:400 clamp(2rem,5vw,2.8rem)/1.05 'Instrument Serif',serif;margin:.2rem 0 .6rem}
.ceja-p{font:500 .7rem 'Geist Mono',monospace;letter-spacing:.18em;text-transform:uppercase;color:var(--suave);margin:0}
.intro{max-width:46rem;color:var(--apagado)}
.tema{font:500 .72rem 'Geist Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--tinta);background:var(--nodo);border:1px solid var(--regla-f);border-radius:4px;min-height:44px;padding:0 1rem;cursor:pointer;margin-top:.4rem}
.tema:focus-visible,.x:focus-visible,summary:focus-visible{outline:2px solid var(--acento);outline-offset:2px}
nav{display:flex;flex-wrap:wrap;gap:.3rem 1rem;font-size:.92rem;margin:1rem 0 0}
.fig{margin:2.2rem 0 0}
.marco{container-type:inline-size;background:var(--papel);border:1px solid var(--regla);border-radius:10px;padding:24px 22px 14px}
.ceja{font:500 .7rem 'Geist Mono',monospace;letter-spacing:.18em;text-transform:uppercase;color:var(--suave);margin:0}
.tit{font:400 2rem/1.1 'Instrument Serif',serif;margin:.25rem 0 .3rem}
.subt{font-size:.95rem;color:var(--apagado);max-width:46rem;margin:0 0 1rem}
.lienzo{position:relative}
.lienzo svg{display:block;width:100%;height:auto}
.solo-h{display:none} .solo-v svg{max-width:520px;margin:0 auto}
@container (min-width:800px){.solo-h{display:block}.solo-v{display:none}.js .croquetas{display:none}.js .pista{margin-top:.9rem}}
@container (max-width:799px){.hud{display:none!important}}
@container (max-width:480px){.tit{font-size:1.6rem}}
@media (max-width:480px){.marco{padding:16px 10px 10px}}
.papel{fill:var(--papel)}
.carril{font:500 12px 'Geist Mono',monospace;letter-spacing:.14em;fill:var(--suave)}
.regla{stroke:var(--regla-f);stroke-width:1}
.zona{fill:none;stroke:var(--regla-f);stroke-dasharray:4 3}
.caja{fill:var(--nodo);stroke:var(--tinta);stroke-width:1}
.foco .caja{fill:var(--tinte);stroke:var(--acento);stroke-width:1.5}
.sal .caja{fill:var(--papel2);stroke:var(--apagado)}
.nn{font:600 15px 'Geist',sans-serif;fill:var(--tinta)} .foco .nn{fill:var(--acento)}
.sb{font:400 12px 'Geist Mono',monospace;fill:var(--apagado)}
.fin-a{fill:none;stroke:var(--tinta);stroke-width:1.2} .fin{fill:var(--tinta)}
.ini{fill:var(--tinta)}
.fl{fill:none;stroke:var(--apagado);stroke-width:1.3;transition:opacity .2s,stroke .2s} .fl.claude,.fl.dash{stroke-dasharray:5 4} .fl.acc{stroke:var(--acento);stroke-width:1.6}
.ah{fill:var(--apagado)} .ah-a{fill:var(--acento)}
.masc{fill:var(--papel)}
.lb{font:500 12px 'Geist Mono',monospace;letter-spacing:.04em;fill:var(--apagado)} .lb.acc-t{fill:var(--acento)}
.cl{font:italic 400 15px 'Instrument Serif',serif;fill:var(--apagado)}
.lb.ok{fill:var(--b-ok)} .lb.de{fill:var(--b-de)} .lb.rel{fill:var(--b-rel)}
.tipo-c{fill:none;stroke:var(--tinta);stroke-opacity:.4;stroke-width:.8} .tipo{font:500 12px 'Geist Mono',monospace;letter-spacing:.1em;fill:var(--tinta)}
html:not(.sin-tipos) .contipo .desplaza{transform:translateY(10px)}
.nota rect{fill:var(--papel2);stroke:none} .nota-c{font:500 12px 'Geist Mono',monospace;letter-spacing:.06em;fill:var(--suave)} .nota-t{font:400 13px 'Geist',sans-serif;fill:var(--tinta)}
.llamada{font:italic 400 15px 'Instrument Serif',serif;fill:var(--apagado)}
.vida{stroke:var(--regla-f);stroke-dasharray:3 4} .act{fill:var(--nodo);stroke:var(--apagado);stroke-width:1}
.estado rect{fill:var(--papel2);stroke:var(--regla-f)} .estado text{font:500 12px 'Geist Mono',monospace;fill:var(--tinta)}
.hito .toque{fill:transparent;stroke:none} .hito .punto{fill:var(--tinta)} .hito.foco .punto{fill:var(--acento)}
.n{cursor:pointer;outline:none;transition:opacity .2s}
.n:focus-visible .caja,.n:focus-visible .toque{stroke:var(--acento);stroke-width:2}
.hl .fl{opacity:.18} .hl .fl.on{opacity:1;stroke:var(--acento);stroke-width:2.2}
.hl .n{opacity:.4} .hl .n.on,.hl .n.cerca{opacity:1} .n.on .caja{stroke:var(--acento);stroke-width:2}
.hl .et{opacity:.35} .hl .et.on{opacity:1} .et{transition:opacity .2s}
.hl .vida{opacity:.4} .hl .vida.on{opacity:1}
.hito.on .toque{fill:var(--tinte)}
.hud{position:absolute;width:300px;background:var(--nodo);border:1px solid var(--regla-f);border-radius:6px;padding:12px 14px;font-size:.86rem;line-height:1.45;color:var(--apagado);z-index:2}
.hud[hidden]{display:none}
.hud h4,.croq .croq-t{font:400 1.45rem/1.1 'Instrument Serif',serif;color:var(--tinta);margin:0}
.hud h4{padding-right:3rem;margin-bottom:.35rem}
.x{position:absolute;top:8px;right:8px;min-width:44px;min-height:44px;background:var(--nodo);color:var(--tinta);border:1px solid var(--regla-f);border-radius:4px;cursor:pointer;font-size:1rem}
.res{margin:0 0 .4rem}
.marcas{display:flex;gap:.8rem;flex-wrap:wrap;list-style:none;margin:0 0 .4rem;padding:0;font:500 .72rem 'Geist Mono',monospace;letter-spacing:.04em;color:var(--tinta)}
.lineas{list-style:none;margin:0;padding:0} .lineas li{margin:.3rem 0}
.bt-h{font:500 .74rem 'Geist Mono',monospace;letter-spacing:.06em;color:var(--apagado)} .bt-h.ok{color:var(--b-ok)} .bt-h.de{color:var(--b-de)} .bt-h.rel{color:var(--b-rel)}
.cl-li{font-style:italic}
.croquetas{display:grid;gap:8px;margin-top:14px}
.croq{background:var(--nodo);border:1px solid var(--regla);border-radius:6px}
.croq summary{cursor:pointer;list-style:none;padding:.55rem .9rem;min-height:44px;display:flex;align-items:center;justify-content:space-between}
.croq summary::-webkit-details-marker{display:none}
.croq summary::after{content:'+';font:500 1rem 'Geist Mono',monospace;color:var(--suave)} .croq[open] summary::after{content:'−'}
.croq[open]{border-color:var(--acento)}
.croq .croq-t{font-size:1.2rem}
.croq .cuerpo{padding:0 .9rem .7rem;font-size:.88rem;color:var(--apagado)}
.pista{font-size:.84rem;color:var(--suave);margin:.6rem 0 0}
.pie{display:flex;justify-content:space-between;flex-wrap:wrap;gap:.4rem;font:500 .64rem 'Geist Mono',monospace;letter-spacing:.16em;color:var(--suave);border-top:1px solid var(--regla);margin-top:12px;padding-top:9px}
section.reglas{margin-top:3rem;border-top:1px solid var(--regla);padding-top:1.2rem}
section.reglas h2{font:400 2rem 'Instrument Serif',serif;margin:0 0 .6rem}
ol.reglas{max-width:52rem;padding-left:1.4rem} ol.reglas li{margin:.45rem 0} ol.reglas b{font-weight:600}
.tokens{max-width:52rem;background:var(--papel);border:1px solid var(--regla);border-radius:8px;padding:.8rem 1rem}
code{font:.88em 'Geist Mono',monospace}
@media (prefers-reduced-motion:reduce){.fl,.n,.et{transition:none}}
/* panel de casillas */
.ajustes-b{display:none;align-items:center;gap:.45rem;min-height:40px;padding:0 .85rem;font:500 .68rem 'Geist Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--apagado);background:var(--nodo);border:1px solid var(--regla-f);border-radius:999px;cursor:pointer;opacity:.85}
.js[data-herramientas~=ajustes] .ajustes-b{display:inline-flex}
.ajustes-b:hover,.ajustes-b[aria-expanded=true]{opacity:1;color:var(--tinta)} .ajustes-b:focus-visible,.op-x:focus-visible{outline:2px solid var(--acento);outline-offset:2px}
.lc-fila .orig{margin-left:auto;font:500 .62rem 'Geist Mono',monospace;letter-spacing:.08em;color:var(--suave)}
.sin-color .lb.ok,.sin-color .lb.de,.sin-color .lb.rel{fill:var(--apagado)} .sin-color .bt-h{color:var(--apagado)!important}
.sin-carriles .carril-g{display:none}
.sin-cursiva .cl-claude{font:500 12px 'Geist Mono',monospace;letter-spacing:.04em;text-transform:uppercase} .sin-cursiva .cl-li{font-style:normal}
.sin-discontinua .fl.claude{stroke-dasharray:none}
.sin-fichas .n{cursor:default} .sin-fichas .pista{display:none}
.sin-croquetas .croquetas{display:none!important}
.sin-recuento .cuenta{display:none}
.sin-tipos .tipo-g{display:none}
.sin-foco .foco .caja{fill:var(--nodo);stroke:var(--tinta);stroke-width:1} .sin-foco .foco .nn{fill:var(--tinta)} .sin-foco .hito.foco .punto{fill:var(--tinta)} .sin-foco .fl.acc{stroke:var(--apagado);stroke-width:1.3} .sin-foco .lb.acc-t{fill:var(--apagado)}
[data-o-orient=horizontal] .solo-h{display:block!important;overflow-x:auto} [data-o-orient=horizontal] .solo-h svg{min-width:960px} [data-o-orient=horizontal] .solo-v{display:none!important}
[data-o-orient=vertical] .solo-h{display:none!important} [data-o-orient=vertical] .solo-v{display:block!important} .js[data-o-orient=vertical] .croquetas{display:grid} [data-o-orient=vertical] .hud{display:none!important}
.cab{display:flex;flex-direction:column}
[data-o-ceja=lado] .cab{flex-direction:row-reverse;justify-content:flex-end;align-items:baseline;flex-wrap:wrap;gap:.2rem 1rem}
[data-o-ceja=oculto] .ceja{display:none}
[data-o-titulo=serifa-p] .tit{font-size:1.45rem!important}
[data-o-titulo=sans] .tit{font:600 1.25rem/1.25 'Geist',sans-serif!important;letter-spacing:-.01em}
[data-o-titulo=mono] .tit{font:500 .95rem/1.3 'Geist Mono',monospace!important;letter-spacing:.1em;text-transform:uppercase}
[data-o-titulo=oculto] .tit{display:none}
[data-o-desc=linea] .subt{max-width:none} [data-o-desc=corta] .d-resto{display:none}
[data-o-desc=oculta] .subt{display:none} [data-o-desc=oculta] .cab{margin-bottom:1rem}
.sin-regla .pie{border-top:0;padding-top:0}
[data-o-pie=centrado] .pie{justify-content:center;opacity:.85} [data-o-pie=centrado] .pie .cuenta::before{content:'· '}
[data-o-pie=oculto] .pie{display:none}
.marco{display:flex;flex-direction:column}
[data-o-pista=encima] .pista{order:-1;margin:0 0 .6rem} [data-o-pista=encima] .cab,[data-o-pista=encima] .subt{order:-2}
[data-o-pista=discreta] .pista{font:italic .9rem 'Instrument Serif',serif;opacity:.85}
[data-o-pista=oculta] .pista{display:none}
.sin-notas .nota rect{fill:none} .sin-notas .nota-t{font:italic 400 15px 'Instrument Serif',serif;fill:var(--apagado)}
/* marcos y flechas finos, como el original: grosor fijo en pantalla */
.sin-marcos .caja,.sin-marcos .fl,.sin-marcos .zona,.sin-marcos .regla,.sin-marcos .act,.sin-marcos .estado rect,.sin-marcos .fin-a{vector-effect:non-scaling-stroke}
.sin-marcos .caja{stroke-width:.8} .sin-marcos .foco .caja{stroke-width:1} .sin-marcos .fl{stroke-width:.95} .sin-marcos .fl.acc{stroke-width:1.1} .sin-marcos rect.caja{rx:8px}
.sin-marcos .hl .fl.on{stroke-width:1.6}
/* letra en las proporciones del original (nombres 13, etiquetas 8 en un lienzo de 1000) */
.sin-letra .nn{font-size:13px} .sin-letra .sb{font-size:9.5px} .sin-letra .lb{font-size:8.5px;letter-spacing:.06em} .sin-letra .carril{font-size:8.5px;letter-spacing:.14em}
.sin-letra .cl{font-size:14px} .sin-letra .estado text{font-size:9.5px} .sin-letra .nota-c{font-size:9px} .sin-letra .nota-t{font-size:12px} .sin-letra .tipo{font-size:8px}
.sin-letra.sin-cursiva .cl-claude{font-size:8.5px}
.sin-letra .tipo-g{transform-box:fill-box;transform-origin:left top;transform:scale(.67)} .sin-letra .tipo{font-size:12px}

"""

JS = r"""
document.documentElement.classList.add('js');
function activo(k){return !document.documentElement.classList.contains('sin-'+k);}
(function(){
  var r=document.documentElement, d=document.getElementById('opciones');
  if(!d||!/\bajustes\b/.test(r.getAttribute('data-herramientas')||'')) return;
  var cajas=[].slice.call(d.querySelectorAll('[data-op]')), sels=[].slice.call(d.querySelectorAll('[data-sel]')), CLAVE='sf-sintesis-opciones-3', bt=document.querySelector('.ajustes-b');
  function abre(o){d.hidden=!o; bt.setAttribute('aria-expanded',String(o)); if(o) d.querySelector('.ml-caja').focus(); else bt.focus();}
  bt.onclick=function(){abre(true);}; d.querySelector('.ml-cerrar').onclick=function(){abre(false);};
  d.addEventListener('mousedown',function(e){if(e.target===d) abre(false);});
  d.addEventListener('keydown',function(e){
    if(e.key==='Escape'){e.stopPropagation(); abre(false); return;}
    if(e.key!=='Tab') return;
    var f=[].slice.call(d.querySelectorAll('button, select, input')), i=f.indexOf(document.activeElement);
    if(e.shiftKey&&i<=0){e.preventDefault(); f[f.length-1].focus();} else if(!e.shiftKey&&i===f.length-1){e.preventDefault(); f[0].focus();}
  });
  function val(s){if(s.tagName==='SELECT') return s.value; var c=s.querySelector('input:checked'); return c?c.value:s.getAttribute('data-def');}
  function fija(s,v){if(s.tagName==='SELECT'){if(s.querySelector('option[value="'+v+'"]')) s.value=v; return;} var c=s.querySelector('input[value="'+v+'"]'); if(c) c.checked=true;}
  function guarda(){try{var o={};cajas.forEach(function(c){o[c.getAttribute('data-op')]=c.checked;});sels.forEach(function(s){o['s-'+s.getAttribute('data-sel')]=val(s);});localStorage.setItem(CLAVE,JSON.stringify(o));}catch(e){}}
  function aplica(){
    cajas.forEach(function(c){r.classList.toggle('sin-'+c.getAttribute('data-op'),!c.checked);});
    sels.forEach(function(s){r.setAttribute('data-o-'+s.getAttribute('data-sel'),val(s));});
    document.querySelectorAll('.fl.acc').forEach(function(e){var m=e.getAttribute('marker-end'); if(m) e.setAttribute('marker-end',activo('foco')?m.replace(/-m\)$/,'-a)'):m.replace(/-a\)$/,'-m)'));});
    d.querySelector('.cuantas').textContent=cajas.filter(function(c){return c.checked;}).length+' de '+cajas.length;
    document.dispatchEvent(new Event('opciones'));
  }
  try{var g=JSON.parse(localStorage.getItem(CLAVE)||'null'); if(g){cajas.forEach(function(c){var k=c.getAttribute('data-op'); if(k in g) c.checked=!!g[k];}); sels.forEach(function(s){var v=g['s-'+s.getAttribute('data-sel')]; if(v) fija(s,v);});}}catch(e){}
  cajas.concat(sels).forEach(function(c){c.addEventListener('change',function(){aplica();guarda();});});
  function pon(a){cajas.forEach(function(c){c.checked=c.getAttribute(a)==='1';}); sels.forEach(function(s){fija(s,s.getAttribute(a));}); aplica(); guarda();}
  d.querySelector('[data-todo]').onclick=function(){pon('data-def');};
  d.querySelector('[data-original]').onclick=function(){pon('data-orig');};
  aplica();
})();
(function(){
  var b=document.getElementById('tema'), r=document.documentElement;
  b.onclick=function(){var o=r.getAttribute('data-theme')!=='dark';r.setAttribute('data-theme',o?'dark':'light');b.setAttribute('aria-pressed',String(o));b.textContent=o?'Modo claro':'Modo oscuro';};
})();
document.querySelectorAll('[data-fig]').forEach(function(fig){
  var lienzo=fig.querySelector('.lienzo'), hud=fig.querySelector('.hud'), hc=fig.querySelector('.hud-c'), sel=null, desde=null;
  function ancho(){return fig.querySelector('.solo-h').offsetParent!==null;}
  function marca(id){
    fig.classList.toggle('hl',!!id);
    var cerca={};
    fig.querySelectorAll('[data-de]').forEach(function(e){
      var on=!!id&&(e.getAttribute('data-de')===id||e.getAttribute('data-a')===id);
      e.classList.toggle('on',on);
      if(on){cerca[e.getAttribute('data-de')]=1;cerca[e.getAttribute('data-a')]=1;}
      var m=e.getAttribute('marker-end');
      if(m&&!e.classList.contains('acc')) e.setAttribute('marker-end',on?m.replace(/-m\)$/,'-a)'):m.replace(/-a\)$/,'-m)'));
    });
    fig.querySelectorAll('.n').forEach(function(n){var k=n.getAttribute('data-n');n.classList.toggle('on',k===id);n.classList.toggle('cerca',!!cerca[k]&&k!==id);});
  }
  function croq(id){fig.querySelectorAll('.croq').forEach(function(d){d.open=d.getAttribute('data-f')===id;});}
  function pon(nodo){
    var L=lienzo.getBoundingClientRect(), r=nodo.getBoundingClientRect(), w=hud.offsetWidth, h=hud.offsetHeight;
    var x=r.right-L.left+12; if(x+w>L.width) x=r.left-L.left-w-12; if(x<0) x=Math.max(0,L.width-w);
    var y=r.top-L.top; y=Math.max(0,Math.min(y,L.height-h));
    hud.style.left=x+'px'; hud.style.top=y+'px';
  }
  function abre(id,nodo){
    sel=id; marca(activo('resaltado')?id:null); croq(id);
    fig.querySelectorAll('.n').forEach(function(n){n.setAttribute('aria-expanded',String(n.getAttribute('data-n')===id));});
    if(!id){hud.hidden=true; if(desde){desde.focus();} desde=null; return;}
    if(nodo) desde=nodo;
    var d=fig.querySelector('.croq[data-f="'+id+'"]');
    hc.innerHTML='<h4></h4>'; hc.firstChild.textContent=d.querySelector('.croq-t').textContent;
    hc.insertAdjacentHTML('beforeend',d.querySelector('.cuerpo').innerHTML);
    if(ancho()&&nodo){hud.hidden=false; pon(nodo);} else hud.hidden=true;
  }
  fig.querySelectorAll('.n').forEach(function(n){
    var id=n.getAttribute('data-n'), d=fig.querySelector('.croq[data-f="'+id+'"]'); if(!d) return;
    n.setAttribute('tabindex','0'); n.setAttribute('role','button'); n.setAttribute('aria-expanded','false');
    n.setAttribute('aria-label',d.querySelector('.croq-t').textContent+': abrir su ficha');
    n.addEventListener('mouseenter',function(){if(!sel&&activo('resaltado')) marca(id);});
    n.addEventListener('mouseleave',function(){if(!sel) marca(null);});
    n.addEventListener('focus',function(){if(!sel&&activo('resaltado')) marca(id);});
    n.addEventListener('blur',function(){if(!sel) marca(null);});
    n.addEventListener('click',function(){if(activo('fichas')) abre(sel===id?null:id,n);});
    n.addEventListener('keydown',function(ev){if((ev.key==='Enter'||ev.key===' ')&&activo('fichas')){ev.preventDefault();abre(sel===id?null:id,n);}});
  });
  fig.querySelectorAll('.croq').forEach(function(d){
    d.querySelector('summary').addEventListener('click',function(ev){ev.preventDefault();var id=d.getAttribute('data-f');abre(d.open?null:id,null);});
  });
  fig.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&sel) abre(null);});
  document.addEventListener('opciones',function(){if(sel&&(!activo('fichas'))){sel=null;marca(null);croq(null);hud.hidden=true;}});
  hud.querySelector('.x').onclick=function(){abre(null);};
});
"""

# Casillas: clave, texto, si el original de diagram-design lo tiene y si va encendida por defecto (las favoritas
# del propietario). «Como el original» deja encendidas solo las que el original también tiene.
OPCIONES = [
    ("color", "Etiquetas con el color del botón", False, True),
    ("carriles", "Carriles con nombre", False, False),
    ("cursiva", "Cursiva para lo que hace Claude", False, True),
    ("discontinua", "Flecha discontinua para lo que hace Claude", True, True),
    ("notas", "Notas «desde cualquier estado» en recuadro", False, True),
    ("tipos", "Chips de tipo (FASE, SALIDA…)", True, False),
    ("foco", "Acento de foco", True, True),
    ("recuento", "Recuento de nodos y flechas en el pie", True, False),
    ("regla", "Línea sobre el pie", True, True),
    ("marcos", "Marcos y flechas más gruesos", False, False),
    ("letra", "Letra más grande (mínimo legible)", False, False),
    ("resaltado", "Resaltado del recorrido al pasar", False, True),
    ("fichas", "Fichas y HUD al pulsar", False, True),
    ("croquetas", "Croquetas bajo la figura", False, True),
]

# Temas para probar: los de documento de crear_documentos (assets/temas/), que son los que verán los diagramas,
# con el color de sesión que les corresponde; y los colores de sesión que no tienen tema de documento, sacados de
# su RGB (hooks/constantes.ts). Cada uno da el acento (foco) y, los de documento, el papel y la tinta en claro.
TEMAS_PLUGIN = Path(__file__).resolve().parents[2] / "plugins/sf/skills/crear_documentos/assets/temas"
SESION_DE_TEMA = {"colorido": "blue", "morado": "purple", "pool": "green", "rojo": "red", "teal": "cyan"}
SESION_SIN_TEMA = {"yellow": "#ca8a04", "orange": "#ea580c", "pink": "#db2777"}


def _mezcla(c, con, k):
    a = [int(c[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(con[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * k):02x}" for x, y in zip(a, b))


def _rgba(c, a):
    return f"rgba({int(c[1:3], 16)},{int(c[3:5], 16)},{int(c[5:7], 16)},{a})"


def temas():
    """[(valor, texto, css)] de los temas que se pueden probar."""
    import json
    out = []
    for f in sorted(TEMAS_PLUGIN.glob("*.json")):
        t = json.loads(f.read_text(encoding="utf-8")); c = {k: v.lower() for k, v in t["colores"].items()}
        pri = c["primario"]; vivo = _mezcla(pri, "#ffffff", .38)
        claro = (f"--acento:{pri};--tinte:{_rgba(pri, .08)};--papel:{c.get('pagina', '#f5f5f4')};--papel2:{c.get('fondo-medio', '#ebeae7')};"
                 f"--tinta:{c.get('texto', '#25283a')};--apagado:{c.get('texto-suave', '#4f5871')};--regla-f:{c.get('borde', '#b9bcc4')}")
        oscuro = f"--acento:{vivo};--tinte:{_rgba(vivo, .14)}"
        out.append((f.stem, f"{t.get('nombre', f.stem)} · sesión {SESION_DE_TEMA.get(f.stem, '—')}", claro, oscuro))
    for k, rgb in SESION_SIN_TEMA.items():
        fuerte = _mezcla(rgb, "#000000", .22 if k == "yellow" else .08)
        out.append((k, f"{k} · sin tema de documento", f"--acento:{fuerte};--tinte:{_rgba(fuerte, .08)}",
                    f"--acento:{_mezcla(rgb, '#ffffff', .25)};--tinte:{_rgba(rgb, .14)}"))
    return out


def css_temas():
    return "\n".join(f":root[data-o-tema={v}]:not([data-theme=dark]){{{cl}}} :root[data-o-tema={v}][data-theme=dark]{{{os}}}"
                      for v, _, cl, os in temas())


# Selectores: clave, texto, opciones (valor, texto), valor por defecto y valor «como el original».
SELECTORES = [
    ("tema", "Tema", [("dd", "diagram-design (el de la síntesis)")] + [(v, t) for v, t, _, _ in temas()], "dd", "dd"),
    ("orient", "Orientación", [("auto", "Automática: vertical si es estrecha"), ("vertical", "Siempre vertical"), ("horizontal", "Siempre horizontal")], "auto", "horizontal"),
    ("ceja", "Antetítulo", [("encima", "Encima del título"), ("lado", "Al lado del título"), ("oculto", "Oculto")], "oculto", "encima"),
    ("titulo", "Título", [("sans", "Sans"), ("serifa", "Serifa grande"), ("serifa-p", "Serifa pequeña"), ("mono", "Mono en mayúsculas"), ("oculto", "Oculto")], "sans", "serifa"),
    ("desc", "Descripción", [("completa", "Completa, en columna"), ("linea", "En una línea (salta si hace falta)"), ("corta", "Corta: la primera frase"), ("oculta", "Oculta")], "linea", "completa"),
    ("pie", "Pie", [("dos", "A dos lados"), ("centrado", "Centrado"), ("oculto", "Oculto")], "dos", "dos"),
    ("pista", "Línea de ayuda", [("debajo", "Debajo de la figura"), ("encima", "Encima de la figura"), ("discreta", "Debajo, discreta"), ("oculta", "Oculta")], "encima", "oculta"),
]


def panel_opciones():
    cas = "".join(f'<label class="lc-fila"><input type="checkbox" data-op="{k}" data-def="{int(d)}" data-orig="{int(o)}"{" checked" if d else ""}> {escape(t)}{" <span class=orig>original</span>" if o else ""}</label>' for k, t, o, d in OPCIONES)
    def control(k, t, ops, d, o):
        if len(ops) > 4:
            return (f'<label class="lc-fila lc-modo"><span>{escape(t)}</span><select data-sel="{k}" data-def="{d}" data-orig="{o}">'
                    + "".join(f'<option value="{v}"{" selected" if v == d else ""}>{escape(x)}</option>' for v, x in ops) + '</select></label>')
        return (f'<fieldset class="lc-radios" data-sel="{k}" data-def="{d}" data-orig="{o}"><legend>{escape(t)}</legend>'
                + "".join(f'<label class="lc-fila"><input type="radio" name="o-{k}" value="{v}"{" checked" if v == d else ""}> {escape(x)}</label>' for v, x in ops)
                + '</fieldset>')
    sel = "".join(control(*c) for c in SELECTORES)
    return (f'<div class="barra-doc"><button type="button" class="ajustes-b" aria-haspopup="dialog" aria-expanded="false" aria-controls="opciones" title="Ajustes de los diagramas">'
            f'<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/></svg>'
            f'<span>Ajustes</span></button></div>'
            f'<div class="modal-lectura" id="opciones" hidden><div class="ml-caja herr-lectura" tabindex="-1" role="dialog" aria-modal="true" aria-labelledby="ml-titulo">'
            f'<header class="ml-cab"><span id="ml-titulo" class="herr-titulo">Ajustes</span><button type="button" class="ml-cerrar" aria-label="Cerrar">✕</button></header>'
            f'<div class="ml-cuerpo">{sel}<p class="ml-grupo">Elementos · <span class="cuantas"></span></p>{cas}'
            f'<div class="ml-acciones"><button type="button" class="lc-tablas" data-todo>Por defecto</button><button type="button" class="lc-tablas" data-original>Como el original</button></div>'
            f'<p class="lc-ayuda">Se recuerda en este navegador, para esta página.</p></div></div></div>')


KIT = Path(__file__).resolve().parents[2] / "plugins/sf/tools/kit_documentos/herramientas.css"
# Reglas del kit de los documentos que se reutilizan: la barra y el modal «Lectura». Los colores del kit se
# toman de los de la página; el fondo blanco del modal pasa al del nodo para el modo oscuro.
REGLAS_KIT = (".barra-doc {", ".report-header .barra-doc", ".herr-titulo {", ".herr-lectura ", ".dc-config:focus-visible", ".modal-lectura", ".ml-")


def css_kit():
    texto = re.sub(r"/\*.*?\*/", "", KIT.read_text(encoding="utf-8"), flags=re.S)
    reglas = [r.strip() + "}" for r in texto.split("}") if r.strip().startswith(REGLAS_KIT)]
    puente = (".modal-lectura,.barra-doc{--primario:var(--acento);--oscuro:var(--tinta);--texto:var(--tinta);--texto-suave:var(--apagado);--borde:var(--regla-f);"
              "--linea:var(--regla);--fondo:var(--papel2);--fondo-suave:var(--papel);--esquinas:10px}")
    propio = (".ml-caja,.ml-cerrar{background:var(--nodo)!important} [data-theme=dark] .modal-lectura{background:rgba(0,0,0,.55)}"
              ".ml-caja{width:min(30rem,100%);font-size:.9rem}.ml-caja .lc-modo select{max-width:62%}"
              ".ml-grupo{margin:1rem 0 .3rem;padding-top:.7rem;border-top:1px solid var(--linea);font:500 .68rem 'Geist Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--texto-suave)}"
              ".lc-radios{border:0;margin:.5rem 0 0;padding:0}.lc-radios legend{padding:0;margin-bottom:.1rem;font-weight:600;font-size:.875rem}"
              ".lc-radios .lc-fila{margin:.15rem 0;min-height:26px}.herr-lectura input[type=radio]{width:1rem;height:1rem;accent-color:var(--primario)}"
              ".ml-acciones{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.6rem}.barra-doc{margin:.2rem 0 .4rem}")
    return puente + "\n" + "\n".join(reglas) + "\n" + propio


def atributos_defecto():
    """Los favoritos ya puestos en <html>: sin la herramienta (o sin JavaScript) la página se ve igual."""
    sin = " ".join(f"sin-{k}" for k, _, _, d in OPCIONES if not d)
    return sin, " ".join(f'data-o-{k}="{d}"' for k, _, _, d, _ in SELECTORES)


FUENTES = "https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&display=swap"

FIGURAS = [
    ("ciclo", "Estados · mapa de fases", "Ciclo de vida de una tarea", "Las fases bajan, o van, por el centro; la vuelta que hace Claude, a un lado; las salidas, al otro. Revertir y Reabrir, que valen desde varios estados, van a notas.", ciclo, CICLO_FICHAS),
    ("arq", "Arquitectura · contención", "Arquitectura de la SF", "Del repositorio fuente al proyecto: RELEASE publica, ACTUALIZAR instala, cola.py escribe la cola y el panel la lee.", arquitectura, ARQ_FICHAS),
    ("seq", "Secuencia", "De la petición al cierre", "Poner en curso y cerrar una tarea: quién habla con quién y qué orden de cola.py cambia su estado. El tiempo baja en las dos versiones; la ancha solo da aire.", secuencia, SEQ_FICHAS),
    ("fases", "Línea de tiempo", "Las fases de la metodología", "De la visión al cierre, con lo que deja cada fase.", fases, FASES_FICHAS),
    ("rel", "Flujo de proceso", "Publicar con RELEASE", "Lo que hace el botón RELEASE del panel, con quién lo hace y dónde se para si algo falla.", proceso, PROC_FICHAS),
    ("pzs", "Mapa de piezas", "Las piezas del plugin sf", "Qué lleva plugins/sf, cómo se usan entre sí y de qué depende.", piezas, PIEZAS_FICHAS),
]


def k(v):
    return f"{v:.1f}".replace(".", ",")


def pagina(herramientas="ajustes"):
    figs, medidas = [], []
    for fid, tipo, tit, subt, fn, fichas in FIGURAS:
        f, (h, v) = figura(fid, tipo, tit, subt, fn, fichas)
        figs.append(f)
        medidas.append((tit, len(f), h.n_nodos, h.n_flechas, v.n_nodos, v.n_flechas))
    reglas = "".join(f"<li><b>{t}.</b> {x}</li>" for t, x in REGLAS)
    c_reglas = sum(len(t) + len(x) for t, x in REGLAS)
    # La skill propia: estas reglas redactadas (unos 4k), una guía corta por tipo (6 × 1,2k) y el uso del generador (1,5k).
    c_skill = 4000 + 6 * 1200 + 1500
    media = sum(m[1] for m in medidas) / len(medidas)
    nav = "".join(f'<a href="#{f[0]}">{escape(f[2])}</a>' for f in FIGURAS) + '<a href="#reglas">Reglas</a>'
    sin, dato = atributos_defecto()
    return f"""<!doctype html>
<html lang="es" data-theme="light" data-herramientas="{herramientas}" class="{sin}" {dato}><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Síntesis de diagramas SF</title>
<link rel="stylesheet" href="{FUENTES}">
<style>{CSS}
{css_temas()}
{css_kit()}</style></head><body><main>
<div class="cabecera"><div><p class="ceja-p">Página de pruebas · tarea 308</p><h1>Síntesis de diagramas de la SF</h1>{panel_opciones() if "ajustes" in herramientas.split() else ""}</div><button type="button" id="tema" class="tema" aria-pressed="false">Modo oscuro</button></div>
<p class="intro">Nuestra síntesis con la estética de diagram-design, en seis tipos de diagrama con contenido real de la SF. Cada figura lleva su versión vertical, de partida, y la horizontal, y elige una según su propio ancho: estrecha la ventana para ver el cambio. Pulsa cualquier elemento para abrir su ficha. Al final, las reglas usadas, que serían la semilla de la skill propia, y lo que costaría cargarla.</p>
<nav>{nav}</nav>
{"".join(figs)}
<section class="reglas" id="reglas"><h2>Reglas usadas</h2>
<ol class="reglas">{reglas}</ol>
<p class="tokens"><b>Lo que costaría cargar la skill.</b> Estas reglas ocupan {k(c_reglas / 1000)}k caracteres. Redactadas como skill, con una guía corta por tipo de diagrama (unos 1,2k cada una) y el uso del generador, rondarían los {k(c_skill / 1000)}k caracteres: unos {k(c_skill / 3.5 / 1000)}k tokens a 3,5 caracteres por token. El CSS y el script van en el generador y no se cargan. Un diagrama hecho así, con sus dos versiones y sus fichas, ocupa de media {k(media / 1000)}k caracteres (unos {k(media / 3.5 / 1000)}k tokens). Para comparar: diagram-design pide unos 17,6k tokens para un diagrama de estados.</p>
</section>
</main><script>{JS}</script></body></html>""", medidas


def main():
    salida = Path(__file__).with_name("sintesis-sf.html")
    import argparse
    ap = argparse.ArgumentParser(description="Genera la página de síntesis de diagramas.")
    ap.add_argument("--herramientas", default="ajustes", help="«ajustes» incluye el panel de ajustes del lector; «ninguna», no")
    html, medidas = pagina(ap.parse_args().herramientas)
    salida.write_text(html, encoding="utf-8")
    for m in medidas:
        print(m)
    print(salida, len(html))


if __name__ == "__main__":
    main()
