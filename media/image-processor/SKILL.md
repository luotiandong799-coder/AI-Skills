---
name: image-processor
display_name: 图片处理
display_name_en: Image Processor
description: "图片压缩、缩放、格式转换、裁剪、旋转、镜像、灰度、水印、圆角等常用处理，完全本地离线，不依赖任何云端服务"
description_zh: "处理用户上传的图片，压缩、缩放、格式转换、裁剪、旋转、翻转、灰度、文字水印、圆角；全程离线，不联网、不付费、无需密钥"
description_en: "Process images, compress, resize, convert, crop, rotate, flip, grayscale, watermark, rounded corners. Fully local and offline, no cloud service, no API key."
category: tool
version: "1.0.0"
author: "unknown"
allowed-tools: "Bash, Read, Write"
---

# 图片处理技能指令

当用户需要处理一张图片（压缩体积、调整尺寸、转换格式、裁剪、旋转、镜像、转黑白、加水印、圆角）时，按以下步骤执行：

1. 拿到用户上传的图片文件路径（输入图片）。
2. 读取 `references/api-spec.md`，确认支持的格式与参数格式。
3. 用 Bash 调用脚本：
   `python3 scripts/process-image.py <输入图片> [选项]`
4. 将脚本输出路径中的结果图片返回给用户。

## 常用调用示例

- 压缩：`python3 scripts/process-image.py img.png --compress 80`
- 缩放：`python3 scripts/process-image.py img.png --resize 800x600`
- 等比例缩放：`python3 scripts/process-image.py img.png --resize 800x-1`
- 格式转换：`python3 scripts/process-image.py img.png --convert webp`
- 裁剪：`python3 scripts/process-image.py img.png --crop 10:10:200:150`
- 旋转：`python3 scripts/process-image.py img.png --rotate 90`
- 水平翻转：`python3 scripts/process-image.py img.png --flip h`
- 转黑白：`python3 scripts/process-image.py img.png --grayscale`
- 文字水印：`python3 scripts/process-image.py img.png --watermark "LOGO"`
- 圆角：`python3 scripts/process-image.py img.png --round 80`
- 指定输出：`python3 scripts/process-image.py img.png --compress 80 --output /tmp/out.jpg`

## 注意事项

- 脚本会自动探测环境里可用的图片引擎（Pillow / ffmpeg / ImageMagick / System.Drawing），挑一个能用的执行，无需用户指定。
- 全程本地离线，不联网、不付费、不需要 API Key。
- 若环境没有任何可用引擎，脚本会给出清晰的安装提示（`pip install pillow` 等），不会崩溃报错。