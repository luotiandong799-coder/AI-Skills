# r138-C 全站实拉 · Pydantic AI 深读（2026-09-22）

## 一、实拉证据（独立重拉，不复用 A/B 轮）
- 全站：**110 路 / 85 OK200**（`yt/r138/c/_summary.txt`；C 轮达率低于 A/B 的 97，未达集合与 A/B 互异——主因是第三轮拉取时部分站点限流）。
- 主源深拉：Pydantic AI 官方 `pydantic.dev/docs/ai` **18 页全 200**（`yt/r138/deep_c/`，`.md` 变体直出）。库中此前 0 处直接引用该站页面。
- 关键页：`overview/coding-agent-skills`、`overview/troubleshooting`、`core-concepts/dependencies|agent-spec|hooks|retries|timeouts|storage|output`、`guides/multi-agent-applications`、`evals/*`（core-concepts / span-based / retry-strategies / online-evaluation / lifecycle）、`capabilities/on-demand`。

## 二、落地（3 文件 3 独点）
| 文件 | 版本 | 独有点 | 层级 |
|---|---|---|---|
| engineering/wb-artifact-verification | 1.74.0 | 过程断言具体项（工具/顺序/空转/绕过护栏/委派链）+ 评测与生产共用同一遥测 + 评测装置自身也要配重试 | 工作流（评测设计） |
| engineering/wb-skill-authoring | 2.58.0 | 机器读者需带 `goal` 意图声明；用"在哪页卡住"的真实数据排维护优先级；隐私边界在入口写明 | 可复用 Skill（文档与遥测设计） |
| engineering/wb-debug-loop | 1.33.0 | 会死锁的用法定为显式错误（不是挂住/超时）；复用实例会继承隐性状态，重建要整条重建 | 工具/工作流（失败形态设计） |

## 三、判非重复（逐条）
1. **过程断言 + 同源代码遥测**：av 已有 §指标要分层（结果+过程）与 §过程可观测要先显式打开，但**只到"要有过程指标"这一层，没有"查哪几项""跑在谁的遥测上""装置自己挂了怎么办"**。官方把 span-based 评测的判定项（工具/顺序/重试与空转/绕过护栏/委派顺序）和"评测与生产同一份 OTel span"写明，且明确被测任务与评测器**两侧都要配重试** → 相邻扩展落。
2. **意图声明 + 卡点反哺维护**：sa §903 有"机器可读溯源元数据块"（静态元信息）、§1678 有"反馈信号自动评估"（装后信号），**没有"取用时动态声明意图 + 用取用失败点排维护优先级"**。这是 pydantic 文档站实际在跑的机制，且自带隐私边界（`goal` 只许一句任务描述 + 公开组织名） → 落。
3. **死锁用法显式化 + 复用继承隐性状态**：dl 全库 `死锁/挂住/连接池` 零命中。官方对"同步工具里再调同步 run"直接抛 `UserError` 而非挂死；对"事件循环关闭后只重建 agent 不重建 provider"给出根因（连接池绑死循环） → 落。

## 四、判重不落地（有证据）
- **依赖注入（RunContext deps）便于测试替换**：与 av §夹具先于实现、sd §密封测试 同功能位 → 不落。
- **evaluator_failures 需显式展示**：av §诊断装置自身可信度（绿色由计数挣得）+ §非零退出不等于检出 已覆盖 → 不落。
- **Agent Spec / Output 结构化输出与校验重试**：sa §工具形状阈值、av §结构化三指标、sd §验收两形态 已覆盖 → 不落。
- **技能随依赖库分发（library-skills.io，传递依赖需 `--all`）**：与豆包 r135-A「dsh 分发形态判据」同一功能位 → 不落。
- **Hooks / 超时 / 存储 / 多 agent 委派 / 在线评测**：分别与 ED §hook 担保硬约束、dl §错误四档、agent-guild 记忆分层、sd §委派四条、r129A 影子评测 重叠 >60% → 不落。

## 五、新发现站点
- 无新增站点（主源为清单内既有 `pydantic_ai_llms` 条目，首次深读）。
- **取正文方法补记**：pydantic.dev **要求**抓页带 `goal`/`organization` 查询参数（用于给维护者看 agent 在哪卡住）；`.md` 变体直出可用。

## 六、三件套评估
- 本轮未改 ponytail / mts / ctx；三点分别落在 av / sa / dl。
- 功能位复查：决策取舍（ponytail）、输出压缩（mts）、输入聚焦（ctx）**无缺口**，亦无新增功能位需求 → 维持 3 件套，不凑数。
