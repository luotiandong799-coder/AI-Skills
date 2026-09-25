# 学习轮 r213-C：Anthropic claude-code plugins官方与OpenClaw automation schedules官方与skillsmp p49与Langflow agents（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/49（#4801-4854，6000/11102 取） | OK（wechat-reader/open-code-review-delegate/tender-master 等） |
| 2 | dify.ai/blog 续读（48746-54378） | OK（Introducing Trigger/Kakaku/TiDB Vector） |
| 3 | docs.anthropic.com claude-code/plugins（5860B 全） | OK（插件结构/monitors/plugin eval/市场审核） |
| 4 | docs.langflow.org/agents（4990/5558 取） | OK（Tool Mode/Agent memory） |
| 5 | pipedream.com/docs（824B 全） | OK（1M+ 开发者/source-available 注册表） |
| 6 | github.com/trending 续读（7303-11430） | 低收获（hindsight 重复） |
| 7 | deeplearning.ai/short-courses 续读（16986-21425） | OK（AI Agents for Image/Video 自动评估迭代） |
| 8 | skillhub.cloud.tencent.com 首页重拉（4283/44457 取） | 重复（与 r212-C C2 相同） |
| 9 | docs.openclaw.ai/automation/cron-jobs/schedules（3279B 全） | OK（五类 schedule/pacing/condition watcher） |
| 10 | make.com/en/help（227B 全） | OK（Make AI 全用户/Audit Log/Scenario inputs） |

## 独点（4 个）
### C1：Anthropic claude-code/plugins 官方页：插件结构 / monitors 背景监控 / plugin eval / 市场审核（来源：docs.anthropic.com/en/docs/claude-code/plugins，2026-09-25 实拉）
- **插件 vs 独立配置**：Standalone `.claude/`=个人工作流/快速实验；Plugins（`.claude-plugin/plugin.json` manifest）=共享/分发/版本化；先 standalone 迭代再转插件。
- **manifest 字段**：name（唯一标识+skill 命名空间前缀 `/my-first-plugin:hello`）/description/version（bump 才发更新）/author。
- **结构铁律**：`.claude-plugin/` 只放 plugin.json——**commands/agents/skills/hooks 必须在插件根**（常见错误）；组件目录：skills//commands//agents//hooks/hooks.json/.mcp.json/.lsp.json/**monitors/monitors.json**/bin（Bash PATH）/settings.json（仅 agent 与 subagentStatusLine 两键）。
- **背景监控 monitors（插件组件）**：`tail -F ./logs/error.log` 每行 stdout 作为通知投递给 Claude——监控即插件，不用教 Claude 启动 watch。
- **plugin eval**：每个 prompt 带/不带插件多次运行，量化插件贡献与回归；`claude plugin validate ./your-plugin` 提交前本地验证（警告不失败，--strict 视为错误）。
- **社区市场**：`claude-plugins-official`（Anthropic 策展，无申请流程）+ `claude-community`（提交后审查，**pin 到 commit SHA**、CI 自动 bump、目录每晚同步）；`--plugin-dir` 支持文件夹（v2.1.265+，即时子文件夹各自成插件，交互会话中增删实时加载）。
- **提升层**：可复用 Skill（插件化分发体系）。

### C2：OpenClaw automation schedules 官方页：五类 schedule / pacing 动态节奏 / condition watcher（来源：docs.openclaw.ai/automation/cron-jobs/schedules，2026-09-25 实拉；与 wb-execute-discipline 既有三条同源合并保留增量，增量 ≥40%）
- **五类 schedule**：`at`（一次性 ISO/相对）/`every`（固定间隔）/`cron`（5-6 字段+--tz）/`on-exit`（**被监控命令退出时触发一次**，事件触发、survives turn teardown）/`stream`（**监督长驻命令的 stdout/stderr 行触发**）。
- **stream 批处理细节**：mode line（默认每行）vs match（正则整行匹配）；batchMs 默认 250ms（clamp 50-5000）；maxBatchBytes 默认 16384（clamp 1024-65536）；只保留一个 payload fire+一个 bounded pending batch（30 秒间隔内合并）；失败 payload 不重试（可能非幂等）；无原生 WebSocket source（用 websocat 桥接）。
- **pacing 动态节奏**：pacing.min/max 时长串（15m/4h）；agent-turn 运行中调 `automations` 工具 `action:"next_check", in:"30m"` 提议下次检查（从成功完成计，clamp 到边界；失败/超时/跳过丢弃提议）。
- **condition watcher（事件触发）**：headless 条件脚本返回 `{fire, message?, state?}`；**state 16KB 上限**；fire:false 静默评估（计完成次数）；**每次评估 30 秒 wall-clock 预算+最多 5 次工具调用**；once:true 首次成功后禁用；**写 watcher 围绕可操作状态而非仅成功**（检查失败时安静=看似健康实则坏了）；**条件脚本与 script payload 默认以拥有 agent 的完整工具策略运行（含 exec）——无人值守代码执行面**，`cron.triggers.enabled:false` 硬停。
- **croner OR 逻辑**：day-of-month 与 day-of-week 非通配时任一匹配；`+` day-of-week 修饰符（`0 9 15 * +1`）要求 AND。
- **提升层**：工具 / 工作流（自动化五形态与守卫细节）。

