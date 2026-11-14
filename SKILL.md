---
name: paper-12-step-review
description: 用 12 步框架閱讀、審查或修改 ML 論文，借鑑 Google Deep Review 的分段驗證流程，依 ASD-STE100 檢查文字，從同一份問題清單產生 md 報告與分色註解的 PDF，並在交付前自動檢查。使用者要求讀論文、審稿、改論文或預測 reviewer 問題時使用。
---

# 論文 12 步審查

## 開始前

### 1. 讀論文
- 讀完整篇論文，包含 appendix 與 supplementary。
- PDF 用 pdf-reading skill 讀取。有 LaTeX 原始檔時一併讀取。
- 圖表要看圖本身，不只看 caption。

### 2. 選擇設定
用 AskUserQuestion 一次問完以下問題。使用者在請求中已說明的項目不再問。沒有 AskUserQuestion 時，用文字列出選項詢問。

| 問題 | 選項 |
|---|---|
| 報告語言 | 中文版／英文版 |
| 論文來源 | 自己的論文／別人的論文 |
| 目標會議 | ICLR／NeurIPS／CVPR／ICML（可自行填寫） |

各選項的影響：
- 中文版：報告與 PDF 註解用繁體中文撰寫，術語保留英文，並遵守中文寫作規範。
- 英文版：報告與 PDF 註解用英文撰寫，並遵守英文寫作規範（ASD-STE100）。
- 論文本文依論文本身的語言選用規範檢查，不受報告語言影響。
- 自己的論文：執行第 1–12 步，並把問題分成 A 類與 B 類（見通用規則）。
- 別人的論文：跳過第 12 步。第 11 步改為「若我是作者會怎麼改」。
- 目標會議：決定頁數上限、匿名規定與評分標準。不確定規定時，用 WebSearch 查詢該會議當年的 author guidelines。

### 3. 複述理解
逐項列出以下內容，每項 1–2 句：
- 問題：論文解決什麼問題。
- 方法：論文用什麼方法。
- 主要 claim：論文宣稱什麼。
- 實驗：用哪些實驗支持 claim。
- 貢獻：論文列出的貢獻。
- Novelty：與既有工作相比，新在哪裡。

使用者確認後才繼續。使用者修正時，以修正後的理解為準。

## 審查流程（借鑑 Google Deep Review）
Google Deep Review 的作法：先分段，依難度分配心力，每段帶著全文脈絡驗證，最後統整並查證。本 skill 依此流程執行，再把結果填入第 1–12 步。

0. 高層先判斷：分段驗證之前，先完成第 1、6、7、8 步的初稿（問題、新穎性、claim、定位）。
   - 高層判斷有 Fatal 問題時，相關的低層問題標成「依附於 Px-y」。這些問題照樣列在報告中，但等高層問題解決後再處理。
   - 細部驗證完成後，回頭修正高層初稿。
1. 分段：依主題把論文切成段落，例如 introduction、related work、method、theory、experiments、appendix。段落可以重疊，但必須涵蓋全文。
2. 分配心力：數學推導、證明、演算法與主實驗表格逐行檢查。Introduction 與 related work 的檢查可以較快。
3. 逐段驗證：每段都對照全文，檢查交叉引用。
   - 數學：逐步重推每個推導。檢查不等號方向、遺漏的絕對值、重複定義的符號、off-by-one、維度是否一致。
   - 定理：嘗試構造反例。找到反例時列為 Fatal。
   - 演算法：pseudo-code、文字描述與公式是否一致？
   - 實驗：有沒有 confounding factor？有沒有缺少的比較？表格數字是否與內文一致？
4. 統整與查證：
   - 合併重複的問題。
   - 跨段一致性：abstract、introduction 與結論中的數字和 claim，是否與表格一致？符號是否全文一致？
   - 回報前重新確認每個問題。無法確認的問題刪除，或標為「待確認」。寧可少報，不要誤報。
   - 判斷證明有誤之前，再推導一次。誤判正確的證明是這類工具已知的失誤。
   - 用 paper-search 或 WebSearch 確認引用的論文存在，且作者與年份正確。

## 通用規則
- 每個判斷都標出依據位置（Sec.、Eq.、Fig.、Table、頁碼）。
- 論文沒寫的內容標「論文未提及」。不替作者補充。
- 每個問題標註嚴重度：
  - Fatal：足以導致 reject。例如 claim 沒有實驗支持、baseline 不公平、主結果不顯著、證明有誤。
  - Major：reviewer 會要求補充，但不至於直接 reject。
  - Minor：寫作、格式或用詞問題。
- 每個問題給一個編號。例如 P5-2 代表第 5 步的第 2 個問題。第 11 步與 PDF 註解都用這個編號。
- 自己的論文：每個問題再標註類別。
  - A 類（本質問題）：需要改寫 claim、補做或重做實驗、重新做 paper survey，或修改方法與理論。這類修改會改變論文的內容。
  - B 類（呈現問題）：行文不順、前後不連貫、太像 AI 寫的、術語不一致、圖表呈現不佳。這類修改不改變論文的內容。
- 報告與每一節都先寫結論，再寫細節。
- 報告保持精簡。Appendix 與 ablation 只在需要時引用。
- 所有問題都先寫進問題清單 `issues.json`（見「問題清單」），md 報告與 PDF 註解都由它產生。
- 不得省略：
  - 禁止「精簡版未逐幅展開」、「其餘同理」、「以相同標準檢查」這類跳過的寫法。每張圖（正文與 appendix）、每條寫作規則、每個步驟都要實際做完。
  - 某一步真的做不到時（例如無法上網），寫進「審查設定與範圍」，說明沒做什麼、原因與影響。
