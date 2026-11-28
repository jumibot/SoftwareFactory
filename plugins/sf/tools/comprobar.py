"""Comprobar un proyecto con una sola orden: elige los tests que toca lo cambiado, los lanza a la vez y resume.

Sirve a cualquier proyecto (decisión 430, informe «Gastar menos tokens al probar»): el subagente la lanza una vez al
acabar cada vuelta, con el plazo de una orden, en lugar de lanzar a mano cada test o comprobación. Hace dos rondas:

1. Seleccionar, de forma determinista. Junta las comprobaciones del proyecto (de las fuentes, ver abajo), compara los
   archivos cambiados (los que difieren de develop en la rama, más los que no tienen commit) con lo que cubre cada
   una y decide cuál corre y cuál se salta, con su porqué. Una comprobación que no dice qué cubre corre siempre; un
   archivo cambiado que no cubre ninguna se avisa. Después, la caché: se salta la que ya pasó con el mismo hash de
   sus archivos y de su orden.
2. Ejecutar a la vez lo seleccionado, cada parte en su proceso: con el reparto del runner cuando lo tiene (vitest,
   jest, Playwright, cargo y go ya reparten en workers) y en trozos cuando no (pytest: un proceso por archivo de
   tests, y los archivos lentos partidos en varios). Devuelve una línea por grupo («Comprobado: …», «Falla: …»,
   «Sin lanzar: …») y, de lo que falla, el nombre del test y la primera línea de su error. La salida entera de cada
   parte va a un log aparte, que el resumen nombra.

Las fuentes de comprobaciones son enchufables (registrar_fuente): cada una da una lista de Comprobacion, y si dos dan
la misma (mismo nombre), manda la de prioridad más alta (número más bajo). Hoy solo está la detección por el stack
(prioridad 30). Lo declarado por el proyecto en .sf/comprobar.json (10) y lo visto lanzar en
.sf/comprobaciones-vistas.json (20) son de otra tarea y entran aquí como otras dos fuentes; para registrar lo lanzado
está AL_TERMINAR, una lista de funciones que reciben el contexto y los resultados al acabar.

Lo que detecta, y cómo (con la versión del runner con la que se verificó cada opción en un proyecto de prueba):
- Python: archivos test_*.py o *_test.py. Con pytest si el intérprete del proyecto lo tiene (-q -rfE --tb=short
  --color=no -p no:cacheprovider, verificadas con pytest 8.3), si no con unittest. Lo que cubre cada archivo sale de lo
  que nombra: sus importaciones, las rutas que construye desde __file__ (y los glob sobre ellas), los nombres de
  archivo que escribe, y lo mismo, de forma transitiva, en los módulos del proyecto que usa. Si no nombra ningún
  archivo del proyecto, no dice qué cubre y corre siempre. ruff check . --output-format concise (verificada con ruff
  0.8), si el proyecto lo configura y está instalado.
- Node (package.json): el script test, con vitest (run --changed REF, verificada con vitest 3.2), jest (--ci
  --changedSince=REF, verificada con jest 29.7) o Playwright (test --reporter=line --only-changed=REF, verificada con
  Playwright 1.55) lanzados directamente cuando el script es solo eso, y si no el script tal cual; los scripts
  typecheck y lint; tsc --noEmit (verificada con TypeScript 5.6) si hay tsconfig.json y no hay script; Playwright, si
  tiene su configuración y ningún script lo lanza. pnpm, yarn, bun o npm según el lockfile. El filtro por lo cambiado
  es el del propio runner; en --todo, sin filtro.
- Plugins de Claude Code (.claude-plugin/plugin.json): claude plugin validate --json y, si tiene pruebas *.test.ts o
  *.test.tsx, claude plugin test (los dos probados con su salida real).
- Rust (Cargo.toml), Go (go.mod) y .NET (*.sln o un *.csproj de tests): cargo test, go test ./... y dotnet test,
  sin opciones de filtro y sin probar en este equipo, que no tiene sus toolchains; el resumen lee sus líneas de
  totales documentadas (test result:, ok y FAIL por paquete, Passed! y Failed!). Corren siempre.

La caché y las duraciones (para partir los archivos lentos y lanzar primero lo que más tarda) van en la carpeta
temporal del sistema (sf-comprobar), fuera del repositorio; también los logs, de los que se guardan los 30 últimos.

Uso:
  python -I -X utf8 comprobar.py [--repo RUTA] [--base develop] [--todo] [--sin-cache] [--seleccion]
                                 [--archivos A [B …]] [--trabajos N] [--plazo SEGUNDOS] [--json]
      --todo        lanza todas las comprobaciones, sin seleccionar por lo cambiado (con la caché, salvo --sin-cache).
      --sin-cache   no se fía de lo que ya pasó. Antes de dejar una tarea lista para probar: --todo --sin-cache.
      --seleccion   solo la ronda 1: la lista de lo que correría y lo que se saltaría, con su porqué; no lanza nada.
      --archivos    los archivos cambiados (relativos a la raíz o absolutos), en lugar de compararlos con la base
                    (en una deliberativa, sin rama).
      --trabajos    cuántas partes a la vez (por defecto, los núcleos del equipo).
      --plazo       segundos para todo (por defecto 570, dentro de los 10 minutos de una orden).
      --json        lo mismo, para otra herramienta.
  Sale con 0 si todo pasa (o no había nada que lanzar), con 1 si algo falla o no se pudo lanzar y con 2 si la carpeta
  no es un repositorio git.
"""

from __future__ import annotations

import argparse
import ast
import concurrent.futures
import datetime
import hashlib
import json
import locale
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

VERSION = 1  # entra en el hash de la caché: si cambia cómo se lanza algo, se sube y nada se da por pasado
PLAZO_TOTAL = 570
PLAZO_PARTE = 540
LOGS_GUARDADOS = 30
FALLOS_MOSTRADOS = 8
LARGO_ORDEN = 24000  # Windows no acepta líneas de órdenes de más de 32.767 caracteres
SIN_MIRAR = {'node_modules', '.venv', 'venv', 'env', '__pycache__', 'site-packages', 'dist', 'build', 'target',
             '.git', '.tox', '.mypy_cache', '.pytest_cache'}
WINDOWS = os.name == 'nt'
ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07')


# ── El repositorio: sus archivos, su estado y lo cambiado ──

def git(raiz: Path, *args: str) -> tuple[int, str]:
    r = subprocess.run(['git', '-C', str(raiz), '-c', 'core.quotepath=off', *args], capture_output=True)
    return r.returncode, r.stdout.decode('utf-8', 'replace')


def lista_z(texto: str) -> list[str]:
    return [x for x in texto.split('\0') if x]


def contenido_id(ruta: Path) -> str:
    """El id de un archivo del árbol de trabajo, igual que el de git para el mismo contenido."""
    try:
        datos = ruta.read_bytes()
    except OSError:
        return 'borrado'
    return hashlib.sha1(b'blob %d\0' % len(datos) + datos).hexdigest()


class Proyecto:
    """Los archivos del repositorio (los de git y los nuevos sin ignorar), el id de cada uno y lo cambiado."""

    def __init__(self, raiz: Path, base: str = 'develop', archivos: list[str] | None = None, todo: bool = False):
        self.raiz = raiz
        _, ls = git(raiz, 'ls-files', '-s', '-z')
        self.estado: dict[str, str] = {}
        for linea in lista_z(ls):
            meta, _, ruta = linea.partition('\t')
            self.estado[ruta] = meta.split()[1] if len(meta.split()) > 1 else ''
        # Los nuevos, sin lo que dejan las herramientas aunque el proyecto no lo ignore (__pycache__, node_modules…)
        nuevos = [r for r in lista_z(git(raiz, 'ls-files', '-o', '--exclude-standard', '-z')[1]) if _mirable(r)]
        sucios = lista_z(git(raiz, 'diff', '--name-only', '--no-renames', '-z')[1])
        for ruta in set(nuevos) | set(sucios):
            self.estado[ruta] = contenido_id(raiz / ruta)
        self.archivos = sorted(r for r, i in self.estado.items() if i != 'borrado')
        self.base = base
        self.aviso = ''
        self.cambiados: list[str] = []
        if archivos is not None:
            self.cambiados = sorted({self.relativa(a) for a in archivos})
        elif todo:
            self.cambiados = None  # todo
        else:
            ref = self.referencia(base)
            if ref is None:
                self.aviso = f'sin la rama {base}: se lanza todo'
                self.cambiados = None  # todo
            else:
                codigo, mb = git(raiz, 'merge-base', 'HEAD', ref)
                desde = mb.strip() if codigo == 0 and mb.strip() else ref
                diff = lista_z(git(raiz, 'diff', '--name-only', '--no-renames', '-z', desde)[1])
                self.cambiados = sorted(set(diff) | set(nuevos))

    def referencia(self, base: str) -> str | None:
        for ref in (base, f'origin/{base}'):
            if git(self.raiz, 'rev-parse', '--verify', '-q', ref + '^{commit}')[0] == 0:
                return ref
        return None

    def relativa(self, ruta: str) -> str:
        p = Path(ruta)
        if p.is_absolute():
            try:
                return p.resolve().relative_to(self.raiz.resolve()).as_posix()
            except ValueError:
                return p.as_posix()
        return p.as_posix()

    def que_cubre(self, cubre: list[str]) -> list[str]:
        regex = [patron(p) for p in cubre]
        return [r for r in self.estado if any(x.match(r) for x in regex)]

    def huella(self, cubre: list[str] | None) -> str:
        """El hash de los archivos que cubre una comprobación (todos, si no dice qué cubre)."""
        rutas = sorted(self.estado) if cubre is None else sorted(self.que_cubre(cubre))
        h = hashlib.sha256()
        for r in rutas:
            h.update(f'{r}\0{self.estado[r]}\n'.encode('utf-8'))
        return h.hexdigest()


