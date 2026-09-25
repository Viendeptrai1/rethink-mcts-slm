import sys

def count_positions_to_make_regular(n, s):
    # Initialize counters
    open_count = 0
    close_count = 0
    imbalance = 0
    result = 0
    
    # First pass: count imbalances
    for char in s:
        if char == '(':
            open_count += 1
        else:
            close_count += 1
        
        if close_count > open_count:
            imbalance += 1
    
    # Second pass: check positions to change
    open_count = 0
    close_count = 0
    for i, char in enumerate(s):
        if char == '(':
            open_count += 1
        else:
            close_count += 1
        
        # Check if changing this position helps
        if (char == '(' and close_count < open_count - 1) or (char == ')' and close_count > open_count):
            result += 1
    
    return result

# Read input
n = int(sys.stdin.readline().strip())
s = sys.stdin.readline().strip()

# Calculate and print the result
print(count_positions_to_make_regular(n, s))