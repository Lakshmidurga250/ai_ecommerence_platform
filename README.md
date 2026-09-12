# AI E-Commerce & Recommendation Platform

An enterprise-grade, multi-vendor e-commerce marketplace powered by an integrated Machine Learning and Artificial Intelligence pipeline.

The platform combines rich multi-vendor retail operations (Customer, Seller, and Admin workflows) with mathematically grounded AI systems: 5-level recommendation engines, NLP query intent parsing, time-series demand forecasting, K-Means customer RFM segmentation, Isolation Forest anomaly/fraud detection, customer churn prediction, and review sentiment analysis.

---

## Key Capabilities & Features

### 🛍️ E-Commerce & Marketplace Operations
- **Multi-Vendor Ecosystem:** Independent seller storefronts, product lifecycle approval, inventory control, and isolated order management.
- **Transactional Core:** Real-time stock reservation, backend price validation, coupon rule engine, multi-step checkout, and audit-logged payment simulation.
- **Fulfillment & Logistics:** Multi-warehouse inventory movements, shipment tracking with carrier simulation, and return/refund eligibility workflows.
- **Interactive Feedback:** Customer reviews with ratings, review moderation, and customer support ticketing system.

### 🧠 Artificial Intelligence & Machine Learning
- **Multi-Tier Recommendation Engine:**
  - *Level 1:* Bayesian popularity & trending decay scoring.
  - *Level 2:* Content-based filtering via TF-IDF vectorization and cosine similarity.
  - *Level 3:* Collaborative filtering (User-Neighborhood & Item-Neighborhood).
  - *Level 4:* Hybrid weighted ensemble with cold-start resolution.
  - *Level 5:* Neural Latent Matrix Factorization embedding recommendations.
- **AI-Powered Natural Language Search:** Intent parsing, attribute extraction (color, category, max price, min rating), and hybrid lexical (BM25) + semantic vector ranking.
- **Time-Series Demand Forecasting:** Lag features, rolling statistics, baseline vs. Random Forest models evaluating real MAE, RMSE, and MAPE metrics for automated stock reordering.
- **Fraud & Anomaly Detection:** Isolation Forest transaction scoring detecting high-velocity and unusual spending patterns with transparent factor attribution.
- **Customer RFM Segmentation:** Recency, Frequency, Monetary clustering via K-Means with Silhouette score validation.
- **Customer Churn Risk Prediction:** Classification model identifying dormant accounts with retention strategy recommendations.
- **Sentiment Analysis Engine:** Aspect and polarity scoring (-1.0 to +1.0) on customer reviews with confidence metrics.
- **AI Shopping Assistant:** Conversational assistant grounded strictly in actual catalog products.
- **Model Registry & Versioning:** Tracks hyperparameters, dataset versions, training timestamps, and real test metrics.

### 🛡️ Enterprise Security & Observability
- **Role-Based Access Control (RBAC):** Strict JWT token authentication with backend authorization barriers for Customer, Seller, and Admin roles.
- **Audit Logging:** Tamper-evident recording of security, financial, and catalog mutations.
- **Observability:** Prometheus metrics (`/metrics`), structured logging, and health checks.
- **Reliable Fallback Adapters:** Dual-mode architecture supporting full Docker stack (PostgreSQL, Redis, Elasticsearch, MinIO) as well as self-contained standalone execution.

---

## Technology Stack

- **Frontend:** React, TypeScript, Vite, Tailwind CSS, React Router, TanStack Query, Lucide Icons.
- **Backend:** Python, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, Uvicorn, WebSockets.
- **Machine Learning:** Pandas, NumPy, Scikit-Learn, SciPy.
- **Database & Cache:** PostgreSQL (Docker) / SQLite (Standalone fallback), Redis (Docker) / In-Memory cache fallback.
- **Search:** Elasticsearch / BM25 In-Memory ranker fallback.
- **Storage:** MinIO / Local filesystem storage adapter.
- **DevOps & Monitoring:** Docker Compose, Prometheus, Grafana, GitHub Actions.

---

## Quickstart Guide

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- Docker and Docker Compose (optional for local standalone execution)

### 1. Standalone Development Setup

```bash
# Clone the repository
git clone <repo-url>
cd "AI E-Commerce"

# Backend setup
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m scripts.setup.init_db
python -m scripts.seed.seed_all

# Start backend server
uvicorn app.main:app --reload --port 8000
```

```bash
# Frontend setup (in a separate terminal)
cd frontend
npm install
npm run dev
```

The frontend will run at `http://localhost:5173` and the API documentation (Swagger UI) will be accessible at `http://localhost:8000/docs`.

### 2. Docker Compose Deployment

```bash
docker-compose up --build
```

---

## Repository Structure

```
├── frontend/             # React + TypeScript Vite frontend
├── backend/              # FastAPI REST & WebSocket backend
├── ai/                   # Machine learning pipelines & model registry
├── database/             # Schemas, seeds, and migrations
├── infrastructure/       # Docker, Prometheus, Grafana configs
├── scripts/              # Audit, seed, and health verification scripts
├── docs/                 # Architectural and API documentation
└── tests/                # Automated test suites
```

---

## License

Academic / Portfolio Software Engineering Project.
