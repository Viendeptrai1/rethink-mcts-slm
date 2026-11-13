import sys
import re

def parse_molecule(s):
    counts = {}
    i = 0
    n = len(s)
    while i < n:
        char = s[i]
        if char.isupper():
            atom = char
            i += 1
            if i < n and s[i].isdigit():
                num = 0
                while i < n and s[i].isdigit():
                    num = num * 10 + int(s[i])
                    i += 1
                counts[atom] = counts.get(atom, 0) + num
            else:
                counts[atom] = counts.get(atom, 0) + 1
        else:
            # Should not happen based on problem description
            i += 1
    return counts

def can_make(output_counts, input_counts, k):
    # Calculate total available atoms from k input molecules
    total_available = {}
    for atom, count in input_counts.items():
        total_available[atom] = total_available.get(atom, 0) + count * k

    # Check if we can make at least one output molecule
    max_molecules = float('inf')
    for atom, count in output_counts.items():
        if atom not in total_available:
            return 0
        possible = total_available[atom] // count
        if possible == 0:
            return 0
        max_molecules = min(max_molecules, possible)
    return max_molecules

def solve():
    input_data = sys.stdin.read().strip()
    if not input_data:
        return
    
    lines = input_data.split('\n')
    first_line = lines[0].strip()
    second_line = lines[1].strip() if len(lines) > 1 else ""
    
    # Parse first line: molecule string and integer k
    # The molecule string consists of uppercase letters and digits, followed by k
    # We need to split the molecule string from k. Since k is at the end and is an integer,
    # we can find the last occurrence of a digit sequence that forms a valid number for k.
    # However, the molecule itself can contain digits. The problem says: "string ... followed by an integer k".
    # This implies the format is: [molecule_string] [space] [k]
    # But the molecule string might not have spaces. Let's assume there is a space before k.
    
    parts = first_line.rsplit(' ', 1)
    if len(parts) != 2:
        # If there's no space, maybe the input format is strict and k is just appended?
        # But the example shows "H 2", "C2H6 10". So there is a space.
        # If for some reason no space, we might need to handle it, but let's stick to rsplit.
        molecule_str = parts[0]
        try:
            k = int(parts[1])
        except:
            # Fallback if split failed unexpectedly
            return
    else:
        molecule_str, k_str = parts
        try:
            k = int(k_str)
        except:
            return

    input_counts = parse_molecule(molecule_str)
    output_counts = parse_molecule(second_line)
    
    result = can_make(output_counts, input_counts, k)
    print(result)

if __name__ == "__main__":
    solve()