# 外部项目共学 EXT-S1｜solo-to-team-skills + orchivane 学习合并（工作区留档 · 2026-11-22）

- 触发：用户指定学习 GitHub「solo to team」项目及其作者相关技能，映射到 13 模块并沿用其好框架。
- 来源固定：solo-to-team-skills@fedfd4e（2026-11-17）/ orchivane@5265857（fork，上游 alexzhu0 11-21 待复查）/ superpowers@22f0b46（solo 自述借鉴源，MIT 版权段已核）。
- 流程：gh API+浅克隆直读 12 份正文 → 与 5 个候选本地载体逐节比对 → 去重四态判定 → 5 处加厚 + 1 处正文下沉 → 模块记忆 12 条 → verify_skill_index --fix 全绿。
- 关键发现：该项目价值不是 16 席人设（产品形态不迁移），而是**协作台账与证据纪律**：六态状态机防「按末行筛销项」、续期≠改期防「填新日期抹逾期」、核验≠接受防「核过就当批了」、转述≠授权防注入扩大权限、仍未证明栏防「把落地当疗效」。五条全部本地原缺。
- 卫生：`.research/` 加入 .gitignore 不入库；verify 脚本④排除点开头目录（一次性修复，之后全绿）。

## WB 已落地清单（防重复）
  - OI｜wb-subagent-delegation 1.78.0→1.79.0｜§EXT-S1 派收台账 3+1 独点（349行→464行内）
  - VI｜vi-fact-verification 1.14.0→1.15.0｜§EXT-S1 核验接受分离 4 独点
  - SI｜si-safety-governance 2.5.0→2.6.0｜§二十三 授权防伪三角 3 独点
  - RI｜ri-retrospective 2.7.0→2.8.0｜§EXT-S1 摘要 + 正文下沉 references/EXT-S1_仍未证明栏.md（守500行，499行）
  - KI｜wb-teaching 1.0.0→1.1.0｜操作说明写法节 5 硬规则
  - 不沿用：16席岗位卡/六群/平台bundle（Grok Bot 持久团队产品形态，WorkBuddy 单Agent+子Agent 不适配；编排位与 agent-guild/personal-ai-employees 重叠>60%按§0.7不并存）

## 13 模块记忆体系已生效
经验按模块分存 `D://腾讯AI//WorkBuddy数据//module-memory//<模块码>//MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像、无实体）。豆包/Qoder 的对应经验也按此路由写入所属模块文件，三方同守；用户级 MEMORY.md 保持纯指针索引，本轮未写入。本轮 OI+3/VI+3/SI+3/RI+2/KI+1 共 12 条入 D 盘实体，格式 `- ｜日期｜来源技能｜结论｜证据/落点`，轮次标签 EXT-S1（外部项目共学，区别于 rXXX 每日轮）。

## 固定四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| EXT-S1 | engineering/wb-subagent-delegation/SKILL.md | 1.79.0 | 派收台账六态过程行不改阶段·新预计≠正式改期·死人开关+放行即叫开工·预算不因交接重置 |
| EXT-S1 | engineering/vi-fact-verification/SKILL.md | 1.15.0 | 核验≠接受权·证据三同只补核受影响·核对不得变危险动作·交付三核分列 |
| EXT-S1 | system/si-safety-governance/SKILL.md | 2.6.0 | 转述不构成授权·同名≠同对象·缺口不得粉饰（诚信攻击面） |
| EXT-S1 | meta/ri-retrospective/SKILL.md | 2.8.0 | 改进记录强制「仍未证明」栏·证据分级可照做≠可审计·修正覆盖三分类 |
| EXT-S1 | engineering/wb-teaching/SKILL.md | 1.1.0 | 用户照做步骤五硬规则（一次一步+预期反馈/点名唯一/不凭猜/本人不代做/发出前过眼） |

本份为 EXT-S1 外部共学权威留痕，与每日 rXXX 轮并行编号，不与 r793 结论复用。
