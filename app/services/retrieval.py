from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import DocumentChunk
from app.rag.embeddings import generate_embedding


def search_similar_chunks(
    db: Session,
    query: str,
    limit: int = 3,
):
    query_embedding = generate_embedding(query)

    statement = (
        select(DocumentChunk)
        .order_by(
            DocumentChunk.embedding.cosine_distance(query_embedding)
        )
        .limit(limit)
    )

    return db.execute(statement).scalars().all()