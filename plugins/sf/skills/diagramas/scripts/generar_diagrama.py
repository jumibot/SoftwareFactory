"""Genera un diagrama de la SF a partir de datos breves (skill diagramas): Claude escribe los datos y el programa dibuja.

    python -I -X utf8 generar_diagrama.py <datos.diagrama> [-o salida.html] [--tema tinta] [--fragmento] [--sin-comprobar]

Escribe una página con la figura: su vertical (400) y, si cabe, su horizontal (960), con los mismos ids, cada una con
cajas desplegadas y plegadas, redondeadas y en croqueta (los ajustes «Plegadas» y «Forma» del grupo Cajas eligen cuál se ve); las
fichas en el HUD al pulsar, el resaltado y Escape (assets/diagramas.css y .js, en línea); el tema (tinta por defecto, en
claro y en oscuro) y los ajustes por defecto de la decisión 302. Con --fragmento, solo la <figure>, para pegarla en un documento.
Al acabar pasa comprobar_diagramas.py (a 375 y a 1440, en claro y en oscuro) si hay Playwright.

Tipos: estados, proceso, arquitectura, piezas, secuencia y fases. Formato de los datos: references/datos.md.
Solo la biblioteca estándar de Python 3.9.
"""
import argparse
import json
import re
import subprocess
import sys
from html import escape
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SKILL = AQUI.parent
TEMAS = SKILL.parent / 'crear_documentos' / 'assets' / 'temas'
TIPOS = ('estados', 'proceso', 'arquitectura', 'piezas', 'secuencia', 'fases')
# Ajustes por defecto (decisión 302): encendidos y apagados. Se cambian con «opciones:» en los datos.
# Casillas (la figura lleva d-no-<clave> si está apagada) y selectores (data-d-<clave>); los mismos que la herramienta
# «diagramas» de los documentos (tools/kit_documentos/diagramas.js), que los cambia en todas las figuras a la vez.
# Carriles y chips cambian el dibujo: solo existen si los datos los piden; luego se pueden ocultar.
CASILLAS = {'tarjeta': True, 'color': True, 'notas': True, 'foco': True,
            'resaltado': True, 'fichas': True, 'carriles': False, 'chips': False, 'recuento': False, 'regla': True,
            'letra': False, 'estilos': True}
# «color»: los colores que dan los datos (si no, gris); «estilos»: su cursiva y su discontinua.
# Cajas y forma cambian el dibujo: se dibujan las cuatro variantes y la figura enseña la de sus ajustes.
VARIANTES = {'cajas': ('desplegadas', 'plegadas'), 'forma': ('redondeada', 'croqueta')}
# «acordeon»: el dibujo de las plegadas, con una sola caja desplegada a la vez (diagramas.js).
PLEGADO = ('desplegadas', 'plegadas', 'acordeon')
# Borde y fondo de las cajas: solo CSS, sobre el mismo dibujo.
SELECTORES = {'cajas': PLEGADO, 'forma': VARIANTES['forma'], 'borde': ('fino', 'ninguno', 'grueso'), 'fondo': ('papel', 'ninguno', 'tintado'),
              'orientacion': ('auto', 'vertical', 'horizontal'), 'antetitulo': ('oculto', 'encima', 'lado'),
              'titulo': ('sans', 'serifa', 'serifa-p', 'mono', 'oculto'), 'desc': ('linea', 'completa', 'corta', 'oculta'),
              'pie': ('dos', 'izquierda', 'derecha', 'centrado', 'oculto'), 'ayuda': ('encima', 'debajo', 'discreta', 'oculta'),
              'recorrido': ('segundo', 'acento', 'grueso'), 'lienzo': ('papel', 'ninguno', 'tintado'),
              # Flechas y etiquetas: grosor del trazo (fino, el de diagram-design), punta y esquinas de los codos.
              'grosor': ('fino', 'normal', 'grueso'), 'punta': ('llena', 'abierta', 'ninguna'), 'esquinas': ('redondeadas', 'rectas'),
              # Notas: recuadro, fondo, tamaño, ubicación (en el hueco libre de la horizontal, debajo o en una columna al
              # lado; en la vertical, siempre debajo) y cabecera.
              'recuadro': ('sin', 'fino', 'barra'), 'fondo-nota': ('tintado', 'papel', 'ninguno'),
              'tamano-nota': ('normal', 'compacto', 'amplio'), 'lugar-nota': ('hueco', 'debajo', 'lado'),
              'cabecera-nota': ('mono', 'negrita'), 'detalle': ('sans', 'mono')}
# Tamaños de las notas: antetítulo (cabecera), texto y relleno; se dibujan los tres y se ve el del ajuste.
TAM_NOTA = {'compacto': (7, 9, 8), 'normal': (8, 10, 10), 'amplio': (9, 11.5, 12)}
ANCHO_LADO = 200                                   # la columna de las notas al lado de la horizontal
POR_DEFECTO = {**CASILLAS, **{k: v[0] for k, v in SELECTORES.items()}}
CLASES_NODO = {'foco', 'salida', 'final', 'externo', 'fin', 'dec'}
BOTONES = {'verde': ('#15803d', '#4ade80'), 'rojo': ('#c81e1e', '#f87171'), 'morado': ('#9333ea', '#c084fc')}
# Colores que los datos pueden dar a una etiqueta (color=X o X sola) o a una línea (linea=X): los del tema y estos tres.
COLORES = ('acento', 'segundo', 'gris') + tuple(BOTONES)

# ── medidas (unidades del SVG) ──
ANCHO = {'v': 400, 'h': 960}
# La letra de diagram-design (output-spec, «Type ramp», standard): nombre 12 (Geist 600), detalle 9, etiqueta de flecha y
# antetítulo 8 (Geist Mono); el texto de las notas, 10 (anotación densa, 7 a 11). Lo que hace Claude, 12 en cursiva de
# serifa. La horizontal se dibuja así. La vertical se ve al 86 % (400 en 375 px): va un 7/6 mayor, para que en el móvil
# se lea al tamaño de la original. Las medidas que dependen de la letra (pasos de línea, altos) la siguen.
LETRA = {'h': 1, 'v': 7 / 6}
K_SANS, K_NEGRITA, K_MONO, K_CURSIVA = .52, .58, .6, .46   # medidos con Geist e Instrument Serif, con margen para la letra de reserva


def ancho_texto(t, fs, k=K_SANS):
    return len(t) * fs * k


def envolver(t, w, fs, k=K_SANS):
    """Parte un texto en las líneas que hagan falta para que quepa en w (las notas)."""
    lineas = []
    for pal in t.split():
        if lineas and ancho_texto(lineas[-1] + ' ' + pal, fs, k) <= w:
            lineas[-1] += ' ' + pal
        elif ancho_texto(pal, fs, k) <= w:
            lineas.append(pal)
        else:
            raise Error(f'«{pal}» no cabe en {w:.0f} de ancho: acórtalo')
    return lineas or ['']


def cabecera_nota(t):
    """La cabecera, en minúsculas con la primera mayúscula si viene toda en mayúsculas: la mono la pone en mayúsculas
    con CSS, y la negrita la deja así."""
    return t[:1] + t[1:].lower() if t.upper() == t else t


def notas_svg(m, o, w, x=8, y=8, pref=''):
    """Las notas en un ancho w, en sus tres tamaños (data-tam): (marcado de cada tamaño, alto de cada uno)."""
    e = LETRA[o]
    grupos, altos = {}, {}
    for tam, (fe, fx, pad) in TAM_NOTA.items():
        fe, fx, pad = round(fe * e * 2) / 2, round(fx * e * 2) / 2, round(pad * e)
        yy, o_ = y, []
        for cab, txt in m['notas']:
            cabs = envolver(cab, w - 24, fe, K_MONO)
            lineas = envolver(txt, w - 24, fx)
            pc, pt = round(fe * 1.5), round(fx * 1.45)
            y1 = pad + fe
            yt = y1 + pc * (len(cabs) - 1) + fx + pad * .8
            h = yt + pt * (len(lineas) - 1) + pad
            g = [f'<g class="d-nota"><rect class="d-nota-c" x="{x:g}" y="{yy:g}" width="{w:g}" height="{h:g}" rx="4"/>'
                 f'<rect class="d-nota-b" x="{x:g}" y="{yy:g}" width="3" height="{h:g}"/>']
            g += [f'<text class="d-nota-t d-etiqueta" x="{x + 12:g}" y="{yy + y1 + pc * i:g}" font-size="{fe}">{escape(cabecera_nota(t))}</text>' for i, t in enumerate(cabs)]
            g += [f'<text class="d-nota-x" x="{x + 12:g}" y="{yy + yt + pt * i:g}" font-size="{fx}">{escape(t)}</text>' for i, t in enumerate(lineas)]
            o_.append(''.join(g) + '</g>')
            yy += h + 8
        grupos[tam], altos[tam] = ''.join(o_), yy - 8 - y
    return grupos, altos


class Error(Exception):
    pass


def color_boton(m, fl, t):
    """El color de la etiqueta: el que le den sus datos (ninguno por defecto)."""
    return fl.get('color', '')


# ───────────────────────── datos ─────────────────────────

