from sqlalchemy import select
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, AIMessage

from app.db.models import Message


def load_conversation_messages(
    conversation_id: int,
    db: Session,
):
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.id)
    )

    messages = db.execute(statement).scalars().all()

    result = []

    for message in messages:
        if message.role == "user":
            result.append(HumanMessage(content=message.content))

        elif message.role == "assistant":
            result.append(AIMessage(content=message.content))

    return result