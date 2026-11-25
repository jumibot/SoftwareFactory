"""Pruebas del estilo del proyecto en el generador único (docs/identidad/estilo.json, decisiones 316 a 323):
lectura y validación de los diez grupos, «sin cambios con el valor por defecto», logo, aviso del aspecto en la cabecera
y conversor, roles del primario claro, contraste, forma de la cabecera de sección, versión en el pie, tema por defecto
sin estilo y enlace legible en la portada oscura.

python -I -X utf8 -m pytest plugins/sf/tests/test_estilo.py
"""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / 'skills'
SCRIPTS = SKILLS / 'crear_documentos' / 'scripts'
GENERADOR = SCRIPTS / 'documento_a_html.py'
CONVERSOR = SCRIPTS / 'convertir_cabecera.py'
TEMAS = SKILLS / 'crear_documentos' / 'assets' / 'temas'

MD = """---
destino: proyecto
herramientas: ninguna
{extra}---
# Prueba

## Uno | Primera {{#uno}}

Entrada con un [enlace](https://example.com).

## Segunda sin etiqueta

Texto.

```json
{{"clave": 1}}
```
"""


def estilo_morado(**grupos) -> dict:
    """Un estilo con los colores y la letra del tema morado: lo mismo que el tema por defecto sin estilo."""
    tema = json.loads((TEMAS / 'morado.json').read_text(encoding='utf-8'))
    estilo = {'version': 1, 'origen': 'morado', 'historial': [], 'colores': dict(tema['colores']),
              'letra': dict(tema['tipografias'])}
    for grupo, valores in grupos.items():
        estilo.setdefault(grupo, {}).update(valores)
    return estilo


def sin_procedencia(h: str) -> str:
    return re.sub(r'<p class="procedencia">.*?</p>', '', h)


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.raiz = Path(self._tmp.name)
        self.ident = self.raiz / 'docs' / 'identidad'
        self.ident.mkdir(parents=True)
        self.md = self.raiz / 'docs' / 'doc.md'

    def tearDown(self):
        self._tmp.cleanup()

    def escribir_estilo(self, estilo):
        (self.ident / 'estilo.json').write_text(json.dumps(estilo, ensure_ascii=False), encoding='utf-8')

    def generar(self, extra: str = '', ok: bool = True, args=(), md: str = None) -> str:
        self.md.write_text(md if md is not None else MD.format(extra=extra), encoding='utf-8')
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(GENERADOR), str(self.md), *args],
                           capture_output=True, text=True, encoding='utf-8')
        self.stderr = r.stderr
        if not ok:
            self.assertNotEqual(r.returncode, 0, r.stdout)
            return r.stderr + r.stdout
        self.assertEqual(r.returncode, 0, r.stderr)
        return self.md.with_suffix('.html').read_text(encoding='utf-8')


class SinEstilo(Base):
    def test_tema_por_defecto_y_un_aviso(self):
        h = self.generar()
        self.assertEqual(self.stderr.count('no tiene estilo'), 1)
        self.assertIn('«Morado»', self.stderr)
        self.assertIn('--primario: #7b2cbf', h)
        self.assertNotIn('data-estilo', h)
        self.assertNotIn('estilo v', h)

    def test_tema_por_el_color_de_sesion(self):
        (self.raiz / '.sf').mkdir()
        (self.raiz / '.sf' / 'proyecto.json').write_text('{"color": "red"}', encoding='utf-8')
        h = self.generar()
        self.assertIn('color de sesión del proyecto, red', self.stderr)
        self.assertIn('--primario: #c62a1f', h)  # rojo

    def test_tema_de_la_identidad_manda_sobre_el_color(self):
        (self.raiz / '.sf').mkdir()
        (self.raiz / '.sf' / 'proyecto.json').write_text('{"color": "red"}', encoding='utf-8')
        (self.ident / 'identidad.json').write_text('{"tema": "teal"}', encoding='utf-8')
        h = self.generar()
        self.assertIn('--primario: #00726b', h)
        self.assertIn("el de identidad.json", self.stderr)

    def test_contraste_del_tema_no_bloquea(self):
        self.generar()
        self.assertNotIn('«borde»', self.stderr)  # el borde de las cajas no avisa (335, 9)

    def test_portada_del_md_vale_y_avisa(self):
        h = self.generar('portada: oscura\n')
        self.assertIn('<header class="portada oscura">', h)
        self.assertIn('fija el aspecto («portada: oscura»)', self.stderr)
        self.assertIn('vale mientras el proyecto no tenga estilo.json', self.stderr)


