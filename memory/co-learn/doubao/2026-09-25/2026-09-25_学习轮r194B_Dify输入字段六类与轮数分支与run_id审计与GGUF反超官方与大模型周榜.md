# 学习轮 r194-B：Dify输入字段六类与轮数分支与run_id审计与GGUF反超官方与大模型周榜（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/workflow/node | OK Start 节点 |
| 2 | docs.n8n.io sub-workflow | 死链 |
| 3 | huggingface.co/models Trending | OK |

## 独点（5 个）
### B1：Dify Start 节点 6 种输入字段 + sys.dialogue_count 用轮数做分支（来源：docs.dify.ai Start）
- Text(256)/Paragraph/Select/Number/Single File/File List；Chatflow 系统变量 `sys.dialogue_count` 每轮自增，配 if-else 在第 N 轮做总结/审历史。
- 判据：**多轮对话的"第 N 轮动作"用轮数计数器触发，不用 LLM 判断"现在第几轮"**。
- **提升层**：工作流。

### B2：sys.workflow_run_id 全链路审计 ID（来源：docs.dify.ai Start）
- 每次 run 独立 workflow_run_id，可追踪整次执行的所有节点。
- 判据：**一次执行一个 run_id，日志/回放/审计都靠它**。
- **提升层**：可观测性。

### B3：unsloth Qwen3.8-27B-GGUF 10.7M 下载反超官方 FP 6.71M（来源：huggingface.co/models）
- 本地量化 GGUF 成主流；多个社区微调版（TURBO-Fable/Uncensored/Aggressive-MTP）日更。
- 判据：**官方权重打不过社区量化**——本地部署是刚需。
- **提升层**：模型/工具。

### B4：本周大模型周榜观察——GLM-5.3 753B / DeepSeek-V4-Flash-Vision 305B / Qwen3.8-Flash-Next 180B（来源：huggingface.co/models）
- zai-org GLM-5.3 753B、GLM-5.3-Flash 321B、dealignai GLM-5.3-CYBERSECURITY-FP8；deepseek-ai V4-Flash-Vision 305B；Qwen3.8-Flash-Next 180B / 120B NVFP4。
- 判据：**开源模型进入 700B+ 时代**；安全专用 FP8 出现。
- **提升层**：模型。

### B5：microsoft/VibeVoice-ASR-Streaming-7B 流式 ASR（来源：huggingface.co/models）
- 流式 ASR 7B，Breeze-TTS-2 3B TTS。
- 判据：**语音 in/out 正在小模型化**。
- **提升层**：模型/工具。

## 判重说明
- B1/B2 → r192 补抓 Dify 已记 scaffolding；取"6 输入字段 + dialogue_count 轮数分支"增量。
- B3 GGUF 反超 → r192-C 已记；取"社区微调日更"增量。
