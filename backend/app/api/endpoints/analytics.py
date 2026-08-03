from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database.database import get_db
from app.schemas.decision import DecisionCreate, DecisionResponse, AnalyticsSummary, FeedbackLog
from app.services import analytics as analytics_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/decisions", response_model=DecisionResponse, status_code=status.HTTP_201_CREATED)
def execute_decision(payload: DecisionCreate, db: Session = Depends(get_db)):
    """
    Executes and saves a business decision.
    """
    try:
        return analytics_service.create_decision(db, payload)
    except Exception as e:
        logger.error(f"Error saving decision: {e}")
        raise HTTPException(status_code=500, detail="Could not save decision.")

@router.get("/decisions", response_model=List[DecisionResponse])
def get_decisions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of all executed decisions.
    """
    from app.models.decision import Decision
    return db.query(Decision).order_by(Decision.execution_time.desc()).offset(skip).limit(limit).all()

@router.get("/dashboard", response_model=AnalyticsSummary)
def get_dashboard_analytics(db: Session = Depends(get_db)):
    """
    Retrieves decision analytics summary for the dashboard.
    """
    return analytics_service.get_analytics_summary(db)

@router.post("/feedback", response_model=List[FeedbackLog])
def trigger_feedback_pipeline(db: Session = Depends(get_db)):
    """
    Triggers the feedback pipeline to evaluate executed decisions against actual outcomes.
    """
    try:
        return analytics_service.run_feedback_pipeline(db)
    except Exception as e:
        logger.error(f"Error running feedback pipeline: {e}")
        raise HTTPException(status_code=500, detail="Could not run feedback pipeline.")
