import sys

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
K = int(data[1])
X = list(map(int, data[2:2+K]))
Q = int(data[2+K])

# Correctly parse the queries
queries = []
index = 2 + K + 1
for _ in range(Q):
    L = int(data[index])
    R = int(data[index + 1])
    queries.append((L, R))
    index += 2

# Initialize the array with zeros
seq = [0] * N

# Apply the something procedure K times
for jump in X:
    i = 0
    while i < N:
        seq[i] += 1
        i += jump

# Compute the prefix sums
prefix_sum = [0] * (N + 1)
for i in range(N):
    prefix_sum[i + 1] = prefix_sum[i] + seq[i]

# Answer each query
for L, R in queries:
    print(prefix_sum[R + 1] - prefix_sum[L])