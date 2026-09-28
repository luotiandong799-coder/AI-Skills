# personal-ai-os 知识库（references/knowledge-base.md）

> 2026-09-28 瘦身：SKILL.md 保持 ≤500 行，以下内容自正文下沉，信息零删减。
- §A = 原 §二十四～§三十三（信源生态与项目处置）
- §B = 原附录 C（部署状态实测）
- §C = 原附录 D 自查清单

---

# §A 原 §二十四～§三十三

## 二十四、GitHub 生态处理原则

GitHub 是**能力资源池，不是安装清单**。必须：
```
搜索 → 验证 → 分类 → 去重 → 安全审查 → 判断价值 → 决定安装/候选/学习/排除
→ 安装 → 配置 → 测试 → 验证 → 清理安装垃圾 → 记录
```
**不得机械安装。**（有疑问或不确定项目是什么 → 直接去 GitHub 搜。）

---

## 二十五、项目验证条件

每个候选项目至少检查：是否真正支持 WorkBuddy / 当前版本兼容性 / Windows 兼容性 / License / 维护情况 / 依赖 / 安装方式 / 安装脚本 / 所需权限 / 数据访问范围 / 是否重复 / 是否值得长期维护 / 是否有替代方案。
注意：**"支持 WorkBuddy"不等于腾讯官方项目。**

---

## 二十六、项目五级分类

- **A. 核心底座**：直接增强 Personal AI OS 核心能力 → 优先验证和安装。
- **B. 增强组件**：明显有价值但非绝对必要 → 验证后安装。
- **C. 按需 Skill**：只有实际任务需要时安装。
- **D. 学习资料**：学习其方法，不安装运行组件。
- **E. 淘汰 / 排除**：重复 / 过时 / 不兼容 / 安全风险 / 维护差 / 无实际价值 / 与 Personal AI OS 无关。

---

## 二十七、Skill / 能力管理

重点检查：WorkBuddy Skill Atlas / WorkBuddy Skill Hub / skill-manager / Skills Constitution / SkillCorpus / Skill Flow / oh-my-workbuddy / WG Skills / WorkBuddy Skills Collection / WorkBuddy AI Agent Skills Collection。
原则：**不同时长期运行多个解决同一问题的 Skill 管理器。** 最终选择：**一个主 Skill 管理系统 + 一个资源索引 / 备用方案。**

---

## 二十八、PC / Environment

重点检查：SOIA Open Env Skills / Windows 环境管理 / Runtime 管理 / Python·Node·Git / 网络诊断 / 存储清理 / 软件环境检查 / 安装验证。
采用：**检测 → 分析 → 修复 → 验证 → 清理残留**。
禁止：一键优化 / 注册表清理器 / 来源不明系统加速器。

---

## 二十九、Knowledge / Memory

重点检查：WorkBuddy Wiki / WorkBuddy Obsidian Plugin / Local Markdown Memory / Five-layer Memory System / llm-wiki Skill / Personal User Manual / AGENTS·Context 类系统。
长期知识必须 有价值 / 可维护 / 可修改 / 可删除 / 可审计。不要无限积累聊天噪音。
同类知识：**更新旧知识，而不是无限新建重复知识。**

---

## 三十、Harness / Agent 执行能力

重点检查：WorkBuddy Harness / WorkBuddy Harness Bluebook / WorkBuddy Runbook / LazyBuddy / Better Harness / Comet / Session Fork。
属于执行增强层，**不要全部安装**。相同能力只保留：更稳定、更安全、更兼容、更简单、更有效的方案。

---

## 三十一、Evaluation

重点使用：WorkBuddy Bench / 实际任务测试 / Baseline 对比。
安装前记录"原来的能力"，安装后比较"新的能力"，比较：成功率 / 稳定性 / 时间 / 错误率 / 人工介入 / 工具调用次数 / 资源消耗。
**如果没有实际提升 → 不保留。** Benchmark 后自动清理测试垃圾。

