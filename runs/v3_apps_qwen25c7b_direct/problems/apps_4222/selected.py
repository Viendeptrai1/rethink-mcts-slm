def count_victims(N, K, d, A):
    has_snacks = [False] * (N + 1)
    for i in range(K):
        for j in range(d[i]):
            has_snacks[A[i][j]] = True
    return sum(not has_snacks[i] for i in range(1, N + 1))

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
K = int(data[1])

d = []
A = []

index = 2
for _ in range(K):
    d.append(int(data[index]))
    index += 1
    A.append(list(map(int, data[index:index + d[-1]])))
    index += d[-1]

# Calculate and print the result
print(count_victims(N, K, d, A))