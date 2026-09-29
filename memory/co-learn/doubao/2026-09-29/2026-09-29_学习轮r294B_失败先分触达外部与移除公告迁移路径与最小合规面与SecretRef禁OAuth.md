# r294B 学习轮（2026-09-29，实拉→独点落地）

判重基线：r284~r294A 全表。本批按主题落地到对应技能文件（wb-artifact-verification / wb-release-maintain / wb-skill-authoring）。

## 独点
1. **探测/调用失败先分「是否触达外部」**（来源：docs.openclaw.ai《Auth credential semantics》2026-09-29 实拉 24,733B 核验）：七类具名 reasonCode（excluded_by_auth_order/missing_credential/expired/invalid_expires/unresolved_ref/ineligible_profile/no_model）把"根本没发出"与"发出后被拒"分开；**本地查缺≠401**；被排除不静默跳过；超时后副作用仍会发生（已落盘未发布）。判重：与 §2.45.0 具名失败词汇互补（那条管空值判据，本条管失败在链路哪一段）。提升层=工具/工作流。
2. **移除公告必带迁移路径**（来源：docs.openclaw.ai《BlueBubbles removal》2026-09-29 实拉 4,187B）：移除公告三件事=移除什么/用什么替代/存量怎么迁；升级期告警=提示+给命令+不阻断；迁移阻断按 provider 收敛（AUTH_PROFILE_MIGRATION_REQUIRED 只冻结受影响提供方）。判重：与已落 release-maintain 兼容面判定互补。提升层=工作流/工具。
3. **规范最小合规面只有 name+description**（来源：anthropics/skills 官方仓 template/SKILL.md 2026-09-29 经 cdn.jsdelivr.net 实拉 140B 全文）：官方模板仅两字段+一行正文；未替换占位文案（template-skill/Replace with）是可机检低质信号。判重：新增面（模板实证）。提升层=工具/工作流。
4. **SecretRef 禁 OAuth**（来源：docs.openclaw.ai《Auth credential semantics》OAuth SecretRef Policy Guard 2026-09-29 实拉）：SecretRef 只承载静态凭据；OAuth 凭据 runtime-mutable（refresh 轮换）→ 引用会**可变状态跨存储分裂**；违规=hard failure（启动/重载抛错）。判重：与 §3.20.0 声明式依赖清单互补（那条管怎么声明，本条管哪些凭据不许声明成引用）。提升层=工具/模型。

判重口径：增量判定。4 独点全部合并保留增量，零纯重复。
落地：engineering/wb-artifact-verification/SKILL.md（2.56.0→2.57.0）+ engineering/wb-release-maintain/SKILL.md（1.22.0→1.23.0）+ engineering/wb-skill-authoring/SKILL.md（3.53.0→3.54.0）。commit d241887。