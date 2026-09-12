"""
Automated Bundle Recommendation Engine.
Synthesizes multi-tier curated packages (Starter, Pro Ecosystem, Master Bundle)
with dynamic bundle discounts and instant cart fulfillment payloads.
"""
from typing import Dict, Any, List, Optional
try:
    from app.models.product import Product
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))
    from app.models.product import Product
from sqlalchemy.orm import Session
from ai.recommendations.outfit_bundle_generator import OutfitBundleGenerator


class BundleRecommender:
    """
    Generates structured multi-tier commercial bundles for catalog items.
    """

    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self.generator = OutfitBundleGenerator(db)

    def generate_tiered_bundles(
        self,
        product_id: int,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Builds Starter, Pro, and Master bundle packages centered around a focal item.
        """
        session = db or self.db
        if not session:
            return {"error": "Database session required"}

        product = session.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {"error": f"Product {product_id} not found"}

        # 1. Starter Bundle (2 items: Anchor + 1 essential accessory, 10% discount)
        starter = self.generator.generate_outfit_for_product(
            product_id=product_id,
            bundle_size=2,
            discount_percentage=10.0,
            db=session
        )
        starter["tier_name"] = "Essential Starter Pair"
        starter["badge"] = "Popular Starter"

        # 2. Pro Ecosystem (3 items: Anchor + 2 complementary items, 15% discount)
        pro = self.generator.generate_outfit_for_product(
            product_id=product_id,
            bundle_size=3,
            discount_percentage=15.0,
            db=session
        )
        pro["tier_name"] = "Pro Ecosystem Suite"
        pro["badge"] = "Best Value"

        # 3. Master Bundle (4 items: Anchor + 3 items, 20% discount)
        master = self.generator.generate_outfit_for_product(
            product_id=product_id,
            bundle_size=4,
            discount_percentage=20.0,
            db=session
        )
        master["tier_name"] = "Ultimate Master Collection"
        master["badge"] = "Maximum Savings"

        return {
            "focal_product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "category": product.category.name if product.category else ""
            },
            "tiered_bundles": [starter, pro, master]
        }
