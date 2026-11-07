---
name: media/pi-audio
description: 音频感知（Audio/Speech Perception）。当需要把录音/会议/播客/通话转成文字、标"谁在什么时候说了什么"、生成字幕、做语音合成（TTS）、识别音频事件（警报/音乐/故障声）或理解音频内容时调用。提供 ASR 选型（AudioTranscribe 本地/Whisper API/faster-whisper/whisperX）、长音频分段并行、VAD 去静音防幻觉、pyannote 说话人分离与时间戳对齐、LLM 后处理、SRT/VTT 输出、TTS 与隐私护栏。不用于音视频格式转码（走 rg-ffmpeg-tools）、图像理解（走 multimodal-intelligence）。
module: PI
modules: PI
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
