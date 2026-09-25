---
name: bsk-drive-logged-in-browser
description: 用 bsk（BrowserSkill）驱动用户「已登录」的 Chromium 浏览器完成实操任务——发邮件、填表、点流程、读页面、抓数据。凡用户说「打开我的浏览器…」「用我登录的 XX 发/做/提交…」「帮我操作网页」「固定标签那个页面…」时使用。核心覆盖 WorkBuddy 环境下的实战坑：daemon 被回收、Agent Window 被关、PATH 缺 coreutils、弹窗确认、用户窗口标签的坐标层。触发词：bsk、BrowserSkill、驱动浏览器、操作已登录浏览器、固定标签、发邮件、163邮箱、填表提交、Agent Window、借用标签、borrow、daemon 被回收、52800、send email。（统一入口=browser-automation；本技能为其 bsk 驱动底层实现位，由它路由；两者同一功能位，只划边界不文件级合并。）
version: 1.2.0
agent_created: true
---

# 用 bsk 驱动用户已登录浏览器

**一句话结论：bsk 的原生 SKILL.md 讲的是「官方语义」；本技能讲的是「WorkBuddy 宿主环境下真正跑通要做哪些动作」——daemon 必须常驻后台、所有命令链式合并成一条、写收件人这类 React 控件要绕开坐标层用 JS、原生弹窗用 Enter 确认。**

宿主环境特征（决定了下面每一条）：
- 每次 Bash 调用结束，宿主**杀掉本次调用产生的子进程** → daemon 只要不是常驻任务就活不过一次调用。
- 每次 Bash 调用 PATH 会重置，且**缺 coreutils**（`dirname`/`head`/`cat`/`sed`/`awk` 都可能是 command not found）→ 命令前缀必须自带 PATH 修正。
- bsk 的输出会混入 shim 报错到 stderr；**不要信 exit code，要落盘读 stdout**。

---

## 0. 环境准备（每个会话只做一次）

### 0.1 PATH 修正 + 常驻 daemon

所有 bsk 命令前必须加这行 PATH 前缀：

```sh
export PATH="/c/Users/26719/.workbuddy/binaries/PortableGit/versions/1.2.0/usr/bin:$PATH"
```

> 不加会看到 `shell-runtime-bash-env.sh: line 3: dirname: command not found`。这行报错本身通常无害（shim 第 3 行 `cd "$(dirname ...)"` 失败但不阻断），但 PATH 里确实没有 coreutils，`head`/`cat`/`sed` 都会失败。

**daemon 必须用 `run_in_background: true` 启动**，否则第一次会话命令跑完 daemon 就被杀：

```sh
export PATH=".../PortableGit/versions/1.2.0/usr/bin:$PATH"; export BSK_AUTO_START=0; bsk daemon start --foreground
```
（用 Bash 工具 + `run_in_background: true` 提交，拿到 task_id 后**不要轮询**，直接进行下一步。）

### 0.2 验证 daemon 与浏览器

```sh
export PATH=".../usr/bin:$PATH"; export BSK_AUTO_START=0; bsk status --json > /d/tmp/st.json 2>&1
```
读 `/d/tmp/st.json`，期望看到：
```json
{ "daemon_version":"0.3.0", "protocol_version":"1.3", "browsers":[{"instance_id":"...","browser_name":"edge"}], "sessions":[] }
```

`browsers` 为空 = 浏览器扩展没连上，**不要重试**，直接让用户打开浏览器/装扩展。有多个浏览器实例时，后续 `session start` 必须带 `--browser <instance_id>`，否则报 `multiple_browsers_online`。

---

## 1. 启动 session（关键：链式合并 + 拿到 session_id）

**坑：session 存活期很脆弱——Agent Window 一被关，session 立刻销毁**（日志 `session removed: user closed Agent Window`）。

所以：**session start 之后立刻把后续步骤串进同一条命令**，不要在两条 Bash 调用之间留窗口。

```sh
export PATH=".../usr/bin:$PATH"; export BSK_AUTO_START=0
BID=$(bsk browsers 2>/dev/null | sed -n '2p' | awk '{print $1}')
bsk session start --json --browser "$BID" > /d/tmp/s.json 2>&1
SID=$(sed -n 's/.*"session_id": "\([a-z]*\)".*/\1/p' /d/tmp/s.json)
echo "SID=$SID"
bsk tab list --scope all --session "$SID" > /d/tmp/tabs.txt 2>&1
bsk observe --session "$SID" --max-tokens 2500 > /d/tmp/obs.txt 2>&1
```

