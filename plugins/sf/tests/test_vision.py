"""Pruebas del generador de la visión (doc_to_html.py, el generador único con el perfil de la visión) y del lector de
libros, recurso común de crear_documentos (assets/lector.css y lector.js): la página de libro y el lector que pagina
(.lector), con su estilo y su script solo cuando el documento lo usa.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GENERADOR = Path(__file__).resolve().parents[1] / 'skills' / 'documento_vision' / 'scripts' / 'doc_to_html.py'

LECTOR = '''<div class="lector" data-titulo="Historia · prólogo">
<div class="libro">
<p class="libro-capitulo">Prólogo</p>
<p class="libro-titulo">Un lunes</p>
<p>Primer párrafo.</p>
<p class="libro-ornamento"></p>
<p>Segundo párrafo.</p>
</div>
</div>
'''


class Lector(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.md = Path(self._tmp.name) / 'vision.md'

    def tearDown(self):
        self._tmp.cleanup()

    def generar(self, cuerpo: str) -> str:
        self.md.write_text('<!-- destino: proyecto -->\n<!-- herramientas: ninguna -->\n# Prueba\n\n' + cuerpo + '\n## Uno\n\nTexto.\n', encoding='utf-8')
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(GENERADOR), str(self.md), '--identidad', 'ninguna',
                            '--logo', 'ninguno'], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        return self.md.with_suffix('.html').read_text(encoding='utf-8')

    def test_con_lector_lleva_su_estilo_y_su_script(self):
        h = self.generar(LECTOR)
        self.assertIn('<div class="lector" data-titulo="Historia · prólogo">', h)
        self.assertIn('<p class="libro-titulo">Un lunes</p>', h)
        self.assertIn('.lector.paginado .libro-flujo', h)
        self.assertIn('Leer la historia completa', h)
        self.assertIn('aria-label="Página siguiente"', h)

    def test_marca_con_la_barra_clara(self):
        # Como el logo «/SF» (decisión 255): lo que va delante de las letras, en el morado claro; las letras, en el de la marca.
        h = self.generar(LECTOR)
        self.assertIn('.lector-portada-logo b { color: var(--lector-marca, #161616); }', h)
        self.assertIn('.lector-marca b { color: var(--lector-marca, #b8b8bd);', h)
        self.assertIn('cursor: pointer; color: var(--lector-marca-claro, #161616); }', h)

    def test_sin_lector_no_lleva_script(self):
        h = self.generar('<div class="caso">\n<p class="caso-etiqueta">El caso · prólogo</p>\n<p>Texto.</p>\n</div>\n')
        self.assertNotIn('Leer la historia completa', h)
        self.assertNotIn('lector.js', h)  # el recurso del lector solo entra si el documento lo usa
        self.assertNotIn('lector.css', h)


class LectorComun(unittest.TestCase):
    """El lector es un recurso común: el generador de crear_documentos lo inyecta en cualquier tipo de documento."""

    def test_generador_comun_con_lector(self):
        comun = Path(__file__).resolve().parents[1] / 'skills' / 'crear_documentos' / 'scripts' / 'documento_a_html.py'
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
            md = Path(d) / 'doc.md'
            md.write_text('---\ndestino: proyecto\nherramientas: ninguna\n---\n# Prueba\n\n## Uno | Uno | Uno {#uno}\n\n'
                          + LECTOR + '\nTexto.\n', encoding='utf-8')
            r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(comun), str(md), '--identidad', 'ninguna',
                                '--logo', 'ninguno'], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stderr)
            h = md.with_suffix('.html').read_text(encoding='utf-8')
        self.assertIn('data-kit="skills/crear_documentos/assets/lector.css"', h)
        self.assertIn('data-kit="skills/crear_documentos/assets/lector.js"', h)
        self.assertIn('<div class="lector" data-titulo="Historia · prólogo">', h)


VISION = """<!-- destino: proyecto -->
<!-- herramientas: ninguna -->
# Prueba: una visión

**Estado:** hoy.

## 1.2 Instalación del plugin

Entrada con «<tarea> (N)» suelto.

### Qué es

Texto de la subsección.

#### Detalle

Detalle plegado.

### Qué es

Otra con el mismo título.

