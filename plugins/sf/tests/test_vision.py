"""Pruebas del lector de libros, recurso común de crear_documentos (assets/lector.css y lector.js): la página de libro y
el lector que pagina (.lector), con su estilo y su script solo cuando el documento lo usa, en el generador de visión
y en el común.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GENERADOR = Path(__file__).resolve().parents[1] / 'skills' / 'documento_vision' / 'scripts' / 'doc_to_html.py'

LECTOR = '''<div class="lector" data-titulo="Historia · prólogo">
<div class="libro">
<p class="libro-capitulo">Prólogo</p>
<p class="libro-titulo">Un lunes</p>
<p>Primer párrafo.</p>
<p class="libro-ornamento"></p>
<p>Segundo párrafo.</p>
</div>
</div>
'''


class Lector(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.md = Path(self._tmp.name) / 'vision.md'

    def tearDown(self):
        self._tmp.cleanup()

    def generar(self, cuerpo: str) -> str:
        self.md.write_text('<!-- destino: proyecto -->\n<!-- herramientas: ninguna -->\n# Prueba\n\n' + cuerpo + '\n## Uno\n\nTexto.\n', encoding='utf-8')
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(GENERADOR), str(self.md), '--identidad', 'ninguna',
                            '--logo', 'ninguno'], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        return self.md.with_suffix('.html').read_text(encoding='utf-8')

    def test_con_lector_lleva_su_estilo_y_su_script(self):
        h = self.generar(LECTOR)
        self.assertIn('<div class="lector" data-titulo="Historia · prólogo">', h)
        self.assertIn('<p class="libro-titulo">Un lunes</p>', h)
        self.assertIn('.lector.paginado .libro-flujo', h)
        self.assertIn('Leer la historia completa', h)
        self.assertIn('aria-label="Página siguiente"', h)

    def test_marca_con_la_barra_clara(self):
        # Como el logo «/SF» (decisión 255): lo que va delante de las letras, en el morado claro; las letras, en el de la marca.
        h = self.generar(LECTOR)
        self.assertIn('.lector-portada-logo b { color: var(--lector-marca, #161616); }', h)
        self.assertIn('.lector-marca b { color: var(--lector-marca, #b8b8bd);', h)
        self.assertIn('cursor: pointer; color: var(--lector-marca-claro, #161616); }', h)

    def test_sin_lector_no_lleva_script(self):
        h = self.generar('<div class="caso">\n<p class="caso-etiqueta">El caso · prólogo</p>\n<p>Texto.</p>\n</div>\n')
        self.assertNotIn('Leer la historia completa', h)
        self.assertNotIn('lector.js', h)  # el recurso del lector solo entra si el documento lo usa
        self.assertNotIn('lector.css', h)


class LectorComun(unittest.TestCase):
    """El lector es un recurso común: el generador de crear_documentos lo inyecta en cualquier tipo de documento."""

    def test_generador_comun_con_lector(self):
        comun = Path(__file__).resolve().parents[1] / 'skills' / 'crear_documentos' / 'scripts' / 'documento_a_html.py'
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
            md = Path(d) / 'doc.md'
            md.write_text('---\ndestino: proyecto\nherramientas: ninguna\n---\n# Prueba\n\n## Uno | Uno | Uno {#uno}\n\n'
                          + LECTOR + '\nTexto.\n', encoding='utf-8')
            r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(comun), str(md), '--identidad', 'ninguna',
                                '--logo', 'ninguno'], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stderr)
            h = md.with_suffix('.html').read_text(encoding='utf-8')
        self.assertIn('data-kit="skills/crear_documentos/assets/lector.css"', h)
        self.assertIn('data-kit="skills/crear_documentos/assets/lector.js"', h)
        self.assertIn('<div class="lector" data-titulo="Historia · prólogo">', h)


if __name__ == '__main__':
    unittest.main()
