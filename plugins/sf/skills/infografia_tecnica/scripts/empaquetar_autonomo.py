"""Crea una versión autónoma (offline) de una infografía para enviarla como archivo.

Uso: python empaquetar_autonomo.py <infografia.html> <salida.html> [version_three, por defecto la del import map]
Descarga three.js y los addons usados, los incrusta como scripts de texto, genera un
import map con URL blob en tiempo de ejecución y añade el esqueleto HTML completo.
"""
import os, re, sys, time, urllib.request
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
# versión de three: la del argumento o, si no, la del import map de la propia página
m = re.search(r'three@([\d.]+)/', s)
ver = sys.argv[3] if len(sys.argv) > 3 else (m.group(1) if m else '0.186.1')
s = re.sub(r'^<meta charset="utf-8">\n', '', s)
s = re.sub(r'<!-- respaldo para Safari.*?</script>\n', '', s, flags=re.S)
s = re.sub(r'<script type="importmap">.*?</script>\n', '', s, flags=re.S)
addons = sorted(set(re.findall(r"from 'three/addons/([^']+)'", s)))
specs = {'three': 'build/three.module.js', **{f'three/addons/{a}': f'examples/jsm/{a}' for a in addons}}
cache = os.path.join(os.path.expanduser('~'), '.cache', 'infografia_tecnica', f'three-{ver}')
def fetch(path):
    # caché local + reintentos: la descarga del CDN a veces se corta
    local = os.path.join(cache, path.replace('/', '_'))
    if os.path.exists(local):
        return open(local, encoding='utf-8').read()
    for i in range(4):
        try:
            code = urllib.request.urlopen(f'https://cdn.jsdelivr.net/npm/three@{ver}/{path}', timeout=60).read().decode('utf-8')
            os.makedirs(cache, exist_ok=True); open(local, 'w', encoding='utf-8').write(code)
            return code
        except Exception as e:
            print('reintento', i + 1, path, e); time.sleep(2 + 2 * i)
    raise SystemExit('No se pudo descargar ' + path)
def fetch_url(url):
    # scripts clásicos de CDN (GSAP y sus plugins): misma caché y reintentos
    local = os.path.join(os.path.expanduser('~'), '.cache', 'infografia_tecnica', 'cdn', re.sub(r'[^\w.-]', '_', url))
    if os.path.exists(local):
        return open(local, encoding='utf-8').read()
    for i in range(4):
        try:
            code = urllib.request.urlopen(url, timeout=60).read().decode('utf-8')
            os.makedirs(os.path.dirname(local), exist_ok=True); open(local, 'w', encoding='utf-8').write(code)
            return code
        except Exception as e:
            print('reintento', i + 1, url, e); time.sleep(2 + 2 * i)
    raise SystemExit('No se pudo descargar ' + url)
s = re.sub(r'<script src="(https://(?:cdnjs\.cloudflare\.com|cdn\.jsdelivr\.net|unpkg\.com)/[^"]+)"></script>',
           lambda m: '<script>' + fetch_url(m.group(1)).replace('</script', '<' + chr(92) + '/script') + '</script>', s)
blocks = []
queue = list(specs.items()); done = set()
while queue:
    spec, path = queue.pop(0)
    if spec in done: continue
    done.add(spec)
    code = fetch(path)
    # los addons se importan entre sí con rutas relativas (../shaders/CopyShader.js): con URL blob
    # no se resuelven, así que se pasan a especificadores 'three/addons/…' y se incluyen también
    def rel(m):
        target = os.path.normpath(os.path.join(os.path.dirname(path), m.group(2))).replace(os.sep, '/')
        sp = 'three/addons/' + target[len('examples/jsm/'):]
        queue.append((sp, target))
        return m.group(1) + sp + m.group(3)
    code = re.sub(r"""(from\s*['"])(\.{1,2}/[^'"]+)(['"])""", rel, code)
    blocks.append(f'<script type="text/plain" data-spec="{spec}">' + code.replace('</script', '<' + chr(92) + '/script') + '</script>')
loader = """<script>
(function(){var m={imports:{}};document.querySelectorAll('script[data-spec]').forEach(function(e){m.imports[e.getAttribute('data-spec')]=URL.createObjectURL(new Blob([e.textContent],{type:'text/javascript'}));});
var i=document.createElement('script');i.type='importmap';i.textContent=JSON.stringify(m);document.currentScript.after(i);})();
</script>
"""
i = s.index('<script type="module">')
s = s[:i] + '\n'.join(blocks) + '\n' + loader + s[i:]
j = s.index('</style>') + len('</style>')
s = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
     '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
     + s[:j] + '\n</head>\n<body>\n' + s[j:] + '\n</body>\n</html>\n')
open(out, 'w', encoding='utf-8').write(s)
print(out, len(s) // 1024, 'KB')
