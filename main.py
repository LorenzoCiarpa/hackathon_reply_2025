from read_file import read_input_file
from sorter import sort_resources, sort_by_efficiency, compute_efficiency
from get_data import get_data
from utils import compute_profit, compute_to_buy

def main_loop(budget, resources_group, resources, turns, T):


    f = open("output-attenborough-mod.txt", "w")

    green_resources = resources_group[0]
    base_resources = resources_group[1]
    non_green_resources = resources_group[2]

    uuid = 0

    resources_purchased = []

    for t in range(T):


        print("\nTurno", t)

        T_m = turns[t][0] #Domanda minima
        T_x = turns[t][1] #Domanda massima
        T_r = turns[t][2] #Profitto per building

        coverage = 0
        maintenance = 0
        purchasing_expenses = 0
        failed = False

        # check what we cover wtih the resources we have
        for res in resources_purchased:
            if res['dead']:
                continue

            maintenance += resources[res['RI']]['RP']
            res['lifetime'] += 1
            res['turn_status'] += 1

            if res['active']:
                coverage += resources[res['RI']]['RU']

        if coverage >= T_m:
            # we have enough coverage
            profit = compute_profit(coverage, T_x, T_r, maintenance)

            f.write(str(t) + " 0\n")

        else:
            
            green_efficiencies = [compute_efficiency(res, turns, T, t) for res in green_resources]
            RA_list_green = [resources[res['RI']]['RA'] for res in green_resources]
            RU_list_green = [resources[res['RI']]['RU'] for res in green_resources]

            # we need to buy resources
            B = compute_to_buy(budget, T_m, green_efficiencies, RA_list_green, RU_list_green)

            if B is None:
                base_efficiencies = [compute_efficiency(res, turns, T, t) for res in base_resources]
                RA_list_base = [resources[res['RI']]['RA'] for res in base_resources]
                RU_list_base = [resources[res['RI']]['RU'] for res in base_resources]

                # we need to buy resources
                B = compute_to_buy(budget, T_m, green_efficiencies + base_efficiencies, RA_list_green + RA_list_base, RU_list_green + RU_list_base)

                if B is None:
                    non_green_efficiencies = [compute_efficiency(res, turns, T, t) for res in non_green_resources]
                    RA_list_non_green = [resources[res['RI']]['RA'] for res in non_green_resources]
                    RU_list_non_green = [resources[res['RI']]['RU'] for res in non_green_resources]

                    # we need to buy resources
                    B = compute_to_buy(budget, T_m, 
                                       green_efficiencies + base_efficiencies + non_green_efficiencies,
                                       RA_list_green + RA_list_base + RA_list_non_green,
                                       RU_list_green + RU_list_base + RU_list_non_green)

            if B is None:
                failed = True
            
            if not failed:
                full_list = green_resources + base_resources + non_green_resources

                stringozza = str(t) + " "
                stringozza += str(sum(B)) + " "
                
                for i, b in enumerate(B):
                    if b > 0:
                        for k in range(b):
                            resources_purchased.append({
                                'uuid': uuid,
                                'RI': full_list[i]['RI'],
                                'lifetime': 0,
                                'turn_status': 0,
                                'active': True,
                                'dead': False,
                            })
                            uuid += 1

                            stringozza += str(full_list[i]['RI']) + " "

                        coverage += full_list[i]['RU'] * b
                        purchasing_expenses += full_list[i]['RA'] * b
                        maintenance += full_list[i]['RP'] * b

                profit = compute_profit(coverage, T_x, T_r, maintenance)

                f.write(stringozza + "\n")


        for res in resources_purchased:
            if res['dead']:
                continue
            
            if res['active'] and res['turn_status'] == resources[res['RI']]['RW']:
                res['active'] = False
                res['turn_status'] = 0

            elif not res['active'] and res['turn_status'] == resources[res['RI']]['RM']:
                res['active'] = True
                res['turn_status'] = 0
            
            if res['lifetime'] == resources[res['RI']]['RL']:
                res['dead'] = True

        print(f"purchased: ", resources_purchased)
        if failed:
            budget -= maintenance
        else:
            budget += profit - purchasing_expenses


        print(f"Er budget è: {budget}")

        if t == T - 1:
            f.close()
            




if __name__ == "__main__":

    file_path = "./data/2-attenborough.txt"
    D, R, T, resources, turns = read_input_file(file_path)

    # Stampa per verifica
    print("Budget iniziale:", D)
    print("Numero di risorse:", R)
    print("Numero di turni:", T)

    print("\nRisorse:")
    for res in resources:
        print(res)
        
    print("\nTurni:")
    for turn in turns:
        print(turn)



    # Esempio di utilizzo
    sorted_resources, green_resources, base_resources, non_green_resources = sort_resources(resources)


    # Stampa per verifica
    print("\nRisorse ordinate:")
    for res in sorted_resources:
        print(res)

    print("\nRisorse verdi:")
    for res in green_resources:
        print(res)

    print("\nRisorse di base:")
    for res in base_resources:
        print(res)

    print("\nAltre risorse:")
    for res in non_green_resources:
        print(res)





    # Riordiniamo le liste con la nuova funzione
    green_resources_sorted = sort_by_efficiency(green_resources, turns, T, 5)
    base_resources_sorted = sort_by_efficiency(base_resources, turns, T, 0)
    non_green_resources_sorted = sort_by_efficiency(non_green_resources, turns, T, 0)

    # Stampa per verifica
    green_efficiencies = []
    print("\nRisorse Green ordinate per efficienza:")
    for res in green_resources_sorted:
        print(res, "Efficienza:", compute_efficiency(res, turns, T, 4))
        green_efficiencies.append(compute_efficiency(res, turns, T, 0))

    print("\nRisorse base ordinate per efficienza:")
    for res in base_resources_sorted:
        print(res, "Efficienza:", compute_efficiency(res, turns, T, 0))

    print("\nRisorse Non-Green ordinate per efficienza:")
    for res in non_green_resources_sorted:
        print(res, "Efficienza:", compute_efficiency(res, turns, T, 0))


    # print("\nRisorse Base (X) ordinate per efficienza:")
    # for res in base_resources_sorted:
    #     print(res, "Efficienza:", compute_efficiency(res, turns, T))

    # print("\nRisorse Non-Green ordinate per efficienza:")
    # for res in non_green_resources_sorted:
    #     print(res, "Efficienza:", compute_efficiency(res, turns, T))

    main_loop(D, [green_resources_sorted, base_resources_sorted, non_green_resources_sorted], resources, turns, T)

    

        

        