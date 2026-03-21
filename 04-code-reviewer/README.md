# 🔍 AI Code Reviewer

An intelligent code review tool that automatically analyses your code,
researches best practices and produces a structured review report with
an improved version of your code.

## What makes this special
Most code review tools use static rules — they check for known patterns.
This tool **understands your code** — it reads it, thinks about it,
searches for relevant best practices and combines everything into a
human-quality review.

## How all 3 AI concepts combine here

| Concept | How it's used |
|---------|--------------|
| **Prompt Engineering** | Reviewer persona, structured output format |
| **RAG** | Code chunked and embedded, relevant sections retrieved for focused review |
| **Agentic AI** | Agent reads code, decides what to search, stops when satisfied |

## Architecture

```
Your Code
    ↓
Chunk by lines + embed into ChromaDB (RAG)
    ↓
Self-directed Agent reads code
    → searches best practices for each issue found
    → decides how many searches needed (not hardcoded!)
    → calls finish tool when satisfied
    ↓
RAG retrieves most relevant code sections
    ↓
Final LLM call combines:
    - Best practices research
    - Relevant code sections
    - Full code
    → Structured review report + improved code
```

## Self-Directed Agent
A key design decision — the agent decides how many searches to make,
not us. Simple code might need 3 searches. Complex code might need 10.
The agent judges this itself based on what it finds.

```python
# Instead of hardcoding:
max_iterations = 6  # ❌ we decided

# Agent signals when done:
{"tool": "finish", "input": "research complete"}  # ✅ agent decides
```

Only an emergency cap of 50 exists — in case something goes wrong,
not to limit the agent's thinking.

## Sample Output

```
🔍 AI Code Reviewer
==================================================
📂 Loading sample_code.py...
✅ Split into 6 chunks
🧠 Building code index...
✅ Indexed 6 chunks
🤖 Agent analysing code and searching best practices...
   🔍 Searching: 'Python error handling best practices'
   🔍 Searching: 'Python input validation'
   🔍 Searching: 'REST API security Python'
   🔍 Searching: 'Python list comprehension'
   ✅ Agent satisfied after 8 searches
📝 Generating review report...

📋 CODE REVIEW REPORT
==================================================
🐛 BUGS & ISSUES ...
⚠️  WARNINGS ...
💡 SUGGESTIONS ...
✨ IMPROVED VERSION ...
```

## Concepts Learned
- Chunking code by lines with overlap
- Embedding code into vector database
- Self-directed agentic loops with finish tool
- Emergency caps vs hardcoded limits
- Combining RAG + Agents in one pipeline
- Structured prompt engineering for consistent output format

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
```bash
python3 reviewer.py
```

Review report is saved to `review_report.txt` after each run.

## Try it on your own code
Replace `sample_code.py` with any Python file you want reviewed.
The agent will adapt its research depth automatically based on
what it finds in your code.