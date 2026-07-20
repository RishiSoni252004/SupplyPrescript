"""
SQLAlchemy ORM model for the Shipment table.

Represents a single supply-chain shipment record with fields for
tracking origin, destination, shipping details, and delay status.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text

from app.database.database import Base


class Shipment(Base):
    """
    Shipment database model.

    Stores all relevant attributes of a supply-chain shipment, including
    logistics metadata and delay information that will later be used
    by the ML prediction pipeline.
    """

    __tablename__ = "shipments"

    # --- Primary Key ---
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # --- Shipment Identification ---
    shipment_id: str = Column(
        String(50), unique=True, nullable=False, index=True,
        comment="Unique business identifier for the shipment (e.g., SHP-0001)",
    )

    # --- Origin / Destination ---
    origin: str = Column(String(100), nullable=False, comment="City or warehouse of origin")
    destination: str = Column(String(100), nullable=False, comment="City or warehouse of destination")

    # --- Shipment Details ---
    shipment_date: datetime = Column(
        DateTime, nullable=False, comment="Date the shipment was dispatched",
    )
    delivery_date: datetime | None = Column(
        DateTime, nullable=True, comment="Actual delivery date (null if not yet delivered)",
    )
    carrier: str = Column(String(100), nullable=False, comment="Logistics carrier name")
    weight_kg: float = Column(Float, nullable=False, comment="Total weight of the shipment in kilograms")
    shipping_cost: float = Column(Float, nullable=False, comment="Cost of shipping in USD")
    transport_mode: str = Column(
        String(50), nullable=False,
        comment="Mode of transport (e.g., Air, Sea, Road, Rail)",
    )

    # --- Delay Information ---
    is_delayed: bool = Column(
        Boolean, default=False, nullable=False,
        comment="Whether the shipment was delayed beyond its expected window",
    )
    delay_days: int = Column(
        Integer, default=0, nullable=False,
        comment="Number of days the shipment was delayed",
    )

    # --- Metadata ---
    notes: str | None = Column(Text, nullable=True, comment="Optional free-text notes about the shipment")
    created_at: datetime = Column(
        DateTime, default=datetime.utcnow, nullable=False,
        comment="Timestamp when this record was created",
    )
    updated_at: datetime = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False,
        comment="Timestamp when this record was last updated",
    )

    def __repr__(self) -> str:
        return (
            f"<Shipment(id={self.id}, shipment_id='{self.shipment_id}', "
            f"origin='{self.origin}', destination='{self.destination}', "
            f"is_delayed={self.is_delayed})>"
        )
