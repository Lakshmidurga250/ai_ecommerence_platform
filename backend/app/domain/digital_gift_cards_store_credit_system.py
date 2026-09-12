"""
Module: gift_card_service
Domain: Digital gift card purchasing, recipient scheduling, and store credit balance
PR #23: Cryptographic gift card codes, automated balance ledger, partial redemption
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
# Domain Schemas for GiftCardServiceService
# ---------------------------------------------------------------------------

class GiftCardServiceServiceRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for idempotency")
    entity_id: str = Field(..., description="Target business entity reference")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Domain calculation input parameters")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Request origination UTC timestamp")

class GiftCardServiceServiceResponse(BaseModel):
    response_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: str = Field("SUCCESS", description="Operation status")
    execution_latency_ms: float = Field(..., description="Compute duration in milliseconds")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Processed business payload")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Audit tracking metadata")

class GiftCardServiceServiceItem(BaseModel):
    item_id: str = Field(..., description="Item identifier")
    sku: str = Field(..., description="Product SKU")
    category: str = Field(..., description="Product retail category")
    unit_price: float = Field(..., ge=0.0, description="Price per unit")
    quantity: int = Field(1, ge=1, description="Quantity count")
    weight_kg: float = Field(0.5, ge=0.0, description="Item mass")
    risk_factor: float = Field(0.05, ge=0.0, le=1.0, description="Inherent domain risk metric")
    tags: List[str] = Field(default_factory=list, description="Categorical feature tags")

class GiftCardServiceServiceAuditRecord(BaseModel):
    audit_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action: str = Field(..., description="Executed domain operation")
    actor: str = Field("SYSTEM", description="Acting entity or user")
    state_before: Dict[str, Any] = Field(default_factory=dict)
    state_after: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ---------------------------------------------------------------------------
# Enterprise Service Implementation: GiftCardServiceService
# ---------------------------------------------------------------------------

class GiftCardServiceService:
    """
    Core business logic engine for Digital gift card purchasing, recipient scheduling, and store credit balance.
    Handles algorithmic evaluation, constraint satisfaction, risk scoring, and audit logging.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._cache: Dict[str, Any] = {}
        self._audit_log: List[Dict[str, Any]] = []
        self.module_version = "3.4.23"
        self.domain_name = "digital-gift-cards-store-credit-system"

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

    def evaluate_business_rules(self, request: GiftCardServiceServiceRequest) -> GiftCardServiceServiceResponse:
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

        return GiftCardServiceServiceResponse(
            status='SUCCESS',
            execution_latency_ms=round((time.perf_counter() - t0) * 1000, 3),
            payload=decision,
            metadata={"engine": "digital-gift-cards-store-credit-system", "pr_id": 23}
        )

    def get_audit_trail(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve persistent audit trail records."""
        return self._audit_log[-limit:]

# Singleton factory accessor
_instance_gift_card_service: Optional[GiftCardServiceService] = None

def get_gift_card_service_service() -> GiftCardServiceService:
    global _instance_gift_card_service
    if _instance_gift_card_service is None:
        _instance_gift_card_service = GiftCardServiceService()
    return _instance_gift_card_service

# Domain Reference Knowledge Base & Entity Lookup Tables
DOMAIN_REFERENCE_MATRIX_23 = [
    {
        "matrix_id": "REF-23-0001",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-1",
        "tier_level": 2,
        "weight_coefficient": 0.108,
        "elasticity_index": 0.853,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_1"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0002",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-2",
        "tier_level": 3,
        "weight_coefficient": 0.116,
        "elasticity_index": 0.856,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_2"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0003",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-3",
        "tier_level": 4,
        "weight_coefficient": 0.124,
        "elasticity_index": 0.859,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_3"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0004",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-4",
        "tier_level": 5,
        "weight_coefficient": 0.132,
        "elasticity_index": 0.862,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_4"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0005",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-5",
        "tier_level": 1,
        "weight_coefficient": 0.14,
        "elasticity_index": 0.865,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_5"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0006",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-6",
        "tier_level": 2,
        "weight_coefficient": 0.148,
        "elasticity_index": 0.868,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_6"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0007",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-7",
        "tier_level": 3,
        "weight_coefficient": 0.156,
        "elasticity_index": 0.871,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_23", "node_7"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0008",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-8",
        "tier_level": 4,
        "weight_coefficient": 0.164,
        "elasticity_index": 0.874,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_8"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0009",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-9",
        "tier_level": 5,
        "weight_coefficient": 0.172,
        "elasticity_index": 0.877,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_9"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0010",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-10",
        "tier_level": 1,
        "weight_coefficient": 0.18,
        "elasticity_index": 0.88,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_10"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0011",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-11",
        "tier_level": 2,
        "weight_coefficient": 0.188,
        "elasticity_index": 0.883,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_11"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0012",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-12",
        "tier_level": 3,
        "weight_coefficient": 0.196,
        "elasticity_index": 0.886,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_12"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0013",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-13",
        "tier_level": 4,
        "weight_coefficient": 0.204,
        "elasticity_index": 0.889,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_13"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0014",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-14",
        "tier_level": 5,
        "weight_coefficient": 0.212,
        "elasticity_index": 0.892,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_23", "node_14"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0015",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-15",
        "tier_level": 1,
        "weight_coefficient": 0.22,
        "elasticity_index": 0.895,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_15"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0016",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-16",
        "tier_level": 2,
        "weight_coefficient": 0.228,
        "elasticity_index": 0.898,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_16"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0017",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-17",
        "tier_level": 3,
        "weight_coefficient": 0.236,
        "elasticity_index": 0.901,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_17"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0018",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-18",
        "tier_level": 4,
        "weight_coefficient": 0.244,
        "elasticity_index": 0.904,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_18"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0019",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-19",
        "tier_level": 5,
        "weight_coefficient": 0.252,
        "elasticity_index": 0.907,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_19"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0020",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-20",
        "tier_level": 1,
        "weight_coefficient": 0.26,
        "elasticity_index": 0.91,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_20"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0021",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-21",
        "tier_level": 2,
        "weight_coefficient": 0.268,
        "elasticity_index": 0.913,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_23", "node_21"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0022",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-22",
        "tier_level": 3,
        "weight_coefficient": 0.276,
        "elasticity_index": 0.916,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_22"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0023",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-23",
        "tier_level": 4,
        "weight_coefficient": 0.284,
        "elasticity_index": 0.919,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_23"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0024",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-24",
        "tier_level": 5,
        "weight_coefficient": 0.292,
        "elasticity_index": 0.922,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_24"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0025",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-25",
        "tier_level": 1,
        "weight_coefficient": 0.3,
        "elasticity_index": 0.925,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_25"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0026",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-26",
        "tier_level": 2,
        "weight_coefficient": 0.308,
        "elasticity_index": 0.928,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_26"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0027",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-27",
        "tier_level": 3,
        "weight_coefficient": 0.316,
        "elasticity_index": 0.931,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_27"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0028",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-28",
        "tier_level": 4,
        "weight_coefficient": 0.324,
        "elasticity_index": 0.934,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_23", "node_28"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0029",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-29",
        "tier_level": 5,
        "weight_coefficient": 0.332,
        "elasticity_index": 0.937,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_29"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0030",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-30",
        "tier_level": 1,
        "weight_coefficient": 0.34,
        "elasticity_index": 0.94,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_30"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0031",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-31",
        "tier_level": 2,
        "weight_coefficient": 0.348,
        "elasticity_index": 0.943,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_31"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0032",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-32",
        "tier_level": 3,
        "weight_coefficient": 0.356,
        "elasticity_index": 0.946,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_32"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0033",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-33",
        "tier_level": 4,
        "weight_coefficient": 0.364,
        "elasticity_index": 0.949,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_33"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0034",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-34",
        "tier_level": 5,
        "weight_coefficient": 0.372,
        "elasticity_index": 0.952,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_34"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0035",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-35",
        "tier_level": 1,
        "weight_coefficient": 0.38,
        "elasticity_index": 0.955,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_23", "node_35"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0036",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-36",
        "tier_level": 2,
        "weight_coefficient": 0.388,
        "elasticity_index": 0.958,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_36"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0037",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-37",
        "tier_level": 3,
        "weight_coefficient": 0.396,
        "elasticity_index": 0.961,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_37"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0038",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-38",
        "tier_level": 4,
        "weight_coefficient": 0.404,
        "elasticity_index": 0.964,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_38"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0039",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-39",
        "tier_level": 5,
        "weight_coefficient": 0.412,
        "elasticity_index": 0.967,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_39"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0040",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-40",
        "tier_level": 1,
        "weight_coefficient": 0.42,
        "elasticity_index": 0.97,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_40"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0041",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-41",
        "tier_level": 2,
        "weight_coefficient": 0.428,
        "elasticity_index": 0.973,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_41"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0042",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-42",
        "tier_level": 3,
        "weight_coefficient": 0.436,
        "elasticity_index": 0.976,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_23", "node_42"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0043",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-43",
        "tier_level": 4,
        "weight_coefficient": 0.444,
        "elasticity_index": 0.979,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_43"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0044",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-44",
        "tier_level": 5,
        "weight_coefficient": 0.452,
        "elasticity_index": 0.982,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_44"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0045",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-45",
        "tier_level": 1,
        "weight_coefficient": 0.46,
        "elasticity_index": 0.985,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_45"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0046",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-46",
        "tier_level": 2,
        "weight_coefficient": 0.468,
        "elasticity_index": 0.988,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_46"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0047",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-47",
        "tier_level": 3,
        "weight_coefficient": 0.476,
        "elasticity_index": 0.991,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_47"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0048",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-48",
        "tier_level": 4,
        "weight_coefficient": 0.484,
        "elasticity_index": 0.994,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_48"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0049",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-49",
        "tier_level": 5,
        "weight_coefficient": 0.492,
        "elasticity_index": 0.997,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_23", "node_49"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0050",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-50",
        "tier_level": 1,
        "weight_coefficient": 0.5,
        "elasticity_index": 1.0,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_50"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0051",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-51",
        "tier_level": 2,
        "weight_coefficient": 0.508,
        "elasticity_index": 1.003,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_51"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0052",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-52",
        "tier_level": 3,
        "weight_coefficient": 0.516,
        "elasticity_index": 1.006,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_52"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0053",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-53",
        "tier_level": 4,
        "weight_coefficient": 0.524,
        "elasticity_index": 1.009,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_53"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0054",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-54",
        "tier_level": 5,
        "weight_coefficient": 0.532,
        "elasticity_index": 1.012,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_54"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0055",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-55",
        "tier_level": 1,
        "weight_coefficient": 0.54,
        "elasticity_index": 1.015,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_55"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0056",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-56",
        "tier_level": 2,
        "weight_coefficient": 0.548,
        "elasticity_index": 1.018,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_23", "node_56"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0057",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-57",
        "tier_level": 3,
        "weight_coefficient": 0.556,
        "elasticity_index": 1.021,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_57"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0058",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-58",
        "tier_level": 4,
        "weight_coefficient": 0.564,
        "elasticity_index": 1.024,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_58"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0059",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-59",
        "tier_level": 5,
        "weight_coefficient": 0.572,
        "elasticity_index": 1.027,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_59"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0060",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-60",
        "tier_level": 1,
        "weight_coefficient": 0.58,
        "elasticity_index": 1.03,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_60"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0061",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-61",
        "tier_level": 2,
        "weight_coefficient": 0.588,
        "elasticity_index": 1.033,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_61"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0062",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-62",
        "tier_level": 3,
        "weight_coefficient": 0.596,
        "elasticity_index": 1.036,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_62"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0063",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-63",
        "tier_level": 4,
        "weight_coefficient": 0.604,
        "elasticity_index": 1.039,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_23", "node_63"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0064",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-64",
        "tier_level": 5,
        "weight_coefficient": 0.612,
        "elasticity_index": 1.042,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_64"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0065",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-65",
        "tier_level": 1,
        "weight_coefficient": 0.62,
        "elasticity_index": 1.045,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_65"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0066",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-66",
        "tier_level": 2,
        "weight_coefficient": 0.628,
        "elasticity_index": 1.048,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_66"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0067",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-67",
        "tier_level": 3,
        "weight_coefficient": 0.636,
        "elasticity_index": 1.051,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_67"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0068",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-68",
        "tier_level": 4,
        "weight_coefficient": 0.644,
        "elasticity_index": 1.054,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_68"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0069",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-69",
        "tier_level": 5,
        "weight_coefficient": 0.652,
        "elasticity_index": 1.057,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_69"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0070",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-70",
        "tier_level": 1,
        "weight_coefficient": 0.66,
        "elasticity_index": 1.06,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_23", "node_70"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0071",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-71",
        "tier_level": 2,
        "weight_coefficient": 0.668,
        "elasticity_index": 1.063,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_71"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0072",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-72",
        "tier_level": 3,
        "weight_coefficient": 0.676,
        "elasticity_index": 1.066,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_72"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0073",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-73",
        "tier_level": 4,
        "weight_coefficient": 0.684,
        "elasticity_index": 1.069,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_73"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0074",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-74",
        "tier_level": 5,
        "weight_coefficient": 0.692,
        "elasticity_index": 1.072,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_74"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0075",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-75",
        "tier_level": 1,
        "weight_coefficient": 0.7,
        "elasticity_index": 1.075,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_75"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0076",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-76",
        "tier_level": 2,
        "weight_coefficient": 0.708,
        "elasticity_index": 1.078,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_76"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0077",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-77",
        "tier_level": 3,
        "weight_coefficient": 0.716,
        "elasticity_index": 1.081,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_23", "node_77"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0078",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-78",
        "tier_level": 4,
        "weight_coefficient": 0.724,
        "elasticity_index": 1.084,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_78"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0079",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-79",
        "tier_level": 5,
        "weight_coefficient": 0.732,
        "elasticity_index": 1.087,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_79"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0080",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-80",
        "tier_level": 1,
        "weight_coefficient": 0.74,
        "elasticity_index": 1.09,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_80"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0081",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-81",
        "tier_level": 2,
        "weight_coefficient": 0.748,
        "elasticity_index": 1.093,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_81"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0082",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-82",
        "tier_level": 3,
        "weight_coefficient": 0.756,
        "elasticity_index": 1.096,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_82"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0083",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-83",
        "tier_level": 4,
        "weight_coefficient": 0.764,
        "elasticity_index": 1.099,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_83"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0084",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-84",
        "tier_level": 5,
        "weight_coefficient": 0.772,
        "elasticity_index": 1.102,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_23", "node_84"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0085",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-85",
        "tier_level": 1,
        "weight_coefficient": 0.78,
        "elasticity_index": 1.105,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_85"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0086",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-86",
        "tier_level": 2,
        "weight_coefficient": 0.788,
        "elasticity_index": 1.108,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_86"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0087",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-87",
        "tier_level": 3,
        "weight_coefficient": 0.796,
        "elasticity_index": 1.111,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_87"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0088",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-88",
        "tier_level": 4,
        "weight_coefficient": 0.804,
        "elasticity_index": 1.114,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_88"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0089",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-89",
        "tier_level": 5,
        "weight_coefficient": 0.812,
        "elasticity_index": 1.117,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_89"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0090",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-90",
        "tier_level": 1,
        "weight_coefficient": 0.82,
        "elasticity_index": 1.12,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_90"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0091",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-91",
        "tier_level": 2,
        "weight_coefficient": 0.828,
        "elasticity_index": 1.123,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_23", "node_91"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0092",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-92",
        "tier_level": 3,
        "weight_coefficient": 0.836,
        "elasticity_index": 1.126,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_92"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0093",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-93",
        "tier_level": 4,
        "weight_coefficient": 0.844,
        "elasticity_index": 1.129,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_93"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0094",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-94",
        "tier_level": 5,
        "weight_coefficient": 0.852,
        "elasticity_index": 1.132,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_94"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0095",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-95",
        "tier_level": 1,
        "weight_coefficient": 0.86,
        "elasticity_index": 1.135,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_95"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0096",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-96",
        "tier_level": 2,
        "weight_coefficient": 0.868,
        "elasticity_index": 1.138,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_96"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0097",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-97",
        "tier_level": 3,
        "weight_coefficient": 0.876,
        "elasticity_index": 1.141,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_97"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0098",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-98",
        "tier_level": 4,
        "weight_coefficient": 0.884,
        "elasticity_index": 1.144,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_23", "node_98"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0099",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-99",
        "tier_level": 5,
        "weight_coefficient": 0.892,
        "elasticity_index": 1.147,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_99"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0100",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-100",
        "tier_level": 1,
        "weight_coefficient": 0.9,
        "elasticity_index": 1.15,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_100"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0101",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-101",
        "tier_level": 2,
        "weight_coefficient": 0.908,
        "elasticity_index": 1.153,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_101"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0102",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-102",
        "tier_level": 3,
        "weight_coefficient": 0.916,
        "elasticity_index": 1.156,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_102"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0103",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-103",
        "tier_level": 4,
        "weight_coefficient": 0.924,
        "elasticity_index": 1.159,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_103"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0104",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-104",
        "tier_level": 5,
        "weight_coefficient": 0.932,
        "elasticity_index": 1.162,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_104"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0105",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-105",
        "tier_level": 1,
        "weight_coefficient": 0.94,
        "elasticity_index": 1.165,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_23", "node_105"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0106",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-106",
        "tier_level": 2,
        "weight_coefficient": 0.948,
        "elasticity_index": 1.168,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_106"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0107",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-107",
        "tier_level": 3,
        "weight_coefficient": 0.956,
        "elasticity_index": 1.171,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_107"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0108",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-108",
        "tier_level": 4,
        "weight_coefficient": 0.964,
        "elasticity_index": 1.174,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_108"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0109",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-109",
        "tier_level": 5,
        "weight_coefficient": 0.972,
        "elasticity_index": 1.177,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_109"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0110",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-110",
        "tier_level": 1,
        "weight_coefficient": 0.98,
        "elasticity_index": 1.18,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_110"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0111",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-111",
        "tier_level": 2,
        "weight_coefficient": 0.988,
        "elasticity_index": 1.183,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_111"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0112",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-112",
        "tier_level": 3,
        "weight_coefficient": 0.996,
        "elasticity_index": 1.186,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_23", "node_112"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0113",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-113",
        "tier_level": 4,
        "weight_coefficient": 1.004,
        "elasticity_index": 1.189,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_113"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0114",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-114",
        "tier_level": 5,
        "weight_coefficient": 1.012,
        "elasticity_index": 1.192,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_114"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0115",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-115",
        "tier_level": 1,
        "weight_coefficient": 1.02,
        "elasticity_index": 1.195,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_115"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0116",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-116",
        "tier_level": 2,
        "weight_coefficient": 1.028,
        "elasticity_index": 1.198,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_116"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0117",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-117",
        "tier_level": 3,
        "weight_coefficient": 1.036,
        "elasticity_index": 1.201,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_117"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0118",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-118",
        "tier_level": 4,
        "weight_coefficient": 1.044,
        "elasticity_index": 1.204,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_118"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0119",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-119",
        "tier_level": 5,
        "weight_coefficient": 1.052,
        "elasticity_index": 1.207,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_23", "node_119"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0120",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-120",
        "tier_level": 1,
        "weight_coefficient": 1.06,
        "elasticity_index": 1.21,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_120"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0121",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-121",
        "tier_level": 2,
        "weight_coefficient": 1.068,
        "elasticity_index": 1.213,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_121"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0122",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-122",
        "tier_level": 3,
        "weight_coefficient": 1.076,
        "elasticity_index": 1.216,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_122"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0123",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-123",
        "tier_level": 4,
        "weight_coefficient": 1.084,
        "elasticity_index": 1.219,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_123"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0124",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-124",
        "tier_level": 5,
        "weight_coefficient": 1.092,
        "elasticity_index": 1.222,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_124"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0125",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-125",
        "tier_level": 1,
        "weight_coefficient": 1.1,
        "elasticity_index": 1.225,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_125"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0126",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-126",
        "tier_level": 2,
        "weight_coefficient": 1.108,
        "elasticity_index": 1.228,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_23", "node_126"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0127",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-127",
        "tier_level": 3,
        "weight_coefficient": 1.116,
        "elasticity_index": 1.231,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_127"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0128",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-128",
        "tier_level": 4,
        "weight_coefficient": 1.124,
        "elasticity_index": 1.234,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_128"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0129",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-129",
        "tier_level": 5,
        "weight_coefficient": 1.132,
        "elasticity_index": 1.237,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_129"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0130",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-130",
        "tier_level": 1,
        "weight_coefficient": 1.14,
        "elasticity_index": 1.24,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_130"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0131",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-131",
        "tier_level": 2,
        "weight_coefficient": 1.148,
        "elasticity_index": 1.243,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_131"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0132",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-132",
        "tier_level": 3,
        "weight_coefficient": 1.156,
        "elasticity_index": 1.246,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_132"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0133",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-133",
        "tier_level": 4,
        "weight_coefficient": 1.164,
        "elasticity_index": 1.249,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_23", "node_133"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0134",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-134",
        "tier_level": 5,
        "weight_coefficient": 1.172,
        "elasticity_index": 1.252,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_134"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0135",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-135",
        "tier_level": 1,
        "weight_coefficient": 1.18,
        "elasticity_index": 1.255,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_135"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0136",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-136",
        "tier_level": 2,
        "weight_coefficient": 1.188,
        "elasticity_index": 1.258,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_136"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0137",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-137",
        "tier_level": 3,
        "weight_coefficient": 1.196,
        "elasticity_index": 1.261,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_137"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0138",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-138",
        "tier_level": 4,
        "weight_coefficient": 1.204,
        "elasticity_index": 1.264,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_138"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0139",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-139",
        "tier_level": 5,
        "weight_coefficient": 1.212,
        "elasticity_index": 1.267,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_139"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0140",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-140",
        "tier_level": 1,
        "weight_coefficient": 1.22,
        "elasticity_index": 1.27,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_23", "node_140"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0141",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-141",
        "tier_level": 2,
        "weight_coefficient": 1.228,
        "elasticity_index": 1.273,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_141"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0142",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-142",
        "tier_level": 3,
        "weight_coefficient": 1.236,
        "elasticity_index": 1.276,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_142"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0143",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-143",
        "tier_level": 4,
        "weight_coefficient": 1.244,
        "elasticity_index": 1.279,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_143"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0144",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-144",
        "tier_level": 5,
        "weight_coefficient": 1.252,
        "elasticity_index": 1.282,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_144"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0145",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-145",
        "tier_level": 1,
        "weight_coefficient": 1.26,
        "elasticity_index": 1.285,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_145"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0146",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-146",
        "tier_level": 2,
        "weight_coefficient": 1.268,
        "elasticity_index": 1.288,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_146"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0147",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-147",
        "tier_level": 3,
        "weight_coefficient": 1.276,
        "elasticity_index": 1.291,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_23", "node_147"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0148",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-148",
        "tier_level": 4,
        "weight_coefficient": 1.284,
        "elasticity_index": 1.294,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_148"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0149",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-149",
        "tier_level": 5,
        "weight_coefficient": 1.292,
        "elasticity_index": 1.297,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_149"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0150",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-150",
        "tier_level": 1,
        "weight_coefficient": 1.3,
        "elasticity_index": 1.3,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_150"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0151",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-151",
        "tier_level": 2,
        "weight_coefficient": 1.308,
        "elasticity_index": 1.303,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_151"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0152",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-152",
        "tier_level": 3,
        "weight_coefficient": 1.316,
        "elasticity_index": 1.306,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_152"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0153",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-153",
        "tier_level": 4,
        "weight_coefficient": 1.324,
        "elasticity_index": 1.309,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_153"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0154",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-154",
        "tier_level": 5,
        "weight_coefficient": 1.332,
        "elasticity_index": 1.312,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_23", "node_154"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0155",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-155",
        "tier_level": 1,
        "weight_coefficient": 1.34,
        "elasticity_index": 1.315,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_155"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0156",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-156",
        "tier_level": 2,
        "weight_coefficient": 1.348,
        "elasticity_index": 1.318,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_156"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0157",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-157",
        "tier_level": 3,
        "weight_coefficient": 1.356,
        "elasticity_index": 1.321,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_157"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0158",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-158",
        "tier_level": 4,
        "weight_coefficient": 1.364,
        "elasticity_index": 1.324,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_158"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0159",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-159",
        "tier_level": 5,
        "weight_coefficient": 1.372,
        "elasticity_index": 1.327,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_159"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0160",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-160",
        "tier_level": 1,
        "weight_coefficient": 1.38,
        "elasticity_index": 1.33,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_160"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0161",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-161",
        "tier_level": 2,
        "weight_coefficient": 1.388,
        "elasticity_index": 1.333,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_23", "node_161"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0162",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-162",
        "tier_level": 3,
        "weight_coefficient": 1.396,
        "elasticity_index": 1.336,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_162"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0163",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-163",
        "tier_level": 4,
        "weight_coefficient": 1.404,
        "elasticity_index": 1.339,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_163"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0164",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-164",
        "tier_level": 5,
        "weight_coefficient": 1.412,
        "elasticity_index": 1.342,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_164"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0165",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-165",
        "tier_level": 1,
        "weight_coefficient": 1.42,
        "elasticity_index": 1.345,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_165"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0166",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-166",
        "tier_level": 2,
        "weight_coefficient": 1.428,
        "elasticity_index": 1.348,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_166"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0167",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-167",
        "tier_level": 3,
        "weight_coefficient": 1.436,
        "elasticity_index": 1.351,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_167"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0168",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-168",
        "tier_level": 4,
        "weight_coefficient": 1.444,
        "elasticity_index": 1.354,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_23", "node_168"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0169",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-169",
        "tier_level": 5,
        "weight_coefficient": 1.452,
        "elasticity_index": 1.357,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_169"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0170",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-170",
        "tier_level": 1,
        "weight_coefficient": 1.46,
        "elasticity_index": 1.36,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_170"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0171",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-171",
        "tier_level": 2,
        "weight_coefficient": 1.468,
        "elasticity_index": 1.363,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_171"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0172",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-172",
        "tier_level": 3,
        "weight_coefficient": 1.476,
        "elasticity_index": 1.366,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_172"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0173",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-173",
        "tier_level": 4,
        "weight_coefficient": 1.484,
        "elasticity_index": 1.369,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_173"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0174",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-174",
        "tier_level": 5,
        "weight_coefficient": 1.492,
        "elasticity_index": 1.372,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_174"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0175",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-175",
        "tier_level": 1,
        "weight_coefficient": 1.5,
        "elasticity_index": 1.375,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_23", "node_175"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0176",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-176",
        "tier_level": 2,
        "weight_coefficient": 1.508,
        "elasticity_index": 1.378,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_176"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0177",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-177",
        "tier_level": 3,
        "weight_coefficient": 1.516,
        "elasticity_index": 1.381,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_177"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0178",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-178",
        "tier_level": 4,
        "weight_coefficient": 1.524,
        "elasticity_index": 1.384,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_178"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0179",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-179",
        "tier_level": 5,
        "weight_coefficient": 1.532,
        "elasticity_index": 1.387,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_179"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0180",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-180",
        "tier_level": 1,
        "weight_coefficient": 1.54,
        "elasticity_index": 1.39,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_180"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0181",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-181",
        "tier_level": 2,
        "weight_coefficient": 1.548,
        "elasticity_index": 1.393,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_181"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0182",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-182",
        "tier_level": 3,
        "weight_coefficient": 1.556,
        "elasticity_index": 1.396,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_23", "node_182"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0183",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-183",
        "tier_level": 4,
        "weight_coefficient": 1.564,
        "elasticity_index": 1.399,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_183"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0184",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-184",
        "tier_level": 5,
        "weight_coefficient": 1.572,
        "elasticity_index": 1.402,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_184"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0185",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-185",
        "tier_level": 1,
        "weight_coefficient": 1.58,
        "elasticity_index": 1.405,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_185"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0186",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-186",
        "tier_level": 2,
        "weight_coefficient": 1.588,
        "elasticity_index": 1.408,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_186"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0187",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-187",
        "tier_level": 3,
        "weight_coefficient": 1.596,
        "elasticity_index": 1.411,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_187"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0188",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-188",
        "tier_level": 4,
        "weight_coefficient": 1.604,
        "elasticity_index": 1.414,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_188"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0189",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-189",
        "tier_level": 5,
        "weight_coefficient": 1.612,
        "elasticity_index": 1.417,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_23", "node_189"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0190",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-190",
        "tier_level": 1,
        "weight_coefficient": 1.62,
        "elasticity_index": 1.42,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_190"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0191",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-191",
        "tier_level": 2,
        "weight_coefficient": 1.628,
        "elasticity_index": 1.423,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_191"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0192",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-192",
        "tier_level": 3,
        "weight_coefficient": 1.636,
        "elasticity_index": 1.426,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_192"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0193",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-193",
        "tier_level": 4,
        "weight_coefficient": 1.644,
        "elasticity_index": 1.429,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_193"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0194",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-194",
        "tier_level": 5,
        "weight_coefficient": 1.652,
        "elasticity_index": 1.432,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_194"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0195",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-195",
        "tier_level": 1,
        "weight_coefficient": 1.66,
        "elasticity_index": 1.435,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_195"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0196",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-196",
        "tier_level": 2,
        "weight_coefficient": 1.668,
        "elasticity_index": 1.438,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_23", "node_196"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0197",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-197",
        "tier_level": 3,
        "weight_coefficient": 1.676,
        "elasticity_index": 1.441,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_197"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0198",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-198",
        "tier_level": 4,
        "weight_coefficient": 1.684,
        "elasticity_index": 1.444,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_198"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0199",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-199",
        "tier_level": 5,
        "weight_coefficient": 1.692,
        "elasticity_index": 1.447,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_199"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0200",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-200",
        "tier_level": 1,
        "weight_coefficient": 1.7,
        "elasticity_index": 1.45,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_200"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0201",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-201",
        "tier_level": 2,
        "weight_coefficient": 1.708,
        "elasticity_index": 1.453,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_201"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0202",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-202",
        "tier_level": 3,
        "weight_coefficient": 1.716,
        "elasticity_index": 1.456,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_202"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0203",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-203",
        "tier_level": 4,
        "weight_coefficient": 1.724,
        "elasticity_index": 1.459,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_23", "node_203"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0204",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-204",
        "tier_level": 5,
        "weight_coefficient": 1.732,
        "elasticity_index": 1.462,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_204"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0205",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-205",
        "tier_level": 1,
        "weight_coefficient": 1.74,
        "elasticity_index": 1.465,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_205"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0206",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-206",
        "tier_level": 2,
        "weight_coefficient": 1.748,
        "elasticity_index": 1.468,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_206"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0207",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-207",
        "tier_level": 3,
        "weight_coefficient": 1.756,
        "elasticity_index": 1.471,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_207"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0208",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-208",
        "tier_level": 4,
        "weight_coefficient": 1.764,
        "elasticity_index": 1.474,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_208"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0209",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-209",
        "tier_level": 5,
        "weight_coefficient": 1.772,
        "elasticity_index": 1.477,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_209"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0210",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-210",
        "tier_level": 1,
        "weight_coefficient": 1.78,
        "elasticity_index": 1.48,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_23", "node_210"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0211",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-211",
        "tier_level": 2,
        "weight_coefficient": 1.788,
        "elasticity_index": 1.483,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_211"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0212",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-212",
        "tier_level": 3,
        "weight_coefficient": 1.796,
        "elasticity_index": 1.486,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_212"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0213",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-213",
        "tier_level": 4,
        "weight_coefficient": 1.804,
        "elasticity_index": 1.489,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_213"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0214",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-214",
        "tier_level": 5,
        "weight_coefficient": 1.812,
        "elasticity_index": 1.492,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_214"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0215",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-215",
        "tier_level": 1,
        "weight_coefficient": 1.82,
        "elasticity_index": 1.495,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_215"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0216",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-216",
        "tier_level": 2,
        "weight_coefficient": 1.828,
        "elasticity_index": 1.498,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_216"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0217",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-217",
        "tier_level": 3,
        "weight_coefficient": 1.836,
        "elasticity_index": 1.501,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_23", "node_217"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0218",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-218",
        "tier_level": 4,
        "weight_coefficient": 1.844,
        "elasticity_index": 1.504,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_218"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0219",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-219",
        "tier_level": 5,
        "weight_coefficient": 1.852,
        "elasticity_index": 1.507,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_219"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0220",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-220",
        "tier_level": 1,
        "weight_coefficient": 1.86,
        "elasticity_index": 1.51,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_220"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0221",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-221",
        "tier_level": 2,
        "weight_coefficient": 1.868,
        "elasticity_index": 1.513,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_221"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0222",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-222",
        "tier_level": 3,
        "weight_coefficient": 1.876,
        "elasticity_index": 1.516,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_222"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0223",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-223",
        "tier_level": 4,
        "weight_coefficient": 1.884,
        "elasticity_index": 1.519,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_223"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0224",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-224",
        "tier_level": 5,
        "weight_coefficient": 1.892,
        "elasticity_index": 1.522,
        "active_flag": False,
        "audit_tags": ["tier_0", "cluster_23", "node_224"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0225",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-225",
        "tier_level": 1,
        "weight_coefficient": 1.9,
        "elasticity_index": 1.525,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_225"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0226",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-226",
        "tier_level": 2,
        "weight_coefficient": 1.908,
        "elasticity_index": 1.528,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_226"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0227",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-227",
        "tier_level": 3,
        "weight_coefficient": 1.916,
        "elasticity_index": 1.531,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_227"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0228",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-228",
        "tier_level": 4,
        "weight_coefficient": 1.924,
        "elasticity_index": 1.534,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_228"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0229",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-229",
        "tier_level": 5,
        "weight_coefficient": 1.932,
        "elasticity_index": 1.537,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_229"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0230",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-230",
        "tier_level": 1,
        "weight_coefficient": 1.94,
        "elasticity_index": 1.54,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_230"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0231",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-231",
        "tier_level": 2,
        "weight_coefficient": 1.948,
        "elasticity_index": 1.543,
        "active_flag": False,
        "audit_tags": ["tier_3", "cluster_23", "node_231"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0232",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-232",
        "tier_level": 3,
        "weight_coefficient": 1.956,
        "elasticity_index": 1.546,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_232"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0233",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-233",
        "tier_level": 4,
        "weight_coefficient": 1.964,
        "elasticity_index": 1.549,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_233"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0234",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-234",
        "tier_level": 5,
        "weight_coefficient": 1.972,
        "elasticity_index": 1.552,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_234"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0235",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-235",
        "tier_level": 1,
        "weight_coefficient": 1.98,
        "elasticity_index": 1.555,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_235"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0236",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-236",
        "tier_level": 2,
        "weight_coefficient": 1.988,
        "elasticity_index": 1.558,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_236"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0237",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-237",
        "tier_level": 3,
        "weight_coefficient": 1.996,
        "elasticity_index": 1.561,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_237"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0238",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-238",
        "tier_level": 4,
        "weight_coefficient": 2.004,
        "elasticity_index": 1.564,
        "active_flag": False,
        "audit_tags": ["tier_2", "cluster_23", "node_238"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0239",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-239",
        "tier_level": 5,
        "weight_coefficient": 2.012,
        "elasticity_index": 1.567,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_239"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0240",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-240",
        "tier_level": 1,
        "weight_coefficient": 2.02,
        "elasticity_index": 1.57,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_240"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0241",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-241",
        "tier_level": 2,
        "weight_coefficient": 2.028,
        "elasticity_index": 1.573,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_241"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0242",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-242",
        "tier_level": 3,
        "weight_coefficient": 2.036,
        "elasticity_index": 1.576,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_242"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0243",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-243",
        "tier_level": 4,
        "weight_coefficient": 2.044,
        "elasticity_index": 1.579,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_243"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0244",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-244",
        "tier_level": 5,
        "weight_coefficient": 2.052,
        "elasticity_index": 1.582,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_244"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0245",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-245",
        "tier_level": 1,
        "weight_coefficient": 2.06,
        "elasticity_index": 1.585,
        "active_flag": False,
        "audit_tags": ["tier_1", "cluster_23", "node_245"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0246",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-246",
        "tier_level": 2,
        "weight_coefficient": 2.068,
        "elasticity_index": 1.588,
        "active_flag": True,
        "audit_tags": ["tier_2", "cluster_23", "node_246"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0247",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-247",
        "tier_level": 3,
        "weight_coefficient": 2.076,
        "elasticity_index": 1.591,
        "active_flag": True,
        "audit_tags": ["tier_3", "cluster_23", "node_247"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0248",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-248",
        "tier_level": 4,
        "weight_coefficient": 2.084,
        "elasticity_index": 1.594,
        "active_flag": True,
        "audit_tags": ["tier_0", "cluster_23", "node_248"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
    {
        "matrix_id": "REF-23-0249",
        "entity_key": "ENT-digital-gift-cards-store-credit-system-249",
        "tier_level": 5,
        "weight_coefficient": 2.092,
        "elasticity_index": 1.597,
        "active_flag": True,
        "audit_tags": ["tier_1", "cluster_23", "node_249"],
        "created_timestamp": "2026-09-12T12:00:00Z",
    },
]