- 不得套版：每則註解與每張圖的評論都必須提到該處獨有的內容，例如 panel 編號、座標軸名稱、顏色、符號或原句用字。

## 寫作規範

### 中文（ASD-STE100 風格改編）
1. 一物一名：核心術語全文統一，不用同義詞替換。只有指涉不同實體時才換詞。
2. 一句一事：每句只講一個動作或論點，不超過 25 字。不用分號。遇到三層以上的連接詞長句就拆句。
3. 主動語態：寫成「主詞＋動詞＋受詞」。不用無主詞句和「被⋯所⋯」。自我指涉用「本研究⋯」或「實驗結果顯示⋯」。
4. 刪虛詞：
   - 禁用「進行⋯的分析」、「具有⋯的重要性」、「在某種程度上」、「做出⋯的貢獻」、「針對⋯的部分」。改用單一動詞，例如把「進行資料的清洗」改成「清洗資料」。
   - 禁用「非常」、「極度」、「大幅度」、「顯著地」，附 p 值時除外。改用數據或比較。

### 英文（ASD-STE100 Issue 9）
論文屬於 STE 的 descriptive writing。只套用以下規則。檢查時用規則編號（E1–E21）標註違規。

**詞（Words）**
- E1 一物一名：同一概念全文只用一個術語。不以 "the model"、"our approach"、"the system" 交替指稱同一實體。
- E2 一詞一義：同一個字全文只用一個意思。例如 "sample" 若指資料點，就不再用來表示「抽樣」的動作。
- E3 名詞串：多字名詞串不超過 3 個字。超過時改寫成介系詞片語，例如 "test set accuracy improvement" 改成 "the accuracy improvement on the test set"。已定義的方法名稱與技術名詞不受此限。
- E4 簡單字：用常見的短字，例如 utilize 改成 use，prior to 改成 before，subsequent to 改成 after，initiate 改成 start，terminate 改成 stop。領域術語不受此限。
- E5 不用 phrasal verbs：改用一個精確的動詞，例如 "figure out" 改成 "determine"。
- E6 不把動詞名詞化："perform an analysis of" 改成 "analyze"，"in order to" 改成 "to"，"it is necessary to" 改成 "we must"。
- E7 禁用填充語："it is worth noting that"、"plays an important role"、"to some extent"。
- E8 禁用模糊副詞："very"、"extremely"、"dramatically"、"significantly"，附統計檢定時除外。改用數據或比較。

**動詞（Verbs）**
- E9 主動語態：用 "We + verb"。只有執行者未知時才用被動。
- E10 簡單時態：優先用 simple present、simple past、simple future。避免進行式與完成式。
- E11 不用縮寫："don't" 改成 "do not"，"can't" 改成 "cannot"。

**句子（Sentences）**
- E12 一句一事：每句只講一個論點。
- E13 句長：每句不超過 25 words。
- E14 不省略冠詞（the、a、an），也不省略子句中的 "that"。
- E15 代名詞：指涉不明時改寫成名詞。句首的 "This" 後面補上名詞，例如 "This result shows..."。
- E16 條件在前：先寫條件，再寫動作，例如 "If the loss diverges, we reduce the learning rate."
- E17 條列：三個以上的並列項目改用條列（vertical list）。

**段落（Paragraphs）**
- E18 每段只有一個主題。
- E19 每段不超過 6 句。

**標點（Punctuation）**
- E20 不用分號。改成句號並另起一句。
- E21 內文不用拉丁縮寫："i.e."、"e.g."、"etc." 改寫成英文或條列。引用格式中的 "et al." 不受此限。

**字數計算（用於 E13）**
- 數字、單位、縮寫、專有名詞、連字號詞各算 1 字。
- 括號內的文字算 1 字。
- 行內數學式與引用標記（例如 [12]）各算 1 字。

**不適用的 STE 規則**
- Approved dictionary：論文需要領域詞彙，不限定字典。
- Procedural writing（祈使句、20 字上限）：只套用在 appendix 的操作步驟，例如重現實驗的指令。
- Safety instructions：論文中沒有這類內容。

## 步驟

### 1. Problem formulation
檢查：
- 問題是否重要？論文是否說明誰會受益？
- 為何值得關注？
- 有哪些切入方向與應用？
- Input 與 output 是否明確定義，包括資料型態、維度與評估指標？

輸出：一段問題摘要，加上 input／output 定義。

### 2. Naive thoughts
檢查：
- 列出 2–3 個直覺解法。
- 說明每個解法為何失敗或不夠好。
- 檢查論文是否說明為何不用這些解法。

輸出：表格，欄位為「直覺解法、問題、論文是否回應」。

### 3. Related work
檢查：
- 寫出領域脈絡：這條研究線如何演變到今天？第 8 步的定位分析會用到。
- 依方法類別將既有工作分組。每組列出代表方法與主要不足。
- 用 paper-search 搜尋近期工作，檢查論文是否漏掉重要的工作。
- 沿引用關係擴充 related work：用 paper-search（OpenAlex）查詢論文引用的關鍵工作。
  - 往後找：這些工作被誰引用（cited by），找出後續與同期的工作。
  - 往前找：這些工作引用了誰（references），找出共同的源頭工作。
  - 被多篇關鍵工作共同引用，或共同引用多篇關鍵工作的論文，優先檢查是否應該納入。
- 列出應該比較、但論文沒有比較的 baseline 與 dataset。
- 用 mermaid 圖畫出既有工作之間的關係：
  - 節點：論文（作者＋年份），依方法類別分組（subgraph）。
  - 邊：延伸、改進、比較、合併等關係，並在邊上標註關係類型。
  - 本論文另外標示，並連到它直接延伸或比較的工作。
  - 論文漏掉的重要工作用虛線框標示。

