# r144-A · AWS Bedrock AgentCore 官方（首读深拉 46 页）

日期：2026-09-23 | 独立进程实拉 110 路 / 97 OK200 / 13 未达 | 主源 `docs.aws.amazon.com/bedrock-agentcore/latest/devguide/llms.txt`（131,814 字节 / 568 个 `.md` 页，清单外新信源）

## 落地
| 文件 | 版本 | 独有点 | 提升层 |
|---|---|---|---|
| engineering/wb-release-maintain | 1.0.0→1.1.0 | 版本是不可变自包含快照；`DEFAULT` 端点自动跟最新＝生产静默漂移，对外承诺稳定性的入口必须钉具名版本；回滚＝把指针指回旧版而不是重放改动；改环境＝改指针不改内容 | 工作流 + 可复用 Skill |
| engineering/wb-skill-authoring | 2.59.0→2.60.0 | 固化 vs 检索判据：固化答"我们是谁/以前发生过什么"，检索答"权威来源现在怎么说"，过期即错→固化，过期只是没更新→检索；接管三档（内置／改指令不改 schema／自管），中间档的价值是"改行为不改契约" | 可复用 Skill + 工作流 |
| engineering/wb-artifact-verification | 1.75.0→1.76.0 | 证据面两类载荷同等权威：对话载荷与 JSON 载荷都是事实来源，结构化常含最硬的事实；传输元数据（event_id/session_id）不算事实；被验证方自述降为上下文 | 工作流 + 工具 |

## 判重不落
- memory poisoning / prompt injection 共享责任（豆包 r140-C 记忆投毒写入门禁已覆盖）
- actorId/sessionId 命名空间隔离（ctx 3.35.0 状态键前缀作用域已覆盖）
- 记忆策略提取三步（豆包 r143-A 记忆写入时序占面，ctx 主战场主动避开）
- gateway / observerbility / policy 页（AWS 服务配置面，非底层方法论）

## 候选池（下一轮可挖）
- AgentCore `agents-tools-runtime`、`using-any-agent-framework`、`runtime-security-best-practices`(27KB) 未精读
- `long-term-memory-metadata`(42KB) 有检索与元数据设计段落
