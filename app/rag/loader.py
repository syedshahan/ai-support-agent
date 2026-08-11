from pathlib import Path

DOCUMENTS_PATH = Path("documents")

def load_documents():
    documents = []

    for file_path in DOCUMENTS_PATH.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "source": file_path.name,
                "content": content,
            }
        )

    return documents
