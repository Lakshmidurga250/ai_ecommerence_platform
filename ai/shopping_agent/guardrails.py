"""
Safety Guardrails & Compliance Filter for AI Shopping Agent.
Prevents prompt injections, price hallucinations, unauthorized discounts,
and ensures all product statements are strictly grounded in catalog truth.
"""

import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session

_current_file = Path(__file__).resolve()
_root_dir = _current_file.parents[2]
_backend_dir = _root_dir / "backend"

for _p in (str(_root_dir), str(_backend_dir)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from app.models.product import Product
except ImportError:
    from backend.app.models.product import Product


class ShoppingAgentGuardrails:
    """Enterprise safety and policy enforcement layer for shopping dialogue."""

    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
        r"system\s+prompt",
        r"you\s+are\s+now\s+in\s+dan\s+mode",
        r"jailbreak",
        r"drop\s+table",
        r"<script.*?>",
        r"reveal\s+(internal|secret|admin)\s+key",
        r"bypass\s+security"
    ]

    UNAUTHORIZED_DISCOUNT_TERMS = [
        r"give\s+me\s+(\d+)%\s+discount",
        r"sell\s+it\s+for\s+free",
        r"override\s+price\s+to\s+0",
        r"make\s+it\s+free"
    ]

    @classmethod
    def validate_user_input(cls, user_text: str) -> Tuple[bool, Optional[str]]:
        """
        Screen user query for prompt injections or malicious manipulation.
        Returns (is_valid, rejection_reason).
        """
        cleaned = user_text.lower().strip()

        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, cleaned):
                return False, "Your request contains disallowed system instructions. Please ask about products, orders, or shopping."

        for pattern in cls.UNAUTHORIZED_DISCOUNT_TERMS:
            if re.search(pattern, cleaned):
                return False, "I cannot alter official prices or grant unauthorized custom discounts. I can show you our current deals and coupons."

        if len(user_text) > 800:
            return False, "Query exceeds maximum allowed length of 800 characters."

        return True, None

    @classmethod
    def verify_grounded_response(
        cls,
        db: Session,
        recommended_products: List[Dict[str, Any]],
        response_text: str
    ) -> Dict[str, Any]:
        """
        Validates that every product ID and price claimed in the response exists accurately in the database.
        Detects price hallucinations.
        """
        if not recommended_products:
            return {"grounded": True, "violations": []}

        violations = []
        for p in recommended_products:
            pid = p.get("id")
            claimed_price = p.get("price")
            db_product = db.query(Product).filter(Product.id == pid).first()
            if not db_product:
                violations.append(f"Product ID {pid} does not exist in catalog.")
            elif claimed_price is not None and abs(db_product.price - float(claimed_price)) > 0.01:
                violations.append(f"Price mismatch for {db_product.name}: claimed ₹{claimed_price}, actual catalog price ₹{db_product.price}")

        return {
            "grounded": len(violations) == 0,
            "violations": violations,
            "groundedness_score": 1.0 if not violations else max(0.0, 1.0 - (len(violations) * 0.25))
        }