def leer(texto):
    """Formato breve: «clave: valor» arriba; secciones («nodos:», «flechas:»…) con una entrada por línea sangrada; en
    «fichas:», las líneas de cada ficha van debajo con «- ». Las # empiezan un comentario."""
    d, seccion, ultima = {}, None, None
    for n, linea in enumerate(texto.splitlines(), 1):
        if not linea.strip() or linea.lstrip().startswith('#'):
            continue
        sangria = len(linea) - len(linea.lstrip())
        s = linea.strip()
        if sangria == 0:
            m = re.match(r'([\w-]+):\s*(.*)$', s)
            if not m:
                raise Error(f'línea {n}: se esperaba «clave: valor» ({s})')
            clave, valor = m.groups()
            if valor:
                d[clave] = valor
                seccion = None
            else:
                seccion = clave
                d[clave] = []
            continue
        if seccion is None:
            raise Error(f'línea {n}: entrada sangrada fuera de una sección')
        if s.startswith('- '):
            if not ultima:
                raise Error(f'línea {n}: «- » sin entrada encima')
            ultima['lineas'].append(s[2:].strip())
            continue
        ultima = {'texto': s, 'lineas': [], 'n': n}
        d[seccion].append(ultima)
    return d


def campos(t):
    return [x.strip() for x in t.split('|')]


def modelo(d):
    tipo = d.get('tipo', '')
    if tipo not in TIPOS:
        raise Error(f'tipo «{tipo}» desconocido; tipos: {", ".join(TIPOS)}')
    m = {'tipo': tipo, 'titulo': d.get('titulo', ''), 'descripcion': d.get('descripcion', ''),
         'antetitulo': d.get('antetitulo', tipo.upper()), 'pie': campos(d.get('pie', '')) if d.get('pie') else [],
         'foco': d.get('foco', ''), 'nodos': {}, 'orden': [], 'flechas': [], 'notas': [], 'zonas': [], 'fichas': {},
         'opciones': dict(POR_DEFECTO)}
    for o in [x.strip() for x in d.get('opciones', '').split(',') if x.strip()]:
        if '=' in o:
            k, v = [y.strip() for y in o.split('=', 1)]
            m['opciones'][k] = v
        else:
            no = o.startswith('sin ')
            k = o[4:] if no else o
            if k in SELECTORES:  # «antetitulo» o «sin ayuda»: el primer valor que se ve, o el oculto
                m['opciones'][k] = SELECTORES[k][-1] if no else next(x for x in SELECTORES[k] if x not in ('oculto', 'oculta', 'auto'))
            else:
                m['opciones'][k] = not no
    for k, v in m['opciones'].items():
        if k not in POR_DEFECTO:
            raise Error(f'opción «{k}» desconocida; opciones: {", ".join(POR_DEFECTO)}')
        if k in SELECTORES and v not in SELECTORES[k]:
            raise Error(f'«{k}={v}» no vale; valores: {", ".join(SELECTORES[k])}')
    for e in d.get('nodos', d.get('actores', [])):
        mm = re.match(r'([\w-]+):\s*(.*)$', e['texto'])
        if not mm:
            raise Error(f'línea {e["n"]}: nodo sin id («id: Nombre | detalle | clases»)')
        nid, resto = mm.groups()
        f = campos(resto)
        nodo = {'id': nid, 'nombre': f[0], 'sub': '', 'clases': set(), 'chip': ''}
        for x in f[1:]:
            if x.startswith('chip='):
                nodo['chip'] = x[5:]
            elif x in CLASES_NODO:
                nodo['clases'].add(x)
            elif x and not nodo['sub']:
                nodo['sub'] = x
            elif x:
                raise Error(f'línea {e["n"]}: «{x}» no es una clase de nodo ({", ".join(sorted(CLASES_NODO))})')
        if nid == m['foco']:
            nodo['clases'].add('foco')
        m['nodos'][nid] = nodo
        m['orden'].append(nid)
    for e in d.get('flechas', d.get('mensajes', [])):
        mm = re.match(r'([\w-]+)\s*>\s*([\w-]+)\s*(?::\s*(.*))?$', e['texto'])
        if not mm:
            raise Error(f'línea {e["n"]}: flecha mal escrita («de > a: ETIQUETA | color | claude»)')
        de, a, resto = mm.groups()
        f = campos(resto or '')
        fl = {'de': de, 'a': a, 'etiqueta': f[0] if f else '', 'clases': set(x for x in f[1:] if x and '=' not in x),
              'estado': next((x[7:] for x in f[1:] if x.startswith('estado=')), '')}
        # Marcas genéricas: color de la etiqueta (color=X o X), de la línea (linea=X), cursiva, discontinua y vuelta
        # (discontinua y, entre vecinas hacia atrás, por encima). «claude» es un atajo de estilo: cursiva y vuelta. «principal»: línea en acento.
        for x in f[1:]:
            k, _, v = x.partition('=')
            if k in ('color', 'linea'):
                if v not in COLORES:
                    raise Error(f'línea {e["n"]}: color «{v}» desconocido; colores: {", ".join(COLORES)}')
                fl[k] = v
        fl['color'] = fl.get('color') or next((x for x in fl['clases'] if x in COLORES), '')
        if 'principal' in fl['clases']:
            fl.setdefault('linea', 'acento')
        if 'claude' in fl['clases']:
            fl['clases'] |= {'cursiva', 'vuelta'}
        for x in (de, a):
            if x != 'inicio' and x not in m['nodos']:
                raise Error(f'línea {e["n"]}: «{x}» no es ningún nodo')
        m['flechas'].append(fl)
    for e in d.get('notas', []):
        cab, _, txt = e['texto'].partition(':')
        m['notas'].append((cab.strip(), txt.strip()))
    for e in d.get('zonas', []):
        mm = re.match(r'([\w-]+):\s*(.*)$', e['texto'])
        nombre, _, ids = (mm.group(2) if mm else e['texto']).partition('|')
        ids = [x.strip() for x in ids.split(',') if x.strip()]
        for x in ids:
            if x not in m['nodos']:
                raise Error(f'línea {e["n"]}: la zona nombra «{x}», que no es ningún nodo')
        m['zonas'].append((nombre.strip(), ids))
    for e in d.get('fichas', []):
        fid, _, resumen = e['texto'].partition(':')
        m['fichas'][fid.strip()] = (resumen.strip(), e['lineas'])
    if len(m['nodos']) > 9:
        print(f'Aviso: {len(m["nodos"])} nodos; el presupuesto es 9. ¿Dos diagramas?', file=sys.stderr)
    if len(m['flechas']) > 12:
        print(f'Aviso: {len(m["flechas"])} flechas; el presupuesto es 12.', file=sys.stderr)
    return m


# ───────────────────────── geometría ─────────────────────────

class R:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    @property
    def r(self):
        return self.x + self.w

    @property
    def b(self):
        return self.y + self.h

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    def mas(self, m):
        return R(self.x - m, self.y - m, self.w + 2 * m, self.h + 2 * m)

    def corta(self, o):
        return min(self.r, o.r) > max(self.x, o.x) and min(self.b, o.b) > max(self.y, o.y)


def seg_rect(a, b, m=0):
    (x1, y1), (x2, y2) = a, b
    return R(min(x1, x2) - m, min(y1, y2) - m, abs(x2 - x1) + 2 * m, abs(y2 - y1) + 2 * m)


def codo(puntos, r=8):
    """Camino ortogonal con codos redondeados de radio r."""
    p = puntos
    d = [f'M{p[0][0]:g},{p[0][1]:g}']
    for i in range(1, len(p) - 1):
        (xa, ya), (xb, yb), (xc, yc) = p[i - 1], p[i], p[i + 1]
        s1 = ((xb > xa) - (xb < xa), (yb > ya) - (yb < ya))
        s2 = ((xc > xb) - (xc < xb), (yc > yb) - (yc < yb))
        q = min(r, abs(xb - xa) / 2 + abs(yb - ya) / 2, abs(xc - xb) / 2 + abs(yc - yb) / 2)
        d.append(f'L{xb - s1[0] * q:g},{yb - s1[1] * q:g} Q{xb:g},{yb:g} {xb + s2[0] * q:g},{yb + s2[1] * q:g}')
    d.append(f'L{p[-1][0]:g},{p[-1][1]:g}')
    return ' '.join(d)


# ───────────────────────── lienzo ─────────────────────────

