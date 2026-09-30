"""
retrieval/keyword_search.py
Wraps BM25Okapi for sparse keyword retrieval in the hybrid pipeline.
"""

from typing import List
from rank_bm25 import BM25Okapi
from config import KEYWORD_TOP_K


def keyword_search(
    bm25_index: BM25Okapi,
    corpus_texts: List[str],
    query: str,
    top_k: int = KEYWORD_TOP_K,
) -> List[str]:
    """
    Performs keyword-based (BM25) search over the corpus.

    Args:
        bm25_index   : Built BM25Okapi index.
        corpus_texts : Original (enriched) chunk texts in the same order as BM25 index.
        query        : The user's search query.
        top_k        : Number of top results to return.

    Returns:
        List of chunk content strings (top_k highest BM25 scores).
    """
    tokenized_query = query.lower().split()
    scores = bm25_index.get_scores(tokenized_query)

    # Sort indices by descending score and pick top_k
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    chunks = [corpus_texts[i] for i in top_indices]

    print(f"[Keyword ] Retrieved {len(chunks)} chunk(s) for query: '{query[:60]}...'")
    return chunks
