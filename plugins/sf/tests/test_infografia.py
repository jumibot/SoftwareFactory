"""Pruebas de la infografía técnica con el estilo del proyecto y del recurso que la incrusta (decisiones 315 y 323):
la plantilla sin colores fijos del HUD fuera de su bloque de estilo, el script que escribe el estilo (con estilo.json o
con el tema por defecto, escenario derivado o claro, HUD primario, acento o #rrggbb y su contraste) y «::: infografia»
en el generador de documentos (marco, pie, «Abrir aparte», imagen fija al imprimir).

python -I -X utf8 -m pytest plugins/sf/tests/test_infografia.py
"""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / 'skills'
PLANTILLA = SKILLS / 'infografia_tecnica' / 'assets' / 'plantilla-infografia.html'
ESTILO_INF = SKILLS / 'infografia_tecnica' / 'scripts' / 'estilo_infografia.py'
GENERADOR = SKILLS / 'crear_documentos' / 'scripts' / 'documento_a_html.py'
TEMAS = SKILLS / 'crear_documentos' / 'assets' / 'temas'
sys.path.insert(0, str(SKILLS / 'crear_documentos' / 'scripts'))
from tema_identidad import contraste, mezclar  # noqa: E402

INICIO, FIN = '/* estilo:inicio', '/* estilo:fin */'


def variables(html: str) -> dict:
    bloque = html[html.index(INICIO):html.index(FIN)]
    raiz = re.search(r':root\{(.*?)\}', bloque, re.S).group(1)
    return dict(re.findall(r'(--[\w-]+):([^;]+);', raiz))


class Plantilla(unittest.TestCase):
    def test_sin_colores_del_hud_fuera_del_bloque(self):
        h = PLANTILLA.read_text(encoding='utf-8')
        fuera = h[:h.index(INICIO)] + h[h.index(FIN):]
        for fijo in ('111,243,255', '#6ff3ff', '0x6ff3ff', '#04121b', '#dafcff', '#15243a', '#060b14', '1d6f80'):
            self.assertNotIn(fijo, fuera.replace("'#6ff3ff'", '').replace("'#060b14'", ''), fijo)
        self.assertIn('<link id="estilo-letra"', h)
        self.assertIn('alpha: true', h)  # el lienzo deja ver el escenario de la hoja
        self.assertIn("classList.add('incrustada')", h)


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.raiz = Path(self._tmp.name)
        self.ident = self.raiz / 'docs' / 'identidad'
        self.ident.mkdir(parents=True)
        self.inf = self.raiz / 'docs' / 'infografias' / 'equipo.html'
        self.inf.parent.mkdir(parents=True)
        self.inf.write_text(PLANTILLA.read_text(encoding='utf-8'), encoding='utf-8')

    def tearDown(self):
        self._tmp.cleanup()

    def escribir_estilo(self, **grupos):
        estilo = {'version': 2, 'origen': 'teal', 'colores': {'primario': '#00726b', 'acento': '#6d28d9',
                                                                  'texto-suave': '#555555'}}
        estilo.update(grupos)
        (self.ident / 'estilo.json').write_text(json.dumps(estilo), encoding='utf-8')

    def estilo_inf(self, *args, ok=True):
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(ESTILO_INF), str(self.inf), *args],
                           capture_output=True, text=True, encoding='utf-8')
        self.salida = r.stdout + r.stderr
        if ok:
            self.assertEqual(r.returncode, 0, self.salida)
        else:
            self.assertNotEqual(r.returncode, 0, self.salida)
        return self.inf.read_text(encoding='utf-8')


class EstiloInfografia(Base):
    def test_sin_estilo_tema_por_defecto_con_aviso(self):
        h = self.estilo_inf()
        self.assertEqual(self.salida.count('no tiene estilo'), 1)
        self.assertIn('«Morado»', self.salida)
        v = variables(h)
        self.assertEqual(v['--bg'], '#faf8fd')
        self.assertIn('DM Sans', v['--body'])
        self.assertIn('DM+Sans', re.search(r'<link id="estilo-letra"[^>]*>', h).group(0))

    def test_tema_por_el_color_de_sesion(self):
        (self.raiz / '.sf').mkdir()
        (self.raiz / '.sf' / 'proyecto.json').write_text('{"color": "red"}', encoding='utf-8')
        self.estilo_inf()
        self.assertIn('color de sesión del proyecto, red', self.salida)

    def test_repetir_no_cambia_y_comprobar(self):
        h1 = self.estilo_inf()
        h2 = self.estilo_inf()
        self.assertEqual(h1, h2)
        self.assertIn('sin cambios', self.salida)
        self.estilo_inf('--comprobar')
        self.assertIn('al día', self.salida)

    def test_comprobar_detecta_lo_desfasado(self):
        self.estilo_inf('--comprobar', ok=False)
        self.assertIn('no está al día', self.salida)
        self.assertEqual(self.inf.read_text(encoding='utf-8'), PLANTILLA.read_text(encoding='utf-8'))

    def test_solo_cambia_el_bloque_y_la_letra(self):
        h = self.estilo_inf()
        original = PLANTILLA.read_text(encoding='utf-8')
        quitar = lambda x: re.sub(r'<link id="estilo-letra"[^>]*>', '', x[:x.index(INICIO)] + x[x.index(FIN):])
        self.assertEqual(quitar(h), quitar(original))

    def test_escenario_derivado_y_hud_primario_brillante(self):
        for tema in sorted(p.stem for p in TEMAS.glob('*.json')):
            with self.subTest(tema=tema):
                self.inf.write_text(PLANTILLA.read_text(encoding='utf-8'), encoding='utf-8')
                v = variables(self.estilo_inf('--tema', tema))
                fondos = (v['--stage-a'], v['--stage-b'])
                self.assertGreaterEqual(contraste('#ffffff', v['--stage-a']), 12)
                self.assertGreaterEqual(min(contraste(v['--hud'], f) for f in fondos), 7)
                self.assertGreaterEqual(min(contraste(v['--hud-ink'], f) for f in fondos), 4.5)
                alfa = float(re.search(r',([\d.]+)\)$', v['--hud-dim']).group(1))
                self.assertGreaterEqual(min(contraste(mezclar(f, v['--hud'], alfa), f) for f in fondos), 4.5)

    def test_estilo_claro_con_hud_acento_y_esquinas(self):
        self.escribir_estilo(aparte={'escenario': 'claro', 'hud': 'acento'}, pagina={'esquinas': 4},
                             letra={'codigo': "'JetBrains Mono', monospace"})
        v = variables(self.estilo_inf())
        self.assertIn('estilo del proyecto v2', self.salida)
        self.assertEqual(v['--hud'], '#6d28d9')
        self.assertEqual(v['--r-marco'], '4px')
        self.assertEqual(v['--mono'], "'JetBrains Mono', monospace")
        self.assertGreater(contraste('#000000', v['--stage-a']), 15)  # escenario claro
        self.assertEqual(v['--hud-fuerte'], v['--ink'])

    def test_hud_hex_sin_contraste_detiene(self):
        self.escribir_estilo(aparte={'hud': '#303030'})
        self.estilo_inf(ok=False)
        self.assertIn('aparte.hud #303030', self.salida)
        self.assertEqual(self.inf.read_text(encoding='utf-8'), PLANTILLA.read_text(encoding='utf-8'))

    def test_hud_hex_con_contraste_tal_cual(self):
        self.escribir_estilo(aparte={'hud': '#ffd84d'})
        self.assertEqual(variables(self.estilo_inf())['--hud'], '#ffd84d')

    def test_sin_bloque_detiene(self):
        self.inf.write_text('<style>:root{}</style>', encoding='utf-8')
        self.estilo_inf(ok=False)
        self.assertIn('bloque «estilo»', self.salida)


