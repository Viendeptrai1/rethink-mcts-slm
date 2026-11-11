MOD = 10**9 + 7

def count_ways(n, k):
    if n == 1:
        return k
    
    # Initialize the DP table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1] - dp[i - 1][j - 1]
            dp[i][j] %= MOD
    
    # The result is the number of ways to fill the grid with at least one 1 in each row and column
    result = pow(k, n, MOD) - dp[n][k]
    result %= MOD
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Output the result
print(count_ways(n, k))