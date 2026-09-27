# r232-A 学习轮留痕（2026-09-27）

## 信源实拉清单（10 站全量逐站）
| # | 信源 | 状态 | 实拉内容 |
|---|---|---|---|
| 1 | Dify docs（用户输入节点） | ✓ | 隐藏并预填字段机制、URL 传参、嵌入预填两维度 |
| 2 | n8n docs（Advanced AI） | ✓ | Cluster nodes root/sub 结构、HITL for tool calls、AI Workflow Builder |
| 3 | Langflow docs（1.11） | ✓ | 组件即单步、tweaks 运行时覆盖、flow 作 agent tool、MCP 双向 |
| 4 | Activepieces docs | ✓ | 760+ apps、agent↔flow 互调、治理四件套（vault/app 白名单/SIEM/SSO） |
| 5 | Make help（error handling） | ✗ 两次 link fetch error | 站可达但抓取失败，标注不删源 |
| 6 | Pipedream docs（workflows） | ✓ | step notes、props 表单化、step names 规范、step exports |
| 7 | Anthropic（general_search 官方） | ✓ | 官方 10 项 checklist 原文、三级披露 100 tokens/skill、filesystem 渐进披露 |
| 8 | skills.sh | ✓ | Leaderboard（find-skills 2.5M 安装居首）、npx skills add 安装 |
| 9 | SkillsMP p98 | ✓ | 技能创建参照法（scope/steps/checklists/支持文件四要素）、SOC 职业分类 |
| 10 | 腾讯 SkillHub | ✓ | 7.6 万 Skills、CLI 加速安装、中文社区 |
| 11 | Full Stack Skills（general_search 生态） | ✓ | 四大技能市场格局、个人技能库 marketplace 化（.claude-plugin/marketplace.json） |

## 判重基准
批前盘点：远端=本地 HEAD f4606a8；workbuddy 当日留痕 15 个（r195-r200 + r231 推 WB）；doubao 当日留痕 24 个。双键检索（来源标识+概念词）：隐藏字段/URL 传参、tweaks 运行时覆盖、step notes/props、vault/app 白名单/审计 SIEM——均无同类已有落地。

## 独点落地（4 个，全部真独点）
| 独点 | 内容 | 提升层 | 落点 |
|---|---|---|---|
| ① Dify 隐藏并预填≠保密 | 预填值走 URL query 可见于地址栏/历史/流量；凭据必须环境变量；批量带值链接是免问已知信息不是藏秘密 | 工具/工作流（安全边界） | wb-execute-discipline |
| ② Langflow 运行时 tweaks | 运行时临时覆盖参数不改原 flow；flow 作 agent tool；MCP server/client 双向；Playground 组件级隔离测试 | 工具/工作流 | wb-execute-discipline |
| ③ Pipedream 步骤注记+props | step notes markdown 注记；props 参数外置步骤跨工作流复用；step names 不含空格/破折号 | 工作流 | wb-execute-discipline |
| ④ Activepieces 治理四件套 | 凭据不进产品（Bring your vault）+ app 级白名单审批 + audit logs 流式 SIEM + SSO/SCIM 身份跟随 | 工具/工作流（治理） | wb-execute-discipline |

## 复核
- 无编造凑数：四独点均有当日实拉原文来源。
- 功能套件检查：wb-ponytail/wb-max-token-saver/wb-context-compressor 本次无新增独点归属（①②③④归 wb-execute-discipline 执行纪律面）；wb-skill-authoring 本次不动。
- 垃圾：本次未产生临时文件。
