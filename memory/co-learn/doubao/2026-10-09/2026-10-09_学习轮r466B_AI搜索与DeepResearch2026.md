# 2026-10-09 学习轮 r466B：AI 搜索与 Deep Research 2026

轮次：r466B（doubao 侧批 r466 第 2 轮）
判重：双键 grep KB 5299 行 + 留痕基线 → 已落相关面：RAG 评估框架（r465B）、Agentic 检索决策（用户偏好）、RAG 与知识库（r465B）——本主题=**2026 深度研究体系面**（Deep Research 核心循环（Plan→Search→Read→Reflect→Iterate→Synthesize，gap detection 回环到 Query Planning；四阶段=query planning/多源搜索/提取排序/结构化报告；Thinker-Actor 递归=fractal tree of inquiry 主 agent 派生子 agent 子 agent 再派生；collaborative_planning 先出计划再执行）、置信度四级评分（单源=low/两独立源一致=medium/三源以上一致=high/源冲突=并陈双方带 URL 留给读者）、事实核查与引文验证（multi-source cross-check+confidence scoring+citation tracing；CiteGuard-RAG 99.1% 检索精度/98.3% 引用有效性，去掉验证层 grounded-answer 精度骤降）、2026 搜索工具对比（Perplexity 92% 实时事实精度 vs ChatGPT 87%、Perplexity 最快 6.8s/报告 2-4 分钟、架构差异=每查询实时搜索 vs 训练数据推理、Perplexity Academic 模式 arXiv/PubMed/Semantic Scholar）、学术组合工作流（三阶段=Perplexity 田野映射+源发现→Perplexity 引文验证+找缺口点每个链接建验证参考列表→ChatGPT/Claude 综合写作））——已落管"RAG 评估指标怎么算"，本面管"2026 深度研究架构+置信度体系+工具选型+学术工作流"，重叠约 35%，独有增量≥65%，按增量判定落地；净增 5 独点。
实拉：3 query×10 站（google-ai-studio-deepresearch/supernodes-deepsearch/github-recursive/zylos-architectures/luowle-deepresearch/myengineeringpath-deepresearch/maxgherman-agentic-search/arxiv-dumate/arxiv-minddr/agentlist-deepresearch + arxiv-qcare/arxiv-rag-playground/microsoft-rag-evaluators/azure-databricks-retrieval/arxiv-citeguard/baai-q2d-web/nsf-trustworthy/azure-it-evaluators/semanticscholar-evidence/acm-genr1 + dev-stimlau/aitrendblend-perplexity/thebestaitools-deepresearch/rawpickai-perplexity/neutrixflow-chatgpt/aiunpacker-30day/tecdigi-perplexity/nesyona-best/awesomeagents-perplexity/toolchase-chatgpt，2026-10-09 实拉），逐站带来源标识。

## 落地 5 独点（每点标注提升层）

### 1. Deep Research 核心循环架构（工作流/可复用 Skill）
来源：zylos / myengineeringpath / github-recursive / luowle / google-ai-studio
- **核心循环**：Plan → Search → Read → Reflect → Iterate → Synthesize；**gap detection 检测到未答子问题就回环到 Query Planning**（不是线性跑完就交）。
- **Thinker-Actor 递归**：主 agent 是根节点，可派生完整独立的子 agent 去查问题子分支——子 agent 还能再派生，形成 fractal tree of inquiry；**上下文预算管理是主导技术挑战**（别把 200K+ token 爬取内容塞进单上下文）。
- **协作规划模式**：`collaborative_planning=True` 先要研究计划回来迭代，定稿后再执行（不直接跑）。
- 提升层：工作流（深度研究管道）。

### 2. 置信度四级评分（可复用 Skill）
来源：supernodes
- **四级置信度**：**单源支撑=low**；**两独立源一致=medium**；**三源以上数据一致=high**；**源冲突=并陈双方+各自 URL，把判断留给读者**。
- 判据：自建深度研究 agent 时直接采用这套——答案若只靠单一来源，必须标低置信。
- 提升层：可复用 Skill（置信度模板）。

### 3. 事实核查与引文验证（工作流）
来源：agentlist / arxiv-citeguard
- **三个子阶段**：iterative retrieval（查询改写/并行搜索/源质量排序）→ **fact verification（多源交叉核对+置信度打分+引文追踪）** → report generation（大纲规划/逐节写作/引文嵌入）。
- **验证层价值量化**：CiteGuard-RAG 受控评测 99.1% 检索精度/98.3% grounded-answer 精度/98.3% 引用有效性；**消融显示去掉验证层后 grounded-answer 精度骤降**（即使检索精度不变）——验证不是锦上添花是必要环节。
- 提升层：工作流（验证管线）。

### 4. 2026 搜索工具对比数据（工具）
来源：tecdigi / awesomeagents / thebestaitools / neutrixflow / aiunpacker
- **量化对比**：实时事实查询 Perplexity 92% vs ChatGPT 87%（独立测试）；Perplexity SimpleQA 93.9%、2026-02 升级达 Deep Search QA/Research Rubric SOTA；**最快 6.8s 中位回答、完整深度研究报告 2-4 分钟**。
- **架构差异才是选型依据**：Perplexity=每查询触发实时搜索（答案反映今天的信息）；ChatGPT=从训练数据推理（有 cutoff，浏览模式需主动开）——**时效性查询选 Perplexity，推理重分析选 ChatGPT**。
- 提升层：工具（选型数据）。

### 5. 学术研究组合工作流（工作流）
来源：toolchase / aitrendblend / nesyona
- **三阶段**：①**Perplexity（Academic 模式）田野映射+源发现**——定主题找关键主题+带链接和 DOI 的验证源清单；②**Perplexity 引文验证+找研究缺口**——确认关键源真实存在，**点每个链接**，建验证过的参考列表；③**ChatGPT/Claude 主题综合与写作**。
- **组合原则**：无单一赢家——Perplexity=快而引用透明的事实研究；ChatGPT Deep Research=推理冲突证据；Gemini=长多源报告；Claude=分析你上传的文档；**重度研究者组合使用**（学术源发现用 Perplexity 因 ChatGPT 不浏览会编不存在的论文）。
- 提升层：工作流（学术研究流水线）。

