"""Pruebas de tools/revision_publica.py: la revisión de lo que sale en una versión (decisión 252).

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"

Los secretos, correos y rutas de prueba se componen al correr: este archivo también se publica y la revisión no debe
encontrarlos en él.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERRAMIENTA = Path(__file__).resolve().parents[1] / 'tools' / 'revision_publica.py'
TOKEN = 'ghp' + '_' + 'a1B2' * 9
CORREO_AJENO = 'ana.ruiz' + '@' + 'correo.es'
AUTORA = 'autora' + '@' + 'dominio.es'
CARPETA = 'C:' + '/Users/' + 'lucia' + '/notas.txt'


class Revision(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.raiz = Path(self._tmp.name) / 'proyecto'
        self.raiz.mkdir()
        self.git('init', '-q', '-b', 'develop')
        self.git('config', 'user.name', 'Autora')
        self.git('config', 'user.email', AUTORA)
        self.git('config', 'commit.gpgsign', 'false')
        # Lo ya publicado: una ruta de la máquina en un documento, en v0.1.0.
        self.ruta_vieja = (Path(self._tmp.name) / 'Otro').as_posix()
        self.commit({'docs/a.md': f'Ver {self.ruta_vieja}\n'}, 'Primero')
        self.git('tag', '-a', 'v0.1.0', '-m', 'v0.1.0')

    def tearDown(self):
        self._tmp.cleanup()

    def git(self, *args: str) -> str:
        r = subprocess.run(['git', '-C', str(self.raiz), *args], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def commit(self, archivos: dict, mensaje: str) -> None:
        for ruta, texto in archivos.items():
            (self.raiz / ruta).parent.mkdir(parents=True, exist_ok=True)
            (self.raiz / ruta).write_text(texto, encoding='utf-8')
        self.git('add', '-A')
        self.git('commit', '-q', '-m', mensaje)

    def revisar(self, *args: str, codigo: int | None = None) -> dict:
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(HERRAMIENTA), '--repo', str(self.raiz), '--json',
                            *args], capture_output=True, text=True, encoding='utf-8')
        if codigo is not None:
            self.assertEqual(r.returncode, codigo, r.stdout + r.stderr)
        return json.loads(r.stdout.strip().splitlines()[-1])

    def motivos(self, r: dict) -> list[tuple[str, str, str]]:
        return [(x['donde'], x['motivo'], x['texto']) for x in r['hallazgos']]

    def test_sin_nada_sale_con_0(self):
        self.commit({'docs/b.md': 'Nada raro. Co-Authored-By: Claude <noreply@anthropic.com>\n'}, 'Segundo')
        r = self.revisar('--desde', 'v0.1.0', codigo=0)
        self.assertEqual((r['commits'], r['hallazgos']), (1, []))

    def test_distingue_lo_ya_subido_de_lo_nuevo(self):
        self.commit({'src/a.py': f'# {CORREO_AJENO}\n'}, 'Subido')
        self.git('update-ref', 'refs/remotes/origin/develop', 'HEAD')
        otro = 'luis' + '@' + 'correo.es'
        self.commit({'src/b.py': f'# {otro}\n'}, 'Nuevo')
        r = self.revisar('--desde', 'v0.1.0', codigo=3)
        self.assertEqual([(x['texto'], x['nivel']) for x in r['hallazgos']], [(otro, 'nuevo'), (CORREO_AJENO, 'subido')])

    def decidir(self, *args: str, codigo: int, accion: str | None = 'release') -> dict:
        r = self.revisar('--decidir', '--repetir', 'repite', *(('--accion', accion) if accion else ()), *args,
                         codigo=codigo)
        self.assertTrue(r['ok'])
        return r

    def permisos(self) -> Path:
        comun = self.git('rev-parse', '--git-common-dir').strip()
        return (self.raiz / comun).resolve() / 'sf-revision.json'

    def test_mirar_a_mano_no_da_permiso(self):
        # Tarea 332: lanzar la revisión a mano, aunque sea con --decidir y dos veces, no anota ni acepta nada.
        self.git('remote', 'add', 'origin', str(Path(self._tmp.name) / 'remoto.git'))
        self.commit({'src/a.py': f'# {CORREO_AJENO}\n'}, 'Nuevo')
        self.revisar(codigo=3)
        for _ in range(3):
            r = self.decidir(codigo=3, accion=None)
            self.assertEqual(r['accion'], 'permiso')
            self.assertIn('Solo se ha mirado', r['mensaje'])
        self.assertFalse(self.permisos().exists())
        # Y no cuenta como primer intento: la acción real pregunta y solo su repetición da el permiso.
        self.assertEqual(self.decidir(codigo=3)['accion'], 'permiso')
        self.decidir(codigo=3, accion=None)
        self.assertEqual(self.decidir(codigo=0)['mensaje'], 'aceptadas 1 cosas de la revisión')

    def test_el_permiso_lo_da_repetir_la_misma_accion(self):
        self.git('remote', 'add', 'origin', str(Path(self._tmp.name) / 'remoto.git'))
        self.commit({'src/a.py': f'# {CORREO_AJENO}\n'}, 'Nuevo')
        self.assertEqual(self.decidir(codigo=3, accion='subir')['accion'], 'permiso')
        self.assertEqual(self.decidir(codigo=3, accion='release')['accion'], 'permiso')
        self.assertEqual(self.decidir(codigo=0, accion='release')['accion'], 'seguir')
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(HERRAMIENTA), '--repo', str(self.raiz), '--decidir',
                            '--accion', 'otra'], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)

    def test_publico_lo_nuevo_bloquea_y_lo_subido_pide_permiso(self):
        # Sin remoto que consultar, se trata como público.
        self.commit({'src/a.py': f'# {CORREO_AJENO}\n'}, 'Subido')
        self.git('update-ref', 'refs/remotes/origin/develop', 'HEAD')
        otro = 'luis' + '@' + 'correo.es'
        self.commit({'src/b.py': f'# {otro}\n'}, 'Nuevo')
        r = self.decidir(codigo=3)
        self.assertEqual(r['accion'], 'bloquear')
        self.assertIn('1 cosas sin subir', r['mensaje'])
        self.assertIn('revision_publica.py', r['mensaje'])
        # Corregido lo nuevo, lo ya subido pide permiso; repetir lo da, y no se vuelve a preguntar.
        self.commit({'src/b.py': '# nada\n'}, 'Corregido')
        self.git('reset', '-q', '--hard', 'HEAD~2')
        r = self.decidir(codigo=3)
        self.assertEqual(r['accion'], 'permiso')
        self.assertIn('ya subidas', r['mensaje'])
        self.assertIn('repite en los próximos 10 minutos', r['mensaje'])
        self.assertEqual(self.decidir(codigo=0)['accion'], 'seguir')
        self.assertEqual(self.decidir(codigo=0)['mensaje'], '')

    def test_privado_pregunta_y_el_cierre_no_revisa(self):
        self.git('remote', 'add', 'origin', str(Path(self._tmp.name) / 'remoto.git'))
        self.commit({'src/a.py': f'# {CORREO_AJENO}\n'}, 'Nuevo')
        r = self.decidir(codigo=3)
        self.assertEqual((r['accion'], r['visibilidad']), ('permiso', 'LOCAL'))
        self.assertIn('no es público', r['mensaje'])
        self.assertEqual(self.decidir('--solo-publico', codigo=0)['hallazgos'], [])

    def test_cola_subir_usa_la_misma_revision(self):
        self.commit({'src/a.py': f'# {CORREO_AJENO}\n'}, 'Nuevo')
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(HERRAMIENTA.with_name('cola.py')), '--raiz',
                            str(self.raiz), '--json', 'subir'], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        j = json.loads(r.stdout.strip().splitlines()[-1])
        self.assertIn('develop sin subir a origin: el repositorio es público', j['mensaje'])
        self.assertIn(CORREO_AJENO, j['mensaje'])

    def test_encuentra_secretos_correos_rutas_e_internos(self):
        ruta_nueva = (Path(self._tmp.name) / 'Contador').as_posix()
        self.commit({'src/x.py': f'T = "{TOKEN}"\n# {CORREO_AJENO} y {AUTORA}\nRAIZ = "{ruta_nueva}"\n',
                     '.env': 'A=1\n'}, f'Con {CARPETA}')
        h = self.motivos(self.revisar('--desde', 'v0.1.0', codigo=3))
        self.assertIn(('src/x.py', 'token de GitHub', TOKEN), h)
        self.assertIn(('src/x.py', 'correo', CORREO_AJENO), h)
        # La carpeta temporal puede estar en la del usuario: entonces sale como tal.
        self.assertTrue(any(x[0] == 'src/x.py' and x[2] == ruta_nueva for x in h), h)
        self.assertIn(('.env', 'archivo interno: variables de entorno', '.env'), h)
        self.assertIn(('mensaje', 'carpeta de un usuario', CARPETA), h)
        self.assertFalse(any('autora' in x[2] for x in h), 'el correo de la autora ya sale con cada commit')

    def test_lo_ya_publicado_no_cuenta(self):
        self.commit({'docs/a.md': f'Ver otra vez {self.ruta_vieja}\n'}, 'Retoque')
        r = self.revisar('--desde', 'v0.1.0', codigo=0)
        self.assertEqual(r['ya_publicados'], 1)
        # Sin --desde, todo es nuevo.
        self.assertTrue(self.revisar(codigo=3)['hallazgos'])

    def test_lo_publicable_del_proyecto_no_cuenta(self):
        self.commit({'src/x.py': f'# {CORREO_AJENO}\n', 'docs/ref/y.md': f'{TOKEN}\n',
                     '.sf/publicable.txt': f'# Lo que puede salir\n{CORREO_AJENO.upper()}\narchivo:docs/ref/*\n'}, 'Tercero')
        self.assertEqual(self.revisar('--desde', 'v0.1.0', codigo=0)['hallazgos'], [])

    def test_si_no_puede_revisar_sale_con_1(self):
        r = self.revisar('--desde', 'v9.9.9', codigo=1)
        self.assertFalse(r['ok'])


if __name__ == '__main__':
    unittest.main()
