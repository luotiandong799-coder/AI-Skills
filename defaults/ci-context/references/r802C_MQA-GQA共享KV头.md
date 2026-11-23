# r802C 逐字全文与判非｜MQA/GQA 共享 KV 头｜2026-11-23 实拉

## 独点
1. KV cache ∝ KV 头数；解码 memory-bandwidth bound。MHA 每 query 一头 / MQA（Shazeer 2019）全共享单头缩 1/H / GQA（Ainslie 2023 EMNLP）分 G 组缩 H/G。实例：Llama3 70B 64 query/8 KV，2048 长 batch32 KV 20.9GB→2.6GB。
2. uptraining：每组 K/V 头 mean-pool 成一个 + 约 5% 原始预训练算力微调 → 质量近 MHA 速度近 MQA；运行时 repeat_interleave 展开 KV 回 query 头数；MQA=n_kv_heads=1、MHA=n_kv_heads=n_q_heads 特例。
3. 正交可叠加：本节改"每 token 存几个 KV 头"（训练期架构维），与 KIVI 位宽/H2O-SnapKV token 去留/vLLM 前缀块复用/分页放置不同层；可组 FlashAttention + 量化 KV；DeepSeek MLA 是"压成 latent 而非减头数"的另一解。

## 一手逐字（第一独立域）
- 来源：https://memx.app/glossary/grouped-query-attention （WebFetch 200 全文）
- "The size of this key-value (KV) cache is proportional to the number of key-value heads, so reducing those heads directly reduces memory use and the memory bandwidth that bottlenecks generation."
- "MQA collapses all key-value heads to one, cutting that part of the cache by the number of heads. GQA collapses them to a small number of groups, for example 8 key-value heads for 64 query heads..."
- "The key and value heads within each target group are mean-pooled into a single head, and the model is then briefly fine-tuned, called uptraining, using only about 5 percent of the original pretraining compute."
- 代码逐字："group = n_q_heads // n_kv_heads ... k = k.repeat_interleave(group, dim=1) ... F.scaled_dot_product_attention(q, k, v, is_causal=True) ... # MQA is the special case n_kv_heads = 1 / # MHA is the special case n_kv_heads = n_q_heads"
- "GQA also composes with other efficiency techniques. It pairs naturally with FlashAttention for faster kernels and with quantized KV caches for further memory savings. DeepSeek's Multi-Head Latent Attention can be seen as a different answer to the same KV-cache problem, compressing keys and values into a shared latent vector instead of reducing the head count."

## 一手逐字（第二独立域）
- 来源：https://arxiv.org/pdf/2407.18003v2 《Keep the Cost Down: A Review on Methods to Optimize LLM's KV-Cache Consumption》（WebSearch 全文逐字）
- "Shazeer (2019) proposed Multi-Query Attention (MQA)... even if we retain only one head for keys and values... KV-Cache space usage to 1/n_h of the original."
- "Ainslie et al. (2023) proposed GQA... divided into n_g groups... KV-Cache we need to store will be reduced to n_g/n_h. When n_g=1, we get MQA... when n_g=n_h, we get MHA."
- "LLaMA2-70B uses GQA with n_g=2, Mistral with n_g=8, and Yi with n_g=4... DeciLM-7B uses different n_g values on different layers: the first few layers are 4, then decay to 2, then to 1, and finally return to 4"
- 参数节省："ratio of savings η = 0.5 + 0.5 · (1 + n_g/n_h)"

## 一手逐字（第三/四/五域 · WebSearch 快照交叉）
- https://www.envisioning.com/vocab/gqa-grouped-query-attention："Joshua Ainslie and colleagues at Google Research introduced it in the 2023 paper ... EMNLP 2023"；"uptraining ... about 5 percent of the original pretraining compute"
- https://aimlds.org/paper/attention-heads-are-not-equal："G = H: full MHA / G = 1: MQA / 1 < G < H: GQA. Near-MHA quality at near-MQA speed"；"Llama 3 70B: 64 query heads, 8 KV heads. The KV cache reduction is exactly 8x. At a sequence length of 2,048 tokens with a batch of 32 ... 20.9 GB and 2.6 GB"；"increasing the number of groups from MQA only results in modest slowdowns initially"
- https://ai360xpert.com/papers/gqa：GQA-8 32 query/8 KV 示意；LLaMA 1→2(70B)→3、Mistral、Gemma 采用；MLA 对照

## 判非（去重五层）
- ci-context 本体 `MQA`/`GQA` 仅 §r783B 一句成本公式因子提及（"MQA 把 Hkv 压到 1、GQA 分组共享 8B 32query/8KV=1/4 成本"），非机制专节；本轮补独立条目并显式分工（那句讲放置维、本条讲头数维）。
- `多查询注意力`/`分组查询`/`uptraining`/`mean-pool` 全库 0 专节；其余命中在豆包自留地 wb-context-compressor KB、wb-execute-discipline KB、co-learn r783B、采购无关域——WB 0 落地。
- 与 §r775B KIVI（位宽）/§r767B H2O-SnapKV（token 去留）/§r751B+§r783B（块级前缀缓存+放置）/§r798C Mamba（换递推状态）正交不复用。
- 数字挂可复拉 URL；arXiv 综述/术语站为二手转述一手论文结论，已登记未冒充论文逐字；未采纳 GQA 论文原文逐字（未直接取 paper PDF 正文）。
