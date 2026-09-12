"""
Inventory & Multi-Warehouse API Endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import RoleChecker
from app.models.user import User
from app.models.inventory import Warehouse, Inventory
from app.schemas.inventory import LowStockAlert, StockAdjustment, WarehouseRead, WarehouseCreate, InventoryRead
from app.services.inventory_service import InventoryService
from app.services.seller_service import SellerService

router = APIRouter(prefix="/inventory", tags=["Inventory Intelligence"])


@router.get("/low-stock-alerts", response_model=List[LowStockAlert])
def get_low_stock_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["SELLER", "ADMIN"]))
):
    """Retrieve intelligence alerts for products nearing or exceeding reorder thresholds."""
    is_admin = "ADMIN" in current_user.role_names
    seller_id = None if is_admin else SellerService.get_seller_by_user_id(db, current_user.id).id
    return InventoryService.get_low_stock_alerts(db, seller_id=seller_id)


@router.post("/adjustment", response_model=InventoryRead)
def record_stock_adjustment(
    data: StockAdjustment,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["SELLER", "ADMIN"]))
):
    """Record manual inbound restock or adjustment with audit notes."""
    return InventoryService.adjust_stock(
        db=db,
        warehouse_id=data.warehouse_id,
        product_id=data.product_id,
        quantity_change=data.quantity_change,
        reason=data.reason,
        reference_id=data.reference_id
    )


@router.get("/warehouses", response_model=List[WarehouseRead])
def list_warehouses(
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["SELLER", "ADMIN"]))
):
    """List operational fulfillment warehouses."""
    return db.query(Warehouse).all()


@router.post("/warehouses", response_model=WarehouseRead, status_code=status.HTTP_201_CREATED)
def create_warehouse(
    data: WarehouseCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN"]))
):
    """Register a new distribution center or warehouse (Admins only)."""
    wh = Warehouse(**data.model_dump())
    db.add(wh)
    db.commit()
    db.refresh(wh)
    return wh
