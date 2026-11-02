"""Pruebas de tools/indice_decisiones.py: la carpeta sf/decisiones/ (decisión 208) y la migración del registro antiguo.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERRAMIENTA = Path(__file__).resolve().parents[1] / 'tools' / 'indice_decisiones.py'

ANTIGUO = """# Decisiones

## Índice

### Segunda

- **Origen:** Demo, 2026-10-02. Ver [la visión](specs/vision.md) y [la primera](#primera).

### Primera

- **Origen:** Demo, 2026-10-01.
"""


class Indice(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.raiz = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def correr(self, *args: str) -> str:
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(HERRAMIENTA), *args], cwd=self.raiz,
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def test_sin_carpeta_crea_sf_decisiones(self):
        self.correr()
        self.assertTrue((self.raiz / 'sf' / 'decisiones' / 'README.md').is_file())
        self.assertFalse((self.raiz / 'docs').exists())

    def test_sin_carpeta_y_solo_la_de_antes_usa_docs(self):
        (self.raiz / 'docs' / 'decisiones').mkdir(parents=True)
        self.correr()
        self.assertTrue((self.raiz / 'docs' / 'decisiones' / 'README.md').is_file())
        self.assertFalse((self.raiz / 'sf').exists())

    def test_con_las_dos_manda_sf(self):
        (self.raiz / 'docs' / 'decisiones').mkdir(parents=True)
        (self.raiz / 'sf' / 'decisiones').mkdir(parents=True)
        self.assertIn('sf/decisiones', self.correr('--nombre', 'Algo', '--fecha', '2026-11-02').replace('\\', '/'))

    def test_migrar_a_sf_rehace_los_enlaces(self):
        (self.raiz / 'docs').mkdir()
        (self.raiz / 'docs' / 'decisiones.md').write_text(ANTIGUO, encoding='utf-8')
        self.correr('sf/decisiones', '--migrar', 'docs/decisiones.md')
        carpeta = self.raiz / 'sf' / 'decisiones'
        nombres = sorted(f.name for f in carpeta.glob('0*.md'))
        self.assertEqual(nombres, ['001-2026-10-01-primera.md', '002-2026-10-02-segunda.md'])
        segunda = (carpeta / nombres[1]).read_text(encoding='utf-8')
        self.assertIn('[la visión](../../docs/specs/vision.md)', segunda)
        self.assertIn('[la primera](001-2026-10-01-primera.md)', segunda)
        self.assertFalse((self.raiz / 'docs' / 'decisiones.md').exists())
        self.assertIn('indice_decisiones.py sf/decisiones`', (carpeta / 'README.md').read_text(encoding='utf-8'))

    def test_migrar_junto_al_antiguo_como_antes(self):
        (self.raiz / 'docs').mkdir()
        (self.raiz / 'docs' / 'decisiones.md').write_text(ANTIGUO, encoding='utf-8')
        self.correr('docs/decisiones', '--migrar', 'docs/decisiones.md')
        segunda = (self.raiz / 'docs' / 'decisiones' / '002-2026-10-02-segunda.md').read_text(encoding='utf-8')
        self.assertIn('[la visión](../specs/vision.md)', segunda)


if __name__ == '__main__':
    unittest.main()
