from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
    )

    chunks = []

    for document in documents:
        document_chunks = splitter.split_text(
            document["content"]
        )

        for chunk in document_chunks:
            chunks.append(
                {
                    "source": document["source"],
                    "content": chunk,
                }
            )

    return chunks