"""Pruebas de la skill fijar_estilo (scripts/estilo.py): estilo completo desde un tema (decisión 317), valores en prueba
fuera de estilo.json hasta aceptarlos, versión, historial y respaldo en cada afinado (322), muestras del generador y
contraste (320).

python -I -X utf8 -m pytest plugins/sf/tests/test_fijar_estilo.py
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / 'skills'
ESTILO = SKILLS / 'fijar_estilo' / 'scripts' / 'estilo.py'
sys.path.insert(0, str(SKILLS / 'crear_documentos' / 'scripts'))
from tema_identidad import ROLES_VALIDOS  # noqa: E402

MD = """---
destino: proyecto
herramientas: ninguna
---
# Prueba

## Uno | Primera {#uno}

Texto.
"""


class FijarEstilo(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.raiz = Path(self._tmp.name)
        (self.raiz / 'docs').mkdir()
        self.doc = self.raiz / 'docs' / 'prueba.md'
        self.doc.write_text(MD, encoding='utf-8')
        self.ident = self.raiz / 'docs' / 'identidad'

    def tearDown(self):
        self._tmp.cleanup()

    def correr(self, *args, ok=True):
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(ESTILO), '--raiz', str(self.raiz), *args],
                           capture_output=True, text=True, encoding='utf-8')
        if ok:
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        else:
            self.assertNotEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout + r.stderr

    def leer(self, nombre):
        return json.loads((self.ident / nombre).read_text(encoding='utf-8'))

    def test_catalogo_ensena_cada_tema_en_claro_y_en_oscuro_sin_tocar_el_estilo(self):
        salida = self.correr('catalogo')
        carpeta = self.ident / 'catalogo-temas'
        temas = sorted(p.stem for p in (SKILLS / 'fijar_estilo' / 'assets' / 'juegos').glob('*.json'))  # una por tema
        self.assertIn(f"Catálogo de temas: {carpeta / 'catalogo-temas.html'}", salida)
        self.assertEqual(sorted(p.name for p in carpeta.iterdir()),
                         sorted(['catalogo-temas.html', *(f'muestra-{t}.html' for t in temas)]))  # sin archivos de paso
        h = (carpeta / 'catalogo-temas.html').read_text(encoding='utf-8')
        for t in temas:
            with self.subTest(t):
                self.assertIn(f'id="tema-{t}"', h)
                self.assertIn(f'estilo.py partir {t}', h)
                for vista in ('', '#recuadros', '#diagrama'):  # tres vistas, en claro y en oscuro: la muestra real
                    self.assertIn(f'<iframe src="muestra-{t}.html{vista}"', h)
                    self.assertIn(f'<iframe src="muestra-{t}.html?modo=oscuro{vista}"', h)
                muestra = (carpeta / f'muestra-{t}.html').read_text(encoding='utf-8')
                self.assertIn("get('modo')!=='oscuro'", muestra)
                self.assertIn('<table', muestra)
                self.assertIn('<svg', muestra)  # el diagrama
        self.assertIn('id="contraste"', h)
        self.assertIn('Todas las muestras pasan la comprobación de contraste', h)
        self.assertFalse((self.ident / 'estilo.json').exists())
        self.assertFalse((self.ident / 'estilo.prueba.json').exists())
        self.assertIn('Es un activo del proyecto', salida)

    def test_el_catalogo_usa_el_estilo_del_proyecto(self):
        self.correr('partir', 'tinta', 'colores.primario=#f5c400', 'colores.sobre-primario=#1a1a1a')
        self.correr('aceptar', '--motivo', 'x')
        self.correr('catalogo')
        h = (self.ident / 'catalogo-temas' / 'catalogo-temas.html').read_text(encoding='utf-8')
        self.assertIn('--primario: #f5c400', h)  # el aspecto del catálogo es el del proyecto (353)
        self.assertIn('estilo v1', h)
        self.assertFalse((self.ident / 'estilo.catalogo.json').exists())

    def test_partir_de_una_muestra_del_plugin_por_su_nombre(self):
        self.correr('partir', 'tecnico')
        e = self.leer('estilo.prueba.json')
        self.assertEqual(e['origen'], 'pool')  # su tema, como origen (317)
        self.assertEqual((e['portada']['forma'], e['secciones']['marcador'], e['pagina']['pie']),
                         ('oscura', 'cuadrado', 'oscuro'))

    def test_el_catalogo_ensena_el_estilo_del_proyecto_tal_cual(self):
        (self.ident).mkdir(parents=True, exist_ok=True)
        (self.ident / 'logo.svg').write_text('<svg viewBox="0 0 40 40"><rect fill="#123456"/></svg>', encoding='utf-8')
        self.correr('partir', 'teal', 'colores.primario=#f5c400', 'colores.sobre-primario=#1a1a1a',
                    'portada.forma=oscura', 'portada.fondo=primario', 'identidad.logo=["logo.svg"]')
        self.correr('aceptar', '--motivo', 'x')
        self.correr('catalogo')
        h = (self.ident / 'catalogo-temas' / 'catalogo-temas.html').read_text(encoding='utf-8')
        self.assertIn('G · Estilo del proyecto (v1)', h)
        self.assertIn('Es el estilo actual', h)
        muestra = (self.ident / 'catalogo-temas' / 'muestra-proyecto.html').read_text(encoding='utf-8')
        self.assertIn('<header class="portada oscura">', muestra)  # su portada destacada, tal cual
        self.assertIn('data:image/svg+xml;base64,', muestra)  # con su logo
        self.assertEqual(list(self.ident.glob('estilo.catalogo*.json')), [])  # sin archivos de paso

    def test_la_miniatura_de_portada_la_ensena_entera(self):
        """El marco de la miniatura (960 × 600, como CSS_CATALOGO) cabe la portada de cada muestra sin cortarla."""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            self.skipTest('sin Playwright')
        self.correr('catalogo')
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
                for muestra in sorted((self.ident / 'catalogo-temas').glob('muestra-*.html')):
                    p = nav.new_page(viewport={'width': 960, 'height': 600})
                    p.goto(muestra.resolve().as_uri())
                    bajo = p.evaluate("document.querySelector('.portada').getBoundingClientRect().bottom")
                    p.close()
                    with self.subTest(muestra.name):
                        self.assertLess(bajo, 600)
            finally:
                nav.close()

    def test_el_estilo_puede_tener_nombre_y_el_catalogo_lo_usa(self):
        self.correr('partir', 'teal')
        self.correr('aceptar', '--motivo', 'x')
        salida = self.correr('cambiar', 'nombre=Áureo')
        self.assertIn('nombre: "Áureo"', salida)
        self.correr('aceptar', '--motivo', 'Nombre del estilo')
        estilo = json.loads((self.ident / 'estilo.json').read_text(encoding='utf-8'))
        self.assertEqual((estilo['nombre'], estilo['version']), ('Áureo', 2))
        self.assertIn('«Áureo», versión 2', self.correr('ver'))
        self.correr('catalogo')
        h = (self.ident / 'catalogo-temas' / 'catalogo-temas.html').read_text(encoding='utf-8')
        self.assertIn('G · Áureo (estilo del proyecto, v2)', h)
        self.correr('cambiar', 'nombre=')
        self.assertNotIn('nombre', json.loads((self.ident / 'estilo.prueba.json').read_text(encoding='utf-8')))

    def test_sin_estilo_el_catalogo_anade_tinta_con_el_color_del_proyecto(self):
        (self.raiz / '.sf').mkdir()
        (self.raiz / '.sf' / 'proyecto.json').write_text('{"color": "#c2410c"}', encoding='utf-8')
        self.correr('catalogo')
        h = (self.ident / 'catalogo-temas' / 'catalogo-temas.html').read_text(encoding='utf-8')
        self.assertIn('G · Color del proyecto', h)
        self.assertIn('estilo.py partir tinta colores.primario=#c2410c colores.sobre-primario=', h)

    def test_el_catalogo_no_sale_fuera_del_proyecto(self):
        with tempfile.TemporaryDirectory() as fuera:
            salida = self.correr('catalogo', '--salida', fuera, ok=False)
            self.assertIn('va dentro de él (decisión 352)', salida)
            self.assertEqual(list(Path(fuera).iterdir()), [])

    def test_partir_resuelve_todos_los_valores_con_el_tema_como_origen(self):
        self.correr('partir', 'colorido')
        e = self.leer('estilo.prueba.json')
        self.assertEqual(e['origen'], 'colorido')
        self.assertEqual(set(ROLES_VALIDOS) - set(e['colores']), set())  # todos los roles, derivados los que faltan
        self.assertEqual(len(e['colores']['serie']), 6)
        self.assertEqual(set(e['colores']['significado']), {'correcto', 'aviso', 'error', 'info'})
        for grupo in ('letra', 'portada', 'secciones', 'pagina', 'diagramas', 'aparte'):
            self.assertIn(grupo, e)
        # Las opciones de aspecto del tema vuelven como valores resueltos (331).
        self.assertEqual(e['secciones']['etiqueta'], 'solida')
        self.assertEqual(e['secciones']['opacidad'], 0.4)
        self.assertEqual(e['secciones']['marcador'], 'ninguno')
        self.assertEqual(e['pagina']['esquinas'], 16)
        self.assertNotIn('destino', e['lectura'])  # el generador no elige por el autor (183)
        self.assertFalse((self.ident / 'estilo.json').exists())

    def test_cabecera_del_tema_pasa_a_la_portada(self):
        self.correr('partir', 'teal')
        tema = json.loads((SKILLS / 'crear_documentos' / 'assets' / 'temas' / 'teal.json').read_text(encoding='utf-8'))
        portada = self.leer('estilo.prueba.json')['portada']
        cabecera = tema.get('estilo', {}).get('cabecera', 'blanca')
        self.assertEqual(portada['forma'], 'clara' if cabecera == 'blanca' else 'oscura')

    def test_partir_desde_un_juego(self):
        self.correr('partir', 'tinta')
        juego = self.raiz / 'juego.json'
        e = self.leer('estilo.prueba.json')
        e.update(origen='sf-amarillo', version=7)
        juego.write_text(json.dumps(e), encoding='utf-8')
        self.correr('partir', str(juego))
        e = self.leer('estilo.prueba.json')
        self.assertEqual((e['origen'], e['version']), ('sf-amarillo', 1))

    def test_cambiar_valida_con_el_catalogo(self):
        self.correr('partir', 'morado')
        salida = self.correr('cambiar', 'secciones.etiqueta=rara', ok=False)
        self.assertIn('Posibles', salida)
        self.correr('cambiar', 'secciones.etiqueta=linea', 'pagina.esquinas=4', 'colores.significado.aviso=#8a4a10')
        e = self.leer('estilo.prueba.json')
        self.assertEqual((e['secciones']['etiqueta'], e['pagina']['esquinas']), ('linea', 4))
        self.assertEqual(e['colores']['significado']['aviso'], '#8a4a10')
        self.correr('cambiar', 'pagina.esquinas=')
        self.assertNotIn('esquinas', self.leer('estilo.prueba.json')['pagina'])

    def test_aceptar_sube_la_version_anota_el_historial_y_respalda(self):
        self.correr('partir', 'tinta')
        self.correr('aceptar', '--motivo', 'muestra F', '--fecha', '2026-11-23')
        v1 = self.leer('estilo.json')
        self.assertEqual(v1['version'], 1)
        self.assertEqual(v1['historial'], [{'version': 1, 'fecha': '2026-11-23', 'cambio': 'estilo de partida desde tinta',
                                            'motivo': 'muestra F'}])
        self.assertFalse((self.ident / 'estilo.prueba.json').exists())
        # Lo que se prueba no toca estilo.json hasta aceptarlo.
        self.correr('cambiar', 'secciones.cabecera=titulo')
        self.assertEqual(self.leer('estilo.json'), v1)
        self.correr('aceptar', '--motivo', 'más limpio', '--fecha', '2026-11-24')
        v2 = self.leer('estilo.json')
        self.assertEqual(v2['version'], 2)
        self.assertEqual(v2['origen'], 'tinta')
        self.assertEqual(v2['secciones']['cabecera'], 'titulo')
        self.assertEqual(v2['historial'][-1], {'version': 2, 'fecha': '2026-11-24',
                                               'cambio': 'secciones.cabecera: "titulo"', 'motivo': 'más limpio'})
        self.assertEqual(json.loads((self.ident / '_respaldo' / 'estilo_v1.json').read_text(encoding='utf-8')), v1)

    def test_la_primera_aceptacion_no_repite_el_motivo(self):
        self.correr('partir', 'tinta', 'pagina.pie=oscuro')
        salida = self.correr('aceptar', '--motivo', 'Estilo de partida desde tinta, con pagina.pie: "oscuro"')
        self.assertEqual(self.leer('estilo.json')['historial'][0]['cambio'],
                         'estilo de partida desde tinta, con pagina.pie: "oscuro"')
        self.assertEqual(salida.count('estilo de partida'), 1, salida)
        self.assertEqual(self.correr('ver').lower().count('estilo de partida'), 1)

    def test_aceptar_sin_cambios_o_sin_prueba_no_hace_nada(self):
        self.correr('aceptar', '--motivo', 'x', ok=False)
        self.correr('partir', 'tinta')
        self.correr('aceptar', '--motivo', 'x')
        self.correr('cambiar', 'secciones.plegado=primera')
        self.assertIn('igual', self.correr('aceptar', '--motivo', 'y', ok=False))

    def test_no_acepta_un_texto_por_debajo_de_4_5(self):
        self.correr('partir', 'pool', 'colores.acento=#b36e1d')  # el acento de pool antes de la 392
        salida = self.correr('aceptar', '--motivo', 'x', ok=False)
        self.assertIn('4.5:1', salida)
        self.assertFalse((self.ident / 'estilo.json').exists())

    def test_muestras_con_el_generador_y_descartar(self):
        self.correr('partir', 'tinta', 'secciones.cabecera=numero-titulo')
        salida = self.correr('muestras', str(self.doc), 'prueba', 'rojo')
        prueba = self.raiz / 'docs' / 'prueba.muestra-prueba.html'
        rojo = self.raiz / 'docs' / 'prueba.muestra-rojo.html'
        self.assertTrue(prueba.is_file(), salida)
        self.assertTrue(rojo.is_file(), salida)
        self.assertIn('estilo v1', prueba.read_text(encoding='utf-8'))
        self.assertEqual(sorted(p.name for p in (self.raiz / 'docs').glob('*.md')), ['prueba.md'])
        self.assertEqual(sorted(p.name for p in self.ident.iterdir()), ['estilo.prueba.json', 'estilo.prueba.muestras'])
        self.correr('descartar')
        self.assertFalse(prueba.exists() or rojo.exists())
        self.assertEqual(list(self.ident.iterdir()), [])

    def test_la_lista_de_muestras_es_relativa_y_descartar_no_sale_del_proyecto(self):
        self.correr('partir', 'tinta')
        self.correr('muestras', str(self.doc))
        self.assertEqual((self.ident / 'estilo.prueba.muestras').read_text(encoding='utf-8'),
                         'docs/prueba.muestra-prueba.html\n')
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as fuera:
            ajeno = Path(fuera) / 'otro.muestra-prueba.html'
            ajeno.write_text('de otro proyecto', encoding='utf-8')
            with (self.ident / 'estilo.prueba.muestras').open('a', encoding='utf-8') as f:
                f.write(f'{ajeno}\n../{Path(fuera).name}/otro.muestra-prueba.html\n')
            self.correr('descartar')
            self.assertTrue(ajeno.is_file())
        self.assertFalse((self.raiz / 'docs' / 'prueba.muestra-prueba.html').exists())

    def test_el_documento_de_muestra_tiene_que_estar_en_el_proyecto(self):
        self.correr('partir', 'tinta')
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as fuera:
            doc = Path(fuera) / 'fuera.md'
            doc.write_text(MD, encoding='utf-8')
            self.assertIn('fuera del proyecto', self.correr('muestras', str(doc), ok=False))
            self.assertEqual(list(Path(fuera).iterdir()), [doc])

    def test_una_muestra_que_no_se_puede_rehacer_no_queda_la_anterior(self):
        self.correr('partir', 'tinta')
        self.correr('muestras', str(self.doc))
        muestra = self.raiz / 'docs' / 'prueba.muestra-prueba.html'
        self.assertTrue(muestra.is_file())
        self.correr('cambiar', 'colores.sobre-primario=#c0502a')
        salida = self.correr('muestras', str(self.doc))
        self.assertIn('se detiene', salida)
        self.assertIn('Borrada la muestra anterior', salida)
        self.assertFalse(muestra.exists())
        self.assertFalse((self.ident / 'estilo.prueba.muestras').exists())

    def test_el_generador_usa_el_estilo_aceptado(self):
        self.correr('partir', 'tinta')
        self.correr('aceptar', '--motivo', 'x')
        self.correr('cambiar', 'pagina.pie=oscuro')
        self.correr('aceptar', '--motivo', 'y')
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8',
                            str(SKILLS / 'crear_documentos' / 'scripts' / 'documento_a_html.py'), str(self.doc)],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('estilo v2', self.doc.with_suffix('.html').read_text(encoding='utf-8'))

    def test_un_primario_nuevo_recalcula_su_familia_en_claro_y_en_oscuro(self):
        from tema_identidad import contraste, mezclar
        self.correr('partir', 'tinta')
        salida = self.correr('cambiar', 'colores.primario=#F5C400', 'colores.sobre-primario=#1a1a1a')
        self.assertNotIn('No pasa el contraste', salida)
        c = self.leer('estilo.prueba.json')['colores']
        self.assertEqual(c['primario'], '#f5c400')
        self.assertEqual(c['primario-vivo'], mezclar('#f5c400', '#ffffff', .25))
        self.assertEqual(c['fondo'], mezclar('#f5c400', '#ffffff', .95))
        self.assertEqual(c['tenue'], mezclar('#f5c400', '#ffffff', .55))
        self.assertEqual(c['sobre-primario'], '#1a1a1a')  # lo pedido en el mismo cambio no se toca
        for fondo in (c['pagina'], '#ffffff', c['fondo']):  # un primario claro da un texto oscurecido que se lee
            self.assertGreaterEqual(contraste(c['primario-texto'], fondo), 4.5)
        self.assertEqual(c['acento'], c['primario-texto'])  # en tinta el acento era el primario: lo sigue
        self.assertEqual(c['acento-fondo'], mezclar(c['acento'], '#ffffff', .94))
        o = c['colores-oscuro']
        self.assertEqual(o['primario'], '#f5c400')
        self.assertEqual(o['acento'], '#f5c400')
        # En oscuro, el texto sobre el primario y el primario como texto también se derivan (347, 348)
        self.assertEqual(o['primario-texto'], '#f5c400')
        self.assertEqual(o['sobre-primario'], o['pagina'])  # la tinta de la página: el blanco no se lee sobre el amarillo
        self.assertGreaterEqual(contraste(o['sobre-primario'], o['primario']), 4.5)
        self.assertEqual(o['tinta-oscura'], '#f2f2f0')  # la tinta fuerte de tinta, clara en oscuro (349)
        # La cabecera destacada se recalcula con el primario, apagada y con su texto (351)
        self.assertNotEqual(c['cabecera'], '#a9401f')
        self.assertGreaterEqual(contraste(c['sobre-cabecera'], c['cabecera']), 4.5)
        self.assertNotEqual(o['cabecera'], '#66433c')
        self.assertGreaterEqual(contraste(o['sobre-cabecera'], o['cabecera']), 4.5)
        self.assertNotIn('#b8431c', json.dumps(c))  # nada de la familia terracota de tinta
        self.assertNotIn('#f08a59', json.dumps(c))

    def test_el_contraste_en_oscuro_se_avisa_como_en_claro(self):
        self.correr('partir', 'morado')
        self.assertIn('colores-oscuro', self.leer('estilo.prueba.json')['colores'])  # completa, derivada (348)
        salida = self.correr('cambiar', 'colores.colores-oscuro.primario=#3a1d5c')
        self.assertIn('No pasa el contraste: en oscuro, texto de los botones y las marcas sobre el primario', salida)

    def test_lo_pedido_en_el_mismo_cambio_y_un_acento_propio_se_conservan(self):
        self.correr('partir', 'teal', 'colores.primario=#c2410c', 'colores.tenue=#123456')
        c = self.leer('estilo.prueba.json')['colores']
        self.assertEqual(c['tenue'], '#123456')
        self.assertEqual(c['acento'], '#6d28d9')  # el acento de teal no era su primario
        from tema_identidad import contraste
        self.assertGreaterEqual(contraste(c['primario-texto'], c['fondo-medio']), 4.5)  # también en la decisión de las preguntas
        self.correr('cambiar', 'colores.primario=amarillo', ok=False)

    def test_cambiar_y_ver_enseñan_lo_cambiado_frente_al_tema_de_partida(self):
        self.correr('partir', 'tinta')
        self.correr('cambiar', 'pagina.pie=oscuro')
        salida = self.correr('cambiar', 'secciones.etiqueta=solida')
        este, todo = salida.split('Frente a tinta, todo lo cambiado:')
        self.assertIn('secciones.etiqueta: "solida"', este)
        self.assertNotIn('pagina.pie', este)
        self.assertIn('pagina.pie: "oscuro"', todo)
        self.assertIn('secciones.etiqueta: "solida"', todo)
        ver = self.correr('ver')
        self.assertIn('Frente a tinta, todo lo cambiado:', ver)
        self.assertIn('pagina.pie: "oscuro"', ver)
        self.correr('aceptar', '--motivo', 'x')
        self.correr('cambiar', 'pagina.esquinas=0')
        ver = self.correr('ver')
        self.assertIn('Frente al estilo del proyecto (v1):\n    pagina.esquinas: 0', ver)

    def test_parametros_enseña_el_catalogo(self):
        salida = self.correr('parametros')
        for linea in ('secciones', '  cabecera: numero-etiqueta | numero-titulo | titulo', 'diagramas', '  tema:'):
            self.assertIn(linea, salida)


if __name__ == '__main__':
    unittest.main()
