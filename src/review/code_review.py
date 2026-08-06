from src.retrieval.search import semantic_search
from src.llm.client import get_llm_client

MODEL_NAME = "llama-3.3-70b-versatile"


def review_repository():
    """
    Generate an AI code review for the repository.
    """

    queries = [
        "main application",
        "repository architecture",
        "error handling",
        "code quality",
        "project structure",
        "performance"
    ]

    docs = []

    for query in queries:
        docs.extend(
            semantic_search(query, top_k=2)
        )

    # Remove duplicates
    unique_docs = []
    seen = set()

    for doc in docs:

        key = (doc.metadata["source"], doc.page_content)

        if key not in seen:
            unique_docs.append(doc)
            seen.add(key)

    context = "\n\n".join(
        [
            f"File: {doc.metadata['source']}\n{doc.page_content}"
            for doc in unique_docs
        ]
    )

    prompt = f"""
You are a Senior Software Engineer performing a professional code review.

Review this repository.

Provide:

1. Overall Code Quality
2. Strengths
3. Weaknesses
4. Possible Bugs
5. Performance Improvements
6. Security Improvements
7. Best Practice Suggestions

Repository:

{context}
"""

    client = get_llm_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.2,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content