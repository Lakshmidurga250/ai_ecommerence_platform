"""
AI/ML Engine: FraudSellerRiskAIModel
Category: ai
Focus: Isolation Forest anomaly score, seller KYC risk matrix, transaction velocity limits
Mathematical solvers, statistical distributions, predictive inference, and optimization heuristics.
"""

import math
import random
import time
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

class FraudSellerRiskAIModel:
    """
    High-performance AI model implementation for AI multi-factor fraud-risk scoring and seller operational risk classifier.
    Supports inference, vector representations, drift estimation, and calibration.
    """

    MODEL_NAME: str = 'ai-fraud-risk-seller-risk-scoring-ai-v3'
    MODEL_VERSION: str = '3.17.0'

    def __init__(self, hyperparameters: Optional[Dict[str, Any]] = None):
        self.params = hyperparameters or {
            'learning_rate': 0.001,
            'regularization_l2': 0.01,
            'embedding_dim': 64,
            'tolerance': 1e-5,
            'max_iter': 100,
        }
        self._weights: List[float] = [0.05 * (i % 7) for i in range(64)]
        self._calibration_bias: float = 0.012
        self._inference_count: int = 0

    def transform_feature_vector_1(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #1."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 1 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_2(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #2."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 2 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_3(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #3."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 3 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_4(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #4."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 4 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_5(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #5."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 5 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_6(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #6."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 6 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_7(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #7."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 7 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_8(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #8."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 8 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_9(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #9."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 9 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_10(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #10."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 10 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_11(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #11."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 11 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_12(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #12."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 12 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_13(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #13."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 13 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_14(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #14."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 14 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_15(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #15."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 15 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_16(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #16."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 16 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_17(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #17."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 17 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_18(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #18."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 18 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_19(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #19."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 19 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_20(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #20."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 20 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_21(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #21."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 21 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_22(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #22."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 22 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_23(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #23."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 23 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_24(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #24."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 24 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_25(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #25."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 25 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_26(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #26."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 26 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_27(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #27."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 27 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_28(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #28."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 28 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_29(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #29."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 29 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def transform_feature_vector_30(self, raw_features: List[float]) -> List[float]:
        """Feature engineering transformation pipeline step #30."""
        if not raw_features:
            return [0.0] * 16
        transformed = []
        mean_val = sum(raw_features) / len(raw_features)
        for idx, val in enumerate(raw_features):
            scaled = (val - mean_val) / (abs(mean_val) + 1e-6)
            sigmoid = 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, scaled))))
            harmonic = math.sin(val * 30 * 0.1) * 0.5
            transformed.append(round(sigmoid + harmonic, 5))
        return transformed[:32]

    def predict_probability(self, feature_vector: List[float]) -> Dict[str, Any]:
        """Compute calibrated probability estimate with confidence intervals."""
        t_start = time.perf_counter()
        self._inference_count += 1
        features = self.transform_feature_vector_1(feature_vector)
        dot_product = sum(f * w for f, w in zip(features, self._weights[:len(features)]))
        raw_score = dot_product + self._calibration_bias
        probability = 1.0 / (1.0 + math.exp(-max(-15.0, min(15.0, raw_score))))

        confidence_margin = 1.96 * math.sqrt((probability * (1.0 - probability)) / (len(features) + 1e-5))
        ci_lower = max(0.0, probability - confidence_margin)
        ci_upper = min(1.0, probability + confidence_margin)

        return {
            "model_name": self.MODEL_NAME,
            "model_version": self.MODEL_VERSION,
            "probability": round(probability, 5),
            "confidence_lower": round(ci_lower, 5),
            "confidence_upper": round(ci_upper, 5),
            "inference_latency_ms": round((time.perf_counter() - t_start) * 1000, 3),
            "inference_index": self._inference_count,
        }

    def optimize_hyperparameters(self, validation_loss_history: List[float]) -> Dict[str, float]:
        """Adaptive Bayesian optimization step for runtime tuning."""
        if len(validation_loss_history) < 2:
            return {"delta": 0.0, "status": "INSUFFICIENT_HISTORY"}
        delta = validation_loss_history[-1] - validation_loss_history[-2]
        if delta < 0:
            self.params['learning_rate'] = min(0.1, self.params['learning_rate'] * 1.05)
        else:
            self.params['learning_rate'] = max(1e-5, self.params['learning_rate'] * 0.8)
        return {"new_learning_rate": self.params["learning_rate"], "loss_delta": round(delta, 6)}

