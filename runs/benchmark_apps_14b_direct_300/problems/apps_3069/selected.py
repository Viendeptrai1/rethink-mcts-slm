def is_valid_bracket_sequence(s):
    balance = 0
    for char in s:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return False
    return balance == 0

def can_make_valid_by_inversion(s):
    n = len(s)
    balance = 0
    first_invalid_index = -1
    
    # Find the first point where the sequence becomes invalid
    for i in range(n):
        if s[i] == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            first_invalid_index = i
            break
    
    # If the sequence is already valid
    if first_invalid_index == -1:
        return "possible"
    
    # Try to find a valid inversion
    for i in range(first_invalid_index, n):
        if s[i] == '(':
            s[i] = ')'
        else:
            s[i] = '('
        
        if is_valid_bracket_sequence(s):
            return "possible"
        
        # Revert the change
        if s[i] == '(':
            s[i] = ')'
        else:
            s[i] = '('
    
    return "impossible"

# Read input
import sys
input = sys.stdin.read().strip()

# Output the result
print(can_make_valid_by_inversion(list(input)))