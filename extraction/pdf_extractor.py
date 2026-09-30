"""
extraction/pdf_extractor.py
Reads a resume PDF page-by-page and extracts structured Key-Value data.

HOW PAGE-BY-PAGE WORKS:
────────────────────────────────────────────────────────────────────────
A 16-page resume is handled as follows:

  Page 1 ─┐
  Page 2  ─┤  → Batch 1 (4 pages) → LLM → Partial ResumeDetails JSON
  Page 3  ─┤
  Page 4 ─┘

  Page 5 ─┐
  Page 6  ─┤  → Batch 2 (4 pages) → LLM → Partial ResumeDetails JSON
  ...

  All Partial JSONs → MERGE → Final ResumeDetails object

Why batching instead of one big call?
  - A 16-page resume can be 15,000+ tokens
  - Local LLMs (Ollama/Mistral) have limited context windows (~8k-32k)
  - Batching keeps each LLM call within safe limits
  - Results are merged: lists are extended, scalars take the last non-empty value
────────────────────────────────────────────────────────────────────────
"""

import sys
import json
from typing import List, Tuple, Dict, Any

from pypdf import PdfReader
from langchain_groq import ChatGroq

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    LLM_TEMPERATURE,
    MAX_PAGES_PER_RESUME,
    PAGES_PER_LLM_BATCH,
)
# No hardcoded Pydantic schema used here anymore


# ──────────────────────────────────────────────────────────────────────────────
# PAGE READING
# ──────────────────────────────────────────────────────────────────────────────

def _read_pages(pdf_path: str) -> List[str]:
    """Read PDF and return a list of per-page text strings."""
    reader = PdfReader(pdf_path)
    total = min(len(reader.pages), MAX_PAGES_PER_RESUME)

    if len(reader.pages) > MAX_PAGES_PER_RESUME:
        print(f"[WARNING] PDF has {len(reader.pages)} pages; "
              f"processing first {MAX_PAGES_PER_RESUME}.")

    pages = []
    for i in range(total):
        text = reader.pages[i].extract_text() or ""
        pages.append(text)

    print(f"[INFO] Read {len(pages)} page(s) from '{pdf_path}'.")
    return pages


# ──────────────────────────────────────────────────────────────────────────────
# PROMPT BUILDER
# ──────────────────────────────────────────────────────────────────────────────

def _build_batch_prompt(batch_text: str, page_range: str) -> str:
    return f"""You are an expert resume parser. Extract ALL information from the resume text below.
Create a comprehensive, dynamic JSON object containing Key-Value pairs of every detail you find.

Do not use a fixed schema. Instead, group information logically. For example:
- Personal Details
- Education History (as a list of objects)
- Work Experience (as a list of objects)
- Publications
- Skills
- Any other relevant details

Rules:
- If date ranges are present, keep them but also try to calculate total years (e.g., "experience_years": "5")
- "First Class" = 60% or above in Indian grading system (note if this is present)
- CRITICAL: If you encounter quotation marks inside a string, you MUST escape them with a backslash (e.g. \\") or use single quotes.
- Return ONLY the raw JSON object, no markdown formatting, no explanation text.

Resume text (Pages {page_range}):
{batch_text}

JSON:"""

# ──────────────────────────────────────────────────────────────────────────────
# PER-BATCH LLM EXTRACTION
# ──────────────────────────────────────────────────────────────────────────────

def _extract_batch(llm: ChatGroq, batch_text: str, batch_idx: int) -> Dict[str, Any]:
    """
    Send a chunk of text to the local LLM and parse the JSON response.
    """
    prompt = _build_batch_prompt(batch_text, str(batch_idx))

    print(f"  → Sending chunk {batch_idx} to {GROQ_MODEL} (approx {len(batch_text)//4} tokens)...")
    import time
    max_retries = 3
    raw_response = ""
    for attempt in range(max_retries):
        try:
            # First attempt: Use strict JSON mode. If it fails, disable it to bypass the 400 error.
            if attempt == 0:
                bound_llm = llm.bind(response_format={"type": "json_object"})
            else:
                bound_llm = llm
                
            raw_response = bound_llm.invoke(prompt).content
            break
        except Exception as e:
            error_str = str(e)
            print(f"  [WARNING] LLM failed on attempt {attempt+1}. Error: {error_str}")
            if "413" in error_str or "rate_limit" in error_str.lower():
                print("  [INFO] Hit Groq Rate Limit (ITPM). Sleeping for 60 seconds to reset limit...")
                time.sleep(60)
            else:
                time.sleep(2)
                
            if attempt == max_retries - 1:
                print(f"  [ERROR] Skipping chunk {batch_idx} after {max_retries} failed attempts.")
                return {}

    # Extract JSON from response (LLM may add preamble text)
    try:
        # Some models still return markdown blocks despite json mode
        if "```json" in raw_response:
            raw_response = raw_response.split("```json")[1].split("```")[0]
        elif "```" in raw_response:
            raw_response = raw_response.split("```")[1].split("```")[0]
            
        start = raw_response.find("{")
        end = raw_response.rfind("}") + 1
        json_str = raw_response[start:end]
        
        # Try to parse, allowing control characters
        try:
            return json.loads(json_str, strict=False)
        except json.JSONDecodeError as e:
            print(f"  [WARNING] Python failed to parse the JSON manually: {e}. Returning empty dictionary.")
            return {}

    except (json.JSONDecodeError, ValueError) as e:
        print(f"  [WARNING] Failed to parse JSON for pages {page_range}: {e}")
        return {}


