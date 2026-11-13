def solve(a, b):
    turn = 0
    while a > 0 and b > 0:
        if turn % 2 == 0:
            if b <= a:
                return "Vladik"
            b -= a + 1
        else:
            if a <= b:
                return "Valera"
            a -= b + 1
        turn += 1
    return "Vladik" if turn % 2 == 1 else "Valera"

a, b = map(int, input().split())
print(solve(a, b))