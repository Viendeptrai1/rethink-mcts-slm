import sys

def count_permutations(n, k, p):
    MOD = p
    
    # Initialize DP table
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    # Fill DP table
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            dp[i][j] = dp[i - 1][j - 1]
            if i > 1:
                dp[i][j] += dp[i - 1][j] * (i - 1)
                dp[i][j] %= MOD
    
    return dp[n][k]

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
p = int(data[2])

# Compute result
result = count_permutations(n, k, p)

# Print result
print(result)