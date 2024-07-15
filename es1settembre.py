import gurobipy as gp
from gurobipy import GRB

model = Model("produzione batterie")

impianto = [1,2]
tipo = ["A", "B","G"]

prezzi{'A':45, 'B':40, 'C':30} # prezzi di vendita
cr = 5 # costo rame
cn = 7 # costo nickel

# consumo rame e nickel
r = {('A', 1): 0, ('B', 1): 1, ('C', 2): 2, ('A', 2):0, ('B',2):2, ('C',2): 5}
n = {('A', 1): 2, ('B', 1): 3, ('C', 2): 0, ('A', 2):4, ('B',2):2, ('C',2): 0}

# costi per batteria i fatta da impianto j
c = {(




