---
name: multimodal-intelligence
description: >-
  多模态理解能力：让 Agent 能「看懂图片」与「读出文字」。Vision 负责图像语义理解（界面识别、故障图判断、流程图解读、商品图分析），OCR 负责把图片/PDF 中的文字、表格、文档结构化提取。两者分工：Vision 看懂画面意图，OCR 读取其中文字。当用户发来截图/照片/扫描件/带图文档并要求理解内容、识别界面、判断故障、提取文字或表格时使用。触发词：看这张图、截图分析、识别界面、这张图什么意思、读一下这个 PDF、提取表格、图片转文字、扫描件识别、流程图理解、商品图分析、故障截图、OCR、图文理解。不适用：生图/改图（走 ImageGen/buddy-image-processing）、纯代码或纯文本任务（走对应工程技能）。
version: 1.2.0
module: PI
modules: PI
---

# multimodal-intelligence（视觉理解 + 文字识别）

定位：个人 Agent 输入理解层的多模态能力。源自 DeepLearning.AI 学习方向「Vision Intelligence / OCR Intelligence」模块，已并入单一技能以符合「少而精」。

## 一、两条通道分工

| 通道 | 职责 | 不负责 |
|---|---|---|
| **Vision** | 看懂画面：界面布局、按钮/控件、故障现象、流程图、商品外观、空间关系 | 精确读出图中文字 |
| **OCR** | 读出文字：截图文字、扫描 PDF、表格、票据、文档结构化 | 理解画面意图/布局 |

铁律：**Vision 看懂，OCR 读字**。一张含文字的图先过 Vision 理解「这是哪类界面/在干什么」，再用 OCR 提取其中的关键文字与表格，二者结果合并成判断。

## 二、标准流程

```
图片/PDF 输入
  → Vision 分析（这是什么、布局、异常点、流程含义）
  → OCR 提取（文字、表格、字段）
  → 信息融合（用 OCR 文字校准 Vision 的推测）
  → 生成判断 / 方案 / 结构化结果
```

## 三、实践要点

1. **界面识别**：先判应用/窗口类型（设置页、报错框、IDE、网页），再定位关键控件与状态文字（错误码、进度、禁用态）。
2. **故障图判断**：区分「报错信息文字」（走 OCR）与「视觉异常」（红框、空白、错位，走 Vision），二者都要报。
3. **流程图理解**：读到节点与连线后，用文字重述因果/分支，不要只描述「有箭头」。
4. **商品图分析**：抓标题、价格、参数区文字（OCR）+ 外观/卖点（Vision），避免把装饰文字当参数。
5. **OCR 后必须结构化**：表格→二维数组，票据→字段键值，文档→章节摘要；禁止把 OCR 原始长文本整段丢回。
6. **隐私**：截图可能含敏感信息（聊天、账号、单据）；提取后仅用于当前任务，不写入长期记忆，不外发。

## 四、边界

- 不用于「生成图片」或「修改图片」——那是 ImageGen / buddy-image-processing 的职责。
- OCR 对手写、倾斜、低分辨率、复杂排版会失真——失真时显式标注「识别置信度低」，不要编造。
- 中文字体乱码/编码问题优先用纯 UTF-8 通道处理，不在图片里反复猜。

## 五、验收

能对任意一张用户截图给出：① 这是什么界面 ② 关键文字/数据（OCR）③ 有无异常 ④ 建议动作。四项缺一即不合格。


## 六、OCR 评测口径与置信度失效（2026-11-11 r737A 实拉，≥2 独立域一手交叉）

### r737A-1 ★CER/WER 不是「准确率」，无上界且分母与归一化决定数值

CER=(S+I+D)/N 的分母 N 是**参考文本**长度，插入过多时 CER>100%（OCR-D 才报压到 0–100% 的归一化 CER，ourbigbook 逐字「not bounded by one」「Clipping the result or using the longer string as denominator defines a different metric」）；WER 对同一输出通常高于 CER，因为一字错毁整词。⇒ 报 OCR 质量必须附「公式 + 归一化约定 + 计分字符集 + 是否忽略标点/换行」四项，孤立的「准确率 95%」不可跨工具、跨语料比较；限制计分到 a–z/A–Z/0–9 会系统性虚高。

### r737A-2 ★聚合口径与阅读顺序是两个独立陷阱，CER 根本不量版面顺序

跨页汇总有「逐行归一化距离取平均（AttentionHTR 2022）」与「全集合错误求和 ÷ 总参考长度（Bisani & Ney 2004）」两种口径，行长不齐时给出不同数字（ourbigbook 实例：未加权均值 50% vs 合并 0.99%）；Neudecker 2021 调查发现即便「标准化」的 CER/WER 也因历史 Unicode 连字归一化与 reading order 处理差异而跨工具不可直接比；TechnoLynx 逐字「CER alone also misses reading order」。⇒ 同一任务固定一种聚合口径并写进报告；表格 / 多栏 / 边注版面必须另设「文本区域顺序」独立验收，不能拿一个 CER 交差。

