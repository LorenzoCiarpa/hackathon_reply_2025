import gurobipy as gp
from gurobipy import GRB

# import pdb; pdb.set_trace()  ## per punti di debug


# Parametri di esempio
T = 10  # Orizzonte temporale
R = 2   # Numero di tipi di risorsa
lifetime = {1: 6, 2: 5}   # Tempo di vita per ogni risorsa
active = {1: 2, 2: 3}     # Numero di turni attivi
nonActive = {1: 1, 2: 2}  # Numero di turni non attivi

# Funzione per determinare se una risorsa acquistata al tempo tau è attiva al tempo t
def is_active(r, tau, t):
    if t < tau or t >= tau + lifetime[r]:  # Fuori dal periodo di vita
        return 0
    relative_t = t - tau  # Tempo relativo rispetto all'acquisto
    cycle_length = active[r] + nonActive[r]  # Lunghezza di un ciclo completo
    return 1 if (relative_t % cycle_length) < active[r] else 0

# Modello
m = gp.Model("Resource_Activation_Full")

# Variabili
x = m.addVars(R, T, vtype=GRB.INTEGER, name="x")  # Risorse acquistate
y = m.addVars(R, T, vtype=GRB.INTEGER, name="y")  # Risorse in vita
p = m.addVars(R, T, vtype=GRB.INTEGER, name="p")  # Risorse attive

# Vincolo per y[r,t]: Somma delle risorse acquistate nei turni precedenti ancora in vita
for r in range(1, R+1):
    for t in range(1, T+1):
        m.addConstr(y[r, t] == gp.quicksum(x[r, tau] for tau in range(max(1, t - lifetime[r] + 1), t+1)),
                    name=f"lifetime_{r}_{t}")

# Vincolo per p[r,t]: Solo una parte delle risorse in vita sono attive
for r in range(1, R+1):
    for t in range(1, T+1):
        m.addConstr(p[r, t] == gp.quicksum(x[r, tau] * is_active(r, tau, t) 
                                           for tau in range(max(1, t - lifetime[r] + 1), t+1)),
                    name=f"activation_{r}_{t}")

# Obiettivo fittizio (minimizzazione totale acquisti, può essere cambiato)
m.setObjective(gp.quicksum(x[r, t] for r in range(1, R+1) for t in range(1, T+1)), GRB.MINIMIZE)

# Risolvi
m.optimize()

# Output risultati
for r in range(1, R+1):
    for t in range(1, T+1):
        print(f"x[{r},{t}] = {x[r,t].x}, y[{r},{t}] = {y[r,t].x}, p[{r},{t}] = {p[r,t].x}")
