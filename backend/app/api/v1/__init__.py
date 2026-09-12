"""
API v1 Router Aggregator.
Combines all 30 functional module routers.
"""

from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.sellers import router as sellers_router
from app.api.v1.products import router as products_router
from app.api.v1.categories import router as categories_router
from app.api.v1.search import router as search_router
from app.api.v1.cart import router as cart_router
from app.api.v1.wishlist import router as wishlist_router
from app.api.v1.orders import router as orders_router
from app.api.v1.payments import router as payments_router
from app.api.v1.coupons import router as coupons_router
from app.api.v1.inventory import router as inventory_router
from app.api.v1.shipping import router as shipping_router
from app.api.v1.returns import router as returns_router
from app.api.v1.reviews import router as reviews_router
from app.api.v1.support import router as support_router
from app.api.v1.ai import router as ai_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.admin import router as admin_router
from app.api.v1.reports import router as reports_router
from app.api.v1.customer_expansion import router as customer_expansion_router
from app.api.v1.marketplace import router as marketplace_router
from app.api.v1.visual_search import router as visual_search_router
from app.api.v1.customer_intelligence import router as customer_intelligence_router
from app.api.v1.inventory_intelligence import router as inventory_intelligence_router
from app.api.v1.fraud_center import router as fraud_center_router
from app.api.v1.logistics import router as logistics_router
from app.api.v1.events import router as events_router
from app.api.v1.mlops import router as mlops_router
from app.api.v1.experiments import router as experiments_router
from app.api.v1.loyalty import router as loyalty_router
from app.api.v1.recommendations_v3 import router as recommendations_v3_router
from app.api.v1.commerce_intelligence import router as commerce_intelligence_router
from app.api.v1.analytics_v3 import router as analytics_v3_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(sellers_router)
api_v1_router.include_router(products_router)
api_v1_router.include_router(categories_router)
api_v1_router.include_router(search_router)
api_v1_router.include_router(cart_router)
api_v1_router.include_router(wishlist_router)
api_v1_router.include_router(orders_router)
api_v1_router.include_router(payments_router)
api_v1_router.include_router(coupons_router)
api_v1_router.include_router(inventory_router)
api_v1_router.include_router(shipping_router)
api_v1_router.include_router(returns_router)
api_v1_router.include_router(reviews_router)
api_v1_router.include_router(support_router)
api_v1_router.include_router(ai_router)
api_v1_router.include_router(analytics_router)
api_v1_router.include_router(admin_router)
api_v1_router.include_router(reports_router)
api_v1_router.include_router(customer_expansion_router)
api_v1_router.include_router(marketplace_router)
api_v1_router.include_router(visual_search_router)
api_v1_router.include_router(customer_intelligence_router)
api_v1_router.include_router(inventory_intelligence_router)
api_v1_router.include_router(fraud_center_router)
api_v1_router.include_router(logistics_router)
api_v1_router.include_router(events_router)
api_v1_router.include_router(mlops_router)
api_v1_router.include_router(experiments_router)
api_v1_router.include_router(loyalty_router)
api_v1_router.include_router(recommendations_v3_router)
api_v1_router.include_router(commerce_intelligence_router)
api_v1_router.include_router(analytics_v3_router)
