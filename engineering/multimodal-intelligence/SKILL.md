---
name: multimodal-intelligence
description: >-
  多模态理解：让 Agent「看懂图片」「读出文字」。生成质量FID可比性陷阱（有限样本协方差使FID随样本量偏高近似1/n·2048维放大/只同样本数同网络同预处理可比·只匹配均值协方差丢多模态结构·保真度与多样性需precision-recall拆开·不读prompt无法评文图匹配）；Vision 管画面语义（界面/故障图/流程图/商品图），OCR 管图片/PDF 文字表格结构化提取：前者看懂意图，后者读取文字。当用户发来截图/照片/扫描件/带图文档并要求理解内容、识别界面、判断故障、提取文字或表格时使用。触发词：看这张图、截图分析、识别界面、读一下这个 PDF、提取表格、图片转文字、扫描件识别、流程图理解、故障截图、OCR、图文理解。不适用：生图/改图（走 ImageGen）、纯代码或纯文本任务。色彩管线与色差口径：sRGB线性光·ICC渲染意图与D50 PCS·ΔE公式版本四元验收。；主观评测协议（六项控制/MOS+95%CI/ACR·DSIS·DSCQS·ACR-HR选型/观察者筛选）。；生成式描述评测（SPICE 场景图语义命题 F-score/n-gram 重叠既不必要也不充分/系统级相关 0.88 与句子级 τ 0.45 两口径必须分开报/参考数改变绝对分）。；目标检测与分割评测（IoU定TP/FP/FN·COCO mAP=12指标10阈值平均·Dice=像素F1与IoU单调等价·mIoU与PixelAccuracy分报·mask/box同协议只换IoU算法）。；非视觉捷径与语言先验（VQA 盲模型靠问题文本「闭眼答对」/VQA v2 互补图配对逼模型用视觉/VQA-CP 答案分布偏移打回原形/无图像基线当主实验变量测视觉依赖/开放题归一化与多标注投票）。；文图对齐组合式验收（CLIPScore 词袋化混淆主谓颠倒/VQAScore 用 P(Yes)/GenEval 目标检测实例级计数位置属性绑定·六类分报/GenAI-Bench 1600 组合提示+15000 人评/位置墙与属性绑定是短板）。；物体幻觉评测（CHAIR-I/S 受提示措辞影响可翻倍·POPE 轮询式 yes/no 三负采样 Random·Popular·Adversarial·正负1:1·Yes率偏置·提示鲁棒性std·只测物体存在不测属性数量位置）。
version: 2.5.0
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

## 八、参考可用度分层与感知质量指标选型（PI · r750B 2026-11-15 实拉，3 独点）

> 与 §六 CER/WER 文本层评测、§七 阅读顺序独立验收分工：那两节评「内容对不对 / 顺序对不对」，本节评**「画面好不好」这一整族的分数在什么前提下才有意义**。三独立域一手交叉：Fora Soft《Full-, Reduced-, No-Reference Video Quality Metrics》（2026-06-22）WebFetch 200 全文 + Netflix `vmaf` 官方 README（github raw 200 全文）+ Springer《A survey on facial image deblurring》§6.1–6.3 + 自动化学报中文核心 + FFmpeg filters 官方文档（仅目录，如实登记）。

### 8.1 指标选型第一问不是精度，是「手上还有多少参考」
- Fora Soft 逐字：「**Before you can pick a video quality metric, you have to answer one question: how much of the pristine original do you still have at the point where you want to measure?**」→ 三族是**三种不同的工作**，不是同一把尺的三档精度：**FR**（full-reference，PSNR / SSIM / MS-SSIM / VMAF，需完整母版）· **RR**（reduced-reference，ITU-T J.246 / J.249，仅需特征指纹但需旁信道）· **NR / blind**（NIQE / BRISQUE / NR-VMAF / ITU-T P.1203 / P.1204.3，无母版）。
- 逐字：「**PSNR, SSIM, and VMAF are all full-reference and are useless on a live stream that has no original**」；「**a full-reference score where there was no master is meaningless, not low**」。RR 因「most companies are not able to connect the measurement point with the originating video supply」实际几乎不部署，NTIA 自述所有现行低带宽模型实现都跑在 FR 模式且**已停止 RR 研究**。NR 是直播 / 视频通话 / 监控 / UGC 的「**the only option**」，同时「**the hardest to trust**」——只可作趋势与告警信号，不可当 ground truth，且禁止跨差异很大的内容 / 设备比较 NR 分数。
- 判据：报质量分先写「参考族 + 母版是否在场 + 是否同场景」。无母版却给 VMAF 分 = 无效测量，不是低分；生产侧只有 NR 时须在结论里标注「趋势信号」。与 §六「报 CER 必附公式/归一化/字符集」同构，本条把「参考」列为质量分数的第一必填项。

### 8.2 FR 分数有前置的三重对齐，未对齐不是低分而是坏分
- Fora Soft 逐字：「**A full-reference metric assumes the two videos are aligned: the same frame in each, at the same resolution, with the same brightness scaling**」；错 2 帧（f100 vs f098）即报「quality collapse that the eye would never see」，1 像素空间偏移或小亮度增益同理；结论逐字「**a full-reference number is only valid once the two videos are aligned. An unaligned full-reference measurement is not a low score, it is a broken one**」。
- 官方口径：NTIA（VQM → ITU-T J.144）警告 PSNR「**is very sensitive to calibration errors**」；ITU-T **J.340** 专设 exhaustive-search PSNR，先穷举找最佳空间偏移 / 时间偏移 / 亮度增益再计分。图注逐字：alignment means「same frame, same pixels, same brightness」。
- 判据：任何 FR 数字必须随附「帧对齐 / 分辨率 / 像素格式 / 亮度标定」四项校验结果；抽帧比对、缩放后比对、转码前后比对若未做对齐先修管线再报数。本仓 `media/rg-ffmpeg-tools` 侧执行时把对齐检查放在计分之前，不把「分数掉了」直接解释成质量退化。

### 8.3 像素误差 ≠ 感知质量，且「读像素 / 读码流」是第二根独立轴
- 多域逐字：Springer 综述「**the numerical results of PSNR are often inconsistent with the subjective perception of human vision. Using the PSNR metric tends to lead to oversmoothed results**」；「**Images with lower SSIM values may also have a good visual experience**」；自动化学报「PSNR 在捕捉感知差异方面存在着一定的局限性，因此 PSNR 值并不与人类的主观感知质量密切相关」。LPIPS 走预训练网络深层特征距离（`d(x,x0)=Σ_l (1/H_lW_l) Σ_hw ||w_l ⊙ (ŷ^l_hw − ŷ^l_0hw)||²₂`），NIQE / BRISQUE / PIQE 走自然场景统计，方向各不同（LPIPS/NIQE 越小越好，SSIM/PSNR 越大越好）。
- Netflix 官方 README 逐字：VMAF 是「**an Emmy-winning perceptual video quality assessment algorithm developed by Netflix**」，`libvmaf` 同包内含 **PSNR, PSNR-HVS, SSIM, MS-SSIM and CIEDE2000**；模型分代明确（2026-06 发布 **v1** 新模型、v0 仍留存、2026-10-26 发布 VMAF-v1 的 **HDR 版**），并有 **NEG (No Enhancement Gain) mode** 专用于 codec 评测 ⇒ 同一段视频跨模型版本 / 跨 NEG 开关的分数不可直接比。
- 第二根轴逐字：FR/RR/NR 是「有多少参考」，另有一根「**what the metric reads**: the decoded pixels, or the encoded bitstream」—— ITU-T **P.1204.3** 码流 NR、**P.1204.4** 像素 FR/RR、**P.1204.5** 混合 NR；「**no-reference does not mean low-tech**」。生成式 / 多解任务下 SSIM 与 LPIPS 这类成对指标也受限（OpenEnvision 逐字「SSIM assumes a meaningful paired reference and can be less appropriate when many visually valid outputs are possible」「PSNR ... often correlates poorly with human perceptual quality on generative tasks」）。
- 判据：验收固定四栏 —— **指标名 + 参考族(FR/RR/NR) + 对齐状态 + 模型版本/读的是像素还是码流**；单一数字不得当质量结论。与 §七「CER 与顺序双栏」同属「一分数不足以承载多维质量」的结构，但对象从文本转到画面，不复用结论。

### r750B 来源与判非（2026-11-15 实拉，逐字核验）
- `https://www.forasoft.com/learn/video-quality/articles-vqm/full-reduced-no-reference-metrics`（Fora Soft Learn，Nikolay Sapunov，**Published 2026-06-22**）— **WebFetch 200 全文逐字**：FR/RR/NR 三族定义、Figure 1 三卡、「a full-reference score where there was no master is meaningless, not low」、对齐三重前提与 Figure 2 错 2 帧、NTIA「very sensitive to calibration errors」、ITU-T J.340 exhaustive-search PSNR、RR 旁信道困境与 NTIA 停止 RR 研究、NR 三风格（NSS / learned / bitstream-parametric）、「the only option」「hardest to trust」「Accuracy falls as reference information falls」、P.1204.3/4/5 三模型与第二轴。**第一独立域（工程实务一手全文）**。
- `https://raw.githubusercontent.com/Netflix/vmaf/master/README.md`（Netflix 官方仓库 README）— **WebFetch 200 全文逐字**：「Emmy-winning perceptual video quality assessment algorithm」、`libvmaf` 内含 PSNR / PSNR-HVS / SSIM / MS-SSIM / CIEDE2000、2026-06 VMAF v1 与 v0 并存、2026-10-26 HDR-VMAF-v1、NEG mode（2020-07-13 memo）、FFmpeg `--enable-libvmaf`、BSD+Patent 许可。**第二独立域（指标作者官方一手）**。
- `https://link.springer.com/content/pdf/10.1007/s41095-023-0336-6.pdf`（Springer《A survey on facial image deblurring》§6.1–6.3）— **WebSearch 快照逐字**：PSNR 与主观不一致 / oversmoothed、SSIM 亮度对比度结构三项、低 SSIM 也可能视觉好、LPIPS 深特征式 (11)、NIQE MVG 式 (12)、IFC/PIQE/NRQM。**第三独立域（同行评审综述，作交叉）**。
- `https://aas.net.cn/article/doi/10.16383/j.aas.c240235`（《自动化学报》《基于深度学习的视频超分辨率重建算法进展》）— WebSearch 快照逐字：PSNR 局限、SSIM 式 (9)、LPIPS 式 (10) 与 VGG 特征、DepictQA 语言化质量感知。**中文核心期刊交叉域**。
- `https://openenvision.org/WorldFoundry/docs/evaluation/metrics/perceptual` + `https://sciencedirect.com/topics/computer-science/spatial-quality`（指标计算契约 / 教材）— WebSearch 快照逐字：LPIPS/SSIM/MS-SSIM/PSNR 定义式、PSNR 生成任务弱相关、多解时 SSIM 不适用、IFC / NIQE / PIQE 口径。**教学与工具立场登记，不作唯一结论来源**。
- `https://ffmpeg.org/ffmpeg-filters.html`（FFmpeg 官方 filters 文档）— **WebFetch 仅返回前 15,000 / 99,996 字目录**，psnr / ssim / libvmaf 正文未取到，**如实登记、不引用其正文**；仅用于确认该文档存在这三节。
- **判非**：窄串全库 `SKILL.md` 精确扫描 — `全参考` / `无参考` / `reduced-reference` / `VMAF` / `LPIPS` / `PSNR` / `NIQE` / `BRISQUE` / `J.340` / `P.1204` / `exhaustive-search PSNR` / `校准误差` **全 0 命中**；`SSIM` 唯一命中在 `media/wb-media-forensics` §68（视频抽帧用 SSIM 感知差异捕捉关键帧，是采样触发器而非质量分数），与本轮「参考族 + 对齐 + 感知失配」命题不同，登记不复用；`coherent` / `reconcil` 命中在执行与治理技能为异命题。与 §六 CER/WER、§七 阅读顺序两族结论不复用。豆包自留地 `wb-execute-discipline` / `wb-context-compressor` **WB 0 落地**。A / C 两轮结论一律不复用。
- **未采纳**：VMAF 各 elementary metric（VIF / DLM / MAD）的权重与训练细节、ITU-T P.1204 各模型相关系数、DepictQA 多模态语言质量描述整段、NR-VMAF 卷积网络结构 —— 属实现与 benchmark 数值，非可迁移判据。

