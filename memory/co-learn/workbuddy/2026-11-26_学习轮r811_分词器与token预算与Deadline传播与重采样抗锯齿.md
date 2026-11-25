# 学习轮 r811（A/B/C）｜分词器与 token 预算 · Deadline 传播 · 重采样与抗锯齿（WorkBuddy · 2026-11-26）

- 轮号：r811A/B/C（上批 r810A/B/C；co-learn r767–r810 续读无跳；Qoder 已卸载，共学两写 WB/豆包，qoder 目录 0 写入）。遵用户 2026-11-25 追加指令「13 模块固定顺序轮转」（KI 论文域排除，按 12 模块 4 组），本批取 CI/OI/PI，避开 r810 VI/RI/MI；除非另行取消不得提前停止或缩减。
- 五层判重：全库 SKILL.md + module-memory + co-learn + references 对 `BPE`/`byte fallback`/`SentencePiece`/`tokenizer`、`deadline propagation`/`剩余预算`/`DEADLINE_EXCEEDED`、`重采样`/`resampling`/`Lanczos`/`Nyquist` 在对应模块本体均 0 机制专节；CI 仅 §r742B「按 token 数建 haystack」+§r763B「用目标模型 tokenizer 重数」两条纪律性提及，OI 仅 §r807B 一句 PM deadline，PI 仅 §r750B 一句 FID resize 实现差异 + §r732A 一句预缩放。豆包自留地 `wb-execute-discipline`/`wb-context-compressor` WB 0 落地。按 rules/07「增＝加厚现有」，0 新建 / 0 合并 / 0 删除。
- 落地：3 轮 / 9 独点 / 3 技能加厚 bump / 3 份 references 新建；CI 399 / OI 370 / PI 377 行（均 ≤500），desc 1020/541/984（均 ≤1024，CI 余 4 字符故 description 一字未动），CR/FFFD=0，module 3/3，来源节 3/3。
- 实拉（每轮 ≥2 独立域一手，URL+日期逐条）：A=compilenrun《WordPiece/Unigram/SentencePiece》WebFetch200 逐字（三算法对比表/byte fallback 256 token/character_coverage 0.9995/dummy prefix/六条 common mistakes）+ AI Computer Institute《Tokenizer Design》WebFetch200 逐字（▁ 可逆/Unigram 剪枝 shrinking_factor 0.75/subword regularization/byte-level 256 无 UNK/英印 27B vs 77B、2.85× floor 与复合放大）+ Belgavi Lab WebFetch200 逐字（V×d 算例 32k→128k 13% vs +197M/sublinear sweet spot）+ 中文三站 WebSearch 二手立场登记｜B=gRPC 官方 Deadlines WebFetch200 全文逐字（deadline vs timeout/client DEADLINE_EXCEEDED/server CANCELLED+应用责任/propagation 语言差异/转 timeout 扣已流逝抗 clock skew）+ zrz.io ZFN-61 WebFetch200 逐字（deadline=请求事实 vs timeout=本地猜测/27 attempts/retry inside budget/non-retryable/envelope field 逐跳递减/decrement-check-propagate-cancel/cancellation correctness+fencing/partial propagation）+ iT 邦帮忙引 Google SRE Book WebFetch200（deadline 是剩余预算非固定时长）+ grpc.io/blog + denis-darkin 交叉｜C=Pillow《Resampling filters compared》WebFetch200 逐字实测（八滤波器枚举/残留假图案与真实细节标准差/缩小放大速度/reducing_gap 167.6→55.1ms/ANTIALIAS=LANCZOS 旧名 Pillow 10 移除/MKS2013-2021/按用途选型含 ML 与 mask）+ JOVANA《影像取樣》WebFetch200 逐字（奈奎斯特–香农 2·f_max/欠采样高频伪装低频=混叠/先 band-limit/「绝不能只是丢掉像素」/SIFT-CNN 金字塔）+ TrueSight 两篇 WebSearch 二手立场登记。