MD = """---
destino: proyecto
herramientas: ninguna
---
# Prueba

## Uno | Primera {{#uno}}

Texto.

{bloque}
"""


class Recurso(Base):
    def generar(self, bloque, ok=True, perfil=None):
        md = self.raiz / 'docs' / 'doc.md'
        md.write_text(MD.format(bloque=bloque), encoding='utf-8')
        args = ['--perfil', str(perfil)] if perfil else []
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(GENERADOR), str(md), *args],
                           capture_output=True, text=True, encoding='utf-8')
        self.salida = r.stdout + r.stderr
        if not ok:
            self.assertNotEqual(r.returncode, 0, self.salida)
            return self.salida
        self.assertEqual(r.returncode, 0, self.salida)
        return md.with_suffix('.html').read_text(encoding='utf-8')

    def test_marco_pie_y_abrir_aparte(self):
        h = self.generar('::: infografia infografias/equipo.html alto=600\nLa vista *principal*.\n:::')
        fig = re.search(r'<figure class="infografia".*?</figure>', h, re.S).group(0)
        self.assertIn('--infografia-alto: 600px', fig)
        self.assertIn('<iframe src="infografias/equipo.html" title="Equipo de ejemplo 3D"', fig)
        self.assertIn('<figcaption>La vista <em>principal</em>.', fig)
        self.assertIn('href="infografias/equipo.html" target="_blank"', fig)
        self.assertIn('Abrir aparte', fig)
        self.assertIn('.infografia-marco', h)  # su CSS, en la hoja común

    def test_imagen_fija_al_imprimir(self):
        h = self.generar('::: infografia infografias/equipo.html\n:::')
        self.assertNotIn('infografia-fija" src', h)
        self.assertIn('no tiene su imagen fija', self.salida)
        self.inf.with_suffix('.png').write_bytes(b'\x89PNG\r\n\x1a\n')
        h = self.generar('::: infografia infografias/equipo.html\n:::')
        self.assertIn('<img class="infografia-fija" src="infografias/equipo.png"', h)
        self.assertIn('--infografia-alto: 640px', h)
        self.assertNotIn('no tiene su imagen fija', self.salida)

    def test_errores(self):
        self.assertIn('no encuentro', self.generar('::: infografia infografias/otra.html\n:::', ok=False))
        self.assertIn('ruta de la página', self.generar('::: infografia\n:::', ok=False))
        self.assertIn('«alto»', self.generar('::: infografia infografias/equipo.html alto=90\n:::', ok=False))

    def test_todos_los_perfiles_la_admiten(self):
        # Decisión 330: una infografía se puede meter en cualquier documento que la necesite.
        for perfil in sorted(SKILLS.glob('*/perfil.json')):
            with self.subTest(perfil=perfil.parent.name):
                recursos = json.loads(perfil.read_text(encoding='utf-8')).get('recursos')
                if recursos is not None:
                    self.assertIn('infografia', recursos)
                h = self.generar('::: infografia infografias/equipo.html\n:::', perfil=perfil)
                self.assertIn('<figure class="infografia"', h)

    def test_movil_no_la_trata_como_grafico_ancho(self):
        # La hoja narrativa (visión) desplaza en horizontal los gráficos anchos en móvil, con su aviso; la infografía
        # cabe en la columna y no lleva ni el desplazamiento ni el aviso.
        css = (SKILLS / 'crear_documentos' / 'assets' / 'narrativa.css').read_text(encoding='utf-8')
        reglas = re.findall(r'figure:not\([^{,]*', css)
        self.assertTrue(reglas)
        for regla in reglas:
            self.assertIn(':not(.infografia)', regla)


if __name__ == '__main__':
    unittest.main()
