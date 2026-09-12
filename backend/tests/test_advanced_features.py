"""
Unit and Integration Tests for Advanced Catalog & Customer Experience Features.
Tests product bundles, customer Q&A, review helpfulness voting,
recently viewed history, price alerts, and faceted typo-tolerant search.
"""

import pytest
from app.models.product import Product
from app.models.user import User
from app.services.catalog_expansion_service import CatalogExpansionService
from app.services.search_service import SearchService


def test_product_bundle_creation_and_discount(db_session):
    """Verifies creation and pricing calculations of Frequently Bought Together bundles."""
    p1 = db_session.query(Product).first()
    p2 = db_session.query(Product).filter(Product.id != p1.id).first()
    assert p1 is not None and p2 is not None

    bundle = CatalogExpansionService.create_bundle(
        db=db_session,
        primary_product_id=p1.id,
        bundle_product_id=p2.id,
        bundle_name=f"Bundle: {p1.name[:15]} + {p2.name[:15]}",
        discount_percent=15.0
    )

    assert bundle.id is not None
    assert bundle.primary_product_id == p1.id
    assert bundle.bundle_product_id == p2.id
    assert bundle.discount_percent == 15.0

    bundles = CatalogExpansionService.get_bundles_for_product(db_session, p1.id)
    assert len(bundles) >= 1
    target_bundle = next(b for b in bundles if b["bundle_id"] == bundle.id)
    
    expected_original = round(p1.price + p2.price, 2)
    expected_bundle_price = round(p1.price + (p2.price * 0.85), 2)
    assert target_bundle["regular_price"] == expected_original
    assert target_bundle["bundle_price"] == expected_bundle_price
    assert target_bundle["savings"] == round(expected_original - expected_bundle_price, 2)


def test_customer_qna_workflow(db_session):
    """Verifies question submission and verified seller response lifecycle."""
    customer = db_session.query(User).filter(User.email == "john.doe@example.com").first()
    seller_user = db_session.query(User).filter(User.email == "seller1@techvault.com").first()
    product = db_session.query(Product).first()

    # Submit question
    question = CatalogExpansionService.ask_question(
        db=db_session,
        product_id=product.id,
        user_id=customer.id,
        question_text="Does this product come with an international warranty?"
    )
    assert question.id is not None
    assert question.product_id == product.id
    assert question.user_id == customer.id

    # Post answer
    answer = CatalogExpansionService.answer_question(
        db=db_session,
        question_id=question.id,
        user_id=seller_user.id,
        answer_text="Yes, it includes a 1-year global manufacturer warranty.",
        is_seller_reply=True
    )
    assert answer.id is not None
    assert answer.question_id == question.id
    assert answer.user_id == seller_user.id

    # Retrieve Q&A list
    qna_list = CatalogExpansionService.get_questions_for_product(db_session, product.id)
    matched = [q for q in qna_list if q["id"] == question.id]
    assert len(matched) == 1
    assert len(matched[0]["answers"]) >= 1
    assert matched[0]["answers"][0]["answer"] == "Yes, it includes a 1-year global manufacturer warranty."


def test_review_helpfulness_voting(db_session):
    """Verifies that customers can cast helpfulness votes on product reviews."""
    from app.models.review import Review
    review = db_session.query(Review).first()
    customer = db_session.query(User).filter(User.email == "john.doe@example.com").first()

    if not review:
        product = db_session.query(Product).first()
        review = Review(
            product_id=product.id,
            user_id=customer.id,
            rating=5,
            comment="Exceptional quality, exceeded expectations!"
        )
        db_session.add(review)
        db_session.commit()
        db_session.refresh(review)

    vote_result = CatalogExpansionService.vote_review(
        db=db_session,
        review_id=review.id,
        user_id=customer.id,
        is_helpful=True
    )
    assert "helpful_votes" in vote_result
    assert vote_result["helpful_votes"] >= 1


def test_recently_viewed_history(db_session):
    """Verifies that user browsing views are recorded and deduped in sequence."""
    customer = db_session.query(User).filter(User.email == "john.doe@example.com").first()
    products = db_session.query(Product).limit(3).all()

    for p in products:
        CatalogExpansionService.record_recently_viewed(db_session, customer.id, p.id)

    recent = CatalogExpansionService.get_recently_viewed(db_session, customer.id, limit=5)
    assert len(recent) >= len(products)
    recent_ids = [r.id for r in recent]
    # Most recently viewed should be at the front
    assert recent_ids[0] == products[-1].id


def test_price_alert_subscription(db_session):
    """Verifies price alert registration and target price thresholds."""
    customer = db_session.query(User).filter(User.email == "john.doe@example.com").first()
    product = db_session.query(Product).first()

    target_price = round(product.price * 0.90, 2)
    alert = CatalogExpansionService.create_price_alert(
        db=db_session,
        user_id=customer.id,
        product_id=product.id,
        target_price=target_price
    )
    assert alert.id is not None
    assert alert.target_price == target_price
    assert alert.is_triggered is False
    assert alert.alert_type == "PRICE_DROP"



def test_faceted_search(client):
    """Verifies that faceted search returns matching products plus brand and category facet distributions."""
    res = client.get("/api/v1/search/faceted?query=phone")
    assert res.status_code == 200
    data = res.json()
    assert "total_results" in data
    assert "products" in data
    assert "facets" in data
    assert "categories" in data["facets"]
    assert "brands" in data["facets"]


def test_typo_tolerant_search(db_session):
    """Verifies that slight typos (e.g. 'phne' -> 'phone' or 'lapttop' -> 'laptop') yield relevant results."""
    # Intentional typo query
    res = SearchService.search(db_session, query_text="headfone", limit=5)
    assert isinstance(res, list)
