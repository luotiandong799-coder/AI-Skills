---
name: career-ops-resume
display_name: Career-Ops 简历评估
display_name_en: Career-Ops Resume Evaluation
description: 基于 career-ops / career-ops-china 开源求职 agent 的 JD 评估与简历定制入口。当用户贴 JD 或招聘链接要求「评估这个岗位/该不该投/帮我打分/匹配我的简历/定制简历投这个岗」，或要求岗位红线筛查（外包/派遣/大小周）、投递优先级排序、面试故事准备时触发。执行 A-F 六块评估 + 10 维加权打分，低于 4.0/5 明确劝退；≥4.0 才进入简历改写（转 resume-ai-help）。纯内容润色不含评估时不触发本技能。
category: 求职招聘
version: 1.0.0
author: WB
agent_created: true
module: KI
modules: KI,DI,TI
---

# Career-Ops 简历评估（本地零安装入口）

框架来源：GitHub `career-ops-hq/career-ops`（83.8k star, MIT）及其中国改版 `shuheng-mo/career-ops-china`。
本地仓库全文：`D:\腾讯AI\简历skill\repos\`（专区说明见 `D:\腾讯AI\简历skill\README.md`）。
本技能 = 零安装路径：不需要 Node.js/CLI，直接把评估框架跑在对话里。需要 bookmarklet 取数、飞书跟进、PDF 流水线时才去用 repos 里的完整版。

## 触发路由

| 用户请求 | 路径 |
|---|---|
| 贴 JD/链接 + 问「值不值得投/打分/匹配」 | 本技能：红线 → A-F 评估 → 10 维打分 |
| 评估通过（≥4.0）后要求改简历措辞 | 转 `writing/resume-ai-help`（只改写、不新增事实） |
| 只要润色、无评估意图 | 直接 `writing/resume-ai-help` |
| 批量 JD / portal 扫描 / 飞书 tracker | 指向 `repos/career-ops-china`（需 Node.js + AI CLI，按其 docs/SETUP.zh.md） |

## 评估流程（每个 JD 依次执行）

### 第 0 步：硬红线（评估前判，命中直接 SKIP，不打分）

向用户要一次红线清单并缓存（默认含）：外包 / OD / 派遣（人瑞、中智、FESCO、外企德科、万宝盛华、科锐国际等人力公司签约）/ 大小周 / 用户点名的前雇主。
派遣识别：JD 发布主体是甲方、合同主体是人力公司 → 按派遣处理。

### 第 1 步：A-F 六块评估

| Block | 内容 |
|---|---|
| A 角色摘要 | archetype、领域、职能、级别、业务方向、base 城市、TL;DR |
| B CV 匹配 | JD 每条要求 → 简历哪一行；列差距 + 弥补策略 |
| C 级别策略 | JD 暗示级别 vs 用户实际级别（阿里 P/字节/腾讯 T/美团 L 对标）；被压级怎么谈 |
| D 薪酬与口碑 | 用看准网/脉脉/OfferShow/知乎/一亩三分地查薪资区间、真实工时、口碑；禁用 Glassdoor/Levels.fyi/Blind 查中国公司 |
| E 改简历建议 | 针对该 JD 的 Top 5 简历修改点（只改措辞/顺序/侧重） |
| F 面试准备 | 6-10 个 STAR+R 故事 + 红线问题预演（离职原因/加班/婚育） |

### 第 2 步：10 维加权评分（国内权重）

| 维度 | 权重 | 维度 | 权重 |
|---|---|---|---|
| 北极星对齐（与目标方向契合） | 25% | 工时与生活（大小周/996） | 10% |
| CV 匹配度 | 15% | 公司稳定性（裁员风险） | 10% |
| 级别 | 15% | 成长路径 | 10% |
| 薪资（含工时折算） | 15% | 技术栈现代度 | 5% |
| 流程速度 | 5% | 文化信号 | 5% |

（无「远程质量」维——国内远程岗几乎不存在。）

### 第 3 步：判决

- **< 4.0/5 → 明确劝退**，写明最大的 2-3 个失分维度；除非用户给出坚持理由。
- **≥ 4.0 → 才允许进入简历定制**，产出 Block E 修改点，改写走 resume-ai-help。

## 事实层纪律（防背调，不可违背）

1. 简历 `cv.md`（或用户提供的原件）= 事实层：雇主、日期、学历、数字只能来自这里。
2. 定制变体只能改写：改措辞、改标题、调顺序、删减、调侧重——**禁止新增简历里没有的雇主/日期/学历/数字**。
3. 永不替用户点提交；邮件/打招呼只出草稿。
4. 不编造经历与指标；不隐瞒外包经历（用项目而非 title 吸引人）。
5. HR 问婚育/年龄/加班：帮用户备得体应对，不美化问题本身。

## 国内特殊提醒（评估中命中即提示）

35 岁门槛（优先独角兽/中小厂/外企）、空窗>3 个月需备好解释、无大厂背景用真实项目补、转大模型方向看重端到端落地（Eval/可观测性/成本/业务影响）而非「会调 LangChain」。

## 交叉引用

- `D:\腾讯AI\简历skill\README.md` — 专区与四仓库定位
- `D:\腾讯AI\简历skill\repos\career-ops\.agents\skills\career-ops\SKILL.md` — 原版 40+ mode 路由（scan/tracker/interview-prep/upskill…）
- `D:\腾讯AI\简历skill\repos\career-ops-china\docs\EVALUATION.md` — 本框架细则原文
- `writing/resume-ai-help` — 内容改写下游（互指）
