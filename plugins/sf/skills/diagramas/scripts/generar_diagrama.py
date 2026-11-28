"""Genera un diagrama de la SF a partir de datos breves (skill diagramas): Claude escribe los datos y el programa dibuja.

    python -I -X utf8 generar_diagrama.py <datos.diagrama> [-o salida.html] [--tema tinta] [--fragmento] [--sin-comprobar]
                                          [--medidas] [--capturas carpeta]

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
from difflib import SequenceMatcher
from itertools import permutations, product
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
CLASES_NODO = {'foco', 'salida', 'final', 'externo', 'fin', 'dec', 'lado', 'izquierda', 'accion', 'previsto', 'nuevo'}
LATERALES = {'lado', 'izquierda'}                  # al lado del eje, a la altura de su destino (decisión 326)
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
    # Lo que los pasos 0 y 1 de la skill fijan antes de dibujar (decisiones 385 y 387), por escrito en los datos: el
    # objetivo, el concepto, los puntos clave con sus módulos e interconexiones clave; y con qué diagrama se compara y
    # cuál era el de antes, si se rehace (concepto() lo comprueba).
    texto = lambda k: d.get(k, '') if isinstance(d.get(k, ''), str) else ' '.join(e['texto'] for e in d[k])
    m['semantica'] = {k: texto(k) for k in ('objetivo', 'concepto', 'compara-con', 'antes', 'fijo')}
    # cada punto clave, su frase y dónde se ve: nodos o zonas («a»), flechas («a > b») o bucles («a > b > a»)
    m['puntos_clave'] = []
    for e in d.get('puntos-clave', []) if isinstance(d.get('puntos-clave'), list) else []:
        frase, _, donde = e['texto'].partition('|')
        m['puntos_clave'].append({'texto': frase.strip(), 'donde': [[y.strip() for y in x.split('>')] for x in donde.split(',') if x.strip()]})
    m['modulos_clave'] = [x.strip() for x in texto('modulos-clave').split(',') if x.strip()]
    # quién actúa (decisión 422): con más de uno, cada paso dice cuál; y de dónde salen las palabras del lector
    # «actores: a, b» o una sección con «a: quién es» por línea
    m['decisiones'] = [x.strip() for x in texto('decisiones').split(',') if x.strip()]
    m['actores'] = ([e['texto'].partition(':')[0].strip() for e in d['actores']] if isinstance(d.get('actores'), list)
                    else [x.strip() for x in texto('actores').split(',') if x.strip()])
    # el glosario (decisión 423): los términos importantes del gráfico, con qué es cada uno en una línea
    m['glosario'] = [tuple(x.strip() for x in e['texto'].partition('|')[::2]) for e in d['glosario']] if isinstance(d.get('glosario'), list) else []
    m['interconexiones_clave'] = ([[x.strip() for x in e['texto'].split('>')] for e in d['interconexiones-clave']]
                                  if isinstance(d.get('interconexiones-clave'), list) else [])
    ops = [x.strip() for x in d.get('opciones', '').split(',') if x.strip()]
    m['completo'] = 'completo' in ops        # el presupuesto, solo informativo: el diagrama tiene que ser completo
    m['una_columna'] = 'una-columna' in ops  # sin probar una columna más para las ramas laterales ni los bloques
    m['abiertos'] = 'abiertos' in ops        # los bloques empiezan abiertos (por defecto, cerrados: decisión 415)
    for o in [x for x in ops if x not in ('completo', 'una-columna', 'abiertos')]:
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
        # las clases, separadas por «|» o por espacios («externo lado»); un campo con algo que no es clase, el detalle
        sep = []
        for x in f[1:]:
            ps = x.split()
            sep += ps if len(ps) > 1 and all(p in CLASES_NODO or p.startswith('chip=') for p in ps) else [x]
        for x in sep:
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
    # Sin corchetes (decisión 420): lo que actúa sobre varias cajas a la vez apunta a la zona que las lleva.
    if d.get('corchetes'):
        raise Error('«corchetes:» ya no existe: usa una zona (las cajas sobre las que actúa, en una carpeta) y apunta la '
                    'flecha a la zona («acc > id_de_la_zona»)')
    m['corchetes'] = {}
    sin_nodo = []
    for e in d.get('flechas', d.get('mensajes', [])):
        # «de > a: ETIQUETA | marcas», o sin etiqueta, «de > a | marcas»; las marcas, separadas por «|» o por espacios
        mm = re.match(r'([\w-]+)\s*>\s*([\w-]+)\s*(?::\s*(.*)|(\|.*))?$', e['texto'])
        if not mm:
            raise Error(f'línea {e["n"]}: flecha mal escrita («de > a: ETIQUETA | color | claude» o «de > a | marcas»)')
        de, a, resto, marcas = mm.groups()
        f = campos(resto or marcas or '')
        f = f[:1] + [p for x in f[1:] for p in x.split()]
        fl = {'de': de, 'a': a, 'etiqueta': f[0] if f else '', 'clases': set(x for x in f[1:] if x and '=' not in x),
              'estado': next((x[7:] for x in f[1:] if x.startswith('estado=')), ''),
              'cauce': next((x[6:].replace('_', ' ') for x in f[1:] if x.startswith('cauce=')), '')}
        # Marcas genéricas: color de la etiqueta (color=X o X), de la línea (linea=X), cursiva, discontinua y vuelta
        # (discontinua y, entre vecinas hacia atrás, por encima). «claude» es un atajo de estilo: cursiva y vuelta. «principal»: línea en acento.
        for x in f[1:]:
            k, _, v = x.partition('=')
            if k in ('color', 'linea'):
                if v not in COLORES:
                    raise Error(f'línea {e["n"]}: color «{v}» desconocido; colores: {", ".join(COLORES)}')
                fl[k] = v
        fl['color'] = fl.get('color') or next((x for x in fl['clases'] if x in COLORES), '')
        if fl['clases'] & {'principal', 'flujo'}:
            fl.setdefault('linea', 'acento')
        if 'claude' in fl['clases']:
            fl['clases'] |= {'cursiva', 'vuelta'}
        for x in (de, a):
            if x != 'inicio' and x not in m['nodos']:
                sin_nodo.append((x, x == de, e['n']))         # ¿una zona? se mira con las zonas
        m['flechas'].append(fl)
    # Cauces (cauce=X en las flechas): lo que viaja por cada una (audio, control…). El del flujo, en el color del camino
    # (acento); los demás, en segundo, morado, verde y gris, por orden; la línea que dan los datos manda.
    cauces = list(dict.fromkeys(f['cauce'] for f in m['flechas'] if f['cauce']))
    del_flujo = next((f['cauce'] for f in m['flechas'] if f['cauce'] and 'flujo' in f['clases']), None)
    resto = iter(('segundo', 'morado', 'verde', 'gris'))
    m['cauces'] = [(c, 'acento' if c == del_flujo else next(resto, 'gris')) for c in ([del_flujo] if del_flujo else []) + [c for c in cauces if c != del_flujo]]
    color_cauce = dict(m['cauces'])
    for f in m['flechas']:
        if f['cauce'] and 'linea' not in f:
            f['linea'] = color_cauce[f['cauce']]
    for e in d.get('notas', []):
        cab, _, txt = e['texto'].partition(':')
        m['notas'].append((cab.strip(), txt.strip()))
    # Zonas: una zona puede nombrar otra (por su id): va dentro, como una cabecera sin marco (m['subzonas']); en
    # m['zonas'], las de primer nivel con todos sus nodos, en orden.
    zdat = []
    for e in d.get('zonas', []):
        mm = re.match(r'([\w-]+):\s*(.*)$', e['texto'])
        nombre, _, ids = (mm.group(2) if mm else e['texto']).partition('|')
        zdat.append((mm.group(1) if mm else None, nombre.strip(), [x.strip() for x in ids.split(',') if x.strip()], e['n']))
    zids = {z[0]: z for z in zdat if z[0] and z[0] not in m['nodos']}
    madre = {}
    for zid, _, ids, n in zdat:
        for x in ids:
            if x in zids:
                if x in madre:
                    raise Error(f'línea {n}: la zona «{x}» va dentro de dos zonas')
                madre[x] = zid

    def nodos_de(z, camino=()):
        zid, _, ids, n = z
        if zid in camino:
            raise Error(f'línea {n}: la zona «{zid}» se contiene a sí misma')
        out = []
        for x in ids:
            if x in zids:
                out += nodos_de(zids[x], camino + (zid,))
            elif x in m['nodos']:
                out.append(x)
            else:
                raise Error(f'línea {n}: la zona nombra «{x}», que no es ningún nodo ni ninguna zona')
        return out
    m['subzonas'], m['zona_ids'] = [], []
    for z in zdat:
        (m['subzonas'] if z[0] in madre else m['zonas']).append((z[1], nodos_de(z)))
        if z[0] not in madre:
            m['zona_ids'].append(z[0])
    # Cada zona, una sola carpeta (encargo del propietario): sus nodos, seguidos en el orden, donde sale el primero (las de
    # dentro, también seguidas). Un recorrido que vuelve a una zona ya dejada no abre otra carpeta: lo que vuelve va a ella
    # (en la vertical, al lado de los suyos: m['desplazados']).
    antes_ = list(m['orden'])
    for _, ids in m['subzonas'] + m['zonas']:
        grupo, nuevo = set(ids), []
        for n in m['orden']:
            if n in grupo:
                if n not in nuevo:
                    nuevo += [x for x in m['orden'] if x in grupo]
            else:
                nuevo.append(n)
        m['orden'] = nuevo
    m['desplazados'] = [n for n in m['orden'] if m['orden'].index(n) < antes_.index(n)]
    m['nodos'] = {n: m['nodos'][n] for n in m['orden']}
    # Una flecha a una zona (decisión 420): actúa sobre todas sus cajas y llega a su carpeta. Por dentro, el destino
    # son los pasos de la zona (sin lo de al lado ni las acciones), seguidos en una columna.
    for x, sale, n in sin_nodo:
        if x not in zids:
            raise Error(f'línea {n}: «{x}» no es ningún nodo ni ninguna zona')
        if sale:
            raise Error(f'línea {n}: una flecha sale de un nodo, no de la zona «{x}»')
        pasos = [i for i in nodos_de(zids[x]) if not m['nodos'][i]['clases'] & (LATERALES | {'accion'})]
        if not pasos:
            raise Error(f'línea {n}: la zona «{x}» no tiene pasos a los que llegar')
        m['corchetes'][x] = (zids[x][1], pasos)
    m['zona_dentro'] = set(madre)
    m['zona_ids_todas'] = [z[0] for z in zdat if z[0]]
    m['zona_nombre'] = {z[0]: z[1] for z in zdat if z[0]}
    # «anillo: a, b, c» o «columnas: a | b | c» (ids de zonas de primer nivel) fijan la forma de los bloques (decisión 415)
    m['forma_bloques'] = None
    for clave, sep in (('anillo', ','), ('columnas', '|')):
        if d.get(clave):
            ids = [x.strip() for x in d[clave].split(sep) if x.strip()]
            for x in ids:
                if x not in m['zona_ids']:
                    raise Error(f'«{clave}:» nombra «{x}», que no es una zona de primer nivel')
            m['forma_bloques'] = (clave, [m['zona_ids'].index(x) for x in ids] + [z for z in range(len(m['zonas'])) if m['zona_ids'][z] not in ids])
    for e in d.get('fichas', []):
        fid, _, resumen = e['texto'].partition(':')
        m['fichas'][fid.strip()] = (resumen.strip(), e['lineas'])
    # Recorrido (replay): cada paso, un nodo («id: porqué») o una flecha («de > a: porqué»), en el orden de la historia.
    m['recorrido'] = []
    if not d.get('recorrido'):
        # sin recorrido en los datos, el del concepto que fluye: los nodos de sus flechas «flujo», en orden, con su ficha
        fl = [f for f in m['flechas'] if 'flujo' in f['clases'] and f['de'] != 'inicio']
        if fl:
            orden = [fl[0]['de']]
            for f in fl:
                for x in (f['de'], f['a']):
                    if x not in orden and x in m['nodos']:
                        orden.append(x)
            m['recorrido'] = [{'nodo': n, 'texto': ''} for n in orden]
    for e in d.get('recorrido', []):
        mm = re.match(r'([\w-]+)\s*>\s*([\w-]+)\s*(?::\s*(.*))?$', e['texto'])
        if mm:
            de, a, txt = mm.groups()
            if not any(f['de'] == de and f['a'] == a for f in m['flechas']):
                raise Error(f'línea {e["n"]}: el recorrido nombra la flecha «{de} > {a}», que no está en «flechas:»')
            m['recorrido'].append({'de': de, 'a': a, 'texto': (txt or '').strip()})
            continue
        mm = re.match(r'([\w-]+)\s*(?::\s*(.*))?$', e['texto'])
        if not mm or mm.group(1) not in m['nodos']:
            raise Error(f'línea {e["n"]}: el recorrido nombra «{e["texto"]}», que no es ningún nodo ni «de > a»')
        m['recorrido'].append({'nodo': mm.group(1), 'texto': (mm.group(2) or '').strip()})
    # El presupuesto es una recomendación (9 nodos y 12 flechas): por encima, se avisa; con «completo», solo se informa.
    n, f = len(m['nodos']), len(m['flechas'])
    if n > 9 or f > 12:
        if m['completo']:
            print(f'· {n} nodos y {f} flechas (se recomiendan 9 y 12): completo, como piden los datos', file=sys.stderr)
        else:
            print(f'Aviso: {n} nodos y {f} flechas; se recomiendan 9 y 12 como mucho. ¿Dos diagramas (vista general y '
                  'detalle) o el detalle a las fichas? Si tiene que ser completo, «opciones: completo».', file=sys.stderr)
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


def sitios_etiqueta(puntos, w, h):
    """Los sitios donde puede ir la etiqueta (w × h) de una flecha, de los mejores a los peores: junto a su tramo, del
    origen al destino (la etiqueta cerca de donde sale la flecha: una vuelta larga no la deja en medio del dibujo), cerca
    de la mitad del tramo; al lado en los tramos verticales y encima o debajo en los horizontales."""
    for a, b in zip(puntos, puntos[1:]):
        vertical = a[0] == b[0]
        largo = abs(b[1] - a[1]) if vertical else abs(b[0] - a[0])
        for t_ in (.5, .3, .7, .2, .8, .4, .6, .1, .9, .15, .85, .25, .75, .35, .65, .45, .55):
            px, py = a[0] + (b[0] - a[0]) * t_, a[1] + (b[1] - a[1]) * t_
            if vertical:
                if largo < h + 16:
                    continue
                yield from (R(px + 8, py - h / 2, w, h), R(px - 8 - w, py - h / 2, w, h))
            else:
                x1, x2 = min(a[0], b[0]), max(a[0], b[0])
                if largo >= w + 16:
                    yield from (R(px - w / 2, py - 8 - h, w, h), R(px - w / 2, py + 8, w, h))
                yield from (R(x1 + 8, py + 8, w, h), R(x1 + 8, py - 8 - h, w, h), R(x2 - 8 - w, py + 8, w, h), R(x2 - 8 - w, py - 8 - h, w, h))


def linea_de_zona(m, ids):
    """El color de una zona: el de la línea (el cauce) que más llevan sus flechas de dentro; sin ninguna, ''."""
    ids = set(ids)
    cuenta = {}
    for f in m['flechas']:
        if f['de'] in ids and f['a'] in ids and f.get('linea'):
            cuenta[f['linea']] = cuenta.get(f['linea'], 0) + 1
    return max(cuenta, key=lambda k: (cuenta[k], k == 'acento')) if cuenta else ''


def carpeta_sub(cajas, ids, hc):
    """El marco de la carpeta de una zona de dentro (decisión 420, opción B del propietario): alrededor de sus cajas,
    con el alto de su cabecera arriba para la pestaña; None si dentro cae una caja de fuera (entonces, cabecera)."""
    cs = [cajas[n] for n in ids if n in cajas]
    if not cs:
        return None
    x1, x2, y1, y2 = min(c.x for c in cs), max(c.r for c in cs), min(c.y for c in cs), max(c.b for c in cs)
    r = R(x1 - 6, y1 - hc, x2 - x1 + 12, y2 + 6 - y1 + hc)
    if any(c.corta(r) for n, c in cajas.items() if n not in ids):
        return None
    return r


def carpeta_d(x, y, w, h, tx, wt, T, r=8, derecha=False):
    """La silueta de una carpeta: x, y, w, h la abarcan entera, con la pestaña (de tx a tx + wt, T de alto) arriba y el
    cuerpo debajo. La pestaña acaba en diagonal, como la de una carpeta. Con derecha, una pestaña más ancha que el
    cuerpo empieza en su borde izquierdo y sobresale por la derecha."""
    b, d = y + h, x + w
    if derecha and wt > w - r:
        return (f'M{x:g},{b - r:g} V{y + 4:g} Q{x:g},{y:g} {x + 4:g},{y:g} H{x + wt - 8:g} L{x + wt:g},{y + T:g} H{d:g} '
                f'V{b - r:g} Q{d:g},{b:g} {d - r:g},{b:g} H{x + r:g} Q{x:g},{b:g} {x:g},{b - r:g} Z')
    tx = min(max(tx, x), x + w - r - wt)
    fin = (f'H{d - r:g} Q{d:g},{y + T:g} {d:g},{y + T + r:g} V{b - r:g} Q{d:g},{b:g} {d - r:g},{b:g} '
           f'H{x + r:g} Q{x:g},{b:g} {x:g},{b - r:g} Z')
    pest = f'V{y + 4:g} Q{tx:g},{y:g} {tx + 4:g},{y:g} H{tx + wt - 8:g} L{tx + wt:g},{y + T:g} '
    if tx <= x + 1:
        return f'M{x:g},{b - r:g} ' + pest + fin
    return f'M{x:g},{b - r:g} V{y + T + r:g} Q{x:g},{y + T:g} {x + r:g},{y + T:g} H{tx:g} ' + pest + fin


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
        self.fz, self.fsz = medio(13), medio(10)
        self.ft = medio(10)                               # el nombre en la pestaña de un bloque cerrado
        self.tope = 0                                     # lo más alto que se dibuja (la pestaña de un bloque cerrado)
        self.pestanas = {}
        self.dentro_pend = []                                # de cada bloque cerrado, su pestaña: x0, x1 y alto
        self.dentro_alt = {}
        self.color_zona = {nombre: linea_de_zona(m, ids) for nombre, ids in m.get('zonas', []) + m.get('subzonas', [])}         # el nombre de una zona (el título de su bloque) y la cabecera de una zona de dentro
        self.pn, self.ps = round(15 * e), round(13 * e)   # de la línea del nombre a la del detalle, y entre detalles
        self.pnn = round(self.fn * 1.35 * 2) / 2     # entre las dos líneas de un nombre partido (sin que se pisen)
        self.partir_nombres = False                # solo la vertical de arquitectura y piezas, que les deja el alto
        self.variante = (cajas, forma)
        self.plegadas, self.croqueta = cajas == 'plegadas', forma == 'croqueta'
        # Cajas de diagram-design: 48 de alto mínimo (plegada, solo el nombre), 56 con una línea de detalle; con chips de
        # tipo, 16 más arriba para el chip, como sus cajas de 72.
        self.chips = any(n['chip'] for n in m['nodos'].values())
        extra = 16 if self.chips else 0
        # Plegada, compacta: 40 de alto, solo el nombre (el ritmo del original, 42); con chips, 48 más su sitio, para que
        # el circulito de plegar, junto al chip, no tape el centro de la caja. Desplegada, 56 con su detalle.
        self.alto0, self.alto1 = round(((48 if extra else 40) + extra) * e), round((56 + extra) * e)
        self.alto = self.alto0 if self.plegadas else self.alto1
        self.pad = 44 if self.croqueta else 32     # la croqueta, con los extremos redondos, pide más ancho
        sufijo = ('-p' if self.plegadas else '') + ('-c' if self.croqueta else '')
        self.pref = f'{m["id"]}-{o}{sufijo}'
        self.fondo, self.flechas, self.etiquetas, self.nodos = [], [], [], []
        self.plegar = []                           # el circulito de cada caja que se pliega sola
        self.tapas = []                            # la tapa de cada zona, para plegarla en su sitio
        self.nombres_zona = []                     # el nombre de cada zona, que se pone al final (acabar)
        self.zonas_rc = []                         # el marco de cada zona (para medir los requiebros)
        self.nuevos = {k for k, n in m['nodos'].items() if 'nuevo' in n['clases']}
        self.cajas = {}                            # id → R
        self.radio = {}                            # id → radio de sus esquinas (para que las flechas toquen el borde)
        self.obst, self.segs = [], []              # obstáculos para las etiquetas
        self.caminos, self.rotulos = [], []        # cada flecha con sus puntos y cada etiqueta con su sitio (medidas)
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
        if 'bloque' in n['clases']:
            self.bloque(nid, n, rc)
            return
        clases = ' '.join(sorted(n['clases'] & {'foco', 'salida', 'externo', 'fin', 'dec', 'accion', 'previsto', 'nuevo'}))
        if 'dec' in n['clases']:
            forma = (f'<polygon class="d-caja" points="{rc.x:g},{rc.cy:g} {rc.x + 18:g},{rc.y:g} {rc.r - 18:g},{rc.y:g} '
                     f'{rc.r:g},{rc.cy:g} {rc.r - 18:g},{rc.b:g} {rc.x + 18:g},{rc.b:g}"/>')
        else:
            rx = min(rc.h, rc.w) / 2 if self.croqueta or 'accion' in n['clases'] else 6   # la acción, en píldora
            self.radio[nid] = rx
            forma = f'<rect class="d-caja" x="{rc.x:g}" y="{rc.y:g}" width="{rc.w:g}" height="{rc.h:g}" rx="{rx:g}"/>'
        margen = 16 + (12 if self.croqueta else 0)
        # el chip de tipo, dentro de la caja arriba a la izquierda (7 en mono, como diagram-design): x, y, ancho, alto
        fch = round(7 * self.escala * 2) / 2
        chip = (rc.x + 8 + (self.radio.get(nid, 6) - 6) * .45, rc.y + 8, ancho_texto(n['chip'], fch, K_MONO + .1) + 12, fch + 8) if n['chip'] else None
        # el nombre, en una línea; si no cabe (solo en la vertical de arquitectura y piezas, que lo prevé), en dos
        nombres = [n['nombre']] if ancho_texto(n['nombre'], self.fn, K_NEGRITA) <= rc.w - margen else None
        if nombres is None:
            try:
                if not self.partir_nombres:
                    raise Error('')
                nombres = self.partir(n['nombre'], rc.w - margen, self.fn, K_NEGRITA)
            except Error:
                raise Error(f'el nombre «{n["nombre"]}» no cabe en su caja: acórtalo')
        extra = self.pnn * (len(nombres) - 1)
        # El detalle va siempre en el marcado: en las plegadas, oculto, para que una caja se despliegue sola en su sitio.
        subs = self.partir(n['sub'], rc.w - margen - 8, self.fs, K_MONO) if n['sub'] else []
        alto = self.fn + extra + (self.pn + self.ps * (len(subs) - 1) if subs and not self.plegadas else 0)
        y = rc.cy - alto / 2 + self.fn * .8
        if subs and 'dec' not in n['clases']:
            hd = rc.h if not self.plegadas else self.alto1 + extra + self.ps * (len(subs) - 1)
            hp = self.alto0 + extra if not self.plegadas else rc.h
            pnn = f' data-pnn="{self.pnn:g}"' if extra else ''
            forma = forma.replace('<rect class="d-caja" ', f'<rect class="d-caja" data-hd="{hd:g}" data-hp="{hp:g}" data-pn="{self.pn}" data-ps="{self.ps}"{pnn} ', 1)
            k = 11 + (self.radio.get(nid, 6) - 6) * .2          # en la croqueta, un poco más adentro de la curva
            px, py = rc.x + k, rc.y + k
            # con el chip a la vista, a su derecha (CSS lo mueve con translate; sin chip, en la esquina)
            mov = f' style="--dx:{chip[0] + chip[2] + 10 - px:.1f}px; --dy:{chip[1] + chip[3] / 2 - py:.1f}px"' if n['chip'] else ''
            self.plegar.append(f'<g class="d-plegar" data-plegar="{nid}"{mov}><circle class="d-plegar-t" cx="{px:g}" cy="{py:g}" r="15"/>'
                               f'<circle class="d-plegar-p" cx="{px:g}" cy="{py:g}" r="3.5"/></g>')
        sub = next((k for k, (_, ids) in enumerate(self.m.get('subzonas', [])) if nid in ids), None)
        sub = f' data-sub="{sub}"' if sub is not None else ''          # la zona de dentro (cuenta para los requiebros)
        o = [f'<g data-nodo="{nid}"{sub} class="d-nodo {clases}{" d-con-chip" if n["chip"] else ""}">{forma}']
        if n['chip']:
            o.append(f'<g class="d-chip-g"><rect class="d-chip-c" x="{chip[0]:g}" y="{chip[1]:g}" width="{chip[2]:.1f}" height="{chip[3]:g}" rx="2"/>'
                     f'<text class="d-chip" x="{chip[0] + 6:g}" y="{chip[1] + chip[3] / 2 + fch * .36:.1f}" font-size="{fch}">{escape(n["chip"])}</text></g>')
        for i, t in enumerate(nombres):
            o.append(f'<text class="d-nn" x="{rc.cx:g}" y="{y + self.pnn * i:.1f}" font-size="{self.fn}" text-anchor="middle">{escape(t)}</text>')
        for i, s in enumerate(subs):
            oculto = ' d-plegado' if self.plegadas else ''
            o.append(f'<text class="d-sb{oculto}" x="{rc.cx:g}" y="{y + extra + self.pn + self.ps * i:.1f}" font-size="{self.fs}" text-anchor="middle">{escape(s)}</text>')
        if 'fin' in n['clases']:
            o.append(f'<circle class="d-fin-a" cx="{rc.r - 14:g}" cy="{rc.y + 14:g}" r="6"/><circle class="d-fin" cx="{rc.r - 14:g}" cy="{rc.y + 14:g}" r="3"/>')
        self.nodos.append(''.join(o) + '</g>')

    def tab_bloque(self, nombre):
        """Ancho y alto de la pestaña de un bloque cerrado."""
        return ancho_texto(nombre, self.ft, K_MONO) + len(nombre) * self.ft * .06 + 20, self.ft + 9

    def bloque(self, nid, n, rc):
        """Un bloque cerrado (decisión 415): una carpeta, la misma que su zona abierta, con su nombre en la pestaña (la
        letra del título de la zona) y, en el cuerpo, cuántos pasos tiene y ▸; con el fondo suave del color de su cauce.
        rc la abarca entera, pestaña incluida (las maquetaciones le dan el alto de la pestaña de más); si no lo trae, la
        pestaña va encima. Las flechas tocan el cuerpo, o la pestaña si llegan por encima de ella (contacto)."""
        self.radio[nid] = 6
        wt, T = self.tab_bloque(n['nombre'])
        if rc.h < self.alto + T - 1:          # sin el alto de la pestaña: encima de la caja
            self.cajas[nid] = rc = R(rc.x, rc.y - T, rc.w, rc.h + T)
            self.tope = min(self.tope, rc.y - 4)
        # una pestaña más ancha que su carpeta que saldría del dibujo por la izquierda: sobresale por la derecha
        d = carpeta_d(rc.x, rc.y, rc.w, rc.h, rc.x, wt, T, 6, derecha=rc.r - 6 - wt < 4 and rc.x + wt <= self.W - 4)
        self.pestanas[nid] = (rc.x, rc.x + wt, T)
        tinte = f' d-tinte-{n["linea"]}' if n.get('linea') else ''
        cy = rc.y + T + (rc.h - T) / 2
        o = [f'<g data-nodo="{nid}" class="d-nodo bloque">',
             f'<path class="d-carpeta-base" d="{d}"/><path class="d-carpeta{tinte}" d="{d}"/><path class="d-caja d-toque" d="{d}"/>',
             f'<text class="d-bloque-n" x="{rc.x + 10:g}" y="{rc.y + T / 2 + self.ft * .36:.1f}" font-size="{self.ft}">{escape(n["nombre"])}</text>',
             f'<text class="d-bloque-s" x="{rc.cx:g}" y="{cy + self.fn * .36:.1f}" font-size="{self.fn}" text-anchor="middle">{escape(n["sub"])}</text>']
        self.nodos.append(''.join(o) + '</g>')

    def partir(self, t, w, fs, k=K_SANS):
        """Parte un texto en líneas que quepan en w; dos como mucho."""
        if ancho_texto(t, fs, k) <= w:
            return [t]
        pal = t.split()
        if len(pal) == 1 and '/' in t:     # una ruta sin espacios: se parte tras una barra
            pal = re.findall(r'[^/]*/|[^/]+$', t)
            cortes = [(''.join(pal[:i]), ''.join(pal[i:])) for i in range(1, len(pal))]
        else:
            cortes = [(' '.join(pal[:i]), ' '.join(pal[i:])) for i in range(1, len(pal))]
        cortes = [c for c in cortes if all(ancho_texto(x, fs, k) <= w for x in c)]
        # el corte más equilibrado, sin empezar la segunda línea por un separador («·», «/», «→»)
        lineas = list(min(cortes, key=lambda c: (c[1][:1] in '·/→|-', abs(len(c[0]) - len(c[1]))))) if cortes else []
        if not lineas:
            raise Error(f'«{t}» no cabe en {w:.0f} de ancho: acórtalo')
        return lineas

    def medida_nodo(self, nid, minimo=0, sub=True):
        n = self.m['nodos'][nid]
        if 'bloque' in n['clases']:
            return max(minimo, 2 * self.tab_bloque(n['nombre'])[0] + 8, ancho_texto(n['sub'], self.fn, K_SANS) + self.pad)
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
        x, y = p
        if nid in self.pestanas and q[0] == x and q[1] < y and abs(y - (c.y - hueco)) <= 1:
            x0, x1, T = self.pestanas[nid]
            if not x0 <= x <= x1:          # por arriba de un bloque cerrado, fuera de su pestaña: hasta su cuerpo
                return (x, c.y + T - hueco)
            if x > x1 - 8:                 # por la diagonal de la pestaña: hasta ella
                return (x, c.y + T * (x - (x1 - 8)) / 8 - hueco)
        if nid in self.pestanas and q[0] == x and q[1] < y:
            x0, x1, T = self.pestanas[nid]
            if x0 <= x <= x1 and abs(y - (c.y + T - hueco)) <= 1:
                # llega al cuerpo por donde está la pestaña: se queda en la pestaña (o en su diagonal)
                return (x, c.y + (T * (x - (x1 - 8)) / 8 if x > x1 - 8 else 0) - hueco)
        if c and 'dec' in self.m['nodos'].get(nid, {}).get('clases', ()) and q[1] == y and q[0] != x:
            # el hexágono de la decisión: por un lado, hasta su lado inclinado
            k = 18 * min(1, abs(y - c.cy) / (c.h / 2))
            if q[0] < x and abs(x - (c.x - hueco)) <= 1:
                return (c.x + k - hueco, y)
            if q[0] > x and abs(x - (c.r + hueco)) <= 1:
                return (c.r - k + hueco, y)
            return p
        if not c or r <= 0:
            return p

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
        if fl['clases'] & {'vuelta', 'claude'}:
            clases.append('d-vuelta')
        if 'principal' in fl['clases']:
            clases.append('d-principal')
        if 'flujo' in fl['clases']:      # lleva el concepto que fluye: la principal, con su trazo
            clases.append('d-principal d-flujo')
        if 'nuevo' in fl['clases'] or fl['de'] in self.nuevos or fl['a'] in self.nuevos:
            clases.append('d-nuevo')
        puntos = list(puntos)
        if fl.get('zona_rc'):             # a la carpeta de una zona (a_carpeta): hasta su borde
            puntos = recortar(puntos, fl['zona_rc'])
            fl = dict(fl, a=fl['zona'])
        if fl['de'] != 'inicio':
            puntos[0] = self.contacto(fl['de'], puntos[0], puntos[1], 0)
        puntos[-1] = self.contacto(fl['a'], puntos[-1], puntos[-2], 2)
        punta = '' if 'sin-punta' in fl['clases'] else f' marker-end="url(#{self.pref}-m)"'
        cabeza = ''
        (x1, y1), (x2, y2) = puntos[-2], puntos[-1]
        lg = max(abs(x2 - x1), abs(y2 - y1))
        if fl['de'].startswith('_b') and fl['a'].startswith('_b') and lg >= 18:
            # entre dos bloques cerrados: ancha y rellena; el trazo acaba donde empieza la punta
            clases = [c for c in clases if c not in ('d-discontinua',)] + ['d-fl-bloque']
            ux, uy = (x2 - x1) / lg, (y2 - y1) / lg
            L_ = min(14, lg - 2)
            bx, by = x2 - ux * L_, y2 - uy * L_
            cabeza = (f'<polygon class="d-cabeza d-l-{fl.get("linea") or "gris"}" points="{x2:g},{y2:g} {bx - uy * 11:g},{by + ux * 11:g} '
                      f'{bx + uy * 11:g},{by - ux * 11:g}"/>')
            for a, b in zip(puntos, puntos[1:]):
                self.obst.append(seg_rect(a, b, 3))          # con el margen de libre(), la etiqueta, fuera de su cuerpo
            puntos = puntos[:-1] + [(bx, by)]
            punta = ''
        de = f' data-de="{fl["de"]}" data-a="{fl["a"]}"' if fl['de'] != 'inicio' else ''
        recto = 'M' + ' L'.join(f'{x:g},{y:g}' for x, y in puntos)
        da = f' data-da="{recto}"' if len(puntos) > 2 else ''
        self.flechas.append(f'<path class="{" ".join(clases)}"{de} d="{codo(puntos)}"{da} fill="none"{punta}/>' + cabeza)
        for a, b in zip(puntos, puntos[1:]):
            self.segs.append((a, b))
        self.caminos.append((fl, puntos))
        if etiqueta and fl['etiqueta']:
            self.pendientes.append((fl, puntos))

    def etiqueta(self, fl, puntos):
        t = fl['etiqueta']
        claude = 'cursiva' in fl['clases']
        w, h = self.ancho_etq(fl), self.fe + 8
        for c in sitios_etiqueta(puntos, w, h):
            if self.libre(c):
                self.pon_etiqueta(fl, t, c, claude)
                return
        # sin sitio junto a un tramo: el hueco libre más cercano a la flecha, a 76 como mucho (las medidas lo dan como
        # etiqueta lejos); solo si no hay ninguno, el aviso de que no cabe
        cerca = []
        for a, b in zip(puntos, puntos[1:]):
            n = max(1, int((abs(b[0] - a[0]) + abs(b[1] - a[1])) // 8))
            for i in range(n + 1):
                px, py = a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n
                for d in range(12, 80, 4):
                    cerca += [(d, R(px + d, py - h / 2, w, h)), (d, R(px - d - w, py - h / 2, w, h)),
                              (d, R(px - w / 2, py + d, w, h)), (d, R(px - w / 2, py - d - h, w, h))]
        c = next((c for _, c in sorted(cerca, key=lambda x: x[0]) if self.libre(c)), None)
        if c:
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
        self.rotulos.append((fl, c))
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

    def zona(self, rc, nombre, derecha=False, x=None):
        # el nombre de la zona, el título de su bloque: más grande y en negrita que las etiquetas, que se vea a 375
        fz = self.fz
        w = ancho_texto(nombre, fz, K_MONO) + 8
        if x is None:
            x = rc.r - 8 - w if derecha else rc.x + 8
        # el nombre se pulsa (30 de alto como poco: 24 px a 375) y pliega la zona en su sitio: una tapa con su nombre
        k = len(self.tapas)
        self.zonas_rc.append(rc)
        self.fondo.append(f'<rect class="d-zona" x="{rc.x:g}" y="{rc.y:g}" width="{rc.w:g}" height="{rc.h:g}" rx="8"/>')
        self.fondo.append('')                     # la carpeta y su nombre, en acabar(): la pestaña donde no la cruce una flecha
        self.nombres_zona.append((len(self.fondo) - 1, rc, nombre, x, w, k))
        self.tapas.append(f'<g class="d-tapa" data-zona="{k}"><rect x="{rc.x:g}" y="{rc.y:g}" width="{rc.w:g}" height="{rc.h:g}" rx="8"/>'
                          f'<text class="d-tapa-n" x="{rc.cx:g}" y="{rc.cy + self.fn * .36:.1f}" font-size="{self.fn}" text-anchor="middle">{escape(nombre)}</text></g>')
        for a, b in (((rc.x, rc.y), (rc.r, rc.y)), ((rc.r, rc.y), (rc.r, rc.b)), ((rc.x, rc.b), (rc.r, rc.b)), ((rc.x, rc.y), (rc.x, rc.b))):
            self.segs.append((a, b))

    def encuadre(self, arriba=12, abajo=16):
        """Lo que hay que mover el dibujo para centrarlo a lo ancho y dejar arriba solo su margen, y el alto que queda:
        lo que ocupan cajas, zonas, tramos de flecha y lo apartado para etiquetas y nombres."""
        rs = list(self.cajas.values()) + list(self.zonas_rc) + list(self.obst)
        xs = [r.x for r in rs] + [r.r for r in rs] + [p[0] for a in self.segs for p in a]
        ys = [r.y for r in rs] + [r.b for r in rs] + [p[1] for a in self.segs for p in a]
        if not xs:
            return 0, 0, self.H
        x0, x1, y0, y1 = min(xs) - 6, max(xs) + 6, min(ys) - 6, max(ys) + 6      # 6: el trazo ancho de un bloque
        dx = round((self.W - (x1 - x0)) / 2 - x0, 1) if x1 - x0 < self.W else 0
        dy = round(arriba - y0, 1)
        return dx, dy, round(y1 - y0 + arriba + abajo, 1)

    def carpeta_dentro(self, r, nombre, T, alt=None):
        """La carpeta de una zona de dentro a la que llega una flecha (decisión 420): su nombre en la pestaña, del tamaño
        de su cabecera, y el fondo suave de su cauce. La pestaña, al poner los nombres (donde no la cruce una flecha)."""
        self.fondo.append('')
        self.dentro_pend.append((len(self.fondo) - 1, r, nombre, T))
        self.dentro_alt[len(self.fondo) - 1] = (alt, len(self.segs))   # sin sitio para la pestaña: la cabecera sobre alt
        self.zonas_rc.append(r)
        wt = ancho_texto(nombre, self.fsz, K_MONO) + len(nombre) * self.fsz * .06 + 22
        self.tab_fin = r.x + wt + 10          # una flecha que baja a su primer paso, más allá de la pestaña
        for a, b in (((r.x, r.y + T), (r.r, r.y + T)), ((r.r, r.y + T), (r.r, r.b)), ((r.x, r.b), (r.r, r.b)), ((r.x, r.y), (r.x, r.b))):
            self.segs.append((a, b))

    def svg(self, clase, aria):
        if self.nombres_zona or self.dentro_pend:     # una maquetación que no pasa por acabar()
            self.nombres()
        p = self.pref
        defs = (f'<defs><marker id="{p}-m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8.4" markerHeight="8.4" markerUnits="userSpaceOnUse" orient="auto-start-reverse">'
                f'<path d="M0,1 L10,5 L0,9 z" class="d-punta d-pl"/><path d="M0,0.5 L10,5 L0,9.5 L0,7.6 L6.2,5 L0,2.4 z" class="d-punta d-pa"/></marker>'
                f'<marker id="{p}-m-on" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8.4" markerHeight="8.4" markerUnits="userSpaceOnUse" orient="auto-start-reverse">'
                f'<path d="M0,1 L10,5 L0,9 z" class="d-punta-on d-pl"/><path d="M0,0.5 L10,5 L0,9.5 L0,7.6 L6.2,5 L0,2.4 z" class="d-punta-on d-pa"/></marker></defs>')
        cuerpo = ''.join(self.fondo + self.flechas + self.etiquetas + self.nodos + self.plegar + self.tapas)
        alto = self.H
        if self.m.get('centrar'):
            # con bloques, cada vista se ajusta a lo que dibuja: centrada a lo ancho y sin hueco arriba, a la misma escala
            dx, dy, alto = self.encuadre()
            if dx or dy:
                cuerpo = f'<g transform="translate({dx:g} {dy:g})">{cuerpo}</g>'
        elif self.tope < 0:       # la pestaña de un bloque cerrado, arriba del todo: todo baja lo que asoma
            cuerpo = f'<g transform="translate(0 {-self.tope:g})">{cuerpo}</g>'
            alto -= self.tope
        # la forma de los bloques (decisión 415): anillo, columnas o apilado pudiendo ir de otra forma (y los hermanos)
        blq = getattr(self, 'bloques', '')
        if blq:
            blq = f' data-bloques="{blq}"'
            if blq.startswith(' data-bloques="apilado') and getattr(self, 'hermanos', None):
                blq += ' data-hermanos="' + escape(';'.join('|'.join(self.m['zonas'][z][0] for z in g) for g in self.hermanos)) + '"'
        return (f'<svg class="{clase}"{blq} viewBox="0 0 {self.W} {alto:g}" style="--d-fe:{self.fe}px" role="img" aria-labelledby="{p}-t {p}-d">'
                f'<title id="{p}-t">{escape(self.m["titulo"] or self.m["tipo"])}</title><desc id="{p}-d">{escape(aria)}</desc>{defs}{cuerpo}</svg>')

    def cabecera(self, c, nombre):
        """El nombre de una zona de dentro, sobre su primer nodo, sin pisar el centro (por donde le llega su flecha): a
        la izquierda; si no cabe, acabando antes del centro o empezando después, dentro de su zona y sin pisar cajas."""
        w = ancho_texto(nombre, self.fsz, K_MONO) + 4
        y0 = c.y - 8 - self.fsz
        zona = min((z for z in self.zonas_rc if z.x <= c.cx <= z.r and z.y <= c.cy <= z.b), key=lambda z: z.w * z.h, default=None)

        def vale(x0):
            r = R(x0, y0, w, self.fsz + 4)
            if zona is not None and (x0 < zona.x + 4 or x0 + w > zona.r - 4):
                return False
            return not any(r.corta(o) for o in list(self.cajas.values()) + self.obst)
        x, ancla = c.x + 2, ''
        if w > c.w / 2 - 8:
            if vale(c.cx - 6 - w):
                x, ancla = c.cx - 6, ' text-anchor="end"'
            elif vale(c.cx + 6):
                x = c.cx + 6
        self.fondo.append(f'<text class="d-carril d-etiqueta d-subzona" x="{x:g}" y="{c.y - 8:g}" font-size="{self.fsz}"{ancla}>{escape(nombre)}</text>')
        self.obst.append(R(x - w if ancla else x - 2, y0, w, self.fsz + 4))

    def nombres(self):
        """Los nombres de las zonas, arriba, en el primer sitio de su borde de arriba que no cruce ninguna flecha (a la
        izquierda, si se puede; si no, corrido a la derecha)."""
        tramos = [seg_rect(a, b, 3) for _, p in self.caminos for a, b in zip(p, p[1:])]
        for i, r, nombre, T_ in self.dentro_pend:      # las carpetas de dentro: su pestaña, donde no la cruce una flecha
            puesto = None
            for fz in (self.fsz, self.fe):
                wt = ancho_texto(nombre, fz, K_MONO) + len(nombre) * fz * .06 + 22
                for x_ in range(int(r.x), int(r.r - wt - 8) + 1, 4):
                    if not any(R(x_, r.y, wt, T_ + 2).corta(t) for t in tramos):
                        puesto = (fz, wt, x_)
                        break
                if puesto:
                    break
            alt, k = self.dentro_alt.get(i, (None, 0))
            if puesto is None and alt is not None:     # una zona de dentro sin flechas que le lleguen: su cabecera
                del self.segs[k:k + 4]
                self.zonas_rc.remove(r)
                self.cabecera(alt, nombre)
                continue
            if puesto is None:
                raise Error(f'no hay sitio para la pestaña de «{nombre}» sin que la cruce una flecha: un nombre más corto')
            fz, wt, x = puesto
            linea = self.color_zona.get(nombre, '')
            tinte = f' d-tinte-{linea}' if linea else ''
            self.fondo[i] = (f'<path class="d-carpeta d-carpeta-zona d-carpeta-dentro{tinte}" d="{carpeta_d(r.x, r.y, r.w, r.h, x, wt, T_)}"/>'
                             f'<text class="d-carril d-etiqueta d-zona-n" x="{x + 9:g}" y="{r.y + T_ / 2 + fz * .36:.1f}" font-size="{fz}">{escape(nombre)}</text>')
            self.obst.append(R(x - 4, r.y - 2, wt + 8, T_ + 4))
        self.dentro_pend = []
        self.dentro_alt = {}
        T = 22
        for i, rc, nombre, x0, _, k in self.nombres_zona:
            puesto = None
            # su tamaño de título; si no hay sitio libre (una zona estrecha que cruzan sus flechas), uno menor
            for fz in (self.fz, round(self.fz * .85 * 2) / 2, self.fe):
                wt = ancho_texto(nombre, fz, K_MONO) + len(nombre) * fz * .06 + 26     # con su espaciado y la diagonal
                if wt > rc.w - 16:
                    continue
                pref = min(max(x0 - 10, rc.x), rc.r - 8 - wt)
                for x_ in [pref] + list(range(int(rc.x), int(rc.r - wt - 8) + 1, 4)):
                    if not any(R(x_, rc.y, wt, T + 2).corta(t) for t in tramos):
                        puesto = (fz, wt, x_)
                        break
                if puesto:
                    break
            w_fe = ancho_texto(nombre, self.fe, K_MONO)
            if puesto is None and any(R(rc.x + 8, rc.y + 3, w_fe + 4, T - 6).corta(t) for t in tramos):
                # una zona estrecha cuyo nombre cruza una flecha: la carpeta se ensancha hacia un lado libre, para que la
                # pestaña quepa junto a la flecha sin que la cruce
                otras = [c for c in self.cajas.values() if not (rc.x <= c.cx <= rc.r and rc.y <= c.cy <= rc.b)] +                         [z for z in self.zonas_rc if z is not rc]
                cruzan = [t for t in tramos if t.corta(R(rc.x, rc.y, rc.w, T + 2))]
                for fz in (self.fz, round(self.fz * .85 * 2) / 2, self.fe):
                    wt = ancho_texto(nombre, fz, K_MONO) + len(nombre) * fz * .06 + 26
                    for x_, nr in ([(max(t.r for t in cruzan) + 2, None)] if cruzan else []) +                                   ([(min(t.x for t in cruzan) - wt - 2, 'izq')] if cruzan else []):
                        x1, x2 = min(rc.x, x_), max(rc.r, x_ + wt + 8)
                        ext = R(x1, rc.y, x2 - x1, rc.h)
                        if x1 < 4 or x2 > self.W - 4 or any(ext.corta(o) and not R(rc.x, rc.y, rc.w, rc.h).corta(o) for o in otras)                                 or any(R(x_, rc.y, wt, T + 2).corta(t) for t in tramos):
                            continue
                        viejos = [((rc.x, rc.y), (rc.r, rc.y)), ((rc.r, rc.y), (rc.r, rc.b)), ((rc.x, rc.b), (rc.r, rc.b)), ((rc.x, rc.y), (rc.x, rc.b))]
                        rc.x, rc.w = x1, x2 - x1
                        nuevos = [((rc.x, rc.y), (rc.r, rc.y)), ((rc.r, rc.y), (rc.r, rc.b)), ((rc.x, rc.b), (rc.r, rc.b)), ((rc.x, rc.y), (rc.x, rc.b))]
                        self.segs = [nuevos[viejos.index(sg)] if sg in viejos else sg for sg in self.segs]
                        self.fondo[i - 1] = f'<rect class="d-zona" x="{rc.x:g}" y="{rc.y:g}" width="{rc.w:g}" height="{rc.h:g}" rx="8"/>'
                        self.tapas[k] = (f'<g class="d-tapa" data-zona="{k}"><rect x="{rc.x:g}" y="{rc.y:g}" width="{rc.w:g}" height="{rc.h:g}" rx="8"/>'
                                         f'<text class="d-tapa-n" x="{rc.cx:g}" y="{rc.cy + self.fn * .36:.1f}" font-size="{self.fn}" text-anchor="middle">{escape(nombre)}</text></g>')
                        puesto = (fz, wt, x_)
                        break
                    if puesto:
                        break
            fz, wt, x = puesto or (self.fe, ancho_texto(nombre, self.fe, K_MONO) + 26, rc.x)
            self.obst.append(R(x - 6, rc.y - 4, wt + 12, T + 8))           # aire: ninguna etiqueta se le pega
            linea = self.color_zona.get(nombre, '')
            tinte = f' d-tinte-{linea}' if linea else ''
            self.fondo[i] = (f'<path class="d-carpeta d-carpeta-zona{tinte}" d="{carpeta_d(rc.x, rc.y, rc.w, rc.h, x, wt, T)}"/>'
                             f'<g class="d-zona-g" data-zona="{k}" data-nombre="{escape(nombre)}" tabindex="0" role="button" aria-expanded="true" '
                             f'aria-label="Plegar la zona {escape(nombre)}"><rect class="d-zona-t" x="{x:g}" y="{rc.y:g}" width="{wt:g}" height="30" rx="4"/>'
                             f'<text class="d-carril d-etiqueta d-zona-n" x="{x + 10:g}" y="{rc.y + T / 2 + fz * .36:.1f}" font-size="{fz}">{escape(nombre)}</text></g>')
        self.nombres_zona = []

    def acabar(self):
        self.nombres()
        # primero las flechas cortas, que tienen menos sitio donde poner su etiqueta; las largas, después
        largo = lambda pts: sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(pts, pts[1:]))
        for fl, puntos in sorted(self.pendientes, key=lambda x: largo(x[1])):
            self.etiqueta(fl, puntos)


# ───────────────────────── maquetaciones ─────────────────────────

def principales(m):
    return [n for n in m['orden'] if not m['nodos'][n]['clases'] & ({'salida', 'final', 'accion'} | LATERALES)]


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
    # los carriles de las vueltas largas, dentro del dibujo: la columna deja su sitio
    wcol = min(wcol, L.W - 2 * x0 - (16 * len(largas) + 8 if largas else 0))
    pide_col = max([ancho_texto(m['nodos'][n]['nombre'], L.fn, K_NEGRITA) + (32 if L.croqueta else 20) for n in prin] + [100])
    if wcol < pide_col:
        raise Error(f'{len(largas)} vueltas largas no caben a la derecha de la columna ({wcol:.0f} < {pide_col:.0f}): '
                    'lo que sale del camino, al lado; menos vueltas o nombres más cortos')
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
    # una zona de dentro cuyos nodos van seguidos en el camino: su carpeta (opción B del propietario)
    sub_ini, sub_fin = {}, {}
    for sub, ids in m.get('subzonas', []):
        if all(n in pos for n in ids) and sorted(pos[n] for n in ids) == list(range(pos[ids[0]], pos[ids[0]] + len(ids))) \
                and len({zona_de.get(n) for n in ids}) == 1:
            sub_ini.setdefault(ids[0], []).append(sub)
            sub_fin[sub] = ids[-1]
    subs_c = []
    zona_act, y_zona, zonas_rc = None, None, []
    for i, n in enumerate(prin):
        z = zona_de.get(n)
        y += (T_SUB + 6) * len(sub_ini.get(n, []))
        if z != zona_act:
            if zona_act is not None:
                zonas_rc.append((zona_act, y_zona, y - 8))
                y += 24
            if z is not None:
                y_zona = y - 8
                y += 32
            zona_act = z
        ha = alto + (L.tab_bloque(m['nodos'][n]['nombre'])[1] if 'bloque' in m['nodos'][n]['clases'] else 0)
        L.nodo(n, R(x0, y, wcol, ha))
        y += ha + (104 if i in dobles else 60) + 8 * sum(1 for s_, u in sub_fin.items() if u == n)
    y_fin = y - 60
    if zona_act is not None:
        zonas_rc.append((zona_act, y_zona, y_fin + 16))
    for z, ya, yb in zonas_rc:
        L.zona(R(8, ya, L.W - 16, yb - ya), m['zonas'][z][0], derecha=True)
    for sub, ids in m.get('subzonas', []):
        if sub in sub_fin:
            a, b = L.cajas[ids[0]], L.cajas[sub_fin[sub]]
            L.carpeta_dentro(R(a.x - 8, a.y - T_SUB - 6, a.w + 16, b.b + 8 - (a.y - T_SUB - 6)), sub, T_SUB, alt=a)
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
            if ca.b + 20 < yb:
                L.flecha(f, [(ca.cx, ca.b), (ca.cx, ca.b + 20), (cb.r + 24, ca.b + 20), (cb.r + 24, yb), (cb.r + 2, yb)])
            elif cb.y + 8 <= ca.cy <= cb.b - 8:
                L.flecha(f, [(ca.x, ca.cy), (cb.r + 2, ca.cy)])
            else:           # más abajo que su destino: sube por el hueco entre las columnas y entra por su lado
                xm = (ca.x + cb.r) / 2
                L.flecha(f, [(ca.x, ca.cy), (xm, ca.cy), (xm, cb.cy), (cb.r + 2, cb.cy)])
    L.acabar()


def eje(m, L):
    """Vertical para proceso y estados con nodos al lado (clases «lado» e «izquierda», decisión 326): el camino en una
    columna, y cada nodo de al lado en la suya, a la altura del nodo al que se une (su ancla: primero uno del eje; si no,
    uno de la otra columna). Los de al lado sin ancla se apilan en su columna, en el orden de los datos. Cada zona, un
    marco alrededor de sus nodos, en cualquier columna. Flechas: rectas entre vecinas de una columna y entre un nodo y
    su ancla; las demás, por los huecos o por un carril a la derecha (las vueltas, siempre por fuera)."""
    L.pendientes = []
    L.partir_nombres = True
    nod, op = m['nodos'], m['opciones']
    prin = principales(m)
    # a la izquierda, «izquierda» y las acciones que no van «lado»; a la derecha, «lado», las salidas y los finales
    izq = [n for n in m['orden'] if 'izquierda' in nod[n]['clases'] or ('accion' in nod[n]['clases'] and 'lado' not in nod[n]['clases'])]
    der = [n for n in m['orden'] if n not in prin and n not in izq]
    columnas = [izq, prin, der]
    col_de = {n: k for k, c in enumerate(columnas) for n in c}
    # corchetes: abarcan nodos seguidos de una columna; cuentan como de esa columna para las anclas
    corch = m.get('corchetes', {})
    for cid, (_, ids) in corch.items():
        ks = {col_de[n] for n in ids}
        pos = sorted(columnas[col_de[ids[0]]].index(n) for n in ids)
        if len(ks) > 1 or pos != list(range(pos[0], pos[0] + len(ids))):
            raise Error(f'la zona «{cid}», a la que llega una flecha, tiene pasos que no van seguidos en una columna')
        col_de[cid] = col_de[ids[0]]
    indice = lambda n: columnas[col_de[n]].index(corch[n][1][0] if n in corch else n)
    flechas = [f for f in m['flechas'] if f['de'] != 'inicio']
    vecinos = lambda n: [f['a'] if f['de'] == n else f['de'] for f in flechas if n in (f['de'], f['a']) and f['de'] != f['a']]
    # anclas: la primera unión con el eje; si no, con la otra columna. Sin cruzarse: en cada columna, en orden.
    zona_de0 = {n: z for z, (_, ids) in enumerate(m['zonas']) for n in ids}
    ancla = {}
    for c in (izq, der):
        ultimo = {}
        for n in c:
            vs = vecinos(n)
            # de su misma zona, primero: lo que vuelve a una zona va junto a los suyos, en su carpeta
            suya = [x for x in prin if zona_de0.get(x) is not None and zona_de0.get(x) == zona_de0.get(n)]
            a = next((x for x in vs if x in suya), None) or (
                next((x for x in reversed(suya) if m['orden'].index(x) < m['orden'].index(n)), None) if suya else None) or \
                next((x for x in vs if col_de[x] == 1), None) or next((x for x in vs if col_de[x] not in (1, col_de[n])), None)
            if a is None:
                continue
            k = indice(a)
            if k < ultimo.get(col_de[a], -1):
                print(f'Aviso: «{n}» no puede ir a la altura de «{a}» sin cruzarse con las de encima: va apilado', file=sys.stderr)
                continue
            ultimo[col_de[a]] = k
            ancla[n] = a
    # reparto en bus: un origen con tres flechas o más a nodos de una misma columna de al lado que no son sus anclas
    bus = {}
    for f in flechas:
        cd = col_de[f['a']]
        if cd != 1 and ancla.get(f['a']) != f['de'] and ancla.get(f['de']) != f['a']:
            bus.setdefault((f['de'], cd), []).append(f)
    bus = {k: v for k, v in bus.items() if len(v) >= 3 and not any(f['a'] in corch for f in v)}
    for f in flechas:
        x = f['a'] if f['a'] in corch else f['de'] if f['de'] in corch else None
        if x and ancla.get(f['de'] if x == f['a'] else f['a']) != x:
            raise Error(f'la zona «{x}» solo recibe flechas de un nodo de al lado, a su altura: «{f["de"]} > {f["a"]}» no puede')
    vuelta = lambda f: bool(f['clases'] & {'vuelta', 'claude'})
    zonas = m['zonas']
    zona_de = {n: z for z, (_, ids) in enumerate(zonas) for n in ids}
    PZ = 10                                          # margen de las zonas a cada lado de sus nodos
    lado_bus = {cd for _, cd in bus}
    # anchos: el cómodo (nombre en una línea) y el mínimo (nombre y detalle en dos líneas como mucho)
    margen_txt = 16 + (12 if L.croqueta else 0)

    def cabe(n, w):
        nd = nod[n]
        if 'final' in nd['clases']:
            return w >= 100
        try:
            L.partir(nd['nombre'], w - margen_txt, L.fn, K_NEGRITA)
            if nd['sub']:
                L.partir(nd['sub'], w - L.pad + 8, L.fs, K_MONO)
            return True
        except Error:
            return False

    def anchos(c):
        if not c:
            return 0, 0
        comodo = max([L.medida_nodo(n) for n in c if 'final' not in nod[n]['clases']] + [120])
        minimo = next((w for w in range(72, 400, 4) if all(cabe(n, w) for n in c)), None)
        if minimo is None:
            raise Error(f'«{max(c, key=lambda n: len(nod[n]["nombre"]))}» no cabe en una columna de la vertical: acórtalo')
        return max(minimo, min(comodo, 200 if c is prin else 160)), minimo
    w_com, w_min = zip(*(anchos(c) for c in columnas))
    usadas = [k for k in range(3) if columnas[k]]
    en_zona = [any(n in zona_de for n in c) for c in columnas]
    marcos_entre = lambda k1, k2: sum(1 for z, (_, ids) in enumerate(zonas)
                                      if any(col_de.get(n) == k1 for n in ids) != any(col_de.get(n) == k2 for n in ids))

    def hueco_col(k1, k2):
        """Entre dos columnas: 12, más el margen de cada marco que pasa entre ellas, y el sitio de la etiqueta de la
        flecha que las une; 24 como poco, para la punta."""
        etq = max([L.ancho_etq(f) + 24 for f in flechas if f['etiqueta'] and {col_de[f['de']], col_de[f['a']]} == {k1, k2}] + [0])
        return max(24, 12 + PZ * marcos_entre(k1, k2), etq)
    huecos = [hueco_col(a, b) for a, b in zip(usadas, usadas[1:])]
    en_bus = {id(f) for fs in bus.values() for f in fs}
    carriles = min(3, sum(1 for f in flechas if id(f) not in en_bus and f['a'] not in (ancla.get(f['de']),) and f['de'] not in (ancla.get(f['a']),)
                         and (vuelta(f) or (col_de[f['de']] == col_de[f['a']] and abs(indice(f['de']) - indice(f['a'])) > 1))))
    # un salto hacia abajo en el eje, con nodos a la derecha y ninguno a la izquierda: sitio para ir por la izquierda
    salto = any(not vuelta(f) and col_de[f['de']] == 1 == col_de[f['a']] and prin.index(f['a']) > prin.index(f['de']) + 1 for f in flechas)
    m_izq = 8 + (PZ if en_zona[usadas[0]] else 0) + (12 if 0 in lado_bus else 0) + (16 if salto and der and not izq else 0)
    # el carril de las vueltas, a 16 de lo de dentro (cajas, zonas y bus) y a 14 del borde del dibujo
    m_der = (14 + 16 + 12 * (carriles - 1) if carriles else 8) + (PZ if en_zona[usadas[-1]] else 0) + (12 if 2 in lado_bus else 0)
    # la etiqueta de una vuelta, junto a su carril, por fuera: si cabe, se le deja sitio (si no, va al hueco más cercano)
    etq_vuelta = max([L.ancho_etq(f) + 4 for f in flechas if f['etiqueta'] and vuelta(f)] + [0]) if carriles else 0
    if etq_vuelta and sum(w_min) <= L.W - m_izq - m_der - etq_vuelta - sum(huecos):
        m_der += etq_vuelta
    libre = L.W - m_izq - m_der - sum(huecos)
    if sum(w_min) > libre:
        raise Error(f'las columnas no caben en la vertical ({sum(w_min) + L.W - libre:.0f} > {L.W}): '
                    'nombres más cortos, menos nodos al lado o una columna menos')
    ws = list(w_min)
    for k in (1, 2, 0):                                    # lo que sobra, primero al eje y luego a los lados
        ws[k] = min(w_com[k], ws[k] + max(0, libre - sum(ws))) if columnas[k] else 0
    x, xs = m_izq + max(0, libre - sum(ws)) / 2, [0, 0, 0]
    for k, hc in zip(usadas, huecos + [0]):
        xs[k] = x
        x += ws[k] + hc

    def alto_de(n):
        nd = nod[n]
        if 'final' in nd['clases']:
            return 72
        if 'bloque' in nd['clases']:
            return L.alto + L.tab_bloque(nd['nombre'])[1]
        w = ws[col_de[n]]
        lineas = len(L.partir(nd['nombre'], w - margen_txt, L.fn, K_NEGRITA))
        subs = len(L.partir(nd['sub'], w - L.pad + 8, L.fs, K_MONO)) if nd['sub'] else 1
        return L.alto + L.pnn * (lineas - 1) + (0 if L.plegadas else L.ps * (subs - 1))
    h = {n: alto_de(n) for n in col_de if n not in corch}

    # zonas dentro de zonas: una cabecera (su nombre, sin marco) sobre su primer nodo en cada columna
    cabeceras = {}
    for nombre, ids in m.get('subzonas', []):
        for c in columnas:
            primero = next((n for n in c if n in ids), None)
            if primero:
                cabeceras.setdefault(primero, nombre)
    sub_de = {n: z for z, (_, ids) in enumerate(m.get('subzonas', [])) for n in ids}
    cab = lambda n: L.fsz + 14 if n in cabeceras else 0

    def hueco(a, b):
        """Entre dos nodos seguidos de una columna: 16 sin flecha, 28 con flecha y 60 con etiqueta; entre zonas, sus
        márgenes, el sitio del nombre de la de abajo y el de la etiqueta que cruza; y el de la cabecera de una zona de
        dentro."""
        fs = [f for f in flechas if {f['de'], f['a']} == {a, b}]
        etq = any(f['etiqueta'] for f in fs)
        za, zb = zona_de.get(a), zona_de.get(b)
        if za == zb:
            base = 60 if etq else 28 if fs else 16
            return max(base, cab(b) + 16) if b in cabeceras and sub_de.get(a) != sub_de.get(b) else base
        return (12 if za is not None else 0) + (30 if zb is not None else 0) + (L.fe + 32 if etq else 16) + cab(b)

    y0 = 16 + (44 if any(f['de'] == 'inicio' for f in m['flechas']) else 0)
    y = {}
    for c in columnas:
        for i, n in enumerate(c):
            y[n] = y0 + (30 if zona_de.get(n) is not None else 0) + cab(n) if i == 0 else 0

    def resolver():
        for _ in range(400):
            cambia = False
            for c in columnas:
                for a, b in zip(c, c[1:]):
                    v = y[a] + h[a] + hueco(a, b)
                    if y[b] < v - .01:
                        y[b], cambia = v, True
            for n, a in ancla.items():
                if a in corch:          # un corchete: su centro, del primer nodo al último
                    ids = corch[a][1]
                    ca_, mueve = (y[ids[0]] + y[ids[-1]] + h[ids[-1]]) / 2, ids[0]
                else:
                    ca_, mueve = y[a] + h[a] / 2, a
                d = ca_ - (y[n] + h[n] / 2)
                if d > .01:
                    y[n] += d
                    cambia = True
                elif d < -.01:
                    y[mueve] -= d
                    cambia = True
            if not cambia:
                return
        raise Error('no se pueden poner los nodos de al lado a la altura de su ancla: revisa el orden de los datos')

    def marcos():
        out = []
        for z, (nombre, ids) in enumerate(zonas):
            cs = [n for n in ids if n in col_de]
            if not cs:
                continue
            x1 = min(xs[col_de[n]] for n in cs) - PZ - (12 if 0 in lado_bus and any(col_de[n] == 0 for n in cs) else 0)
            x2 = max(xs[col_de[n]] + ws[col_de[n]] for n in cs) + PZ + (12 if 2 in lado_bus and any(col_de[n] == 2 for n in cs) else 0)
            y1 = min(y[n] - cab(n) for n in cs) - 30
            y2 = max(y[n] + h[n] for n in cs) + 12
            out.append((z, R(x1, y1, x2 - x1, y2 - y1)))
        return out

    resolver()
    for _ in range(12):                    # dos zonas que se pisan: la de abajo baja entera
        rc = marcos()
        par = next(((a, b) for i, a in enumerate(rc) for b in rc[i + 1:] if a[1].mas(4).corta(b[1])), None)
        if not par:
            break
        a, b = sorted(par, key=lambda t: t[1].y)
        delta = a[1].b + 16 - b[1].y
        for n in zonas[b[0]][1]:
            if n in y:
                y[n] += delta
        resolver()
    else:
        raise Error('las zonas no caben sin pisarse en la vertical: revisa qué nodos van en cada una')
    for n in m['orden']:
        L.nodo(n, R(xs[col_de[n]], y[n], ws[col_de[n]], h[n]))
    rc = marcos()
    for z, r in rc:
        L.zona(r, zonas[z][0])
    # las zonas a las que llega una flecha (decisión 420): la flecha, a su borde, del lado de lo que les llega; la de
    # dentro, con su carpeta (en el sitio de su cabecera)
    caja_corch, con_carpeta, entra_x = {}, set(), {}
    for cid, (nombre, ids) in corch.items():
        cs_ = [L.cajas[n] for n in ids]
        otros = [ancla_n for ancla_n, a in ancla.items() if a == cid]
        izquierda = any(col_de[o] < col_de[cid] for o in otros) or not otros
        if cid in m.get('zona_dentro', ()):
            r = R(min(c.x for c in cs_) - 6, cs_[0].y - cab(ids[0]), max(c.r for c in cs_) - min(c.x for c in cs_) + 12,
                  cs_[-1].b + 6 - cs_[0].y + cab(ids[0]))
            L.carpeta_dentro(r, nombre, max(cab(ids[0]) - 6, 16))
            con_carpeta.add(ids[0])
            entra_x[ids[0]] = L.tab_fin
        else:
            r = next(r for z, r in rc if zonas[z][0] == nombre)
        caja_corch[cid] = R((r.x if izquierda else r.r) - 1, cs_[0].y, 2, cs_[-1].b - cs_[0].y)
    # las demás zonas de dentro, también carpetas si en su marco no cae nada de fuera; si no, su cabecera
    hechas_c = {nombre for cid, (nombre, _) in corch.items() if cid in m.get('zona_dentro', ())}
    for nombre, ids in m.get('subzonas', []):
        primeros = [n for n in cabeceras if n in ids and cabeceras[n] == nombre]
        if nombre in hechas_c or len(primeros) != 1:
            continue
        r = carpeta_sub(L.cajas, ids, cab(primeros[0]))
        if r:
            L.carpeta_dentro(r, nombre, max(cab(primeros[0]) - 6, 16), alt=L.cajas[primeros[0]])
            con_carpeta.add(primeros[0])
            entra_x[primeros[0]] = L.tab_fin
    for n, nombre in cabeceras.items():     # la cabecera de la zona de dentro: su nombre, sobre su primer nodo
        if n not in con_carpeta:
            L.cabecera(L.cajas[n], nombre)
    bordes = [r for _, r in rc]
    y_fin = max([c.b for c in L.cajas.values()] + [r.b for r in bordes])
    L.H = L.notas(y_fin + 32) + 8
    # flechas
    hechas = set()
    usados = []

    def pon(f, pts):
        L.flecha(f, pts)
        usados.extend(zip(pts, pts[1:]))
        hechas.add(id(f))

    pares = {(f['de'], f['a']) for f in flechas}
    for f in m['flechas']:
        if f['de'] == 'inicio':
            c = L.cajas[f['a']]
            L.fondo.append(f'<circle class="d-ini" cx="{c.cx:g}" cy="{c.y - 38:g}" r="6"/>')
            L.flecha(f, [(c.cx, c.y - 32), (c.cx, c.y - 2)])
            hechas.add(id(f))
    for f in flechas:                       # vecinas de una misma columna: rectas
        a, b = f['de'], f['a']
        c = columnas[col_de[a]]
        if a not in corch and b not in corch and col_de[a] == col_de[b] and abs(c.index(a) - c.index(b)) == 1:
            ca, cb = L.cajas[a], L.cajas[b]
            baja = c.index(b) > c.index(a)
            w = L.ancho_etq(f) + 8 if f['etiqueta'] else 0
            dx = (-12 if baja else 12) if (b, a) in pares else 0
            # por el centro si la etiqueta cabe a su derecha, hasta la caja de al lado que haya a esa altura
            y1_, y2_ = sorted((ca.b, cb.y) if baja else (cb.b, ca.y))
            tope = min([L.cajas[n].x for n in col_de if n in L.cajas and L.cajas[n].x > ca.cx
                        and L.cajas[n].y < y2_ and L.cajas[n].b > y1_] + [L.W - 8])
            x_ = ca.cx + dx if w <= tope - ca.cx - 12 or dx else ca.x + 24
            if b in entra_x and baja:            # a la carpeta de dentro: junto a su pestaña, sin cruzarla
                x_ = min(max(x_, entra_x[b]), cb.r - 10)
            pon(f, [(x_, ca.b), (x_, cb.y - 2)] if baja else [(x_, ca.y), (x_, cb.b + 2)])
    for f in flechas:                       # un nodo y su ancla: recta, a su altura
        a, b = f['de'], f['a']
        if id(f) in hechas or not (ancla.get(a) == b or ancla.get(b) == a):
            continue
        ca, cb = caja_corch.get(a) or L.cajas[a], caja_corch.get(b) or L.cajas[b]
        dy = (-8 if a < b else 8) if (b, a) in pares else 0
        yy = (ca.cy if a not in corch else cb.cy) + dy
        pon(f, [(ca.r, yy), (cb.x - 2, yy)] if cb.x > ca.r else [(ca.x, yy), (cb.r + 2, yy)])
    for (o, cd), fs in bus.items():         # reparto en bus: un tronco por fuera de la columna y ramas cortas
        fs = [f for f in fs if id(f) not in hechas]
        if not fs:
            continue
        co = L.cajas[o]
        cajas_d = [L.cajas[f['a']] for f in fs]
        derecha = cd == 2 or (cd == 1 and co.cx < cajas_d[0].cx)
        xt = max(c.r for c in cajas_d) + 12 if derecha else min(c.x for c in cajas_d) - 12
        ys = co.cy if (co.r < xt if derecha else co.x > xt) else None
        for f in fs:
            cb = L.cajas[f['a']]
            if ys is None:                      # el origen está en la misma columna: sale por su lado de fuera
                inicio = [(co.r if derecha else co.x, co.cy)]
            else:
                inicio = [(co.r if derecha else co.x, ys)]
            pon(f, inicio + [(xt, inicio[0][1]), (xt, cb.cy), (cb.r + 2 if derecha else cb.x - 2, cb.cy)])
    for f in flechas:                       # un salto en el eje, hacia abajo: por el lado sin nodos al lado a esa altura
        a, b = f['de'], f['a']
        if id(f) in hechas or vuelta(f) or col_de[a] != 1 or col_de[b] != 1 or prin.index(b) <= prin.index(a) + 1:
            continue
        ca, cb = L.cajas[a], L.cajas[b]
        entre = [L.cajas[n] for n in prin[prin.index(a):prin.index(b) + 1]]
        for derecha in (True, False):
            xr = max(c.r for c in entre) + 14 if derecha else min(c.x for c in entre) - 14
            ocupado = any((c.x < xr + 8 and c.r > xr - 8) for n, c in L.cajas.items() if col_de[n] != 1 and c.y < cb.cy and c.b > ca.cy)
            ocupado = ocupado or any(seg_rect((xr, ca.cy), (xr, cb.cy), 6).corta(seg_rect(p, q, .5)) for p, q in usados)
            if not ocupado and 8 <= xr <= L.W - 8:
                lado_a, lado_b = (ca.r, cb.r + 2) if derecha else (ca.x, cb.x - 2)
                pon(f, [(lado_a, ca.cy), (xr, ca.cy), (xr, cb.cy), (lado_b, cb.cy)])
                break
    resto = [f for f in flechas if id(f) not in hechas]
    if resto:
        etq = lambda f: (L.ancho_etq(f), L.fe + 8)
        for f, pts in zip(resto, enrutar_v(resto, L.cajas, L.W, etq, usados, bordes, vuelta)[0]):
            L.flecha(f, pts)
    L.acabar()


def grupos_zonas(m):
    """Los nodos por zona, en el orden en que la zona los nombra; los que no van en ninguna, en un grupo sin marco,
    delante si el primero de ellos va antes que todos los de las zonas, y si no, detrás."""
    zona_de = {n: z for z, (_, ids) in enumerate(m['zonas']) for n in ids}
    grupos = [(nombre, [n for n in ids if zona_de.get(n) == z]) for z, (nombre, ids) in enumerate(m['zonas'])]
    sueltos = [n for n in m['orden'] if n not in zona_de]
    if sueltos:
        delante = m['orden'].index(sueltos[0]) < min((m['orden'].index(n) for n in zona_de), default=0)
        grupos = [('', sueltos)] + grupos if delante else grupos + [('', sueltos)]
    return [g for g in grupos if g[1]]


def rutas_v(ca, cb, W, calles, margen):
    """Caminos ortogonales posibles de la caja ca a la cb en la vertical, de los más cortos a los más largos: recto si
    se miran, en Z por el hueco de una de las dos filas, en L, por una calle entre columnas y por un carril a la derecha
    de las cajas (margen: su borde derecho)."""
    cands = []
    sx = max(ca.x, cb.x), min(ca.r, cb.r)
    sy = max(ca.y, cb.y), min(ca.b, cb.b)
    if sx[1] - sx[0] >= 24:
        for x in ((sx[0] + sx[1]) / 2, sx[0] + 16, sx[1] - 16):
            cands.append([(x, ca.b), (x, cb.y - 2)] if cb.y > ca.b else [(x, ca.y), (x, cb.b + 2)])
    if sy[1] - sy[0] >= 24:
        for yy in ((sy[0] + sy[1]) / 2, sy[0] + 14, sy[1] - 14):
            cands.append([(ca.r, yy), (cb.x - 2, yy)] if cb.x > ca.r else [(ca.x, yy), (cb.r + 2, yy)])
    baja = cb.cy > ca.cy
    sale, entra = (ca.b, cb.y - 2) if baja else (ca.y, cb.b + 2)
    xs_a = (ca.cx, ca.x + 24, ca.r - 24)
    xs_b = (cb.cx, cb.x + 24, cb.r - 24)
    if abs(cb.cy - ca.cy) > 8:
        for d in (20, 12, 28):
            for ym in ((ca.b + d, cb.y - d) if baja else (ca.y - d, cb.b + d)):
                for xa in xs_a:
                    for xb in xs_b:
                        if abs(xa - xb) > 2:
                            cands.append([(xa, sale), (xa, ym), (xb, ym), (xb, entra)])
        derecha = cb.cx > ca.cx
        lado_a = ca.r if derecha else ca.x
        for xb in xs_b:
            if (xb > lado_a) == derecha:
                cands.append([(lado_a, ca.cy), (xb, ca.cy), (xb, entra)])
        lado_b = cb.x - 2 if derecha else cb.r + 2
        for xa in xs_a:
            if (xa < lado_b) == derecha:
                cands.append([(xa, sale), (xa, cb.cy), (lado_b, cb.cy)])
        y1, y2 = (ca.b + 20, cb.y - 20) if baja else (ca.y - 20, cb.b + 20)
        # por una calle, cada flecha su carril: el centro y, si está ocupado, a 10 a un lado o al otro
        for dx in (0, -10, 10):
            for xs in calles:
                for xa in xs_a:
                    for xb in xs_b:
                        cands.append([(xa, sale), (xa, y1), (xs + dx, y1), (xs + dx, y2), (xb, y2), (xb, entra)])
    # por un carril a la derecha de las cajas, cada flecha el suyo, a 12 de la anterior
    for j in range(8):
        xm = margen + 16 + 12 * j
        if xm > W - 14:
            break
        for ya in (ca.cy, ca.cy - 12, ca.cy + 12):
            for yb in (cb.cy, cb.cy - 12, cb.cy + 12):
                if xm > max(ca.r, cb.r) + 8:
                    cands.append([(ca.r, ya), (xm, ya), (xm, yb), (cb.r + 2, yb)])

    def largo(p):
        return sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(p, p[1:])) + 48 * (len(p) - 2)
    return sorted(cands, key=largo), largo


def ruta_libre(p, propias, cajas, usados, cruzar=False):
    """Que el camino p no pase por otra caja ni toque otra flecha; con cruzar, puede cruzar otra en ángulo recto."""
    otros = [c for n, c in cajas.items() if n not in propias]
    tramos = list(zip(p, p[1:]))
    if any(seg_rect(a, b, 4).corta(o) for a, b in tramos for o in otros):
        return False
    vertical = lambda a, b: a[0] == b[0]
    return not any(seg_rect(a, b, 6).corta(seg_rect(c, d, .5)) for a, b in tramos for c, d in usados
                   if not (cruzar and vertical(a, b) != vertical(c, d)
                           and not seg_rect(a, b, 6).corta(seg_rect(c, c, .5)) and not seg_rect(a, b, 6).corta(seg_rect(d, d, .5))))


def calles_de(cajas):
    """Las calles verticales: el centro del hueco entre dos cajas vecinas de una misma fila."""
    v = list(cajas.values())
    return sorted({(c.r + d.x) / 2 for c in v for d in v if c.y == d.y and d.x > c.r
                   and not any(e.y == c.y and c.r < e.x < d.x for e in v)})


def enrutar_v(flechas, cajas, W, etq, usados0=(), bordes=(), fuera=lambda f: False):
    """Un camino para cada flecha, en orden; devuelve los caminos y su coste (lo que mide la colocación). Con etiqueta,
    mejor un camino que le deje sitio junto a un tramo (etq(f): su ancho y su alto). usados0: tramos ya puestos;
    bordes: zonas, cuyos carriles van por fuera; fuera(f): la flecha va por un carril a la derecha (una vuelta)."""
    usados, caminos, coste = list(usados0), [], 0
    calles = calles_de(cajas)

    def sitio(f, p, segs):
        w, h = etq(f)
        return any(c.x >= 4 and c.r <= W - 4 and not any(c.corta(o.mas(4)) for o in cajas.values())
                   and not any(c.corta(seg_rect(a, b, 5.5)) for a, b in segs) for c in sitios_etiqueta(p, w, h))

    def cabe(f, p):
        """Que su etiqueta tenga sitio, y que no se lo quite a las de las flechas ya puestas."""
        segs = usados + list(zip(p, p[1:]))
        return all(sitio(g, q, segs) for g, q in zip(flechas, caminos + [p]) if g['etiqueta'])

    for f in flechas:
        ca, cb = cajas[f['de']], cajas[f['a']]
        # los carriles, a la derecha de las cajas que hay entre las dos filas
        y0, y1 = min(ca.y, cb.y), max(ca.b, cb.b)
        derecha = max([c.r for c in cajas.values() if c.b >= y0 and c.y <= y1] + [z.r for z in bordes if z.b >= y0 and z.y <= y1])
        cands, largo = rutas_v(ca, cb, W, calles, derecha)
        if fuera(f):
            cands = [p for p in cands if len(p) == 4 and p[1][0] >= derecha]
        libres = [p for p in cands if ruta_libre(p, (f['de'], f['a']), cajas, usados)]
        pts = next((p for p in libres if cabe(f, p)), None) if etq else (libres[0] if libres else None)
        k = largo(pts) if pts else 0
        if pts is None and libres:
            pts, k = libres[0], largo(libres[0]) + 150
        if pts is None:     # si no hay otro, uno que cruce otra flecha en ángulo recto (lejos de sus extremos)
            pts = next((p for p in cands if ruta_libre(p, (f['de'], f['a']), cajas, usados, True)), None)
            k = largo(pts) + 300 if pts else 0
        if pts is None:
            pts, k = (cands[-1] if cands else [(ca.cx, ca.b), (cb.cx, cb.y - 2)]), 2000
        usados.extend(zip(pts, pts[1:]))
        caminos.append(pts)
        coste += k
    return caminos, coste


def trozos(m, ids):
    """Los nodos de una zona, partidos en trozos: los de cada zona de dentro (seguidos, con su nombre) y los demás."""
    subz = sorted(m.get('subzonas', []), key=lambda z: -len(z[1]))
    out, i = [], 0
    while i < len(ids):
        sz = next(((nom, s) for nom, s in subz if s and ids[i:i + len(s)] == s and len(s) < len(ids)), None)
        if sz:
            out.append(sz)
            i += len(sz[1])
            continue
        if out and not out[-1][0]:
            out[-1][1].append(ids[i])
        else:
            out.append(('', [ids[i]]))
        i += 1
    return out


T_SUB = 20      # el alto de la pestaña de una zona de dentro, fuera del eje


def a_carpeta(m, L, flechas, marcos=()):
    """Fuera del eje, una flecha a una zona (decisión 420) se enruta a su paso de en medio y se corta donde entra en
    la carpeta de la zona (la de dentro, de L.dentro_pend; la de primer nivel, de marcos: [(nombre, rect)]); sin
    carpeta dibujada, se queda en ese paso."""
    rcs = {nombre: R(r.x, r.y + T, r.w, r.h - T) for _, r, nombre, T in L.dentro_pend}
    rcs.update({nombre: r for nombre, r in marcos if nombre not in rcs})
    out = []
    for f in flechas:
        if f['a'] in m.get('corchetes', {}):
            nombre, ids = m['corchetes'][f['a']]
            medio = ids[len(ids) // 2]
            out.append(dict(f, a=medio, zona=f['a'], zona_rc=rcs.get(nombre)) if nombre in rcs else dict(f, a=medio))
        else:
            out.append(f)
    return out


def recortar(pts, r):
    """El camino hasta donde entra en el rectángulo r, a 2 de su borde; si no entra desde fuera, entero."""
    fuera = lambda p: not (r.x < p[0] < r.r and r.y < p[1] < r.b)
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        if not fuera(a):
            continue
        if a[0] == b[0] and r.x < a[0] < r.r:
            for yb in (r.y, r.b):
                if min(a[1], b[1]) <= yb <= max(a[1], b[1]) and a[1] != yb:
                    return pts[:i + 1] + [(a[0], yb - 2 if b[1] > a[1] else yb + 2)]
        if a[1] == b[1] and r.y < a[1] < r.b:
            for xb in (r.x, r.r):
                if min(a[0], b[0]) <= xb <= max(a[0], b[0]) and a[0] != xb:
                    return pts[:i + 1] + [(xb - 2 if b[0] > a[0] else xb + 2, a[1])]
    return pts


def rejilla_v(m, L):
    """Vertical para arquitectura y piezas: cada zona, una banda; dentro, sus nodos en filas de hasta tres cajas, tantas
    como quepan con su nombre entero (el detalle puede ir en dos líneas). Si dos cajas de una zona se unen con una
    flecha con etiqueta, el hueco entre columnas deja sitio a la etiqueta. Dentro de cada zona, las cajas se colocan
    donde sus flechas salgan más cortas (a igualdad, en el orden de los datos): rectas si se miran, en L o en Z por los
    huecos si no, por una calle entre columnas y, si no hay otro camino, por el margen derecho."""
    L.pendientes = []
    L.partir_nombres = True
    flechas = [f for f in m['flechas'] if f['de'] != 'inicio']
    etq = lambda f: (L.ancho_etq(f), L.fe + 8)
    zonas = bool(m['zonas'])
    xi = 24 if zonas else 16
    dentro = L.W - 2 * xi

    def reparto(ids, k, partir):
        """Hueco entre columnas, ancho, líneas del nombre y del detalle con k cajas por fila; None si algo no cabe.
        Con partir, un nombre que no cabe va en dos líneas."""
        gx = 24
        if k > 1:
            gx = max([gx] + [L.ancho_etq(f) + 24 for f in flechas if f['etiqueta'] and f['de'] in ids and f['a'] in ids])
        w = (dentro - gx * (k - 1)) / k
        if k == 1:
            w = min(dentro, max([L.medida_nodo(n) for n in ids] + [160]))
        try:
            margen = 16 + (12 if L.croqueta else 0)      # el de Lienzo.nodo, que parte el nombre
            nombres = max(1 if L.medida_nodo(n, sub=False) <= w else
                          len(L.partir(L.m['nodos'][n]['nombre'], w - margen, L.fn, K_NEGRITA)) if partir else 9 for n in ids)
            lineas = max(L.lineas_sub(n, w) for n in ids)
        except Error:
            return None
        return (gx, w, nombres, lineas) if lineas <= 2 and nombres <= 2 else None

    grupos_z = grupos_zonas(m)
    y = 16
    hueco_fila, bandas, huecos, cadenas, grupos, subs = 40, [], [], [], [], []
    for gi, (nombre, ids_z) in enumerate(grupos_z):
        y0 = y
        # arriba, el sitio del nombre de la zona; sin zona, el de la etiqueta de la flecha que llega de la de encima
        y += 32 if nombre else 24 if gi else 0
        # una zona de dentro, su trozo con su carpeta (opción B del propietario)
        partes = trozos(m, ids_z) if nombre else [('', ids_z)]
        for pi, (sub, ids) in enumerate(partes):
            if pi:
                y += hueco_fila
            if sub:
                y += T_SUB + 6
            # tres por fila, dos, dos con algún nombre en dos líneas, o una
            # plegadas, tres por fila aunque algún nombre vaya en dos líneas: compactas
            intentos = [(k, p) for k, p in ((3, False), (3, L.plegadas), (2, False), (2, True), (1, False)) if k <= len(ids)]
            k, r = next(((k, x) for k, p in intentos for x in [reparto(ids, k, p)] if x), (0, None))
            if r is None:
                raise Error(f'los nodos de «{sub or nombre or "fuera de las zonas"}» no caben en la vertical: acorta sus nombres')
            gx, w, nombres, lineas = r
            h = L.alto + L.pnn * (nombres - 1) + (0 if L.plegadas else L.ps * (lineas - 1))
            # una cadena (cada nodo de la zona, con flecha al siguiente): en serpentina, en el orden de la zona
            cadena = k > 1 and all(any(f['de'] == a and f['a'] == b for f in flechas) for a, b in zip(ids, ids[1:]))
            col = lambda i: (k - 1 - i % k) if cadena and (i // k) % 2 else i % k
            huecos.append([R(xi + col(i) * (w + gx), y + (i // k) * (h + hueco_fila), w, h) for i in range(len(ids))])
            cadenas.append(cadena)
            grupos.append((sub or nombre, ids))
            y1 = y
            y += ((len(ids) + k - 1) // k) * (h + hueco_fila) - hueco_fila
            if sub:
                subs.append((sub, R(xi - 8, y1 - T_SUB - 6, dentro + 16, y + 8 - (y1 - T_SUB - 6))))
                y += 8
        if nombre:
            bandas.append((nombre, R(8, y0, L.W - 16, y + 16 - y0)))
        y += (16 if nombre else 8) + (24 if gi < len(grupos_z) - 1 else 0)
    y_fin = y - 8
    # Colocación: la de las cajas de cada zona con las flechas más cortas y con sitio para sus etiquetas (a igualdad,
    # en el orden de los datos). Todas las zonas a la vez si las combinaciones son pocas; si no, zona a zona.
    def coste(puestas, perms, rapido=False):
        fs = [f for f in flechas if f['de'] in puestas and f['a'] in puestas]
        return enrutar_v(fs, puestas, L.W, None if rapido else etq)[1] + 4 * sum(abs(p[i] - i) for p in perms for i in range(len(p)))

    def mejor(cands, perms):
        """La de menor coste: primero sin mirar las etiquetas (rápido) y, entre las doce mejores, mirándolas."""
        cands = sorted(cands, key=lambda c: coste(c, perms(c), True))[:12]
        return min(cands, key=lambda c: coste(c, perms(c)))

    def colocar(base, gs, perms):
        out = dict(base)
        for ((_, ids), sitios), perm in zip(gs, perms):
            out.update({n: sitios[perm[i]] for i, n in enumerate(ids)})
        return out

    gs = list(zip(grupos, huecos))
    opciones = [[tuple(range(len(ids)))] if cad or len(ids) > 7 else list(permutations(range(len(ids))))
                for ids, cad in zip((g[1] for g in grupos), cadenas)]
    total = 1
    for o in opciones:
        total *= len(o)
    if total <= 150 and len(grupos) > 1:
        orden = lambda pu: [tuple(sorted(range(len(ids)), key=lambda i: pu[ids[i]].y * 1000 + pu[ids[i]].x)) for _, ids in grupos]
        puestas = mejor([colocar({}, gs, perms) for perms in product(*opciones)], orden)
    else:
        puestas = {}
        for g, ops in zip(gs, opciones):
            ids = g[0][1]
            puestas = mejor([colocar(puestas, [g], [perm]) for perm in ops],
                            lambda pu: [tuple(sorted(range(len(ids)), key=lambda i: pu[ids[i]].y * 1000 + pu[ids[i]].x))])
    for n in m['orden']:
        L.nodo(n, puestas[n])
    L.H = L.notas(y_fin + 32) + 8
    primero = {sub: ids for sub, ids in grupos}
    for sub, rc in subs:
        L.carpeta_dentro(rc, sub, T_SUB, alt=min((L.cajas[n] for n in primero[sub]), key=lambda c: (c.y, c.x)))
    flechas = a_carpeta(m, L, flechas, bandas)
    for f, pts in zip(flechas, enrutar_v(flechas, L.cajas, L.W, etq)[0]):
        L.flecha(f, pts)
    # el nombre de cada zona, arriba a la derecha; si una flecha lo cruza, donde no (Lienzo.nombres)
    for nombre, rc in bandas:
        L.zona(rc, nombre, derecha=True)
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
    # cada columna, sus trozos; una zona de dentro, con su carpeta (y, si empieza la columna, más abajo: su pestaña)
    cols = []
    for (nombre, ids), w in zip(grupos, anchos):
        ys, subs, yy = {}, [], 56
        for sub, tr in (trozos(m, ids) if nombre else [('', ids)]):
            if sub and yy == 56:
                yy += T_SUB + 4
            for n in tr:
                ys[n] = yy
                yy += paso
            if sub:
                subs.append((sub, tr))
                yy += 8
        cols.append((ys, subs, yy - paso + alto))
    fondo = max(c[2] for c in cols)
    marcos = []
    for (nombre, ids), w, (ys, subs, _) in zip(grupos, anchos, cols):
        if nombre:
            marcos.append((nombre, R(x, 16, w + 48, fondo + 24 - 16)))
            L.zona(marcos[-1][1], nombre)
        for n in ids:
            L.nodo(n, R(x + 24, ys[n], w, alto))
        for sub, tr in subs:
            y1 = ys[tr[0]] - T_SUB - 6
            L.carpeta_dentro(R(x + 16, y1, w + 16, ys[tr[-1]] + alto + 8 - y1), sub, T_SUB, alt=L.cajas[tr[0]])
        x += w + 48 + hueco
    y_fin = fondo + 32
    L.H = L.notas(y_fin + 16) + 8
    enrutar(dict(m, flechas=a_carpeta(m, L, m['flechas'], marcos)), L)
    L.acabar()


def rejilla_filas(m, L, grupos):
    anchos = max(L.medida_nodo(n, 200) for _, ids in grupos for n in ids)
    etq = max([L.ancho_etq(f) for f in m['flechas']] + [40])
    hueco = max(80, etq + 32)
    w = min(anchos, (L.W - 64 - 2 * hueco) / 3)
    alto = L.alto
    paso = alto + 60
    # una zona de dentro cuyos nodos van seguidos en una fila: su carpeta (en la primera fila, más abajo: su pestaña)
    subs = [(sub, tr) for sub, tr in trozos(m, [n for _, ids in grupos for n in ids]) if sub]
    fila_de = {n: k for k, (_, ids) in enumerate(grupos) for n in ids}
    subs = [(sub, tr) for sub, tr in subs if len({fila_de[n] for n in tr}) == 1]
    y = 64 + (T_SUB + 4 if any(fila_de[tr[0]] == 0 for _, tr in subs) else 0)
    for nombre, ids in grupos:
        for i, n in enumerate(ids):
            L.nodo(n, R(40 + i * (w + hueco), y, w, alto))
        y += paso
    for sub, tr in subs:
        a, b = L.cajas[tr[0]], L.cajas[tr[-1]]
        L.carpeta_dentro(R(a.x - 8, a.y - T_SUB - 6, b.r - a.x + 16, alto + T_SUB + 14), sub, T_SUB, alt=a)
    marcos = []
    if m['zonas']:
        marcos.append((m['zonas'][0][0], R(16, 16, L.W - 32, y - paso + alto + 24)))
        L.zona(marcos[0][1], m['zonas'][0][0])
    y_fin = y - paso + alto + 40
    fuera = [n for n in m['orden'] if n not in L.cajas]
    for i, n in enumerate(fuera):
        wf = L.medida_nodo(n, 200)
        L.nodo(n, R(L.W / 2 - wf / 2, y_fin + 32, wf, alto))
        y_fin += 32 + alto
    L.H = L.notas(y_fin + 24) + 8
    enrutar(dict(m, flechas=a_carpeta(m, L, m['flechas'], marcos)), L)
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


# ───────────────────────── bloques: ciclo o jerarquía (decisión 415) ─────────────────────────
# El primer paso al colocar las zonas de un flujo: el grafo de bloques (las zonas de primer nivel; las aristas, todas
# las flechas entre ellas salvo las de las acciones). Si hay un ciclo entre bloques, en anillo: lado a lado, alternando
# el sentido, para que el ciclo se cierre en su sitio; si es una jerarquía en un solo sentido, en columnas por orden, y
# lo supeditado al lado de lo que depende. Se mide contra la forma apilada y se queda la que mejor se lee; «anillo:» o
# «columnas:» en los datos la fijan y «opciones: una-columna» lo apaga.

def _fuertes(n, suc):
    """Componentes fuertemente conexas (Tarjan) de un grafo de n vértices."""
    indice, bajo, pila, en_pila, out, k = {}, {}, [], set(), [], [0]

    def visita(v):
        indice[v] = bajo[v] = k[0]
        k[0] += 1
        pila.append(v)
        en_pila.add(v)
        for w in suc[v]:
            if w not in indice:
                visita(w)
                bajo[v] = min(bajo[v], bajo[w])
            elif w in en_pila:
                bajo[v] = min(bajo[v], indice[w])
        if bajo[v] == indice[v]:
            c = []
            while True:
                w = pila.pop()
                en_pila.discard(w)
                c.append(w)
                if w == v:
                    break
            out.append(sorted(c))
    for v in range(n):
        if v not in indice:
            visita(v)
    return out


def bloques(m):
    """El grafo de bloques y su forma: {'forma': 'anillo' | 'columnas', 'orden': [zonas], 'ciclo': [zonas],
    'hermanos': [[zonas]]} o None si no hay bloques que colocar así (menos de dos zonas, o nodos fuera de las zonas)."""
    zonas = m['zonas']
    if len(zonas) < 2 or m.get('una_columna'):
        return None
    zd = {n: z for z, (_, ids) in enumerate(zonas) for n in ids}
    for cid, (_, ids) in m.get('corchetes', {}).items():
        zd[cid] = zd.get(ids[0])
    acc = {n for n, d in m['nodos'].items() if 'accion' in d['clases']}
    if any(n not in zd and n not in acc for n in m['nodos']):
        return None
    ar = {}
    for f in m['flechas']:
        if f['de'] in acc or f['a'] in acc or f['de'] == 'inicio':
            continue
        a, b = zd.get(f['de']), zd.get(f['a'])
        if a is not None and b is not None and a != b:
            ar.setdefault((a, b), []).append(f)
    k = len(zonas)
    # por partes: (1) los pares con flechas en los dos sentidos (ida y vuelta) cuentan por su ida, la que lleva el flujo
    # (si no se distingue, la que sale del bloque que va antes), y se dibujan vecinos con la ida y la vuelta separadas;
    # (2) un ciclo de la ida, en anillo, abarque todos los bloques o solo algunos (el resto cuelga de él)
    vuelta_ = lambda f: bool(f['clases'] & {'vuelta', 'claude'})
    ini = next((zd.get(f['a']) for f in m['flechas'] if f['de'] == 'inicio' and zd.get(f['a']) is not None), None)
    primero = {z: (z != ini, min((m['orden'].index(n) for n in ids if n in m['orden']), default=0)) for z, (_, ids) in enumerate(zonas)}
    peso = lambda a, b: sum(not vuelta_(f) for f in ar[(a, b)])
    dobles = sorted((a, b) for (a, b) in ar if (b, a) in ar and a < b)
    red = dict(ar)
    for a, b in dobles:
        ida = (a, b) if (peso(a, b), primero[b]) > (peso(b, a), primero[a]) else (b, a)
        del red[(ida[1], ida[0])]
    suc = {z: sorted({b for (a, b) in red if a == z}) for z in range(k)}
    pre = {z: sorted({a for (a, b) in red if b == z}) for z in range(k)}
    fijo = m.get('forma_bloques')
    ciclo = max((c for c in _fuertes(k, suc) if len(c) >= 2), key=len, default=None)
    base = {'hermanos': [], 'aristas': ar, 'dobles': dobles}
    if fijo:
        forma, orden = fijo
        return dict(base, forma=forma, orden=orden, ciclo=orden if forma == 'anillo' else None)
    if ciclo:
        # todos en el ciclo: empieza por el bloque al que vuelve una vuelta (lo que cierra el ciclo); si no, por el
        # primero del ciclo. Solo algunos: por el del inicio o al que llega lo de fuera
        dentro = set(ciclo)
        entra = [b for (a, b) in red if b in dentro and a not in dentro]
        vuelve = [b for (a, b), fs in red.items() if any(vuelta_(f) for f in fs)]
        if len(dentro) == k:
            inicio = vuelve[0] if vuelve else ciclo[0]
        else:
            inicio = ini if ini in dentro else (entra[0] if entra else min(dentro, key=primero.get))
        anillo = [inicio]
        while len(anillo) < len(dentro):
            cand = [b for b in suc[anillo[-1]] if b in dentro and b not in anillo]
            if not cand:
                break
            cand.sort(key=lambda b: (not any('flujo' in f['clases'] for f in red[(anillo[-1], b)]), b))
            anillo.append(cand[0])
        anillo += sorted((z for z in dentro if z not in anillo), key=primero.get)
        # lo demás cuelga del anillo: en el orden de la ida (primero lo que sale de él, por cercanía)
        resto, frontera = [], list(anillo)
        while len(anillo) + len(resto) < k:
            cand = [z for z in range(k) if z not in anillo and z not in resto and any(y in frontera for y in suc[z] + pre[z])]
            if not cand:
                cand = [z for z in range(k) if z not in anillo and z not in resto]
            z = min(cand, key=primero.get)
            resto.append(z)
            frontera.append(z)
        return dict(base, forma='anillo', orden=anillo + resto, ciclo=anillo, ida=red)
    # jerarquía: orden topológico; hermanos, los que tienen los mismos de antes y no se unen entre sí
    orden, grado = [], {z: len(pre[z]) for z in range(k)}
    libres = [z for z in range(k) if not grado[z]]
    while libres:
        z = libres.pop(0)
        orden.append(z)
        for b in suc[z]:
            grado[b] -= 1
            if not grado[b]:
                libres.append(b)
                libres.sort()
    grupos = {}
    for z in range(k):
        if pre[z]:
            grupos.setdefault(tuple(pre[z]), []).append(z)
    hermanos = [g for g in grupos.values() if len(g) > 1]
    return dict(base, forma='columnas', orden=orden, ciclo=None, hermanos=hermanos)


def _topo(ids, aristas):
    grado = {n: 0 for n in ids}
    for a, b in aristas:
        grado[b] += 1
    out, libres = [], [n for n in ids if not grado[n]]
    while libres:
        n = libres.pop(0)
        out.append(n)
        for a, b in aristas:
            if a == n:
                grado[b] -= 1
                if not grado[b]:
                    libres.append(b)
                    libres.sort(key=ids.index)
    return out + [n for n in ids if n not in out]


def en_bloques(m, L, blq, marcos=None):
    """Las zonas como bloques: en anillo (el primero, una fila arriba; los demás, columnas que alternan el sentido: una
    baja y la siguiente sube, para que cada paso entre bloques sea un puente corto y la vuelta cierre arriba) o en
    columnas por orden. En cada bloque, su camino en línea recta y lo de al lado a la altura de su ancla: lo de fuera
    del anillo, por fuera; las acciones del primero, por dentro. Con marcos=False (el resumen de los bloques cerrados),
    sin marcos ni cabeceras; con un conjunto, solo esas zonas llevan marco (por omisión, el de los datos o todas). Si
    no cabe, Error."""
    if marcos is None:
        marcos = m.get('marcos_bloques', True)
    L.pendientes, L.partir_nombres = [], True
    nod, zonas, orden = m['nodos'], m['zonas'], blq['orden']
    corch = m.get('corchetes', {})
    fl = [f for f in m['flechas'] if f['de'] != 'inicio']
    acc = {n for n in nod if 'accion' in nod[n]['clases']}
    zd = {n: z for z, (_, ids) in enumerate(zonas) for n in ids}
    vuelta = lambda f: bool(f['clases'] & {'vuelta', 'claude'})
    anillo = blq['forma'] == 'anillo'
    # el anillo puede abarcar solo algunos bloques (los primeros del orden): lo demás cuelga de él, en columnas a su lado
    ciclo_ = [z for z in (blq.get('ciclo') or orden) if z in orden] if anillo else []
    arriba = anillo and len(ciclo_) >= 3
    fila_z = orden[0] if arriba else None
    cols = orden[1:] if arriba else list(orden)
    nc = len(ciclo_) - 1 if arriba else len(cols)          # las columnas del anillo, las primeras
    ida = blq.get('ida') or blq.get('aristas') or {}
    if anillo:
        sig = {z: ciclo_[(i + 1) % len(ciclo_)] for i, z in enumerate(ciclo_)}
        for z in orden:
            if z not in sig:
                sig[z] = next((b for (a, b) in ida if a == z and b not in ciclo_), None)
    else:
        sig = {z: (orden[i + 1] if i + 1 < len(orden) else None) for i, z in enumerate(orden)}
    ant = {v: k for k, v in sig.items() if v is not None}
    for z in orden:
        if z not in ant and anillo and z not in ciclo_:
            ant[z] = next((a for (a, b) in ida if b == z), None)
    entradas = lambda z: [f['a'] for f in fl if zd.get(f['a']) == z and ant.get(z) is not None and zd.get(f['de']) == ant[z] and f['de'] not in acc]
    salidas = lambda z: [f['de'] for f in fl if zd.get(f['de']) == z and sig.get(z) is not None and zd.get(f['a']) == sig[z] and f['a'] not in acc]
    LAT = LATERALES | {'accion', 'salida'}
    eje_de, lat_de = {}, {}
    for z in orden:
        ids = list(zonas[z][1])
        en, sa = set(entradas(z)), set(salidas(z))
        fuerza = (en if len(en) == 1 else set()) | (sa if len(sa) == 1 else set())
        ax = [n for n in ids if not (nod[n]['clases'] & LAT) or n in fuerza]
        dentro = [(f['de'], f['a']) for f in fl if f['de'] in ax and f['a'] in ax and not vuelta(f) and f['de'] != f['a']]
        ax = _topo(ax, dentro)
        # un flujo lineal va recto: la cadena del bloque (cada paso, una sola entrada y una sola salida dentro de él)
        # sigue en el camino aunque sus pasos sean de al lado; el codo, solo si no cabe
        de_z = [(f['de'], f['a']) for f in fl if f['de'] in ids and f['a'] in ids and not vuelta(f) and f['de'] != f['a']
                and f['de'] not in acc and f['a'] not in acc]
        sal = lambda n: [b for a, b in de_z if a == n]
        ent = lambda n: [a for a, b in de_z if b == n]
        if ax:
            while len(ent(ax[0])) == 1 and len(sal(ent(ax[0])[0])) == 1 and ent(ax[0])[0] not in ax:
                ax.insert(0, ent(ax[0])[0])
            while len(sal(ax[-1])) == 1 and len(ent(sal(ax[-1])[0])) == 1 and sal(ax[-1])[0] not in ax:
                ax.append(sal(ax[-1])[0])
        eje_de[z] = ax
        lat_de[z] = [n for n in ids if n not in ax]
    for n in sorted(acc, key=m['orden'].index):           # cada acción, con el bloque de lo que cambia
        dest = next((f['a'] for f in fl if f['de'] == n), None) or next((f['de'] for f in fl if f['a'] == n), None)
        z = zd.get(corch[dest][1][0]) if dest in corch else zd.get(dest)
        if z is None:
            raise Error(f'la acción «{n}» no se une a ningún bloque')
        lat_de[z].append(n)
    vecinos = lambda n: [f['a'] if f['de'] == n else f['de'] for f in fl if n in (f['de'], f['a']) and f['de'] != f['a']]

    def ancla(n, z):
        for v in vecinos(n):
            if v in eje_de[z] or (v in corch and corch[v][1][0] in eje_de[z]):
                return v
        return None
    # el lado de cada nodo de al lado: en la primera columna, lo de fuera a la izquierda y las acciones a la derecha
    # (por dentro); en las demás, todo a la derecha (por fuera en la última)
    lado = {}
    for c, z in enumerate(cols):
        for n in lat_de[z]:
            lado[n] = ('der' if n in acc else 'izq') if c == 0 and len(cols) > 1 else 'der'
    # anchos
    cab_txt = 16 + (12 if L.croqueta else 0)

    def ancho(ns, lo, hi):
        return max([lo] + [min(hi, L.medida_nodo(n)) for n in ns])
    w_eje = {z: ancho(eje_de[z], 110, 180) for z in orden}
    w_lat = {(z, s): ancho([n for n in lat_de[z] if lado.get(n) == s], 100, 160) for z in cols for s in ('izq', 'der')}
    etq = lambda a, b: max([L.ancho_etq(f) + 24 for f in fl if {f['de'], f['a']} == {a, b} and f['etiqueta']] + [0])
    G = 40
    bus_izq = any(lado.get(n) == 'izq' for n in lat_de[cols[0]]) if cols else False
    x = 16 + (20 if bus_izq else 0)
    xs = {}
    for c, z in enumerate(cols):
        for s in ('izq', 'eje', 'der'):
            if s == 'eje':
                xs[(z, 'eje')] = x
                x += w_eje[z]
            else:
                ns = [n for n in lat_de[z] if lado.get(n) == s]
                if not ns:
                    continue
                g = max([G] + [etq(n, ancla(n, z) or '') for n in ns])
                if s == 'izq':
                    xs[(z, 'izq')] = x
                    x += w_lat[(z, s)] + g
                else:
                    x += g
                    xs[(z, 'der')] = x
                    x += w_lat[(z, s)]
        if c + 1 < len(cols):
            puente = max([etq(a, b) for a in zonas[z][1] for b in zonas[cols[c + 1]][1]] + [56]) + (24 if marcos else 0)
            x += puente
    if x + 16 > L.W:
        raise Error(f'los bloques no caben lado a lado ({x + 16:.0f} > {L.W})')
    dx = (L.W - 16 - x) / 2
    xs = {k: v + dx for k, v in xs.items()}
    # altos: una fila de cajas del mismo alto (el ritmo); entre dos del camino, 28 o 60 con etiqueta
    def alto(n, w):
        nd = nod[n]
        lineas = len(L.partir(nd['nombre'], w - cab_txt, L.fn, K_NEGRITA))
        subs = len(L.partir(nd['sub'], w - L.pad + 8, L.fs, K_MONO)) if nd['sub'] else 1
        return L.alto + L.pnn * (lineas - 1) + (0 if L.plegadas else L.ps * (subs - 1))
    w_de = {}
    for z in cols:
        for n in eje_de[z]:
            w_de[n] = w_eje[z]
        for n in lat_de[z]:
            w_de[n] = w_lat[(z, lado[n])]
    w_fila = w_eje[fila_z] if arriba else 0
    if arriba:
        for n in eje_de[fila_z] + lat_de[fila_z]:
            w_de[n] = w_fila
    H = max(alto(n, w_de[n]) for n in w_de)
    subz = m.get('subzonas', []) if marcos else []
    cabecera = {}
    for nombre, ids in subz:
        primero = min((n for n in ids if n in w_de), key=lambda n: (m['orden'].index(n)), default=None)
        if primero:
            cabecera[primero] = nombre
    hcab = L.fsz + 14
    paso = lambda a, b: H + (60 if etq(a, b) else 28) + (hcab if b in cabecera else 0)
    y = {}
    y0 = 24
    if arriba:
        hay_encima = bool(lat_de[fila_z])
        y_fila = y0 + (30 if marcos else 0) + ((H + 44) if hay_encima else 0)
        y_cols = y_fila + H + (12 + 40 + 30 if marcos else 72)
    else:
        y_cols = y0 + (30 if marcos else 0)
    extra_cab = hcab if any(n in cabecera for z in cols for n in eje_de[z][:1] + lat_de[z]) else 0
    y_cols += extra_cab
    # columnas: la primera baja desde arriba; la siguiente sube, con su entrada a la altura de la salida de la otra
    fondo = y_cols
    for c, z in enumerate(cols):
        ax = eje_de[z]
        if c % 2 == 0:
            yy = y_cols
            for i, n in enumerate(ax):
                if i:
                    yy += paso(ax[i - 1], n)
                y[n] = yy
            fondo = max(fondo, yy)
    for c, z in enumerate(cols):
        ax = eje_de[z]
        if c % 2 == 1:
            yy = fondo
            for i, n in enumerate(ax):
                if i:
                    yy -= paso(ax[i - 1], n)
                y[n] = yy
            if yy < y_cols:                     # más alta que la de al lado: todo baja lo que falta
                d = y_cols - yy
                for n in y:
                    y[n] += d
    # lo de al lado, a la altura de su ancla (o del centro de su corchete); sin ancla, debajo del anterior
    for z in cols:
        ultimo = {}
        for n in lat_de[z]:
            a = ancla(n, z)
            if a in corch:
                ids = corch[a][1]
                yy = (y[ids[0]] + y[ids[-1]] + H) / 2 - H / 2
            elif a is not None and a in y:
                yy = y[a]
            else:
                yy = ultimo.get(lado[n], y_cols - H - 28) + H + 28
            while any(abs(yy - y[o]) < H + 8 for o in lat_de[z] if o in y and lado.get(o) == lado[n]):
                yy += H + 16
            y[n] = yy
            ultimo[lado[n]] = yy
    # la fila de arriba: de derecha a izquierda, con su entrada sobre la última columna y su salida sobre la primera
    if arriba:
        ax = eje_de[fila_z]
        cx_ult = xs[(cols[nc - 1], 'eje')] + w_eje[cols[nc - 1]] / 2
        cx_pri = xs[(cols[0], 'eje')] + w_eje[cols[0]] / 2
        en, sa = entradas(fila_z), salidas(fila_z)
        ie = ax.index(en[0]) if en and en[0] in ax else 0
        isal = ax.index(sa[0]) if sa and sa[0] in ax else len(ax) - 1
        if isal < ie:
            ie, isal = 0, len(ax) - 1
        # en una fila, de derecha a izquierda: la salida sobre la primera columna; la entrada, sobre la última si hay
        # sitio para los pasos de antes; si no, todos al mismo paso. Lo que se salga, corrido hacia dentro.
        s_min = w_fila + G
        cabe_ent = isal > ie and (cx_ult - cx_pri) >= (isal - ie) * s_min and cx_ult + ie * s_min + w_fila / 2 <= L.W - 8
        def borde_col(c):
            z = cols[c]
            ks = [k_ for k_ in xs if k_[0] == z]
            return min(xs[k_] for k_ in ks), max(xs[k_] + (w_eje[z] if k_[1] == 'eje' else w_lat[(z, k_[1])]) for k_ in ks)
        c0, c1 = borde_col(0)[0], borde_col(nc - 1)[1]
        cx = {}
        if len(ax) == 1 and not lat_de[fila_z]:      # un solo paso (un bloque cerrado): centrado sobre las columnas
            cx[ax[0]] = (c0 + c1) / 2
        for i, n in enumerate(ax if not cx else []):
            if cabe_ent and ie <= i <= isal:
                cx[n] = cx_ult + (cx_pri - cx_ult) * (i - ie) / (isal - ie)
            elif cabe_ent and i < ie:
                cx[n] = cx_ult + (ie - i) * s_min
            else:
                cx[n] = cx_pri + (isal - i) * s_min
        der = max(cx.values()) + w_fila / 2 - (L.W - 8)
        izq = 8 - (min(cx.values()) - w_fila / 2)
        if der > 0 or izq > 0:
            if der > 0 and izq > 0 or (der > 0 and der + 8 > min(cx.values()) - w_fila / 2):
                raise Error('la fila de arriba no cabe a lo ancho')
            d_ = -der if der > 0 else izq
            cx = {n: v + d_ for n, v in cx.items()}
        for n in ax:
            y[n] = y_fila
            xs[('n', n)] = cx[n] - w_fila / 2
        for n in lat_de[fila_z]:
            a = ancla(n, fila_z)
            xs[('n', n)] = (cx[a] if a in cx else cx[ax[0]]) - w_fila / 2
            y[n] = y_fila - H - 44
        # simetría de pesos: si la fila es más ancha que las columnas, las columnas se reparten bajo ella (la primera,
        # bajo la salida; las demás, más separadas, hasta su borde); si es más estrecha, va centrada sobre ellas
        f0 = min(v for k_, v in xs.items() if k_[0] == 'n')
        f1 = max(v for k_, v in xs.items() if k_[0] == 'n') + w_fila
        if nc >= 2 and f1 - c1 > 24:
            d_ = f1 - c1
            for c in range(1, len(cols)):
                for k_ in [k_ for k_ in xs if k_[0] == cols[c]]:
                    xs[k_] += d_ * min(c, nc - 1) / (nc - 1)
        elif (c1 - c0) - (f1 - f0) > 24 and len(ax) > 1:
            d_ = (c0 + c1) / 2 - (f0 + f1) / 2
            for k_ in [k_ for k_ in xs if k_[0] == 'n']:
                xs[k_] += d_
    # cajas
    for n in m['orden']:
        if n not in y:
            continue
        if ('n', n) in xs:
            x_ = xs[('n', n)]
        else:
            z = zd.get(n)
            if z is None:
                z = next(zz for zz in cols if n in lat_de[zz])
            x_ = xs[(z, 'eje')] if n in eje_de.get(z, []) else xs[(z, lado[n])]
        tb = L.tab_bloque(nod[n]['nombre'])[1] if 'bloque' in nod[n]['clases'] else 0
        L.nodo(n, R(x_, y[n] - tb, w_de[n], H + tb))
    cs = {n: (R(c.x, c.y + L.pestanas[n][2], c.w, c.h - L.pestanas[n][2]) if n in L.pestanas else c) for n, c in L.cajas.items()}
    # las zonas a las que llega una flecha (decisión 420): la de dentro, con su carpeta en el sitio de su cabecera; la
    # flecha, a su borde (o al de la zona de primer nivel), del lado de su acción
    caja_corch, carpeta_de, entra_x = {}, {}, {}
    for cid, (nombre, ids) in corch.items():
        if not all(n in cs for n in ids):
            continue
        acciones = [n for n in acc if cid in vecinos(n)]
        dcha = not acciones or cs[acciones[0]].cx > cs[ids[0]].cx
        x1, x2 = min(cs[n].x for n in ids), max(cs[n].r for n in ids)
        y1, y2 = cs[ids[0]].y, cs[ids[-1]].b
        if cid in m.get('zona_dentro', ()):
            hc = hcab if ids[0] in cabecera else 18
            carpeta_de[ids[0]] = (R(x1 - 6, y1 - hc, x2 - x1 + 12, y2 + 6 - y1 + hc), nombre, max(hc - 6, 16), None)
            x0 = x2 + 6 if dcha else x1 - 6
        else:
            x0 = x2 + 12 if dcha else x1 - 12          # el borde de su zona de primer nivel (12 a cada lado)
        caja_corch[cid] = R(x0 - 1, y1, 2, y2 - y1)
    # marcos de las zonas (sin las acciones) y cabeceras de las de dentro
    bordes = []
    con_marco = set(range(len(zonas))) if marcos is True else set(marcos or ())
    if con_marco:
        for z, (nombre, ids) in enumerate(zonas):
            if z not in con_marco:
                continue
            ns = [n for n in ids if n in cs]
            if not ns:
                continue
            arriba_z = min(cs[n].y - (hcab if n in cabecera else 0) for n in ns) - 30
            r = R(min(cs[n].x for n in ns) - 12, arriba_z, max(cs[n].r for n in ns) - min(cs[n].x for n in ns) + 24,
                  max(cs[n].b for n in ns) + 12 - arriba_z)
            L.zona(r, nombre)
            bordes.append(r)
        hechas_c = {v[1] for v in carpeta_de.values()}
        for nombre, ids in subz:
            n = next((k for k, v in cabecera.items() if v == nombre), None)
            if n is None or nombre in hechas_c or n in carpeta_de:
                continue
            r = carpeta_sub(cs, ids, hcab)
            if r:
                carpeta_de[n] = (r, nombre, max(hcab - 6, 16), cs[n])
        for n, nombre in cabecera.items():
            if n not in carpeta_de:
                L.cabecera(cs[n], nombre)
        for n, (r, nombre, T_, alt) in carpeta_de.items():
            L.carpeta_dentro(r, nombre, T_, alt=alt)
            entra_x[n] = L.tab_fin
    # flechas
    usados, hechas = [], set()
    pares = {(f['de'], f['a']) for f in fl}

    def pon(f, pts):
        L.flecha(f, pts)
        usados.extend(zip(pts, pts[1:]))
        hechas.add(id(f))
    caja = lambda n: caja_corch.get(n) or cs[n]
    for f in fl:
        a, b = f['de'], f['a']
        if a not in cs and a not in caja_corch or b not in cs and b not in caja_corch:
            continue
        ca, cb = caja(a), caja(b)
        doble = (b, a) in pares
        if abs(ca.cy - cb.cy) < 1 and (cb.x > ca.r or cb.r < ca.x):              # a la misma altura: recta
            yy = ca.cy + ((-8 if a < b else 8) if doble else 0)
            pon(f, [(ca.r, yy), (cb.x - 2, yy)] if cb.x > ca.r else [(ca.x, yy), (cb.r + 2, yy)])
        elif abs(ca.cx - cb.cx) < 1 and (cb.y > ca.b or cb.b < ca.y):            # en la misma columna: recta
            sobre = [c for n, c in cs.items() if n not in (a, b) and c.x < ca.cx < c.r and min(ca.b, cb.b) < c.cy < max(ca.y, cb.y)]
            if sobre:
                continue
            xx = ca.cx + ((-12 if a < b else 12) if doble else 0)
            if b in entra_x and cb.y > ca.b:     # a la carpeta de dentro: junto a su pestaña, sin cruzarla
                xx = min(max(xx, entra_x[b]), cb.r - 10)
            pon(f, [(xx, ca.b), (xx, cb.y - 2)] if cb.y > ca.b else [(xx, ca.y), (xx, cb.b + 2)])
        elif a in caja_corch or b in caja_corch:
            yy = (cs[a] if a in cs else cs[b]).cy
            pon(f, [(ca.r, yy), (cb.x - 2, yy)] if cb.x > ca.r else [(ca.x, yy), (cb.r + 2, yy)])
    # reparto en bus: un origen con tres o más destinos de al lado, por fuera de ellos
    por_origen = {}
    for f in fl:
        if id(f) not in hechas and f['a'] in lado and f['de'] in cs:
            por_origen.setdefault((f['de'], lado[f['a']]), []).append(f)
    for (o, s), fs in por_origen.items():
        if len(fs) < 3:
            continue
        co = cs[o]
        dest = [cs[f['a']] for f in fs]
        if s == 'izq':
            xt = min([c.x for c in dest] + [r.x for r in bordes if any(r.x <= c.x and c.r <= r.r and r.y <= c.y for c in dest)]) - 8
            for f in fs:
                cb = cs[f['a']]
                pon(f, [(co.x, co.cy), (xt, co.cy), (xt, cb.cy), (cb.x - 2, cb.cy)])
        else:
            xt = max([c.r for c in dest] + [r.r for r in bordes if any(r.x <= c.x and c.r <= r.r and r.y <= c.y for c in dest)]) + 8
            for f in fs:
                cb = cs[f['a']]
                pon(f, [(co.r, co.cy), (xt, co.cy), (xt, cb.cy), (cb.r + 2, cb.cy)])
    # entre la fila de arriba y una columna: por el pasillo de entre las dos, en ángulo recto (si nada se cruza)
    if arriba:
        en_fila = set(eje_de[fila_z]) | set(lat_de[fila_z])
        fila_b = max(cs[n].b for n in en_fila if n in cs)
        ymid = fila_b + (32 if marcos else 36)
        for f in fl:
            a, b = f['de'], f['a']
            if id(f) in hechas or a not in cs or b not in cs or (a in en_fila) == (b in en_fila):
                continue
            ca, cb = cs[a], cs[b]
            col, fil = (cb, ca) if a in en_fila else (ca, cb)
            # si una caja queda encima de la otra, recta: en el centro de la de la columna o lo más cerca, sin repetir
            # una x ya usada en la caja de la fila
            ocupadas = [p_[0] for p_, q_ in usados if p_[0] == q_[0] and (abs(p_[1] - fil.b) < 3 or abs(q_[1] - fil.b) < 3)]
            # una decisión, por su borde recto (sus esquinas van en diagonal)
            mg = 24 if 'dec' in m['nodos'].get(a, {}).get('clases', ()) | m['nodos'].get(b, {}).get('clases', ()) else 14
            lo, hi = max(ca.x, cb.x) + mg, min(ca.r, cb.r) - mg
            xr = None
            if lo <= hi:
                cands = sorted({min(max(col.cx, lo), hi)} | set(range(int(lo), int(hi) + 1, 4)), key=lambda x_: abs(x_ - col.cx))
                ncol = b if a in en_fila else a          # por arriba de la caja de la columna: no por su pestaña
                p0, p1 = L.pestanas.get(ncol, (0, -1, 0))[:2]
                p0, p1 = p0 - 6, p1 + 6
                xr = next((x_ for x_ in cands if all(abs(x_ - o_) >= 16 for o_ in ocupadas) and not p0 <= x_ <= p1), None)
            if xr is not None:
                pts = [(xr, ca.b), (xr, cb.y - 2)] if a in en_fila else [(xr, ca.y), (xr, cb.b + 2)]
            else:
                xf = fil.cx
                if any(abs(xf - o_) < 16 for o_ in ocupadas):
                    xf += 24 if col.cx > fil.cx else -24
                if a in en_fila:
                    pts = [(xf, ca.b), (xf, ymid), (cb.cx, ymid), (cb.cx, cb.y - 2)]
                else:
                    pts = [(ca.cx, ca.y), (ca.cx, ymid), (xf, ymid), (xf, cb.b + 2)]
            corta_ = lambda pts: any(seg_rect(p_, q_, 1).corta(R(c.x + 1, c.y + 1, c.w - 2, c.h - 2))
                                     for p_, q_ in zip(pts, pts[1:]) for k_, c in cs.items() if k_ not in (a, b))
            if corta_(pts):
                # por fuera de la columna (de su carpeta), por el lado con sitio: rodea sus cajas sin cruzarlas (una
                # vuelta que sube desde el fondo de un bloque, o lo que baja a él, en sentido contrario a la ida)
                marco = next((r_ for r_ in bordes if r_.x <= col.x and col.r <= r_.r and r_.y <= col.y <= r_.b), col)
                ocup_x = [p_[0] for p_, q_ in usados if p_[0] == q_[0]]
                for xl in (marco.x - 16, marco.r + 16, marco.x - 28, marco.r + 28):
                    if not 8 <= xl <= L.W - 8 or any(abs(xl - o_) < 10 for o_ in ocup_x):
                        continue
                    xf_ = min(max(col.cx, fil.x + mg), fil.r - mg)
                    xf_ = min((x_ for x_ in range(int(fil.x + mg), int(fil.r - mg) + 1, 4) if all(abs(x_ - o_) >= 16 for o_ in ocupadas)),
                              key=lambda x_: abs(x_ - xl), default=xf_)
                    ent = col.x if xl < col.x else col.r
                    if a in en_fila:
                        alt = [(xf_, ca.b), (xf_, ymid), (xl, ymid), (xl, cb.cy), (ent + (-2 if xl < col.x else 2), cb.cy)]
                    else:
                        alt = [(ent, ca.cy), (xl, ca.cy), (xl, ymid), (xf_, ymid), (xf_, cb.b + 2)]
                    if not corta_(alt):
                        pts = alt
                        break
            if not corta_(pts):
                pon(f, pts)
    # entre dos columnas vecinas (la ida y la vuelta de un par de bloques, cada una por su sitio): por el pasillo de
    # entre las dos, con dos codos, sin cruzar cajas ni otra flecha
    pos_col = {z: i for i, z in enumerate(cols)}
    def marco_z(z):
        ns = [n for n in zonas[z][1] if n in cs]
        return (min(cs[n].x for n in ns) - 12, max(cs[n].r for n in ns) + 12) if ns else None

    def cruza(pts):
        for p_, q_ in zip(pts, pts[1:]):
            for u_, v_ in usados:
                h1, h2 = p_[1] == q_[1], u_[1] == v_[1]
                if h1 == h2:
                    if ((h1 and abs(p_[1] - u_[1]) < 8 and min(max(p_[0], q_[0]), max(u_[0], v_[0])) > max(min(p_[0], q_[0]), min(u_[0], v_[0])))
                            or (not h1 and abs(p_[0] - u_[0]) < 8 and min(max(p_[1], q_[1]), max(u_[1], v_[1])) > max(min(p_[1], q_[1]), min(u_[1], v_[1])))):
                        return True
                    continue
                (hx0, hx1, hy), (vx, vy0, vy1) = ((min(p_[0], q_[0]), max(p_[0], q_[0]), p_[1]), (u_[0], min(u_[1], v_[1]), max(u_[1], v_[1]))) if h1                     else ((min(u_[0], v_[0]), max(u_[0], v_[0]), u_[1]), (p_[0], min(p_[1], q_[1]), max(p_[1], q_[1])))
                if hx0 + 1 < vx < hx1 - 1 and vy0 + 1 < hy < vy1 - 1:
                    return True
        return any(seg_rect(p_, q_, 1).corta(R(c.x + 1, c.y + 1, c.w - 2, c.h - 2))
                   for p_, q_ in zip(pts, pts[1:]) for c in cs.values() if not (c.x <= p_[0] <= c.r and c.y <= p_[1] <= c.b)
                   and not (c.x - 3 <= q_[0] <= c.r + 3 and c.y - 3 <= q_[1] <= c.b + 3))
    for f in fl:
        a, b = f['de'], f['a']
        if id(f) in hechas or a not in cs or b not in cs:
            continue
        za, zb = zd.get(a), zd.get(b)
        if za not in pos_col or zb not in pos_col or abs(pos_col[za] - pos_col[zb]) != 1:
            continue
        ca, cb = cs[a], cs[b]
        der_ = pos_col[za] < pos_col[zb]                      # el destino, a la derecha
        mi, md = (marco_z(za), marco_z(zb)) if der_ else (marco_z(zb), marco_z(za))
        x0_, x1_ = mi[1] + 4, md[0] - 4
        if x1_ - x0_ < 16:
            continue
        xm0 = (x0_ + x1_) / 2
        hecho = False
        for dx in (0, -10, 10, -20, 20):
            for dya in (0, -12, 12):
                for dyb in (0, 12, -12):
                    xm = xm0 + dx
                    ya, yb = ca.cy + dya, cb.cy + dyb
                    if not (x0_ < xm < x1_):
                        continue
                    pts = [(ca.r if der_ else ca.x, ya), (xm, ya), (xm, yb), ((cb.x - 2) if der_ else (cb.r + 2), yb)]
                    if abs(ya - yb) < 1:
                        pts = [pts[0], pts[3]]
                    if not cruza(pts):
                        pon(f, pts)
                        hecho = True
                        break
                if hecho:
                    break
            if hecho:
                break
    resto = [f for f in fl if id(f) not in hechas and f['de'] in cs and f['a'] in cs]
    if resto:
        etq_ = lambda f: (L.ancho_etq(f), L.fe + 8)
        for f, pts in zip(resto, enrutar_v(resto, cs, L.W, etq_, usados, bordes, vuelta)[0]):
            L.flecha(f, pts)
    L.H = max([c.b for c in cs.values()] + [r.b for r in bordes]) + 24
    L.acabar()
    return L


def estado_bloques(m, blq, abierto=None):
    """El modelo de un estado de los bloques: todos cerrados (abierto=None) o uno abierto en su sitio. Cada bloque
    cerrado, una caja con su nombre y cuántos pasos tiene (id «_b<k>»), en su propia zona sin marco; entre dos cajas,
    una flecha por sentido, la principal (la del flujo o la que tiene etiqueta). Las acciones de un bloque cerrado no
    salen. Devuelve (modelo, zonas con marco)."""
    nod, zonas = m['nodos'], m['zonas']
    acc = {n for n, d in nod.items() if 'accion' in d['clases']}
    zd = {n: z for z, (_, ids) in enumerate(zonas) for n in ids}
    corch = m.get('corchetes', {})
    for cid, (_, ids) in corch.items():
        zd[cid] = zd.get(ids[0])

    def dueno(n):   # la acción va con el bloque de lo que cambia
        if n not in acc:
            return zd.get(n)
        dest = next((f['a'] for f in m['flechas'] if f['de'] == n), None) or next((f['de'] for f in m['flechas'] if f['a'] == n), None)
        return zd.get(dest)
    cerrada = lambda z: z != abierto
    nodos, orden, zs = {}, [], []
    for z, (nombre, ids) in enumerate(zonas):
        if cerrada(z):
            pasos = [i for i in ids if i not in acc]
            nid = f'_b{z}'
            nodos[nid] = {'id': nid, 'nombre': nombre.split(' · ')[0].upper(), 'sub': f'{len(pasos)} paso{"" if len(pasos) == 1 else "s"} ▸',
                          'clases': {'bloque'}, 'chip': '', 'bloque': z, 'linea': linea_de_zona(m, ids)}
            orden.append(nid)
            zs.append((nombre, [nid]))
        else:
            zs.append((nombre, list(ids)))
    for n in m['orden']:
        z = dueno(n)
        if z is not None and not cerrada(z):
            nodos[n] = nod[n]
            orden.insert(len(orden), n)
    orden.sort(key=lambda n: (nodos[n].get('bloque', dueno(n) or 0), m['orden'].index(n) if n in m['orden'] else -1))
    ext = lambda n: f'_b{dueno(n)}' if dueno(n) is not None and cerrada(dueno(n)) else n
    flechas, vistas = [], {}
    for f in m['flechas']:
        if f['de'] == 'inicio':
            continue
        if (f['de'] in acc and cerrada(dueno(f['de']))) or (f['a'] in acc and cerrada(dueno(f['a']))):
            continue
        a, b = ext(f['de']), ext(f['a'])
        if a == b and a.startswith('_b'):
            continue
        if a.startswith('_b') or b.startswith('_b'):
            k = (a, b)
            peso = ('flujo' in f['clases']) * 2 + bool(f['etiqueta'])
            if k in vistas:
                if peso <= vistas[k][0]:
                    continue
                flechas[vistas[k][1]] = dict(f, de=a, a=b)
                vistas[k] = (peso, vistas[k][1])
                continue
            vistas[k] = (peso, len(flechas))
        flechas.append(dict(f, de=a, a=b))
    # las de dentro del bloque abierto, antes: así cada paso de al lado se ancla a uno de su bloque, no a una caja cerrada
    flechas.sort(key=lambda f: f['de'].startswith('_b') or f['a'].startswith('_b'))
    abiertos_c = {cid: v for cid, v in corch.items() if not cerrada(zd.get(cid))}
    subz = [(nombre, ids) for nombre, ids in m.get('subzonas', []) if all(i in nodos for i in ids)]
    fichas = {n: v for n, v in m['fichas'].items() if n in nodos}
    for z, (nombre, ids) in enumerate(zonas):
        if cerrada(z):
            pasos = [nod[i]['nombre'] for i in ids if i not in acc]
            fichas[f'_b{z}'] = (', '.join(pasos[:-1]) + (' y ' if len(pasos) > 1 else '') + pasos[-1] + '. Pulsa para abrir el bloque.', [])
    marcos = set() if abierto is None else {abierto}
    mm = dict(m, nodos=nodos, orden=orden, zonas=zs, flechas=flechas, subzonas=subz, corchetes=abiertos_c, fichas=fichas,
              notas=[], recorrido=[], forma_bloques=('anillo' if blq['forma'] == 'anillo' else 'columnas', blq['orden']))
    return mm, marcos


def ramas_laterales(m):
    """Las ramas laterales del camino: nodos con una sola conexión, con un paso que no es el de antes (una salida que
    cuelga de un paso del medio). En una sola columna irían al fondo, tras el final, y parecerían el final del flujo."""
    prin = principales(m)
    fl = [f for f in m['flechas'] if f['de'] != 'inicio' and f['de'] != f['a']]
    out = []
    for i, n in enumerate(prin):
        vs = {f['a'] if f['de'] == n else f['de'] for f in fl if n in (f['de'], f['a'])}
        if i > 0 and len(vs) == 1 and next(iter(vs)) in prin and next(iter(vs)) != prin[i - 1]:
            out.append(n)
    return out


def ramas_finales(m):
    """Lo que sale del camino y acaba fuera de él: un paso sin salida al que se llega desde uno que no es el de antes
    (la rama de una decisión que no vuelve), con lo que solo se une a él (otra entrada que solo lleva a ella).
    En una columna, el lector lo toma por la continuación del camino: va al lado (decisión 326)."""
    prin = principales(m)
    fl = [f for f in m['flechas'] if f['de'] != 'inicio' and f['de'] != f['a']]
    fuera = []
    for i, n in enumerate(prin):
        if i == 0 or m['nodos'][n]['clases'] & {'fin', 'final'} or any(f['de'] == n for f in fl):
            continue
        # al final del camino también se llega desde una decisión (lo que se salta): si viene del de antes, es el camino
        if any(f['a'] == n and f['de'] in prin and f['de'] != prin[i - 1] for f in fl) and \
                not any(f['a'] == n and f['de'] == prin[i - 1] for f in fl):
            fuera.append(n)
    for n in prin:      # lo que solo se une a una rama, con ella
        vs = {f['a'] if f['de'] == n else f['de'] for f in fl if n in (f['de'], f['a'])}
        if n not in fuera and vs and vs <= set(fuera) and not any(f['a'] == n for f in m['flechas'] if f['de'] == 'inicio'):
            fuera.append(n)
    return fuera


def con_clase(m, ids, clase):
    """Una copia del modelo con la clase añadida a esos nodos (para probar otra disposición)."""
    m2 = dict(m)
    m2['nodos'] = {k: dict(v, clases=v['clases'] | ({clase} if k in ids else set())) for k, v in m['nodos'].items()}
    return m2


def puntuar(L, m):
    """Lo que pesa al elegir entre dos disposiciones: una caja lejos de la única con que se une (otra en medio) pesa más
    que todo; luego cruces, tramos por una caja ajena, etiquetas lejos, codos y largo."""
    r = medidas(L, m)
    return (1000 * len(r['aisladas']) + 200 * (r['cruces'] + len(r['por_caja'])) + 100 * len(r['lejos']) + 50 * len(r['requiebros'])
            + 20 * r['codos'] + r['largo'] / 20)


def dibujar(m, o, cajas='desplegadas', forma='redondeada', hueco=True):
    t = m['tipo']
    blq = bloques(m) if t in ('estados', 'proceso') else None
    if blq:
        # los bloques en anillo o en columnas, contra la forma apilada: la que mejor se lee; fijada en los datos, esa
        try:
            Lb = en_bloques(m, Lienzo(m, o, cajas, forma), blq)
        except Error:
            Lb = None
        if Lb is not None and m.get('forma_bloques'):
            Lb.bloques = blq['forma']
            return Lb
        ma = m
        if m.get('marcos_bloques') is not None:     # un estado de los bloques, apilado: solo el bloque abierto, con marco
            ma = dict(m, zonas=[m['zonas'][z] for z in sorted(m['marcos_bloques'])])
        try:
            La = _dibujar_ramas(ma, o, cajas, forma, hueco)
        except Error:
            if Lb is None:
                raise
            Lb.bloques = blq['forma']
            return Lb
        if Lb is not None and puntuar(Lb, m) + Lb.H * Lb.W / 2000 <= puntuar(La, ma) + La.H * La.W / 2000:
            Lb.bloques = blq['forma']
            return Lb
        # apilado: si cabía la forma deducida y se lee peor, el comprobador lo avisa (data-bloques)
        La.bloques = ('apilado-' + blq['forma']) if Lb is not None else ''
        La.hermanos = blq['hermanos']
        return La
    return _dibujar_ramas(m, o, cajas, forma, hueco)


def otro_lado(m):
    """Los nodos «lado» (sin «izquierda»), a la izquierda; None si no hay ninguno."""
    nodos = {k: (dict(v, clases=(v['clases'] - {'lado'}) | {'izquierda'}) if 'lado' in v['clases'] and 'izquierda' not in v['clases'] else v)
             for k, v in m['nodos'].items()}
    return dict(m, nodos=nodos) if any(nodos[k] is not m['nodos'][k] for k in nodos) else None


def _dibujar_ramas(m, o, cajas='desplegadas', forma='redondeada', hueco=True):
    t = m['tipo']
    finales = ramas_finales(m) if t in ('estados', 'proceso') and o == 'v' else []
    if finales and m.get('una_columna'):
        # quitar la marca es más fácil que acortar los rótulos: con --exigir (el dibujante), un error
        texto = (f'«{", ".join(m["nodos"][n]["nombre"] for n in finales)}» sale del camino y acaba fuera de él: al lado, no '
                 'en el eje (sin «una-columna»); si no cabe, acorta los rótulos')
        if m.get('exigir'):
            raise Error(texto)
        if not m.get('_avisado_una_columna'):
            print(f'Aviso: {texto}', file=sys.stderr)
            m['_avisado_una_columna'] = True
    ramas = list(dict.fromkeys(ramas_laterales(m) + finales)) if t in ('estados', 'proceso') and not m.get('una_columna') else []
    cands = [m] + ([con_clase(m, ramas, 'lado' if o == 'v' else 'salida')] if ramas else [])
    vuelven = [n for n in m.get('desplazados', []) if n in principales(m)] if t in ('estados', 'proceso') and o == 'v' else []
    if vuelven:
        cands.append(con_clase(m, vuelven, 'lado'))
    if o == 'v' and t in ('estados', 'proceso'):
        # lo que va al lado, también a la izquierda: si por la derecha cruza algo, el generador prueba el otro lado
        cands += [x for x in map(otro_lado, cands) if x]
    if len(cands) > 1:
        # ¿Una columna, o una más para las ramas laterales? Se dibujan las dos y se queda la que mejor se lee (decisión
        # 326: cada rama, al lado del paso del que cuelga; en la horizontal, en la segunda fila).
        mejor, no_cabe = None, None
        for mm in cands:
            try:
                L = _dibujar(mm, o, cajas, forma, hueco)
            except Error as e:
                if mm is not m and 'no caben' in str(e):
                    no_cabe = e
                continue
            k = puntuar(L, mm)
            if mejor is None or k < mejor[0]:
                mejor = (k, L, mm)
        al_lado = lambda mm: all(mm['nodos'][n]['clases'] & (LATERALES | {'salida'}) for n in finales)
        if mejor and no_cabe and finales and not al_lado(mejor[2]):
            raise Error(f'{no_cabe}; «{", ".join(m["nodos"][n]["nombre"] for n in finales)}» sale del camino: '
                        'acorta los rótulos para que quepa al lado')
        if mejor and no_cabe and o == 'v' and medidas(mejor[1], mejor[2])['aisladas']:
            # en una columna, lo que cuelga de un solo paso queda lejos de él: al lado, con los rótulos más cortos
            raise Error(f'{no_cabe}; en una columna, {medidas(mejor[1], mejor[2])["aisladas"][0]}: acorta los rótulos para que quepa al lado')
        if mejor:
            return mejor[1]
    return _dibujar(m, o, cajas, forma, hueco)


def _dibujar(m, o, cajas='desplegadas', forma='redondeada', hueco=True):
    t = m['tipo']
    lados = any(n['clases'] & (LATERALES | {'accion'}) for n in m['nodos'].values())
    if m.get('corchetes') and t not in ('arquitectura', 'piezas') and not (t in ('estados', 'proceso') and o == 'v' and lados):
        # sin eje (la fila, la columna, la rejilla): la flecha a una zona llega a su paso de en medio
        medio = {cid: ids[len(ids) // 2] for cid, (_, ids) in m['corchetes'].items()}
        m = dict(m, corchetes={}, flechas=[dict(f, a=medio.get(f['a'], f['a'])) for f in m['flechas']])
    zonas_pk = {x for p in m.get('puntos_clave', []) for e in p['donde'] for x in e} & set(m.get('zona_ids_todas', []))
    if o == 'h' and t in ('estados', 'proceso') and zonas_pk:
        raise Error(f'la fila horizontal no dibuja las zonas, y «{", ".join(sorted(zonas_pk))}» es un punto clave')
    L = Lienzo(m, o, cajas, forma)
    L.hueco = hueco
    if t in ('estados', 'proceso'):
        (eje if lados else columna)(m, L) if o == 'v' else fila(m, L)
    elif t in ('arquitectura', 'piezas'):
        (rejilla_v if o == 'v' else rejilla)(m, L)
    elif t == 'secuencia':
        secuencia(m, L)
    else:
        fases(m, L)
    return L


# ───────────────────────── medidas de lectura ─────────────────────────
# Lo que el bucle de afinado mide en cada ronda (SKILL.md, «Bucle de afinado»): el generador mide y Claude mira la
# captura, contesta las preguntas de lectura y decide el cambio en los datos.

PANTALLA = {375: (375 - 32, 844), 1440: (400, 900)}   # ancho del dibujo vertical y alto de la pantalla, en px


def _largo(p):
    return sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in zip(p, p[1:]))


def zona_de(m):
    """La zona de primer nivel de cada nodo (para contar los puentes entre áreas)."""
    return {n: nombre for nombre, ids in m['zonas'] for n in ids}


def requiebros(cajas, zonas, flechas, subzonas=()):
    """Un flujo lineal va recto si cabe: las cadenas de tres pasos o más dentro de una zona (cada uno, una sola entrada
    y una sola salida dentro de ella) que no van en una fila ni en una columna, cuando la zona tiene sitio para ponerlas
    rectas (a lo ancho o a lo alto, con 24 entre cajas). Devuelve los nombres de sus pasos, uno por cadena."""
    def zona(n):
        c = cajas[n]
        dentro = [z for z in zonas if z.x <= c.cx <= z.r and z.y <= c.cy <= z.b]
        return min(dentro, key=lambda z: z.w * z.h) if dentro else None
    sub = {n: k for k, (_, ids) in enumerate(subzonas) for n in ids}
    zn = {n: zona(n) for n in cajas}
    ar = [(a, b) for a, b in flechas if a in cajas and b in cajas and a != b and zn[a] is not None and zn[a] is zn[b]
          and sub.get(a) == sub.get(b)]
    sal = {n: [b for a, b in ar if a == n] for n in cajas}
    ent = {n: [a for a, b in ar if b == n] for n in cajas}
    lineal = lambda n: len(sal[n]) <= 1 and len(ent[n]) <= 1
    out = []
    for n in cajas:
        if not lineal(n) or (ent[n] and lineal(ent[n][0]) and len(sal[ent[n][0]]) == 1):
            continue           # no empieza aquí una cadena
        cad = [n]
        while len(sal[cad[-1]]) == 1 and sal[cad[-1]][0] not in cad and lineal(sal[cad[-1]][0]):
            cad.append(sal[cad[-1]][0])
        if len(cad) < 3:
            continue
        cs = [cajas[x] for x in cad]
        fila = all(abs(c.cy - cs[0].cy) < 2 for c in cs)
        col = all(abs(c.cx - cs[0].cx) < 2 for c in cs)
        if fila or col:
            continue
        z = zn[n]
        cabe = (sum(c.w for c in cs) + 24 * (len(cs) - 1) <= z.w - 16) or (sum(c.h for c in cs) + 24 * (len(cs) - 1) <= z.h - 40)
        if cabe:
            out.append(' → '.join(cad))
    return out


def medidas(L, m):
    """Las medidas de lectura de un dibujo: largo, codos, tramo compartido (dos flechas a menos de 6 en paralelo; las de
    un mismo origen, el reparto en bus, no cuentan), cruces, tramos por una caja ajena, flechas que suben sin ser vuelta,
    etiquetas a más de 16 de su flecha, la flecha más larga en pantallas a 375 y a 1440, puentes entre áreas (más de dos
    entre las mismas, sin contar el bus ni las rectas) y, si hay flujo, sus codos y sus subidas."""
    cam = [(f, p) for f, p in L.caminos if f['de'] != 'inicio']
    vuelta = lambda f: bool(f['clases'] & {'vuelta', 'claude'})
    r = {'flechas': len(cam), 'largo': round(sum(_largo(p) for _, p in cam)), 'codos': sum(len(p) - 2 for _, p in cam)}
    comp = cruces = 0
    for i, (f, p) in enumerate(cam):
        for g, q in cam[i + 1:]:
            mismo = f['de'] == g['de'] or f['a'] == g['a']   # bus o llegada común: comparten a propósito
            for a, b in zip(p, p[1:]):
                for c, d in zip(q, q[1:]):
                    va, vc = a[0] == b[0], c[0] == d[0]
                    if va == vc:
                        k = 0 if va else 1
                        if abs(a[k] - c[k]) < 6 and not mismo:
                            j = 1 - k
                            comp += max(0, min(max(a[j], b[j]), max(c[j], d[j])) - max(min(a[j], b[j]), min(c[j], d[j])))
                    elif not mismo:
                        h, v = ((a, b), (c, d)) if not va else ((c, d), (a, b))
                        x, y = v[0][0], h[0][1]
                        if min(h[0][0], h[1][0]) + 2 < x < max(h[0][0], h[1][0]) - 2 and min(v[0][1], v[1][1]) + 2 < y < max(v[0][1], v[1][1]) - 2:
                            cruces += 1
    r['compartido'], r['cruces'] = round(comp), cruces
    r['por_caja'] = [f'{f["de"]} > {f["a"]}' for f, p in cam
                     if any(seg_rect(a, b).corta(R(c.x + 2, c.y + 2, c.w - 4, c.h - 4)) for a, b in zip(p, p[1:])
                            for n, c in L.cajas.items() if n not in (f['de'], f['a']))]
    r['suben'] = [f'{f["de"]} > {f["a"]}' for f, p in cam if L.o == 'v' and not vuelta(f) and p[-1][1] < p[0][1] - 8]
    def hueco(c, a, b):   # de la etiqueta a un tramo: lo que separa sus dos rectángulos
        s_ = seg_rect(a, b)
        return (max(0, c.x - s_.r, s_.x - c.r) ** 2 + max(0, c.y - s_.b, s_.y - c.b) ** 2) ** .5
    r['lejos'] = [f['etiqueta'] for f, c in L.rotulos
                  if min((hueco(c, a, b) for g, p in cam if g is f for a, b in zip(p, p[1:])), default=0) > 16]
    if L.o == 'v':
        larga = max(((_largo(p), f) for f, p in cam if not vuelta(f)), key=lambda x: x[0], default=(0, None))
        r['pantallas'] = {a: round(larga[0] * w / L.W / h, 2) for a, (w, h) in PANTALLA.items()}
        r['mas_larga'] = f'{larga[1]["de"]} > {larga[1]["a"]}' if larga[1] else ''
    # cajas lejos de la única con que se unen: la línea entre sus centros pasa por otra caja
    vec = {}
    for f, _ in cam:
        if f['de'] != f['a'] and f['de'] in L.cajas and f['a'] in L.cajas:
            vec.setdefault(f['de'], set()).add(f['a'])
            vec.setdefault(f['a'], set()).add(f['de'])
    r['aisladas'] = []
    for n, vs in vec.items():
        if len(vs) == 1:
            v = next(iter(vs))
            a, b = L.cajas[n], L.cajas[v]
            pts = [(a.cx + (b.cx - a.cx) * i / 40, a.cy + (b.cy - a.cy) * i / 40) for i in range(41)]
            medio = [k for k, c in L.cajas.items() if k not in (n, v)
                     and any(c.x + 2 < x < c.r - 2 and c.y + 2 < y < c.b - 2 for x, y in pts)]
            if medio:
                r['aisladas'].append(f'{n} ({v}; en medio, {", ".join(medio)})')
    r['requiebros'] = requiebros(L.cajas, L.zonas_rc, [(f['de'], f['a']) for f, _ in cam if not vuelta(f)], m.get('subzonas', []))
    zd, pares = zona_de(m), {}
    for f, p in cam:
        if len(p) == 2:          # recta: una entrada frente a su destino ya está en la frontera
            continue
        za, zb = zd.get(f['de']), zd.get(f['a'])
        if za and zb and za != zb:
            pares.setdefault(tuple(sorted((za, zb))), set()).add(f['de'])   # un origen con varias, un bus: cuenta uno
    r['puentes'] = {f'{a} – {b}': len(v) for (a, b), v in pares.items() if len(v) > 2}
    flujo = [(f, p) for f, p in cam if 'flujo' in f['clases']]
    if flujo:
        r['flujo'] = {'flechas': len(flujo), 'codos': sum(len(p) - 2 for _, p in flujo),
                      'suben': sum(1 for _, p in flujo if p[-1][1] < p[0][1] - 8) if L.o == 'v' else 0}
    return r


def texto_medidas(r, nombre):
    coma = lambda x: f'{x:g}'.replace('.', ',')
    t = [f'{r["flechas"]} flechas', f'largo {r["largo"]}', f'codos {r["codos"]}', f'compartido {r["compartido"]}',
         f'cruces {r["cruces"]}']
    t.append(f'por caja ajena {len(r["por_caja"])}' + (f' ({", ".join(r["por_caja"])})' if r['por_caja'] else ''))
    if 'pantallas' in r:
        t.append(f'suben {len(r["suben"])}' + (f' ({", ".join(r["suben"])})' if r['suben'] else ''))
        t.append(f'más larga {coma(r["pantallas"][375])} pantallas a 375 y {coma(r["pantallas"][1440])} a 1440'
                 + (f' ({r["mas_larga"]})' if r['mas_larga'] else ''))
    t.append(f'cajas lejos de su única unión {len(r["aisladas"])}' + (f' ({"; ".join(r["aisladas"])})' if r['aisladas'] else ''))
    t.append(f'requiebros con sitio para ir recta {len(r["requiebros"])}' + (f' ({"; ".join(r["requiebros"])})' if r['requiebros'] else ''))
    t.append(f'etiquetas lejos {len(r["lejos"])}' + (f' ({", ".join(r["lejos"])})' if r['lejos'] else ''))
    t.append('puentes de más ' + (', '.join(f'{k} {v}' for k, v in r['puentes'].items()) if r['puentes'] else '0'))
    if 'flujo' in r:
        t.append(f'flujo: {r["flujo"]["flechas"]} flechas, {r["flujo"]["codos"]} codos, {r["flujo"]["suben"]} suben')
    return f'Medidas ({nombre}): ' + ' · '.join(t)


# ───────────────────────── figura y página ─────────────────────────

def linea_ficha(t, m):
    mm = re.match(r'([A-ZÁÉÍÓÚÑÜ0-9 ·\-]{2,})(?:\s*\((\w+)\))?\s*:\s*(.*)$', t)
    if t.startswith('claude:'):
        return f'<li class="d-li-claude">{escape(t[7:].strip())}</li>'
    if t.startswith('codigo:'):     # una orden, una ruta o un nombre del código: en mono
        return f'<li class="d-li-codigo"><code>{escape(t[7:].strip())}</code></li>'
    if mm:
        bt, color, resto = mm.groups()
        c = f' d-b-{color}' if color in COLORES else ''
        return f'<li><b class="d-bt{c}">{escape(bt.strip())}</b> {escape(resto)}</li>'
    return f'<li>{escape(t)}</li>'


def figura(m, tema=''):
    """La <figure>: las dos formas, si caben, con todos los ajustes puestos como clases y atributos, para que la
    herramienta «diagramas» los cambie sin volver a generar. Con tema, data-d-tema (el documento trae sus colores)."""
    def dibujos(m):
        """Todo lo que se dibuja de la figura (variantes, estados de los bloques): sus trozos y lo que hace falta luego."""
        dib = {}
        errores = []
        variantes = [(c, f) for c in VARIANTES['cajas'] for f in VARIANTES['forma']]
        # La vertical, siempre. La croqueta, más ancha, puede no caber: entonces esa variante usa el dibujo redondeado
        # (data-forma-dibujo lo dice) y se avisa; la redondeada tiene que caber.
        dib = {'v': {}, 'h': {}}
        sustituidas = set()
        if m['tipo'] in ('estados', 'proceso') and not m.get('abiertos') and bloques(m):
            m = dict(m, centrar=True)          # con bloques, cada vista centrada y ajustada a lo que dibuja
        for v in variantes:
            try:
                dib['v'][v] = dibujar(m, 'v', *v)
            except Error as e:
                if v[1] == 'redondeada':
                    raise
                dib['v'][v] = dib['v'][(v[0], 'redondeada')]
                sustituidas.add(v)
                print(f'Aviso: la croqueta no cabe en la vertical ({", ".join(v)}: {e}); con «Croqueta» se ve redondeada', file=sys.stderr)
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
            # (con la horizontal solo en algunas variantes, diagramas.css enseña estas notas con las que no la tienen)
            pref = f'{m["id"]}-n{o}-{lugar}'
            return ''.join(f'<svg class="d-notas-svg {clase}" data-lugar="{lugar}" data-tam="{t}" viewBox="0 0 {w} {altos[t] + 16:g}" role="img" '
                           f'aria-labelledby="{pref}-{t}"><title id="{pref}-{t}">Notas</title>{g}</svg>' for t, g in grupos.items())

        svgs = []
        if hay_h:
            svgs.append('<div class="d-fila">' + ''.join(
                dib['h'][v].svg('ancho solo-ancho', aria).replace('<svg ', f'<svg data-cajas="{v[0]}" data-forma="{v[1]}" ', 1) for v in variantes if v in dib['h'])
                + svg_notas('h', 'lado') + '</div>' + svg_notas('h', 'debajo'))
        # Cada vertical, solo para lo estrecho si su variante tiene horizontal; si no (la croqueta, más ancha, puede no
        # caber), se ve siempre: nunca se queda la figura sin dibujo.
        def svg_v(v):
            L = dib['v'][v]
            s = L.svg('vertical solo-estrecho' if v in dib['h'] else 'vertical', aria)
            if v in sustituidas:     # el mismo dibujo dos veces: ids propios en la copia
                s = s.replace(f'{L.pref}-', f'{L.pref}-cr-').replace('<svg ', '<svg data-forma-dibujo="redondeada" ', 1)
            return s.replace('<svg ', f'<svg data-cajas="{v[0]}" data-forma="{v[1]}" ', 1)
        svgs += [svg_v(v) for v in variantes]
        sin_h = ' '.join(f'{c}-{f}' for c, f in variantes if (c, f) not in dib['h'])
        svgs.append(svg_notas('v', 'debajo'))
        elegida = ('plegadas' if m['opciones']['cajas'] != 'desplegadas' else 'desplegadas', m['opciones']['forma'])
        # Bloques cerrados al empezar (decisión 415), en todas las anchuras: un estado con todos cerrados, que deja ver el
        # ciclo o la jerarquía entre ellos, y uno por bloque abierto en su sitio; «Abrir todos», el dibujo entero. Cada
        # estado, en la variante elegida (los ajustes de cajas y forma valen para el dibujo entero). Al imprimir, abiertos.
        blq = bloques(m) if m['tipo'] in ('estados', 'proceso') and not m.get('abiertos') else None
        estados = []
        for k, ab in enumerate([None] + list(range(len(m['zonas']))) if blq else []):
            mm, mc = estado_bloques(m, blq, ab)
            mm['id'], mm['marcos_bloques'] = f'{m["id"]}-e{k}', mc
            par = []
            try:
                Lh = dibujar(mm, 'h', *elegida)
            except Error:
                Lh = None
            try:
                # en la vertical, con sus pasos de al lado o todos en una columna: la que mejor se lee (sin pasar por cajas)
                una = dict(mm, nodos={k: dict(v, clases=v['clases'] - LATERALES) for k, v in mm['nodos'].items()})
                cands = []
                for mv in (mm, una):
                    try:
                        Lc = dibujar(mv, 'v', *elegida)
                        cands.append((puntuar(Lc, mv) + Lc.H / 20, len(cands), Lc))
                    except Error as e_:
                        err = e_
                if not cands:
                    raise err
                Lv = min(cands)[2]
            except Error as e:
                # sin vertical, la figura no puede empezar cerrada en el móvil: empieza abierta, como sin bloques
                print(f'Aviso: {"los bloques cerrados" if ab is None else "el bloque «" + m["zonas"][ab][0] + "» abierto"} no cabe'
                      f' en la vertical ({e}): la figura empieza abierta', file=sys.stderr)
                estados = []
                break
            if Lh is not None:
                par.append(Lh.svg('ancho solo-ancho', aria))
            par.append(Lv.svg('vertical solo-estrecho' if Lh else 'vertical', aria))
            nombre = 'cerrado' if ab is None else f'b{ab}'
            estados.append(f'<div class="d-vista" data-vista="{nombre}"{"" if ab is None else " hidden"}>' + ''.join(par) + '</div>')
        if estados:
            svgs = estados + ['<div class="d-vista" data-vista="todo" hidden>'] + svgs + ['</div>']
        return dict(svgs=svgs, estados=estados, blq=blq, dib=dib, sin_h=sin_h, errores=errores, hueco=hueco, elegida=elegida)

    # Chips (decisión del propietario): apagados, las cajas no les guardan sitio (la plegada, 40); encendidos, la figura
    # usa su otro dibujo (la plegada, 64). Con chips en los datos se dibujan los dos y la figura enseña el de su ajuste.
    con_chips = any(n['chip'] for n in m['nodos'].values())
    sin = dict(m, nodos={k: dict(v, chip='') for k, v in m['nodos'].items()})
    d = dibujos(m if m['opciones']['chips'] or not con_chips else sin)
    svgs, estados, blq, dib, sin_h, errores, hueco, elegida = (d[k] for k in ('svgs', 'estados', 'blq', 'dib', 'sin_h', 'errores', 'hueco', 'elegida'))
    if con_chips:
        si = 'si' if m['opciones']['chips'] else 'no'
        otro = dibujos(dict(sin if si == 'si' else m, id=m['id'] + '-k'))['svgs']
        marca = lambda trozos, v: [re.sub(r'^<div |<svg ', lambda x: f'{x.group(0)}data-chips="{v}" ', t) for t in trozos]
        svgs = marca(svgs, si) + marca(otro, 'no' if si == 'si' else 'si')
    dib = {o: d[elegida] for o, d in dib.items() if elegida in d}
    op = m['opciones']
    cab = [f'<p class="d-antetitulo">{escape(m["antetitulo"])}</p>']
    if m['titulo']:
        cab.append(f'<p class="d-titulo">{escape(m["titulo"])}</p>')
    if m['descripcion']:
        primera, _, resto = m['descripcion'].partition('. ')
        cab.append(f'<p class="d-desc"><span class="d-desc-1">{escape(primera + ("." if resto else ""))}</span>'
                   + (f'<span class="d-desc-resto"> {escape(resto)}</span>' if resto else '') + '</p>')
    pasos = m['recorrido']
    ayuda = ('<p class="d-ayuda">' + ('Pulsa un bloque para abrirlo en su sitio; su nombre lo vuelve a cerrar. ' if estados else '')
             + 'Pulsa un elemento para ver su ficha; pasa el ratón o llega con el tabulador para resaltar su recorrido. Escape la cierra.'
             + (' «Recorrer» lo cuenta paso a paso, con ← y →.' if pasos else '') + '</p>'
             if m['fichas'] or pasos or estados else '')
    if pasos:
        def paso(p):
            if 'nodo' in p:
                return f'<div data-paso-nodo="{p["nodo"]}">{escape(p["texto"])}</div>'
            return f'<div data-paso-de="{p["de"]}" data-paso-a="{p["a"]}">{escape(p["texto"])}</div>'
        pasos_html = '<div class="d-pasos" hidden>' + ''.join(paso(p) for p in pasos) + '</div>'
    else:
        pasos_html = ''
    fichas = ''
    if m['fichas']:
        f = []
        for nid in m['orden']:
            if nid not in m['fichas']:
                continue
            resumen, lineas = m['fichas'][nid]
            cuerpo = (f'<p>{escape(resumen)}</p>' if resumen else '') + ('<ul>' + ''.join(linea_ficha(x, m) for x in lineas) + '</ul>' if lineas else '')
            chip = m['nodos'][nid]['chip']
            tipo = f' data-tipo="{escape(chip)}"' if chip else ''
            f.append(f'<div data-ficha="{nid}" data-nombre="{escape(m["nodos"][nid]["nombre"])}"{tipo}>{cuerpo}</div>')
        fichas = '<div class="d-fichas" hidden>' + ''.join(f) + '</div>'
    if estados:     # la ficha de cada bloque cerrado (lo que lleva dentro), para el foco y el lector de pantalla
        f = []
        for z, (nombre, ids) in enumerate(m['zonas']):
            pasos_z = [m['nodos'][i]['nombre'] for i in ids if 'accion' not in m['nodos'][i]['clases']]
            f.append(f'<div data-ficha="_b{z}" data-nombre="{escape(nombre)}"><p>{escape(", ".join(pasos_z))}.</p></div>')
        fichas = (fichas[:-len('</div>')] if fichas else '<div class="d-fichas" hidden>') + ''.join(f) + '</div>'
    izq, der = (m['pie'] + ['', ''])[:2] if m['pie'] else ('', '')
    recuento = f'<span class="d-recuento">{"· " if der else ""}{len(m["nodos"])} NODOS · {len(m["flechas"])} FLECHAS</span>'
    vacio = '' if der else ' class="d-vacio"'
    pie = (f'<div class="d-pie{"" if izq or der else " d-pie-vacio"}"><span>{escape(izq)}</span>'
           f'<span{vacio}>{escape(der)}{" " if der else ""}{recuento}</span></div>')
    nuevo = any('nuevo' in n['clases'] for n in m['nodos'].values()) or any('nuevo' in f['clases'] for f in m['flechas'])
    attr = ' data-diagrama' if m['fichas'] or pasos or nuevo or estados else ''
    if estados:
        attr += f' data-bloques-forma="{blq["forma"]}"'
    if pasos:
        attr += ' data-modo="recorrer"'
    no = ' '.join(f'd-no-{k}' for k in CASILLAS if not op[k])
    datos = ''.join(f' data-d-{k}="{op[k]}"' for k in SELECTORES)
    if tema:
        datos += f' data-d-tema="{escape(tema)}"'
    if hueco and m['notas']:
        no += ' d-hueco'
    aviso_h = ''
    if sin_h:   # la horizontal no cabe (en todas o en algunas variantes): la figura lo dice si se elige
        datos += f' data-sin-h="{sin_h}" data-sin-horizontal="{escape(errores[0] if errores else "")}"'
        aviso_h = '<p class="d-aviso-h" role="note">No cabe en horizontal a este ancho: se ve en vertical.</p>'
    # con dos cauces o más, su leyenda: una raya de su color y su nombre
    leyenda = ('<p class="d-cauces" role="note">' + ''.join(
        f'<span class="d-cauce"><span class="d-cauce-m d-c-{c}" aria-hidden="true"></span>{escape(n)}</span>' for n, c in m['cauces'])
        + '</p>') if len(m.get('cauces', [])) >= 2 else ''
    if m.get('puntos_clave'):   # el comprobador mira que cada uno se vea (decisión 385)
        pk = [{'texto': p['texto'], 'nodos': [x[0] for x in p['donde'] if len(x) == 1 and x[0] in m['nodos']],
               'zonas': [m['zona_nombre'][x[0]] for x in p['donde'] if len(x) == 1 and x[0] in m.get('zona_nombre', {})],
               'flechas': [[a, b] for x in p['donde'] for a, b in zip(x, x[1:])]} for p in m['puntos_clave']]
        datos += f' data-puntos-clave="{escape(json.dumps(pk, ensure_ascii=False))}"'
    html = (f'<figure class="diagrama d-gen {no}" id="{m["id"]}"{attr}{datos} data-marca-on="auto">'
            f'<div class="d-cabecera">{"".join(cab)}</div>' + leyenda + ayuda + aviso_h + ''.join(svgs) + pie + fichas + pasos_html + '</figure>')
    return html, dib, errores


def css_tema(nombre):
    ruta = Path(nombre) if nombre.endswith('.json') else TEMAS / f'{nombre}.json'
    tema = json.loads(ruta.read_text(encoding='utf-8'))
    comun = SKILL.parent / 'crear_documentos' / 'scripts'
    if (comun / 'tema_identidad.py').is_file():  # los roles completos, con la paleta oscura derivada si falta (348)
        sys.path.insert(0, str(comun))
        from tema_identidad import normalizar_tema
        completo = normalizar_tema(json.loads(json.dumps(tema)), ruta.name)
        tema['colores'], tema['colores-oscuro'] = completo['colores'], completo['colores-oscuro']
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


FIJO = ('pasos', 'decisiones', 'flechas', 'bucles', 'etiquetas')


def ciclos(m, por_id=False):
    """Los bucles del grafo: cada ciclo simple, empezando por su nodo más pequeño (por nombres o, con por_id, por ids)."""
    nombre = (lambda n: n) if por_id else (lambda n: m['nodos'][n]['nombre'] if n in m['nodos'] else n)
    suc = {}
    for f in m['flechas']:
        if f['de'] != 'inicio':
            suc.setdefault(f['de'], []).append(f['a'])
    out = set()

    def ir(ini, n, camino):
        for v in suc.get(n, []):
            if v == ini:
                c = [nombre(x) for x in camino]
                k = c.index(min(c))
                out.add(tuple(c[k:] + c[:k]))
            elif v not in camino and v > ini:
                ir(ini, v, camino + [v])
    for n in sorted(suc):
        ir(n, n, [n])
    return out


def grafo(m):
    """Lo que dice el diagrama, por ids (el rótulo puede mejorar al rehacerlo): pasos, decisiones, flechas (de → a),
    sus etiquetas y sus bucles."""
    fl = {(f['de'], f['a']): f['etiqueta'] for f in m['flechas']}
    return {'pasos': set(m['nodos']), 'decisiones': {x for x, n in m['nodos'].items() if 'dec' in n['clases']},
            'flechas': set(fl), 'etiquetas': fl, 'bucles': ciclos(m, por_id=True)}


def comparar_grafos(antes, ahora, fijo=FIJO):
    """Lo que cambia de un diagrama a otro en lo que no puede cambiar (rehacer o convertir conserva el concepto), por
    ids; en el texto, con su rótulo."""
    a, b, out = grafo(antes), grafo(ahora), []
    rot = lambda x: (ahora['nodos'].get(x) or antes['nodos'].get(x) or {}).get('nombre') or x
    uno = lambda x: ' → '.join(rot(y) for y in x) if isinstance(x, tuple) else rot(x)
    lista = lambda xs: '», «'.join(sorted(uno(x) for x in xs))
    for k in ('pasos', 'decisiones', 'flechas', 'bucles'):
        if k in fijo:
            if a[k] - b[k]:
                out.append(f'faltan {k} del concepto: «{lista(a[k] - b[k])}»')
            if b[k] - a[k]:
                out.append(f'sobran {k} que el concepto no tiene: «{lista(b[k] - a[k])}»')
    if 'etiquetas' in fijo:
        for k in sorted(a['flechas'] & b['flechas']):
            if a['etiquetas'][k] != b['etiquetas'][k]:
                out.append(f'la flecha «{uno(k)}» decía «{a["etiquetas"][k]}» y ahora «{b["etiquetas"][k]}»')
    return out


# Lo que no es verbo + objeto en un rótulo (decisión 422): un modo («a ojo») en vez de qué se hace.
ADVERBIOS = re.compile(r'\b(a ojo|a mano|uno a uno|uno por uno|a ciegas|a la vez|sin más|tal cual|así|bien|mal|rápido|despacio|\w{4,}mente)\b', re.I)
VACIAS = set("""a al algo ante con contra de del desde el en entre es hasta la las le lo los más mi no o para pero por que qué
se si sí sin sobre su sus te tu un una uno unos unas y ya yo cada cuál cómo como este esta esto ese esa eso otro otra
todo toda todos todas muy hay ha han son ser va van vez veces lo cual cuando donde dónde""".split())


def palabras(t):
    """Las palabras con contenido de un texto, en minúsculas y sin plural sencillo."""
    out = set()
    for w in re.findall(r'[a-záéíóúüñ]{4,}', t.lower()):
        if w not in VACIAS:
            out.add(w[:-2] if w.endswith('es') and len(w) > 5 else w[:-1] if w.endswith('s') else w)
    return out


def rotulos(m, base=Path('.')):
    """Avisos de los rótulos (decisiones 422 y 423): en un proceso, cada paso, verbo y objeto («Decidir qué tests
    lanzar»), sin un modo en su lugar; con varios actores, cada paso dice cuál. El glosario inspira, no obliga (426):
    no se avisa de sus términos sin usar ni de las palabras de fuera."""
    avisos = []
    if m['tipo'] == 'proceso':
        for nid, n in m['nodos'].items():
            nombre, sub = n['nombre'], n.get('sub', '')
            if n['clases'] & {'final', 'bloque'} or nombre.startswith('¿'):
                continue
            sin_pref = re.sub(r'^[^:]{1,14}:\s*', '', nombre)      # «Ronda 1: seleccionar»: lo de después
            primera = sin_pref.split()[0].lower() if sin_pref.split() else ''
            if not re.search(r'(ar|er|ir|ír)(se|lo|la|los|las|le)?$', primera) or len(sin_pref.split()) < 2:
                avisos.append(f'«{nombre}»: ¿verbo y objeto («Decidir qué tests lanzar»)?')
            for t in (nombre, sub):
                a = ADVERBIOS.search(t)
                if a:
                    avisos.append(f'«{t}» dice cómo («{a.group(0)}»), no qué: el objeto o la consecuencia')
    pasos = [x for x in m['orden'] if not m['nodos'][x]['clases'] & {'final', 'bloque'}]
    if len(m['actores']) > 1 and m['tipo'] == 'proceso' and pasos:
        # quién: el primer paso lo dice y, después, solo donde cambia, mejor en el detalle que en cada título
        dice = lambda x, campo: any(a.lower() in (m['nodos'][x].get(campo) or '').lower() for a in m['actores'])
        if not (dice(pasos[0], 'nombre') or dice(pasos[0], 'sub') or dice(pasos[0], 'chip')):
            avisos.append(f'«{m["nodos"][pasos[0]]["nombre"]}»: ¿quién? Hay varios actores ({", ".join(m["actores"])}): '
                          'el primer paso dice cuál y, después, donde cambia')
        en_titulo = [x for x in pasos if dice(x, 'nombre')]
        if len(en_titulo) > 2 and len(en_titulo) * 2 > len(pasos):
            avisos.append('el actor va en el título de casi todos los pasos: solo donde cambia, y en el detalle')
    if m['tipo'] == 'proceso':
        sale = {}
        for f in m['flechas']:
            if f['de'] != 'inicio':
                sale.setdefault(f['de'], []).append(f)
        # un bucle dice cuándo acaba: alguna flecha sale de él con su etiqueta (o de una decisión suya)
        rot = lambda c: ' → '.join(m['nodos'][x]['nombre'] for x in c)
        for c in ciclos(m, por_id=True):
            ids = set(c)
            salidas = [f for x in ids for f in sale.get(x, []) if f['a'] not in ids and 'discontinua' not in f['clases']]
            if not any(f['etiqueta'] for f in salidas):
                avisos.append(f'el bucle «{rot(c)}» no dice cuándo acaba: una flecha que sale de él, con su condición')
            # la estructura del concepto: un bucle vuelve desde una decisión (su pregunta y sus salidas), no desde una acción
            if not any('dec' in m['nodos'][x]['clases'] for x in ids):
                avisos.append(f'el bucle «{rot(c)}» vuelve desde una acción: desde una decisión, con su pregunta («¿Falló o cambió?», dec)')
        # cada «si …» del concepto es una decisión: un paso cuyo detalle o nombre empieza por «si» lo es
        for x, n in m['nodos'].items():
            if 'dec' not in n['clases'] and any(re.match(r'(si|tras cada|cuando)\b', t.strip(), re.I) for t in (n['nombre'], n.get('sub') or '')):
                avisos.append(f'«{n["nombre"]}» es una condición: una decisión (dec) con la pregunta y sus salidas como etiquetas')
        # una rama que no vuelve dice en qué acaba (en su detalle), salvo un final, un fin o lo externo (un registro)
        for x, n in m['nodos'].items():
            if x in sale or n['clases'] & {'final', 'fin', 'externo', 'salida'}:
                continue
            origenes = [f['de'] for f in m['flechas'] if f['a'] == x and f['de'] != 'inicio']
            entra = [f for f in m['flechas'] if f['a'] == x]
            fin_flujo = any('flujo' in f['clases'] for f in entra) or (x == pasos[-1] and not any('flujo' in f['clases'] for f in m['flechas']))
            if any(len(sale.get(o, [])) > 1 for o in origenes) and not fin_flujo \
                    and not re.search(r'\b(acaba|termina|hasta|vuelve|fin|queda)\w*', n.get('sub') or '', re.I):
                avisos.append(f'«{n["nombre"]}» no vuelve al camino: ¿en qué acaba? (en su detalle)')
    # la idea, no todo el detalle (decisión 387, criterio): el número de cajas lo decide el objetivo, no el concepto
    # entero; los códigos y las cifras, a las fichas
    if m['semantica']['objetivo'] and m['tipo'] in ('proceso', 'estados') and len(m['nodos']) > 8:
        avisos.append(f'{len(m["nodos"])} cajas: ¿la versión más simple que transmite el objetivo? Una caja puede resumir '
                      'varias cosas y un punto clave verse en ella; el detalle, a las fichas (o, si todo hace falta, zonas '
                      'por actor que se abren, 415)')
    for t in [n['nombre'] for n in m['nodos'].values()] + [f['etiqueta'] or '' for f in m['flechas']]:
        c = re.search(r'\b\d{3}\b|\b\d+\s?(?:s|ms|min|seg\w*|minutos?)\b', t, re.I)
        if c:
            avisos.append(f'«{t}» lleva un código o una cifra («{c.group(0)}»): a la ficha; el dibujo, la idea')
    if m['tipo'] in ('proceso', 'estados') and m['nodos'] and not any(f['de'] == 'inicio' for f in m['flechas']):
        avisos.append('sin punto de inicio («inicio > id» en las flechas): ¿por dónde se empieza a leer?')
    # la etiqueta de una flecha dice lo que pasa o lo que viaja, no una razón
    for f in m['flechas']:
        e = f['etiqueta'] or ''
        if len(e.split()) > 3 or re.search(r'\b(porque|para|ya que|dice|según)\b', e, re.I):
            avisos.append(f'la etiqueta «{e}» explica; corta, lo que pasa o lo que viaja (el porqué, a la ficha)')
    # la discontinua, con un solo sentido en todo el diagrama: atajo del camino o efecto lateral, no los dos
    disc = [f for f in m['flechas'] if 'discontinua' in f['clases'] and f['de'] != 'inicio']
    # un atajo llega a una caja del camino (a la que llega también una flecha continua); un efecto lateral, no
    lateral = lambda x: not any(g['a'] == x and 'discontinua' not in g['clases'] for g in m['flechas'])
    if any(lateral(f['a']) for f in disc) and any(not lateral(f['a']) for f in disc):
        avisos.append('la discontinua tiene dos sentidos (un atajo del camino y un efecto lateral): uno solo, o el otro con otro trazo')
    # el id y el rótulo hablan de lo mismo: el rótulo usa la palabra del id o un término del glosario
    terminos = palabras(' '.join(t for t, _ in m['glosario']))
    for x, n in m['nodos'].items():
        if len(x) < 5 or not x.isalpha() or 'dec' in n['clases']:
            continue
        rot = palabras(n['nombre'] + ' ' + (n.get('sub') or ''))
        if not any(SequenceMatcher(None, w, x.lower()).ratio() >= .5 for w in rot) and not rot & terminos:
            avisos.append(f'«{n["nombre"]}» no habla de «{x}», su id, ni usa un término del glosario: ¿es el mismo concepto?')
    if m['glosario']:
        if not 5 <= len(m['glosario']) <= 10:
            avisos.append(f'el glosario tiene {len(m["glosario"])} términos: de cinco a diez, los importantes del gráfico')
        for t, q in m['glosario']:
            if not q:
                avisos.append(f'el término «{t}» del glosario no dice qué es («término | qué es»)')
    return avisos


def lectura(m):
    """Solo lo que se ve escrito en el dibujo, en texto, para la lectura en frío (decisión 422): las cajas con su
    detalle y su zona, y las flechas con su etiqueta; sin fichas, ni título, ni lo fijado antes de dibujar."""
    zona = {n: nombre for nombre, ids in m['zonas'] + m.get('subzonas', []) for n in ids}
    nombre = lambda x: m['nodos'][x]['nombre'] if x in m['nodos'] else (m['corchetes'][x][0] if x in m.get('corchetes', {}) else x)
    out = (['Glosario:'] + [f'- {t}: {q}' for t, q in m['glosario']] if m['glosario'] else []) + ['Cajas:']
    for x in m['orden']:
        n = m['nodos'][x]
        out.append(f'- {n["nombre"]}' + (f' ({n["sub"]})' if n.get('sub') else '') + (f' [{zona[x]}]' if x in zona else ''))
    out.append('Flechas:')
    for f in m['flechas']:
        de = 'el inicio' if f['de'] == 'inicio' else nombre(f['de'])
        out.append(f'- {de} → {nombre(f["a"])}' + (f': {f["etiqueta"]}' if f['etiqueta'] else ''))
    return chr(10).join(out)


def concepto(m, base=Path('.'), exigir=False):
    """Lo que el dibujo debe respetar de lo fijado antes de dibujar (decisiones 385 y 387): (errores, avisos).
    Errores: un punto clave sin dónde se ve o que no aparece, un módulo clave que no aparece, una carpeta que no es un
    módulo clave, una interconexión clave (o un bucle) que no aparece, un cambio de lo fijo respecto al diagrama de antes
    y, con exigir, que falten el objetivo, el concepto o los puntos clave. Sin exigir, eso último es un aviso; y otra
    forma que el diagrama con que se compara, también."""
    sem, errores, avisos = m['semantica'], [], rotulos(m, base)
    falta = [k for k, v in (('objetivo', sem['objetivo']), ('concepto', sem['concepto']), ('puntos-clave', m['puntos_clave'])) if not v]
    if falta:
        texto = (f'faltan {", ".join(f"«{k}:»" for k in falta)}: lo que los pasos 0 y 1 de la skill fijan antes de dibujar '
                 '(decisiones 385 y 387), por escrito en los datos (references/datos.md, «Antes de dibujar»)')
        (errores if exigir else avisos).append(texto)
    zonas = m.get('zona_ids_todas', [])
    pares = {(f['de'], f['a']) for f in m['flechas']}

    sig = {}
    for f in m['flechas']:
        if f['de'] != 'inicio':
            sig.setdefault(f['de'], set()).add(f['a'])

    def llega(a, b):   # hay un camino de a a b siguiendo las flechas
        vistos, pila = set(), [a]
        while pila:
            for v in sig.get(pila.pop(), ()):
                if v == b:
                    return True
                if v not in vistos:
                    vistos.add(v)
                    pila.append(v)
        return False

    def no_esta(x):    # lo que falta de un elemento de un punto clave o de una interconexión clave
        if len(x) == 1:
            return [] if x[0] in m['nodos'] or x[0] in zonas else [f'«{x[0]}»']
        # un bucle («a > b > a») nombra sus pasos clave, no todos: cada tramo, por un camino del dibujo
        bucle = len(x) > 2 and x[0] == x[-1]
        return [f'«{a} > {b}»' for a, b in zip(x, x[1:]) if (a, b) not in pares and not (bucle and llega(a, b))]
    for x in m['decisiones']:     # «decisiones:» fija qué pasos del concepto son decisiones (su pregunta, dec)
        if x not in m['nodos']:
            errores.append(f'la decisión «{x}» del concepto no es ningún nodo')
        elif 'dec' not in m['nodos'][x]['clases']:
            errores.append(f'«{m["nodos"][x]["nombre"]}» es una decisión del concepto: dec, con su pregunta y sus salidas')
    for p in m['puntos_clave']:
        if not p['donde']:
            errores.append(f'el punto clave «{p["texto"]}» no dice dónde se ve («| nodo, a > b, a > b > a»)')
        mal = [y for x in p['donde'] for y in no_esta(x)]
        if mal:
            errores.append(f'el punto clave «{p["texto"]}» no aparece: falta {", ".join(mal)}')
    if m['modulos_clave']:
        for x in m['modulos_clave']:
            if x not in m['nodos'] and x not in zonas:
                errores.append(f'el módulo clave «{x}» no aparece (ni nodo ni zona)')
        for z in zonas:
            if z not in m['modulos_clave']:
                errores.append(f'la carpeta «{z}» no es un módulo clave del concepto: las carpetas solo agrupan etapas reales')
    for b in m['interconexiones_clave']:
        mal = no_esta(b)
        if mal:
            que = 'el bucle' if len(b) > 2 and b[0] == b[-1] else 'la interconexión clave'
            errores.append(f'{que} «{" → ".join(b)}» no aparece: falta {", ".join(mal)}')
    # una pareja que se compara va en la misma forma sin tener que leer la otra (se dibujan por separado): en vertical,
    # que siempre cabe, salvo que los datos fijen otra
    if sem['compara-con'] and m['opciones']['orientacion'] == 'auto':
        m['opciones']['orientacion'] = 'vertical'
    for clave in ('antes', 'compara-con'):
        if not sem[clave]:
            continue
        ruta = (base / sem[clave])
        try:
            otro = modelo(leer(ruta.read_text(encoding='utf-8')))
        except (OSError, Error) as e:
            (errores if clave == 'antes' else avisos).append(f'«{clave}: {sem[clave]}» no se puede leer ({e})')
            continue
        if clave == 'antes':
            fijo = [x.strip() for x in sem['fijo'].split(',') if x.strip()] or FIJO
            errores += [f'respecto a {sem[clave]}: {x}' for x in comparar_grafos(otro, m, fijo)]
        else:
            efectiva = lambda x: 'vertical' if x['opciones']['orientacion'] == 'auto' else x['opciones']['orientacion']
            if efectiva(otro) != m['opciones']['orientacion']:
                avisos.append(f'va en {m["opciones"]["orientacion"]} y {sem[clave]}, con el que se compara, en {efectiva(otro)}: la misma forma')
            if {t for t, _ in otro['glosario']} != {t for t, _ in m['glosario']}:
                avisos.append(f'el glosario no es el mismo que el de {sem[clave]}, con el que se compara: los dos, el mismo (decisión 423)')
            for k in ('cajas', 'forma'):
                if otro['opciones'][k] != m['opciones'][k]:
                    avisos.append(f'«{k}» es «{m["opciones"][k]}» y en {sem[clave]}, con el que se compara, «{otro["opciones"][k]}»: misma forma y escala')
            if otro['tipo'] != m['tipo']:
                avisos.append(f'es de tipo «{m["tipo"]}» y {sem[clave]}, con el que se compara, de «{otro["tipo"]}»')
    return errores, avisos


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='Genera un diagrama de la SF a partir de datos breves.')
    ap.add_argument('datos', type=Path)
    ap.add_argument('-o', '--salida', type=Path)
    ap.add_argument('--tema', default='tinta')
    ap.add_argument('--fragmento', action='store_true', help='solo la <figure>, sin página')
    ap.add_argument('--sin-comprobar', action='store_true')
    ap.add_argument('--medidas', action='store_true', help='las medidas de lectura de cada dibujo (bucle de afinado)')
    ap.add_argument('--lectura', action='store_true', help='solo los rótulos y las flechas en texto, para la lectura en frío')
    ap.add_argument('--exigir', action='store_true', help='sin objetivo, concepto o puntos clave en los datos, no genera')
    ap.add_argument('--antes', type=Path, help='el diagrama de antes: rehacerlo conserva su concepto (pasos, flechas, bucles y etiquetas)')
    ap.add_argument('--capturas', type=Path, help='carpeta para la captura de la figura en cada ancho y modo (comprobador)')
    a = ap.parse_args(argv)
    try:
        m = modelo(leer(a.datos.read_text(encoding='utf-8')))
        m['id'] = re.sub(r'[^a-z0-9]+', '-', a.datos.stem.lower()).strip('-') or 'd'
        if a.antes:
            m['semantica']['antes'] = str(a.antes.resolve())
        if a.lectura:
            print(lectura(m))
            return 0
        m['exigir'] = a.exigir
        mal, avisos = concepto(m, a.datos.parent, a.exigir)
        for x in avisos:
            print(f'· {x}', file=sys.stderr)
        if mal:
            raise Error('el dibujo contradice su cabecera semántica:' + ''.join(chr(10) + '  ' + x for x in mal))
        if a.fragmento:
            html, _, errores = figura(m, Path(a.tema).stem)
        else:
            html, errores = pagina(m, a.tema)
        if a.medidas:
            for o, nombre in (('v', 'vertical'), ('h', 'horizontal')):
                for v in [(c, f) for c in VARIANTES['cajas'] for f in VARIANTES['forma'][:1]]:
                    try:
                        print(texto_medidas(medidas(dibujar(m, o, *v), m), f'{nombre}, {v[0]}'))
                    except Error:
                        pass
    except Error as e:
        print(f'✕ {e}', file=sys.stderr)
        return 2
    for e in errores:
        print(f'· sin horizontal: {e}', file=sys.stderr)
    if errores and m['opciones']['orientacion'] == 'horizontal':
        print('Aviso: los datos piden la horizontal y no cabe: la figura se ve en vertical y lo dice al lector', file=sys.stderr)
    salida = a.salida or a.datos.with_suffix('.html')
    salida.write_text(html, encoding='utf-8')
    print(f'{salida} ({len(html)} caracteres)')
    if a.fragmento or a.sin_comprobar:
        return 0
    extra = ['--capturas', str(a.capturas)] if a.capturas else []
    r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(AQUI / 'comprobar_diagramas.py'), str(salida), '--oscuro'] + extra)
    return r.returncode


if __name__ == '__main__':
    sys.exit(main())
