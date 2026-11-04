# Migración de la carpeta de trabajo de la SF al clon público (328, decisión 252)

`<proyectos>` es la carpeta que contiene la de trabajo de la SF en el equipo del propietario.

Estado al 2026-11-04: público jumibot/SoftwareFactory con main = develop = 25d6406 (v1.7.6). Carpeta actual
<proyectos>/SoftwareFactory con origin en SoftwareFactory-historia (privado), develop 409b458, sin historia común
con el público. Diferencia de árboles público→develop: 108 archivos, casi todo docs (decisiones 253-279, sprints y
sus _respaldo); en código solo crear_documentos y documento_vision; plugin.json 1.6.2 (sub-328 lo deja en 1.7.6).
Sin rutas, correos ni secretos en esa diferencia (búsqueda de usuario y rutas de la máquina, correos y tokens).

Nada se sube hasta el paso 9. Hasta ahí, volver atrás = borrar la carpeta nueva.

## Antes (con el propietario)
0. Decidir: (a) OK a que develop y las ramas sean públicas desde ya; (b) plugins/sf/tsconfig.json (sin seguimiento):
   añadir, ignorar o borrar; (c) si los `_respaldo/` de informes salen públicos; (d) si se cierra antes la 332
   (revision_publica.py) o se revisa a mano.
1. Parar el trabajo: ningún subagente activo. Cada uno con trabajo sin commit (hoy 345: 1, 346: 2, 350: 1, 351: 4
   archivos) hace commit en su sub-NN y lo entrega a su feature/NN (merge). Comprobar: `git -C <wt> status --short`
   vacío en todos y `git rev-list --count feature/NN..sub-NN` = 0. Cerrar la 328 queda para después (es la migración).
2. Copia de seguridad (en la carpeta vieja):
   `git bundle create <proyectos>/SF-historia-2026-11-04.bundle --all`
   y copiar `.sf/`, `.claude/settings.local.json`, `plugins/sf/tsconfig.json` y, si existe,
   `.git/sf-revision.json` a <proyectos>/SF-copia-2026-11-04/. (Opcional: `git push origin --all` a la historia
   privada para dejarla con el último estado.)

## Clon nuevo
3. `git clone https://github.com/jumibot/SoftwareFactory.git <proyectos>/SoftwareFactory-nuevo`
   `cd <proyectos>/SoftwareFactory-nuevo && git checkout develop`
   `git config user.email <el correo de git del propietario>` (el local de la carpeta vieja, que no es el global).
   `git config core.longpaths true` (hay nombres de decisiones de más de 150 caracteres; en rutas largas falla).

Ensayado el 2026-11-04 en una carpeta temporal (sin subir nada): pasos 3, 4, 5 y 7 salen limpios; develop nuevo
difiere del viejo solo en plugin.json, y las 7 ramas con contenido se aplican sin conflicto.
4. Traer las ramas viejas a refs aparte (no se suben nunca con `git push origin <rama>`):
   `git fetch <proyectos>/SoftwareFactory "+refs/heads/*:refs/historia/*"`
5. develop = árbol del develop viejo + versión publicada, encima del develop público:
   `git read-tree -u --reset refs/historia/develop`
   `sed -i 's/"version": "1.6.2"/"version": "1.7.6"/' plugins/sf/.claude-plugin/plugin.json && git add -A`
   `git commit -m "develop de la SF, traído de la historia privada (328)"`
   Comprobar: `git diff refs/historia/develop develop --stat` = solo plugin.json; `git log --oneline -2` = este commit
   sobre 25d6406.
6. Revisión de lo que saldría: `git diff origin/develop develop` con revision_publica.py (si la 332 está cerrada) o
   a mano (rutas de la máquina, correos, tokens, documentos internos).
7. Ramas en curso, una a una, cada una en un commit sobre el develop nuevo (diff de tres puntos = solo lo suyo, aunque
   esté atrasada):
   `git checkout -b feature/NN-x develop`
   `git diff --binary refs/historia/develop...refs/historia/feature/NN-x | git apply --3way --index`
   `git commit -m "Lo hecho en la tarea, traído de la historia (NN)"`
   Con contenido: 332, 333, 337, 338, 339, 342, 352 (y las que el paso 1 llene). Vacías (345, 346, 350, 351): solo
   `git branch feature/NN-x develop`. La 328: su cambio ya va en develop (paso 5) → `git branch feature/328-version-publicada develop`.
   La 333 es la rama activa hoy en la carpeta vieja (modo prueba): dejar el clon nuevo en develop.
8. Copiar a la carpeta nueva: `.sf/` entera (cola, historial, copias, registro, subagentes; prueba.json/log solo si
   se sigue probando la 333), `.claude/settings.local.json`, lo decidido de tsconfig.json y `sf-revision.json` al
   `.git/` nuevo si existía. `.sf/publicable.txt`, si existe, va en el repositorio (no está ignorado).