---

## 三十二、AI Learning

重点检查：AI 10x Learning / WorkBuddyGuide / WorkBuddy Starter / WorkBuddy Efficiency Training Course / Agent Learning Guide / Skill Onboarding / ZZZ Plain-language AI Guide / WorkBuddy Harness Bluebook。
学习必须尽量转化成：**知识 → 方法 → Skill → Workflow → 实际应用 → 验证**。

---

## 三十三、专业 Skill 资源池（按需使用，不要全部预装）

Public Agent Suite / SenseNova Skills / WG Skills / Frank Presales Skills / MOSS Skills / Ray Skills / MCK PPT Design Skill / Zotero MCP WorkBuddy Guide / 1688 Product Reader / Ecommerce Detail-page Planner / WorkBuddy WeChat Publisher / Travel Planner / Voice Refine Skill / Time Rhythm Planner。

---

# §B 原附录 C

# 附录 C：当前部署状态（2026-09-20 实测复验）

> 复验方式：每个连接器**真机发一次实际调用**，非"看开关是否打开"。

| 连接器 | 状态 | 实测证据 |
|---|---|---|
| windows-mcp | ✅ 端到端通过 | 截图 / `DisplayInventory`(2560×1600@144dpi) / UI 树 / 剪贴板读写 / 开应用 / 点击 全部成功；完整链路＝开记事本→`Clipboard set`→`ctrl+v`→截图确认文字→点"不保存"→进程已退出 |
| playwright | ✅ 端到端通过 | 导航 `example.com` 与**必应新闻动态页**并抽取可访问性树；headless Edge 带登录态（页面显示已登录账号） |
| filesystem | ✅ 通过（含越权拒绝） | 白名单 `D:\腾讯AI` + `D:\腾讯AI\skills`；实测读 `C:\Windows\win.ini` 返回 `Access denied - path outside allowed directories` |
| desktop-commander | ✅ 通过（只读） | 代理白名单 13 个只读工具（`read_file`/`list_directory`/`list_processes`…），显式拒绝 13 个写/高危工具（`write_file`/`edit_block`/`start_process`…）；实测 `get_config`（v0.2.51）+ `list_processes`（400+ 进程） |
| GitHub | ✅ connected | `get_me` → `luotiandong799-coder` |
| agent-mail | ✅ connected | `GetMe` 可取别名（已隐去），日发额度 50 封 |
| sheetagent | ⚠️ 需前置 | 服务存活，但未打开工作簿时返回 `MCP error -32603: No workbook open`（属正常前置缺失，非故障） |
| genie-baas（云服务） | ⚠️ 无目标 | 需 `applicationId`（取自 `.workbuddy/applications.yaml`）；当前工作区无该文件 → 无应用可查 |
| weixinpay | ⚠️ 绑定报错 | 服务有响应，但绑定流程返回"无法绑定微信支付AI专属卡：遇到了一些问题，请稍后重试" |

