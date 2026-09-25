def correct_bracketing(brackets: str) -> bool:
    balance = 0
    for char in brackets:
        if char == '<':
            balance += 1
        elif char == '>':
            balance -= 1
        # If balance goes negative, there are more closing brackets than opening ones
        if balance < 0:
            return False
    # In the end, balance should be zero for correct pairing
    return balance == 0

# Test cases
print(correct_bracketing("<"))      # False
print(correct_bracketing("<>"))     # True
print(correct_bracketing("<<><>>")) # True
print(correct_bracketing("><<>"))   # False