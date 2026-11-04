"""El progreso de una incorporación a la SF, para que el panel lo enseñe (tarea 333).

Mientras Claude lleva la incorporación (skill sf:incorporar_proyecto_a_sf, con menús), el panel de la SF enseña los
pasos —«1. Plugin», «2. Caso»…— con la respuesta dada en cada uno, el actual resaltado y los que faltan atenuados,
para que el propietario sepa dónde está y lo repase todo antes del OK. Claude anota el progreso con esta herramienta:
lo que se puede hacer con un comando no se infiere (metodología, 1).

El progreso se guarda fuera del proyecto, que no cambia sin el OK del propietario: en la carpeta de la SF de Claude
Code (~/.claude/sf, o $CLAUDE_CONFIG_DIR/sf, la misma que usa el panel para sus copias de cola.py), un archivo por
proyecto, incorporacion-<carpeta>.json (la ruta del proyecto en minúsculas, con «_» en lo que no es letra, cifra o
guion, como claveIncorporacion() del mod), con la carpeta dentro. No depende de la sesión: sobrevive a /reload-plugins,
/clear, al modo prueba y a una sesión nueva o reanudada en la misma carpeta (tarea 333, a petición del propietario). El
mod, al acabar un turno o al cargarse con la incorporación a medias (también con Esc), le pone "pausa": true, que
quita cualquier orden que escriba; al abandonarla, al cerrar la lista terminada o al salir el panel operativo, lo deja
en {} (sin pasos), que vale como borrado (decisión 258).

  {
    "version": 1,
    "carpeta": "/ruta/a/Contador",
    "caso": "existente",
    "actual": 3,
    "pasos": [ { "nombre": "Plugin", "respuesta": "Al día, 1.7.6" }, { "nombre": "Caso", "respuesta": "Existente" },
               { "nombre": "Diagnóstico", "respuesta": null }, … ],
    "cambio": "2026-11-03T10:15:00+01:00"
  }

`actual` es el número (desde 1) del paso en que se está; 0, si ya no queda ninguno. Los anteriores con respuesta están
hechos; los que vienen, por hacer.

Uso (desde la carpeta del proyecto; <plugin> es la carpeta del plugin sf, la de la skill):
  python -I -X utf8 <plugin>/tools/incorporacion.py empezar CASO [--pasos NOMBRE …] [--raiz RUTA]
      Fija la lista de pasos del caso (nuevo, existente, actualizar o diagnosticar; con --pasos, otra lista) y se pone
      en el primero sin respuesta. Si ya había una incorporación en esta carpeta, se conservan las
      respuestas de los pasos que se llaman igual: así se cambia de caso tras el menú del caso sin perder lo dicho.
  … paso N|NOMBRE           Se pone en ese paso (para volver a uno o saltar a otro).
  … anotar N|NOMBRE TEXTO   Anota la respuesta de un paso (lo detectado sin preguntar también) y, si era el actual,
                            pasa al siguiente sin respuesta. Un texto de varias líneas queda en una, con « · ».
  … ver                     Los pasos, con su respuesta y cuál es el actual.
  … borrar                  Borra el progreso: al empezar de nuevo. Al terminar no: lo quita el mod cuando el
                            proyecto ya tiene su panel operativo; si se para a medias, el propietario, con Abandonar.

Todas las órdenes toman --raiz RUTA (por omisión, la carpeta actual): el proyecto cuyo progreso se lee o escribe.

Sale con 0 si todo va bien, con 1 si la orden no vale (un paso que no existe, nada que anotar) y con 2 si no hay
incorporación empezada. Con --json (en cualquier orden), la salida es una línea JSON con ok y mensaje.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

VERSION = 1
# Los pasos de cada caso, en el orden de la skill sf:incorporar_proyecto_a_sf («Nuevo y existente», «Actualizar» y
# «Procedimiento»), tras poner al día el plugin, antes de nada (tools/plugin_sf.py). Los nombres son cortos: el panel
# los pinta en una columna estrecha.
PASOS = {
    'nuevo': ['Plugin', 'Caso', 'Identidad', 'Repositorio', 'Convenciones', 'Cambios y OK', 'Aplicar', 'Comprobación'],
    'existente': ['Plugin', 'Caso', 'Diagnóstico', 'Identidad', 'Repositorio', 'Convenciones', 'Cambios y OK', 'Aplicar',
                  'CLAUDE.md', 'Pasar a sf/', 'Comprobación'],
    'actualizar': ['Plugin', 'Caso', 'Diagnóstico', 'Configuración', 'Cambios y OK', 'Aplicar', 'CLAUDE.md',
                   'Pasar a sf/', 'Comprobación'],
    'diagnosticar': ['Plugin', 'Caso', 'Diagnóstico', 'Informe'],
}
LARGO_RESPUESTA = 300
LARGO_NOMBRE = 40
# Las de otros proyectos (o las de antes, por sesión) que nadie borró, tras estos días.
DIAS_VIEJAS = 7


class Fallo(Exception):
    def __init__(self, mensaje: str, codigo: int = 1):
        super().__init__(mensaje)
        self.codigo = codigo


def carpeta_sf() -> Path:
    config = os.environ.get('CLAUDE_CONFIG_DIR', '').strip()
    return (Path(config) if config else Path.home() / '.claude') / 'sf'


def normal(ruta: str) -> str:
    """Como normal() del mod: barras normales y sin la del final."""
    return ruta.replace('\\', '/').rstrip('/')


def carpeta_de(raiz: str) -> str:
    return normal(str(Path(raiz).resolve()))


def clave(carpeta: str) -> str:
    """El nombre del archivo de un proyecto: su ruta en minúsculas, con «_» en lo que no es letra o cifra ASCII o
    guion (como claveIncorporacion() del mod)."""
    return ''.join(c if c.isascii() and (c.isalnum() or c == '-') else '_' for c in normal(carpeta).lower())


def archivo(carpeta: str) -> Path:
    return carpeta_sf() / f'incorporacion-{clave(carpeta)}.json'


def ahora() -> str:
    return datetime.now().astimezone().isoformat(timespec='seconds')


def leer(carpeta: str) -> dict | None:
    """El progreso del proyecto, o None si no hay."""
    ruta = archivo(carpeta)
    try:
        datos = json.loads(ruta.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None
    if not isinstance(datos, dict) or not isinstance(datos.get('pasos'), list):
        return None
    if normal(str(datos.get('carpeta', ''))).lower() != normal(carpeta).lower():
        return None
    return datos


def escribir(datos: dict) -> None:
    ruta = archivo(datos['carpeta'])
    ruta.parent.mkdir(parents=True, exist_ok=True)
    # Anotar algo quita la pausa que pone el mod al acabar un turno con la incorporación a medias (decisión 258).
    datos.pop('pausa', None)
    datos['cambio'] = ahora()
    fd, tmp = tempfile.mkstemp(prefix='.incorporacion-', suffix='.tmp', dir=str(ruta.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
            f.write('\n')
        os.replace(tmp, ruta)
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def borrar_viejas(propia: Path) -> None:
    limite = time.time() - DIAS_VIEJAS * 86_400
    for p in propia.parent.glob('incorporacion-*.json'):
        try:
            if p != propia and p.stat().st_mtime < limite:
                p.unlink()
        except OSError:
            pass


def una_linea(texto: str, largo: int) -> str:
    partes = [x.strip() for x in texto.replace('\r', '\n').split('\n')]
    t = ' · '.join(x for x in partes if x)
    return t if len(t) <= largo else t[:largo - 1].rstrip() + '…'


def indice(datos: dict, cual: str) -> int:
    """El número (desde 1) del paso, por número o por nombre (sin distinguir mayúsculas)."""
    pasos = datos['pasos']
    if cual.strip().isdigit():
        n = int(cual)
        if 1 <= n <= len(pasos):
            return n
        raise Fallo(f'no hay paso {n}: van del 1 al {len(pasos)}.')
    for i, p in enumerate(pasos, 1):
        if str(p.get('nombre', '')).lower() == cual.strip().lower():
            return i
    raise Fallo(f'no hay ningún paso «{cual}»: son {", ".join(str(p.get("nombre")) for p in pasos)}.')


def siguiente_sin_respuesta(datos: dict, desde: int) -> int:
    pasos = datos['pasos']
    for i in range(desde, len(pasos) + 1):
        if not pasos[i - 1].get('respuesta'):
            return i
    return 0


def resumen(datos: dict) -> str:
    n = datos.get('actual', 0)
    total = len(datos['pasos'])
    if not n:
        return f'Incorporación ({datos.get("caso")}): los {total} pasos, hechos.'
    return f'Incorporación ({datos.get("caso")}): paso {n} de {total}, {datos["pasos"][n - 1]["nombre"]}.'


def requerida(raiz: str) -> dict:
    datos = leer(carpeta_de(raiz))
    if datos is None:
        raise Fallo('no hay ninguna incorporación empezada en esta carpeta: antes, «empezar CASO».', 2)
    return datos


def o_empezar(caso: str, pasos: list[str] | None, raiz: str) -> dict:
    caso = caso.strip().lower()
    if pasos:
        nombres = [una_linea(x, LARGO_NOMBRE) for x in pasos if x.strip()]
    elif caso in PASOS:
        nombres = PASOS[caso]
    else:
        raise Fallo(f'caso «{caso}» desconocido: {", ".join(PASOS)}, o la lista con --pasos.')
    if not nombres:
        raise Fallo('la lista de pasos está vacía.')
    carpeta = carpeta_de(raiz)
    antes = leer(carpeta) or {'pasos': []}
    dichas = {str(p.get('nombre', '')).lower(): p.get('respuesta') for p in antes['pasos']}
    datos = {
        'version': VERSION,
        'carpeta': carpeta,
        'caso': caso,
        'actual': 0,
        'pasos': [{'nombre': x, 'respuesta': dichas.get(x.lower()) or None} for x in nombres],
    }
    datos['actual'] = siguiente_sin_respuesta(datos, 1)
    escribir(datos)
    borrar_viejas(archivo(carpeta))
    return datos


def o_paso(cual: str, raiz: str) -> dict:
    datos = requerida(raiz)
    datos['actual'] = indice(datos, cual)
    escribir(datos)
    return datos


def o_anotar(cual: str, texto: str, raiz: str) -> dict:
    datos = requerida(raiz)
    n = indice(datos, cual)
    respuesta = una_linea(texto, LARGO_RESPUESTA)
    if not respuesta:
        raise Fallo('no hay nada que anotar: la respuesta está vacía.')
    datos['pasos'][n - 1]['respuesta'] = respuesta
    if datos.get('actual') == n:
        datos['actual'] = siguiente_sin_respuesta(datos, n + 1)
    escribir(datos)
    return datos


def o_borrar(raiz: str) -> bool:
    try:
        archivo(carpeta_de(raiz)).unlink()
        return True
    except FileNotFoundError:
        return False


def texto_ver(datos: dict) -> str:
    lineas = [resumen(datos)]
    for i, p in enumerate(datos['pasos'], 1):
        marca = '▶' if i == datos.get('actual') else ('✓' if p.get('respuesta') else '·')
        lineas.append(f'{marca} {i}. {p["nombre"]}' + (f': {p["respuesta"]}' if p.get('respuesta') else ''))
    return '\n'.join(lineas)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog='incorporacion.py', description='El progreso de una incorporación a la SF, para el panel.')
    ap.add_argument('--json', action='store_true', help='salida en una línea JSON')
    comun = argparse.ArgumentParser(add_help=False)
    comun.add_argument('--json', action='store_true', dest='json_orden', help='salida en una línea JSON')
    comun.add_argument('--raiz', default='.', help='la carpeta del proyecto (por omisión, la actual)')
    sub = ap.add_subparsers(dest='orden', required=True)
    e = sub.add_parser('empezar', parents=[comun])
    e.add_argument('caso')
    e.add_argument('--pasos', nargs='+')
    p = sub.add_parser('paso', parents=[comun])
    p.add_argument('cual')
    a = sub.add_parser('anotar', parents=[comun])
    a.add_argument('cual')
    a.add_argument('texto', nargs='+')
    sub.add_parser('ver', parents=[comun])
    sub.add_parser('borrar', parents=[comun])
    args = ap.parse_args(argv)
    como_json = args.json or args.json_orden
    try:
        if args.orden == 'empezar':
            datos = o_empezar(args.caso, args.pasos, args.raiz)
        elif args.orden == 'paso':
            datos = o_paso(args.cual, args.raiz)
        elif args.orden == 'anotar':
            datos = o_anotar(args.cual, ' '.join(args.texto), args.raiz)
        elif args.orden == 'ver':
            datos = requerida(args.raiz)
        else:
            borrado = o_borrar(args.raiz)
            mensaje = 'Progreso de la incorporación borrado.' if borrado else 'No había progreso que borrar.'
            print(json.dumps({'ok': True, 'mensaje': mensaje}, ensure_ascii=False) if como_json else mensaje)
            return 0
    except Fallo as f:
        if como_json:
            print(json.dumps({'ok': False, 'mensaje': str(f)}, ensure_ascii=False))
        else:
            print(f'incorporacion.py: {f}', file=sys.stderr)
        return f.codigo
    if como_json:
        print(json.dumps({'ok': True, 'mensaje': resumen(datos), 'progreso': datos}, ensure_ascii=False))
    else:
        print(texto_ver(datos) if args.orden == 'ver' else resumen(datos))
    return 0


if __name__ == '__main__':
    sys.exit(main())
