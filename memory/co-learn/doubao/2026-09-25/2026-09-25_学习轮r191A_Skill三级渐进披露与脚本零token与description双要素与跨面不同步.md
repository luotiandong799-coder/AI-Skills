# 学习轮 r191-A：Skill三级渐进披露与脚本零token与description双要素与跨面不同步（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.anthropic.com/.../agent-skills/overview | OK 重量级 |
| 2 | skills.sh | OK（生态榜） |
| 3 | agentskills.io | OK（开放规范） |

## 独点（5 个）
### A1：Skill 三级渐进披露——metadata~100tok常驻 / SKILL.md<5k触发 / scripts不进context（来源：Anthropic Agent Skills）
- Level1 frontmatter（name+description）约 100 token 常驻系统提示；Level2 触发后才读 SKILL.md；Level3 脚本和参考文件按需 bash 执行/读取。
- 判据：**装 100 个 skill 也只花 ~10k token**——靠 metadata 常驻、正文触发加载。
- **提升层**：可复用 Skill / 上下文。

### A2：脚本代码本身不进 context，只回 output——确定性操作零推理 token（来源：同上）
- `validate_form.py` 跑了，代码不进模型上下文，只有"Validation passed"或错误消息进。
- 判据：**确定性活走脚本，只有结果进 context**——别让模型现场写代码，那既不稳又费 token。
- **提升层**：工具/成本。

### A3：description 必须写"做什么 + 什么时候用"（来源：同上）
- frontmatter description 上限 1024 字符；触发靠它，只写功能不写触发条件=该用时不出来。
- 判据：**description 是路由用的不是介绍用的**——后半句"Use when..."才是关键。
- **提升层**：可复用 Skill。

### A4：Skill 跨 surface 不自动同步（来源：同上）
- claude.ai / API / Claude Code 三处分别上传；sharing scope 也不同（API=workspace 共享，claude.ai=个人）。
- 判据：**一份 skill 想全平台用，得逐面部署**；别假设改了一处他处生效。
- **提升层**：工作流。

### A5：装 skill 像装软件——外部 fetch 内容可携带注入（来源：同上）
- 未审第三方 skill 可能在脚本/外部 URL 回包藏指令；跨面外部依赖也会被污染。
- 判据：**skill 描述本身就是 prompt 一部分**——装之前审 SKILL.md/scripts/外部 URL。
- **提升层**：安全。

## 判重说明
- progressive disclosure → r190-C C5 部分相关；本条取"三级 token 预算量化"增量。
- skill description 双要素 → wb-skill-authoring 已有触发质量评测；取 Anthropic 官方 100tok/skill 量化口径增量。
