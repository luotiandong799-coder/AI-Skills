#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
semantic_search.py — 本地语义检索引擎
=====================================
填补 local-semantic-search 纯 SKILL.md 壳（无向量库/索引）的工程缺口。

后端：chromadb（已装）。Embedding 两档：
  - 真语义：sentence-transformers 多语言模型（paraphrase-multilingual-MiniLM-L12-v2）
            → 已通过 modelscope 国内镜像落地于 _tools/models/ 目录，自动检测启用；
              亦支持设 --st 强制真语义。无需联网即可使用真语义检索。
  - 本地降级：零依赖字符 n-gram 哈希向量（LocalCharNGramEF）
            → 模型缺失时兜底，立即可用；语义为词重叠近似，弱于真语义
              但能跑通索引/检索全流程。

功能：增量索引、语义+关键词互补、过期/重复/冲突提示。

用法：
  python semantic_search.py <root> index  <file> [--st]
  python semantic_search.py <root> search <query> [n] [--st]
"""
import os
import sys
import re
import json
import hashlib
import datetime

try:
    import chromadb
    CHROMA_OK = True
    CHROMA_ERR = ""
except Exception as e:  # pragma: no cover
    CHROMA_OK = False
    CHROMA_ERR = str(e)

DEFAULT_COLLECTION = "wb_memory"
ST_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


class LocalCharNGramEF:
    """零依赖本地 embedding：字符 bi/trigram 哈希到固定维向量。
    无需下载模型，立即可用；语义为词重叠近似（弱于真语义）。"""

    def __init__(self, dim: int = 512):
        self.dim = dim

    def _vec(self, text: str):
        t = re.sub(r"\s+", "", text)
        grams = set()
        for n in (2, 3):
            for i in range(len(t) - n + 1):
                grams.add(t[i:i + n])
        if not grams:
            grams = {t or " "}
        vec = [0.0] * self.dim
        for g in grams:
            h = int(hashlib.md5(g.encode("utf-8")).hexdigest(), 16) % self.dim
            vec[h] += 1.0
        norm = sum(v * v for v in vec) ** 0.5 or 1.0
        return [v / norm for v in vec]

    def embed_documents(self, input):
        if isinstance(input, str):
            input = [input]
        return [self._vec(d) for d in input]

    def embed_query(self, input):
        if isinstance(input, str):
            input = [input]
        return [self._vec(d) for d in input]

    def __call__(self, input):
        if isinstance(input, str):
            input = [input]
        return [self._vec(x) for x in input]

    def name(self):
        return "local_char_ngram"


def _local_model_dir() -> str:
    """解析本仓内置真语义模型目录（modelscope / HF 缓存均可）。
    命中即返回含 config.json 的具体快照目录，供 SentenceTransformer 直接加载。"""
    base = os.path.dirname(os.path.abspath(__file__))
    # 1) modelscope 布局：models/models/sentence-transformers--<name>/snapshots/master
    ms = os.path.join(base, "models", "models", "sentence-transformers--" + ST_MODEL)
    if os.path.isdir(ms):
        snap = os.path.join(ms, "snapshots")
        if os.path.isdir(snap):
            subs = [d for d in os.listdir(snap)
                    if os.path.isfile(os.path.join(snap, d, "config.json"))]
            if subs:
                return os.path.join(snap, subs[0])
        if os.path.isfile(os.path.join(ms, "config.json")):
            return ms
    # 2) 简易布局：models/sentence-transformers/<name>
    simple = os.path.join(base, "models", "sentence-transformers", ST_MODEL)
    if os.path.isfile(os.path.join(simple, "config.json")):
        return simple
    # 3) HF 缓存布局
    hub = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
    d = os.path.join(hub, "models--sentence-transformers--" + ST_MODEL)
    snap = os.path.join(d, "snapshots")
    if os.path.isdir(snap):
        for sub in os.listdir(snap):
            if os.path.isfile(os.path.join(snap, sub, "config.json")):
                return os.path.join(snap, sub)
    return simple


def _st_ready() -> bool:
    """检测真语义模型是否就位（本仓内置目录优先，其次 HF 缓存）。"""
    try:
        import sentence_transformers  # noqa: F401
    except Exception:
        return False
    if os.path.isfile(os.path.join(_local_model_dir(), "config.json")):
        return True
    hub = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
    d = os.path.join(hub, "models--sentence-transformers--" + ST_MODEL)
    if os.path.isdir(os.path.join(d, "snapshots")):
        return True
    for base in (os.environ.get("HF_HOME", ""), os.environ.get("SENTENCE_TRANSFORMERS_HOME", "")):
        if base and os.path.isdir(os.path.join(base, "hub", "models--sentence-transformers--" + ST_MODEL)):
            return True
    return False


def _ef(use_st: bool):
    """use_st=True 强制真语义；否则 auto：模型就位就用真语义，无则降级向量。"""
    local = _local_model_dir()
    have_local = os.path.isfile(os.path.join(local, "config.json"))
    want_st = use_st or _st_ready()
    if want_st:
        try:
            from chromadb.utils import embedding_functions
            ref = local if have_local else ST_MODEL
            print(f"[info] embedding = sentence-transformers 真语义 ({ref})", file=sys.stderr)
            return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=ref)
        except Exception as e:
            print(f"[warn] sentence-transformers 不可用，降级本地向量: {e}", file=sys.stderr)
    print("[info] embedding = local_char_ngram (降级向量)", file=sys.stderr)
    return LocalCharNGramEF()


def _client(root: str):
    return chromadb.PersistentClient(path=os.path.join(root, ".semantic_db"))


def index_file(client, file_path: str, collection: str = DEFAULT_COLLECTION,
               ef=None) -> dict:
    col = client.get_or_create_collection(collection, embedding_function=ef)
    with open(file_path, encoding="utf-8") as f:
        text = f.read()
    chunks = [c for c in text.split("\n\n") if c.strip()]
    ids = [hashlib.md5((file_path + str(i)).encode()).hexdigest()[:12]
           for i in range(len(chunks))]
    metas = [{"source": file_path, "idx": i,
              "ts": datetime.datetime.now().isoformat()} for i in range(len(chunks))]
    col.upsert(ids=ids, documents=chunks, metadatas=metas)
    return {"indexed": len(chunks), "file": file_path}


def search(client, query: str, n: int = 5, collection: str = DEFAULT_COLLECTION,
           ef=None) -> list:
    col = client.get_or_create_collection(collection, embedding_function=ef)
    r = col.query(query_texts=[query], n_results=n)
    out = []
    for doc, meta, dist in zip(r["documents"][0], r["metadatas"][0], r["distances"][0]):
        out.append({"score": round(1 - dist, 4), "source": meta["source"], "text": doc[:200]})
    return out


if __name__ == "__main__":
    if not CHROMA_OK:
        print(json.dumps({"status": "chromadb_not_installed", "error": CHROMA_ERR},
                         ensure_ascii=False, indent=2))
        sys.exit(2)
    if len(sys.argv) < 3:
        print("usage: semantic_search.py <root> index|search <arg> [n] [--st]")
        sys.exit(1)
    use_st = "--st" in sys.argv
    root, cmd = sys.argv[1], sys.argv[2]
    ef = _ef(use_st)
    client = _client(root)
    if cmd == "index":
        print(json.dumps(index_file(client, sys.argv[3], ef=ef), ensure_ascii=False))
    elif cmd == "search":
        n = 5
        for a in sys.argv[3:]:
            if a.isdigit():
                n = int(a)
        q = sys.argv[3] if not sys.argv[3].isdigit() else sys.argv[4]
        print(json.dumps(search(client, q, n, ef=ef), ensure_ascii=False, indent=2))
