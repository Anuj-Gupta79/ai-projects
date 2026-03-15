import os
from dotenv import load_dotenv # type: ignore
from sentence_transformers import SentenceTransformer # type: ignore
import chromadb # type: ignore
from groq import Groq # type: ignore

# ─── 1. LOAD ENVIRONMENT VARIABLES ───────────────────────────────
load_dotenv()

# ─── 2. INITIALISE GROQ CLIENT ───────────────────────────────────
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ─── 3. LOAD EMBEDDING MODEL ─────────────────────────────────────
# Same model as ingest.py — MUST be the same model
# Because vectors only make sense when compared using same model
# Different model = different vector space = wrong results
print("🧠 Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ─── 4. CONNECT TO CHROMADB ──────────────────────────────────────
# We connect to the same chroma_db folder created by ingest.py
# This is why we called it PersistentClient — data survives between runs
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection("documents")

print(f"✅ Connected to ChromaDB — {collection.count()} chunks loaded")
print("\n📄 Document Q&A Ready! (type 'exit' to quit)\n")

# ─── 5. CONVERSATION LOOP ────────────────────────────────────────
while True:
    user_question = input("You: ").strip()

    if user_question.lower() == "exit":
        print("Goodbye!")
        break

    if not user_question:
        continue

    # ─── 6. CONVERT QUESTION TO VECTOR ───────────────────────────
    # Same process as ingest.py — text becomes numbers
    # Now we can compare this vector against our stored chunk vectors
    question_vector = embedding_model.encode([user_question]).tolist()

    # ─── 7. SEARCH CHROMADB FOR SIMILAR CHUNKS ───────────────────
    # n_results=3 — fetch top 3 most similar chunks
    # ChromaDB compares question vector against all 89 chunk vectors
    # Returns the chunks whose vectors are closest in meaning
    results = collection.query(query_embeddings=question_vector, n_results=3)

    # ─── 8. EXTRACT THE RELEVANT CHUNKS ──────────────────────────
    # results["documents"][0] gives us list of 3 matching text chunks
    relevant_chunks = results["documents"][0]

    # Join chunks into one context block to send to AI
    context = "\n\n---\n\n".join(relevant_chunks)

    # ─── 9. BUILD PROMPT WITH CONTEXT ────────────────────────────
    # This is RAG in action — we're AUGMENTING the prompt with
    # RETRIEVED context before GENERATING the answer
    # Notice: we only send 3 relevant chunks, not the whole document!
    prompt = f"""Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I couldn't find that in the document."
Always mention which part of the document your answer comes from.

CONTEXT:
{context}

QUESTION:
{user_question}
"""

    # ─── 10. SEND TO GROQ ────────────────────────────────────────
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    # ─── 11. PRINT ANSWER + SOURCES ──────────────────────────────
    # We show the answer AND the raw chunks used
    # This is called "citing sources" — important in real RAG apps
    # User can verify the AI didn't make anything up
    print(f"\n🤖 Answer: {answer}")
    print("\n📚 Sources used:")
    for i, chunk in enumerate(relevant_chunks):
        print(f"\n  Chunk {i+1}: ...{chunk[:150]}...")
    print()
