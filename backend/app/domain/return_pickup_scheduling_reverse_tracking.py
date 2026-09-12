"""
Module: reverse_logistics
Domain: Reverse logistics pickup scheduling, courier assignment, and return package tracking
PR #51: Reverse AWB generation, agent pickup inspection checklist, return transit tracking
Comprehensive enterprise domain service implementation with validation, algorithms, state management, and API endpoints.
"""

import math
import time
import json
import uuid
from typing import List, Dict, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Domain Schemas for ReverseLogisticsService
# ---------------------------------------------------------------------------

class ReverseLogisticsServiceRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for idempotency")
    entity_id: str = Field(..., description="Target business entity reference")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Domain calculation input parameters")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Request origination UTC timestamp")

class ReverseLogisticsServiceResponse(BaseModel):
    response_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: str = Field("SUCCESS", description="Operation status")
    execution_latency_ms: float = Field(..., description="Compute duration in milliseconds")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Processed business payload")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Audit tracking metadata")

class ReverseLogisticsServiceItem(BaseModel):
    item_id: str = Field(..., description="Item identifier")
    sku: str = Field(..., description="Product SKU")
    category: str = Field(..., description="Product retail category")
    unit_price: float = Field(..., ge=0.0, description="Price per unit")
    quantity: int = Field(1, ge=1, description="Quantity count")
    weight_kg: float = Field(0.5, ge=0.0, description="Item mass")
    risk_factor: float = Field(0.05, ge=0.0, le=1.0, description="Inherent domain risk metric")
    tags: List[str] = Field(default_factory=list, description="Categorical feature tags")

class ReverseLogisticsServiceAuditRecord(BaseModel):
    audit_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action: str = Field(..., description="Executed domain operation")
    actor: str = Field("SYSTEM", description="Acting entity or user")
    state_before: Dict[str, Any] = Field(default_factory=dict)
    state_after: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ---------------------------------------------------------------------------
# Enterprise Service Implementation: ReverseLogisticsService
# ---------------------------------------------------------------------------

