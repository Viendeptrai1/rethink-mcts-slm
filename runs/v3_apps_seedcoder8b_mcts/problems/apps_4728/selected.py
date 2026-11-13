import sys
import re
from collections import defaultdict

def parse_molecule(molecule):
    pattern = r'([A-Z])(\d*)'
    matches = re.findall(pattern, molecule)
    atom_count = defaultdict(int)
    for atom, count in matches:
        if count == '':
            count = 1
        else:
            count = int(count)
        atom_count[atom] += count
    return atom_count

def max_output(input_molecule, input_count, output_molecule):
    input_atoms = parse_molecule(input_molecule)
    output_atoms = parse_molecule(output_molecule)
    
    min_ratio = float('inf')
    for atom, count in output_atoms.items():
        if atom in input_atoms:
            min_ratio = min(min_ratio, input_atoms[atom] // count)
        else:
            return 0
    
    return min_ratio * input_count

def main():
    input_line = sys.stdin.readline().strip()
    input_parts = input_line.rsplit(' ', 1)
    input_molecule = input_parts[0]
    input_count = int(input_parts[1])
    
    output_molecule = sys.stdin.readline().strip()
    
    result = max_output(input_molecule, input_count, output_molecule)
    print(result)

if __name__ == "__main__":
    main()