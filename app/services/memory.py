import os

from dotenv import load_dotenv
from google import genai
from sqlalchemy import select
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, AIMessage

from app.db.models import Conversation, Message

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)


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

    all_messages = db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.id.asc())
    ).scalars().all()

    recent_messages = all_messages[-limit:]

    result = []

    for message in recent_messages:
        if message.role == "user":
            result.append(
                HumanMessage(content=message.content)
            )

        elif message.role == "assistant":
            result.append(
                AIMessage(content=message.content)
            )

    summary_messages = [
        message
        for message in all_messages
        if conversation.summary_through_id is None
        or message.id > conversation.summary_through_id
    ]

    old_messages = summary_messages[:-limit]

    return {
        "summary": conversation.summary,
        "messages": result,
        "old_messages": old_messages,
    }


def update_conversation_summary(
    conversation_id: int,
    db: Session,
    old_messages: list[Message],
):
    if not old_messages:
        return

    conversation = db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id
        )
    ).scalar_one()

    old_conversation = "\n".join(
        f"{message.role}: {message.content}"
        for message in old_messages
    )

    prompt = f"""
Create a concise summary of this customer support conversation.

Preserve important information such as:
- order numbers
- customer information
- products
- problems
- decisions
- important requests
- relevant context

Existing summary:
{conversation.summary or "None"}

Older conversation:
{old_conversation}

Return only the updated summary.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    conversation.summary = response.text.strip()
    conversation.summary_through_id = old_messages[-1].id

    db.commit()