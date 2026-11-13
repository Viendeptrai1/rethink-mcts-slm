from math import comb

def count_arrangements(N, K):
    MOD = 10**9 + 7
    result = [0] * K
    
    for i in range(1, K + 1):
        if N >= K:
            result[i-1] = comb(N - K, i - 1) % MOD
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
K = int(data[1])

# Calculate and print results
results = count_arrangements(N, K)
for result in results:
    print(result)