class Lienzo:
    def __init__(self, m, o, cajas='desplegadas', forma='redondeada'):
        self.m, self.o = m, o                      # o: 'v' u 'h'
        self.W = ANCHO[o]
        e = self.escala = LETRA[o]
        medio = lambda v: round(v * e * 2) / 2
        self.fn, self.fs, self.fe, self.fc, self.fx = medio(12), medio(9), medio(8), medio(12), medio(10)
        self.pn, self.ps = round(15 * e), round(13 * e)   # de la línea del nombre a la del detalle, y entre detalles
        self.variante = (cajas, forma)
        self.plegadas, self.croqueta = cajas == 'plegadas', forma == 'croqueta'
        # Cajas de diagram-design: 48 de alto mínimo (plegada, solo el nombre), 56 con una línea de detalle; con chips de
        # tipo, 16 más arriba para el chip, como sus cajas de 72.
        self.chips = any(n['chip'] for n in m['nodos'].values())
        extra = 16 if self.chips else 0
        self.alto0, self.alto1 = round((48 + extra) * e), round((56 + extra) * e)
        self.alto = self.alto0 if self.plegadas else self.alto1
        self.pad = 44 if self.croqueta else 32     # la croqueta, con los extremos redondos, pide más ancho
        sufijo = ('-p' if self.plegadas else '') + ('-c' if self.croqueta else '')
        self.pref = f'{m["id"]}-{o}{sufijo}'
        self.fondo, self.flechas, self.etiquetas, self.nodos = [], [], [], []
        self.plegar = []                           # el circulito de cada caja que se pliega sola
        self.cajas = {}                            # id → R
        self.radio = {}                            # id → radio de sus esquinas (para que las flechas toquen el borde)
        self.obst, self.segs = [], []              # obstáculos para las etiquetas
        self.H = 0
        self.hueco = True                          # las notas pueden ir en el hueco libre de la horizontal
        self.notas_dentro = False

    # nodos
    def nodo(self, nid, rc):
        n = self.m['nodos'][nid]
        self.cajas[nid] = rc
        self.obst.append(rc)
        if 'final' in n['clases']:
            cx, cy = rc.cx, rc.y + 10
            o = [f'<g data-nodo="{nid}" class="d-nodo d-final"><rect class="d-caja d-toque" x="{rc.x:g}" y="{rc.y:g}" width="{rc.w:g}" height="{rc.h:g}"/>'
                 f'<circle class="d-fin-a" cx="{cx:g}" cy="{cy:g}" r="8"/><circle class="d-fin" cx="{cx:g}" cy="{cy:g}" r="4"/>']
            for i, t in enumerate(self.partir(n['nombre'], rc.w, self.fc, K_CURSIVA)):
                o.append(f'<text class="d-cl" x="{cx:g}" y="{cy + 12 + self.fc + round(self.fc * 1.4) * i:g}" font-size="{self.fc}" text-anchor="middle">{escape(t)}</text>')
            self.nodos.append(''.join(o) + '</g>')
            return
        clases = ' '.join(sorted(n['clases'] & {'foco', 'salida', 'externo', 'fin', 'dec'}))
        if 'dec' in n['clases']:
            forma = (f'<polygon class="d-caja" points="{rc.x:g},{rc.cy:g} {rc.x + 18:g},{rc.y:g} {rc.r - 18:g},{rc.y:g} '
                     f'{rc.r:g},{rc.cy:g} {rc.r - 18:g},{rc.b:g} {rc.x + 18:g},{rc.b:g}"/>')
        else:
            rx = min(rc.h, rc.w) / 2 if self.croqueta else 6
            self.radio[nid] = rx
            forma = f'<rect class="d-caja" x="{rc.x:g}" y="{rc.y:g}" width="{rc.w:g}" height="{rc.h:g}" rx="{rx:g}"/>'
        margen = 16 + (12 if self.croqueta else 0)
        # el chip de tipo, dentro de la caja arriba a la izquierda (7 en mono, como diagram-design): x, y, ancho, alto
        fch = round(7 * self.escala * 2) / 2
        chip = (rc.x + 8 + (self.radio.get(nid, 6) - 6) * .45, rc.y + 8, ancho_texto(n['chip'], fch, K_MONO + .1) + 12, fch + 8) if n['chip'] else None
        if ancho_texto(n['nombre'], self.fn, K_NEGRITA) > rc.w - margen:
            raise Error(f'el nombre «{n["nombre"]}» no cabe en su caja: acórtalo')
        # El detalle va siempre en el marcado: en las plegadas, oculto, para que una caja se despliegue sola en su sitio.
        subs = self.partir(n['sub'], rc.w - margen - 8, self.fs, K_MONO) if n['sub'] else []
        alto = self.fn + (self.pn + self.ps * (len(subs) - 1) if subs and not self.plegadas else 0)
        y = rc.cy - alto / 2 + self.fn * .8
        if subs and 'dec' not in n['clases']:
            hd = rc.h if not self.plegadas else self.alto1 + self.ps * (len(subs) - 1)
            hp = self.alto0 if not self.plegadas else rc.h
            forma = forma.replace('<rect class="d-caja" ', f'<rect class="d-caja" data-hd="{hd:g}" data-hp="{hp:g}" data-pn="{self.pn}" data-ps="{self.ps}" ', 1)
            k = 11 + (self.radio.get(nid, 6) - 6) * .2          # en la croqueta, un poco más adentro de la curva
            px, py = rc.x + k, rc.y + k
            # con el chip a la vista, a su derecha (CSS lo mueve con translate; sin chip, en la esquina)
            mov = f' style="--dx:{chip[0] + chip[2] + 10 - px:.1f}px; --dy:{chip[1] + chip[3] / 2 - py:.1f}px"' if n['chip'] else ''
            self.plegar.append(f'<g class="d-plegar" data-plegar="{nid}"{mov}><circle class="d-plegar-t" cx="{px:g}" cy="{py:g}" r="15"/>'
                               f'<circle class="d-plegar-p" cx="{px:g}" cy="{py:g}" r="3.5"/></g>')
        o = [f'<g data-nodo="{nid}" class="d-nodo {clases}{" d-con-chip" if n["chip"] else ""}">{forma}']
        if n['chip']:
            o.append(f'<g class="d-chip-g"><rect class="d-chip-c" x="{chip[0]:g}" y="{chip[1]:g}" width="{chip[2]:.1f}" height="{chip[3]:g}" rx="2"/>'
                     f'<text class="d-chip" x="{chip[0] + 6:g}" y="{chip[1] + chip[3] / 2 + fch * .36:.1f}" font-size="{fch}">{escape(n["chip"])}</text></g>')
        o.append(f'<text class="d-nn" x="{rc.cx:g}" y="{y:.1f}" font-size="{self.fn}" text-anchor="middle">{escape(n["nombre"])}</text>')
        for i, s in enumerate(subs):
            oculto = ' d-plegado' if self.plegadas else ''
            o.append(f'<text class="d-sb{oculto}" x="{rc.cx:g}" y="{y + self.pn + self.ps * i:.1f}" font-size="{self.fs}" text-anchor="middle">{escape(s)}</text>')
        if 'fin' in n['clases']:
            o.append(f'<circle class="d-fin-a" cx="{rc.r - 14:g}" cy="{rc.y + 14:g}" r="6"/><circle class="d-fin" cx="{rc.r - 14:g}" cy="{rc.y + 14:g}" r="3"/>')
        self.nodos.append(''.join(o) + '</g>')

    def partir(self, t, w, fs, k=K_SANS):
        """Parte un texto en líneas que quepan en w; dos como mucho."""
        if ancho_texto(t, fs, k) <= w:
            return [t]
        pal = t.split()
        cortes = [(' '.join(pal[:i]), ' '.join(pal[i:])) for i in range(1, len(pal))]
        cortes = [c for c in cortes if all(ancho_texto(x, fs, k) <= w for x in c)]
        lineas = list(min(cortes, key=lambda c: abs(len(c[0]) - len(c[1])))) if cortes else []
        if not lineas:
            raise Error(f'«{t}» no cabe en {w:.0f} de ancho: acórtalo')
        return lineas

    def medida_nodo(self, nid, minimo=0, sub=True):
        n = self.m['nodos'][nid]
        fin = 24 if 'fin' in n['clases'] else 0      # sitio para la marca de fin, arriba a la derecha
        return max(minimo, ancho_texto(n['nombre'], self.fn, K_NEGRITA) + self.pad + fin,
                   ancho_texto(n['sub'], self.fs, K_MONO) + self.pad if n['sub'] and sub else 0)

    def lineas_sub(self, nid, w):
        n = self.m['nodos'][nid]
        return len(self.partir(n['sub'], w - self.pad + 8, self.fs, K_MONO)) if n['sub'] else 1

    def contacto(self, nid, p, q, hueco):
        """El extremo p de una flecha (en el borde de la caja nid, o a «hueco» de él), corrido hasta el borde de verdad
        si cae en una esquina redondeada: así toca también la croqueta. q es el punto vecino del camino."""
        c, r = self.cajas.get(nid), self.radio.get(nid, 0)
        if not c or r <= 0:
            return p
        x, y = p

        def dentro(v, a, b):            # cuánto se mete el borde redondeado en la posición v de un lado de a a b
            d = (a + r - v) if v < a + r else (v - (b - r)) if v > b - r else 0
            d = min(max(d, 0), r)
            return r - (r * r - d * d) ** .5

        if q[0] == x and q[1] != y:     # tramo vertical: entra por arriba o por abajo
            if q[1] < y and abs(y - (c.y - hueco)) <= 1:
                return (x, c.y + dentro(x, c.x, c.r) - hueco)
            if q[1] > y and abs(y - (c.b + hueco)) <= 1:
                return (x, c.b - dentro(x, c.x, c.r) + hueco)
        elif q[1] == y:                 # tramo horizontal: por la izquierda o por la derecha
            if q[0] < x and abs(x - (c.x - hueco)) <= 1:
                return (c.x + dentro(y, c.y, c.b) - hueco, y)
            if q[0] > x and abs(x - (c.r + hueco)) <= 1:
                return (c.r - dentro(y, c.y, c.b) + hueco, y)
        return p

    # flechas
    def flecha(self, fl, puntos, etiqueta=True):
        clases = ['d-fl']
        if fl.get('linea'):
            clases.append(f'd-l-{fl["linea"]}')
        if fl['clases'] & {'discontinua', 'previsto', 'vuelta'}:
            clases.append('d-discontinua')
        if 'principal' in fl['clases']:
            clases.append('d-principal')
        puntos = list(puntos)
        if fl['de'] != 'inicio':
            puntos[0] = self.contacto(fl['de'], puntos[0], puntos[1], 0)
        puntos[-1] = self.contacto(fl['a'], puntos[-1], puntos[-2], 2)
        punta = '' if 'sin-punta' in fl['clases'] else f' marker-end="url(#{self.pref}-m)"'
        de = f' data-de="{fl["de"]}" data-a="{fl["a"]}"' if fl['de'] != 'inicio' else ''
        recto = 'M' + ' L'.join(f'{x:g},{y:g}' for x, y in puntos)
        da = f' data-da="{recto}"' if len(puntos) > 2 else ''
        self.flechas.append(f'<path class="{" ".join(clases)}"{de} d="{codo(puntos)}"{da} fill="none"{punta}/>')
        for a, b in zip(puntos, puntos[1:]):
            self.segs.append((a, b))
        if etiqueta and fl['etiqueta']:
            self.pendientes.append((fl, puntos))

    def etiqueta(self, fl, puntos):
        t = fl['etiqueta']
        claude = 'cursiva' in fl['clases']
        w = self.ancho_etq(fl)
        h = self.fe + 8
        tramos = sorted(zip(puntos, puntos[1:]), key=lambda s: -(abs(s[1][0] - s[0][0]) + abs(s[1][1] - s[0][1])))
        for a, b in tramos:
            vertical = a[0] == b[0]
            largo = abs(b[1] - a[1]) if vertical else abs(b[0] - a[0])
            for t_ in (.5, .3, .7, .2, .8):
                px, py = a[0] + (b[0] - a[0]) * t_, a[1] + (b[1] - a[1]) * t_
                if vertical:
                    if largo < h + 16:
                        continue
                    cands = [R(px + 8, py - h / 2, w, h), R(px - 8 - w, py - h / 2, w, h)]
                else:
                    x1 = min(a[0], b[0])
                    cands = [R(px - w / 2, py - 8 - h, w, h), R(px - w / 2, py + 8, w, h)] if largo >= w + 16 else []
                    x2 = max(a[0], b[0])
                    cands += [R(x1 + 8, py + 8, w, h), R(x1 + 8, py - 8 - h, w, h), R(x2 - 8 - w, py + 8, w, h), R(x2 - 8 - w, py - 8 - h, w, h)]
                for c in cands:
                    if self.libre(c):
                        self.pon_etiqueta(fl, t, c, claude)
                        return
        raise Error(f'no hay sitio para la etiqueta «{t}» ({fl["de"]} > {fl["a"]}) en la {"vertical" if self.o == "v" else "horizontal"}: '
                    'acórtala, quita una flecha o pásala a una nota')

    def ancho_etq(self, fl):
        """Ancho de la máscara de una etiqueta: mono de 8, o la de Claude (la cursiva es más estrecha: con la medida de la
        recta cabe también sin ella)."""
        if not fl['etiqueta']:
            return 0
        claude = 'cursiva' in fl['clases']
        return ancho_texto(fl['etiqueta'], self.fc if claude else self.fe, K_SANS if claude else K_MONO) + 8

    def libre(self, c):
        if c.x < 4 or c.r > self.W - 4 or c.y < 4 or c.b > self.H - 4:
            return False
        if any(c.corta(o.mas(4)) for o in self.obst):
            return False
        return not any(c.corta(seg_rect(a, b, 5.5)) for a, b in self.segs)

    def pon_etiqueta(self, fl, t, c, claude):
        self.obst.append(c.mas(6))    # dos etiquetas, bien separadas: que no se lean como una
        color = color_boton(self.m, fl, t)
        cl = ('d-cl' if claude else 'd-etiqueta') + (f' d-b-{color}' if color else '')
        de = f' data-de="{fl["de"]}" data-a="{fl["a"]}"' if fl['de'] != 'inicio' else ''
        self.etiquetas.append(f'<g class="d-et"{de}><rect class="d-mascara" x="{c.x:g}" y="{c.y:g}" width="{c.w:g}" height="{c.h:g}" rx="2"/>'
                              f'<text class="{cl}" x="{c.x + 4:g}" y="{c.cy + (self.fc if claude else self.fe) * .36:.1f}" font-size="{self.fc if claude else self.fe}">{escape(t)}</text></g>')

    def notas(self, y, x=None, w=None):
        """Las notas «desde varios estados». Debajo del dibujo van en su propio svg (notas_svg, en figura): aquí solo se
        deja el margen. Con x y w, en el hueco libre del dibujo, en sus tres tamaños. Devuelve dónde acaban (el amplio)."""
        if x is None or not self.m['notas']:
            return y - 16
        grupos, altos = notas_svg(self.m, self.o, w, x, y)
        self.fondo += [f'<g class="d-notas-g" data-tam="{t}">{g}</g>' for t, g in grupos.items()]
        self.obst.append(R(x, y, w, altos['amplio']))
        self.notas_dentro = True
        return y + altos['amplio'] + 8

    def carril(self, x, y, w, nombre):
        if self.m['opciones']['carriles']:
            self.fondo.append(f'<g class="d-carril-g"><text class="d-carril d-etiqueta" x="{x:g}" y="{y:g}" font-size="{self.fe}">{escape(nombre)}</text>'
                              f'<line class="d-regla" x1="{x:g}" y1="{y + 6:g}" x2="{x + w:g}" y2="{y + 6:g}"/></g>')
            self.obst.append(R(x, y - self.fe, w, self.fe + 8))

    def zona(self, rc, nombre, derecha=False):
        w = ancho_texto(nombre, self.fe, K_MONO) + 8
        x = rc.r - 8 - w if derecha else rc.x + 8
        self.fondo.append(f'<rect class="d-zona" x="{rc.x:g}" y="{rc.y:g}" width="{rc.w:g}" height="{rc.h:g}" rx="8"/>'
                          f'<text class="d-carril d-etiqueta" x="{x + 4:g}" y="{rc.y + 20:g}" font-size="{self.fe}">{escape(nombre)}</text>')
        self.obst.append(R(x, rc.y + 6, w, 20))
        for a, b in (((rc.x, rc.y), (rc.r, rc.y)), ((rc.r, rc.y), (rc.r, rc.b)), ((rc.x, rc.b), (rc.r, rc.b)), ((rc.x, rc.y), (rc.x, rc.b))):
            self.segs.append((a, b))

    def svg(self, clase, aria):
        p = self.pref
        defs = (f'<defs><marker id="{p}-m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8.4" markerHeight="8.4" markerUnits="userSpaceOnUse" orient="auto-start-reverse">'
                f'<path d="M0,1 L10,5 L0,9 z" class="d-punta d-pl"/><path d="M0,0.5 L10,5 L0,9.5 L0,7.6 L6.2,5 L0,2.4 z" class="d-punta d-pa"/></marker>'
                f'<marker id="{p}-m-on" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8.4" markerHeight="8.4" markerUnits="userSpaceOnUse" orient="auto-start-reverse">'
                f'<path d="M0,1 L10,5 L0,9 z" class="d-punta-on d-pl"/><path d="M0,0.5 L10,5 L0,9.5 L0,7.6 L6.2,5 L0,2.4 z" class="d-punta-on d-pa"/></marker></defs>')
        cuerpo = ''.join(self.fondo + self.flechas + self.etiquetas + self.nodos + self.plegar)
        return (f'<svg class="{clase}" viewBox="0 0 {self.W} {self.H:g}" style="--d-fe:{self.fe}px" role="img" aria-labelledby="{p}-t {p}-d">'
                f'<title id="{p}-t">{escape(self.m["titulo"] or self.m["tipo"])}</title><desc id="{p}-d">{escape(aria)}</desc>{defs}{cuerpo}</svg>')

    def acabar(self):
        # primero las flechas cortas, que tienen menos sitio donde poner su etiqueta; las largas, después
        largo = lambda pts: sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(pts, pts[1:]))
        for fl, puntos in sorted(self.pendientes, key=lambda x: largo(x[1])):
            self.etiqueta(fl, puntos)


