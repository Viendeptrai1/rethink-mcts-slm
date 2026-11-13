def can_make_valid(s):
    def is_valid(seq):
        balance = 0
        for char in seq:
            if char == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                return False
        return balance == 0

    n = len(s)
    for i in range(n):
        for j in range(i, n):
            inverted_seq = s[:i] + ''.join(')' if c == '(' else '(' for c in s[i:j+1]) + s[j+1:]
            if is_valid(inverted_seq):
                return "possible"
    return "impossible"

# Example usage:
import sys
input = sys.stdin.read
data = input().strip()
print(can_make_valid(data))