import gurobipy as gp
from gurobipy import GRB

try:
    # Dati del problema per l'agenzia A
    max_passengers_A = 800  # Numero massimo di passeggeri totali
    max_top_class_A = 150  # Numero massimo di passeggeri in Top class
    seats_top_first_type_A = 10  # Posti in Top class del primo tipo di aereo per A
    seats_economy_first_type_A = 30  # Posti in Economy class del primo tipo di aereo per A
    seats_top_second_type_A = 20  # Posti in Top class del secondo tipo di aereo per A
    seats_economy_second_type_A = 100  # Posti in Economy class del secondo tipo di aereo per A
    profit_first_type_A = 10  # Utile per volo del primo tipo (in migliaia di euro) per A
    profit_second_type_A = 25  # Utile per volo del secondo tipo (in migliaia di euro) per A

    # Dati del problema per l'agenzia B
    max_passengers_B = 500  # Numero massimo di passeggeri totali per B
    max_top_class_B = 100  # Numero massimo di passeggeri in Top class per B
    seats_top_first_type_B = 17  # Posti in Top class del primo tipo di aereo per B (noleggiato)
    seats_economy_first_type_B = 55  # Posti in Economy class del primo tipo di aereo per B (noleggiato)
    seats_top_second_type_B = 5  # Posti in Top class del secondo tipo di aereo per B (noleggiato)
    seats_economy_second_type_B = 25  # Posti in Economy class del secondo tipo di aereo per B (noleggiato)
    profit_plane1_B = 15  # Utile per volo dell'aereo 1 noleggiato (in migliaia di euro) per B
    profit_plane2_B = 7  # Utile per volo dell'aereo 2 noleggiato (in migliaia di euro) per B

    # Creazione del modello
    model = gp.Model("Maximize Airline Profit")

    # Variabili decisionali
    x1_A = model.addVar(vtype=GRB.INTEGER, name="x1_A")  # Numero di voli del primo tipo di aereo per A
    x2_A = model.addVar(vtype=GRB.INTEGER, name="x2_A")  # Numero di voli del secondo tipo di aereo per A
    x1_B = model.addVar(vtype=GRB.INTEGER, name="x1_B")  # Numero di voli del primo tipo di aereo per B (noleggiato)
    x2_B = model.addVar(vtype=GRB.INTEGER, name="x2_B")  # Numero di voli del secondo tipo di aereo per B (noleggiato)

    # Funzione obiettivo: massimizzare l'utile totale
    model.setObjective(profit_first_type_A * x1_A + profit_second_type_A * x2_A +
                       profit_plane1_B * x1_B + profit_plane2_B * x2_B, sense=GRB.MAXIMIZE)

    # Vincoli per l'agenzia A
    model.addConstr(seats_top_first_type_A * x1_A + seats_economy_first_type_A * x1_A +
                    seats_top_second_type_A * x2_A + seats_economy_second_type_A * x2_A <= max_passengers_A,
                    "max_passengers_A_constraint")
    model.addConstr(seats_top_first_type_A * x1_A + seats_top_second_type_A * x2_A <= max_top_class_A,
                    "max_top_class_A_constraint")

    # Vincoli per l'agenzia B
    model.addConstr(seats_top_first_type_B * x1_B + seats_economy_first_type_B * x1_B +
                    seats_top_second_type_B * x2_B + seats_economy_second_type_B * x2_B <= max_passengers_B,
                    "max_passengers_B_constraint")
    model.addConstr(seats_top_first_type_B * x1_B + seats_top_second_type_B * x2_B <= max_top_class_B,
                    "max_top_class_B_constraint")

    # Vincoli aggiuntivi per l'agenzia B
    model.addConstr(x1_B + x2_B >= 1, "exclusive_flights_constraint_B")  # Voli non condivisi con A
    model.addConstr(x1_B <= 0.5 * x2_B, "proportion_constraint_B")  # Proporzione dei voli

    # Risoluzione del modello
    model.optimize()

    # Stampare la soluzione ottimale
    if model.status == GRB.OPTIMAL:
        print("Soluzione ottimale trovata:")
        print(f"Numero di voli del primo tipo di aereo per A (x1_A): {int(x1_A.x)}")
        print(f"Numero di voli del secondo tipo di aereo per A (x2_A): {int(x2_A.x)}")
        print(f"Numero di voli del primo tipo di aereo per B (x1_B): {int(x1_B.x)}")
        print(f"Numero di voli del secondo tipo di aereo per B (x2_B): {int(x2_B.x)}")
        print(f"Utile totale massimizzato: {model.objVal} migliaia di euro")
    else:
        print("Il modello non ha trovato una soluzione ottimale.")

except gp.GurobiError as e:
    print(f"Errore Gurobi trovato: {e}")

except Exception as e:
    print(f"Errore durante l'esecuzione del programma: {e}")

