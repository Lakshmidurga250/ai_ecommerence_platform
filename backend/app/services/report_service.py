"""
Report Generation Service.
Generates structured CSV and JSON exports for Sales, Inventory, and Fraud audits.
"""

import io
import csv
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.inventory import Inventory, Warehouse
from app.models.analytics import FraudAlert


class ReportService:
    @staticmethod
    def generate_sales_csv(db: Session) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Order Number", "Date", "Customer ID", "Status", "Subtotal", "Tax", "Discount", "Total Amount", "Payment Method"])

        orders = db.query(Order).order_by(Order.created_at.desc()).all()
        for o in orders:
            writer.writerow([
                o.order_number,
                o.created_at.strftime("%Y-%m-%d %H:%M:%S") if o.created_at else "",
                o.customer_id,
                o.status,
                o.subtotal,
                o.tax_amount,
                o.discount_amount,
                o.total_amount,
                o.payments[0].payment_method if o.payments else "N/A"
            ])
        return output.getvalue()

    @staticmethod
    def generate_inventory_csv(db: Session) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Product ID", "SKU", "Product Name", "Warehouse", "Total Stock", "Reserved Stock", "Available Stock", "Reorder Level", "Status"])

        inventories = db.query(Inventory).all()
        for inv in inventories:
            p = inv.product
            w = inv.warehouse
            status = "OUT_OF_STOCK" if inv.available_quantity == 0 else ("LOW_STOCK" if inv.available_quantity <= inv.reorder_level else "IN_STOCK")
            writer.writerow([
                inv.product_id,
                p.sku if p else "",
                p.name if p else "",
                w.name if w else "",
                inv.quantity,
                inv.reserved_quantity,
                inv.available_quantity,
                inv.reorder_level,
                status
            ])
        return output.getvalue()

    @staticmethod
    def generate_fraud_alerts_csv(db: Session) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Alert ID", "Order ID", "User ID", "Risk Score", "Risk Level", "Reasons", "Status", "Created At"])

        alerts = db.query(FraudAlert).order_by(FraudAlert.created_at.desc()).all()
        for a in alerts:
            writer.writerow([
                a.id,
                a.order_id,
                a.user_id,
                a.risk_score,
                a.risk_level,
                "; ".join(a.trigger_reasons or []),
                a.status,
                a.created_at.strftime("%Y-%m-%d %H:%M:%S") if a.created_at else ""
            ])
        return output.getvalue()
