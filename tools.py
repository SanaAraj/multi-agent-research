from duckduckgo_search import DDGS


def web_search(query: str, max_results: int = 5) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return f"No results found for: {query}"

        formatted = []
        for r in results:
            title = r.get("title", "")
            body = r.get("body", "")
            formatted.append(f"**{title}**\n{body}")

        return "\n\n".join(formatted)

    except Exception as e:
        return f"Search error: {str(e)}"


def mock_search(query: str) -> str:
    return f"""**{query} Overview**
{query} is an important area of study with significant developments in recent years.
Key aspects include technology advancement, policy changes, and market growth.

**Recent Developments in {query}**
Experts report major breakthroughs in this field. Investment has increased substantially.
New applications are emerging across multiple industries.

**Future of {query}**
Analysts predict continued growth and innovation. Challenges remain but progress is steady.
The field is expected to transform multiple sectors in the coming decade."""
