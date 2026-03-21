# 🧠 AI Projects — Learning Journey

A collection of hands-on projects built to understand Generative AI,
prompt engineering and agentic AI from scratch.

Built with zero prior AI experience. Each project introduces new concepts
and builds on the previous one.

## Projects

| #   | Project                                 | Concepts Covered                                            | Status  |
| --- | --------------------------------------- | ----------------------------------------------------------- | ------- |
| 01  | [Resume Chatbot](./01-resume-chatbot/)  | API calls, Prompt Engineering, Fake Memory                  | ✅ Done |
| 02  | [Document Q&A Tool](./02-document-qa/)  | RAG, Embeddings, Vector Search, ChromaDB                    | ✅ Done |
| 03  | [AI Research Agent](./03-ai-agent/)     | Agentic AI, Tool Use, Multi-step Reasoning                  | ✅ Done |
| 04  | [AI Code Reviewer](./04-code-reviewer/) | RAG + Agentic AI + Self-directed Agent + Prompt Engineering | ✅ Done |

## What I Learned

- How Generative AI works under the hood — API calls, tokens, context windows
- Prompt engineering — system prompts, personas, structured outputs
- RAG (Retrieval Augmented Generation) — chunking, embeddings, vector search
- Agentic AI — tool use, autonomous planning, self-directed agents
- The difference between GenAI and Agentic AI in practice

## The Learning Curve

```
Project 1 → You control everything, AI just responds
Project 2 → AI answers from your documents intelligently
Project 3 → AI plans and acts autonomously with tools
Project 4 → All three combined into one real product
```

## Tech Stack

- **Language** — Python
- **LLM** — Groq (Llama 3.3 70b)
- **Embeddings** — sentence-transformers (local, free)
- **Vector DB** — ChromaDB
- **APIs** — Wikipedia, wttr.in

## Setup

Each project has its own folder with its own `README.md` and `requirements.txt`.
Navigate into any project folder and follow its setup instructions:

```bash
cd 01-resume-chatbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
