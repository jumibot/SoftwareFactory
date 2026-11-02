"""La configuración de un proyecto con la SF (.sf/proyecto.json): verla, comprobarla y detectar sus convenciones.

Solo lee: no escribe la configuración ni toca el repositorio. Cambiarla se le pide a Claude, con menús y con el OK del
propietario («La configuración se cambia pidiéndoselo a Claude, con menús», 228; skill sf:configurar_proyecto y
/sf_config), y la incorporación la escribe al incorporar y al poner al día (sf:incorporar_proyecto_a_sf). Las dos usan
esta herramienta para lo mismo: lo que se ve y se detecta con comandos no se infiere (metodología, 1). La lectura de
la configuración, con sus valores por defecto, es la de cola.py (leer_configuracion), la misma que la del mod.

Uso:
  python -I -X utf8 configuracion.py ver [--repo RUTA] [--json]
      La configuración del proyecto: lo que dice el archivo, lo que vale cada campo (con los valores por defecto donde
      falta) y los problemas: campos obligatorios que faltan o no valen, valores que no se entienden, el kanban en la
      forma antigua, un remoto que no existe o no apunta a GitHub (230), una rama de publicación o una develop que no
      existen, un manifiesto que no está o no tiene versión, interruptores que no se conocen. Sale con 0 sin
      problemas, con 1 si los hay y con 2 si el proyecto no está incorporado (sin .sf/proyecto.json) o no es un
      repositorio git.
  python -I -X utf8 configuracion.py detectar [--repo RUTA] [--json]
      Lo que se detecta para proponer valores en los menús: los remotos (y cuáles son de GitHub y a cuál siguen develop
      y la rama de publicación), las ramas main, master y develop (locales y en los remotos), los manifiestos con
      versión (raíz y un nivel por debajo), la forma de los últimos 50 commits y su línea de coautoría más usada, y los
      colores que usan los proyectos de las carpetas vecinas. El idioma no se detecta con comandos: lo dice Claude leyendo el README, el CLAUDE.md y los
      commits.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location('cola_sf', Path(__file__).resolve().parent / 'cola.py')
cola = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cola)

PROYECTO = Path('.sf') / 'proyecto.json'
# Los colores de sesión de un proyecto; purple es el de la SF (constantes.ts, COLORES y COLOR_SF).
COLORES = ('red', 'blue', 'green', 'yellow', 'orange', 'pink', 'cyan')
COLOR_SF = 'purple'
LARGO_DESCRIPCION = 120
# Los interruptores de «automatizaciones» (decisión 171), encendidos salvo false, con lo que apagan.
AUTOMATIZACIONES = {
    'orquestacion': 'el mod entrega sf:orquestacion al empezar, tras /clear y tras compactar (si no, la carga el principal)',
    'avisos_subagentes': 'avisos de tareas en curso sin subagente y de subagentes terminados sin recoger',
    'encargo_subagente': 'cola.py encargo N escribe la parte fija del encargo de un subagente',
    'dependencias_al_actualizar': 'al actualizar el plugin desde el panel, se instalan sus dependencias',
}
# Un título conventional: tipo(ámbito)!: con un tipo de los habituales.
CONVENTIONAL = re.compile(r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]*\))?!?: ')
NUMERO_AL_FINAL = re.compile(r'\(\d+\)\s*$')
MANIFIESTOS = ('package.json', 'pyproject.toml', '.claude-plugin/plugin.json')
SIN_MIRAR = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', '.sf', 'sf', 'dist', 'build'}


def git(repo: Path, *args: str) -> tuple[int, str]:
    r = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, encoding='utf-8',
                       errors='replace')
    return r.returncode, r.stdout.strip()


def es_repositorio(repo: Path) -> bool:
    return git(repo, 'rev-parse', '--git-dir')[0] == 0


def remotos(repo: Path) -> dict[str, str]:
    """Cada remoto con su url (la de fetch)."""
    salida = {}
    for nombre in git(repo, 'remote')[1].splitlines():
        nombre = nombre.strip()
        if nombre:
            salida[nombre] = git(repo, 'remote', 'get-url', nombre)[1]
    return salida


def es_de_github(url: str) -> bool:
    """La misma regla que esDeGithub del mod: https://github.com/…, git@github.com:…, ssh://git@github.com/…"""
    return bool(re.search(r'(^|[@/.])github\.com[:/]', url, re.I))


def ramas(repo: Path) -> tuple[set[str], dict[str, set[str]]]:
    """Las ramas locales y, por remoto, las suyas."""
    locales = set(git(repo, 'for-each-ref', '--format=%(refname:short)', 'refs/heads')[1].split())
    en_remotos: dict[str, set[str]] = {}
    for ref in git(repo, 'for-each-ref', '--format=%(refname)', 'refs/remotes')[1].split():
        partes = ref.split('/', 3)
        if len(partes) == 4 and partes[3] != 'HEAD':
            en_remotos.setdefault(partes[2], set()).add(partes[3])
    return locales, en_remotos


