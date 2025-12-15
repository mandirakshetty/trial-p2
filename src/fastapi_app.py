# src/fastapi_app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os

from src.services.reader import locate_and_read_logs
from src.services.chunker import chunk_texts
from src.services.embeddings import EmbeddingProvider
from src.services.vector_store import VectorStore
from src.services.rag import RAGProcessor

# CONFIG
ROOT_LOGSPACE = r"E:/LogSpace"   # change if needed
VECTOR_INDEX_DIR = "data/indices"

app = FastAPI(title="LogSpace RCA API")

# init providers (local-default). You can configure env var to use bedrock.
emb_provider = EmbeddingProvider(mode="local")   # modes: "local" or "bedrock"
vector_store = VectorStore(index_dir=VECTOR_INDEX_DIR)
rag = RAGProcessor(emb_provider=emb_provider, vector_store=vector_store)


class AnalyzeRequest(BaseModel):
    client: str
    logspace: str     # app name like Unigy
    timestamp: Optional[str] = None
    version: Optional[str] = None
    top_k: Optional[int] = 5
    # optional: you could accept uploaded logs as text in this field
    uploaded_log_text: Optional[str] = None


@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    # 1. Locate logs (either via uploaded text or folder structure)
    if req.uploaded_log_text:
        raw_texts = [req.uploaded_log_text]
    else:
        raw_texts = locate_and_read_logs(ROOT_LOGSPACE, req.client, req.logspace, req.version)
        if not raw_texts:
            raise HTTPException(status_code=404, detail="No logs found for given filters")

    # 2. Chunk texts
    chunks = chunk_texts(raw_texts, chunk_size=800, overlap=100)

    # 3. Embed chunks and upsert into temporary vector store (or reuse prebuilt)
    # We'll compute embeddings on-the-fly and search within them
    results = rag.run_rag(
        query=f"{req.logspace} {req.version} {req.timestamp or ''}",
        chunks=chunks,
        top_k=req.top_k
    )

    return {"status": "ok", "client": req.client, "logspace": req.logspace, "results": results}


if __name__ == "__main__":
    uvicorn.run("src.fastapi_app:app", host="0.0.0.0", port=8000, reload=True)