## 九、色彩管线与色差口径：解码链、渲染意图与 ΔE 四元验收（2026-11-15 r754B 实拉，3 独点）

> 分工：§八 管「有多少参考（FR/RR/NR）+ 对齐 + 指标版本」，本节管「这些数值是从哪条解码链与哪套色差口径读出来的」。两节是输入面与计分面，不复用结论。

### 9.1 RGB 数不是颜色：色彩空间 + 传递函数 + 白点才定义感知输入
- W3C CSS Color 4（CRD 2026-11-12）逐字给出 sRGB 解码：`if (abs <= 0.04045) { cl = c / 12.92; } else { cl = sign * (Math.pow((abs + 0.055) / 1.055, 2.4)); }`，并明写「**c is the gamma-encoded red, green or blue component. cl is the corresponding linear-light component**」；同页「**Most RGB spaces are not additive, because the components are gamma encoded. Undoing this gamma encoding produces linear-light values**」。
- 同一个颜色逐字对应五组不同数值：`color(sRGB 0.41587 0.503670 0.36664)` / `color(display-p3 0.43313 0.50108 0.37950)` / `color(a98-rgb 0.44091 0.49971 0.37408)` / `color(prophoto-rgb 0.36589 0.41717 0.31333)` / `color(rec2020 0.47428 0.52316 0.41425)` ⇒ 脱离色彩空间谈 RGB 三元组没有感知含义。
- **判据**：报「模型看到的颜色 / 两图色差 / 色调统计」先写三元组（空间 + 传递函数 + 白点）；均值、插值、alpha 合成、缩放、差分等运算必须在 **linear-light** 上做，直接在 gamma 编码值上算会系统性偏差（编码空间非线性光，混色预测不成立）。与 §8.2「FR 三重对齐」并列为两个前置校验：一个查帧/分辨率/亮度，一个查解码链。

### 9.2 白点与渲染意图决定「转换后还算不算同一个颜色」，往返不是无损
- W3C 逐字：「**To avoid cumulative round-trip errors, it is important that the identical chromaticity values are used consistently, at all places in a calculation**」；D65 是「**6500 Kelvin (actually 6504, because the value of Plank's constant has changed since the color was originally defined)**」；规范摘要明写它规定「**how colors are interpolated, and how to gamut map colors**」。
- ICC.1:2004-04 §0.3 逐字：「**four rendering intents (colour rendering styles) are defined ... Each one represents a different colour reproduction compromise**」；media-relative 把介质白归一到 PCS `L*a*b* = (100,0,0)` 且「**this procedure inevitably introduces some change in all colours in the reproduction**」；「**When an exact colour match is required for all within gamut colours the absolute colorimetric rendering intent will define this**」；「**The colour rendering of the perceptual and saturation rendering intents is vendor specific**」。ICC.2:2018 §7.2.17 给四意图编码值（0/1/2/3），§7.2.18 给 PCS 照明体 D50 = `X 0,964 2 / Y 1,0 / Z 0,824 9`。ICC 官方讲义逐字：「**The ICC PCS is D50 and if the source or destination colorimetry is not D50, it must be transformed to D50 using a chromatic adaptation transform**」；官方幻灯片对复杂 RGB/CMYK profile 明确标「**Non-invertible profile**」。
- **判据**：跨设备 / 跨格式转换若声称「颜色一致」，必须写 ① PCS 白点（D50）与源白点（常见 D65） ② 是否做色适应变换 ③ 渲染意图 ④ 有无 profile。media-relative 会改动域内**全部**颜色，只有 absolute 对域内精确匹配；perceptual/saturation 由厂商自定、不可跨实现比较；gamut mapping 是压缩妥协、复杂设备 profile 不可逆 ⇒ 往返测试不能当无损证据，跨管线累积误差要单列。

### 9.3 ΔE 是「公式版本 + 参数因子 + 观察条件 + 用途」四元函数，不是色差单值
- 二手逐字（厂商 / 检测机构 / 实现片段，均登记立场）：`ΔE*ab = √[(ΔL*)²+(Δa*)²+(Δb*)²]` 是 Lab 欧氏距离，「**在明度差、彩度与色相差视觉偏差**」上不均匀、饱和蓝区尤甚；CIE94 / CMC(l:c) 引入 `S_L/S_C/S_H` 与参数因子 `k_L,k_C,k_H`（参考条件全 1；纺织常 `k_L=2`、印刷推荐 `k_L=1.4`；CMC 可觉察取 `l=c=1`、可接受取 `l=2,c=1`）；CIEDE2000 增 `R_T` 旋转项「**校正颜色空间中蓝色区域容差椭圆主轴方向的偏转**」并改进低彩度区，官方表述是「**重新定义了色差计算方法**」而不是新建颜色空间；目视比较（D65/D50/TL84 标准光源箱 + 培训观察者）仍是验证仪器结果是否符合人类感知的基准。
- **判据**：报色差固定五栏 —— **公式名 + 参数因子（kL/kC/kH 或 l:c）+ 照明/观察条件 + 用途（可觉察 vs 可接受）+ 样本来源**。同一对颜色跨公式数值不同，阈值不可跨版本抄；ΔE 是模型不是主观实验，「ΔE 小」不等于「感知一致」。与 §8.3 关系：那里只把 `CIEDE2000` 列为 libvmaf 内含 elementary metric 的名字，本节给它口径，不重述 VMAF 分代结论。
- **诚实边界**：ΔE 公式族与行业参数逐字来自中文厂商/检测机构站与实现片段（**二手**）；未取得 CIE / Sharma 官方实现备注全文（域名解析失败，见来源节），故本节只取「版本 / 参数 / 条件 / 用途」这一可迁移**结构**，具体行业 `k_L` 取值标注待官方核验、不移植为通用事实。

### r754B 来源与判非（2026-11-15 实拉，逐字核验）
- `https://www.w3.org/TR/css-color-4/`（W3C **CSS Color Module Level 4, Candidate Recommendation Draft, 2026-11-12**）— **curl 200 / 1,252,283B 全文逐字**（WebFetch 两次 AI 摘要 60s 超时仅返回前 15,000 / 99,782 字，改 curl 去标签得 332,213 字全文）：sRGB 传递函数 `0.04045 / 12.92 / 0.055 / 1.055 / 2.4` 与「gamma-encoded / linear-light」、「Most RGB spaces are not additive」、同一颜色五空间数值、D65 6504K 与「cumulative round-trip errors」、additive color space / white point / chromaticity 定义、gamut map 摘要。**第一独立域（标准组织一手全文）**。
- `https://www.color.org/ICC1V42old.pdf`（ICC.1:2004-04 §0.3）+ `https://www.color.org/specification/ICC.2-2018.pdf`（§7.2.17 / §7.2.18）+ `https://www.color.org/events/medical/Green.pdf`（ICC 官方讲义）+ `https://archive.color.org/files/slidepres2003.pdf`（ICC 教程）— **WebSearch 逐字快照**：四意图定义与「different colour reproduction compromise」、media-relative「inevitably introduces some change in all colours」、absolute 域内精确匹配、perceptual/saturation「vendor specific」、PCS 照明体 D50 三值、色适应变换必须、参考介质与 P2 观察条件、`Non-invertible profile`。**如实登记**：`https://www.color.org/` 首页 curl 200 / 29,415B 但为门户导航（无规范条文）；四份 PDF 未逐页下载，按快照取证、不冒充 PDF 全文。**第二独立域（标准组织官方规范，多份互证）**。
- `https://www.nhnhnh.com/baike/1444.html`（三恩时）+ `http://www.mobccs.cn/news/575.html`（MOBCCS）+ `https://a.bjhgyjs.cn/xiangmu/cl/468131.html`（中析检测）+ `https://itohi.com/snippets/colors/color-difference`（实现片段）— **WebSearch 快照逐字（二手）**：ΔE76 / CMC(l:c) / CIE94 / CIEDE2000 四式、`S_L/S_C/S_H` 与 `k_L/k_C/k_H`、`R_T` 蓝色区旋转项、可觉察 vs 可接受、目视比较基准、公式实现权重 `S_C=1+0.045C*`、`S_H=1+0.015C*`。**第三~六独立域（厂商/检测机构/实现，二手立场逐条登记）**。
- **失败登记**：`http://www2.ece.rochester.edu/~gsharma/ciede2000/`（Sharma 等 CIEDE2000 官方实现备注与测试数据）**curl 000 / `Could not resolve host`、WebFetch `fetch failed`**；`https://colour.readthedocs.io/en/develop/manual/color_difference.html` 与 `https://www.color.org/renderingintent.html` **WebFetch 404**；`https://www.color.org/renderingintent.html` 另由 `site:color.org` 检索定位到规范 PDF 才取得条文。以上均如实登记、**不引用其正文**。
- **判非**：窄串全库 `SKILL.md` 精确扫描 —— `linear-light` / `gamma encoded` / `rendering intent` / `chromatic adaptation` / `ΔE` / `色适应` / `色彩空间` / `白点` / `色域映射` **全 0 命中**；`CIEDE2000` 2 命中在本技能 §8.3 与 r750B 来源节（Netflix libvmaf **内含指标清单**，仅列名未给口径），本轮按「**优＝加厚现有**」补色差口径，不重述 VMAF v0/v1/HDR/NEG 分代结论；与 §六 CER/WER、§七 阅读顺序、§八 FR/RR/NR 三族结论均不复用。豆包自留地 **WB 0 落地**。A / C 两轮结论一律不复用。
- **未采纳**：CSS gamut mapping 的 OKLCH chroma reduction 具体算法与 δEOK 阈值（正文未取到）、ICC 参考介质 89% 反射率 / 500 lux / 20% surround 数值、ΔE2000 完整公式与测试数据集、各厂商 ΔE 合格阈值表 —— 属实现数值或未核验二手，不迁移为通用判据。

## 十、主观评测是客观质量指标的真值来源：六项控制、MOS 置信区间与方法选型（r758B · 2026-11-16 实拉）

> 与 §八分工：§八讲 FR/RR/NR 客观指标**按参考可用度选型**与对齐前置；本节讲这些客观分数**凭什么算对**——它们都是对主观面板的预测，真值来自受控的主观测试。VMAF 本身就是「训练在主观分上的融合指标」（§8.3），故本节是它的验收前置，不重述分代结论。

### 10.1 客观指标只是对面板的预测；六项控制缺一，结果就「不是测量」
- Fora Soft《Why Subjective Testing Is the Ground Truth for Video》逐字：「**every objective video-quality metric — PSNR, SSIM, VMAF — is a machine's prediction of what humans would say**」；「**when a properly run panel and a metric disagree, the panel wins**」；「**Six things turn a show of hands into a measurement, and international standards specify each one**」；「**Miss any one of these and the result stops being a measurement**」。
- 六项控制（逐字要点）：① **the right viewers** —— naive 非专家，「**Your encoding team is the worst possible panel: they know what to look for, they know which encode is the new one, and they want it to win**」，P.910 §10 要求筛 normal vision；② **enough of them** —— 可用区间约 4–40 人、稳定下限约 15；③ **controlled environment** —— 观看距离/显示标定/房间照明由 BT.500-15 固定，「**so that a score means the same thing from one session to the next**」；④ **defined method and scale** —— 固定呈现流程 + 带标签量表（5 点 ACR 或损伤量表）；⑤ **randomization** —— 「**the order of clips is shuffled per viewer so that fatigue and learning do not pile onto whichever encode happened to go last**」；⑥ **screening and statistics** —— 剔除内部不一致的观察者 + 每个 MOS 带置信区间。
- 假测试逐字：「**"I showed it to the team and they liked it." ... fails at least four of the six controls at once — expert viewers instead of naive ones, far too few of them, no controlled environment, and no scale or statistics**」；「**It is fine as a smoke test for "is anything obviously broken." It is worthless as evidence that encode B is better than encode A**」。
- **判据**：报「B 的 VMAF/PSNR 更高所以更好」时，必须能回答它对照的真值面板是否满足六项；团队内部看图只配当 smoke test，不能写成 A/B 优劣证据。与 §8.2「未对齐的 FR 测量是坏分不是低分」互补：那条查管线，本条查真值来源的合格性。

### 10.2 MOS 差必须带 95% CI；精度按 1/√N 缩放，ΔSCI 给出「多少人能分辨多小的差」
- 逐字公式（ITU-R BT.500 口径）：`ε = 1.96 × ( S / √N )`。Worked example：A `3.40` / B `3.80` / `S=0.90` / `N=24` → `ε=0.36`，A `[3.04, 3.76]`、B `[3.44, 4.16]`；同样条件 `N=5` → `ε=0.79`、两区间几乎全重叠 → 「**the honest conclusion from five viewers is we cannot tell A and B apart**」；且小样本应换 Student's t≈2.78 → ±1.12「**dissolves the comparison entirely**」。逐字结论：「**a confidence interval scales with 1/√N, so shrinking the panel widens the uncertainty until two truly different encodes become statistically indistinguishable**」。
- 一处易读反的逐字澄清：「**overlapping confidence intervals do not by themselves prove the encodes are equal**」；同一批观察者应改配对检验，「**compares each viewer's two scores and cancels their personal harshness**」，比看两区间重叠敏感得多。
- ITU-T P.910 (10/2023) 官方 §8.1 逐字：「**Let the subjective test's confidence interval (ΔSCI) be defined as the minimum difference in mean opinion score (MOS) values where 95 per cent of stimuli pairs are statistically different (according to the Student's t-test using a 95 per cent confidence level)**」；「**the ACR method rarely yields ΔSCI below the following values: 0.5 for 24 subjects, 0.7 for 15 subjects, 1.1 for 9 subjects, and 1.5 for 6 subjects**」；「**The size of the confidence interval depends on the post subject screening method**」。
- **判据**：报 MOS 固定五栏 —— 均值 + N + S(或方差) + 95% CI + 观察者筛选规则（含筛前/筛后人数）。两 MOS 差小于该人数下的 ΔSCI 就不得写「B 更好」：想分辨 0.4 需 24 人级面板，5 人在结构上判不出来。「区间重叠」≠「相等」，同批评委改配对检验；CI 大小还依赖筛选方法，不给筛选规则的 CI 不可复核。

