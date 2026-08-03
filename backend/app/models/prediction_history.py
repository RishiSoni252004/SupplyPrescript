"""
SQLAlchemy ORM model for PredictionHistory table.

Stores historical ML predictions for auditing and analysis.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base

class PredictionHistory(Base):
    """
    Records a prediction event.
    """
    __tablename__ = "prediction_history"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    shipment_id: int = Column(
        Integer,
        ForeignKey("shipments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key to the shipment"
    )

    predicted_delay_days: float = Column(Float, nullable=False, comment="The predicted delay in days")
    model_version: str = Column(String(50), nullable=False, comment="Version of the ML model used")
    features_json: str = Column(Text, nullable=True, comment="JSON string of the features used for prediction")
    
    created_at: datetime = Column(
        DateTime, default=datetime.utcnow, nullable=False,
        comment="Timestamp when the prediction was made"
    )

    # Relationship
    shipment = relationship("Shipment")

    def __repr__(self) -> str:
        return f"<PredictionHistory(id={self.id}, shipment_id={self.shipment_id}, delay={self.predicted_delay_days})>"
