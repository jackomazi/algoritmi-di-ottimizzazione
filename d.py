import gurobipy as gp
from gurobipy import GRB

# Dati del problema
profit_first_type = 10  # Utile per volo del primo tipo (in migliaia di euro)
profit_second_type = 25  # Utile per volo del secondo tipo (in migliaia di euro)
profit_plane1 = 15  # Utile per volo dell'aereo 1 noleggiato (in migliaia di euro)
profit_plane2 = 7  # Utile per volo dell'aereo 2 noleggiato (in migliaia di euro)

max_passengers = 800  # Numero massimo di passeggeri totali
max_top_class = 150  # Numero massimo di passeggeri in Top class

seats_top_first_type = 10  # Posti in Top class del primo tipo di aereo
seats_economy_first_type = 30  # Posti in Economy class del primo tipo di aereo
seats_top_second_type = 20  # Posti in Top class del secondo tipo di aereo
seats_economy_second_type = 100  # Posti in Economy class del secondo tipo di aereo

seats_top_plane1 = 17  # Posti in Top class dell'aereo 1 noleggiato
seats_economy_plane1 = 55  # Posti in Economy class dell'aereo 1 noleggiato
seats_top_plane2 = 5  # Posti in Top class dell'aereo 2 noleggiato
seats_economy_plane2 = 25  # Posti in Economy class dell'aereo 2 noleggiato

# Creazione del modello
model = gp.Model("Maximize Airline Profit")

# Variabili decisionali
x1 = model.addVar(vtype=GRB.INTEGER, name="x1")  # Numero di voli del primo tipo di aereo originale
x2 = model.addVar(vtype=GRB.INTEGER, name="x2")  # Numero di voli del secondo tipo di aereo originale
y1 = model.addVar(vtype=GRB.INTEGER, name="y1")  # Numero di voli dell'aereo 1 noleggiato
y2 = model.addVar(vtype=GRB.INTEGER, name="y2")  # Numero di voli dell'aereo 2 noleggiato

# Funzione obiettivo: massimizzare l'utile totale
model.setObjective(profit_first_type * x1 + profit_second_type * x2 +
                   profit_plane1 * y1 + profit_plane2 * y2, sense=GRB.MAXIMIZE)

# Vincoli
# Vincolo sul numero massimo di passeggeri
model.addConstr(seats_top_first_type * x1 + seats_economy_first_type * x1 +
                seats_top_second_type * x2 + seats_economy_second_type * x2 +
                seats_top_plane1 * y1 + seats_economy_plane1 * y1 +
                seats_top_plane2 * y2 + seats_economy_plane2 * y2 <= max_passengers,
                "max_passengers_constraint")

# Vincolo sul numero massimo di passeggeri in Top class
model.addConstr(seats_top_first_type * x1 +
                seats_top_second_type * x2 +
                seats_top_plane1 * y1 +
                seats_top_plane2 * y2 <= max_top_class,
                "max_top_class_constraint")

# Vincolo aggiuntivo per il primo tipo di aereo originale
model.addConstr(x1 <= 2, "max_flights_original_plane_constraint")

# Risoluzione del modello
model.optimize()

# Stampare la soluzione ottimale
if model.status == GRB.OPTIMAL:
    print("Soluzione ottimale trovata:")
    print(f"Numero di voli del primo tipo di aereo (x1): {int(x1.x)}")
    print(f"Numero di voli del secondo tipo di aereo (x2): {int(x2.x)}")
    print(f"Numero di voli dell'aereo 1 noleggiato (y1): {int(y1.x)}")
    print(f"Numero di voli dell'aereo 2 noleggiato (y2): {int(y2.x)}")
    print(f"Utile totale massimizzato: {model.objVal} migliaia di euro")
else:
    print("Il modello non ha trovato una soluzione ottimale.")