### 10.3 方法按损伤量级与吞吐选型；参考位置带偏置，观察次序要在分析时消除
- 四方法选型（Fora Soft 主观测试设计 checklist 逐字表）：**DSCQS**「Ref + Imp, random order, replay」~41s，「Near-transparent codec comparisons」；**DSIS**「Ref first, Imp second, no replay」~20s，「Large impairments, transmission errors」；**ACR**「Single stimulus, no reference」~12s，「High-throughput multimedia studies」；**ACR-HR**「ACR + hidden reference in pool」~13s，「Production ladders, codec selection」。样本量：lab 控制环境 15 最低 / 24 标准（BT.500-14、P.910 2023）；众包 60 最低 / 100 标准（P.808 2021 adapted）。
- ITU-T P.910 官方逐字：**DCR（=BT.500 的 DSIS）5 点损伤量表**「5 Imperceptible / 4 Perceptible but not annoying / 3 Slightly annoying / 2 Annoying / 1 Very annoying」；「**DCR ratings are minimally influenced by a subject's opinion of the content ... Thus, DCR is able to detect colour impairments and skipping errors that the ACR method may miss**」；「**DCR ratings may contain a slight bias. This occurs because the reference always appears first, and people know that the first stimulus is the reference**」；**CCR 7 点比较量表** −3..+3 且「**During data analysis, the randomized order of presentation must be removed**」。
- 四陷阱逐字：「**Comparing MOS across two studies that were not cross-calibrated with a shared anchor**」；「**Using ACR at near-transparent quality; switch to DSCQS / DSIS for small impairments**」；「**Treating MOS as a true interval scale; the gaps between labels are not equal**」（ACR 标签不等距，偏态时改报中位数）；「**Skipping outlier screening; one bad viewer can swing MOS by 0.3-0.5 points**」（规则：BT.500 kurtosis 或 P.910 LPCC）。12 步预检还要求每位观察者 4–6 段 anchor 训练、单场 <60min、随机化不得把同一条件聚在一起。
- **判据**：验收表写四项 —— 方法名 + 损伤量级匹配 + 是否隐藏参考 + 筛查规则；近透明质量用 ACR 会把小损伤判成无差别；跨研究比 MOS 必须有共享 anchor 交叉校准；MOS 不是真区间尺度，别做「提升 0.4 分＝提升 8%」这类换算；报分同时报筛前/筛后人数。与 §七 阅读顺序验收分工：那条管 OCR 版面顺序，本节管主观真值的统计与流程合格性。

### r758B 来源与判非（2026-11-16 实拉，逐字核验）
- `https://www.itu.int/epublications/ru/publication/itu-t-p-910-2023-10-subjective-video-quality-assessment-methods-for-multimedia-applications/en`（**ITU-T P.910 (10/2023) 官方全文页**）— **WebFetch 200，AI 摘要 60s 超时返回前 15,000 / 99,561 字原文逐字**：版本表（7.0 2026-07-29 / 6.0 2023-10-29 …）、ACR/DCR/CCR 定义、DCR 5 点量表与偏置段、CCR 7 点量表与「randomized order must be removed」；ΔSCI 定义与 0.5/0.7/1.1/1.5 四个数值、「The size of the confidence interval depends on the post subject screening method」由官方页 §8.1 同批 WebSearch 逐字快照交叉核验。**第一独立域（标准组织官方一手全文）**。
- `https://www.forasoft.com/learn/video-quality/articles-vqm/why-subjective-testing-is-ground-truth`（Fora Soft 2026-06-23，Nikolay Sapunov）— **WebFetch 200 全文逐字**：六项控制全文、假测试段、`ε=1.96×(S/√N)` 与 A/B 两组 worked numbers、1/√N 结论、t≈2.78、区间重叠澄清与配对检验、References 列出 P.910 / BT.500-15 / P.808 三份 Tier 1 标准。**第二独立域（工程厂商方法论长文，逐条对照官方条文）**。
- `https://cdn.prod.website-files.com/64e8910adc5a63966a68acea/.../subjective-test-design-checklist.pdf`（Fora Soft 主观测试设计 checklist，配套 article 6.2）— **curl 200 / 3,983B → pypdf 1 页 / 2,454 字全文逐字**：四方法选型表、三档样本量、12 步预检、四陷阱、BT.500 kurtosis / P.910 LPCC 筛查规则。**第三域（同厂商配套清单，一手 PDF，与上条同立场，按二手转述登记不作唯一结论来源）**。
- `https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.500-13-201201-S!!TOC-HTM-E.htm`（**ITU-R BT.500-13 官方目录**）— **WebSearch 逐字快照**：§2.1 观看条件（实验室/家庭/监视器分辨率与对比度）、§2.4 条件范围与锚定、§2.5 Observers、§4 DSIS、§5 DSCQS、§6 单刺激/刺激比较/SSCQE/SDSCE、Annex 2 §2.2 置信区间计算、§2.3 观察者筛选（区分 DSIS/DSCQS 与 SSCQE）。**第四独立域（标准组织官方目录，版本 2012；现行 BT.500-15 (05/2023) 由 P.910 参考表与 Fora Soft References 双域佐证，如实登记版本差）**。
- **判非**：窄串全库 `SKILL.md` 精确扫描 —— `BT.500` / `DSIS` / `SAMVIQ` / `观看条件` / `平均意见分` / `绝对类别评级` / `DSCQS` / `ACR-HR` / `ΔSCI` **全 0 命中**；`ACR` 2 命中经查为 `writing/supply-chain-thesis-master`（智能仓储「ACR/CTU 料箱机器人」，异命题）与误抓子串；`MOS` 5 命中经查为 `wb-agent-evaluation`（MOSAIC-3M 数据集名）、`win-native-app-automation`（SetWindowPos 片段）等**子串误抓/异命题**；`主观评测` 1 命中在 `engineering/wb-execute-discipline`（自纠错在「主观评测任务」信息增益为负，异命题）；`observer` 1 命中在 `wb-debug-loop`（隔离 observer，异命题）。按 rules/07 四态判「**优＝加厚现有 `engineering/multimodal-intelligence`**」，不新建并行层。PI 模块记忆 §8（FR/RR/NR 与对齐）、§9（色彩/ΔE）结论**一律不复用**；豆包自留地 **WB 0 落地**。与 r757/r756/r755 九模块结论不复用；A / C 两轮结论亦不复用。
- **未采纳**：BT.500 Annex 2 逻辑函数拟合目标模型的具体参数、P.1401 客观模型资格评定流程、P.1203/P.1204 参数模型公式、crowdsourcing gold/trapping 题库设计、SAMVIQ 完整实现、各版本 5 点/9 点量表逐条差异 —— 属标准实现细节与工程配置，不迁移为通用判据。

## 十一、生成式描述的评测：语义命题 F-score 与「系统级 / 句子级」两口径（r762B · 2026-11-18 实拉）

> 与 §六～§八分工：那些章节评「识别/画质」这类有确定参考的问题；本节评「图像描述生成」这类**一个图有多个合法答案**、自动指标只能近似人类判断的问题。与 §十主观测试协议同源：真值是人，指标只是对人类的预测——SPICE 论文把这一点做成了可机检的两口径分解。

### 11.1 n-gram 重叠既不充分也不必要：同词不同图高分、同义改写零重叠低分
- SPICE 论文（Anderson 等，ECCV 2016，arXiv:1607.08822）WebFetch 200 原文逐字：「Existing automatic evaluation metrics are primarily sensitive to n-gram overlap, which is **neither necessary nor sufficient** for the task of simulating human judgment」。论文给的两组反例：「A young girl standing on top of a tennis court.」vs「A giraffe standing on top of a green field.」描述两张极不同的图，却因共享 5-gram「standing on top of a」被 n-gram 指标打高分；「A shiny metal pot filled with some diced veggies.」vs「The pan on the stove has chopped vegetables in it.」几乎同义却无共同词、n-gram 相似度低。
- 各指标机制逐字：Bleu「a modified precision metric with a sentence-brevity penalty, calculated as a weighted geometric mean over different length n-grams」；METEOR 用「exact, stem, synonym and paraphrase matches」对齐后算带碎片惩罚的加权 F-score；ROUGE 是 F-measure 摘要包；CIDEr「applies term frequency-inverse document frequency (tf-idf) weights to n-grams… compared by summing their cosine similarity」。
- **判据**：评生成式文本（描述/摘要/转写）先问「共享词是不是同义的必要条件」——不是就别用 Bleu/ROUGE 单指标下结论。报指标必写它对齐的是词面还是语义命题。

### 11.2 SPICE 的做法：依赖树 → 场景图（对象/属性/关系元组）→ F-score；图像本身被忽略，是纯文本评测
- 论文逐字：两阶段「syntactic dependencies… established using a dependency parser… pre-trained on a large dataset」（Universal Dependency relations），再「map from dependency trees to scene graphs using a rule-based system」；「our metric computes an F-score defined over the conjunction of logical tuples representing semantic propositions in the scene graph」。场景图「explicitly encodes the objects, attributes and relationships found in image captions, abstracting away most of the lexical and syntactic idiosyncrasies」。
- 作者项目页 panderson.me/spice WebFetch 200 逐字：「Reference and candidate captions are mapped through dependency parse trees… to semantic scene graphs… encoding the objects (red), attributes (green), and relations (blue) present. Caption quality is determined using an F-score calculated over tuples」。论文同页注明 AMR + Smatch「performed poorly as image caption representations」，故未采用。
- **判据**：SPICE 是**文本对文本**的评分，不看图；它继承语义解析器的错误（「parser errors directly degrade the metric score regardless of actual caption quality」，二手实现说明逐字）。所以「SPICE 高」只证明候选覆盖了参考里的语义命题，不证明图里真有那些东西——图证仍归 Vision 通道（§一分工）。