## Subir y cambiar de carpeta
9. (OK del propietario) `git push -u origin develop` y, si se quiere, `git push -u origin feature/NN-x` de cada una.
   Nunca `--all` ni `--mirror` (subirían refs/historia).
10. Quitar las refs viejas del clon: `git for-each-ref --format="%(refname)" refs/historia | xargs -n1 git update-ref -d`
11. Cerrar Claude Code y el panel en la carpeta vieja. En la vieja: `git worktree remove <proyectos>/SoftwareFactory-wt-NN`
    de cada uno (están limpios por el paso 1; las ramas sub-NN quedan en el bundle) y `git worktree prune`.
12. Renombrar: SoftwareFactory → SoftwareFactory-historia, SoftwareFactory-nuevo → SoftwareFactory. La ruta final es
    la misma: memoria del proyecto, marketplace local (`<proyectos>`) y rutas de .sf/subagentes.json siguen valiendo.
13. Rehacer los worktrees de las tareas en curso desde la carpeta nueva:
    `git worktree add <proyectos>/SoftwareFactory-wt-NN -b sub-NN feature/NN-x`

## Comprobar después
14. `git remote -v` → jumibot/SoftwareFactory; `git log develop --oneline -3` sobre 25d6406; `git worktree list`.
15. `python -I -X utf8 "$HOME/.claude/sf/cola.py" lista` (o la orden de listar) lee la cola entera.
16. `claude plugin test plugins/sf` y `python -m pytest -q plugins/sf/tests` en develop.
17. El panel enseña «SF 1.7.6»; `cola.py decision` hace su commit en develop; un RELEASE de prueba (sin publicar) mira
    el remoto público y lanza la revisión.
18. Si sale mal antes del paso 9: borrar SoftwareFactory-nuevo (o deshacer el renombrado). Después del 9: lo subido es
    público; corregir con un commit nuevo, no reescribiendo (force push solo con OK expreso).

## Hecho el 2026-11-04 (pasos 2 a 8 y 10), con la decisión 280
- 0: decidido por la 280 (develop público, ramas de tarea locales, `_respaldo/` públicos); tsconfig.json ya ignorado;
  la 332 cerrada, así que la revisión la hace `plugins/sf/tools/revision_publica.py`.
- 1: solo quedaban en curso con rama la 328 y la 337, con sus worktrees limpios; las sub-NN de las tareas cerradas
  (342, 345, 346, 350, 351, 352) ya estaban en develop por squash y quedan solo en el bundle.
- 4: el fetch de las ramas trae también los tags de la historia (v1.0.0…v1.6.2). Se borraron del clon los que no
  están en el público, para que un `git push --tags` no los suba. En otra migración: `git fetch --no-tags …`.
- 5: develop nuevo = develop viejo (21d4e91) con plugin.json en 1.7.6, un commit sobre 25d6406.
- 6: la revisión da 4 hallazgos, todos datos de prueba de `clave()`/`claveIncorporacion` (rutas de ejemplo con
  la unidad y la carpeta de proyectos de la máquina) en `tests/panel.test.tsx` y `tests/test_incorporacion.py`;
  cambiados por rutas ficticias en develop antes de subir. Las demás rutas ya estaban publicadas.
- 7: solo hay ramas de la 328 y la 337; la 337 aplicada sin conflicto.

## Hecho el 2026-11-04 (pasos 9 y 11 a 17)
- 9: subido develop (9f321f8, sobre 25d6406); origin queda con solo develop y main, y tags v1.7.0 a v1.7.6.
- 11 y 12: el script de la mudanza falló al renombrar: Windows no deja renombrar una carpeta que tiene abierta otro
  proceso (una sesión de Claude Code, un terminal o un editor sobre ella o sobre un worktree suyo). El renombrado y
  los worktrees se terminaron a mano, sin pérdidas.
- 13 a 16: worktree de la 328 rehecho; plugin.json dice 1.7.6; `claude plugin validate plugins/sf` pasa;
  `claude plugin test plugins/sf`: 407 pruebas bien, ninguna mal; pytest: 291 bien.
- 17: RELEASE, en esta carpeta, usa el remoto origin (el público), publica develop en main y parte del último tag
  (v1.7.6). La revisión de lo que va de v1.7.6 a develop da «seguir», sin hallazgos, y ve el repositorio como
  público. Queda mirar en el panel la versión y que `cola.py decision` haga su commit en develop.

**Aprendido para otra mudanza:** antes de renombrar, cerrar todas las sesiones de Claude Code, terminales y editores
abiertos en la carpeta y en sus worktrees; y que el script pare con un aviso claro si el renombrado falla.