- `--no-focus`：**不要用**。会让 Agent Window 不显示，反而更易被环境回收。
- 每步 `echo` 状态码，但**判断成败看落盘文件内容**。

---

## 2. 找到目标页面

```sh
bsk tab list --scope all --session "$SID" > /d/tmp/tabs.txt 2>&1
```

输出行格式：`TAB_ID  SCOPE  WIN_ID  TITLE  URL`。三种 scope：

| scope | 含义 | 能否直接操作 |
|---|---|---|
| `agent` | Agent Window 里的标签（bsk 新建的，如 `navigate` 出来的） | ✅ 直接操作 |
| `user` | **用户自己窗口里的标签**（例：固定标签、已登录页） | ⚠️ 需 `tab borrow` |
| 其他 | — | 不支持 |

- 用户说「固定标签」「我登录的那个页面」→ 找 `user` scope 且 TITLE/URL 匹配的标签。
- **优先借用户标签**，因为只有它带登录态。bsk 新建的 agent 标签是**全新会话、没有你的登录态**（实测：导航到 mail.163.com 只拿到登录页）。
- 找到后选中：`bsk tab select <TAB_ID> --session "$SID"`。

### 借用（borrow_confirmation=always 时必做）

```sh
bsk tab borrow <TAB_ID> --session "$SID"     # 浏览器会弹确认，用户点允许
```
- 会话 `interaction.borrow_confirmation = "always"` 时，**不 borrow 直接操作 user 标签会被拒**，报 `operation denied by the Agent Window sandbox` / `details: element not visible`。
- borrow 的结果可能是 `denied`/`timed_out`/`borrow_outcome_unknown`——**确认过就不重试**，先 `tab list` 看标签是否已在 agent scope。
- 用完立刻归还：`bsk tab return <TAB_ID> --session "$SID"`。

---

## 3. 读页面 → 决定动作

```sh
bsk observe --session "$SID" --max-tokens 2500 > /d/tmp/obs.txt 2>&1
```

- `@eN` 是 ref，**每次 observe/snapshot 都会全部作废**，动作前必须重新 observe。
- 内容多时用 `--max-tokens` 截断，返回的 `@more observe --cursor <token>` 可续读。
- 需要看视觉实况（弹窗、渲染异常）用截图：
  ```sh
  bsk screenshot --session "$SID" --out /d/tmp/shot.png >/dev/null 2>&1
  ```
  然后 **用 Read 工具看这张 PNG**——这是判断页面真实状态最可靠的手段。

---

## 4. 执行动作

| 需求 | 命令 |
|---|---|
| 点击 | `bsk click @e3 --session "$SID"` |
| 填普通输入框 | `bsk fill @e3 --value "text" --session "$SID"` |
| 逐字输入 | `bsk type @e3 "text" --session "$SID"` |
| 按键 | `bsk press Enter --session "$SID"` |
| 选下拉 | `bsk select @e3 --value "v" --session "$SID"` |

### 4.1 React / 富文本控件：fill 会「假成功」

实测网易邮箱收件人框：`fill @eN` 返回成功、observe 也显示 `[filled]`，**但截图一看是空的**——React 受控组件不认程序写入的 `.value`。

**正确做法：用 evaluate 走原生 setter + 触发事件。**

```sh
bsk evaluate "(()=>{const el=document.querySelector('<CSS>');if(!el)return 'NF';
const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
s.call(el,'要输入的值');
el.dispatchEvent(new Event('input',{bubbles:true}));
el.dispatchEvent(new Event('change',{bubbles:true}));
el.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:13,bubbles:true}));
return el.value})()" --session "$SID" > /d/tmp/ev.json 2>&1
```

- 富文本正文（contenteditable）不能这样 set，用 `fill @eN` 一般有效。
- 先探测选择器别猜：
  ```sh
  bsk evaluate "document.querySelector('input[placeholder*=收件人]')?.className||'NF'" --session "$SID"
  ```
- **每次 evaluate 后必须截图确认真的填进去了**，别信返回值。

### 4.2 原生弹窗（confirm/alert）：JS 摸不到，用 Enter

实测「确定真的不需要写主题吗？」弹窗：DOM 里 `querySelectorAll` 查不到「确定」，evaluate 返回 `[]`——**它是浏览器原生 dialog**。

- **首选：`bsk press Enter --session "$SID"`**（默认焦点在确定键，实测一击即中）。
- 若 Enter 无效，用 `request-help` 交给人：
  ```sh
  bsk request-help --session "$SID" --prompt "请点击弹窗的「确定」按钮"
  ```

### 4.3 坐标系陷阱

