"""Bloques de código de los documentos: coloreado de sintaxis propio, sin dependencias, y su caja.

Lo usa documento_a_html.py sobre el HTML que deja markdown (<pre><code class="language-x">). Cada bloque va en una caja
<div class="codigo" data-lenguaje="x"> con una barra con el nombre del lenguaje (si lo tiene); el plegado y el botón «Copiar» los
ponen assets/codigo.js. Cada fragmento reconocido va en un <span class="sx-…">; los colores y la caja están en
assets/estilo_documento.css (variables --sx-…; pagina.codigo del estilo elige la forma de la caja). Un bloque sin
lenguaje se colorea como JSON si lo es; el resto (text, árboles de carpetas, un lenguaje sin coloreado) sale igual,
en su caja.

Clases: sx-c comentario, sx-s cadena, sx-n número o literal, sx-k palabra clave, sx-p clave o propiedad,
sx-f orden o función, sx-t etiqueta, sx-a atributo u opción.
"""
import html as _html
import json
import re

_CAD = r'"(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\''
_NUM = r'-?\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b'


def _kw(*palabras):
    return r'\b(?:' + '|'.join(palabras) + r')\b'


# Cada lenguaje: lista de (clase, patrón) en orden de prioridad.
_LENGUAJES = {
    'json': [
        ('sx-p', r'"(?:[^"\\\n]|\\.)*"(?=\s*:)'),
        ('sx-s', r'"(?:[^"\\\n]|\\.)*"'),
        ('sx-n', _NUM + r'|\b(?:true|false|null)\b'),
    ],
    'javascript': [
        ('sx-c', r'//[^\n]*|/\*[\s\S]*?\*/'),
        ('sx-s', _CAD + r'|`(?:[^`\\]|\\.)*`'),
        ('sx-k', _kw('const', 'let', 'var', 'function', 'return', 'if', 'else', 'for', 'while', 'do', 'of', 'in',
                     'new', 'class', 'extends', 'import', 'export', 'from', 'default', 'async', 'await', 'try',
                     'catch', 'finally', 'throw', 'switch', 'case', 'break', 'continue', 'typeof', 'instanceof',
                     'interface', 'type', 'as', 'this', 'yield', 'delete', 'void')),
        ('sx-n', _NUM + r'|\b(?:true|false|null|undefined|NaN)\b'),
        ('sx-f', r'\b[A-Za-z_$][\w$]*(?=\s*\()'),
    ],
    'python': [
        ('sx-c', r'#[^\n]*'),
        ('sx-s', r'[rbfuRBFU]{0,2}(?:"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|' + _CAD + ')'),
        ('sx-k', _kw('def', 'return', 'if', 'elif', 'else', 'for', 'while', 'in', 'not', 'and', 'or', 'is',
                     'import', 'from', 'as', 'class', 'with', 'try', 'except', 'finally', 'raise', 'lambda',
                     'pass', 'break', 'continue', 'yield', 'global', 'nonlocal', 'assert', 'async', 'await', 'del')),
        ('sx-n', _NUM + r'|\b(?:True|False|None)\b'),
        ('sx-f', r'\b[A-Za-z_]\w*(?=\s*\()'),
    ],
    'bash': [
        ('sx-c', r'(?:^|(?<=\s))#[^\n]*'),
        ('sx-s', _CAD),
        ('sx-n', r'\$\{[^}\n]*\}|\$[A-Za-z_]\w*|\$env:\w+'),
        ('sx-f', r'^[ \t]*[A-Za-z_][\w./-]*|(?<=\| )[A-Za-z_][\w.-]*|(?<=; )[A-Za-z_][\w.-]*|(?<=&& )[A-Za-z_][\w.-]*'),
        ('sx-a', r'(?<=\s)--?[A-Za-z][\w-]*'),
    ],
    'css': [
        ('sx-c', r'/\*[\s\S]*?\*/'),
        ('sx-s', _CAD),
        ('sx-p', r'--?[A-Za-z][\w-]*(?=\s*:)'),
        ('sx-n', r'#[0-9a-fA-F]{3,8}\b|-?\b\d+(?:\.\d+)?(?:px|rem|em|%|vh|vw|s|ms|deg|fr)?\b'),
        ('sx-k', r'@[\w-]+|!important'),
    ],
    'html': [
        ('sx-c', r'<!--[\s\S]*?-->'),
        ('sx-t', r'</?[A-Za-z][\w:-]*|/?>'),
        ('sx-a', r'(?<=\s)[A-Za-z_:][\w:.-]*(?==)'),
        ('sx-s', _CAD),
    ],
    'sql': [
        ('sx-c', r'--[^\n]*|/\*[\s\S]*?\*/'),
        ('sx-s', r"'(?:[^']|'')*'"),
        ('sx-k', r'(?i)\b(?:select|from|where|and|or|not|insert|into|values|update|set|delete|create|table|alter|'
                 r'drop|add|column|index|on|join|left|right|inner|outer|group|by|order|having|limit|as|primary|key|'
                 r'foreign|references|unique|default|null|is|in|exists|distinct|union|all|case|when|then|else|end|'
                 r'begin|commit|rollback|constraint|check|if)\b'),
        ('sx-n', _NUM),
    ],
    'yaml': [
        ('sx-c', r'(?:^|(?<=\s))#[^\n]*'),
        ('sx-p', r'(?m)^\s*-?\s*[\w.-]+(?=\s*:)'),
        ('sx-s', _CAD),
        ('sx-n', _NUM + r'|\b(?:true|false|null|yes|no)\b'),
    ],
}
_ALIAS = {'js': 'javascript', 'ts': 'javascript', 'typescript': 'javascript', 'tsx': 'javascript', 'jsx': 'javascript',
          'mjs': 'javascript', 'jsonc': 'javascript', 'py': 'python', 'sh': 'bash', 'shell': 'bash', 'console': 'bash',
          'zsh': 'bash', 'powershell': 'bash', 'ps1': 'bash', 'pwsh': 'bash', 'xml': 'html', 'svg': 'html',
          'yml': 'yaml', 'scss': 'css'}
