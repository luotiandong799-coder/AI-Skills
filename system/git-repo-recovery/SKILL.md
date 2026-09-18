---
name: git-repo-recovery
description: >-
  本地 .git 损坏时的取证与恢复。当出现 `fatal: not a git repository`（明明 .git 目录还在）、`git fsck` 刷屏 `failed to load pack entry` / `unable to read`、`.git/refs` 或 `packed-refs` 消失、`objects/pack/*.pack` 不见只剩 .idx、git 命令全部报 unknown revision / ambiguous argument、仓库突然"不被识别"时使用。流程：只读取证（reflog 是最重要的幸存线索）→ 分清「refs 丢失可原地重建」还是「pack 损毁只能从远端重取」→ 保留工作树、只换 .git → 三查验收（fsck_rc=0 + HEAD==远端 sha + status 干净）。也适用于：**把敏感/私人文件从 git 历史里彻底清除**（`git filter-repo` 抹路径 + `--force-with-lease` 推送 + 发现「force push 后 GitHub 仍保留不可达对象，旧 SHA 照样匿名可读」这条反直觉事实）、全历史密钥审计（判定到底哪些算敏感）、多副本（live + 镜像）一致性核对、恢复后 status 一堆 M 的真假甄别（stat 假脏 vs 真改动）、autocrlf 造成的 CRLF 漂移排查。触发词：.git 损坏、仓库坏了、not a git repository、failed to load pack entry、pack 丢失、refs 丢失、git 仓库打不开、fsck 报错、reflog 取证、从远端恢复仓库、git 仓库修复、corrupt git repo、recover git repository、objects 损坏、**历史重写、抹除历史、隐私问题、force push、force-with-lease、filter-repo、删掉历史里的文件、旧提交还能读到、仓库重命名、删库重建、密钥审计、敏感内容扫描**。不适用：GitHub 连不上 / push 超时（走 github-ssh-over-443）、只是合并冲突或撤销提交（走 git 常规操作）。
version: 1.2.0
agent_created: true
---

# git-repo-recovery（本地 .git 损坏的取证与恢复）

来源：2026-09-18 实测事故（`D:\腾讯AI\skills` 仓库，Windows + Git 2.55）。当时 `.git/refs/`、`packed-refs`、`objects/pack/*.pack` 全部消失，松散对象只剩 6 个，所有 git 命令报 `not a git repository`。**工作树文件一个没丢**，按下面流程 15 分钟内无损恢复。

## 症状识别
- `fatal: not a git repository (or any of the parent directories)`
- `git fsck` 刷屏 `error: failed to load pack entry` / `unable to read`
- `git log` / `git rev-parse` 报 `ambiguous argument ... unknown revision`
- 明明 `ls .git` 看得到目录，git 就是不认

## 第一步：只读取证（别动任何东西）
```bash
ls -la .git/                                  # 结构还在吗
cat .git/HEAD
ls .git/refs/ .git/refs/heads/ 2>&1           # refs 在不在
cat .git/packed-refs 2>&1
ls -la .git/objects/pack/                     # ★ 关键：.pack 是否还在
find .git/objects -type f -not -path "*/pack/*" | wc -l   # 松散对象数
tail -n 20 .git/logs/HEAD                     # ★ reflog 常幸存 → 时间线 + 最后状态
cat .git/FETCH_HEAD 2>&1                      # 上次 fetch 若成功，这里有效
git fsck --no-progress 2>&1 | tail -5         # 报错本身就是证据
```

判读：

| 现象 | 含义 | 处置 |
|---|---|---|
| `refs/` 或 `packed-refs` 没了，`objects` 完好 | 只是引用丢失 | 可原地重建 refs 指向 reflog 里的 sha，成本最低 |
| `objects/pack/*.pack` 没了（只剩 `.idx`） | 对象库损毁，本地历史不可恢复 | 走"从远端重取" |
| `FETCH_HEAD` 有效 | 上次 fetch 成功，远端可达 | 直接用它对比 sha |

**reflog（`.git/logs/HEAD`）是最重要的幸存线索**：它记录每次 HEAD 移动的时间、old/new sha、动作（commit/reset/…），既能定位损坏时间窗，也能在 refs 全丢时提供 sha 让 git 恢复对象。

