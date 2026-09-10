---
name: github-ssh-over-443
description: >-
  GitHub 连不上 / git push 超时 / GitHub 打不开时用 SSH over 443 绕过。当出现以下情况时应用：`git push` 报 `Failed to connect to github.com:443`、clone/fetch 卡住无响应、github.com 网页打不开、为推代码反复启动 VPN、需要给 GitHub 配置免翻墙访问。核心判断：HTTPS(443) 被 TLS SNI 检测阻断，而 SSH 协议不带 SNI 所以放行——改 remote 为 SSH 即可直连，多数情况根本不需要 VPN。也适用于判断"到底是网络被封还是认证没配好"。
version: 1.0.0
---

# github-ssh-over-443（GitHub 访问被打断时的直连解法）

来源：2026-09-10 实测（用户环境：Windows，github.com 的 HTTPS 长期超时，一直在用 VPN 推代码）。

## 诊断：先分清是"被封"还是"没认证"
两条命令，30 秒出结论：
```bash
# 1. HTTPS 路径
timeout 20 curl -sS -o /dev/null -w "HTTPS: %{http_code} %{time_total}s\n" --max-time 15 https://github.com

# 2. SSH 路径（无 key 也会走到认证阶段，那就是通了）
timeout 20 ssh -T -o BatchMode=yes git@github.com 2>&1 | tail -1
```
判读：
- HTTPS 超时/HTTP 000，SSH 返回 `Permission denied (publickey)` → **网络通，只是没配密钥** → 按下面做即可
- SSH 返回 `Connection timed out` → SSH 也被阻断，才需要用 VPN
- 两边都超时 → 真·断网或被全面封锁

**关键**：`Permission denied (publickey)` 是好消息，不是失败。它意味着 TCP 连上、SSH 握手完成、服务器只是不认识你。

## 为什么 SSH 能过、HTTPS 不能
封锁基于 **TLS SNI 检测**：HTTPS 握手时客户端明文发送要访问的域名（SNI），检测器看到 `github.com` 就阻断。SSH 协议不是 TLS、不发送 SNI，检测器认不出它在连谁，因此放行。
实测数据（2026-09-10）：`github.com:443` HTTPS 超时 20s ❌；`github.com:22` SSH ✅；`ssh.github.com:443` SSH ✅（3/3 稳定）。

## 解决（一次性配置，约 1 分钟）
1. **生成密钥**（无 passphrase 才能无人值守推送）：
   ```bash
   ssh-keygen -t ed25519 -C "备注名" -f ~/.ssh/id_ed25519 -N ""
   ```
2. **写 `~/.ssh/config`**，让 github.com 自动走 443（22 端口可能被单独封）：
   ```
   Host github.com
     HostName ssh.github.com
     Port 443
     User git
     IdentityFile ~/.ssh/id_ed25519
     IdentitiesOnly yes
   ```
3. **把公钥加到 GitHub**（唯一需要人工的一步）：`cat ~/.ssh/id_ed25519.pub`，粘贴到 https://github.com/settings/ssh/new
4. **改 remote**：
   ```bash
   git remote set-url origin git@github.com:<用户名>/<仓库>.git
   ```
5. **验证**：`ssh -T git@github.com` 应返回 `Hi <用户名>! You've successfully authenticated`；随后 `git push` 应一次成功。

## 注意
- **HTTPS + token 方案无效**：token 也要走被阻断的 443 TLS 通道，绕不过去。
- **SSH 仍可能被间歇阻断**：不是绝对保险。真断了再上 VPN。
- **passphrase 的取舍**：设了更安全，但自动化/无人值守推送会失败。要自动化就别设，代价是能访问该机器的人就能用它推送。
- **私钥绝不入仓**：`.gitignore` 加 `.ssh/`、`id_ed25519*`；只外传 `.pub` 公钥。
- **切换前先确认没有其他 remote 依赖 HTTPS**：`git remote -v` 全看一眼。

## 反模式
- 一直重试 HTTPS → 封的是协议特征，重试一万次也不会通，纯浪费时间
- 为 push 反复启停 VPN → 多数情况 SSH 直连就够；本类 VPN 常只能起进程、无法自动建隧道
- 每次 push 失败就放弃、不做一次性修复 → 同样是每天浪费一次超时
- 把私钥或含密钥的 config 提交进仓库