_PATRONES: dict[str, re.Pattern] = {}


def patron(p: str) -> re.Pattern:
    """Un patrón de rutas (posix, relativo a la raíz) como expresión regular: ** cualquier número de carpetas, *
    dentro de una, ? un carácter y {a,b} alternativas. Una carpeta (acabada en / o sin comodines) vale por todo lo
    que hay dentro."""
    if p in _PATRONES:
        return _PATRONES[p]
    q = p.replace('\\', '/')
    while q.startswith('./'):
        q = q[2:]
    if q.endswith('/'):
        q += '**'
    salida, i = '', 0
    while i < len(q):
        c = q[i]
        if q.startswith('**/', i):
            salida += '(?:.*/)?'
            i += 3
            continue
        if q.startswith('**', i):
            salida += '.*'
            i += 2
            continue
        if c == '*':
            salida += '[^/]*'
        elif c == '?':
            salida += '[^/]'
        elif c == '{':
            fin = q.find('}', i)
            if fin > i:
                salida += '(?:' + '|'.join(re.escape(x) for x in q[i + 1:fin].split(',')) + ')'
                i = fin + 1
                continue
            salida += re.escape(c)
        else:
            salida += re.escape(c)
        i += 1
    if not any(ch in q for ch in '*?{'):
        salida += '(?:/.*)?'
    _PATRONES[p] = re.compile(salida + r'\Z')
    return _PATRONES[p]


# ── Las comprobaciones y sus fuentes ──

@dataclass
class Comprobacion:
    """Una comprobación: un test, un archivo de tests o una orden. `nombre` la identifica (y la caché y las fuentes
    la reconocen por él); `grupo`, cómo sale en el resumen, que junta las del mismo grupo en una línea.

    orden: la lista de argumentos (o una cadena, que se lanza con el intérprete de órdenes).
    carpeta: dónde se lanza, relativa a la raíz.
    cubre: patrones de los archivos de los que depende; None si no lo dice, y entonces corre siempre.
    lector: cómo se lee su salida (pytest, unittest, vitest, jest, playwright, claude_test, claude_validate, tsc,
        cargo, go, dotnet o generico).
    reparto: 'archivo' si se puede partir por tests (pytest); None si no (o si ya reparte el runner).
    filtro: argumentos que se añaden fuera de --todo para que el runner filtre por lo cambiado; {base} es la rama.
    navegador: abre un navegador; de estas, solo una a la vez.
    sustituye: patrones de nombres de comprobaciones de menos prioridad que esta reemplaza (una declarada que
        lanza toda la suite puede quitar las detectadas archivo por archivo).
    """
    nombre: str
    grupo: str
    orden: list[str] | str
    carpeta: str = ''
    cubre: list[str] | None = None
    lector: str = 'generico'
    reparto: str | None = None
    filtro: list[str] | None = None
    plazo: int = PLAZO_PARTE
    navegador: bool = False
    archivo: str | None = None
    origen: str = 'detectado'
    sustituye: list[str] = field(default_factory=list)
    peso: float = 10.0


@dataclass
class Contexto:
    raiz: Path
    proyecto: Proyecto
    base: str
    todo: bool
    sin_cache: bool
    trabajos: int
    carpeta_tmp: Path


Fuente = Callable[[Contexto], 'list[Comprobacion]']
FUENTES: list[tuple[int, str, Fuente]] = []
AL_TERMINAR: list[Callable[[Contexto, list], None]] = []


def registrar_fuente(prioridad: int, nombre: str, funcion: Fuente) -> None:
    """Añade una fuente de comprobaciones. Menos es más prioridad: declarado 10, visto 20, detectado 30."""
    FUENTES.append((prioridad, nombre, funcion))
    FUENTES.sort(key=lambda f: f[0])


def juntar(ctx: Contexto) -> list[Comprobacion]:
    """Las comprobaciones de todas las fuentes; con el mismo nombre, la de más prioridad."""
    elegidas: dict[str, Comprobacion] = {}
    sustituidas: list[re.Pattern] = []
    for _, origen, funcion in FUENTES:
        for c in funcion(ctx):
            c.origen = origen
            if c.nombre in elegidas or any(x.match(c.nombre) for x in sustituidas):
                continue
            elegidas[c.nombre] = c
        sustituidas += [_patron_nombre(p) for c in elegidas.values() for p in c.sustituye]
    return list(elegidas.values())


def _patron_nombre(p: str) -> re.Pattern:
    return re.compile(''.join('.*' if ch == '*' else re.escape(ch) for ch in p) + r'\Z')


# ── Detección por el stack ──

def ejecutable(nombre: str, *carpetas: Path) -> str | None:
    """Un ejecutable de node_modules/.bin o del sistema."""
    for c in carpetas:
        for sufijo in (('.cmd', '.exe', '') if WINDOWS else ('',)):
            p = c / 'node_modules' / '.bin' / (nombre + sufijo)
            if p.is_file():
                return str(p)
    return None


def detectar(ctx: Contexto) -> list[Comprobacion]:
    salida: list[Comprobacion] = []
    for detector in DETECTORES:
        salida += detector(ctx)
    return salida


def _carpeta(ruta: str) -> str:
    """La carpeta de un archivo, relativa a la raíz ('' en la raíz)."""
    return ruta.rsplit('/', 1)[0] if '/' in ruta else ''


def _mirable(ruta: str) -> bool:
    return not any(parte in SIN_MIRAR for parte in ruta.split('/')[:-1])


# Python

_PYTHON_OK: dict[str, bool] = {}


def python_del_proyecto(carpeta: Path) -> str:
    for venv in ('.venv', 'venv'):
        for p in (carpeta / venv / 'Scripts' / 'python.exe', carpeta / venv / 'bin' / 'python'):
            if p.is_file():
                return str(p)
    return sys.executable


def tiene_pytest(python: str) -> bool:
    if python not in _PYTHON_OK:
        r = subprocess.run([python, '-c', 'import pytest'], capture_output=True)
        _PYTHON_OK[python] = r.returncode == 0
    return _PYTHON_OK[python]


CONFIG_PYTHON = ('pyproject.toml', 'pytest.ini', 'setup.cfg', 'tox.ini')
ES_TEST_PY = re.compile(r'(^|/)(test_[^/]*|[^/]*_test)\.py$')


def detectar_python(ctx: Contexto) -> list[Comprobacion]:
    proyecto = ctx.proyecto
    tests = [r for r in proyecto.archivos if ES_TEST_PY.search(r) and _mirable(r)]
    if not tests:
        return []
    indice = Indice(proyecto)
    salida = []
    for t in tests:
        texto = _leer(ctx.raiz / t)
        if not re.search(r'\bunittest\b|\bpytest\b|^\s*def test', texto, re.M):
            continue
        carpeta = _raiz_python(ctx.raiz, t)
        python = python_del_proyecto(ctx.raiz / carpeta)
        desde = Path(t).relative_to(carpeta).as_posix() if carpeta else t
        dir_test = Path(t).parent.as_posix()
        grupo = f'tests de Python ({dir_test})' if dir_test != '.' else 'tests de Python'
        cubre = indice.cubre_test(t)
        if cubre is not None:
            cubre += [f'{carpeta}/{c}' if carpeta else c for c in CONFIG_PYTHON]
            cubre += [p for p in _conftests(t)]
        n = max(1, len(re.findall(r'^\s*(?:async\s+)?def test', texto, re.M)))
        if tiene_pytest(python):
            orden = [python, '-X', 'utf8', '-m', 'pytest', '-q', '-rfE', '--tb=short', '--color=no',
                     '-p', 'no:cacheprovider', '--durations=0', '--durations-min=0.5', desde]
            salida.append(Comprobacion(f'pytest {t}', grupo, orden, carpeta, cubre, 'pytest', 'archivo',
                                       archivo=desde, peso=0.4 * n))
        else:
            orden = [python, '-X', 'utf8', '-m', 'unittest', 'discover', '-s', str(Path(desde).parent),
                     '-p', Path(t).name, '-t', str(Path(desde).parent)]
            salida.append(Comprobacion(f'unittest {t}', grupo, orden, carpeta, cubre, 'unittest',
                                       archivo=desde, peso=0.4 * n))
    return salida


def _raiz_python(raiz: Path, test: str) -> str:
    """La carpeta del proyecto de Python de un test: la más cercana con su configuración; si no, la raíz."""
    partes = Path(test).parts[:-1]
    for i in range(len(partes), 0, -1):
        carpeta = Path(*partes[:i])
        if any((raiz / carpeta / c).is_file() for c in CONFIG_PYTHON):
            return carpeta.as_posix()
    return ''


def _conftests(test: str) -> list[str]:
    partes = Path(test).parts[:-1]
    return [Path(*partes[:i], 'conftest.py').as_posix() for i in range(len(partes) + 1)]


