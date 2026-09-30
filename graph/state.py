"""
graph/state.py
LangGraph AgentState — the shared state object that flows
through every node in the pipeline.
"""

from typing import List, Optional, TypedDict
from rank_bm25 import BM25Okapi
from langchain_chroma import Chroma
# No Pydantic schema imported


class AgentState(TypedDict):
    """
    Shared state passed between LangGraph nodes.

    Fields populated by each node:
    ─────────────────────────────────────────────
    INPUT (set by caller before graph.invoke()):
        pdf_path        : Path to the uploaded resume PDF.
        question        : The user's eligibility question.
        vector_store    : Initialized Chroma vector store (injected at runtime).
        bm25_index      : Initialized BM25 index (injected at runtime).
        corpus_texts    : Raw corpus texts for BM25 lookup (injected at runtime).

    NODE: extract_resume
        resume_raw_pages  : List of per-page text strings from the PDF.
        resume_kv         : Structured ResumeDetails Pydantic object.

    NODE: hybrid_retrieve_and_rerank
        semantic_chunks   : Top-k chunks from ChromaDB semantic search.
        keyword_chunks    : Top-k chunks from BM25 keyword search.
        best_chunks       : Top chunks after CrossEncoder reranking.

    NODE: evaluate
        final_answer      : The final LLM-generated eligibility evaluation.
    """

    # ── Inputs ──
    pdf_path: str
    question: str
    vector_store: Chroma
    bm25_index: BM25Okapi
    corpus_texts: List[str]

    # ── extract_resume outputs ──
    resume_raw_pages: List[str]
    resume_kv: Optional[dict]

    # ── hybrid_retrieve_and_rerank outputs ──
    semantic_chunks: List[str]
    keyword_chunks: List[str]
    best_chunks: List[str]

    # ── evaluate output ──
    final_answer: str
