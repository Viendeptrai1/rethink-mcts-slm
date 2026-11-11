import sys
from collections import defaultdict

def parse_molecule(molecule):
    elements = defaultdict(int)
    i = 0
    while i < len(molecule):
        if molecule[i].isalpha():
            element = molecule[i]
            count = 1
            i += 1
            while i < len(molecule) and molecule[i].isdigit():
                count = count * 10 + int(molecule[i])
                i += 1
            elements[element] += count
        else:
            i += 1
    return elements

def max_output_molecules(input_molecule, k, output_molecule):
    input_elements = parse_molecule(input_molecule)
    output_elements = parse_molecule(output_molecule)
    
    max_molecules = float('inf')
    for element, count in output_elements.items():
        if element not in input_elements:
            return 0
        max_molecules = min(max_molecules, input_elements[element] // (count * k))
    
    return max_molecules

def main():
    input_data = sys.stdin.read().splitlines()
    input_molecule, k = input_data[0].split()
    k = int(k)
    output_molecule = input_data[1]
    
    result = max_output_molecules(input_molecule, k, output_molecule)
    print(result)

if __name__ == "__main__":
    main()