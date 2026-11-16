---
name: paper-motivation-check
description: 檢查 ML 論文的 motivation 與 problem setting：問題重不重要、誰受益、motivation 鏈是否完整、problem setting 是否有正式定義（input／output、假設、評估指標）、setting 是否貼近真實情境、評估是否對應 motivation。對應原 12 步審查的第 1 步。使用者要求「檢查 motivation」「problem setting 清不清楚」「這個問題值不值得做」「check the motivation / problem formulation」時使用。
---

# Motivation 與 problem setting 檢查

先讀 `../paper-review-shared/conventions.md`，執行其中的「開始前」。問題編號用 P1-x。

## 檢查

### 1. Motivation 鏈
把論文的 motivation 拆成 4 環，逐環找出論文中的依據位置：

| 環 | 要回答的問題 |
|---|---|
| 現象 | 哪個實際問題或觀察觸發這項研究？ |
| 重要性 | 誰受益？受益多少？論文有沒有給證據（數據、引用、案例）？ |
| 缺口 | 既有方法在哪裡失敗？失敗是否有證據，還是只是宣稱？ |
| 主張 | 論文要填補哪個缺口？主張與缺口是否一一對應？ |

- 任一環缺少依據時，列為問題。
- 缺口只靠宣稱、沒有證據（例如沒有實驗、沒有引用）時，至少列為 Major。
- 檢查 abstract、introduction 與 conclusion 的 motivation 是否一致。

### 2. Problem setting
- Input：資料型態、維度、取得方式。
- Output：預測目標、型態、維度。
- 假設：資料分布、可用資訊、計算限制。逐條判斷每個假設在實際應用中是否成立。
- 評估指標：用哪些 metric？metric 是否量到 motivation 中宣稱的好處？
- 正式定義：有沒有數學 formulation（目標函數、符號）？符號是否在使用前定義？
- 與既有 setting 的差異：本論文的 setting 是新的、修改過的，還是標準 setting？修改時是否說明原因？

### 3. Setting 是否貼近真實
- Benchmark 或模擬環境是否代表 motivation 中的應用？
- 有沒有為了讓方法好做而簡化 setting？簡化是否在論文中說明？
- 切入方向與應用：列出這個問題可延伸的方向與應用，判斷論文選的切入點是否合理。

### 4. 問題卡
用一張表總結：

| 欄位 | 內容 |
|---|---|
| 一句話問題 | 不超過 30 字 |
| 受益者 | ... |
| Input | ... |
| Output | ... |
| 關鍵假設 | ... |
| 評估指標 | ... |
| 缺口的證據 | 位置，或「論文未提及」 |

## 輸出
- 報告 `paper-motivation-check_<zh 或 en>.md`，依共用規範的「每份報告的固定結構」撰寫：
  1. 結論：問題值不值得做、setting 清不清楚。
  2. Motivation 鏈表（環、論文的說法、位置、是否有證據、問題）。
  3. Problem setting 檢查與問題卡。
  4. 問題表（P1-x）。
  5. 交接：問題卡給 paper-survey-and-naive-ideas 與 paper-novelty-positioning 使用。
  6. 範圍與限制。
- 把 P1-x 寫入 `issues.json`。
