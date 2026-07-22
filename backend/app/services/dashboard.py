"""
Service layer for Analytics Dashboard queries.

Contains pure data-access functions that run aggregation queries against
the shipments table.  Each function returns a plain dictionary that the
endpoint handler passes directly into the corresponding Pydantic schema.
"""

import logging

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.shipment import Shipment

logger = logging.getLogger(__name__)


def get_dashboard_summary(db: Session) -> dict:
    """
    Compute high-level KPIs from the shipments table.

    Returns a dict with keys matching ``DashboardSummaryResponse``:
        - total_shipments
        - on_time_shipments
        - delayed_shipments
        - on_time_percentage
        - average_shipping_cost
        - average_delay_days
    """
    total: int = db.query(func.count(Shipment.id)).scalar() or 0

    if total == 0:
        logger.info("Dashboard summary requested — no shipments in database")
        return {
            "total_shipments": 0,
            "on_time_shipments": 0,
            "delayed_shipments": 0,
            "on_time_percentage": 0.0,
            "average_shipping_cost": 0.0,
            "average_delay_days": 0.0,
        }

    delayed: int = (
        db.query(func.count(Shipment.id))
        .filter(Shipment.is_delayed.is_(True))
        .scalar()
        or 0
    )
    on_time: int = total - delayed

    avg_cost: float = (
        db.query(func.avg(Shipment.shipping_cost)).scalar() or 0.0
    )

    avg_delay: float = (
        db.query(func.avg(Shipment.delay_days))
        .filter(Shipment.is_delayed.is_(True))
        .scalar()
        or 0.0
    )

    on_time_pct: float = round((on_time / total) * 100, 2) if total else 0.0

    logger.info(
        "Dashboard summary: total=%d on_time=%d delayed=%d avg_cost=%.2f avg_delay=%.2f",
        total, on_time, delayed, avg_cost, avg_delay,
    )

    return {
        "total_shipments": total,
        "on_time_shipments": on_time,
        "delayed_shipments": delayed,
        "on_time_percentage": round(on_time_pct, 2),
        "average_shipping_cost": round(float(avg_cost), 2),
        "average_delay_days": round(float(avg_delay), 2),
    }


def get_transport_analysis(db: Session) -> dict:
    """
    Group shipments by ``transport_mode`` and return counts.

    Returns a dict with keys matching ``TransportAnalysisResponse``:
        - total_shipments
        - breakdown  (list of {transport_mode, count})
    """
    rows = (
        db.query(
            Shipment.transport_mode,
            func.count(Shipment.id).label("count"),
        )
        .group_by(Shipment.transport_mode)
        .order_by(func.count(Shipment.id).desc())
        .all()
    )

    breakdown = [
        {"transport_mode": mode, "count": count}
        for mode, count in rows
    ]
    total = sum(item["count"] for item in breakdown)

    logger.info("Transport analysis: %d modes, %d total shipments", len(breakdown), total)

    return {
        "total_shipments": total,
        "breakdown": breakdown,
    }


def get_supplier_analysis(db: Session) -> dict:
    """
    Group shipments by ``carrier`` (supplier) and return counts.

    Returns a dict with keys matching ``SupplierAnalysisResponse``:
        - total_suppliers
        - breakdown  (list of {supplier, count})
    """
    rows = (
        db.query(
            Shipment.carrier,
            func.count(Shipment.id).label("count"),
        )
        .group_by(Shipment.carrier)
        .order_by(func.count(Shipment.id).desc())
        .all()
    )

    breakdown = [
        {"supplier": carrier, "count": count}
        for carrier, count in rows
    ]

    logger.info("Supplier analysis: %d distinct suppliers", len(breakdown))

    return {
        "total_suppliers": len(breakdown),
        "breakdown": breakdown,
    }


def get_recent_shipments(db: Session, limit: int = 10) -> dict:
    """
    Return the most recently created shipment records.

    Args:
        db: Active database session.
        limit: Maximum number of records to return (default 10).

    Returns a dict with keys matching ``RecentShipmentsResponse``:
        - count
        - shipments  (list of Shipment ORM instances)
    """
    shipments = (
        db.query(Shipment)
        .order_by(Shipment.created_at.desc())
        .limit(limit)
        .all()
    )

    logger.info("Recent shipments: returning %d records", len(shipments))

    return {
        "count": len(shipments),
        "shipments": shipments,
    }
