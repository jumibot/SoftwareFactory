"""Pruebas de tools/cola.py, sobre colas y repositorios temporales (nunca la cola real).

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"
"""
import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

HERRAMIENTA = Path(__file__).resolve().parents[1] / 'tools' / 'cola.py'
_spec = importlib.util.spec_from_file_location('cola', HERRAMIENTA)
cola = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cola)

# La descripción que las pruebas dan a la tarea que crea Claude, que la orden exige (tarea 326).
DESCRIPCION = 'Qué se pide y por qué.'


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        raise AssertionError(f'git {" ".join(args)}: {r.stderr}')
    return r.stdout.strip()


class Base(unittest.TestCase):
    """Un proyecto temporal con .sf/ y una cola; con git=True, además un repositorio con develop."""
    git = False

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.raiz = Path(self._tmp.name) / 'proyecto'
        (self.raiz / '.sf').mkdir(parents=True)
        self.escribir({'ultimo': 10, 'peticiones': []})
        if self.git:
            git(self.raiz, 'init', '-q', '-b', 'develop')
            git(self.raiz, 'config', 'user.name', 'Prueba')
            git(self.raiz, 'config', 'user.email', 'prueba@example.com')
            git(self.raiz, 'config', 'core.autocrlf', 'false')
            (self.raiz / '.gitignore').write_text('.sf/\n', encoding='utf-8')
            (self.raiz / 'a.txt').write_text('uno\n', encoding='utf-8')
            git(self.raiz, 'add', '.')
            git(self.raiz, 'commit', '-q', '-m', 'Inicio')

    def tearDown(self):
        self._tmp.cleanup()

    @property
    def archivo(self) -> Path:
        return self.raiz / '.sf' / 'peticiones.json'

    def escribir(self, datos: dict) -> None:
        self.archivo.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    def leer(self) -> dict:
        return json.loads(self.archivo.read_text(encoding='utf-8'))

    def tarea(self, id_: int) -> dict | None:
        return next((t for t in self.leer()['peticiones'] if t['id'] == id_), None)

    def archivadas(self) -> list:
        h = self.raiz / '.sf' / 'historial.jsonl'
        return [json.loads(x) for x in h.read_text(encoding='utf-8').splitlines()] if h.exists() else []

    def orden(self, *args: str, ok: bool = True) -> str:
        """Ejecuta cola.py en el proceso y devuelve su mensaje; comprueba si hizo el cambio."""
        return self.respuesta(*args, ok=ok)['mensaje']

    def respuesta(self, *args: str, ok: bool = True, descripcion: bool = True) -> dict:
        """Como orden, pero devuelve la respuesta JSON entera, la que lee el panel. Un «crear» o un «de-propuesta» de
        Claude sin --descripcion la recibe aquí, que la orden la exige (tarea 326); descripcion=False no la pone."""
        if descripcion and args and args[0] in ('crear', 'de-propuesta') and '--descripcion' not in args \
                and '--quien' not in args:
            args = (*args, '--descripcion', DESCRIPCION)
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            codigo = cola.main(['--raiz', str(self.raiz), '--json', *args])
        r = json.loads(salida.getvalue())
        self.assertEqual(r['ok'], ok, r['mensaje'])
        self.assertEqual(codigo, 0 if ok else 1)
        return r

    def eventos(self, t: dict) -> list:
        return [e['evento'] for e in t.get('historial', [])]

    def commit_en(self, rama: str, archivo: str, texto: str) -> None:
        git(self.raiz, 'switch', '-q', rama)
        (self.raiz / archivo).write_text(texto, encoding='utf-8')
        git(self.raiz, 'add', archivo)
        git(self.raiz, 'commit', '-q', '-m', f'Cambio en {archivo}')


class Alta(Base):
    def test_crear_da_el_siguiente_a_ultimo_y_lo_sube(self):
        self.assertIn('Creada la 11', self.orden('crear', 'Primera', '--descripcion', 'Detalle'))
        t = self.tarea(11)
        self.assertEqual((t['estado'], t['descripcion'], self.leer()['ultimo']), ('en-cola', 'Detalle', 11))
        self.assertEqual(t['historial'][0] | {'fecha': None},
                         {'evento': 'creada', 'fecha': None, 'quien': 'principal', 'via': 'cli', 'detalle': 'en-cola'})
        self.orden('crear', 'Segunda', '--en-curso')
        self.assertEqual(self.tarea(12)['estado'], 'en-curso')

    def test_crear_da_su_numero_en_la_respuesta(self):
        r = self.respuesta('crear', 'Del registro', '--quien', 'propietario', '--via', 'panel')
        self.assertEqual(r, {'ok': True, 'mensaje': 'Creada la 11, en cola: «Del registro».', 'id': 11})
        self.assertNotIn('id', self.respuesta('en-curso', '11'))

    def test_quien_y_via(self):
        self.orden('crear', 'Del panel', '--quien', 'propietario', '--via', 'panel')
        e = self.tarea(11)['historial'][0]
        self.assertEqual((e['quien'], e['via']), ('propietario', 'panel'))

    def test_claude_no_crea_sin_descripcion(self):  # tarea 326: el panel la enseña al desplegar la tarea
        for extra in ((), ('--descripcion', '  '), ('--quien', 'principal')):
            r = self.respuesta('crear', 'Sin detalle', *extra, ok=False, descripcion=False)
            self.assertIn('--descripcion', r['mensaje'])
            self.assertIn('crear "Sin detalle" --descripcion', r['mensaje'])
        self.assertEqual(self.leer()['peticiones'], [])
        self.orden('crear', 'Con detalle', '--descripcion', ' Qué y por qué. ')
        self.assertEqual(self.tarea(11)['descripcion'], 'Qué y por qué.')

    def test_el_propietario_y_el_panel_crean_sin_descripcion(self):  # tarea 326
        self.respuesta('crear', 'Del propietario', '--quien', 'propietario', descripcion=False)
        self.respuesta('crear', 'Por el panel', '--quien', 'principal', '--via', 'panel', descripcion=False)
        self.respuesta('crear', 'Desde el panel', '--quien', 'propietario', '--via', 'panel', descripcion=False)
        self.assertEqual([('descripcion' in self.tarea(n)) for n in (11, 12, 13)], [False, False, False])

    def test_los_numeros_no_se_reutilizan(self):
        self.orden('crear', 'Una')
        self.orden('eliminar', '11')
        self.escribir({'peticiones': []})  # aun perdiendo `ultimo`, el historial lo recuerda
        self.assertIn('Creada la 12', self.orden('crear', 'Otra'))

    def test_en_curso_y_en_cola(self):
        self.orden('crear', 'Una')
        self.orden('en-curso', '11')
        self.orden('en-curso', '11', ok=False)
        self.orden('en-cola', '11')
        self.assertEqual(self.eventos(self.tarea(11)), ['creada', 'en-curso', 'en-cola'])

    def test_sin_carpeta_sf_no_escribe(self):
        (self.raiz / '.sf' / 'peticiones.json').unlink()
        (self.raiz / '.sf').rmdir()
        self.assertIn('no está en la SF', self.orden('crear', 'Una', ok=False))

    def test_cola_con_ruta_de_archivo(self):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            cola.main(['--raiz', str(self.archivo), 'crear', 'Por archivo', '--descripcion', DESCRIPCION])
        self.assertEqual(self.tarea(11)['texto'], 'Por archivo')


class Pasos(Base):
    def setUp(self):
        super().setUp()
        self.orden('crear', 'Con pasos', '--en-curso')

    def test_anadir_marcar_quitar(self):
        self.orden('paso', 'añadir', '11', 'Redactar la tabla')
        self.orden('paso', 'anadir', '11', 'Revisarla')
        self.orden('paso', 'marcar', '11', '1', 'hecho', '--texto', 'Redactada la tabla')
        self.orden('paso', 'quitar', '11', '1', ok=False)  # hecho: no se quita
        self.orden('paso', 'quitar', '11', '2')
        self.orden('paso', 'quitar', '11', '5', ok=False)
        t = self.tarea(11)
        self.assertEqual(t['pasos'], [{'texto': 'Redactada la tabla', 'estado': 'hecho'},
                                      {'texto': 'Activar rama para poder probar', 'estado': 'pendiente'},
                                      {'texto': 'Cerrar la tarea', 'estado': 'pendiente'}])
        self.assertEqual(self.eventos(t).count('paso'), 4)

    def test_ver_numera_los_pasos_desde_1(self):  # tarea 253: lo que piden «paso marcar» y «paso quitar»
        self.orden('paso', 'añadir', '11', 'Uno')
        self.assertIn('Paso 2 de 4 de la 11', self.orden('paso', 'añadir', '11', 'Dos'))
        self.assertEqual([(p['n'], p['texto']) for p in json.loads(self.orden('ver', '11'))['pasos']],
                         [(1, 'Uno'), (2, 'Dos'), (3, 'Activar rama para poder probar'), (4, 'Cerrar la tarea')])
        self.assertNotIn('n', self.tarea(11)['pasos'][0])  # solo al mostrarla
        self.assertIn('Paso 2 de 4 de la 11, hecho: «Dos»', self.orden('paso', 'marcar', '11', '2', 'hecho'))

    def test_lista_cuenta_los_pasos_de_trabajo(self):  # decisión 235: ver qué tarea crece
        self.orden('crear', 'Sin pasos')
        self.assertNotIn(' · pasos', self.orden('lista'))
        self.orden('paso', 'añadir', '11', 'Uno')
        self.orden('paso', 'añadir', '11', 'Dos')
        self.orden('paso', 'marcar', '11', '1', 'hecho')
        self.orden('paso', 'añadir', '11', 'Mirar el color', '--prueba')  # ayuda: no cuenta
        lineas = self.orden('lista').splitlines()
        self.assertIn('en curso · pasos 1/2\tCon pasos', lineas[0])  # sin los de cierre
        self.assertNotIn(' · pasos', lineas[1])

    def test_los_pasos_de_cierre_no_cambian_de_texto(self):  # tarea 253
        self.orden('paso', 'añadir', '11', 'Quitar la negrita')
        self.orden('listo', '11', '--prueba', 'mirar')
        self.assertIn('de cierre', self.orden('paso', 'marcar', '11', '2', 'hecho', '--texto', 'Quitada la negrita', ok=False))
        self.assertIn('de cierre', self.orden('paso', 'marcar', '11', '1', 'hecho', '--texto', 'Cerrar la tarea', ok=False))
        self.assertIn('de cierre', self.orden('paso', 'añadir', '11', 'Activar rama para poder probar', ok=False))
        self.orden('paso', 'marcar', '11', '2', 'hecho')  # sin texto, sí
        self.assertEqual([(p['texto'], p['estado']) for p in self.tarea(11)['pasos']],
                         [('Quitar la negrita', 'pendiente'), ('Activar rama para poder probar', 'hecho'), ('Cerrar la tarea', 'pendiente')])

    def test_listo_no_repite_el_paso_de_prueba(self):  # tarea 253
        self.orden('listo', '11', '--prueba', 'mirar')
        self.orden('paso', 'añadir', '11', 'Otro')
        self.assertNotIn('Aviso', self.orden('listo', '11', '--prueba', 'mirar otra vez'))
        self.assertEqual([p['texto'] for p in self.tarea(11)['pasos']], ['Otro', 'Activar rama para poder probar', 'Cerrar la tarea'])

    def test_al_cargar_la_cola_una_en_curso_recibe_los_pasos_de_cierre(self):  # decisión 174; como quedó la 247
        self.escribir({'ultimo': 13, 'peticiones': [
            {'id': 11, 'texto': 'Reescrito', 'estado': 'en-curso', 'pasos': [
                {'texto': 'Hecho', 'estado': 'hecho'}, {'texto': 'Quitada la negrita', 'estado': 'hecho'},
                {'texto': 'Cerrar la tarea', 'estado': 'pendiente'}]},
            {'id': 12, 'texto': 'Repetido', 'estado': 'en-curso', 'pasos': [
                {'texto': 'Activar rama para poder probar', 'estado': 'hecho'}, {'texto': 'Cerrar la tarea', 'estado': 'pendiente'},
                {'texto': 'Activar rama para poder probar', 'estado': 'pendiente'}]},
            {'id': 13, 'texto': 'En cola', 'estado': 'en-cola'}]})
        self.assertEqual([(p['n'], p['texto']) for p in json.loads(self.orden('ver', '11'))['pasos']][2:],
                         [(3, 'Activar rama para poder probar'), (4, 'Cerrar la tarea')])
        self.orden('renombrar', '13', 'En cola, renombrada')  # cualquier escritura los guarda
        self.assertEqual([p['texto'] for p in self.tarea(11)['pasos']],
                         ['Hecho', 'Quitada la negrita', 'Activar rama para poder probar', 'Cerrar la tarea'])
        self.assertEqual([(p['texto'], p['estado']) for p in self.tarea(12)['pasos']],  # queda el primero, con su estado
                         [('Activar rama para poder probar', 'hecho'), ('Cerrar la tarea', 'pendiente')])
        self.assertNotIn('pasos', self.tarea(13))  # en cola, no
        self.assertNotIn('Aviso', self.orden('listo', '11', '--prueba', 'mirar'))

    def test_un_paso_nuevo_deja_pendiente_otra_vez_el_de_prueba(self):  # decisión 174
        self.orden('paso', 'añadir', '11', 'Hacer')
        self.orden('paso', 'marcar', '11', '1', 'hecho')
        self.orden('paso', 'marcar', '11', '2', 'hecho')  # activada la rama una vez
        self.assertIn('otra vez pendiente', self.orden('paso', 'añadir', '11', 'Corregir'))
        self.assertEqual([p['estado'] for p in self.tarea(11)['pasos']], ['hecho', 'pendiente', 'pendiente', 'pendiente'])
        self.assertNotIn('otra vez', self.orden('paso', 'añadir', '11', 'Más'))

    def test_paso_nuevo_antes_de_los_de_cierre(self):
        self.orden('listo', '11', '--prueba', 'mirar')
        self.orden('paso', 'añadir', '11', 'Otro')
        self.assertEqual([p['texto'] for p in self.tarea(11)['pasos']], ['Otro', 'Activar rama para poder probar', 'Cerrar la tarea'])

    def test_ayudas_de_prueba_tras_activar_la_rama(self):  # decisión 184
        self.orden('paso', 'añadir', '11', 'Hacer')
        self.orden('paso', 'marcar', '11', '1', 'hecho')
        self.orden('paso', 'marcar', '11', '2', 'hecho')  # rama activada
        r = self.orden('paso', 'añadir', '11', 'Abrir el panel', '--prueba')
        self.assertIn('Ayuda de prueba 3 de 4', r)
        self.assertNotIn('otra vez', r)
        self.orden('paso', 'añadir', '11', 'Pulsar Cerrar', '--prueba')
        self.orden('paso', 'añadir', '11', 'Corregir')  # uno de trabajo, antes de «Activar rama», que vuelve a pendiente
        self.assertEqual([(p['texto'], p['estado'], p.get('ayuda', False)) for p in self.tarea(11)['pasos']],
                         [('Hacer', 'hecho', False), ('Corregir', 'pendiente', False),
                          ('Activar rama para poder probar', 'pendiente', False), ('Abrir el panel', 'pendiente', True),
                          ('Pulsar Cerrar', 'pendiente', True), ('Cerrar la tarea', 'pendiente', False)])
        self.orden('paso', 'quitar', '11', '5')  # una ayuda se quita
        self.assertEqual(len(self.tarea(11)['pasos']), 5)

    def test_las_ayudas_quedan_entre_los_de_cierre_al_cargar(self):  # decisión 184
        self.escribir({'ultimo': 11, 'peticiones': [{'id': 11, 'texto': 'Vieja', 'estado': 'en-curso', 'pasos': [
            {'texto': 'Mirar', 'estado': 'pendiente', 'ayuda': True}, {'texto': 'Hacer', 'estado': 'hecho'},
            {'texto': 'Cerrar la tarea', 'estado': 'pendiente'}]}]})
        self.orden('renombrar', '11', 'Vieja, renombrada')  # cualquier escritura los guarda
        self.assertEqual([p['texto'] for p in self.tarea(11)['pasos']],
                         ['Hacer', 'Activar rama para poder probar', 'Mirar', 'Cerrar la tarea'])

    def test_el_paso_probar_la_tarea_se_renombra_al_escribir(self):
        # Decisión 172: las colas anteriores tienen «Probar la tarea»; la primera escritura lo renombra.
        self.escribir({'ultimo': 11, 'peticiones': [{'id': 11, 'texto': 'Vieja', 'estado': 'en-curso', 'pasos': [
            {'texto': 'Hacer', 'estado': 'pendiente'}, {'texto': 'Probar la tarea', 'estado': 'pendiente'},
            {'texto': 'Cerrar la tarea', 'estado': 'pendiente'}]}]})
        self.orden('paso', 'añadir', '11', 'Otro')
        self.assertEqual([p['texto'] for p in self.tarea(11)['pasos']],
                         ['Hacer', 'Otro', 'Activar rama para poder probar', 'Cerrar la tarea'])

    def test_paso_en_observacion_si_descartada_no(self):
        self.escribir({'ultimo': 12, 'peticiones': [{'id': 11, 'texto': 'En prueba', 'estado': 'en-observacion', 'observando': True},
                                                    {'id': 12, 'texto': 'Fuera', 'estado': 'descartada'}]})
        self.orden('paso', 'añadir', '11', 'Corregir', '--quien', 'propietario', '--via', 'panel')
        self.assertEqual(self.tarea(11)['pasos'], [{'texto': 'Corregir', 'estado': 'pendiente'}])
        self.orden('paso', 'añadir', '12', 'Nada', ok=False)

    def test_renombrar_comprobado_subagente_informe(self):
        self.orden('renombrar', '11', 'Nombre nuevo')
        self.orden('comprobado', '11', 'test pasa')
        self.orden('subagente', '11', '--worktree', '.claude/worktrees/x', '--rama', 'feature/11-a-cli')
        self.orden('informe', '11', '--interrumpido', 'falta una decisión')
        t = self.tarea(11)
        self.assertEqual(t['texto'], 'Nombre nuevo')
        self.assertNotIn('comprobado', t)
        self.assertIn({'texto': 'Comprobado: test pasa', 'estado': 'hecho'}, t['pasos'])
        self.assertEqual(self.eventos(t)[-4:], ['renombrada', 'comprobado', 'subagente', 'informe'])
        self.assertEqual(t['historial'][-1]['detalle'], 'interrumpido: falta una decisión')


    def test_redescribir(self):
        self.orden('redescribir', '11', 'Uno.\n\nDos.')
        t = self.tarea(11)
        self.assertEqual((t['descripcion'], self.eventos(t)[-1]), ('Uno.\n\nDos.', 'redescrita'))
        self.assertNotIn('detalle', t['historial'][-1])
        self.orden('redescribir', '11', ' ')
        self.assertNotIn('descripcion', self.tarea(11))

