# r795H｜CI｜缓存复用 KV：CacheBlend 让非前缀块也能复用，代价是选择性重算

访问日期：2026-11-22。每轮独立实拉，禁止复用上轮结论。

## 一手来源逐字

- https://arxiv.org/abs/2405.16444（Yao 等，arXiv:2405.16444，2024-05-26，WebFetch 200 逐字：非前缀不可用原因 / selectively recomputes / TTFT 2.2-3.3× 与吞吐 2.8-5×）

- https://arxiv.org/html/2405.16444v3（WebFetch 200 逐字：HKVD top-k 偏差选择 / 15% tokens 时 KV 加载掩盖重算）

- https://github.com/LMCache/LMCache（作者一手仓库，WebFetch 200 逐字：Non-prefix KV reuse / KV 从临时态变可持久复用知识 / 适用 RAG 与多轮）

## 独有点

1. 非前缀判据：A/B 对照——同一文档块分别置于 prompt 位置 0 与 k>0，两次都应命中缓存；若 cache key 含「必须是公共前缀」约束则不合格。论文逐字：reused chunks「are not always the input prefix…ignore the text's cross-attention with the preceding texts」；引用必须是 `arXiv:2405.16444`（真实标题 CacheBlend: Fast Large Language Model Serving for RAG with Cached Knowledge Fusion），不得写 2501.xxx。

2. 选中即重算：命中后不能直接拼 KV，须按「新算 KV 与载入 KV 的逐 token 偏差」降序取 top-k（HKVD tokens）重算，其余复用；论文给出 15% tokens 时 KV 加载可掩盖重算延迟，机检 `recompute_tokens/total_tokens ≤ 0.15` 为零额外延迟候选，但跨模型/硬件须实测 TTFT，不能当普适常数。

3. 场景判据：多文档 RAG、多轮共享参考、长上下文 agentic 才需要非前缀复用；固定单前缀场景用 prefix caching 即可。论文报 TTFT 降 2.2–3.3×、吞吐升 2.8–5×（不牺牲生成质量），这是原论文设定下的结果，不迁移成本仓验收阈值。

## 判重与判非

- 判重：`CacheBlend` 本体仅 §r751B 前缀缓存判非句出现，无专节；与 §前缀缓存、§context editing、§KV 量化分工不复用。豆包自留地 `wb-context-compressor` WB 0 落地。ID 纠错：真实 arXiv:2405.16444，v1 2024-05-26。

- 抓取失败：题面猜测 ID arXiv 2501.xxx 不存在，已核实纠正；dblp 记录页 Anubis 反爬，未采用。
