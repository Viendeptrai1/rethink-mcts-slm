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
    for l in range(n):
        for r in range(l, n):
            # Create a new string with the segment [l, r] inverted
            inverted_segment = ''.join(')' if c == '(' else '(' for c in s[l:r+1])
            new_sequence = s[:l] + inverted_segment + s[r+1:]
            if is_valid_bracket_sequence(new_sequence):
                return "possible"
    return "impossible"

# Read input from standard input
import sys
input_sequence = sys.stdin.read().strip()

# Output the result
print(can_make_valid_by_inversion(input_sequence))