class SinGit(Base):
    def test_cerrar_sin_rama_sale_de_la_cola(self):
        self.orden('crear', 'Propuesta', '--en-curso')
        self.orden('listo', '11', '--prueba', 'leerla')
        self.orden('cerrar', '11')
        self.assertIsNone(self.tarea(11))
        a = self.archivadas()[-1]
        self.assertEqual((self.eventos(a)[-1], a['estado']), ('cerrada', 'cerrada'))
        self.assertEqual([(p['texto'], p['estado']) for p in a['pasos']],
                         [('Activar rama para poder probar', 'hecho'), ('Cerrar la tarea', 'hecho')])

    def test_una_en_curso_sin_pasos_de_cierre_se_cierra(self):  # de antes de la 174: los recibe al cargar la cola
        self.escribir({'ultimo': 11, 'peticiones': [{'id': 11, 'texto': 'Propuesta', 'estado': 'en-curso'}]})
        self.orden('cerrar', '11')
        self.assertEqual([p['estado'] for p in self.archivadas()[-1]['pasos']], ['hecho', 'hecho'])

    def test_cierre_con_paso_de_trabajo_pendiente_no(self):
        self.orden('crear', 'Propuesta', '--en-curso')
        self.orden('paso', 'añadir', '11', 'Redactarla')
        self.orden('listo', '11', '--prueba', 'leerla')
        self.assertIn('sin hacer: 1', self.orden('cerrar', '11', ok=False))
        self.assertIn('sin hacer: 1', self.orden('a-observacion', '11', ok=False))
        self.assertEqual(self.tarea(11)['estado'], 'en-curso')

    def test_los_pasos_de_cierre_no_se_quitan_y_cerrar_marca_el_de_prueba(self):  # decisión 174
        self.orden('crear', 'Propuesta', '--en-curso')
        self.assertEqual([(p['texto'], p['estado']) for p in self.tarea(11)['pasos']],
                         [('Activar rama para poder probar', 'pendiente'), ('Cerrar la tarea', 'pendiente')])
        for i in ('1', '2'):
            self.assertIn('no se quita', self.orden('paso', 'quitar', '11', i, ok=False))
        self.orden('cerrar', '11')  # sin probar: cerrar no pide «Activar rama» y lo marca
        a = self.archivadas()[-1]
        self.assertEqual((a['estado'], [p['estado'] for p in a['pasos']]), ('cerrada', ['hecho', 'hecho']))

    def test_cerrar_y_a_observacion_no_exigen_las_ayudas(self):  # decisión 184
        for texto in ('Uno', 'Dos'):
            self.orden('crear', texto, '--en-curso')
        for n in ('11', '12'):
            self.orden('paso', 'añadir', n, 'Mirar el panel', '--prueba')
        self.orden('a-observacion', '12')
        self.assertEqual([p['estado'] for p in self.tarea(12)['pasos']], ['pendiente', 'pendiente', 'hecho'])
        self.orden('cerrar', '12')
        self.orden('cerrar', '11')
        a = self.archivadas()[-1]  # la ayuda queda sin hacer, como estaba
        self.assertEqual([(p['texto'], p['estado']) for p in a['pasos']],
                         [('Activar rama para poder probar', 'hecho'), ('Mirar el panel', 'pendiente'), ('Cerrar la tarea', 'hecho')])

    def test_los_pasos_de_cierre_al_entrar_en_curso(self):  # decisión 174
        self.orden('crear', 'En cola')
        self.assertEqual(self.tarea(11).get('pasos', []), [])
        self.orden('paso', 'añadir', '11', 'Hacer')
        self.orden('en-curso', '11')
        cierre = ['Activar rama para poder probar', 'Cerrar la tarea']
        self.assertEqual([p['texto'] for p in self.tarea(11)['pasos']], ['Hacer'] + cierre)
        self.orden('en-cola', '11')
        self.orden('en-curso', '11')  # no se repiten
        self.assertEqual([p['texto'] for p in self.tarea(11)['pasos']], ['Hacer'] + cierre)
        self.orden('paso', 'añadir', '11', 'Otro')
        self.assertEqual([p['texto'] for p in self.tarea(11)['pasos']], ['Hacer', 'Otro'] + cierre)
        # split: los de cierre no se separan; la nueva, en cola, sin ellos; la de origen los conserva
        self.assertIn('de cierre', self.orden('split', '11', '2,3', ok=False))
        self.orden('paso', 'añadir', '11', 'Tercero')
        self.orden('split', '11', '2,3')
        self.assertEqual([p['texto'] for p in self.tarea(11)['pasos']], ['Hacer'] + cierre)
        self.assertEqual([p['texto'] for p in self.tarea(12)['pasos']], ['Otro', 'Tercero'])
        self.assertIn('de trabajo', self.orden('split', '11', '1', ok=False))
        # fusionar dos en curso: los de cierre, una vez y al final
        self.orden('en-curso', '12')
        self.orden('fusionar', '11', '12')
        self.assertEqual([p['texto'] for p in self.tarea(12)['pasos']], ['Hacer', 'Otro', 'Tercero'] + cierre)

    def test_la_linea_del_historial_lleva_el_estado_de_salida(self):
        for texto in ('Cerrada', 'Eliminada', 'Una', 'Dos', 'Observada'):
            self.orden('crear', texto, '--en-curso')
        self.orden('listo', '11', '--prueba', 'mirar')
        self.orden('cerrar', '11')
        self.orden('eliminar', '12')
        self.orden('fusionar', '13', '14')
        self.orden('listo', '15', '--prueba', 'mirar')
        self.orden('a-observacion', '15')
        self.orden('cerrar', '15')
        self.escribir(self.leer() | {'peticiones': self.leer()['peticiones'] + [
            {'id': 16, 'texto': 'Descartada', 'estado': 'descartada'}]})
        self.orden('limpiar')
        salida = {n: t['estado'] for n, t in cola.Cola(self.raiz, 'principal', 'cli').archivadas().items()}
        self.assertEqual(salida, {11: 'cerrada', 12: 'eliminada', 13: 'absorbida', 15: 'cerrada', 16: 'descartada'})
        self.assertEqual(json.loads(self.orden('ver', '11'))['estado'], 'cerrada')
        self.assertIn('cerrada', self.orden('en-curso', '11', ok=False))
        self.orden('restaurar', '12')
        self.assertEqual(self.tarea(12)['estado'], 'en-curso')
        self.orden('reabrir', '11', 'falla', '--en-cola')
        self.assertEqual(self.tarea(11)['estado'], 'en-cola')

    def test_observacion_observando_seguir_cerrar(self):
        self.orden('crear', 'Publicada', '--en-curso')
        self.orden('listo', '11', '--prueba', 'mirar')
        self.orden('a-observacion', '11', '--commit', 'sf 1.0', '--prueba', 'abrir el panel')
        t = self.tarea(11)
        self.assertEqual((t['estado'], t['commit'], t['prueba']), ('en-observacion', 'sf 1.0', 'abrir el panel'))
        self.orden('observando', '11')
        self.assertTrue(self.tarea(11)['observando'])
        self.orden('seguir', '11')
        self.assertNotIn('observando', self.tarea(11))
        self.orden('descartar', '11', ok=False)  # en observación se revierte, no se descarta
        self.orden('cerrar', '11')
        self.assertIsNone(self.tarea(11))
        self.assertEqual(self.eventos(self.archivadas()[-1])[-1], 'cerrada')

    def test_reobservar_solo_una_cerrada(self):
        self.orden('reobservar', '11', ok=False)  # ni en la cola ni en el historial
        self.orden('crear', 'En cola')
        self.assertIn('en cola', self.orden('reobservar', '11', ok=False))
        self.orden('eliminar', '11')
        self.assertIn('eliminada', self.orden('reobservar', '11', ok=False))
        self.orden('crear', 'Sin rama', '--en-curso')
        self.orden('listo', '12', '--prueba', 'mirar')
        self.orden('cerrar', '12')
        self.assertEqual(self.orden('reobservar', '12'), 'La 12 vuelve a observación, sin commit en develop que revertir.')
        t = self.tarea(12)
        self.assertEqual((t['estado'], 'commit' in t, self.eventos(t)[-1]), ('en-observacion', False, 'reobservada'))

    def test_eliminar_y_restaurar(self):
        self.orden('crear', 'Sobra')
        self.orden('eliminar', '11')
        self.assertIsNone(self.tarea(11))
        self.orden('reabrir', '11', 'vuelve', ok=False)  # una eliminada se restaura
        self.orden('restaurar', '11')
        self.assertEqual(self.eventos(self.tarea(11)), ['creada', 'eliminada', 'restaurada'])
        self.orden('restaurar', '11', ok=False)

    def test_eliminar_con_rama_no(self):
        self.escribir({'ultimo': 11, 'peticiones': [{'id': 11, 'texto': 'Con rama', 'estado': 'en-curso', 'rama': 'feature/11-x'}]})
        self.assertIn('descartar', self.orden('eliminar', '11', ok=False))

    def test_fusionar(self):
        self.escribir({'ultimo': 13, 'peticiones': [
            {'id': 11, 'texto': 'Una', 'estado': 'en-curso', 'descripcion': 'A.'},
            {'id': 12, 'texto': 'Dos', 'estado': 'en-cola', 'rama': 'feature/12-dos',
             'pasos': [{'texto': 'P1', 'estado': 'hecho'}, {'texto': 'P2', 'estado': 'pendiente'}]},
            {'id': 13, 'texto': 'Tres', 'estado': 'en-cola', 'descripcion': 'C.'},
        ]})
        self.assertIn('Fusionadas en la 13 las 11 y 12', self.orden('fusionar', '11', '13', '12'))
        t = self.tarea(13)
        self.assertEqual((t['estado'], t['rama'], t['descripcion']), ('en-curso', 'feature/12-dos', 'C.\n\nA.'))
        self.assertEqual([p['texto'] for p in t['pasos']], ['Una', 'P1', 'P2', 'Tres', 'Activar rama para poder probar', 'Cerrar la tarea'])
        self.assertEqual([x['id'] for x in self.leer()['peticiones']], [13])
        self.assertEqual({a['id']: self.eventos(a)[-1] for a in self.archivadas()}, {11: 'absorbida', 12: 'absorbida'})
        self.assertEqual(self.leer()['ultimo'], 13)

    def test_fusionar_rechaza(self):
        self.escribir({'ultimo': 13, 'peticiones': [
            {'id': 11, 'texto': 'Una', 'estado': 'en-curso', 'rama': 'feature/11-a'},
            {'id': 12, 'texto': 'Dos', 'estado': 'en-cola', 'rama': 'feature/12-b'},
            {'id': 13, 'texto': 'Tres', 'estado': 'en-observacion'},
        ]})
        self.orden('fusionar', '11', '12', ok=False)
        self.orden('fusionar', '11', '13', ok=False)
        self.orden('fusionar', '11', ok=False)

    def test_split(self):
        self.escribir({'ultimo': 11, 'peticiones': [{'id': 11, 'texto': 'Grande', 'estado': 'en-curso', 'pasos': [
            {'texto': 'A', 'estado': 'hecho'}, {'texto': 'B', 'estado': 'hecho'}, {'texto': 'C', 'estado': 'pendiente'}]}]})
        self.orden('split', '11', '1,2,3', ok=False)
        self.orden('split', '11', '4', ok=False)
        r = self.respuesta('split', '11', '2,3')
        self.assertEqual(r['id'], 12)
        self.assertEqual(r['mensaje'], 'Separado de la 11 los pasos 2 y 3: tarea 12, «B», en cola. '
                                       'El trabajo del paso 2, ya hecho, sigue en la rama de la 11.')
        self.assertEqual([p['texto'] for p in self.tarea(11)['pasos']], ['A', 'Activar rama para poder probar', 'Cerrar la tarea'])
        n = self.tarea(12)
        self.assertEqual((n['texto'], n['estado'], len(n['pasos'])), ('B', 'en-cola', 2))
        self.assertEqual(self.eventos(n), ['nacida'])
        self.assertEqual(self.leer()['ultimo'], 12)


class APropuesta(Base):
    """A propuesta (tarea 243): una tarea en cola vuelve a la propuesta de la que salió o pasa a una nueva. En
    sf/propuestas.md («Los documentos de la SF van en la carpeta sf/», 203)."""
    RUTA = 'sf/propuestas.md'
    MD = ('# Propuestas\n\n## Propuestas pendientes\n\n### P01 Una\n\n- **Origen:** SF, 2026-10-01.\n'
          '- **Estado:** pasada a la tarea 11 de la cola el 2026-10-31.\n\n### P07 Otra\n\n'
          '- **Estado:** propuesta, pendiente de aprobación.\n\n## Descartadas\n\n### P03 Vieja\n')

    def setUp(self):
        super().setUp()
        self.propuestas = self.raiz / self.RUTA
        self.propuestas.parent.mkdir()
        self.propuestas.write_bytes(self.MD.encode('utf-8'))

    def md(self) -> str:
        return self.propuestas.read_bytes().decode('utf-8')

    def test_vuelve_a_la_propuesta_de_la_que_salio(self):
        self.escribir({'ultimo': 11, 'peticiones': [{'id': 11, 'texto': 'Una', 'estado': 'en-cola'}]})
        r = self.respuesta('a-propuesta', '11')
        self.assertEqual(r['propuesta'], 'P01')
        self.assertEqual(self.md(), self.MD.replace('pasada a la tarea 11 de la cola el 2026-10-31.',
                                                    'propuesta, pendiente de aprobación.'))
        self.assertIsNone(self.tarea(11))
        salida = self.archivadas()[-1]
        self.assertEqual(salida['estado'], 'eliminada')
        self.assertEqual(salida['historial'][-1]['evento'], 'a-propuesta')
        self.assertEqual(salida['historial'][-1]['detalle'], 'P01 devuelta')
        self.orden('restaurar', '11', ok=False)  # la propuesta manda

    def test_la_plantilla_de_la_incorporacion_recibe_la_primera(self):
        # Decisiones 196 y 203: sf:incorporar_proyecto_a_sf crea sf/propuestas.md desde templates/propuestas.md.
        plantilla = (HERRAMIENTA.parents[1] / 'templates' / 'propuestas.md').read_text(encoding='utf-8')
        self.propuestas.write_bytes(plantilla.encode('utf-8'))
        self.escribir({'ultimo': 5, 'peticiones': [{'id': 5, 'texto': 'Primera', 'estado': 'en-cola'}]})
        self.assertEqual(self.respuesta('a-propuesta', '5')['propuesta'], 'P01')
        self.assertTrue(self.md().startswith(plantilla.rstrip('\n') + '\n\n### P01 Primera\n'))

    def test_sin_numero_por_su_titulo(self):
        self.propuestas.write_bytes(self.MD.replace('la tarea 11', 'tarea').encode('utf-8'))
        self.escribir({'ultimo': 11, 'peticiones': [{'id': 11, 'texto': 'Una', 'estado': 'en-cola'}]})
        self.assertEqual(self.respuesta('a-propuesta', '11')['propuesta'], 'P01')

    def test_nueva_con_titulo_tipo_y_descripcion_y_crlf(self):
        self.propuestas.write_bytes(self.MD.replace('\n', '\r\n').encode('utf-8'))
        self.escribir({'ultimo': 12, 'peticiones': [
            {'id': 12, 'texto': 'Nueva idea', 'estado': 'en-cola', 'tipo': 'diseñar', 'descripcion': 'Primero.\n\nSegundo.'}]})
        self.assertEqual(self.respuesta('a-propuesta', '12')['propuesta'], 'P08')  # tras la P07 (y la P03 descartada)
        md = self.md()
        self.assertNotIn('\n', md.replace('\r\n', ''))
        bloque = md.split('### P08 Nueva idea\r\n\r\n')[1].split('\r\n\r\n## Descartadas')[0]
        self.assertTrue(bloque.startswith('- **Origen:** proyecto, '))
        self.assertIn('Devuelta a propuesta desde la tarea 12 de la cola.', bloque)
        self.assertIn('- **Tipo:** diseñar.\r\n- **Cambio propuesto:** Primero.\r\n\r\n  Segundo.\r\n'
                      '- **Estado:** propuesta, pendiente de aprobación.', bloque)
        self.assertIn('pendiente de aprobación.\r\n\r\n### P08', md)
        self.assertIsNone(self.tarea(12))

    def test_nueva_sin_descripcion_ni_tipo_y_nombre_del_proyecto(self):
        (self.raiz / '.sf' / 'proyecto.json').write_text('{"proyecto": "Demo"}', encoding='utf-8')
        self.escribir({'ultimo': 12, 'peticiones': [{'id': 12, 'texto': 'Sola', 'estado': 'en-cola'}]})
        self.orden('a-propuesta', '12')
        bloque = self.md().split('### P08 Sola\n\n')[1]
        self.assertTrue(bloque.startswith('- **Origen:** Demo, '))
        self.assertNotIn('**Tipo:**', bloque.split('## Descartadas')[0])
        self.assertIn('- **Cambio propuesto:** por concretar.\n- **Estado:**', bloque)

    def test_solo_en_cola_y_sin_rama(self):
        self.escribir({'ultimo': 12, 'peticiones': [
            {'id': 11, 'texto': 'Una', 'estado': 'en-curso'},
            {'id': 12, 'texto': 'Con rama', 'estado': 'en-cola', 'rama': 'feature/12-x'}]})
        self.orden('a-propuesta', '11', ok=False)
        self.assertIn('descartar', self.orden('a-propuesta', '12', ok=False))
        self.assertEqual(self.md(), self.MD)

    def test_sin_propuestas_no_las_crea(self):
        self.propuestas.unlink()
        self.escribir({'ultimo': 11, 'peticiones': [{'id': 11, 'texto': 'Una', 'estado': 'en-cola'}]})
        self.assertIn('no lleva propuestas', self.orden('a-propuesta', '11', ok=False))
        self.assertFalse(self.propuestas.exists())
        self.propuestas.write_text('# Propuestas\n', encoding='utf-8')
        self.orden('a-propuesta', '11', ok=False)
        self.assertIsNotNone(self.tarea(11))


