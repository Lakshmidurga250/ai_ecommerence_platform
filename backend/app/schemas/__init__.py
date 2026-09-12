"""
Pydantic Schemas Package.
"""

from app.schemas.auth import Token, TokenData, UserRegister, UserLogin, RefreshTokenRequest
from app.schemas.user import UserRead, UserProfileRead, UserProfileUpdate, AddressCreate, AddressRead, AddressUpdate
from app.schemas.seller import SellerRegister, SellerRead, SellerUpdate, SellerStatusUpdate
from app.schemas.product import CategoryCreate, CategoryRead, BrandCreate, BrandRead, ProductCreate, ProductUpdate, ProductRead
from app.schemas.cart import CartItemAdd, CartItemUpdate, CartItemRead, CartRead, WishlistItemAdd, WishlistRead, CouponValidate, CouponCreate, CouponRead
from app.schemas.order import CheckoutRequest, OrderRead, OrderItemRead, OrderStatusUpdate, PaymentSimulateRequest, PaymentSimulationResponse, ReturnRequestCreate, ReturnRead
from app.schemas.inventory import WarehouseCreate, WarehouseRead, StockAdjustment, InventoryRead, LowStockAlert
from app.schemas.review import ReviewCreate, ReviewRead, ReviewSentimentRead, ReviewModerationUpdate
from app.schemas.support import SupportTicketCreate, SupportTicketRead, SupportMessageCreate, SupportMessageRead
from app.schemas.ai import (
    RecommendationItem, RecommendationResponse, ParsedSearchIntent,
    DemandForecastItem, FraudRiskEvaluation, CustomerSegmentProfile,
    ChurnRiskProfile, ShoppingAssistantRequest, ShoppingAssistantResponse
)
from app.schemas.analytics import BusinessOverviewMetrics, SellerDashboardMetrics, AuditLogRead, BehaviorEventCreate

__all__ = [
    "Token", "TokenData", "UserRegister", "UserLogin", "RefreshTokenRequest",
    "UserRead", "UserProfileRead", "UserProfileUpdate", "AddressCreate", "AddressRead", "AddressUpdate",
    "SellerRegister", "SellerRead", "SellerUpdate", "SellerStatusUpdate",
    "CategoryCreate", "CategoryRead", "BrandCreate", "BrandRead", "ProductCreate", "ProductUpdate", "ProductRead",
    "CartItemAdd", "CartItemUpdate", "CartItemRead", "CartRead", "WishlistItemAdd", "WishlistRead", "CouponValidate", "CouponCreate", "CouponRead",
    "CheckoutRequest", "OrderRead", "OrderItemRead", "OrderStatusUpdate", "PaymentSimulateRequest", "PaymentSimulationResponse", "ReturnRequestCreate", "ReturnRead",
    "WarehouseCreate", "WarehouseRead", "StockAdjustment", "InventoryRead", "LowStockAlert",
    "ReviewCreate", "ReviewRead", "ReviewSentimentRead", "ReviewModerationUpdate",
    "SupportTicketCreate", "SupportTicketRead", "SupportMessageCreate", "SupportMessageRead",
    "RecommendationItem", "RecommendationResponse", "ParsedSearchIntent",
    "DemandForecastItem", "FraudRiskEvaluation", "CustomerSegmentProfile",
    "ChurnRiskProfile", "ShoppingAssistantRequest", "ShoppingAssistantResponse",
    "BusinessOverviewMetrics", "SellerDashboardMetrics", "AuditLogRead", "BehaviorEventCreate"
]
