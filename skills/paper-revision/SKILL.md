---
name: paper-revision
description: 改 ML 論文：彙整 paper-* 系列各 skill 找到的所有問題，依「問題定義→方法→實驗→寫作→格式」排序出修改計畫（自己的論文分 A 類本質／B 類呈現，每個 Fatal／Major 至少 3 個有實質差異的方案，附成本、預期結果、退路），做投稿合規檢查（匿名、PDF metadata、LaTeX、supplementary、頁數與模板），最後合併成一份 md 總報告與分色註解的 PDF，並跑交付前檢查。對應原 12 步審查的第 11、12 步。使用者要求「改論文」「修改計畫」「revision plan」「投稿前檢查」「匿名檢查」「幫我把審查結果整理成要怎麼改」時使用。
---

# 改論文：修改計畫與合規

先讀 `../paper-review-shared/conventions.md`，執行其中的「開始前」。問題編號用 P11-x（修改計畫）與 P12-x（合規）。
改寫範例依 `../paper-review-shared/writing-rules.md`。PDF 註解依本資料夾的 `pdf-annotation.md`。

## 輸入
- `issues.json` 中所有問題。
- 工作資料夾中所有報告。paper-limitations 報告的「修掉」與「縮小 claim」清單優先處理。

## 缺少上游產出時
- 在報告開頭列出覆蓋表：9 個 skill 各自是否已執行。
- 只有少數 skill 執行過時，修改計畫只涵蓋已找到的問題，並在結論寫出未覆蓋的面向與建議補跑的 skill。
- 不自行補做上游 skill 的完整檢查。
- 例外：`issues.json` 沒有 `figures` 時，先執行 paper-presentation-check。`check_review.py` 要求每張圖都有圖的註解。

## 1. 修改計畫
- 彙整所有問題編號。合併重複的問題，保留所有原編號。
- 依「問題定義 → 方法 → 實驗 → 寫作 → 格式」排序。上層錯誤會使下層修改失去意義。
- 有依附關係的問題（例如方法改了，相關實驗要重跑）標成「依附於 Px-y」。

### 自己的論文
先 A 類，再 B 類。
- **A 類：本質問題**（claim、實驗、paper survey、方法、理論）
  - 每個 Fatal 和 Major 問題至少提出 3 個方案。
  - 每個方案包含：具體改法、所需成本（時間與計算資源）、預期結果、結果不如預期時的退路。
  - 方案之間要有實質差異。例如一個縮小 claim，一個補實驗，一個修改方法。
  - 標出建議的方案與理由。
- **B 類：呈現問題**（行文、連貫性、AI 痕跡、術語、圖表）
  - 每個問題列出改法與改寫範例。
  - 圖的問題附上 paper-presentation-check 的重新設計建議。
- 時程：依截止日期排出順序。先做成本低、影響大的修改。

### 別人的論文
- 不分類。依上述排序列出「若我是作者會怎麼改」。
- 每個 Fatal 和 Major 問題至少 3 個方案。

### Minor 問題
- 只列改法。

## 2. 合規（僅限自己的論文）
- 匿名：作者、致謝、單位、GitHub 連結、可辨識身分的自我引用。
- PDF metadata：用 pdfinfo 或 pypdf 讀取 Author、Creator、Producer、Title 欄位。檢查是否內嵌檔案路徑，例如 /Users/名字/。
- LaTeX 原始檔（若有）：\author 是否匿名，註解中是否有私人內容。
- Supplementary（若有）：檔名、程式碼中的使用者名稱與路徑、git 紀錄。
- 格式：頁數與模板版本是否符合目標會議當年的規定。不確定時用 WebSearch 查詢 author guidelines。
- 會議要求的 checklist（例如 NeurIPS paper checklist）是否填寫完整。

輸出：合規檢查表（項目、結果、位置、修正方式）。

## 3. 合併交付
1. 閱讀導引：在 `issues.json` 的 `reading_guide` 加入 R1、R2⋯，標出問題定義、主要 claim、貢獻列表、關鍵定義與符號、核心公式、演算法、主要結果的圖表、限制。規格見 `pdf-annotation.md`。
2. 總報告 `<論文簡稱>_review_<zh 或 en>.md`：
   1. Outline。
   2. 結論摘要：整體判斷與傾向、定位與定位評估（取自 paper-novelty-positioning）、Fatal 問題總表（編號、問題、位置、對應方案；自己的論文加 A／B 類）。
   3. 論文理解（取自 `understanding.md`）。
   4. 每個已執行的 skill 一節：放該 skill 報告的結論與問題表，並連到完整報告。未執行的 skill 寫「未執行」。
   5. 修改計畫（自己的論文分 A 類與 B 類）。
   6. 合規檢查表（別人的論文寫「不適用」）。
   7. 審查設定與範圍：語言、模式、目標會議、審查時間；各 skill 的覆蓋表；沒做到的項目與影響；交付前檢查的結果。
   - 總報告必須列出 `issues.json` 中的每一個問題編號。
3. 註解 PDF `<原檔名>_annotated.pdf`：依 `pdf-annotation.md` 加問題註解、圖的註解、閱讀導引、總評頁與顏色圖例頁。總評頁的 7 項中，對應 skill 未執行時寫「未執行 <skill 名稱>」，不得留空。
4. 交付前檢查：

```
python check_review.py --pdf <原檔名>_annotated.pdf --md <總報告>.md --issues issues.json
```

- `check_review.py` 與 `annotate_tools.py` 在本資料夾。
- 輸出「全部通過」才可以交付。有錯誤就修正後重跑。
- 確實無法修正的項目（例如圖是掃描圖片），在「審查設定與範圍」逐項說明原因。
- 無法執行程式的環境：仍產生 `issues.json` 與 md，並說明 PDF 註解與交付前檢查未執行。

## 輸出
1. 總報告 md。
2. 註解 PDF。
3. `issues.json`。

三個檔案都用 SendUserFile 傳給使用者。