輸出：領域脈絡（3–5 句）、mermaid 關係圖、表格（類別、代表方法、不足、論文是否比較）、引用擴充後找到的遺漏工作、缺少的 baseline 與 dataset 清單。

### 4. Methodology
檢查：
- 描述 inference pipeline 與 training pipeline 的資料流。
- 每個設計決策：動機是什麼？有沒有對應的數學推導？依審查流程第 3 步驗證推導是否正確。
- 每個 block／function：為什麼這樣設計？換成更簡單的設計會怎樣？
- 第 3 步的每個不足，由方法中哪個部分負責解決？
- 寫出預期結果，留到第 5 步對照。
- 論文類型：判斷這是方法論文、理論論文，還是應用論文，並說明依據。類型決定後續的檢查重點：
  - 方法論文：方法設計是否有動機，實驗是否證明方法有效。
  - 理論論文：定理與證明是否正確，假設是否合理。
  - 應用論文：問題是否真實存在，方法是否適合該應用，評估是否貼近實際使用情境。
- 理論基礎：論文是否有足夠的理論支撐？
  - 問題是否有數學上的 formulation（目標函數、假設、符號定義）？
  - 方法是否有理論支持，例如收斂性、界限或與既有理論的連結？
  - 若沒有理論，論文是否用足夠的實證分析彌補？
  - 依論文類型判斷理論基礎是否足夠。理論論文的要求最高，應用論文的要求最低。

輸出：pipeline 描述、設計決策表（block、動機、數學依據、疑點）、數學驗證結果、預期結果、論文類型與依據、理論基礎評估。

### 5. Experimental results
檢查：
- 主實驗是否解決第 3 步列出的每個不足？逐一對照。
- Ablation 是否涵蓋第 4 步的每個設計決策？
- 提升是否顯著？記錄數值、variance、seed 數，以及是否做統計檢定。
- Baseline 是否公平：相同資料、相同調參預算、相同計算量。
- 有沒有 confounding factor？
- 結果與第 4 步的預期是否一致？不一致時分析原因。
- 提升不顯著時分析原因。這是常見的 reject 理由。

輸出：對照表，欄位為「不足、對應實驗、結果、是否解決」。

### 6. Novelty
檢查：
- 列出論文宣稱的貢獻。
- 判斷每項貢獻屬於新概念、既有方法的新組合，或既有方法搬到新領域。
- 若只是組合，組合本身是否帶來非顯而易見的結果？
- 貢獻應如何表述，才能讓 reviewer 認可？

輸出：貢獻表，欄位為「宣稱、實際新穎程度、建議表述」。

### 7. Limitation and claim
檢查：
- 列出論文尚未解決的限制。
- 若看不出限制，檢查 task 是否太少或分析不足。
- 逐條檢查 claim 是否超出實驗支持的範圍。
- 提出 future work 方向。

輸出：限制清單、overclaim 表（claim、位置、支持的實驗、落差）、future work。

### 8. Overall assessment 與定位
**總結**
- 綜合第 1–7 步，判斷這是否為好論文。
- 給出傾向：Accept、Borderline 或 Reject。
- 列出最強的 3 個優點與最嚴重的 3 個問題，並說明理由。

**定位**
- 研究脈絡：論文屬於哪條研究線？延續或挑戰了哪些工作？
- 貢獻類型：新問題、新方法、新理論、新分析、新 benchmark，或實證研究。
- 目標讀者：哪個社群會引用這篇論文？
- 最接近的 2–3 篇工作，以及本論文與它們的差異。

**定位評估：好或壞**
逐項判斷，並說明理由：
- 定位是否有證據支撐？claim 的範圍是否與實驗範圍相符？
- 定位是否太廣（無法證明）或太窄（貢獻顯得小）？
- 該研究線是否過度擁擠，使貢獻難以凸顯？
- 定位是否符合目標會議的讀者與評分標準？
- 若定位不佳，提出更好的定位，並說明需要哪些證據支持。

### 9. Presentation

**逐層閱讀（由粗到細）**
依序只讀到下列每一層，檢查讀者能否說出論文的問題、方法與貢獻：
1. 標題
2. 摘要
3. Figure 1 與 caption
4. Introduction 的貢獻列表
5. 章節與小節標題
6. 每段的第一句
7. 完整內文

每層都要能獨立讀懂，下一層只補充細節。哪一層讀不懂，或與上一層矛盾，就標出斷掉的層級與原因。

**文字**
- 英文論文依 ASD-STE100 規則 E1–E21 檢查全文。中文論文依中文規範 1–4 檢查。
- 掃過主文全文，不是抽樣。先輸出規則統計表：每條規則一列（E1–E21 或中文 1–4），欄位為「規則編號、規則說明、違規次數」，0 次也要列。
- 再列違規明細：規則編號、規則說明、位置、原句與改寫。規則說明用一句話寫出該規則的內容，例如「E13：每句不超過 25 words」。同一規則的違規超過 10 處時，列前 10 處並註明總數。
- 是否由淺入深？讀者產生疑問時，下一段是否就給出答案？
- 段落之間是否連貫？每段開頭是否接得上前一段？
- 是否有明顯的 AI 寫作痕跡？例如空泛的強調詞（crucial、pivotal、seamlessly、delve、leverage）、固定的三項並列、每段結尾重複總結、過多破折號、過度保留的語氣。
- 主文有無冗餘或重複內容？
- 比較結果能否改用表格或圖表？
- 用詞是否過於冷僻？
- 以上連貫性、AI 寫作痕跡、冗餘、改用表格或圖表、冷僻用詞五項，在報告中用一張表格回覆。欄位為「檢查項目、結果（有問題／無問題）、位置、原句或內容、說明、改法」。同一項目有多處問題時，每處各佔一列。
- Causal（先定義、後使用）：每個術語、符號、縮寫與概念第一次使用之前，前文都要已經定義或描述。
  - 摘要與 introduction 用到的術語，是否在使用處或之前說明？
  - 數學符號是否在公式之前或緊接著定義？
  - 圖表中的術語與符號，是否在該圖第一次被引用之前定義？
  - 當前句子是否要靠後文才定義的內容才能讀懂？
  - 列出所有檢查過的術語與符號，不只列出有問題的。欄位為「術語、第一次使用的位置、定義的位置（或「未定義」）、是否違規、建議改法」。

