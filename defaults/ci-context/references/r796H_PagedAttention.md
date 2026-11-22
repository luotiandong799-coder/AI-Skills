# r796H｜CI｜KV 显存分页 PagedAttention：块表映射非连续显存，COW 共享前缀

访问日期：2026-11-22；每轮独立实拉禁止复用上轮。

## 一手来源逐字

- https://arxiv.org/html/2309.06180（Kwon 等，SOSP 2023，arXiv:2309.06180，WebFetch 200 逐字：OS 分页启发/块非连续/20.4-38.2% 利用率/消除外部碎片/块级共享）

- https://blog.vllm.ai/2023/06/20/vllm.html（vLLM 官方博客，2023-06-20，WebFetch 200 逐字：浪费 60-80%→under 4%/block table COW/reference count）

## 独有点

1. OS 类比四元组齐全：blocks=pages / tokens=bytes / requests=processes / block table 映射逻辑块→非连续物理块；判据——缺「物理块非连续」或缺 block table 不命中。论文逐字：divides KV cache into blocks … not necessarily stored in contiguous space；one can think of blocks as pages, tokens as bytes, requests as processes。

2. 数字成对出现：现有系统仅 20.4–38.2% KV 显存放真实 token 状态、浪费 60–80% → vLLM under 4%；判据——只写「零浪费」判不精确。定长块消除外部碎片，块级共享 + reference count + Copy-on-Write 让共享前缀只存一份（vLLM 官方博客逐字）。

3. 正交判据：PagedAttention 管显存放法与碎片/共享（怎么放），prefix caching 管跨请求复用已算 KV（是否重算）；判据——把两者等同或互相替代判错（论文 §6.4 shared prefix 只论证吞吐收益，官方 prefix caching 页面 404 未取一手，正交性为机制归纳按推断标注）。

## 判重与判非

- 判重：`PagedAttention` 在本体仅 r783B 未采纳句（当时判为显存产品实现未展开），无专节；与 §前缀缓存/KV 量化/FlashAttention/MemGPT 分工不复用。豆包自留地 WB 0 落地。

- 抓取失败：arXiv PDF 非文本改 HTML；docs.vllm.ai prefix caching 页 404，正交性标推断。
