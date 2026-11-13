def min_rest_days(n, activities):
    dp = [[float('inf')] * 4 for _ in range(n + 1)]
    
    # Base case initialization
    dp[0][0] = 0
    
    for i in range(1, n + 1):
        a = activities[i - 1]
        
        # Rest option
        dp[i][0] = min(dp[i - 1]) + 1
        
        # Contest option
        if a == 1 or a == 3:
            dp[i][1] = dp[i - 1][0]
        
        # Sport option
        if a == 2 or a == 3:
            dp[i][2] = dp[i - 1][0]
        
        # Both contest and sport options are not allowed
        dp[i][3] = float('inf')
    
    return min(dp[n])

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
activities = list(map(int, data[1:]))

# Output result
print(min_rest_days(n, activities))