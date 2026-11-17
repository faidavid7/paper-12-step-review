"""用一個書目資料庫查每筆參考文獻的 DOI 與 metadata（Compliance 的引用驗證）。

用法：python lookup.py <refs.bib> --source s2|crossref|openalex --out <結果.json>
  s2        Semantic Scholar API（agent A）
  crossref  Crossref API（agent B）
  openalex  OpenAlex API（主 agent 自己查）
每筆輸出：key、bib 的標題／年份／第一作者、查到的 doi、title、year、authors、venue、arxiv、match（標題相似度 0–1）。
只送出被引用論文的標題，不送出審查中論文的內容。失敗最多重試 3 次並退避。
"""
import argparse, json, re, sys, time, unicodedata, urllib.parse, urllib.request
from difflib import SequenceMatcher

sys.stdout.reconfigure(encoding="utf-8")
import os
UA = {"User-Agent": "paper-12-step-review-citation-check/1.0"}
S2H = dict(UA, **({"x-api-key": os.environ["S2_API_KEY"]} if os.environ.get("S2_API_KEY") else {}))


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = re.sub(r"\\[a-zA-Z]+|[{}$\\]", "", s)
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def sim(a, b):
    return round(SequenceMatcher(None, norm(a), norm(b)).ratio(), 3)


def parse_bib(text):
    """簡單的 BibTeX 解析：@type{key, field = {…} 或 "…" 或數字, …}。"""
    out = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        if m.group(1).lower() in ("comment", "string", "preamble"):
            continue
        i, depth = m.end(), 1
        while i < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        body, f = text[m.end():i - 1], {}
        for fm in re.finditer(r"(\w+)\s*=\s*", body):
            j = fm.end()
            if j >= len(body):
                continue
            if body[j] == "{":
                d, k = 1, j + 1
                while k < len(body) and d:
                    d += {"{": 1, "}": -1}.get(body[k], 0)
                    k += 1
                val = body[j + 1:k - 1]
            elif body[j] == '"':
                k = body.index('"', j + 1)
                val = body[j + 1:k]
            else:
                val = re.match(r"[^,\n]*", body[j:]).group(0)
            f.setdefault(fm.group(1).lower(), re.sub(r"\s+", " ", val).strip())
        out.append({"key": m.group(2), "type": m.group(1).lower(), **f})
    return out


def get(url, headers=UA, tries=3):
    for t in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2 ** (t + 1) * (5 if e.code == 429 else 1))  # S2 未登入時常回 429
        except Exception:
            time.sleep(2 ** (t + 1))
    return {"_error": True}


def s2(title):
    q = urllib.parse.quote(norm(title))
    d = get(f"https://api.semanticscholar.org/graph/v1/paper/search/match?query={q}"
            "&fields=title,year,authors,venue,externalIds,publicationVenue", S2H, 5)
    if not d or d.get("_error") or not d.get("data"):
        return d if d and d.get("_error") else None
    p = d["data"][0]
    ids = p.get("externalIds") or {}
    return {"doi": ids.get("DOI"), "title": p.get("title"), "year": p.get("year"),
            "authors": [a["name"] for a in p.get("authors", [])], "venue": p.get("venue"),
            "arxiv": ids.get("ArXiv")}


def crossref(title):
    q = urllib.parse.quote(title)
    d = get(f"https://api.crossref.org/works?query.bibliographic={q}&rows=3"
            "&select=DOI,title,issued,author,container-title,type")
    if not d or d.get("_error"):
        return d
    items = d.get("message", {}).get("items", [])
    if not items:
        return None
    p = max(items, key=lambda x: sim(title, (x.get("title") or [""])[0]))
    return {"doi": p.get("DOI"), "title": (p.get("title") or [""])[0],
            "year": (p.get("issued", {}).get("date-parts") or [[None]])[0][0],
            "authors": [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in p.get("author", [])],
            "venue": (p.get("container-title") or [""])[0], "arxiv": None, "type": p.get("type")}


def openalex(title):
    q = urllib.parse.quote(norm(title))
    d = get(f"https://api.openalex.org/works?search={q}&per-page=3")
    if not d or d.get("_error"):
        return d
    items = d.get("results", [])
    if not items:
        return None
    p = max(items, key=lambda x: sim(title, x.get("title") or ""))
    doi = (p.get("doi") or "").replace("https://doi.org/", "") or None
    loc = (p.get("primary_location") or {}).get("source") or {}
    return {"doi": doi, "title": p.get("title"), "year": p.get("publication_year"),
            "authors": [a["author"]["display_name"] for a in p.get("authorships", [])],
            "venue": loc.get("display_name"), "arxiv": None}


ap = argparse.ArgumentParser()
ap.add_argument("bib", nargs="+")
ap.add_argument("--source", required=True, choices=["s2", "crossref", "openalex"])
ap.add_argument("--out", required=True)
ap.add_argument("--keys", help="只查這些 key（逗號分隔），例如只查內文有引用的")
a = ap.parse_args()
fn = {"s2": s2, "crossref": crossref, "openalex": openalex}[a.source]
gap = {"s2": 1.2 if os.environ.get("S2_API_KEY") else 3.5, "crossref": 0.3, "openalex": 0.2}[a.source]
entries = [e for b in a.bib for e in parse_bib(open(b, encoding="utf-8").read())]
if a.keys:
    keep = set(a.keys.split(","))
    entries = [e for e in entries if e["key"] in keep]
res = []
for e in entries:
    t = e.get("title", "")
    r = fn(t) if t else None
    row = {"key": e["key"], "bib_title": t, "bib_year": e.get("year"), "bib_doi": e.get("doi"),
           "bib_first_author": (e.get("author", "").split(" and ")[0]).strip(),
           "bib_venue": " ".join(e.get(k, "") for k in ("journal", "booktitle", "eprint", "archiveprefix", "publisher")).strip()}
    if r and r.get("_error"):
        row["status"] = "查詢失敗"
    elif not r:
        row["status"] = "查無資料"
    else:
        row.update(r, status="找到", match=sim(t, r.get("title")))
        if row["doi"]:
            row["doi"] = row["doi"].lower()
    res.append(row)
    print(f"{e['key']}: {row['status']} {row.get('doi') or ''} {row.get('match', '')}")
    time.sleep(gap)
json.dump(res, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(res)} 筆 → {a.out}")