_COMPILADOS = {}


def _regex(lenguaje):
    if lenguaje not in _COMPILADOS:
        partes = []
        for i, (_, patron) in enumerate(_LENGUAJES[lenguaje]):
            banderas = ''
            m = re.match(r'\(\?([a-z]+)\)', patron)
            if m:  # las banderas en línea solo valen al principio: se aplican al grupo
                banderas, patron = m.group(1), patron[m.end():]
            partes.append(f'(?P<g{i}>' + (f'(?{banderas}:' + patron + ')' if banderas else patron) + ')')
        _COMPILADOS[lenguaje] = re.compile('|'.join(partes), re.M)
    return _COMPILADOS[lenguaje]


def _fichas(codigo: str, lenguaje: str) -> list:
    """Código en texto plano → [(clase o None, texto)], con las reglas del lenguaje (sin reglas, todo sin clase)."""
    if lenguaje not in _LENGUAJES:
        return [(None, codigo)]
    clases = [c for c, _ in _LENGUAJES[lenguaje]]
    fichas, pos = [], 0
    for m in _regex(lenguaje).finditer(codigo):
        if m.start() == m.end():
            continue
        if m.start() > pos:
            fichas.append((None, codigo[pos:m.start()]))
        fichas.append((clases[int(m.lastgroup[1:])], m.group(0)))
        pos = m.end()
    if pos < len(codigo):
        fichas.append((None, codigo[pos:]))
    return fichas


def _html_ficha(clase, texto: str) -> str:
    t = _html.escape(texto, quote=False)
    return f'<span class="{clase}">{t}</span>' if clase else t


def colorear(codigo: str, lenguaje: str) -> str:
    """Código en texto plano → HTML escapado con <span class="sx-…">."""
    return ''.join(_html_ficha(c, t) for c, t in _fichas(codigo, lenguaje))


def _lineas(fichas: list) -> list:
    """Las fichas partidas por líneas: [[(clase, texto), …], …]. Una ficha de varias líneas (un comentario, una cadena
    larga) se parte en una por línea, con su clase en cada trozo, para que cada línea sea HTML cerrado."""
    lineas = [[]]
    for clase, texto in fichas:
        for i, trozo in enumerate(texto.split('\n')):
            if i:
                lineas.append([])
            if trozo:
                lineas[-1].append((clase, trozo))
    return lineas


