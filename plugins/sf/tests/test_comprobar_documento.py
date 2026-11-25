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
    def generar(cls, nombre: str, extra: str) -> Path:
        md = cls.dir / f'{nombre}.md'
        md.write_text(MD.format(extra=extra), encoding='utf-8')
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


if __name__ == '__main__':
    unittest.main()
