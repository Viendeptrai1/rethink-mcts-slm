MOD = 10**9 + 7

def count_ways(N, K):
    # dp[i][j] will store the number of ways to split j blue balls into i segments
    dp = [[0] * (K + 1) for _ in range(K + 1)]
    dp[0][0] = 1
    
    for i in range(1, K + 1):
        for j in range(i, K + 1):
            dp[i][j] = dp[i - 1][j - 1] + dp[i][j - 1]
            dp[i][j] %= MOD
    
    # Calculate the number of ways to arrange N balls with exactly i segments
    result = []
    for i in range(1, K + 1):
        ways = dp[i][K]
        # Choose i-1 positions out of N-K-1 gaps to place the segments
        ways *= comb(N - K - 1, i - 1)
        ways %= MOD
        result.append(ways)
    
    return result

def comb(n, k):
    if k > n:
        return 0
    if k == 0 or k == n:
        return 1
    k = min(k, n - k)
    c = 1
    for i in range(k):
        c = c * (n - i) // (i + 1)
    return c

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
K = int(data[1])

# Get the result
result = count_ways(N, K)

# Print the result
for r in result:
    print(r)