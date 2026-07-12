from utils.vector_store import similarity_search, format_context
from utils.web_search import web_search


def retrieve(query, vector_store):
    """
    Retrieve relevant context for a query.

    Strategy (improved):
    1. ALWAYS search the vector store first (from uploaded PDFs)
    2. ALWAYS supplement with web search for broader coverage
    3. Combine both sources to give agents the richest possible context

    This ensures that even if the PDF doesn't fully cover the specific
    question, the agents still have enough material to work with.

    Returns:
        tuple: (context_string, source_type) where source_type is
               'database', 'web', or 'database + web'
    """
    db_context = ""
    web_context = ""

    # Step 1: Search vector store (uploaded PDFs)
    try:
        results = similarity_search(vector_store, query, k=5)
        if results and len(results) > 0:
            db_context = format_context(results)
    except Exception:
        pass

    # Step 2: ALWAYS supplement with web search for broader coverage
    try:
        web_context = web_search(query)
    except Exception:
        pass

    # Step 3: Combine both sources
    if db_context and web_context:
        combined = (
            "=== FROM YOUR UPLOADED DOCUMENTS ===\n\n"
            f"{db_context}\n\n"
            "=== FROM WEB SEARCH (supplementary) ===\n\n"
            f"{web_context}"
        )
        return combined, "database + web"
    elif db_context:
        return db_context, "database"
    elif web_context:
        return web_context, "web"
    else:
        return "No relevant information found.", "none"
