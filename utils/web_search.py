from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper


def search_wikipedia(query, max_results=3):
    """Search Wikipedia for relevant content."""
    try:
        wiki_wrapper = WikipediaAPIWrapper(
            top_k_results=max_results, doc_content_chars_max=4000
        )
        wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)
        result = wiki_tool.run(query)
        return result
    except Exception:
        return ""


def search_duckduckgo(query, max_results=5):
    """Search DuckDuckGo for relevant content."""
    try:
        ddg_wrapper = DuckDuckGoSearchAPIWrapper(max_results=max_results)
        search_tool = DuckDuckGoSearchRun(api_wrapper=ddg_wrapper)
        result = search_tool.run(query)
        return result
    except Exception:
        return ""


def web_search(query):
    """Combined web search: tries Wikipedia first, then DuckDuckGo as fallback."""
    # Try Wikipedia first (higher quality content)
    wiki_result = search_wikipedia(query)

    # Try DuckDuckGo as supplementary source
    ddg_result = search_duckduckgo(query)

    combined = ""
    if wiki_result:
        combined += f"Wikipedia:\n{wiki_result}\n\n"
    if ddg_result:
        combined += f"Web Search:\n{ddg_result}\n\n"

    if not combined:
        combined = "No relevant information found from web sources."

    return combined
