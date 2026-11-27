"""Pruebas del catálogo de emojis: skills/orquestacion/scripts/emojis.py genera el .md y el HTML desde el emoji-test.txt guardado.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"
"""
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / 'skills' / 'orquestacion'
SCRIPT = SKILL / 'scripts' / 'emojis.py'
LISTA = SKILL / 'assets' / 'emoji-test.txt'
BOTON = r'<button type="button"(?: class="tono")? title='


def correr(*args):
    return subprocess.run([sys.executable, '-I', '-X', 'utf8', str(SCRIPT), *args],
                          capture_output=True, text=True, encoding='utf-8')


class Catalogo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
            destino = Path(d) / 'emojis.md'
            r = correr(str(LISTA), str(destino), '--estilo', 'ninguno')
            assert r.returncode == 0, r.stderr + r.stdout
            cls.salida = r.stdout
            cls.md = destino.read_text(encoding='utf-8')
            cls.html = destino.with_suffix('.html').read_text(encoding='utf-8')

    def test_numero(self):
        self.assertEqual(len(re.findall(BOTON, self.md)), 3963)
        self.assertEqual(len(re.findall(BOTON, self.html)), 3963)
        self.assertIn('3963 emojis', self.salida)

    def test_estructura_del_md(self):
        self.assertEqual(len(re.findall(r'^## ', self.md, re.M)), 9)
        self.assertIn('## Caras y emociones', self.md)
        self.assertNotIn('Component', self.md)
        subgrupos = len(re.findall(r'^### ', self.md, re.M))
        self.assertEqual(subgrupos, self.md.count('<div class="emojis">'))
        self.assertEqual(subgrupos, self.md.count('</div>'))
        self.assertIn('<button type="button" title="grinning face" aria-label="grinning face">😀</button>', self.md)
        self.assertRegex(self.md, r'<button type="button" class="tono" title="[^"]*skin tone[^"]*"')

    def test_html_con_el_kit(self):
        self.assertEqual(self.html.count('<details class="seccion'), 9)
        self.assertIn('class="subseccion"', self.html)
        for rastro in ('barra-emojis', 'sin-tonos', 'clipboard', '.emojis{'):
            self.assertIn(rastro, self.html)

    def test_sin_lista(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
            vacio = Path(d) / 'v.txt'
            vacio.write_text('# nada', encoding='utf-8')
            self.assertEqual(correr(str(vacio), str(Path(d) / 'o.md')).returncode, 1)


if __name__ == '__main__':
    unittest.main()
