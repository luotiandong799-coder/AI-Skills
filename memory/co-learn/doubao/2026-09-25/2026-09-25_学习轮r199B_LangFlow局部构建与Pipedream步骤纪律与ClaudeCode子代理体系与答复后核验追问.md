# 学习轮 r199-B：LangFlow局部构建与防篡改公开执行与Pipedream步骤纪律与ClaudeCode子代理体系与答复后核验追问（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/api-reference | 导航壳 |
| 2 | docs.n8n.io/integrations | security 拦截 |
| 3 | docs.langflow.org/api | OK 全文 25870 字 |
| 4 | make.com/en/help/scenarios/ | fetch error |
| 5 | pipedream.com/docs/workflows/ | OK 全文 |
| 6 | docs.anthropic.com/en/docs/claude-code/agents | OK 全文 11758 字 |
| 7 | skills.sh/latest | 死链 |
| 8 | skillsmp.com/skills/page/4 | OK（#301-334） |
| 9 | docs.activepieces.com/docs/advanced/ | fetch error |
| 10 | GitHub 生态（trendshift 搜索） | OK |

## 独点（5 个）
### B1：LangFlow API 局部构建与防篡改公开执行——start/stop 组件 + 不接收 data 参数（来源：docs.langflow.org/api 全文）
- **局部构建**：POST /build/{flow_id}/flow 支持 `start_component_id` / `stop_component_id`——**从任意组件开始/在任意组件停止执行**（不是整流程重跑）；返回 job_id 轮询事件；event_delivery 三模式 streaming/direct/polling。
- **三种 Run 端点**：/run/advanced/{id}（inputs 按组件定向注入 + outputs 可选 + tweaks 覆盖组件参数 + session_id 复用）；/run/{id}（简化：input_type/input_value/output_component，streaming + telemetry，**从 HTTP headers 提取全局变量 `X-LANGFLOW-GLOBAL-VAR-*` 注入 flow**）；/webhook/{id}（异步 202）。
- **防篡改公开执行**：build_public_tmp **不接受 data 参数**（防 flow 定义篡改，只能执行数据库存储的定义）+ 用 client_id cookie 生成**确定性 UUID**（跟踪用途）+ 用 flow owner 权限执行。
- **job 所有权安全**：Cancel Build 需 ownership 验证防 DoS（不能 abort 别人 job）；Get Build Events owner 不匹配返回 404 **防 job 存在性泄露**。
- 判据：**"从中间节点起止执行"= 流程级 debug 与局部重跑**；公共 flow 的执行定义必须锁定、输入必须走注入而非覆盖定义；作业存在性本身要防探测。
- **提升层**：工具 / 工作流。

### B2：Pipedream 步骤纪律——exports 必须 JSON 可序列化、props 仅 Node、step 名禁空格破折号（来源：docs.pipedream.com/workflows）
- **step exports 必须 JSON serializable**（跨步骤传数据的前提）；step name 禁空格/破折号（用下划线或驼峰），改名后**必须同步更新所有引用**（steps.get_data 等）。
- **props 仅 Node.js code steps 支持**（Python/Bash/Go 不支持 form 化输入）；step notes 支持 markdown 但**只在 Build 模式可见**（Inspector 无）。
- 一个 workflow 可加**多个 trigger**（不同事件触发同流程）；2,500+ 集成应用；保存即部署到服务器，**浏览器是否打开都执行**。
- 判据：**跨步骤契约 = JSON 可序列化 + 稳定命名 + props 化复用**；换语言会丢 props 能力（平台能力不是均匀的）。
- **提升层**：工作流。

