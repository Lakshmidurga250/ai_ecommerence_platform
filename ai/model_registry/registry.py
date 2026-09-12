"""
Model Registry & Versioning System.
Tracks model lifecycle, hyperparameters, real evaluation metrics, and production status.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.analytics import ModelRegistryEntry
from app.core.logging import logger


class ModelRegistryService:
    @staticmethod
    def register_model(
        db: Session,
        model_name: str,
        version: str,
        algorithm: str,
        dataset_version: str,
        hyperparameters: Dict[str, Any],
        metrics: Dict[str, Any],
        artifact_path: Optional[str] = None,
        status: str = "PRODUCTION"
    ) -> ModelRegistryEntry:
        """Register a newly trained model version with verified evaluation metrics."""
        # Check if version exists
        entry = db.query(ModelRegistryEntry).filter(
            ModelRegistryEntry.model_name == model_name,
            ModelRegistryEntry.version == version
        ).first()

        if entry:
            entry.algorithm = algorithm
            entry.dataset_version = dataset_version
            entry.hyperparameters = hyperparameters
            entry.metrics = metrics
            entry.artifact_path = artifact_path
            entry.status = status
        else:
            entry = ModelRegistryEntry(
                model_name=model_name,
                version=version,
                algorithm=algorithm,
                dataset_version=dataset_version,
                hyperparameters=hyperparameters,
                metrics=metrics,
                artifact_path=artifact_path,
                status=status
            )
            db.add(entry)

        db.commit()
        db.refresh(entry)
        logger.info(f"Model '{model_name}' [{version}] registered with status {status}. Metrics: {metrics}")
        return entry

    @staticmethod
    def list_models(db: Session) -> List[ModelRegistryEntry]:
        return db.query(ModelRegistryEntry).order_by(ModelRegistryEntry.created_at.desc()).all()

    @staticmethod
    def get_production_model(db: Session, model_name: str) -> Optional[ModelRegistryEntry]:
        return db.query(ModelRegistryEntry).filter(
            ModelRegistryEntry.model_name == model_name,
            ModelRegistryEntry.status == "PRODUCTION"
        ).order_by(ModelRegistryEntry.created_at.desc()).first()