**已知坑（勿重复踩）**
- Windows MCP 启动参数必须带 `serve` 子命令。
- **`App` 的 `mode: "launch"` 按开始菜单名检索会失败**（2026-09-20 实测：`name: "notepad"` → `Notepad not found in start menu`）→ 改用 `mode: "launch_executable"` + `executable` 绝对路径（如 `C:\Windows\System32\notepad.exe`）。
- **`Click` / `Type` 的 `label` 只吃 Snapshot 返回的整数 id，不吃文字**；按坐标点击用 Snapshot 给出的**屏幕坐标**最稳（Screenshot 的图内像素需乘 `Screenshot Coordinate Scale`，实测 1.481481）。
- 中文输入不走 `Type`（SendKeys 不支持非 ASCII）：先 `Clipboard`（`mode: set`）→ `Shortcut ctrl+v`。
- `Type` 工具 `loc` 必填（坐标或元素标签），只给 `text` 会报 `Either loc or label must be provided`。
- 新 Notepad 另存为必须给绝对路径，否则提示"你不能保存到此电脑"。
- **windows-mcp 限制代理的已知边界**：`Registry` 整项移除、`FileSystem` 的 write/delete/move 拦截，但 **`PowerShell` 工具可执行任意命令，代理拦不住** → 真正兜底仍是系统权限 + 人工确认（勿把它当强隔离）。
- Windows MCP 服务常驻会占住 stdin，长任务建议分阶段重连，不要一个会话连打几十个动作。
- PowerShell 工具调用结束时会清理未跑完的子进程，导致 uv 下载中断留陈旧 `.lock`。
- **清理纪律**：UI 自动化测试收尾必须查残留——2026-09-20 复验时在 `D:\` 根发现上次测试遗留的 `Windows MCP 测试成功.txt`，已清。

---

# §C 原附录 D 自查清单

# 附录 D：路由自查（每次使用本技能前过一遍）

- [ ] 我这次要做的事，属于九大模块中哪个？要动的是 Skill / MCP / 电脑 / 知识 / 评估？
- [ ] 该模块的**首选能力**我加载了吗（不是凭记忆复述）？
- [ ] 是否在重复实现已有能力？→ 是则停下改走路由。
- [ ] 前置检查（目标/状态/能力/风险/资源/冲突）过一遍了吗？
- [ ] 属于 L0 / L1 / L2 哪级？L2 必须先取得明确确认。
- [ ] 是否触发停止条件（目标完成/副作用/风险升级/验证失败/连续失败/状态未知/资源异常/数据风险/权限不足/工具不可靠）？
- [ ] 收尾：清理临时文件·无用缓存·安装测试残留 + 检查残留进程/目录 + 记录 + 判断是否需优化？

# §E 补充下沉（同轮）

## 三十五、自动优化与淘汰

Personal AI OS 不允许无限膨胀。定期审查 Skill / MCP / Workflow / Expert / Harness / Connector / Memory / 本地工具 / 缓存 / 临时目录 / 下载残留。
处理结果：**保留**（高频·有价值·稳定·安全）/ **降级**（低频但偶尔需要 → 保留但不默认加载）/ **替换**（新旧测试 → 新方案通过 → 停用旧方案 → 清理旧残留）/ **删除**（重复·长期不用·已失效·不兼容·停维护·权限过大·安全风险·依赖过重·实际无提升·已被原生或更稳定方案替代）。
删除前保留必要回滚信息。

---

# §E 补充下沉（同轮）

## 三十九、跨 Agent 项目规则

跨 Agent 项目不是一律排除。只有同时满足：明确支持 WorkBuddy / 能独立运行 / 不依赖其他 Agent 才能工作 / 真正增强 WorkBuddy / 安全 / 稳定 / 没有更简单的原生方案 → 才进入候选；否则排除。

---

# §E 补充下沉（同轮）

## 四十、本地能力索引

持续维护能力索引（结构见 §一 九大模块），每个组件记录：
名称 / GitHub 地址 / 类型 / 功能 / WorkBuddy 兼容性 / Windows 兼容性 / License / 权限 / 依赖 / 当前版本 / 安装时间 / 使用频率 / 测试结果 / 是否重复 / 是否启用 / 是否值得保留 / 替代项目 / 回滚方式 / 清理方式。
（索引文件落 `D:\腾讯AI\yt\outputs\<日期>_PersonalAIOS能力索引\`。）

---

# §E 补充下沉（同轮）

## 四十一、AI Intelligence Radar

持续关注：新模型 / 新 Agent / 新 Skill / 新 MCP / 新 Harness / Computer Use / AI Computer / AI OS / Windows Agent / 浏览器 Agent / Automation / 开源项目 / AI 工具 / 商业机会 / 新职业方向。
发现更优方案：**对比 → 验证 → 测试 → 决策 → 替换 → 清理旧方案。** 不要因为"新"就直接安装。

---

