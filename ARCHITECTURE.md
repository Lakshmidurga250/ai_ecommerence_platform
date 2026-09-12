# Architecture Specification

## 1. Architectural Principles

The platform adheres to modern software engineering best practices:
- **Clean Separation of Concerns:** Clear boundary lines between Presentation (React), API Gateway/Controller (FastAPI), Business Service layer, Data Persistence (SQLAlchemy Repositories), and Machine Learning Engine.
- **Strict Single Source of Truth:** Transactional state (Catalog, Stock, Balances, Orders) resides exclusively in PostgreSQL. Redis acts strictly as a cache, broker, and rate limiter.
- **Fail-Safe Adapters (Rule 85):** All external infrastructure dependencies (PostgreSQL, Redis, Elasticsearch, MinIO, Celery) provide transparent, localized fallback adapters so the application can run in zero-configuration local standalone mode or containerized Docker environments.
- **Zero Hallucination AI Grounding:** AI recommendations, predictions, forecasts, and conversational shopping assistants query real underlying database entities and mathematical models. No predictions or metrics are hard-coded.

---

## 2. Layered Architecture

```
[ Client Applications ]
  │
  ├─ Customer Portal (Storefront, Cart, Checkout, Dashboard)
  ├─ Seller Center (Catalog Management, Orders, Inventory, Forecasts)
  └─ Admin Console (Moderation, System Health, Fraud Alerts, AI Registry)
  │
  ▼
[ API Gateway & Middleware Layer (FastAPI) ]
  │
  ├─ CORS & Security Headers
  ├─ Rate Limiting (Token Bucket / Sliding Window)
  ├─ Prometheus Metrics Instrumentation (/metrics)
  ├─ Audit Trail Interceptor
  └─ JWT Authentication & Role-Based Authorization Guard (RBAC)
  │
  ▼
[ Service & Domain Logic Layer ]
  │
  ├─ AuthService, UserService, RBACService
  ├─ ProductService, CatalogService, CategoryService
  ├─ CartService (Price validation, stock reservation)
  ├─ OrderService, CheckoutService, PaymentSimulationService
  ├─ InventoryService, WarehouseService, ShippingService, ReturnService
  ├─ ReviewService, SentimentService, SupportTicketService
  └─ NotificationService (WebSocket Manager & Push Events)
  │
  ▼
[ Machine Learning & AI Services ]
  │
  ├─ Multi-Level Recommendation Engine (L1 Popularity, L2 Content, L3 CF, L4 Hybrid, L5 Neural)
  ├─ NLP Query Intent Parser & Attribute Extractor
  ├─ Hybrid Search Ranker (BM25 + Semantic Cosine Embedding)
  ├─ Demand Forecasting Service (Time-series Random Forest / MA)
  ├─ Fraud & Transaction Anomaly Service (Isolation Forest)
  ├─ Customer RFM Segmentation Service (K-Means + Silhouette)
  ├─ Churn Prediction Service (Logistic / Random Forest Classifier)
  └─ Model Registry & Evaluation Service
  │
  ▼
[ Storage & Persistence Layer ]
  │
  ├─ PostgreSQL (40+ normalized relational tables)
  ├─ Redis (In-memory caching, rate-limit counters, Celery queue)
  ├─ Elasticsearch (Indexed product search engine)
  └─ MinIO (S3-compatible object storage)
```

---

## 3. Data Flow Workflows

### Customer Purchase & Recommendation Feedback Loop
1. **Browse & Search:** Customer enters search term. NLP query parser extracts category, price range, and attributes.
2. **Dynamic Ranking:** Elasticsearch/BM25 scores products blended with popularity and rating signals.
3. **Behavior Event Logging:** Interaction events (`view`, `click`, `add_to_cart`) are asynchronously recorded to `behavior_events`.
4. **Checkout & Reservation:** Cart items reserve inventory stock with row-level locks. Payment is securely simulated and logged.
5. **Order Lifecycle:** Order transitions from `PENDING` -> `CONFIRMED` -> `SHIPPED` -> `DELIVERED`.
6. **Model Feedback:** Purchase and review events update interaction matrices and retrain recommendation baselines.
