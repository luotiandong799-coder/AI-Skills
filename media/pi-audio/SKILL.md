---
name: media/pi-audio
description: 音频感知（Audio/Speech Perception）。当需要把录音/会议/播客/通话转成文字、标"谁在什么时候说了什么"、生成字幕、做语音合成（TTS）、识别音频事件（警报/音乐/故障声）或理解音频内容时调用。提供 ASR 选型（AudioTranscribe 本地/Whisper API/faster-whisper/whisperX）、长音频分段并行、VAD 去静音防幻觉、pyannote 说话人分离与时间戳对齐、LLM 后处理、SRT/VTT 输出、TTS 与隐私护栏。不用于音视频格式转码（走 rg-ffmpeg-tools）、图像理解（走 multimodal-intelligence）。；响度归一化与 LUFS 测量口径（K-weighting/双门控/M·S·I 三时间常数/真峰 dBTP）；声音事件检测 SED 评测口径（segment-based F1/ER vs event-based collar F1 vs PSDS 交集匹配/DTC·GTC·αCT·αST 参数/50 工作点/threshold-independent/跨数据集与年份分数不可比）。；语音反欺骗评测（ASVspoof 三任务 LA/PA/DF/有 ASV 看 min t-DCF 含 C0·C1·C2 串联 ASV 性能、无 ASV 的 DF 看 EER 不可跨任务比/progress→eval EER 崩塌是过拟合泛化失败/四基线 CQCC-GMM·LFCC-GMM·LFCC-LCNN·RawNet2 用 2019 数据无增强）。
module: PI
modules: PI
version: "1.5.0"
---

# PI · 音频感知（Audio / Speech Perception）

> 本技能覆盖 Personal AI OS 13 模块中 **PI（感知智能）** 的音频侧。与 `media/rg-ffmpeg-tools`（转码/元数据，做 16kHz mono 预处理）和 `engineering/multimodal-intelligence`（图像 Vision+OCR）互补：本技能管"语音→文字/说话人/时间戳"与 TTS。
> 方法论实拉自 2026-11-07 WebSearch（真实可核验）：keimodel.com（Whisper API/本地/faster-whisper/pyannote）、bub.im（WhisperX runbook/模型显存/坑表）、whipscribe.com（faster-whisper vs 云/流水线税/Large-v3-turbo）、pyannote.ai（diarization 对齐）、aijobsok.com（音频流水线阶段/隐私/评测）、primo.ai（语音 AI 三件套/STT-LLM-TTS/指标）。

## 一、四条能力通道 + 分工

| 通道 | 职责 | 本仓落点 |
|---|---|---|
| **ASR 语音转文字** | 音频→文本（可带词级时间戳/置信度） | 本技能；本地工具 `AudioTranscribe` 或 faster-whisper |
| **Diarization 说话人分离** | 谁在什么时候说话（speaker,start,end） | 本技能（pyannote）；再与 ASR 时间戳对齐 |
| **TTS 语音合成** | 文本→音频（配音/无障碍/读回校验） | 本技能（发音规则/披露/授权） |
| **音频事件/理解** | 警报/音乐/故障声/情绪等 | 本技能；分类器（YAMNet/AST）或音频大模型 |

**边界**：格式转码、抽帧、元数据 → `rg-ffmpeg-tools`；只看图 → `multimodal-intelligence`；本技能只做"听懂声音"。

## 二、标准转写流水线（7 步）

```
音频 → ①预处理(16k mono) → ②VAD 去静音 → ③ASR 转写(词级时间戳)
     → ④强制对齐(修时间戳漂移) → ⑤说话人分离+时间重叠对齐 → ⑥LLM 后处理 → ⑦复核/输出
```
- **① 预处理**：`ffmpeg -ar 16000 -ac 1`（Whisper 内部就是 16kHz mono；直接喂 44.1kHz 立体声 = 准确率骤降的高频原因）。
- **② VAD**：先裁大段静音/音乐再进 ASR，省时且**避免模型在静音/音乐段编造台词（幻觉）**。
- **③ ASR**：走下方选型；开 `word_timestamps` 供字幕/对齐。
- **④ 对齐**：长音频 vanilla Whisper 时间戳会漂移 → 用 WhisperX 强制对齐修回。
- **⑤ 分离**：pyannote 出说话人段 → 取每条转写段与说话人段**最大时间重叠**者作为该段说话人。
- **⑥ 后处理**：LLM 去口水词、补标点、分段，**保原意**（不许改语义/编造）。
- **⑦ 复核**：低置信段、专名/数字/决定、重叠语音标"待人工核"。

## 三、ASR 选型（按隐私/成本/硬件）

| 方案 | 何时用 | 要点 |
|---|---|---|
| **`AudioTranscribe` 本地工具**（本环境已有） | 本机音频、要中/英/方言、要说话人分离、免配环境 | 直接调 deferred 工具，支持长音频 + speaker separation |
| **Whisper API** | 短音频、低量、图省事 | $0.006/分钟、≤25MB、`response_format='verbose_json'` 出词级时间戳 |
| **faster-whisper**（CTranslate2） | 本地批量、有 GPU | 比原版快 2–4×、省 ~40% 显存；`vad_filter=True`、`word_timestamps=True` |
| **whisperX** | 要**词级时间戳 + 说话人标签** | faster-whisper + 强制对齐 + pyannote 一体 |
| **云端（Deepgram/AssemblyAI）** | 要托管 diarization/弹性扩容、数据可出境 | 按分钟计费；先查保留/训练条款 |

**模型档**：`large-v3` 最准（多语/低资源，~10GB 显存）；`large-v3-turbo` 英文/日常~6–8× 快（~6GB），多语稍降；CPU 用 `tiny/base`+int8 或 whisper.cpp。

## 四、长音频与分段（防误差累积）