同一个页面可能同时存在两个坐标层：Agent Window 层 与 用户窗口层。表现：
- 对 `@e30`（发送按钮）`click` 成功 → 实际生效
- 对 `@e37`（收件人框）`click` 失败 → `operation denied by Agent Window sandbox` + `element not visible`

**判断法**：`tab list --scope all` 看该标签属于哪个 scope。user scope 未 borrow 的元素会走到「拒绝」；已 borrow 或 agent scope 的才可点。**遇到 denied 不要换 selector 硬试，先补 borrow。**

---

## 5. 验证（必做，不能省）

**发送/提交类动作，必须找到独立成功信号，不能以「点了按钮」为完成。**

| 任务 | 独立成功信号 |
|---|---|
| 发邮件 | 页面出现「邮件发送成功」+ 标签页 TITLE 变为「来自XXX」；或去「已发送」查到 |
| 表单提交 | 出现成功提示条 / URL 跳转 / 列表新增一条 |
| 数据抓取 | 落盘的内容非空且条数与预期一致 |

```sh
bsk screenshot --session "$SID" --out /d/tmp/verify.png >/dev/null 2>&1
```
Read 看图确认。**任何一步成功后不要再刷新或重复点**（会重复发送）。

---

## 6. 收尾

```sh
bsk session stop "$SID"     # 成功失败都要执行，会归还借用的标签
```
- 归还的标签会**留在用户窗口**，保持打开。
- 不要 stop/restart 共享 daemon 来结束任务。
- 不要用 `rm` 清理 `.bsk` 运行时文件。

---

## 7. 与用户配合的点（不可绕过）

这三件事**必须用户配合**，做之前一次性说清，别反复打断：

1. **Agent Window 别关**——那是操作通道，关了 session 立刻死。
2. **borrow 确认框**点允许——借用用户自己窗口的标签时会弹。
3. **登录/CAPTCHA/OTP**——遇到就 `request-help`，不要试图绕过。

> 若用户反复关掉 Agent Window：把「session start → 借标签 → 动作」压进**单次 Bash 调用**，把窗口存活期缩到最短。

---

## 8. 完整范例：用已登录的网易邮箱发一封邮件

```sh
P="/c/Users/26719/.workbuddy/binaries/PortableGit/versions/1.2.0/usr/bin"
export PATH="$P:$PATH"; export BSK_AUTO_START=0; T=/d/tmp; mkdir -p $T

# ① 常驻 daemon（用 run_in_background=true 提交这一条）
bsk daemon start --foreground

# ② 起 session + 找标签（一条命令，别拆）
BID=$(bsk browsers 2>/dev/null | sed -n '2p' | awk '{print $1}')
bsk session start --json --browser "$BID" > $T/s.json 2>&1
SID=$(sed -n 's/.*"session_id": "\([a-z]*\)".*/\1/p' $T/s.json); echo "SID=$SID"
bsk tab list --scope all --session "$SID" > $T/tabs.txt 2>&1

# ③ 借用邮箱标签（用户窗口的固定标签）
TB=$(grep -i "163\|mail" $T/tabs.txt | head -1 | awk '{print $1}')
bsk tab borrow $TB --session "$SID" > $T/borrow.txt 2>&1
bsk tab select $TB --session "$SID" >/dev/null 2>&1
bsk observe --session "$SID" --max-tokens 2500 > $T/obs.txt 2>&1
# → 读 obs.txt 找到「写 信」按钮的 @eN

# ④ 点写信 → observe → 填收件人（JS setter）→ 填正文（fill）→ 发送
bsk click @eNN --session "$SID" >/dev/null 2>&1; sleep 3
bsk evaluate "(()=>{const el=document.querySelector('.nui-editableAddr-ipt');
const s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
s.call(el,'receiver@163.com');
el.dispatchEvent(new Event('input',{bubbles:true}));
el.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',keyCode:13,bubbles:true}));
return el.value})()" --session "$SID" > $T/ev.json 2>&1
bsk fill @eBODY --value "正文内容" --session "$SID" >/dev/null 2>&1
bsk screenshot --session "$SID" --out $T/before_send.png >/dev/null 2>&1   # ← 必须看一眼

bsk click @eSEND --session "$SID" >/dev/null 2>&1; sleep 3
bsk press Enter --session "$SID" >/dev/null 2>&1; sleep 2                  # ← 空主题确认弹窗
bsk screenshot --session "$SID" --out $T/after_send.png >/dev/null 2>&1    # ← 确认「邮件发送成功」

# ⑤ 收尾
bsk session stop "$SID"
```

---

## 9. 速查：症状 → 处置

