# 学习轮 r194-C：LangFlow FreezePath与Group打包与版本分叉与Pipedream step命名与props语言限制（2026-09-25）

## 实拉记录
| # | 站点 | 结果 |
|---|---|---|
| 1 | docs.langflow.org/components-overview | OK |
| 2 | activepieces.com/docs/activepieces/agents | 死链 |
| 3 | pipedream.com/docs/workflows/ | OK |

## 独点（5 个）
### C1：LangFlow Freeze Path——锁上一步输出防重跑（来源：docs.langflow.org）
- 组件跑过后可"Freeze Path"锁定输出，下游再跑不重算上游。
- 判据：**调试大 RAG 流时，向量检索/embedding 这种慢节点冻住，只改下游 prompt**。
- **提升层**：工作流/调试。

### C2：LangFlow Group 多组件打包成一个可复用组件（来源：docs.langflow.org）
- Shift 多选 → Group → 合并成单组件，可存 sidebar 复用（如 RAG+向量库打包）。
- 判据：**可视化编排也要有"子流程"概念**——不是把所有节点平铺。
- **提升层**：工作流。

### C3：LangFlow sidebar template vs workspace 实例分离——拖出来就分叉（来源：docs.langflow.org）
- sidebar 是 starter template；拖到画布后两者脱钩，组件版本号锁定在拖入时；点 Update 才升级。
- 判据：**模板升级不自动覆盖已实例化的流**——避免用户已改的流被静默升级冲掉。
- **提升层**：版本管理。

### C4：Pipedream step 名禁空格/连字符，必须下划线/camelCase（来源：pipedream.com/docs/workflows）
- `steps.get_data.myData` 引用；改名后要更新所有旧引用。
- 判据：**步骤名是代码标识符**——不是显示名。
- **提升层**：工作流。

### C5：Pipedream props 表单化输入仅 Node.js 支持（来源：pipedream.com/docs/workflows）
- Python/Bash/Go code step 不支持 builder 表单 props。
- 判据：**跨语言工作流引擎的"高级特性"往往只在主语言可用**——选语言时要看功能矩阵。
- **提升层**：工具。

## 判重说明
- C1/C2/C3 → r192 补抓 LangFlow 已记 component=单步/playground/tweaks；取 Freeze Path/Group/版本分叉增量。
- C4/C5 → r192 补抓 Pipedream 已记 Connect SDK；取 step 命名/props 语言限制增量。
