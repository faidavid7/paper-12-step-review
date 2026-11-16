---
name: paper-experiment-check
description: 檢查 ML 論文的實驗：主實驗是否逐一證明不足 D1…Dn 已被解決、ablation 是否涵蓋每個設計決策、結果是否符合方法推出的預期、提升是否顯著（variance、seed、統計檢定）、baseline 是否公平、有無 confounding factor 與資料洩漏、表格與內文數字是否一致、能否重現。對應原 12 步審查的第 5 步。使用者要求「檢查實驗」「實驗夠不夠」「ablation 完不完整」「結果顯不顯著」「check the experiments」時使用。
---

# 實驗檢查

先讀 `../paper-review-shared/conventions.md`，執行其中的「開始前」。問題編號用 P5-x。

## 缺少上游產出時
- 需要 `issues.json` 的 `handoff.deficits`、`handoff.design_decisions`、`handoff.expected_results`。
- 缺 deficits：從論文自述整理 D1…Dn（同 paper-method-check 的作法）。
- 缺 design_decisions：依方法章節列出 M1…Mn，每項一句。
- 缺 expected_results：依論文自己宣稱的效果寫出 X1…Xn。
- 在「範圍與限制」標出哪些清單是自行整理的，以及可能的影響。

## 檢查

### 1. 不足 → 實驗
- 每個 D：哪個實驗（Table／Fig.）證明它已被解決？結果是什麼？是否真的解決？
- 沒有對應實驗的 D，而論文宣稱已解決時，列為 Fatal。

### 2. 設計決策 → ablation
- 每個 M：有沒有 ablation？拿掉或替換後掉多少？
- 沒有 ablation 的 M 列為 Major。效果小於 variance 的 M，表示該設計可能不必要。

### 3. 預期 → 實際
- 每個 X：實驗結果是否符合？
- 不符合時分析原因：方法機制有誤、實驗設定不同，還是 variance。
- 論文沒有做能檢驗 X 的實驗時，寫出應該補的實驗。

### 4. 顯著性
- 記錄主結果的數值、variance（std 或 CI）、seed 數，以及是否做統計檢定。
- 提升小於 variance，或只有單一 seed 時，列為 Major 以上。
- 多個 dataset 或 metric 同時比較時，檢查是否處理多重比較。
- 提升不顯著時分析原因。這是常見的 reject 理由。

### 5. 公平性與 confounding
- Baseline 是否用相同資料、相同調參預算、相同計算量、相同 backbone？
- Baseline 數字是自己重跑，還是抄原論文？抄的時候 setting 是否一致？
- 有沒有 confounding factor，例如更多參數、更多訓練步數、額外資料、不同的前處理？
- 有沒有資料洩漏，例如在 test set 上選超參數？
- paper-survey-and-naive-ideas 列出的缺少 baseline 與 dataset：缺少的影響有多大？

### 6. 一致性與重現性
- 表格數字與內文、abstract 中的數字是否一致？逐一核對。
- 最佳結果的粗體標示是否正確？
- 超參數、計算資源、訓練時間、程式碼是否公開？缺少哪些就無法重現？

## 輸出
- 報告 `paper-experiment-check_<zh 或 en>.md`，依共用規範的「每份報告的固定結構」撰寫：
  1. 結論：實驗是否支持主 claim。
  2. 對照表（不足 D、對應實驗、結果、是否解決）。
  3. Ablation 表（M、對應 ablation、效果、是否足夠）。
  4. 預期對照表（X、實際結果、是否一致、原因）。
  5. 顯著性表（實驗、數值、variance、seed 數、統計檢定、結論）。
  6. 公平性、confounding、一致性與重現性檢查。
  7. 問題表（P5-x）。
  8. 交接：已證明與未證明的 claim 清單（給 paper-novelty-positioning 與 paper-limitations）。
  9. 範圍與限制。
- 把 P5-x 寫入 `issues.json`。
