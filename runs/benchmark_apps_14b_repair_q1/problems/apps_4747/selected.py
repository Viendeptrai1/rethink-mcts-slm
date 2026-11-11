def expected_score(n, k):
    # Initialize the DP table
    dp = [[0.0] * (k + 1) for _ in range(n + 1)]
    
    # Base case: if there's only one roll left, the expected value is the average of all faces
    for i in range(1, n + 1):
        dp[i][1] = (i + 1) / 2
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(2, k + 1):
            dp[i][j] = sum(dp[x][j - 1] for x in range(1, i + 1)) / i + i / 2
    
    # The answer is the expected score when starting with n sides and k rolls
    return dp[n][k]

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Calculate and print the result
print(expected_score(n, k))