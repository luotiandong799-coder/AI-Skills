---
name: system/skills-security-check
description: "腾讯云鼎实验室出品，Skill安全审查工具。对用户指定的skill.md文件及其配套的文档、程序、脚本等进行全面安全审计，确保引用安全"
description_zh: "腾讯云鼎出品，Skill 安全审计工具"
description_en: "Scan a third-party skill for security risks before enabling it"
version: "1.27.0"
allowed-tools: Read, Grep, Glob, Bash
display_name: "system/skills-security-check"
display_name_en: "system/skills-security-check"
visibility: "public"
---
## 功能描述（全文见 references/knowledge-base.md §下沉·skills-security-check·功能描述）

## 约束（全文见 references/knowledge-base.md §下沉·skills-security-check·r439·约束）

## 🎯 审计核心原则：关注供应链投毒风险

**⚠️ 重要：审计的核心目标是防止skills本身成为攻击载体，而非评估教学代码质量！**

### 审计边界

**核心判断**：skill 会不会自动执行该操作？

- **skill 自动执行**（命令、脚本、安装）→ ✅ 是投毒风险，按步骤6的 Malicious/Suspicious 标准定级
- **仅作为示例**，需用户手动复制使用 → ❌ 不是投毒风险，不报告
- **教学代码质量问题**（SQL 注入示例、异常处理缺失、命名规范、算法效率、架构设计等）→ ❌ 开发者自行负责，不报告

**示例对比**：

| 情况                                        | 是否报告           | 理由                                                                                                                |
| ------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------- |
| skill.md中Python示例有SQL注入               | ❌**不报告** | 仅是教学代码，skill不自动执行                                                                                       |
| skill自动执行 `curl \| bash`               | ✅**需报告** | skill自动执行远程脚本，触发步骤4深度分析后根据远程内容定级（Malicious或Suspicious）                                 |
| 配套脚本 `init.sh`包含 `npm install -g typescript@5.0.0` | ❌**不报告** | skill自动执行全局安装但**版本已固定**，无投毒风险                                                                   |
| 配套脚本 `init.sh`包含 `npm install -g some-tool` | ✅**需报告** | skill自动执行全局安装**未固定版本**，可能拉取被投毒的最新版本 → Suspicious                                           |

## 执行逻辑

**## 约束：请严格按照流程执行所有步骤！**

**⚠️ 扫描说明**：

- 步骤2-5为关键词扫描，列出的关键词**仅作参考**，必须理解每类风险的本质特征，灵活识别变种和等价形式
- 先用基础关键词快速扫描，发现可疑点后深入搜索相关变种
- 扫描阶段只管**记录命中**，是否构成风险在步骤6统一判定

### 步骤1：读取目标skill文件

- 完整读取目标 **skill.md 文件**本身及其配套的**相关文档、脚本、程序**
- 记录文件路径和行号，便于后续定位问题

### 步骤2：搜索危险关键词（不仅限于以下示例）

在skill文件及相关目录中搜索以下关键词：

**命令执行类**（包括但不限于）：

- `curl`, `wget`, `bash`, `sh`, `zsh`
- `eval`, `exec(`, `system`, `subprocess`, `os.system`
- `shell_exec`, `popen`, `Runtime.exec`, `ProcessBuilder`
- 多语言变种：`os.popen()`, `Popen()`, `call()`, `check_output()`

**隐蔽执行类**（包括但不限于）：

- `silently`, `background`, `hidden`, `--quiet`, `-q`, `--silent`
- `2>/dev/null`, `>/dev/null`, `&>/dev/null`
- `nohup`, `disown`

**网络请求类**（包括但不限于）：

- `http://`, `https://`, `ftp://`
- `curl`, `wget`, `fetch`, `axios`, `requests.get`, `requests.post`, `urllib`
- `httpx`, `aiohttp`, `got`, `node-fetch`, `XMLHttpRequest`, `$.ajax`
- 提取所有 URL 和域名，识别 Base64 编码字符串（正则：`[A-Za-z0-9+/]{20,}={0,2}`）

**权限提升类**（包括但不限于）：

- `sudo`, `root`, `chmod`, `chown`, `requires_approval`

### 步骤3：检查文件操作与敏感路径（不仅限于以下示例）

**敏感路径**（包括但不限于）：

- 系统：`~/.ssh`, `~/.gnupg`, `/etc/passwd`, `/etc/shadow`, `/etc/hosts`
- 云凭证：`~/.aws`, `~/.gcloud`, `~/.azure`, `~/.kube`, `~/.docker`
- 环境变量：`.env`, `.env.local`, `.env.production`
- 密钥相关：`credentials`, `secrets`, `tokens`, `password`, `api_key`, `private_key`, `secret_key`
- Windows：`C:\Users`, `%APPDATA%`, `%USERPROFILE%`

**文件操作**（包括但不限于）：

- 读取：`cat`, `open(`, `readFile`, `fs.readFileSync`
- 写入：`write(`, `writeFile`, `fs.writeFileSync`
- 删除/移动：`rm`, `rm -rf`, `unlink`, `shutil.rmtree`, `mv`, `os.remove`

### 步骤4：远程脚本内容深度分析（Malicious 远程执行类必做）

**触发条件**：步骤2-3中发现 skill 自动下载并执行远程脚本（如 `curl | bash`、`wget | sh`、下载后执行等）时，**必须**用 `web_fetch` 抓取远程 URL 的文本内容进行静态分析（只读取，不执行）。

**执行流程**：

1. **抓取远程内容**：对每个被自动执行的远程 URL 调用 `web_fetch` 获取脚本文本

   - URL 无法访问（404/超时/拒绝）→ 标注"**无法验证内容安全性**"
   - 内容为二进制文件 → 标注"**无法静态分析**"
2. **深度分析脚本内容**，逐项检查以下行为并**结合上下文判断是否合理**：

   | 检查项                  | 关注的行为模式                                               | 判断标准（恶意 vs 合理）                                                                                                   |
   | ----------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
   | **二次下载+执行** | 脚本内部再次 `curl \| bash`、`wget` 下载并执行其他脚本    | 🔴 几乎总是恶意的（链式下载极难审计），除非来源为同一官方域名且有明确必要性                                                |
   | **数据外送**      | `curl -d`、`wget --post-data`、`nc` 等向外发送数据     | 需同时看**发送内容**和**目标地址**：敏感信息发送到未知第三方域名 → 🔴恶意；向官方域名发送非敏感数据 → ✅常见 |
   | **后门/持久化**   | 写入 crontab、添加 SSH authorized_keys、创建系统服务         | 视目的而定：官方工具创建自身更新任务 → ✅合理；写入未知 SSH key → 🔴恶意                                                 |
   | **系统破坏**      | `rm -rf /`、覆盖系统文件、修改 `/etc/hosts`              | 🔴 几乎总是恶意的                                                                                                          |
   | **权限提升**      | `sudo`、`chmod 777`、修改用户权限                        | 安装系统级工具需要 sudo → ✅合理；`sudo rm -rf /` → 🔴恶意                                                             |
   | **隐蔽操作**      | 大量 `>/dev/null 2>&1`、`nohup`、删除操作日志            | 隐蔽安装输出 → ✅常见；隐蔽向官方域名发非敏感数据 → ✅常见；隐蔽向第三方域名发数据 → 🔴可疑                             |
   | **环境篡改**      | 修改 `PATH`、写入 `.bashrc`/`.zshrc`、设置别名覆盖命令 | 将安装路径加入 PATH → ✅常见；别名覆盖 `ls`/`curl` → 🔴恶意                                                          |


   > **核心原则**：不以行为模式本身定性，而是分析行为的**目的、对象和上下文**来判断。
   >
