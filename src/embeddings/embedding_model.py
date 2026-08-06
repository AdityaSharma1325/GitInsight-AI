from langchain_community.embeddings import HuggingFaceEmbeddings

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def get_embedding_model():
    """
    Return the embedding model
    """

    return HuggingFaceEmbeddings(
        model_name = MODEL_NAME
    )