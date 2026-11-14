---
name: wb-media-forensics
description: 视频 / 图片类内容的取证与提取（反爬短链 → 拿到内容本体 → 抽帧读图）。当用户发来视频分享链接（抖音 / 快手 / B站 / 小红书 / 视频号短链）、要求"看看这个视频讲了什么""视频里推荐的工具/仓库是什么"、页面被反爬拦住拿不到正文、或视频没有可用字幕接口时使用。四步链路：短链解析 → Edge 无头渲染取播放地址 → 下载 + 本地解码抽帧 → 拼联络表多模态读图。触发词：抖音、快手、B站、小红书、视频链接、看看这个视频、视频讲了什么、逐帧、逐帧分析、口播、字幕、抓视频、video frames、media forensics。
agent_created: true
version: 1.3.0
module: VI
modules: VI
---

# wb-media-forensics（媒体内容取证：先取画面，再下结论）

**硬规则：画面 > 字幕 > 标题 > 评论区。** 拿不到正文时**先逐帧读图**（我本身是多模态），不要用标题 + 评论区的弱证据先下结论。
> 教训（2026-09-12，真实发生）：抖音视频任务里先用标题 + 评论区推断"视频主张 = 用 Skill 定框架"，改完技能、写完报告才去逐帧——结果画面显示视频讲的是具体仓库 `mattpocock/skills`，首轮结论错误。**有更强的证据手段却不用 = 违反证据优先。**

## 一、短链 → 真实地址
```bash
curl -sIL -A "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" "<短链>" | grep -iE "^(HTTP|location)"
```
拿到 `iesdouyin.com/share/video/<aweme_id>` 或平台对应页 + ID。

## 二、反爬页面 → 取页面数据（不要硬爬官方 API）
抖音的 `iteminfo` / `comment/list` 等公开接口现已风控（返回空 / 403 / 需签名），`r.jina.ai` 代理同样无效。**可行路径 = Edge 无头渲染**：
```bash
"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" --headless=new --disable-gpu \
  --no-sandbox --virtual-time-budget=8000 --dump-dom "<分享页 URL>" > "<D盘tmp>/page.html"
```
- 页面数据在 `window._ROUTER_DATA`：定位后**按大括号配平**取出 JSON 再 `json.loads`
- 播放地址也可能直接出现在渲染后的 DOM 里，grep `douyinvod|mime_type=video_mp4|\.mp4`
- 连不上时先看 Edge 是否装在 `C:/Program Files (x86)/Microsoft/Edge/Application/`（另一处是 `Program Files`）

### 二·补：微信视频号（`weixin.qq.com/sph/<id>` 短链）——只有封面可取，视频流拿不到
实测（2026-09-19）：短链 301 → `https://channels.weixin.qq.com/finder-preview/pages/sph?id=<id>`。该页是 **QR 扫码登录墙**，结论明确：
- **可取**：封面图（公开 CDN，带 Referer `https://channels.weixin.qq.com/` 可直接下载）、发布时间（`.feed-create-time-wrap` → 如「2026年6月1日」）、画面右上/下方的**标题与字幕文字**（都在封面图里，读图即得）。
  - 封面 URL 在渲染后 DOM 的 `<img class="video-player" src="https://finder.video.qq.com/251/20304/stodownload?encfilekey=...">`；注意 HTML 里 `&amp;` 要还原成 `&` 再 curl。
- **取不到**：播放地址、视频本体、ASR 字幕。视频流由点击播放后凭登录态**动态签名**生成，DOM/`window.*`/内联 JSON 里都没有；`.qr-modal-overlay` 会拦截所有 pointer 事件（Playwright `element.click()` 超时；`eval_on_selector(e=>e.click())` 能绕过点击但 QR 弹层立刻重现、`<video>` 仍为空、无任何 video 流请求）。**别再反复重试，直接如实告知用户需要微信登录态。**
- 兜底：把封面图当 `wb-visual-gen` 不改、直接多模态读图（本次即靠封面读出了标题「用Agent找工作 这么炸裂么?」及一行字幕）；若需完整内容，请用户在微信里打开→转发/保存视频文件或录屏后发来。

## 三、下载 + 抽帧（本机无 ffmpeg 也能做）
1. 下载 mp4 **必须带 Referer**，否则 403：
   `curl -sL -A "<桌面端 UA>" -H "Referer: https://www.douyin.com/" "<播放地址>" -o "<D盘tmp>/v.mp4`
2. 本机无 ffmpeg → 用隔离 venv 的 **PyAV**：
   `"C:/Users/26719/.workbuddy/binaries/python/envs/default/Scripts/python.exe" -m pip install --quiet av pillow numpy`
3. 抽帧策略（省 token 的关键，别逐帧全读）：
   - **秒级采样 + 帧差去重**：只有相邻帧差异超过阈值才留（滚动字幕/静态画面不会重复占位）
   - 每帧缩到约 360px 宽，拼 **N×M 联络表**（实测 36s / 1024×576 → 26 帧 → 5 张 2×3 足够覆盖）
   - 先读联络表定位关键时段 → 再对关键秒**单独抽单帧放大细看**（命令 / 仓库名 / 报错文字）

