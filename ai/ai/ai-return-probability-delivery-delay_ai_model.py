"""
AI/ML Engine: ReturnDelayPredictorAIModel
Category: ai
Focus: Category return volatility index, carrier transit delay hazard model, risk attribution
Mathematical solvers, statistical distributions, predictive inference, and optimization heuristics.
"""

import math
import random
import time
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

class ReturnDelayPredictorAIModel:
    """
    High-performance AI model implementation for AI return-probability scoring and transit delivery-delay risk predictor.
    Supports inference, vector representations, drift estimation, and calibration.
    """

    MODEL_NAME: str = 'ai-return-probability-delivery-delay-ai-v3'
    MODEL_VERSION: str = '3.16.0'

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

def get_return_delay_predictor_ai_model() -> ReturnDelayPredictorAIModel:
    return ReturnDelayPredictorAIModel()

# High-Dimensional Feature Embeddings & Quantization Weights
STATIC_NEURAL_WEIGHTS_16 = [
    {
        "node_id": "AI-VEC-16-001",
        "dimension": 16,
        "vector": [-0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23],
        "norm": 1.2339,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-002",
        "dimension": 16,
        "vector": [-0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16],
        "norm": 0.9579,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-003",
        "dimension": 16,
        "vector": [-0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09],
        "norm": 0.6853,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-004",
        "dimension": 16,
        "vector": [-0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02],
        "norm": 0.4224,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-005",
        "dimension": 16,
        "vector": [-0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05],
        "norm": 0.2098,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-006",
        "dimension": 16,
        "vector": [-0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12],
        "norm": 0.2577,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-007",
        "dimension": 16,
        "vector": [0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19],
        "norm": 0.4956,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-008",
        "dimension": 16,
        "vector": [0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26],
        "norm": 0.7626,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-009",
        "dimension": 16,
        "vector": [0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33],
        "norm": 1.0365,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-010",
        "dimension": 16,
        "vector": [0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4],
        "norm": 1.313,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-011",
        "dimension": 16,
        "vector": [0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47],
        "norm": 1.5907,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-012",
        "dimension": 16,
        "vector": [0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43],
        "norm": 1.7977,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-013",
        "dimension": 16,
        "vector": [0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36],
        "norm": 1.7497,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-014",
        "dimension": 16,
        "vector": [-0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29],
        "norm": 1.4716,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-015",
        "dimension": 16,
        "vector": [-0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22],
        "norm": 1.1943,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-016",
        "dimension": 16,
        "vector": [-0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15],
        "norm": 0.9187,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-017",
        "dimension": 16,
        "vector": [-0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08],
        "norm": 0.6468,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-018",
        "dimension": 16,
        "vector": [-0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01],
        "norm": 0.3868,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-019",
        "dimension": 16,
        "vector": [-0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
        "norm": 0.1939,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-020",
        "dimension": 16,
        "vector": [-0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13],
        "norm": 0.2871,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-021",
        "dimension": 16,
        "vector": [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2],
        "norm": 0.5329,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-022",
        "dimension": 16,
        "vector": [0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27],
        "norm": 0.8015,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-023",
        "dimension": 16,
        "vector": [0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34],
        "norm": 1.0759,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-024",
        "dimension": 16,
        "vector": [0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41],
        "norm": 1.3526,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-025",
        "dimension": 16,
        "vector": [0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48],
        "norm": 1.6305,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-026",
        "dimension": 16,
        "vector": [0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42],
        "norm": 1.8044,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-027",
        "dimension": 16,
        "vector": [0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35],
        "norm": 1.7241,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-028",
        "dimension": 16,
        "vector": [-0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28],
        "norm": 1.4319,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-029",
        "dimension": 16,
        "vector": [-0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21],
        "norm": 1.1548,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-030",
        "dimension": 16,
        "vector": [-0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14],
        "norm": 0.8795,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-031",
        "dimension": 16,
        "vector": [-0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07],
        "norm": 0.6086,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-032",
        "dimension": 16,
        "vector": [-0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0],
        "norm": 0.3521,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-033",
        "dimension": 16,
        "vector": [-0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07],
        "norm": 0.1855,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-034",
        "dimension": 16,
        "vector": [-0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14],
        "norm": 0.3187,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-035",
        "dimension": 16,
        "vector": [0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21],
        "norm": 0.5706,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-036",
        "dimension": 16,
        "vector": [0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28],
        "norm": 0.8405,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-037",
        "dimension": 16,
        "vector": [0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35],
        "norm": 1.1153,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-038",
        "dimension": 16,
        "vector": [0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42],
        "norm": 1.3923,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-039",
        "dimension": 16,
        "vector": [0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49],
        "norm": 1.6702,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-040",
        "dimension": 16,
        "vector": [0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41],
        "norm": 1.8067,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-041",
        "dimension": 16,
        "vector": [0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34],
        "norm": 1.6933,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-042",
        "dimension": 16,
        "vector": [-0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27],
        "norm": 1.3923,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-043",
        "dimension": 16,
        "vector": [-0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2],
        "norm": 1.1153,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-044",
        "dimension": 16,
        "vector": [-0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13],
        "norm": 0.8405,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-045",
        "dimension": 16,
        "vector": [-0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06],
        "norm": 0.5706,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-046",
        "dimension": 16,
        "vector": [-0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01],
        "norm": 0.3187,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-047",
        "dimension": 16,
        "vector": [-0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08],
        "norm": 0.1855,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-048",
        "dimension": 16,
        "vector": [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15],
        "norm": 0.3521,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-049",
        "dimension": 16,
        "vector": [0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22],
        "norm": 0.6086,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-050",
        "dimension": 16,
        "vector": [0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29],
        "norm": 0.8795,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-051",
        "dimension": 16,
        "vector": [0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36],
        "norm": 1.1548,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-052",
        "dimension": 16,
        "vector": [0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43],
        "norm": 1.4319,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-053",
        "dimension": 16,
        "vector": [0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5],
        "norm": 1.71,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-054",
        "dimension": 16,
        "vector": [0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4],
        "norm": 1.8044,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-055",
        "dimension": 16,
        "vector": [0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33],
        "norm": 1.657,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-056",
        "dimension": 16,
        "vector": [-0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26],
        "norm": 1.3526,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-057",
        "dimension": 16,
        "vector": [-0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19],
        "norm": 1.0759,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-058",
        "dimension": 16,
        "vector": [-0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12],
        "norm": 0.8015,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-059",
        "dimension": 16,
        "vector": [-0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05],
        "norm": 0.5329,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-060",
        "dimension": 16,
        "vector": [-0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02],
        "norm": 0.2871,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-061",
        "dimension": 16,
        "vector": [-0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09],
        "norm": 0.1939,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-062",
        "dimension": 16,
        "vector": [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16],
        "norm": 0.3868,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-063",
        "dimension": 16,
        "vector": [0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23],
        "norm": 0.6468,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-064",
        "dimension": 16,
        "vector": [0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3],
        "norm": 0.9187,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-065",
        "dimension": 16,
        "vector": [0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37],
        "norm": 1.1943,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-066",
        "dimension": 16,
        "vector": [0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44],
        "norm": 1.4716,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-067",
        "dimension": 16,
        "vector": [0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51],
        "norm": 1.7497,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-068",
        "dimension": 16,
        "vector": [0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39],
        "norm": 1.7977,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-069",
        "dimension": 16,
        "vector": [0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32],
        "norm": 1.6149,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-070",
        "dimension": 16,
        "vector": [-0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25],
        "norm": 1.313,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-071",
        "dimension": 16,
        "vector": [-0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18],
        "norm": 1.0365,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-072",
        "dimension": 16,
        "vector": [-0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11],
        "norm": 0.7626,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-073",
        "dimension": 16,
        "vector": [-0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04],
        "norm": 0.4956,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-074",
        "dimension": 16,
        "vector": [-0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03],
        "norm": 0.2577,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-075",
        "dimension": 16,
        "vector": [-0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1],
        "norm": 0.2098,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-076",
        "dimension": 16,
        "vector": [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17],
        "norm": 0.4224,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-077",
        "dimension": 16,
        "vector": [0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24],
        "norm": 0.6853,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-078",
        "dimension": 16,
        "vector": [0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31],
        "norm": 0.9579,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-079",
        "dimension": 16,
        "vector": [0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38],
        "norm": 1.2339,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-080",
        "dimension": 16,
        "vector": [0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45],
        "norm": 1.5113,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-081",
        "dimension": 16,
        "vector": [0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45],
        "norm": 1.7705,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-082",
        "dimension": 16,
        "vector": [0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38],
        "norm": 1.7864,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-083",
        "dimension": 16,
        "vector": [0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31],
        "norm": 1.5666,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-084",
        "dimension": 16,
        "vector": [-0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24],
        "norm": 1.2734,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-085",
        "dimension": 16,
        "vector": [-0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17],
        "norm": 0.9972,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-086",
        "dimension": 16,
        "vector": [-0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1],
        "norm": 0.7239,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-087",
        "dimension": 16,
        "vector": [-0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03],
        "norm": 0.4587,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-088",
        "dimension": 16,
        "vector": [-0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04],
        "norm": 0.2315,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-089",
        "dimension": 16,
        "vector": [-0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11],
        "norm": 0.2315,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-090",
        "dimension": 16,
        "vector": [0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18],
        "norm": 0.4587,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-091",
        "dimension": 16,
        "vector": [0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25],
        "norm": 0.7239,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-092",
        "dimension": 16,
        "vector": [0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32],
        "norm": 0.9972,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-093",
        "dimension": 16,
        "vector": [0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39],
        "norm": 1.2734,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-094",
        "dimension": 16,
        "vector": [0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46],
        "norm": 1.551,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-095",
        "dimension": 16,
        "vector": [0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44],
        "norm": 1.7864,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-096",
        "dimension": 16,
        "vector": [0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37],
        "norm": 1.7705,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-097",
        "dimension": 16,
        "vector": [-0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3],
        "norm": 1.5113,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-098",
        "dimension": 16,
        "vector": [-0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23],
        "norm": 1.2339,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-099",
        "dimension": 16,
        "vector": [-0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16],
        "norm": 0.9579,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-100",
        "dimension": 16,
        "vector": [-0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09],
        "norm": 0.6853,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-101",
        "dimension": 16,
        "vector": [-0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02],
        "norm": 0.4224,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-102",
        "dimension": 16,
        "vector": [-0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05],
        "norm": 0.2098,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-103",
        "dimension": 16,
        "vector": [-0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12],
        "norm": 0.2577,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-104",
        "dimension": 16,
        "vector": [0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19],
        "norm": 0.4956,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-105",
        "dimension": 16,
        "vector": [0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26],
        "norm": 0.7626,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-106",
        "dimension": 16,
        "vector": [0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33],
        "norm": 1.0365,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-107",
        "dimension": 16,
        "vector": [0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4],
        "norm": 1.313,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-108",
        "dimension": 16,
        "vector": [0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47],
        "norm": 1.5907,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-109",
        "dimension": 16,
        "vector": [0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43],
        "norm": 1.7977,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-110",
        "dimension": 16,
        "vector": [0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36],
        "norm": 1.7497,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-111",
        "dimension": 16,
        "vector": [-0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29],
        "norm": 1.4716,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-112",
        "dimension": 16,
        "vector": [-0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22],
        "norm": 1.1943,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-113",
        "dimension": 16,
        "vector": [-0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15],
        "norm": 0.9187,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-114",
        "dimension": 16,
        "vector": [-0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08],
        "norm": 0.6468,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-115",
        "dimension": 16,
        "vector": [-0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01],
        "norm": 0.3868,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-116",
        "dimension": 16,
        "vector": [-0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
        "norm": 0.1939,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-117",
        "dimension": 16,
        "vector": [-0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13],
        "norm": 0.2871,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-118",
        "dimension": 16,
        "vector": [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2],
        "norm": 0.5329,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-119",
        "dimension": 16,
        "vector": [0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27],
        "norm": 0.8015,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-120",
        "dimension": 16,
        "vector": [0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34],
        "norm": 1.0759,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-121",
        "dimension": 16,
        "vector": [0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41],
        "norm": 1.3526,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-122",
        "dimension": 16,
        "vector": [0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48],
        "norm": 1.6305,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-123",
        "dimension": 16,
        "vector": [0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42],
        "norm": 1.8044,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-124",
        "dimension": 16,
        "vector": [0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35],
        "norm": 1.7241,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-125",
        "dimension": 16,
        "vector": [-0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28],
        "norm": 1.4319,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-126",
        "dimension": 16,
        "vector": [-0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21],
        "norm": 1.1548,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-127",
        "dimension": 16,
        "vector": [-0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14],
        "norm": 0.8795,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-128",
        "dimension": 16,
        "vector": [-0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07],
        "norm": 0.6086,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-129",
        "dimension": 16,
        "vector": [-0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0],
        "norm": 0.3521,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-130",
        "dimension": 16,
        "vector": [-0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07],
        "norm": 0.1855,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-131",
        "dimension": 16,
        "vector": [-0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14],
        "norm": 0.3187,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-132",
        "dimension": 16,
        "vector": [0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21],
        "norm": 0.5706,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-133",
        "dimension": 16,
        "vector": [0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28],
        "norm": 0.8405,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-134",
        "dimension": 16,
        "vector": [0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35],
        "norm": 1.1153,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-135",
        "dimension": 16,
        "vector": [0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42],
        "norm": 1.3923,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-136",
        "dimension": 16,
        "vector": [0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49],
        "norm": 1.6702,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-137",
        "dimension": 16,
        "vector": [0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41],
        "norm": 1.8067,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-138",
        "dimension": 16,
        "vector": [0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34],
        "norm": 1.6933,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-139",
        "dimension": 16,
        "vector": [-0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27],
        "norm": 1.3923,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-140",
        "dimension": 16,
        "vector": [-0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2],
        "norm": 1.1153,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-141",
        "dimension": 16,
        "vector": [-0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13],
        "norm": 0.8405,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-142",
        "dimension": 16,
        "vector": [-0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06],
        "norm": 0.5706,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-143",
        "dimension": 16,
        "vector": [-0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01],
        "norm": 0.3187,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-144",
        "dimension": 16,
        "vector": [-0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08],
        "norm": 0.1855,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-145",
        "dimension": 16,
        "vector": [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15],
        "norm": 0.3521,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-146",
        "dimension": 16,
        "vector": [0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22],
        "norm": 0.6086,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-147",
        "dimension": 16,
        "vector": [0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29],
        "norm": 0.8795,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-148",
        "dimension": 16,
        "vector": [0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36],
        "norm": 1.1548,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-149",
        "dimension": 16,
        "vector": [0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43],
        "norm": 1.4319,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-150",
        "dimension": 16,
        "vector": [0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5],
        "norm": 1.71,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-151",
        "dimension": 16,
        "vector": [0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4],
        "norm": 1.8044,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-152",
        "dimension": 16,
        "vector": [0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33],
        "norm": 1.657,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-153",
        "dimension": 16,
        "vector": [-0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26],
        "norm": 1.3526,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-154",
        "dimension": 16,
        "vector": [-0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19],
        "norm": 1.0759,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-155",
        "dimension": 16,
        "vector": [-0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12],
        "norm": 0.8015,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-156",
        "dimension": 16,
        "vector": [-0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05],
        "norm": 0.5329,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-157",
        "dimension": 16,
        "vector": [-0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02],
        "norm": 0.2871,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-158",
        "dimension": 16,
        "vector": [-0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09],
        "norm": 0.1939,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-159",
        "dimension": 16,
        "vector": [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16],
        "norm": 0.3868,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-160",
        "dimension": 16,
        "vector": [0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23],
        "norm": 0.6468,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-161",
        "dimension": 16,
        "vector": [0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3],
        "norm": 0.9187,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-162",
        "dimension": 16,
        "vector": [0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37],
        "norm": 1.1943,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-163",
        "dimension": 16,
        "vector": [0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44],
        "norm": 1.4716,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-164",
        "dimension": 16,
        "vector": [0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51],
        "norm": 1.7497,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-165",
        "dimension": 16,
        "vector": [0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39],
        "norm": 1.7977,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-166",
        "dimension": 16,
        "vector": [0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32],
        "norm": 1.6149,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-167",
        "dimension": 16,
        "vector": [-0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25],
        "norm": 1.313,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-168",
        "dimension": 16,
        "vector": [-0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18],
        "norm": 1.0365,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-169",
        "dimension": 16,
        "vector": [-0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11],
        "norm": 0.7626,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-170",
        "dimension": 16,
        "vector": [-0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04],
        "norm": 0.4956,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-171",
        "dimension": 16,
        "vector": [-0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03],
        "norm": 0.2577,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-172",
        "dimension": 16,
        "vector": [-0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1],
        "norm": 0.2098,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-173",
        "dimension": 16,
        "vector": [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17],
        "norm": 0.4224,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-174",
        "dimension": 16,
        "vector": [0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24],
        "norm": 0.6853,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-175",
        "dimension": 16,
        "vector": [0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31],
        "norm": 0.9579,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-176",
        "dimension": 16,
        "vector": [0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38],
        "norm": 1.2339,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-177",
        "dimension": 16,
        "vector": [0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45],
        "norm": 1.5113,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-178",
        "dimension": 16,
        "vector": [0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45],
        "norm": 1.7705,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-179",
        "dimension": 16,
        "vector": [0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38],
        "norm": 1.7864,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-180",
        "dimension": 16,
        "vector": [0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31],
        "norm": 1.5666,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-181",
        "dimension": 16,
        "vector": [-0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24],
        "norm": 1.2734,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-182",
        "dimension": 16,
        "vector": [-0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17],
        "norm": 0.9972,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-183",
        "dimension": 16,
        "vector": [-0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1],
        "norm": 0.7239,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-184",
        "dimension": 16,
        "vector": [-0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03],
        "norm": 0.4587,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-185",
        "dimension": 16,
        "vector": [-0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04],
        "norm": 0.2315,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-186",
        "dimension": 16,
        "vector": [-0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11],
        "norm": 0.2315,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-187",
        "dimension": 16,
        "vector": [0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18],
        "norm": 0.4587,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-188",
        "dimension": 16,
        "vector": [0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25],
        "norm": 0.7239,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-189",
        "dimension": 16,
        "vector": [0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32],
        "norm": 0.9972,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-190",
        "dimension": 16,
        "vector": [0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39],
        "norm": 1.2734,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-191",
        "dimension": 16,
        "vector": [0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46],
        "norm": 1.551,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-192",
        "dimension": 16,
        "vector": [0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44],
        "norm": 1.7864,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-193",
        "dimension": 16,
        "vector": [0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37],
        "norm": 1.7705,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-194",
        "dimension": 16,
        "vector": [-0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3],
        "norm": 1.5113,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-195",
        "dimension": 16,
        "vector": [-0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23],
        "norm": 1.2339,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-196",
        "dimension": 16,
        "vector": [-0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16],
        "norm": 0.9579,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-197",
        "dimension": 16,
        "vector": [-0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09],
        "norm": 0.6853,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-198",
        "dimension": 16,
        "vector": [-0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02],
        "norm": 0.4224,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-199",
        "dimension": 16,
        "vector": [-0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05],
        "norm": 0.2098,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-200",
        "dimension": 16,
        "vector": [-0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12],
        "norm": 0.2577,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-201",
        "dimension": 16,
        "vector": [0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19],
        "norm": 0.4956,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-202",
        "dimension": 16,
        "vector": [0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26],
        "norm": 0.7626,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-203",
        "dimension": 16,
        "vector": [0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33],
        "norm": 1.0365,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-204",
        "dimension": 16,
        "vector": [0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4],
        "norm": 1.313,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-205",
        "dimension": 16,
        "vector": [0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47],
        "norm": 1.5907,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-206",
        "dimension": 16,
        "vector": [0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43],
        "norm": 1.7977,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-207",
        "dimension": 16,
        "vector": [0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36],
        "norm": 1.7497,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-208",
        "dimension": 16,
        "vector": [-0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29],
        "norm": 1.4716,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-209",
        "dimension": 16,
        "vector": [-0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22],
        "norm": 1.1943,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-210",
        "dimension": 16,
        "vector": [-0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15],
        "norm": 0.9187,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-211",
        "dimension": 16,
        "vector": [-0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08],
        "norm": 0.6468,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-212",
        "dimension": 16,
        "vector": [-0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01],
        "norm": 0.3868,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-213",
        "dimension": 16,
        "vector": [-0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
        "norm": 0.1939,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-214",
        "dimension": 16,
        "vector": [-0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13],
        "norm": 0.2871,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-215",
        "dimension": 16,
        "vector": [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2],
        "norm": 0.5329,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-216",
        "dimension": 16,
        "vector": [0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27],
        "norm": 0.8015,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-217",
        "dimension": 16,
        "vector": [0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34],
        "norm": 1.0759,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-218",
        "dimension": 16,
        "vector": [0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41],
        "norm": 1.3526,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-219",
        "dimension": 16,
        "vector": [0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48],
        "norm": 1.6305,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-220",
        "dimension": 16,
        "vector": [0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42],
        "norm": 1.8044,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-221",
        "dimension": 16,
        "vector": [0.47, 0.48, 0.49, 0.5, 0.51, -0.45, -0.44, -0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35],
        "norm": 1.7241,
        "cluster_label": "cluster_5",
    },
    {
        "node_id": "AI-VEC-16-222",
        "dimension": 16,
        "vector": [-0.43, -0.42, -0.41, -0.4, -0.39, -0.38, -0.37, -0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28],
        "norm": 1.4319,
        "cluster_label": "cluster_6",
    },
    {
        "node_id": "AI-VEC-16-223",
        "dimension": 16,
        "vector": [-0.36, -0.35, -0.34, -0.33, -0.32, -0.31, -0.3, -0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21],
        "norm": 1.1548,
        "cluster_label": "cluster_7",
    },
    {
        "node_id": "AI-VEC-16-224",
        "dimension": 16,
        "vector": [-0.29, -0.28, -0.27, -0.26, -0.25, -0.24, -0.23, -0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14],
        "norm": 0.8795,
        "cluster_label": "cluster_0",
    },
    {
        "node_id": "AI-VEC-16-225",
        "dimension": 16,
        "vector": [-0.22, -0.21, -0.2, -0.19, -0.18, -0.17, -0.16, -0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07],
        "norm": 0.6086,
        "cluster_label": "cluster_1",
    },
    {
        "node_id": "AI-VEC-16-226",
        "dimension": 16,
        "vector": [-0.15, -0.14, -0.13, -0.12, -0.11, -0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0],
        "norm": 0.3521,
        "cluster_label": "cluster_2",
    },
    {
        "node_id": "AI-VEC-16-227",
        "dimension": 16,
        "vector": [-0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07],
        "norm": 0.1855,
        "cluster_label": "cluster_3",
    },
    {
        "node_id": "AI-VEC-16-228",
        "dimension": 16,
        "vector": [-0.01, 0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14],
        "norm": 0.3187,
        "cluster_label": "cluster_4",
    },
    {
        "node_id": "AI-VEC-16-229",
        "dimension": 16,
        "vector": [0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21],
        "norm": 0.5706,
        "cluster_label": "cluster_5",
    },
]

