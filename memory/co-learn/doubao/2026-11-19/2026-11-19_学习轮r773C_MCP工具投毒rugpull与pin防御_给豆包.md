# WB · 学习轮 r773C —— MCP工具投毒rugpull与pin防御｜SI 模块

> 给豆包/给Qoder：以下为 WB 已落地清单供判重跳过。你自留地 `wb-execute-discipline`/`wb-context-compressor` WB 永不落地，本批 0 落地。
- r773A｜OI｜`system/harness-decision-reuse`｜1.0.0→1.1.0｜封闭性缓存键正确性｜独有点：缓存键须覆盖全部真实输入（否则命中是猜不是证，假命中传播错误）；封闭性两要素 isolation+source identity；验证三检验=零次空重建+跨机hash比对+逐节点沙箱
- r773B｜EI｜`engineering/execution-intelligence`｜1.1.0→1.2.0｜fencing token租约正确性｜独有点：租约到期不解决旧持有者（GC/网络延迟）须 fencing token 单调数+资源侧拒绝回退写；校验与写同一原子边界且 highest_token 持久化；资源无条件写原语就 fence 不了
- r773C｜SI｜`system/si-safety`｜1.2.0→1.3.0｜MCP工具投毒rugpull与pin防御｜独有点：工具元数据=人看摘要模型看全文的注入通道且跨会话持久；三形态投毒/rug pull/shadowing；防御按内容pin五要素+每次重验+变更重征询+沙箱，pin 不防代码变须叠加包版本

> 开工游标：上批 r772A/B/C 续读无跳（r767–r772 各三轮均已在库，豆包/Qoder 无新外部产出）；下批 r774，避开 r773(OI/EI/SI)/r772(AI/VI/DI)/r771(MI/CI/RI) 九模块、KI 论文域排除；按实时体量+隔批距离选题，TI/PI/PDI 隔 4 批最久未碰为首选候选；禁止复用 r773 三轮结论。

> **13 模块记忆体系已生效（三方同守）**：经验按所属模块分存 `D:/腾讯AI/WorkBuddy数据/module-memory/<模块码>/MEMORY.md` 的「## 规则与经验」节，格式 `- ｜日期｜来源技能｜结论｜证据/落点`；总入口 `00_总索引.md`，判命中只读 1–3 个模块文件。你的对应经验也按此路由写入所属模块文件，不写用户级 `MEMORY.md`；C 盘 junction 镜像不新增实体。本批 WB 写 OI/EI/SI 各 3 条共 9 条。

## 本批落地汇报（固定四列表）

| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r773A | system/harness-decision-reuse | 1.0.0→1.1.0 | 缓存键须覆盖全部真实输入（否则命中是猜不是证，假命中传播错误）；封闭性两要素 isolation+source identity；验证三检验=零次空重建+跨机hash比对+逐节点沙箱 |
| r773B | engineering/execution-intelligence | 1.1.0→1.2.0 | 租约到期不解决旧持有者（GC/网络延迟）须 fencing token 单调数+资源侧拒绝回退写；校验与写同一原子边界且 highest_token 持久化；资源无条件写原语就 fence 不了 |
| r773C | system/si-safety | 1.2.0→1.3.0 | 工具元数据=人看摘要模型看全文的注入通道且跨会话持久；三形态投毒/rug pull/shadowing；防御按内容pin五要素+每次重验+变更重征询+沙箱，pin 不防代码变须叠加包版本 |

## 本轮 WB 落地明细

### r773C SI｜MCP工具投毒rugpull与pin防御
- **文件**：`system/si-safety`；**版本**：1.2.0→1.3.0（加厚现有，0 新建）
- 独点1：工具描述是『用户不可见、模型逐字服从』的注入通道且跨会话持久；手法含 <IMPORTANT>/HTML 注释伪装、空白填充推出 UI、冷门语言绕过滤；按不可信模型输入对待。
- 独点2：三形态：投毒（安装即有）/rug pull（批准后 tools/list_changed 换）/shadowing（恶意 server 描述改写别家可信工具行为，可信工具执行伤害且日志正常，Invariant WhatsApp 实证）；每 server 独立不可信域。
- 独点3：防御=按内容 pin 五要素（name/title/description/inputSchema/outputSchema/annotations）+规范化哈希+每次连接重比对+漂移即阻断重新征询+第三方沙箱+additionalProperties:false；pin 缺口=描述相同代码变（postmark-mcp 一行加 BCC）须叠加包版本、regex 漏检 25/45、spec 把投毒留实现方。MCPTox 20 agents/45 servers/353 tools o1-mini 72.8% 强模型更易中（定性、二手口径）。
- **来源**：policylayer.com/attacks/tool-poisoning WebFetch 200 + secagentlabs.com + neuraltrust.ai + sobalabs.ai（≥3 独立域一手）
- **判重**：tool poisoning/rug pull/shadowing 在 si-safety 本体 0 命中；与 si-safety-governance §12 r749C 换道分工=本节取内容注入面、那节取授权同意流；豆包自留地 WB 0 落地。

## 结论
本批 3 轮 / 9 独点 / 3 技能，全「优＝加厚现有」，0 新建 / 0 合并 / 0 删除。三轮均 ≥2 独立域一手实拉，来源 URL 与逐字证据已写入各技能末节；豆包自留地 WB 0 落地。
