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
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # First token: input molecule string
    # Second token: integer k
    # Third token: output molecule string
    # Note: The molecule string might contain digits, but the split() handles whitespace separation.
    # The problem says "The first line contains the input molecule... followed by an integer k".
    # Since molecule strings don't contain spaces, split() works perfectly.

    input_mol_str = input_data[0]
    k = int(input_data[1])
    output_mol_str = input_data[2]

    input_counts = parse_mol_str(input_mol_str)
    output_counts = parse_mol_str(output_mol_str)

    # Calculate how many output molecules can be formed per single input molecule
    # For each atom in output, check if input has enough.
    # If an atom is missing in input, we can make 0.
    
    possible = True
    min_per_input = float('inf')
    
    for atom, needed in output_counts.items():
        if atom not in input_counts:
            possible = False
            break
        available = input_counts[atom]
        if available < needed:
            possible = False
            break
        # How many output molecules can we make based on this atom?
        count = available // needed
        if count < min_per_input:
            min_per_input = count
    
    if not possible:
        print(0)
        return

    # Total input molecules available
    total_input = k
    
    # Total output molecules = (molecules per input) * total_input
    result = min_per_input * total_input
    print(result)

if __name__ == "__main__":
    solve()