| 症状 | 根因 | 处置 |
|---|---|---|
| bsk 命令无输出 + SIGTERM | daemon 被宿主回收 | 用 `run_in_background` 常驻启动 daemon |
| `dirname: command not found` | PATH 缺 coreutils | 命令前缀补 PortableGit `usr/bin` |
| `session not registered or already stopped` | Agent Window 被关 | 重开 session，把后续步骤并进同一命令 |
| `multiple_browsers_online` | 多个浏览器实例 | `session start --browser <id>` |
| `operation denied by the Agent Window sandbox` | 操作用户窗口标签但未借用 | `tab borrow <TAB_ID>` |
| fill 成功但字段还是空 | React 受控组件 | 改用 evaluate 原生 setter + 事件 |
| 点发送没反应 | 原生确认弹窗挡住 | `bsk press Enter` |
| 邮箱页只显示登录页 | agent 标签冷启动 / 站点按窗口隔离 | 2026-09-20 实测 agent 标签**共享 cookie**（agent 标签 navigate 到 mail.163.com 直接是已登录态）。先试 agent 标签 navigate，被拦再 borrow |
| `evaluate` 返回 `NF`，但 `observe` 明明列出了那个按钮 | JS 只在顶层 document 跑；或 `innerText` 带换行导致 `===` 不成立 | 见 §10.2：钻 `iframe.contentDocument` + 比较前 `.replace(/\s+/g,'')` |
| `screenshot` 报 `write screenshot to ...: 系统找不到指定的路径 (os error 3)` | `--out` 用了 MSYS 路径 `/d/tmp/x.png` | 改用 Windows 路径 `--out "D:\tmp\x.png"` |
| 浏览器起来几秒后又断开（daemon 日志 `browser disconnected`） | 浏览器是前台 Bash 调用的子进程，调用结束被宿主连带杀掉 | 见 §10.1：放进 `run_in_background` 常驻任务里启动 |
| `CREATE_BREAKAWAY_FROM_JOB` 报 `WinError 5 拒绝访问` | job 不允许逃逸 | 逃不掉，只能靠常驻任务续命 |
| `tasklist` 说没有 msedge.exe，但浏览器明明在用 | 本沙箱的进程枚举看不到用户进程 | **以 `bsk status` 的 `browsers` 为准**，不要用 tasklist 判断浏览器是否在跑 |
| 连不上 / daemon 起不来 | 扩展未连或 daemon 缺失 | `bsk status`；缺失就常驻启动，未连就让用户开浏览器 |

---

## 10. 实战补充（2026-09-20 · 网易邮箱授权码全流程跑通）

### 10.1 浏览器没开时，由 Agent 自己拉起来
- 先看 `bsk status` 的 `browsers`；为空 = 扩展没连。**`tasklist` 在本沙箱里看不到 `msedge.exe`，不要用它判断浏览器是否在跑**，以 bsk 状态为准。
- 拉起浏览器必须放在 **`run_in_background: true` 的常驻任务**里：`python 脚本 → Popen(msedge.exe, --profile-directory=Default, URL) → while True: sleep(60)`。
  - 放在前台 Bash 里 Popen，调用一结束浏览器就被宿主连带杀掉（实测 Edge 连上 bsk 17 秒后日志出现 `ws read error / browser disconnected`）。
  - `CREATE_BREAKAWAY_FROM_JOB` 在本环境**失败**（`WinError 5 拒绝访问`），逃不出 job。
- 常驻脚本**不要写"退出就重启"逻辑**：否则用户手动关掉浏览器后会被每 30 秒重新弹出来。

### 10.2 evaluate 只作用于顶层文档：跨 iframe 要自己钻
`bsk evaluate` 的 JS 在**顶层 document** 执行，而 `bsk observe` 会把 iframe 内容一起列出来 —— 于是出现「observe 能看到按钮，evaluate 却返回 `NF`」的假象。
163 设置页所有弹窗（继续开启 / 短信验证 / 授权码）都在同源 iframe 里，必须这样写：

```js
(function(){
  var fs=[].slice.call(document.querySelectorAll('iframe'));
  for(var i=0;i<fs.length;i++){
    var d=null; try{d=fs[i].contentDocument}catch(e){continue}
    if(!d) continue;
    var c=[].slice.call(d.querySelectorAll('button,a,div,span,strong'))
      .filter(function(e){return (e.innerText||'').replace(/\s+/g,'')==='目标文字'});
    if(c.length){
      var el=c.filter(function(e){return e.tagName==='BUTTON'})[0]||c[c.length-1];
      ['mouseover','mousedown','mouseup','click'].forEach(function(t){
        el.dispatchEvent(new MouseEvent(t,{bubbles:true,cancelable:true,view:window}))});
      return 'clicked F'+i+':'+el.tagName;
    }
  }
  return 'NF';
})()
```
三个要点：① 遍历 `iframe.contentDocument`（必须同源）；② 比较文字前 `.replace(/\s+/g,'')`，否则 `innerText` 里的换行让 `===` 永远不成立、白返回 `NF`；③ 元素经常拿不到 `@eN` ref（如绿底「继续开启」只是个 `strong`），JS 派发整套鼠标事件比 ref 更管用。

