"""Revisión de lo que sale al publicar en un repositorio público («La SF se trabaja en el repositorio público, con
revisión antes de publicar», 252). La lanza RELEASE antes de tocar nada; también se puede lanzar a mano.

Con comandos y sin Claude, mira cada commit nuevo (desde el último tag hasta develop): su mensaje, las líneas que
añade y los archivos que toca. Busca secretos (claves privadas, tokens de GitHub, Anthropic, AWS, Slack, Google, y
contraseñas o claves escritas en el código), datos personales (correos, el usuario y el nombre de esta máquina, rutas
de una carpeta de usuario o de la carpeta que contiene el repositorio) y archivos internos que no deben salir (.env,
claves, la cola y el estado local de la SF, los ajustes locales de Claude Code). Solo lee.

Dice si el remoto es público, según `gh repo view` (sin poder saberlo, se trata como público). Tres niveles
(decisión 259):
- ya publicado: un texto que ya está en el árbol del último tag (--desde), o en el mensaje de un commit publicado; no
  cuenta;
- subido: lo de un commit que ya está en <remoto>/develop (la referencia local, sin fetch); se enseña y se pide permiso;
- nuevo: lo de un commit aún sin subir; con el remoto público, bloquea; con el privado, se pregunta.
Tampoco cuentan los correos de los autores de esos commits y el de git config user.email (ya salen con cada commit),
ni lo que el proyecto da por publicable en .sf/publicable.txt, una entrada por línea (# para comentarios), sin
distinguir mayúsculas: un texto, que basta con que aparezca en el hallazgo, o «archivo:PATRÓN», que deja pasar todo lo
de los archivos que casan con el patrón (fnmatch, p. ej. «archivo:docs/referencias/*»).

Antes de subir (antes_de_subir; decisión 259), lo mismo para RELEASE y para el push de develop al cerrar una tarea:
nada que contar, sigue; algo nuevo con el remoto público, se para («bloquear»); lo demás (lo ya subido, o cualquier
cosa con el remoto privado), se enseña y se pide permiso: repetir la misma acción en 10 minutos, con los mismos
hallazgos, es darlo. Lo aceptado se guarda en el directorio de git (sf-revision.json) y no se vuelve a preguntar. El
push del cierre solo revisa con el remoto público (--solo-publico).

Mirar no es dar permiso (tarea 332): el intento y su repetición solo los anotan las acciones reales, que se nombran con
--accion (release, el botón RELEASE; subir, el push de develop al cerrar y `cola.py subir`), y la repetición tiene que
ser de la misma acción. Sin --accion, --decidir solo enseña lo que pasaría: no anota ningún intento ni acepta nada,
por muchas veces que se lance a mano.

Uso:
  python -I -X utf8 revision_publica.py [--repo RUTA] [--remoto origin] [--desde vX.Y.Z] [--hasta develop] [--json]
      La lista de hallazgos. Sale con 0 si no hay nada, con 3 si hay y con 1 si no puede revisar. Sin --desde, todos
      los commits de --hasta.
  python -I -X utf8 revision_publica.py … --decidir [--accion release|subir] [--repetir "cómo dar el permiso"]
          [--solo-publico] [--json]
      Lo que hacer antes de subir: {accion: seguir|permiso|bloquear, mensaje}. Sale con 0 si sigue y con 3 si no.
      Sin --desde, el último tag vX.Y.Z. Sin --accion, solo mira: no guarda nada.
"""

from __future__ import annotations

import argparse
import fnmatch
import getpass
import json
import os
import re
import socket
import subprocess
import sys
from pathlib import Path

PERMITIDOS = Path('.sf') / 'publicable.txt'
MAX_TEXTO = 120

