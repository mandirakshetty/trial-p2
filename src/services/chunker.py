# src/services/chunker.py
from typing import List
import math

def chunk_texts(texts: List[str], chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Simple chunker: concatenates input texts and splits into overlapping chunks.
    """
    joined = "\n\n".join(texts)
    if len(joined) <= chunk_size:
        return [joined]
    chunks = []
    start = 0
    length = len(joined)
    while start < length:
        end = start + chunk_size
        chunk = joined[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks
