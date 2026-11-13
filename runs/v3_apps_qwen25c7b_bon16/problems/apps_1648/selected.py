from math import comb

def count_arrangements(N, K):
    MOD = 10**9 + 7
    result = [0] * K
    
    for k in range(1, K + 1):
        result[k-1] = comb(K, k-1) * comb(N-K+1, k)
        result[k-1] %= MOD
    
    return result

# Read input
N, K = map(int, input().split())

# Calculate and print results
results = count_arrangements(N, K)
for res in results:
    print(res)