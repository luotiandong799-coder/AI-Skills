# 学习轮 r222C：skillsmp p76精选与Langflow升级纪律与Dify记忆分层与n8n版本面与progress drafts增量（2026-09-25）

## 实拉记录（10 次调用，6 成功 / 4 失败计数）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/76（#7501-7559，5944/10664 取） | OK |
| 2 | docs.langflow.org/next/release-notes（1508 全） | OK |
| 3 | Dify 记忆/Agent 节点检索（Mem0/Mintlify/BestHub） | OK |
| 4 | docs.n8n.io what-agents-do.md（667 全） | OK |
| 5 | Hugging Face/模型生态检索（Funes/Agents-A1/smolagents） | OK |
| 6 | WaytoAGI 检索（最简化原则/2026 template） | OK |
| 7 | docs.openclaw.ai/concepts/progress-drafts（4360 全） | OK |
| 8 | activepieces.com/docs/agents/create-an-agent | dead |
| 9 | deepseek-plugin 生态检索（V4.1-Flash/Harness 桌面） | OK |
| 10 | n8n 版本检索（2.40/2.39/n8n Agents） | OK |

## 独点（4 个）
### C1：skillsmp p76 精选：多源时效情报 / 确定性动画 / 估值脚本计算（来源：skillsmp.com/skills/page/76，2026-09-25 实拉）
- **pulse（alirezarezvani/claude-skills ★26,225）**：**多源时效性研究——Reddit/HN/open web/可选 X/Twitter 近窗（默认 30 天）；强制 intake 先澄清主题特异性、角度（趋势/情绪/问题/机会/对比）、时间窗、平台范围再搜索；返回带引用+参与度指标+跨平台模式分析的合成简报**（多源时效情报面）。
- **hyperframes-animation（heygen-com/hyperframes ★52,018）**：**确定性动画知识——原子运动规则+多阶段场景蓝图+转场+7 个运行时适配器（GSAP 默认/Lottie/Three.js/Anime.js/CSS keyframes/Web Animations API/TypeGPU）；单暂停时间线 seek-safe 确定性；审计现有合成编排（animation map）+24 个命名文本动画效果**。
- **equity-research（rollingSirius ★442）**：**机构级研报九章——一手披露优先级自动降级；预期差主线（市场隐含 vs 独立预期）；估值一律脚本计算（反向 DCF+PVGO/三情景概率加权/EPV/EVA 交叉验证+蒙特卡洛）；财报质量核查（应计/M-Score）；结论按预注册标定规则映射+反方论证复核；带来源时间戳存文件**（估值可复算/反方复核纪律）。
- **context-memory-keeper（yushui ★446）**：持久记忆双结构——**Long-term Principles（规则）+Short-term Workbench（任务）**。
- **design-review（Donchitos ★25,342）**：游戏设计文档评审——完整性/内部一致性/可实现性/设计标准符合性，**交程序员前先跑**。
- **提升层**：可复用 Skill / 工作流。

### C2：Langflow 1.12 升级纪律与运行时策略控制（来源：docs.langflow.org/next/release-notes，2026-09-25 实拉）
- **升级四步纪律**：**①导出项目备份 flows（`curl .../api/v1/projects/download/$PROJECT_ID`）→②新 venv/VM 隔离安装新版本（或 Docker 独立容器/桌面隔离机）→③导入 flows 测试新版本（升级组件）→④测试通过后再升级主安装**；流有改动时导出导入回主安装免重复升级组件。判据：**先隔离验证再动主环境——breaking changes/bug 时现有安装保持稳定态**。
- **langflow-base 版本对齐**：`langflow-base` 现为完整版本对齐安装（pin `~=1.12.0` 而非 `~=0.x`）；**bundle 分离完结**：`uv pip install langflow` 只装精选 providers，缺包时组件可见但 flow 不 build，报错点名缺失包（`uv pip install lfx-exa`）。
- **运行时策略控制**：**LANGFLOW_TWEAKS_POLICY 控制 API 调用方运行时可覆盖哪些组件字段；Catalog/Model policy APIs 让 superusers block/allow 组件/模板/模型 providers/具体模型；Admin Page 移除（用户管理走 Users API）**。
- **提升层**：工作流（升级/权限面）。