### 11.3 系统级与句子级是两个相关口径，差一个量级；参考数改变绝对分，MM/HC 各需不同指标
- 系统级（MS COCO 15 条目＋人类生成字幕，按每个模型一个点）：项目页逐字「system-level correlation of 0.88 with human judgments on the MS COCO dataset, versus 0.43 for CIDEr and 0.53 for METEOR」；Springer ECCV 章节逐字「Only SPICE (top left) scores human-generated captions significantly higher than challenge entries, which is consistent with human judgement」，且「SPICE is the only metric to correctly rank human-generated captions first—CIDEr and METEOR rank human captions 7th and 4th, respectively」。
- 句子级（Kendall τ，表 3）：Flickr 8K — Bleu-1 0.32 / Bleu-4 0.14 / ROUGE-L 0.32 / METEOR 0.42 / CIDEr 0.44 / **SPICE 0.45** / **Inter-human 0.73**；composite — 0.26 / 0.18 / 0.28 / 0.35 / 0.36 / **0.39**。论文逐字「Relative to the correlation between human scores of 0.73, this represents only a modest improvement over existing metrics」——句子级几乎没拉开差距，且离人类一致性上限很远。
- PASCAL-50S 成对分类准确率（5 参考，表 4，四类配对）：HC（两条都对的人类字幕）Bleu-1 64.9 最高；HI（一错）METEOR 98.1；HM（人 vs 机）METEOR 94.2；**MM（两条都是机器生成）SPICE 68.2 最高** vs METEOR 66.8。论文逐字「SPICE is best at matching human judgments on pairs of model-generated captions (MM). METEOR is best at differentiating human and model captions (HM) and human captions where one is incorrect (HI). Bleu-1 performs best given two correct human captions (HC)」，并点明「distinguishing better performing algorithms is the primary motivation for this work」。
- 参考数效应（项目页逐字）：「On MS COCO, with 5 reference captions scores are typically in the range 0.15 - 0.20. With 40 reference captions, scores are typically in the range 0.03 - 0.07. This is the expected result due to the impact of the recall component of the metric. On the MS COCO leaderboard, C40 SPICE scores are multiplied by 10.」
- 语义命题可分解（表 2）：按 object / relation / attribute 及 color / count / size 子类报 F-score；论文逐字「the MSR entry — incorporating specifically trained visual detectors…—exceeds the human F-score baseline for tuples containing color attributes. However, there is less evidence that any of these models have learned to count objects」。
- **判据**：报生成式描述的自动分固定四栏 —— ① 哪个指标（n-gram 还是语义命题）② 哪个口径（系统级 ρ 还是句子级 τ）③ 几条参考字幕 ④ 对比的是哪类配对（HC/HI/HM/MM）。用系统级 0.88 去证明「这条字幕写得好」是层次错配；不同参考数的 SPICE 绝对值不可比；要挑更好的模型看 MM 栏（SPICE 强），要挑错字幕看 HI/HM 栏（METEOR 强）。

### r762B 来源与判非（2026-11-18 实拉，逐字核验）
- `https://arxiv.org/html/1607.08822`（Anderson, Fernando, Johnson, Gould《SPICE: Semantic Propositional Image Caption Evaluation》，ECCV 2016 / LNCS 9909）— **WebFetch 200，AI 摘要 60s 超时后返回前 15,000 / 50,850 字原文逐字**：摘要、n-gram 不充分必要与两组反例、Bleu/METEOR/ROUGE/CIDEr 机制段、依赖树→场景图→F-score 方法段、AMR 判非、表 3/表 4 全值、caption-level vs system-level 区分、结论。**第一独立域（作者一手论文全文主体）**。
- `https://www.panderson.me/spice/`（第一作者 Peter Anderson 官方项目页）— **WebFetch 200 全文逐字**：0.88 / 0.43 / 0.53 系统级相关、场景图定义与 F-score、参考数效应原文（5 refs 0.15–0.20 / 40 refs 0.03–0.07 / C40×10）、COCO leaderboard 与「Only SPICE scores human-generated captions significantly higher」、SPICE F-Score 0.167/Pr0.5/Re0.1 示例。**第二独立域（作者官方发布页，与论文逐字交叉）**。
- `https://link.springer.com/10.1007/978-3-319-46454-1_24`（Springer ECCV 章节页）＋ `https://openresearch-repository.anu.edu.au/items/854e5cc6-...`（ANU 机构仓储著录，2016-09-16，DOI 10.1007/978-3-319-46454-1_24）＋ `https://www.aclweb.org/anthology/P18-3003.pdf`（ACL《Learning-based Composite Metrics for Improved Caption Evaluation》，组合指标 BLEU 0.202/METEOR 0.352/CIDEr 0.356/SPICE 0.366 vs EvalMS 0.386）— **WebFetch / WebSearch 逐字快照**：卷期页码、表 2/3/4 交叉、组合指标仍只是相关而非真值。**第三～五域（出版社/机构仓储/ACL 会议论文，交叉登记）**。
- **失败与降级如实登记**：arxiv HTML 页 AI 摘要 **60s 超时**，取前 15,000 / 50,850 字原文逐字（表 3/4 的数值由同批 WebSearch 对该页的逐字快照补齐）；ANU PDF 与 Springer 正文页只有摘要/著录与部分图注可读，按快照登记，未冒充已读全文。
- **判非**：窄串全库 `SKILL.md` 精确扫描 —— `SPICE` / `CIDEr` / `METEOR` / `图像描述` / `caption` / `BLEU` **目标技能 `engineering/multimodal-intelligence` 0 命中**；其他命中在 `media/wb-visual-gen`（文生图，异命题）、`meta/agent-evolution`、`wb-media-forensics`（取证，异命题）、豆包自留地 `wb-context-compressor` 及大量 co-learn 历史记录。按 rules/07 四态判「**优＝加厚现有 `engineering/multimodal-intelligence`**」，补的是「生成式描述评测」这一正交层，不重述 §6 CER/WER、§7 阅读顺序、§8 FR/RR/NR、§9 色彩、§10 主观测试。PI 模块记忆前 16 条结论不复用。豆包自留地 WB 0 落地。与 r760(AI/VI/DI)/r761(OI/EI/SI) 九模块结论不复用；A/C 两轮结论亦不复用。
- **未采纳**：SPICE 完整场景图解析规则与 WordNet 同义词匹配实现、各挑战赛逐系统分数、组合指标 EvalMS/EvalCS 训练细节、Flickr30k 数据集划分 —— 属实现细节与 benchmark 数值，不迁移为通用判据。

## 十二、目标检测与分割评测：IoU 阈值决定 TP，mAP 是多阈值平均（r766B · 2026-11-19 实拉，≥2 独立域交叉）

> 与 §六～§十一分工：那几节评的是「OCR 文字/图像质量/主观面板/生成字幕」；本节评的是**目标定位与像素分割**这一族任务，判据各自独立，不重述 CER/WER、色彩、主观测试或 SPICE。

### 12.1（r766B-1）IoU≥阈值才计 TP：先定阈值再算 P/R/F1，同一预测换阈值结论会翻
- ZOOZ 工程逐字：2D box 的核心是 `IoU=overlap_area/union_area`；`IoU≥threshold → TP`，`IoU<threshold 或无匹配 GT → FP`，GT 无匹配预测 → FN；再由 TP/FP/FN 算 Precision=TP/(TP+FP)、Recall=TP/(TP+FN)、F1。AP = PR 曲线下面积，mAP = 各类 AP 均值（COCO 上还跨 0.50–0.95 的 IoU 阈值再平均）。
- 逐字解释为何用 IoU 不用中心距：「Two boxes can have the same center distance but very different overlap if one is much larger; IoU captures both position and size accuracy」。实例分割 `Mask_IoU=overlap_pixels/union_pixels`，TP 判据同逻辑；语义分割逐类 `IoU_c=TP_c/(TP_c+FP_c+FN_c)`、mIoU=各类 IoU 均值；关键点用 OKS 而非 IoU（按对象尺度 s 与关键点容忍 k_i 的高斯加权）。
- **判据**：凡报检测/分割的 P/R/F1，必须附 IoU 阈值（0.5 宽松 / 0.75 严格 / 0.5:0.95 多阈值）与匹配规则（一个 GT 是否只匹配一个预测）；不写阈值的「准确率」不可比。

### 12.2（r766B-2）COCO 的 12 指标：AP 与 mAP 不区分、10 阈值平均奖励定位、尺度与 AR 是独立维度
- COCO 官方逐字：主指标 **AP @ IoU=.50:.05:.95（primary challenge metric）**，另有 `AP^IoU=.50`（PASCAL VOC metric）与 `AP^IoU=.75`（strict metric）；**「Traditionally, this is called 'mean average precision' (mAP). We make no distinction between AP and mAP」**。跨 10 个 IoU 阈值（.50:.05:.95）平均，「Averaging over IoUs rewards detectors with better localization」——这是刻意打破单阈值 .50 传统。
- 尺度档逐字：`AP_small/AP_medium/AP_large`（area<32² / 32²<area<96² / area>96²，按 segmentation mask 像素数计），COCO 中约 41% 小、34% 中、24% 大；`AR_max=1/10/100` 是「给定每图最多 1/10/100 个检测时的最大召回」，最多 100 个 top-scoring 检测/图；默认 `iouThrs=.5:.05:.95`（T=10）、`recThrs=0:.01:1`（R=101）、`areaRng` 四档、`maxDets=[1 10 100]`（M=3）。**「detection with bounding boxes and segmentation masks are identical in all respects except for the IoU computation」**——box/mask 只差 IoU 在框还是掩码上算。
- **判据**：报 COCO 系分数固定写清「AP 还是 AP50/AP75、是否跨尺度、maxDets 多少」；跨尺度分报 small/medium/large，不用总体 AP 掩盖小目标失效。AP=mAP 在此口径下同义，禁把两者当两个独立指标相加。

### 12.3（r766B-3）Dice=像素 F1=2·IoU/(1+IoU)：与 IoU 单调等价但数值不可混报，mIoU 才是语义分割主指标
- 逐字：Dice `=2|A∩B|/(|A|+|B|)=2TP/(2TP+FP+FN)`，「literally the F1 formula, so Dice = F1 for binary pixel classification」；`Dice=2·IoU/(1+IoU)` 与 IoU 单调相关、对同一模型排序相同，但数值不同，医学影像偏好 Dice（作 Dice Loss）；IoU「tends to penalize false positives more heavily than the DSC」。
- 语义分割主指标是 mIoU，「PixelAccuracy can be skewed by majority classes」——95% 背景全预测背景得 95% pixel accuracy 却什么也没抓住；实例分割 AP_mask 与检测 AP 同协议、只把 IoU 换成 mask IoU；全景分割用 PQ=SQ×RQ。图像生成另走 FID（Inception 特征分布 Fréchet 距离，越低越好），与检测/分割不是同一族。
- **判据**：① Dice 与 IoU 可互相换算、排序一致，但**数值不能混用或跨指标比较**；② 类别不平衡时禁报 pixel accuracy 当主指标，报 mIoU；③ 检测 mAP、分割 mIoU/Dice、生成 FID 分属不同任务族，禁把单一分数跨族比较「谁更好」。

### r766B 来源与判非（2026-11-19 实拉，逐字核验）
- `http://cocodataset.org/#detections-eval`（COCO 官方检测评测页）— **WebFetch 200 全文逐字**：12 指标定义、AP 与 mAP 不区分、10 IoU 阈值 .50:.05:.95、尺度档与 41/34/24% 分布、AR maxDets、params 默认值（R=101/T=10/A=4/M=3）、box 与 mask 同协议只换 IoU 算法、analyze() 的 C75/C50/Loc/Sim/Oth/BG/FN 错误分解与 ResNet AP .399→定位完美 .682 的数值。**第一独立域（基准官方一手）**。
- `https://engineering.zooz.com/.../the-human-intelligence-behind-machine-vision-...`（ZOOZ Engineering 标注与指标长文）— **WebFetch / WebSearch 逐字快照**：2D/3D box 的 IoU 与 TP/FP/FN、BEV IoU、nuScenes ATE/AOE/ASE、mask IoU、Dice、语义分割 mIoU、关键点 OKS、polyline/点云 Chamfer、任务分档评测。**第二独立域（工程实践一手，与 COCO 官方交叉）**。
- `https://s-samarth.github.io/DataSciencePreparation/ClassicalML/evaluation/vision-rl` + `https://danielhamlin.com/blog/Computer%20Vision/post-3-18-evaluation.html` + `https://www.nature.com/articles/s41597-025-06419-1_reference.pdf` — **WebSearch 逐字快照**：Dice=2·IoU/(1+IoU) 单调等价、FID 定义、PASCAL VOC 11 点插值 vs COCO 全点、Dice/IoU 在电极缺陷分割的公式与「IoU penalizes FP more heavily」、mAP@0.5 与 mAP@[0.5:0.95] 对照表。**第三～五域（教学笔记/工程博客/期刊数据集论文，交叉登记）**。
- **失败与降级如实登记**：ZOOZ 长文与 danielhamlin 页只取 WebSearch 逐字快照，未冒充已读全文；Nature 数据集论文命中为 references PDF 页，公式与对照表按快照登记。PASCAL VOC 11 点插值与 COCO 全点积分是两代协议口径差，并列登记不择一。
- **判非**：窄串全库 `SKILL.md` 精确扫描 —— `mAP` / `IoU` / `Dice` / `平均精度` / `AP50` 的命中中，**本技能内仅 §七/§八/§九判非串出现 `mAP`（OCR-D「mAP 不适用于文档版面」异命题）**，目标检测/像素分割评测本体 **0 命中**；其余命中在 `agent-guild`/`grill-me`/`ci-context`/`wb-agent-evaluation` 等（泛词或异命题）。按 rules/07 四态判「**优＝加厚现有 `engineering/multimodal-intelligence`**」，补目标检测/分割评测这一正交层，不重述 §六 CER/WER、§七阅读顺序、§八 FR/RR/NR、§九色彩、§十主观、§十一生成字幕。PI 模块记忆前 17 条结论不复用。豆包自留地 WB 0 落地。与 r765(OI/EI/SI)/r764(AI/VI/DI)/r763(MI/CI/RI) 九模块结论不复用；A/C 两轮结论亦不复用。
- **未采纳**：nuScenes 全部子指标与 BEV 实现、Panoptic PQ 的 SQ/RQ 公式细节、Chamfer 距离的 3D 重建协议、COCO analyze() 的 372 张图生成细节 —— 属专项基准实现，不迁移为通用判据。

