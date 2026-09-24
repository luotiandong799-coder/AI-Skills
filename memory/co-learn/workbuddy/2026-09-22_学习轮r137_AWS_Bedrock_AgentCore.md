# 学习轮 r137 · AWS Bedrock AgentCore（2026-09-22）

> 轮号接续：r136 → r137。本轮回合主源 = r136「下轮提示」指定的可转新主源（AWS AgentCore）。VPN 本轮已开（33210/33233 监听），直连 200。
> 注：AgentCore 路径初探 404，实为 **Bedrock AgentCore**（docs.aws.amazon.com/bedrock-agentcore）。

## 一、落地（1 独点 → 1 技能升版）

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r137 | engineering/wb-skill-authoring/SKILL.md | 2.55.0 → 2.56.0 | 语义检索式工具分发（gateway 模式）：工具别全塞 prompt，按上下文检索相关几个再调；网关顺带做协议翻译/凭证注入/双向认证 |

## 二、独点详述（来源：docs.aws.amazon.com/bedrock-agentcore，2026-09-22 首读）

**语义检索式工具分发（gateway 模式）**——工具一多，把全部 tool schema 静态塞 system prompt 会撑爆上下文、拖慢首 token、且模型在几百工具里选不准。AgentCore Gateway 做法：工具收在**统一入口（gateway）**后，agent 按任务上下文**语义检索**出最相关几个再调用（官方："use thousands of tools while minimizing prompt size and reducing latency"）。
- 网关额外解决三件工程面：① 协议翻译（REST API / Lambda / 已有服务 → MCP-compatible 工具）；② 凭证注入（各工具 OAuth/token 由网关代发，agent 不持明文）；③ 进出双向认证（inbound 验 agent 身份、egress 连工具）。
- 判据：工具数 < 15 全量暴露更简单；上几十、跨多服务/多鉴权 → 必须上检索/网关层，否则 prompt 与运维一起崩。
- 与 §11「工具暴露要看得见」互补（那条管运行时可见性，这条管规模化分发）；与「组合三平面」不冲突（网关是行为层工具调度实现）。

## 三、判非重复（已查重，不落地）

- **AgentCore Memory 短/长期记忆分离**（short-term turn-by-turn + long-term auto-extract 偏好/事实/摘要跨会话）——与 r136 Strands session/memory/storage 三层分离 + `agent-guild` 记忆模型重叠 >60%，仅记要点，不重复写。AWS 的独特措辞："statelessness is the fundamental challenge in agentic AI"，与既有一致。
- **产品页其余组件**（Runtime 会话隔离 serverless / Code Interpreter / Browser / Observability）——多为产品目录，无新方法论，不落地。
- **A2A（Agent-to-Agent）流量经网关 passthrough** ——与既有多 agent 协作思路一致，不重复落地。

## 四、清单外新信源

- `docs.aws.amazon.com/bedrock-agentcore/latest/devguide/`（Bedrock AgentCore 开发者指南，memory/gateway 两页有实拉 .md）+ 产品页 aws.amazon.com/bedrock/agentcore。建议计入必须项（待用户定）；本轮 urls.txt 仍 108 路未增（深读页面路径，不新增清单条目）。

## 五、审计（待收尾脚本跑）

- 改 1 文件：wb-skill-authoring 2.56.0。
- PyYAML 解析、CRLF / STRAY_CR / FFD / TRAILING_WS / description>1024 收尾统一校验。
- push：rebase 到豆包线上（mao-strategy）→ SSH over 443 非强推；cp 回 live 后 sha256。