### r737A-3 ★引擎置信度不是正确率，误差沿采集→分割→识别链路级联

Tesseract 官方 confidence 在 2021 报纸语料上与 CER 仅微弱相关，不能当人工复核替代品；阈值应按下游用途分档（引用/校勘 <2%、全文检索 5–8%、自动转录 ≤10%、关键词 10–15%），且须拿**置信区间上界**而非点估计卡门槛（「A model whose CER might plausibly be 7% hasn't cleared a 5% bar」）。上游是硬天花板：官方 ≥300 DPI、去斜、二值化（Otsu 在背景不均时失效）、`--psm` 版面假设；「errors introduced at capture generally cannot be fully recovered later」；行分割错误对信息抽取的伤害大于识别错误，且 published CER 多来自人工裁好的干净行 ⇒ 端到端必须在**自动分割行**上重测。失真时先查链路三段再换模型。

**提升层**：PI 输入保真 / AI 验收协议 / PDI 结算台账（按轮）。触发词：CER、WER、编辑距离、归一化 CER、阅读顺序、OCR 置信度、300 DPI、psm、行分割、阈值按用途分档。

### r737A 来源与判非（逐字核验）

- `tesseract-ocr.github.io/tessdoc/ImproveQuality.html`（Tesseract 官方，WebFetch 200 全文逐字）：「Tesseract works best on images which have a DPI of at least 300 dpi」；去斜「The quality of Tesseract's line segmentation reduces significantly if a page is too skewed」；二值化「Tesseract does this internally (Otsu algorithm), but the result can be suboptimal, particularly if the page background is of uneven darkness」，5.0.0 新增 Adaptive Otsu / Sauvola；噪声「Certain types of noise cannot be removed by Tesseract in the binarisation step」；`--psm`「By default Tesseract expects a page of text」，13 种模式逐条列出。**一手官方全文逐字**
- `printerarchive.net/guides/ocr-accuracy`（PrinterArchive Editorial，Last updated 2026-07-06，WebFetch 200 全文逐字）：「CER = (S + I + D) / N」「WER = (S + I + D) / W」；「a single wrong character can invalidate an entire word, so WER is typically higher (worse) than CER」；陷阱逐字「edit-distance metrics treat all errors equally (a mid-word substitution counts the same as a structural line break), Unicode normalization choices vary between tools, and some reported figures are inflated by restricting scoring to a subset of characters」；「Evaluation is not standardized in practice; differing normalization and scoring conventions make cross-study accuracy comparisons unreliable」；13 源透明清单。**独立二手综述（源透明）**
- `technolynx.com/post/validating-trocr-against-legacy-ocr-for-handwritten-manuscripts`（2026-11-01 发布，WebFetch 200 全文逐字）：「CER = (S + D + I) / N」；Neudecker et al. 2021 调查「even 'standardised' CER and WER cannot be compared directly across tools: they handle reading order differently, and they normalise historical Unicode such as decomposed ligatures differently」；「OCR-D reports a normalised CER that stays between 0 and 100%. The raw formula can go above 100% when an engine inserts a lot of text」；两种聚合「averages each line's normalised edit distance (AttentionHTR, 2022)」vs「sums the errors across the whole set and divides by the total reference length (Bisani and Ney, 2004)」；「Tesseract's confidence correlated only slightly with CER」；用途分档 <2% / 5–8% / 10% / 10–15% / 20–30%；「test the upper end of the confidence interval against it, not the point estimate」；「segmentation errors have been shown to hurt information extraction more than recognition errors do」；「CER alone also misses reading order」。**商业立场（CV 服务方）已登记，仅取可迁移判据**
- `zenodo.org/records/6638946/files/varsamisIJCO1-2022.pdf`（IJCO 2022 论文，WebSearch 快照逐字）：式(1)(4)「WER=(iw+sw+dw)/nw」「CER=(ic+sc+dc)/nc」，分母均为参考文本长度；「The word-level error rate is usually higher than the character-level error rate」；另列 cosine/Jaccard/Gestalt ratio 三种非编辑距离相似度。**学术一手交叉（PDF 未全文直取，仅快照公式）**
- `ourbigbook.com/codex/optical-character-recognition`（OCR-D QA 转述，WebSearch 快照）：逐字「character error rate is not bounded by one」「Clipping the result or using the longer string as denominator defines a different metric」；聚合实例「one one-character sample has one error and a hundred-character sample has none. The unweighted mean of their two rates is 50%, while pooling edits and reference lengths gives 1/101≈0.99%」；Unicode code points vs grapheme clusters 影响分母。**独立二手交叉（引 OCR-D 官方 QA）**

