"""Pruebas del diagrama como recurso del catálogo (decisión 314): el .md nombra su .diagrama y documento_a_html.py
lo dibuja en cada generación con el motor de la skill de diagramas, con el estilo del documento (decisión 307).

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_diagrama_recurso.py"
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / 'skills'
sys.path.insert(0, str(SKILLS / 'crear_documentos' / 'scripts'))
import diagramas_recurso as dr  # noqa: E402

DOCUMENTO = SKILLS / 'crear_documentos' / 'scripts' / 'documento_a_html.py'
EJEMPLO = SKILLS / 'diagramas' / 'assets' / 'ejemplos' / 'estados.diagrama'
CABECERA = '---\ndestino: proyecto\nherramientas: recomendadas\n---\n# Prueba\n\n## Uno | Primera {#uno}\n\nTexto.\n\n'


def generar(md: Path):
    return subprocess.run([sys.executable, '-I', '-X', 'utf8', str(DOCUMENTO), str(md), '--identidad', 'ninguna', '--logo', 'ninguno'],
                          capture_output=True, text=True, encoding='utf-8')


class Referencias(unittest.TestCase):
    def test_solo_una_linea_sola_fuera_del_codigo(self):
        md = ('![](a.diagrama)\n'
              'Texto con ![](b.diagrama) dentro.\n'
              '![Pie](<sub/c d.diagrama>)\n'
              '![](e.png)\n'
              '```\n![](f.diagrama)\n```\n'
              '~~~markdown\n```\n![](g.diagrama)\n~~~\n'
              '  ![](h.diagrama)  \n')
        self.assertEqual(dr.referencias(md), [(1, 'a.diagrama'), (3, 'sub/c d.diagrama'), (12, 'h.diagrama')])

    def test_sin_referencias_no_cambia(self):
        self.assertEqual(dr.expandir('# Uno\n\nTexto.\n', Path('.')), '# Uno\n\nTexto.\n')


class EnElDocumento(unittest.TestCase):
    def test_el_generador_lo_dibuja_con_el_estilo_del_documento(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / 'diagramas').mkdir()
            shutil.copy(EJEMPLO, d / 'diagramas' / 'flujo.diagrama')
            md = d / 'doc.md'
            md.write_text(CABECERA + '![](diagramas/flujo.diagrama)\n\nDespués.\n', encoding='utf-8')
            r = generar(md)
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
            html = md.with_suffix('.html').read_text(encoding='utf-8')
            self.assertIn('<figure class="diagrama d-gen', html)
            self.assertIn('id="flujo"', html)                       # el id, del nombre del archivo
            etiqueta = html.split('<figure class="diagrama', 1)[1].split('>', 1)[0]
            self.assertNotIn('data-d-tema=', etiqueta)              # sin tema propio: el del documento (307)
            self.assertNotIn('flujo.diagrama', html)                # la referencia no queda en la página
            self.assertIn('data-kit="skills/diagramas/assets/diagramas.js"', html)
            self.assertIn('data-kit="tools/kit_documentos/diagramas.js"', html)
            # determinista: el mismo .diagrama con el mismo estilo da la misma figura
            primera = html.split('<figure class="diagrama', 1)[1].split('</figure>', 1)[0]
            self.assertEqual(generar(md).returncode, 0)
            otra = md.with_suffix('.html').read_text(encoding='utf-8').split('<figure class="diagrama', 1)[1].split('</figure>', 1)[0]
            self.assertEqual(primera, otra)
            # se mantiene al día: cambia el .diagrama y cambia la figura
            datos = (d / 'diagramas' / 'flujo.diagrama').read_text(encoding='utf-8')
            nuevo = datos.replace('titulo:', 'titulo: Cambiado ·', 1)
            self.assertNotEqual(nuevo, datos)
            (d / 'diagramas' / 'flujo.diagrama').write_text(nuevo, encoding='utf-8')
            self.assertEqual(generar(md).returncode, 0)
            self.assertIn('Cambiado ·', md.with_suffix('.html').read_text(encoding='utf-8'))

    def test_un_diagrama_que_falta_detiene_con_su_linea(self):
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / 'doc.md'
            md.write_text(CABECERA + '![](no-esta.diagrama)\n', encoding='utf-8')
            r = generar(md)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn('línea 11', r.stderr)
            self.assertIn('no-esta.diagrama', r.stderr)
            self.assertFalse(md.with_suffix('.html').exists())

    def test_unos_datos_malos_dan_el_error_del_motor(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / 'malo.diagrama').write_text('tipo: inexistente\n', encoding='utf-8')
            md = Path(d) / 'doc.md'
            md.write_text(CABECERA + '![](malo.diagrama)\n', encoding='utf-8')
            r = generar(md)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn('malo.diagrama', r.stderr)


if __name__ == '__main__':
    unittest.main()
