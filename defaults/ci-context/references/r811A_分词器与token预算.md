# r811A 逐字存档｜分词器是上下文预算的隐藏分母（CI · 2026-11-26）

## 实拉来源（WebFetch 200 逐字，≥3 独立域）

### 源1 · compilenrun《WordPiece, Unigram and SentencePiece》
URL: https://www.compilenrun.com/docs/ai/llm/llm-tokenization/llm-wordpiece-unigram-sentencepiece/

对比表（逐字单元格）：
| Property | BPE (byte-level) | WordPiece | Unigram |
|---|---|---|---|
| Training direction | Bottom-up merges | Bottom-up merges | Top-down pruning |
| Merge or keep criterion | Pair frequency | Likelihood gain | Likelihood loss on removal |
| Encoding | Apply merges by rank | Greedy longest match | Viterbi (or sampling) |
| Unknown input | Never, bytes cover all | Whole word becomes `[UNK]` | `<unk>` unless byte fallback |
| Stores per-token score | No (only merge order) | No | Yes, log-probabilities |
| Example models | GPT-2 to GPT-4o, Llama 3, Qwen, DeepSeek-V3 | BERT, DistilBERT, ELECTRA | T5, ALBERT, XLNet, XLM-R, mBART |

逐字引文：
- "Byte fallback. With `byte_fallback=true`, characters outside the vocabulary are encoded as their UTF-8 bytes using 256 reserved tokens named `<0x00>` to `<0xFF>`. This gives SentencePiece the \"never unknown\" property of byte-level BPE while keeping a character-based vocabulary."
- "character_coverage (default 0.9995) keeps only the characters that cover that fraction of the training text; the rest map to `<unk>` unless byte fallback is on."
- "Whitespace is a symbol. Spaces are replaced by the meta-symbol `▁` (U+2581, \"lower one eighth block\") and become part of the pieces, so `▁the` is \"the\" with a preceding space. Decoding is concatenation plus replacing `▁` with a space, so the round trip is lossless."
- "Dummy prefix. By default (`add_dummy_prefix=true`) a `▁` is prepended to the input so the first word looks the same as words in the middle of a sentence. This is why the Llama 2 tokenizer often produces a lone `▁` token before digits or at the start of text."
- "Gemma, Llama 1 and 2 and Mistral 7B use SentencePiece with BPE, which sits between the first and third columns: BPE merges over characters, the `▁` whitespace convention, and byte fallback for rare characters."
- Llama 2 罕见字：`rare = "ꙮ"  # U+A66E` → `['▁', '<0xEA>', '<0x99>', '<0xAE>']`（三 UTF-8 字节 + dummy prefix + 数字拆分 `2,0,2,6`）。
- Common mistakes 逐字：
  - "Calling SentencePiece an algorithm. It is a library that trains Unigram (default) or BPE; check `model_type` before describing a model's tokenizer."
  - "Stripping `▁` or `##` by hand. Use the tokenizer's `decode`; manual string surgery breaks on edge cases like leading spaces and byte-fallback tokens."
  - "Forgetting the dummy prefix. SentencePiece adds a leading `▁` by default, so encoding \"Hello\" alone and in the middle of a sentence can give different first tokens."
  - "Training without byte fallback for open-domain text. With `character_coverage` below 1.0 and no byte fallback, rare characters silently become `<unk>`."
  - "Assuming WordPiece fails gracefully. One unknown character turns the whole word into `[UNK]`."
  - "Comparing algorithms on different data. Differences in training corpus and vocabulary size usually dwarf differences between BPE and Unigram."
- "Bostrom and Durrett (2020) found that Unigram segmentations align better with morphology than BPE and gave slightly better downstream results for BERT-style models of that size. Yet almost every large decoder-only LLM released since 2023 uses byte-level BPE."

### 源2 · AI Computer Institute《Tokenizer Design: BPE and SentencePiece》
URL: https://www.aicomputerinstitute.com/grades/12/chapters/g12s-tokenizer-bpe