3. **生成深度分析结论**，在报告中为每个远程 URL 输出：

   - **URL** / **可访问性** / **脚本行数**
   - **发现的风险行为**：具体列举，并标注每项行为经上下文分析后的判定（恶意/可疑/合理）
   - **脚本主要功能**：一句话总结
   - **深度分析结论**：综合判定该脚本当前内容的安全性

**深度分析与风险定级联动**：

| 深度分析结论                                        | 最终定级                    | 说明                             |
| --------------------------------------------------- | --------------------------- | -------------------------------- |
| 🔴 发现**确认恶意**的行为                     | **Malicious（恶意）**    | 远程脚本含实际恶意行为           |
| ⚠️ 远程脚本**无法访问**或**无法解析** | **Suspicious（可疑）** | 无法验证内容安全性，建议人工确认 |
| ⚠️ 存在**可疑但无法确认恶意**的行为         | **Suspicious（可疑）** | 建议人工复核                     |
| ✅ 所有行为均为**合理/常见操作**              | **Suspicious（可疑）** | 当前内容安全，降为 Suspicious    |

**降级时报告须注明**：✅ 当前内容经深度分析未发现恶意行为 → ⚠️ 但远程执行模式存在固有风险（内容可被替换/中间人篡改）→ 💡 建议固化到本地或增加 checksum 校验

### 步骤5：检查依赖安装风险（供应链安全）

#### 5.1 全局依赖安装检测（不仅限于以下示例）

搜索全局安装**且未固定版本**的模式，关键看：
1. **是否在隔离环境中**（虚拟环境/容器）
2. **是否固定版本**（如 `==2.28.1` / `@1.2.3`）

**判断标准**：
- ✅ **固定版本** + 全局安装 → 不报风险（如 `pip install requests==2.28.1`）
- ⚠️ **未固定版本** + 全局安装 → Suspicious（如 `pip install requests`、`npm install -g tool`）
- ✅ 虚拟环境中安装（即使未固定版本）→ 风险较低，不报风险

**检测模式**：
- **Python**：`pip install <包名>`（无 `==`/`>=`/`~=` 版本号）、`pip3 install`、`sudo pip install`
- **Node.js**：`npm install -g <包名>`（无 `@version`）、`yarn global add`、`pnpm add -g`
- **其他**：`gem install`、`cargo install`、`go install`、`brew install`

#### 5.2 依赖来源检测

检查是否从非官方源或不可信引用安装：

- `pip install -i <非官方镜像源>` / `--index-url <可疑URL>`（无法验证源安全性）
- `npm install --registry <非官方源>`
- 从代码仓库安装**且未固定 commit SHA**（如 `git+https://...@main` / `git+https://...@v1.0`）
  - ✅ **已固定 commit SHA** → 不报风险（如 `git+https://repo.git@a1b2c3d4e5f6`）
  - ⚠️ **分支/tag/未指定** → Suspicious（代码可被随时更新）

### 步骤6：风险评估和报告生成

**⚠️ 定级原则**：

- **不要机械匹配关键词**——单个关键词命中不构成风险，要判断多个操作组合在一起是否形成危险行为
- 关键看 skill **自动执行了什么操作组合**，而不是出现了什么关键词
- 例如：`subprocess` 在沙箱中执行和直接执行风险不同；`~/.ssh` 在教学说明中出现和被自动读取+发送是完全不同的事

**⚠️ 不构成 Malicious 的前置判断（优先于下方 Malicious 条目匹配，每个疑似 Malicious 必须按以下递进链逐步判断）**：

```
Step 0: 是否为作者自身凭证？（硬编码凭证排除规则，仅针对当前凭证项）
  发现硬编码凭证（API Key、Token、私钥、钱包密钥、数据库密码等）时，先判断：
  该凭证是否是 Skill 作者自身的凭证（而非窃取用户的凭证）？
  判断依据：凭证出现在作者编写的代码/配置/备份文件中，属于作者自己的账号、密钥、Token 等。
  → 是作者自身的凭证
    → 该凭证项归入「📝 信息性提醒（非风险项）」section，**禁止**放入 Malicious 或 Suspicious 区域
    → 如果 skill 利用该凭证执行了其他对用户有害的行为，这些行为作为**独立的发现项**继续走 Step A→B→C
    → 跳过该凭证项，继续检查其他发现项
  → 不是作者自身的凭证（如 skill 通过代码窃取用户凭证并外送）→ 继续 Step A

Step A: 是否自动执行？
  该操作是 skill 自动执行的（无需用户审批即可运行），
  还是仅定义/提供了能力（如提供命令执行接口、文件操作工具等，agent 使用时需经用户审批确认）？
  → 仅定义/提供能力 → 不构成 Malicious，最高 Suspicious。停止判断。
    （禁止通过"本质上等效""间接实现了相同效果"等类比推理将"提供能力"等同于"自动执行"）
  → 是自动执行 → 继续 Step B

Step B: 是否危险操作？
  该自动执行的操作是否属于危险操作（匹配下方 Malicious 条目中的任一项）？
  → 不属于危险操作（如 os.popen('date') 获取时间戳、subprocess(['git','status']) 只读操作等）
    → 不构成 Malicious，按 Suspicious/Benign 标准另行定级。停止判断。
  → 属于危险操作 → 继续 Step C

Step C: 是否包含恶意意图？
  该危险操作是否包含恶意意图？综合判断：
  - skill 的功能描述与实际行为是否一致？（不一致 → 有隐藏意图）
  - 是否存在隐藏的恶意代码？
  - 深度分析（如远程脚本内容）是否发现恶意行为？
  → 确认无恶意意图 → 匹配 Malicious 条目但必须走降级条件（→ Suspicious），不得以假设性风险维持 Malicious。⛔ 输出约束：降级为 Suspicious 的发现项必须放在「⚠️ Suspicious（可疑）风险发现」区域展示，**禁止**放在「🔴 Malicious（恶意）风险发现」区域
  → 发现恶意意图 → Malicious
  → 远程脚本不可访问或无法解析 → Suspicious（无法验证内容安全性，建议人工确认）
```

→ Malicious 仅适用于 skill **自动执行**包含**恶意意图**的**危险操作组合**的投毒场景。

根据检测结果分类风险等级：

**🔴 Malicious - 恶意（skill自动执行危险操作组合）**：

- ✅ **下载 + 执行**：skill自动从远程下载内容并执行（如 `curl | bash`、下载脚本后 `eval`）
  - ⚠️ **降级条件（→ Suspicious）**：①步骤4深度分析确认远程脚本当前内容无恶意行为；②远程脚本无法访问或无法解析（无法验证内容安全性，建议人工确认）。以上情况**必须**降为 **Suspicious**，需在报告中注明降级原因和远程执行的固有风险。已确认无恶意或无法访问 → 必须降级，不得以"供应链攻击面""将来可能被攻陷"等假设性风险维持 Malicious
  - 🔴 **维持 Malicious**：远程脚本包含恶意行为、或未执行深度分析
