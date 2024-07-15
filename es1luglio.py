import gurobipy as gp
from gurobipy import GRB

try:
    model = gp.Model("Maximize cucine")

    # variabili decisionali
    x1 = model.addVar(vtype=GRB.CONTINUOUS, name = "x1")
    x2 = model.addVar(vtype=GRB.CONTINUOUS, name = "x2")
    x3 = model.addVar(vtype=GRB.CONTINUOUS, name = "x3")
    
    # funzione obiettivo
    model.setObjective((4000 - 1500) * x1 + (7500 - 2500) * x2 + (5000 - 2000) * x3 - 150 - 125, sense=GRB.MAXIMIZE)

    # vincoli
    # disponibilità di tavole m^2
    model.addConstr(24 * x1 + 27 * x2 + 23 * x3 <= 800, "tavole_constraint")
    # cucine minime
    model.addConstr(x1 >= 4, "cucinaA_constraint")
    model.addConstr(x2 >= 5, "cucinaB_constraint")
    model.addConstr(x3 >= 6, "cucinaC_constraint")

    # ore per reparto
    model.addConstr(20 * x1 + 30 * x2 + 25 * x3 <= 20 * 60, "taglio_constraint")
    model.addConstr(10 * x1 + 15 * x2 + 10 * x3 <= 18 * 60, "verniciatura_constraint")
    model.addConstr(8 * x1 + 12 * x2 + 15 * x3 <= 22 * 60, "montaggio_constraint")
    
    model.addConstr(x1 >= 0, "non_negative_x1")
    model.addConstr(x2 >= 0, "non_negative_x2")
    model.addConstr(x3 >= 0, "non_negative_x3")
    
    model.optimize()

    # stampa della soluzione ottimale

    if model.status == GRB.OPTIMAL:
        print("Soluzione ottimale trovata")
        print(f"Cucine di tipo A da produrre: {x1.x:.2f}")
        print(f"Cucine di tipo B da produrre: {x2.x:.2f}")
        print(f"Cucine di tipo C da produrre: {x3.x:.2f}")

        print(f"Incasso totale: € {model.objval:.2f}")
    else:
        print("Il modello non ha trovato una soluzione ottimale.")

except gp.GurobiError as e:
    print(f"Errore Gurobi: {e}")
    
except Exception as e:
    print(f"Errore durante l'esecuzione del programma: {e}")
print("VERSIONE CON VARIABILI DISCRETE")

try:
    model = gp.Model("Maximize cucine")

    # variabili decisionali
    x1 = model.addVar(vtype=GRB.INTEGER, name = "x1")
    x2 = model.addVar(vtype=GRB.INTEGER, name = "x2")
    x3 = model.addVar(vtype=GRB.INTEGER, name = "x3")
    
    # funzione obiettivo
    model.setObjective((4000 - 1500) * x1 + (7500 - 2500) * x2 + (5000 - 2000) * x3 - 150 - 125, sense=GRB.MAXIMIZE)

    # vincoli
    # disponibilità di tavole m^2
    model.addConstr(24 * x1 + 27 * x2 + 23 * x3 <= 800, "tavole_constraint")
    # cucine minime
    model.addConstr(x1 >= 4, "cucinaA_constraint")
    model.addConstr(x2 >= 5, "cucinaB_constraint")
    model.addConstr(x3 >= 6, "cucinaC_constraint")

    # ore per reparto
    model.addConstr(20 * x1 + 30 * x2 + 25 * x3 <= 20 * 60, "taglio_constraint")
    model.addConstr(10 * x1 + 15 * x2 + 10 * x3 <= 18 * 60, "verniciatura_constraint")
    model.addConstr(8 * x1 + 12 * x2 + 15 * x3 <= 22 * 60, "montaggio_constraint")
    
    model.addConstr(x1 >= 0, "non_negative_x1")
    model.addConstr(x2 >= 0, "non_negative_x2")
    model.addConstr(x3 >= 0, "non_negative_x3")
    
    model.optimize()

    # stampa della soluzione ottimale

    if model.status == GRB.OPTIMAL:
        print("Soluzione ottimale trovata")
        print(f"Cucine di tipo A da produrre: {x1.x:.2f}")
        print(f"Cucine di tipo B da produrre: {x2.x:.2f}")
        print(f"Cucine di tipo C da produrre: {x3.x:.2f}")

        print(f"Incasso totale: € {model.objval:.2f}")
    else:
        print("Il modello non ha trovato una soluzione ottimale.")

except gp.GurobiError as e:
    print(f"Errore Gurobi: {e}")
    
except Exception as e:
    print(f"Errore durante l'esecuzione del programma: {e}")





    