class Catalogo(Base):
    def test_sin_cambios_con_el_valor_por_defecto(self):
        """Un estilo con los valores del tema por defecto da el mismo HTML que el tema sin estilo (salvo el pie)."""
        sin = self.generar()
        self.escribir_estilo(estilo_morado())
        con = self.generar()
        self.assertIn('estilo v1', con)
        self.assertEqual(sin_procedencia(sin), sin_procedencia(con))

    def test_valores_por_defecto_explicitos_no_cambian_nada(self):
        self.escribir_estilo(estilo_morado())
        base = self.generar()
        self.escribir_estilo(estilo_morado(
            letra={'tamano': 17, 'escala': 'editorial'}, portada={'forma': 'clara', 'fondo': 'oscuro', 'linea': 'si'},
            secciones={'cabecera': 'numero-etiqueta', 'etiqueta': 'tinte', 'opacidad': 1, 'marcador': 'flecha',
                       'plegado': 'primera'},
            pagina={'ancho': 1240, 'pie': 'claro'}, lectura={'menu': 'botones'},
            aparte={'escenario': 'derivado', 'hud': 'primario'}))
        self.assertEqual(sin_procedencia(base), sin_procedencia(self.generar()))
        self.escribir_estilo(estilo_morado(pagina={'codigo': 'bloque'}))
        self.assertEqual(sin_procedencia(base), sin_procedencia(self.generar()))

    def test_desconocidos_se_detienen_con_los_posibles(self):
        for estilo, texto in ((dict(estilo_morado(), raro={}), 'grupos desconocidos: raro'),
                              (estilo_morado(portada={'color': 'x'}), '«portada» no tiene color'),
                              (estilo_morado(portada={'forma': 'rara'}), 'Posibles: clara | oscura | compacta'),
                              (estilo_morado(pagina={'ancho': 3000}), 'entero de 980 a 1400'),
                              (estilo_morado(diagramas={'forma': 'rombo'}), 'redondeada | croqueta'),
                              (estilo_morado(colores={'magenta': '#ff00ff'}), '«colores» no tiene magenta')):
            with self.subTest(texto=texto):
                self.escribir_estilo(estilo)
                self.assertIn(texto, self.generar(ok=False))

    def test_version_y_primario_obligatorios(self):
        e = estilo_morado()
        del e['version']
        self.escribir_estilo(e)
        self.assertIn('falta «version»', self.generar(ok=False))
        e = estilo_morado()
        del e['colores']['primario']
        self.escribir_estilo(e)
        self.assertIn('falta «colores.primario»', self.generar(ok=False))

    def test_version_del_estilo_en_el_pie(self):
        e = estilo_morado()
        e['version'] = 3
        self.escribir_estilo(e)
        h = self.generar()
        self.assertRegex(h, r'<p class="procedencia">[^<]*· estilo v3</p>')

    def test_estilo_indicado_y_ninguno(self):
        otro = self.raiz / 'otro.json'
        otro.write_text(json.dumps(estilo_morado(colores={'primario': '#1d6fb6'})), encoding='utf-8')
        self.assertIn('--primario: #1d6fb6', self.generar(args=('--estilo', str(otro))))
        self.escribir_estilo(estilo_morado())
        self.assertNotIn('estilo v1', self.generar(args=('--estilo', 'ninguno')))

    def test_tema_ignorado_con_estilo(self):
        self.escribir_estilo(estilo_morado())
        h = self.generar(args=('--tema', 'rojo'))
        self.assertIn('--primario: #7b2cbf', h)
        self.assertIn('--tema rojo no se usa', self.stderr)


