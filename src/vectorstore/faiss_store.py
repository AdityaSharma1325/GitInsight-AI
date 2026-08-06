from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from src.embeddings.embedding_model import get_embedding_model


def create_faiss_index(chunks):
    """
    Creates a FAISS vector store from chunks.
    """

    embedding_model = get_embedding_model()

    documents = []

    for chunk in chunks:

        documents.append(
            Document(
                page_content=chunk["content"],
                metadata={
                    "source": chunk["source"],
                    "extension": chunk["extension"],
                    "chunk_length": len(chunk["content"])
                }
            )
        )

    vectorstore = FAISS.from_documents(
        documents,
        embedding_model
    )

    return vectorstore

# Save the FAISS Index
def save_faiss_index(vectorstore):
     """
     save faiss index locally
     """
     vectorstore.save_local("faiss_index")

def load_faiss_index():
    """
    Load FAISS index from disk
    """

    embedding_model = get_embedding_model()

    return FAISS.load_local(
        "faiss_index",
        embedding_model,
        allow_dangerous_deserialization=True
    )
