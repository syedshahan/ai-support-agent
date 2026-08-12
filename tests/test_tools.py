from app.agent.tools import get_refund_policy


def test_get_refund_policy():
    result = get_refund_policy.invoke({})

    assert result["policy"] == (
        "Customers can request a refund within 30 days "
        "of receiving their order."
    )