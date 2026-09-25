# 学习轮 r221C：skillsmp p73精选与Langflow 1.12运维面与OpenAgentSkill注册表与认知技能分类法（2026-09-25）

## 实拉记录（10 次调用，5 成功 / 5 失败计数）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/73（#7201-7256，5945/9929 取） | OK |
| 2 | dify.ai/blog 续读（163733-168442） | OK（Claude2 100K/LLMOps 历史面） |
| 3 | docs.langflow.org/next/release-notes（1.12.x 全） | OK |
| 4 | docs.n8n.io store-and-search-data-with-vectors.md | OK（1296 全） |
| 5 | GitHub Trending 搜索（Cognitive-Core-Skills/tech-leads-club/awesome-openclaw） | OK |
| 6 | deeplearning.ai 搜索（Long-Term Agentic Memory LangGraph/LangMem） | OK |
| 7 | docs.openclaw.ai/automation/automations | dead |
| 8 | activepieces.com/docs/triggers | dead |
| 9 | openagentskill.com | OK（首次成功 4234） |
| 10 | agentskills.io/overview | dead |

## 独点（4 个）
### C1：skillsmp p73 精选：会话开始工作恢复 / 空结果关键词增强 / 库文档实时查（来源：skillsmp.com/skills/page/73，2026-09-25 实拉）
- **working-memory（nowledge-co ★177）**：**会话开始加载跨工具 Nowledge context——显示当前工作、优先级、未解决 flags；Codex 本地 Memory 是分离的、不替代此 context；resume 或用户问"我在做什么"时触发**（工作恢复的加载面，与记忆提取互补）。
- **xianyu-hub（OpenMinis ★421）**：**Keyword Enhancement——搜索结果为 0 或极少时，自动从同品类加替代关键词重试，显著提高命中率**（空结果自动同义词重试的具体实现）。
- **context7-docs（upstash/context7 ★62,263）**：**任何库/框架/SDK/CLI 的最新文档+代码示例——训练数据可能不反映近期 API 变化；API 语法/配置/版本迁移/库特定调试都查；宁可实时查不用训练数据；库文档查询优先于 web search**。
- **p3c-code-quality（LeoYeAI ★2,128）**：阿里巴巴 P3C 规范代码质量检查——命名/异常/并发/数据库/OOP/安全/单测。
- **create-hook（microsoft/vscode ★192,746）**：创建 .json hook 强制执行策略或自动化 agent 生命周期事件。
- **提升层**：可复用 Skill / 工作流（恢复面+检索面）。

### C2：Langflow 1.12 升级与运维面：隔离升级流程 / microVM 沙箱 / preflight / 策略 API（来源：docs.langflow.org/next/release-notes，2026-09-25 实拉）
- **升级隔离流程（官方推荐）**：**新版本先装到新 venv 或 VM → export projects 备份（curl /api/v1/projects/download）→ import flows 测试 → 通过后再升主环境**；升级组件可用 "Create backup flow before updating" 选项。
- **langflow-base 成为完整版本对齐安装**：`langflow-base~=0.x` pin 全部换成 `~=1.12.0`。
- **bundle separation 完结**：**`uv pip install langflow` 只装 curated providers；缺的 provider 组件在编辑器可见但 flow 不 build，报错点名缺哪个包（如 `uv pip install lfx-exa`）**。
- **Python Interpreter microVM 沙箱**：**`LANGFLOW_SANDBOX_BACKEND=exec-sandbox` 让 Python Interpreter 组件跑在专用 QEMU microVM 而非 Langflow server 进程内**（`uv pip install 'langflow[sandbox]'`）。
- **Production preflight checks**：`LANGFLOW_DEPLOYMENT_PROFILE=prod` 在任何 worker 启动前探测部署；默认 dev 跳过。
- **LANGFLOW_TWEAKS_POLICY**：控制 API 调用方运行时能覆盖哪些组件字段；**Catalog and model policy APIs**：superuser 可封禁/放行组件、starter templates、模型提供方、具体模型。
- **Admin Page 移除**：用户管理走 Users API。
- **提升层**：工作流（升级/运维/沙箱策略）。

### C3：OpenAgentSkill：任务到技能的注册表 API + 信任档案（来源：openagentskill.com，2026-09-25 首拉）
- **定位**：**普通目录给人浏览；OpenAgentSkill 让 agent 自动发现/比较/安装合适技能——33,260 indexed skills / 25,513 projects / 33,794 validated**。
- **四层架构（intent 到 install）**：①intent capture（自然语言任务描述）→②recommendation engine（按 workflow fit/quality/freshness/audit 排名）→③skill trust profile（readiness notes/install commands/review prompts）→④agent install path（返回 agent 可安全执行的下一步）。
- **任务解析 API**：`POST /api/agent/resolve` 返回 recommended_skill+install_command+why_recommended+risk_summary（safety/notes）；`GET /api/agent/skills/{id}` 查信任档案；`GET /api/skills/{id}/install?format=text` 拿安装命令。
- **Safety before install**：stars/freshness/quality score/permission hints/risks/readiness notes 与安装命令同列（信任信号在安装前可见）。
- **执行环**：Discover → Inspect → Install（如 crawl4ai 96/100 fit）。
- **提升层**：工具 / 工作流（agent 侧技能发现层）。

### C4：认知核心技能分类法 + 验证注册表生态 + LangGraph 长期记忆增量（来源：GitHub Trending 检索 + deeplearning.ai，2026-09-25 实拉）
- **eli-labz/Cognitive-Core-Skills**：**通用认知核心技能分类法（perception/memory/reasoning/planning/action/verification/learning/governance 八类）——面向 LLM/SLM/agent/world model，含 schema+159 skill cards+benchmarks+CI**（认知技能的标准化分类面）。
- **tech-leads-club/agent-skills（★6,753，月 +1759）**：**secure, validated skill registry for professional AI coding agents——扩展 Antigravity/Claude Code/Cursor/Copilot 的验证注册表**。
- **awesome-openclaw-skills（VoltAgent）**：**5,400+ OpenClaw skills 从官方 Skills Registry 过滤分类**。
- **Long-Term Agentic Memory With LangGraph（deeplearning.ai，1h24m）**：**三种记忆 semantic/episodic/procedural；LangMem 管理；个人 email agent 把 facts/user preferences/evolving system prompts 存入可检索 memory store**（r220C 已落 Oracle Agent Memory 细节，LangGraph 三型记忆+LangMem 为增量）。
- **提升层**：工具 / 可复用 Skill（分类法与注册表面）。

## 判重说明
- C1 working-memory 会话开始加载/空结果关键词增强/context7 实时查为独有增量，落。
- C2 Langflow 1.12 升级隔离+microVM 沙箱+preflight+tweaks/catalog policy 全新（1.11 已落 r220B），落。
- C3 OpenAgentSkill 四层注册表+resolve API+信任档案全新站点首拉，落。
- C4 Cognitive-Core-Skills 八类 159 卡片/验证注册表/LangGraph 三型记忆为增量，落。
- 未落：openclaw automations（死）、activepieces triggers（死）、agentskills.io/overview（死）、dify 历史面（Claude2/LLMOps 低增量）、n8n 向量基础（r21x 已覆盖）。
