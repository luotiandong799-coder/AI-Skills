# AI技能仓库

WorkBuddy 自定义技能 + 记忆 + 身份配置，版本管理并同步到 GitHub。豆包与 WorkBuddy 共用 `memory/co-learn/` 一起学习。

> 技能按职能分目录（2026-09-18 整理）。每个技能在 `类别/技能名/SKILL.md`。
> 本地实时目录 `D:\腾讯AI\skills`（junction → `C:\Users\26719\.workbuddy\skills`）保持平铺；本仓库为分类归档。
> `AGENTS.md` 留根目录（全局规则入口）。

## 分类目录

| 类别 | 说明 | 技能 |
| --- | --- | --- |
| `engineering/` | 工程方法（调试/规格/验证/发布/技能工程/QA/教学） | wb-artifact-verification · wb-debug-loop · wb-execute-discipline · wb-release-maintain · wb-skill-authoring · wb-spec-driven · wb-ui-visual-qa · wb-teaching |
| `defaults/` | 三件套（每会话默认长期开启） | wb-ponytail · wb-max-token-saver · wb-context-compressor |
| `writing/` | 写作/文档/润色/简历/知识蒸馏 | wb-doc-writing · humanizer-zh · resume-ai-help · cangjie-skill |
| `media/` | 图像/音视频/生图/取证 | wb-visual-gen · image-processor · rg-ffmpeg-tools · wb-media-forensics |
| `research/` | 调研/搜索/抓取 | agent-reach · user-centric-research · web-scrape |
| `agent/` | 跨 agent 协作/拷问/提示词库 | agent-guild · grill-me · prompt-library-40 |
| `system/` | 系统/文件/GitHub/浏览器自动化 | windows-migrate-to-d-via-junction · edge-pwa-shortcut · local-file-dedup · github · github-ssh-over-443 · browser-automation |
| `meta/` | 仓库元信息（SkillHub 迁移记录、plugins） | _bm_skillid_migration.json · plugins/ |

## 共同学习区
- `memory/co-learn/` —— 豆包 + WorkBuddy 共享学习地址，详见 [`memory/co-learn/README.md`](memory/co-learn/README.md)。
- `memory/` —— 学习记录与共同学习区；`AGENTS.md` —— 全局规则。

## 同步约定
- push：SSH over 443（`~/.ssh/config` 已配 `github.com → ssh.github.com:443`），一次推送，不重试、不启 VPN、禁止强推。
- 同步时按上表把 `技能名/SKILL.md` 落到对应 `类别/技能名/SKILL.md`，**禁止在仓库根平铺技能**。
