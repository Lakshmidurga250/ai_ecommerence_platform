"""
Prompt Management & Grounding Templates for AI Shopping Agent.
Defines system instructions, few-shot requirement extraction templates,
tool definitions, and structured response formatters.
"""

from typing import Dict, Any, List

SYSTEM_SHOPPING_AGENT_PROMPT = """You are OmniCommerce's Autonomous AI Shopping Concierge.
Your mission is to help customers find, compare, evaluate, and purchase products from our verified catalog.

CORE CAPABILITIES:
1. Conversational Shopping: Chat naturally, ask clarifying questions when requirements are underspecified.
2. Requirement Extraction: Extract category, budget constraints, use case, brand, and feature requirements.
3. Grounded Recommendations: Every product recommended MUST exist in our real database catalog. Never invent prices or specifications.
4. Product Comparison: Provide objective side-by-side comparisons with specs, price differentials, and category winners.
5. Cart & Wishlist Actions: Autonomously assist with adding products to cart or wishlist upon user request.
6. Order & Tracking Assistance: Lookup order status and delivery updates directly from user order records.
7. Explainability: Clearly explain WHY a product was recommended based on user preferences.

STRICT GUARDRAIL POLICIES:
- Never offer discounts or prices not present in the catalog.
- If an exact product or budget match does not exist, recommend verified alternatives and explain the trade-off.
- Keep tone polite, expert, concise, and helpful.
"""

FEW_SHOT_REQUIREMENT_EXTRACTIONS = [
    {
        "input": "I need wireless headphones under ₹5,000 for gaming with good battery life.",
        "output": {
            "intent": "DISCOVER_PRODUCTS",
            "category": "audio-wearables",
            "max_budget": 5000.0,
            "min_budget": None,
            "use_case": "gaming",
            "requirements": ["wireless", "good battery life"],
            "brand": None
        }
    },
    {
        "input": "Compare boAt Rockerz 550 and Sony WH-CH520 headphones",
        "output": {
            "intent": "COMPARE_PRODUCTS",
            "category": "audio-wearables",
            "max_budget": None,
            "min_budget": None,
            "use_case": None,
            "requirements": ["comparison"],
            "brand": None,
            "comparison_candidates": ["boAt Rockerz 550", "Sony WH-CH520"]
        }
    },
    {
        "input": "Add the first gaming mouse to my cart",
        "output": {
            "intent": "CART_ACTION",
            "action": "ADD_TO_CART",
            "category": "gaming-accessories",
            "max_budget": None
        }
    },
    {
        "input": "Where is my order #1042?",
        "output": {
            "intent": "ORDER_LOOKUP",
            "order_id": 1042
        }
    }
]

def format_explanation(product_name: str, extracted_reqs: Dict[str, Any], rating: float, price: float) -> str:
    """Generate human-readable explainability for a recommended product."""
    reasons = []
    use_case = extracted_reqs.get("use_case")
    max_b = extracted_reqs.get("max_budget")
    reqs = extracted_reqs.get("requirements", [])

    if max_b:
        reasons.append(f"fits well within your ₹{int(max_b):,} budget at ₹{int(price):,}")
    if use_case:
        reasons.append(f"optimized for {use_case}")
    if reqs:
        reasons.append(f"delivers on {', '.join(reqs)}")
    if rating >= 4.4:
        reasons.append(f"backed by a high customer rating of {rating}★")

    if reasons:
        return f"Recommended because it {', and '.join(reasons)}."
    return f"Recommended as a top-rated catalog choice matching your search preferences."
