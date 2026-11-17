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
- 列出這一批打算做的修改：編號、位置、原文、改後，以及 plan.md 的為什麼改、怎麼改、預期結果。圖的修改附上改前與改後的圖片。
- 用 AskUserQuestion 詢問是否 OK，選項為「全部 OK」「只改部分（請列出編號）」「都不要改」。沒有 AskUserQuestion 時，用文字詢問。
- 只執行使用者同意的修改。被拒絕的修改寫進修改紀錄，標「使用者未同意」。
- 使用者提出修正時，依修正後的內容執行。
- 一批修改以一個步驟為單位：第 2 節文字、第 3 節弱點處理、第 4 節每張圖、第 4.9 節表格。單一步驟的修改超過 20 處時，分成多批詢問。
- 沒有得到回覆時，不修改。

### 無法詢問使用者時
在沒有 AskUserQuestion、也無法用文字等回覆的環境（例如 headless 執行、subagent）：
- 「開始前」的設定自己判斷，寫進 `issues.json` 的 `meta`，並標「未經使用者確認」：
  - 目標會議：從 `\documentclass`、`\usepackage{cvpr}` 這類樣式檔判斷。
  - 論文來源：自己的論文。
  - 報告語言：中文版。
- 不複述理解、不等確認。把理解寫進 `understanding.md`，最上方寫「未經使用者確認」。
- 所有修改都做在副本上（見「輸出」），不動原檔。修改紀錄最後一欄寫「待確認」，不寫「是」。
- 所有步驟照常執行，包括第 4 節的圖。不因為無法詢問而跳過任何步驟。

## 改前計畫與改後驗收
每處修改（文字的 C 編號、弱點處理、每張重畫或重排的圖）都走三步：先寫計畫，再修改，最後驗收。

1. 改之前：在 `polish/plan.md` 的表格寫一列。先寫計畫，才可以動檔案。
   | 編號 | 對象 | 為什麼改 | 怎麼改 | 預期結果 | 驗收方法 | 驗收結果 | 證據 |
   |---|---|---|---|---|---|---|---|
   - 編號：文字與弱點處理用修改紀錄的 C 編號，圖用 spec.md 的圖號（例如 `Fig. 3`）。
   - 為什麼改：具體的問題與依據，例如「句長 41 字，違反 E1」「圖例框蓋住資料」「claim 超出實驗範圍（只測室內）」。「讓它更好」不是理由。
   - 怎麼改：具體做法，例如「拆成兩句」「圖例改成直接標籤」「把 all scenes 改成 indoor scenes」。
   - 預期結果：改完後可以檢查的目標，例如「兩句都 ≤ 25 字，意思不變」「資料區不小於舊圖，讀者不用看圖例就能分出 Ours」「claim 與 Tab. 2 的範圍相同」。
   - 驗收方法：怎麼確認達到預期，例如「數字數」「visual_check.py 並排看」「check_polish.py」「對照 Tab. 2」。
   - 驗收結果、證據：先空著，改完再填。
2. 修改。
3. 改完後：依「驗收方法」逐列檢查結果是否符合「預期結果」，也確認原本的目標（為什麼改）真的解決了，而且沒有產生新問題（意思改變、資料遺失、版面變差）。
   - 驗收結果只寫「達成」或「已還原」。沒有達成時，修到達成；修不好就還原這處修改，寫「已還原」與原因。
   - 證據寫實際看到的結果：字數、檢查輸出、`figures/compare_<圖名>.png` 的路徑與看到的差異。沒有證據不能寫「達成」。
4. 詢問使用者時（見「修改前先確認」），列出的內容就是 plan.md 的「為什麼改、怎麼改、預期結果」，圖再附改前與改後的圖片。

`check_polish.py` 會檢查：修改紀錄的每個 C 編號、spec.md 中每張重畫或重排的圖，在 plan.md 都有一列，前五欄與證據不空，驗收結果是「達成」或「已還原」。

