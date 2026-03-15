# 📄 Document Q&A Tool

A terminal-based RAG (Retrieval Augmented Generation) pipeline that lets you 
chat with any PDF document intelligently.

## What is RAG?
Instead of sending an entire document to AI (expensive, limited by context window),
RAG splits the document into chunks, converts them to vectors, stores them in a 
vector database, and only retrieves relevant chunks when a question is asked.

> Smart search first, AI answers second.

## Concepts Learned
- RAG pipeline end to end
- Text chunking with overlap
- Embeddings — converting text to vectors (384 numbers per chunk)
- Vector similarity search with ChromaDB
- Augmented prompt generation
- Source citation in AI answers

## How it works

### Phase 1 — Indexing (run once)
```
PDF → Extract text → Split into chunks → Convert to vectors → Store in ChromaDB
```

### Phase 2 — Querying (run every question)
```
Question → Convert to vector → Search ChromaDB → Send top 3 chunks to AI → Answer
```

## Tech Stack
- **Groq + Llama 3.3 70b** — LLM for answering
- **sentence-transformers** — local embedding model (no API cost)
- **ChromaDB** — local vector database
- **pypdf** — PDF text extraction

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add your Groq API key to `.env`:
```
GROQ_API_KEY=your_key_here
```

## Run

**Step 1 — Index your PDF** (run once or when document changes)
```bash
python3 ingest.py
```

**Step 2 — Ask questions**
```bash
python3 query.py
```

## Pro tip
RAG works best with specific questions, not vague ones.

✅ "What were the BLEU scores in the experiments?"
❌ "What is this document about?"

The more specific your question, the better the vector match,
the better the answer.

## Paper used for testing
**"Attention Is All You Need"** — Vaswani et al. (2017)
The original Transformer paper that powers every modern AI model.