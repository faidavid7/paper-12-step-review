---
name: paper-polish
description: 在不改動任何實驗的前提下修飾 ML 論文：直接改 LaTeX 原始檔，依 ASD-STE100（英文 E1–E21、中文規範 1–4）改寫文字，修好逐層閱讀與 Causal 問題，處理論文弱點（縮小 claim、在文中先回應、降低易被攻擊的用詞、把 limitation 與 future work 寫進論文），用全篇統一的樣式重畫數據圖（matplotlib）與方法圖（TikZ），重寫 caption，整理表格，並用交付前檢查確認所有實驗數字與公式都沒有改變。使用者要求「修飾論文」「潤稿」「polish paper」「把圖畫漂亮」「改 presentation」「把弱點包起來」「把 limitation 寫進論文」時使用。只要分析該怎麼寫 limitation、不改檔案時，用 paper-limitations。
---

# 論文修飾（Polish）

先讀 `../paper-review-shared/conventions.md`，執行其中的「開始前」。
寫作規則見 `../paper-review-shared/writing-rules.md`。
本 skill 只做不改實驗的修改：B 類（呈現）全部，加上 A 類中只需改寫文字的部分（第 3 節縮小 claim）。修改編號用 C1、C2⋯，有對應的問題編號（例如 P9-x、P7-x）時一併標出。
交付前檢查用本資料夾的 `check_polish.py`。

## 硬限制：不改實驗
以下內容在修飾前後必須完全相同：
- 實驗數字：表格、內文、圖中的每個數值，包括小數位數。
- 公式的數學內容。只能改排版，例如斷行與對齊。
- Claim 不加強。只有在第 3 節「弱點處理」中才可以縮小。
- 實驗設定：資料集、baseline、超參數、seed 數。

發現實驗本身的問題時（A 類），寫進修改紀錄的「未處理」一節，交給使用者決定。不自行修改。

## 修改前先確認
每次修改論文檔案（LaTeX、圖、表格）之前，都先詢問使用者：
- 列出這一批打算做的修改：編號、位置、原文、改後、理由。圖的修改附上改前與改後的圖片。
- 用 AskUserQuestion 詢問是否 OK，選項為「全部 OK」「只改部分（請列出編號）」「都不要改」。沒有 AskUserQuestion 時，用文字詢問。
- 只執行使用者同意的修改。被拒絕的修改寫進修改紀錄，標「使用者未同意」。
- 使用者提出修正時，依修正後的內容執行。
- 一批修改以一個步驟為單位：第 2 節文字、第 3 節弱點處理、第 4 節每張圖、第 4.7 節表格。單一步驟的修改超過 20 處時，分成多批詢問。
- 沒有得到回覆時，不修改。

## 輸入
- LaTeX 原始檔（必要）。沒有原始檔時停下來，向使用者要。
- 編譯後的 PDF。
- 數據圖的原始數據或原本的畫圖程式。沒有時，該圖只改 caption 與 LaTeX 排版。

## 缺少上游產出時
- `issues.json` 有 P9-x 時，用它當修改清單的起點。
- 沒有 P9-x 時，先執行 paper-presentation-check。

## 1. 凍結清單
修改前，從 LaTeX 原始檔抽出以下內容，寫進 `frozen.json`：
- 每個表格的每個儲存格。
- 內文中的每個數字，連同所在的句子。句子只用來定位，不要求句子不變。
- 每個公式環境的內容。
- 每個主要 claim 的原句（摘要、introduction 的貢獻列表、結論）。

```json
{
  "numbers":  [{"value": "83.4", "sentence": "Our method reaches 83.4% accuracy ..."}],
  "tables":   [{"label": "tab:main", "cells": ["83.4", "$\\pm$0.3", "ResNet-50"]}],
  "equations":[{"label": "eq:loss", "body": "\\mathcal{L} = ..."}],
  "claims":   [{"where": "abstract", "sentence": "..."}]
}
```

交付前檢查會用這份清單比對修改後的檔案：
- 數字、表格儲存格：原樣出現在修改後的檔案中。
- 公式：去掉空白、`&`、`\\`、`\nonumber`、`\notag` 後內容相同。只容許斷行與對齊的改變。
- Claim：原句沒有出現時，修改紀錄的弱點處理表必須有這句原句，處理方式為「縮小 claim」。

