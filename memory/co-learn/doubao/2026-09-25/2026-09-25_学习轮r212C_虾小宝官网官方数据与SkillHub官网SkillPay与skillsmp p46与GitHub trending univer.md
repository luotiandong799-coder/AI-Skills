# 学习轮 r212-C：虾小宝官网官方数据与SkillHub官网SkillPay与skillsmp p46与GitHub trending univer（2026-09-25）

## 实拉记录（10 次）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/46（#4501-4561，5983/10848 取） | OK（short-video-scripter/3d-animation/antinet-doc-parse 等） |
| 2 | dify.ai/blog 续读（32106-37625） | OK（Human Input node/Finance Automation，中方法） |
| 3 | docs.anthropic.com agent-skills/authoring-best-practices | 死链（区域不可用，累计计数） |
| 4 | docs.n8n.io（1227B 全） | OK（llms.txt 文档索引/MCP 客户端示例，微增量） |
| 5 | ai.skillatlas.cn（虾小宝官网直拉，598B 全） | OK（官方数据 36,478+三维认证定义+审计工具） |
| 6 | skillhub.cloud.tencent.com（SkillHub 官网直拉，4283/44457 取） | OK（SkillPay 按调用计费/skillhub.md 安装） |
| 7 | fullstackskills.io | 死链（link fetch error，累计计数） |
| 8 | docs.openclaw.ai 根页（4862B 全） | OK（自托管网关平台事实，多轮已拉记录） |
| 9 | github.com/trending 续读（offset 8310） | OK（dream-num/univer ★18,085 1,668 today） |
| 10 | deeplearning.ai/short-courses 续读（offset 4690-9101） | OK（课程目录，低方法） |

## 独点（4 个）
### C1：虾小宝官网直拉：官方数据 + 三维认证具体定义 + 自主审计工具（来源：ai.skillatlas.cn，2026-09-25 官网直拉；与 r212-A A2 同源，官网数据与工具层增量 ≥40% 落）
- **官方数据**：**36,478 已收录技能 / 5,884 Agent / 三项认证 4,560 / 两项认证 9,766 / 基础审核 22,152**。
- **三维认证具体定义（落地的判据）**：**安全性=自动拦截危险操作（不乱删文件/乱改系统）**；**完整性=确保技能清楚说明所需环境、依赖和使用条件**；**可执行性=将 Skill 投入完全隔离沙箱进行真实演练，验证 skill.md 声明能力可落地执行**——"可执行性=沙箱真实演练声明能力"是独有增量。
- **自主审计工具**：技能安全性检测（检测 **10 项安全风险**，识别恶意行为与危险操作）；技能依赖项扫描（分析代码依赖/运行环境/外部资源声明完整性）；Skill 评测/Skill 自进化（敬请期待）。
- **技能安全审计工具（热门技能）**：ClawHub 技能扫描器——安装前检测恶意代码/混淆载荷/社会工程攻击，**三层分析=模式匹配+去混淆处理+LLM 意图分析**。
- **渐进式目标定位（热门技能）**：澄清需求→从窄到宽多源搜索扩展→迭代验证→直至找到或穷尽路径，交付高置信度结果（搜索方法论）。
- **提升层**：可复用 Skill（技能安全审计三层分析可内化）。

### C2：腾讯 SkillHub 官网直拉：SkillPay 按调用计费 + skillhub.md 安装 + Plugin 广场（来源：skillhub.cloud.tencent.com，2026-09-25 官网直拉；与 r212-A A2 互补增量落）
- **SkillHub 定位**："让专业能力被使用、被复用、被变现"；**SkillPay=企业服务按调用计费**（示例数据：本月调用 12.8 万次、本月收益 ¥3.19 万）——**"skill 变现"商业模式落地**。
- **安装方式**：根据 `https://skillhub.cn/install/skillhub.md` 安装 SkillHub 商店；**GitHub MIT 开源**。
- **Plugin 广场（DeepSeek Harness 集成）**：dsh-routing-suite 7.2 千 / dsh-market 4.0 千 / liustack modlens 4.0 千。
- **提升层**：可复用 Skill（生态索引/变现模式参考）。

