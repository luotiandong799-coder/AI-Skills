# AI 输入入口增强系统（WeChatBridge 融合终版）

> 版本：1.0.0（重建版）
> 来源说明：**本文件重建自 2026-09-27 对话中丢失的原文大纲（12 章标题）+ 现有 WB 体系（AGENTS.md / rules / 现有 skills / co-learn）**。非用户原稿逐字版，待用户校正后定稿。
> 定位：**编排/元层原则文档**，不是新 skill。依原则一「不新增重复 Skill」，与现有 skill 重叠 >60% 处一律引用，不重复建。

---

## 一、总原则（不新增重复 Skill）
- 落地任何输入增强前，先全库 grep 关键词；与现有 skill 重叠 >60% 不重复建，改引用或并入。
- 本系统只定义「入口如何归一、如何判断、如何路由」，具体能力由现有 skill 提供。
- 根目录禁止平铺技能（见 `00_总目录_所有AI入口.md` §3）。

## 二、统一 AI 输入层（文本 / 图片 / 文件）
所有来源（微信 / 聊天 / 文件 / 浏览器 / CLI）归一为输入对象：
`{ type: text|image|file, source, raw, meta }`
- 文本：直入处理流。
- 图片：走 `media/image-processor` / `media/wb-media-forensics`（抽帧读图）。
- 文件：走 `engineering/wb-doc-file-intel` / 腾讯文档系技能。
- 浏览器来源：见 `system/browser-automation`。

## 三、统一信息处理流程
`输入 → 识别来源 → 判类型 → 提取核心 → 补上下文 → 判目标 → 选 Skill → 执行 → 验证 → 记录`
- 流程骨架：`engineering/wb-spec-driven`
- 执行纪律：`engineering/wb-execute-discipline`（点名目标须真实执行，不抽样）
- 验证：`engineering/wb-artifact-verification`（三条独立证据源判定成败）

## 四、信息价值判断（高 / 中 / 低）
- **高**：用户明确指令 / 含决策 / 含任务 / 涉隐私需处理 / 跨会话复用 → 全量处理 + 记忆沉淀。
- **中**：参考性 / 可学 → 抽要点入记忆或共学。
- **低**：寒暄 / 冗余 / 已处理 → 压缩或丢弃。
- 价值筛选机制见 `defaults/wb-context-compressor`（只注相关信息，不重复搬运无关上下文）。

## 五、聊天信息增强
- 自动理解上下文：连续对话的引用 / 指代消解，不丢关键约束。
- 回复辅助：草拟不代发；除非用户显式授权。
- 微信通道：`wechat-desktop-claw-automatic-control__skillhub`（只发不读）、`workbuddy-claw-wechat-send`。
- 对外发消息默认先确认；用户已授权企微直发「原样透传原话」（见 `rules/04_wecom企业微信`）。

## 六、自动任务提取
从输入抽取 `{ 任务 / 负责人 / 时间 / 优先级 / 下一步 }`，结构化进任务系统或工单。
- 拆工单：见 `engineering/to-tickets`（先核对粒度与依赖再写）。

## 七、AI 输入路由系统
- 按 `来源 + 类型 + 目标` 选 Skill；未匹配走显式默认路由（见 `wb-spec-driven` 1.100 Fallback，不静默丢弃）。
- 跨 agent 交接 / 共享记忆：见 `agent/agent-guild`（收件箱交接、每日日志、学习台账）。

## 八、隐私安全规则
- 私密不入公开仓；密钥 / token / cookie / secret 不提交（见 `rules/06_Git与仓库红线`）。
- 敏感输入走护栏：`wb-artifact-verification` 四模式（block / redact / retry / require-approval）+ secret/PII 内置检测器。
- 用户真实文件永不永久删除，优先回收站（见 `rules/01`）。

## 九、记忆管理规则
- 长期事实（A 级）进 `MEMORY.md`；方法 / 规范进 `rules/`；过程进 Daily Log；升级需验证。
- 详细见 `rules/07_记忆管理规则`（可信度分级、冲突优先级、优化闭环）。
- 共学双写 `memory/co-learn/<工具名>/`，命名 `YYYY-MM-DD_主题.md`。

## 十、开源项目学习机制
- 信源全量实拉（含腾讯 SkillHub `skillhub.cn/skills?sortBy=score` 分数面）；区域封锁站点留痕不重复试。
- 每次触发连跑 A/B/C 3 轮独立实拉，不共用；独点判定重叠 <60% 才落。
- 落地汇报用四列表格（轮 / 文件 / 版本 / 独有点）。
- 调度见自动化 `070cce0c`；总入口见 `00_总目录_所有AI入口.md`。

## 十一、执行标准（Fast / Deep）
- **Fast**：单步 / 明确任务直接做，开工先报总步数；N≥2 渲染进度。
- **Deep**：多步 / 模糊任务走 `wb-spec-driven` 计划 → 实现 → 验证；失败 ≥2 次必根因诊断（见 `wb-debug-loop`）。
- 默认三件套常开：`wb-ponytail`（决策少写）/ `wb-max-token-saver`（输出压缩）/ `wb-context-compressor`（输入压缩）。

## 十二、最终目标
WB = **统一 AI 信息入口**：任意来源输入 → 归一 → 价值判断 → 路由到正确 Skill → 执行验证 → 记忆沉淀。全程隐私安全、无重复建设、跨 agent 共享记忆。
