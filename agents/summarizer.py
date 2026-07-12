from langchain.chains import LLMChain
from config import get_llm, call_with_retry
from prompts.summarizer_prompt import summarizer_prompt


def summarize(context, topic):
    """
    Generate concise, well-structured study notes from retrieved context.

    Uses a lower temperature (0.3) for factual accuracy and consistency.
    Includes automatic retry on rate limit errors.

    Args:
        context: The retrieved raw context text
        topic: The user's question or topic

    Returns:
        str: Formatted study notes in markdown
    """
    llm = get_llm(temperature=0.3)
    chain = LLMChain(llm=llm, prompt=summarizer_prompt)
    result = call_with_retry(chain, {"topic": topic, "context": context})
    return result