# --- Ámbitos plegables ------------------------------------------------------------------------------------------------
# Cada línea que abre un ámbito de dos líneas o más lleva su flecha (la pone assets/codigo.js): por llaves y corchetes
# en los lenguajes de llaves; por sangría en los demás y sin lenguaje. Un ámbito es (línea de apertura, última línea de
# su cuerpo): plegado, se ve la de apertura con «…» y la siguiente al cuerpo (la de cierre, en los de llaves).
POR_LLAVES = {'json', 'jsonc', 'json5', 'javascript', 'js', 'mjs', 'ts', 'typescript', 'tsx', 'jsx', 'css', 'scss',
              'less', 'powershell', 'ps1', 'pwsh', 'rust', 'rs', 'c', 'cpp', 'h', 'hpp', 'cs', 'csharp', 'java', 'kotlin',
              'kt', 'go', 'swift', 'php', 'dart', 'scala', 'groovy', 'hcl', 'tf'}
# Para buscar las llaves de un lenguaje sin coloreado: las cadenas y los comentarios no cuentan.
_GENERICO = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|' + _CAD)


def _fichas_genericas(codigo: str) -> list:
    fichas, pos = [], 0
    for m in _GENERICO.finditer(codigo):
        fichas += [(None, codigo[pos:m.start()]), ('sx-c' if m.group(0)[0] == '/' else 'sx-s', m.group(0))]
        pos = m.end()
    return fichas + [(None, codigo[pos:])]


def _ambitos_llaves(fichas: list) -> list:
    """Ámbitos entre {} y [] fuera de cadenas y comentarios, con al menos una línea entre la apertura y el cierre."""
    pila, ambitos, n = [], [], 0
    for clase, texto in fichas:
        if clase in ('sx-s', 'sx-c'):
            n += texto.count('\n')
            continue
        for ch in texto:
            if ch == '\n':
                n += 1
            elif ch in '{[':
                pila.append((ch, n))
            elif ch in '}]':
                if pila and pila[-1][0] == {'}': '{', ']': '['}[ch]:
                    inicio = pila.pop()[1]
                    if n - inicio >= 2:
                        ambitos.append((inicio, n - 1))
                else:
                    pila.clear()  # descompensadas: no se adivina
    return ambitos


def _ambitos_sangria(lineas: list) -> list:
    """Ámbitos por sangría: una línea seguida de otras más sangradas (las líneas en blanco del medio van dentro; las
    del final, fuera)."""
    sangria = [len(l) - len(l.lstrip(' \t')) if l.strip() else None for l in lineas]
    ambitos = []
    for i, s in enumerate(sangria):
        if s is None:
            continue
        fin = None
        for j in range(i + 1, len(sangria)):
            if sangria[j] is not None:
                if sangria[j] <= s:
                    break
                fin = j
        if fin is not None:
            ambitos.append((i, fin))
    return ambitos


def ambitos(codigo: str, escrito: str, lenguaje: str) -> list:
    """Los ámbitos plegables de un bloque: [(apertura, última línea del cuerpo)], uno por línea de apertura (el
    mayor). «escrito», el lenguaje como lo puso el autor; «lenguaje», el del coloreado. Por llaves, los lenguajes de
    llaves y uno sin coloreado que las tenga; por sangría, los demás y el bloque sin lenguaje."""
    sin_coloreado = escrito not in _SIN_NOMBRE and lenguaje not in _LENGUAJES
    encontrados = []
    if escrito in POR_LLAVES or sin_coloreado:
        fichas = _fichas(codigo, lenguaje) if lenguaje in _LENGUAJES else _fichas_genericas(codigo)
        encontrados = _ambitos_llaves(fichas)
    if not encontrados and escrito not in POR_LLAVES:
        encontrados = _ambitos_sangria(codigo.split('\n'))
    mayor = {}
    for inicio, fin in encontrados:
        mayor[inicio] = max(fin, mayor.get(inicio, -1))
    return sorted(mayor.items())


