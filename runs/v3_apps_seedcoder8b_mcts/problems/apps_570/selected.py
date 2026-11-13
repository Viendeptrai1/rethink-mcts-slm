def who_cannot_give_candy(a, b):
    turn = 0  # 0 for Vladik, 1 for Valera
    while a > 0 and b > 0:
        if turn == 0:
            if b <= a + 1:
                return "Valera"
            b -= a + 1
        else:
            if a <= b + 1:
                return "Vladik"
            a -= b + 1
        turn = 1 - turn  # Switch turns

    return "Vladik" if turn == 1 else "Valera"

# Read input
a, b = map(int, input().split())

# Print the result
print(who_cannot_give_candy(a, b))