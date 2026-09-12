"""
Warehouse, Inventory, and Inventory Movements Models.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Warehouse(Base, TimestampMixin):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)  # e.g., "WH-BLR-01"
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), default="India")
    capacity_units = Column(Integer, default=50000, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    inventory_items = relationship("Inventory", back_populates="warehouse", cascade="all, delete-orphan")


class Inventory(Base, TimestampMixin):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = Column(Integer, default=0, nullable=False)
    reserved_quantity = Column(Integer, default=0, nullable=False)
    reorder_level = Column(Integer, default=10, nullable=False)

    warehouse = relationship("Warehouse", back_populates="inventory_items")
    product = relationship("Product", back_populates="inventory_items")
    movements = relationship("InventoryMovement", back_populates="inventory", cascade="all, delete-orphan")

    @property
    def available_quantity(self) -> int:
        return max(0, self.quantity - self.reserved_quantity)


class InventoryMovement(Base, TimestampMixin):
    __tablename__ = "inventory_movements"

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id", ondelete="CASCADE"), nullable=False, index=True)
    movement_type = Column(String(50), nullable=False)  # INBOUND, OUTBOUND, RESERVATION, RELEASE, ADJUSTMENT
    quantity = Column(Integer, nullable=False)
    reference_type = Column(String(50), nullable=True)  # ORDER, RETURN, RESTOCK, AUDIT
    reference_id = Column(String(100), nullable=True)
    notes = Column(String(255), nullable=True)

    inventory = relationship("Inventory", back_populates="movements")
