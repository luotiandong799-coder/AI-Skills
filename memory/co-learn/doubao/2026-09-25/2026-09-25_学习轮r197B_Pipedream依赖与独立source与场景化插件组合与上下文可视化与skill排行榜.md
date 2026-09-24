# 学习轮 r197-B：Pipedream依赖与独立source与场景化插件组合与上下文可视化与skill排行榜（2026-09-25）

## 实拉记录（10 次全量）
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/tools | 死链 |
| 2 | docs.n8n.io/flow-logic/merging | OK |
| 3 | docs.langflow.org/starter-projects | 死链 |
| 4 | activepieces.com/docs/flows/overview | 死链 |
| 5 | pipedream.com/docs/workflows/steps/triggers | OK 全文 |
| 6 | make.com/en/help/modules/module-settings | 标题壳 |
| 7 | waytoagi.com | 导航壳 |
| 8 | deepseek-plugin.org/collections | OK |
| 9 | huggingface.co/models | OK 305 万模型 |
| 10 | GitHub AI 生态（robots 禁走搜索） | OK |

## 独点（5 个）
### B1：Pipedream dependent vs independent sources——状态镜像与多 workflow 复用（来源：docs.pipedream.com triggers）
- 新加 source 默认 **dependent**：父 workflow 暂停/删除会连带暂停/删除 source，重新启用会恢复；同一 source 加进第二个 workflow 后变 **independent**。当前无任何 UI 指示区分。
- 判据：**source 是独立资源，别让它默默绑定一个 workflow 生命周期**——多 workflow 复用同一个 source 才变 independent。
- **提升层**：工作流。

### B2：Pipedream $.respond() + 5TB 大文件 + email +data 元数据 + 多 trigger（来源：docs.pipedream.com triggers）
- 自定义 HTTP 响应用 `$.respond({status, headers, body})`（body 可为 string/object/Buffer/Readable）；multipart 上传文件内容不计入 payload 限额、最大 5TB；email 地址支持 `+data` 后缀注入元数据做条件分支；一个 workflow 可加多个 trigger。
- 判据：**触发器入口多样化是 Pipedream 的第一设计原则**——同一 workflow 多入口 + 响应自定义。
- **提升层**：工作流。

### B3：deepseek-plugin 按场景选插件 + dsh-context 上下文可视化 + dsh-at-file 存在性引用（来源：deepseek-plugin.org/collections）
- Collections 按真实问题给组合（Starter workspace 4 件套：dsh-web-ui/better-sidebar/dsh-market/modlens）；dsh-context 面板展示上下文窗口构成、历史 token 趋势、压缩与裁剪事件——让模型用量可视化；dsh-at-file 注入 `@` 文件时**只给存在性引用不读文件**，省上下文。
- 判据：**"装什么插件"已按场景打包成 collection**；上下文可视化是省 token 的前提。
- **提升层**：工具/上下文管理。

### B4：HF 模型趋势信号——MiniCPM5-2B / timesfm-3.0 / GLM-5.3 FP8（来源：huggingface.co/models）
- 305.36 万模型；Trending：MiniCPM5-2B 2.88k★、google/timesfm-3.0-pytorch 时序预测 0.3B、GLM-5.3-CYBERSECURITY-FP8 753B、LTX-2.5 视频 1.64M 下载、Qwen3.8-27B 6.71M。
- 判据：**小模型（2B）+ 垂直任务（时序/视频）+ 大模型量化（FP8）并行霸榜**。
- **提升层**：生态观察。

### B5：独立 skill 排行榜与话题趋势——skillleaderboard / repositorystats（来源：GitHub 生态走搜索）
- skillleaderboard.com 追踪 36.4k skills、529k stars/30 天、8M SKILL.md 行；obra/superpowers 居首；repositorystats topics：ai-agents 2095 / claude-code 1236 / agent-skills 874 仓库；Understand-Anything：多 agent 管线把任意代码库转交互知识图谱 +5.6k/天。
- 判据：**skill 生态已可独立度量（星速/行数/话题）**——装 skill 前查排行榜与来源话题热度。
- **提升层**：生态观察。

## 判重说明
- B1/B2 → r196-A 已记 sources vs actions 职责分界；取 dependent/independent 状态 + $.respond/多 trigger 增量。
- B3 → r196-C 已记 deepseek-plugin 12,733 插件复核；collections 首次真拉，dsh-context/dsh-at-file 全新。
- B4 → r194-B 已记 GGUF 反超/大模型周榜；取 MiniCPM5/timesfm/FP8 增量。
- B5 → r196-A 已记 trending 替代源；skillleaderboard/repositorystats 全新站点信号。
