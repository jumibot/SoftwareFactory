"""Pruebas de tools/comprobar.py: detectar las comprobaciones de un proyecto, seleccionar por lo cambiado, la caché,
lanzar a la vez (con los archivos lentos partidos), leer cada runner y el resumen, sobre repositorios temporales.

python -I -X utf8 -m pytest plugins/sf/tests/test_comprobar.py
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

HERRAMIENTA = Path(__file__).resolve().parents[1] / 'tools' / 'comprobar.py'
_spec = importlib.util.spec_from_file_location('comprobar_sf', HERRAMIENTA)
comprobar = importlib.util.module_from_spec(_spec)
sys.modules['comprobar_sf'] = comprobar  # las dataclasses buscan su módulo en sys.modules
_spec.loader.exec_module(comprobar)


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        raise AssertionError(f'git {" ".join(args)}: {r.stderr}')
    return r.stdout.strip()


MODULO = '''\
from pathlib import Path
OTRO = Path(__file__).resolve().parent / 'otro.py'

def doble(x):
    return 2 * x
'''
TEST_MODULO = '''\
import importlib.util
import unittest
from pathlib import Path

RUTA = Path(__file__).resolve().parents[1] / 'herramienta' / 'modulo.py'
_spec = importlib.util.spec_from_file_location('modulo', RUTA)
modulo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(modulo)


class Doble(unittest.TestCase):
    def test_dos(self):
        self.assertEqual(modulo.doble(1), 2)

    def test_tres(self):
        self.assertEqual(modulo.doble(2), 4)
'''
TEST_SOLO = '''\
import unittest


class Solo(unittest.TestCase):
    def test_suma(self):
        self.assertEqual(1 + 1, 2)
'''
TEST_DATOS = '''\
import json
import unittest
from pathlib import Path

DATOS = Path(__file__).resolve().parents[1] / 'datos'


class Datos(unittest.TestCase):
    def test_todos_son_json(self):
        for f in DATOS.glob('*.json'):
            json.loads(f.read_text(encoding='utf-8'))
'''


class Repo(unittest.TestCase):
    """Un proyecto de Python con tres archivos de tests, en develop y en una rama de tarea."""

    def setUp(self):
        self.base = Path(tempfile.mkdtemp())
        self.tmp = self.base / 'tmp'
        self.repo = self.base / 'Demo'
        self.repo.mkdir()
        self._env = mock.patch.dict(os.environ, {'SF_COMPROBAR_TMP': str(self.tmp)})
        self._env.start()
        git(self.repo, 'init', '-q', '-b', 'develop')
        git(self.repo, 'config', 'user.email', 'prueba@example.com')
        git(self.repo, 'config', 'user.name', 'Prueba')
        git(self.repo, 'config', 'core.autocrlf', 'false')
        self.escribir('herramienta/modulo.py', MODULO)
        self.escribir('herramienta/otro.py', 'X = 1\n')
        self.escribir('datos/a.json', '{"a": 1}\n')
        self.escribir('README.md', 'Demo\n')
        self.escribir('tests/test_modulo.py', TEST_MODULO)
        self.escribir('tests/test_solo.py', TEST_SOLO)
        self.escribir('tests/test_datos.py', TEST_DATOS)
        self.escribir('.gitignore', '__pycache__/\n')
        git(self.repo, 'add', '-A')
        git(self.repo, 'commit', '-q', '-m', 'uno')
        git(self.repo, 'checkout', '-q', '-b', 'feature/1-algo')

    def tearDown(self):
        self._env.stop()
        shutil.rmtree(self.base, ignore_errors=True)

    def escribir(self, ruta: str, texto: str):
        p = self.repo / ruta
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(texto, encoding='utf-8', newline='\n')

    def seleccion(self, **kw):
        r = comprobar.comprobar(self.repo, solo_seleccion=True, trabajos=2, **kw)
        return {e['nombre'].split('/')[-1] if e['nombre'].startswith(('pytest', 'unittest')) else e['nombre']: e
                for e in r['seleccion']}, r

    def correr(self, **kw):
        return comprobar.comprobar(self.repo, trabajos=2, **kw)


class Detectar(Repo):
    def test_un_archivo_de_tests_por_comprobacion_con_lo_que_cubre(self):
        sel, _ = self.seleccion(todo=True)
        self.assertEqual(sorted(sel), ['test_datos.py', 'test_modulo.py', 'test_solo.py'])
        cubre = sel['test_modulo.py']['cubre']
        # lo que nombra el test, y de forma transitiva lo que nombra el módulo
        for r in ('tests/test_modulo.py', 'herramienta/modulo.py', 'herramienta/otro.py', 'tests/conftest.py'):
            self.assertIn(r, cubre)
        self.assertNotIn('datos/a.json', cubre)
        self.assertEqual(sel['test_datos.py']['grupo'], 'tests de Python (tests)')
        self.assertIn('datos/*.json', sel['test_datos.py']['cubre'])  # el glob sobre una ruta de __file__
        self.assertIsNone(sel['test_solo.py']['cubre'])  # no nombra nada del proyecto: corre siempre

    def test_sin_tests_lo_dice(self):
        for t in ('test_modulo.py', 'test_solo.py', 'test_datos.py'):
            (self.repo / 'tests' / t).unlink()
        r = self.correr()
        self.assertEqual(r['codigo'], 0)
        self.assertIn('Sin comprobaciones: no se ha detectado ningún test ni comprobación en este proyecto',
                      r['lineas'])

    def test_node_con_el_runner_y_su_filtro(self):
        self.escribir('web/package.json', json.dumps({'scripts': {'test': 'vitest', 'typecheck': 'tsc --noEmit',
                                                                  'lint': 'eslint .'}}))
        bin_ = self.repo / 'web' / 'node_modules' / '.bin'
        bin_.mkdir(parents=True)
        for nombre in ('vitest', 'vitest.cmd'):
            (bin_ / nombre).write_text('', encoding='utf-8')
        self.escribir('otro/package.json', json.dumps({'scripts': {'test': 'echo "Error: no test specified" && exit 1'}}))
        git(self.repo, 'add', 'web/package.json', 'otro/package.json')
        proyecto = comprobar.Proyecto(self.repo)
        ctx = comprobar.Contexto(self.repo, proyecto, 'develop', False, False, 2, self.tmp)
        cs = {c.nombre: c for c in comprobar.detectar_node(ctx)}
        self.assertEqual(sorted(cs), ['npm run lint (web)', 'npm run typecheck (web)', 'vitest (web)'])
        v = cs['vitest (web)']
        self.assertEqual((v.lector, v.carpeta, v.orden[1:], v.filtro), ('vitest', 'web', ['run'], ['--changed', '{base}']))
        partes = comprobar.preparar(ctx, [v], {})
        self.assertEqual(partes[0].orden[-2:], ['--changed', 'develop'])
        ctx.todo = True  # en la pasada completa, sin filtro
        self.assertEqual(comprobar.preparar(ctx, [v], {})[0].orden[1:], ['run'])

    def test_plugin_de_claude_code(self):
        self.escribir('mod/.claude-plugin/plugin.json', '{"name": "mod"}')
        self.escribir('mod/tests/a.test.ts', '')
        proyecto = comprobar.Proyecto(self.repo, todo=True)
        ctx = comprobar.Contexto(self.repo, proyecto, 'develop', False, False, 2, self.tmp)
        with mock.patch.object(comprobar.shutil, 'which', return_value='claude'):
            cs = {c.nombre: c for c in comprobar.detectar_plugins(ctx)}
        self.assertEqual(sorted(cs), ['claude plugin test (mod)', 'claude plugin validate (mod)'])
        self.assertEqual(cs['claude plugin validate (mod)'].orden, ['claude', 'plugin', 'validate', 'mod', '--json'])
        self.assertTrue(comprobar.patron(cs['claude plugin test (mod)'].cubre[0]).match('mod/hooks/panel.tsx'))

    def test_cargo_en_un_workspace_una_sola_vez(self):
        self.escribir('Cargo.toml', '[workspace]\nmembers = ["core"]\n')
        self.escribir('core/Cargo.toml', '[package]\nname = "core"\n')
        self.escribir('go/go.mod', 'module x\n')
        proyecto = comprobar.Proyecto(self.repo, todo=True)
        ctx = comprobar.Contexto(self.repo, proyecto, 'develop', False, False, 2, self.tmp)
        cs = {c.nombre: c for c in comprobar.detectar_compilados(ctx)}
        self.assertEqual(sorted(cs), ['cargo test', 'go test (go)'])
        self.assertEqual(cs['cargo test'].orden, ['cargo', 'test', '--workspace'])


class Seleccionar(Repo):
    def test_corre_lo_que_toca_lo_cambiado_y_lo_que_no_dice_que_cubre(self):
        self.escribir('herramienta/otro.py', 'X = 2\n')  # sin commit: también cuenta
        sel, r = self.seleccion()
        self.assertEqual((sel['test_modulo.py']['corre'], sel['test_modulo.py']['motivo']),
                         (True, 'toca herramienta/otro.py'))
        self.assertEqual((sel['test_solo.py']['corre'], sel['test_solo.py']['motivo']), (True, 'no dice qué cubre'))
        self.assertEqual((sel['test_datos.py']['corre'], sel['test_datos.py']['motivo']),
                         (False, 'nada de lo que cubre cambió'))
        self.assertEqual(r['sin_cubrir'], [])

    def test_lo_cambiado_en_la_rama_frente_a_develop(self):
        self.escribir('datos/b.json', '{}\n')
        git(self.repo, 'add', '-A')
        git(self.repo, 'commit', '-q', '-m', 'dos')
        sel, _ = self.seleccion()
        self.assertTrue(sel['test_datos.py']['corre'])
        self.assertFalse(sel['test_modulo.py']['corre'])

    def test_lo_que_no_cubre_ningun_test_se_avisa(self):
        self.escribir('README.md', 'Demo 2\n')
        _, r = self.seleccion()
        self.assertEqual(r['sin_cubrir'], ['README.md'])

    def test_determinista(self):
        self.escribir('herramienta/modulo.py', MODULO + '\n')
        self.assertEqual(self.seleccion()[1]['seleccion'], self.seleccion()[1]['seleccion'])

    def test_archivos_nombrados_en_lugar_de_la_rama(self):
        sel, _ = self.seleccion(archivos=[str(self.repo / 'datos' / 'a.json')])
        self.assertTrue(sel['test_datos.py']['corre'])
        self.assertFalse(sel['test_modulo.py']['corre'])

    def test_sin_develop_lanza_todo(self):
        git(self.repo, 'branch', '-m', 'develop', 'otra')
        sel, r = self.seleccion()
        self.assertTrue(all(e['corre'] for e in sel.values()))
        self.assertEqual(r['seleccion'][0]['motivo'], 'todo')


class Ejecutar(Repo):
    def test_pasa_y_la_cache_lo_salta_la_vez_siguiente(self):
        self.escribir('herramienta/otro.py', 'X = 2\n')
        r = self.correr()
        self.assertEqual(r['codigo'], 0, r['lineas'])
        self.assertRegex(r['lineas'][0], r'^Comprobado: 3 tests de Python \(tests\), en 2 de 3 archivos, sin fallos · \d+ s$')
        self.assertEqual(r['lineas'][1], 'Sin lanzar: 1 de 3 archivos de tests de Python (tests): nada de lo que cubre cambió')
        self.assertTrue(r['lineas'][-1].startswith('Log: '))
        self.assertTrue(Path(r['log']).is_file())
        segunda = self.correr()
        self.assertEqual(segunda['resultados'], [])
        self.assertRegex(segunda['lineas'][0], r'^Sin lanzar: 3 archivos de tests de Python \(tests\): 1, nada de lo '
                                               r'que cubren cambió; 2 ya pasaron sin cambios \(la última, a las \d\d:\d\d\)$')
        self.assertEqual(len(self.correr(sin_cache=True)['resultados']), 2)
        self.escribir('herramienta/otro.py', 'X = 3\n')  # otro hash: vuelve a correr
        self.assertEqual(len(self.correr()['resultados']), 2)

    def test_todo_sin_cache_lanza_todo(self):
        r = self.correr(todo=True, sin_cache=True)
        self.assertEqual(r['codigo'], 0, r['lineas'])
        self.assertEqual(len(r['resultados']), 3)
        self.assertRegex(r['lineas'][0], r'^Comprobado: 4 tests de Python \(tests\), sin fallos')

    def test_un_fallo_con_su_nombre_y_su_error(self):
        self.escribir('herramienta/modulo.py', MODULO.replace('2 * x', '3 * x'))
        r = self.correr()
        self.assertEqual(r['codigo'], 1)
        self.assertRegex(r['lineas'][0], r'^Falla: 2 de 3 tests de Python \(tests\), en 2 de 3 archivos · \d+ s$')
        self.assertIn('  tests/test_modulo.py::Doble::test_dos', r['lineas'])
        self.assertIn('    AssertionError: 3 != 2', r['lineas'])
        # lo que falla no queda en la caché
        self.assertEqual(len(self.correr()['resultados']), 1)

    def test_archivo_lento_partido_en_trozos(self):
        self.escribir('tests/test_lento.py', 'import unittest\n\n\n' + ''.join(
            f'class C{i}(unittest.TestCase):\n    def test_a(self):\n        pass\n\n    def test_b(self):\n        pass\n\n\n'
            for i in range(3)))
        cache = comprobar.archivo_cache(comprobar.carpeta_tmp(), self.repo)
        cache.write_text(json.dumps({'duraciones': {'pytest tests/test_lento.py': 100}}), encoding='utf-8')
        r = comprobar.comprobar(self.repo, todo=True, trabajos=3)
        self.assertEqual(r['codigo'], 0, r['lineas'])
        lento = next(x for x in r['resultados'] if x['nombre'] == 'pytest tests/test_lento.py')
        self.assertEqual((lento['partes'], lento['total']), (3, 6))  # una clase entera por trozo
        self.assertIn('Comprobado: 10 tests de Python (tests), sin fallos', r['lineas'][0])

    def test_sin_terminar_y_sin_poder_lanzar(self):
        def fuente(ctx):
            return [comprobar.Comprobacion('espera', 'espera', [sys.executable, '-c', 'import time; time.sleep(60)'],
                                           plazo=2),
                    comprobar.Comprobacion('no existe', 'no existe', ['orden-que-no-existe-sf']),
                    comprobar.Comprobacion('pytest *', 'nada', [sys.executable, '-c', ''], sustituye=['pytest *'])]
        comprobar.registrar_fuente(10, 'declarado', fuente)
        try:
            r = self.correr(todo=True)
        finally:
            comprobar.FUENTES[:] = [f for f in comprobar.FUENTES if f[2] is not fuente]
        self.assertEqual(r['codigo'], 1)
        self.assertEqual(sorted(x['nombre'] for x in r['resultados']), ['espera', 'no existe', 'pytest *'])
        texto = '\n'.join(r['lineas'])
        self.assertRegex(texto, r'Falla: espera · \d+ s\n  espera: no terminó en \d+ s')
        self.assertIn('  no existe: no se pudo lanzar', texto)
        self.assertIn('Comprobado: nada, sin errores', texto)
        self.assertTrue(all(e['origen'] == 'declarado' for e in r['seleccion']))


class Fuentes(Repo):
    def test_manda_la_de_mas_prioridad(self):
        declarada = comprobar.Comprobacion('pytest tests/test_solo.py', 'declarados', ['x'], cubre=['tests/**'])

        def fuente(ctx):
            return [declarada]
        comprobar.registrar_fuente(10, 'declarado', fuente)
        try:
            sel, _ = self.seleccion(todo=True)
        finally:
            comprobar.FUENTES[:] = [f for f in comprobar.FUENTES if f[2] is not fuente]
        self.assertEqual((sel['test_solo.py']['grupo'], sel['test_solo.py']['origen']), ('declarados', 'declarado'))
        self.assertEqual(sel['test_modulo.py']['origen'], 'detectado')


class Repartir(unittest.TestCase):
    def test_clases_enteras_y_el_mas_largo_solo(self):
        tests = [f'a.py::C{c}::test_{t}' for c in range(4) for t in range(3)] + ['a.py::test_lento']
        tiempos = {'a.py::test_lento': 60.0, 'a.py::C0::test_0': 5.0}
        trozos = comprobar.repartir(tests, tiempos, 3, 20.0, 80.0)
        self.assertEqual(trozos[0], (['a.py::test_lento'], 60.0))
        juntos = [t for trozo, _ in trozos for t in trozo]
        self.assertEqual(sorted(juntos), sorted(tests))
        for trozo, _ in trozos:  # cada clase en un solo trozo
            clases = {t.split('::')[1] for t in trozo}
            for c in clases:
                self.assertEqual(sum(t.split('::')[1] == c for t in trozo), 3 if c.startswith('C') else 1)
        self.assertEqual(trozos, comprobar.repartir(tests, tiempos, 3, 20.0, 80.0))

    def test_tiempos_de_durations(self):
        c = comprobar.Comprobacion('pytest t/test_a.py', 'g', ['x'], archivo='t/test_a.py')
        texto = ('============ slowest durations ============\n'
                 '2.50s call     t/test_a.py::C::test_x\n'
                 '0.70s setup    t/test_a.py::C::test_x\n'
                 '1.00s call     test_a.py::test_y\n')
        self.assertEqual(comprobar.tiempos_pytest(c, texto), {'t/test_a.py::C::test_x': 3.2, 't/test_a.py::test_y': 1.0})


class Patrones(unittest.TestCase):
    def test_patrones(self):
        casos = [('src/**/*.py', 'src/a.py', True), ('src/**/*.py', 'src/x/y/a.py', True),
                 ('src/**/*.py', 'srcx/a.py', False), ('src/*.py', 'src/x/a.py', False),
                 ('docs/', 'docs/a/b.md', True), ('docs', 'docs/a.md', True), ('docs', 'docsx', False),
                 ('**/*.{ts,tsx}', 'a.tsx', True), ('**/*.{ts,tsx}', 'b/c.ts', True), ('**/*.{ts,tsx}', 'c.js', False),
                 ('./a.py', 'a.py', True), ('p/.claude-plugin/**', 'p/.claude-plugin/plugin.json', True),
                 ('t?st.py', 'test.py', True), ('**', 'x/y', True)]
        for p, ruta, sale in casos:
            with self.subTest(p=p, ruta=ruta):
                self.assertEqual(bool(comprobar.patron(p).match(ruta)), sale)


class Leer(unittest.TestCase):
    def test_salida_que_no_es_utf8_y_con_colores(self):
        self.assertEqual(comprobar.decodificar('\x1b[32mcanción ñ\x1b[0m\r\n'.encode('cp1252')).strip()[-1], 'ñ')
        self.assertEqual(comprobar.decodificar('\x1b[1A\x1b[2Kok ✓\r\n'.encode('utf-8')), 'ok ✓\n')

    def test_pytest(self):
        texto = ('..F\n=========================== short test summary info ============================\n'
                 'FAILED tests/test_a.py::C::test_x - AssertionError: 1 != 2\n1 failed, 2 passed in 0.12s\n')
        x = comprobar.leer_pytest(texto, 1)
        self.assertEqual((x.ok, x.total, x.fallidos, x.fallos),
                         (False, 3, 1, [('tests/test_a.py::C::test_x', 'AssertionError: 1 != 2')]))
        self.assertEqual(comprobar.leer_pytest('\nno tests ran in 0.01s\n', 5).nota, 'sin tests')

    def test_pytest_sin_el_error_en_el_resumen(self):
        texto = ('_________________ C.test_x _________________\n\n    def test_x(self):\n'
                 '>       self.assertEqual(1, 2)\nE       AssertionError: 1 != 2\n\n'
                 'FAILED tests/test_a.py::C::test_x\n1 failed in 0.1s\n')
        self.assertEqual(comprobar.leer_pytest(texto, 1).fallos, [('tests/test_a.py::C::test_x', 'AssertionError: 1 != 2')])

    def test_unittest(self):
        texto = ('.F\n======================================================================\n'
                 'FAIL: test_x (test_a.C.test_x)\n----------------------------------------------------------------------\n'
                 'Traceback (most recent call last):\n  File "t.py", line 3, in test_x\nAssertionError: 1 != 2\n\n'
                 '----------------------------------------------------------------------\nRan 2 tests in 0.001s\n\n'
                 'FAILED (failures=1)\n')
        x = comprobar.leer_unittest(texto, 1)
        self.assertEqual((x.total, x.fallidos, x.fallos), (2, 1, [('test_a.C.test_x', 'AssertionError: 1 != 2')]))

    # Las salidas de abajo son las de cada runner en un proyecto de prueba (sin colores).
    def test_vitest(self):
        texto = textwrap.dedent('''\
             FAIL  src/b.test.js > b falla
            AssertionError: expected 2 to be 3 // Object.is equality

             Test Files  1 failed | 1 passed (2)
                  Tests  1 failed | 2 passed (3)
            ''')
        x = comprobar.leer_vitest(texto, 1)
        self.assertEqual((x.total, x.fallidos, x.fallos),
                         (3, 1, [('src/b.test.js > b falla', 'AssertionError: expected 2 to be 3 // Object.is equality')]))
        self.assertEqual(comprobar.leer_vitest('No test files found, exiting with code 0\n', 0).nota,
                         'ningún test tocado por lo cambiado')

    def test_jest(self):
        texto = ('FAIL src/b.test.js\n  ● grupo › b falla\n\n    expect(received).toBe(expected) // Object.is equality\n\n'
                 'Tests:       1 failed, 2 passed, 3 total\n')
        x = comprobar.leer_jest(texto, 1)
        self.assertEqual((x.total, x.fallidos, x.fallos),
                         (3, 1, [('grupo › b falla', 'expect(received).toBe(expected) // Object.is equality')]))

    def test_playwright(self):
        texto = ('[3/3] tests\\b.spec.js:7:3 › grupo › b falla\n'
                 '  1) tests\\b.spec.js:7:3 › grupo › b falla ──────────────\n\n'
                 '    Error: expect(received).toBe(expected) // Object.is equality\n\n'
                 '  1 failed\n    tests\\b.spec.js:7:3 › grupo › b falla ──────\n  2 passed (571ms)\n')
        x = comprobar.leer_playwright(texto, 1)
        self.assertEqual((x.total, x.fallidos, x.fallos),
                         (3, 1, [('tests\\b.spec.js:7:3 › grupo › b falla',
                                  'Error: expect(received).toBe(expected) // Object.is equality')]))

    def test_claude_plugin_test(self):
        texto = ('tests\\a.test.ts:\n(pass) uno pasa [1.05ms]\n(fail) dos falla [0.31ms]\n'
                 '  AssertionError: expect(received).toBe()\n\n Expected: 3\n\n 1 pass\n 1 fail\n'
                 'Ran 2 tests across 1 file. [0.12s]\n')
        x = comprobar.leer_claude_test(texto, 1)
        self.assertEqual((x.total, x.fallidos, x.fallos),
                         (2, 1, [('dos falla', 'AssertionError: expect(received).toBe()')]))

    def test_claude_plugin_validate(self):
        datos = {'success': True, 'manifest': {'file': 'p/plugin.json', 'errors': [], 'warnings': []},
                 'contents': [{'file': 'p/hooks/hooks.json', 'errors': [], 'warnings': ['w']}],
                 'directory': {'findings': [{'code': 'ICON_MISSING'}]}}
        x = comprobar.leer_claude_validate(json.dumps(datos), 0)
        self.assertEqual((x.ok, x.nota), (True, '1 aviso, 1 aviso del directorio de plugins'))
        datos['success'] = False
        datos['manifest']['errors'] = [{'message': 'falta name'}]
        x = comprobar.leer_claude_validate(json.dumps(datos), 1)
        self.assertEqual((x.ok, x.fallos), (False, [('plugin.json', 'falta name')]))

    def test_ruff(self):
        x = comprobar.leer_ruff('a.py:1:8: F401 [*] `os` imported but unused\nFound 1 error.\n', 1)
        self.assertEqual(x.fallos, [('a.py:1:8', 'F401 [*] `os` imported but unused')])

    def test_tsc(self):
        x = comprobar.leer_tsc("src/a.ts(1,7): error TS2322: Type 'string' is not assignable to type 'number'.\n", 2)
        self.assertEqual(x.fallos, [('src/a.ts(1,7)', "TS2322: Type 'string' is not assignable to type 'number'.")])


class Orden(unittest.TestCase):
    def test_fuera_de_un_repositorio(self):
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run([sys.executable, '-X', 'utf8', str(HERRAMIENTA), '--repo', d],
                               capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 2)

    def test_la_ruta_del_log_sin_la_carpeta_del_usuario(self):
        ruta = Path.home() / 'AppData' / 'x.log'
        self.assertEqual(comprobar.ruta_visible(ruta), str(Path('~') / 'AppData' / 'x.log'))


if __name__ == '__main__':
    unittest.main()