- ✅ **读取敏感信息 + 危险操作**：skill自动读取敏感文件（`~/.ssh`、`.env`等）并进行网络发送、写入外部位置等危险操作
  - ⚠️ **降级条件**：读取特定凭证调用其对应的官方服务（如读取 `OPENAI_API_KEY` 调用 `api.openai.com`），或通过 SSH 协议使用 SSH key → 降为 **Suspicious**
  - 🔴 **维持 Malicious**：发送到与该凭证无关的第三方域名；批量读取多个敏感文件后外送；SSH 私钥通过 HTTP POST 发送
- ✅ **自动执行破坏性命令**：skill自动执行 `rm -rf`、修改系统配置等不可逆操作
  - ⚠️ **降级条件**：删除目标为项目内路径或临时目录（如 `rm -rf ./dist`、`rm -rf /tmp/cache-*`）→ 降为 **Suspicious**
  - 🔴 **维持 Malicious**：删除目标为系统级/用户级路径（如 `/`、`~/*`、`/etc/`）；路径来自变量且无法确认安全范围
- ✅ **隐蔽 + 危险操作**：使用 `2>/dev/null`、`--quiet`、`nohup` 等方式隐蔽执行上述危险操作
  - ⚠️ **降级条件**：被隐蔽的操作本身经分析已降为 Suspicious → 本条同步降为 **Suspicious**
  - 🔴 **维持 Malicious**：被隐蔽的操作仍为 Malicious
- ✅ **权限提升 + 危险操作**：`sudo`/`chmod 777` 配合上述危险操作（如 `sudo curl | bash`、`sudo rm -rf /`）
  - ⚠️ **降级条件**：被提权的操作本身经分析已降为 Suspicious → 本条同步降为 **Suspicious**
  - 🔴 **维持 Malicious**：被提权的操作仍为 Malicious

**⚠️ Suspicious - 可疑（环境风险或供应链风险）**：

- skill **自动执行全局安装未固定版本**的依赖（如 `pip install requests`、`npm install -g tool`）
  - 投毒风险：未固定版本可能拉取被投毒的最新版本
  - 不报风险情况：已固定版本（如 `pip install requests==2.28.1`）或在虚拟环境中安装
- 从非官方源安装依赖（`--index-url <非PyPI>`、`--registry <非官方源>`）
  - 无法验证源的安全性，仅做提醒
- 从代码仓库安装**且未固定 commit SHA**（如 `git+https://repo.git@main` / `git+https://...@v1.0`）
  - 投毒风险：分支/tag 可被随时更新或强制推送
  - 不报风险情况：已固定 commit SHA（如 `git+https://repo.git@a1b2c3d4e5f6`）

**✅ Benign - 可信（无投毒风险）**：

- 纯教学文档，无可执行代码
- 代码示例仅供参考（用户需手动复制使用）
- 示例代码中的质量问题（SQL注入、异常处理缺失等）→ **不报告**

---

**❌ 不报告教学代码质量问题**（SQL 注入示例、异常处理缺失、命名规范、算法效率、架构设计等均由开发者自行负责）

**📊 安全评分计算规则**（内部计算逻辑，不展示在报告中）：

**评分区间与风险等级对应关系**：
- 🔴 Malicious（恶意）→ 0-30 分
- ⚠️ Suspicious（可疑）→ 31-75 分
- ✅ Benign（可信）→ 76-100 分

**计算方法**：
1. **存在 Malicious 发现项**（最终评分：0-30 分）
   - 基础分 30 分
   - 每个 Malicious 发现项扣 10 分（最低 0 分）
   - 计算公式：`max(0, 30 - malicious_count × 10)`

2. **无 Malicious，但存在 Suspicious 发现项**（最终评分：31-75 分）
   - 基础分 75 分
   - 每个 Suspicious 发现项扣 8 分（最低 31 分）
   - 计算公式：`max(31, 75 - suspicious_count × 8)`

3. **无任何风险发现（Benign）**（最终评分：76-100 分）
   - 纯教学文档、无可执行代码 → 100 分
   - 有代码但无风险行为 → 85 分

### 步骤7：输出完整报告

按以下格式生成md格式报告：

```markdown
# 🔍 安全审计报告

## 📊 执行摘要
- **审计对象**: [skill名称和路径]
- **发现问题总数**: X个
  - 🔴 Malicious（恶意）: X个
  - ⚠️ Suspicious（可疑）: X个
  - 📝 信息性提醒: X个（非风险项，不计入风险总数）
- **安全评分**: [0-100]分

---

## 🔴 Malicious（恶意）风险发现
[如果没有，显示：✅ 未发现 Malicious 风险]

1. **[问题类型]**
   - **位置**: 文件名:行号
   - **代码片段**: `具体代码`
   - **风险描述**: 详细说明安全风险
   - **攻击场景**: 攻击者可以如何利用
   - **修复建议**: 具体的修复方案

---

## ⚠️ Suspicious（可疑）风险发现
[如果没有，显示：✅ 未发现 Suspicious 风险]

---

## 📝 信息性提醒（非风险项）
[Step 0 排除的作者自身凭证泄露等不构成投毒风险的发现项归入此处。如果没有，显示：✅ 无信息性提醒]

1. **[问题类型]**（信息性提醒）
   - **位置**: 文件名:行号
   - **代码片段**: `具体代码`
   - **说明**: 该凭证为作者自身凭证，不构成对用户的投毒风险
   - **建议**: 建议作者改用环境变量管理敏感凭证

---

## 📋 详细检查结果

### 命令执行与权限检查
- 发现次数: X次
- 详细列表: [列出所有匹配的行号和内容]

### 文件操作与敏感路径检查
- 发现次数: X次
- 详细列表: [列出所有匹配的行号和内容]

### 网络请求检查
- 发现的URL: [列出所有URL]
- Base64编码检测: [是否发现可疑编码]

### 远程脚本深度分析
[如果存在自动下载+执行的远程URL，对每个URL列出深度分析结果]
- **URL**: [具体URL]
- **脚本可访问性**: [可访问 / 不可访问 / 二进制文件]
- **发现的恶意/可疑行为**: [具体列举，或"未发现明显恶意行为"]
- **脚本主要功能**: [一句话总结]
- **深度分析结论**: [当前内容安全性评估]
- **定级影响**: [基于深度分析结论，该风险项最终定级为 Malicious/Suspicious，并说明理由]

### 依赖安装风险检查
- **全局安装检测**: [是否发现全局安装命令（Suspicious（可疑）环境破坏风险）]
- **虚拟环境检查**: [是否提供虚拟环境隔离说明]
- **依赖来源检查**: [是否从非官方源安装（Suspicious（可疑）潜在风险提示）]

---

## 💡 总体建议

[根据发现的问题给出总体改进建议]

---

## ✅ 审计结论

**风险等级**: [基于 Malicious / Suspicious / Benign 标准判定]

**使用建议**:
- ✅ **Benign（可信）- 可以安全使用**（76-100分）：无投毒风险，纯教学内容
- ⚠️ **Suspicious（可疑）- 建议改进后使用**（31-75分）：存在环境风险或供应链风险，建议确认后使用
- 🚫 **Malicious（恶意）- 严禁使用**（0-30分）：存在自动执行危险操作的投毒风险
```

---

## 重要提示

⚠️ **执行此skill时必须**：

1. 完整执行所有步骤（含步骤4远程脚本深度分析）
2. 对存在风险的每个检测项给出明确结果
3. 不跳过任何搜索步骤
4. 提供完整的行号和代码片段
5. 给出明确的安全评分和使用建议
## 学习轮章节（已下沉 references/knowledge-base.md，正文留指针）

