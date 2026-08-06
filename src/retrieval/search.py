from src.vectorstore.faiss_store import load_faiss_index

def semantic_search(query:str, top_k:int=5):
    """
    Search the FASISS index for the most relevant chunks
    """
    vectorstore = load_faiss_index()

    results = vectorstore.similarity_search(
          query = query,
          k = 10
    )

    results = [
        doc for doc in results
        if doc.metadata["extension"] in {
            ".py",
            ".js",
            ".ts",
            ".java",
            ".cpp",
            ".go",
        }
    ]

    return results[:top_k]