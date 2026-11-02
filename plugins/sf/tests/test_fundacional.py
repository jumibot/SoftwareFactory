"""Pruebas del generador común de los documentos (skills/crear_documentos/scripts/documento_a_html.py), por los
generadores del fundacional y del informe de las deliberativas: tarjetas con color, icono y plegado, preguntas con
opciones, perfiles por tipo de documento y respaldo.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[1] / 'skills'
GENERADOR = SKILLS / 'documento_fundacional' / 'scripts' / 'fundacional_to_html.py'
INFORME = SKILLS / 'informe_deliberativa' / 'scripts' / 'informe_to_html.py'
RESPALDAR = SKILLS / 'crear_documentos' / 'scripts' / 'respaldar.py'

CABECERA = """---
destino: proyecto
herramientas: ninguna
---
# Prueba

## Uno | Primera {#uno}

Entrada.

"""


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.md = Path(self._tmp.name) / 'doc.md'

    def tearDown(self):
        self._tmp.cleanup()

    def generar(self, cuerpo: str, ok: bool = True, generador: Path = GENERADOR) -> str:
        self.md.write_text(CABECERA + cuerpo, encoding='utf-8')
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(generador), str(self.md), '--identidad', 'ninguna',
                            '--logo', 'ninguno'], capture_output=True, text=True, encoding='utf-8')
        self.stderr = r.stderr
        if not ok:
            self.assertNotEqual(r.returncode, 0)
            return r.stderr
        self.assertEqual(r.returncode, 0, r.stderr)
        return self.md.with_suffix('.html').read_text(encoding='utf-8')


class Tarjetas(Base):
    def test_sin_opciones_igual_que_siempre(self):
        h = self.generar("::: tarjetas 2\n\n### A\n\nTexto a.\n\n### B\n\nTexto b.\n\n:::\n")
        self.assertIn('<div class="tarjetas cols-2">', h)
        self.assertEqual(h.count('<article class="tarjeta">'), 2)
        self.assertNotIn('con-cabecera', h.split('</style>')[-1])

    def test_color_icono_y_plegable(self):
        h = self.generar("::: tarjetas 3 plegables\n\n#### Código {color=turquesa icono=codigo} {: #cod}\n\n"
                         "Tipos\n:   - implementar\n    - corregir\n\n#### Otra\n\nTexto.\n\n:::\n")
        cuerpo = h.split('<main')[1]
        self.assertIn('<details class="tarjeta con-cabecera con-color plegable" id="cod"', cuerpo)
        self.assertIn('--c:#1f7a7a', cuerpo)
        self.assertRegex(cuerpo, r'<summary class="tarjeta-cabecera">\s*<svg class="tarjeta-icono"')
        self.assertIn('<h4 class="tarjeta-titulo">Código</h4>', cuerpo)
        self.assertIn('<li>implementar</li>', cuerpo)  # el Markdown de dentro se convierte
        self.assertIn('<details class="tarjeta con-cabecera plegable"', cuerpo)  # sin color, también plegable
        self.assertNotIn('{color', cuerpo)

    def test_color_sin_plegar(self):
        h = self.generar("::: tarjetas 2\n\n### A {color=#123456}\n\nTexto.\n\n:::\n")
        self.assertIn('<article class="tarjeta con-cabecera con-color" style="--c:#123456', h)
        self.assertRegex(h, r'<div class="tarjeta-cabecera">\s*<h3 class="tarjeta-titulo">A</h3>\s*</div>')

    def test_errores(self):
        self.assertIn('Color de tarjeta no válido', self.generar("::: tarjetas 2\n\n### A {color=rosa}\n\nX.\n\n:::\n", ok=False))
        self.assertIn('Icono de tarjeta desconocido', self.generar("::: tarjetas 2\n\n### A {icono=gato}\n\nX.\n\n:::\n", ok=False))
        self.assertIn('Opción de tarjeta desconocida', self.generar("::: tarjetas 2\n\n### A {tamano=2}\n\nX.\n\n:::\n", ok=False))


PREGUNTAS = """::: preguntas 2 plegables

### 1 · Abierta {recomendada=A} {: #p1}

Contexto.

Opción A
:   Uno.

Opción B
:   Dos.

Recomendación
:   **A.** Porque sí.

### 2 · Decidida {estado=decidida recomendada=A elegida=B}

Opción A
:   Uno.

Opción B
:   Dos.

Decisión
:   B.

### 3 · Separada {estado=separada destino=tarea_303 recomendada=A}

Opción A
:   Uno.

Opción B
:   Dos.