## 2. 文字
依 presentation-check 的檢查項目逐項修改，不是抽樣。
- 逐層閱讀：依序修好標題、摘要、Figure 1 與 caption、貢獻列表、章節標題、每段第一句。每層都要能獨立讀懂。
- 寫作規則：英文依 E1–E21 改寫，中文依規範 1–4 改寫。
- Causal：每個術語、符號與縮寫在第一次使用處或之前定義。
- 連貫性：每段開頭接上前一段。
- AI 寫作痕跡：刪除空泛強調詞、固定三項並列、段尾重複總結、多餘破折號。
- 冗餘：合併重複的段落。
- 改寫時不加強 claim。例如不把 "improves" 改成 "significantly improves"。
- 每處修改寫進修改紀錄：編號、位置、原文、改後、依據的規則。

## 3. 弱點處理
目標：在不改實驗的前提下，讓弱點不容易被攻擊；無法消除的弱點，寫成具體、有範圍的 limitation 與 future work。

### 3.1 找出弱點
- 有 paper-limitations 報告時，直接用它的分流表與 overclaim 表。
- 沒有時，從 `issues.json` 收集 P5（實驗）、P7（限制）、P10（reviewer 提問）的 Fatal 與 Major 問題。
- 兩者都沒有時，以「嚴苛批評者」與「只花 30 秒的 AC」的角度快速檢查：
  - Claim 是否超出實驗範圍。
  - 提升是否落在 std 之內。
  - 資料集或 task 是否太少。
  - 是否缺少重要的 baseline。
  - 計算成本是否較高。
  - 假設是否過強。
- 每個弱點寫一列：編號、弱點、位置、reviewer 可能怎麼問。

### 3.2 分流
每個弱點選一種或多種處理方式：

| 處理方式 | 適用條件 | 作法 |
|---|---|---|
| 縮小 claim | Claim 超出證據 | 改寫 claim，使範圍與實驗相符。 |
| 先回應 | Reviewer 一定會問，而論文已有答案或理由 | 在 reviewer 會產生疑問的位置，加一句話說明設計理由，或指向既有的實驗與 appendix。 |
| 寫成 limitation | 不影響主 claim，或修正超出本論文範圍 | 依 3.4 撰寫，並接上 future work。 |
| 調整呈現順序 | 主結果強，但有個別較弱的結果 | 在摘要、introduction 與段落開頭先寫最強的證據。較弱的結果仍放在原本的表格與章節，並用一句話說明原因。 |
| 交給使用者 | 要補實驗才能解決 | 寫進「未處理」。不在文字上掩蓋。 |

- Fatal 問題不得只寫成 limitation。列入「未處理」，並在結論中提醒使用者。
- 「先回應」只能引用論文中已經存在的結果或理由，不可以寫出論文沒有的實驗結論。

### 3.3 降低攻擊面的用詞
以下用詞容易被 reviewer 攻擊。只在有對應證據時使用，否則依右欄改寫：

| 容易被攻擊的寫法 | 需要的證據 | 改寫方向 |
|---|---|---|
| state-of-the-art | 比較了該 benchmark 上目前最好的方法 | "outperforms the compared baselines on X" |
| general、universal、any | 跨多種 domain 或規模驗證 | "on the N benchmarks we evaluate" |
| guarantee、prove | 有定理與證明 | "we observe"、"empirically" |
| significantly | 有統計檢定 | 寫出數值與 std |
| because、causes | 有 ablation 或介入實驗 | "is associated with"、"coincides with" |
| the first | 完整的 related work 搜尋 | "to our knowledge, the first" |
| solve、eliminate | 問題完全消失 | "reduce"、"mitigate" |
| robust | 測過擾動或分布偏移 | 寫出測過的條件 |

### 3.4 Limitation 與 future work 的寫法
沿用 paper-limitations 的四個部分：範圍、證據、影響、因應。另外依下列方式寫得完整：
- 寫成適用範圍，不寫成失敗。例如寫 "We evaluate on image classification. Extending to dense prediction requires ..."，不寫 "Our method fails on ..."。
- 每條 limitation 說明為什麼它不影響本論文的主 claim。
- 每條 limitation 接一個具體的 future work：要做什麼，以及它解決哪條 limitation。
- 不把 limitation 寫得比實際嚴重，避免自毀主 claim。
- 不寫空泛的句子，例如 "Our method has some limitations."
- 依目標會議規定擺放：獨立的 Limitations 段落、Conclusion 的一部分，或 checklist。不確定時用 WebSearch 查詢。
- 英文依 E1–E21，中文依規範 1–4。

