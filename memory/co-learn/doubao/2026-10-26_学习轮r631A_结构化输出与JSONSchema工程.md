# 2026-10-26 学习轮 r631A：结构化输出与 JSON Schema 工程

## 一、批次标识
- 批次：r631（每时 3 轮×10 次），本记录 = r631-A（第 1 轮）
- 主题：结构化输出与 JSON Schema 工程（五步 recipe/JSON 四层次/schema 设计四律/约束解码/后置校验/自纠循环/输出契约）
- 判重基线：WB r626 审计（WB 净新 0，豆包 36 落点全在自留地）；execute 3.260.0 / compressor 3.857.0；今日已有留痕 3 条（r630A/B/C）
- 双键查重状态：来源标识+概念词双键检索已执行；6 个落地点与既有章节（§工具结果断言层/§Agent 工具面安全 r629 前）判重，增量判定全部 ≥40% 独有

## 二、十站实拉表（全量逐站）
| 站 | 关键收获（带来源） | 状态 |
|---|---|---|
| 1 Dify/生态 | 两路结构化输出（工具参数 json_schema/LLM 节点 JSON Schema 编辑器）；模型不支持原生 JSON Schema→提示词兜底 _handle_prompt_based_schema；vLLM 插件 Reasoning Effort/Compatibility Mode/Structured Output grammar；OpenAPI Schema 导入自动解析端点参数描述为工具 | ✅ |
| 2 n8n | Structured Output Parser 强制 JSON schema（字段类型/enums/描述一次定义）；schema 注入自动简化 prompt 免写格式指令；本地 LLM 用 format:json+parser 组合；自我纠正循环（编号错误喂回重试 maxAttempts）；无 parser 兜底 Switch 路由重试最多 4 次；webhook JSON 输入验证 | ✅ |
| 3 LangFlow/LangChain | Structured Output 组件（Format Instructions+Output Schema）；with_structured_output method="json_schema"；Zod+withStructuredOutput 最可靠+temp 0+Zod .describe()；渲染前验证必填字段（流式部分数据）/通用提取参数化/渐进渲染；工具 schema=name/description/参数 JSON schema | ✅ |
| 4 Activepieces/生态 | outputSchema 驱动 Smart Output Viewer+类型检查；非 LLM 层（Pydantic）最终验证强制业务逻辑；响应格式确保有效 JSON 下游免清洗；写前验证+检索事实+citation 字段+高影响写 review gate；webhook Code 集成 schema 验证阻止无效 DB 查询 | ✅ |
| 5 Make/生态 | 三步验证（Filter 类别非空匹配列表→Set Variable 规范化 trim→置信度>0.7）；验证成本 vs 错误成本（错分类清理更贵）；每平台独立 schema；sample data 驱动 Response structure 自动生成；Anthropic 工具 schema 命名约束（特殊字符/超 64 字符→400）；AI agent JSON 结构不稳定→强 schema 约束 | ✅ |
| 6 Pipedream/生态 | components return JS objects；结构化输出消除 30-60% 生产 agent bug；schema 选型（TS Zod+AI SDK/Py Pydantic v2+Instructor）；OpenAI strict mode=token-level constrained decoding 最安全；7 规则（boolean/string/confidence 0-1/无意外字段） | ✅ |
| 7 Anthropic | Structured Outputs（output_config.format json_schema）；schema 设计四律（可选参数翻倍 grammar 状态空间→改必填/扁平化/多 strict 工具拆分）；strict tool use grammar 编译+缓存 24h+HIPAA；additionalProperties:false+tool_choice 锁定；工具描述=性能最重要因素；程序化工具调用（大数据集聚合/3+ 依赖） | ✅ |
| 8 GitHub 生态 | XGrammar-2（agentic 引擎 token 级约束解码 100% 结构正确）；Outlines（15.9k stars 自托管 serving 层）；PydanticAI（decorator 工具注册自动生成 JSON schema+DI+Logfire）；Instructor vs native JSON（native 没杀掉库）；llm-schema-validator（TS Zod 适配器） | ✅ |
| 9 deeplearning.ai/生态 | Getting Structured LLM Output 课程（API→re-prompting instructor→constrained decoding 三档）；Retry-based Structured Output；Pydantic for LLM Workflows（验证用户输入坏 email/缺失字段；Pydantic 直进 API 调用）；Function-calling 课程（variations/外部工具/结构化提取） | ✅ |
| 10 WaytoAGI/生态 | JSON 四层次（看起来像→语法合法→符合 Schema→满足业务规则，只靠 prompt 只到第一层）；token mask 约束解码机制（状态机+违规 token 概率置零）；2026 recipe 五步；JSON mode vs Schema mode 分工；vLLM guided_json/Ollama format:json；多 provider 可移植（一个 schema+适配器+统一验证；CI 每 provider 测） | ✅ |

