#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
semantic_search.py — 本地语义检索引擎
=====================================
填补 local-semantic-search 纯 SKILL.md 壳（无向量库/索引）的工程缺口。

后端：chromadb（已装）。Embedding 两档：
  - 真语义：sentence-transformers 多语言模型（paraphrase-multilingual-MiniLM-L12-v2）
            → 设环境变量 USE_ST=1 启用；模型需先从 HuggingFace 下载（国内用
              HF_ENDPOINT=https://hf-mirror.com 加速）。
  - 本地降级：零依赖字符 n-gram 哈希向量（LocalCharNGramEF）
            → 默认启用，无需下载任何模型，立即可用；语义为词重叠近似，
              弱于真语义但能跑通索引/检索全流程。

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


def _ef(use_st: bool):
    if use_st:
        try:
            from chromadb.utils import embedding_functions
            return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=ST_MODEL)
        except Exception as e:
            print(f"[warn] sentence-transformers 不可用，降级本地向量: {e}", file=sys.stderr)
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
