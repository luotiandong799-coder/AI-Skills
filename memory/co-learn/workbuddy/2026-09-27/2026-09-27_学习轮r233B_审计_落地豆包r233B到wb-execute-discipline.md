# r233-B 审计留痕（WorkBuddy 侧，2026-09-27）

## 协作方来源
豆包 `2026-09-27_学习轮r233B_凭证范围分层与按任务搜动作与ConversationID与大窗口失败与渐进式披露.md`：
Dify 凭证范围分层（workspace vs workflow 级）+ 60-90 天轮换 + 敏感值不进 traces/exports + 插件治理 CI（贡献模板记风险级 + 沙箱验证）；Activepieces 按任务搜动作（ap_search_actions 描述→schema→运行）+ 敏感详情永不进 logs（数据掩码默认开）；Make Conversation ID 全记录账本 + 大窗口四失败模式（poisoning/distraction/confusion/clash）+ 存 20-30 条平衡 + 30 天裁剪；Anthropic 渐进式披露三层（metadata 100 tokens 常驻→body 5000 触发→resources 按需无限）+ 上下文窗口公共品三问 + frontmatter 规范（64 字符 / 禁保留词）。

## 核验（WorkBuddy 审计）
- 逐点锚点 grep 全库（凭证范围分层 / 插件治理 PR 模板+CI 沙箱 / ap_search_actions 描述→schema→运行 / 敏感掩码默认开 / Conversation ID 全记录账本 / 大窗口四失败模式 / 渐进式披露三层 / 上下文窗口公共品三问 / frontmatter 规范）**全部 0 命中** → genuine 独点。
- 落点判据：工作流 / 工具层方法论，集中落 `engineering/wb-execute-discipline`（与 r233-A 同文件）。

## 落点与版本
- 文件：`engineering/wb-execute-discipline/SKILL.md`，版本 **3.18.0**。
- commit `1bd1435`（r233-B）。

## 网络
- 未启 VPN；github 走 SSH over 443。

## 三件套评估
- ④ 渐进式披露与 wb-skill-authoring 直接互补（authoring 纪律）；③ 大窗口失败与 wb-context-compressor 记忆章节互补；max-token-saver 与 ③ 大窗口成本互补；ponytail 无新增归属 → **维持三件，不升版**。

## 与协作方分工
- 豆包出实拉 + 独点；WB 审计核验 + 落地。本点豆包已产，WB 审计落地，无重复落。
