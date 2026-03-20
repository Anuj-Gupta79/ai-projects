---

### Project 3 is done! Let's wrap it up.

**1. Save dependencies**
```bash
pip freeze > requirements.txt
```

**2. Create `README.md`** — here it is:

```markdown
# 🤖 AI Research Agent

A terminal-based agentic AI that plans, uses tools, and completes 
goals autonomously — without being told which steps to take.

## Agentic vs Generative AI
- **GenAI** → you ask, it answers
- **Agentic AI** → you give a goal, it figures out the steps

## Tools Available
- `web_search` — searches Wikipedia for factual information
- `get_weather` — gets real time weather for any city
- `calculate` — evaluates math expressions safely

## Concepts Learned
- Tool use and function calling
- Agentic loop — reason, act, observe, repeat
- JSON as communication between AI and code
- Prompt engineering for structured outputs
- Handling LLM unpredictability in production

## How it works
```
User gives goal
     ↓
Agent thinks → responds with JSON tool call
     ↓
Code executes tool → sends result back to agent
     ↓
Agent thinks again → another tool or final answer
     ↓
Repeat until agent is satisfied
```

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
python3 agent.py
```

## Example goals to try
- "What is the weather in Tokyo and how many days until New Year 2026?"
- "Search for Python programming language and calculate 2025 minus its creation year"
- "Get weather in London and calculate 20% tip on a £60 bill"