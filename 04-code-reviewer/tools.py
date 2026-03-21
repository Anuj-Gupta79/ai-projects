import requests


def web_search(query: str) -> str:
    """Search Wikipedia for best practices and programming concepts"""
    try:
        headers = {"User-Agent": "ai-code-reviewer/1.0 (learning project)"}

        # Clean query — remove question words, keep technical terms
        stop_words = [
            "what",
            "how",
            "why",
            "when",
            "where",
            "is",
            "are",
            "the",
            "a",
            "an",
            "for",
            "to",
            "in",
            "of",
            "and",
        ]
        words = query.lower().split()
        topic_words = [w for w in words if w not in stop_words]
        clean_query = " ".join(topic_words) if topic_words else query

        # Step 1 — find the best matching page
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

        # Step 2 — fetch full summary
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


# Tool registry — easy to add more tools later
TOOLS = {"web_search": web_search}

TOOL_DESCRIPTIONS = """
You have access to this tool:

1. web_search(query) — Search for programming best practices and concepts
   Use when: you need to look up best practices for a pattern you found in the code
   Example queries: "Python error handling best practices", "REST API security"
"""