- 超长文件按**静音边界切 ~2 分钟 chunk 并行**（多 worker），拼接时段间留 overlap 并 trim 重叠防重复句。
- 本地 Whisper 内部 30s 窗口**不跨窗带上下文** → 长转写用 `condition_on_previous_text=False` 防误差累积/跑偏。
- 每段独立对齐时间戳，别指望一条长链时间戳全程准。
- 监控显存峰值，单次别塞超长音频；diarization 放**第二遍**单独跑，避免和 ASR 同时抢显存。

## 五、说话人分离（pyannote）

- pyannote `speaker-diarization-3.1` 出 speaker/start/end；与 ASR 段做时间重叠对齐。
- **传入已知说话人数显著提升准确率**。
- 阈值调优：同人被拆两个身份→调大 distance_threshold；不同人被合并/重叠→调小；切太碎→调大 min_speaker_duration。
- 跑完先看 speaker 段时间分布图：某说话人平均只 2 秒且碎成片=过分割；分布异常整齐=被强噪声带偏。

## 六、输出与后处理

- **结构化 JSON**：`{speaker, text, start, end, confidence}` + 源块回链，便于下游摘要/检索/跳转。
- **字幕**：启词级时间戳 → SRT/VTT，按 ~20 字符/秒可读性拆过长句。
- **LLM 后处理**：去 `um/ah`、修标点、分段，**保留说话人原语气**；只做可读性，不做"改写事实"。

## 七、坑与护栏（硬规则）

- **绝不把转写当"真相"**：口音、重叠、专名、数字、噪声都会错；关键项（姓名/金额/日期/决定）必须保留原始音频 + 给复核路径。
- **幻觉段落**：静音/音乐段最易出现重复台词；VAD + 去死气是第一道闸。
- **语言**：短片段/中英混说务必显式 `--language`，别靠自动探测。
- **隐私**：录音含对话/身份/健康/生物特征 → 说明是否存储、存多久、谁能访问；传输与静态加密、可删除；第三方处理的先查保留与训练条款。
- **TTS 护栏**：先定发音/停顿/数字/缩写规则 + 安全上限；预览用代表性内容；合成语音在可能混淆处须**披露**；**未获授权不得克隆他人声音**（防语音欺诈）。

## 八、TTS（语音合成）

- 场景：配音/无障碍/读回校验。级联语音 agent = `STT→LLM→TTS`（可控可日志，延迟略高）；要最低延迟用语音到语音模型。
- 开源本地：Kokoro、Piper（轻量、可离线）；商用：ElevenLabs/OpenAI/Microsoft/Google。
- 铁律见 §七 TTS 护栏。

## 九、与 OS 协作

- 音频格式预处理（16k mono/抽轨/切块）→ 委派 **`media/rg-ffmpeg-tools`**。
- 转写后摘要/纪要 → **KI/写作**技能；决策/概率 → **DI/PDI**。
- 评测口径：WER（词错率）、diarization error rate、延迟、可读性；流水线"错误可见可管理"即达标，不强求每句完美。

## 十、来源（2026-11-07 实拉）

- Whisper API vs 本地 / faster-whisper / pyannote 对齐 / 长音频切分：keimodel.com/how-to/whisper-audio-transcription
- WhisperX runbook / 模型显存 / 坑表（幻觉/漂移/显存/OOM）：bub.im?p=5689
- faster-whisper vs 云 / Large-v3-turbo / 流水线税 / word_timestamps/vad_filter：whipscribe.com/blog/faster-whisper-vs-whipscribe-2026
- pyannote diarization / 时间重叠对齐 / 已知人数提升准确率：pyannote.ai + pyannote.ai/blog/multi-speaker-meeting-transcription-pyannoteai-whisper
- 音频流水线阶段 / 隐私保留 / 评测（WER）：aijobsok.com/topics/multimodal-ai/audio-processing-pipelines
- 语音 AI 三件套 / STT-LLM-TTS / 指标 / voice fraud：primo.ai/w/index.php?oldid=46727

## r708C 下沉：分离评测是三分量诊断，幻觉阈值必须按域校准（2026-11-08 实拉）

> 与既有「WER / pyannote 对齐 / VAD 去静音防幻觉」分工：那些管**流水线搭起来**；本节管**"做完了到底错在哪"的量法**与**阈值的可信区间**。判重：全库 `WDER` / `JER` / `collar` / `no_speech_prob` / `missed speech` / `speaker confusion` 词边界 **0 命中** ⇒ 净新。

