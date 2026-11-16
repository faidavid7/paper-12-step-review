---
name: paper-survey-and-naive-ideas
description: 為 ML 論文做 paper survey 與直覺解法（naive thoughts）檢查：先列 2–3 個直覺解法並說明為何不夠好，再整理研究線脈絡、依方法分組既有工作、用 paper-search 沿引用關係找遺漏的近期工作，列出缺少的 baseline 與 dataset，並產出不足清單 D1…Dn 給方法與實驗檢查使用。對應原 12 步審查的第 2、3 步。使用者要求「paper survey」「related work 有沒有漏」「直覺解法」「simple baseline 為什麼不行」「find missing related work」時使用。
---

# Paper survey 與直覺解法

先讀 `../paper-review-shared/conventions.md`，執行其中的「開始前」。問題編號用 P2-x（直覺解法）與 P3-x（survey）。
有 `paper-motivation-check` 的問題卡時，以它的 problem setting 為準。

## 檢查

### 1. 直覺解法（先做，不看論文的方法）
- 只根據問題卡，列出 2–3 個直覺解法。至少一個是最簡單的 baseline，例如更大的模型、更多資料、既有方法直接套用、簡單的 heuristic。
- 說明每個解法為何失敗或不夠好。理由要具體，例如計算量、假設不成立、已知的失敗案例。
- 檢查論文是否說明為何不用這些解法。
- 論文沒有回應、而且該解法可能有效時，列為 Major：reviewer 會要求比較。
- 每個直覺解法對應到哪條既有研究線？在第 2 項的分組表中標出。

### 2. 研究線脈絡與分組
- 領域脈絡：用 3–5 句寫出這條研究線如何演變到今天。
- 依方法類別把既有工作分組。每組列出代表方法與主要不足。
- 不足要具體到可以用實驗檢驗，例如「長序列時記憶體為 O(n²)」，不寫「效果不好」。

### 3. 找遺漏的工作
- 用 paper-search 搜尋近 2 年的工作，檢查論文是否漏掉重要的工作。
- 沿引用關係擴充：
  - 往後找：論文引用的關鍵工作被誰引用（cited by），找出後續與同期的工作。
  - 往前找：這些關鍵工作引用了誰（references），找出共同的源頭工作。
  - 被多篇關鍵工作共同引用，或共同引用多篇關鍵工作的論文，優先檢查。
- 每篇候選遺漏工作都要確認：論文存在、作者與年份正確、確實與本論文相關。無法確認的不列。
- 列出應該比較、但論文沒有比較的 baseline 與 dataset，並說明理由。

### 4. 關係圖
用 mermaid 畫出既有工作之間的關係：
- 節點：論文（作者＋年份），依方法類別分組（subgraph）。
- 邊：延伸、改進、比較、合併等關係，邊上標註關係類型。
- 本論文另外標示，並連到它直接延伸或比較的工作。
- 遺漏的重要工作用虛線框標示。

### 5. 不足清單（交接用）
- 彙整第 1–3 項找到的不足，編號 D1、D2⋯。
- 每項寫：不足的內容、來源（哪組方法或哪個直覺解法）、論文是否宣稱要解決它。
- 寫入 `issues.json` 的 `handoff.deficits`。paper-method-check 與 paper-experiment-check 會逐項對照。

## 輸出
- 報告 `paper-survey-and-naive-ideas_<zh 或 en>.md`，依共用規範的「每份報告的固定結構」撰寫：
  1. 結論：survey 是否完整、直覺解法是否被排除。
  2. 直覺解法表（直覺解法、問題、論文是否回應、對應研究線）。
  3. 領域脈絡、mermaid 關係圖、分組表（類別、代表方法、不足、論文是否比較）。
  4. 遺漏工作表（論文、年份、關係、為何應納入、如何找到）。
  5. 缺少的 baseline 與 dataset 清單。
  6. 問題表（P2-x、P3-x）。
  7. 交接：不足清單 D1…Dn；最接近的 2–3 篇工作（給 paper-novelty-positioning）。
  8. 範圍與限制：例如無法上網時未做引用擴充。
- 把 P2-x、P3-x 與 `handoff.deficits` 寫入 `issues.json`。
