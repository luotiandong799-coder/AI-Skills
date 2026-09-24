# 学习轮 r196-A：n8n单行JS表达式与Pipedream组件职责分界与Dify双ETL与heartbeat三defer条件与科学技能库（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai knowledge | OK |
| 2 | docs.n8n.io/code/expressions | OK 全文 |
| 3 | docs.langflow.org/components-memory | 死链 |
| 4 | pipedream.com/docs/components | OK |
| 5 | skills.sh | OK 榜单 |
| 6 | activepieces.com/docs/developers | 死链 |
| 7 | docs.openclaw.ai/automation | OK |
| 8 | waytoagi.com | 导航壳 |
| 9 | huggingface.co/spaces | OK 周榜 |
| 10 | GitHub Trending（robots 禁走搜索） | OK 经 gaojihao/startupcorners 等 |

## 独点（5 个）
### A1：n8n 表达式是单行 JavaScript——不能赋值/多操作（来源：docs.n8n.io/code/expressions）
- `{{$json.body.city}}` 访问上节点数据；内置 Luxon（日期）+ JMESPath（JSON 查询）；表达式内禁变量赋值与多语句。
- 判据：**复杂逻辑移出表达式放进 Code 节点**——表达式只做取数，不做计算。
- **提升层**：工作流。

### A2：Pipedream sources vs actions 职责分界 + verified registry（来源：pipedream.com/docs/components）
- sources：独立运行资源，可作 trigger，支持 dedupe 策略 + KV store + 多部署（UI/CLI/API）；actions：只能在工作流内，return JSON 可序列化数据。
- verified 组件走 GitHub PR 评审流程，community 组件不入册。
- 判据：**能独立监听/轮询的做 source，只在流内改数据的做 action**；用 verified 优先于 community。
- **提升层**：工作流/分发。

### A3：Dify 双 ETL 选型——SaaS 锁 Unstructured，社区默认 Dify 可切换（来源：docs.dify.ai knowledge）
- SaaS 默认 Unstructured ETL 不可改；社区版默认 Dify ETL，可环境变量启用 Unstructured。
- 格式差异：Unstructured 额外支持 eml/msg/pptx/ppt/xml/epub。
- 判据：**邮件/PPT/XML 类非结构化文档必须走 Unstructured ETL**——Dify ETL 不覆盖。
- **提升层**：RAG 工具链。

### A4：heartbeat 三 defer 条件 + empty-heartbeat-file（来源：docs.openclaw.ai/automation）
- 调度中的 monitor turn 在 ①主队列/自动化忙 ②同 agent 另一 run 活跃 ③目标 session 有 active/queued work 时推迟；空 scratch 记 `empty-heartbeat-file` 跳过。
- 判据：**ambient 巡检不该抢主任务资源**——忙时静默跳档是特性不是 bug。
- **提升层**：调度。

### A5：GitHub 生态新信号——科学技能库 / 分布式 agent runtime / 安全审计 skill（来源：GitHub Trending 走搜索）
- K-Dense-AI/scientific-agent-skills 46.3k★/月：165 个科学技能 + 100+ 数据库，19 万科学家，兼容 Cursor；google/ax 开源分布式 agent runtime 4.5k★ 日 +2.3k；cloudflare/security-audit-skill、alibaba/open-code-review、Tencent/BrowserSkill 热榜前列。
- 判据：**skill 已商品化到"按学科打包"**——科学/安全/浏览器都是独立赛道。
- **提升层**：生态观察。

## 判重说明
- A1 → n8n 此前多页死链，本次首次真抓 expressions；全新。
- A2 → r194-C 已记 Pipedream workflows；取 sources/actions 分界 + verified PR 流程增量。
- A3 → r192 补抓已记 Dify scaffolding；取双 ETL 选型 + 格式差增量。
- A4 → r193-C 已记 heartbeat 30min；取三 defer 条件 + empty 文件增量。
- A5 → r193-C/r194-B 已记 HF 周榜；GitHub Trending 生态信号为新增维度。
