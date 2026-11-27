"""Pruebas del recurso «Bloques de código» de crear_documentos (tarea 396): la caja con el lenguaje, el coloreado propio,
el botón «Copiar» (assets/codigo.js), pagina.codigo del estilo, el desplazamiento en el móvil y la impresión en A4.

python -I -X utf8 -m pytest plugins/sf/tests/test_codigo.py
"""
import html
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CREAR = Path(__file__).resolve().parents[1] / 'skills' / 'crear_documentos'
GENERADOR = CREAR / 'scripts' / 'documento_a_html.py'
CSS = (CREAR / 'assets' / 'estilo_documento.css').read_text(encoding='utf-8')
_spec = importlib.util.spec_from_file_location('resaltar_codigo', CREAR / 'scripts' / 'resaltar_codigo.py')
rc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rc)
VALLA = '`' * 3


def bloque(lenguaje: str, codigo: str) -> str:
    """El HTML que deja markdown para un bloque de código con ese lenguaje."""
    clase = f' class="language-{lenguaje}"' if lenguaje else ''
    return f'<pre><code{clase}>{html.escape(codigo, quote=False)}\n</code></pre>'


def valla(lenguaje: str, codigo: str) -> str:
    return f'\n{VALLA}{lenguaje}\n{codigo}\n{VALLA}\n'


class Caja(unittest.TestCase):
    def test_json_en_su_caja_con_el_lenguaje_y_saltos(self):
        h = rc.resaltar(bloque('json', '{\n  "a": 1,\n  "b": [true, null]\n}'))
        self.assertTrue(h.startswith('<div class="codigo" data-lenguaje="json"><div class="codigo-barra">'
                                     '<span class="codigo-lenguaje">JSON</span></div><pre><code class="language-json">'))
        self.assertIn('<span class="amb"><span class="amb-cabeza">{<span class="amb-marca"></span>\n</span>'
                      '<span class="amb-cuerpo">  <span class="sx-p">"a"</span>: <span class="sx-n">1</span>,\n', h)
        self.assertIn('<span class="sx-n">true</span>', h)
        self.assertTrue(h.endswith('</code></pre></div>'))

    def test_python_y_bash_coloreados(self):
        py = rc.resaltar(bloque('python', 'def f(x):\n    # nota\n    return "x"'))
        self.assertIn('<span class="codigo-lenguaje">Python</span>', py)
        for trozo in ('<span class="sx-k">def</span>', '<span class="sx-c"># nota</span>', '<span class="sx-s">"x"</span>'):
            self.assertIn(trozo, py)
        sh = rc.resaltar(bloque('bash', 'ls -la "$HOME" | grep x'))
        self.assertIn('<span class="codigo-lenguaje">Bash</span>', sh)
        for trozo in ('<span class="sx-f">ls</span>', '<span class="sx-a">-la</span>', '<span class="sx-f">grep</span>'):
            self.assertIn(trozo, sh)

    def test_sin_lenguaje_sin_barra_y_json_si_lo_es(self):
        arbol = rc.resaltar(bloque('', 'docs/\n└── a.md'))
        self.assertEqual(arbol, '<div class="codigo"><pre><code>docs/\n└── a.md\n</code></pre></div>')
        js = rc.resaltar(bloque('', '{"a": 1}'))
        self.assertIn('<pre><code class="language-json">{<span class="sx-p">"a"</span>', js)
        self.assertNotIn('codigo-barra', js)

    def test_alias_con_su_nombre_y_lenguaje_sin_coloreado(self):
        ps = rc.resaltar(bloque('powershell', 'Get-ChildItem -Path .'))
        self.assertIn('data-lenguaje="powershell"', ps)
        self.assertIn('<span class="codigo-lenguaje">PowerShell</span>', ps)
        self.assertIn('class="language-bash"', ps)
        rust = rc.resaltar(bloque('rust', 'fn main() { println!("<hola>"); }'))
        self.assertIn('<span class="codigo-lenguaje">rust</span>', rust)
        self.assertIn('println!("&lt;hola&gt;")', rust)  # tal cual, escapado
        self.assertNotIn('sx-', rust)
        self.assertNotIn('codigo-barra', rc.resaltar(bloque('text', 'hola')))

    def test_el_codigo_no_se_altera(self):
        for lenguaje, codigo in (('python', 'if a < b and c > "d":\n\tprint(\'&amp;\')  # ok\n    """doc\nmás"""'),
                                 ('json', '{\n  "a": [\n    1\n  ]\n}'), ('', 'a\n  b\n    c\n\nd'),
                                 ('rust', 'fn f() {\n    let s = "}";\n}')):
            h = rc.resaltar(bloque(lenguaje, codigo))
            dentro = re.search(r'<pre>(.*)</pre>', h, re.S).group(1)
            self.assertEqual(html.unescape(re.sub(r'<[^>]+>', '', dentro)), codigo + '\n', lenguaje)
            self.assertEqual(dentro.count('<span'), dentro.count('</span>'))


