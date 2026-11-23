"""Guarda la imagen fija de la vista principal de una infografía, la que sale al imprimir un documento que la incrusta.

Abre la infografía en su modo de prueba (?test, que fija el estado y para la rotación), espera a que la escena se asiente
y guarda una captura PNG junto a ella, con el mismo nombre (<infografia>.png). El recurso «::: infografia» del generador
de documentos la pone en lugar del marco al imprimir en A4 (decisión 315). Se vuelve a guardar cada vez que la
infografía cambia de aspecto (modelo, estilo, vista principal).

Uso:
    python -I -X utf8 scripts/imagen_fija.py <infografia.html> [--estado "mode=marcha&explode=0"] [--ancho 1600]
        [--alto 900] [--canal chrome|msedge] [--salida <ruta.png>]

Requiere Playwright (`pip install playwright`) y Chrome o Edge instalados.
"""
import argparse
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

FOTOGRAMAS = 60  # los que hacen falta para que el centrado y las etiquetas se asienten


def capturar(html: Path, salida: Path, estado: str, ancho: int, alto: int, canal: str) -> None:
    url = html.resolve().as_uri() + "?test" + (f"&{estado.lstrip('&?')}" if estado else "")
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(channel=canal, args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
        pagina = navegador.new_page(viewport={"width": ancho, "height": alto}, device_scale_factor=1)
        errores = []
        pagina.on("pageerror", lambda e: errores.append(str(e)))
        pagina.goto(url)
        try:
            pagina.wait_for_function(
                f"document.body.dataset.snap && JSON.parse(document.body.dataset.snap).fc >= {FOTOGRAMAS}",
                timeout=90_000)
        except Exception:
            navegador.close()
            sys.exit(f"La escena no ha llegado a {FOTOGRAMAS} fotogramas en 90 s"
                     + (f"; errores: {'; '.join(errores[:3])}" if errores else ""))
        if errores:
            navegador.close()
            sys.exit("Errores de página: " + "; ".join(errores[:3]))
        foto = json.loads(pagina.evaluate("document.body.dataset.snap"))
        pagina.locator("#view").screenshot(path=str(salida))
        navegador.close()
    print(f"{salida} · {ancho}×{alto} · modo {foto.get('mode')} · {len(foto.get('tags', []))} etiquetas")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("html")
    p.add_argument("--estado", default="", help="estado de la vista principal, como en el modo de prueba (mode=…&explode=…)")
    p.add_argument("--ancho", type=int, default=1600)
    p.add_argument("--alto", type=int, default=900)
    p.add_argument("--canal", default="chrome", help="navegador instalado: chrome o msedge")
    p.add_argument("--salida", default=None, help="por defecto, <infografia>.png junto a ella")
    a = p.parse_args()
    html = Path(a.html)
    if not html.is_file():
        sys.exit(f"No encuentro la infografía: {html}")
    capturar(html, Path(a.salida) if a.salida else html.with_suffix(".png"), a.estado, a.ancho, a.alto, a.canal)


if __name__ == "__main__":
    main()
