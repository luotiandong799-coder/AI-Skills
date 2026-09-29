# r297A 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r296 全量（含本侧 r296A/B/C 30 独点）+ 并行侧 r296 批。查询词与 r296 三轮全错开（本轮=Agent节点三形态/社区节点供应链/策略守卫/事件流/存储选型/远程MCP/前matter保留词/遥测排行榜/服务退休/错误分析主题）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | Agent 节点三形态判据：Workflow（一次跑完，自动化/批处理）vs Chatflow（多轮，支持/引导问答）vs Agent node（流程内动态工具选择）——先定交互形态再选载体；Agent Strategies 按模型能力选思考策略 | 合并保留增量（r296A 工作流 YAML，本点=三形态判据） | 工作流 |
| 2 | n8n | 2026-05-01 起验证社区节点必须 GitHub Actions+provenance statement 发布（不能本地直发）——provenance 让任何人密码学验证包由哪个 repo/commit 构建；声明式节点模式（REST API 用 requestDefaults 描述，不写自定义 execute） | 合并保留增量（r296A Pin SHA 供应链族，本点=发布强制 provenance） | 工具 |
| 3 | LangFlow | Policies 组件（ToolGuard）：自然语言业务规则→可执行 guard 代码，工具调用运行前检查（guarded tools）；Guardrails 组件三类检测（凭证/越狱/攻击性）；**guard 生成器自身是 RCE 面**（IBM 公告：Dynamic CodeInput 字段绕过+denylist 不完整） | 合并保留增量（r295A Guardrails CVE 族，本点=策略守卫+生成器 RCE） | 工作流 |
| 4 | Activepieces | 三触发器技术：Polling/Webhooks/App Webhooks（OAuth2 单 URL）；Event Streaming：审计日志→New Destination→Generate handler flow 自动生成 webhook 触发流（每事件一 router 分支+flow.run.finished 失败分支） | 合并保留增量（r296C 多触发器，本点=审计事件自动生成流） | 工作流 |
| 5 | Make | 存储选型表：去重/缓存几小时/跟踪执行状态→Data Store；团队共享/非 Make 用户报表→Sheets；复杂关系→外部数据库；Agent 工作流记忆：Scenario Builder 让 context 捕获/传递/写入/丢失可见；变量跨 Break 需 scope=roundtrip | 合并保留增量（r296C 三类记忆，本点=选型表+roundtrip） | 工作流 |
| 6 | Pipedream | 远程 MCP 免自托管（remote.mcp.pipedream.net，SSE+streamable HTTP 双传输动态支持）；**x-pd-external-user-id 头代理用户态**（agent 挑工具、auth 已处理）；3000+ apps 单 URL | 合并保留增量（r296C 单 URL MCP，本点=用户态透传头） | 工具 |
| 7 | Anthropic | frontmatter 硬约束：name≤64 字符仅小写字母数字连字符、不能含 XML 标签、**不能含保留词 anthropic/claude**；description≤1024 必填；API 用 skill 可钉版本（type+skill_id+version） | 合并保留增量（r295C frontmatter，本点=保留词禁止+API 钉版本） | 可复用 Skill |
| 8 | skills.sh | 排行榜由匿名遥测驱动（skills CLI 聚合安装数，无个人/设备信息）；API 三视图 all-time/trending/hot；**SkillsBench 1.1：curated Skills 把 mean resolution 33.9%→50.5%（+16.6 点）** | 合并保留增量（r296A 评测/r296B 目录，本点=遥测机制+量化收益） | 工具 |
| 9 | GitHub | **GitHub Models 2026-07-30 全面退休**：playground/catalog/Inference/BYOK 全关，无兜底；7/16+7/23 两次 brownout 让静默断的调用先暴露；迁移不是换端点：Playground→保存实验配置/成本/可复现性，Inference→model map/retries/tool contract，BYOK→allowlists/key owner/secret rotation | 合并保留增量（r295B 生态盘点，本点=服务生命周期风险管理） | 工具 |
| 10 | deeplearning | Agentic AI 课程（Andrew Ng）：四大设计模式 reflection/tool use/planning/multi-agent；Module 4 实用技巧：evals→**error analysis→按影响排序优先下一步**→component-level evaluations（组件级先于端到端） | 合并保留增量（r296B 评测三步，本点=错误分析排序+组件级先行） | 工作流 |

判重口径：增量判定。本轮 10 合并保留增量，零纯重复。