class Ambitos(unittest.TestCase):
    """Los ámbitos plegables: (línea de apertura, última línea del cuerpo), contando desde 0."""

    def test_json_por_llaves_y_corchetes_anidados(self):
        codigo = '{\n  "a": [\n    1,\n    2\n  ],\n  "b": {"c": 1},\n  "d": {\n    "e": "}"\n  }\n}'
        self.assertEqual(rc.ambitos(codigo, 'json', 'json'), [(0, 8), (1, 3), (6, 7)])

    def test_una_linea_no_es_ambito(self):
        self.assertEqual(rc.ambitos('{"a": [1, 2]}', 'json', 'json'), [])
        self.assertEqual(rc.ambitos('{\n}', 'json', 'json'), [])  # sin cuerpo
        self.assertEqual(rc.ambitos('x = 1\ny = 2', 'python', 'python'), [])

    def test_llaves_en_cadenas_y_comentarios_no_cuentan(self):
        codigo = 'function f() {\n  // }\n  const s = "{";\n  if (a) {\n    b();\n  }\n}'
        self.assertEqual(rc.ambitos(codigo, 'ts', 'javascript'), [(0, 5), (3, 4)])

    def test_python_por_sangria(self):
        codigo = 'class A:\n    def f(self):\n        if x:\n            return 1\n\n        return 2\n\nprint(A)'
        self.assertEqual(rc.ambitos(codigo, 'python', 'python'), [(0, 5), (1, 5), (2, 3)])

    def test_bash_y_yaml_por_sangria(self):
        bash = 'f() {\n    if [ -f x ]; then\n        echo si\n    fi\n}\nfor a in b; do\n    echo "$a"\ndone'
        self.assertEqual(rc.ambitos(bash, 'bash', 'bash'), [(0, 3), (1, 2), (5, 6)])
        yaml = 'a:\n  b: 1\n  c:\n    - x\n    - y\nd: 2'
        self.assertEqual(rc.ambitos(yaml, 'yaml', 'yaml'), [(0, 4), (2, 4)])

    def test_powershell_y_rust_por_llaves(self):
        ps = 'function F {\n    Get-Item | Where-Object {\n        $_.Length\n    }\n}'
        self.assertEqual(rc.ambitos(ps, 'powershell', 'bash'), [(0, 3), (1, 2)])
        rust = 'fn main() {\n    let s = "{";\n    if a {\n        b();\n    }\n}'
        self.assertEqual(rc.ambitos(rust, 'rust', 'rust'), [(0, 4), (2, 3)])

    def test_sin_lenguaje_por_sangria_aunque_sea_json(self):
        self.assertEqual(rc.ambitos('docs/\n    a.md\n    b/\n        c.md\nsf/', '', ''), [(0, 3), (2, 3)])
        self.assertEqual(rc.ambitos('{\n  "a": 1\n}', '', 'json'), [(0, 1)])

    def test_una_apertura_con_dos_ambitos_toma_el_mayor(self):
        self.assertEqual(rc.ambitos('[{\n  "a": 1\n},\n{\n  "b": 2\n}]', 'json', 'json'), [(0, 4), (3, 4)])

    def test_marcado_anidado(self):
        h = rc.con_ambitos(['a {', 'b {', 'c', '}', '}'], [(0, 3), (1, 2)])
        self.assertEqual(h, '<span class="amb"><span class="amb-cabeza">a {<span class="amb-marca"></span>\n</span>'
                            '<span class="amb-cuerpo"><span class="amb"><span class="amb-cabeza">b {'
                            '<span class="amb-marca"></span>\n</span><span class="amb-cuerpo">c\n</span></span>}\n'
                            '</span></span>}')


