from langchain_core.tools import tool
from sqlalchemy import select

from app.db.database import SessionLocal
from app.db.models import Order, User


@tool
def get_order(order_id: int):
    """Get an order by its order ID."""

    db = SessionLocal()

    try:
        statement = select(Order).where(Order.id == order_id)
        order = db.execute(statement).scalar_one_or_none()

        if order is None:
            return {"error": f"Order {order_id} not found"}

        return {
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "product": order.product,
        }

    finally:
        db.close()


@tool
def get_customer(user_id: int):
    """Get customer information by user ID."""

    db = SessionLocal()

    try:
        statement = select(User).where(User.id == user_id)
        user = db.execute(statement).scalar_one_or_none()

        if user is None:
            return {"error": f"Customer {user_id} not found"}

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }

    finally:
        db.close()


@tool
def get_refund_policy():
    """Get the company's refund policy."""

    return {
        "policy": (
            "Customers can request a refund within 30 days "
            "of receiving their order."
        )
    }

@tool
def search_knowledge(question: str):
    """Search company documents for information relevant to the user's question."""

    db = SessionLocal()

    try:
        from app.services.retrieval import search_similar_chunks

        chunks = search_similar_chunks(
            db=db,
            query=question,
            limit=3,
        )

        if not chunks:
            return {
                "error": "No relevant information found."
            }

        return {
            "results": [
                {
                    "source": chunk.source,
                    "content": chunk.content,
                }
                for chunk in chunks
            ]
        }

    finally:
        db.close()