import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from app.models.decision import Decision
from app.models.shipment import Shipment
from app.models.feedback import Feedback
from app.models.analytics_snapshot import AnalyticsSnapshot
from app.schemas.decision import DecisionCreate, DecisionResponse, AnalyticsSummary, FeedbackLog

logger = logging.getLogger(__name__)

def create_decision(db: Session, payload: DecisionCreate) -> Decision:
    """
    Creates a new decision record in the database.
    """
    db_decision = Decision(**payload.model_dump())
    db.add(db_decision)
    db.commit()
    db.refresh(db_decision)
    return db_decision

def get_analytics_summary(db: Session) -> AnalyticsSummary:
    """
    Computes analytics summary for all decisions and saves a daily snapshot.
    """
    decisions = db.query(Decision).all()
    total_decisions = len(decisions)
    
    successful_recommendations = 0
    failed_recommendations = 0
    total_savings = 0.0
    
    for decision in decisions:
        shipment = decision.shipment
        if not shipment:
            continue
            
        actual_cost = shipment.shipping_cost
        actual_delay = shipment.delay_days
        
        predicted_cost = decision.predicted_cost
        predicted_delay = decision.predicted_delay
        
        if actual_cost <= predicted_cost and actual_delay <= predicted_delay:
            successful_recommendations += 1
            savings = predicted_cost - actual_cost
            if savings > 0:
                total_savings += savings
        elif decision.status == "evaluated":
            failed_recommendations += 1
        else:
            if actual_cost > predicted_cost or actual_delay > predicted_delay:
                failed_recommendations += 1
    
    average_savings = total_savings / successful_recommendations if successful_recommendations > 0 else 0.0
    evaluated_total = successful_recommendations + failed_recommendations
    accuracy_percentage = (successful_recommendations / evaluated_total * 100.0) if evaluated_total > 0 else 0.0
    decision_roi = (total_savings / (total_decisions * 100)) * 100 if total_decisions > 0 else 0.0
    
    # Save/Update daily snapshot
    today = date.today()
    snapshot = db.query(AnalyticsSnapshot).filter(AnalyticsSnapshot.snapshot_date == today).first()
    if snapshot:
        snapshot.total_decisions = total_decisions
        snapshot.success_rate = accuracy_percentage
        snapshot.avg_savings = average_savings
        snapshot.roi = decision_roi
    else:
        snapshot = AnalyticsSnapshot(
            snapshot_date=today,
            total_decisions=total_decisions,
            success_rate=accuracy_percentage,
            avg_savings=average_savings,
            roi=decision_roi
        )
        db.add(snapshot)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save snapshot: {e}")

    return AnalyticsSummary(
        total_decisions=total_decisions,
        successful_recommendations=successful_recommendations,
        failed_recommendations=failed_recommendations,
        average_savings=average_savings,
        decision_roi=decision_roi,
        accuracy_percentage=accuracy_percentage
    )

def run_feedback_pipeline(db: Session) -> List[FeedbackLog]:
    """
    Reads pending decisions, compares with shipment actuals, and updates status.
    Saves results to Feedback table and flags for retraining if variance is too high.
    """
    pending_decisions = db.query(Decision).filter(Decision.status == "executed").all()
    logs: List[FeedbackLog] = []
    
    for decision in pending_decisions:
        shipment = decision.shipment
        if not shipment:
            continue
            
        actual_cost = shipment.shipping_cost
        actual_delay = shipment.delay_days
        
        cost_variance = actual_cost - decision.predicted_cost
        delay_variance = actual_delay - decision.predicted_delay
        
        was_successful = (actual_cost <= decision.predicted_cost and actual_delay <= decision.predicted_delay)
        
        needs_retraining = False
        if decision.predicted_cost > 0 and (cost_variance / decision.predicted_cost) > 0.1:
            needs_retraining = True
        if delay_variance > 2:
            needs_retraining = True
            
        decision.status = "evaluated"
        decision.needs_retraining = needs_retraining
        
        # Save to Feedback table
        feedback_entry = Feedback(
            decision_id=decision.id,
            cost_variance=cost_variance,
            delay_variance=delay_variance,
            was_successful=was_successful
        )
        db.add(feedback_entry)
        
        log = FeedbackLog(
            decision_id=decision.id,
            shipment_id=decision.shipment_id,
            cost_variance=cost_variance,
            delay_variance=delay_variance,
            marked_for_retraining=needs_retraining,
            status_updated_to="evaluated"
        )
        logs.append(log)
        
    db.commit()
    return logs

