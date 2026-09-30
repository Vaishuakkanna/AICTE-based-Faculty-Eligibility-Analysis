# AICTE Faculty Eligibility RAG System

This project is a Retrieval-Augmented Generation (RAG) system designed to evaluate faculty candidates' eligibility based on the All India Council for Technical Education (AICTE) guidelines. It automatically parses a candidate's resume, retrieves relevant AICTE rules, and uses an LLM to determine if the candidate qualifies for specific roles (e.g., Assistant Professor, Associate Professor).

## Features

- **Resume Parsing:** Extracts structured key-value pairs (education, experience, publications, etc.) from PDF resumes.
- **Advanced RAG Pipeline:** Uses a hybrid retrieval approach combining dense vector search (ChromaDB) and keyword search (BM25), followed by cross-encoder reranking to ensure highly relevant guideline retrieval.
- **LangGraph Workflow:** Orchestrates the evaluation process step-by-step using a state graph.
- **FastAPI Backend:** Provides a robust REST API for integrating with web interfaces.
- **React Frontend:** A Vite-powered web interface for easy file uploads and user interaction.
- **CLI Support:** Run evaluations directly from the command line.

## Project Structure

```
.
├── api.py                  # FastAPI backend server
├── config.py               # Configuration settings and environment variables
├── main.py                 # CLI entry point and LangGraph pipeline definition
├── requirements.txt        # Python dependencies
├── ingestion/              # Logic for ingesting AICTE guidelines into the knowledge base
├── extraction/             # PDF extraction and parsing logic
├── retrieval/              # Hybrid retrieval and reranking logic
├── graph/                  # LangGraph nodes and state definitions
├── data/                   # Directory for raw data/documents (e.g., AICTE PDFs)
├── chroma_db/              # Local Chroma vector database storage
└── frontend/               # React + Vite frontend application
```

## Prerequisites

- Python 3.9+
- Node.js (for the frontend)
- API Keys for the required LLM providers (configured via `.env` or `config.py`)

## Setup Instructions

### 1. Clone the repository
Navigate to the project root directory.

### 2. Backend Setup
1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   Create a `.env` file in the root directory and add necessary keys (e.g., `GROQ_API_KEY` or others required by the LLM).

### 3. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm packages:
   ```bash
   npm install
   ```

## Usage

### Running the API Backend
From the root directory, start the FastAPI server:
```bash
uvicorn api:api --reload
```
The API will be available at `http://localhost:8000`.

### Running the Web Frontend
From the `frontend` directory, start the Vite development server:
```bash
npm run dev
```

### Running via Command Line Interface (CLI)
You can test the pipeline directly without starting the servers:
```bash
python main.py --pdf path/to/resume.pdf --question "Is this person eligible for the role of Assistant Professor in Computer Science at a degree-level institution as per AICTE norms?"
```

## How It Works

1. **Ingestion:** The `ingestion` module processes the AICTE guidelines, chunks the text, and stores it in a ChromaDB vector store and a BM25 index. This step runs idempotently.
2. **Extraction:** The `extraction` module reads the uploaded candidate resume and extracts structured data (Education, Experience, etc.).
3. **Retrieval & Reranking:** For the given query, the system retrieves top candidate chunks using both vector similarity and keyword search, then uses a cross-encoder to rerank them.
4. **Evaluation:** An LLM evaluates the extracted resume details against the best-matching guidelines to produce a final eligibility decision.
