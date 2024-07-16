import gurobipy as gp
from gurobipy import GRB, quicksum

model = gp.Model("Produzione scarpe")

scarpe = ['A', 'B', 'C']
stab = [1, 2, 3, 4, 5]
mat_prime = ['P', 'L', 'S']

# prezzi scarpe
p = {'A': 30, 'B': 55, 'C':40}
#costo materia prima
c = {'P':4.5, 'L':.73, 'S':7}
# quantità spedita in un collo
s = {'P':10, 'L':5, 'S':3}

# quantità di materia prima k per produrre scarpa di tipo i
mp = {('A', 'P'):1, ('B', 'P'):.7 , ('C', 'P'):1.35, ('A', 'L'):.5, ('B', 'L'):.45, ('C', 'L'):.90, ('A', 'S'):1, ('B', 'S'):1, ('C', 'S'):1}
# quantità di scarpe di tipo i producibili da stabilimento k
q = {('A', 1):4,('A', 2):12,('A', 3):3,('A', 4):9,('A', 5):7,('B', 1):2,('B', 2):7,('B', 3):3,('B', 4):14,('B', 5):5,('C', 1):8,('C', 2):3,('C', 3):5,('C', 4):2,('C', 5):9}
# quantità di materie prime k distibuite a j
y = {('P', 1):10, ('L', 1):5, ('S', 1):3,('P', 2):10, ('L', 2):5, ('S', 2):3,('P', 3):10, ('L', 3):5, ('S', 3):3,('P', 4):10, ('L', 4):5, ('S', 4):3, ('P', 5):10, ('L', 5):5, ('S', 5):3}

# x
x = model.addVars(scarpe, stab, name = "x", vtype=GRB.CONTINUOUS)

model.setObjective(quicksum((x[i,j]*p[i]) for i in scarpe for j in stab)-quicksum((c[k]*s[k]*y[k,j]) for k in mat_prime for j in stab), GRB.MAXIMIZE)

model.addConstr(quicksum((c[k]*s[k]*y[k,j]) for k in mat_prime for j in stab) <= 1000, "mat_prime")

model.addConstr(quicksum(x['A', j] for j in stab) >= 5, "scarpaA")

model.addConstr(quicksum(x[i, 1] for i in scarpe) == quicksum(x[i,3] for i in scarpe), "stab13")

for i in scarpe:
    for j in stab:
        model.addConstr(x[i,j] <= q[i, j], "scarpe")

model.addConstr(x['B', 4] >= 2)

for k in mat_prime:
    for j in stab:
        model.addConstr(quicksum((2*x[i, j]*mp[i,k]) for i in scarpe) <= (y[k,j]*s[k]), "boh")


model.optimize()

if model.status == GRB.OPTIMAL:
    print("Soluzione ottima trovata")
    for i in scarpe:
        for j in stab:
            print(f"Scarpa {i} prodotte {x[i,j].x} nello stabilimento {j}")
    print(f"Soluzione ottima: {model.objval:.2f}")
else:
    print("Nessuna soluzione trovata")


