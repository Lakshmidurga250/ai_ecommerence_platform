# System Audit V2: Baseline Architecture & Capabilities

**Audit Timestamp:** 2026-09-12T13:15:00Z  
**Platform:** AI-Powered Multi-Vendor E-Commerce Platform V2  
**Operating Environment:** Windows 10/11 / Python 3.14 / Node.js v20+ / SQLite 3 (`ecommerce.db`) / React 18 + Vite  

---

## 1. Verified Quantitative Baseline

| Measurement Area | Baseline Value | Method of Verification |
| :--- | :---: | :--- |
| **Total Source LOC** | **18,840 LOC** | `python scripts/audit/audit_codebase.py` |
| **Backend Core & API Services** | **6,563 LOC** (84 files) | Python line counter excluding `venv`/cache |
| **AI / Machine Learning Modules** | **1,572 LOC** (13 files) | Python line counter (`ai/` directory) |
| **Database Models & Migrations** | **4,581 LOC** (8 files) | SQLAlchemy models & Alembic env |
| **Frontend (React / TypeScript)** | **5,051 LOC** (29 files) | `src/` directory line counter |
| **Automated Test Suite** | **1,073 LOC** (10 files) | `backend/tests/` directory line counter |
| **Active Catalog Products** | **216 unique products** | Database count (`Product.is_active == True`) |
| **Categories** | **9 categories** | Database count (18 to 26 items per category) |
| **Brands** | **29 brands** | Database count (Apple, Samsung, Sony, Nike, etc.) |
| **Marketplace Sellers** | **15 merchants** | Database count (`Seller` records) |
| **Regional Warehouses** | **3 fulfillment centers** | WH-BLR-01, WH-MUM-02, WH-DEL-03 |
| **Total Network Stock** | **26,419 units** | Sum of `Inventory.quantity` |
| **Enriched Customer Reviews** | **94 reviews** | Database count (100% scored via SentimentAnalyzer) |
| **Frequently Bought Together Bundles**| **11 bundles** | `ProductBundle` database records |
| **Community Q&A Pairs** | **15 threads** | `ProductQuestion` and `ProductAnswer` records |
| **Relational Database Tables** | **49 tables** | SQLAlchemy `Base.metadata.tables` |
| **FastAPI OpenAPI Paths** | **85 unique paths** | `app.openapi()["paths"]` |
| **Automated Test Results** | **80 / 80 passed (100%)** | `python -m pytest backend/tests/ -v` |
| **Pydantic v2 Deprecation Warnings** | **0 warnings** | All schemas use `ConfigDict(from_attributes=True)` |
| **Frontend Build Status** | **0 errors (Success)** | `npm.cmd run build` (1,523 modules bundled) |

---

## 2. Active AI / ML Engine Inventory

1. **Neural Collaborative Filtering (`ai/recommendations/neural_cf.py`)**: PyTorch NeuMF deep learning dual-branch model (GMF + MLP) with Adam optimizer and binary cross-entropy loss.
2. **Offline Recommendation Evaluator (`ai/recommendations/evaluator.py`)**: Precision@K, Recall@K, MAP@K, NDCG@K, HitRate@K.
3. **Hybrid & Content-Based Recommendation (`ai/recommendations/hybrid.py`)**: Feature similarity matrix and cosine similarity.
4. **Sentiment Analyzer (`ai/sentiment/analyzer.py`)**: Mathematical lexicon-based polarity score (-1.0 to +1.0) and aspect extractor.
5. **Demand Forecaster (`ai/forecasting/demand_forecaster.py`)**: Scikit-Learn RandomForest time-series regression with MAE/RMSE calculation.
6. **Isolation Forest Fraud Detector (`ai/fraud/detector.py`)**: Unsupervised anomaly scoring (0–100) with outlier explanation.
7. **3-Layer Layered Fraud Shield (`ai/fraud/layered_shield.py`)**: Deterministic rules + transaction velocity + Isolation Forest anomaly scoring.
8. **Customer CLV & RFM Cohorts (`ai/customer_intelligence/clv_cohorts.py`)**: Historical CLV + predictive 12-month CLV with retail loyalty tiers (`VIP_PLATINUM`, `LOYAL_GOLD`, etc.).
9. **Statistical Inventory Replenishment (`ai/inventory_intelligence/replenishment.py`)**: Safety Stock, Reorder Point (ROP), and Wilson Economic Order Quantity (EOQ).
10. **Query Intent Parser (`ai/search/intent_parser.py`)**: Natural language query attribute and entity extraction.
11. **Grounded AI Support Assistant (`backend/app/services/ai_support_service.py`)**: Live order tracking, return eligibility checking, sentiment triage.

