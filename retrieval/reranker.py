"""
retrieval/reranker.py
Cross-Encoder reranker: scores and picks the best chunks from the
combined semantic + keyword candidate set.
"""

from typing import List, Tuple
from sentence_transformers import CrossEncoder
from config import RERANKER_MODEL, RERANKED_TOP_K


_reranker_instance = None

def get_reranker_instance(model_name: str = RERANKER_MODEL) -> CrossEncoder:
    """Returns a singleton instance of the CrossEncoder to keep weights in memory."""
    global _reranker_instance
    if _reranker_instance is None:
        print(f"[Reranker] Loading weights into memory ({model_name})...")
        _reranker_instance = CrossEncoder(model_name)
    return _reranker_instance

def rerank(
    query: str,
    candidate_chunks: List[str],
    top_k: int = RERANKED_TOP_K,
    model_name: str = RERANKER_MODEL,
) -> List[Tuple[str, float]]:
    """
    Re-ranks a list of candidate chunks using a CrossEncoder model.

    Args:
        query            : The user's question.
        candidate_chunks : Combined (semantic + keyword) unique chunks.
        top_k            : Number of top chunks to return after reranking.
        model_name       : HuggingFace CrossEncoder model name.

    Returns:
        List of (chunk_text, score) tuples sorted by descending score.
    """
    if not candidate_chunks:
        return []

    reranker = get_reranker_instance(model_name)

    # Build (query, chunk) pairs for scoring
    pairs = [[query, chunk] for chunk in candidate_chunks]
    scores: List[float] = reranker.predict(pairs).tolist()

    # Zip and sort by score descending
    scored = sorted(zip(candidate_chunks, scores), key=lambda x: x[1], reverse=True)

    top_results = scored[:top_k]
    print(
        f"[Reranker] Scored {len(candidate_chunks)} candidates → kept top {len(top_results)}. "
        f"Best score: {top_results[0][1]:.4f}"
    )
    return top_results


def get_best_chunks(
    query: str,
    semantic_chunks: List[str],
    keyword_chunks: List[str],
    top_k: int = RERANKED_TOP_K,
) -> List[str]:
    """
    Convenience wrapper:
      1. Deduplicates semantic + keyword results.
      2. Reranks using CrossEncoder.
      3. Returns only the text of the top-k chunks.

    Args:
        query           : The user's question.
        semantic_chunks : Top chunks from ChromaDB semantic search.
        keyword_chunks  : Top chunks from BM25 keyword search.
        top_k           : Final number of best chunks to return.

    Returns:
        List of chunk text strings (best top_k).
    """
    # Deduplicate while preserving order
    seen = set()
    combined = []
    for chunk in semantic_chunks + keyword_chunks:
        if chunk not in seen:
            seen.add(chunk)
            combined.append(chunk)

    print(f"[Reranker] Combined {len(semantic_chunks)} semantic + {len(keyword_chunks)} keyword "
          f"→ {len(combined)} unique candidates.")

    scored_chunks = rerank(query, combined, top_k=top_k)
    return [chunk for chunk, _ in scored_chunks]
