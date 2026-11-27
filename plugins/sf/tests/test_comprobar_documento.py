"""Pruebas de la comprobación de un documento con una sola orden (crear_documentos/scripts/comprobar_documento.py):
un documento pequeño correcto pasa y uno con un bloque demasiado ancho da sus desbordes, en pantalla y en A4.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_comprobar_documento.py"
"""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills' / 'crear_documentos' / 'scripts'
GENERADOR = SCRIPTS / 'documento_a_html.py'
spec = importlib.util.spec_from_file_location('comprobar_documento', SCRIPTS / 'comprobar_documento.py')
cdoc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cdoc)

MD = """---
destino: proyecto
herramientas: todas
---
# Prueba de la comprobación

## Uno | Primera {{#uno}}

Entrada con un [enlace a la segunda](#dos) y otro [de fuera](https://example.com).

::: tarjetas 2

### Qué es {{color=turquesa icono=documento}}

Para quién
:   El equipo.

### Estado {{color=naranja icono=check}}

Fecha
:   Hoy.

:::

{extra}

## Dos | Segunda {{#dos}}

| Columna | Otra |
|---|---|
| a | b |

```python
def f(**kw):
    return kw
```
"""

ANCHO = '<div class="demasiado-ancho" style="width: 900px">Un bloque de 900 px.</div>'

PORTADA_OSCURA = """---
destino: proyecto
herramientas: ninguna
portada: oscura
---
# Prueba de la portada oscura

Entrada con `código en línea` en la portada.

## Uno | Primera {#uno}

Texto.
"""

PARRAFO = ('<p>Àlex abrió el portátil con el café todavía caliente y repasó la cola: un bug en el gemelo, una petición de '
           'Laura y tres tareas a medias que nadie había vuelto a mirar desde el viernes por la tarde.</p>')
HISTORIA = """---
destino: proyecto
herramientas: ninguna
---
# Prueba de la historia: abrir en el lector

<div class="lector" data-titulo="Historia · prólogo" data-al-abrir="historia" data-marca="/SF" data-invitacion="Pulsa el logo">
<div class="libro">
<p class="libro-capitulo">Prólogo</p>
<p class="libro-titulo">Un lunes</p>
""" + '\n'.join([PARRAFO] * 24) + """
</div>
</div>

## Uno | Primera {#uno}

Texto de la primera sección.

<div class="caso">
<p class="caso-etiqueta">El caso · capítulo 1 · El martes</p>
<p>El martes, Àlex fijó el objetivo.</p>
</div>

<p class="palido" style="color:#dddddd">Texto pálido, para ver que el documento se mide.</p>

<figure class="vertical">
<svg viewBox="0 0 200 60" width="200" role="img" aria-label="Una caja" style="font-family:var(--fuente-texto)"><rect x="10" y="10" width="180" height="40" fill="none" stroke="#333333"/><text x="100" y="36" text-anchor="middle" font-size="16" fill="#222222">Caja</text></svg>
<figcaption>Una caja.</figcaption>
</figure>
"""


def hay_navegador() -> bool:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            cdoc.cd.navegador(pw).close()
        return True
    except BaseException:  # noqa: BLE001 — sin Playwright o sin navegador, se saltan
        return False


class Estaticas(unittest.TestCase):
    def test_oscuro_y_diagramas_se_detectan(self):
        self.assertTrue(cdoc.tiene_oscuro(':root[data-theme="dark"] { --texto: #fff; }'))
        self.assertFalse(cdoc.tiene_oscuro(':root { --texto: #000; }'))
        self.assertTrue(cdoc.tiene_diagramas('<figure class="diagrama"><svg></svg></figure>'))
        self.assertFalse(cdoc.tiene_diagramas('<figure><img></figure><div><svg class="icono"></svg></div>'))

    def test_contraste_con_capas(self):
        gris = {'elemento': 'p', 'color': [0x77, 0x77, 0x77, 1], 'capas': [], 'px': 17, 'peso': 400}
        self.assertEqual(cdoc.contrastes([gris]), ['contraste 4,48:1 en p (mín. 4,5:1)'])
        self.assertEqual(cdoc.contrastes([dict(gris, px=24)]), [])   # grande: 3:1
        oscuro = dict(gris, color=[255, 255, 255, 1], capas=[[0, 0, 0, 1]])
        self.assertEqual(cdoc.contrastes([oscuro]), [])