- **判非**：窄串词边界全库 SKILL.md：`CER` **0 命中**（此前 20 文件命中经查为 `USER`/`ANSWER` 等子串）；`WER` 唯一命中在 `media/pi-audio`（音频 ASR 词错率，无视觉版面/归一化链路）；`Levenshtein` 唯一命中在豆包自留地 `wb-context-compressor`（typosquatting 近似名，非编辑距离评测）；`reading order` / `psm` / `ground truth 归一化` / `置信区间上界` 全 0 命中 ⇒ 净新。与 `engineering/pi-perception` r732A（服务端降采样/坐标回算/token 计价）分工：那条管「模型实际看到什么分辨率」，本轮管「输出文本质量凭什么可信」。豆包自留地 WB 0 落地。
- **换道/未采纳**：换道：TrOCR/Transkribus 具体 CER 数值与厂商排名（易过时、来自他人语料）不采纳；Transkribus 自家 help centre 与 CER explainer 阈值互相冲突，仅取「按用途分档」这一可迁移判据并登记分歧；econstor PDF 被 Anubis 反爬拦截（本轮 C 方向）如实登记，不冒充一手。B/C 两轮结论一律不复用。

## 七、阅读顺序的独立验收口径（2026-11-14 r744A 实拉，≥3 独立域一手交叉）

> 补 §六 r737A-2 明确点名但当时未给方法的「表格 / 多栏 / 边注版面必须另设文本区域顺序独立验收」。三条各管一层：双轨口径 → 顺序分数的构造与可比性 → 评测协议。

### r744A-1 ★CER 被顺序拉低的成因是「对齐失败」不是「字认错」，故识别与顺序必须双轨记账
OCR-D 官方逐字：「CER (if applied naively by comparing concatenated page-level texts) is **heavily dependent on the reading order** an OCR engine detects. Thus, where text blocks are **rearranged or merged, no suitable text alignment can be made, so CER is very low, even if single characters, words and even lines have been perfectly recognized**」。FCA（→ FCER）用行级最大匹配把两轴解耦：① 两侧文本切行 → ② GT 行按长度降序 → ③ 取最长 GT 行找编辑距离最低/覆盖最高的 OCR 行（可部分匹配）→ ④ 全匹配则双侧出队，部分匹配则切下未匹配片段回列表重排 → ⑤ 迭代 → ⑥ 剩余未匹配行按来源计为插入或删除 → ⑦ 对所有已配对行求 **micro-average CER = FCER**；出处 Clausner/Pletschacher/Antonacopoulos, *Pattern Recognition Letters* 131 (2020) 390–397, p.392。
- 判据：报 OCR 质量固定两栏「字符识别（FCER 或行级 CER）」+「顺序（独立验收）」；只报一个页级 CER 时，版面重排会被误判成识别模型退化，据此换模型/调阈值是修错对象。与 §六 r737A-2 分工：那条立「必须另设」的规矩，本条给可执行的双轨算法。

### r744A-2 ★阅读顺序的验收对象是「区域两两关系」而非一条序列，分数是相对 50% 一致基线的比值
Clausner/Pletschacher/Antonacopoulos 2013 把任意两区域关系分五类：**direct / indirect successor·predecessor、unordered、undefined**；先按 **overlap area** 匹配 GT 与检出区域（**一个 GT 区域可对应多个检出**），再逐对比较关系类型，任何偏差按预定义 **penalty matrix** 计代价，代价同时取决于关系种类与重叠相对大小（官方逐字「Direct opposition is more expensive than indirect」）。示例：GT 为「somewhere after（含 unordered 组）」而检出为「directly before」罚 **10**，GT 为「directly after」则罚 **40**——理由是后者更具体。总误差 e 为全部 GT×检出关系比较之和，归一化到假设 50% 一致的误差 `e50 = pmax * nGT / 2`（pmax=矩阵最高单项罚、nGT=GT 区域数），成功度 `s = 1 / (e * (1/e50) + 1)`（官方公式渲染为 `s=1e∗(1/e50)+1`，此处按语义还原，**原文形式一并留档**）。
- 判据：① 顺序分数不是「排序准确率」，随分数必须报 **pmax / nGT / 矩阵版本**，否则跨文档、跨标注粒度不可比；② 区域匹配允许一对多 ⇒ 先报匹配策略再报分数；③ 官方逐字 mAP「**is not adequate for document layout** for various reasons」（照片场景假设重叠可允许且不冲突 text flow，版面不成立），只可作参考不可作验收门；④ 更完备形态是 Clausner 2011 **Scenario-Driven Performance Evaluation**——不是单一指标，而是统一方法导出的一组 measures 按 **evaluation scenarios** 加权（headline/keyword extraction、linear fulltext、newspaper、figure extraction），且区分 benign deviations（多出空白）与 pathological（断行断词），故「换一个下游用途就要换一套权重」是设计而非缺陷。

