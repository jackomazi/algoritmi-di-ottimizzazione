import gurobipy as gp
from gurobipy import GRB

try:
    model = gp.Model("Maximize autovetture vendute")

    # variabili decisionali
    x1 = model.addVar(vtype=GRB.CONTINUOUS, name = "x1")
    x2 = model.addVar(vtype=GRB.CONTINUOUS, name = "x2")
    x3 = model.addVar(vtype=GRB.CONTINUOUS, name = "x3")

    model.setObjective(1000 * x1 + 1500*x2 + 2200*x3, sense=GRB.MAXIMIZE)

    # vincoli
    # ore disponibilità robot
    model.addConstr(20*x1 + 30*x2 + 62*x3 <= 60*8, "robotA_constraint")
    model.addConstr(31*x1 + 42*x2 + 51*x3 <= 60*8, "robotB_constraint")
    model.addConstr(16*x1 + 81*x2 + 10*x3 <= 60*5, "robotC_constraint")

    # max e min di x3 e x1
    model.addConstr(x3 <= 0.2*(x1 + x2 + x3), "lusso_constraint")
    model.addConstr(x1 >= 0.4*(x1 + x2 + x3), "economico_constraint")

    # non negatività
    model.addConstr(x1 >= 0, "non_negative_x1")
    model.addConstr(x2 >= 0, "non_negative_x2")
    model.addConstr(x3 >= 0, "non_negative_x3")

    model.optimize()

    # stampa

    if model.status == GRB.OPTIMAL:
        print("Soluzione ottimale trovata")
        print(f"Autovetture economiche da produrre: {x1.x:.2f}")
        print(f"Autovetture normali da produrre: {x2.x:.2f}")
        print(f"Autovetture di lusso da produrre: {x3.x:.2f}")

        print(f"Incasso totale: € {model.objval:.2f}")
    else:
        print("Il modello non ha trovato una soluzione ottima")

except gp.GurobiError as e:
    print(f"Errore Gurobi: {e}")

except Exception as e:
    print(f"Errore durante l'esecuzione del programma: {e}")

