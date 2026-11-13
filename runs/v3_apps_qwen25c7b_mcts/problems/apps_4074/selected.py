def min_packages(n, k):
    for i in range(k, 0, -1):
        if n % i == 0:
            return n // i

# Input handling
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

# Output results
for result in results:
    print(result)