### C3：skillsmp p49 精选：微信反爬专用 / 确定性 vs LLM 分工 / 标书方法论 / 同名任务路由（来源：skillsmp.com/skills/page/49，2026-09-25 实拉）
- **wechat-reader（yangwhale/CloseCrab ★3）**：读微信公众号文章——**模拟微信内置浏览器绕过反爬 CAPTCHA**；mp.weixin.qq.com 链接必须用它替代 WebFetch/Jina（那些会报"环境异常"CAPTCHA 失败）。
- **open-code-review-delegate（alibaba/open-code-review ★38,832）**：**OCR 委托模式**——不是 OCR 调 LLM 端点，而是指示宿主 agent 自己做 code review，OCR 只用于确定性工程（文件选择与规则解析）——"确定性 vs LLM 分工"。
- **tender-master（railwise-cn/tender-master ★4）**：招投标全流程编制——**目录=评分表镜像、每条要求逐条响应、风控内容与正文物理隔离、不编造资质案例参数**。
- **make-textbook-figure（lingxiaobc ★0）**：教材级黑白矢量插图（SVG 线条+LaTeX/MathJax 公式）；**与 make-infographic 路由区分：黑白精确教学图（准确性驱动）vs 彩色信息图（版式驱动）**——同名任务按用途路由。
- **deep-research（XiaomiMiMo/MiMo-Code ★13,225）**：并行子 agent+内置工具只（WebSearch/WebFetch+免费 API 无 key）；NOT for 简单查询（single WebSearch 足够）、NOT for 学术综述（用 auto-research）——边界写清。
- **xhs-article-to-images（Pluviobyte/rnskill ★1,586）**：长文转小红书 3:4 图组——Agent 读文章拆页填 HTML、Playwright 渲染器逐张截图 PNG（Agent+渲染器分工）。
- **提升层**：可复用 Skill / 工作流。

### C4：Langflow agents Tool Mode + Agent memory + 生成-评估迭代（来源：docs.langflow.org/agents + deeplearning.ai，2026-09-25 实拉）
- **Langflow Tool Mode**：**任意组件可变成 agent 工具**（开启 Tool Mode 后组件有 Toolset 端口连 Agent Tools 端口）；agent 可用任何组件作工具（包括其他 agent 和 MCP server）；MCP Tools 组件连外部 MCP。
- **Agent memory**：内置 chat memory 默认开启，**按 session_id 分组**（自定义 session_id 隔离不同用户/应用）；Message History 组件用于外部记忆（如 Mem0）；**Structured Response 输出时不发事件、不写聊天历史**。
- **AI Agents for Image and Video Generation（Google）**：构建生成图片/视频的 agent——**自动评估输出并迭代直到结果达到质量标准**（生成-评估-迭代闭环）。
- **提升层**：工作流 / 工具。

## 判重说明
- C1 → claude-code/plugins 官方全量（插件结构/monitors/eval/市场），新页，落。
- C2 → OpenClaw automation schedules 官方全量（五类 schedule/pacing/watcher），与 wb-execute-discipline 既有三条同源合并保留增量（增量 ≥40%），落。
- C3 → skillsmp p49 精选（微信反爬/OCR 委托/标书镜像/路由），全新，落。
- C4 → Langflow Tool Mode+Agent memory + 生成-评估迭代，工作流层增量合并，落。
- 未落：SkillHub 首页重拉（与 r212-C 重复）、hindsight（重复）、intelligence-network-espionage（间谍情报技能安全红线不落）、adult-nsfw（色情不落）、github trending（低收获）、Pipedream docs（平台级事实，低方法）。
