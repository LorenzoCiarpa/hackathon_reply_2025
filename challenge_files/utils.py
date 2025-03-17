def compute_profit(coverage, T_x, T_r, maintenance):
    revenue = min(coverage, T_x) * T_r
    return  revenue - maintenance