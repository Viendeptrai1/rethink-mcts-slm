def min_packages(n, k):
    return (n + k - 1) // k

import sys
input = sys.stdin.read
data = input().split()

t = int(data[0])
results = []

index = 1
for _ in range(t):
    n = int(data[index])
    k = int(data[index + 1])
    index += 2
    results.append(min_packages(n, k))

print('\n'.join(map(str, results)))