# r130-B 全站实拉 · 非原子失败安全重试/挣自主/双向偏好熵/workflow-as-tool/参数化离线优化/fail-closed 落地 · 生命周期驱逐判重

> 日期：2026-09-22｜批次：r130-B｜模式：定时任务「AI技能库学习·每时3轮×10次」触发

## 一、逐站实拉（10 次，全量信源覆盖）
| # | 信源 | 实拉内容 | 提炼 |
|---|---|---|---|
| 1 | arXiv Synapse/E-mem/HMAT/MetaCTO | 记忆系统 | spreading activation；双进程记忆；情节重建 |
| 2 | agent-works/n8n blog/LangGraph/Microsoft | 编排恢复 | Saga 补偿；重试风暴幂等；safe retry 五步 |
| 3 | arXiv 2608.02645/MetaCTO/loooop | 工具可靠性 | 非原子失败；可行动报错；错误对象结构化 |
| 4 | dspy.ai/Hermes PLAN | 评估驱动 | GEPA 优化；system prompt 参数化离线优化 |
| 5 | arXiv TokenPilot/Headroom/Zylos | 上下文缓存 | 生命周期驱逐；CCR 可逆压缩；压缩与缓存张力 |
| 6 | n8n blog/n8nlogic/Mason | n8n 模式 | workflow as tool；迭代上限=工具链+2 |
| 7 | AWS/openlegion/pickaxe/prefactor | HITL | 挣自主；置信度升级；审批超时安全默认 |
| 8 | arXiv SCOPE/CyclicJudge/BabelJudge | LLM judge | 双向偏好熵；循环配对；受控扰动金标 |
| 9 | aurorasre/Sista/Microsoft | Guardrails | 七层 fail closed；结构性防护 |
| 10 | agentman/flaviocopes/agskills | 技能 | reference 按需加载；finish line；Plan→Verify→Cleanup |

## 二、判重与落地
- **D250+D251 非原子失败+安全重试五步（落 · ED）**：ED 稳定错误名 0/后置条件 0/verify-before 0/非原子 0；非原子三形态+验证感知包装+五步配方+可行动报错为独有增量 → 落。
- **D252 按动作挣自主+置信度升级（落 · ED）**：ED 挣自主 0/毕业 0/置信度升级 0；per-action 错误率<5% 毕业+低置信度升级+审批超时安全默认为独有增量 → 落。
- **D254 双向偏好熵+循环配对（落 · sa）**：sa 熵 0/排列不变 0/循环配对 0；BPE 两序都问+聚合熵+循环配对降方差为独有增量 → 落。
- **D256 system prompt 参数化离线优化（落 · sa）**：sa 离线优化 0；段落参数化+只离线优化+新版本部署不破坏缓存为独有增量 → 落。
- **D255 多层 guardrails fail closed（落 · av）**：av fail closed 0/七层 0；任一可阻断+LLM 检查失败即关闭为独有增量 → 落。
- **D257 workflow as tool+迭代上限（落 · ED）**：ED workflow as tool 0/最长工具链 0；封装粒度+迭代上限=真实链路+2 为独有增量 → 落。
- **D253 TokenPilot 生命周期驱逐（不落）**：ctx 驱逐 2/生命周期 8 已覆盖；残余效用+批量轮次为细分 → 不落。
- **D258 reference 按需加载（不落）**：ctx 按需加载 5 已覆盖 → 不落。

## 三、逐站判非重复理由（未落地站点）
- 记忆系统（spreading activation/双进程/四层分类）：ctx 记忆架构已覆盖；行为状态衰减已落。
- Saga 补偿/重试风暴幂等：ED 幂等/重试已覆盖。
- DSPy GEPA 工具本身：sa GEPA 3 已覆盖（工具）。
- Headroom CCR/KV 压缩：ctx 压缩已覆盖；KV 服务端。
- n8n 确定性流水线/混合规则：已落（按需 agent 化）。
- HITL 2×2/预执行门/超时升级：ED 授权已覆盖。
- judge 事后校准/受控扰动金标：sa 边界例校准已覆盖。
- guardrails 风险评级/最小权限：av 已覆盖。
- skill finish line/单职责：sa 已覆盖。

## 四、功能套件检查（每轮）
- 套件：wb-ponytail / wb-max-token-saver / wb-context-compressor
- 本轮无套件相关增量；ED/sa/av 增量不影响三件套覆盖，无需增删。
