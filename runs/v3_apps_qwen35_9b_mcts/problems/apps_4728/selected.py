import sys
from collections import Counter

def parse_molecule(s):
    counts = Counter()
    i = 0
    n = len(s)
    while i < n:
        char = s[i]
        if char.isupper():
            atom = char
            i += 1
            if i < n and s[i].isdigit():
                num_str = ""
                while i < n and s[i].isdigit():
                    num_str += s[i]
                    i += 1
                counts[atom] += int(num_str) if num_str else 1
            else:
                counts[atom] += 1
        else:
            # Should not happen based on problem description (only uppercase letters start atoms)
            i += 1
    return counts

def solve():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    first_line = input_data[0].strip()
    parts = first_line.rsplit(' ', 1)
    input_mol_str = parts[0]
    k = int(parts[1])
    
    output_mol_str = input_data[1].strip()
    
    inventory = parse_molecule(input_mol_str)
    total_inventory = {atom: count * k for atom, count in inventory.items()}
    
    required = parse_molecule(output_mol_str)
    
    if not required:
        print(0)
        return
    
    max_molecules = float('inf')
    
    for atom, req_count in required.items():
        if req_count == 0:
            continue
        if atom not in total_inventory:
            max_molecules = 0
            break
        possible = total_inventory[atom] // req_count
        if possible < max_molecules:
            max_molecules = possible
    
    if max_molecules == float('inf'):
        print(0)
    else:
        print(max_molecules)

if __name__ == "__main__":
    solve()