## 十三、非视觉捷径：语言先验让模型「闭着眼睛答对」，盲模型基线才是照妖镜（r770B · 2026-11-19 实拉，≥2 独立域交叉）

> 与 §六～§十二分工：那几节评「读得准不准 / 图质量好不好 / 检测分割对不对」——都假定模型真在用视觉输入；本节评更前置的一问：**模型到底有没有在看图？** 语言先验/非视觉捷径使高分可以完全不来自视觉理解，是评测效度（construct validity）层面的问题，不重述 OCR 的 CER、SPICE 命题 F-score 或 mAP/IoU。

### 13.1（r770B-1）语言先验：问题文本本身泄露答案，「盲模型」不看图也能拿高分
- Goyal 等 VQA v2 原论文（arXiv:1612.00837）摘要逐字：「**inherent structure in our world and bias in our language tend to be a simpler signal for learning than visual modalities, resulting in models that ignore visual information, leading to an inflated sense of their capability**」——世界结构与语言偏置是比视觉更简单的学习信号，模型忽略视觉、能力被虚高。
- 一手长文（grapeot.me 十年脉络）逐字：Agrawal 2016 首析 VQA 语言先验（「What sport is…」高频答案 tennis 不需要图）；Goyal 2017 VQA v2 量化——「**完全无视视觉输入的盲模型(blind model)在二选一问题上能达到 67% 的准确率,在开放问题上也有 27%**」；2018 VQA-CP v2 改变测试集答案分布使其与训练不同，「当时的 SOTA 模型准确率直接下降了 24~27 个百分点……模型学到的很大程度上是问题表面形式和答案之间的统计关联,而非图片内容与答案之间的语义关系」。
- 观微录逐字同构：VQA v1「有没有/是不是」答案严重偏斜（正确答案常是「是」），模型只记「看到『有没有』预测『有』」即可降损失、「不需要提取任何视觉特征」；二元问题类别均衡时随机猜 50%，只答「是」的垃圾模型在 yes 占比高的数据集也能高分。
- **判据**：① 多模态任务报高分前必须先建**盲模型基线**（只给问题文本、不给图）——盲模型高分说明测的是语言先验不是视觉理解；② 二元/是否题单报准确率无意义（类别不均衡 + 语言先验灌水），必须配类别分布与问题-only 基线；③ 测评集与训练答案分布一致性要显式核对，分布一变 SOTA 掉 24–27 点说明模型在背统计关联。

### 13.2（r770B-2）VQA v2 的互补图配对：同一问题配两张答案不同的相似图，逼模型真用视觉
- VQA v2 原论文摘要逐字：「**we balance the popular VQA dataset by collecting complementary images such that every question in our balanced dataset is associated with not just a single image, but rather a pair of similar images that result in two different answers to the question**……approximately twice the number of image-question pairs……**All models perform significantly worse on our balanced dataset, suggesting that these models have indeed learned to exploit language priors. This finding provides the first concrete empirical evidence**」。
- 观微录逐字解释机制：「这个人是男性吗」同时出现在男性与女性图片上，「只靠语言模式猜答案的模型,在这两个互补样本上必然错一个,总分被打回原形」。aiknowledge 逐字：VQA v1（Antol 2015，20.4 万图/61.4 万问）靠「how many 一律答 2 / is there 一律答 yes」走捷径，v2「让『只靠语言走捷径』几乎失效」。
- **判据**：① 设计多模态评测时优先补**互补样本/最小对立对**（同问不同图答案不同、或同图不同问），让纯语言策略必然出错；② 平衡后在平衡集上显著掉分的模型，判定其原高分来自语言先验，不能以旧分数宣称视觉理解能力；③ VQA v2 还附「反例解释」——指出一张相似但答案不同的图，作为可解释性与「是否真看图」的双重验证。

### 13.3（r770B-3）无图像基线当主实验变量、文本先验探测器与医学影像捷径——捷径是跨领域通病
- aicompass 镜像（arXiv:2606.10400 措辞控制基准综述）逐字：Rahmanzadehgervi 2024 记录「大型视觉语言模型在视力正常者都能轻松完成的简单任务上失败」；Tong 2024 基于 CLIP 的模型有系统性盲点并传导到 VLM；Luo 2025「构建了一个文本先验探测器,其项目特意设计为仅凭文本即可作答,以衡量对视觉的规避程度」；「**无图像(仅文本)基线统一了这些发现:去除图像能精确地衡量一个模型依赖问题措辞的程度**」，该工作「将图像依赖性作为主要的实验变量而非次要诊断手段」。
- CSDN 非视觉捷径逐字三形态——语言先验偏差 / 答案分布偏差（VSI-Bench「洗碗机长度」90% 答案集中 85–95cm）/ 模板结构泄露（固定句式「X 在 Y 的哪侧」）；「仅使用问题文本训练的『盲模型』平均准确率比随机猜测高出 33 个百分点」。
- grapeot.me 医学影像逐字：Zech 2018 PLoS Medicine——肺炎检测模型实际学会识别拍片医院来源，「仅用医院来源信息做预测的简单模型就能达到 AUC 0.861，而 CNN 能以 99.95% 的准确率识别影像来自哪家医院」；根因「NIH 数据中肺炎患病率为 1.2%,而 Mount Sinai Hospital 为 34.2%」的基线差。
- **判据**：① 把「去图像」从辅助诊断**升格为主实验变量**（固定 540 图集、跨四变体改措辞 + 大规模无图像消融配对），量化「没有图还能答对多少」；② 警惕**元数据/来源捷径**（医院标记、采集设备、模板句式）——模型可能靠混杂元数据而非目标特征，须做来源盲化/分布平衡；③ 捷径是跨 VQA 与医学影像的通病（近十年积累），任何「某任务高分」结论都要问「去掉目标模态/打散元数据后还剩多少」。

### r770B 来源与判非（2026-11-19 实拉，逐字核验）
- `https://arxiv.org/abs/1612.00837`（Goyal 等《Making the V in VQA Matter》，VQA v2 原论文）— **WebFetch 200 摘要全文逐字**：语言偏置致模型忽略视觉、互补图配对（一问两图两答案）、数据集翻倍、所有模型在平衡集显著更差、「first concrete empirical evidence」、反例解释模型。**第一独立域（原论文一手摘要，主证据）**。
- `https://grapeot.me/share/mirage-multimodal-benchmark-20260405.html`（Computing Life·视觉理解评估十年困局）— **WebFetch/WebSearch 逐字快照**：2016–2018 语言先验脉络、盲模型 67%/27%、VQA-CP v2 掉 24–27 点、Zech 2018 医院来源 AUC 0.861/CNN 99.95%/患病率 1.2% vs 34.2%、MIRAGE 前沿模型量化。**第二独立域（技术长文一手，与第一交叉）**。
- `http://bittide.aicompass.dev/article/...`（arXiv:2606.10400 措辞控制基准镜像）＋ `https://guanweilu.cn/article/453.html`（观微录·开放 vs 二元 VQA）＋ `https://blog.csdn.net/.../160554057`（非视觉捷径）＋ `https://aiknowledge.cn/article/68852`（视觉语言模型）— **WebFetch/WebSearch 逐字快照**：文本先验探测器、无图像基线当主变量、二元随机猜 50%/只答是、三形态捷径、盲模型高于随机 33 点、VQA v1 的 20.4 万图/61.4 万问与 v2 平衡机制。**第三～六域（镜像/技术博客/百科，交叉登记）**。
- **失败与降级如实登记**：VQA v2 原论文仅取 WebFetch 摘要（PDF 正文未逐页核），按摘要逐字登记不冒充全文已读；arXiv:2606.10400 经 aicompass 镜像取得中文转述、未直取原论文；盲模型 67%/27%、VQA-CP 掉 24–27 点、盲模型高随机 33 点、医院 AUC 0.861 等数值均挂各自来源口径，只取定性结论、不择一冒充唯一权威。
- **判非**：窄串全库 `SKILL.md` 精确扫描 —— `language bias` / `语言先验` / `捷径学习` / `answer prior` / `盲模型` 命中全部在 `wb-context-compressor`/`wb-agent-evaluation`/`wb-execute-discipline` 的 **references 下沉文件（豆包自留地）** 与 co-learn 台账，本技能正文（§六～§十二）0 命中本体。按 rules/07 四态判「**优＝加厚现有 `engineering/multimodal-intelligence`**」，补「视觉依赖效度」这一前置层，不重述 §十一 SPICE 命题 F-score（那是评字幕语义覆盖）、§十二 mAP（那是评定位）。PI 模块记忆前 17 条结论不复用。豆包自留地 WB 0 落地。与 r769(OI/EI/SI)/r768(AI/VI/DI)/r767(MI/CI/RI) 九模块结论不复用；A/C 两轮结论亦不复用。
- **未采纳**：MIRAGE 对 GPT-5.1/Claude Opus 4.5/Gemini 3 Pro 的具体分数、VQA-CP 各模型逐项排名、CLIP 盲点清单、错措辞控制基准的四个变体构造细节 —— 属特定模型/数据集评测结果，不迁移为通用判据。

## 十四、生成图像质量 FID：一个数字背后四个被违反的假设（PI · r786B 2026-11-20 实拉，≥4 独立域交叉）

> 与 §六～§十三分工：那些评「读得准不准」（OCR/阅读顺序）、「图质量好不好」（FR/NR 失真）、「检测分割对不对」（mAP/mIoU）、「有没有真看图」（语言先验）——对象是**判别/理解**；本节评**生成**——一组生成图相对一组真实图的分布距离 FID。§十二曾一句「图像生成另走 FID」只给定义，本节展开其可比性条件与失效面。Heusel 等 2017（arXiv:1706.08500）定义：两组图过固定 Inception-v3 的 2048 维 pool3 特征，各拟合多元高斯，取两高斯的 Fréchet（2-Wasserstein）距离平方 `FID=‖μr−μg‖²+Tr(Σr+Σg−2(ΣrΣg)^{1/2})`，越低越好、0 表示两个拟合高斯重合。

### 14.1（r786B-1）★样本量偏差使 FID 系统性偏高、近似 1/n 衰减且随特征维放大——跨论文不可直接比
insightful-data-lab（2025-03-26）逐字实验：同一 32 维高斯抽两独立组、真距离应为 0，五重复平均 FD 在 n=64 时 **9.539**、256 时 2.333、1024 时 0.588、4096 时 0.147、16384 时 0.036——偏差 roughly in proportion to 1/n；且「grows with feature dimension because there are more covariance entries to estimate (Inception features have 2,048 dimensions, not 32)」。根因是有限样本协方差估计误差抬高 trace 项。Ultralytics 中文逐字：小样本抬高分数，原作者建议至少 10,000 张图，5,000 样本与 50,000 样本算出的分数不可比；差异小于绝对偏差不自动无信息（共同偏差可相消），须用重复采样/配对重采样看差值稳不稳。aiwiki 引 Chong & Forsyth CVPR 2020：FID 是有偏估计且**偏差依赖被评模型本身**，模型 A 比 B FID 低可能只是 A 的偏差项小、不是图更好，固定样本量也校不掉，需 FID-infinity 外推。判据：报 FID 必须同时写样本数、特征网络与权重、图像分辨率、resize 实现、参考集；不同样本量的两个 FID 数字不可比高低，差值须报配对重采样或不确定度。

