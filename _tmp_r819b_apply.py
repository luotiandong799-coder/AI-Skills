import re, io
p = r'D:\腾讯AI\skills\meta\ri-retrospective\SKILL.md'
t = io.open(p, encoding='utf-8').read()

# 1) sink r800A full into references, keep summary
m = re.search(r'(## r800A · 变更分析[^\n]*\n)(.*?)(?=\n## r804A)', t, re.S)
assert m, 'r800A not found'
sec = m.group(1) + m.group(2)
io.open(r'D:\腾讯AI\skills\meta\ri-retrospective\references\r800A_变更分析.md', 'w', encoding='utf-8', newline='\n').write('# r800A 变更分析（全文下沉 · 2026-11-23 原节）\n\n' + sec.strip() + '\n')
summary = '''## r800A · 变更分析（全文下沉 references/r800A_变更分析.md）

> 三独点（曾正常→现失效才适用·拿基线比差异 / IS-IS-NOT 矩阵把「问题不存在处」当等值证据 / 临时与渐进漂移最易漏·替换件须规格相同）与四独立域一手逐字已下沉 `references/r800A_变更分析.md`，结论仍有效：找因先锁定差异集合；与本轮鱼骨图（分类穷举可能因）分工不复用。

'''
t = t[:m.start()] + summary + t[m.end():]

# 2) desc lossless tighten + add triggers
frags = [
 ('当任务完成或失败后需要沉淀经验、比较预期与实际、做根因分析、总结可复用规则时调用。', '任务完成/失败后沉淀经验·比较预期与实际·根因分析·总结规则时调用。'),
 ('RI 可提议修改 Skills/提示词/规则/工作流，但未经授权不得直接改系统核心配置、复盘标签体系与跨事故模式聚合（severity 与 taxonomy 分工、受控枚举、已知/潜在与原文锚点）。', 'RI 可提议改 Skills/提示词/规则/工作流，未授权不得改系统核心配置·标签体系·跨事故聚合（severity/taxonomy 分工·受控枚举·原文锚点）。'),
 ('HAZOP危险与可操作性（IEC 61882·引导词+参数=偏差·节点逐段·定性四阶段·OSHA PSM 五年再验证·与FMEA/HAZID分工·Delta渐进漂移再验证）', 'HAZOP（IEC 61882·引导词×参数=偏差·定性四阶段·OSHA五年再验证·与FMEA/HAZID分工·Delta漂移再验证）'),
]
for a, b in frags:
    assert a in t, 'frag missing: '+a[:30]
    t = t.replace(a, b, 1)
add = '·鱼骨图/石川图（因果图·5M1E/6M分类·鱼头在右为原因型左为对策型·头脑风暴后归并·定性非定量须数据验证·与5Why/FTA/HAZOP分工）'
dm = re.search(r'^(description: .+)$', t, re.M)
assert dm
t = t[:dm.start(1)] + dm.group(1) + add + t[dm.end(1):]

# 3) bump version
t = t.replace('version: "2.15.0"', 'version: "2.16.0"', 1)

