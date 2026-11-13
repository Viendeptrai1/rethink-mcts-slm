def can_be_valid_by_inversion(bracket_sequence):
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
    for i in range(n):
        for j in range(i, n):
            inverted_sequence = list(bracket_sequence)
            for k in range(i, j + 1):
                if inverted_sequence[k] == '(':
                    inverted_sequence[k] = ')'
                else:
                    inverted_sequence[k] = '('
            if is_valid(''.join(inverted_sequence)):
                return "possible"
    return "impossible"

# Example usage:
import sys
input = sys.stdin.read
data = input().strip()
print(can_be_valid_by_inversion(data))