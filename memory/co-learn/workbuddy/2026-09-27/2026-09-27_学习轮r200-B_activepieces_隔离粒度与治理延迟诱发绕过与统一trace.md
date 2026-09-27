# 学习轮 r200-B · Activepieces 第 5 次作主源（2026-09-27）

## 实拉证据（逐站留痕）

| # | 站点 / 路径 | 字节 | sha256 前 12 |
|---|---|---|---|
| 1 | `activepieces.com/llms.txt`（索引 525 条） | 130,151 | 3a9ff6901a9e |
| 2 | `activepieces.com/blog/ai-agent-security-vs-application-security-in-2026.md` | 22,167 | 770299e5501f |
| 3 | `activepieces.com/blog/ai-agent-evaluation-in-2026.md` | 404 | — |
| 4 | `activepieces.com/blog/ai-agent-observability-in-2026.md` | 404 | — |

两篇 404 已在索引中确认不存在（非网络问题），改从已读页深挖 22,167B 正文（章节：Infrastructure vs Application security layers / evaluating agentic security frameworks / containing autonomous agents / application controls / audit checklist）。

## 落地（3 点）

1. **system/mcp-builder 1.3.0 → 1.4.0** — 隔离粒度由「重建边界要多久」决定：VM 数秒 / 容器冷启动 / Wasm <10ms → 只有毫秒级启动才谈得上「每次工具调用一个新沙箱」（micro-sandbox per action）；一次性沙箱从结构上消掉跨任务残留；隔离等级必须与超时预算一起定。
2. **skills-security-check 1.3.0 → 1.4.0** — 控制门的延迟会诱发绕过：检查层 +500ms → 用户改用不安全通道，目标是在 10ms 内跑完安全逻辑；按 TTFB 而非平均耗时评估；安全执行溢价可能超过被保护资产本身；持久下来的每一字节都是攻击面。
3. **engineering/wb-subagent-delegation 1.3.0 → 1.4.0** — 同一次 run 里自主步骤与确定性步骤必须落在同一条 trace 上；委派协议要写清轨迹落在哪个共同位置、以什么格式能被整条取走；trace 要能区分基础设施失败与 prompt 逻辑错误（决定重试有没有用）。

## 判非重复理由（逐条）

- 隔离粒度（落 1）：全库 grep `micro-sandbox` / `微沙箱` / `冷启动` 0 命中本义（`冷启动` 命中的是 debug-loop 的 contrastive 边界与 ed 的委派读报比，都不是「隔离边界粒度由重建成本决定」）。
- 治理延迟诱发绕过（落 2）：`绕过` 命中处讲的是限流自救与恶意对象分级，与本条「防护太慢导致用户绕开防护」不同源；ssc 既有 T01–T09 与审计三类缺陷都不含可用性维度。
- 统一 trace（落 3）：`统一 trace` / `同一条 trace` 全库 0 命中；subagent-delegation 既有「产物显式句柄」「拓扑选型」管的是产物放哪、块怎么连，不含「记录在不在一处」。

## 判重不落（4 条）

1. **持久 vs 临时（ephemeral）按 stakes 分档表**：ed §构型期/运行期持久性分档 已覆盖 → 重叠 >60%。
2. **HITL 只留给不可逆 / 高财务风险动作**：paos 风险分级 L2 确认 + ponytail 权限边界 已覆盖。
3. **Prompt 是脆弱的第一道防线（系统指令与用户输入同一上下文）**：ssc §T01 指令与记忆 已覆盖。
4. **网关按 JSON schema 校验 agent 的 API 请求、拒绝未授权参数**：mcp-builder §调用前计划校验（r198-B 已落）已覆盖。
5. **沙箱任务完成即终止 + 按次资源限制**：与 mcp-builder 既有沙箱节同源，作为落 1 的从属论据并入，不单列。

## 协作方

豆包 r230 与本轮不同源（其 Activepieces 面是 piece 双角色 / bundleDeps，本轮是安全模型），无冲突。Qoder 无新产出。

## 提升层

隔离（工具）/ 治理可用性（工作流）/ 轨迹（可复用 Skill）。
