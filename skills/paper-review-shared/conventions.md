# 共用規範

paper-* 系列的 9 個 skill 都先讀本檔。本檔定義工作資料夾、開始前流程、問題編號、`issues.json` 格式與驗證守則。

## skill 與原 12 步的對應

| skill | 原步驟 | 問題編號 | 讀取的上游產出 |
|---|---|---|---|
| paper-motivation-check | 1 | P1-x | 無 |
| paper-survey-and-naive-ideas | 2、3 | P2-x、P3-x | motivation 報告（選用） |
| paper-method-check | 4 | P4-x | survey 報告的不足清單 D1…Dn |
| paper-experiment-check | 5 | P5-x | 不足清單 D1…Dn、預期結果 X1…Xn、設計決策 M1…Mn |
| paper-novelty-positioning | 6、8 | P6-x、P8-x | survey、method、experiment 報告 |
| paper-limitations | 7 | P7-x | 所有已產生的報告 |
| paper-presentation-check | 9 | P9-x | 無 |
| paper-reviewer-personas | 10 | P10-x | 所有已產生的報告（選用） |
| paper-revision | 11、12 | P11-x、P12-x | 所有已產生的報告與 `issues.json` |
| paper-polish | 無（直接改 LaTeX） | 修改編號 C1…Cn | P9-x（presentation）；paper-limitations 報告（選用） |

- 問題編號沿用原 12 步的步驟號。這樣各 skill 的問題可以合併成一份 `issues.json`，PDF 配色也不變。
- 各 skill 可以單獨執行。上游產出不存在時，依各 skill 的「缺少上游產出時」一節處理。

## 工作資料夾
- 在論文 PDF 旁邊建立 `<論文簡稱>_review/`。所有 skill 共用這個資料夾。
- 資料夾內容：

| 檔案 | 寫入者 |
|---|---|
| `understanding.md` | 第一個執行的 skill |
| `issues.json` | 每個 skill 寫入自己步驟的問題 |
| `<skill 名稱>_<zh 或 en>.md` | 各 skill 的報告，例如 `paper-method-check_zh.md` |
| `<論文簡稱>_review_<zh 或 en>.md`、`<原檔名>_annotated.pdf` | paper-revision |

## 開始前

### 1. 讀論文
- 讀完整篇論文，包含 appendix 與 supplementary。
- PDF 先用 markitdown 或 pdf-reading skill 讀取文字。有 LaTeX 原始檔時一併讀取。
- 圖表要看圖本身：用 PyMuPDF `page.get_pixmap(dpi=200)` 把頁面轉成圖片。不只看 caption。

### 2. 選擇設定
- `issues.json` 已有 `meta` 時，沿用其中的設定，不再詢問。
- 否則用 AskUserQuestion 一次問完以下問題。使用者在請求中已說明的項目不再問。

| 問題 | 選項 |
|---|---|
| 報告語言 | 中文版／英文版 |
| 論文來源 | 自己的論文／別人的論文 |
| 目標會議 | ICLR／NeurIPS／CVPR／ICML（可自行填寫） |

- 中文版：報告用繁體中文撰寫，術語保留英文，並遵守 `writing-rules.md` 的中文規範。
- 英文版：報告用英文撰寫，並遵守 `writing-rules.md` 的英文規範（E1–E21）。
- 論文本文依論文本身的語言選用規範檢查，不受報告語言影響。
- 自己的論文：每個問題標 A 類或 B 類（見「問題」）。
- 目標會議：決定頁數上限、匿名規定與評分標準。不確定規定時，用 WebSearch 查詢該會議當年的 author guidelines。
- 把設定寫進 `issues.json` 的 `meta`。

### 3. 複述理解
- `understanding.md` 已存在且標示「使用者已確認」時，讀取它，不再複述。
- 否則逐項列出以下內容，每項 1–2 句：問題、方法、主要 claim、實驗、貢獻、Novelty。
- 使用者確認後才繼續。使用者修正時，以修正後的理解為準。
- 把確認後的內容寫進 `understanding.md`，最上方寫「使用者已確認：YYYY-MM-DD HH:MM」。

## 問題
- 每個判斷都標出依據位置（Sec.、Eq.、Fig.、Table、頁碼）。
- 論文沒寫的內容標「論文未提及」。不替作者補充。
- 嚴重度：
  - Fatal：足以導致 reject。例如 claim 沒有實驗支持、baseline 不公平、主結果不顯著、證明有誤。
  - Major：reviewer 會要求補充，但不至於直接 reject。
  - Minor：寫作、格式或用詞問題。
- 編號：P<步驟>-<序號>，例如 P5-2。
- 自己的論文再標類別：
  - A 類（本質問題）：需要改寫 claim、補做或重做實驗、重做 paper survey，或修改方法與理論。
  - B 類（呈現問題）：行文、連貫性、AI 痕跡、術語、圖表。內容不變。