# ───────────────────────── maquetaciones ─────────────────────────

def principales(m):
    return [n for n in m['orden'] if not m['nodos'][n]['clases'] & {'salida', 'final'}]


def columna(m, L):
    """Vertical para estados, proceso, arquitectura y piezas: el camino en una columna; las vueltas largas, por carriles
    a la derecha; las salidas, en una segunda columna, un poco por debajo de su origen."""
    L.pendientes = []
    prin = principales(m)
    lados = [n for n in m['orden'] if n not in prin]
    pos = {n: i for i, n in enumerate(prin)}
    pares = {(f['de'], f['a']) for f in m['flechas']}
    vecinas = [f for f in m['flechas'] if f['de'] in pos and f['a'] in pos and abs(pos[f['a']] - pos[f['de']]) == 1]
    largas = [f for f in m['flechas'] if f['de'] in pos and f['a'] in pos and abs(pos[f['a']] - pos[f['de']]) > 1]
    a_lado = [f for f in m['flechas'] if f['de'] != 'inicio' and (f['de'] in lados or f['a'] in lados)]
    zona_de = {n: z for z, (_, ids) in enumerate(m['zonas']) for n in ids}
    x0 = 24 if m['zonas'] else 16
    wcol = max(160, max(L.medida_nodo(n) for n in prin))
    if not lados and not largas:
        wcol = max(wcol, 240)
    dobles = set()
    for f in vecinas:   # ida y vuelta entre vecinos: cada etiqueta, dentro de la columna, una más arriba que la otra
        if (f['a'], f['de']) in pares and f['etiqueta']:
            wcol = max(wcol, L.ancho_etq(f) + 64)
            dobles.add(min(pos[f['de']], pos[f['a']]))
    wcol = min(wcol, L.W - 2 * x0)
    carriles_x = [x0 + wcol + 16 + 16 * k for k in range(len(largas))]
    xl = (carriles_x[-1] + 24) if carriles_x else x0 + wcol + 32
    wl = L.W - 16 - xl
    pide = max([ancho_texto(m['nodos'][n]['nombre'], L.fn, K_NEGRITA) + (32 if L.croqueta else 20) for n in lados if 'final' not in m['nodos'][n]['clases']] + [100])
    if lados and wl < pide:
        raise Error(f'las salidas no caben al lado del camino en la vertical ({wl:.0f} < {pide:.0f}): '
                    'menos vueltas largas o nombres más cortos')
    y = 16
    if m['opciones']['carriles']:
        L.carril(x0, 28, wcol, 'CAMINO')
        if lados:
            L.carril(xl, 28, wl, 'SALIDAS')
        y = 44
    if any(f['de'] == 'inicio' for f in m['flechas']):
        y += 44
    alto = L.alto
    zona_act, y_zona, zonas_rc = None, None, []
    for i, n in enumerate(prin):
        z = zona_de.get(n)
        if z != zona_act:
            if zona_act is not None:
                zonas_rc.append((zona_act, y_zona, y - 8))
                y += 24
            if z is not None:
                y_zona = y - 8
                y += 32
            zona_act = z
        L.nodo(n, R(x0, y, wcol, alto))
        y += alto + (104 if i in dobles else 60)
    y_fin = y - 60
    if zona_act is not None:
        zonas_rc.append((zona_act, y_zona, y_fin + 16))
    for z, ya, yb in zonas_rc:
        L.zona(R(8, ya, L.W - 16, yb - ya), m['zonas'][z][0], derecha=True)
    # salidas: en la segunda columna, 52 por debajo de su origen (o de la siguiente que quede libre)
    libre_desde = 0

    def origen_de(n):
        return next((f['de'] for f in m['flechas'] if f['a'] == n and f['de'] in pos), None) or \
            next((f['a'] for f in m['flechas'] if f['de'] == n and f['a'] in pos), prin[0])

    for n in sorted(lados, key=lambda n: pos[origen_de(n)]):
        nd = m['nodos'][n]
        origen = origen_de(n)
        h = 72 if 'final' in nd['clases'] else alto + (0 if L.plegadas else L.ps * (L.lineas_sub(n, wl) - 1))
        yy = max(L.cajas[origen].y + 52, libre_desde)
        L.nodo(n, R(xl, yy, wl, h))
        libre_desde = yy + h + 32
        y_fin = max(y_fin, yy + h)
    L.H = L.notas(y_fin + 32) + 8
    # flechas
    puertos = {}
    for f in largas:
        puertos.setdefault(f['de'], []).append(id(f))
        puertos.setdefault(f['a'], []).append(id(f))

    def y_puerto(n, f):
        lista, c = puertos[n], L.cajas[n]
        return c.y + c.h * (lista.index(id(f)) + 1) / (len(lista) + 1)

    for f in m['flechas']:
        a, b = f['de'], f['a']
        if a == 'inicio':
            c = L.cajas[b]
            cx = c.x + 24 if min(pos.get(b, 0), 0) in dobles else c.cx
            L.fondo.append(f'<circle class="d-ini" cx="{cx:g}" cy="{c.y - 38:g}" r="6"/>')
            L.flecha(f, [(cx, c.y - 32), (cx, c.y - 2)])
        elif f in vecinas:
            ca, cb = L.cajas[a], L.cajas[b]
            baja = pos[b] > pos[a]
            w = L.ancho_etq(f) + 8 if f['etiqueta'] else 0
            x = (ca.x + 24 if baja else ca.r - 24) if (b, a) in pares else (ca.cx if w <= ca.w / 2 - 4 else ca.x + 24)
            L.flecha(f, [(x, ca.b), (x, cb.y - 2)] if baja else [(x, ca.y), (x, cb.b + 2)])
        elif f in largas:
            xc = carriles_x[largas.index(f)]
            ya, yb = y_puerto(a, f), y_puerto(b, f)
            L.flecha(f, [(L.cajas[a].r, ya), (xc, ya), (xc, yb), (L.cajas[b].r + 2, yb)])
        elif a in pos:      # a una salida: sale por arriba a la derecha y baja a la salida
            ca, cb = L.cajas[a], L.cajas[b]
            xb = cb.cx if 'final' in m['nodos'][b]['clases'] else cb.r - 24
            ya = ca.y + 14
            L.flecha(f, [(ca.r, ya), (xb, ya), (xb, cb.y - 2)])
        else:               # de una salida al camino: sale por la izquierda y entra por abajo a la derecha
            ca, cb = L.cajas[a], L.cajas[b]
            yb = cb.b - 14
            L.flecha(f, [(ca.cx, ca.b), (ca.cx, ca.b + 20), (cb.r + 24, ca.b + 20), (cb.r + 24, yb), (cb.r + 2, yb)]
                     if ca.b + 20 < yb else [(ca.x, ca.cy), (cb.r + 2, ca.cy)])
    L.acabar()