**每張圖的分析流程**
方法圖與數據圖都依此流程分析。分析時把該頁轉成圖片（`page.get_pixmap(dpi=200)`），看圖本身。
1. 切分區塊：把圖切成幾個區塊（panel、模組、階段或圖例），逐一寫出每個區塊的內容與用途。
2. 評估切分：
   - 區塊的切法是否對應論文的邏輯，例如 pipeline 的階段或方法的模組？
   - 有沒有該合併或該拆開的區塊？
   - 區塊之間的閱讀順序是否清楚？
   - 有問題時，提出新的切法。
3. 零先備知識檢查：假設讀者什麼都不知道，只看這張圖與它的 caption，不讀內文。
   - 列出圖中每個元素：區塊、圖示、箭頭、顏色、線型、符號、縮寫、座標軸、圖例。
   - 逐一判斷每個元素能否被理解。可以理解的條件只有兩種：
     - 能從圖中其他元素推得，例如由圖例、位置或箭頭方向推出含義。
     - 圖中文字或 caption 有描述它。
   - 兩種條件都不滿足的元素，列為問題，並提出改法：加標籤、加圖例、在 caption 補一句說明，或刪除該元素。
   - 檢查結果要讓讀者一眼看懂圖中所有元素。
4. 依四項標準評估。四項同等重要：
   - 正確性
   - 可讀性：文字是否過多？能否一眼看懂？
   - 精簡
   - 美觀
5. 總評：說明這張圖是否達成目的，以及最需要修改的地方。

**方法圖（pipeline、architecture）**
以下是方法圖在四項標準下的檢查細項。
- 正確性：圖中每個元件、箭頭、標籤都與方法描述一致。標籤用字與內文術語完全相同（E1）。
- 可讀性：
  - 版面對應結構：pipeline 由左到右，分層架構上下堆疊，階層由上而下。
  - 頂層元件超過 8 個時分組。
  - 箭頭盡量不交叉。
  - 不同類型的流向用不同箭頭樣式，例如實線表示資料流，虛線表示輔助流程。
- 精簡：
  - 只放核心資訊。圖中不放 caption 或標題文字。
  - 圖中文字太多時，改用編號或符號，再於 caption 說明。
  - 圖是否過於 low level 而顯得 trivial？
- 美觀：
  - 全篇使用同一種視覺風格。
  - 區塊底色用低飽和的淺色。飽和色只用在關鍵元件或最終輸出。
  - 標籤用 sans-serif 字型，數學變數用 serif 斜體，並與內文符號一致。
  - 避免 PowerPoint 預設樣式、混用字型、2D 與 3D 混用、高飽和底色。
- AI 生成痕跡：拼錯或變形的文字、風格不一的 icon、與內容無關的裝飾。
- Figure 1：讀者只看這張圖，能否說出問題、方法與貢獻？

**數據圖**
- 圖型是否合適：

| 要呈現的內容 | 建議圖型 |
|---|---|
| 隨訓練步數或時間的趨勢 | line plot，加上 uncertainty band |
| 類別或 ablation 比較 | grouped bar chart，標上數值 |
| 分布 | violin plot 或 box plot |
| 相關性 | scatter plot |
| 矩陣，例如 confusion matrix | heatmap，標上數值 |
| 多個方法、單一指標 | horizontal bar chart |
| 組成比例 | stacked bar chart，不用圓餅圖 |

- 顏色：
  - 本方法用醒目顏色，baseline 用灰色。
  - 用色盲友善色盤（例如 Okabe-Ito），並搭配不同 marker 或線型。
  - 連續值用 Viridis，正負值用 Coolwarm。不用 rainbow 或 jet。
- 誤差：標出 error bar 或 band，並說明是 std 還是 CI，以及用了幾個 seed。
- 格式：
  - 用向量 PDF。
  - 寬度符合會議欄寬。
  - 圖中字級接近內文字級。
  - 格線用淺色。
  - 不用 3D 長條圖或 Excel 預設樣式。

**圖的建議**
每張有問題的圖都要給出具體的重新設計：版面配置、元件與分組、箭頭樣式、顏色用途、要刪除的文字。

輸出：逐層閱讀結果表（層級、能否讀懂、斷掉的原因）、文字檢查表（檢查項目、結果、位置、原句或內容、說明、改法）、寫作規則統計表、寫作違規明細表（規則編號、規則說明、位置、原句、改寫）、Causal 檢查表（術語、第一次使用位置、定義位置、是否違規、改法）、每張圖的分析表（一張圖一列，欄位為圖號、區塊切分、切分問題與改法、零先備知識檢查、正確性、可讀性、精簡、美觀、總評；正文與 appendix 的圖都要列）、重新設計建議。

### 10. Reviewer personas
依序以下列身分提問。每個身分至少提 3 題。