def con_ambitos(lineas: list, ambs: list) -> str:
    """Las líneas (HTML) con sus ámbitos: <span class="amb"><span class="amb-cabeza">apertura<span class="amb-marca">
    </span>⏎</span><span class="amb-cuerpo">…</span></span>. El texto no cambia: cada línea, con su salto."""
    por_inicio = dict(ambs)
    salida, abiertos = [], []
    for i, linea in enumerate(lineas):
        salto = '\n' if i < len(lineas) - 1 else ''
        if i in por_inicio:
            salida.append(f'<span class="amb"><span class="amb-cabeza">{linea}<span class="amb-marca"></span>{salto}'
                          '</span><span class="amb-cuerpo">')
            abiertos.append(por_inicio[i])
        else:
            salida.append(linea + salto)
        while abiertos and abiertos[-1] == i:
            abiertos.pop()
            salida.append('</span></span>')
    return ''.join(salida) + '</span></span>' * len(abiertos)


def _es_json(texto: str) -> bool:
    t = texto.strip()
    if not t or t[0] not in '{[':
        return False
    try:
        json.loads(t)
        return True
    except ValueError:
        return False


# El nombre que se ve en la barra del bloque; un lenguaje que no está aquí sale tal cual lo escribió el autor.
_NOMBRES = {'json': 'JSON', 'jsonc': 'JSON', 'javascript': 'JavaScript', 'js': 'JavaScript', 'mjs': 'JavaScript',
            'ts': 'TypeScript', 'typescript': 'TypeScript', 'tsx': 'TSX', 'jsx': 'JSX', 'python': 'Python', 'py': 'Python',
            'bash': 'Bash', 'sh': 'Shell', 'shell': 'Shell', 'zsh': 'Zsh', 'console': 'Consola', 'powershell': 'PowerShell',
            'ps1': 'PowerShell', 'pwsh': 'PowerShell', 'css': 'CSS', 'scss': 'SCSS', 'html': 'HTML', 'xml': 'XML',
            'svg': 'SVG', 'sql': 'SQL', 'yaml': 'YAML', 'yml': 'YAML'}
_SIN_NOMBRE = {'', 'text', 'txt', 'plain', 'plaintext', 'texto'}


def caja(cuerpo_html: str, escrito: str, lenguaje: str) -> str:
    """El bloque en su caja: «escrito», el lenguaje como lo puso el autor (el nombre de la barra); «lenguaje», el del
    coloreado (vacío si no se colorea)."""
    nombre = '' if escrito in _SIN_NOMBRE else _NOMBRES.get(escrito, escrito)
    datos = f' data-lenguaje="{_html.escape(escrito)}"' if escrito else ''
    barra = (f'<div class="codigo-barra"><span class="codigo-lenguaje">{_html.escape(nombre)}</span></div>'
             if nombre else '')
    clase = f' class="language-{lenguaje or escrito}"' if (lenguaje or escrito) else ''
    return f'<div class="codigo"{datos}>{barra}<pre><code{clase}>{cuerpo_html}</code></pre></div>'


def resaltar(html: str) -> str:
    """Pone en su caja, colorea y marca los ámbitos plegables de los <pre><code> de un HTML generado por markdown."""
    def uno(m):
        escrito, cuerpo = (m.group(1) or '').lower(), m.group(2)
        codigo = _html.unescape(cuerpo)
        lenguaje = _ALIAS.get(escrito, escrito)
        if not lenguaje and _es_json(codigo):
            lenguaje = 'json'
        final = '\n' if codigo.endswith('\n') else ''
        codigo = codigo[:len(codigo) - len(final)]
        lineas = [''.join(_html_ficha(c, t) for c, t in linea) for linea in _lineas(_fichas(codigo, lenguaje))]
        cuerpo_html = con_ambitos(lineas, ambitos(codigo, escrito, lenguaje)) + final
        return caja(cuerpo_html, escrito, lenguaje if lenguaje in _LENGUAJES else '')
    return re.sub(r'<pre><code(?: class="language-([\w+-]+)")?>([\s\S]*?)</code></pre>', uno, html)
