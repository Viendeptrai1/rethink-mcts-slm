from collections import Counter
import sys

def max_output_molecules(input_molecule, num_input_molecules, output_molecule):
    def parse_molecule(molecule):
        i, n = 0, len(molecule)
        counter = Counter()
        while i < n:
            atom = molecule[i]
            i += 1
            if i < n and molecule[i].isdigit():
                j = i
                while j < n and molecule[j].isdigit():
                    j += 1
                count = int(molecule[i:j])
                i = j
            else:
                count = 1
            counter[atom] += count
        return counter
    
    input_counter = parse_molecule(input_molecule * num_input_molecules)
    output_counter = parse_molecule(output_molecule)
    
    min_count = float('inf')
    for atom, count in output_counter.items():
        if atom not in input_counter:
            return 0
        min_count = min(min_count, input_counter[atom] // count)
    
    return min_count

if __name__ == "__main__":
    input_data = sys.stdin.read().splitlines()
    input_molecule = input_data[0].split()[0]
    num_input_molecules = int(input_data[0].split()[1])
    output_molecule = input_data[1]
    
    result = max_output_molecules(input_molecule, num_input_molecules, output_molecule)
    print(result)