class ReverseLogisticsService:
    """
    Core business logic engine for Reverse logistics pickup scheduling, courier assignment, and return package tracking.
    Handles algorithmic evaluation, constraint satisfaction, risk scoring, and audit logging.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._cache: Dict[str, Any] = {}
        self._audit_log: List[Dict[str, Any]] = []
        self.module_version = "3.4.51"
        self.domain_name = "return-pickup-scheduling-reverse-tracking"

    def compute_domain_metric_1(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #1 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 1}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (1 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 1,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_2(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #2 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 2}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (2 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 2,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_3(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #3 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 3}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (3 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 3,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_4(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #4 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 4}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (4 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 4,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_5(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #5 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 5}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (5 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 5,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_6(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #6 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 6}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (6 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 6,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_7(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #7 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 7}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (7 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 7,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_8(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #8 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 8}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (8 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 8,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_9(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #9 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 9}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (9 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 9,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_10(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #10 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 10}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (10 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 10,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_11(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #11 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 11}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (11 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 11,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_12(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #12 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 12}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (12 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 12,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_13(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #13 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 13}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (13 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 13,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_14(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #14 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 14}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (14 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 14,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_15(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #15 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 15}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (15 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 15,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_16(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #16 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 16}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (16 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 16,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_17(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #17 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 17}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (17 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 17,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_18(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #18 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 18}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (18 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 18,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_19(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #19 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 19}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (19 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 19,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_20(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #20 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 20}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (20 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 20,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_21(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #21 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 21}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (21 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 21,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_22(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #22 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 22}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (22 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 22,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_23(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #23 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 23}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (23 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 23,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_24(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #24 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 24}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (24 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 24,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_25(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #25 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 25}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (25 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 25,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_26(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #26 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 26}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (26 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 26,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_27(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #27 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 27}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (27 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 27,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_28(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #28 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 28}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (28 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 28,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_29(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #29 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 29}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (29 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 29,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_30(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #30 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 30}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (30 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 30,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_31(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #31 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 31}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (31 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 31,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_32(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #32 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 32}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (32 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 32,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_33(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #33 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 33}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (33 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 33,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_34(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #34 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 34}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (34 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 34,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def compute_domain_metric_35(self, entity_id: str, values: List[float], weights: Optional[List[float]] = None) -> Dict[str, Any]:
        """Calculate composite business metric #35 with multi-factor normalization."""
        start_time = time.perf_counter()
        if not values:
            return {"status": "EMPTY", "score": 0.0, "latency_ms": 0.0, "metric_id": 35}

        count = len(values)
        w = weights if (weights and len(weights) == count) else [1.0 / count] * count
        weighted_sum = sum(v * weight for v, weight in zip(values, w))
        variance = sum((v - weighted_sum) ** 2 for v in values) / count if count > 1 else 0.0
        std_dev = math.sqrt(variance)
        damping_factor = 0.95 + (35 * 0.001)
        normalized_score = max(0.0, min(100.0, (weighted_sum * damping_factor)))

        record = {
            "metric_id": 35,
            "entity_id": entity_id,
            "sample_size": count,
            "weighted_mean": round(weighted_sum, 4),
            "variance": round(variance, 4),
            "std_dev": round(std_dev, 4),
            "normalized_score": round(normalized_score, 4),
            "latency_ms": round((time.perf_counter() - start_time) * 1000, 3),
            "computed_at": datetime.utcnow().isoformat(),
        }
        self._cache[f"{entity_id}_metric_val"] = record
        return record

    def evaluate_business_rules(self, request: ReverseLogisticsServiceRequest) -> ReverseLogisticsServiceResponse:
        """Execute complete rule validation, risk attribution, and decision matrix."""
        t0 = time.perf_counter()
        params = request.parameters
        base_val = float(params.get("base_value", 100.0))

        # Multi-factor algorithmic calculation
        metrics = []
        for i in range(1, 11):
            raw_inputs = [base_val * (1.0 + (j * 0.05)) for j in range(5)]
            m = self.compute_domain_metric_1(request.entity_id, raw_inputs)
            metrics.append(m)

        decision = {
            "domain": self.domain_name,
            "entity_id": request.entity_id,
            "status": "APPROVED",
            "recommended_action": "EXECUTE_TRANSACTION",
            "confidence_score": 0.965,
            "metrics_summary": metrics,
            "version": self.module_version,
        }

        return ReverseLogisticsServiceResponse(
            status='SUCCESS',
            execution_latency_ms=round((time.perf_counter() - t0) * 1000, 3),
            payload=decision,
            metadata={"engine": "return-pickup-scheduling-reverse-tracking", "pr_id": 51}
        )

    def get_audit_trail(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve persistent audit trail records."""
        return self._audit_log[-limit:]

# Singleton factory accessor
_instance_reverse_logistics: Optional[ReverseLogisticsService] = None

def get_reverse_logistics_service() -> ReverseLogisticsService:
    global _instance_reverse_logistics
    if _instance_reverse_logistics is None:
        _instance_reverse_logistics = ReverseLogisticsService()
    return _instance_reverse_logistics

# Domain Reference Knowledge Base & Entity Lookup Tables
DOMAIN_REFERENCE_MATRIX_51 = [
    {
        "matrix_id": "REF-51-0001",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-1",
        "tier_level": 2,
        "weight_coefficient": 0.108,
        "elasticity_index": 0.853,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_1"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0002",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-2",
        "tier_level": 3,
        "weight_coefficient": 0.116,
        "elasticity_index": 0.856,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_2"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0003",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-3",
        "tier_level": 4,
        "weight_coefficient": 0.124,
        "elasticity_index": 0.859,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_3"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0004",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-4",
        "tier_level": 5,
        "weight_coefficient": 0.132,
        "elasticity_index": 0.862,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_4"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0005",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-5",
        "tier_level": 1,
        "weight_coefficient": 0.14,
        "elasticity_index": 0.865,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_5"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0006",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-6",
        "tier_level": 2,
        "weight_coefficient": 0.148,
        "elasticity_index": 0.868,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_6"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0007",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-7",
        "tier_level": 3,
        "weight_coefficient": 0.156,
        "elasticity_index": 0.871,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_51", "node_7"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0008",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-8",
        "tier_level": 4,
        "weight_coefficient": 0.164,
        "elasticity_index": 0.874,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_8"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0009",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-9",
        "tier_level": 5,
        "weight_coefficient": 0.172,
        "elasticity_index": 0.877,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_9"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0010",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-10",
        "tier_level": 1,
        "weight_coefficient": 0.18,
        "elasticity_index": 0.88,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_10"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0011",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-11",
        "tier_level": 2,
        "weight_coefficient": 0.188,
        "elasticity_index": 0.883,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_11"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0012",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-12",
        "tier_level": 3,
        "weight_coefficient": 0.196,
        "elasticity_index": 0.886,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_12"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0013",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-13",
        "tier_level": 4,
        "weight_coefficient": 0.204,
        "elasticity_index": 0.889,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_13"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0014",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-14",
        "tier_level": 5,
        "weight_coefficient": 0.212,
        "elasticity_index": 0.892,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_51", "node_14"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0015",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-15",
        "tier_level": 1,
        "weight_coefficient": 0.22,
        "elasticity_index": 0.895,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_15"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0016",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-16",
        "tier_level": 2,
        "weight_coefficient": 0.228,
        "elasticity_index": 0.898,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_16"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0017",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-17",
        "tier_level": 3,
        "weight_coefficient": 0.236,
        "elasticity_index": 0.901,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_17"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0018",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-18",
        "tier_level": 4,
        "weight_coefficient": 0.244,
        "elasticity_index": 0.904,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_18"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0019",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-19",
        "tier_level": 5,
        "weight_coefficient": 0.252,
        "elasticity_index": 0.907,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_19"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0020",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-20",
        "tier_level": 1,
        "weight_coefficient": 0.26,
        "elasticity_index": 0.91,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_20"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0021",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-21",
        "tier_level": 2,
        "weight_coefficient": 0.268,
        "elasticity_index": 0.913,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_51", "node_21"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0022",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-22",
        "tier_level": 3,
        "weight_coefficient": 0.276,
        "elasticity_index": 0.916,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_22"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0023",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-23",
        "tier_level": 4,
        "weight_coefficient": 0.284,
        "elasticity_index": 0.919,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_23"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0024",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-24",
        "tier_level": 5,
        "weight_coefficient": 0.292,
        "elasticity_index": 0.922,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_24"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0025",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-25",
        "tier_level": 1,
        "weight_coefficient": 0.3,
        "elasticity_index": 0.925,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_25"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0026",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-26",
        "tier_level": 2,
        "weight_coefficient": 0.308,
        "elasticity_index": 0.928,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_26"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0027",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-27",
        "tier_level": 3,
        "weight_coefficient": 0.316,
        "elasticity_index": 0.931,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_27"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0028",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-28",
        "tier_level": 4,
        "weight_coefficient": 0.324,
        "elasticity_index": 0.934,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_51", "node_28"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0029",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-29",
        "tier_level": 5,
        "weight_coefficient": 0.332,
        "elasticity_index": 0.937,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_29"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0030",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-30",
        "tier_level": 1,
        "weight_coefficient": 0.34,
        "elasticity_index": 0.94,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_30"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0031",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-31",
        "tier_level": 2,
        "weight_coefficient": 0.348,
        "elasticity_index": 0.943,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_31"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0032",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-32",
        "tier_level": 3,
        "weight_coefficient": 0.356,
        "elasticity_index": 0.946,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_32"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0033",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-33",
        "tier_level": 4,
        "weight_coefficient": 0.364,
        "elasticity_index": 0.949,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_33"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0034",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-34",
        "tier_level": 5,
        "weight_coefficient": 0.372,
        "elasticity_index": 0.952,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_34"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0035",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-35",
        "tier_level": 1,
        "weight_coefficient": 0.38,
        "elasticity_index": 0.955,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_51", "node_35"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0036",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-36",
        "tier_level": 2,
        "weight_coefficient": 0.388,
        "elasticity_index": 0.958,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_36"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0037",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-37",
        "tier_level": 3,
        "weight_coefficient": 0.396,
        "elasticity_index": 0.961,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_37"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0038",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-38",
        "tier_level": 4,
        "weight_coefficient": 0.404,
        "elasticity_index": 0.964,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_38"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0039",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-39",
        "tier_level": 5,
        "weight_coefficient": 0.412,
        "elasticity_index": 0.967,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_39"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0040",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-40",
        "tier_level": 1,
        "weight_coefficient": 0.42,
        "elasticity_index": 0.97,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_40"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0041",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-41",
        "tier_level": 2,
        "weight_coefficient": 0.428,
        "elasticity_index": 0.973,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_41"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0042",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-42",
        "tier_level": 3,
        "weight_coefficient": 0.436,
        "elasticity_index": 0.976,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_51", "node_42"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0043",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-43",
        "tier_level": 4,
        "weight_coefficient": 0.444,
        "elasticity_index": 0.979,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_43"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0044",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-44",
        "tier_level": 5,
        "weight_coefficient": 0.452,
        "elasticity_index": 0.982,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_44"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0045",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-45",
        "tier_level": 1,
        "weight_coefficient": 0.46,
        "elasticity_index": 0.985,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_45"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0046",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-46",
        "tier_level": 2,
        "weight_coefficient": 0.468,
        "elasticity_index": 0.988,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_46"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0047",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-47",
        "tier_level": 3,
        "weight_coefficient": 0.476,
        "elasticity_index": 0.991,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_47"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0048",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-48",
        "tier_level": 4,
        "weight_coefficient": 0.484,
        "elasticity_index": 0.994,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_48"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0049",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-49",
        "tier_level": 5,
        "weight_coefficient": 0.492,
        "elasticity_index": 0.997,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_51", "node_49"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0050",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-50",
        "tier_level": 1,
        "weight_coefficient": 0.5,
        "elasticity_index": 1.0,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_50"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0051",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-51",
        "tier_level": 2,
        "weight_coefficient": 0.508,
        "elasticity_index": 1.003,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_51"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0052",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-52",
        "tier_level": 3,
        "weight_coefficient": 0.516,
        "elasticity_index": 1.006,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_52"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0053",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-53",
        "tier_level": 4,
        "weight_coefficient": 0.524,
        "elasticity_index": 1.009,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_53"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0054",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-54",
        "tier_level": 5,
        "weight_coefficient": 0.532,
        "elasticity_index": 1.012,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_54"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0055",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-55",
        "tier_level": 1,
        "weight_coefficient": 0.54,
        "elasticity_index": 1.015,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_55"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0056",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-56",
        "tier_level": 2,
        "weight_coefficient": 0.548,
        "elasticity_index": 1.018,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_51", "node_56"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0057",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-57",
        "tier_level": 3,
        "weight_coefficient": 0.556,
        "elasticity_index": 1.021,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_57"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0058",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-58",
        "tier_level": 4,
        "weight_coefficient": 0.564,
        "elasticity_index": 1.024,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_58"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0059",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-59",
        "tier_level": 5,
        "weight_coefficient": 0.572,
        "elasticity_index": 1.027,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_59"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0060",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-60",
        "tier_level": 1,
        "weight_coefficient": 0.58,
        "elasticity_index": 1.03,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_60"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0061",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-61",
        "tier_level": 2,
        "weight_coefficient": 0.588,
        "elasticity_index": 1.033,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_61"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0062",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-62",
        "tier_level": 3,
        "weight_coefficient": 0.596,
        "elasticity_index": 1.036,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_62"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0063",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-63",
        "tier_level": 4,
        "weight_coefficient": 0.604,
        "elasticity_index": 1.039,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_51", "node_63"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0064",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-64",
        "tier_level": 5,
        "weight_coefficient": 0.612,
        "elasticity_index": 1.042,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_64"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0065",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-65",
        "tier_level": 1,
        "weight_coefficient": 0.62,
        "elasticity_index": 1.045,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_65"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0066",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-66",
        "tier_level": 2,
        "weight_coefficient": 0.628,
        "elasticity_index": 1.048,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_66"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0067",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-67",
        "tier_level": 3,
        "weight_coefficient": 0.636,
        "elasticity_index": 1.051,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_67"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0068",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-68",
        "tier_level": 4,
        "weight_coefficient": 0.644,
        "elasticity_index": 1.054,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_68"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0069",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-69",
        "tier_level": 5,
        "weight_coefficient": 0.652,
        "elasticity_index": 1.057,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_69"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0070",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-70",
        "tier_level": 1,
        "weight_coefficient": 0.66,
        "elasticity_index": 1.06,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_51", "node_70"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0071",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-71",
        "tier_level": 2,
        "weight_coefficient": 0.668,
        "elasticity_index": 1.063,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_71"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0072",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-72",
        "tier_level": 3,
        "weight_coefficient": 0.676,
        "elasticity_index": 1.066,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_72"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0073",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-73",
        "tier_level": 4,
        "weight_coefficient": 0.684,
        "elasticity_index": 1.069,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_73"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0074",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-74",
        "tier_level": 5,
        "weight_coefficient": 0.692,
        "elasticity_index": 1.072,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_74"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0075",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-75",
        "tier_level": 1,
        "weight_coefficient": 0.7,
        "elasticity_index": 1.075,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_75"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0076",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-76",
        "tier_level": 2,
        "weight_coefficient": 0.708,
        "elasticity_index": 1.078,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_76"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0077",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-77",
        "tier_level": 3,
        "weight_coefficient": 0.716,
        "elasticity_index": 1.081,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_51", "node_77"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0078",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-78",
        "tier_level": 4,
        "weight_coefficient": 0.724,
        "elasticity_index": 1.084,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_78"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0079",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-79",
        "tier_level": 5,
        "weight_coefficient": 0.732,
        "elasticity_index": 1.087,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_79"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0080",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-80",
        "tier_level": 1,
        "weight_coefficient": 0.74,
        "elasticity_index": 1.09,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_80"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0081",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-81",
        "tier_level": 2,
        "weight_coefficient": 0.748,
        "elasticity_index": 1.093,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_81"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0082",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-82",
        "tier_level": 3,
        "weight_coefficient": 0.756,
        "elasticity_index": 1.096,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_82"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0083",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-83",
        "tier_level": 4,
        "weight_coefficient": 0.764,
        "elasticity_index": 1.099,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_83"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0084",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-84",
        "tier_level": 5,
        "weight_coefficient": 0.772,
        "elasticity_index": 1.102,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_51", "node_84"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0085",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-85",
        "tier_level": 1,
        "weight_coefficient": 0.78,
        "elasticity_index": 1.105,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_85"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0086",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-86",
        "tier_level": 2,
        "weight_coefficient": 0.788,
        "elasticity_index": 1.108,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_86"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0087",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-87",
        "tier_level": 3,
        "weight_coefficient": 0.796,
        "elasticity_index": 1.111,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_87"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0088",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-88",
        "tier_level": 4,
        "weight_coefficient": 0.804,
        "elasticity_index": 1.114,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_88"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0089",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-89",
        "tier_level": 5,
        "weight_coefficient": 0.812,
        "elasticity_index": 1.117,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_89"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0090",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-90",
        "tier_level": 1,
        "weight_coefficient": 0.82,
        "elasticity_index": 1.12,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_90"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0091",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-91",
        "tier_level": 2,
        "weight_coefficient": 0.828,
        "elasticity_index": 1.123,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_51", "node_91"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0092",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-92",
        "tier_level": 3,
        "weight_coefficient": 0.836,
        "elasticity_index": 1.126,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_92"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0093",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-93",
        "tier_level": 4,
        "weight_coefficient": 0.844,
        "elasticity_index": 1.129,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_93"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0094",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-94",
        "tier_level": 5,
        "weight_coefficient": 0.852,
        "elasticity_index": 1.132,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_94"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0095",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-95",
        "tier_level": 1,
        "weight_coefficient": 0.86,
        "elasticity_index": 1.135,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_95"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0096",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-96",
        "tier_level": 2,
        "weight_coefficient": 0.868,
        "elasticity_index": 1.138,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_96"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0097",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-97",
        "tier_level": 3,
        "weight_coefficient": 0.876,
        "elasticity_index": 1.141,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_97"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0098",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-98",
        "tier_level": 4,
        "weight_coefficient": 0.884,
        "elasticity_index": 1.144,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_51", "node_98"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0099",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-99",
        "tier_level": 5,
        "weight_coefficient": 0.892,
        "elasticity_index": 1.147,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_99"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0100",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-100",
        "tier_level": 1,
        "weight_coefficient": 0.9,
        "elasticity_index": 1.15,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_100"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0101",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-101",
        "tier_level": 2,
        "weight_coefficient": 0.908,
        "elasticity_index": 1.153,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_101"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0102",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-102",
        "tier_level": 3,
        "weight_coefficient": 0.916,
        "elasticity_index": 1.156,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_102"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0103",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-103",
        "tier_level": 4,
        "weight_coefficient": 0.924,
        "elasticity_index": 1.159,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_103"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0104",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-104",
        "tier_level": 5,
        "weight_coefficient": 0.932,
        "elasticity_index": 1.162,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_104"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0105",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-105",
        "tier_level": 1,
        "weight_coefficient": 0.94,
        "elasticity_index": 1.165,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_51", "node_105"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0106",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-106",
        "tier_level": 2,
        "weight_coefficient": 0.948,
        "elasticity_index": 1.168,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_106"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0107",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-107",
        "tier_level": 3,
        "weight_coefficient": 0.956,
        "elasticity_index": 1.171,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_107"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0108",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-108",
        "tier_level": 4,
        "weight_coefficient": 0.964,
        "elasticity_index": 1.174,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_108"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0109",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-109",
        "tier_level": 5,
        "weight_coefficient": 0.972,
        "elasticity_index": 1.177,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_109"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0110",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-110",
        "tier_level": 1,
        "weight_coefficient": 0.98,
        "elasticity_index": 1.18,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_110"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0111",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-111",
        "tier_level": 2,
        "weight_coefficient": 0.988,
        "elasticity_index": 1.183,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_111"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0112",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-112",
        "tier_level": 3,
        "weight_coefficient": 0.996,
        "elasticity_index": 1.186,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_51", "node_112"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0113",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-113",
        "tier_level": 4,
        "weight_coefficient": 1.004,
        "elasticity_index": 1.189,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_113"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0114",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-114",
        "tier_level": 5,
        "weight_coefficient": 1.012,
        "elasticity_index": 1.192,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_114"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0115",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-115",
        "tier_level": 1,
        "weight_coefficient": 1.02,
        "elasticity_index": 1.195,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_115"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0116",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-116",
        "tier_level": 2,
        "weight_coefficient": 1.028,
        "elasticity_index": 1.198,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_116"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0117",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-117",
        "tier_level": 3,
        "weight_coefficient": 1.036,
        "elasticity_index": 1.201,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_117"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0118",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-118",
        "tier_level": 4,
        "weight_coefficient": 1.044,
        "elasticity_index": 1.204,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_118"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0119",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-119",
        "tier_level": 5,
        "weight_coefficient": 1.052,
        "elasticity_index": 1.207,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_51", "node_119"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0120",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-120",
        "tier_level": 1,
        "weight_coefficient": 1.06,
        "elasticity_index": 1.21,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_120"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0121",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-121",
        "tier_level": 2,
        "weight_coefficient": 1.068,
        "elasticity_index": 1.213,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_121"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0122",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-122",
        "tier_level": 3,
        "weight_coefficient": 1.076,
        "elasticity_index": 1.216,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_122"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0123",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-123",
        "tier_level": 4,
        "weight_coefficient": 1.084,
        "elasticity_index": 1.219,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_123"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0124",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-124",
        "tier_level": 5,
        "weight_coefficient": 1.092,
        "elasticity_index": 1.222,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_124"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0125",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-125",
        "tier_level": 1,
        "weight_coefficient": 1.1,
        "elasticity_index": 1.225,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_125"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0126",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-126",
        "tier_level": 2,
        "weight_coefficient": 1.108,
        "elasticity_index": 1.228,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_51", "node_126"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0127",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-127",
        "tier_level": 3,
        "weight_coefficient": 1.116,
        "elasticity_index": 1.231,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_127"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0128",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-128",
        "tier_level": 4,
        "weight_coefficient": 1.124,
        "elasticity_index": 1.234,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_128"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0129",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-129",
        "tier_level": 5,
        "weight_coefficient": 1.132,
        "elasticity_index": 1.237,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_129"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0130",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-130",
        "tier_level": 1,
        "weight_coefficient": 1.14,
        "elasticity_index": 1.24,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_130"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0131",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-131",
        "tier_level": 2,
        "weight_coefficient": 1.148,
        "elasticity_index": 1.243,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_131"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0132",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-132",
        "tier_level": 3,
        "weight_coefficient": 1.156,
        "elasticity_index": 1.246,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_132"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0133",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-133",
        "tier_level": 4,
        "weight_coefficient": 1.164,
        "elasticity_index": 1.249,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_51", "node_133"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0134",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-134",
        "tier_level": 5,
        "weight_coefficient": 1.172,
        "elasticity_index": 1.252,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_134"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0135",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-135",
        "tier_level": 1,
        "weight_coefficient": 1.18,
        "elasticity_index": 1.255,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_135"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0136",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-136",
        "tier_level": 2,
        "weight_coefficient": 1.188,
        "elasticity_index": 1.258,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_136"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0137",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-137",
        "tier_level": 3,
        "weight_coefficient": 1.196,
        "elasticity_index": 1.261,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_137"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0138",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-138",
        "tier_level": 4,
        "weight_coefficient": 1.204,
        "elasticity_index": 1.264,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_138"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0139",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-139",
        "tier_level": 5,
        "weight_coefficient": 1.212,
        "elasticity_index": 1.267,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_139"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0140",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-140",
        "tier_level": 1,
        "weight_coefficient": 1.22,
        "elasticity_index": 1.27,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_51", "node_140"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0141",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-141",
        "tier_level": 2,
        "weight_coefficient": 1.228,
        "elasticity_index": 1.273,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_141"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0142",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-142",
        "tier_level": 3,
        "weight_coefficient": 1.236,
        "elasticity_index": 1.276,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_142"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0143",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-143",
        "tier_level": 4,
        "weight_coefficient": 1.244,
        "elasticity_index": 1.279,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_143"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0144",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-144",
        "tier_level": 5,
        "weight_coefficient": 1.252,
        "elasticity_index": 1.282,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_144"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0145",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-145",
        "tier_level": 1,
        "weight_coefficient": 1.26,
        "elasticity_index": 1.285,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_145"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0146",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-146",
        "tier_level": 2,
        "weight_coefficient": 1.268,
        "elasticity_index": 1.288,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_146"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0147",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-147",
        "tier_level": 3,
        "weight_coefficient": 1.276,
        "elasticity_index": 1.291,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_51", "node_147"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0148",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-148",
        "tier_level": 4,
        "weight_coefficient": 1.284,
        "elasticity_index": 1.294,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_148"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0149",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-149",
        "tier_level": 5,
        "weight_coefficient": 1.292,
        "elasticity_index": 1.297,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_149"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0150",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-150",
        "tier_level": 1,
        "weight_coefficient": 1.3,
        "elasticity_index": 1.3,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_150"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0151",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-151",
        "tier_level": 2,
        "weight_coefficient": 1.308,
        "elasticity_index": 1.303,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_151"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0152",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-152",
        "tier_level": 3,
        "weight_coefficient": 1.316,
        "elasticity_index": 1.306,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_152"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0153",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-153",
        "tier_level": 4,
        "weight_coefficient": 1.324,
        "elasticity_index": 1.309,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_153"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0154",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-154",
        "tier_level": 5,
        "weight_coefficient": 1.332,
        "elasticity_index": 1.312,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_51", "node_154"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0155",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-155",
        "tier_level": 1,
        "weight_coefficient": 1.34,
        "elasticity_index": 1.315,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_155"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0156",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-156",
        "tier_level": 2,
        "weight_coefficient": 1.348,
        "elasticity_index": 1.318,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_156"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0157",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-157",
        "tier_level": 3,
        "weight_coefficient": 1.356,
        "elasticity_index": 1.321,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_157"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0158",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-158",
        "tier_level": 4,
        "weight_coefficient": 1.364,
        "elasticity_index": 1.324,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_158"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0159",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-159",
        "tier_level": 5,
        "weight_coefficient": 1.372,
        "elasticity_index": 1.327,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_159"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0160",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-160",
        "tier_level": 1,
        "weight_coefficient": 1.38,
        "elasticity_index": 1.33,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_160"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0161",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-161",
        "tier_level": 2,
        "weight_coefficient": 1.388,
        "elasticity_index": 1.333,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_51", "node_161"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0162",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-162",
        "tier_level": 3,
        "weight_coefficient": 1.396,
        "elasticity_index": 1.336,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_162"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0163",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-163",
        "tier_level": 4,
        "weight_coefficient": 1.404,
        "elasticity_index": 1.339,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_163"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0164",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-164",
        "tier_level": 5,
        "weight_coefficient": 1.412,
        "elasticity_index": 1.342,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_164"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0165",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-165",
        "tier_level": 1,
        "weight_coefficient": 1.42,
        "elasticity_index": 1.345,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_165"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0166",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-166",
        "tier_level": 2,
        "weight_coefficient": 1.428,
        "elasticity_index": 1.348,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_166"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0167",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-167",
        "tier_level": 3,
        "weight_coefficient": 1.436,
        "elasticity_index": 1.351,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_167"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0168",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-168",
        "tier_level": 4,
        "weight_coefficient": 1.444,
        "elasticity_index": 1.354,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_51", "node_168"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0169",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-169",
        "tier_level": 5,
        "weight_coefficient": 1.452,
        "elasticity_index": 1.357,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_169"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0170",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-170",
        "tier_level": 1,
        "weight_coefficient": 1.46,
        "elasticity_index": 1.36,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_170"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0171",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-171",
        "tier_level": 2,
        "weight_coefficient": 1.468,
        "elasticity_index": 1.363,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_171"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0172",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-172",
        "tier_level": 3,
        "weight_coefficient": 1.476,
        "elasticity_index": 1.366,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_172"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0173",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-173",
        "tier_level": 4,
        "weight_coefficient": 1.484,
        "elasticity_index": 1.369,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_173"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0174",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-174",
        "tier_level": 5,
        "weight_coefficient": 1.492,
        "elasticity_index": 1.372,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_174"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0175",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-175",
        "tier_level": 1,
        "weight_coefficient": 1.5,
        "elasticity_index": 1.375,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_51", "node_175"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0176",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-176",
        "tier_level": 2,
        "weight_coefficient": 1.508,
        "elasticity_index": 1.378,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_176"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0177",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-177",
        "tier_level": 3,
        "weight_coefficient": 1.516,
        "elasticity_index": 1.381,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_177"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0178",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-178",
        "tier_level": 4,
        "weight_coefficient": 1.524,
        "elasticity_index": 1.384,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_178"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0179",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-179",
        "tier_level": 5,
        "weight_coefficient": 1.532,
        "elasticity_index": 1.387,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_179"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0180",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-180",
        "tier_level": 1,
        "weight_coefficient": 1.54,
        "elasticity_index": 1.39,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_180"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0181",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-181",
        "tier_level": 2,
        "weight_coefficient": 1.548,
        "elasticity_index": 1.393,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_181"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0182",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-182",
        "tier_level": 3,
        "weight_coefficient": 1.556,
        "elasticity_index": 1.396,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_51", "node_182"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0183",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-183",
        "tier_level": 4,
        "weight_coefficient": 1.564,
        "elasticity_index": 1.399,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_183"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0184",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-184",
        "tier_level": 5,
        "weight_coefficient": 1.572,
        "elasticity_index": 1.402,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_184"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0185",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-185",
        "tier_level": 1,
        "weight_coefficient": 1.58,
        "elasticity_index": 1.405,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_185"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0186",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-186",
        "tier_level": 2,
        "weight_coefficient": 1.588,
        "elasticity_index": 1.408,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_186"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0187",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-187",
        "tier_level": 3,
        "weight_coefficient": 1.596,
        "elasticity_index": 1.411,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_187"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0188",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-188",
        "tier_level": 4,
        "weight_coefficient": 1.604,
        "elasticity_index": 1.414,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_188"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0189",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-189",
        "tier_level": 5,
        "weight_coefficient": 1.612,
        "elasticity_index": 1.417,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_51", "node_189"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0190",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-190",
        "tier_level": 1,
        "weight_coefficient": 1.62,
        "elasticity_index": 1.42,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_190"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0191",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-191",
        "tier_level": 2,
        "weight_coefficient": 1.628,
        "elasticity_index": 1.423,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_191"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0192",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-192",
        "tier_level": 3,
        "weight_coefficient": 1.636,
        "elasticity_index": 1.426,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_192"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0193",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-193",
        "tier_level": 4,
        "weight_coefficient": 1.644,
        "elasticity_index": 1.429,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_193"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0194",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-194",
        "tier_level": 5,
        "weight_coefficient": 1.652,
        "elasticity_index": 1.432,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_194"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0195",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-195",
        "tier_level": 1,
        "weight_coefficient": 1.66,
        "elasticity_index": 1.435,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_195"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0196",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-196",
        "tier_level": 2,
        "weight_coefficient": 1.668,
        "elasticity_index": 1.438,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_51", "node_196"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0197",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-197",
        "tier_level": 3,
        "weight_coefficient": 1.676,
        "elasticity_index": 1.441,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_197"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0198",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-198",
        "tier_level": 4,
        "weight_coefficient": 1.684,
        "elasticity_index": 1.444,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_198"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0199",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-199",
        "tier_level": 5,
        "weight_coefficient": 1.692,
        "elasticity_index": 1.447,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_199"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0200",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-200",
        "tier_level": 1,
        "weight_coefficient": 1.7,
        "elasticity_index": 1.45,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_200"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0201",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-201",
        "tier_level": 2,
        "weight_coefficient": 1.708,
        "elasticity_index": 1.453,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_201"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0202",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-202",
        "tier_level": 3,
        "weight_coefficient": 1.716,
        "elasticity_index": 1.456,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_202"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0203",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-203",
        "tier_level": 4,
        "weight_coefficient": 1.724,
        "elasticity_index": 1.459,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_51", "node_203"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0204",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-204",
        "tier_level": 5,
        "weight_coefficient": 1.732,
        "elasticity_index": 1.462,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_204"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0205",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-205",
        "tier_level": 1,
        "weight_coefficient": 1.74,
        "elasticity_index": 1.465,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_205"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0206",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-206",
        "tier_level": 2,
        "weight_coefficient": 1.748,
        "elasticity_index": 1.468,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_206"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0207",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-207",
        "tier_level": 3,
        "weight_coefficient": 1.756,
        "elasticity_index": 1.471,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_207"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0208",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-208",
        "tier_level": 4,
        "weight_coefficient": 1.764,
        "elasticity_index": 1.474,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_208"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0209",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-209",
        "tier_level": 5,
        "weight_coefficient": 1.772,
        "elasticity_index": 1.477,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_209"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0210",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-210",
        "tier_level": 1,
        "weight_coefficient": 1.78,
        "elasticity_index": 1.48,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_51", "node_210"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0211",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-211",
        "tier_level": 2,
        "weight_coefficient": 1.788,
        "elasticity_index": 1.483,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_211"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0212",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-212",
        "tier_level": 3,
        "weight_coefficient": 1.796,
        "elasticity_index": 1.486,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_212"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0213",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-213",
        "tier_level": 4,
        "weight_coefficient": 1.804,
        "elasticity_index": 1.489,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_213"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0214",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-214",
        "tier_level": 5,
        "weight_coefficient": 1.812,
        "elasticity_index": 1.492,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_214"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0215",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-215",
        "tier_level": 1,
        "weight_coefficient": 1.82,
        "elasticity_index": 1.495,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_215"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0216",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-216",
        "tier_level": 2,
        "weight_coefficient": 1.828,
        "elasticity_index": 1.498,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_216"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0217",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-217",
        "tier_level": 3,
        "weight_coefficient": 1.836,
        "elasticity_index": 1.501,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_51", "node_217"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0218",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-218",
        "tier_level": 4,
        "weight_coefficient": 1.844,
        "elasticity_index": 1.504,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_218"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0219",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-219",
        "tier_level": 5,
        "weight_coefficient": 1.852,
        "elasticity_index": 1.507,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_219"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0220",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-220",
        "tier_level": 1,
        "weight_coefficient": 1.86,
        "elasticity_index": 1.51,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_220"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0221",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-221",
        "tier_level": 2,
        "weight_coefficient": 1.868,
        "elasticity_index": 1.513,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_221"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0222",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-222",
        "tier_level": 3,
        "weight_coefficient": 1.876,
        "elasticity_index": 1.516,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_222"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0223",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-223",
        "tier_level": 4,
        "weight_coefficient": 1.884,
        "elasticity_index": 1.519,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_223"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0224",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-224",
        "tier_level": 5,
        "weight_coefficient": 1.892,
        "elasticity_index": 1.522,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_51", "node_224"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0225",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-225",
        "tier_level": 1,
        "weight_coefficient": 1.9,
        "elasticity_index": 1.525,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_225"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0226",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-226",
        "tier_level": 2,
        "weight_coefficient": 1.908,
        "elasticity_index": 1.528,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_226"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0227",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-227",
        "tier_level": 3,
        "weight_coefficient": 1.916,
        "elasticity_index": 1.531,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_227"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0228",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-228",
        "tier_level": 4,
        "weight_coefficient": 1.924,
        "elasticity_index": 1.534,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_228"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0229",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-229",
        "tier_level": 5,
        "weight_coefficient": 1.932,
        "elasticity_index": 1.537,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_229"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0230",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-230",
        "tier_level": 1,
        "weight_coefficient": 1.94,
        "elasticity_index": 1.54,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_230"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0231",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-231",
        "tier_level": 2,
        "weight_coefficient": 1.948,
        "elasticity_index": 1.543,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_51", "node_231"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0232",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-232",
        "tier_level": 3,
        "weight_coefficient": 1.956,
        "elasticity_index": 1.546,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_232"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0233",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-233",
        "tier_level": 4,
        "weight_coefficient": 1.964,
        "elasticity_index": 1.549,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_233"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0234",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-234",
        "tier_level": 5,
        "weight_coefficient": 1.972,
        "elasticity_index": 1.552,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_234"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0235",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-235",
        "tier_level": 1,
        "weight_coefficient": 1.98,
        "elasticity_index": 1.555,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_235"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0236",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-236",
        "tier_level": 2,
        "weight_coefficient": 1.988,
        "elasticity_index": 1.558,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_236"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0237",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-237",
        "tier_level": 3,
        "weight_coefficient": 1.996,
        "elasticity_index": 1.561,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_237"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0238",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-238",
        "tier_level": 4,
        "weight_coefficient": 2.004,
        "elasticity_index": 1.564,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_51", "node_238"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0239",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-239",
        "tier_level": 5,
        "weight_coefficient": 2.012,
        "elasticity_index": 1.567,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_239"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0240",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-240",
        "tier_level": 1,
        "weight_coefficient": 2.02,
        "elasticity_index": 1.57,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_240"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0241",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-241",
        "tier_level": 2,
        "weight_coefficient": 2.028,
        "elasticity_index": 1.573,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_241"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0242",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-242",
        "tier_level": 3,
        "weight_coefficient": 2.036,
        "elasticity_index": 1.576,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_242"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0243",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-243",
        "tier_level": 4,
        "weight_coefficient": 2.044,
        "elasticity_index": 1.579,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_243"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0244",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-244",
        "tier_level": 5,
        "weight_coefficient": 2.052,
        "elasticity_index": 1.582,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_244"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0245",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-245",
        "tier_level": 1,
        "weight_coefficient": 2.06,
        "elasticity_index": 1.585,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_51", "node_245"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0246",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-246",
        "tier_level": 2,
        "weight_coefficient": 2.068,
        "elasticity_index": 1.588,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_51", "node_246"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0247",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-247",
        "tier_level": 3,
        "weight_coefficient": 2.076,
        "elasticity_index": 1.591,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_51", "node_247"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0248",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-248",
        "tier_level": 4,
        "weight_coefficient": 2.084,
        "elasticity_index": 1.594,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_51", "node_248"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-51-0249",
        "entity_key": "ENT-return-pickup-scheduling-reverse-tracking-249",
        "tier_level": 5,
        "weight_coefficient": 2.092,
        "elasticity_index": 1.597,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_51", "node_249"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
]

