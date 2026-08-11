from sqlalchemy.orm import Session

from app.services.llm import generate_response
from app.services.retrieval import search_similar_chunks


def generate_rag_response(
    db: Session,
    question: str,
) -> str:

    chunks = search_similar_chunks(
        db=db,
        query=question,
        limit=3,
    )

    context = "\n\n".join(
        chunk.content
        for chunk in chunks
    )

    prompt = f"""
Answer the user's question using the provided context.

Context:
{context}

User question:
{question}

If the answer cannot be found in the context, say you don't know.
"""

    return generate_response(prompt, db)