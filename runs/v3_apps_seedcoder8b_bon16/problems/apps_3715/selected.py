def min_rest_days(n, activities):
    # dp[i][0] - Minimum rest days if the last day is a rest
    # dp[i][1] - Minimum rest days if the last day is sport
    # dp[i][2] - Minimum rest days if the last day is contest
    dp = [[0, float('inf'), float('inf')] for _ in range(n)]
    
    if activities[0] == 0:
        dp[0][0] = 1
    elif activities[0] == 1:
        dp[0][2] = 0
    elif activities[0] == 2:
        dp[0][1] = 0
    elif activities[0] == 3:
        dp[0][1] = 0
        dp[0][2] = 0
    
    for i in range(1, n):
        if activities[i] == 0:
            dp[i][0] = min(dp[i-1][0], dp[i-1][1], dp[i-1][2]) + 1
            dp[i][1] = float('inf')
            dp[i][2] = float('inf')
        elif activities[i] == 1:
            dp[i][0] = min(dp[i-1][0], dp[i-1][1], dp[i-1][2]) + 1
            dp[i][1] = float('inf')
            dp[i][2] = dp[i-1][0]
        elif activities[i] == 2:
            dp[i][0] = min(dp[i-1][0], dp[i-1][1], dp[i-1][2]) + 1
            dp[i][1] = dp[i-1][0]
            dp[i][2] = float('inf')
        elif activities[i] == 3:
            dp[i][0] = min(dp[i-1][0], dp[i-1][1], dp[i-1][2]) + 1
            dp[i][1] = dp[i-1][0]
            dp[i][2] = dp[i-1][0]
    
    return min(dp[n-1][0], dp[n-1][1], dp[n-1][2])

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    activities = list(map(int, data[1:]))
    
    result = min_rest_days(n, activities)
    print(result)