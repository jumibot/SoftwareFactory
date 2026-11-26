// La línea del foco y el recordatorio del off-topic en los avisos del mod (decisión 357, 9 y 10; tarea 436). Aparte,
// sin dependencias: lo usan avisos.ts, subagentes.ts y foco.ts, que se importan entre sí por otros caminos.

// El número de una tarea en el chat (tarea 417): dígitos en círculo negro pegados a la T y un espacio detrás de cada uno,
// porque el terminal los pinta más anchos y sin espacio se montan: 392 → «T❸ ❾ ❷ ».
const CIRCULOS = '⓿❶❷❸❹❺❻❼❽❾'
export function numeroTarea(id: number | string): string {
  return 'T' + [...String(id)].map(d => (/[0-9]/.test(d) ? `${[...CIRCULOS][Number(d)]} ` : d)).join('')
}

// La línea del foco, como la escribe Claude: «🅵🅾🅲🆄🆂 `título (T❸ ❾ ❷ )`» (sf:orquestacion, «Cómo escribir»).
export function lineaFoco(f: { id: number; texto: string }): string {
  return `🅵🅾🅲🆄🆂 \`${f.texto} (${numeroTarea(f.id)})\``
}

// El recordatorio, de una línea: solo con el foco guardado en la cola («cola.py foco N») y cuando los avisos del mod
// traen algo de otras tareas; null si no. Sin foco guardado, «libre»: nada que recordar.
export function recordatorioFoco(foco: { id: number; texto: string } | null | undefined, tareas: readonly number[]): string | null {
  if (!foco) return null
  const otras = [...new Set(tareas)].filter(n => n !== foco.id).sort((a, b) => a - b)
  if (!otras.length) return null
  const cuales = otras.length === 1 ? `la ${String(otras[0])}` : `las ${otras.slice(0, -1).join(', ')} y ${String(otras.at(-1))}`
  return (
    `${lineaFoco(foco)} es el foco: lo que estos avisos traen de ${cuales}, y lo que hagas por ellos, va al final ` +
    'como off-topic, sin menús de otras tareas.'
  )
}
