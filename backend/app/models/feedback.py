"""
SQLAlchemy ORM model for Feedback table.

Stores explicit user/system feedback on decisions for closed-loop analytics.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base

class Feedback(Base):
    """
    Records feedback for a specific decision.
    """
    __tablename__ = "feedback"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    decision_id: int = Column(
        Integer,
        ForeignKey("decisions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key to the decision being evaluated"
    )

    cost_variance: float = Column(Float, nullable=False, default=0.0, comment="Actual cost - Predicted cost")
    delay_variance: float = Column(Float, nullable=False, default=0.0, comment="Actual delay - Predicted delay")
    was_successful: bool = Column(Boolean, nullable=False, default=False, comment="Whether the decision is considered successful")
    
    created_at: datetime = Column(
        DateTime, default=datetime.utcnow, nullable=False,
        comment="Timestamp when the feedback was generated"
    )

    # Relationship
    decision = relationship("Decision", backref="feedbacks")

    def __repr__(self) -> str:
        return f"<Feedback(id={self.id}, decision_id={self.decision_id}, success={self.was_successful})>"
