from langchain_core.tools import tool
from sqlalchemy import select

from app.db.database import SessionLocal
from app.db.models import Order, User
from app.services.retrieval import search_similar_chunks


@tool
def get_order(order_id: int):
    """Get the current status and details of a customer order by order ID."""

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

    except Exception as e:
        return {"error": f"Failed to retrieve order: {str(e)}"}

    finally:
        db.close()


@tool
def get_customer(user_id: int):
    """Get a customer's name and email address by user ID."""

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

    except Exception as e:
        return {"error": f"Failed to retrieve customer: {str(e)}"}

    finally:
        db.close()


@tool
def get_refund_policy():
    """Get the company's official refund policy and eligibility period."""

    return {
        "policy": (
            "Customers can request a refund within 30 days "
            "of receiving their order."
        )
    }

@tool
def search_knowledge(question: str):
    """Search the company's knowledge base for policies, procedures, shipping, refunds, and other support information."""

    db = SessionLocal()

    try:
        chunks = search_similar_chunks(
            db=db,
            query=question,
            limit=3,
        )

        if not chunks:
            return {"error": "No relevant information found."}

        return {
            "results": [
                {
                    "source": chunk.source,
                    "content": chunk.content,
                }
                for chunk in chunks
            ]
        }

    except Exception as e:
        return {"error": f"Knowledge search failed: {str(e)}"}

    finally:
        db.close()