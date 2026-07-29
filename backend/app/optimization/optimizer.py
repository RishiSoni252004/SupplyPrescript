import pulp
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

def optimize_action(options: List[Dict], budget: float, max_delay: int) -> Optional[str]:
    """
    Uses Linear Programming (via PuLP) to find the most cost-effective option 
    that satisfies both the budget and maximum delay constraints.
    
    Args:
        options: List of dictionaries with 'name', 'estimated_cost', 'estimated_delay'
        budget: Maximum budget constraint
        max_delay: Maximum acceptable delay constraint
        
    Returns:
        The name of the optimal option, or None if no feasible solution exists.
    """
    if not options:
        return None
        
    # Define the problem: we want to MINIMIZE cost
    prob = pulp.LpProblem("SupplyChain_Action_Optimization", pulp.LpMinimize)
    
    # Decision variables: Binary variables for each option (0 or 1)
    option_vars = {}
    for idx, opt in enumerate(options):
        var_name = f"Option_{idx}"
        option_vars[idx] = pulp.LpVariable(var_name, cat=pulp.LpBinary)
        
    # Objective Function: Minimize total delay
    prob += pulp.lpSum([options[i]['estimated_delay'] * option_vars[i] for i in range(len(options))]), "Total_Delay"
    
    # Constraint 1: Exactly ONE option must be selected
    prob += pulp.lpSum([option_vars[i] for i in range(len(options))]) == 1, "Exactly_One_Option"
    
    # Constraint 2: Total cost must be within budget
    prob += pulp.lpSum([options[i]['estimated_cost'] * option_vars[i] for i in range(len(options))]) <= budget, "Budget_Constraint"
    
    # Constraint 3: Total delay must be within max_delay
    prob += pulp.lpSum([options[i]['estimated_delay'] * option_vars[i] for i in range(len(options))]) <= max_delay, "Delay_Constraint"
    
    try:
        # Solve the problem
        prob.solve(pulp.PULP_CBC_CMD(msg=False))
        
        # Check status
        if pulp.LpStatus[prob.status] == 'Optimal':
            # Find which option was selected
            for i in range(len(options)):
                if pulp.value(option_vars[i]) == 1.0:
                    return options[i]['name']
        else:
            logger.warning(f"Optimization failed with status: {pulp.LpStatus[prob.status]}")
            
    except Exception as e:
        logger.error(f"Error during optimization: {e}")
                
    return None
