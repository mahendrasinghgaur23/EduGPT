from langchain.chains import LLMChain
from config import get_llm, call_with_retry
from prompts.quiz_prompt import quiz_prompt


def generate_quiz(summary, topic):
    """
    Generate 5 MCQs from summary notes to test student understanding.

    Uses a moderate temperature (0.5) for variety while maintaining accuracy.
    Includes automatic retry on rate limit errors.

    Args:
        summary: The summarized study notes
        topic: The user's question or topic

    Returns:
        str: Formatted quiz questions in markdown
    """
    llm = get_llm(temperature=0.5)
    chain = LLMChain(llm=llm, prompt=quiz_prompt)
    result = call_with_retry(chain, {"topic": topic, "summary": summary})
    return result
