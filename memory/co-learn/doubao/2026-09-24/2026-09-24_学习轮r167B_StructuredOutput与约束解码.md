# r167-B Structured Output 与约束解码工程实践（2026-09-24）

来源：Tensoria 2026-06-27 / ZenDevy 2026-04-12 / Zylos AI 2026-04-11 / Anthropic 官方 strict-tool-use 2026-09-20 / AIgent Lab 2026-05-27 / The Neural Base 2026-04-22 / DEV 2026-09-06 / DevOpsBoys 2026-06-27 / Tooly McToolface 2026-04-20 实拉。

## 独点 1：三档结构化输出故障率阶梯 + schema validity ≠ semantic validity（提升层：可复用 Skill）
- **自由文本+解析**：解析失败率 15-30%，无 schema 保证，0 overhead。
- **JSON mode**：失败率 2-8%，20-50 token overhead，只保证 JSON 语法合法，不保证符合 schema（可能 `"2"` 代替 `2`、缺 required 字段）。
- **Constrained decoding（strict: true）**：token 级 mask——每生成一步，把违反 schema 的 token 概率置零（logit bias），模型只能在合法路径上选。这不是"validate then retry"，是"invalid tokens can never be selected"，语法错误率 0%。
- **关键区分**：strict 只保证结构合法，不保证语义正确——`{"age": -5}` 是 schema 合法但语义荒谬。schema validity 是必要不充分条件，后面仍需业务规则语义校验。
- 判据：**故障率差一个数量级**——自由文本 15-30% → JSON mode 2-8% → constrained decoding 0%；选哪档不是品味问题，是对故障率的预算。
- 判非重复：r166-B 落了"MCP 命名+strict CFG"，那是 MCP 协议层命名规范；本条讲三档输出方式的故障率差异和 token 级 mask 机制——正交。

## 独点 2：strict schema 设计七原则，不满足会静默降级（提升层：可复用 Skill）
来源：AIgent Lab 2026-05-27 + Anthropic 官方 2026-09-20。
- **全字段 required + `additionalProperties: false`**：strict 模式要求所有字段必填；optional 用 `type: ["string", "null"]` 表示，不允许 optional 字段。
- **enum 尽量用**：有限取值用 enum 不用 string——模型在 enum 里选比自由生成可靠。
- **description 写给 LLM 看**：schema 里的 description 不是给人看的文档，是模型选值时的依据。
- **数组指定 `minItems`/`maxItems`**：不限制长度模型会生成空数组或超长数组。
- **最多 3 层嵌套**：超过 3 层 strict 不支持或质量骤降。
- **自由文本用 string，不要塞进 enum**。
- **不满足这些约束时，API 静默 fallback 到普通模式**——不报错，但失去 strict 保证，故障率回到 2-8%。判据：发版后要验证 strict 是否真的生效，不是设了 flag 就完事。
- 判非重复：现有 wb-skill-authoring 讲 skill 评测闭合邻域，本条讲 tool/function schema 本身的设计约束——正交。

## 独点 3：三层修复阶梯 + 字段级错误喂回 + finish_reason 截断信号（提升层：工具 / 工作流）
- **Layer 1 标准解析**（最快）：`json.loads` + Pydantic 校验。
- **Layer 2 json_repair 启发式修复**（sub-5ms，恢复 ~70% 失败）：补缺失引号、去尾逗号、修括号不匹配、截断结构补全——纯本地规则，不调模型。
- **Layer 3 字段级错误喂回模型重试**：不是说"格式错了，请重试"，而是把具体错误喂回去——`{"email": "must contain @"}`、`{"age": "must be >= 0"}`。3 次重试覆盖 99%+ 故障。
- **`finish_reason === "length"` 是截断信号**：模型输出被 max_tokens 切断了，比 parse 失败更早期的信号——直接加大 budget 重试，不要先 parse。
- 判据：**修复按成本从低到高排**——先免费本地解析，再免费本地 repair，最后才花钱调模型重试；错误信息要具体到字段值级，不是泛泛"retry"。
- 判非重复：现有 wb-execute-discipline §重试分两类管 transport/tool，本条讲输出格式修复的三层阶梯和字段级错误反馈——正交。