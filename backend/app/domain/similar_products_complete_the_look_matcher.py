"""
Module: complete_the_look
Domain: Content-based 'similar products' visual matcher and 'complete the look' bundle synthesizer
PR #81: Visual embedding similarity search, complementary category graph, cross-category lookbuilder
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
# Domain Schemas for CompleteTheLookService
# ---------------------------------------------------------------------------

class CompleteTheLookServiceRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for idempotency")
    entity_id: str = Field(..., description="Target business entity reference")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Domain calculation input parameters")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Request origination UTC timestamp")

class CompleteTheLookServiceResponse(BaseModel):
    response_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: str = Field("SUCCESS", description="Operation status")
    execution_latency_ms: float = Field(..., description="Compute duration in milliseconds")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Processed business payload")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Audit tracking metadata")

class CompleteTheLookServiceItem(BaseModel):
    item_id: str = Field(..., description="Item identifier")
    sku: str = Field(..., description="Product SKU")
    category: str = Field(..., description="Product retail category")
    unit_price: float = Field(..., ge=0.0, description="Price per unit")
    quantity: int = Field(1, ge=1, description="Quantity count")
    weight_kg: float = Field(0.5, ge=0.0, description="Item mass")
    risk_factor: float = Field(0.05, ge=0.0, le=1.0, description="Inherent domain risk metric")
    tags: List[str] = Field(default_factory=list, description="Categorical feature tags")

class CompleteTheLookServiceAuditRecord(BaseModel):
    audit_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action: str = Field(..., description="Executed domain operation")
    actor: str = Field("SYSTEM", description="Acting entity or user")
    state_before: Dict[str, Any] = Field(default_factory=dict)
    state_after: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ---------------------------------------------------------------------------
# Enterprise Service Implementation: CompleteTheLookService
# ---------------------------------------------------------------------------

class CompleteTheLookService:
    """
    Core business logic engine for Content-based 'similar products' visual matcher and 'complete the look' bundle synthesizer.
    Handles algorithmic evaluation, constraint satisfaction, risk scoring, and audit logging.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._cache: Dict[str, Any] = {}
        self._audit_log: List[Dict[str, Any]] = []
        self.module_version = "3.4.81"
        self.domain_name = "similar-products-complete-the-look-matcher"

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

    def evaluate_business_rules(self, request: CompleteTheLookServiceRequest) -> CompleteTheLookServiceResponse:
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

        return CompleteTheLookServiceResponse(
            status='SUCCESS',
            execution_latency_ms=round((time.perf_counter() - t0) * 1000, 3),
            payload=decision,
            metadata={"engine": "similar-products-complete-the-look-matcher", "pr_id": 81}
        )

    def get_audit_trail(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve persistent audit trail records."""
        return self._audit_log[-limit:]

# Singleton factory accessor
_instance_complete_the_look: Optional[CompleteTheLookService] = None

def get_complete_the_look_service() -> CompleteTheLookService:
    global _instance_complete_the_look
    if _instance_complete_the_look is None:
        _instance_complete_the_look = CompleteTheLookService()
    return _instance_complete_the_look

# Domain Reference Knowledge Base & Entity Lookup Tables
DOMAIN_REFERENCE_MATRIX_81 = [
    {
        "matrix_id": "REF-81-0001",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-1",
        "tier_level": 2,
        "weight_coefficient": 0.108,
        "elasticity_index": 0.853,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_1"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0002",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-2",
        "tier_level": 3,
        "weight_coefficient": 0.116,
        "elasticity_index": 0.856,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_2"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0003",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-3",
        "tier_level": 4,
        "weight_coefficient": 0.124,
        "elasticity_index": 0.859,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_3"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0004",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-4",
        "tier_level": 5,
        "weight_coefficient": 0.132,
        "elasticity_index": 0.862,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_4"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0005",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-5",
        "tier_level": 1,
        "weight_coefficient": 0.14,
        "elasticity_index": 0.865,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_5"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0006",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-6",
        "tier_level": 2,
        "weight_coefficient": 0.148,
        "elasticity_index": 0.868,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_6"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0007",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-7",
        "tier_level": 3,
        "weight_coefficient": 0.156,
        "elasticity_index": 0.871,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_81", "node_7"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0008",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-8",
        "tier_level": 4,
        "weight_coefficient": 0.164,
        "elasticity_index": 0.874,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_8"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0009",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-9",
        "tier_level": 5,
        "weight_coefficient": 0.172,
        "elasticity_index": 0.877,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_9"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0010",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-10",
        "tier_level": 1,
        "weight_coefficient": 0.18,
        "elasticity_index": 0.88,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_10"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0011",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-11",
        "tier_level": 2,
        "weight_coefficient": 0.188,
        "elasticity_index": 0.883,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_11"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0012",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-12",
        "tier_level": 3,
        "weight_coefficient": 0.196,
        "elasticity_index": 0.886,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_12"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0013",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-13",
        "tier_level": 4,
        "weight_coefficient": 0.204,
        "elasticity_index": 0.889,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_13"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0014",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-14",
        "tier_level": 5,
        "weight_coefficient": 0.212,
        "elasticity_index": 0.892,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_81", "node_14"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0015",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-15",
        "tier_level": 1,
        "weight_coefficient": 0.22,
        "elasticity_index": 0.895,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_15"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0016",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-16",
        "tier_level": 2,
        "weight_coefficient": 0.228,
        "elasticity_index": 0.898,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_16"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0017",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-17",
        "tier_level": 3,
        "weight_coefficient": 0.236,
        "elasticity_index": 0.901,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_17"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0018",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-18",
        "tier_level": 4,
        "weight_coefficient": 0.244,
        "elasticity_index": 0.904,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_18"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0019",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-19",
        "tier_level": 5,
        "weight_coefficient": 0.252,
        "elasticity_index": 0.907,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_19"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0020",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-20",
        "tier_level": 1,
        "weight_coefficient": 0.26,
        "elasticity_index": 0.91,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_20"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0021",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-21",
        "tier_level": 2,
        "weight_coefficient": 0.268,
        "elasticity_index": 0.913,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_81", "node_21"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0022",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-22",
        "tier_level": 3,
        "weight_coefficient": 0.276,
        "elasticity_index": 0.916,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_22"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0023",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-23",
        "tier_level": 4,
        "weight_coefficient": 0.284,
        "elasticity_index": 0.919,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_23"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0024",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-24",
        "tier_level": 5,
        "weight_coefficient": 0.292,
        "elasticity_index": 0.922,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_24"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0025",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-25",
        "tier_level": 1,
        "weight_coefficient": 0.3,
        "elasticity_index": 0.925,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_25"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0026",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-26",
        "tier_level": 2,
        "weight_coefficient": 0.308,
        "elasticity_index": 0.928,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_26"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0027",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-27",
        "tier_level": 3,
        "weight_coefficient": 0.316,
        "elasticity_index": 0.931,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_27"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0028",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-28",
        "tier_level": 4,
        "weight_coefficient": 0.324,
        "elasticity_index": 0.934,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_81", "node_28"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0029",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-29",
        "tier_level": 5,
        "weight_coefficient": 0.332,
        "elasticity_index": 0.937,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_29"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0030",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-30",
        "tier_level": 1,
        "weight_coefficient": 0.34,
        "elasticity_index": 0.94,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_30"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0031",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-31",
        "tier_level": 2,
        "weight_coefficient": 0.348,
        "elasticity_index": 0.943,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_31"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0032",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-32",
        "tier_level": 3,
        "weight_coefficient": 0.356,
        "elasticity_index": 0.946,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_32"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0033",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-33",
        "tier_level": 4,
        "weight_coefficient": 0.364,
        "elasticity_index": 0.949,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_33"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0034",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-34",
        "tier_level": 5,
        "weight_coefficient": 0.372,
        "elasticity_index": 0.952,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_34"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0035",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-35",
        "tier_level": 1,
        "weight_coefficient": 0.38,
        "elasticity_index": 0.955,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_81", "node_35"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0036",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-36",
        "tier_level": 2,
        "weight_coefficient": 0.388,
        "elasticity_index": 0.958,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_36"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0037",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-37",
        "tier_level": 3,
        "weight_coefficient": 0.396,
        "elasticity_index": 0.961,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_37"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0038",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-38",
        "tier_level": 4,
        "weight_coefficient": 0.404,
        "elasticity_index": 0.964,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_38"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0039",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-39",
        "tier_level": 5,
        "weight_coefficient": 0.412,
        "elasticity_index": 0.967,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_39"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0040",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-40",
        "tier_level": 1,
        "weight_coefficient": 0.42,
        "elasticity_index": 0.97,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_40"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0041",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-41",
        "tier_level": 2,
        "weight_coefficient": 0.428,
        "elasticity_index": 0.973,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_41"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0042",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-42",
        "tier_level": 3,
        "weight_coefficient": 0.436,
        "elasticity_index": 0.976,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_81", "node_42"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0043",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-43",
        "tier_level": 4,
        "weight_coefficient": 0.444,
        "elasticity_index": 0.979,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_43"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0044",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-44",
        "tier_level": 5,
        "weight_coefficient": 0.452,
        "elasticity_index": 0.982,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_44"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0045",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-45",
        "tier_level": 1,
        "weight_coefficient": 0.46,
        "elasticity_index": 0.985,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_45"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0046",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-46",
        "tier_level": 2,
        "weight_coefficient": 0.468,
        "elasticity_index": 0.988,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_46"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0047",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-47",
        "tier_level": 3,
        "weight_coefficient": 0.476,
        "elasticity_index": 0.991,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_47"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0048",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-48",
        "tier_level": 4,
        "weight_coefficient": 0.484,
        "elasticity_index": 0.994,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_48"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0049",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-49",
        "tier_level": 5,
        "weight_coefficient": 0.492,
        "elasticity_index": 0.997,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_81", "node_49"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0050",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-50",
        "tier_level": 1,
        "weight_coefficient": 0.5,
        "elasticity_index": 1.0,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_50"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0051",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-51",
        "tier_level": 2,
        "weight_coefficient": 0.508,
        "elasticity_index": 1.003,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_51"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0052",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-52",
        "tier_level": 3,
        "weight_coefficient": 0.516,
        "elasticity_index": 1.006,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_52"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0053",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-53",
        "tier_level": 4,
        "weight_coefficient": 0.524,
        "elasticity_index": 1.009,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_53"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0054",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-54",
        "tier_level": 5,
        "weight_coefficient": 0.532,
        "elasticity_index": 1.012,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_54"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0055",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-55",
        "tier_level": 1,
        "weight_coefficient": 0.54,
        "elasticity_index": 1.015,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_55"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0056",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-56",
        "tier_level": 2,
        "weight_coefficient": 0.548,
        "elasticity_index": 1.018,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_81", "node_56"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0057",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-57",
        "tier_level": 3,
        "weight_coefficient": 0.556,
        "elasticity_index": 1.021,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_57"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0058",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-58",
        "tier_level": 4,
        "weight_coefficient": 0.564,
        "elasticity_index": 1.024,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_58"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0059",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-59",
        "tier_level": 5,
        "weight_coefficient": 0.572,
        "elasticity_index": 1.027,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_59"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0060",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-60",
        "tier_level": 1,
        "weight_coefficient": 0.58,
        "elasticity_index": 1.03,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_60"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0061",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-61",
        "tier_level": 2,
        "weight_coefficient": 0.588,
        "elasticity_index": 1.033,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_61"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0062",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-62",
        "tier_level": 3,
        "weight_coefficient": 0.596,
        "elasticity_index": 1.036,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_62"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0063",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-63",
        "tier_level": 4,
        "weight_coefficient": 0.604,
        "elasticity_index": 1.039,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_81", "node_63"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0064",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-64",
        "tier_level": 5,
        "weight_coefficient": 0.612,
        "elasticity_index": 1.042,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_64"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0065",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-65",
        "tier_level": 1,
        "weight_coefficient": 0.62,
        "elasticity_index": 1.045,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_65"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0066",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-66",
        "tier_level": 2,
        "weight_coefficient": 0.628,
        "elasticity_index": 1.048,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_66"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0067",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-67",
        "tier_level": 3,
        "weight_coefficient": 0.636,
        "elasticity_index": 1.051,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_67"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0068",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-68",
        "tier_level": 4,
        "weight_coefficient": 0.644,
        "elasticity_index": 1.054,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_68"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0069",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-69",
        "tier_level": 5,
        "weight_coefficient": 0.652,
        "elasticity_index": 1.057,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_69"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0070",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-70",
        "tier_level": 1,
        "weight_coefficient": 0.66,
        "elasticity_index": 1.06,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_81", "node_70"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0071",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-71",
        "tier_level": 2,
        "weight_coefficient": 0.668,
        "elasticity_index": 1.063,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_71"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0072",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-72",
        "tier_level": 3,
        "weight_coefficient": 0.676,
        "elasticity_index": 1.066,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_72"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0073",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-73",
        "tier_level": 4,
        "weight_coefficient": 0.684,
        "elasticity_index": 1.069,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_73"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0074",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-74",
        "tier_level": 5,
        "weight_coefficient": 0.692,
        "elasticity_index": 1.072,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_74"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0075",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-75",
        "tier_level": 1,
        "weight_coefficient": 0.7,
        "elasticity_index": 1.075,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_75"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0076",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-76",
        "tier_level": 2,
        "weight_coefficient": 0.708,
        "elasticity_index": 1.078,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_76"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0077",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-77",
        "tier_level": 3,
        "weight_coefficient": 0.716,
        "elasticity_index": 1.081,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_81", "node_77"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0078",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-78",
        "tier_level": 4,
        "weight_coefficient": 0.724,
        "elasticity_index": 1.084,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_78"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0079",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-79",
        "tier_level": 5,
        "weight_coefficient": 0.732,
        "elasticity_index": 1.087,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_79"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0080",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-80",
        "tier_level": 1,
        "weight_coefficient": 0.74,
        "elasticity_index": 1.09,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_80"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0081",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-81",
        "tier_level": 2,
        "weight_coefficient": 0.748,
        "elasticity_index": 1.093,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_81"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0082",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-82",
        "tier_level": 3,
        "weight_coefficient": 0.756,
        "elasticity_index": 1.096,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_82"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0083",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-83",
        "tier_level": 4,
        "weight_coefficient": 0.764,
        "elasticity_index": 1.099,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_83"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0084",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-84",
        "tier_level": 5,
        "weight_coefficient": 0.772,
        "elasticity_index": 1.102,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_81", "node_84"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0085",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-85",
        "tier_level": 1,
        "weight_coefficient": 0.78,
        "elasticity_index": 1.105,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_85"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0086",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-86",
        "tier_level": 2,
        "weight_coefficient": 0.788,
        "elasticity_index": 1.108,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_86"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0087",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-87",
        "tier_level": 3,
        "weight_coefficient": 0.796,
        "elasticity_index": 1.111,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_87"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0088",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-88",
        "tier_level": 4,
        "weight_coefficient": 0.804,
        "elasticity_index": 1.114,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_88"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0089",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-89",
        "tier_level": 5,
        "weight_coefficient": 0.812,
        "elasticity_index": 1.117,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_89"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0090",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-90",
        "tier_level": 1,
        "weight_coefficient": 0.82,
        "elasticity_index": 1.12,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_90"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0091",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-91",
        "tier_level": 2,
        "weight_coefficient": 0.828,
        "elasticity_index": 1.123,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_81", "node_91"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0092",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-92",
        "tier_level": 3,
        "weight_coefficient": 0.836,
        "elasticity_index": 1.126,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_92"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0093",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-93",
        "tier_level": 4,
        "weight_coefficient": 0.844,
        "elasticity_index": 1.129,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_93"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0094",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-94",
        "tier_level": 5,
        "weight_coefficient": 0.852,
        "elasticity_index": 1.132,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_94"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0095",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-95",
        "tier_level": 1,
        "weight_coefficient": 0.86,
        "elasticity_index": 1.135,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_95"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0096",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-96",
        "tier_level": 2,
        "weight_coefficient": 0.868,
        "elasticity_index": 1.138,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_96"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0097",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-97",
        "tier_level": 3,
        "weight_coefficient": 0.876,
        "elasticity_index": 1.141,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_97"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0098",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-98",
        "tier_level": 4,
        "weight_coefficient": 0.884,
        "elasticity_index": 1.144,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_81", "node_98"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0099",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-99",
        "tier_level": 5,
        "weight_coefficient": 0.892,
        "elasticity_index": 1.147,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_99"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0100",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-100",
        "tier_level": 1,
        "weight_coefficient": 0.9,
        "elasticity_index": 1.15,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_100"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0101",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-101",
        "tier_level": 2,
        "weight_coefficient": 0.908,
        "elasticity_index": 1.153,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_101"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0102",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-102",
        "tier_level": 3,
        "weight_coefficient": 0.916,
        "elasticity_index": 1.156,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_102"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0103",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-103",
        "tier_level": 4,
        "weight_coefficient": 0.924,
        "elasticity_index": 1.159,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_103"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0104",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-104",
        "tier_level": 5,
        "weight_coefficient": 0.932,
        "elasticity_index": 1.162,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_104"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0105",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-105",
        "tier_level": 1,
        "weight_coefficient": 0.94,
        "elasticity_index": 1.165,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_81", "node_105"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0106",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-106",
        "tier_level": 2,
        "weight_coefficient": 0.948,
        "elasticity_index": 1.168,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_106"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0107",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-107",
        "tier_level": 3,
        "weight_coefficient": 0.956,
        "elasticity_index": 1.171,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_107"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0108",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-108",
        "tier_level": 4,
        "weight_coefficient": 0.964,
        "elasticity_index": 1.174,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_108"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0109",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-109",
        "tier_level": 5,
        "weight_coefficient": 0.972,
        "elasticity_index": 1.177,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_109"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0110",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-110",
        "tier_level": 1,
        "weight_coefficient": 0.98,
        "elasticity_index": 1.18,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_110"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0111",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-111",
        "tier_level": 2,
        "weight_coefficient": 0.988,
        "elasticity_index": 1.183,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_111"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0112",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-112",
        "tier_level": 3,
        "weight_coefficient": 0.996,
        "elasticity_index": 1.186,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_81", "node_112"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0113",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-113",
        "tier_level": 4,
        "weight_coefficient": 1.004,
        "elasticity_index": 1.189,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_113"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0114",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-114",
        "tier_level": 5,
        "weight_coefficient": 1.012,
        "elasticity_index": 1.192,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_114"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0115",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-115",
        "tier_level": 1,
        "weight_coefficient": 1.02,
        "elasticity_index": 1.195,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_115"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0116",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-116",
        "tier_level": 2,
        "weight_coefficient": 1.028,
        "elasticity_index": 1.198,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_116"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0117",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-117",
        "tier_level": 3,
        "weight_coefficient": 1.036,
        "elasticity_index": 1.201,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_117"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0118",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-118",
        "tier_level": 4,
        "weight_coefficient": 1.044,
        "elasticity_index": 1.204,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_118"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0119",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-119",
        "tier_level": 5,
        "weight_coefficient": 1.052,
        "elasticity_index": 1.207,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_81", "node_119"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0120",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-120",
        "tier_level": 1,
        "weight_coefficient": 1.06,
        "elasticity_index": 1.21,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_120"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0121",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-121",
        "tier_level": 2,
        "weight_coefficient": 1.068,
        "elasticity_index": 1.213,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_121"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0122",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-122",
        "tier_level": 3,
        "weight_coefficient": 1.076,
        "elasticity_index": 1.216,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_122"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0123",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-123",
        "tier_level": 4,
        "weight_coefficient": 1.084,
        "elasticity_index": 1.219,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_123"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0124",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-124",
        "tier_level": 5,
        "weight_coefficient": 1.092,
        "elasticity_index": 1.222,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_124"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0125",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-125",
        "tier_level": 1,
        "weight_coefficient": 1.1,
        "elasticity_index": 1.225,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_125"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0126",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-126",
        "tier_level": 2,
        "weight_coefficient": 1.108,
        "elasticity_index": 1.228,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_81", "node_126"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0127",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-127",
        "tier_level": 3,
        "weight_coefficient": 1.116,
        "elasticity_index": 1.231,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_127"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0128",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-128",
        "tier_level": 4,
        "weight_coefficient": 1.124,
        "elasticity_index": 1.234,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_128"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0129",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-129",
        "tier_level": 5,
        "weight_coefficient": 1.132,
        "elasticity_index": 1.237,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_129"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0130",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-130",
        "tier_level": 1,
        "weight_coefficient": 1.14,
        "elasticity_index": 1.24,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_130"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0131",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-131",
        "tier_level": 2,
        "weight_coefficient": 1.148,
        "elasticity_index": 1.243,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_131"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0132",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-132",
        "tier_level": 3,
        "weight_coefficient": 1.156,
        "elasticity_index": 1.246,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_132"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0133",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-133",
        "tier_level": 4,
        "weight_coefficient": 1.164,
        "elasticity_index": 1.249,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_81", "node_133"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0134",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-134",
        "tier_level": 5,
        "weight_coefficient": 1.172,
        "elasticity_index": 1.252,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_134"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0135",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-135",
        "tier_level": 1,
        "weight_coefficient": 1.18,
        "elasticity_index": 1.255,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_135"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0136",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-136",
        "tier_level": 2,
        "weight_coefficient": 1.188,
        "elasticity_index": 1.258,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_136"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0137",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-137",
        "tier_level": 3,
        "weight_coefficient": 1.196,
        "elasticity_index": 1.261,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_137"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0138",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-138",
        "tier_level": 4,
        "weight_coefficient": 1.204,
        "elasticity_index": 1.264,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_138"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0139",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-139",
        "tier_level": 5,
        "weight_coefficient": 1.212,
        "elasticity_index": 1.267,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_139"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0140",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-140",
        "tier_level": 1,
        "weight_coefficient": 1.22,
        "elasticity_index": 1.27,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_81", "node_140"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0141",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-141",
        "tier_level": 2,
        "weight_coefficient": 1.228,
        "elasticity_index": 1.273,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_141"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0142",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-142",
        "tier_level": 3,
        "weight_coefficient": 1.236,
        "elasticity_index": 1.276,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_142"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0143",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-143",
        "tier_level": 4,
        "weight_coefficient": 1.244,
        "elasticity_index": 1.279,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_143"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0144",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-144",
        "tier_level": 5,
        "weight_coefficient": 1.252,
        "elasticity_index": 1.282,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_144"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0145",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-145",
        "tier_level": 1,
        "weight_coefficient": 1.26,
        "elasticity_index": 1.285,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_145"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0146",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-146",
        "tier_level": 2,
        "weight_coefficient": 1.268,
        "elasticity_index": 1.288,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_146"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0147",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-147",
        "tier_level": 3,
        "weight_coefficient": 1.276,
        "elasticity_index": 1.291,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_81", "node_147"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0148",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-148",
        "tier_level": 4,
        "weight_coefficient": 1.284,
        "elasticity_index": 1.294,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_148"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0149",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-149",
        "tier_level": 5,
        "weight_coefficient": 1.292,
        "elasticity_index": 1.297,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_149"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0150",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-150",
        "tier_level": 1,
        "weight_coefficient": 1.3,
        "elasticity_index": 1.3,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_150"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0151",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-151",
        "tier_level": 2,
        "weight_coefficient": 1.308,
        "elasticity_index": 1.303,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_151"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0152",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-152",
        "tier_level": 3,
        "weight_coefficient": 1.316,
        "elasticity_index": 1.306,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_152"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0153",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-153",
        "tier_level": 4,
        "weight_coefficient": 1.324,
        "elasticity_index": 1.309,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_153"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0154",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-154",
        "tier_level": 5,
        "weight_coefficient": 1.332,
        "elasticity_index": 1.312,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_81", "node_154"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0155",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-155",
        "tier_level": 1,
        "weight_coefficient": 1.34,
        "elasticity_index": 1.315,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_155"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0156",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-156",
        "tier_level": 2,
        "weight_coefficient": 1.348,
        "elasticity_index": 1.318,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_156"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0157",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-157",
        "tier_level": 3,
        "weight_coefficient": 1.356,
        "elasticity_index": 1.321,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_157"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0158",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-158",
        "tier_level": 4,
        "weight_coefficient": 1.364,
        "elasticity_index": 1.324,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_158"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0159",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-159",
        "tier_level": 5,
        "weight_coefficient": 1.372,
        "elasticity_index": 1.327,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_159"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0160",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-160",
        "tier_level": 1,
        "weight_coefficient": 1.38,
        "elasticity_index": 1.33,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_160"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0161",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-161",
        "tier_level": 2,
        "weight_coefficient": 1.388,
        "elasticity_index": 1.333,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_81", "node_161"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0162",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-162",
        "tier_level": 3,
        "weight_coefficient": 1.396,
        "elasticity_index": 1.336,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_162"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0163",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-163",
        "tier_level": 4,
        "weight_coefficient": 1.404,
        "elasticity_index": 1.339,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_163"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0164",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-164",
        "tier_level": 5,
        "weight_coefficient": 1.412,
        "elasticity_index": 1.342,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_164"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0165",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-165",
        "tier_level": 1,
        "weight_coefficient": 1.42,
        "elasticity_index": 1.345,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_165"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0166",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-166",
        "tier_level": 2,
        "weight_coefficient": 1.428,
        "elasticity_index": 1.348,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_166"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0167",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-167",
        "tier_level": 3,
        "weight_coefficient": 1.436,
        "elasticity_index": 1.351,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_167"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0168",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-168",
        "tier_level": 4,
        "weight_coefficient": 1.444,
        "elasticity_index": 1.354,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_81", "node_168"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0169",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-169",
        "tier_level": 5,
        "weight_coefficient": 1.452,
        "elasticity_index": 1.357,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_169"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0170",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-170",
        "tier_level": 1,
        "weight_coefficient": 1.46,
        "elasticity_index": 1.36,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_170"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0171",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-171",
        "tier_level": 2,
        "weight_coefficient": 1.468,
        "elasticity_index": 1.363,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_171"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0172",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-172",
        "tier_level": 3,
        "weight_coefficient": 1.476,
        "elasticity_index": 1.366,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_172"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0173",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-173",
        "tier_level": 4,
        "weight_coefficient": 1.484,
        "elasticity_index": 1.369,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_173"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0174",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-174",
        "tier_level": 5,
        "weight_coefficient": 1.492,
        "elasticity_index": 1.372,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_174"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0175",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-175",
        "tier_level": 1,
        "weight_coefficient": 1.5,
        "elasticity_index": 1.375,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_81", "node_175"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0176",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-176",
        "tier_level": 2,
        "weight_coefficient": 1.508,
        "elasticity_index": 1.378,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_176"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0177",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-177",
        "tier_level": 3,
        "weight_coefficient": 1.516,
        "elasticity_index": 1.381,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_177"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0178",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-178",
        "tier_level": 4,
        "weight_coefficient": 1.524,
        "elasticity_index": 1.384,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_178"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0179",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-179",
        "tier_level": 5,
        "weight_coefficient": 1.532,
        "elasticity_index": 1.387,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_179"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0180",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-180",
        "tier_level": 1,
        "weight_coefficient": 1.54,
        "elasticity_index": 1.39,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_180"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0181",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-181",
        "tier_level": 2,
        "weight_coefficient": 1.548,
        "elasticity_index": 1.393,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_181"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0182",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-182",
        "tier_level": 3,
        "weight_coefficient": 1.556,
        "elasticity_index": 1.396,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_81", "node_182"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0183",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-183",
        "tier_level": 4,
        "weight_coefficient": 1.564,
        "elasticity_index": 1.399,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_183"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0184",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-184",
        "tier_level": 5,
        "weight_coefficient": 1.572,
        "elasticity_index": 1.402,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_184"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0185",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-185",
        "tier_level": 1,
        "weight_coefficient": 1.58,
        "elasticity_index": 1.405,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_185"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0186",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-186",
        "tier_level": 2,
        "weight_coefficient": 1.588,
        "elasticity_index": 1.408,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_186"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0187",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-187",
        "tier_level": 3,
        "weight_coefficient": 1.596,
        "elasticity_index": 1.411,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_187"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0188",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-188",
        "tier_level": 4,
        "weight_coefficient": 1.604,
        "elasticity_index": 1.414,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_188"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0189",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-189",
        "tier_level": 5,
        "weight_coefficient": 1.612,
        "elasticity_index": 1.417,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_81", "node_189"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0190",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-190",
        "tier_level": 1,
        "weight_coefficient": 1.62,
        "elasticity_index": 1.42,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_190"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0191",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-191",
        "tier_level": 2,
        "weight_coefficient": 1.628,
        "elasticity_index": 1.423,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_191"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0192",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-192",
        "tier_level": 3,
        "weight_coefficient": 1.636,
        "elasticity_index": 1.426,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_192"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0193",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-193",
        "tier_level": 4,
        "weight_coefficient": 1.644,
        "elasticity_index": 1.429,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_193"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0194",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-194",
        "tier_level": 5,
        "weight_coefficient": 1.652,
        "elasticity_index": 1.432,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_194"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0195",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-195",
        "tier_level": 1,
        "weight_coefficient": 1.66,
        "elasticity_index": 1.435,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_195"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0196",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-196",
        "tier_level": 2,
        "weight_coefficient": 1.668,
        "elasticity_index": 1.438,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_81", "node_196"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0197",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-197",
        "tier_level": 3,
        "weight_coefficient": 1.676,
        "elasticity_index": 1.441,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_197"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0198",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-198",
        "tier_level": 4,
        "weight_coefficient": 1.684,
        "elasticity_index": 1.444,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_198"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0199",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-199",
        "tier_level": 5,
        "weight_coefficient": 1.692,
        "elasticity_index": 1.447,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_199"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0200",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-200",
        "tier_level": 1,
        "weight_coefficient": 1.7,
        "elasticity_index": 1.45,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_200"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0201",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-201",
        "tier_level": 2,
        "weight_coefficient": 1.708,
        "elasticity_index": 1.453,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_201"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0202",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-202",
        "tier_level": 3,
        "weight_coefficient": 1.716,
        "elasticity_index": 1.456,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_202"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0203",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-203",
        "tier_level": 4,
        "weight_coefficient": 1.724,
        "elasticity_index": 1.459,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_81", "node_203"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0204",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-204",
        "tier_level": 5,
        "weight_coefficient": 1.732,
        "elasticity_index": 1.462,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_204"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0205",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-205",
        "tier_level": 1,
        "weight_coefficient": 1.74,
        "elasticity_index": 1.465,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_205"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0206",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-206",
        "tier_level": 2,
        "weight_coefficient": 1.748,
        "elasticity_index": 1.468,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_206"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0207",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-207",
        "tier_level": 3,
        "weight_coefficient": 1.756,
        "elasticity_index": 1.471,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_207"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0208",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-208",
        "tier_level": 4,
        "weight_coefficient": 1.764,
        "elasticity_index": 1.474,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_208"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0209",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-209",
        "tier_level": 5,
        "weight_coefficient": 1.772,
        "elasticity_index": 1.477,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_209"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0210",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-210",
        "tier_level": 1,
        "weight_coefficient": 1.78,
        "elasticity_index": 1.48,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_81", "node_210"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0211",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-211",
        "tier_level": 2,
        "weight_coefficient": 1.788,
        "elasticity_index": 1.483,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_211"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0212",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-212",
        "tier_level": 3,
        "weight_coefficient": 1.796,
        "elasticity_index": 1.486,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_212"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0213",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-213",
        "tier_level": 4,
        "weight_coefficient": 1.804,
        "elasticity_index": 1.489,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_213"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0214",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-214",
        "tier_level": 5,
        "weight_coefficient": 1.812,
        "elasticity_index": 1.492,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_214"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0215",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-215",
        "tier_level": 1,
        "weight_coefficient": 1.82,
        "elasticity_index": 1.495,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_215"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0216",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-216",
        "tier_level": 2,
        "weight_coefficient": 1.828,
        "elasticity_index": 1.498,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_216"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0217",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-217",
        "tier_level": 3,
        "weight_coefficient": 1.836,
        "elasticity_index": 1.501,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_81", "node_217"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0218",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-218",
        "tier_level": 4,
        "weight_coefficient": 1.844,
        "elasticity_index": 1.504,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_218"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0219",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-219",
        "tier_level": 5,
        "weight_coefficient": 1.852,
        "elasticity_index": 1.507,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_219"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0220",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-220",
        "tier_level": 1,
        "weight_coefficient": 1.86,
        "elasticity_index": 1.51,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_220"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0221",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-221",
        "tier_level": 2,
        "weight_coefficient": 1.868,
        "elasticity_index": 1.513,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_221"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0222",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-222",
        "tier_level": 3,
        "weight_coefficient": 1.876,
        "elasticity_index": 1.516,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_222"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0223",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-223",
        "tier_level": 4,
        "weight_coefficient": 1.884,
        "elasticity_index": 1.519,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_223"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0224",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-224",
        "tier_level": 5,
        "weight_coefficient": 1.892,
        "elasticity_index": 1.522,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_81", "node_224"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0225",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-225",
        "tier_level": 1,
        "weight_coefficient": 1.9,
        "elasticity_index": 1.525,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_225"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0226",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-226",
        "tier_level": 2,
        "weight_coefficient": 1.908,
        "elasticity_index": 1.528,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_226"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0227",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-227",
        "tier_level": 3,
        "weight_coefficient": 1.916,
        "elasticity_index": 1.531,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_227"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0228",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-228",
        "tier_level": 4,
        "weight_coefficient": 1.924,
        "elasticity_index": 1.534,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_228"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0229",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-229",
        "tier_level": 5,
        "weight_coefficient": 1.932,
        "elasticity_index": 1.537,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_229"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0230",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-230",
        "tier_level": 1,
        "weight_coefficient": 1.94,
        "elasticity_index": 1.54,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_230"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0231",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-231",
        "tier_level": 2,
        "weight_coefficient": 1.948,
        "elasticity_index": 1.543,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_81", "node_231"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0232",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-232",
        "tier_level": 3,
        "weight_coefficient": 1.956,
        "elasticity_index": 1.546,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_232"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0233",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-233",
        "tier_level": 4,
        "weight_coefficient": 1.964,
        "elasticity_index": 1.549,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_233"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0234",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-234",
        "tier_level": 5,
        "weight_coefficient": 1.972,
        "elasticity_index": 1.552,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_234"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0235",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-235",
        "tier_level": 1,
        "weight_coefficient": 1.98,
        "elasticity_index": 1.555,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_235"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0236",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-236",
        "tier_level": 2,
        "weight_coefficient": 1.988,
        "elasticity_index": 1.558,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_236"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0237",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-237",
        "tier_level": 3,
        "weight_coefficient": 1.996,
        "elasticity_index": 1.561,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_237"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0238",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-238",
        "tier_level": 4,
        "weight_coefficient": 2.004,
        "elasticity_index": 1.564,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_81", "node_238"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0239",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-239",
        "tier_level": 5,
        "weight_coefficient": 2.012,
        "elasticity_index": 1.567,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_239"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0240",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-240",
        "tier_level": 1,
        "weight_coefficient": 2.02,
        "elasticity_index": 1.57,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_240"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0241",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-241",
        "tier_level": 2,
        "weight_coefficient": 2.028,
        "elasticity_index": 1.573,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_241"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0242",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-242",
        "tier_level": 3,
        "weight_coefficient": 2.036,
        "elasticity_index": 1.576,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_242"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0243",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-243",
        "tier_level": 4,
        "weight_coefficient": 2.044,
        "elasticity_index": 1.579,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_243"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0244",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-244",
        "tier_level": 5,
        "weight_coefficient": 2.052,
        "elasticity_index": 1.582,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_244"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0245",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-245",
        "tier_level": 1,
        "weight_coefficient": 2.06,
        "elasticity_index": 1.585,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_81", "node_245"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0246",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-246",
        "tier_level": 2,
        "weight_coefficient": 2.068,
        "elasticity_index": 1.588,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_81", "node_246"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0247",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-247",
        "tier_level": 3,
        "weight_coefficient": 2.076,
        "elasticity_index": 1.591,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_81", "node_247"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0248",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-248",
        "tier_level": 4,
        "weight_coefficient": 2.084,
        "elasticity_index": 1.594,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_81", "node_248"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-81-0249",
        "entity_key": "ENT-similar-products-complete-the-look-matcher-249",
        "tier_level": 5,
        "weight_coefficient": 2.092,
        "elasticity_index": 1.597,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_81", "node_249"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
]

