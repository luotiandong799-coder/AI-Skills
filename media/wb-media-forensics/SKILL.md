---
name: wb-media-forensics
description: 视频 / 图片类内容的取证与提取（反爬短链 → 拿到内容本体 → 抽帧读图）。当用户发来视频分享链接（抖音 / 快手 / B站 / 小红书 / 视频号短链）、要求"看看这个视频讲了什么""视频里推荐的工具/仓库是什么"、页面被反爬拦住拿不到正文、或视频没有可用字幕接口时使用。四步链路：短链解析 → Edge 无头渲染取播放地址 → 下载 + 本地解码抽帧 → 拼联络表多模态读图。触发词：抖音、快手、B站、小红书、视频链接、看看这个视频、视频讲了什么、逐帧、逐帧分析、口播、字幕、抓视频、video frames、media forensics。
agent_created: true
version: 1.1.0
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