### 10.3 没有 ref 的元素怎么点
有 ref 就 `bsk click @eN`；没 ref 就在（正确的）document 里找 `tagName==='BUTTON'`，找不到就取最内层节点派发事件。别靠截图目测坐标硬点。

### 10.4 screenshot 的 `--out` 必须用 Windows 路径
`--out /d/tmp/x.png` → `write screenshot to /d/tmp/x.png: 系统找不到指定的路径 (os error 3)`。
改用 `--out "D:\tmp\x.png"`。落盘后用 Read 看图，这是判断页面真实状态最可靠的手段（判断弹窗遮不遮、字段填没填进去，全靠它）。

### 10.5 网易邮箱 163 授权码全流程（已跑通）
1. 打开 `mail.163.com`（agent 标签即可，cookie 与用户窗口共享，直接是已登录态）。
2. 顶部「设置」是 `<a href="javascript:;">`，**单纯 `.click()` 不生效** → 派发 `mouseover/mousedown/mouseup/click` 一整套才会展开下拉。
3. 下拉里的「POP3/SMTP/IMAP」也没有 ref → 顶层文档里按文字匹配 `li` 后同样派发事件。成功后 URL hash 变为 `#module=options.LinkModule%7C%7B%22link%22%3A%22option_pop3%22%7D`。
4. 设置正文在 iframe `https://mail.163.com/html/authcode/index.html` 内。「IMAP/SMTP服务」后的「开启」在 observe 里是 `@eN button "IMAP/SMTP服务 | 已关闭 开启"`，可直接 click。
5. 弹「账号安全提示」→ 点「继续开启」（无 ref，走 §10.2）。
6. 弹短信验证 → **必须人来**：`bsk request-help --session $SID --title "..." --prompt "把手机 xxx 收到的 6 位验证码填进页面输入框再点验证" --timeout 5m`。用户完成后返回 `outcome=continued`，流程自动接上，不用重新起 session。
7. 授权码弹窗出现后**从 DOM 精确取，别用截图 OCR**（0/O、l/1 易混）：
   ```js
   iframeDoc.body.innerText.match(/[A-Za-z0-9]{16}/g)   // 命中 div.authcode-text-with-copy
   ```
8. 点弹窗「确定」落库，再回读 iframe 文本确认 `IMAP/SMTP服务 已开启`。
9. 授权码**只显示一次**，拿到立刻写进本地配置再往下走。

### 10.6 收尾
- `bsk session stop $SID`。
- 借过的标签才需要 `tab return`；**borrow 超时/没借成功就不用管**，标签本来就还在用户窗口。
- 常驻的浏览器托管任务和 daemon 任务留着，别 stop/restart daemon。

---

## 11. 站点适配器执行位（bb-sites 范式，来自 bb-browser/bb-sites 方法论）

browser-automation §八 定义的站点适配器（一个 JS 函数、页内 eval、返 JSON）在本技能的执行位就是 `bsk evaluate`。映射：

- **T1（仅 Cookie）**：`bsk evaluate "fetch('/api/x?q='+encodeURIComponent('...'),{credentials:'include'}).then(r=>r.json())" --session $SID` 直出 JSON。
- **T2（Bearer+CSRF）**：evaluate 里从 `document.cookie` 取 `ct0` 等 token，拼 `headers` 后 fetch。
- **T3（签名）**：evaluate 里取 `__vue_app__.$pinia._s.get('store')` 调 store action，或拦截 `XMLHttpRequest` 抓 response（见 browser-automation §八 决策树）。
- **逆向抓包**：bsk CLI 未直接暴露 `network --with-body`；要逆向站点 API，走 Edge/Chrome DevTools 的 Network 面板，或用 CDP `Network.enable` 抓请求/响应体，再据此写适配器。**不要为抓包而开远程调试端口**。

**私有适配器收纳**：`~/.workbuddy/browser-adapters/<platform>/<command>.js`（同名覆盖，含登录态/私有站点，不入仓）。执行前先 `bsk tab borrow` 借到带登录态的用户标签（见 §2），用完 `tab return`。
