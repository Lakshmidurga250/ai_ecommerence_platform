"""
AI Outfit & Bundle Generator Engine.
Generates context-aware, complementary multi-product combinations (outfits, workstation setups, bundles)
based on category compatibility graphs, price proportionality, style matching, and bundle discount economics.
"""
from typing import List, Dict, Any, Optional
import math
from sqlalchemy.orm import Session
try:
    from app.models.product import Product, Category
except ImportError:
    from backend.app.models.product import Product, Category


class OutfitBundleGenerator:
    """
    Intelligent bundle and outfit synthesis engine.
    Uses multi-partite category compatibility graph with price proportionality and savings optimization.
    """

    # Multi-partite compatibility graph: Category Slug -> list of compatible category slugs with affinity weights
    COMPATIBILITY_GRAPH = {
        "footwear-running": [
            {"slug": "athletic-apparel", "weight": 0.95, "role": "Apparel Match"},
            {"slug": "audio-wearables", "weight": 0.85, "role": "Fitness Tech"},
            {"slug": "personal-care-grooming", "weight": 0.60, "role": "Daily Care"},
        ],
        "athletic-apparel": [
            {"slug": "footwear-running", "weight": 0.95, "role": "Footwear"},
            {"slug": "audio-wearables", "weight": 0.85, "role": "Audio Companion"},
            {"slug": "personal-care-grooming", "weight": 0.55, "role": "Recovery Care"},
        ],
        "laptops-computing": [
            {"slug": "gaming-accessories", "weight": 0.90, "role": "Peripherals"},
            {"slug": "audio-wearables", "weight": 0.85, "role": "Audio Headset"},
            {"slug": "books-stationery", "weight": 0.65, "role": "Productivity Journal"},
        ],
        "smartphones-tablets": [
            {"slug": "audio-wearables", "weight": 0.95, "role": "True Wireless Audio"},
            {"slug": "gaming-accessories", "weight": 0.75, "role": "Mobile Accessories"},
            {"slug": "books-stationery", "weight": 0.60, "role": "Desk Stationery"},
        ],
        "audio-wearables": [
            {"slug": "smartphones-tablets", "weight": 0.90, "role": "Source Device"},
            {"slug": "athletic-apparel", "weight": 0.80, "role": "Workout Gear"},
            {"slug": "laptops-computing", "weight": 0.85, "role": "Workstation Audio"},
        ],
        "gaming-accessories": [
            {"slug": "laptops-computing", "weight": 0.95, "role": "Host Machine"},
            {"slug": "audio-wearables", "weight": 0.85, "role": "Immersive Sound"},
        ],
        "home-kitchen": [
            {"slug": "personal-care-grooming", "weight": 0.70, "role": "Lifestyle Care"},
            {"slug": "books-stationery", "weight": 0.65, "role": "Home Office Reading"},
        ],
        "personal-care-grooming": [
            {"slug": "home-kitchen", "weight": 0.70, "role": "Living Essentials"},
            {"slug": "athletic-apparel", "weight": 0.60, "role": "Post-Workout"},
        ],
        "books-stationery": [
            {"slug": "laptops-computing", "weight": 0.75, "role": "Study Workstation"},
            {"slug": "smartphones-tablets", "weight": 0.70, "role": "Digital Planner"},
            {"slug": "home-kitchen", "weight": 0.60, "role": "Reading Nook"},
        ],
    }

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def generate_outfit_for_product(
        self,
        product_id: int,
        bundle_size: int = 3,
        discount_percentage: float = 12.0,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Generates a curated outfit/bundle centered around a focal product.
        """
        session = db or self.db
        if not session:
            return {"error": "Database session required"}

        focal_product = session.query(Product).filter(Product.id == product_id).first()
        if not focal_product:
            return {"error": f"Product {product_id} not found"}

        focal_category = focal_product.category.slug if focal_product.category else "general"
        compat_specs = self.COMPATIBILITY_GRAPH.get(focal_category, [])

        bundle_items = [self._format_product_summary(focal_product, is_focal=True, role="Anchor Item")]
        total_mrp = focal_product.price
        selected_ids = {focal_product.id}

        for spec in compat_specs:
            if len(bundle_items) >= bundle_size:
                break

            target_slug = spec["slug"]
            # Find candidate products in this category with price proportionality
            candidates = session.query(Product).join(Category).filter(
                Category.slug == target_slug,
                Product.is_active == True,
                Product.id.notin_(selected_ids)
            ).all()

            if not candidates:
                continue

            # Score candidates based on price balance: target ratio 0.3 to 1.5 of focal product
            best_candidate = None
            best_score = -1.0

            for c in candidates:
                ratio = c.price / max(1.0, focal_product.price)
                # Ideal price proportionality Gaussian curve centered at 0.65
                price_prop = math.exp(-0.5 * ((ratio - 0.65) / 0.5) ** 2)
                rating_score = (c.rating or 4.0) / 5.0
                composite = 0.5 * spec["weight"] + 0.3 * price_prop + 0.2 * rating_score

                if composite > best_score:
                    best_score = composite
                    best_candidate = c

            if best_candidate:
                selected_ids.add(best_candidate.id)
                bundle_items.append(
                    self._format_product_summary(best_candidate, is_focal=False, role=spec["role"], score=best_score)
                )
                total_mrp += best_candidate.price

        # Calculate bundle pricing
        bundle_discount = discount_percentage / 100.0
        final_price = round(total_mrp * (1.0 - bundle_discount), 2)
        total_savings = round(total_mrp - final_price, 2)

        # Generate human-readable theme title
        theme_title = self._get_bundle_theme_title(focal_product.name, focal_category, len(bundle_items))

        return {
            "bundle_id": f"bundle-{focal_product.id}-{len(bundle_items)}",
            "theme_title": theme_title,
            "focal_product_id": focal_product.id,
            "category": focal_category,
            "items_count": len(bundle_items),
            "items": bundle_items,
            "original_total_price": round(total_mrp, 2),
            "bundle_discount_pct": discount_percentage,
            "bundle_price": final_price,
            "total_savings": total_savings,
            "currency": "INR",
            "one_click_add_payload": {
                "product_ids": [item["id"] for item in bundle_items],
                "discount_code": f"BUNDLE{int(discount_percentage)}"
            }
        }

    def _get_bundle_theme_title(self, name: str, category_slug: str, count: int) -> str:
        if "footwear" in category_slug or "athletic" in category_slug:
            return f"The Performance Fit: {name[:24]} & Coordinated Gear ({count} Pieces)"
        elif "laptops" in category_slug or "smartphones" in category_slug:
            return f"Complete Digital Setup: {name[:24]} Ecosystem ({count} Items)"
        elif "audio" in category_slug:
            return f"Audiophile Experience: {name[:24]} + Studio Companions"
        elif "kitchen" in category_slug or "home" in category_slug:
            return f"Modern Living Suite: {name[:24]} Essentials"
        return f"Curated Lifestyle Set: {name[:24]} ({count} Items)"

    def _format_product_summary(
        self, product: Product, is_focal: bool, role: str, score: float = 1.0
    ) -> Dict[str, Any]:
        return {
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "brand": product.brand.name if product.brand else "Generic",
            "price": product.price,
            "rating": product.rating,
            "image_url": (product.images[0].image_url if getattr(product, 'images', None) else getattr(product, 'image_url', '')) or '',
            "is_focal": is_focal,
            "role": role,
            "compatibility_score": round(score, 2),
        }