逐字引文：
- "SentencePiece treats the raw input as a plain stream of Unicode characters, with no external pre-tokenizer at all — including no assumption that whitespace marks a word boundary."
- "Space itself is replaced by a literal symbol, \"▁\" (U+2581), placed in front of the word it used to precede, and treated by the vocabulary exactly like any other character."
- "Because ▁ is a normal vocabulary symbol rather than external metadata, detokenization becomes exact string concatenation of the output tokens followed by replacing ▁ with a real space: fully reversible, and identical code regardless of whether the underlying language uses spaces at all."
- "Unigram works in the opposite direction from BPE: instead of starting from single characters and growing the vocabulary by merging, it starts from a large seed vocabulary of candidate substrings — harvested from frequent substrings in the corpus, for instance via a suffix array — and shrinks it."
- "…discards the least useful slice of the vocabulary (~25% per iteration — the library's default shrinking_factor is 0.75), and repeats until the vocabulary reaches its target size — always keeping every individual byte or character as a guaranteed fallback, which is what lets SentencePiece, like byte-level BPE, avoid an unknown-token symbol entirely."
- "The Unigram model's explicit probabilities give it a capability greedy BPE structurally cannot have: because a word can have more than one valid segmentation under the model, SentencePiece can sample among them during training instead of always producing the single canonical split — Kudo calls this subword regularization."
- "Greedy BPE, by contrast, is fully deterministic — a given word always decomposes into exactly one fixed sequence of merges, with no room for that kind of variation."
- "OpenAI's GPT-2 (Radford et al., 2019) pushed one step further: instead of running BPE over Unicode characters, it runs over raw UTF-8 bytes, so the base vocabulary is fixed at exactly 256 symbols and no input string — any script, any emoji, any malformed text — can ever produce an unrepresentable character."
- "This byte-level choice is why GPT-family tokenizers never emit an unknown-token placeholder."
- "A character-level BPE tokenizer's base vocabulary is instead built only from characters that actually appeared in its training corpus; a character from a script the corpus never contained has no vocabulary entry at all and must be replaced by a designated unknown-token placeholder, permanently destroying that information."
- 英印字节比：English "India launched a satellite." = 27 chars / 27 bytes；Hindi "भारत ने एक उपग्रह लॉन्च किया।" = 29 chars / 77 bytes；77/27 ≈ 2.85。
- "The Devanagari block (U+0900–U+097F …) sits above U+0800, and UTF-8's encoding rule requires three bytes for every code point from U+0800 to U+FFFF, against one byte for the ASCII range every English letter lives in."
- "if that corpus is dominated by English and other Latin-script web text, the tokenizer accumulates thousands of merge rules that fold common English byte sequences — \"ing\", \"tion\", \" the\" — into single tokens, while Devanagari, Tamil, or Bengali byte sequences, being rarer in that same mix, get far fewer merges."
- "The 2.85x byte-length ratio measured above is therefore a *floor* on the real token-count penalty, not the actual figure — the true gap is typically wider once you account for how unevenly the merge budget was spent during training."
- "The token-count ratio compounds the encoding-length ratio rather than merely inheriting it, making the real gap at least 2.85x, typically by a further, corpus-dependent margin."

### 源3 · Belgavi.AI Lab《SentencePiece Tokenizer Explained》
URL: http://aicassindra.com/blogs/transformer_math/tm_sentencepiece_deep.html

逐字引文：
- "Choose deliberately; the choice is baked into the model file forever."
- "SentencePiece makes this explicit with character_coverage — typically 0.9995 for character-rich languages like Japanese and 1.0 for Latin scripts — meaning the alphabet keeps the most frequent characters covering that fraction of the corpus and discards the long tail. Without a safety net, any discarded character at inference time collapses to <unk>, and destroys the round trip."
- "With byte_fallback=true, the vocabulary reserves 256 pieces …, and any character with no piece is emitted as its raw UTF-8 bytes. Nothing is ever unknown, and decode still reconstructs the string exactly. The cost is length: a rare CJK character or emoji that would have been one token becomes three or four byte tokens. That is a good trade — correctness always, with a length penalty only on genuinely rare input."
- "One library, several model types. SentencePiece is a container for segmentation algorithms, not one algorithm. model_type selects among four: unigram (the default), bpe, char, and word."
- "vocab_size is the one hyperparameter you must set, and it trades two costs against each other. A larger vocabulary means longer pieces, so fewer tokens per document … It also means a taller embedding matrix: V × d parameters, doubled if the output head is untied."
- 算例（d=2048, corpus=100M English chars）：V=32,000 → ~3.9 chars/token → 25.6M tokens → embed 65.5M params；V=128,000 → ~4.5 chars/token → 22.2M tokens (-13%) → 262.1M params (+196.6M)。
- "Quadrupling V bought a 13% length reduction for roughly 197M extra parameters … Compression gains are strongly sublinear in V, so 32k–64k remains the sweet spot for monolingual small models; the pressure toward 128k and beyond comes almost entirely from multilingual coverage."
- "Feeding the model different segmentations of the same word across training steps acts as data augmentation directly on the input representation … measurably improves translation quality and robustness, especially on low-resource and morphologically rich language pairs."

### 源4（二手，立场登记）
- fudengji.cn/article/12906：BPE 未登录词处理与多语言分词策略；中文 token 膨胀举例（"阿司匹林水杨酸酯" 拆 5+ token）。
- guanweilu.cn/article/12152.html：字节级 BPE 多语言信息密度表（英语 ~0.75–0.85 token/word、德语/俄语 ~1.0–1.2、简体中文 ~1.5–2.0、日语 ~2.0–3.0）。
- tsight.io/articles/12619516：领域级分词扩充「能将平均 Token 长度缩短 15%-20%」（工程博客，无同行评议，立场登记）。
以上为中文二手转述，仅作交叉佐证与语感校准，不冒充一手论文逐字，不作唯一证据。

## 判非
- 三算法是三个控制面（训练方向/编码/UNK 行为），非同一旋钮档位；BPE 无 OOV 的前提是 byte-level，字符级 BPE 照样 UNK。
- SentencePiece 是库不是算法；手剥 ▁/## 破坏 byte-fallback 边界。
- byte fallback 用长度换覆盖：罕见 CJK/emoji 1 token → 3–4 byte token，是正确性兜底非免费加固。
- 2.85× 是 UTF-8 编码 floor，真实 token gap 因 merge 预算偏斜更大；词表扩容收益强烈次线性。
- 与 §r742B（评估顺序把 tokenization 当前提）、§r763B（压缩后用目标 tokenizer 重数）分工：本节补分词器分母机制。
- 豆包自留地 WB 0 落地；按 rules/07「增＝加厚现有」，0 新建 / 0 合并 / 0 删除。
