def min_operations(a, b):
    return (abs(b - a) * (abs(b - a) + 1)) // 2

t = int(input())
results = []
for _ in range(t):
    a, b = map(int, input().split())
    results.append(min_operations(a, b))

for result in results:
    print(result)