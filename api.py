import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from ingestion.ingestor import ingest
from graph.state import AgentState
from main import build_graph

api = FastAPI(title="AICTE Evaluator API")

# Allow CORS for React frontend (running on a different port)
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to hold models so they stay in memory
vector_store = None
bm25_index = None
corpus_texts = None

from retrieval.reranker import get_reranker_instance

@api.on_event("startup")
def startup_event():
    global vector_store, bm25_index, corpus_texts
    print("[API] Initializing Knowledge Base (Loading Embeddings & DB)...")
    vector_store, bm25_index, corpus_texts = ingest()
    
    print("[API] Pre-loading Reranker weights into memory...")
    get_reranker_instance()
    
    print("[API] Startup complete! Ready to evaluate.")

@api.post("/api/evaluate")
async def evaluate_resume(
    question: str = Form(...),
    file: UploadFile = File(...)
):
    global vector_store, bm25_index, corpus_texts
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
        
    # Save uploaded file to temp file
    fd, temp_path = tempfile.mkstemp(suffix=".pdf")
    with os.fdopen(fd, "wb") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        
    try:
        print(f"[API] Evaluating {file.filename} for query: {question}")
        initial_state = AgentState(
            pdf_path=temp_path,
            question=question,
            vector_store=vector_store,
            bm25_index=bm25_index,
            corpus_texts=corpus_texts,
            resume_raw_pages=[],
            resume_kv={},
            semantic_chunks=[],
            keyword_chunks=[],
            best_chunks=[],
            final_answer=""
        )
        
        # Compile the graph
        app = build_graph()
        
        # Run the RAG LangGraph Pipeline
        result = app.invoke(initial_state)
        
        return {
            "evaluation": result.get("final_answer", ""),
            "resume_kv": result.get("resume_kv", {}),
            "retrieved_chunks": [{"text": chunk} for chunk in result.get("best_chunks", [])]
        }
    except Exception as e:
        print(f"[API] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(temp_path)
