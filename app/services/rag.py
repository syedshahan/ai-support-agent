from sqlalchemy.orm import Session

from app.services.retrieval import search_similar_chunks


def get_rag_context(
    db: Session,
    question: str,
) -> str:

    chunks = search_similar_chunks(
        db=db,
        query=question,
        limit=3,
    )

    return "\n\n".join(
        chunk.content
        for chunk in chunks
    )