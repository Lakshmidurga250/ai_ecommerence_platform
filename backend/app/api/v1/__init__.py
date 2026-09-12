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
