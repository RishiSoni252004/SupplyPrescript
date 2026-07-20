"""
Pydantic schemas for Shipment request/response validation.

These schemas define the data shapes that the API accepts and returns,
keeping the transport layer separate from the database layer.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ShipmentBase(BaseModel):
    """
    Shared fields for all Shipment schemas.
    """
    shipment_id: str
    origin: str
    destination: str
    shipment_date: datetime
    delivery_date: datetime | None = None
    carrier: str
    weight_kg: float
    shipping_cost: float
    transport_mode: str
    is_delayed: bool = False
    delay_days: int = 0
    notes: str | None = None


class ShipmentResponse(ShipmentBase):
    """
    Schema returned to clients when reading Shipment records.

    Includes the database-generated `id` and timestamp fields.
    Uses `model_config` with `from_attributes=True` so Pydantic can
    read data directly from SQLAlchemy model instances.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