# 4) append section
sec819b = '''

## r819B · 鱼骨图 / 石川图（cause-and-effect diagram）：先用分类穷举「可能因」，再谈哪一个是真因（RI · 2026-11-28 实拉，≥3 独立域一手）

**独点 1｜鱼骨图是「分类穷举 + 归并」的定性工具，不是根因判定器。** ASQ 官方逐字「a quality tool that helps users identify the many possible causes for a problem by sorting ideas into useful categories… especially useful in structuring brainstorming sessions」；它是「Seven basic quality tools」之一、以 creator Kaoru Ishikawa 命名。结构固定：先就问题陈述达成一致，画一条向右的水平箭头作鱼脊，箭头末端（鱼头）写问题并加框，各主因类别是从中央箭头长出的分支（鱼刺），再用「Why does this happen?」逐层问出子原因，层级分支表示因果关系——**层的含义是「因果分支」，不是「重要性排序」**。foodmate 明确它是「分析问题根本原因的**定性方法**，强调透过现象看本质，核心逻辑基于因果树规律」。⇒ 复盘里鱼骨图的产出是「一张分类完整的候选因清单」，把它当「已找到根因」是越权：ASQ 在复杂问题上明说它只是「one of several tools… alongside others like a responsibility matrix or an action-planning matrix」。

**独点 2｜分类框架是启发式的记忆支架，可以按问题改；鱼头方向区分「找原因」与「找对策」。** ISHIKAWA 引入的 6M 是通用标签：Materials（parts/ingredients/supplies）、Machinery（设备/搬运设备/软件）、Methods（程序/技术/流程/法规）、Measurement（关键指标/量具/数据采集点）、Manpower（人/培训/技能/胜任力）、Mother Nature（环境与外部性），另可加第七个 M = Money（运营费用与资本投入）；ASQ 特别写「he also encouraged creativity in naming these categories to communicate more clearly」——**分类是可改的脚手架，不是物理定律**。中文资料给出 5M1E（人机料法环测）与 8M（加 Mission/Management/Maintenance）、营销 4P/8P、服务 4S 等变体。鱼头方向携带语义：原因型（鱼头在右）问「为什么发生问题」、对策型（鱼头在左）问「如何改善问题」、整理问题型只做结构化梳理（非因果）——**同一张图混用两种方向会让读图者误解箭头含义**。⇒ 复盘模板写清本次用哪套分类、鱼头朝哪边；跨团队比较图之前先对齐分类口径，否则「分类不同」会被误读成「结论不同」。

**独点 3｜鱼骨图的已知弱点必须显式处理：主观、非定量、同一因可归多类。** foodmate 直列两条局限——「主观性：依赖团队经验，易受头脑风暴影响；非定量：需结合数据分析工具（如帕累托、AHP）等验证关键因素」；ASQ 的实例里 calibration 同时出现在 Methods（分析方法的一个因素）与 Measurement（实验室误差的一个原因）、iron tools 同时出现在 Methods（取样）与 Manpower（维护人员），并明写「some ideas appear in multiple places」。方法上用 20/80 聚焦、关键原因一般不超过 7 个、逐条检查描述语法简明；后续用 check sheet 收集数据验证（ASQ 例：用核查表查实验室错误频率是否有规律）。⇒ 鱼骨图后必须接一步「验证门」：候选因逐条标「有数据 / 仅经验」，仅经验者不得进改进项；同一因被列多处时合并到最有解释力的一类并保留交叉引用，避免重复计数当成两个独立证据。与 §r800A 变更分析（有基线时只在差异里找因）、§r804A Tripod Beta（沿事件—屏障—人因—组织重建）、§r814B HAZOP（引导词×参数枚举偏离）分工：鱼骨图在**无明确基线时把可能因铺全**，其余各有特定锚点。

**判据（RI 落地）**：复盘画鱼骨图时验三件事——① 产出是否为「分类完整的候选因清单」而非直接宣布的根因；② 分类框架与鱼头方向是否写明、同一因归多类是否合并；③ 候选因是否有数据验证门（仅经验者不得进改进项）。三条缺一，「画过鱼骨图」不构成根因分析完成。

**判重**：全库 SKILL.md / module-memory / co-learn 对 `鱼骨图` / `石川图` / `Ishikawa` / `特性要因图` 0 专节（RI 正文有「5 Whys」「因果模型层」等异命题；wb-debug-loop / wb-subagent-delegation / ti-critical-reasoning / 采购skill 的命中均为「图/因果」语境子串，非本工具）；豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地。

**来源与诚信**：`https://asq.org/quality-resources/fishbone`（ASQ 美国质量学会官方质量工具页，WebFetch 200 全文逐字：定义/七大工具/Ishikawa 6M 全类与 Money 第七 M/八步绘制程序/分类可创新命名/同一因多处/复杂问题需配责任矩阵/check sheet 验证/example 两则）——第一独立域·权威机构官方一手；`https://qms.foodmate.net/news/show.php?itemid=173007`（食品伙伴网质量服务中心《鱼骨图分析法 5M1E》，WebFetch 200 全文逐字：石川磐 1950s 起源/1953 川崎重工/TQM 与六西格玛/定性方法与因果树规律/原因型-对策型-整理问题型三型/5M1E 六类含义/制作五步/20-80 与关键原因≤7/主观性+非定量局限）——第二独立域·质量资讯一手；`https://www.wikiwand.com/zh-hans/articles/石川图` 与 `https://bafybeiemxf...ipfs.4everland.io/wiki/Fishbone_chart.html`（WebSearch 快照逐字：1956 石川馨《品质管理入门》/鱼头大类中类小类层级/5M1E/8M/4P/4S/5Why 配合）——第三、四独立域百科交叉，Wikiwand WebFetch 本地回退禁用（`CODEBUDDY_WEBFETCH_DISABLE_LOCAL_FALLBACK=1`）如实登记。诚信：起源年份 1953/1956/1960s/1968 多说并存、人物「石川馨/Kaoru Ishikawa」与 foodmate「石川磐」异写，均按来源并列不强行统一；鱼骨图与思维导图类比按来源族折叠。逐字全文与判非见 `references/r819B_鱼骨图.md`。
'''
t = t.rstrip('\n') + '\n' + sec819b
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)

