import sys

def min_cost(n, k, a, b):
    # Initialize the DP table with infinity
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    
    for i in range(1, n + 1):
        for j in range(k + 1):
            # Option 1: Do not prepare or print a problem on day i
            dp[i][j] = dp[i - 1][j]
            
            # Option 2: Prepare a problem on day i and print it on day i
            if j > 0:
                dp[i][j] = min(dp[i][j], dp[i - 1][j - 1] + a[i - 1] + b[i - 1])
            
            # Option 3: Prepare a problem on day i and print it on any previous day
            for l in range(i):
                if j > 0:
                    dp[i][j] = min(dp[i][j], dp[l][j - 1] + a[i - 1] + b[l])
    
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