def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        if n % 4 == 0:
            print("YES")
            half = n // 2
            even_sum = half * (half + 1)
            print(*range(1, half + 1), *range(half + 1, n + 1))
        else:
            print("NO")

solve()