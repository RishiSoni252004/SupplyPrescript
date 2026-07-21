"""
Pydantic schemas for Shipment request/response validation.

These schemas define the data shapes that the API accepts and returns,
keeping the transport layer separate from the database layer.

Schema hierarchy:
    ShipmentBase  – shared validated fields
    ShipmentCreate(ShipmentBase) – used for POST (all base fields required)
    ShipmentUpdate – used for PUT (all fields optional for partial updates)
    ShipmentResponse(ShipmentBase) – returned to clients with DB-generated fields
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ShipmentBase(BaseModel):
    """
    Shared fields for all Shipment schemas.

    Includes field-level constraints and validators so that invalid data
    is rejected *before* it reaches the database layer.
    """

    shipment_id: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Unique business identifier (e.g., SHP-0001)",
        examples=["SHP-0001"],
    )
    origin: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="City or warehouse of origin",
        examples=["Mumbai"],
    )
    destination: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="City or warehouse of destination",
        examples=["Delhi"],
    )
    shipment_date: datetime = Field(
        ...,
        description="Date the shipment was dispatched",
        examples=["2026-07-20T10:00:00"],
    )
    delivery_date: Optional[datetime] = Field(
        default=None,
        description="Actual delivery date (null if not yet delivered)",
        examples=["2026-07-25T15:30:00"],
    )
    carrier: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Logistics carrier name",
        examples=["BlueDart"],
    )
    weight_kg: float = Field(
        ...,
        gt=0,
        description="Total weight of the shipment in kilograms (must be > 0)",
        examples=[250.5],
    )
    shipping_cost: float = Field(
        ...,
        ge=0,
        description="Cost of shipping in USD (must be >= 0)",
        examples=[1200.00],
    )
    transport_mode: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Mode of transport (e.g., Air, Sea, Road, Rail)",
        examples=["Road"],
    )
    is_delayed: bool = Field(
        default=False,
        description="Whether the shipment was delayed",
    )
    delay_days: int = Field(
        default=0,
        ge=0,
        description="Number of days the shipment was delayed (must be >= 0)",
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional free-text notes about the shipment",
    )

    @field_validator("transport_mode")
    @classmethod
    def validate_transport_mode(cls, value: str) -> str:
        """Ensure transport_mode is one of the accepted values."""
        allowed = {"Air", "Sea", "Road", "Rail"}
        if value not in allowed:
            raise ValueError(
                f"transport_mode must be one of {sorted(allowed)}, got '{value}'"
            )
        return value

    @field_validator("delay_days")
    @classmethod
    def validate_delay_consistency(cls, value: int, info) -> int:
        """If is_delayed is False, delay_days must be 0."""
        is_delayed = info.data.get("is_delayed", False)
        if not is_delayed and value != 0:
            raise ValueError(
                "delay_days must be 0 when is_delayed is False"
            )
        return value


class ShipmentCreate(ShipmentBase):
    """
    Schema for creating a new shipment (POST request body).

    Inherits all validated fields from ShipmentBase.
    """

    pass


class ShipmentUpdate(BaseModel):
    """
    Schema for updating an existing shipment (PUT request body).

    All fields are optional so clients can send partial updates.
    The same validation rules from ShipmentBase apply to any
    fields that *are* provided.
    """

    shipment_id: Optional[str] = Field(
        default=None, min_length=1, max_length=50,
    )
    origin: Optional[str] = Field(
        default=None, min_length=1, max_length=100,
    )
    destination: Optional[str] = Field(
        default=None, min_length=1, max_length=100,
    )
    shipment_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    carrier: Optional[str] = Field(
        default=None, min_length=1, max_length=100,
    )
    weight_kg: Optional[float] = Field(default=None, gt=0)
    shipping_cost: Optional[float] = Field(default=None, ge=0)
    transport_mode: Optional[str] = Field(
        default=None, min_length=1, max_length=50,
    )
    is_delayed: Optional[bool] = None
    delay_days: Optional[int] = Field(default=None, ge=0)
    notes: Optional[str] = Field(default=None, max_length=1000)

    @field_validator("transport_mode")
    @classmethod
    def validate_transport_mode(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        allowed = {"Air", "Sea", "Road", "Rail"}
        if value not in allowed:
            raise ValueError(
                f"transport_mode must be one of {sorted(allowed)}, got '{value}'"
            )
        return value


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
