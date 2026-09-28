---
name: ai-input-enhancement
description: >-
  WB 统一 AI 信息入口的总架构原则与输入路由：外部信息如何归一进 AI、如何判断价值、如何路由到正确 Skill、隐私与记忆边界。当用户要梳理「统一输入/信息入口/输入增强/WeChatBridge/输入路由/价值判断/聊天增强/任务提取」或 WB 输入层架构，或要新增输入类能力时应用。本技能是编排/元层原则，不替代各引用 Skill 的执行细节，重叠>60% 一律引用不重复建。触发词：统一输入、信息入口、输入增强、WeChatBridge、输入路由、价值判断、聊天增强、任务提取、记忆管理、开源学习、Fast/Deep 执行。
version: 1.0.0
compatibility: WorkBuddy；引用 media/ engineering/ defaults/ agent/ system/ rules/ 下现有 skill（不重复建）
---

# AI 输入入口增强系统（WeChatBridge 融合终版）

> 本技能为**编排/元层原则**，非执行手册，能力由引用 Skill 提供。总入口见 `00_总目录_所有AI入口.md`。

## 边界（先读）
本技能定义「入口如何归一、何时路由」，**能力由引用 Skill 提供**，不是执行手册。它不是 `wb-context-compressor` 的副本，也不是 `wb-spec-driven` 的路由表——价值判断细节看 context-compressor，流程/路由细节看 spec-driven，验证看 artifact-verification。

## STOP / WAIT / PROCEED
| 状态 | 动作 |
|---|---|
| 已有 Skill 覆盖该能力 | **STOP**——直接引用，不重复写 |
| 要落地新输入能力 | **WAIT**——先查现有 skill 重叠；>60% 则引用不建 |
| 确属独特点 | **PROCEED**——落到对应 skill 或本技能独点段 |

## 目标
将 WB 打造成统一 AI 信息入口：
```
信息获取 → 内容理解 → 价值判断 → 任务提取 → 调用 Skill/Agent → 执行验证 → 经验沉淀
```
少重复操作，提 AI 使用效率。

---

# 一、总原则

## 1. 不新增重复 Skill
新输入能力先查已有：消息处理 / Windows 操控 / 文件处理 / 浏览器 / 记忆管理 / 自动化 / 执行验证 类 skill。
- 已有能完成 → 直接复用
- 已有不足 → 合并增强
- **禁止**：为单一功能建重复 skill、为数量增无价值 skill

# 二、统一 AI 输入层（AI Input Layer）
所有外部信息先经统一输入层，归一为 `{ type, source, raw, meta }`。

## 文本输入
来源：微信复制文本 / QQ 消息 / 浏览器文本 / 网页内容 / 剪贴板 / 文档文字。直入处理流。

## 图片输入
来源：微信聊天截图 / 图片资料 / 页面截图 / 图片文件。
```
图片识别 → 文字提取 → 语义理解 → 任务分析
```
实现见 `media/image-processor`、`media/wb-media-forensics`。

## 文件输入
支持 PDF / Word / Excel / 图片 / 压缩文件。
```
读取 → 分析 → 总结 → 提取行动项
```
实现见 `engineering/wb-doc-file-intel`、腾讯文档系（`tencent-docs` / `tencent-docx`）；浏览器来源见 `system/browser-automation`。

# 三、统一信息处理流程
```
输入信息 → 识别来源 → 识别类型 → 提取核心内容 → 补充上下文
→ 判断用户目标 → 选择对应 Skill/Agent → 执行 → 验证结果 → 记录有效经验
```
流程骨架 `engineering/wb-spec-driven`；执行纪律 `engineering/wb-execute-discipline`（点名目标须真实执行）；验证 `engineering/wb-artifact-verification`。

# 四、信息价值判断
收到信息先判价值，筛选机制见 `defaults/wb-context-compressor`。

## 高价值（进任务管理或记忆）
工作任务 / 重要沟通 / 长期偏好 / 决策依据 / 可复用经验 / 已验证方案。

