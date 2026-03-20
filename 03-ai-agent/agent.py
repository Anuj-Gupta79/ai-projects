import os
import json
from dotenv import load_dotenv  # type: ignore
from groq import Groq  # type: ignore
from tools import TOOLS, TOOL_DESCRIPTIONS

# ─── 1. LOAD ENVIRONMENT VARIABLES ───────────────────────────────
load_dotenv()

# ─── 2. INITIALISE GROQ CLIENT ───────────────────────────────────
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ─── 3. SYSTEM PROMPT ────────────────────────────────────────────
# This is the most important part of an agent
# We tell the AI exactly how to behave, what tools it has
# and CRITICALLY — how to communicate tool calls back to us
system_prompt = f"""
You are a helpful research assistant with access to tools.

{TOOL_DESCRIPTIONS}

IMPORTANT RULES:
1. When you need to use a tool, respond with ONLY raw JSON, no other text:
{{"tool": "tool_name", "input": "tool_input"}}

2. NEVER write JSON and text together in the same response.

3. NEVER put a tool call in your final answer.

4. Once you have enough information from tools, write ONLY plain text summary.

5. If search results contain partial info, combine with your own knowledge.

6. Think step by step before acting.
"""


# ─── 4. THE AGENT LOOP ───────────────────────────────────────────
# This is the core of agentic AI
# We keep looping until AI gives a plain text response
# (meaning it's done using tools and ready to answer)
def run_agent(user_goal: str):
    print(f"\n🎯 Goal: {user_goal}")
    print("─" * 50)

    # conversation history — same fake memory concept from project 1!
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_goal},
    ]

    # ─── 5. AGENTIC LOOP ─────────────────────────────────────────
    # max_iterations prevents infinite loops
    # if AI keeps calling tools forever, we stop at 10
    max_iterations = 10
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        print(f"\n🤔 Agent thinking... (step {iteration})")

        # Send current conversation to LLM
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", messages=messages
        )

        ai_message = response.choices[0].message.content.strip()

        # ─── 6. PARSE RESPONSE ───────────────────────────────────
        # Extract first JSON object found in the response
        clean_message = ai_message.strip()

        # Remove code blocks if present
        if clean_message.startswith("```"):
            clean_message = clean_message.split("\n", 1)[1]
            clean_message = clean_message.rsplit("```", 1)[0]

        # Find first { and last } to extract just one JSON object
        start = clean_message.find("{")
        end = clean_message.find("}") + 1

        if start != -1 and end != 0:
            try:
                json_str = clean_message[start:end]
                tool_call = json.loads(json_str)
                tool_name = tool_call.get("tool")
                tool_input = tool_call.get("input")

                # ─── 7. EXECUTE TOOL ─────────────────────────────
                if tool_name in TOOLS:
                    print(f"🔧 Using tool: {tool_name}('{tool_input}')")
                    tool_result = TOOLS[tool_name](tool_input)
                    print(f"📥 Result: {tool_result[:200]}...")

                    messages.append({"role": "assistant", "content": ai_message})
                    messages.append(
                        {
                            "role": "user",
                            "content": f"Tool result for {tool_name}: {tool_result}",
                        }
                    )
                else:
                    print(f"❌ Unknown tool: {tool_name}")
                    break

            except json.JSONDecodeError:
                # Has { } but not valid JSON — treat as final answer
                print("\n✅ Agent finished research!")
                print("\n" + "─" * 50)
                print("📋 FINAL ANSWER:")
                print("─" * 50)
                print(ai_message)
                print("─" * 50)
                return
        else:
            # No JSON found — this is the final answer
            print("\n✅ Agent finished research!")
            print("\n" + "─" * 50)
            print("📋 FINAL ANSWER:")
            print("─" * 50)
            print(ai_message)
            print("─" * 50)
            return

    print("⚠️ Max iterations reached")


# ─── 10. MAIN LOOP ───────────────────────────────────────────────
print("🤖 AI Research Agent Ready! (type 'exit' to quit)\n")

while True:
    user_input = input("\nYou: ").strip()

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if not user_input:
        continue

    run_agent(user_input)
