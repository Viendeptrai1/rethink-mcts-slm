MOD = 10**6 + 7

def count_ways(N, M, K):
    # Initialize the DP table
    dp = [[0] * (K + 1) for _ in range(N + 1)]
    
    # Base case: There's one way to choose 0 objects from any number of types
    for i in range(N + 1):
        dp[i][0] = 1
    
    # Fill the DP table
    for i in range(1, N + 1):
        for j in range(1, K + 1):
            # Sum up all the ways to choose j objects considering the current type
            for k in range(M + 1):
                if j >= k:
                    dp[i][j] = (dp[i][j] + dp[i - 1][j - k]) % MOD
    
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