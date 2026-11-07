# WorkBuddy 工程工具层（`skills/_tools/`）

> 2026-10-12 全量部署：将吸收包中「仅规则层、无底层能力」的项落地为可运行工程。
> 2026-11-07 增补：`execution_intelligence.py`（EDG / GDR / CCS，HarnessMM 思想落地）。
> 所有工具低依赖，由 personal-ai-os / 主会话按需调用。规则层单源：`rules/07 §十`。

| 工具 | 能力 | 验证 | 依赖 |
|---|---|---|---|
| `memory_tx.py` | 记忆原子写 / 版本快照 / 回滚 / 跨副本同步状态 | ✅ 已验证 | 标准库 |
| `semantic_search.py` | 本地语义检索（chromadb 向量引擎） | ✅ 真语义+降级向量均验证通过 | chromadb + sentence-transformers（modelscope 镜像已落地 `models/`，自动检测启用） |
| `model_router.py` | 任务级模型路由决策 + 子任务 `model` 参数 | ✅ 已验证 | 标准库 |
| `context_budget.py` | 上下文动态预算裁剪（优先级序） | ✅ 已验证 | 标准库 |
| `guardian_precheck.py` | 运行时安全前置检查（No-Go 路径 / L2 确认门） | ✅ 已验证 | 标准库 |
| `ocr_tool.py` | 独立 OCR 引擎壳 | ⏳ 代码就绪，依赖未装 | 系统 Tesseract 或 `pip install paddleocr` |
| `dag_scheduler.py` | 多 Agent DAG 状态机底座：依赖/就绪队列/并行分层/循环依赖检测/质量门禁/重试上限/检查点恢复 | ✅ 已验证 | 标准库 |
| `execution_intelligence.py` | EDG 编译校验 + Guard 求值 + GDR 决策复用 + CCS 执行证书账本 + Token 估算统计 | ✅ 自测 8/8 + 验收对照通过 | 标准库 |

## 诚实边界（不得宣称已解决）

1. **LocalSearch 真语义已落地**：sentence-transformers 多语言模型（paraphrase-multilingual-MiniLM-L12-v2，1.9GB）已通过 modelscope 国内镜像下载至 `skills/_tools/models/`，引擎自动检测启用，无需联网即可真语义检索（已验证排序正确）；字符 n-gram 降级向量保留作离线兜底。
2. **OCR 依赖未装**：`ocr_tool.py` 在 Tesseract / paddleocr 缺失时返回依赖缺失提示，不假装已具备能力。
3. **Model Router 主会话不自切**：仅生成路由建议 + 子任务 `model` 参数分派，受 WB 产品限制。
4. **Guardian 非进程级拦截**：规则 + precheck 形态，非系统级沙箱。
5. **执行智能引擎不代宿主跳过模型回调**：`plan` 只输出「该步是否需要模型重新判断」，真实跳过由宿主执行；`tokens_saved_estimate` 为估算口径（默认 1200 输入 + 300 输出/次），非实测计数。
6. **RSI 未实现**：自动改提示 / Guard / 配置缺独立验证集与回滚通道，按规范 P2/P3 暂缓。

## 用法

```bash
python memory_tx.py write <path> "<content>" --actor yt --note "重要更新" --source-type user --verified
python memory_tx.py list  <path>
python memory_tx.py rollback <path> [--vid V]
python memory_tx.py sync <path> <replica> <status>
python memory_tx.py status <path> [--set deprecated --reason "被取代"]
python memory_tx.py delete <path> --actor yt --reason "用户要求删除" --cascade "idx:foo,replica:bar"
python memory_tx.py dep <path> add "rules/07#M22"

python semantic_search.py <root> index  <file> [--st]
python semantic_search.py <root> search <query> [n] [--st]

python model_router.py "分析架构设计并给出多步推理方案"
python context_budget.py
python guardian_precheck.py "删除文件" "C:/Users/26719/Desktop/x"   # → deny
python guardian_precheck.py "执行支付"                              # → confirm_required

python execution_intelligence.py selftest                            # 8 组内置用例
python execution_intelligence.py compile spec.json edg.json          # 结构/权限/参数三重校验
python execution_intelligence.py plan    edg.json facts.json          # GDR 五态判定
python execution_intelligence.py certify edg.json facts.json --ledger certs.jsonl
python execution_intelligence.py run     edg.json facts.json [--apply] [--write-facts out.json]
python execution_intelligence.py stats   certs.jsonl
python execution_intelligence.py schema
```
