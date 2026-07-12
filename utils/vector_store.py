from langchain_astradb import AstraDBVectorStore
from config import get_embeddings, ASTRA_DB_API_ENDPOINT, ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_COLLECTION_NAME


def get_vector_store():
    """Connect to AstraDB and return a vector store instance."""
    embeddings = get_embeddings()
    vector_store = AstraDBVectorStore(
        embedding=embeddings,
        collection_name=ASTRA_DB_COLLECTION_NAME,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
    )
    return vector_store


def add_documents(vector_store, documents):
    """Add document chunks to the vector store."""
    vector_store.add_documents(documents)
    return len(documents)


def similarity_search(vector_store, query, k=5):
    """Search for the top-k most similar documents in the vector store."""
    results = vector_store.similarity_search(query, k=k)
    return results


def format_context(documents):
    """Format retrieved documents into a readable context string."""
    if not documents:
        return ""
    context_parts = []
    for i, doc in enumerate(documents, 1):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")
        context_parts.append(f"[Source {i} | Page {page}]\n{doc.page_content}")
    return "\n\n---\n\n".join(context_parts)
