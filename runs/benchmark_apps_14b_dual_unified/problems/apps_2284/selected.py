import sys

def min_cost(n, k, a, b):
    # Initialize the DP table with infinity
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(k + 1):
            if j > 0:
                # Option 1: Prepare a new problem on day i
                dp[i][j] = min(dp[i][j], dp[i - 1][j - 1] + a[i - 1])
                # Option 2: Print the j-th problem on day i
                dp[i][j] = min(dp[i][j], dp[i - 1][j] + b[i - 1])
            else:
                # If no problems are prepared yet, just consider printing
                dp[i][j] = min(dp[i][j], dp[i - 1][j])
    
    return dp[n][k]

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:n+2]))
b = list(map(int, data[n+2:]))

# Calculate and print the result
print(min_cost(n, k, a, b))