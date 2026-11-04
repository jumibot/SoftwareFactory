import { expect, test } from 'claude-code/testing'
import { ANCHO_LETRAS, ANCHO_LOGO, BARRA, COLOR_BARRA, COLOR_LETRAS, LETRAS, logoSvg, logoTexto } from '../hooks/logo'

// ── El logo «/SF» (tarea 339, decisión 255) ──

test('Logo: la barra y las letras, cinco filas del mismo ancho; 18 columnas en total', () => {
  expect(BARRA.length).toBe(LETRAS.length)
  for (const f of BARRA) expect(f.length).toBe(BARRA[0]!.length)
  for (const f of LETRAS) expect(f.length).toBe(ANCHO_LETRAS)
  expect(ANCHO_LETRAS).toBe(13)
  expect(ANCHO_LOGO).toBe(18)
  // La barra sube hacia la derecha: arriba, a la derecha; abajo, a la izquierda; con hueco antes de la S.
  expect(BARRA[0]!.indexOf('█')).toBeGreaterThan(BARRA.at(-1)!.indexOf('█'))
  for (const f of BARRA) expect(f.endsWith(' ')).toBe(true)
})

test('Logo: con la barra si caben 18 columnas; si no, solo las letras desde 13; por debajo, nada', () => {
  for (const w of [18, 40]) {
    const l = logoTexto(w)
    expect(l.map(x => x.barra)).toEqual(BARRA)
    expect(l.map(x => x.letras)).toEqual(LETRAS)
  }
  for (const w of [13, 17]) {
    const l = logoTexto(w)
    expect(l.every(x => x.barra === '')).toBe(true)
    expect(l.map(x => x.letras)).toEqual(LETRAS)
  }
  expect(logoTexto(12)).toEqual([])
})

test('Logo: el SVG pinta la barra en el morado claro y las letras en el de la SF; sin barra, solo las letras', () => {
  expect(COLOR_LETRAS).toBe('#827dbd')
  const svg = logoSvg(5)
  expect(svg.startsWith('<svg')).toBe(true)
  expect(svg).toContain(`viewBox="0 0 ${ANCHO_LOGO} 10"`)
  expect(svg).toContain(`width="${ANCHO_LOGO * 5}"`)
  expect(svg.indexOf(`fill="${COLOR_BARRA}"`)).toBeLessThan(svg.indexOf(`fill="${COLOR_LETRAS}"`))
  const sola = logoSvg(9, false)
  expect(sola).toContain(`viewBox="0 0 ${ANCHO_LETRAS} 10"`)
  expect(sola).not.toContain(COLOR_BARRA)
  expect(sola).toContain(`fill="${COLOR_LETRAS}"`)
})
