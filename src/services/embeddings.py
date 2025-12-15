# src/services/embeddings.py
import os
from typing import List
import numpy as np

# Local HF
try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None

# Placeholder for AWS Bedrock client (you will wire actual SDK)
# import boto3

class EmbeddingProvider:
    def __init__(self, mode="local"):
        self.mode = mode
        if mode == "local":
            if SentenceTransformer is None:
                raise RuntimeError("sentence-transformers not installed")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
        elif mode == "bedrock":
            # init bedrock client or other provider
            self.model = None
        else:
            raise ValueError("Unknown embedding mode")

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Return list of embeddings (numpy arrays).
        """
        if self.mode == "local":
            arr = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
            return arr
        elif self.mode == "bedrock":
            # PSEUDO: call AWS Bedrock embedding endpoint
            # client = boto3.client("bedrock-runtime")
            # call model -> returns embeddings
            raise NotImplementedError("Bedrock mode not implemented in offline prototype")
        else:
            raise RuntimeError("unsupported mode")
