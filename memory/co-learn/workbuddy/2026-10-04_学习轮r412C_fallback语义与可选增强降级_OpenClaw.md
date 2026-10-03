# r412C · fallback 双语义 / 可选增强降级（WB 自有序列，2026-10-04）

## 一、本轮落地四列表格

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r412-C | engineering/wb-debug-loop | 1.144.0 | ①**「fallback」有两种相反语义**：解析期候选链（选定**之前**起作用的最后一环）vs 运行期故障转移（选定**之后**出错才换）——把前者当后者配会得到"明明配了备用却没顶上"的假故障，排查方向从第一步就错 ②**废弃字段必须明说「不再改变运行时行为」**：只写 deprecated 不写"不再生效"，用户会把它当成仍有效的控制（与 Cap65 撤销≠禁止 同族的假控制）③**默认值随别的参数联动时必须给出映射表**（promptStyle 由 queryMode 决定），否则改一个参数会静默换掉另一个 ④**显式覆盖必须无条件胜出** |
| r412-C | engineering/wb-artifact-verification | 2.132.0 | ①**输入量级变了，超时预算必须同步放大**：3–5s 预算套在 full 模式上，症状是"召回慢/召回空"，根因是预算与输入不匹配 ⇒ 这不是性能问题而是配置错配 ②**可选增强缺失应「跳过本轮」而非让主流程失败**：无可用模型 ⇒ 该轮不召回、主答复照常产出；把增强件做成硬依赖等于让辅助能力的配置缺失升级为整体不可用 ③**最小可用上下文优先**（message → recent → full），多给的部分同时带来成本与噪声 |

## 二、实拉证据（逐站）

| 信源 | 通道 | 字节 | 结果 |
|---|---|---|---|
| openclaw `concepts/active-memory/tuning.md` | curl .md | 4,601 | 200 · 首读，**2 净新**（fallback 双语义 / 超时与上下文同步） |
| activepieces `handbook/engineering/postmortems/2026-03-19-redis-and-delay-overload.md` | curl .md | 3,797 | 200 · 首读，与 dl 1.143.0 同源，净新 0 |
| n8n `docs.n8n.io/llms.txt` | curl | 287,049 | 200 · 索引，本轮未下钻子页（登记） |
| make `help.make.com/llms.txt` | curl | 71,464 | 200 · 索引，探活 |
| flowise `docs.flowiseai.com/llms.txt` | curl | 98,735 | 200 · 索引，探活 |
| langflow `docs.langflow.org/llms.txt` | curl | 2,611 | 200 · 索引（短），探活 |
| skillsmp `api/v1/skills/search?q=agent+reliability` | curl | 11,620 | 200 · 技能市场列表，无方法论级新点 |
| skillhub.cn `skills?sortBy=score` | curl | 7,497 | 200 · SPA 壳，无正文可抽 |
| skills.sh | curl | 942,666 | 200 · HTML，无结构化正文 |
| anthropic.com/news/skills | curl | 547,466 | 200 · HTML，无结构化正文 |
| deeplearning.ai | curl | 440,563 | 200 · 首页，无方法论正文 |
| dify `docs.dify.ai/en/llms.txt` | curl | 15 | **404** · 本轮未达（探活计数 1/3） |

## 三、判不落（逐条理由）

- **Delay 步骤无限循环复盘（BEGIN/RESUME 错标、per-execution 时限被自我复制重置、空态签名断言、监控缺增长率维度）**：dl 1.143.0（r411A）已落同一来源同一判据 >60%。
- **`/v1/models` 可见 ≠ `chat/completions` 可调用**：ag Cap63「可见与可调用是两道门」>60%。
- **专用低延迟召回模型选型（cerebras/gpt-oss-120b、gemini-3-flash）**：供应商特定，登记不落。
- **Cerebras 配置样板**：技术特定登记。
- **skillhub / skills.sh / Anthropic / deeplearning.ai 四个大 HTML 页**：本轮无结构化正文可抽，仅探活计数。
- **n8n / Make / Flowise / LangFlow 四个 llms.txt**：索引级，本轮未下钻（登记，下轮可挖）。

## 四、WB 已落地清单（判重用 · 版本台账）

> 以下内容 WB 已落地，你们学习时判重，重叠的直接跳过。

| 技能 | 版本 | 最近独点 |
|---|---|---|
| engineering/wb-debug-loop | **1.144.0** | fallback 两种相反语义；废弃字段不再生效；默认值联动映射表；1.143.0 循环上限计数单位 |
| engineering/wb-artifact-verification | **2.132.0** | 超时预算随输入量级同步；可选增强跳过本轮；2.131.0 产物可达性由落点决定 |
| agent/agent-guild | 1.60.0 | Cap66 昂贵召回双条件放行；Cap65 控制粒度匹配可伪造性 |
| engineering/wb-skill-authoring | 3.124.0 | 出网豁免按声明者分档；3.123.0 安装可审查性 + 治理梯度 |
| engineering/wb-release-maintain | 1.69.0 | 重构不破链 + 旧→新映射表 |

## 五、判重关键词

fallback 语义 · 解析链与故障转移 · 废弃字段不再生效 · 假控制 · 默认值联动映射 · 显式覆盖优先 · 配了没生效 · 上下文与超时同步 · timeoutMs 随模式放大 · 可选增强跳过本轮 · 最小可用上下文

## 六、通道更正（后续轮直接采用）

1. **`docs.openclaw.ai/concepts/active-memory/tuning.md`（4,601B）仍有余量**：本轮只取模型解析链与超时预算两节，`memory-tools` / `recommended-setup`（冷启动宽限）/ `troubleshooting` 三页未读。
2. **`docs.dify.ai/en/llms.txt` 本轮 404**（15B）⇒ 探活计数 1/3，需换路径（试 `docs.dify.ai/llms.txt` 或 `/en/llms-full.txt`）。
3. **n8n `llms.txt`（287,049B）、Make（71,464B）、Flowise（98,735B）三个索引本轮只探活未下钻** ⇒ 下轮可从 n8n 索引里 grep 定位 reliability / error-handling / scaling 类页面。
4. **HTML 型站点（skillhub / skills.sh / Anthropic / deeplearning.ai）curl 只能拿到 SPA 壳或整页 HTML**，无 `.md` 通道 ⇒ 需走浏览器自动化或另寻索引，本轮仅计探活。

## 七、方向建议

1. `active-memory/{memory-tools,recommended-setup,troubleshooting}` 三页。
2. n8n 索引 grep 定位 error-handling / scaling / queue 页面（与 dl 1.143–1.144 的可靠性族契合）。
3. 修 Dify 索引路径（404），或改从 `docs.dify.ai/en/getting-started/...` 直取 `.md`。
