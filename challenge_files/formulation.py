from gurobipy import Model, GRB

def compute_to_buy(budget, turns, T, resources):
    """

    Parameters:
    - budget (int): Available budget constraint.
    - T_m (int): Minimum required resource constraint.
    - eff (list): List of efficiency coefficients.
    - RA (list): List of resource allocation costs.
    - RU (list): List of resource usages.

    Returns:
    - list: Optimal values of x_r ore none if no feasible solution.
    """
    
    R = len(resources)

    # Create Gurobi model
    model = Model("OptimizationProblem")
    model.setParam('OutputFlag', 0)  # Disable output

    # Define variables: x_r ∈ Z+ (integer variables)
    x = model.addVars(R, T, vtype=GRB.INTEGER, name="x")

    # Set objective: Maximize sum(eff_r * x_r)
    # model.setObjective(sum( * x[r] for r in R), GRB.MAXIMIZE)
    # model.setObjective(sum(RA[r] * x[r] for r in R), GRB.MINIMIZE)

    # Constraints
    for t in range(T):
        model.addConstr(sum(x[r, t] * resources[r]['RA'] for r in R) <= budget, "BudgetConstraint")
    
    for t in range(T):
        model.addConstr(sum(x[r, t_] * resources[r]['RU'] for r in R for t_ in range(t)) >= turns[t][0], "ResourceUsageConstraint")
        model.addConstr(sum(x[r, t_] * resources[r]['RU'] for r in R for t_ in range(t)) <= turns[t][1], "ResourceUsageConstraint")
    
    for t in range(T):
        model.addConstr(sum(x[r, t] for r in R) <= 50, "ItemLimitConstraint")
        
    # for r in R:
    #     model.addConstr(x[r] <= sum(x[r_] for r_ in R if r_ != r), "variabilita")


    # Solve the model
    model.optimize()

    # Extract the solution
    if model.status == GRB.OPTIMAL:
        return [int(x[r].x) for r in R]
    else:
        return None  # No feasible solution