- **DER 是三分量之和，不是单一分数**：`DER = (Missed Speech + False Alarm + Confusion) / 总参考语音时长`。三分量各自指向**不同修法**：missed（参考有语音、系统没标）→ 查 VAD / 重叠处理；false alarm（非语音区被标语音）→ 查噪声门限；confusion（语音区在、说话人标签错）→ 查嵌入/聚类/跨文件链接。**只报总 DER 不知道该修哪**，须用 `detailed=True` 分列输出。
- **分数脱离评分协议不可比**：报告必须同时写明 ① **forgiveness collar**（常见 ±0.25s；pyannote 的 collar 是**总宽**，0.5 等价于双边 0.25；DIHARD 用零 collar 从严）② **重叠语音是否计分** ③ 参考集条件（远场/电话/会议）。标签置换歧义先用 Hungarian 求最优映射。判据：**没写这两项设置的 DER 数字不要跨来源比较**。
- **按用途选指标**：DER 按时长加权，对**话少的说话人**不敏感 ⇒ 少数说话人要并报 **JER**（每说话人等权 Jaccard，DIHARD 引入）；下游是**带说话人标签的转写稿**时用 **WDER**（按词界算，短犹豫里的一次混淆对 DER 几乎无感、对 WDER 会跨好几个词）。看**逐文件**分数，别只看均值——一类录音三倍于其余的失效会被平均掉；同时核对「估计说话人数」与参考，一个被拆成两人的说话人几乎不抬 DER 却毁掉分人摘要。
- **`no_speech_prob` 不是通用字段**：仅 OpenAI `whisper` 库 `model.transcribe()` 的 dict 输出提供；**`faster-whisper` / streaming API / `whisper.js` 都没有** ⇒ 换引擎时该过滤规则整体失效，必须改用该引擎自有信号并重测。
- **阈值按域标定，别抄 0.5**：收 50+ 份本域真实转写，人工标"静音区幻觉 vs 真实语音"，画分布后选阈（语音密集域常见 0.6–0.75，示例 0.65）。边界例：`0.51` 且含微弱语音会被误滤。过滤要**可配置**（音频编辑、带时间空档的字幕需保留静音段），不硬编码。
- 组合防线（与"先裁静音"串联）：`no_speech_prob` 阈值 + 幻觉正则（`[(` / music / applause / laughter / silence / inaudible / untranscribed）+ 时长/字符下限 + **词级时间戳落在有效片段外即丢弃**；解码侧关掉 `condition_on_previous_text`（噪声多人会放大错误传播）、温度回退封顶、`logprob_threshold` / `compression_ratio_threshold` 触发重切或人工复核。判据：**段级平均置信度会掩盖段内一整句臆造**，须下钻词级。

**来源（2026-11-08 实拉，逐串核验）**：
- `www.pyannote.ai/blog/how-to-evaluate-speaker-diarization-performance` — HTTP 200 / 464,580B，命中 Missed Speech·False Alarm·Confusion·WDER·JER·Jaccard·collar·overlap。
- `theaicompendium.com/8-audio/speaker-diarization.html`（DER 公式 / Hungarian / ±0.25s collar / JER 对少数说话人）、`pixldata.com/blog/audio-annotation-guide`（三分量 + 必须随数报 collar 与是否计重叠）、`www.aicassindra.com/blogs/audio/audio_diarization.html`（`pyannote.metrics` `detailed=True` 分列三分量、参考集自建 20–40 分钟/类型）。
- `theneuralbase.com/whisper/learn/beginner/hallucination-on-silence` — HTTP 200 / 214,348B，命中 no_speech_prob(35 处)·0.65·50+·fasterwhisper·calibrat·configurable；`blog.gitcode.com/de1aa2f5d03a23c8702e30a0a93af759.html`（五道防线 + 幻觉正则 + 词级范围过滤）；`transcribeall.io/knowledge/how_do_you_prevent_whisper_hallucinations...`（解码参数、条件关闭、段级均值盲区）。

## 十一、响度归一化：LUFS 不是「把峰值调到 0」，报数值必须带测量口径（2026-11-15 r747B 实拉，3 独点）

> 适用：音频转写前的增益/归一化、播客与字幕交付、多段录音拼接、TTS 输出电平。与 §r708C 分离评测（DER / 幻觉阈值）互补：那条管「转得对不对、谁在说」，本节管「进 ASR 之前被按什么口径改过电平」。

### 11.1（r747B-1）★峰值归一化是「响度战争」的成因；BS.1770 只定义测量，R128 在其上叠加门控 / LRA / 目标电平，三层不可混
EBU 官方《EBU R 128 – the EBU loudness recommendation》（2010-09，"10 things you need to know"，2 页 5,417 字符，本地 pypdf 逐字）点 1 逐字：「audio levelling based on **loudness, not peaks**」「Audio signal normalisation based on **peaks** has led to more and more dynamic compression and a phenomenon called the '**Loudness War**'. The problem arose because of misuse of the traditional metering method (**Quasi Peak Programme Meter – QPPM**) and the extended headroom due to digital delivery」；点 2 逐字「**ITU-R BS.1770 defines the basic measurement, EBU R 128 builds on it and extends it**」「It introduces '**K-weighting**', a simple weighting curve that leads to a good match between subjective impression and objective measurement. EBU R 128 takes BS.1770 and extends it with a **gating function**, the descriptor **Loudness Range (LRA)** and the **Target Level: -23 LUFS**」；点 3 逐字「Gating of the measurement is used to achieve better loudness matching of programmes which contain **longer periods of silence**. Longer periods of silence lead to a lower measured loudness level. **After subsequent loudness normalisation such programmes would end up too loud**」「a relative gate of **8LU** (Loudness Units; 1LU is equivalent to 1dB) below the ungated loudness level」。Quantara 官方页逐字把分工再拆一层：「**BS.1770 defines the measurement method. EBU R128 is a broadcast recommendation built on BS.1770 that adds a target (-23 LUFS), a true-peak ceiling (-1 dBTP) and the LRA descriptor**」「Streaming platforms use their own targets (around -14 LUFS) but **the same BS.1770 measurement underneath**」。
- **判据**：① 「按峰值拉到 -1dBFS」不是响度归一化，做增益前先问按的是 QPPM 峰值还是 LUFS，二者会导向相反的压缩量。② 三层分开记账：**测量算法（BS.1770：K-weighting + gating）／管理建议（R128：目标 -23 LUFS、容差、LRA、真峰上限）／分发平台目标（各家 -14 ~ -16 LUFS）**；换平台改的是目标值，不是测量算法，别把「-14 比 -23 响」当成算法不同。③ 长静音段会拉低未门控测量、归一化后整体变响 ⇒ 拼接含静音的录音（会议、播客、VAD 前后）必须按整段重算，不能逐段归一化再拼。④ 与 §四「长音频与分段」分工：那条管误差累积，本条管分段带来的电平漂移。

