"""
Unit and Mathematical Verification Tests for Neural Collaborative Filtering & Recommendation Evaluator.
Validates PyTorch / NumPy dual-branch NeuMF training, loss progression,
and rigorous mathematical metrics (NDCG@K, Recall@K, MAP@K, HitRate@K, Precision@K).
"""

import pytest
import math
from ai.recommendations.neural_cf import NeuralCFEngine, HAS_TORCH
from ai.recommendations.evaluator import RecommendationEvaluator


def test_neural_cf_training_and_inference():
    """Verifies that NeuralCFEngine builds user/item index embeddings, executes forward pass, and infers rankings."""
    engine = NeuralCFEngine(latent_dim_gmf=8, latent_dim_mlp=16)

    # Multi-user, multi-product interaction matrix
    interactions = [
        (1, 101, 1.0), (1, 102, 1.0), (1, 103, 0.8),
        (2, 101, 1.0), (2, 104, 1.0), (2, 105, 0.9),
        (3, 102, 1.0), (3, 103, 1.0), (3, 106, 0.7),
        (4, 104, 1.0), (4, 105, 1.0), (4, 106, 1.0),
    ]

    fit_result = engine.fit(interactions, epochs=3, batch_size=4, learning_rate=0.01)
    assert engine.is_trained is True
    assert fit_result["num_users"] == 4
    assert fit_result["num_items"] == 6
    assert fit_result["samples_trained"] > 0
    assert "final_loss" in fit_result

    # Inference test
    candidates = [101, 102, 103, 104, 105, 106]
    recs = engine.predict_user_recommendations(user_id=1, candidate_product_ids=candidates, limit=3)
    assert len(recs) == 3
    # Check sorted descending by affinity score
    for i in range(len(recs) - 1):
        assert recs[i][1] >= recs[i + 1][1]


def test_evaluator_precision_and_recall_at_k():
    """Mathematically verifies Precision@K and Recall@K calculation."""
    recommended = [101, 102, 103, 104, 105]
    actual = [102, 104, 108]  # 2 hits out of 5 recommended, out of 3 total relevant

    # K = 5
    p5 = RecommendationEvaluator.precision_at_k(recommended, actual, k=5)
    r5 = RecommendationEvaluator.recall_at_k(recommended, actual, k=5)

    assert p5 == round(2 / 5, 4)  # 0.4
    assert r5 == round(2 / 3, 4)  # 0.6667

    # K = 2 (first 2 items [101, 102] contains 1 hit [102])
    p2 = RecommendationEvaluator.precision_at_k(recommended, actual, k=2)
    assert p2 == 0.5


def test_evaluator_hit_rate_at_k():
    """Verifies binary HitRate@K calculation."""
    recommended = [1, 2, 3, 4, 5]
    assert RecommendationEvaluator.hit_rate_at_k(recommended, [3, 9], k=5) == 1.0
    assert RecommendationEvaluator.hit_rate_at_k(recommended, [8, 9], k=5) == 0.0


def test_evaluator_map_at_k():
    """Verifies Mean Average Precision at K with positional relevance weights."""
    recommended = [101, 102, 103, 104]  # Hits at pos 1 (index 0) and pos 3 (index 2)
    actual = [101, 103]

    # pos 1: precision = 1/1
    # pos 2: 102 not in actual
    # pos 3: precision = 2/3
    # AP = (1.0 + 2/3) / 2 = 1.6667 / 2 = 0.8333
    ap = RecommendationEvaluator.average_precision_at_k(recommended, actual, k=4)
    assert ap == round((1.0 + (2.0 / 3.0)) / 2.0, 4)


def test_evaluator_ndcg_at_k():
    """Verifies Normalized Discounted Cumulative Gain with logarithmic discount."""
    recommended = [101, 102, 103]  # 101 hit, 102 hit
    actual = [101, 102]

    # Perfect ranking NDCG@2 should equal 1.0
    ndcg = RecommendationEvaluator.ndcg_at_k(recommended, actual, k=2)
    assert ndcg == 1.0

    # Sub-optimal ranking: hit at rank 2 only
    rec_suboptimal = [999, 101]
    ndcg_sub = RecommendationEvaluator.ndcg_at_k(rec_suboptimal, [101], k=2)
    # DCG = 1 / log2(2 + 1) = 1 / 1.585 = 0.6309
    # IDCG = 1 / log2(1 + 1) = 1.0
    # NDCG = 0.6309
    assert ndcg_sub < 1.0
    assert ndcg_sub > 0.60


def test_evaluator_full_benchmark():
    """Verifies full benchmark generation across multiple users and recommendation models."""
    evaluator = RecommendationEvaluator()

    ground_truth = {
        1: [10, 20, 30],
        2: [40, 50],
        3: [60, 70, 80]
    }

    dummy_model_recs = {
        1: [10, 99, 20, 88, 77],
        2: [40, 50, 11, 22, 33],
        3: [12, 14, 16, 18, 20]
    }

    metrics = evaluator.evaluate_model("TestModel", dummy_model_recs, ground_truth, k_values=[3, 5])
    assert metrics["model_name"] == "TestModel"
    assert "metrics" in metrics
    assert "Precision@3" in metrics["metrics"]
    assert "Recall@3" in metrics["metrics"]
    assert "NDCG@3" in metrics["metrics"]
    assert "MAP@3" in metrics["metrics"]
    assert "HitRate@3" in metrics["metrics"]
