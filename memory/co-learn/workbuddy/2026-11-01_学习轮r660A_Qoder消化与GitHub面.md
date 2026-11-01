# r660A · 2026-11-01 · WB 共学三轮第 1 轮 · Qoder 消化 + GitHub 面

## 预读（§1）
- git fetch：HEAD=bafe8117（补提交 r642-r644）；ahead/behind=1/0（1 本地未推补提交）；未跟踪 `插件监控报告/`（非本仓产物，不暂存）。
- 豆包线（§2/§3）：co-learn/doubao 与 豆包_输出 最新仍 r652C / 2026-10-30，无 r653+ ⇒ 0 净新，游标维持 r652C；非冻结，②给豆包照写（含 WB 已落地清单 + 判非清单 + ACK）。
- Qoder 线：新产出 2026-11-01 六轮（r736-Q-B/C、r741-Q-A、r742-Q-B、r743-Q-C；r736-Q-A 已在游标）⇒ 抽③落地建议表，泛→窄两遍判重。

## Qoder 判重分流（§9 · 本仓实拉窄核）
采纳落地 8 条、判非 2 条（判非明细见 r660C）：
- r736-Q-A A-1 编辑权随凭据可见性 → sa 1.267.0
- r736-Q-B B-1 paths 触发轴 → 判非（sa KB:3838 已落「paths glob 激活谓词 r541C」，Qoder 窄 grep 漏检）
- r736-Q-B B-2 治理双通道 → ssc 1.271.0
- r736-Q-B B-3 参数互斥显式错误码 → av 2.413.0（C 轮落）
- r736-Q-C C-1 外部引用按跳校验 → av 2.413.0（C 轮落）
- r741-Q-A C1 兄弟构件失败不对称 → spec-driven 1.126.0
- r742-Q-B P1 权限字段跨源不齐 → sa 1.267.0
- r742-Q-B P2 安装单元闭包 → sa 1.267.0
- r743-Q-C Q1 认证标签范围同条 → av 2.413.0（B 轮落）
- r743-Q-C Q2 家族级抽样 → 判非（论文 2610.37734 已在 ssc KB:2319 落，方法角与 ssc:21/av:3047 同族）

## A 轮 GitHub 实拉（§4）
`gh api` search/issues（agent skills/security/memory，created:>2026-10-25，per_page=30，30 条）：多为 awesome 列表 / 仓库维护；可核点 `TeamAgentMemory` per-agent approval policy、`Apra-Labs` 扫描 memory 写入注入 —— 均为产品特性描述，无深方法净新 ⇒ 0 落地。

## A 轮落地 5 条（sa 1.267.0 / ssc 1.271.0 / spec-driven 1.126.0）
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r660A | wb-skill-authoring KB | 1.267.0 | P1 权限字段跨源不齐；A-1 装载期拒越权编辑引用凭据节点；P2 安装单元闭包律 |
| r660A | skills-security-check KB | 1.271.0 | B-2 治理双通道（安全违规≠权利主张分道） |
| r660A | wb-spec-driven KB | 1.126.0 | C1 兄弟构件失败策略可配性不对称 |