ref = '''# r819B 鱼骨图 / 石川图逐字取证 · 2026-11-28

> 载体：meta/ri-retrospective SKILL.md r819B 节（version 2.16.0）。≥3 独立域一手交叉。

## 一手域 1 — ASQ 美国质量学会官方（WebFetch 200 全文逐字）
URL: https://asq.org/quality-resources/fishbone
- "a quality tool that helps users identify the many possible causes for a problem by sorting ideas into useful categories… especially useful in structuring brainstorming sessions."
- "one of the most widely used tools in quality management and is considered one of the Seven basic quality tools… also known as a cause and effect diagram or an Ishikawa diagram (after its creator, Kaoru Ishikawa)."
- 变体：Cause enumeration diagram / Process fishbone / CEDAC / Desired-result fishbone / Reverse fishbone diagram。
- "In smaller projects or when immediate action is needed, the fishbone diagram may be the only tool used to determine the root cause(s)… For complex problems, however, it may be one of several tools used in the improvement process alongside others like a responsibility matrix or an action-planning matrix."
- 八步程序：① agree problem statement ② draw horizontal right-facing arrow as spine, problem at head in a box ③ identify main categories as branches；"Ishikawa introduced the '6 M's' as generic labels… but he also encouraged creativity in naming these categories to communicate more clearly to those who would be using the diagram"；Materials / Machinery / Methods / Measurement / Manpower / Mother Nature + 第七 M Money ④ ask "Why does this happen?" to brainstorm, "Causes can be written in several places if they relate to several categories" ⑤ continue asking "Why?" deeper, "Layers of branches indicate causal relationships" ⑥ focus where fewer ideas ⑦ "the purpose is to cure the problem, not the symptoms" ⑧ follow up with responsibility matrix。
- 复杂例："some ideas appear in multiple places" — Calibration 同时在 Methods 与 Measurement；Iron tools 同时在 Methods 与 Manpower；结论 "additional information and data are needed" 并用 check sheet 查 lab errors 频率。

## 一手域 2 — 食品伙伴网质量服务中心（WebFetch 200 全文逐字）
URL: https://qms.foodmate.net/news/show.php?itemid=173007 （发布日期 2025-07-31）
- 起源："鱼骨图由日本质量管理专家石川磐（Kaoru Ishikawa）于20世纪50年代提出"；"1953首次应用于川崎重工船厂"；后成 TQM 与六西格玛核心工具；60 年代推广至 GE/福特。
- 定义："一种图形化结构（鱼头为主问题，鱼骨为分类原因）分析问题根本原因的定性方法，强调'透过现象看本质'。核心逻辑基于'因果树规律'，即多方向、多层次的因果链关系。"
- 三型：原因型（鱼头在右）分析"为什么发生问题"；对策型（鱼头在左）制定"如何改善问题"；整理问题型结构化梳理（非因果关系）。
- 5M1E 六类：人 Man/Manpower（技能/经验/身体/心理）·机 Machine（性能/稳定性/维护/自动化）·料 Material（质量/规格/供应稳定）·法 Method（工艺流程/操作规范/质控标准/生产计划）·环 Environment（温湿度/洁净度/照明/噪音振动）·测 Measurement（测量与监控、仪器）。
- 制作五步：选层别法→头脑风暴归大骨/中骨/小骨→归类整理明确从属标识关键原因（一般不超过 7 个）→遵循 20/80 聚焦→检查描述语法简明意思明确。
- 局限逐字："主观性：依赖团队经验，易受头脑风暴影响。非定量：需结合数据分析工具（如帕累托、层次分析法AHP）等验证关键因素。"

## 交叉域 3/4 — WebSearch 快照逐字（不作一手全文）
- https://www.wikiwand.com/zh-hans/articles/石川图：1956 石川馨《品质管理入门》创制；鱼头—大类—中类—小类层级；5M1E（人机物法环测）与 8M（+Mission/Mother nature、Management/Money power、Maintenance）、营销 8P、服务 4S；"原因也可以用五个为什么设法找到其根本原因"；品管七大手法之一。
- https://bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq.ipfs.4everland.io/wiki/Fishbone_chart.html（维基百科镜像）："created by Kaoru Ishikawa (1968)"；6M 英文全称；"Causes can be traced back to root causes with the 5 Whys technique"；Mazda Miata "Jinba Ittai" 例；参考文献 Ishikawa 1968 Guide to Quality Control (JUSE) / Tague 2004 The Quality Toolbox (ASQ)。

## 诚信登记
- Wikiwand WebFetch 本地回退禁用（CODEBUDDY_WEBFETCH_DISABLE_LOCAL_FALLBACK=1），按 WebSearch 快照转述不冒充全文；IPFS 镜像与 Wikiwand 同源按来源族折叠。
- 起源年份 1953 / 1956 / 1960s / 1968 四说并存、人物「石川馨」与「石川磐」异写，均按来源并列不强行统一。
- 全库判重：RI 正文 5 Whys/因果模型层为异命题；wb-debug-loop / wb-subagent-delegation / ti-critical-reasoning / 采购skill 命中为「图/因果」子串噪声；豆包自留地 WB 0 落地。
'''
io.open(r'D:\腾讯AI\skills\meta\ri-retrospective\references\r819B_鱼骨图.md', 'w', encoding='utf-8', newline='\n').write(ref)

t = io.open(p, encoding='utf-8').read()
dm = re.search(r'^description: (.+)$', t, re.M)
print('LINES', t.count(chr(10))+1, 'DESC', len(dm.group(1)), 'VER', re.search(r'version: "([^"]+)', t).group(1), 'CR', t.count(chr(13)), 'FFFD', t.count(chr(0xFFFD)))