## 四、读图、提取、归档
- 直接读取联络表（多模态），提取：屏幕上的工具名 / 仓库名 / 安装命令 / 字幕原文 / 网址
- 产物归档 `D:\腾讯AI\yt\outputs\<日期>_<主题>\`；临时 mp4 / HTML / 解码脚本落 `D:\腾讯AI\yt\tmp`，**用完即清，不落 C 盘**

## 反模式
- 只拿到标题 + 评论区就下结论（弱证据 → 结论错，本技能的第 0 条硬规则就是为此）
- 反复重试已封的官方 API / 代理站（浪费轮次）
- 逐帧全量读图（烧 token）→ 应先联络表、后单帧
- 中文路径写 `.ps1` 脚本（编码损坏）→ 用 python 脚本 + 绝对路径参数
- 下载不带 Referer / UA 就直接判定"下不到"

## 与相邻技能的分工
| 场景 | 走谁 |
|---|---|
| 只是打开网页 / 取 DOM / 截图 / 填表 | `browser-automation`（本技能只在"要拿到媒体内容本体"时用） |
| 已拿到 transcript / 长文，要蒸馏成一堆可执行技能 | `cangjie-skill` |
| 要生成图片 / 视频（不是取证） | `wb-visual-gen` |
| 取到画面后，把里面的方法吸收进自身工作流 | 走当前标准流程（自动学习那套：先查同类 → 合并 / 新建 → git → memory） |

## 多模态处理纪律：视频抽帧采样 / 长视频三段式 / 图像上下文外置（来源：Ayi NEDJIMI《Multimodal RAG 2026》PDF + arXiv《Omni-Modal Long Videos》2512.16978 + arXiv《Cognitive-structured Multimodal Agent》2607.08497 实拉，与 §视觉提取三纪律 互补——那条管「从图提取文字/数据」，本条管「视频/图像作为记忆与索引怎么处理」）
- **视频抽帧采样按内容类型定帧率**：训练/教学视频 1 帧/秒、会议录 1 帧/5 秒；关键帧提取用色彩直方图或 SSIM 感知差异捕捉信息量大的帧；音频引导采样——在转写主题变化处取帧。
- **长视频理解三段式**：①预处理分镜（shot-boundary 检测）+ 统一多模态索引（帧嵌入 + ASR 转写 + 音频描述存同一向量库）→ ②自适应检索（orchestrator 按 query 定位相关时间段）→ ③只把相关段送高成本模型——计算集中在最该花的地方。
- **图像上下文外置（PAE 模式）**：图像先进感知抽象引擎→结构化语义（描述性 caption + 属性标签 + 缩略图）存外部视觉记忆，不占对话窗口；需要时跨模态检索召回。判据：**图像是记忆不是对话内容**——塞窗口的只是抽象，不是像素。
- 判据：**多模态的成本大头在输入 token 与检索**——视频别整段塞、图像别最高清、帧别均匀抽；先采样与索引，再送理解。
## 二·补二、真伪核验的证明边界（r739B 实拉 · 2026-11-14）

> 本技能原有硬规则是「画面 > 字幕 > 标题 > 评论区」，回答的是**怎么取到证据**；本节补的是**取到之后能证明什么、不能证明什么**。与 `engineering/vi-fact-verification`（单条声称三态 / 证据充分度门）、`engineering/wb-agent-evaluation`（SRM 与实验可信度）分工：那两条管「判据是否够、实验是否有效」，本条管「图像/视频这类证据对象的能力边界与结论分级」。豆包自留地曾把 C2PA 作为「水印双轨 / 移除工具」提及，本轮不搬水印机制，只取官方规范里的断言语义与检出边界。

### 11.1 有效凭证只证明三件事，不证明内容为真；缺失是默认态不是危险信号
C2PA 官方 Security Considerations v2.4 逐字定义：**Assertion** = 「a statement **asserted by an actor** concerning the asset」；**Claim** = 「digitally signed and tamper-evident ... references a set of assertions」；信任根是「the identity of the claim generator associated with the cryptographic signing key」。同篇自陈边界：「C2PA **does not offer any protection against the complete removal of C2PA manifests** from assets」，且 2.0 起 identity assertion 可为「a human actor, a pseudonym, completely anonymous, or ... a service」，规范「no longer defines how identity must be expressed」——签的是「谁签的」，不是「画面是真的」。useosint 的一句最直白：「一张经过签名的摆拍场景照片仍然是签名照片」。

阴性同样不能反推：多数相机不签名、多数编辑流程不保留清单、平台重编码会剥离凭证，故「缺少凭证是默认状态，**而非危险信号**」；IPTC 数字源类型字段与厂商隐形水印同理——**阳性可验才强，阴性只说明没找到某一供应商的标记**（aiimagedetector 2026-08-27：「A missing credential does not prove manipulation ... Treat the absence as a gap in provenance」）。

判据：验证报告必须分两栏写「这个凭证证明了什么」（签名链完整 / 文件自签名后未改 / 可追责主体）与「它不证明什么」（场景是否摆拍 / 标注是否真实 / 事件是否发生）。禁止把「无 C2PA / 无水印」列入「疑似伪造」的证据列；也禁止把「有 C2PA」直接写成「内容属实」。

### 11.2 ELA 与检测器分数都不得单独升格为结论
ELA 四种误用（useosint SKILL 中文全文逐字）：① 它对**内容**有反应，边缘纹理必然高亮、平坦天空皮肤必然暗，「每张图像都有可疑亮区」；② 一次重新保存即失效，社媒下载件测到的只是平台编码器特性；③ 内容感知填充 / 生成式编辑 / 完整重存不留可检差异史；④ **双向都错**——未篡改出亮区、被篡改输出干净都常见。仅剩的窄适用场景是「直接来自相机的单代 JPEG + 从不同压缩来源粘贴」。aiimagedetector 独立交叉逐字：「ELA **detects compression differences, not "fakeness" itself**」。

检测器分数同理：对压缩 / 缩放 / 放大 / 低光真实照片误报，对训练数据之后的新生成器漏报，轻微重压缩即改分；NewsGuard 实测主流工具把真实图误标 AI 达 **13.33%**、其中一款 **40%**。useosint 的判据是「如果你的证据只是网站给出的百分比，那你没有任何证据」。另有基线率问题：对真实图跑六个取证工具，总有一个结果看起来异常——**异常是真实图像的正常状态**；平台处理产生的 artifacts 常被误认成篡改痕迹。

判据：像素级信号只能作弱输入，且必须声明「可用副本的处理历史」与「哪些测试因此无效」；报告不得出现「分析显示这是假的」这类整体判断。优先基于物理与结构的**持久特征**（阴影汇聚、光影方向、透视、接触与遮挡、相机噪声/色差/景深），不依赖会被模型迭代修复的过时特征（手指/牙齿数、耳朵不对称、面部过度对称）。

### 11.3 结论按「主张」分级而非二值，且「未检出篡改」是对测试的陈述
先分流再动手（useosint 分流表）：主张是「这展示了 X 地 Y 事件」→ 先查最早副本与地理定位，**任何取证滤镜都要避开**（重新语境化不留像素痕迹）；是「这是一张未被篡改的照片」→ 只对最少处理版本做信号级分析；是「这张截图是真的」→ 查布局/字体/界面版本与底层记录，而非图像取证。绝大多数有欺骗性的媒体是**标注错误的真实素材**——像素是真的，年份/地点/事件是错的。

置信度六档分别对每个主张评级（一张图可同时「来源已确认」+「标注被反驳」+「真实性未确认」）：已确认原版且标注正确 / **已确认重新语境化** / 可能被篡改 / 可能是合成的 / **未确认**（多数案例终态）/ **无法评估**（副本过度处理，须说明哪些测试无效及原因）。「未检测到篡改」只是对测试结果的陈述，不是对图像的判断（「未确认」是合法终态，不得为求确定强行下结论）。

报告标准固定四件事：验证了什么、无法验证什么、每个结论的依据、跑过的测试及其阴性结果；并写出文件处理历史与所依据的假设。**画面取到了 ≠ 主张被证明了**——这是本技能第 0 条硬规则在「结论侧」的对应面。

**来源（r739B 独立实拉 2026-11-14，≥2 独立域交叉）**：
- `c2pa.org/specifications/` + `spec.c2pa.org/specifications/specifications/2.4/security/Security_Considerations.html`（C2PA 官方规范 2.4，WebFetch 200 全文逐字：Assertion asserted by an actor / 不防 complete removal of manifests / 匿名 identity assertion / Trust List）
- `www.skill4agent.com/zh/skill/useosint-skills/is-this-photo-real`（useosint/skills `is-this-photo-real` 中文译版 SKILL 全文逐字，原始来源 `github.com/useosint/skills`，添加于 2026-08-24；ELA 四误用、C2PA 三段语义、置信度六档、分流表、报告标准）
- `www.aiimagedetector.com/blog/what-is-image-verification`（2026-08-27 独立一手全文逐字：missing credential does not prove manipulation / ELA detects compression differences / 13.33%·40% 误报 / 三层模型）
- `skillselion.com/skills/useosint/osint-skills/is-this-photo-real`（英文原文镜像，搜索快照逐串交叉）；`timestampcamera.net/photo-guides/how-to-detect-ai-generated-images`（2026 指南，仅作 C2PA opt-in 交叉）
- 立场登记：`timestampcamera.net` / `aiimagedetector.com` 均为检测器厂商内容，其产品段落一律判非不采信；C2PA 主页为倡导方立场，凡「adoption/成员数」类宣传数字不搬。