def version_de_manifiesto(ruta: Path) -> str | None:
    """La versión de un manifiesto soportado (.json con clave version, pyproject.toml con version = "…"), o None."""
    try:
        texto = ruta.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return None
    if cola.formato_manifiesto(ruta.name) == 'json':
        try:
            v = json.loads(texto).get('version')
        except (ValueError, AttributeError):
            return None
        return v if isinstance(v, str) and v.strip() else None
    m = re.search(r'^\s*version\s*=\s*["\']([^"\']+)["\']', texto, re.M)
    return m.group(1) if m else None


def manifiestos(repo: Path) -> list[dict]:
    """Los manifiestos con versión de la raíz y de un nivel por debajo, por ruta relativa."""
    carpetas = [repo] + sorted(p for p in repo.iterdir() if p.is_dir() and p.name not in SIN_MIRAR
                               and not p.name.startswith('.'))
    vistos = []
    for carpeta in carpetas:
        for nombre in MANIFIESTOS:
            ruta = carpeta / nombre
            if ruta.is_file():
                v = version_de_manifiesto(ruta)
                if v:
                    vistos.append({'ruta': ruta.relative_to(repo).as_posix(), 'version': v})
    return vistos


def commits(repo: Path, rama: str | None) -> dict:
    """La forma de los últimos 50 títulos (sin merges): cuántos son conventional y cuántos acaban en «(N)»."""
    args = ['log', '-50', '--no-merges', '--format=%s'] + ([rama] if rama else [])
    codigo, salida = git(repo, *args)
    titulos = salida.splitlines() if codigo == 0 else []
    conventional = sum(1 for t in titulos if CONVENTIONAL.match(t))
    con_numero = sum(1 for t in titulos if NUMERO_AL_FINAL.search(t))
    if not titulos:
        propuesto = 'libre'
    elif conventional * 2 > len(titulos):
        propuesto = 'conventional'
    else:
        propuesto = 'libre'
    return {'mirados': len(titulos), 'conventional': conventional, 'con_numero_al_final': con_numero,
            'ejemplos': titulos[:5], 'propuesto': propuesto}


COAUTORIA = re.compile(r'^co-authored-by:\s*(.+?)\s*$', re.I | re.M)


def coautoria(repo: Path, rama: str | None) -> dict:
    """Las líneas de coautoría de los últimos 50 commits (sin merges): cuántos la llevan y la más usada, que es la que
    se propone para `coautor` («La firma del commit de cierre es configurable», 238)."""
    args = ['log', '-50', '--no-merges', '--format=%B%x00'] + ([rama] if rama else [])
    codigo, salida = git(repo, *args)
    cuerpos = [x for x in salida.split('\x00') if x.strip()] if codigo == 0 else []
    cuenta: dict[str, int] = {}
    for cuerpo in cuerpos:
        m = COAUTORIA.search(cuerpo)
        if m:
            linea = f'Co-Authored-By: {m.group(1)}'
            cuenta[linea] = cuenta.get(linea, 0) + 1
    mas = max(cuenta, key=lambda k: cuenta[k]) if cuenta else None
    return {'mirados': len(cuerpos), 'con_linea': sum(cuenta.values()), 'mas_usada': mas}


def colores_vecinos(repo: Path) -> dict:
    """Los colores de los proyectos de las carpetas vecinas (solo lectura) y los que quedan libres."""
    usados: dict[str, list[str]] = {}
    try:
        vecinos = [p for p in repo.resolve().parent.iterdir() if p.is_dir() and p.resolve() != repo.resolve()]
    except OSError:
        vecinos = []
    for carpeta in sorted(vecinos):
        try:
            d = json.loads((carpeta / PROYECTO).read_text(encoding='utf-8'))
        except (OSError, ValueError):
            continue
        if isinstance(d, dict) and isinstance(d.get('color'), str):
            usados.setdefault(d['color'], []).append(d.get('proyecto') if isinstance(d.get('proyecto'), str) else carpeta.name)
    return {'usados': usados, 'libres': [c for c in COLORES if c not in usados]}


def leer_archivo(repo: Path) -> tuple[dict | None, str | None]:
    """El contenido de .sf/proyecto.json, o None y el motivo."""
    ruta = repo / PROYECTO
    if not ruta.is_file():
        return None, 'no hay .sf/proyecto.json: el proyecto no está incorporado a la SF'
    try:
        datos = json.loads(ruta.read_text(encoding='utf-8'))
    except (OSError, ValueError) as e:
        return None, f'.sf/proyecto.json no es un JSON válido: {e}'
    if not isinstance(datos, dict):
        return None, '.sf/proyecto.json no es un objeto JSON'
    return datos, None


