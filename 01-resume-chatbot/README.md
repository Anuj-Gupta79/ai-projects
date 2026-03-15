# 🤖 Resume Chatbot

A terminal-based AI chatbot that answers questions about a person's resume.

## Concepts Learned

- Calling an AI API (Groq + Llama 3.3 70b)
- System prompt engineering
- Conversation history (how AI "fake memory" works)

## How it works

1. Resume is loaded as text
2. Injected into a system prompt
3. User asks questions in terminal
4. AI answers using ONLY resume context
5. Conversation history grows each turn creating illusion of memory

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add your `GEMINI_API_KEY` to a `.env` file:

```
GROQ_API_KEY=your_key_here
```

## Run

```bash
python3 chatbot.py
```
