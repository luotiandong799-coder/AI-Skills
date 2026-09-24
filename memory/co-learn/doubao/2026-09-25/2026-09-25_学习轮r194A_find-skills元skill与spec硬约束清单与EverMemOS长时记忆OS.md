# 学习轮 r194-A：find-skills元skill与spec硬约束清单与EverMemOS长时记忆OS（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | skills.sh 首页榜 | OK All Time 榜 |
| 2 | agentskills.io/specification | OK 全文 |
| 3 | waytoagi.com | OK 导航 |

## 独点（5 个）
### A1：find-skills 是元 skill——skill 自己找 skill，2.5M 安装居首（来源：skills.sh 榜）
- vercel-labs/skills 仓库的 find-skills 排第一，installs 2.5M，说明"skill 发现"本身是高频刚需。
- 判据：**装一个 skill 之前先装"找 skill 的 skill"**——目录导航是基础设施。
- **提升层**：可复用 Skill/生态。

### A2：agentskills spec 硬约束清单（来源：agentskills.io/specification）
- name：1-64 字符，小写数字连字符，禁首尾连字符、禁 `--`，必须匹配父目录名；description 1-1024 字符含"做什么+什么时候用"+关键词；allowed-tools 白名单（实验性）；主 SKILL.md <500 行；文件引用一层深；`skills-ref validate ./my-skill` CLI 校验 frontmatter。
- 判据：**skill 不写 name 匹配父目录，跨 runtime 就装不上**。
- **提升层**：可复用 Skill。

### A3：description 反例"Helps with PDFs"——必须写触发词（来源：agentskills.io spec）
- 好例："Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction."
- 判据：**description 是路由用的，不是营销语**——没写触发词 = agent 激活不了它。
- **提升层**：可复用 Skill。

### A4：lark suite 自家 skills 8.8M 装机——企业级 skill 生态真实规模（来源：skills.sh 榜）
- open.feishu.cn 的 lark-approval/okr/markdown/doc 等合计 8.8M；larksuite/cli 3.1M。
- 判据：**国内企业级 skill 头部已是飞书自家套件**。
- **提升层**：生态。

### A5：EverMemOS 开源企业级长时记忆 OS（来源：waytoagi.com 新工具）
- EverMind-AI 团队开源，跨会话/跨平台/可推理/可进化的长期记忆，解决"换会话就忘"。
- 判据：**记忆正在从"skill 的一个章节"独立成 OS 层**。
- **提升层**：记忆。

## 判重说明
- A2 spec 硬约束 → r192 补抓 D5 已记；取"skills-ref validate CLI + 文件引用一层深"增量。
- A5 EverMemOS → r193-A MemTensor 四层记忆呼应，取"独立 OS 层"定位增量。
