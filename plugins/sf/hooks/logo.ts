// ── El logo «/SF» (tarea 339, decisión 255) ──
// Una barra delante de SF, para que recuerde la orden /sf que abre el panel: estrecha y empinada (≈79°), pixelada
// como las letras, y en otro color para que se lea como tecla y no como ruta. En un terminal sin color real la barra
// queda del color de las letras: se sigue leyendo «/SF», y está bien así.

// Los colores del logo oscuro del estilo de la SF (docs/identidad/logo-oscuro.svg, decisión 335), porque el panel se
// pinta sobre fondo oscuro: las letras en su amarillo (primario) y la barra en su texto claro.
export const COLOR_LETRAS = '#f5c400'
export const COLOR_BARRA = '#f2f2f0'
// Con el tema claro, los del logo claro (docs/identidad/logo.svg): las letras en tinta y la barra en el amarillo
// (tarea 395).
export const COLOR_LETRAS_CLARO = '#25283a'
export const COLOR_BARRA_CLARO = '#f5c400'

// El modo del logo: claro con un tema claro de Claude Code; oscuro con cualquier otro, sin ajuste o «auto» (tarea 395).
export type ModoLogo = 'claro' | 'oscuro'
export function modoDeTema(tema: unknown): ModoLogo {
  return typeof tema === 'string' && tema.startsWith('light') ? 'claro' : 'oscuro'
}
export function coloresLogo(modo: ModoLogo): { barra: string; letras: string } {
  return modo === 'claro' ? { barra: COLOR_BARRA_CLARO, letras: COLOR_LETRAS_CLARO } : { barra: COLOR_BARRA, letras: COLOR_LETRAS }
}

// «SF» en letra de bloques, cinco filas de 13 columnas.
export const LETRAS = [
  '▄█████ ██████',
  '██     ██    ',
  '▀████▄ █████ ',
  '    ██ ██    ',
  '█████▀ ██    ',
]
// La barra, cinco filas de 4 columnas y una de hueco, el mismo que hay entre S y F.
export const BARRA = [
  '  ██ ',
  ' ▄█▀ ',
  ' ██  ',
  '▄█▀  ',
  '██   ',
]
export const ANCHO_LETRAS = LETRAS[0]!.length
export const ANCHO_LOGO = BARRA[0]!.length + ANCHO_LETRAS

// Las filas del logo de texto para w columnas: con la barra si cabe (18); si no, solo las letras (13), antes que
// quitarlo; por debajo, ninguna. Barra y letras van aparte para pintarlas cada una con su color.
export type FilaLogo = { barra: string; letras: string }
export function logoTexto(w: number): FilaLogo[] {
  if (w >= ANCHO_LOGO) return LETRAS.map((letras, i) => ({ barra: BARRA[i]!, letras }))
  if (w >= ANCHO_LETRAS) return LETRAS.map(letras => ({ barra: '', letras }))
  return []
}

// El logo como SVG, para las superficies gráficas (la app de escritorio, VS Code, el móvil): allí los bloques ▄█▀ van
// en una fuente que no los dibuja a una celda y el logo se descuadra (tarea 323). Cada carácter, una celda de 1×2:
// █ entera, ▄ la mitad de abajo, ▀ la de arriba. Sin barra, solo las letras. Los colores son los del logo oscuro, y
// con la app en modo claro, los del claro, por prefers-color-scheme dentro del propio SVG (tarea 395).
function rects(filas: string[], x0: number): string {
  const r: string[] = []
  filas.forEach((fila, y) =>
    [...fila].forEach((c, x) => {
      const [dy, alto] = c === '█' ? [0, 2] : c === '▄' ? [1, 1] : c === '▀' ? [0, 1] : [0, 0]
      if (alto > 0) r.push(`<rect x="${x + x0}" y="${y * 2 + dy}" width="1.04" height="${alto + 0.04}"/>`)
    }),
  )
  return r.join('')
}
export function logoSvg(celda = 9, conBarra = true): string {
  const x0 = conBarra ? BARRA[0]!.length : 0
  const w = x0 + ANCHO_LETRAS
  const h = LETRAS.length * 2
  const barra = conBarra ? `<g class="barra" fill="${COLOR_BARRA}">${rects(BARRA, 0)}</g>` : ''
  const claro = `<style>@media (prefers-color-scheme: light) { .barra { fill: ${COLOR_BARRA_CLARO} } .letras { fill: ${COLOR_LETRAS_CLARO} } }</style>`
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w * celda}" height="${h * celda}" shape-rendering="crispEdges">${claro}${barra}<g class="letras" fill="${COLOR_LETRAS}">${rects(LETRAS, x0)}</g></svg>`
}
