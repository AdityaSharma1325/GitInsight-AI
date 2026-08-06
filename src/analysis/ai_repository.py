from src.retrieval.search import semantic_search
from src.llm.client import get_llm_client

MODEL_NAME = "llama-3.3-70b-versatile"


def analyze_repository_ai():
    """
    Generate an AI overview of the repository.
    """

    queries = [
        "Explain the overall project.",
        "What is the architecture?",
        "What are the main components?",
        "What technologies are used?"
    ]

    retrieved_docs = []

    for query in queries:
        retrieved_docs.extend(
            semantic_search(query, top_k=2)
        )

    # Remove duplicate chunks
    unique_docs = []
    seen = set()

    for doc in retrieved_docs:
        key = (doc.metadata["source"], doc.page_content)

        if key not in seen:
            unique_docs.append(doc)
            seen.add(key)

    context = "\n\n".join(
        f"File: {doc.metadata['source']}\n{doc.page_content}"
        for doc in unique_docs
    )

    prompt = f"""
You are an expert software architect.

Analyze this GitHub repository.

Provide:

1. Project Purpose
2. Overall Workflow
3. Main Components
4. Technologies Used
5. Entry Point
6. Important Files
7. Suggestions for Improvement

Repository Context:

{context}
"""

    client = get_llm_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content