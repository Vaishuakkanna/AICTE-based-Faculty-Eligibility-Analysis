"""
ingestion/chunker.py
Loads the pre-defined meaningful AICTE chunks and auto-generates
keywords for each chunk using KeyBERT (all-MiniLM-L6-v2, fully local).

Chunk boundary rule (no text splitter needed):
  1 role x 1 discipline = 1 chunk
  e.g. "Engineering & Technology — Associate Professor" = 1 chunk
       "CAS: Stage 1 → Stage 2"                        = 1 chunk

KeyBERT uses MMR (Maximal Marginal Relevance) to extract diverse,
non-redundant keywords that improve both semantic and BM25 search recall.
"""

import json
from typing import List, Tuple

from langchain_core.documents import Document
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

from config import (
    EMBEDDING_MODEL,
    KEYBERT_TOP_N_KEYWORDS,
    KEYBERT_KEYPHRASE_NGRAM_RANGE,
    KEYBERT_DIVERSITY,
)
from data.guidelines.aicte_chunks import AICTE_CHUNKS

# ──────────────────────────────────────────────────────────────────────────────
# Singleton KeyBERT model — loaded once per process
# ──────────────────────────────────────────────────────────────────────────────
_kw_model: KeyBERT | None = None


def _get_keybert() -> KeyBERT:
    """Load KeyBERT with all-MiniLM-L6-v2 (cached after first call)."""
    global _kw_model
    if _kw_model is None:
        print(f"[KeyBERT] Loading model: {EMBEDDING_MODEL} ...")
        sentence_model = SentenceTransformer(EMBEDDING_MODEL)
        _kw_model = KeyBERT(model=sentence_model)
        print("[KeyBERT] Model ready.")
    return _kw_model


# ──────────────────────────────────────────────────────────────────────────────
# KEYWORD EXTRACTION
# ──────────────────────────────────────────────────────────────────────────────

def extract_keywords(text: str) -> List[str]:
    """
    Extract diverse keywords from a chunk using KeyBERT + MMR.

    Args:
        text: The chunk's content string.

    Returns:
        List of keyword / keyphrase strings (unigrams and bigrams).
    """
    kw_model = _get_keybert()

    results: List[Tuple[str, float]] = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=KEYBERT_KEYPHRASE_NGRAM_RANGE,
        stop_words="english",
        use_mmr=True,
        diversity=KEYBERT_DIVERSITY,
        top_n=KEYBERT_TOP_N_KEYWORDS,
    )

    return [kw for kw, _ in results]


# ──────────────────────────────────────────────────────────────────────────────
# MAIN: LOAD CHUNKS → KEYBERT → DOCUMENTS
# ──────────────────────────────────────────────────────────────────────────────

def load_chunks_as_documents() -> List[Document]:
    """
    Loads the 32 pre-defined meaningful AICTE chunks, runs KeyBERT on
    each chunk's content to auto-generate keywords, then:

      - Appends the keywords to the page_content so BM25 benefits from them.
      - Stores them in metadata for inspection and filtering.

    Returns:
        List of LangChain Document objects ready for ChromaDB + BM25 ingestion.
    """
    print(f"[Chunker] Loading {len(AICTE_CHUNKS)} meaningful AICTE chunks...")
    documents: List[Document] = []

    for i, chunk in enumerate(AICTE_CHUNKS):
        content: str = chunk["content"]

        # ── KeyBERT keyword extraction ──────────────────────────────────────
        keywords: List[str] = extract_keywords(content)
        keywords_str: str = " | ".join(keywords)

        # ── Enrich content (chunk text + keywords for BM25) ─────────────────
        enriched_content = (
            f"{content.strip()}\n\n"
            f"[Keywords: {keywords_str}]"
        )

        # ── Serialize metadata (ChromaDB requires str/int/float/bool values) ─
        raw_meta = {
            "chunk_id": chunk["id"],
            "discipline": chunk["discipline"],
            "position": chunk["position"],
            "institution_type": chunk["institution_type"],
            "keywords": keywords_str,
            **{
                k: (json.dumps(v) if isinstance(v, (list, dict)) else ("" if v is None else v))
                for k, v in chunk["metadata"].items()
            },
        }

        doc = Document(
            page_content=enriched_content,
            metadata=raw_meta,
        )
        documents.append(doc)
        print(f"  [{i+1:02d}/{len(AICTE_CHUNKS)}] {chunk['id']:35s} → {keywords[:3]}")

    print(f"\n[Chunker] Done. {len(documents)} Documents ready for ingestion.")
    return documents


def get_corpus_texts(documents: List[Document]) -> List[str]:
    """
    Extract enriched content strings for BM25 index construction.
    The enriched text (chunk + keywords) ensures keyword search picks
    up both natural language matches and KeyBERT-generated terms.
    """
    return [doc.page_content for doc in documents]


# ──────────────────────────────────────────────────────────────────────────────
# CLI TEST
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    docs = load_chunks_as_documents()
    print("\n=== Sample: First chunk ===")
    print(docs[0].page_content[:600])
    print("\nMetadata:", docs[0].metadata)
    print(f"\nTotal chunks: {len(docs)}")
