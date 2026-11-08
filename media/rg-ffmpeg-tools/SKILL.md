---
name: rg-ffmpeg-tools
display_name: 搜索与音视频工具箱
display_name_en: Ripgrep & FFmpeg Tools
description: 内置 ripgrep 快速文件搜索与 ffmpeg/ffprobe/ffplay 音视频处理工具，全部本地离线可用。需要快速在大量文件/代码中搜索文本、或处理音视频（转码、抽帧、截取、合并、分析元数据、播放）时使用。
description_zh: 使用 ripgrep 在文件与代码中高速搜索文本；使用 ffmpeg 处理音视频（格式转换、抽帧、裁剪、合并、压缩）；使用 ffprobe 查看音视频元数据；使用 ffplay 本地播放。工具全部位于本技能 bin 目录，无需联网。
description_en: Ripgrep for fast text search across files; FFmpeg for audio/video processing (transcode, extract frames, trim, merge, compress); FFprobe for media metadata; FFplay for local playback. Fully local and offline.
category: tool
version: "1.1.0"
author: "doubao"
module: PI
modules: PI
---

# rg-ffmpeg-tools（搜索与音视频工具箱）

本技能内置四个本地工具，均位于本技能目录 `bin\` 下，可直接调用，无需联网、无需额外安装：

| 工具 | 用途 |
|---|---|
| `rg.exe` | 高速文本/正则搜索（ripgrep） |
| `ffmpeg.exe` | 音视频处理：转码、抽帧、裁剪、合并、压缩 |
| `ffprobe.exe` | 查看音视频文件的元数据（时长、编码、分辨率等） |
| `ffplay.exe` | 本地播放音视频 |

## 调用方式

工具绝对路径为 `D:\腾讯AI\skills\media\rg-ffmpeg-tools\bin\`，例如：

```powershell
& 'D:\腾讯AI\skills\media\rg-ffmpeg-tools\bin\rg.exe' --version
& 'D:\腾讯AI\skills\media\rg-ffmpeg-tools\bin\ffmpeg.exe' -version
```

## 常用命令示例

**ripgrep 搜索**（比 findstr 快得多，自动忽略 .gitignore 文件）：

```powershell
# 在目录中搜索关键词（递归、带行号、彩色）
& 'D:\腾讯AI\skills\media\rg-ffmpeg-tools\bin\rg.exe' '关键词' 'D:\目标目录'

# 只搜 .py / .md 文件
& 'D:\腾讯AI\skills\media\rg-ffmpeg-tools\bin\rg.exe' -g '*.py' 'def main' 'D:\目标目录'

# 统计匹配文件数
& 'D:\腾讯AI\skills\media\rg-ffmpeg-tools\bin\rg.exe' -l '关键词' 'D:\目标目录' | Measure-Object
```

**ffmpeg 音视频处理**：

```powershell
# 格式转换（mp4 -> mp3 提取音频）
& 'D:\腾讯AI\skills\media\rg-ffmpeg-tools\bin\ffmpeg.exe' -i '输入.mp4' -vn '输出.mp3'

# 视频抽帧（每秒 1 帧输出为图片）
& 'D:\腾讯AI\skills\media\rg-ffmpeg-tools\bin\ffmpeg.exe' -i '输入.mp4' -vf "fps=1" '帧_%03d.jpg'

# 裁剪片段（从第 10 秒开始截 30 秒）
& 'D:\腾讯AI\skills\media\rg-ffmpeg-tools\bin\ffmpeg.exe' -ss 10 -i '输入.mp4' -t 30 -c copy '输出.mp4'

# 压缩视频（H.264，CRF 23）
& 'D:\腾讯AI\skills\media\rg-ffmpeg-tools\bin\ffmpeg.exe' -i '输入.mp4' -c:v libx264 -crf 23 '输出.mp4'
```

**ffprobe 元数据**：

```powershell
& 'D:\腾讯AI\skills\media\rg-ffmpeg-tools\bin\ffprobe.exe' -v error -show_format -show_streams '输入.mp4'
```

## 说明

- 工具为 WinGet 安装版原样复制（ripgrep 15.2.0、FFmpeg 9.0.1 full build），静态编译无 dll 依赖，拷贝到任意目录可直接运行。
- 系统 PATH 中若另有同版本工具，优先使用本技能 bin 下的本地副本，保证行为一致。
## GIF / 动图输出门：参数先定，再画，再用 ffprobe 验（来源：`anthropics/skills`·`skills/slack-gif-creator/SKILL.md` 7,841B，2026-11-08 实拉）

- **先定参数再画**：表情类 128×128、消息类 480×480；FPS 10–30（越低体积越小）；色数 48–128（越少越小）；表情动图时长**控制在 3 秒内**。参数是交付约束，不是画完再凑。
- **ffmpeg 出 GIF 必须两遍调色板**：先 `palettegen` 生成调色板，再 `paletteuse` 合成——
  `ffmpeg -i in.mp4 -vf "fps=12,scale=480:-1:flags=lanczos,palettegen" palette.png`
  `ffmpeg -i in.mp4 -i palette.png -filter_complex "fps=12,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" out.gif`
  单遍直出会脏、渐变出带状。
- **帧去重是最高性价比的减重**：静止段重复帧占体积大头，先 `remove duplicate frames` 再谈降 FPS/色数。
- **验收用 ffprobe 读事实**：`nb_frames` / `avg_frame_rate` / `duration` / `width,height`；"看起来在动"不是验收。
- **不要用 emoji 字体渲染**：跨平台字形不可靠；自绘矢量基元，或直接用用户提供的图。
- **优化只在被要求时做**：先交能跑的版本，再按需降 FPS/色数/尺寸。
- **提升层**：工具（媒体输出）+ 工作流（交付门）。
