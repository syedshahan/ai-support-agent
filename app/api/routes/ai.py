from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.agent.graph import graph

from app.db.database import get_db
from app.db.models import Conversation, Message
from app.services.memory import (
    load_conversation_memory,
    update_conversation_summary,
)


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

    # 3. Load conversation history
    memory = load_conversation_memory(
        conversation.id,
        db,
    )

    if len(memory["old_messages"]) > 10:
        update_conversation_summary(
            conversation.id,
            db,
            memory["old_messages"],
        )

        memory = load_conversation_memory(
            conversation.id,
            db,
        )

    messages = memory["messages"]
    summary = memory["summary"]

    # 4. Run LangGraph
    result = graph.invoke(
        {
            "messages": messages,
            "conversation_id": conversation.id,
            "summary": summary,
        }
    )

    # 5. Get the final assistant message
    assistant_content = result["messages"][-1].content

    if isinstance(assistant_content, list):
        assistant_response = ""

        for item in assistant_content:
            if isinstance(item, dict) and item.get("type") == "text":
                assistant_response += item.get("text", "")
    else:
        assistant_response = str(assistant_content)

    # 6. Save assistant response
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=assistant_response,
    )

    db.add(assistant_message)
    db.commit()

    # 7. Return the response
    return {
        "response": assistant_response
    }
