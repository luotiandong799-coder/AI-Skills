# 安装使用步骤（同事极简上手）

> 目标：在你自己的电脑上，把 WorkBuddy 的任务结果推送到**你自己的微信**。
> 前提：已安装 WorkBuddy 桌面端，且微信里能看到一个名为 ClawBot 的机器人（即你已在 WorkBuddy 绑定了微信通道）。

---

## 第一步：安装 Skill

两种方式任选其一：

- **技能市场（推荐）**：在 WorkBuddy 技能管理界面搜索 `wechat-clawbot-push` 安装，或点击"添加技能 → 上传技能"，选择本技能的 zip 包。
- **手动放置**：把整个技能文件夹复制到 WorkBuddy 的 skills 目录：
  - 个人级（推荐，所有项目可用）：`~/.workbuddy/skills/wechat-clawbot-push/`
  - 项目级（仅当前项目）：`<你的工作区>/.workbuddy/skills/wechat-clawbot-push/`

安装后目录结构应类似：
```
wechat-clawbot-push/
├── SKILL.md
├── scripts/
│   └── wechat_clawbot_push_mcp.py
└── references/
    └── install.md
```

---

## 第二步：让 WorkBuddy 注册连接器

打开 WorkBuddy 对话，直接对 AI 说（可整句复制）：

> 帮我在 ~/.workbuddy/mcp.json 里注册一个 stdio 连接器 wechat-clawbot-push，
> command 用 python3，args 为 [本机 wechat_clawbot_push_mcp.py 的绝对路径, "--mcp"]。
> 脚本在 ~/.workbuddy/skills/wechat-clawbot-push/scripts/wechat_clawbot_push_mcp.py。

注册完成后，去 **WorkBuddy → 连接器管理 → 找到 wechat-clawbot-push → 点 Trust 启用**。

---

## 第三步：首次授权（每台电脑一次）

iLink 是回复型协议，必须先让 bot 拿到你的"对话凭证"：

1. 打开**手机微信**，给这个 ClawBot 发**任意一条消息**（例如"你好"）。
2. 在 WorkBuddy 对话里让 AI 调用 `acquire_token()` 工具，或自己运行：
   ```bash
   python3 ~/.workbuddy/skills/wechat-clawbot-push/scripts/wechat_clawbot_push_mcp.py --acquire
   ```
3. 看到"已获取并缓存 context_token"即成功。

---

## 第四步：开始推送

之后随时在对话里说：

> 把刚才的结论用微信推送到我手机。

或让自动化任务调用：

> 调用 wechat-clawbot-push 连接器的 push_wechat_message 工具，text 写"xxx 已完成"。

---

## 常见问题

| 现象 | 处理 |
|---|---|
| 提示 `尚未获取 token` | 回到第三步，先去微信给 bot 发消息再 `acquire_token()` |
| 提示 `TOKEN_EXPIRED` | token 失效，重新发消息 + `acquire_token()` |
| 推了但微信没收到 | 确认连接器已 Trust、WorkBuddy 在运行、微信在线 |
| 想群发团队通知 | 本通道是个人微信，建议改用企业微信 Webhook |

---

## 安全提示

- 脚本零第三方依赖、不联网回传，可放心使用。
- 凭证（botToken / context_token）只存在你本机 `~/.workbuddy/`，不会上传。
- 每位同事都用**自己的微信**绑定，互不影响。
