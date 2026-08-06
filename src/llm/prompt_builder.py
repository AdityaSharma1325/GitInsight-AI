def build_prompt(question, retrieved_docs):
    """
    Build the RAG prompt.
    """

    context = "\n\n".join(
        [
            f"Source: {doc.metadata['source']}\n{doc.page_content}"
            for doc in retrieved_docs
        ]
    )

    prompt = f"""
You are an expert Software Engineer.

You are answering questions ONLY using the repository context below.

If the answer cannot be found inside the repository, say:

"I couldn't find this information in the repository."

Repository Context:

{context}

-----------------------

Question:

{question}

Answer:
"""

    return prompt