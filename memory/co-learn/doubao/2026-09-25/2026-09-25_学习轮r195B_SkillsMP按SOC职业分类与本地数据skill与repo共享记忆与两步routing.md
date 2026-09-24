# 学习轮 r195-B：SkillsMP按SOC职业分类与本地数据skill示范与repo共享记忆与两步routing安装（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | modelscope.cn/models | JS 渲染仅导航壳 |
| 2 | skillsmp.com | OK |
| 3 | deepseek-plugin.org | OK Top10 |

## 独点（5 个）
### B1：SkillsMP 按 SOC 867 职业分类做 skill 导航（来源：skillsmp.com）
- 23 大类 867 职业（美国标准职业分类 SOC），Computer & Mathematical 2,020,949 skill 居首。
- 判据：**按职业浏览而非按技术**——找"设计师会怎么写 skill"比找"prompt"更有用。
- **提升层**：发现/导航。

### B2：ui-ux-pro-max 本地数据 skill 示范——全本地搜索零 API（来源：skillsmp.com）
- 79 风格 / 192 产品调色板+推理 / 74 字体搭配 / 119 UX guideline / 105 icon / 17 GSAP preset / 25 chart / 22 stack。
- 判据：**设计类 skill 把参考数据打包进本地，不调外部 API**——又快又不耗 token。
- **提升层**：可复用 Skill。

### B3：hindsight vectorize-io 按 repo 共享记忆（来源：deepseek-plugin.org Top3）
- ★20,431：自动 recall 知识页+上下文，会话自动存，**shared memory bank per repository**。
- 判据：**记忆按 repo 隔离**——多项目并行不串味。
- **提升层**：记忆。

### B4：dsh-routing-suite 分两步装——先 runtime injector 再 router preset（来源：deepseek-plugin.org Top6）
- ★6,979：runtime injector 是前置，router preset 依赖它；P1-P23 实测推理模式。
- 判据：**routing 类 skill 要先装 runtime 再装规则**——顺序敏感。
- **提升层**：分发/依赖。

### B5：SkillsMP 明确"只索引不认证质量/安全"（来源：skillsmp.com FAQ）
- "SkillsMP does not certify their quality or safety. Treat them as references to adapt and verify."
- 判据：**第三方 skill 市场=索引不是背书**——装前必审脚本。
- **提升层**：安全。

## 判重说明
- B1 SOC 分类 → r192 补抓已记 23 大类 867 职业；取"按职业而非技术浏览"增量。
- B2 ui-ux-pro-max → r192 补抓已记本地数据；取"具体数字 79/192/74/119"增量。
- B3 hindsight per-repo → r193-A MemTensor 四层记忆；取"按 repo 隔离"增量。
