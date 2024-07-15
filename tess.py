from gurobipy import Model, GRB, quicksum

# Create a new model
model = Model("battery_production")

# Sets
plants = [1, 2]
battery_types = ['A', 'B', 'G']

# Parameters
prices = {'A': 45, 'B': 40, 'G': 30}
copper_cost = 5
nickel_cost = 7

copper_consumption = {
    ('A', 1): 0, ('A', 2): 0,
    ('B', 1): 1, ('B', 2): 2,
    ('G', 1): 2, ('G', 2): 5
}

nickel_consumption = {
    ('A', 1): 2, ('A', 2): 4,
    ('B', 1): 3, ('B', 2): 2,
    ('G', 1): 0, ('G', 2): 0
}

labor_costs = {
    ('A', 1): 12, ('A', 2): 8,
    ('B', 1): 6, ('B', 2): 10,
    ('G', 1): 4, ('G', 2): 3
}

production_capacity = {
    ('A', 1): 30, ('A', 2): 40,
    ('B', 1): 30, ('B', 2): 20,
    ('G', 1): 10, ('G', 2): 20
}

max_copper = 200
max_nickel = 200

# Variables
x = model.addVars(battery_types, plants, name="x", vtype=GRB.CONTINUOUS, lb=0)

# Objective function
model.setObjective(
    quicksum(x[i, j] * (prices[i] - labor_costs[i, j] - copper_cost * copper_consumption[i, j] - nickel_cost * nickel_consumption[i, j])
             for i in battery_types for j in plants), GRB.MAXIMIZE)

# Constraints
# Copper constraint
model.addConstr(quicksum(x[i, j] * copper_consumption[i, j] for i in battery_types for j in plants) <= max_copper, "Copper")

# Nickel constraint
model.addConstr(quicksum(x[i, j] * nickel_consumption[i, j] for i in battery_types for j in plants) <= max_nickel, "Nickel")

# Production capacity constraints
for i in battery_types:
    for j in plants:
        model.addConstr(x[i, j] <= production_capacity[i, j], f"Cap_{i}_{j}")

# Relationship constraints
model.addConstr(quicksum(x['A', j] for j in plants) >= 2 * quicksum(x['B', j] for j in plants), "Double_B")
model.addConstr(quicksum(x['A', j] for j in plants) <= quicksum(x['G', j] for j in plants), "A_less_equal_G")

# Optimize the model
model.optimize()

# Output the results
if model.status == GRB.OPTIMAL:
    print("Optimal solution found:")
    for i in battery_types:
        for j in plants:
            print(f"Produce {x[i, j].x} boxes of battery type {i} in plant {j}")
    print(f"Maximum profit: {model.objVal}")
else:
    print("No optimal solution found.")