def problemas(repo: Path, datos: dict, efectiva: dict) -> list[str]:
    """Lo que no vale de la configuración, en frases cortas."""
    p = []
    if not (isinstance(datos.get('sf'), str) and re.fullmatch(r'\d+\.\d+\.\d+', datos['sf'].strip())):
        p.append('sf: falta o no es una versión X.Y.Z (lo escribe «poner al día»)')
    if not (isinstance(datos.get('proyecto'), str) and datos['proyecto'].strip()):
        p.append('proyecto: falta el nombre')
    d = datos.get('descripcion')
    if not (isinstance(d, str) and d.strip()):
        p.append('descripcion: falta')
    elif len(d.strip()) > LARGO_DESCRIPCION:
        p.append(f'descripcion: {len(d.strip())} caracteres, más de {LARGO_DESCRIPCION}')
    color = datos.get('color')
    if color == COLOR_SF:
        p.append('color: purple es el de la SF')
    elif color not in COLORES:
        p.append(f'color: falta o no es uno de {", ".join(COLORES)}')
    for campo in efectiva['desconocidos']:
        p.append(f'{campo}: no se entiende {json.dumps(datos.get(campo), ensure_ascii=False)}; vale lo de por defecto')
    if isinstance(datos.get('kanban'), str):
        p.append('kanban: en la forma antigua (cadena); va en bloque { "proveedor": "jkanban", "proyecto": "…" }')
    if es_repositorio(repo):
        rem = remotos(repo)
        url = rem.get(efectiva['remoto'])
        if url is None:
            p.append(f'remoto: no existe el remoto {efectiva["remoto"]}')
        elif not es_de_github(url):
            p.append(f'remoto: {efectiva["remoto"]} no apunta a GitHub ({url}); la SF solo trabaja con GitHub')
        locales, en_remotos = ramas(repo)
        for rama, campo in ((efectiva['rama_main'], 'rama_main'), ('develop', 'develop')):
            if rama not in locales:
                donde = [r for r, rs in en_remotos.items() if rama in rs]
                p.append(f'{campo}: la rama {rama} no existe en local' + (f' (sí en {", ".join(donde)})' if donde else ''))
    for ruta in efectiva['manifiesto']:
        archivo = repo / ruta
        if not archivo.is_file():
            p.append(f'manifiesto: no existe {ruta}')
        elif version_de_manifiesto(archivo) is None:
            p.append(f'manifiesto: {ruta} no tiene versión')
    auto = datos.get('automatizaciones')
    if auto is not None:
        if not isinstance(auto, dict):
            p.append('automatizaciones: no es un bloque')
        else:
            for clave, valor in auto.items():
                if clave not in AUTOMATIZACIONES:
                    p.append(f'automatizaciones: no se conoce el interruptor {clave}')
                elif not isinstance(valor, bool):
                    p.append(f'automatizaciones.{clave}: vale {json.dumps(valor)}, no true ni false')
    return p


CAMPOS = ('sf', 'proyecto', 'descripcion', 'color', 'metodologia', 'kanban', 'idioma', 'commits', 'remoto',
          'rama_main', 'manifiesto', 'coautor')


def o_ver(repo: Path) -> tuple[int, dict]:
    if not es_repositorio(repo):
        return 2, {'error': f'{repo} no es un repositorio git'}
    datos, motivo = leer_archivo(repo)
    if datos is None:
        return 2, {'error': motivo}
    efectiva = cola.leer_configuracion(datos, es_sf=(repo / cola.MARCA_SF).is_file())
    vale = {
        'sf': datos.get('sf'), 'proyecto': datos.get('proyecto'), 'descripcion': datos.get('descripcion'),
        'color': datos.get('color'), 'metodologia': efectiva['metodologia'], 'kanban': efectiva['kanban'],
        'idioma': efectiva['idioma'], 'commits': efectiva['commits'], 'remoto': efectiva['remoto'],
        'rama_main': efectiva['rama_main'], 'manifiesto': efectiva['manifiesto'] or None,
        'coautor': efectiva['coautor'],
        'automatizaciones': {k: efectiva['automatizaciones'].get(k) is not False for k in AUTOMATIZACIONES},
    }
    por_defecto = [c for c in CAMPOS if c not in datos and c not in ('sf', 'proyecto', 'descripcion', 'color')]
    lista = problemas(repo, datos, efectiva)
    return (1 if lista else 0), {'archivo': datos, 'vale': vale, 'por_defecto': por_defecto, 'problemas': lista}


