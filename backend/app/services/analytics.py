import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.decision import Decision
from app.models.shipment import Shipment
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
    Computes analytics summary for all decisions.
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
            
        # Only evaluate if the shipment is considered 'completed' or has actual delay data
        # For simplicity, we assume actual outcome data is present in shipment (shipping_cost, delay_days)
        actual_cost = shipment.shipping_cost
        actual_delay = shipment.delay_days
        
        predicted_cost = decision.predicted_cost
        predicted_delay = decision.predicted_delay
        
        # Determine success
        if actual_cost <= predicted_cost and actual_delay <= predicted_delay:
            successful_recommendations += 1
            savings = predicted_cost - actual_cost
            if savings > 0:
                total_savings += savings
        elif decision.status == "evaluated":
            failed_recommendations += 1
        else:
            # Not evaluated yet, but we have actual data, let's just count based on current data
            if actual_cost > predicted_cost or actual_delay > predicted_delay:
                failed_recommendations += 1
    
    average_savings = total_savings / successful_recommendations if successful_recommendations > 0 else 0.0
    
    evaluated_total = successful_recommendations + failed_recommendations
    accuracy_percentage = (successful_recommendations / evaluated_total * 100.0) if evaluated_total > 0 else 0.0
    
    # ROI: (Savings / Total predicted cost of successful recommendations) * 100
    # For simplicity, we just use arbitrary formula or simple ratio
    decision_roi = (total_savings / (total_decisions * 100)) * 100 if total_decisions > 0 else 0.0  # Placeholder ROI logic

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
    Flags for retraining if variance is too high.
    """
    pending_decisions = db.query(Decision).filter(Decision.status == "executed").all()
    logs: List[FeedbackLog] = []
    
    for decision in pending_decisions:
        shipment = decision.shipment
        if not shipment:
            continue
            
        # Assume actuals are known if shipment is delivered (or we just evaluate based on current data)
        actual_cost = shipment.shipping_cost
        actual_delay = shipment.delay_days
        
        cost_variance = actual_cost - decision.predicted_cost
        delay_variance = actual_delay - decision.predicted_delay
        
        # Logic to mark for retraining
        # E.g., if cost variance > 10% of predicted, or delay variance > 2 days
        needs_retraining = False
        if decision.predicted_cost > 0 and (cost_variance / decision.predicted_cost) > 0.1:
            needs_retraining = True
        if delay_variance > 2:
            needs_retraining = True
            
        decision.status = "evaluated"
        decision.needs_retraining = needs_retraining
        
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
