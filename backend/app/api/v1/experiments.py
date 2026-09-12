"""
A/B Testing & Experimentation API Router.
Provides experiment registry, traffic allocation, and conversion lift analytics.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import RoleChecker
from app.services.ab_testing_service import ABTestingService

router = APIRouter(prefix="/experiments", tags=["A/B Testing & Experimentation"])


class ExperimentEventRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    experiment_id: int
    variant: str = Field(..., description="CONTROL or VARIANT")
    event_type: str = Field(..., description="IMPRESSION, CLICK, CONVERSION, REVENUE")
    value: float = Field(1.0, description="Event monetary or count value")
    user_id: Optional[int] = None
    session_id: Optional[str] = None


@router.get("")
@router.get("/")
def list_experiments(db: Session = Depends(get_db)):
    """Retrieves all active and historical A/B experiments."""
    experiments = ABTestingService.get_or_create_default_experiments(db)
    return [{
        "id": exp.id,
        "experiment_id": exp.id,
        "name": exp.name,
        "description": exp.description,
        "status": exp.status,
        "traffic_split_ratio": exp.traffic_split_ratio,
        "target_metric": exp.target_metric,
        "control_config": exp.control_config,
        "variant_config": exp.variant_config
    } for exp in experiments]


@router.get("/{experiment_id}/analytics")
def get_experiment_analytics(
    experiment_id: int,
    db: Session = Depends(get_db)
):
    """Calculates conversion lift, p-value, and statistical significance for an experiment."""
    return ABTestingService.get_experiment_results(db, experiment_id)


@router.post("/events", status_code=status.HTTP_201_CREATED)
def log_experiment_event(
    payload: ExperimentEventRequest,
    db: Session = Depends(get_db)
):
    """Logs an impression, click, or conversion within an A/B experiment."""
    ev = ABTestingService.track_experiment_event(
        db=db,
        experiment_id=payload.experiment_id,
        variant=payload.variant,
        event_type=payload.event_type,
        user_id=payload.user_id,
        session_id=payload.session_id,
        value=payload.value
    )
    return {"status": "SUCCESS", "event_id": ev.id}
