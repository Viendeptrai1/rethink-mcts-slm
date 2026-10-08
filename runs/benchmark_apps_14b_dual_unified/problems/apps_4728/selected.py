import sys
from collections import defaultdict

def parse_molecule(molecule):
    stack = []
    current_atom = ''
    current_count = ''
    result = defaultdict(int)
    
    for char in molecule:
        if char.isalpha():
            if current_atom:
                if current_count:
                    result[current_atom] += int(current_count)
                else:
                    result[current_atom] += 1
            current_atom = char
            current_count = ''
        elif char.isdigit():
            current_count += char
    
    if current_atom:
        if current_count:
            result[current_atom] += int(current_count)
        else:
            result[current_atom] += 1
    
    return result

def max_output_molecules(input_molecule, k, output_molecule):
    input_counts = parse_molecule(input_molecule)
    output_counts = parse_molecule(output_molecule)
    
    min_ratio = float('inf')
    
    for atom, count in output_counts.items():
        if atom not in input_counts:
            return 0
        min_ratio = min(min_ratio, input_counts[atom] * k // count)
    
    return min_ratio

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    input_molecule = data[0]
    k = int(data[1])
    output_molecule = data[2]
    
    result = max_output_molecules(input_molecule, k, output_molecule)
    print(result)

if __name__ == "__main__":
    main()