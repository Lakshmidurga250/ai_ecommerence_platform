"""
Unified Event Tracking & Ingestion Platform.
Ingests real-time behavioral user events:
product_view, search, cart_add, cart_remove, wishlist_add,
checkout_start, purchase, review, return, recommendation_click, ai_query.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.models.analytics import BehaviorEvent


class EventTrackingService:
    """
    High-throughput event collector service persisting behavioral signals for ML features and analytics.
    """

    ALLOWED_EVENT_TYPES = [
        "product_view",
        "page_view",
        "search",
        "cart_add",
        "cart_remove",
        "wishlist_add",
        "wishlist_remove",
        "checkout_start",
        "purchase",
        "review",
        "return",
        "recommendation_impression",
        "recommendation_click",
        "ai_query"
    ]

    @classmethod
    def record_event(
        cls,
        db: Session,
        event_type: str,
        user_id: Optional[int] = None,
        session_id: Optional[str] = None,
        product_id: Optional[int] = None,
        category_id: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> BehaviorEvent:
        """
        Validates and records a single behavioral event.
        """
        normalized_type = event_type.lower().strip()
        if normalized_type not in cls.ALLOWED_EVENT_TYPES:
            normalized_type = "other"

        event = BehaviorEvent(
            user_id=user_id,
            session_id=session_id or "anonymous",
            event_type=normalized_type.upper(),
            product_id=product_id,
            category_id=category_id,
            event_metadata=metadata or {}
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @classmethod
    def record_batch(
        cls,
        db: Session,
        events: List[Dict[str, Any]]
    ) -> int:
        """
        Batch records multiple client-side events in a single transaction.
        """
        count = 0
        for ev in events:
            ev_type = ev.get("event_type", "other").lower().strip()
            db.add(BehaviorEvent(
                user_id=ev.get("user_id"),
                session_id=ev.get("session_id", "anonymous"),
                event_type=ev_type.upper(),
                product_id=ev.get("product_id"),
                category_id=ev.get("category_id"),
                event_metadata=ev.get("metadata", {})
            ))
            count += 1

        db.commit()
        return count

    @classmethod
    def get_event_metrics_summary(cls, db: Session) -> Dict[str, Any]:
        """
        Returns count breakdown by event type for operational dashboards.
        """
        counts = db.query(
            BehaviorEvent.event_type,
            func.count(BehaviorEvent.id)
        ).group_by(BehaviorEvent.event_type).all()

        total = sum(c[1] for c in counts)
        breakdown_dict = {c[0]: c[1] for c in counts}
        return {
            "total_events": total,
            "total_events_recorded": total,
            "breakdown": breakdown_dict,
            "events_by_type": breakdown_dict
        }