def fila(m, L):
    """Horizontal para estados y proceso: el camino en una fila de cajas del mismo ancho, con flechas rectas entre
    vecinas si sus etiquetas caben; si no, esa ida va por encima y su vuelta por debajo. Las vueltas que hace Claude, por
    arriba; las vueltas largas, por carriles debajo; las salidas, en una segunda fila, y las notas a su derecha."""
    L.pendientes = []
    prin = principales(m)
    lados = [n for n in m['orden'] if n not in prin]
    pos = {n: i for i, n in enumerate(prin)}
    vecinas = [f for f in m['flechas'] if f['de'] in pos and f['a'] in pos and abs(pos[f['a']] - pos[f['de']]) == 1]
    largas = [f for f in m['flechas'] if f['de'] in pos and f['a'] in pos and abs(pos[f['a']] - pos[f['de']]) > 1]
    bucles = [f for f in vecinas if 'vuelta' in f['clases'] and pos[f['a']] < pos[f['de']]]
    rectas = [f for f in vecinas if f not in bucles]
    pares = {(f['de'], f['a']) for f in rectas}
    n = len(prin)

    etq = L.ancho_etq

    del_hueco = [[f for f in rectas if min(pos[f['de']], pos[f['a']]) == i] for i in range(n - 1)]
    recto = [max([36] + [etq(f) + 24 for f in fs]) for fs in del_hueco]
    arco = [40 if any(f['etiqueta'] for f in fs) else 36 for fs in del_hueco]
    hay_ini = any(f['de'] == 'inicio' for f in m['flechas'])

    def total(ws, modos, x0):
        return x0 + sum(ws) + sum(recto[i] if modos[i] == 'r' else arco[i] for i in range(n - 1)) + 16

    # Anchos: con el detalle en una línea, uno igual para toda la fila o cada caja el suyo; solo si no cabe, el detalle
    # en dos. Gana la opción con más flechas rectas (las que no caben, en arco); a igualdad, la primera.
    entero = [L.medida_nodo(x) for x in prin]
    partido = [max(L.medida_nodo(x, sub=False), min(L.medida_nodo(x), ancho_texto(m['nodos'][x]['sub'], L.fs, K_MONO) / 2 + 48)) for x in prin]
    mejor = None
    for grupo in (([max([150] + entero)] * n, [max([104] + entero)] * n, [max(104, w) for w in entero]),
                  ([max([150] + partido)] * n, [max([104] + partido)] * n, [max(104, w) for w in partido])):
        for ws in grupo:
            modos = ['r'] * (n - 1)
            while total(ws, modos, 16) > L.W and any(modos[i] == 'r' and recto[i] > arco[i] for i in range(n - 1)):
                i = max((i for i in range(n - 1) if modos[i] == 'r'), key=lambda i: recto[i] - arco[i])
                modos[i] = 'a'
            if total(ws, modos, 16) <= L.W and (mejor is None or modos.count('r') > mejor[1].count('r')):
                mejor = (ws, modos)
        if mejor:
            break
    if mejor is None:
        raise Error(f'no cabe en horizontal ({total(ws, modos, 16):.0f} > {L.W})')
    ws, modos = mejor
    x0 = 48 if hay_ini and total(ws, modos, 48) <= L.W else 16     # el punto de inicio, a la izquierda si cabe
    huecos = [recto[i] if modos[i] == 'r' else arco[i] for i in range(n - 1)]
    extra = (L.W - total(ws, modos, x0)) / max(1, len(huecos))      # el sobrante, repartido entre los huecos
    huecos = [h + min(extra, 48) for h in huecos]
    lineas = max(L.lineas_sub(x, w) for x, w in zip(prin, ws))
    alto = L.alto + (0 if L.plegadas else L.ps * (lineas - 1))
    arriba = any(modos[min(pos[f['de']], pos[f['a']])] == 'a' and pos[f['a']] > pos[f['de']] for f in rectas if f['etiqueta'])
    abajo_arcos = any(modos[min(pos[f['de']], pos[f['a']])] == 'a' and pos[f['a']] < pos[f['de']] for f in rectas if f['etiqueta'])
    y = 24 + (40 if m['opciones']['carriles'] else 0)
    if m['opciones']['carriles']:
        L.carril(16, 36, L.W - 32, 'CAMINO')
    # la vuelta de Claude, por encima de los arcos de su hueco si los hay
    alto_bucle = 70 if any(modos[min(pos[f['de']], pos[f['a']])] == 'a' for f in bucles) else 44
    yn = y + (alto_bucle + 36 if bucles else 40 if arriba else 0)
    x = x0 + max(0, (L.W - 16 - x0 - sum(ws) - sum(huecos)) / 2)
    for i, (nid, w) in enumerate(zip(prin, ws)):
        L.nodo(nid, R(x, yn, w, alto))
        x += w + (huecos[i] if i < len(huecos) else 0)
    yb = yn + alto
    y0c = yb + (64 if abajo_arcos else 28)
    carriles_y = [y0c + 18 * k for k in range(len(largas))]
    ys = (carriles_y[-1] + 40) if carriles_y else y0c + 44
    usados = []
    for nid in lados:
        origen = next((f['de'] for f in m['flechas'] if f['a'] == nid and f['de'] in pos), prin[0])
        nd = m['nodos'][nid]
        ws = L.medida_nodo(nid, 120) if 'final' not in nd['clases'] else 160
        xx = L.cajas[origen].cx - ws / 2
        while any(abs(xx - u) < ws + 24 for u in usados):
            xx += ws + 24
        usados.append(xx)
        L.nodo(nid, R(max(16, min(xx, L.W - 16 - ws)), ys, ws, L.alto if 'final' not in nd['clases'] else 72))
    abajo = {}
    for f in largas + [f for f in m['flechas'] if f['a'] in lados or f['de'] in lados]:
        if f['de'] == 'inicio':
            continue
        k = f['de'] if f['de'] in pos else f['a']
        abajo.setdefault(k, []).append(id(f))
        if f in largas:
            abajo.setdefault(f['a'], []).append(id(f))

    def x_puerto(k, f):
        lista, c = abajo[k], L.cajas[k]
        return c.x + c.w * (lista.index(id(f)) + 1) / (len(lista) + 1)

    for f in m['flechas']:
        a, b = f['de'], f['a']
        if a == 'inicio':
            c = L.cajas[b]
            if x0 == 48:
                L.fondo.append(f'<circle class="d-ini" cx="20" cy="{c.cy:g}" r="6"/>')
                L.flecha(f, [(26, c.cy), (c.x - 2, c.cy)])
            else:
                L.fondo.append(f'<circle class="d-ini" cx="{c.x + 24:g}" cy="{c.y - 30:g}" r="6"/>')
                L.flecha(f, [(c.x + 24, c.y - 24), (c.x + 24, c.y - 2)])
        elif f in bucles:   # la vuelta de Claude: sube, cruza por arriba y baja a su vecina
            ca, cb = L.cajas[a], L.cajas[b]
            yl = yn - alto_bucle
            L.flecha(f, [(ca.cx, ca.y), (ca.cx, yl), (cb.cx, yl), (cb.cx, cb.y - 2)])
        elif f in vecinas:
            ca, cb = L.cajas[a], L.cajas[b]
            ida = pos[b] > pos[a]
            if modos[min(pos[a], pos[b])] == 'a' and f['etiqueta']:
                if ida:
                    ya = ca.y - 26
                    L.flecha(f, [(ca.r - 20, ca.y), (ca.r - 20, ya), (cb.x + 20, ya), (cb.x + 20, cb.y - 2)])
                else:
                    ya = ca.b + 26
                    L.flecha(f, [(ca.x + 20, ca.b), (ca.x + 20, ya), (cb.r - 20, ya), (cb.r - 20, cb.b + 2)])
            else:
                dy = (-14 if ida else 14) if (b, a) in pares else 0
                L.flecha(f, [(ca.r, ca.cy + dy), (cb.x - 2, cb.cy + dy)] if ida else [(ca.x, ca.cy + dy), (cb.r + 2, cb.cy + dy)])
        elif f in largas:
            yc = carriles_y[largas.index(f)]
            xa, xb = x_puerto(a, f), x_puerto(b, f)
            L.flecha(f, [(xa, L.cajas[a].b), (xa, yc), (xb, yc), (xb, L.cajas[b].b + 2)])
        elif a in pos:
            ca, cb = L.cajas[a], L.cajas[b]
            xa = x_puerto(a, f)
            if cb.x + 12 <= xa <= cb.r - 12:
                L.flecha(f, [(xa, ca.b), (xa, cb.y - 2)])
            else:
                ym = cb.y - 24
                L.flecha(f, [(xa, ca.b), (xa, ym), (cb.cx, ym), (cb.cx, cb.y - 2)])
        else:
            ca, cb = L.cajas[a], L.cajas[b]
            xb = x_puerto(b, f)
            L.flecha(f, [(ca.cx, ca.y), (ca.cx, ca.y - 20), (xb, ca.y - 20), (xb, cb.b + 2)] if not (ca.x + 12 <= xb <= ca.r - 12)
                     else [(xb, ca.y), (xb, cb.b + 2)])
    y_fin = max(c.b for c in L.cajas.values())
    # las notas, a la derecha de las salidas, en el hueco bajo el flujo, si caben sin tocar ninguna flecha; si no, debajo
    xn = max([L.cajas[x].r for x in lados] + [0]) + 32 if lados else 16
    wn = L.W - 16 - xn
    fx = TAM_NOTA['amplio'][1]       # cabe con el tamaño amplio: así caben los tres
    pide = max([ancho_texto(t, fx) + 24 for c, t in m['notas']] + [0])   # la cabecera puede ir en dos líneas
    al_lado = False
    if m['notas'] and L.hueco and wn >= pide:
        try:
            caja = R(xn, ys, wn, notas_svg(m, L.o, wn, xn, ys)[1]['amplio'])
            al_lado = not any(caja.mas(4).corta(seg_rect(p, q)) for p, q in L.segs)
        except Error:
            pass
    if al_lado:
        L.H = max(y_fin, L.notas(ys, xn, wn) - 8) + 16
    else:
        L.H = L.notas(y_fin + 28) + 8
    L.acabar()


