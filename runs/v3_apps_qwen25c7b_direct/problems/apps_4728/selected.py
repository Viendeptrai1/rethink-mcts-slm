import sys
from collections import Counter

def parse_molecule(molecule):
    i = 0
    result = []
    while i < len(molecule):
        element = molecule[i]
        i += 1
        count = ''
        while i < len(molecule) and molecule[i].isdigit():
            count += molecule[i]
            i += 1
        if count == '':
            result.append((element, 1))
        else:
            result.append((element, int(count)))
    return result

def calculate_max_output(input_molecule, output_molecule, num_input_molecules):
    input_counts = Counter(parse_molecule(input_molecule))
    output_counts = Counter(parse_molecule(output_molecule))
    
    max_output = float('inf')
    for element, count in output_counts.items():
        if element not in input_counts:
            return 0
        max_output = min(max_output, input_counts[element] // count)
    
    return max_output * num_input_molecules

if __name__ == "__main__":
    input_data = sys.stdin.read().splitlines()
    input_molecule = input_data[0].split()[0]
    num_input_molecules = int(input_data[0].split()[1])
    output_molecule = input_data[1]
    
    result = calculate_max_output(input_molecule, output_molecule, num_input_molecules)
    print(result)