### 11.2（r747B-2）★K-weighting 两级 + 双门 + 400ms 块是「一个算法」，改任一环即换口径；门控值随标准版本漂移
Quantara 逐字：「BS.1770 first passes the audio through a **K-weighting** filter with two stages: a high-shelf pre-filter that gently boosts high frequencies (roughly **+4 dB above ~1.5 kHz**, modelling the head-related boost), and a **RLB high-pass** that rolls off very low frequencies (around **38 Hz**)」；流水线逐字「**1)** K-weight both channels; **2)** split into **400 ms blocks with 75% overlap**; **3)** compute mean-square power per block; **4)** apply the **-70 LUFS absolute gate** and the **-10 LU relative gate**; **5)** average the surviving blocks and convert to LUFS」；并逐字「Loudness Range (LRA) is derived **separately from the spread of 3-second short-term measurements**」「Many web meters approximate K-weighting with generic parametric-EQ (RBJ) biquads, which drift from the spec's exact filter — the deviation can reach **several tenths of a LU in the presence region around 3 kHz**」「Quantara Music measures to the **BS.1770-4** standard, so the reading matches it at both 44.1 kHz and 48 kHz」。tonalux 逐字补机制：「The standard explicitly models the head as a **rigid sphere**」「The absolute gate discards any 400 ms block that measures below -70 LUFS … First, the algorithm computes the absolute-gated average across all non-silent blocks. Then it sets a threshold **10 LU below that average** and recomputes」「you **cannot game the measurement by padding a loud master with silence**」。
- **判据**：① **门控值带版本号**：EBU 2010 官方 flyer 记为**单级相对门 8LU**（below the ungated loudness level）；现行 BS.1770-4 系**两级门**（绝对 -70 LUFS + 相对 10 LU below the absolute-gated average）。两处数字与基准都不同，属标准演进，报测量值必须写「按哪一版、哪一门控」，**禁止跨版本互抄 8 与 10**。② LRA 不是集成响度、也不是峰值范围，它从 3s short-term 分布统计得出；EBU 官方点 4 逐字「'Loudness Range' is a tool to assess if a programme fits the tolerance of the transmission chain and target audience and if **dynamic compression is needed**」「A broadcaster can establish a **maximum LRA value** for specific genres and transmission platforms」⇒ LRA 是「要不要压动态」的判据，不是合格线（官方未给通用上限）。③ K-weighting 近似实现会有数十分之一 LU 偏差 ⇒ 跨工具/跨采样率的 LUFS 数字不可直接比较，与 §r708C「没写 collar 的 DER 不要跨来源比」同构但对象不同（那条是时间容差，本条是滤波器与门控口径）。

### 11.3（r747B-3）★M/S/I 三个时间常数是三种不同测量对象；真峰是采样间峰，0 dBFS 不等于安全
EBU 官方点 5 逐字「There are **three time constants which differ in the integration time: Momentary (400ms), Short-term (3s) and Integrated (from start to stop; the whole programme/item)**. These three meters are abbreviated **M, S and I**」「the result of a loudness measurement is a **Loudness Level, abbreviated L_K, the value is expressed in 'LUFS'**」「'M' and 'S' are commonly used in stereophony for 'Mid' and 'Side'. To distinguish the integration times 'Momentary' and 'Short-term', the versions '**ML_K**' and '**SL_K**' (as well as '**IL_K**') may be used」；并逐字「A tolerance of **± 1 LU** is generally acceptable」（与 -23 LUFS 目标配套）。Quantara / tonalux / electronicsguide 三域交叉真峰：逐字「**True peak measurement, specified in ITU-R BS.1770, addresses inter-sample peaks that exceed the maximum sample value when the digital signal is reconstructed as analog**」「R128 specifies a maximum true peak level of **-1 dBTP** (decibels true peak relative to full scale), preventing **overload in analog stages and lossy codecs**」「a master that peaks at exactly **0 dBFS can still audibly clip after encoding**」；tonalux 另记平台差异「**YouTube: -14 LUFS (attenuation only, does not boost quiet masters)**」「A track at -18 LUFS gets boosted 4 LU on Spotify. A track at -8 LUFS gets attenuated 6 LU」。
- **判据**：① 报响度固定写「M / S / I 哪一档 + 窗口 + 目标值 + 容差 + 标准版本」，只给一个数字「-16 LUFS」无法判断是瞬时冲高还是整段合规。② **样本峰值 0 dBFS 与真峰 -1 dBTP 是两个量**：转码/重采样后出现削波，查的是 dBTP 不是 dBFS；ASR 前若做重采样，须在重采样后重测真峰。③ 平台归一化可能是「只衰减不提升」（YouTube）或双向增益（Spotify）⇒ 「我传到平台会自动变正常」不成立，过静的素材不会被救；本地交付要自己按目标测。④ 与 §七「坑与护栏」分工：那条管解码幻觉与静音过滤，本条管电平与感知响度；VAD 裁掉静音会改变 gating 结果，两处须联读。

**提升层**：感知 / 音频工程 / 交付验收。触发词：LUFS、EBU R128、BS.1770、K-weighting、绝对门 -70 LUFS、相对门 8LU vs 10 LU 版本差、M/S/I 三时间常数、LRA 不是合格线、-23 LUFS ±1 LU、dBTP 真峰、inter-sample peak、QPPM 响度战争、只衰减不提升。

