import gurobipy as gp
from gurobipy import GRB
from gurobipy import quicksum

model = gp.Model("produzione batterie")

impianti = [1,2]
tipi = ['A', 'B','G']

max_rame = 200
max_nickel = 200

prezzi = {'A':45, 'B':40, 'G':30} # prezzi di vendita
cr = 5 # costo rame
cn = 7 # costo nickel

# consumo rame e nickel
r = {('A', 1): 0, ('B', 1): 1, ('G', 1): 2, ('A', 2):0, ('B',2):2, ('G',2): 5}
n = {('A', 1): 2, ('B', 1): 3, ('G', 1): 0, ('A', 2):4, ('B',2):2, ('G',2): 0}

# costi per batteria i fatta da impianto j
c = {('A', 1): 12, ('B', 1): 6, ('G', 1): 4, ('A', 2):8, ('B',2):10, ('G',2): 3}

# capacità produttiva
m = {('A', 1): 30, ('B', 1): 30, ('G', 1): 10, ('A', 2):40, ('B',2):20, ('G',2): 20}

# variabili
x = model.addVars(tipi, impianti, name = "x", vtype=GRB.CONTINUOUS)

# funzione obiettivo
model.setObjective(quicksum(x[i,j] * (prezzi[i] - cr * r[i,j] - cn * n[i,j] - c[i,j]) for i in tipi for j in impianti), GRB.MAXIMIZE)

# constraint
model.addConstr(quicksum(x[i,j] * r[i,j] for i in tipi for j in impianti) <= max_rame, "rame")
model.addConstr(quicksum(x[i,j] * n[i,j] for i in tipi for j in impianti) <= max_nickel, "nickel")

# capacità produttiva batterie
for i in tipi:
    for j in impianti:
        model.addConstr(x[i,j] <= m[i,j],"cap_prod")


# ultimi constraint
model.addConstr(quicksum(x['A',j] for j in impianti) >= 2 * quicksum(x['B',j] for j in impianti))
model.addConstr(quicksum(x['A', j] for j in impianti) <= quicksum(x['G', j] for j in impianti))

model.optimize()

if model.status == GRB.OPTIMAL:
    print("Soluzione ottima trovata")
    for i in tipi:
        for j in impianti:
            print(f"Prodotte {x[i, j].x} scatole di batterie di tipo {i} da impianto {j}")
    print(f"Massimo profitto: € {model.objval:.2f}")
else:
    print("Nessuna soluzione ottima trovata")

    
                       



	
