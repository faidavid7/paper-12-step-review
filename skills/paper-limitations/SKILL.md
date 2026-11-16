---
name: paper-limitations
description: 在 motivation、survey、方法、實驗、novelty 等檢查做完後，彙整 ML 論文還剩哪些問題，逐一決定「修掉、縮小 claim、或寫成限制」，檢查 overclaim，並教怎麼寫 Limitations 段落（具體、有範圍、有證據、附因應或 future work、不自毀主 claim），最後產出可直接貼進論文的 Limitations 草稿。對應原 12 步審查的第 7 步。使用者要求「還有什麼問題」「limitation 怎麼寫」「幫我寫限制」「有沒有 overclaim」「write the limitations section」時使用。
---

# 剩餘問題與限制寫法

先讀 `../paper-review-shared/conventions.md`，執行其中的「開始前」。問題編號用 P7-x。
Limitations 草稿依 `../paper-review-shared/writing-rules.md` 撰寫。

## 輸入
- `issues.json` 中所有已存在的問題。
- 工作資料夾中已存在的報告：motivation、survey、method、experiment、novelty-positioning。

## 缺少上游產出時
- 任何一部分存在就可以執行。
- 在報告開頭列出覆蓋表：每個上游 skill 是否已執行。
- 未執行的部分，自行快速檢查：只看 claim 有沒有實驗支持、論文有沒有寫 limitation。在「範圍與限制」說明未覆蓋的面向。
- 只有不到兩份上游報告時，在結論提醒：限制清單可能不完整，建議先跑 paper-method-check 與 paper-experiment-check。

## 檢查

### 1. 彙整剩餘問題
- 收集所有 Fatal 與 Major 問題，加上本 skill 新找到的問題。
- 合併重複的問題，保留原編號，例如「P4-2／P5-3」。

### 2. Overclaim
- 逐條檢查 abstract、introduction、conclusion 的 claim。
- 每條 claim 找出支持它的實驗，判斷 claim 的範圍是否超出實驗範圍。
- 常見的 overclaim：只在一種資料上驗證卻寫「general」；只比較部分 baseline 卻寫「state-of-the-art」；沒有理論卻寫「guarantee」；相關性寫成因果。
- 看不出限制時，檢查 task 是否太少或分析不足。這本身就是限制。

### 3. 分流：每個剩餘問題怎麼處理
每個問題決定一個處理方式，並說明理由：

| 處理方式 | 適用條件 |
|---|---|
| 修掉 | 問題影響主 claim，而且在截止前可以修（補實驗、改方法、改證明）。交給 paper-revision。 |
| 縮小 claim | 實驗只支持較小的 claim。改寫 claim，使它與證據相符。 |
| 寫成限制 | 問題不影響主 claim，或修正超出本論文範圍。寫進 Limitations。 |
| 不需處理 | 確認後不是問題。說明理由。 |

- Fatal 問題不得只寫成限制。Limitations 段落不能用來掩蓋主 claim 沒有證據的問題。

### 4. Limitations 怎麼寫
每條限制包含 4 個部分：
1. 範圍：在哪個條件下，方法的什麼性質不成立或未被驗證。要具體到資料、規模、假設或 setting。
2. 證據：為何知道這是限制（實驗結果、理論假設、未測試的情境）。
3. 影響：限制對結果與應用的影響有多大。
4. 因應：可行的緩解方式或 future work 方向。

寫法規則：
- 寫具體的條件，不寫空泛的句子，例如不寫「our method has some limitations」。
- 限制的範圍不要寫得比實際大，避免自毀主 claim。
- 每條限制都要與論文中某個 claim 或實驗對應。
- 依目標會議的規定擺放：例如 NeurIPS 要求 Limitations 段落與 checklist。不確定時用 WebSearch 查詢。
- 自己的論文：英文依 E1–E21，中文依規範 1–4。

### 5. Future work
- 從「寫成限制」的問題推出 2–4 個 future work 方向。每個方向寫出它解決哪條限制。

## 輸出
- 報告 `paper-limitations_<zh 或 en>.md`，依共用規範的「每份報告的固定結構」撰寫：
  1. 結論：還剩幾個 Fatal／Major、多少要修、多少寫成限制。
  2. 上游覆蓋表。
  3. Overclaim 表（claim、位置、支持的實驗、落差、建議改寫）。
  4. 分流表（問題編號、問題、處理方式、理由）。
  5. Limitations 草稿：用論文的語言撰寫，可以直接貼進論文。每條限制後面用括號標出對應的問題編號，貼進論文前刪除。
  6. Future work。
  7. 問題表（P7-x）。
  8. 交接：「修掉」與「縮小 claim」的清單給 paper-revision。
  9. 範圍與限制。
- 把 P7-x 寫入 `issues.json`。
