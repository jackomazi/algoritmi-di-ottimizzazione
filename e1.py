import gurobipy as gp
from gurobipy import GRB

try:
    # Creazione del modello
    model = gp.Model("Maximize Airline Profit")

    # Variabili decisionali
    x1 = model.addVar(vtype=GRB.INTEGER, name="x1")  # Numero di voli del primo tipo di aereo
    x2 = model.addVar(vtype=GRB.INTEGER, name="x2")  # Numero di voli del secondo tipo di aereo

    # Funzione obiettivo: massimizzare l'utile totale
    model.setObjective(10 * x1 + 25 * x2, sense=GRB.MAXIMIZE)

    # Vincoli
    # Vincolo sul numero massimo di passeggeri totali per A
    model.addConstr(10 * x1 + 30 * x1 + 20 * x2 + 100 * x2 <= 800, "max_passengers_A_constraint")
    
    # Vincolo sul numero massimo di passeggeri in Top class per A
    model.addConstr(10 * x1 + 20 * x2 <= 150, "max_top_class_A_constraint")
    
    # Vincolo sulla garanzia dei posti per A
    model.addConstr(10 * x1 + 30 * x1 >= 650, "min_seats_A_constraint")
    
    # Vincolo sul numero massimo di passeggeri totali per B
    model.addConstr(10 * x1 + 30 * x1 + 20 * x2 + 100 * x2 <= 500, "max_passengers_B_constraint")
    
    # Vincolo sul numero massimo di passeggeri in Top class per B
    model.addConstr(10 * x1 + 20 * x2 <= 100, "max_top_class_B_constraint")
    
    # Vincolo sull'esclusività dei voli tra A e B
    model.addConstr(x1 + x2 >= 1, "exclusive_flights_constraint")
    
    # Vincolo sulla proporzione dei voli
    model.addConstr(x1 <= 0.5 * x2, "proportion_constraint")
    
    # Risoluzione del modello
    model.optimize()

    # Stampare la soluzione ottimale
    if model.status == GRB.OPTIMAL:
        print("Soluzione ottimale trovata:")
        print(f"Numero di voli del primo tipo di aereo (x1): {int(x1.x)}")
        print(f"Numero di voli del secondo tipo di aereo (x2): {int(x2.x)}")
        print(f"Utile totale massimizzato: {model.objVal}")
    else:
        print("Il modello non ha trovato una soluzione ottimale.")

except gp.GurobiError as e:
    print(f"Errore Gurobi: {e}")

except Exception as e:
    print(f"Errore durante l'esecuzione del programma: {e}")