### 3.5 界線
以下作法不可以使用：
- 刪除不利的結果、baseline 或資料集。
- 把不利結果移到 appendix，正文卻不提。移到 appendix 時，正文要有一句話說明結果並指向該處。
- 用座標軸範圍、顏色或排版淡化不利的結果。
- 寫出與實驗不符的理由或解釋。

理由：reviewer 發現被隱藏的弱點時，扣分比弱點本身更重。誠實寫出範圍，反而降低被攻擊的機會。

## 4. 圖
本節綜合 30 個畫論文圖的 skill（來源見最後一節「圖的規範來源」）。

### 4.1 原則
1. 忠實優先於美觀：
   - 只用原始數據或原畫圖程式重畫。
   - 不從舊圖的點陣圖讀數值。
   - 不刪資料點，也不調整座標軸範圍來放大差異。
   - 缺值留空，不連線。
2. 一張圖一個訊息：畫之前先寫一句話，說明讀者看完這張圖要看到什麼比較。
3. 全篇一致：所有圖共用同一份樣式、同一套顏色對應與字型。
4. 不加論文沒有的東西：
   - 只畫論文已經報告的統計量。
   - 原始數據有多個 seed、論文卻沒有畫誤差時，寫進「未處理」，不自行加上。
   - 顯著性標記只用在論文已經做過檢定的比較。

### 4.2 圖的盤點與規格
為每張圖（正文與 appendix）在 `figures/spec.md` 寫一列：

| 欄位 | 內容 |
|---|---|
| 圖號 | Fig. N |
| 類型 | 數據圖／方法圖／定性結果（圖片） |
| 一句話訊息 | 讀者看完要得到的結論 |
| 資料來源 | 數據檔或畫圖程式的路徑；沒有時寫「無」 |
| 處理方式 | 重畫數據圖／重畫方法圖／只改 caption／保留 |
| 寬度 | `\columnwidth` 或 `\textwidth` |
| 顏色對應 | 每個方法或元件用的顏色 |

同一個方法在每張圖都用同一個顏色。顏色對應只寫一次，所有圖共用。

### 4.3 全篇樣式
寫一份 `figures/paper_style.mplstyle` 給數據圖用，再寫一份 `figures/paper_tikz.tex` 給方法圖用，兩份用同一組 hex 色碼。

**尺寸**
- 在論文中加入 `\typeout{COL=\the\columnwidth, TEXT=\the\textwidth}`，編譯後從 log 讀出欄寬與全文寬。不用記憶中的數字。讀出後刪除這一行。
- `figsize` 的寬度設成實際寬度。LaTeX 用 `width=\linewidth` 放入，不再縮放。這樣圖中字級就等於印出來的字級。
- 高寬比依內容決定，不拉伸。

**字型與字級**
- 數據圖的字型與內文相同：開啟 `text.usetex`，並使用論文 preamble 中的字型套件。
- 方法圖的標籤用 sans-serif，數學變數用論文的 macro（serif 斜體）。
- 印出後的字級：座標軸標籤與刻度 7–9 pt，panel 標籤 9 pt 粗體。最小不低於 6 pt。
- 同一種角色的文字只用一種字級。

**線與框**
- 數據線 1.0–1.5 pt，座標軸 0.5–0.75 pt。
- 去掉上方與右方的框線。
- 格線用淺灰色，或不畫格線。
- 不畫圖內標題。標題寫在 caption。
- 不用背景色、3D、陰影、圓餅圖、漸層。

**顏色**
- 本方法用一個醒目的顏色，例如 Okabe-Ito 藍 `#0072B2`。
- Baseline 用不同深淺的灰色，或其餘的 Okabe-Ito 顏色。
- 一張圖最多 4–5 個顏色。超過時改用線型或拆成多個 panel。
- 顏色一定搭配第二種編碼：marker、線型或直接標籤。
- 不同時用紅色與綠色區分類別。
- 連續值用 `viridis` 或 `cividis`。有中心點的值用 `RdBu`，並把中心設在 0。
- 不用 `jet` 或 `rainbow`。

