"""
Report Export API Endpoints (CSV & JSON).
"""

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import RoleChecker
from app.models.user import User
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Reporting Engine"])


@router.get("/sales/csv")
def download_sales_report_csv(
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN", "SELLER"]))
):
    """Download historical sales audit report in CSV format."""
    csv_data = ReportService.generate_sales_csv(db)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=sales_report.csv"}
    )


@router.get("/inventory/csv")
def download_inventory_report_csv(
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN", "SELLER"]))
):
    """Download live inventory and reorder audit report in CSV format."""
    csv_data = ReportService.generate_inventory_csv(db)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=inventory_report.csv"}
    )


@router.get("/fraud/csv")
def download_fraud_report_csv(
    db: Session = Depends(get_db),
    admin_user: User = Depends(RoleChecker(["ADMIN"]))
):
    """Download security fraud alerts audit report in CSV format."""
    csv_data = ReportService.generate_fraud_alerts_csv(db)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=fraud_alerts_report.csv"}
    )
