---
name: system/harness-decision-reuse
description: |
  已定决策复用（decision reuse）：把已经结算的动作、参数与结论固化成决策图，后续同类步骤直接复现，不再重复推理。
  触发：token 消耗太高 / 同一份资料反复读 / 同一结论反复核 / 长任务压成本 / harness 瘦身 / 决策复用 / 少调用省 token。
  （来源：HarnessMM, arXiv:2610.32813，清华 + 微软亚研，2026-10-23 提交；视频号 GeekTechs 2026-11-06 转述。技能正文按论文写，不按口播写。）
version: 1.1.0
module: OI
modules: OI
---

# system/harness-decision-reuse

## 一句话

省 token 的正解不是「少干活」，而是**同一决策只推理一次**：把已结算的动作与参数固化成可复用图，后续走复现；只有出现新语义才回原推理。

## 论文实测（照抄数字，不放大）

- DeepSeek Harness / HumanEval 98 题：成功率 71.43% → **85.71%**；Tokens/task 96.28k → **11.62k（−87.93%）**
- Codex 基线保持 **90.82%**，66.72k → 47.02k（−29.54%）——**同一方法在不同 harness 上收益差极大，省多少取决于基线里重复推理的密度**
- MBPP 消融：比 single-use graphs 低 **26.91%**，比 retained callbacks 低 **19.52%**

## 机制拆成可执行五件套

1. **Executable Decision Graph**：节点存四样——精确动作、字面参数、因果依赖、公开守卫（guard）。守卫必须能被别人复核，不许写「上次就是这样」。
2. **Guarded Decision Reuse**：从上次执行留下的 receipt（证据）激活，不重新推理。
3. **Certified Callback Substitution**：走原生接口执行，并记录「移除了哪个慢回调」，可审计。
4. **RSI + validation**：用训练反馈迭代配置，部署版本由 validation 选，不许自评自选。
5. **回退三条件**：新语义决策 / 证据不足 / selector 弃权 → 回原 actor。硬套缓存是主要失败模式。

## 落到本机工作流

- 同一事实**第二次核验必须给理由**（文件已变更、结论冲突、时效过期），否则直接引用首次结论并写明出处。
- 反复出现的检索路径、账套口径、字段名、项目根目录，写成可复用清单——这就是决策图。
- 压成本时先量「整任务成功率 + tokens/task」，两个数一起报；只报省 token、不报正确率的优化一律不采纳。
- 决策图随代码/配置版本化：接口或参数一变，受影响的节点整片作废，不逐条打补丁。

## 风险

- 复用陈旧决策 = 错误按图传播；守卫里必须写清「什么情况下不得复用」。
- 小型任务图化收益低、维护成本高；只在同类步骤 ≥3 次出现时才固化。

## 决策图复用的正确性前提：封闭性（hermeticity）与内容寻址缓存键（r773A 实拉）

> 来源（≥2 独立域一手）：`bazel.build/basics/hermeticity`（Bazel 官方文档，WebFetch 200 全文）；`bazel.virtuslab.com/book/2~3~1`（Bazel Knowledge Hub 独立一手，逐字 "Hermeticity breaks into two pieces: isolation from the host machine and stable identity of the inputs themselves"）；`hermetiq.com/blog/what-is-hermeticity`（独立一手，cache correctness 论证逐字）；`reproducible-builds.org`（可复现构建官方站）。与 §机制五件套的分工：那节讲「图里存什么、怎么复用」，本节讲「复用命中凭什么是对的」——缓存正确性，不是缓存机制。

- **r773A-1 ★缓存键必须覆盖全部真实输入，否则命中是「猜」不是「证」**：Bazel Knowledge Hub 逐字「If something outside that recorded set can influence the output, Bazel is no longer reusing a proven result when it hits the cache. **It is reusing a guess.**」；「**A cache miss costs time. A false cache hit spreads a bad result.**」——隐藏输入比普通 miss 危险，错误缓存条目进共享远端后所有开发者一起复用。Bazel 官方两要素逐字 **Isolation**（"treat tools as source code"，不依赖宿主装了什么版本）+ **Source identity**（"use this hash to identify changes to the build's input"）。⇒ 落到决策图：节点的 key 不是动作名，而是**全部真实输入的哈希**——动作 + 字面参数 + 工具/技能版本 + 环境配置 + 引用文件内容；任何一项未纳入 = 该项变化时仍命中旧决策 = 错误按图传播。守卫只写「什么情况不得复用」还不够，必须写「什么变了就必须换 key」。
- **r773A-2 ★封闭性是频谱不是布尔，partial  adoption 付出成本却拿不到保证**：Bazel 官方列非封闭来源逐字「Actions or tooling that create files non-deterministically, usually involving **build IDs or timestamps**」「System binaries that differ across hosts」「Writing to the source tree during the build」；独立一手逐字「**Half a hermetic build gives you the cost without the guarantee.**」「Every cache miss you can't explain is a hermeticity violation waiting to be found.」⇒ 决策图里三类隐蔽输入对应：① 输出含时间戳/随机数 → 结果不可复现，禁止作为可复用节点；② 依赖「本机恰好装了某工具/某路径」→ 换机即错，须显式声明工具版本为 key 一部分；③ 复用过程改写了源数据 → 同一输入第二次走图结果不同。判据：无法解释的 miss 视为封闭性违例信号，先查隐藏输入而非直接重算。
- **r773A-3 ★验证动作是「零次空重建 + 跨机 hash 比对 + 逐 action 沙箱」**：Bazel 官方排障逐字「Ensure null sequential builds: If you run `make` and get a successful build, running the build again **should not rebuild any targets**. If you run each build step twice or on different systems, compare a hash of the file contents and get results that differ, **the build is not reproducible**.」「Execute a build within a docker container that contains nothing but the checked-out source tree and explicit list of host tools」「Enable strict **sandboxing** at the per-action level, since actions in a build can be stateful」。⇒ 决策图三检验：① 同一 spec 连跑两次，第二次应零重推理（只走复用）；② 两台机器/两个会话跑同一决策，比对输出 hash，不同即非封闭；③ 每个复用节点在沙箱内执行，禁止读未声明文件——读不到即暴露隐藏依赖。与 §风险「陈旧决策按图传播」互补：那条讲 guard 失效，本条讲 key 不完备与封闭性违例。
- **归属与判非**：`hermetic` / `cache key` / `内容寻址` / `content-address` 在 OI 各技能 SKILL.md 本体 0 命中（机检 4 目标技能）；与 `execution-intelligence` §r715A「机检天花板 / 变更参数重判」异命题（那条管断言可机检性，本条管缓存命中的正确性前提）；豆包自留地 `wb-execute-discipline` / `wb-context-compressor` WB 0 落地。加厚现有 1 技能，0 新建 / 0 合并 / 0 删除。

### 本轮来源（2026-11-19 r773A 实拉）
- `https://bazel.build/basics/hermeticity`（Bazel 官方文档，WebFetch 200 全文逐字；isolation + source identity 两要素、非封闭来源清单、null sequential builds 排障、逐 action sandboxing）
- `https://bazel.virtuslab.com/book/2~3~1`（Bazel Knowledge Hub，独立一手；"reusing a guess" / "A false cache hit spreads a bad result" / hidden inputs broader than source files）
- `https://www.hermetiq.com/blog/what-is-hermeticity`（独立一手；cache/parallelism/reproducibility 均建立在封闭性之上、"half a hermetic build" 成本论）
- `https://reproducible-builds.org/`（可复现构建官方站；确定性 → 环境记录 → 可重建校验三步）
