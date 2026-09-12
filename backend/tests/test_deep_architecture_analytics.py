"""
Test Suite: Deep Architecture & Analytics Subsystems.
Tests Dijkstra shortest-path logistics routing, nearest-neighbor TSP, standardized feature store,
analytical star schema ETL, product knowledge graph, semantic vector search, conversion funnels, and financial forecasting.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.product import Product
from ai.logistics.route_optimizer import LogisticsRouteOptimizer
from ai.feature_store.feature_store import FeatureStore
from ai.knowledge_graph.product_graph import ProductKnowledgeGraph
from ai.search.semantic_search import SemanticVectorSearchEngine
from backend.app.analytics.data_warehouse import DataWarehouseService
from backend.app.services.funnel_analytics_service import FunnelAnalyticsService
from backend.app.services.financial_intelligence_service import FinancialIntelligenceService

client = TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.close()


def test_logistics_dijkstra_route():
    optimizer = LogisticsRouteOptimizer()
    res = optimizer.find_optimal_transit_route(origin_hub="DEL", destination_hub="BLR")
    assert res["origin"] == "DEL"
    assert res["destination"] == "BLR"
    assert res["total_distance_km"] > 0
    assert res["total_transit_hours"] > 0
    assert len(res["route_path"]) >= 2
    assert res["carbon_kg_co2"] > 0
    assert res["algorithm_used"] == "DIJKSTRA_SHORTEST_PATH"


def test_logistics_tsp_sequence():
    optimizer = LogisticsRouteOptimizer()
    stops = ["DEL", "BOM", "BLR", "HYD", "MAA"]
    res = optimizer.optimize_delivery_sequence_tsp(stop_codes=stops)
    assert len(res["optimized_delivery_sequence"]) == len(stops)
    assert res["total_estimated_km"] > 0
    assert res["algorithm"] == "TSP_NEAREST_NEIGHBOR_APPROXIMATION"


def test_feature_store_customer_features(db_session):
    store = FeatureStore(db_session)
    res = store.get_customer_features(user_id=1)
    assert res["feature_view"] == "customer_engagement_features"
    assert "order_count" in res["features"]
    assert "total_spend" in res["features"]
    assert "loyalty_tier" in res["features"]


def test_feature_store_product_features(db_session):
    store = FeatureStore(db_session)
    res = store.get_product_features(product_id=1)
    assert res["feature_view"] == "product_commercial_features"
    assert "price" in res["features"]
    assert "rating" in res["features"]
    assert "quality_score" in res["features"]


def test_data_warehouse_star_schema_sync_and_summary(db_session):
    dw = DataWarehouseService(db_session)
    sync_res = dw.run_etl_sync()
    assert sync_res["status"] == "SUCCESS"
    assert "synced_records" in sync_res

    bi_res = dw.get_executive_bi_summary()
    assert bi_res["warehouse_status"] == "OPERATIONAL_SYNCED"
    assert bi_res["schema_architecture"] == "STAR_SCHEMA"
    assert "kpis" in bi_res
    assert bi_res["kpis"]["total_gross_revenue"] > 0


def test_product_knowledge_graph(db_session):
    graph = ProductKnowledgeGraph(db_session)
    prod = db_session.query(Product).first()
    assert prod is not None

    res = graph.get_product_subgraph(product_id=prod.id)
    assert "error" not in res
    assert res["nodes_count"] > 1
    assert res["edges_count"] > 0
    assert "graph" in res


def test_semantic_vector_search(db_session):
    engine = SemanticVectorSearchEngine(db_session)
    res = engine.semantic_search(query="lightweight laptop for programming", limit=5)
    assert res["total_matches"] >= 0
    assert "results" in res


def test_customer_journey_funnel(db_session):
    service = FunnelAnalyticsService(db_session)
    res = service.calculate_conversion_funnel()
    assert "funnel_summary" in res
    assert "funnel_steps" in res
    assert len(res["funnel_steps"]) == len(FunnelAnalyticsService.FUNNEL_STAGES)
    assert len(res["ai_optimization_recommendations"]) > 0


def test_financial_intelligence_dashboard(db_session):
    service = FinancialIntelligenceService(db_session)
    res = service.get_financial_dashboard()
    assert "financial_kpis" in res
    assert "cost_breakdown" in res
    assert "revenue_forecast_multi_horizon" in res
    assert "payment_methods_performance" in res


def test_api_analytics_endpoints():
    funnel_res = client.get("/api/v1/analytics-v3/funnel")
    assert funnel_res.status_code == 200

    fin_res = client.get("/api/v1/analytics-v3/financial-dashboard")
    assert fin_res.status_code == 200

    route_res = client.post(
        "/api/v1/analytics-v3/logistics/route",
        json={"origin_hub": "DEL", "destination_hub": "BOM"}
    )
    assert route_res.status_code == 200
    assert route_res.json()["origin"] == "DEL"
