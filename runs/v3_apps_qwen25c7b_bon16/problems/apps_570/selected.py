def determine_winner(a, b):
    turn = 1
    while True:
        if turn % 2 == 1:  # Vladik's turn
            if a >= turn // 2 + 1:
                a -= turn // 2 + 1
            else:
                return "Vladik"
        else:  # Valera's turn
            if b >= turn // 2 + 1:
                b -= turn // 2 + 1
            else:
                return "Valera"
        turn += 1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
a = int(data[0])
b = int(data[1])

result = determine_winner(a, b)
print(result)