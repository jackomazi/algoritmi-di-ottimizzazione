import gurobipy as gp
from gurobipy  import GRB
from gurobipy import quicksum
import numpy as np

model = gp.Model("aerei")

x1 = model.addVar(vtype=GRB.CONTINUOUS, name = "x1")
x2 = model.addVar(vtype=GRB.CONTINUOUS, name = "x2")

model.setObjective(10000*x1 + 25000*x2, sense = GRB.MAXIMIZE)

# vincoli

model.addConstr(10*x1 + 20 * x2 <= 150, "ore_constraint")
model.addConstr(30*x1 + 100 * x2 <= 650, "cost_constraint")

# non negatività
model.addConstr(x1 >= 0, "non_negative_x1")
model.addConstr(x2 >= 0, "non_negative_x2")

model.optimize()

if model.status == GRB.OPTIMAL:
    x1= model.getAttr('x')[0]
    x2= model.getAttr('x')[1]
    print(x1,x2)

# b
model_b = gp.Model("aerei_b")


x1 = model_b.addVar(vtype=GRB.CONTINUOUS, name = "x1")
x2 = model_b.addVar(vtype=GRB.CONTINUOUS, name = "x2")

model_b.setObjective(10000*x1 + 25000*x2, sense = GRB.MAXIMIZE)

# vincoli

model_b.addConstr(10*x1 + 20 * x2 <= 150, "ore_constraint")
model_b.addConstr(30*x1 + 100 * x2 <= 650, "cost_constraint")

# non negatività
model_b.addConstr(x1 >= 0, "non_negative_x1")
model_b.addConstr(x2 >= 0, "non_negative_x2")

model_b.addConstr(x2 == 0)

model_b.optimize()

if model_b.status == GRB.OPTIMAL:
    x1= model_b.getAttr('x')[0]
    x2= model_b.getAttr('x')[1]
    print(x1,x2)


# c
model_c = gp.Model("aerei_c")


x1 = model_c.addVar(vtype=GRB.CONTINUOUS, name = "x1")
x2 = model_c.addVar(vtype=GRB.CONTINUOUS, name = "x2")

model_c.setObjective(10000*x1 + 25000*x2, sense = GRB.MAXIMIZE)

# vincoli

model_c.addConstr(10*x1 + 20 * x2 <= 150, "ore_constraint")
model_c.addConstr(10*x1 + 20 * x2 + 30 * x1 + 100 * x2 == 800, "ore_cost_constraint")

# non negatività
model_c.addConstr(x1 >= 0, "non_negative_x1")
model_c.addConstr(x2 >= 0, "non_negative_x2")

model_c.addConstr(x2 == 0)

model_c.optimize()

if model_c.status == GRB.OPTIMAL:
    x1= model_c.getAttr('x')[0]
    x2= model_c.getAttr('x')[1]
    print(x1,x2)

# d

model_d = gp.Model("aerei_d")
n_var = 4

x = model_d.addMVar(n_var, lb = [0] * n_var, name = "x")
A = np.array([[10, 20, 17, 5],[40,120,72,27], [1,0,0,0] ])

b = np.array([[150, 800, 2]])

# vincoli

ct = model_d.addConstr(A @x <= b)
utile = np.array([[10000, 25000, 15000, 7000]])

model_d.setObjective(utile @ x - 15000, GRB.MAXIMIZE)

model_d.optimize()

x1= model_d.getAttr('x')[0]
x2= model_d.getAttr('x')[1]
x3= model_d.getAttr('x')[2]
x4= model_d.getAttr('x')[3]
print(x1,x2,x3,x4) #x1=0.0 x2=0.0 x3=0.0 x4=29.62962962962963




