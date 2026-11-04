"""Pruebas de tools/incorporacion.py (el progreso de una incorporación, para el panel), en carpetas temporales.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"
"""
import contextlib
import importlib.util
import io
import json
import os
import shutil
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

HERRAMIENTA = Path(__file__).resolve().parents[1] / 'tools' / 'incorporacion.py'
_spec = importlib.util.spec_from_file_location('incorporacion', HERRAMIENTA)
inc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(inc)


class Incorporacion(unittest.TestCase):
    def setUp(self):
        self.base = Path(tempfile.mkdtemp())
        self.config = self.base / 'claude'
        self.proyecto = self.base / 'Contador'
        self.proyecto.mkdir()
        self.entorno = mock.patch.dict(os.environ, {'CLAUDE_CONFIG_DIR': str(self.config),
                                                    'CLAUDE_CODE_SESSION_ID': 'ses/1'})
        self.ruta = self.config / 'sf' / f'incorporacion-{inc.clave(inc.carpeta_de(str(self.proyecto)))}.json'
        self.entorno.start()

    def tearDown(self):
        self.entorno.stop()
        shutil.rmtree(self.base, ignore_errors=True)

    def orden(self, *args):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida), contextlib.redirect_stderr(io.StringIO()):
            codigo = inc.main(['--json', *args, *([] if '--raiz' in args else ['--raiz', str(self.proyecto)])])
        return codigo, json.loads(salida.getvalue().strip().splitlines()[-1])

    def guardado(self):
        return json.loads(self.ruta.read_text(encoding='utf-8'))

    def test_empezar_con_los_pasos_del_caso(self):
        codigo, r = self.orden('empezar', 'nuevo', '--raiz', str(self.proyecto))
        self.assertEqual(codigo, 0)
        d = self.guardado()
        self.assertEqual([p['nombre'] for p in d['pasos']], inc.PASOS['nuevo'])
        self.assertEqual((d['actual'], d['caso'], d['version']), (1, 'nuevo', 1))
        self.assertEqual(d['carpeta'], inc.normal(str(self.proyecto.resolve())))
        self.assertNotIn('\\', d['carpeta'])
        self.assertTrue(all(p['respuesta'] is None for p in d['pasos']))

    def test_anotar_pasa_al_siguiente_sin_respuesta(self):
        self.orden('empezar', 'existente', '--raiz', str(self.proyecto))
        self.orden('anotar', '4', 'Contador · verde')
        self.assertEqual(self.guardado()['actual'], 1, 'anotar otro paso no mueve el actual')
        self.orden('anotar', 'plugin', 'Al día, 1.7.6')
        self.orden('anotar', 'caso', 'Existente')
        self.orden('anotar', 'Diagnóstico', 'falta .sf/\ny develop')
        d = self.guardado()
        self.assertEqual(d['actual'], 5, 'salta la Identidad, que ya tiene respuesta')
        self.assertEqual(d['pasos'][2]['respuesta'], 'falta .sf/ · y develop')

    def test_paso_vuelve_atras(self):
        self.orden('empezar', 'nuevo', '--raiz', str(self.proyecto))
        self.orden('anotar', '1', 'Al día')
        self.orden('anotar', '2', 'Nuevo')
        self.orden('anotar', '3', 'Contador')
        codigo, r = self.orden('paso', 'identidad')
        self.assertEqual((codigo, self.guardado()['actual']), (0, 3))
        self.assertIn('paso 3 de 8, Identidad', r['mensaje'])

    def test_al_final_actual_es_cero(self):
        self.orden('empezar', 'diagnosticar', '--raiz', str(self.proyecto))
        for i in (1, 2, 3, 4):
            self.orden('anotar', str(i), 'hecho')
        self.assertEqual(self.guardado()['actual'], 0)

    def test_cambiar_de_caso_conserva_lo_dicho(self):
        self.orden('empezar', 'existente', '--raiz', str(self.proyecto))
        self.orden('anotar', 'Plugin', 'Al día')
        self.orden('anotar', 'Caso', 'Nuevo')
        self.orden('empezar', 'nuevo', '--raiz', str(self.proyecto))
        d = self.guardado()
        self.assertEqual((d['caso'], d['pasos'][1]['respuesta'], d['actual']), ('nuevo', 'Nuevo', 3))

    def test_anotar_quita_la_pausa(self):
        self.orden('empezar', 'nuevo', '--raiz', str(self.proyecto))
        ruta = self.ruta
        d = self.guardado()
        d['pausa'] = True
        ruta.write_text(json.dumps(d), encoding='utf-8')
        self.orden('paso', '1')
        self.assertNotIn('pausa', self.guardado())

    def test_vaciado_por_el_mod_vale_como_sin_progreso(self):
        ruta = self.ruta
        ruta.parent.mkdir(parents=True)
        ruta.write_text('{}', encoding='utf-8')
        self.assertEqual(self.orden('ver')[0], 2)

    def test_el_plugin_primero_en_todos_los_casos(self):
        self.assertTrue(all(pasos[0] == 'Plugin' and pasos.count('Plugin') == 1 for pasos in inc.PASOS.values()))

    def test_otra_carpeta_empieza_de_cero_sin_tocar_la_primera(self):
        otra = self.base / 'Otra'
        otra.mkdir()
        self.orden('empezar', 'nuevo', '--raiz', str(self.proyecto))
        self.orden('anotar', '1', 'Nuevo')
        codigo, r = self.orden('empezar', 'nuevo', '--raiz', str(otra))
        self.assertIsNone(r['progreso']['pasos'][0]['respuesta'])
        self.assertEqual(self.guardado()['pasos'][0]['respuesta'], 'Nuevo')

    def test_no_depende_de_la_sesion(self):
        self.orden('empezar', 'nuevo')
        self.orden('anotar', '1', 'Al día')
        with mock.patch.dict(os.environ, {'CLAUDE_CODE_SESSION_ID': 'otra'}):
            codigo, r = self.orden('ver')
        self.assertEqual((codigo, r['progreso']['pasos'][0]['respuesta']), (0, 'Al día'))
        with mock.patch.dict(os.environ, {'CLAUDE_CODE_SESSION_ID': ''}):
            self.assertEqual(self.orden('ver')[0], 0)

    def test_clave_como_la_del_mod(self):
        self.assertEqual(inc.clave(r'D:\Projectes\Contador/'), 'd__projectes_contador')
        self.assertEqual(inc.clave('/sf'), '_sf')
        self.assertEqual(inc.clave('/home/Año'), '_home_a_o')

    def test_pasos_propios(self):
        self.orden('empezar', 'otro', '--pasos', 'Uno', 'Dos', '--raiz', str(self.proyecto))
        self.assertEqual([p['nombre'] for p in self.guardado()['pasos']], ['Uno', 'Dos'])

    def test_errores(self):
        self.assertEqual(self.orden('ver')[0], 2)
        self.assertEqual(self.orden('empezar', 'raro', '--raiz', str(self.proyecto))[0], 1)
        self.orden('empezar', 'nuevo', '--raiz', str(self.proyecto))
        self.assertEqual(self.orden('paso', '9')[0], 1)
        self.assertEqual(self.orden('paso', 'Nada')[0], 1)
        self.assertEqual(self.orden('anotar', '1', '  ')[0], 1)

    def test_respuesta_larga_recortada(self):
        self.orden('empezar', 'nuevo', '--raiz', str(self.proyecto))
        self.orden('anotar', '1', 'x' * 1000)
        r = self.guardado()['pasos'][0]['respuesta']
        self.assertEqual(len(r), inc.LARGO_RESPUESTA)
        self.assertTrue(r.endswith('…'))

    def test_borrar(self):
        self.orden('empezar', 'nuevo', '--raiz', str(self.proyecto))
        self.assertEqual(self.orden('borrar'), (0, {'ok': True, 'mensaje': 'Progreso de la incorporación borrado.'}))
        self.assertFalse(self.ruta.exists())
        self.assertEqual(self.orden('borrar')[0], 0)

    def test_borra_las_viejas_de_otras_sesiones(self):
        carpeta = self.config / 'sf'
        carpeta.mkdir(parents=True)
        vieja, reciente = carpeta / 'incorporacion-vieja.json', carpeta / 'incorporacion-reciente.json'
        for p in (vieja, reciente):
            p.write_text('{}', encoding='utf-8')
        hace = time.time() - (inc.DIAS_VIEJAS + 1) * 86_400
        os.utime(vieja, (hace, hace))
        self.orden('empezar', 'nuevo', '--raiz', str(self.proyecto))
        self.assertEqual((vieja.exists(), reciente.exists()), (False, True))

    def test_sin_config_va_a_la_carpeta_del_usuario(self):
        with mock.patch.dict(os.environ, {'CLAUDE_CONFIG_DIR': ''}):
            self.assertEqual(inc.carpeta_sf(), Path.home() / '.claude' / 'sf')


if __name__ == '__main__':
    unittest.main()
