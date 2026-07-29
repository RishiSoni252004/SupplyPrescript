"""
Recommendation Engine that bridges the business request with the mathematical optimizer.
"""
from typing import Dict, Any
import logging

from app.schemas.recommendation import RecommendationRequest, RecommendationResponse, AlternativeOption
from app.optimization.constraints import calculate_max_acceptable_delay, validate_constraints
from app.optimization.optimizer import optimize_action

logger = logging.getLogger(__name__)

def generate_options(predicted_delay_days: int) -> list[Dict[str, Any]]:
    """
    Generates the dynamic list of options based on the predicted delay.
    """
    return [
        {
            "name": "Air Freight",
            "estimated_cost": 15000.0,
            "estimated_delay": 2, # Fixed fast delivery
        },
        {
            "name": "Backup Supplier",
            "estimated_cost": 8000.0,
            "estimated_delay": 5, # Medium delay
        },
        {
            "name": "Delay Product Launch",
            "estimated_cost": 0.0,
            "estimated_delay": predicted_delay_days, # Highest delay, lowest cost
        }
    ]

def get_recommendations(request: RecommendationRequest) -> RecommendationResponse:
    """
    Processes the recommendation request, calculates constraints, runs optimization,
    and returns a structured response.
    """
    # 1. Generate options
    options_data = generate_options(request.predicted_delay_days)
    
    # 2. Calculate dynamic constraints
    max_delay = calculate_max_acceptable_delay(
        priority=request.priority,
        inventory_level=request.inventory_level
    )
    
    logger.info(f"Calculated Max Delay: {max_delay} for Priority: {request.priority}, Inventory: {request.inventory_level}")
    
    # 3. Validate if any options are feasible before running optimizer
    if not validate_constraints(request.budget, max_delay, options_data):
        logger.warning("No feasible options within budget and delay constraints.")
        # Fallback to the cheapest option
        best_opt_name = "Delay Product Launch"
        reason = "Budget and delay constraints could not be met. Defaulted to the lowest cost option."
    else:
        # 4. Run Optimizer
        best_opt_name = optimize_action(options_data, request.budget, max_delay)
        
        if best_opt_name:
            reason = "Meets budget while minimizing delay."
        else:
            # Fallback if optimization fails
            best_opt_name = "Delay Product Launch"
            reason = "Optimization failed to find a valid solution. Defaulted to lowest cost."
            
    # Find the details of the best option
    best_opt_details = next((opt for opt in options_data if opt["name"] == best_opt_name), options_data[2])
    
    # Construct response
    alternatives = [
        AlternativeOption(**opt) for opt in options_data
    ]
    
    return RecommendationResponse(
        best_option=best_opt_name,
        estimated_cost=best_opt_details["estimated_cost"],
        estimated_delay=best_opt_details["estimated_delay"],
        reason=reason,
        alternatives=alternatives
    )
