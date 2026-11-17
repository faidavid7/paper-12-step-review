// 用 citation.js 依指定格式輸出參考文獻，預覽 bib 在各格式下的樣子（見 citation-styles.md）。
// 用法：node format_refs.mjs <refs.bib> --style nature|ieee|lncs|acl|apa [--keys a,b] [--out refs_<style>.txt]
// 只用來預覽與找缺漏欄位；論文中的實際格式由會議的 .bst 產生。
import { Cite, plugins } from '@citation-js/core'
import '@citation-js/plugin-bibtex'
import '@citation-js/plugin-csl'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const args = process.argv.slice(2)
const opt = k => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null }
const files = { nature: 'nature', ieee: 'ieee', lncs: 'springer-lecture-notes-in-computer-science',
  acl: 'association-for-computational-linguistics', apa: 'apa' }
const style = opt('--style') || 'ieee'
if (!files[style]) { console.error(`style 只能是 ${Object.keys(files).join('、')}`); process.exit(2) }
plugins.config.get('@csl').templates.add(style, fs.readFileSync(path.join(here, 'csl', files[style] + '.csl'), 'utf8'))

let data = new Cite(fs.readFileSync(args[0], 'utf8')).data
const keys = opt('--keys')
if (keys) { const k = new Set(keys.split(',')); data = data.filter(d => k.has(d.id) || k.has(d['citation-key'])) }
const txt = new Cite(data).format('bibliography', { format: 'text', template: style, lang: 'en-US' })
if (opt('--out')) fs.writeFileSync(opt('--out'), txt)
console.log(txt)
