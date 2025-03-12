def sort_resources(resources):
    # Creazione delle tre liste separate
    green_resources = []
    base_resources = []
    non_green_resources = []
    
    for res in resources:
        if res["RT"] == "X":
            base_resources.append(res)
        elif "RE" in res and res["RE"] > 0:
            green_resources.append(res)
        else:
            non_green_resources.append(res)

    # Ordinare le liste
    green_resources.sort(key=lambda x: x["RE"], reverse=True)  # Ordinati per RE decrescente
    base_resources.sort(key=lambda x: x["RI"], reverse=True)  # Ordinati per ID decrescente (arbitrario)
    non_green_resources.sort(key=lambda x: x["RE"] if "RE" in x else 0, reverse=True)  # Ordinati per RE decrescente

    # Unire le liste nell'ordine richiesto
    sorted_resources = green_resources + base_resources + non_green_resources

    return sorted_resources, green_resources, base_resources, non_green_resources


def compute_efficiency(resource, turns, total_turns, init_turn):
    """
    Calcola l'efficienza di una risorsa in base alla formula:
    eff(r,t) = sum(RU * TR) / [(T-t) * RP + RA]
    
    Parameters:
        resource (dict): dizionario della risorsa.
        turns (list): lista di turni, ciascuno con [TM, TX, TR].
        total_turns (int): numero totale di turni nel gioco.
    
    Returns:
        float: valore di efficienza della risorsa.
    """
    RU = resource["RU"]
    RP = resource["RP"]
    RA = resource["RA"]
    
    # Somma dei valori RU * TR per tutti i turni
    numerator = sum(RU * turns[i][2] for i in range(init_turn, total_turns))
    
    # Evitiamo divisioni per zero
    denominator = (total_turns - init_turn) * RP  + RA
    
    return numerator / denominator if denominator != 0 else 0

def sort_by_efficiency(resources, turns, total_turns, init_turn):
    """
    Ordina la lista di risorse in base all'efficienza decrescente.
    """
    return sorted(resources, key=lambda r: compute_efficiency(r, turns, total_turns, init_turn), reverse=True)
