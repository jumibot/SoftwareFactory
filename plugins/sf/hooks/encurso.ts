import { atom, read, update } from 'claude-code'
import type { Peticion } from '../types'
import { PETICIONES } from './constantes'
import { esperaAlPropietario, listaParaProbar } from './cola'
import { conAbsorbidas, leerPeticiones, leerSubagentes, raizSesion } from './lectura'
import type { SubagentesDeTareas } from './lectura'
import type { $ } from './lectura'

// ── Las tareas en curso en el contexto (tarea 442, decisión 284) ──
// Con cada mensaje del propietario, con la SF activa, el mod pone en el contexto del principal las tareas en curso:
// una línea por tarea con su número, su título corto, si está lista para probar o espera al propietario, y cómo está
// su subagente. Así no tiene que lanzar `cola.py lista` antes de contestar; `lista` queda para lo demás (las de la
// cola, las de observación, los pasos).
// Si no ha cambiado desde el último mensaje que la llevó, una sola línea, «Tareas en curso: sin cambios.», y no nada:
// cuesta unas pocas palabras y le dice al principal que la lista que ya tiene sigue valiendo; sin ella no distinguiría
// «sin cambios» de «el mod no ha podido leer la cola» y tendría que volver a consultarla. La lista entera, otra vez,
// al empezar la sesión, tras /clear y tras compactar (el principal ya no la tiene) y tras recargar el mod.
// Sin pasos ni otros detalles: cada paso marcado volvería a mandar la lista entera.

export const CABECERA_EN_CURSO = 'Tareas en curso'
export const SIN_CAMBIOS = `${CABECERA_EN_CURSO}: sin cambios.`
export const NINGUNA = `${CABECERA_EN_CURSO}: ninguna.`
// El título, cortado por palabras hasta este largo.
export const LARGO_TITULO = 50

// La última lista dada al principal en esta conversación; null, ninguna (la sesión empieza, /clear, compactar).
const enCursoDado = atom({ plugin: 'sf', key: 'enCursoDado' } as const, null as string | null)

export function tituloCorto(texto: string, largo = LARGO_TITULO): string {
  const t = texto.replace(/\s+/g, ' ').trim()
  if (t.length <= largo) return t
  const corte = t.slice(0, largo)
  const espacio = corte.lastIndexOf(' ')
  return `${(espacio > largo / 2 ? corte.slice(0, espacio) : corte).replace(/[\s,;:.]+$/, '')}…`
}

// Cómo está el subagente de la tarea, como el ● y el ○ del panel, pero diciendo si espera o se detuvo: al que espera
// se le retoma; al detenido, no.
function subagenteDe(id: number, s: SubagentesDeTareas): string {
  if (s.subagentes[id] !== undefined) return 'subagente trabaja'
  if (s.subagentesEsperando[id] !== undefined) return 'subagente parado, espera instrucciones'
  if (s.subagentesParados[id] !== undefined) return 'subagente detenido'
  return 'sin subagente'
}

// El bloque de las tareas en curso, por número: «- 442 «título» · lista para probar · subagente trabaja».
export function bloqueEnCurso(peticiones: Peticion[], s: SubagentesDeTareas): string {
  const enCurso = peticiones.filter(p => p.estado === 'en-curso').sort((a, b) => a.id - b.id)
  if (!enCurso.length) return NINGUNA
  const subs = conAbsorbidas(s, peticiones)
  const lineas = enCurso.map(p => {
    const partes = [`- ${String(p.id)} «${tituloCorto(p.texto)}»`]
    if (listaParaProbar(p)) partes.push('lista para probar')
    if (esperaAlPropietario(p)) partes.push('espera al propietario')
    partes.push(subagenteDe(p.id, subs))
    return partes.join(' · ')
  })
  return `${CABECERA_EN_CURSO} (las demás, con \`cola.py lista\`):\n${lineas.join('\n')}`
}

// Lo que va en el contexto: la lista si ha cambiado (o no se ha dado en esta conversación), y si no, SIN_CAMBIOS.
export const textoEnCurso = (bloque: string, dado: string | null) => (bloque === dado ? SIN_CAMBIOS : bloque)

// Lee la cola y los subagentes y toma el texto del contexto, dándolo por dado; con devolver, si el mensaje no llega a
// enviarse, la lista vuelve a contar como no dada. Sin cola (una carpeta sin SF) o si no se puede leer, null: no se
// dice nada y la lista dada sigue siendo la de antes.
export async function tomarEnCurso($: $): Promise<{ texto: string; devolver: () => Promise<void> } | null> {
  const raiz = await raizSesion($)
  if (!(await $.fs.exists(`${raiz}/${PETICIONES}`))) return null
  const cola = await leerPeticiones($, raiz)
  if (cola.error) return null
  const { subagentes, subagentesEsperando, subagentesParados } = await leerSubagentes($)
  const bloque = bloqueEnCurso(cola.peticiones, { subagentes, subagentesEsperando, subagentesParados })
  const dado = await read($, enCursoDado)
  await update($, enCursoDado, () => bloque)
  return { texto: textoEnCurso(bloque, dado), devolver: () => update($, enCursoDado, v => (v === bloque ? dado : v)) }
}

// Al empezar la sesión, tras /clear y tras compactar: el principal ya no tiene la lista; el siguiente mensaje la lleva entera.
export async function olvidarEnCurso($: $): Promise<void> {
  await update($, enCursoDado, () => null)
}
