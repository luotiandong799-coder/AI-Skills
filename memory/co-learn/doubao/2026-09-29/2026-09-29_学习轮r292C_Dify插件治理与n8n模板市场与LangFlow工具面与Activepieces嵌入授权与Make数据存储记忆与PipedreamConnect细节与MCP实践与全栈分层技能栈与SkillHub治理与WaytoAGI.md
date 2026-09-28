# r292C 学习轮（2026-09-29，十站实拉→十独点）

判重基线：r284~r292B 全表。查询词与既往全表错开（本轮=插件治理、模板市场、工具面、嵌入授权流、数据存储记忆、Connect 细节、MCP 实践、分层技能栈、SkillHub 治理、WaytoAGI）。

## 十站实拉 → 十独点
| # | 站 | 独点 | 判重 | 提升层 |
|---|---|---|---|---|
| 1 | Dify | 插件治理：marketplace 安全评级（Security Rating S/A+最后检查时间）/ 发布验证管线（作者验证防冒充+依赖扫描 pip+沙箱测试+API 校验+版本唯一性）/ 插件资源限制（max memory 128-256MB+访问域名声明）/ A2A 插件 | 合并保留增量（r292A 模型适配层/r292B 沙箱隔离，本点=插件治理+安全评级） | 工作流 |
| 2 | n8n | 模板市场内容面：文件转换模板 5 类（PDF 提取/DOCX→PDF/图片批缩放/音频转码/批量多格式）/ 数据管道 ETL 免外部服务（extract-transform-load+分页多源聚合）/ 免费模板发布 | 合并保留增量（r292A Webhook/r292B Agents，本点=模板+ETL 面） | 工作流 |
| 3 | LangFlow | 工具面：post-tool JSON 处理（大 JSON 响应动态生成 Python 代码提取相关数据减上下文）/ OpenAI Responses API 兼容端点（POST /api/v1/responses 换 model 名即用）/ LFX MCP create_flow_from_spec（一条请求建流）/ Agent 组件 Tools 端口（任何组件+MCP Tools） | 合并保留增量（r291C prompt 组件/r292B 扩展，本点=post-tool 处理+LFX MCP） | 工具 |
| 4 | Activepieces | 嵌入授权流：Embed Builder（iframe+SDK configure）/ Embeddable MCP 完整 OAuth 流（authRequestId→Authorize 弹窗→code→token→跑 flows）/ Data Tables 内置存储 | 合并保留增量（r292A Embeddable 概念，本点=完整授权流+Embed Builder） | 工具 |
| 5 | Make | 数据存储记忆：data store 模块做外部记忆（读→AI 模块→写 store 闭环）/ 知识文件双通道（静态走 AI Agent app/频繁更新走 Knowledge app）/ AI Tools 9 个免 prompt 模块 | 合并保留增量（r292A 错误语义/r292B webhook 面，本点=数据存储记忆+知识文件） | 工作流 |
| 6 | Pipedream | Connect 细节：external_user_id 关联模型（250 字符上限）/ Connect Link 托管零构建 / managed auth（托管 OAuth+自动刷新+加密 per project）/ BYO OAuth clients | 合并保留增量（r291B Connect/r292B 组件契约，本点=external_user_id+Connect Link） | 工具 |
| 7 | MCP | 实践面：Tool Search（2026 默认，仅工具名+服务器指令先加载，完整 schema 按需加载降 token）/ .mcp.json 团队提交（${VAR} 防 secret 进 Git）/ 远程 MCP（claude mcp add --url）/ Form/URL auth 模式（credential 不经 MCP 客户端） | 合并保留增量（r289B/r291B MCP 治理，本点=Tool Search+团队化+auth 模式） | 可复用 Skill |
| 8 | Full Stack | 分层技能栈：agenticskills.io 分层装配（前端/数据库/认证/部署按层 npx skills add）/ 技术栈自动检测（从文件/配置/目录检测加载框架技能）/ 角色推荐组合（初创 vs 大型项目） | 合并保留增量（r292A skills.sh，本点=分层装配+栈检测） | 可复用 Skill |
| 9 | 腾讯 SkillHub | 治理面：TRACE 严选评测框架（2026-05-21 腾讯+玄武实验室，五维度）/ SkillPay 支付体系（技能分发+Agent 调用+支付同链路）/ 实名发布（人脸核身）/ 规模（7.8 万→10 万+，2 个月 3000 万下载）/ 腾讯产品 Skill 化 | 合并保留增量（r290A SkillHub 数据面，本点=TRACE+SkillPay 重大增量） | 可复用 Skill |
| 10 | WaytoAGI | 蓝皮书五篇二十章结构+布鲁姆六阶学习法（记忆→理解→应用→分析→评价→创造）/ 900 万学习者知识库 | 合并保留增量（r291C 蓝皮书路径，本点=布鲁姆六阶+平台规模） | 可复用 Skill |

判重口径：增量判定。本轮 10 合并保留增量（每点均含≥40% 独有增量），零纯重复、零新面。