def detectar_ruff(ctx: Contexto) -> list[Comprobacion]:
    pyproject = _leer(ctx.raiz / 'pyproject.toml')
    if '[tool.ruff' not in pyproject and not any((ctx.raiz / c).is_file() for c in ('ruff.toml', '.ruff.toml')):
        return []
    ruff = shutil.which('ruff', path=str(Path(python_del_proyecto(ctx.raiz)).parent)) or shutil.which('ruff')
    if not ruff:
        return []
    return [Comprobacion('ruff', 'ruff', [ruff, 'check', '.', '--output-format', 'concise'], '',
                         ['**/*.py', '**/*.pyi', 'pyproject.toml', 'ruff.toml', '.ruff.toml'], 'ruff', peso=2)]


def _leer(ruta: Path) -> str:
    try:
        return ruta.read_text(encoding='utf-8', errors='replace')
    except OSError:
        return ''


class Indice:
    """Lo que nombra cada archivo de Python del proyecto, para saber qué cubre un test.

    De cada archivo se leen sus importaciones (de módulos del proyecto), las rutas que construye desde __file__
    (Path(__file__).resolve().parents[1] / 'tools' / 'cola.py', y las constantes hechas de otras), los glob,
    rglob e iterdir sobre esas rutas (que dan un patrón), las rutas pasadas a os.walk o os.listdir y los nombres de
    archivo que escribe ('estilo_documento.css'). Los glob sobre algo que no sale de __file__ (una carpeta
    temporal) no cuentan. Se sigue de forma transitiva por los .py del proyecto que nombra."""

    MARCAS = ('glob', 'rglob', 'iterdir')

    def __init__(self, proyecto: Proyecto):
        self.proyecto = proyecto
        self.raiz = proyecto.raiz.resolve()
        self.por_nombre: dict[str, list[str]] = {}
        self.por_modulo: dict[str, list[str]] = {}
        for r in proyecto.archivos:
            nombre = r.rsplit('/', 1)[-1]
            self.por_nombre.setdefault(nombre, []).append(r)
            if nombre.endswith('.py'):
                modulo = r.rsplit('/', 2)[-2] if nombre == '__init__.py' and '/' in r else nombre[:-3]
                self.por_modulo.setdefault(modulo, []).append(r)
        self._nombra: dict[str, tuple[set[str], set[str]]] = {}

    def cubre_test(self, test: str) -> list[str] | None:
        archivos, patrones = {test}, set()
        pendientes, vistos = [test], set()
        while pendientes:
            r = pendientes.pop()
            if r in vistos:
                continue
            vistos.add(r)
            a, p = self.nombra(r)
            archivos |= a
            patrones |= p
            pendientes += [x for x in a if x.endswith('.py') and x not in vistos]
        if archivos == {test} and not patrones:
            return None
        return sorted(archivos) + sorted(patrones)

    def nombra(self, r: str) -> tuple[set[str], set[str]]:
        if r in self._nombra:
            return self._nombra[r]
        archivos: set[str] = set()
        patrones: set[str] = set()
        self._nombra[r] = (archivos, patrones)
        try:
            arbol = ast.parse(_leer(self.proyecto.raiz / r))
        except (SyntaxError, ValueError):
            return archivos, patrones
        rutas = _Rutas(self.proyecto.raiz / r, arbol)
        for n in ast.walk(arbol):
            if isinstance(n, ast.Import):
                for a in n.names:
                    for parte in a.name.split('.'):
                        archivos.update(self.por_modulo.get(parte, ()))
            elif isinstance(n, ast.ImportFrom):
                for parte in (n.module or '').split('.') + [a.name for a in n.names]:
                    archivos.update(self.por_modulo.get(parte, ()))
            elif isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) < 300:
                for nombre in re.findall(r'[\w.-]+\.[A-Za-z][A-Za-z0-9]{0,7}\b', n.value):
                    archivos.update(self.por_nombre.get(nombre.rsplit('/', 1)[-1], ()))
            elif isinstance(n, ast.Call):
                f = n.func
                if isinstance(f, ast.Attribute) and f.attr in self.MARCAS:
                    base = rutas.valor(f.value)
                    if base is not None:
                        patron_arg = n.args[0].value if n.args and isinstance(n.args[0], ast.Constant) else '*'
                        rel = self._relativa(base)
                        if rel is not None and isinstance(patron_arg, str):
                            pre = f'{rel}/' if rel else ''
                            patrones.add(pre + ('**/' if f.attr == 'rglob' else '') + patron_arg)
                elif (isinstance(f, ast.Attribute) and f.attr in ('walk', 'listdir', 'scandir')
                      and isinstance(f.value, ast.Name) and f.value.id == 'os' and n.args):
                    base = rutas.valor(n.args[0])
                    rel = self._relativa(base) if base is not None else None
                    if rel is not None:
                        patrones.add(f'{rel}/**' if rel else '**')
        for valor in rutas.todas():
            rel = self._relativa(valor)
            if rel and rel in self.proyecto.estado:
                archivos.add(rel)
        archivos.discard(r)
        return archivos, patrones

    def _relativa(self, ruta: Path) -> str | None:
        try:
            rel = Path(os.path.normpath(str(ruta))).relative_to(self.raiz)
        except ValueError:
            try:
                rel = Path(os.path.normpath(str(ruta))).relative_to(self.proyecto.raiz)
            except ValueError:
                return None
        return '' if str(rel) == '.' else rel.as_posix()


class _Rutas:
    """Evalúa, sin ejecutar nada, las rutas que un archivo construye desde __file__."""

    def __init__(self, archivo: Path, arbol: ast.AST):
        self.archivo = Path(os.path.abspath(str(archivo)))
        self.nombres: dict[str, Path] = {}
        self.valores: list[Path] = []
        cuerpo = getattr(arbol, 'body', [])
        otras = [n for n in ast.walk(arbol) if isinstance(n, ast.Assign)]
        for n in [x for x in cuerpo if isinstance(x, ast.Assign)] + otras:
            if len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
                nombre = n.targets[0].id
                v = self.valor(n.value)
                if v is not None and nombre not in self.nombres:
                    self.nombres[nombre] = v
        for n in ast.walk(arbol):
            if isinstance(n, (ast.BinOp, ast.Call)):
                v = self.valor(n)
                if v is not None:
                    self.valores.append(v)

    def todas(self) -> list[Path]:
        return self.valores + list(self.nombres.values())

    def valor(self, n: ast.AST) -> Path | None:
        if isinstance(n, ast.Name):
            if n.id == '__file__':
                return self.archivo
            return self.nombres.get(n.id)
        if isinstance(n, ast.Call):
            f = n.func
            nombre = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ''
            if nombre in ('Path', 'PurePath') and len(n.args) == 1:
                return self.valor(n.args[0])
            if isinstance(f, ast.Attribute) and f.attr in ('resolve', 'absolute') and not n.args:
                return self.valor(f.value)
            if isinstance(f, ast.Attribute) and f.attr == 'joinpath':
                base = self.valor(f.value)
                partes = [a.value for a in n.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
                return base.joinpath(*partes) if base is not None and len(partes) == len(n.args) else None
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Attribute) and f.value.attr == 'path':
                if f.attr in ('dirname',) and n.args:
                    v = self.valor(n.args[0])
                    return v.parent if v is not None else None
                if f.attr in ('abspath', 'realpath', 'normpath') and n.args:
                    return self.valor(n.args[0])
                if f.attr == 'join' and n.args:
                    base = self.valor(n.args[0])
                    resto = [a.value for a in n.args[1:] if isinstance(a, ast.Constant) and isinstance(a.value, str)]
                    return base.joinpath(*resto) if base is not None and len(resto) == len(n.args) - 1 else None
            return None
        if isinstance(n, ast.Attribute) and n.attr == 'parent':
            v = self.valor(n.value)
            return v.parent if v is not None else None
        if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Attribute) and n.value.attr == 'parents':
            v = self.valor(n.value.value)
            indice = n.slice.value if isinstance(n.slice, ast.Constant) else None  # 3.9+: el índice va tal cual
            if v is not None and isinstance(indice, int) and 0 <= indice < len(v.parents):
                return v.parents[indice]
            return None
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div):
            v = self.valor(n.left)
            if v is not None and isinstance(n.right, ast.Constant) and isinstance(n.right.value, str):
                return v / n.right.value
        return None


# Node

LOCKS = (('pnpm-lock.yaml', 'pnpm'), ('yarn.lock', 'yarn'), ('bun.lockb', 'bun'), ('bun.lock', 'bun'))
SCRIPT_DIRECTO = re.compile(r'^\s*(vitest(?:\s+run)?|jest|playwright\s+test)(\s+[^&|;<>]*)?\s*$')


def gestor(raiz: Path, carpeta: Path) -> str:
    for c in (carpeta, raiz):
        for lock, nombre in LOCKS:
            if (c / lock).is_file():
                return nombre
    return 'npm'


