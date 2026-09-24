# r171-C 学习轮：FastMCP 双层拦截 + Evidently 生产轨迹持续评测

- 日期：2026-09-24｜轮号：r171-C（全局唯一）
- 落点：`engineering/wb-spec-driven` §七·4.5（新增）+ `engineering/wb-skill-authoring` 文末（新增）
- 版本：wb-spec-driven 1.91.0 → **1.92.0**；wb-skill-authoring 2.87.0 → **2.88.0**

## 实拉证据（本轮独立实拉，非复用）
| 信源 | 状态 | 关键证据 |
|---|---|---|
| gofastmcp.com/llms.txt | 200 | middleware 家族（authorization/caching/rate_limiting/timing/error_handling/response_limiting/tool_injection）+ transforms（Tool Transformation/Namespace Transform/Component Visibility/version_filter）+ callable 级授权 + Tool Fingerprinting + Provider 抽象（含 Skills Provider）|
| docs.evidentlyai.com/llms.txt | 200 | Scheduled evals over traces / Alerts / Data Drift preset（customize_data_drift）/ Descriptors(行级) vs Metrics(数据集级) / LLM-as-a-jury |
| huggingface.co/docs/smolagents/llms.txt | **fetch failed** | 探活失败累计 +1（待下轮复核） |

## 落地独有点（2 个）
1. **拦截分层：调用时 middleware × 暴露时 transform**（→ wb-spec-driven §七·4.5）：
   - 静态可判（可见性/命名/参数形状/版本过滤）放暴露时；依赖调用上下文（权限/限流/密钥/危险操作）放调用时。
   - 补 §七·4 之外的四个默认拦截位：限流/响应上限/计时/缓存。
   - Namespace Transform（命名空间前缀防同名覆盖）——直接对应本机"MCP 同名冲突"痛点，暴露层预防。
2. **上线后持续评测闭环：生产轨迹按计划回灌评测 + 漂移告警接回滚**（→ wb-skill-authoring）：
   - trace 采集 → scheduled evals → 告警绑定预定义动作（回滚/收窄触发词/摘除技能）。
   - 漂移分型三轴独立阈值：输入漂移 / 输出质量漂移 / 成本漂移。

## 判非重复理由
- 双层拦截 vs wb-spec-driven §七·4（运行时硬拦截）与 §4 工具安全标注契约：§4/标注管"拦什么/怎么声明"，本条管"**治理位分层——哪层放什么**"以及补齐 4 个默认拦截位，重叠 <60%。Namespace 前缀防冲突：本库无对应条目（AGENTS.md 的同名冲突是环境事实非技能纪律）。
- 持续评测闭环 vs r168-B 上线门禁（golden task 预发布回归+两次稳才发）：那条是**发布前**，本条是**发布后**（生产 trace 回灌），互补成两道门。vs r152C 发布侧治理（准入/回滚/进库/排序）：未含 trace 计划评测与漂移分型。vs r161-C 量化评估器：那条管判定器本身，本条管评测的**调度与行动绑定**。
- FastMCP 其余面判不落：Tool Search（工具爆炸→按需搜索）与既有"工具别全塞进 prompt（语义检索分发）"重叠；Tool Fingerprinting 与 line 1956"工具定义是版本化契约"重叠（指纹是其实现细节）；Proxy/stdio 桥接、Session State、DI 凭据注入与本库工作流形态距离远，暂记候选池。
- Evidently 其余面判不落：LLM-as-a-jury 与 wb-spec-driven 评审团/r162-A 评委校准重叠；Descriptors 行级 vs Metrics 数据集级两分法为弱增量；合成对抗测试数据与 sa 2.80 触发评测诱饵用例重叠。
- 提升层级：1=工作流+可复用 Skill；2=工作流。