### C3：Dify 记忆分层与 Agent 节点执行控制 + n8n 2.40/2.39 版本面（来源：Dify 记忆检索 + n8n 版本检索，2026-09-25 实拉）
- **Dify 多轮上下文分层**：短期记忆——**summary 模式压缩早期轮次/key-info 提取只留实体与关键记忆**；长期记忆（1.0 起）——**自动记忆（AI 提取关键事实）/手动记忆（显式写条目）/语义检索召回/记忆过期 TTL**；持久层用 Knowledge Bases+向量库（13+ VECTOR_STORE 可选）经 Knowledge Retrieval 节点检索。
- **Dify Agent 节点执行控制**：**Max Iterations 防无限循环安全限——简单任务 3-5、复杂研究 10-15；Memory 用 TokenBufferMemory 控记忆条数——窗口大上下文多但 token 成本涨**（平衡判据）。
- **n8n 2.40.0**：**AI Agent 节点跨工具调用保留空文本 Anthropic thinking blocks（#38302）；assistant 构建 workflow 优先 native nodes 而非 code nodes（#38598）**；**Anthropic Chat Model v1.6 opt-in prompt caching——TTL 5 分钟或 1 小时，system prompt/tool definitions/对话历史跨请求复用，大 prompt/多工具调用 agent 降成本降延迟（默认关）**。
- **n8n 2.39.0**：Instance AI 永久记忆、workspace 文件夹浏览、**sub-agents 共享沙箱**、公开 API 管理版本（source control）。
- **n8n Agents（2026-09 发布）**：**每个已建 workflow 无需改动即可被 agent 使用——"agent 建一次、随处用"**。
- **提升层**：工作流（记忆/执行控制）/ 工具（缓存/沙箱）。

### C4：OpenClaw progress drafts 工具 typed progress 纪律 + WaytoAGI 提示词最简化 + HF Funes（来源：docs.openclaw.ai/concepts/progress-drafts + WaytoAGI 检索 + HF 生态检索，2026-09-25 实拉）
- **工具 typed progress 机制**：**工具可在单次调用运行中发 typed progress（部分工具结果：content 空+显式 public channel 元数据）——只渲染 progress.text，正常结果仍以 content/details 返回模型；web_fetch 延迟 5 秒才发（快调用无进度行、慢调用有、取消调用清 timer）；progress text 是公共 UI 侧通道，绝不含 secrets/raw args/fetched content/command output/page text**。
- **progress 草稿裁剪**：默认 8 行、行 120 字符（长 path 中间省略保后缀）；finalization 纪律——**发新最终答案优于丢文本/错线程/覆盖草稿（media/审批/长答案/渠道不支持时走正常投递路径不回写草稿）**；工具失败/非零退出不进草稿（错误终态保留草稿作失败记录）。
- **WaytoAGI 提示词最简化三则**：**①不含作者/版本等无关信息；②分类表述避免互相污染（"提供改进建议以及原因"与"评分 1-10 分"并列会错误分类）；③拼写正确（Constraints 拼错=限制条件不可执行）**。
- **HF Funes**：**带记忆的 agent 框架最高减 token 用量 87.5%**（工具面参考）。
- **提升层**：工作流（进度/提示词）/ 工具（记忆）。

## 判重说明
- C1 pulse/hyperframes-animation/equity-research 全新面，落。
- C2 升级四步纪律为通用可内化流程（与已有隔离安装面互补，具体化为备份→隔离→测试→升级），落。
- C3 Dify 记忆分层（TTL/自动手动/TokenBuffer 平衡）为平台具体实现增量（与 wb-context-compressor 记忆提取面互补）；n8n 2.40/2.39 版本面（thinking blocks/prompt caching/共享沙箱/source control）为工具面增量，落。
- C4 typed progress 纪律与 wb-max-token-saver 已落 progress-drafts 面重叠>60% 含≥40% 增量（5 秒延迟/禁 secrets/行裁剪/finalization fallback）合并保留增量；WaytoAGI 最简化原则+Funces 为增量，落。
- 未落：activepieces create-an-agent（死）、n8n what-agents-do（与 agents-vs-chains 面重复）。