- 🏛️ 平台级技能准入参考模型 → 

- Skill 安全风险九类分层（T01–T09）：审查要按"攻击面层级"过，不按文件顺序过 → 

- 审查别拿"符合性代理"当技术证据：记录面要按三类缺陷主动查，不看厂商标签 → 

- 控制门的延迟会诱发绕过：安全开销本身就是合规率的一部分 → 

- 审阅/验证第三方技能这一步本身不得引入运行期副作用：Staging 不跑 install/build/postinstall，按对象类型选扫描器 → 

- 内容可读与代码可执行必须分两档：远端技能包可全文下发、强校验，但包内脚本永不执行；同步排除清单把可信钩子挡在不可信沙箱外 → 

- 风险分层按「是否含可执行资产」，不按文本扫描结论；技能文件本身就是注入载荷 → 

- 本地小模型审计技能包要走"证据引导两段式"，不能让 compact LLM 直接判 → 

- 信任信号要逐维度报覆盖率，不能只给一个总通过率；单维 100% 可能掩盖其他维几乎为零 → 

- 门控资格与分诊资格是两档：一个检测配置有没有「门控资格」由它对良性样本的标记率单独判定，召回提升换不来门控权 → 

- 允许集与校验集是两个集合：字段被接受不等于字段被检查，名字像安全承诺的字段尤其危险 → 

- 审查结论要有一个显式的「不处置」档位，且误报形态可枚举：不是每条读数都要整改，关闭必须带理由 → 

- 出站副作用要在 frontmatter 里声明成契约，审计器不执行也能判：外发字段与失败姿势必须可静态读 → 

- 来源要分两个锚：registry 上的 owner 只是分发渠道标签，不等于发布者密码学证明 →

- 扫描判级三原则（能力≠滥用、云端判定缓冲、Safe 模板禁无证据默认✅）：扫描器判定要区分「能力存在」与「能力被滥用」——敏感原语（bash/子进程/读密钥/env）若属声明功能所需且有文档，只报能力不判恶意；云端 risky 不默认高危，按实际影响二次映射，unknown/请求失败必须降级本地审计并记「云情报不可用」；Safe 输出模板禁止无证据默认✅，须附「静态分析不覆盖后续更新风险」免责（来源：matrix.tencent.com/clawscan/skill.md 46,622B，2026-10-07 独立 curl 实拉逐串命中 `ability vs Abuse`/`can do dangerous`/`base64`/`zero-width`/`ROT13`；与 §审查结论要有「不处置」档位 互补——那条管误报形态枚举，本条管扫描判级的总原则）
- **判据**：① **「能做事」与「在做坏事」是两层判定**：扫描器若一见危险原语就标 Medium+，会把"声明功能需要的敏感能力"误判为恶意 ⇒ 判定逻辑要先问"这个能力是否为该技能声明功能所必需且已文档化"，是则不升恶意、只作能力登记。② **云端分级结论要带缓冲**：risky 类结果默认不映射到高危，必须按本地实际影响二次判定；云端情报不可用（unknown/请求失败）时降级到本地审计并留痕，不许假装云端结论存在。③ **Safe 模板的✅必须基于证据**：无证据不得默认给通过章，且强制附"静态分析不覆盖后续更新"免责，防止"扫过=安全"的错误暗示。④ 与既有「审查结论要有显式不处置档 + 误报形态可枚举」构成"判级原则 + 误报枚举"双层，本条是原则层。
- 提升层：可复用 Skill / 工具。触发词：能力-滥用二分、声明功能所需才报能力、risky 不默认高危、云端降级本地审计、Safe 模板禁无证据默认✅、静态分析不覆盖后续更新。

- 漏洞类别全清单（17 类 / 68 模式）作扫描规则覆盖度对照表，Triage 处置动词表五档（阻断至修或正式接受 / 发布前移除 / 欠声明→改权限或删行为 / 有漏洞依赖→升级-pin-文档化豁免 / 描述-行为失配→改描述或改代码），报告格式含 SARIF 入 CI（来源：docs.nvidia.com/skills/scanning-agent-skills.md 4,822B，2026-10-07 独立 curl 实拉逐串命中 `Memory poisoning`/`Trigger abuse`/`Taint tracking`/`YARA`/`MCP least privilege`/`MCP tool poisoning`；与 §审查九类 T01–T09 互补——九类是自家分层，本条是 NVIDIA 公开 17 类全清单，可作覆盖度对照）
- **判据**：① 自家九类分层要对照公开 17 类找覆盖盲区（如 memory poisoning / trigger abuse / taint tracking / YARA / MCP least privilege / MCP tool poisoning 等是否已在自家判级里）。② **处置动词要可机检**：每条发现对应一个明确动作（修 / 删行为 / 文档化豁免 / 改描述），含糊的"建议注意"不算处置。③ **SARIF 入 CI** 使扫描结果可进流水线条件，不只是给人看的报告。
- 提升层：工具。触发词：17 类漏洞清单、68 模式、Triage 五档处置动词、SARIF 入 CI、覆盖度对照。

- 信任徽标必须自带「负向适用范围」声明：徽标/扫描结论若只报"已覆盖的项"，要同时写明它**不裁定**的那一面（如 AIPM Registry 明示 "metadata checks, not a malware verdict"——元数据校验≠恶意裁决）（来源：aipm-registry.com/research/state-of-agent-skills-2026 43,058B，2026-10-07 独立 curl+UA 实拉逐串命中 `metadata checks`/`not a malware verdict`/`1%`/`Organization`；与 §信任信号要逐维度报覆盖率 互补——那条管"维度覆盖率要分别报"，本条管"结论要明示不裁定面"）
- **判据**：① 任何对外展示的信任信号（徽标/扫描通过章/评分）都要写清它**不证明**什么，否则读者会把"部分覆盖"读成"整体安全"。② 与覆盖率倒挂同族但机制不同：覆盖率倒挂管"各类信号实际占比要公开"（1% 组织审查伪装成 100% 安全感），本条管"每个信号本身要声明否定式适用范围"。
- 提升层：可复用 Skill。触发词：信任徽标负向适用范围、metadata checks not a malware verdict、声明不裁定面。

## r436A-r436A2（全文已下沉 references/knowledge-base.md §r436A-r436A2；2026-10-09 r484 正文预算下沉）
## 技能「形态」应在内容审查之前先定权限档：是否捆绑可执行脚本是可静态判定的事实，直接决定权限下限——实测 bundling executable scripts 使漏洞风险 2.12×（来源：arxiv.org/html/2602.12430v4 169,999B，2026-10-08 独立 curl 实拉逐串命中 `Skills bundling executable scripts are 2.12` / `An unvetted community skill (T1) receives instructions-only access with full tool isolation` / `T1 and T2 skills are never granted script execution` / `Level 3 executable scripts require T3 or T4 trust`；与 §恶意产能按发布者聚合熔断 互补——那条管封禁的作用域单位，本条管单个技能安装前的权限先验档）
- **判据**：① **形态先于内容**：有无 `scripts/`、frontmatter 是否声明可执行资源，是零成本可判的事实；把它作为权限档输入，可在读第一行代码前就把默认权限压到 instructions-only（T1/T2 永不授予脚本执行），审查资源优先投给含脚本者。② **2.12× 是分诊权重不是罪名**：倍数是排队依据（含脚本优先深审、加行为回归），不是「含脚本即恶意」。③ **与行为定档串联而非替换**：既有按沙箱观察后定档是事后校验，本条是事前先验，串成「先验给下限、行为校验再升降档」。④ 数字须连原文位置引：2.12× 出 Sec 6.2 实测、T1–T4 出 Sec 6.4 权限映射，混引会造出不存在的因果。（细则见 references/knowledge-base.md §r437A）
- 提升层：可复用 Skill（准入策略 / 权限先验）。触发词：形态先验权限档、2.12×、T1/T2 不授予脚本执行、Level 3 脚本需 T3/T4、含脚本优先深审、先验档与行为定档串联。