| 身分 | 閱讀方式 | 提問方向 |
|---|---|---|
| 領域專家 | 逐節細讀，對照熟悉的方法 | 與 SOTA 的差距、遺漏的比較 |
| 領域新手 | 從頭讀，卡住就停 | 未定義的術語、跳過的推導 |
| 資深研究者 | 看研究脈絡 | 問題是否值得做、貢獻是否持久 |
| 嚴苛批評者 | 專找漏洞 | 能推翻主 claim 的反例 |
| 統計學家 | 看實驗設定與數字 | 顯著性、seed、variance、多重比較 |
| 方法學家 | 看實驗設計 | baseline 公平性、資料洩漏、調參預算 |
| 只讀標題、摘要和 Figure 1 的讀者 | 只看前兩頁 | 看完能否說出貢獻 |
| 只花 30 秒的 AC | 看摘要和主表 | 能否找到 reject 的理由 |

每題包含：問題、在論文中搜尋的位置、是否找到答案、嚴重度。優先列出足以推翻論文的問題。

### 11. Revision plan
- 彙整第 1–10 步的所有問題編號。
- 依「問題定義 → 方法 → 實驗 → 寫作 → 格式」排序。上層錯誤會使下層修改失去意義。
- 自己的論文：分成兩部分，先 A 類再 B 類。
  - **A 類：本質問題**（claim、實驗、paper survey、方法、理論）
    - 每個 Fatal 和 Major 問題至少提出 3 個方案。
    - 每個方案包含：具體改法、所需成本（時間與計算資源）、預期實驗結果、結果不如預期時的退路。
    - 方案之間要有實質差異。例如一個縮小 claim，一個補實驗，一個修改方法。
  - **B 類：呈現問題**（行文、連貫性、AI 痕跡、術語、圖表）
    - 每個問題列出改法。英文改寫遵守 ASD-STE100 規則 E1–E21，中文改寫遵守中文規範。
    - 圖的問題附上第 9 步的重新設計建議。
- 別人的論文：不分類，依上述排序列出「若我是作者會怎麼改」。每個 Fatal 和 Major 問題至少 3 個方案。
- Minor 問題只列改法。

### 12. Compliance（僅限自己的論文）
- 匿名規範：檢查作者、致謝、單位、GitHub 連結、可辨識身分的自我引用。
- PDF metadata：用 pdfinfo 或 pypdf 讀取 Author、Creator、Producer、Title 欄位。檢查是否內嵌檔案路徑，例如 /Users/名字/。
- LaTeX 原始檔（若有）：檢查 \author 是否匿名，以及註解中是否有私人內容。
- Supplementary（若有）：檢查檔名、程式碼中的使用者名稱與路徑、git 紀錄。
- 格式：頁數與模板版本是否符合目標會議規定？

輸出：合規檢查表，欄位為「項目、結果、位置、修正方式」。