# ──────────────────────────────────────────────────────────────────────────────
# MERGE LOGIC
# ──────────────────────────────────────────────────────────────────────────────

def _merge_batches(batch_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge multiple dynamic per-batch JSON dicts into one final dict.
    - Lists with the same key are concatenated.
    - Dicts with the same key are recursively merged.
    - Scalars take the first non-null/non-empty value found.
    """
    merged: Dict[str, Any] = {}

    def deep_merge(target: dict, source: dict):
        for k, v in source.items():
            if k not in target:
                target[k] = v
            elif isinstance(v, list) and isinstance(target[k], list):
                target[k].extend(v)
            elif isinstance(v, dict) and isinstance(target[k], dict):
                deep_merge(target[k], v)
            elif isinstance(v, (int, float)) and isinstance(target[k], (int, float)):
                # If they look like counts, sum them
                if "count" in k.lower() or "total" in k.lower():
                    target[k] += v
                else:
                    if target[k] in (None, "", 0):
                        target[k] = v
            else:
                if target[k] in (None, "") and v not in (None, ""):
                    target[k] = v

    for batch in batch_results:
        if batch:
            deep_merge(merged, batch)

    return merged


# ──────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ──────────────────────────────────────────────────────────────────────────────

def extract_resume_kv(pdf_path: str) -> Tuple[List[str], Dict[str, Any]]:
    """
    Main entry point for dynamic resume extraction using chunked token limits.
    """
    # 1. Read pages
    pages = _read_pages(pdf_path)
    full_text = "\n\n".join(pages)

    # 2. Initialize local LLM
    llm = ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=LLM_TEMPERATURE,
        max_tokens=900,
    )

    # 3. Chunk text by safe token limit (Groq Qwen limit is ~7000 tokens)
    # Estimate 4 chars per token. Safe max tokens = 4500 (leaving room for prompt)
    SAFE_MAX_CHARS = 4500 * 4 
    OVERLAP_CHARS = 500 * 4  # 500 tokens of overlap for context

    chunks = []
    current_idx = 0
    while current_idx < len(full_text):
        end_idx = min(current_idx + SAFE_MAX_CHARS, len(full_text))
        chunk_text = full_text[current_idx:end_idx]
        chunks.append(chunk_text)
        if end_idx == len(full_text):
            break
        current_idx = end_idx - OVERLAP_CHARS

    print(f"[INFO] Processing {len(pages)} page(s) into {len(chunks)} chunk(s) "
          f"(Max tokens per chunk ≈ {SAFE_MAX_CHARS//4}, Overlap ≈ {OVERLAP_CHARS//4})...")

    # 4. Extract sequentially to respect rate limits and process context
    batch_results: List[Dict[str, Any]] = []
    
    for idx, chunk in enumerate(chunks, 1):
        if idx > 1:
            chunk = f"[Context from previous part]:\n...{chunks[idx-2][-OVERLAP_CHARS:]}\n\n[Current part]:\n{chunk}"
        result = _extract_batch(llm, chunk, idx)
        batch_results.append(result)

    # 5. Merge all batches
    print("[INFO] Merging batch results...")
    merged = _merge_batches(batch_results)

    print(f"[INFO] Extraction complete.")
    return pages, merged


# ──────────────────────────────────────────────────────────────────────────────
# CLI TEST
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m extraction.pdf_extractor <resume.pdf>")
        sys.exit(1)

    _, details = extract_resume_kv(sys.argv[1])
    print("\n=== Extracted Resume Key-Value Pairs ===")
    print(json.dumps(details, indent=2))
