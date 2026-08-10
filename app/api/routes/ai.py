from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Conversation, Message
from app.services.llm import generate_response


router = APIRouter(prefix="/ai", tags=["AI"])


class ChatRequest(BaseModel):
    user_id: int
    conversation_id: int
    message: str


@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):

    # 1. Find the conversation
    statement = select(Conversation).where(
        Conversation.id == request.conversation_id,
        Conversation.user_id == request.user_id,
    )

    conversation = db.execute(statement).scalar_one_or_none()

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    # 2. Save the user's message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message,
    )

    db.add(user_message)
    db.commit()

    # 3. Load previous conversation messages
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.id)
    )

    messages = db.execute(statement).scalars().all()

    # 4. Build conversation context for Gemini
    conversation_text = ""

    for message in messages:
        conversation_text += (
            f"{message.role.capitalize()}: {message.content}\n"
        )

    # 5. Send conversation history to Gemini
    response = generate_response(conversation_text)

    # 6. Save the assistant's response
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=response,
    )

    db.add(assistant_message)
    db.commit()

    # 7. Return the response
    return {
        "response": response
    }

