---
name: personal-ai-os
description: >-
  Personal AI OS（个人 AI 电脑助手环境）总路由与模块规范。当用户提出「电脑助手 / 帮我操作电脑 / 打开软件 / 输入内容 / 截图看看 / 桌面自动化 / 个人 AI 环境 / Personal AI OS / 我的电脑助手 / 电脑维护 / 系统体检 / 磁盘空间 / 开机自启 / 电脑变慢了 / 清理缓存 / AI 学习 / 学 AI / 关注 AI 动态 / AI 信息雷达 / AI 行业新闻 / 每日 AI 简报 / 个人知识管理 / 整理我的资料 / 知识库 / 笔记体系 / 第二大脑」这类需求时应用。本技能不重复实现已有能力，只做**总路由 + 五大模块的规范与安全边界**：电脑助手 → Windows MCP；AI 学习 → wb-teaching + agent-reach；电脑维护 → wb-debug-loop + Desktop Commander；AI 信息雷达 → Playwright MCP + agent-reach + web-scrape；个人知识管理 → File MCP + wb-doc-writing。触发词：电脑助手、桌面自动化、帮我操作电脑、打开应用、截图、Personal AI OS、个人AI环境、电脑维护、系统体检、磁盘清理、开机启动项、电脑慢、AI学习、学AI、AI动态、AI新闻、AI信息雷达、每日AI简报、知识管理、资料整理、知识库、笔记、第二大脑、personal ai os、desktop assistant、ai radar。
version: 1.0.0
agent_created: true
---

# Personal AI OS（个人 AI 电脑助手环境 · 总路由）

本技能是**路由器 + 规范层**，不是实现层。所有具体能力都下沉到已有技能或 MCP 连接器，本技能只负责：

1. **分诊**：判断用户需求落在哪个模块
2. **路由**：把任务交给正确的已有能力
3. **规范**：定义每个模块的目标、触发条件、执行流程、输出格式
4. **守边界**：安全约束集中在此，各模块不得绕过

**硬规则：本技能不允许自行"重新实现"任何已有能力。** 遇到以下场景必须先加载对应技能，不得凭本技能正文直接干活。

---

## 〇、能力总表（先查这张表，再决定路由）

| 需求类型 | 首选能力 | 落点 |
|---|---|---|
| 操作 Windows 桌面（开应用/点按钮/输文字/截图/剪贴板/窗口） | **Windows MCP**（window-mcp，工具 `App` / `Click` / `Type` / `Shortcut` / `Clipboard` / `Screenshot` / `Snapshot`） | mcp.json |
| 浏览网页 / 抓页面 / 填表 / 搜索 | **Playwright MCP**（headless，Edge 内核） | mcp.json |
| 需登录态 / 反爬 / 验证码的浏览器任务 | `browser-automation`、`bsk-drive-logged-in-browser`、`agent-browser` | 技能 |
| 读写本地文件（限定 D 盘） | **File MCP**（filesystem，白名单 `D:\腾讯AI` + `D:\AI技能仓库`） | mcp.json |
| 查看系统/进程/环境信息（只读） | **Desktop Commander 只读代理**（工具 `list_processes` / `get_file_info` / `list_directory` / `read_file`） | mcp.json + 代理脚本 |
| GitHub 仓库操作 | `github` 技能 / `gh` CLI | 技能 |
| 排障（报错、崩溃、变慢、跑不起来） | `wb-debug-loop` | 技能 |
| 多步实现 / 交付类改造 | `wb-spec-driven` | 技能 |
| 批量目标全量覆盖 / 失败换路 | `wb-execute-discipline` | 技能 |
| 交付物先验证 | `wb-artifact-verification` | 技能 |
| 写文档 / 报告 / 方案 | `wb-doc-writing` | 技能 |
| 中文去 AI 味 | `humanizer-zh` | 技能 |
| 教学 / 学习路径 / 概念讲解 | `wb-teaching` | 技能 |
| 特定平台调研（小红书/B站/推特/雪球/YouTube…） | `agent-reach` | 技能 |
| 通用网页抓取转 Markdown | `web-scrape` | 技能 |
| 重复文件清理 | `local-file-dedup` | 技能 |
| C 盘迁 D 盘 | `windows-migrate-to-d-via-junction` | 技能 |

---

## 一、模块 A：电脑助手（Computer Assistant）

