"""Genera el HTML de un documento de visión o de un documento explicativo («Cómo funciona…») con el generador único.

Uso:
    python <skills>/documento_vision/scripts/doc_to_html.py <documento>.md [opciones de documento_a_html.py]

Es el generador común de la skill crear_documentos (crear_documentos/scripts/documento_a_html.py) con el perfil de la
visión (../perfil.json): todos los recursos del catálogo, las subsecciones plegables (### abiertas, #### plegadas) y
los id de las secciones como los calculaba la maqueta antigua, para que los enlaces sigan valiendo. Regenerar un
documento de la maqueta antigua ya lo migra (decisión 309); su cabecera se pone al día con
crear_documentos/scripts/convertir_cabecera.py. «--paleta» sigue valiendo como sinónimo de «--tema».
"""
import runpy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
COMUN = AQUI.parent.parent / "crear_documentos" / "scripts" / "documento_a_html.py"
if not COMUN.is_file():
    sys.exit(f"Falta la skill crear_documentos junto a esta: no encuentro {COMUN}")
sys.argv[1:] = ["--tema" if a == "--paleta" else "--tema=" + a[9:] if a.startswith("--paleta=") else a for a in sys.argv[1:]]
sys.argv[1:1] = ["--perfil", str(AQUI.parent / "perfil.json")]
runpy.run_path(str(COMUN), run_name="__main__")
