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

def can_be_made_valid(s):
    n = len(s)
    for l in range(n):
        for r in range(l, n):
            # Invert the segment [l, r]
            inverted = list(s)
            for i in range(l, r + 1):
                inverted[i] = '(' if inverted[i] == ')' else ')'
            if is_valid_bracket_sequence(inverted):
                return "possible"
    return "impossible"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(can_be_made_valid(input))