## 問題清單（issues.json）
所有問題、閱讀導引與圖的評論先寫進一份 `issues.json`。md 報告、PDF 註解與總評頁都由這份清單產生，不另外分開寫，確保三者的編號與結論一致。

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
  ]
}
```

- `sentence` 必須從 `page.get_text()` 抽出的文字逐字複製整句，不能改寫或只截一段。
- `page` 是原論文的頁碼（從 1 開始）。無法定位的問題設為 `null`，md 中標註「PDF 未精確定位」。
- 別人的論文 `category` 設為 `null`。

## PDF 註解
報告完成後，依 `issues.json` 在論文 PDF 上標出問題、圖的評論與閱讀導引。

### 顏色
顏色依問題所屬的步驟決定。12 個步驟各用一個顏色，不得重複。

| 步驟 | 顏色 | Hex |
|---|---|---|
| 1 Problem formulation | 黃 | #FFEB3B |
| 2 Naive thoughts | 橙 | #FFB74D |
| 3 Related work | 紅 | #EF9A9A |
| 4 Methodology | 綠 | #A5D6A7 |
| 5 Experimental results | 藍 | #90CAF9 |
| 6 Novelty | 紫 | #CE93D8 |
| 7 Limitation and claim | 青 | #80CBC4 |
| 8 Overall assessment 與定位 | 棕 | #BCAAA4 |
| 9 Presentation | 萊姆綠 | #DCE775 |
| 10 Reviewer personas | 粉紅 | #F48FB1 |
| 11 Revision plan | 靛藍 | #9FA8DA |
| 12 Compliance | 灰 | #B0BEC5 |
| 閱讀導引 | 深灰 | #424242 |

PyMuPDF 的顏色用 0–1 的 RGB，hex 值除以 255。

### 問題註解
- 標題：問題編號｜步驟名稱｜嚴重度｜標註時間。自己的論文再加上 A 類或 B 類。例如「P9-3｜Presentation｜Minor｜B｜2026-11-14 15:18」。
- 標註時間：精確到年、月、日、時、分，格式為 YYYY-MM-DD HH:MM，使用使用者所在的時區。每則註解都要有。
- 內容：分多行撰寫，每個欄位一行，每個欄位至少一句完整的話，不得只寫關鍵字。語言與報告相同。
  - 文字問題：問題、原因（規則編號與規則說明）、建議改法、改寫範例。
  - Causal 問題：術語、第一次使用的位置、定義的位置（或「未定義」）、建議改法。
  - 其他問題：問題、原因、建議改法。
- 標記範圍：整句，不多也不少。
- 同一句有多個問題時，只標一次：
  - 標題列出所有問題編號，例如「P4-4／P7-5｜Methodology｜Major｜2026-11-14 15:18」。嚴重度寫最高的那個。
  - 內容依序寫出每個問題，問題之間空一行。
  - 顏色用步驟編號最小（最上層）的那個問題的顏色。
- 跨頁的句子：每頁各標一段。第一段寫完整註解，其餘各段的標題寫「Px-y（續）」。
- 無法定位的問題：用 `add_text_annot` 在相關段落旁加便利貼註解，顏色相同。

### 圖的註解
- 每張圖都要有一則，正文與 appendix 都算，即使沒有問題也要寫。
- 用 `add_rect_annot` 框住整張圖，不能只框 caption。框好後把框的範圍轉成圖片（`page.get_pixmap(clip=rect, dpi=100)`）實際看一次，確認框到的是圖。
- 標題：「Fig. N｜圖的評論｜Presentation｜標註時間」。
- 內容依序為：總評、區塊切分（列出每個區塊）、切分的問題與改法、零先備知識檢查、正確性、可讀性、精簡、美觀。每項都要寫到這張圖獨有的元素。
- 某個區塊有個別問題時，再框住該區塊，標題寫「Fig. N(b)｜⋯」。
- 顏色用第 9 步的顏色。

### 閱讀導引註解
除了問題註解，另外標出幫助理解論文的關鍵位置，並說明怎麼讀。自己的論文與別人的論文都要做。
- 要標的位置：問題定義、主要 claim、貢獻列表、關鍵定義與符號、核心公式、演算法、主要結果的圖表、限制。
- 編號：R1、R2⋯，依建議的閱讀順序編號。
- 標記方式：
  - 文字用底線，標出整句，不能只標標題（例如只標「Theorem 3.2」）。
  - 圖表用框線框起來。
  - 顏色一律用深灰 #424242。
- 標題：R 編號｜閱讀導引｜標註時間。
- 內容：分多行撰寫，每個欄位一行，每個欄位至少一句完整的話：
  - 這段在講什麼：用白話說明。
  - 為什麼重要：與論文主線的關係。
  - 怎麼讀：需要的先備知識、該注意的細節、第一次讀可否略過。
  - 前後關聯：要與哪些段落、公式或圖表一起看。

### 總評頁與圖例頁
- 所有註解完成後，在 PDF 最前面插入總評頁：`doc.new_page(0, width=..., height=...)` 與 `page.insert_textbox(...)`。中文用 `fontname="china-t"`，英文用 `fontname="helv"`。`insert_textbox` 回傳負值表示內容超出一頁，此時在後面接續插入一頁。
- 總評頁最上方寫上審查時間（YYYY-MM-DD HH:MM），再由 high level 寫到 low level，7 項都要寫，不能只寫「詳見 md」：
  1. 整體判斷與傾向（一到兩句）。
  2. 定位與定位評估。
  3. 論文類型與理論基礎。
  4. Fatal 問題。自己的論文分成 A 類與 B 類。
  5. 方法與實驗的主要問題。
  6. 呈現問題：逐層閱讀、圖、文字、Causal。
  7. 格式與合規。別人的論文寫「不適用」。
  每一項都附上對應的問題編號。
- 在 PDF 最後加一頁顏色圖例，列出 12 個步驟與閱讀導引的顏色與 hex 值。
- 存成 `<原檔名>_annotated.pdf`，不覆蓋原檔。

### 作法
先安裝 PyMuPDF（`pip install pymupdf`），再把以下程式存成 `annotate_tools.py` 使用。

- `mark(page, sentence, ...)`：用整句原文比對頁面上的每個字，逐行標記。能處理跨行、連字號斷行，以及投稿版 PDF 的行號。
- `figure_rect(page, n)`：依 caption「Figure n:」往上找圖的範圍。回傳 `None` 時，把整頁轉成圖片，目視決定範圍。
- 處理 annotation 時，`page` 物件要存在變數裡重複使用，不要每次都寫 `doc[i]`，否則 annotation 會失去綁定。

```python
import re, pymupdf

def norm(s):
    s = re.sub(r"(?<![\w.])\d{1,3}(?![\w.])", " ", s)   # 去掉行號這類獨立的 1–3 位數字
    return re.sub(r"[\s\-‐‑–]", "", s).lower()

def find_sentence(page, sentence):
    """回傳整句每一行的矩形。能處理跨行、連字號斷行、行號。找不到回傳 None。"""
    words = page.get_text("words")
    buf, owner = "", []
    for i, w in enumerate(words):
        n = norm(w[4])
        buf += n
        owner += [i] * len(n)
    target = norm(sentence)
    k = buf.find(target)
    if not target or k < 0:
        return None
    idx = sorted(set(owner[k:k + len(target)]))
    lines = {}
    for i in idx:
        key = (words[i][5], words[i][6])          # (block, line)
        r = pymupdf.Rect(words[i][:4])
        lines[key] = lines[key] | r if key in lines else r
    return list(lines.values())

def marked_text(page, annot):
    v = annot.vertices or []
    rects = [pymupdf.Quad(v[i:i+4]).rect for i in range(0, len(v), 4)]
    out = []
    for r in rects:
        ws = [w for w in page.get_text("words")
              if r.contains(pymupdf.Point((w[0]+w[2])/2, (w[1]+w[3])/2))]
        out += [w[4] for w in sorted(ws, key=lambda w: w[0])]
    return " ".join(out)

def mark(page, sentence, color, title, lines, kind="highlight", pdf_time=None):
    rects = find_sentence(page, sentence)
    if rects is None:
        return None
    f = page.add_highlight_annot if kind == "highlight" else page.add_underline_annot
    a = f(quads=[r.quad for r in rects])
    a.set_colors(stroke=color)
    a.set_info(title=title, content="\n".join(lines))
    if pdf_time:
        a.set_info(creationDate=pdf_time, modDate=pdf_time)
    a.update()
    return a

