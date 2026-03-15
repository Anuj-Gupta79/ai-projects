import os
from pypdf import PdfReader  # type: ignore
from sentence_transformers import SentenceTransformer  # type: ignore
import chromadb  # type: ignore

# ─── 1. LOAD THE PDF ─────────────────────────────────────────────
# PdfReader opens the PDF and lets us access each page
# We loop through all pages and extract text from each
print("📄 Loading PDF...")
reader = PdfReader("research-paper.pdf")
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()

print(f"✅ Extracted {len(full_text)} characters from {len(reader.pages)} pages")

# ─── 2. SPLIT INTO CHUNKS ────────────────────────────────────────
# We can't embed the whole document at once
# So we split into chunks of ~500 characters with 50 char overlap
# Overlap is important — so we don't lose context at chunk boundaries
# Example: if a sentence starts at end of chunk 1 and ends at chunk 2
# the overlap makes sure it appears in both chunks
print("\n✂️  Splitting into chunks...")

chunk_size = 500
chunk_overlap = 50
chunks = []

start = 0
while start < len(full_text):
    end = start + chunk_size
    chunk = full_text[start:end]
    if chunk.strip():  # skip empty chunks
        chunks.append(chunk)
    start = end - chunk_overlap  # overlap with previous chunk

print(f"✅ Created {len(chunks)} chunks")

# ─── 3. LOAD EMBEDDING MODEL ─────────────────────────────────────
# sentence-transformers runs LOCALLY on your machine
# No API call, no cost, no internet needed after first download
# all-MiniLM-L6-v2 is small but very capable — perfect for learning
print("\n🧠 Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Embedding model loaded")

# ─── 4. CONVERT CHUNKS TO VECTORS ───────────────────────────────
# .encode() takes a list of strings and returns a list of vectors
# Each vector is an array of 384 numbers for this model
# This is where text becomes numbers!
print("\n🔢 Converting chunks to vectors...")
embeddings = embedding_model.encode(chunks, show_progress_bar=True)
print(f"✅ Created {len(embeddings)} vectors of size {len(embeddings[0])}")

# ─── 5. STORE IN CHROMADB ────────────────────────────────────────
# ChromaDB creates a local folder called chroma_db on your machine
# It stores both the vectors AND the original text chunks together
# So when we search, we get back the actual text, not just numbers
print("\n💾 Storing in ChromaDB...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Delete collection if it already exists (clean re-index)
try:
    chroma_client.delete_collection("documents")
except:
    pass

collection = chroma_client.create_collection("documents")

# Add everything to ChromaDB
# ids     — unique identifier for each chunk
# embeddings — the vectors
# documents  — the original text (so we can retrieve it later)
collection.add(
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    embeddings=embeddings.tolist(),
    documents=chunks,
)

print(f"✅ Stored {len(chunks)} chunks in ChromaDB")
print("\n🎉 Indexing complete! You can now run query.py")
