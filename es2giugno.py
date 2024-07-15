import gurobipy as gp
from gurobipy import GRB, quicksum

model = gp.Model("ore collaboratori")

collaboratori = [1, 2,3,4,5,6,7,8,9, 10]
progetti = [1,2,3,4,5]

# disponibilità ore
d = {1:50, 2:35, 3:17, 4:29, 5:12, 6:77, 7:20, 8:51, 9:31, 10:19}
# parcella collaboratori
p = {1:7, 2:3, 3:4, 4:5.2, 5:2.8, 6:6, 7:3.5, 8:4.9, 9:3.2, 10:2.5}
# ore per progetto
o = {1:38, 2:17, 3:21, 4:44, 5:29}

x = model.addVars(collaboratori, progetti, name="x", vtype=GRB.CONTINUOUS)

model.setObjective(quicksum(x[i,j]*p[i] for i in collaboratori for j in progetti), GRB.MINIMIZE)

for j in progetti:
    model.addConstr(quicksum(x[i,j] for i in collaboratori) == o[j], "ore")

for i in collaboratori:
    model.addConstr(quicksum(x[i, j] for j in progetti) <= d[i], "disponibilità")

model.addConstr(quicksum(x[2,j]*p[2] for j in progetti) >= 50, "collab2")

model.addConstr(quicksum(x[5,j]*p[5] for j in progetti) >= 25, "collab5")

model.addConstr(quicksum((x[1,j] + x[3,j] + x[7,j] + x[9,j]) for j in progetti) <= 70, "ore_complessive")

model.addConstr(x[4,2] >= 5, "collab42")
model.addConstr(x[8,3] >= 5, "collab83")

model.optimize()

if model.status == GRB.OPTIMAL:
    print("Soluzione ottima trovata")
    for i in collaboratori:
        for j in progetti:
            print(f"Collaboratore {i} lavora {x[i,j].x} ore su progetto {j}")
    print(f"Soluzione ottima: {model.objval:.2f}")
else:
    print("Nessuna soluzione trovata")


