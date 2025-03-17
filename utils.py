from compute_input import parse_input_file
def apply_effects(resources, turns, acquired_resources, T):
    """
    Applica gli effetti speciali delle risorse agli input del modello,
    considerando tutte le risorse attive in ogni turno.
    """
    modified_turns = turns.copy()
    modified_resources = resources.copy()
    accumulator_capacity = 0  # Capacità dell'accumulatore

    # Struttura per tracciare le risorse attive
    active_resources = {t: [] for t in range(T)}

    #innanzitutto cicla e considera 

    # Costruire la lista di risorse attive per ogni turno
    for t in range(T):
        # Aggiungere le risorse acquistate nei turni precedenti che sono ancora in vita
        for past_t in range(max(0, t - max(resources[r]["RL"] for r in resources)), t + 1):
            if past_t in acquired_resources:
                for r in acquired_resources[past_t]:
                    RL = resources[r]["RL"]
                    if t < past_t + RL:  # La risorsa è ancora in vita
                        active_resources[t].append(r)

        # Effetti accumulati
        effect_A = 1.0  # Modifica RU (numero di edifici alimentati)
        effect_B = 1.0  # Modifica TM e TX
        effect_C = {}   # Modifica RL per ogni risorsa
        effect_D = 1.0  # Modifica TR
        temp_accumulator = 0  # Per accumulo dell'effetto E

        for r in active_resources[t]:
            effect = resources[r]["RT"]
            effect_value = resources[r]["RE"]

            if effect == "A" and effect_value:
                effect_A *= (1 + effect_value / 100)  # Incrementa RU del r%

            if effect == "B" and effect_value:
                effect_B *= (1 + effect_value / 100)  # Incrementa TM e TX del t%

            if effect == "C" and effect_value:
                effect_C[r] = (1 + effect_value / 100)  # Incrementa RL del r%

            if effect == "D" and effect_value:
                effect_D *= (1 + effect_value / 100)  # Incrementa TR del t%

            if effect == "E":
                temp_accumulator += effect_value  # Incrementa capacità dell'accumulatore

        # Applicare gli effetti per il turno corrente
        modified_turns[t]["TM"] = int(turns[t]["TM"] * effect_B)
        modified_turns[t]["TX"] = int(turns[t]["TX"] * effect_B)
        modified_turns[t]["TR"] = int(turns[t]["TR"] * effect_D)

        # Modifica RU per ogni risorsa con effetto A
        for r in resources:
            modified_resources[r]["RU"] = int(resources[r]["RU"] * effect_A)

        # Modifica RL per ogni risorsa con effetto C
        for r in effect_C:
            modified_resources[r]["RL"] = int(resources[r]["RL"] * effect_C[r])

        # Aggiornare capacità dell'accumulatore
        accumulator_capacity += temp_accumulator

    return modified_resources, modified_turns, accumulator_capacity
