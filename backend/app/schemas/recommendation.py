from pydantic import BaseModel, Field
from typing import List

class RecommendationRequest(BaseModel):
    """
    Input schema for requesting a business action recommendation.
    """
    predicted_delay_days: int = Field(..., description="Predicted delay for the shipment in days", ge=0)
    budget: float = Field(..., description="Maximum allowed extra budget for mitigation", ge=0)
    priority: str = Field(..., description="Priority level of the shipment (e.g., High, Medium, Low)")
    inventory_level: int = Field(..., description="Current inventory level of the product", ge=0)

class AlternativeOption(BaseModel):
    """
    Schema for an alternative business option.
    """
    name: str = Field(..., description="Name of the alternative option")
    estimated_cost: float = Field(..., description="Estimated cost of this option")
    estimated_delay: int = Field(..., description="Estimated delay in days if this option is chosen")

class RecommendationResponse(BaseModel):
    """
    Output schema containing the best recommended option and alternatives.
    """
    best_option: str = Field(..., description="The recommended action to take")
    estimated_cost: float = Field(..., description="Cost of the best option")
    estimated_delay: int = Field(..., description="Delay of the best option")
    reason: str = Field(..., description="Reasoning for this recommendation")
    alternatives: List[AlternativeOption] = Field(..., description="List of all considered options")