@unittest.skipUnless(hay_navegador(), 'sin Playwright o sin navegador')
class EnElNavegador(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.dir = Path(cls._tmp.name)
        cls.bien = cls.generar('bien', '')
        cls.mal = cls.generar('mal', ANCHO)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    @classmethod
    def generar(cls, nombre: str, extra: str, texto: str = '') -> Path:
        md = cls.dir / f'{nombre}.md'
        md.write_text(texto or MD.format(extra=extra), encoding='utf-8')
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(GENERADOR), str(md), '--identidad', 'ninguna',
                            '--logo', 'ninguno', '--tema', 'tinta'], capture_output=True, text=True, encoding='utf-8')
        assert r.returncode == 0, r.stderr + r.stdout
        return md.with_suffix('.html')

    def test_el_correcto_pasa_en_las_cuatro_vistas_y_en_a4(self):
        pdf = self.dir / 'bien.pdf'
        res = cdoc.comprobar(self.bien, pdf)
        self.assertEqual(cdoc.errores(res), [])
        self.assertEqual([(v['vista'], v['modo']) for v in res['vistas']],
                         [('escritorio', 'claro'), ('móvil', 'claro'), ('escritorio', 'oscuro'), ('móvil', 'oscuro')])
        self.assertTrue(pdf.is_file())
        self.assertGreaterEqual(res['a4']['paginas'], 2)   # la portada, sola, y el cuerpo
        self.assertIsNone(res['diagramas'])                # sin diagramas, no se pasa su comprobación
        self.assertEqual(cdoc.main([str(self.bien), '--pdf', str(pdf)]), 0)

    def test_el_desborde_sale_en_el_movil_y_en_a4_y_no_en_el_escritorio(self):
        res = cdoc.comprobar(self.mal, self.dir / 'mal.pdf')
        lista = cdoc.errores(res)
        movil = [e for e in lista if e.startswith('móvil (390 px)')]
        self.assertTrue(any('se sale de la pantalla div.demasiado-ancho' in e for e in movil), lista)
        self.assertTrue(any(e.startswith('móvil (390 px), oscuro') for e in movil), lista)
        self.assertFalse([e for e in lista if e.startswith('escritorio')], lista)
        self.assertTrue(any(e.startswith('A4: se corta por la derecha div.demasiado-ancho') for e in lista), lista)
        self.assertEqual(cdoc.main([str(self.mal), '--pdf', str(self.dir / 'mal.pdf')]), 1)

    def test_el_codigo_en_linea_se_lee_sobre_la_portada_oscura(self):
        # El fondo suave del código es claro y el texto de la portada oscura, blanco: sin su regla, 1,08:1.
        html = self.generar('portada-oscura', '', PORTADA_OSCURA)
        lista = cdoc.errores(cdoc.comprobar(html, self.dir / 'portada-oscura.pdf'))
        self.assertFalse([e for e in lista if 'code' in e], lista)

    def test_el_documento_que_abre_en_la_historia_se_mide(self):
        # Con data-al-abrir="historia", la capa del lector oculta el documento: se mide después de salir de ella. Y el
        # prólogo, antes de la primera sección, no entra en la portada, que cabe sola en la primera página del A4.
        html = self.generar('historia', '', HISTORIA)
        res = cdoc.comprobar(html, self.dir / 'historia.pdf')
        lista = cdoc.errores(res)
        self.assertTrue(any('p.palido' in e and e.startswith('escritorio (1300 px), claro: contraste') for e in lista), lista)
        self.assertTrue(res['diagramas'], 'sin la comprobación de los diagramas')
        self.assertTrue(all(len(m['figuras']) == 1 for m in res['diagramas']), res['diagramas'])
        self.assertLessEqual(res['a4']['portada']['alto'], cdoc.A4_ALTO)
        self.assertFalse([e for e in lista if e.startswith('A4: la portada')], lista)


if __name__ == '__main__':
    unittest.main()
