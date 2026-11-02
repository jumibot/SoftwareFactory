"""Comprueba que una infografía funciona sin conexión.

Abre el HTML en Chrome (o Edge) y en WebKit con todas las peticiones a internet
bloqueadas y dice, para cada navegador, si hay lienzo, qué versión de three.js
ha cargado y qué errores de página ha habido. Sirve para validar la versión
autónoma antes de compartirla como archivo.

Uso:
    python -I scripts/comprobar_sin_red.py <infografia.html> [--espera 9] [--canal chrome|msedge]

Requiere Playwright (`pip install playwright` y `python -m playwright install webkit`).
Devuelve código 1 si algún navegador no dibuja la escena o da errores.
"""
import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def comprobar(html, espera_s, canal):
    url = Path(html).resolve().as_uri()
    todo_bien = True
    with sync_playwright() as pw:
        for motor in ("chromium", "webkit"):
            opciones = {"channel": canal} if motor == "chromium" else {}
            navegador = getattr(pw, motor).launch(**opciones)
            contexto = navegador.new_context(viewport={"width": 1400, "height": 900})
            # Bloquea todo lo que salga a la red: solo vale lo que va dentro del archivo.
            contexto.route("**/*", lambda r: r.abort() if r.request.url.startswith("http") else r.continue_())
            pagina = contexto.new_page()
            errores = []
            pagina.on("pageerror", lambda e: errores.append(str(e)))
            pagina.goto(url)
            pagina.wait_for_timeout(espera_s * 1000)
            lienzo = pagina.evaluate("!!document.querySelector('canvas')")
            three = pagina.evaluate("window.__THREE__ || '?'")
            print(f"{motor}: sin red | lienzo: {'sí' if lienzo else 'NO'} | three.js: {three} | "
                  f"errores: {'; '.join(errores[:3]) if errores else 'ninguno'}")
            todo_bien = todo_bien and lienzo and not errores
            navegador.close()
    return todo_bien


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("html")
    p.add_argument("--espera", type=int, default=9, help="segundos de espera tras cargar (por defecto, 9)")
    p.add_argument("--canal", default="chrome", help="navegador instalado para Chromium: chrome o msedge")
    a = p.parse_args()
    sys.exit(0 if comprobar(a.html, a.espera, a.canal) else 1)


if __name__ == "__main__":
    main()
