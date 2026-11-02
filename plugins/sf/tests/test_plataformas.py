"""Que las herramientas de Python del plugin funcionen fuera de esta máquina: en macOS, el python3 de las herramientas de
línea de órdenes es el 3.9 («La orden de Python sale del intérprete que se detecta», 236; el mod acepta desde el 3.9).

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"
"""
import ast
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
SCRIPTS = sorted(p for p in PLUGIN.rglob('*.py') if 'tests' not in p.relative_to(PLUGIN).parts)


def anotaciones(arbol: ast.AST) -> list:
    salida = []
    for n in ast.walk(arbol):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.returns is not None:
            salida.append(n.returns)
        if isinstance(n, (ast.arg, ast.AnnAssign)) and n.annotation is not None:
            salida.append(n.annotation)
    return salida


class Python39(unittest.TestCase):
    def test_hay_scripts(self):
        self.assertIn(PLUGIN / 'tools' / 'cola.py', SCRIPTS)

    def test_sintaxis_de_python_39(self):
        for p in SCRIPTS:
            with self.subTest(p.relative_to(PLUGIN).as_posix()):
                ast.parse(p.read_text(encoding='utf-8'), feature_version=(3, 9))

    def test_tipos_con_barra_solo_con_annotations_diferidas(self):
        """`str | None` en una anotación se evalúa al definir la función en 3.9 y falla: hace falta
        `from __future__ import annotations`."""
        for p in SCRIPTS:
            arbol = ast.parse(p.read_text(encoding='utf-8'))
            diferidas = any(isinstance(n, ast.ImportFrom) and n.module == '__future__'
                            and any(a.name == 'annotations' for a in n.names) for n in arbol.body)
            barra = any(isinstance(m, ast.BinOp) and isinstance(m.op, ast.BitOr)
                        for a in anotaciones(arbol) for m in ast.walk(a))
            with self.subTest(p.relative_to(PLUGIN).as_posix()):
                self.assertTrue(diferidas or not barra)


if __name__ == '__main__':
    unittest.main()