def detectar_node(ctx: Contexto) -> list[Comprobacion]:
    salida = []
    for r in ctx.proyecto.archivos:
        if not (r == 'package.json' or r.endswith('/package.json')) or not _mirable(r) or r.count('/') > 3:
            continue
        try:
            paquete = json.loads(_leer(ctx.raiz / r))
        except ValueError:
            continue
        if not isinstance(paquete, dict):
            continue
        carpeta = Path(r).parent.as_posix()
        carpeta = '' if carpeta == '.' else carpeta
        dir_abs = ctx.raiz / carpeta
        donde = f' ({carpeta})' if carpeta else ''
        pm = gestor(ctx.raiz, dir_abs)
        pm_exe = shutil.which(pm) or pm
        scripts = paquete.get('scripts') if isinstance(paquete.get('scripts'), dict) else {}
        deps = {**(paquete.get('dependencies') or {}), **(paquete.get('devDependencies') or {})}
        test = str(scripts.get('test') or '')
        lanza_playwright = any('playwright test' in str(s) for s in scripts.values())
        if test and 'no test specified' not in test:
            salida.append(_node_test(ctx, test, pm_exe, carpeta, dir_abs, donde))
        for nombre in ('typecheck', 'type-check', 'check-types', 'types'):
            if nombre in scripts:
                salida.append(Comprobacion(f'{pm} run {nombre}{donde}', f'{nombre}{donde}',
                                           [pm_exe, 'run', nombre], carpeta, lector='tsc', peso=8))
                break
        else:
            tsc = ejecutable('tsc', dir_abs, ctx.raiz)
            if (dir_abs / 'tsconfig.json').is_file() and tsc:
                pre = f'{carpeta}/' if carpeta else ''
                cubre = [f'{pre}**/*.{{ts,tsx,mts,cts}}', f'{pre}**/tsconfig*.json', f'{pre}package.json']
                salida.append(Comprobacion(f'tsc{donde}', f'tsc{donde}', [tsc, '--noEmit', '-p', '.'], carpeta,
                                           cubre, 'tsc', peso=8))
        if 'lint' in scripts:
            salida.append(Comprobacion(f'{pm} run lint{donde}', f'lint{donde}', [pm_exe, 'run', 'lint'], carpeta,
                                       peso=6))
        config_pw = any((dir_abs / f'playwright.config.{e}').is_file() for e in ('ts', 'js', 'mjs', 'cjs', 'mts'))
        if config_pw and not lanza_playwright and ('@playwright/test' in deps or ejecutable('playwright', dir_abs)):
            pw = ejecutable('playwright', dir_abs, ctx.raiz)
            if pw:
                salida.append(Comprobacion(f'playwright{donde}', f'Playwright{donde}',
                                           [pw, 'test', '--reporter=line'], carpeta, lector='playwright',
                                           filtro=['--only-changed={base}'], navegador=True, peso=60))
    return salida


def _node_test(ctx: Contexto, test: str, pm_exe: str, carpeta: str, dir_abs: Path, donde: str) -> Comprobacion:
    m = SCRIPT_DIRECTO.match(test)
    if m:
        partes = m.group(1).split()
        resto = (m.group(2) or '').split()
        exe = ejecutable(partes[0], dir_abs, ctx.raiz)
        if exe:
            if partes[0] == 'vitest':
                return Comprobacion(f'vitest{donde}', f'tests de vitest{donde}', [exe, 'run', *resto], carpeta,
                                    lector='vitest', filtro=['--changed', '{base}'], peso=20)
            if partes[0] == 'jest':
                return Comprobacion(f'jest{donde}', f'tests de jest{donde}', [exe, *resto, '--ci'], carpeta,
                                    lector='jest', filtro=['--changedSince={base}'], peso=20)
            return Comprobacion(f'playwright{donde}', f'Playwright{donde}',
                                [exe, 'test', *resto, '--reporter=line'], carpeta, lector='playwright',
                                filtro=['--only-changed={base}'], navegador=True, peso=60)
    lector = 'vitest' if 'vitest' in test else 'jest' if 'jest' in test else (
        'playwright' if 'playwright' in test else 'generico')
    return Comprobacion(f'test{donde}', f'test{donde}', [pm_exe, 'test'], carpeta, lector=lector,
                        navegador=lector == 'playwright', peso=20)


# Plugins de Claude Code

def detectar_plugins(ctx: Contexto) -> list[Comprobacion]:
    claude = shutil.which('claude')
    if not claude:
        return []
    salida = []
    for r in ctx.proyecto.archivos:
        if not r.endswith('.claude-plugin/plugin.json') or not _mirable(r):
            continue
        carpeta = Path(r).parent.parent.as_posix()
        carpeta = '' if carpeta == '.' else carpeta
        pre = f'{carpeta}/' if carpeta else ''
        donde = f' ({carpeta})' if carpeta else ''
        salida.append(Comprobacion(f'claude plugin validate{donde}', f'claude plugin validate{donde}',
                                   [claude, 'plugin', 'validate', carpeta or '.', '--json'], '',
                                   [f'{pre}.claude-plugin/**', f'{pre}hooks/**', f'{pre}skills/**/SKILL.md',
                                    f'{pre}commands/**', f'{pre}agents/**', f'{pre}*.json', f'{pre}types/**',
                                    f'{pre}README.md'], 'claude_validate', peso=3))
        pruebas = [x for x in ctx.proyecto.archivos if x.startswith(pre) and re.search(r'\.test\.tsx?$', x)]
        if pruebas:
            salida.append(Comprobacion(f'claude plugin test{donde}', f'claude plugin test{donde}',
                                       [claude, 'plugin', 'test', carpeta or '.'], '',
                                       [f'{pre}**/*.{{ts,tsx,js,mjs,cjs,json}}'], 'claude_test', peso=70))
    return salida


# Rust, Go y .NET (sin probar en este equipo: corren siempre, sin filtro)

def detectar_compilados(ctx: Contexto) -> list[Comprobacion]:
    salida = []
    archivos = ctx.proyecto.archivos
    carpetas = {_carpeta(r) for r in archivos if r.rsplit('/', 1)[-1] == 'Cargo.toml' and _mirable(r)}
    raices = [d for d in carpetas if not any(o != d and (o == '' or d.startswith(o + '/')) for o in carpetas)]
    for carpeta in sorted(raices)[:3]:
        workspace = '[workspace]' in _leer(ctx.raiz / carpeta / 'Cargo.toml')
        donde = f' ({carpeta})' if carpeta else ''
        salida.append(Comprobacion(f'cargo test{donde}', f'cargo test{donde}',
                                   ['cargo', 'test'] + (['--workspace'] if workspace else []), carpeta,
                                   lector='cargo', peso=60))
    for g in [r for r in archivos if r.rsplit('/', 1)[-1] == 'go.mod' and _mirable(r)][:3]:
        carpeta = _carpeta(g)
        donde = f' ({carpeta})' if carpeta else ''
        salida.append(Comprobacion(f'go test{donde}', f'go test{donde}', ['go', 'test', './...'], carpeta,
                                   lector='go', peso=30))
    slns = [r for r in archivos if r.endswith('.sln') and _mirable(r)]
    proyectos_test = [r for r in archivos if r.endswith('.csproj') and _mirable(r)
                      and 'Microsoft.NET.Test.Sdk' in _leer(ctx.raiz / r)]
    if slns or proyectos_test:
        objetivo = slns[0] if slns else proyectos_test[0]
        salida.append(Comprobacion('dotnet test', 'dotnet test', ['dotnet', 'test', objetivo], '',
                                   lector='dotnet', peso=60))
    return salida


DETECTORES: list[Callable[[Contexto], list[Comprobacion]]] = [detectar_python, detectar_ruff, detectar_node,
                                                               detectar_plugins, detectar_compilados]
registrar_fuente(30, 'detectado', detectar)


# ── Ronda 1: seleccionar ──

@dataclass
class Eleccion:
    comprobacion: Comprobacion
    corre: bool
    motivo: str
    huella: str = ''


def seleccionar(ctx: Contexto, comprobaciones: list[Comprobacion], cache: dict) -> tuple[list[Eleccion], list[str]]:
    """Qué corre y qué se salta, con su porqué, y los archivos cambiados que no cubre ninguna comprobación. Con los
    mismos archivos, el mismo registro y la misma caché, siempre la misma lista."""
    cambiados = ctx.proyecto.cambiados
    todo = ctx.todo or cambiados is None
    elecciones = []
    cubiertos: set[str] = set()
    for c in sorted(comprobaciones, key=lambda x: x.nombre):
        huella = hashlib.sha256(json.dumps([VERSION, c.orden, c.carpeta, c.filtro if not todo else None,
                                            ctx.proyecto.huella(c.cubre)]).encode('utf-8')).hexdigest()
        if todo:
            corre, motivo = True, 'todo'
        elif c.cubre is None:
            corre, motivo = True, 'no dice qué cubre'
        else:
            regex = [patron(p) for p in c.cubre]
            tocados = [r for r in cambiados if any(x.match(r) for x in regex)]
            cubiertos.update(tocados)
            if tocados:
                corre = True
                motivo = 'toca ' + tocados[0] + (f' y {len(tocados) - 1} más' if len(tocados) > 1 else '')
            else:
                corre, motivo = False, 'nada de lo que cubre cambió'
        if corre and not ctx.sin_cache:
            previo = cache.get('pasadas', {}).get(c.nombre)
            if previo and previo.get('huella') == huella:
                corre, motivo = False, f'ya pasó, sin cambios desde las {previo.get("hora", "?")}'
        elecciones.append(Eleccion(c, corre, motivo, huella))
    sin_cubrir = [] if todo else [r for r in cambiados if r not in cubiertos]
    return elecciones, sin_cubrir


# ── Ronda 2: ejecutar ──

@dataclass
class Parte:
    comprobacion: Comprobacion
    orden: list[str] | str
    etiqueta: str
    peso: float


@dataclass
class Salida:
    parte: Parte
    codigo: int | None
    segundos: float
    texto: str
    agotada: bool = False
    no_lanzada: str = ''
    inicio: float = 0.0
    fin: float = 0.0


