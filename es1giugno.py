
import gurobipy as gp
from gurobipy import GRB

try:
    # Creazione del modello
    model = gp.Model("Maximize Bakery Profit")

    # Variabili decisionali
    x1 = model.addVar(vtype=GRB.CONTINUOUS, name="x1")  # kg di panettone
    x2 = model.addVar(vtype=GRB.CONTINUOUS, name="x2")  # kg di pizza bianca
    x3 = model.addVar(vtype=GRB.CONTINUOUS, name="x3")  # kg di ciambellone
    

    # Funzione obiettivo: massimizzare l'incasso totale
    model.setObjective(7*x1 + 6*x2 + 10*x3, sense=GRB.MAXIMIZE)

    # Vincoli
    # Disponibilità di ingredienti
    model.addConstr(0.7 * 0.6 * x1 + 0.6 * x2 + 0.5 * x3 <= 15, "farina_constraint")
    model.addConstr(0.7 * 0.02 * x1 + 0.02 * x2 <= 0.2, "lievito_constraint")
    model.addConstr(2 * x1 + 4 * x3 <= 32, "uova_constraint")
    model.addConstr((0.7 * 0.05 + 0.2) * x1 + 0.05  * x2 + 0.3 * x3 <= 6, "zucchero_constraint")

    model.addConstr(x2 >= 4, "pizza_bianca_order_constraint")
    # Limite massimo di panettoni
    model.addConstr(x1 <= 7, "max_panettone_constraint")
    # Relazione tra farina e zucchero
    model.addConstr(15 - (0.7 * 0.6 * x1 + 0.6 * x2 + 0.5 * x3) >= 
                    2 * (6 - ((0.7 * 0.05 + 0.2) * x1 + 0.05 * x2 + 0.3 * x3)), "farina_zucchero_relation_constraint") 
    # Xi >= 0
    model.addConstr(x1 >= 0, "non_negative_x1")
    model.addConstr(x2 >= 0, "non_negative_x2")
    model.addConstr(x3 >= 0, "non_negative_x3")

    # Risoluzione del modello
    model.optimize()

    # Stampare la soluzione ottimale
    if model.status == GRB.OPTIMAL:
        print("Soluzione ottimale trovata:")
        print(f"Panettone da produrre: {x1.x:.2f} kg")
        print(f"Pizza bianca da produrre: {x2.x:.2f} kg")
        print(f"Ciambellone da produrre: {x3.x:.2f} kg")
        print(f"Incasso totale massimizzato: € {model.objVal:.2f}")
    else:
        print("Il modello non ha trovato una soluzione ottimale.")

except gp.GurobiError as e:
    print(f"Errore Gurobi: {e}")

except Exception as e:
    print(f"Errore durante l'esecuzione del programma: {e}")