class Hoja(unittest.TestCase):
    def test_desplazamiento_dentro_de_la_caja_y_columnas_que_no_crecen(self):
        self.assertIn('overflow-x: auto', CSS[CSS.index('pre { background'):])
        self.assertIn(':is(.tarjeta, .columna, .tarjeta-cuerpo) { min-width: 0; }', CSS)

    def test_caja_sin_filete_y_con_las_esquinas_del_estilo(self):
        caja = re.search(r'^\.codigo \{[^}]*\}', CSS, re.M).group(0)
        self.assertNotIn('border-left', caja)
        self.assertIn('border-radius: var(--esquinas, 8px);', caja)
        self.assertNotIn('border-left', re.search(r'^pre \{[^}]*\}', CSS, re.M).group(0))

    def test_impresion_desplegada_sin_botones_y_con_las_lineas_partidas(self):
        impresion = CSS[CSS.index('@media print {\n  @page'):]
        self.assertIn('.codigo-copiar, .codigo-lineas, .codigo-plegar::before, '
                      '.codigo-barra:not(:has(.codigo-lenguaje:not(.codigo-generico))) {\n    display: none !important; }',
                      impresion)
        self.assertIn('.codigo > pre[hidden] { display: block !important; }', impresion)
        self.assertIn('.amb-flecha, .amb-marca { display: none !important; }', impresion)
        self.assertIn('.amb-cuerpo[hidden] { display: inline !important; }', impresion)
        self.assertIn('white-space: pre-wrap; overflow-wrap: anywhere; overflow: visible;', impresion)

    def test_el_plegado_es_un_boton_accesible(self):
        js = (CREAR / 'assets' / 'codigo.js').read_text(encoding='utf-8')
        for trozo in ("plegar.type = 'button'", "setAttribute('aria-expanded', 'true')", "setAttribute('aria-controls', pre.id)",
                      "pre.hidden = abierto", "'codigo-lenguaje codigo-generico'"):
            self.assertIn(trozo, js)

    def test_colores_del_codigo_en_oscuro(self):
        sys.path.insert(0, str(CREAR / 'scripts'))
        import tema_identidad as ti
        css = ti.variables_css(ti.cargar_tema('morado'))
        oscuro = css[css.index(':root[data-theme="dark"]'):]
        for k in ti.SX_FIJOS:
            self.assertIn(f'--sx-{k}:', oscuro)


