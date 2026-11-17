"""比對三份引用查詢結果：agent A（Semantic Scholar＋citation.js）、agent B（Crossref）、主 agent（OpenAlex）。

用法：python compare_refs.py --s2 s2.json --citejs citejs.json --crossref crossref.json --openalex openalex.json --out refcheck.md
每筆的判定：
  一致         三個來源的 DOI 相同（或三者都查無 DOI、標題相符，常見於 ICLR／NeurIPS 等沒有 DOI 的會議）
  多數一致     兩個來源相同，第三個不同或查無資料：寫出哪個不同（只回傳 arXiv DOI 的來源不算不同）
  不一致       三個來源互不相同
  bib 錯誤     bib 的 DOI 與查到的不同，或 citation.js 解析出的標題、第一作者與 bib 不符
  需更新       bib 引用 arXiv 版或舊年份，但已有正式發表版
  查不到       三個來源都找不到標題相符（match < 0.8）的論文：可能是標題打錯，或論文不存在
輸出 md 表格與 JSON（同檔名 .json），exit 1 表示有需要處理的列。
"""
import argparse, json, sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
ap = argparse.ArgumentParser()
for k in ("s2", "citejs", "crossref", "openalex"):
    ap.add_argument(f"--{k}", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
L = {k: {r["key"]: r for r in json.load(open(getattr(a, k), encoding="utf-8"))}
     for k in ("s2", "citejs", "crossref", "openalex")}


def doi(r):
    """標題相符（match ≥ 0.8）才採用該來源的 DOI；不相符視為查無。"""
    if not r or r.get("status") != "找到" or r.get("match", 0) < 0.8:
        return None
    return (r.get("doi") or "").lower() or "無 DOI"


import re


def is_arxiv(d):
    return bool(d) and d.startswith("10.48550/arxiv")


rows, bad = [], 0
for key, r0 in L["s2"].items():
    src = {"A: S2": doi(r0), "B: Crossref": doi(L["crossref"].get(key)), "主: OpenAlex": doi(L["openalex"].get(key))}
    cj = L["citejs"].get(key, {})
    found = {k: v for k, v in src.items() if v}
    real = [v for v in found.values() if v != "無 DOI"]
    pub = [v for v in real if not is_arxiv(v)]          # 正式發表版的 DOI
    cnt = Counter(pub or real)
    best = cnt.most_common(1)[0][0] if cnt else None
    note = []
    if not found:
        verdict = "查不到"
        note.append("三個來源都找不到標題相符的論文：確認標題，或論文是否存在")
    elif not real:
        verdict = "一致"
        note.append("所有來源都沒有 DOI（例如 OpenReview 會議論文），以標題與年份核對")
    elif len(cnt) > 1 and cnt.most_common(1)[0][1] < 2:
        verdict = "不一致"
        note.append("、".join(f"{k}={v or '查無'}" for k, v in src.items()))
    elif all(src.values()) and all(v == best or is_arxiv(v) for v in src.values()):
        verdict = "一致"
    else:
        verdict = "多數一致"
        note.append("、".join(f"{k}={v or '查無'}" for k, v in src.items() if v != best))
    if any(is_arxiv(v) for v in found.values()) and pub:
        note.append("有來源只回傳 arXiv 版 DOI，正式版是 " + best)
    bib_doi = (r0.get("bib_doi") or "").lower().removeprefix("https://doi.org/")
    bib_arxiv = bool(re.search(r"arxiv|corr", r0.get("bib_venue", ""), re.I))
    if bib_doi and best and bib_doi != best and not (is_arxiv(bib_doi) and pub):
        verdict = "bib 錯誤"
        note.append(f"bib 的 DOI 是 {bib_doi}，查到 {best}")
    if cj.get("status") == "不一致":
        verdict = "bib 錯誤" if verdict in ("一致", "多數一致") else verdict
        note.append(f"citation.js 解析 {cj.get('doi')} 得到「{(cj.get('csl_title') or '')[:60]}」"
                    f"（第一作者 {cj.get('csl_first_family')}），與 bib 的標題或第一作者不符")
    elif cj.get("status") == "DOI 無法解析":
        note.append("citation.js 無法解析 A 的 DOI")
    if pub and (bib_arxiv or is_arxiv(bib_doi)):
        verdict = "需更新" if verdict in ("一致", "多數一致") else verdict
        note.append(f"bib 引用 arXiv 版，已有正式發表版 {best}：改引正式版（期刊／會議名稱、年份、頁碼）")
    elif cj.get("status") == "一致" and cj.get("year_ok") is False:
        verdict = "需更新" if verdict in ("一致", "多數一致") else verdict
        note.append(f"年份：bib {r0.get('bib_year')}，DOI {cj.get('csl_year')}")
    if verdict != "一致":
        bad += 1
    rows.append({"key": key, "verdict": verdict, **src, "citejs": cj.get("status", "—"), "note": "；".join(note)})

order = {"查不到": 0, "不一致": 1, "bib 錯誤": 2, "需更新": 3, "多數一致": 4, "一致": 5}
rows.sort(key=lambda r: order[r["verdict"]])
md = ["| key | 判定 | A: S2 | citation.js | B: Crossref | 主: OpenAlex | 說明 |", "|---|---|---|---|---|---|---|"]
md += [f"| {r['key']} | {r['verdict']} | {r['A: S2'] or '查無'} | {r['citejs']} | {r['B: Crossref'] or '查無'} | "
       f"{r['主: OpenAlex'] or '查無'} | {r['note']} |" for r in rows]
c = Counter(r["verdict"] for r in rows)
head = f"共 {len(rows)} 筆：" + "、".join(f"{k} {c[k]}" for k in order if c[k])
open(a.out, "w", encoding="utf-8").write(head + "\n\n" + "\n".join(md) + "\n")
json.dump(rows, open(a.out.rsplit(".", 1)[0] + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(head)
sys.exit(1 if bad else 0)