class Parametros(Base):
    def css(self, **grupos) -> str:
        self.escribir_estilo(estilo_morado(**grupos))
        h = self.generar()
        m = re.search(r'<style data-estilo="v1">(.*?)</style>', h, re.S)
        return m.group(1) if m else ''

    def test_cada_parametro_cambia_su_parte(self):
        casos = [({'letra': {'tamano': 18}}, 'font-size: 1.125rem'),
                 ({'letra': {'escala': 'compacta'}}, '.seccion h2 { font-size: 1.05rem'),
                 ({'letra': {'codigo': "'JetBrains Mono', monospace"}}, "code, pre, kbd, .formula { font-family: 'JetBrains Mono'"),
                 ({'portada': {'forma': 'compacta'}}, '.portada.compacta'),
                 ({'portada': {'forma': 'oscura', 'fondo': 'primario'}}, '.portada.oscura { background: var(--cabecera); color: var(--sobre-cabecera)'),
                 ({'secciones': {'etiqueta': 'solida', 'opacidad': 0.4}}, 'rgba(var(--primario-rgb), 0.4)'),
                 ({'secciones': {'etiqueta': 'solida'}}, '.seccion[open] > .seccion-titulo { margin-bottom: 1.1rem; }'),
                 ({'secciones': {'etiqueta': 'linea'}}, 'border-left: 4px solid var(--primario)'),
                 ({'secciones': {'etiqueta': 'ninguna'}}, 'color: var(--texto-suave)'),
                 ({'secciones': {'marcador': 'circulo'}}, 'border-radius: 50%'),
                 ({'secciones': {'marcador': 'ninguno'}}, '.seccion-titulo::after { display: none; }'),
                 ({'pagina': {'ancho': 1100}}, 'min(1100px, 100% - 32px)'),
                 ({'pagina': {'esquinas': 0}}, '--esquinas: 0px'),
                 ({'pagina': {'codigo': 'linea'}}, 'border-top: 1px solid var(--borde)'),
                 ({'pagina': {'pie': 'oscuro'}}, '.pie { background: var(--oscuro)'),
                 ({'pagina': {'filetes': 'no'}}, '.portada, .menu { border-bottom: 0; } .pie { border-top: 0; }'),
                 ({'recuadros': {'filete': 'no'}}, '.recuadro:not(.decision) { border-left: 0;')]
        for grupos, esperado in casos:
            with self.subTest(grupos=grupos):
                self.assertIn(esperado, self.css(**grupos))

    def test_filetes_por_defecto_no_cambian_nada(self):
        self.assertEqual(self.css(pagina={'filetes': 'si'}, recuadros={'filete': 'si'}), '')
        self.escribir_estilo(estilo_morado(recuadros={'filete': 'tal vez'}))
        self.assertIn('«recuadros.filete: "tal vez"» no vale. Posibles: si | no.', self.generar(ok=False))

    def test_portada_del_estilo_manda_sobre_el_md(self):
        self.escribir_estilo(estilo_morado(portada={'forma': 'oscura'}))
        h = self.generar()
        self.assertIn('<header class="portada oscura">', h)
        self.escribir_estilo(estilo_morado())
        h = self.generar('portada: oscura\n')
        self.assertIn('<header class="portada">', h)
        self.assertIn('se ignora: manda el estilo del proyecto', self.stderr)

    def test_linea_de_portada(self):
        self.escribir_estilo(estilo_morado(portada={'linea': 'no'}))
        self.assertNotIn('<hr class="portada-linea">', self.generar())

    def test_plegado(self):
        self.escribir_estilo(estilo_morado(secciones={'plegado': 'todas'}))
        self.assertEqual(self.generar().count('<details class="seccion" id="uno" open>'), 1)
        self.assertIn('id="segunda-sin-etiqueta" open>', self.generar())
        self.escribir_estilo(estilo_morado(secciones={'plegado': 'ninguna'}))
        self.assertNotRegex(self.generar(), r'<details class="seccion"[^>]*open>')

    def test_serie(self):
        self.escribir_estilo(estilo_morado(colores={'serie': ['#1f7a7a', '#a6501a']}))
        h = self.generar()
        self.assertIn('<details class="seccion bloque-1"', h)
        self.assertIn('<details class="seccion bloque-2"', h)

    def test_lectura_del_estilo_y_del_documento(self):
        self.escribir_estilo(estilo_morado(lectura={'destino': 'usuario', 'herramientas': 'buscador', 'menu': 'no'}))
        md = MD.replace('destino: proyecto\nherramientas: ninguna\n', '').format(extra='')
        h = self.generar(md=md)
        self.assertIn('data-destino="usuario" data-herramientas="buscador"', h)
        self.assertNotIn('<nav class="menu"', h)
        h = self.generar()  # el documento manda
        self.assertIn('data-destino="proyecto" data-herramientas="ninguna"', h)

    def test_producto_y_enlace(self):
        self.escribir_estilo(estilo_morado(identidad={'producto': 'Marca', 'enlace': 'https://github.com/x/y'}))
        h = self.generar()
        self.assertIn('<p>Marca · Documento</p>', h)
        self.assertIn('<p class="enlace-proyecto"><a href="https://github.com/x/y" class="externo" target="_blank"'
                      ' rel="noopener noreferrer">github.com/x/y</a></p>', h)

    def test_significado_en_las_tarjetas(self):
        self.escribir_estilo(estilo_morado(colores={'significado': {'correcto': '#0f5132'}}))
        md = MD.format(extra='') + '\n::: tarjetas 2\n\n#### Bien {color=correcto}\n\nSí.\n\n#### Mal {color=error}\n\nNo.\n\n:::\n'
        h = self.generar(md=md)
        self.assertIn('--c:#0f5132', h)
        self.assertIn('--c:#be185d', h)

    def test_diagramas_toman_los_valores_del_estilo(self):
        figura = ('<figure class="diagrama d-gen" id="f" data-diagrama data-d-forma="redondeada" data-d-tema="tinta">'
                  '<p>x</p></figure>')
        md = MD.format(extra='') + '\n' + figura + '\n'
        self.escribir_estilo(estilo_morado(diagramas={'forma': 'croqueta', 'recorrido': 'acento', 'tema': 'documento'}))
        h = self.generar(md=md)
        tag = re.search(r'<figure class="diagrama[^>]*>', h).group(0)
        self.assertIn('data-d-forma="croqueta"', tag)
        self.assertIn('data-d-recorrido="acento"', tag)
        self.assertNotIn('data-d-tema', tag)


class Cabecera(Base):
    def test_numero_etiqueta_y_306(self):
        h = self.generar()
        self.assertIn('<span class="etiqueta">01 / Uno</span><h2>Primera</h2>', h)
        # Sin etiqueta, número y título, sin antetítulo repetido (306).
        self.assertIn('<summary class="seccion-titulo sin-etiqueta"><h2><span class="seccion-numero">02</span> '
                      'Segunda sin etiqueta</h2></summary>', h)

    def test_numero_titulo_y_titulo(self):
        self.escribir_estilo(estilo_morado(secciones={'cabecera': 'numero-titulo'}))
        h = self.generar()
        self.assertIn('<h2><span class="seccion-numero">01</span> Primera</h2>', h)
        self.assertNotIn('class="etiqueta"', h.split('<main')[1])
        self.escribir_estilo(estilo_morado(secciones={'cabecera': 'titulo'}))
        h = self.generar()
        self.assertIn('<summary class="seccion-titulo sin-etiqueta"><h2>Primera</h2></summary>', h)


