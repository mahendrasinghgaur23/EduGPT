from langchain.chains import LLMChain
from config import get_llm, call_with_retry
from prompts.explainer_prompt import explainer_prompt


def explain(summary, topic):
    """
    Generate a personal tutor-style explanation from summary notes.

    Uses a higher temperature (0.7) for creative, engaging explanations.
    Includes automatic retry on rate limit errors.

    Args:
        summary: The summarized study notes
        topic: The user's question or topic

    Returns:
        str: Personal tutor explanation in markdown
    """
    llm = get_llm(temperature=0.7)
    chain = LLMChain(llm=llm, prompt=explainer_prompt)
    result = call_with_retry(chain, {"topic": topic, "summary": summary})
    return result
