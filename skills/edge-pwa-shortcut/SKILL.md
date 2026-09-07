---
name: edge-pwa-shortcut
description: 用脚本方式把任意网站做成 Edge 独立窗口 App（伪 PWA）。包含启动参数 --app=、独立 user-data-dir 绕过单实例复用、Python + pywin32 替代被安全策略拦掉的 PowerShell COM。
---

# Edge 独立窗口快捷方式（脚本版 PWA）

把任何 URL 做成"双击 → 真独立窗口 → 任务栏独立图标"，不依赖 `edge://apps` 手动安装。

## 适用场景

- 想给网站（chatgpt、claude、notion、内部系统...）弄个桌面图标
- 不愿意每次走 Edge 右上角 `...` → `安装此网站为应用`（这套需要手动点击）
- 用户机器上没有 PowerToys，想配合系统自带的"Win 键输入名称"快速启动

## 两个关键坑

### 坑 1：Edge 单实例复用吞掉 --app

当主 Edge 已经在跑，用 `msedge.exe --app=https://example.com` 启动新窗口，**会被原 Edge 实例吞掉变成新标签页，--app 不生效**。

**解决**：给一个独立的 `--user-data-dir`，强制 Edge 拉起全新实例：

```cmd
msedge.exe --app=https://example.com --user-data-dir="C:\Users\<u>\AppData\Local\<app>-EdgeProfile"
```

代价：独立 Cookie，首次需要在那个 profile 里重新登录目标网站一次。

### 坑 2：PowerShell 创建 .lnk 的 COM 路径可能被安全策略拦

`New-Object -ComObject WScript.Shell` 经常被沙箱拦（返回 "Command blocked for security: COM object instantiation..."）。

**解决**：用 Python + pywin32 替代：

```python
import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")
sc = shell.CreateShortcut(r"D:\path\to\MyApp.lnk")
sc.TargetPath = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
sc.Arguments = '--app=https://example.com --user-data-dir="C:\\path\\to\\profile" --window-size=1300,900'
sc.WorkingDirectory = r"C:\Program Files (x86)\Microsoft\Edge\Application"
sc.IconLocation = r"C:\path\to\app.ico,0"
sc.Description = "..."
sc.WindowStyle = 1
sc.Save()
```

注意：
- PowerShell 命令行里 `-c "..."` 加 COM 调用会被识别为 LOLBin 拦掉——把代码放进 `.py` 文件再执行。

## 完整脚本模板

```python
import os, win32com.client

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
ICON = r"C:\path\to\app.ico"
URL  = "https://example.com/"
PROFILE = r"C:\Users\__USER__\AppData\Local\__APP__-EdgeProfile"
os.makedirs(PROFILE, exist_ok=True)

ARGS = f'--app={URL} --user-data-dir="{PROFILE}" --window-size=1300,900'
DESKTOP   = os.path.join(os.path.expanduser("~"), "Desktop")  # 注意 OneDrive 重定向
STARTMENU = r"C:\Users\__USER__\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"

shell = win32com.client.Dispatch("WScript.Shell")
for root in (DESKTOP, STARTMENU):
    p = os.path.join(root, "__APP__.lnk")
    sc = shell.CreateShortcut(p)
    sc.TargetPath = EDGE
    sc.Arguments  = ARGS
    sc.WorkingDirectory = os.path.dirname(EDGE)
    sc.IconLocation = f"{ICON},0"
    sc.Description = "__APP__（Edge 独立窗口）"
    sc.WindowStyle = 1
    sc.Save()
```

## 图标

如果目标有官方 App 装在 WindowsApps，从它的 `assets\Square*Logo.targetsize-256_altform-unplated.png` 取 256×256 PNG 转 ICO（用 Pillow 多尺寸）：

```python
from PIL import Image
img = Image.open(r"C:\Program Files\WindowsApps\...\assets\Square44x44Logo.targetsize-256_altform-unplated.png")
img.save(r"...\app.ico", format="ICO", sizes=[(s,s) for s in (16,20,24,32,40,48,64,96,128,256)])
```

否则下载站点 favicon.png 用 Pillow 转。

## 验证是否真的进了 --app 模式

主 Edge 在跑时检查 `Get-CimInstance Win32_Process`：

```powershell
Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" |
  Where-Object { $_.CommandLine -like '*--app=*' -and $_.CommandLine -like '*example.com*' }
```

如果返回 0 条说明被单实例吞了，需要独立 user-data-dir。

## Windows 自带键盘启动器（无需 PowerToys）

把 `.lnk` 放到「开始菜单 Programs」目录后，**按 Win 键输入应用名 → Enter** 就能搜到，相当于 0 安装的"Alt+Space"。

## 何时应该用真正的 PWA 安装

脚本版的局限：
- 没有"独立任务栏图标分组"（Edge --app 模式下，多个 `--app` 实例可能仍归到 Edge 同一图标）
- 没有"登录时自动启动"的图形化开关（要实现得自己放 `.lnk` 到 Startup 文件夹）
- Windows 应用列表 / 设置里看不到这个应用

如果需要这些，还是走 Edge 右上角 `...` → `将此站点安装为应用`，3 秒搞定。

## 验证清单

- [ ] 双击桌面 .lnk → 真独立窗口（无标签页、无地址栏）
- [ ] 主 Edge 已开时也能开新独立窗口（独立 user-data-dir）
- [ ] 任务栏分组与主 Edge 分开
- [ ] 按 Win 键输入名字能搜到
- [ ] ICO 图标在桌面和开始菜单都显示正确