class Colores(Base):
    def test_roles_derivados(self):
        self.escribir_estilo(estilo_morado())
        h = self.generar()
        self.assertIn('--sobre-primario: #ffffff;', h)
        self.assertIn('--primario-texto: #7b2cbf;', h)

    def test_primario_claro_se_detiene_sin_primario_texto(self):
        e = estilo_morado()
        e['colores'] = {'primario': '#f2c230', 'oscuro': '#3a2e00', 'tenue': '#f2c230', 'texto-suave': '#5c5c60'}
        self.escribir_estilo(e)
        salida = self.generar(ok=False)
        self.assertIn('Contraste insuficiente', salida)
        self.assertIn('«primario-texto» #f2c230', salida)
        e['colores']['primario-texto'] = '#6b5200'
        self.escribir_estilo(e)
        h = self.generar()
        self.assertIn('--sobre-primario: #2b2b2f;', h)  # el texto oscuro: más contraste que el blanco sobre el amarillo
        self.assertIn('--primario-texto: #6b5200;', h)

    def test_titulo_grande_pide_3_a_1(self):
        e = estilo_morado(secciones={'etiqueta': 'solida', 'opacidad': 0.75})
        e['colores'] = {'primario': '#2f6fc0', 'oscuro': '#1d3a66', 'tenue': '#a9c4ee', 'texto-suave': '#5c5c60'}
        self.escribir_estilo(e)
        salida = self.generar(ok=False)
        self.assertIn('número y etiqueta de la cabecera de sección sólida', salida)
        self.assertNotIn('título de la cabecera de sección sólida', salida)

    def test_bordes_solo_avisan(self):
        self.escribir_estilo(estilo_morado())
        self.generar()
        self.assertNotIn('bordes y líneas con poco contraste', self.stderr)  # campos derivados a 3:1, cajas fuera
        self.escribir_estilo(estilo_morado(colores={'primario': '#7b2cbf', 'borde-campo': '#eeeeee'}))
        self.generar()
        self.assertIn('bordes de los campos: «borde-campo» #eeeeee', self.stderr)


class Logo(Base):
    def test_logo_svg_del_estilo(self):
        (self.ident / 'logo.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50">'
                                             '<rect width="200" height="50"/></svg>', encoding='utf-8')
        self.escribir_estilo(estilo_morado(identidad={'logo': ['logo.svg']}))
        h = self.generar()
        self.assertIn('<img src="data:image/svg+xml;base64,', h)
        self.assertIn('width="160" height="40">', h)

    def test_en_la_cabecera_destacada_el_logo_va_con_su_texto(self):
        """Con portada destacada (fondo primario) y una cabecera de texto oscuro en claro y claro en oscuro, el logo
        claro va en el modo claro y el oscuro en el oscuro (351)."""
        (self.ident / 'logo.svg').write_text('<svg viewBox="0 0 40 40"><rect fill="#111111"/></svg>', encoding='utf-8')
        (self.ident / 'logo-oscuro.svg').write_text('<svg viewBox="0 0 40 40"><rect fill="#eeeeee"/></svg>',
                                                    encoding='utf-8')
        sys.path.insert(0, str(SKILLS / 'fijar_estilo' / 'scripts'))
        import estilo as herramienta
        estilo = herramienta.aplicar_cambios(herramienta.resolver_tema('tinta', self.ident), [
            'colores.primario=#f5c400', 'colores.sobre-primario=#1a1a1a', 'portada.forma=oscura',
            'portada.fondo=primario', 'identidad.logo=["logo.svg"]', 'identidad.logo-oscuro=logo-oscuro.svg'])
        self.escribir_estilo(estilo)
        h = self.generar()
        marca = re.search(r'<p class="marca">(.*?)</p>', h, re.S).group(1)
        imgs = re.findall(r'<img class="(logo-claro|logo-oscuro)" src="data:image/svg\+xml;base64,([^"]+)"', marca)
        import base64
        contenido = {clase: base64.b64decode(datos).decode() for clase, datos in imgs}
        self.assertIn('#111111', contenido['logo-claro'])  # cabecera clara (texto oscuro): el logo de letras oscuras
        self.assertIn('#eeeeee', contenido['logo-oscuro'])  # en oscuro, la cabecera es oscura: el logo claro

    def test_logo_que_falta_se_detiene(self):
        self.escribir_estilo(estilo_morado(identidad={'logo': 'no-esta.svg'}))
        self.assertIn('No encuentro el logo «no-esta.svg»', self.generar(ok=False))

    def test_placa_en_la_portada_oscura(self):
        (self.ident / 'logo.svg').write_text('<svg viewBox="0 0 40 40"></svg>', encoding='utf-8')
        self.escribir_estilo(estilo_morado(identidad={'logo': 'logo.svg', 'logo-oscuro': 'placa'},
                                           portada={'forma': 'oscura'}))
        self.assertIn('<img class="placa" src="data:image/svg+xml', self.generar())


class Arreglos(Base):
    def test_enlace_legible_en_la_portada_oscura(self):
        h = self.generar('portada: oscura\n')
        self.assertIn('.portada.oscura a { color: #fff;', h)

    def test_codigo_en_bloque_y_coloreado(self):
        h = self.generar()
        self.assertIn('<pre><code class="language-json">{<span class="sx-p">"clave"</span>', h)
        self.assertIn('pre { background: var(--fondo-suave); border-left: 3px solid var(--primario);', h)


TEMAS_DEL_CATALOGO = ('colorido', 'morado', 'pool', 'rojo', 'teal', 'tinta')


def abrir_navegador(pw):
    for canal in (None, 'chrome', 'msedge'):
        try:
            return pw.chromium.launch(channel=canal) if canal else pw.chromium.launch()
        except Exception:  # noqa: BLE001 — se prueba el siguiente
            continue
    return None


def navegador_disponible() -> bool:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            nav = abrir_navegador(pw)
            if nav:
                nav.close()
                return True
    except BaseException:  # noqa: BLE001 — sin Playwright, se salta
        pass
    return False


