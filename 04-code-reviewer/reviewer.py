import os
import json
from dotenv import load_dotenv  # type: ignore
from groq import Groq  # type: ignore
from sentence_transformers import SentenceTransformer  # type: ignore
import chromadb  # type: ignore
from tools import TOOLS, TOOL_DESCRIPTIONS

# Add finish tool — signals agent is done researching
TOOLS["finish"] = lambda x: x

# ─── 1. SETUP ────────────────────────────────────────────────────
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# ─── 2. LOAD AND CHUNK THE CODE ──────────────────────────────────
# Same chunking concept as Project 2 but for code
# We split by lines instead of characters — more natural for code
def load_and_chunk_code(filepath: str) -> list:
    with open(filepath, "r") as f:
        lines = f.readlines()

    chunks = []
    chunk_size = 20  # 20 lines per chunk
    overlap = 3  # 3 lines overlap — keeps function context

    for i in range(0, len(lines), chunk_size - overlap):
        chunk = "".join(lines[i : i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)

    return chunks


# ─── 3. BUILD VECTOR DB FROM CODE ────────────────────────────────
# Same as Project 2 — embed chunks and store in ChromaDB
# But this time we're embedding CODE not documents
def build_code_index(chunks: list):
    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    try:
        chroma_client.delete_collection("code")
    except:
        pass

    collection = chroma_client.create_collection("code")
    embeddings = embedding_model.encode(chunks)

    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        embeddings=embeddings.tolist(),
        documents=chunks,
    )

    return collection


# ─── 4. RETRIEVE RELEVANT CODE SECTIONS ──────────────────────────
# Given a question/concern, find the most relevant code chunks
# This is RAG — retrieve before generating
def retrieve_relevant_code(collection, query: str, n=3) -> str:
    question_vector = embedding_model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=question_vector, n_results=min(n, collection.count())
    )
    return "\n\n---\n\n".join(results["documents"][0])


# ─── 5. AGENT — DECIDES WHAT TO SEARCH ───────────────────────────
# First pass — agent reads the code and decides what to search for
# This is the agentic part — AI decides its own research agenda
def research_best_practices(code: str) -> str:
    print("\n🤖 Agent analysing code and searching best practices...")

    system_prompt = f"""
You are a code analysis agent. Your job is to:
1. Read the provided code carefully
2. Identify ALL programming patterns, languages and potential issues
3. Search for best practices for each issue you find
4. Decide yourself when you have enough information
5. Return a summary of relevant best practices

{TOOL_DESCRIPTIONS}

RULES:
1. Search for best practices for EACH distinct issue you find
2. For tool calls respond with ONLY raw JSON:
{{"tool": "web_search", "input": "your search query"}}
3. When YOU are satisfied with your research, signal completion with:
{{"tool": "finish", "input": "research complete"}}
4. After finish tool write a plain text summary of best practices found
5. NEVER mix JSON and text in the same response
6. YOU decide how many searches are needed — not us
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Analyse this code and search for relevant best practices:\n\n{code}",
        },
    ]

    best_practices = []
    emergency_cap = 50
    iteration = 0

    while iteration < emergency_cap:
        iteration += 1

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", messages=messages
        )

        ai_message = response.choices[0].message.content.strip()

        # Parse response — same pattern as Project 3
        clean_message = ai_message.strip()
        if clean_message.startswith("```"):
            clean_message = clean_message.split("\n", 1)[1]
            clean_message = clean_message.rsplit("```", 1)[0]

        start = clean_message.find("{")
        end = clean_message.find("}") + 1

        if start != -1 and end != 0:
            try:
                json_str = clean_message[start:end]
                tool_call = json.loads(json_str)
                tool_name = tool_call.get("tool")
                tool_input = tool_call.get("input")

                if tool_name == "finish":
                    # Agent decided it's done — respect that decision
                    print(f"   ✅ Agent satisfied after {iteration} searches")
                    break

                elif tool_name in TOOLS:
                    print(f"   🔍 Searching: '{tool_input}'")
                    tool_result = TOOLS[tool_name](tool_input)
                    best_practices.append(f"Query: {tool_input}\nResult: {tool_result}")

                    messages.append({"role": "assistant", "content": ai_message})
                    messages.append(
                        {
                            "role": "user",
                            "content": f"Search result: {tool_result}. Continue searching if needed or call finish tool when done.",
                        }
                    )
            except json.JSONDecodeError:
                # Final summary from agent
                best_practices.append(ai_message)
                break
        else:
            # Plain text — agent is done
            best_practices.append(ai_message)
            break

    return "\n\n".join(best_practices)


# ─── 6. MAIN REVIEWER ────────────────────────────────────────────
# This is the final step — takes code + best practices
# and produces a structured review report
def review_code(code: str, best_practices: str, relevant_sections: str) -> str:
    print("\n📝 Generating review report...")

    review_prompt = f"""
You are a senior software engineer doing a thorough code review.

BEST PRACTICES RESEARCH:
{best_practices}

RELEVANT CODE SECTIONS:
{relevant_sections}

FULL CODE:
{code}

Write a detailed code review report with these exact sections:

🐛 BUGS & ISSUES
List actual bugs that could cause crashes or wrong behaviour.
For each: describe the issue, which line/function, why it's a problem.

⚠️ WARNINGS  
List code smells, bad practices, and maintainability issues.

💡 SUGGESTIONS
List improvements for readability, performance and pythonic style.

✨ IMPROVED VERSION
Rewrite the entire code with all issues fixed.
Add comments explaining what you changed and why.

Be specific, reference actual line numbers and function names.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": review_prompt}],
        max_tokens=4000,
    )

    return response.choices[0].message.content


# ─── 7. MAIN FLOW ────────────────────────────────────────────────
def main():
    print("🔍 AI Code Reviewer")
    print("=" * 50)

    # Load code
    filepath = "sample_code.py"
    print(f"\n📂 Loading {filepath}...")
    chunks = load_and_chunk_code(filepath)
    print(f"✅ Split into {len(chunks)} chunks")

    # Read full code for review
    with open(filepath, "r") as f:
        full_code = f.read()

    # Build vector index
    print("\n🧠 Building code index...")
    collection = build_code_index(chunks)
    print(f"✅ Indexed {collection.count()} chunks")

    # Agent searches best practices
    best_practices = research_best_practices(full_code)

    # RAG — retrieve most relevant sections for focused review
    print("\n🎯 Retrieving relevant code sections...")
    relevant_sections = retrieve_relevant_code(
        collection, "error handling bugs security issues", n=3
    )

    # Generate review
    review = review_code(full_code, best_practices, relevant_sections)

    # Output report
    print("\n" + "=" * 50)
    print("📋 CODE REVIEW REPORT")
    print("=" * 50)
    print(review)

    # Save report to file
    with open("review_report.txt", "w") as f:
        f.write(review)
    print("\n💾 Report saved to review_report.txt")


if __name__ == "__main__":
    main()
