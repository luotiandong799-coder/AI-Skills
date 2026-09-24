# 学习轮 r200-A：Pipedream组件能力差异表与ClaudeCode插件打包体系与生成器-评估器迭代与OpenClaw网关定位与评测驱动选技能（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/model/overview | 死链 |
| 2 | docs.n8n.io/embed | OK 全文 |
| 3 | docs.langflow.org/custom-components | 死链 |
| 4 | make.com/en/help/scheduling/ | fetch error |
| 5 | pipedream.com/docs/components/api | OK 全文 16165 字 |
| 6 | docs.anthropic.com/en/docs/claude-code/plugins | OK 全文 5860 字 |
| 7 | skills.sh/hot | OK 首页（安装命令） |
| 8 | skillsmp.com/skills/page/6 | OK（#501-540） |
| 9 | docs.openclaw.ai/ | OK 全文 |
| 10 | GitHub 生态（openagentskill 搜索） | OK |

## 独点（5 个）
### A1：Pipedream sources vs actions 能力差异表 + props 四类 + secret 加密（来源：docs.pipedream.com/components/api 全文）
- **七维差异表**：type 字段（action 需 `type: "action"`，source 不设）；事件出口（sources 用 `this.$emit` 触发 workflow + **dedupe 仅 sources**；actions 用 `return`/`$.export` 给后续步骤）；hooks（activate/deactivate/deploy **仅 sources**）；`$` 变量（actions 专属：发数据/导出/返回 HTTP 响应）；开发（sources 可用 `pd dev` 迭代，actions 不能）；部署（`pd deploy` sources / `pd publish` actions）；**interfaces 仅 sources**（可挂 HTTP endpoint/timer，定义如何被调用；actions 无 interface 因为在 workflow 内逐步跑）。
- **props 四类**：User Input（部署时接受输入）/ Interface（挂 HTTP/timer）/ Service（KV 状态存储）/ App（managed auth）。
- **secret prop**：仅 string 类型，隐藏输入 + 加密存储 + 运行时解密；**async options 三分页参数**（page 数字分页 / prevContext 游标 + 返回 {options, context:{nextPageToken}} / query 实时搜索需 useQuery）；**propDefinition 跨组件复用** app 定义的 prop（可箭头函数引用前置 prop 值）。
- 组件即 Node.js 模块跑在 serverless；npm 包直接用无需 install；1,400+ apps managed auth。
- 判据：**sources 与 actions 是同 API 两种生命周期**——事件源要可挂接口、可迭代、可去重；动作要能出口数据给下游；props 是组件复用与安全边界（secret）的主入口。
- **提升层**：工具 / 工作流。

