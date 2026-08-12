from sqlalchemy import select
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, AIMessage

from app.db.models import Message


def load_conversation_messages(
    conversation_id: int,
    db: Session,
    limit: int = 10,
):
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.id.desc())
        .limit(limit)
    )

    messages = db.execute(statement).scalars().all()
    messages.reverse()

    result = []

    for message in messages:
        if message.role == "user":
            result.append(HumanMessage(content=message.content))

        elif message.role == "assistant":
            result.append(AIMessage(content=message.content))

    return result