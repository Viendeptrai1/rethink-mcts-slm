def min_rest_days(n, activities):
    dp = [[float('inf')] * 4 for _ in range(n + 1)]
    dp[0][0] = 0
    
    for i in range(1, n + 1):
        for j in range(4):
            if j == 0:
                dp[i][j] = min(dp[i-1][1], dp[i-1][2], dp[i-1][3])
            elif j == 1:
                dp[i][j] = min(dp[i-1][0], dp[i-1][2], dp[i-1][3]) + (activities[i-1] != 1)
            elif j == 2:
                dp[i][j] = min(dp[i-1][0], dp[i-1][1], dp[i-1][3]) + (activities[i-1] != 2)
            else:
                dp[i][j] = min(dp[i-1][0], dp[i-1][1], dp[i-1][2]) + (activities[i-1] != 3)
    
    return min(dp[n])

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
activities = list(map(int, data[1:]))

print(min_rest_days(n, activities))