:::
"""


class Preguntas(Base):
    def test_estado_y_opciones(self):
        h = self.generar(PREGUNTAS, generador=INFORME).split('<main')[1]
        self.assertIn('<div class="tarjetas preguntas cols-2">', h)
        self.assertRegex(h, r'<details class="tarjeta con-cabecera pregunta abierta plegable"[^>]*id="p1"')
        self.assertIn('<span class="estado-pregunta abierta">Abierta</span>', h)
        self.assertIn('<span class="estado-pregunta decidida">Decidida · B</span>', h)
        self.assertIn('<span class="estado-pregunta separada">Separada · tarea 303</span>', h)
        self.assertIn('<dt class="opcion recomendada">Opción A<span class="marca-opcion recomendada">Recomendada</span></dt>', h)
        self.assertIn('<dt class="opcion elegida">Opción B<span class="marca-opcion elegida">Elegida</span></dt>', h)
        self.assertIn('<dd class="opcion recomendada descartada">', h)
        self.assertIn('<dt class="recomendacion">Recomendación</dt>', h)
        self.assertIn('<dt class="decision">Decisión</dt>', h)
        self.assertNotIn('{estado', h)

    def test_errores(self):
        e = self.generar("::: preguntas\n\n### P {recomendada=C}\n\nOpción A\n:   x\n\n:::\n", ok=False, generador=INFORME)
        self.assertIn('no tiene «Opción C»', e)
        e = self.generar("::: preguntas\n\n### P {elegida=A}\n\nOpción A\n:   x\n\n:::\n", ok=False, generador=INFORME)
        self.assertIn('solo vale con estado=decidida', e)
        e = self.generar("::: preguntas\n\n### P {estado=pendiente}\n\nOpción A\n:   x\n\n:::\n", ok=False, generador=INFORME)
        self.assertIn('Estado de pregunta no válido', e)
        e = self.generar("::: preguntas\n\n### P {color=verde}\n\nOpción A\n:   x\n\n:::\n", ok=False, generador=INFORME)
        self.assertIn('Opción de pregunta desconocida', e)

    def test_aviso_sin_recomendacion(self):
        self.generar("::: preguntas\n\n### P\n\nOpción A\n:   x\n\n:::\n", generador=INFORME)
        self.assertIn('no tiene opción recomendada', self.stderr)


class Perfiles(Base):
    def test_el_fundacional_no_usa_preguntas(self):
        e = self.generar(PREGUNTAS, ok=False)
        self.assertIn('no usa el recurso «::: preguntas»', e)

    def test_tipo_por_defecto(self):
        self.assertIn('<title>Prueba · Documento fundacional</title>', self.generar("Texto.\n"))
        self.assertIn('<title>Prueba · Informe</title>', self.generar("Texto.\n", generador=INFORME))

    def test_rutas_del_kit_comunes(self):
        h = self.generar("Texto.\n")
        self.assertIn('data-kit="skills/crear_documentos/assets/estilo_documento.css"', h)
        self.assertIn('data-kit="skills/crear_documentos/assets/plegado.js"', h)
        self.assertNotIn('documento_fundacional/assets', h)


class Respaldo(unittest.TestCase):
    def test_respalda_md_y_html_y_no_pisa(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
            md = Path(d) / 'Informe.md'
            md.write_text('uno', encoding='utf-8')
            md.with_suffix('.html').write_text('<p>uno</p>', encoding='utf-8')
            orden = [sys.executable, '-I', '-X', 'utf8', str(RESPALDAR), str(md), 'Sin mapa']
            r = subprocess.run(orden, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual((Path(d) / '_respaldo' / 'Informe_antes-sin-mapa.md').read_text(encoding='utf-8'), 'uno')
            self.assertTrue((Path(d) / '_respaldo' / 'Informe_antes-sin-mapa.html').is_file())
            r = subprocess.run(orden, capture_output=True, text=True, encoding='utf-8')
            self.assertNotEqual(r.returncode, 0)
            self.assertIn('Ya hay un respaldo', r.stderr)


class Avisos(Base):
    def test_etiquetas_sueltas_fuera_del_codigo(self):
        self.generar('Va a <documento> y a `<otro>`, con <strong>negrita</strong> y <https://ejemplo.org>.\n\n'
                     '```text\n<ruta>\n```\n')
        self.assertIn('«<documento>»', self.stderr)
        self.assertNotIn('<otro>', self.stderr)
        self.assertNotIn("<ruta>", self.stderr)
        self.assertNotIn('strong', self.stderr)
        self.assertNotIn('ejemplo.org', self.stderr)


class IconosPropios(unittest.TestCase):
    def test_iconos_de_la_identidad(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
            ident = Path(d) / 'docs' / 'identidad'
            ident.mkdir(parents=True)
            (ident / 'casa.svg').write_text('<svg viewBox="0 0 24 24"><path d="M3 11l9-8 9 8"/></svg>', encoding='utf-8')
            (ident / 'identidad.json').write_text('{"iconos": {"cohete": "<path d=\\"M12 2l4 8\\"/>", "casa": "casa.svg"}}',
                                                  encoding='utf-8')
            md = Path(d) / 'docs' / 'doc.md'
            md.write_text(CABECERA + '::: tarjetas 2\n\n### A {icono=cohete}\n\nX.\n\n### B {icono=casa}\n\nY.\n\n:::\n',
                          encoding='utf-8')
            r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(GENERADOR), str(md), '--logo', 'ninguno'],
                               capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stderr)
            h = md.with_suffix('.html').read_text(encoding='utf-8')
            self.assertIn('<path d="M12 2l4 8"/></svg>', h)
            self.assertIn('<path d="M3 11l9-8 9 8"/></svg>', h)


if __name__ == '__main__':
    unittest.main()
