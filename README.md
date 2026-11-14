# paper-12-step-review

用 12 步框架閱讀、審查或修改 ML 論文的 AI skill。借鑑 Google Deep Review 的分段驗證流程，依 ASD-STE100 檢查文字，從同一份問題清單 `issues.json` 產生 md 審查報告與分色註解的 PDF，並在交付前自動檢查三者是否一致。

適用情境：讀論文、審別人的稿、改自己的論文、預測 reviewer 會問的問題（ICLR / NeurIPS / CVPR / ICML 等）。

## 檔案

| 檔案 | 用途 |
|---|---|
| `SKILL.md` | skill 本體：12 步流程、嚴重度規則、`issues.json` 格式、PDF 註解配色、輸出規格 |
| `annotate_tools.py` | PDF 註解工具：在 PDF 上定位整句（可處理跨行、連字號、行號）、加 highlight / underline、框出 Figure |
| `check_review.py` | 交付前檢查：總評頁、圖例頁、每則註解的格式、md / `issues.json` / PDF 三者編號一致 |

## 下載
按綠色 `Code` → `Download ZIP` 下載整個專案，或：

```bash
git clone https://github.com/faidavid7/paper-12-step-review.git
```

## 解壓縮
把下載的 `.zip` 解壓縮，會得到 `paper-12-step-review/` 資料夾（裡面有 `SKILL.md` 與兩個 `.py`）。

## 選擇資料夾（安裝）

**Claude Code**：把整個資料夾放到 skills 目錄。

```bash
# 個人全域（所有專案可用）
~/.claude/skills/paper-12-step-review/
# 或只給單一專案
<你的專案>/.claude/skills/paper-12-step-review/
```

**Claude.ai / Claude Desktop**：把資料夾壓成 zip，到 Settings → Capabilities → Skills 上傳。

**其他 AI 環境（ChatGPT 等）**：把 `SKILL.md` 的內容貼進對話或 system prompt，並上傳兩個 `.py`。`SKILL.md` 的「工具替代」一節列出沒有對應工具時的做法。

## 用法

### 1. 安裝相依套件

```bash
pip install pymupdf
```

### 2. 叫 AI 審論文
放好 PDF 後直接講，例如：

- 「用 12 步審這篇論文 `paper.pdf`」
- 「幫我審我自己要投 ICLR 的論文，列出 reviewer 會問的問題」
- "Review this paper with the 12-step framework"

AI 會一次問三個設定（使用者已說明的就不問）：

| 設定 | 選項 | 影響 |
|---|---|---|
| 報告語言 | 中文 / 英文 | 報告與 PDF 註解的語言 |
| 論文來源 | 自己的 / 別人的 | 自己的論文會做第 12 步，並把問題分成 A 類（本質）與 B 類（呈現） |
| 目標會議 | ICLR / NeurIPS / CVPR / ICML / 自填 | 頁數上限、匿名規定、評分標準 |

接著 AI 會先複述論文的問題、方法、claim、實驗、貢獻與 novelty，**你確認後才開始審**。

### 3. 拿到三個輸出

| 輸出 | 內容 |
|---|---|
| `<論文簡稱>_review_<zh 或 en>.md` | 審查報告：結論摘要、Fatal 問題總表、第 1–12 步逐節分析、審查設定與範圍 |
| `<原檔名>_annotated.pdf` | 註解 PDF：第一頁總評、內文依步驟分色標註、最後一頁顏色圖例 |
| `issues.json` | 問題清單，上面兩個檔都由它產生，編號如 `P5-2`（第 5 步第 2 個問題） |

每個問題都標嚴重度（Fatal / Major / Minor）與依據位置（Sec. / Eq. / Fig. / Table / 頁碼）。

### 4. 手動跑交付前檢查（選用）
AI 會自己跑；要自己確認時：

```bash
python check_review.py --pdf paper_annotated.pdf --md paper_review_zh.md --issues issues.json
```

印出「全部通過」且 exit code 為 0 即通過；否則逐項列出錯誤。`check_review.py` 需與 `annotate_tools.py` 放在同一資料夾。

## 授權
本專案採用 Apache License 2.0，詳見 [LICENSE](LICENSE)。
