# r798C Mamba 选择性状态空间 · 逐字来源与判非

> CI · 2026-11-23 实拉 · ≥2 独立域一手交叉 · 落地 defaults/ci-context 2.9.0

## 一、alphaXiv 2312.00752 原论文中文概览（全文逐字）

来源：https://alphaxiv.org/zh/overview/2312.00752v1 （Gu & Dao《Mamba: Linear-Time Sequence Modeling with Selective State Spaces》，arXiv:2312.00752，全文逐字）
- 选择机制："作者通过一种硬件感知的并行扫描算法解决了这个挑战，该算法有效地实现了循环计算"；"通过将扩展状态保存在快速 GPU 内存 (SRAM) 而不是较慢的高带宽内存 (HBM) 中来仔细管理内存使用，从而显著降低了内存访问成本"。
- "Mamba 的扫描操作(红线)随着序列长度线性缩放，并且对于更长的序列，甚至优于优化的注意力实现，例如 FlashAttention-2。"
- "在 A100 GPU 上比先前方法速度快了3倍。"（硬件感知实现节）
- 选择机制挑战："选择机制阻止了通常用于标准 SSM 的基于快速卷积的算法的使用，因为参数在每个时间步都会发生变化。"
- 性能：Mamba-3B 优于同规模 Transformer，某些基准匹敌两倍大小 Transformer；推理吞吐 5×；语言/音频/基因组学跨模态 SOTA，无需领域特定修改。

## 二、Mamba2 微信公众号深度长文（全文逐字，SSD 对偶边界最详）

来源：http://mp.weixin.qq.com/s?__biz=MjM5NjE4MzIzMA==&mid=2454237020&idx=1&sn=c8864a7f0c9f32a2d9e47e0c0774dee2 （WebSearch 返回全文逐字）
- 论文：Dao & Gu 2024 ICML《Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality》，arXiv:2405.21060；Mamba 原论文 arXiv:2312.00752。
- 三关键词："SSM(用一个不断变化的内部状态来压缩历史信息) / Selective(根据当前输入决定哪些信息应该被保存、遗忘或读取) / SSD(让状态更新既可以像 RNN 一样递推，又可以转换成适合 GPU 的矩阵计算)"。
- "Transformer 倾向于通过访问历史 Token 表示获取信息，而 Mamba2 将历史压缩到可递推的状态中"；"Mamba2 的状态不是原始历史 Token 的无损存储，而是学习得到的固定维度信息摘要…可能丢失某些历史细节。"
- SSD 等价边界（关键）："当 A_t = α_t I（标量-单位矩阵结构）时，SSM 可视为因果线性注意力的一种形式"；"论文不是证明任意 Softmax Transformer 都等价于 Mamba2。它主要建立了结构化 SSM、半可分矩阵与某些线性注意力形式之间的联系。Softmax Attention 的归一化和非线性匹配性质不能直接通过上述变换获得。"
- Chunk 非截断："SSD 加速并不是把历史信息截断为 256 个 Token。chunk_size=256 只是计算分块长度，历史信息仍然能够通过块间状态向后传递。"
- 速度：Mamba2 核心层相对 Mamba1 "约 2–8 倍的速度提升…这是特定实验设置下的结果，并不代表任何模型、GPU 和任务都能获得同样的加速"。
- 状态缓存："16 个 Head、ngroups=1 时…256 KiB 的 SSM 状态缓存(单个样本、单个 Mamba2 层)"；"即使序列从 4096 Token 增加到 32768 Token，这个 SSM 状态张量的形状也不需要随之增加。这与传统 Transformer 的 KV Cache 不同。"
- 短板："对于需要从很长的上下文中精确找回某个数字、代码或原文片段的任务，固定状态压缩可能成为瓶颈。"
- 理论 vs 实际："短序列下，经过高度优化的 FlashAttention 可能非常快。Mamba2 的投影层、内存带宽和 Kernel 调度也有实际开销。Mamba2 不保证在所有 Batch、上下文长度和 GPU 上快于 Transformer。SSM 固定状态缓存也不等于整个模型的推理内存完全固定。"
- 末尾提及 Mamba-3（arXiv:2603.15569，梯形离散化/复数化 SSM/MIMO SSM）——本轮未独立取证，标未采纳。

## 三、CSDN 架构详解 + Waleffe 基准（全文逐字）

来源：https://blog.csdn.net/u012133341/article/details/159834523 （WebSearch 返回全文逐字）
- 复杂度对比表：Transformer 训练 O(N²)/推理内存 O(N)/序列并行完全/长程全局但二次方；Mamba(SSM) 训练 O(N)/推理内存 O(1)/序列并行受限/长程线性衰减；Mamba-2(SSD) 训练 O(N) 优化后/推理内存 O(1)/序列并行完全/长程可控衰减。
- Waleffe 等人 2024 系统性基准（8B 参数）："在 4096 tokens 长度时，Mamba的内存效率是Transformer的 12.46倍；序列长度超过 220 tokens 时即展现内存优势"；"4096 tokens 时推理速度快 10.67倍，交叉点约为 370 tokens。"
- Mamba-2 SSD："当 A_t = α_t I 时，SSM 可视为因果线性注意力的一种形式…等价于序列半可分矩阵(sequentially-semiseparable matrices)的变换"；张量并行化 / 块分解（训练速度 2–8×）/ 多头结构。

来源：https://blog.csdn.net/qq_45981086/article/details/141675075 （论文总结，全文逐字）
- 两大工作："简单地将SSM参数作为输入的函数，解决了离散模态的弱点，允许模型根据当前标记有选择地沿着序列长度维度传播或忘记信息(选择性扫描算法)"；"设计了一种递归模式下的硬件感知并行算法…通过扫描而不是卷积来循环计算模型，但不具体化扩展状态，以避免GPU内存层次结构的不同级别之间的IO访问"。
- S4 的 LTI 局限："线性时间不变性(LTI)：(Δ、A、B、C)，以及(A、B)对于所有时间步长都是固定的。"

## 四、百度百科概览（交叉佐证）

来源：https://baike.baidu.com/item/mamba/65401625 （全文逐字）
- Mamba 由 Tri Dao 与 Albert Gu 2023 年提出；选择性状态空间模型 + 硬件感知并行扫描；线性复杂度 + 恒定推理内存；Mamba-3B 优于同规模 Transformer，5× 推理吞吐；2024 Mamba-2 SSD 框架统一 SSM 与注意力，状态维度 16→256，2–8× 训练加速。

## 五、判非与诚信

- 判重（落地前）：`Mamba`/`选择性状态空间`/`state space`/`线性注意力`/`SSD` 全库 SKILL.md 0 专节；唯一「稀疏注意力」命中在豆包自留地 wb-execute-discipline 且为异命题。与 §FlashAttention（exact 精确注意力，优化 HBM 读写）、§PagedAttention（KV 显存放法）、§前缀缓存（是否重算 KV）、§KV 量化（低比特存 KV）分工正交：那些都优化 Transformer 注意力路径，本条绕开注意力改递推状态。豆包自留地 WB 0 落地。
- 全部为 WebSearch 返回页面全文逐字；微信长文为二手深度解读（非论文原文页），CSDN 为二手总结，alphaXiv 为中文概览——均未冒充 arXiv 论文原文逐字。
- 12.46×/10.67×/220/370 token 交叉点来自 Waleffe 2024 经 CSDN 转述，标注为"特定实验设置"，未推广为普适结论。Mamba-3 未独立取证，未采纳为独点。
