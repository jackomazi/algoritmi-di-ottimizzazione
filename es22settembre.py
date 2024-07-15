import gurobipy as gp
from gurobipy import GRB

try:
    model = gp.Model("Maximize autovetture vendute")

    # variabili decisionali
    x11 = model.addVar(vtype=GRB.CONTINUOUS, name = "x11")
    x12 = model.addVar(vtype=GRB.CONTINUOUS, name = "x12")
    x13 = model.addVar(vtype=GRB.CONTINUOUS, name = "x13")
    x21 = model.addVar(vtype=GRB.CONTINUOUS, name = "x21")
    x22 = model.addVar(vtype=GRB.CONTINUOUS, name = "x22")
    x23 = model.addVar(vtype=GRB.CONTINUOUS, name = "x23")
    x31 = model.addVar(vtype=GRB.CONTINUOUS, name = "x31")
    x32 = model.addVar(vtype=GRB.CONTINUOUS, name = "x32")
    x33 = model.addVar(vtype=GRB.CONTINUOUS, name = "x33")
 

    model.setObjective(1000 * (x11 + x21 + x31) + 1500 * (x12 + x22 + x32) + 2200 * (x13 + x23 + x33), sense=GRB.MAXIMIZE)

    # vincoli
    # ore disponibilità robot
    model.addConstr(20*x11 + 30*x12 + 62*x13 <= 60*8, "robotA_constraint")
    model.addConstr(31*x21 + 42*x22 + 51*x23 <= 60*8, "robotB_constraint")
    model.addConstr(16*x31 + 81*x32 + 10*x33 <= 60*5, "robotC_constraint")

    # max e min di x3 e x1
    model.addConstr(x13 + x23 + x33 <= 0.2*(x11 + x12 + x13 + x21 + x22 + x23 + x31 + x32 + x33), "lusso_constraint")
    model.addConstr(x11 + x21 + x31 >= 0.4*(x11 + x12 + x13 + x21 + x22 + x23 + x31 + x32 + x33), "economica_constraint")

    # non negatività
    model.addConstr(x11 >= 0, "non_negative_x11")
    model.addConstr(x12 >= 0, "non_negative_x12")
    model.addConstr(x13 >= 0, "non_negative_x13")
    model.addConstr(x21 >= 0, "non_negative_x21")
    model.addConstr(x22 >= 0, "non_negative_x22")
    model.addConstr(x23 >= 0, "non_negative_x23")
    model.addConstr(x31 >= 0, "non_negative_x31")
    model.addConstr(x32 >= 0, "non_negative_x32")
    model.addConstr(x33 >= 0, "non_negative_x33")

    model.optimize()

    # stampa

    if model.status == GRB.OPTIMAL:
        print("Soluzione ottimale trovata")
        print(f"Autovetture economiche da produrre A: {x11.x:.2f}")
        print(f"Autovetture normali da produrre B: {x12.x:.2f}")
        print(f"Autovetture di lusso da produrre C: {x13.x:.2f}")
        print(f"Autovetture economiche da produrre A: {x21.x:.2f}")
        print(f"Autovetture normali da produrre B: {x22.x:.2f}")
        print(f"Autovetture di lusso da produrre C {x23.x:.2f}")
        print(f"Autovetture economiche da produrre A: {x31.x:.2f}")
        print(f"Autovetture normali da produrre B: {x32.x:.2f}")
        print(f"Autovetture di lusso da produrre C: {x33.x:.2f}")

        print(f"Incasso totale: € {model.objval:.2f}")
    else:
        print("Il modello non ha trovato una soluzione ottima")

except gp.GurobiError as e:
    print(f"Errore Gurobi: {e}")

except Exception as e:
    print(f"Errore durante l'esecuzione del programma: {e}")