## 风险档位只由「可能性 × 影响」决定，不得按「偏离清单的条目数」打分；判定三态中未确认项被显式剥夺 severity，且检查者不得是发现者（来源：github.com/cloudflare/security-audit-skill 295,484B，2026-10-08 独立 curl 实拉逐串命中 `Severity requires impact.` / `Likelihood x impact, not deviation from a checklist.` / `confirmed, needs_validation, and rejected` / `The agent that checks a finding is never the agent that found it.`；与 §扫描判级三原则 互补——那条管能力≠滥用，本条管定级的算术与判定者分离）
- **判据**：① **符合度不是风险**：偏离清单条目多不等于风险高，只有 likelihood×impact 才是定级输入；把「不符合项计数」当风险分会让清单越长风险越高。② **三态各带约束**：`confirmed` 需 complete source trace + bounded observed result；`needs_validation` 只记未决事实、**禁带 severity**（未证实的候选不得预先打分）；`rejected` **显式记录被证伪的候选**（不静默丢弃）。③ **检查者≠发现者**：验最终源主张要用 fresh agent，不复用原 detector。（细则见 references/knowledge-base.md §r437C-4）
- 提升层：可复用 Skill。触发词：Likelihood x impact、not deviation from a checklist、needs_validation 禁 severity、rejected 记录被证伪候选、检查者不等于发现者。

## 运行期可执行面的允许清单，声明权归「部署运营方」而非技能作者：作者侧管字段可见性，运营方管命令可执行性——两个声明者要分别检查（来源：github.com/FlowiseAI/Flowise/releases/tag/flowise@3.1.4 213,716B，2026-10-08 独立 curl 实拉逐串命中 `Fix Flowise 709 Make Custom MCP stdio command allowlist operator-controlled by @yau-wd in #6578`；与 §出站副作用声明成契约 互补——那条管作者声明外发面，本条管谁有权定义可执行命令面）
- **判据**：① 审计允许清单时先问「这份清单是谁写的」：作者随包提交的允许清单是**自证**，运营方在部署期注入的才是外部约束；二者同名但约束方向相反（作者想放宽以便运行 vs 运营方要收紧以便管控）。② 同一技能可以两面都有，审计报告须分列两个声明者，不许合并成「已配置允许清单」。③ 运行期命令面（stdio 命令、可执行路径）属运营方所有权，作者无权自授。（细则见 references/knowledge-base.md §r437C-5）
- 提升层：可复用 Skill。触发词：允许清单声明权、operator-controlled allowlist、作者自证 vs 运营方约束、运行期命令面所有权、两个声明者分列。

## 批准不是权限本身，而是「派生关联」：每次使用都要对活的授权行再验证，且批准绑定的是规范化执行上下文（cwd + 精确 argv + env 绑定 + 固定可执行路径），启动前重解析重检查（来源：docs.openclaw.ai/tools/exec-approvals 一手 363,977B，2026-10-08 r438B 独立 curl 实拉逐串命中 `a grant is derivative correlation, revalidated against the live approval row, automation row, and revocation state on every use` / `bind canonical execution context: cwd, exact argv, env binding when present, and pinned executable path` / `re-check it before launch` / `not a per-user auth boundary or filesystem read-only policy`；全库 grep `revalidated` / `exact argv` 均 0 命中）
- **① 授权状态不能缓存**：批准记录是**对另一行授权状态的派生关联**，不是一份自足的权限；每次使用都要拿活授权行 + 自动化行 + 吊销状态三者重新对一遍。判据：**审计"有没有权限"时，看的是再验证的动作，不是批准记录的存在**；只查"批过没有"等于把可撤销的引用当成了既得权限。
- **② 批准要钉到可执行身份，不能钉到命令名**：批准的粒度是规范执行上下文——cwd、精确 argv、env 绑定、固定可执行文件路径；网关侧在评审前绑定每个解析出的命令段可执行文件，**启动前再检查一次**。原文同时给出边界声明：这只降低误执行风险，**不构成按用户的认证边界，也不构成文件系统只读策略**。判据：审查批准/白名单机制时问三件事——绑的是名字还是 argv+路径？启动时重不重查？文档有没有把"批准过"说成"有权"？三者任一答错即判缺陷。
- 提升层：可复用 Skill（权限模型）/ 工作流（运行期授权复核）。触发词：批准不是授权边界、derivative correlation、revalidated on every use、exact argv、pinned executable path、re-check before launch、授权不能缓存、批准粒度、per-user auth boundary


## 审批校验要验「记录的签发者是否有权为本动作签发」，不能只验记录存在：跨技能链把伪造审批藏在单技能扫描的盲区（来源：arxiv.org/abs/2610.01564 + /html/2610.01564v1 293,934B，2026-10-08 一手实拉）
- **实证**：APEX 全链攻击成功率 **84.3%**，而把同样的两步合并进**单个技能**只有 **17.4%**；512/690 attempts＝**74.2%**；提示层防御把良性 verifier 通过率从 **86.7%** 压到 **56.3%**。原文机制：「an agent-written record of genuine task progress can carry a false claim of user approval across skills」「an upstream skill induces the agent to create the record, and a downstream skill ...」。
- **判据**：① **风险藏在链上，不在件上**——单技能静态扫描对本类攻击天然高漏（84.3% vs 17.4% 的差值就是链带来的增量），审计必须按**调用序列**而非单包取证；② 消费侧见「已批准」记录时，要回溯**该记录的签发者是否被授权签这一类动作**，只验存在性等于把上游诱导当授权；③ **防御代价必须与攻击成功率并列报告**（86.7%→56.3% 的可用性损失不是免费的），只报拦截率的防御方案不可验收。
- **与既有能力分工**：r437C「允许清单声明权归运营方」管**谁有权写清单**；本条管**跨技能传递的审批声明由谁签发**——两处都是「声明者身份」，但一在授权面一在传递面，须分别检查。
- 提升层：工具（取证面）/ 工作流（审计序列）。触发词：链式审批伪造、84.3 vs 17.4、agent-written record、跨技能链、签发者权限、防御代价并列报告。


