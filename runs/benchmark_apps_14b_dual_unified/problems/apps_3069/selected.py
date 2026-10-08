import sys

def is_possible_to_make_valid(s):
    n = len(s)
    open_count = 0
    close_count = 0
    imbalance = 0
    first_imbalance_index = -1
    
    for i in range(n):
        if s[i] == '(':
            open_count += 1
        else:
            close_count += 1
        
        if close_count > open_count:
            imbalance += 1
            if first_imbalance_index == -1:
                first_imbalance_index = i
    
    if imbalance == 0:
        return "possible"
    
    if imbalance % 2 != 0:
        return "impossible"
    
    # Check if we can fix the imbalance with one inversion
    if first_imbalance_index >= 1 and s[first_imbalance_index - 1] == ')':
        return "possible"
    
    if first_imbalance_index + 1 < n and s[first_imbalance_index + 1] == '(':
        return "possible"
    
    return "impossible"

# Read input from stdin
input_sequence = sys.stdin.read().strip()

# Output the result
print(is_possible_to_make_valid(input_sequence))