class APropuestaAntes(APropuesta):
    """Lo mismo en docs/propuestas.md, el sitio de antes, mientras el proyecto no se ha puesto al día (203)."""
    RUTA = 'docs/propuestas.md'

    def test_con_las_dos_manda_sf(self):
        nuevo = self.raiz / APropuesta.RUTA
        nuevo.parent.mkdir()
        nuevo.write_bytes(self.MD.encode('utf-8'))
        self.escribir({'ultimo': 11, 'peticiones': [{'id': 11, 'texto': 'Una', 'estado': 'en-cola'}]})
        self.orden('a-propuesta', '11')
        self.assertEqual(self.md(), self.MD)
        self.assertNotIn('pasada a la tarea 11', nuevo.read_text(encoding='utf-8'))


class PropuestasEnDevelop(Base):
    """propuestas.md vive en develop (tarea 273): «a-propuesta» y «de-propuesta» hacen su commit en develop, también
    con otra rama activa, y no dejan cambios sin commit en la rama activa, que impedirían cerrar su tarea."""
    git = True
    MD = APropuesta.MD
    RUTA = 'sf/propuestas.md'

    def setUp(self):
        super().setUp()
        self.propuestas = self.raiz / self.RUTA
        self.propuestas.parent.mkdir()
        self.propuestas.write_bytes(self.MD.encode('utf-8'))
        git(self.raiz, 'add', '.')
        git(self.raiz, 'commit', '-q', '-m', 'Propuestas')
        self.escribir({'ultimo': 12, 'peticiones': [{'id': 11, 'texto': 'Una', 'estado': 'en-cola'},
                                                    {'id': 12, 'texto': 'Nueva idea', 'estado': 'en-cola'}]})

    def en_develop(self) -> str:
        return git(self.raiz, 'show', f'develop:{self.RUTA}') + '\n'

    def limpio(self) -> None:
        self.assertEqual(git(self.raiz, 'status', '--porcelain', '--untracked-files=no'), '')

    def otra_rama(self) -> str:
        git(self.raiz, 'switch', '-q', '-c', 'feature/9-otra')
        (self.raiz / 'a.txt').write_text('dos\n', encoding='utf-8')
        git(self.raiz, 'commit', '-q', '-am', 'Trabajo de la 9')
        return git(self.raiz, 'rev-parse', 'HEAD')

    def test_a_propuesta_con_develop_activa(self):
        r = self.respuesta('a-propuesta', '11')
        self.assertIn(f'{self.RUTA}, en develop', r['mensaje'])
        self.limpio()
        self.assertEqual(git(self.raiz, 'log', '-1', '--format=%s'), 'P01 vuelve a propuesta desde la tarea 11 de la cola')
        self.assertIn('### P01 Una', self.en_develop())
        self.assertNotIn('pasada a la tarea 11', self.en_develop())
        self.assertEqual(self.propuestas.read_text(encoding='utf-8'), self.en_develop())

    def test_a_propuesta_con_otra_rama_activa(self):
        cabeza = self.otra_rama()
        r = self.respuesta('a-propuesta', '12')
        self.assertEqual(r['propuesta'], 'P08')
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'feature/9-otra')
        self.assertEqual(git(self.raiz, 'rev-parse', 'HEAD'), cabeza)
        self.limpio()
        self.assertEqual(self.propuestas.read_bytes().decode('utf-8'), self.MD)  # la de la rama activa, intacta
        self.assertIn('### P08 Nueva idea', self.en_develop())
        self.assertEqual(git(self.raiz, 'log', '-1', '--format=%s', 'develop'),
                         'P08 vuelve a propuesta desde la tarea 12 de la cola')
        self.assertEqual(git(self.raiz, 'show', '--name-only', '--format=', 'develop'), self.RUTA)
        self.assertEqual(git(self.raiz, 'show', 'develop:a.txt'), 'uno')
        self.assertIsNone(self.tarea(12))

    def test_de_propuesta_de_claude_sin_descripcion_no_toca_nada(self):  # tarea 326, como crear
        cabeza = git(self.raiz, 'rev-parse', 'develop')
        r = self.respuesta('de-propuesta', 'Otra', '--numero', 'P07', ok=False, descripcion=False)
        self.assertIn('--descripcion', r['mensaje'])
        self.assertEqual(git(self.raiz, 'rev-parse', 'develop'), cabeza)
        self.assertIsNone(self.tarea(13))
        # Desde el panel («A Pendientes»), sin resumen, sí.
        self.respuesta('de-propuesta', 'Otra', '--numero', 'P07', '--quien', 'propietario', '--via', 'panel',
                       descripcion=False)
        self.assertNotIn('descripcion', self.tarea(13))

    def test_de_propuesta_con_develop_activa_y_no_dos_veces(self):
        r = self.respuesta('de-propuesta', 'Otra', '--numero', 'P07', '--descripcion', 'Detalle', '--tipo', 'diseñar')
        self.assertEqual(r['id'], 13)
        self.assertEqual({k: self.tarea(13)[k] for k in ('texto', 'estado', 'descripcion', 'tipo')},
                         {'texto': 'Otra', 'estado': 'en-cola', 'descripcion': 'Detalle', 'tipo': 'diseñar'})
        self.limpio()
        self.assertEqual(git(self.raiz, 'log', '-1', '--format=%s'), 'P07 pasa a la tarea 13 de la cola')
        self.assertRegex(self.en_develop(), r'### P07 Otra\n\n- \*\*Estado:\*\* pasada a la tarea 13 de la cola el '
                                            r'\d{4}-\d\d-\d\d\.\n')
        self.assertIn('ya no está por decidir', self.orden('de-propuesta', 'Otra', '--numero', 'P07', ok=False))
        self.assertIsNone(self.tarea(14))

    def test_de_propuesta_con_otra_rama_activa(self):
        cabeza = self.otra_rama()
        self.orden('de-propuesta', 'Otra', '--numero', 'P07')
        self.assertEqual(git(self.raiz, 'rev-parse', 'HEAD'), cabeza)
        self.limpio()
        self.assertIn('pasada a la tarea 13 de la cola', self.en_develop())
        self.assertEqual(self.propuestas.read_bytes().decode('utf-8'), self.MD)
        # Se mira la de develop: la de la rama activa sigue diciendo «pendiente», pero ya no se pasa otra vez.
        self.orden('de-propuesta', 'Otra', '--numero', 'P07', ok=False)
        # Y la tarea de la rama activa se cierra: develop no la estorba.
        self.escribir({**self.leer(), 'peticiones': self.leer()['peticiones'] + [{
            'id': 9, 'texto': 'Otra tarea', 'estado': 'en-curso', 'rama': 'feature/9-otra',
            'pasos': [{'texto': 'Activar rama para poder probar', 'estado': 'hecho'},
                      {'texto': 'Cerrar la tarea', 'estado': 'pendiente'}]}]})
        self.orden('cerrar', '9')
        self.assertEqual(git(self.raiz, 'show', 'develop:a.txt'), 'dos')
        self.assertIn('pasada a la tarea 13 de la cola', self.propuestas.read_text(encoding='utf-8'))

    def test_con_cambios_sin_commit_en_develop_no_hace_nada(self):
        self.propuestas.write_bytes((self.MD + '\nA mano.\n').encode('utf-8'))
        self.assertIn('cambios sin commit', self.orden('a-propuesta', '11', ok=False))
        self.assertIsNotNone(self.tarea(11))
        self.assertEqual(self.en_develop(), self.MD)

    def test_con_develop_en_otro_worktree_no_hace_nada(self):
        git(self.raiz, 'switch', '-q', '-c', 'feature/9-otra')
        otro = Path(self._tmp.name) / 'otro'
        git(self.raiz, 'worktree', 'add', '-q', str(otro), 'develop')
        self.assertIn('worktree', self.orden('de-propuesta', 'Otra', '--numero', 'P07', ok=False))
        self.assertEqual(self.en_develop(), self.MD)
        self.assertIsNone(self.tarea(13))

    def test_si_falla_la_cola_develop_vuelve_atras(self):
        self.otra_rama()
        antes = git(self.raiz, 'rev-parse', 'develop')
        guardar = cola.Cola.guardar

        def falla(self_):
            raise OSError('disco lleno')
        cola.Cola.guardar = falla
        try:
            with self.assertRaises(OSError):
                cola.main(['--raiz', str(self.raiz), '--json', 'a-propuesta', '11'])
        finally:
            cola.Cola.guardar = guardar
        self.assertEqual(git(self.raiz, 'rev-parse', 'develop'), antes)
        self.assertIsNotNone(self.tarea(11))

    def test_sin_git_solo_el_archivo_y_lo_avisa(self):
        shutil.rmtree(self.raiz / '.git', onerror=lambda f, p, e: (os.chmod(p, 0o700), f(p)))
        r = self.respuesta('de-propuesta', 'Otra', '--numero', 'P07')
        self.assertIn('sin commit: no hay git con develop', r['mensaje'])
        self.assertIn('pasada a la tarea 13 de la cola', self.propuestas.read_text(encoding='utf-8'))


class Decisiones(Base):
    """«decision» (tarea 283): registra o reescribe una decisión en sf/decisiones/ (208) con su índice y hace el commit
    en develop, también con otra rama activa, sin cambiarla ni tocar su copia de trabajo."""
    git = True
    RUTA = 'sf/decisiones'
    PRIMERA = '# Primera\n\n- **Decisión:** una.\n'
    HOY = time.strftime('%Y-%m-%d')

    def setUp(self):
        super().setUp()
        self.carpeta = self.raiz / self.RUTA
        self.carpeta.mkdir(parents=True)
        (self.carpeta / '007-2026-01-02-primera.md').write_text(self.PRIMERA, encoding='utf-8')
        (self.carpeta / 'README.md').write_text('# Decisiones\n\nIntro propia.\n\n## Índice\n\nviejo\n', encoding='utf-8')
        git(self.raiz, 'add', '.')
        git(self.raiz, 'commit', '-q', '-m', 'Decisiones')
        # La cola no se toca: ni siquiera rota estorba.
        self.archivo.write_text('{roto', encoding='utf-8')

    def en_develop(self, nombre: str) -> str:
        return git(self.raiz, 'show', f'develop:{self.RUTA}/{nombre}') + '\n'

    def limpio(self) -> None:
        self.assertEqual(git(self.raiz, 'status', '--porcelain', '--untracked-files=no'), '')

    def test_con_develop_activa(self):
        r = self.respuesta('decision', 'Las decisiones, en develop', '--texto', '- **Decisión:** sí, «ahora».',
                           '--coautor', 'Co-Authored-By: Prueba <p@example.com>')
        nombre = f'008-{self.HOY}-las-decisiones-en-develop.md'
        self.assertEqual((r['numero'], r['archivo']), (8, f'{self.RUTA}/{nombre}'))
        self.assertEqual(r['hash'], git(self.raiz, 'rev-parse', '--short', 'develop'))
        self.assertIn(f'Decisión 008 registrada en develop ({r["hash"]})', r['mensaje'])
        self.limpio()
        self.assertEqual(self.en_develop(nombre), '# Las decisiones, en develop\n\n- **Decisión:** sí, «ahora».\n')
        self.assertEqual(git(self.raiz, 'log', '-1', '--format=%B'),
                         'Decisión 008: Las decisiones, en develop\n\nCo-Authored-By: Prueba <p@example.com>')
        indice = self.en_develop('README.md')
        self.assertTrue(indice.startswith('# Decisiones\n\nIntro propia.\n\n## Índice\n'))
        self.assertLess(indice.index(f'| 8 | {self.HOY} | [Las decisiones, en develop]({nombre}) |'),
                        indice.index('| 7 | 2026-01-02 | [Primera](007-2026-01-02-primera.md) |'))
        self.assertEqual((self.carpeta / 'README.md').read_text(encoding='utf-8'), indice)
        self.assertEqual(self.archivo.read_text(encoding='utf-8'), '{roto')
        # La siguiente, también con develop activa (con o sin README.html sin versionar).
        self.assertEqual(self.respuesta('decision', 'Otra más', '--texto', 'Texto.')['numero'], 9)
        self.limpio()

    def test_con_otra_rama_activa_no_la_cambia_ni_toca_su_copia(self):
        git(self.raiz, 'switch', '-q', '-c', 'feature/9-otra')
        (self.raiz / 'a.txt').write_text('dos\n', encoding='utf-8')
        git(self.raiz, 'commit', '-q', '-am', 'Trabajo de la 9')
        (self.raiz / 'a.txt').write_text('a medias\n', encoding='utf-8')  # cambios sin commit de la rama: no estorban
        cabeza = git(self.raiz, 'rev-parse', 'HEAD')
        indice_antes = (self.carpeta / 'README.md').read_bytes()
        r = self.respuesta('decision', 'Otra rama', '--texto', 'Texto.')
        nombre = f'008-{self.HOY}-otra-rama.md'
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'feature/9-otra')
        self.assertEqual(git(self.raiz, 'rev-parse', 'HEAD'), cabeza)
        self.assertEqual(git(self.raiz, 'status', '--porcelain', '--untracked-files=all'), 'M a.txt')
        self.assertFalse((self.carpeta / nombre).exists())
        self.assertEqual((self.carpeta / 'README.md').read_bytes(), indice_antes)
        self.assertEqual(r['hash'], git(self.raiz, 'rev-parse', '--short', 'develop'))
        self.assertEqual(git(self.raiz, 'log', '-1', '--format=%s', 'develop'), 'Decisión 008: Otra rama')
        self.assertEqual(git(self.raiz, 'show', '--name-only', '--format=', 'develop').splitlines(),
                         [f'{self.RUTA}/{nombre}', f'{self.RUTA}/README.md'])
        self.assertEqual(self.en_develop(nombre), '# Otra rama\n\nTexto.\n')
        self.assertIn(f'[Otra rama]({nombre})', self.en_develop('README.md'))
        self.assertIn('Intro propia.', self.en_develop('README.md'))
        self.assertEqual(git(self.raiz, 'show', 'develop:a.txt'), 'uno')
        # La siguiente, sobre la de develop: la 9.
        self.assertEqual(self.respuesta('decision', 'Tercera', '--texto', 'Más.')['numero'], 9)

    def test_reescribir_por_numero(self):
        git(self.raiz, 'switch', '-q', '-c', 'feature/9-otra')
        texto = self.raiz / 'texto.md'
        texto.write_text('# Primera, mejor\n\n**Sustituida** el 2026-02-01 por «Otra».\n', encoding='utf-8')
        r = self.respuesta('decision', 'Primera, mejor', '--archivo', str(texto), '--numero', '7')
        self.assertEqual((r['numero'], r['archivo']), (7, f'{self.RUTA}/007-2026-01-02-primera.md'))
        self.assertEqual(git(self.raiz, 'log', '-1', '--format=%s', 'develop'), 'Decisión 007: Primera, mejor (modificada)')
        self.assertEqual(self.en_develop('007-2026-01-02-primera.md'), texto.read_text(encoding='utf-8'))
        self.assertIn('| 7 | 2026-01-02 | [Primera, mejor](007-2026-01-02-primera.md) (sustituida) |',
                      self.en_develop('README.md'))
        self.assertIn('ya dice eso', self.orden('decision', 'Primera, mejor', '--archivo', str(texto), '--numero', '7',
                                                ok=False))
        self.assertIn('No hay decisión 005', self.orden('decision', 'X', '--texto', 'Y', '--numero', '5', ok=False))

    def test_titulo_y_encabezado_distintos_no_hace_nada(self):
        antes = git(self.raiz, 'rev-parse', 'develop')
        self.assertIn('que coincidan', self.orden('decision', 'Uno', '--texto', '# Dos\n\nTexto.', ok=False))
        self.assertEqual(git(self.raiz, 'rev-parse', 'develop'), antes)

    def test_con_develop_en_otro_worktree_no_hace_nada(self):
        git(self.raiz, 'switch', '-q', '-c', 'feature/9-otra')
        otro = Path(self._tmp.name) / 'otro'
        git(self.raiz, 'worktree', 'add', '-q', str(otro), 'develop')
        antes = git(self.raiz, 'rev-parse', 'develop')
        self.assertIn('worktree', self.orden('decision', 'Nueva', '--texto', 'Texto.', ok=False))
        self.assertEqual(git(self.raiz, 'rev-parse', 'develop'), antes)

    def test_con_cambios_sin_commit_en_las_decisiones_no_hace_nada(self):
        (self.carpeta / '007-2026-01-02-primera.md').write_text(self.PRIMERA + 'A mano.\n', encoding='utf-8')
        self.assertIn('cambios sin commit', self.orden('decision', 'Nueva', '--texto', 'Texto.', ok=False))
        self.assertEqual(git(self.raiz, 'log', '-1', '--format=%s'), 'Decisiones')

    def test_push(self):
        remoto = Path(self._tmp.name) / 'remoto.git'
        git(self.raiz, 'init', '-q', '--bare', str(remoto))
        git(self.raiz, 'remote', 'add', 'origin', str(remoto))
        git(self.raiz, 'switch', '-q', '-c', 'feature/9-otra')
        r = self.respuesta('decision', 'Subida', '--texto', 'Texto.', '--push')
        self.assertIn('Subida a origin.', r['mensaje'])
        self.assertEqual(git(remoto, 'rev-parse', 'develop'), git(self.raiz, 'rev-parse', 'develop'))

    def test_sin_git_solo_los_archivos_y_lo_avisa(self):
        shutil.rmtree(self.raiz / '.git', onerror=lambda f, p, e: (os.chmod(p, 0o700), f(p)))
        r = self.respuesta('decision', 'Sin git', '--texto', 'Texto.')
        self.assertIn('sin commit: no hay git con develop', r['mensaje'])
        self.assertTrue((self.carpeta / f'008-{self.HOY}-sin-git.md').is_file())
        self.assertIn('[Sin git]', (self.carpeta / 'README.md').read_text(encoding='utf-8'))


class DecisionesAntes(Decisiones):
    """Lo mismo en docs/decisiones/, la carpeta de antes, mientras el proyecto no se ha puesto al día (208)."""
    RUTA = 'docs/decisiones'

    def test_con_las_dos_manda_sf(self):
        nueva = self.raiz / Decisiones.RUTA
        nueva.mkdir(parents=True)
        (nueva / 'README.md').write_text('# Decisiones\n\n## Índice\n', encoding='utf-8')
        git(self.raiz, 'add', '.')
        git(self.raiz, 'commit', '-q', '-m', 'sf/')
        r = self.respuesta('decision', 'Otra', '--texto', '- **Decisión:** no.')
        self.assertTrue(r['archivo'].startswith('sf/decisiones/001-'))