## 第二步：先问远端，别急着重装
```bash
gh api repos/<o>/<r> --jq '{visibility,pushed_at,size}'
gh api repos/<o>/<r>/commits/main --jq '{sha:.sha,date:.commit.committer.date}'
curl -s -o /dev/null -w "%{http_code}\n" "https://api.github.com/repos/<o>/<r>/contents/<已知文件>"
```
远端 200 = 远端健康 → 本地恢复的验收基准就是它的 sha。

## 第三步：恢复（保留工作树，只换 .git）
工作树里的源码通常没坏，坏的是 `.git`。**不要删工作树重 clone**——那会丢未提交改动和临时产物。

```bash
mv .git .git.broken-<日期>            # 1. 残骸留证，别 rm（reflog 还要看）
git clone <remote> /tmp/reclone       # 2. 全新 clone 到临时目录
mv /tmp/reclone/.git .git             # 3. 只把 .git 装回来
git rev-parse --is-inside-work-tree   # 4. 校验
git rev-parse HEAD
git fsck --no-progress --no-dangling  # 期望 rc=0
git status --short
```

### 装回 `.git` 后的三个必查坑
1. **索引丢失 → 之前的 `git rm --cached` 全部失效**：那些"已取消跟踪"的文件会重新出现在 status 里成待删除项。用 `git add -A <paths>` 补齐暂存再提交。
2. **stat 假脏**：新 clone 的索引与旧工作树的 stat 缓存对不上，`git status` 会报一堆 `M`。`git diff --stat` 一跑就消失的 = 假脏，不是真改动。**真假甄别必须看 `git diff` 内容，不能只看 status**；`git add <paths>` 刷新缓存即可。
3. **`core.autocrlf=true` 会让 checkout 写出 CRLF**：`.gitattributes` 只锁 `*.md text eol=lf` 时，`.txt` 等类型会被写出 CRLF，与另一份 LF 副本 diff 不一致。检测**必须二进制读**：
   ```python
   open(f, "rb").read().count(b"\r\n")   # 正确
   # io.open(f, encoding='utf-8').read() 走 universal newlines，\r\n 被读成 \n，永远测不出
   ```
   要让副本逐字节一致：在该仓库 `git config core.autocrlf false` 后重新 checkout 相关文件。
   根治：`.gitattributes` 补 `*.txt text eol=lf`。

## 第四步：收尾与验收
三个信号齐了才算恢复完成：
- `git fsck --no-progress --no-dangling` → **rc=0**
- `git rev-parse HEAD` → **等于远端 sha**
- `git status --short` → **干净**（或只剩你预期的差异）

然后把残骸 `mv` 出工作树留档（不要留在仓库里）。记录"损坏时间窗 + 当时在跑什么"；**原因查不出就写"未定论"，不要编一个原因**。

### 多副本一致性核对（live + 镜像）
```bash
diff -rq <live>/ <mirror>/                    # 快速全局比对
# 逐文件核对（含中文名，别漏）
cd <live> && find . -type f | while read -r f; do
  diff -q "$f" "<mirror>/$f" >/dev/null 2>&1 || echo "DIFF: $f"
done
```
`diff` 报不一致时，**先用二进制确认是不是纯行尾差**，再决定改哪边——不要默认内容是坏的。

## 反模式
- 一报 `not a git repository` 就删 `.git` 重 clone → 丢掉 reflog（唯一取证线索）和所有未提交内容
- 看到大量 `M` 就 `reset --hard` → 可能把真改动一起冲掉；先 `git diff` 定性
- 在损坏的仓库里跑 `git gc` / `git repack` → 可能把残骸也清掉，**先取证**
- 把"refs 丢失"和"pack 丢失"当一回事 → 前者可原地救，后者只能从远端重取
- 只测一次就宣布"修好了" → 必须 fsck + HEAD 对比 + status 三查
- 恢复完就说"原因肯定是 X" → 无证据就写未定论

## 敏感内容：从历史里彻底清除（2026-09-18 实测）