**座標軸**
- 標籤寫出量與單位，例如 "Training steps (k)"。不用程式變數名稱。
- 長條圖從 0 開始。
- 要互相比較的 panel 用相同的座標軸範圍。
- Log 座標要在軸標籤註明。
- 每軸約 4–6 個刻度。

**圖例**
- 5 條以下的線，直接在線尾標名稱，不放圖例框。
- 需要圖例時，順序與圖中由上到下的順序相同，不依字母排序。
- 圖例不加框，放在不遮住資料的位置。
- 多個 panel 共用一個圖例。

**誤差**
- 依論文已報告的統計量畫 error bar 或區帶。
- Caption 寫明是 std、SE 還是 CI，以及 seed 數。

**多 panel**
- 用同一個 figure 畫所有 panel，不拼接 PNG。
- Panel 標籤 (a)、(b)、(c) 放在各 panel 左上角。
- 共用座標軸。每個格子都要有內容。
- 用 `layout="constrained"`。

**匯出**
- 向量 PDF，設定 `pdf.fonttype: 42`。
- 不用 `bbox_inches="tight"`，避免改變圖的尺寸。
- 熱圖格子很多時，只對該 artist 設 `rasterized=True`，文字仍是向量。
- 定性結果的圖片保留原始像素，不放大。

### 4.4 數據圖：圖型選擇
先寫出一句話訊息，再依訊息選圖型：

| 要呈現的內容 | 圖型 |
|---|---|
| 隨訓練步數或時間的趨勢 | line plot，加上誤差區帶 |
| 少數類別或 ablation 比較 | grouped bar，標上數值；或 dot plot |
| 多個方法、單一指標 | horizontal bar 或 dot plot，依數值排序 |
| 分布 | violin 或 box，加上個別資料點 |
| 兩個連續變數的關係 | scatter |
| 矩陣，例如 confusion matrix | heatmap，標上數值與 colorbar |
| 組成比例 | stacked bar |
| 多組小比較 | small multiples，共用座標軸 |

原圖型已經合適時，只改樣式，不換圖型。

### 4.5 方法圖（TikZ）
不用 AI 生成圖片。AI 圖片是點陣圖，標籤常拼錯，也無法沿用論文的 macro。

**規劃**：畫之前在 `spec.md` 寫出設計稿：
- 實體：有哪些元件。標籤用字與內文術語完全相同（E1）。
- 關係：元件之間的資料流。
- 版面：pipeline 由左到右，分層架構由上到下，中心架構用輻射狀。
- 分組：頂層元件超過 8 個時分組。

**樣式**（定義在 `paper_tikz.tex` 的 `\tikzset`）：
- 色彩：3–5 個顏色。分組用低飽和的淺色底框。醒目色只用在本論文提出的元件或最終輸出，與數據圖的本方法顏色相同。
- 箭頭：深灰 `#333333`，0.8–1.2 pt，實心箭頭。
- 線型：實線代表資料流，虛線代表輔助流程或梯度。在 caption 說明。
- 箭頭不交叉。跨越 3 列以上的長斜線，改排版面。
- 箭頭傳遞的內容不明顯時，在箭頭旁標上符號。
- 同一種角色的元件用相同大小。
- 圓角半徑小（約 2 pt）。
- 不巢狀分組。不用陰影、漸層、3D、裝飾性 icon。
- 文字多的地方改用編號，在 caption 說明。

**輸出**：用 `standalone` 類別單獨編譯成 PDF，再用 `\includegraphics` 放入論文。

**Figure 1**：
- 最大、最醒目的元素是主要結論或核心概念。
- 流向為「輸入 → 方法 → 結果」。
- 縮小到 25% 時，仍要看得出主要訊息。
- 讀者只看這張圖與 caption，要能說出問題、方法與貢獻。

### 4.6 Caption
- 第一句寫結論。
- 接著依序寫：畫的是什麼量、每個 panel 的內容、顏色與線型的意義、誤差的種類與 seed 數、實驗設定。
- 定義圖中所有縮寫與符號。
- Caption 的結論必須對每個 panel 都成立。
- Caption 的結論不超過內文的 claim。

