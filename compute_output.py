from compute_input import parse_input_file
from utils import apply_effects

def parse_output_file(file_path):
    """
    Legge il file di output e restituisce un dizionario con i turni e le risorse acquistate.
    """
    acquired_resources = {}
    with open(file_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        parts = list(map(int, line.split()))
        turn = parts[0]  # Turno di acquisto
        num_resources = parts[1]  # Numero di risorse acquistate
        resources = parts[2:]  # Lista ID risorse acquistate

        acquired_resources[turn] = resources

    return acquired_resources

def calculate_actual_profit(input_file, output_file):
    """
    Calcola il profitto effettivo generato sulla base degli input e del file di output.
    """
    # Parsing file di input
    parsed_data = parse_input_file(input_file)
    D = parsed_data["D"]
    R = parsed_data["R"]
    T = parsed_data["T"]
    resources = parsed_data["resources"]
    turns = parsed_data["turns"]

    # Parsing file di output
    acquired_resources = parse_output_file(output_file)

    # Applicare effetti speciali
    updated_resources, updated_turns, accumulator_capacity = apply_effects(resources, turns, acquired_resources, len(turns))

    # Variabili per calcolo profitto
    budget = D
    total_profit = 0
    active_resources = {}  # Dizionario per tenere traccia delle risorse attive per turno
    energy_accumulator = 0  # Capacità accumulata se presente effetto E

    # Simulazione turni
    for t in range(T):
        # Aggiorna risorse attive
        if t in acquired_resources:
            for r in acquired_resources[t]:
                if r not in active_resources:
                    active_resources[r] = []
                active_resources[r].append(t)

        # Calcolo del numero di edifici alimentati
        buildings_powered = 0
        expired_resources = []

        for r, start_times in active_resources.items():
            RW = updated_resources[r]["RW"]
            RM = updated_resources[r]["RM"]
            RL = updated_resources[r]["RL"]
            RU = updated_resources[r]["RU"]

            # Controlliamo quali risorse sono ancora attive in questo turno
            active_count = 0
            for start in start_times:
                if t < start + RL and (t - start) % (RW + RM) < RW:
                    active_count += 1

            buildings_powered += active_count * RU

            # Controlla risorse scadute
            if t >= start + RL:
                expired_resources.append(r)

        # Rimuove risorse scadute
        for r in expired_resources:
            del active_resources[r]

        # Gestione accumulatore
        if buildings_powered < updated_turns[t]["TM"] and accumulator_capacity > 0:
            needed = updated_turns[t]["TM"] - buildings_powered
            if energy_accumulator >= needed:
                buildings_powered += needed
                energy_accumulator -= needed
            else:
                buildings_powered += energy_accumulator
                energy_accumulator = 0

        elif buildings_powered > updated_turns[t]["TX"] and accumulator_capacity > 0:
            surplus = buildings_powered - updated_turns[t]["TX"]
            energy_accumulator += surplus
            buildings_powered = updated_turns[t]["TX"]

        # Calcolo profitto
        if buildings_powered >= updated_turns[t]["TM"]:
            profit = buildings_powered * updated_turns[t]["TR"]
        else:
            profit = 0  # Nessun profitto se TM non è raggiunto

        # Calcolo costi di manutenzione
        maintenance_cost = sum(updated_resources[r]["RP"] for r in active_resources)

        # Aggiorna budget
        budget += profit - maintenance_cost
        total_profit += profit

    return total_profit


if __name__ == '__main__':

    # File input e output
    input_file = "data/8-shiva.txt"
    output_file = "output/output-8-shiva.txt"

    # Calcolo profitto effettivo
    actual_profit = calculate_actual_profit(input_file, output_file)
    print(actual_profit)
