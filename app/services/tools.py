from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Order, User


def get_order(order_id: int, db: Session):
    statement = select(Order).where(Order.id == order_id)

    order = db.execute(statement).scalar_one_or_none()

    if order is None:
        return None

    return {
        "id": order.id,
        "user_id": order.user_id,
        "status": order.status,
        "product": order.product,
    }


def get_customer(user_id: int, db: Session):
    statement = select(User).where(User.id == user_id)

    user = db.execute(statement).scalar_one_or_none()

    if user is None:
        return None

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }


def get_refund_policy():
    return {
        "policy": (
            "Customers can request a refund within 30 days "
            "of receiving their order."
        )
    }