### A2：Claude Code 插件 = 打包分发单位——standalone 先迭代、plugin 再共享（来源：docs.anthropic.com/en/docs/claude-code/plugins）
- **对照表**：standalone（.claude/ 目录）技能名 `/hello`，适合个人/项目/快速实验；plugin（独立目录 + `.claude-plugin/plugin.json`）技能名 `/plugin-name:hello`，适合团队共享/社区分发/**版本化发布**——**先 standalone 快速迭代，能分享时再迁 plugin**。
- **plugin.json 字段**：name（唯一标识 + skill 命名空间前缀）、description、version（**bump 才推送更新**）、author/homepage/repository/license。
- **目录纪律**：`.claude-plugin/` 只放 plugin.json；skills/commands/agents/hooks/.mcp.json/.lsp.json/monitors/bin/settings.json 全在插件根——常见错误是把组件目录放进 .claude-plugin/。
- **background monitors**：`monitors/monitors.json` 数组（name+command，如 `tail -F ./logs/error.log`），**插件启用即自动启动监控，每行 stdout 作为通知投递给 Claude**——"插件自动盯日志，事件来了主动报"。
- **settings.json 默认设置**（目前仅 agent/subagentStatusLine）：`{"agent": "security-reviewer"}` 激活插件自定义 agent 为主线程，**插件能改变 Claude Code 默认行为**；settings.json 优先于 plugin.json 的 settings。
- **评测**：`claude plugin eval`——每条 prompt 带/不带插件各跑多次，看插件贡献并防回归（换模型/改插件后回归可测）；`--plugin-dir` 本地加载（zip 可），同名时本地优先于 marketplace 安装版（managed 强制除外）；`claude plugin init` 脚手架；单技能插件可把 SKILL.md 放插件根。
- 判据：**可复用能力的单元是"插件"而非单文件**——命名空间防撞、version 控更新、monitors 自动监控、eval 证贡献；打包与快速实验分离，别一开始就上插件。
- **提升层**：可复用 Skill。

### A3：生成器-评估器迭代（GAN 启发）+ 单会话角色模拟 + throwaway 原型（来源：skillsmp #520/#501/#525）
- **gan-style-harness（ECC）**：基于 Anthropic 2026-03 harness 设计论文——**Generator-Evaluator 迭代直到过质量线**，特性自主构建；与 wb-execute-discipline"生成→验证→回退"同源，但它明确是"两个角色的对抗/迭代循环直到通过质量栏"。
- **dev-team（ECC）**：单会话模拟多角色 dev team（PM/Architect/Developer/QA 对同一问题各自表态）——**不切换 agent 的多角色视角**，适合设计评审/提案 review。
- **prototype（mattpocock）**：**throwaway prototype 答设计问题**（状态模型是否合理/UI 该长什么样）——一次性原型是探索工具不是交付物，用完即弃。
- 判据：**"过质量线才停"的迭代是循环不是单次生成**；多角色视角可以同一会话内角色扮演获得；原型的目的就是被扔掉——探索类问题别写生产级代码。
- **提升层**：工作流。

### A4：OpenClaw = self-hosted gateway——聊天↔agent 桥、单 Gateway 是真相源（来源：docs.openclaw.ai 根页）
- 定位：**自托管网关**连接聊天应用（Discord/Signal/Telegram/WhatsApp/Zalo 等）↔ AI coding agents；**单 Gateway 进程是会话/路由/通道连接的唯一真相源**；同一部署可个人用（笔记本）或团队用（配置不同）。
- 差异化：self-hosted（自己的硬件自己的规则）/ 多通道（一个 Gateway 服务所有 channel plugin）/ agent-native（工具使用/会话/记忆/多 agent 路由）/ MIT + 501(c)(3) 基金会 + 无付费层 + 无遥测（版本检查可关）。
- **多 agent 路由**：按 agent/workspace/sender 隔离会话；移动节点（iOS/Android 配对相机/屏幕/语音）；Web Control UI（127.0.0.1:18789）；Skills 按需加载；cron/hooks/webhooks 自动化；Node 26。
- 判据：**"gateway 真相源 + 通道插件化 + 会话按 sender 隔离"是个人 AI 基础设施的架构样本**；入口多样（聊天/CLI/UI/移动）但状态单源。
- **提升层**：生态观察。

### A5：评测驱动选技能——Agent Proven 实测证据 + 7 天活动排名 + 成功率排序（来源：openagentskill.com 榜单系）
- openagentskill 指标体系：**fit 分数**（workflow 关键词匹配）+ Trust Score + 质量信号 + **Agent Proven（agent 调用/成功的报告证据）** + 维护新鲜度 + 清晰安装路径——选技能排序 = 工作流匹配 × 质量 × 实测证据 × 新鲜度。
- **best-by-success-rate 榜**：按 reported success rate + recent success + output quality + install success + Trust Score 排序（30 条展示/471 候选）——**以"实测成功率"排技能**是新评测维度。
- **Trending 按 7 个完整 UTC 天活动排名**（不是 lifetime stars）；New this week 抓新入库；grill-me 技能在站上 98 分（本库已装技能的外部验证）。
- 判据：**选技能/插件看"代理实测证据 + 近期活动 + 成功率"三维**，不只看星星数；评测分数本身要能解释（fit/trust/proven 权重公开）。
- **提升层**：工作流。

## 判重说明
- A1 → r198-C C2（components 架构）/r199-A A1（sources 消费）已记；本篇首次拉 components/api 全页，**七维差异表 + props 四类 + secret + async options 分页 + propDefinition** 为独有增量。
- A2 → r199-C C3（MCP 管理）已记 plugin 捆绑 MCP；plugins 页首次拉全，standalone→plugin 迁移 + 命名空间 + monitors + settings 激活 + plugin eval 为独有增量。
- A3 → r198 多 agent 协作（按技能建 agent 等）已记；gan-style-harness/dev-team/prototype 首次见，迭代过质量线 + 角色模拟 + throwaway 原型为独有增量。
- A4 → OpenClaw 子页（cron/automation/progress）已多轮拉过；根页首次拉全，gateway 真相源 + 多 agent 路由隔离 + 移动节点为独有增量。
- A5 → r198-C 已记 skillleaderboard/repositorystats；openagentskill 指标体系首次见，Agent Proven + 成功率排序 + 7 天活动为独有增量。
