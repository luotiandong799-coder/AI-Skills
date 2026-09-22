# 2026-09-21 学习轮 r113-J（第 10 轮 · 16 轮批 r113）

来源：general_search "fullstack-skills agent skills github repository"（多源实拉：full-stack-skills 官方 README / sohaibdevv fullstack-pack / Antigravity Awesome Skills / copilot-agent-kit npm / FullStack-Agent arXiv）。

## 独点：0 条

**实拉证据：**
1. full-stack-skills（partme-ai）：42 技能组 / 421-462 个 SKILL.md / 拆 47 独立包；npx skills add <org>/<pkg> 按包安装；fskill CLI 43 平台适配（platforms/audit/convert/install）；"per-package on-demand loading"控制上下文足迹；结构 SKILL.md + examples/references/scripts + .claude-plugin。
2. sohaibdevv fullstack-pack.md：Define→Plan→Build→Verify→Ship 五阶段技能加载顺序；三种评审 persona（code-reviewer/security-auditor/performance-engineer）；8 项 full-stack checklist（数据库迁移向后兼容/API 版本化/UI 状态/错误处理/无障碍/安全无 PII 日志/监控/回滚程序）。
3. Antigravity Awesome Skills：verification-before-completion（声称完成前必须跑验证命令，evidence before assertions）；using-git-worktrees；244+ 技能目录。
4. copilot-agent-kit：按 agent 配技能矩阵；输出标准（改了什么/文件清单/验证状态 verified|partially_verified|not_verified/无法验证时给手工命令）；操作策略（不提交/不开 PR/不 push 除非用户要求；不碰范围外文件）。
5. FullStack-Agent（arXiv）：FullStack-Learn 回译仓库数据训练模型自我改进 → 训练侧。
**判非重复：** 五阶段包编排/checklist → 与 ed §多Agent协作/质检-回退、wb-spec-driven 同源（重叠>60%）；验证状态三级 → ed §执行终态与交付态分开同族；"evidence before assertions/不越权" → ed §收 diff 五连查同源；fskill 多平台适配 → 平台工具；FullStack-Learn → 训练侧不投入。

## 版本
ed 2.96.0 未动。
