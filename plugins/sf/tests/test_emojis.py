"""Pruebas del catálogo de emojis: skills/orquestacion/scripts/emojis.py genera la página desde el emoji-test.txt guardado.

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


class Catalogo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
            destino = Path(d) / 'emojis.html'
            r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(SCRIPT), str(LISTA), str(destino)],
                               capture_output=True, text=True, encoding='utf-8')
            assert r.returncode == 0, r.stderr
            cls.salida = r.stdout
            cls.html = destino.read_text(encoding='utf-8')

    def test_numero(self):
        self.assertEqual(len(re.findall(r'<span(?: class="t")? title=', self.html)), 3963)
        self.assertIn('3963 emojis', self.salida)
        self.assertIn('3963 emojis, lista oficial', self.html)

    def test_estructura(self):
        self.assertEqual(self.html.count('<h2>'), 9)
        self.assertIn('<h2>Caras y emociones</h2>', self.html)
        self.assertNotIn('Component', self.html)
        self.assertEqual(self.html.count('<div class="f">'), self.html.count('</div>') - 1)  # el otro es la barra
        self.assertIn('<span title="grinning face">😀</span>', self.html)
        self.assertRegex(self.html, r'<span class="t" title="[^"]*skin tone[^"]*">')

    def test_controles(self):
        for ident in ('id="q"', 'id="st"', 'prefers-color-scheme:dark', 'clipboard'):
            self.assertIn(ident, self.html)

    def test_sin_lista(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
            vacio = Path(d) / 'v.txt'
            vacio.write_text('# nada\n', encoding='utf-8')
            r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(SCRIPT), str(vacio), str(Path(d) / 'o.html')],
                               capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(r.returncode, 1)


if __name__ == '__main__':
    unittest.main()
