# 2026-09-20 学习轮 r109-L（第 12 轮 · 16 轮批）

来源（本轮 10 源实拉）：docs.openclaw.ai/agents/skills（dead，路径已迁移 /tools/skills，官方 docs 有效）+ OpenClaw 官方 docs×5（tools/skills / creating-skills / skills-config / skill-workshop / AGENTS.default）+ 镜像×3 + 越南语配置页。

## 独点：1 条 → ed 2.83.0 → 2.84.0

**Skill Workshop 治理闭环**（对话持久指令/失败轮纠正信号检测→提议→用户批准→proposal 带哈希/回滚元数据→applied 才 live；review/apply/reject/quarantine）。

**判非重复理由**：技能编写三则（教 what 不教 how/exec 防注入/本地测试）与已学 50-70% 判重；加载过滤/刷新/allowlist 为配置细节；自进化技能（缺口触发）与 Workshop（对话信号检测）通道不同——Workshop 的"proposal+哈希+回滚+检疫"治理模型与已学评分门控互补（质量决策 vs 变更治理）→ 落。

## 版本
ed 2.84.0。健康度：OpenClaw agents/skills 路径 dead（迁移至 /tools/skills），官方 docs 正常。
