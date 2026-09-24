# 学习轮 r192-C：manual与production执行分账与执行数据脱敏与模型榜观察与404自愈（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | deeplearning.ai/learn | robots 禁 |
| 2 | docs.n8n.io/workflows/ + components/ + executions/ | OK |
| 3 | huggingface.co/models | OK（Trending 榜） |
| 4 | skills.sh/obra/superpowers/skill-creator | 404（renamed/removed 提示） |

## 独点（5 个）
### C1：manual vs production 执行分账——开发时 Inactive，manual 不占 quota（来源：n8n executions）
- 只有 trigger/schedule/polling 自动触发的 production 执行才计 quota；Manual 测试执行不计数。开发保持 Inactive。
- 判据：**调试跑活不该占生产额度**——把"测试执行"和"生产执行"分账，才敢放开跑测试。
- **提升层**：工作流/运维。

### C2：execution data redaction——隐藏 input/output 但保留 status/timing/node 元数据（来源：n8n）
- 敏感数据脱敏后仍可审计执行时长、节点名、成败，不丢排障线索。
- 判据：**脱敏不是清空日志**——业务数据藏住，运行元数据留下。
- **提升层**：安全/运维。

### C3：HF Trending 2026-09 观察——本地量化 GGUF 下载量反超官方、多模态 I2T2T 占榜、小模型 2-4B 回潮（来源：huggingface.co/models 实拉）
- unsloth/Qwen3.8-27B-GGUF 10.7M 下载 > 官方 Qwen/Qwen3.8-27B 6.71M；MiniCPM5-2B/Spark-X2.5-4B 等小模型占榜；I2T2T 多模态成主流。
- 判据：**个人用户选模型优先本地量化版**——不花 API 钱、隐私在本地；小模型够日常。
- **提升层**：模型选择。

### C4：两层 execution list——workflow-level 调试 vs all-executions 审计（来源：n8n）
- 单工作流执行列表排障，全工作流列表做全局审计。
- 判据：**排障视角和审计视角是两个查询**——别用全局列表找单 bug。
- **提升层**：运维。

### C5：skill 404 自愈——提示 renamed/removed + 推荐相近 skill（来源：skills.sh）
- 链接失效时不直接 404，而是给"Did you mean?"列表保留仓库内可用 skill。
- 判据：**生态目录要处理漂移**——skill 改名/删除是常态，目录要留重定向。
- **提升层**：可复用 Skill/生态。

## 判重说明
- execution 模式 → r190-B 已记 iteration 错误三策略；取"manual/production quota 分账"增量。
- redaction → wb-context-compressor 已有 PII 处理；取"保留元数据排障"增量。
