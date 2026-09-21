---
name: computer-use-windows
display_name: Windows桌面操控
version: 1.0.0
agent_created: true
description: >-
  Windows 桌面级操控（手）：鼠标移动/点击/拖拽、键盘输入、窗口切换与前置、截图、视觉与 OCR 定位、等待与桌面级交互。优先用 windows-mcp 的 Snapshot/Screenshot/Click/Type/Shortcut/Clipboard；中文输入走剪贴板+Ctrl+V（SendKeys 不支持非 ASCII）；坐标点击仅作兜底，能用控件/键盘解决就不点坐标。需要像素级或跨应用桌面交互时结合截图+视觉/OCR。触发词：computer use、桌面操控、鼠标点击、键盘输入、截图、视觉定位、OCR定位、窗口切换、屏幕交互、GUI点击、桌面自动化。
---

# Windows 桌面操控（通用"手"层）

> 本技能是 Windows 操控的**输入与视觉交互层**。控件级优先走 `winapp-ui-automation`；命令行能做的优先走 `powershell-windows-cli`；引擎选择由 `windows-automation` 路由。**框架纪律由 personal-ai-os / wb-* 承担，本技能不重复。**

## 一、工具选择（优先 windows-mcp 原语）

| 动作 | windows-mcp 工具 |
|---|---|
| 看屏/取 UI 树 | `Snapshot(use_vision, use_ui_tree)` |
| 截图 | `Screenshot` |
| 点击 | `Click`（优先 UI 树元素坐标） |
| 输入 | `Type`（仅 ASCII） |
| 快捷键 | `Shortcut` |
| 中文/复杂文本 | `Clipboard` set → `Ctrl+V` |

- **中文输入不走 `Type`**（SendKeys 不支持非 ASCII）→ 先 `Clipboard` 设值，再 `Ctrl+V`（实证见 win-native-app-automation §1）。
- 坐标换算用 `Snapshot` 返回的 `Screenshot Coordinate Scale`；**优先用 UI 树元素坐标，不目测**。

## 二、窗口管理

- 前置/还原：`SetForegroundWindow` 单独调用常失败，需 `AttachThreadInput` 借前台线程（代码见 win-native-app-automation §2.1）。
- 每次键事件前复核 `GetForegroundWindow() == 目标 hwnd`，不等就重做 Force。
- 最小化窗口：Click 任务栏按钮（坐标从 UI 树读）。

## 三、视觉 / OCR 定位

- 截图 → 读 UI 树/视觉 → 定位目标；无稳定控件时按**颜色/形状/比例区域**识别（如微信发送按钮绿 `#07C160` 判据）。
- 坐标点击仅兜底；能用键盘/控件解决就不点坐标。

## 四、等待与验证

- 等待加载/动画完成再操作，不盲点。
- 每步 `Snapshot(use_vision)` 留证；关键动作前先 `Ctrl+A` 清空再输入。
- 验证以"实际结果"为准（见 `wb-artifact-verification`），不只看工具返回。

## 五、与识别层衔接

- 能拿到 AutomationId/Name → 交给 `winapp-ui-automation` 控件级定位。
- 识别失败 → `windows-automation` 降级到 OCR/视觉/坐标。
