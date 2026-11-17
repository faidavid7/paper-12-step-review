// 用 citation.js 解析 DOI（doi.org content negotiation），確認 DOI 指向的論文就是 bib 那一筆。
// 用法：node citejs_check.mjs <lookup 結果.json> --out <citejs.json>
// 對每筆有 doi 的結果：取 DOI 的 CSL-JSON，比對標題、年份、第一作者姓氏。
import { Cite } from '@citation-js/core'
import '@citation-js/plugin-doi'
import fs from 'node:fs'

const [inp, , out] = process.argv.slice(2)
const rows = JSON.parse(fs.readFileSync(inp, 'utf8'))
const norm = s => (s || '').normalize('NFKD').replace(/\\[a-zA-Z]+|[{}$\\]/g, '')
  .toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim()
const sleep = ms => new Promise(r => setTimeout(r, ms))

// 標題相似度：共同單字比例
const sim = (a, b) => {
  const A = new Set(norm(a).split(' ')), B = new Set(norm(b).split(' '))
  const n = [...A].filter(w => B.has(w)).length
  return Math.round(100 * n / Math.max(A.size, B.size, 1)) / 100
}

const res = []
for (const r of rows) {
  const row = { key: r.key, doi: r.doi || null }
  if (!r.doi) { row.status = '沒有 DOI'; res.push(row); continue }
  let d = null
  for (let t = 0; t < 3 && !d; t++) {
    try { d = (await Cite.async(r.doi)).data[0] } catch { await sleep(2000 * (t + 1)) }
  }
  if (!d) { row.status = 'DOI 無法解析'; res.push(row); continue }
  const year = d.issued?.['date-parts']?.[0]?.[0] ?? null
  const fam = d.author?.[0]?.family ?? ''
  row.csl_title = d.title
  row.csl_year = year
  row.csl_first_family = fam
  row.csl_venue = d['container-title'] || ''
  row.title_sim = sim(r.bib_title, d.title)
  row.year_ok = !r.bib_year || !year || String(year) === String(r.bib_year)
  row.author_ok = !fam || norm(r.bib_first_author).includes(norm(fam))
  row.status = row.title_sim >= 0.8 && row.author_ok ? '一致' : '不一致'
  res.push(row)
  console.log(`${r.key}: ${row.status} ${r.doi} title_sim=${row.title_sim} year_ok=${row.year_ok}`)
  await sleep(300)
}
fs.writeFileSync(out, JSON.stringify(res, null, 1))
console.log(`${res.length} 筆 → ${out}`)