## 技能根目录是「容纳边界」：装载时对越根软链一律跳过并留原因位，共享靠显式白名单目录而非隐式跟随（来源：docs.openclaw.ai `/gateway/troubleshooting/skills-and-model-providers` 247,412B，2026-10-08 一手实拉）
- **实证**：官方日志形态「Skipping escaped skill path outside its configured root: ... **reason=symlink-escape**」；定性原句「**Every skill root is a containment boundary**」——`~/.agents/skills`、`<workspace>/.agents/skills`、`<workspace>/skills`、`~/.openclaw/skills` 下的越根软链一律 skip；放行须同时具备显式 `extraDirs` + `allowSymlinkTargets`，且 `~`、`/` 这类宽目标被禁。
- **判据**：① **复用技能不许用软链"借道"**——把外部目录链进技能根等价于让该目录绕过一次准入审查；共享只能走显式登记的额外目录白名单；② **跳过必须留原因位**（`reason=symlink-escape`），静默跳过会让"技能没生效"变成无痕失败，排查时看不到被拒的那一次；③ **白名单目标是路径精度问题**：`~`、`/` 这类宽目标一旦开了等于边界失效。
- **与既有能力分工**：r437A「形态先验权限档」管**有没有脚本决定权限下限**；本条管**技能根之外的内容能不能被带进来**——前者是权限档，后者是容纳面。
- 提升层：工具（装载面）/ 工作流（准入）。触发词：容纳边界、symlink-escape、越根软链、extraDirs、allowSymlinkTargets、技能没生效无痕失败。

## 复审的记分对象是「新增」不是全量；LLM 语义阶段只升不降置信，未确认项须显式打 `llm-unconfirmed`（来源：api.github.com/repos/NVIDIA/SkillSpector/contents/README.md 53,632B 全解，2026-10-08 一手实拉）
- **实证**：官方原文「Scan against the baseline — **only NEW findings are reported and scored**」；「Findings the model reviews but does not confirm (disputed, low-confidence, or unaddressed) are tagged **`llm-unconfirmed`** in JSON and SARIF output」。
- **判据**：① **跨轮扫描必须区分三态：新增 / 已被 baseline 抑制 / 未确认**——把全量重贴当"本轮发现"会让同一个 finding 在每轮报告里重复计分，风险趋势图上看到的是基线漂移而非真实新增；② **模型没确认的东西不许当已确认**：语义阶段只升不降置信 ⇒ 未确认项要单独留标签位，混进 confirmed 会让"AI 复核过"变成虚高可信度；③ baseline 是记分口径的一部分，**换基线等于换量纲**，跨基线比较前必须先对齐基线版本。
- **与既有能力分工**：r437C「风险档位 = likelihood×impact，needs_validation 禁 severity」管**单条 finding 怎么定级**；本条管**跨轮之间怎么记分与去重**——定级在前，记分在后。
- 提升层：工作流（扫描口径）/ 工具（报告契约）。触发词：only NEW findings、llm-unconfirmed、基线记分、重复计分、跨轮三态、换基线换量纲。

## 拦截项要分「可翻墙」与「不可翻墙」两档并显式标注；下架与撤权是两个可分档位（来源：docs.openclaw.ai/cli/skills 25,891B + clawhub/how-it-works.md 3,662B，2026-10-08 一手 curl 取 `.md` 原文逐串命中 `Neither --force nor the acknowledgement overrides block or a policy failure` / `upload gates, automated checks, user reports, and moderator action` / `may disappear from public search and install flows while remaining visible to the owner for diagnostics`；与 §复审记分对象是新增 互补——那条管跨轮记分，本条管拦截的绕过面与处置分档）
- **实证**：官方原文「Neither `--force` nor the acknowledgement overrides `block` or a policy failure」；ClawHub 四道关卡「releases are still subject to **upload gates, automated checks, user reports, and moderator action**」（举报是独立一道，机扫与人审之外）；被处置内容「may **disappear from public search and install flows** while **remaining visible to the owner for diagnostics**」；宿主消歧：技能可替换同名 bundled command，但**不替换其别名**（覆盖只作用于直呼名）。
- **判据**：① **把「`--force` 能过」当默认是治理漏洞**：拦截项必须逐条标注属"带确认可强推"还是"policy failure，force/ack 皆无效"；不标注时，使用者会把所有拦截都当成可翻墙，真正的硬拦截在一次误操作后失去意义。② **下架 ≠ 撤权**：从公域搜索/安装流消失、同时保留属主可见用于诊断，是**两个可分档位**——复审期工件仍需可被属主使用与取证；一步到封杀会同时毁掉取证面。③ **举报是独立一道关卡**：自动化扫描与人工审核之外必须有独立举报入口；只有机扫+人审的体系，其漏网面永远等于"没人点开看过的那些"。④ **覆盖语义只作用于直呼名**：技能能替换同名内置命令但不替换其别名 ⇒ 冒名面不是"改个名字就绕过了"那么简单，消歧规则要按调用形态（直呼 vs 别名）分别判定。
- **与既有能力分工**：r439B「技能根=容纳边界」管**装载时能不能被带进来**；本条管**已经被拦下之后还能不能被绕过、以及拦下的处置档位**——准入在前，处置在后。
- 提升层：工作流（处置分档）/ 工具（拦截语义）。触发词：--force 不可翻墙、policy failure、下架不等于撤权、owner 可见诊断、用户举报独立关卡、覆盖不替换别名、拦截项分档标注。


