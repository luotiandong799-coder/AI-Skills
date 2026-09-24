# 学习轮 r193-B：monorepo拆独立包与渐进披露三层与TRACE评测与个人草稿反模式（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | raw.githubusercontent.com/partme-ai/full-stack-skills/README.md | OK 全文 |
| 2 | general_search 腾讯 SkillHub | 定位 skillhub.tencent.com / skillhub.cloud.tencent.com |
| 3 | docs.openclaw.ai/concepts/subagents | 死链 |

## 独点（5 个）
### B1：monorepo 拆独立包——每包独立版本发布，避免强制协调（来源：full-stack-skills README）
- 原 460k star monorepo 拆成 50 个独立可装包；`npx skills add org/pkg` 按需装；版本锁定问题由独立发版解决。
- 判据：**skill 多了就拆包，别在一个 monorepo 里强制同步发版**。
- **提升层**：可复用 Skill/工程。

### B2：渐进式披露三层——启动只 name+description → 激活加载 SKILL.md → 深入才读 references（来源：full-stack-skills）
- 与 agentskills.io spec 一致：启动 ~100 token 元数据、激活 <5000 token 正文、references 按需。
- 判据：**skill 目录结构本身就是上下文预算**——主文件瘦、引用文件深。
- **提升层**：上下文。

### B3：SkillHub TRACE 评测体系 + 三线安全审核 + 本土化镜像（来源：腾讯云开发者社区）
- 腾讯 SkillHub = ClawHub 国内高速镜像；7.1万-8万 skills；TRACE 评测识别高质量；三线并行安全审核；支持 WorkBuddy/QClaw/ima。
- 判据：**国内 skill 生态要有本土化镜像+安全审核+评测打分**——不能只靠 stars。
- **提升层**：生态。

### B4：boss-skills 反模式——个人草稿混入 monorepo 无 skills/ 子目录，不计入正式包（来源：full-stack-skills README）
- 明确标注"仅散落脚本，无 skills/ 子目录，未计入正式包"。
- 判据：**skill 包必须有 skills/<name>/SKILL.md 结构**——散落脚本不算 skill。
- **提升层**：可复用 Skill。

### B5：多 runtime 适配——同一套 SKILL.md 适配 WorkBuddy/QClaw/ima/Claude Code/Cursor（来源：SkillHub + full-stack-skills）
- 包结构 `.claude-plugin/` 元数据 + skills/ 目录；手动 cp 到 `.claude/skills/`。
- 判据：**SKILL.md 是跨 runtime 通用格式**，元数据按 runtime 各自挂。
- **提升层**：可复用 Skill。

## 判重说明
- B2 渐进披露 → r192 补抓 D5 已记 spec；取"三层 token 预算"增量。
- B3 SkillHub → 新信源首次真抓。
