import numpy as np

def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    D, R, T = map(int, lines[0].split())
    resources = []
    for i in range(1, R + 1):
        data = lines[i].split()
        resources.append({
            'RI': int(data[0]), 'RA': int(data[1]), 'RP': int(data[2]),
            'RW': int(data[3]), 'RM': int(data[4]), 'RL': int(data[5]),
            'RU': int(data[6]), 'RT': data[7],
            'RE': int(data[8]) if len(data) > 8 else 0
        })
    
    turns = []
    for i in range(R + 1, R + 1 + T):
        turns.append(tuple(map(int, lines[i].split())))
    
    return D, resources, turns

def select_resources(budget, resources, needed_power):
    affordable = [r for r in resources if r['RA'] <= budget]
    affordable.sort(key=lambda r: (r['RU'] / r['RA']), reverse=True)
    
    selected = []
    current_power = 0
    
    for r in affordable:
        if current_power >= needed_power:
            break
        selected.append(r['RI'])
        current_power += r['RU']
        budget -= r['RA']
    
    return selected, budget

def simulate_game(D, resources, turns):
    budget = D
    active_resources = []
    output = []
    
    for t, (TM, TX, TR) in enumerate(turns):
        needed_power = max(0, TM - sum(r['RU'] for r in active_resources))
        
        if needed_power > 0:
            selected, budget = select_resources(budget, resources, needed_power)
            if selected:
                output.append(f"{t} {len(selected)} " + " ".join(map(str, selected)))
                active_resources.extend([r for r in resources if r['RI'] in selected])
        
        powered = min(sum(r['RU'] for r in active_resources), TX)
        profit = powered * TR if powered >= TM else 0
        maintenance = sum(r['RP'] for r in active_resources)
        budget += profit - maintenance
        
        active_resources = [r for r in active_resources if r['RL'] > 1]
        for r in active_resources:
            r['RL'] -= 1
    
    return output

def main():
    input_file = "data/0-demo.txt"
    D, resources, turns = read_input(input_file)
    output = simulate_game(D, resources, turns)
    
    with open("output.txt", "w") as f:
        for line in output:
            f.write(line + "\n")
    
if __name__ == "__main__":
    main()