class ModoOscuro(Base):
    """El modo oscuro de «Lectura» aplica la paleta oscura del estilo (decisiones 347 a 350)."""

    def setUp(self):
        super().setUp()
        sys.path.insert(0, str(SCRIPTS))
        import estilo_proyecto
        import tema_identidad
        self.ep, self.ti = estilo_proyecto, tema_identidad

    def test_los_seis_temas_tienen_paleta_oscura_completa_y_legible(self):
        for nombre in TEMAS_DEL_CATALOGO:
            with self.subTest(nombre):
                tema = self.ti.cargar_tema(nombre)
                o = tema['colores-oscuro']
                self.assertEqual(set(o), self.ti.ROLES_VALIDOS)
                self.assertLess(self.ti.luminancia(o['pagina']), .05)
                self.assertGreater(self.ti.luminancia(o['tinta-oscura']), .3)  # la tinta fuerte, clara (349)
                self.assertGreaterEqual(self.ti.contraste('#ffffff', o['oscuro']), 4.5)  # la superficie, oscura
                errores, _ = self.ep.comprobar_contraste(tema, None)
                self.assertEqual([e for e in errores if e.startswith('en oscuro')], [])

    def test_los_temas_que_pasan_en_claro_siguen_pasando(self):
        for nombre in ('colorido', 'morado', 'rojo', 'teal', 'tinta'):
            with self.subTest(nombre):
                self.assertEqual(self.ep.comprobar_contraste(self.ti.cargar_tema(nombre), None)[0], [])

    def test_una_paleta_oscura_dada_se_respeta_y_se_completa(self):
        tema = self.ti.normalizar_tema({'colores': {'primario': '#7b2cbf'},
                                        'colores-oscuro': {'primario': '#c9a3ff', 'pagina': '#101010'}}, 'prueba')
        o = tema['colores-oscuro']
        self.assertEqual((o['primario'], o['pagina']), ('#c9a3ff', '#101010'))
        self.assertEqual(o['sobre-primario'], '#101010')  # la tinta de la página, más contraste que el blanco

    def test_paleta_oscura_antigua_con_oscuro_claro_pasa_a_tinta(self):
        o = self.ti.derivar_oscuro(self.ti.cargar_tema('morado')['colores'], {'oscuro': '#f2f2f0'})
        self.assertEqual(o['tinta-oscura'], '#f2f2f0')
        self.assertLess(self.ti.luminancia(o['oscuro']), .1)

    def test_el_contraste_en_oscuro_detiene_el_generador(self):
        e = estilo_morado()
        e['colores']['colores-oscuro'] = {'primario': '#3a1d5c'}  # un primario oscuro sobre la página oscura
        self.escribir_estilo(e)
        salida = self.generar(ok=False)
        self.assertIn('en oscuro, enlaces y rótulos sobre la página', salida)

    def test_el_documento_no_invierte_y_lleva_la_paleta_oscura(self):
        self.escribir_estilo(estilo_morado())
        h = self.generar()
        self.assertNotIn('invert(', h)
        self.assertIn('@media screen {', h)
        self.assertRegex(h, r':root\[data-theme="dark"\] \{ --primario: #[0-9a-f]{6};[^}]*--sobre-primario: #')
        self.assertIn('--tinta-oscura: #4c1d80;', h)
        self.assertIn('--superficie: #ffffff;', h)
        self.assertIn('--sx-cadena:', h)

    def test_tarjetas_con_color_llevan_su_tono_oscuro(self):
        self.escribir_estilo(estilo_morado())
        md = MD.format(extra='') + ('\n::: tarjetas 2\n#### Bien {color=correcto}\n\nCampo\n:   valor\n\n'
                                    '#### Mal {color=error}\n\nTexto.\n:::\n')
        self.assertIn('--c-oscuro-o:', self.generar(md=md))

    def test_logo_de_la_portada_clara_cambia_en_oscuro(self):
        (self.ident / 'logo.svg').write_text('<svg viewBox="0 0 40 40"></svg>', encoding='utf-8')
        self.escribir_estilo(estilo_morado(identidad={'logo': 'logo.svg', 'logo-oscuro': 'placa'}))
        h = self.generar()
        self.assertIn('<img class="logo-claro" src=', h)
        self.assertIn('<img class="placa logo-oscuro" src=', h)

    @unittest.skipUnless(navegador_disponible(), 'sin Playwright o sin navegador')
    def test_en_el_navegador_el_boton_toma_el_primario_oscuro(self):
        """Con un primario amarillo y texto oscuro, en oscuro el botón es el amarillo con texto legible."""
        from playwright.sync_api import sync_playwright
        sys.path.insert(0, str(SKILLS / 'fijar_estilo' / 'scripts'))
        import estilo as herramienta
        estilo = herramienta.resolver_tema('tinta', self.ident)
        estilo = herramienta.aplicar_cambios(estilo, ['colores.primario=#f5c400', 'colores.sobre-primario=#1a1a1a'])
        self.escribir_estilo(estilo)
        self.generar()
        html = self.md.with_suffix('.html')
        o = estilo['colores']['colores-oscuro']
        rgb = lambda x: 'rgb(' + ', '.join(str(int(x[i:i + 2], 16)) for i in (1, 3, 5)) + ')'
        with sync_playwright() as pw:
            nav = abrir_navegador(pw)
            try:
                p = nav.new_page()
                p.goto(html.resolve().as_uri())
                p.evaluate("document.documentElement.dataset.modo = 'oscuro'; "
                           "document.documentElement.dataset.theme = 'dark'")
                p.wait_for_timeout(300)
                medido = p.evaluate("""() => { const b = getComputedStyle(document.querySelector('.imprimir'));
                    return {filtro: getComputedStyle(document.documentElement).filter,
                            pagina: getComputedStyle(document.body).backgroundColor,
                            boton: b.backgroundColor, texto: b.color}; }""")
            finally:
                nav.close()
        self.assertEqual(medido['filtro'], 'none')
        self.assertEqual(medido['pagina'], rgb(o['pagina']))
        self.assertEqual(medido['boton'], rgb(o['primario']))
        self.assertEqual(medido['texto'], rgb(o['sobre-primario']))
        self.assertEqual(o['primario'], '#f5c400')
        self.assertGreaterEqual(self.ti.contraste(o['primario'], o['sobre-primario']), 4.5)