### r747B 来源与判非（2026-11-15 实拉，逐字核验）
- `https://tech.ebu.ch/docs/events/ibc10/presentations/ebu_ibc10_r128.pdf`（**EBU 官方**，2010-09，"10 things you need to know about EBU R 128"）— **curl HTTP 200 / application/pdf / 403,445 B**，WebFetch 对 PDF 返回「non-text resource, bytes dropped」故按 r731 先例改本地下载 + pypdf 逐字提取（2 页 5,417 字符）：点 1 QPPM / Loudness War、点 2 K-weighting 与 BS.1770→R128 扩展关系、点 3 8LU 相对门与长静音后果、点 4 LRA 定义、点 5 M/S/I 三时间常数与 L_K/ML_K/SL_K/IL_K、-23 LUFS 与 ±1 LU。**第一独立域（标准组织官方一手）**。临时 PDF 已在本批收尾删除，未入仓。
- `https://www.quantaramusic.com/learn/bs1770-loudness`（Quantara Music《What is BS.1770 loudness?》，Updated 26 October 2026）— **WebFetch 200 全文逐字**：K-weighting 两级（+4dB@~1.5kHz / RLB@~38Hz）、五步流水线、400ms 75% overlap、-70 LUFS 绝对门 + -10 LU 相对门、LRA 由 3s short-term 分布导出、BS.1770-4、RBJ biquad 近似偏差、BS.1770 vs R128 分工、自列 ITU / EBU / Spotify 官方参考链接。**第二独立域（厂商技术文档一手，产品立场登记，不作唯一来源）**。
- `https://tonalux.org/blog/lufs-ebu-r128-streaming-normalization-explained`（《LUFS Explained》）、`https://www.electronicsguide.net/applied-electronics/audio-and-acoustics/specialized-industry-applications/broadcast-engineering-systems`（《Broadcast Engineering Systems》）、`https://www.endlesswiki.com/wiki/EBU_R128` — **WebSearch 快照逐字**：K-weight 刚球模型、两级门机制、不能靠填静音刷分、BS.1770-4 两级门、ATSC A/85 -24 LKFS 与 dialog-gated、-1 dBTP、各平台目标表（Spotify -14 / Apple -16 / YouTube -14 只衰减 / Deezer -15）、R128-2017 短内容修订、libebur128 / FFmpeg ebur128。**第三、四独立域（工程教学与百科，交叉不作唯一结论来源）**。
- `https://www.itu.int/rec/R-REC-BS.1770-5-202311-I`（ITU-R BS.1770-5, 2023-11）与 `https://tech.ebu.ch/publications/r128`（EBU R 128 正式发布页）— 由 Quantara 官方 Sources 段给出，用于核对标准编号与版本，**本轮未单独 WebFetch 全文**，如实登记为标准索引而非一手正文。
- **判非**：窄串全库 `SKILL.md` 精确扫描（97 文件）— `LUFS` / `EBU R128` / `BS.1770` / `K-weighting` / `relative gate` / `absolute gate` / `dBTP` / `Loudness Range` / `Integrated` / `-23 LUFS` / `inter-sample` / `QPPM` / `gated loudness` / `ReplayGain` / `LKFS` **全 0 命中**；`gating` 6 命中在 `agent/agent-guild`（入站门控）/ 豆包自留地（准入门）等异命题、`Short-term` 1 命中在 `defaults/wb-context-compressor`（豆包自留地）、`LRA` 2 命中为子串噪声（豆包自留地与 execute-discipline 的缩写），均非响度测量。**豆包自留地 WB 0 落地**。与本技能 §r708C（DER 三分量 / collar / no_speech_prob / 幻觉过滤）结论不复用：那条管分离与转写正确性，本条管电平与感知响度；A/C 两轮信源域与结论亦不复用。
- **未采纳**：各流媒体平台的具体目标值随时间可能调整（表中数值仅作 2026-11-15 快照，不作为长期事实）；ATSC A/85 与 CALM Act 的法规合规流程、EBU Tech 3341/3342 的仪表实现细节、母带处理与压缩器参数，属专门工程或地域法规，只取可迁移的测量口径判据。**EBU 官方 2 页 flyer 中 `true peak` 0 命中**，-1 dBTP 由三域交叉得到，未冒充官方 flyer 一手。

## 声音事件检测（SED）评测口径：三族分数不跨族比、参数冻结才可复现

> r774B（2026-11-19）实拉。上文 DER/JER/WDER 管「谁在说话」的说话人日志，响度节管「多大声」，本节管「出现了什么声音事件、何时开始结束」的评测——三类问题用三套度量，互不替代。

### 13.1（r774B-1）三族评测：segment-based、event-based(collar)、PSDS 是三种不同工作
- segment-based（DCASE 2017 / 2024 Task4）：把时间切成 1 秒段，逐段判类是否 active，算 micro/macro F1 与 error rate（ER=替换+删除+插入 / 参考事件数，借自语音识别）；阈值固定 0.5。
- event-based collar F1（DCASE 2018–2020）：整事件匹配，onset 容 200ms、offset 容 200ms 或事件时长 20% 取大者；**分数依赖所选阈值与 collar**，不同论文的 F1 数字不可直接比。
- PSDS（polyphonic sound detection score，2021–2023 主指标）：按**事件交集**而非固定 collar 匹配，对主观标注边界更稳；扫 50 个工作点（0.01–0.99 线性）画 TPR–每小时误报 ROC 压成一个数。DCASE 2024 又引入 threshold-independent PSDS（用带时间戳的分数而非检出事件）。
- **判据**：① 报 SED 分数必须写「哪一族 + 阈值/工作点 + collar 或交集参数 + 在哪个数据集哪个类集上算」；② segment F1 高不等于 event F1 高（一个跨多段的事件在 segment 里被重复计），两者分开报；③ DCASE 自己声明 2023 threshold-independent PSDS 与往年不可直接比，跨年分数别并排行。

