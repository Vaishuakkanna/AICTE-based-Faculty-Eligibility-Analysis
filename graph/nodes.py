"""
graph/nodes.py
LangGraph node functions.
Each node receives the current AgentState and returns a dict of
updated fields to merge back into the state.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

from config import GROQ_API_KEY, GROQ_MODEL, LLM_TEMPERATURE
from extraction.pdf_extractor import extract_resume_kv
from retrieval.semantic_search import semantic_search
from retrieval.keyword_search import keyword_search
from retrieval.reranker import get_best_chunks
from graph.state import AgentState


# ──────────────────────────────────────────────────────────────────────────────
# NODE 1 — EXTRACT RESUME
# ──────────────────────────────────────────────────────────────────────────────

def extract_resume(state: AgentState) -> dict:
    """
    Node: extract_resume
    Reads the PDF page-by-page and uses a structured LLM to populate
    a typed ResumeDetails Pydantic object.

    Inputs  (from state): pdf_path
    Outputs (to state)  : resume_raw_pages, resume_kv
    """
    print("\n" + "=" * 60)
    print("NODE: extract_resume")
    print("=" * 60)

    pdf_path = state["pdf_path"]
    pages, resume_kv = extract_resume_kv(pdf_path)

    return {
        "resume_raw_pages": pages,
        "resume_kv": resume_kv,
    }


# ──────────────────────────────────────────────────────────────────────────────
# NODE 2 — HYBRID RETRIEVE & RERANK
# ──────────────────────────────────────────────────────────────────────────────

def hybrid_retrieve_and_rerank(state: AgentState) -> dict:
    """
    Node: hybrid_retrieve_and_rerank
    1. Semantic search  → top-3 chunks from ChromaDB.
    2. Keyword search   → top-3 chunks from BM25.
    3. Deduplicate      → combine up to 6 unique candidates.
    4. CrossEncoder     → rerank and keep the best 3.

    Inputs  (from state): question, vector_store, bm25_index, corpus_texts
    Outputs (to state)  : semantic_chunks, keyword_chunks, best_chunks
    """
    print("\n" + "=" * 60)
    print("NODE: hybrid_retrieve_and_rerank")
    print("=" * 60)

    question = state["question"]
    vector_store = state["vector_store"]
    bm25_index = state["bm25_index"]
    corpus_texts = state["corpus_texts"]

    # 1. Semantic Search (ChromaDB)
    sem_chunks = semantic_search(vector_store, question)
    print(f"\n[Semantic] Retrieved {len(sem_chunks)} chunk(s) for query: '{question[:50]}...'")
    for i, chunk in enumerate(sem_chunks):
        print(f"  [Semantic {i+1}] {chunk[:120].replace(chr(10), ' ')}...")

    # 2. Keyword Search (BM25)
    kw_chunks = keyword_search(bm25_index, corpus_texts, question)
    print(f"\n[Keyword ] Retrieved {len(kw_chunks)} chunk(s) for query: '{question[:50]}...'")
    for i, chunk in enumerate(kw_chunks):
        print(f"  [Keyword {i+1}] {chunk[:120].replace(chr(10), ' ')}...")

    # 3. Deduplicate + Rerank (CrossEncoder)
    best = get_best_chunks(question, sem_chunks, kw_chunks)

    return {
        "semantic_chunks": sem_chunks,
        "keyword_chunks": kw_chunks,
        "best_chunks": best,
    }


# ──────────────────────────────────────────────────────────────────────────────
# NODE 3 — EVALUATE
# ──────────────────────────────────────────────────────────────────────────────

_EVALUATION_PROMPT = PromptTemplate.from_template("""
You are an expert HR Eligibility Evaluator for AICTE-approved technical institutions in India.

Your job is to assess whether the given candidate meets the AICTE eligibility criteria for the
specified position, using ONLY:
  1. The candidate's structured Resume Details (extracted Key-Value pairs).
  2. The AICTE Eligibility Guideline Chunks retrieved below — treat these as the source of truth.

CLARIFICATION ON INTENT:
If the user asks if a candidate is eligible to "attend a conference", and the guidelines specify criteria for "receiving a travel grant for paper presentations", assume the user implies attending via this scheme. Evaluate if they meet the criteria to get the grant, and DO NOT mark them "NOT ELIGIBLE" simply because the rule says "presenting" instead of "attending".

DO NOT list out each requirement or do a criterion-by-criterion breakdown.
Instead, keep your response extremely concise:
1. State "ELIGIBLE" or "NOT ELIGIBLE" immediately.
2. Follow it with a single, short sentence explaining why.

QUESTION / ROLE BEING EVALUATED:
{question}

CANDIDATE RESUME:
{resume_json}

AICTE ELIGIBILITY GUIDELINE CHUNKS:
{context}

CONCISE VERDICT AND REASON:
""")


def evaluate(state: AgentState) -> dict:
    """
    Node: evaluate
    Uses the LLM to produce a final structured eligibility evaluation
    by combining the resume KV data + top guideline chunks.

    Inputs  (from state): question, resume_kv, best_chunks
    Outputs (to state)  : final_answer
    """
    print("\n" + "=" * 60)
    print("NODE: evaluate")
    print("=" * 60)

    question = state["question"]
    resume_kv = state["resume_kv"]
    best_chunks = state["best_chunks"]

    context = "\n\n---\n\n".join(
        [f"[Chunk {i+1}]\n{chunk}" for i, chunk in enumerate(best_chunks)]
    )
    import json
    resume_json = json.dumps(resume_kv, indent=2)

    llm = ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=LLM_TEMPERATURE,
        max_tokens=900,
    )

    chain = _EVALUATION_PROMPT | llm
    final_answer: str = chain.invoke({
        "question": question,
        "resume_json": resume_json,
        "context": context,
    }).content
    print("\n[INFO] Evaluation complete.")
    return {"final_answer": final_answer}