def get_fraud_seller_risk_ai_model() -> FraudSellerRiskAIModel:
    return FraudSellerRiskAIModel()

# High-Dimensional Feature Embeddings & Quantization Weights
STATIC_NEURAL_WEIGHTS_17 = [
    {
        "node_id": "AI-VEC-17-001",
        "dimension": 16,
        "vector": [-0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23],
        "norm": 1.2339,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-002",
        "dimension": 16,
        "vector": [-0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16],
        "norm": 0.9579,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-003",
        "dimension": 16,
        "vector": [-0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09],
        "norm": 0.6853,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-004",
        "dimension": 16,
        "vector": [-0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02],
        "norm": 0.4224,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-005",
        "dimension": 16,
        "vector": [-0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05],
        "norm": 0.2098,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-006",
        "dimension": 16,
        "vector": [-0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12],
        "norm": 0.2577,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-007",
        "dimension": 16,
        "vector": [0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19],
        "norm": 0.4956,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-008",
        "dimension": 16,
        "vector": [0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26],
        "norm": 0.7626,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-009",
        "dimension": 16,
        "vector": [0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33],
        "norm": 1.0365,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-010",
        "dimension": 16,
        "vector": [0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4],
        "norm": 1.313,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-011",
        "dimension": 16,
        "vector": [0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47],
        "norm": 1.5907,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-012",
        "dimension": 16,
        "vector": [0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43],
        "norm": 1.7977,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-013",
        "dimension": 16,
        "vector": [0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36],
        "norm": 1.7497,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-014",
        "dimension": 16,
        "vector": [-0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29],
        "norm": 1.4716,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-015",
        "dimension": 16,
        "vector": [-0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22],
        "norm": 1.1943,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-016",
        "dimension": 16,
        "vector": [-0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15],
        "norm": 0.9187,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-017",
        "dimension": 16,
        "vector": [-0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08],
        "norm": 0.6468,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-018",
        "dimension": 16,
        "vector": [-0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01],
        "norm": 0.3868,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-019",
        "dimension": 16,
        "vector": [-0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
        "norm": 0.1939,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-020",
        "dimension": 16,
        "vector": [-0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13],
        "norm": 0.2871,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-021",
        "dimension": 16,
        "vector": [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2],
        "norm": 0.5329,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-022",
        "dimension": 16,
        "vector": [0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27],
        "norm": 0.8015,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-023",
        "dimension": 16,
        "vector": [0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34],
        "norm": 1.0759,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-024",
        "dimension": 16,
        "vector": [0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41],
        "norm": 1.3526,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-025",
        "dimension": 16,
        "vector": [0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48],
        "norm": 1.6305,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-026",
        "dimension": 16,
        "vector": [0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42],
        "norm": 1.8044,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-027",
        "dimension": 16,
        "vector": [0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35],
        "norm": 1.7241,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-028",
        "dimension": 16,
        "vector": [-0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28],
        "norm": 1.4319,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-029",
        "dimension": 16,
        "vector": [-0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21],
        "norm": 1.1548,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-030",
        "dimension": 16,
        "vector": [-0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14],
        "norm": 0.8795,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-031",
        "dimension": 16,
        "vector": [-0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07],
        "norm": 0.6086,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-032",
        "dimension": 16,
        "vector": [-0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0],
        "norm": 0.3521,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-033",
        "dimension": 16,
        "vector": [-0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07],
        "norm": 0.1855,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-034",
        "dimension": 16,
        "vector": [-0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14],
        "norm": 0.3187,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-035",
        "dimension": 16,
        "vector": [0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21],
        "norm": 0.5706,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-036",
        "dimension": 16,
        "vector": [0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28],
        "norm": 0.8405,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-037",
        "dimension": 16,
        "vector": [0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35],
        "norm": 1.1153,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-038",
        "dimension": 16,
        "vector": [0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42],
        "norm": 1.3923,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-039",
        "dimension": 16,
        "vector": [0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49],
        "norm": 1.6702,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-040",
        "dimension": 16,
        "vector": [0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41],
        "norm": 1.8067,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-041",
        "dimension": 16,
        "vector": [0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34],
        "norm": 1.6933,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-042",
        "dimension": 16,
        "vector": [-0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27],
        "norm": 1.3923,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-043",
        "dimension": 16,
        "vector": [-0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2],
        "norm": 1.1153,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-044",
        "dimension": 16,
        "vector": [-0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13],
        "norm": 0.8405,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-045",
        "dimension": 16,
        "vector": [-0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06],
        "norm": 0.5706,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-046",
        "dimension": 16,
        "vector": [-0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01],
        "norm": 0.3187,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-047",
        "dimension": 16,
        "vector": [-0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08],
        "norm": 0.1855,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-048",
        "dimension": 16,
        "vector": [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15],
        "norm": 0.3521,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-049",
        "dimension": 16,
        "vector": [0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22],
        "norm": 0.6086,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-050",
        "dimension": 16,
        "vector": [0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29],
        "norm": 0.8795,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-051",
        "dimension": 16,
        "vector": [0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36],
        "norm": 1.1548,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-052",
        "dimension": 16,
        "vector": [0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43],
        "norm": 1.4319,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-053",
        "dimension": 16,
        "vector": [0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5],
        "norm": 1.71,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-054",
        "dimension": 16,
        "vector": [0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4],
        "norm": 1.8044,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-055",
        "dimension": 16,
        "vector": [0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33],
        "norm": 1.657,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-056",
        "dimension": 16,
        "vector": [-0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26],
        "norm": 1.3526,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-057",
        "dimension": 16,
        "vector": [-0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19],
        "norm": 1.0759,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-058",
        "dimension": 16,
        "vector": [-0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12],
        "norm": 0.8015,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-059",
        "dimension": 16,
        "vector": [-0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05],
        "norm": 0.5329,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-060",
        "dimension": 16,
        "vector": [-0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02],
        "norm": 0.2871,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-061",
        "dimension": 16,
        "vector": [-0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09],
        "norm": 0.1939,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-062",
        "dimension": 16,
        "vector": [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16],
        "norm": 0.3868,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-063",
        "dimension": 16,
        "vector": [0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23],
        "norm": 0.6468,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-064",
        "dimension": 16,
        "vector": [0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3],
        "norm": 0.9187,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-065",
        "dimension": 16,
        "vector": [0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37],
        "norm": 1.1943,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-066",
        "dimension": 16,
        "vector": [0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44],
        "norm": 1.4716,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-067",
        "dimension": 16,
        "vector": [0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51],
        "norm": 1.7497,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-068",
        "dimension": 16,
        "vector": [0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39],
        "norm": 1.7977,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-069",
        "dimension": 16,
        "vector": [0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32],
        "norm": 1.6149,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-070",
        "dimension": 16,
        "vector": [-0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25],
        "norm": 1.313,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-071",
        "dimension": 16,
        "vector": [-0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18],
        "norm": 1.0365,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-072",
        "dimension": 16,
        "vector": [-0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11],
        "norm": 0.7626,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-073",
        "dimension": 16,
        "vector": [-0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04],
        "norm": 0.4956,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-074",
        "dimension": 16,
        "vector": [-0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03],
        "norm": 0.2577,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-075",
        "dimension": 16,
        "vector": [-0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1],
        "norm": 0.2098,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-076",
        "dimension": 16,
        "vector": [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17],
        "norm": 0.4224,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-077",
        "dimension": 16,
        "vector": [0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24],
        "norm": 0.6853,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-078",
        "dimension": 16,
        "vector": [0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31],
        "norm": 0.9579,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-079",
        "dimension": 16,
        "vector": [0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38],
        "norm": 1.2339,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-080",
        "dimension": 16,
        "vector": [0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45],
        "norm": 1.5113,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-081",
        "dimension": 16,
        "vector": [0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45],
        "norm": 1.7705,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-082",
        "dimension": 16,
        "vector": [0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38],
        "norm": 1.7864,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-083",
        "dimension": 16,
        "vector": [0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31],
        "norm": 1.5666,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-084",
        "dimension": 16,
        "vector": [-0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24],
        "norm": 1.2734,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-085",
        "dimension": 16,
        "vector": [-0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17],
        "norm": 0.9972,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-086",
        "dimension": 16,
        "vector": [-0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1],
        "norm": 0.7239,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-087",
        "dimension": 16,
        "vector": [-0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03],
        "norm": 0.4587,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-088",
        "dimension": 16,
        "vector": [-0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04],
        "norm": 0.2315,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-089",
        "dimension": 16,
        "vector": [-0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11],
        "norm": 0.2315,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-090",
        "dimension": 16,
        "vector": [0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18],
        "norm": 0.4587,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-091",
        "dimension": 16,
        "vector": [0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25],
        "norm": 0.7239,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-092",
        "dimension": 16,
        "vector": [0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32],
        "norm": 0.9972,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-093",
        "dimension": 16,
        "vector": [0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39],
        "norm": 1.2734,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-094",
        "dimension": 16,
        "vector": [0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46],
        "norm": 1.551,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-095",
        "dimension": 16,
        "vector": [0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44],
        "norm": 1.7864,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-096",
        "dimension": 16,
        "vector": [0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37],
        "norm": 1.7705,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-097",
        "dimension": 16,
        "vector": [-0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3],
        "norm": 1.5113,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-098",
        "dimension": 16,
        "vector": [-0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23],
        "norm": 1.2339,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-099",
        "dimension": 16,
        "vector": [-0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16],
        "norm": 0.9579,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-100",
        "dimension": 16,
        "vector": [-0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09],
        "norm": 0.6853,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-101",
        "dimension": 16,
        "vector": [-0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02],
        "norm": 0.4224,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-102",
        "dimension": 16,
        "vector": [-0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05],
        "norm": 0.2098,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-103",
        "dimension": 16,
        "vector": [-0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12],
        "norm": 0.2577,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-104",
        "dimension": 16,
        "vector": [0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19],
        "norm": 0.4956,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-105",
        "dimension": 16,
        "vector": [0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26],
        "norm": 0.7626,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-106",
        "dimension": 16,
        "vector": [0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33],
        "norm": 1.0365,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-107",
        "dimension": 16,
        "vector": [0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4],
        "norm": 1.313,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-108",
        "dimension": 16,
        "vector": [0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47],
        "norm": 1.5907,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-109",
        "dimension": 16,
        "vector": [0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43],
        "norm": 1.7977,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-110",
        "dimension": 16,
        "vector": [0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36],
        "norm": 1.7497,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-111",
        "dimension": 16,
        "vector": [-0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29],
        "norm": 1.4716,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-112",
        "dimension": 16,
        "vector": [-0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22],
        "norm": 1.1943,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-113",
        "dimension": 16,
        "vector": [-0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15],
        "norm": 0.9187,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-114",
        "dimension": 16,
        "vector": [-0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08],
        "norm": 0.6468,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-115",
        "dimension": 16,
        "vector": [-0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01],
        "norm": 0.3868,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-116",
        "dimension": 16,
        "vector": [-0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
        "norm": 0.1939,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-117",
        "dimension": 16,
        "vector": [-0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13],
        "norm": 0.2871,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-118",
        "dimension": 16,
        "vector": [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2],
        "norm": 0.5329,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-119",
        "dimension": 16,
        "vector": [0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27],
        "norm": 0.8015,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-120",
        "dimension": 16,
        "vector": [0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34],
        "norm": 1.0759,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-121",
        "dimension": 16,
        "vector": [0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41],
        "norm": 1.3526,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-122",
        "dimension": 16,
        "vector": [0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48],
        "norm": 1.6305,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-123",
        "dimension": 16,
        "vector": [0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42],
        "norm": 1.8044,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-124",
        "dimension": 16,
        "vector": [0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35],
        "norm": 1.7241,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-125",
        "dimension": 16,
        "vector": [-0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28],
        "norm": 1.4319,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-126",
        "dimension": 16,
        "vector": [-0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21],
        "norm": 1.1548,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-127",
        "dimension": 16,
        "vector": [-0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14],
        "norm": 0.8795,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-128",
        "dimension": 16,
        "vector": [-0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07],
        "norm": 0.6086,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-129",
        "dimension": 16,
        "vector": [-0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0],
        "norm": 0.3521,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-130",
        "dimension": 16,
        "vector": [-0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07],
        "norm": 0.1855,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-131",
        "dimension": 16,
        "vector": [-0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14],
        "norm": 0.3187,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-132",
        "dimension": 16,
        "vector": [0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21],
        "norm": 0.5706,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-133",
        "dimension": 16,
        "vector": [0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28],
        "norm": 0.8405,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-134",
        "dimension": 16,
        "vector": [0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35],
        "norm": 1.1153,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-135",
        "dimension": 16,
        "vector": [0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42],
        "norm": 1.3923,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-136",
        "dimension": 16,
        "vector": [0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49],
        "norm": 1.6702,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-137",
        "dimension": 16,
        "vector": [0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41],
        "norm": 1.8067,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-138",
        "dimension": 16,
        "vector": [0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34],
        "norm": 1.6933,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-139",
        "dimension": 16,
        "vector": [-0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27],
        "norm": 1.3923,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-140",
        "dimension": 16,
        "vector": [-0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2],
        "norm": 1.1153,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-141",
        "dimension": 16,
        "vector": [-0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13],
        "norm": 0.8405,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-142",
        "dimension": 16,
        "vector": [-0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06],
        "norm": 0.5706,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-143",
        "dimension": 16,
        "vector": [-0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01],
        "norm": 0.3187,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-144",
        "dimension": 16,
        "vector": [-0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08],
        "norm": 0.1855,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-145",
        "dimension": 16,
        "vector": [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15],
        "norm": 0.3521,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-146",
        "dimension": 16,
        "vector": [0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22],
        "norm": 0.6086,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-147",
        "dimension": 16,
        "vector": [0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29],
        "norm": 0.8795,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-148",
        "dimension": 16,
        "vector": [0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36],
        "norm": 1.1548,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-149",
        "dimension": 16,
        "vector": [0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43],
        "norm": 1.4319,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-150",
        "dimension": 16,
        "vector": [0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5],
        "norm": 1.71,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-151",
        "dimension": 16,
        "vector": [0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4],
        "norm": 1.8044,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-152",
        "dimension": 16,
        "vector": [0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33],
        "norm": 1.657,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-153",
        "dimension": 16,
        "vector": [-0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26],
        "norm": 1.3526,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-154",
        "dimension": 16,
        "vector": [-0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19],
        "norm": 1.0759,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-155",
        "dimension": 16,
        "vector": [-0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12],
        "norm": 0.8015,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-156",
        "dimension": 16,
        "vector": [-0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05],
        "norm": 0.5329,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-157",
        "dimension": 16,
        "vector": [-0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02],
        "norm": 0.2871,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-158",
        "dimension": 16,
        "vector": [-0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09],
        "norm": 0.1939,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-159",
        "dimension": 16,
        "vector": [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16],
        "norm": 0.3868,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-160",
        "dimension": 16,
        "vector": [0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23],
        "norm": 0.6468,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-161",
        "dimension": 16,
        "vector": [0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3],
        "norm": 0.9187,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-162",
        "dimension": 16,
        "vector": [0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37],
        "norm": 1.1943,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-163",
        "dimension": 16,
        "vector": [0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44],
        "norm": 1.4716,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-164",
        "dimension": 16,
        "vector": [0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51],
        "norm": 1.7497,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-165",
        "dimension": 16,
        "vector": [0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39],
        "norm": 1.7977,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-166",
        "dimension": 16,
        "vector": [0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32],
        "norm": 1.6149,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-167",
        "dimension": 16,
        "vector": [-0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25],
        "norm": 1.313,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-168",
        "dimension": 16,
        "vector": [-0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18],
        "norm": 1.0365,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-169",
        "dimension": 16,
        "vector": [-0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11],
        "norm": 0.7626,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-170",
        "dimension": 16,
        "vector": [-0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04],
        "norm": 0.4956,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-171",
        "dimension": 16,
        "vector": [-0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03],
        "norm": 0.2577,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-172",
        "dimension": 16,
        "vector": [-0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1],
        "norm": 0.2098,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-173",
        "dimension": 16,
        "vector": [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17],
        "norm": 0.4224,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-174",
        "dimension": 16,
        "vector": [0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24],
        "norm": 0.6853,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-175",
        "dimension": 16,
        "vector": [0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31],
        "norm": 0.9579,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-176",
        "dimension": 16,
        "vector": [0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38],
        "norm": 1.2339,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-177",
        "dimension": 16,
        "vector": [0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45],
        "norm": 1.5113,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-178",
        "dimension": 16,
        "vector": [0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45],
        "norm": 1.7705,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-179",
        "dimension": 16,
        "vector": [0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38],
        "norm": 1.7864,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-180",
        "dimension": 16,
        "vector": [0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31],
        "norm": 1.5666,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-181",
        "dimension": 16,
        "vector": [-0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24],
        "norm": 1.2734,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-182",
        "dimension": 16,
        "vector": [-0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17],
        "norm": 0.9972,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-183",
        "dimension": 16,
        "vector": [-0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1],
        "norm": 0.7239,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-184",
        "dimension": 16,
        "vector": [-0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03],
        "norm": 0.4587,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-185",
        "dimension": 16,
        "vector": [-0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04],
        "norm": 0.2315,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-186",
        "dimension": 16,
        "vector": [-0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11],
        "norm": 0.2315,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-187",
        "dimension": 16,
        "vector": [0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18],
        "norm": 0.4587,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-188",
        "dimension": 16,
        "vector": [0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25],
        "norm": 0.7239,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-189",
        "dimension": 16,
        "vector": [0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32],
        "norm": 0.9972,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-190",
        "dimension": 16,
        "vector": [0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39],
        "norm": 1.2734,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-191",
        "dimension": 16,
        "vector": [0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46],
        "norm": 1.551,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-192",
        "dimension": 16,
        "vector": [0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44],
        "norm": 1.7864,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-193",
        "dimension": 16,
        "vector": [0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37],
        "norm": 1.7705,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-194",
        "dimension": 16,
        "vector": [-0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3],
        "norm": 1.5113,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-195",
        "dimension": 16,
        "vector": [-0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23],
        "norm": 1.2339,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-196",
        "dimension": 16,
        "vector": [-0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16],
        "norm": 0.9579,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-197",
        "dimension": 16,
        "vector": [-0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09],
        "norm": 0.6853,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-198",
        "dimension": 16,
        "vector": [-0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02],
        "norm": 0.4224,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-199",
        "dimension": 16,
        "vector": [-0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05],
        "norm": 0.2098,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-200",
        "dimension": 16,
        "vector": [-0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12],
        "norm": 0.2577,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-201",
        "dimension": 16,
        "vector": [0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19],
        "norm": 0.4956,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-202",
        "dimension": 16,
        "vector": [0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26],
        "norm": 0.7626,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-203",
        "dimension": 16,
        "vector": [0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33],
        "norm": 1.0365,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-204",
        "dimension": 16,
        "vector": [0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4],
        "norm": 1.313,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-205",
        "dimension": 16,
        "vector": [0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47],
        "norm": 1.5907,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-206",
        "dimension": 16,
        "vector": [0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43],
        "norm": 1.7977,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-207",
        "dimension": 16,
        "vector": [0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36],
        "norm": 1.7497,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-208",
        "dimension": 16,
        "vector": [-0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29],
        "norm": 1.4716,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-209",
        "dimension": 16,
        "vector": [-0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22],
        "norm": 1.1943,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-210",
        "dimension": 16,
        "vector": [-0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15],
        "norm": 0.9187,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-211",
        "dimension": 16,
        "vector": [-0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08],
        "norm": 0.6468,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-212",
        "dimension": 16,
        "vector": [-0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01],
        "norm": 0.3868,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-213",
        "dimension": 16,
        "vector": [-0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
        "norm": 0.1939,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-214",
        "dimension": 16,
        "vector": [-0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13],
        "norm": 0.2871,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-215",
        "dimension": 16,
        "vector": [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2],
        "norm": 0.5329,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-216",
        "dimension": 16,
        "vector": [0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27],
        "norm": 0.8015,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-217",
        "dimension": 16,
        "vector": [0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34],
        "norm": 1.0759,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-218",
        "dimension": 16,
        "vector": [0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41],
        "norm": 1.3526,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-219",
        "dimension": 16,
        "vector": [0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48],
        "norm": 1.6305,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-220",
        "dimension": 16,
        "vector": [0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42],
        "norm": 1.8044,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-221",
        "dimension": 16,
        "vector": [0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35],
        "norm": 1.7241,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-17-222",
        "dimension": 16,
        "vector": [-0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28],
        "norm": 1.4319,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-17-223",
        "dimension": 16,
        "vector": [-0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21],
        "norm": 1.1548,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-17-224",
        "dimension": 16,
        "vector": [-0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14],
        "norm": 0.8795,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-17-225",
        "dimension": 16,
        "vector": [-0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07],
        "norm": 0.6086,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-17-226",
        "dimension": 16,
        "vector": [-0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0],
        "norm": 0.3521,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-17-227",
        "dimension": 16,
        "vector": [-0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07],
        "norm": 0.1855,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-17-228",
        "dimension": 16,
        "vector": [-0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14],
        "norm": 0.3187,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-17-229",
        "dimension": 16,
        "vector": [0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21],
        "norm": 0.5706,
        "cluster_label": "cluster_5",
    },
]

