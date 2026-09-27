# r233-C 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify（HTTP request/error handling 四类节点） | ✓ | 四类易错节点错误处理形态（LLM 默认输出/HTTP 重试+分支/Tool 切备份/Code fallback）、retry_on 白名单（5xx+timeout，4xx 不重试）、backoff+jitter |
| 2 | n8n（source control environments/GitOps） | ✓ | Git 为 source of truth、双向同步（UI→external hooks→磁盘；Git→启动导入）、三环境凭证配置（dev mock/staging test/prod real）、CI 验证 JSON+单命令回滚、agent 直写 JSON commit |
| 3 | LangFlow（custom components/troubleshoot） | ✓ | ValueError/ToolException 自动捕获显示、连接类型不匹配独立故障类、Structured Output JSON/Table、Python Interpreter 错误分类 |
| 4 | Activepieces（flows versioning/piece syncing） | ✓ | draft 可编辑→publish 锁定、编辑已发布自动建新 draft、step 钉精确版本不自动升级、prompt 版本化（Tables 存 version/owner/rollout+回归测试+失败阈值自动回滚） |
| 5 | Make（scenario history/run replay/code app） | ✓ | 执行日志留存分级（Free 7 天/Pro-Teams 30 天/Ent 60 天）、全文本日志搜索、run replay 重放调试、Make Code App 全可观察执行 |
| 6 | Pipedream（props/propDefinition/$.export） | ✓ | code step 参数化 props 提升复用、propDefinition 跨对象引用 app props、$.export 导出供下游 steps |
| 7 | Claude Code（hooks 文档） | ✓ | hooks 确定性 vs CLAUDE.md advisory、20+ hook 事件、permissionDecision+reason 拒绝工具调用、Stop 事件 decision 顶层、超时按事件分档 |
| 8 | GitHub（trending/gh changelog） | ✓ | openclaw 283k/superpowers 113k（无营销无 VC）、Copilot 1.18 assisted approvals、Stream Vision-Agents、grok-build Rust harness |
| 9 | 腾讯云（ADP 4.1.0/SkillHub/Skills 广场） | ✓ | Skills 广场 150+ Skills、企业共享 Skills 审批流（提交→审批→企业区）、SkillHub 13000+ 技能中文搜索、Claw 调用树可视化、SkillPay |
| 10 | deeplearning.ai（Agent Memory 课程） | ✓ | 四类记忆（Working/Episodic/Semantic/Procedural）、记忆工程一等基础设施、Agentic 五模块（reflection→tool use→evaluation→multi-agent） |

## 判重基准
双键检索（来源标识+概念词）：错误处理节点形态/retry 白名单、GitOps/三环境凭证、hook 确定性/permissionDecision、四类记忆/Procedural——均无同类已有落地。hook 与 r232"Hooks 五类型"重叠>60% 但 permissionDecision/Stop 顶层/超时档位为纯新增实现细节（≥40% 独有增量）合并落地；四类记忆与 r232-C"记忆四策略提取"部分重叠但 Procedural 一类为独有增量合并落地。

## 独点落地（4 个，全部真独点）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① 四类节点错误处理+retry 白名单 | LLM 默认输出/HTTP 重试+分支/Tool 切备份/Code fallback；retry_on=5xx+timeout、4xx 分支处理；backoff+jitter | 工作流 | wb-execute-discipline |
| ② GitOps 三环境+凭证分层 | Git source of truth+双向同步+agent 直写 JSON；dev mock/staging test/prod real；CI 验证+单命令回滚 | 工作流 | wb-execute-discipline |
| ③ Hook 确定性+拒绝姿势 | hooks 确定性 vs advisory；permissionDecision+reason；Stop decision 顶层；超时按事件分档 | 工具 | wb-execute-discipline |
| ④ 四类记忆形式 | Working/Episodic/Semantic/Procedural；每轮 traces 归类；Procedural=可复用技能链 | 可复用 Skill | wb-execute-discipline |

## 复核
- 无编造凑数：四独点均有当日实拉原文来源。
- 功能套件检查：④ 四类记忆与 wb-context-compressor 记忆章节直接互补（Procedural 一类新增）；② GitOps 与 wb-skill-authoring 版本化互补；wb-max-token-saver/wb-ponytail 无新增归属。
- 垃圾：未产生临时文件。
