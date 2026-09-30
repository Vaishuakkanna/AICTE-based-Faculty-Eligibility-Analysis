"""
retrieval/semantic_search.py
Wraps ChromaDB similarity search for the hybrid retrieval pipeline.
"""

from typing import List
from langchain_chroma import Chroma
from config import SEMANTIC_TOP_K


def semantic_search(vector_store: Chroma, query: str, top_k: int = SEMANTIC_TOP_K) -> List[str]:
    """
    Performs dense semantic search using ChromaDB vector similarity.

    Args:
        vector_store : Initialized Chroma instance.
        query        : The user's question or search query.
        top_k        : Number of top results to return.

    Returns:
        List of chunk content strings (top_k most semantically similar).
    """
    results = vector_store.similarity_search(query, k=top_k)
    chunks = [doc.page_content for doc in results]
    print(f"[Semantic] Retrieved {len(chunks)} chunk(s) for query: '{query[:60]}...'")
    return chunks
