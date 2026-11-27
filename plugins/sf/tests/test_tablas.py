"""Pruebas del ancho de las columnas de las tablas de un documento (crear_documentos): una columna de contenido breve,
como la del número, queda estrecha y el ancho va a las de texto, sin desbordes en móvil.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_tablas.py"
"""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills' / 'crear_documentos' / 'scripts'
GENERADOR = SCRIPTS / 'documento_a_html.py'
spec = importlib.util.spec_from_file_location('documento_a_html', SCRIPTS / 'documento_a_html.py')
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

MD = """---
destino: proyecto
herramientas: ninguna
---
# Prueba de tablas

## Uno | Primera {{#uno}}

| Nº | Decisión | Qué fija aquí |
|---|---|---|
| 12 | Publicar solo lo que ya está revisado por el propietario antes de cada versión | Que nada llegue al remoto sin su visto bueno, ni siquiera en una rama auxiliar |
| 345 | Guardar una copia de cada informe al cambiar de versión | La carpeta de respaldo, con el nombre de la versión anterior |
"""

TABLA = ('<table><thead><tr><th>Nº</th><th>Texto</th></tr></thead><tbody>'
         '<tr><td>1</td><td>Una frase larga que sí pide ancho.</td></tr>'
         '<tr><td>22</td><td>Otra frase larga.</td></tr></tbody></table>')


class Marcado(unittest.TestCase):
    def test_la_columna_de_numero_es_corta_y_la_de_texto_no(self):
        h = gen.etiquetar_tablas(TABLA)
        self.assertIn('<th class="corta">Nº</th>', h)
        self.assertIn('<td class="corta" data-label="Nº">22</td>', h)
        self.assertNotIn('<th class="corta">Texto', h)
        self.assertIn('<td data-label="Texto">Otra frase larga.</td>', h)

    def test_una_celda_larga_quita_la_clase_de_toda_la_columna(self):
        h = gen.etiquetar_tablas(TABLA.replace('<td>22</td>', '<td>Veintidós mil</td>'))
        self.assertNotIn('corta', h)

    def test_el_css_da_a_la_columna_corta_lo_justo(self):
        css = (SCRIPTS.parent / 'assets' / 'estilo_documento.css').read_text(encoding='utf-8')
        self.assertIn('.seccion td.corta', css)


def hay_navegador() -> bool:
    try:
        from playwright.sync_api import sync_playwright
        spec2 = importlib.util.spec_from_file_location('comprobar_documento', SCRIPTS / 'comprobar_documento.py')
        m = importlib.util.module_from_spec(spec2)
        spec2.loader.exec_module(m)
        with sync_playwright() as pw:
            m.cd.navegador(pw).close()
        return True
    except BaseException:  # noqa: BLE001 — sin Playwright o sin navegador, se saltan
        return False


@unittest.skipUnless(hay_navegador(), 'sin Playwright o sin navegador')
class EnElNavegador(unittest.TestCase):
    def test_el_numero_no_se_lleva_un_tercio_y_el_movil_no_desborda(self):
        from playwright.sync_api import sync_playwright
        spec2 = importlib.util.spec_from_file_location('comprobar_documento', SCRIPTS / 'comprobar_documento.py')
        m = importlib.util.module_from_spec(spec2)
        spec2.loader.exec_module(m)
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / 'tablas.md'
            md.write_text(MD, encoding='utf-8')
            r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(GENERADOR), str(md), '--estilo', 'ninguno'],
                               capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stderr)
            url = (Path(d) / 'tablas.html').as_uri()
            with sync_playwright() as pw:
                b = m.cd.navegador(pw)
                for ancho in (1280, 375):
                    p = b.new_page(viewport={'width': ancho, 'height': 900})
                    p.goto(url)
                    p.evaluate("document.querySelectorAll('details').forEach(x => x.open = true)")
                    self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'), ancho)
                    if ancho == 1280:
                        w = p.evaluate("[...document.querySelector('.seccion table tr').children]"
                                       ".map(c => c.getBoundingClientRect().width)")
                        self.assertLess(w[0], 100)
                        self.assertGreater(w[1], 300)
                        self.assertGreater(w[2], 300)
                b.close()


if __name__ == '__main__':
    unittest.main()


class CifrasEnFila(unittest.TestCase):
    def test_las_cifras_seguidas_van_en_un_contenedor_y_una_sola_no(self):
        dos = gen.a_html('**29 %** uno\n{: .metrica}\n\n**41 %** dos\n{: .metrica}\n\n**7** tres\n{: .metrica}\n')
        self.assertEqual(dos.count('<div class="metricas">'), 1)
        self.assertEqual(dos.count('<p class="metrica">'), 3)
        sola = gen.a_html('**29 %** uno\n{: .metrica}\n\nTexto.\n\n**41 %** dos\n{: .metrica}\n')
        self.assertNotIn('metricas', sola)

    def test_el_css_las_reparte_en_el_ancho(self):
        css = (SCRIPTS.parent / 'assets' / 'estilo_documento.css').read_text(encoding='utf-8')
        self.assertIn('.metricas { display: grid; grid-template-columns: repeat(auto-fit', css)
