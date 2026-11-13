def can_make_valid_by_inversion(bracket_sequence):
    def is_valid(sequence):
        balance = 0
        for char in sequence:
            if char == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                return False
        return balance == 0
    
    n = len(bracket_sequence)
    
    # Check if the original sequence is already valid
    if is_valid(bracket_sequence):
        return "possible"
    
    # Try inverting every possible segment
    for i in range(n):
        for j in range(i, n):
            inverted_segment = [')' if char == '(' else '(' for char in bracket_sequence[i:j+1]]
            new_sequence = bracket_sequence[:i] + ''.join(inverted_segment) + bracket_sequence[j+1:]
            if is_valid(new_sequence):
                return "possible"
    
    return "impossible"

# Example usage:
import sys
input = sys.stdin.read().strip()
result = can_make_valid_by_inversion(input)
print(result)