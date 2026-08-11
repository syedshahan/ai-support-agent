from sqlalchemy import select
from langchain_core.tools import tool

from app.db.database import SessionLocal
from app.db.models import Order


@tool
def get_order(order_id: int):
    """
    Get an order by its order ID.
    """
    db = SessionLocal()

    try:
        statement = select(Order).where(Order.id == order_id)

        order = db.execute(statement).scalar_one_or_none()

        if order is None:
            return {
                "error": f"Order {order_id} not found"
            }

        return {
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "product": order.product,
        }

    finally:
        db.close()