### 先审计，别猜谁敏感
一次 `cat-file --batch-all-objects --batch` 流式扫全部 blob（**别用每个 blob 一个 subprocess，会被超时杀**；也别往 `--batch` 的 stdin 一次性灌全部 SHA，会因 stdout 满而**管道死锁**）。同时列出 `rev-list --objects --all` 的全部历史路径。
经验数据：1526 个 blob 里，8 处"像手机号"经上下文核对全是第三方文档的 E.164 样例，`key=` 赋值全是代码样例——**只看正则命中会误判，必须回到上下文**。

### 抹除与推送（必须按顺序）
```bash
git bundle create ../bk.bundle --all          # 1. 回滚网：bundle 含全部旧历史
git fetch origin main && git reset --hard FETCH_HEAD   # 2. 对齐最新 tip
git clone <repo> <tmp>/rewrite && cd <tmp>/rewrite     # 3. 全新 clone 里改写
python git-filter-repo --force --filename-callback '
  if filename == b"私密文件.md": return None
  if filename.startswith(b"private/") and not filename.startswith(b"private/public/"):
    return None
  return filename'
# 4. 校验 HEAD 树哈希与改写前完全一致（= 零附带损伤）→ 再推
git push --force-with-lease=refs/heads/main:<观察到的远端 sha> <remote> main
```
- **工具获取**：本机 `git filter-repo` 命令未必存在 → 取单文件脚本 `curl -H "Accept: application/vnd.github.raw" https://api.github.com/repos/newren/git-filter-repo/contents/git-filter-repo`（raw.githubusercontent.com 被墙时用 contents API），托管 python 直接跑。
- **必须用 `--force-with-lease`**：有他人也在推时，远端 tip 会变，普通 `--force` 会无声覆盖对方成果；带租约会自动拒绝。把"对齐 → clone → 改写 → 校验 → 推送"压在**一条命令里**执行，缩短竞态窗口。
- **⚠️ 但 lease 不等于安全（2026-09-18 亲测踩坑）**：`--force-with-lease` 只担保"远端 tip 等于你观察到的那个值"，**不担保你的分支包含它**。情形：你基于旧基线 A 提交了 C，期间别人推了 B；你观察到的远端是 B，于是 lease 通过，而你的推送会把 **B 整会从分支上抹掉**，且 git 只提示 `(forced update)`、不报错。
  - **硬校验**：推送前必须 `git merge-base --is-ancestor FETCH_HEAD HEAD`（为真才可推；否则先把 FETCH_HEAD merge/rebase 进来）。
  - **补救（亲测有效）**：正因为 GitHub 保留不可达对象，被抹掉的提交**还能救回** —— `git fetch origin <被覆盖的 sha>` 把它取回本地，再在**干净克隆**里 `git merge <sha>` 后用**非强制**推送即可完整恢复。若发现被抹掉，立刻先在 GitHub 上确认该 SHA 仍返回 200（`commits/<sha>`），再动手。
- **验收三查**：① 前后 `HEAD^{tree}` 完全一致；② `git log --all --full-history -- <被删路径>` 命中 **0**；③ fsck=0、技能/文件数一个不少。空提交会被自动剪枝，提交数变少属正常。

### ★反直觉：force push 之后，旧内容照样能读
GitHub **保留不可达对象**，只要知道确切旧 commit SHA 就还能匿名访问：
```bash
curl -s -o /dev/null -w '%{http_code}' \
  "https://api.github.com/repos/<o>/<r>/contents/AGENTS.md?ref=<旧sha>"   # 实测 → 200
```
即 **force push 不等于清除**，只等于"没有 ref 指向它、不易被发现"。彻底清除只有两条路：**删库重建**、或**改名置换**（新建干净仓库 → 推送 → 旧库改名 → 新库改成原名 → 删旧库）；等 GitHub 自动 GC 时间不可控。删除前务必确认 bundle/本地副本完好。

### 反向操作：layout 变了怎么办
多副本（live + 镜像）在历史重写后都要各自 `reset --hard FETCH_HEAD` 再 `checkout -f HEAD -- .`；**reset 不重写"归一化后内容一致"的文件**，有残留时先 `rm` 再 checkout（见上文坑 3）。

## 与相邻技能的分工
- **网络层**（连不上 / push 超时 / 被墙）→ `github-ssh-over-443`
- **本地 `.git` 损毁**（本技能）→ 取证 + 从远端重取 + 验收
- **修复是否真的生效**（补丁级验证）→ `wb-artifact-verification`
