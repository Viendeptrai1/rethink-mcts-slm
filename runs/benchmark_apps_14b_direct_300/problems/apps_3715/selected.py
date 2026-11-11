import sys

def min_rest_days(n, activities):
    # Initialize DP table with infinity
    dp = [[float('inf')] * 4 for _ in range(n)]
    
    # Base case initialization
    dp[0][0] = 0 if activities[0] == 0 else 1
    dp[0][1] = 0 if activities[0] == 1 else 1
    dp[0][2] = 0 if activities[0] == 2 else 1
    dp[0][3] = 0 if activities[0] == 3 else 1
    
    # Fill the DP table
    for i in range(1, n):
        if activities[i] == 0:
            dp[i][0] = min(dp[i-1][1], dp[i-1][2], dp[i-1][3])
        elif activities[i] == 1:
            dp[i][1] = min(dp[i-1][0], dp[i-1][2], dp[i-1][3])
        elif activities[i] == 2:
            dp[i][2] = min(dp[i-1][0], dp[i-1][1], dp[i-1][3])
        elif activities[i] == 3:
            dp[i][3] = min(dp[i-1][0], dp[i-1][1], dp[i-1][2])
    
    # Find the minimum value in the last row of the DP table
    return min(dp[n-1])

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
activities = list(map(int, data[1:]))

# Output the result
print(min_rest_days(n, activities))