def rejilla(m, L):
    """Horizontal para arquitectura y piezas: cada zona, una columna; sus nodos, apilados."""
    L.pendientes = []
    grupos = [(nombre, ids) for nombre, ids in m['zonas']]
    sueltos = [n for n in m['orden'] if not any(n in ids for _, ids in grupos)]
    if sueltos:
        grupos.append(('', sueltos))
    if len(m['zonas']) <= 1 and len(grupos[0][1]) > 3:  # una zona grande: en filas de tres, y lo de fuera, debajo
        ids = grupos[0][1]
        return rejilla_filas(m, L, [(grupos[0][0] if i == 0 else '', ids[i:i + 3]) for i in range(0, len(ids), 3)])
    etq = max([L.ancho_etq(f) for f in m['flechas']] + [40])
    hueco = max(80, etq + 32)
    anchos = [max(L.medida_nodo(n, 160) for n in ids) for _, ids in grupos]
    total = 16 + sum(w + 48 for w in anchos) + hueco * (len(grupos) - 1) + 16
    if total > L.W:
        raise Error(f'no cabe en horizontal ({total:.0f} > {L.W})')
    x, alto = 16, L.alto
    paso = alto + 60
    filas_max = max(len(ids) for _, ids in grupos)
    for (nombre, ids), w in zip(grupos, anchos):
        if nombre:
            L.zona(R(x, 16, w + 48, 48 + paso * filas_max - (paso - alto) + 16), nombre)
        for i, n in enumerate(ids):
            L.nodo(n, R(x + 24, 56 + paso * i, w, alto))
        x += w + 48 + hueco
    y_fin = 56 + paso * filas_max - (paso - alto) + 32
    L.H = L.notas(y_fin + 16) + 8
    enrutar(m, L)
    L.acabar()


def rejilla_filas(m, L, grupos):
    anchos = max(L.medida_nodo(n, 200) for _, ids in grupos for n in ids)
    etq = max([L.ancho_etq(f) for f in m['flechas']] + [40])
    hueco = max(80, etq + 32)
    w = min(anchos, (L.W - 64 - 2 * hueco) / 3)
    alto = L.alto
    paso = alto + 60
    y = 64
    for nombre, ids in grupos:
        for i, n in enumerate(ids):
            L.nodo(n, R(40 + i * (w + hueco), y, w, alto))
        y += paso
    if m['zonas']:
        L.zona(R(16, 16, L.W - 32, y - paso + alto + 24), m['zonas'][0][0])
    y_fin = y - paso + alto + 40
    fuera = [n for n in m['orden'] if n not in L.cajas]
    for i, n in enumerate(fuera):
        wf = L.medida_nodo(n, 200)
        L.nodo(n, R(L.W / 2 - wf / 2, y_fin + 32, wf, alto))
        y_fin += 32 + alto
    L.H = L.notas(y_fin + 24) + 8
    enrutar(m, L)
    L.acabar()


def enrutar(m, L):
    """Une cada par de nodos: recto si comparten columna o fila; si no, en L por el lado que no tropiece."""
    for f in m['flechas']:
        if f['de'] == 'inicio':
            continue
        ca, cb = L.cajas[f['de']], L.cajas[f['a']]
        otros = [c for n, c in L.cajas.items() if n not in (f['de'], f['a'])]
        sx = max(ca.x, cb.x), min(ca.r, cb.r)
        sy = max(ca.y, cb.y), min(ca.b, cb.b)
        if sx[1] - sx[0] >= 24:
            x = (sx[0] + sx[1]) / 2
            pts = [(x, ca.b), (x, cb.y - 2)] if cb.y > ca.b else [(x, ca.y), (x, cb.b + 2)]
        elif sy[1] - sy[0] >= 24:
            y = (sy[0] + sy[1]) / 2
            pts = [(ca.r, y), (cb.x - 2, y)] if cb.x > ca.r else [(ca.x, y), (cb.r + 2, y)]
        else:
            ida = [(ca.r if cb.cx > ca.cx else ca.x, ca.cy), (cb.cx, ca.cy), (cb.cx, cb.y - 2 if cb.y > ca.cy else cb.b + 2)]
            vuelta = [(ca.cx, ca.b if cb.cy > ca.cy else ca.y), (ca.cx, cb.cy), (cb.x - 2 if cb.x > ca.cx else cb.r + 2, cb.cy)]
            limpia = lambda p: not any(seg_rect(a, b, 4).corta(o) for a, b in zip(p, p[1:]) for o in otros)
            pts = ida if limpia(ida) or not limpia(vuelta) else vuelta
        L.flecha(f, pts)