### 13.2（r774B-2）PSDS 参数是策略声明不是可调旋钮；ranking 是多指标拼接
- DCASE 2024 Task4 官方逐字参数：DTC（Detection Tolerance criterion）0.7 / GTC（Ground Truth intersection）0.7 / αST（类间不稳定代价）1 / αCT（交叉触发对用户代价）0 / e_max 100。Collar F1 对照指标：onset 200ms / offset 200ms 或 20% 取大，阈值 0.5。
- 早期两年两场景：scenario1（DTC/GTC 0.7，快速反应如报警，定位重要）vs scenario2（DTC/GTC 0.1 + cttc 0.3，避免类间混淆、反应时间次要）；最终排名 = 两场景 PSDS 各按 baseline 归一化后相加。DCASE 2024 ranking = pAUC_M（MAESTRO 集/类）+ PSDS（DESED 集/类）**之和**——两个不同数据集、不同类集、不同指标的拼接。
- **判据**：① 引用 PSDS 必附 DTC/GTC/αCT/αST/e_max 五参数，缺一即不可复现；② 排名分是拼接量，不能反推「PSDS 高多少」的单项改进；③ 要快响应用 scenario1 参数、要少混淆用 scenario2，别拿一套参数声称覆盖全部应用。

### 13.3（r774B-3）参考标注主观、合成训练与真实评测分离、多 run 标准差与能耗入账
- aiunderstanding 逐字：参考标注有主观性（DCASE 组织者查 AudioSet 片段发现不少并不含所标事件）；合成声景训练的模型在真实录音上吃力；短/轻/重叠加事件与稀有类易漏；**分数依赖 metric/collar/threshold，跨论文常不可比**。
- DCASE 2024 强制：三次不同初始化独立训练的输出分数（处理后+未处理）都要交，以评模型性能**标准差**；置信区间基于三次 run + 评测集 bootstrap。能耗（kWh，CodeCarbon，训练 + devtest 推理）当年起**强制上报**，另加 MACs/10s（THOP）作为计算复杂度补充。
- **判据**：① 单 run 分数不当结论，至少三次初始化报标准差/置信区间；② 合成集成绩与真实集成绩分开报，排名只看真实集；③ 能耗与算力作为独立列，别把「PSDS 提升」与「用了多少算力」混成一个数。

### r774B 来源与判非（2026-11-19 实拉，逐字核验）
- `https://dcase.community/challenge2024/task-sound-event-detection-with-heterogeneous-training-dataset-and-potentially-missing-labels`（DCASE 2024 Task4 官方）— **WebFetch 200 全文逐字**：segment 五指标、PSDS 五参数（DTC .7/GTC .7/αST 1/αCT 0/e_max 100）、collar 200ms/20%、ranking=pAUC_M+PSDS、三 run 标准差、能耗强制、MACs。**第一独立域（赛事官方一手，主证据）**。
- `https://www.emerald.com/atsip/article/13/1/1/1331409/Sound-Event-Detection-A-Journey-Through-DCASE`（Emerald 综述《A Journey Through DCASE Challenge Series》）— **WebSearch 逐字快照**：2013 AEER→2016 total ER→2017 segment ER→2018–2020 event F1 collar→2021–22 PSDS 50 工作点两场景→2023 threshold-independent PSDS、scenario1/2 定义、排名归一化相加。**第二独立域（学术综述一手，年份谱系交叉）**。
- `https://dcase.community/challenge2020/task-sound-event-detection-and-separation-in-domestic-environments` + `https://dcase.community/challenge2022/task-sound-event-detection-in-domestic-environments` + `https://aiunderstanding.org/learn/sound-event-detection`（DCASE 官方历年页 + 技术长文）— **WebFetch/WebSearch 逐字快照**：PSDS 三形态（cross-trigger/macro）、αCT/αST 含义、PSDS 由 Bilen 等 ICASSP 2020 提出、标注主观性、合成vs真实、跨论文不可比、手算 F1 例。**第三～五域（官方历年/技术长文，交叉登记）**。
- **失败与降级如实登记**：Mesaros 2016《Metrics for Polyphonic SED》原论文（MDPI）只取 DCASE 官方页转述的摘要与书目，未直读全文；Bilen PSDS 原始论文只取技术长文转述，不冒充已读全文；DTC/GTC 数值挂 DCASE 2024 官方口径，scenario 参数挂 2022 官方口径，不混为同一套。
- **判非**：窄串全库 `SKILL.md` 精确扫描 —— `sound event detection` / `声音事件检测` / `PSDS` / `polyphonic` / `Detection Tolerance` / `event-based F1` **全 0 命中**；`collar` 命中在 `engineering/pi-perception` 与本节上文 r708C（都是**说话人日志 diarization** 的 forgiveness collar，异命题：那是「谁在说话」，本轮是「什么事件、交集匹配」）。按 rules/07 四态判「**优＝加厚现有 `media/pi-audio`**」，SED 是音频评测的自然延伸，不重述上文 DER/WER/响度。PI 模块记忆前 17 条结论不复用。豆包自留地 WB 0 落地。与 r773(OI/EI/SI)/r772(AI/VI/DI) 六模块结论不复用；A/C 两轮结论亦不复用。
- **未采纳**：sed_eval / sed_scores_eval / psds_eval 具体实现、CodeCarbon/THOP 工具用法、各参赛队排名分数、SCM 类教程细节 —— 属工具/赛事结果，不迁移为通用判据。

## 十四、语音增强/分离的客观评测：保真、质量、可懂度三件事不可互证（PI · r778B 2026-11-20 实拉，≥2 独立域交叉）

### 14.1（r778B-1）★三类指标测三个对象，必须成组报，禁单指标排名跨族比
SI-SDR（Scale-Invariant SDR）测信号保真：对参考与估计做最优缩放后再比，增益失配不该拖垮一个好分离，是源分离主指标；SDRi/CI-SDR/SA-SDR/SIR/SAR 是其场景变体。PESQ（ITU-T P.862）与 POLQA（P.863）测感知质量：PESQ 只对电话线窄带验证过的损伤（codec artefact/丢包/加性噪声）可信，约 4 MOS 以上严重饱和，分不出「很好」和「极好」，新工作多改用 POLQA（授权，开源项目仍用 PESQ）。STOI/ESTOI 测可懂度：短时相关预测，「polish」判断或可懂度已 100% 时不可靠。综述明确推荐「report SI-SDR (or SI-SDRi) as the primary metric for separation accuracy, alongside traditional SDR ... PESQ for speech quality and STOI (or ESTOI) for speech intelligibility」，四件套覆盖信号保真 + 人类感知两面。判据：增强/分离报告至少给 SI-SDR + PESQ + STOI/ESTOI 三族，每族标口径（窄带/宽带、侵入/无参考）；只给一个数的排名不通过验收。

