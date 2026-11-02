"""Coloreado de sintaxis de los bloques de código, sin dependencias.

Lo usa doc_to_html.py sobre el HTML que deja markdown (<pre><code class="language-x">). Cada fragmento
reconocido va en un <span class="sx-…">; los colores están en estilo_base.css (variables --sx-…).
Un bloque sin lenguaje se colorea como JSON si lo es; el resto (text, árboles de carpetas…) se deja igual.

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


def colorear(codigo: str, lenguaje: str) -> str:
    """Código en texto plano → HTML escapado con <span class="sx-…">."""
    clases = [c for c, _ in _LENGUAJES[lenguaje]]
    salida, pos = [], 0
    for m in _regex(lenguaje).finditer(codigo):
        if m.start() == m.end():
            continue
        salida.append(_html.escape(codigo[pos:m.start()], quote=False))
        clase = clases[int(m.lastgroup[1:])]
        salida.append(f'<span class="{clase}">' + _html.escape(m.group(0), quote=False) + '</span>')
        pos = m.end()
    salida.append(_html.escape(codigo[pos:], quote=False))
    return ''.join(salida)


def _es_json(texto: str) -> bool:
    t = texto.strip()
    if not t or t[0] not in '{[':
        return False
    try:
        json.loads(t)
        return True
    except ValueError:
        return False


def resaltar(html: str) -> str:
    """Colorea los <pre><code> de un HTML generado por markdown."""
    def uno(m):
        lenguaje, cuerpo = (m.group(1) or '').lower(), m.group(2)
        codigo = _html.unescape(cuerpo)
        lenguaje = _ALIAS.get(lenguaje, lenguaje)
        if not lenguaje and _es_json(codigo):
            lenguaje = 'json'
        if lenguaje not in _LENGUAJES:
            return m.group(0)
        return f'<pre><code class="language-{lenguaje}">' + colorear(codigo, lenguaje) + '</code></pre>'
    return re.sub(r'<pre><code(?: class="language-([\w+-]+)")?>([\s\S]*?)</code></pre>', uno, html)
