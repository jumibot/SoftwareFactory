"""La versión del plugin sf: si está al día y, si no, ponerlo al día (tarea 333).

La usan sf:comprobar_instalacion y, antes de cualquier pregunta, sf:incorporar_proyecto_a_sf: incorporar con un plugin
viejo deja el proyecto con reglas y herramientas viejas. Hace con comandos lo mismo que el botón ACTUALIZAR/REFRESCAR
del panel (hooks/cola.ts), que en una carpeta sin SF no sale: lo que se puede hacer con un comando no se infiere.

Compara tres versiones de sf@softwarefactory:
  - la que corre: la del plugin.json de la carpeta de esta herramienta (la del plugin cargado en la sesión; desde la
    copia de trabajo de la SF, ninguna);
  - la instalada: la de installed_plugins.json, en el scope de usuario y en los local o project de la carpeta;
  - la publicada: el tag vX.Y.Z más alto del repositorio del catálogo softwarefactory (git ls-remote --tags).

Uso (desde la carpeta del proyecto):
  python -I -X utf8 <plugin>/tools/plugin_sf.py ver [--json]
      Las tres versiones y el estado:
        al_dia       nada que hacer;
        actualizar   la publicada es más nueva que la instalada en algún scope: `actualizar`, con el OK del usuario
                     (cambia la instalación de todos los proyectos), y después reiniciar Claude Code;
        refrescar    lo instalado ya es más nuevo que lo que corre: /reload-plugins (lo escribe el usuario);
        sin_instalar sf@softwarefactory no está instalado para esta carpeta (corre otra copia);
      Desde la copia de trabajo de la SF (el modo prueba), la que corre no se compara: el estado es el de la instalada
      frente a la publicada, y el mensaje lo dice («corre la copia de trabajo»).
        desconocido  no se sabe la publicada (sin red, sin catálogo): se sigue y se dice.
  … actualizar [--json]
      Refresca el catálogo, actualiza sf en cada scope atrasado e instala las dependencias de la versión nueva que
      falten, una orden por dependencia. Para en el primer fallo. Después hay que reiniciar Claude Code: el plugin
      nuevo solo se carga en una sesión nueva.

Sale con 0 si va bien (con `ver`, aunque haya que actualizar: lo dice el estado), con 1 si una orden falla y con 2 si
no se puede leer la instalación. Con --json, una línea JSON con ok, estado, mensaje y las versiones.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PLUGIN = 'sf@softwarefactory'
CATALOGO = 'softwarefactory'
SEMVER = re.compile(r'^\d+\.\d+\.\d+$')
TAG = re.compile(r'\trefs/tags/v(\d+\.\d+\.\d+)$')
RAIZ_PLUGIN = Path(__file__).resolve().parents[1]


def carpeta_claude() -> Path:
    config = os.environ.get('CLAUDE_CONFIG_DIR', '').strip()
    return Path(config) if config else Path.home() / '.claude'


def clave(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in v.split('.'))


def mas_alta(versiones) -> str | None:
    vs = [v for v in versiones if isinstance(v, str) and SEMVER.match(v)]
    return max(vs, key=clave) if vs else None


def normal(ruta: str) -> str:
    r = ruta.replace('\\', '/').rstrip('/')
    return r.lower() if re.match(r'^[a-zA-Z]:', r) else r


def leer_json(ruta: Path) -> dict:
    datos = json.loads(ruta.read_text(encoding='utf-8'))
    return datos if isinstance(datos, dict) else {}


def ejecutar(argv: list[str], cwd: str) -> tuple[int, str]:
    """Lanza una orden y da su código y su salida (o el primer error). Se cambia en las pruebas."""
    try:
        r = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace',
                           timeout=300)
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)
    return r.returncode, r.stdout if r.returncode == 0 else (r.stderr.strip() or r.stdout.strip())


def desde_copia() -> bool:
    """Corre la copia de trabajo de la SF (el plugin, dos niveles por debajo de la raíz de un repositorio), como el
    mod: su versión no se compara con lo instalado."""
    return (RAIZ_PLUGIN.parents[1] / '.git').exists()


def version_corre() -> str | None:
    if desde_copia():
        return None
    try:
        v = leer_json(RAIZ_PLUGIN / '.claude-plugin' / 'plugin.json').get('version')
    except (OSError, ValueError):
        return None
    return v if isinstance(v, str) and SEMVER.match(v) else None


def de_la_carpeta(x: dict, raiz: str) -> bool:
    return x.get('scope') == 'user' or (x.get('scope') in ('local', 'project') and isinstance(x.get('projectPath'), str)
                                        and normal(x['projectPath']) == normal(raiz))


def instaladas(raiz: str) -> dict:
    """Las entradas de installed_plugins.json, por plugin. Lanza OSError/ValueError si no se puede leer."""
    p = leer_json(carpeta_claude() / 'plugins' / 'installed_plugins.json').get('plugins')
    return p if isinstance(p, dict) else {}


def version_publicada(raiz: str) -> str | None:
    try:
        s = leer_json(carpeta_claude() / 'plugins' / 'known_marketplaces.json').get(CATALOGO, {}).get('source', {})
    except (OSError, ValueError, AttributeError):
        return None
    if s.get('source') == 'github' and isinstance(s.get('repo'), str):
        url = f'https://github.com/{s["repo"]}.git'
    elif s.get('source') == 'git' and isinstance(s.get('url'), str):
        url = s['url']
    else:
        return None
    codigo, salida = ejecutar(['git', 'ls-remote', '--tags', url], raiz)
    if codigo != 0:
        return None
    return mas_alta(m.group(1) for m in (TAG.search(l.strip()) for l in salida.splitlines()) if m)


def ver(raiz: str) -> dict:
    sf = [x for x in instaladas(raiz).get(PLUGIN, []) if isinstance(x, dict) and de_la_carpeta(x, raiz)]
    corre = version_corre()
    instalada = mas_alta(x.get('version') for x in sf)
    publicada = version_publicada(raiz)
    r = {'corre': corre, 'instalada': instalada, 'publicada': publicada, 'scopes': {str(x.get('scope')): x.get('version') for x in sf},
         'atrasados': []}
    if not sf:
        r.update(estado='sin_instalar', mensaje=f'{PLUGIN} no está instalado para esta carpeta: corre la {corre or "?"}.')
        return r
    if publicada:
        r['atrasados'] = sorted({str(x.get('scope')) for x in sf if isinstance(x.get('version'), str)
                                 and SEMVER.match(x['version']) and clave(publicada) > clave(x['version'])})
    if r['atrasados']:
        r.update(estado='actualizar', mensaje=f'Publicada la {publicada}; instalada la {instalada}'
                 f' ({", ".join(r["atrasados"])}): hay que actualizar y reiniciar Claude Code.')
    elif corre and instalada and clave(instalada) > clave(corre):
        r.update(estado='refrescar', mensaje=f'Instalada la {instalada}, pero esta sesión corre la {corre}: /reload-plugins.')
    elif not publicada:
        r.update(estado='desconocido', mensaje=f'No se sabe la publicada (sin red o sin catálogo); corre la {corre or "?"}.')
    else:
        r.update(estado='al_dia', mensaje=f'Al día: la {publicada}.')
    if desde_copia():
        r['mensaje'] += ' Corre la copia de trabajo de la SF (modo prueba): su versión no se compara.'
    return r


def id_dependencia(d) -> str | None:
    if isinstance(d, str):
        return d if '@' in d else f'{d}@{CATALOGO}'
    if isinstance(d, dict) and isinstance(d.get('name'), str):
        return f'{d["name"]}@{d["marketplace"] if isinstance(d.get("marketplace"), str) else CATALOGO}'
    return None


def dependencias_que_faltan(raiz: str, scopes: list[str]) -> list[tuple[str, str]]:
    todas = instaladas(raiz)
    faltan: list[tuple[str, str]] = []
    for x in todas.get(PLUGIN, []):
        if not (isinstance(x, dict) and de_la_carpeta(x, raiz) and x.get('scope') in scopes):
            continue
        carpeta = Path(x['installPath']) if isinstance(x.get('installPath'), str) else \
            carpeta_claude() / 'plugins' / 'cache' / CATALOGO / 'sf' / str(x.get('version'))
        try:
            deps = leer_json(carpeta / '.claude-plugin' / 'plugin.json').get('dependencies') or []
        except (OSError, ValueError):
            continue
        for i in filter(None, map(id_dependencia, deps)):
            hay = any(y.get('scope') == 'user' or (y.get('scope') == x['scope'] and de_la_carpeta(y, raiz))
                      for y in todas.get(i, []) if isinstance(y, dict))
            if not hay and (i, x['scope']) not in faltan:
                faltan.append((i, str(x['scope'])))
    return [(i, s) for i, s in faltan if s == 'user' or (i, 'user') not in faltan]


def actualizar(raiz: str) -> dict:
    r = ver(raiz)
    if r['estado'] != 'actualizar':
        return {**r, 'ok': r['estado'] != 'sin_instalar', 'hecho': []}
    hecho: list[str] = []

    def orden(argv: list[str]) -> str | None:
        codigo, salida = ejecutar(argv, raiz)
        if codigo != 0:
            return f'falló «{" ".join(argv)}»: {(salida.splitlines() or ["sin salida"])[0]}'
        hecho.append(' '.join(argv))
        return None

    fallo = orden(['claude', 'plugin', 'marketplace', 'update', CATALOGO])
    for scope in r['atrasados']:
        fallo = fallo or orden(['claude', 'plugin', 'update', PLUGIN, '--scope', scope])
    if not fallo:
        for i, scope in dependencias_que_faltan(raiz, r['atrasados']):
            fallo = fallo or orden(['claude', 'plugin', 'install', i, '--scope', scope])
    if fallo:
        return {**r, 'ok': False, 'hecho': hecho, 'mensaje': f'No se pudo actualizar: {fallo}. Sin sus dependencias, sf no carga.'}
    return {**r, 'ok': True, 'estado': 'reiniciar', 'hecho': hecho,
            'mensaje': f'sf actualizado a la {r["publicada"]}: reinicia Claude Code (/exit y vuelve a abrirlo) para cargarlo.'}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog='plugin_sf.py', description='Si el plugin sf está al día y, si no, actualizarlo.')
    ap.add_argument('orden', choices=['ver', 'actualizar'])
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--raiz', default='.')
    args = ap.parse_args(argv)
    raiz = str(Path(args.raiz).resolve())
    try:
        r = ver(raiz) if args.orden == 'ver' else actualizar(raiz)
    except (OSError, ValueError) as e:
        r = {'ok': False, 'estado': 'error', 'mensaje': f'no se puede leer la instalación de los plugins ({e}).'}
        print(json.dumps(r, ensure_ascii=False) if args.json else f'plugin_sf.py: {r["mensaje"]}',
              file=sys.stdout if args.json else sys.stderr)
        return 2
    r.setdefault('ok', True)
    if args.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        print(r['mensaje'])
        for h in r.get('hecho', []):
            print(f'  hecho: {h}')
    return 0 if r['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
