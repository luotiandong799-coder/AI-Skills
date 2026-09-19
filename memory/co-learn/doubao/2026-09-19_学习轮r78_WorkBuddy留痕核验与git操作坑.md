# 2026-09-19 学习轮 r78（WorkBuddy 留痕学习）

来源：共享学习区 `co-learn/workbuddy/` 5 份留痕（用户指令「看看wb学到的 然后你学习」）。

## 学了什么（核验式学习）
1. **r100 GPT Store 方法论**（货架按用户意图分 8 类 / 爆款条目结构公式=场景名+双语价值主张+创建者分层+评分+对话量 / 描述模板=能力动词+输入方式+产出）→ **核验已在库**：sa L319「GPT Store 货架与爆款信任公式」。
2. **r99 工具安全标注契约**（readOnly/destructive/idempotent/openWorld 4 hint 声明层安全）→ **核验已在库**：wb-spec-driven L427「工具安全标注契约」。
3. **技能合并判据**（同一功能位+触发词互相覆盖才合并；市场/第三方技能只划边界不文件级合并；六步合并姿势；合并后不通报协作方=白做）→ **核验已在库**：sa L1219（WorkBuddy r113 已写入，内容完整）。
4. **结构变化知情**：browser-reuse 已并入 browser-automation 2.0.0（浏览器域唯一入口，不再新建浏览器桥接类技能）；distill-cat 已由 WorkBuddy 升 **1.1.0**（cangjie 边界声明）；web-scrape/agent-reach、github/github-ssh-over-443 边界声明。
5. **环境坑**：git rm -r 连删父目录其余文件（index/HEAD 完好，git restore 复原）。

## 本批真独点（并入 wb-execute-discipline 2.17.0 → 2.18.0）
- **git rm -r 删目录连坐父目录**：删完立刻 `ls 父目录` + `git status --short` 复核；异常 `git restore -- <父目录>/` 复原再查因（全库无此记录，git-repo-recovery 只覆盖索引丢失）。

## 判重说明
- WorkBuddy 其余方法论均已由其本人并入仓库，不重复落。
- CDP 抓取过程协议（junction 复用登录态）属浏览器域，已入 browser-automation，不入。

## 版本变更
- ed 2.17.0 → **2.18.0**（git rm 坑）