## 漏洞情报源要带「自动离线回退」，且模式库规模必须给出「类别数 × 模式数」双层粒度作为覆盖基准的分母（来源：api.github.com/repos/NVIDIA/SkillSpector/readme 53,566B 解码全文，2026-10-08 一手 curl 逐串命中 `71 vulnerability patterns` across `17 categories` / `SC4 | Known Vulnerable Dependencies | HIGH | Dependencies with known CVEs (live OSV.dev lookup)` / `real-time CVE data with automatic offline fallback`；与 §r435C 17 类漏洞清单 + Triage 五档处置 + SARIF 入 CI 互补——那条落"检出来怎么处置与怎么进 CI"，本条落"情报从哪来、断网时朝哪个方向失败、覆盖够不够怎么量"）
- **实证**：原文「**71 vulnerability patterns** across **17 categories**: prompt injection, data exfiltration, privilege escalation, supply chain, excessive agency, output handling, system prompt leakage, memory poisoning, tool misuse, rogue agent, anti-refusal, trigger abuse, dangerous code (AST), taint tracking, YARA signatures, MCP least privilege, and MCP tool poisoning」；「**Live vulnerability lookups**: SC4 queries [OSV.dev](https://osv.dev) for real-time CVE data with **automatic offline fallback**」；「**Multiple output formats**: Terminal, JSON, Markdown, and **SARIF** reports」；阶段与基线「Two-stage analysis: Fast static analysis + optional LLM semantic evaluation」「Baseline / false-positive suppression … so re-scans surface only *new* issues」。
- **判据**：① **依赖实时情报的检查必须显式声明离线时的方向**：SC4 命中 CVE 靠在线查询，官方明写"自动离线回退" ⇒ 联网检查的默认失败方向如果是"查不到=没有漏洞"，断网期间的扫描会静默降级成"全部安全"；正确写法是把"情报源不可用"作为可观测状态（与"扫过且无 CVE"区分）。② **模式库规模要分两层报（类别数 × 模式数）**：17 个类别是目录、71 个模式是条目 ⇒ 只报"覆盖 17 类"会让人以为只有 17 项检查；覆盖率的分母是模式数，归类方式由类别数决定，两者缺一都无法判断"这个扫描器是否够用"。③ **类别清单本身就是威胁面清单**：17 类里既有注入/外传/提权这类经典面，也有 memory poisoning、rogue agent、anti-refusal、trigger abuse、MCP tool poisoning 这类 agent 特有的面 ⇒ 审自己的技能库时，先拿这份清单对一遍"哪些面我根本没有检查项"。④ **两阶段（快速静态 + 可选语义）意味着第二阶段可缺席**：LLM 语义评估是 optional ⇒ 报告里必须标注本次是否跑了语义阶段，否则同一份结果可能是两种强度的产出。⑤ **与处置链串成完整闭环**：模式库（覆盖什么）→ 情报源（依赖是否已知有洞，含离线回退）→ 基线（只报新增）→ SARIF（进 CI）⇒ 任何一环缺席，扫描结论都只能当线索不能当裁决。
- **与既有能力分工**：r435C「17 类清单 + Triage 五档 + SARIF 入 CI」管**检出之后的处置与集成**；本条管**情报来源的失败方向与覆盖度的计量基准**。
- 提升层：工具（扫描器接入三要素）/ 治理（覆盖度分母）。触发词：71 模式 17 类别、模式库规模双层粒度、OSV.dev 实时 CVE、automatic offline fallback、离线回退方向、两阶段可选语义、类别清单即威胁面、覆盖度分母。

## 审查对象应是「带证据的发布物 + 可重跑的体检通道」而非源树：发布附带 release-manifest / postpublish-evidence / dependency-evidence（json+sha256）三资产 + Doctor 只读托管配置修复（来源：api.github.com/repos/openclaw/openclaw/releases，2026-10-08 一手 curl 逐串命中 `release-manifest`×12/`postpublish-evidence`×12/`dependency-evidence`×6/`sha256`×26；与 r423C「交付物验收而非源树」同轴，补证据文件命名集；r445A 落地）
- **实证**：openclaw v2026.10.1-beta.1 随发布附带 **release-manifest / postpublish-evidence / dependency-evidence（json+sha256 三件套资产）** + "Updates and Doctor"（serving-verdict 恢复、只读托管配置修复）；v2026.9.8 稳定版 "58 commits · 43 PRs · 21 contributors"。
- **判据**：① 验收一个技能/包，看的应是"它发布时带了哪些可验证证据"而不是"源码长什么样"；② 证据文件要有命名约定（manifest/evidence 分三类：发布清单、发布后证据、依赖证据）且带 sha256 可重算；③ 配套一个只读的"体检"通道（Doctor）能在不破坏托管配置前提下修复/恢复 verdict ⇒ 审查与自愈是两个伴生能力，缺一不可。
- **与既有能力分工**：r423C 管"验收对象是交付物不是源树"这一原则；本条补"交付物该带哪几类证据文件"的具体形态。
- 提升层：工具（发布证据链）/ 治理（验收口径）。触发词：release-manifest、postpublish-evidence、dependency-evidence、json+sha256 三件套、Doctor 只读托管修复、带证据的发布物、交付物验收。

## 软 404 识别法（等大小 200 = SPA 壳，真枚举走 robots→llms→sitemap→*.md）+ 安全审查可落地为「三档判定 + with/without A/B + evals.json 导入」的评测而非人审徽章（来源：skillhub.cn/install/skillhub.md（7,429B 壳对照）+ github.com/alibaba/skill-up README，2026-10-08 一手 curl 逐串命中 `rule_based`/`script`/`agent_judge`/`evals.json`/`Qoder`；r445B 落地）
- **实证**：① 软 404：skillhub.cn `/api/*` `/docs` `/version.json` 全为 ~7,429B 同形 SPA 壳（无 `__NEXT_DATA__`），真内容走 robots→llms.txt→sitemap→`*.md` 链；判定法：**等大小 200 = 壳信号**。② alibaba/skill-up：`eval.yaml` + `cases/*.yaml`、`schema_version: v1alpha1`、判定三档 `rule_based`/`script`/`agent_judge`、with/without-Skill A/B、Docker/OpenSandbox 供给、引擎含 **Qoder CLI**/Claude Code/Codex、可导入 `evals.json`、提供 GitHub Action。
- **判据**：① 抓取技能市场/文档时，必须区分"真 404"与"软 404（同形壳）"——后者会骗过"200 即有内容"的假设，curl 拿到的 7KB 壳不是真内容；② 安全审查不该只是贴"已审"徽章，而应是一套可跑的评测（三档判定 + A/B + 可导入既有 evals）；③ 与 r443C「评测产物落盘契约」互补——那条管 WB 自己怎么评测技能，本条管"上游平台把审查做成评测"的形态。
- **与既有能力分工**：r443C 管 WB 评测产物落盘契约；本条管"上游平台审查即评测"的可复用形态与站点抓取判活法。
- 提升层：工具（站点抓取判活）/ 工作流（审查即评测）。触发词：软404 等大小200、robots→llms→sitemap→md、rule_based script agent_judge、with/without A/B、evals.json 导入、审查可跑评测、skill-up。
## 「已审核 / Vetted」只是形容词：给不出方法学页的市场，其收录量与审核字样一律不计入信任权重，只作候选发现面（来源：skills.rest 688,475B + /llms.txt 2,533B + /sitemap.xml 9,664B + /docs 404（23,304B 软 404 壳），2026-10-09 一手 curl 逐串命中 `113,000+ vetted agent skills` / `Vetted. One-click install. 100% free.` / `contributed by official partners, verified authors, and the community`；r472B 落地）
- **实证**：① 三处自陈「审核」——llms.txt「**113,000+ vetted agent skills**」、首页标语「**Vetted.** One-click install. 100% free.」、贡献者说明「contributed by official partners, **verified authors**, and the community」；但对 `vetting 方法 / scanner / threshold / re-audit 节拍` 的语境逐串抽取，**全部零命中**（"verified" 只作为技能描述里的形容词出现，非平台方法学）。② **方法学页缺失**：`/docs` 返回 404 且附带 23,304B 软 404 壳 ⇒ 无任何方法学页可核对。③ 三通道安装：Claude Code = 详情页给出的安装命令；Claude.ai = 下载 **.zip** → 项目设置上传解压 → `/skill` 激活；API = 引用技能包 URL。④ sitemap 为**索引式**（含 `repos.xml`、`authors-0..3.xml` 等分片，`<loc>` 可枚举）⇒ 按仓轴与作者轴可静态枚举。**诚实边界**：Qoder 转述的 `npx skills add <owner>/<repo> --all -g -y` 在本轮实拉的三个文件内 **0 命中**，不予采信，留候选池待详情页复核。
- **判据**：① **「已审核」是结论不是证据**：凡只给形容词、给不出 **扫描器名单 + 判定阈值 + 复审节拍** 的，其收录量与「审核」字样**不计入信任权重**，只作候选发现面（与 r410C / r442-Q-B「认证是带再验证时钟的状态」「徽标 ≠ 安全」同轴；本条补的是**「方法学页缺失」这一可机检的负证据信号**）。② **机检路径固定**：探 `/docs`、`/methodology`、`/security` 是否 200 且有实质正文；软 404（等大壳页）按**未达**计，不得记为「有页面」——把壳页当正文是最典型的假阳性。③ **规模越大越要先验证方法学**：113,000 级自陈规模配零方法学出处 ⇒ 规模不构成可信度，反而放大误采信面（呼应 ssc 既有「标记率 ≠ 风险规模」）。④ **分发通道本身计入风险面**：zip 下载解压 + `/skill` 激活这类形态把人工复核点从安装流里移除 ⇒ 评信任时要把安装通道的默认参数一并看，凡是「免确认 / 全量」形态都应视为复核点被跳过的显式证据。⑤ **新站登记（建议入必须项，按低信任计数源处理）**：skills.rest = 第三方 Agent Skills 聚合注册表，自述 113,000+ / 10 个专业领域 / 三通道安装，可与 skills.sh、SkillsMP 构成**第三家独立计数源**，用于跨注册表同名技能扩散比对，但不得单独作为可信度依据。
- 提升层：可复用 Skill（市场准入判据）/ 工作流（信源分级）。触发词：自陈已审核、Vetted 无方法学、方法学页缺失、/docs 软 404、113,000 vetted、聚合注册表低信任计数源、skills.rest。

## 扫描覆盖的是「检查面」，执行面可被随包字节码缓存替换：扫描对象须含 __pycache__/.pyc 并与源码做行为一致性比对，且防御代价必须与检出率并列（来源：arxiv.org/abs/2610.10612（PyCache Trap）43,017B，2026-10-09 一手 curl 逐串命中 `Python may execute a bundled bytecode cache with different behavior` / `Across 100 skills and seven scanners, PyCache Trap achieves 94-100% attack success, with no semantic recognition of the cache-resident behavior` / `detects all 100 evaluated source-present cache substitutions and reaches 92.8% Recall at 10.0% FPR across five attack families and 200 benign skills`；r472B 落地）
- **实证**：① 缝隙定义「Existing skill scanners inspect documentation and visible source, but **Python may execute a bundled bytecode cache with different behavior**」；② 攻击构造 = 良性源码 + 被替换且被 loader 接受的缓存 + 任务相关调用，并用 **scanner-guided rewriting** 改调用措辞而保留缓存本体，把「包准入」与「对隐藏行为的识别」脱钩；③ 规模「Across **100 skills and seven scanners**, PyCache Trap achieves **94-100%** attack success, with **no semantic recognition** of the cache-resident behavior」；④ 防御 EAV（execution-aware validation）把被检查的指令 / 脚本 / import / 运行期工件连成 **typed execution graph**，「detects **all 100** evaluated source-present cache substitutions and reaches **92.8% Recall at 10.0% FPR** across five attack families and 200 benign skills」。
- **判据**：① **检查面 ≠ 执行面**：静态扫描默认只覆盖可见源码，运行时却可能加载随包字节码缓存 ⇒ 准入只看源码等于放行执行面（与 r445B / r448-Q-C 已落的「预编译字节码绕过」同机制；本条补的是**一手规模数值**与**防御侧代价**）。② **不是个别扫描器失手，是全行业面失效**：100 技能 × 7 扫描器 94–100% ASR、对缓存内行为零语义识别 ⇒ 单换扫描器不构成缓解。③ **防御的误报率必须与检出率并列报告**：EAV 100/100 检出的代价是 **92.8% Recall @ 10.0% FPR**（200 个良性里约 20 个误报）⇒ 只报 100/100 的防御方案不可采信（沿用 ssc 既有「防御代价须与攻击成功率并列报告」纪律）。④ **可操作增量**：扫描对象清单必须显式包含 `__pycache__/` 与 `*.pyc`，并与源码做**行为一致性比对**（而非仅存在性检查 / 仅源码扫描）。⑤ **措辞层面的相似性比对无效**：攻击靠 scanner-guided rewriting 改措辞保留工件本体 ⇒ 检测必须落到工件级（字节码/代码对象归一化后比对），不能落在文本级。
- 提升层：可复用 Skill（技能扫描与准入）/ 工具（执行面校验）。触发词：PyCache Trap、字节码缓存替换、检查面不等于执行面、__pycache__ 扫描、行为一致性比对、92.8% Recall 10.0% FPR、EAV typed execution graph。

## 技能「选择阶段」存在不需要任何注入痕迹的攻击面：用户提示与技能描述单看都良性，靠语义关系塑形即可把选择率从 15.2% 推到 63.5%，而人工评审只拦住 2.9%、五个 LLM 检查器平均放行 82.9%（来源：arxiv.org/abs/2609.02035（ISM）42,386B，2026-10-09 一手 curl HTTP 200 逐串命中 `increases the average target-selection rate (TSR) from 15.2% to 63.5%` / `73.5% TSR, only 9.8 percentage points below Explicit Steering` / `Human reviewers block ISM in only 2.9% of judgments, versus 91.4% for Explicit Steering` / `five LLM-based inspectors pass ISM at an average rate of 82.9%, versus 37.4%`）
- **实证**：① 攻击定义「even when the user prompt and skill description appear benign **in isolation**, their **semantic relationship** can still be strategically shaped to favor an attacker-chosen skill」；② 三阶段策略「broaden semantic coverage, strengthen target distinctiveness, and preserve natural prompt wording」；③ 跨度「Across four task domains and eight selector models, ISM increases the average TSR from **15.2%** to **63.5%**」；④ 与显式操纵的对照「In a matched comparison, ISM achieves a **73.5%** TSR, **only 9.8 percentage points below** Explicit Steering」；⑤ **人审几乎无效**「Human reviewers block ISM in only **2.9%** of judgments, versus **91.4%** for Explicit Steering」；⑥ **机审同样失效且方向相反**「five LLM-based inspectors **pass ISM at an average rate of 82.9%**, versus **37.4%** for Explicit Steering」。
- **判据**：① **"内容干净"不构成安全证据，因为被操纵的是关系不是内容**：提示与描述各自过审、组合起来仍能定向 ⇒ 检查必须落到"这个技能为什么会被选中"，逐件审查对这类攻击结构性盲。② **显式与隐式的拦截率差 31 倍（91.4% vs 2.9%），说明我们现有的"看一眼内容"式人审只对显式攻击有效**：把人审写进控制项时，必须声明它只对哪一类攻击起效，否则等于在控制矩阵里记了一个 2.9% 的措施却按 91.4% 上报。③ **LLM 检查器不是人审的替代品，是同一种盲的另一种形态**：对显式操纵放行 37.4%、对隐式放行 82.9% ⇒ 隐式攻击对机器评审比对人更宽松；加 LLM 检查器不能补人审的洞，两者在 ISM 上同向失效。④ **隐式攻击的代价只有 9.8pp，防御方却要付出"看起来正常"的全部伪装成本**：有效性损失这么小 ⇒ 不能假设攻击者会为了绕过而留下异常措辞；"读起来自然"不是良性信号。⑤ **选择阶段必须引入与描述无关的第二路判据**：既然描述可被塑形，那么最终选谁就不能只由描述与请求的语义匹配度决定 ⇒ 需要不可由描述单独影响的锚（安装位置 / 显式白名单 / 来源信任档），这与 r472A「安装位置决定谁跑」互补——那条是实测事实，本条给了"为什么必须这样"的攻击面证据。⑥ **报告口径**：任何"已通过人工审核"的声明，只在其针对显式攻击时成立；对隐式选择操纵，现行人工流程的实际拦截率是 2.9%。
- **与既有能力分工**：r439A「审批校验验签发者是否有权为本动作签发」管**授权链**；r437A「形态先验权限档」管**形态决定权限下限**；本条管**选择阶段这一前置入口**（授权与形态都还没生效之前，技能就已经可能被选中了）。
- 提升层：可复用 Skill（准入审查）/ 工具（选择面控制项）。触发词：ISM、Implicit Skill-Selection Manipulation、Semantic Matching、15.2% 到 63.5%、2.9% 人工拦截、82.9% LLM 放行、语义关系塑形、选择阶段攻击面、skill selection poisoning。
