def min_product(a, b, x, y, n):
    if n >= (a - x + b - y):
        return max((a - x) * (b - y), (a - y) * (b - x))
    else:
        return (a - n // 2) * (b - n - n // 2)

import sys
input = sys.stdin.read
data = input().split()

t = int(data[0])
index = 1
results = []

for _ in range(t):
    a = int(data[index])
    b = int(data[index + 1])
    x = int(data[index + 2])
    y = int(data[index + 3])
    n = int(data[index + 4])
    index += 5
    results.append(min_product(a, b, x, y, n))

for result in results:
    print(result)