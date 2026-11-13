def solve():
    n = int(input())
    count = 0
    for _ in range(n):
        p, q = map(int, input().split())
        if p + 2 <= q:
            count += 1
    print(count)