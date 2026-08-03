"""
SQLAlchemy ORM model for the Decision table.

Stores executed recommendations and is used later in the feedback pipeline
to compare predicted outcomes with actual outcomes.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Decision(Base):
    """
    Decision database model.

    Records the option selected for a shipment, along with predicted cost and delay.
    """

    __tablename__ = "decisions"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)

    shipment_id: int = Column(
        Integer,
        ForeignKey("shipments.id"),
        nullable=False,
        index=True,
        comment="Foreign key to the shipment this decision applies to",
    )

    selected_option: str = Column(String(100), nullable=False, comment="The option selected by the user/system")
    predicted_cost: float = Column(Float, nullable=False, comment="Predicted cost of the selected option")
    predicted_delay: float = Column(Float, nullable=False, comment="Predicted delay (days) of the selected option")
    
    execution_time: datetime = Column(
        DateTime, default=datetime.utcnow, nullable=False,
        comment="Timestamp when the decision was executed",
    )
    
    user_notes: str | None = Column(String(500), nullable=True, comment="Optional user notes or justification for the decision")
    
    status: str = Column(String(50), nullable=False, default="executed", comment="Status of the decision (e.g., executed, evaluated)")
    needs_retraining: bool = Column(Boolean, default=False, nullable=False, comment="Flag indicating if the prediction was inaccurate enough to require retraining")

    # Relationship to shipment
    shipment = relationship("Shipment", backref="decisions")

    def __repr__(self) -> str:
        return (
            f"<Decision(id={self.id}, shipment_id={self.shipment_id}, "
            f"selected_option='{self.selected_option}', status='{self.status}')>"
        )