SECRETOS = [
    ('clave privada', re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----')),
    ('token de GitHub', re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})')),
    ('clave de Anthropic', re.compile(r'\bsk-ant-[A-Za-z0-9_-]{20,}')),
    ('clave de API', re.compile(r'\bsk-[A-Za-z0-9]{32,}')),
    ('clave de AWS', re.compile(r'\bAKIA[0-9A-Z]{16}\b')),
    ('token de Slack', re.compile(r'\bxox[abprs]-[A-Za-z0-9-]{10,}')),
    ('clave de Google', re.compile(r'\bAIza[0-9A-Za-z_-]{35}')),
    ('contraseña o clave escrita', re.compile(
        r'(?i)\b(?:password|passwd|contraseña|secret|token|api[_-]?key|client_secret)\b["\']?\s*[:=]\s*["\'][^"\'\s]{8,}["\']')),
]
CORREO = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
# Los correos que no son de nadie: los de ejemplo y los «noreply».
CORREO_GENERICO = re.compile(r'(?i)(noreply|no-reply|@example\.|@ejemplo\.|@test\.|@x\.|@localhost)')
# La carpeta de un usuario: C:\Users\<nombre>, /home/<nombre>, /Users/<nombre>, hasta el final de la ruta; sin los
# nombres de ejemplo.
FIN_RUTA = r'[^\s"\'`<>|,;()\[\]{}*«»“”]*(?<![.:])'
CARPETA_USUARIO = re.compile(
    r'(?i)(?:\b[A-Z]:[\\/]{1,2}Users|(?<![\w.])/home|(?<![\w.])/Users)[\\/]{1,2}([^\\/\s"\'`<>%$*{}()|,;:]+)' + FIN_RUTA)
NOMBRES_EJEMPLO = {'usuario', 'user', 'username', 'nombre', 'name', 'you', 'tu', 'yo', 'me', 'public', 'default',
                   'all users', 'runner', 'x', 'xxx', 'foo', 'ejemplo', 'example', '<usuario>', '<user>'}
INTERNOS = [
    ('variables de entorno', re.compile(r'(^|/)\.env(\.(?!example$|ejemplo$|sample$)[^/]+)?$')),
    ('clave o certificado', re.compile(r'\.(pem|key|p12|pfx)$|(^|/)id_(rsa|ed25519|ecdsa|dsa)(\.pub)?$')),
    ('credenciales', re.compile(r'(^|/)credentials[^/]*\.json$')),
    ('estado local de la SF', re.compile(
        r'(^|/)\.sf/(peticiones\.json|peticiones\.lock|historial\.jsonl|copias/|subagentes\.json|prueba\.json|'
        r'prueba\.log|registro\.json|estado\.json)')),
    ('ajustes locales de Claude Code', re.compile(r'(^|/)\.claude/(settings\.local\.json|worktrees/)')),
]
RUTA_MAQUINA = 'ruta de esta máquina'
USUARIO_MAQUINA = 'usuario de esta máquina'


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, encoding='utf-8',
                          errors='replace')


def repo_github(url: str) -> str | None:
    """«dueño/nombre» de una url de GitHub (https o ssh); None si no es de GitHub."""
    m = re.match(r'^(?:https?://(?:[^@/]+@)?github\.com/|git@github\.com:|ssh://git@github\.com/)([^/]+/[^/]+?)(?:\.git)?/?$',
                 url.strip())
    return m.group(1) if m else None


