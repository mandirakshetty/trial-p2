# src/services/vector_store.py
import faiss
import numpy as np
import os
from typing import List, Tuple

class VectorStore:
    def __init__(self, index_dir="data/indices"):
        os.makedirs(index_dir, exist_ok=True)
        self.index_dir = index_dir
        # we will create ephemeral index per-request in RAGProcessor for simplicity

    def build_index(self, embeddings: np.ndarray) -> faiss.Index:
        dim = embeddings.shape[1]
        idx = faiss.IndexFlatIP(dim)
        faiss.normalize_L2(embeddings)
        idx.add(embeddings)
        return idx

    def search_index(self, idx: faiss.Index, query_emb: np.ndarray, top_k: int=5) -> Tuple[List[float], List[int]]:
        D, I = idx.search(query_emb, top_k)
        return D[0].tolist(), I[0].tolist()
