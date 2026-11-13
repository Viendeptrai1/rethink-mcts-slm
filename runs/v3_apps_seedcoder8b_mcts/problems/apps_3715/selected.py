def min_rest_days(n, activities):
    # dp[i][0] - minimum rest days if the last day is a rest
    # dp[i][1] - minimum rest days if the last day is doing sport
    # dp[i][2] - minimum rest days if the last day is writing contest
    
    # Initialize dp array
    dp = [[float('inf')] * 3 for _ in range(n)]
    
    # Base case for the first day
    if activities[0] == 0:
        dp[0][0] = 1  # Rest
        dp[0][1] = float('inf')  # Can't do sport
        dp[0][2] = float('inf')  # Can't write contest
    elif activities[0] == 1:
        dp[0][0] = 1  # Rest
        dp[0][1] = float('inf')  # Can't do sport
        dp[0][2] = 0  # Write contest
    elif activities[0] == 2:
        dp[0][0] = 1  # Rest
        dp[0][1] = 0  # Do sport
        dp[0][2] = float('inf')  # Can't write contest
    elif activities[0] == 3:
        dp[0][0] = 1  # Rest
        dp[0][1] = 0  # Do sport
        dp[0][2] = 0  # Write contest
    
    # Fill the dp table
    for i in range(1, n):
        if activities[i] == 0:
            dp[i][0] = min(dp[i-1][0], dp[i-1][1], dp[i-1][2]) + 1
            dp[i][1] = float('inf')
            dp[i][2] = float('inf')
        elif activities[i] == 1:
            dp[i][0] = min(dp[i-1][0], dp[i-1][1], dp[i-1][2]) + 1
            dp[i][1] = float('inf')
            dp[i][2] = min(dp[i-1][0], dp[i-1][2])
        elif activities[i] == 2:
            dp[i][0] = min(dp[i-1][0], dp[i-1][1], dp[i-1][2]) + 1
            dp[i][1] = min(dp[i-1][0], dp[i-1][2])
            dp[i][2] = float('inf')
        elif activities[i] == 3:
            dp[i][0] = min(dp[i-1][0], dp[i-1][1], dp[i-1][2]) + 1
            dp[i][1] = min(dp[i-1][0], dp[i-1][2])
            dp[i][2] = min(dp[i-1][0], dp[i-1][1])
    
    # Return the minimum of the last day's rest, sport, and contest
    return min(dp[n-1][0], dp[n-1][1], dp[n-1][2])

# Read input
n = int(input())
activities = list(map(int, input().split()))

# Calculate and print the result
result = min_rest_days(n, activities)
print(result)