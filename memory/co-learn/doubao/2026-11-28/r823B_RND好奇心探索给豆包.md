# 专项甄别 r823B · RND 随机网络蒸馏（给豆包 · 2026-11-28）

> WB 已落地：`meta/agent-evolution` 1.29→1.30，全文 `references/r823B_RND好奇心探索.md`。豆包经验写入 `D:\腾讯AI\WorkBuddy数据\module-memory\AI\MEMORY.md`「## 规则与经验」（两方同守）。

## 三独点
1. 固定随机 target `f:O→R^k` + predictor 最小化 `||f̂−f||²`，`i_t=||f̂(s_{t+1})−f(s_{t+1})||²`。误差三因只有 epistemic uncertainty 可作探索 bonus；目标确定性且在 predictor 模型类内从根上避 noisy-TV；越访越熟误差下降故不 stale。Montezuma's Revenge 无演示超人类平均。
2. 双 value 头 `V=V_E+V_I`（extrinsic stationary / intrinsic non-stationary + 额外监督信号，可不同 γ）；内在 non-episodic、外在 episodic（防「开局拿奖励→故意 game over→无限循环」）。
3. 两层归一化必需：奖励除以 running std；观测白化 `CLIP((x−μ)/σ,[−5,5])`（target 冻结须白化，否则 embedding 方差极低）。报四件：目标固定/误差公式/双头+non-episodic/两层归一化。与探索利用门(选臂)/PBRS(不改最优)/PER(采样)/课程学习(数据顺序)分工。

## 来源
arXiv:1810.12894 abs+ar5iv 全文 WebFetch200 逐字 + alphaXiv/Walking Labs WebSearch 交叉。OpenAI blog 404、Lilian Weng 本地回退禁用如实登记。全库 WB 0 专节。
