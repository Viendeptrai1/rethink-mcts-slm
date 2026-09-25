def correct_bracketing(brackets: str) -> bool:
    balance = 0
    for char in brackets:
        if char == '<':
            balance += 1
        elif char == '>':
            balance -= 1
        # If balance goes negative, there are more closing brackets than opening
        if balance < 0:
            return False
    # If balance is zero, all opening brackets have matching closing brackets
    return balance == 0