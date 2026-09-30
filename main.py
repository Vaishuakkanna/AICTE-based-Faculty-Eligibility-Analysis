"""
main.py — Entry point for the AICTE Faculty Eligibility RAG System.

Usage:
    python main.py --pdf path/to/resume.pdf --question "Is this person eligible for Associate Professor (CS)?"

Steps:
    1. Ingest AICTE guidelines into ChromaDB + BM25 (idempotent, runs once).
    2. Compile the LangGraph pipeline.
    3. Run the pipeline with the given resume and question.
    4. Print the structured resume KV and the final evaluation.
"""

import argparse
import json

from langgraph.graph import StateGraph, START, END

from ingestion.ingestor import ingest
from graph.state import AgentState
from graph.nodes import extract_resume, hybrid_retrieve_and_rerank, evaluate


# ──────────────────────────────────────────────────────────────────────────────
# BUILD LANGGRAPH
# ──────────────────────────────────────────────────────────────────────────────

def build_graph():
    """Compile and return the LangGraph application."""
    workflow = StateGraph(AgentState)

    # Register nodes
    workflow.add_node("extract_resume", extract_resume)
    workflow.add_node("hybrid_retrieve_and_rerank", hybrid_retrieve_and_rerank)
    workflow.add_node("evaluate", evaluate)

    # Define edges (linear pipeline)
    workflow.add_edge(START, "extract_resume")
    workflow.add_edge("extract_resume", "hybrid_retrieve_and_rerank")
    workflow.add_edge("hybrid_retrieve_and_rerank", "evaluate")
    workflow.add_edge("evaluate", END)

    return workflow.compile()


# ──────────────────────────────────────────────────────────────────────────────
# MAIN RUNNER
# ──────────────────────────────────────────────────────────────────────────────

def run(pdf_path: str, question: str):
    """
    End-to-end pipeline:
      1. Ingest guidelines.
      2. Build graph.
      3. Invoke with resume + question.
      4. Print results.
    """
    print("\n" + "=" * 60)
    print("  AICTE Faculty Eligibility RAG System")
    print("=" * 60)

    # Step 1: Ingest (idempotent — skips if already done)
    print("\n[STEP 1] Setting up knowledge base...")
    vector_store, bm25_index, corpus_texts = ingest()

    # Step 2: Build LangGraph pipeline
    print("\n[STEP 2] Compiling LangGraph pipeline...")
    app = build_graph()

    # Step 3: Build initial state
    initial_state: AgentState = {
        "pdf_path": pdf_path,
        "question": question,
        "vector_store": vector_store,
        "bm25_index": bm25_index,
        "corpus_texts": corpus_texts,
        # These will be populated by the nodes:
        "resume_raw_pages": [],
        "resume_kv": None,
        "semantic_chunks": [],
        "keyword_chunks": [],
        "best_chunks": [],
        "final_answer": "",
    }

    # Step 4: Run the graph
    print("\n[STEP 3] Running evaluation pipeline...")
    result = app.invoke(initial_state)

    # Step 5: Display outputs
    print("\n" + "=" * 60)
    print("  EXTRACTED RESUME — KEY-VALUE PAIRS")
    print("=" * 60)
    import json
    print(json.dumps(result["resume_kv"], indent=2))

    print("\n" + "=" * 60)
    print("  RETRIEVED GUIDELINE CHUNKS USED")
    print("=" * 60)
    for i, chunk in enumerate(result["best_chunks"], 1):
        print(f"\n[Chunk {i}]\n{chunk[:300]}...")

    print("\n" + "=" * 60)
    print("  FINAL ELIGIBILITY EVALUATION")
    print("=" * 60)
    print(result["final_answer"])

    return result


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="AICTE Faculty Eligibility Evaluator — RAG Pipeline"
    )
    parser.add_argument(
        "--pdf",
        type=str,
        required=True,
        help="Path to the candidate's resume PDF",
    )
    parser.add_argument(
        "--question",
        type=str,
        default="Is this person eligible for the role of Assistant Professor in Computer Science at a degree-level institution as per AICTE norms?",
        help="Eligibility question to evaluate",
    )

    args = parser.parse_args()
    run(pdf_path=args.pdf, question=args.question)
