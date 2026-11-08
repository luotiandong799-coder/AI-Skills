# 学习轮 r699-B（10 站实拉 + 3 点落地）

## 一、10 站实拉（第二组入口，逐站全量）

| 站 | module | 入口 | 状态/字节 |
|---|---|---|---|
| Dify | CI | docs.dify.ai/en/guides/workflow | 200 / 161,615 |
| n8n | OI | docs.n8n.io/ | 200 / 483,200 |
| LangFlow | VI | www.langflow.org/（文档站整站首页） | 200 / 2,216,805 |
| Activepieces | OI | activepieces.com/docs | 200 / 235,904 |
| Pipedream | OI | pipedream.com/docs/workflows | 200 / 200,471 |
| agentskills.io | KI | /specification | 200 / 262,060 |
| skills.sh | KI | 根站 | 200 / 923,651 |
| WaytoAGI | EI | /blog | 200 / 134,435 |
| docs.openclaw.ai | KI | /tools | 200 / 271,842 |
| GitHub 生态 | RI | `q=agent framework in:name,description pushed:>2026-11-03&sort=stars` | 200 / total 1,908 |

榜单：TauricResearch/TradingAgents 121,190、crewAIInc/crewAI 60,619、AstrBotDevs/AstrBot 46,373、TencentCloud/TencentDB-Agent-Memory 30,618、openai/openai-agents-python 30,550、mastra-ai/mastra 29,397、deepset-ai/haystack 26,942、agent0ai/agent-zero 19,790、wanshuiyin/Auto-claude-code-research-in-sleep 18,840、pipecat-ai/pipecat 17,114。

深挖 `wanshuiyin/Auto-claude-code-research-in-sleep`（767 文件全树）：`skills/shared-references/effort-contract.md`（8,352B）、`fan-out-pattern.md`（21,698B）、`resumable-runs.md`（6,694B）、`acceptance-gate.md`（16,967B）、`capture-antipatterns.md`（4,516B）、`evidence-precheck.md`（3,248B）。该库把"无人值守长跑"拆成一整套共享契约（20+ 份 shared-references），比单条技能更接近"流程即产物"。

## 二、判重（双键）

| 候选点 | 命中 | 判定 |
|---|---|---|
| 工作量档位（lite/balanced/max/beast）＋验证严格度为第二轴＋硬不变量 | mt KB:380 只有"用 reasoning_effort 控深度"，无工作量档位、无"档位不动评审" | 新，落 |
| 扇出：子代理只产候选不打分＋分片/并发/轮次硬上限＋叶子能力封闭＋覆盖率回执 | sub KB 有扇出/中继判据、fork 越权、并行产出归属，**无覆盖率回执与不打分原则** | 增量 ≥40%，落 |
| done / accepted 两态＋续跑走第一个非终态＋accept 必须留 verdict id | ed KB:247 有 run_state 三文件、:1445 有从检查点续跑，**无"执行完成 vs 质量验收"拆分** | 增量 ≥40%，落 |
| capture-antipatterns（记录反模式） | 与 av 既有取证/记录判据重叠 >60% | 判非 |
| evidence-precheck（证据预检） | av KB 已有 evidence 类判据 15 处 | 判非 |
| 跨模型评审团（jury） | 用户只用豆包单模型，无法自建多模型评审 | 判非（不符合用户实际条件） |

## 三、三点落地

1. **工作量档位与验证严格度两条轴**（`defaults/wb-max-token-saver` KB，1.96.0→1.97.0）：四档 0.4x/1x/2.5x/5–8x，只调广度/深度/轮次/覆盖；评审深度、引用核验、评审独立性、完整性、sanity、强制审计出结论属**硬不变量**；审计严格度单列一轴（草稿级/投稿级）；自动继续与难度评估是用户决定项。判据：**降档只降工作量，不降把关**。**提升层：工作流（预算分轴）＋可复用 Skill（成本口径）**。
2. **扇出是火力、裁判席不动**（`wb-subagent-delegation` KB，1.63.0→1.64.0）：子代理只产候选、永不打分；先冻结单元表再切 ≤8 片、≤4 并发、每片 ≤8 轮、递归关；叶子代理工具白名单排除再委派/shell/写操作（能力面封闭，非提示约束）；失败分片最多一次同侧顺序回退、不许借机新派；收工出覆盖率回执（计划/完成/失败分片、已覆盖/未覆盖单元、机械算出的 coverage_complete），回执只证覆盖不判质量。**提升层：工作流（并行编排）＋工具（覆盖率回执）**。
3. **断点续跑只认已验收**（`wb-execute-discipline` KB，3.298.0→3.299.0）：阶段状态落盘并拆 `done`（执行者写完，可自报）与 `accepted`（评审/确定性校验肯定，只有 accept 能写）；续跑走第一个非终态 {accepted, skipped}，自报 done 但崩在审计前的阶段会被重审；accept 强制留非空 verdict id + reviewer；`set_status()` 与 `accept()` 的写权限在代码层分开。判据：**"活干完了"与"活被验过了"必须分别记账**。**提升层：工作流（长跑恢复）＋工具（状态机 API）**。

## 四、功能套件检查

本轮第 1 点直接升级核心套件 `wb-max-token-saver`（1.96.0→1.97.0）：原来只有"成本四层"与"reasoning_effort 控深度"，补上"工作量档位 × 审计严格度"两轴后，套件在"省多少"与"松多少"之间有了明确边界——**省 token 不得顺手降审计**。ponytail、context-compressor 无改动需求。

## 五、环境事实

- 10 站本轮全部 200；Pipedream `/docs/workflows` 页面标题已出现"Workflows and String Are Shutting Down on March 31, 2027"公告（该产品线将停），后续该子路径价值下降，待观察。
- GitHub 搜索本轮 total 1,908（`agent framework` 限定更窄），排序 stars。
- 深挖仓库 767 文件，shared-references 20+ 份，属"流程契约库"型仓库，适合做方法来源而非直接安装。
- git 仍不可用。