- 報告與每一節都先寫結論，再寫細節。
- 不得省略：禁止「其餘同理」、「以相同標準檢查」這類跳過的寫法。某項真的做不到時（例如無法上網），寫進報告的「範圍與限制」一節，說明沒做什麼、原因與影響。
- 不得套版：每則評論都要提到該處獨有的內容，例如 panel 編號、座標軸名稱、符號或原句用字。

## 驗證守則（借鑑 Google Deep Review）
- 數學：逐步重推每個推導。檢查不等號方向、遺漏的絕對值、重複定義的符號、off-by-one、維度是否一致。
- 定理：嘗試構造反例。找到反例時列為 Fatal。判斷證明有誤之前，再推導一次。
- 演算法：pseudo-code、文字描述與公式是否一致。
- 跨段一致性：abstract、introduction、結論中的數字與 claim 是否與表格一致。
- 引用：用 paper-search 或 WebSearch 確認被引用的論文存在，且作者與年份正確。
- 回報前重新確認每個問題。無法確認的問題刪除，或標「待確認」。寧可少報，不要誤報。

## issues.json
- 每個 skill 只新增或取代自己步驟的項目，不動其他步驟的項目。
- 寫入方式：讀取 → 刪除自己步驟的舊項目 → 加入新項目 → 寫回。檔案不存在時新建。
- `sentence` 必須從 `page.get_text()` 抽出的文字逐字複製整句。
- `page` 是原論文的頁碼（從 1 開始）。無法定位時設為 `null`。
- 別人的論文 `category` 設為 `null`。

```json
{
  "meta": {"title": "...", "mode": "own 或 others", "venue": "ICLR 2027",
           "language": "zh 或 en", "time": "2026-11-14 16:12"},
  "issues": [
    {"id": "P5-1", "step": 5, "severity": "Fatal", "category": "A",
     "kind": "text", "page": 8,
     "sentence": "從 PDF 抽出的整句原文，逐字複製",
     "fields": {"問題": "...", "原因": "...", "建議改法": "..."}},
    {"id": "P9-6", "step": 9, "severity": "Minor", "category": "B",
     "kind": "figure", "figure": "Fig. 1", "page": 3,
     "fields": {"問題": "...", "原因": "...", "建議改法": "..."}},
    {"id": "P12-1", "step": 12, "severity": "Major", "category": "B",
     "kind": "note", "page": null,
     "fields": {"問題": "...", "原因": "...", "建議改法": "..."}}
  ],
  "figures": [
    {"figure": "Fig. 1", "page": 3,
     "fields": {"總評": "...", "區塊切分": "...", "切分的問題與改法": "...",
                "零先備知識檢查": "...", "正確性": "...", "可讀性": "...",
                "精簡": "...", "美觀": "..."}}
  ],
  "reading_guide": [
    {"id": "R1", "kind": "text", "page": 2, "sentence": "...",
     "fields": {"這段在講什麼": "...", "為什麼重要": "...",
                "怎麼讀": "...", "前後關聯": "..."}}
  ],
  "handoff": {
    "deficits": [{"id": "D1", "text": "...", "source": "Sec. 2"}],
    "design_decisions": [{"id": "M1", "block": "...", "addresses": ["D1"]}],
    "expected_results": [{"id": "X1", "text": "...", "tests": ["M1"]}]
  }
}
```

- `figures` 由 paper-presentation-check 寫入。`reading_guide` 由 paper-revision 寫入。
- `handoff` 存放 skill 之間傳遞的清單。`deficits` 由 paper-survey-and-naive-ideas 寫入，`design_decisions` 與 `expected_results` 由 paper-method-check 寫入。

## 每份報告的固定結構
1. 結論：3–5 句。
2. 本 skill 的各項檢查，依 SKILL.md 的順序。
3. 問題表：編號、嚴重度、類別（自己的論文）、位置、問題、建議改法。
4. 交接：寫給下游 skill 的清單（若有）。
5. 範圍與限制：沒做到的項目、原因與影響；缺少的上游產出。

## 工具替代（非 Claude 環境）

| 原工具 | 替代方式 |
|---|---|
| markitdown／pdf-reading skill | 用 PyMuPDF 的 `page.get_text()` 讀文字，`page.get_pixmap()` 轉圖片看圖 |
| AskUserQuestion | 用文字列出選項詢問 |
| paper-search（OpenAlex） | 呼叫 OpenAlex API：`https://api.openalex.org/works?search=<標題>`；被引用用 `filter=cites:<work id>`；參考文獻看該筆的 `referenced_works` |
| WebSearch | 使用該環境的網頁搜尋 |
| SendUserFile | 提供檔案下載 |
