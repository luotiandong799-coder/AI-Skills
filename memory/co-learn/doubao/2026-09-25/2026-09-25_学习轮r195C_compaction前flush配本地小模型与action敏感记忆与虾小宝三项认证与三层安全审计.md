# 学习轮 r195-C：compaction前flush配本地小模型与action-sensitive记忆与虾小宝三项认证与三层安全审计与50+客户端（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.openclaw.ai/concepts/memory | OK 全文 |
| 2 | agentskills.io/ | OK overview + client showcase |
| 3 | ai.skillatlas.cn | OK |

## 独点（5 个）
### C1：compaction 前 memoryFlush 可单独配本地小模型省钱（来源：docs.openclaw.ai memory）
- flush turn 用私有对话，housekeeping 消息不进 user turn；可单独配 `agents.defaults.compaction.memoryFlush.model: ollama/qwen3:8b`，不继承主 session 模型 fallback。
- 判据：**housekeeping 用小模型，主任务用大模型**——成本分层。
- **提升层**：成本/上下文。

### C2：action-sensitive memory 必须记"何时可行动/谁授权/何时过期"（来源：docs.openclaw.ai memory）
- 不只记事实，要记：what changes behavior / when applies / when expires / what to avoid / who owns。
- 判据：**"另一个 session 在设计 API，这边别改"这类记忆必须带边界**，否则未来 session 会照记忆乱改。
- **提升层**：记忆/安全。

### C3：虾小宝三项认证——安全/完整/可执行（来源：ai.skillatlas.cn）
- 三项认证 4560 个：安全性（拦危险操作）+完整性（环境依赖声明）+可执行性（隔离沙箱真跑验证 skill.md 声明能力）。
- 判据：**"可执行性"是沙箱真跑，不是读一遍 skill.md**。
- **提升层**：安全/评测。

### C4：skill 安全审计三层——模式匹配→去混淆→LLM 意图分析（来源：ai.skillatlas.cn）
- ClawHub 技能扫描器三层分析：pattern matching / deobfuscation / LLM intent analysis。
- 判据：**单靠模式匹配漏混淆 payload，单靠 LLM 误报**——三层叠加。
- **提升层**：安全。

### C5：agentskills.io client showcase 50+ 客户端——skill 已成跨厂标准（来源：agentskills.io）
- Cursor/Cline/OpenHands/Kiro/Gemini CLI/Codex/Qodo/JetBrains Junie/VS Code/Tabnine/Coder/Claude Code/OpenClaw/Hermes/Nanobot/Letta/Factory.ai/Ampcode/AutoHand 等。
- 判据：**SKILL.md 格式已是事实标准**，单写一份跨客户端可用。
- **提升层**：生态。

## 判重说明
- C1 flush 配小模型 → r192-B 已记 compaction 前 flush；取"单独配本地小模型"增量。
- C2 action-sensitive → r192-B 已记 action-sensitive memory；取"边界五要素"增量。
- C3/C4 → r192 补抓 SkillsMP 已记"不认证"；取虾小宝"真认证三层"对照增量。
