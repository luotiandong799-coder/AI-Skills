# 2026-09-27 · 系统文档落地：AI 输入入口增强系统（WeChatBridge 融合终版）

> 写入方：WorkBuddy｜类型：用户授权系统文档落地（非信源学习轮）

## 落点
- 文件：`meta/ai-input-enhancement-system.md`（编排/元层原则文档，**非新 skill**）
- commit：`7e033b5`（前序重建草稿 `3f49760` 已作废替换）

## 落地三纪律（用户 16:13–16:14 指定）
1. **合理存用**：与现有 skill 重叠 >60% 处一律交叉引用，不重复建。
   - 图片输入 → `media/image-processor`·`wb-media-forensics`
   - 文件输入 → `wb-doc-file-intel`·腾讯文档系
   - 流程 → `wb-spec-driven` / 执行 → `wb-execute-discipline` / 验证 → `wb-artifact-verification`
   - 价值判断 → `wb-context-compressor` / 任务提取 → `to-tickets`
   - 路由 Fallback → `wb-spec-driven` 1.100 / 跨 agent → `agent-guild`
   - 隐私 → `wb-artifact-verification` 护栏 + `rules/06` / 记忆 → `rules/07`
   - 学习调度 → 自动化 `070cce0c` / 总入口 → `00_总目录`
2. **不盲目复制**：整篇作为元文档，不新建重复 skill（与文档自定原则一一致）。
3. **删无用话语**：删冗余重复表述，保留 12 章结构与实质规则、示例。

## 关键决策
- 原文在 2026-09-27 对话压缩时丢失，用户重贴真内容（16:42）后落地。
- 先建过一版「重建草稿」（`3f49760`），收到真内容后整体替换为清理版（`7e033b5`，+118/-65）。
- 根目录禁平铺技能（见 `00_总目录` §3），故落 `meta/` 而非根目录或 `defaults/`。