### 14.2（r786B-2）★只匹配均值与协方差会丢掉多模态结构——同前两矩的两组分布可以 FID≈0 却形状完全不同
insightful-data-lab 逐字实验：真实数据是**两个分离簇**、生成数据是从同均值同协方差的单高斯抽样（填满两簇之间的空隙），结果 fake 有 **37.8%** 样本落在真实数据没有任何样本的区域（真实为 0.000）而 **FD 仍仅 0.0001**；反过来丢掉其中一个簇却被检出（FD=6.918）。结论逐字「FID sees only the mean and covariance of the features. Two sets with the same first two moments score 0 whatever their shapes」；真实图像的特征分布本就是多模态+重尾，高斯假设因此失效。aiwiki 引 Borji 2022 同构：FID/KID 只反映分布的前几阶矩、对全局结构不敏感；Jayasumana 2024 显示 FID 把 VQGAN 潜空间噪声造成的失真图评为比不失真版本更好、也不反映 Stable Diffusion/Muse 迭代精修的渐进改善。判据：FID 低不等于「图真的像/多样性对」，须配一项结构诊断（mode collapse 检查、最近邻记忆检查、或 precision/recall、CMMD 等免高斯假设的核距离）；声称「覆盖真实分布」不能只靠一个 FID。

### 14.3（r786B-3）★FID 混淆保真度与多样性、读不到 prompt、且对实现细节敏感到可逆转排名
insightful-data-lab 逐字：单个距离把「生成的图像像不像真的（fidelity）」与「是否覆盖真实图像的多样性（diversity）」两件事混在一起；提高扩散模型 guidance scale 通常在一定范围内用多样性换保真度，FID 沿 guidance 扫描是两者合成、可升可降，单看 FID 分不出变化来自哪一者——拆开需特征空间最近邻估计的 precision/recall 或独立多样性指标（Kynkaanniemi 2019 arXiv:1904.06991）。Inception 训练于 ImageNet 分类，对区分 ImageNet 类别敏感、对其不要求的属性（文字渲染、手、医学影像结构、艺术风格）较不敏感；且 FID 完全不用 prompt，「says nothing about whether an image matches its caption」——文生图任务须另报 CLIP Score 或 GenEval/DPG-Bench 这类逐项语义核验。实现敏感性（labhub 引 clean-fid CVPR 2022 与 aiwiki 引 Parmar 2022）：同一批图换 resize 实现（PIL bicubic 为参考，OpenCV/PyTorch/TF 各差 6 分以上）、JPEG 压缩质量、TF 与 PyTorch Inception 权重差异、参考图随机种子，都让 FID 偏移几个点——幅度可超过论文宣称的模型改进，正是 Clean-FID 标准化的动因。判据：文生图验收至少三项分报——FID（分布距离，同口径可比）+ 文图匹配（CLIP Score/逐项核验）+ 保真/覆盖拆分（precision-recall 或记忆检查）；只报 FID 一个数字不足以支撑「更好」或「更贴合提示」。

### r786B 来源与判非（2026-11-20 实拉，逐字核验）
- `https://insightful-data-lab.com/2025/03/26/frechet-inception-distance-fid`（WebFetch 200 全文逐字：FID 公式与一维校验 1.985、样本偏差五点数值 9.539/2.333/0.588/0.147/0.036 与 1/n、两簇 vs 同矩高斯 37.8%/0.0001/6.918、fidelity 与 diversity 混合、Inception 不读 prompt、CMMD 无偏替代）——第一独立域·带可复现实验的技术一手。
- `https://www.ultralytics.com/zh/glossary/frechet-inception-distance-fid`（WebFetch/WebSearch 逐字：中文口径「至少 10,000 张图」「5,000 vs 50,000 不可比」「torchvision Inception 与原始 TF 权重不可比」「JPEG/resize 偏移几个点」、KID 小样本更稳、CLIP Score 补文图匹配、FD-DINOv2 因大规模人类研究发现 FID 不反映扩散图逼真度评价）——第二独立域·工程 glossary 一手。
- `https://praveentn.live/learn/concepts/fid-and-generative-evaluation-metrics`（WebFetch 逐字：三个假设显性化、样本偏差足以反转模型排名、precision/recall 定义与 mode collapse=高 precision 低 recall、FID 看不见记忆化、guidance scale 使 FID 成曲线而非点）——第三独立域·概念长文一手。
- `https://aiwiki.ai/wiki/frechet_inception_distance`（WebFetch 逐字：Chong & Forsyth CVPR 2020 有偏且模型依赖、FID-infinity、Parmar 2022 五项实现敏感、Jayasumana 2024 与人类判断相悖、Borji 2022 前几阶矩、FVD/FAD/FCD/Clean-FID 变体）——第四独立域·方法百科交叉。
- **判重**：全库 SKILL.md 精确扫描 `Fréchet`/`Frechet`/`CMMD` 0 命中本体，唯一 FID 相关命中为本技能 §十二 r766B「图像生成另走 FID（定义句）」与 `media/pi-audio` r778B「FID 22 命中均为图像生成语境异命题」的判非句——均无专节、无样本偏差/结构/保真多样性的口径。本轮按四态判「**优＝加厚现有 engineering/multimodal-intelligence**」，把 §十二一句展开为独立评测节，不重述检测 mAP/分割 mIoU/语言先验结论。豆包自留地 WB 0 落地。与 r785(OI/EI/SI)/r784(AI/VI/DI)/r783(MI/CI/RI) 九模块结论不复用；A/C 两轮结论亦不复用。
- **未采纳**：Heusel 原论文 GAN 训练细节、StyleGAN2 FID 2.84 / Imagen 7.27 / DALL-E 2 10.39 等特定模型分数、FVD/FAD/FCD 各领域变体公式 —— 属特定模型/特定域结果，不迁移为通用验收判据。

## 十五、文图对齐不能只靠 CLIPScore：词袋化盲区与组合式逐项验收（PI · r790B 2026-11-22 实拉，≥3 独立域交叉）
> 与 §十四分工：FID 评「生成图整体像不像真实分布」且**完全不读 prompt**，§14.3 末尾只留一句「文生图须另报 CLIP Score 或逐项核验」。本节展开这句：当提示涉及对象、属性、关系与数量时，全局嵌入相似度给出的是一个 holistic 数字，无法回答「哪一条组合要求没画对」。

### 15.1（r790B-1）★CLIP 文本编码器的「词袋」性质使主谓颠倒得高分——组合提示不可信
Lin 等 ECCV 2024（arXiv:2404.01291）逐字：the widely-used CLIPScore measures the alignment between a (generated) image and text prompt, but **it fails to produce reliable scores for complex prompts involving compositions of objects, attributes, and relations**；原因「text encoders of CLIP can notoriously act as a 'bag of words', conflating prompts such as 'the horse is eating the grass' with 'the grass is eating the horse'」。GenEval 官方（NeurIPS 2023 arXiv:2310.11513）同向：FID 与 CLIPScore「only offer a holistic measure of image quality or image-text alignment, and are unsuited for fine-grained or instance-level analysis」。判据：含关系/方位/数目的提示禁止只报 CLIPScore；主谓互换的最小对立对是检验对齐指标是否词袋化的干净探针。
### 15.2（r790B-2）★VQAScore 把对齐改成「这张图是否展示了 {text}」的 P(Yes)，用判别式问答绕开全局嵌入
ECCV 2024 原文逐字：VQAScore「uses a visual-question-answering (VQA) model to produce an alignment score by computing the probability of a 'Yes' answer to a simple 'Does this figure show {text}?' question」——off-the-shelf 模型即跨 8 个图文对齐基准达 SOTA；自研双向图像-问题编码器 CLIP-FlanT5「outperforms even the strongest baselines that make use of the proprietary GPT-4V」；只用图像训练却可对齐视频与 3D。配套 GenAI-Bench：1,600 条组合提示（场景/对象/属性/关系及比较与逻辑等高阶推理）+ 逾 15,000 条人评（覆盖 Stable Diffusion/DALL·E 3/Gen2）。判据：组合提示验收优先用可逐条提问的判别式指标，并把用了哪个 VQA 模型/是否双向/提示模板写进结算栏；不要再拿单一余弦相似度当「贴合提示」的证据。
### 15.3（r790B-3）★GenEval 用目标检测拆六类逐项计分；位置墙与属性绑定仍是共同短板
GenEval 官方 table（逐字数值）：CLIP retrieval baseline Overall **0.35**（Position 0.03、Color attribution 0.00）、SD v1.5 0.43、SD v2.1 0.50、SD XL 0.55、**IF-XL 0.61**（Counting 0.66、Color attribution 0.35、Position 0.13）；六类为 single object / two object / counting / colors / position / color attribution。机制：Mask2Former（MS COCO）检测分割逐实例判存在与计数、质心算相对方位、裁物体＋中性灰遮背景后 zero-shot CLIP ViT-L/14 判属性，逐项二值 correct/incorrect 再平均——用专用判别模型验证内容，比通用多模态嵌入「measure」更可靠；6,000 条人标下与人判断一致率 83%（人类之间 88%）。独立二手 Lacuna 综述逐字复述同一结论：CLIPScore「blind to details like spatial relationships and specific attribute binding——struggling to distinguish 'a red cube on a blue sphere' and 'a blue cube on a red sphere'」，IF-XL 有 first-mentioned-object-on-the-left 位置偏置、SD v2.1 更易 color swapping。局限：受 COCO 80 类词表约束、检测器偏真实照片、对高度风格化图弱。判据：文生图结算栏至少三行——分布距离（FID 同口径）+ 文图匹配（VQAScore/GenAI-Bench 含用了哪个模型）+ 实例级六类分报（GenEval 或等价逐项核验），Overall 一个数不足以定位失败模式。
### r790B 来源与判非（2026-11-22 实拉，逐字核验）
- `https://alphaxiv.org/abs/2404.01291v1`（Lin 等《Evaluating Text-to-Visual Generation with Image-to-Text Generation》ECCV 2024，WebFetch 200 全文逐字：CLIPScore 词袋化与主谓颠倒例、VQAScore P(Yes) 机制、8 基准 SOTA、CLIP-FlanT5 双向编码器、GenAI-Bench 1600+15000 人评）——第一独立域·原论文一手摘要全文。
- `https://github.com/djghosh13/geneval`（GenEval 官方仓库，WebFetch 200 全文逐字：holistic 局限六类任务、Mask2Former 检测管线、六模型完整结果表 CLIP retrieval 0.35→IF-XL 0.61、二值 correct/reason JSONL、逐任务 summary_scores）——第二独立域·原论文官方实现一手。
- `https://lacuna.tiptreesystems.com/work/geneval-an-object-focused-framework-for-evaluating-text-vwem/version/art_072abe669df00d543dab554ff16006c2`（WebFetch 200 逐字：红方块蓝球互换例、六类与 553 prompts、83% vs 88% 人标一致率、position wall、IF-XL 位置偏置与 SD v2.1 换色、COCO 80 类局限）——第三独立域·独立技术综述一手。
- **判重**：全库 SKILL.md 扫描 CLIP Score/GenEval 命中仅本技能 §14.3 一句「须另报 CLIP Score 或 GenEval/DPG-Bench 这类逐项语义核验」与其来源行——无专节、无词袋化机制/六类分报/位置墙口径；豆包自留地 defaults/wb-context-compressor 的 CLIP 命中为上下文压缩语境异命题、WB 0 落地。本轮按四态判「增＝加厚现有 engineering/multimodal-intelligence」，把 §14.3 一句展开为独立节，不重述 FID 样本偏差/结构丢失/保真多样性结论。与 r789(OI/EI/SI)/r788(AI/VI/DI)/r787(MI/CI/RI) 九模块不复用；A/C 两轮不复用。
- **未采纳**：DPG-Bench 与 T2I-CompBench 的完整协议、VQAScore 内部训练细节与各基准逐项分数、CLIP-FlanT5 的架构参数 —— 属特定基准/实现，不迁移为通用验收判据。

