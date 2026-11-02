"""Genera el HTML de un documento fundacional con el generador común de la skill crear_documentos.

Uso:
    python <skills>/documento_fundacional/scripts/fundacional_to_html.py <documento>.md [opciones de documento_a_html.py]

Es el generador común con el perfil del fundacional (../perfil.json): su tipo por defecto y los recursos del
catálogo que usa. Las opciones son las de crear_documentos/scripts/documento_a_html.py.
"""
import runpy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
COMUN = AQUI.parent.parent / "crear_documentos" / "scripts" / "documento_a_html.py"
if not COMUN.is_file():
    sys.exit(f"Falta la skill crear_documentos junto a esta: no encuentro {COMUN}")
sys.argv[1:1] = ["--perfil", str(AQUI.parent / "perfil.json")]
runpy.run_path(str(COMUN), run_name="__main__")