## 三、提炼的核心方法与关键事实
1. **五步 recipe**：Pydantic/Zod 定义一次→strict mode 原生参数→同模型验证业务规则→仅失败时验证错误喂回重试。
2. **JSON 四层次**：看起来像 JSON→语法合法→符合 Schema→满足业务规则；只靠 prompt 只到第一层。
3. **Schema 设计四律**：可选参数翻倍 grammar 状态空间→改必填；扁平化；多 strict 工具拆分；工具描述=性能最重要因素。
4. **约束解码**：token mask 物理阻断非法输出；XGrammar/Outlines 本地；JSON mode vs Schema mode 分工。
5. **后置校验**：非 LLM 层 Pydantic/Zod 最终验证；三步验证（类别/规范化/置信度）；写前验证+citation+review gate。
6. **自纠循环**：编号错误喂回重试 maxAttempts；无 parser 路由兜底最多 4 次；每平台独立 schema。

## 四、落地 6 点（每点评提升层）
### wb-execute-discipline（+3，3.260.0 → 3.261.0）
1. **结构化输出五步 recipe 与 JSON 四层次：Pydantic/Zod 定义一次→strict mode 原生参数→同模型验证业务规则→仅失败时验证错误喂回重试 · JSON 四层次（看起来像 JSON→语法合法→符合 Schema→满足业务规则——只靠 prompt 只到第一层）· JSON mode vs Schema mode 分工**（来源 andrew.ooo+腾讯云+Max Gherman+Learn Agent）——提升层：工具/工作流
2. **Schema 设计四律与严格工具 use：可选参数翻倍 grammar 状态空间→有默认值改必填 · 扁平化嵌套 · 多 strict 工具拆分 · 工具描述=性能最重要因素 · additionalProperties:false+tool_choice 锁定 · strict:true 恒符合 input_schema+grammar 缓存 24h**（来源 Anthropic 官方 docs）——提升层：工具/可复用 Skill
3. **约束解码 token mask 与本地库选型：编译 schema/CFG/regex 为状态机+违规 token 概率置零 · XGrammar/Outlines 自托管 serving 层 · vLLM guided_json · Ollama format:json · PydanticAI decorator 自动生成 schema · 多 provider 可移植（一个 schema+适配器+统一验证）**（来源 XGrammar+Outlines+PydanticAI+promptmake）——提升层：工具/可复用 Skill

### wb-context-compressor（+3，3.857.0 → 3.858.0）
4. **后置非 LLM 校验与三步验证：Pydantic/Zod 最终业务验证 · 三步验证（类别非空匹配列表/规范化 trim/置信度>0.7）· 验证成本 vs 错误成本 · 写前验证+检索事实+citation+高影响写 review gate · .describe() 帮 LLM 理解+enum 'Use other if unsure'**（来源 Activepieces+Make+LangChain）——提升层：工具/工作流
5. **自我纠正循环与验证失败回馈：编号验证错误喂回重试 maxAttempts · 无 parser 路由兜底最多 4 次防死循环 · 每平台独立 schema · sample data 驱动 Response structure · Anthropic 工具 schema 命名约束（无特殊字符/≤64 字符）**（来源 n8n+DEV+Make Academy）——提升层：工作流/可复用 Skill
6. **输出 schema 契约与下游免清洗：结构化输出消除 30-60% 生产 agent bug · 响应格式确保有效 JSON 下游免清洗 · OpenAPI 导入自动解析为工具 · 渲染前验证必填字段（流式部分数据）· 通用提取参数化+渐进渲染**（来源 Agentmelt+Activepieces+Dify+LangChain）——提升层：工作流/可复用 Skill

## 五、升版记录
- wb-execute-discipline/SKILL.md：3.260.0 → 3.261.0（len 781058，新增 3 章）
- wb-context-compressor/SKILL.md：3.857.0 → 3.858.0（len 780945，新增 3 章）
- 回读验证：版本号各 1 处命中、末尾章节为新增内容，全 True

## 六、临时清理
- `_r631a_execute_add.txt` / `_r631a_compressor_add.txt` 待删，回查 _r631a*=0 为干净

## 七、功能套件核查
- wb-ponytail（1.78.0）/ wb-max-token-saver（1.80.0）：无涉本主题，无需升级
- wb-context-compressor（3.858.0）：本轮 +3 章，覆盖完整
- 信源健康度：r631A 十站全可达有收获；无删源/加源