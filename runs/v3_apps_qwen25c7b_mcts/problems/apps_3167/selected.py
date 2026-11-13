import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
K = int(data[1])
jumps = list(map(int, data[2:2+K]))
Q = int(data[2+K])
queries = [(int(data[2+K+2*i]), int(data[2+K+2*i+1])) for i in range(Q)]

def calculate_prefix_sums(N, jumps):
    prefix_sums = [0] * (N + 1)
    for jump in jumps:
        for i in range(jump - 1, N, jump):
            prefix_sums[i + 1] += 1
    return prefix_sums

prefix_sums = calculate_prefix_sums(N, jumps)

results = []
for L, R in queries:
    results.append(prefix_sums[R + 1] - prefix_sums[L])

for result in results:
    print(result)