## 執行順序
1. 第 1 節：凍結清單。
2. 第 4 節：圖。先做圖，因為圖最花工夫，最容易被省略。
   - 範圍：先做正文（主檔 `\input` 的內容）的每張圖，這是必做。補充材料的圖等正文的圖都通過檢查後才做。
   - 開始前在 `polish/progress.md` 列出正文的每張圖，一張一列：圖號、原圖檔、狀態（未開始／重畫中／完成／保留）。
   - 一張一張做：做完一張，就對這張跑 4.10 的目視檢查，更新 progress.md，再換下一張。大的方法圖也要做。
   - 正文的圖超過 3 張，而且可以用 Agent tool 時：每張圖（或 2–3 張同類的小圖）派一個 subagent 做。派工內容：這份 SKILL.md 的路徑、第 4 節的相關小節、圖號、原圖檔、共用樣式檔 `paper_style.mplstyle`／`paper_tikz.tex`、輸出路徑。可以同時派多個。你自己負責：先建共用樣式檔，收回每張圖後跑 4.10 目視檢查與 `check_polish.py`，不合格就退回該 subagent 修。
   - 「看起來已經不錯」「工作量太大」都不是跳過的理由。舊圖已經很好時，仍要做出重畫版，依 4.10 比較後才可以保留。
3. 第 2、3 節：文字與弱點處理。
4. 第 5 節：交付前檢查，修到只剩頁數一項。
5. 這次執行做不完時：progress.md 寫明每張圖的狀態與下一步，回報的第一句寫「未完成」與剩下的項目。下次執行時先讀 progress.md，從未完成的圖接著做。

`check_polish.py` 會自己重跑抽取，驗證「抽取未通過」是否屬實，也會檢查每個保留原因的證據。不要為了通過檢查而寫不屬實的原因：被發現時，這張圖仍要重畫。

## 輸入
- LaTeX 原始檔（必要）。沒有原始檔時停下來，向使用者要。
- 編譯後的 PDF。
- 數據圖的數值來源，依優先順序：
  1. 原始數據或原本的畫圖程式。
  2. 圖檔是向量 PDF 時：依 4.3 從 PDF 的繪圖指令抽出數值。
  3. 兩者都沒有（數據圖只有點陣圖）：該圖只改 caption 與 LaTeX 排版，寫進「未處理」，向使用者要數據。
- 方法圖不需要數據：依舊圖的文字與版面用 TikZ 重畫（4.6）。

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
   - 只用原始數據、原畫圖程式，或從向量 PDF 抽出並通過驗證的數值重畫（4.3）。
   - 不從點陣圖讀數值。
   - 不刪資料點，也不調整座標軸範圍來放大差異。
   - 缺值留空，不連線。
2. 一張圖一個訊息：畫之前先寫一句話，說明讀者看完這張圖要看到什麼比較。
3. 全篇一致：所有圖共用同一份樣式、同一套顏色對應與字型。
4. 不加論文沒有的東西：
   - 只畫論文已經報告的統計量。
   - 原始數據有多個 seed、論文卻沒有畫誤差時，寫進「未處理」，不自行加上。
   - 顯著性標記只用在論文已經做過檢定的比較。

### 4.2 圖的盤點與規格
找出論文實際用到的每張圖：依 `\includegraphics` 與 `\input` 追到實際的檔案。資料夾中沒被用到的舊版圖檔不處理。
為每張圖（正文與 appendix）在 `figures/spec.md` 的表格寫一列，欄位依下列順序：

| 欄位 | 內容 |
|---|---|
| 圖號 | Fig. N |
| 原圖檔 | 論文原本 `\includegraphics` 的檔名；多個檔案時全部列出 |
| 新圖檔 | 重畫後的檔名（放在 `figures/`）；沒有重畫時寫「無」 |
| 類型 | 數據圖／方法圖／定性結果（圖片） |
| 一句話訊息 | 讀者看完要得到的結論 |
| 資料來源 | 數據檔、畫圖程式，或「向量 PDF 抽取」；沒有時寫「無」 |
| 資料組對應 | 數據圖：抽取報告中每組資料（例如 `p0_g3`）是哪個方法。圖例樣本、框線、註解引線等寫成「非資料：p0_g5、p0_g6」，checker 比對資料時會排除它們。重畫後每組資料都要出現在新圖 |
| 處理方式 | 重畫數據圖／重畫方法圖／重排定性結果／只改 caption／保留 |
| 原因 | 處理方式是「只改 caption」或「保留」時必填，寫法見下方 |
| 寬度 | `\columnwidth` 或 `\textwidth` |
| 顏色對應 | 每個方法或元件用的顏色 |

- 預設處理方式：
  - 數據圖：重畫數據圖。
  - 方法圖：重畫方法圖（4.6）。方法圖不需要數據，一定要先畫出 TikZ 版本。
  - 定性結果：重排定性結果（4.7）。
- 「只改 caption」或「保留」的原因欄，必須用下列其中一個開頭，並附上證據檔。`check_polish.py` 會檢查證據檔是否存在：

