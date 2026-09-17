# -*- coding: utf-8 -*-
"""
图片处理技能 - 自动探测多引擎版
================================
设计目标：不依赖任何云端/在线/付费服务，也不赌某个库一定存在。
脚本启动后，先自动探测环境里有哪些可用的图片处理引擎，挑一个能用的来干活，
一个都没有则清晰报错。全程离线、无网络、无密钥。

引擎探测优先级：
    Pillow (Python 库)  ->  ffmpeg  ->  ImageMagick (magick / convert)

用法：
    python process-image.py <输入图片> [选项]

常用选项：
    --compress 85              按质量压缩（0-100）
    --resize 800x600           缩放（宽x高，等比例用 -1，如 800x-1）
    --convert webp             格式转换（png/jpg/jpeg/webp/bmp）
    --crop 10:10:200:150       裁剪（左:上:宽:高）
    --rotate 90                旋转角度
    --flip h                   水平翻转（h）/ 垂直翻转（v）
    --grayscale                转灰度/黑白
    --watermark "文字"         文字水印（需 Pillow）
    --round 80                 圆角半径（需 Pillow）
    --output 输出路径          输出文件路径（默认 输入文件名_processed.后缀）
"""
import os, sys, shutil, subprocess

# ============================================================
# 第一步：自动探测环境里有哪些图片引擎（完全自动，无需人工）
# ============================================================
def detect_engine():
    """自动检查环境里可用的图片处理引擎，返回 (engine, handle)。"""
    # 1) Pillow —— Python 最常用的图片库
    try:
        import PIL  # noqa
        return ("pillow", None)
    except Exception:
        pass

    # 2) ffmpeg
    for exe in ("ffmpeg", "ffmpeg.exe"):
        p = shutil.which(exe)
        if p:
            return ("ffmpeg", p)

    # 3) ImageMagick
    for exe in ("magick", "magick.exe"):
        p = shutil.which(exe)
        if p:
            return ("imagemagick", p)

    # 4) ImageMagick 老版本 (convert 命令, 需排除 Windows 磁盘工具)
    for exe in ("convert", "convert.exe"):
        p = shutil.which(exe)
        if p and os.name != "nt":       # convert.exe 在 Windows 是磁盘工具, 跳过
            return ("imagemagick", p)

    # 5) Windows 自带 System.Drawing（经 PowerShell，免安装）
    if os.name == "nt":
        ps = shutil.which("powershell")
        if ps:
            return ("systemdrawing", ps)

    return (None, None)                 # 一个都没有


