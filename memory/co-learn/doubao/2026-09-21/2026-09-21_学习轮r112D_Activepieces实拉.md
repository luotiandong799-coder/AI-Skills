# 2026-09-21 学习轮 r112-D（第 4 轮 · 16 轮批 r112）

来源：activepieces.com 官网实拉（docs 接口参数失败未返回）。

## 独点：0 条

**实拉证据：**
1. Agent 自然语言端到端任务（自动拆步骤/选工具，连接 app + MCP server 全可调）；关键步骤人工审批 gate（触碰钱/客户/生产的步骤设闸，其余放行）。
2. 可靠性：Run 从最后 checkpoint 恢复，不从开头重跑。
3. Flow 构建：Chat 描述→AI 构建 flow；TypeScript 内联代码；断点/重试/子流程/错误处理/人工审批。
4. 企业级：Projects/SSO/RBAC/审计流/Secret Manager/air-gapped——按规则企业级不投入。
5. MCP server 把 flow 暴露给 Claude/Cursor；Tables 数据读写；Knowledge Base 供 agent 检索。
6. 判非重复：审批 gate → r111-B 工具级 HITL / r112-A Human Input 同源；checkpoint 恢复 → 平台可靠性细节，与 ed §重放幂等分工不冲突但非新方法论；Chat 构建 flow → Dify New Agent 同源；MCP 暴露 → r112-C 同源；企业级项 → 规则不投入。

## 版本
ed 2.96.0 未动。
