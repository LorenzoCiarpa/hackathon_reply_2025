import json

def parse_input_file(file_path):
    """
    Legge il file di input e restituisce un dizionario contenente:
    - D: budget iniziale
    - R: numero di risorse disponibili
    - T: numero di turni
    - resources: dizionario con i dettagli delle risorse
    - turns: dizionario con i parametri di ogni turno
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Parsing della prima riga: D (budget iniziale), R (numero di risorse), T (numero di turni)
    D, R, T = map(int, lines[0].split())

    # Parsing delle risorse
    resources = {}
    for i in range(1, R + 1):
        parts = lines[i].split()
        RI = int(parts[0])  # ID della risorsa
        RA = int(parts[1])  # Costo di attivazione
        RP = int(parts[2])  # Costo periodico
        RW = int(parts[3])  # Turni attivi
        RM = int(parts[4])  # Turni inattivi
        RL = int(parts[5])  # Vita totale
        RU = int(parts[6])  # Edifici alimentati
        RT = parts[7]       # Tipo di effetto (A, B, C, D, E, X)
        RE = int(parts[8]) if len(parts) > 8 else None  # Effetto speciale, se presente

        resources[RI] = {
            "RA": RA, "RP": RP, "RW": RW, "RM": RM, "RL": RL, 
            "RU": RU, "RT": RT, "RE": RE
        }

    # Parsing dei turni
    turns = {}
    for i in range(R + 1, R + 1 + T):
        parts = list(map(int, lines[i].split()))
        turn_id = i - (R + 1)
        turns[turn_id] = {
            "TM": parts[0],  # Minimo edifici da alimentare
            "TX": parts[1],  # Massimo edifici alimentabili
            "TR": parts[2],  # Profitto per edificio
        }

    return {"D": D, "R": R, "T": T, "resources": resources, "turns": turns}


if __name__ == '__main__':

    # Esegui la funzione con il tuo file
    file_path = "0-demo.txt"  # Cambia il percorso se necessario
    parsed_data = parse_input_file(file_path)

    print(json.dumps(parsed_data, indent=4))
