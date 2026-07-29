"""
This module defines the dynamic business constraints for the Optimization Engine.
"""

def calculate_max_acceptable_delay(priority: str, inventory_level: int) -> int:
    """
    Calculates the maximum acceptable delay in days based on priority and inventory level.
    
    Logic:
    - High priority: Base delay of 2 days
    - Medium priority: Base delay of 5 days
    - Low priority: Base delay of 10 days
    
    Inventory padding: Every 10 units of inventory buys 1 extra day of acceptable delay.
    """
    priority_map = {
        "High": 2,
        "Medium": 5,
        "Low": 10
    }
    
    # Default to Medium if priority is unknown
    base_delay = priority_map.get(priority.capitalize(), 5)
    
    # Inventory padding: e.g., 30 inventory = 3 extra days
    inventory_padding = int(inventory_level / 10)
    
    max_delay = base_delay + inventory_padding
    return max_delay

def validate_constraints(budget: float, max_delay: int, options: list) -> bool:
    """
    Validates if there is at least one option that satisfies the absolute constraints.
    Returns True if feasible, False otherwise.
    """
    for opt in options:
        if opt['estimated_cost'] <= budget and opt['estimated_delay'] <= max_delay:
            return True
    return False
