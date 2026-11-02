"""Pruebas de tools/configuracion.py (ver y detectar, solo lee), sobre repositorios temporales.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"
"""
import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

HERRAMIENTA = Path(__file__).resolve().parents[1] / 'tools' / 'configuracion.py'
_spec = importlib.util.spec_from_file_location('configuracion', HERRAMIENTA)
configuracion = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(configuracion)


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        raise AssertionError(f'git {" ".join(args)}: {r.stderr}')
    return r.stdout.strip()


BUENA = {'sf': '1.5.0', 'proyecto': 'Demo', 'descripcion': 'Un proyecto de prueba', 'color': 'blue',
         'metodologia': False, 'idioma': 'es', 'commits': 'libre', 'remoto': 'origin', 'rama_main': 'main',
         'manifiesto': None}


class Configuracion(unittest.TestCase):
    def setUp(self):
        self.base = Path(tempfile.mkdtemp())
        self.repo = self.base / 'Demo'
        self.repo.mkdir()
        git(self.repo, 'init', '-q', '-b', 'main')
        git(self.repo, 'config', 'user.email', 'prueba@example.com')
        git(self.repo, 'config', 'user.name', 'Prueba')
        git(self.repo, 'commit', '-q', '--allow-empty', '-m', 'feat: uno')
        git(self.repo, 'branch', 'develop')
        git(self.repo, 'remote', 'add', 'origin', 'https://github.com/prueba/demo.git')

    def tearDown(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def escribir(self, datos):
        (self.repo / '.sf').mkdir(exist_ok=True)
        (self.repo / '.sf' / 'proyecto.json').write_text(json.dumps(datos), encoding='utf-8')

    def test_sin_problemas(self):
        self.escribir(BUENA)
        codigo, r = configuracion.o_ver(self.repo)
        self.assertEqual((codigo, r['problemas']), (0, []))
        self.assertEqual(r['por_defecto'], ['kanban', 'coautor'])
        self.assertIsNone(r['vale']['coautor'])
        self.assertTrue(all(r['vale']['automatizaciones'].values()))

    def test_coautor(self):
        self.escribir({**BUENA, 'coautor': 'Ana <ana@example.com>'})
        codigo, r = configuracion.o_ver(self.repo)
        self.assertEqual((codigo, r['vale']['coautor']), (0, 'Co-Authored-By: Ana <ana@example.com>'))
        self.escribir({**BUENA, 'coautor': ['no']})
        self.assertIn('coautor: no se entiende', '\n'.join(configuracion.o_ver(self.repo)[1]['problemas']))

    def test_sin_incorporar_o_sin_git(self):
        self.assertEqual(configuracion.o_ver(self.repo)[0], 2)
        otra = self.base / 'sin-git'
        otra.mkdir()
        self.assertEqual(configuracion.o_ver(otra)[0], 2)
        self.assertEqual(configuracion.o_detectar(otra)[0], 2)

    def test_problemas(self):
        (self.repo / 'web').mkdir()
        (self.repo / 'web' / 'package.json').write_text('{"name": "x"}', encoding='utf-8')
        git(self.repo, 'remote', 'add', 'gl', 'https://gitlab.com/prueba/demo.git')
        self.escribir({**BUENA, 'color': 'purple', 'descripcion': 'x' * 121, 'kanban': 'JKanban', 'commits': 'raro',
                       'remoto': 'gl', 'rama_main': 'master', 'manifiesto': ['web/package.json', 'no/pyproject.toml'],
                       'automatizaciones': {'orquestacion': False, 'otra': True, 'avisos_subagentes': 'no'}})
        codigo, r = configuracion.o_ver(self.repo)
        self.assertEqual(codigo, 1)
        texto = '\n'.join(r['problemas'])
        for esperado in ('color: purple', 'descripcion: 121', 'kanban: en la forma antigua', 'commits: no se entiende',
                         'gl no apunta a GitHub', 'la rama master no existe', 'web/package.json no tiene versión',
                         'no existe no/pyproject.toml', 'no se conoce el interruptor otra',
                         'automatizaciones.avisos_subagentes'):
            self.assertIn(esperado, texto)
        self.assertEqual(r['vale']['kanban'], {'proveedor': 'jkanban', 'proyecto': 'JKanban'})
        self.assertFalse(r['vale']['automatizaciones']['orquestacion'])

    def test_remoto_que_no_existe_y_develop_solo_en_el_remoto(self):
        git(self.repo, 'update-ref', 'refs/remotes/origin/develop', 'HEAD')
        git(self.repo, 'branch', '-D', 'develop')
        self.escribir({**BUENA, 'remoto': 'upstream'})
        texto = '\n'.join(configuracion.o_ver(self.repo)[1]['problemas'])
        self.assertIn('no existe el remoto upstream', texto)
        self.assertIn('la rama develop no existe en local (sí en origin)', texto)

    def test_detectar(self):
        for i in range(3):
            git(self.repo, 'commit', '-q', '--allow-empty', '-m', f'fix: arreglo {i}')
        git(self.repo, 'commit', '-q', '--allow-empty', '-m', 'Otra cosa (12)\n\nCo-Authored-By: Ana <a@x.com>')
        git(self.repo, 'checkout', '-q', 'develop')
        git(self.repo, 'merge', '-q', 'main')
        git(self.repo, 'config', 'branch.develop.remote', 'origin')
        git(self.repo, 'remote', 'add', 'gl', 'git@gitlab.com:prueba/demo.git')
        (self.repo / 'pyproject.toml').write_text('[project]\nname = "x"\nversion = "0.3.1"\n', encoding='utf-8')
        (self.repo / 'web').mkdir()
        (self.repo / 'web' / 'package.json').write_text('{"version": "1.2.0"}', encoding='utf-8')
        (self.repo / 'node_modules').mkdir()
        (self.repo / 'node_modules' / 'package.json').write_text('{"version": "9.9.9"}', encoding='utf-8')
        vecino = self.base / 'Vecino' / '.sf'
        vecino.mkdir(parents=True)
        (vecino / 'proyecto.json').write_text('{"proyecto": "Vecino", "color": "green"}', encoding='utf-8')
        codigo, r = configuracion.o_detectar(self.repo)
        self.assertEqual(codigo, 0)
        self.assertEqual({x['nombre']: x['github'] for x in r['remotos']}, {'origin': True, 'gl': False})
        self.assertEqual(r['siguen'], {'develop': 'origin'})
        self.assertEqual(r['ramas']['master'], {'local': False, 'remotos': []})
        self.assertTrue(r['ramas']['develop']['local'])
        self.assertEqual(r['manifiestos'], [{'ruta': 'pyproject.toml', 'version': '0.3.1'},
                                            {'ruta': 'web/package.json', 'version': '1.2.0'}])
        self.assertEqual((r['commits']['mirados'], r['commits']['conventional'], r['commits']['con_numero_al_final']),
                         (5, 4, 1))
        self.assertEqual(r['commits']['propuesto'], 'conventional')
        self.assertEqual(r['coautoria'], {'mirados': 5, 'con_linea': 1, 'mas_usada': 'Co-Authored-By: Ana <a@x.com>'})
        self.assertEqual(r['colores']['usados'], {'green': ['Vecino']})
        self.assertNotIn('green', r['colores']['libres'])
        self.assertNotIn('purple', r['colores']['libres'])

    def test_salida_en_texto_y_json(self):
        self.escribir(BUENA)
        for orden in ('ver', 'detectar'):
            salida = io.StringIO()
            with contextlib.redirect_stdout(salida):
                codigo = configuracion.main([orden, '--repo', str(self.repo), '--json'])
            self.assertEqual(codigo, 0)
            json.loads(salida.getvalue())
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            configuracion.main(['ver', '--repo', str(self.repo)])
        self.assertIn('Problemas: ninguno', salida.getvalue())
        self.assertIn('kanban: null  (por defecto', salida.getvalue())

    def test_no_escribe(self):
        self.escribir(BUENA)
        antes = (self.repo / '.sf' / 'proyecto.json').read_bytes()
        estado = git(self.repo, 'status', '--porcelain')
        configuracion.o_ver(self.repo)
        configuracion.o_detectar(self.repo)
        self.assertEqual((self.repo / '.sf' / 'proyecto.json').read_bytes(), antes)
        self.assertEqual(git(self.repo, 'status', '--porcelain'), estado)


if __name__ == '__main__':
    unittest.main()
