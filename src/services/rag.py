# src/services/rag.py
from typing import List, Dict
from src.services.embeddings import EmbeddingProvider
from src.services.vector_store import VectorStore
import numpy as np

class RAGProcessor:
    def __init__(self, emb_provider: EmbeddingProvider, vector_store: VectorStore):
        self.emb = emb_provider
        self.vs = vector_store

    def run_rag(self, query: str, chunks: List[str], top_k: int=5) -> List[Dict]:
        """
        1) Embed chunks, build local FAISS index
        2) Embed query, retrieve top_k chunks
        3) Build prompt with retrieved chunks and call LLM (Bedrock) or create simple summary
        4) Return explanation + evidence chunks
        """
        # embed chunks
        chunk_embeddings = self.emb.embed(chunks)
        if isinstance(chunk_embeddings, list):
            chunk_embeddings = np.array(chunk_embeddings)

        idx = self.vs.build_index(chunk_embeddings)

        # embed query
        q_emb = self.emb.embed([query])
        if isinstance(q_emb, list):
            q_emb = np.array(q_emb)

        # search
        D, I = idx.search(q_emb, top_k)
        D = D[0]
        I = I[0]

        retrieved = []
        for score, idx_i in zip(D, I):
            retrieved.append({"score": float(score), "text": chunks[int(idx_i)]})

        # Build an LLM prompt (for prototype we generate deterministic answer)
        # In production: call Bedrock with prompt + retrieved as context
        answer = self.simple_summarize(query, retrieved)

        return [{"answer": answer, "evidence": retrieved}]

    def simple_summarize(self, query: str, retrieved: List[Dict]) -> str:
        # Basic template that references evidence — replace with real LLM call
        lines = [f"RCA for: {query}", ""]
        lines.append("Summary:")
        # Heuristic: count ERROR occurrences
        total_err = 0
        for r in retrieved:
            total_err += r["text"].lower().count("error")
        if total_err == 0:
            lines.append("No critical errors detected in the retrieved logs.")
        else:
            lines.append(f"Detected {total_err} error occurrences across retrieved fragments.")
            lines.append("Probable causes include component instability or network/API failures; check the evidence below.")
        lines.append("")
        lines.append("Evidence excerpts:")
        for i, r in enumerate(retrieved, 1):
            excerpt = r["text"][:500].replace("\n", " ")
            lines.append(f"{i}. (score: {r['score']:.3f}) {excerpt}...")
        lines.append("")
        lines.append("Suggested actions: Verify configuration, check connectivity, restart affected services.")
        return "\n".join(lines)
