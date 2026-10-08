import sys
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
K = int(data[1])
jumps = list(map(int, data[2:2+K]))
Q = int(data[2+K])

# Initialize the array
seq = [0] * N

# Apply the jumps
for jump in jumps:
    for i in range(0, N, jump):
        seq[i] += 1

# Compute prefix sums
prefix_sum = [0] * (N + 1)
for i in range(N):
    prefix_sum[i + 1] = prefix_sum[i] + seq[i]

# Answer the queries
results = []
for i in range(2 + K + 1, 2 + K + 1 + Q * 2, 2):
    L = int(data[i])
    R = int(data[i + 1])
    results.append(prefix_sum[R + 1] - prefix_sum[L])

# Print the results
for result in results:
    print(result)