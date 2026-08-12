from sqlalchemy import select
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, AIMessage

from app.db.models import Conversation, Message


def load_conversation_memory(
    conversation_id: int,
    db: Session,
    limit: int = 10,
):
    conversation = db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id
        )
    ).scalar_one()

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
            result.append(
                HumanMessage(content=message.content)
            )

        elif message.role == "assistant":
            result.append(
                AIMessage(content=message.content)
            )

    return {
        "summary": conversation.summary,
        "messages": result,
    }