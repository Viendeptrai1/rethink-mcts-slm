import sys
from itertools import product

def calculate_walk_value(walk):
    current_node = 1
    for move in walk:
        if move == 'L':
            current_node *= 2
        elif move == 'R':
            current_node = 2 * current_node + 1
    return current_node

def calculate_set_value(pattern):
    # Generate all possible combinations of 'L', 'R', 'P' for '*'
    replacements = [''.join(p) for p in product('LRP', repeat=pattern.count('*'))]
    
    total_value = 0
    for replacement in replacements:
        # Replace '*' in the pattern with the current combination
        walk = pattern.replace('*', replacement)
        total_value += calculate_walk_value(walk)
    
    return total_value

# Read input from stdin
input_pattern = sys.stdin.read().strip()

# Calculate and print the result
print(calculate_set_value(input_pattern))