# ============================================================
# Pillow 分支：支持全部八项常用功能
# ============================================================
def handle_pillow(args):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.open(args.input)
    im.load()
    mode = "RGB"

    # --crop（先裁剪，之后再叠其他操作）
    if args.crop:
        l, t, w, h = [int(x) for x in args.crop.split(":")]
        im = im.crop((l, t, l + w, t + h))

    # --resize
    if args.resize:
        wi, hi = args.resize.lower().split("x")
        wi = int(wi) if wi != "-1" else None
        hi = int(hi) if hi != "-1" else None
        if wi is None:
            wi = int(im.width * (hi / im.height))
        if hi is None:
            hi = int(im.height * (wi / im.width))
        im = im.resize((wi, hi), Image.LANCZOS)

    # --rotate
    if args.rotate is not None:
        im = im.rotate(args.rotate, expand=True)

    # --flip
    if args.flip:
        from PIL import Image as _I
        if args.flip == "h":
            im = im.transpose(_I.FLIP_LEFT_RIGHT)
        elif args.flip == "v":
            im = im.transpose(_I.FLIP_TOP_BOTTOM)

    # --grayscale
    if args.grayscale:
        im = im.convert("L")

    # --watermark
    if args.watermark:
        im = im.convert("RGBA")
        overlay = Image.new("RGBA", im.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(overlay)
        w, h = im.size
        if os.name == "nt":                      # 常见 Windows 字体路径
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", max(24, w // 12))
        else:
            font = ImageFont.load_default()
        d.text((w - int(w * 0.9), h - int(h * 0.9)), args.watermark, font=font, fill=(255, 255, 255, 150))
        im = Image.alpha_composite(im, overlay).convert(mode)

    # --round（圆角，RGBA 通道处理）
    if args.round is not None:
        r = int(args.round)
        im = im.convert("RGBA")
        from PIL import ImageDraw as _D
        mask = Image.new("L", im.size, 0)
        d = _D.Draw(mask)
        d.rounded_rectangle([0, 0, im.size[0], im.size[1]], radius=r, fill=255)
        im = Image.composite(im, Image.new("RGBA", im.size, (0, 0, 0, 0)), mask)

    # 保存/输出
    out = args.output or _default_output(args.input, "png")
    fmt = _out_format(out)
    save_kwargs = {}
    if fmt in ("JPEG", "JPG"):
        save_kwargs["quality"] = args.compress if args.compress else 85
        save_kwargs["optimize"] = True
    if args.round is not None:
        im.save(out, "PNG")          # 圆角/透明 建议输出 png
    else:
        im.convert("RGB").save(out, fmt, **save_kwargs) if fmt != "PNG" else im.save(out, "PNG")
    return out


# ============================================================
# ffmpeg 分支：核心功能（压缩/缩放/转换/裁剪/旋转/翻转/灰度）
# ============================================================
def handle_ffmpeg(args):
    exe = args.engine_handle
    vf = []
    if args.crop:
        l, t, w, h = [int(x) for x in args.crop.split(":")]
        vf.append("crop=%d:%d:%d:%d" % (w, h, l, t))
    if args.resize:
        vf.append("scale=" + args.resize.replace("x", ":").replace("-1", "-1"))
    if args.rotate is not None:
        vf.append("rotate=%s" % args.rotate)
    if args.flip == "h":
        vf.append("hflip")
    elif args.flip == "v":
        vf.append("vflip")
    if args.grayscale:
        vf.append("format=gray")
    out = args.output or _default_output(args.input, "jpg")
    cmd = [exe, "-y", "-i", args.input]
    if vf:
        cmd += ["-vf", ",".join(vf)]
    q = args.compress if args.compress else 2
    cmd += ["-q:v", str(q), out]
    subprocess.run(cmd, check=True)
    return out


# ============================================================
# ImageMagick 分支：核心功能
# ============================================================
def handle_imagemagick(args):
    exe = args.engine_handle
    out = args.output or _default_output(args.input, "png" if args.round else "png")
    cmd = [exe, args.input]
    if args.crop:
        x, y, w, h = [int(v) for v in args.crop.split(":")]
        cmd += ["-crop", "%dx%d+%d+%d" % (w, h, x, y), "+repage"]
    if args.resize:
        wi, hi = args.resize.lower().split("x")
        cmd += ["-resize", "%s%s%s" % (wi, "x" if hi and hi != "-1" else "", "" if hi in ("-1", "") else hi)]
    if args.rotate is not None:
        cmd += ["-rotate", str(args.rotate)]
    if args.flip == "h":
        cmd += ["-flop"]
    elif args.flip == "v":
        cmd += ["-flip"]
    if args.grayscale:
        cmd += ["-colorspace", "Gray"]
    if args.watermark:
        cmd += ["-annotate", "+15+15", args.watermark]
    if args.compress:
        cmd += ["-quality", str(args.compress)]
    cmd += [out]
    subprocess.run(cmd, check=True)
    return out


# ============================================================
# System.Drawing 分支：通过 Windows 自带引擎(powershell)完成，免安装
# ============================================================
def handle_systemdrawing(args):
    ps = args.engine_handle
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "process-image.ps1")
    out = args.output or _default_output(args.input, args.convert or "jpg")
    cmd = [ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script,
           "-InputImage", args.input, "-Output", out]
    if args.compress:
        cmd += ["-Compress", str(args.compress)]
    if args.resize:
        cmd += ["-Resize", args.resize]
    if args.crop:
        cmd += ["-Crop", args.crop]
    if args.rotate is not None:
        cmd += ["-Rotate", str(args.rotate)]
    if args.flip:
        cmd += ["-Flip", args.flip]
    if args.grayscale:
        cmd += ["-Grayscale"]
    if args.watermark:
        cmd += ["-Watermark", args.watermark]
    if args.round is not None:
        cmd += ["-Round", str(args.round)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("System.Drawing 处理失败: " + (r.stderr or r.stdout))
    return out


# ============================================================
# 通用辅助
# ============================================================
def _default_output(inp, ext):
    base, _ = os.path.splitext(inp)
    return base + "_processed." + ext

def _out_format(out):
    e = os.path.splitext(out)[1].lstrip(".").upper()
    return "JPG" if e == "JPEG" else ("JPEG" if e == "JPG" else e)

def main():
    # 手写参数解析（避免引入额外依赖，标准库优先）
    args = _parse_args(sys.argv[1:])
    if not args.input:
        print("用法: python process-image.py <输入图片> [--compress 85 --resize 800x600 --convert webp ...]")
        sys.exit(1)

    engine, handle = detect_engine()
    args.engine_handle = handle
    if engine is None:
        print("图片处理失败：当前环境没有任何可用图片引擎。")
        print("请安装其一：pip install pillow  ·  或安装 ffmpeg  ·  或安装 ImageMagick")
        sys.exit(2)
    print("自动探测到引擎:", engine, "(" + (handle or "Python库") + ")")

    if engine == "pillow":
        out = handle_pillow(args)
    elif engine == "ffmpeg":
        out = handle_ffmpeg(args)
    elif engine == "systemdrawing":
        out = handle_systemdrawing(args)
    else:
        out = handle_imagemagick(args)
    print("处理完成:", out)

def _parse_args(argv):
    class NS: pass
    a = NS()
    a.input = None; a.output = None; a.compress = None
    a.resize = None; a.convert = None; a.crop = None
    a.rotate = None; a.flip = None; a.grayscale = False
    a.watermark = None; a.round = None
    i = 0
    while i < len(argv):
        t = argv[i]
        if t in ("--output",):
            i += 1; a.output = argv[i]
        elif t == "--compress":
            i += 1; a.compress = int(argv[i])
        elif t == "--resize":
            i += 1; a.resize = argv[i]
        elif t == "--convert":
            i += 1; a.convert = argv[i]
        elif t == "--crop":
            i += 1; a.crop = argv[i]
        elif t == "--rotate":
            i += 1; a.rotate = int(argv[i])
        elif t == "--flip":
            i += 1; a.flip = argv[i]
        elif t == "--grayscale":
            a.grayscale = True
        elif t == "--watermark":
            i += 1; a.watermark = argv[i]
        elif t == "--round":
            i += 1; a.round = int(argv[i])
        else:
            if not t.startswith("--"):
                a.input = t
        i += 1
    return a

if __name__ == "__main__":
    main()