---
name: pi-perception
description: 环境感知与多模态（Perception Intelligence）。当任务需要先"看清当前真实环境再动手"——读取/操作真实桌面与文件系统、屏幕截图理解、图像/音频/视频多模态生成与处理、说话人分离与音频转写指标评测、Windows 原生应用自动化与 GUI 操控、计算机视觉理解、视觉输入分辨率与坐标保真、图像 token 计价口径核对时使用。是 13 模块中 PI 的载体。
version: 1.2.0
module: PI
modules: PI
---

# PI · 环境感知与多模态（Perception Intelligence）

> 本技能是 13 模块中 **PI（感知智能）** 的载体。完整经验日志在 D 盘：`D:\腾讯AI\WorkBuddy数据\module-memory\PI\MEMORY.md`。关联子技能：`engineering/multimodal-intelligence`、`media/image-processor`、`media/pi-audio`、`media/rg-ffmpeg-tools`、`media/wb-visual-gen`、`system/computer-use-windows`、`system/win-native-app-automation`、`system/winapp-ui-automation`。

## 一、真实环境优先（本模块最硬的一条）

- 动手前先确认"用户所见真实环境"在哪，**沙箱视图 ≠ 真实环境**：
  - Bash/Git-Bash 与 Python 沙箱把 `C:\Users\<user>\Desktop` **虚拟化**，经沙箱写该绝对路径，文件落不到用户真实桌面（用户看不到）。
  - ⇒ 任何"交付到桌面"必须用**原生 PowerShell**：`$d=[Environment]::GetFolderPath('Desktop')` 取当前真实值 + `Copy-Item -Force` 落盘；不得在 Bash/Python 里直接写桌面绝对路径。
- 桌面路径每次现取不缓存（OneDrive 接管等会让旧值失效，rules/01 旧值已过时不可信）。
- 屏幕 / 截图理解、GUI 自动化优先用专用子技能与 Windows 原生能力，不靠猜坐标。

## 二、触发与协作

- 何时加载：要操作真实桌面 / 文件、要理解屏幕或图像、要做音视频生成 / 处理、要 Windows 应用自动化时。
- 与 OI（编排）：环境操作是 agent 对外动作的一类；与 SI（安全）：操作个人文件前先过安全闸。

## 三、说话人分离评测方法论（实拉 r708C，2026-11-08）

> 来源：`pyannote.ai/blog/how-to-evaluate...`（200/464,580B，命中 Missed Speech / False Alarm / Confusion / collar / overlap）；`pixldata`、`aicassindra` 交叉；`theneuralbase.com`（200/214,348B，no_speech_prob 35 处命中）；`gitcode` / `transcribeall` 交叉；落地 `media/pi-audio/SKILL.md` →1.1.0 末节。

- **（1）DER 是三分量之和，只报总数不知道修哪**：DER = (Missed + False Alarm + Confusion) / 总参考语音时长。三分量指向**不同修法**——Missed→VAD/重叠处理、False Alarm→噪声门限、Confusion→嵌入聚类。⇒ 用 `detailed=True` 分列报告，禁止只给一个总 DER 数字。
- **（2）缺 collar 与重叠口径的数字不可跨来源比较**：报告必须同时写明 forgiveness collar（常用 ±0.25s；注意 pyannote 的 collar 参数是**总宽**，0.5≈双边 0.25；DIHARD 用零 collar）与**重叠语音是否计分**。两项缺一，数字没有可比性。
- **（3）指标按用途选，均值会掩盖失效**：
  - DER 按时长加权，对少数说话人不敏感 ⇒ 少数说话人场景并报 **JER**（每说话人等权 Jaccard，DIHARD 引入）；下游是带说话人标签的转写稿用 **WDER**（按词界）。
  - 必须看**逐文件分数**并核对估计说话人数：均值会掩盖"一类录音三倍失效"；一个被拆成两人的说话人几乎不抬 DER，却毁掉分人摘要。
  - 标签置换歧义先用 **Hungarian 算法**求最优映射再算分。
- **（4）引擎迁移使阈值过滤规则整体失效**：`no_speech_prob` 仅 OpenAI whisper 库 `transcribe()` dict 输出提供，faster-whisper / streaming API / whisper.js 都没有 ⇒ 换引擎后原过滤规则**不可移植**，须用自有信号重测。
- **（5）阈值不可抄，须按本域分布定**：不抄 0.5；取 50+ 份本域真实转写、人工标"静音区幻觉 vs 真实语音"、画分布后选阈值（语音密集域 0.6–0.75，示例 0.65），且过滤须**可配置**（音频编辑、带时间空档的字幕要保留静音段）。段级平均置信度会掩盖段内一整句臆造，须下钻**词级**。

