"""Pruebas de la skill diagramas: el cálculo de contraste del comprobador y, con un navegador, que el ejemplo pasa
y que una página mala da cada error.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_diagramas.py"
"""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / 'skills' / 'diagramas'
spec = importlib.util.spec_from_file_location('comprobar_diagramas', SKILL / 'scripts' / 'comprobar_diagramas.py')
cd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cd)


def hay_navegador() -> bool:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            cd.navegador(pw).close()
        return True
    except BaseException:  # noqa: BLE001 — sin Playwright o sin navegador, se saltan
        return False


class Contraste(unittest.TestCase):
    def test_blanco_y_negro(self):
        self.assertAlmostEqual(cd.contraste((0, 0, 0), (255, 255, 255)), 21, places=2)

    def test_gris_del_tema(self):
        # --texto-suave #555 sobre blanco: 7,46:1
        self.assertAlmostEqual(cd.contraste((0x55,) * 3, (255, 255, 255)), 7.46, places=2)

    def test_composicion_y_pila(self):
        self.assertEqual(cd.componer((0, 0, 0, 0.5), (255, 255, 255)), (127.5, 127.5, 127.5))
        fondo = cd.fondo_de([(0xe0, 0xf4, 0xf3, 1)], (255, 255, 255, 1))
        self.assertEqual(fondo, (0xe0, 0xf4, 0xf3))

    def test_texto_grande(self):
        self.assertTrue(cd.texto_grande(24, 400))
        self.assertTrue(cd.texto_grande(19, 700))
        self.assertFalse(cd.texto_grande(19, 600))


TEMAS = SKILL.parent / 'crear_documentos'
FUNDACIONAL = SKILL.parent / 'documento_fundacional' / 'scripts' / 'fundacional_to_html.py'
DOCUMENTO = SKILL.parent / 'crear_documentos' / 'scripts' / 'documento_a_html.py'


class TemaTinta(unittest.TestCase):
    """El tema tinta, la paleta de diagram-design, en claro y en oscuro (tema de referencia de los diagramas)."""

    def setUp(self):
        import sys
        sys.path.insert(0, str(TEMAS / 'scripts'))
        import tema_identidad
        self.ti = tema_identidad
        self.tema = tema_identidad.cargar_tema('tinta')

    def test_carga_con_sus_dos_versiones(self):
        c, o = self.tema['colores'], self.tema['colores-oscuro']
        self.assertEqual((c['primario'], c['texto'], c['pagina']), ('#b8431c', '#25283a', '#fbfbfa'))
        self.assertEqual((o['primario'], o['texto'], o['pagina']), ('#f08a59', '#f2f2f0', '#1b1d2c'))
        self.assertEqual(set(c), {r for r, _, _ in self.ti.ROLES})
        self.assertEqual(set(o), {r for r, _, _ in self.ti.ROLES})
        css = self.ti.variables_css(self.tema)
        self.assertIn('--primario: #b8431c;', css)
        self.assertIn(':root[data-theme="dark"] { --primario: #f08a59;', css)

    def test_contraste_de_los_textos(self):
        h = lambda x: tuple(int(x[i:i + 2], 16) for i in (1, 3, 5))
        for colores in (self.tema['colores'], self.tema['colores-oscuro']):
            for fondo in ('pagina', 'fondo-suave'):
                for texto in ('texto', 'texto-suave', 'texto-tenue', 'primario', 'acento', 'oscuro'):
                    k = cd.contraste(h(colores[texto]), h(colores[fondo]))
                    self.assertGreaterEqual(k, 4.5, f'{texto} sobre {fondo}: {k:.2f}')

    def test_un_rol_oscuro_raro_se_rechaza(self):
        import json
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / 'raro.json'
            ruta.write_text(json.dumps({'colores': {'primario': '#b8431c'}, 'colores-oscuro': {'inventado': '#000000'}}), encoding='utf-8')
            with self.assertRaises(SystemExit):
                self.ti.cargar_tema(str(ruta))

    def test_el_generador_lo_acepta(self):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / 'doc.md'
            md.write_text('---\ndestino: proyecto\nherramientas: ninguna\n---\n# Prueba\n\n## Uno | Primera {#uno}\n\nTexto.\n',
                          encoding='utf-8')
            r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(FUNDACIONAL), str(md), '--tema', 'tinta',
                                '--identidad', 'ninguna', '--logo', 'ninguno'], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
            html = md.with_suffix('.html').read_text(encoding='utf-8')
        self.assertIn('--primario: #b8431c;', html)
        self.assertIn('Instrument+Serif', html)


