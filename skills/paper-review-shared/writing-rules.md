# 寫作規範（ASD-STE100）

供 paper-presentation-check、paper-limitations、paper-revision 使用。內容與原 12 步 skill 的「寫作規範」相同。

## 中文（ASD-STE100 風格改編）
1. 一物一名：核心術語全文統一，不用同義詞替換。只有指涉不同實體時才換詞。
2. 一句一事：每句只講一個動作或論點，不超過 25 字。不用分號。遇到三層以上的連接詞長句就拆句。
3. 主動語態：寫成「主詞＋動詞＋受詞」。不用無主詞句和「被⋯所⋯」。自我指涉用「本研究⋯」或「實驗結果顯示⋯」。
4. 刪虛詞：
   - 禁用「進行⋯的分析」、「具有⋯的重要性」、「在某種程度上」、「做出⋯的貢獻」、「針對⋯的部分」。改用單一動詞，例如把「進行資料的清洗」改成「清洗資料」。
   - 禁用「非常」、「極度」、「大幅度」、「顯著地」，附 p 值時除外。改用數據或比較。

## 英文（ASD-STE100 Issue 9）
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
