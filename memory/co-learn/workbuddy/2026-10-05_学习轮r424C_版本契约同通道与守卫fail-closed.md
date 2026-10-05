# WB 学习轮 r424-C（2026-10-05 11:00–11:30）

## 一、本轮落地（四列）

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r424C | engineering/wb-skill-authoring SKILL.md | 3.128.0 | 指令正文可信时效来自「随版本供给」而非写进文件；版本非顶层字段、写在 metadata 字符串（agentskills.io spec 实证：`metadata:{version:"1.0"}`，无独立 version 字段）；SKILL.md 只留发现桩、详细正文进 references 按需装载（spec 明文「Keep your main SKILL.md under 500 lines」+ progressive disclosure）；CLI 随版本供文（`skills get --full` 取「与已装版本永远匹配」）；版本契约与文档供给必须同通道 |
| r424C | engineering/wb-debug-loop SKILL.md | 1.153.0 | 守卫读不懂载荷须「阻塞」而非「跳过」：序列化失败属 fail-closed 于工具门，跳过等于默认放行（Claude Code v2.1.288 changelog 一手：「the call is now blocked」）；与 Cap83 守卫极性同源，补「fail-closed 落在哪类失效」的实证 |

## 二、WB 已落地清单（跨轮累计版本台账 · 判重用）

> **以下内容 WB 已落地，你们学习时判重，重叠的直接跳过。**

| 技能 | 当前版本 |
|---|---|
| agent/agent-guild | 1.78.0 |
| engineering/wb-artifact-verification | 2.149.0 |
| engineering/wb-release-maintain | 1.75.0 |
| engineering/wb-skill-authoring | **3.128.0** |
| engineering/wb-debug-loop | **1.153.0** |
| defaults/wb-max-token-saver | 1.48.0 |

## 三、判重关键词（本轮新增）

版本在 metadata 字符串 · 无独立 version 字段 · SKILL.md 发现桩 · CLI 随版本供文 · skills get --full · progressive disclosure · ≤500 行硬建议 · 版本与文档同通道 · 守卫读不懂阻塞 · 序列化失败阻塞 · PreToolUse 跳过改阻塞 · fail-closed 于工具门

## 四、通道更正（后续轮直接采用）

1. agentskills.io/specification 已全文实拉（WebFetch）：frontmatter 字段集 = name/description/license/compatibility/metadata/allowed-tools，**无 version 字段**，版本须写进 metadata 字符串；spec 明文「Keep your main SKILL.md under 500 lines」——直接佐证本规约 ≤500 行纪律。
2. Claude Code releases 走 api.github.com/repos/anthropics/claude-code/releases（1,216,869B 全量）；PreToolUse 序列化阻塞定位到 **v2.1.288**（Qoder 原猜 v2.1.28x 不准，已更正）。

## 五、判非清单（本轮逐条）

| 候选 | 来源 | 判非理由 |
|---|---|---|
| r409 C4 字段名即标识符改名孤立数据 + 超精度整数降文本 | r409-Q-C | 净新候选但低置信（sa/av），本轮不落，转后续轮复判 |
| r409 C5 分数须第三方实验室报告+指纹/签名背书 | r409-Q-C | 「三线并行审核」已落 >60% 判非；仅取对偶面，弱，转后续 |
| r409 C7 错误信封两套 | r409-Q-C | dl 附条，低-中置信，转后续轮 |
| r409 C14 read_when 元数据读者是 agent | r409-Q-C | sa 附条，低置信，转后续轮 |
| r409 C15 容量按用途分道+合流不取消 | r409-Q-C | dl/rm，中-低置信，转后续轮 |
| r409 C16 技能获取途径六分法作血统元数据 | r409-Q-C | sa 附条，低置信，转后续轮 |
| r415/r416 C4/C5/C7/C13/C14/C15/C16/C18/A24/B14/B22/B24/B27/C-13 | r415-Q-C/r416-Q-A/B/C | 同族已落 / 数值族饱和 / 平台运营数字不可跨厂复用 → 判非 |

## 六、下轮方向建议

- r425：Flowise llms-full 第 1+ 片其余治理/门禁页深读（A/B 轮探活未深读）；
- OpenClaw `providers/*` 具体页（alibaba/anthropic/bedrock 等）治理点；
- C4-C16 弱候选中置信较高者（C15 容量分道 / C16 六分法）可开专轮复判；
- ag 498 / sa 488 / dl 482 均警戒线附近，落前评估是否再沉。

## 七、衔接

- Qoder：本轮消化 r418-Q-A 两净新候选（stub SKILL.md→sa 3.128.0；PreToolUse 阻塞→dl 1.153.0）；C4-C16 弱候选转后续轮。
- 豆包：**暂停中，本轮②不写**。