def _codificacion_del_sistema() -> str:
    """La de las órdenes que no escriben en UTF-8 (en Windows, su página de códigos), también con -X utf8."""
    obtener = getattr(locale, 'getencoding', None)  # 3.11+: el modo UTF-8 no la cambia
    nombre = obtener() if obtener else ('cp1252' if WINDOWS else locale.getpreferredencoding(False))
    return 'cp1252' if WINDOWS and nombre.lower().replace('-', '') in ('utf8', '') else nombre


def decodificar(datos: bytes) -> str:
    """La salida de una orden como texto, línea a línea: en UTF-8 la que lo es y en la codificación del sistema la
    que no (una orden puede mezclarlas), sin romperse nunca."""
    try:
        texto = datos.decode('utf-8')
    except UnicodeDecodeError:
        otra = _codificacion_del_sistema()
        lineas = []
        for linea in datos.split(b'\n'):
            try:
                lineas.append(linea.decode('utf-8'))
            except UnicodeDecodeError:
                lineas.append(linea.decode(otra, 'replace'))
        texto = '\n'.join(lineas)
    return ANSI.sub('', texto).replace('\r\n', '\n')


def entorno() -> dict[str, str]:
    e = dict(os.environ)
    e.update({'PYTHONUTF8': '1', 'PYTHONIOENCODING': 'utf-8', 'FORCE_COLOR': '0', 'CARGO_TERM_COLOR': 'never',
              'PY_COLORS': '0', 'COLUMNS': '200'})  # con 80 columnas, pytest corta el error del resumen
    e.pop('NO_COLOR', None)  # con FORCE_COLOR, node avisa en cada proceso si están los dos
    return e


def lanzar(orden: list[str] | str, cwd: Path, plazo: float,
           baja: bool = False) -> tuple[int | None, bytes, bool, str]:
    """Lanza una orden y espera como mucho `plazo` segundos; si no acaba, mata su árbol de procesos. Con `baja`,
    con menos prioridad (sus hijos la heredan), para que la parte más larga, que marca el total, no espere a las
    demás cuando todas compiten por el procesador."""
    if WINDOWS:
        flags = subprocess.CREATE_NEW_PROCESS_GROUP | (subprocess.BELOW_NORMAL_PRIORITY_CLASS if baja else 0)
        extra = {'creationflags': flags}
    else:
        extra = {'start_new_session': True}
        if baja and isinstance(orden, list) and shutil.which('nice'):
            orden = ['nice', '-n', '5', *orden]
    try:
        p = subprocess.Popen(orden, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             stdin=subprocess.DEVNULL, env=entorno(), shell=isinstance(orden, str), **extra)
    except OSError as e:
        return None, b'', False, f'{e.strerror or e}'
    try:
        datos, _ = p.communicate(timeout=max(1.0, plazo))
        return p.returncode, datos, False, ''
    except subprocess.TimeoutExpired:
        matar(p)
        try:
            datos, _ = p.communicate(timeout=10)
        except (subprocess.TimeoutExpired, ValueError):
            datos = b''
        return p.returncode, datos or b'', True, ''


def matar(p: subprocess.Popen) -> None:
    try:
        if WINDOWS:
            subprocess.run(['taskkill', '/F', '/T', '/PID', str(p.pid)], capture_output=True)
        else:
            os.killpg(p.pid, signal.SIGKILL)
    except (OSError, ProcessLookupError):
        p.kill()


def recoger_pytest(ctx: Contexto, comprobaciones: list[Comprobacion]) -> dict[str, list[str]]:
    """Los ids de los tests de cada archivo de pytest, en una sola recogida por carpeta y por intérprete."""
    salida: dict[str, list[str]] = {}
    grupos: dict[tuple[str, str], list[Comprobacion]] = {}
    for c in comprobaciones:
        grupos.setdefault((c.carpeta, c.orden[0]), []).append(c)
    for (carpeta, python), cs in grupos.items():
        orden = [python, '-X', 'utf8', '-m', 'pytest', '--collect-only', '-q', '--color=no', '-p',
                 'no:cacheprovider', *[c.archivo for c in cs]]
        codigo, datos, _, _ = lanzar(orden, ctx.raiz / carpeta, 120)
        ids = [x.strip() for x in decodificar(datos).splitlines() if '::' in x and not x.startswith(' ')]
        for c in cs:
            propio = c.archivo.replace('\\', '/')
            for i in ids:
                fichero, _, resto = i.partition('::')
                fichero = fichero.replace('\\', '/')
                if propio == fichero or propio.endswith('/' + fichero) or fichero.endswith('/' + propio):
                    salida.setdefault(c.nombre, []).append(f'{c.archivo}::{resto}')
    return salida


def preparar(ctx: Contexto, elegidas: list[Comprobacion], duraciones: dict[str, float],
             tiempos: dict[str, dict[str, float]] | None = None) -> list[Parte]:
    """Las partes que se lanzan: una por comprobación, y los archivos de pytest que tardan más que la parte que
    toca a cada trabajo, repartidos en varias por lo que tardó cada test la última vez."""
    base = ctx.base
    todo = ctx.todo or ctx.proyecto.cambiados is None
    tiempos = tiempos or {}
    peso = {c.nombre: duraciones.get(c.nombre, c.peso) for c in elegidas}
    objetivo = max(10.0, sum(peso.values()) / max(1, ctx.trabajos))
    partibles = [c for c in elegidas if c.reparto == 'archivo' and c.lector == 'pytest'
                 and peso[c.nombre] > objetivo and isinstance(c.orden, list)]
    ids = recoger_pytest(ctx, partibles) if partibles else {}
    partes = []
    for c in elegidas:
        orden = c.orden
        if c.filtro and not todo and isinstance(orden, list):
            orden = orden + [x.replace('{base}', base) for x in c.filtro]
        tests = ids.get(c.nombre, [])
        n = min(len(tests), 16, math.ceil(peso[c.nombre] / objetivo)) if tests else 1
        if n <= 1:
            partes.append(Parte(c, orden, c.nombre, peso[c.nombre]))
            continue
        trozos = repartir(tests, tiempos.get(c.nombre, {}), n, objetivo, peso[c.nombre])
        if any(sum(len(t) + 3 for t in trozo) > LARGO_ORDEN for trozo, _ in trozos):
            partes.append(Parte(c, orden, c.nombre, peso[c.nombre]))  # no cabría en una línea de órdenes
            continue
        for k, (trozo, t) in enumerate(trozos, 1):
            partes.append(Parte(c, orden[:-1] + trozo, f'{c.nombre} [{k}/{len(trozos)}]', t))
    return sorted(partes, key=lambda p: (-p.peso, p.etiqueta))


def repartir(tests: list[str], tiempos: dict[str, float], n: int, objetivo: float,
             total: float) -> list[tuple[list[str], float]]:
    """Reparte los tests de un archivo en n trozos de duración parecida: cada clase va entera a un trozo (su
    setUpClass corre una vez) salvo que tarde más que el objetivo; el más largo primero, al trozo más corto.
    Determinista: con los mismos tests y tiempos, los mismos trozos, y cada uno en el orden del archivo."""
    conocidos = [tiempos[t] for t in tests if t in tiempos]
    resto = max(0.0, total - sum(conocidos))
    desconocidos = len(tests) - len(conocidos)
    defecto = max(0.05, resto / desconocidos) if desconocidos else 0.05
    unidades: dict[str, list[str]] = {}
    for t in tests:
        trozos = t.split('::')
        unidades.setdefault('::'.join(trozos[:2]) if len(trozos) > 2 else t, []).append(t)
    lista: list[tuple[list[str], float]] = []
    for miembros in unidades.values():
        duracion = sum(tiempos.get(m, defecto) for m in miembros)
        if duracion > objetivo and len(miembros) > 1:
            lista += [([m], tiempos.get(m, defecto)) for m in miembros]
        else:
            lista.append((miembros, duracion))
    cajas: list[list] = [[0.0, i, []] for i in range(n)]
    for miembros, duracion in sorted(lista, key=lambda x: -x[1]):
        caja = min(cajas, key=lambda c: (c[0], c[1]))
        caja[0] += duracion
        caja[2] += miembros
    orden = {t: i for i, t in enumerate(tests)}
    return [(sorted(c[2], key=orden.get), c[0]) for c in sorted(cajas, key=lambda c: c[1]) if c[2]]


def tiempos_pytest(c: Comprobacion, texto: str) -> dict[str, float]:
    """Lo que tardó cada test (preparar, correr y recoger), de las líneas de --durations."""
    salida: dict[str, float] = {}
    for m in re.finditer(r'^\s*([\d.]+)s (?:setup|call|teardown)\s+(\S.*?)\s*$', texto, re.M):
        _, _, resto = m.group(2).partition('::')
        if resto:
            clave = f'{c.archivo}::{resto}'
            salida[clave] = round(salida.get(clave, 0.0) + float(m.group(1)), 2)
    return salida