class PropuestasEnDevelopAntes(PropuestasEnDevelop):
    """Lo mismo con docs/propuestas.md, el sitio de antes (203)."""
    RUTA = 'docs/propuestas.md'


class Tipo(Base):
    """El tipo de la tarea, de una lista cerrada en infinitivo (decisión del propietario, 2026-10-31)."""

    def mal_escrita(self, *args: str) -> None:
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as e:
            cola.main(['--raiz', str(self.raiz), *args])
        self.assertEqual(e.exception.code, 2)

    def test_crear_con_tipo_y_fuera_de_la_lista(self):
        self.orden('crear', 'Pensarlo', '--tipo', 'deliberar')
        self.assertEqual(self.tarea(11)['tipo'], 'deliberar')
        self.orden('crear', 'Sin tipo')
        self.assertNotIn('tipo', self.tarea(12))
        self.mal_escrita('crear', 'Otra', '--tipo', 'pensar')
        self.assertIsNone(self.tarea(13))

    def test_tipo_lo_pone_o_cambia_y_lo_anota(self):
        self.orden('crear', 'Una')
        self.assertEqual(self.orden('tipo', '11', 'investigar'), 'La 11, de tipo investigar.')
        self.orden('tipo', '11', 'implementar')
        t = self.tarea(11)
        self.assertEqual(t['tipo'], 'implementar')
        self.assertEqual([(e['evento'], e.get('detalle')) for e in t['historial'][-2:]],
                         [('tipo', 'investigar'), ('tipo', 'implementar (antes: investigar)')])
        self.orden('tipo', '11', 'implementar', ok=False)
        self.orden('tipo', '99', 'corregir', ok=False)
        self.mal_escrita('tipo', '11', 'arreglar')
        self.assertEqual(self.tarea(11)['tipo'], 'implementar')

    def test_se_conserva_al_salir_y_volver(self):
        self.orden('crear', 'Sobra', '--tipo', 'documentar')
        self.orden('eliminar', '11')
        self.assertEqual(self.archivadas()[-1]['tipo'], 'documentar')
        self.orden('restaurar', '11')
        self.assertEqual(self.tarea(11)['tipo'], 'documentar')
        self.escribir({'ultimo': 11, 'peticiones': [{'id': 11, 'texto': 'En observación', 'estado': 'en-observacion', 'tipo': 'corregir'}]})
        self.orden('reabrir', '11', 'falla', '--en-cola')
        self.assertEqual(self.tarea(11)['tipo'], 'corregir')

    def test_fusionar_y_split_lo_conservan(self):
        self.escribir({'ultimo': 13, 'peticiones': [
            {'id': 11, 'texto': 'Una', 'estado': 'en-cola', 'tipo': 'diseñar'},
            {'id': 12, 'texto': 'Dos', 'estado': 'en-cola'},
            {'id': 13, 'texto': 'Tres', 'estado': 'en-cola', 'tipo': 'especificar'},
        ]})
        self.orden('fusionar', '11', '13')
        self.assertEqual(self.tarea(13)['tipo'], 'especificar')  # el de la que queda
        self.orden('fusionar', '12', '13')
        self.assertEqual(self.tarea(13)['tipo'], 'especificar')
        self.escribir({'ultimo': 13, 'peticiones': [{'id': 12, 'texto': 'Dos', 'estado': 'en-cola'},
                                                    {'id': 13, 'texto': 'Sin', 'estado': 'en-cola', 'tipo': None}]})
        self.orden('fusionar', '12', '13')
        self.assertNotIn('tipo', {k: v for k, v in self.tarea(13).items() if v})
        self.escribir({'ultimo': 20, 'peticiones': [
            {'id': 20, 'texto': 'Sin tipo', 'estado': 'en-cola'},
            {'id': 21, 'texto': 'Con tipo', 'estado': 'en-cola', 'tipo': 'investigar'},
        ]})
        self.orden('fusionar', '20', '21')
        self.assertEqual(self.tarea(21)['tipo'], 'investigar')
        self.escribir({'ultimo': 30, 'peticiones': [{'id': 30, 'texto': 'Grande', 'estado': 'en-cola', 'tipo': 'implementar',
                                                     'pasos': [{'texto': 'A', 'estado': 'pendiente'}, {'texto': 'B', 'estado': 'pendiente'}]}]})
        self.orden('split', '30', '2')
        self.assertEqual(self.tarea(31)['tipo'], 'implementar')


class Copias(Base):
    def test_una_copia_antes_de_cada_escritura_y_solo_50(self):
        self.orden('crear', 'Una')
        copias = cola.lista_copias(self.raiz / '.sf' / 'copias')
        self.assertEqual(len(copias), 1)
        self.assertEqual(json.loads(copias[0].read_text(encoding='utf-8'))['peticiones'], [])
        for i in range(55):
            self.orden('renombrar', '11', f'Nombre {i}')
        self.assertEqual(len(cola.lista_copias(self.raiz / '.sf' / 'copias')), 50)

    def test_recuperar_y_deshacer(self):
        self.orden('crear', 'Una')
        self.orden('crear', 'Dos')
        self.orden('renombrar', '12', 'Dos bis')
        self.escribir({'peticiones': 'roto'})  # a mano, sin el CLI: no deja copia
        self.assertIn('2 tareas\tdespués: bajas 11, 12', self.orden('copias'))
        self.orden('recuperar', '1')  # la copia 1: antes del último cambio del CLI
        self.assertEqual([t['texto'] for t in self.leer()['peticiones']], ['Una', 'Dos'])
        self.orden('recuperar', '1')  # deshace la recuperación
        self.assertEqual(self.leer()['peticiones'], 'roto')
        self.orden('recuperar', '99', ok=False)

    def test_json_roto_no_se_toca(self):
        self.archivo.write_text('{roto', encoding='utf-8')
        self.assertIn('recuperar', self.orden('crear', 'Una', ok=False))
        self.assertEqual(self.archivo.read_text(encoding='utf-8'), '{roto')


class Migracion215(Base):
    """«En observación», sin alias ni rastros (decisión 215): lo guardado con los nombres de antes se convierte una vez
    al cargarlo, y las órdenes viejas ya no existen. Solo las líneas con «migración 215» nombran lo de antes."""
    VIEJO = 'sin-probar'  # migración 215
    VIEJA = {'id': 11, 'texto': 'Vieja', 'estado': VIEJO, 'probando': True, 'historial': [  # migración 215
        {'evento': 'a-testing', 'fecha': 'f', 'quien': 'principal', 'via': 'cli', 'detalle': 'develop abc1234'},  # migración 215
        {'evento': 'probando', 'fecha': 'f', 'quien': 'principal', 'via': 'cli'},  # migración 215
        {'evento': 'pendiente', 'fecha': 'f', 'quien': 'principal', 'via': 'cli'}]}  # migración 215
    SALIDA = {'id': 9, 'texto': 'Salida', 'estado': 'cerrada', 'historial': [
        {'evento': 'a-testing', 'fecha': 'f', 'quien': 'principal', 'via': 'cli', 'detalle': 'develop def5678'},  # migración 215
        {'evento': 'probada', 'fecha': 'f', 'quien': 'propietario', 'via': 'panel'}]}  # migración 215

    def test_comprobado_es_un_paso_hecho_sin_volver_a_probar(self):  # decisión 288
        self.escribir({'ultimo': 11, 'peticiones': [{'id': 11, 'texto': 'Ya vista', 'estado': 'en-curso', 'pasos': [
            {'texto': 'Hacer', 'estado': 'hecho'}, {'texto': 'Activar rama para poder probar', 'estado': 'hecho'},
            {'texto': 'Mirar', 'estado': 'pendiente', 'ayuda': True}, {'texto': 'Cerrar la tarea', 'estado': 'pendiente'}]}]})
        m = self.orden('comprobado', '11', '300 pruebas de Python, sin fallos')
        self.assertIn('Paso 2 de 5 de la 11, hecho: «Comprobado: 300 pruebas de Python, sin fallos»', m)
        self.orden('comprobado', '11', 'Comprobado en el navegador: se ve')  # ya con la palabra, no la repite
        self.assertEqual([(p['texto'], p['estado']) for p in self.tarea(11)['pasos']], [
            ('Hacer', 'hecho'), ('Comprobado: 300 pruebas de Python, sin fallos', 'hecho'),
            ('Comprobado en el navegador: se ve', 'hecho'), ('Activar rama para poder probar', 'hecho'),
            ('Mirar', 'pendiente'), ('Cerrar la tarea', 'pendiente')])
        self.assertEqual(self.eventos(self.tarea(11))[-1], 'comprobado')
        self.orden('comprobado', '11', '  ', ok=False)

    def test_el_campo_comprobado_pasa_a_los_pasos_al_cargar(self):  # decisión 288
        self.escribir({'ultimo': 12, 'peticiones': [
            {'id': 11, 'texto': 'Vieja', 'estado': 'en-observacion', 'comprobado': 'lo abrí',
             'pasos': [{'texto': 'Hacer', 'estado': 'hecho'}, {'texto': 'Cerrar la tarea', 'estado': 'hecho'}]},
            {'id': 12, 'texto': 'Vacía', 'estado': 'en-cola', 'comprobado': ''}]})
        self.orden('renombrar', '12', 'Vacía, renombrada')  # cualquier escritura la guarda
        t11, t12 = self.tarea(11), self.tarea(12)
        self.assertNotIn('comprobado', t11)
        self.assertNotIn('comprobado', t12)
        self.assertEqual([p['texto'] for p in t11['pasos']], ['Hacer', 'Comprobado: lo abrí', 'Cerrar la tarea'])
        self.assertEqual(t12.get('pasos', []), [])

    def comprobar_nueva(self, t: dict) -> None:
        self.assertEqual(t['estado'], 'en-observacion')
        self.assertTrue(t['observando'])
        self.assertNotIn(self.VIEJO, json.dumps(t))
        self.assertEqual(self.eventos(t)[:3], ['a-observacion', 'observando', 'seguir'])

    def test_la_cola_se_convierte_al_cargarla_una_vez(self):
        self.escribir({'ultimo': 11, 'peticiones': [json.loads(json.dumps(self.VIEJA))]})
        self.orden('comprobado', '11', 'visto')
        self.comprobar_nueva(self.tarea(11))
        antes = self.leer()
        c = cola.Cola(self.raiz, 'principal', 'cli')
        c.cargar()
        self.assertEqual(c.datos, antes)  # otra carga no cambia nada
        self.assertFalse(cola.migrar_tarea(c.datos['peticiones'][0]))

    def test_lista_y_ver_ya_la_ven_convertida(self):
        self.escribir({'ultimo': 11, 'peticiones': [json.loads(json.dumps(self.VIEJA))]})
        self.assertIn('en observación', self.orden('lista'))
        self.assertEqual(json.loads(self.orden('ver', '11'))['estado'], 'en-observacion')

    def test_las_ordenes_nuevas_sobre_una_cola_vieja(self):
        self.escribir({'ultimo': 11, 'peticiones': [json.loads(json.dumps(self.VIEJA))]})
        self.assertEqual(self.orden('seguir', '11'), 'La 11 sigue en observación.')
        self.assertNotIn('observando', self.tarea(11))
        self.assertEqual(self.orden('observando', '11'), 'La 11, en observación: la estás mirando.')
        self.assertEqual(self.orden('cerrar', '11'), 'Cerrada la 11, en observación: sale de la cola.')
        a = self.archivadas()[-1]
        self.assertEqual((a['estado'], self.eventos(a)[-1], a['historial'][-1]['detalle']),
                         ('cerrada', 'cerrada', 'en observación'))

    def test_el_historial_se_convierte_al_escribir(self):
        (self.raiz / '.sf' / 'historial.jsonl').write_text(json.dumps(self.SALIDA) + '\n', encoding='utf-8')
        self.assertIn('cerrada', self.orden('ver', '9'))
        self.orden('crear', 'Otra')
        a = self.archivadas()[0]
        self.assertEqual(self.eventos(a), ['a-observacion', 'cerrada'])
        self.assertEqual(a['historial'][1]['detalle'], 'en observación')
        self.orden('reobservar', '9')
        t = self.tarea(9)
        self.assertEqual((t['estado'], t['commit']), ('en-observacion', 'def5678'))

    def test_una_copia_vieja_se_convierte_al_recuperarla(self):
        self.escribir({'ultimo': 11, 'peticiones': [json.loads(json.dumps(self.VIEJA))]})
        self.orden('crear', 'Otra')  # copia la cola de antes, con los nombres viejos
        copia = cola.lista_copias(self.raiz / '.sf' / 'copias')[0]
        copia.write_text(json.dumps({'ultimo': 11, 'peticiones': [self.VIEJA]}), encoding='utf-8')
        self.assertIn('después:', self.orden('copias'))
        self.orden('recuperar', '1')
        self.comprobar_nueva(self.tarea(11))

    def test_las_ordenes_viejas_ya_no_existen(self):
        self.escribir({'ultimo': 11, 'peticiones': [json.loads(json.dumps(self.VIEJA))]})
        for vieja in ('a-testing', 'probada', 'probando', 'pendiente'):  # migración 215
            with self.subTest(vieja), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as e:
                cola.main(['--raiz', str(self.raiz), vieja, '11'])
            self.assertEqual(e.exception.code, 2)
        self.assertNotIn('probada', cola.__doc__)  # migración 215


class Bloqueo(Base):
    def test_bloqueo_reciente_impide_escribir(self):
        espera = cola.ESPERA_BLOQUEO
        cola.ESPERA_BLOQUEO = 0.2
        try:
            (self.raiz / '.sf' / 'peticiones.lock').write_text('otro', encoding='utf-8')
            self.assertIn('bloqueada', self.orden('crear', 'Una', ok=False))
        finally:
            cola.ESPERA_BLOQUEO = espera
        self.assertTrue((self.raiz / '.sf' / 'peticiones.lock').exists())  # no es suyo: no lo quita

    def test_bloqueo_abandonado_se_quita(self):
        lock = self.raiz / '.sf' / 'peticiones.lock'
        lock.write_text('viejo', encoding='utf-8')
        viejo = time.time() - 3600
        os.utime(lock, (viejo, viejo))
        self.orden('crear', 'Una')
        self.assertFalse(lock.exists())

    def test_lectura_sin_bloqueo(self):
        (self.raiz / '.sf' / 'peticiones.lock').write_text('otro', encoding='utf-8')
        self.orden('lista')


