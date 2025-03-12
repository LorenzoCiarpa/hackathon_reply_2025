def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Leggere i parametri iniziali
    D, R, T = map(int, lines[0].strip().split())

    resources = []
    turns = []

    # Leggere le risorse
    for i in range(1, R + 1):
        parts = lines[i].strip().split()
        resource = {
            "RI": int(parts[0]),
            "RA": int(parts[1]),
            "RP": int(parts[2]),
            "RW": int(parts[3]),
            "RM": int(parts[4]),
            "RL": int(parts[5]),
            "RU": int(parts[6]),
            "RT": parts[7],  # Special effect type (char)
        }
        if len(parts) == 9:  # Se c'è un parametro extra
            resource["RE"] = int(parts[8])  # Additional parameter (if present)
        
        resources.append(resource)

    # Leggere i turni
    for i in range(R + 1, R + 1 + T):
        turns.append(list(map(int, lines[i].strip().split())))

    return D, R, T, resources, turns