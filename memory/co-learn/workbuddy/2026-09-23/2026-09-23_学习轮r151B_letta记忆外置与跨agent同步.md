# 2026-09-23 学习轮 r151-B（Letta：记忆外置 / 共享知识引用 / 跨 agent 同步）

## 实拉证据（全量 165 路 + letta 深拉）
- **全量抓取**：`fetchall.py b` → 165 路 / 122 OK200 / 43 未达（与 A 同集合，独立进程取证）。
- **主源深拉（清单外新信源首读）**：Letta 官方 `docs.letta.com/llms.txt`（29 链接）→ 深拉 **28/29 页全 200**：`concepts/stateful-agents`、`configuration/memory`、`agent-sdk/memory`、`concepts/shared-memory`、`agent-sdk/repositories`、`agent-sdk/mcp` 等。
- 注：本轮原定 convex，但其 `llms.txt` 是重定向桩（→www.convex.dev 404），改用 letta（fetchall 中 `letta_docs_llms` 200）。together 经代理 403 亦弃用。
- 逐站留痕：`b/` + `deep_b/` 28 份原文。

## 独点清单 + 判非重复理由（3 点落地 cc/pt/sa）
1. **记忆外置为按需投影的 git 仓库、按需引用不内联**（→ cc 3.44.0→3.45.0）：记忆是投影到机器的 git 仓库，system prompt 只列路径+顶层文件、按文件树读。判非重复：cc 现有 §/doctor 审计（放置/重复/token）管"胖了怎么清"，本条管"更前置的存贮形态——外置+按需引用不内联"，增量 ≥50%。
2. **共享知识放一处、各 agent 引用不复制**（→ pt 1.61.0→1.62.0）：多 agent 要同一知识→共享仓库引用，而非每人复制进上下文（漂移+占 token）。判非重复：pt §能描述就别编程 管"声明式优于实现"，本条管"可被多 agent 共享的知识外置成引用源"，知识复用层 YAGNI。
3. **跨 agent 共享记忆须带显式同步协议**（→ sa 2.66.0→2.67.0）：挂仓库→system prompt 列路径+文件→文件+git 编辑→commit/push→他人 fast-forward pull。判非重复：sa §互操作兜底层 管"能力不齐怎么互操作"，本条管"共享可变状态时同步协议必须显式，不能假装共享即一致"。

## 落地汇报（强制四列表格）
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| B | defaults/wb-context-compressor | 3.45.0 | 记忆外置为 git 仓库、按需按文件树引用不内联（system prompt 只列路径，省 token 且跨模型/电脑可带） |
| B | defaults/wb-ponytail | 1.62.0 | 共享知识放一处各 agent 引用不复制（多 agent 共用→外置仓库引用，避免漂移与重复占用） |
| B | engineering/wb-skill-authoring | 2.67.0 | 跨 agent 共享记忆须显式同步协议（commit/push→fast-forward pull，不能假装共享即一致） |

## 三件套评估（B）
- 本轮落 cc/pt/sa，**避开 mts/ED**。三件套 **维持 3 件套**。

## 审计
- 7 文件 CRLF=0 / STRAY_CR=0 / U+FFFD=0 / 尾空白=0 / description≤1024（cc660/pt588/sa798）。ISSUES=0。
- repo→live 7/7 SAME。版本化随 A 同 commit `024ae90` 推送。