def visibilidad(repo: Path, remoto: str) -> str | None:
    """PUBLIC, PRIVATE o INTERNAL, según gh; LOCAL si el remoto es una carpeta de esta máquina; None si no se puede
    saber (sin gh, sin red o sin ese remoto)."""
    r = git(repo, 'remote', 'get-url', remoto)
    url = r.stdout.strip() if r.returncode == 0 else ''
    if url and (url.startswith('file://') or not re.match(r'^[\w+.-]+://|^[^/\\:]+@[^:]+:', url)):
        return 'LOCAL'
    nombre = repo_github(url) if url else None
    if not nombre:
        return None
    try:
        v = subprocess.run(['gh', 'repo', 'view', nombre, '--json', 'visibility', '-q', '.visibility'],
                           capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    valor = v.stdout.strip().upper()
    return valor if v.returncode == 0 and valor in ('PUBLIC', 'PRIVATE', 'INTERNAL') else None


def permitidos(repo: Path) -> tuple[list[str], list[str]]:
    """(textos, patrones de archivo) de .sf/publicable.txt, en minúsculas."""
    try:
        lineas = (repo / PERMITIDOS).read_text(encoding='utf-8').splitlines()
    except OSError:
        return [], []
    entradas = [x.strip().lower() for x in lineas if x.strip() and not x.strip().startswith('#')]
    archivos = [x[len('archivo:'):].strip() for x in entradas if x.startswith('archivo:')]
    return [x for x in entradas if not x.startswith('archivo:')], [x for x in archivos if x]


def identidad_maquina(repo: Path) -> list[tuple[str, str]]:
    """Lo que identifica esta máquina: su usuario, su nombre y la carpeta que contiene el repositorio."""
    datos = []
    try:
        usuario = getpass.getuser()
    except Exception:  # noqa: BLE001 (sin usuario que leer)
        usuario = os.environ.get('USERNAME') or os.environ.get('USER') or ''
    if len(usuario) >= 3 and usuario.lower() not in NOMBRES_EJEMPLO:
        datos.append((USUARIO_MAQUINA, usuario))
    for host in {socket.gethostname(), os.environ.get('COMPUTERNAME', '')}:
        if len(host) >= 3 and host.lower() != 'localhost':
            datos.append(('nombre de esta máquina', host))
    padre = str(repo.resolve().parent)
    if len(Path(padre).parts) > 1:
        datos.append((RUTA_MAQUINA, padre))
    return datos


def buscar_en(texto: str, correos_autores: set[str], maquina: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Los hallazgos de una línea: (motivo, texto encontrado). Las rutas, enteras, para distinguirlas de las ya
    publicadas que empiezan igual."""
    halla = []
    for motivo, patron in SECRETOS:
        for m in patron.finditer(texto):
            halla.append((motivo, m.group(0)))
    for m in CORREO.finditer(texto):
        c = m.group(0)
        if not CORREO_GENERICO.search(c) and c.lower() not in correos_autores:
            halla.append(('correo', c))
    rutas = []
    for m in CARPETA_USUARIO.finditer(texto):
        if m.group(1).lower() not in NOMBRES_EJEMPLO and not m.group(1).startswith('.'):
            rutas.append(m.group(0))
            halla.append(('carpeta de un usuario', m.group(0)))
    bajo = texto.lower()
    for motivo, valor in maquina:
        v = valor.lower()
        if motivo == RUTA_MAQUINA:
            for forma in {v, v.replace('\\', '/'), v.replace('/', '\\'), v.replace('\\', '\\\\')}:
                for m in re.finditer(re.escape(forma), bajo):
                    ruta = texto[m.start():m.end()] + re.match(FIN_RUTA, texto[m.end():]).group(0)
                    if not any(ruta in r or r in ruta for r in rutas):
                        rutas.append(ruta)
                        halla.append((motivo, ruta))
        elif re.search(rf'(?<![A-Za-z0-9]){re.escape(v)}(?![A-Za-z0-9])', bajo):
            # El usuario dentro de una ruta ya hallada no se cuenta dos veces.
            if not any(v in r.lower() for r in rutas):
                halla.append((motivo, valor))
    return halla


class Publicado:
    """Si un texto ya salió en la versión publicada `desde`: en su árbol o en el mensaje de uno de sus commits."""

    def __init__(self, repo: Path, desde: str | None):
        self.repo, self.desde, self.vistos = repo, desde, {}

    def __call__(self, texto: str) -> bool:
        if not self.desde or len(texto) < 4:
            return False
        clave = texto.lower()
        if clave not in self.vistos:
            formas = sorted({texto, texto.replace('\\', '/'), texto.replace('/', '\\')})
            patrones = [x for f in formas for x in ('-e', f)]
            arbol = git(self.repo, 'grep', '-q', '-F', '-i', *patrones, self.desde, '--')
            hay = arbol.returncode == 0
            if not hay:
                log = git(self.repo, 'log', '-1', '--format=%H', '-F', '-i',
                          *[f'--grep={f}' for f in formas], self.desde)
                hay = log.returncode == 0 and bool(log.stdout.strip())
            self.vistos[clave] = hay
        return self.vistos[clave]


def revisar(repo: Path, desde: str | None = None, hasta: str = 'develop', remoto: str = 'origin',
            vis: str | None = '?') -> dict:
    """{visibilidad, commits, ya_publicados, hallazgos: [{commit, donde, motivo, texto, nivel}]}; nivel: subido (en
    <remoto>/develop) o nuevo. vis: la visibilidad, si ya se sabe."""
    if vis == '?':
        vis = visibilidad(repo, remoto)
    arriba = f'refs/remotes/{remoto}/develop'
    hay_arriba = git(repo, 'rev-parse', '-q', '--verify', arriba).returncode == 0
    rango = f'{desde}..{hasta}' if desde else hasta
    lista = git(repo, 'rev-list', rango)
    if lista.returncode:
        raise RuntimeError(f'git rev-list {rango}: {lista.stderr.strip()}')
    subidos = set()
    if hay_arriba:
        r = git(repo, 'rev-list', f'{desde}..{arriba}' if desde else arriba)
        subidos = set(r.stdout.split()) if r.returncode == 0 else set()
    textos_ok, archivos_ok = permitidos(repo)
    maquina = identidad_maquina(repo)
    publicado = Publicado(repo, desde)
    propio = git(repo, 'config', 'user.email').stdout.strip().lower()
    hallazgos: list[dict] = []
    vistos: set[tuple] = set()
    ya = 0

    def anotar(commit: str, donde: str, motivo: str, texto: str) -> None:
        nonlocal ya
        bajo = texto.lower()
        if any(p in bajo for p in textos_ok) or any(fnmatch.fnmatch(donde.lower(), p) for p in archivos_ok):
            return
        clave = (donde, motivo, bajo)
        if clave in vistos:
            return
        vistos.add(clave)
        if not motivo.startswith('archivo interno') and publicado(texto):
            ya += 1
            return
        hallazgos.append({'commit': commit[:7], 'donde': donde, 'motivo': motivo, 'texto': texto[:MAX_TEXTO],
                          'nivel': 'subido' if commit in subidos else 'nuevo'})

    # De una vez: cada commit empieza con \x1e y su cabecera (hash, correos y mensaje) acaba en \x1d; después, su parche.
    r = git(repo, 'log', '--reverse', '--no-color', '--no-ext-diff', '--no-renames', '--unified=0', '-p',
            '--format=%x1e%H%x1f%ae%x1f%ce%x1f%B%x1d', rango)
    if r.returncode:
        raise RuntimeError(f'git log {rango}: {r.stderr.strip()}')
    for bloque in r.stdout.split('\x1e')[1:]:
        cabecera, _, parche = bloque.partition('\x1d')
        h, ae, ce, mensaje = (cabecera.split('\x1f', 3) + ['', '', ''])[:4]
        correos = {ae.strip().lower(), ce.strip().lower(), propio} - {''}
        for linea in mensaje.splitlines():
            for motivo, texto in buscar_en(linea, correos, maquina):
                anotar(h, 'mensaje', motivo, texto)
        archivo = '?'
        for linea in parche.splitlines():
            nuevo_archivo = None
            if linea.startswith('+++ b/'):
                nuevo_archivo = linea[6:]
            elif linea.startswith('Binary files ') and ' and b/' in linea:
                nuevo_archivo = linea.rsplit(' and b/', 1)[1].removesuffix(' differ')
            if nuevo_archivo is not None:
                archivo = nuevo_archivo.rstrip('\t').strip('"')
                for motivo, patron in INTERNOS:
                    if patron.search(archivo):
                        anotar(h, archivo, f'archivo interno: {motivo}', archivo)
            elif linea.startswith('+++ '):
                archivo = '?'
            elif linea.startswith('+'):
                for motivo, texto in buscar_en(linea[1:], correos, maquina):
                    anotar(h, archivo, motivo, texto)
    # Los nuevos, primero.
    hallazgos.sort(key=lambda x: x['nivel'] != 'nuevo')
    return {'visibilidad': vis, 'commits': len(lista.stdout.split()), 'ya_publicados': ya, 'hallazgos': hallazgos}


def resumen(r: dict) -> str:
    ya = f' ({r["ya_publicados"]} ya publicados, que no cuentan)' if r['ya_publicados'] else ''
    if not r['hallazgos']:
        return f'Revisados {r["commits"]} commits: nada que no deba salir{ya}.'
    nuevos = sum(x['nivel'] == 'nuevo' for x in r['hallazgos'])
    lineas = [f'Revisados {r["commits"]} commits: {len(r["hallazgos"])} hallazgos, {nuevos} sin subir{ya}.']
    lineas += [f'- {x["commit"]} {x["donde"]}: {x["motivo"]} «{x["texto"]}»'
               + (' (ya subido)' if x['nivel'] == 'subido' else '') for x in r['hallazgos']]
    lineas.append(f'Corrígelo o, si puede publicarse, apúntalo en {PERMITIDOS.as_posix()}.')
    return '\n'.join(lineas)


# ── Antes de subir: la misma decisión para RELEASE y para el push del cierre (decisión 259) ──
MAX_LISTA = 5
PLAZO_PERMISO = 600  # s: repetir la acción en este plazo, con los mismos hallazgos, da el permiso
PERMISOS = 'sf-revision.json'
ACCIONES = ('release', 'subir')  # las únicas que anotan intentos y dan el permiso al repetirse


def ultimo_tag(repo: Path) -> str | None:
    r = git(repo, 'tag', '--list', 'v*', '--sort=-v:refname')
    return next((t for t in r.stdout.split() if re.fullmatch(r'v\d+\.\d+\.\d+', t)), None)


def clave_de(h: dict) -> str:
    return f'{h["commit"]}|{h["donde"]}|{h["motivo"]}|{h["texto"].lower()}'


def archivo_permisos(repo: Path) -> Path:
    """En el directorio de git común (el mismo desde cualquier worktree): nunca se versiona."""
    r = git(repo, 'rev-parse', '--git-common-dir')
    if r.returncode:
        raise RuntimeError(f'git rev-parse --git-common-dir: {r.stderr.strip()}')
    return (repo / r.stdout.strip()).resolve() / PERMISOS


def leer_permisos(ruta: Path) -> dict:
    try:
        datos = json.loads(ruta.read_text(encoding='utf-8'))
        return datos if isinstance(datos, dict) else {}
    except (OSError, ValueError):
        return {}


def orden_lista(repo: Path, remoto: str, desde: str | None) -> str:
    exe = Path(sys.executable).stem or 'python'
    return (f'{exe} -I -X utf8 "{Path(__file__).resolve()}" --repo "{repo.resolve()}" --remoto {remoto}'
            + (f' --desde {desde}' if desde else ''))


def lista_corta(hs: list) -> str:
    texto = '; '.join(f'{x["commit"]} {x["donde"]}: {x["motivo"]} «{x["texto"]}»'
                      + (' (ya subido)' if x['nivel'] == 'subido' else '') for x in hs[:MAX_LISTA])
    return texto + (f' y {len(hs) - MAX_LISTA} más' if len(hs) > MAX_LISTA else '')


def antes_de_subir(repo: Path, remoto: str = 'origin', desde: str | None = None, hasta: str = 'develop',
                   repetir: str = 'repite la acción', solo_publico: bool = False, ahora: float | None = None,
                   accion: str | None = None) -> dict:
    """{accion: seguir|permiso|bloquear, mensaje, hallazgos, visibilidad}. Sin desde, el último tag. Con
    solo_publico, si el remoto no es público, sigue sin revisar. `accion` (release o subir) es la acción real que
    sube: solo ella anota el intento, y repetirla, la misma, en el plazo y con los mismos hallazgos da el permiso. Sin
    ella, solo se mira: no se escribe nada. Lanza RuntimeError si no puede revisar."""
    if accion is not None and accion not in ACCIONES:
        raise RuntimeError(f'acción desconocida: {accion} (release o subir)')
    import time
    ahora = time.time() if ahora is None else ahora
    vis = visibilidad(repo, remoto)
    publico = vis not in ('PRIVATE', 'INTERNAL', 'LOCAL')
    if solo_publico and not publico:
        return {'accion': 'seguir', 'mensaje': '', 'hallazgos': [], 'visibilidad': vis}
    desde = desde or ultimo_tag(repo)
    r = revisar(repo, desde, hasta, remoto, vis)
    ruta = archivo_permisos(repo)
    permisos = leer_permisos(ruta)
    aceptados = set(permisos.get('aceptados') or [])
    quedan = [h for h in r['hallazgos'] if clave_de(h) not in aceptados]
    base = {'hallazgos': quedan, 'visibilidad': vis}
    if not quedan:
        return {'accion': 'seguir', 'mensaje': '', **base}
    nuevos = [h for h in quedan if h['nivel'] == 'nuevo']
    orden = orden_lista(repo, remoto, desde)
    if publico and nuevos:
        subidos = len(quedan) - len(nuevos)
        return {'accion': 'bloquear', **base, 'mensaje': (
            f'el repositorio es público y hay {len(nuevos)} cosas sin subir que quizá no deban publicarse'
            + (f' (y {subidos} ya subidas)' if subidos else '') + f': {lista_corta(quedan)}. '
            f'Corrígelo o, si puede salir, apúntalo en {PERMITIDOS.as_posix()}. La lista entera: {orden}')}
    claves = sorted(clave_de(h) for h in quedan)
    por_que = 'ya subidas' if publico else 'el repositorio no es público'
    if accion is None:
        return {'accion': 'permiso', **base, 'mensaje': (
            f'hay {len(quedan)} cosas que quizá no deban publicarse ({por_que}): {lista_corta(quedan)}. '
            f'Solo se ha mirado: no se anota ni se acepta nada; el permiso lo da repetir RELEASE o la subida de '
            f'develop. La lista entera: {orden}')}
    if (permisos.get('pendientes') == claves and permisos.get('accion') == accion
            and ahora <= float(permisos.get('hasta') or 0)):
        permisos.update(aceptados=sorted(aceptados | set(claves)), pendientes=[], hasta=0, accion=None)
        ruta.write_text(json.dumps(permisos, ensure_ascii=False, indent=1), encoding='utf-8')
        return {'accion': 'seguir', **base, 'mensaje': f'aceptadas {len(claves)} cosas de la revisión'}
    permisos.update(pendientes=claves, hasta=ahora + PLAZO_PERMISO, accion=accion)
    ruta.write_text(json.dumps(permisos, ensure_ascii=False, indent=1), encoding='utf-8')
    return {'accion': 'permiso', **base, 'mensaje': (
        f'hay {len(quedan)} cosas que quizá no deban publicarse ({por_que}): {lista_corta(quedan)}. '
        f'Para seguir igualmente, {repetir} en los próximos {PLAZO_PERMISO // 60} minutos; si no, corrígelo o '
        f'apúntalo en {PERMITIDOS.as_posix()}. La lista entera: {orden}')}


def main(argv: list | None = None) -> int:
    for flujo in (sys.stdout, sys.stderr):
        if hasattr(flujo, 'reconfigure'):
            flujo.reconfigure(encoding='utf-8')
    p = argparse.ArgumentParser(prog='revision_publica.py', description=__doc__.split('\n\n')[0])
    p.add_argument('--repo', type=Path, default=Path.cwd())
    p.add_argument('--remoto', default='origin')
    p.add_argument('--desde', help='el último tag publicado; sin él, todos los commits')
    p.add_argument('--hasta', default='develop')
    p.add_argument('--decidir', action='store_true', help='qué hacer antes de subir: seguir, permiso o bloquear')
    p.add_argument('--accion', choices=ACCIONES,
                   help='con --decidir: la acción real que sube (la usan RELEASE y cola.py); sin ella, solo mira')
    p.add_argument('--repetir', default='repite la acción', help='con --decidir: cómo se da el permiso')
    p.add_argument('--solo-publico', action='store_true', help='con --decidir: sin revisar si el remoto no es público')
    p.add_argument('--json', action='store_true')
    a = p.parse_args(argv)
    if a.decidir:
        try:
            d = antes_de_subir(a.repo, a.remoto, a.desde, a.hasta, a.repetir, a.solo_publico,
                               accion=a.accion)
        except RuntimeError as err:
            d = {'ok': False, 'mensaje': str(err)}
        else:
            d = {'ok': True, **d}
        print(json.dumps(d, ensure_ascii=False) if a.json else (d['mensaje'] or d.get('accion', '')))
        return 1 if not d['ok'] else 0 if d['accion'] == 'seguir' else 3
    try:
        r = revisar(a.repo, a.desde, a.hasta, a.remoto)
    except RuntimeError as err:
        if a.json:
            print(json.dumps({'ok': False, 'mensaje': str(err)}, ensure_ascii=False))
        else:
            print(err, file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps({'ok': True, 'mensaje': resumen(r), **r}, ensure_ascii=False))
    else:
        print(resumen(r))
    return 3 if r['hallazgos'] else 0


if __name__ == '__main__':
    sys.exit(main())
