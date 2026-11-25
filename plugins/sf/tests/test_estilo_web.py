"""La web comercial y la marca del panel, con los colores, la letra y los logos del estilo de la SF (decisiones 312 y 335).

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_estilo_web.py"

La web (site/) lee el estilo con scripts/estilo_web.py: si alguien cambia docs/identidad/estilo.json o sus logos sin
pasarlo, esta prueba lo dice. El panel lleva la marca y el logo en constantes (hooks/bienvenida.ts y hooks/logo.ts): aquí
se comprueba que siguen siendo los del estilo y su logo oscuro.
"""
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
ESTILO = RAIZ / 'docs' / 'identidad' / 'estilo.json'
HOOKS = RAIZ / 'plugins' / 'sf' / 'hooks'


def constante(archivo: str, nombre: str) -> str:
    m = re.search(rf"export const {nombre} = '([^']+)'", (HOOKS / archivo).read_text(encoding='utf-8'))
    assert m, f'{nombre} no está en {archivo}'
    return m.group(1).lower()


def colores_del_logo(nombre: str) -> set[str]:
    return {c.lower() for c in re.findall(r'fill="(#[0-9a-fA-F]{6})"', (ESTILO.parent / nombre).read_text(encoding='utf-8'))}


@unittest.skipUnless((RAIZ / 'site' / 'index.html').is_file() and ESTILO.is_file(), 'solo en el repositorio de la SF')
class EstiloWeb(unittest.TestCase):
    def test_la_web_tiene_el_estilo_al_dia(self):
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(RAIZ / 'scripts' / 'estilo_web.py'), '--comprobar'],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stderr or r.stdout)

    def test_la_web_no_lleva_colores_de_marca_propios(self):
        html = (RAIZ / 'site' / 'index.html').read_text(encoding='utf-8')
        for viejo in ('#f4bf36', '#827dbd', '#b3aee6'):
            self.assertNotIn(viejo, html.lower())

    def test_la_marca_del_panel_es_el_primario_del_estilo(self):
        primario = json.loads(ESTILO.read_text(encoding='utf-8'))['colores']['primario'].lower()
        self.assertEqual(constante('bienvenida.ts', 'COLOR_MARCA'), primario)

    def test_el_logo_del_panel_es_el_logo_oscuro_del_estilo(self):
        self.assertEqual({constante('logo.ts', 'COLOR_LETRAS'), constante('logo.ts', 'COLOR_BARRA')},
                         colores_del_logo('logo-oscuro.svg'))


if __name__ == '__main__':
    unittest.main()