class ColorDeCabecera(Base):
    """La portada destacada usa «cabecera», un tono del primario menos brillante, en claro y en oscuro (351)."""

    def setUp(self):
        super().setUp()
        sys.path.insert(0, str(SCRIPTS))
        import tema_identidad
        self.ti = tema_identidad

    def test_los_seis_temas_la_derivan_menos_brillante_y_legible(self):
        for nombre in TEMAS_DEL_CATALOGO:
            for modo in ('colores', 'colores-oscuro'):
                with self.subTest(nombre, modo=modo):
                    tema = self.ti.cargar_tema(nombre)
                    c = tema['colores'] if modo == 'colores' else tema['colores-oscuro']
                    self.assertGreaterEqual(self.ti.contraste(c['sobre-cabecera'], c['cabecera']), 4.5)
                    if modo == 'colores':
                        self.assertLessEqual(self.ti.luminancia(c['cabecera']), self.ti.LUMINANCIA_CABECERA)
                    else:  # profunda: más oscura que el primario oscuro, sin deslumbrar sobre la página
                        self.assertLess(self.ti.luminancia(c['cabecera']), self.ti.luminancia(c['primario']))

    def test_un_amarillo_da_una_cabecera_apagada(self):
        tema = self.ti.normalizar_tema({'colores': {'primario': '#f5c400', 'texto': '#25283a'}}, 'amarillo')
        self.assertLessEqual(self.ti.luminancia(tema['colores']['cabecera']), .3)
        self.assertLess(self.ti.luminancia(tema['colores-oscuro']['cabecera']), .15)

    def test_la_portada_con_fondo_primario_la_usa(self):
        self.escribir_estilo(estilo_morado(portada={'forma': 'oscura', 'fondo': 'primario'}))
        h = self.generar()
        self.assertIn('.portada.oscura { background: var(--cabecera); color: var(--sobre-cabecera)', h)
        self.assertRegex(h, r'--cabecera: #[0-9a-f]{6}')

    def test_su_texto_sin_contraste_detiene_el_generador(self):
        self.escribir_estilo(estilo_morado(colores={'primario': '#7b2cbf', 'cabecera': '#7b2cbf',
                                                    'sobre-cabecera': '#8a3cd0'}))
        self.assertIn('texto de la portada destacada con el color del proyecto', self.generar(ok=False))


class ContrasteDeLosTemas(Base):
    """Ningún tema del catálogo detiene el generador por contraste, ni en claro ni en oscuro (392)."""

    def test_todos_pasan_en_claro_y_en_oscuro(self):
        sys.path.insert(0, str(SCRIPTS))
        import estilo_proyecto as ep
        import tema_identidad as ti
        for nombre in sorted(p.stem for p in TEMAS.glob('*.json')):
            with self.subTest(nombre):
                errores, _ = ep.comprobar_contraste(ti.cargar_tema(nombre), None)
                self.assertEqual(errores, [])


class ListasDeMuchasCifras(Base):
    """Una lista numerada reserva el ancho de su número más largo, sin límite de cifras (425)."""

    def lista(self, n: int) -> str:
        items = "\n".join(f"{i}. Elemento {i} con un texto que ocupa la línea." for i in range(1, n + 1))
        return MD.format(extra='').replace('Entrada con un', items + '\n\nEntrada con un', 1)

    def test_el_generador_pone_las_cifras_del_numero_mas_largo(self):
        self.assertNotIn('style="--cifras', self.generar(md=self.lista(99)))  # dos cifras: la regla por defecto
        self.assertIn('<ol style="--cifras: 3">', self.generar(md=self.lista(100)))
        self.assertIn('<ol style="--cifras: 4">', self.generar(md=self.lista(1000)))
        self.assertIn('<ol style="--cifras: 5">', self.generar(md=self.lista(10000)))

    @unittest.skipUnless(navegador_disponible(), 'sin Playwright o sin navegador')
    def test_en_el_navegador_el_numero_no_se_monta_en_el_texto(self):
        from playwright.sync_api import sync_playwright
        for n in (1000, 10000):
            self.generar(md=self.lista(n))
            html = self.md.with_suffix('.html').resolve().as_uri()
            with sync_playwright() as pw:
                nav = abrir_navegador(pw)
                try:
                    for ancho in (1280, 375):
                        with self.subTest(n=n, ancho=ancho):
                            p = nav.new_page(viewport={'width': ancho, 'height': 800})
                            p.goto(html)
                            m = p.evaluate("""() => { const li = document.querySelector('.seccion ol > li:last-child');
                                const antes = getComputedStyle(li, '::before');
                                return {numero: parseFloat(antes.width), sangria: parseFloat(getComputedStyle(li).paddingLeft),
                                        alto: parseFloat(antes.height), linea: parseFloat(antes.lineHeight)}; }""")
                            p.close()
                            self.assertLess(m['numero'], m['sangria'])  # el número cabe en la sangría
                            self.assertLess(m['alto'], m['linea'] * 1.5)  # en una sola línea, sin apilar
                finally:
                    nav.close()