class Generador(unittest.TestCase):
    MD = """---
destino: proyecto
herramientas: ninguna
---
# Prueba

## Uno | Primera {{#uno}}

Texto.
{codigo}
"""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.raiz = Path(self._tmp.name)
        (self.raiz / 'docs').mkdir()
        self.md = self.raiz / 'docs' / 'doc.md'

    def tearDown(self):
        self._tmp.cleanup()

    def generar(self, codigo: str, estilo: dict = None) -> str:
        if estilo:
            ident = self.raiz / 'docs' / 'identidad'
            ident.mkdir(exist_ok=True)
            (ident / 'estilo.json').write_text(json.dumps(estilo), encoding='utf-8')
        self.md.write_text(self.MD.format(codigo=codigo), encoding='utf-8')
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(GENERADOR), str(self.md)],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        return self.md.with_suffix('.html').read_text(encoding='utf-8')

    def test_el_boton_entra_solo_con_codigo(self):
        h = self.generar(valla('json', '{\n  "a": 1\n}'))
        self.assertIn('<div class="codigo" data-lenguaje="json">', h)
        self.assertIn('data-kit="skills/crear_documentos/assets/codigo.js"', h)
        self.assertNotIn('data-kit="skills/crear_documentos/assets/codigo.js"', self.generar(''))

    def test_bloque_dentro_de_una_tarjeta(self):
        h = self.generar('\n::: tarjetas 2\n\n### Una\n' + valla('bash', 'ls -la') + '\n### Otra\n\nTexto.\n\n:::\n')
        self.assertIn('<div class="codigo" data-lenguaje="bash"><div class="codigo-barra">', h)

    def test_pagina_codigo_linea(self):
        tema = json.loads((CREAR / 'assets' / 'temas' / 'morado.json').read_text(encoding='utf-8'))
        estilo = {'version': 1, 'origen': 'morado', 'historial': [], 'colores': dict(tema['colores']),
                  'letra': dict(tema['tipografias']), 'pagina': {'codigo': 'linea'}}
        h = self.generar(valla('json', '{"a": 1}'), estilo)
        self.assertIn('pre, .codigo { background: none; border-left: 0;', h)
        self.assertIn('.codigo > pre { border: 0;', h)

    def test_en_el_navegador_cada_bloque_se_pliega_por_separado(self):
        """Con teclado y ratón, cada bloque (también el que no tiene lenguaje) se pliega solo; al imprimir, desplegado."""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            self.skipTest('sin Playwright')
        self.generar(valla('json', '{\n  "a": 1\n}') + valla('', 'docs/\n└── a.md'))
        with sync_playwright() as pw:
            nav = None
            for canal in (None, 'chrome', 'msedge'):
                try:
                    nav = pw.chromium.launch(channel=canal) if canal else pw.chromium.launch()
                    break
                except Exception:  # noqa: BLE001 — se prueba el siguiente
                    continue
            if not nav:
                self.skipTest('sin navegador')
            try:
                p = nav.new_page()
                p.goto(self.md.with_suffix('.html').resolve().as_uri())
                botones = p.locator('.codigo-plegar')
                self.assertEqual(botones.count(), 2)
                self.assertEqual(p.locator('.codigo-generico').text_content(), 'Código')
                self.assertEqual(botones.nth(0).get_attribute('aria-expanded'), 'true')
                botones.nth(0).focus()
                p.keyboard.press('Enter')
                self.assertEqual(botones.nth(0).get_attribute('aria-expanded'), 'false')
                self.assertFalse(p.locator('.codigo >> nth=0 >> pre').is_visible())
                self.assertTrue(p.locator('.codigo >> nth=1 >> pre').is_visible())
                self.assertIn('3 líneas', botones.nth(0).inner_text())
                botones.nth(1).click()
                self.assertEqual(botones.nth(1).get_attribute('aria-expanded'), 'false')
                p.emulate_media(media='print')
                self.assertTrue(p.locator('.codigo >> nth=0 >> pre').is_visible())
                self.assertFalse(p.locator('.codigo-copiar >> nth=0').is_visible())
                self.assertFalse(p.locator('.codigo-generico').is_visible())
                p.emulate_media(media='screen')
                botones.nth(0).focus()
                p.keyboard.press('Space')
                self.assertEqual(botones.nth(0).get_attribute('aria-expanded'), 'true')
            finally:
                nav.close()

    def test_en_el_navegador_los_ambitos_se_pliegan_por_dentro(self):
        """Cada ámbito se pliega solo, con teclado; plegado, «…» y la línea de cierre; «Copiar» copia todo; al imprimir,
        desplegado y sin flechas."""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            self.skipTest('sin Playwright')
        codigo = '{\n  "a": [\n    1,\n    2\n  ],\n  "b": {"c": 1}\n}'
        self.generar(valla('json', codigo))
        with sync_playwright() as pw:
            nav = None
            for canal in (None, 'chrome', 'msedge'):
                try:
                    nav = pw.chromium.launch(channel=canal) if canal else pw.chromium.launch()
                    break
                except Exception:  # noqa: BLE001 — se prueba el siguiente
                    continue
            if not nav:
                self.skipTest('sin navegador')
            try:
                p = nav.new_page(viewport={'width': 390, 'height': 844})
                p.goto(self.md.with_suffix('.html').resolve().as_uri())
                flechas = p.locator('.amb-flecha')
                self.assertEqual(flechas.count(), 2)  # «{» y «"a": [»; «"b": {…}» es de una línea
                interior = flechas.nth(1)
                self.assertEqual(interior.get_attribute('aria-expanded'), 'true')
                self.assertEqual(interior.text_content(), '')
                interior.focus()
                p.keyboard.press('Enter')
                self.assertEqual(interior.get_attribute('aria-expanded'), 'false')
                cuerpo = p.locator('#' + interior.get_attribute('aria-controls'))
                self.assertFalse(cuerpo.is_visible())
                visible = p.locator('pre code').inner_text()
                marca = p.evaluate("getComputedStyle(document.querySelectorAll('.amb-marca')[1], '::after').content")
                self.assertEqual(marca, '"…"')
                self.assertIn('],', visible)  # la línea de cierre, a la vista
                self.assertEqual(flechas.nth(0).get_attribute('aria-expanded'), 'true')  # el de fuera, abierto
                texto = p.evaluate("document.querySelector('pre code').textContent")
                self.assertEqual(texto, codigo + '\n')  # lo que copia «Copiar»: todo
                self.assertEqual(p.evaluate('document.documentElement.scrollWidth'), 390)
                p.emulate_media(media='print')
                self.assertTrue(cuerpo.is_visible())
                self.assertFalse(interior.is_visible())
                p.emulate_media(media='screen')
                interior.click()
                self.assertTrue(cuerpo.is_visible())
            finally:
                nav.close()


if __name__ == '__main__':
    unittest.main()