<div class="escena" role="note">
<p class="escena-etiqueta">Escena</p>
<div class="turno"><p class="ponente">Ana</p><p>Hola.</p></div>
</div>

<svg viewBox="0 0 10 10"><circle cx="5" cy="5" r="4" fill="#7b2cbf"/></svg>

```css
.x { color: #7b2cbf; }
```

## Otra sección {#propia}

::: tarjetas 2

### Tarjeta uno

Texto.

### Tarjeta dos

Texto.

:::
"""


class GeneradorUnico(unittest.TestCase):
    """doc_to_html.py es el generador único con el perfil de la visión: regenerar un documento de la maqueta antigua ya
    lo migra (decisión 309), con las subsecciones plegables, las anclas de siempre y los recursos narrativos."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.md = Path(self._tmp.name) / 'vision.md'

    def tearDown(self):
        self._tmp.cleanup()

    def generar(self, md: str = VISION, *args) -> str:
        self.md.write_text(md, encoding='utf-8')
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(GENERADOR), str(self.md), '--identidad', 'ninguna',
                            '--logo', 'ninguno', *args], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.stderr = r.stderr
        return self.md.with_suffix('.html').read_text(encoding='utf-8')

    def test_maqueta_comun_sin_la_antigua(self):
        h = self.generar()
        self.assertIn('data-kit="skills/crear_documentos/assets/estilo_documento.css"', h)
        self.assertNotIn('estilo_base', h)
        self.assertNotIn('class="bloque', h)
        self.assertIn('Documento de visión', h)
        self.assertFalse((GENERADOR.parent / 'carcasa.py').exists())

    def test_opciones_en_comentarios(self):
        h = self.generar()
        self.assertIn('data-destino="proyecto"', h)
        self.assertIn('convertir_cabecera.py', self.stderr)

    def test_subsecciones_plegables_con_las_anclas_de_siempre(self):
        h = self.generar()
        self.assertIn('<details class="seccion" id="instalacion-del-plugin" open>', h)
        self.assertIn('<details id="que-es" class="subseccion" open><summary class="subseccion-summary">Qué es</summary>', h)
        self.assertIn('<details id="que-es-1" class="subseccion" open>', h)
        self.assertIn('<details id="detalle" class="subsubseccion"><summary class="subsubseccion-summary">Detalle</summary>', h)
        self.assertIn('id="propia"', h)
        # Los títulos de las tarjetas no son subsecciones.
        self.assertNotIn('<details id="tarjeta-uno"', h)
        self.assertIn('Tarjeta uno', h)

    def test_recursos_narrativos(self):
        h = self.generar()
        self.assertIn('data-kit="skills/crear_documentos/assets/narrativa.css"', h)
        self.assertIn('.turno { display: grid;', h)
        sin = self.generar('---\ndestino: proyecto\nherramientas: ninguna\n---\n# Prueba\n\n## Uno\n\nTexto.\n')
        self.assertNotIn('narrativa.css', sin)

    def test_colores_del_md_al_tema_salvo_el_codigo(self):
        h = self.generar(VISION, '--paleta', 'teal')
        self.assertIn('--primario: #00726b', h)  # --paleta sigue valiendo como --tema
        self.assertIn('style="fill: var(--primario)"', h)
        self.assertIn('#7b2cbf', h.split('<pre')[1].split('</pre>')[0])


class SinPerfilNoPliega(unittest.TestCase):
    def test_el_fundacional_no_pliega_los_apartados(self):
        comun = Path(__file__).resolve().parents[1] / 'skills' / 'crear_documentos' / 'scripts' / 'documento_a_html.py'
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
            md = Path(d) / 'doc.md'
            md.write_text('---\ndestino: proyecto\nherramientas: ninguna\n---\n# Prueba\n\n## Uno\n\nTexto.\n\n### Apartado\n\nMás.\n',
                          encoding='utf-8')
            r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(comun), str(md), '--identidad', 'ninguna',
                                '--logo', 'ninguno'], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stderr)
            h = md.with_suffix('.html').read_text(encoding='utf-8')
        self.assertIn('<h3>Apartado</h3>', h)
        self.assertNotIn('class="subseccion', h)


if __name__ == '__main__':
    unittest.main()
