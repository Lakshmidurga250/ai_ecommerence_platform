"""
Autonomous AI Shopping Agent Engine.
Integrates Conversational Shopping, Natural Language Requirement Extraction,
Autonomous Tool Dispatch (Search, Compare, Cart, Wishlist, Orders, Bundles),
Multi-Turn Memory, Grounding Guardrails, Response Evaluation, and Telemetry Analytics.
"""

import time
import re
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc

from app.models.product import Product, Category, Brand
from app.models.order import Order
from app.models.cart import Cart, CartItem
from app.models.review import Review

from ai.shopping_agent.memory import SessionMemoryRegistry, ShoppingAgentMemory
from ai.shopping_agent.guardrails import ShoppingAgentGuardrails
from ai.shopping_agent.prompts import format_explanation, SYSTEM_SHOPPING_AGENT_PROMPT
from ai.shopping_agent.tools import (
    SearchAndFilterTool, ProductComparisonTool, CartActionTool,
    WishlistActionTool, OrderLookupTool, AlternativeAndBundleTool
)
from ai.shopping_agent.evaluator import ResponseEvaluator
from ai.shopping_agent.analytics import ConversationAnalytics


class AIShoppingAgent:
    """
    Intelligent shopping concierge grounded in real database catalog, customer orders, and cart context.
    Orchestrates memory, requirement extraction, tool execution, guardrails, and quality evaluation.
    """

    INTENTS = [
        "DISCOVER_PRODUCTS",
        "COMPARE_PRODUCTS",
        "FILTER_BUDGET",
        "CHECK_SPECIFICATION",
        "CART_ACTION",
        "WISHLIST_ACTION",
        "ORDER_LOOKUP",
        "RETURN_INQUIRY",
        "BUNDLE_SUGGESTION",
        "RECOMMENDATION_REASONING",
        "GENERAL_ASSISTANCE"
    ]

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def handle_shopping_query(
        self,
        query: str,
        user_id: Optional[int] = None,
        context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Entry point for shopping requests."""
        res = self.process_message(self.db, query, user_id=user_id, context=context, session_id=session_id)
        return {
            "reply": res.get("reply_text") or res.get("reply", ""),
            "action_pills": res.get("action_pills") or res.get("suggested_actions", []),
            "grounded_products": res.get("recommended_products") or res.get("grounded_products", []),
            "comparison_table": res.get("comparison_table"),
            "extracted_requirements": res.get("extracted_requirements", {}),
            "evaluation": res.get("evaluation", {}),
            **res
        }

    def _match_category(self, text: str):
        if not self.db:
            return None
        cat, _ = self.__class__._extract_entities(self.db, text)
        return cat

    def _match_brand(self, text: str):
        if not self.db:
            return None
        _, brand = self.__class__._extract_entities(self.db, text)
        return brand

    @classmethod
    def process_message(
        cls,
        db: Session,
        message: str,
        user_id: Optional[int] = None,
        context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main autonomous processing pipeline:
        1. Guardrail Validation
        2. Session Memory Retrieval
        3. Intent Classification & Requirement Extraction
        4. Tool Dispatch (Search, Compare, Cart, Wishlist, Order, Bundle)
        5. Ranking & Grounded Explanation
        6. Response Evaluation & Analytics Logging
        """
        start_time = time.time()
        context = context or {}
        cleaned_msg = message.strip()

        # Handle empty query gracefully
        if not cleaned_msg:
            return {
                "intent": "GENERAL_ASSISTANCE",
                "reply_text": "Hello! I am your AI Shopping Concierge. Tell me what you're looking for, e.g., 'wireless headphones under ₹5,000 for gaming' or 'compare top running shoes'.",
                "recommended_products": [],
                "suggested_actions": [
                    {"label": "Find Gaming Headphones", "action": "search", "payload": {"q": "gaming headphones"}},
                    {"label": "Running Shoes under ₹3,000", "action": "search", "payload": {"q": "running shoes under 3000"}},
                    {"label": "Check My Orders", "action": "order_lookup", "payload": {}}
                ],
                "action_pills": [
                    {"label": "Top Headphones", "action": "search", "payload": {"q": "headphones"}},
                    {"label": "Best Laptops", "action": "search", "payload": {"q": "laptops"}}
                ],
                "extracted_requirements": {}
            }

        # 1. Guardrail input validation
        is_safe, reject_reason = ShoppingAgentGuardrails.validate_user_input(cleaned_msg)
        if not is_safe:
            return {
                "intent": "GUARDRAIL_TRIGGERED",
                "reply_text": reject_reason,
                "recommended_products": [],
                "suggested_actions": [],
                "action_pills": [],
                "extracted_requirements": {},
                "evaluation": {"safety_passed": False, "verdict": "BLOCKED"}
            }

        # 2. Memory Session
        memory = SessionMemoryRegistry.get_or_create(session_id=session_id, user_id=user_id)

        # 3. Intent & Requirement Extraction
        intent = cls._classify_intent(cleaned_msg.lower())
        extracted_reqs = cls.extract_requirements(db, cleaned_msg)

        # Record user turn in memory
        memory.add_user_message(cleaned_msg, intent=intent, extracted_reqs=extracted_reqs)

        tools_invoked = []
        result_payload = {}

        # 4. Tool Dispatch based on detected intent
        if intent == "CART_ACTION":
            tools_invoked.append("CartActionTool")
            result_payload = cls._handle_cart_action(db, cleaned_msg, user_id, extracted_reqs, memory)

        elif intent == "WISHLIST_ACTION":
            tools_invoked.append("WishlistActionTool")
            result_payload = cls._handle_wishlist_action(db, cleaned_msg, user_id, extracted_reqs, memory)

        elif intent == "COMPARE_PRODUCTS":
            tools_invoked.append("ProductComparisonTool")
            result_payload = cls._handle_comparison_intent(db, cleaned_msg, extracted_reqs, memory)

        elif intent == "ORDER_LOOKUP":
            tools_invoked.append("OrderLookupTool")
            result_payload = cls._handle_order_lookup(db, cleaned_msg, user_id)

        elif intent == "BUNDLE_SUGGESTION":
            tools_invoked.append("AlternativeAndBundleTool")
            result_payload = cls._handle_bundle_intent(db, cleaned_msg, extracted_reqs)

        elif intent in ["DISCOVER_PRODUCTS", "FILTER_BUDGET", "CHECK_SPECIFICATION"]:
            tools_invoked.append("SearchAndFilterTool")
            result_payload = cls._handle_discovery_intent(db, cleaned_msg, extracted_reqs, memory, context)

        else:
            tools_invoked.append("SearchAndFilterTool")
            result_payload = cls._handle_general_intent(db, cleaned_msg, extracted_reqs, memory)

        # 5. Extract products and formulate actions
        recommended_products = result_payload.get("recommended_products", [])
        reply_text = result_payload.get("reply_text", "")
        comparison_table = result_payload.get("comparison_table")
        suggested_actions = result_payload.get("suggested_actions", [])
        action_pills = result_payload.get("action_pills", suggested_actions)

        # 6. Evaluation & Telemetry
        latency_ms = (time.time() - start_time) * 1000.0
        evaluation = ResponseEvaluator.evaluate(
            db=db,
            user_query=cleaned_msg,
            extracted_requirements=extracted_reqs,
            recommended_products=recommended_products,
            response_text=reply_text,
            latency_ms=latency_ms
        )

        ConversationAnalytics.record_turn(
            intent=intent,
            tools_invoked=tools_invoked,
            latency_ms=latency_ms,
            evaluation=evaluation
        )

        # Record assistant turn in memory
        p_ids = [p["id"] for p in recommended_products if "id" in p]
        memory.add_assistant_message(
            reply=reply_text,
            intent=intent,
            tools_invoked=tools_invoked,
            grounded_product_ids=p_ids
        )

        return {
            "session_id": memory.session_id,
            "intent": intent,
            "reply_text": reply_text,
            "recommended_products": recommended_products,
            "grounded_products": recommended_products,
            "comparison_table": comparison_table,
            "suggested_actions": suggested_actions,
            "action_pills": action_pills,
            "extracted_requirements": extracted_reqs,
            "tools_invoked": tools_invoked,
            "evaluation": evaluation,
            **result_payload
        }

    @classmethod
    def _classify_intent(cls, text: str) -> str:
        """Classify customer message into actionable intent."""
        # Cart actions
        if any(w in text for w in ["add to cart", "buy this", "add to my cart", "cart items", "my basket", "put in cart"]):
            return "CART_ACTION"
        # Wishlist actions
        if any(w in text for w in ["add to wishlist", "save for later", "save to wishlist", "wishlist"]):
            return "WISHLIST_ACTION"
        # Product comparison
        if any(w in text for w in ["compare", "versus", "vs", "which one is better", "difference between"]):
            return "COMPARE_PRODUCTS"
        # Orders / tracking
        if any(w in text for w in ["order status", "track my order", "where is my order", "tracking", "delivery status", "order #", "order id", "where is my package"]):
            return "ORDER_LOOKUP"
        # Bundle suggestions
        if any(w in text for w in ["bundle", "combo", "package deal", "complete kit"]):
            return "BUNDLE_SUGGESTION"
        # Budget filtering
        if any(w in text for w in ["under", "below", "less than", "budget", "cheap", "affordable", "maximum price", "upto", "up to", "between"]) and any(c.isdigit() for c in text):
            return "FILTER_BUDGET"
        # Specifications
        if any(w in text for w in ["battery", "ram", "processor", "warranty", "spec", "storage", "camera", "display", "size"]):
            return "CHECK_SPECIFICATION"
        # Discovery / recommendation
        if any(w in text for w in ["find", "show me", "looking for", "recommend", "suggest", "search", "best", "laptop", "shoes", "phone", "headphones", "earbuds", "watch"]):
            return "DISCOVER_PRODUCTS"

        return "GENERAL_ASSISTANCE"

    @classmethod
    def extract_requirements(cls, db: Session, text: str) -> Dict[str, Any]:
        """
        Extracts structured constraints:
        - Category
        - Budget range (min_budget, max_budget)
        - Use case (e.g. 'gaming', 'running', 'casual')
        - Key requirements (e.g. 'wireless', 'good battery life', 'noise cancelling')
        - Brand
        """
        lower = text.lower()
        cat_obj, brand_obj = cls._extract_entities(db, text)
        min_b, max_b = cls._extract_budget_range(lower)

        # Extract use cases
        use_cases = ["gaming", "running", "casual", "office", "marathon", "fitness", "travel", "programming", "workout"]
        detected_use_case = None
        for uc in use_cases:
            if uc in lower:
                detected_use_case = uc
                break

        # Extract specific requirements
        known_reqs = [
            ("wireless", "wireless"),
            ("bluetooth", "wireless"),
            ("battery", "good battery life"),
            ("noise cancell", "noise cancellation"),
            ("waterproof", "water resistant"),
            ("lightweight", "lightweight design"),
            ("fast charg", "fast charging"),
            ("rgb", "RGB illumination"),
            ("leather", "leather finish")
        ]
        detected_reqs = []
        for term, label in known_reqs:
            if term in lower and label not in detected_reqs:
                detected_reqs.append(label)

        return {
            "category": cat_obj.slug if cat_obj else None,
            "category_name": cat_obj.name if cat_obj else None,
            "category_id": cat_obj.id if cat_obj else None,
            "brand": brand_obj.name if brand_obj else None,
            "brand_id": brand_obj.id if brand_obj else None,
            "min_budget": min_b,
            "max_budget": max_b,
            "use_case": detected_use_case,
            "requirements": detected_reqs,
            "raw_query": text
        }


    @classmethod
    def _extract_budget_range(cls, text: str) -> Tuple[Optional[float], Optional[float]]:
        """Extracts minimum and maximum budget from text."""
        min_budget, max_budget = None, None
        lower = text.lower()

        # Pattern: between X and Y
        between_match = re.search(r"between\s+(?:₹|rs\.?|inr)?\s*([0-9,k]+)\s+and\s+(?:₹|rs\.?|inr)?\s*([0-9,k]+)", lower)
        if between_match:
            min_budget = cls._parse_currency_token(between_match.group(1))
            max_budget = cls._parse_currency_token(between_match.group(2))
            return min_budget, max_budget

        # Pattern: under / below / less than / max / upto X
        under_match = re.search(r"(?:under|below|less than|within|upto|up to|max|maximum)\s+(?:₹|rs\.?|inr)?\s*([0-9,k]+)", lower)
        if under_match:
            max_budget = cls._parse_currency_token(under_match.group(1))
            return None, max_budget

        # Pattern: above / more than X
        above_match = re.search(r"(?:above|more than|over)\s+(?:₹|rs\.?|inr)?\s*([0-9,k]+)", lower)
        if above_match:
            min_budget = cls._parse_currency_token(above_match.group(1))
            return min_budget, None

        return None, None

    @classmethod
    def _extract_budget(cls, text: str) -> Optional[float]:
        """Returns single budget ceiling or floor for backward compatibility."""
        min_b, max_b = cls._extract_budget_range(text)
        if max_b is not None:
            return max_b
        if min_b is not None:
            return min_b

        # Fallback single number search
        match = re.search(r"(?:₹|rs\.?|inr)\s*([0-9,k]+)", text.lower())
        if match:
            return cls._parse_currency_token(match.group(1))

        # Check for number preceded by budget terms
        num_match = re.search(r"(?:budget|price)\s*(?:is|of)?\s*([0-9,k]+)", text.lower())
        if num_match:
            return cls._parse_currency_token(num_match.group(1))

        return None

    @classmethod
    def _parse_currency_token(cls, token: str) -> Optional[float]:
        token = token.replace(",", "").strip()
        if token.endswith("k"):
            try:
                return float(token[:-1]) * 1000.0
            except ValueError:
                return None
        try:
            return float(token)
        except ValueError:
            return None

    @classmethod
    def _extract_entities(cls, db: Session, text: str) -> Tuple[Optional[Category], Optional[Brand]]:
        """Match categories and brands against database."""
        lower_text = text.lower()
        all_categories = db.query(Category).all()
        matched_category = None

        category_synonyms = {
            "audio-wearables": ["audio", "wearables", "headphones", "earbuds", "earphones", "headset", "speakers", "soundbar", "watch", "smartwatch"],
            "footwear-running": ["footwear", "running", "shoes", "sneakers", "boots", "sandals", "slippers"],
            "laptops-computing": ["laptops", "laptop", "computing", "computer", "pc", "macbook", "notebook"],
            "smartphones-tablets": ["smartphones", "smartphone", "tablets", "tablet", "phone", "iphone", "android", "ipad", "mobile"],
            "athletic-apparel": ["apparel", "clothing", "tshirt", "t-shirt", "shirt", "jersey", "hoodie", "shorts", "pants"],
            "gaming-accessories": ["gaming", "game", "controller", "playstation", "xbox", "mouse", "keyboard"],
            "home-kitchen": ["home", "kitchen", "cookware", "appliance", "air fryer", "blender", "coffee"],
            "personal-care": ["personal care", "grooming", "trimmer", "skincare", "perfume", "shampoo"],
            "books-stationery": ["books", "stationery", "notebook", "pen"]
        }

        best_match = None
        longest_token_len = 0

        for cat in all_categories:
            words = [w for w in cat.name.lower().split() if len(w) > 3 and w not in ["with", "from"]]
            syns = category_synonyms.get(cat.slug, [])
            tokens = [cat.slug] + words + syns
            for tok in tokens:
                pattern = r"\b" + re.escape(tok) + r"\b"
                if re.search(pattern, lower_text):
                    if len(tok) > longest_token_len:
                        longest_token_len = len(tok)
                        best_match = cat

        matched_category = best_match

        all_brands = db.query(Brand).all()
        matched_brand = None
        longest_brand_len = 0
        for br in all_brands:
            for b_token in [br.name.lower(), br.slug.lower()]:
                pattern = r"\b" + re.escape(b_token) + r"\b"
                if re.search(pattern, lower_text):
                    if len(b_token) > longest_brand_len:
                        longest_brand_len = len(b_token)
                        matched_brand = br

        return matched_category, matched_brand


    # -------------------------------------------------------------
    # Tool Handlers
    # -------------------------------------------------------------
    @classmethod
    def _handle_discovery_intent(
        cls,
        db: Session,
        message: str,
        reqs: Dict[str, Any],
        memory: ShoppingAgentMemory,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handles natural language product search with requirement extraction and ranking."""
        cat_id = reqs.get("category_id")
        category_obj = db.query(Category).filter(Category.id == cat_id).first() if cat_id else None
        brand_id = reqs.get("brand_id")
        brand_obj = db.query(Brand).filter(Brand.id == brand_id).first() if brand_id else None
        max_b = reqs.get("max_budget") or memory.cumulative_preferences.get("max_budget")
        min_b = reqs.get("min_budget") or memory.cumulative_preferences.get("min_budget")
        use_case = reqs.get("use_case")


        # Keywords for search
        keywords = [w for w in message.split() if len(w) >= 3]
        if use_case and use_case not in keywords:
            keywords.append(use_case)

        products = SearchAndFilterTool.execute(
            db=db,
            category=category_obj,
            brand=brand_obj,
            min_price=min_b,
            max_price=max_b,
            keywords=keywords,
            limit=4
        )

        cat_title = category_obj.name if category_obj else "catalog products"
        budget_str = f" under ₹{int(max_b):,}" if max_b else ""
        use_case_str = f" for {use_case}" if use_case else ""
        brand_str = f" from {brand_obj.name}" if brand_obj else ""

        if products:
            reply = f"I found {len(products)} top-rated {cat_title}{brand_str}{budget_str}{use_case_str} grounded in our catalog:"
        else:
            reply = f"I couldn't find exact matches{budget_str}, but here are our top-rated marketplace options:"

        rec_cards = []
        actions = []
        for p in products:
            explanation = format_explanation(p.name, reqs, p.rating, p.price)
            img = p.images[0].image_url if p.images else None
            rec_cards.append({
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "compare_at_price": p.compare_at_price,
                "rating": p.rating,
                "slug": p.slug,
                "stock": p.stock,
                "image_url": img,
                "explanation": explanation
            })
            actions.append({
                "label": f"View {p.name[:22]}... (₹{int(p.price):,})",
                "action": "view_product",
                "payload": {"slug": p.slug}
            })

        if len(rec_cards) >= 2:
            actions.append({
                "label": f"Compare Top 2 {cat_title}",
                "action": "compare",
                "payload": {"product_ids": [rec_cards[0]["id"], rec_cards[1]["id"]]}
            })

        return {
            "reply_text": reply,
            "recommended_products": rec_cards,
            "suggested_actions": actions,
            "action_pills": actions
        }

    @classmethod
    def _handle_comparison_intent(
        cls,
        db: Session,
        message: str,
        reqs: Dict[str, Any],
        memory: ShoppingAgentMemory
    ) -> Dict[str, Any]:
        """Compares 2 or more products mentioned in text or from memory."""
        all_products = db.query(Product).filter(Product.is_active == True).all()
        candidates = []

        for p in all_products:
            p_short = p.name.lower()
            if any(term in message.lower() for term in [p_short[:15], p.slug, p.name.split()[0].lower() if len(p.name.split()) > 0 else ""]):
                if p not in candidates:
                    candidates.append(p)
                if len(candidates) >= 3:
                    break

        if len(candidates) < 2:
            # Fall back to recently viewed product IDs from session memory
            if memory.last_viewed_product_ids:
                for pid in memory.last_viewed_product_ids[:2]:
                    db_p = db.query(Product).filter(Product.id == pid).first()
                    if db_p and db_p not in candidates:
                        candidates.append(db_p)

        if len(candidates) < 2:
            # Pick top 2 in category or overall
            cat_id = reqs.get("category_id")
            q = db.query(Product).filter(Product.is_active == True)
            if cat_id:
                q = q.filter(Product.category_id == cat_id)
            candidates = q.order_by(desc(Product.rating)).limit(2).all()

        comparison = ProductComparisonTool.execute(db, candidates)
        winner_name = comparison.get("winner", {}).get("name", "Option 1")
        reply = f"Here is a side-by-side specification and value comparison for {len(candidates)} products. {comparison.get('winner', {}).get('verdict', '')}"

        rec_cards = []
        for p in candidates:
            img = p.images[0].image_url if p.images else None
            rec_cards.append({
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "compare_at_price": p.compare_at_price,
                "rating": p.rating,
                "slug": p.slug,
                "stock": p.stock,
                "image_url": img
            })

        actions = [
            {"label": f"Choose {winner_name[:20]}", "action": "add_to_cart", "payload": {"product_id": comparison.get("winner", {}).get("product_id")}},
            {"label": "Explore More Alternatives", "action": "search", "payload": {"q": reqs.get("category") or "electronics"}}
        ]

        return {
            "reply_text": reply,
            "comparison_table": comparison,
            "recommended_products": rec_cards,
            "suggested_actions": actions,
            "action_pills": actions
        }

    @classmethod
    def _handle_cart_action(
        cls,
        db: Session,
        message: str,
        user_id: Optional[int],
        reqs: Dict[str, Any],
        memory: ShoppingAgentMemory
    ) -> Dict[str, Any]:
        """Handles natural language cart actions like 'add first product to cart'."""
        lower = message.lower()
        # Check target product
        product_id = None
        all_prods = db.query(Product).filter(Product.is_active == True).all()

        for p in all_prods:
            if p.name.lower() in lower or p.slug.lower() in lower:
                product_id = p.id
                break

        if not product_id and memory.last_viewed_product_ids:
            # Add most recently viewed product
            product_id = memory.last_viewed_product_ids[-1]

        if not product_id:
            # Pick top product in category or top rated
            cat_id = reqs.get("category_id")
            q = db.query(Product).filter(Product.is_active == True)
            if cat_id:
                q = q.filter(Product.category_id == cat_id)
            top_p = q.order_by(desc(Product.rating)).first()
            if top_p:
                product_id = top_p.id

        cart_res = CartActionTool.execute(
            db=db,
            action="ADD" if any(w in lower for w in ["add", "buy", "put"]) else "VIEW",
            user_id=user_id,
            product_id=product_id
        )

        reply = cart_res.get("message", "Updated your shopping cart.")
        actions = [
            {"label": "View Shopping Cart", "action": "navigate", "payload": {"path": "/cart"}},
            {"label": "Proceed to Checkout", "action": "navigate", "payload": {"path": "/checkout"}}
        ]

        return {
            "reply_text": reply,
            "cart_result": cart_res,
            "recommended_products": [],
            "suggested_actions": actions,
            "action_pills": actions
        }

    @classmethod
    def _handle_wishlist_action(
        cls,
        db: Session,
        message: str,
        user_id: Optional[int],
        reqs: Dict[str, Any],
        memory: ShoppingAgentMemory
    ) -> Dict[str, Any]:
        """Handles saving items to wishlist."""
        product_id = memory.last_viewed_product_ids[-1] if memory.last_viewed_product_ids else None
        if not product_id:
            top_p = db.query(Product).filter(Product.is_active == True).first()
            product_id = top_p.id if top_p else None

        wishlist_res = WishlistActionTool.execute(
            db=db,
            action="ADD",
            user_id=user_id,
            product_id=product_id
        )

        reply = wishlist_res.get("message", "Saved item to your wishlist.")
        actions = [
            {"label": "View My Wishlist", "action": "navigate", "payload": {"path": "/wishlist"}}
        ]
        return {
            "reply_text": reply,
            "wishlist_result": wishlist_res,
            "recommended_products": [],
            "suggested_actions": actions,
            "action_pills": actions
        }

    @classmethod
    def _handle_order_lookup(
        cls,
        db: Session,
        message: str,
        user_id: Optional[int]
    ) -> Dict[str, Any]:
        """Grounded order status lookup."""
        order_res = OrderLookupTool.execute(db=db, user_id=user_id)
        reply = order_res.get("reply_summary") or order_res.get("message", "Order details retrieved.")

        actions = [
            {"label": "View All Orders", "action": "navigate", "payload": {"path": "/orders"}},
            {"label": "Track Delivery", "action": "navigate", "payload": {"path": "/account"}}
        ]
        return {
            "reply_text": reply,
            "order_result": order_res,
            "recommended_products": [],
            "suggested_actions": actions,
            "action_pills": actions
        }

    @classmethod
    def _handle_bundle_intent(
        cls,
        db: Session,
        message: str,
        reqs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Curates bundle suggestions."""
        cat_id = reqs.get("category_id")
        q = db.query(Product).filter(Product.is_active == True)
        if cat_id:
            q = q.filter(Product.category_id == cat_id)
        primary = q.order_by(desc(Product.sales_count)).first()
        if not primary:
            primary = db.query(Product).filter(Product.is_active == True).first()

        bundle = AlternativeAndBundleTool.get_bundle_suggestion(db, primary)
        reply = f"Here is our recommended '{bundle.get('bundle_title', 'Curated Bundle')}' saving you ₹{bundle.get('savings', 0):,} (12% off):"

        return {
            "reply_text": reply,
            "bundle": bundle,
            "recommended_products": [],
            "suggested_actions": [
                {"label": "Add Complete Bundle to Cart", "action": "add_bundle", "payload": {"bundle": bundle}}
            ],
            "action_pills": [
                {"label": "Add Bundle", "action": "add_bundle", "payload": {}}
            ]
        }

    @classmethod
    def _handle_general_intent(
        cls,
        db: Session,
        message: str,
        reqs: Dict[str, Any],
        memory: ShoppingAgentMemory
    ) -> Dict[str, Any]:
        """Handles general greetings and open-ended shopping queries."""
        top_prods = db.query(Product).filter(Product.is_active == True).order_by(desc(Product.rating)).limit(3).all()
        rec_cards = []
        for p in top_prods:
            rec_cards.append({
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "compare_at_price": p.compare_at_price,
                "rating": p.rating,
                "slug": p.slug,
                "stock": p.stock,
                "image_url": p.images[0].image_url if p.images else None
            })

        reply = "I am your AI Shopping Concierge. You can ask me to find products within a specific budget, compare features, check your orders, or add items directly to your cart. How can I help you today?"
        actions = [
            {"label": "Headphones under ₹5,000 for gaming", "action": "search", "payload": {"q": "headphones under 5000 for gaming"}},
            {"label": "Best Laptops under ₹75,000", "action": "search", "payload": {"q": "laptops under 75000"}},
            {"label": "Track My Orders", "action": "order_lookup", "payload": {}}
        ]

        return {
            "reply_text": reply,
            "recommended_products": rec_cards,
            "suggested_actions": actions,
            "action_pills": actions
        }