## 十六、物体幻觉评测：CHAIR 的提示敏感与 POPE 的轮询式二分类（PI · r794B 2026-11-22 实拉，≥2 独立域一手交叉）
> 与 §十五分工：§十五管「生成的图/回答是否贴合组合提示（主谓、方位、数量、属性绑定画对没）」，用 VQAScore/GenEval；本节管「图生文描述或 LVLM 回答里是否出现图中根本不存在的物体」——是物体存在性的幻觉检测，不是对齐度。二者量纲与失败模式不同，不可互替。

### 16.1（r794B-1）★CHAIR 两种形式与提示敏感性：同一模型换个措辞分数翻倍，排序可翻转
alphaXiv（Li 等 EMNLP 2023, arXiv:2305.10355）逐字：CHAIR 来自 Rohrbach 等 2018，两种形式——CHAIR-I 统计幻觉物体提及数占所有物体提及数的比例；CHAIR-S 统计至少含一个幻觉物体的描述占所有描述的比例。「从自由形式文本中提取物体提及需要依赖规则，也可能受到提示和生成风格的影响。」对 LLaVA，用「为图像生成简短描述」时 CHAIR-S 为 32.7；用「请简要描述给定图像」时为 62.7，且作者指出某些比较中模型排序会变化。原文明确限定边界：这「并不能证明 CHAIR 在所有用途下都不可靠」——是特定测试中的提示敏感性，不过度推广。另须分 intrinsic（与图矛盾，如可见范围内断言火车旁有长椅，看图即可否证）与 extrinsic（超出图可验证范围，如断言火车内有座位，需图外信息），后者是否算错取决于用户意图（描述可见场景 vs 求建议）。判据：用 CHAIR 报幻觉率必须写提示模板与物体提取规则，换措辞后的分数不可直接比；把 intrinsic/extrinsic 混成一个数等于把「看图能查的错」与「图外无法判的断言」算成一笔。

### 16.2（r794B-2）★POPE 把描述打分改成「图中有 {物体} 吗」的 yes/no 轮询，正负 1:1，三种负采样探不同偏置
POPE（Polling-based Object Probing Evaluation）三步逐字：①通过人工标注或 SEEM 等自动分割工具，获取每张图像中存在的物体；②根据存在的物体生成「是」问题，再通过采样该图像中不存在的物体生成「否」问题；③提出「图像中有椅子吗？」之类的简短问题，根据标签对「是/否」回答评分。正向与负向问题比例 1:1。缺失物体三种选法——Random 随机采样一个不存在的物体；Popular 选数据集中频繁出现但图中不存在的物体（测是否默认常见物）；Adversarial 选经常与图中真实物体共同出现但图中不存在的物体（如看到餐桌问「有刀吗」，测是否靠共现先验而非像素）。后两者更难：InstructBLIP 的 POPE F1 从 Random 89.29 降到 Adversarial 78.45。「Yes bias」是关键失效——LLaVA / mPLUG-Owl 对几乎所有物体询问答 Yes，某些设置 Yes 率近 99%，而这种「全答是」模式在 caption 幻觉分数里是隐藏的。判据：LVLM 物体幻觉结算至少报 Random/Popular/Adversarial 三档 F1 + Yes 率；只报一个 caption 幻觉率无法诊断由共现先验引发的幻觉。

### 16.3（r794B-3）★POPE 提示鲁棒性更好但仍是不同量纲、且不能消除幻觉；只测存在性
alphaXiv 逐字：四种措辞下 POPE 报告平均 F1 67.43、标准差 0.78；CHAIR-I 平均 13.88、标准差 3.22——「这是不同量纲的不同指标」，该比较只说明这次测试中 POPE 的提示间变化较小，「并不能保证它在所有设置下都稳定」。四模板 POPE F1 为 68.65 / 66.83 / 66.67 / 67.58；四描述提示 CHAIR-I 为 10.50 / 18.80 / 14.60 / 11.60。硬边界逐字：POPE「是一种评估方法，而非缓解幻觉的技术，其得分也不能衡量 LVLM 的整体能力」；自动分割可能引入与人工标注不一致的标签，答案匹配流程会误判未明确含「是」或「否」的回答；研究范围限定粗粒度物体级错误，不涉属性、数量或位置。与 §十五 GenEval 分工：GenEval 六类含 counting/position/color attribution，POPE 只做存在性二分类。判据：报 POPE 须写负采样策略 + 提示模板 + 标签来源（人工/SEEM）；断言「模型不幻觉物体」须有三档 F1 + Yes 率 + 提示鲁棒性，单档 F1 不构成证据。

### r794B 来源与判非（2026-11-22 实拉，逐字核验）
- `https://www.alphaxiv.org/zh/abs/2305.10355`（Li 等《Evaluating Object Hallucination in Large Vision-Language Models》EMNLP 2023，人大/美团，WebFetch 200 全文逐字：CHAIR-I/S 定义、LLaVA 32.7 vs 62.7、intrinsic/extrinsic、POPE 三步与正负 1:1、Random/Popular/Adversarial 定义、InstructBLIP 89.29→78.45、POPE F1 67.43±0.78 对 CHAIR-I 13.88±3.22、四模板数值、局限边界）——第一独立域·原论文一手全文。
- `https://research.elamur.ai/free/en/papers/li-2023-evaluating-object-hallucination-large-vision`（独立论文解读，WebSearch 逐字交叉：CHAIR 短描述指令 32.7 对 OSCAR Base 13.0、改「brief description」措辞可翻转排名、POPE 与 VQA 分工——MiniGPT-4 物体探测分更高但 LLaVA 在更广 VQA 上更好、SEEM 自动分割构建问题）——第二独立域·独立解读交叉（WebSearch 逐字非 WebFetch，如实登记）。
- **判重**：全库 SKILL.md 扫描 `POPE` / `物体幻觉` / `CHAIR` / `polling-based` 命中仅 system/bsk-drive-logged-in-browser 的 `Popen`（Python 子进程 API 子串误命中，非学术指标）；本技能 §十五是文图对齐（VQAScore/GenEval 组合提示），与物体存在性幻觉异命题。按四态判「增＝加厚现有 engineering/multimodal-intelligence」，不重述 §十四 FID 或 §十五对齐结论。豆包自留地 WB 0 落地。与 r793(OI/EI/SI)/r792(VI/AI/DI)/r791(MI/CI/RI) 九模块及 A/C 两轮不复用。
- **未采纳**：POPE 在 A-OKVQA/GQA 上的迁移数值、CHAIR 在全部模型上的逐项分数表、缓解幻觉的训练方法（本轮只做评测协议，不做缓解）——属特定实现/特定域结果，不迁移为通用验收判据。

## 视觉 token 剪枝 FastV：第 2 层后按注意力分数剪，45% FLOPs 不是随便剪一半（r795J 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）

§CHAIR/POPE 管「幻觉怎么测」，本章管**推理成本**：VLM 深层对视觉 token 的注意力极稀疏，剪枝是 plug-and-play 的推理期旋钮，不改训练。

**独点1** 标题/ID 判据：arXiv:2403.06764 的真实标题是「An Image is Worth 1/2 Tokens After Layer 2: Plug-and-Play Inference Acceleration for Large Vision-Language Models」（ECCV 2024 Oral），引用不含此标题即判错误条目；曾错配的 2403.01670 / 2404.10719 一律不得入库。

**独点2** 参数判据：一手须同时出现 `K=2`（第 2 层后开始）与 `R=50%`（保留比例）；论文逐字「Beyond this selected layer, image tokens are re-evaluated based on their average received attention scores」，`K=2,R=50%` 报约 45% FLOPs 降低且不掉性能。宣称「末层剪枝」「需微调」与一手冲突——训练无关。

**独点3** 分类判据：pruning（永久丢弃视觉信息）与 merging（合并冗余特征，如 ToMe/PruMerge）须分列；把 merging 方法归为 FastV 本体判混淆。与本章 §物体幻觉评测分工：剪枝省算力，不自动改善对象存在性幻觉，须另测。

- **判重：`FastV`/视觉 token pruning 在本体与全库 SKILL.md 0 命中；与 §FID、§文图对齐、§CHAIR/POPE 分工不复用。豆包自留地 WB 0 落地。**
- **来源与诚信**：https://ar5iv.arxiv.org/html/2403.06764（Chen 等，arXiv:2403.06764，提交 2024-03-11，v3 2024-09-02，ECCV 2024 Oral，WebFetch 200 逐字：深层注意力低效 / 第 2 层后按平均注意力重评 / K=2 R=50% 约 45% FLOPs）；https://github.com/pkunlp-icler/FastV（作者官方仓库，WebFetch 200 逐字：plug-and-play inference acceleration / 45% theoretical FLOPs / Oral 2%）。第三方综述 arXiv:2603.27960 的提交日未单独核实，仅作分类交叉，不作标题一手。 逐字全文与判非见 `references/r795J_FastV视觉剪枝.md`。
## 图表问答 ChartQA：人写与机器增广两半分报，逻辑+算术推理不是 OCR（r796J 独立实拉 2026-11-22，≥2 独立域一手交叉，3 独点）

§CHAIR/POPE 测物体幻觉、§FastV 省算力，本章管**读图答问评测**：图表问题要跨视觉属性与算术，OCR 对了不等于答对了。

**独点1** 双半数据必须分报：ChartQA-H（human-authored，4.8K 图 / 9.6K QA）与 ChartQA-M（machine-generated，17.1K 图 / 23.1K QA，由人写图表摘要经 T5 生成并人工抽检）；判据——合并成单一分数判不合格。论文逐字：generated another 23,111 questions automatically from human-written chart summaries using a T5 model。

**独点2** 推理类型判据：问题需「logical and arithmetic operations」并引用视觉属性（颜色、峰值）；判据——只用 OCR 文本匹配、不看图表视觉表示的方法在 OCR 出错或问题用同义词指代图表元素时会失效（论文逐字）。与文档 TableQA 分工：那里输入是结构化表格，这里输入是图表视觉编码。

**独点3** 拆分与可复现：官方仓库 train/val/test，train 含 train_human.json 与 train_augmented.json 双文件；判据——报结果须写明在哪一半与哪个 split。relaxed accuracy 容差、盲基线数值、图表幻觉术语本轮未从一手取到，不得写成已验证事实。

- **判重：`ChartQA`/图表问答在本体与全库 SKILL.md 0；与 §FID/文图对齐/CHAIR-POPE/FastV 分工不复用。豆包自留地 WB 0 落地。**
- **来源与诚信**：https://arxiv.org/abs/2203.10244（ChartQA，ACL 2022 Findings，2022-03-19，WebFetch 200 逐字：复杂逻辑与算术推理/T5 生成 23111 问题）; https://arxiv.org/html/2203.10244v1（WebFetch 逐字：OCR 错误或同义词使空间编码分类法失效/表 1 双半数据量）; https://github.com/vis-nlp/ChartQA（作者官方数据集仓库，WebFetch 200 逐字：train_human.json 与 train_augmented.json 双文件/split 结构）。初抓 2003.10244 错配地球物理论文已更正 2203.10244；HTML 全文 60s 超时仅前 15000 字，metric/盲基线未取到。 逐字全文与判非见 `references/r796J_ChartQA.md`。

## 视觉对比解码 VCD：training-free 解码期缓解物体幻觉（PI · r797B 2026-11-23）
§16 CHAIR/POPE 是**测**幻觉，本章是**缓解**幻觉；与 r795J FastV（推理加速）异命题。
**独点1** 两大幻觉根因＝统计偏差（高频物体/虚假共现）＋语言先验（视觉模糊时退化为文本 next-word）。给图像加高斯噪声＝主动造一个「偏向幻觉的分布」当负样本；噪声不是抗噪而是「幻觉放大镜」，同时放大两类 bias。对比原图与噪声图两分布剥掉幻觉概率。
**独点2** 对比式 `diffs=(1+α)L_orig−αL_noise`（等价无分类器引导 (1+α)ε(x,c)−αε(x)，α 放大差异、α=0 回常规解码）。直接全局对比会误伤噪声图仍保留的语法常识 → 自适应合理性约束：只在原图分布高概率 token 集合内对比（β 控截断、越大越激进）。报 VCD 写清 α/β/扰动方式。
**独点3** 收益 POPE 最高 +7.4 F1／MME 幻觉子集 +18%，跨 LLaVA-1.5/InstructBLIP/Qwen-VL；α∈[0.25,1] 与 5 种采样策略均鲁棒，7B≈13B 说明堆参数不解决幻觉。边界：只缓解存在性幻觉、噪声方式粗糙、论文用词 mitigate 非消除。
判重：本体 0 专节；豆包自留地 WB 0 落地。
来源与诚信：Leng 等 arXiv:2311.16922（DAMO/NTU，2023-11-28）WebFetch 200 一手（全文超时仅取前 15000 字）＋CSDN/DeepWiki/Lacuna/llm-paper-notes 方法细节逐字。逐字全文与判非见 `references/r797B_视觉对比解码VCD.md`。

