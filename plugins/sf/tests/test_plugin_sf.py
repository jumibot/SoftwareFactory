"""Pruebas de tools/plugin_sf.py (si el plugin sf está al día y ponerlo al día), con una instalación de mentira.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"
"""
import contextlib
import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERRAMIENTA = Path(__file__).resolve().parents[1] / 'tools' / 'plugin_sf.py'
_spec = importlib.util.spec_from_file_location('plugin_sf', HERRAMIENTA)
ps = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ps)

LS_REMOTE = 'abc\trefs/tags/v1.6.0\nabd\trefs/tags/v1.7.6\nabe\trefs/tags/v1.7.6^{}\nabf\trefs/tags/v1.10.0-rc\n'


class PluginSf(unittest.TestCase):
    def setUp(self):
        self.base = Path(tempfile.mkdtemp())
        self.config = self.base / 'claude'
        self.proyecto = self.base / 'Contador'
        self.proyecto.mkdir()
        (self.config / 'plugins').mkdir(parents=True)
        self.corre = self.base / 'corre'
        self.plugin_json(self.corre, '1.6.0')
        self.ordenes = []
        self.fallan = set()
        self.remoto = LS_REMOTE
        self.parches = [mock.patch.dict(os.environ, {'CLAUDE_CONFIG_DIR': str(self.config)}),
                        mock.patch.object(ps, 'RAIZ_PLUGIN', self.corre),
                        mock.patch.object(ps, 'ejecutar', self.ejecutar)]
        for p in self.parches:
            p.start()
        self.escribir('known_marketplaces.json', {'softwarefactory': {'source': {'source': 'github', 'repo': 'jumibot/SoftwareFactory'}}})
        self.instalar({'sf@softwarefactory': [self.entrada('user', '1.6.0')]})

    def tearDown(self):
        for p in reversed(self.parches):
            p.stop()
        shutil.rmtree(self.base, ignore_errors=True)

    def plugin_json(self, carpeta, version, deps=()):
        (carpeta / '.claude-plugin').mkdir(parents=True, exist_ok=True)
        (carpeta / '.claude-plugin' / 'plugin.json').write_text(
            json.dumps({'name': 'sf', 'version': version, 'dependencies': list(deps)}), encoding='utf-8')

    def escribir(self, nombre, datos):
        (self.config / 'plugins' / nombre).write_text(json.dumps(datos), encoding='utf-8')

    def instalar(self, plugins):
        self.escribir('installed_plugins.json', {'version': 2, 'plugins': plugins})

    def entrada(self, scope, version, carpeta=None):
        e = {'scope': scope, 'version': version, 'installPath': str(self.base / 'cache' / scope / version)}
        if scope != 'user':
            e['projectPath'] = str(carpeta or self.proyecto)
        return e

    def ejecutar(self, argv, cwd):
        self.ordenes.append(' '.join(argv))
        if argv[:2] == ['git', 'ls-remote']:
            return (0, self.remoto) if self.remoto is not None else (128, 'fatal: sin red')
        return (1, 'error de prueba') if argv[-1] in self.fallan or ' '.join(argv) in self.fallan else (0, 'ok')

    def orden(self, *args):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(io.StringIO()):
            codigo = ps.main([*args, '--json', '--raiz', str(self.proyecto)])
        return codigo, json.loads(salida.getvalue().strip().splitlines()[-1])

    def test_atrasado_pide_actualizar(self):
        codigo, r = self.orden('ver')
        self.assertEqual(codigo, 0)
        self.assertEqual((r['estado'], r['publicada'], r['instalada'], r['atrasados']), ('actualizar', '1.7.6', '1.6.0', ['user']))
        self.assertIn('git ls-remote --tags https://github.com/jumibot/SoftwareFactory.git', self.ordenes)

    def test_al_dia(self):
        self.plugin_json(self.corre, '1.7.6')
        self.instalar({'sf@softwarefactory': [self.entrada('user', '1.7.6')]})
        self.assertEqual(self.orden('ver')[1]['estado'], 'al_dia')

    def test_instalada_mas_nueva_que_la_que_corre_pide_refrescar(self):
        self.instalar({'sf@softwarefactory': [self.entrada('user', '1.7.6')]})
        self.assertEqual(self.orden('ver')[1]['estado'], 'refrescar')

    def test_sin_red_no_se_sabe(self):
        self.remoto = None
        self.assertEqual(self.orden('ver')[1]['estado'], 'desconocido')

    def test_scopes_de_otra_carpeta_no_cuentan(self):
        self.instalar({'sf@softwarefactory': [self.entrada('local', '1.0.0', self.base / 'Otro')]})
        self.assertEqual(self.orden('ver')[1]['estado'], 'sin_instalar')

    def test_scope_local_de_la_carpeta_atrasado(self):
        self.instalar({'sf@softwarefactory': [self.entrada('user', '1.7.6'), self.entrada('local', '1.5.0')]})
        self.assertEqual(self.orden('ver')[1]['atrasados'], ['local'])

    def test_desde_la_copia_de_trabajo_no_compara_la_que_corre(self):
        (self.base / '.git').mkdir()
        self.instalar({'sf@softwarefactory': [self.entrada('user', '1.7.6')]})
        with mock.patch.object(ps, 'RAIZ_PLUGIN', self.base / 'plugins' / 'sf'):
            r = self.orden('ver')[1]
        self.assertEqual((r['corre'], r['estado']), (None, 'al_dia'))
        self.assertIn('copia de trabajo', r['mensaje'])

    def test_actualizar_catalogo_scope_y_dependencias_que_faltan(self):
        self.plugin_json(self.base / 'cache' / 'user' / '1.6.0', '1.7.6', ['oklch-skill@softwarefactory', 'gsap-skills'])
        self.instalar({'sf@softwarefactory': [self.entrada('user', '1.6.0')],
                       'gsap-skills@softwarefactory': [self.entrada('user', '1.0.0')]})
        codigo, r = self.orden('actualizar')
        self.assertEqual((codigo, r['estado']), (0, 'reiniciar'))
        self.assertEqual(r['hecho'], ['claude plugin marketplace update softwarefactory',
                                      'claude plugin update sf@softwarefactory --scope user',
                                      'claude plugin install oklch-skill@softwarefactory --scope user'])
        self.assertIn('reinicia Claude Code', r['mensaje'])

    def test_actualizar_para_en_el_primer_fallo(self):
        self.fallan = {'softwarefactory'}
        codigo, r = self.orden('actualizar')
        self.assertEqual((codigo, r['ok'], r['hecho']), (1, False, []))
        self.assertFalse(any('plugin update' in o for o in self.ordenes))

    def test_actualizar_al_dia_no_hace_nada(self):
        self.plugin_json(self.corre, '1.7.6')
        self.instalar({'sf@softwarefactory': [self.entrada('user', '1.7.6')]})
        codigo, r = self.orden('actualizar')
        self.assertEqual((codigo, r['estado'], r['hecho']), (0, 'al_dia', []))
        self.assertFalse(any(o.startswith('claude') for o in self.ordenes))

    def test_sin_instalacion_legible_sale_con_2(self):
        (self.config / 'plugins' / 'installed_plugins.json').unlink()
        self.assertEqual(self.orden('ver')[0], 2)


if __name__ == '__main__':
    unittest.main()