**目标**：让 AI 能直接操作本机 Windows 桌面——开应用、点按钮、输入文本、截图确认，把"手把手教用户点"变成"AI 直接做完"。

**触发条件**
- "帮我打开 XX 软件 / 记事本 / 浏览器 / 计算器"
- "在 XX 里输入 / 粘贴 / 填一下"
- "截图看看现在屏幕什么样"
- "帮我点一下 / 关掉这个窗口 / 切到 XX"
- "桌面自动化 / 电脑助手 / 帮我操作电脑"

**执行流程**
1. **先看再动**：`Snapshot` 或 `Screenshot` 取当前屏幕状态与 UI 树，确认焦点窗口是谁。不要盲点坐标。
   - `Snapshot` 返回完整 UI 树（含元素坐标与可点击标记），用于找控件
   - `Screenshot` 返回快速图像 + 坐标缩放比（**注意**：图像经下采样，用 `Click` 前需按返回的 `Screenshot Coordinate Scale` 换算）
2. **激活目标窗口**：`App`（`mode: resize` / `switch`）或先 `Click` 目标窗口区域使其前台化。
3. **执行操作**：`Click` / `Type` / `Shortcut` / `Clipboard` / `Scroll`。
   - **中文文本不走 `Type`**（SendKeys 不支持非 ASCII）：先 `Clipboard`（`mode: set`）→ `Shortcut ctrl+v`。这是本环境实测有效的路径。
   - `Type` 的 `loc` **必填**（坐标或元素标签），只给 `text` 会报 `Either loc or label must be provided`。
