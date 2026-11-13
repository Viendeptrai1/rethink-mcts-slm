def is_valid_bracket_sequence(s: str) -> bool:
    balance = 0
    for char in s:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return False
    return balance == 0

def can_make_valid(s: str) -> str:
    # First check if the sequence is already valid
    if is_valid_bracket_sequence(s):
        return "possible"

    n = len(s)
    for l in range(n):
        for r in range(l, n):
            # Create a new sequence by inverting the segment [l, r]
            new_s = list(s)
            for i in range(l, r + 1):
                if new_s[i] == '(':
                    new_s[i] = ')'
                else:
                    new_s[i] = '('
            new_s = ''.join(new_s)
            # Check if the new sequence is valid
            if is_valid_bracket_sequence(new_s):
                return "possible"

    return "impossible"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    result = can_make_valid(input)
    print(result)