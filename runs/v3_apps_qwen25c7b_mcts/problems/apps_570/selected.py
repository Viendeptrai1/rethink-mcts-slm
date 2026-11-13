def determine_winner(a, b):
    diff = abs(a - b)
    turn = 1
    while diff > turn:
        if diff <= turn + 1:
            return "Vladik" if a < b else "Valera"
        diff -= turn
        turn += 1
    return "Vladik" if a < b else "Valera"

# Example usage:
a, b = map(int, input().split())
print(determine_winner(a, b))