4. **关键动作前清空**：输入前先 `ctrl+a` 再粘贴，避免追加污染原内容。
5. **截图留证**：操作完成必须 `Screenshot` 并保存到 `D:\腾讯AI\yt\outputs\<日期>_<主题>验证\`。
6. **收尾**：关掉临时打开的窗口；不留后台进程。

**输出格式**
- 图片路径清单（绝对路径）
- 操作序列一句话概括（做了什么 → 得到什么）
- 若中途失败：卡在哪一步 + 下一步换什么路径

**安全边界**
- 不操作与任务无关的窗口；不确认对方身份前不发消息类操作
- 涉及删除、发送、支付、改注册表 → 见第五节统一约束
- `Registry` 工具**默认禁用**，除非用户明确点名且理由充分
- 记事本另存为对话框必须给**绝对路径**，否则新 Notepad 会提示"你不能保存到此电脑"

---

## 二、模块 B：AI 学习（AI Learning）

**目标**：把"想学 AI"变成有路径、有节奏、有检索练习的持续学习，而不是零散读文章。

**触发条件**
- "教我 X / 我想学 X / 带我入门 X / 帮我规划学习路线"
- "AI 这块我该从哪开始 / 什么是 XX（且要求讲清楚而非查定义）"
- "帮我复习 / 考考我 / 我学到哪了"

**执行流程**
1. **加载 `wb-teaching`**（方法论：使命锚定 + 学习记录 + 检索练习 + 最近发展区），本技能不重复其内容。
2. 补最新资料时叠加 `agent-reach`（特定平台）或 `web-scrape`（通用网页），**先判断信源权威性再引用**。
3. 学习记录落 `D:\腾讯AI\skills\memory\` 或用户指定路径，跨会话可续。

**输出格式**
- 课时内容（自包含，可单独看懂）
- 本次 3 个检索问题（不给答案，下次问）
- 下一步建议 + 当前所处阶段

**安全边界**
- 不编造论文/数据/引用；拿不到权威来源就明说"未验证"
- 学习记录属个人文件 → 只追加，不覆盖历史

---

## 三、模块 C：电脑维护（Computer Maintenance）

**目标**：定期体检 + 排障 + 磁盘治理，让机器保持在可用状态，且所有"清理"动作可回溯。

**触发条件**
- "电脑变慢了 / 卡 / 风扇一直响 / 内存不够"
- "C 盘快满了 / 清理一下磁盘 / 哪些文件占地方"
- "系统体检 / 看看硬件配置 / 磁盘用了多少"
- "开机启动项看一下" / "某个软件跑不起来 / 报错"

**执行流程**
1. **只读扫描先行**：环境信息走 Desktop Commander 只读代理（`list_processes` / `get_file_info` / `list_directory`）或 Windows MCP 的 PowerShell 工具。**扫描阶段不改任何东西。**
2. **排障走纪律**：任何"报错 / 跑不起来 / 变慢"→ 加载 `wb-debug-loop`（重现 → 最小化 → 假设 → 验证 → 修复 → 回归），禁止先改再猜。
3. **清理走清单**：重复文件 → `local-file-dedup`；C 盘迁移 → `windows-migrate-to-d-via-junction`。
4. **删除动作必须三项齐全**：加粗风险警告 + 逐条列出受影响路径 + 用户明确确认。用回收站不用 `rm`。
5. 周期体检建议做成自动化（见第六节方案），但**创建前须用户确认**。

**输出格式**
- 体检表：CPU / 内存 / 磁盘 / 系统版本 / 异常进程
- 问题分级：🔴 立即处理 / 🟡 观察 / 🟢 正常
- 清理建议：每条附"影响范围 + 可回滚性"

**安全边界（本模块最严）**
- **只读扫描不等于可以顺手清理**。扫描产出报告后停下等确认。
- 不碰：私钥、密码管理器、银行/支付目录、`AppData`、`Library`、`~/.config`、系统目录
- 禁 `rm -rf` / `del /S /Q` / `shutil.rmtree` / 通配符批量删
- 单批最多 10 个文件，每批验证，失败即停

---

## 四、模块 D：AI 信息雷达（AI Radar）

**目标**：自动把当日/本周的 AI 行业动态压缩成可读要点，不刷信息流也能跟上。

**触发条件**
- "今天 AI 有什么新闻 / AI 圈最近发生了什么"
- "AI 信息雷达 / 每日 AI 简报 / AI 行业动态"
- "帮我盯着 XX 的消息 / 有更新告诉我"
- "看看大家怎么评价 XX"（这类更偏 `agent-reach`，注意分流）

**执行流程**
1. **抓取层**：Playwright MCP（`browser_navigate` → `browser_evaluate` 取 `document.body.innerText`）抓新闻聚合页。本环境已验证 `https://www.bing.com/news/search?q=<关键词>&qft=interval%3d%227%22` 可稳定返回中文+英文混合结果。
2. **需要深度/特定平台** → 升级到 `agent-reach`（小红书/推特/B站/雪球/Reddit/LinkedIn/YouTube 字幕）或 `web-scrape`。
3. **交叉验证**：同一事件至少两个独立来源；单一来源标注"待核实"。
4. **压缩**：按重要性排序，剔除营销稿与重复稿。
5. **输出中文**（需要时过 `humanizer-zh`），落 `D:\腾讯AI\yt\outputs\<日期>_AI简报\`。

**输出格式**
```markdown
# AI 简报 · YYYY-MM-DD
## 1. <标题>
- **来源**：<媒体>（<时间>）
- **要点**：1-2 句
- **影响**：对行业/用户意味着什么
（共 3-5 条，按重要性降序）
## 交叉验证说明
- ✅ 多源确认：…
- ⚠️ 单一来源：…
```

**安全边界**
- 不编造来源与数据；抓取失败如实报"未取到"，不用记忆填充
- 不登录他人账号；需要登录态时走 `browser-automation` 或 `bsk-drive-logged-in-browser` 并说明
- 评论类内容标注观点属性，不当事实转述

---

## 五、模块 E：个人知识管理（Personal Knowledge Management）

**目标**：把散落在本机 D 盘的资料变成可检索、有分类、不重复的知识库。

**触发条件**
- "整理我的资料 / 帮我看看 XX 文件夹都有什么"
- "知识库 / 笔记体系 / 第二大脑"
- "把 XX 归类 / 建个索引"
- "搜一下我本地关于 XX 的文件"

**执行流程**
1. **扫描走 File MCP**（白名单 `D:\腾讯AI`、`D:\AI技能仓库`）或 Desktop Commander 只读代理。
   - `directory_tree` 取结构 → `search_files` 按模式找 → `read_text_file` 读内容
   - **边界已由 MCP 强制**：越界路径会返回 `Access denied - path outside allowed directories`
2. **分类产出清单**（路径 + 大小 + 修改时间 + 主题标签），**只出清单，不移动不删除**。
3. **结构化沉淀**：长文档/方案 → `wb-doc-writing`；索引与体系 → 写到用户指定路径。
4. **去重**：发现重复内容 → `local-file-dedup`（先只读扫描出报告）。
5. 用户确认后再执行任何移动/合并。

**输出格式**
```markdown
# 资料分类清单 · YYYY-MM-DD
| 分类 | 文件数 | 代表文件 | 建议动作 |
|---|---|---|---|
| AI 技能/Skill | n | path | 保留 |
| 待归档 | n | path | 建议归入 X |
```
末尾附：**本清单仅为只读扫描结果，未移动/删除任何文件。**

**安全边界**
- 个人文件**一律先只读扫描**，不擅自移动/删除/改名
- 不读私钥、密码、银行支付相关文件；遇到即跳过并说明
- 不外传本地内容（除非用户明确要求且确认发送目标）

---

## 六、跨模块安全约束（不可违反 · 所有模块共用）

1. **不碰**：私钥、密码管理器、银行/支付相关数据
2. **个人文件**：先只读扫描，不擅自移动/删除
3. **不装**：企业办公类连接器（CRM / OA / 企业邮箱等）
4. **二次确认类**：删除 / 发送 / 支付 / 卸载 / 改系统设置 / 改注册表 → 说明理由 + 影响 + 可回滚性后再执行；属本次任务必需的清理，做并记录
5. **落点默认 D 盘**；C 盘不留本次产生的垃圾
6. **失败如实报**，不用猜测或旧数据填空

---

## 七、当前部署状态（2026-09-19）

| 连接器 | 状态 | 说明 |
|---|---|---|
| windows-mcp | ✅ 已验证 | uvx 安装；`args: ["windows-mcp","serve"]`（**必须带 serve**，否则 stdio 握手超时） |
| playwright | ✅ 已验证 | 本地 npm 包直调 node，`--browser msedge --headless`，复用已装 Edge，无需额外下载浏览器 |
| filesystem | ✅ 已验证 | 白名单 `D:\腾讯AI` + `D:\AI技能仓库`，C 盘越权已实测被拒 |
| desktop-commander | ✅ 已验证（只读） | 经 `D:\腾讯AI\tools\desktop-commander-readonly\readonly-proxy.js` 代理，仅暴露读/查看/进程查看类工具，写类工具硬拦截 |
| GitHub | ✅ connected | `gh` CLI 已登录 `luotiandong799-coder` |

**已知坑（勿重复踩）**
- Windows MCP 启动参数必须带 `serve` 子命令
- 中文输入不走 `Type`，走 `Clipboard` + `ctrl+v`
- `Type` 工具 `loc` 必填
- 新 Notepad 另存为必须给绝对路径
- Windows MCP 服务保持常驻时会占住 stdin，长任务建议分阶段重连，不要一个会话连打几十个动作
- PowerShell 工具调用结束时会清理未跑完的子进程，导致 uv 下载中断留陈旧 `.lock`

---

## 八、建议自动化（方案备选 · 创建前需用户确认）

### 方案 1：每日 AI 简报
- **频率**：每天 09:00
- **内容**：模块 D 流程 → 抓 AI 新闻 → 交叉验证 → 输出 3-5 条要点 Markdown
- **落点**：`D:\腾讯AI\yt\outputs\<日期>_AI简报\`
- **依赖**：Playwright MCP（headless 无需人工干预）

### 方案 2：每周电脑健康检查
- **频率**：每周日 10:00
- **内容**：模块 C 只读扫描 → CPU/内存/磁盘/异常进程体检表 + 清理候选清单（**只出清单不清理**）
- **落点**：`D:\腾讯AI\yt\outputs\<日期>_电脑体检\`
- **依赖**：Desktop Commander 只读代理 / PowerShell 工具

### 方案 3：每周资料库索引
- **频率**：每周六 20:00
- **内容**：模块 E 扫描 `D:\腾讯AI` → 更新分类清单 + 新增文件摘要
- **落点**：`D:\腾讯AI\yt\outputs\<日期>_资料索引\`
- **依赖**：File MCP

---

## 九、路由自查（每次使用本技能前过一遍）

- [ ] 我这次要做的事，属于 A/B/C/D/E 哪个模块？
- [ ] 该模块的**首选能力**我加载了吗（不是凭记忆复述）？
- [ ] 是不是在重复实现已有技能的能力？→ 如果是，停下来改走路由。
- [ ] 涉及删除/发送/支付/系统设置了吗？→ 走第二节第 4 条。
- [ ] 输出落到 D 盘了吗？截图/清单/文件留证了吗？