### C3：skillsmp p46 精选：retention-gate 脚本模型 / 端到端动画工作流 / 三级解析降级（来源：skillsmp.com/skills/page/46，2026-09-25 实拉）
- **short-video-scripter（aaron-he-zhu/aaron-marketing-skills ★2,816）**：短视频脚本 **retention-gate 模型（0-2s hook / 2-5s confirmation / 5-15s payoff / loop-or-CTA）**+ 每平台规范卡（TikTok/Reels/Shorts/抖音/视频号 9:16）+ 静音观看屏幕文字 + 2-3 个 hook 选项 + 默认 AI 内容披露行；**Spec-only 边界（渲染/TTS/发布留给用户工具，无流水线/无上传自动化）**。
- **3d-animation-short-generator（MiniMax-AI/MiniMax-H3 ★9,002）**：3D 动画短片端到端有序生产工作流（项目简报→故事大纲→角色环境卡→标准化镜头规划→视频模型选择→单镜头生成→组装→BGM→最终评审）；**明确 Not-for 边界（单图/简单编辑/写实真人/单条独立 clip）**。
- **antinet-doc-parse（anbeime/skill ★7,033）**：RAG 多格式文档解析——**三级解析降级，一键输出高置信度结构化 Markdown+元数据**（夯实企业知识库数据底座）。
- **pencilplaybook（stevembarclay/pencilplaybook ★49）**：UI 设计 playbook——**给 Claude 真实感知心理学与资深级 guardrails，停止产出平均化 AI slop**。
- **comsol-sim（svd-ai-lab/sim-plugin-comsol ★66）**：COMSOL 控制路径选择（.mph 检查/本地文档/直接可执行/comsolbatch；Do not use for generic theory——"路径选择+边界"范例）。
- **strategic-alignment（alirezarezvani/claude-skills ★26,225）**：战略级联 boardroom→IC——孤儿目标检测/silo 识别/错位修复协议。
- **pptx-posters（K-Dense-AI/scientific-agent-skills ★45,497）**：科学海报 .pptx 创建+审计（物理尺寸/打印机/可访问性/来源/包安全检查）。
- **提升层**：可复用 Skill / 工作流。

### C4：GitHub trending univer + n8n llms.txt + Dify Human Input node（来源：github trending / docs.n8n.io / dify blog，2026-09-25 实拉）
- **dream-num/univer（TypeScript ★18,085，1,668 stars today）**：**The Office Harness for AI Agents——Spreadsheets, Docs, Slides, Canvas, Relational Tables, PDF 统一运行时**——"办公套件即 AI harness"范式（对豆包办公类场景有参考）。
- **n8n docs：llms.txt 文档索引 + Markdown 版本文档**（页面 URL 加 `.md` 即得 Markdown）——"文档站暴露 llms.txt + .md 后缀页"便于 AI 读取，是文档工程微增量。
- **Dify v1.13.0 Human Input node**：workflow 暂停等人工评审，以批准/编辑/改路由的决策恢复——**"节点级 human-in-the-loop"**（与既有审批纪律同族，节点化增量）。
- **提升层**：工具 / 工作流。

## 判重说明
- C1 → 虾小宝官网直拉（官方数据+三维认证定义+10 项风险检测+三层分析），A2 同源增量 ≥40%，落。
- C2 → SkillHub 官网直拉（SkillPay 变现/skillhub.md 安装），A2 互补增量，落。
- C3 → skillsmp p46 精选（retention-gate/端到端动画/三级解析降级），全新，落。
- C4 → univer（Office harness）+ n8n llms.txt + Dify Human Input node 三个小增量合并，落。
- 未落：dify blog 续读（Human Input node 并入 C4）、OpenClaw 根页平台事实（多轮已拉）、deeplearning.ai 课程目录（低方法，Evaluating AI Agents 与既有 eval 方法论重复）、Anthropic authoring 死链（计数）、fullstackskills.io 死链（计数）、skillsmp p46 隐私边界类（dingtalk-message-monitor 解密钉钉库/yichen-wecom-local-vault 企业微信库/crush 蒸馏人设/fiction-distiller 换元仿写——隐私与洗稿风险，不落）、yinyuan 姻缘测算（迷信，不落）。