| 原因開頭 | 適用 | 證據檔 |
|---|---|---|
| `點陣圖：` | 原圖檔本身是一張 png／jpg：數據圖沒有原始數據；或定性結果已拼成一張圖，專案中找不到個別圖片 | 原圖檔是 png／jpg。原因欄寫出搜尋過的檔名模式與結果，例如「搜尋 `figs/*grid7*`：只有 `p2s_grid7_tiles.jpg`，已是拼好的檔」。原圖是 PDF 時不能用這個原因：PDF 內嵌的圖片都可以用 `extract_figure_assets.py` 取出 |
| `抽取未通過：` | 向量 PDF 抽取沒有通過 4.3 的驗證，寫出哪一項 | `figures/data/<原圖名>_report.json` |
| `重畫後較差：` | 已經做出完整的重畫版，依 4.10 第 4 點比較後新圖沒有更好，寫出比較結果 | `figures/compare_<原圖名>.png`，且「新圖檔」欄列出重畫版。重畫版必須完整：舊圖的每個文字標籤、每組資料、每種線型（例如虛線）都在。漏東西、文字重疊的重畫版是還沒做完，要先修好，不能拿來證明舊圖較好 |

- 「這張圖已經夠好」「時間不夠」「範圍沒做到」都不是原因。
- 同一個方法在每張圖都用同一個顏色。顏色對應只寫一次，所有圖共用。

### 4.3 從向量 PDF 抽數據
matplotlib、pgfplots 等工具輸出的 PDF 存著每條線、每個點、每根長條的精確座標。從這些座標換算出的數值與原始數據相同，只差浮點誤差。這不是讀像素。

**步驟**：
1. 對每張向量 PDF 數據圖執行本資料夾的工具：
   ```
   python extract_vector_plot.py <原圖.pdf> --out figures/data/
   ```
   輸出 `<圖名>.csv`（每組資料換算後的數值）、`<圖名>_report.json`（座標軸對應與刻度檢查）、`<圖名>_overlay.png`（抽到的點用洋紅色疊在舊圖上）。
2. 工具支援線性、log、等距的順序軸（例如 0、0.02、0.05 等距排列），以及只有一軸有數字刻度的圖（另一軸是方法或序列名稱，輸出 PDF 座標，依位置對應標籤文字）。上方或右側的第二軸列在 report 的 `secondary_axes`，重畫時保留。
   工具判定刻度檢查未通過時（exit code 1），看 report 中哪個 panel 的哪個軸未通過，再自己寫換算：
   - 常見原因：非標準座標（例如 log(x−1)、symlog）、刻度標籤不是數字。
   - 用 csv 中的 PDF 座標與刻度標籤，寫出該軸的換算，再做 4 項驗證。
   - 工具未通過不是保留的原因。只有自己的換算也沒通過驗證時，原因欄才寫「抽取未通過：」，並寫出試過的換算。
3. 工具找不到座標軸時（exit code 2），先看舊圖判斷類型：
   - 方法圖：依 4.6 重畫。
   - 沒有數字刻度的向量數據圖（例如 top-view 軌跡、只有比例尺的圖、示意曲線）：重播繪圖指令。用 `page.get_drawings()` 取出每條路徑的座標，原樣保留相對位置與比例，只換線寬、顏色、字型與標籤。座標沒有換算成數值，所以不需要刻度檢查；改做疊圖檢查與數量檢查（每條路徑的點數與舊圖相同）。
4. 依圖例的文字與顏色，把 report 中的每組資料對應到方法名稱，寫進 spec.md 的「資料組對應」欄。圖例樣本、框線、註解箭頭標成非資料。
5. 原圖有工具處理不了的部分（例如點陣的熱圖 panel），該 panel 保留原圖的點陣內容，其餘 panel 重畫。

**驗證**（每張圖都做，任一項不通過就不重畫，原因欄寫「抽取未通過：」與未通過的項目）：
1. 刻度檢查：工具已做。刻度換算誤差不超過該軸範圍的 0.5%。
2. 疊圖檢查：用 Read 打開 `_overlay.png`，洋紅點要落在舊圖的每個資料點與折線轉折處上。
3. 交叉核對：圖中的數值同時出現在表格或內文時，抽出的值四捨五入後要相同。
4. 數量檢查：每組資料的點數與舊圖相同。新圖畫出每一組資料，包括淡色的個別曲線、參考線與次要的 baseline。

### 4.4 全篇樣式
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

### 4.5 數據圖：圖型選擇
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

### 4.6 方法圖（TikZ）
不用 AI 生成圖片。AI 圖片是點陣圖，標籤常拼錯，也無法沿用論文的 macro。