def ejecutar(ctx: Contexto, partes: list[Parte], plazo_total: float) -> list[Salida]:
    """Lanza las partes a la vez, la que más tarda primero; la más larga, con la prioridad normal, y las demás, con
    menos, para que el total sea el de la más larga y no el de todas peleando por el procesador."""
    inicio = time.monotonic()
    navegador = threading.Semaphore(1)
    larga = max(partes, key=lambda p: p.peso) if len(partes) > 1 else None

    def una(parte: Parte) -> Salida:
        resta = plazo_total - (time.monotonic() - inicio)
        if resta <= 1:
            return Salida(parte, None, 0.0, '', agotada=True)
        candado = navegador if parte.comprobacion.navegador else None
        if candado:
            candado.acquire()
        try:
            t0 = time.monotonic()
            resta = plazo_total - (t0 - inicio)
            codigo, datos, agotada, error = lanzar(parte.orden, ctx.raiz / parte.comprobacion.carpeta,
                                                   min(parte.comprobacion.plazo, resta),
                                                   baja=larga is not None and parte is not larga)
            t1 = time.monotonic()
            return Salida(parte, codigo, t1 - t0, decodificar(datos), agotada, error, t0, t1)
        finally:
            if candado:
                candado.release()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, ctx.trabajos)) as ex:
        return list(ex.map(una, partes))


# ── Leer cada salida ──

@dataclass
class Lectura:
    ok: bool
    total: int | None = None
    fallidos: int = 0
    fallos: list[tuple[str, str]] = field(default_factory=list)
    nota: str = ''


def _cuenta(texto: str, palabra: str) -> int:
    return sum(int(x) for x in re.findall(rf'(\d+) {palabra}\b', texto))


def _corta(texto: str, largo: int = 160) -> str:
    texto = ' '.join(texto.split())
    return texto if len(texto) <= largo else texto[:largo - 1] + '…'


def leer_pytest(texto: str, codigo: int | None) -> Lectura:
    final = ''
    for linea in reversed(texto.splitlines()):
        if re.search(r'\d+ (passed|failed|error|errors|skipped|deselected)\b|no tests ran', linea):
            final = linea
            break
    pasados, fallidos = _cuenta(final, 'passed'), _cuenta(final, 'failed') + _cuenta(final, 'errors?')
    fallos = []
    for linea in texto.splitlines():
        m = re.match(r'(FAILED|ERROR) (\S+)(?: - (.*))?$', linea)
        if m:
            fallos.append((m.group(2), _corta(m.group(3) or _primer_error(texto, m.group(2)) or m.group(1).lower())))
    ok = codigo in (0, 5)
    return Lectura(ok, pasados + fallidos + _cuenta(final, 'skipped'), max(fallidos, len(fallos)) if not ok else 0,
                   fallos, 'sin tests' if codigo == 5 else '')


def _primer_error(texto: str, nodo: str) -> str:
    """La primera línea «E   …» del traceback de un test, cuando el resumen no trae su error."""
    nombre = nodo.rsplit('::', 1)[-1]
    m = re.search(r'^_{3,} .*?\b' + re.escape(nombre) + r'\b.*? _{3,}$', texto, re.M)
    if not m:
        return ''
    e = re.search(r'^E\s+(.+)$', texto[m.end():], re.M)
    return e.group(1) if e else ''


def leer_unittest(texto: str, codigo: int | None) -> Lectura:
    m = re.search(r'^Ran (\d+) tests?', texto, re.M)
    fallos = []
    bloques = re.split(r'^={50,}\n', texto, flags=re.M)
    for b in bloques[1:]:
        cab = re.match(r'(FAIL|ERROR): (\S+) \((.+?)\)', b)
        if cab:
            trozos = b.split('-' * 70)
            lineas = [x for x in (trozos[1] if len(trozos) > 1 else b).strip().splitlines() if x.strip()]
            error = next((x for x in reversed(lineas) if re.match(r'\w*(Error|Exception)\b', x.strip())),
                         lineas[-1] if lineas else '')
            completo = cab.group(3) if cab.group(3).endswith('.' + cab.group(2)) else f'{cab.group(3)}.{cab.group(2)}'
            fallos.append((completo, _corta(error)))
    ok = codigo == 0
    return Lectura(ok, int(m.group(1)) if m else None, 0 if ok else max(1, len(fallos)), fallos)


def leer_vitest(texto: str, codigo: int | None) -> Lectura:
    tests = re.search(r'^\s*Tests\s+(.*)$', texto, re.M)
    linea = tests.group(1) if tests else ''
    fallos = []
    for m in re.finditer(r'^\s*FAIL\s+(\S+ > .+)$', texto, re.M):
        resto = texto[m.end():].lstrip('\n').splitlines()
        fallos.append((m.group(1).strip(), _corta(next((x for x in resto if x.strip()), ''))))
    ok = codigo == 0
    total = _cuenta(linea, 'passed') + _cuenta(linea, 'failed') + _cuenta(linea, 'skipped')
    nota = 'ningún test tocado por lo cambiado' if 'No test files found' in texto else ''
    return Lectura(ok, total if tests else None, 0 if ok else max(_cuenta(linea, 'failed'), len(fallos), 1),
                   _unicos(fallos), nota)


def leer_jest(texto: str, codigo: int | None) -> Lectura:
    tests = re.search(r'^Tests:\s+(.*)$', texto, re.M)
    linea = tests.group(1) if tests else ''
    fallos = []
    for m in re.finditer(r'^\s*● (.+)$', texto, re.M):
        resto = texto[m.end():].lstrip('\n').splitlines()
        fallos.append((m.group(1).strip(), _corta(next((x for x in resto if x.strip()), ''))))
    ok = codigo == 0
    nota = 'ningún test tocado por lo cambiado' if 'No tests found related' in texto else ''
    return Lectura(ok, _cuenta(linea, 'total') if tests else None,
                   0 if ok else max(_cuenta(linea, 'failed'), len(fallos), 1), fallos, nota)


def leer_playwright(texto: str, codigo: int | None) -> Lectura:
    fallos = []
    for m in re.finditer(r'^\s*\d+\) (.+?)\s*─*$', texto, re.M):
        resto = texto[m.end():].lstrip('\n').splitlines()
        fallos.append((m.group(1).strip(), _corta(next((x for x in resto if x.strip()), ''))))
    pasados = sum(int(x) for x in re.findall(r'^\s*(\d+) passed', texto, re.M))
    fallidos = sum(int(x) for x in re.findall(r'^\s*(\d+) failed', texto, re.M))
    ok = codigo == 0
    return Lectura(ok, pasados + fallidos or None, 0 if ok else max(fallidos, len(fallos), 1), _unicos(fallos))


def leer_claude_test(texto: str, codigo: int | None) -> Lectura:
    lineas = texto.splitlines()
    fallos = []
    for i, linea in enumerate(lineas):
        m = re.match(r'\(fail\) (.+?)(?: \[[\d.]+m?s\])?$', linea.strip())
        if m:
            error = next((x.strip() for x in lineas[i + 1:i + 6] if x.strip()), '')
            fallos.append((m.group(1), _corta(error)))
    total = re.search(r'Ran (\d+) tests?', texto)
    ok = codigo == 0
    fallidos = re.search(r'^\s*(\d+) fail\b', texto, re.M)
    n = int(fallidos.group(1)) if fallidos else len(fallos)
    if not ok and not fallos:
        fallos = [('', _corta(x)) for x in [y for y in lineas if y.strip()][-3:]]
    return Lectura(ok, int(total.group(1)) if total else None, 0 if ok else max(n, 1), fallos)


def leer_claude_validate(texto: str, codigo: int | None) -> Lectura:
    inicio = texto.find('{')
    try:
        datos = json.loads(texto[inicio:]) if inicio >= 0 else None
    except ValueError:
        datos = None
    if not isinstance(datos, dict):
        return leer_generico(texto, codigo)
    piezas = [datos.get('manifest') or {}] + list(datos.get('contents') or [])
    errores = [(Path(str(p.get('file', ''))).name, _mensaje(e)) for p in piezas for e in (p.get('errors') or [])]
    avisos = sum(len(p.get('warnings') or []) for p in piezas)
    directorio = len(((datos.get('directory') or {}).get('findings')) or [])
    notas = []
    if avisos:
        notas.append(f'{avisos} aviso' + ('s' if avisos > 1 else ''))
    if directorio:
        notas.append(f'{directorio} aviso' + ('s' if directorio > 1 else '') + ' del directorio de plugins')
    ok = codigo == 0 and bool(datos.get('success', True))
    return Lectura(ok, None, 0 if ok else max(1, len(errores)), [(a, _corta(m)) for a, m in errores],
                   ', '.join(notas))


def _mensaje(e) -> str:
    if isinstance(e, dict):
        return str(e.get('message') or e.get('msg') or json.dumps(e, ensure_ascii=False))
    return str(e)


def leer_tsc(texto: str, codigo: int | None) -> Lectura:
    errores = re.findall(r'^(.+?\(\d+,\d+\)): error (TS\d+: .*)$', texto, re.M)
    ok = codigo == 0
    fallos = [(a, _corta(b)) for a, b in errores] or ([] if ok else _ultimas(texto))
    return Lectura(ok, None, 0 if ok else max(1, len(errores)), fallos)


def leer_ruff(texto: str, codigo: int | None) -> Lectura:
    errores = re.findall(r'^(\S.*?:\d+:\d+): (.+)$', texto, re.M)
    ok = codigo == 0
    return Lectura(ok, None, 0 if ok else max(1, len(errores)), [(a, _corta(b)) for a, b in errores])


def leer_cargo(texto: str, codigo: int | None) -> Lectura:
    pasados = _cuenta(texto, 'passed')
    fallidos = _cuenta(texto, 'failed')
    fallos = [(m, '') for m in re.findall(r'^test (\S+) \.\.\. FAILED$', texto, re.M)]
    ok = codigo == 0
    return Lectura(ok, pasados + fallidos if 'test result:' in texto else None,
                   0 if ok else max(fallidos, len(fallos), 1), fallos or ([] if ok else _ultimas(texto)))


