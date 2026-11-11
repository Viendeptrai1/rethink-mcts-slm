import sys

def min_rest_days(n, activities):
    # Initialize DP table
    dp = [[0] * 4 for _ in range(n)]
    
    # Base case
    dp[0][0] = 1 if activities[0] == 0 else 0
    dp[0][1] = 1 if activities[0] == 1 else 0
    dp[0][2] = 1 if activities[0] == 2 else 0
    dp[0][3] = 1 if activities[0] == 3 else 0
    
    # Fill DP table
    for i in range(1, n):
        for j in range(4):
            dp[i][j] = float('inf')
            if activities[i] == 0:
                dp[i][0] = min(dp[i][0], dp[i-1][0] + 1, dp[i-1][1] + 1, dp[i-1][2] + 1, dp[i-1][3] + 1)
            elif activities[i] == 1:
                dp[i][1] = min(dp[i][1], dp[i-1][0] + 1, dp[i-1][1] + 1, dp[i-1][2] + 1, dp[i-1][3] + 1)
                dp[i][1] = min(dp[i][1], dp[i-1][0])
            elif activities[i] == 2:
                dp[i][2] = min(dp[i][2], dp[i-1][0] + 1, dp[i-1][1] + 1, dp[i-1][2] + 1, dp[i-1][3] + 1)
                dp[i][2] = min(dp[i][2], dp[i-1][1])
            elif activities[i] == 3:
                dp[i][3] = min(dp[i][3], dp[i-1][0] + 1, dp[i-1][1] + 1, dp[i-1][2] + 1, dp[i-1][3] + 1)
                dp[i][3] = min(dp[i][3], dp[i-1][0], dp[i-1][2])
    
    # Find the minimum rest days
    return min(dp[n-1])

# Read input
n = int(sys.stdin.readline().strip())
activities = list(map(int, sys.stdin.readline().strip().split()))

# Output the result
print(min_rest_days(n, activities))