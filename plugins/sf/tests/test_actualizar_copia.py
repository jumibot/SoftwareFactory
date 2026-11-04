"""Pruebas de actualizar_copia.py (kit_documentos): al poner al día el estilo de un documento ya generado, las
plantillas con marcadores de color ({{primario}}, {{oscuro}}…) se rellenan con el tema del propio documento.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"
"""
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
GENERADOR = PLUGIN / 'skills' / 'documento_vision' / 'scripts' / 'doc_to_html.py'
ACTUALIZAR = PLUGIN / 'tools' / 'kit_documentos' / 'actualizar_copia.py'
ESTILO = 'skills/documento_vision/assets/estilo_base.css'
BLOQUE = re.compile(r'(<style data-kit="' + re.escape(ESTILO) + r'">)(.*?)(</style>)', re.S)


def ejecutar(*args) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, '-I', '-X', 'utf8', *map(str, args)], capture_output=True, text=True,
                          encoding='utf-8')


class RellenaColores(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        md = Path(self._tmp.name) / 'vision.md'
        md.write_text('<!-- destino: proyecto -->\n<!-- herramientas: ninguna -->\n# Prueba\n\n## Uno\n\nTexto.\n',
                      encoding='utf-8')
        r = ejecutar(GENERADOR, md, '--identidad', 'ninguna', '--logo', 'ninguno', '--tema', 'teal')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.html = md.with_suffix('.html')

    def tearDown(self):
        self._tmp.cleanup()

    def envejecer(self) -> None:
        """Deja el estilo como en una copia vieja: otro cuerpo, para que haya que ponerlo al día."""
        texto = self.html.read_text(encoding='utf-8')
        self.html.write_text(BLOQUE.sub(lambda m: m.group(1) + '\n/* estilo viejo */\n' + m.group(3), texto, count=1),
                             encoding='utf-8')

    def test_rellena_con_el_tema_del_documento(self):
        generado = self.html.read_text(encoding='utf-8')
        primario = re.search(r':root \{[^}]*--primario: (#[0-9a-f]+);', generado).group(1)
        self.envejecer()
        r = ejecutar(ACTUALIZAR, self.html)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('actualizado: estilo_base.css', r.stdout)
        estilo = BLOQUE.search(self.html.read_text(encoding='utf-8')).group(2)
        # Sin marcadores de color por rellenar (el {{rol}} del comentario de cabecera no es uno).
        self.assertEqual(set(re.findall(r'\{\{([a-z-]+)\}\}', estilo)) - {'rol'}, set())
        self.assertIn(f"stroke='%23{primario.lstrip('#')}'", estilo)
        # Queda como lo deja el generador.
        self.assertEqual(estilo.strip(), BLOQUE.search(generado).group(2).strip())

    def test_al_dia_no_cambia(self):
        antes = self.html.read_text(encoding='utf-8')
        r = ejecutar(ACTUALIZAR, self.html)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('sin cambios', r.stdout)
        self.assertEqual(self.html.read_text(encoding='utf-8'), antes)

    def test_sin_tema_no_toca_nada(self):
        self.envejecer()
        texto = re.sub(r'--primario: #[0-9a-f]+;', '', self.html.read_text(encoding='utf-8'))
        self.html.write_text(texto, encoding='utf-8')
        r = ejecutar(ACTUALIZAR, self.html)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('primario', r.stderr)
        self.assertEqual(self.html.read_text(encoding='utf-8'), texto)


if __name__ == '__main__':
    unittest.main()