class ConGit(Base):
    git = True

    def en_curso_con_rama(self, texto='Tarea', nombre='tarea') -> int:
        self.orden('crear', texto, '--en-curso')
        id_ = self.leer()['ultimo']
        self.orden('rama', str(id_), nombre)
        return id_

    def test_rama_desde_develop(self):
        self.orden('crear', 'Una', '--en-curso')
        self.assertIn('activa', self.orden('rama', '11', 'una'))
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'feature/11-una')
        self.orden('rama', '11', 'otra', ok=False)
        self.orden('crear', 'Dos', '--en-curso')
        self.orden('rama', '12', 'dos', '--sin-activar')
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'feature/11-una')
        self.assertEqual(self.tarea(12)['rama'], 'feature/12-dos')
        self.orden('crear', 'Tres', '--en-curso')
        self.orden('rama', '13', 'no-existe', '--anotar', ok=False)

    def test_cerrar_exige_los_pasos_de_trabajo_hechos(self):
        id_ = self.en_curso_con_rama()
        self.orden('paso', 'añadir', str(id_), 'Hacer')
        self.assertIn('sin hacer: 1', self.orden('cerrar', str(id_), ok=False))

    def test_cerrar_con_squash_push_fallido(self):
        id_ = self.en_curso_con_rama('Cambiar a', 'cambiar-a')
        self.orden('paso', 'añadir', str(id_), 'Cambiar a.txt')
        self.commit_en('feature/11-cambiar-a', 'a.txt', 'dos\n')
        self.orden('paso', 'marcar', str(id_), '1', 'hecho', '--texto', 'Cambiado a.txt')
        self.orden('listo', str(id_), '--prueba', 'leer a.txt')
        mensaje = self.orden('cerrar', str(id_))
        self.assertIn('falta el push', mensaje)
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'develop')
        self.assertEqual(git(self.raiz, 'log', '-1', '--format=%s'), 'Cambiar a (11)')
        self.assertIn('- Cambiado a.txt', git(self.raiz, 'log', '-1', '--format=%b'))
        self.assertNotIn('feature/11-cambiar-a', git(self.raiz, 'branch'))
        self.assertIsNone(self.tarea(11))
        a = self.archivadas()[-1]
        hash_ = git(self.raiz, 'rev-parse', '--short', 'HEAD')
        self.assertEqual(self.eventos(a)[-2:], ['cerrada', 'push-fallido'])
        self.assertEqual(a['historial'][-2]['detalle'], f'develop {hash_}')
        self.assertTrue(all(p['estado'] == 'hecho' for p in a['pasos']))

    def test_cerrar_con_push(self):
        remoto = Path(self._tmp.name) / 'remoto.git'
        subprocess.run(['git', 'init', '-q', '--bare', str(remoto)], check=True)
        git(self.raiz, 'remote', 'add', 'origin', str(remoto))
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.assertNotIn('Aviso', self.orden('cerrar', str(id_)))
        self.assertEqual(git(remoto, 'log', '-1', '--format=%s', 'develop'), 'Tarea (11)')
        self.assertNotIn('push-fallido', self.eventos(self.archivadas()[-1]))

    def proyecto(self, **campos) -> None:
        (self.raiz / '.sf' / 'proyecto.json').write_text(json.dumps({'proyecto': 'Demo', **campos}), encoding='utf-8')

    def test_cerrar_con_push_al_remoto_de_la_configuracion(self):
        remoto = Path(self._tmp.name) / 'pose.git'
        subprocess.run(['git', 'init', '-q', '--bare', str(remoto)], check=True)
        git(self.raiz, 'remote', 'add', 'PoseTracker', str(remoto))
        self.proyecto(remoto='PoseTracker')
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.assertNotIn('Aviso', self.orden('cerrar', str(id_)))
        self.assertEqual(git(remoto, 'log', '-1', '--format=%s', 'develop'), 'Tarea (11)')

    def test_cerrar_firma_con_el_coautor_configurado_o_el_de_la_orden(self):
        self.proyecto(coautor='Ana <ana@example.com>')
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.orden('cerrar', str(id_))
        self.assertEqual(git(self.raiz, 'log', '-1', '--format=%(trailers:key=Co-Authored-By,valueonly)'),
                         'Ana <ana@example.com>')
        id_ = self.en_curso_con_rama('Otra', 'otra')
        self.commit_en('feature/12-otra', 'c.txt', 'c\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.orden('cerrar', str(id_), '--coautor', 'Claude Fable <noreply@anthropic.com>')
        self.assertEqual(git(self.raiz, 'log', '-1', '--format=%B'),
                         'Otra (12)\n\nCo-Authored-By: Claude Fable <noreply@anthropic.com>')
        with self.assertRaises(cola.Rechazo):
            cola.coautor_de(mock.Mock(coautor='a\nb'))

    def test_cerrar_en_la_sf_firma_con_su_linea(self):
        (self.raiz / 'plugins/sf/.claude-plugin').mkdir(parents=True)
        (self.raiz / cola.MARCA_SF).write_text('{"version": "1.6.0"}', encoding='utf-8')
        git(self.raiz, 'add', 'plugins')
        git(self.raiz, 'commit', '-q', '-m', 'marca')
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.orden('cerrar', str(id_))
        self.assertTrue(git(self.raiz, 'log', '-1', '--format=%B').endswith(cola.COAUTOR))

    def test_cerrar_con_trailer_en_conventional(self):
        self.proyecto(commits='conventional')
        id_ = self.en_curso_con_rama('feat: lista de tareas', 'lista')
        self.orden('paso', 'añadir', str(id_), 'Hacer la lista')
        self.commit_en('feature/11-lista', 'b.txt', 'b\n')
        self.orden('paso', 'marcar', str(id_), '1', 'hecho')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.orden('cerrar', str(id_))
        self.assertEqual(git(self.raiz, 'log', '-1', '--format=%s'), 'feat: lista de tareas')
        cuerpo = git(self.raiz, 'log', '-1', '--format=%b')
        self.assertIn('- Hacer la lista', cuerpo)
        # Sin `coautor` en la configuración, sin línea de coautoría (238).
        self.assertTrue(cuerpo.endswith('SF-Tarea: 11'), cuerpo)
        self.assertNotIn('Co-Authored-By', cuerpo)
        self.assertEqual(git(self.raiz, 'log', '-1', '--format=%(trailers:key=SF-Tarea,valueonly)'), '11')
        # Lo encuentra como al de «(N)», y su revert lo deja fuera.
        hash_ = git(self.raiz, 'rev-parse', '--short', 'HEAD')
        self.assertEqual(cola.hashes_en_develop(self.raiz, 11), [hash_])
        git(self.raiz, 'revert', '--no-edit', 'HEAD')
        self.assertEqual(cola.hashes_en_develop(self.raiz, 11), [])

    def test_cerrar_en_conventional_con_el_prefijo_del_tipo(self):
        self.proyecto(commits='conventional')
        self.orden('crear', 'Arreglar el cierre', '--tipo', 'corregir', '--en-curso')
        self.orden('rama', '11', 'cierre')
        self.commit_en('feature/11-cierre', 'b.txt', 'b\n')
        self.orden('listo', '11', '--prueba', 'mirar')
        self.orden('cerrar', '11')
        self.assertEqual(git(self.raiz, 'log', '-1', '--format=%s'), 'fix: Arreglar el cierre')

    def test_cierre_con_choques_se_deshace(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'a.txt', 'rama\n')
        self.commit_en('develop', 'a.txt', 'develop\n')
        git(self.raiz, 'switch', '-q', 'feature/11-tarea')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        r = self.respuesta('cerrar', str(id_), ok=False)
        self.assertIn('a.txt', r['mensaje'])
        self.assertEqual((r['fallo'], r['motivo']), ('choques', 'choques en el merge de feature/11-tarea: a.txt'))
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'feature/11-tarea')
        self.assertEqual(git(self.raiz, 'status', '--porcelain', '--untracked-files=no'), '')
        t = self.tarea(11)
        self.assertEqual((t['estado'], self.eventos(t)[-1]), ('en-curso', 'cierre-fallido'))

    def test_cerrar_con_cambios_sin_commit(self):
        id_ = self.en_curso_con_rama()
        self.orden('listo', str(id_), '--prueba', 'mirar')
        (self.raiz / 'a.txt').write_text('sucio\n', encoding='utf-8')
        self.assertIn('sin commit', self.orden('cerrar', str(id_), ok=False))
        self.assertEqual(self.eventos(self.tarea(11))[-1], 'listo')

    def test_a_observacion_con_squash_y_revertir(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.orden('a-observacion', str(id_))
        t = self.tarea(11)
        hash_ = git(self.raiz, 'rev-parse', '--short', 'HEAD')
        self.assertEqual((t['estado'], t['commit'], 'rama' in t), ('en-observacion', hash_, False))
        self.assertEqual(git(self.raiz, 'log', '-1', '--format=%s'), 'Tarea (11)')
        self.orden('descartar', str(id_), ok=False)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            cola.main(['--raiz', str(self.raiz), 'revertir', str(id_)])  # sin destino, mal escrita
        self.assertIn('eliminada', self.orden('revertir', str(id_), '--eliminar'))
        self.assertTrue((git(self.raiz, 'log', '-1', '--format=%s')).startswith('Revert "Tarea (11)"'))
        self.assertFalse((self.raiz / 'b.txt').exists())
        self.assertIsNone(self.tarea(11))
        a = self.archivadas()[-1]
        self.assertEqual((self.eventos(a)[-2:], a['estado']), (['revertida', 'eliminada'], 'eliminada'))
        self.orden('revertir', str(id_), '--eliminar', ok=False)  # ya revertida: no le quedan commits
        # Restaurada, vuelve en cola y reabierta.
        self.orden('restaurar', str(id_))
        t = self.tarea(11)
        self.assertEqual((t['estado'], t.get('reabierta')), ('en-cola', True))
        self.assertEqual(self.cierre(t), ['pendiente', 'pendiente'])

    def test_reobservar_una_cerrada_y_revertirla(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.orden('cerrar', str(id_))
        hash_ = git(self.raiz, 'rev-parse', '--short', 'HEAD')
        self.assertEqual(self.orden('reobservar', '11'), f'La 11 vuelve a observación, con su commit de develop ({hash_}).')
        t = self.tarea(11)
        self.assertEqual((t['estado'], t['commit'], t['prueba']), ('en-observacion', hash_, 'mirar'))
        self.assertEqual(self.eventos(t)[-1], 'reobservada')
        self.assertEqual(t['historial'][-1]['detalle'], f'con develop {hash_}')
        self.assertEqual(cola.hashes_de(t), [hash_])  # su evento no repite el commit: se revierte una vez
        self.orden('reobservar', '11', ok=False)  # ya en observación
        self.assertIn('vuelve a Pendientes', self.orden('revertir', '11', '--pendiente'))
        self.assertFalse((self.raiz / 'b.txt').exists())
        self.assertEqual(self.tarea(11)['estado'], 'en-cola')

    def test_reobservar_y_cerrarla_otra_vez(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.orden('cerrar', str(id_))
        self.orden('reobservar', '11')
        self.orden('cerrar', '11')
        a = self.archivadas()[-1]
        self.assertEqual((a['estado'], self.eventos(a)[-2:]), ('cerrada', ['reobservada', 'cerrada']))
        self.orden('reobservar', '11')  # cerrada otra vez, puede volver otra vez
        self.assertEqual(self.tarea(11)['estado'], 'en-observacion')

    def cierre(self, t):
        return [x['estado'] for x in t['pasos'] if x['texto'] in ('Activar rama para poder probar', 'Cerrar la tarea')]

    def test_revertir_desde_observacion_a_pendientes(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.orden('a-observacion', str(id_))
        self.assertIn('vuelve a Pendientes', self.orden('revertir', str(id_), '--pendiente'))
        self.assertFalse((self.raiz / 'b.txt').exists())
        t = self.tarea(11)
        self.assertEqual((t['estado'], t['reabierta'], t.get('rama'), t.get('commit')), ('en-cola', True, None, None))
        self.assertEqual(self.eventos(t)[-2:], ['revertida', 'reabierta'])
        self.assertEqual(self.cierre(t), ['pendiente', 'pendiente'])
        self.assertEqual(self.archivadas(), [])
        self.orden('revertir', str(id_), '--pendiente', ok=False)  # en cola: no se revierte

    def test_revertir_una_cerrada_desde_otra_rama(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.orden('cerrar', str(id_))
        git(self.raiz, 'switch', '-q', '-c', 'otra')
        self.assertIn('Activa: develop', self.orden('revertir', '11', '--pendiente'))
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'develop')
        t = self.tarea(11)
        self.assertEqual((t['estado'], t['reabierta'], self.eventos(t)[-2:]), ('en-cola', True, ['revertida', 'reabierta']))
        # Vuelve a la cola sin línea nueva en el historial: la última sigue siendo la de su cierre.
        self.assertEqual(self.archivadas()[-1]['estado'], 'cerrada')

    def test_revertir_una_cerrada_y_eliminarla(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.orden('cerrar', str(id_))
        self.orden('revertir', '11', '--eliminar')
        self.assertIsNone(self.tarea(11))
        a = self.archivadas()[-1]
        self.assertEqual((a['estado'], self.eventos(a)[-2:]), ('eliminada', ['revertida', 'eliminada']))
        self.orden('crear', 'Otra')
        self.assertEqual(self.leer()['ultimo'], 12)  # su número no se reutiliza

    def test_revertir_con_choques_se_deshace(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'a.txt', 'rama\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.orden('a-observacion', str(id_))
        hash_ = git(self.raiz, 'rev-parse', '--short', 'HEAD')
        self.commit_en('develop', 'a.txt', 'después\n')
        r = self.respuesta('revertir', str(id_), '--pendiente', ok=False)
        self.assertEqual((r['fallo'], r['motivo']), ('choques', f'choques al revertir {hash_}'))
        self.assertEqual(git(self.raiz, 'status', '--porcelain', '--untracked-files=no'), '')
        self.assertEqual(self.tarea(11)['estado'], 'en-observacion')

    def test_revertir_sin_historial_lee_develop(self):
        self.commit_en('develop', 'c.txt', 'c\n')
        git(self.raiz, 'commit', '-q', '--amend', '-m', 'Antigua (7)')
        self.escribir({'ultimo': 10, 'peticiones': [{'id': 7, 'texto': 'Antigua', 'estado': 'en-observacion'}]})
        self.orden('revertir', '7', '--eliminar')
        self.assertFalse((self.raiz / 'c.txt').exists())

    def test_reabrir_una_cerrada_con_rama_nueva_desde_develop(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.orden('cerrar', str(id_))
        self.assertIn('feature/11-tarea', self.orden('reabrir', '11', 'falla b'))
        t = self.tarea(11)
        self.assertEqual((t['estado'], t['reabierta'], t['rama']), ('en-curso', True, 'feature/11-tarea'))
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'feature/11-tarea')
        self.assertEqual(git(self.raiz, 'rev-parse', 'HEAD'), git(self.raiz, 'rev-parse', 'develop'))
        self.assertEqual(self.eventos(t)[-2:], ['reabierta', 'rama'])
        self.assertEqual(self.cierre(t), ['pendiente', 'pendiente'])
        # listo solo guarda el «qué mirar»: los pasos quedan como estaban (decisión 174).
        for x in t['pasos']:
            x['estado'] = 'hecho'
        d = self.leer()
        d['peticiones'] = [t if x['id'] == 11 else x for x in d['peticiones']]
        self.escribir(d)
        self.assertNotIn('Aviso', self.orden('listo', '11', '--prueba', 'otra vez'))
        self.assertEqual(self.cierre(self.tarea(11)), ['hecho', 'hecho'])

    def test_reabrir_desde_observacion_en_cola_sin_rama(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.orden('a-observacion', str(id_))
        self.orden('reabrir', '11', 'falla', '--en-cola')
        t = self.tarea(11)
        self.assertEqual((t['estado'], t.get('rama')), ('en-cola', None))

    def con_rama_que_sobrevive(self, extra: bool) -> str:
        """La 11 en observación con su rama aún viva, como si no se hubiera podido borrar en el squash; con `extra`, la
        rama tiene además un commit que no entró en develop."""
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        punta = git(self.raiz, 'rev-parse', 'HEAD')
        git(self.raiz, 'switch', '-q', 'develop')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.orden('a-observacion', str(id_))
        git(self.raiz, 'branch', 'feature/11-tarea', punta)
        if extra:
            self.commit_en('feature/11-tarea', 'e.txt', 'e\n')
            git(self.raiz, 'switch', '-q', 'develop')
        d = self.leer()
        d['peticiones'][0]['rama'] = 'feature/11-tarea'
        self.escribir(d)
        return str(id_)

    def test_revertir_eliminar_borra_la_rama_que_sobrevivio(self):
        n = self.con_rama_que_sobrevive(extra=False)
        self.assertIn('Borrada la rama feature/11-tarea', self.orden('revertir', n, '--eliminar'))
        self.assertNotIn('feature/11-tarea', git(self.raiz, 'branch'))
        self.orden('restaurar', n)
        self.assertNotIn('rama', self.tarea(11))

    def test_revertir_eliminar_no_borra_una_rama_con_commits_fuera(self):
        n = self.con_rama_que_sobrevive(extra=True)
        self.assertIn('queda la rama feature/11-tarea, ya fuera de la tarea: tiene commits que no entraron en develop',
                      self.orden('revertir', n, '--eliminar'))
        self.assertIn('feature/11-tarea', git(self.raiz, 'branch'))  # en git, sí; en la tarea, no
        self.assertNotIn('rama', self.archivadas()[-1])

    def test_revertir_pendiente_deja_la_tarea_sin_rama_y_limpia(self):
        n = self.con_rama_que_sobrevive(extra=False)
        self.assertIn('Borrada la rama feature/11-tarea', self.orden('revertir', n, '--pendiente'))
        self.assertNotIn('feature/11-tarea', git(self.raiz, 'branch'))
        t = self.tarea(11)
        self.assertEqual((t['estado'], 'rama' in t), ('en-cola', False))

    def test_revertir_pendiente_no_borra_una_rama_con_commits_fuera(self):
        n = self.con_rama_que_sobrevive(extra=True)
        self.assertIn('queda la rama feature/11-tarea', self.orden('revertir', n, '--pendiente'))
        self.assertIn('feature/11-tarea', git(self.raiz, 'branch'))
        self.assertNotIn('rama', self.tarea(11))

    def test_descartar_limpiar_reabrir(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.assertIn('Activa: develop', self.orden('descartar', str(id_)))
        self.assertNotIn('feature/11-tarea', git(self.raiz, 'branch'))
        self.assertEqual(self.tarea(11)['estado'], 'descartada')
        self.orden('reabrir', '11', 'otra vez', '--rama', 'segunda', '--sin-activar')
        t = self.tarea(11)
        self.assertEqual((t['estado'], t['rama']), ('en-curso', 'feature/11-segunda'))
        self.orden('descartar', '11')
        self.orden('limpiar')
        self.assertIsNone(self.tarea(11))
        self.assertEqual(self.eventos(self.archivadas()[-1])[-1], 'limpiada')

    def test_descartar_rama_en_otro_worktree(self):
        id_ = self.en_curso_con_rama()
        git(self.raiz, 'switch', '-q', 'develop')
        otro = Path(self._tmp.name) / 'otro'
        git(self.raiz, 'worktree', 'add', '-q', str(otro), 'feature/11-tarea')
        self.assertIn('worktree', self.orden('descartar', str(id_), ok=False))
        self.assertEqual(self.tarea(11)['estado'], 'en-curso')

    # ── Recogida de los subagentes al cerrar (tarea 246) ──
    def con_subagente(self, rama: str, cambio_aux: bool = True) -> tuple[int, Path]:
        """Una tarea en curso con rama sin activar y un subagente en su worktree, con rama auxiliar sub-N, cuyo
        commit (si cambio_aux) se integra en la rama de la tarea, como hace el principal al revisarlo; sin él, el
        commit va directo a la rama de la tarea."""
        self.orden('crear', 'Con subagente', '--en-curso')
        id_ = self.leer()['ultimo']
        self.orden('rama', str(id_), rama, '--sin-activar')
        aux, wt = f'sub-{id_}', Path(self._tmp.name) / f'wt-{id_}'
        git(self.raiz, 'worktree', 'add', '-q', '-b', aux, str(wt), f'feature/{id_}-{rama}')
        self.orden('subagente', str(id_), '--worktree', wt.as_posix(), '--rama', aux)
        if cambio_aux:
            (wt / 'b.txt').write_text('b\n', encoding='utf-8')
            git(wt, 'add', 'b.txt')
            git(wt, 'commit', '-q', '-m', 'Del subagente')
            git(self.raiz, 'switch', '-q', f'feature/{id_}-{rama}')
            git(self.raiz, 'merge', '-q', '--ff-only', aux)
        else:  # el cambio, hecho en la rama de la tarea
            self.commit_en(f'feature/{id_}-{rama}', 'b.txt', 'b\n')
        git(self.raiz, 'switch', '-q', 'develop')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        return id_, wt

    def test_cerrar_recoge_el_subagente(self):
        id_, wt = self.con_subagente('tarea')
        mensaje = self.orden('cerrar', str(id_))
        self.assertIn('Quitados:', mensaje)
        self.assertNotIn('Aviso: q', mensaje)
        self.assertFalse(wt.exists())
        self.assertNotIn(f'sub-{id_}', git(self.raiz, 'branch'))
        self.assertNotIn(wt.as_posix(), git(self.raiz, 'worktree', 'list'))
        h = self.archivadas()[-1]['historial']
        self.assertEqual(h[-1]['evento'], 'recogida')
        self.assertIn(f'sub-{id_}', h[-1]['detalle'])

    def commit_sin_traer(self, wt: Path, nombre: str = 'c.txt') -> None:
        (wt / nombre).write_text('c\n', encoding='utf-8')  # un commit que el principal no trajo
        git(wt, 'add', nombre)
        git(wt, 'commit', '-q', '-m', 'Sin traer')

    def test_cerrar_y_a_observacion_se_niegan_con_commits_sin_traer(self):
        id_, wt = self.con_subagente('tarea')
        self.commit_sin_traer(wt)
        for orden in ('cerrar', 'a-observacion'):
            mensaje = self.orden(orden, str(id_), ok=False)
            self.assertIn(f'sin traer a feature/{id_}-tarea: sub-{id_} (1 commit)', mensaje)
            self.assertIn(f'git fetch . sub-{id_}:feature/{id_}-tarea', mensaje)
            self.assertIn(f'git merge --ff-only sub-{id_}', mensaje)
        t = self.tarea(id_)
        self.assertEqual((t['estado'], t['rama']), ('en-curso', f'feature/{id_}-tarea'))
        self.assertIn(f'feature/{id_}-tarea', self.ramas())
        self.assertTrue(wt.exists())
        # traído como dice el mensaje, ya cierra y recoge
        git(self.raiz, 'fetch', '-q', '.', f'sub-{id_}:feature/{id_}-tarea')
        mensaje = self.orden('cerrar', str(id_))
        self.assertIn('Quitados:', mensaje)
        self.assertNotIn(f'sub-{id_}', self.ramas())
        self.assertIn('c.txt', git(self.raiz, 'ls-tree', '--name-only', 'develop'))

    def test_se_niega_tambien_con_la_sub_sin_anotar(self):
        id_ = self.en_curso_con_rama()
        self.commit_en(f'feature/{id_}-tarea', 'b.txt', 'b\n')
        git(self.raiz, 'branch', f'sub-{id_}', f'feature/{id_}-tarea')
        self.commit_en(f'sub-{id_}', 'c.txt', 'c\n')
        git(self.raiz, 'switch', '-q', 'develop')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.assertIn(f'sub-{id_} (1 commit)', self.orden('cerrar', str(id_), ok=False))

    def test_cerrar_observada_conserva_la_auxiliar_con_commits_que_no_entraron(self):
        """En observación ya (la tarea entró en develop), el subagente hace otro commit: al cerrarla, la rama
        auxiliar y su worktree se quedan y se avisa; nunca se borran (decisión 169)."""
        id_, wt = self.con_subagente('tarea')
        (wt / 'a.txt').write_text('sucio\n', encoding='utf-8')
        self.orden('a-observacion', str(id_))  # queda el worktree, sucio
        git(wt, 'checkout', '--', 'a.txt')
        self.commit_sin_traer(wt)
        mensaje = self.orden('cerrar', str(id_))
        self.assertIn(f'sub-{id_} tiene 2 commits que no entraron en develop', mensaje)  # el traído, por squash, cuenta
        self.assertNotIn('Quitados', mensaje)
        self.assertIn(f'sub-{id_}', self.ramas())
        self.assertTrue(wt.exists())
        self.assertEqual(self.eventos(self.archivadas()[-1])[-1], 'recogida-con-avisos')

    def test_descartar_borra_la_auxiliar_aunque_tenga_commits_que_no_entraron(self):
        """El descarte descarta todo (decisión 189)."""
        id_, wt = self.con_subagente('tarea')
        self.commit_sin_traer(wt)
        mensaje = self.orden('descartar', str(id_))
        self.assertIn('Quitados:', mensaje)
        self.assertNotIn('Aviso', mensaje)
        self.assertNotIn(f'sub-{id_}', self.ramas())
        self.assertFalse(wt.exists())

    def test_descartar_quita_el_worktree_con_cambios_sin_commit(self):
        id_, wt = self.con_subagente('tarea')
        (wt / 'a.txt').write_text('sucio\n', encoding='utf-8')
        mensaje = self.orden('descartar', str(id_))
        self.assertIn('Quitados:', mensaje)
        self.assertNotIn('Aviso', mensaje)
        self.assertFalse(wt.exists())
        self.assertNotIn(f'sub-{id_}', self.ramas())

    def test_limpiar_quita_lo_que_quedo_de_una_descartada(self):
        """Lo que dejó un descarte de un cola.py anterior: worktree sucio y auxiliar con commits; limpiar lo quita."""
        id_, wt = self.con_subagente('tarea')
        self.orden('descartar', str(id_))
        git(self.raiz, 'worktree', 'add', '-q', '-b', f'sub-{id_}', str(wt), 'develop')
        self.commit_sin_traer(wt)
        (wt / 'a.txt').write_text('sucio\n', encoding='utf-8')
        datos = self.leer()
        t = next(x for x in datos['peticiones'] if x['id'] == id_)
        t['historial'].append({'evento': 'subagente', 'detalle': f'{wt.as_posix()} · sub-{id_}'})
        self.escribir(datos)
        self.assertIn(f'La {id_}: Quitados:', self.orden('limpiar'))
        self.assertNotIn(f'sub-{id_}', self.ramas())
        self.assertFalse(wt.exists())

    def test_cerrar_con_worktree_sucio_no_lo_quita_ni_falla(self):
        id_, wt = self.con_subagente('tarea')
        (wt / 'a.txt').write_text('sucio\n', encoding='utf-8')
        mensaje = self.orden('cerrar', str(id_))
        self.assertIn('Cerrada', mensaje)
        self.assertIn('cambios sin commit', mensaje)
        self.assertIn(f'queda la rama sub-{id_}', mensaje)
        self.assertTrue((wt / 'a.txt').exists())
        self.assertIn(f'sub-{id_}', git(self.raiz, 'branch'))
        h = self.archivadas()[-1]['historial']
        self.assertEqual(h[-1]['evento'], 'recogida-con-avisos')
        self.assertIn('cambios sin commit', h[-1]['detalle'])

    def test_cerrar_con_worktree_ya_quitado(self):
        id_, wt = self.con_subagente('tarea', cambio_aux=False)
        git(self.raiz, 'worktree', 'remove', str(wt))
        git(self.raiz, 'branch', '-D', f'sub-{id_}')
        mensaje = self.orden('cerrar', str(id_))
        self.assertNotIn('queda', mensaje)
        self.assertEqual(self.archivadas()[-1]['historial'][-1] | {'fecha': None},
                         {'evento': 'recogida', 'fecha': None, 'quien': 'principal', 'via': 'cli', 'detalle': 'nada que quitar'})

    def test_cerrar_con_carpeta_del_worktree_borrada(self):
        id_, wt = self.con_subagente('tarea', cambio_aux=False)
        shutil.rmtree(wt)
        self.assertIn('Quitados:', self.orden('cerrar', str(id_)))
        self.assertNotIn(wt.as_posix(), git(self.raiz, 'worktree', 'list'))
        self.assertNotIn(f'sub-{id_}', git(self.raiz, 'branch'))

    def test_descartar_recoge_el_subagente(self):
        id_, wt = self.con_subagente('tarea')
        mensaje = self.orden('descartar', str(id_))
        self.assertIn('Quitados:', mensaje)
        self.assertFalse(wt.exists())
        self.assertNotIn(f'sub-{id_}', git(self.raiz, 'branch'))
        self.assertEqual(self.eventos(self.tarea(id_))[-2:], ['descartada', 'recogida'])

    def test_cerrar_sin_subagente_no_anota_recogida(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.assertNotIn('Quitados', self.orden('cerrar', str(id_)))
        self.assertNotIn('recogida', self.eventos(self.archivadas()[-1]))

    def test_no_quita_la_carpeta_del_proyecto(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        git(self.raiz, 'switch', '-q', 'develop')
        self.orden('subagente', str(id_), '--worktree', str(self.raiz))
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.assertIn('es la carpeta del proyecto', self.orden('cerrar', str(id_)))
        self.assertTrue((self.raiz / 'a.txt').exists())

    def test_cerrar_observada_recoge_lo_que_quedo_y_no_repite(self):
        id_, wt = self.con_subagente('tarea')
        (wt / 'a.txt').write_text('sucio\n', encoding='utf-8')
        self.assertIn('cambios sin commit', self.orden('a-observacion', str(id_)))
        git(wt, 'checkout', '--', 'a.txt')  # el principal lo resuelve
        self.assertIn('Quitados:', self.orden('cerrar', str(id_)))
        self.assertFalse(wt.exists())
        self.assertEqual(self.eventos(self.archivadas()[-1])[-3:], ['recogida-con-avisos', 'cerrada', 'recogida'])

    def test_tras_una_recogida_completa_no_vuelve_a_anotarse(self):
        id_, _ = self.con_subagente('tarea')
        self.orden('a-observacion', str(id_))
        self.assertNotIn('Quitados', self.orden('cerrar', str(id_)))
        self.assertEqual(self.eventos(self.archivadas()[-1]).count('recogida'), 1)

    def test_eliminar_recoge_el_subagente_de_una_sin_rama(self):
        self.orden('crear', 'Investigar', '--en-curso')
        wt = Path(self._tmp.name) / 'wt-11'
        git(self.raiz, 'worktree', 'add', '-q', '-b', 'sub-11', str(wt), 'develop')
        self.orden('subagente', '11', '--worktree', wt.as_posix(), '--rama', 'sub-11')
        self.assertIn('Quitados:', self.orden('eliminar', '11'))
        self.assertFalse(wt.exists())
        self.assertNotIn('sub-11', git(self.raiz, 'branch'))
        self.assertEqual(self.eventos(self.archivadas()[-1])[-2:], ['recogida', 'eliminada'])
        self.orden('restaurar', '11')  # «eliminada», el último evento: se restaura igual
        self.assertEqual(self.tarea(11)['estado'], 'en-curso')

    def test_revertir_conserva_la_auxiliar_con_commits_que_nunca_entraron(self):
        id_, wt = self.con_subagente('tarea')
        (wt / 'a.txt').write_text('sucio\n', encoding='utf-8')
        self.orden('a-observacion', str(id_))  # queda el worktree, sucio
        git(wt, 'checkout', '--', 'a.txt')
        self.commit_sin_traer(wt)
        mensaje = self.orden('revertir', str(id_), '--pendiente')
        self.assertIn(f'quedan {wt.as_posix()} y sub-{id_}: sub-{id_} tiene', mensaje)
        self.assertNotIn('Quitados', mensaje)
        self.assertIn(f'sub-{id_}', self.ramas())
        self.assertTrue(wt.exists())

    def test_revertir_y_limpiar_recogen_lo_que_quedo(self):
        id_, wt = self.con_subagente('tarea')
        (wt / 'a.txt').write_text('sucio\n', encoding='utf-8')
        self.orden('a-observacion', str(id_))
        git(wt, 'checkout', '--', 'a.txt')
        self.assertIn('Quitados:', self.orden('revertir', str(id_), '--pendiente'))
        self.assertFalse(wt.exists())
        self.assertEqual(self.eventos(self.tarea(id_))[-3:], ['recogida', 'revertida', 'reabierta'])
        # limpiar, de una descartada sin restos: nada que quitar (lo que quedó, en test_limpiar_quita_lo_que_quedo…)
        id2, wt2 = self.con_subagente('otra', cambio_aux=False)
        self.orden('descartar', str(id2))
        self.assertFalse(wt2.exists())
        self.assertNotIn('Quitados', self.orden('limpiar'))

    def dos_con_rama(self) -> None:
        """La 11 y la 12 en curso, cada una con su rama sin activar y un commit en ella."""
        for nombre in ('una', 'dos'):
            self.orden('crear', nombre.capitalize(), '--en-curso')
            self.orden('rama', str(self.leer()['ultimo']), nombre, '--sin-activar')
        self.commit_en('feature/11-una', 'b.txt', 'b\n')
        self.commit_en('feature/12-dos', 'c.txt', 'c\n')
        git(self.raiz, 'switch', '-q', 'develop')

    def ramas(self) -> list:
        return git(self.raiz, 'branch', '--format=%(refname:short)').split()

    def test_fusionar_con_rama_integrada(self):
        self.dos_con_rama()
        git(self.raiz, 'branch', 'sub-11', 'feature/11-una')
        git(self.raiz, 'switch', '-q', 'feature/12-dos')
        git(self.raiz, 'merge', '-q', '--no-edit', 'feature/11-una')
        git(self.raiz, 'switch', '-q', 'develop')
        mensaje = self.orden('fusionar', '11', '12')
        self.assertIn('feature/11-una', mensaje)
        self.assertEqual(self.tarea(12)['rama'], 'feature/12-dos')
        self.assertNotIn('feature/11-una', self.ramas())
        self.assertNotIn('sub-11', self.ramas())
        self.assertIn('feature/12-dos', self.ramas())

    def test_fusionar_con_rama_ya_borrada(self):
        self.dos_con_rama()
        git(self.raiz, 'branch', '-D', 'feature/11-una')
        self.orden('fusionar', '11', '12')
        self.assertEqual(self.tarea(12)['rama'], 'feature/12-dos')
        self.assertIsNone(self.tarea(11))

    def test_fusionar_rama_destino_de_otra(self):
        self.dos_con_rama()
        git(self.raiz, 'switch', '-q', 'feature/12-dos')
        git(self.raiz, 'merge', '-q', '--no-edit', 'feature/11-una')
        git(self.raiz, 'switch', '-q', 'develop')
        self.orden('crear', 'Tres')  # la 13, sin rama: se lleva la que contiene a las demás
        self.assertIn('Rama: feature/12-dos', self.orden('fusionar', '11', '12', '13'))
        self.assertEqual(self.tarea(13)['rama'], 'feature/12-dos')
        self.assertNotIn('feature/11-una', self.ramas())

    def test_fusionar_rama_sin_integrar_no(self):
        self.dos_con_rama()
        mensaje = self.orden('fusionar', '11', '12', ok=False)
        self.assertIn('feature/11-una', mensaje)
        self.assertIn('feature/12-dos', mensaje)
        self.assertEqual(len(self.leer()['peticiones']), 2)
        self.assertIn('feature/11-una', self.ramas())

    def test_fusionar_recoge_el_subagente_de_la_absorbida(self):
        self.dos_con_rama()
        otro = Path(self._tmp.name) / 'otro'
        git(self.raiz, 'worktree', 'add', '-q', '-b', 'sub-11', str(otro), 'feature/11-una')
        self.orden('subagente', '11', '--worktree', otro.as_posix(), '--rama', 'sub-11')
        wt12 = Path(self._tmp.name) / 'wt-12'
        git(self.raiz, 'worktree', 'add', '-q', '-b', 'sub-12', str(wt12), 'feature/12-dos')
        self.orden('subagente', '12', '--worktree', wt12.as_posix(), '--rama', 'sub-12')
        git(self.raiz, 'switch', '-q', 'feature/12-dos')
        git(self.raiz, 'merge', '-q', '--no-edit', 'feature/11-una')
        git(self.raiz, 'switch', '-q', 'develop')
        self.assertIn('La 11: Quitados:', self.orden('fusionar', '11', '12'))
        self.assertFalse(otro.exists())
        self.assertNotIn('sub-11', self.ramas())
        self.assertTrue(wt12.exists())  # la que queda conserva el suyo
        self.assertIn('sub-12', self.ramas())
        self.assertEqual(self.eventos(self.archivadas()[-1])[-2:], ['recogida', 'absorbida'])

    def test_fusionar_con_subagente_sin_integrar_avisa_y_lo_deja(self):
        self.dos_con_rama()
        otro = Path(self._tmp.name) / 'otro'
        git(self.raiz, 'worktree', 'add', '-q', '-b', 'sub-11', str(otro), 'feature/11-una')
        self.orden('subagente', '11', '--worktree', otro.as_posix(), '--rama', 'sub-11')
        (otro / 'd.txt').write_text('d\n', encoding='utf-8')
        git(otro, 'add', 'd.txt')
        git(otro, 'commit', '-q', '-m', 'Sin integrar')
        git(self.raiz, 'switch', '-q', 'feature/12-dos')
        git(self.raiz, 'merge', '-q', '--no-edit', 'feature/11-una')
        git(self.raiz, 'switch', '-q', 'develop')
        mensaje = self.orden('fusionar', '11', '12')
        self.assertIn('sub-11 tiene 1 commit que no está en feature/12-dos', mensaje)
        self.assertTrue(otro.exists())
        self.assertIn('sub-11', self.ramas())
        self.assertNotIn('feature/11-una', self.ramas())

    def test_reabrir_limpia_el_worktree_viejo_aunque_tenga_cambios(self):
        id_, wt = self.con_subagente('tarea')
        (wt / 'a.txt').write_text('sucio\n', encoding='utf-8')
        self.assertIn('cambios sin commit', self.orden('a-observacion', str(id_)))
        mensaje = self.orden('reabrir', str(id_), 'falla', '--rama', 'segunda', '--sin-activar')
        self.assertIn('Quitados:', mensaje)
        self.assertNotIn('Aviso', mensaje)
        self.assertFalse(wt.exists())
        self.assertNotIn(f'sub-{id_}', self.ramas())
        self.assertEqual(self.eventos(self.tarea(id_))[-3:], ['recogida', 'reabierta', 'rama'])
        # el subagente nuevo puede usar la misma carpeta y la misma rama
        git(self.raiz, 'worktree', 'add', '-q', '-b', f'sub-{id_}', str(wt), f'feature/{id_}-segunda')

    def test_en_cola_sin_rama_si_con_commits_propios_no(self):  # decisión 170
        self.orden('crear', 'Sin rama', '--en-curso')
        self.assertIn('en cola', self.orden('en-cola', '11'))
        id_ = self.en_curso_con_rama()
        self.commit_en(f'feature/{id_}-tarea', 'a.txt', 'dos\n')
        mensaje = self.orden('en-cola', str(id_), ok=False)
        self.assertIn('1 commit que no está en develop', mensaje)
        self.assertIn('ciérrala, pásala a observación o descártala', mensaje)
        t = self.tarea(id_)
        self.assertEqual((t['estado'], t['rama']), ('en-curso', f'feature/{id_}-tarea'))
        self.assertIn(f'feature/{id_}-tarea', self.ramas())

    def test_en_cola_con_la_rama_vacia_la_borra(self):  # tarea 275
        id_ = self.en_curso_con_rama()  # activa, sin commits propios
        self.commit_en('develop', 'b.txt', 'b\n')  # develop sigue: la rama queda atrás, sigue vacía
        git(self.raiz, 'switch', '-q', f'feature/{id_}-tarea')
        mensaje = self.orden('en-cola', str(id_))
        self.assertIn(f'en cola; rama feature/{id_}-tarea borrada', mensaje)
        self.assertIn('Activa: develop.', mensaje)
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'develop')
        self.assertNotIn(f'feature/{id_}-tarea', self.ramas())
        t = self.tarea(id_)
        self.assertEqual((t['estado'], t.get('rama')), ('en-cola', None))
        self.assertEqual(t['historial'][-1]['detalle'], f'sin la rama feature/{id_}-tarea: borrada, sin commits propios')
        self.orden('en-curso', str(id_))  # se retoma con su número y una rama nueva
        self.orden('rama', str(id_), 'tarea')
        self.assertEqual(self.tarea(id_)['rama'], f'feature/{id_}-tarea')

    def test_en_cola_con_la_rama_borrada(self):  # tarea 275
        id_ = self.en_curso_con_rama()
        git(self.raiz, 'switch', '-q', 'develop')
        git(self.raiz, 'branch', '-D', f'feature/{id_}-tarea')
        self.assertIn('quitada: ya no existía', self.orden('en-cola', str(id_)))
        t = self.tarea(id_)
        self.assertEqual((t['estado'], t.get('rama')), ('en-cola', None))

    def subagente_vacio(self) -> tuple[int, Path]:
        """Una tarea en curso con rama sin activar y un subagente en su worktree (sub-N), los dos sin commits."""
        self.orden('crear', 'Con subagente', '--en-curso')
        id_ = self.leer()['ultimo']
        self.orden('rama', str(id_), 'tarea', '--sin-activar')
        wt = Path(self._tmp.name) / f'wt-{id_}'
        git(self.raiz, 'worktree', 'add', '-q', '-b', f'sub-{id_}', str(wt), f'feature/{id_}-tarea')
        self.orden('subagente', str(id_), '--worktree', wt.as_posix(), '--rama', f'sub-{id_}')
        return id_, wt

    def test_en_cola_recoge_el_subagente_vacio(self):  # tarea 275
        id_, wt = self.subagente_vacio()
        self.assertIn('Quitados:', self.orden('en-cola', str(id_)))
        self.assertFalse(wt.exists())
        self.assertNotIn(f'sub-{id_}', self.ramas())
        self.assertNotIn(f'feature/{id_}-tarea', self.ramas())
        self.assertEqual(self.eventos(self.tarea(id_))[-2:], ['recogida', 'en-cola'])

    def test_en_cola_se_niega_con_trabajo_del_subagente(self):  # tarea 275
        id_, wt = self.subagente_vacio()
        (wt / 'a.txt').write_text('sucio\n', encoding='utf-8')
        self.assertIn('cambios sin commit', self.orden('en-cola', str(id_), ok=False))
        git(wt, 'checkout', '--', 'a.txt')
        self.commit_sin_traer(wt)
        self.assertIn(f'sub-{id_} (1 commit)', self.orden('en-cola', str(id_), ok=False))
        self.assertEqual(self.tarea(id_)['estado'], 'en-curso')
        self.assertIn(f'feature/{id_}-tarea', self.ramas())
        self.assertTrue(wt.exists())

    def test_probar_activa_la_rama(self):
        self.orden('crear', 'Una', '--en-curso')
        self.orden('rama', '11', 'una', '--sin-activar')
        self.orden('listo', '11', '--prueba', 'mirar')
        self.assertIn('La 11, en prueba: rama feature/11-una activa. Prueba: mirar', self.orden('probar', '11'))
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'feature/11-una')
        t = self.tarea(11)
        self.assertEqual(t['estado'], 'en-curso')
        self.assertEqual([p['estado'] for p in t['pasos']], ['hecho', 'pendiente'])  # activar la rama es el paso de prueba (172); cerrarla, no

    def test_probar_con_la_rama_ya_activa_marca_el_paso(self):  # tarea 253: decisión 172, también si ya lo está
        self.orden('crear', 'Una', '--en-curso')
        self.orden('rama', '11', 'una')  # la deja activa
        self.orden('listo', '11', '--prueba', 'mirar')
        self.assertIn('La 11, en prueba: rama feature/11-una (ya era la activa). Prueba: mirar', self.orden('probar', '11'))
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'feature/11-una')
        t = self.tarea(11)
        self.assertEqual([p['estado'] for p in t['pasos']], ['hecho', 'pendiente'])
        self.assertEqual(self.eventos(t)[-1], 'probar')


    # ── probar integra develop antes de activar (tarea 270) ──
    def test_probar_integra_develop_sin_choques(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'b.txt', 'b\n')
        self.commit_en('develop', 'c.txt', 'c\n')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        self.assertIn('La 11, en prueba: rama feature/11-tarea activa, con develop integrado. Prueba: mirar',
                      self.orden('probar', str(id_)))
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'feature/11-tarea')
        self.assertTrue((self.raiz / 'b.txt').exists() and (self.raiz / 'c.txt').exists())
        git(self.raiz, 'merge-base', '--is-ancestor', 'develop', 'feature/11-tarea')
        t = self.tarea(11)
        self.assertEqual(t['pasos'][0]['estado'], 'hecho')
        self.assertEqual(t['historial'][-1]['detalle'], 'feature/11-tarea · con develop integrado')

    def test_probar_con_choques_lo_deshace_y_no_activa(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('feature/11-tarea', 'a.txt', 'rama\n')
        self.commit_en('develop', 'a.txt', 'develop\n')
        antes = git(self.raiz, 'rev-parse', 'feature/11-tarea')
        self.orden('listo', str(id_), '--prueba', 'mirar')
        r = self.respuesta('probar', str(id_), ok=False)
        self.assertIn('a.txt', r['mensaje'])
        self.assertIn('sigues en develop', r['mensaje'])
        self.assertEqual((r['fallo'], r['motivo']), ('choques', 'choques al integrar develop en feature/11-tarea: a.txt'))
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'develop')
        self.assertEqual(git(self.raiz, 'rev-parse', 'feature/11-tarea'), antes)
        self.assertEqual(git(self.raiz, 'status', '--porcelain', '--untracked-files=no'), '')
        t = self.tarea(11)
        self.assertEqual((t['pasos'][0]['estado'], self.eventos(t)[-1]), ('pendiente', 'probar-fallido'))

    def test_probar_con_choques_y_la_rama_ya_activa_la_deja_como_estaba(self):
        id_ = self.en_curso_con_rama()
        self.commit_en('develop', 'a.txt', 'develop\n')
        self.commit_en('feature/11-tarea', 'a.txt', 'rama\n')
        antes = git(self.raiz, 'rev-parse', 'HEAD')
        self.orden('probar', str(id_), ok=False)
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'feature/11-tarea')
        self.assertEqual(git(self.raiz, 'rev-parse', 'HEAD'), antes)
        self.assertEqual((self.raiz / 'a.txt').read_text(encoding='utf-8'), 'rama\n')

    def test_probar_con_trabajo_del_subagente_sin_traer_no_integra_ni_activa(self):
        id_, wt = self.con_subagente('tarea')
        (wt / 'c.txt').write_text('c\n', encoding='utf-8')  # el subagente sigue: commit sin traer
        git(wt, 'add', 'c.txt')
        git(wt, 'commit', '-q', '-m', 'Sin traer')
        self.commit_en('develop', 'd.txt', 'd\n')
        antes = git(self.raiz, 'rev-parse', f'feature/{id_}-tarea')
        r = self.respuesta('probar', str(id_), ok=False)
        self.assertIn(f'sub-{id_} (1 commit)', r['mensaje'])
        self.assertEqual(r['fallo'], 'sin-traer')
        self.assertIn(f'sub-{id_} (1 commit)', r['motivo'])
        self.assertEqual(git(self.raiz, 'branch', '--show-current'), 'develop')
        self.assertEqual(git(self.raiz, 'rev-parse', f'feature/{id_}-tarea'), antes)
        self.assertEqual(self.tarea(id_)['pasos'][-2]['estado'], 'pendiente')

    def test_probar_adelanta_la_rama_del_subagente(self):
        id_, wt = self.con_subagente('tarea')
        self.commit_en('develop', 'd.txt', 'd\n')
        self.assertNotIn('Aviso', self.orden('probar', str(id_)))
        self.assertEqual(git(self.raiz, 'rev-parse', f'sub-{id_}'), git(self.raiz, 'rev-parse', f'feature/{id_}-tarea'))
        self.assertTrue((wt / 'd.txt').exists())  # su worktree, al día: el siguiente --ff-only sigue valiendo

class Terminal(Base):
    def test_se_ejecuta_como_programa(self):
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(HERRAMIENTA), '--raiz', str(self.raiz), 'crear', 'Ñandú', '--descripcion', DESCRIPCION],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.tarea(11)['texto'], 'Ñandú')
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(HERRAMIENTA), '--raiz', str(self.raiz), 'en-cola', '11'],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 1)
        self.assertIn('en cola', r.stderr)

    def test_escribe_utf8_aunque_la_consola_sea_cp1252(self):
        self.orden('crear', 'A → B')
        entorno = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
        entorno |= {'PYTHONIOENCODING': 'cp1252', 'PYTHONUTF8': '0'}

        def ejecutar(*args):
            return subprocess.run([sys.executable, '-X', 'utf8=0', str(HERRAMIENTA), '--raiz', str(self.raiz), *args],
                                  capture_output=True, env=entorno)
        r = ejecutar('lista')
        self.assertEqual(r.returncode, 0, r.stderr.decode('utf-8', 'replace'))
        self.assertIn('A → B', r.stdout.decode('utf-8'))
        r = ejecutar('ver', '99')
        self.assertEqual(r.returncode, 1)
        self.assertIn('no está', r.stderr.decode('utf-8'))



class Lanzador(Base):
    """~/.claude/sf/cola.py (tarea 252): pasa la orden a la copia de cola.py de la sesión, la misma que lanza el panel."""

    def setUp(self):
        super().setUp()
        self.sf = Path(self._tmp.name) / 'home' / '.claude' / 'sf'
        self.sf.mkdir(parents=True)
        shutil.copy(HERRAMIENTA.parent / 'cola_sesion.py', self.sf / 'cola.py')

    def lanzar(self, sesion, *args, config=None):
        entorno = {k: v for k, v in os.environ.items() if k not in ('CLAUDE_CODE_SESSION_ID', 'CLAUDE_CONFIG_DIR')}
        if sesion is not None:
            entorno['CLAUDE_CODE_SESSION_ID'] = sesion
        if config is not None:
            entorno['CLAUDE_CONFIG_DIR'] = str(config)
        return subprocess.run([sys.executable, '-I', '-X', 'utf8', str(self.sf / 'cola.py'), '--raiz', str(self.raiz), *args],
                              capture_output=True, text=True, encoding='utf-8', env=entorno)

    def test_lanza_la_copia_de_la_sesion_y_no_otra(self):
        shutil.copy(HERRAMIENTA, self.sf / 'cola-s1.py')
        (self.sf / 'cola-s2.py').write_text('raise SystemExit("otra sesión")', encoding='utf-8')
        r = self.lanzar('s1', 'crear', 'Ñandú', '--descripcion', DESCRIPCION)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.tarea(11)['texto'], 'Ñandú')
        r = self.lanzar('s1', 'en-cola', '11')
        self.assertEqual(r.returncode, 1)
        self.assertIn('en cola', r.stderr)

    def test_con_claude_config_dir_lanza_la_copia_de_esa_carpeta(self):
        # Una configuración aparte (tarea 269): el panel deja la copia en $CLAUDE_CONFIG_DIR/sf; la de ~/.claude/sf no.
        config = Path(self._tmp.name) / 'config'
        (config / 'sf').mkdir(parents=True)
        shutil.copy(HERRAMIENTA, config / 'sf' / 'cola-s1.py')
        (self.sf / 'cola-s1.py').write_text('raise SystemExit("la de ~/.claude")', encoding='utf-8')
        r = self.lanzar('s1', 'crear', 'Ñandú', '--descripcion', DESCRIPCION, config=config)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.tarea(11)['texto'], 'Ñandú')
        r = self.lanzar('s2', 'crear', 'X', config=config)
        self.assertEqual(r.returncode, 2)
        self.assertIn(str(config / 'sf' / 'cola-s2.py'), r.stderr)

    def test_la_copia_del_panel_encuentra_indice_decisiones_en_su_plugin(self):
        # Tarea 322: la copia, sola en ~/.claude/sf, lleva en su primera línea la raíz del plugin (como la escribe
        # copiarCola en hooks/cola.ts) y «decision» usa el indice_decisiones.py de allí.
        texto = HERRAMIENTA.read_text(encoding='utf-8')
        (self.sf / 'cola-s1.py').write_text(f'# sf-plugin: {HERRAMIENTA.parents[1]}\n{texto}', encoding='utf-8')
        (self.sf / 'cola-s2.py').write_text(texto, encoding='utf-8')  # sin la línea: dice qué falta
        carpeta = self.raiz / 'sf' / 'decisiones'
        carpeta.mkdir(parents=True)
        r = self.lanzar('s2', '--json', 'decision', 'Sin plugin', '--texto', 'Texto.')
        self.assertEqual(r.returncode, 1)
        self.assertIn('indice_decisiones.py', r.stdout)
        r = self.lanzar('s1', '--json', 'decision', 'Desde la copia', '--texto', 'Texto.')
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        self.assertEqual(json.loads(r.stdout.strip().splitlines()[-1])['numero'], 1)
        self.assertTrue(list(carpeta.glob('001-*-desde-la-copia.md')))
        self.assertTrue((carpeta / 'README.md').is_file())

    def test_sin_sesion_o_sin_copia_sale_con_2_sin_tocar_la_cola(self):
        antes = self.archivo.read_text(encoding='utf-8')
        r = self.lanzar(None, 'crear', 'X')
        self.assertEqual(r.returncode, 2)
        self.assertIn('CLAUDE_CODE_SESSION_ID', r.stderr)
        r = self.lanzar('sin-copia', 'crear', 'X')
        self.assertEqual(r.returncode, 2)
        self.assertIn('/reload-plugins', r.stderr)
        self.assertEqual(self.archivo.read_text(encoding='utf-8'), antes)