### 14.2（r778B-2）★指标排名随度量剧烈翻转；非侵入指标换域必须重验相关性，不能继承论文 PCC
CHiME-7 UDASE 官方结论：「the ranking of the methods varies a lot according to the chosen metric」——同一系统 SI-SDR 最好却在 TAS SI-SDR 最差之一。侵入指标与其 TorchAudio-Squim 非侵入估计的 Pearson 相关在 CHiME-7 UDASE 上只有 0.20–0.30，而原论文（Kumar 2023）报 0.95–0.98；原因是有监督非侵入模型训在 DNS Challenge 2020，泛化不到新域，「these ... estimates are not sufficiently reliable on the CHiME-7 UDASE data」。低 SNR 无人机噪声的可控主观实验再证：NISQA（学习型感知）、ESTOI（可懂度）与主观判断最一致，SI-SDR 次之，PESQ 较弱；「conventional objective metrics may fail to accurately reflect perceived speech quality」。判据：用 DNSMOS/NISQA/SQUIM 等无参考指标前，先在当前域做一次与主观或小样本侵入指标的相关性校验（PCC 明显低于文献值即判不可移植）；换数据集/语言/噪声类型视为换域，继承他人 PCC 是范畴错误。

### 14.3（r778B-3）★客观指标三种失效：域外、饱和、可 gaming；「质量相近」≠「感知相同」
AudioLab 归纳三种反复出现的失效：① 域外材料——PESQ 在电话线语音上验证，拿去评歌剧「you get numbers, but those numbers don't mean what they mean on phone-line speech」；经典指标天然带域，作者无意也不豁免。② 高端饱和——多数语音指标区分 bad/okay 好、okay/good 差，模型真好了指标就 plateau，dashboard 全绿却已退化。③ 可 gaming——「A model can learn to produce outputs that maximise PESQ without producing outputs that humans prefer.」感知差异/偏好与质量分是不同判据：论文实测 PESQ 的区分相关约 0.05、偏好方向约 0.31，SQUIM-STOI 两者约 0.62；两个信号质量评分相近仍可能被轻易区分，「质量相似不等于感知相同」，低相关不是指标无用而是测的不是一回事。判据：新品上线决策配一组主观听测（MUSHRA/ABX/MOS）做三角验证；任何单一客观指标不得直接当 go/no-go 门槛；指标分差须注明是否落在饱和区与域外区。

### r778B 来源与判非（2026-11-20 实拉，逐字核验）
- `https://hal.science/hal-04430786v1/file/CHiME_7_UDASE.pdf`（CHiME-7 UDASE 官方论文：ranking varies a lot / PCC 0.20–0.30 vs 0.95–0.98 / DNS Challenge 2020 训练不泛化 / TAS MOS 相对可靠；**WebFetch 被 Anubis 反爬拦截未取到正文**，以 WebSearch 返回的该 PDF 正文片段逐串登记，不冒充全文直读）
- `https://qmro.qmul.ac.uk/handle/123456789/131888`（QMUL / IEEE Signal Processing Letters 33:2470-2474 (2026) 论文摘要 WebSearch 逐字：低 SNR 无人机噪声下 NISQA/ESTOI 与主观最一致、SI-SDR 次之、PESQ 较弱、metric 间 substantial inconsistencies）
- `https://arxiv.org/pdf/2508.10830`（arXiv 2508.10830 语音分离综述 §B Objective Metrics WebSearch 快照逐字：SI-SDR/SDRi/CI-SDR/SA-SDR/SIR/SAR 家族分工、PESQ/POLQA/STOI/DNSMOS 三层面、四件套推荐、「no single metric is suitable for all speech separation tasks」、PESQ-NB 宽带/音乐不准）
- `https://audiolab.tools/insights/evaluating-audio-ai-models`（AudioLab 评测指南 WebSearch 快照逐字：主观/客观 2x2、PESQ ~4 MOS 饱和、域外/饱和/gaming 三失效、「wrong evaluation strategy can let you ship a regression that 80% of listeners notice while every metric glows green」）
- `https://nanless.github.io/audio-paper-digest-blog/posts/2026-10-29-perceptual-differences-and-preferences-in-speech-2610-36892`（arXiv 2610.36892 中文精读 WebSearch 快照：区分相关 PESQ 0.05 vs SQUIM-STOI 0.62、偏好方向 0.31 vs 0.62、质量相近≠感知相同、众包变异局限）
- **判重**：全库 SKILL.md 精确扫描 `PESQ`/`STOI`/`SI-SDR`/`语音增强`/`speech enhancement`/`depth estimation` 全 0 命中；`FID` 22 命中均为图像生成/多模态生成语境异命题。本技能 §r708C 是说话人分离评测、§十三是声音事件检测（SED，检测命题），本轮补信号质量/可懂度（增强与分离命题），正交不复用。豆包自留地 WB 0 落地。

## 十五、语音反欺骗评测：ASV 任务看 t-DCF、无 ASV 看 EER，泛化失败是主战场（PI · r782B 2026-11-20 实拉，≥2 独立域交叉）

> 与 §五说话人分离（「谁在说话」）/ §十三 SED（「什么事件」）/ §十四语音增强（质量保真）分工：本节是「这段语音是真人还是伪造/重放」的 countermeasure（CM）评测。ASVspoof 2021 官方计划 + 结果总结论文逐字核验。

