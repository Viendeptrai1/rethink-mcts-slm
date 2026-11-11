import sys

def min_cost(n, k, a, b):
    # Initialize the DP table
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(k + 1):
            if j > 0:
                dp[i][j] = min(dp[i][j], dp[i - 1][j])
                dp[i][j] = min(dp[i][j], dp[i - 1][j - 1] + a[i - 1] + b[i - 1])
                if i > 1:
                    dp[i][j] = min(dp[i][j], dp[i - 2][j - 1] + a[i - 2] + b[i - 1])
            else:
                dp[i][j] = min(dp[i][j], dp[i - 1][j])
    
    return dp[n][k]

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:2 + n]))
b = list(map(int, data[2 + n:]))

# Calculate and print the result
result = min_cost(n, k, a, b)
print(result)