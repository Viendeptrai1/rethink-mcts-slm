import sys
import re
from collections import defaultdict

def parse_molecule(molecule):
    pattern = r'([A-Z])(\d*)'
    matches = re.findall(pattern, molecule)
    atom_count = defaultdict(int)
    
    for atom, count in matches:
        atom_count[atom] += int(count) if count else 1
        
    return atom_count

def max_molecules(input_molecule, input_count, output_molecule):
    input_atoms = parse_molecule(input_molecule)
    output_atoms = parse_molecule(output_molecule)
    
    max_molecules = float('inf')
    
    for atom, output_count in output_atoms.items():
        if atom in input_atoms:
            max_molecules = min(max_molecules, input_atoms[atom] // output_count)
        else:
            return 0
    
    return max_molecules

def main():
    input_data = sys.stdin.read().strip()
    first_line, second_line = input_data.split('\n')
    
    input_molecule = ''.join(first_line.split()[:-1])
    input_count = int(first_line.split()[-1])
    output_molecule = second_line
    
    result = max_molecules(input_molecule, input_count, output_molecule)
    print(result)

if __name__ == "__main__":
    main()