### B3：Claude Code 子代理体系——内置三型 + 工具黑白名单 + maxTurns 防失控 + worktree 隔离（来源：docs.anthropic.com/en/docs/claude-code/agents）
- **内置三型**：Explore（Haiku、只读禁 Write/Edit、委托时指定 thoroughness quick/medium/very thorough）；Plan（plan mode 研究、只读、**subagents 不能 spawn subagents 防无限嵌套**）；general-purpose（全工具，复杂多步）。
- **frontmatter 关键字段**：tools（省略=继承全部）/ **disallowedTools（从继承列表删工具）** / model（alias/完整 ID/inherit）/ permissionMode / **maxTurns（最大 agentic 轮数防失控）** / **skills（启动时注入完整 skill 内容——不继承父对话 skills）** / memory（user/project/local 持久记忆 ~/.claude/agent-memory/）/ **isolation: worktree（临时 git worktree 隔离仓库副本，无改动自动清理）** / background / initialPrompt。
- **scope 优先级**：managed > --agents CLI（JSON 会话级临时，不落盘）> project .claude/agents/ > user ~/.claude/agents/ > plugin（最低）；**插件 subagent 不支持 hooks/mcpServers/permissionMode（安全原因字段被忽略）**——要用的复制到 .claude/agents/。
- **模型解析顺序**：CLAUDE_CODE_SUBAGENT_MODEL env > 本次调用 model 参数 > frontmatter > 主对话模型。
- subagent 只收到自己的 system prompt（+cwd 等基础环境），不是完整 Claude Code system prompt；subagent 内 cd 不持久不影响主对话。
- 判据：**子代理是"隔离上下文 + 限制工具 + 限定轮数"的三重沙箱**；委托依据 description 显式声明；降级到脚本用 --agents JSON 不落盘。
- **提升层**：Agent 编排。

### B4：答复后核验追问（discernment-nudge）——定稿前追加 2-3 个核对问题，一次对话至多一次（来源：skillsmp #304 anthropics/skills 官方）
- 触发：给出用户可能行动的实质答复/草稿（建议、计划、提案、邮件、估算、数据分析、可依赖的事实声明、多步论证）**定稿前调用**，追加 2-3 个与产出具体内容绑定的追问，帮用户核对关键事实、探测推理/假设、发现缺失上下文。
- **跳过边界**：trivial how-to、纯教育解释、纯格式/转换/组装、用户要跑会执行的代码、创意写作/闲聊、用户已要求 double-check——**守住边界不打扰**。
- 同页可内化：**token-budget-advisor（ECC）**——回答前给用户显式选择消耗多少响应深度（与 wb-max-token-saver 的"按需裁剪"互补：那条是默认机制，这条是对话内显式选择）；**cangjie-skill 10,385★**——把书/长视频/播客/课程蒸馏成可执行技能集（拆书→原子可复用 skill，与学习留痕体系同思路）；huashu-design 24,324★——任何新设计 100% 先出三个方向初稿（指定风格也不豁免）。
- 判据：**有价值的追问是"与产出绑定的核对项"不是通用确认**；追问本身要遵守打扰边界；给用户预算选择权优于替用户定默认深度。
- **提升层**：输出 / 工作流。

### B5：GitHub 生态——桌面协调器 + 个人 agent + 无 Docker 框架（来源：trendshift 周榜）
- **Recursive-Cognitive-Optimization-RCO**：Claude Code/Codex 桌面应用的视觉协调器——shared tasks / review checkpoints / automated checks（多桌面 agent 的检查点式编排）。
- CopilotKit/openmuse：personal agent（browser+terminal+files+持续工作）基于 AG-UI；**ApodexAI/FrontierAgent**：native TUI + ReAct + Agent Team 模式，**无预装、无硬 Docker 依赖**（一键运行是差异化）；alibaba/page-agent 网页交互自动化；karpathy/autoresearch 单 GPU 训练自动研究。
- 判据：**"桌面级编排"与"无依赖一键跑"是 2026 agent 工具的两大卖点**；检查点（checkpoint）比日志更适合作多 agent 协作同步点。
- **提升层**：工具 / 生态观察。

## 判重说明
- B1 → r196-C/r197-C 已记 LangFlow Tool Mode/File/Dual output；API 页首次拉，局部构建 + build_public_tmp 防篡改 + header 全局变量 + job 所有权为独有增量。
- B2 → r198-C C2/r199-A A1 已记 Pipedream components/sources；workflows 页首次拉，exports JSON 纪律 + props 仅 Node + step 命名 + notes 仅 Build 为独有增量。
- B3 → r199-A A2 已记 skill 调用控制；agents 页首次拉，内置三型 + disallowedTools/maxTurns/isolation + scope 优先级 + 插件安全降级 + --agents JSON 为独有增量。
- B4 → r197-B 已记 token saver 变体；discernment-nudge/cangjie-skill 首次见，追问模式 + 蒸馏成技能为独有增量。
- B5 → r199-A A5 已记 GitHub 生态；RCO/openmuse/FrontierAgent 首次见。