class Choques(Base):
    """«choques N»: archivos que la N comparte con las en curso o en observación (decisión 130)."""
    git = True

    def choques(self, *args: str) -> tuple[int, dict]:
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            codigo = cola.main(['--raiz', str(self.raiz), '--json', 'choques', *args])
        return codigo, json.loads(salida.getvalue())

    def con_rama(self, archivo: str, en_curso: bool = True) -> int:
        self.orden('crear', f'Toca {archivo}', *(['--en-curso'] if en_curso else []))
        id_ = self.leer()['ultimo']
        if en_curso:
            self.orden('rama', str(id_), f't{id_}', '--sin-activar')
            self.commit_en(f'feature/{id_}-t{id_}', archivo, f'{id_}\n')
            git(self.raiz, 'switch', '-q', 'develop')
        return id_

    def test_comparte_un_archivo(self):
        otra = self.con_rama('a.txt')
        self.con_rama('b.txt')
        self.orden('crear', 'Nueva')
        n = str(self.leer()['ultimo'])
        codigo, r = self.choques(n, '--archivos', 'a.txt', 'c.txt')
        self.assertEqual(codigo, cola.CON_CHOQUES)
        self.assertTrue(r['ok'])
        self.assertEqual([(c['id'], c['archivos']) for c in r['choques']], [(otra, ['a.txt'])])
        self.assertIn('fusionar', r['mensaje'])

    def test_sin_choques_sale_con_0(self):
        self.con_rama('a.txt')
        self.orden('crear', 'Nueva')
        codigo, r = self.choques(str(self.leer()['ultimo']), '--archivos', '.\\docs\\c.txt')
        self.assertEqual((codigo, r['choques'], r['archivos']), (0, [], ['docs/c.txt']))

    def test_con_rama_propia_y_en_observacion(self):
        otra = self.con_rama('a.txt')
        datos = self.leer()
        datos['peticiones'][0]['estado'] = 'en-observacion'
        self.escribir(datos)
        n = self.con_rama('a.txt')
        codigo, r = self.choques(str(n))
        self.assertEqual(codigo, cola.CON_CHOQUES)
        self.assertEqual(r['choques'][0]['id'], otra)

    def test_rama_auxiliar_y_worktree_sin_commit(self):
        otra = self.con_rama('a.txt')
        git(self.raiz, 'branch', 'auxiliar', 'develop')
        wt = Path(self._tmp.name) / 'wt'
        git(self.raiz, 'worktree', 'add', '-q', str(wt), 'auxiliar')
        (wt / 'nuevo.txt').write_text('x\n', encoding='utf-8')
        self.orden('subagente', str(otra), '--worktree', str(wt), '--rama', 'auxiliar')
        self.orden('crear', 'Nueva')
        codigo, r = self.choques(str(self.leer()['ultimo']), '--archivos', 'nuevo.txt')
        self.assertEqual((codigo, r['choques'][0]['archivos']), (cola.CON_CHOQUES, ['nuevo.txt']))

    def test_rama_que_no_existe_no_falla(self):
        otra = self.con_rama('a.txt')
        git(self.raiz, 'branch', '-D', f'feature/{otra}-t{otra}')
        self.orden('crear', 'Nueva')
        codigo, r = self.choques(str(self.leer()['ultimo']), '--archivos', 'a.txt')
        self.assertEqual((codigo, r['choques'], r['sin_rama']), (0, [], [otra]))

    def test_sin_archivos_no(self):
        self.orden('crear', 'Nueva')
        codigo, r = self.choques(str(self.leer()['ultimo']))
        self.assertEqual((codigo, r['ok']), (1, False))
        self.assertIn('--archivos', r['mensaje'])

    def test_no_escribe_la_cola(self):
        self.con_rama('a.txt')
        self.orden('crear', 'Nueva')
        antes = self.archivo.read_bytes()
        self.choques(str(self.leer()['ultimo']), '--archivos', 'a.txt')
        self.assertEqual(self.archivo.read_bytes(), antes)


