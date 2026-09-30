"""
ingestion/ingestor.py
Handles one-time ingestion of AICTE guidelines into:
  - ChromaDB using SentenceTransformer embeddings (all-MiniLM-L6-v2, fully local)
  - BM25Okapi index for keyword search (cached to disk)
Call `ingest()` once before running the LangGraph pipeline.
"""

import pickle
from pathlib import Path
from typing import List, Tuple

import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from rank_bm25 import BM25Okapi

from config import (
    CHROMA_COLLECTION_NAME,
    CHROMA_PERSIST_DIR,
    EMBEDDING_MODEL,
)
from ingestion.chunker import load_chunks_as_documents, get_corpus_texts

# Paths for BM25 disk cache
BM25_CACHE_PATH = Path(CHROMA_PERSIST_DIR) / "bm25_index.pkl"
CORPUS_CACHE_PATH = Path(CHROMA_PERSIST_DIR) / "bm25_corpus.pkl"

# Lazy-loaded embedding singleton
_embeddings: HuggingFaceEmbeddings | None = None


def _get_embeddings() -> HuggingFaceEmbeddings:
    """
    Returns HuggingFaceEmbeddings using all-MiniLM-L6-v2.
    Model is downloaded once (~80MB) and cached by sentence-transformers.
    """
    global _embeddings
    if _embeddings is None:
        print(f"[INFO] Loading embedding model: {EMBEDDING_MODEL}")
        _embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},         # change to "cuda" if GPU available
            encode_kwargs={"normalize_embeddings": True},
        )
        print("[INFO] Embedding model loaded.")
    return _embeddings


# ──────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ──────────────────────────────────────────────────────────────────────────────

def ingest() -> Tuple[Chroma, BM25Okapi, List[str]]:
    """
    Ingests all AICTE guideline chunks into ChromaDB and BM25.
    Idempotent: skips ChromaDB re-insertion if docs already exist.
    BM25 index is persisted to disk and reloaded on subsequent runs.

    Returns:
        (vector_store, bm25_index, corpus_texts)
    """
    embeddings = _get_embeddings()

    # ── 1. Setup ChromaDB ──────────────────────────────────────────────────
    vector_store = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )

    existing_count = vector_store._collection.count()

    if existing_count == 0:
        print("[INFO] ChromaDB is empty — chunking and ingesting guidelines...")
        documents = load_chunks_as_documents()
        vector_store.add_documents(documents)
        print(f"[INFO] Inserted {len(documents)} chunks into ChromaDB.")
        corpus_texts = get_corpus_texts(documents)
    else:
        print(f"[INFO] ChromaDB already has {existing_count} docs. Skipping re-ingestion.")
        corpus_texts = None  # will load from BM25 cache

    # ── 2. Build or Load BM25 ─────────────────────────────────────────────
    bm25_index, corpus_texts = _load_or_build_bm25(corpus_texts)

    return vector_store, bm25_index, corpus_texts


def _load_or_build_bm25(
    corpus_texts: List[str] | None,
) -> Tuple[BM25Okapi, List[str]]:
    """
    Load BM25 from disk cache if available.
    If not, build from corpus_texts and persist to disk.

    The corpus_texts includes the enriched content (chunk + keywords)
    so BM25 benefits from keyword signals during tokenization.
    """
    if BM25_CACHE_PATH.exists() and CORPUS_CACHE_PATH.exists():
        print("[INFO] Loading BM25 index from disk cache...")
        with open(BM25_CACHE_PATH, "rb") as f:
            bm25_index = pickle.load(f)
        with open(CORPUS_CACHE_PATH, "rb") as f:
            corpus_texts = pickle.load(f)
        print(f"[INFO] BM25 loaded: {len(corpus_texts)} documents.")
    else:
        if corpus_texts is None:
            raise RuntimeError(
                "[ERROR] BM25 cache not found and no corpus_texts available. "
                "Delete chroma_db/ and re-run to rebuild everything from scratch."
            )
        print("[INFO] Building BM25 index from corpus...")
        tokenized_corpus = [text.lower().split() for text in corpus_texts]
        bm25_index = BM25Okapi(tokenized_corpus)

        # Persist to disk
        BM25_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(BM25_CACHE_PATH, "wb") as f:
            pickle.dump(bm25_index, f)
        with open(CORPUS_CACHE_PATH, "wb") as f:
            pickle.dump(corpus_texts, f)
        print(f"[INFO] BM25 cached to {BM25_CACHE_PATH}.")

    return bm25_index, corpus_texts


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    vs, bm25, corpus = ingest()
    print(f"\n[DONE] Ingestion complete.")
    print(f"  ChromaDB chunks : {vs._collection.count()}")
    print(f"  BM25 corpus     : {len(corpus)} entries")
