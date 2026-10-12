#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ocr_tool.py — 独立 OCR 引擎
===========================
增补 multimodal-intelligence「仅靠模型原生视觉、无独立 OCR 引擎」的缺口。
提供本地 OCR 能力，不再完全依赖模型视觉。

依赖（需安装其一，未装时诚实返回缺失提示，不假装已具备能力）：
  A) 系统装 Tesseract +  pip install pytesseract pillow
  B)  pip install paddleocr paddlepaddle        （中文效果更佳，但体积大）

用法：
  python ocr_tool.py <image_path> [lang=ch]
"""
import sys
import json

try:
    from paddleocr import PaddleOCR
    BACKEND = "paddle"
except Exception:
    try:
        import pytesseract
        from PIL import Image
        BACKEND = "tesseract"
    except Exception:
        BACKEND = None


def ocr(image_path: str, lang: str = "ch") -> dict:
    if BACKEND is None:
        return {"status": "dependency_missing",
                "hint": "pip install paddleocr paddlepaddle  或  系统装 Tesseract + pip install pytesseract pillow"}
    if BACKEND == "paddle":
        engine = PaddleOCR(use_angle_cls=True, lang=lang, show_log=False)
        res = engine.ocr(image_path)
        lines = [line[1][0] for block in res for line in (block or [])]
        return {"status": "ok", "backend": "paddle", "lines": lines}
    else:
        txt = pytesseract.image_to_string(Image.open(image_path), lang=lang)
        return {"status": "ok", "backend": "tesseract", "text": txt}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"hint": "ocr_tool.py <image_path> [lang]"}, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps(ocr(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "ch"),
                     ensure_ascii=False, indent=2))
