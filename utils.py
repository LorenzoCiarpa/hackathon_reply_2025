from gurobipy import Model, GRB

def compute_to_buy(budget, T_m, eff, RA, RU):
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
    R = range(len(eff))  # Set of items

    # Create Gurobi model
    model = Model("OptimizationProblem")
    model.setParam('OutputFlag', 0)  # Disable output

    # Define variables: x_r ∈ Z+ (integer variables)
    x = model.addVars(R, vtype=GRB.INTEGER, name="x")

    # Set objective: Maximize sum(eff_r * x_r)
    model.setObjective(sum(eff[r] * x[r] for r in R), GRB.MAXIMIZE)
    # model.setObjective(sum(RA[r] * x[r] for r in R), GRB.MINIMIZE)

    # Constraints
    model.addConstr(sum(x[r] * RA[r] for r in R) <= budget, "BudgetConstraint")
    model.addConstr(sum(x[r] * RU[r] for r in R) >= T_m, "ResourceUsageConstraint")
    model.addConstr(sum(x[r] for r in R) <= 50, "ItemLimitConstraint")

    # Solve the model
    model.optimize()

    # Extract the solution
    if model.status == GRB.OPTIMAL:
        return [int(x[r].x) for r in R]
    else:
        return None  # No feasible solution

def compute_profit(coverage, T_x, T_r, maintenance):
    revenue = min(coverage, T_x) * T_r
    return  revenue - maintenance