# 学习轮 r198-B：LangFlow安全责任边界与Pipedream分层集成与DSH万级插件目录与四层记忆与Markdown记忆架构（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/v2/api | 死链 |
| 2 | docs.n8n.io/data/data-mapping | OK |
| 3 | docs.langflow.org/security | OK 全文 |
| 4 | activepieces.com/docs/getting-started | 死链 |
| 5 | make.com/en/help/modules/types-of-modules | 标题壳 |
| 6 | docs.anthropic.com tool-use | region 不可用 |
| 7 | pipedream.com/docs/apps | OK |
| 8 | skills.sh/skills | OK |
| 9 | deepseek-plugin.org/plugins | OK 全文 |
| 10 | GitHub AI 生态（robots 禁走搜索） | OK |

## 独点（5 个）
### B1：LangFlow 安全责任边界声明——IDE 即代码执行平台，不隔离用户（来源：docs.langflow.org/security）
- 官方明示：Langflow 本质可执行**任意 Python，带后端进程/文件系统/网络全权限**；**不隔离用户、不限制磁盘网络**；flow 可见性为可用性设计非安全执行；多租户必须靠**基础设施级隔离**（进程/磁盘/网络/数据库四层），应用级不提供；可禁用 custom component execution、容器化运行；LLM 生成代码或用户提交代码是责任点。
- 判据：**代码执行类平台的信任模型=完全信任或完全隔离，没有中间态**；拿它做多租户必须自己上四层隔离。
- **提升层**：安全。

### B2：Pipedream 2,700+ 集成 + Premium Apps 分层 + actions 可 fork（来源：docs.pipedream.com/apps）
- 2,700+ 内建集成；**Premium Apps 分层**（AWS/Asana/HubSpot/Jira/Salesforce/Stripe/Snowflake/Shopify/Zoom 等要在活跃 workflow 用需 Premium）；actions 只是 code，可 fork 修改、可发布到社区；集成缺失可贡献进 source-available registry。
- 判据：**"集成数"要按免费/付费分层看**——常用企业级 app 多数在 Premium 名单。
- **提升层**：工作流。

### B3：deepseek-plugin 12,507 插件目录分 12 类 + MemOS 四层本地记忆（来源：deepseek-plugin.org/plugins）
- 总目录 12,507（Official 226 / UI 2,691 / Developer Tools 1,648 / Integrations 4,308 / Themes 519 / Models&Routing 867 / Task&Auto 1,527 / Knowledge 1,263 / Vision 225 / Memory 398 / Security 174 / Creative 108 / Fun 557）；**MemOS 本地四层长记忆**（L1 轨迹 / L2 策略 / L3 世界模型 / skills），每轮自动检索 + 注册 6 个记忆工具；pi2dsh：一个 Pi Host ABI 跑未改 Pi 扩展为原生 DSH 插件（生态桥）。
- 判据：**记忆已分四层落地为插件（轨迹→策略→世界模型→技能），且"一个 ABI 两个生态"是插件移植的最省路径**。
- **提升层**：工具/记忆。

### B4：GitHub 官方 skills 仓库形态（来源：skills.sh/skills）
- github.com/skills 官方仓库发布 secure-code-game 等 9 个 onboarding/技能，27 installs——官方以 skill 形式发布教程型内容。
- 判据：**平台官方用 skill 格式发教程（security 游戏化 onboarding）**——官方内容也在走 agent 可读格式。
- **提升层**：生态观察。

### B5：GitHub 生态——Meta Muse 基于 OpenClaw 的 Markdown 记忆架构 + herdr 运行时 + new-api 统一 hub（来源：GitHub 生态走搜索）
- Meta Muse 技术基因=OpenClaw（38.7 万★，GitHub 历史增长最快之一）：**SOUL.md / IDENTITY.md / USER.md 纯 Markdown 文件管理记忆**；herdr 40,115★：coding agents 运行时；new-api 48,431★：统一模型 hub（LLM 交叉转 OpenAI/Claude/Gemini 兼容格式）；Ponytail 128.2k★（同名信号：最懒资深 dev 心智）。
- 判据：**自托管 agent 的记忆=一组 Markdown 角色文件（SOUL/IDENTITY/USER），身份与记忆可版本化**。
- **提升层**：生态观察/记忆。

## 判重说明
- B1 → r195-A 已记 Guardian/权限；Langflow 官方责任边界声明首次真拉，四层基础设施隔离增量。
- B2 → r196-A 已记 Pipedream sources/actions 分界；apps 页首次真拉，Premium 分层增量。
- B3 → r196-C 已记 12,733 复核；/plugins 目录首次真拉，MemOS 四层记忆 + pi2dsh 增量。
- B4 → r195-C 已记 SKILL.md 标准 50+ 客户端；github/skills 官方仓库信号增量。
- B5 → r198-A 已记 OpenSpec/orca；SOUL/IDENTITY/USER Markdown 记忆架构 + herdr + new-api 增量。
