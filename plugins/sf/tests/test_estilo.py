"""Pruebas del estilo del proyecto en el generador único (docs/identidad/estilo.json, decisiones 316 a 323):
lectura y validación de los nueve grupos, «sin cambios con el valor por defecto», logo, aviso del aspecto en la cabecera
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
        self.assertIn('Contraste del tema', self.stderr)
        self.assertIn('«borde»', self.stderr)

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
                 ({'portada': {'forma': 'oscura', 'fondo': 'primario'}}, '.portada.oscura { background: var(--primario)'),
                 ({'secciones': {'etiqueta': 'solida', 'opacidad': 0.4}}, 'rgba(var(--primario-rgb), 0.4)'),
                 ({'secciones': {'etiqueta': 'linea'}}, 'border-left: 4px solid var(--primario)'),
                 ({'secciones': {'etiqueta': 'ninguna'}}, 'color: var(--texto-suave)'),
                 ({'secciones': {'marcador': 'circulo'}}, 'border-radius: 50%'),
                 ({'secciones': {'marcador': 'ninguno'}}, '.seccion-titulo::after { display: none; }'),
                 ({'pagina': {'ancho': 1100}}, 'min(1100px, 100% - 32px)'),
                 ({'pagina': {'esquinas': 0}}, '--esquinas: 0px'),
                 ({'pagina': {'codigo': 'linea'}}, 'border-top: 1px solid var(--borde)'),
                 ({'pagina': {'pie': 'oscuro'}}, '.pie { background: var(--oscuro)')]
        for grupos, esperado in casos:
            with self.subTest(grupos=grupos):
                self.assertIn(esperado, self.css(**grupos))

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
        self.assertIn('bordes y líneas con poco contraste', self.stderr)


class Logo(Base):
    def test_logo_svg_del_estilo(self):
        (self.ident / 'logo.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50">'
                                             '<rect width="200" height="50"/></svg>', encoding='utf-8')
        self.escribir_estilo(estilo_morado(identidad={'logo': ['logo.svg']}))
        h = self.generar()
        self.assertIn('<img src="data:image/svg+xml;base64,', h)
        self.assertIn('width="160" height="40">', h)

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


if __name__ == '__main__':
    unittest.main()
