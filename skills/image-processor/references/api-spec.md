# 图片处理 API 规范 / 参数说明

## 支持的输入格式
png, jpg/jpeg, webp, bmp, gif（取决于环境内 Pillow/ffmpeg/ImageMagick 的能力）

## 参数列表
| 参数        | 格式                 | 说明 |
|------------|----------------------|------|
| --compress | 整数 0-100           | 压缩质量，默认 85（JPEG/格式转换时生效） |
| --resize   | `宽x高`              | 缩放，`-1` 表示保持比例，如 `800x-1` |
| --convert  | 目标格式             | 格式转换，如 webp/png/jpg |
| --crop     | `左:上:宽:高`         | 裁剪区域，如 `10:10:200:150` |
| --rotate   | 整数角度             | 旋转，如 90/180/270 |
| --flip     | `h` 或 `v`           | h=水平翻转, v=垂直翻转 |
| --grayscale| 无值                 | 转为灰度/黑白 |
| --watermark| 文字                 | 文字水印（需 Pillow） |
| --round    | 整数半径 px          | 圆角处理（需 Pillow） |
| --output   | 输出路径              | 默认 `<输入名>_processed.<后缀>` |

## 运行时机
脚本 `scripts/process-image.py` 由 AI 通过 Bash 执行。命令格式：
`python3 scripts/process-image.py <输入图片> [选项]`

## 错误处理
- 引擎探测失败：输出 `图片处理失败：当前环境没有任何可用图片引擎`，并提示安装 `pip install pillow`。
- 其他异常：错误信息会由脚本打印，AI 需如实反馈给用户。