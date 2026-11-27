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

    def test_dos_catalogos_con_su_entrada(self):
        # Vigentes y deprecadas, en dos archivos, y el README.md como entrada que conserva su cabecera (decisión 389).
        carpeta = self.raiz / 'sf' / 'decisiones'
        carpeta.mkdir(parents=True)
        decisiones = {
            '001-2026-10-01-uno.md': '# Uno\n\nEstado: deprecada el 2026-11-25 por «Cinco» (5); lo demás, por «Dos» (2).\n\nTexto.\n',
            '002-2026-10-02-dos.md': '# Dos\n\n> **Sustituida en parte** el 2026-10-29 por «Tres»: algo.\n',
            '003-2026-10-03-tres.md': '# Tres\n\n**Sustituida** el 2026-11-01 por «Cuatro | bis».\n',
            '004-2026-10-04-cuatro-bis.md': '# Cuatro | bis\n\n- **Estado:** sustituida por [Cinco](005-2026-10-05-cinco.md)\n\n## Contexto\n',
            '005-2026-10-05-cinco.md': '# Cinco\n\nRecoge lo que sigue valiendo de «Uno» (1), que queda deprecada.\n\n'
                                       'Estado: deprecada el … (ejemplo en el texto, no bajo el título).\n',
        }
        for nombre, texto in decisiones.items():
            (carpeta / nombre).write_text(texto, encoding='utf-8')
        (carpeta / 'README.md').write_text('# Mías\n\nCabecera propia.\n\n## Índice\n\n| viejo |\n', encoding='utf-8')
        self.assertIn('2 vigentes y 3 deprecadas', self.correr())
        readme = (carpeta / 'README.md').read_text(encoding='utf-8')
        self.assertTrue(readme.startswith('# Mías\n\nCabecera propia.\n\n## Índice\n'))
        self.assertIn('[Vigentes](vigentes.md)', readme)
        self.assertIn('[Deprecadas](deprecadas.md)', readme)
        self.assertNotIn('viejo', readme)
        vigentes = (carpeta / 'vigentes.md').read_text(encoding='utf-8')
        self.assertEqual([x for x in vigentes.splitlines() if x.startswith('| ') and x[2].isdigit()], [
            '| 5 | 2026-10-05 | [Cinco](005-2026-10-05-cinco.md) |',
            '| 2 | 2026-10-02 | [Dos](002-2026-10-02-dos.md) (sustituida en parte) |'])
        deprecadas = (carpeta / 'deprecadas.md').read_text(encoding='utf-8')
        self.assertIn('| Nº | Fecha | Decisión | Sustituida por |', deprecadas)
        # Por su número, en el orden de la línea; por su título, en la marca de antes; por su enlace, en la MADR.
        self.assertEqual([x for x in deprecadas.splitlines() if x.startswith('| ') and x[2].isdigit()], [
            '| 4 | 2026-10-04 | [Cuatro \\| bis](004-2026-10-04-cuatro-bis.md) | [Cinco](005-2026-10-05-cinco.md) |',
            '| 3 | 2026-10-03 | [Tres](003-2026-10-03-tres.md) | [Cuatro \\| bis](004-2026-10-04-cuatro-bis.md) |',
            '| 1 | 2026-10-01 | [Uno](001-2026-10-01-uno.md) | [Cinco](005-2026-10-05-cinco.md); [Dos](002-2026-10-02-dos.md) |'])
        # Regenerar no cambia nada.
        catalogos = ('README.md', 'vigentes.md', 'deprecadas.md')
        antes = [(carpeta / x).read_bytes() for x in catalogos]
        self.correr('sf/decisiones')
        self.assertEqual([(carpeta / x).read_bytes() for x in catalogos], antes)

    def test_sin_readme_lleva_el_formato_y_la_fecha_del_registro(self):
        # Decisiones 388 y 390: el formato «regla y porqué» y la fecha del registro, en la cabecera de un proyecto nuevo.
        self.correr()
        carpeta = self.raiz / 'sf' / 'decisiones'
        readme = (carpeta / 'README.md').read_text(encoding='utf-8')
        self.assertIn('la fecha del registro', readme)
        self.assertIn('«Porqué:»', readme)
        self.assertIn('«Estado: deprecada el AAAA-MM-DD por', readme)
        self.assertNotIn('**Origen:**', readme)
        self.assertNotIn('fecha del origen', readme)
        self.assertIn('Ninguna todavía.', (carpeta / 'deprecadas.md').read_text(encoding='utf-8'))
        self.assertIn('Ninguna todavía.', (carpeta / 'vigentes.md').read_text(encoding='utf-8'))

    def test_html_de_los_tres_enlazados_entre_si(self):
        (self.raiz / 'sf' / 'decisiones').mkdir(parents=True)
        (self.raiz / 'sf' / 'decisiones' / '001-2026-10-01-uno.md').write_text('# Uno\n\nTexto.\n', encoding='utf-8')
        self.correr()
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(HERRAMIENTA), 'sf/decisiones', '--html'],
                           cwd=self.raiz, capture_output=True, text=True, encoding='utf-8')
        if r.returncode != 0 and 'No module named' in r.stdout + r.stderr:
            self.skipTest('sin los paquetes del generador')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        carpeta = self.raiz / 'sf' / 'decisiones'
        readme = (carpeta / 'README.html').read_text(encoding='utf-8')
        self.assertIn('href="vigentes.html"', readme)
        self.assertIn('href="deprecadas.html"', readme)
        self.assertIn('href="README.html"', (carpeta / 'vigentes.html').read_text(encoding='utf-8'))
        self.assertIn('href="vigentes.html"', (carpeta / 'deprecadas.html').read_text(encoding='utf-8'))
        # Del .html, con fichas; los .md, en tablas, y sin restos de las variantes (tarea 439).
        self.assertEqual(sorted(x.name for x in carpeta.iterdir()),
                         ['001-2026-10-01-uno.md', 'README.html', 'README.md', 'deprecadas.html', 'deprecadas.md', 'vigentes.html', 'vigentes.md'])
        self.assertIn('class="fichas', (carpeta / 'vigentes.html').read_text(encoding='utf-8'))
        self.assertNotIn(':::', (carpeta / 'vigentes.md').read_text(encoding='utf-8'))

    def test_variantes_html_con_fichas_y_filtros(self):
        # El .html de los catálogos, con los recursos de crear_documentos (tarea 439): tarjetas en la entrada; fichas
        # con la fecha en una insignia, filtro por mes y, en las deprecadas, por cuántas la sustituyen, con su lista.
        import importlib.util
        spec = importlib.util.spec_from_file_location('indice_decisiones', HERRAMIENTA)
        indice = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(indice)
        decisiones = [
            ('001-2026-10-01-uno.md', '# Uno\n\nEstado: deprecada el 2026-11-25 por «Tres» (3) y «Dos» (2).\n'),
            ('002-2026-10-02-dos.md', '# Dos\n\n> **Sustituida en parte** el 2026-10-29 por «Tres»: algo.\n'),
            ('003-2026-11-03-tres.md', '# Tres\n\nTexto.\n'),
        ]
        v = indice.variantes_html('# Mías\n\nEntrada propia.\n\nMás texto.\n\n## Índice\n', decisiones)
        self.assertIn('::: tarjetas 2', v['README.md'])
        self.assertIn('**2** decisiones', v['README.md'])
        self.assertIn('[Ver las deprecadas](deprecadas.md){: .salto}', v['README.md'])
        self.assertIn('## Cómo se llevan {#registro}\n\nMás texto.', v['README.md'])
        self.assertTrue(v['README.md'].startswith('# Mías\n\nEntrada propia.\n\n## Catálogos'))
        self.assertIn('::: fichas 2', v['vigentes.md'])
        self.assertIn('### 3 · [Tres](003-2026-11-03-tres.md) {: #d3}\n\n'
                      '[2026-11-03](#d3){: .insignia data-filtro="2026-11 · noviembre"}', v['vigentes.md'])
        self.assertIn('data-filtro="2026-10 · octubre; Sustituida en parte"', v['vigentes.md'])
        self.assertIn('data-filtro="2026-10 · octubre; Sustituida por 2"', v['deprecadas.md'])
        self.assertIn('Sustituida por\n:   - [Tres](003-2026-11-03-tres.md) (3)\n    - [Dos](002-2026-10-02-dos.md) (2)',
                      v['deprecadas.md'])

    def test_migrar_junto_al_antiguo_como_antes(self):
        (self.raiz / 'docs').mkdir()
        (self.raiz / 'docs' / 'decisiones.md').write_text(ANTIGUO, encoding='utf-8')
        self.correr('docs/decisiones', '--migrar', 'docs/decisiones.md')
        segunda = (self.raiz / 'docs' / 'decisiones' / '002-2026-10-02-segunda.md').read_text(encoding='utf-8')
        self.assertIn('[la visión](../specs/vision.md)', segunda)


if __name__ == '__main__':
    unittest.main()