**來源**：執行本資料夾的工具，取出舊圖的內嵌圖片、文字標籤與位置：
```
python extract_figure_assets.py <舊圖.pdf> --out figures/assets/
```
- `layout.json` 列出每張圖片的位置（pt）與每個文字標籤；`preview.png` 標出圖片編號。
- 新圖保留舊圖的每個元件、每條資料流與每張圖片，只改樣式與排列。
- 文字與數學式用 LaTeX 重新打字：數學式寫成 `$...$`，用論文的 macro，與內文寫法相同。不要直接複製 `layout.json` 的字串：數學字型抽出的字元常是亂碼（例如 τ 變成「¿」、Σ 變成「¼¾」）。`layout.json` 只用來確認位置與字級。
- 照片、渲染結果等點陣部分：用 `\includegraphics` 放進 TikZ 節點，不重畫。
- 論文用 LaTeX 疊在圖上的標籤（例如 `picture` 環境中的 `\put`），尤其含 `\cite`、`\ref` 時，保留在 LaTeX 中，不移進圖內，這樣引用仍可點擊。只統一字型與顏色。
- 舊圖中的小型曲線圖（例如示意的資料曲線）：先用 `extract_vector_plot.py` 抽數值，用 pgfplots 或 matplotlib 重畫；抽不出時，把舊圖裁切該區域（`\includegraphics[trim=..., clip]`）放進節點，其餘部分仍用 TikZ 重畫。不因為圖中有一部分無法重畫，就保留整張舊圖。

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

### 4.7 定性結果
- 保留原始像素。不放大、不重新壓縮、不調色。
- 統一版面：多張圖片用同一個 figure 排成格子，欄與列對齊，間距相同。
- 欄標題（方法名稱）與列標題用論文的術語與字型，字級依 4.4。
- 本方法的欄標題用 4.4 的本方法顏色，或放在固定的位置（例如最右欄）。
- 放大區域（zoom-in）的框線顏色與粗細全篇一致。
- 原圖是 PDF（向量外框加內嵌照片、渲染圖或熱圖）時：
  1. 執行 `python extract_figure_assets.py <舊圖.pdf> --out figures/assets/`，取出每張內嵌圖片的原始位元組，以及它們的位置與文字標籤。
  2. 打開 `preview.png`，對照 `layout.json` 確認格子的列與欄。
  3. 用 TikZ 重排：每張圖片放一個節點，`\includegraphics[width=<原寬度>pt]{assets/.../imgN.jpg}`。欄標題、列標題、色條刻度與註解用論文字型重寫。
  4. 色條（colorbar）是點陣圖時一併取出放回；是向量時用 pgfplots 的 colorbar 重畫，刻度數值與舊圖相同。
  5. 圖片上的疊加標註（數字、圓圈、箭頭）是向量時，依 `layout.json` 的位置用 TikZ 重畫；是燒在圖片裡的像素時保留。
- 原圖本身是一張 png／jpg、已拼好時：先在專案中搜尋個別圖片，用原圖檔名的前綴、場景名稱與方法名稱搜尋。找到就重排；找不到時保留，原因欄寫「點陣圖：」並列出搜尋過的模式與結果。

### 4.8 Caption
- 第一句寫結論。
- 接著依序寫：畫的是什麼量、每個 panel 的內容、顏色與線型的意義、誤差的種類與 seed 數、實驗設定。
- 定義圖中所有縮寫與符號。
- Caption 的結論必須對每個 panel 都成立。
- Caption 的結論不超過內文的 claim。

### 4.9 表格
- 用 booktabs（`\toprule`、`\midrule`、`\bottomrule`）。不用直線，不用 `\hline`。
- 數字靠右對齊或依小數點對齊。
- 只改排版。數字、小數位數與粗體標示的最佳值都不變。
- 表格超出版面時，先調整欄位或改成橫式，最後才用 `\resizebox`。

### 4.10 目視檢查
每張新圖都要做：
1. 執行本資料夾的工具，產生實際大小、灰階與 deuteranopia 模擬的並排圖（第二列是舊圖）：
   ```
   python visual_check.py figures/<新圖>.pdf <舊圖> --out figures/visual/
   ```
   用 Read 打開輸出的 png 實際看。不能只用文字推論代替。
