"""
MLOps & Model Registry API Router.
Provides model lifecycle management, offline evaluation benchmarks, and drift monitoring.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import RoleChecker
from ai.model_registry.mlops_service import MLOpsService

router = APIRouter(prefix="/mlops", tags=["MLOps & Model Registry"])


class ModelPromoteRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: Optional[str] = Field(None, description="Target status: STAGING, PRODUCTION, or RETIRED")
    target_stage: Optional[str] = Field(None, description="Target stage: STAGING, PRODUCTION, or RETIRED")


@router.get("/models", dependencies=[Depends(RoleChecker(["ADMIN"]))])
def list_models(db: Session = Depends(get_db)):
    """Retrieves all registered machine learning models, algorithms, and evaluation metrics."""
    return MLOpsService.list_registered_models(db)


@router.get("/drift", dependencies=[Depends(RoleChecker(["ADMIN"]))])
def get_model_drift(db: Session = Depends(get_db)):
    """Evaluates feature distribution shift and prediction drift across active production models."""
    res = MLOpsService.evaluate_model_drift(db)
    return res.get("drift_reports", [])


@router.post("/models/{model_id}/promote", dependencies=[Depends(RoleChecker(["ADMIN"]))])
def promote_model_deployment(
    model_id: int,
    payload: ModelPromoteRequest,
    db: Session = Depends(get_db)
):
    """Promotes or retires a machine learning model version."""
    target_status = payload.target_stage or payload.status or "PRODUCTION"
    return MLOpsService.promote_model(db, model_id, target_status)