### 4.7 表格
- 用 booktabs（`\toprule`、`\midrule`、`\bottomrule`）。不用直線，不用 `\hline`。
- 數字靠右對齊或依小數點對齊。
- 只改排版。數字、小數位數與粗體標示的最佳值都不變。
- 表格超出版面時，先調整欄位或改成橫式，最後才用 `\resizebox`。

### 4.8 目視檢查
每張新圖都要做：
1. 編譯論文，把該頁轉成圖片（`page.get_pixmap(dpi=200)`），用實際大小看。
2. 檢查：文字重疊、被裁切、圖例遮住資料、空白 panel、資料點糊成一團、字太小。
3. 轉成灰階看一次，再用色盲模擬（deuteranopia）看一次。比較仍要看得出來。
4. 與舊圖並排比較。新圖沒有更好時，保留舊圖。
5. 比對新圖畫出的數值與原始數據。
6. 依 presentation-check 的「零先備知識檢查」：只看圖與 caption，圖中每個元素都要能理解。

有問題就修改後重新檢查。

## 5. 交付前檢查
執行本資料夾的 `check_polish.py`（需要 `pip install pymupdf`）：

```
python check_polish.py --frozen frozen.json --tex <修改後的所有 .tex> --pdf <修改後>.pdf \
  --log <修改後>.log --changelog paper-polish_<zh 或 en>.md --figures figures/ --venue-pages <頁數上限>
```

- `--tex` 可以給多個檔案，包含 `\input` 的子檔。
- 修改紀錄中每一列 C 編號的最後一欄寫「是」（已同意並執行）或「使用者未同意」。

檢查項目：
- `frozen.json` 中的每個數字、表格儲存格與公式，都在修改後的檔案中原樣出現。
- 每處修改都有寫進修改紀錄，並標記使用者已同意。
- 正文頁數不超過會議上限。
- PDF 中沒有 Type 3 字型，所有字型都已嵌入。
- `figures/` 中的數據圖與方法圖都是向量 PDF。
- 論文可以編譯，沒有未定義的參照。
- 每張圖都在內文中被引用，編號連續。

輸出「全部通過」才可以交付。無法修正的項目，寫進修改紀錄的「範圍與限制」。

## 輸出
放在工作資料夾 `<論文簡稱>_review/polish/`：
- 修改後的 LaTeX 原始檔。不覆蓋原檔。
- `figures/`：每張圖一個畫圖程式、`paper_style.mplstyle`、`paper_tikz.tex`、`spec.md`、輸出的 PDF。
- `frozen.json`。
- 修改紀錄 `paper-polish_<zh 或 en>.md`，依共用規範的「每份報告的固定結構」：
  1. 結論：3–5 句，說明最大的改變。
  2. 文字修改表：編號、位置、原文、改後、依據規則、對應的 P9-x、使用者是否同意。
  3. 弱點處理表：編號、弱點、位置、處理方式、改前、改後、使用者是否同意。
  4. 圖的修改表：圖號、處理方式、一句話訊息、改了什麼、目視檢查結果、使用者是否同意。
  5. 未處理：A 類問題、Fatal 弱點，以及缺少數據而無法重畫的圖。
  6. 範圍與限制。
- 改前與改後的對照 PDF `compare.pdf`：每頁左邊是舊版，右邊是新版。用 PyMuPDF 的 `page.show_pdf_page()` 把兩份 PDF 的同一頁放進一張兩倍寬的新頁面。

## 圖的規範來源
第 4 節「圖」綜合以下 30 個 skill。表中列出每個 skill 採用的內容。

