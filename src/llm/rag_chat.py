from src.llm.client import get_llm_client
from src.llm.prompt_builder import build_prompt
from src.retrieval.search import semantic_search
from src.memory.conversation import get_recent_history


MODEL_NAME = "llama-3.3-70b-versatile"


def ask_repository(question,history):
    """
    Complete RAG pipeline.
    """

    docs = semantic_search(question)

    prompt = build_prompt(
        question,
        docs
    )

    messages = [
        {
            "role": "system",
            "content": "You are an expert AI software engineer. Answer only using the repository context."
        }
    ]

    recent_history = get_recent_history(history)

    messages.extend(recent_history)

    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    client = get_llm_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2
    )

    answer = response.choices[0].message.content

    return answer, docs
