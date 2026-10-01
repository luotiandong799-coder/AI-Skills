# 本仓长期笔记（curated · 持续精炼）

## MEMORY / 指针管理原则（2026-10-01 用户指令）
- **做指针做指针，分类指针**：维护 MEMORY.md / rules 时，凡可引用文件处一律用指针（指向真身文件/规则），不内联重复内容；同类指针归到同一分类小节下。
- 指针形态统一用真身路径 `D:\腾讯AI\skills\...`（唯一物理真身，rules/06），与 MEMORY.md 现有技能指针保持一致；junction 形式 `C:\Users\26719\.workbuddy\skills\...` 须含完整 `system/` 等类别段，否则断链。
- 背景：2026-10-01 巡检发现 rules/05 微信技能指针漏 `system/` 段（断链），已修正为 `D:\腾讯AI\skills\system\wechat-desktop-claw-automatic-control__skillhub\SKILL.md`。巡检报告曾误标为 MEMORY.md 第44行（实为 win-native-app-automation，正常），已纠错。

## MEMORY.md 指针化硬纪律（2026-10-01 20:17 用户强制）
- MEMORY.md 条目**默认做成指针**（指向真身文件/规则/SKILL.md），**不要大段内联文字**——否则易爆 4000 字符上限。
- 微信（VX）等条目也改为指针式（见 MEMORY.md 应用运行规则节）。
- 对所有会话/自动化生效；新增 MEMORY 内容先判断能否指针化，能则不做内联。
- 2026-10-01 20:23 已清理：5 处大段内联改指针（环境/系统、收尾、联网入口层、路径、AGENTS同步），MEMORY.md 3472 字符，余量 528。