---

## 3. Database Schema Overview (49 Relational Tables)

- **Identity & Access Management (5 tables):** `users`, `roles`, `user_roles`, `user_profiles`, `addresses`
- **Merchant Management (2 tables):** `sellers`, `seller_profiles`
- **Product Catalog & Hierarchy (5 tables):** `categories`, `brands`, `products`, `product_variants`, `product_images`
- **Inventory & Fulfillment (3 tables):** `warehouses`, `inventories`, `inventory_movements`
- **Shopping Cart & Promotions (6 tables):** `carts`, `cart_items`, `wishlists`, `wishlist_items`, `coupons`, `coupon_usages`
- **Orders, Payments & Shipping (8 tables):** `orders`, `order_items`, `payments`, `shipments`, `shipment_events`, `returns`, `return_items`, `seller_payouts`
- **Reviews & Community Intelligence (6 tables):** `reviews`, `review_sentiments`, `review_helpfulness_votes`, `product_questions`, `product_answers`, `product_bundles`
- **Customer Experience & Alerts (3 tables):** `user_recently_viewed`, `price_alerts`, `inventory_ledgers`
- **Support & Audit (3 tables):** `support_tickets`, `support_messages`, `audit_logs`
- **Analytics & ML Inferences (8 tables):** `behavior_events`, `search_events`, `recommendation_logs`, `demand_forecasts`, `fraud_alerts`, `customer_segments`, `churn_predictions`, `model_registry`

---

## 4. Expansion Plan for V2 Platform

The V2 expansion introduces 18 integrated priorities:
1. **Core Database Models**: Add `platform_expansion_v2.py` declaring A/B testing, loyalty, dynamic pricing, smart logistics, and MLOps drift models.
2. **AI Shopping Agent**: Intent classification, budget understanding, cart-aware recommendations, side-by-side product comparisons, and action pills.
3. **AI Visual Search**: Color/category vector extraction and cosine similarity image search.
4. **Advanced Recommendation Pipeline**: Candidate generation -> feature engineering -> scoring -> business rules -> MMR diversity -> final ranking.
5. **AI Review Intelligence**: Automated pros/cons extraction, aspect scores, and suspicious review detection.
6. **Customer 360 & Churn**: Profile aggregation, churn risk scoring, and automated retention action recommendations.
7. **Demand & Inventory Intelligence**: Multi-horizon forecasting (7/30/90 days) and ABC/XYZ inventory matrix.
8. **Seller Intelligence**: Dynamic pricing elasticity recommendations and revenue simulation.
9. **Fraud Intelligence Center**: Admin fraud operations with explainable 0–100 composite scoring.
10. **Smart Logistics & Returns**: Proximity warehouse selection, delivery ETA prediction, and return reason classification.
11. **Unified Event Tracking**: High-throughput behavioral event collector.
12. **MLOps Platform**: Model lifecycle management, evaluation benchmarks, and drift detection.
13. **A/B Testing Infrastructure**: Deterministic traffic splitting, metric tracking, and lift calculation.
14. **Loyalty & Smart Promotions**: Point accrual, tier progression, and dynamic coupon eligibility.
15. **Testing Expansion**: Target 150+ passing tests across backend, AI, and integration workflows.