class PrimarioLinea(Base):
    """Las líneas y bordes de los diagramas en el color del proyecto llegan a 3:1 con un primario claro (335, 8)."""

    def test_un_amarillo_da_lineas_de_3_a_1_en_claro_y_en_oscuro(self):
        sys.path.insert(0, str(SCRIPTS))
        import tema_identidad as ti
        tema = ti.normalizar_tema({'colores': {'primario': '#f5c400', 'texto': '#25283a'}}, 'amarillo')
        for modo in ('colores', 'colores-oscuro'):
            c = tema[modo]
            for fondo in ('pagina', 'superficie'):
                with self.subTest(modo=modo, fondo=fondo):
                    self.assertGreaterEqual(ti.contraste(c['primario-linea'], c[fondo]), 3)
        self.assertNotEqual(tema['colores']['primario-linea'], '#f5c400')  # el amarillo tal cual no llega

    def test_los_diagramas_usan_el_rol(self):
        css = (SKILLS / 'diagramas' / 'assets' / 'diagramas.css').read_text(encoding='utf-8')
        self.assertNotRegex(css, r'(?<!, )var\(--primario, #00726b\)')  # siempre dentro de primario-linea o -texto
        self.assertIn('.d-gen .d-fl.d-principal { stroke: var(--primario-linea, var(--primario, #00726b)); }', css)


class MarcaElegida(Base):
    """La marca «Elegida» de una pregunta decidida se lee con un primario claro, en claro y en oscuro (427)."""

    @unittest.skipUnless(navegador_disponible(), 'sin Playwright o sin navegador')
    def test_con_el_amarillo_se_lee_en_claro_y_en_oscuro(self):
        from playwright.sync_api import sync_playwright
        sys.path.insert(0, str(SKILLS / 'fijar_estilo' / 'scripts'))
        sys.path.insert(0, str(SCRIPTS))
        import estilo as herramienta
        import tema_identidad as ti
        estilo = herramienta.aplicar_cambios(herramienta.resolver_tema('tinta', self.ident),
                                             ['colores.primario=#f5c400', 'colores.sobre-primario=#1a1a1a'])
        self.escribir_estilo(estilo)
        md = MD.format(extra='').replace('Entrada con un', """::: preguntas 1

### ¿Cuál? {recomendada=A estado=decidida elegida=B}

Opción A
:   Una.

Opción B
:   Otra.

Recomendación
:   La A.

Decisión
:   La B.

:::

Entrada con un""", 1)
        self.generar(md=md)
        html = self.md.with_suffix('.html').resolve().as_uri()
        hexa = lambda rgb: '#' + ''.join(f'{int(x):02x}' for x in rgb[rgb.index('(') + 1:rgb.index(')')].split(',')[:3])
        with sync_playwright() as pw:
            nav = abrir_navegador(pw)
            try:
                for modo in ('claro', 'oscuro'):
                    p = nav.new_page()
                    p.goto(html)
                    if modo == 'oscuro':
                        p.evaluate("document.documentElement.dataset.modo = 'oscuro'; "
                                   "document.documentElement.dataset.theme = 'dark'")
                    m = p.evaluate("""() => { const e = getComputedStyle(document.querySelector('.marca-opcion.elegida'));
                        return [e.color, e.backgroundColor]; }""")
                    p.close()
                    with self.subTest(modo):
                        self.assertGreaterEqual(ti.contraste(hexa(m[0]), hexa(m[1])), 4.5)
            finally:
                nav.close()


class TarjetasPlegables(Base):
    """Las tarjetas con cabecera de color se pliegan con un clic o con el teclado y se imprimen abiertas (427)."""

    @unittest.skipUnless(navegador_disponible(), 'sin Playwright o sin navegador')
    def test_clic_teclado_e_impresion(self):
        from playwright.sync_api import sync_playwright
        md = MD.format(extra='').replace('Entrada con un', """::: tarjetas 2 plegables

### Qué es {color=turquesa icono=documento}

Para quién
:   El equipo.

### Estado {color=naranja icono=check}

Fecha
:   Hoy.

:::

Entrada con un""", 1)
        self.generar(md=md)
        html = self.md.with_suffix('.html').resolve().as_uri()
        abierta = "document.querySelector('details.tarjeta.con-color').open"
        with sync_playwright() as pw:
            nav = abrir_navegador(pw)
            try:
                p = nav.new_page(viewport={'width': 1280, 'height': 900})
                p.goto(html)
                self.assertTrue(p.evaluate(abierta))  # abiertas en pantalla ancha
                p.click('details.tarjeta.con-color > summary')
                self.assertFalse(p.evaluate(abierta))  # la cabecera la pliega
                p.focus('details.tarjeta.con-color > summary')
                p.keyboard.press('Enter')
                self.assertTrue(p.evaluate(abierta))  # y el teclado la abre
                p.click('details.tarjeta.con-color > summary')
                p.evaluate("window.dispatchEvent(new Event('beforeprint'))")
                self.assertTrue(p.evaluate(abierta))  # al imprimir, abierta
                p.close()
            finally:
                nav.close()