### 15.1（r782B-1）★指标按任务选：有 ASV 的 LA/PA 看 t-DCF，无 ASV 的 DF 看 EER，两个数字不可跨任务比
ASVspoof 2021 三任务（官方 WebFetch 逐字）：logical access（LA，TTS/VC 合成语音经电话与 VoIP 编解码传输）、physical access（PA，真实空间录制重放、不同质量回放设备）、speech deepfake（DF，TTS/VC 伪造但**不含说话人验证 ASV**）。指标分工（官方原文）：LA 与 PA 用 **minimum tandem detection cost function（min t-DCF）**——因 CM 与未受保护的 ASV 是串联工作；DF 因没有 ASV 系统，revert to **equal error rate（EER）**（误接受=误拒绝的点），EER 是「best achievable (Bayes) error rate 的上界」。t-DCF 公式（结果论文 Eq.1 逐字）：`t-DCF = min_τ {C0 + C1·P_miss(τ) + C2·P_fa(τ)}`，P_miss/P_fa 是 CM 的漏检/误报率，C0/C1/C2 由预置成本、先验**与 ASV 性能**共同决定——C0/C1 依赖 bonafide 上 ASV 表现、C2 随 ASV spoof false alarm rate 线性增长（**攻击对 ASV 危害越大、CM 误报罚得越重**）。关键差异：2019 丢弃的 C0（ASV floor＝零错误 CM 时的 t-DCF，反映 ASV 自身错误）2021 **保留**；C 参数 LA/PA 不同、progress/eval 分区也不同——是「moving target metric」反映串联系统的设计目标随 ASV 变化。判据：报反欺骗分数必写任务（LA/PA/DF）+ 指标（min t-DCF/EER）+ ASV 工作点与 C 参数，LA 的 t-DCF 与 DF 的 EER 不可比高低。

### 15.2（r782B-2）★progress 到 eval 的 EER 崩塌是泛化失败信号，不是「方法更好」的证据
结果论文（alphaxiv 逐字）：DF 任务 progress 阶段部分系统 EER 低至 **0.10%**（近完美），最终 evaluation 最佳系统 T23 却为 **15.64%**（基线 22.38%）——巨大落差是**对 progress 分区严重过拟合**的信号：eval 分区含 100+ 未在 progress/ASVspoof2019 训练集出现的生成算法与 mp3/m4a/ogg 有损压缩。LA 相对乐观（最佳 min t-DCF 0.2177 vs 基线 0.3445，对应 EER 1.32%），PA 难（0.6824 vs 0.9434）。统计显著性：DF 顶级系统间差异多不显著（同样的泛化瓶颈），LA/PA 顶级层有清晰显著层级。判据：反欺骗「领先」必须在**独立 eval 分区**（新攻击算法+新压缩）复现才认；progress/开发集上的低 EER 不得外推；报分附显著性分组，别把不显著的差距当排序。

### 15.3（r782B-3）★四条基线是评测锚点，报分须声明数据分区与是否用增强
官方四条可复现基线（github.com/asvspoof-challenge/2021）：B1=CQCC-GMM、B2=LFCC-GMM、B3=LFCC-LCNN（含 LSTM）、B4=RawNet2（端到端原始波形）。**全部仅在 ASVspoof 2019 数据上训练、无数据增强**，为参赛系统提供公平比较点；2021 明确鼓励参赛者**自带**训练/开发数据并用数据增强模拟信道变化（因不发布新训练/开发数据、只发新评测数据）。ASV 后端是 x-vector（VoxCeleb2 训练）+ PLDA，在目标-nontarget EER 阈值工作（pool 该任务该分区全部 bonafide 段求得）。判据：复现/对比须写基线编号、训练数据版本（2019）、是否增强、ASV 工作点口径；「我们比基线好」但换了训练数据或增强策略的比较不成立。

### r782B 来源与判非（2026-11-20 实拉，逐字核验）
- `https://www.asvspoof.org/index2021.html`（ASVspoof 官方 WebFetch 200 全文逐字：三子挑战 LA/PA/DF、DF「no ASV」、4 基线名、t-DCF 参考实现、evaluation plan v0.4、无新训练/开发数据只发新评测数据、鼓励自带数据+增强）——第一独立域·挑战官方。
- `https://www.asvspoof.org/asvspoof2021/asvspoof2021_evaluation_plan.pdf`（官方 evaluation plan WebSearch 全文逐字 TL;DR：LA/PA 用 slightly revised t-DCF、DF 用 EER 及原因、三任务定义、2021 目标=信道鲁棒/真实空间/数据增强/非 ASV deepfake 场景）——第二独立页·官方一手（PDF WebFetch 未取正文、以 WebSearch 全文片段逐字登记，如实标注）。
- `https://arxiv.org/pdf/2109.00537v1`（ASVspoof 2021 结果总结论文 WebSearch 逐字：t-DCF Eq.1 含 C0 保留与 C2 随 ASV spoof FA 增长、moving target metric、EER 作为 Bayes 误差上界、x-vector+PLDA 后端、LA 0.2177/PA 0.6824/DF 15.64% 结果、progress 0.10%→eval 15.64% 泛化崩塌、显著性分组）——第三独立域·一手结果论文。
- `https://www.alphaxiv.org/abs/2109.00537`（中文逐字：100+ 生成算法、mp3/m4a/ogg 压缩、EER 定义与四基线）——交叉佐证。
- **判重**：全库 SKILL.md 精确扫描 `ASVspoof`/`anti-spoof`/`反欺骗`/`minDCF`/`t-DCF`/`EER`/`equal error rate` 0 命中（PI 唯一命中为本节来源段的 `engineering` 子串误命中）。本技能 §r708C 说话人日志、§十三 SED、§十四增强均异命题。豆包自留地 WB 0 落地。