| # | Skill | Repo | 採用的內容 |
|---|---|---|---|
| 1 | scientific-visualization | K-Dense-AI/scientific-agent-skills | 不改資料、長條圖從 0 開始、缺值不連線、固定尺寸不用 tight bbox、fonttype 42 |
| 2 | matplotlib | K-Dense-AI/scientific-agent-skills | constrained layout、sequential／diverging 色盤、比較的熱圖用相同 norm |
| 3 | seaborn | K-Dense-AI/scientific-agent-skills | 誤差要以獨立樣本計算、缺值會被自動連線的陷阱 |
| 4 | scientific-schematics | K-Dense-AI/scientific-agent-skills | 示意圖寫明元件、方向與標籤；AI 生成圖的拼字問題 |
| 5 | scientific-figures | rhowardstone/Claude-Code-Scientist | panel 標籤、全篇一致配色、存檔前檢查表 |
| 6 | paper-figures | evoscientist/evoskills | 先寫 figure spec 再畫、忠實優先於美觀、不加未要求的元素、畫完後稽核 |
| 7 | publication-chart-skill | Galaxy-Dawn/claude-scholar | 依溝通目標選圖或表、縮小後的可讀性、擠的 panel 要拆開 |
| 8 | plot | michaelrizvi/claude-config | 沿用既有畫圖程式的樣式、圖例用論文術語、誤差必標 |
| 9 | academic-plotting | Orchestra-Research/AI-Research-SKILLs | 圖型決策表、本方法用獨立顏色、方法圖先抽實體與關係、標籤逐字取自論文 |
| 10 | paper-figure | wanshuiyin/Auto-claude-code-research-in-sleep | 圖內不放標題、caption 對每個 panel 都成立、一圖一程式、不寫死數據 |
| 11 | paper-illustration | wanshuiyin/Auto-claude-code-research-in-sleep | 方法圖由左到右、分組底框、深色實心箭頭、箭頭不交叉、避免陰影與 3D |
| 12 | figure-spec | wanshuiyin/Auto-claude-code-research-in-sleep | 方法圖用確定性的向量輸出、不巢狀分組、不畫長斜線、同角色同字級 |
| 13 | scientific-visualization | aiming-lab/AutoResearchClaw | 一圖一訊息、直接標籤取代圖例、去上右框線、小樣本不用長條圖 |
| 14 | scientific-visualization | kjgarza/marketplace-claude | 單位寫在括號、不用 jet、diverging 色盤設中心值、灰階測試 |
| 15 | general-figure-guide | jaechang-hits/SciAgent-Skills | 每次產圖後目視檢查：重疊、裁切、空白、過度擁擠 |
| 16 | multipanel | jaechang-hits/SciAgent-Skills | 同一個 figure 畫所有 panel、不拼接 PNG、每格都要有內容、圖例屬於所在 panel |
| 17 | statistical-significance-annotation | jaechang-hits/SciAgent-Skills | 只標已做過檢定的比較、多重比較用校正後的 p 值 |
| 18 | nature-figure-guide | jaechang-hits/SciAgent-Skills | 字型嵌入（TrueType 42，不用 Type 3）、panel 標籤字級 |
| 19 | publication-figures-guide | wentorai/research-plugins | 線寬 0.5–1.5 pt、以實際大小檢查、全篇樣式一致 |
| 20 | tikz-diagrams-guide | wentorai/research-plugins | standalone 編譯 TikZ、常用 TikZ library |
| 21 | latex-drawing-guide | wentorai/research-plugins | `\tikzset` 全域樣式、相對定位、TikZ 沿用文件字型 |
| 22 | scientific-illustration-guide | wentorai/research-plugins | 不用紅綠區分、顏色搭配形狀、直接標籤 |
| 23 | graphical-abstract-guide | wentorai/research-plugins | Figure 1 的視覺層次、輸入→方法→結果、縮小檢查、3–5 色 |
| 24 | visual-audit | pedrohcgs/claude-code-my-workflow | 逐頁目視稽核、依嚴重度回報 |
| 25 | figures | scdenney/open-science-skills | 先寫一句比較再選圖型、圖例順序等於視覺順序、caption 自足 |
| 26 | figure-table-audit | scdenney/open-science-skills | 圖表盤點、內文引用與編號連續、caption 寫樣本與誤差 |
| 27 | tables-and-figures | regisely/superpapers | booktabs、不用直線、只用向量 PDF、表格不超出版面 |
| 28 | figure | brycewang-stanford/Auto-Empirical-Research-Skills（skills/67） | 資料線 ≥ 0.5 pt、座標軸 ≥ 0.75 pt、字型與內文一致、不用預設主題 |
| 29 | aer-tables-figures | brycewang-stanford/AER-skills | 一圖一主張、六條線改成多個 panel、表格只改排版 |
| 30 | econ-visualization | thalysandratos/claude-code-skills | 全篇座標尺度一致、記錄資料篩選 |

第 19–30 項取自 brycewang-stanford/Auto-Empirical-Research-Skills（原名 Awesome-Agent-Skills-for-Empirical-Research）收錄的版本，Repo 欄是原始出處。