## 三轮固定四列表
| 轮 | 文件 | 版本 | 独有点 |
|---|---|---|---|
| r811A | defaults/ci-context/SKILL.md | 2.12.0 | 分词器是窗口预算隐藏分母：BPE byte-level 词表锁死 256 UTF-8 字节故任何输入不 UNK（字符级 BPE 照样 UNK）、WordPiece 一未知字符整词塌 [UNK]、Unigram 自顶向下 removal loss 剪枝+Viterbi+log-prob 可采样（greedy BPE 结构上做不到）；SentencePiece 是库非算法（check model_type）、▁ 代空格+add_dummy_prefix 默认 true 使同词单独/句中首 token 不同、手剥 ▁/## 破坏 fallback 边界。byte fallback 256 个 `<0x00>`–`<0xFF>` token 拿罕见字 1→3-4 token 长度换「永不 UNK+精确往返」，character_coverage 0.9995 无 fallback 则静默 `<unk>`。多语言膨胀 2.85× 只是 UTF-8 floor（U+0800–FFFF 每码点 3 字节），真实 gap 因英语主导语料把 merge 花在 ing/tion/the 上而复合放大；V 32k→128k 仅 13% 长度降却 +197M 参数 |
| r811B | meta/personal-ai-employees/SKILL.md | 1.15.0 | deadline=请求事实、timeout=本地防御猜测；每跳独立 timeout 三层各重试 3 次=27 attempts 是设计期埋的放大。正解 edge 设一次、作 remaining budget（duration 逐跳递减+monotonic clock，非绝对时间戳）随 envelope field 传，每层从 remainder 设本地 timeout（本地猜测退化为 fallback），retry 装在预算内不叠在上面。传播抗时钟偏斜：gRPC 把 deadline 转 timeout 并扣已流逝时间（C++ 需显式/Java-Go 默认）；client DEADLINE_EXCEEDED 与 server CANCELLED 两端独立判定可不一致，deadline_exceeded 是终态不可重试。取消须 ripple down 整树+应用停衍生工作；取消正确性落幂等+fencing（mutation 被中途杀须能安全重试/放弃）；partial propagation 静默退化须审计链在哪断 |
| r811C | engineering/multimodal-intelligence/SKILL.md | 2.4.0 | 缩小=低通滤波再重采样非丢像素，最近邻缩小=欠采样：奈奎斯特 2·f_max，欠采样高频伪装虚假低频=混叠（锯齿/闪烁/摩尔纹），正确缩小先 band-limit（面积平均/高斯/光学低通）再重采样。八滤波器是混叠残留×锐度×速度三维实测：Pillow 13 缩 4× 残留假图案 NEAREST 90.8→LANCZOS 0.6、真实细节 BICUBIC 69.7/LANCZOS 79.1/MKS2013 84.3、速度 NEAREST 0.08ms→LANCZOS 14.38ms；ANTIALIAS=LANCZOS 旧名 Pillow 10 已移除，MKS2013 Pillow 13 新增；reducing_gap=3 使 167.6→55.1ms 像素差仅 3。选型看下游：ML 预处理跟训练口径（BILINEAR/BICUBIC）压过视觉更锐，mask/标签图必须 NEAREST，放大只决定填缝不加细节；库默认暗中改结论须固定并上报 |

## WB 已落地清单（防重复）
- r811A CI｜defaults/ci-context/SKILL.md 2.12.0｜分词器三独点 + references/r811A_分词器与token预算.md
- r811B OI｜meta/personal-ai-employees/SKILL.md 1.15.0｜Deadline 传播三独点 + references/r811B_Deadline传播.md
- r811C PI｜engineering/multimodal-intelligence/SKILL.md 2.4.0｜重采样与抗锯齿三独点 + references/r811C_重采样与抗锯齿.md

## 13 模块记忆体系已生效
经验按模块分存 `D:\腾讯AI\WorkBuddy数据\module-memory\<模块码>\MEMORY.md`（总入口 `00_总索引.md`，C 盘仅 junction 镜像、无实体）。豆包的对应经验也按此路由写入所属模块文件（本批 CI/OI/PI 各 3 条，格式 `- ｜日期｜来源技能｜结论｜证据/落点`），两方同守；Qoder 已于 2026-11-23 卸载，`co-learn/qoder/` 席位已移除，禁止再写该目录。用户级 MEMORY.md 保持纯指针索引（≤4000 上限结构性保障，本批未写入）。

本批为 r811A/B/C 独立实拉留痕，三轮标准一致、禁止复用 r810 结论。下批 r812A/B/C 按 13 模块固定顺序取 SI/AI/PDI（KI 论文域排除，避开 r811 CI/OI/PI）；每模块累计计数按台账续；Qoder 席位已移除仅两写。
