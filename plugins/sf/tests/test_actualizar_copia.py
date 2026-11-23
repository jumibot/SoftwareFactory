"""Pruebas de actualizar_copia.py (kit_documentos): un documento ya generado se pone al día con la versión actual de
los archivos del kit que lleva (data-kit) sin tocar su contenido; los marcadores de color de una plantilla
({{primario}}, {{oscuro}}…) se rellenan con el tema del propio documento; y el bloque de un archivo que ya no existe
(estilo_base.css de la maqueta antigua de la visión, retirada con el generador único) se deja como está.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"
"""
import importlib.util
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
GENERADOR = PLUGIN / 'skills' / 'documento_vision' / 'scripts' / 'doc_to_html.py'
ACTUALIZAR = PLUGIN / 'tools' / 'kit_documentos' / 'actualizar_copia.py'
ESTILO = 'skills/crear_documentos/assets/estilo_documento.css'
BLOQUE = re.compile(r'(<style data-kit="' + re.escape(ESTILO) + r'">)(.*?)(</style>)', re.S)


def ejecutar(*args) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, '-I', '-X', 'utf8', *map(str, args)], capture_output=True, text=True,
                          encoding='utf-8')


def modulo():
    spec = importlib.util.spec_from_file_location('actualizar_copia', ACTUALIZAR)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class PoneAlDia(unittest.TestCase):
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

    def test_pone_al_dia_el_estilo(self):
        generado = self.html.read_text(encoding='utf-8')
        self.envejecer()
        r = ejecutar(ACTUALIZAR, self.html)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('actualizado: estilo_documento.css', r.stdout)
        # Queda como lo deja el generador.
        self.assertEqual(BLOQUE.search(self.html.read_text(encoding='utf-8')).group(2).strip(),
                         BLOQUE.search(generado).group(2).strip())

    def test_al_dia_no_cambia(self):
        antes = self.html.read_text(encoding='utf-8')
        r = ejecutar(ACTUALIZAR, self.html)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('sin cambios', r.stdout)
        self.assertEqual(self.html.read_text(encoding='utf-8'), antes)

    def test_archivo_retirado_se_deja(self):
        texto = self.html.read_text(encoding='utf-8').replace(
            '</head>', '<style data-kit="skills/documento_vision/assets/estilo_base.css">\n.viejo {}\n</style>\n</head>', 1)
        self.html.write_text(texto, encoding='utf-8')
        r = ejecutar(ACTUALIZAR, self.html)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('desconocido (se deja): estilo_base.css', r.stdout)
        self.assertIn('.viejo {}', self.html.read_text(encoding='utf-8'))


class Marcadores(unittest.TestCase):
    """Los marcadores de color de una plantilla del kit se rellenan con el tema del documento, como hacían los
    generadores; sin el color de su tema, se dice cuál falta."""

    def test_rellena_con_el_tema_del_documento(self):
        m = modulo()
        colores = m.colores_tema('<style>\n:root { --primario: #00726b; --oscuro: #004d47; }\n</style>')
        cuerpo = "a { background: url(\"data:image/svg+xml;utf8,<svg stroke='{{primario}}'/>\"); } /* {{rol}} */"
        self.assertEqual(m.faltan_colores(cuerpo, colores), [])
        relleno = m.rellenar(cuerpo, colores)
        self.assertIn("stroke='%2300726b'", relleno)
        self.assertIn('{{rol}}', relleno)  # el del comentario no es un marcador de color

    def test_sin_tema_dice_que_falta(self):
        self.assertEqual(modulo().faltan_colores("x { stroke: '{{primario}}' }", {}), ['primario'])


if __name__ == '__main__':
    unittest.main()
