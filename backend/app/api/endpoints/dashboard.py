"""
API endpoints for the Analytics Dashboard.

Provides read-only analytical views over the shipments data:
    GET /summary              – High-level KPIs
    GET /transport-analysis   – Shipment counts by transport mode
    GET /supplier-analysis    – Shipment counts by supplier (carrier)
    GET /recent-shipments     – Latest 10 shipment records
"""

import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    RecentShipmentsResponse,
    SupplierAnalysisResponse,
    TransportAnalysisResponse,
)
from app.services.dashboard import (
    get_dashboard_summary,
    get_recent_shipments,
    get_supplier_analysis,
    get_transport_analysis,
)

logger = logging.getLogger(__name__)

router = APIRouter()


# ---------------------------------------------------------------------------
# GET /dashboard/summary
# ---------------------------------------------------------------------------
@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get dashboard summary",
    description="Returns high-level KPIs: total shipments, on-time vs delayed "
                "counts, average shipping cost, and average delay days.",
)
def dashboard_summary(
    db: Session = Depends(get_db),
) -> DashboardSummaryResponse:
    """
    Compute and return aggregate shipment KPIs.
    """
    data = get_dashboard_summary(db=db)
    return DashboardSummaryResponse(**data)


# ---------------------------------------------------------------------------
# GET /dashboard/transport-analysis
# ---------------------------------------------------------------------------
@router.get(
    "/transport-analysis",
    response_model=TransportAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Get transport mode analysis",
    description="Returns shipment counts grouped by transport mode "
                "(Air, Sea, Road, Rail), ordered by count descending.",
)
def transport_analysis(
    db: Session = Depends(get_db),
) -> TransportAnalysisResponse:
    """
    Return shipment breakdown by transport mode.
    """
    data = get_transport_analysis(db=db)
    return TransportAnalysisResponse(**data)


# ---------------------------------------------------------------------------
# GET /dashboard/supplier-analysis
# ---------------------------------------------------------------------------
@router.get(
    "/supplier-analysis",
    response_model=SupplierAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Get supplier analysis",
    description="Returns shipment counts grouped by supplier (carrier), "
                "ordered by count descending.",
)
def supplier_analysis(
    db: Session = Depends(get_db),
) -> SupplierAnalysisResponse:
    """
    Return shipment breakdown by supplier (carrier).
    """
    data = get_supplier_analysis(db=db)
    return SupplierAnalysisResponse(**data)


# ---------------------------------------------------------------------------
# GET /dashboard/recent-shipments
# ---------------------------------------------------------------------------
@router.get(
    "/recent-shipments",
    response_model=RecentShipmentsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get recent shipments",
    description="Returns the 10 most recently created shipment records, "
                "ordered by creation timestamp descending.",
)
def recent_shipments(
    db: Session = Depends(get_db),
) -> RecentShipmentsResponse:
    """
    Return the latest 10 shipment records.
    """
    data = get_recent_shipments(db=db, limit=10)
    return RecentShipmentsResponse(**data)
