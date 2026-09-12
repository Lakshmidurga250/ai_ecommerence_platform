"""
V3 Analytics, Architecture & Logistics Routers.
Exposes Funnel Analytics, Financial Intelligence, Data Warehouse Star Schema,
Feature Store, Advanced Logistics Routing, Knowledge Graph, and Semantic Search.
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.expansion_v3 import (
    RouteOptimizationRequest, TSPSequenceRequest, SemanticSearchRequest
)
from app.services.funnel_analytics_service import FunnelAnalyticsService
from app.services.financial_intelligence_service import FinancialIntelligenceService
from app.analytics.data_warehouse import DataWarehouseService
from ai.feature_store.feature_store import FeatureStore
from ai.logistics.route_optimizer import LogisticsRouteOptimizer
from ai.knowledge_graph.product_graph import ProductKnowledgeGraph
from ai.search.semantic_search import SemanticVectorSearchEngine

router = APIRouter(prefix="/analytics-v3", tags=["Analytics & Architecture V3"])


@router.get("/funnel")
def get_customer_journey_funnel(db: Session = Depends(get_db)):
    """
    Returns the multi-stage conversion funnel and primary drop-off bottlenecks.
    """
    service = FunnelAnalyticsService(db)
    return service.calculate_conversion_funnel(db=db)


@router.get("/financial-dashboard")
def get_financial_intelligence_dashboard(db: Session = Depends(get_db)):
    """
    Returns executive financial metrics, unit economics, and 30/60/90-day GMV forecasts.
    """
    service = FinancialIntelligenceService(db)
    return service.get_financial_dashboard(db=db)


@router.get("/data-warehouse/summary")
def get_data_warehouse_summary(db: Session = Depends(get_db)):
    """
    Returns OLAP rollup aggregates across star schema fact and dimension tables.
    """
    service = DataWarehouseService(db)
    return service.get_executive_bi_summary(db=db)


@router.post("/data-warehouse/sync")
def trigger_data_warehouse_etl_sync(db: Session = Depends(get_db)):
    """
    Runs incremental ETL job syncing operational transactions into the star schema.
    """
    service = DataWarehouseService(db)
    return service.run_etl_sync(db=db)


@router.get("/feature-store/customer/{user_id}")
def get_customer_features_vector(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves standardized online feature vector for a customer.
    """
    store = FeatureStore(db)
    return store.get_customer_features(user_id=user_id, db=db)


@router.get("/feature-store/product/{product_id}")
def get_product_features_vector(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieves standardized commercial feature vector for a product.
    """
    store = FeatureStore(db)
    return store.get_product_features(product_id=product_id, db=db)


@router.post("/logistics/route")
def calculate_optimal_fulfillment_route(payload: RouteOptimizationRequest):
    """
    Calculates Dijkstra shortest transit path, transit hours, and carbon emission footprint.
    """
    router_engine = LogisticsRouteOptimizer()
    return router_engine.find_optimal_transit_route(
        origin_hub=payload.origin_hub,
        destination_hub=payload.destination_hub
    )


@router.post("/logistics/tsp-sequence")
def optimize_multi_stop_delivery_tsp(payload: TSPSequenceRequest):
    """
    Calculates optimal delivery sequence using nearest-neighbor TSP approximation.
    """
    router_engine = LogisticsRouteOptimizer()
    return router_engine.optimize_delivery_sequence_tsp(stop_codes=payload.stop_codes)


@router.get("/knowledge-graph/product/{product_id}")
def get_product_knowledge_subgraph(
    product_id: int,
    max_hops: int = Query(2, ge=1, le=3),
    db: Session = Depends(get_db)
):
    """
    Returns knowledge graph neighborhood of a product with category, brand, and companion nodes.
    """
    graph = ProductKnowledgeGraph(db)
    result = graph.get_product_subgraph(product_id=product_id, max_hops=max_hops, db=db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/knowledge-graph/path")
def find_graph_path_between_products(
    source_id: int = Query(...),
    target_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """
    Explains the semantic relationship path between two products in the knowledge graph.
    """
    graph = ProductKnowledgeGraph(db)
    result = graph.find_path_between_entities(product_id_a=source_id, product_id_b=target_id, db=db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/semantic-search")
def execute_semantic_vector_search(
    payload: SemanticSearchRequest,
    db: Session = Depends(get_db)
):
    """
    Executes semantic vector search matching natural language queries against document concept vectors.
    """
    engine = SemanticVectorSearchEngine(db)
    return engine.semantic_search(
        query=payload.query,
        limit=payload.limit or 10,
        min_score=payload.min_score or 0.10,
        db=db
    )
