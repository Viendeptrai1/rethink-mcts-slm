def min_product(a, b, x, y, n):
    if a - n >= x:
        a -= n
    elif b - n >= y:
        b -= n
    return a * b

t = int(input())
results = []
for _ in range(t):
    a, b, x, y, n = map(int, input().split())
    results.append(min_product(a, b, x, y, n))
for result in results:
    print(result)