def figure_rect(page, n):
    """依 caption「Figure n:」往上找圖形範圍。找不到回傳 None，改用目視判斷。"""
    cap = None
    for b in page.get_text("blocks"):
        if re.match(rf"\s*(Figure|Fig\.)\s*{n}\s*[:.]", b[4]):
            cap = pymupdf.Rect(b[:4]); break
    if cap is None:
        return None
    g = [r for r in page.cluster_drawings()] + [pymupdf.Rect(i["bbox"]) for i in page.get_image_info()]
    g = [r for r in g if r.y0 < cap.y0 - 5 and r.y1 <= cap.y1 and r.x1 > cap.x0 - 20 and r.x0 < cap.x1 + 20 and r.height > 3]
    if not g:
        return None
    g = [pymupdf.Rect(r.x0, r.y0, r.x1, min(r.y1, cap.y0)) for r in g]
    g.sort(key=lambda r: -r.y1)
    u = pymupdf.Rect(g[0])
    if cap.y0 - u.y1 > 60:
        return None
    changed = True
    while changed:
        changed = False
        for r in g:
            if not u.contains(r) and r.y1 >= u.y0 - 15:
                u |= r; changed = True
    u.y1 = min(u.y1, cap.y0)
    # 納入圖內文字（座標軸、標籤）
    for b in page.get_text("blocks"):
        br = pymupdf.Rect(b[:4])
        if br.intersects(u) and br.y1 <= cap.y0 + 1:
            u |= br
    return u + (-3, -3, 3, 3)
```

## 交付前檢查
把以下程式存成 `check_review.py`，與 `annotate_tools.py` 放在同一個資料夾。所有檔案完成後執行：

```
python check_review.py --pdf <原檔名>_annotated.pdf --md <報告>.md --issues issues.json
```

- 輸出「全部通過」才可以交付。
- 有錯誤就修正後重新執行，直到通過。
- 確實無法修正的項目（例如圖是掃描圖片、無法自動定位），在「審查設定與範圍」逐項說明原因。

檢查項目：
- 總評頁有 7 項，最後一頁是顏色圖例。
- 每則註解的標題都有標註時間，內容至少兩行，且沒有只寫關鍵字的欄位。
- 每個問題的標記涵蓋整句，而且沒有超出原句。
- 同一頁沒有互相重疊的螢光標記。
- 每張圖都有圖的註解，框的高度足夠且框內有圖形，各張圖的評論沒有完全相同。
- md、`issues.json` 與 PDF 的問題編號一致。

```python
"""交付前檢查。用法：python check_review.py --pdf X_annotated.pdf [--md X.md] [--issues issues.json]"""
import argparse, json, re, sys, collections, pymupdf
from annotate_tools import norm, marked_text

ap = argparse.ArgumentParser()
ap.add_argument("--pdf", required=True); ap.add_argument("--md"); ap.add_argument("--issues")
a = ap.parse_args()
doc = pymupdf.open(a.pdf)
errs = []
ID = re.compile(r"\b([PR]\d+-?[A-Z]?\d*)\b")
TIME = re.compile(r"20\d\d-\d\d-\d\d \d\d:\d\d")
FRONT = ["整體判斷", "定位", "論文類型", "Fatal", "方法與實驗", "呈現", "合規"]
FRONT_EN = ["overall", "position", "paper type", "fatal", "method", "presentation", "compliance"]

# 1. 總評頁與圖例頁
front = doc[0].get_text().lower()
if not (all(k.lower() in front for k in FRONT) or all(k in front for k in FRONT_EN)):
    miss = [k for k in FRONT if k.lower() not in front]
    errs.append(f"總評頁缺少項目：{miss}")
if "#ffeb3b" not in doc[-1].get_text().lower():
    errs.append("最後一頁不是顏色圖例")

def caption_near(page, r):
    best = None
    for b in page.get_text("blocks"):
        m = re.match(r"\s*(Figure|Fig\.)\s*(\d+)\s*[:.]", b[4])
        if m:
            d = abs(b[1] - r.y1) if b[1] >= r.y0 - 5 else 1e9
            if best is None or d < best[0]:
                best = (d, f"Fig.{m.group(2)}")
    return best[1] if best else f"未知圖(p{page.number+1})"

# 2. 逐則檢查註解
issues = json.load(open(a.issues, encoding="utf-8")) if a.issues else None
sent = {}
if issues:
    for it in issues.get("issues", []) + issues.get("reading_guide", []):
        if it.get("sentence"):
            sent[it["id"]] = it["sentence"]
