# 学习轮 r225B：skillsmp p84精选与Dify混合检索与n8n输出解析器与Anthropic技能分类框架与Activepieces版本管理（2026-09-27）

## 实拉记录（10 次调用，10 站实拉）
| # | 站点 | 结果 |
|---|---|---|
| 1 | skillsmp.com/skills/page/84（#8301-8350 取） | OK |
| 2 | Dify 检索（embedding/向量库/混合检索/rerank/多模态） | OK |
| 3 | n8n 检索（AI Agent 设置/Output Parser/记忆子节点） | OK |
| 4 | LangFlow 检索（RAG/PDF 用例/Docling） | OK |
| 5 | Activepieces 检索（版本管理/回滚/pieces 打包/Projects） | OK |
| 6 | Make 检索（AI Agent New/knowledge files/最佳实践） | OK |
| 7 | Pipedream 检索（Connect managed auth） | OK（与 r224-C 重叠，无新增不落） |
| 8 | Anthropic 检索（技能九类框架/verification loops/触发调优） | OK |
| 9 | GitHub 检索（awesome-claude-skills 规模/agentskill.sh/lean-ctx） | OK |
| 10 | agentskills.io 检索（规格三维/gh skill/metadata 字段） | OK |

## 独点（4 个）
### B1：skillsmp p84 精选：反推拆解 / 持久 SEO 工作流 / 脚本口语化（来源：skillsmp.com/skills/page/84，2026-09-27 实拉）
- **storyboard-scene-breakdown（2799662352/ai-image-master）**：**爆款视频/参考图拆解成可复刻提示词——不输出标签词堆砌，输出时间切片/构图机位/主体动作/光影方向/环境纵深/镜头运动**（AI 视频面增量，r224-C storyboard-consistency 互补：那条管"生成保一致"，这条管"从成品反推拆解"）。
- **seoagent（davila7/claude-code-templates ★30,896）**：**持久 SEO 工作流——技术 SEO 审计→hub-and-spoke 关键词策略→page-type-aware 内容简报→SEO 文章；产物持久化到 .seoagent/ workspace，跨会话累积**（SEO 工作流+持久 workspace 模式面——"工作产物落盘跨会话复利"与用户既有的"唯一落地位置+留痕"一致）。
- **huashu-script-polish（alchaincyf/huashu-skills ★1,581）**：**视频脚本口语化审校——去书面腔让脚本适合说出来**（脚本写作面专项）。
- **提升层**：工作流 / 可复用 Skill。

### B2：Dify 检索面：混合检索三模式 + Rerank 权重 + 多模态统一语义空间（来源：dify.ai/docs + mintlify，2026-09-27 实拉）
- **检索三模式**：**Vector Retrieval（语义）/Full-Text Retrieval（关键词精确，适合产品码/名称/ID）/Hybrid Retrieval（语义+全文+rerank，精度最高但慢、需 rerank 模型）**——按查询类型选模式而非一律向量。
- **Rerank 细节**：**Weighted Score=语义相似度与关键词匹配的相对权重（仅所有 KB 均 High Quality 模式可用）；Rerank Model 用第三方（Cohere rerank-multilingual-v3.0 等）对混合结果重排**（r224-B 双层检索面深化：权重语义+前置条件）。
- **多模态检索（v1.11.0）**：**多模态 embedding 放统一语义空间——Image-to-Text/Text-to-Image/Image-to-Image 检索；配多模态 rerank（Vision 图标）；自动提取 Markdown 链接图片（JPG/PNG/GIF ≤2MB）**（多模态检索面）。
- **向量库选型**：**Weaviate 多模态/Milvus 十亿级企业/Pinecone 完全托管**。
- **提升层**：工作流 / 工具。

### B3：n8n 输出解析器 + Anthropic 技能分类与触发调优（来源：blog.n8n.io + claude.com/blog + resources.anthropic.com，2026-09-27 实拉）
- **n8n Require Specific Output Format 三种 Output Parser**：**Structured Output Parser 强制 JSON schema（定义 allowed values/types/required fields——输出恒定一致，category 永远是 "billing" 不会变体）；Auto-fixing Output Parser（解析失败自动让模型修复）；Item List Output Parser**（输出校验面，与 r224-C doublecheck 互补：那条管"事实对不对"，这条管"格式恒定型"）。
- **Anthropic Claude Code 技能九类框架（2026-06-03）**：**内部技能聚类成九类；最好的技能干净落一类，跨多类的会混淆 agent——用九类框架识别自己技能库空白与越界**（技能治理面，可直接用于自查现有技能库）。
- **Verification loops 技能化（2026-07-22）**：**验证循环（跑测试/lint/自定义检查→修失败→继续）打包成技能，每会话自动应用相同检查，不靠人记住**（验证工作流面，与 wb-artifact-verification 互补）。
- **Under/Overtriggering 信号调 description**：**undertriggering（该载未载/用户手动启用）→描述加细节与关键词；overtriggering（无关查询也载/用户禁用）→加负面触发词更具体**（触发调优方法面）。
- **提升层**：工作流 / 可复用 Skill。

### B4：Activepieces 版本管理 + 技能生态规模 + lean-ctx（来源：activepieces.com/docs + chat2anyllm.github.io + agentskills.io + agskills.dev，2026-09-27 实拉）
- **Activepieces flow 版本管理**：**草稿模式随便改→发布即锁定不可编辑；改已发布 flow 自动建新草稿并从已发布版本复制；可回滚到任意版本（无版本上限/无自动清理——完整审计轨迹但存储增长）；rollback 命令 `docker run ... npm run rollback -- --to 0.77.0`；监控类工作流建议 peer review 步骤+版本化发布+回滚**（工作流发布-回滚面，与 r195-A A4 迁移三步验收互补：那条管数据库迁移，这条管 flow 发布）。
- **Activepieces pieces 打包（2026-09）**：**每个 piece（含依赖）编译成单个 KB 级产物而非多 MB 模块树**（打包优化面）。
- **技能生态规模事实**：**awesome-claude-skills 数据（2026-08-13）：启用源仓库 3,410、可发现技能 121,584、健康仓库 3,315；agentskill.sh 可安装 69,000+ skills（20+ AI 工具）；Agent Almanac 317 skills/65 agents/14 teams；GitHub `gh skill` CLI（2026-04-16）管理技能发现/安装**（生态规模+CLI 面）。
- **lean-ctx**：**MCP server + context runtime——session caching、AST-aware compression、90+ shell patterns 降 token**（上下文压缩工具面，与 wb-context-compressor 互补）。
- **提升层**：工具 / 工作流。

## 判重说明
- B1 全为新面（反推拆解/持久 SEO 工作流/脚本口语化），落。
- B2 混合检索三模式+Weighted Score+多模态统一语义空间为 r224-B 双层检索深化（含独有增量），落。
- B3 n8n 三种 Output Parser 未落过（r224-C doublecheck 是事实验证）；Anthropic 九类框架/verification 技能化/触发调优未落过；落。
- B4 Activepieces 版本管理新；技能生态规模新事实；lean-ctx 新；落。
- 未落：Make knowledge files（机制简单且与已有记忆面重叠>60%）；Pipedream managed auth（r224-C 已落 Connect）；LangFlow RAG 用例（与既有 RAG 面重叠）。