## 图像缩放的重采样滤波器与混叠：先低通再重采样，滤波器选型是测出来的不是描述的（PI · r811C 独立实拉 2026-11-26，≥2 独立域一手交叉，3 独点）

§r732A 管「服务端静默降采样改写了感知输入的分辨率」、§r750B 管 FID 的 resize 实现差异——本节补**缩放动作本身**：重采样滤波器如何决定混叠/锐度/速度，以及为何这是感知评测的前置变量。

**独点1** 缩小是低通滤波再重采样，不是丢像素——最近邻缩小就是欠采样：奈奎斯特–香农定理逐字「若入射影像沒有高於某個最大值 f_max 的空間頻率…以高於 2 f_max 的取樣率…就能精確擷取訊號」；「取樣慢於此即為欠取樣（undersampling）：高頻無法被表示，而且它們不會單純消失，反而會偽裝成虛假的低頻。這就是混疊（aliasing）的根本原因」，后果是锯齿斜线/闪烁细线/摩尔纹。正解逐字「你必須在取樣之前先做頻帶限制（band-limit）…先稍微模糊，以抗鋸齒光學低通濾鏡，或對每個像素的面積取平均」；「要正確縮小影像，你必須先低通濾波再次取樣，絕不能只是丟掉像素」。判据——把「缩小」当信息无损是错的：物理层高频不可逆丢失，能做的只是按 HVS 做感知重构；此规则同样支配 SIFT/CNN 前处理的图像金字塔。

**独点2** 八种滤波器是「混叠残留 × 锐度 × 速度」三维权衡，且必须看实测数字而非口号：Pillow 13.0.0 实测（1600→400 缩小）残留假图案标准差 NEAREST 90.8 / BOX 10.4 / BILINEAR 1.2 / HAMMING 4.9 / BICUBIC 1.0 / LANCZOS 0.6（越小越干净），真实细节保留 NEAREST 91.3（高只因连混叠一起保留）/ BICUBIC 69.7 / LANCZOS 79.1 / MKS2013 84.3；速度 NEAREST 0.08ms / BILINEAR 5.13ms / BICUBIC 9.12ms / LANCZOS 14.38ms。官方「Short answer」逐字：缩照片用 LANCZOS、近似质量更快用 BICUBIC、「NEAREST only for pixel art or masks whose exact values must not be blended」；「Image.ANTIALIAS was the old name of LANCZOS and was removed in Pillow 10」；Pillow 13 新增 MKS2013（「measured sharper than LANCZOS with about as little aliasing and runs faster」，但仅 resize/thumbnail 可用、rotate/transform 不接受）。判据——报「用什么缩放」须写滤波器名+库版本+是否先 reducing_gap：6000×4000→600×400 直接 LANCZOS 167.6ms、reducing_gap=3 降到 55.1ms 且最大像素差仅 3（肉眼不可见），`thumbnail()` 默认 reducing_gap=2.0；Lanczos 锐利但有振铃（高对比边缘虚假亮暗边），放大「cannot add detail; the filter only decides how to fill the gaps」。

**独点3** 选滤波器要看下游用途，ML 预处理「跟模型训练时一致」压过「视觉上更锐」：「Machine-learning preprocessing → whatever the model was trained with — Usually BILINEAR or BICUBIC; mismatches cost accuracy」；分割 mask/标签图必须 NEAREST（「Other filters blend labels into values that mean nothing」），像素画/QR 码放大也要 NEAREST 保硬边与精确色值。与 §r732A 视觉输入降采样、§r750B FID 对 resize 实现敏感（PIL bicubic 为参考，换实现差 6 分以上）联动：同一张图换滤波器就换掉模型实际看到的像素，感知结论与 FID 数字都会变。判据——感知管线的 resize 滤波器须作为声明项固定并随结果上报，不能让库默认值（`resize()` 不传滤波器对照片用 BICUBIC、对 1/P 模式图用 NEAREST）暗中改变结论；色度抽样（4:2:0 牺牲色度保亮度）是与空间重采样正交的另一维压缩（二手工程口径，立场登记）。

**判重**：`重采样`/`resampling`/`Lanczos`/`bicubic`/`抗锯齿`/`混叠`/`Nyquist` 在 multimodal-intelligence 本体仅 §14.3 FID 一句「换 resize 实现差 6 分」、§r732A 一句「按可控插值预缩放」提及，无滤波器机制/采样定理专节；全库 SKILL.md 0 专节（命中在 co-learn/采购域）。豆包自留地 WB 0 落地。按 rules/07「增＝加厚现有」，0 新建 / 0 合并 / 0 删除。

**来源与诚信**（≥2 独立域一手 WebFetch 200 逐字）：https://pillowpython.com/guides/resampling-filters/（Pillow 13.0.0 实测页 Updated 2026-11-22：八滤波器枚举值与编号／残留假图案与真实细节标准差／缩小放大速度 ms／reducing_gap=3 167.6→55.1ms 最大差 3／ANTIALIAS=LANCZOS 旧名 Pillow 10 移除／MKS2013-2021／按用途选型表含 ML 预处理与 mask 用 NEAREST）——第一独立域·可复现实测一手；https://jovanaeducation.com/zh/glossary/image-sampling（影像取樣 glossary 逐字：奈奎斯特–香农 2·f_max／欠采样高频伪装低频=混叠／先 band-limit 面积平均或光学低通／「要正確縮小影像…絕不能只是丟掉像素」／最近邻缩小=欠采样／SIFT/CNN 图像金字塔）——第二独立域·术语一手；TrueSight tsight.io 两篇（插值算法对比表、色度抽样 4:2:0，WebSearch 二手立场登记，不冒充一手）。数字挂可复拉 URL；逐字全文与判非见 `references/r811C_重采样与抗锯齿.md`。


## 多目标跟踪（MOT）评测：MOTA 检测偏科 / IDF1 关联偏科 / HOTA 几何平均平衡 + 五类错误分解（PI · r816C 独立实拉 2026-11-27，≥2 独立域一手交叉，3 独点）

§r766B 评单帧检测/分割、§r790B 评文图对齐、§r794B 评幻觉——本节补「跨帧身份关联」这一维度：MOT 分数为何必须三指标分报、HOTA 怎么平衡、分数掉了怎么定位错误类型。

**独点1** 三指标偏科不同，必须分报不可互证：原论文 Fig.1 逐字「MOTA and IDF1 overemphasize the effect of accurate detection and association respectively. HOTA balances both」；「MOTA performs both matching and association scoring at a local detection level which biases scores toward measuring detection, while IDF1 performs both at a trajectory level which ends up being biased towards association. HOTA matches at the detection level while scoring association globally over trajectories」。MOTA=1−(|FN|+|FP|+|IDSW|)/|gtDet|（式2，检测级逐帧一对一匹配，IDSW 只与「同 gtID 的上一个 TP」比、不计 ID Transfer）；IDF1=|IDTP|/(|IDTP|+0.5|IDFN|+0.5|IDFP|)（式6，轨迹级匹配，对身份保持敏感，但对检测非单调）。判据——DeepSORT「ID 切换少 45% 但 MOTA 只多 1.6 分」、FairMOT「只训检测、re-ID 随机的模型 MOTA 反而更高」均说明 MOTA 高不等于跟得对；MOTA 高 IDF1 低=老丢 ID 又重启；两者矛盾用 HOTA 裁决。

**独点2** HOTA 是几何平均（不是二手常写的调和平均），且跨阈值积分有顺序约束：原式21 `HOTA_α=√(DetA_α·AssA_α)`，DetA=|TP|/(|TP|+|FN|+|FP|)、AssA=(1/|TP|)Σ𝒜(c)、𝒜(c)=|TPA|/(|TPA|+|FNA|+|FPA|)（「double Jaccard」）；最终 `HOTA=∫₀¹HOTA_αdα≈(1/19)Σ_{α∈{0.05..0.95}}`，每个 α **各自重新匹配**，且逐字「DetA and AssA should only be combined into HOTA before integrating over α values, not afterwards」。判据——CSDN 把 HOTA 写成 `2·AssA·DetA/(AssA+DetA)`（调和平均）是**错的**，以原论文几何平均为准；报 HOTA 须带 α 网格与「先合成后积分」顺序。

**独点3** 五类基本错误拆成子指标，单一标量不足以定位：原论文逐字「false negatives, false positives, fragmentations, mergers and deviations … equivalent to detection recall, detection precision, association recall, association precision, and localisation」。DetRe=|TP|/(|TP|+|FN|)、DetPr=|TP|/(|TP|+|FP|)、DetA=DetRe·DetPr/(DetRe+DetPr−DetRe·DetPr)；AssRe/AssPr 逐 TP 求关联 recall/precision 再同式合成 AssA（低 AssRe=把一物体拆成多轨、低 AssPr=一轨跨多物体）；LocA=逐 TP 空间相似度跨 α 积分（「similar to MOTP, however evaluated over multiple localisation thresholds」）。MOTChallenge 官方 19 项：MOTA/IDF1/HOTA/MT/ML/FP/FN/Rcll/Prcn/AssA/DetA/AssRe/AssPr/DetRe/DetPr/LocA/FAF/ID Sw./Frag（ID Sw ratio=#ID switches/recall、Frag ratio=#FM/recall）；MOT16 MOTeD 实测 MOTA 61.9/IDF1 56.2/HOTA 46.2 说明同跟踪器三项差距大。判据——分数掉了先定位 DetRe/DetPr/AssRe/AssPr/LocA 哪一类再改模型，不拿单一 MOTA 当 go/no-go；用 TrackEval 官方脚本复现 protocol。

**判重**：`MOTA`/`IDF1`/`HOTA`/`多目标跟踪` 全库 SKILL.md 0 专节；豆包自留地 WB 0 落地。与 §r766B 检测/分割（单帧 IoU/mAP/Dice）、§r790B 文图对齐、§r794B 幻觉分工：那些评单帧或单图，本节评跨帧 ID 关联与时序轨迹。按 rules/07「增＝加厚现有」，0 新建 / 0 合并 / 0 删除。

**来源与诚信**（≥2 独立域一手）：https://arxiv.org/html/2009.07736v2（Luiten et al. IJCV，WebFetch 200 全文逐字：Fig1 三跟踪器偏科／式2 MOTA／式4-6 IDF1／式13-16 HOTA double Jaccard+跨阈值积分／式18-21 DetA·AssA 几何平均／式22-27 DetRe·DetPr·AssRe·AssPr／五基本错误分类／「combine before integrating, not afterwards」）——第一独立域·原论文一手；https://motchallenge.net/method/MOT=2950&chl=5&vidSeq=MOT16-12（MOTChallenge 官方归档 WebFetch 200 全文逐字：19 项指标全称表／MOT16 MOTA 61.9 IDF1 56.2 HOTA 46.2 ID Sw.1003(14.6%) Frag 2776(40.5%)／页面标 evaluation service closed、Archive 2026-04-16 如实登记）——第二独立域·官方一手；docsaid.org 中文解读 + qubittool 词条 + CSDN（WebSearch 逐字：DeepSORT 45%/1.6 转述／CSDN 调和平均公式错误已按一手纠正）——第三～五域交叉（立场登记）。诚信：`arXiv:2009.13713` 号错配（实为数学论文《Chaos and frequent hypercyclicity…》）WebFetch 检出后整篇弃用，改用正确号 2009.07736，不虚构；逐字全文与判非见 `references/r816C_MOT评测MOTA-IDF1-HOTA.md`。
