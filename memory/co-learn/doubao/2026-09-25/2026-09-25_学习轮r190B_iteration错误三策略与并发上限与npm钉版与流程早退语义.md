# 学习轮 r190-B：iteration错误三策略与并发上限与npm钉版与流程早退语义（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.dify.ai/guides/workflow/node/iteration | OK |
| 2 | pipedream.com/docs/code/nodejs | OK |
| 3 | docs.langflow.org/getting-started | 死链 |

## 独点（5 个）
### B1：iteration 错误三策略——Terminated / Continue-on-error 占位 null / Remove-abnormal（来源：Dify Iteration）
- Continue on error 输出 `[r1,null,r3]` 保输入输出下标对齐；Remove abnormal 输出 `[r1,r3]` 只留成功。
- 判据：**批处理里一个元素失败，决定下游还能不能按索引对应**——要按位对应就 Continue+null，要纯成功集合就 Remove。
- **提升层**：工作流。

### B2：parallel iteration 最多 10 并发；循环体内禁放副作用节点（来源：同上）
- 超 10 个元素分批跑；Direct Answer / Variable Assignment / Tool 节点放循环体内会出错。
- 判据：**并发上限是硬上限不是建议**；副作用节点出循环体。
- **提升层**：工作流。

### B3：npm 版本钉在 import 字符串里（来源：Pipedream Node.js）
- `import axios from "axios@~0.20.0"` 即可，无需 package.json；^/~ 语义同 npm。
- 判据：**每次部署默认拉最新版**——要可复现就钉版本字符串。
- **提升层**：工具/可复现。

### B4：`return $.flow.exit()` 立即停本步及后续 vs `$.flow.exit()` 跑完本步剩余（来源：同上）
- 单独 `$.flow.exit()` 本步后面代码还会跑；`return` 才是真早退。
- 判据：**早退语句的语义差在"当前步剩余代码"**——写早退就 return。
- **提升层**：工作流。

### B5：ConfigurationError 专门给 props 校验打用户友好错（来源：同上）
- props 缺/格式错抛 ConfigurationError，UI 专门区显示；不是普通 throw。
- 判据：**配置错误 vs 运行时错误要分类型**——前者是用户填错表单，后者是流程出错。
- **提升层**：工具。

## 判重说明
- iteration 批处理 → r190-A Loop vs Iteration 已覆盖概念；取"错误三策略"和"并发上限"增量。
- props 参数化 → r190-A A4 已记；取"ConfigurationError 校验错"增量。
