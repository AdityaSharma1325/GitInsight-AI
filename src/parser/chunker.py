from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):
    """
    Split repository documents into chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        separators = [
            "\nclass ",
            "\ndef ",
            "\n\n",
            "\n",
            " ",
            "",
        ],
        chunk_size = 1000,
        chunk_overlap=200
    )
    

    chunks = []

    for document in documents:

        split_text = splitter.split_text(
            document["content"]
        )

        for chunk in split_text:

            chunks.append(
                {
                    "source": document["source"],
                    "content": chunk,
                    "extension": document["extension"]
                }
            )

    return chunks
