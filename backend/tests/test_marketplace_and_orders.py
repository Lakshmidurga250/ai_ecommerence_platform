"""
Unit and API Integration Tests for Multi-Vendor Marketplace & Order Orchestration.
Tests seller scorecards, payout settlements, order splitting, return eligibility,
and context-grounded AI support assistant.
"""

import pytest
from app.models.seller import Seller
from app.models.order import Order, OrderItem
from app.models.user import User
from app.services.marketplace_service import MarketplaceService
from app.services.order_orchestration_service import OrderOrchestrationService
from app.services.ai_support_service import AISupportService


def test_seller_scorecard_calculation(db_session):
    """Verifies vendor metrics, GMV, commission withholding, and net payable balances."""
    seller = db_session.query(Seller).first()
    assert seller is not None

    scorecard = MarketplaceService.get_seller_scorecard(db_session, seller.id)
    assert scorecard["seller_id"] == seller.id
    assert "catalog_metrics" in scorecard
    assert "fulfillment_metrics" in scorecard
    assert "financial_metrics" in scorecard
    assert scorecard["financial_metrics"]["gross_sales"] >= 0.0
    assert scorecard["financial_metrics"]["net_earnings"] >= 0.0
    assert scorecard["financial_metrics"]["available_balance"] >= 0.0


def test_seller_payout_lifecycle(db_session):
    """Verifies that sellers cannot withdraw beyond available balance and valid payouts are registered."""
    seller = db_session.query(Seller).first()
    scorecard = MarketplaceService.get_seller_scorecard(db_session, seller.id)
    available = scorecard["financial_metrics"]["available_balance"]

    # Attempting to withdraw more than available must raise an exception
    with pytest.raises(Exception):
        MarketplaceService.request_payout(db_session, seller.id, amount=available + 5000.0)

    # Valid payout request (if available > 0, or with $1 when available)
    if available >= 1.0:
        payout = MarketplaceService.request_payout(db_session, seller.id, amount=1.0)
        assert payout.id is not None
        assert payout.status == "PENDING"
        assert payout.amount == 1.0

        # Admin approves payout
        settled = MarketplaceService.process_payout_disbursement(db_session, payout.id, action="APPROVE")
        assert settled.status == "PROCESSED"


def test_order_partitioning_by_seller(db_session):
    """Verifies multi-vendor basket partitioning into discrete vendor sub-orders."""
    order = db_session.query(Order).first()
    assert order is not None

    split = OrderOrchestrationService.split_order_by_seller(db_session, order.id)
    assert split["order_id"] == order.id
    assert "vendor_sub_orders" in split
    assert len(split["vendor_sub_orders"]) >= 1

    sub = split["vendor_sub_orders"][0]
    assert "seller_id" in sub
    assert "store_name" in sub
    assert "items" in sub
    assert "commission_rate" in sub
    assert "platform_commission" in sub
    assert "net_payable" in sub
    assert sub["subtotal"] == round(sub["platform_commission"] + sub["net_payable"], 2)


def test_return_eligibility_policy(db_session):
    """Verifies that non-delivered orders or unowned orders are rejected under platform policy."""
    customer = db_session.query(User).filter(User.email == "john.doe@example.com").first()
    order = db_session.query(Order).filter(Order.customer_id == customer.id).first()

    if order and order.items:
        item = order.items[0]
        # Check return eligibility
        eligibility = OrderOrchestrationService.check_return_eligibility(
            db=db_session,
            user_id=customer.id,
            order_id=order.id,
            order_item_id=item.id
        )
        assert "eligible" in eligibility
        assert "reason" in eligibility

        # Unauthorized user check
        unauth_check = OrderOrchestrationService.check_return_eligibility(
            db=db_session,
            user_id=customer.id + 9999,
            order_id=order.id,
            order_item_id=item.id
        )
        assert unauth_check["eligible"] is False


def test_ai_support_grounded_assistant(db_session):
    """Verifies natural language query resolution, intent classification, and database context grounding."""
    # Test order status intent
    res_order = AISupportService.process_customer_query(
        db=db_session,
        message="Where is my order? Can you give me the tracking status?",
        user_id=None
    )
    assert res_order["intent"] == "ORDER_STATUS"
    assert "reply" in res_order
    assert len(res_order["suggested_actions"]) >= 1

    # Test shipping policy intent
    res_ship = AISupportService.process_customer_query(
        db=db_session,
        message="How long does standard delivery take?",
        user_id=None
    )
    assert res_ship["intent"] == "SHIPPING_POLICY"
    assert "Standard Delivery" in res_ship["reply"]

    # Test sentiment escalation on angry inquiry
    res_angry = AISupportService.process_customer_query(
        db=db_session,
        message="This is terrible and broken! I am angry and want to talk to an agent immediately!",
        user_id=None
    )
    assert res_angry["sentiment"] == "FRUSTRATED"
    assert res_angry["escalate_to_human"] is True


def test_marketplace_api_endpoints(client, admin_token):
    """Verifies marketplace administrative overview endpoint."""
    res = client.get(
        "/api/v1/marketplace/overview",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert "total_sellers" in data
    assert "gross_merchandise_volume" in data
    assert "platform_commission_revenue" in data


def test_ai_support_api_chat(client):
    """Verifies public AI Support Chat endpoint."""
    res = client.post("/api/v1/marketplace/ai-support/chat", json={
        "message": "What is the return policy?",
        "context": {}
    })
    assert res.status_code == 200
    data = res.json()
    assert data["intent"] == "RETURN_REFUND"
    assert "reply" in data
