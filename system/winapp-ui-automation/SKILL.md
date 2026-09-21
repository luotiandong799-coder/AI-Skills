---
name: winapp-ui-automation
display_name: Windows控件识别
version: 1.0.0
agent_created: true
description: >-
  Windows UI 元素识别与控件级定位：用 UIA/UIA3（FlaUI、pywinauto、UIAutomation COM）枚举并识别窗口、按钮、输入框、菜单、列表、树、表格等元素，以 AutomationId/Name/ControlType/运行时 ID 做控件级定位与交互，不依赖固定屏幕坐标。适用于目标程序暴露无障碍树、需稳定可重复定位桌面控件的场景；Qt 类自绘应用（如微信 4.x 暴露 0 元素）退回 vision/OCR（见 computer-use-windows 与 win-native-app-automation）。触发词：UIA、UIAutomation、控件识别、控件级定位、FlaUI、pywinauto、AutomationId、无障碍树、元素定位、窗口枚举。
---

# Windows UI 元素识别（通用"眼睛"层）

> 本技能是 Windows 操控的**控件识别层**，与 `computer-use-windows`（输入/视觉）、`windows-automation`（引擎路由）、`powershell-windows-cli`（命令行）、`win-native-app-automation`（微信/QQ 实战配方）互补。**框架纪律（执行前检查/权限/停止/恢复/清理）由 personal-ai-os 与 wb-* 技能承担，本技能不重复。**

## 一、何时用本技能（识别层）

- 目标程序**暴露无障碍树**（Win32/WPF/.NET/标准控件）→ UIA 控件级定位最稳。
- 目标程序是**自绘/Qt 类**（如微信 4.x：窗口暴露 0 个元素，MSAA 仅根节点）→ UIA 不可用，退回 `computer-use-windows` 的视觉/OCR 定位（实证见 win-native-app-automation §2）。

## 二、识别手段

| 手段 | 适用 | 入口 |
|---|---|---|
| **FlaUI**（UIA3/UIA2） | .NET/C# 最强，支持 Invoke/Value/Text 等 Pattern | `FlaUI.UIA3` NuGet，PowerShell `Add-Type` 或编译小工具 |
| **pywinauto** | Python 侧，跨 UIA/Win32 后端 | `pywinauto.Application(backend="uia")` |
| **UIAutomation COM** | 纯 PowerShell，无需第三方 | `New-Object -ComObject UIAutomationClient.CUIAutomation` |
| **inspect.exe / Accessibility Insights** | 人工探查控件树、取 AutomationId | Windows SDK |

## 三、定位属性优先级（不依赖坐标）

1. **AutomationId**（最稳，版本升级通常不变）
2. **Name + ControlType** 组合
3. **运行时 ID / ClassName**（辅助）
4. **坐标兜底**（仅当以上全无，且用 UI 树返回坐标而非目测）

## 四、交互 Pattern

- `InvokePattern`（按钮点击）· `ValuePattern`（输入框设值）· `TextPattern`（读文本）
- `ExpandCollapsePattern`（菜单/树展开）· `SelectionItemPattern`（列表/单选）· `TogglePattern`（勾选）
- 识别后**读回元素属性/状态**确认目标正确，再交互。

## 五、与操控层衔接

- 本技能只产出"目标元素 + 定位方式"，实际点击/输入交给 `computer-use-windows` 或 `win-native-app-automation`。
- 无法可靠识别时，由 `windows-automation` 决策降级到下一引擎。
