# r138-B 全站实拉 · OpenAI Agents SDK 深读（2026-09-22）

## 一、实拉证据（独立重拉，不复用 A 轮）
- 全站：**110 路 / 97 OK200**（`yt/r138/b/_summary.txt`，与 A 轮同一清单独立重跑，未复用 A 轮任何结论）。
- 主源深拉：OpenAI Agents SDK 官方 `openai.github.io/openai-agents-python` **16 页全 200**（`yt/r138/deep_b/`）。该站 `.md` 变体 404（返回 36 字节），改走 HTML 剥离后落盘——此前库中 0 处直接引用该站页面。
- 关键页：`guardrails`、`handoffs`、`context`、`multi_agent`、`config`、`tracing`、`sessions`、`tools`、`running_agents`。

## 二、落地（3 文件 3 独点）
| 文件 | 版本 | 独有点 | 层级 |
|---|---|---|---|
| engineering/wb-artifact-verification | 1.73.0 | 检查点挂载点三型（链首/链尾/每次调用）+ 并行 vs 阻塞是"副作用能否撤回"+ 拦截后留痕三规则 | 工作流（检查点设计） |
| defaults/wb-context-compressor | 3.34.0 | 环节间默认全量转发、**压缩≠脱敏**（工具参数与输出仍留在摘要里）、收窄必须显式过滤、下游及其服务商算收件人 | 工作流（交接与暴露面） |
| engineering/wb-debug-loop | 1.32.0 | 可观测采集默认全采敏感数据、脱敏用 allowlist 不用 blocklist、关采集须留关联 ID | 工具/工作流（可观测治理） |

## 三、判非重复（逐条）
1. **检查点位置三型**：av 有 §验证通道禁止副作用、§阻塞与警告不得混同，但**全部管"检查本身的性质"，没有一条管"检查挂在流程哪一段、覆盖哪几步"**。官方明确"输入护栏只在第一个 agent 跑、输出护栏只在最后一个跑"——这条缺了会出现整段漏检 → 落。
2. **压缩≠脱敏**：ctx §42 有"进上下文前扫敏感数据 fail-closed"、§121 有带外通道，但**没有"已进上下文的历史在环节之间传递时被谁看到"**。官方对嵌套历史的警告是"压缩不脱敏，工具参数与输出可能留在摘要里" → 落。
3. **可观测默认全采**：dl §254 有"跨边界错误文本脱敏"，但**没有"观测数据落存储后归谁看、默认开关朝哪边"**。官方 `trace_include_sensitive_data` 默认 True，脱敏示例用 allowlist 且保留链路 ID → 落。

## 四、判重不落地（有证据）
- **Handoff 推荐提示 / 意图分类 / agents-as-tools**：sd §委派这道口子、§派活与提问分成两个入口（r132 已落 Inngest/CrewAI） → 已覆盖。
- **Sessions 自动历史持久化 / SQLAlchemy / 加密会话**：与 agent-guild 记忆分层 + r136 Strands session managers 重叠 >60% → 不落。
- **MCP 集成 / 工具 schema / 结构化输出**：sa §MCP 工具 schema 设计、av §结构化三指标已覆盖 → 不落。
- **Testing 无 provider 请求的确定性测试**：av §三条独立证据源 + sd §密封测试（ADK）已覆盖同一功能位 → 不落。
- **Realtime / Voice / 可视化 / 计费**：模态与运维面，非技能系统底层方法论 → 不落。

## 五、新发现站点
- 无新增站点（本轮主源为清单内既有条目 `openai_agents_docs/llms`，首次深读）。
- 记录一条**取正文方法**：Mintlify 系站点（openai.github.io）**不提供 `.md` 变体**，需走 HTML + 标签剥离；MCP 官网（同为 Mintlify）**提供 `.md` 变体**。同一家族两种行为，下轮按站先试 `.md` 再降级 HTML。

## 六、三件套评估
- 本轮 ctx 3.33.0→3.34.0 属三件套内部升级（交接暴露面），与 ponytail/mts 无冲突。
- 功能位覆盖检查：决策（ponytail）、输出压缩（mts）、输入聚焦（ctx）三者本轮无缺口 → 数量不变（3 件套）。