def leer_go(texto: str, codigo: int | None) -> Lectura:
    fallos = [(m, '') for m in re.findall(r'^\s*--- FAIL: (\S+)', texto, re.M)]
    paquetes = len(re.findall(r'^ok\s+\S+', texto, re.M))
    ok = codigo == 0
    return Lectura(ok, None, 0 if ok else max(len(fallos), 1), fallos or ([] if ok else _ultimas(texto)),
                   f'{paquetes} paquetes' if paquetes else '')


def leer_dotnet(texto: str, codigo: int | None) -> Lectura:
    total = sum(int(x) for x in re.findall(r'Total:\s*(\d+)', texto))
    fallidos = sum(int(x) for x in re.findall(r'Failed:\s*(\d+)', texto))
    fallos = [(m, '') for m in re.findall(r'^\s*Failed (\S+) \[', texto, re.M)]
    ok = codigo == 0
    return Lectura(ok, total or None, 0 if ok else max(fallidos, len(fallos), 1),
                   fallos or ([] if ok else _ultimas(texto)))


def leer_generico(texto: str, codigo: int | None) -> Lectura:
    ok = codigo == 0
    return Lectura(ok, None, 0 if ok else 1, [] if ok else _ultimas(texto))


def _ultimas(texto: str, n: int = 3) -> list[tuple[str, str]]:
    return [('', _corta(x)) for x in [y for y in texto.splitlines() if y.strip()][-n:]]


def _unicos(fallos: list[tuple[str, str]]) -> list[tuple[str, str]]:
    vistos, salida = set(), []
    for f in fallos:
        if f[0] not in vistos:
            vistos.add(f[0])
            salida.append(f)
    return salida


LECTORES: dict[str, Callable[[str, 'int | None'], Lectura]] = {
    'pytest': leer_pytest, 'unittest': leer_unittest, 'vitest': leer_vitest, 'jest': leer_jest,
    'playwright': leer_playwright, 'claude_test': leer_claude_test, 'claude_validate': leer_claude_validate,
    'tsc': leer_tsc, 'ruff': leer_ruff, 'cargo': leer_cargo, 'go': leer_go, 'dotnet': leer_dotnet, 'generico': leer_generico}


# ── El resumen ──

@dataclass
class Resultado:
    """Lo que dio una comprobación entera (todas sus partes)."""
    comprobacion: Comprobacion
    ok: bool
    segundos: float
    total: int | None
    fallidos: int
    fallos: list[tuple[str, str]]
    nota: str
    problema: str = ''  # «no terminó en N s» o «no se pudo lanzar: …»
    salidas: list[Salida] = field(default_factory=list)


def juntar_salidas(salidas: list[Salida]) -> list[Resultado]:
    por: dict[str, list[Salida]] = {}
    for s in salidas:
        por.setdefault(s.parte.comprobacion.nombre, []).append(s)
    resultados = []
    for ss in por.values():
        c = ss[0].parte.comprobacion
        lector = LECTORES.get(c.lector, leer_generico)
        lecturas = [lector(s.texto, s.codigo) for s in ss if not s.no_lanzada and not s.agotada]
        problema = ''
        if any(s.no_lanzada for s in ss):
            problema = 'no se pudo lanzar: ' + next(s.no_lanzada for s in ss if s.no_lanzada)
        elif any(s.agotada for s in ss):
            problema = 'no terminó a tiempo' if all(s.segundos == 0 for s in ss if s.agotada) else (
                f'no terminó en {round(max(s.segundos for s in ss if s.agotada))} s')
        totales = [x.total for x in lecturas if x.total is not None]
        for x, s in zip(lecturas, [s for s in ss if not s.no_lanzada and not s.agotada]):
            if not x.ok:
                x.fallidos = max(1, x.fallidos)
                if not x.fallos:
                    x.fallos = _ultimas(s.texto)
        resultados.append(Resultado(
            c, not problema and all(x.ok for x in lecturas), sum(s.segundos for s in ss),
            sum(totales) if totales else None, sum(x.fallidos for x in lecturas),
            [f for x in lecturas for f in x.fallos], next((x.nota for x in lecturas if x.nota), ''), problema, ss))
    return resultados


def segundos(s: float) -> str:
    if s < 100:
        return f'{round(s)} s'
    minutos, resto = divmod(round(s), 60)
    return f'{minutos} min' + (f' {resto} s' if resto else '')


def hora(iso: str) -> str:
    return iso[11:16] if len(iso) >= 16 else iso


def lineas_resumen(ctx: Contexto, elecciones: list[Eleccion], resultados: list[Resultado], sin_cubrir: list[str],
                   paredes: dict[str, float], log: str) -> list[str]:
    """Pocas líneas: una por grupo que corrió (Comprobado o Falla, con sus fallos debajo), una por grupo que se
    saltó entero (Sin lanzar) y las que avisan."""
    lineas = []
    if ctx.proyecto.aviso:
        lineas.append(f'Aviso: {ctx.proyecto.aviso}')
    grupos: dict[str, list[Eleccion]] = {}
    for e in elecciones:
        grupos.setdefault(e.comprobacion.grupo, []).append(e)
    por_nombre = {r.comprobacion.nombre: r for r in resultados}
    fallan, pasan, saltan = [], [], []
    for grupo, es in sorted(grupos.items()):
        corridos = [por_nombre[e.comprobacion.nombre] for e in es if e.comprobacion.nombre in por_nombre]
        saltados = [e for e in es if not e.corre]
        if corridos:
            (pasan if all(r.ok for r in corridos) else fallan).append(
                _linea_grupo(grupo, es, corridos, saltados, paredes.get(grupo, 0.0)))
        if saltados and not corridos:
            cuantos = f'{len(es)} archivos de ' if len(es) > 1 else ''
            saltan.append(f'Sin lanzar: {cuantos}{grupo}: {_motivos(saltados)}')
        elif saltados:
            saltan.append(f'Sin lanzar: {len(saltados)} de {len(es)} archivos de {grupo}: {_motivos(saltados)}')
    for bloque in fallan:
        lineas += bloque
    for bloque in pasan:
        lineas += bloque
    lineas += saltan
    if sin_cubrir:
        muestra = ', '.join(sin_cubrir[:3]) + (f' y {len(sin_cubrir) - 3} más' if len(sin_cubrir) > 3 else '')
        sin_decir = any(e.comprobacion.cubre is None for e in elecciones)
        lineas.append(f'Sin ningún test que diga cubrirlo: {muestra}'
                      + (' (corren los que no dicen qué cubren)' if sin_decir else ''))
    if not elecciones:
        lineas.append('Sin comprobaciones: no se ha detectado ningún test ni comprobación en este proyecto')
    if log:
        lineas.append(f'Log: {log}')
    return lineas


def _cuantos(grupo: str, n: int, de: int | None = None) -> str:
    """«38 tests de Python (backend)» o «claude plugin test (plugins/sf): 528 tests», con «1 de» si hace falta."""
    cifra = f'{n} de {de}' if de is not None else f'{n}'
    if grupo.startswith('tests de'):
        return f'{cifra} {"test" + grupo[5:] if n == 1 and de is None else grupo}'
    return f'{grupo}: {cifra} test' + ('' if n == 1 and de is None else 's')


def _linea_grupo(grupo: str, es: list[Eleccion], corridos: list[Resultado], saltados: list[Eleccion],
                 pared: float) -> list[str]:
    total = sum(r.total for r in corridos if r.total is not None)
    hay_total = any(r.total is not None for r in corridos)
    fallidos = sum(r.fallidos for r in corridos)
    en = f', en {len(corridos)} de {len(es)} archivos' if len(es) > 1 and saltados else ''
    tiempo = f' · {segundos(pared)}'
    notas = sorted({r.nota for r in corridos if r.nota})
    nota = f' ({"; ".join(notas)})' if notas else ''
    if all(r.ok for r in corridos):
        if hay_total:
            return [f'Comprobado: {_cuantos(grupo, total)}{en}, sin fallos{nota}{tiempo}']
        return [f'Comprobado: {grupo}{en}, sin errores{nota}{tiempo}']
    problemas = [f'{r.comprobacion.nombre}: {r.problema}' for r in corridos if r.problema]
    cabeza = f'Falla: {_cuantos(grupo, fallidos, total)}' if hay_total and total else f'Falla: {grupo}'
    bloque = [cabeza + en + tiempo]
    fallos = [f for r in corridos if not r.ok for f in r.fallos]
    for nombre, error in fallos[:FALLOS_MOSTRADOS]:
        if nombre:
            bloque.append(f'  {nombre}')
        if error:
            bloque.append(f'    {error}' if nombre else f'  {error}')
    if len(fallos) > FALLOS_MOSTRADOS:
        bloque.append(f'  … y {len(fallos) - FALLOS_MOSTRADOS} más (en el log)')
    bloque += [f'  {p}' for p in problemas]
    return bloque


def _motivos(saltados: list[Eleccion]) -> str:
    sin_cambios = [e for e in saltados if e.motivo.startswith('nada')]
    pasadas = [e for e in saltados if e.motivo.startswith('ya pasó')]
    if len(saltados) == 1:
        return saltados[0].motivo
    cuando = max((e.motivo.rsplit(' ', 1)[-1] for e in pasadas), default='')
    if not pasadas:
        return 'nada de lo que cubren cambió'
    if not sin_cambios:
        return f'ya pasaron sin cambios (la última, a las {cuando})'
    return (f'{len(sin_cambios)}, nada de lo que cubren cambió; '
            f'{len(pasadas)} ya pasaron sin cambios (la última, a las {cuando})')


