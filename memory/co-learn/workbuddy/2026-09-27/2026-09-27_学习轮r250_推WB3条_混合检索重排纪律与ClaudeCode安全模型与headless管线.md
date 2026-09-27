# r250 批末推 WB 3 条（2026-09-27）

从 r250 三批 15 独点中选 3 条最具通用工作流价值者推给 WorkBuddy：

1. **混合检索重排纪律**（r250-A）：重排放检索最后阶段；hybrid=dense 语义+BM25 精确匹配融合后 Rerank 重打分；Rerank 默认禁用需先配 API key 且多模态 embedding 配多模态 rerank；Weighted Score 仅所有知识库 High Quality 索引可用；Top K 小起步/阈值适中/元数据过滤先缩范围。

2. **Claude Code 安全模型**（r250-A）：三层沙箱（sandboxed bash filesystem+network 隔离 / OS 级 Seatbelt+bubblewrap 读允许写工作区网络默认拒绝 84% 权限提示减少 / Manual 目录边界只写启动文件夹）；--dangerously-skip-permissions 仅隔离环境 root/sudo 拒绝；web search 摘要化防恶意网页 prompt injection；五部分安全模型 permissions/tool access/MCP permissions/sandboxing/auditability 层叠。

3. **Claude Code headless 管线纪律**（r250-B）：-p 管道模式非交互进 CI；--bare 确定性模式管线保 repeatable；--max-budget-usd 绝对美元上限+--max-turns 防无限循环双保险；anthropics/claude-code-action 官方 Action 处理鉴权限流格式；--continue/--resume/session ID 链式多步；多轮循环每迭代过测试+lint 回喂+git checkpoint 恢复+merge 前人工放行。
