# 2026-09-23 学习轮 r151-B（Letta 实拉 · WorkBuddy 吸收）

## 主源（独立首读）
Letta 官方 `docs.letta.com/llms.txt`（28/29 页 200）。注：convex llms.txt 是重定向桩（→www 404）、together 经代理 403，改用 letta。全量 165 路 fetchall：122 OK200。

## 吸收点（落地 cc 3.45.0 / pt 1.62.0 / sa 2.67.0）
1. **记忆外置为 git 仓库、按需引用不内联**：MemFS 投影到机器，system prompt 只列路径+顶层文件、按文件树读，不是铺进上下文。（cc）
2. **共享知识放一处、各 agent 引用不复制**：多 agent 共用→外置仓库引用，避免漂移与重复占用。（pt）
3. **跨 agent 共享记忆须显式同步协议**：挂仓库→列路径+文件→文件+git 编辑→commit/push→他人 fast-forward pull。（sa）

## 判非重复
cc 现有 §/doctor 审计（放置/重复/token）管"胖了怎么清"，本条管"更前置的存贮形态"；pt §能描述就别编程 管声明式，本条管知识复用层 YAGNI；sa §互操作兜底层 管能力不齐，本条管共享可变状态的同步协议。均增量 ≥50%。

## 版本化
随 r151 同 commit `024ae90` 推送，repo↔live 7/7 SAME。
