"""
config.py — Central configuration for the AICTE Faculty RAG System.
All model names, paths, and hyperparameters live here.
"""

# ──────────────────────────────────────────
# Groq API (free, cloud-hosted, very fast)
# Get free API key at: https://console.groq.com
# Add your key to the .env file (never hardcode here)
# ──────────────────────────────────────────
import os
from dotenv import load_dotenv

load_dotenv()   # auto-reads .env file from project root

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = "qwen/qwen3.8-27b"
LLM_TEMPERATURE: float = 0.0

# ──────────────────────────────────────────
# Local Embedding Model (SentenceTransformers)
# all-MiniLM-L6-v2 → fast, 384-dim, great for semantic search
# Downloaded automatically on first run (~80MB)
# ──────────────────────────────────────────
EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

# ──────────────────────────────────────────
# KeyBERT — auto keyword extraction per chunk
# Uses the same embedding model as above
# ──────────────────────────────────────────
KEYBERT_TOP_N_KEYWORDS: int = 10       # keywords to extract per chunk
KEYBERT_KEYPHRASE_NGRAM_RANGE: tuple = (1, 2)  # unigrams and bigrams
KEYBERT_DIVERSITY: float = 0.5         # MMR diversity (0=similar, 1=diverse)

# ──────────────────────────────────────────
# CrossEncoder Reranker (local, HuggingFace)
# ──────────────────────────────────────────
RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ──────────────────────────────────────────
# ChromaDB (local persistent store)
# ──────────────────────────────────────────
CHROMA_PERSIST_DIR: str = "./chroma_db"
CHROMA_COLLECTION_NAME: str = "aicte_guidelines"

# ──────────────────────────────────────────
# Chunking Strategy
# Pre-defined meaningful chunks: 1 role x 1 discipline = 1 chunk
# KeyBERT generates keywords automatically at ingestion time
# ──────────────────────────────────────────

# ──────────────────────────────────────────
# Retrieval Hyperparameters
# ──────────────────────────────────────────
SEMANTIC_TOP_K: int = 5        # chunks from ChromaDB semantic search
KEYWORD_TOP_K: int = 5         # chunks from BM25 keyword search
RERANKED_TOP_K: int = 5        # best chunks after cross-encoder reranking

# ──────────────────────────────────────────
# PDF Extraction
# ──────────────────────────────────────────
MAX_PAGES_PER_RESUME: int = 50  # safety cap on resume pages
# Send all pages in a single API call to bypass Groq rate limits for small batch sizes
PAGES_PER_LLM_BATCH: int = 100   # how many pages to send per LLM call

# ──────────────────────────────────────────
# Raw Guidelines File
# ──────────────────────────────────────────
GUIDELINES_RAW_FILE: str = "data/guidelines/aicte_raw.txt"
