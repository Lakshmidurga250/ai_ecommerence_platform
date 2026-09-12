"""
Warehouse, Inventory, and Stock Movement Pydantic Schemas.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class WarehouseBase(BaseModel):
    name: str
    code: str
    address: str
    city: str
    state: str
    postal_code: str
    country: str = "India"
    capacity_units: int = 50000
    is_active: bool = True


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseRead(WarehouseBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StockAdjustment(BaseModel):
    warehouse_id: int
    product_id: int
    quantity_change: int  # Positive for restock, negative for deduction
    reason: str  # e.g., "Supplier Restock", "Damaged goods write-off"
    reference_id: Optional[str] = None


class InventoryMovementRead(BaseModel):
    id: int
    movement_type: str
    quantity: int
    reference_type: Optional[str] = None
    reference_id: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InventoryRead(BaseModel):
    id: int
    warehouse_id: int
    product_id: int
    quantity: int
    reserved_quantity: int
    available_quantity: int
    reorder_level: int
    warehouse: Optional[WarehouseRead] = None
    movements: List[InventoryMovementRead] = []

    model_config = ConfigDict(from_attributes=True)


class LowStockAlert(BaseModel):
    product_id: int
    product_name: str
    sku: str
    current_stock: int
    reserved_stock: int
    available_stock: int
    reorder_level: int
    urgency: str  # LOW, MEDIUM, CRITICAL