def secuencia(m, L):
    actores = m['orden']
    L.pendientes = []
    if L.o == 'h':
        n = len(actores)
        paso_x = (L.W - 32) / n
        xs = [16 + paso_x * (i + .5) for i in range(n)]
        pos = dict(zip(actores, xs))
        y0, paso = 24 + L.alto + 32, 60
        H = y0 + paso * len(m['flechas']) + 16
        for a in actores:
            w = min(paso_x - 16, L.medida_nodo(a, 120))
            L.fondo.append(f'<line class="d-vida" x1="{pos[a]:g}" y1="{24 + L.alto - 4:g}" x2="{pos[a]:g}" y2="{H - 8:g}" data-de="{a}" data-a="{a}"/>')
            L.nodo(a, R(pos[a] - w / 2, 24, w, L.alto - 4))
        for i, f in enumerate(m['flechas']):
            y = y0 + paso * i
            x1, x2 = pos[f['de']], pos[f['a']]
            s = 1 if x2 > x1 else -1
            L.flecha(f, [(x1 + 4 * s, y), (x2 - 6 * s, y)], etiqueta=False)
            t = f['etiqueta']
            claude = 'cursiva' in f['clases']
            w = L.ancho_etq(f)
            L.H = H
            xe = x1 + 14 if s == 1 else x1 - 14 - w
            L.pon_etiqueta(f, t, R(xe, y - 8 - L.fe - 8, w, L.fe + 8), claude)
            if f['estado']:
                xs_ = x2 + 12 if s == 1 else x2 - 12
                ancla = 'start' if s == 1 else 'end'
                L.nodos.append(f'<text class="d-sb d-estado" data-de="{f["de"]}" data-a="{f["a"]}" x="{xs_:g}" y="{y + 6 + L.fs:g}" font-size="{L.fs}" text-anchor="{ancla}">→ {escape(f["estado"])}</text>')
        L.H = L.notas(H + 8) + 8
        return
    # vertical: los actores arriba, en dos filas si hace falta, y cada mensaje una fila «de → a» con su verbo
    cols = 2
    w = (L.W - 32 - 16) / cols
    y = 16
    for i, a in enumerate(actores):
        L.nodo(a, R(16 + (i % cols) * (w + 16), y + (i // cols) * (L.alto + 8), w, L.alto - 4))
    y += ((len(actores) + cols - 1) // cols) * (L.alto + 8) + 16
    for i, f in enumerate(m['flechas']):
        de, a = m['nodos'][f['de']]['nombre'], m['nodos'][f['a']]['nombre']
        claude = 'cursiva' in f['clases']
        color = f['color']
        cl = ('d-cl' if claude else 'd-etiqueta') + (f' d-b-{color}' if color else '')
        linea = f'{de} → {a}'
        if ancho_texto(linea, L.fs) > L.W - 72:
            raise Error(f'«{linea}» no cabe en la vertical')
        y1, y2 = y + round(16 * L.escala), y + round(34 * L.escala)
        o = [f'<g class="d-paso" data-de="{f["de"]}" data-a="{f["a"]}">',
             f'<text class="d-num d-etiqueta" x="16" y="{y1:g}" font-size="{L.fe}">{i + 1:02d}</text>',
             f'<text class="d-sb" x="56" y="{y1:g}" font-size="{L.fs}">{escape(linea)}</text>',
             f'<text class="{cl}" x="56" y="{y2:g}" font-size="{L.fc if claude else L.fe}">{escape(f["etiqueta"])}</text>']
        if f['estado']:
            o.append(f'<text class="d-sb" x="{L.W - 16:g}" y="{y2:g}" font-size="{L.fs}" text-anchor="end">→ {escape(f["estado"])}</text>')
        L.etiquetas.append(''.join(o) + '</g>')
        y += round(46 * L.escala)
    L.H = L.notas(y + 8) + 8


def fases(m, L):
    L.pendientes = []
    ids = m['orden']
    if L.o == 'v':
        alto_h = L.alto0 + 4 if L.plegadas else L.alto1 + 4
        paso, y = alto_h + 16, 40
        for i, n in enumerate(ids):
            nd = m['nodos'][n]
            if i:
                L.flechas.append(f'<line class="d-regla d-fase" x1="28" y1="{y - paso + 9:g}" x2="28" y2="{y - 9:g}" data-de="{ids[i - 1]}" data-a="{n}"/>')
            foco = 'foco' in nd['clases']
            L.cajas[n] = R(8, y - 26, L.W - 16, alto_h)
            subs = L.partir(nd['sub'], L.W - 72, L.fs) if nd['sub'] and not L.plegadas else []
            o = [f'<g data-nodo="{n}" class="d-nodo d-hito{" foco" if foco else ""}"><rect class="d-caja d-toque" x="8" y="{y - 26:g}" width="{L.W - 16}" height="{alto_h}" rx="6"/>',
                 f'<circle class="d-punto" cx="28" cy="{y - 6:g}" r="{7 if foco else 5}"/>',
                 f'<text class="d-nn" x="52" y="{y:g}" font-size="{L.fn}">{escape(nd["nombre"])}</text>']
            for j, s in enumerate(subs[:1]):
                o.append(f'<text class="d-sb" x="52" y="{y + L.pn:g}" font-size="{L.fs}">{escape(s)}</text>')
            L.nodos.append(''.join(o) + '</g>')
            y += paso
        L.H = L.notas(y - 20) + 8
        return
    n = len(ids)
    paso = (L.W - 64) / (n - 1) if n > 1 else 0
    xs = [32 + paso * i for i in range(n)]
    w_hito = min(2 * paso - 24, L.W - 16)
    alto_arriba = max(len(L.partir(m['nodos'][nid]['nombre'], w_hito, L.fn, K_NEGRITA)) + (len(L.partir(m['nodos'][nid]['sub'], w_hito, L.fs)) if m['nodos'][nid]['sub'] and not L.plegadas else 0)
                      for nid in ids[::2])
    yl = 16 + 20 + L.pn * (alto_arriba - 1) + 24 + 14
    for i, nid in enumerate(ids):
        nd = m['nodos'][nid]
        w = min(2 * paso - 24, L.W - 16)
        nombre = L.partir(nd['nombre'], w, L.fn, K_NEGRITA)
        subs = L.partir(nd['sub'], w, L.fs) if nd['sub'] and not L.plegadas else []
        arriba = i % 2 == 0
        lineas = len(nombre) + len(subs)
        x = min(max(xs[i], 16 + w / 2), L.W - 16 - w / 2)
        if i:
            L.flechas.append(f'<line class="d-regla d-fase" x1="{xs[i - 1] + 9:g}" y1="{yl}" x2="{xs[i] - 9:g}" y2="{yl}" data-de="{ids[i - 1]}" data-a="{nid}"/>')
        foco = 'foco' in nd['clases']
        y_txt = (yl - 24 - L.pn * (lineas - 1)) if arriba else yl + 40
        top = (y_txt - 20) if arriba else yl - 14
        bot = (yl + 14) if arriba else y_txt + L.pn * (lineas - 1) + 8
        L.cajas[nid] = R(x - w / 2, top, w, bot - top)
        o = [f'<g data-nodo="{nid}" class="d-nodo d-hito{" foco" if foco else ""}"><rect class="d-caja d-toque" x="{x - w / 2:g}" y="{top:g}" width="{w:g}" height="{bot - top:g}" rx="6"/>',
             f'<circle class="d-punto" cx="{xs[i]:g}" cy="{yl}" r="{7 if foco else 5}"/>']
        k = 0
        for t in nombre:
            o.append(f'<text class="d-nn" x="{x:g}" y="{y_txt + L.pn * k:g}" font-size="{L.fn}" text-anchor="middle">{escape(t)}</text>')
            k += 1
        for t in subs:
            o.append(f'<text class="d-sb" x="{x:g}" y="{y_txt + L.pn * k:g}" font-size="{L.fs}" text-anchor="middle">{escape(t)}</text>')
            k += 1
        L.nodos.append(''.join(o) + '</g>')
    L.H = L.notas(max(c.b for c in L.cajas.values()) + 24) + 8


def dibujar(m, o, cajas='desplegadas', forma='redondeada', hueco=True):
    L = Lienzo(m, o, cajas, forma)
    L.hueco = hueco
    t = m['tipo']
    if t in ('estados', 'proceso'):
        (columna if o == 'v' else fila)(m, L)
    elif t in ('arquitectura', 'piezas'):
        (columna if o == 'v' else rejilla)(m, L)
    elif t == 'secuencia':
        secuencia(m, L)
    else:
        fases(m, L)
    return L


# ───────────────────────── figura y página ─────────────────────────

def linea_ficha(t, m):
    mm = re.match(r'([A-ZÁÉÍÓÚÑÜ0-9 ·\-]{2,})(?:\s*\((\w+)\))?\s*:\s*(.*)$', t)
    if t.startswith('claude:'):
        return f'<li class="d-li-claude">{escape(t[7:].strip())}</li>'
    if mm:
        bt, color, resto = mm.groups()
        c = f' d-b-{color}' if color in COLORES else ''
        return f'<li><b class="d-bt{c}">{escape(bt.strip())}</b> {escape(resto)}</li>'
    return f'<li>{escape(t)}</li>'


def figura(m, tema=''):
    """La <figure>: las dos formas, si caben, con todos los ajustes puestos como clases y atributos, para que la
    herramienta «diagramas» los cambie sin volver a generar. Con tema, data-d-tema (el documento trae sus colores)."""
    dib = {}
    errores = []
    variantes = [(c, f) for c in VARIANTES['cajas'] for f in VARIANTES['forma']]
    dib = {'v': {v: dibujar(m, 'v', *v) for v in variantes}, 'h': {}}
    for v in variantes:
        try:
            dib['h'][v] = dibujar(m, 'h', *v)
        except Error as e:
            errores.append(f'{"" if v == variantes[0] else ", ".join(v) + ": "}{e}')
    # Las notas, en el hueco de la horizontal solo si caben en las cuatro variantes: así el ajuste vale para todas.
    hueco = bool(dib['h']) and all(L.notas_dentro for L in dib['h'].values())
    if dib['h'] and not hueco and any(L.notas_dentro for L in dib['h'].values()):
        dib['h'] = {v: dibujar(m, 'h', *v, hueco=False) for v in dib['h']}
    aria = m['descripcion'] or m['titulo']
    hay_h = bool(dib['h'])

    def svg_notas(o, lugar):
        if not m['notas']:
            return ''
        w = ANCHO[o] if lugar == 'debajo' else ANCHO_LADO
        grupos, altos = notas_svg(m, o, w - 16)
        clase = ('ancho solo-ancho' if lugar == 'debajo' else 'solo-ancho') if o == 'h' else ('vertical solo-estrecho' if hay_h else 'vertical')
        pref = f'{m["id"]}-n{o}-{lugar}'
        return ''.join(f'<svg class="d-notas-svg {clase}" data-lugar="{lugar}" data-tam="{t}" viewBox="0 0 {w} {altos[t] + 16:g}" role="img" '
                       f'aria-labelledby="{pref}-{t}"><title id="{pref}-{t}">Notas</title>{g}</svg>' for t, g in grupos.items())

    svgs = []
    if hay_h:
        svgs.append('<div class="d-fila">' + ''.join(
            dib['h'][v].svg('ancho solo-ancho', aria).replace('<svg ', f'<svg data-cajas="{v[0]}" data-forma="{v[1]}" ', 1) for v in variantes if v in dib['h'])
            + svg_notas('h', 'lado') + '</div>' + svg_notas('h', 'debajo'))
    clase = 'vertical solo-estrecho' if hay_h else 'vertical'
    svgs += [dib['v'][v].svg(clase, aria).replace('<svg ', f'<svg data-cajas="{v[0]}" data-forma="{v[1]}" ', 1) for v in variantes]
    svgs.append(svg_notas('v', 'debajo'))
    elegida = ('plegadas' if m['opciones']['cajas'] != 'desplegadas' else 'desplegadas', m['opciones']['forma'])
    dib = {o: d[elegida] for o, d in dib.items() if elegida in d}
    op = m['opciones']
    cab = [f'<p class="d-antetitulo">{escape(m["antetitulo"])}</p>']
    if m['titulo']:
        cab.append(f'<p class="d-titulo">{escape(m["titulo"])}</p>')
    if m['descripcion']:
        primera, _, resto = m['descripcion'].partition('. ')
        cab.append(f'<p class="d-desc"><span class="d-desc-1">{escape(primera + ("." if resto else ""))}</span>'
                   + (f'<span class="d-desc-resto"> {escape(resto)}</span>' if resto else '') + '</p>')
    ayuda = ('<p class="d-ayuda">Pulsa un elemento para ver su ficha; pasa el ratón o llega con el tabulador para resaltar su recorrido. Escape la cierra.</p>'
             if m['fichas'] else '')
    fichas = ''
    if m['fichas']:
        f = []
        for nid in m['orden']:
            if nid not in m['fichas']:
                continue
            resumen, lineas = m['fichas'][nid]
            cuerpo = (f'<p>{escape(resumen)}</p>' if resumen else '') + ('<ul>' + ''.join(linea_ficha(x, m) for x in lineas) + '</ul>' if lineas else '')
            f.append(f'<div data-ficha="{nid}" data-nombre="{escape(m["nodos"][nid]["nombre"])}">{cuerpo}</div>')
        fichas = '<div class="d-fichas" hidden>' + ''.join(f) + '</div>'
    izq, der = (m['pie'] + ['', ''])[:2] if m['pie'] else ('', '')
    recuento = f'<span class="d-recuento">{"· " if der else ""}{len(m["nodos"])} NODOS · {len(m["flechas"])} FLECHAS</span>'
    vacio = '' if der else ' class="d-vacio"'
    pie = (f'<div class="d-pie{"" if izq or der else " d-pie-vacio"}"><span>{escape(izq)}</span>'
           f'<span{vacio}>{escape(der)}{" " if der else ""}{recuento}</span></div>')
    attr = ' data-diagrama' if m['fichas'] else ''
    no = ' '.join(f'd-no-{k}' for k in CASILLAS if not op[k])
    datos = ''.join(f' data-d-{k}="{op[k]}"' for k in SELECTORES)
    if tema:
        datos += f' data-d-tema="{escape(tema)}"'
    if hueco and m['notas']:
        no += ' d-hueco'
    html = (f'<figure class="diagrama d-gen {no}" id="{m["id"]}"{attr}{datos} data-marca-on="auto">'
            f'<div class="d-cabecera">{"".join(cab)}</div>' + ayuda + ''.join(svgs) + pie + fichas + '</figure>')
    return html, dib, errores


def css_tema(nombre):
    ruta = Path(nombre) if nombre.endswith('.json') else TEMAS / f'{nombre}.json'
    tema = json.loads(ruta.read_text(encoding='utf-8'))
    claro = ' '.join(f'--{k}:{v};' for k, v in tema['colores'].items())
    oscuro = ' '.join(f'--{k}:{v};' for k, v in tema.get('colores-oscuro', {}).items())
    b_claro = ' '.join(f'--b-{k}:{v[0]};' for k, v in BOTONES.items())
    b_oscuro = ' '.join(f'--b-{k}:{v[1]};' for k, v in BOTONES.items())
    t = tema.get('tipografias', {})
    fuentes = f'--fuente-texto:{t.get("texto", "system-ui, sans-serif")}; --fuente-escena:{t.get("escena", "Georgia, serif")}; --fuente-titulos:{t.get("titulos", "system-ui, sans-serif")};'
    css = f':root {{ {claro} {b_claro} {fuentes} --diagrama-papel:var(--pagina); }}\n'
    if oscuro:
        css += f':root[data-theme="dark"] {{ {oscuro} {b_oscuro} }}\n'
    return css, t.get('url', '')


def pagina(m, tema):
    fig, dib, errores = figura(m)
    css_t, url = css_tema(tema)
    base = (SKILL / 'assets' / 'diagramas.css').read_text(encoding='utf-8')
    js = (SKILL / 'assets' / 'diagramas.js').read_text(encoding='utf-8')
    fuentes = f'<link rel="stylesheet" href="{url}">' if url else ''
    return (f'<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{escape(m["titulo"] or "Diagrama")}</title>\n{fuentes}\n<style>\n{css_t}'
            'body { margin:0; padding:1.5rem 16px 3rem; background:var(--pagina); color:var(--texto); font:17px/1.55 var(--fuente-texto); }\n'
            'main { max-width:62rem; margin:0 auto; }\n'
            f'{base}\n</style>\n</head>\n<body>\n<main>\n{fig}\n</main>\n<script>\n{js}\n</script>\n</body>\n</html>\n'), errores


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='Genera un diagrama de la SF a partir de datos breves.')
    ap.add_argument('datos', type=Path)
    ap.add_argument('-o', '--salida', type=Path)
    ap.add_argument('--tema', default='tinta')
    ap.add_argument('--fragmento', action='store_true', help='solo la <figure>, sin página')
    ap.add_argument('--sin-comprobar', action='store_true')
    a = ap.parse_args(argv)
    try:
        m = modelo(leer(a.datos.read_text(encoding='utf-8')))
        m['id'] = re.sub(r'[^a-z0-9]+', '-', a.datos.stem.lower()).strip('-') or 'd'
        if a.fragmento:
            html, _, errores = figura(m, Path(a.tema).stem)
        else:
            html, errores = pagina(m, a.tema)
    except Error as e:
        print(f'✕ {e}', file=sys.stderr)
        return 2
    for e in errores:
        print(f'· sin horizontal: {e}', file=sys.stderr)
    salida = a.salida or a.datos.with_suffix('.html')
    salida.write_text(html, encoding='utf-8')
    print(f'{salida} ({len(html)} caracteres)')
    if a.fragmento or a.sin_comprobar:
        return 0
    r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(AQUI / 'comprobar_diagramas.py'), str(salida), '--oscuro'])
    return r.returncode


if __name__ == '__main__':
    sys.exit(main())