def o_detectar(repo: Path) -> tuple[int, dict]:
    if not es_repositorio(repo):
        return 2, {'error': f'{repo} no es un repositorio git'}
    rem = remotos(repo)
    locales, en_remotos = ramas(repo)
    datos, _ = leer_archivo(repo)
    rama_main = cola.leer_configuracion(datos).get('rama_main', 'main')
    siguen = {}
    for rama in sorted({'develop', rama_main, 'main', 'master'} & locales):
        codigo, r = git(repo, 'config', f'branch.{rama}.remote')
        if codigo == 0 and r:
            siguen[rama] = r
    nombres = sorted({'main', 'master', 'develop', rama_main})
    return 0, {
        'carpeta': repo.resolve().name,
        'remotos': [{'nombre': n, 'url': u, 'github': es_de_github(u)} for n, u in rem.items()],
        'siguen': siguen,
        'ramas': {n: {'local': n in locales, 'remotos': sorted(r for r, rs in en_remotos.items() if n in rs)}
                  for n in nombres},
        'manifiestos': manifiestos(repo),
        'commits': commits(repo, 'develop' if 'develop' in locales else None),
        'coautoria': coautoria(repo, 'develop' if 'develop' in locales else None),
        'colores': colores_vecinos(repo),
    }


def texto_ver(r: dict) -> str:
    if 'error' in r:
        return r['error']
    lineas = ['Configuración (.sf/proyecto.json):']
    for campo, valor in r['vale'].items():
        if campo == 'automatizaciones':
            apagadas = [k for k, v in valor.items() if not v]
            valor = 'todas encendidas' if not apagadas else 'apagadas: ' + ', '.join(apagadas)
        elif not isinstance(valor, str):
            valor = json.dumps(valor, ensure_ascii=False)
        lineas.append(f'  {campo}: {valor}' + ('  (por defecto: no está en el archivo)' if campo in r['por_defecto'] else ''))
    lineas.append('Problemas: ' + ('ninguno' if not r['problemas'] else ''))
    lineas += [f'  - {p}' for p in r['problemas']]
    return '\n'.join(lineas)


def texto_detectar(r: dict) -> str:
    if 'error' in r:
        return r['error']
    lineas = [f'Carpeta: {r["carpeta"]}', 'Remotos:']
    lineas += [f'  {x["nombre"]}: {x["url"]}' + ('' if x['github'] else '  (no es de GitHub)') for x in r['remotos']] or ['  ninguno']
    if r['siguen']:
        lineas.append('Siguen a: ' + ', '.join(f'{k} → {v}' for k, v in r['siguen'].items()))
    lineas.append('Ramas:')
    for n, v in r['ramas'].items():
        donde = (['local'] if v['local'] else []) + v['remotos']
        lineas.append(f'  {n}: {", ".join(donde) if donde else "no existe"}')
    lineas.append('Manifiestos con versión: ' + (', '.join(f'{m["ruta"]} ({m["version"]})' for m in r['manifiestos']) or 'ninguno'))
    c = r['commits']
    lineas.append(f'Commits: {c["conventional"]} conventional y {c["con_numero_al_final"]} con «(N)» al final, de los '
                  f'últimos {c["mirados"]}; propuesto: {c["propuesto"]}')
    lineas += [f'  «{t}»' for t in c['ejemplos']]
    co = r['coautoria']
    lineas.append(f'Coautoría: {co["con_linea"]} de los últimos {co["mirados"]} con línea Co-Authored-By'
                  + (f'; la más usada: «{co["mas_usada"]}»' if co['mas_usada'] else ''))
    usados = r['colores']['usados']
    lineas.append('Colores de los vecinos: ' + (', '.join(f'{k} ({", ".join(v)})' for k, v in usados.items()) or 'ninguno'))
    lineas.append('Colores libres: ' + (', '.join(r['colores']['libres']) or 'ninguno'))
    return '\n'.join(lineas)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog='configuracion.py', description='Ver, comprobar y detectar la configuración de un proyecto con la SF (solo lee).')
    sub = p.add_subparsers(dest='orden', required=True)
    for nombre, ayuda in (('ver', 'la configuración y sus problemas'), ('detectar', 'lo que se detecta para los menús')):
        s = sub.add_parser(nombre, help=ayuda)
        s.add_argument('--repo', default='.', help='carpeta del proyecto (por defecto, la actual)')
        s.add_argument('--json', action='store_true', help='la salida en JSON')
    a = p.parse_args(argv)
    repo = Path(a.repo)
    codigo, r = (o_ver if a.orden == 'ver' else o_detectar)(repo)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(texto_ver(r) if a.orden == 'ver' else texto_detectar(r))
    return codigo


if __name__ == '__main__':
    sys.exit(main())
