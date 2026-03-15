import os
from dotenv import load_dotenv  # type: ignore
from groq import Groq  # type: ignore

# ─── 1. LOAD ENVIRONMENT VARIABLES ───────────────────────────────
# Same as before — reads .env file
load_dotenv()

# ─── 2. INITIALISE GROQ CLIENT ───────────────────────────────────
# Groq works differently from Gemini — no separate configure step
# We just create a client with the API key directly
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ─── 3. LOAD THE RESUME ──────────────────────────────────────────
with open("resume.txt", "r") as f:
    resume = f.read()

# ─── 4. SYSTEM PROMPT ────────────────────────────────────────────
# Same concept as before — job description for the AI
system_prompt = f"""
You are a professional assistant representing Alex Rivera.
Answer questions about Alex using ONLY the information in the resume below.
If something is not in the resume, say "I don't have that information."
Keep answers concise and professional.

RESUME:
{resume}
"""

# ─── 5. CONVERSATION HISTORY ─────────────────────────────────────
# Remember our "fake memory" discussion?
# This is the list that grows with each message
# Groq follows the OpenAI message format — most AI APIs do actually
# Each message has a "role" and "content"
# Roles: "system" (instructions), "user" (human), "assistant" (AI)
messages = [{"role": "system", "content": system_prompt}]

# ─── 6. THE CONVERSATION LOOP ────────────────────────────────────
print("🤖 Resume Chatbot Ready! (type 'exit' to quit)\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if not user_input:
        continue

    # ─── 7. ADD USER MESSAGE TO HISTORY ──────────────────────────
    # Every new message gets appended to the list
    # This is the "fake memory" in action — history grows each turn
    messages.append({"role": "user", "content": user_input})

    # ─── 8. SEND TO GROQ API ─────────────────────────────────────
    # We send the ENTIRE messages list every time
    # model: llama-3.3-70b is Meta's latest open source model
    # 70b means 70 billion parameters — very capable
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=messages
    )

    # ─── 9. EXTRACT AND DISPLAY RESPONSE ─────────────────────────
    # Groq returns a structured object — we dig into it to get text
    assistant_message = response.choices[0].message.content
    print(f"\nAlex's Assistant: {assistant_message}\n")

    # ─── 10. ADD AI RESPONSE TO HISTORY TOO ──────────────────────
    # Important! We save the AI's reply in history as well
    # So next time, AI sees full conversation — both sides
    messages.append({"role": "assistant", "content": assistant_message})
