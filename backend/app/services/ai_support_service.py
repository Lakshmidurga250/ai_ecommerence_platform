"""
Context-Grounded AI Support Assistant Service.
Authentic conversational agent that grounds inquiries against real user order history,
return policy eligibility, product catalogs, and shipping timelines.
"""

from typing import Dict, Any, List, Optional
import re
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.services.order_orchestration_service import OrderOrchestrationService
from app.services.search_service import SearchService


class AISupportService:
    @staticmethod
    def process_customer_query(
        db: Session,
        message: str,
        user_id: Optional[int] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Interprets customer query, performs intent classification and sentiment scoring,
        retrieves database ground truth, and generates an authentic structured response.
        """
        normalized = message.lower().strip()

        # Sentiment Analysis
        sentiment = AISupportService._detect_sentiment(normalized)

        # Intent Classification
        intent = AISupportService._classify_intent(normalized)

        # Grounded response generation
        if intent == "ORDER_STATUS":
            response = AISupportService._handle_order_status(db, user_id, normalized)
        elif intent == "RETURN_REFUND":
            response = AISupportService._handle_return_refund(db, user_id, normalized)
        elif intent == "PRODUCT_INQUIRY":
            response = AISupportService._handle_product_inquiry(db, normalized)
        elif intent == "SHIPPING_POLICY":
            response = AISupportService._handle_shipping_policy()
        elif intent == "PAYMENT_INQUIRY":
            response = AISupportService._handle_payment_inquiry()
        else:
            response = AISupportService._handle_general_inquiry(user_id)

        # Append sentiment and escalation flag
        response["sentiment"] = sentiment
        response["escalate_to_human"] = sentiment == "FRUSTRATED" or "agent" in normalized or "human" in normalized

        if response["escalate_to_human"]:
            response["suggested_actions"].insert(0, {
                "label": "Escalate to Human Agent",
                "action": "CREATE_SUPPORT_TICKET",
                "payload": {"priority": "HIGH"}
            })

        return response

    @staticmethod
    def _detect_sentiment(text: str) -> str:
        frustrated_words = ["angry", "upset", "terrible", "worst", "broken", "scam", "cheat", "ridiculous", "refund now", "cancel everything", "horrible"]
        positive_words = ["great", "awesome", "thank", "thanks", "perfect", "love", "good", "fast"]

        if any(w in text for w in frustrated_words):
            return "FRUSTRATED"
        if any(w in text for w in positive_words):
            return "POSITIVE"
        return "NEUTRAL"

    @staticmethod
    def _classify_intent(text: str) -> str:
        if any(w in text for w in ["shipping fee", "delivery time", "how long", "standard delivery", "shipping policy", "free shipping", "international shipping"]):
            return "SHIPPING_POLICY"
        if any(w in text for w in ["return", "refund", "replace", "exchange", "damaged", "wrong item", "money back"]):
            return "RETURN_REFUND"
        if any(w in text for w in ["where is", "order status", "track", "my order", "my package", "has arrived", "delivery status"]):
            return "ORDER_STATUS"
        if any(w in text for w in ["recommend", "looking for", "buy", "product", "laptop", "shoe", "phone", "headphones", "search", "price of"]):
            return "PRODUCT_INQUIRY"
        if any(w in text for w in ["payment", "card", "stripe", "credit", "invoice", "charge"]):
            return "PAYMENT_INQUIRY"
        return "GENERAL"


    @staticmethod
    def _handle_order_status(db: Session, user_id: Optional[int], text: str) -> Dict[str, Any]:
        if not user_id:
            return {
                "reply": "I would love to check your order status! Please sign in to your account so I can look up your orders securely.",
                "intent": "ORDER_STATUS",
                "grounded_data": None,
                "suggested_actions": [{"label": "Sign In", "action": "NAVIGATE", "payload": {"path": "/login"}}]
            }

        orders = (
            db.query(Order)
            .filter(Order.customer_id == user_id)
            .order_by(Order.created_at.desc())
            .limit(3)
            .all()
        )

        if not orders:
            return {
                "reply": "I checked your account records, and you don't have any active or past orders yet. Would you like to explore our trending products?",
                "intent": "ORDER_STATUS",
                "grounded_data": {"order_count": 0},
                "suggested_actions": [{"label": "Browse Catalog", "action": "NAVIGATE", "payload": {"path": "/products"}}]
            }

        latest_order = orders[0]
        items_summary = ", ".join(f"{it.product_name} (x{it.quantity})" for it in latest_order.items[:2])
        if len(latest_order.items) > 2:
            items_summary += f" and {len(latest_order.items) - 2} more item(s)"

        reply = (
            f"Your most recent order **#{latest_order.order_number}** containing {items_summary} "
            f"is currently **{latest_order.status}** with a total of ${latest_order.total_amount:.2f}."
        )

        grounded_data = {
            "order_number": latest_order.order_number,
            "status": latest_order.status,
            "total_amount": latest_order.total_amount,
            "items": [{"name": i.product_name, "quantity": i.quantity, "status": i.status} for i in latest_order.items]
        }

        actions = [
            {"label": f"View Order #{latest_order.order_number}", "action": "NAVIGATE", "payload": {"path": f"/orders/{latest_order.id}"}},
            {"label": "View All Orders", "action": "NAVIGATE", "payload": {"path": "/orders"}}
        ]

        return {
            "reply": reply,
            "intent": "ORDER_STATUS",
            "grounded_data": grounded_data,
            "suggested_actions": actions
        }

    @staticmethod
    def _handle_return_refund(db: Session, user_id: Optional[int], text: str) -> Dict[str, Any]:
        if not user_id:
            return {
                "reply": "Our standard policy offers hassle-free returns within 30 days of delivery. Please sign in to verify eligibility on your specific orders.",
                "intent": "RETURN_REFUND",
                "grounded_data": None,
                "suggested_actions": [{"label": "Sign In", "action": "NAVIGATE", "payload": {"path": "/login"}}]
            }

        # Check recent delivered orders
        recent_delivered = (
            db.query(Order)
            .filter(Order.customer_id == user_id, Order.status.in_([OrderStatus.DELIVERED.value, OrderStatus.SHIPPED.value]))
            .order_by(Order.created_at.desc())
            .first()
        )

        if not recent_delivered:
            return {
                "reply": "We accept returns on delivered items within 30 days of receipt. You currently don't have any delivered orders eligible for return.",
                "intent": "RETURN_REFUND",
                "grounded_data": None,
                "suggested_actions": [{"label": "View Orders", "action": "NAVIGATE", "payload": {"path": "/orders"}}]
            }

        # Check first item eligibility
        first_item = recent_delivered.items[0] if recent_delivered.items else None
        if first_item:
            eligibility = OrderOrchestrationService.check_return_eligibility(
                db, user_id, recent_delivered.id, first_item.id
            )
            if eligibility["eligible"]:
                reply = (
                    f"Your order **#{recent_delivered.order_number}** ({first_item.product_name}) is eligible for return! "
                    f"You can return up to {eligibility['max_quantity']} unit(s) for a refund of ${eligibility['unit_refund'] * eligibility['max_quantity']:.2f}."
                )
            else:
                reply = f"For order **#{recent_delivered.order_number}**: {eligibility['reason']}"
        else:
            reply = "You can initiate return requests directly from your order history within 30 days of delivery."

        return {
            "reply": reply,
            "intent": "RETURN_REFUND",
            "grounded_data": {"order_id": recent_delivered.id, "order_number": recent_delivered.order_number},
            "suggested_actions": [
                {"label": f"Manage Order #{recent_delivered.order_number}", "action": "NAVIGATE", "payload": {"path": f"/orders/{recent_delivered.id}"}}
            ]
        }

    @staticmethod
    def _handle_product_inquiry(db: Session, text: str) -> Dict[str, Any]:
        # Extract keywords
        clean = re.sub(r"[^\w\s]", "", text)
        words = [w for w in clean.split() if len(w) > 3 and w not in ("looking", "recommend", "product", "search", "find")]
        query_str = " ".join(words) if words else "electronics"

        search_res = SearchService.search_products(db, query=query_str, limit=3)
        products = search_res.get("items", [])

        if products:
            p_names = ", ".join(f"**{p.get('name', 'Product')}** (${p.get('price', 0):.2f})" for p in products)
            reply = f"Here are the top matches from our catalog for your search: {p_names}."
            actions = [
                {"label": f"View {p.get('name', 'Product')[:20]}...", "action": "NAVIGATE", "payload": {"path": f"/products/{p.get('id')}"}}
                for p in products[:2]
            ]
        else:
            reply = "I couldn't find exact matches for that query, but our catalog features top deals in Electronics, Fashion, Home & Kitchen, and Books!"
            actions = [{"label": "Explore All Products", "action": "NAVIGATE", "payload": {"path": "/products"}}]

        return {
            "reply": reply,
            "intent": "PRODUCT_INQUIRY",
            "grounded_data": {"matched_products": [{"id": p.get("id"), "name": p.get("name"), "price": p.get("price")} for p in products]},
            "suggested_actions": actions
        }

    @staticmethod
    def _handle_shipping_policy() -> Dict[str, Any]:
        return {
            "reply": (
                "📦 **Platform Shipping Policy**:\n"
                "- **Standard Delivery**: 3 to 5 business days ($5.00 flat or FREE on orders over $50.00).\n"
                "- **Express Delivery**: 1 to 2 business days ($15.00).\n"
                "- **Multi-Vendor Orders**: Items from different vendors ship directly from their respective fulfillment centers with independent tracking numbers."
            ),
            "intent": "SHIPPING_POLICY",
            "grounded_data": {"free_shipping_threshold": 50.0, "standard_shipping_fee": 5.0},
            "suggested_actions": [{"label": "Shop Now", "action": "NAVIGATE", "payload": {"path": "/products"}}]
        }

    @staticmethod
    def _handle_payment_inquiry() -> Dict[str, Any]:
        return {
            "reply": (
                "💳 **Accepted Payment Methods**:\n"
                "- Major Credit & Debit Cards (Visa, MasterCard, American Express)\n"
                "- Simulated Digital Wallet & Direct Bank Transfer\n"
                "All transactions are encrypted with 256-bit SSL and protected by our multi-layered fraud defense shield."
            ),
            "intent": "PAYMENT_INQUIRY",
            "grounded_data": None,
            "suggested_actions": [{"label": "View Cart", "action": "NAVIGATE", "payload": {"path": "/cart"}}]
        }

    @staticmethod
    def _handle_general_inquiry(user_id: Optional[int]) -> Dict[str, Any]:
        return {
            "reply": (
                "Hello! I am your AI E-Commerce Assistant. I can help you with:\n"
                "• Checking your active **order tracking and status**\n"
                "• Verifying **return eligibility** and refund requests\n"
                "• Finding **product recommendations** and catalog deals\n"
                "• Answering platform **shipping & payment policies**\n\n"
                "How can I assist you today?"
            ),
            "intent": "GENERAL",
            "grounded_data": None,
            "suggested_actions": [
                {"label": "Where is my order?", "action": "SEND_MESSAGE", "payload": {"text": "Where is my order?"}},
                {"label": "Return policy", "action": "SEND_MESSAGE", "payload": {"text": "What is the return policy?"}},
                {"label": "Browse deals", "action": "NAVIGATE", "payload": {"path": "/products"}}
            ]
        }