## 中价值（当前任务用，不长期存）
临时资料 / 一次性分析 / 普通咨询。

## 低价值（不保存，避免污染记忆）
普通闲聊 / 重复信息 / 无后续价值通知。

# 五、聊天信息增强能力
针对微信、QQ 等。

## 1. 自动理解上下文
分析：沟通对象 / 当前主题 / 前后关系 / 用户目的 / 历史相关信息 → 输出当前情况、核心问题、建议方案。
通道：`system/wechat-desktop-claw-automatic-control__skillhub`（只发不读）、`system/workbuddy-claw-wechat-send`；对外发消息见 `rules/04_wecom企业微信`（默认先确认，企微直发原样透传）。

## 2. 回复辅助
生成时考虑：联系人关系 / 历史交流方式 / 当前语境 / 用户表达习惯。
```
普通消息：分析 → 生成建议
重要消息：生成 → 检查 → 用户确认 → 发送
```
**禁止**：未经确认自动发高风险消息。

# 六、自动任务提取
聊天/文件/网页分析后自动提取：
```
任务：
负责人：
时间：
优先级：
下一步行动：
```
例：原消息「月底前提交方案」→ 任务：提交方案 / 时间：月底前 / 下一步：整理资料并生成初稿。
结构化落地见 `engineering/to-tickets`。

# 七、AI 输入路由系统
```
所有输入 → AI Input Router → 判断需求 → 调用对应能力
```
调用顺序：① 专用 Skill ② 已有 Workflow ③ 通用能力 ④ 新建能力。
**禁止**：多 Skill 同时抢占任务。未匹配走 `wb-spec-driven` 的显式默认路由（不静默丢弃）；跨 agent 交接见 `agent/agent-guild`。

# 八、隐私安全规则
默认：不读微信数据库 / 不扫无关聊天 / 不取未授权信息 / 只处理用户主动提供内容。
高风险操作（自动发消息 / 删文件 / 改重要数据 / 外部账号操作 / 权限变化）**必须**：执行前确认 → 执行中检查 → 执行后验证。
细则：敏感输入走 `wb-artifact-verification` 护栏四模式（block/redact/retry/require-approval）+ secret/PII 检测器；密钥/token 不提交（`rules/06`）；用户真实文件优先回收站。

# 九、记忆管理规则
只存长期有价值信息：用户长期偏好 / 常用工作方式 / 有效方案 / 已验证流程 / 重要经验。
不存：临时聊天 / 一次性信息 / 无价值内容。目标：提未来效率，避免垃圾记忆。
规范见 `rules/07_记忆管理规则`；共学双写 `memory/co-learn/<工具名>/`，命名 `YYYY-MM-DD_主题.md`。

# 十、开源项目学习机制
学：微信 AI 工具 / Agent / Skill / MCP 项目。流程：
```
发现 → 分析核心能力 → 查已有体系重复 → 删无用部分 → 改造成 WB 能力 → 合并进现有系统
```
**禁止**：直接复制项目 / 引复杂无用功能 / 增重复 skill。调度见自动化 `070cce0c`；信源含腾讯 SkillHub `skillhub.cn/skills?sortBy=score` 分数面。

# 十一、执行标准
简单任务：Fast 模式（直接做，先报步数）。复杂任务：Deep 模式（计划→实现→验证，`wb-spec-driven` + `wb-debug-loop`，失败≥2 次必根因）。
执行要求：判断需求 → 制定方案 → 调用能力 → 执行 → 验证 → 总结。
默认三件套常开：`wb-ponytail` / `wb-max-token-saver` / `wb-context-compressor`。

# 十二、最终目标
让 WB 从「回答问题的 AI」升级为「理解信息、整理任务、辅助决策、推动执行的个人 AI 系统」。
核心：少而精 · 优先复用 · 快速执行 · 结果可验证 · 持续优化。
