import requests
import json


# ─── TOOL 1: WEB SEARCH ──────────────────────────────────────────
# Uses DuckDuckGo's free API — no key needed!
# Returns top 3 search results with title, url and snippet
def web_search(query: str) -> str:
    """Search Wikipedia and return summary"""
    try:
        headers = {"User-Agent": "ai-research-agent/1.0 (learning project)"}

        # Remove common question words to get the core topic
        # "who founded OpenAI" → "OpenAI"
        # "when was Python created" → "Python"
        stop_words = [
            "who",
            "what",
            "when",
            "where",
            "why",
            "how",
            "founded",
            "created",
            "invented",
            "is",
            "are",
            "was",
            "were",
            "the",
            "a",
            "an",
            "of",
            "for",
            "tell",
            "me",
            "about",
            "search",
            "find",
        ]
        words = query.lower().split()
        topic_words = [w for w in words if w not in stop_words]
        clean_query = " ".join(topic_words) if topic_words else query

        print(f"   🔍 Searching Wikipedia for: '{clean_query}'")

        # Search endpoint to find the right page
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "opensearch",
            "search": clean_query,
            "limit": 1,
            "format": "json",
        }
        response = requests.get(search_url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        if not data[1]:
            return f"No results found for: {clean_query}"

        top_title = data[1][0]

        # Fetch full summary for that title
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{top_title.replace(' ', '_')}"
        summary_response = requests.get(summary_url, headers=headers, timeout=5)
        summary_response.raise_for_status()
        summary_data = summary_response.json()

        extract = summary_data.get("extract", "")
        if extract:
            return f"{top_title}: {extract[:1000]}"

        return f"No summary found for: {top_title}"

    except Exception as e:
        return f"Search error: {str(e)}"


# ─── TOOL 2: WEATHER ─────────────────────────────────────────────
# Uses wttr.in — completely free, no API key needed
# Returns current weather for any city
def get_weather(city: str) -> str:
    """Get current weather for a city"""
    try:
        # wttr.in is a free weather service with a simple API
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"Could not get weather for {city}"
    except Exception as e:
        return f"Weather error: {str(e)}"


# ─── TOOL 3: CALCULATOR ──────────────────────────────────────────
# Safe math evaluator — no imports, no security risk
# Handles basic arithmetic the AI might need
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression"""
    try:
        # We only allow safe characters — no exec() risk
        allowed = set("0123456789+-*/()., ")
        if not all(c in allowed for c in expression):
            return "Error: only basic arithmetic allowed"
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"


# ─── TOOL REGISTRY ───────────────────────────────────────────────
# This dictionary maps tool names to functions
# When AI says "use web_search", we look it up here and call it
# Easy to add new tools — just add a function and register it here
TOOLS = {"web_search": web_search, "get_weather": get_weather, "calculate": calculate}

# Tool descriptions — this is what we show the AI
# Good descriptions = AI uses tools correctly
TOOL_DESCRIPTIONS = """
You have access to these tools:

1. web_search(query) — Search the web for current information
   Use when: you need facts, news, or information about any topic

2. get_weather(city) — Get current weather for any city
   Use when: asked about weather or climate in a location

3. calculate(expression) — Evaluate a math expression
   Use when: you need to compute numbers accurately
"""
