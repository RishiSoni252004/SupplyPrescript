"""
Pydantic response schemas for the Analytics Dashboard endpoints.

Each schema maps to a specific dashboard endpoint response. All schemas
are read-only (no create/update variants) since the dashboard is purely
analytical.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# GET /dashboard/summary
# ---------------------------------------------------------------------------
class DashboardSummaryResponse(BaseModel):
    """
    High-level KPIs computed from the shipments table.
    """

    total_shipments: int = Field(
        ..., description="Total number of shipment records", examples=[120],
    )
    on_time_shipments: int = Field(
        ..., description="Shipments delivered on time (is_delayed=False)", examples=[95],
    )
    delayed_shipments: int = Field(
        ..., description="Shipments that were delayed (is_delayed=True)", examples=[25],
    )
    on_time_percentage: float = Field(
        ..., description="Percentage of shipments delivered on time", examples=[79.17],
    )
    average_shipping_cost: float = Field(
        ..., description="Mean shipping cost across all shipments (USD)", examples=[1450.75],
    )
    average_delay_days: float = Field(
        ...,
        description="Mean delay in days (computed only over delayed shipments, "
                    "0.0 if none are delayed)",
        examples=[3.2],
    )


# ---------------------------------------------------------------------------
# GET /dashboard/transport-analysis
# ---------------------------------------------------------------------------
class TransportModeCount(BaseModel):
    """
    Shipment count for a single transport mode.
    """

    transport_mode: str = Field(
        ..., description="Mode of transport", examples=["Road"],
    )
    count: int = Field(
        ..., description="Number of shipments using this mode", examples=[42],
    )


class TransportAnalysisResponse(BaseModel):
    """
    Breakdown of shipments by transport mode.
    """

    total_shipments: int = Field(
        ..., description="Total shipment count", examples=[120],
    )
    breakdown: list[TransportModeCount] = Field(
        ..., description="Per-mode shipment counts",
    )


# ---------------------------------------------------------------------------
# GET /dashboard/supplier-analysis
# ---------------------------------------------------------------------------
class SupplierCount(BaseModel):
    """
    Shipment count for a single supplier (carrier).
    """

    supplier: str = Field(
        ..., description="Carrier / supplier name", examples=["BlueDart"],
    )
    count: int = Field(
        ..., description="Number of shipments handled by this supplier", examples=[18],
    )


class SupplierAnalysisResponse(BaseModel):
    """
    Breakdown of shipments by supplier (carrier).
    """

    total_suppliers: int = Field(
        ..., description="Number of distinct suppliers", examples=[5],
    )
    breakdown: list[SupplierCount] = Field(
        ..., description="Per-supplier shipment counts",
    )


# ---------------------------------------------------------------------------
# GET /dashboard/recent-shipments
# ---------------------------------------------------------------------------
class RecentShipmentItem(BaseModel):
    """
    Abbreviated shipment record returned in the recent-shipments list.
    """

    id: int
    shipment_id: str
    origin: str
    destination: str
    shipment_date: datetime
    delivery_date: Optional[datetime] = None
    carrier: str
    weight_kg: float
    shipping_cost: float
    transport_mode: str
    is_delayed: bool
    delay_days: int
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RecentShipmentsResponse(BaseModel):
    """
    The latest shipments ordered by creation timestamp (descending).
    """

    count: int = Field(
        ..., description="Number of shipments returned", examples=[10],
    )
    shipments: list[RecentShipmentItem] = Field(
        ..., description="Most recently created shipment records",
    )
