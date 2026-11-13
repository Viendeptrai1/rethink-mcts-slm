import sys
from collections import Counter

def parse_molecule(molecule):
    i = 0
    result = []
    while i < len(molecule):
        atom = molecule[i]
        count = 1
        if i + 1 < len(molecule) and molecule[i + 1].isdigit():
            j = i + 2
            while j < len(molecule) and molecule[j].isdigit():
                count = count * 10 + int(molecule[j])
                j += 1
            i = j - 1
        result.append((atom, count))
        i += 1
    return Counter(result)

def max_output(input_molecule, output_molecule, num_input_molecules):
    input_counter = parse_molecule(input_molecule)
    output_counter = parse_molecule(output_molecule)
    
    min_count = float('inf')
    
    for atom, count in output_counter.items():
        if atom not in input_counter:
            return 0
        min_count = min(min_count, input_counter[atom] // count)
    
    return min_count * num_input_molecules

if __name__ == "__main__":
    input_molecule, num_input_molecules = input().strip().split()
    output_molecule = input().strip()
    print(max_output(input_molecule, output_molecule, int(num_input_molecules)))