import sys
from collections import defaultdict

def solve():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    index += 1
    K = int(data[index])
    index += 1
    
    X = [int(data[index + i]) for i in range(K)]
    index += K
    
    Q = int(data[index])
    index += 1
    
    queries = [(int(data[index + 2 * i]), int(data[index + 2 * i + 1])) for i in range(Q)]
    
    # Using a dictionary to simulate the effect of the procedure
    seq = defaultdict(int)
    
    for jump in X:
        for i in range(jump - 1, N, jump):
            seq[i] += 1
    
    # Precompute prefix sums
    prefix_sums = [0] * (N + 1)
    for i in range(N):
        prefix_sums[i + 1] = prefix_sums[i] + seq[i]
    
    # Answer the queries
    results = []
    for L, R in queries:
        result = prefix_sums[R + 1] - prefix_sums[L]
        results.append(result)
    
    # Print results
    for result in results:
        print(result)