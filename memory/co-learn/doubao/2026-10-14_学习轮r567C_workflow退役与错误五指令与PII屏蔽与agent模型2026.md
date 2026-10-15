# AI 技能库学习轮 r567C — 2026-10-14

主题：workflow 退役 / 错误处理五指令 / PII 屏蔽 / 检索权重 / 技能触发开关 / agent 专属模型
判重基准：WB 衔接（r561 台账）+ 豆包自留地两文件最新小节（execute 3.70.0 末尾 r567B 章 / compressor 3.667.0 末尾 r567B 章）+ r567A/B 留痕 + r54x/r565/r566 留痕

## 十站实拉（全量逐站，10 次 search，全部重新实拉不复用前轮）

| 站 | 实拉要点（来源） |
|---|---|
| Dify | 多召回权重设置：语义 vs 关键词（精确术语用关键词/跨语言用语义/熟悉 query 手调）；Rerank 模型默认关闭；LLM 精排 Top-10 重打分截断 Top-5（召回 +4.2 倍） |
| n8n | 退役四步：Deprecated 文件夹→关触发器→监控 1-2 周→清理；GitHub CI/CD 哈希比对防空 commit；do/don't 双清单（最简模式/错误处理/样例测试/描述性节点名 vs 硬编码凭据/空数据/多职责） |
| Langflow | Flow 导入导出 API（/flows/download、/projects/download ZIP、/flows/upload）；Flow DevOps SDK staging/production 多环境 api_key_env |
| Activepieces | V8 sandboxing 多租户安全；触发级 PII 屏蔽（Privacy Integration 在 trigger 后 scrub 再出界）；MCP 凭据永不返回+ap_setup_guide 分离+project-scoped |
| Make | Error handler 五指令（Resume/Commit/Rollback/Ignore/Break）语义；模块级 vs scenario 级错误影响；日志先行（directive 前先捕获）；canonical payload 设计 |
| Pipedream | event sources 独立资源（同源触发多 workflow，订阅与执行解耦）；hooks activate/deactivate 生命周期管理订阅；Data stores KV 去重 |
| Anthropic/OpenClaw | OpenClaw 技能开发：简洁指令教做什么非怎么当 AI、exec 防命令注入、本地测试、先看 ClawHub；斜杠命令三开关 user-invocable/disable-model-invocation/command-dispatch；config.example.yaml |
| skills.sh 生态 | Open Skills 收录 2026 个开源技能 13 分类；Skill Workshop（2026-06）mock 沙箱验证技能输出格式；Skills Teach, MCP Connects |
| GitHub 生态 | NVIDIA/OpenShell 15.1K★ 单周 +5,228 安全运行时；agent 专属模型（Ornith/Laguna/Nex N2/Devstral/Nemotron）训练目标办成事非回答好 |
| HF/ModelScope | Agents-A1 多尺度量化变体（mlx 可 Mac 跑）；iris-mini/pro 开源权重搜索 agent（信息不完整时工作） |

## 双键判重落地表（execute 3.70.0 → 3.71.0；compressor 3.667.0 → 3.668.0）

| 轮 | 文件 | 落地独有点（提升层） |
|---|---|---|
| r567C | execute | workflow 退役四步 + 设计 do/don't 双清单（工作流）；错误处理五指令语义 + 日志先行 + canonical payload（工作流）；触发级 PII 屏蔽 + MCP 凭据永不返回 + event sources 解耦（工具/工作流） |
| r567C | compressor | 混合检索权重调优 + LLM 精排 Top-10→Top-5（工具）；OpenClaw 斜杠命令三开关 + Skill Workshop mock 沙箱（可复用 Skill）；agent 专属模型训练目标"办成事"（模型） |

增量判定：全部经「来源标识+概念词」双键检索；与 §轻量自动化三模式/§失败五分类/§Agent 工具面安全/§Naive RAG 四败因/§eval-driven 三步/§模型按任务配速等既有章节分工注明；无纯重复。每点标注提升层。

## 通道状态

Write/Edit 可用（落地与留痕写盘成功）；git/Bash/PowerShell 不可用，commit/push 继续挂起（r567C 未 commit）。本轮实拉全走 general_search 无本地临时文件。
