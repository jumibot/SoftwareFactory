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
        self.orden('anotar', '4', 'Sin choques')
        self.assertEqual(self.guardado()['actual'], 1, 'anotar otro paso no mueve el actual')
        self.orden('anotar', 'plugin', 'Al día, 1.7.6')
        self.orden('anotar', 'caso', 'Existente')
        self.orden('anotar', 'Diagnóstico', 'falta .sf/\ny develop')
        d = self.guardado()
        self.assertEqual(d['actual'], 5, 'salta Reglas del proyecto, que ya tiene respuesta')
        self.assertEqual(d['pasos'][2]['respuesta'], 'falta .sf/ · y develop')

    def test_paso_vuelve_atras(self):
        self.orden('empezar', 'nuevo', '--raiz', str(self.proyecto))
        self.orden('anotar', '1', 'Al día')
        self.orden('anotar', '2', 'Nuevo')
        self.orden('anotar', '3', 'De acuerdo')
        codigo, r = self.orden('paso', 'repositorio')
        self.assertEqual((codigo, self.guardado()['actual']), (0, 3))
        self.assertIn('paso 3 de 8, Repositorio', r['mensaje'])

    def test_al_final_actual_es_cero(self):
        self.orden('empezar', 'diagnosticar', '--raiz', str(self.proyecto))
        for i in range(1, len(inc.PASOS['diagnosticar']) + 1):
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
        self.assertEqual(inc.clave(r'C:\Proyectos\Ejemplo/'), 'c__proyectos_ejemplo')
        self.assertEqual(inc.clave('/sf'), '_sf')
        self.assertEqual(inc.clave('/srv/Año'), '_srv_a_o')

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

    # ── Tarea 366: no perder lo respondido, el paso de las reglas y la recarga sin escribir la orden ──
    def a_medias(self):
        self.orden('empezar', 'existente', '--raiz', str(self.proyecto))
        for paso, texto in (('Plugin', 'Al día'), ('Caso', 'Existente'), ('Diagnóstico', 'falta .sf/'),
                            ('Reglas del proyecto', '1 choque: commits'), ('Repositorio', 'De acuerdo'),
                            ('Identidad', 'PoseTracker · verde')):
            self.orden('anotar', paso, texto)

    def test_reglas_del_proyecto_antes_de_preguntar_y_el_repositorio_antes_que_la_identidad(self):
        for caso in ('existente', 'actualizar', 'diagnosticar'):
            pasos = inc.PASOS[caso]
            self.assertEqual(pasos.index('Reglas del proyecto'), pasos.index('Diagnóstico') + 1, caso)
        for caso in ('nuevo', 'existente'):
            pasos = inc.PASOS[caso]
            self.assertLess(pasos.index('Repositorio'), pasos.index('Identidad'), caso)

    def test_volver_a_anotar_el_plugin_no_borra_lo_respondido(self):
        self.a_medias()
        self.orden('paso', 'Plugin')
        self.orden('anotar', 'Plugin', 'Actualizado a la 1.8.1')
        d = self.guardado()
        self.assertEqual(d['actual'], 7, 'sigue en el primer paso sin respuesta, Convenciones')
        self.assertEqual([p['respuesta'] for p in d['pasos'][1:6]],
                         ['Existente', 'falta .sf/', '1 choque: commits', 'De acuerdo', 'PoseTracker · verde'])
        # Volver a empezar el mismo caso (al pedir de nuevo la incorporación) tampoco borra nada.
        self.orden('empezar', 'existente', '--raiz', str(self.proyecto))
        self.assertEqual((self.guardado()['actual'], self.guardado()['pasos'][5]['respuesta']), (7, 'PoseTracker · verde'))

    def test_borrar_a_medias_guarda_lo_respondido_y_recuperar_lo_trae(self):
        self.a_medias()
        codigo, r = self.orden('borrar')
        self.assertIn('queda guardado', r['mensaje'])
        codigo, r = self.orden('ver')
        self.assertEqual(codigo, 2)
        self.assertIn('Hay respuestas guardadas de una incorporación anterior (existente, 6 pasos respondidos', r['mensaje'])
        # Se empieza de nuevo (otra sesión) y se recupera: lo anotado ahora manda.
        self.orden('empezar', 'existente', '--raiz', str(self.proyecto))
        self.orden('anotar', 'Plugin', 'Actualizado a la 1.8.1')
        codigo, r = self.orden('recuperar')
        self.assertEqual(codigo, 0)
        d = self.guardado()
        self.assertEqual((d['pasos'][0]['respuesta'], d['pasos'][5]['respuesta'], d['actual']),
                         ('Actualizado a la 1.8.1', 'PoseTracker · verde', 7))
        self.assertFalse(inc.archivo_guardado(inc.carpeta_de(str(self.proyecto))).exists(), 'lo guardado se gasta')
        self.assertEqual(self.orden('recuperar')[0], 2)

    def test_lo_vaciado_por_el_mod_se_recupera_de_su_copia(self):
        # El mod deja el progreso en {} y copia antes lo respondido en .guardada.json (borrarIncorporacion).
        self.a_medias()
        guardada = inc.archivo_guardado(inc.carpeta_de(str(self.proyecto)))
        guardada.write_text(self.ruta.read_text(encoding='utf-8'), encoding='utf-8')
        self.ruta.write_text('{}', encoding='utf-8')
        self.assertEqual(self.orden('recuperar')[0], 0)
        self.assertEqual(self.guardado()['actual'], 7)

    def test_borrar_sin_guardar_y_lo_terminado_no_se_guardan(self):
        self.a_medias()
        self.orden('borrar')
        self.orden('empezar', 'existente', '--raiz', str(self.proyecto))
        self.orden('borrar', '--sin-guardar')
        guardada = inc.archivo_guardado(inc.carpeta_de(str(self.proyecto)))
        self.assertFalse(guardada.exists(), 'empezar de nuevo quita también lo guardado')
        self.orden('empezar', 'diagnosticar', '--raiz', str(self.proyecto))
        for i in range(1, len(inc.PASOS['diagnosticar']) + 1):
            self.orden('anotar', str(i), 'hecho')
        self.orden('borrar')
        self.assertFalse(guardada.exists(), 'una terminada no se guarda')

    def test_recargar_deja_la_marca_para_el_mod_y_anotar_la_quita(self):
        self.a_medias()
        d = self.guardado()
        d['pausa'] = True
        self.ruta.write_text(json.dumps(d), encoding='utf-8')
        codigo, r = self.orden('recargar')
        self.assertEqual(codigo, 0)
        self.assertIn('recarga los plugins', r['mensaje'])
        d = self.guardado()
        self.assertEqual((d.get('recargar'), 'pausa' in d, d['actual']), (True, False, 7))
        self.orden('anotar', 'Convenciones', 'español')
        self.assertNotIn('recargar', self.guardado())

    def test_sin_config_va_a_la_carpeta_del_usuario(self):
        with mock.patch.dict(os.environ, {'CLAUDE_CONFIG_DIR': ''}):
            self.assertEqual(inc.carpeta_sf(), Path.home() / '.claude' / 'sf')


if __name__ == '__main__':
    unittest.main()
