def determine_winner(a, b):
    turn = 1
    while True:
        if turn % 2 == 1:  # Vladik's turn
            if a < turn // 2 + 1:
                return "Vladik"
            a -= turn // 2 + 1
        else:  # Valera's turn
            if b < turn // 2 + 1:
                return "Valera"
            b -= turn // 2 + 1
        turn += 1

# Example usage:
a, b = map(int, input().split())
print(determine_winner(a, b))