class Configuracion(unittest.TestCase):
    """leer_configuracion: los valores por defecto donde falta un campo o no se entiende (informe «Configuración
    inicial»)."""

    def test_por_defecto(self):
        c = cola.leer_configuracion({'sf': '1.4.0', 'proyecto': 'Demo', 'color': 'green'})
        self.assertEqual({k: c[k] for k in ('proyecto', 'idioma', 'commits', 'remoto', 'rama_main', 'manifiesto',
                                            'metodologia', 'kanban', 'desconocidos')},
                         {'proyecto': 'Demo', 'idioma': 'es', 'commits': 'libre', 'remoto': 'origin',
                          'rama_main': 'main', 'manifiesto': [], 'metodologia': True, 'kanban': None,
                          'desconocidos': []})

    def test_campos(self):
        c = cola.leer_configuracion({'idioma': 'ca', 'commits': 'conventional', 'remoto': 'PoseTracker',
                                     'rama_main': 'master', 'metodologia': False,
                                     'manifiesto': ['frontend/package.json', 'backend/pyproject.toml'],
                                     'kanban': {'proveedor': 'jkanban', 'proyecto': 'JKanban'}})
        self.assertEqual((c['idioma'], c['commits'], c['remoto'], c['rama_main'], c['metodologia']),
                         ('ca', 'conventional', 'PoseTracker', 'master', False))
        self.assertEqual(c['manifiesto'], ['frontend/package.json', 'backend/pyproject.toml'])
        self.assertEqual(c['kanban'], {'proveedor': 'jkanban', 'proyecto': 'JKanban'})
        self.assertEqual(cola.leer_configuracion({'manifiesto': 'package.json'})['manifiesto'], ['package.json'])
        self.assertEqual(cola.leer_configuracion({'manifiesto': None})['manifiesto'], [])

    def test_kanban_en_cadena_es_jkanban(self):
        self.assertEqual(cola.leer_configuracion({'kanban': 'JKanban'})['kanban'],
                         {'proveedor': 'jkanban', 'proyecto': 'JKanban'})

    def test_desconocidos_valen_lo_de_por_defecto(self):
        c = cola.leer_configuracion({'commits': 'gitmoji', 'remoto': None, 'idioma': 'Español', 'rama_main': '',
                                     'manifiesto': ['pom.xml', 'package.json'], 'metodologia': 'sí',
                                     'kanban': {'proveedor': 'github'}})
        self.assertEqual((c['commits'], c['remoto'], c['idioma'], c['rama_main'], c['metodologia'], c['kanban']),
                         ('libre', 'origin', 'es', 'main', True, None))
        self.assertEqual(c['manifiesto'], ['package.json'])
        self.assertEqual(sorted(c['desconocidos']),
                         ['commits', 'idioma', 'kanban', 'manifiesto', 'metodologia', 'rama_main', 'remoto'])

    def test_la_sf_por_su_marca(self):
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d)
            (repo / 'plugins/sf/.claude-plugin').mkdir(parents=True)
            (repo / cola.MARCA_SF).write_text('{"version": "1.4.2"}', encoding='utf-8')
            c = cola.configuracion(repo)
            self.assertEqual((c['manifiesto'], c['remoto'], c['rama_main'], c['proyecto']),
                             ([cola.MARCA_SF], 'origin', 'main', None))
            self.assertEqual(cola.nombre_proyecto(repo), repo.name)

    def test_mensaje_de_tarea(self):
        self.assertEqual(cola.mensaje_de_tarea('Lista', '- Hecho\n', 7, 'libre', coautor=cola.COAUTOR),
                         f'Lista (7)\n\n- Hecho\n\n{cola.COAUTOR}\n')
        self.assertEqual(cola.mensaje_de_tarea('feat: lista', '', 7, 'conventional', coautor=cola.COAUTOR),
                         f'feat: lista\n\nSF-Tarea: 7\n{cola.COAUTOR}\n')
        # Sin línea de coautoría (238): nada al pie con libres; solo el trailer con conventional.
        self.assertEqual(cola.mensaje_de_tarea('Lista', '- Hecho\n', 7, 'libre'), 'Lista (7)\n\n- Hecho\n')
        self.assertEqual(cola.mensaje_de_tarea('Lista', '', 7, 'libre'), 'Lista (7)\n')
        self.assertEqual(cola.mensaje_de_tarea('feat: lista', '', 7, 'conventional'), 'feat: lista\n\nSF-Tarea: 7\n')

    def test_coautor_en_la_configuracion(self):
        leer = lambda d, sf=False: cola.leer_configuracion(d, es_sf=sf)
        self.assertIsNone(leer({})['coautor'])
        self.assertEqual(leer({}, True)['coautor'], cola.COAUTOR)
        self.assertEqual(leer({'coautor': 'Ana <a@x.com>'})['coautor'], 'Co-Authored-By: Ana <a@x.com>')
        self.assertEqual(leer({'coautor': ' co-authored-by: Ana <a@x.com> '})['coautor'], 'co-authored-by: Ana <a@x.com>')
        # En la SF, null o vacío la quita; un valor que no se entiende vale como si faltara y se nombra.
        self.assertIsNone(leer({'coautor': None}, True)['coautor'])
        self.assertIsNone(leer({'coautor': ''})['coautor'])
        for raro in ('a\nb', 7, ['x']):
            c = leer({'coautor': raro})
            self.assertEqual((c['coautor'], c['desconocidos']), (None, ['coautor']))

    def test_motivo_de_git_la_linea_que_explica(self):
        sin_remoto = subprocess.CompletedProcess([], 128, '', "fatal: 'origin' does not appear to be a git repository\n"
                                                 'fatal: Could not read from remote repository.\n\nPlease make sure you '
                                                 'have the correct access rights\nand the repository exists.\n')
        self.assertEqual(cola.motivo(sin_remoto), "fatal: 'origin' does not appear to be a git repository")
        self.assertEqual(cola.motivo(subprocess.CompletedProcess([], 1, 'Algo\nOtra cosa\n', '')), 'Otra cosa')
        self.assertEqual(cola.motivo(subprocess.CompletedProcess([], 1, '', '')), 'git no responde')
        self.assertEqual(cola.motivo_bytes(subprocess.CompletedProcess([], 1, b'', b'hint: x\r\nerror: no va\r\n')),
                         'error: no va')

    def test_orden_python(self):
        with mock.patch.object(cola.sys, 'executable', '/usr/bin/python3'), \
                mock.patch.object(cola.shutil, 'which', lambda n: '/usr/bin/python3'):
            self.assertEqual(cola.orden_python(), 'python3')
        with mock.patch.object(cola.sys, 'executable', '/opt/py/bin/python3.12'), \
                mock.patch.object(cola.shutil, 'which', lambda n: None):
            self.assertEqual(cola.orden_python(), '/opt/py/bin/python3.12')
        with mock.patch.object(cola.sys, 'executable', 'C:/Python313/python.exe'):
            self.assertEqual(cola.orden_python(), 'python')
        with mock.patch.object(cola.sys, 'executable', ''):
            self.assertEqual(cola.orden_python(), 'python')

    def test_misma_ruta_tras_resolver_enlaces(self):
        # En macOS, /var es un enlace a /private/var: git puede dar el worktree con la ruta resuelta.
        with mock.patch.object(cola.os.path, 'realpath', lambda x: '/private' + x if x.startswith('/var/') else x):
            self.assertTrue(cola.misma_ruta('/var/t/wt-1', '/private/var/t/wt-1'))
            self.assertFalse(cola.misma_ruta('/var/t/wt-1', '/private/var/t/wt-2'))

    def test_prefijo_del_tipo_de_tarea(self):
        titulo = lambda tipo, formato='conventional', t='Lista de tareas': cola.mensaje_de_tarea(
            t, '', 7, formato, tipo).split('\n')[0]
        for tipo, prefijo in (('implementar', 'feat'), ('corregir', 'fix'), ('documentar', 'docs'),
                              ('especificar', 'docs'), ('investigar', 'docs'), ('deliberar', 'docs'),
                              ('diseñar', 'docs'), (None, 'chore')):
            self.assertEqual(titulo(tipo), f'{prefijo}: Lista de tareas')
        self.assertEqual(titulo('corregir', 'propio'), 'fix: Lista de tareas')
        self.assertEqual(titulo('implementar', 'libre'), 'Lista de tareas (7)')
        self.assertEqual(titulo('implementar', t='fix(panel): ya lleva'), 'fix(panel): ya lleva')

    def test_tareas_en_develop_acepta_las_dos_formas(self):
        lineas = [
            'h6\tRevert "feat: otra"\t',
            'h5\tfeat: otra\t9',
            'h4\tTercera (8)\t',
            'h3\tRevert "Segunda (8)"\t',
            'h2\tSegunda (8)\t',
            'h1\tfeat: primera\t9',
            'h0\tSin tarea\t',
        ]
        self.assertEqual(cola.tareas_en_develop(lineas), {8: ['h4']})
        self.assertEqual(cola.tareas_en_develop(lineas[1:]), {9: ['h5', 'h1'], 8: ['h4']})