marked = collections.defaultdict(str)
fig_contents = collections.defaultdict(list)
fig_seen = set()
pdf_ids = set()
for pno in range(1, len(doc) - 1):
    page = doc[pno]
    hl = []
    for an in page.annots():
        t, title, content = an.type[1], an.info["title"], an.info["content"]
        if not TIME.search(title):
            errs.append(f"p{pno+1} {title[:20]}：標題沒有標註時間")
        lines = [l for l in content.split("\n") if l.strip()]
        if "（續）" not in title and (len(lines) < 2 or any(len(l.split("：", 1)[-1].strip()) < 5 for l in lines)):
            errs.append(f"p{pno+1} {title[:20]}：內容少於兩行，或有欄位只寫關鍵字")
        m = re.match(r"\s*(Fig\.\s*\d+)", title)
        is_fig = t == "Square" and (m or "區塊切分" in content or "Blocks" in content)
        if is_fig and "(" not in title.split("｜")[0]:
            key = m.group(1).replace(" ", "") if m else caption_near(page, an.rect)
            fig_seen.add(key)
            fig_contents[content].append(f"p{pno+1} {key}")
            r = an.rect
            draws = [d["rect"] for d in page.get_drawings()] + [pymupdf.Rect(i["bbox"]) for i in page.get_image_info()]
            if r.height < 60 or not any(r.intersects(d) for d in draws):
                errs.append(f"p{pno+1} {key}：框太小或框內沒有圖形（h={r.height:.0f}），可能框到 caption")
            continue
        for i in ID.findall(title.split("｜")[0]):
            pdf_ids.add(i)
        if t in ("Highlight", "Underline"):
            txt = marked_text(page, an)
            for i in ID.findall(title.split("｜")[0]):
                marked[i] += txt
            hl.append((t, title, [pymupdf.Quad(an.vertices[j:j+4]).rect for j in range(0, len(an.vertices), 4)]))
    for x in range(len(hl)):
        for y in range(x + 1, len(hl)):
            if hl[x][0] != hl[y][0]:
                continue  # 底線與螢光可以並存
            if any(r1.intersects(r2) and (r1 & r2).get_area() > 4 for r1 in hl[x][2] for r2 in hl[y][2]):
                errs.append(f"p{pno+1}：{hl[x][1][:12]} 與 {hl[y][1][:12]} 重疊，請合併成一則")

for c, where in fig_contents.items():
    if len(where) > 1:
        errs.append(f"圖註解內容完全相同（套版）：{where}")

# 3. 每張圖都要有圖註解
figs = set()
for pno in range(1, len(doc) - 1):
    for b in doc[pno].get_text("blocks"):
        m = re.match(r"\s*(Figure|Fig\.)\s*(\d+)\s*[:.]", b[4])
        if m:
            figs.add(f"Fig.{m.group(2)}")
if figs - fig_seen:
    errs.append(f"以下圖沒有圖註解：{sorted(figs - fig_seen, key=lambda s: int(s[4:]))}")

# 4. 整句涵蓋與標過頭
for i, s in sent.items():
    if i not in marked:
        continue
    ms, ss = norm(marked[i]), norm(s)
    if ss not in ms:
        errs.append(f"{i}：沒有涵蓋整句")
    elif len(ms) > len(ss) * 1.15 + 20:
        errs.append(f"{i}：標記超出原句")

# 5. md、issues.json、PDF 的編號一致
if issues:
    ids = {it["id"] for it in issues["issues"]}
    located = {it["id"] for it in issues["issues"] if it.get("page") and it.get("kind") != "figure"}
    for it in issues["issues"]:
        if it.get("kind") == "figure" and it.get("figure", "").replace(" ", "") not in fig_seen:
            errs.append(f"{it['id']}：{it.get('figure')} 沒有圖註解")
    if located - pdf_ids:
        errs.append(f"issues.json 有、PDF 沒標：{sorted(located - pdf_ids)}")
    if (pdf_ids - ids) - {r["id"] for r in issues.get("reading_guide", [])}:
        errs.append(f"PDF 有、issues.json 沒有：{sorted(pdf_ids - ids)}")
    if a.md:
        md_ids = set(re.findall(r"\bP\d+-\d+\b", open(a.md, encoding="utf-8").read()))
        if ids ^ md_ids:
            errs.append(f"md 與 issues.json 編號不一致：只在 md {sorted(md_ids - ids)}；只在 json {sorted(ids - md_ids)}")

print("\n".join(errs) if errs else "全部通過")
print(f"共 {len(errs)} 項錯誤")
sys.exit(1 if errs else 0)
```

## 工具替代（非 Claude 環境）
本 skill 在其他 AI 環境（例如 ChatGPT）也要能執行。以下工具不存在時，改用替代方式：

| 原工具 | 替代方式 |
|---|---|
| pdf-reading skill | 用 PyMuPDF 的 `page.get_text()` 讀文字，`page.get_pixmap()` 轉圖片看圖 |
| AskUserQuestion | 用文字列出選項詢問 |
| paper-search（OpenAlex） | 直接呼叫 OpenAlex API：`https://api.openalex.org/works?search=<標題>`；被引用用 `filter=cites:<work id>`；參考文獻看該筆的 `referenced_works` |
| WebSearch | 使用該環境的網頁搜尋 |
| SendUserFile | 提供檔案下載 |

- 以上方式都無法使用時，該步驟不能省略不提，要寫進「審查設定與範圍」，說明沒做什麼與影響。
- 無法執行程式的環境：仍要產生 `issues.json` 與 md，並在「審查設定與範圍」說明 PDF 註解與交付前檢查未執行。

## 輸出
1. md 報告，依選擇的語言撰寫，存成 `<論文簡稱>_review_<zh 或 en>.md`。結構如下：
   1. Outline：列出報告所有章節。
   2. 結論摘要：
      - 整體判斷與傾向（第 8 步的總結）。
      - 定位與定位評估（第 8 步的定位）。
      - Fatal 問題總表：列出問題編號、問題、位置、對應方案。自己的論文再加上 A／B 類欄位。
   3. 論文理解：開始前第 3 步的複述內容。
   4. 第 1–12 步，各一節。自己的論文在第 11 步分成 A 類與 B 類兩部分。
   5. 審查設定與範圍：
      - 語言、模式（自己或別人的論文）、目標會議、審查時間。
      - 沒做到的步驟、原因與影響，例如無法上網而未做引用擴充。
      - 交付前檢查的結果。未通過的項目逐項說明原因。
2. 註解 PDF：`<原檔名>_annotated.pdf`。第一頁是總評，最後一頁是顏色圖例。
3. `issues.json`：問題清單。

三個檔案都用 SendUserFile 傳給使用者。