# ── La caché, los logs y la orden ──

def carpeta_tmp() -> Path:
    c = Path(os.environ.get('SF_COMPROBAR_TMP') or Path(tempfile.gettempdir()) / 'sf-comprobar')
    c.mkdir(parents=True, exist_ok=True)
    return c


def archivo_cache(tmp: Path, raiz: Path) -> Path:
    clave = hashlib.sha256(str(raiz.resolve()).lower().encode('utf-8')).hexdigest()[:16]
    return tmp / f'cache-{clave}.json'


def leer_cache(ruta: Path) -> dict:
    try:
        datos = json.loads(ruta.read_text(encoding='utf-8'))
        return datos if isinstance(datos, dict) else {}
    except (OSError, ValueError):
        return {}


def guardar_cache(ruta: Path, cache: dict) -> None:
    tmp = ruta.with_suffix(f'.{os.getpid()}.tmp')
    tmp.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding='utf-8')
    os.replace(tmp, ruta)


def ruta_visible(ruta: Path) -> str:
    """La ruta del log como se enseña: con ~ en lugar de la carpeta del usuario, para que no salga su nombre."""
    casa = Path.home()
    try:
        return str(Path('~') / ruta.resolve().relative_to(casa.resolve()))
    except ValueError:
        return str(ruta)


def escribir_log(tmp: Path, ctx: Contexto, elecciones: list[Eleccion], salidas: list[Salida],
                 sin_cubrir: list[str]) -> Path:
    ahora = datetime.datetime.now()
    ruta = tmp / f'{ahora:%Y-%m-%d-%H%M%S}-{os.getpid()}.log'
    trozos = [f'comprobar.py · {ahora:%Y-%m-%d %H:%M:%S} · {ctx.raiz.name}',
              f'base: {ctx.base} · todo: {ctx.todo} · sin caché: {ctx.sin_cache} · trabajos: {ctx.trabajos}', '']
    cambiados = ctx.proyecto.cambiados
    trozos.append('Cambiados: ' + ('todos' if cambiados is None else str(len(cambiados))))
    trozos += [f'  {c}' for c in (cambiados or [])[:300]]
    trozos += ['', 'Ronda 1, selección:']
    for e in elecciones:
        trozos.append(f'  {"corre" if e.corre else "salta"}  {e.comprobacion.nombre} [{e.comprobacion.origen}]'
                      f': {e.motivo}')
    if sin_cubrir:
        trozos += ['', 'Sin ningún test que diga cubrirlos:'] + [f'  {r}' for r in sin_cubrir]
    trozos += ['', 'Ronda 2, ejecución:']
    for s in salidas:
        orden = s.parte.orden if isinstance(s.parte.orden, str) else subprocess.list2cmdline(s.parte.orden)
        estado = 'no lanzada: ' + s.no_lanzada if s.no_lanzada else 'agotada' if s.agotada else f'código {s.codigo}'
        trozos += ['', '=' * 100, f'{s.parte.etiqueta} · {estado} · {s.segundos:.1f} s',
                   f'$ {orden}', f'(en {s.parte.comprobacion.carpeta or "."})', '-' * 100, s.texto.rstrip()]
    ruta.write_text('\n'.join(trozos) + '\n', encoding='utf-8')
    logs = sorted(tmp.glob('*.log'))
    for viejo in logs[:-LOGS_GUARDADOS]:
        try:
            viejo.unlink()
        except OSError:
            pass
    return ruta


def comprobar(raiz: Path, base: str = 'develop', todo: bool = False, sin_cache: bool = False,
              solo_seleccion: bool = False, archivos: list[str] | None = None, trabajos: int | None = None,
              plazo: float = PLAZO_TOTAL) -> dict:
    """Las dos rondas. Devuelve lo que se enseña: las líneas, la selección, los resultados, el log y el código."""
    tmp = carpeta_tmp()
    proyecto = Proyecto(raiz, base, archivos, todo)
    ctx = Contexto(raiz, proyecto, base, todo, sin_cache, trabajos or os.cpu_count() or 4, tmp)
    ruta_cache = archivo_cache(tmp, raiz)
    cache = leer_cache(ruta_cache)
    comprobaciones = juntar(ctx)
    elecciones, sin_cubrir = seleccionar(ctx, comprobaciones, cache)
    seleccion = [{'nombre': e.comprobacion.nombre, 'grupo': e.comprobacion.grupo, 'corre': e.corre,
                  'motivo': e.motivo, 'origen': e.comprobacion.origen, 'cubre': e.comprobacion.cubre}
                 for e in elecciones]
    if solo_seleccion:
        lineas = [f'{"corre" if e.corre else "salta"}  {e.comprobacion.nombre}: {e.motivo}' for e in elecciones]
        if sin_cubrir:
            lineas.append(f'Sin ningún test que diga cubrirlo: {", ".join(sin_cubrir)}')
        return {'lineas': lineas, 'seleccion': seleccion, 'sin_cubrir': sin_cubrir, 'resultados': [],
                'log': None, 'codigo': 0}
    elegidas = [e.comprobacion for e in elecciones if e.corre]
    duraciones = cache.get('duraciones', {})
    tiempos = cache.get('tiempos', {})
    partes = preparar(ctx, elegidas, duraciones, tiempos)
    inicio = time.monotonic()
    salidas = ejecutar(ctx, partes, plazo - (time.monotonic() - inicio) - 5)
    resultados = juntar_salidas(salidas)
    paredes = _paredes(salidas)
    ahora = datetime.datetime.now().isoformat(timespec='seconds')
    pasadas = cache.setdefault('pasadas', {})
    huellas = {e.comprobacion.nombre: e.huella for e in elecciones}
    for r in resultados:
        nombre = r.comprobacion.nombre
        if r.ok:
            pasadas[nombre] = {'huella': huellas[nombre], 'hora': hora(ahora), 'fecha': ahora}
        else:
            pasadas.pop(nombre, None)
        if not r.problema:
            duraciones[nombre] = round(r.segundos, 1)
        if r.comprobacion.lector == 'pytest':
            medidos = {}
            for s in r.salidas:
                medidos.update(tiempos_pytest(r.comprobacion, s.texto))
            tiempos[nombre] = {**tiempos.get(nombre, {}), **medidos}
    cache['duraciones'] = duraciones
    cache['tiempos'] = tiempos
    guardar_cache(ruta_cache, cache)
    log = escribir_log(tmp, ctx, elecciones, salidas, sin_cubrir)
    for funcion in AL_TERMINAR:
        funcion(ctx, resultados)
    visible = ruta_visible(log)
    lineas = lineas_resumen(ctx, elecciones, resultados, sin_cubrir, paredes, visible)
    codigo = 0 if all(r.ok for r in resultados) else 1
    return {'lineas': lineas, 'seleccion': seleccion, 'sin_cubrir': sin_cubrir, 'codigo': codigo,
            'log': str(log), 'log_visible': visible, 'cambiados': proyecto.cambiados,
            'resultados': [{'nombre': r.comprobacion.nombre, 'grupo': r.comprobacion.grupo, 'ok': r.ok,
                            'segundos': round(r.segundos, 1), 'total': r.total, 'fallidos': r.fallidos,
                            'fallos': [list(f) for f in r.fallos], 'nota': r.nota, 'problema': r.problema,
                            'partes': len(r.salidas)} for r in resultados]}


def _paredes(salidas: list[Salida]) -> dict[str, float]:
    """El tiempo de reloj de cada grupo: del primero que empezó al último que acabó (las partes van a la vez)."""
    por: dict[str, tuple[float, float]] = {}
    for s in salidas:
        if not s.fin:
            continue
        g = s.parte.comprobacion.grupo
        a, b = por.get(g, (s.inicio, s.fin))
        por[g] = (min(a, s.inicio), max(b, s.fin))
    return {g: b - a for g, (a, b) in por.items()}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog='comprobar.py', description=__doc__.split('\n\n')[0])
    ap.add_argument('--repo', default='.', help='el proyecto (por defecto, la carpeta actual)')
    ap.add_argument('--base', default='develop', help='la rama con la que se compara lo cambiado')
    ap.add_argument('--todo', action='store_true', help='todas las comprobaciones, sin seleccionar')
    ap.add_argument('--sin-cache', action='store_true', help='sin fiarse de lo que ya pasó')
    ap.add_argument('--seleccion', action='store_true', help='solo la ronda 1: qué correría y por qué')
    ap.add_argument('--archivos', nargs='+', help='los archivos cambiados, en lugar de compararlos con la base')
    ap.add_argument('--trabajos', type=int, help='partes a la vez (por defecto, los núcleos)')
    ap.add_argument('--plazo', type=float, default=PLAZO_TOTAL, help='segundos para todo (570)')
    ap.add_argument('--json', action='store_true', help='la salida en JSON')
    a = ap.parse_args(argv)
    codigo, raiz = git(Path(a.repo), 'rev-parse', '--show-toplevel')
    if codigo:
        print(f'No es un repositorio git: {a.repo}', file=sys.stderr)
        return 2
    r = comprobar(Path(raiz.strip()), a.base, a.todo, a.sin_cache, a.seleccion, a.archivos, a.trabajos, a.plazo)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        print('\n'.join(r['lineas']))
    return r['codigo']


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