class SerieEnOscuro(Base):
    """En oscuro, cada bloque de la serie redefine también los neutros: tinta, superficies de tabla y líneas (392)."""

    def test_los_bloques_no_se_quedan_con_los_neutros_claros(self):
        sys.path.insert(0, str(SCRIPTS))
        import tema_identidad as ti
        tema = ti.cargar_tema('colorido')
        o = tema['colores-oscuro']
        css = ti.variables_css(tema)
        regla = re.search(r':root\[data-theme="dark"\] \.bloque-1 \{([^}]*)\}', css).group(1)
        for rol in ('tinta-oscura', 'oscuro', 'fondo-suave', 'fondo-medio', 'linea'):
            with self.subTest(rol):
                self.assertIn(f'--{rol}: {o[rol]};', regla)

    def test_el_catalogo_puede_generar_un_tema_sin_contraste_avisando(self):
        estilo = estilo_morado(colores={'primario': '#7b2cbf', 'acento': '#d9a441'})
        self.escribir_estilo(estilo)
        self.generar(ok=False)
        h = self.generar(args=['--contraste-avisa'])
        self.assertIn('<html', h)


class Conversor(Base):
    def convertir(self, texto: str, *args):
        self.md.write_text(texto, encoding='utf-8')
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(CONVERSOR), str(self.md), *args],
                           capture_output=True, text=True, encoding='utf-8')
        return r, self.md.read_text(encoding='utf-8')

    def test_quita_el_aspecto_y_pasa_los_comentarios(self):
        r, texto = self.convertir('---\nversion: 1\nportada: oscura\nmenu: secciones\n---\n'
                                  '<!-- destino: usuario -->\n<!-- herramientas: buscador -->\n# Título\n\nTexto.\n')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(texto, '---\nversion: 1\nmenu: secciones\ndestino: usuario\nherramientas: buscador\n---\n'
                                '# Título\n\nTexto.\n')
        self.assertIn('quitada «portada: oscura»', r.stdout)

    def test_sin_cabecera_y_comprobar(self):
        original = '<!-- destino: proyecto -->\n# Título\n'
        r, texto = self.convertir(original, '--comprobar')
        self.assertEqual(r.returncode, 1)
        self.assertEqual(texto, original)
        r, texto = self.convertir(original)
        self.assertEqual(texto, '---\ndestino: proyecto\n---\n# Título\n')
        r, _ = self.convertir(texto)
        self.assertIn('ya está al día', r.stdout)


class FallosDeLaComprobacion(Base):
    """Lo que encontró comprobar_documento.py (437): el rol de cada color según su uso, el tipo de documento en la
    portada oscura y los colores de la serie en oscuro."""

    def setUp(self):
        super().setUp()
        sys.path.insert(0, str(SCRIPTS))
        import tema_identidad
        self.ti = tema_identidad

    def test_un_color_de_texto_toma_el_rol_legible_y_un_trazo_el_de_las_lineas(self):
        h = self.ti.colores_a_variables(
            '<p style="color:#00726b">a</p><p style="color:var(--primario)">b</p><svg><text fill="#004d47">c</text>'
            '<text fill="#888">d</text><path stroke="#00726b"/><rect fill="#00726b" stroke="#004d47"/></svg>'
            '<div style="border-top:4px solid #00726b;--oscuro:#134c4c">e</div>')
        self.assertIn('<p style="color:var(--primario-texto)">a', h)
        self.assertIn('<p style="color:var(--primario-texto)">b', h)
        self.assertIn('<text style="fill: var(--tinta-oscura)">c', h)
        self.assertIn('<text style="fill: var(--texto-suave)">d', h)
        self.assertIn('<path style="stroke: var(--primario-linea)"/>', h)
        self.assertIn('<rect style="fill: var(--primario); stroke: var(--oscuro)"/>', h)  # rellenos: su rol
        self.assertIn('border-top:4px solid var(--primario);--oscuro:#134c4c', h)

    def test_el_tipo_de_documento_no_va_en_el_primario_sobre_la_portada_oscura(self):
        css = (SKILLS / 'crear_documentos' / 'assets' / 'estilo_documento.css').read_text(encoding='utf-8')
        self.assertIn('@media screen { .oscura .tipo-doc { color: var(--tenue); } }', css)
        self.assertIn(':is(.oscura .marca, .oscura .tipo-doc,', css)
        self.escribir_estilo(estilo_morado(portada={'forma': 'oscura', 'fondo': 'primario'}))
        self.assertIn('.portada.oscura .tipo-doc,', self.generar())

    def test_en_la_portada_oscura_va_el_logo_para_fondo_oscuro(self):
        css = (SKILLS / 'crear_documentos' / 'assets' / 'estilo_documento.css').read_text(encoding='utf-8')
        self.assertIn('.portada.oscura .marca img.logo-claro:has(+ img.logo-oscuro) { display: none; }', css)
        self.assertIn('.portada.oscura .marca img.logo-oscuro { display: inline; }', css)

    def test_en_oscuro_cada_color_de_la_serie_se_lee_sobre_su_fondo_y_en_las_decisiones(self):
        for nombre in sorted(p.stem for p in TEMAS.glob('*.json')):
            tema = self.ti.cargar_tema(nombre)
            o = tema['colores-oscuro']
            for s in tema.get('serie', []):
                t = self.ti.tonos_serie_oscuro(s, o)
                for fondo in (t['fondo'], o['oscuro'], o['pagina'], o['superficie']):
                    with self.subTest(nombre, serie=s, fondo=fondo):
                        self.assertGreaterEqual(self.ti.contraste(t['primario'], fondo), 4.5)


if __name__ == '__main__':
    unittest.main()