### r744A-3 ★评测协议先锁 GT 来源与线性化策略，再用四指标联读分离顺序失败与内容漂移
ACM JCDL 2026《Accessibility Annotations as OCR Ground Truth》四指标互补：CER/WER 量替换·插入·删除，**Kendall τ** 只在 hypothesis/reference 已匹配词的位置上算「纯顺序一致性」，**LCS ratio** 把顺序与长度耦合（罚漏与伪内容）。官方逐字：「high τ with low CER indicates a clean transcription, **high τ with high CER indicates content drift under correct order, and low τ indicates a genuine reading-order failure**」。协议三处硬约束：① GT 顺序来自无障碍标注的 OOXML 文档序——「a screen reader consumes the document strictly in sequence … **no spatial inference is required** to recover it」；② 各系统输出一律取**默认预测顺序**，「**no coordinate re-sorting or post-hoc linearization**」——按坐标重排再算 τ 等于把要验的能力本身做掉；③ 报 **per-image medians** 而非均值，近空白/图主导页的短参考会放大归一化误差。Table 4 实证范围：Qwen3-VL 0.102/0.170/**0.996**/0.852、Tesseract 0.112/0.263/**0.994**/0.845、LayoutReader 0.734/0.931/**0.460**/0.315（CER/WER/τ/LCS）。
- 判据：顺序验收表固定四栏并写 GT 来源 + 是否允许后处理线性化；第三域 OmniDocBench V1.5 / *Unlimited OCR Works* 把 **Reading-order Edit Distance** 与 Text Edit / Formula CDM / Table TEDS **分列**，而端到端 overall 是 text+formula+table 加权平均 ⇒ **总分高不代表阅读顺序合格**，须单独卡线。数值仅作量级参照，不搬作本机结论。

**提升层**：PI 输入保真 / VI 验收协议 / 工作流（文档解析验收表）。触发词：reading order evaluation、FCA/FCER、penalty matrix、e50、success measure s、Clausner、unordered、direct successor、Kendall τ、LCS ratio、no post-hoc linearization、per-image median、Read-order Edit、scenario-driven evaluation、mAP 不适用于版面。

### r744A 来源与判非（逐字核验）
- `https://ocr-d.de/en/spec/ocrd_eval`（OCR-D 官方规范，2026-11-14 WebFetch **200 全文逐字**）：FCA 七步算法、Reading Order Evaluation 五类关系 / penalty matrix / 10 vs 40 / `e50=pmax∗nGT/2` / `s=1e∗(1/e50)+1`、mAP「not adequate for document layout」、Scenario-Driven 段；并给出 CER 定义、Bag of Words、P-R 曲线与全部参考文献（含 `primaresearch.org/.../ICDAR2013_Clausner_ReadingOrder.pdf`、`PRL_Clausner_FlexibleCharacterAccuracy.pdf`）。**一手官方全文**。
- `https://dl.acm.org/doi/10.1145/3805696.3846504` + `https://dlnext.acm.org/doi/10.1145/3805696.3846504` 同 DOI（ACM JCDL 2026 论文，**WebSearch 快照逐字**）：四指标定义、失败模式三分、「no coordinate re-sorting or post-hoc linearization」、screen-reader 顺序 GT、per-image medians、Table 4 六系统数值、200 DPI / 191 页 / H200 设置。**dlnext WebFetch 仅返回 Basic Edition 订阅页，正文未全文直取，如实登记，不冒充一手全文**。
- `https://arxiv.org/pdf/2606.23050`（*Unlimited OCR Works*）+ `https://baike.baidu.com/item/OmniDocBench%20V1.5`（**WebSearch 快照逐字**）：OmniDocBench 四类专用指标（Text Edit / Formula CDM / Table TEDS·TEDS-S / **Reading Order Edit Distance**）、overall 为 text+formula+table 加权平均；V1.5 标注阅读顺序与 Block 从属关系、19 种布局类别、200 DPI。**独立第三域交叉（数值不采信为结论）**。
- **判非**：窄串全库 `SKILL.md`：`FCA` / `FCER` / `penalty matrix` / `e50` / `success measure` / `Clausner` / `OmniDocBench` / `TEDS` / `direct successor` / `unordered` **全 0 命中**；`reading order` 唯一命中在**本技能 §六 r737A-2**（点名缺口未给方法，本轮补齐、不重述结论）；`Kendall` 唯一命中在 `engineering/wb-artifact-verification` r567B（评分格式过滤器中「τ_b 折扣平局」，异命题）。豆包自留地 `wb-execute-discipline` / `wb-context-compressor` **WB 0 落地**。B/C 两轮结论一律不复用。
