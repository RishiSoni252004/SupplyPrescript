"""
SQLAlchemy ORM model for AnalyticsSnapshot table.

Stores periodic snapshots of KPI metrics for trend charting.
"""

from datetime import date
from sqlalchemy import Column, Integer, Float, Date

from app.database.database import Base

class AnalyticsSnapshot(Base):
    """
    Records a daily/monthly snapshot of analytics metrics.
    """
    __tablename__ = "analytics_snapshots"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    snapshot_date: date = Column(
        Date, nullable=False, unique=True, index=True,
        comment="Date for this snapshot"
    )

    total_decisions: int = Column(Integer, nullable=False, default=0)
    success_rate: float = Column(Float, nullable=False, default=0.0)
    avg_savings: float = Column(Float, nullable=False, default=0.0)
    roi: float = Column(Float, nullable=False, default=0.0)

    def __repr__(self) -> str:
        return f"<AnalyticsSnapshot(date={self.snapshot_date}, success_rate={self.success_rate})>"
