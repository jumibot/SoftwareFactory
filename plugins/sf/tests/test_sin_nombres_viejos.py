"""«En observación», sin rastros del nombre viejo (decisiones 212 y 215): falla si reaparece en lo que está en el alcance.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"

El alcance: el plugin entero (código, skills con sus references, plantillas, tipos y pruebas), el CLAUDE.md, el README
y los documentos que describen el flujo. Fuera, con su porqué: las decisiones y el historial de versiones de los
documentos (son historia, 215), docs/referencias/ (también la procedencia de las piezas), docs/specs/vision/ y
_respaldo/ («testing» en su sentido general o histórico) y las líneas con «migración 215», las únicas que nombran lo de antes para
convertirlo al cargar. Fuera también lo que Claude Code genera en el plugin al pasar sus pruebas (tsconfig.json y
.claude-plugin/types/, los tipos del motor): no es del plugin, va al .gitignore y no se publica (tarea 346).
"""
import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
PLUGIN = RAIZ / 'plugins' / 'sf'
DOCUMENTOS = [
    'CLAUDE.md',
    'README.md',
    'docs/como-funciona-la-software-factory.md',
    'docs/como-funciona-el-panel.md',
    'docs/como-funcionan-los-estados.md',
    'docs/specs/funcional/software-factory.md',
    'docs/mejora-continua-a-la-software-factory.md',
    'docs/uso-del-panel.md',
]
# Documentos compartidos que se ponen al día en su propia tarea «Actualizar <documento>»: mientras tengan el nombre
# viejo, no hacen fallar la prueba; cuando ya no lo tengan, la prueba pide sacarlos de aquí.
EN_SU_TAREA = {
    'docs/como-funciona-el-panel.md',
    'docs/como-funcionan-los-estados.md',
    'docs/uso-del-panel.md',
}
# Lo que Claude Code genera en el plugin (claude plugin test): rutas relativas a plugins/sf, archivo o carpeta.
GENERADOS = {'tsconfig.json', '.claude-plugin/types'}
EXTENSIONES = {'.py', '.ts', '.tsx', '.md', '.json', '.html', '.txt', '.css', '.js'}
MARCA = 'migración 215'
# Lo que nombraba el estado de antes y sus órdenes, campos, botones y frases.
VIEJOS = re.compile(
    r'testing'                                   # el estado, a-testing, aTesting, TESTING
    r'|sin-probar|sinprobar'                     # el valor interno y sus variables
    r'|\bprobando\b'                             # la marca y su orden
    r'|probar ahora|test mode'                   # la respuesta y la T de antes
    r'|[`\'"«]probada[`\'"»]'                    # la orden
    r'|\bpor probada\b|\by probada\b|\blas probadas\b',  # dar por probada, cerrada y probada
    re.IGNORECASE)
# Las claves y funciones de la orden (probada-tarea, probadaTarea), sin confundirlas con «comprobadaEn».
IDENTIFICADORES = re.compile(r'\bprobada(?=[A-Z_-])')
# «testing» en otro sentido: el módulo de pruebas del motor y una skill externa.
PERMITIDOS = re.compile(r'claude-code/testing|webapp-testing')
# Las filas del historial de versiones de los documentos: «| 1.0.0 | …» o «| próxima | …».
VERSION = re.compile(r'^\|\s*(próxima|\d+\.\d+\.\d+)\s*\|')


def generado(ruta: Path) -> bool:
    relativa = ruta.relative_to(PLUGIN).as_posix()
    return any(relativa == g or relativa.startswith(g + '/') for g in GENERADOS)


def archivos():
    for ruta in sorted(PLUGIN.rglob('*')):
        if ruta.is_file() and ruta.suffix in EXTENSIONES and not generado(ruta) \
                and '__pycache__' not in ruta.parts and 'node_modules' not in ruta.parts \
                and ruta != Path(__file__).resolve():
            yield ruta
    for nombre in DOCUMENTOS:
        if (RAIZ / nombre).is_file():
            yield RAIZ / nombre


def rastros(ruta: Path) -> list:
    hallados = []
    for n, linea in enumerate(ruta.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
        if MARCA in linea or VERSION.match(linea):
            continue
        limpia = PERMITIDOS.sub('', linea)
        if VIEJOS.search(limpia) or IDENTIFICADORES.search(limpia):
            hallados.append(f'{n}: {linea.strip()[:140]}')
    return hallados


class SinNombresViejos(unittest.TestCase):
    def test_nada_en_el_alcance_nombra_lo_de_antes(self):
        for ruta in archivos():
            relativa = ruta.relative_to(RAIZ).as_posix()
            if relativa in EN_SU_TAREA:
                continue
            with self.subTest(relativa):
                self.assertEqual(rastros(ruta), [], f'{relativa} nombra lo de antes de «En observación» (215)')

    def test_los_pendientes_de_su_tarea_siguen_pendientes(self):
        for relativa in sorted(EN_SU_TAREA):
            with self.subTest(relativa):
                self.assertTrue((RAIZ / relativa).is_file(), f'{relativa} ya no existe: sácalo de EN_SU_TAREA')
                self.assertNotEqual(rastros(RAIZ / relativa), [], f'{relativa} ya está al día: sácalo de EN_SU_TAREA')

    def test_lo_generado_por_claude_code_queda_fuera(self):
        for relativa, fuera in [('tsconfig.json', True), ('.claude-plugin/types/tsconfig.json', True),
                                ('.claude-plugin/types/claude-code/index.d.ts', True), ('.claude-plugin/plugin.json', False),
                                ('types/index.d.ts', False), ('hooks/tsconfig.json', False)]:
            self.assertEqual(generado(PLUGIN / relativa), fuera, relativa)

    def test_la_prueba_detecta_lo_de_antes(self):
        prueba = PLUGIN / 'tests' / '__rastro_215__.md'
        try:
            for linea, rastro in [('Pasa a Test' + 'ing', True), ('`a-' + 'testing`', True), ('sin-pro' + 'bar', True),
                                  ("'proba" + "da'", True), ('darla por proba' + 'da', True), ('Probar ' + 'ahora', True),
                                  ('proba' + 'daTarea', True), ("key: 'proba" + "da-tarea:x:2'", True),
                                  ('En observación', False), ('lista para probar', False), ('una plantilla probada', False),
                                  ('const comprobadaEn = 1', False), ('obligaciones aprobadas', False),
                                  ("import { test } from 'claude-code/test" + "ing'", False),
                                  ('| 0.30.0 | Sin probar pasa a Test' + 'ing. |', False)]:
                prueba.write_text(linea + '\n', encoding='utf-8')
                self.assertEqual(bool(rastros(prueba)), rastro, linea)
        finally:
            prueba.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