2. 檢查：文字重疊、被裁切、圖例遮住資料、空白 panel、資料點糊成一團、字太小。
3. 灰階與色盲模擬中，各方法仍要分得出來。
4. 與舊圖比較：舊圖的每個元件、每組資料都在新圖中。新圖的資料區（座標軸圍出的區域）不小於舊圖；加圖例、標題或 panel 標籤不能壓縮資料區，空間不夠時改用直接標籤。`check_polish.py` 會比對新舊圖的軸長，小於 85% 時報錯。舊圖用縮排、分組標題、位置或線型表示的層級與分組（例如子項目縮排在母項目下方），新圖要保留；分組標題不放進資料區。新圖沒有更好時，保留舊圖，原因欄寫「重畫後較差：」，並把並排圖存成 `figures/compare_<原圖名>.png`。
5. 比對新圖畫出的數值與原始數據，或與 4.3 抽出的數據。
6. 依 presentation-check 的「零先備知識檢查」：只看圖與 caption，圖中每個元素都要能理解。

有問題就修改後重新檢查。

## 5. 交付前檢查
執行本資料夾的 `check_polish.py`（需要 `pip install pymupdf`）：

```
python check_polish.py --frozen frozen.json --tex <修改後的所有 .tex> --pdf <修改後>.pdf \
  --log <修改後>.log --changelog paper-polish_<zh 或 en>.md --figures figures/ --venue-pages <頁數上限> \n  --orig-tex <原始的所有 .tex> [--body-end "LLM Usage Statement"]
```

- `--tex` 可以給多個檔案，包含 `\input` 的子檔。
- 修改紀錄中每一列 C 編號的最後一欄寫「是」（已同意並執行）、「使用者未同意」，或「待確認」（無法詢問使用者時）。
- `--orig-tex` 給原始的主檔（正文）時，會另外檢查正文用到的圖。補充材料另外跑一次，`--orig-tex` 給補充材料的 .tex。檢查內容：論文用到的每張圖，若仍指向原本的圖檔，`spec.md` 必須有該圖的列，且原因欄不空白。

檢查項目：
- `frozen.json` 中的每個數字、表格儲存格與公式，都在修改後的檔案中原樣出現。
- 每處修改都有寫進修改紀錄，並標記使用者已同意。
- 正文頁數不超過會議上限。
- PDF 中沒有 Type 3 字型，所有字型都已嵌入。
- `figures/` 中的數據圖與方法圖都是向量 PDF。
- `figures/spec.md` 存在；「只改 caption」或「保留」的原因欄以規定的開頭起頭，並有對應的證據檔（4.2）。
- 論文中沒有重畫的圖都在 `spec.md` 寫了原因。
- 重畫的數據圖：對新、舊圖都執行抽取，新圖的資料組數與資料點數不少於舊圖。
- 論文可以編譯，沒有未定義的參照。
- 每張圖都在內文中被引用，編號連續。

輸出「全部通過」才可以交付。
- 與圖、修改紀錄、參照、字型有關的錯誤，一律可以修正：重畫，或依 4.2 的規定寫原因並附證據檔。修正後重跑，直到這些錯誤歸零。不能以「時間不夠」「這次沒做完」結束。
- 只有頁數超過上限可以留下：polish 不刪內容，要刪什麼由使用者決定。寫進修改紀錄的「未處理」。
- `--body-end`：會議規定某個段落（例如 LLM Usage Statement）不計入頁數時，給該段標題，正文頁數算到它為止。依據寫進修改紀錄。不確定時不給。

## 輸出
放在工作資料夾 `<論文簡稱>_review/polish/`：
- 修改後的 LaTeX 原始檔。不覆蓋原檔。
- `plan.md`：每處修改的計畫與驗收結果（見「改前計畫與改後驗收」）。
- `figures/`：每張圖一個畫圖程式、`paper_style.mplstyle`、`paper_tikz.tex`、`spec.md`、輸出的 PDF。
- `frozen.json`。
- 修改紀錄 `paper-polish_<zh 或 en>.md`，依共用規範的「每份報告的固定結構」：
  1. 結論：3–5 句，說明最大的改變。另寫驗收統計：計畫幾處、達成幾處、還原幾處。
  2. 文字修改表：編號、位置、原文、改後、依據規則、對應的 P9-x、使用者是否同意。
  3. 弱點處理表：編號、弱點、位置、處理方式、改前、改後、使用者是否同意。
  4. 圖的修改表：圖號、處理方式、資料來源、一句話訊息、改了什麼、目視檢查結果、使用者是否同意。每張重畫的圖附一張改前與改後並排的圖片 `figures/compare_<圖名>.png`。
  5. 未處理：A 類問題、Fatal 弱點，以及無法重畫的圖與原因。
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