spec_g = importlib.util.spec_from_file_location('generar_diagrama', SKILL / 'scripts' / 'generar_diagrama.py')
gd = importlib.util.module_from_spec(spec_g)
spec_g.loader.exec_module(gd)
EJEMPLOS = sorted((SKILL / 'assets' / 'ejemplos').glob('*.diagrama'))


class Generador(unittest.TestCase):
    """El generador: datos breves → figura con su vertical y su horizontal, mismos ids, fichas y tema."""

    def figura(self, texto):
        m = gd.modelo(gd.leer(texto))
        m['id'] = 'p'
        return gd.figura(m)

    def test_hay_un_ejemplo_por_tipo(self):
        self.assertEqual({p.stem for p in EJEMPLOS}, set(gd.TIPOS))

    def test_las_dos_formas_con_los_mismos_ids(self):
        import re
        for ruta in EJEMPLOS:
            with self.subTest(ruta.stem):
                html, dib, errores = self.figura(ruta.read_text(encoding='utf-8'))
                self.assertEqual(set(dib), {'v', 'h'}, errores)
                svgs = re.findall(r'<svg .*?</svg>', html)
                ids = [sorted(set(re.findall(r'data-nodo="([\w-]+)"', x))) for x in svgs]
                self.assertEqual(ids[0], ids[1])
                self.assertIn('data-diagrama', html)
                self.assertIn('data-ficha=', html)
                self.assertIn('<div class="d-fichas" hidden>', html)   # las fichas, solo para el HUD: sin lista debajo
                self.assertNotIn('<details', html)
                for c in gd.VARIANTES['cajas']:
                    for f in gd.VARIANTES['forma']:
                        self.assertIn(f'data-cajas="{c}" data-forma="{f}" class="vertical', html)

    def test_cajas_plegadas_y_croqueta(self):
        import re
        m = gd.modelo(gd.leer((SKILL / 'assets' / 'ejemplos' / 'estados.diagrama').read_text(encoding='utf-8')))
        m['id'] = 'p'
        for o in ('v', 'h'):
            with self.subTest(o):
                normal, plegada = gd.dibujar(m, o), gd.dibujar(m, o, 'plegadas')
                self.assertLess(plegada.H, normal.H)                       # más compacta, no solo sin texto
                self.assertLess(plegada.cajas['curso'].h, normal.cajas['curso'].h)
                self.assertNotIn('class="d-sb"', ''.join(plegada.nodos))
                croqueta = gd.dibujar(m, o, 'desplegadas', 'croqueta')
                c, r = croqueta.cajas['curso'], croqueta.radio['curso']
                self.assertEqual(r, c.h / 2)
                # cada flecha que llega a una caja toca su borde redondeado: el extremo, dentro de la caja y a 2 o menos
                for d in re.findall(r'data-a="(\w+)" d="[^"]*L([\d.]+),([\d.]+)"', ''.join(croqueta.flechas)):
                    b, x, y = croqueta.cajas[d[0]], float(d[1]), float(d[2])
                    rr = croqueta.radio.get(d[0], 0)
                    if rr and b.x <= x <= b.r and (y <= b.cy):
                        # llega por arriba (al borde de arriba) o por la izquierda (al lado redondo)
                        dx = max(b.x + rr - x, x - (b.r - rr), 0)
                        arriba = b.y + rr - (rr * rr - min(dx, rr) ** 2) ** .5
                        dy = max(b.y + rr - y, y - (b.b - rr), 0)
                        izquierda = b.x + rr - (rr * rr - min(dy, rr) ** 2) ** .5
                        self.assertTrue(abs(y - (arriba - 2)) <= .6 or abs(x - (izquierda - 2)) <= .6, msg=d)

    def test_estados_como_la_sintesis(self):
        html = self.figura((SKILL / 'assets' / 'ejemplos' / 'estados.diagrama').read_text(encoding='utf-8'))[0]
        self.assertIn('data-de="curso" data-a="cerr"', html)               # CERRAR desde En curso
        self.assertIn('d-etiqueta d-b-verde', html)                         # botón sin color: verde
        self.assertIn('Desde en observación o cerradas', html)   # la mono la pone en mayúsculas
        self.assertIn('class="d-nota-c"', html)
        self.assertNotIn('d-b-verde">sin trabajo', html)                    # lo que hace Claude no es un botón
        # ajustes por defecto nuevos, y cada caja con detalle, plegable sola
        for k, v in (('cajas', 'desplegadas'), ('forma', 'redondeada'), ('borde', 'fino'), ('fondo', 'papel'),
                     ('recorrido', 'segundo'), ('lienzo', 'papel')):
            self.assertIn(f'data-d-{k}="{v}"', html)
        self.assertNotIn('d-no-tarjeta', html)
        self.assertIn('data-plegar="curso"', html)
        self.assertIn('class="d-sb d-plegado"', html)                       # el detalle de las plegadas, oculto
        self.assertIn('data-d-cajas="acordeon"', self.figura('opciones: cajas=acordeon\n' + (SKILL / 'assets' / 'ejemplos' / 'estados.diagrama').read_text(encoding='utf-8'))[0])

    def test_errores_que_se_explican(self):
        for texto, trozo in (('tipo: tarta', 'tipo «tarta»'),
                             ('tipo: estados\nnodos:\n  a: A\nflechas:\n  a > b: X', '«b» no es ningún nodo'),
                             ('tipo: estados\nnodos:\n  a: A | x | rara', 'no es una clase de nodo'),
                             ('tipo: estados\nnodos:\n  a: ' + 'Nombre larguísimo ' * 4, 'no cabe')):
            with self.subTest(trozo), self.assertRaises(gd.Error) as e:
                self.figura(texto)
            self.assertIn(trozo, str(e.exception))

    def test_opciones_de_la_decision_302(self):
        base = (SKILL / 'assets' / 'ejemplos' / 'estados.diagrama').read_text(encoding='utf-8')
        html = self.figura(base)[0]
        self.assertIn('d-b-rojo', html)
        self.assertIn('d-cl', html)                 # «claude»: atajo de cursiva y vuelta
        self.assertIn('d-discontinua', html)
        self.assertNotIn('d-carril', html)
        html = self.figura('opciones: carriles, sin color, orientacion=vertical\n' + base)[0]
        self.assertIn('d-carril', html)
        self.assertIn('d-no-color', html)            # el color sigue en el marcado: la herramienta lo puede volver a poner
        self.assertIn('data-d-orientacion="vertical"', html)
        self.assertIn('solo-ancho', html)            # las dos formas, para poder cambiar de orientación
        with self.assertRaises(gd.Error):
            self.figura('opciones: titulo=gigante\n' + base)

    def test_fragmento_en_un_documento(self):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as d:
            frag = Path(d) / 'f.html'
            self.assertEqual(gd.main([str(EJEMPLOS[0]), '--fragmento', '-o', str(frag)]), 0)
            figura = frag.read_text(encoding='utf-8')
            self.assertIn('data-d-tema="tinta"', figura)
            for herr, con_kit in (('recomendadas', True), ('todas -diagramas', False)):
                md = Path(d) / 'doc.md'
                md.write_text(f'---\ndestino: proyecto\nherramientas: {herr}\n---\n# Prueba\n\n## Uno | Primera {{#uno}}\n\nTexto.\n\n{figura}\n',
                              encoding='utf-8')
                r = subprocess.run([sys.executable, '-X', 'utf8', str(DOCUMENTO), str(md), '--identidad', 'ninguna', '--logo', 'ninguno'],
                                   capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
                html = md.with_suffix('.html').read_text(encoding='utf-8')
                self.assertIn('data-kit="skills/diagramas/assets/diagramas.css"', html)
                self.assertIn('data-kit="skills/diagramas/assets/diagramas.js"', html)
                self.assertIn('.diagrama[data-d-tema="tinta"]', html)
                self.assertIn('id="diagramas-temas"', html)
                self.assertEqual('data-kit="tools/kit_documentos/diagramas.js"' in html, con_kit, herr)
                self.assertIn('class="ancho solo-ancho"', html)   # el fragmento pasa entero
            md.write_text('---\ndestino: proyecto\nherramientas: recomendadas\n---\n# Prueba\n\n## Uno | Primera\n\nTexto.\n', encoding='utf-8')
            subprocess.run([sys.executable, '-X', 'utf8', str(DOCUMENTO), str(md), '--identidad', 'ninguna', '--logo', 'ninguno'],
                           capture_output=True, check=True)
            self.assertNotIn('skills/diagramas/assets/diagramas.css', md.with_suffix('.html').read_text(encoding='utf-8'))

    def test_pagina_con_el_tema(self):
        m = gd.modelo(gd.leer(EJEMPLOS[0].read_text(encoding='utf-8')))
        m['id'] = 'p'
        html, _ = gd.pagina(m, 'tinta')
        self.assertIn('--primario:#b8431c;', html)
        self.assertIn(':root[data-theme="dark"]', html)
        self.assertIn('window.sfDiagramas', html)


MALO = """<!doctype html><html><head><meta name="viewport" content="width=device-width"></head>
<body style="margin:0;padding:0 16px"><figure style="margin:0">
<svg viewBox="0 0 400 300" width="100%" role="img" aria-label="malo">
<line x1="0" y1="40" x2="400" y2="40" stroke="#555"/>
<text x="20" y="45" font-size="17">cruzado</text>
<rect x="20" y="80" width="80" height="40" fill="none" stroke="#555"/>
<text x="30" y="105" font-size="17">se sale de la caja</text>
<rect x="60" y="100" width="80" height="40" fill="none" stroke="#555"/>
<text x="200" y="200" font-size="6">menuda</text>
<text x="200" y="240" font-size="17" fill="#bbb">clarito</text>
<text x="205" y="246" font-size="17">pisa</text>
<text x="380" y="280" font-size="17">fuera</text>
<g tabindex="0"><circle cx="300" cy="100" r="5" fill="#555"/></g>
</svg></figure></body></html>"""


@unittest.skipUnless(hay_navegador(), 'sin Playwright o sin navegador')
class EnNavegador(unittest.TestCase):
    def test_el_ejemplo_pasa(self):
        salida = cd.comprobar(SKILL / 'assets' / 'ejemplo-estados.html', [375, 1440], 6.5, ('claro', 'oscuro'))
        for m in salida:
            self.assertIsNone(m['pagina'])
            self.assertEqual(m['interaccion'], [], m['ancho'])
            self.assertEqual(m['js'], [])
            self.assertEqual([e for f in m['figuras'] for e in f['errores']], [], m['ancho'])

    def test_cada_tipo_generado_pasa(self):
        with tempfile.TemporaryDirectory() as d:
            for ruta in EJEMPLOS:
                with self.subTest(ruta.stem):
                    salida = Path(d) / (ruta.stem + '.html')
                    self.assertEqual(gd.main([str(ruta), '-o', str(salida), '--sin-comprobar']), 0)
                    for m in cd.comprobar(salida, [375, 1440], 6.5, ('claro', 'oscuro')):
                        self.assertEqual(m['interaccion'], [], (m['ancho'], m['modo']))
                        self.assertEqual(m['js'], [])
                        self.assertEqual([e for f in m['figuras'] for e in f['errores']], [], (m['ancho'], m['modo']))

    def test_el_documento_de_ejemplo_pasa_y_su_herramienta_cambia_todas(self):
        ruta = SKILL / 'assets' / 'ejemplo-documento.html'
        for m in cd.comprobar(ruta, [375, 1440], 6.5, ('claro',)):
            self.assertEqual(m['interaccion'], [], m['ancho'])
            self.assertEqual(m['js'], [])
            self.assertEqual(len([f for f in m['figuras'] if f['nombre'] != 'Notas']), 6)
            self.assertEqual([e for f in m['figuras'] for e in f['errores']], [], m['ancho'])
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = cd.navegador(pw)
            p = b.new_page(viewport={'width': 1440, 'height': 900})
            p.goto(ruta.resolve().as_uri())
            p.wait_for_timeout(500)
            self.assertEqual(p.locator('#herr-diagramas').get_attribute('data-modo'), 'columna')
            grupos = p.evaluate("() => [...document.querySelectorAll('#herr-diagramas .dg-grupo > summary')].map(s => s.textContent)")
            self.assertEqual(grupos, ['Aspecto general', 'Cabecera', 'Cajas', 'Flechas y etiquetas', 'Notas', 'Interacción', 'Pie'])
            # empiezan plegados; abiertos, todos los desplegables con el mismo ancho y en la misma columna
            self.assertEqual(p.evaluate("document.querySelectorAll('#herr-diagramas .dg-grupo[open]').length"), 0)
            p.evaluate("document.querySelectorAll('#herr-diagramas .dg-grupo').forEach(d => d.open = true)")
            # solo ajustes genéricos: el color y el estilo de cada flecha, de sus datos
            visibles = "() => [...document.querySelectorAll('#herr-diagramas .dg-grupo[data-grupo=flechas] label')].map(l => l.textContent.trim())"
            self.assertIn('Colores de los datos', p.evaluate(visibles))
            self.assertFalse(any('Claude' in x or 'botón' in x for x in p.evaluate(visibles)))
            cajas = p.evaluate("() => [...document.querySelectorAll('#herr-diagramas .dg-grupo select')].map(s => { const r = s.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.width)]; })")
            self.assertEqual(len(set(map(tuple, cajas))), 1, cajas)
            # Flechas y etiquetas y Notas cambian todas las figuras
            p.select_option('#herr-diagramas select[data-dg="esquinas"]', 'rectas')
            self.assertNotIn('Q', p.evaluate("document.querySelector('#estados path[data-da]').getAttribute('d')"))
            p.select_option('#herr-diagramas select[data-dg="esquinas"]', 'redondeadas')
            p.select_option('#herr-diagramas select[data-dg="lugar-nota"]', 'debajo')
            self.assertTrue(p.evaluate("[...document.querySelectorAll('#estados svg.d-notas-svg')].some(s => s.getBoundingClientRect().width)"))
            p.select_option('#herr-diagramas select[data-dg="lugar-nota"]', 'hueco')
            p.select_option('#herr-diagramas select[data-dg="orientacion"]', 'vertical')
            p.uncheck('#herr-diagramas input[data-dg="color"]')
            estado = p.evaluate("() => [...document.querySelectorAll('figure.diagrama')].map(f => [f.dataset.dOrientacion, f.classList.contains('d-no-color')])")
            self.assertEqual(estado, [['vertical', True]] * 6)
            p.click('#herr-diagramas [data-dg-poner="def"]')
            estado = p.evaluate("() => [...document.querySelectorAll('figure.diagrama')].map(f => [f.dataset.dOrientacion, f.classList.contains('d-no-color'), f.dataset.dTema])")
            self.assertEqual(estado, [['auto', False, 'tinta']] * 6)
            # «Letra más grande» cambia la letra de las seis figuras, también en la horizontal
            escala = "() => [...document.querySelectorAll('figure.diagrama')].map(f => getComputedStyle([...f.querySelectorAll('svg')].find(s => s.getBoundingClientRect().width).querySelector('.d-nn')).transform)"
            self.assertEqual(set(p.evaluate(escala)), {'none'})
            p.check('#herr-diagramas input[data-dg="letra"]')
            self.assertNotIn('none', p.evaluate(escala))
            p.uncheck('#herr-diagramas input[data-dg="letra"]')
            # el circulito pliega su caja sola, sin abrir la ficha, y su flecha sigue tocándola
            caja = "() => { const s = [...document.querySelectorAll('#estados svg')].find(s => s.getBoundingClientRect().width); const r = s.querySelector('[data-nodo=\"obs\"] .d-caja'); const f = s.querySelector('path[data-a=\"obs\"][data-de=\"curso\"]').getAttribute('d').match(/(-?[\\d.]+),(-?[\\d.]+)$/); return [+r.getAttribute('y'), +r.getAttribute('height'), +f[2]]; }"
            y, h, fy = p.evaluate(caja)
            p.locator('#estados svg:visible [data-plegar="obs"]').click()
            y2, h2, fy2 = p.evaluate(caja)
            self.assertLess(h2, h)
            self.assertTrue(y2 - 3 <= fy2 <= y2 + h2, (fy2, y2, h2))   # la flecha (ahora recta, por el lado) sigue en la caja
            self.assertTrue(p.evaluate("document.querySelector('#estados .d-hud').hidden"))
            self.assertEqual(p.locator('#estados svg:visible [data-plegar="obs"]').get_attribute('aria-expanded'), 'false')
            # recorrido en el segundo color del tema (en tinta, azul)
            p.locator('#estados svg:visible [data-nodo="pend"]').hover()
            p.wait_for_timeout(400)   # la transición del resaltado
            self.assertEqual(p.evaluate("getComputedStyle([...document.querySelectorAll('#estados path.d-on')].find(e => e.getBoundingClientRect().width)).stroke"), 'rgb(47, 85, 151)')
            b.close()

    def test_una_pagina_mala_da_cada_error(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / 'malo.html'
            ruta.write_text(MALO, encoding='utf-8')
            m = cd.comprobar(ruta, [375], 6.5)[0]
        errores = ' | '.join(m['figuras'][0]['errores'])
        for trozo in ('role="img" con elementos que se pulsan', 'se pulsa en', 'letra de', '«menuda»',
                      'se sale de su caja', '«fuera» se sale del dibujo', 'se pisan', 'dos cajas se pisan',
                      'una línea cruza «cruzado»', 'contraste'):
            self.assertIn(trozo, errores)


if __name__ == '__main__':
    unittest.main()
