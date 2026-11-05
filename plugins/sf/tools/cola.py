"""Cola de tareas de un proyecto de la SF: cada cambio de estado, con una orden (skill sf:flujo_tareas).

Uso:
  python -I -X utf8 cola.py [--raiz RUTA] [--quien propietario|principal] [--via cli|panel] [--json] <orden> …

  --raiz   la carpeta del proyecto (la cola es .sf/peticiones.json) o la ruta de una cola; por omisión, la carpeta
           actual. Con una cola suelta, el repositorio es la carpeta que contiene su .sf/.
  --quien  quién decide el cambio (principal por omisión); --via, por dónde llega (cli por omisión).
  --json   la respuesta en una línea JSON: {"ok", "mensaje", …}, para el panel. Además, «crear» y «split» dan el
           número nuevo («id»); un cierre, una reversión o un «probar» que choca, «fallo» (choques, commit, merge
           o sin-traer) y su «motivo».

Órdenes (la tabla de cambios está en skills/flujo_tareas/references/estados.md):
  lista | ver N | copias
  crear "texto" [--descripcion D] [--tipo T] [--en-curso]   en-curso N | en-cola N
           (--descripcion, obligatoria cuando crea Claude: --quien principal, el de omisión, salvo --via panel)
  rama N nombre [--sin-activar | --anotar]           paso añadir N "texto" [--prueba] | paso marcar N P estado [--texto T]
  paso quitar N P                                    renombrar N "texto" | tipo N T
  subagente N --worktree RUTA [--rama AUX]           informe N --terminado|--interrumpido ["texto"]
  listo N --prueba "qué mirar"                       comprobado N "texto"
  probar N | observando N | seguir N                 cerrar N | a-observacion N [--prueba P] [--coautor L]
  reobservar N                                       una cerrada vuelve a observación, con su commit de develop
  descartar N | limpiar                              reabrir N "qué falla" [--en-cola] [--rama nombre] [--sin-activar]
  revertir N --eliminar|--pendiente [--commit H …]
  eliminar N | restaurar N                           fusionar N M … | split N 2,3
  a-propuesta N                                      (en cola, sin rama) vuelve a su propuesta o crea una
  de-propuesta "título" [--numero P] [--descripcion D] [--tipo T]   la propuesta por decidir, a tarea en cola
           (--descripcion, obligatoria como en crear)
  recuperar n|archivo                                choques N [--archivos a b …]
  encargo N [--coautor "Co-Authored-By: …"]          la parte fija del encargo de su subagente
  decision "Título" --archivo RUTA|--texto T [--numero NNN] [--coautor "Co-Authored-By: …"] [--push]
           registra en sf/decisiones/ (o en docs/decisiones/, la de antes; NNN-AAAA-MM-DD-titulo.md, el siguiente número) o reescribe la NNN, rehace su
           README.md y hace el commit «Decisión NNN: Título» en develop, también con otra rama activa, sin cambiarla
           (tarea 283); da el número y el hash. No toca la cola.
  subir [--repetir T]  sube develop a su remoto. Como el push de un cierre, con el remoto público revisa antes lo que sale
           (revision_publica.py, decisión 259): con algo nuevo, no sube; con algo ya subido, sube si se repite la
           subida en 10 minutos con los mismos hallazgos. No toca la cola.

Cada escritura guarda antes una copia de la cola en .sf/copias/ (las últimas 50), con la cola bloqueada por
.sf/peticiones.lock. Cada tarea lleva su historial {evento, fecha, quien, via, detalle}; las que salen de la cola
pasan, con él, a .sf/historial.jsonl (una línea por salida, con el estado con que sale: cerrada, eliminada,
absorbida o descartada, o revertida en las anteriores a la decisión 134; la última de cada número manda).
Revertir deja la tarea eliminada o en Pendientes, reabierta (decisión 134). Una tarea lleva los pasos de cierre,
«Activar rama para poder probar» y «Cerrar la tarea», desde que entra en curso, y no se quitan (decisión 174). Cerrar,
también a observación, pide «Cerrar la tarea» y hechos los demás salvo «Activar rama para poder probar», que el cierre marca
(decisiones 121 y 172). Una en observación se cierra (va bien, «cerrar», sin git: ya está en develop) o se revierte
(va mal); los nombres de antes de la decisión 215 se convierten al cargar la cola. Las órdenes que dejan una tarea sin su
subagente (cerrar, a-observacion, descartar, eliminar, a-propuesta, revertir, limpiar, reabrir y, en las absorbidas,
fusionar) quitan su worktree y borran su rama auxiliar, sin forzar (salvo reabrir): lo que queda se avisa (decisión
169). Una tarea en curso con commits propios en su rama no vuelve a la cola (decisión 170); con la rama vacía o ya
borrada, sí: «en-cola» borra la rama y recoge su subagente vacío (tarea 275).
Las deliberativas (investigar, deliberar, diseñar) no tienen rama, worktree ni rama auxiliar: «rama» y «subagente» se
niegan, su único paso de cierre es «Cerrar la tarea» y no pasan a observación (decisiones 256 y 278). Una rama sin
cambios respecto a develop se cierra sin commit: «cerrar» la borra y saca la tarea (tarea 345).
«probar» activa la rama, o la deja si ya lo está, y marca hecho el paso de prueba (decisión 172). Antes integra develop
en ella (merge), para probar con lo último; con choques, lo deshace, no la activa y dice qué archivos chocan («fallo»:
choques); con commits de una rama auxiliar sin traer a la de la tarea, ni integra ni activa (tarea 270). P, el número de un
paso, cuenta desde 1, como en los mensajes y en el «n» de cada paso de «ver». Los pasos de cierre no cambian de texto
ni se repiten: quedan al final, una vez cada uno; una en curso sin ellos los recibe al cargar la cola. Un paso de
trabajo nuevo deja otra vez pendiente el de prueba (decisión 174). Una ayuda de prueba («paso añadir --prueba») va
entre los dos de cierre, no la exige ningún cierre, que la deja como esté, ni devuelve el de prueba a pendiente
(decisión 184). «comprobado» añade lo comprobado como paso hecho («Comprobado: …»), sin devolver el de prueba a
pendiente; el campo «comprobado» de antes pasa así a sus pasos al cargar (decisión 288). Los números no se reutilizan. Sale con 0 si hace el
cambio, 1 si no lo hace (y dice por qué) y 2 si la orden está mal escrita. «choques», de consulta,
sale con 0 si la tarea no comparte archivos con las en curso o en observación y con 3 si los comparte (decisión 130).
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ESTADOS = ('en-cola', 'en-curso', 'en-observacion', 'descartada')
# El `estado` con que sale de la cola una tarea, en su línea de .sf/historial.jsonl. «revertida», solo en las líneas
# anteriores a la decisión 134: ahora una revertida sale eliminada o vuelve a la cola.
ESTADOS_SALIDA = ('cerrada', 'eliminada', 'absorbida', 'descartada', 'revertida')
ESTADOS_PASO = ('pendiente', 'en-curso', 'hecho')
PASOS_CIERRE = ('Activar rama para poder probar', 'Cerrar la tarea')
# El paso de prueba se llamaba «Probar la tarea»: la cola lo renombra al cargarla (decisión 172).
PASO_PROBAR, PASO_PROBAR_ANTES = PASOS_CIERRE[0], 'Probar la tarea'
# El tipo de cada tarea, en infinitivo; el panel lo pinta tras el título, «(DELIBERAR)» (decisión del propietario,
# 2026-10-31). Opcional: las tareas anteriores no lo tienen.
TIPOS = ('deliberar', 'documentar', 'diseñar', 'implementar', 'especificar', 'corregir', 'investigar')
# Las deliberativas (metodología, «Tipos de tarea»: investigar, deliberar y diseñar) no tienen rama, worktree ni rama
# auxiliar: solo escriben su documento, que va directo a develop en cada vuelta; lo demás, a tareas propias con rama
# («Las tareas de investigar no tienen rama», 256; «Una deliberativa solo escribe su documento, sin rama…», 278). No
# se prueban ni pasan por observación (218): su único paso de cierre es «Cerrar la tarea».
DELIBERATIVAS = ('investigar', 'deliberar', 'diseñar')
MAX_COPIAS = 50
# La línea de coautoría de los commits de la propia SF, que no tiene .sf/proyecto.json: su valor de `coautor` por
# defecto. Un proyecto la configura en `coautor` de su .sf/proyecto.json o con --coautor; sin ninguna, sus commits
# van sin línea («La firma del commit de cierre es configurable; sin configurar, sin línea», 238).
COAUTOR = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>'
# Los nombres de antes de «En observación» (decisión 215) no son alias: la cola, una copia al recuperarla y el
# historial se convierten una vez al cargarlos. Las líneas con «migración 215» son las únicas que los nombran.
ESTADOS_VIEJOS = {'sin-probar': 'en-observacion'}  # migración 215
CAMPOS_VIEJOS = {'probando': 'observando'}  # migración 215
EVENTOS_VIEJOS = {'a-testing': 'a-observacion', 'probada': 'cerrada', 'probando': 'observando', 'pendiente': 'seguir'}  # migración 215
ESPERA_BLOQUEO = 10  # segundos
BLOQUEO_VIEJO = 120  # segundos: un bloqueo más antiguo se da por abandonado


class Rechazo(Exception):
    """El cambio no se hace: la cola queda como estaba."""


# ---------- Configuración del proyecto (.sf/proyecto.json; informe «Configuración inicial», tarea 263) ----------

# El repositorio de la propia SF se reconoce por la fuente del plugin; no tiene .sf/proyecto.json: su configuración
# sale de esta marca, con el manifiesto del plugin y lo demás por defecto.
MARCA_SF = 'plugins/sf/.claude-plugin/plugin.json'
FORMATOS_COMMIT = ('libre', 'conventional', 'propio')
# Lo que vale cada campo que falta (o que no se entiende): lo de antes de la configuración, así los proyectos ya
# incorporados no cambian hasta ponerlos al día. manifiesto: ninguno, solo el tag.
POR_DEFECTO = {'idioma': 'es', 'commits': 'libre', 'remoto': 'origin', 'rama_main': 'main', 'manifiesto': [],
               'metodologia': True, 'kanban': None, 'coautor': None}
TRAILER_TAREA = 'SF-Tarea'


def _nombre_valido(v) -> bool:
    return isinstance(v, str) and bool(v.strip()) and not re.search(r'[\s~^:?*\[\\]|\.\.|^-', v.strip())


def formato_manifiesto(ruta: str) -> str | None:
    """«json» (clave version: package.json, plugin.json) o «pyproject» (pyproject.toml); None si no se soporta."""
    nombre = ruta.strip().replace('\\', '/').rsplit('/', 1)[-1].lower()
    return 'json' if nombre.endswith('.json') else 'pyproject' if nombre == 'pyproject.toml' else None


def linea_coautor(v) -> str | None:
    """La línea de coautoría de un valor de `coautor` o de --coautor: con «Co-Authored-By: » delante si no lo lleva;
    None si está vacío. Un valor de más de una línea, o que no es texto, no vale (ValueError)."""
    if v is None or (isinstance(v, str) and not v.strip()):
        return None
    if not isinstance(v, str) or '\n' in v.strip() or '\r' in v.strip():
        raise ValueError('coautor')
    v = v.strip()
    return v if v.lower().startswith('co-authored-by:') else f'Co-Authored-By: {v}'


def leer_configuracion(datos, es_sf: bool = False) -> dict:
    """La configuración del proyecto, con los valores por defecto donde falta un campo o no se entiende (y entonces
    lo nombra en «desconocidos», sin bloquear: decisión 171). En la SF (es_sf, por su marca), su manifiesto y su línea
    de coautoría si no dice otra cosa, y lo demás por defecto. kanban, en bloque: la cadena antigua es el proyecto de
    JKanban. coautor: la línea de coautoría de los commits de la SF, o None: sin línea (238)."""
    d = datos if isinstance(datos, dict) else {}
    c = {k: (list(v) if isinstance(v, list) else v) for k, v in POR_DEFECTO.items()}
    c['proyecto'] = d['proyecto'].strip() if isinstance(d.get('proyecto'), str) and d['proyecto'].strip() else None
    raros = []
    if 'idioma' in d:
        if isinstance(d['idioma'], str) and re.fullmatch(r'[a-z]{2,3}(-[A-Za-z]{2,4})?', d['idioma'].strip()):
            c['idioma'] = d['idioma'].strip()
        else:
            raros.append('idioma')
    if 'commits' in d:
        if d['commits'] in FORMATOS_COMMIT:
            c['commits'] = d['commits']
        else:
            raros.append('commits')
    for campo in ('remoto', 'rama_main'):
        if campo in d:
            if _nombre_valido(d[campo]):
                c[campo] = d[campo].strip()
            else:
                raros.append(campo)
    if 'manifiesto' in d:
        m = d['manifiesto']
        lista = [] if m is None else [m] if isinstance(m, str) else m if isinstance(m, list) else None
        if lista is None or not all(isinstance(x, str) and formato_manifiesto(x) for x in lista):
            raros.append('manifiesto')
            lista = [x for x in (lista or []) if isinstance(x, str) and formato_manifiesto(x)]
        c['manifiesto'] = [x.strip().replace('\\', '/') for x in lista]
    elif es_sf:
        c['manifiesto'] = [MARCA_SF]
    if 'metodologia' in d:
        if isinstance(d['metodologia'], bool):
            c['metodologia'] = d['metodologia']
        else:
            raros.append('metodologia')
    if 'kanban' in d and d['kanban'] is not None:
        k = d['kanban']
        if isinstance(k, str) and k.strip():
            c['kanban'] = {'proveedor': 'jkanban', 'proyecto': k.strip()}
        elif (isinstance(k, dict) and k.get('proveedor') == 'jkanban' and isinstance(k.get('proyecto'), str)
              and k['proyecto'].strip()):
            c['kanban'] = {'proveedor': 'jkanban', 'proyecto': k['proyecto'].strip()}
        else:
            raros.append('kanban')
    if 'coautor' in d:
        try:
            c['coautor'] = linea_coautor(d['coautor'])
        except ValueError:
            raros.append('coautor')
    elif es_sf:
        c['coautor'] = COAUTOR
    auto = d.get('automatizaciones')
    c['automatizaciones'] = auto if isinstance(auto, dict) else {}
    c['desconocidos'] = raros
    return c


def configuracion(repo: Path) -> dict:
    """La de .sf/proyecto.json del proyecto (o la de la SF, por su marca); un archivo que no se lee, como si faltara."""
    try:
        datos = json.loads((repo / '.sf' / 'proyecto.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        datos = None
    return leer_configuracion(datos, es_sf=(repo / MARCA_SF).is_file())


# El prefijo conventional del título del squash, por tipo de tarea («El título del commit en formato conventional
# sale del tipo de tarea», 233). Lo que no es código entrega documentos (informes, diseños): docs. Sin tipo, chore.
PREFIJO_POR_TIPO = {'implementar': 'feat', 'corregir': 'fix', 'documentar': 'docs', 'especificar': 'docs',
                    'investigar': 'docs', 'deliberar': 'docs', 'diseñar': 'docs'}
PREFIJO_SIN_TIPO = 'chore'
YA_CONVENTIONAL = re.compile(r'^[a-z]+(\([^)]*\))?!?: ')


def mensaje_de_tarea(titulo: str, cuerpo: str, id_: int, formato: str, tipo: str | None = None,
                     coautor: str | None = None) -> str:
    """El mensaje del commit de una tarea con su número según el formato (decisión 207): «(N)» al final del título
    con commits libres; con conventional o propio, el trailer «SF-Tarea: N» al pie, junto a la coautoría, y el
    título con el prefijo de su tipo (233), salvo que ya lo lleve. La línea de coautoría, solo si la hay (238)."""
    cuerpo = cuerpo.strip('\n')
    pie = [coautor] if coautor else []
    if formato == 'libre':
        titulo = f'{titulo} ({id_})'
    else:
        if not YA_CONVENTIONAL.match(titulo):
            titulo = f'{PREFIJO_POR_TIPO.get(tipo or "", PREFIJO_SIN_TIPO)}: {titulo}'
        pie.insert(0, f'{TRAILER_TAREA}: {id_}')
    return '\n\n'.join([titulo] + ([cuerpo] if cuerpo else []) + (['\n'.join(pie)] if pie else [])) + '\n'


def convenciones(c: dict) -> str:
    """La línea de convenciones del proyecto: la lleva el encargo de un subagente (y el mod la entrega igual)."""
    marca = '«(N)» al final del título' if c['commits'] == 'libre' else f'el trailer «{TRAILER_TAREA}: N» al pie'
    formato = {'libre': 'libres', 'conventional': 'conventional commits',
               'propio': 'con la forma de los últimos del proyecto'}[c['commits']]
    partes = [f'idioma {c["idioma"]}', f'commits {formato}, con el número de la tarea como {marca}',
              f'remoto {c["remoto"]}']
    if c['rama_main'] != 'main':
        partes.append(f'se publica en {c["rama_main"]}, que hace de main')
    return 'Convenciones del proyecto: ' + '; '.join(partes) + '.'


# ---------- Cola, copias, bloqueo e historial ----------

class Cola:
    def __init__(self, raiz: Path, quien: str, via: str):
        raiz = raiz.resolve()
        if raiz.suffix == '.json':
            self.archivo, self.sf = raiz, raiz.parent
            self.repo = self.sf.parent
        else:
            self.repo, self.sf = raiz, raiz / '.sf'
            self.archivo = self.sf / 'peticiones.json'
        self.copias = self.sf / 'copias'
        self.historial = self.sf / 'historial.jsonl'
        self.bloqueo = self.sf / 'peticiones.lock'
        self.quien, self.via = quien, via
        self.bloqueada = False
        self.datos: dict = {}
        self.original: str | None = None
        # Lo que la respuesta JSON lleva además de ok y mensaje (el panel lo lee).
        self.extra: dict = {}

    # Bloqueo: un archivo creado en exclusiva; si otro lo tiene, espera; si es muy antiguo, lo quita.
    def bloquear(self) -> None:
        if not self.sf.is_dir():
            raise Rechazo(f'No hay {self.sf}: el proyecto no está en la SF.')
        limite = time.monotonic() + ESPERA_BLOQUEO
        while True:
            try:
                fd = os.open(self.bloqueo, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, f'{os.getpid()} {ahora()}\n'.encode())
                os.close(fd)
                self.bloqueada = True
                return
            except FileExistsError:
                try:
                    viejo = time.time() - self.bloqueo.stat().st_mtime > BLOQUEO_VIEJO
                except FileNotFoundError:
                    continue
                if viejo:
                    self.bloqueo.unlink(missing_ok=True)
                    continue
                if time.monotonic() > limite:
                    raise Rechazo(f'La cola está bloqueada ({self.bloqueo.name}): otra escritura en marcha.')
                time.sleep(0.05)

    def desbloquear(self) -> None:
        if self.bloqueada:
            self.bloqueo.unlink(missing_ok=True)
            self.bloqueada = False

    def cargar(self) -> None:
        if self.archivo.exists():
            self.original = self.archivo.read_bytes().decode('utf-8')
            try:
                self.datos = json.loads(self.original)
            except json.JSONDecodeError as e:
                raise Rechazo(f'{self.archivo.name} no es JSON válido ({e}): recupera una copia con «recuperar».')
        else:
            self.original, self.datos = None, {}
        self.datos.setdefault('ultimo', 0)
        if not isinstance(self.datos.get('peticiones'), list):
            self.datos['peticiones'] = []
        for t in self.datos['peticiones']:
            migrar_tarea(t)
            for x in (t.get('pasos') if isinstance(t, dict) and isinstance(t.get('pasos'), list) else []):
                if isinstance(x, dict) and x.get('texto') == PASO_PROBAR_ANTES:
                    x['texto'] = PASO_PROBAR
            # Una tarea en curso de antes de la decisión 174 recibe aquí sus pasos de cierre, una vez y al final.
            if isinstance(t, dict) and t.get('estado') == 'en-curso':
                asegurar_cierre(t)

    @property
    def tareas(self) -> list:
        return self.datos['peticiones']

    def buscar(self, id_: int) -> dict | None:
        return next((t for t in self.tareas if t.get('id') == id_), None)

    def tarea(self, id_: int, *estados: str) -> dict:
        t = self.buscar(id_)
        if t is None:
            fuera = self.archivadas().get(id_)
            raise Rechazo(f'La {id_} no está en la cola' + (f' ({situacion(fuera)}).' if fuera else '.'))
        if estados and t.get('estado') not in estados:
            raise Rechazo(f'La {id_} está {nombre_estado(t)}: la orden pide {" o ".join(estados)}.')
        return t

    def copiar(self) -> Path | None:
        """Copia la cola actual en .sf/copias/ y deja solo las últimas MAX_COPIAS."""
        if self.original is None:
            return None
        self.copias.mkdir(exist_ok=True)
        while True:
            marca = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')[:-3]
            destino = self.copias / f'peticiones-{marca}.json'
            if not destino.exists():
                break
            time.sleep(0.002)
        destino.write_bytes(self.original.encode('utf-8'))
        for vieja in lista_copias(self.copias)[MAX_COPIAS:]:
            vieja.unlink(missing_ok=True)
        return destino

    def guardar(self) -> None:
        self.copiar()
        self.migrar_historial()
        texto = json.dumps(self.datos, ensure_ascii=False, indent=2) + '\n'
        temporal = self.archivo.with_name(self.archivo.name + '.tmp')
        temporal.write_bytes(texto.encode('utf-8'))
        os.replace(temporal, self.archivo)
        self.original = texto

    def archivadas(self) -> dict:
        """El último registro de cada número que salió de la cola, de .sf/historial.jsonl."""
        salida: dict = {}
        if self.historial.exists():
            for linea in self.historial.read_bytes().decode('utf-8').splitlines():
                if linea.strip():
                    try:
                        t = json.loads(linea)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(t, dict) and isinstance(t.get('id'), int):
                        migrar_tarea(t)
                        salida[t['id']] = t
        return salida

    def migrar_historial(self) -> None:
        """Reescribe .sf/historial.jsonl con los nombres de ahora si alguna línea trae los de antes (decisión 215)."""
        if not self.historial.exists():
            return
        lineas, cambio = [], False
        for linea in self.historial.read_bytes().decode('utf-8').splitlines():
            try:
                t = json.loads(linea) if linea.strip() else None
            except json.JSONDecodeError:
                t = None
            if isinstance(t, dict) and migrar_tarea(t):
                cambio = True
                linea = json.dumps(t, ensure_ascii=False)
            lineas.append(linea)
        if cambio:
            temporal = self.historial.with_name(self.historial.name + '.tmp')
            temporal.write_bytes(''.join(x + '\n' for x in lineas).encode('utf-8'))
            os.replace(temporal, self.historial)

    def archivar(self, t: dict) -> None:
        with self.historial.open('ab') as f:
            f.write((json.dumps(t, ensure_ascii=False) + '\n').encode('utf-8'))

    def sacar(self, t: dict, estado: str) -> None:
        """Saca la tarea de la cola y la deja, con su historial y el estado con que sale, en .sf/historial.jsonl."""
        assert estado in ESTADOS_SALIDA, estado
        self.datos['peticiones'] = [x for x in self.tareas if x is not t]
        t['estado'] = estado
        self.archivar(t)

    def siguiente(self) -> int:
        ids = [self.datos.get('ultimo')] + [t.get('id') for t in self.tareas] + list(self.archivadas())
        return max([x for x in ids if isinstance(x, int)], default=0) + 1

    def anotar(self, t: dict, evento: str, detalle: str | None = None) -> None:
        e = {'evento': evento, 'fecha': ahora(), 'quien': self.quien, 'via': self.via}
        if detalle:
            e['detalle'] = detalle
        t.setdefault('historial', []).append(e)


def migrar_tarea(t) -> bool:
    """Pasa a los nombres de ahora el estado, el campo y los eventos de antes de «En observación» (decisión 215).
    Dice si ha cambiado algo; una tarea ya convertida no cambia."""
    if not isinstance(t, dict):
        return False
    cambio = False
    if t.get('estado') in ESTADOS_VIEJOS:
        t['estado'], cambio = ESTADOS_VIEJOS[t['estado']], True
    for viejo, nuevo in CAMPOS_VIEJOS.items():
        if viejo in t:
            valor = t.pop(viejo)
            if valor:
                t[nuevo] = valor
            cambio = True
    for e in t.get('historial') if isinstance(t.get('historial'), list) else []:
        if isinstance(e, dict) and e.get('evento') in EVENTOS_VIEJOS:
            if e['evento'] == 'probada' and not e.get('detalle'):  # migración 215
                e['detalle'] = 'en observación'
            e['evento'], cambio = EVENTOS_VIEJOS[e['evento']], True
    if 'comprobado' in t:
        # El campo «comprobado» se retira: lo que tenga pasa a un paso hecho (decisión 288).
        valor = t.pop('comprobado')
        if isinstance(valor, str) and valor.strip():
            anadir_comprobado(t, valor)
        cambio = True
    return cambio


def texto_comprobado(texto: str) -> str:
    texto = texto.strip()
    return texto if texto.lower().startswith('comprobado') else f'Comprobado: {texto}'


def anadir_comprobado(t: dict, texto: str) -> int:
    """Añade lo comprobado como paso hecho, antes de los de cierre y de las ayudas de prueba, sin devolver a pendiente
    «Activar rama para poder probar» (decisión 288). Da su número."""
    p = pasos(t)
    sitio = next((i for i, x in enumerate(p) if isinstance(x, dict) and (es_de_cierre(x.get('texto')) or es_ayuda(x))), len(p))
    p.insert(sitio, {'texto': texto_comprobado(texto), 'estado': 'hecho'})
    return sitio + 1


def ahora() -> str:
    return datetime.datetime.now().astimezone().isoformat(timespec='seconds')


def lista_copias(carpeta: Path) -> list:
    """Las copias, la más reciente primero."""
    if not carpeta.is_dir():
        return []
    return sorted(carpeta.glob('peticiones-*.json'), key=lambda p: p.name, reverse=True)


def nombre_estado(t: dict) -> str:
    e = t.get('estado')
    return {'en-cola': 'en cola', 'en-curso': 'en curso', 'en-observacion': 'en observación', 'descartada': 'descartada',
            'cerrada': 'cerrada', 'eliminada': 'eliminada', 'absorbida': 'absorbida',
            'revertida': 'revertida'}.get(e, f'«{e}»')


def situacion(t: dict) -> str:
    """Por qué salió de la cola: el último evento de salida de su historial."""
    for e in reversed(t.get('historial', [])):
        if e.get('evento') in ('cerrada', 'eliminada', 'absorbida', 'limpiada', 'revertida'):
            return {'cerrada': 'cerrada', 'eliminada': 'eliminada',
                    'absorbida': 'absorbida', 'limpiada': 'descartada y limpiada', 'revertida': 'revertida'}[e['evento']]
    return 'fuera de la cola'


def ultimo_evento(t: dict) -> str | None:
    h = t.get('historial') or []
    return h[-1].get('evento') if h else None


def pasos(t: dict) -> list:
    p = t.get('pasos')
    if not isinstance(p, list):
        p = t['pasos'] = []
    return p


def paso(t: dict, i: int) -> dict:
    p = pasos(t)
    if not 1 <= i <= len(p):
        raise Rechazo(f'La {t["id"]} no tiene paso {i}: tiene {len(p)}.')
    return p[i - 1]


def es_de_cierre(texto) -> bool:
    return isinstance(texto, str) and texto.strip() in PASOS_CIERRE


def es_ayuda(x) -> bool:
    """Una ayuda de prueba («paso añadir N texto --prueba»): va entre «Activar rama para poder probar» y «Cerrar la
    tarea» y no la exige ningún cierre (decisión 184)."""
    return isinstance(x, dict) and x.get('ayuda') is True and not es_de_cierre(x.get('texto'))


def es_deliberativa(t: dict) -> bool:
    return t.get('tipo') in DELIBERATIVAS


def pasos_cierre(t: dict) -> tuple:
    """Los pasos de cierre de la tarea: los dos (174) o, en una deliberativa sin rama, que no se prueba (218, 278),
    solo «Cerrar la tarea»."""
    return PASOS_CIERRE[1:] if es_deliberativa(t) and not t.get('rama') else PASOS_CIERRE


def asegurar_cierre(t: dict) -> list:
    """Deja los pasos de cierre al final, una vez cada uno y en su orden (decisión 174), con las ayudas de prueba entre
    los dos (decisión 184): el que falta, pendiente; uno repetido se quita y queda el primero, con su estado. Una
    deliberativa sin rama no lleva «Activar rama para poder probar» (278): si lo tiene, se quita. Devuelve los avisos de
    lo que ha arreglado (tarea 253)."""
    p = pasos(t)
    cierre = pasos_cierre(t)
    habia = [x for x in p if es_de_cierre(x.get('texto'))]
    ayudas = [x for x in p if es_ayuda(x)]
    p[:] = [x for x in p if not es_de_cierre(x.get('texto')) and not es_ayuda(x)]
    avisos, faltan = [], []
    if PASO_PROBAR not in cierre:
        p.extend(ayudas)
    for nombre in cierre:
        mismos = [x for x in habia if x.get('texto').strip() == nombre]
        if len(mismos) > 1:
            avisos.append(f'«{nombre}» estaba {len(mismos)} veces: queda una')
        if not mismos:
            faltan.append(nombre)
        p.append({'texto': nombre, 'estado': mismos[0].get('estado', 'pendiente') if mismos else 'pendiente'})
        if nombre == PASO_PROBAR:
            p.extend(ayudas)
    if faltan:
        avisos.append(f'faltaba{"n" if len(faltan) > 1 else ""} {enumerar([f"«{x}»" for x in faltan])}: '
                      f'añadido{"s" if len(faltan) > 1 else ""}')
    return avisos


def probar_otra_vez(t: dict) -> bool:
    """Un paso de trabajo nuevo vuelve a dejar pendiente «Activar rama para poder probar», si estaba hecho: hay que
    probar otra vez (decisión 174). Dice si lo ha cambiado."""
    cambiado = False
    for x in pasos(t):
        if x.get('texto') == PASO_PROBAR and x.get('estado') == 'hecho':
            x['estado'] = 'pendiente'
            cambiado = True
    return cambiado


def a_en_curso(t: dict) -> None:
    """La tarea pasa a en curso con sus pasos de cierre, pendientes (decisión 174)."""
    t['estado'] = 'en-curso'
    asegurar_cierre(t)
    cierre_pendiente(t)


def enumerar(lista: list) -> str:
    lista = [str(x) for x in lista]
    return lista[0] if len(lista) == 1 else ', '.join(lista[:-1]) + ' y ' + lista[-1]


# ---------- git ----------

def git(repo: Path, *args: str, entrada: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(['git', '-C', str(repo), *args], input=entrada, capture_output=True,
                          text=True, encoding='utf-8', errors='replace')


def linea_de_motivo(texto: str) -> str:
    """La línea que explica un error de git: la primera «fatal:» o «error:» (sin remoto, «fatal: 'origin' does not
    appear to be a git repository», no la última, «and the repository exists.»); si no hay, la última."""
    lineas = [x.strip() for x in texto.strip().splitlines() if x.strip()]
    if not lineas:
        return 'git no responde'
    return next((x for x in lineas if re.match(r'(fatal|error):', x, re.I)), lineas[-1])


def motivo(r: subprocess.CompletedProcess) -> str:
    return linea_de_motivo(r.stderr or r.stdout or '')


def rama_activa(repo: Path) -> str | None:
    r = git(repo, 'symbolic-ref', '--short', '-q', 'HEAD')
    return r.stdout.strip() if r.returncode == 0 else None


def existe_rama(repo: Path, rama: str) -> bool:
    return git(repo, 'show-ref', '--verify', '--quiet', f'refs/heads/{rama}').returncode == 0


def worktree_ajeno(repo: Path, rama: str) -> str | None:
    """La ruta del worktree de otro agente que tiene `rama` activa, o None."""
    if rama_activa(repo) == rama:
        return None
    r = git(repo, 'worktree', 'list', '--porcelain')
    if r.returncode != 0:
        raise Rechazo(f'git no responde ({motivo(r)}).')
    for bloque in re.split(r'\n\s*\n', r.stdout.replace('\r\n', '\n')):
        if f'branch refs/heads/{rama}' in bloque.split('\n'):
            m = re.search(r'^worktree (.+)$', bloque, re.M)
            return m.group(1) if m else '?'
    return None


def exigir_limpio(repo: Path, donde: str) -> None:
    r = git(repo, 'status', '--porcelain', '--untracked-files=no')
    if r.returncode != 0:
        raise Rechazo(f'git no responde ({motivo(r)}).')
    if r.stdout.strip():
        raise Rechazo(f'Hay cambios sin commit en {donde}. Haz commit antes.')


def a_develop(repo: Path) -> str | None:
    """Pasa a develop si no es la activa; devuelve la rama de antes."""
    antes = rama_activa(repo)
    if antes != 'develop':
        r = git(repo, 'switch', 'develop')
        if r.returncode != 0:
            raise Rechazo(f'No se pudo pasar a develop: {motivo(r)}')
    return antes


def nombre_rama(id_: int, nombre: str) -> str:
    return nombre if nombre.startswith('feature/') else f'feature/{id_}-{nombre}'


def crear_rama(repo: Path, rama: str, activar: bool) -> None:
    if not existe_rama(repo, 'develop'):
        raise Rechazo('No hay rama develop.')
    if existe_rama(repo, rama):
        raise Rechazo(f'La rama {rama} ya existe.')
    r = git(repo, 'switch', '-c', rama, 'develop') if activar else git(repo, 'branch', rama, 'develop')
    if r.returncode != 0:
        raise Rechazo(f'No se pudo crear {rama}: {motivo(r)}')


class Fallo(Exception):
    """Un cierre que no sale: queda en el historial de la tarea. `tipo`: choques o commit."""

    def __init__(self, motivo: str, tipo: str):
        super().__init__(motivo)
        self.tipo = tipo


def sin_cambios(repo: Path, rama: str) -> bool:
    """La rama no trae nada a develop: sin diferencias desde su base común con develop (tarea 345)."""
    return existe_rama(repo, 'develop') and git(repo, 'diff', '--quiet', f'develop...{rama}', '--').returncode == 0


def squash(cola: Cola, t: dict, coautor: str | None = None) -> tuple[str | None, str | None, str | None]:
    """Pasa la rama de la tarea a develop por squash. Devuelve (hash, error del push, error al borrar la rama). Una
    rama sin cambios respecto a develop no da commit: se borra y el hash es None (tarea 345; antes, el commit fallaba
    con «nothing added to commit»)."""
    repo, rama, id_ = cola.repo, t['rama'], t['id']
    if not existe_rama(repo, rama):
        raise Rechazo(f'La rama {rama} no existe.')
    ajeno = worktree_ajeno(repo, rama)
    if ajeno:
        raise Rechazo(f'La rama {rama} está en el worktree {ajeno}. Para ese agente y quita el worktree antes.')
    if sin_cambios(repo, rama):
        if rama_activa(repo) == rama:
            exigir_limpio(repo, rama)
            a_develop(repo)
        borrado = git(repo, 'branch', '-D', rama)
        return None, None, (motivo(borrado) if borrado.returncode else None)
    exigir_limpio(repo, rama_activa(repo) or 'la rama activa')
    antes = a_develop(repo)

    def deshacer() -> None:
        git(repo, 'reset', '--merge')
        if antes and antes != 'develop':
            git(repo, 'switch', antes)

    r = git(repo, 'merge', '--squash', rama)
    if r.returncode != 0:
        choques = git(repo, 'diff', '--name-only', '--diff-filter=U').stdout.split()
        deshacer()
        raise Fallo(f'choques en el merge de {rama}' + (f': {", ".join(choques)}' if choques else ''), 'choques')
    if git(repo, 'diff', '--cached', '--quiet').returncode == 0:  # lo suyo ya estaba en develop: nada que commitear
        git(repo, 'reset', '-q', '--merge')
        borrado = git(repo, 'branch', '-D', rama)
        return None, None, (motivo(borrado) if borrado.returncode else None)
    hechos = [p['texto'] for p in pasos(t) if p.get('estado') == 'hecho' and p.get('texto') not in PASOS_CIERRE
              and not es_ayuda(p)]
    cuerpo = ''.join(f'- {x}\n' for x in hechos)
    conf = configuracion(repo)
    mensaje = mensaje_de_tarea(t['texto'], cuerpo, id_, conf['commits'], t.get('tipo'), coautor or conf['coautor'])
    r = git(repo, 'commit', '-q', '-F', '-', entrada=mensaje)
    if r.returncode != 0:
        deshacer()
        raise Fallo(f'falló el commit ({motivo(r)})', 'commit')
    hash_ = git(repo, 'rev-parse', '--short', 'HEAD').stdout.strip()
    push = subir_develop(repo, conf['remoto'])
    borrado = git(repo, 'branch', '-D', rama)
    return hash_, push, (motivo(borrado) if borrado.returncode else None)


def hashes_de(t: dict) -> list:
    """Los commits de la tarea en develop sin revertir, según su historial, el más reciente primero."""
    hechos, revertidos = [], set()
    for e in t.get('historial', []):
        m = re.match(r'develop ([0-9a-f]{4,40})', e.get('detalle') or '')
        if e.get('evento') in ('cerrada', 'a-observacion') and m:
            hechos.append(m.group(1))
        if e.get('evento') == 'revertida':
            revertidos.update(re.findall(r'[0-9a-f]{7,40}', (e.get('detalle') or '').partition('revierte')[2]))
    return [h for h in reversed(hechos) if h not in revertidos]


# git log de develop para buscar los commits de cada tarea: hash corto, título y el trailer SF-Tarea.
FORMATO_LOG = f'--format=%h%x09%s%x09%(trailers:key={TRAILER_TAREA},valueonly,separator=%x2C)'


def tareas_en_develop(lineas: list) -> dict:
    """Por número de tarea, sus commits en develop sin revertir, el más reciente primero, de las líneas de
    FORMATO_LOG (las más recientes primero). El número sale de «(N)» al final del título o del trailer
    «SF-Tarea: N» (decisión 207). Un «Revert "<título>"» deja fuera los commits de la tarea más antiguos que él: el
    de un título «… (N)» nombra la tarea; si no, la del commit más cercano, por debajo, con ese título."""
    filas = []
    for linea in lineas:
        h, _, resto = linea.partition('\t')
        titulo, _, trailer = resto.partition('\t')
        titulo, h = titulo.strip(), h.strip()
        if not h or not titulo:
            continue
        m = re.search(r' \((\d+)\)$', titulo)
        n = int(m.group(1)) if m else next((int(x) for x in re.findall(r'\d+', trailer)), None)
        filas.append((h, titulo, n))
    corte = {}
    for i, (_, titulo, _) in enumerate(filas):
        rv = re.match(r'^Revert "(.*)"$', titulo)
        if not rv:
            continue
        m = re.search(r' \((\d+)\)$', rv.group(1))
        n = int(m.group(1)) if m else next((x[2] for x in filas[i + 1:] if x[1] == rv.group(1)), None)
        if n is not None:
            corte.setdefault(n, i)
    salida = {}
    for i, (h, titulo, n) in enumerate(filas):
        if n is None or titulo.startswith('Revert "') or i > corte.get(n, len(filas)):
            continue
        salida.setdefault(n, []).append(h)
    return salida


def hashes_en_develop(repo: Path, id_: int) -> list:
    """Como el panel: los commits de la tarea en develop, «… (N)» o con «SF-Tarea: N», sin un revert posterior, el
    más reciente primero."""
    r = git(repo, 'log', 'develop', '--first-parent', '--max-count=1000', FORMATO_LOG)
    if r.returncode != 0:
        return []
    return tareas_en_develop(r.stdout.splitlines()).get(id_, [])


# ---------- Recogida de los subagentes (tarea 246) ----------

def subagentes_de(t: dict) -> list:
    """Los (worktree, rama auxiliar o None) anotados para los subagentes de la tarea desde su última recogida
    completa, sin repetir, por orden: los ya recogidos no se vuelven a mirar; tras una con avisos, sí."""
    salida = []
    for e in t.get('historial', []):
        if e.get('evento') == 'recogida':
            salida = []
        if e.get('evento') != 'subagente' or not (e.get('detalle') or '').strip():
            continue
        wt, _, aux = e['detalle'].rpartition(' · ') if ' · ' in e['detalle'] else (e['detalle'], '', '')
        par = (wt.strip(), aux.strip() or None)
        if par not in salida:
            salida.append(par)
    return salida


def misma_ruta(a, b) -> bool:
    """La misma carpeta: igual escrita (sin distinguir mayúsculas en Windows) o igual tras resolver los enlaces, como
    /var y /private/var en macOS, donde git puede dar la ruta resuelta de un worktree."""
    def forma(x, f):
        return os.path.normcase(f(str(x)))
    return forma(a, os.path.abspath) == forma(b, os.path.abspath) or forma(a, os.path.realpath) == forma(b, os.path.realpath)


def lista_worktrees(repo: Path) -> list:
    """Los worktrees de git del repositorio: [(ruta, rama o None)]; el primero es el principal."""
    r = git(repo, 'worktree', 'list', '--porcelain')
    salida = []
    for bloque in re.split(r'\n\s*\n', r.stdout.replace('\r\n', '\n')) if r.returncode == 0 else []:
        w = re.search(r'^worktree (.+)$', bloque, re.M)
        b = re.search(r'^branch refs/heads/(.+)$', bloque, re.M)
        if w:
            salida.append((Path(w.group(1)), b.group(1) if b else None))
    return salida


def sin_integrar_de(repo: Path, t: dict) -> dict:
    """Por cada rama auxiliar que existe, los commits que no están en develop ni en la rama de la tarea. Se mira
    antes del squash, que borra la rama de la tarea y deja en develop su contenido, no sus commits."""
    salida = {}
    rama = t.get('rama')
    auxiliares = [aux for _, aux in subagentes_de(t)]
    if t.get('id') is not None and f'sub-{t["id"]}' not in auxiliares:  # la sub-N sin anotar, también
        auxiliares.append(f'sub-{t["id"]}')
    for aux in auxiliares:
        if not aux or aux == rama or not existe_rama(repo, aux):
            continue
        fuera = ['develop'] + ([rama] if rama and existe_rama(repo, rama) else [])
        r = git(repo, 'rev-list', '--count', aux, '--not', *fuera)
        if r.returncode == 0 and r.stdout.strip().isdigit():
            salida[aux] = 0 if en_develop_por_contenido(repo, aux) else int(r.stdout.strip())
    return salida


def en_develop_por_contenido(repo: Path, aux: str, base: str = 'develop') -> bool:
    """Si fusionar `aux` en `base` no cambiaría nada: su trabajo ya entró, por squash (sin sus commits). Pide git
    2.38 o posterior (merge-tree --write-tree); con uno anterior, o con choques, no."""
    r = git(repo, 'merge-tree', '--write-tree', base, aux)
    arbol = git(repo, 'rev-parse', f'{base}^{{tree}}')
    return r.returncode == 0 and arbol.returncode == 0 and r.stdout.split()[:1] == [arbol.stdout.strip()]


def fuera_de(repo: Path, aux: str, destino: str) -> int:
    """Los commits de `aux` que no están en `destino` ni en develop, ni entraron en ellos por squash."""
    bases = [b for b in dict.fromkeys([destino, 'develop']) if existe_rama(repo, b)]
    r = git(repo, 'rev-list', '--count', aux, '--not', *bases)
    if r.returncode or not r.stdout.strip().isdigit():
        return 0
    n = int(r.stdout.strip())
    return 0 if n and any(en_develop_por_contenido(repo, aux, b) for b in bases) else n


def recoger_subagentes(repo: Path, t: dict, sin_integrar: dict, destino: str | None = None, pares: list | None = None,
                       forzar: bool = False) -> tuple[list, list]:
    """Quita los worktrees y borra las ramas auxiliares de los subagentes de la tarea, sin forzar: un worktree con
    cambios sin commit queda, y con él su rama; una auxiliar con commits que no entraron (`sin_integrar`), también,
    con su worktree. Con `destino` (fusionar), solo si la auxiliar ya está en esa rama: si
    no, quedan las dos. Con `forzar` (reabrir), también con cambios sin commit. Devuelve (lo quitado, los avisos). No
    falla: lo que no sale, se avisa."""
    quitados, avisos = [], []
    rama = t.get('rama')
    for wt, aux in (subagentes_de(t) if pares is None else pares):
        if destino and aux and aux != rama and existe_rama(repo, aux):
            n = fuera_de(repo, aux, destino)
            if n:
                avisos.append(f'quedan {wt or "su worktree"} y {aux}: {aux} tiene {n} commit{"s" if n > 1 else ""} '
                              f'que no {"están" if n > 1 else "está"} en {destino}')
                continue
        n = sin_integrar.get(aux, 0) if aux and aux != rama and existe_rama(repo, aux) else 0
        if n:  # sus commits no entraron: quedan la rama y su worktree, nunca se borran (decisión 169)
            avisos.append(f'quedan {wt or "su worktree"} y {aux}: {aux} tiene {n} commit{"s" if n > 1 else ""} '
                          f'que no entr{"aron" if n > 1 else "ó"} en develop')
            continue
        ruta = (Path(wt) if Path(wt).is_absolute() else repo / wt) if wt else None
        registrados = lista_worktrees(repo)
        principal = registrados[0][0] if registrados else repo
        en_git = next((p for p, _ in registrados if misma_ruta(p, ruta)), None) if ruta else None
        if en_git is None and aux:  # la auxiliar, activa en otro worktree que no es el anotado
            en_git = next((p for p, b in registrados[1:] if b == aux), None)
        queda_wt = False
        if (ruta and (misma_ruta(ruta, repo) or misma_ruta(ruta, principal))) or (en_git is not None and misma_ruta(en_git, principal)):
            avisos.append(f'no se quita {wt}: es la carpeta del proyecto')
            queda_wt = True
        elif en_git is not None and not en_git.is_dir():
            git(repo, 'worktree', 'prune')
            quitados.append(en_git.as_posix())
        elif en_git is not None:
            sucio = None if forzar else git(en_git, 'status', '--porcelain')
            if sucio and sucio.returncode == 0 and sucio.stdout.strip():
                avisos.append(f'queda el worktree {en_git.as_posix()}: tiene cambios sin commit')
                queda_wt = True
            else:
                r = git(repo, 'worktree', 'remove', *(['--force', '--force'] if forzar else []), str(en_git))
                if r.returncode:
                    avisos.append(f'queda el worktree {en_git.as_posix()} ({motivo(r)})')
                    queda_wt = True
                else:
                    quitados.append(en_git.as_posix())
        elif ruta and ruta.is_dir():
            avisos.append(f'queda la carpeta {wt}: no es un worktree de git')
        if not aux or aux == rama or not existe_rama(repo, aux):
            continue
        if queda_wt or any(b == aux for _, b in lista_worktrees(repo)):
            avisos.append(f'queda la rama {aux}: su worktree sigue')
            continue
        r = git(repo, 'branch', '-D', aux)
        if r.returncode:
            avisos.append(f'no se pudo borrar {aux} ({motivo(r)})')
            continue
        quitados.append(aux)
    return quitados, avisos


def recogida(cola: Cola, t: dict, sin_integrar: dict, destino: str | None = None, pares: list | None = None,
             forzar: bool = False) -> str:
    """Recoge los subagentes de una tarea que se queda sin ellos (decisión 169: cerrar, a observación, descartar,
    eliminar, revertir, limpiar, reabrir, forzando, y las absorbidas al fusionar), después del squash o del borrado de
    su rama, y lo anota: «recogida» (lo quitado) si todo salió, o «recogida-con-avisos» (lo que queda o se perdió),
    que el panel pasa a Claude. Devuelve el trozo del mensaje; sin subagentes, nada."""
    pares = subagentes_de(t) if pares is None else pares
    if not pares:
        return ''
    quitados, avisos = recoger_subagentes(cola.repo, t, sin_integrar, destino, pares, forzar)
    if avisos:
        cola.anotar(t, 'recogida-con-avisos', '; '.join(avisos))
    else:
        cola.anotar(t, 'recogida', ', '.join(quitados) or 'nada que quitar')
    hecho = f' Quitados: {", ".join(quitados)}.' if quitados else ''
    return hecho + ''.join(f' Aviso: {x}.' for x in avisos)


# ---------- Órdenes ----------

def o_lista(cola: Cola, a) -> str:
    if not cola.tareas:
        return 'Cola vacía.'
    return '\n'.join(f'{t.get("id")}\t{nombre_estado(t)}{" · la mira el propietario" if t.get("observando") else ""}'
                     f'{" · " + t["rama"] if t.get("rama") else ""}{cuenta_pasos(t)}\t{t.get("texto")}'
                     for t in cola.tareas)


def cuenta_pasos(t: dict) -> str:
    """« · pasos H/T»: hechos y total de los pasos de trabajo, sin los de cierre ni las ayudas de prueba. Con cada
    mensaje el principal mira la lista; así ve qué tarea crece y valora sugerir partirla o cerrar lo hecho (decisión
    235). Solo cuenta: cuándo sugerirlo lo decide el criterio del principal."""
    p = t.get('pasos')
    trabajo = [x for x in p if isinstance(x, dict) and x.get('texto') not in PASOS_CIERRE and not es_ayuda(x)] \
        if isinstance(p, list) else []
    if not trabajo:
        return ''
    return f' · pasos {sum(x.get("estado") == "hecho" for x in trabajo)}/{len(trabajo)}'


def o_ver(cola: Cola, a) -> str:
    t = cola.buscar(a.n) or cola.archivadas().get(a.n)
    if t is None:
        raise Rechazo(f'La {a.n} no está en la cola ni en el historial.')
    # Cada paso, con su número «n», desde 1: el que piden «paso marcar» y «paso quitar» (tarea 253). Solo en lo que
    # se muestra; la cola no lo guarda.
    if isinstance(t.get('pasos'), list):
        t = {**t, 'pasos': [{'n': i, **x} if isinstance(x, dict) else x for i, x in enumerate(t['pasos'], 1)]}
    return json.dumps(t, ensure_ascii=False, indent=2)


def exigir_descripcion(cola: Cola, a, orden: str) -> None:
    """La tarea que crea Claude lleva descripción: es lo que el panel enseña al desplegarla (tarea 326). La que crea
    el propietario, o llega por el panel, puede ir sin ella."""
    if cola.quien == 'principal' and cola.via != 'panel' and not (a.descripcion or '').strip():
        raise Rechazo(f'La tarea que crea Claude necesita descripción: qué se pide y por qué, en una o dos frases. '
                      f'Pásala con --descripcion: {orden} "{a.texto.strip()}" --descripcion "…".')


def o_crear(cola: Cola, a) -> str:
    id_ = cola.siguiente()
    t = {'id': id_, 'texto': a.texto.strip(), 'estado': 'en-curso' if a.en_curso else 'en-cola'}
    if not t['texto']:
        raise Rechazo('La tarea necesita un texto.')
    exigir_descripcion(cola, a, 'crear')
    if (a.descripcion or '').strip():
        t['descripcion'] = a.descripcion.strip()
    if a.tipo:
        t['tipo'] = a.tipo
    if a.en_curso:
        a_en_curso(t)
    cola.anotar(t, 'creada', t['estado'])
    cola.tareas.append(t)
    cola.datos['ultimo'] = id_
    cola.guardar()
    cola.extra['id'] = id_
    return f'Creada la {id_}, {nombre_estado(t)}: «{t["texto"]}».'


def o_en_curso(cola: Cola, a) -> str:
    t = cola.tarea(a.n, 'en-cola')
    a_en_curso(t)
    cola.anotar(t, 'en-curso')
    cola.guardar()
    return f'La {a.n}, en curso.'


def propios(repo: Path, rama: str) -> int:
    """Los commits de `rama` que no están en develop (sin develop, todos los suyos)."""
    r = git(repo, 'rev-list', '--count', rama, *(['--not', 'develop'] if existe_rama(repo, 'develop') else []))
    return int(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip().isdigit() else 0


def worktrees_sucios(repo: Path, t: dict) -> list:
    """Los worktrees de los subagentes de la tarea que siguen en git y tienen cambios sin commit."""
    registrados = lista_worktrees(repo)[1:]
    sucios = []
    for wt, aux in subagentes_de(t):
        ruta = (Path(wt) if Path(wt).is_absolute() else repo / wt) if wt else None
        en_git = next((p for p, _ in registrados if ruta and misma_ruta(p, ruta)), None)
        if en_git is None and aux:
            en_git = next((p for p, b in registrados if b == aux), None)
        if en_git is not None and en_git.is_dir():
            r = git(en_git, 'status', '--porcelain')
            if r.returncode == 0 and r.stdout.strip() and en_git.as_posix() not in sucios:
                sucios.append(en_git.as_posix())
    return sucios


def o_en_cola(cola: Cola, a) -> str:
    """Una en curso vuelve a la cola si no tiene trabajo: sin rama, con la rama ya borrada o con una rama sin commits
    propios respecto a develop, que se borra; y lo de su subagente, también vacío, se recoge como al cerrar. Con
    commits propios, en su rama o en una auxiliar, o con cambios sin commit en un worktree, se niega (decisión 170,
    tarea 275): para dejarla, se cierra, se pasa a observación o se descarta."""
    t = cola.tarea(a.n, 'en-curso')
    repo, rama = cola.repo, t.get('rama')
    viva = bool(rama) and existe_rama(repo, rama)
    n = propios(repo, rama) if viva else 0
    if n:  # decisión 170
        raise Rechazo(f'La {a.n} tiene rama ({rama}) con {n} commit{"s" if n > 1 else ""} que no '
                      f'{"están" if n > 1 else "está"} en develop: una tarea en curso con trabajo en su rama no vuelve '
                      f'a la cola. Para dejarla, ciérrala, pásala a observación o descártala.')
    sin_integrar = sin_integrar_de(repo, t)
    falta = {aux: k for aux, k in sin_integrar.items() if k}
    if falta:
        lista = enumerar([f'{aux} ({k} commit{"s" if k > 1 else ""})' for aux, k in falta.items()])
        raise Rechazo(f'La {a.n} tiene trabajo de su subagente que no está en develop: {lista}. No vuelve a la cola: '
                      f'ciérrala, pásala a observación o descártala.')
    sucios = worktrees_sucios(repo, t)
    if sucios:
        raise Rechazo(f'La {a.n} tiene cambios sin commit en {enumerar(sucios)}: no vuelve a la cola. Haz commit o '
                      f'descártalos antes, o descarta la tarea.')
    activa = False
    if viva:
        ajeno = worktree_ajeno(repo, rama)
        if ajeno:
            raise Rechazo(f'La rama {rama} está en el worktree {ajeno}. Para ese agente y quita el worktree antes.')
        activa = rama_activa(repo) == rama
        if activa:
            exigir_limpio(repo, rama)
            a_develop(repo)
        r = git(repo, 'branch', '-D', rama)
        if r.returncode != 0:
            raise Rechazo(f'No se pudo borrar {rama}: {motivo(r)}')
        cola.cargar()
        t = cola.tarea(a.n)
    recogido = recogida(cola, t, sin_integrar)
    t.pop('rama', None)
    t['estado'] = 'en-cola'
    cola.anotar(t, 'en-cola', (f'sin la rama {rama}: ' + ('borrada, sin commits propios' if viva else 'ya no existía'))
                if rama else None)
    cola.guardar()
    return (f'La {a.n}, en cola' + (f'; rama {rama} {"borrada: no tenía commits propios" if viva else "quitada: ya no existía"}'
                                    if rama else '') + '.' + (' Activa: develop.' if activa else '') + recogido)


def sin_rama_deliberativa(t: dict) -> str:
    """Por qué una deliberativa no lleva rama (256, 278), para los rechazos."""
    return (f'La {t["id"]} es de {t["tipo"]}, deliberativa: no tiene rama, worktree ni rama auxiliar; solo escribe su '
            f'documento, que va directo a develop en cada vuelta, y lo demás va a tareas propias con rama (decisiones '
            f'256 y 278). Si no es deliberativa, cámbiale el tipo con «tipo {t["id"]} T».')


def o_rama(cola: Cola, a) -> str:
    t = cola.tarea(a.n, 'en-curso')
    if t.get('rama'):
        raise Rechazo(f'La {a.n} ya tiene rama: {t["rama"]}.')
    if es_deliberativa(t):
        raise Rechazo(sin_rama_deliberativa(t))
    rama = nombre_rama(a.n, a.nombre)
    if a.anotar:
        if not existe_rama(cola.repo, rama):
            raise Rechazo(f'La rama {rama} no existe.')
    else:
        crear_rama(cola.repo, rama, activar=not a.sin_activar)
    t['rama'] = rama
    cola.anotar(t, 'rama', rama)
    cola.guardar()
    return f'Rama {rama} de la {a.n}' + (', anotada.' if a.anotar else ', creada sin activar.' if a.sin_activar else ', activa.')


def o_paso_anadir(cola: Cola, a) -> str:
    # También en observación: la que el propietario está mirando recibe pasos con /sf_paso (decisión del propietario, 2026-10-28).
    t = cola.tarea(a.n, 'en-cola', 'en-curso', 'en-observacion')
    p = pasos(t)
    nuevo = {'texto': a.texto.strip(), 'estado': 'pendiente'}
    if not nuevo['texto']:
        raise Rechazo('El paso necesita un texto.')
    if es_de_cierre(nuevo['texto']):
        raise Rechazo(f'«{nuevo["texto"]}» es un paso de cierre: la tarea lo lleva desde que entra en curso.')
    if a.prueba:
        # Una ayuda de prueba, antes de «Cerrar la tarea»: no exige nada ni devuelve la rama a pendiente (decisión 184).
        nuevo['ayuda'] = True
        sitio = next((i for i, x in enumerate(p) if x.get('texto') == PASOS_CIERRE[1]), len(p))
        p.insert(sitio, nuevo)
        cola.anotar(t, 'paso', f'ayuda de prueba {sitio + 1}: {nuevo["texto"]}')
        cola.guardar()
        return f'Ayuda de prueba {sitio + 1} de {len(p)} de la {a.n}, sin exigirla para cerrar: «{nuevo["texto"]}».'
    sitio = next((i for i, x in enumerate(p) if es_de_cierre(x.get('texto')) or es_ayuda(x)), len(p))
    p.insert(sitio, nuevo)
    cola.anotar(t, 'paso', f'añadido {sitio + 1}: {nuevo["texto"]}')
    otra_vez = probar_otra_vez(t)
    cola.guardar()
    return (f'Paso {sitio + 1} de {len(p)} de la {a.n}: «{nuevo["texto"]}».'
            + (f' «{PASO_PROBAR}», otra vez pendiente: hay que probar de nuevo.' if otra_vez else ''))


def o_paso_marcar(cola: Cola, a) -> str:
    t = cola.tarea(a.n)
    x = paso(t, a.i)
    texto = a.texto.strip() if a.texto else None
    if texto and texto != x.get('texto'):
        # Un paso de cierre reescrito deja de serlo (tarea 253).
        if es_de_cierre(x.get('texto')):
            raise Rechazo(f'El paso {a.i} de la {a.n} es «{x["texto"]}», de cierre: no cambia de texto. '
                          f'¿Era otro? Los pasos cuentan desde 1; míralos con «ver {a.n}».')
        if es_de_cierre(texto):
            raise Rechazo(f'«{texto}» es un paso de cierre: la tarea lo lleva desde que entra en curso.')
        x['texto'] = texto
    x['estado'] = a.estado
    cola.anotar(t, 'paso', f'{a.i} {a.estado}: {x["texto"]}')
    cola.guardar()
    return f'Paso {a.i} de {len(pasos(t))} de la {a.n}, {a.estado}: «{x["texto"]}».'


def o_paso_quitar(cola: Cola, a) -> str:
    t = cola.tarea(a.n)
    x = paso(t, a.i)
    if es_de_cierre(x.get('texto')):
        raise Rechazo(f'«{x["texto"]}» es un paso de cierre: no se quita (decisión 174). '
                      f'Cerrar no pide «{PASO_PROBAR}»: lo marca al cerrar.')
    if x.get('estado') != 'pendiente':
        raise Rechazo(f'El paso {a.i} de la {a.n} está {x.get("estado")}: solo se quita uno pendiente.')
    pasos(t).pop(a.i - 1)
    cola.anotar(t, 'paso', f'quitado {a.i}: {x.get("texto")}')
    cola.guardar()
    return f'Quitado el paso {a.i} de la {a.n}: «{x.get("texto")}».'


def o_renombrar(cola: Cola, a) -> str:
    t = cola.tarea(a.n)
    if not a.texto.strip():
        raise Rechazo('La tarea necesita un texto.')
    antes, t['texto'] = t.get('texto'), a.texto.strip()
    cola.anotar(t, 'renombrada', f'antes: {antes}')
    cola.guardar()
    return f'La {a.n} se llama «{t["texto"]}».'


def o_tipo(cola: Cola, a) -> str:
    t = cola.tarea(a.n)
    antes = t.get('tipo')
    if antes == a.tipo:
        raise Rechazo(f'La {a.n} ya es de tipo {a.tipo}.')
    t['tipo'] = a.tipo
    cola.anotar(t, 'tipo', a.tipo + (f' (antes: {antes})' if antes else ''))
    aviso = ''
    if t.get('estado') == 'en-curso':
        # Una deliberativa sin rama no lleva «Activar rama para poder probar»; las demás, sí (278).
        tenia = any(x.get('texto') == PASO_PROBAR for x in pasos(t))
        asegurar_cierre(t)
        tiene = any(x.get('texto') == PASO_PROBAR for x in pasos(t))
        if tenia != tiene:
            aviso = f' «{PASO_PROBAR}», {"añadido" if tiene else "quitado: una deliberativa no se prueba"}.'
    if es_deliberativa(t) and t.get('rama'):
        aviso += (f' Tiene rama ({t["rama"]}), de antes: se cierra con su squash, o sin commit si no tiene cambios; '
                  f'una deliberativa nueva no lleva rama (278).')
    cola.guardar()
    return f'La {a.n}, de tipo {a.tipo}.' + aviso


def o_redescribir(cola: Cola, a) -> str:
    t = cola.tarea(a.n)
    # Sin guardar la anterior en el historial (decisión del propietario, 2026-10-30).
    t['descripcion'] = a.texto.strip()
    if not t['descripcion']:
        del t['descripcion']
    cola.anotar(t, 'redescrita')
    cola.guardar()
    return f'La {a.n}, con su descripción nueva.'


def o_subagente(cola: Cola, a) -> str:
    t = cola.tarea(a.n, 'en-curso')
    if es_deliberativa(t) and not t.get('rama'):
        raise Rechazo(sin_rama_deliberativa(t) + ' Su subagente se lanza sin anotarlo: «encargo» no lo pide.')
    cola.anotar(t, 'subagente', a.worktree + (f' · {a.rama}' if a.rama else ''))
    cola.guardar()
    return f'Subagente en la {a.n}: {a.worktree}.'


def o_informe(cola: Cola, a) -> str:
    t = cola.tarea(a.n)
    fin = 'terminado' if a.terminado else 'interrumpido'
    cola.anotar(t, 'informe', fin + (f': {a.texto}' if a.texto else ''))
    cola.guardar()
    return f'Informe del subagente de la {a.n}: {fin}.'


def cierre_pendiente(t: dict) -> None:
    """Una tarea que vuelve a trabajarse tiene sin hacer los dos pasos de cierre."""
    for x in pasos(t):
        if x.get('texto') in PASOS_CIERRE:
            x['estado'] = 'pendiente'


def o_listo(cola: Cola, a) -> str:
    t = cola.tarea(a.n, 'en-curso')
    # Solo guarda el «qué mirar» (decisión 174). Una tarea de antes, sin los pasos de cierre o con uno repetido, se
    # arregla aquí, y se avisa.
    avisos = asegurar_cierre(t)
    t['prueba'] = a.prueba
    cola.anotar(t, 'listo', a.prueba)
    cola.guardar()
    return f'La {a.n}, lista para probar: {a.prueba}' + ''.join(f' Aviso: {x}.' for x in avisos)


def o_comprobado(cola: Cola, a) -> str:
    # Un paso hecho, en una sola orden y sin volver a pedir la prueba (decisión 288).
    t = cola.tarea(a.n, 'en-cola', 'en-curso', 'en-observacion')
    if not a.texto.strip():
        raise Rechazo('Lo comprobado necesita un texto, con su resultado.')
    i = anadir_comprobado(t, a.texto)
    texto = pasos(t)[i - 1]['texto']
    cola.anotar(t, 'comprobado', f'{i}: {texto}')
    cola.guardar()
    return f'Paso {i} de {len(pasos(t))} de la {a.n}, hecho: «{texto}».'


def auxiliares_de(repo: Path, t: dict) -> list:
    """Las ramas auxiliares que existen de los subagentes de la tarea, con su worktree o None: las anotadas y, si
    existe, la sub-N de siempre."""
    rama = t.get('rama')
    auxs = [aux for _, aux in subagentes_de(t) if aux] + [f'sub-{t["id"]}']
    en_wt = {b: p for p, b in lista_worktrees(repo)[1:] if b}
    return [(aux, en_wt.get(aux)) for aux in dict.fromkeys(auxs) if aux != rama and existe_rama(repo, aux)]


def sin_traer(repo: Path, t: dict) -> dict:
    """Por cada rama auxiliar, los commits que aún no están en la rama de la tarea (ni en develop): el subagente no ha
    terminado o el principal no los ha traído."""
    salida = {}
    for aux, _ in auxiliares_de(repo, t):
        n = fuera_de(repo, aux, t['rama'])
        if n:
            salida[aux] = n
    return salida


def es_antecesora(repo: Path, a: str, b: str) -> bool:
    return git(repo, 'merge-base', '--is-ancestor', a, b).returncode == 0


def adelantar_auxiliares(repo: Path, t: dict) -> list:
    """Tras integrar develop en la rama de la tarea, lleva a ella cada auxiliar, que ya estaba dentro, para que el
    principal siga trayendo los commits del subagente con «git merge --ff-only». En su worktree, con
    «merge --ff-only» (git no pisa cambios sin commit); sin worktree, moviendo la rama. Devuelve los avisos."""
    rama, avisos = t['rama'], []
    for aux, wt in auxiliares_de(repo, t):
        if not es_antecesora(repo, aux, rama):
            avisos.append(f'{aux} no se ha adelantado: no está entera en {rama}; el subagente, antes de seguir, '
                          f'«git merge {rama}»')
            continue
        r = git(wt, 'merge', '-q', '--ff-only', rama) if wt else git(repo, 'branch', '-f', aux, rama)
        if r.returncode:
            avisos.append(f'{aux} no se ha adelantado ({motivo(r)}); el subagente, antes de seguir, «git merge {rama}»')
    return avisos


def o_probar(cola: Cola, a) -> str:
    t = cola.tarea(a.n, 'en-cola', 'en-curso', 'en-observacion')
    rama, repo = t.get('rama'), cola.repo
    if not rama or not existe_rama(repo, rama):
        raise Rechazo(f'La {a.n} no tiene rama' + (f': {rama} no existe.' if rama else '.'))
    # Se prueba con lo último de develop (tarea 270), pero solo si el subagente ha terminado: con commits sin traer,
    # se probaría una versión a medias, y el merge los dejaría detrás. Ni activa ni integra.
    pendientes = sin_traer(repo, t)
    if pendientes:
        lista = enumerar([f'{aux} ({n} commit{"s" if n > 1 else ""})' for aux, n in pendientes.items()])
        cola.extra.update(fallo='sin-traer', motivo=f'trabajo del subagente sin traer a {rama}: {lista}')
        raise Rechazo(f'La {a.n} tiene trabajo del subagente sin traer a {rama}: {lista}. No se activa: se probaría '
                      f'sin él. Que termine, tráelo con «git merge --ff-only» y repite.')
    integrar = existe_rama(repo, 'develop') and not es_antecesora(repo, 'develop', rama)
    ya = rama_activa(repo) == rama
    if not ya or integrar:
        exigir_limpio(repo, 'la rama activa')
    antes = rama_activa(repo)
    if not ya:
        ajeno = worktree_ajeno(repo, rama)
        if ajeno:
            raise Rechazo(f'La rama {rama} está en el worktree {ajeno}. Quítalo antes.')
        r = git(repo, 'switch', rama)
        if r.returncode != 0:
            raise Rechazo(f'No se pudo activar {rama}: {motivo(r)}')
    avisos = []
    if integrar:
        r = git(repo, 'merge', '-q', '--no-edit', 'develop')
        if r.returncode != 0:
            choques = git(repo, 'diff', '--name-only', '--diff-filter=U').stdout.split()
            git(repo, 'merge', '--abort')
            if not ya and antes:
                git(repo, 'switch', antes)
            causa = (f'choques al integrar develop en {rama}: {", ".join(choques)}' if choques
                     else f'no se pudo integrar develop en {rama} ({motivo(r)})')
            cola.anotar(t, 'probar-fallido', causa)
            cola.guardar()
            cola.extra.update(fallo='choques' if choques else 'merge', motivo=causa)
            raise Rechazo(f'No se activa la {a.n}: {causa}. Está deshecho, {rama} como estaba'
                          + (f' y sigues en {antes}' if not ya and antes else '')
                          + '. Que lo resuelva su subagente (integrando develop en su rama) y repite.')
        avisos = adelantar_auxiliares(repo, t)
    if t['estado'] == 'en-cola':
        a_en_curso(t)
    # Activar la rama es el paso de prueba: queda hecho, también si ya era la activa (tarea 253); el OK del
    # propietario es cerrar (decisión 172).
    for x in pasos(t):
        if x.get('texto') == PASO_PROBAR:
            x['estado'] = 'hecho'
    cola.anotar(t, 'probar', rama + (' · con develop integrado' if integrar else ''))
    cola.guardar()
    # Lo importante primero: el panel lo enseña en un aviso emergente, que se corta por el final (tarea 257).
    return (f'La {a.n}, en prueba: rama {rama}{" (ya era la activa)" if ya else " activa"}'
            + (', con develop integrado' if integrar else '')
            + (f'. Prueba: {t["prueba"]}' if t.get('prueba') else '.')
            + ''.join(f' Aviso: {x}.' for x in avisos))


def o_observando(cola: Cola, a) -> str:
    t = cola.tarea(a.n, 'en-observacion')
    t['observando'] = True
    cola.anotar(t, 'observando')
    cola.guardar()
    return f'La {a.n}, en observación: la estás mirando.'


def o_seguir(cola: Cola, a) -> str:
    t = cola.tarea(a.n, 'en-observacion')
    t.pop('observando', None)
    cola.anotar(t, 'seguir')
    cola.guardar()
    return f'La {a.n} sigue en observación.'


def cierre_git(cola: Cola, t: dict, evento: str, coautor: str | None = None) -> tuple[dict, str, list]:
    """El squash de un cierre (C o a observación): anota el commit, el push fallido y la rama sin borrar.
    Devuelve la tarea releída de la cola, el commit y los avisos. coautor: la de --coautor, sobre la configurada."""
    id_ = t['id']
    try:
        hash_, push, borrado = squash(cola, t, coautor)
    except Fallo as f:
        cola.cargar()
        t2 = cola.buscar(id_)
        if t2 is not None:
            cola.anotar(t2, 'cierre-fallido', str(f))
            cola.guardar()
        cola.extra.update(fallo=f.tipo, motivo=str(f))
        raise Rechazo(f'No se pudo cerrar la {id_}: {f}. Está deshecho; resuélvelo y repite.')
    rama = t['rama']
    # Se relee: el panel puede haber escrito la cola mientras git trabajaba.
    cola.cargar()
    t2 = cola.buscar(id_)
    if t2 is None:  # salió de la cola mientras tanto: el cierre se anota en la que había
        cola.tareas.append(t)
    else:
        t = t2
    avisos = []
    if hash_ is None:  # sin cambios: sin commit ni push (tarea 345)
        cola.anotar(t, evento, f'sin cambios: {rama} ' + ('sin borrar' if borrado else 'borrada'))
        if borrado:
            avisos.append(f'no se pudo borrar {rama} ({borrado})')
        else:
            t.pop('rama', None)
        return t, None, avisos
    cola.anotar(t, evento, f'develop {hash_}')
    if push:
        cola.anotar(t, 'push-fallido', push)
        avisos.append(f'falta el push de develop ({push}); después, súbela con la orden «subir» de cola.py')
    if borrado:
        avisos.append(f'no se pudo borrar {rama} ({borrado})')
    else:
        t.pop('rama', None)
    t['commit'] = hash_
    return t, hash_, avisos


def exigir_cierre(t: dict) -> None:
    """Todo cierre, con rama o sin ella, pide el paso «Cerrar la tarea» y hechos los demás, salvo «Activar rama
    para poder probar», que el cierre marca (decisiones 121, 172 y 174), y las ayudas de prueba, que quedan como estén
    (decisión 184); en una cola de antes, puede faltar."""
    n = t['id']
    if not any(p.get('texto') == 'Cerrar la tarea' for p in pasos(t)):
        raise Rechazo(f'La {n} no tiene el paso «Cerrar la tarea»: «listo {n} --prueba "qué mirar"» añade los de cierre.')
    sin_hacer = [i + 1 for i, p in enumerate(pasos(t))
                 if p.get('estado') != 'hecho' and p.get('texto') not in PASOS_CIERRE and not es_ayuda(p)]
    if sin_hacer:
        raise Rechazo(f'La {n} tiene pasos sin hacer: {enumerar(sin_hacer)}. Márcalos con «paso marcar {n} P hecho» '
                      f'o quita los pendientes con «paso quitar {n} P» (P, el número del paso).')


def exigir_traido(t: dict, sin_integrar: dict) -> None:
    """Antes del squash, que borra la rama de la tarea: si una rama auxiliar tiene commits que no están en ella, el
    principal no los ha traído y se perderían en develop. Se niega y dice cómo traerlos (tarea 271)."""
    rama = t.get('rama')
    falta = {aux: n for aux, n in sin_integrar.items() if n}
    if not rama or not falta:
        return
    lista = enumerar([f'{aux} ({n} commit{"s" if n > 1 else ""})' for aux, n in falta.items()])
    uno = next(iter(falta))
    raise Rechazo(f'La {t["id"]} tiene trabajo de su subagente sin traer a {rama}: {lista}. Tráelo antes de cerrar: '
                  f'con {rama} activa, «git merge --ff-only {uno}»; sin activar, «git fetch . {uno}:{rama}». Si ese '
                  f'trabajo sobra, borra la rama auxiliar a mano y vuelve a cerrar.')


def coautor_de(a) -> str | None:
    """La línea de --coautor, si se ha dado."""
    try:
        return linea_coautor(getattr(a, 'coautor', None))
    except ValueError:
        raise Rechazo('--coautor: una sola línea, «Co-Authored-By: Nombre <correo>».')


def o_cerrar(cola: Cola, a) -> str:
    t = cola.buscar(a.n)
    if t is not None and t.get('estado') == 'en-observacion':
        return cerrar_observada(cola, t, a.n)
    t = cola.tarea(a.n, 'en-curso')
    exigir_cierre(t)
    sin_integrar = sin_integrar_de(cola.repo, t)
    exigir_traido(t, sin_integrar)
    avisos: list = []
    if t.get('rama'):
        t, hash_, avisos = cierre_git(cola, t, 'cerrada', coautor_de(a))
        mensaje = (f'Cerrada la {a.n} en develop ({hash_}).' if hash_ else
                   f'Cerrada la {a.n}, sin commit: su rama no tenía cambios respecto a develop y se ha borrado.')
    else:
        cola.anotar(t, 'cerrada', 'sin rama')
        mensaje = f'Cerrada la {a.n}, sin rama.'
    mensaje += recogida(cola, t, sin_integrar) + ''.join(f' Aviso: {x}.' for x in avisos)
    for p in pasos(t):  # la C es el OK del propietario: «Activar rama para poder probar», si está, queda hecho
        if p.get('texto') in PASOS_CIERRE:
            p['estado'] = 'hecho'
    cola.sacar(t, 'cerrada')
    cola.guardar()
    return mensaje


def o_a_observacion(cola: Cola, a) -> str:
    t = cola.tarea(a.n, 'en-curso')
    if es_deliberativa(t):
        raise Rechazo(f'La {a.n} es de {t["tipo"]}, deliberativa: no pasa por observación (218); se cierra con '
                      f'«cerrar {a.n}».')
    exigir_cierre(t)
    sin_integrar = sin_integrar_de(cola.repo, t)
    exigir_traido(t, sin_integrar)
    rama = t.get('rama')
    if rama and existe_rama(cola.repo, rama) and sin_cambios(cola.repo, rama):
        raise Rechazo(f'La rama {rama} no tiene cambios respecto a develop: no hay nada que observar. Ciérrala con '
                      f'«cerrar {a.n}», que borra la rama sin commit.')
    avisos: list = []
    if rama:
        t, hash_, avisos = cierre_git(cola, t, 'a-observacion', coautor_de(a))
        if hash_ is None:  # lo suyo ya estaba en develop: se cierra, sin commit (tarea 345)
            for p in pasos(t):
                if p.get('texto') in PASOS_CIERRE:
                    p['estado'] = 'hecho'
            cola.anotar(t, 'cerrada', 'sin cambios')
            recogido = recogida(cola, t, sin_integrar)
            cola.sacar(t, 'cerrada')
            cola.guardar()
            return (f'Cerrada la {a.n}, sin commit: lo de su rama ya estaba en develop; no pasa a observación.'
                    + recogido + ''.join(f' Aviso: {x}.' for x in avisos))
        detalle = f' en develop ({hash_})'
    else:
        cola.anotar(t, 'a-observacion', a.commit)
        if a.commit:
            t['commit'] = a.commit
        detalle = ''
    for p in pasos(t):
        if p.get('texto') == 'Cerrar la tarea':
            p['estado'] = 'hecho'
    t['estado'] = 'en-observacion'
    if a.prueba:
        t['prueba'] = a.prueba
    recogido = recogida(cola, t, sin_integrar)
    cola.guardar()
    return f'La {a.n}, en observación{detalle}.' + recogido + ''.join(f' Aviso: {x}.' for x in avisos)


def cerrar_observada(cola: Cola, t: dict, n: int) -> str:
    """Cerrar una en observación (204, 215): va bien. Ya entró en develop al pasarla a observación: sale de la cola
    sin git."""
    t.pop('observando', None)
    for p in pasos(t):
        if p.get('texto') in PASOS_CIERRE:
            p['estado'] = 'hecho'
    cola.anotar(t, 'cerrada', 'en observación')
    recogido = recogida(cola, t, sin_integrar_de(cola.repo, t))  # lo que quedó al pasarla a observación
    cola.sacar(t, 'cerrada')
    cola.guardar()
    return f'Cerrada la {n}, en observación: sale de la cola.' + recogido


def o_reobservar(cola: Cola, a) -> str:
    """Una cerrada por error vuelve a observación («en-observacion»; tarea 296): de
    .sf/historial.jsonl a la cola, con su commit de develop, para seguir vigilándola y poder revertirla. «revertir» lee
    sus commits del historial, de los eventos «cerrada» y «a-observacion»: el suyo, «reobservada», no los repite."""
    t = cola.buscar(a.n)
    if t is not None:
        raise Rechazo(f'La {a.n} está {nombre_estado(t)}: solo vuelve a observación una cerrada.')
    t = cola.archivadas().get(a.n)
    if t is None:
        raise Rechazo(f'La {a.n} no está en la cola ni en el historial.')
    if t.get('estado') != 'cerrada':
        raise Rechazo(f'La {a.n} salió {situacion(t)}: solo vuelve a observación una cerrada.')
    hashes = hashes_de(t)
    t['estado'] = 'en-observacion'
    t.pop('observando', None)
    if hashes:
        t['commit'] = hashes[0]
    cola.anotar(t, 'reobservada', f'con develop {" ".join(hashes)}' if hashes else 'sin commit en develop')
    cola.tareas.append(t)
    cola.guardar()
    con = f', con su commit de develop ({" ".join(hashes)})' if hashes else ', sin commit en develop que revertir'
    return f'La {a.n} vuelve a observación{con}.'


def o_descartar(cola: Cola, a) -> str:
    t = cola.tarea(a.n)
    if t.get('estado') == 'en-observacion':
        raise Rechazo(f'La {a.n} está en observación: ya entró en develop; se revierte («revertir {a.n}»).')
    t = cola.tarea(a.n, 'en-cola', 'en-curso')
    rama = t.get('rama')
    if not rama:
        raise Rechazo(f'La {a.n} no tiene rama: se elimina («eliminar {a.n}»).')
    repo = cola.repo
    ajeno = worktree_ajeno(repo, rama)
    if ajeno:
        raise Rechazo(f'La rama {rama} está en el worktree {ajeno}. Para ese agente y quita el worktree antes.')
    activa = rama_activa(repo) == rama
    if activa:
        exigir_limpio(repo, rama)
        a_develop(repo)
    existe = existe_rama(repo, rama)
    if existe:
        r = git(repo, 'branch', '-D', rama)
        if r.returncode != 0:
            raise Rechazo(f'No se pudo borrar {rama}: {motivo(r)}')
    cola.cargar()
    t = cola.tarea(a.n)
    t['estado'] = 'descartada'
    cola.anotar(t, 'descartada', rama)
    # El descarte descarta todo: también la auxiliar con commits que no entraron y el worktree con cambios sin commit
    # (decisión 189).
    recogido = recogida(cola, t, {}, forzar=True)
    cola.guardar()
    return (f'Descartada la {a.n}: rama {rama} {"borrada" if existe else "ya no existía"}.' + (' Activa: develop.' if activa else '')
            + recogido)


def o_limpiar(cola: Cola, a) -> str:
    fuera = [t for t in cola.tareas if t.get('estado') == 'descartada']
    if not fuera:
        return 'No hay descartadas que limpiar.'
    recogido = ''
    for t in fuera:
        cola.anotar(t, 'limpiada')
        r = recogida(cola, t, {}, forzar=True)  # lo que quedó al descartarla: todo fuera (decisión 189)
        recogido += f' La {t["id"]}:{r}' if r else ''
        cola.sacar(t, 'descartada')
    cola.guardar()
    return f'Limpiadas {len(fuera)}: {enumerar([t["id"] for t in fuera])}.' + recogido


def o_revertir(cola: Cola, a) -> str:
    t = cola.buscar(a.n)
    if t is not None and t.get('estado') != 'en-observacion':
        raise Rechazo(f'La {a.n} está {nombre_estado(t)}: solo se revierte una en observación o cerrada.')
    archivada = t is None
    if archivada:
        t = cola.archivadas().get(a.n)
        if t is None:
            raise Rechazo(f'La {a.n} no está en la cola ni en el historial.')
        if ultimo_evento(t) == 'revertida':
            raise Rechazo(f'La {a.n} ya está revertida.')
    repo = cola.repo
    hashes = a.commit or hashes_de(t) or hashes_en_develop(repo, a.n)
    if not hashes:
        raise Rechazo(f'La {a.n} no tiene commits en develop que revertir.')
    ajeno = worktree_ajeno(repo, 'develop')
    if ajeno:
        raise Rechazo(f'develop está en el worktree {ajeno}. Revierte allí.')
    exigir_limpio(repo, rama_activa(repo) or 'la rama activa')
    # La rama de la tarea que siga viva (no se pudo borrar en el squash): sus commits fuera de develop, antes del revert.
    viva = t.get('rama') if t.get('rama') and existe_rama(repo, t['rama']) else None
    fuera_viva = fuera_de(repo, viva, 'develop') if viva else 0
    # Las auxiliares con commits que nunca entraron, antes del revert (después, lo que entró por squash ya no se ve
    # en develop): se quedan con su worktree y se avisa (decisión 169).
    sin_integrar = sin_integrar_de(repo, t)
    antes = a_develop(repo)
    r = git(repo, 'revert', '--no-edit', *hashes)
    if r.returncode != 0:
        git(repo, 'revert', '--abort')
        if antes and antes != 'develop':
            git(repo, 'switch', antes)
        cola.extra.update(fallo='choques', motivo=f'choques al revertir {" ".join(hashes)}')
        raise Rechazo(f'Choques al revertir la {a.n} ({" ".join(hashes)}): deshecho con git revert --abort. Resuélvelo a mano, sin push.')
    hash_ = git(repo, 'rev-parse', '--short', 'HEAD').stdout.strip()
    cola.cargar()
    t2 = cola.buscar(a.n)
    if t2 is not None:
        t = t2
    t.pop('observando', None)
    t.pop('commit', None)
    # Lo que quedó al pasarla a observación o cerrarla, antes de «revertida»: restaurar mira si va justo antes de «eliminada».
    recogido = recogida(cola, t, sin_integrar)
    cola.anotar(t, 'revertida', f'develop {hash_} revierte {" ".join(hashes)}')
    activa = (' Activa: develop.' if antes != 'develop' else '') + recogido
    # Decisión 134: nunca queda revertida en Cerradas; sale eliminada, sin rastro, o vuelve a Pendientes.
    # Sale sin rama, y la de la tarea que siga viva se borra, sin forzar: con commits que nunca entraron en develop,
    # u ocupada, queda en git y se avisa (decisión 170). Así ni restaurarla ni reabrirla la devuelve a la cola con rama.
    t.pop('rama', None)
    if viva and fuera_viva:
        activa += f' Aviso: queda la rama {viva}, ya fuera de la tarea: tiene commits que no entraron en develop.'
    elif viva and worktree_ajeno(repo, viva):
        activa += f' Aviso: queda la rama {viva}, ya fuera de la tarea: está en el worktree {worktree_ajeno(repo, viva)}.'
    elif viva:
        b = git(repo, 'branch', '-D', viva)
        activa += f' Aviso: no se pudo borrar {viva} ({motivo(b)}).' if b.returncode else f' Borrada la rama {viva}.'
    if a.eliminar:
        cola.anotar(t, 'eliminada', 'en-cola')  # «restaurar» la devuelve en cola, reabierta
        if t2 is not None:
            cola.sacar(t, 'eliminada')
            cola.guardar()
        else:
            t['estado'] = 'eliminada'
            cola.archivar(t)
        return f'Revertida la {a.n} en develop ({hash_}), sin push, y eliminada; su número no se reutiliza.' + activa
    t['estado'] = 'en-cola'
    t['reabierta'] = True
    cierre_pendiente(t)
    cola.anotar(t, 'reabierta', 'revertida')
    if t2 is None:
        cola.tareas.append(t)
    cola.guardar()
    return f'Revertida la {a.n} en develop ({hash_}), sin push; vuelve a Pendientes, en cola.' + activa


def o_reabrir(cola: Cola, a) -> str:
    t = cola.buscar(a.n)
    if t is not None and t.get('estado') not in ('en-observacion', 'descartada'):
        raise Rechazo(f'La {a.n} está {nombre_estado(t)}: no hace falta reabrirla.')
    en_cola = t is not None
    if not en_cola:
        t = cola.archivadas().get(a.n)
        if t is None:
            raise Rechazo(f'La {a.n} no está en la cola ni en el historial.')
        ev = ultimo_evento(t)
        if ev == 'eliminada':
            raise Rechazo(f'La {a.n} se eliminó: se recupera con «restaurar {a.n}».')
        if ev == 'absorbida':
            raise Rechazo(f'La {a.n} se fusionó en otra: deshacer la fusión es /desfusionar (tarea 135).')
    vieja = t.get('rama') or next((e.get('detalle') for e in reversed(t.get('historial', []))
                                   if e.get('evento') == 'rama'), None)
    estado = 'en-cola' if a.en_cola else 'en-curso'
    if a.rama and es_deliberativa(t):
        raise Rechazo(sin_rama_deliberativa(t))
    # Un worktree viejo no se reutiliza nunca: lo que quedó se limpia, también con cambios sin commit y sin avisar de
    # commits perdidos, antes de la rama nueva (decisión 169).
    recogido = recogida(cola, t, {}, forzar=True)
    rama = None
    if estado == 'en-curso' and not es_deliberativa(t):
        if a.rama:
            rama = nombre_rama(a.n, a.rama)
        elif vieja:
            rama = vieja
        if rama:
            crear_rama(cola.repo, rama, activar=not a.sin_activar)
    t['estado'] = estado
    t['reabierta'] = True
    t.pop('observando', None)
    t.pop('rama', None)
    if estado == 'en-curso':
        a_en_curso(t)
    cierre_pendiente(t)
    if rama:
        t['rama'] = rama
    cola.anotar(t, 'reabierta', a.texto)
    if rama:
        cola.anotar(t, 'rama', rama)
    if not en_cola:
        cola.tareas.append(t)
    cola.guardar()
    falta = ('' if rama or estado == 'en-cola' else ' Sin rama: es deliberativa (278).' if es_deliberativa(t)
             else ' Sin rama: créala con «rama» antes del primer activo.')
    return f'Reabierta la {a.n}, {nombre_estado(t)}' + (f', rama {rama} desde develop.' if rama else '.') + falta + recogido


def o_eliminar(cola: Cola, a) -> str:
    t = cola.tarea(a.n, 'en-cola', 'en-curso')
    if t.get('rama'):
        raise Rechazo(f'La {a.n} tiene rama ({t["rama"]}): se descarta («descartar {a.n}»).')
    recogido = recogida(cola, t, sin_integrar_de(cola.repo, t))
    cola.anotar(t, 'eliminada', t['estado'])  # el estado de antes, para restaurarla (y el último evento)
    cola.sacar(t, 'eliminada')
    cola.guardar()
    return f'Eliminada la {a.n}; su número no se reutiliza.' + recogido


def o_restaurar(cola: Cola, a) -> str:
    if cola.buscar(a.n):
        raise Rechazo(f'La {a.n} ya está en la cola.')
    t = cola.archivadas().get(a.n)
    if t is None or ultimo_evento(t) != 'eliminada':
        raise Rechazo(f'La {a.n} no es una eliminada del historial.')
    antes = t['historial'][-1].get('detalle')
    if antes not in ('en-cola', 'en-curso'):  # una línea anterior a los estados de salida guarda el de antes
        antes = t.get('estado') if t.get('estado') in ('en-cola', 'en-curso') else 'en-cola'
    t['estado'] = antes
    if antes == 'en-curso':
        a_en_curso(t)
    if len(t['historial']) > 1 and t['historial'][-2].get('evento') == 'revertida':
        t['reabierta'] = True  # eliminada al revertirla (decisión 134): vuelve como reabierta
    cierre_pendiente(t)
    cola.anotar(t, 'restaurada', antes)
    cola.tareas.append(t)
    cola.guardar()
    return f'Restaurada la {a.n}, {nombre_estado(t)}.'


# ---------- A propuesta (tarea 243) ----------

# Las propuestas del proyecto (sf/propuestas.md): «### P<nn> <título>», con su línea «- **Estado:**». El
# «A Pendientes» de Propuestas, en el panel, pasa una a tarea y cambia su estado por «pasada a la tarea N de la cola el <fecha>».
# Van en sf/ («Los documentos de la SF van en la carpeta sf/», 203); docs/propuestas.md, el sitio de antes, se sigue
# leyendo y escribiendo mientras el proyecto no se ha puesto al día.
PROPUESTAS = 'sf/propuestas.md'
PROPUESTAS_ANTES = 'docs/propuestas.md'
SECCION_PROPUESTAS = '## Propuestas pendientes'
ESTADO_POR_APROBAR = '- **Estado:** propuesta, pendiente de aprobación.'


def nombre_proyecto(repo: Path) -> str:
    """El campo «proyecto» de .sf/proyecto.json; sin él, el nombre de la carpeta."""
    return configuracion(repo)['proyecto'] or repo.name


def a_propuestas(md: str, t: dict, fecha: str, proyecto: str) -> tuple[str, str, bool]:
    """Devuelve propuestas.md con la tarea como propuesta, su número (P<nn>) y si es la propuesta de la que salió.

    Si salió de una (su «Estado» dice «pasada a la tarea N de la cola», o sin número y con su mismo título), vuelve a
    «propuesta, pendiente de aprobación»; si no, va una nueva al final de «Propuestas pendientes», con el primer número
    libre, su título, su tipo y su descripción como cambio propuesto. Conserva los fines de línea CRLF."""
    crlf = '\r\n' in md
    lineas = [x.rstrip('\r') for x in md.split('\n')]
    ini = next((i for i, x in enumerate(lineas) if x.strip() == SECCION_PROPUESTAS), None)
    if ini is None:
        raise Rechazo(f'propuestas.md no tiene «{SECCION_PROPUESTAS}».')
    fin = next((i for i in range(ini + 1, len(lineas)) if lineas[i].startswith('## ')), len(lineas))
    id_, texto = t['id'], t['texto'].strip()
    con_numero = re.compile(rf'^- \*\*Estado:\*\* pasada a la tarea {id_} de la cola\b')
    sin_numero = re.compile(r'^- \*\*Estado:\*\* pasada a tarea de la cola\b')
    titulos = [i for i in range(ini + 1, fin) if lineas[i].startswith('### ')]
    for k, i in enumerate(titulos):
        m = re.match(r'(P\d+) (.+)$', lineas[i][4:].strip())
        numero, nombre = (m.group(1), m.group(2).strip()) if m else ('', lineas[i][4:].strip())
        for j in range(i + 1, titulos[k + 1] if k + 1 < len(titulos) else fin):
            if con_numero.match(lineas[j]) or (sin_numero.match(lineas[j]) and nombre == texto):
                lineas[j] = ESTADO_POR_APROBAR
                return ('\r\n' if crlf else '\n').join(lineas), numero or nombre, True
    numero = f'P{max((int(x) for x in re.findall(r"(?m)^### P(\d+) ", md)), default=0) + 1:02d}'
    parr = [x.strip() for x in re.split(r'\n\s*\n', (t.get('descripcion') or '').replace('\r', '')) if x.strip()]
    cambio = [f'- **Cambio propuesto:** {parr[0] if parr else "por concretar."}']
    for x in parr[1:]:
        cambio += [''] + ['  ' + y for y in x.split('\n')]
    bloque = [f'### {numero} {texto}', '',
              f'- **Origen:** {proyecto}, {fecha}. Devuelta a propuesta desde la tarea {id_} de la cola.',
              *([f'- **Tipo:** {t["tipo"]}.'] if t.get('tipo') else []), *cambio, ESTADO_POR_APROBAR]
    ultima = max(i for i in range(ini, fin) if lineas[i].strip())
    lineas = lineas[:ultima + 1] + [''] + bloque + [''] + (lineas[fin:] if fin < len(lineas) else [''])
    return ('\r\n' if crlf else '\n').join(lineas), numero, False


# propuestas.md vive en develop (tarea 273): «a-propuesta» y «de-propuesta» lo cambian con su propio commit en
# develop, también con otra rama activa, sin tocar la copia de trabajo de esa rama, que quedaría con cambios sin
# commit e impediría cerrar su tarea. Sin git o sin develop, solo se escribe el archivo, y se avisa.
def git_bytes(repo: Path, *args: str, entrada: bytes | None = None, env: dict | None = None) -> subprocess.CompletedProcess:
    """Como git(), en bytes: el contenido del archivo pasa tal cual, con sus fines de línea."""
    return subprocess.run(['git', '-C', str(repo), *args], input=entrada, capture_output=True,
                          env={**os.environ, **env} if env else None)


def motivo_bytes(r: subprocess.CompletedProcess) -> str:
    return linea_de_motivo((r.stderr or r.stdout or b'').decode('utf-8', 'replace'))


def ruta_sf(repo: Path, con_git: bool, nueva: str, antes: str) -> str:
    """La ruta de un documento de la SF: la de sf/ (decisión 203) o, si solo existe la de antes en docs/, esa, porque
    el proyecto aún no se ha puesto al día. Con otra rama activa, mira develop, donde viven."""
    def hay(rel: str) -> bool:
        if con_git and rama_activa(repo) != 'develop':
            return git(repo, 'cat-file', '-e', f'develop:{rel}').returncode == 0
        return (repo / rel).exists()
    return antes if not hay(nueva) and hay(antes) else nueva


def leer_propuestas(repo: Path) -> tuple[str, str, str]:
    """El texto de propuestas.md, dónde vive y su ruta: «develop» (la activa), «otra» (otra rama activa: el de
    develop) o «archivo» (sin git o sin develop)."""
    con_git = git(repo, 'rev-parse', '--git-dir').returncode == 0 and existe_rama(repo, 'develop')
    rel = ruta_sf(repo, con_git, PROPUESTAS, PROPUESTAS_ANTES)
    ruta = repo / rel
    if con_git and rama_activa(repo) != 'develop':
        ajeno = worktree_ajeno(repo, 'develop')
        if ajeno:
            raise Rechazo(f'develop está en el worktree {ajeno}: {rel} se cambia allí.')
        r = git_bytes(repo, 'cat-file', 'blob', f'develop:{rel}')
        if r.returncode != 0:
            raise Rechazo(f'No hay {rel} en develop: este proyecto no lleva propuestas.')
        return r.stdout.decode('utf-8'), 'otra', rel
    if not ruta.is_file():
        raise Rechazo(f'No hay {rel}: este proyecto no lleva propuestas.')
    if con_git:
        r = git(repo, 'status', '--porcelain', '--', rel)
        if r.returncode != 0 or r.stdout.strip():
            raise Rechazo(f'{rel} tiene cambios sin commit en develop: haz commit antes.')
    return ruta.read_bytes().decode('utf-8'), 'develop' if con_git else 'archivo', rel


def commit_en_develop(repo: Path, donde: str, cambios: dict, titulo: str):
    """Un commit «titulo» en develop con `cambios` ({ruta relativa: bytes}). Con develop activa («develop»), commit normal
    de solo esas rutas; con otra rama activa («otra»), sin cambiar de rama ni tocar su copia de trabajo: con un índice
    aparte, hash-object, commit-tree y update-ref (tarea 273). Devuelve con qué deshacerlo y el hash corto."""
    antes = git(repo, 'rev-parse', 'refs/heads/develop').stdout.strip()
    mensaje = (titulo.rstrip('\n') + '\n').encode('utf-8')
    rutas = list(cambios)
    fallo = f'No se pudo hacer el commit de {enumerar(rutas)} en develop'
    if donde == 'develop':
        originales = {x: (repo / x).read_bytes() if (repo / x).is_file() else None for x in rutas}

        def restaurar() -> None:
            git(repo, 'reset', '-q', '--', *rutas)
            for x, o in originales.items():
                if o is None:
                    (repo / x).unlink(missing_ok=True)
                else:
                    (repo / x).write_bytes(o)
        for x, contenido in cambios.items():
            (repo / x).parent.mkdir(parents=True, exist_ok=True)
            (repo / x).write_bytes(contenido)
        r = git_bytes(repo, 'add', '--', *rutas)
        if r.returncode == 0:
            r = git_bytes(repo, 'commit', '-q', '--only', '-F', '-', '--', *rutas, entrada=mensaje)
        if r.returncode != 0:
            restaurar()
            raise Rechazo(f'{fallo}: {motivo_bytes(r)}')

        def deshacer() -> None:
            git(repo, 'reset', '-q', '--soft', antes)
            restaurar()
    else:  # otra rama activa: el commit va a develop sin cambiar de rama, con un índice aparte
        with tempfile.TemporaryDirectory() as tmp:
            env = {'GIT_INDEX_FILE': str(Path(tmp) / 'index')}
            r = git_bytes(repo, 'read-tree', 'develop', env=env)
            for x, contenido in cambios.items():
                if r.returncode != 0:
                    break
                modo = git(repo, 'ls-tree', 'develop', '--', x).stdout.split()
                r = git_bytes(repo, 'hash-object', '-w', '--stdin', entrada=contenido)
                if r.returncode == 0:
                    info = f'{modo[0] if modo else "100644"},{r.stdout.decode().strip()},{x}'
                    r = git_bytes(repo, 'update-index', '--add', '--cacheinfo', info, env=env)
            if r.returncode == 0:
                r = git_bytes(repo, 'write-tree', env=env)
            if r.returncode == 0:
                r = git_bytes(repo, 'commit-tree', r.stdout.decode().strip(), '-p', antes, '-F', '-', entrada=mensaje)
            if r.returncode == 0:
                r = git_bytes(repo, 'update-ref', '-m', titulo.split('\n')[0], 'refs/heads/develop',
                              r.stdout.decode().strip(), antes)
        if r.returncode != 0:
            raise Rechazo(f'{fallo}: {motivo_bytes(r)}')

        def deshacer() -> None:
            ahora_ = git(repo, 'rev-parse', 'refs/heads/develop').stdout.strip()
            git(repo, 'update-ref', 'refs/heads/develop', antes, ahora_)
    return deshacer, git(repo, 'rev-parse', '--short', 'refs/heads/develop').stdout.strip()


def escribir_propuestas(repo: Path, donde: str, rel: str, original: str, nuevo: str, titulo: str):
    """Deja `nuevo` en propuestas.md, en la ruta `rel` que dio leer_propuestas: en develop, con un commit «titulo», o solo en el archivo. Devuelve con qué
    deshacerlo (si después falla la cola) y lo que se añade al mensaje."""
    ruta = repo / rel
    if donde == 'archivo':
        ruta.write_bytes(nuevo.encode('utf-8'))
        return (lambda: ruta.write_bytes(original.encode('utf-8'))), f' {rel}, sin commit: no hay git con develop.'
    deshacer, hash_ = commit_en_develop(repo, donde, {rel: nuevo.encode('utf-8')}, titulo)
    return deshacer, f' {rel}, en develop ({hash_}).'


def o_a_propuesta(cola: Cola, a) -> str:
    t = cola.tarea(a.n, 'en-cola')
    if t.get('rama'):
        raise Rechazo(f'La {a.n} tiene rama ({t["rama"]}): se descarta («descartar {a.n}»).')
    original, donde, rel = leer_propuestas(cola.repo)
    md, numero, devuelta = a_propuestas(original, t, ahora()[:10], nombre_proyecto(cola.repo))
    deshacer, aviso = escribir_propuestas(cola.repo, donde, rel, original, md,
                                          f'{numero} vuelve a propuesta desde la tarea {a.n} de la cola')
    try:
        recogido = recogida(cola, t, sin_integrar_de(cola.repo, t))
        # Sale como una eliminada, sin pasar por Cerradas; «restaurar» no la devuelve: la propuesta manda.
        cola.anotar(t, 'a-propuesta', f'{numero} {"devuelta" if devuelta else "nueva"}')
        cola.sacar(t, 'eliminada')
        cola.guardar()
    except Exception:
        deshacer()
        raise
    cola.extra['propuesta'] = numero
    hecho = f'la {numero} vuelve a pendiente de aprobación' if devuelta else f'nueva propuesta {numero}'
    return f'La {a.n}, a propuesta: {hecho}; sale de la cola.' + aviso + recogido


def marcar_pasada(md: str, encabezado: str, id_: int, fecha: str) -> str:
    """«A Pendientes» de Propuestas: el «Estado» de la propuesta «### encabezado», si sigue por decidir, pasa a «pasada a la tarea
    N de la cola el <fecha>»; ya no dice «pendiente de…», así que no se pasa dos veces. Conserva los fines de línea."""
    lineas = md.split('\n')
    ini = next((i for i, x in enumerate(lineas) if x.strip() == f'### {encabezado}'), None)
    if ini is not None:
        fin = next((i for i in range(ini + 1, len(lineas)) if lineas[i].startswith('##')), len(lineas))
        i = next((j for j in range(ini, fin) if lineas[j].startswith('- **Estado:**')), None)
        if i is not None and re.search(r'pendiente de (aprobación|decisión)', lineas[i], re.I):
            cr = '\r' if lineas[i].endswith('\r') else ''
            lineas[i] = f'- **Estado:** pasada a la tarea {id_} de la cola el {fecha}.{cr}'
            return '\n'.join(lineas)
    raise Rechazo('La mejora ya no está por decidir.')


def o_de_propuesta(cola: Cola, a) -> str:
    exigir_descripcion(cola, a, 'de-propuesta')
    original, donde, rel = leer_propuestas(cola.repo)
    id_ = cola.siguiente()
    texto = a.texto.strip()
    md = marcar_pasada(original, f'{a.numero} {texto}' if a.numero else texto, id_, ahora()[:10])
    deshacer, aviso = escribir_propuestas(cola.repo, donde, rel, original, md,
                                          f'{a.numero or texto} pasa a la tarea {id_} de la cola')
    try:
        mensaje = o_crear(cola, a)
    except Exception:
        deshacer()
        raise
    return mensaje + aviso


# ---------- Decisiones (tarea 283) ----------

# Cada decisión del propietario, un archivo en sf/decisiones/ con su índice README.md («Las decisiones son material de
# la SF: siempre en sf/decisiones/», 208; docs/decisiones/ mientras el proyecto no se ha puesto al día), que viven en
# develop como propuestas.md: «decision» escribe el archivo, rehace el índice y hace su commit en develop con commit_en_develop,
# también con otra rama activa, sin cambiar de rama ni tocar su copia de trabajo. No toca la cola.
DECISIONES = 'sf/decisiones'
DECISIONES_ANTES = 'docs/decisiones'


# La primera línea de la copia que hace el panel de este archivo en ~/.claude/sf/cola-<sesión>.py (decisión 136):
# «# sf-plugin: <raíz del plugin>». Sin ella, este archivo está en el tools/ de su plugin (tarea 322).
MARCA_PLUGIN = '# sf-plugin: '


def carpeta_tools() -> Path:
    """El tools/ del plugin: junto a este archivo o, en la copia del panel, el de la raíz que lleva su primera línea."""
    aqui = Path(__file__).resolve()
    if (aqui.parent / 'indice_decisiones.py').is_file():
        return aqui.parent
    try:
        with open(aqui, encoding='utf-8') as f:
            primera = f.readline().rstrip('\r\n')
    except OSError:
        primera = ''
    if primera.startswith(MARCA_PLUGIN):
        return Path(primera[len(MARCA_PLUGIN):].strip()) / 'tools'
    return aqui.parent


def indice_decisiones():
    """El módulo indice_decisiones.py del tools/ del plugin, que viaja entero en él (carpeta_tools)."""
    import importlib.util
    ruta = carpeta_tools() / 'indice_decisiones.py'
    if not ruta.is_file():
        raise Rechazo(f'No está {ruta}, que necesita «decision». Con el plugin sf activo, /reload-plugins rehace la copia de cola.py.')
    spec = importlib.util.spec_from_file_location('indice_decisiones', ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def leer_decisiones(repo: Path) -> tuple[dict, str | None, str, str]:
    """Las decisiones donde viven ({nombre: texto}), el README.md (o None), dónde («develop», «otra» o «archivo», como
    leer_propuestas) y su carpeta, relativa."""
    con_git = git(repo, 'rev-parse', '--git-dir').returncode == 0 and existe_rama(repo, 'develop')
    rel = ruta_sf(repo, con_git, DECISIONES, DECISIONES_ANTES)
    carpeta = repo / rel
    if con_git and rama_activa(repo) != 'develop':
        ajeno = worktree_ajeno(repo, 'develop')
        if ajeno:
            raise Rechazo(f'develop está en el worktree {ajeno}: las decisiones se registran allí.')
        r = git(repo, 'ls-tree', '--name-only', 'develop', f'{rel}/')
        nombres = [Path(x).name for x in r.stdout.splitlines() if x.endswith('.md')]
        textos = {}
        if nombres:
            # De una vez: «cat-file --batch» da cada blob con su cabecera «objeto tipo tamaño» delante.
            r = git_bytes(repo, 'cat-file', '--batch',
                          entrada=''.join(f'develop:{rel}/{x}\n' for x in nombres).encode('utf-8'))
            datos, i = r.stdout, 0
            for x in nombres:
                fin = datos.index(b'\n', i)
                cabecera = datos[i:fin].split()
                if len(cabecera) < 3 or cabecera[1] != b'blob':
                    i = fin + 1
                    continue
                n = int(cabecera[2])
                textos[x] = datos[fin + 1:fin + 1 + n].decode('utf-8', 'replace')
                i = fin + 1 + n + 1
        readme = textos.pop('README.md', None)
        return textos, readme, 'otra', rel
    if con_git:
        r = git(repo, 'status', '--porcelain', '--', rel)
        # README.html no se versiona (decisión 163): si no está en .gitignore, no cuenta como cambio.
        if r.returncode != 0 or [x for x in r.stdout.splitlines() if not x.endswith('/README.html')]:
            raise Rechazo(f'{rel} tiene cambios sin commit en develop: haz commit antes.')
    textos = {f.name: f.read_bytes().decode('utf-8', 'replace') for f in carpeta.iterdir()
              if f.is_file() and f.suffix == '.md'} if carpeta.is_dir() else {}
    readme = textos.pop('README.md', None)
    return textos, readme, 'develop' if con_git else 'archivo', rel


REPETIR_SUBIDA = 'sube develop con la orden «subir» de cola.py'


def subir_develop(repo: Path, remoto: str, repetir: str = REPETIR_SUBIDA) -> str | None:
    """Sube develop a `remoto`, tras la revisión de lo que sale si el remoto es público (decisión 259: la misma que
    RELEASE, antes_de_subir de revision_publica.py). Devuelve por qué no se ha subido, o None si se ha subido."""
    import importlib.util
    ruta = carpeta_tools() / 'revision_publica.py'
    if not ruta.is_file():
        return f'no está {ruta}, que revisa lo que sale; con el plugin sf activo, /reload-plugins rehace la copia de cola.py'
    spec = importlib.util.spec_from_file_location('revision_publica', ruta)
    rev = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rev)
    try:
        d = rev.antes_de_subir(repo, remoto, repetir=repetir, solo_publico=True, accion='subir')
    except RuntimeError as err:
        return f'no se pudo revisar lo que sale ({err})'
    if d['accion'] != 'seguir':
        return d['mensaje']
    r = git(repo, 'push', '-q', remoto, 'refs/heads/develop:refs/heads/develop')
    return motivo(r) if r.returncode else None


def push_develop(repo: Path) -> str:
    """Sube develop al remoto de la configuración (origin, si no dice otro). Devuelve lo que añadir al mensaje."""
    remoto = configuracion(repo)['remoto']
    error = subir_develop(repo, remoto)
    return f' Subida a {remoto}.' if error is None else f' Sin subir a {remoto}: {error}'


def o_subir(cola: Cola, a) -> str:
    """Sube develop a su remoto, con la revisión de lo que sale (decisión 259): tras un cierre que no la subió."""
    remoto = configuracion(cola.repo)['remoto']
    error = subir_develop(cola.repo, remoto, getattr(a, 'repetir', None) or REPETIR_SUBIDA)
    if error:
        raise Rechazo(f'develop sin subir a {remoto}: {error}')
    return f'develop subida a {remoto}.'


def o_decision(cola: Cola, a) -> str:
    repo, idx = cola.repo, indice_decisiones()
    titulo = ' '.join(a.titulo.split())
    if not titulo:
        raise Rechazo('Falta el título de la decisión.')
    if a.archivo:
        try:
            texto = Path(a.archivo).read_bytes().decode('utf-8')
        except (OSError, UnicodeDecodeError) as e:
            raise Rechazo(f'No se puede leer {a.archivo}: {e}')
    else:
        texto = a.texto
    texto = texto.removeprefix('﻿').replace('\r\n', '\n').strip('\n')
    if not texto.strip():
        raise Rechazo('La decisión está vacía.')
    cabeza = texto.split('\n', 1)[0]
    if cabeza.startswith('# '):
        if ' '.join(cabeza[2:].split()) != titulo:
            raise Rechazo(f'El texto empieza por «{cabeza}» y el título es «{titulo}»: que coincidan.')
    else:
        texto = f'# {titulo}\n\n{texto}'
    decisiones, readme, donde, carpeta = leer_decisiones(repo)
    numeros = {int(m.group(1)): x for x in decisiones if (m := idx.NOMBRE.match(x))}
    if a.numero is not None:
        nombre = numeros.get(a.numero)
        if not nombre:
            raise Rechazo(f'No hay decisión {a.numero:03d} en {carpeta}' + (' de develop.' if donde != 'archivo' else '.'))
        if decisiones[nombre].replace('\r\n', '\n').strip('\n') == texto:
            raise Rechazo(f'La decisión {a.numero:03d} ya dice eso.')
        numero = a.numero
    else:
        numero = max(numeros, default=0) + 1
        nombre = f'{numero:03d}-{datetime.date.today().isoformat()}-{idx.kebab(titulo)}.md'
    # Los fines de línea, los del índice que ya hay.
    nl = '\r\n' if readme and '\r\n' in readme else '\n'
    decisiones[nombre] = texto + '\n'
    indice, _ = idx.indice(readme, decisiones.items())
    cambios = {f'{carpeta}/{nombre}': (texto + '\n').replace('\n', nl).encode('utf-8'),
               f'{carpeta}/README.md': indice.replace('\n', nl).encode('utf-8')}
    que = 'modificada' if a.numero is not None else 'registrada'
    cola.extra.update({'numero': numero, 'archivo': f'{carpeta}/{nombre}'})
    if donde == 'archivo':
        for x, contenido in cambios.items():
            (repo / x).parent.mkdir(parents=True, exist_ok=True)
            (repo / x).write_bytes(contenido)
        return f'Decisión {numero:03d} {que}: {carpeta}/{nombre}, sin commit: no hay git con develop.'
    coautor = coautor_de(a) or configuracion(repo)['coautor']
    mensaje = f'Decisión {numero:03d}: {titulo}' + (' (modificada)' if a.numero is not None else '')
    _, hash_ = commit_en_develop(repo, donde, cambios, mensaje + (f'\n\n{coautor}' if coautor else ''))
    cola.extra['hash'] = hash_
    respuesta = f'Decisión {numero:03d} {que} en develop ({hash_}): {carpeta}/{nombre}.'
    if donde == 'develop':  # README.html no se versiona (decisión 163): se rehace en la copia de trabajo, que es develop
        html = idx.generar_html(repo / carpeta)
        if html.startswith('sin README.html'):
            respuesta += f' {html}.'
    return respuesta + (push_develop(repo) if a.push else '')


def contenida(repo: Path, rama: str, en: str) -> bool:
    return git(repo, 'merge-base', '--is-ancestor', rama, en).returncode == 0


def ramas_de_fusion(cola: Cola, queda: dict, con_rama: list) -> tuple[dict, list]:
    """Con varias tareas con rama, la que conserva la suya y las ramas que sobran, que existen y ya están en ella.
    Rechaza si alguna tiene commits fuera de la de destino o está en un worktree."""
    repo = cola.repo
    if git(repo, 'rev-parse', '--git-dir').returncode != 0:
        raise Rechazo(f'Tienen rama {enumerar([t["id"] for t in con_rama])} y no hay git para ver si están integradas.')
    vivas = [t for t in con_rama if existe_rama(repo, t['rama'])]
    if queda in con_rama:
        destino = queda
    elif not vivas:
        destino = con_rama[-1]  # ninguna existe: la de número más alto
    else:  # la que contiene a todas las vivas (con empate, la de número más alto)
        llenas = [t for t in vivas if all(contenida(repo, o['rama'], t['rama']) for o in vivas)]
        if not llenas:
            raise Rechazo(f'Las ramas {enumerar([t["rama"] for t in vivas])} tienen commits distintos: integra las '
                          f'demás en una antes de fusionar.')
        destino = llenas[-1]
    dest = destino['rama']
    sin_integrar = [t['rama'] for t in vivas if t is not destino and not (existe_rama(repo, dest) and contenida(repo, t['rama'], dest))]
    if sin_integrar:
        raise Rechazo(f'{"La rama" if len(sin_integrar) == 1 else "Las ramas"} {enumerar(sin_integrar)} '
                      f'{"tiene" if len(sin_integrar) == 1 else "tienen"} commits que no están en {dest}: '
                      f'intégra{"la" if len(sin_integrar) == 1 else "las"} en {dest} antes de fusionar.')
    sobran = [t['rama'] for t in vivas if t is not destino]
    for rama in sobran:
        ajeno = worktree_ajeno(repo, rama)
        if ajeno:
            raise Rechazo(f'La rama {rama} está en el worktree {ajeno}: quita el worktree antes de fusionar.')
        if rama_activa(repo) == rama:
            raise Rechazo(f'La rama {rama} es la activa: pasa a otra antes de fusionar.')
    return destino, sobran


def o_fusionar(cola: Cola, a) -> str:
    ids = sorted(set(a.ids))
    if len(ids) < 2:
        raise Rechazo('Hacen falta dos tareas o más: fusionar 104 105.')
    todas = []
    for id_ in ids:
        t = cola.tarea(id_)
        if t.get('estado') == 'en-observacion':
            raise Rechazo(f'La {id_} está en observación: no se fusiona.')
        if t.get('estado') not in ('en-cola', 'en-curso'):
            raise Rechazo(f'La {id_} está {nombre_estado(t)}: no se fusiona.')
        todas.append(t)
    queda, salen = todas[-1], todas[:-1]
    con_rama = [t for t in todas if t.get('rama')]
    destino, sobran = ramas_de_fusion(cola, queda, con_rama) if len(con_rama) > 1 else (con_rama[0] if con_rama else None, [])
    for rama in sobran:  # integradas en la de destino: se borran antes de tocar la cola
        r = git(cola.repo, 'branch', '-D', rama)
        if r.returncode != 0:
            raise Rechazo(f'No se pudo borrar {rama}: {motivo(r)}')
    # Los subagentes de las absorbidas se recogen si su auxiliar ya está en la rama que queda; la que queda conserva
    # el suyo (decisión 169). Una sub-N sin anotar, de antes de anotarlas, también.
    rama_final = destino['rama'] if destino else 'develop'
    recogidos = []
    for t in salen:
        pares = subagentes_de(t)
        if existe_rama(cola.repo, f'sub-{t["id"]}') and all(aux != f'sub-{t["id"]}' for _, aux in pares):
            pares.append((None, f'sub-{t["id"]}'))
        r = recogida(cola, t, {}, destino=rama_final, pares=pares)
        recogidos.append(f' La {t["id"]}:{r}' if r else '')
    nuevos = []
    for t in todas:
        # Los de cierre, una vez y al final, si la que queda está en curso (decisión 174).
        propios = [p for p in pasos(t) if isinstance(p, dict) and p.get('texto') and not es_de_cierre(p.get('texto'))]
        nuevos += propios or [{'texto': t.get('texto'), 'estado': 'en-curso' if t.get('estado') == 'en-curso' else 'pendiente'}]
    # Cada descripción, en su párrafo: punto y aparte entre ellas (decisión del propietario, 2026-10-30).
    descripcion = '\n\n'.join(t['descripcion'] for t in [queda, *salen] if t.get('descripcion'))
    prueba = next((t['prueba'] for t in [queda, *salen] if t.get('prueba')), None)
    tipo = next((t['tipo'] for t in [queda, *salen] if t.get('tipo')), None)
    queda['pasos'] = nuevos
    if any(t.get('estado') == 'en-curso' for t in todas):
        a_en_curso(queda)
    else:
        queda['estado'] = 'en-cola'
    if descripcion:
        queda['descripcion'] = descripcion
    if destino:
        queda['rama'] = destino['rama']
    if prueba:
        queda['prueba'] = prueba
    if tipo:
        queda['tipo'] = tipo
    if queda['estado'] == 'en-curso':  # con su tipo y su rama ya puestos: una deliberativa sin rama no se prueba (278)
        asegurar_cierre(queda)
    otras = [t['id'] for t in salen]
    cola.anotar(queda, 'fusion', f'absorbe {enumerar(otras)}')
    for t in salen:
        propia = t.get('rama') if t is not destino else None
        borrada = f', rama {propia} {"borrada" if propia in sobran else "ya no existía"}' if propia else ''
        cola.anotar(t, 'absorbida', f'en {queda["id"]}{borrada}')
        cola.sacar(t, 'absorbida')
    cola.guardar()
    rama = f' Rama: {queda["rama"]}.' if destino and destino is not queda else ''
    borradas = f' Borradas, ya integradas: {enumerar(sobran)}.' if sobran else ''
    return (f'Fusionadas en la {queda["id"]} {"la" if len(otras) == 1 else "las"} {enumerar(otras)}: {len(pasos(queda))} pasos.'
            f'{rama}{borradas}' + ''.join(recogidos))


def o_split(cola: Cola, a) -> str:
    t = cola.tarea(a.n, 'en-cola', 'en-curso')
    p = pasos(t)
    try:
        nums = sorted({int(x) for x in a.pasos.replace(' ', '').split(',') if x})
    except ValueError:
        raise Rechazo(f'Los pasos van separados por comas: split {a.n} 2,3.')
    trabajo = [i + 1 for i, x in enumerate(p) if not es_de_cierre(x.get('texto')) and not es_ayuda(x)]
    if len(trabajo) < 2:
        raise Rechazo(f'La {a.n} tiene {len(trabajo)} paso{"s" if len(trabajo) != 1 else ""} de trabajo: separar pide '
                      f'dos o más.')
    if not nums:
        raise Rechazo(f'Di qué pasos de la {a.n} separas: split {a.n} 2,3.')
    fuera = next((n for n in nums if not 1 <= n <= len(p)), None)
    if fuera is not None:
        raise Rechazo(f'La {a.n} no tiene paso {fuera}: tiene {len(p)}.')
    cierre = [n for n in nums if n not in trabajo]
    if cierre:
        raise Rechazo(f'{"El paso" if len(cierre) == 1 else "Los pasos"} {enumerar(cierre)} de la {a.n} '
                      f'{"es" if len(cierre) == 1 else "son"} de cierre o de ayuda a la prueba: no se separa'
                      f'{"n" if len(cierre) > 1 else ""}.')
    if len(nums) == len(trabajo):
        raise Rechazo(f'No se pueden separar todos los pasos de la {a.n}: eso es renombrarla.')
    separados = [p[n - 1] for n in nums]
    t['pasos'] = [x for i, x in enumerate(p) if i + 1 not in nums]
    id_ = cola.siguiente()
    nueva = {'id': id_, 'texto': separados[0].get('texto'), 'estado': 'en-cola', 'pasos': separados}
    if t.get('tipo'):
        nueva['tipo'] = t['tipo']  # la separada, del mismo tipo que su origen
    cola.anotar(t, 'separada', f'pasos {enumerar(nums)} a la {id_}')
    cola.anotar(nueva, 'nacida', f'de la {a.n}')
    cola.tareas.append(nueva)
    cola.datos['ultimo'] = id_
    cola.guardar()
    cola.extra['id'] = id_
    hechos = [n for n in nums if p[n - 1].get('estado') == 'hecho']
    aviso = (f' El trabajo {"del paso" if len(hechos) == 1 else "de los pasos"} {enumerar(hechos)}, ya hecho, sigue en la '
             f'rama de la {a.n}.' if hechos else '')
    return f'Separado de la {a.n} {"el paso" if len(nums) == 1 else "los pasos"} {enumerar(nums)}: tarea {id_}, «{nueva["texto"]}», en cola.{aviso}'


def leer_copia(ruta: Path) -> dict:
    try:
        d = json.loads(ruta.read_bytes().decode('utf-8'))
        for t in d.get('peticiones') if isinstance(d.get('peticiones'), list) else []:
            migrar_tarea(t)
        return d if isinstance(d.get('peticiones'), list) else {'peticiones': []}
    except (OSError, json.JSONDecodeError):
        return {'peticiones': []}


def diferencia(antes: dict, despues: dict) -> str:
    a = {t.get('id'): t for t in antes.get('peticiones', [])}
    d = {t.get('id'): t for t in despues.get('peticiones', [])}
    partes = []
    altas = [i for i in d if i not in a]
    bajas = [i for i in a if i not in d]
    cambios = [f'{i} {a[i].get("estado")}→{d[i].get("estado")}' for i in d if i in a and a[i].get('estado') != d[i].get('estado')]
    otros = [i for i in d if i in a and a[i] != d[i] and a[i].get('estado') == d[i].get('estado')]
    if altas:
        partes.append('altas ' + ', '.join(map(str, altas)))
    if bajas:
        partes.append('bajas ' + ', '.join(map(str, bajas)))
    if cambios:
        partes.append(', '.join(cambios))
    if otros:
        partes.append('cambian ' + ', '.join(map(str, otros)))
    return '; '.join(partes) or 'sin cambios'


def o_copias(cola: Cola, a) -> str:
    copias = lista_copias(cola.copias)
    if not copias:
        return 'No hay copias.'
    actual = leer_copia(cola.archivo) if cola.archivo.exists() else {'peticiones': []}
    lineas, despues = [], actual
    for n, c in enumerate(copias, 1):
        d = leer_copia(c)
        m = re.match(r'peticiones-(\d{4})(\d\d)(\d\d)-(\d\d)(\d\d)(\d\d)', c.name)
        fecha = f'{m[1]}-{m[2]}-{m[3]} {m[4]}:{m[5]}:{m[6]}' if m else c.name
        lineas.append(f'{n}\t{fecha}\t{len(d["peticiones"])} tarea{"" if len(d["peticiones"]) == 1 else "s"}\tdespués: {diferencia(d, despues)}')
        despues = d
    return '\n'.join(lineas)


def o_recuperar(cola: Cola, a) -> str:
    copias = lista_copias(cola.copias)
    if a.copia.isdigit():
        n = int(a.copia)
        if not 1 <= n <= len(copias):
            raise Rechazo(f'No hay copia {n}: hay {len(copias)}.')
        elegida = copias[n - 1]
    else:
        elegida = next((c for c in copias if c.name == a.copia or c.stem == a.copia), None)
        if elegida is None:
            raise Rechazo(f'No hay copia «{a.copia}».')
    texto = elegida.read_bytes().decode('utf-8')
    try:
        cola.datos = json.loads(texto)
    except json.JSONDecodeError:
        raise Rechazo(f'La copia {elegida.name} no es JSON válido.')
    for t in cola.datos.get('peticiones') if isinstance(cola.datos.get('peticiones'), list) else []:
        migrar_tarea(t)
    cola.guardar()
    return f'Recuperada {elegida.name}; la cola de antes es ahora la copia 1 («recuperar 1» lo deshace).'


# ---------- Choques entre tareas (decisión 130) ----------

class Consulta(str):
    """Respuesta de una orden de consulta con datos para --json y su propio código de salida."""
    def __new__(cls, mensaje: str, datos: dict, codigo: int = 0):
        c = super().__new__(cls, mensaje)
        c.datos, c.codigo = datos, codigo
        return c


CON_CHOQUES = 3  # código de salida de «choques» cuando la tarea comparte archivos
SIN_COMILLAS = ('-c', 'core.quotepath=false')  # rutas con tildes, tal cual


def ramas_de(t: dict) -> list:
    """La rama de la tarea y las auxiliares de sus subagentes (historial «worktree · rama»)."""
    ramas = [t['rama']] if t.get('rama') else []
    for e in t.get('historial', []):
        if e.get('evento') == 'subagente' and ' · ' in (e.get('detalle') or ''):
            aux = e['detalle'].rsplit(' · ', 1)[1].strip()
            if aux and aux not in ramas:
                ramas.append(aux)
    return ramas


def worktrees_por_rama(repo: Path) -> dict:
    r = git(repo, 'worktree', 'list', '--porcelain')
    salida = {}
    for bloque in re.split(r'\n\s*\n', r.stdout.replace('\r\n', '\n')) if r.returncode == 0 else []:
        w = re.search(r'^worktree (.+)$', bloque, re.M)
        b = re.search(r'^branch refs/heads/(.+)$', bloque, re.M)
        if w and b:
            salida[b.group(1)] = Path(w.group(1))
    return salida


def archivos_de_rama(repo: Path, rama: str, worktrees: dict) -> set | None:
    """Lo que la rama cambia respecto a develop, más lo que su worktree tiene sin commit; None si no existe."""
    if not existe_rama(repo, rama):
        return None
    r = git(repo, *SIN_COMILLAS, 'diff', '--name-only', f'develop...{rama}')
    if r.returncode != 0:
        return None
    archivos = set(r.stdout.splitlines())
    wt = worktrees.get(rama)
    if wt is not None and wt.is_dir():
        for args in (('diff', '--name-only', 'HEAD'), ('ls-files', '--others', '--exclude-standard')):
            r = git(wt, *SIN_COMILLAS, *args)
            if r.returncode == 0:
                archivos |= set(r.stdout.splitlines())
    return archivos


def normalizar(ruta: str) -> str:
    ruta = ruta.replace('\\', '/').strip()
    return ruta[2:] if ruta.startswith('./') else ruta


def o_choques(cola: Cola, a) -> str:
    t = cola.tarea(a.n)
    if git(cola.repo, 'rev-parse', '--verify', '--quiet', 'refs/heads/develop').returncode != 0:
        raise Rechazo('No hay rama develop con la que comparar.')
    worktrees = worktrees_por_rama(cola.repo)
    propios = {normalizar(x) for x in a.archivos or []}
    for rama in ramas_de(t):
        propios |= archivos_de_rama(cola.repo, rama, worktrees) or set()
    if not propios:
        raise Rechazo(f'La {a.n} no tiene archivos que comparar: sin rama o sin cambios, pasa --archivos con los previstos.')
    choques, sin_git, comparadas = [], [], []
    for o in cola.tareas:
        if o.get('id') == a.n or o.get('estado') not in ('en-curso', 'en-observacion') or not o.get('rama'):
            continue
        suyos, alguna = set(), False
        for rama in ramas_de(o):
            r = archivos_de_rama(cola.repo, rama, worktrees)
            if r is not None:
                suyos |= r
                alguna = True
        if not alguna:
            sin_git.append(o['id'])
            continue
        comparadas.append(o['id'])
        comunes = sorted(propios & suyos)
        if comunes:
            choques.append({'id': o['id'], 'estado': o['estado'], 'texto': o.get('texto'),
                            'ramas': ramas_de(o), 'archivos': comunes})
    datos = {'choques': choques, 'archivos': sorted(propios), 'comparadas': comparadas, 'sin_rama': sin_git}
    nota = f' Sin rama en git: {enumerar(sin_git)}.' if sin_git else ''
    if not choques:
        return Consulta(f'La {a.n} no comparte archivos con las tareas en curso ni en observación'
                        + (f' (comparada con {enumerar(comparadas)}).' if comparadas else '.') + nota, datos)
    lineas = [f'La {a.n} comparte archivos con:']
    for c in choques:
        lineas.append(f'- {c["id"]} ({nombre_estado(c)} · {c["ramas"][0]}): {", ".join(c["archivos"])}')
    ids = ' '.join(str(x) for x in sorted([a.n] + [c['id'] for c in choques]))
    lineas.append(f'Recomendado: esperar a que se cierre{"n" if len(choques) > 1 else ""} o fusionar ({ids}).' + nota)
    return Consulta('\n'.join(lineas), datos, CON_CHOQUES)


# ---------- Encargo de un subagente (tarea 250) ----------

def proyecto_json(cola: Cola) -> dict:
    """.sf/proyecto.json, o {} si no está o no se lee."""
    try:
        d = json.loads((cola.sf / 'proyecto.json').read_text(encoding='utf-8'))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def orden_python() -> str:
    """Cómo se lanza en esta máquina el Python que ejecuta cola.py («La orden de Python sale del intérprete que se
    detecta», 236): su nombre (python3 en macOS y en muchas Linux), o su ruta si ese nombre no está en el PATH."""
    if not sys.executable:
        return 'python'
    exe = Path(sys.executable)
    nombre = exe.stem if exe.suffix.lower() == '.exe' else exe.name
    return nombre if nombre == 'python' or shutil.which(nombre) else exe.as_posix()


def o_encargo(cola: Cola, a) -> str:
    """La parte fija del encargo de un subagente: el principal añade solo lo propio de la tarea. Se apaga en
    .sf/proyecto.json con "automatizaciones": {"encargo_subagente": false}; la línea de coautoría, con --coautor o el
    campo "coautor" de ese archivo (en la SF, la suya); sin ninguna, los commits van sin línea de coautoría (238)."""
    proyecto = proyecto_json(cola)
    auto = proyecto.get('automatizaciones')
    if isinstance(auto, dict) and auto.get('encargo_subagente') is False:
        raise Rechazo('El encargo está apagado en .sf/proyecto.json (automatizaciones.encargo_subagente): escríbelo a mano.')
    t = cola.tarea(a.n, 'en-curso', 'en-observacion')
    subs = subagentes_de(t)
    deliberativa = es_deliberativa(t) and not t.get('rama')
    if not subs and not deliberativa:
        raise Rechazo(f'La {a.n} no tiene subagente anotado: antes, cola.py subagente {a.n} --worktree RUTA --rama sub-{a.n}.')
    wt, aux = subs[-1] if subs else (None, None)
    conf = leer_configuracion(proyecto, es_sf=(cola.repo / MARCA_SF).is_file())
    coautor = coautor_de(a) or conf['coautor']
    nombre = conf['proyecto'] or cola.repo.name
    marca = f'«({a.n})» al final del título' if conf['commits'] == 'libre' else f'el trailer «{TRAILER_TAREA}: {a.n}» al pie'
    rama = f' (nunca la rama de la tarea, {t["rama"]}, ni otras)' if t.get('rama') else ' (nunca la rama de la tarea ni otras)'
    if deliberativa:  # sin rama, worktree ni rama auxiliar (256, 278)
        donde = (f'Sin rama, worktree ni rama auxiliar: es de {t["tipo"]}, deliberativa («Una deliberativa solo escribe su '
                 f'documento, sin rama…», 278). Lees en la carpeta del proyecto, {cola.repo.as_posix()}, sin cambiar de '
                 f'rama, y solo escribes su documento (el informe y, si la hay, la visión), que va directo a develop en '
                 f'cada vuelta, con el respaldo de la versión anterior en _respaldo/. Lo demás que haga falta cambiar '
                 f'(código, skills, otros documentos) no lo cambias: propónlo en el informe como tarea aparte, con rama. '
                 f'Si develop no es la rama activa de esa carpeta, no la cambies: deja el documento sin commit y dilo en '
                 f'el informe.')
    else:
        donde = f'Worktree: {wt}' + (f', rama auxiliar {aux}{rama}.' if aux else f'{rama}.')
    lineas = [
        f'Tarea {a.n} de {nombre}: «{t.get("texto", "")}».',
        '',
        donde,
        '',
        'Reglas:',
        '- No escribas la cola (.sf/peticiones.json) ni uses cola.py para cambiarla: en pruebas, solo colas temporales.',
        '- No cargues sf:orquestacion: sigue este encargo.',
        '- No toques documentos compartidos («Cómo funciona…», la metodología, la plantilla claude-sf.md, el CLAUDE.md)'
        ' salvo que el encargo lo pida: propón el texto en el informe.',
        '- Textos compactos: títulos de paso y commit empiezan por lo que cambia, sin prefijos ni relleno. Sin referencias'
        ' por número que no se vean en pantalla: por su título, con el número entre paréntesis si ayuda.',
        f'- Commits {"solo de su documento, en develop" if deliberativa else "en la rama auxiliar"}, con {marca} y '
        + (f'terminados en «{coautor}».' if coautor
           else 'sin línea de coautoría (Co-Authored-By): el proyecto no la tiene configurada.'),
        *([] if deliberativa else ['- Antes de terminar, pasa las pruebas y la validación del proyecto.']),
        '- Si algo exige una decisión del propietario, para y devuélvela con opciones.',
        '- Si un hook o un permiso te bloquea, no lo sortees (otra herramienta, un script, otra ruta): para y dilo en'
        ' el informe, con lo que bloqueó y por qué.',
        f'- {convenciones(conf)}',
    ]
    py = orden_python()
    if py != 'python':
        lineas.append(f'- Python, en esta máquina: «{py}», no «python»: úsalo en toda orden de Python de la SF (la cola, '
                      f'sus herramientas y los scripts de las skills).')
    lineas += [
        '',
        'Informe final, breve:',
        '- Lo hecho.',
        '- Lo comprobado: una línea por comprobación, con su resultado («Comprobado: 300 pruebas de Python, sin '
        'fallos»), lista para pasar a pasos hechos; lo no comprobado, como tal.',
        '- Lo que debe decidir el propietario.',
        '- Documentos compartidos a actualizar, con el texto propuesto.',
        *([] if deliberativa else ['- Qué mirar en la prueba.']),
    ]
    texto = '\n'.join(lineas)
    return Consulta(texto, {'encargo': texto, 'worktree': wt, 'rama_auxiliar': aux, 'sin_rama': deliberativa})


# ---------- Línea de órdenes ----------

SOLO_LECTURA = {'lista', 'ver', 'copias', 'choques', 'encargo'}
# No leen ni escriben la cola: ni la bloquean ni la cargan.
SIN_COLA = {'decision', 'subir'}


def analizador() -> argparse.ArgumentParser:
    comun = argparse.ArgumentParser(add_help=False)
    comun.add_argument('--raiz', type=Path, default=argparse.SUPPRESS, help='carpeta del proyecto o ruta de la cola')
    comun.add_argument('--quien', choices=('propietario', 'principal'), default=argparse.SUPPRESS)
    comun.add_argument('--via', choices=('cli', 'panel'), default=argparse.SUPPRESS)
    comun.add_argument('--json', action='store_true', default=argparse.SUPPRESS, help='respuesta en JSON')
    p = argparse.ArgumentParser(prog='cola.py', parents=[comun], description='Cola de tareas de un proyecto de la SF.')
    o = p.add_subparsers(dest='orden', required=True, metavar='orden')

    def orden(nombre, f, ayuda, *args, padre=o, **kw):
        s = padre.add_parser(nombre, parents=[comun], help=ayuda, **kw)
        s.set_defaults(f=f, orden=nombre)
        for a_ in args:
            if a_ == 'i':
                s.add_argument(a_, type=int, metavar='P', help='número del paso, desde 1 (el «n» de ver)')
            else:
                s.add_argument(a_, type=int) if a_ == 'n' else s.add_argument(a_)
        return s

    orden('lista', o_lista, 'las tareas de la cola')
    orden('ver', o_ver, 'una tarea, de la cola o del historial', 'n')
    s = orden('crear', o_crear, 'tarea nueva, en cola', 'texto')
    s.add_argument('--descripcion', help='qué se pide y por qué; obligatoria cuando crea Claude (tarea 326)')
    s.add_argument('--tipo', choices=TIPOS, help='deliberar, documentar, diseñar, implementar, especificar, corregir o investigar')
    s.add_argument('--en-curso', action='store_true')
    orden('en-curso', o_en_curso, 'de en cola a en curso', 'n')
    orden('en-cola', o_en_cola, 'de en curso a en cola, sin rama (decisión 170)', 'n')
    s = orden('rama', o_rama, 'crea la rama feature/N-nombre desde develop', 'n', 'nombre')
    g = s.add_mutually_exclusive_group()
    g.add_argument('--sin-activar', action='store_true', help='la crea sin cambiar a ella (para un subagente)')
    g.add_argument('--anotar', action='store_true', help='solo la anota: ya existe')
    sp = o.add_parser('paso', help='añadir, marcar o quitar un paso').add_subparsers(dest='accion', required=True, metavar='acción')
    s = orden('añadir', o_paso_anadir, 'paso nuevo, pendiente, antes de los de cierre', 'n', 'texto', padre=sp, aliases=['anadir'])
    s.add_argument('--prueba', action='store_true',
                   help='ayuda de prueba: tras «Activar rama para poder probar», sin exigirla para cerrar (decisión 184)')
    s = orden('marcar', o_paso_marcar, 'cambia el estado de un paso', 'n', 'i', padre=sp)
    s.add_argument('estado', choices=ESTADOS_PASO)
    s.add_argument('--texto', help='texto nuevo (al hacerse, en participio)')
    orden('quitar', o_paso_quitar, 'quita un paso pendiente (no «Cerrar la tarea»)', 'n', 'i', padre=sp)
    orden('renombrar', o_renombrar, 'nombre nuevo, mismo número', 'n', 'texto')
    s = orden('tipo', o_tipo, 'pone o cambia el tipo de la tarea', 'n')
    s.add_argument('tipo', choices=TIPOS)
    orden('redescribir', o_redescribir, 'descripción nueva (vacía, la quita); párrafos separados por una línea en blanco', 'n', 'texto')
    s = orden('subagente', o_subagente, 'anota un subagente lanzado', 'n')
    s.add_argument('--worktree', required=True)
    s.add_argument('--rama', help='su rama auxiliar')
    s = orden('informe', o_informe, 'anota el informe de un subagente', 'n')
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument('--terminado', action='store_true')
    g.add_argument('--interrumpido', action='store_true')
    s.add_argument('texto', nargs='?')
    s = orden('listo', o_listo, 'pasos de cierre y qué probar', 'n')
    s.add_argument('--prueba', required=True)
    orden('comprobado', o_comprobado, 'lo comprobado y su resultado, como paso hecho (decisión 288)', 'n', 'texto')
    orden('probar', o_probar, 'integra develop en la rama de la tarea, la activa (o la deja, si ya lo está) y marca '
          'hecho el paso de prueba', 'n')
    orden('observando', o_observando, 'en observación, el propietario la mira ahora', 'n')
    orden('seguir', o_seguir, 'sigue en observación', 'n')
    s = orden('cerrar', o_cerrar, 'cierra, con «Cerrar la tarea»: con rama, squash en develop (la C); sin rama, sale de la cola; en observación, sale de la cola sin git', 'n')
    s.add_argument('--coautor', help='la línea Co-Authored-By del squash, sobre la de .sf/proyecto.json')
    s = orden('a-observacion', o_a_observacion, 'cierra y la deja en observación: squash en develop', 'n')
    s.add_argument('--coautor', help='la línea Co-Authored-By del squash, sobre la de .sf/proyecto.json')
    s.add_argument('--prueba')
    s.add_argument('--commit', help='sin rama: el commit o la versión del cierre')
    orden('reobservar', o_reobservar, 'devuelve a observación una cerrada, con su commit de develop', 'n')
    orden('descartar', o_descartar, 'borra la rama y la deja descartada', 'n')
    orden('limpiar', o_limpiar, 'saca de la cola las descartadas')
    s = orden('revertir', o_revertir, 'git revert en develop de sus commits; después, eliminada o a Pendientes', 'n')
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument('--eliminar', action='store_true', help='sale de la cola sin rastro, como con la E')
    g.add_argument('--pendiente', action='store_true', help='vuelve a Pendientes, en cola y reabierta, sin rama')
    s.add_argument('--commit', nargs='+', help='los commits que revertir, si no están en el historial')
    s = orden('reabrir', o_reabrir, 'vuelve a en curso, con rama nueva desde develop', 'n', 'texto')
    s.add_argument('--en-cola', action='store_true')
    s.add_argument('--rama', help='nombre de la rama nueva (por omisión, el de la anterior)')
    s.add_argument('--sin-activar', action='store_true')
    orden('eliminar', o_eliminar, 'sale de la cola, sin rama ni trabajo', 'n')
    orden('restaurar', o_restaurar, 'devuelve a la cola una eliminada', 'n')
    orden('a-propuesta', o_a_propuesta, f'de en cola, sin rama, a propuesta de {PROPUESTAS}; sale de la cola', 'n')
    s = orden('de-propuesta', o_de_propuesta, f'propuesta por decidir de {PROPUESTAS} a tarea en cola', 'texto')
    s.add_argument('--numero', help='su número fijo, P07, si lo tiene')
    s.add_argument('--descripcion')
    s.add_argument('--tipo', choices=TIPOS)
    s.set_defaults(en_curso=False)
    s = orden('fusionar', o_fusionar, 'junta tareas en la de número más alto')
    s.add_argument('ids', type=int, nargs='+')
    orden('split', o_split, 'separa pasos en una tarea nueva', 'n', 'pasos')
    orden('copias', o_copias, 'lista las copias de la cola')
    orden('recuperar', o_recuperar, 'pone una copia como cola', 'copia')
    s = orden('choques', o_choques, 'archivos que comparte con las en curso o en observación (sale con 3 si hay)', 'n')
    s.add_argument('--archivos', nargs='+', help='los archivos previstos, si aún no tiene rama')
    s = orden('decision', o_decision, f'registra una decisión en {DECISIONES} y su índice, con commit en develop', 'titulo')
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument('--archivo', help='el archivo con el texto de la decisión (UTF-8)')
    g.add_argument('--texto', help='el texto de la decisión')
    s.add_argument('--numero', type=int, help='reescribe la decisión con ese número, sin cambiar su nombre')
    s.add_argument('--coautor', help='la línea Co-Authored-By del commit')
    s.add_argument('--push', action='store_true', help='sube develop a su remoto tras el commit')
    s = orden('subir', o_subir, 'sube develop a su remoto, con la revisión de lo que sale (decisión 259)')
    s.add_argument('--repetir', help='cómo se da el permiso si la revisión lo pide (el panel: volver a pulsar develop)')
    s = orden('encargo', o_encargo, 'la parte fija del encargo de su subagente', 'n')
    s.add_argument('--coautor', help='la línea Co-Authored-By de los commits')
    return p


def salida_utf8() -> None:
    """UTF-8 en stdout y stderr, sea cual sea la consola o la redirección (en Windows, cp1252)."""
    for flujo in (sys.stdout, sys.stderr):
        if hasattr(flujo, 'reconfigure'):
            flujo.reconfigure(encoding='utf-8')


def main(argv: list | None = None) -> int:
    salida_utf8()
    a = analizador().parse_args(argv)
    raiz = getattr(a, 'raiz', Path.cwd())
    como_json = getattr(a, 'json', False)
    cola = Cola(raiz, getattr(a, 'quien', 'principal'), getattr(a, 'via', 'cli'))
    try:
        try:
            if a.orden not in SOLO_LECTURA | SIN_COLA:
                cola.bloquear()
            if a.orden not in SIN_COLA:
                cola.cargar()
            mensaje, ok = a.f(cola, a), True
        finally:
            cola.desbloquear()
    except Rechazo as r:
        mensaje, ok = str(r), False
    datos, codigo = (mensaje.datos, mensaje.codigo) if isinstance(mensaje, Consulta) else ({}, 0)
    if como_json:
        print(json.dumps({'ok': ok, 'mensaje': mensaje, **cola.extra, **datos}, ensure_ascii=False))
    else:
        print(mensaje, file=sys.stdout if ok else sys.stderr)
    return codigo if ok else 1


if __name__ == '__main__':
    sys.exit(main())