## 四、感知层通用纪律

- 多模态输入（图/音/视频）先分辨"内容层"与"元数据层"：截图里看到的是渲染结果，不代表文件真实属性（与桌面虚拟化同构——**看到的 ≠ 真实的**）。
- 评测类输出永远带三件套：口径定义、比较前提（collar/重叠计不计）、逐样本明细，否则数字不可复核。

## 五、视觉输入保真与坐标回算（实拉 r732A，2026-11-11）

> 来源：Anthropic 官方 `platform.claude.com/docs/en/build-with-claude/vision` + 中文版（WebFetch 被地区重定向，改由搜索结果取官方正文逐串核验；`.md` 直取返回 HTML 壳无正文，如实登记）；OpenAI 官方 `platform.openai.com/docs/guides/images-vision` + `help.openai.com` 镜像正文（WebFetch 遇 Cloudflare 拦截）；`awesomeagents.ai/guides/ai-vision-image-resolution-limits`（2026-03-29，WebFetch 200 全文）；`appscale.blog`《The Resize Is the Price》（2026-10-31，WebFetch 200 全文）。四独立来源交叉。

- **（r732A-1）服务端静默降采样改写了感知输入，不是模型幻觉**：官方标准层长边 ≤1568px / 1568 tokens，高分辨层（Claude 4.7+ 自动启用、无需 opt-in）2576px / 4784 tokens；超限按宽高比缩小并在底/右 pad 到 28 的倍数；硬上限 8000x8000，单请求 >20 图时降到 2000x2000。4K 截图里 12px 标注缩到约 3px ⇒ 模型"答错"是**物理读不到**。⇒ 感知结论必须声明"模型实际看到的分辨率"而非上传分辨率；正确动作是客户端自己按可控插值预缩放，或 **crop 局部再送**（裁剪去 token 不丢细节，缩放全图丢细节），不让服务端替你决定。
- **（r732A-2）坐标输出锚在缩放+padding 后的图上，必须反算**：官方逐字 "they will be expressed with respect to the resized/padded image and will need to be rescaled/translated accordingly client-side based on the original and resized dimensions"。⇒ GUI 点击 / bbox 类任务拿回坐标后，必须按「原图尺寸 + 缩放后尺寸 + padding 量」做仿射回算，否则系统性点偏；且 patch 粒度因厂商而异（28px / 32px / 512px tile），**换算规则不可跨厂商复用**。与 `system/computer-use-windows` 的 `Screenshot Coordinate Scale` 互补：那条用宿主给的缩放因子，本条解释因子从哪来。
- **（r732A-3）计价口径随版本漂移，且 tool_result 截图是拒绝而非缩放**：`width*height/750` 已被 `⌈w/28⌉×⌈h/28⌉` 取代；OpenAI 新模型用 32px patch × 模型 multiplier（旧 gpt-4o/4.1 才是 2048→768→512 tile、85+170×tiles）；Gemini 是固定桶 280/560/1120/2240。同一 1920×1080 截图跨厂商/档位 280–2700 tokens 近 10 倍 ⇒ **参数族必须标型号+日期**（与 r715B 缓存档位分裂同构）。普通图像超限自动缩小，但 **computer-use / browser-use 的 `tool_result` 截图超限直接报验证错误**，须应用侧先 resize 或设 `transformations` 显式控制 ⇒ 两条通路混用会让 GUI 自动化整轮失败。

## 六、来源

- pyannote.ai/blog/how-to-evaluate-speaker-diarization（DER 三分量 / collar / overlap / JER / WDER）
- theaicompendium.com/8-audio/speaker-diarization.html（JER / Jaccard 交叉）
- theneuralbase.com（no_speech_prob / 0.65 / 50+ / configurable）
- pixldata / aicassindra / gitcode / transcribeall（交叉验证）
- 本会话实测：沙箱桌面虚拟化（2026-11-08 交付事故复盘）
- r732A：Anthropic Vision 官方文档 + OpenAI images-vision 官方文档（均经拦截，正文由搜索快照与镜像核验）+ awesomeagents.ai 2026-03-29 + appscale.blog 2026-10-31
