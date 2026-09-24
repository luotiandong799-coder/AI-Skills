# 学习轮 r192-补：全量信源补抓（Dify/LangFlow/Activepieces/Pipedream/ModelScope/agentskills-spec/SkillsMP/WaytoAGI）（2026-09-25）

## 实拉记录（9 站）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/workflow | OK |
| 2 | docs.langflow.org | OK |
| 3 | activepieces.com/docs | OK |
| 4 | pipedream.com/docs | OK |
| 5 | modelscope.cn/models | OK（国内榜） |
| 6 | agentskills.io/specification | OK（规范全文） |
| 7 | skillsmp.com | OK（326 万 SKILL.md 索引） |
| 8 | waytoagi.com | OK（导航站） |
| 9 | github.com/fullstack-skills（猜测域） | robots 禁，Full Stack Skills 仓库未定位，待下次用搜索 |

## 独点（7 个）
### D1：Dify 定位 scaffolding not toolbox；REST 把 prompt 从业务逻辑分离（来源：docs.dify.ai）
- BaaS+LLMOps；非技术也能搭；prompt 通过 API 与业务代码解耦，方便集中管成本/数据/用量。
- 判据：**prompt 是资产不是代码注释**——独立托管、版本化、可审计，业务代码里不硬编码。
- **提升层**：工作流。

### D2：LangFlow component=单步；playground 单组件隔离测；tweaks 运行时覆盖；MCP server/client 双向（来源：docs.langflow.org）
- 每个组件可单独跑测依赖；tweaks 临时改 flow 参数；既能暴露为 MCP server 也能连外部 MCP。
- 判据：**可视化编排的最小可测单元是组件不是整条 flow**——先单测再串。
- **提升层**：工具/工作流。

### D3：Activepieces Agents/Flows/Tables 三件套互通；credentials 自带 vault 不进产品；审计流 SIEM（来源：activepieces.com）
- agent 可调 flow、flow 可调 agent、共享表；SSO/SCIM 控权；审计日志流 SIEM。
- 判据：**自动化平台要自带治理**——谁建、连谁、模型看什么数据、凭据存哪、全可审。
- **提升层**：工作流/安全。

### D4：Pipedream Connect SDK 3000+ OAuth；source-available component registry 可 PR（来源：pipedream.com/docs）
- 给自家 app 加 customer-facing 集成；组件库开源，可贡献 PR。
- 判据：**集成组件做成 registry 让社区共建**——不自己写 3000 个。
- **提升层**：工具生态。

### D5：agentskills.io spec 硬约束（来源：agentskills.io/specification）
- `name` 必须匹配父目录名、禁连续连字符；`allowed-tools` 白名单实验性；`skills-ref validate` CLI 校验；文件引用保持一层深；SKILL.md 主文件 <500 行。
- 判据：**skill 格式要可机器校验**——name 规范、引用不嵌套、主文件瘦身，才 progressive disclosure 生效。
- **提升层**：可复用 Skill。

### D6：SkillsMP 索引 326 万 SKILL.md 按 SOC 职业分类；ui-ux-pro-max 本地数据规模示范（来源：skillsmp.com）
- 23 大类 867 职业；Computer & Math 类 200 万 skill；明确"只索引不认证质量"。ui-ux-pro-max 本地带 79 风格/192 调色板/74 字体搭配/119 UX 规则/105 icon/17 GSAP/25 图表/22 栈。
- 判据：**skill 的知识可以是本地静态数据库**——不必每次让模型生成，查表即得。
- **提升层**：可复用 Skill/生态。

### D7：ModelScope 国内榜观察——Qwen3.8-27B 509k 下载居首，与 HF 互补（来源：modelscope.cn/models）
- 国内榜：Qwen3.8-27B 509k、GLM-5.3-Flash 76.6k、Kimi-K3、DeepSeek-V4-Pro、混元 Hy4。
- 判据：**国内模型选 ModelScope 源，国际/HF 源互补**；国内下载量权重与 HF 不同。
- **提升层**：模型选择。

## 判重说明
- D2 LangFlow tweaks/单组件测 → r190 已记 n8n iteration；取"可视化编排单组件 playground"增量。
- D5 spec name 规则 → r191-B 已记 description 第三人称；取"name 匹配目录+skills-ref validate"增量。
- D6 本地数据库式 skill → 新增形态，之前未记。
