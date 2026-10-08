MOD = 10**6 + 7

def count_ways(N, M, K):
    dp = [[0] * (K + 1) for _ in range(N + 1)]
    dp[0][0] = 1
    
    for i in range(1, N + 1):
        for j in range(K + 1):
            dp[i][j] = dp[i - 1][j]
            if j >= 1:
                dp[i][j] = (dp[i][j] + dp[i][j - 1]) % MOD
            if j >= M + 1:
                dp[i][j] = (dp[i][j] - dp[i - 1][j - M - 1] + MOD) % MOD
    
    return dp[N][K]

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
M = int(data[1])
K = int(data[2])

# Output the result
print(count_ways(N, M, K))