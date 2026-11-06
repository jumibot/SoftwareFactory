"""Genera diagramas-flujo.html: el ciclo de vida de una tarea dibujado por cada skill
candidata a su manera, lo que más puede hacer cada una y lo que pesa en tokens (tarea 308).

Uso: python -I -X utf8 docs/_pruebas/diagramas_flujo.py
"""
import json
from html import escape
from pathlib import Path


def ancho(t, fs, k=0.62, extra=0.0):
    return len(t) * (fs * k + extra)


def etiqueta(x, y, t, fs=8, k=0.62, extra=0.48, ancla="middle", clase="lbl", mascara="mask", pad=4):
    """Texto con su máscara opaca detrás (y es la línea base)."""
    w = ancho(t, fs, k, extra) + pad * 2
    rx = {"middle": x - w / 2, "start": x - pad, "end": x - w + pad}[ancla]
    return (f'<rect class="{mascara}" x="{rx:.1f}" y="{y - fs - 1:.1f}" width="{w:.1f}" height="{fs + 5:.1f}" rx="2"/>'
            f'<text class="{clase}" x="{x}" y="{y}" text-anchor="{ancla}">{escape(t)}</text>')


def flecha_defs(pref, clases):
    return "".join(
        f'<marker id="{pref}-{c}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        f'orient="auto"><path d="M0,1 L10,5 L0,9 z" class="ah-{c}"/></marker>' for c in clases)


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


# ───────────────────────── diagram-design ─────────────────────────

def dd_nodo(x, y, w, h, tag, nombre, sub, clase="phase", nid=None, g="fases", tk=5.2):
    a = f' class="dd-n" data-n="{nid}" data-g="{g}"' if nid else ""
    return (f'<g{a}><rect class="{clase}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
            f'<rect class="tagbox" x="{x + 10}" y="{y + 10}" width="{len(tag) * tk + 10:.0f}" height="{12 if tk < 6 else 14}" rx="2"/>'
            f'<text class="tag" x="{x + 15}" y="{y + (19 if tk < 6 else 20.5)}">{tag}</text>'
            f'<text class="nn" x="{x + w / 2}" y="{y + h / 2 + 6}" text-anchor="middle">{escape(nombre)}</text>'
            f'<text class="sl" x="{x + w / 2}" y="{y + h / 2 + 21}" text-anchor="middle">{escape(sub)}</text></g>')


def dd_kit(p, i):
    """Piezas del mapa de fases. Con i, cada pieza lleva su grupo y sus extremos, para plegar y resaltar."""
    def e(d, de, a, g, k=""):
        mk = "a" if k == "acc" else "m"
        at = f' data-de="{de}" data-a="{a}" data-g="{g}"' if i else ""
        return f'<path class="fl {k}" d="{d}"{at} marker-end="url(#{p}-{mk})"/>'

    def gr(g, s):
        return f'<g data-g="{g}">{s}</g>' if i else s

    def n(nid):
        return nid if i else None
    return e, gr, n


def dd_defs(p):
    return (f'<defs><pattern id="{p}-dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".9" class="dot"/></pattern>'
            + flecha_defs(p, ["m", "a"]) + '</defs>')


def dd_ciclo(p="dd", i=False):
    e, gr, n = dd_kit(p, i)
    o = ['<svg viewBox="0 0 1000 540" role="img" aria-label="Mapa de fases: Pendientes, En curso, En observación y Cerradas en un carril; '
         'arriba, las vueltas que hace Claude; abajo, las salidas Descartada y Fuera de la cola.">',
         dd_defs(p),
         f'<rect width="1000" height="540" class="paper"/><rect width="1000" height="540" fill="url(#{p}-dots)" opacity=".55"/>',
         '<rect class="band" x="24" y="40" width="952" height="150" rx="8"/><rect class="band" x="24" y="388" width="952" height="130" rx="8"/>',
         '<text class="eb" x="40" y="60">VUELTAS · LAS HACE CLAUDE</text><text class="eb" x="40" y="208">FASES DEL PANEL</text>'
         '<text class="eb" x="40" y="406">SALIDAS</text>',
         e("M26 252 H70", "ini", "pend", "fases"),
         e("M220 244 H310", "pend", "curso", "fases"),
         e(codo((360, 216), (360, 170), (165, 170), (165, 216)), "curso", "pend", "vueltas", "dash"),
         e("M460 244 H550", "curso", "obs", "fases"),
         e("M700 244 H790", "obs", "cerr", "fases", "acc"),
         e("M790 268 H700", "cerr", "obs", "fases"),
         e(codo((880, 216), (880, 110), (410, 110), (410, 216)), "cerr", "curso", "vueltas", "dash"),
         gr("vueltas", '<path class="fl dash" d="M640 216 V110"' + (' data-de="obs" data-a="curso"' if i else '') + '/><circle class="ink" cx="640" cy="110" r="3"/>'),
         e(codo((430, 288), (430, 340), (850, 340), (850, 288)), "curso", "cerr", "fases"),
         e("M370 288 V416", "curso", "desc", "salidas"),
         e("M145 288 V416", "pend", "fuera", "salidas"),
         etiqueta(46, 238, "NUEVA"), etiqueta(265, 235, "ACTIVAR RAMA"), gr("vueltas", etiqueta(262, 161, "SIN TRABAJO")),
         etiqueta(505, 235, "A OBSERVACIÓN"), etiqueta(745, 235, "CERRAR", clase="lbl acc-t"),
         etiqueta(745, 285, "A OBSERVACIÓN"), gr("vueltas", etiqueta(520, 101, "REABRIR")), etiqueta(638, 331, "CERRAR"),
         gr("salidas", etiqueta(381, 365, "DESCARTAR", ancla="start") + etiqueta(156, 359, "ELIMINAR", ancla="start")),
         '<circle class="ink" cx="20" cy="252" r="6"/>',
         dd_nodo(70, 216, 150, 72, "FASE", "Pendientes", "sin rama", nid=n("pend")),
         dd_nodo(310, 216, 150, 72, "FASE", "En curso", "rama · subagente", nid=n("curso")),
         dd_nodo(550, 216, 150, 72, "FASE", "En observación", "en develop", nid=n("obs")),
         dd_nodo(790, 216, 150, 72, "FASE", "Cerradas", "en develop", "phase focal", nid=n("cerr")),
         '<circle class="ring-a" cx="922" cy="234" r="7"/><circle class="fill-a" cx="922" cy="234" r="4"/>',
         dd_nodo(70, 416, 150, 72, "SALIDA", "Fuera de la cola", "eliminada", "terminal", nid=n("fuera"), g="salidas"),
         dd_nodo(310, 416, 150, 72, "SALIDA", "Descartada", "sin botones", "terminal", nid=n("desc"), g="salidas"),
         gr("vueltas", '<text class="call" x="560" y="76">Claude reabre desde En observación, Cerradas o Descartada.</text>'),
         gr("salidas", '<text class="call" x="520" y="448">Revertir devuelve En observación y Cerradas a Pendientes</text>'
            '<text class="call" x="520" y="468">o las saca de la cola: va en el diagrama de detalle.</text>')]
    if i:
        o.append('<text class="plegado" data-plegado="vueltas" x="40" y="128">Vueltas plegadas: Sin trabajo y Reabrir.</text>'
                 '<text class="plegado" data-plegado="salidas" x="40" y="462">Dos salidas plegadas: Descartada y Fuera de la cola.</text>')
    o.append('</svg>')
    return "".join(o)


def dd_ciclo_v(p="ddv", i=False):
    """La misma máquina en vertical: las fases bajan por el centro; vueltas a la izquierda y salidas a la derecha.
    Escala tipográfica propia (clase v) para que a 375 de ancho los nombres no bajen de unos 9 px."""
    e, gr, n = dd_kit(p, i)

    def lab(x, y, t, **kw):
        return etiqueta(x, y, t, fs=10, **kw)
    o = ['<svg class="v" viewBox="0 0 560 640" role="img" aria-label="Mapa de fases en vertical: las fases bajan por el centro; a la izquierda, las vueltas que hace Claude; a la derecha, las salidas.">',
         dd_defs(p),
         f'<rect width="560" height="640" class="paper"/><rect width="560" height="640" fill="url(#{p}-dots)" opacity=".55"/>',
         '<rect class="band" x="12" y="40" width="132" height="588" rx="8"/><rect class="band" x="388" y="40" width="164" height="588" rx="8"/>',
         '<text class="eb" x="24" y="60">VUELTAS</text><text class="eb" x="400" y="60">SALIDAS</text><text class="eb" x="160" y="60">FASES</text>',
         '<circle class="ink" cx="250" cy="24" r="6"/>',
         e("M250 30 V70", "ini", "pend", "fases"),
         e("M235 134 V220", "pend", "curso", "fases"),
         e(codo((175, 240), (100, 240), (100, 110), (175, 110)), "curso", "pend", "vueltas", "dash"),
         e("M250 284 V370", "curso", "obs", "fases"),
         e("M235 434 V520", "obs", "cerr", "fases", "acc"),
         e("M265 520 V434", "cerr", "obs", "fases"),
         e(codo((325, 270), (370, 270), (370, 552), (325, 552)), "curso", "cerr", "fases"),
         e("M325 236 H400", "curso", "desc", "salidas"),
         e("M325 94 H400", "pend", "fuera", "salidas"),
         e(codo((175, 552), (60, 552), (60, 264), (175, 264)), "cerr", "curso", "vueltas", "dash"),
         gr("vueltas", '<path class="fl dash" d="M175 402 H60"' + (' data-de="obs" data-a="curso"' if i else '') + '/><circle class="ink" cx="60" cy="402" r="3"/>'),
         lab(262, 52, "NUEVA", ancla="start"), lab(227, 182, "ACTIVAR RAMA", ancla="end"),
         gr("vueltas", lab(92, 180, "SIN", ancla="end") + lab(92, 196, "TRABAJO", ancla="end")),
         lab(258, 332, "A OBSERVACIÓN", ancla="start"), lab(227, 482, "CERRAR", ancla="end", clase="lbl acc-t"),
         lab(273, 482, "A OBSERVACIÓN", ancla="start"), lab(376, 422, "CERRAR", ancla="start"),
         gr("salidas", lab(362, 225, "DESCARTAR") + lab(362, 84, "ELIMINAR")),
         gr("vueltas", lab(70, 482, "REABRIR", ancla="start")),
         dd_nodo(175, 70, 150, 64, "FASE", "Pendientes", "sin rama", nid=n("pend"), tk=5.9),
         dd_nodo(175, 220, 150, 64, "FASE", "En curso", "rama · subagente", nid=n("curso"), tk=5.9),
         dd_nodo(175, 370, 150, 64, "FASE", "En observación", "en develop", nid=n("obs"), tk=5.9),
         dd_nodo(175, 520, 150, 64, "FASE", "Cerradas", "en develop", "phase focal", nid=n("cerr"), tk=5.9),
         '<circle class="ring-a" cx="309" cy="536" r="6"/><circle class="fill-a" cx="309" cy="536" r="3.5"/>',
         dd_nodo(400, 70, 148, 64, "SALIDA", "Fuera de la cola", "eliminada", "terminal", nid=n("fuera"), g="salidas", tk=5.9),
         dd_nodo(400, 204, 148, 64, "SALIDA", "Descartada", "sin botones", "terminal", nid=n("desc"), g="salidas", tk=5.9),
         gr("vueltas", '<text class="call" x="22" y="600">Claude también</text><text class="call" x="22" y="618">reabre Descartada.</text>'),
         gr("salidas", '<text class="call" x="400" y="470">Revertir devuelve</text><text class="call" x="400" y="488">En observación y</text>'
            '<text class="call" x="400" y="506">Cerradas a Pendientes</text><text class="call" x="400" y="524">o las saca de la cola:</text>'
            '<text class="call" x="400" y="542">va en el detalle.</text>')]
    if i:
        o.append('<text class="plegado" data-plegado="vueltas" x="22" y="300">Vueltas</text><text class="plegado" data-plegado="vueltas" x="22" y="318">plegadas.</text>'
                 '<text class="plegado" data-plegado="salidas" x="400" y="120">Dos salidas</text><text class="plegado" data-plegado="salidas" x="400" y="138">plegadas.</text>')
    o.append('</svg>')
    return "".join(o)


def dd_arquitectura():
    o = ['<svg viewBox="0 0 1000 340" role="img" aria-label="Arquitectura: el repositorio fuente publica el plugin sf, que se instala en el equipo; '
         'cola.py escribe la cola del proyecto y el panel la muestra.">',
         '<defs><pattern id="dd-dots2" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".9" class="dot"/></pattern>',
         flecha_defs("dd2", ["m", "a"]), '</defs>',
         '<rect width="1000" height="340" class="paper"/><rect width="1000" height="340" fill="url(#dd-dots2)" opacity=".55"/>',
         '<rect class="zone" x="24" y="30" width="300" height="290" rx="8"/><rect class="zone" x="360" y="30" width="300" height="290" rx="8"/>'
         '<rect class="zone" x="696" y="30" width="280" height="290" rx="8"/>',
         '<text class="eb" x="40" y="52">FUENTE · REPOSITORIO</text><text class="eb" x="376" y="52">EQUIPO · ~/.CLAUDE</text>'
         '<text class="eb" x="712" y="52">PROYECTO CONSUMIDOR</text>',
         '<line class="fl acc" x1="300" y1="126" x2="384" y2="126" marker-end="url(#dd2-a)"/>',
         '<line class="fl" x1="510" y1="162" x2="510" y2="220" marker-end="url(#dd2-m)"/>',
         f'<path class="fl" d="{codo((636, 256), (678, 256), (678, 126), (720, 126))}" marker-end="url(#dd2-m)"/>',
         '<line class="fl dash" x1="836" y1="220" x2="836" y2="162" marker-end="url(#dd2-m)"/>',
         etiqueta(342, 117, "PUBLICA"), etiqueta(518, 195, "INSTALA", ancla="start"),
         etiqueta(686, 195, "ESCRIBE", ancla="start"), etiqueta(844, 195, "LEE", ancla="start"),
         dd_nodo(48, 90, 252, 72, "CÓDIGO", "plugins/sf", "skills · mod · cola.py"),
         dd_nodo(48, 220, 252, 72, "DOCS", "docs/", "brain de desarrollo"),
         dd_nodo(384, 90, 252, 72, "PLUGIN", "Plugin sf", "versión publicada", "phase focal"),
         dd_nodo(384, 220, 252, 72, "CLI", "cola.py", "~/.claude/sf/cola.py"),
         dd_nodo(720, 90, 232, 72, "ESTADO", "peticiones.json", ".sf/peticiones.json"),
         dd_nodo(720, 220, 232, 72, "MOD", "Panel de la SF", "muestra la cola"),
         '</svg>']
    return "".join(o)


def dd_secuencia():
    xs = {"Propietario": 130, "Principal": 390, "Subagente": 650, "cola.py": 880}
    o = ['<svg viewBox="0 0 1000 410" role="img" aria-label="Secuencia: el propietario pide, el principal anota en la cola, '
         'encarga al subagente, recibe su informe, pide el OK y cierra.">',
         '<defs>', flecha_defs("dd3", ["m", "a"]), '</defs>',
         '<rect width="1000" height="410" class="paper"/>']
    for n, x in xs.items():
        o.append(f'<line class="life" x1="{x}" y1="76" x2="{x}" y2="392"/>'
                 f'<rect class="phase" x="{x - 70}" y="36" width="140" height="40" rx="6"/>'
                 f'<text class="nn" x="{x}" y="61" text-anchor="middle">{n}</text>')
    o.append('<rect class="act" x="384" y="104" width="12" height="268" rx="2"/>')
    msgs = [(130, 384, 120, "PIDE", ""), (396, 880, 160, "ANOTA", ""), (396, 650, 200, "ENCARGA", ""),
            (650, 396, 240, "INFORME", "dash"), (384, 130, 280, "¿OK?", ""), (130, 384, 320, "OK", "acc"),
            (396, 880, 360, "CIERRA", "")]
    for x1, x2, y, t, k in msgs:
        mk = "dd3-a" if k == "acc" else "dd3-m"
        o.append(f'<line class="fl {k}" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" marker-end="url(#{mk})"/>')
        o.append(etiqueta((x1 + x2) / 2, y - 7, t, clase="lbl acc-t" if k == "acc" else "lbl"))
    o.append('</svg>')
    return "".join(o)


def dd_fases():
    fases = ["Visión", "Especificación e interfaz", "Definición técnica", "Devslices", "Preparación",
             "Desarrollo y verificación", "Cierre"]
    o = ['<svg viewBox="0 0 1000 200" role="img" aria-label="Línea de fases de la metodología, de la visión al cierre.">',
         '<rect width="1000" height="200" class="paper"/>', '<line class="rule" x1="70" y1="100" x2="930" y2="100"/>']
    for i, f in enumerate(fases):
        x = 70 + i * (860 / 6)
        acc = i == 5
        arriba = i % 2 == 0
        o.append(f'<circle class="{"fill-a" if acc else "ink"}" cx="{x:.0f}" cy="100" r="{6 if acc else 4}"/>')
        o.append(f'<line class="tick" x1="{x:.0f}" y1="{88 if arriba else 112}" x2="{x:.0f}" y2="{76 if arriba else 124}"/>')
        o.append(f'<text class="eb" x="{x:.0f}" y="{54 if arriba else 144}" text-anchor="middle">FASE {i + 1}</text>')
        o.append(f'<text class="nn{" acc-t" if acc else ""}" x="{x:.0f}" y="{70 if arriba else 160}" text-anchor="middle">{escape(f)}</text>')
    o.append('</svg>')
    return "".join(o)


# ───────────────────────── visual-explainer ─────────────────────────

def ve_nodo(nid, x, y, nombre, sub, kind, extra=""):
    return (f'<g class="ve-n {extra}" data-n="{nid}"><rect class="halo" x="{x - 5}" y="{y - 5}" width="190" height="74" rx="9"/>'
            f'<rect class="box" x="{x}" y="{y}" width="180" height="64" rx="5"/>'
            f'<text class="kind" x="{x + 12}" y="{y + 17}">{kind}</text>'
            f'<text class="nm" x="{x + 12}" y="{y + 37}">{escape(nombre)}</text>'
            f'<text class="sb" x="{x + 12}" y="{y + 54}">{escape(sub)}</text></g>')


def ve_ciclo():
    aristas = [("new", "M130 22 V64", ""), ("act", "M220 86 H310", ""), ("elim", "M130 128 V264", ""), ("sin", "M310 110 H220", "dash"),
               ("obs", "M490 86 H580", ""), ("cer", "M650 128 V264", ""), ("vob", "M690 264 V128", ""),
               ("cdir", codo((460, 128), (460, 226), (610, 226), (610, 264)), ""), ("desc", "M400 128 V264", ""),
               ("rdesc", "M350 264 V128", "dash"),
               ("rdev", codo((670, 44), (670, 24), (430, 24), (430, 64)), "dash"),
               ("rev", codo((670, 348), (670, 378), (20, 378), (20, 104), (40, 104)), ""),
               ("relim", "M130 378 V328", "")]
    o = ['<svg viewBox="0 0 830 400" role="img" aria-label="Máquina de estados de una tarea, con un recorrido paso a paso de ocho eventos.">',
         '<defs><pattern id="ve-grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" class="gridl"/></pattern>',
         '<marker id="ve-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M0,1 L10,5 L0,9 z" class="ah"/></marker>',
         '<marker id="ve-ah-on" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4.5" markerHeight="4.5" orient="auto"><path d="M0,1 L10,5 L0,9 z" class="ah-on"/></marker></defs>',
         '<rect width="830" height="400" fill="url(#ve-grid)"/>',
         '<rect class="bnd" x="564" y="44" width="212" height="304" rx="4"/><text class="bnd-t" x="572" y="58">EN DEVELOP</text>']
    for aid, d, k in aristas:
        o.append(f'<path class="ve-e {k}" data-e="{aid}" d="{d}" marker-end="url(#ve-ah)"/>')
    o.append('<circle class="jn" cx="130" cy="378" r="3.5"/>')
    labs = [(146, 40, "nueva petición", "start"), (265, 78, "Activar rama", "middle"), (265, 126, "sin trabajo", "middle"),
            (535, 76, "A observación", "middle"), (642, 170, "Cerrar", "end"), (698, 200, "A observación", "start"),
            (535, 218, "Cerrar", "middle"), (406, 252, "Descartar", "start"), (342, 238, "Reabrir", "end"),
            (550, 16, "Reabrir, con Claude", "middle"), (400, 370, "Revertir", "middle"), (138, 360, "eliminar", "start"),
            (26, 236, "a Pendientes", "start"), (138, 200, "Eliminar", "start")]
    for x, y, t, a in labs:
        o.append(etiqueta(x, y, t, fs=10.5, k=0.55, extra=0, ancla=a, clase="ve-l", mascara="halo-t", pad=3))
    o += [ve_nodo("pend", 40, 64, "Pendientes", "sin rama", "ESTADO"),
          ve_nodo("curso", 310, 64, "En curso", "rama · subagente", "ESTADO"),
          ve_nodo("obs", 580, 64, "En observación", "squash en develop", "ESTADO"),
          ve_nodo("fuera", 40, 264, "Fuera de la cola", "eliminada", "EFECTO", "gone"),
          ve_nodo("desc", 310, 264, "Descartada", "nada en develop", "ESTADO", "gone"),
          ve_nodo("cerr", 580, 264, "Cerradas", "en develop", "ESTADO")]
    for x, y, t in [(130, 50, "1"), (265, 98, "2·6"), (535, 98, "3"), (650, 236, "4"), (230, 378, "5"), (400, 150, "7"), (350, 210, "8")]:
        o.append(f'<g class="co" data-s="{t.replace("·", " ")}" transform="translate({x} {y})"><circle r="10"/><text y="3.5">{t}</text></g>')
    o.append('</svg>')
    return "".join(o)


VE_PASOS = [
    ("", "", "El ciclo completo. Pulsa ▶ para recorrerlo evento a evento."),
    ("new", "pend", "Llega una petición: entra en Pendientes, sin rama."),
    ("act", "curso", "Activar rama: pasa a En curso, porque ahora tiene rama y subagente."),
    ("obs", "obs", "A observación: el squash entra en develop y la rama ya no hace falta."),
    ("cer", "cerr", "Cerrar: pasa a Cerradas; el trabajo sigue en develop."),
    ("rev", "pend", "Revertir · a Pendientes: vuelve a Pendientes y su cambio sale de develop."),
    ("act", "curso", "Activar rama: otra vez En curso, con su rama y su subagente."),
    ("desc", "desc", "Descartar: pasa a Descartada; nada llega a develop."),
    ("rdesc", "curso", "Reabrir, con Claude: vuelve a En curso."),
]


def ve_arquitectura():
    def l(x, y, t, a="middle"):
        return etiqueta(x, y, t, fs=10.5, k=0.55, extra=0, ancla=a, clase="ve-l", mascara="halo-t", pad=3)
    return ('<svg viewBox="0 0 760 300" role="img" aria-label="El principal ordena a cola.py, que escribe la cola y hace commits en develop; el panel muestra la cola.">'
            '<defs><pattern id="ve-grid2" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" class="gridl"/></pattern>'
            '<marker id="ve-ah2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M0,1 L10,5 L0,9 z" class="ah"/></marker></defs>'
            '<rect width="760" height="300" fill="url(#ve-grid2)"/>'
            '<rect class="bnd" x="16" y="20" width="728" height="262" rx="4"/><text class="bnd-t" x="26" y="36">EQUIPO DEL PROPIETARIO</text>'
            '<path class="ve-e" d="M200 90 H300" marker-end="url(#ve-ah2)"/>'
            '<path class="ve-e" d="M480 90 H560" marker-end="url(#ve-ah2)"/>'
            '<path class="ve-e" d="M390 122 V198" marker-end="url(#ve-ah2)"/>'
            '<path class="ve-e dash" d="M650 200 V126" marker-end="url(#ve-ah2)"/>'
            + l(250, 80, "ordena") + l(520, 80, "escribe") + l(398, 166, "commit", "start") + l(658, 172, "muestra", "start")
            + '<g class="dots" aria-hidden="true"><circle r="4" class="tok"/><circle r="4" class="tok t2"/><circle r="4" class="tok t3"/></g>'
            '<g class="ve-n"><rect class="box" x="40" y="58" width="160" height="64" rx="5"/><text class="kind" x="52" y="75">AGENTE</text>'
            '<text class="nm" x="52" y="95">Principal</text><text class="sb" x="52" y="112">habla con el propietario</text></g>'
            '<g class="ve-n is-key"><rect class="halo" x="295" y="53" width="190" height="74" rx="9"/><rect class="box" x="300" y="58" width="180" height="64" rx="5"/>'
            '<text class="kind" x="312" y="75">CLI</text><text class="nm" x="312" y="95">cola.py</text><text class="sb" x="312" y="112">único que escribe</text></g>'
            '<g class="ve-n"><path class="cyl" d="M560 66 v48 a90 10 0 0 0 180 0 v-48"/><ellipse class="cyl" cx="650" cy="66" rx="90" ry="10"/>'
            '<text class="nm" x="650" y="98" text-anchor="middle">peticiones.json</text><text class="sb" x="650" y="114" text-anchor="middle">.sf/</text></g>'
            '<g class="ve-n"><path class="cyl" d="M300 208 v44 a90 10 0 0 0 180 0 v-44"/><ellipse class="cyl" cx="390" cy="208" rx="90" ry="10"/>'
            '<text class="nm" x="390" y="240" text-anchor="middle">git · develop</text><text class="sb" x="390" y="256" text-anchor="middle">decisiones y cierres</text></g>'
            '<g class="ve-n"><rect class="box" x="560" y="200" width="180" height="64" rx="5"/><text class="kind" x="572" y="217">MOD</text>'
            '<text class="nm" x="572" y="237">Panel</text><text class="sb" x="572" y="254">muestra la cola</text></g>'
            '</svg>')


def ve_mini(clave, tramos, etiqueta_aria):
    pos = {"P": 34, "C": 112, "O": 190, "X": 268}
    nombres = {"P": "Pend.", "C": "Curso", "O": "Obs.", "X": "Cerr."}
    o = [f'<svg viewBox="0 0 302 96" role="img" aria-label="{escape(etiqueta_aria)}" class="m-{clave}">',
         f'<defs><marker id="ve-ahm-{clave}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4.5" markerHeight="4.5" orient="auto"><path d="M0,1 L10,5 L0,9 z" class="mini-ah"/></marker></defs>']
    for a, b in tramos:
        xa, xb = pos[a], pos[b]
        if xb - xa == 78:
            o.append(f'<path class="mini-e" d="M{xa + 30} 40 H{xb - 30}" marker-end="url(#ve-ahm-{clave})"/>')
        elif xb > xa:
            o.append(f'<path class="mini-e" d="{codo((xa, 22), (xa, 8), (xb, 8), (xb, 20), r=6)}" marker-end="url(#ve-ahm-{clave})"/>')
        else:
            o.append(f'<path class="mini-e" d="{codo((xa, 58), (xa, 84), (xb, 84), (xb, 60), r=6)}" marker-end="url(#ve-ahm-{clave})"/>')
    for k, x in pos.items():
        on = any(k in t for t in tramos)
        o.append(f'<rect class="mini-n{" on" if on else ""}" x="{x - 30}" y="22" width="60" height="36" rx="4"/>'
                 f'<text class="mini-t" x="{x}" y="45" text-anchor="middle">{nombres[k]}</text>')
    o.append('</svg>')
    return "".join(o)


# ───────────────────────── process-flow-diagram ─────────────────────────

def cc_paso(n, x, y, nombre, l1, l2, tipo, actor):
    return (f'<text class="actor" x="{x + 80}" y="{y - 10}" text-anchor="middle">{actor}</text>'
            f'<rect class="st {tipo}" x="{x}" y="{y}" width="160" height="80" rx="8"/>'
            f'<circle class="badge {tipo}" cx="{x}" cy="{y}" r="12"/><text class="bn" x="{x}" y="{y + 4}" text-anchor="middle">{n}</text>'
            f'<text class="t" x="{x + 80}" y="{y + 32}" text-anchor="middle">{escape(nombre)}</text>'
            f'<text class="d" x="{x + 80}" y="{y + 50}" text-anchor="middle">{escape(l1)}</text>'
            f'<text class="d" x="{x + 80}" y="{y + 64}" text-anchor="middle">{escape(l2)}</text>')


CC_DEFS = ('<marker id="{p}-s" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#64748b"/></marker>'
           '<marker id="{p}-r" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#fb7185"/></marker>'
           '<marker id="{p}-c" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#22d3ee"/></marker>')


def cc_ciclo():
    a, r = 'marker-end="url(#cc-s)"', 'marker-end="url(#cc-r)"'
    o = ['<svg viewBox="0 0 1180 540" role="img" aria-label="Flujo de proceso de una tarea, de la nueva petición a Cerradas, con las excepciones debajo y la vuelta de Reabrir por arriba.">',
         '<defs><pattern id="cc-grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="rgba(148,163,184,.07)"/></pattern>',
         CC_DEFS.format(p="cc"), '</defs>',
         '<rect width="1180" height="540" fill="#020617"/><rect width="1180" height="540" fill="url(#cc-grid)"/>',
         '<rect x="30" y="20" width="1120" height="56" rx="8" fill="rgba(30,41,59,.2)" stroke="#64748b" stroke-dasharray="6,4"/>',
         '<text class="actor" x="50" y="44">PRERREQUISITOS</text>',
         '<text class="d" x="50" y="62">proyecto incorporado a la SF · cola en .sf/peticiones.json · panel de la SF abierto</text>',
         f'<path d="{codo((1070, 200), (1070, 108), (575, 108), (575, 168))}" fill="none" stroke="#22d3ee" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#cc-c)"/>',
         '<text x="790" y="101" class="lc" text-anchor="middle">↻ Reabrir, con Claude</text>',
         f'<line x1="150" y1="220" x2="208" y2="220" class="ln" {a}/>', '<text class="la" x="180" y="212" text-anchor="middle">cola</text>',
         f'<line x1="370" y1="220" x2="428" y2="220" class="ln" {a}/>', '<text class="la" x="399" y="212" text-anchor="middle">Activar rama</text>',
         f'<line x1="590" y1="220" x2="636" y2="220" class="ln" {a}/>', '<text class="la" x="613" y="212" text-anchor="middle">prueba</text>',
         f'<line x1="724" y1="220" x2="778" y2="220" class="ln" {a}/>', '<text class="la" x="751" y="212" text-anchor="middle">observar</text>',
         f'<line x1="940" y1="220" x2="998" y2="220" class="ln" {a}/>', '<text class="la" x="969" y="212" text-anchor="middle">Cerrar</text>',
         f'<path d="{codo((680, 176), (680, 146), (1030, 146), (1030, 200))}" class="ln" {a}/>',
         '<text class="la" x="855" y="139" text-anchor="middle">sí · Cerrar sin observar</text>',
         f'<path d="{codo((480, 260), (480, 300), (340, 300), (340, 262))}" class="ln" stroke-dasharray="6,3" {a}/>',
         '<text class="la" x="410" y="316" text-anchor="middle">sin trabajo → Pendientes</text>',
         f'<path d="M680 264 V378" class="lr" {r}/>', '<text class="lx" x="690" y="330">no · Descartar</text>',
         f'<path d="{codo((240, 260), (240, 400), (172, 400))}" class="lr" {r}/>',
         '<text class="lx" x="248" y="352">Eliminar</text>',
         f'<path d="{codo((860, 260), (860, 490), (100, 490), (100, 422))}" class="lr" {r}/>',
         f'<path d="{codo((1070, 240), (1070, 490), (860, 490))}" class="lr"/>',
         f'<path d="M300 490 V262" class="lr" {r}/>',
         '<text class="lx" x="580" y="482" text-anchor="middle">Revertir · eliminar o a Pendientes</text>',
         '<text class="lx" x="308" y="444">a Pendientes</text>',
         '<rect x="30" y="200" width="120" height="40" rx="20" fill="rgba(8,51,68,.4)" stroke="#22d3ee" stroke-width="2"/>',
         '<text class="t" x="90" y="224" text-anchor="middle">Nueva petición</text>',
         cc_paso(1, 210, 180, "Pendientes", "en la cola", "sin rama", "manual", "PROPIETARIO"),
         cc_paso(2, 430, 180, "En curso", "rama + subagente", "trabaja la tarea", "auto", "SUBAGENTE"),
         '<text class="actor" x="668" y="182" text-anchor="end">PROPIETARIO</text>',
         '<rect x="650" y="190" width="60" height="60" rx="4" transform="rotate(45 680 220)" fill="rgba(136,19,55,.4)" stroke="#fb7185" stroke-width="1.5"/>',
         '<text class="t" x="680" y="224" text-anchor="middle">¿Sigue?</text>',
         cc_paso(3, 780, 180, "En observación", "squash en develop", "sin rama", "integ", "DEVELOP"),
         '<rect x="1000" y="200" width="140" height="40" rx="20" fill="rgba(8,51,68,.4)" stroke="#22d3ee" stroke-width="2"/>',
         '<text class="t" x="1070" y="224" text-anchor="middle">Cerradas</text>',
         '<rect x="610" y="380" width="140" height="60" rx="8" fill="rgba(136,19,55,.4)" stroke="#fb7185" stroke-width="1.5"/>',
         '<text class="t" x="680" y="406" text-anchor="middle">Descartada</text><text class="d" x="680" y="424" text-anchor="middle">Claude puede reabrirla</text>',
         '<rect x="30" y="380" width="140" height="40" rx="20" fill="rgba(136,19,55,.25)" stroke="#fb7185" stroke-width="1.5"/>',
         '<text class="t" x="100" y="404" text-anchor="middle">Fuera de la cola</text>',
         '</svg>']
    return "".join(o)


def cc_bucle():
    a = 'marker-end="url(#cc2-s)"'
    return ('<svg viewBox="0 0 1060 320" role="img" aria-label="Bucle de mejora continua: detectar, anotar, proponer, aprobar y aplicar, y vuelta a empezar.">'
            '<defs>' + CC_DEFS.format(p="cc2") + '</defs>'
            '<rect width="1060" height="320" fill="#020617"/>'
            f'<path d="{codo((990, 140), (1020, 140), (1020, 50), (80, 50), (80, 98))}" fill="none" stroke="#22d3ee" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#cc2-c)"/>'
            '<text class="lc" x="570" y="43" text-anchor="middle">↻ siguiente mejora</text>'
            f'<line x1="210" y1="140" x2="268" y2="140" class="ln" {a}/><text class="la" x="239" y="132" text-anchor="middle">anota</text>'
            f'<line x1="430" y1="140" x2="488" y2="140" class="ln" {a}/><text class="la" x="459" y="132" text-anchor="middle">prepara</text>'
            f'<line x1="650" y1="140" x2="694" y2="140" class="ln" {a}/>'
            f'<line x1="782" y1="140" x2="828" y2="140" class="ln" {a}/><text class="la" x="805" y="132" text-anchor="middle">sí</text>'
            '<path d="M738 184 V238" class="lr" marker-end="url(#cc2-r)"/><text class="lx" x="748" y="214">no</text>'
            + cc_paso(1, 50, 100, "Detectar mejora", "en el trabajo", "de una sesión", "manual", "CLAUDE")
            + cc_paso(2, 270, 100, "Anotar", "bajo Mejorar la", "Software Factory", "auto", "COLA")
            + cc_paso(3, 490, 100, "Preparar propuesta", "concreta, con", "su porqué", "auto", "CLAUDE")
            + '<text class="actor" x="738" y="92" text-anchor="middle">PROPIETARIO</text>'
            '<rect x="708" y="110" width="60" height="60" rx="4" transform="rotate(45 738 140)" fill="rgba(136,19,55,.4)" stroke="#fb7185" stroke-width="1.5"/>'
            '<text class="t" x="738" y="144" text-anchor="middle">¿OK?</text>'
            + cc_paso(4, 830, 100, "Aplicar y publicar", "en su tarea", "y su rama", "integ", "SF")
            + '<rect x="668" y="240" width="140" height="50" rx="8" fill="rgba(30,41,59,.3)" stroke="#94a3b8" stroke-dasharray="5,3"/>'
            '<text class="t" x="738" y="270" text-anchor="middle">Queda en propuestas</text>'
            '</svg>')


# ───────────────────────── síntesis para la SF ─────────────────────────

def sf_boton(x, y, t, ancla="middle", de=False):
    fs = 10.5
    w = len(t) * fs * 0.56 + 14
    rx = {"middle": x - w / 2, "start": x, "end": x - w}[ancla]
    k = " de" if de else ""
    return (f'<rect class="btn{k}" x="{rx:.1f}" y="{y - 11}" width="{w:.1f}" height="17" rx="5"/>'
            f'<text class="btn-t{k}" x="{rx + w / 2:.1f}" y="{y + 1}" text-anchor="middle">{escape(t)}</text>')


def sf_estado(eid, x, y, nombre, marcas, clase=""):
    return (f'<g class="es {clase}" data-e="{eid}" tabindex="0" role="button" aria-expanded="false" aria-label="{escape(nombre)}: ver su ficha">'
            f'<rect class="es-c" x="{x}" y="{y}" width="180" height="64" rx="10"/>'
            f'<rect class="es-b" x="{x}" y="{y + 10}" width="4" height="44" rx="2"/>'
            f'<text class="es-n" x="{x + 18}" y="{y + 28}">{escape(nombre)}</text>'
            f'<text class="es-m" x="{x + 18}" y="{y + 47}">{marcas}</text></g>')


def sf_ciclo():
    m, r, c = 'marker-end="url(#sf-m)"', 'marker-end="url(#sf-r)"', 'marker-end="url(#sf-c)"'
    o = ['<svg viewBox="0 0 560 530" role="img" aria-label="Ciclo de vida de una tarea en tres carriles: deshacer a la izquierda, las fases en el centro y la salida Descartada a la derecha. Pulsa un estado para ver su ficha.">',
         '<defs>', flecha_defs("sf", ["m", "r", "c"]), '</defs>',
         '<text class="carril" x="24" y="16">DESHACER</text><text class="carril" x="190" y="16">FASES</text><text class="carril" x="440" y="16">SALIDA</text>',
         '<circle class="pt" cx="280" cy="32" r="5"/>', f'<line class="e" x1="280" y1="38" x2="280" y2="60" {m}/>',
         '<text class="nota" x="292" y="40">nueva petición</text>',
         f'<line class="e" x1="260" y1="124" x2="260" y2="190" {m}/>', f'<line class="e cl" x1="300" y1="190" x2="300" y2="124" {c}/>',
         f'<line class="e" x1="280" y1="254" x2="280" y2="320" {m}/>',
         f'<line class="e" x1="260" y1="384" x2="260" y2="450" {m}/>', f'<line class="e" x1="300" y1="450" x2="300" y2="384" {m}/>',
         f'<line class="e de" x1="370" y1="206" x2="440" y2="206" {r}/>', f'<line class="e cl" x1="440" y1="226" x2="370" y2="226" {c}/>',
         f'<path class="e" d="{codo((370, 244), (398, 244), (398, 482), (370, 482))}" {m}/>',
         f'<line class="e de" x1="190" y1="80" x2="58" y2="80" {r}/>',
         '<line class="e de" x1="190" y1="352" x2="150" y2="352"/>',
         f'<path class="e de" d="{codo((190, 490), (150, 490), (150, 296))}"/>',
         f'<path class="e de" d="{codo((150, 296), (150, 112), (190, 112))}" {r}/>',
         f'<path class="e de" d="{codo((150, 296), (50, 296), (50, 88))}" {r}/>',
         '<circle class="jn" cx="150" cy="296" r="4"/><circle class="jn" cx="150" cy="352" r="3"/>',
         '<circle class="fin-a" cx="50" cy="80" r="8"/><circle class="fin" cx="50" cy="80" r="4.5"/>',
         '<text class="nota" x="24" y="50">fuera de la cola</text>',
         sf_boton(252, 160, "Activar rama", "end"), '<text class="cl-t" x="308" y="161">Claude, sin trabajo</text>',
         sf_boton(288, 290, "A observación", "start"),
         sf_boton(252, 420, "Cerrar", "end"), sf_boton(308, 420, "A observación", "start"),
         sf_boton(405, 192, "Descartar", "middle", True), '<text class="cl-t" x="405" y="244" text-anchor="middle">Reabrir</text>',
         sf_boton(406, 300, "Cerrar", "start"),
         sf_boton(124, 70, "Eliminar", "middle", True), sf_boton(140, 420, "Revertir", "end", True),
         sf_boton(140, 200, "a Pendientes", "end", True), sf_boton(97, 284, "eliminar", "middle", True),
         sf_estado("pend", 190, 60, "Pendientes", "rama ✕ · subagente ✕ · develop ✕"),
         sf_estado("curso", 190, 190, "En curso", "rama ✓ · subagente ✓ · develop ✕", "foco"),
         sf_estado("obs", 190, 320, "En observación", "rama ✕ · subagente ✕ · develop ✓"),
         sf_estado("cerr", 190, 450, "Cerradas", "rama ✕ · subagente ✕ · develop ✓", "hecho"),
         '<g class="es salida" data-e="desc" tabindex="0" role="button" aria-expanded="false" aria-label="Descartada: ver su ficha">'
         '<rect class="es-c" x="440" y="190" width="112" height="64" rx="10"/><text class="es-n" x="452" y="218">Descartada</text>'
         '<text class="es-m" x="452" y="237">sin botones</text></g>',
         '<text class="nota" x="412" y="400">Claude reabre también</text><text class="nota" x="412" y="416">En observación</text>'
         '<text class="nota" x="412" y="432">y Cerradas.</text>',
         '</svg>']
    return "".join(o)


SF_FICHAS = {
    "pend": ("Pendientes", "Pendientes", "✕✕✕", [("Activar rama", "", "con rama, o al elegirla → En curso"), ("A propuesta", "", "→ propuestas"), ("Eliminar", "de", "→ fuera de la cola")]),
    "curso": ("En curso", "arriba, en amarillo", "✓✓✕", [("A observación", "", "→ En observación"), ("Cerrar", "", "→ Cerradas"), ("Descartar", "de", "→ Descartada"), ("Activar rama", "", "→ la prueba en su rama"), ("", "cl", "Claude, sin trabajo en su rama → Pendientes")]),
    "obs": ("En observación", "En observación", "✕✕✓", [("Cerrar", "", "→ Cerradas"), ("Revertir · eliminar", "de", "→ fuera de la cola"), ("Revertir · a Pendientes", "de", "→ Pendientes"), ("", "cl", "↺ Reabrir, con Claude → En curso")]),
    "cerr": ("Cerradas", "Cerradas, en verde", "✕✕✓", [("A observación", "", "→ En observación"), ("Revertir · eliminar", "de", "→ fuera de la cola"), ("Revertir · a Pendientes", "de", "→ Pendientes"), ("", "cl", "↺ Reabrir, con Claude → En curso")]),
    "desc": ("Descartada", "Cerradas, con D", "✕✕✕", [("", "cl", "↺ Reabrir, con Claude → En curso")]),
}


def sf_fichas():
    o = []
    for eid, (nombre, panel, marcas, botones) in SF_FICHAS.items():
        ms = "".join(f'<li><b class="{"si" if ch == "✓" else "no"}">{ch}</b> {n}</li>' for ch, n in zip(marcas, ["rama", "subagente", "en develop"]))
        bs = "".join(
            (f'<li><span class="bt {k}">{escape(b)}</span> {escape(t)}</li>' if b else f'<li class="cl-li">{escape(t)}</li>')
            for b, k, t in botones)
        o.append(f'<div class="ficha" data-f="{eid}" hidden><h4>{escape(nombre)}</h4><ul class="marcas">{ms}</ul>'
                 f'<p class="en-panel">En el panel: {escape(panel)}</p><ul class="bts">{bs}</ul></div>')
    return "".join(o)


# ───────────────────────── versiones verticales ─────────────────────────
# Reutilizan las definiciones (flechas, retículas) de su versión horizontal, que está en la misma página.

def dd_arquitectura_v():
    o = ['<svg class="v" viewBox="0 0 560 500" role="img" aria-label="Arquitectura en vertical: fuente, equipo y proyecto, de arriba abajo.">',
         '<rect width="560" height="500" class="paper"/><rect width="560" height="500" fill="url(#dd-dots2)" opacity=".55"/>',
         '<rect class="zone" x="20" y="24" width="520" height="138" rx="8"/><rect class="zone" x="20" y="188" width="520" height="138" rx="8"/>'
         '<rect class="zone" x="20" y="352" width="520" height="138" rx="8"/>',
         '<text class="eb" x="36" y="44">FUENTE · REPOSITORIO</text><text class="eb" x="36" y="208">EQUIPO · ~/.CLAUDE</text>'
         '<text class="eb" x="36" y="372">PROYECTO CONSUMIDOR</text>',
         '<line class="fl acc" x1="150" y1="138" x2="150" y2="220" marker-end="url(#dd2-a)"/>',
         '<line class="fl" x1="260" y1="256" x2="310" y2="256" marker-end="url(#dd2-m)"/>',
         '<line class="fl" x1="415" y1="292" x2="415" y2="384" marker-end="url(#dd2-m)"/>',
         '<line class="fl dash" x1="260" y1="420" x2="310" y2="420" marker-end="url(#dd2-m)"/>',
         etiqueta(158, 180, "PUBLICA", ancla="start", fs=10), etiqueta(285, 248, "INSTALA", fs=10),
         etiqueta(423, 344, "ESCRIBE", ancla="start", fs=10), etiqueta(285, 412, "LEE", fs=10),
         dd_nodo(40, 66, 220, 72, "CÓDIGO", "plugins/sf", "skills · mod · cola.py", tk=5.9),
         dd_nodo(310, 66, 210, 72, "DOCS", "docs/", "brain de desarrollo", tk=5.9),
         dd_nodo(40, 220, 220, 72, "PLUGIN", "Plugin sf", "versión publicada", "phase focal", tk=5.9),
         dd_nodo(310, 220, 210, 72, "CLI", "cola.py", "~/.claude/sf/cola.py", tk=5.9),
         dd_nodo(40, 384, 220, 72, "MOD", "Panel de la SF", "muestra la cola", tk=5.9),
         dd_nodo(310, 384, 210, 72, "ESTADO", "peticiones.json", ".sf/peticiones.json", tk=5.9),
         '</svg>']
    return "".join(o)


def dd_fases_v():
    fases = ["Visión", "Especificación e interfaz", "Definición técnica", "Devslices", "Preparación",
             "Desarrollo y verificación", "Cierre"]
    o = ['<svg class="v" viewBox="0 0 560 500" role="img" aria-label="Línea de fases de la metodología en vertical, de la visión al cierre.">',
         '<rect width="560" height="500" class="paper"/>', '<line class="rule" x1="60" y1="36" x2="60" y2="464"/>']
    for i, f in enumerate(fases):
        y = 40 + i * 70
        acc = i == 5
        o.append(f'<circle class="{"fill-a" if acc else "ink"}" cx="60" cy="{y}" r="{6 if acc else 4}"/>'
                 f'<line class="tick" x1="72" y1="{y}" x2="86" y2="{y}"/>'
                 f'<text class="eb" x="96" y="{y - 6}">FASE {i + 1}</text>'
                 f'<text class="nn{" acc-t" if acc else ""}" x="96" y="{y + 12}">{escape(f)}</text>')
    o.append('</svg>')
    return "".join(o)


def ve_ciclo_v():
    aristas = [("new", "M240 22 V60", ""), ("act", "M220 124 V210", ""), ("sin", "M260 210 V124", "dash"),
               ("elim", "M330 92 H400", ""), ("desc", "M330 226 H400", ""), ("rdesc", "M400 256 H330", "dash"),
               ("obs", "M240 274 V410", ""), ("cer", "M220 474 V560", ""), ("vob", "M260 560 V474", ""),
               ("cdir", codo((150, 262), (110, 262), (110, 600), (150, 600)), ""),
               ("rdev", codo((350, 500), (372, 500), (372, 270), (330, 270)), "dash"),
               ("rev", codo((240, 650), (240, 680), (40, 680), (40, 108), (150, 108)), ""),
               ("relim", codo((240, 680), (552, 680), (552, 150), (470, 150), (470, 124)), "")]
    o = ['<svg viewBox="0 0 560 700" role="img" aria-label="Máquina de estados en vertical, con el mismo recorrido paso a paso.">',
         '<rect width="560" height="700" fill="url(#ve-grid)"/>',
         '<rect class="bnd" x="130" y="384" width="220" height="266" rx="4"/><text class="bnd-t" x="138" y="400">EN DEVELOP</text>']
    for aid, d, k in aristas:
        o.append(f'<path class="ve-e {k}" data-e="{aid}" d="{d}" marker-end="url(#ve-ah)"/>')
    o.append('<circle class="jn" cx="240" cy="680" r="3.5"/>')
    labs = [(252, 40, "nueva petición", "start"), (212, 176, "Activar rama", "end"), (268, 176, "sin trabajo", "start"),
            (365, 84, "Eliminar", "middle"), (365, 214, "Descartar", "middle"), (365, 274, "Reabrir", "middle"),
            (248, 350, "A observación", "start"), (212, 524, "Cerrar", "end"), (268, 524, "A observación", "start"),
            (102, 440, "Cerrar", "end"), (380, 392, "Reabrir, con Claude", "start"), (250, 670, "Revertir", "start"),
            (48, 200, "a Pendientes", "start"), (544, 420, "eliminar", "end")]
    for x, y, t, a in labs:
        o.append(etiqueta(x, y, t, fs=10.5, k=0.55, extra=0, ancla=a, clase="ve-l", mascara="halo-t", pad=3))
    o += [ve_nodo("pend", 150, 60, "Pendientes", "sin rama", "ESTADO"),
          ve_nodo("curso", 150, 210, "En curso", "rama · subagente", "ESTADO"),
          ve_nodo("obs", 150, 410, "En observación", "squash en develop", "ESTADO"),
          ve_nodo("cerr", 150, 560, "Cerradas", "en develop", "ESTADO")]
    for nid, x, y, nombre, sub, kind in [("fuera", 400, 60, "Fuera de la cola", "eliminada", "EFECTO"),
                                         ("desc", 400, 210, "Descartada", "nada en develop", "ESTADO")]:
        o.append(f'<g class="ve-n gone" data-n="{nid}"><rect class="halo" x="{x - 5}" y="{y - 5}" width="150" height="74" rx="9"/>'
                 f'<rect class="box" x="{x}" y="{y}" width="140" height="64" rx="5"/><text class="kind" x="{x + 10}" y="{y + 17}">{kind}</text>'
                 f'<text class="nm" x="{x + 10}" y="{y + 37}">{escape(nombre)}</text><text class="sb" x="{x + 10}" y="{y + 54}">{escape(sub)}</text></g>')
    for x, y, t in [(240, 44, "1"), (220, 150, "2·6"), (240, 300, "3"), (220, 496, "4"), (140, 680, "5"), (342, 226, "7"), (342, 256, "8")]:
        o.append(f'<g class="co" data-s="{t.replace("·", " ")}" transform="translate({x} {y})"><circle r="10"/><text y="3.5">{t}</text></g>')
    o.append('</svg>')
    return "".join(o)


def ve_arquitectura_v():
    def l(x, y, t, a="start"):
        return etiqueta(x, y, t, fs=10.5, k=0.55, extra=0, ancla=a, clase="ve-l", mascara="halo-t", pad=3)
    return ('<svg viewBox="0 0 560 620" role="img" aria-label="Arquitectura en vertical: el principal ordena a cola.py, que escribe la cola y hace commits en develop; el panel muestra la cola.">'
            '<rect width="560" height="620" fill="url(#ve-grid2)"/>'
            '<rect class="bnd" x="16" y="16" width="528" height="588" rx="4"/><text class="bnd-t" x="26" y="34">EQUIPO DEL PROPIETARIO</text>'
            '<path class="ve-e" d="M280 114 V190" marker-end="url(#ve-ah2)"/>'
            f'<path class="ve-e" d="{codo((230, 254), (230, 290), (150, 290), (150, 318))}" marker-end="url(#ve-ah2)"/>'
            f'<path class="ve-e" d="{codo((330, 254), (330, 290), (410, 290), (410, 318))}" marker-end="url(#ve-ah2)"/>'
            '<path class="ve-e dash" d="M150 500 V396" marker-end="url(#ve-ah2)"/>'
            + l(288, 156, "ordena") + l(120, 282, "escribe", "end") + l(422, 282, "commit") + l(158, 452, "muestra")
            + '<g class="dots v" aria-hidden="true"><circle r="4" class="tok"/><circle r="4" class="tok t2"/><circle r="4" class="tok t3"/></g>'
            '<g class="ve-n"><rect class="box" x="190" y="50" width="180" height="64" rx="5"/><text class="kind" x="202" y="67">AGENTE</text>'
            '<text class="nm" x="202" y="87">Principal</text><text class="sb" x="202" y="104">habla con el propietario</text></g>'
            '<g class="ve-n is-key"><rect class="halo" x="185" y="185" width="190" height="74" rx="9"/><rect class="box" x="190" y="190" width="180" height="64" rx="5"/>'
            '<text class="kind" x="202" y="207">CLI</text><text class="nm" x="202" y="227">cola.py</text><text class="sb" x="202" y="244">único que escribe</text></g>'
            '<g class="ve-n"><path class="cyl" d="M60 330 v48 a90 10 0 0 0 180 0 v-48"/><ellipse class="cyl" cx="150" cy="330" rx="90" ry="10"/>'
            '<text class="nm" x="150" y="362" text-anchor="middle">peticiones.json</text><text class="sb" x="150" y="378" text-anchor="middle">.sf/</text></g>'
            '<g class="ve-n"><path class="cyl" d="M320 330 v48 a90 10 0 0 0 180 0 v-48"/><ellipse class="cyl" cx="410" cy="330" rx="90" ry="10"/>'
            '<text class="nm" x="410" y="362" text-anchor="middle">git · develop</text><text class="sb" x="410" y="378" text-anchor="middle">decisiones y cierres</text></g>'
            '<g class="ve-n"><rect class="box" x="60" y="500" width="180" height="64" rx="5"/><text class="kind" x="72" y="517">MOD</text>'
            '<text class="nm" x="72" y="537">Panel</text><text class="sb" x="72" y="554">muestra la cola</text></g>'
            '</svg>')


def cc_paso_v(n, x, y, nombre, l1, l2, tipo, actor):
    """Paso del flujo vertical: el actor va a la izquierda, encima de la caja."""
    return (f'<text class="actor" x="{x + 18}" y="{y - 6}">{actor}</text>'
            f'<rect class="st {tipo}" x="{x}" y="{y}" width="160" height="80" rx="8"/>'
            f'<circle class="badge {tipo}" cx="{x}" cy="{y}" r="12"/><text class="bn" x="{x}" y="{y + 4}" text-anchor="middle">{n}</text>'
            f'<text class="t" x="{x + 80}" y="{y + 32}" text-anchor="middle">{escape(nombre)}</text>'
            f'<text class="d" x="{x + 80}" y="{y + 50}" text-anchor="middle">{escape(l1)}</text>'
            f'<text class="d" x="{x + 80}" y="{y + 64}" text-anchor="middle">{escape(l2)}</text>')


def cc_ciclo_v():
    a, r = 'marker-end="url(#cc-s)"', 'marker-end="url(#cc-r)"'
    o = ['<svg viewBox="0 0 560 760" role="img" aria-label="El mismo flujo en vertical: los pasos bajan por el centro, las excepciones a la derecha y las vueltas a la izquierda.">',
         '<rect width="560" height="760" fill="#020617"/><rect width="560" height="760" fill="url(#cc-grid)"/>',
         '<rect x="16" y="14" width="528" height="52" rx="8" fill="rgba(30,41,59,.2)" stroke="#64748b" stroke-dasharray="6,4"/>',
         '<text class="actor" x="30" y="34">PRERREQUISITOS</text><text class="d" x="30" y="52">proyecto en la SF · cola en .sf/ · panel abierto</text>',
         f'<line x1="200" y1="120" x2="200" y2="148" class="ln" {a}/>', '<text class="la" x="208" y="138">cola</text>',
         f'<line x1="200" y1="230" x2="200" y2="288" class="ln" {a}/>', '<text class="la" x="208" y="264">Activar rama</text>',
         f'<line x1="200" y1="370" x2="200" y2="406" class="ln" {a}/>', '<text class="la" x="208" y="392">prueba</text>',
         f'<line x1="200" y1="494" x2="200" y2="538" class="ln" {a}/>', '<text class="la" x="208" y="520">observar</text>',
         f'<line x1="200" y1="620" x2="200" y2="678" class="ln" {a}/>', '<text class="la" x="208" y="654">Cerrar</text>',
         f'<path d="{codo((158, 450), (95, 450), (95, 660), (150, 660), (150, 678))}" class="ln" {a}/>',
         '<text class="la" x="126" y="442" text-anchor="middle">sí · Cerrar</text>',
         f'<path d="{codo((120, 320), (90, 320), (90, 200), (118, 200))}" class="ln" stroke-dasharray="6,3" {a}/>',
         '<text class="la" x="84" y="262" text-anchor="end">sin trabajo</text>',
         f'<path d="{codo((130, 700), (40, 700), (40, 340), (118, 340))}" fill="none" stroke="#22d3ee" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#cc-c)"/>',
         '<text class="lc" x="46" y="590">↻ Reabrir</text><text class="lc" x="46" y="602">con Claude</text>',
         f'<line x1="280" y1="190" x2="378" y2="190" class="lr" {r}/>', '<text class="lx" x="330" y="182" text-anchor="middle">Eliminar</text>',
         f'<line x1="242" y1="450" x2="378" y2="450" class="lr" {r}/>', '<text class="lx" x="310" y="442" text-anchor="middle">no · Descartar</text>',
         f'<path d="{codo((280, 580), (548, 580), (548, 136), (240, 136), (240, 148))}" class="lr" {r}/>',
         f'<path d="{codo((270, 700), (548, 700), (548, 580))}" class="lr"/>',
         f'<path d="M548 190 H522" class="lr" {r}/>',
         '<text class="lx" x="540" y="560" text-anchor="end">Revertir · eliminar o a Pendientes</text>',
         '<text class="lx" x="400" y="130" text-anchor="middle">a Pendientes</text>',
         '<rect x="140" y="84" width="120" height="36" rx="18" fill="rgba(8,51,68,.4)" stroke="#22d3ee" stroke-width="2"/>',
         '<text class="t" x="200" y="106" text-anchor="middle">Nueva petición</text>',
         cc_paso_v(1, 120, 150, "Pendientes", "en la cola", "sin rama", "manual", "PROPIETARIO"),
         cc_paso_v(2, 120, 290, "En curso", "rama + subagente", "trabaja la tarea", "auto", "SUBAGENTE"),
         '<rect x="170" y="420" width="60" height="60" rx="4" transform="rotate(45 200 450)" fill="rgba(136,19,55,.4)" stroke="#fb7185" stroke-width="1.5"/>',
         '<text class="t" x="200" y="454" text-anchor="middle">¿Sigue?</text>',
         cc_paso_v(3, 120, 540, "En observación", "squash en develop", "sin rama", "integ", "DEVELOP"),
         '<rect x="130" y="680" width="140" height="40" rx="20" fill="rgba(8,51,68,.4)" stroke="#22d3ee" stroke-width="2"/>',
         '<text class="t" x="200" y="704" text-anchor="middle">Cerradas</text>',
         '<rect x="380" y="170" width="140" height="40" rx="20" fill="rgba(136,19,55,.25)" stroke="#fb7185" stroke-width="1.5"/>',
         '<text class="t" x="450" y="194" text-anchor="middle">Fuera de la cola</text>',
         '<rect x="380" y="420" width="140" height="60" rx="8" fill="rgba(136,19,55,.4)" stroke="#fb7185" stroke-width="1.5"/>',
         '<text class="t" x="450" y="446" text-anchor="middle">Descartada</text><text class="d" x="450" y="464" text-anchor="middle">Claude puede reabrirla</text>',
         '</svg>']
    return "".join(o)


def cc_bucle_v():
    a = 'marker-end="url(#cc2-s)"'
    return ('<svg viewBox="0 0 560 680" role="img" aria-label="Bucle de mejora continua en vertical: la vuelta sube por la izquierda.">'
            '<rect width="560" height="680" fill="#020617"/>'
            f'<path d="{codo((200, 620), (200, 650), (40, 650), (40, 70), (118, 70))}" fill="none" stroke="#22d3ee" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#cc2-c)"/>'
            '<text class="lc" x="46" y="356">↻ siguiente</text><text class="lc" x="46" y="368">mejora</text>'
            f'<line x1="200" y1="110" x2="200" y2="168" class="ln" {a}/><text class="la" x="208" y="144">anota</text>'
            f'<line x1="200" y1="250" x2="200" y2="308" class="ln" {a}/><text class="la" x="208" y="284">prepara</text>'
            f'<line x1="200" y1="390" x2="200" y2="426" class="ln" {a}/>'
            f'<line x1="200" y1="514" x2="200" y2="538" class="ln" {a}/><text class="la" x="208" y="530">sí</text>'
            '<line x1="242" y1="470" x2="378" y2="470" class="lr" marker-end="url(#cc2-r)"/><text class="lx" x="310" y="462" text-anchor="middle">no</text>'
            + cc_paso_v(1, 120, 30, "Detectar mejora", "en el trabajo", "de una sesión", "manual", "CLAUDE")
            + cc_paso_v(2, 120, 170, "Anotar", "bajo Mejorar la", "Software Factory", "auto", "COLA")
            + cc_paso_v(3, 120, 310, "Preparar propuesta", "concreta, con", "su porqué", "auto", "CLAUDE")
            + '<text class="actor" x="246" y="430">PROPIETARIO</text>'
            '<rect x="170" y="440" width="60" height="60" rx="4" transform="rotate(45 200 470)" fill="rgba(136,19,55,.4)" stroke="#fb7185" stroke-width="1.5"/>'
            '<text class="t" x="200" y="474" text-anchor="middle">¿OK?</text>'
            + cc_paso_v(4, 120, 540, "Aplicar y publicar", "en su tarea", "y su rama", "integ", "SF")
            + '<rect x="380" y="445" width="150" height="50" rx="8" fill="rgba(30,41,59,.3)" stroke="#94a3b8" stroke-dasharray="5,3"/>'
            '<text class="t" x="455" y="474" text-anchor="middle">Queda en propuestas</text>'
            '</svg>')


# ───────────────────────── pesos en tokens ─────────────────────────
# Tamaños en bytes de los archivos en el commit citado (API de GitHub) o en este repositorio.
# Tokens estimados a 4 caracteres por token en inglés y 3,5 en español; es una estimación.

PESOS = [
    ("diagram-design", "SKILL.md 30,9k + style-guide.md 20,7k + type-state.md 2,0k + semantic-patterns.md 16,7k (el ciclo de vida lo exige)",
     70.3, 4.0, "Si además lee primitives-core.md (13,0k), 83,3k: unos 21k tokens.",
     "example-state.html 8,7k; la página completa del mapa de fases, 12,6k", 8.7, 12.6, 4.0),
    ("visual-explainer", "SKILL.md 8,6k + style-guide.md 7,6k + diagrams.md 5,8k + motion.md 5,3k (el replay)",
     27.3, 4.0, "Con kit.md (6,5k), 33,8k: unos 8,5k tokens. El kit CSS/JS lo inyecta su renderizador y no pasa por el contexto.",
     "replay-job-queue.html 19,0k (página entera con su replay)", 19.0, 19.0, 4.0),
    ("process-flow-diagram", "SKILL.md 17,5k + resources/template.html 20,7k (la skill manda copiarlo)",
     38.2, 4.0, "Siempre las dos piezas.",
     "sprint-report-flow.html 15,2k a inventory-control.html 20,0k, con la barra de exportar", 15.2, 20.0, 4.0),
    ("theme-factory", "SKILL.md 3,1k + un tema 0,5k", 3.7, 4.0, "No dibuja: solo paleta y letra.", "—", 0, 0, 4.0),
    ("diagramas-svg (guía actual de la SF)", "diagramas-svg.md 8,3k", 8.3, 3.5,
     "Hoy se lee junto a crear_documentos (SKILL.md 42,8k), que se carga de todos modos para escribir el documento.",
     "las croquetas actuales de Cómo funcionan los estados: 17,1k (SVG, CSS y datos en línea)", 17.1, 17.1, 3.5),
]


def k(v):
    return f"{v:.1f}k".replace(".", ",")


def tabla_pesos(medidas):
    filas = []
    for nombre, que, kb, cpt, nota, ej, d1, d2, cpt2 in PESOS:
        tok = kb * 1000 / cpt
        diag = "—" if not d1 else (k(d1 / cpt2) if d1 == d2 else f"{k(d1 / cpt2)} a {k(d2 / cpt2)}")
        filas.append(f'<tr><th scope="row">{escape(nombre)}</th><td>{escape(que)}</td><td class="n">{k(kb)}</td><td class="n">{k(tok / 1000)}</td>'
                     f'<td>{escape(nota)}</td><td>{escape(ej)}</td><td class="n">{diag}</td></tr>')
    sintesis_kb = 8.3 + 5.0
    filas.append('<tr class="prop"><th scope="row">Síntesis para la SF (estimada)</th><td>diagramas-svg.md 8,3k + una sección de flujos de unos 5k (reglas de flechas, carriles, botones, fichas y presupuesto)</td>'
                 f'<td class="n">{k(sintesis_kb)}</td><td class="n">{k(sintesis_kb / 3.5)}</td><td>Sin plantillas ni ejemplos que cargar: lo común ya está en crear_documentos.</td>'
                 f'<td>el diagrama de esta página: {k(medidas["sf"] / 1000)} (SVG con fichas; el CSS común iría al generador)</td><td class="n">{k(medidas["sf"] / 3500)}</td></tr>')
    return ('<div class="tabla"><table><caption>Lo que pesa cada opción en el contexto de Claude. Tamaños en miles de caracteres; tokens estimados a 4 caracteres por token en inglés y 3,5 en español.</caption>'
            '<thead><tr><th scope="col">Opción</th><th scope="col">Qué se carga para un diagrama de estados</th><th scope="col">Caracteres</th><th scope="col">Tokens</th>'
            '<th scope="col">Nota</th><th scope="col">Diagrama típico</th><th scope="col">Tokens del diagrama</th></tr></thead><tbody>'
            + "".join(filas) + '</tbody></table></div>'
            f'<p class="tipos">Como referencia, lo que ocupan los diagramas de esta página: diagram-design, {k(medidas["dd"] / 1000)} caracteres; '
            f'visual-explainer con su replay, {k(medidas["ve"] / 1000)}; process-flow-diagram, {k(medidas["cc"] / 1000)}; la Síntesis, {k(medidas["sf"] / 1000)}, sin contar el CSS de la página.</p>')


# ───────────────────────── página ─────────────────────────

CSS = r"""
:root{--p-fondo:#ffffff;--p-texto:#1f2937;--p-suave:#4b5563;--p-borde:#e2e8f0;--p-enlace:#1d6fb6;--p-op:#f8fafc}
:root[data-theme=dark]{--p-fondo:#0b0f14;--p-texto:#e5e7eb;--p-suave:#9ca3af;--p-borde:#273142;--p-enlace:#7cb4ea;--p-op:#111821}
*{box-sizing:border-box}
body{margin:0;background:var(--p-fondo);color:var(--p-texto);font:16px/1.55 'DM Sans',system-ui,sans-serif}
a{color:var(--p-enlace)}
.cabecera{display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;flex-wrap:wrap}
.tema{font:500 .85rem 'DM Sans',sans-serif;color:var(--p-texto);background:var(--p-op);border:1px solid var(--p-borde);border-radius:6px;padding:.35rem .8rem;cursor:pointer;margin-top:.4rem}
.tema:focus-visible{outline:2px solid var(--p-enlace);outline-offset:2px}
main{max-width:1400px;margin:0 auto;padding:2rem 16px 4rem}
h1{font:600 clamp(1.7rem,4vw,2.2rem)/1.15 'Outfit',sans-serif;margin:0 0 .6rem}
.intro{max-width:46rem;color:var(--p-suave)}
nav.indice{display:flex;flex-wrap:wrap;gap:.4rem 1rem;margin:1rem 0 0;font-size:.92rem}
section.skill{border-top:1px solid var(--p-borde);margin-top:3rem;padding-top:1.4rem}
section.skill>h2{font:600 1.5rem/1.25 'Outfit',sans-serif;margin:0}
.fuente{font-size:.82rem;color:var(--p-suave);margin:.2rem 0 1rem;overflow-wrap:anywhere}
h3.sub{font:600 1.1rem/1.3 'Outfit',sans-serif;margin:2rem 0 .3rem}
.juicio{max-width:46rem} .juicio b{font-weight:600}
.opinion{max-width:46rem;background:var(--p-op);border:1px solid var(--p-borde);border-radius:8px;padding:.7rem 1rem;margin:1.2rem 0 0}
.opinion b{font-weight:600}
.desliza{overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:8px}
.desliza>svg{display:block;width:100%;height:auto}
.aviso-movil{display:none;font-size:.78rem;opacity:.75;margin:.3rem 0 0}
@media (max-width:720px){.aviso-movil{display:block}}
figcaption.pie{font-size:.88rem;color:var(--p-suave);margin-top:.5rem;max-width:46rem}
figure{margin:1rem 0 0}
.pareja{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);gap:18px;align-items:start}
.pareja.ancha{grid-template-columns:minmax(0,2.2fr) minmax(0,1fr)}
@media (max-width:980px){.pareja,.pareja.ancha{grid-template-columns:minmax(0,1fr)}}
.lado{font:600 .66rem/1.2 'DM Sans',sans-serif;letter-spacing:.14em;text-transform:uppercase;opacity:.7;margin:0 0 .45rem}
.eyebrow+.pareja,.lab+.pareja{margin-top:.9rem}
.vert>svg{display:block;width:100%;max-width:560px;height:auto;margin:0 auto}
.sin-v{font-size:.86rem;color:var(--p-suave);max-width:46rem;margin:.5rem 0 0}
.sin-v b{font-weight:600}
.cq{container-type:inline-size} .cq .solo-v{display:none}
.moviles{display:flex;flex-wrap:wrap;gap:24px;margin-top:1rem;align-items:flex-start}
.telefono{width:375px;max-width:100%;border:1px solid var(--p-borde);border-radius:24px;padding:18px 16px;background:var(--p-fondo)}
.telefono .tit{font-size:.84rem;color:var(--p-suave);margin:0 0 .6rem}
.telefono .dd{padding:16px 12px 12px}
.lista{max-width:46rem;padding-left:1.2rem} .lista li{margin:.3rem 0}
table.corta{min-width:0}
.tipos{font-size:.92rem;color:var(--p-suave);max-width:60rem}
.una-linea{max-width:46rem;padding:.8rem 1rem;border-left:3px solid var(--p-borde)}
code{font-size:.88em}
.tabla{overflow-x:auto;margin-top:1rem}
table{border-collapse:collapse;font-size:.86rem;min-width:760px;width:100%}
caption{text-align:left;color:var(--p-suave);font-size:.85rem;margin-bottom:.5rem}
th,td{border-top:1px solid var(--p-borde);padding:.5rem .6rem;text-align:left;vertical-align:top}
thead th{font-weight:600;border-top:0;border-bottom:2px solid var(--p-borde)}
td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr.prop th,tr.prop td{background:var(--p-op)}

/* diagram-design */
.dd{--paper:#f5f5f5;--paper2:#ececec;--ink:#2d3142;--muted:#4f5d75;--soft:#5a6580;--rule:rgba(45,49,66,.12);--rule-s:#bfc0c0;--accent:#bf4520;--tint:rgba(191,69,32,.08);--node:#fff;--dots:rgba(45,49,66,.10);
 background:var(--paper);color:var(--ink);border-radius:10px;padding:26px 22px 16px}
:root[data-theme=dark] .dd{--paper:#2d3142;--paper2:#393e53;--ink:#f5f5f5;--muted:#bfc0c0;--soft:#949eb2;--rule:rgba(245,245,245,.12);--rule-s:rgba(191,192,192,.25);--accent:#f08a59;--tint:rgba(240,138,89,.10);--node:#353a4e;--dots:rgba(245,245,245,.10)}
.dd .eyebrow{font:500 .66rem 'Geist Mono',monospace;letter-spacing:.18em;text-transform:uppercase;color:var(--soft);margin:0}
.dd h4.t{font:400 2rem/1.1 'Instrument Serif',serif;margin:.3rem 0 .4rem}
.dd .subt{font:400 .95rem/1.5 'Geist',sans-serif;color:var(--muted);max-width:44rem;margin:0 0 1rem}
.dd .paper{fill:var(--paper)} .dd .dot{fill:var(--dots)}
.dd .band{fill:none;stroke:var(--rule-s);stroke-dasharray:4 3}
.dd .zone{fill:none;stroke:var(--rule-s)}
.dd .eb{font:500 8px 'Geist Mono',monospace;letter-spacing:.14em;fill:var(--soft)}
.dd .fl{fill:none;stroke:var(--muted);stroke-width:1.2} .dd .fl.dash{stroke-dasharray:5 4} .dd .fl.acc{stroke:var(--accent);stroke-width:1.4}
.dd .ah-m{fill:var(--muted)} .dd .ah-a{fill:var(--accent)}
.dd .mask{fill:var(--paper)}
.dd .lbl{font:400 8px 'Geist Mono',monospace;letter-spacing:.06em;fill:var(--muted)} .dd .acc-t{fill:var(--accent)}
.dd .phase{fill:var(--node);stroke:var(--ink);stroke-width:1} .dd .phase.focal{fill:var(--tint);stroke:var(--accent)}
.dd .terminal{fill:var(--paper2);stroke:var(--muted);stroke-width:1}
.dd .tagbox{fill:none;stroke:var(--ink);stroke-opacity:.4;stroke-width:.8}
.dd .tag{font:500 7px 'Geist Mono',monospace;letter-spacing:.1em;fill:var(--ink)}
.dd .nn{font:600 13px 'Geist',sans-serif;fill:var(--ink)} .dd .nn.acc-t{fill:var(--accent)}
.dd .sl{font:400 9px 'Geist Mono',monospace;fill:var(--muted)}
.dd .ink{fill:var(--ink)} .dd .ring-a{fill:none;stroke:var(--accent)} .dd .fill-a{fill:var(--accent)}
.dd .call{font:italic 400 15px 'Instrument Serif',serif;fill:var(--muted)}
.dd .life{stroke:var(--rule-s);stroke-dasharray:3 4} .dd .act{fill:var(--node);stroke:var(--muted)}
.dd .rule{stroke:var(--rule-s);stroke-width:1.2} .dd .tick{stroke:var(--rule-s)}
.dd .cards{display:grid;grid-template-columns:1.1fr 1fr .9fr;gap:14px;margin-top:18px}
@media (max-width:720px){.dd .cards{grid-template-columns:1fr}}
.dd .card{background:var(--node);border:1px solid var(--rule);border-radius:6px;padding:14px 16px;font:400 .86rem/1.5 'Geist',sans-serif;color:var(--muted)}
.dd .card h5{font:600 .95rem 'Geist',sans-serif;color:var(--ink);margin:.1rem 0 .3rem;display:flex;align-items:center;gap:.45rem}
.dd .card .cd{width:8px;height:8px;border-radius:50%;background:var(--muted);display:inline-block} .dd .card .cd.c{background:var(--accent)}
.dd .card p{margin:0}
.dd .foot{display:flex;justify-content:space-between;flex-wrap:wrap;gap:.5rem;font:500 .62rem 'Geist Mono',monospace;letter-spacing:.16em;color:var(--soft);margin-top:16px;border-top:1px solid var(--rule);padding-top:10px}
.dd .desliza>svg{min-width:720px}
.dd .desliza.skill>svg{min-width:1000px}
.dd svg.v .nn{font-size:16px} .dd svg.v .lbl{font-size:10px} .dd svg.v .sl{font-size:11px} .dd svg.v .tag{font-size:8px} .dd svg.v .eb{font-size:10px} .dd svg.v .call{font-size:16px}
.dd .plegado{font:italic 400 15px 'Instrument Serif',serif;fill:var(--muted)} .dd svg.v .plegado{font-size:16px}
.dd [data-g],.dd [data-plegado]{transition:opacity .25s,visibility .25s}
.dd [data-plegado]{opacity:0;visibility:hidden}
.pl-vueltas [data-g=vueltas],.pl-salidas [data-g=salidas]{opacity:0;visibility:hidden}
.pl-vueltas [data-plegado=vueltas],.pl-salidas [data-plegado=salidas]{opacity:1;visibility:visible}
.dd .mandos{display:flex;gap:.5rem;flex-wrap:wrap;margin:0 0 .8rem}
.dd .mandos button,.dd .hud .x{min-height:44px;font:500 .7rem 'Geist Mono',monospace;letter-spacing:.14em;text-transform:uppercase;background:var(--node);color:var(--ink);border:1px solid var(--rule-s);border-radius:4px;padding:0 .9rem;cursor:pointer}
.dd .mandos button[aria-expanded=false]{color:var(--muted);border-style:dashed}
.dd .mandos button:focus-visible,.dd .hud .x:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.dd .pista{font:400 .84rem/1.45 'Geist',sans-serif;color:var(--muted);margin:.6rem 0 0} .dd .pista.arriba{margin:0 0 .8rem}
[data-hud] .dd-n{cursor:pointer;outline:none}
.dd .fl{transition:opacity .2s,stroke .2s} .dd .dd-n{transition:opacity .2s}
.hl .fl{opacity:.2} .hl .fl.on{opacity:1;stroke:var(--accent);stroke-width:2}
.hl .dd-n{opacity:.45} .hl .dd-n.on{opacity:1}
.dd .dd-n.on>rect:first-child,.dd .dd-n:focus-visible>rect:first-child{stroke:var(--accent);stroke-width:2}
.dd.hud-fig{position:relative}
.dd .hud{position:absolute;right:14px;bottom:14px;width:300px;background:var(--node);border:1px solid var(--rule-s);border-radius:6px;padding:12px 14px;font:400 .84rem/1.45 'Geist',sans-serif;color:var(--muted);box-shadow:0 8px 28px rgba(0,0,0,.14)}
.dd .hud[hidden]{display:none}
.dd .hud h5{font:400 1.6rem/1.1 'Instrument Serif',serif;color:var(--ink);margin:.1rem 0 .45rem;padding-right:3rem}
.dd .hud p{margin:0 0 .4rem}
.dd .hud .x{position:absolute;top:8px;right:8px;min-width:44px;padding:0}
.dd .hud ul{margin:0;padding:0;list-style:none} .dd .hud li{margin:.25rem 0}
.dd .hud .marcas{display:flex;gap:.8rem;flex-wrap:wrap;font:500 .7rem 'Geist Mono',monospace;letter-spacing:.06em;margin-bottom:.4rem}
.dd .hud .bt{font:500 .68rem 'Geist Mono',monospace;letter-spacing:.06em;text-transform:uppercase;border:1px solid var(--muted);border-radius:3px;padding:0 .35em;color:var(--ink)}
.dd .hud .bt.de{border-style:dashed} .dd .hud .cl-li{font-style:italic}
@container (max-width:640px){.cq .solo-h{display:none} .cq .solo-v{display:block} .cq .hud{position:relative;right:auto;bottom:auto;width:auto;margin-top:12px;box-shadow:none}}

/* visual-explainer, registro Blueprint */
.ve{--bg:#f6f8fb;--surface:#ffffff;--text:#16212e;--dim:#566577;--border:rgba(22,33,46,.10);--border-b:#7b8796;--accent:#0b63c5;--accent-dim:rgba(11,99,197,.12);--grid:rgba(11,99,197,.07);--risk:#b42318;--ok:#1a7f37;
 background:var(--bg);color:var(--text);border-radius:6px;padding:22px 22px 16px;font-family:'IBM Plex Sans',sans-serif}
:root[data-theme=dark] .ve{--bg:#0e1621;--surface:#152131;--text:#e6edf5;--dim:#9fb0c3;--border:rgba(230,237,245,.10);--border-b:#7f91a6;--accent:#5aa2f0;--accent-dim:rgba(90,162,240,.16);--grid:rgba(90,162,240,.08);--risk:#f2867b;--ok:#6cc483}
.ve .lab{font:500 .7rem 'IBM Plex Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--dim);margin:0}
.ve h4.t{font:600 1.45rem/1.2 'IBM Plex Sans',sans-serif;margin:.2rem 0 .8rem}
.ve .gridl{fill:none;stroke:var(--grid)}
.ve .bnd{fill:none;stroke:var(--border-b);stroke-dasharray:5 4} .ve .bnd-t{font:500 9.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;fill:var(--dim)}
.ve .ve-e{fill:none;stroke:var(--border-b);stroke-width:1.5;transition:stroke .3s,stroke-width .3s} .ve .ve-e.dash{stroke-dasharray:5 4}
.ve .ve-e.on{stroke:var(--accent);stroke-width:3;marker-end:url(#ve-ah-on)}
.ve .ah{fill:var(--border-b)} .ve .ah-on{fill:var(--accent)}
.ve .halo-t{fill:var(--bg)} .ve .ve-l{font:400 10.5px 'IBM Plex Sans',sans-serif;fill:var(--dim)}
.ve .box{fill:var(--surface);stroke:var(--border-b);stroke-width:1.5;transition:stroke .3s} .ve .gone .box{stroke-dasharray:5 4}
.ve .halo{fill:none;stroke:none} .ve .ve-n.on .halo,.ve .ve-n.is-key .halo{fill:var(--accent-dim)} .ve .ve-n.on .box,.ve .ve-n.is-key .box{stroke:var(--accent);stroke-width:2}
.ve .kind{font:500 8.5px 'IBM Plex Mono',monospace;letter-spacing:.1em;fill:var(--dim)}
.ve .nm{font:600 14px 'IBM Plex Sans',sans-serif;fill:var(--text)} .ve .sb{font:400 10px 'IBM Plex Mono',monospace;fill:var(--dim)}
.ve .jn{fill:var(--border-b)}
.ve .co circle{fill:var(--bg);stroke:var(--accent);stroke-width:1.2} .ve .co text{font:600 9px 'IBM Plex Mono',monospace;fill:var(--accent);text-anchor:middle}
.ve .co.on circle{fill:var(--accent)} .ve .co.on text{fill:var(--bg)}
.ve .player{display:flex;align-items:center;gap:.5rem;margin-top:.7rem;flex-wrap:wrap}
.ve .player button{font:500 .85rem 'IBM Plex Mono',monospace;background:var(--surface);color:var(--text);border:1px solid var(--border-b);border-radius:4px;padding:.25rem .65rem;cursor:pointer}
.ve .player button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.ve .player input{flex:1;min-width:120px;accent-color:var(--accent)}
.ve .player .pos{font:500 .8rem 'IBM Plex Mono',monospace;color:var(--dim);font-variant-numeric:tabular-nums}
.ve .cap{font:400 .98rem/1.45 'IBM Plex Sans',sans-serif;margin:.5rem 0 0;min-height:2.9em}
.ve .cyl{fill:var(--surface);stroke:var(--border-b);stroke-width:1.5}
.ve .tok{fill:var(--accent);offset-path:path('M120 90 H650');animation:ve-run 2.6s linear infinite} .ve .t2{animation-delay:-.87s} .ve .t3{animation-delay:-1.74s}
.ve .v .tok{offset-path:path('M280 82 V290 H150 V330')}
@keyframes ve-run{from{offset-distance:0%}to{offset-distance:100%}}
@media (prefers-reduced-motion:reduce){.ve .tok{animation:none;offset-distance:60%}}
.ve .multiples{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:.4rem}
.ve .case{border-top:1px solid var(--border);padding-top:8px}
.ve .chip{display:inline-block;font:500 .68rem 'IBM Plex Mono',monospace;letter-spacing:.08em;text-transform:uppercase;border:1px solid currentColor;border-radius:3px;padding:0 .4em}
.ve .case h6{font:600 .9rem 'IBM Plex Sans',sans-serif;margin:.35rem 0 .2rem}
.ve .case svg{width:100%;height:auto;display:block}
.ve .k-ok{color:var(--ok)} .ve .k-info{color:var(--accent)} .ve .k-risk{color:var(--risk)}
.ve .m-ok{--st:var(--ok)} .ve .m-info{--st:var(--accent)} .ve .m-risk{--st:var(--risk)}
.ve .mini-e{fill:none;stroke:var(--st);stroke-width:2.5} .ve .mini-ah{fill:var(--st)}
.ve .mini-n{fill:var(--surface);stroke:var(--border-b)} .ve .mini-n.on{stroke:var(--st);stroke-width:2}
.ve .mini-t{font:500 14px 'IBM Plex Sans',sans-serif;fill:var(--text)}
.ve .desliza>svg{min-width:620px}
.ve figcaption{font-size:.86rem;color:var(--dim);margin-top:.4rem}

/* process-flow-diagram (Cocoon-AI): solo oscuro, por diseño */
.cc{background:#020617;border-radius:10px;padding:20px 20px 16px;color:#e2e8f0;font-family:'JetBrains Mono',monospace}
.cc h4.t{font:600 1.1rem 'JetBrains Mono',monospace;margin:0 0 .2rem;color:#f1f5f9} .cc .subt{font-size:.75rem;color:#94a3b8;margin:0 0 .8rem}
.cc .actor{font:500 8px 'JetBrains Mono',monospace;letter-spacing:.12em;fill:#64748b}
.cc .t{font:600 11px 'JetBrains Mono',monospace;fill:#f8fafc} .cc .d{font:400 9px 'JetBrains Mono',monospace;fill:#94a3b8}
.cc .bn{font:600 10px 'JetBrains Mono',monospace;fill:#fff}
.cc .st,.cc .badge{stroke-width:1.5} .cc .badge{fill:#1e293b!important}
.cc .manual{fill:rgba(6,78,59,.4);stroke:#34d399} .cc .auto{fill:rgba(76,29,149,.4);stroke:#a78bfa} .cc .integ{fill:rgba(120,53,15,.3);stroke:#fbbf24}
.cc .ln{fill:none;stroke:#64748b;stroke-width:1.5} .cc .lr{fill:none;stroke:#fb7185;stroke-width:1.5;stroke-dasharray:6 3}
.cc .la{font:400 8px 'JetBrains Mono',monospace;fill:#94a3b8} .cc .lx{font:400 8.5px 'JetBrains Mono',monospace;fill:#fb7185} .cc .lc{font:600 9px 'JetBrains Mono',monospace;fill:#22d3ee}
.cc .cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:14px}
@media (max-width:720px){.cc .cards{grid-template-columns:1fr}}
.cc .card{background:rgba(15,23,42,.8);border:1px solid #1e293b;border-radius:8px;padding:12px 14px;font-size:.74rem;line-height:1.55;color:#cbd5e1}
.cc .card h5{margin:0 0 .35rem;font-size:.72rem;letter-spacing:.12em;color:#22d3ee}
.cc .card ul{margin:0;padding-left:1.1em}
.cc .desliza>svg{min-width:1000px}
.cc .pareja .desliza>svg{min-width:860px}

/* síntesis SF */
.sf{--texto:#1f2937;--suave:#4b5563;--tenue:#6b7280;--nodo:#fff;--borde:#cbd5e1;--naranja:#a6501a;--verde:#1f812d;--rojo:#991b1b;--naranja-f:#fdf3ec;--verde-f:#eef7ef}
:root[data-theme=dark] .sf{--texto:#e5e7eb;--suave:#a3acb9;--tenue:#8b95a3;--nodo:#161d26;--borde:#334155;--naranja:#e8935a;--verde:#6cc47a;--rojo:#f08a8a;--naranja-f:#2a1d14;--verde-f:#14261a}
.sf .lienzo{display:grid;grid-template-columns:minmax(0,560px) minmax(0,1fr);gap:1.5rem;align-items:start}
@media (max-width:900px){.sf .lienzo{grid-template-columns:1fr}}
.sf svg{width:100%;max-width:560px;height:auto;display:block}
.sf .carril{font:600 9px 'DM Sans',sans-serif;letter-spacing:.16em;fill:var(--tenue)}
.sf .e{fill:none;stroke:var(--suave);stroke-width:1.4} .sf .e.de{stroke:var(--rojo)} .sf .e.cl{stroke:var(--tenue);stroke-dasharray:5 4}
.sf .ah-m{fill:var(--suave)} .sf .ah-r{fill:var(--rojo)} .sf .ah-c{fill:var(--tenue)}
.sf .btn{fill:var(--p-fondo);stroke:var(--suave);stroke-width:1} .sf .btn.de{stroke:var(--rojo)}
.sf .btn-t{font:600 10.5px 'DM Sans',sans-serif;fill:var(--texto)} .sf .btn-t.de{fill:var(--rojo)}
.sf .cl-t{font:italic 500 10.5px 'DM Sans',sans-serif;fill:var(--suave)}
.sf .nota{font:400 11px 'DM Sans',sans-serif;fill:var(--suave)}
.sf .pt{fill:var(--suave)} .sf .jn{fill:var(--rojo)} .sf .fin-a{fill:none;stroke:var(--rojo)} .sf .fin{fill:var(--rojo)}
.sf .es{cursor:pointer;outline:none}
.sf .es-c{fill:var(--nodo);stroke:var(--borde);stroke-width:1;transition:stroke .2s}
.sf .es-b{fill:var(--tenue)} .sf .foco .es-c{fill:var(--naranja-f);stroke:var(--naranja)} .sf .foco .es-b{fill:var(--naranja)}
.sf .hecho .es-c{fill:var(--verde-f);stroke:var(--verde)} .sf .hecho .es-b{fill:var(--verde)}
.sf .salida .es-c{stroke-dasharray:4 3}
.sf .es-n{font:600 15px 'Outfit',sans-serif;fill:var(--texto)} .sf .foco .es-n{fill:var(--naranja)} .sf .hecho .es-n{fill:var(--verde)}
.sf .es-m{font:400 9.5px 'DM Sans',sans-serif;fill:var(--suave)}
.sf .es:hover .es-c,.sf .es:focus-visible .es-c,.sf .es.abierta .es-c{stroke:var(--texto);stroke-width:2}
.sf .ficha{border:1px solid var(--borde);border-radius:10px;padding:.9rem 1rem;background:var(--nodo);font-size:.9rem;max-width:26rem}
.sf .ficha h4{font:600 1.1rem 'Outfit',sans-serif;margin:0 0 .4rem}
.sf .ficha ul{list-style:none;margin:0;padding:0} .sf .marcas{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:.4rem!important}
.sf .si{color:var(--verde)} .sf .no{color:var(--rojo)}
.sf .en-panel{color:var(--suave);margin:0 0 .5rem}
.sf .bts li{margin:.3rem 0} .sf .bt{display:inline-block;font:600 .78rem 'DM Sans',sans-serif;border:1px solid var(--suave);border-radius:5px;padding:0 .45em;line-height:1.6}
.sf .bt.de{border-color:var(--rojo);color:var(--rojo)} .sf .cl-li{font-style:italic;color:var(--suave)}
.sf .vacia{color:var(--suave);font-size:.9rem;margin-top:0}
"""

JS = r"""
(function(){
  var b=document.getElementById('tema'), r=document.documentElement;
  b.onclick=function(){var o=r.getAttribute('data-theme')!=='dark';r.setAttribute('data-theme',o?'dark':'light');b.setAttribute('aria-pressed',o);b.textContent=o?'Modo claro':'Modo oscuro';};
})();
(function(){
  document.querySelectorAll('.ve-replay').forEach(function(fig){
  var pasos=JSON.parse(fig.getAttribute('data-pasos'));
  var rng=fig.querySelector('input'), cap=fig.querySelector('.cap'), pos=fig.querySelector('.pos'), n=0, timer=null;
  function pinta(i){
    n=i; rng.value=i; pos.textContent=i+' / '+(pasos.length-1); cap.textContent=pasos[i][2];
    fig.querySelectorAll('.ve-e').forEach(function(e){e.classList.toggle('on', i>0 && e.getAttribute('data-e')===pasos[i][0]);});
    fig.querySelectorAll('.ve-n').forEach(function(g){g.classList.toggle('on', i>0 && g.getAttribute('data-n')===pasos[i][1]);});
    fig.querySelectorAll('.co').forEach(function(c){c.classList.toggle('on', i>0 && c.getAttribute('data-s').split(' ').indexOf(String(i))>=0);});
  }
  var play=fig.querySelector('[data-play]');
  function para(){ if(timer){clearInterval(timer);timer=null;play.textContent='▶';play.setAttribute('aria-label','Reproducir');} }
  fig.querySelector('[data-go="-1"]').onclick=function(){para();pinta(Math.max(0,n-1));};
  fig.querySelector('[data-go="1"]').onclick=function(){para();pinta(Math.min(pasos.length-1,n+1));};
  play.onclick=function(){
    if(timer){para();return;} play.textContent='❚❚'; play.setAttribute('aria-label','Pausa'); if(n>=pasos.length-1) pinta(0);
    timer=setInterval(function(){ if(n>=pasos.length-1){para();return;} pinta(n+1); },1800);
  };
  rng.oninput=function(){para();pinta(+rng.value);};
  pinta(0);
  });
})();
(function(){
  var sf=document.getElementById('sf-ciclo'); if(!sf) return;
  var vacia=sf.querySelector('.vacia');
  function abre(id){
    sf.querySelectorAll('.es').forEach(function(g){var si=g.getAttribute('data-e')===id;g.classList.toggle('abierta',si);g.setAttribute('aria-expanded',si);});
    sf.querySelectorAll('.ficha').forEach(function(f){f.hidden=f.getAttribute('data-f')!==id;});
    vacia.hidden=!!id;
  }
  sf.querySelectorAll('.es').forEach(function(g){
    g.addEventListener('click',function(){abre(g.classList.contains('abierta')?null:g.getAttribute('data-e'));});
    g.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();g.dispatchEvent(new Event('click'));}});
  });
})();
(function(){
  document.querySelectorAll('[data-plegable]').forEach(function(root){
    root.querySelectorAll('[data-plegar]').forEach(function(b){
      b.onclick=function(){var g=b.getAttribute('data-plegar'), on=root.classList.toggle('pl-'+g);
        b.setAttribute('aria-expanded',String(!on)); b.textContent=(on?'+ ':'− ')+b.getAttribute('data-nombre');};
    });
  });
  document.querySelectorAll('[data-hud]').forEach(function(root){
    var datos=JSON.parse(root.getAttribute('data-hud')), hud=root.querySelector('.hud'), sel=null, desde=null;
    function marca(id){
      root.classList.toggle('hl',!!id);
      root.querySelectorAll('.dd-n').forEach(function(n){n.classList.toggle('on',n.getAttribute('data-n')===id);});
      root.querySelectorAll('.fl[data-de]').forEach(function(e){
        var on=!!id&&(e.getAttribute('data-de')===id||e.getAttribute('data-a')===id), m=e.getAttribute('marker-end');
        e.classList.toggle('on',on);
        if(m&&!e.classList.contains('acc')) e.setAttribute('marker-end',on?m.replace(/-m\)$/,'-a)'):m.replace(/-a\)$/,'-m)'));
      });
    }
    function el(t,c,x){var e=document.createElement(t); if(c) e.className=c; if(x) e.textContent=x; return e;}
    function abre(id,nodo){
      sel=id; marca(id);
      root.querySelectorAll('.dd-n').forEach(function(n){n.setAttribute('aria-expanded',String(n.getAttribute('data-n')===id));});
      if(!id){hud.hidden=true; if(desde){desde.focus();desde=null;} return;}
      if(nodo) desde=nodo;
      var d=datos[id], cuerpo=hud.querySelector('.cuerpo'); cuerpo.textContent='';
      cuerpo.appendChild(el('p','eyebrow','Estado · ficha'));
      cuerpo.appendChild(el('h5','',d[0]));
      var ms=el('ul','marcas');
      ['rama','subagente','en develop'].forEach(function(n,i){ms.appendChild(el('li','',(d[2][i]==='✓'?'✓ ':'✕ ')+n));});
      cuerpo.appendChild(ms);
      cuerpo.appendChild(el('p','','En el panel: '+d[1]));
      var bs=el('ul','');
      d[3].forEach(function(b){var li=el('li',b[1]==='cl'?'cl-li':'');
        if(b[0]){li.appendChild(el('span','bt '+b[1],b[0])); li.appendChild(document.createTextNode(' '+b[2]));} else li.textContent=b[2];
        bs.appendChild(li);});
      cuerpo.appendChild(bs); hud.hidden=false;
    }
    root.querySelectorAll('.dd-n').forEach(function(n){
      var id=n.getAttribute('data-n');
      n.setAttribute('tabindex','0'); n.setAttribute('role','button'); n.setAttribute('aria-expanded','false');
      n.setAttribute('aria-label',datos[id][0]+': abrir su ficha');
      n.addEventListener('mouseenter',function(){if(!sel) marca(id);});
      n.addEventListener('mouseleave',function(){if(!sel) marca(null);});
      n.addEventListener('focus',function(){if(!sel) marca(id);});
      n.addEventListener('blur',function(){if(!sel) marca(null);});
      n.addEventListener('click',function(){abre(sel===id?null:id,n);});
      n.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();abre(sel===id?null:id,n);}});
    });
    root.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&sel) abre(null);});
    hud.querySelector('.x').onclick=function(){abre(null);};
  });
})();
"""

FUENTES = ("https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500"
           "&family=Instrument+Serif:ital@0;1&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600"
           "&family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@500;600&family=DM+Sans:ital,wght@0,400;0,500;0,600;1,500&display=swap")


def hz(svg, clase=""):
    return f'<div class="desliza{" " + clase if clase else ""}">{svg}</div>{movil()}'


def pareja(h, v, ancha=False, lado_h="Horizontal · la de la skill", lado_v="Vertical"):
    return (f'<div class="pareja{" ancha" if ancha else ""}"><div><p class="lado">{lado_h}</p>{h}</div>'
            f'<div><p class="lado">{lado_v}</p><div class="vert">{v}</div></div></div>')


def cambia(h, v):
    """La figura elige por su propio ancho: la horizontal si cabe, la vertical si no (consulta de contenedor)."""
    return f'<div class="solo-h">{hz(h)}</div><div class="solo-v vert">{v}</div>'


DD_HUD = {k: (v[0], v[1], v[2], v[3]) for k, v in SF_FICHAS.items()}
DD_HUD["fuera"] = ("Fuera de la cola", "no aparece", "✕✕✕", [("", "", "Eliminada: no tiene botones y no vuelve.")])

DD_FUENTE = "https://github.com/cathrynlavery/diagram-design/blob/f24d98b05e2d7a5e68c2dedfe46e5b7173f50118/"


def dd_fondo():
    hud = escape(json.dumps(DD_HUD, ensure_ascii=False))
    filas = [("Lienzo fijo por tamaño (viewBox) y desplazamiento local en el móvil", "Sí, y lo comprueba a 390 de ancho", "—"),
             ("Versión vertical del mismo diagrama", "No: su ciclo de vida pide un carril de izquierda a derecha", "Sí, con los mismos ids"),
             ("Cambio de horizontal a vertical según el ancho", "No", "Sí, por consulta de contenedor"),
             ("Escala de letra propia de la vertical", "No", "Sí"),
             ("Paso a paso, revelado al cargar y punto que recorre", "Sí: su controlador fijado, hasta 8 pasos y 8 s", "Lo usaríamos tal cual"),
             ("Plegar y desplegar grupos", "No: queda fuera de la skill", "Sí (demo 1)"),
             ("Ficha al pulsar un estado", "No", "Sí (demo 2; ya está en la Síntesis)"),
             ("Resaltar el recorrido de un estado", "No", "Sí (demo 2, al pasar el ratón o con el foco)")]
    tabla = ('<div class="tabla"><table class="corta"><caption>Qué es de la skill y qué añadiríamos.</caption>'
             '<thead><tr><th scope="col">Capacidad</th><th scope="col">diagram-design</th><th scope="col">Nuestro</th></tr></thead><tbody>'
             + "".join(f'<tr><th scope="row">{escape(a)}</th><td>{escape(b)}</td><td>{escape(c)}</td></tr>' for a, b, c in filas)
             + '</tbody></table></div>')
    return f"""<section class="skill" id="dd-fondo"><h2>diagram-design: móvil e interacción</h2>
<p class="fuente">Del mismo commit f24d98b: <a href="{DD_FUENTE}skills/diagram-design/references/output-spec.md">output-spec.md</a> (tamaños y pantalla estrecha), <a href="{DD_FUENTE}skills/diagram-design/references/animation.md">animation.md</a> (movimiento) y sus decisiones <a href="{DD_FUENTE}docs/adr/0001-static-by-default-single-pinned-controller.md">«Estático por defecto; un solo controlador fijado»</a> y <a href="{DD_FUENTE}docs/adr/0003-reveal-is-the-only-sanctioned-autoplay.md">«El revelado es el único movimiento automático»</a>.</p>
<h3 class="sub">Responsividad: qué dice la skill</h3>
<ul class="lista">
<li><b>Lienzo fijo.</b> El tamaño elegido da el viewBox: 960×600 por defecto, 1280×720 para documentación ancha o diapositivas, 1080×1080 para redes. Nada se recoloca: no hay reflujo ni paso de horizontal a vertical.</li>
<li><b>En el móvil no se encoge, se desplaza.</b> El SVG lleva <code>min-width</code> igual al ancho de su viewBox, dentro de un contenedor propio con <code>overflow-x: auto</code>. Su porqué: encogido, un nombre de 12 px baja de su mínimo y nada lo avisa.</li>
<li><b>Lo comprueba.</b> Un script suyo dibuja cada plantilla a 390 de ancho y falla si la página se desborda, si falta el contenedor que desplaza o si <code>min-width</code> no coincide con el viewBox.</li>
<li><b>Al imprimir</b> suelta las dos cosas y deja que el dibujo se encoja entero.</li>
<li><b>Su patrón de ciclo de vida</b> pide un carril de fases de izquierda a derecha. Las verticales de esta página salen de su patrón: son nuestras.</li>
</ul>
<h3 class="sub">Cómo se ve a 375 de ancho</h3>
<div class="moviles">
<div class="telefono"><p class="tit">Como manda la skill: el lienzo entero, que se desplaza.</p>
<div class="dd">{hz(dd_ciclo("ddm1"), "skill")}</div></div>
<div class="telefono"><p class="tit">Como lo haríamos: la vertical, cuando la figura no cabe.</p>
<div class="dd cq">{cambia(dd_ciclo("ddm2h"), dd_ciclo_v("ddm2v"))}</div></div>
</div>
<p class="juicio">A la izquierda, la letra está a su tamaño, pero se ve un tercio del dibujo y hay que desplazar para llegar a Cerradas y a las salidas. A la derecha se ve todo a la vez: el dibujo queda a un 57 %, los nombres de los estados a unos 9 px, y las etiquetas de las flechas a unos 6 px, que es poco.</p>
<h3 class="sub">Cómo lo haríamos nosotros</h3>
<ul class="lista">
<li><b>Dos dibujos de los mismos datos</b>, horizontal y vertical, con los mismos ids, para que la interacción valga en los dos.</li>
<li><b>La figura elige según su propio ancho</b>, con una consulta de contenedor (<code>@container</code>), no según la pantalla: así también sirve en una columna estrecha de escritorio. En las demos de abajo, estrecha la ventana y verás el cambio.</li>
<li><b>La vertical, a unos 400 de ancho y no a 560</b>, para que a 375 quede cerca del 90 % y las etiquetas de las flechas no bajen de 8 px. Si una etiqueta no cabe, su texto va a la ficha.</li>
<li><b>El desplazamiento, como último recurso</b>, para lo que no tiene vertical (una arquitectura muy ancha).</li>
<li><b>La misma comprobación que la suya</b>, a 390 de ancho, más un mínimo de tamaño de letra para el dibujo que se ve.</li>
</ul>
<h3 class="sub">Interacción: qué admite</h3>
<ul class="lista">
<li><b>Estática por defecto</b>, sin ningún script.</li>
<li><b>Movimiento opcional en cuatro modos:</b> ninguno; revelado, una sola vez al cargar; paso a paso, con Reproducir, Pausa, Repetir, Anterior y Siguiente, las flechas del teclado y un aviso para lectores de pantalla; y bucle, un punto decorativo que recorre una flecha. Como mucho, 8 pasos y 8 segundos, y con movimiento reducido se ve el dibujo completo.</li>
<li><b>Un solo controlador fijado:</b> el script tiene que coincidir byte a byte con su plantilla, y su comprobación lo rechaza si no. Lo dice así: un diagrama que necesite una interacción a medida queda fuera de la skill.</li>
<li><b>Por tanto</b>, el paso a paso es suyo (como el replay de visual-explainer, pero con su controlador). Plegar, la ficha al pulsar y el resaltado son nuestros: como dependencia no se podrían añadir sin romper su comprobación. Adaptada como propia, sí, con sus mismas reglas: todo visible sin script, teclado, movimiento reducido, y el estado en atributos y CSS.</li>
</ul>
<h3 class="sub">Demo 1 · Plegar y desplegar</h3>
<figure><div class="dd cq" data-plegable><div class="mandos"><button type="button" data-plegar="vueltas" data-nombre="Vueltas" aria-expanded="true">− Vueltas</button><button type="button" data-plegar="salidas" data-nombre="Salidas" aria-expanded="true">− Salidas</button></div>
{cambia(dd_ciclo("ddf", True), dd_ciclo_v("ddfv", True))}
<p class="pista">Pliega las vueltas o las salidas y queda solo el carril de fases, con una nota de lo plegado. Es lo que la skill resuelve con un diagrama de detalle aparte.</p></div></figure>
<h3 class="sub">Demo 2 · Ficha al pulsar y recorrido resaltado</h3>
<figure><div class="dd cq hud-fig" data-hud="{hud}">
<p class="pista arriba">Pasa el ratón por un estado, o llega a él con el tabulador, y se resaltan las flechas que entran y salen. Púlsalo y se abre su ficha con todos sus botones, también los que el dibujo no muestra, como A propuesta. Escape la cierra.</p>
{cambia(dd_ciclo("ddh", True), dd_ciclo_v("ddhv", True))}
<div class="hud" hidden role="region" aria-label="Ficha del estado" aria-live="polite"><button type="button" class="x" aria-label="Cerrar la ficha">✕</button><div class="cuerpo"></div></div></div></figure>
{tabla}
<p class="opinion"><b>Mi opinión.</b> Con esto, diagram-design gana también para mí, pero adaptada como propia y no como dependencia: su regla de un solo controlador fijado no deja añadir plegar ni la ficha, y su lienzo fijo no deja pasar a vertical. Me quedaría con su dibujo, sus reglas y su paso a paso, y añadiríamos la vertical a 400, el cambio por contenedor, plegar y la ficha, con su misma disciplina.</p>
</section>"""


def movil():
    return '<p class="aviso-movil">Diagrama ancho: desliza a los lados para verlo entero.</p>'


def pagina():
    pasos = json.dumps(VE_PASOS, ensure_ascii=False)
    d_dd, d_ve, d_cc, d_sf = dd_ciclo(), ve_ciclo(), cc_ciclo(), sf_ciclo()
    medidas = {"dd": len(d_dd), "ve": len(d_ve), "cc": len(d_cc), "sf": len(d_sf) + len(sf_fichas())}
    s = [f"""<!doctype html>
<html lang="es" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Diagramas de flujo comparados</title>
<link rel="stylesheet" href="{FUENTES}">
<style>{CSS}</style></head><body><main>
<div class="cabecera"><h1>Diagramas de flujo comparados</h1><button type="button" id="tema" class="tema" aria-pressed="false">Modo oscuro</button></div>
<p class="intro">El ciclo de vida de una tarea de <a href="../como-funcionan-los-estados.html">Cómo funcionan los estados</a>, dibujado por cada skill candidata a su manera: su disposición, sus formas, sus flechas y su forma de anotar. Cada diagrama va en pareja: a la izquierda, la horizontal de la skill; a la derecha, su versión vertical, o una línea que dice por qué no la tiene. Debajo de cada una, qué más puede hacer, con ejemplos de la propia SF dibujados con sus pautas, y mi opinión. Al final, la síntesis que se propone para la SF y lo que pesa cada opción en tokens. Página de pruebas de la tarea «Actualizar Cómo funcionan los estados» (308). No se ha instalado ninguna skill: se han leído y se han seguido sus pautas a mano.</p>
<nav class="indice"><a href="#dd">diagram-design</a><a href="#dd-fondo">diagram-design: móvil e interacción</a><a href="#ve">visual-explainer</a><a href="#cc">process-flow-diagram</a><a href="#tf">theme-factory</a><a href="#sf">Síntesis para la SF</a><a href="#pesos">Peso en tokens</a></nav>
"""]
    s.append(f"""<section class="skill" id="dd"><h2>diagram-design</h2>
<p class="fuente">cathrynlavery/diagram-design · skills/diagram-design · commit f24d98b · MIT · v2.6 · <a href="https://github.com/cathrynlavery/diagram-design/tree/f24d98b05e2d7a5e68c2dedfe46e5b7173f50118/skills/diagram-design">código</a> · <a href="https://cathrynlavery.github.io/diagram-design/">galería oficial</a> · <a href="https://diagramdesign.dev">web</a></p>
<p class="juicio">Para un ciclo de vida elige el patrón <b>mapa de fases</b>: las fases en un carril horizontal, las vueltas en una banda encima y las salidas en otra debajo. Admite como mucho diez transiciones, así que <b>Revertir</b> pasa a una nota y a un diagrama de detalle. Un solo acento marca el final feliz. La página editorial lleva antetítulo, título con serifa, tres tarjetas de ancho distinto y un pie técnico.</p>
<figure><div class="dd"><p class="eyebrow">Estado · mapa de fases</p><h4 class="t">Ciclo de vida de una tarea</h4>
<p class="subt">Cuatro fases en un carril. Las vueltas atrás las hace Claude y no son fases; cada salida nombra su causa.</p>
{pareja(hz(d_dd), dd_ciclo_v())}
<div class="cards"><div class="card"><p class="eyebrow">Lo principal</p><h5><span class="cd c"></span>Las fases van en un carril</h5><p>Pendientes, En curso, En observación y Cerradas. Cerrar puede saltarse la observación.</p></div>
<div class="card"><h5><span class="cd"></span>Claude solo vuelve atrás</h5><p>Sin trabajo devuelve a Pendientes; Reabrir, a En curso.</p></div>
<div class="card"><h5><span class="cd"></span>Cada salida, su causa</h5><p>Descartar sale de En curso; Eliminar, de Pendientes.</p></div></div>
<div class="foot"><span>DIAGRAM DESIGN · MÁQUINA DE ESTADOS</span><span>6 ESTADOS · 10 TRANSICIONES</span></div></div></figure>
<h3 class="sub">Qué más puede hacer</h3>
<p class="tipos">45 tipos, cada uno con su guía: arquitectura y su versión antes y después, flujo, secuencia, máquina de estados, entidad-relación y esquema de base de datos, línea de tiempo, calles (swimlane), cuadrante, capas, árbol, organigrama, despiece y planta axonométricos, mapa de Wardley, kanban, viaje de usuario, service blueprint, despliegue, grafo de dependencias, UML, story map, Gantt y gráficos de datos. Importa .drawio, Mermaid y .excalidraw, y puede animar si se le pide.</p>
<figure><div class="dd"><p class="eyebrow">Arquitectura · contención</p>{pareja(hz(dd_arquitectura()), dd_arquitectura_v())}</div>
<figcaption class="pie">Mapa de piezas de la SF: zonas que contienen, un foco (el plugin publicado) y flechas con verbo.</figcaption></figure>
<figure><div class="dd"><p class="eyebrow">Secuencia</p><div class="desliza">{dd_secuencia()}</div>{movil()}</div>
<figcaption class="pie">Una petición entre el propietario, el principal, el subagente y la cola. El OK del propietario es el único acento.</figcaption></figure>
<p class="sin-v"><b>Sin vertical:</b> la secuencia ya es vertical, porque el tiempo baja.</p>
<figure><div class="dd"><p class="eyebrow">Línea de tiempo · fases</p>{pareja(hz(dd_fases()), dd_fases_v())}</div>
<figcaption class="pie">Las fases de la metodología, con el foco en una.</figcaption></figure>
<p class="juicio"><b>Fuerte:</b> el oficio. Tiene reglas de flechas que comprueba un script, presupuesto de complejidad, un foco por diagrama, contraste verificado y una piel que se cambia en un archivo. <b>Límites:</b> es grande (45 guías y una configuración la primera vez), dibuja en horizontal a 1000 de ancho, en el móvil obliga a desplazar y no trae interacción, salvo una animación opcional.</p>
<p class="opinion"><b>Mi opinión.</b> Es la mejor de las cuatro dibujando: sus diagramas parecen hechos por alguien que sabe, y sus reglas se pueden comprobar, no solo seguir. Pero es demasiado grande para cargarla entera cada vez (unos 17k tokens para un diagrama de estados), su horizontal choca con nuestra norma de vertical a 560 y su estética de papel gris con naranja es la suya, no la nuestra. La usaría como fuente: me quedaría con sus reglas y su presupuesto, adaptados como propios.</p>
</section>""")
    s.append(dd_fondo())
    s.append(f"""<section class="skill" id="ve"><h2>visual-explainer</h2>
<p class="fuente">nicobailon/visual-explainer · commit 9d5f880 · MIT · v0.15 · <a href="https://github.com/nicobailon/visual-explainer/tree/9d5f880b7e8e0a9a80c890b8e1bb6918b68481ad">código</a> · <a href="https://github.com/nicobailon/visual-explainer/blob/9d5f880b7e8e0a9a80c890b8e1bb6918b68481ad/examples/replay-job-queue.html">ejemplo oficial de replay</a>. Corrección a la vuelta anterior: la versión 0.15 ya dibuja en SVG a mano; la que usaba Mermaid era la copia antigua de jamditis.</p>
<p class="juicio">Para una máquina de estados pide un <b>replay</b>: la máquina entera y un recorrido de un evento por paso, con una frase que dice qué pasó y por qué. Usa el registro <b>Blueprint</b>: retícula de 24, un marco discontinuo con etiqueta monoespaciada para lo que va junto (aquí, lo que está en develop) y llamadas numeradas sobre el dibujo. Hay un solo color, y marca el paso activo.</p>
<figure class="ve-replay" data-pasos='{escape(pasos)}'><div class="ve"><p class="lab">Máquina de estados · replay</p><h4 class="t">Una tarea pasa por develop y puede volver</h4>
{pareja(hz(d_ve), ve_ciclo_v())}
<div class="player"><button type="button" data-go="-1" aria-label="Paso anterior">◀</button><button type="button" data-play aria-label="Reproducir">▶</button><input type="range" min="0" max="{len(VE_PASOS) - 1}" value="0" aria-label="Paso"><button type="button" data-go="1" aria-label="Paso siguiente">▶▶</button><span class="pos"></span></div>
<p class="cap" aria-live="polite"></p>
<figcaption>Lo que está en develop comparte marco: Revertir y Reabrir salen del marco y valen para los dos estados.</figcaption></div></figure>
<h3 class="sub">Qué más puede hacer</h3>
<p class="tipos">Hace páginas enteras cuyo eje son las figuras: arquitectura, flujo de datos, secuencia, esquema y antes y después, con puntos de flujo animados, pasos y replays. También casos como pequeños múltiplos, tablas de auditoría, cifras con barras, gofres o sparklines, figuras vivas con controles, 3D con three.js, presentaciones y vídeo MP4. Con <code>&lt;ve-flow&gt;</code> lee una máquina de estados del código, la recorre entera y marca en el dibujo los estados olvidados y las reglas que se rompen.</p>
<figure><div class="ve"><p class="lab">Arquitectura · puntos de flujo</p>{pareja(hz(ve_arquitectura()), ve_arquitectura_v())}
<figcaption>Flechas con verbo, cilindros para lo que guarda datos y un único nodo clave. Los puntos recorren el camino de escritura y se quedan quietos si el sistema pide reducir el movimiento.</figcaption></div></figure>
<figure><div class="ve"><p class="lab">Pequeños múltiplos · casos</p>
<div class="multiples">
<div class="case"><span class="chip k-ok">ok</span><h6>Cerrar desde En curso</h6>{ve_mini("ok", [("C", "X")], "Cerrar desde En curso")}</div>
<div class="case"><span class="chip k-info">info</span><h6>Cerrar tras observar</h6>{ve_mini("info", [("C", "O"), ("O", "X")], "Cerrar tras observar")}</div>
<div class="case"><span class="chip k-risk">riesgo</span><h6>Revertir una cerrada</h6>{ve_mini("risk", [("X", "P")], "Revertir una cerrada")}</div>
</div><figcaption>El mismo dibujo en cada caso; solo cambia el camino, con el color de su estado.</figcaption></div></figure>
<p class="sin-v"><b>Sin vertical:</b> los pequeños múltiplos ya se apilan en una columna cuando no caben.</p>
<p class="juicio"><b>Fuerte:</b> explica. Tiene replays con su porqué, enlaza el texto con las figuras, pinta cifras y pequeños múltiplos y compara la máquina con el código, algo que encaja con cola.py. <b>Límites:</b> para salir como está pensada depende de su kit y de su renderizador en Node; es más una forma de hacer páginas enteras que un recurso para un documento, y elige la letra (IBM Plex, Instrument Sans…) en cada página.</p>
<p class="opinion"><b>Mi opinión.</b> Es la más inteligente: no solo dibuja, explica, y el replay es justo lo que pedían las croquetas, ver el ciclo moverse con el porqué de cada paso. Su <code>&lt;ve-flow&gt;</code>, que contrasta el dibujo con el código, es la idea más valiosa que he visto para la SF, porque el diagrama de estados dejaría de poder desfasarse de cola.py. Como dependencia no la quiero: trae su kit, su renderizador y su forma de página. Tomaría el replay y las llamadas numeradas, y más adelante la comprobación contra el código.</p>
</section>""")
    s.append(f"""<section class="skill" id="cc"><h2>process-flow-diagram</h2>
<p class="fuente">Cocoon-AI/process-flow-diagram-generator · commit 6e0c72a · MIT · v1.1 · <a href="https://github.com/Cocoon-AI/process-flow-diagram-generator/tree/6e0c72a3b4b46f87ac01ed1291f646bf77beafb0">código</a> · <a href="https://github.com/Cocoon-AI/process-flow-diagram-generator/tree/6e0c72a3b4b46f87ac01ed1291f646bf77beafb0/examples">ejemplos oficiales</a></p>
<p class="juicio">Lo ve como un <b>proceso</b> de izquierda a derecha. Empieza y acaba en píldoras, numera los pasos con el actor encima y usa un rombo para la decisión. Las excepciones van debajo, en rosa discontinuo, y la vuelta continua va por arriba, en cian. Debajo lleva tres tarjetas: prerrequisitos, entradas y salidas, y herramientas. Todo es oscuro y en JetBrains Mono, y fija el ancho para que nada se corte. Para encajar el ciclo en su forma hay que inventar una decisión («¿Sigue?») que el panel no tiene.</p>
<figure><div class="cc"><h4 class="t">Ciclo de vida de una tarea</h4><p class="subt">Proceso · 3 pasos · 1 decisión · excepciones debajo</p>
{pareja(hz(d_cc), cc_ciclo_v(), True, "Horizontal", "Vertical · la skill también la contempla")}
<div class="cards"><div class="card"><h5>PRERREQUISITOS</h5><ul><li>Proyecto incorporado a la SF</li><li>Panel de la SF abierto</li></ul></div>
<div class="card"><h5>ENTRADAS Y SALIDAS</h5><ul><li>Entra: una petición</li><li>Sale: un squash en develop</li></ul></div>
<div class="card"><h5>HERRAMIENTAS</h5><ul><li>cola.py</li><li>git: rama feature/NN-nombre</li></ul></div></div></div></figure>
<h3 class="sub">Qué más puede hacer</h3>
<p class="tipos">Solo flujos de proceso, en tres disposiciones: en línea con decisiones, en varias filas unidas por un conector, y en bucle sin principio ni fin. Exporta a PNG y PDF desde la propia página. La arquitectura es otra skill del mismo autor, <a href="https://github.com/Cocoon-AI/architecture-diagram-generator">architecture-diagram-generator</a>.</p>
<figure><div class="cc">{pareja(hz(cc_bucle()), cc_bucle_v(), True, "Horizontal", "Vertical")}</div>
<figcaption class="pie">Bucle de mejora continua de la SF: la vuelta por arriba, en cian, y el «no», debajo.</figcaption></figure>
<p class="juicio"><b>Fuerte:</b> sus reglas para que un flujo ancho no se corte, y su gramática de excepciones debajo y bucle encima. <b>Límites:</b> solo modo oscuro y solo monoespaciada, los colores neón por defecto que las otras dos prohíben, y solo procesos en línea.</p>
<p class="opinion"><b>Mi opinión.</b> No. Es la estética de «panel técnico oscuro» que todo el mundo reconoce como hecha por una IA, y obliga a meter un ciclo de estados en un proceso en línea, hasta el punto de inventar una decisión. De ella solo salvaría una idea: las excepciones siempre en el mismo sitio (debajo) y las vueltas en otro (encima).</p>
</section>""")
    s.append("""<section class="skill" id="tf"><h2>theme-factory</h2>
<p class="fuente">anthropics/skills · skills/theme-factory · commit ca45fc4 · Apache 2.0 · <a href="https://github.com/anthropics/skills/tree/ca45fc496a3436251f191354091d557da31c15b5/skills/theme-factory">código</a></p>
<p class="una-linea">No da para más: son diez temas de cuatro colores y una letra (DejaVu Sans) para cualquier pieza, sin ninguna pauta de cómo dibujar un diagrama. Lo que aporta ya lo cubren oklch-skill y los temas de crear_documentos. Mi opinión: descartada.</p>
<p class="sin-v"><b>Sin vertical:</b> no dibuja.</p>
</section>""")
    s.append(f"""<section class="skill sf" id="sf"><h2>Síntesis para la SF</h2>
<p class="fuente">Propuesta, no es una skill. Toma la disciplina de diagram-design, el marco y la explicación de visual-explainer y las fichas de las croquetas, con la letra y la paleta de crear_documentos.</p>
<p class="juicio">En vertical, a 560 de ancho, como pide la guía de diagramas, para que se lea en el móvil sin desplazar. Tiene tres carriles con nombre: <b>deshacer</b> a la izquierda, <b>fases</b> en el centro y <b>salida</b> a la derecha. El carril dice qué es cada flecha antes que su color. Los botones del panel son etiquetas con forma de botón, y lo que hace Claude va en cursiva y discontinuo. Hay un foco (En curso, en naranja como en el panel) y un final (Cerradas, en verde), y el rojo oscuro es solo para deshacer. Cada estado se pulsa y abre su ficha con todos sus botones, también los que el dibujo no muestra, como A propuesta.</p>
<div id="sf-ciclo" class="lienzo">{d_sf}<div><p class="vacia">Pulsa un estado para ver su ficha.</p>{sf_fichas()}</div></div>
<p class="sin-v"><b>Sin vertical aparte:</b> ya es vertical, a 560 de ancho.</p>
<p class="opinion"><b>Mi opinión, y lo que elegiría.</b> Haría una skill propia de diagramas de flujo, o un recurso de crear_documentos, con esta síntesis como forma. De <b>diagram-design</b>, adaptado como propio y citando su origen MIT, tomaría las reglas de flechas, el presupuesto de nodos y flechas, un foco por diagrama, la nota para lo que vale «desde cualquier estado» y la comprobación de geometría con script. De <b>visual-explainer</b> tomaría el replay con el porqué de cada paso como modo opcional y, más adelante, la comprobación contra cola.py. Ninguna de las dos como dependencia: cargarlas costaría entre 7k y 21k tokens por diagrama, y la síntesis rondaría los 4k.</p>
</section>""")
    s.append(f"""<section class="skill" id="pesos"><h2>Peso en tokens</h2>
<p class="juicio">Lo que cuesta cargar cada skill para hacer un diagrama de estados (el SKILL.md y las referencias que su propio texto manda leer en ese caso) y lo que ocupa un diagrama típico hecho con ella.</p>
{tabla_pesos(medidas)}
</section>""")
    s.append(f"</main><script>{JS}</script></body></html>")
    return "".join(s), medidas


def main():
    salida = Path(__file__).with_name("diagramas-flujo.html")
    html, medidas = pagina()
    salida.write_text(html, encoding="utf-8")
    print(salida, medidas, len(html))


if __name__ == "__main__":
    main()