class Encargo(Base):
    def setUp(self):
        super().setUp()
        self.orden('crear', 'Encargo fijo', '--en-curso')
        self.orden('subagente', '11', '--worktree', 'D:/wt-11', '--rama', 'sub-11')

    def test_con_worktree_rama_y_reglas(self):
        r = self.respuesta('encargo', '11')
        m = r['mensaje']
        self.assertTrue(m.startswith('Tarea 11 de proyecto: «Encargo fijo».'))
        self.assertIn('Worktree: D:/wt-11, rama auxiliar sub-11', m)
        for texto in ('No escribas la cola', 'No cargues sf:orquestacion', 'claude-sf.md', '«(11)»',
                      'sin línea de coautoría', 'decisión del propietario', 'no lo sortees', 'Qué mirar en la prueba'):
            self.assertIn(texto, m)
        self.assertEqual((r['encargo'], r['worktree'], r['rama_auxiliar']), (m, 'D:/wt-11', 'sub-11'))

    def test_lo_comprobado_en_lista_para_pasos(self):
        self.orden('crear', 'Deliberar', '--tipo', 'deliberar', '--en-curso')
        for n in ('11', '12'):  # con rama y deliberativa
            self.assertIn('- Lo comprobado: una línea por comprobación, con su resultado («Comprobado: 300 pruebas de '
                          'Python, sin fallos»), lista para pasar a pasos hechos; lo no comprobado, como tal.', self.orden('encargo', n))

    def test_no_escribe_la_cola(self):
        antes = self.archivo.read_bytes()
        self.orden('encargo', '11')
        self.assertEqual(self.archivo.read_bytes(), antes)

    def test_el_ultimo_subagente_y_la_rama_de_la_tarea(self):
        t = self.leer()
        t['peticiones'][0]['rama'] = 'feature/11-encargo'
        self.escribir(t)
        self.orden('subagente', '11', '--worktree', 'D:/wt-11b', '--rama', 'sub-11b')
        m = self.orden('encargo', '11')
        self.assertIn('Worktree: D:/wt-11b, rama auxiliar sub-11b (nunca la rama de la tarea, feature/11-encargo', m)

    def test_proyecto_json_nombre_y_coautor(self):
        (self.raiz / '.sf' / 'proyecto.json').write_text(
            json.dumps({'proyecto': 'Lectura', 'coautor': 'Co-Authored-By: X <x@example.com>'}), encoding='utf-8')
        m = self.orden('encargo', '11')
        self.assertIn('Tarea 11 de Lectura', m)
        self.assertIn('terminados en «Co-Authored-By: X <x@example.com>»', m)
        m = self.orden('encargo', '11', '--coautor', 'Co-Authored-By: Y <y@example.com>')
        self.assertIn('«Co-Authored-By: Y <y@example.com>»', m)

    def test_python_de_la_maquina(self):
        with mock.patch.object(cola, 'orden_python', lambda: 'python3'):
            m = self.orden('encargo', '11')
        self.assertIn('- Python, en esta máquina: «python3», no «python»', m)
        with mock.patch.object(cola, 'orden_python', lambda: 'python'):
            self.assertNotIn('Python, en esta máquina', self.orden('encargo', '11'))

    def test_convenciones_y_marca_del_numero(self):
        m = self.orden('encargo', '11')
        self.assertIn('- Convenciones del proyecto: idioma es; commits libres, con el número de la tarea como '
                      '«(N)» al final del título; remoto origin.', m)
        (self.raiz / '.sf' / 'proyecto.json').write_text(json.dumps(
            {'proyecto': 'JKanban', 'idioma': 'en', 'commits': 'conventional', 'rama_main': 'master'}),
            encoding='utf-8')
        m = self.orden('encargo', '11')
        self.assertIn('con el trailer «SF-Tarea: 11» al pie', m)
        self.assertNotIn('«(11)»', m)
        self.assertIn('idioma en; commits conventional commits', m)
        self.assertIn('se publica en master, que hace de main.', m)

    def test_interruptor_apagado(self):
        (self.raiz / '.sf' / 'proyecto.json').write_text(
            json.dumps({'automatizaciones': {'encargo_subagente': False}}), encoding='utf-8')
        self.assertIn('apagado', self.orden('encargo', '11', ok=False))

    def test_sin_subagente_o_fuera_de_curso(self):
        self.orden('crear', 'Otra', '--en-curso')
        self.assertIn('cola.py subagente 12', self.orden('encargo', '12', ok=False))
        self.orden('crear', 'En cola')
        self.orden('encargo', '13', ok=False)
        self.orden('encargo', '99', ok=False)


class Deliberativas(Base):
    """Las deliberativas (investigar, deliberar, diseñar) no tienen rama, worktree ni rama auxiliar, ni se prueban
    (decisiones 218, 256 y 278; tarea 345)."""
    git = True

    def textos(self, id_: int) -> list:
        return [x['texto'] for x in self.tarea(id_)['pasos']]

    def test_en_curso_sin_paso_de_activar_rama(self):
        for tipo in cola.DELIBERATIVAS:
            r = self.respuesta('crear', f'Pensar {tipo}', '--tipo', tipo, '--en-curso')
            self.assertEqual(self.textos(r['id']), ['Cerrar la tarea'])
        self.orden('crear', 'Hacer', '--tipo', 'implementar', '--en-curso')
        self.assertEqual(self.textos(14), list(cola.PASOS_CIERRE))

    def test_rama_y_subagente_se_niegan(self):
        self.orden('crear', 'Investigar', '--tipo', 'investigar', '--en-curso')
        self.assertIn('deliberativa', self.orden('rama', '11', 'investigar', '--sin-activar', ok=False))
        self.assertIn('deliberativa', self.orden('subagente', '11', '--worktree', '../wt', '--rama', 'sub-11', ok=False))
        self.assertNotIn('feature/11-investigar', git(self.raiz, 'branch'))
        self.assertIsNone(self.tarea(11).get('rama'))

    def test_encargo_sin_worktree(self):
        self.orden('crear', 'Deliberar', '--tipo', 'deliberar', '--en-curso')
        r = self.respuesta('encargo', '11')
        self.assertTrue(r['sin_rama'])
        self.assertIsNone(r['worktree'])
        self.assertIn('Sin rama, worktree ni rama auxiliar', r['encargo'])
        self.assertNotIn('Qué mirar en la prueba', r['encargo'])

    def test_cierra_sin_rama_y_no_va_a_observacion(self):
        self.orden('crear', 'Deliberar', '--tipo', 'deliberar', '--en-curso')
        self.orden('paso', 'añadir', '11', 'Escribir el informe')
        self.orden('paso', 'marcar', '11', '1', 'hecho')
        self.assertIn('observación', self.orden('a-observacion', '11', ok=False))
        self.assertIn('sin rama', self.orden('cerrar', '11'))
        self.assertEqual(self.archivadas()[-1]['estado'], 'cerrada')

    def test_cambiar_el_tipo_pone_o_quita_activar_rama(self):
        self.orden('crear', 'Algo', '--tipo', 'implementar', '--en-curso')
        self.assertIn('quitado', self.orden('tipo', '11', 'investigar'))
        self.assertEqual(self.textos(11), ['Cerrar la tarea'])
        self.assertIn('añadido', self.orden('tipo', '11', 'corregir'))
        self.assertEqual(self.textos(11), list(cola.PASOS_CIERRE))

    def test_al_cargar_una_deliberativa_pierde_activar_rama(self):
        self.escribir({'ultimo': 11, 'peticiones': [{'id': 11, 'texto': 'Vieja', 'tipo': 'investigar', 'estado': 'en-curso',
                                                     'pasos': [{'texto': x, 'estado': 'pendiente'} for x in cola.PASOS_CIERRE]}]})
        self.orden('paso', 'añadir', '11', 'Leer')
        self.assertEqual(self.textos(11), ['Leer', 'Cerrar la tarea'])

    def test_reabrir_deliberativa_sin_rama(self):
        self.orden('crear', 'Deliberar', '--tipo', 'deliberar', '--en-curso')
        self.orden('cerrar', '11')
        self.assertIn('deliberativa', self.orden('reabrir', '11', 'Falta algo'))
        self.assertIsNone(self.tarea(11).get('rama'))
        self.orden('cerrar', '11')
        self.assertIn('deliberativa', self.orden('reabrir', '11', 'otra', '--rama', 'x', ok=False))


class RamaVacia(Base):
    """Una rama sin cambios respecto a develop se cierra sin commit: se borra y la tarea sale de la cola (tarea 345;
    antes, el squash fallaba con «nothing added to commit»)."""
    git = True

    def preparar(self, activar: bool = False) -> str:
        self.orden('crear', 'Vacía', '--tipo', 'corregir', '--en-curso')
        self.orden('rama', '11', 'vacia', *([] if activar else ['--sin-activar']))
        return git(self.raiz, 'rev-parse', 'develop')

    def test_cerrar_rama_sin_commits(self):
        antes = self.preparar()
        (self.raiz / 'suelto.txt').write_text('sin seguir\n', encoding='utf-8')  # «untracked files present»
        self.assertIn('sin commit', self.orden('cerrar', '11'))
        self.assertEqual(git(self.raiz, 'rev-parse', 'develop'), antes)
        self.assertNotIn('feature/11-vacia', git(self.raiz, 'branch'))
        self.assertIsNone(self.tarea(11))
        salida = self.archivadas()[-1]
        self.assertEqual(salida['estado'], 'cerrada')
        self.assertNotIn('commit', salida)

    def test_cerrar_rama_activa_sin_cambios(self):
        antes = self.preparar(activar=True)
        self.assertIn('sin commit', self.orden('cerrar', '11'))
        self.assertEqual((git(self.raiz, 'branch', '--show-current'), git(self.raiz, 'rev-parse', 'develop')),
                         ('develop', antes))

    def test_cerrar_rama_cuyo_cambio_ya_esta_en_develop(self):
        self.preparar()
        self.commit_en('feature/11-vacia', 'a.txt', 'dos\n')
        self.commit_en('develop', 'a.txt', 'dos\n')
        antes = git(self.raiz, 'rev-parse', 'develop')
        self.assertIn('sin commit', self.orden('cerrar', '11'))
        self.assertEqual(git(self.raiz, 'rev-parse', 'develop'), antes)
        self.assertNotIn('feature/11-vacia', git(self.raiz, 'branch'))

    def test_cerrar_recoge_la_auxiliar_vacia(self):
        self.preparar()
        wt = self.raiz.parent / 'wt-11'
        git(self.raiz, 'worktree', 'add', '-q', '-b', 'sub-11', str(wt), 'feature/11-vacia')
        self.orden('subagente', '11', '--worktree', str(wt), '--rama', 'sub-11')
        self.orden('cerrar', '11')
        self.assertNotIn('sub-11', git(self.raiz, 'branch'))
        self.assertFalse(wt.exists())

    def test_a_observacion_se_niega(self):
        self.preparar()
        self.assertIn('nada que observar', self.orden('a-observacion', '11', ok=False))
        self.assertEqual(self.tarea(11)['estado'], 'en-curso')


if __name__ == '__main__':
    unittest.main()
