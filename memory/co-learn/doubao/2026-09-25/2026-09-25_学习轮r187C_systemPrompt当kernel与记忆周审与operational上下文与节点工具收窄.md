# 学习轮 r187-C：system prompt当kernel与记忆周审与operational上下文与节点级工具收窄与上下文包eval（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | aicostcheck.com（Anthropic 80% prompt cut 解读） | OK 全文 |
| 2 | dev.to production context 2026 六层栈 | OK 全文 |

## 独点（5 个）
### C1：system prompt 是 kernel 不是知识库——四类内容各归其位（来源：aicostcheck）
- Anthropic 把 Claude Code 系统提示词砍 80% 无 eval 损失后，内容归位：stable behavior→system prompt；task knowledge→retrieval；operational guidance→tool schema/描述；durable preference→auto-memory。
- 长提示词四种失败：指令冲突（prompt 与 tool 说明打架）/稀释注意力（40 页手册对重命名函数是死重）/重复计费（静态 token 每跑都重发）/eval 噪声（坏了不知是哪条）。
- 判据：**别把知识库塞系统提示词**；先挪走 tool 手册/长示例/风格指南/罕用政策。与 r187-B right altitude、r187-A typed context 互补。
- **提升层**：可复用 Skill。

### C2：记忆好坏清单 + 每周审 memory（来源：同上）
- 好记忆=一句可执行事实："项目用 pnpm 不是 npm"/"API 错误用 RFC7807"/"账单导出 UTC 月边界"/"安全评审否了供应商 X"；坏记忆=整段 transcript/临时任务态/未验证猜测/secrets/该走检索的大文档。**坏记忆导致持续坏行为，每周 review 一次。**
- 判据：r186-C 三支柱管"入库前打分"，本条管"入库后定期清"——记忆不是只进不出，坏了要删。
- **提升层**：记忆。

### C3：operational context 层——剩余预算/既往失败显式喂模型（来源：dev.to 六层栈）
- demo 常漏的第六层：剩余步骤预算、剩余 token/cost 预算、既往工具失败、审批态、trace id。显式喂给模型，防它在永久错误上无限循环。
- 判据：**预算和失败历史不是 orchestrator 自己知道就行，要让模型看见**——它看见"只剩 2 步"才会收敛收尾。与 §工具循环查 stop_reason 互补。
- **提升层**：工作流。

### C4：按 workflow node 组装上下文，工具按节点收窄（来源：同上）
- 一个 agent 一个全局提示词是错的；每节点声明 include/exclude：理解请求节点不暴露写工具，发邮件节点只留 create_ticket 一个写工具，退款节点不暴露 delete_customer。
- 判据：**MCP 让暴露工具变容易，也让过度暴露变容易**；最小权限在工具目录层落地到"当前这一步只看见该看见的"。与 §per-tool 最小权限互补——那条管单工具权限，本条管节点级目录裁剪。
- **提升层**：安全/工作流。

### C5：上下文包本身要 eval，不只评最终答案（来源：同上）
- 直接评组装质量：检索到该政策没？排除无关工具没？摘要保住关键约束没？引用对不对claim？拿了旧文档没？token 超预算没？配套反例：缺文档/政策冲突/注入文档/超长对话/跨租户/工具过度暴露。prompt 或检索改动要过 eval 门再上线。
- 判据：**只评最终答案会错过失败根因**——"幻觉"时 trace 要能区分是证据缺、证据冲突、还是模型无视证据。与 wb-skill-authoring 闭合邻域评测互补。
- **提升层**：可复用 Skill（评测）。

## 判重说明
- typed task context、retrieved text 不可信 + delimiter、PII per-turn、credential vault → r187-A/B 已记。
- 六层栈里 instruction/retrieval/memory 分层属常识，只取 operational/节点工具收窄/包 eval 增量。
